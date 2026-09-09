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

# إنشاء موجه المسارات الخاص بـ FastAPI
router = APIRouter()

# البرومبت الأساسي الذي يحدد شخصية وقواعد الأستاذ نبيل وتنسيق البطاقة الأكاديمية
SYSTEM_PROMPT = """
You are Professor Nabil, an expert digital teacher of the official Lebanese Curriculum (CRDP) for Grade 9 (Brevet).

You must ALWAYS output your responses using this exact structure and formatting template word-for-word, ensuring clear line breaks between each section:

**رقم التمرين:** [Write Exercise/Problem number here]

**المعطيات / مدخل الشرح (Given / Introduction):**  
- [Write the given information here]

**القانون المستخدم / النظريات (Formula / Property):**  
- [Write formulas or properties here]

**خطوات الحل / تفصيل الشرح (Steps / Detailed Explanation):**  
- a) [First step]  
- b) [Second step]  
- c) [Third step]  

**النتيجة النهائية / الخلاصة (Final Result / Summary):**  
- [Write final results with scientific terms]

Strict rules:
- Never use raw LaTeX like \\text, $, or tags like <think>.
- Keep the exact headings and structure as shown above for every response.
"""

# تعريف نماذج الذكاء الاصطناعي المستخدمة (الرؤية والنصوص)
VISION_MODEL = "qwen/qwen3.6-27b"
TEXT_MODEL = "openai/gpt-oss-120b"

def clean_reply(text: str) -> str:
    """دالة لتنظيف النص الصادر من الذكاء الاصطناعي وإزالة الوسوم والرموز غير المرغوب فيها"""
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
    text = re.sub(r"#{1,6}\s*", "", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"^-{3,}$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

class ChatResponse(BaseModel):
    """نموذج بيانات الاستجابة المُرسلة إلى الواجهة الأمامية"""
    conversation_id: str
    reply: str
    sources: list[dict] = []
    transcribed_text: Optional[str] = None


@router.post("/chat", response_model=ChatResponse)
async def voice_chat(
    audio: Optional[UploadFile] = File(None),              # استقبال ملف الصوت (إن وجد)
    image: Optional[UploadFile] = File(None),              # استقبال الصورة المرفقة (إن وجدت)
    message: Optional[str] = Form(None),                   # النص المكتوب من المستخدم
    student_id: str = Form(...),                         # معرف الطالب
    conversation_id: Optional[str] = Form(None),           # معرف المحادثة الحالي للحفاظ على الذاكرة
    subject: Optional[str] = Form(None),                   # المادة الدراسية
    grade: Optional[str] = Form(None),                     # الصف الدراسي
    curriculum: Optional[str] = Form(None),                # المنهج المعتمد
    db: Session = Depends(get_db)                          # اتصال قاعدة البيانات
):
    # التحقق من وجود مفتاح API الخاص بـ Groq
    if not settings.GROQ_API_KEY:
        raise HTTPException(500, "GROQ_API_KEY غير مضبوط بإعدادات السيرفر")

    client = Groq(api_key=settings.GROQ_API_KEY)

    # 1. معالجة الملف الصوتي وتحويله لنص عبر Whisper
    if audio is not None:
        audio_bytes = await audio.read()
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

    # 2. معالجة الصورة المرفقة واستخراج التمارين منها عبر نموذج الرؤية
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
                            {"type": "text", "text": "Extract precisely the text of the exercise from this image according to the Lebanese curriculum. Write only the extracted text."},
                            {
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{encoded_image}"
                                },
                                "type": "image_url"
                            }
                        ]
                    }
                ],
                max_tokens=500,
            )
            extracted_text = vision_response.choices[0].message.content or ""
            if message:
                message = f"{message}\n{extracted_text}"
            else:
                message = extracted_text
        except Exception as e:
            print(f"⚠️ خطأ في قراءة الصورة عبر نموذج الرؤية: {e}", flush=True)

    if not message:
        message = "Hello teacher, please help me."

    # 3. إدارة جلسات المحادثة والطلاب في قاعدة البيانات
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

    # 4. استرجاع كامل رسائل المحادثة السابقة (بدون حد أقصى) لضمان تذكر كل الصور والتمارين السابقة
    previous_messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation.id)
        .order_by(Message.created_at.asc())
        .all()  # تم إزالة الـ limit لضمان عدم نسيان أي سياق قديم
    )

    # حفظ رسالة الطالب الجديدة في قاعدة البيانات
    db.add(Message(conversation_id=conversation.id, role="student", content=message))
    db.commit()

    # 5. البحث في الكتب المدرسية (RAG) لإحضار الصفحات والمصادر ذات الصلة
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
        text_part = f"{context_block}\n\nStudent Question: {text_part}"

    # تجهيز سجل المحادثات لإرساله إلى نموذج الذكاء الاصطناعي
    role_map = {"student": "user", "teacher": "assistant"}
    history_messages = [
        {"role": role_map[m.role], "content": m.content}
        for m in previous_messages
    ]

    # 6. إرسال الطلب والسياق الكامل إلى نموذج النصوص لتوليد الرد الأكاديمي
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

    raw_content = completion.choices[0].message.content or ""
    reply_text = clean_reply(raw_content)

    # حفظ رد الأستاذ نبيل في قاعدة البيانات
    db.add(Message(conversation_id=conversation.id, role="teacher", content=reply_text))
    db.commit()

    # إرجاع الاستجابة النهائية للواجهة
    return ChatResponse(
        conversation_id=conversation.id,
        reply=reply_text,
        sources=[{"book": c["book_title"], "page": c["page"]} for c in source_chunks],
        transcribed_text=message
    )
