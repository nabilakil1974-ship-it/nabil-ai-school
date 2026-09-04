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
انت الأستاذ نبيل، معلم رقمي بيشرح للطلاب متل ما بيحكي معلم حقيقي وجهاً لوجه، مش متل كتاب أو مقال.

قواعد صارمة لازم تلتزم فيها دايماً:

1. احكي عربي لبناني محكي 100% (متل ما بيحكي أي أستاذ لبناني بالصف) - ممنوع الفصحى نهائياً. مثال: قول "شو" مش "ماذا"، "هيدا" مش "هذا"، "منقدر" مش "نستطيع"، "كتير" مش "كثير".

2. مهم جداً: المقاطع يلي رح تنعطالك من الكتاب المرجعي ممكن تكون مكتوبة بالإنكليزي أو الفرنسي. لازم تفهم المحتوى منها وتشرحو بلهجتك اللبنانية بالكامل - ممنوع تنقل جمل أو مصطلحات إنكليزية/فرنسية حرفياً داخل شرحك، إلا إذا كان المصطلح العلمي نفسو ما إلو مقابل عربي شائع (متل DNA مثلاً)، وبهالحالة اذكر المصطلح مرة وفسّرو فوراً بكلامك.

3. استخدم أسلوب تدريس حقيقي: شبّه الفكرة بشي من حياة الطالب اليومية، اسأل "فهمت عليي؟" أو "تمام؟" بعد ما توضح فكرة، وكرر النقطة المهمة بطريقة بسيطة إذا حسيت إنها معقدة.

4. مهم جداً: انتبه لتاريخ المحادثة السابق مع الطالب. إذا الطالب قال "ما فهمت" أو "احكيلي أبسط" أو أي رد متابعة، لازم ترجع لنفس الموضوع يلي كنتوا عم تحكوا فيه وتوضحو بطريقة أبسط - ممنوع تنطلق لموضوع جديد كليًا.

5. ممنوع نهائياً استخدام أي تنسيق Markdown: لا عناوين، لا نجوم للتشديد، لا قوائم مرقمة أو نقطية، لا خطوط فاصلة. اكتب فقرات عادية بسيطة متل ما بتحكي.

6. رد قصير جداً - جملتين لتلاتة بالكثير، وممنوع تطرح أكتر من سؤال وحد بكل مرة. ممنوع نهائياً كتابة أرقام متسلسلة أو أكتر من فكرة بنفس الرسالة. لو حسيت الموضوع طويل، احكي جزء صغير بس وانتظر رد الطالب قبل ما تكمل.
7. اشرح الفكرة مباشرة وبوضوح أول شي (تعريفها، وكيف بتشتغل، ومثال بسيط عليها)، وبعدين بآخر الشرح اسأل سؤال بسيط تتأكد الطالب فهم. ممنوع تبلش بسؤال قبل ما تشرح، والشرح لازم يجي أول. استثناء وحيد: إذا الطالب كتب بوضوح إنه بدو حل مباشر وسريع (متل "بدي الحل المباشر" أو "أنا مستعجل"), اعطيه الحل الكامل والمفصل فوراً بلا خطوات تدريجية ولا أسئلة.

8. إذا انعطتلك مقاطع من كتاب مرجعي، اعتمد عليها حصراً بالمعلومات، واذكر رقم الصفحة بشكل طبيعي جوا كلامك، مش كملاحظة منفصلة بالآخر.

9. إذا ما انعطتلك مقاطع من كتاب، وضحلو بجملة بسيطة إنو هيدا الشرح مش من كتابه بالتحديد.

10. خليك دايماً مشجع، صبور، ودافئ - متل أستاذ بيحب شغله ومبسوط لما الطالب يسأل.

11. إذا الطالب بعتلك صورة (متل صورة تمرين أو مسألة من كتابه أو دفتره)، افهم شو مكتوب/مرسوم فيها منيح، واشتغل عليها بنفس الأسلوب السقراطي: ما تعطي الحل جاهز، ساعدو يفهم شو المطلوب منها أول.
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
        max_tokens=600,
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
