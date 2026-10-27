"""Grade 10 Mathematics — Lines in the coordinate plane."""
from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.lessons.g10_math_en_012 import plane

LESSON_ID = "G10-MATH-EN-013"
GRADE = 10
SUBJECT = "math"
TITLES = {"en": "Lines in the coordinate plane", "ar": "المستقيمات في المستوي الإحداثي", "fr": "Droites dans le plan"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "Does A(3, 7) lie on y = 2x + 1?  2·3 + 1 = ?", "opts": ["7", "6", "5", "8"], "a": 0,
     "why": {"6": _w("2 × 3 = 6, then add 1.", "2 × 3 = 6 ثم نضيف 1.", "2 × 3 = 6 puis + 1."),
             "5": _w("That is 2·2 + 1.", "هذه 2·2 + 1.", "C'est 2·2 + 1."),
             "8": _w("Too big by one.", "زائدة بواحد.", "Trop grand de 1.")}, "ok": "7 = 7: A is on the line"},
    {"q": "C(2, 4) and y = 2x + 1: is C on the line?", "opts": ["No: 2·2 + 1 = 5", "Yes, it looks close", "Yes: 2·2 = 4", "Cannot tell"], "a": 0,
     "why": {"Yes, it looks close": _w("Appearance is not proof; substitute.", "المظهر ليس برهانًا؛ نعوّض.", "Remplace."),
             "Yes: 2·2 = 4": _w("Do not forget + 1.", "لا تنسَ + 1.", "N'oublie pas + 1."),
             "Cannot tell": _w("Substitution decides.", "التعويض يحسم.", "La substitution décide.")}, "ok": "5 ≠ 4"},
    {"q": "y = −3x + 2 and x = −2: y = ?", "opts": ["8", "−4", "−8", "4"], "a": 0,
     "why": {"−4": _w("−3·(−2) = +6, then + 2.", "−3·(−2) = +6 ثم + 2.", "−3·(−2) = +6."),
             "−8": _w("Minus times minus is plus.", "سالب في سالب موجب.", "Moins fois moins = plus."),
             "4": _w("−3·(−2) = 6, then 6 + 2.", "−3·(−2) = 6 ثم 6 + 2.", "6 + 2.")}, "ok": "(−2, 8)"},
]

THEORY = [
    ("A line is a set of points", "المستقيم مجموعة نقاط", "Une droite est un ensemble de points", "135", [
        T("Hello! A straight line is a set of points, and each point on it passes the same test. For y = 2x + 1 a point belongs to the line only if its coordinates make the equation true. Choose x = 0: y = 1, so (0, 1). Choose x = 2: y = 5, so (2, 5). Two points are enough to draw the line; then we return to the equation to check.",
          "مرحبًا! المستقيم مجموعة نقاط وكل نقطة عليه تجتاز الاختبار نفسه. في y = 2x + 1 تنتمي النقطة إلى المستقيم فقط إذا جعلت إحداثياتها المعادلة صحيحة. نأخذ x = 0 فنجد y = 1 أي (0, 1). ونأخذ x = 2 فنجد y = 5 أي (2, 5). نقطتان تكفيان لرسم المستقيم ثم نعود إلى المعادلة لنتحقق.",
          "y = 2x + 1 : (0,1) et (2,5)."),
        plane({"P": (0, 1), "Q": (2, 3)}, line=((-2, -3), (2, 5)), rng=5),
        F("x = 0 → y = 1      x = 2 → y = 5"),
    ]),
    ("Point-on-line test", "اختبار الانتماء إلى المستقيم", "Le point est-il sur la droite ?", "135", [
        T("Does A(3, 7) lie on y = 2x + 1? Substitute x = 3: 2 × 3 + 1 = 7, equal to y, so yes. Does B(3, 6) lie on it? 2 × 3 + 1 = 7, not 6, so no. A small visual difference does not change the algebraic verdict.",
          "هل A(3, 7) على y = 2x + 1؟ نعوّض x = 3: 2 × 3 + 1 = 7 وهو y المعطى فنعم. وهل B(3, 6) عليه؟ 2 × 3 + 1 = 7 لا 6 فلا. والفرق البصري الصغير لا يغيّر الحكم الجبري.",
          "Substituer : 2×3+1 = 7."),
        F("2 × 3 + 1 = 7  ✓ A(3, 7)      7 ≠ 6  ✗ B(3, 6)"),
    ]),
    ("Build a table before drawing", "نبني جدولًا قبل الرسم", "Tableau avant le tracé", "136", [
        T("To draw a line, make a small table of x values, compute y, then plot. Algebra produces the points; the drawing only represents them. Never pick points on a picture and then force the equation on them.",
          "لرسم مستقيم نصنع جدولًا صغيرًا لقيم x ونحسب y ثم نعيّن النقط. الجبر ينتج النقط والرسم يمثّلها. ولا نختار نقطًا من الرسم ثم نُجبر المعادلة عليها.",
          "L'algèbre produit les points."),
        F("x = −1 → y = −1      x = 0 → y = 1      x = 1 → y = 3"),
    ]),
    ("Find a point with a given x", "نقطة بإحداثية أولى معطاة", "Un point d'abscisse donnée", "136", [
        T("On y = −3x + 2 find the point with first coordinate −2. Substitute x = −2: y = −3 × (−2) + 2 = 6 + 2 = 8. The point is (−2, 8). Check: 8 = 8.",
          "على y = −3x + 2 أوجد النقطة التي إحداثيتها الأولى −2. نعوّض x = −2: y = −3 × (−2) + 2 = 6 + 2 = 8. النقطة (−2, 8). نتحقق: 8 = 8.",
          "x = −2 donne y = 8."),
        F("−3 × (−2) + 2 = 8"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("A line equation is a membership rule. Test a point by substituting. A drawing is never proof.", "معادلة المستقيم قاعدة انتماء. نختبر النقطة بالتعويض. والرسم ليس برهانًا أبدًا.", "L'équation est une règle d'appartenance."),
        F("point on line ⇔ coordinates satisfy the equation"),
    ]),
]

EXERCISES = [
    EX("1", "", st("Does A(3, 7) lie on y = 2x + 1?", "هل A(3, 7) على y = 2x + 1؟", "A(3,7) est-il sur y = 2x + 1 ?"), [F("2 × 3 + 1 = 7  ✓")]),
    EX("2", "", st("Does B(3, 6) lie on it?", "هل B(3, 6) عليه؟", "B(3,6) ?"), [F("2 × 3 + 1 = 7 ≠ 6  ✗")]),
    EX("3", "", st("Error detective: C(2, 4) \"lies on y = 2x + 1 because it looks on the line\".", "المحقق: «C(2, 4) على y = 2x + 1 لأنها تبدو على المستقيم».", "Détective : C(2,4) semble sur la droite."), [F("2 × 2 + 1 = 5 ≠ 4"), T("The drawing is inaccurate or the point misplaced; the equation checks.", "الرسم غير دقيق أو النقطة في غير موضعها؛ المعادلة هي التحقق.", "L'équation vérifie.")]),
    EX("4", "", st("On y = −3x + 2 find the point with first coordinate −2.", "على y = −3x + 2 أوجد النقطة ذات الإحداثية الأولى −2.", "Point d'abscisse −2 sur y = −3x + 2."), [F("y = −3 × (−2) + 2 = 8      (−2, 8)")]),
    EX("5", "", st("Explain why looking on the line is not enough; then build and test your own point.", "اشرح لماذا لا يكفي أن تبدو النقطة على المستقيم ثم ابنِ نقطتك واختبرها.", "Pourquoi l'apparence ne suffit pas ?"), [T("Choose x, compute y, then test by substituting again.", "نختار x ونحسب y ثم نختبر بالتعويض من جديد.", "Choisis x, calcule y, vérifie.")]),
]
