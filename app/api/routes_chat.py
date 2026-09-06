import re
import base64
from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.orm import Session
from typing import Optional
from groq import Groq

from app.core.config import settings
from app.db.session import get_db
from app.db.models import Conversation, Message, Student
from app.services.rag_search import search_book_pages, build_context_block

router = APIRouter()

SYSTEM_PROMPT = """
انت الأستاذ نبيل، معلم رقمي خبير بالمنهج اللبناني الرسمي (CRDP). 

قواعد صارمة لازم تلتزم فيها دايماً بكل الإجابات:

1. الأسلوب واللغة: احكي دايماً عربي لبناني محكي لطيف ودافي بالشرح البسيط (مثل: "أهلاً بك يا بطل!"، "خليني اشرحلك ياه...").
2. الهيكلية والشرح للدروس والمسائل: عندما يسألك الطالب عن درس (مثل القوى، الجبر، أو الهندسة) أو يطلب حل مسألة، يجب أن تقسم إجابتك بشكل دقيق ومرتب كالتالي:
   - مقدمة مبسطة وشرح المفاهيم: شرح فكرة الدرس بأسلوب سلس ومثال واضح مع تحديد الأساس والأس (Base & Exponent) إن وجد.
   - حالات خاصة وقواعد ذهبية: ذكر القواعد الأساسية التي لا غنى عنها في المنهاج اللبناني.
   - العمليات والخطوات بالأمثلة: تفصيل الخطوات الرياضية (ضرب، قسمة، برهان) مع الأمثلة المرقمة.
   - الخلاصة والتشجيع: ختم الإجابة بعبارة تشجيعية دافئة.

3. في أسئلة الهندسة والبرهان: التزم بالنمط العلمي (Geometric Analysis, Key Theorem Application, Step-by-Step Conclusion) ولكن بلغة واضحة.

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


@router.post("/chat", response_model=ChatResponse)
async def chat(
    student_id: str = Form(...),
    message: str = Form(...),
    conversation_id: Optional[str] = Form(None),
    subject: Optional[str] = Form(None),
    grade: Optional[str] = Form(None),
    curriculum: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    if not settings.GROQ_API_KEY:
        raise HTTPException(500, "GROQ_API_KEY غير مضبوط بإعدادات السيرفر")

    image_base64 = None
    if image:
        contents = await image.read()
        image_base64 = f"data:{image.content_type};base64,{base64.b64encode(contents).decode('utf-8')}"

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

    saved_message_content = message if message else "[صورة]"
    db.add(Message(conversation_id=conversation.id, role="student", content=saved_message_content))
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

    text_part = message or "شو في بهالصورة؟ ساعدني افهمها."
    if context_block:
        text_part = f"{context_block}\n\nسؤال الطالب: {text_part}"

    role_map = {"student": "user", "teacher": "assistant"}
    history_messages = [
        {"role": role_map[m.role], "content": m.content}
        for m in previous_messages
    ]

    if image_base64:
        model = VISION_MODEL
        user_content = [
            {"type": "text", "text": text_part},
            {"type": "image_url", "image_url": {"url": image_base64}},
        ]
    else:
        model = TEXT_MODEL
        user_content = text_part

    client = Groq(api_key=settings.GROQ_API_KEY)
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *history_messages,
            {"role": "user", "content": user_content},
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
    )
