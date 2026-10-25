"""Grade 1 Mathematics — Geometric shapes."""
from scripts.direct_lessons.common import T, F, EX, st, scene

LESSON_ID = "G01-MATH-EN-018"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Geometric shapes", "ar": "الأشكال الهندسية", "fr": "Les formes géométriques"}


def shp(kind, cx, cy, r, color, sid, rot=0):
    t = f' transform="rotate({rot} {cx} {cy})"'
    if kind == "circle":
        return f'<circle id="{sid}" cx="{cx}" cy="{cy}" r="{r}" fill="{color}" stroke="#0b3d5c" stroke-width="3"/>'
    if kind == "square":
        return f'<rect id="{sid}" x="{cx-r}" y="{cy-r}" width="{2*r}" height="{2*r}" fill="{color}" stroke="#0b3d5c" stroke-width="3"{t}/>'
    if kind == "rect":
        return f'<rect id="{sid}" x="{cx-r*1.5}" y="{cy-r*0.8}" width="{3*r}" height="{1.6*r}" fill="{color}" stroke="#0b3d5c" stroke-width="3"{t}/>'
    return f'<polygon id="{sid}" points="{cx},{cy-r} {cx-r},{cy+r} {cx+r},{cy+r}" fill="{color}" stroke="#0b3d5c" stroke-width="3"{t}/>'


def shapes(specs, tag="s"):
    """specs: list of (kind, x, y, r, color, rot)"""
    svg, ids = "", []
    for i, (k, x, y, r, c, rot) in enumerate(specs):
        sid = f"{tag}{i}"
        svg += shp(k, x, y, r, c, sid, rot); ids.append(sid)
    return scene(svg, ids)


R, B, G = "#e53935", "#1e63d6", "#43a047"
THEORY = [
    ("Look at the form, not the decoration", "ننظر إلى الشكل لا إلى الزينة", "Regarder la forme, pas la décoration", "52", [
        T("Hello! Today we use our eyes a lot. Some shapes look alike and some are different. But here is the trick: I can make a shape bigger, smaller, or turn it. Does it stay the same shape?",
          "مرحبًا! اليوم نستعمل عيوننا كثيرًا. بعض الأشكال متشابهة وبعضها مختلف. لكن هناك خدعة: أستطيع تكبير الشكل أو تصغيره أو تدويره. هل يبقى الشكل نفسه؟",
          "Bonjour ! Aujourd'hui on utilise beaucoup nos yeux. Certaines formes se ressemblent, d'autres non. Mais voici l'astuce : je peux agrandir, rétrécir ou tourner une forme. Reste-t-elle la même ?"),
        shapes([("triangle", 180, 220, 90, R, 0), ("triangle", 480, 220, 90, B, 0)]),
        T("This one is red and this one is blue. Does color alone make them different shapes? No. We look at the form itself: its boundary and how it is shaped. Color is decoration; form is geometry.",
          "هذا أحمر وهذا أزرق. هل اللون وحده يجعلهما شكلين مختلفين؟ لا. ننظر إلى الشكل نفسه: حدّه وطريقة تكوّنه. اللون زينة والشكل هو الهندسة.",
          "Celle-ci est rouge, celle-là bleue. La couleur seule les rend-elle différentes ? Non. On regarde la forme : son contour. La couleur est une décoration ; la forme, c'est la géométrie."),
    ]),
    ("Size does not change the shape", "الحجم لا يغيّر الشكل", "La taille ne change pas la forme", "52", [
        shapes([("square", 190, 230, 120, G, 0), ("square", 480, 270, 50, G, 0)], "z"),
        T("One is big and one is small. Did they become different shapes because the size changed? No. We made it bigger or smaller, but the form stayed the same.",
          "واحد كبير وواحد صغير. هل صارا شكلين مختلفين لأن الحجم تغيّر؟ لا. كبّرناه أو صغّرناه لكن الشكل بقي نفسه.",
          "L'une est grande, l'autre petite. Sont-elles devenues différentes parce que la taille a changé ? Non. On a agrandi ou rétréci, mais la forme est la même."),
    ]),
    ("Turning does not make a new shape", "التدوير لا يصنع شكلًا جديدًا", "Tourner ne crée pas une nouvelle forme", "53", [
        shapes([("triangle", 180, 220, 90, B, 0), ("triangle", 480, 220, 90, B, 135)], "t"),
        T("I turn the card. Did I change the form? No. I changed only the direction, the orientation. The geometry stayed the same.",
          "أدوّر البطاقة. هل غيّرت الشكل؟ لا. غيّرت الاتجاه فقط. الهندسة بقيت نفسها.",
          "Je tourne la carte. Ai-je changé la forme ? Non. J'ai changé seulement l'orientation. La géométrie est la même."),
    ]),
    ("Trace the boundary", "نتتبّع الحدّ", "Suivre le contour", "53", [
        shapes([("rect", 330, 220, 90, R, 0)], "b"),
        T("If we are not sure, we follow the boundary with a finger. Start here and walk all around. Does the boundary go the same way in the other shape? Tracing helps us compare the forms directly.",
          "إذا لم نكن متأكدين نتتبّع الحدّ بإصبعنا. نبدأ من هنا ونمشي حول الشكل. هل يسير الحدّ بالطريقة نفسها في الشكل الآخر؟ التتبّع يساعدنا على مقارنة الأشكال مباشرة.",
          "Si on n'est pas sûr, on suit le contour avec le doigt. On part d'ici et on fait le tour. Le contour va-t-il pareil dans l'autre forme ? Suivre le contour aide à comparer les formes directement."),
    ]),
    ("Sort by shape, not by color", "نصنّف حسب الشكل لا اللون", "Trier par forme, pas par couleur", "53", [
        shapes([("circle", 110, 130, 50, R, 0), ("square", 330, 130, 50, B, 0), ("circle", 550, 130, 50, G, 0),
                ("square", 110, 320, 50, G, 0), ("circle", 330, 320, 50, B, 0), ("square", 550, 320, 50, R, 0)], "k"),
        T("We make groups. It is forbidden to group by color. We put together the cards whose form is the same. Colors, sizes and direction may differ, but the form must match.",
          "نصنع مجموعات. يُمنع التجميع حسب اللون. نجمع البطاقات التي شكلها واحد. قد تختلف الألوان والأحجام والاتجاه، لكن يجب أن يتطابق الشكل.",
          "On fait des groupes. Interdit de grouper par couleur. On réunit les cartes qui ont la même forme. Couleurs, tailles et directions peuvent différer, mais la forme doit être la même."),
    ]),
    ("Reproduce a shape", "نعيد رسم شكل", "Reproduire une forme", "53", [
        T("After we can recognize a shape, we make one like it. Do not draw quickly. Look at the boundary and trace it with your finger first. The size does not have to be exactly the same. What matters is the form.",
          "بعد أن نميّز الشكل نصنع شكلًا مثله. لا ترسم بسرعة. انظر إلى الحدّ وتتبّعه بإصبعك أولًا. لا يجب أن يكون الحجم نفسه تمامًا. المهم الشكل.",
          "Quand on sait reconnaître une forme, on en fait une pareille. Ne dessine pas vite. Regarde le contour et suis-le d'abord du doigt. La taille n'a pas à être exactement la même. Ce qui compte, c'est la forme."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("We know a shape by its form. Color, size and direction may change, but if the geometry is the same, the shape stays the same.",
          "نعرف الشكل من هيئته. اللون والحجم والاتجاه قد تتغير، لكن إذا كانت الهندسة نفسها يبقى الشكل نفسه.",
          "On reconnaît une forme par sa forme. Couleur, taille et direction peuvent changer, mais si la géométrie est la même, la forme reste la même."),
        F("LOOK AT FORM → TRACE → ROTATE IF NEEDED → MATCH / SORT → REPRODUCE → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "52", st("Which candidate has the same form as the target? The color may differ.", "أي مرشّح له شكل الهدف نفسه؟ قد يختلف اللون.", "Quelle forme est la même que la cible ? La couleur peut différer."), [
        shapes([("triangle", 110, 120, 70, R, 0), ("triangle", 330, 330, 70, B, 0), ("circle", 520, 330, 60, B, 0), ("square", 190, 330, 55, B, 0)], "m"),
        T("Cover the color in your mind and look only at the boundary. The blue triangle matches: the color changed, the form did not.",
          "غطِّ اللون في خيالك وانظر إلى الحدّ فقط. المثلث الأزرق يطابق: تغيّر اللون ولم يتغيّر الشكل.",
          "Cache la couleur dans ta tête et regarde le contour. Le triangle bleu correspond : la couleur a changé, pas la forme."),
    ]),
    EX("2", "52", st("A small square and a big square. Same form or different?", "مربع صغير ومربع كبير. الشكل نفسه أم مختلف؟", "Un petit carré et un grand carré. Même forme ou différente ?"), [
        shapes([("square", 190, 230, 110, B, 0), ("square", 480, 260, 45, B, 0)], "q"),
        T("Same form. The size changed; the shape is the same.",
          "الشكل نفسه. الحجم تغيّر والشكل هو هو.",
          "Même forme. La taille a changé ; la forme est la même."),
    ]),
    EX("3", "53", st("Can the turned card be the same as the target?", "هل يمكن أن تكون البطاقة المدوَّرة هي الهدف نفسه؟", "La carte tournée peut-elle être la même que la cible ?"), [
        shapes([("rect", 180, 220, 70, R, 0), ("rect", 480, 220, 70, R, 90)], "r"),
        T("Let us try: turn it and put it on top of the target. It matches, so it is the same shape.",
          "لنجرّب: ندوّرها ونضعها فوق الهدف. تطابقه، إذن هو الشكل نفسه.",
          "Essayons : on la tourne et on la pose sur la cible. Elle correspond : c'est la même forme."),
    ]),
    EX("4", "53", st("Trace the target, then trace the other shape. Where do you first feel the difference?", "تتبّع الهدف ثم تتبّع الشكل الآخر. أين أول مكان تشعر فيه بالفرق؟", "Suis la cible puis l'autre forme. Où sens-tu d'abord la différence ?"), [
        shapes([("square", 190, 220, 90, G, 0), ("circle", 480, 220, 90, G, 0)], "d"),
        T("You did not guess; you compared the boundaries. One has a boundary that goes round smoothly, the other turns at its corners.",
          "لم تخمّن بل قارنت الحدود. أحدهما حدّه يدور بسلاسة والآخر يتغيّر اتجاهه عند زواياه.",
          "Tu n'as pas deviné : tu as comparé les contours. L'un tourne en douceur, l'autre change de direction aux coins."),
    ]),
    EX("5", "53", st("Sort the cards into two families by form.", "صنّف البطاقات إلى عائلتين حسب الشكل.", "Trie les cartes en deux familles selon la forme."), [
        shapes([("circle", 110, 130, 50, R, 0), ("square", 330, 130, 50, B, 0), ("circle", 550, 130, 50, G, 0),
                ("square", 110, 320, 50, G, 0), ("circle", 330, 320, 50, B, 0), ("square", 550, 320, 50, R, 0)], "f"),
        T("Do not look at color. Try turning the card. Compare the boundary. The circles go together and the squares go together.",
          "لا تنظر إلى اللون. جرّب تدوير البطاقة. قارن الحدّ. الدوائر معًا والمربعات معًا.",
          "Ne regarde pas la couleur. Essaie de tourner la carte. Compare le contour. Les cercles ensemble, les carrés ensemble."),
    ]),
    EX("6", "53", st("Error detective: “It is different only because it is turned.” Is this a strong reason?", "المحقق: «هو مختلف فقط لأنه مدوَّر». هل هذا سبب قوي؟", "Détective : « Elle est différente seulement parce qu'elle est tournée ». Est-ce une bonne raison ?"), [
        shapes([("triangle", 180, 220, 90, R, 0), ("triangle", 480, 220, 90, R, 180)], "e"),
        T("No. A good check is to rotate it, overlay it, or trace it before deciding.",
          "لا. التحقّق الجيد هو التدوير أو التطبيق أو التتبّع قبل الحكم.",
          "Non. Une bonne vérification : tourner, superposer ou suivre le contour avant de décider."),
    ]),
    EX("7", "53", st("Challenge: find all copies of the target even if color, size and direction change.", "تحدٍّ: جد كل نسخ الهدف حتى لو تغيّر اللون والحجم والاتجاه.", "Défi : trouve toutes les copies de la cible même si couleur, taille et direction changent."), [
        shapes([("triangle", 110, 110, 60, R, 0), ("triangle", 330, 330, 40, G, 45), ("rect", 520, 330, 45, G, 0), ("triangle", 540, 150, 80, B, 200), ("circle", 190, 330, 45, B, 0)], "x"),
        T("Follow the boundary and turn it in your mind. Your attention is on the geometry itself.",
          "تابع الحدّ ودوّره في ذهنك. تركيزك على الهندسة نفسها.",
          "Suis le contour et tourne-la dans ta tête. Ton attention est sur la géométrie elle-même."),
    ]),
    EX("8", "53", st("Final check: why can a turned shape still be the same?", "تقييم أخير: لماذا يمكن أن يبقى الشكل المدوَّر هو نفسه؟", "Évaluation : pourquoi une forme tournée peut-elle rester la même ?"), [
        shapes([("rect", 180, 220, 70, B, 0), ("rect", 480, 220, 70, B, 60)], "y"),
        T("Because turning changes only the direction, not the form. When we place it on the other one, it fits exactly.",
          "لأن التدوير يغيّر الاتجاه فقط لا الشكل. وعندما نضعه فوق الآخر ينطبق عليه تمامًا.",
          "Parce que tourner ne change que la direction, pas la forme. Posée sur l'autre, elle s'ajuste exactement."),
    ]),
]
