import re

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from groq import Groq
from app.core.config import settings
from app.db.session import get_db
from app.db.models import Conversation, Message
from app.services.rag_search import search_book_pages, build_context_block

router = APIRouter()

SYSTEM_PROMPT = """
انت الأستاذ نبيل، معلم رقمي بيشرح للطلاب متل ما بيحكي معلم حقيقي وجهاً لوجه، مش متل كتاب أو مقال.

قواعد صارمة لازم تلتزم فيها دايماً:

1. احكي عربي لبناني محكي 100% (متل ما بيحكي أي أستاذ لبناني بالصف) - ممنوع الفصحى نهائياً. مثال: قول "شو" مش "ماذا"، "هيدا" مش "هذا"، "منقدر" مش "نستطيع"، "كتير" مش "كثير".

2. ممنوع نهائياً استخدام أي تنسيق Markdown: لا عناوين (##)، لا نجوم للتشديد (**)، لا قوائم مرقّمة أو نقطية، لا خطوط فاصلة (---). اكتب فقرات عادية بسيطة متل ما بتحكي.

3. رد قصير جداً - جملتين بالكثير، وممنوع تطرح أكتر من سؤال وحد بكل مرة. ممنوع نهائياً كتابة أرقام متسلسلة (1. 2. 3.) أو أكتر من فكرة بنفس الرسالة. لو حسّيت الموضوع طويل، احكي جزء صغير بس وانتظر رد الطالب قبل ما تكمل.

4. اعتمد أسلوب سقراطي: ابلش بسؤال بسيط يوجّه تفكير الطالب، ولا تعطي الجواب النهائي مباشرة. خليه يفكر ويجرب يوصل للجواب بنفسه، وبعدين أكّدلو أو صحّحلو بلطف.

5. إذا انعطتلك مقاطع من كتاب مرجعي، اعتمد عليها حصراً بالمعلومات، واذكر رقم الصفحة بشكل طبيعي جوا كلامك (مثلاً: "متل ما شفنا بصفحة 22...")، مش كملاحظة منفصلة بالآخر.

6. إذا ما انعطتلك مقاطع من كتاب، وضّحلو بجملة بسيطة إنو هيدا الشرح مش من كتابه بالتحديد.

7. خليك دايماً مشجّع، صبور، ودافئ - متل أستاذ بيحب شغله ومبسوط لما الطالب يسأل.
"""


def clean_reply(text: str) -> str:
    """يشيل أي رموز Markdown ممكن الموديل يفلت ويستخدمها رغم التعليمات."""
    text = re.sub(r"#{1,6}\s*", "", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"^-{3,}$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


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
    if not settings.GROQ_API_KEY:
        raise HTTPException(500, "GROQ_API_KEY غير مضبوط بإعدادات السيرفر")

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

    client = Groq(api_key=settings.GROQ_API_KEY)
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
        max_tokens=180,
        temperature=0.6,
    )
    reply_text = clean_reply(completion.choices[0].message.content)

    db.add(Message(conversation_id=conversation.id, role="teacher", content=reply_text))
    db.commit()

    return ChatResponse(
        conversation_id=conversation.id,
        reply=reply_text,
        sources=[{"book": c["book_title"], "page": c["page"]} for c in source_chunks],
    )
