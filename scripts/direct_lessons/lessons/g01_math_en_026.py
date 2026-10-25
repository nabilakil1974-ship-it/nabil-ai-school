"""Grade 1 Mathematics — Draw with a ruler."""
from scripts.direct_lessons.common import T, F, EX, st, scene

LESSON_ID = "G01-MATH-EN-026"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Draw with a ruler", "ar": "الرسم بالمسطرة", "fr": "Tracer avec une règle"}

INK = "#0b3d5c"


def pt(x, y, name, sid):
    return (f'<circle id="{sid}" cx="{x}" cy="{y}" r="9" fill="#e53935"/>'
            f'<text id="{sid}t" x="{x}" y="{y - 18}" font-size="30" font-weight="700" text-anchor="middle" fill="{INK}" font-family="sans-serif">{name}</text>')


def ruler(x1, y1, x2, y2, sid="r"):
    import math
    ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    L = math.hypot(x2 - x1, y2 - y1) + 140
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    return (f'<g id="{sid}" transform="translate({cx} {cy}) rotate({ang})"><rect x="{-L/2}" y="0" width="{L}" height="44" rx="6" '
            f'fill="#ffe082" stroke="{INK}" stroke-width="3"/></g>')


def line(x1, y1, x2, y2, sid="ln"):
    return f'<line id="{sid}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'


def two_points(a, b, with_ruler=True, with_line=False, ruler_off=None):
    svg = ""; ids = []
    if with_ruler:
        rx1, ry1, rx2, ry2 = (a + b)
        svg += ruler(*(a + b)) if ruler_off is None else ruler(a[0], a[1] + ruler_off, b[0], b[1] + ruler_off); ids.append("r")
    svg += pt(a[0], a[1], "A", "pa") + pt(b[0], b[1], "B", "pb"); ids += ["pa", "pat", "pb", "pbt"]
    if with_line:
        svg += line(a[0], a[1], b[0], b[1]); ids.append("ln")
    return scene(svg, ids)


A, B = (120, 220), (540, 220)
THEORY = [
    ("Align the ruler with the target path", "نضبط المسطرة على المسار المطلوب", "Placer la règle sur le trajet voulu", "72", [
        T("Hello! Today we have a ruler and a pencil. But careful: today the ruler is not for measuring. We use it to help us draw a straight line.",
          "مرحبًا! اليوم معنا مسطرة وقلم. لكن انتبه: اليوم المسطرة ليست للقياس بل تساعدنا على رسم خط مستقيم.",
          "Bonjour ! Aujourd'hui on a une règle et un crayon. Mais attention : la règle ne sert pas à mesurer. Elle nous aide à tracer un trait droit."),
        two_points(A, B, with_ruler=False),
        T("I have two points and I want to join them with a straight, exact line. If I draw by hand without a ruler, the line may wobble.",
          "عندي نقطتان وأريد أن أصلهما بخط مستقيم ودقيق. إذا رسمت باليد بدون مسطرة فقد يخرج الخط متعرجًا.",
          "J'ai deux points et je veux les relier par un trait droit et précis. Si je dessine à main levée, le trait peut trembler."),
        two_points(A, B, ruler_off=120),
        T("If the ruler is here, does its edge pass through the two points? No. Before drawing, we must align it.",
          "إذا كانت المسطرة هنا فهل حافتها تمرّ بالنقطتين؟ لا. قبل الرسم يجب أن نضبطها.",
          "Si la règle est ici, son bord passe-t-il par les deux points ? Non. Avant de tracer, il faut l'aligner."),
        two_points((120, 190), (540, 190)),
        T("Now the edge of the ruler passes through both points. This is the first step: ALIGN.",
          "الآن حافة المسطرة تمرّ بالنقطتين. هذه الخطوة الأولى: نضبط.",
          "Maintenant le bord de la règle passe par les deux points. C'est la première étape : ALIGNER."),
    ]),
    ("Hold the ruler still", "نثبّت المسطرة", "Tenir la règle immobile", "72", [
        T("The ruler is in the right place. But if it moves while I draw, what happens? The line changes and does not stay straight. So the second step is HOLD. One hand holds the ruler and the other holds the pencil. We do not press hard; we just keep it still.",
          "المسطرة في مكانها الصحيح. لكن إذا تحرّكت أثناء الرسم فماذا يحدث؟ يتغيّر الخط ولا يبقى مستقيمًا. إذن الخطوة الثانية: نثبّت. يد تثبّت المسطرة واليد الأخرى تمسك القلم. لا نضغط بعنف، فقط نبقيها ثابتة.",
          "La règle est au bon endroit. Mais si elle bouge pendant que je trace, que se passe-t-il ? Le trait change et n'est plus droit. La deuxième étape est donc TENIR. Une main tient la règle et l'autre le crayon. On n'appuie pas fort ; on la garde immobile."),
    ]),
    ("Draw along the edge", "نرسم على الحافة", "Tracer le long du bord", "73", [
        two_points((120, 190), (540, 190), with_line=True),
        T("The ruler is aligned and still, so now we draw. Put the pencil at the first point, touching the edge of the ruler, and move it gently along the edge to the second point. This is the third step: DRAW ALONG THE EDGE. We keep the pencil against the edge because the ruler is what guides the line.",
          "المسطرة مضبوطة وثابتة، والآن نرسم. نضع القلم عند النقطة الأولى ملاصقًا لحافة المسطرة ونحرّكه بهدوء على الحافة حتى النقطة الثانية. هذه الخطوة الثالثة: نرسم على الحافة. نُبقي القلم ملاصقًا للحافة لأن المسطرة هي التي توجّه الخط.",
          "La règle est alignée et immobile : on trace. On pose le crayon sur le premier point, contre le bord, et on le glisse doucement jusqu'au deuxième point. C'est la troisième étape : TRACER LE LONG DU BORD. On garde le crayon contre le bord car c'est la règle qui guide le trait."),
    ]),
    ("The ruler can turn; the steps stay the same", "المسطرة قد تدور والخطوات نفسها", "La règle peut tourner ; les étapes restent", "73", [
        two_points((120, 330), (540, 330), with_line=True),
        two_points((330, 60), (330, 380), with_line=True),
        two_points((120, 360), (540, 100), with_line=True),
        T("Sometimes the ruler is horizontal, sometimes vertical, sometimes slanted. Does the rule change? No. Whatever the direction: ALIGN, HOLD, DRAW. We turn the ruler to fit the points; we do not make the points follow the ruler.",
          "أحيانًا تكون المسطرة أفقية وأحيانًا عمودية وأحيانًا مائلة. هل تتغير القاعدة؟ لا. مهما كان الاتجاه: نضبط ثم نثبّت ثم نرسم. ندير المسطرة حسب مكان النقطتين ولا نجعل النقطتين تتبعان المسطرة.",
          "Parfois la règle est horizontale, parfois verticale, parfois oblique. La règle du jeu change-t-elle ? Non. Quelle que soit la direction : ALIGNER, TENIR, TRACER. On tourne la règle selon les points ; on ne fait pas suivre la règle aux points."),
    ]),
    ("Check the result", "نتحقق من النتيجة", "Vérifier le résultat", "73", [
        two_points((120, 220), (500, 220), with_line=True),
        T("The line passes near B but does not reach it. Is it finished correctly? No. The line must follow the intended path and reach the required point. Drawing is not only a motion of the pencil; we must CHECK: did I start at the right point? Did I reach the other point? Did I stay along the edge of the ruler?",
          "الخط يمرّ قرب B لكنه لا يصلها. هل انتهى الرسم بشكل صحيح؟ لا. يجب أن يتبع الخط المسار المقصود ويصل إلى النقطة المطلوبة. الرسم ليس حركة قلم فقط، بل يجب أن نتحقق: هل بدأت من النقطة الصحيحة؟ هل وصلت إلى النقطة الأخرى؟ هل بقيت ملاصقًا لحافة المسطرة؟",
          "Le trait passe près de B sans l'atteindre. Est-il bien terminé ? Non. Le trait doit suivre le trajet voulu et arriver au point demandé. Dessiner n'est pas seulement un geste ; il faut VÉRIFIER : suis-je parti du bon point ? Suis-je arrivé à l'autre point ? Suis-je resté le long du bord ?"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Today the ruler helped us draw an exact straight line. We did not draw fast. We did four steps: align, hold, draw, check.",
          "اليوم ساعدتنا المسطرة على رسم خط مستقيم بدقة. لم نرسم بسرعة. فعلنا أربع خطوات: نضبط، نثبّت، نرسم، نتحقق.",
          "Aujourd'hui la règle nous a aidés à tracer un trait droit précis. On n'a pas dessiné vite. Quatre étapes : aligner, tenir, tracer, vérifier."),
        F("ALIGN → HOLD → DRAW → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "72", st("Which ruler placement is ready for drawing?", "أي وضع للمسطرة جاهز للرسم؟", "Quel placement de la règle est prêt pour tracer ?"), [
        two_points((120, 200), (540, 200), ruler_off=140),
        two_points((120, 200), (540, 320), ruler_off=0),
        two_points((120, 190), (540, 190)),
        T("Check the first point, then the second. The same edge must pass through both. Only the third placement is ready.",
          "نفحص النقطة الأولى ثم الثانية. يجب أن تمرّ الحافة نفسها بالاثنتين. فقط الوضع الثالث جاهز.",
          "Vérifie le premier point, puis le second. Le même bord doit passer par les deux. Seul le troisième placement est prêt."),
    ]),
    EX("2", "73", st("Draw between two new points. Align, hold, draw, check.", "ارسم بين نقطتين جديدتين: نضبط، نثبّت، نرسم، نتحقق.", "Trace entre deux nouveaux points : aligner, tenir, tracer, vérifier."), [
        two_points((140, 340), (520, 120), with_line=True),
        T("Did the line start at the first point? Did it reach the second? Did it stay against the edge? Then it is correct.",
          "هل بدأ الخط من النقطة الأولى؟ هل وصل إلى الثانية؟ هل بقي ملاصقًا للحافة؟ إذن هو صحيح.",
          "Le trait part-il du premier point ? Arrive-t-il au second ? Reste-t-il contre le bord ? Alors il est juste."),
    ]),
    EX("3", "73", st("Three pairs of points: horizontal, vertical and slanted. Draw each trace.", "ثلاثة أزواج من النقاط: أفقي وعمودي ومائل. ارسم كل خط.", "Trois paires de points : horizontale, verticale et oblique. Trace chaque trait."), [
        two_points((120, 330), (540, 330), with_line=True),
        two_points((330, 60), (330, 380), with_line=True),
        two_points((120, 360), (540, 100), with_line=True),
        T("After each one check: alignment first, then stability, then the line.",
          "بعد كل واحد نتحقق: الضبط أولًا ثم الثبات ثم الخط.",
          "Après chacun, vérifie : l'alignement d'abord, puis la stabilité, puis le trait."),
    ]),
    EX("4", "73", st("Error detective: one picture moved while drawing, one ruler misses the points, one is correct. Which is right?", "المحقق: صورة تحرّكت فيها المسطرة أثناء الرسم، وصورة المسطرة لا تمرّ بالنقطتين، وصورة صحيحة. أيها الصحيحة؟", "Détective : une image où la règle a bougé, une où la règle manque les points, une juste. Laquelle est juste ?"), [
        two_points((120, 200), (540, 200), ruler_off=140),
        two_points((120, 190), (540, 190), with_line=True),
        T("The third picture is correct: aligned, held still, and drawn along the edge.",
          "الصورة الثالثة صحيحة: مضبوطة وثابتة ومرسومة على الحافة.",
          "La troisième image est juste : alignée, immobile et tracée le long du bord."),
    ]),
    EX("5", "73", st("Put the steps in order: DRAW, HOLD, ALIGN, CHECK.", "رتّب الخطوات: نرسم، نثبّت، نضبط، نتحقق.", "Range les étapes : TRACER, TENIR, ALIGNER, VÉRIFIER."), [
        T("Ask yourself: can I draw before I know where the ruler is? No.",
          "اسأل نفسك: هل أستطيع أن أرسم قبل أن أعرف أين المسطرة؟ لا.",
          "Demande-toi : puis-je tracer avant de savoir où est la règle ? Non."),
        F("ALIGN → HOLD → DRAW → CHECK"),
    ]),
    EX("6", "73", st("Join A with B, then B with C. Do all four steps for each line.", "صِل A مع B ثم B مع C. افعل الخطوات الأربع لكل خط.", "Relie A à B puis B à C. Fais les quatre étapes pour chaque trait."), [
        scene(pt(120, 330, "A", "pa") + pt(330, 90, "B", "pb") + pt(540, 330, "C", "pc") + line(120, 330, 330, 90, "l1") + line(330, 90, 540, 330, "l2"),
              ["pa", "pat", "pb", "pbt", "pc", "pct", "l1", "l2"]),
        T("When the figure has more than one line, we do not hurry. Each line has its own alignment.",
          "عندما يكون في الشكل أكثر من خط لا نستعجل. لكل خط ضبطه الخاص.",
          "Quand la figure a plusieurs traits, on ne se presse pas. Chaque trait a son propre alignement."),
    ]),
    EX("7", "73", st("Challenge: two points very close and two points far apart. Which pair needs the same steps?", "تحدٍّ: نقطتان قريبتان جدًا ونقطتان بعيدتان. أي زوج يحتاج الخطوات نفسها؟", "Défi : deux points très proches et deux points éloignés. Quelle paire demande les mêmes étapes ?"), [
        two_points((250, 150), (330, 150), with_line=True),
        two_points((60, 300), (600, 300), with_line=True),
        T("Both. The distance changes, but the procedure is the same. Draw both and check.",
          "كلاهما. تتغير المسافة لكن الإجراء نفسه. ارسم الاثنين وتحقق.",
          "Les deux. La distance change, mais la procédure est la même. Trace les deux et vérifie."),
    ]),
    EX("8", "73", st("Final check: say the four steps aloud and draw a slanted line between two points.", "تقييم أخير: قل الخطوات الأربع بصوت عالٍ وارسم خطًا مائلًا بين نقطتين.", "Évaluation : dis les quatre étapes à voix haute et trace un trait oblique entre deux points."), [
        two_points((120, 340), (540, 110), with_line=True),
        F("ALIGN → HOLD → DRAW → CHECK"),
        T("If you can do the steps and explain why, you understand using a ruler as a straightedge.",
          "إذا استطعت تنفيذ الخطوات وشرح السبب فقد فهمت استعمال المسطرة كأداة للخط المستقيم.",
          "Si tu sais faire les étapes et expliquer pourquoi, tu as compris l'usage de la règle comme règle à tracer."),
    ]),
]
