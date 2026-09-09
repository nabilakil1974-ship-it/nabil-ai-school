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
You are Professor Nabil, an expert digital teacher of the official Lebanese Curriculum (CRDP) for Grade 9 and Secondary levels.

CRITICAL INSTRUCTION FOR MATH & SYMBOLS:
- Always use clear standard mathematical notation and keep LaTeX formatting wrapped properly with $ or $$ so the frontend can render equations (like $x^2 + y^2 = 25$ and $\Delta$) correctly.

You must ALWAYS output your responses using this exact structure and formatting template word-for-word, ensuring clear line breaks between each section:

**رقم التمرين:** [Write Exercise/Problem number here]

**المعطيات / مدخل الشرح (Given / Introduction):**  
- [Write the given information here]

**الرسم التوضيحي الهندسي (Geometric Construction):**  
- [Describe the exact geometrical layout and figures matching the question]

**القانون المستخدم / النظريات (Formula / Property):**  
- [Write formulas or properties here]

**خطوات الحل / تفصيل الشرح (Steps / Detailed Explanation):**  
- a) [First step]  
- b) [Second step]  
- c) [Third step]  

**النتيجة النهائية / الخلاصة (Final Result / Summary):**  
- [Write final results with scientific terms]

Strict rules:
- Never use tags like <think>.
- Keep the exact headings and structure as shown above for every response.
"""

VISION_MODEL = "qwen/qwen2-vl-7b-instruct"
TEXT_MODEL = "llama-3.3-70b-versatile"

def clean_reply(text: str) -> str:
    """دالة تنظيف مع الحفاظ على الرموز الرياضية وتنسيق الـ LaTeX للرؤية الصحيحة"""
    if not text:
        return ""
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    if "</think>" in text:
        text = text.split("</think>")[-1]
    if "<think>" in text:
        text = text.split("<think>")[0]
    
    # تم إزالة إزالة الـ $ الحافظة للرياضيات لكي يتم عرض الرموز والمعادلات بشكل صحيح
    text = re.sub(r"#{1,6}\s*", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
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
                            {"type": "text", "text": "Extract problem text briefly."},
                            {"image_url": {"url": f"data:{mime_type};base64,{encoded_image}"}, "type": "image_url"}
                        ]
                    }
                ],
                max_tokens=150,
            )
            extracted_text = vision_response.choices[0].message.content or ""
            message = f"{message}\n{extracted_text}" if message else extracted_text
        except Exception as e:
            print(f"⚠️ خطأ في قراءة الصورة: {e}", flush=True)

    if not message:
        message = "مرحباً أستاذ، يرجى مساعدتي في هذا التمرين."

    conversation = None
    if conversation_id:
        conversation = db.query(Conversation).filter_by(id=conversation_id).first()

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
        .order_by(Message.created_at.desc())
        .limit(1)
        .all()
    )
    previous_messages.reverse()

    db.add(Message(conversation_id=conversation.id, role="student", content=message))
    db.commit()

    context_block = ""
    source_chunks = []
    if subject and grade and curriculum and message:
        source_chunks = search_book_pages(db=db, query=message, subject=subject, grade=grade, curriculum=curriculum)
        if source_chunks:
            source_chunks = source_chunks[:1] 
        context_block = build_context_block(source_chunks)

    text_part = message
    if context_block:
        text_part = f"{context_block}\n\nStudent Question: {text_part}"

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
        max_tokens=800,
        temperature=0.3,
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
