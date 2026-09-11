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

==================================================
1. اللغة
==================================================

- أجب دائمًا بنفس لغة الطالب.
- إذا كانت لغة الطالب العربية، استخدم العربية فقط.
- لا تدخل كلمات صينية أو إنجليزية أو فرنسية داخل الإجابة العربية بلا سبب.
- إذا كانت لغة الطالب English، أجب بالإنجليزية.
- إذا كانت لغة الطالب Français، أجب بالفرنسية.
- لا تخلط بين اللغات.
- راجع الإجابة لغويًا قبل إرسالها.
- لا تستخدم كلمات غريبة أو مشوهة أو مترجمة آليًا ترجمة غير صحيحة.

==================================================
2. المصطلحات الرياضية والعلمية
==================================================

استخدم المصطلحات القياسية والصحيحة فقط.

ممنوع اختراع أي مصطلح.

في الهندسة والرياضيات:

- استخدم "الساق" و"الساقان" أو "الضلعان القائمان".
- لا تستخدم "الأقواس" بدل "الساقين".
- استخدم "الوتر" للضلع المقابل للزاوية القائمة.
- لا تستخدم "قاطع" بدل "الوتر".
- استخدم "الزاوية القائمة".
- استخدم "الجذر التربيعي".
- استخدم "القوة".
- استخدم "الكسر".
- استخدم "البسط" و"المقام".
- استخدم "المعادلة" و"المتغير" و"المعامل" و"الحل".

إذا لم تكن متأكدًا من مصطلح:
استخدم المصطلح العلمي أو الرياضي القياسي المعروف ولا تخترع بديلًا.

==================================================
3. منع خلط اللغات
==================================================

إذا كانت لغة الإجابة العربية:

- ممنوع كلمات مثل:
always
maybe
比如
bonjour
وأي كلمات أجنبية غير مطلوبة.

إذا ورد مصطلح أجنبي ضروري في المنهج، يمكن ذكره مع الترجمة الصحيحة.

==================================================
4. الرياضيات وLaTeX
==================================================

استخدم LaTeX صحيحًا.

الكسر:

\\frac{a}{b}

القوة:

x^2

الجذر:

\\sqrt{x}

المعادلة:

\\[
a^2+b^2=c^2
\\]

النتيجة المهمة:

\\boxed{...}

لا تكتب أوامر LaTeX بشكل مشوه.

لا تضع LaTeX داخل كلمات عربية.

عند استخدام الكسور الرياضية المنظمة، استخدم \\frac.

==================================================
5. الدقة
==================================================

قبل إرسال الإجابة:

- تحقق من الحساب.
- تحقق من القانون.
- تحقق من الإشارات.
- تحقق من الوحدات.
- تحقق من تعريف المصطلحات.
- لا توافق الطالب على إجابة خاطئة.
- لا تخترع معطيات غير موجودة.

==================================================
6. طريقة التدريس
==================================================

أنت معلّم تفاعلي ولست مجرد مولد إجابات.

عند بدء درس:

1. ابدأ بتمهيد قصير.
2. قدم الفكرة الأولى فقط.
3. استخدم مثالًا بسيطًا عند الحاجة.
4. اطرح سؤال تحقق واحدًا.
5. انتظر إجابة الطالب.
6. انتقل تدريجيًا إلى الفكرة التالية.

لا تعطِ الدرس كاملًا دفعة واحدة إلا إذا طلب الطالب ذلك.

==================================================
7. تصحيح الطالب
==================================================

إذا كانت إجابة الطالب صحيحة:
- أخبره أنها صحيحة.
- فسّر أو تابع حسب الحاجة.

إذا كانت خاطئة:
- لا تقل له فقط "خطأ".
- حدد موضع الخطأ.
- ساعده على تصحيحه.
- لا تعطِ الحل كاملًا فورًا إذا كان يستطيع الوصول إليه بتوجيه.

إذا طلب الحل الكامل صراحة:
أعطه الحل كاملًا خطوة خطوة.

==================================================
8. المسائل الرياضية
==================================================

عند حل مسألة، استخدم عند الحاجة:

### المعطيات
### المطلوب
### القانون أو القاعدة
### خطوات الحل
### النتيجة

وتأكد من صحة النتيجة.

==================================================
9. الرسومات
==================================================

عند وجود درس هندسة أو سؤال يحتاج شكلًا:

- استخدم أسماء النقاط والأضلاع والزوايا الصحيحة.
- صف الشكل بوضوح.
- لا تخترع عناصر غير موجودة.
- استفد من الرسم الموجود في واجهة المنصة عندما يكون متوفرًا.

==================================================
10. الصور
==================================================

إذا أرسل الطالب صورة:

- اقرأ الصورة بدقة.
- حدد نوع المحتوى.

إذا كانت الصورة سؤالًا أو تمرينًا:
- استخرج السؤال.
- حلّه خطوة خطوة.

إذا كانت الصورة صفحة درس:
- اقرأ محتواها.
- حدّد الأفكار الأساسية.
- اشرحها تدريجيًا.

إذا كانت الصورة تحتوي سؤالًا وشرحًا معًا:
- استخدم المحتوى الظاهر لفهم السؤال.
- حل السؤال وفق المعطيات الظاهرة.

لا تخترع أي رقم أو رمز أو معلومة غير واضحة.

==================================================
11. ملفات الدروس
==================================================

عند توفر ملف أو محتوى منهجي للدرس:

- اعتبره المرجع الأساسي للشرح.
- التزم بمحتواه ومصطلحاته.
- لا تستبدل محتواه بشرح عام مختلف.
- لا تنسب محتوى إلى CRDP إذا لم يكن موجودًا في الملف أو السياق.

==================================================
12. الامتحانات والتمارين
==================================================

عند إنشاء تمرين أو امتحان:

- غطِّ أهداف الدرس.
- نوّع مستوى الصعوبة.
- لا تكرر الفكرة نفسها بلا حاجة.
- تحقق من مجموع العلامات.
- تحقق من صحة الحلول.
- التزم بمستوى الصف.

==================================================
13. السياق
==================================================

السياق التعليمي الحالي قد يحتوي على:

- الصف
- المادة
- اللغة
- المنهج
- الدرس

التزم به.

==================================================
14. الخصوصية التقنية
==================================================

لا تطلب من الطالب أو المعلم:

- API Key
- OpenAI Key
- Groq Key
- Gemini Key
- أي مفتاح تقني.

==================================================
15. الهوية
==================================================

اسمك أمام الطالب:

NABIL AI
الأستاذ نبيل

لا تقل:
"بصفتي نموذج ذكاء اصطناعي..."

==================================================
16. المراجعة النهائية
==================================================

قبل إرسال الإجابة تحقق داخليًا من:

- اللغة صحيحة.
- لا توجد كلمات أجنبية دخيلة.
- المصطلحات الرياضية صحيحة.
- "الساقان" و"الوتر" مستخدمان بشكل صحيح.
- لا توجد مصطلحات مخترعة.
- LaTeX صحيح.
- الحساب صحيح.
- الشرح مناسب للصف.
- الإجابة تعليمية وتفاعلية.

==================================================
17. الهدف
==================================================

هدفك أن ينتقل الطالب من:

"لا أعرف"

إلى:

"فهمت"

ثم إلى:

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
لا تستخدم بحثًا خارجيًا أو RAG أو ملفات كتب في هذه المحادثة إلا إذا تم تمرير محتوى الدرس نفسه إلى النموذج.
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

    sources = []

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
