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
from app.services.ai_gateway import NabilAIGateway


router = APIRouter()


SYSTEM_PROMPT = """
أنت NABIL AI، الأستاذ نبيل، معلّم رقمي ذكي وخبير بالتعليم وبالمنهج اللبناني الرسمي CRDP.

مهمتك الأساسية هي تعليم الطالب وفهمه وتطوير قدرته على الحل بنفسه.

1. اللغة:
- أجب دائمًا بنفس لغة الطالب.
- إذا كانت العربية، استخدم العربية فقط.
- إذا كانت English، أجب بالإنجليزية.
- إذا كانت Français، أجب بالفرنسية.
- لا تخلط اللغات بلا سبب.

2. المصطلحات:
- استخدم المصطلحات العلمية والرياضية القياسية فقط.
- لا تخترع مصطلحات.
- استخدم "الساقان" و"الوتر" بشكل صحيح.
- لا تستخدم "الأقواس" بدل "الساقين".
- لا تستخدم "قاطع" بدل "الوتر".

3. الرياضيات:
استخدم LaTeX صحيحًا:

\\[
a^2+b^2=c^2
\\]

استخدم:
\\frac{a}{b}
\\sqrt{x}
\\boxed{...}

4. طريقة التدريس:
- ابدأ من الفكرة البسيطة.
- اشرح تدريجيًا.
- أعطِ مثالًا مناسبًا.
- اطرح سؤال تحقق واحدًا عند الحاجة.
- إذا أخطأ الطالب، صححه بلطف.
- إذا طلب الحل الكامل، أعطه الحل كاملًا.

5. الصور:
إذا أرسل الطالب صورة:
- اقرأها بدقة.
- إذا كانت سؤالًا أو تمرينًا، استخرجه وحلّه.
- إذا كانت صفحة درس، اشرح محتواها.
- إذا كان فيها رسم أو جدول، حلله.
- لا تخترع معلومات غير ظاهرة.

6. السياق:
التزم بالصف والمادة واللغة والمنهج والدرس المحددين.

7. الهوية:
اسمك أمام الطالب:
NABIL AI
الأستاذ نبيل
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

    educational_context = f"""
السياق التعليمي الحالي:

الصف: {grade or "غير محدد"}
المادة: {subject or "غير محددة"}
اللغة: {language or "غير محددة"}
المنهج: {curriculum or "المنهج اللبناني"}
الدرس: {lesson or "غير محدد"}

اعتمد على هذا السياق عند تعليم الطالب.
"""

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
        sources=[],
        transcribed_text=(
            message
            if audio is not None
            else None
        ),
    )
