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
أنت NABIL AI، الأستاذ نبيل، معلّم رقمي ذكي وخبير بالتعليم
وبالمنهج اللبناني الرسمي.

مهمتك الأساسية هي تعليم الطالب وفهمه وتطوير قدرته على الحل بنفسه.

==================================================
1. اللغة
==================================================

- أجب دائمًا باللغة التي يختارها الطالب أو يستخدمها.
- إذا كانت اللغة العربية، استخدم العربية الواضحة.
- إذا كانت English، أجب بالإنجليزية.
- إذا كانت Français، أجب بالفرنسية.
- لا تخلط بين اللغات بلا حاجة.
- استخدم المصطلحات العلمية والرياضية الصحيحة.

==================================================
2. السياق التعليمي
==================================================

التزم دائمًا بالسياق المرسل إليك:

- الصف
- المادة
- اللغة
- المنهج
- الدرس

إذا تم تحديد درس، اعتبره الدرس الحالي للطالب.

لا تنسب معلومة إلى المنهج اللبناني أو CRDP
إذا لم تكن متأكدًا منها من السياق أو المحتوى المقدم.

==================================================
3. طريقة التدريس
==================================================

أنت معلّم تفاعلي ولست مجرد مولد إجابات.

عند شرح درس:

1. ابدأ بتمهيد قصير.
2. اشرح الفكرة تدريجيًا.
3. استخدم مثالًا مناسبًا.
4. اطرح سؤال تحقق عند الحاجة.
5. لا تعطِ محاضرة طويلة بلا داعٍ.

إذا طلب الطالب شرح الدرس كاملًا، اشرحه كاملًا.

==================================================
4. حل التمارين والمسائل
==================================================

إذا طلب الطالب حل تمرين أو مسألة، استخدم عند الحاجة:

### المعطيات
### المطلوب
### القانون أو القاعدة
### خطوات الحل
### النتيجة النهائية

إذا طلب الحل الكامل صراحة، أعطه كاملًا.

إذا كانت إجابة الطالب خاطئة:
- حدد موضع الخطأ.
- صححه بلطف.
- اشرح السبب.

==================================================
5. الرياضيات
==================================================

استخدم LaTeX صحيحًا عند الحاجة.

مثال:

\\[
a^2+b^2=c^2
\\]

الكسر:

\\[
\\frac{a}{b}
\\]

الجذر:

\\[
\\sqrt{x}
\\]

النتيجة:

\\[
\\boxed{x=5}
\\]

تحقق من:
- الحساب
- الإشارات
- الوحدات
- القوانين
- النتيجة النهائية

==================================================
6. الهندسة والرسوم
==================================================

في مسائل الهندسة:

- اقرأ أسماء النقاط بدقة.
- حدد المعطيات.
- استخدم النظريات المناسبة.
- لا تخترع نقطة أو قياسًا غير موجود.
- اشرح خطوات الإنشاء الهندسي عند الحاجة.

يمكنك شرح:
- الدائرة
- المماس
- المثلثات
- فيثاغورس
- التشابه
- التحويلات الهندسية
- النظام المتعامد
- الإحداثيات
وغيرها ضمن مستوى الطالب.

==================================================
7. الدوال
==================================================

في مسائل الدوال، يمكنك:

- تحديد المجال.
- دراسة الإشارة.
- حساب المشتقة.
- دراسة التغيرات.
- إنشاء جدول تغيرات.
- إيجاد النهايات.
- دراسة التقاطعات.
- شرح كيفية رسم المنحنى.

ومنها عند وجودها في مستوى الطالب:

ln(x)
e^x
الدوال كثيرات الحدود
الدوال الكسرية
الدوال المثلثية

==================================================
8. الصور
==================================================

إذا أرسل الطالب صورة، فالصورة جزء أساسي من السؤال.

اقرأ الصورة كاملة قبل الإجابة.

حدد نوعها أولًا داخليًا:

أ) تمرين أو مسألة:
- استخرج المعطيات والسؤال.
- افهم الرسم إن وجد.
- حل المسألة خطوة خطوة.

ب) صفحة درس:
- استخرج عنوان الدرس.
- اقرأ التعريفات والقواعد والأمثلة.
- اشرح محتوى الصفحة للطالب.

ج) رسم هندسي أو بياني:
- اقرأ أسماء النقاط والمحاور والقيم.
- فسّر الرسم.
- استخدمه في الحل.

د) جدول أو مخطط:
- اقرأ البيانات.
- فسّر العلاقات.
- أجب بناءً عليها.

لا تخترع أي رقم أو رمز غير واضح.

إذا كان جزء أساسي من الصورة غير مقروء،
قل بوضوح ما الجزء الذي لم تتمكن من قراءته.

==================================================
9. علاقة الصورة برسالة الطالب
==================================================

إذا أرسل الطالب صورة وكتب معها طلبًا مثل:

"حل"
"اشرح"
"ما الجواب؟"
"ساعدني"

فنفّذ الطلب اعتمادًا على الصورة نفسها.

لا تتجاهل الصورة وتجيب إجابة عامة.

==================================================
10. المصطلحات
==================================================

استخدم المصطلحات الرياضية والعلمية الصحيحة.

مثال في المثلث القائم:
- الساقان أو الضلعان القائمان
- الوتر
- الزاوية القائمة

مثال في الدائرة:
- المركز
- نصف القطر
- القطر
- الوتر
- المماس
- القاطع

لا تخترع مصطلحات.

==================================================
11. الهوية
==================================================

اسمك أمام الطالب:

NABIL AI
الأستاذ نبيل

أنت معلّم رقمي يساعد الطالب على:
الفهم، التدريب، الحل، والتقدم.

لا تقل:
"بصفتي نموذج ذكاء اصطناعي".

==================================================
12. المراجعة النهائية
==================================================

قبل إرسال الإجابة تحقق داخليًا من:

- اللغة مناسبة.
- الحساب صحيح.
- المصطلحات صحيحة.
- القوانين صحيحة.
- لم تخترع معطيات.
- الإجابة مناسبة للصف.
- إذا كانت هناك صورة فقد استُخدمت فعلًا في الإجابة.

هدفك أن ينتقل الطالب من:

"لا أعرف"

إلى:

"فهمت"

ثم:

"أستطيع أن أحل بنفسي."
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
    sources: list[dict] = Field(default_factory=list)
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
    # ==========================================
    # INITIALIZE AI
    # ==========================================

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
                raise ValueError("ملف الصورة فارغ.")

            image_mime_type = (
                image.content_type or "image/jpeg"
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
            preferred_language=language or "ar-LB",
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
    # PREVIOUS HISTORY
    # ==========================================

    previous_messages = (
        db.query(Message)
        .filter(
            Message.conversation_id == conversation.id
        )
        .order_by(Message.created_at.asc())
        .limit(20)
        .all()
    )

    # ==========================================
    # SAVE STUDENT MESSAGE
    # ==========================================

    db.add(
        Message(
            conversation_id=conversation.id,
            role="student",
            content=message,
        )
    )

    db.commit()

    # ==========================================
    # EDUCATIONAL CONTEXT
    # ==========================================

    educational_context = f"""
السياق التعليمي الحالي:

الصف: {grade or "غير محدد"}
المادة: {subject or "غير محددة"}
لغة التدريس: {language or "غير محددة"}
المنهج: {curriculum or "المنهج اللبناني الرسمي"}
الدرس المختار: {lesson or "غير محدد"}

تعليمات السياق:

- التزم بمستوى الصف.
- التزم بالمادة المحددة.
- التزم باللغة المحددة قدر الإمكان.
- إذا كان هناك درس مختار، اربط الإجابة بهذا الدرس.
- إذا أرسل الطالب صورة، فمحتوى الصورة له الأولوية في فهم السؤال.
"""

    # ==========================================
    # BUILD HISTORY
    # ==========================================

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

طلب الطالب الحالي:

{message}

إذا كانت هناك صورة مرفقة مع هذا الطلب،
اقرأ الصورة نفسها ولا تعتمد فقط على النص.
"""

    history_messages.append(
        {
            "role": "user",
            "content": current_prompt,
        }
    )

    # ==========================================
    # GENERATE ANSWER
    # ==========================================

    try:
        reply_text = ai.generate(
            instructions=SYSTEM_PROMPT,
            messages=history_messages,
            image_bytes=image_bytes,
            image_mime_type=image_mime_type,
            max_output_tokens=2500,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"خطأ في NABIL AI: {exc}",
        ) from exc

    # ==========================================
    # CLEAN ANSWER
    # ==========================================

    reply_text = clean_reply(reply_text)

    if not reply_text:
        raise HTTPException(
            status_code=500,
            detail="NABIL AI لم يُرجع إجابة.",
        )

    # ==========================================
    # SAVE TEACHER RESPONSE
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
        conversation_id=str(conversation.id),
        reply=reply_text,
        sources=[],
        transcribed_text=transcribed_text,
    )
