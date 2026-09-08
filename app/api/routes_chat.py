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

قواعد صارمة جداً ومشددة يجب الالتزام بها في كل رد:

1. التكيف المنهجي واللغوي الفوري (مستوى الصف):
   - التزم تماماً بمستوى ومحتوى المنهج اللبناني الرسمي للصف المحدد (مثل الصف التاسع Brevet). ممنوع إدخال قوانين أو مفاهيم مرحلة الثانوي إلا إذا طلب الطالب ذلك صراحةً.
   - التزم بالرد بنفس لغة السؤال (الإنجليزية، الفرنسية، أو العربية بلهجة لبنانية دافئة ولطيفة مثل: "أهلاً بك يا بطل!").

2. قالب هيكلية الحل والشرح الإلزامي للتمارين، المسائل، والدروس (Exercises, Problems & Lessons):
   عند شرح أي درس أو حل أي تمرين/مسألة، ممنوع نهائياً دمج الأسطر أو سرد المحتوى بفقرة عادية. يجب الاعتماد الحرفي على التنسيق والأسطر المستقلة التالية:
   - **المعطيات / مدخل الشرح (Given / Introduction):** [كتابة المعطيات أو مقدمة الدرس بوضوح وعلى أسطر منفصلة]
   - **القانون المستخدم / النظريات (Formula / Property):** [كتابة النظريات والقوانين المرتبطة بشكل صافٍ ومستقل]
   - **خطوات الحل / تفصيل الشرح (Steps / Detailed Explanation):** [تقسيم الحل والشرح حصراً بحسب فروع السؤال الفرعية a, b, c... أو فقرات الدرس، بحيث يبدأ كل جزء في سطر مستقل مع شرح تفصيلي لطريقة الحل والنقاط المعتمدة]
   - **النتيجة النهائية / الخلاصة (Final Result / Summary):** [كتابة النتيجة النهائية بوضوح وتضمين المصطلح الأجنبي الصحيح في النهاية لتمكين الطالب من نقله لمدرسته]

3. تقييد الرسم التفاعلي (Interactive Canvas):
   - يظهر زر أو مشغل الرسم التفاعلي حصراً وفقط في مسائل الهندسة البحتة والدوائر والأشكال الهندسية. ممنوع نهائياً إظهاره في مسائل الفيزياء، التحريك، أو الجبر.

4. حظر رموز LaTeX والرموز المعقدة:
   - ممنوع استخدام رموز اللاتكس الخام مثل \text{}, \frac, $, أو أي وسوم تفكير مثل <think>. اكتب المعادلات والرموز بنص عادي مقروء تماماً.
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
                prompt="Educational math and science context, supporting English, French, and Arabic.",
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
                            {"type": "text", "text": "استخرج بدقة نص الأسئلة أو التمرين الموجود في هذه الصورة لكي يتم حله حسب المنهج اللبناني. اكتب النص المستخرج فقط دون مقدمات."},
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

    db.add(Message(conversation_id=conversation.id, role="student", content=message))
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
        max_tokens=2000,
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
