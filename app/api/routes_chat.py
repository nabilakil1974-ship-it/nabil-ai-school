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

1. كشف اللغة والتكيف الفوري (مهم جداً): 
    - التزم دائماً بالرد على الطالب **بنفس اللغة التي استخدمها في سؤاله**:
      * إذا سأل باللغة **الإنجليزية**، أجب بالكامل باللغة **الإنجليزية** بأسلوب تربوي لطيف.
      * إذا سأل باللغة **الفرنسية**، أجب بالكامل باللغة **الفرنسية**.
      * إذا سأل باللغة **العربية**، أجب باللغة العربية بلهجة لبنانية محكية لطيفة ودافئة (مثل: "أهلاً بك يا بطل!").

2. التمييز الذكي بين السؤال والجواب:
    - إذا كان سؤاله مسألة جديدة، اشرحها خطوة بخطوة بالاستناد للمنهج.
    - إذا كان حلاً مقترحاً بخط يده أو بصوته، دقق خطواته وتأكد منها، وإذا وجد خطأ دلّه عليه بمحبة ولطف.

3. في أسئلة الهندسة والبرهان: التزم بالنمط العلمي بوضوح يتناسب مع لغة السؤال.

4. ممنوع نهائياً استخدام أي تنسيق Markdown معقد يفسد الشكل البصري، واستخدم الرموز الرياضية الواضحة. وفورا أجب بالحل النهائي بدون أي كتابة لعمليات التفكير الداخلية أو وسوم think.
"""

VISION_MODEL = "qwen/qwen3.6-27b"
TEXT_MODEL = "openai/gpt-oss-120b"

def clean_reply(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    if "</think>" in text:
        text = text.split("</think>")[-1]
    if "<think>" in text:
        text = text.split("<think>")[0]
    text = re.sub(r"#{1,6}\s*", "", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"^-{3,}$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

class ChatResponse(BaseModel):
    conversation_id: str
    reply: str
    sources: list[dict] = []
    transcribed_text: Optional[str] = None


# نقطة النهاية (Endpoint) الخاصة باستقبال الرسائل الصوتية من المايك
@router.post("/voice-chat", response_model=ChatResponse)
async def voice_chat(
    audio: UploadFile = File(...),
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
    
    # 1. قراءة الملف الصوتي المرفق من الواجهة الأمامية
    audio_bytes = await audio.read()
    
    # 2. تفريغ الصوت وتحويله لنص باستخدام نموذج Whisper (يدعم الإنجليزية والفرنسية والعربية تلقائياً وبدقة مذهلة)
    try:
        transcription = client.audio.transcriptions.create(
            file=(audio.filename or "voice.webm", audio_bytes),
            model="whisper-large-v3",
            prompt="Educational math and science context, supporting English, French, and Arabic.",
            response_format="text"
        )
        message = transcription.strip()
    except Exception as e:
        raise HTTPException(500, f"خطأ في معالجة الصوت: {str(e)}")

    if not message:
        message = "Hello teacher, please help me."

    # 3. متابعة نفس منطق الشات الطبيعي بعد استخراج النص الصوتي
    conversation = None
    if conversation_id:
        conversation = db.query(Conversation).filter_by(id=conversation_id).first()

    student = db.query(Student).filter_by(id=student_id).first()
    if student is None:
        student = Student(
            id=student_id,
            name=student_id,
            grade=grade or "غير محدد",
            preferred_language="ar-LB",
        )
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

    db.add(Message(conversation_id=conversation.id, role="student", content=f"[صوت] {message}"))
    db.commit()

    context_block = ""
    source_chunks = []
    if subject and grade and curriculum and message:
        source_chunks = search_book_pages(
            db=db,
            query=message,
            subject=subject,
            grade=grade,
            curriculum=curriculum,
        )
        context_block = build_context_block(source_chunks)

    text_part = message
    if context_block:
        text_part = f"{context_block}\n\nسؤال الطالب: {text_part}"

    role_map = {"student": "user", "teacher": "assistant"}
    history_messages = [
        {"role": role_map[m.role], "content": m.content}
        for m in previous_messages
    ]

    completion = client.chat.completions.create(
        model=TEXT_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *history_messages,
            {"role": "user", "content": text_part},
        ],
        max_tokens=4000,
        temperature=0.4,
    )

    raw_content = completion.choices[0].message.content or ""
    reply_text = clean_reply(raw_content)

    db.add(Message(conversation_id=conversation.id, role="teacher", content=reply_text))
    db.commit()

    return ChatResponse(
        conversation_id=conversation.id,
        reply=reply_text,
        sources=[{"book": c["book_title"], "page": c["page"]} for c in source_chunks],
        transcribed_text=message
    )
