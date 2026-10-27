"""Grade 11 Mathematics — Self evaluation: antiderivatives and complex numbers."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G11-MATH-EN-030"
GRADE = 11
SUBJECT = "math"
TITLES = {"en": "Self evaluation — answers and hints", "ar": "التقييم الذاتي — إجابات وتلميحات", "fr": "Auto-évaluation — réponses et indices"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "A primitive of x⁴ is …", "opts": ["x⁵/5 + C", "x⁴/4 + C", "4x³ + C", "x⁵ + C"], "a": 0,
     "why": {"x⁴/4 + C": _w("Differentiate: you get x³, not x⁴.", "اشتق: تحصل على x³ لا x⁴.", "Dérive : x³."),
             "4x³ + C": _w("That is a derivative.", "هذه مشتقة.", "C'est une dérivée."),
             "x⁵ + C": _w("Divide by the new exponent 5.", "نقسم على الأس الجديد 5.", "Divise par 5.")}, "ok": "x⁵/5 + C"},
    {"q": "(1 + i)² = ?", "opts": ["2i", "2 + 2i", "1 + i", "2"], "a": 0,
     "why": {"2 + 2i": _w("1 + 2i + i² = 2i because i² = −1.", "1 + 2i + i² = 2i لأن i² = −1.", "i² = −1."),
             "1 + i": _w("Expand fully.", "ننشر كاملًا.", "Développe."),
             "2": _w("Do not drop the middle term 2i.", "لا نحذف الحد 2i.", "Garde 2i.")}, "ok": "2i"},
    {"q": "|3 + 4i| = ?", "opts": ["5", "7", "25", "−5"], "a": 0,
     "why": {"7": _w("√(3² + 4²), not 3 + 4.", "√(3² + 4²) لا 3 + 4.", "Racine."),
             "25": _w("Take the square root.", "نأخذ الجذر.", "Racine."),
             "−5": _w("A modulus is a distance: never negative.", "المعيار مسافة: لا يكون سالبًا.", "Jamais négatif.")}, "ok": "5"},
]

THEORY = [
    ("A smart self-evaluation", "تقييم ذاتي ذكي", "Auto-évaluation intelligente", "", [
        T("Hello! This unit is not a page of final answers. Each item follows the same path: question, hint 1, hint 2, strategy, worked solution, error detective, final check. Before seeing a solution, say which mathematical idea is needed first.",
          "مرحبًا! هذه الوحدة ليست صفحة أجوبة نهائية. كل مسألة تتبع المسار نفسه: السؤال، التلميح 1، التلميح 2، الاستراتيجية، الحل المفصّل، المحقق، والتحقق النهائي. قبل رؤية الحل قل ما الفكرة الرياضية المطلوبة أولًا.",
          "Question, indices, solution, vérification."),
        F("Hint 1: concept → Hint 2: structure → Hint 3: first step"),
    ]),
    ("Antiderivatives: reverse differentiation", "الأصيلة: عكس الاشتقاق", "Primitives", "", [
        T("Start with: which function gives this expression when differentiated? The aim is to reverse differentiation, not to memorise disconnected formulas. To check a proposed primitive F of f, compute F′ and compare: if F′(x) = f(x) it is correct.",
          "نبدأ بالسؤال: أي دالة تعطي هذا التعبير عند اشتقاقها؟ الهدف عكس الاشتقاق لا حفظ صيغ منفصلة. ولاختبار أصيلة مقترحة F للدالة f نحسب F′ ونقارن: إذا كانت F′(x) = f(x) فهي صحيحة.",
          "F′ = f."),
        F("∫ xⁿ dx = xⁿ⁺¹ / (n + 1) + C,   n ≠ −1"),
        F("∫ (1/x) dx = ln|x| + C"),
    ]),
    ("Error detectives: antiderivatives", "المحققون: الأصيلات", "Détectives : primitives", "", [
        T("Missing constant: when all antiderivatives are requested the complete family is F(x) + C. Power rule: the claim ∫x⁴ dx = x⁴/4 + C is exposed by differentiating, which gives x³. The correct primitive is x⁵/5 + C. The exception: for 1/x the power rule would divide by zero, so we use ln|x| + C. Initial condition: first find the family F₀ + C, then use F(a) = b to find C; never discard C before using the condition.",
          "الثابت المنسي: عند طلب كل الأصيلات فالعائلة الكاملة F(x) + C. قاعدة القوة: الادعاء ∫x⁴ dx = x⁴/4 + C ينكشف بالاشتقاق إذ نحصل على x³. والأصيلة الصحيحة x⁵/5 + C. الاستثناء: في 1/x ستقسم القاعدة على صفر فنستعمل ln|x| + C. الشرط الابتدائي: نجد العائلة F₀ + C أولًا ثم نستعمل F(a) = b لإيجاد C، ولا نهمل C قبل تطبيق الشرط.",
          "+ C, dérive pour vérifier."),
        F("(x⁵/5)′ = x⁴"),
    ]),
    ("Complex numbers: classify first", "الأعداد العقدية: نصنّف أولًا", "Complexes : classer", "", [
        T("Decide the task: algebraic calculation, conjugate, modulus, argument, trigonometric form, equation, geometric interpretation, or transformation. For algebra, reduce to a + ib using i² = −1. Powers of i follow the cycle i, −1, −i, 1; reduce the exponent modulo 4. If z = a + ib then z̄ = a − ib and z·z̄ = |z|². For division, multiply by the conjugate of the denominator. The modulus |a + ib| = √(a² + b²) is a distance, never negative.",
          "نحدد نوع المهمة: حساب جبري أو مرافق أو معيار أو عمدة أو صيغة مثلثية أو معادلة أو تفسير هندسي أو تحويل. في الجبر نختزل إلى a + ib باستعمال i² = −1. قوى i تتبع الدورة i و−1 و−i و1، فنختزل الأس بترديد 4. إذا كان z = a + ib فإن z̄ = a − ib وz·z̄ = |z|². وللقسمة نضرب في مرافق المقام. والمعيار |a + ib| = √(a² + b²) مسافة فلا يكون سالبًا.",
          "i² = −1."),
        F("i, −1, −i, 1 (period 4)"),
        F("|a + ib| = √(a² + b²)"),
    ]),
    ("Argument, trigonometric form, De Moivre", "العمدة والصيغة المثلثية ودوموافر", "Argument, forme trigonométrique", "", [
        T("Do not find the quadrant from tan θ = b/a alone: inspect the signs of Re(z) and Im(z), then choose θ modulo 2π. Compute r = |z|, cos θ = a/r, sin θ = b/r, then z = r(cos θ + i sin θ), and rebuild the real and imaginary parts as a check. De Moivre: [r(cos θ + i sin θ)]ⁿ = rⁿ[cos nθ + i sin nθ]. Do not forget to raise the modulus to n.",
          "لا نحدد الربع من tan θ = b/a وحدها: نفحص إشارتي Re(z) وIm(z) ثم نختار θ بترديد 2π. نحسب r = |z| وcos θ = a/r وsin θ = b/r ثم z = r(cos θ + i sin θ) ونعيد بناء الجزءين الحقيقي والتخيلي للتحقق. دوموافر: [r(cos θ + i sin θ)]ⁿ = rⁿ[cos nθ + i sin nθ]. لا تنسَ رفع المعيار إلى القوة n.",
          "rⁿ et nθ."),
        F("[r(cos θ + i sin θ)]ⁿ = rⁿ(cos nθ + i sin nθ)"),
    ]),
    ("Quadratics and geometry in ℂ", "المعادلات والهندسة في ℂ", "Équations et géométrie", "", [
        T("For az² + bz + c = 0 compute Δ = b² − 4ac. In ℂ a negative discriminant does not stop us: √(−k) = i√k, then apply the quadratic formula. Geometry: affix of AB is z_B − z_A and AB = |z_B − z_A|, so |z − z_A| = r is the circle centred at A with radius r (r > 0). Also z′ = iz keeps the modulus and turns the direction by π/2: a rotation about O.",
          "في المعادلة az² + bz + c = 0 نحسب Δ = b² − 4ac. في ℂ المميّز السالب لا يوقفنا: √(−k) = i√k ثم نطبق قانون الجذور. هندسيًا: لاحقة AB هي z_B − z_A وAB = |z_B − z_A| فتمثل |z − z_A| = r الدائرة التي مركزها A ونصف قطرها r (r > 0). وz′ = iz يحفظ المعيار ويدير الاتجاه بزاوية π/2: دوران حول O.",
          "Cercle |z − zA| = r."),
        F("|z − z_A| = r"),
    ]),
    ("Mastery rule", "قاعدة الإتقان", "Règle de maîtrise", "", [
        T("After each item choose: sure, unsure, guessed. A correct guess does not count as mastery; you get a nearby transfer question. Mastery = correctness + reasoning + independent verification: understand, choose, solve, explain, verify.",
          "بعد كل مسألة اختر: متأكد أو غير متأكد أو خمّنت. التخمين الصحيح لا يُحتسب إتقانًا فتحصل على سؤال نقل قريب. الإتقان = الصحة + الاستدلال + التحقق المستقل: نفهم ونختار ونحلّ ونشرح ونتحقق.",
          "Comprendre, choisir, résoudre, expliquer, vérifier."),
    ]),
]

EXERCISES = [
    EX("1", "", st("Error detective: ∫x⁴ dx = x⁴/4 + C.", "المحقق: ∫x⁴ dx = x⁴/4 + C.", "Détective."), [F("(x⁴/4)′ = x³ ≠ x⁴"), F("∫x⁴ dx = x⁵/5 + C")]),
    EX("2", "", st("Error detective: (1 + i)² = 2 + 2i.", "المحقق: (1 + i)² = 2 + 2i.", "Détective."), [F("1 + 2i + i² = 2i")]),
    EX("3", "", st("Compute |3 + 4i|.", "احسب |3 + 4i|.", "Calcule |3 + 4i|."), [F("√(9 + 16) = 5")]),
    EX("4", "", st("Find i²⁰²⁶.", "أوجد i²⁰²⁶.", "Calcule i²⁰²⁶."), [T("2026 ≡ 2 (mod 4), so i²⁰²⁶ = i² = −1.", "2026 ≡ 2 (mod 4) إذن i²⁰²⁶ = i² = −1.", "= −1.")]),
]
