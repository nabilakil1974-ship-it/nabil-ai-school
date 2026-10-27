"""Grade 10 Mathematics — Basic functions."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G10-MATH-EN-020"
GRADE = 10
SUBJECT = "math"
TITLES = {"en": "Basic functions", "ar": "الدوال المرجعية", "fr": "Fonctions de référence"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "f(x) = x². f(−2) = ?", "opts": ["4", "−4", "2", "−2"], "a": 0,
     "why": {"−4": _w("(−2)² = 4: brackets.", "(−2)² = 4: الأقواس.", "(−2)² = 4."),
             "2": _w("Square the input.", "نربّع المدخل.", "Carré."),
             "−2": _w("Square the input.", "نربّع المدخل.", "Carré.")}, "ok": "4"},
    {"q": "For f(x) = x², f(−3) and f(3) are …", "opts": ["equal (both 9)", "opposite", "0", "3 and −3"], "a": 0,
     "why": {"opposite": _w("(−3)² = 3² = 9.", "(−3)² = 3² = 9.", "Égaux."),
             "0": _w("Both equal 9.", "كلاهما 9.", "9."),
             "3 and −3": _w("Those are inputs, not outputs.", "هذه مدخلات.", "Entrées.")}, "ok": "symmetry"},
    {"q": "g(x) = 1/x. Which input is forbidden?", "opts": ["0", "1", "−1", "2"], "a": 0,
     "why": {"1": _w("1/1 = 1 is fine.", "1/1 = 1 مقبول.", "OK."),
             "−1": _w("−1/1... 1/(−1) = −1 is fine.", "1/(−1) = −1 مقبول.", "OK."),
             "2": _w("1/2 is fine.", "1/2 مقبول.", "OK.")}, "ok": "x ≠ 0"},
]

THEORY = [
    ("Reference models", "نماذج مرجعية", "Modèles de référence", "205", [
        T("Hello! Basic functions are reference shapes we will return to later. I do not want you to memorise a picture. I want you to connect the rule to the domain, to sample values and to the graph.",
          "مرحبًا! الدوال المرجعية أشكال سنرجع إليها لاحقًا. لا أريدك أن تحفظ الرسم كصورة، أريدك أن تربط القاعدة بالمجال وبقيم نموذجية وبشكل التمثيل البياني.",
          "Règle + domaine + valeurs + graphe."),
    ]),
    ("Build a graph from values", "نبني الرسم من القيم", "Construire le graphe", "205", [
        T("For each function: start from the rule, choose inputs inside the domain, compute outputs, plot the points with the right scale, then look for a pattern. The graph is a result of the values, not a picture copied from the book.",
          "لكل دالة: نبدأ من القاعدة، نختار مدخلات داخل المجال، نحسب المخرجات، نضع النقاط بالسلّم الصحيح ثم نبحث عن النمط. الرسم نتيجة للقيم لا صورة منقولة من الكتاب.",
          "Le graphe vient des valeurs."),
    ]),
    ("The square function", "دالة المربع", "La fonction carré", "206", [
        T("f(x) = x²: f(−2) = 4, f(−1) = 1, f(0) = 0, f(1) = 1, f(2) = 4. Opposite inputs give the same output: a symmetry that the table itself supports, not only the eye.",
          "f(x) = x²: f(−2) = 4 وf(−1) = 1 وf(0) = 0 وf(1) = 1 وf(2) = 4. المدخلان المتعاكسان يعطيان المخرج نفسه: تناظر يدعمه الجدول نفسه لا النظر وحده.",
          "Symétrie des valeurs."),
        F("x:  −2  −1  0  1  2"),
        F("x²:  4   1  0  1  4"),
    ]),
    ("Domain habit", "عادة المجال", "Habitude du domaine", "206", [
        T("When the rule has a denominator, ask at once where it equals zero and exclude those inputs before plotting or substituting. For 1/x, x = 0 is forbidden. A graph never lets us ignore a domain restriction.",
          "عندما يحتوي القانون على مقام نسأل فورًا أين يساوي صفرًا ونستبعد هذه المدخلات قبل الرسم أو التعويض. في 1/x القيمة x = 0 ممنوعة. الرسم لا يسمح بتجاهل قيود المجال.",
          "x ≠ 0 pour 1/x."),
        F("g(x) = 1/x      x ≠ 0"),
    ]),
    ("Absolute value", "القيمة المطلقة", "Valeur absolue", "207", [
        T("When |x| appears, remember the lesson on distance. We can build sample values from the meaning of absolute value, not only memorise a shape.",
          "عندما يظهر |x| نتذكر درس المسافة. نستطيع بناء قيم نموذجية من معنى القيمة المطلقة بدل حفظ الشكل فقط.",
          "|x| = distance à 0."),
        F("|−3| = 3      |0| = 0      |3| = 3"),
    ]),
    ("Error detective", "المحقق", "Détective", "207", [
        T("A student joins points across a forbidden input as if the function were defined there. First question: is this x inside the domain? If not, the drawing has no right to invent a value. The domain rules the graph.",
          "وصل طالب النقاط عبر مدخل ممنوع كأن الدالة معرّفة هناك. السؤال الأول: هل هذا x داخل المجال؟ إن لم يكن فلا يحق للرسم أن يخترع قيمة. المجال يحكم الرسم.",
          "Le domaine gouverne le graphe."),
    ]),
    ("Challenge", "تحدٍّ", "Défi", "208", [
        T("For f(x) = x², compare f(−3) and f(3). (−3)² = 9 and 3² = 9: equal. Why? Squaring opposite numbers removes the sign.",
          "لتكن f(x) = x²، قارن f(−3) وf(3). (−3)² = 9 و3² = 9 فهما متساويان. لماذا؟ لأن تربيع عددين متعاكسين يزيل الإشارة.",
          "(−3)² = 3² = 9."),
        F("(−3)² = 9      3² = 9"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Basic function = rule + domain + values + graph. Build from verified points. Respect domain gaps. Understand the shape; do not memorise it blindly.",
          "دالة مرجعية = قاعدة + مجال + قيم + رسم. نبني من نقاط محققة. نحترم فجوات المجال. نفهم الشكل ولا نحفظه بعمى.",
          "Comprendre la forme."),
    ]),
]

EXERCISES = [
    EX("1", "", st("Fill the table for f(x) = x² at x = −2…2.", "أكمل جدول f(x) = x² عند x = −2…2.", "Table de x²."), [F("4  1  0  1  4")]),
    EX("2", "", st("Which input is forbidden for 1/x?", "أي مدخل ممنوع للدالة 1/x؟", "Valeur interdite."), [F("x = 0")]),
    EX("3", "", st("Compare f(−3) and f(3) for x².", "قارن f(−3) وf(3) للدالة x².", "Compare."), [F("(−3)² = 9 = 3²")]),
    EX("4", "", st("Error detective: joining points across x = 0 for 1/x.", "المحقق: وصل النقاط عبر x = 0 للدالة 1/x.", "Détective."), [T("The function is not defined at 0.", "الدالة غير معرّفة عند 0.", "Non définie en 0.")]),
]
