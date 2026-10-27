"""Grade 10 Mathematics — Coordinate systems (source-controlled; NABIL's own examples)."""
from scripts.direct_lessons.common import T, F, EX, st, scene

LESSON_ID = "G10-MATH-EN-012"
GRADE = 10
SUBJECT = "math"
TITLES = {"en": "Coordinate systems", "ar": "الجمل الإحداثية", "fr": "Repères du plan"}


def plane(pts=(), line=None, rng=5, tag="C"):
    """Coordinate plane -rng..rng with labelled points {name:(x,y)} and an optional line ((x1,y1),(x2,y2))."""
    s, ox, oy = 52, 330, 220
    X = lambda v: ox + v * s
    Y = lambda v: oy - v * s
    svg = f'<g id="{tag}g">'
    for i in range(-rng, rng + 1):
        svg += (f'<line x1="{X(i)}" y1="{Y(-4)}" x2="{X(i)}" y2="{Y(4)}" stroke="#e0e6ea" stroke-width="2"/>')
    for j in range(-4, 5):
        svg += f'<line x1="{X(-rng)}" y1="{Y(j)}" x2="{X(rng)}" y2="{Y(j)}" stroke="#e0e6ea" stroke-width="2"/>'
    svg += (f'<line x1="{X(-rng)}" y1="{oy}" x2="{X(rng)}" y2="{oy}" stroke="#0b3d5c" stroke-width="4"/>'
            f'<line x1="{ox}" y1="{Y(-4)}" x2="{ox}" y2="{Y(4)}" stroke="#0b3d5c" stroke-width="4"/>')
    for i in range(-rng, rng + 1):
        if i:
            svg += f'<text x="{X(i)}" y="{oy+22}" font-size="16" text-anchor="middle" fill="#0b3d5c" font-family="sans-serif">{i}</text>'
    for j in range(-4, 5):
        if j:
            svg += f'<text x="{ox-12}" y="{Y(j)+5}" font-size="16" text-anchor="end" fill="#0b3d5c" font-family="sans-serif">{j}</text>'
    svg += '</g>'
    ids = [tag + "g"]
    if line:
        (x1, y1), (x2, y2) = line
        svg += f'<g id="{tag}L"><line x1="{X(x1)}" y1="{Y(y1)}" x2="{X(x2)}" y2="{Y(y2)}" stroke="#e53935" stroke-width="5"/></g>'
        ids.append(tag + "L")
    for k, (x, y) in dict(pts).items():
        svg += (f'<g id="{tag}{k}"><circle cx="{X(x)}" cy="{Y(y)}" r="9" fill="#1e88e5" stroke="#0b3d5c" stroke-width="2"/>'
                f'<text x="{X(x)+12}" y="{Y(y)-10}" font-size="22" font-weight="700" fill="#0b3d5c" font-family="sans-serif">{k}({x},{y})</text></g>')
        ids.append(f"{tag}{k}")
    return scene(svg, ids)


def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "M(3, 2): which number is the abscissa?", "opts": ["3", "2", "5", "1"], "a": 0,
     "why": {"2": _w("That is the ordinate (second).", "هذه هي الإحداثية الثانية.", "C'est l'ordonnée."),
             "5": _w("We do not add the coordinates.", "لا نجمع الإحداثيتين.", "On n'additionne pas."),
             "1": _w("Read x first.", "نقرأ x أولًا.", "Lis x d'abord.")}, "ok": "abscissa = 3"},
    {"q": "Plot C(2, 5): where do we go?", "opts": ["2 along x, then 5 along y", "5 along x, then 2 along y", "7 along x", "2 along y only"], "a": 0,
     "why": {"5 along x, then 2 along y": _w("Reversed order: that is the point (5,2).", "ترتيب معكوس: هذه النقطة (5,2).", "Ordre inversé : (5,2)."),
             "7 along x": _w("Do not add.", "لا نجمع.", "Ne pas additionner."),
             "2 along y only": _w("We need both coordinates.", "نحتاج الإحداثيتين.", "Les deux coordonnées.")}, "ok": "first coordinate on the first axis"},
]

THEORY = [
    ("A reference system", "الجملة المرجعية", "Un repère", "123", [
        T("Hello! Last time we saw that an ordered pair has an order. Now it becomes a real place. The pair (3, 2) does not live in empty space: we need the origin, the axes, the orientation and the scale. The same geometric point can get different coordinates if the reference system changes.",
          "مرحبًا! رأينا أن للزوج المرتب ترتيبًا. الآن يصبح مكانًا حقيقيًا. الزوج (3, 2) لا يعيش في الفراغ: نحتاج المبدأ والمحورين والاتجاه والسلم. ويمكن أن تنال النقطة الهندسية نفسها إحداثيات مختلفة إذا تغيّرت الجملة المرجعية.",
          "Un repère : origine, axes, orientation, échelle."),
        plane(),
    ]),
    ("Abscissa and ordinate", "الفاصلة والترتيبة", "Abscisse et ordonnée", "123", [
        T("In M(x, y): x is the first coordinate, the abscissa, read on the first axis; y is the second coordinate, the ordinate, read on the second axis. Always read x first, y second. The pair is a trip from the origin: first along x, then along y.",
          "في M(x, y): x هي الإحداثية الأولى أي الفاصلة وتُقرأ على المحور الأول، وy الإحداثية الثانية أي الترتيبة وتُقرأ على المحور الثاني. نقرأ x أولًا ثم y. والزوج رحلة من المبدأ: أولًا على x ثم على y.",
          "M(x, y) : abscisse puis ordonnée."),
        plane({"M": (3, 2)}),
    ]),
    ("Plotting and negative coordinates", "تعيين النقط والإحداثيات السالبة", "Placer des points", "123", [
        T("Plot A(4, 2): go 4 along the first axis, then 2 along the second, then check the point against both axes. For B(−3, 2) the minus sign tells us the side: 3 to the left of the origin, then 2 up. Finally read the point back to make sure we recover (−3, 2). Always read the scale: if each mark is 2 units, the third mark is 6, not 3.",
          "نعيّن A(4, 2): 4 على المحور الأول ثم 2 على الثاني ثم نتحقق من النقطة على المحورين. وفي B(−3, 2) تخبرنا إشارة الناقص بالجهة: 3 إلى يسار المبدأ ثم 2 إلى أعلى. وأخيرًا نقرأ النقطة لنسترجع (−3, 2). ونقرأ السلم دائمًا: إذا كان كل تدريج يمثّل وحدتين فالتدريج الثالث هو 6 لا 3.",
          "A(4,2), B(−3,2) : lire l'échelle."),
        plane({"A": (4, 2), "B": (-3, 2)}),
    ]),
    ("Equal coordinates", "إحداثيات متساوية", "Coordonnées égales", "124", [
        T("P(2, 1) and Q(2, 5) have the same first coordinate. R(−1, 3) and S(4, 3) have the same second coordinate. We read this from the numbers, not from the drawing: it is more exact than \"they look level\".",
          "للنقطتين P(2, 1) وQ(2, 5) الإحداثية الأولى نفسها، وللنقطتين R(−1, 3) وS(4, 3) الإحداثية الثانية نفسها. نقرأ ذلك من الأعداد لا من الرسم، وهذا أدقّ من «تبدوان على مستوى واحد».",
          "Même abscisse ou même ordonnée."),
        plane({"P": (2, 1), "Q": (2, 3)}),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Reference first, coordinates second. x first, y second. Read with the scale. Coordinates depend on the reference system.",
          "المرجع أولًا ثم الإحداثيات. x أولًا ثم y. نقرأ بالسلم. والإحداثيات تعتمد على الجملة المرجعية.",
          "Repère d'abord, coordonnées ensuite."),
        F("M(x, y):  x → abscissa,  y → ordinate"),
    ]),
]

EXERCISES = [
    EX("1", "", st("Plot D(−2, −3) and read it back.", "عيّن D(−2, −3) ثم اقرأها من جديد.", "Place D(−2, −3) et relis-la."), [plane({"D": (-2, -3)}), F("(−2, −3)")]),
    EX("2", "", st("A point is read as x = 4 and y = −1: write its coordinates.", "قُرئت نقطة بـx = 4 وy = −1: اكتب إحداثياتها.", "x = 4, y = −1 : écris les coordonnées."), [F("(4, −1)")]),
    EX("3", "", st("Compare U(3, −2) and V(3, 4).", "قارن U(3, −2) وV(3, 4).", "Compare U(3,−2) et V(3,4)."), [T("Same first coordinate 3, different second coordinates.", "الإحداثية الأولى نفسها 3 والثانية مختلفة.", "Même abscisse 3, ordonnées différentes.")]),
    EX("4", "", st("Error detective: C(2, 5) plotted where (5, 2) is.", "المحقق: عُيّنت C(2, 5) في موضع (5, 2).", "Détective : C(2,5) placée en (5,2)."), [T("The order was reversed: the first coordinate must stay first.", "انعكس الترتيب: الإحداثية الأولى تبقى أولى.", "Ordre inversé.")]),
    EX("5", "", st("Error detective: each mark means 2 units, but a student reads the third mark as 3.", "المحقق: كل تدريج يمثّل وحدتين لكن طالبًا قرأ التدريج الثالث 3.", "Détective : chaque graduation vaut 2."), [F("third mark = 3 × 2 = 6")]),
]
