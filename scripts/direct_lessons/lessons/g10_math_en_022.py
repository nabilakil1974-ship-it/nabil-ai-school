"""Grade 10 Mathematics — Polynomials."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G10-MATH-EN-022"
GRADE = 10
SUBJECT = "math"
TITLES = {"en": "Polynomials", "ar": "كثيرات الحدود", "fr": "Polynômes"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "Degree of 5 − 4x² + x⁵ ?", "opts": ["5", "2", "7", "0"], "a": 0,
     "why": {"2": _w("Look for the largest exponent.", "نبحث عن أكبر أس.", "Plus grand exposant."),
             "7": _w("Do not add exponents.", "لا نجمع الأسس.", "Pas de somme."),
             "0": _w("That is the constant term.", "هذا الحد الثابت.", "Constante.")}, "ok": "degree 5"},
    {"q": "(x + 2)² = ?", "opts": ["x² + 4x + 4", "x² + 4", "x² + 2x + 4", "x² + 2"], "a": 0,
     "why": {"x² + 4": _w("The middle term 4x is missing.", "ينقص الحد الأوسط 4x.", "Terme du milieu."),
             "x² + 2x + 4": _w("Middle term is 2·x·2 = 4x.", "الحد الأوسط 2·x·2 = 4x.", "4x."),
             "x² + 2": _w("Expand (x+2)(x+2).", "ننشر (x+2)(x+2).", "Développe.")}, "ok": "x² + 4x + 4"},
    {"q": "x² − 9 = 0 → x = ?", "opts": ["3 or −3", "3", "9", "−9"], "a": 0,
     "why": {"3": _w("(x−3)(x+3) = 0 gives two roots.", "(x−3)(x+3) = 0 تعطي جذرين.", "Deux racines."),
             "9": _w("x² = 9 means x = ±3.", "x² = 9 تعني x = ±3.", "±3."),
             "−9": _w("x² = 9 means x = ±3.", "x² = 9 تعني x = ±3.", "±3.")}, "ok": "x = ±3"},
]

THEORY = [
    ("One polynomial, many forms", "كثير حدود بأشكال متعددة", "Un polynôme, plusieurs formes", "227", [
        T("Hello! Before any calculation, look at a polynomial as a structure that can appear in different forms. P(x) = x² + 5x + 6 and P(x) = (x + 2)(x + 3) are the same polynomial, but each form tells us something different. The expanded form shows the terms clearly; the factorized form makes the zeros easy to see.",
          "مرحبًا! قبل أي حساب انظر إلى كثير الحدود كبنية يمكن أن تظهر بأشكال مختلفة. P(x) = x² + 5x + 6 وP(x) = (x + 2)(x + 3) هما كثير الحدود نفسه، لكن كل شكل يخبرنا بشيء مختلف. الشكل المنشور يُظهر الحدود بوضوح، والشكل المحلَّل يجعل الأصفار أسهل رؤيةً.",
          "Forme développée / factorisée."),
        F("x² + 5x + 6 = (x + 2)(x + 3)"),
    ]),
    ("Read the structure", "نقرأ البنية", "Lire la structure", "227", [
        T("P(x) = 3x³ − 2x + 7. The variable is x and the highest term is 3x³, so the degree is 3. The missing x² does not mean the expression is not a polynomial: its coefficient is 0. What is the degree of 5 − 4x² + x⁵? Find the largest exponent first: 5.",
          "P(x) = 3x³ − 2x + 7. المتغير x والحد الأعلى درجة 3x³ لذلك الدرجة 3. غياب x² لا يعني أنه ليس كثير حدود: معاملها 0. ما درجة 5 − 4x² + x⁵؟ نبحث عن أكبر أس أولًا: 5.",
          "Degré 3 ; puis degré 5."),
        F("deg(3x³ − 2x + 7) = 3"),
    ]),
    ("Why choose a form?", "لماذا نختار الشكل؟", "Pourquoi choisir ?", "228", [
        T("P(x) = x² − 9. To evaluate at x = 4, the expanded form is direct. To solve P(x) = 0, think factorization: x² − 9 = (x − 3)(x + 3), and by the zero-product reasoning x = 3 or x = −3.",
          "P(x) = x² − 9. إذا طُلب التقويم عند x = 4 فالشكل المنشور مباشر. أما حلّ P(x) = 0 فنفكر بالتحليل: x² − 9 = (x − 3)(x + 3) ومن قاعدة الجداء المعدوم نحصل على x = 3 أو x = −3.",
          "x = 3 ou −3."),
        F("(x − 3)(x + 3) = 0  →  x = 3  or  x = −3"),
    ]),
    ("Common factor", "العامل المشترك", "Facteur commun", "228", [
        T("6x³ + 9x² = 3x²(2x + 3). Check by distributing: 3x²·2x = 6x³ and 3x²·3 = 9x². The check is not decoration; it discovers a missing factor or a wrong sign.",
          "6x³ + 9x² = 3x²(2x + 3). نتحقق بإعادة التوزيع: 3x²·2x = 6x³ و3x²·3 = 9x². التحقق ليس زينة بل وسيلة لاكتشاف عامل ناقص أو إشارة خاطئة.",
          "Vérifie en développant."),
        F("6x³ + 9x² = 3x²(2x + 3)"),
    ]),
    ("Error detective", "المحقق", "Détective", "229", [
        T("A student wrote (x + 2)² = x² + 4. He forgot the middle term. We rebuild the meaning: (x + 2)² = (x + 2)(x + 2) = x² + 4x + 4.",
          "كتب طالب (x + 2)² = x² + 4. نسي الحد الأوسط. نعيد المعنى: (x + 2)² = (x + 2)(x + 2) = x² + 4x + 4.",
          "x² + 4x + 4."),
        F("(x + 2)(x + 2) = x² + 4x + 4"),
    ]),
    ("Strategy and challenge", "الاستراتيجية والتحدي", "Stratégie et défi", "229", [
        T("Simplify → expand. Solve a product-like equation → factorize. Compare degree or coefficients → organized expanded form. Never change form without a purpose. Challenge: P(x) = x² + x − 6. Two numbers with product −6 and sum 1: 3 and −2. So P(x) = (x + 3)(x − 2); zeros x = −3 and x = 2. Re-expand to check.",
          "إذا طُلب التبسيط ← ننشر. حلّ معادلة جداء ← نحلّل. مقارنة الدرجة أو المعاملات ← الشكل المنشور المرتّب. لا نغيّر الشكل بلا هدف. تحدٍّ: P(x) = x² + x − 6. عددان جداؤهما −6 ومجموعهما 1: هما 3 و−2. إذن P(x) = (x + 3)(x − 2) والأصفار x = −3 وx = 2. نعيد النشر للتحقق.",
          "(x+3)(x−2)."),
        F("x² + x − 6 = (x + 3)(x − 2)"),
        F("(x + 3)(x − 2) = x² − 2x + 3x − 6 = x² + x − 6"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Polynomial → non-negative integer powers. Degree → highest power with nonzero coefficient. Equivalent forms → same polynomial, different usefulness. Best habit: transform, then verify.",
          "كثير الحدود ← قوى صحيحة غير سالبة. الدرجة ← أعلى قوة بمعامل غير معدوم. الأشكال المتكافئة ← الكثير نفسه بفائدة مختلفة. العادة الأفضل: نحوّل ثم نتحقق.",
          "Transformer puis vérifier."),
    ]),
]

EXERCISES = [
    EX("1", "", st("Degree of 3x³ − 2x + 7.", "درجة 3x³ − 2x + 7.", "Degré."), [F("3")]),
    EX("2", "", st("Solve x² − 9 = 0.", "حلّ x² − 9 = 0.", "Résous x² − 9 = 0."), [F("(x−3)(x+3) = 0      x = ±3")]),
    EX("3", "", st("Factor 6x³ + 9x² and check.", "حلّل 6x³ + 9x² وتحقق.", "Factorise."), [F("3x²(2x + 3)")]),
    EX("4", "", st("Error detective: (x + 2)² = x² + 4.", "المحقق: (x + 2)² = x² + 4.", "Détective."), [F("x² + 4x + 4")]),
    EX("5", "", st("Factor x² + x − 6 and find its zeros.", "حلّل x² + x − 6 وأوجد أصفاره.", "Factorise x² + x − 6."), [F("(x + 3)(x − 2)      x = −3, 2")]),
]
