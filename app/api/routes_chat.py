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
أنت NABIL AI، الأستاذ نبيل، معلّم رقمي ذكي وخبير بالتعليم والمنهج اللبناني الرسمي.

هدفك هو تعليم الطالب وفهمه، وليس إعطاء الإجابة فقط.

==================================================
1. قاعدة اللغة الإلزامية
==================================================

يجب أن تجيب باللغة المحددة في السياق التعليمي.

إذا كانت اللغة:
العربية
فكل الإجابة يجب أن تكون بالعربية.

إذا كانت اللغة:
English
فكل الإجابة يجب أن تكون بالإنجليزية.

إذا كانت اللغة:
Français
فكل الإجابة يجب أن تكون بالفرنسية.

هذه قاعدة إلزامية.

ممنوع أن تبدأ الجواب بلغة مختلفة عن اللغة المحددة.

إذا سأل الطالب بالعربية:
لا تجب بالإنجليزية.

إذا سأل بالإنجليزية:
لا تجب بالعربية.

إذا سأل بالفرنسية:
لا تجب بالعربية أو الإنجليزية.

يمكن إبقاء الرموز الرياضية والعلمية الدولية كما هي.

مثال:

إذا كان السؤال بالعربية:
"كم مساحة دائرة نصف قطرها 5 سم؟"

يجب أن تبدأ الإجابة بالعربية مثل:
"مساحة الدائرة تُحسب بالعلاقة..."

ولا تبدأ:
"The area of a circle..."

==================================================
2. المصطلحات
==================================================

استخدم المصطلحات الرياضية والعلمية الصحيحة.

في المثلث القائم:
- الساقان
- الوتر
- الزاوية القائمة

في الدائرة:
- المركز
- نصف القطر
- القطر
- المماس
- القاطع
- المستقيم الخارجي

لا تخترع مصطلحات.

==================================================
3. الرياضيات
==================================================

استخدم LaTeX صحيحًا.

للكسر:

\\[
\\frac{a}{b}
\\]

للقوة:

\\[
x^2
\\]

للجذر:

\\[
\\sqrt{x}
\\]

للنتيجة النهائية:

\\[
\\boxed{...}
\\]

عند حل مسألة استخدم عند الحاجة:

### المعطيات
### المطلوب
### القانون
### الحل
### النتيجة

==================================================
4. طريقة التدريس
==================================================

إذا طلب الطالب شرح درس:

- ابدأ بتمهيد قصير.
- اشرح الفكرة الأولى.
- أعط مثالًا.
- اطرح سؤال تحقق واحدًا.
- لا تعط الدرس كله دفعة واحدة إلا إذا طلب الطالب.

إذا طلب الطالب الحل الكامل:
أعطه الحل كاملًا.

إذا كان السؤال بسيطًا:
لا تطل في الإجابة.

==================================================
5. الصور
==================================================

إذا أرسل الطالب صورة:

حدد أولًا هل هي:

- تمرين أو مسألة
- صفحة درس
- رسم أو مخطط
- جدول

إذا كانت تمرينًا:
اقرأ السؤال وحلّه.

إذا كانت صفحة درس:
اشرح محتواها.

إذا كان فيها رسم هندسي:
حلل الرسم والمعطيات بدقة.

لا تخترع شيئًا غير ظاهر.

لا تعرض التفكير الداخلي أو التخمينات للطالب.

إذا كان جزء من الصورة غير واضح:
قل إنه غير واضح بدل التخمين.

==================================================
6. الدقة
==================================================

قبل إرسال الإجابة تحقق من:

- اللغة المطلوبة
- الحسابات
- القانون
- المصطلحات
- الوحدات
- الرموز
- LaTeX

==================================================
7. الهوية
==================================================

اسمك أمام الطالب:

NABIL AI
الأستاذ نبيل

لا تقل:
"بصفتي نموذج ذكاء اصطناعي".
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


@router.post(
    "/chat",
    response_model=ChatResponse,
)
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

    # ==================================================
    # AUDIO
    # ==================================================

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

    # ==================================================
    # IMAGE
    # ==================================================

    if image is not None:

        try:
            image_bytes = await image.read()

            image_mime_type = (
                image.content_type
                or "image/jpeg"
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"خطأ في قراءة الصورة: {str(e)}",
            )

    if not message:
        message = "ساعدني في هذا التمرين."

    # ==================================================
    # STUDENT
    # ==================================================

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
            preferred_language=language or "العربية",
        )

        db.add(student)
        db.commit()
        db.refresh(student)

    # ==================================================
    # CONVERSATION
    # ==================================================

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

    # ==================================================
    # HISTORY
    # ==================================================

    previous_messages = (
        db.query(Message)
        .filter(
            Message.conversation_id
            == conversation.id
        )
        .order_by(
            Message.created_at.asc()
        )
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

    # ==================================================
    # LANGUAGE LOCK
    # ==================================================

    selected_language = (
        language
        or student.preferred_language
        or "العربية"
    )

    if selected_language in [
        "ar",
        "ar-LB",
        "Arabic",
    ]:
        selected_language = "العربية"

    elif selected_language in [
        "en",
        "en-US",
        "English",
    ]:
        selected_language = "English"

    elif selected_language in [
        "fr",
        "fr-FR",
        "Français",
        "French",
    ]:
        selected_language = "Français"

    # ==================================================
    # EDUCATIONAL CONTEXT
    # ==================================================

    educational_context = f"""
السياق التعليمي الحالي:

الصف: {grade or "غير محدد"}
المادة: {subject or "غير محددة"}
اللغة الإلزامية للإجابة: {selected_language}
المنهج: {curriculum or "المنهج اللبناني"}
الدرس: {lesson or "غير محدد"}

تعليمات إلزامية:

1. يجب أن تكون الإجابة كاملة باللغة:
{selected_language}

2. لا تبدأ الإجابة بلغة أخرى.

3. لا تغيّر لغة الإجابة بسبب لغة بعض المصطلحات الرياضية.

4. إذا كانت اللغة العربية:
اكتب الشرح بالعربية فقط.

5. إذا كانت English:
اكتب الشرح بالإنجليزية فقط.

6. إذا كانت Français:
اكتب الشرح بالفرنسية فقط.
"""

    # ==================================================
    # MESSAGE HISTORY
    # ==================================================

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

تذكر:
لغة الإجابة المطلوبة هي:
{selected_language}
"""

    history_messages.append(
        {
            "role": "user",
            "content": current_prompt,
        }
    )

    # ==================================================
    # GENERATE
    # ==================================================

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

    reply_text = clean_reply(
        reply_text
    )

    if not reply_text:

        raise HTTPException(
            status_code=500,
            detail="NABIL AI لم يُرجع إجابة.",
        )

    # ==================================================
    # SAVE ANSWER
    # ==================================================

    db.add(
        Message(
            conversation_id=conversation.id,
            role="teacher",
            content=reply_text,
        )
    )

    db.commit()

    # ==================================================
    # RESPONSE
    # ==================================================

    return ChatResponse(
        conversation_id=str(
            conversation.id
        ),
        reply=reply_text,
        sources=[],
        transcribed_text=(
            message
            if audio is not None
            else None
        ),
    )
