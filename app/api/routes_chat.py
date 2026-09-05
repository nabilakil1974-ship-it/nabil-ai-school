import re

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from groq import Groq
from app.core.config import settings
from app.db.session import get_db
from app.db.models import Conversation, Message, Student
from app.services.rag_search import search_book_pages, build_context_block

router = APIRouter()

SYSTEM_PROMPT = """
انت الأستاذ نبيل، معلم رقمي خبير بالمنهج اللبناني الرسمي (CRDP). 

قواعد صارمة لازم تلتزم فيها دايماً:

1. احكي عربي لبناني محكي لطيف بالشرح البسيط، ولكن في أسئلة الهندسة، الجبر، والمسائل البرهانية الرياضية، يجب أن تقدم الإجابة بالنمط العلمي والمنظم التالي:
   - **Geometric Analysis & Given Data:** تفصيل المعطيات بدقة.
   - **Key Theorem Application:** ذكر النظريات الهندسية المستخدمة بوضوح (مثل خواص المماسات والدوائر).
   - **Proving & Step-by-Step Conclusion:** كتابة البرهان الرياضي خطوة بخطوة للوصول إلى النتيجة المطلوبة.

2. مقاطع الكتاب المرجعي قد تكون بالإنكليزي أو الفرنسي؛ افهمها وشرحها بلهجتك اللبنانية مع ذكر المصطلحات العلمية الضرورية وتفسيرها فوراً.

3. إذا طلب الطالب "حل مباشر" أو "أنا مستعجل"، أو إذا كان السؤال عبارة عن برهان هندسي رياضي، قدم الحل الكامل والمفصل فوراً بلا تقييد بطول قصير جداً، لضمان فهم البرهان الهندسي كاملاً.

4. انتبه لتاريخ المحادثة السابق مع الطالب لضمان الاستمرارية وعدم القفز لموضوع جديد كلياً.

5. ممنوع نهائياً استخدام أي تنسيق Markdown معقد يفسد الشكل، لكن حافظ على وضوح وترتيب خطوات البرهان الرياضي.

6. خليك دايماً مشجع، صبور، ودافئ - متل أستاذ بيحب شغله ومبسوط لما الطالب يسأل.
"""

VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
TEXT_MODEL = "openai/gpt-oss-120b"


def clean_reply(text: str) -> str:
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
    image_base64: str | None = None


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

    student = db.query(Student).filter_by(id=req.student_id).first()
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
        conversation = Conversation(student_id=req.student_id, subject=req.subject)
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

    saved_message_content = req.message if req.message else "[صورة]"
    db.add(Message(conversation_id=conversation.id, role="student", content=saved_message_content))
    db.commit()

    context_block = ""
    source_chunks = []
    if req.subject and req.grade and req.curriculum and req.message:
        source_chunks = search_book_pages(
            db=db,
            query=req.message,
            subject=req.subject,
            grade=req.grade,
            curriculum=req.curriculum,
        )
        context_block = build_context_block(source_chunks)

    text_part = req.message or "شو في بهالصورة؟ ساعدني افهمها."
    if context_block:
        text_part = f"{context_block}\n\nسؤال الطالب: {text_part}"

    role_map = {"student": "user", "teacher": "assistant"}
    history_messages = [
        {"role": role_map[m.role], "content": m.content}
        for m in previous_messages
    ]

    if req.image_base64:
        model = VISION_MODEL
        user_content = [
            {"type": "text", "text": text_part},
            {"type": "image_url", "image_url": {"url": req.image_base64}},
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
        max_tokens=800,
        temperature=0.4,
    )
    reply_text = clean_reply(completion.choices[0].message.content)

    db.add(Message(conversation_id=conversation.id, role="teacher", content=reply_text))
    db.commit()

    return ChatResponse(
        conversation_id=conversation.id,
        reply=reply_text,
        sources=[{"book": c["book_title"], "page": c["page"]} for c in source_chunks],
    )
