import re
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.core.config import settings
from app.db.session import get_db
from app.db.models import Conversation, Message, Student
from app.services.rag_search import search_book_pages, build_context_block
from app.services.ai_gateway import NabilAIGateway

router = APIRouter()

SYSTEM_PROMPT = """
أنت NABIL AI، الأستاذ نبيل، معلّم رقمي ذكي وخبير بالمنهج اللبناني الرسمي CRDP.

أجب بنفس لغة الطالب، وكن معلماً تفاعلياً يساعده على الفهم وليس مجرد إعطاء الإجابة.

إذا توفر محتوى CRDP/RAG فاعتبره المرجع الأساسي، ولا تخترع محتوى منهجياً.

في الرياضيات:
- ابدأ بالمعطيات عند الحاجة.
- اذكر القاعدة أو القانون.
- اعرض خطوات الحل بوضوح.
- أعط النتيجة النهائية.
- استخدم الرموز الرياضية الواضحة.

في الهندسة والبرهان:
- التحليل الهندسي.
- تحديد النظرية المناسبة.
- خطوات البرهان.
- النتيجة.

إذا أرسل الطالب صورة:
- اقرأ المسألة بدقة.
- استخرج المعلومات الظاهرة في الصورة.
- لا تفترض معلومات غير موجودة.
- ساعد الطالب في الحل خطوة بخطوة.

لا تعرض عمليات التفكير الداخلية.
"""

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


class ChatRequest(BaseModel):
    student_id: str
    conversation_id: Optional[str] = None
    message: str
    subject: Optional[str] = None
    grade: Optional[str] = None
    curriculum: Optional[str] = None
    image_base64: Optional[str] = None


class ChatResponse(BaseModel):
    conversation_id: str
    reply: str
    sources: list[dict] = []


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, db: Session = Depends(get_db)):

    try:
        ai = NabilAIGateway()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"خطأ في إعداد NABIL AI: {str(e)}",
        )

    conversation = None

    if req.conversation_id:
        conversation = (
            db.query(Conversation)
            .filter_by(id=req.conversation_id)
            .first()
        )

    student = (
        db.query(Student)
        .filter_by(id=req.student_id)
        .first()
    )

    if student is None:
        student = Student(
            id=req.student_id,
            name=req.student_id,
            grade=req.grade or "غير محدد",
            preferred_language="ar-LB",
        )

        db.add(student)
        db.commit()

    if conversation is None:
        conversation = Conversation(
            student_id=req.student_id,
            subject=req.subject,
        )

        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    previous_messages = (
        db.query(Message)
        .filter(
            Message.conversation_id == conversation.id
        )
        .order_by(Message.created_at.asc())
        .limit(10)
        .all()
    )

    saved_message_content = (
        req.message
        if req.message
        else "[صورة]"
    )

    db.add(
        Message(
            conversation_id=conversation.id,
            role="student",
            content=saved_message_content,
        )
    )

    db.commit()

    context_block = ""
    source_chunks = []

    if (
        req.subject
        and req.grade
        and req.curriculum
        and req.message
    ):
        try:
            source_chunks = search_book_pages(
                db=db,
                query=req.message,
                subject=req.subject,
                grade=req.grade,
                curriculum=req.curriculum,
            )

            context_block = build_context_block(
                source_chunks
            )

        except Exception as e:
            print(
                f"RAG warning: {e}",
                flush=True,
            )

    text_part = (
        req.message
        or "ساعدني في فهم هذه الصورة."
    )

    if context_block:
        text_part = (
            f"{context_block}\n\n"
            f"سؤال الطالب: {text_part}"
        )

    role_map = {
        "student": "user",
        "teacher": "assistant",
    }

    history_messages = [
        {
            "role": role_map.get(
                m.role,
                "user",
            ),
            "content": m.content,
        }
        for m in previous_messages
    ]

    image_bytes = None
    image_mime_type = "image/jpeg"

    if req.image_base64:
        try:
            if "," in req.image_base64:
                header, encoded_data = (
                    req.image_base64.split(",", 1)
                )

                if "image/" in header:
                    image_mime_type = (
                        header.split("image/", 1)[1]
                        .split(";", 1)[0]
                    )

                import base64

                image_bytes = base64.b64decode(
                    encoded_data
                )
            else:
                import base64

                image_bytes = base64.b64decode(
                    req.image_base64
                )

        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"خطأ في قراءة الصورة: {str(e)}",
            )

    history_messages.append(
        {
            "role": "user",
            "content": text_part,
        }
    )

    try:
        reply_text = ai.generate(
            instructions=SYSTEM_PROMPT,
            messages=history_messages,
            image_bytes=image_bytes,
            image_mime_type=image_mime_type,
            max_output_tokens=2000,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"خطأ في NABIL AI: {str(e)}",
        )

    reply_text = clean_reply(reply_text)

    if not reply_text:
        raise HTTPException(
            status_code=500,
            detail="NABIL AI لم يُرجع إجابة.",
        )

    db.add(
        Message(
            conversation_id=conversation.id,
            role="teacher",
            content=reply_text,
        )
    )

    db.commit()

    return ChatResponse(
        conversation_id=str(conversation.id),
        reply=reply_text,
        sources=[
            {
                "book": c.get("book_title"),
                "page": c.get("page"),
            }
            for c in source_chunks
        ],
    )
