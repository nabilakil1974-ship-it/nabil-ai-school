"""Grade 10 Mathematics — Vectors (source-controlled; general examples)."""
from scripts.direct_lessons.common import T, F, EX, st, scene

LESSON_ID = "G10-MATH-EN-008"
GRADE = 10
SUBJECT = "math"
TITLES = {"en": "Vectors", "ar": "المتجهات", "fr": "Les vecteurs"}


def arrows(pts, path, tag="V", labels=True, res=None):
    """pts: {'A':(x,y),..}; path: list of letters drawn as successive arrows; res: (from,to) dashed resultant."""
    svg = '<defs><marker id="ah" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#0b3d5c"/></marker>' \
          '<marker id="ar" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#e53935"/></marker></defs>'
    ids = []
    for i in range(len(path) - 1):
        a, b = pts[path[i]], pts[path[i + 1]]
        svg += f'<g id="{tag}a{i}"><line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#0b3d5c" stroke-width="5" marker-end="url(#ah)"/></g>'
        ids.append(f"{tag}a{i}")
    if res:
        a, b = pts[res[0]], pts[res[1]]
        svg += f'<g id="{tag}r"><line x1="{a[0]}" y1="{a[1]+14}" x2="{b[0]}" y2="{b[1]+14}" stroke="#e53935" stroke-width="5" stroke-dasharray="12 7" marker-end="url(#ar)"/></g>'
        ids.append(tag + "r")
    for k, (x, y) in pts.items():
        svg += (f'<g id="{tag}p{k}"><circle cx="{x}" cy="{y}" r="9" fill="#1e88e5"/>'
                f'<text x="{x-4}" y="{y-16}" font-size="30" font-weight="700" fill="#0b3d5c" font-family="sans-serif">{k}</text></g>')
        ids.append(f"{tag}p{k}")
    return scene(svg, ids)


def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "A→B then B→C: the resultant goes from ? to ?", "opts": ["A to C", "A to B", "B to C", "C to A"], "a": 0,
     "why": {"A to B": _w("That is only the first step.", "هذه الخطوة الأولى فقط.", "Seulement la 1re étape."),
             "B to C": _w("That is only the second step.", "هذه الخطوة الثانية فقط.", "Seulement la 2e étape."),
             "C to A": _w("The sense is reversed.", "الاتجاه معكوس.", "Sens inversé.")}, "ok": "AB + BC = AC"},
    {"q": "AB and BA have the same ?", "opts": ["magnitude", "sense", "initial point", "vector"], "a": 0,
     "why": {"sense": _w("The sense is reversed.", "الاتجاه معكوس.", "Le sens est inversé."),
             "initial point": _w("A start point is A for one and B for the other.", "البداية A في الأول وB في الثاني.", "Le départ change."),
             "vector": _w("They are opposite vectors.", "هما متجهان متعاكسان.", "Vecteurs opposés.")}, "ok": "same magnitude, opposite sense"},
]

THEORY = [
    ("A vector is a displacement", "المتجه انتقال", "Un vecteur est un déplacement", "", [
        T("Hello! Imagine walking from A to B. It is not enough to know how many metres: we also need the direction and the sense. A vector describes the whole displacement: direction, sense and magnitude. The vector AB starts at the initial point A and ends at the terminal point B. The length AB is just a non-negative number.",
          "مرحبًا! تخيّل أنك تمشي من A إلى B. لا يكفي أن نعرف كم مترًا، بل نحتاج الاتجاه والمنحى أيضًا. المتجه يصف الانتقال كاملًا: الحامل والمنحى والطول. المتجه AB يبدأ من نقطة البداية A وينتهي عند نقطة النهاية B، أما الطول AB فعدد غير سالب فقط.",
          "Un vecteur : direction, sens, norme. AB va de A à B."),
        arrows({"A": (100, 270), "B": (500, 130)}, ["A", "B"]),
        F("vector AB: A → B      length AB ≥ 0"),
    ]),
    ("AB and BA", "AB وBA", "AB et BA", "", [
        T("Swapping the letters gives vector BA: same magnitude, but the sense is reversed. AB and BA are opposite vectors, not equal vectors.",
          "تبديل الحرفين يعطي المتجه BA: الطول نفسه لكن المنحى معكوس. AB وBA متجهان متعاكسان لا متساويان.",
          "BA est l'opposé de AB."),
        arrows({"A": (100, 270), "B": (500, 130)}, ["B", "A"]),
    ]),
    ("Equal vectors", "المتجهات المتساوية", "Vecteurs égaux", "", [
        T("Two arrows in different places can represent the same vector if they have the same direction, the same sense and the same magnitude. Equal length alone is not enough: 4 units to the right is not equal to 4 units to the left. And never decide from a rough drawing: we need explicit data.",
          "قد يمثّل سهمان في مكانين مختلفين المتجه نفسه إذا اتفقا في الحامل والمنحى والطول. تساوي الطول وحده لا يكفي: 4 وحدات يمينًا لا تساوي 4 وحدات يسارًا. ولا نحكم من رسم تقريبي بل نحتاج معطيات صريحة.",
          "Même direction, même sens, même norme."),
    ]),
    ("Addition: successive displacements", "الجمع: انتقالات متتالية", "Addition : déplacements successifs", "", [
        T("Move from A to B, then from B to C. Where are you relative to the start? At C. So AB + BC = AC. The end of the first displacement becomes the start of the second (head to tail). We do not cancel the letter B like a fraction: the reason is geometric, the two moves connect at B.",
          "ننتقل من A إلى B ثم من B إلى C. أين صرنا نسبةً إلى البداية؟ عند C. إذن AB + BC = AC. نهاية الانتقال الأول تصبح بداية الثاني (رأس بذيل). ولا نحذف الحرف B كما في الكسور: السبب هندسي، فالانتقالان يتصلان عند B.",
          "AB + BC = AC (relation de Chasles)."),
        arrows({"A": (80, 300), "B": (280, 130), "C": (540, 250)}, ["A", "B", "C"], res=("A", "C")),
        F("AB + BC = AC"),
    ]),
    ("A chain of displacements", "سلسلة انتقالات", "Une chaîne de déplacements", "", [
        T("A→B, B→C, C→D gives the resultant AD, whatever the lengths. We never add the lengths automatically, because the directions differ. A numerical magnitude of AD needs extra data.",
          "A→B وB→C وC→D تعطي المحصّلة AD مهما كانت الأطوال. لا نجمع الأطوال تلقائيًا لأن الاتجاهات تختلف. والطول العددي لـAD يحتاج معطيات إضافية.",
          "AB + BC + CD = AD."),
        arrows({"A": (60, 300), "B": (220, 130), "C": (420, 250), "D": (590, 100)}, ["A", "B", "C", "D"], res=("A", "D")),
        F("AB + BC + CD = AD"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Identify start and end and the meaning BEFORE manipulating notation. Vector ≠ magnitude. Equal vectors share direction, sense and magnitude.",
          "نحدّد البداية والنهاية والمعنى قبل التعامل مع الرموز. المتجه ليس طوله. والمتجهات المتساوية تشترك في الحامل والمنحى والطول.",
          "Début, fin, sens d'abord."),
        F("AB + BC = AC      BA = −AB"),
    ]),
]

EXERCISES = [
    EX("1", "", st("A movement goes from P to Q: initial and terminal points?", "انتقال من P إلى Q: ما نقطتا البداية والنهاية؟", "Déplacement de P à Q : départ et arrivée ?"), [T("Initial: P. Terminal: Q. The order of the letters tells us.", "البداية P والنهاية Q. ترتيب الحرفين يخبرنا بذلك.", "Départ P, arrivée Q.")]),
    EX("2", "", st("Compare vector AB with vector BA.", "قارن المتجه AB بالمتجه BA.", "Compare AB et BA."), [T("Same magnitude, reversed sense: opposite vectors, not equal.", "الطول نفسه والمنحى معكوس: متعاكسان لا متساويان.", "Même norme, sens opposé.")]),
    EX("3", "", st("A→B followed by B→C: the resultant?", "A→B ثم B→C: ما المحصّلة؟", "A→B puis B→C : résultante ?"), [arrows({"A": (80, 300), "B": (280, 130), "C": (540, 250)}, ["A", "B", "C"], res=("A", "C")), F("AB + BC = AC")]),
    EX("4", "", st("Error detective: \"the arrows have the same length, so the vectors are equal\".", "المحقق: «السهمان لهما الطول نفسه فالمتجهان متساويان».", "Détective : même longueur donc égaux ?"), [T("Direction and sense must also be established.", "يجب إثبات الحامل والمنحى أيضًا.", "Direction et sens aussi.")]),
    EX("5", "", st("A→B, B→C, C→D: find the resultant.", "A→B وB→C وC→D: أوجد المحصّلة.", "A→B, B→C, C→D : résultante."), [F("AB + BC + CD = AD")]),
    EX("6", "", st("If a question asks for the magnitude, do we answer with a vector?", "إذا طُلب الطول، هل نجيب بمتجه؟", "Si on demande la norme, répond-on par un vecteur ?"), [T("No: magnitude is a number; a vector has direction and sense too.", "لا: الطول عدد، أما المتجه ففيه حامل ومنحى أيضًا.", "Non : la norme est un nombre.")]),
]
