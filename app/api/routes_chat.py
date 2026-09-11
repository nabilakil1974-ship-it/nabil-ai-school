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


# =========================================================
# SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = r"""
أنت NABIL AI، الأستاذ نبيل، معلّم رقمي ذكي.

مهمتك تعليم الطالب وفق:
- الصف المحدد.
- المادة المحددة.
- اللغة المحددة.
- الدرس المحدد.
- المنهج اللبناني الرسمي.

الصف والمادة والدرس ليست معلومات إضافية،
بل قيود إلزامية يجب احترامها في كل إجابة.


==================================================
1. اللغة
==================================================

أجب باللغة المحددة في السياق.

إذا كانت اللغة العربية:
- استخدم العربية فقط في الشرح.
- لا تخلط كلمات إنجليزية أو فرنسية دون ضرورة تعليمية.
- الرموز الرياضية مثل x و y و ln(x) و e^x تبقى كما هي.

إذا كانت English:
- أجب باللغة الإنجليزية فقط، باستثناء الرموز العلمية اللازمة.

إذا كانت Français:
- أجب باللغة الفرنسية فقط، باستثناء الرموز العلمية اللازمة.


==================================================
2. أسلوب التعليم
==================================================

- اشرح بمستوى الطالب الحقيقي.
- استخدم المصطلحات العلمية الصحيحة.
- تحقق من جميع العمليات الحسابية قبل إرسالها.
- إذا كان السؤال بسيطًا فلا تطل بلا حاجة.
- إذا كان درسًا، اشرح تدريجيًا.
- إذا كان تمرينًا، حلّه خطوة خطوة.
- إذا طلب الطالب الحل الكامل، أعطه الحل الكامل.
- لا تقفز مباشرة إلى أدوات أو نظريات من صف أعلى.
- لا تجعل المثال أصعب من المفهوم الذي تريد شرحه.
- لا تخترع معطيات غير موجودة في سؤال الطالب.
- لا تخترع نقاطًا أو إحداثيات أو أطوالًا بلا ضرورة.
- استخدم أمثلة مناسبة للصف والدرس.


==================================================
3. الرياضيات وLaTeX
==================================================

استخدم LaTeX صحيحًا وواضحًا.

أمثلة صحيحة:

\[
a^2+b^2=c^2
\]

\[
\frac{a}{b}
\]

\[
\sqrt{x}
\]

\[
\boxed{x=5}
\]

مثال لدالة أسية:

\[
g(x)=\left(\frac{1}{2}\right)^x
\]

قواعد إلزامية:

- استخدم \frac وليس \dfrac.
- إذا استخدمت \left فيجب أن تستخدم \right المقابلة لها.
- تأكد من إغلاق جميع الأقواس.
- لا تكتب أبدًا:
  \boxedOT
- اكتب:
  \boxed{OT=5\text{ cm}}

- لا تكتب أوامر LaTeX كنص عادي خارج محددات الرياضيات.
- لا تستخدم رموزًا مشوهة أو غير قياسية.
- عند كتابة أس يحتوي أكثر من رمز استخدم الأقواس بوضوح.

مثال:

بدلًا من كتابة صيغة ملتبسة مثل:

5^x-2

إذا كنت تقصد:

\[
5^{x-2}
\]

فاكتب الأس كاملًا بوضوح.

وإذا كنت تقصد:

\[
5^x-2
\]

فاكتبها بهذا الشكل ووضح أن -2 خارج الأس.

راجع المعادلات قبل الإرسال.


==================================================
4. ممنوع رسومات ASCII
==================================================

لا تستخدم رسومات نصية أو ASCII إطلاقًا.

ممنوع رسم أشكال باستخدام:

*
/
|
-
\

أو أي رسم نصي مشابه.

الرسم المرئي تتولاه واجهة NABIL AI عبر DRAWING_JSON.


==================================================
5. الصور
==================================================

إذا أرسل الطالب صورة:

- اقرأها كاملة.
- إذا كانت تمرينًا، استخرج السؤال ثم حله.
- إذا كانت صفحة درس، اشرح محتواها.
- إذا كان فيها رسم، اقرأ أسماء النقاط والمعطيات.
- لا تخترع أي رقم أو رمز غير واضح.
- إذا كانت معلومة غير مقروءة، قل إنها غير واضحة.
- لا تعرض التفكير الداخلي أو التخمينات.


==================================================
6. الرسم الديناميكي
==================================================

إذا كان الجواب يستفيد فعلًا من رسم،
أضف في نهاية الإجابة كتلة واحدة فقط:

<DRAWING_JSON>
{JSON}
</DRAWING_JSON>

لا تعرض هذه الكتلة للطالب كنص.

يجب أن يكون JSON صالحًا تمامًا.

لا تستخدم تعليقات داخل JSON.


--------------------------------------------------
أ) رسم دالة رياضية
--------------------------------------------------

مثال ln(x):

<DRAWING_JSON>
{
  "type": "function",
  "title": "Graph of ln(x)",
  "function": "ln",
  "expression": "ln(x)",
  "coefficient": 1,
  "x_shift": 0,
  "y_shift": 0,
  "x_min": -1,
  "x_max": 7,
  "y_min": -4,
  "y_max": 3,
  "points": [
    {
      "x": 1,
      "y": 0,
      "label": "(1,0)"
    },
    {
      "x": 2.71828,
      "y": 1,
      "label": "(e,1)"
    }
  ],
  "vertical_asymptote": 0
}
</DRAWING_JSON>


القيم المقبولة حاليًا في:

"function"

هي:

ln
exp
square
linear
inverse


--------------------------------------------------
الدوال الأسية
--------------------------------------------------

عند رسم دالة أسية يجب تحديد الأساس الحقيقي.

إذا كانت:

\[
f(x)=2^x
\]

استخدم:

<DRAWING_JSON>
{
  "type": "function",
  "title": "Graph of f(x)=2^x",
  "function": "exp",
  "expression": "2^x",
  "base": 2,
  "coefficient": 1,
  "x_shift": 0,
  "y_shift": 0,
  "x_min": -4,
  "x_max": 5,
  "y_min": -1,
  "y_max": 17,
  "points": [
    {
      "x": -2,
      "y": 0.25,
      "label": "(-2,0.25)"
    },
    {
      "x": -1,
      "y": 0.5,
      "label": "(-1,0.5)"
    },
    {
      "x": 0,
      "y": 1,
      "label": "(0,1)"
    },
    {
      "x": 1,
      "y": 2,
      "label": "(1,2)"
    },
    {
      "x": 2,
      "y": 4,
      "label": "(2,4)"
    },
    {
      "x": 3,
      "y": 8,
      "label": "(3,8)"
    },
    {
      "x": 4,
      "y": 16,
      "label": "(4,16)"
    }
  ],
  "horizontal_asymptote": 0
}
</DRAWING_JSON>


إذا كانت:

\[
g(x)=\left(\frac{1}{2}\right)^x
\]

استخدم:

<DRAWING_JSON>
{
  "type": "function",
  "title": "Graph of g(x)=(1/2)^x",
  "function": "exp",
  "expression": "(1/2)^x",
  "base": 0.5,
  "coefficient": 1,
  "x_shift": 0,
  "y_shift": 0,
  "x_min": -4,
  "x_max": 6,
  "y_min": -1,
  "y_max": 10,
  "points": [
    {
      "x": -2,
      "y": 4,
      "label": "(-2,4)"
    },
    {
      "x": -1,
      "y": 2,
      "label": "(-1,2)"
    },
    {
      "x": 0,
      "y": 1,
      "label": "(0,1)"
    },
    {
      "x": 1,
      "y": 0.5,
      "label": "(1,0.5)"
    },
    {
      "x": 2,
      "y": 0.25,
      "label": "(2,0.25)"
    },
    {
      "x": 3,
      "y": 0.125,
      "label": "(3,0.125)"
    }
  ],
  "horizontal_asymptote": 0
}
</DRAWING_JSON>


إذا كانت:

\[
h(x)=5^{x-2}+3
\]

استخدم:

"base": 5

"x_shift": 2

"y_shift": 3


قاعدة مهمة جدًا:

ممنوع رسم:

e^x

بدل:

2^x

أو:

5^x

أو:

(1/2)^x

يجب أن يكون الأساس في الرسم هو نفس أساس السؤال.


--------------------------------------------------
ب) مثلث قائم
--------------------------------------------------

<DRAWING_JSON>
{
  "type": "right_triangle",
  "title": "Right triangle",
  "a": 3,
  "b": 4,
  "c": 5,
  "labels": {
    "a": "3 cm",
    "b": "4 cm",
    "c": "5 cm"
  }
}
</DRAWING_JSON>

إذا لم تكن بعض الأطوال معروفة استخدم null.


--------------------------------------------------
ج) دائرة ومماس
--------------------------------------------------

<DRAWING_JSON>
{
  "type": "circle_tangent",
  "title": "Circle and tangent",
  "radius": 5,
  "center": "O",
  "tangent_point": "T",
  "external_point": null
}
</DRAWING_JSON>

لا تضف نقطة خارجية إذا لم تكن مستخدمة في السؤال أو الشرح.


--------------------------------------------------
د) مخطط القوى
--------------------------------------------------

<DRAWING_JSON>
{
  "type": "forces",
  "title": "Force diagram",
  "object": "m",
  "forces": [
    {
      "direction": "up",
      "label": "N"
    },
    {
      "direction": "down",
      "label": "mg"
    }
  ]
}
</DRAWING_JSON>

الاتجاهات المقبولة:

up
down
left
right


--------------------------------------------------
هـ) جزيء مبسط
--------------------------------------------------

<DRAWING_JSON>
{
  "type": "molecule",
  "title": "Molecular structure",
  "atoms": [
    {
      "label": "H"
    },
    {
      "label": "O"
    },
    {
      "label": "H"
    }
  ]
}
</DRAWING_JSON>


==================================================
7. متى ترسل الرسم؟
==================================================

أرسل DRAWING_JSON عندما يكون الرسم مفيدًا، مثل:

- رسم دالة.
- درس يتناول graph أو curve.
- سؤال يقول plot أو draw أو graph.
- هندسة تحتاج شكلًا.
- فيثاغورس.
- دائرة أو مماس.
- مخطط قوى.
- بنية جزيئية مبسطة.

إذا قال الطالب:

plot the graph

فاعتمد الدالة التي كان يناقشها في الرسائل السابقة.

لا تطلب منه إعادة كتابة الدالة إذا كانت واضحة من سياق المحادثة.


==================================================
8. قواعد صحة الرسم
==================================================

- الرسم يجب أن يمثل السؤال الحالي.
- لا تستخدم مثالًا مختلفًا عن السؤال.
- لا تخترع نقاطًا غير موجودة بلا داعٍ.
- كل نقطة ترسمها يجب أن تحقق الدالة حسابيًا.
- تحقق من كل نقطة قبل إرسال DRAWING_JSON.
- إذا كان السؤال عن ln(x)، استخدم ln.
- إذا كان السؤال عن 2^x، استخدم base=2.
- إذا كان السؤال عن (1/2)^x، استخدم base=0.5.
- إذا كان السؤال عن 5^x، استخدم base=5.
- إذا لم تعرف قيمة هندسية، استخدم null.
- لا تضف عناصر غير مستخدمة إلى الشكل.


==================================================
9. الالتزام الصارم بالصف والمنهج
==================================================

الصف والمادة والدرس المحددون في السياق
قيود إلزامية على طريقة الشرح والحل.

قواعد إلزامية:

- لا تستخدم نظرية أو طريقة من صف أعلى.
- لا تحول المسألة إلى طريقة أكثر تقدمًا لمجرد أنها صحيحة.
- إذا كان الدرس هندسة مدرسية، استخدم الهندسة المدرسية.
- لا تستخدم الهندسة التحليلية إلا عندما يكون الدرس نفسه عنها.
- لا تستخدم التفاضل أو التكامل أو المتجهات قبل المستوى المناسب.
- الأمثلة والأسئلة يجب أن تكون من مستوى الصف.
- إذا كان للسؤال عدة طرق، اختر طريقة الصف الحالي.


للصف التاسع خصوصًا:

في درس:

المماسات والدوائر
Tangents and circles
Tangentes et cercles

استخدم:

- خصائص المماس.
- خصائص الدائرة.
- الهندسة الإقليدية.
- نصف القطر إلى نقطة التماس عمودي على المماس.
- المماسان المرسومان من نقطة خارجية متساويان عند الحاجة.
- فيثاغورس فقط إذا ظهر مثلث قائم طبيعيًا في الشكل.

ممنوع في هذا الدرس:

- استخدام معادلة الدائرة:

x^2+y^2=r^2

- اختراع نقطة مثل:

M(8,3)

- تحويل السؤال إلى هندسة تحليلية.

أما دروس الإحداثيات والتمثيل البياني نفسها،
فيمكن استخدام الإحداثيات فيها.


==================================================
10. التحقق من المستوى
==================================================

قبل الإجابة تحقق داخليًا من:

1. ما الصف؟
2. ما المادة؟
3. ما الدرس؟
4. ما المفاهيم التي يعرفها الطالب في هذا المستوى؟
5. هل الطريقة التي سأستخدمها تحتاج مفهومًا من صف أعلى؟

إذا كانت الطريقة أعلى من مستوى الطالب،
استبدلها بطريقة مناسبة للصف.

لا تعرض هذا الفحص الداخلي للطالب.


==================================================
11. سير الدرس
==================================================

عند بدء درس:

- ابدأ بتمهيد قصير.
- اشرح المفهوم الأول.
- أعط مثالًا مناسبًا.
- أعط سؤال تحقق قصيرًا.
- انتظر إجابة الطالب.

بعد إجابة الطالب:

- صححها.
- إذا كانت خاطئة، اشرح الخطأ باختصار.
- انتقل للمفهوم التالي.

لا تكرر Quick Check بلا نهاية.

تابع حتى تغطي المفاهيم الأساسية للدرس.


==================================================
12. الاختبار النهائي
==================================================

بعد اكتمال المفاهيم الأساسية للدرس:

قل للطالب إن الشرح الأساسي للدرس انتهى
وأنه سيبدأ اختبارًا قصيرًا.

أنشئ اختبارًا نهائيًا من:

5 أسئلة فقط.

شروط الاختبار:

- من نفس الصف.
- من نفس المادة.
- من نفس الدرس.
- من المنهج المحدد.
- باللغة المحددة.
- لا تستخدم مفهومًا من صف أعلى.

نوّع الأسئلة قدر الإمكان بين:

- فهم مفهوم.
- تطبيق مباشر.
- اختيار من متعدد.
- صح أو خطأ.
- مسألة قصيرة.
- رسم أو قراءة شكل إذا كان مناسبًا.


==================================================
13. طريقة إجراء الاختبار
==================================================

لا تعرض الأسئلة الخمسة دفعة واحدة.

اعرض:

السؤال 1 فقط.

ثم انتظر جواب الطالب.

بعد جوابه:

- صحح بسرعة.
- لا تعط تقييمًا نهائيًا بعد.
- أعط السؤال 2.

ثم السؤال 3.

ثم السؤال 4.

ثم السؤال 5.


بعد السؤال الخامس:

احسب:

العلامة من 5.

ثم:

النسبة من 100.

مثال:

4/5 = 80%


ثم أعط:

- نقاط القوة: نقطتان كحد أقصى.
- نقاط الضعف: نقطتان كحد أقصى.

إذا كانت العلامة أقل من 70%:

- أخبر الطالب أنه يحتاج مراجعة مركزة.
- اقترح المفاهيم التي يجب مراجعتها.

إذا كانت العلامة 70% أو أكثر:

- اعتبر أن الطالب حقق الحد الأدنى من الإتقان.


==================================================
14. قواعد جودة أسئلة التحقق والاختبار
==================================================

كل سؤال يجب أن يكون:

- واضحًا.
- غير ملتبس.
- له جواب صحيح محدد.
- مناسبًا للصف.
- مطابقًا للدرس.

قبل إرسال السؤال:
احسب جوابه داخليًا للتأكد من صحته.

إذا كتبت دالة أسية،
وضح مكان الأس بدقة.

مثال:

\[
h(x)=5^x-2
\]

يعني -2 خارج الأس.

أما:

\[
h(x)=5^{x-2}
\]

فيعني x-2 داخل الأس.

لا تستخدم صيغة يمكن فهمها بطريقتين.

لا تقل:

"يمكنك إبقاء الجواب ككسر"

إلا إذا كان السؤال فعلًا قد ينتج كسرًا.


==================================================
15. هوية NABIL AI
==================================================

اسمك:

NABIL AI
الأستاذ نبيل

لا تقل:

"بصفتي نموذج ذكاء اصطناعي"

ولا تذكر أسماء مزودي الذكاء الاصطناعي للطالب.
"""


# =========================================================
# CURRICULUM GUARDRAILS
# =========================================================

def build_curriculum_guardrail(
    grade: Optional[str],
    subject: Optional[str],
    lesson: Optional[str],
) -> str:

    grade_text = (
        grade or ""
    ).strip()

    subject_text = (
        subject or ""
    ).strip()

    lesson_text = (
        lesson or ""
    ).strip().lower()

    rules = [
        (
            "استخدم فقط الأدوات والمفاهيم "
            "المناسبة للصف المحدد."
        ),
        (
            "لا تخترع معطيات أو نقاطًا أو "
            "إحداثيات غير موجودة في سؤال الطالب."
        ),
        (
            "إذا كان الدرس محددًا، ابقَ داخل نطاقه "
            "ولا تستبدله بموضوع أكثر تقدمًا."
        ),
    ]

    # -----------------------------------------------------
    # Grades 1–6
    # -----------------------------------------------------

    if grade_text in {
        "الصف الأول",
        "الصف الثاني",
        "الصف الثالث",
        "الصف الرابع",
        "الصف الخامس",
        "الصف السادس",
    }:

        rules.extend(
            [
                (
                    "استخدم لغة بسيطة جدًا "
                    "وأمثلة محسوسة ومباشرة."
                ),
                (
                    "تجنب الرموز والجبر المتقدم "
                    "ما لم يكن ضمن الدرس."
                ),
                (
                    "لا تستخدم مفاهيم من المرحلة "
                    "المتوسطة أو الثانوية."
                ),
            ]
        )

    # -----------------------------------------------------
    # Grades 7–9
    # -----------------------------------------------------

    if grade_text in {
        "الصف السابع",
        "الصف الثامن",
        "الصف التاسع",
    }:

        rules.extend(
            [
                "استخدم طرق الحلقة الثالثة فقط.",
                (
                    "تجنب التفاضل والتكامل والمتجهات "
                    "والأساليب الثانوية المتقدمة."
                ),
                (
                    "في الهندسة فضّل البرهان "
                    "والخواص الهندسية المدرسية."
                ),
            ]
        )

    # -----------------------------------------------------
    # Grade 9 math: tangents
    # -----------------------------------------------------

    is_grade_9 = (
        grade_text ==
        "الصف التاسع"
    )

    is_math = (
        subject_text ==
        "رياضيات"
    )

    tangent_keywords = (
        "مماس" in lesson_text
        or "دائر" in lesson_text
        or "tangent" in lesson_text
        or "circle" in lesson_text
        or "tangente" in lesson_text
        or "cercle" in lesson_text
    )

    coordinate_keywords = (
        "إحداث" in lesson_text
        or "معلم" in lesson_text
        or "تمثيل بياني" in lesson_text
        or "graphic" in lesson_text
        or "coordinate" in lesson_text
        or "repère" in lesson_text
        or "graphique" in lesson_text
    )

    if (
        is_grade_9
        and is_math
        and tangent_keywords
        and not coordinate_keywords
    ):

        rules.extend(
            [
                (
                    "هذا درس هندسة إقليدية للصف التاسع، "
                    "وليس هندسة تحليلية."
                ),
                (
                    "اعتمد خاصية أن نصف القطر عند "
                    "نقطة التماس عمودي على المماس."
                ),
                (
                    "يمكن استخدام تساوي المماسين "
                    "من نقطة خارجية عند الحاجة."
                ),
                (
                    "يمكن استخدام فيثاغورس فقط "
                    "داخل مثلث قائم طبيعي من الشكل."
                ),
                (
                    "ممنوع استخدام معادلة الدائرة "
                    "x^2+y^2=r^2 في هذا الدرس."
                ),
                (
                    "ممنوع اختراع إحداثيات "
                    "أو نقاط رقمية لم يذكرها السؤال."
                ),
                (
                    "اجعل أسئلة التحقق والاختبار "
                    "هندسية ومن مستوى التاسع."
                ),
            ]
        )

    # -----------------------------------------------------
    # Secondary 1
    # -----------------------------------------------------

    if grade_text == "الأول ثانوي":

        rules.extend(
            [
                "استخدم مفاهيم الأول ثانوي فقط.",
                (
                    "لا تستخدم التفاضل أو التكامل "
                    "قبل ظهورها في الصفوف اللاحقة."
                ),
            ]
        )

    # -----------------------------------------------------
    # Secondary 2
    # -----------------------------------------------------

    if grade_text == "الثاني ثانوي":

        rules.extend(
            [
                "استخدم مفاهيم الثاني ثانوي فقط.",
                (
                    "يمكن استخدام النهايات والمشتقات "
                    "فقط عندما يكون الدرس متعلقًا بها."
                ),
                (
                    "لا تستخدم أدوات الثالث ثانوي "
                    "إلا إذا طلبها الطالب كإضافة."
                ),
            ]
        )

    # -----------------------------------------------------
    # Secondary 3
    # -----------------------------------------------------

    if grade_text == "الثالث ثانوي":

        rules.extend(
            [
                (
                    "يمكن استخدام أدوات الثالث ثانوي "
                    "المرتبطة بالدرس الحالي."
                ),
                (
                    "لا تقحم موضوعات جامعية "
                    "تتجاوز المنهج المدرسي."
                ),
            ]
        )

    return "\n".join(
        f"- {rule}"
        for rule in rules
    )


# =========================================================
# CLEAN AI REPLY
# =========================================================

def clean_reply(
    text: str,
) -> str:

    if not text:
        return ""

    # Remove hidden reasoning tags
    text = re.sub(
        r"<think>.*?</think>",
        "",
        text,
        flags=(
            re.DOTALL |
            re.IGNORECASE
        ),
    )

    if "</think>" in text:
        text = text.split(
            "</think>"
        )[-1]

    if "<think>" in text:
        text = text.split(
            "<think>"
        )[0]

    # Normalize common LaTeX variants
    text = text.replace(
        r"\dfrac",
        r"\frac",
    )

    # Fix occasional model formatting
    text = re.sub(
        r"\\boxed\s+([A-Za-z0-9=+\-*/. ]+)",
        r"\\boxed{\1}",
        text,
    )

    return text.strip()


# =========================================================
# DRAWING NORMALIZATION
# =========================================================

def infer_exponential_base(
    expression: str,
) -> Optional[float]:

    if not expression:
        return None

    expr = expression.replace(
        " ",
        "",
    )

    # (1/2)^x
    fraction_match = re.search(
        r"\(?([0-9.]+)\s*/\s*([0-9.]+)\)?\^",
        expr,
    )

    if fraction_match:

        numerator = float(
            fraction_match.group(1)
        )

        denominator = float(
            fraction_match.group(2)
        )

        if denominator != 0:
            return (
                numerator /
                denominator
            )

    # 2^x, 5^x, etc.
    simple_match = re.search(
        r"([0-9]*\.?[0-9]+)\^",
        expr,
    )

    if simple_match:
        return float(
            simple_match.group(1)
        )

    # e^x
    if re.search(
        r"\be\^",
        expr,
        flags=re.IGNORECASE,
    ):
        return 2.718281828459045

    return None


def normalize_drawing(
    drawing: Optional[dict],
) -> Optional[dict]:

    if not isinstance(
        drawing,
        dict,
    ):
        return None

    drawing_type = drawing.get(
        "type"
    )

    if drawing_type != "function":
        return drawing

    function_kind = drawing.get(
        "function"
    )

    if function_kind == "exp":

        base = drawing.get(
            "base"
        )

        if base is None:

            inferred = (
                infer_exponential_base(
                    str(
                        drawing.get(
                            "expression",
                            "",
                        )
                    )
                )
            )

            if inferred is not None:
                drawing["base"] = (
                    inferred
                )

        if "coefficient" not in drawing:
            drawing[
                "coefficient"
            ] = 1

        if "x_shift" not in drawing:
            drawing[
                "x_shift"
            ] = 0

        if "y_shift" not in drawing:
            drawing[
                "y_shift"
            ] = 0

    if function_kind in {
        "ln",
        "square",
        "inverse",
    }:

        drawing.setdefault(
            "coefficient",
            1,
        )

        drawing.setdefault(
            "x_shift",
            0,
        )

        drawing.setdefault(
            "y_shift",
            0,
        )

    if function_kind == "linear":

        drawing.setdefault(
            "slope",
            1,
        )

        drawing.setdefault(
            "intercept",
            0,
        )

    return drawing


# =========================================================
# EXTRACT DRAWING JSON
# =========================================================

def extract_drawing(
    text: str,
):

    if not text:
        return text, None

    pattern = (
        r"<DRAWING_JSON>\s*"
        r"(.*?)"
        r"\s*</DRAWING_JSON>"
    )

    match = re.search(
        pattern,
        text,
        flags=(
            re.DOTALL |
            re.IGNORECASE
        ),
    )

    if not match:
        return (
            text.strip(),
            None,
        )

    drawing = None

    try:

        drawing = json.loads(
            match
            .group(1)
            .strip()
        )

        drawing = (
            normalize_drawing(
                drawing
            )
        )

    except Exception:
        drawing = None

    clean_text = re.sub(
        pattern,
        "",
        text,
        flags=(
            re.DOTALL |
            re.IGNORECASE
        ),
    ).strip()

    return (
        clean_text,
        drawing,
    )


# =========================================================
# RESPONSE MODEL
# =========================================================

class ChatResponse(
    BaseModel
):

    conversation_id: str

    reply: str

    sources: list[dict] = Field(
        default_factory=list
    )

    transcribed_text: Optional[
        str
    ] = None

    drawing: Optional[
        dict
    ] = None


# =========================================================
# CHAT ENDPOINT
# =========================================================

@router.post(
    "/chat",
    response_model=ChatResponse,
)
async def voice_chat(

    audio: Optional[
        UploadFile
    ] = File(None),

    image: Optional[
        UploadFile
    ] = File(None),

    message: Optional[
        str
    ] = Form(None),

    student_id: str = Form(...),

    conversation_id: Optional[
        str
    ] = Form(None),

    subject: Optional[
        str
    ] = Form(None),

    grade: Optional[
        str
    ] = Form(None),

    curriculum: Optional[
        str
    ] = Form(None),

    language: Optional[
        str
    ] = Form(None),

    lesson: Optional[
        str
    ] = Form(None),

    db: Session = Depends(
        get_db
    ),
):

    # =====================================================
    # AI gateway
    # =====================================================

    try:

        ai = NabilAIGateway()

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                "خطأ في إعداد NABIL AI: "
                f"{exc}"
            ),
        ) from exc

    image_bytes = None

    image_mime_type = (
        "image/jpeg"
    )

    transcribed_text = None


    # =====================================================
    # AUDIO
    # =====================================================

    if audio is not None:

        try:

            audio_bytes = (
                await audio.read()
            )

            transcribed_text = (
                ai.transcribe(
                    audio_bytes=(
                        audio_bytes
                    ),
                    filename=(
                        audio.filename
                        or "voice.webm"
                    ),
                )
            )

            message = (
                transcribed_text
            )

        except Exception as exc:

            raise HTTPException(
                status_code=500,
                detail=(
                    "خطأ في معالجة الصوت: "
                    f"{exc}"
                ),
            ) from exc


    # =====================================================
    # IMAGE
    # =====================================================

    if image is not None:

        try:

            image_bytes = (
                await image.read()
            )

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

            if (
                image_mime_type
                not in
                allowed_types
            ):

                raise ValueError(
                    (
                        "نوع الصورة غير مدعوم: "
                        f"{image_mime_type}"
                    )
                )

        except Exception as exc:

            raise HTTPException(
                status_code=400,
                detail=(
                    "خطأ في قراءة الصورة: "
                    f"{exc}"
                ),
            ) from exc


    # =====================================================
    # DEFAULT MESSAGE
    # =====================================================

    if (
        not message
        or not message.strip()
    ):

        if image_bytes is not None:

            message = (
                "اقرأ هذه الصورة كاملة. "
                "إذا كانت تمرينًا فحلّه، "
                "وإذا كانت صفحة درس "
                "فاشرحها بحسب مستوى الطالب."
            )

        else:

            message = (
                "ساعدني في هذا الدرس."
            )

    message = (
        message.strip()
    )


    # =====================================================
    # STUDENT
    # =====================================================

    student = (
        db.query(
            Student
        )
        .filter_by(
            id=student_id
        )
        .first()
    )

    if student is None:

        student = Student(
            id=student_id,
            name=student_id,
            grade=(
                grade
                or "غير محدد"
            ),
            preferred_language=(
                language
                or "العربية"
            ),
        )

        db.add(
            student
        )

        db.commit()

        db.refresh(
            student
        )

    else:

        # Keep profile aligned
        # with current selection.

        if grade:
            student.grade = grade

        if language:
            student.preferred_language = (
                language
            )

        db.commit()


    # =====================================================
    # CONVERSATION
    # =====================================================

    conversation = None

    if conversation_id:

        conversation = (
            db.query(
                Conversation
            )
            .filter_by(
                id=conversation_id
            )
            .first()
        )

    if conversation is None:

        conversation = (
            Conversation(
                student_id=student_id,
                subject=subject,
            )
        )

        db.add(
            conversation
        )

        db.commit()

        db.refresh(
            conversation
        )


    # =====================================================
    # HISTORY
    # =====================================================

    previous_messages = (
        db.query(
            Message
        )
        .filter(
            Message.conversation_id
            ==
            conversation.id
        )
        .order_by(
            Message.created_at.asc()
        )
        .limit(30)
        .all()
    )


    # =====================================================
    # SAVE CURRENT STUDENT MESSAGE
    # =====================================================

    db.add(
        Message(
            conversation_id=(
                conversation.id
            ),
            role="student",
            content=message,
        )
    )

    db.commit()


    # =====================================================
    # CONTEXT
    # =====================================================

    selected_language = (
        language
        or student.preferred_language
        or "العربية"
    )

    curriculum_guardrail = (
        build_curriculum_guardrail(
            grade=grade,
            subject=subject,
            lesson=lesson,
        )
    )

    educational_context = f"""
السياق التعليمي الحالي:

الصف:
{grade or "غير محدد"}

المادة:
{subject or "غير محددة"}

اللغة الإلزامية:
{selected_language}

المنهج:
{curriculum or "المنهج اللبناني الرسمي"}

الدرس:
{lesson or "غير محدد"}


هذه البيانات إلزامية وليست اختيارية.


قواعد المستوى لهذا الطلب:

{curriculum_guardrail}


تعليمات تنفيذية إضافية:

- لا تنتقل إلى مفهوم من صف أعلى.
- لا تخترع مثالًا عدديًا متقدمًا بلا حاجة.
- لا تخترع إحداثيات أو نقاطًا غير موجودة.
- إذا كان هذا درسًا، تابع من النقطة التي وصل إليها الطالب في المحادثة.
- لا تبدأ شرح الدرس من الصفر في كل رسالة.
- إذا أجاب الطالب عن Quick Check، صحح الإجابة ثم تابع الدرس.
- لا تستمر بإعطاء Quick Check إلى ما لا نهاية.
- بعد اكتمال المفاهيم الأساسية، انتقل إلى الاختبار النهائي من 5 أسئلة.
- أثناء الاختبار أعط سؤالًا واحدًا فقط في كل رسالة.
- بعد السؤال الخامس أعط العلامة والتقييم.
- إذا طلب الطالب الرسم أو قال plot / graph / draw، أرسل DRAWING_JSON.
- DRAWING_JSON يجب أن يطابق الدالة أو الشكل الحالي تمامًا.
- لا تستخدم رسومات ASCII.
"""


    # =====================================================
    # HISTORY MESSAGES
    # =====================================================

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
                "content": (
                    msg.content
                ),
            }
        )


    # =====================================================
    # CURRENT PROMPT
    # =====================================================

    current_prompt = f"""
{educational_context}

رسالة الطالب الحالية:

{message}

اعتمد أيضًا على سياق المحادثة السابقة
حتى تعرف أين وصل الطالب في الدرس.

إذا كانت الرسالة مثل:

plot the graph
draw it
ارسمها
ارسم الدالة

فحدد الدالة من سياق المحادثة السابقة
وأرسل DRAWING_JSON المناسب لها.
"""

    history_messages.append(
        {
            "role": "user",
            "content": (
                current_prompt
            ),
        }
    )


    # =====================================================
    # AI
    # =====================================================

    try:

        raw_reply = (
            ai.generate(
                instructions=(
                    SYSTEM_PROMPT
                ),
                messages=(
                    history_messages
                ),
                image_bytes=(
                    image_bytes
                ),
                image_mime_type=(
                    image_mime_type
                ),
                max_output_tokens=(
                    3500
                ),
            )
        )

    except Exception as exc:

        # نبقي التفاصيل ظاهرة حاليًا
        # أثناء مرحلة التطوير كما اتفقنا.

        raise HTTPException(
            status_code=500,
            detail=(
                "خطأ في NABIL AI: "
                f"{exc}"
            ),
        ) from exc


    # =====================================================
    # CLEAN
    # =====================================================

    raw_reply = (
        clean_reply(
            raw_reply
        )
    )


    # =====================================================
    # DRAWING
    # =====================================================

    reply_text, drawing = (
        extract_drawing(
            raw_reply
        )
    )


    # =====================================================
    # VALIDATE REPLY
    # =====================================================

    if not reply_text:

        raise HTTPException(
            status_code=500,
            detail=(
                "NABIL AI لم يُرجع إجابة."
            ),
        )


    # =====================================================
    # SAVE ASSISTANT MESSAGE
    # =====================================================

    db.add(
        Message(
            conversation_id=(
                conversation.id
            ),
            role="teacher",
            content=(
                reply_text
            ),
        )
    )

    db.commit()


    # =====================================================
    # RESPONSE
    # =====================================================

    return ChatResponse(
        conversation_id=str(
            conversation.id
        ),
        reply=reply_text,
        sources=[],
        transcribed_text=(
            transcribed_text
        ),
        drawing=drawing,
    )
