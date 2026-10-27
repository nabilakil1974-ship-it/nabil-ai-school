"""Grade 10 Mathematics — Linear systems."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G10-MATH-EN-018"
GRADE = 10
SUBJECT = "math"
TITLES = {"en": "Linear systems", "ar": "جمل المعادلات الخطية", "fr": "Systèmes linéaires"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "x + y = 7 and x − y = 1. Adding them gives 2x = ?", "opts": ["8", "6", "7", "1"], "a": 0,
     "why": {"6": _w("7 + 1 = 8.", "7 + 1 = 8.", "7 + 1 = 8."),
             "7": _w("Add both right sides: 7 + 1.", "نجمع الطرفين الأيمنين: 7 + 1.", "7 + 1."),
             "1": _w("Add both right sides: 7 + 1.", "نجمع الطرفين الأيمنين: 7 + 1.", "7 + 1.")}, "ok": "2x = 8, x = 4"},
    {"q": "With x = 4 in x + y = 7, y = ?", "opts": ["3", "11", "4", "−3"], "a": 0,
     "why": {"11": _w("Subtract: 7 − 4.", "نطرح: 7 − 4.", "7 − 4."),
             "4": _w("That is x.", "هذا x.", "C'est x."),
             "−3": _w("7 − 4 = +3.", "7 − 4 = +3.", "+3.")}, "ok": "(4, 3)"},
    {"q": "2x + y = 9 and x − y = 0. Solution?", "opts": ["(3, 3)", "(9, 0)", "(4, 1)", "(3, 0)"], "a": 0,
     "why": {"(9, 0)": _w("x = y from the second.", "من الثانية x = y.", "x = y."),
             "(4, 1)": _w("Check x − y = 0.", "تحقق من x − y = 0.", "Vérifie x − y = 0."),
             "(3, 0)": _w("x = y, so y = 3.", "x = y إذن y = 3.", "y = 3.")}, "ok": "x = y = 3"},
]

THEORY = [
    ("Together", "معًا", "Ensemble", "183", [
        T("Hello! A system does not ask for a solution of each equation alone. It asks for a pair that satisfies both equations together. The word “together” is the key to this lesson.",
          "مرحبًا! الجملة لا تبحث عن حل لكل معادلة منفردة، بل عن زوج يحقق المعادلتين معًا. كلمة «معًا» هي مفتاح الدرس.",
          "Un couple qui vérifie les deux équations."),
    ]),
    ("Choosing a method", "اختيار الطريقة", "Choisir la méthode", "183", [
        T("For x + y = 7 and x − y = 1 we can write x = 7 − y from the first and substitute into the second, or eliminate. Either method keeps the system itself unchanged. Look at the coefficients: if a variable is easy to isolate, substitution; if cancellation is close, elimination.",
          "في x + y = 7 وx − y = 1 يمكن أن نكتب x = 7 − y من الأولى ونعوّض في الثانية، أو نستعمل الحذف. المهم أن الطريقة تحافظ على الجملة نفسها. ننظر إلى المعاملات: إذا سهل عزل متغير نعوّض، وإذا كان الحذف قريبًا نحذف.",
          "Substitution ou élimination selon la structure."),
    ]),
    ("Elimination example", "مثال بالحذف", "Exemple par élimination", "184", [
        T("x + y = 7 and x − y = 1. Adding the equations makes y disappear: 2x = 8, so x = 4. Substitute into the first: 4 + y = 7, so y = 3.",
          "x + y = 7 وx − y = 1. بجمع المعادلتين يختفي y: 2x = 8 إذن x = 4. نعوّض في الأولى: 4 + y = 7 إذن y = 3.",
          "x = 4, y = 3."),
        F("(x + y) + (x − y) = 7 + 1  →  2x = 8  →  x = 4"),
        F("4 + y = 7  →  y = 3"),
        T("The check is not in one equation only: 4 + 3 = 7 and 4 − 3 = 1. So (4, 3) is a common solution.",
          "التحقق ليس في معادلة واحدة فقط: 4 + 3 = 7 و4 − 3 = 1. إذن (4, 3) حل مشترك.",
          "Vérifie les deux."),
        F("4 + 3 = 7      4 − 3 = 1"),
    ]),
    ("Geometric meaning", "المعنى الهندسي", "Sens géométrique", "184", [
        T("When the two equations represent lines, the common solution is the point that lies on both. Algebra and the graph must agree.",
          "عندما تمثّل المعادلتان مستقيمين فالحل المشترك هو النقطة التي تقع عليهما معًا. ويجب أن يتفق الجبر مع الرسم.",
          "Le point d'intersection."),
    ]),
    ("Error detective", "المحقق", "Détective", "185", [
        T("A student finds x = 4 and stops. A system with two unknowns needs a complete pair: go back to find y, then check in every equation.",
          "وجد طالب x = 4 ثم توقف. جملة بمجهولين تحتاج إلى زوج كامل: نرجع لإيجاد y ثم نتحقق في كل المعادلات.",
          "Il faut le couple complet."),
    ]),
    ("Challenge", "تحدٍّ", "Défi", "185", [
        T("2x + y = 9 and x − y = 0. From the second, x = y. Substitute: 2x + x = 9, so 3x = 9, x = 3 and y = 3. Check both equations before announcing the solution.",
          "2x + y = 9 وx − y = 0. من الثانية x = y. نعوّض: 2x + x = 9 إذن 3x = 9 وx = 3 وy = 3. نتحقق في المعادلتين قبل إعلان الحل.",
          "(3, 3)."),
        F("3x = 9  →  x = y = 3"),
        F("2 × 3 + 3 = 9      3 − 3 = 0"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("System → common solution. Choose the method from the structure. Find the whole pair. Verify in every original equation.",
          "جملة ← حل مشترك. نختار الطريقة من البنية. نجد الزوج كاملًا. ونتحقق في كل المعادلات الأصلية.",
          "Couple complet, vérifié."),
    ]),
]

EXERCISES = [
    EX("1", "", st("Solve x + y = 7, x − y = 1.", "حلّ x + y = 7 وx − y = 1.", "Résous le système."), [F("2x = 8      x = 4      y = 3")]),
    EX("2", "", st("Verify (4, 3) in both equations.", "تحقق من (4, 3) في المعادلتين.", "Vérifie (4,3)."), [F("4 + 3 = 7      4 − 3 = 1")]),
    EX("3", "", st("Error detective: x = 4 and stop.", "المحقق: x = 4 ثم التوقف.", "Détective."), [T("We still need y.", "ما زال ينقصنا y.", "Il manque y.")]),
    EX("4", "", st("Solve 2x + y = 9, x − y = 0.", "حلّ 2x + y = 9 وx − y = 0.", "Résous."), [F("x = y      3x = 9      (3, 3)")]),
]
