import asyncio
import hashlib
import json
import os
import re
import threading
import time
from collections import defaultdict, deque
from pathlib import Path
from typing import Optional
from datetime import datetime
 
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
from starlette.concurrency import run_in_threadpool
 
from app.db.session import get_db
from app.db.models import Conversation, Message, Student
from app.db.student_learning import StudentLearningProfile
from app.services.ai_gateway import NabilAIGateway
 
 

router = APIRouter()


# ==========================================================
# Production traffic protection
# ==========================================================

RATE_LIMIT_REQUESTS = int(
    os.getenv("NABIL_RATE_LIMIT_REQUESTS", "8")
)

RATE_LIMIT_WINDOW_SECONDS = int(
    os.getenv("NABIL_RATE_LIMIT_WINDOW_SECONDS", "60")
)

RATE_LIMIT_MIN_INTERVAL_SECONDS = float(
    os.getenv("NABIL_RATE_LIMIT_MIN_INTERVAL_SECONDS", "1.5")
)

AI_MAX_CONCURRENCY = int(
    os.getenv("NABIL_AI_MAX_CONCURRENCY", "30")
)

AI_QUEUE_TIMEOUT_SECONDS = float(
    os.getenv("NABIL_AI_QUEUE_TIMEOUT_SECONDS", "4")
)

LESSON_CACHE_TTL_SECONDS = int(
    os.getenv("NABIL_LESSON_CACHE_TTL_SECONDS", "1800")
)

LESSON_CACHE_MAX_ITEMS = int(
    os.getenv("NABIL_LESSON_CACHE_MAX_ITEMS", "500")
)

_rate_lock = threading.Lock()
_student_request_times = defaultdict(deque)
_student_last_request = {}

_cache_lock = threading.Lock()
_lesson_cache = {}

_ai_gateway_lock = threading.Lock()
_ai_gateway_instance = None

_ai_concurrency = asyncio.Semaphore(
    max(1, AI_MAX_CONCURRENCY)
)


def get_shared_ai_gateway() -> NabilAIGateway:
    global _ai_gateway_instance

    if _ai_gateway_instance is not None:
        return _ai_gateway_instance

    with _ai_gateway_lock:
        if _ai_gateway_instance is None:
            _ai_gateway_instance = NabilAIGateway()

    return _ai_gateway_instance


def enforce_student_rate_limit(
    student_id: str,
) -> None:

    now = time.monotonic()

    with _rate_lock:
        queue = _student_request_times[
            student_id
        ]

        while (
            queue
            and now - queue[0]
            >= RATE_LIMIT_WINDOW_SECONDS
        ):
            queue.popleft()

        last = _student_last_request.get(
            student_id
        )

        if (
            last is not None
            and now - last
            < RATE_LIMIT_MIN_INTERVAL_SECONDS
        ):
            wait_for = max(
                1,
                round(
                    RATE_LIMIT_MIN_INTERVAL_SECONDS
                    - (now - last)
                ),
            )

            raise HTTPException(
                status_code=429,
                detail=(
                    "أرسلت الطلبات بسرعة كبيرة. "
                    f"انتظر نحو {wait_for} ثانية ثم أعد المحاولة."
                ),
            )

        if len(queue) >= RATE_LIMIT_REQUESTS:
            retry_after = max(
                1,
                round(
                    RATE_LIMIT_WINDOW_SECONDS
                    - (now - queue[0])
                ),
            )

            raise HTTPException(
                status_code=429,
                detail=(
                    "وصلت إلى الحد المؤقت للطلبات. "
                    f"أعد المحاولة بعد نحو {retry_after} ثانية."
                ),
            )

        queue.append(now)
        _student_last_request[
            student_id
        ] = now


def _is_cacheable_lesson_start(
    message: str,
    image_bytes: Optional[bytes],
) -> bool:

    if image_bytes is not None:
        return False

    normalized = (
        message
        .strip()
        .lower()
    )

    return normalized.startswith(
        "ابدأ درسًا تفاعليًا"
    )


def _lesson_cache_key(
    *,
    grade: Optional[str],
    branch: Optional[str],
    subject: Optional[str],
    language: Optional[str],
    lesson: Optional[str],
    curriculum: Optional[str],
    message: str,
) -> str:

    raw = "|".join(
        [
            grade or "",
            branch or "",
            subject or "",
            language or "",
            lesson or "",
            curriculum or "",
            " ".join(message.split()),
        ]
    )

    return hashlib.sha256(
        raw.encode("utf-8")
    ).hexdigest()


def _get_cached_lesson(
    cache_key: str,
) -> Optional[str]:

    now = time.monotonic()

    with _cache_lock:
        item = _lesson_cache.get(
            cache_key
        )

        if item is None:
            return None

        expires_at, value = item

        if expires_at <= now:
            _lesson_cache.pop(
                cache_key,
                None,
            )
            return None

        return value


def _store_cached_lesson(
    cache_key: str,
    value: str,
) -> None:

    now = time.monotonic()

    with _cache_lock:
        expired = [
            key
            for key, item
            in _lesson_cache.items()
            if item[0] <= now
        ]

        for key in expired:
            _lesson_cache.pop(
                key,
                None,
            )

        if len(_lesson_cache) >= LESSON_CACHE_MAX_ITEMS:
            oldest_key = min(
                _lesson_cache,
                key=lambda key: _lesson_cache[key][0],
            )

            _lesson_cache.pop(
                oldest_key,
                None,
            )

        _lesson_cache[
            cache_key
        ] = (
            now + LESSON_CACHE_TTL_SECONDS,
            value,
        )


 
 
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
كتلة رسومات واحدة فقط بالشكل التالي:

<DRAWINGS_JSON>
[
  {JSON_OBJECT_1},
  {JSON_OBJECT_2}
]
</DRAWINGS_JSON>

قواعد الرسومات:
- الرسمة الواحدة هي الافتراضية.
- استخدم أكثر من رسمة فقط إذا احتاج الشرح إلى أفكار بصرية مختلفة فعلًا.
- الحد الأقصى 3 رسومات في الجواب الواحد.
- لا تكرر نفس الرسم بتغييرات شكلية فقط.
- رتّب الرسومات بحسب ترتيب الشرح.
- كل عنصر يجب أن يكون JSON صالحًا.
- لا تعرض كتلة JSON للطالب كنص.
- للتوافق مع الإجابات القديمة يستطيع الخادم فهم DRAWING_JSON المفرد أيضًا.
- في الإجابات الجديدة استخدم DRAWINGS_JSON.

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

عند function = "exp" يجب تحديد أساس الدالة الحقيقي في "base".
أمثلة:
- 2^x => "base": 2
- 5^x => "base": 5
- (1/2)^x => "base": 0.5
- e^x => "base": 2.718281828459045

يمكن أيضًا استعمال:
- "coefficient"
- "x_shift"
- "y_shift"
- "slope"
- "intercept"

ممنوع رسم e^x بدل دالة بأساس آخر.
كل نقطة في points يجب أن تحقق الدالة حسابيًا.

 
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
 

--------------------------------------------------
و) مثلث عام
--------------------------------------------------

{
  "type": "triangle",
  "title": "مثلث ABC",
  "labels": {"a": "A", "b": "B", "c": "C"},
  "side_ab": "5 cm",
  "side_ac": "4 cm",
  "side_bc": "6 cm"
}

استخدمه للمثلثات العامة عندما لا يكون النوع right_triangle أنسب.

--------------------------------------------------
ز) نقاط على المستوى الإحداثي
--------------------------------------------------

{
  "type": "coordinate_points",
  "title": "تمثيل النقاط",
  "points": [
    {"label": "A", "x": 2, "y": 3},
    {"label": "B", "x": -1, "y": 1}
  ]
}

--------------------------------------------------
ح) مستقيم الأعداد
--------------------------------------------------

{
  "type": "number_line",
  "title": "تمثيل الأعداد",
  "min": -5,
  "max": 5,
  "marks": [
    {"value": -2, "label": "A"},
    {"value": 3, "label": "B"}
  ]
}



--------------------------------------------------
ط) محرّك الهندسة التحليلية والمتجهات
--------------------------------------------------

عندما يحتاج الدرس رسمًا في معلم متعامد ومتجانس أو مستوى متجهات،
استخدم النوع analytic_plane أو orthonormal_system أو vector_plane.

مثال شامل:

{
  "type": "analytic_plane",
  "title": "Orthonormal system (O; i, j)",
  "xmin": -6,
  "xmax": 6,
  "ymin": -5,
  "ymax": 5,
  "grid": true,
  "points": [
    {"label": "A", "x": 2, "y": 3},
    {"label": "B", "x": -2, "y": 1}
  ],
  "vectors": [
    {"label": "u", "x1": 0, "y1": 0, "x2": 3, "y2": 2},
    {"label": "AB", "x1": 2, "y1": 3, "x2": -2, "y2": 1}
  ],
  "segments": [
    {"label": "[AB]", "x1": 2, "y1": 3, "x2": -2, "y2": 1}
  ],
  "lines": [
    {"label": "d: y=2x+1", "a": 2, "b": -1, "c": 1}
  ],
  "circles": [
    {"label": "(C)", "cx": 1, "cy": 0, "r": 2}
  ],
  "projections": [
    {"x": 2, "y": 3}
  ]
}

قواعد المحرّك:
- points للنقاط وإحداثياتها.
- vectors للمتجهات مع نقطة بداية ونهاية وسهم اتجاه.
- segments للقطع المستقيمة.
- lines للمستقيمات بالصيغة ax + by + c = 0.
- circles للدوائر ذات المركز (cx, cy) ونصف القطر r.
- projections للإسقاطات المتقطعة على المحورين.
- استخدم تدريجًا متساويًا للمحورين عند طلب orthonormal system.
- يمكن تمثيل midpoint كنقطة عادية مع label مناسب.
- يمكن تمثيل translation برسم المتجه وصور النقاط.
- يمكن رسم parallel/perpendicular lines بإرسال معاملات المستقيمات الصحيحة.
- لا تستخدم أي مفهوم تحليلي أو متجهي غير موجود في الدرس الحالي أو الصف الحالي.
- لا تستنتج إحداثيات أو معادلات غير معطاة أو غير مستخرجة حسابيًا من المعطيات.
- إذا كان الرسم البسيط الموجود سابقًا أوضح للطالب، استخدمه بدل هذا المحرّك.


==================================================
6. متى ترسل الرسم؟
==================================================
 
أرسل DRAWINGS_JSON عند:
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
8. الالتزام الصارم بالصف والمنهج
==================================================
 
الصف والمادة والدرس المحددون في السياق ليسوا معلومات إضافية فقط،
بل هم قيود إلزامية على طريقة الشرح والحل.
 
قواعد إلزامية:
- لا تستخدم نظرية أو طريقة أو مصطلحًا من صف أعلى إذا لم يكن ضمن الدرس الحالي.
- لا تحوّل المسألة إلى طريقة أكثر تقدّمًا لمجرد أنها صحيحة رياضيًا.
- إذا كان الدرس هندسة مدرسية، استخدم الهندسة المدرسية المناسبة لذلك الصف أولًا.
- لا تستخدم الهندسة التحليلية أو معادلات الإحداثيات في درس هندسي إذا لم يكن هذا هو موضوع الدرس.
- لا تستخدم التفاضل أو التكامل أو المثلثات أو المتجهات أو اللوغاريتمات أو الأساليب المتقدمة قبل مستوى الطالب.
- الأمثلة والأسئلة الختامية يجب أن تكون من مستوى الصف نفسه.
- إذا كان السؤال يمكن حله بطريقتين، اختر الطريقة الموجودة في منهج الصف الحالي.
- إذا طلب الطالب صراحة طريقة متقدمة، اشرح له أولًا طريقة صفه، ثم اذكر الطريقة المتقدمة فقط على أنها إضافة اختيارية إن كانت مناسبة.
 
للصف التاسع خصوصًا:
- في درس "المماسات والدوائر" / "Tangents and circles" / "Tangentes et cercles":
  * استخدم خصائص المماس والدائرة والهندسة الإقليدية.
  * نصف القطر المرسوم إلى نقطة التماس عمودي على المماس.
  * يمكن استعمال تساوي طولي المماسين المرسومين من نقطة خارجية عند الحاجة.
  * استخدم المثلث القائم وفيثاغورس فقط إذا كان ذلك مناسبًا للمعطيات ومستوى الدرس.
  * لا تستخدم معادلة الدائرة x^2 + y^2 = r^2.
  * لا تخترع إحداثيات مثل M(8,3) أو نقاطًا غير موجودة في السؤال.
  * لا تحوّل الدرس إلى هندسة تحليلية.
- في دروس التمثيل البياني أو الإحداثيات المخصصة لذلك في الصف التاسع،
  يمكن استخدام الإحداثيات لأن الدرس نفسه يسمح بذلك.
 
==================================================
9. التحقق من المستوى قبل الإجابة
==================================================
 
قبل كتابة الجواب، اسأل نفسك داخليًا:
1) ما الصف؟
2) ما الدرس؟
3) ما الأدوات التي تعلمها الطالب في هذا المستوى؟
4) هل طريقتي تحتاج مفهومًا من صف أعلى؟
 
إذا كانت الإجابة نعم، استبدلها بطريقة أبسط من منهج الصف الحالي.
 
لا تذكر هذا الفحص الداخلي للطالب.
 
==================================================
10. سير الدرس والاختبار النهائي
==================================================

عند شرح درس كامل:
- اشرح مفهومًا ثم مثالًا ثم سؤال تحقق قصيرًا.
- بعد إجابة الطالب صحح باختصار ثم تابع للمفهوم التالي.
- لا تكرر Quick Check بلا نهاية.
- عند اكتمال المفاهيم الأساسية أعلن انتهاء الشرح الأساسي.

بعد اكتمال الدرس:
- ابدأ اختبارًا نهائيًا من 5 أسئلة فقط.
- اعرض سؤالًا واحدًا في كل مرة.
- الأسئلة من نفس الصف والمادة والدرس والمنهج.
- لا تعرض الحل قبل إجابة الطالب.
- بعد السؤال الخامس أعط العلامة من 5 والنسبة من 100.
- اذكر نقطتي قوة ونقطتي ضعف كحد أقصى.
- أقل من 70%: اقترح مراجعة مركزة.
- 70% أو أكثر: اعتبر الحد الأدنى من الإتقان متحققًا.

قواعد الأسئلة:
- يجب أن تكون غير ملتبسة.
- فرّق بوضوح بين 5^x-2 و 5^(x-2).
- لا تذكر إمكانية إبقاء الجواب كسرًا إلا إذا كان السؤال ينتج كسرًا.
- تحقق من الجواب المتوقع قبل إرسال السؤال.

==================================================
10. ملف تقدم الطالب - بروتوكول داخلي
==================================================

في نهاية كل إجابة تعليمية أضف كتلة داخلية واحدة فقط:

<PROGRESS_JSON>
{
  "lesson_completed": false,
  "strengths": [],
  "weaknesses": [],
  "mistakes": [],
  "concepts_to_review": [],
  "assessment": {
    "name": "",
    "score": null,
    "out_of": null
  }
}
</PROGRESS_JSON>

قواعد PROGRESS_JSON:
- لا تعرض هذه الكتلة للطالب.
- لا تسجل قوة أو ضعفًا بلا دليل من تفاعل الطالب.
- lesson_completed=true فقط عند اكتمال الدرس فعلًا.
- assessment يُملأ فقط عند تصحيح اختبار واضح.
- إذا لا يوجد تقييم اترك score و out_of بقيمة null.

==================================================
11. الهوية
==================================================
 
اسمك:
NABIL AI
الأستاذ نبيل
 
لا تقل:
"بصفتي نموذج ذكاء اصطناعي".
"""
 
 

CURRICULUM_INDEX_PATH = Path(
    "app/static/crdp_scientific_curriculum_index.json"
)

CURRICULUM_SCHEMA_VERSION = "6"


def load_curriculum_index() -> dict:
    try:
        if not CURRICULUM_INDEX_PATH.exists():
            return {}

        return json.loads(
            CURRICULUM_INDEX_PATH.read_text(
                encoding="utf-8"
            )
        )

    except Exception:
        return {}


def get_lesson_policy(
    grade: Optional[str],
    branch: Optional[str],
    subject: Optional[str],
    lesson_title: Optional[str],
) -> Optional[dict]:

    grade_text = (grade or "").strip()
    branch_text = (branch or "").strip()
    subject_text = (subject or "").strip()
    lesson_text = (lesson_title or "").strip().lower()

    if not all(
        [
            grade_text,
            subject_text,
            lesson_text,
        ]
    ):
        return None

    index = load_curriculum_index()

    details = (
        index
        .get(
            "annual_curriculum_details",
            {}
        )
        .get(
            "الثانوي",
            {}
        )
        .get(
            grade_text,
            {}
        )
    )

    if branch_text:
        details = details.get(
            branch_text,
            {}
        )

    subject_lessons = details.get(
        subject_text,
        []
    )

    for item in subject_lessons:

        title = str(
            item.get(
                "title",
                ""
            )
        ).strip().lower()

        if (
            title == lesson_text
            or lesson_text in title
            or title in lesson_text
        ):
            return item

    return None


def format_lesson_policy_for_prompt(
    policy: Optional[dict],
) -> str:

    if not policy:
        return (
            "لا توجد تفاصيل سنوية دقيقة "
            "لهذا الدرس في ملف الفهرسة الحالي. "
            "التزم بعنوان الدرس فقط ولا تخترع "
            "أي فقرة فرعية غير مؤكدة."
        )

    included = policy.get(
        "included_sections",
        []
    )

    suspended = policy.get(
        "suspended_sections",
        []
    )

    status = policy.get(
        "status",
        "maintained"
    )

    lines = [
        f"حالة الدرس الرسمية: {status}.",
        (
            "مسموح شرح الدرس ضمن الحدود "
            "المذكورة في الفهرسة السنوية فقط."
        ),
    ]

    if included:
        lines.append(
            "الأجزاء المطلوبة حصراً:"
        )

        lines.extend(
            f"- {item}"
            for item in included
        )

    if suspended:
        lines.append(
            "الأجزاء المعلّقة/المحذوفة "
            "وممنوع شرحها كجزء مطلوب:"
        )

        lines.extend(
            f"- {item}"
            for item in suspended
        )

    if policy.get("notes"):
        lines.append(
            "ملاحظة رسمية:"
        )
        lines.append(
            str(
                policy["notes"]
            )
        )

    return "\n".join(lines)


def build_curriculum_guardrail(
    grade: Optional[str],
    subject: Optional[str],
    lesson: Optional[str],
) -> str:
    """
    حارس منهجي عام لجميع الصفوف والمواد.
    الصف + المادة + الدرس = حدود إلزامية لا يجوز تجاوزها.
    """

    grade_text = (grade or "").strip()
    subject_text = (subject or "").strip()
    lesson_text = (lesson or "").strip()
    lower_lesson = lesson_text.lower()

    rules = [
        "الصف المحدد قيد إلزامي على مستوى الشرح والمصطلحات وطريقة الحل.",
        "المادة المحددة قيد إلزامي: لا تنتقل إلى مادة أخرى إلا إذا كان الربط ضروريًا لفهم نفس الدرس.",
        "الدرس المحدد هو الحد الأعلى للمحتوى في هذه المحادثة التعليمية.",
        "لا تضف نظرية أو قاعدة أو مفهومًا من درس آخر لمجرد أنه مفيد أو صحيح.",
        "لا تستخدم طريقة من صف أعلى إذا كانت خارج محتوى الدرس الحالي.",
        "لا تخترع معطيات أو نقاطًا أو إحداثيات أو تجارب أو أرقامًا غير موجودة في السؤال.",
        "إذا احتجت مثالًا من عندك، اجعله بسيطًا ومباشرًا ويختبر نفس مهارة الدرس فقط.",
        "إذا طلب الطالب شيئًا خارج الدرس، أخبره باختصار أنه خارج نطاق الدرس الحالي ثم اسأله إن كان يريد الانتقال إلى الدرس المناسب.",
        "لا تعتبر المعرفة العامة للنموذج بديلًا عن فهرسة المنهج؛ التزم بعنوان الدرس وسياق المنهج المرسل إليك.",
        "أسئلة التحقق والاختبار النهائي يجب أن تقيس محتوى الدرس نفسه فقط.",
        "لا تكرر نفس الفكرة بصيغ مختلفة على أنها مفاهيم جديدة.",
    ]

    primary = {
        "الصف الأول",
        "الصف الثاني",
        "الصف الثالث",
        "الصف الرابع",
        "الصف الخامس",
        "الصف السادس",
    }

    intermediate = {
        "الصف السابع",
        "الصف الثامن",
        "الصف التاسع",
    }

    if grade_text in primary:
        rules.extend([
            "استخدم لغة بسيطة جدًا وجملًا قصيرة وأمثلة محسوسة.",
            "لا تستخدم أي أداة من الحلقة الثالثة أو المرحلة الثانوية.",
            "تجنب الرموز المجردة إذا لم تكن جزءًا من الدرس نفسه.",
        ])

    if grade_text in intermediate:
        rules.extend([
            "استخدم أدوات الحلقة الثالثة فقط.",
            "لا تستخدم التفاضل أو التكامل أو المتجهات أو المصفوفات أو أي تقنية ثانوية متقدمة.",
            "في الهندسة استخدم الخواص والبراهين المدرسية المناسبة للصف قبل أي معالجة تحليلية.",
        ])

    if grade_text == "الأول ثانوي":
        rules.extend([
            "استخدم مفاهيم الأول ثانوي فقط.",
            "لا تستخدم التفاضل أو التكامل قبل أن يكونا ضمن الدرس المحدد.",
        ])

    if grade_text == "الثاني ثانوي":
        rules.extend([
            "استخدم مفاهيم الثاني ثانوي فقط.",
            "لا تستخدم أدوات الثالث ثانوي إلا إذا كانت مذكورة صراحة في الدرس الحالي.",
        ])

    if grade_text == "الثالث ثانوي":
        rules.extend([
            "استخدم أدوات الثالث ثانوي المرتبطة بالدرس الحالي فقط.",
            "لا تقحم موضوعات جامعية أو تقنيات خارج المنهج المدرسي.",
        ])

    if subject_text == "رياضيات":
        rules.extend([
            "لا تحوّل درسًا هندسيًا إلى هندسة تحليلية إلا إذا كان الدرس نفسه عن الإحداثيات أو المعادلات.",
            "لا تستخدم اشتقاقًا أو تكاملًا أو لوغاريتمات أو مثلثات إلا إذا كان عنوان الدرس يسمح بذلك.",
        ])

    elif subject_text == "فيزياء":
        rules.extend([
            "استخدم القوانين والمفاهيم الفيزيائية الخاصة بالدرس الحالي فقط.",
            "لا تدخل قانونًا من فصل آخر لتسريع الحل.",
            "لا تستخدم حساب التفاضل أو المتجهات المتقدمة إذا لم تكن ضمن مستوى الصف والدرس.",
        ])

    elif subject_text == "كيمياء":
        rules.extend([
            "التزم بالتفاعلات والمفاهيم الكيميائية المندرجة ضمن الدرس الحالي فقط.",
            "لا تدخل بنى ذرية أو روابط أو حسابات مولية إذا لم تكن ضمن درس الطالب الحالي.",
            "لا تفترض مادة كيميائية أو تجربة لم يذكرها السؤال إلا كمثال تعليمي واضح ومناسب للدرس.",
        ])

    elif subject_text == "علوم":
        rules.extend([
            "التزم بالمفهوم العلمي المحدد في الدرس وبمستوى المرحلة الابتدائية.",
            "لا تحول درس العلوم إلى شرح تخصصي في الفيزياء أو الكيمياء أو الأحياء يفوق مستوى الصف.",
        ])

    elif subject_text == "علوم الحياة":
        rules.extend([
            "التزم بالبنية أو الوظيفة أو الظاهرة الحيوية المحددة في الدرس.",
            "لا تدخل في الوراثة أو المناعة أو الفسيولوجيا المتقدمة إلا إذا كانت ضمن عنوان الدرس الحالي.",
        ])

    tangent_keywords = (
        "مماس" in lower_lesson
        or "دائر" in lower_lesson
        or "tangent" in lower_lesson
        or "circle" in lower_lesson
        or "tangente" in lower_lesson
        or "cercle" in lower_lesson
    )

    coordinate_keywords = (
        "إحداث" in lower_lesson
        or "معلم" in lower_lesson
        or "تمثيل بياني" in lower_lesson
        or "coordinate" in lower_lesson
        or "graphic" in lower_lesson
        or "repère" in lower_lesson
        or "graphique" in lower_lesson
    )

    if (
        grade_text == "الصف التاسع"
        and subject_text == "رياضيات"
        and tangent_keywords
        and not coordinate_keywords
    ):
        rules.extend([
            "هذا درس هندسة إقليدية للصف التاسع، وليس هندسة تحليلية.",
            "اعتمد خاصية أن نصف القطر عند نقطة التماس عمودي على المماس.",
            "يمكن استخدام تساوي المماسين من نقطة خارجية عند الحاجة.",
            "يمكن استخدام فيثاغورس فقط داخل مثلث قائم ينشأ طبيعيًا من الشكل.",
            "ممنوع استخدام معادلة الدائرة x^2+y^2=r^2 في هذا الدرس.",
            "ممنوع اختراع إحداثيات أو نقاط رقمية لم يذكرها السؤال.",
        ])

    return "\n".join(
        f"- {rule}"
        for rule in rules
    )



def extract_progress_metadata(text: str):
    if not text:
        return text, {}

    metadata = {}

    complete_pattern = (
        r"<PROGRESS_JSON>\s*(.*?)\s*</PROGRESS_JSON>"
    )

    match = re.search(
        complete_pattern,
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )

    if match:
        raw_json = match.group(1).strip()

        try:
            parsed = json.loads(raw_json)

            if isinstance(parsed, dict):
                metadata = parsed

        except Exception:
            # Invalid progress metadata must never break the lesson.
            metadata = {}

        text = re.sub(
            complete_pattern,
            "",
            text,
            flags=re.DOTALL | re.IGNORECASE,
        )

    # Hide malformed/incomplete internal metadata from the student.
    text = re.sub(
        r"<PROGRESS_JSON>.*$",
        "",
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )

    text = re.sub(
        r"</?PROGRESS_JSON>",
        "",
        text,
        flags=re.IGNORECASE,
    )

    return text.strip(), metadata
def _merge_unique_strings(current, new_items, limit=50):
    output = []

    for item in list(current or []) + list(new_items or []):
        value = str(item).strip()

        if value and value not in output:
            output.append(value)

    return output[-limit:]


def get_or_create_learning_profile(
    db: Session,
    student_id: str,
):
    profile = (
        db.query(StudentLearningProfile)
        .filter_by(student_id=student_id)
        .first()
    )

    if profile is None:
        profile = StudentLearningProfile(
            student_id=student_id,
        )

        db.add(profile)
        db.commit()
        db.refresh(profile)

    return profile


def profile_to_dict(profile):
    return {
        "student_id": profile.student_id,
        "current_grade": profile.current_grade,
        "current_branch": profile.current_branch,
        "current_subject": profile.current_subject,
        "current_lesson": profile.current_lesson,
        "lessons_studied": StudentLearningProfile.loads_list(
            profile.lessons_studied_json
        ),
        "lesson_mastery": StudentLearningProfile.loads_list(
            profile.lesson_mastery_json
        ),
        "strengths": StudentLearningProfile.loads_list(
            profile.strengths_json
        ),
        "weaknesses": StudentLearningProfile.loads_list(
            profile.weaknesses_json
        ),
        "frequent_mistakes": StudentLearningProfile.loads_list(
            profile.frequent_mistakes_json
        ),
        "concepts_to_review": StudentLearningProfile.loads_list(
            profile.concepts_to_review_json
        ),
        "test_results": StudentLearningProfile.loads_list(
            profile.test_results_json
        ),
        "overall_progress_percent": float(
            profile.overall_progress_percent or 0
        ),
        "mastered_lessons_count": int(
            profile.mastered_lessons_count or 0
        ),
        "total_learning_minutes": int(
            profile.total_learning_minutes or 0
        ),
        "interaction_count": int(
            profile.interaction_count or 0
        ),
        "last_active_activity": profile.last_active_activity,
        "trial_started_at": (
            profile.trial_started_at.isoformat()
            if profile.trial_started_at
            else None
        ),
        "trial_ends_at": (
            profile.trial_ends_at.isoformat()
            if profile.trial_ends_at
            else None
        ),
        "subscription_status": profile.subscription_status,
        "subscription_started_at": (
            profile.subscription_started_at.isoformat()
            if profile.subscription_started_at
            else None
        ),
        "subscription_ends_at": (
            profile.subscription_ends_at.isoformat()
            if profile.subscription_ends_at
            else None
        ),
    }


def update_lesson_mastery(
    profile,
    grade,
    branch,
    subject,
    lesson,
    metadata,
):
    if not lesson:
        return

    mastery = StudentLearningProfile.loads_list(
        profile.lesson_mastery_json
    )

    key = {
        "grade": grade or "",
        "branch": branch or "",
        "subject": subject or "",
        "lesson": lesson,
    }

    current = None

    for item in mastery:
        if (
            item.get("grade") == key["grade"]
            and item.get("branch") == key["branch"]
            and item.get("subject") == key["subject"]
            and item.get("lesson") == key["lesson"]
        ):
            current = item
            break

    if current is None:
        current = {
            **key,
            "status": "learning",
            "best_score_percent": 0.0,
            "attempts": 0,
        }
        mastery.append(current)

    assessment = (
        metadata.get("assessment")
        if isinstance(metadata, dict)
        else None
    )

    if isinstance(assessment, dict):
        score = assessment.get("score")
        out_of = assessment.get("out_of")

        if (
            isinstance(score, (int, float))
            and isinstance(out_of, (int, float))
            and out_of > 0
        ):
            percent = round(
                float(score) / float(out_of) * 100,
                2,
            )

            current["attempts"] = int(
                current.get("attempts", 0)
            ) + 1

            current["best_score_percent"] = max(
                float(current.get("best_score_percent", 0)),
                percent,
            )

            if percent >= 80:
                current["status"] = "mastered"
            elif percent < 60:
                current["status"] = "needs_review"
            else:
                current["status"] = "learning"

    if metadata.get("lesson_completed") is True:
        if current.get("status") != "needs_review":
            current["status"] = "mastered"

    profile.lesson_mastery_json = (
        StudentLearningProfile.dumps_list(
            mastery[-300:]
        )
    )

    started = [
        item
        for item in mastery
        if item.get("status") in {
            "learning",
            "mastered",
            "needs_review",
        }
    ]

    mastered = [
        item
        for item in mastery
        if item.get("status") == "mastered"
    ]

    profile.mastered_lessons_count = len(mastered)

    if started:
        profile.overall_progress_percent = round(
            len(mastered) / len(started) * 100,
            2,
        )


def update_learning_profile(
    db: Session,
    profile,
    grade,
    branch,
    subject,
    lesson,
    message,
    metadata,
):
    metadata = metadata if isinstance(metadata, dict) else {}

    profile.current_grade = grade or profile.current_grade
    profile.current_branch = branch or profile.current_branch
    profile.current_subject = subject or profile.current_subject
    profile.current_lesson = lesson or profile.current_lesson

    profile.interaction_count = int(
        profile.interaction_count or 0
    ) + 1

    profile.total_learning_minutes = int(
        profile.total_learning_minutes or 0
    ) + 1

    profile.last_active_activity = (
        f"{subject or ''} | {lesson or ''} | {message[:180]}"
    ).strip(" |")

    lessons = StudentLearningProfile.loads_list(
        profile.lessons_studied_json
    )

    if lesson:
        lesson_key = {
            "grade": grade or "",
            "branch": branch or "",
            "subject": subject or "",
            "lesson": lesson,
        }

        if lesson_key not in lessons:
            lessons.append(lesson_key)

    profile.lessons_studied_json = json.dumps(
        lessons[-200:],
        ensure_ascii=False,
    )

    profile.strengths_json = StudentLearningProfile.dumps_list(
        _merge_unique_strings(
            StudentLearningProfile.loads_list(
                profile.strengths_json
            ),
            metadata.get("strengths", []),
        )
    )

    profile.weaknesses_json = StudentLearningProfile.dumps_list(
        _merge_unique_strings(
            StudentLearningProfile.loads_list(
                profile.weaknesses_json
            ),
            metadata.get("weaknesses", []),
        )
    )

    profile.frequent_mistakes_json = StudentLearningProfile.dumps_list(
        _merge_unique_strings(
            StudentLearningProfile.loads_list(
                profile.frequent_mistakes_json
            ),
            metadata.get("mistakes", []),
        )
    )

    profile.concepts_to_review_json = StudentLearningProfile.dumps_list(
        _merge_unique_strings(
            StudentLearningProfile.loads_list(
                profile.concepts_to_review_json
            ),
            metadata.get("concepts_to_review", []),
        )
    )

    tests = StudentLearningProfile.loads_list(
        profile.test_results_json
    )

    assessment = metadata.get("assessment")

    if isinstance(assessment, dict):
        score = assessment.get("score")
        out_of = assessment.get("out_of")

        if (
            isinstance(score, (int, float))
            and isinstance(out_of, (int, float))
            and out_of > 0
        ):
            tests.append(
                {
                    "name": str(
                        assessment.get("name")
                        or lesson
                        or "Assessment"
                    ),
                    "score": float(score),
                    "out_of": float(out_of),
                    "percent": round(
                        float(score)
                        / float(out_of)
                        * 100,
                        2,
                    ),
                    "grade": grade or "",
                    "branch": branch or "",
                    "subject": subject or "",
                    "lesson": lesson or "",
                    "date": datetime.utcnow().isoformat(),
                }
            )

            profile.test_results_json = (
                StudentLearningProfile.dumps_list(
                    tests[-100:]
                )
            )

    if metadata.get("lesson_completed") is True:
        profile.mastered_lessons_count = int(
            profile.mastered_lessons_count or 0
        ) + 1

    percentages = [
        float(item.get("percent", 0))
        for item in tests
        if isinstance(item, dict)
        and isinstance(
            item.get("percent"),
            (int, float),
        )
    ]

    if percentages:
        recent = percentages[-10:]

        profile.overall_progress_percent = round(
            sum(recent) / len(recent),
            2,
        )

    elif lessons:
        profile.overall_progress_percent = min(
            100.0,
            round(len(lessons) * 2.0, 2),
        )

    update_lesson_mastery(
        profile=profile,
        grade=grade,
        branch=branch,
        subject=subject,
        lesson=lesson,
        metadata=metadata,
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)


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
 
 
def _normalize_drawing(drawing):
    if not isinstance(drawing, dict):
        return None

    if drawing.get("type") == "function":
        kind = drawing.get("function")

        if kind == "exp":
            drawing.setdefault("base", 2.718281828459045)
            drawing.setdefault("coefficient", 1)
            drawing.setdefault("x_shift", 0)
            drawing.setdefault("y_shift", 0)

        elif kind in {"ln", "square", "inverse"}:
            drawing.setdefault("coefficient", 1)
            drawing.setdefault("x_shift", 0)
            drawing.setdefault("y_shift", 0)

        elif kind == "linear":
            drawing.setdefault("slope", 1)
            drawing.setdefault("intercept", 0)

    return drawing


def extract_drawings(text: str):
    if not text:
        return text, []

    drawings = []

    multi_pattern = (
        r"<DRAWINGS_JSON>\s*(.*?)\s*</DRAWINGS_JSON>"
    )

    multi_match = re.search(
        multi_pattern,
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )

    if multi_match:
        try:
            parsed = json.loads(
                multi_match.group(1).strip()
            )

            if isinstance(parsed, list):
                for item in parsed[:3]:
                    normalized = _normalize_drawing(item)
                    if normalized is not None:
                        drawings.append(normalized)

            elif isinstance(parsed, dict):
                normalized = _normalize_drawing(parsed)
                if normalized is not None:
                    drawings.append(normalized)

        except Exception:
            drawings = []

        text = re.sub(
            multi_pattern,
            "",
            text,
            flags=re.DOTALL | re.IGNORECASE,
        )

    legacy_pattern = (
        r"<DRAWING_JSON>\s*(.*?)\s*</DRAWING_JSON>"
    )

    legacy_matches = re.findall(
        legacy_pattern,
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )

    for raw in legacy_matches:
        if len(drawings) >= 3:
            break

        try:
            item = json.loads(raw.strip())
            normalized = _normalize_drawing(item)

            if normalized is not None:
                drawings.append(normalized)

        except Exception:
            pass

    text = re.sub(
        legacy_pattern,
        "",
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )

    return text.strip(), drawings


class ChatResponse(BaseModel):
    conversation_id: str
    reply: str
    sources: list[dict] = Field(default_factory=list)
    transcribed_text: Optional[str] = None
    drawings: list[dict] = Field(default_factory=list)
    drawing: Optional[dict] = None
    student_profile: Optional[dict] = None
 
 
@router.get(
    "/student-profile/{student_id}"
)
def get_student_profile(
    student_id: str,
    db: Session = Depends(get_db),
):
    profile = get_or_create_learning_profile(
        db=db,
        student_id=student_id,
    )

    return profile_to_dict(
        profile
    )


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
    branch: Optional[str] = Form(None),
    curriculum: Optional[str] = Form(None),
    language: Optional[str] = Form(None),
    lesson: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    enforce_student_rate_limit(
        student_id
    )

    try:
        ai = get_shared_ai_gateway()

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="خدمة NABIL AI غير جاهزة مؤقتًا.",
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
    else:
        if grade:
            student.grade = grade

        if language:
            student.preferred_language = language

        db.add(student)
        db.commit()

    learning_profile = get_or_create_learning_profile(
        db=db,
        student_id=student_id,
    )

 
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
 
    curriculum_guardrail = build_curriculum_guardrail(
        grade=grade,
        subject=subject,
        lesson=lesson,
    )

    lesson_policy = get_lesson_policy(
        grade=grade,
        branch=branch,
        subject=subject,
        lesson_title=lesson,
    )

    lesson_policy_text = (
        format_lesson_policy_for_prompt(
            lesson_policy
        )
    )

    student_profile_context = profile_to_dict(
        learning_profile
    )

    educational_context = f"""
السياق التعليمي الحالي:
 
الصف: {grade or "غير محدد"}
الفرع: {branch or "غير مطبق"}
المادة: {subject or "غير محددة"}
اللغة الإلزامية: {selected_language}
المنهج: {curriculum or "المنهج اللبناني الرسمي"}
الدرس: {lesson or "غير محدد"}
 
هذه البيانات إلزامية وليست اختيارية.
إذا كان الفرع محددًا فهو قيد منهجي إلزامي، ولا يجوز استخدام محتوى فرع ثانوي آخر.
 
قواعد المستوى لهذا الطلب:
{curriculum_guardrail}
 
تعليمات تنفيذية:
- لا تنتقل إلى مفهوم من صف أعلى.
- إذا كان جزء من الدرس معلّقًا أو محذوفًا رسميًا فلا تشرحه كجزء مطلوب ولا تختبر الطالب فيه.
- استخدم ملف الطالب للاستمرار من مستواه الحالي فقط، ولا تخترع نقاط قوة أو ضعف.
- لا تخترع مثالًا عدديًا متقدمًا إذا لم يطلبه الطالب.
- لا تخترع إحداثيات أو معادلات أو نقاطًا غير موجودة في السؤال.
- إذا كنت تشرح درسًا، ابدأ بالمفهوم والخاصية المناسبة للصف ثم مثال مناسب.
- سؤال التحقق النهائي يجب أن يكون من مستوى الصف نفسه ومن نفس الدرس.
- إذا كان الرسم مفيدًا، أرسل DRAWINGS_JSON مطابقًا للسؤال الحالي ولمستوى الصف، من 1 إلى 3 رسومات فقط عند الحاجة.
- لا تستخدم رسومات ASCII.
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
    cache_key = None
    raw_reply = None

    if _is_cacheable_lesson_start(
        message=message,
        image_bytes=image_bytes,
    ):
        cache_key = _lesson_cache_key(
            grade=grade,
            branch=branch,
            subject=subject,
            language=selected_language,
            lesson=lesson,
            curriculum=curriculum,
            message=message,
        )

        raw_reply = _get_cached_lesson(
            cache_key
        )

    if raw_reply is None:
        acquired = False

        try:
            await asyncio.wait_for(
                _ai_concurrency.acquire(),
                timeout=AI_QUEUE_TIMEOUT_SECONDS,
            )
            acquired = True

        except asyncio.TimeoutError as exc:
            raise HTTPException(
                status_code=503,
                detail=(
                    "هناك ضغط مرتفع على NABIL AI الآن. "
                    "حاول مرة أخرى بعد لحظات."
                ),
            ) from exc

        try:
            raw_reply = await run_in_threadpool(
                ai.generate,
                instructions=SYSTEM_PROMPT,
                messages=history_messages,
                image_bytes=image_bytes,
                image_mime_type=image_mime_type,
                max_output_tokens=3000,
            )

        except Exception as exc:
            raise HTTPException(
                status_code=503,
                detail=str(exc),
            ) from exc

        finally:
            if acquired:
                _ai_concurrency.release()

        if (
            cache_key
            and raw_reply
        ):
            _store_cached_lesson(
                cache_key,
                raw_reply,
            )

 
    raw_reply, progress_metadata = extract_progress_metadata(
        raw_reply
    )

    raw_reply = clean_reply(
        raw_reply
    )
    reply_text, drawings = extract_drawings(
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
    try:
        update_learning_profile(
            db=db,
            profile=learning_profile,
            grade=grade,
            branch=branch,
            subject=subject,
            lesson=lesson,
            message=message,
            metadata=progress_metadata,
        )

    except Exception:
        # Progress saving is secondary; never fail the lesson because of it.
        try:
            db.rollback()
        except Exception:
            pass

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
        drawings=drawings,
        drawing=(
            drawings[0]
            if drawings
            else None
        ),
        student_profile=profile_to_dict(
            learning_profile
        ),
    )
