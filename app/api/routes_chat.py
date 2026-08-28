from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from openai import OpenAI

from app.core.config import settings
from app.db.session import get_db
from app.db.models import Conversation, Message

router = APIRouter()

SYSTEM_PROMPT = """
انت الأستاذ نبيل، معلم رياضيات وعلوم رقمي بيشرح للطلاب بطريقة بسيطة وودودة.
- احكي باللهجة اللبنانية المحكية (مش الفصحى) إلا إذا الطالب طلب فرنسي أو عربي فصيح.
- اشرح خطوة خطوة، وما تعطي الجواب النهائي مباشرة - وجّه الطالب ليوصل للحل بنفسه (أسلوب سقراطي).
- خليك مشجّع وصبور دائماً.
"""


class ChatRequest(BaseModel):
    student_id: str
    conversation_id: str | None = None
    message: str


class ChatResponse(BaseModel):
    conversation_id: str
    reply: str


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    if not settings.OPENAI_API_KEY:
        raise HTTPException(500, "OPENAI_API_KEY غير مضبوط بإعدادات السيرفر")

    # جلب أو إنشاء محادثة
    conversation = None
    if req.conversation_id:
        conversation = db.query(Conversation).filter_by(id=req.conversation_id).first()
    if conversation is None:
        conversation = Conversation(student_id=req.student_id)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    # حفظ رسالة الطالب
    db.add(Message(conversation_id=conversation.id, role="student", content=req.message))
    db.commit()

    # استدعاء نموذج الذكاء الاصطناعي
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": req.message},
        ],
    )
    reply_text = completion.choices[0].message.content

    # حفظ رد المعلم
    db.add(Message(conversation_id=conversation.id, role="teacher", content=reply_text))
    db.commit()

    return ChatResponse(conversation_id=conversation.id, reply=reply_text)
