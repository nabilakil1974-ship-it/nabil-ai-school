import re
import base64
import traceback
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

CRITICAL DRAWING & GEOMETRIC INSTRUCTION:
- Whenever a student asks a geometry problem involving shapes, you MUST include a clear geometric construction or precise step-by-step layout breakdown.
- Ensure the description strictly adheres to the exact names of points and conditions.

You must ALWAYS output your responses using this exact structure:

**رقم التمرين:** [Write Exercise/Problem number here]

**المعطيات / مدخل الشرح (Given / Introduction):**  
- [Write the given information here]

**الرسم التوضيحي الهندسي (Geometric Construction):**  
- [Describe the exact geometrical layout]

**القانون المستخدم / النظريات (Formula / Property):**  
- [Write formulas or properties here]

**خطوات الحل / تفصيل الشرح (Steps / Detailed Explanation):**  
- a) [First step]  
- b) [Second step]  

**النتيجة النهائية / الخلاصة (Final Result / Summary):**  
- [Write final results]
"""

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
    student_id: str = Form("default_student"),
    conversation_id: Optional[str] = Form(None),
    subject: Optional[str] = Form(None),
    grade: Optional[str] = Form(None),
    curriculum: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    try:
        api_key = settings.GROQ_API_KEY if settings and hasattr(settings, "GROQ_API_KEY") else None
        if not api_key:
            import os
            api_key = os.getenv("GROQ_API_KEY", "")
        
        client = Groq(api_key=api_key) if api_key else None

        if not message:
            message = "مرحباً يا أستاذ، أرجو مساعدتي في هذا التمرين."

        # معالجة الصوت
        if audio is not None and client:
            try:
                audio_bytes = await audio.read()
                transcription = client.audio.transcriptions.create(
                    file=(audio.filename or "voice.webm", audio_bytes),
                    model="whisper-large-v3",
                    response_format="text"
                )
                message = transcription.strip()
            except Exception as e:
                print(f"⚠️ خطأ الصوت: {e}")

        # معالجة الصورة
        if image is not None and client:
            try:
                image_bytes = await image.read()
                encoded_image = base64.b64encode(image_bytes).decode('utf-8')
                mime_type = image.content_type or "image/jpeg"
                vision_response = client.chat.completions.create(
                    model=VISION_MODEL,
                    messages=[{"role": "user", "content": [{"type": "text", "text": "Extract exercise details."}, {"image_url": {"url": f"data:{mime_type};base64,{encoded_image}"}, "type": "image_url"}]}],
                    max_tokens=1000,
                )
                extracted_text = vision_response.choices[0].message.content or ""
                message = f"{message}\n{extracted_text}" if message else extracted_text
            except Exception as e:
                print(f"⚠️ خطأ الصورة: {e}")

        conv_id = conversation_id or "default_conv"
        try:
            student = db.query(Student).filter_by(id=student_id).first()
            if student is None:
                student = Student(id=student_id, name=student_id, grade=grade or "غير محدد", preferred_language="ar-LB")
                db.add(student)
                db.commit()

            conversation = db.query(Conversation).filter_by(id=conv_id).first() if conversation_id else None
            if conversation is None:
                conversation = Conversation(student_id=student_id, subject=subject)
                db.add(conversation)
                db.commit()
                db.refresh(conversation)
                conv_id = conversation.id
            
            db.add(Message(conversation_id=conv_id, role="student", content=message))
            db.commit()
        except Exception as db_err:
            print(f"⚠️ خطأ قاعدة البيانات: {db_err}")

        # البحث في الكتب (RAG)
        context_block = ""
        source_chunks = []
        try:
            if subject and grade and curriculum and message:
                source_chunks = search_book_pages(db=db, query=message, subject=subject, grade=grade, curriculum=curriculum)
                context_block = build_context_block(source_chunks)
        except Exception as rag_err:
            print(f"⚠️ خطأ RAG: {rag_err}")

        text_part = f"{context_block}\n\nStudent Question: {message}" if context_block else message

        reply_text = ""
        if client:
            try:
                completion = client.chat.completions.create(
                    model=TEXT_MODEL,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": text_part}
                    ],
                    max_tokens=2000,
                    temperature=0.4,
                )
                reply_text = clean_reply(completion.choices[0].message.content or "")
            except Exception as ai_err:
                print(f"⚠️ خطأ Groq API: {ai_err}")

        # إذا عجز الذكاء الاصطناعي عن الإجابة، لا نؤلف أبداً بل نعتذر بوضوح تام ضمن الهيكل الأكاديمي
        if not reply_text:
            reply_text = (
                "**رقم التمرين:** غير محدد\n\n"
                "**المعطيات / مدخل الشرح (Given / Introduction):**\n"
                "- تعذر معالجة السؤال حالياً نظراً لضغط الاتصال أو عدم توفر النموذج.\n\n"
                "**الرسم التوضيحي الهندسي (Geometric Construction):**\n"
                "- يرجى إعادة صياغة السؤال أو إرساله مرة أخرى.\n\n"
                "**القانون المستخدم / النظريات (Formula / Property):**\n"
                "- غير متوفر حالياً.\n\n"
                "**خطوات الحل / تفصيل الشرح (Steps / Detailed Explanation):**\n"
                "- أ) نعتذر منك يا بطل، حدث ضغط مؤقت في الخادم.\n"
                "- ب) يرجى إعادة إرسال السؤال أو المحاولة بعد قليل لضمان إعطائك الحل الدقيق 100%.\n\n"
                "**النتيجة النهائية / الخلاصة (Final Result / Summary):**\n"
                "- يرجى إعادة المحاولة."
            )

        return ChatResponse(
            conversation_id=conv_id,
            reply=reply_text,
            sources=[{"book": c.get("book_title", ""), "page": c.get("page", 0)} for c in source_chunks],
            transcribed_text=message
        )

    except Exception as e:
        print(f"🔥 خطأ فادح غير متوقع: {str(e)}", flush=True)
        traceback.print_exc()
        
        # رد اعتذار رسمي وواضح بدون تأليف أي معلومات علمية خاطئة
        error_reply = (
            "**رقم التمرين:** تنبيه النظام\n\n"
            "**المعطيات / مدخل الشرح (Given / Introduction):**\n"
            "- حدث خطأ تقني مؤقت أثناء الاتصال بمحرك الذكاء الاصطناعي.\n\n"
            "**الرسم التوضيحي الهندسي (Geometric Construction):**\n"
            "- لا يوجد رسم متاح حالياً.\n\n"
            "**القانون المستخدم / النظريات (Formula / Property):**\n"
            "- غير متوفر.\n\n"
            "**خطوات الحل / تفصيل الشرح (Steps / Detailed Explanation):**\n"
            "- أ) نعتذر منك يا بطل، لتفادي إعطائك أي إجابة خاطئة.\n"
            "- ب) يرجى إعادة المحاولة وإرسال السؤال مرة أخرى بعد ثوانٍ.\n\n"
            "**النتيجة النهائية / الخلاصة (Final Result / Summary):**\n"
            "- حاول مجدداً لضمان دقة الحل العلمي."
        )
        
        return ChatResponse(
            conversation_id="error_conv",
            reply=error_reply,
            sources=[],
            transcribed_text=message or "سؤال"
        )
