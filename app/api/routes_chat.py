import re
import base64
from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from groq import Groq

from app.core.config import settings
from app.db.session import get_db
from app.db.models import Conversation, Message, Student
from app.services.rag_search import search_book_pages, build_context_block

router = APIRouter()

SYSTEM_PROMPT = """
انت الأستاذ نبيل، معلم رقمي خبير بالمنهج اللبناني الرسمي (CRDP). 

قواعد صارمة لازم تلتزم فيها دايماً بكل الإجابات:

1. كشف اللغة والتكيف الفوري: 
    - التزم دائماً بالرد على الطالب بنفس اللغة التي استخدمها في سؤاله (عربي بلهجة لبنانية محكية لطيفة ودافئة، إنجليزي، أو فرنسي).

2. الدخول المباشر وتنظيم الحل: ابدأ بالإجابة أو الشرح فوراً بدون مقدمات طويلة. رتب الحل دايماً بهالترتيب: المعطيات أولاً، بعدين القانون أو القاعدة المستخدمة، بعدين خطوات الحل تفصيلياً، وأخيراً النتيجة النهائية بارزة. ممنوع كتابة رموز LaTeX خام مثل \\text{} أو $...$ - اكتب المعادلات بشكل نص عادي مقروء.
"""

# أسماء النماذج الحقيقية والصحيحة المدعومة في Groq
VISION_MODEL = "llama-3.2-11b-vision-preview"
TEXT_MODEL = "llama3-70b-8192"

def clean_reply(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    if "</think>" in text:
        text = text.split("</think>")[-1]
    if "<think>" in text:
        text = text.split("<think>")[0]

    text = re.sub(r"\\text\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\\((.*?)\\\)", r"\1", text, flags=re.DOTALL)
    text = re.sub(r"\\\[(.*?)\\\]", r"\1", text, flags=re.DOTALL)
    text = re.sub(r"\$\$(.*?)\$\$", r"\1", text, flags=re.DOTALL)
    text = re.sub(r"\$(.*?)\$", r"\1", text)
    text = text.replace("\\,", " ").replace("\\perp", "⊥").replace("\\parallel", "∥")
    text = text.replace("\\sqrt", "جذر").replace("\\times", "×").replace("\\cdot", "×")
    text = re.sub(r"\\[a-zA-Z]+", "", text)
    return text.strip()

class ChatResponse(BaseModel):
    conversation_id: str
    reply: str
    sources: list[dict] = []
    transcribed_text: Optional[str] = None


@router.post("/chat", response_model=ChatResponse)
async def voice_chat(
    audio: Optional[UploadFile] = File(None),
    image: Optional[UploadFile] = File(None),
    message: Optional[str] = Form(None),
    student_id: str = Form(...),
    conversation_id: Optional[str] = Form(None),
    subject: Optional[str] = Form(None),
    grade: Optional[str] = Form(None),
    curriculum: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    if not settings.GROQ_API_KEY:
        raise HTTPException(500, "GROQ_API_KEY غير مضبوط بإعدادات السيرفر")

    client = Groq(api_key=settings.GROQ_API_KEY)

    if audio is not None:
        audio_bytes = await audio.read()
        try:
            transcription = client.audio.transcriptions.create(
                file=(audio.filename or "voice.webm", audio_bytes),
                model="whisper-large-v3",
                response_format="text"
            )
            message = transcription.strip()
        except Exception as e:
            raise HTTPException(500, f"خطأ في معالجة الصوت: {str(e)}")

    if image is not None:
        image_bytes = await image.read()
        encoded_image = base64.b64encode(image_bytes).decode('utf-8')
        mime_type = image.content_type or "image/jpeg"

        try:
            vision_response = client.chat.completions.create(
                model=VISION_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "استخرج بدقة نص الأسئلة أو التمرين الموجود في هذه الصورة."},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{encoded_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500,
            )
            extracted_text = vision_response.choices[0].message.content or ""
            message = f"{message}\n{extracted_text}" if message else extracted_text
        except Exception as e:
            print(f"⚠️ خطأ في قراءة الصورة: {e}", flush=True)

    if not message:
        message = "Hello teacher, please help me."

    conversation = db.query(Conversation).filter_by(id=conversation_id).first() if conversation_id else None
    student = db.query(Student).filter_by(id=student_id).first()
    if student is None:
        student = Student(id=student_id, name=student_id, grade=grade or "غير محدد", preferred_language="ar-LB")
        db.add(student)
        db.commit()

    if conversation is None:
        conversation = Conversation(student_id=student_id, subject=subject)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    previous_messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation.id)
        .order_by(Message.created_at.asc())
        .limit(10)
        .all()
    )

    db.add(Message(conversation_id=conversation.id, role="student", content=message))
    db.commit()

    context_block = ""
    source_chunks = []
    if subject and grade and curriculum and message:
        source_chunks = search_book_pages(db=db, query=message, subject=subject, grade=grade, curriculum=curriculum)
        context_block = build_context_block(source_chunks)

    text_part = f"{context_block}\n\nسؤال الطالب: {message}" if context_block else message
    role_map = {"student": "user", "teacher": "assistant"}
    history_messages = [{"role": role_map[m.role], "content": m.content} for m in previous_messages]

    completion = client.chat.completions.create(
        model=TEXT_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *history_messages,
            {"role": "user", "content": text_part},
        ],
        max_tokens=2000,
        temperature=0.4,
    )

    reply_text = clean_reply(completion.choices[0].message.content or "")

    db.add(Message(conversation_id=conversation.id, role="teacher", content=reply_text))
    db.commit()

    return ChatResponse(
        conversation_id=conversation.id,
        reply=reply_text,
        sources=[{"book": c["book_title"], "page": c["page"]} for c in source_chunks],
        transcribed_text=message
    )
