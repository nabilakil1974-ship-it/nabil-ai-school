"""Grade 10 Mathematics — Cumulative review: Coordinate geometry and vectors (supplementary)."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G10-MATH-EN-029"
GRADE = 10
SUBJECT = "math"
TITLES = {"en": "Cumulative review: Coordinate geometry and vectors", "ar": "مراجعة شاملة: الهندسة الإحداثية والمتجهات", "fr": "Révision : géométrie analytique et vecteurs"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "A(1, 2), B(4, 6): vector AB = ?", "opts": ["(3, 4)", "(−3, −4)", "(5, 8)", "(4, 3)"], "a": 0,
     "why": {"(−3, −4)": _w("That is BA. AB = terminal − initial.", "هذا BA. AB = النهاية − البداية.", "C'est BA."),
             "(5, 8)": _w("Subtract, do not add.", "نطرح لا نجمع.", "Soustrais."),
             "(4, 3)": _w("x first: 4 − 1 = 3.", "x أولًا: 4 − 1 = 3.", "x d'abord.")}, "ok": "(3, 4)"},
    {"q": "If AB = (3, 4), then BA = ?", "opts": ["(−3, −4)", "(3, 4)", "(4, 3)", "(0, 0)"], "a": 0,
     "why": {"(3, 4)": _w("Direction reverses.", "الاتجاه ينعكس.", "Inverse."),
             "(4, 3)": _w("Swapping is not reversing.", "التبديل ليس عكسًا.", "Non."),
             "(0, 0)": _w("Only AB + BA = 0.", "فقط AB + BA = 0.", "AB + BA = 0.")}, "ok": "(−3, −4)"},
    {"q": "(2, 1)·(1, −2) = ?", "opts": ["0", "4", "−4", "5"], "a": 0,
     "why": {"4": _w("2×1 + 1×(−2) = 0.", "2×1 + 1×(−2) = 0.", "= 0."),
             "−4": _w("2×1 + 1×(−2) = 0.", "2×1 + 1×(−2) = 0.", "= 0."),
             "5": _w("2×1 + 1×(−2) = 0.", "2×1 + 1×(−2) = 0.", "= 0.")}, "ok": "perpendicular"},
]

THEORY = [
    ("Translate both ways", "الترجمة في الاتجاهين", "Traduire dans les deux sens", "", [
        T("Hello! I want you to translate in both directions: from the figure to algebra, then from algebra to a geometric meaning. Calculation alone is not enough if you forget what the numbers represent.",
          "مرحبًا! أريدك أن تترجم في الاتجاهين: من الشكل إلى الجبر ثم من الجبر إلى معنى هندسي. الحساب وحده لا يكفي إذا نسيت ما تمثله الأرقام.",
          "Géométrie ⇄ algèbre."),
    ]),
    ("Points and coordinates", "النقاط والإحداثيات", "Points et coordonnées", "", [
        T("A point A(x, y) is not a pair of meaningless numbers. x gives the horizontal move and y the vertical move in the coordinate system. Before using coordinates, check the axes, the origin and the scale.",
          "النقطة A(x, y) ليست زوج أرقام بلا معنى. x يحدد الحركة الأفقية وy الحركة العمودية في جملة الإحداثيات. قبل استعمال الإحداثيات نتأكد من المحورين والمبدأ والسلّم.",
          "x : horizontal, y : vertical."),
    ]),
    ("Vectors", "المتجهات", "Vecteurs", "", [
        T("Vector AB is the displacement from A to B. In coordinates keep the direction: terminal minus initial. Example: A(1, 2), B(4, 6) gives AB = (3, 4). Check: from 1 to 4 we moved +3 horizontally, from 2 to 6 we moved +4 vertically.",
          "المتجه AB هو الانتقال من A إلى B. في الإحداثيات نحافظ على الاتجاه: النهاية ناقص البداية. مثال: A(1, 2) وB(4, 6) يعطي AB = (3, 4). نتحقق: من 1 إلى 4 تحركنا +3 أفقيًا ومن 2 إلى 6 تحركنا +4 عموديًا.",
          "AB = B − A."),
        F("AB = (4 − 1, 6 − 2) = (3, 4)"),
    ]),
    ("Error detective", "المحقق", "Détective", "", [
        T("A student computed AB in reverse order. Do not only fix the signs: say the movement aloud, “from A to B”. That shows why it must be terminal minus initial. And if AB = (3, 4), then BA = (−3, −4): swapping the points reverses the direction.",
          "حسب طالب AB بعكس الترتيب. لا نصلح الإشارات فقط بل ننطق الحركة: «من A إلى B». هذا يكشف لماذا يجب أن تكون النهاية ناقص البداية. وإذا كان AB = (3, 4) فإن BA = (−3, −4): تبديل النقطتين يعكس الاتجاه.",
          "BA = −AB."),
        F("BA = −AB = (−3, −4)"),
    ]),
    ("Operations, lines, scalar product", "العمليات والمستقيمات والجداء السلمي", "Opérations, droites, produit scalaire", "", [
        T("Adding vectors means composing displacements. To test whether a point is on a line, substitute its coordinates instead of trusting the drawing. The scalar product is not a mechanical formula: compute precisely, then interpret. For example (2, 1)·(1, −2) = 2 − 2 = 0, so the vectors are perpendicular.",
          "جمع المتجهات يعني تركيب انتقالات. ولاختبار انتماء نقطة إلى مستقيم نعوّض إحداثياتها بدل الثقة بالرسم. والجداء السلمي ليس صيغة آلية: نحسب بدقة ثم نفسّر. مثلًا (2, 1)·(1, −2) = 2 − 2 = 0 إذن المتجهان متعامدان.",
          "Calculer puis interpréter."),
        F("2 × 1 + 1 × (−2) = 0"),
    ]),
    ("Proof bridge", "جسر البرهان", "Pont vers la preuve", "", [
        T("Geometry statement → choose coordinates or vectors → compute a justified relation → translate the result back to geometry. If the result stays as numbers without interpretation, the solution is not finished.",
          "عبارة هندسية ← نختار إحداثيات أو متجهات ← نحسب علاقة مبرَّرة ← نترجم النتيجة إلى هندسة. إذا بقيت النتيجة أرقامًا بلا تفسير فلم ينتهِ الحل.",
          "Retour à la géométrie."),
        F("Plot → translate → calculate → verify → interpret"),
    ]),
]

EXERCISES = [
    EX("1", "", st("A(1, 2), B(4, 6): find AB and BA.", "A(1, 2) وB(4, 6): أوجد AB وBA.", "Trouve AB et BA."), [F("AB = (3, 4)      BA = (−3, −4)")]),
    EX("2", "", st("Are (2, 1) and (1, −2) perpendicular?", "هل (2, 1) و(1, −2) متعامدان؟", "Perpendiculaires ?"), [F("2 − 2 = 0  ⇒  yes")]),
    EX("3", "", st("Error detective: AB = A − B.", "المحقق: AB = A − B.", "Détective."), [T("From A to B means B − A.", "من A إلى B تعني B − A.", "B − A.")]),
    EX("4", "", st("Say in a sentence what AB = (3, 4) means.", "قل بجملة ماذا يعني AB = (3, 4).", "Explique AB = (3, 4)."), [T("Move 3 right and 4 up.", "نتحرك 3 يمينًا و4 للأعلى.", "3 à droite, 4 en haut.")]),
]
