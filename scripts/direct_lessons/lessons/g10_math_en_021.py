"""Grade 10 Mathematics — Graphical solutions of equations and inequalities."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G10-MATH-EN-021"
GRADE = 10
SUBJECT = "math"
TITLES = {"en": "Graphical solutions of equations and inequalities", "ar": "الحل البياني للمعادلات والمتراجحات", "fr": "Résolution graphique d'équations et d'inéquations"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "f(x) = x + 1 and g(x) = 3 meet at x = ?", "opts": ["2", "3", "1", "4"], "a": 0,
     "why": {"3": _w("x + 1 = 3 gives x = 2.", "x + 1 = 3 تعطي x = 2.", "x = 2."),
             "1": _w("x + 1 = 3, subtract 1.", "نطرح 1.", "x = 2."),
             "4": _w("x + 1 = 3, not 3 + 1.", "x + 1 = 3.", "x = 2.")}, "ok": "x = 2"},
    {"q": "The graphs meet at x = −1 and x = 4. Solutions of f(x) = g(x)?", "opts": ["−1 and 4", "only 4", "only −1", "−1 to 4"], "a": 0,
     "why": {"only 4": _w("Every intersection counts.", "كل تقاطع يُحتسب.", "Tous."),
             "only −1": _w("Every intersection counts.", "كل تقاطع يُحتسب.", "Tous."),
             "−1 to 4": _w("That is for an inequality.", "هذا للمتراجحة.", "Pour une inéquation.")}, "ok": "x = −1 or 4"},
    {"q": "f(x) > g(x) is read where …", "opts": ["f is above g", "f is below g", "they meet", "f is zero"], "a": 0,
     "why": {"f is below g": _w("That is f < g.", "هذه f < g.", "f < g."),
             "they meet": _w("That is equality.", "هذه مساواة.", "Égalité."),
             "f is zero": _w("Not what it says.", "ليس المقصود.", "Non.")}, "ok": "above"},
]

THEORY = [
    ("Seeing the meaning", "نرى المعنى", "Voir le sens", "219", [
        T("Hello! Before saying \"solve graphically\", I want you to see the meaning. When I write f(x) = g(x), I look for the values of x that make the two heights equal. On the drawing: where do the curves meet? And f(x) > g(x) asks: where is the curve of f above the curve of g?",
          "مرحبًا! قبل أن أقول «حلّ بيانيًا» أريدك أن ترى المعنى. عندما أكتب f(x) = g(x) أبحث عن قيم x التي تجعل الارتفاعين متساويين. على الرسم: أين يلتقي المنحنيان؟ أما f(x) > g(x) فالسؤال: أين يكون منحنى f أعلى من منحنى g؟",
          "Égalité : intersection. f > g : f au-dessus."),
    ]),
    ("Full example", "مثال كامل", "Exemple complet", "219", [
        T("Take f(x) = x + 1 and g(x) = 3. The intersection satisfies x + 1 = 3, so x = 2. Graphically the line y = x + 1 meets y = 3 at abscissa 2. The drawing and the calculation tell the same story.",
          "لنأخذ f(x) = x + 1 وg(x) = 3. نقطة التقاطع تحقق x + 1 = 3 أي x = 2. بيانيًا يلتقي المستقيم y = x + 1 مع y = 3 عند الفاصلة 2. الرسم والحساب يرويان القصة نفسها.",
          "x = 2."),
        F("x + 1 = 3  →  x = 2"),
    ]),
    ("Equation: all intersections", "المعادلة: كل التقاطعات", "Équation : toutes les intersections", "220", [
        T("If the curves meet at x = −1 and x = 4, the solutions of f(x) = g(x) are −1 and 4: the abscissas of every intersection point.",
          "إذا التقى المنحنيان عند x = −1 وx = 4 فحلول f(x) = g(x) هي −1 و4، أي فواصل كل نقاط التقاطع.",
          "−1 et 4."),
    ]),
    ("Inequality: intervals", "المتراجحة: مجالات", "Inéquation : intervalles", "220", [
        T("For f(x) > g(x) the intersection points are not enough. We mark the regions where f is above g, then read the interval on the x-axis. At the endpoints we check > or ≥: equality enters only when the sign allows it.",
          "في f(x) > g(x) لا تكفي نقاط التقاطع. نحدد مناطق الرسم التي يكون فيها f فوق g ثم نقرأ المجال على محور x. عند النهايات نتحقق من > أو ≥: المساواة تدخل فقط إذا سمح الرمز.",
          "Bornes selon le signe."),
        F("f(x) > g(x)  ⇔  f above g"),
    ]),
    ("Check rule", "قاعدة التحقق", "Règle de vérification", "221", [
        T("Never read a graph without its scale and never forget endpoints. If the drawing is approximate, the graphical solution is approximate too: we do not turn an approximate reading into an exact value without proof.",
          "لا نقرأ الرسم دون سلّمه ولا ننسى النهايات. وإذا كان الرسم تقريبيًا فالحل البياني تقريبي أيضًا: لا نحوّل قراءة تقريبية إلى قيمة دقيقة دون دليل.",
          "Échelle et bornes."),
    ]),
    ("Error detective", "المحقق", "Détective", "221", [
        T("A student found one intersection and stopped, though the drawing shows a second. Scan the whole domain from left to right and look for every change in the order of the two curves.",
          "وجد طالب نقطة تقاطع واحدة وتوقف مع أن الرسم يُظهر ثانية. نمسح المجال كله من اليسار إلى اليمين ونبحث عن كل تغيّر في ترتيب المنحنيين.",
          "Balaye tout le domaine."),
    ]),
    ("Challenge", "تحدٍّ", "Défi", "222", [
        T("Picture y = x and y = x². Where are they equal? x² = x gives x(x − 1) = 0: x = 0 or x = 1. Where is x² > x? Predict from the picture, then verify: for x > 1 and for x < 0.",
          "تخيّل y = x وy = x². أين يتساويان؟ x² = x تعطي x(x − 1) = 0 إذن x = 0 أو x = 1. وأين x² > x؟ نتوقع من الرسم ثم نتحقق: عندما x > 1 وعندما x < 0.",
          "x = 0 ou 1."),
        F("x² = x  →  x(x − 1) = 0"),
        F("x² > x  ⇔  x < 0  or  x > 1"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Equation → abscissas of intersections. Inequality → intervals where one graph is above or below the other. Endpoints follow the sign. Check scale and domain, then confirm algebraically.",
          "المعادلة ← فواصل التقاطع. المتراجحة ← مجالات يكون فيها أحد الرسمين فوق الآخر أو تحته. النهايات تتبع الرمز. نتحقق من السلّم والمجال ثم نؤكد جبريًا.",
          "Graphique + algèbre."),
    ]),
]

EXERCISES = [
    EX("1", "", st("Solve x + 1 = 3 and read it on the graph.", "حلّ x + 1 = 3 واقرأه على الرسم.", "Résous x + 1 = 3."), [F("x = 2")]),
    EX("2", "", st("Curves meet at x = −1 and x = 4. Solve f(x) = g(x).", "يلتقي المنحنيان عند x = −1 وx = 4. حلّ f(x) = g(x).", "Résous f = g."), [F("x = −1  or  x = 4")]),
    EX("3", "", st("How do you read f(x) > g(x)?", "كيف تقرأ f(x) > g(x)؟", "Lecture de f > g."), [T("Where f is above g.", "حيث f فوق g.", "f au-dessus de g.")]),
    EX("4", "", st("Solve x² = x and x² > x.", "حلّ x² = x وx² > x.", "Résous."), [F("x = 0 or 1      x < 0 or x > 1")]),
]
