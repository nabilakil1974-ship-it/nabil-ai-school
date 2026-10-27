"""Grade 10 Mathematics — Cumulative review: Algebra and functions (supplementary)."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G10-MATH-EN-028"
GRADE = 10
SUBJECT = "math"
TITLES = {"en": "Cumulative review: Algebra and functions", "ar": "مراجعة شاملة: الجبر والدوال", "fr": "Révision : algèbre et fonctions"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "−3x ≤ 9 → x ? −3", "opts": ["≥", "≤", "<", ">"], "a": 0,
     "why": {"≤": _w("Dividing by −3 reverses the sign.", "القسمة على −3 تعكس الرمز.", "On inverse."),
             "<": _w("Keep the equality and reverse.", "نبقي المساواة ونعكس.", "Inverse."),
             ">": _w("Keep the equality.", "نبقي المساواة.", "Garde =.")}, "ok": "x ≥ −3"},
    {"q": "x + y = 7 and x − y = 1: (x, y) = ?", "opts": ["(4, 3)", "(3, 4)", "(7, 1)", "(8, 0)"], "a": 0,
     "why": {"(3, 4)": _w("2x = 8, so x = 4.", "2x = 8 إذن x = 4.", "x = 4."),
             "(7, 1)": _w("Check both equations.", "تحقق من المعادلتين.", "Vérifie."),
             "(8, 0)": _w("Check both equations.", "تحقق من المعادلتين.", "Vérifie.")}, "ok": "(4, 3)"},
    {"q": "x² + x − 6 = 0 → x = ?", "opts": ["−3 or 2", "3 or −2", "6 or −1", "1 or −6"], "a": 0,
     "why": {"3 or −2": _w("(x + 3)(x − 2) = 0.", "(x + 3)(x − 2) = 0.", "(x+3)(x−2)."),
             "6 or −1": _w("Product −6 and sum +1: 3 and −2.", "جداء −6 ومجموع 1: 3 و−2.", "3 et −2."),
             "1 or −6": _w("Re-expand to check.", "ننشر للتحقق.", "Développe.")}, "ok": "x = −3 or 2"},
]

THEORY = [
    ("One toolbox, many tools", "صندوق أدوات واحد", "Une boîte à outils", "", [
        T("Hello! This is not a quick replay of every lesson. I will link the ideas so you know when to use each tool. Before any question ask: is it numerical? an equation? an inequality? a function? a graph? a polynomial? Choosing the right language is half the solution.",
          "مرحبًا! هذه ليست إعادة سريعة لكل الدروس. سأربط الأفكار لتعرف متى تستعمل كل أداة. قبل أي سؤال اسأل: هل هو عددي؟ معادلة؟ متراجحة؟ دالة؟ رسم؟ كثير حدود؟ اختيار اللغة الصحيحة نصف الحل.",
          "Choisir le bon langage."),
    ]),
    ("Powers, absolute value, approximation", "القوى والقيمة المطلقة والتقريب", "Puissances, valeur absolue", "", [
        T("Check that the expression allows a power rule before applying it: add exponents only when multiplying powers of the same base. Absolute value is a distance from zero, so it is never negative. An approximation is a close value, not an exact equality.",
          "نتحقق أن شكل التعبير يسمح بقاعدة القوى قبل تطبيقها: نجمع الأسس فقط عند ضرب قوى لها الأساس نفسه. القيمة المطلقة مسافة عن الصفر فلا تكون سالبة. والتقريب قيمة قريبة لا مساواة دقيقة.",
          "|x| ≥ 0."),
        F("a^m × a^n = a^(m+n)      |−5| = 5"),
    ]),
    ("Equations, inequalities, systems", "المعادلات والمتراجحات والجمل", "Équations, inéquations, systèmes", "", [
        T("In an equation keep equivalence. In an inequality watch the operation that may reverse the order, then state the solution set and check the boundary. For a system, the solution must satisfy both equations together; choose substitution or elimination to reduce complexity, then substitute back into the originals.",
          "في المعادلة نحافظ على التكافؤ. وفي المتراجحة ننتبه للعملية التي قد تعكس الترتيب ثم نكتب مجموعة الحلول ونتحقق من الحد. وفي الجملة يجب أن يحقق الحل المعادلتين معًا؛ نختار التعويض أو الحذف بما يقلل التعقيد ثم نعوّض في الأصل.",
          "Vérifier dans les originaux."),
        F("−3x ≤ 9  →  x ≥ −3"),
        F("x + y = 7,  x − y = 1  →  (4, 3)"),
    ]),
    ("Functions and graphs", "الدوال والرسوم", "Fonctions et graphes", "", [
        T("f(x) is not f multiplied by x; it is the output linked to the input x. Read the domain first, then values, then graph behaviour. Graphically: f(x) = g(x) means the abscissas of intersections; f(x) > g(x) means where the graph of f is higher. Check scale and endpoints, and never turn an approximate reading into an exact answer.",
          "f(x) ليست ضرب f في x، بل المخرج المرتبط بالمدخل x. نقرأ المجال أولًا ثم القيم ثم سلوك الرسم. بيانيًا: f(x) = g(x) تعني فواصل التقاطع، وf(x) > g(x) تعني حيث منحنى f أعلى. نتحقق من السلّم والنهايات ولا نحوّل قراءة تقريبية إلى جواب دقيق.",
          "f(x) : sortie de x."),
    ]),
    ("Polynomials", "كثيرات الحدود", "Polynômes", "", [
        T("Expanded and factorized forms are not enemies; they are two tools. The degree shows easily in an organized expanded form, while zeros appear faster in a factorized form.",
          "الشكل المنشور والمحلَّل ليسا خصمين بل أداتان. تظهر الدرجة بسهولة في الشكل المنشور المرتّب وتظهر الأصفار أسرع في الشكل المحلَّل.",
          "Développée / factorisée."),
    ]),
    ("Mixed challenge", "تحدٍّ مختلط", "Défi mixte", "", [
        T("P(x) = x² + x − 6. Evaluate P(2) = 4 + 2 − 6 = 0. Factorize: (x + 3)(x − 2). Solve P(x) = 0: x = −3 or x = 2. Interpret graphically: the curve crosses the x-axis at −3 and 2. The topics are not separate islands.",
          "P(x) = x² + x − 6. نحسب P(2) = 4 + 2 − 6 = 0. نحلّل: (x + 3)(x − 2). نحلّ P(x) = 0: x = −3 أو x = 2. نفسّر بيانيًا: يقطع المنحنى محور الفواصل عند −3 و2. الموضوعات ليست جزرًا منفصلة.",
          "Trois outils, un résultat."),
        F("(x + 3)(x − 2) = 0  →  x = −3  or  x = 2"),
    ]),
    ("Mastery check", "فحص الإتقان", "Vérifier la maîtrise", "", [
        T("Choose the method and say why. Solve step by step. Verify with a second method when possible. Explain the result in a sentence, not only in symbols.",
          "نختار الطريقة ونفسّر لماذا. نحلّ خطوة خطوة. نتحقق بطريقة ثانية إن أمكن. نشرح النتيجة بجملة لا بالرموز فقط.",
          "Choisir, résoudre, vérifier, expliquer."),
    ]),
]

EXERCISES = [
    EX("1", "", st("Solve −3x ≤ 9.", "حلّ −3x ≤ 9.", "Résous −3x ≤ 9."), [F("x ≥ −3")]),
    EX("2", "", st("Solve x + y = 7, x − y = 1.", "حلّ x + y = 7 وx − y = 1.", "Résous."), [F("(4, 3)")]),
    EX("3", "", st("Factorize x² + x − 6 and solve it.", "حلّل x² + x − 6 وحلّه.", "Factorise."), [F("(x+3)(x−2) = 0      x = −3 or 2")]),
    EX("4", "", st("f(x) = 3x − 2: find f(x) = 13.", "f(x) = 3x − 2: حلّ f(x) = 13.", "Résous f(x) = 13."), [F("x = 5")]),
]
