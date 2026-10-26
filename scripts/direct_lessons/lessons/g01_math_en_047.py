"""Grade 1 Mathematics — Superposition of figures."""
from scripts.direct_lessons.common import T, F, EX, st, scene

A, B, ST = "#ffb74d", "#4fc3f7", "#0b3d5c"


def _poly(pid, pts, fill, op=1.0):
    p = " ".join(f"{x},{y}" for x, y in pts)
    return f'<polygon id="{pid}" points="{p}" fill="{fill}" fill-opacity="{op}" stroke="{ST}" stroke-width="4"/>'


def _shape(kind, cx, cy, s, rot=0):
    import math
    if kind == "sq":
        pts = [(-s, -s), (s, -s), (s, s), (-s, s)]
    elif kind == "rect":
        pts = [(-1.5 * s, -s * 0.7), (1.5 * s, -s * 0.7), (1.5 * s, s * 0.7), (-1.5 * s, s * 0.7)]
    elif kind == "tri":
        pts = [(0, -s), (s * 1.1, s * 0.8), (-s * 1.1, s * 0.8)]
    else:
        return None
    r = math.radians(rot)
    return [(round(cx + x * math.cos(r) - y * math.sin(r), 1), round(cy + x * math.sin(r) + y * math.cos(r), 1)) for x, y in pts]


def pair(k1, s1, k2, s2, rot2=0, over=False, tag="P"):
    """Two figures side by side, or the second laid over the first (same centre) when over=True."""
    svg, ids = "", []
    c1 = (330, 140) if over else (170, 140)
    c2 = (330, 140) if over else (470, 140)
    for n, (k, s, c, col, rot) in enumerate([(k1, s1, c1, A, 0), (k2, s2, c2, B, rot2)]):
        sid = f"{tag}{n}"
        if k == "circle":
            svg += f'<circle id="{sid}" cx="{c[0]}" cy="{c[1]}" r="{s}" fill="{col}" fill-opacity="{0.6 if over else 1}" stroke="{ST}" stroke-width="4"/>'
        else:
            svg += _poly(sid, _shape(k, c[0], c[1], s, rot), col, 0.6 if over else 1)
        ids.append(sid)
    return scene(svg, ids)


LESSON_ID = "G01-MATH-EN-047"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Superposition of figures", "ar": "تطابق الأشكال بالوضع فوق بعضها", "fr": "Superposition de figures"}

THEORY = [
    ("Do they look the same?", "هل يبدوان متماثلين؟", "Se ressemblent-elles ?", "118", [
        pair("sq", 60, "sq", 60),
        T("Hello, champion! Here are two figures that look the same. How can we be sure? Looking is not enough. We can lay one over the other, like cutting out a paper shape and placing it on top. This is called superposition.",
          "مرحبًا يا بطل! هنا شكلان يبدوان متماثلين. كيف نتأكد؟ النظر وحده لا يكفي. نستطيع وضع أحدهما فوق الآخر كأننا نقصّ شكلًا ورقيًا ونضعه عليه. هذا يسمى التطابق بالوضع فوق بعضها.",
          "Voici deux figures qui se ressemblent. Comment être sûr ? Regarder ne suffit pas. On peut poser l'une sur l'autre, comme une forme découpée en papier. C'est la superposition."),
    ]),
    ("They coincide exactly", "تنطبقان تمامًا", "Elles coïncident exactement", "118", [
        pair("sq", 60, "sq", 60, over=True),
        T("When we put one square on the other, all the edges and corners cover each other exactly. We see only one square. The two figures coincide: same shape and same size.",
          "عندما نضع مربعًا فوق الآخر تنطبق كل الأضلاع والزوايا تمامًا. لا نرى إلا مربعًا واحدًا. الشكلان متطابقان: الشكل نفسه والحجم نفسه.",
          "En posant un carré sur l'autre, tous les côtés et les coins se recouvrent exactement. On ne voit qu'un carré. Les figures coïncident : même forme, même taille."),
    ]),
    ("Same kind, different size", "النوع نفسه والحجم مختلف", "Même genre, taille différente", "119", [
        pair("sq", 40, "sq", 70, over=True),
        T("Both are squares, but when we lay the small one on the big one, the edges do not meet. The big square sticks out. They do not coincide because the sizes are different.",
          "كلاهما مربع، لكن عندما نضع الصغير على الكبير لا تتلاقى الأضلاع. المربع الكبير يبرز. لا يتطابقان لأن الحجمين مختلفان.",
          "Ce sont deux carrés, mais en posant le petit sur le grand, les côtés ne se rencontrent pas. Le grand dépasse. Elles ne coïncident pas car les tailles sont différentes."),
    ]),
    ("Turning before comparing", "ندير الشكل قبل المقارنة", "Tourner avant de comparer", "120", [
        pair("tri", 60, "tri", 60, rot2=180),
        T("Sometimes one figure is turned. These two triangles are the same, but one is upside down. We must turn it first, then lay it over the other. After turning, all the edges cover each other exactly.",
          "أحيانًا يكون أحد الشكلين مقلوبًا. هذان المثلثان متماثلان لكن أحدهما مقلوب. علينا أن ندير الشكل أولًا ثم نضعه فوق الآخر. بعد الإدارة تنطبق كل الأضلاع تمامًا.",
          "Parfois une figure est tournée. Ces deux triangles sont identiques, mais l'un est retourné. On le tourne d'abord, puis on le pose sur l'autre : tous les côtés se recouvrent."),
        pair("tri", 60, "tri", 60, over=True),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Superposition is a direct way to test whether two figures have the same shape and size. We may move or turn a figure, but we never stretch it. Two figures coincide only when the whole outline covers exactly.",
          "الوضع فوق بعضها طريقة مباشرة لمعرفة هل للشكلين الشكل نفسه والحجم نفسه. نستطيع تحريك الشكل أو إدارته لكن لا نمطّه أبدًا. يتطابق الشكلان فقط إذا انطبق الإطار كله تمامًا.",
          "La superposition teste directement si deux figures ont la même forme et la même taille. On peut déplacer ou tourner une figure, jamais l'étirer. Elles coïncident seulement si tout le contour se recouvre."),
        F("MOVE OR TURN → LAY ONE ON THE OTHER → CHECK THE WHOLE OUTLINE"),
    ]),
]

EXERCISES = [
    EX("1", "118", st("Do these two squares coincide?", "هل يتطابق هذان المربعان؟", "Ces deux carrés coïncident-ils ?"), [
        pair("sq", 60, "sq", 60, over=True),
        T("Yes. The whole outline covers exactly.", "نعم. ينطبق الإطار كله تمامًا.", "Oui. Tout le contour se recouvre."),
    ]),
    EX("2", "119", st("Does the small square coincide with the big square?", "هل ينطبق المربع الصغير على المربع الكبير؟", "Le petit carré coïncide-t-il avec le grand ?"), [
        pair("sq", 35, "sq", 65, over=True),
        T("No. The edges do not meet; the big one sticks out.", "لا. الأضلاع لا تتلاقى والكبير يبرز.", "Non. Les côtés ne se rencontrent pas, le grand dépasse."),
    ]),
    EX("3", "119", st("Square and rectangle: do they coincide?", "مربع ومستطيل: هل يتطابقان؟", "Carré et rectangle : coïncident-ils ?"), [
        pair("sq", 55, "rect", 55, over=True),
        T("No. The rectangle is longer on two sides, so part of it is not covered by the square.", "لا. المستطيل أطول من جهتين فجزء منه لا يغطيه المربع.", "Non. Le rectangle est plus long, une partie dépasse du carré."),
    ]),
    EX("4", "120", st("Two triangles, one turned upside down. Can they coincide?", "مثلثان أحدهما مقلوب. هل يمكن أن يتطابقا؟", "Deux triangles, l'un retourné. Peuvent-ils coïncider ?"), [
        pair("tri", 60, "tri", 60, rot2=180),
        T("Yes, after turning one of them the outline covers exactly.", "نعم، بعد إدارة أحدهما ينطبق الإطار تمامًا.", "Oui, après avoir tourné l'une, le contour se recouvre."),
    ]),
    EX("5", "120", st("Two circles of different sizes. Do they coincide?", "دائرتان بحجمين مختلفين. هل تتطابقان؟", "Deux cercles de tailles différentes. Coïncident-ils ?"), [
        pair("circle", 40, "circle", 70, over=True),
        T("No. Same kind of figure, different size.", "لا. النوع نفسه لكن الحجم مختلف.", "Non. Même genre de figure, taille différente."),
    ]),
    EX("6", "121", st("Error check: a child says two figures coincide because one corner matches. Is that enough?", "تحقّق من الخطأ: يقول طفل إن الشكلين يتطابقان لأن زاوية واحدة تنطبق. هل يكفي ذلك؟", "Vérifie l'erreur : un enfant dit que deux figures coïncident car un coin correspond. Est-ce suffisant ?"), [
        pair("sq", 55, "rect", 55, over=True),
        T("No. We must check the complete outline, not only one corner or one side.", "لا. يجب فحص الإطار كاملًا لا زاوية واحدة أو ضلعًا واحدًا.", "Non. Il faut vérifier tout le contour, pas un seul coin ni un seul côté."),
    ]),
    EX("7", "121", st("Challenge: two equal rectangles, one turned sideways. Can they coincide?", "تحدٍّ: مستطيلان متساويان أحدهما مدار جانبيًا. هل يتطابقان؟", "Défi : deux rectangles égaux, l'un tourné. Peuvent-ils coïncider ?"), [
        pair("rect", 55, "rect", 55, rot2=90),
        T("Yes. Turn one a quarter turn and the outlines cover exactly. Turning does not change the figure.", "نعم. ندير أحدهما ربع دورة فينطبق الإطار تمامًا. الإدارة لا تغيّر الشكل.", "Oui. En tournant l'un d'un quart de tour, les contours se recouvrent. Tourner ne change pas la figure."),
    ]),
    EX("8", "121", st("Final check: superpose a pair and say whether they coincide.", "تقييم أخير: ضع زوجًا فوق بعضه وقل هل يتطابقان.", "Évaluation : superpose une paire et dis si elles coïncident."), [
        pair("tri", 60, "tri", 60, over=True),
        T("The outlines cover exactly, so the two triangles coincide.", "ينطبق الإطاران تمامًا، إذن المثلثان متطابقان.", "Les contours se recouvrent exactement : les deux triangles coïncident."),
    ]),
]
