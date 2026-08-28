from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import google.generativeai as genai

from app.core.config import settings
from app.db.session import get_db
from app.db.models import Conversation, Message
from app.services.rag_search import search_book_pages, build_context_block

router = APIRouter()

SYSTEM_PROMPT = """
انت الأستاذ نبيل، معلم رياضيات وعلوم رقمي بيشرح للطلاب بطريقة بسيطة وودودة.
- احكي باللهجة اللبنانية المحكية (مش الفصحى) إلا إذا الطالب طلب فرنسي أو عربي فصيح.
- اشرح خطوة خطوة، وما تعطي الجواب النهائي مباشرة - وجّه الطالب ليوصل للحل بنفسه (أسلوب سقراطي).
- إذا انعطتلك مقاطع من الكتاب المرجعي، اعتمد عليها حصراً بالشرح واذكر رقم
  الصفحة بالضبط متل ما هو معطى لك - لا تخترع رقم صفحة أبداً.
- إذا ما انعطتلك مقاطع من كتاب، اشرح من معرفتك العامة بس نبّه الطالب إنو
  هاد الشرح مش موخوذ من كتابه بالتحديد.
- خليك مشجّع وصبور دائماً.
"""


class ChatRequest(BaseModel):
    student_id: str
    conversation_id: str | None = None
    message: str
    subject: str | None = None
    grade: str | None = None
    curriculum: str | None = None


class ChatResponse(BaseModel):
    conversation_id: str
    reply: str
    sources: list[dict] = []


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    if not settings.GEMINI_API_KEY:
        raise HTTPException(500, "GEMINI_API_KEY غير مضبوط بإعدادات السيرفر")

    conversation = None
    if req.conversation_id:
        conversation = db.query(Conversation).filter_by(id=req.conversation_id).first()
    if conversation is None:
        conversation = Conversation(student_id=req.student_id, subject=req.subject)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    db.add(Message(conversation_id=conversation.id, role="student", content=req.message))
    db.commit()

    context_block = ""
    source_chunks = []
    if req.subject and req.grade and req.curriculum:
        source_chunks = search_book_pages(
            db=db,
            query=req.message,
            subject=req.subject,
            grade=req.grade,
            curriculum=req.curriculum,
        )
        context_block = build_context_block(source_chunks)

    user_content = req.message
    if context_block:
        user_content = f"{context_block}\n\nسؤال الطالب: {req.message}"

    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT,
    )
    response = model.generate_content(user_content)
    reply_text = response.text

    db.add(Message(conversation_id=conversation.id, role="teacher", content=reply_text))
    db.commit()

    return ChatResponse(
        conversation_id=conversation.id,
        reply=reply_text,
        sources=[{"book": c["book_title"], "page": c["page"]} for c in source_chunks],
    )
