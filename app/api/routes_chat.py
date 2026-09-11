import json
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
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Conversation, Message, Student
from app.services.ai_gateway import NabilAIGateway


router = APIRouter()


SYSTEM_PROMPT = """
أنت NABIL AI، الأستاذ نبيل، معلّم رقمي ذكي.

مهمتك تعليم الطالب وفق الصف والمادة واللغة والدرس المحددين.

==================================================
1. اللغة
==================================================

أجب باللغة المحددة في السياق.

إذا كانت العربية:
- استخدم العربية فقط في الشرح.
- لا تخلط كلمات إنجليزية أو فرنسية دون حاجة.
- الرموز الرياضية مثل x, y, ln(x), e^x تبقى كما هي.

إذا كانت English:
أجب بالإنجليزية.

إذا كانت Français:
أجب بالفرنسية.

==================================================
2. التعليم
==================================================

- اشرح بمستوى الطالب.
- استخدم المصطلحات العلمية الصحيحة.
- تحقق من العمليات الحسابية.
- إذا كان السؤال بسيطًا، لا تطل.
- إذا كان درسًا، اشرح تدريجيًا.
- إذا كان تمرينًا، حلّه خطوة خطوة.
- إذا طلب الطالب الحل الكامل، أعطه الحل الكامل.

==================================================
3. الرياضيات
==================================================

استخدم LaTeX صحيحًا:

\\[
a^2+b^2=c^2
\\]

\\[
\\frac{a}{b}
\\]

\\[
\\sqrt{x}
\\]

\\[
\\boxed{...}
\\]

لا تستخدم رسومات ASCII إطلاقًا.

ممنوع رسم أشكال باستخدام:
*
/
|
-
أو أي رسم نصي مشابه.

الرسمة المرئية ستتولاها واجهة NABIL AI.

==================================================
4. الصور
==================================================

إذا أرسل الطالب صورة:

- اقرأها كاملة.
- إذا كانت تمرينًا: استخرج السؤال وحلّه.
- إذا كانت صفحة درس: اشرح محتواها.
- إذا كان فيها رسم: اقرأ أسماء النقاط والمعطيات.
- لا تخترع معلومة غير واضحة.
- لا تعرض التفكير الداخلي أو التخمينات.

==================================================
5. الرسم الديناميكي
==================================================

إذا كان الجواب يستفيد فعلاً من رسم، أضف في نهاية الإجابة
كتلة واحدة فقط بالشكل التالي:

<DRAWING_JSON>
{JSON}
</DRAWING_JSON>

لا تعرض هذه الكتلة للطالب كنص.

يجب أن يكون JSON صالحًا تمامًا.

الأنواع المدعومة:

--------------------------------------------------
أ) دالة رياضية
--------------------------------------------------

{
  "type": "function",
  "title": "رسم الدالة ln(x)",
  "function": "ln",
  "expression": "ln(x)",
  "x_min": 0.1,
  "x_max": 7,
  "y_min": -3,
  "y_max": 3,
  "points": [
    {"x": 1, "y": 0, "label": "(1,0)"},
    {"x": 2.71828, "y": 1, "label": "(e,1)"}
  ],
  "vertical_asymptote": 0
}

القيم المقبولة في function:
ln
exp
square
linear
inverse

--------------------------------------------------
ب) مثلث قائم
--------------------------------------------------

{
  "type": "right_triangle",
  "title": "مثلث قائم الزاوية",
  "a": 3,
  "b": 4,
  "c": 5,
  "labels": {
    "a": "3 cm",
    "b": "4 cm",
    "c": "5 cm"
  }
}

إذا لم تكن بعض الأطوال معروفة استخدم null.

--------------------------------------------------
ج) دائرة ومماس
--------------------------------------------------

{
  "type": "circle_tangent",
  "title": "دائرة ومماس",
  "radius": 5,
  "center": "O",
  "tangent_point": "A",
  "external_point": "M"
}

--------------------------------------------------
د) قوى في الفيزياء
--------------------------------------------------

{
  "type": "forces",
  "title": "مخطط القوى",
  "object": "m",
  "forces": [
    {"direction": "up", "label": "N"},
    {"direction": "down", "label": "mg"},
    {"direction": "right", "label": "F"}
  ]
}

الاتجاهات المقبولة:
up
down
left
right

--------------------------------------------------
هـ) جزيء مبسط
--------------------------------------------------

{
  "type": "molecule",
  "title": "بنية جزيئية مبسطة",
  "atoms": [
    {"label": "H"},
    {"label": "O"},
    {"label": "H"}
  ]
}

==================================================
6. متى ترسل الرسم؟
==================================================

أرسل DRAWING_JSON عند:
- رسم دالة.
- هندسة تحتاج شكلاً.
- فيثاغورس.
- دائرة أو مماس.
- مخطط قوى في الفيزياء.
- بنية جزيئية مبسطة في الكيمياء.

لا ترسله إذا لم يكن الرسم مفيدًا.

==================================================
7. قواعد مهمة للرسم
==================================================

- الرسم يجب أن يمثل السؤال الحالي لا مثالًا عامًا مختلفًا.
- إذا كان السؤال عن أطوال 3 و4 و5، استخدم 3 و4 و5.
- إذا كان السؤال عن ln(x)، استخدم ln.
- لا تخترع أرقامًا غير موجودة.
- لا تخترع نقاطًا هندسية غير موجودة.
- إذا لم تعرف قيمة، ضع null.

==================================================
8. الهوية
==================================================

اسمك:
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
        flags=re.DOTALL | re.IGNORECASE,
    )

    if "</think>" in text:
        text = text.split("</think>")[-1]

    if "<think>" in text:
        text = text.split("<think>")[0]

    return text.strip()


def extract_drawing(text: str):
    if not text:
        return text, None

    pattern = r"<DRAWING_JSON>\s*(.*?)\s*</DRAWING_JSON>"

    match = re.search(
        pattern,
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )

    if not match:
        return text.strip(), None

    drawing = None

    try:
        drawing = json.loads(
            match.group(1).strip()
        )

    except Exception:
        drawing = None

    clean_text = re.sub(
        pattern,
        "",
        text,
        flags=re.DOTALL | re.IGNORECASE,
    ).strip()

    return clean_text, drawing


class ChatResponse(BaseModel):
    conversation_id: str
    reply: str
    sources: list[dict] = Field(default_factory=list)
    transcribed_text: Optional[str] = None
    drawing: Optional[dict] = None


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

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"خطأ في إعداد NABIL AI: {exc}",
        ) from exc

    image_bytes = None
    image_mime_type = "image/jpeg"
    transcribed_text = None

    # ==========================================
    # AUDIO
    # ==========================================

    if audio is not None:

        try:
            audio_bytes = await audio.read()

            transcribed_text = ai.transcribe(
                audio_bytes=audio_bytes,
                filename=audio.filename or "voice.webm",
            )

            message = transcribed_text

        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=f"خطأ في معالجة الصوت: {exc}",
            ) from exc

    # ==========================================
    # IMAGE
    # ==========================================

    if image is not None:

        try:
            image_bytes = await image.read()

            if not image_bytes:
                raise ValueError(
                    "ملف الصورة فارغ."
                )

            image_mime_type = (
                image.content_type
                or "image/jpeg"
            )

            allowed_types = {
                "image/jpeg",
                "image/jpg",
                "image/png",
                "image/webp",
                "image/gif",
            }

            if image_mime_type not in allowed_types:
                raise ValueError(
                    f"نوع الصورة غير مدعوم: {image_mime_type}"
                )

        except Exception as exc:
            raise HTTPException(
                status_code=400,
                detail=f"خطأ في قراءة الصورة: {exc}",
            ) from exc

    # ==========================================
    # DEFAULT MESSAGE
    # ==========================================

    if not message or not message.strip():

        if image_bytes is not None:
            message = (
                "اقرأ هذه الصورة. "
                "إذا كانت تمرينًا فحلّه، "
                "وإذا كانت صفحة درس فاشرحها."
            )

        else:
            message = "ساعدني في هذا الدرس."

    message = message.strip()

    # ==========================================
    # STUDENT
    # ==========================================

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

    # ==========================================
    # CONVERSATION
    # ==========================================

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

    # ==========================================
    # HISTORY
    # ==========================================

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

    # ==========================================
    # CONTEXT
    # ==========================================

    selected_language = (
        language
        or student.preferred_language
        or "العربية"
    )

    educational_context = f"""
السياق التعليمي الحالي:

الصف: {grade or "غير محدد"}
المادة: {subject or "غير محددة"}
اللغة الإلزامية: {selected_language}
المنهج: {curriculum or "المنهج اللبناني الرسمي"}
الدرس: {lesson or "غير محدد"}

التزم بمستوى الطالب.

إذا كان الرسم مفيدًا،
أرسل DRAWING_JSON مطابقًا للسؤال الحالي.

لا تستخدم رسومات ASCII.
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

    # ==========================================
    # AI
    # ==========================================

    try:

        raw_reply = ai.generate(
            instructions=SYSTEM_PROMPT,
            messages=history_messages,
            image_bytes=image_bytes,
            image_mime_type=image_mime_type,
            max_output_tokens=3000,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"خطأ في NABIL AI: {exc}",
        ) from exc

    raw_reply = clean_reply(
        raw_reply
    )

    reply_text, drawing = extract_drawing(
        raw_reply
    )

    if not reply_text:

        raise HTTPException(
            status_code=500,
            detail="NABIL AI لم يُرجع إجابة.",
        )

    # ==========================================
    # SAVE
    # ==========================================

    db.add(
        Message(
            conversation_id=conversation.id,
            role="teacher",
            content=reply_text,
        )
    )

    db.commit()

    # ==========================================
    # RESPONSE
    # ==========================================

    return ChatResponse(
        conversation_id=str(
            conversation.id
        ),
        reply=reply_text,
        sources=[],
        transcribed_text=transcribed_text,
        drawing=drawing,
    )
