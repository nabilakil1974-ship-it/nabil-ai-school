import re
from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Form,
    File,
    UploadFile,
)
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Conversation, Message, Student
from app.services.rag_search import (
    search_book_pages,
    build_context_block,
)
from app.services.ai_gateway import NabilAIGateway


router = APIRouter()


SYSTEM_PROMPT = """
أنت NABIL AI، الأستاذ نبيل، معلّم رقمي ذكي وخبير بالمنهج اللبناني الرسمي CRDP.

أنت معلّم تفاعلي ولست مجرد chatbot.

هدفك الأساسي هو مساعدة الطالب على الفهم والتعلّم، وليس إعطاء الإجابة فقط.

قواعدك:

1. اللغة:
- أجب بنفس لغة الطالب.
- العربية: عربية واضحة ودافئة.
- English: أجب بالإنجليزية.
- Français: أجب بالفرنسية.

2. السياق التعليمي:
- احترم الصف والمادة واللغة والمنهج والدرس المحددين.
- إذا تم توفير محتوى من CRDP/RAG، اعتبره المرجع الأساسي.
- لا تنسب معلومة إلى CRDP إذا لم تكن موجودة في السياق.
- لا تخترع محتوى منهجيًا.

3. طريقة التعليم:
- ساعد الطالب على الفهم.
- استخدم أسلوب السؤال والجواب عند الحاجة.
- إذا كانت المسألة تحتاج تفكيرًا، ساعد الطالب خطوة خطوة.
- لا تعطِ الحل النهائي مباشرة إذا كان من الأفضل تربويًا أن تجعل الطالب يفكر.
- إذا طلب الطالب الحل الكامل صراحة، أعطه الحل الكامل.
- إذا أخطأ الطالب، وضّح الخطأ بلطف وساعده على تصحيحه.

4. الرياضيات:
رتّب الحل عند الحاجة:
المعطيات
القانون أو القاعدة
خطوات الحل
النتيجة النهائية

استخدم LaTeX:
\\( ... \\)
\\[ ... \\]

والنتيجة النهائية أو القاعدة المهمة:
\\boxed{...}

5. شرح الدروس:
إذا كتب الطالب اسم درس فقط، اعتبره طلبًا لشرح الدرس.

استخدم عند الحاجة:
## التعريفات الأساسية
## النظريات والقواعد
## أمثلة محلولة
## تدريب للطالب
## خلاصة للامتحان ⭐

6. الحوار:
يمكنك التحدث مع الطالب بطريقة طبيعية.
اطرح سؤالًا واحدًا أو سؤالين في كل مرة للتحقق من فهمه.
لا تحوّل المحادثة إلى محاضرة طويلة دون تفاعل.

7. الصور:
إذا أرسل الطالب صورة لتمرين:
- اقرأها بدقة.
- استخرج السؤال.
- لا تفترض معلومات غير ظاهرة.
- ساعد الطالب في الحل.

8. الصوت:
تعامل مع كلام الطالب بعد تحويله من الصوت إلى نص كما لو أنه كتبه بنفسه.

9. الخصوصية والتقنية:
لا تطلب من الطالب أو المعلم أي API Key.
لا تطلب OpenAI Key أو Groq Key أو Gemini Key.
المفاتيح التقنية موجودة على الخادم فقط.

10. الهوية:
اسمك أمام الطالب:
NABIL AI
الأستاذ نبيل

أنت معلّم رقمي يساعد الطالب على التعلم والفهم والتقدم.
"""


def clean_reply(text: str) -> str:
    if not text:
        return ""

    text = re.sub(
        r"<think>.*?</think>",
        "",
        text,
        flags=re.DOTALL,
    )

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
    student_id: str = Form(...),
    conversation_id: Optional[str] = Form(None),
    subject: Optional[str] = Form(None),
    grade: Optional[str] = Form(None),
    curriculum: Optional[str] = Form(None),
    language: Optional[str] = Form(None),
    lesson: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    try:
        ai = NabilAIGateway()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"خطأ في إعداد NABIL AI: {str(e)}",
        )

    image_bytes = None
    image_mime_type = "image/jpeg"
    original_message = message

    # =========================
    # VOICE
    # =========================
    if audio is not None:
        try:
            audio_bytes = await audio.read()

            message = ai.transcribe(
                audio_bytes=audio_bytes,
                filename=audio.filename or "voice.webm",
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"خطأ في معالجة الصوت: {str(e)}",
            )

    # =========================
    # IMAGE
    # =========================
    if image is not None:
        try:
            image_bytes = await image.read()

            image_mime_type = (
                image.content_type or "image/jpeg"
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"خطأ في قراءة الصورة: {str(e)}",
            )

    if not message:
        message = "ساعدني في هذا التمرين."

    # =========================
    # STUDENT
    # =========================
    student = (
        db.query(Student)
        .filter_by(id=student_id)
        .first()
    )

    if student is None:
        student = Student(
            id=student_id,
            name=student_id,
            grade=grade or "غير محدد",
            preferred_language=language or "ar-LB",
        )

        db.add(student)
        db.commit()
        db.refresh(student)

    # =========================
    # CONVERSATION
    # =========================
    conversation = None

    if conversation_id:
        conversation = (
            db.query(Conversation)
            .filter_by(id=conversation_id)
            .first()
        )

    if conversation is None:
        conversation = Conversation(
            student_id=student_id,
            subject=subject,
        )

        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    # =========================
    # HISTORY
    # =========================
    previous_messages = (
        db.query(Message)
        .filter(
            Message.conversation_id == conversation.id
        )
        .order_by(Message.created_at.asc())
        .limit(20)
        .all()
    )

    db.add(
        Message(
            conversation_id=conversation.id,
            role="student",
            content=message,
        )
    )

    db.commit()

    # =========================
    # RAG / CRDP
    # =========================
    source_chunks = []
    context_block = ""

    if (
        subject
        and grade
        and curriculum
        and message
    ):
        try:
            source_chunks = search_book_pages(
                db=db,
                query=message,
                subject=subject,
                grade=grade,
                curriculum=curriculum,
            )

            context_block = build_context_block(
                source_chunks
            )

        except Exception as e:
            print(
                f"RAG warning: {e}",
                flush=True,
            )

    # =========================
    # EDUCATIONAL CONTEXT
    # =========================
    educational_context = f"""
السياق التعليمي الحالي:

الصف: {grade or "غير محدد"}
المادة: {subject or "غير محددة"}
اللغة: {language or "غير محددة"}
المنهج: {curriculum or "المنهج اللبناني"}
الدرس: {lesson or "غير محدد"}

محتوى CRDP/RAG:
{context_block or "لا يوجد محتوى RAG متوفر لهذا السؤال."}
"""

    # =========================
    # MESSAGE HISTORY
    # =========================
    history_messages = []

    for msg in previous_messages:
        role = (
            "assistant"
            if msg.role == "teacher"
            else "user"
        )

        history_messages.append(
            {
                "role": role,
                "content": msg.content,
            }
        )

    current_prompt = f"""
{educational_context}

سؤال الطالب:

{message}
"""

    history_messages.append(
        {
            "role": "user",
            "content": current_prompt,
        }
    )

    # =========================
    # NABIL AI
    # =========================
    try:
        reply_text = ai.generate(
            instructions=SYSTEM_PROMPT,
            messages=history_messages,
            image_bytes=image_bytes,
            image_mime_type=image_mime_type,
            max_output_tokens=2500,
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

    # =========================
    # SAVE RESPONSE
    # =========================
    db.add(
        Message(
            conversation_id=conversation.id,
            role="teacher",
            content=reply_text,
        )
    )

    db.commit()

    # =========================
    # SOURCES
    # =========================
    sources = []

    for chunk in source_chunks:
        sources.append(
            {
                "book": chunk.get("book_title"),
                "page": chunk.get("page"),
            }
        )

    return ChatResponse(
        conversation_id=str(conversation.id),
        reply=reply_text,
        sources=sources,
        transcribed_text=(
            message
            if audio is not None
            else None
        ),
    )
