"""Grade 1 Mathematics — Solids."""
from scripts.direct_lessons.common import T, F, EX, st, scene

LESSON_ID = "G01-MATH-EN-030"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Solids", "ar": "المجسّمات", "fr": "Les solides"}
INK = "#0b3d5c"


def _shade(c, k):
    c = c.lstrip("#")
    r, g, b = (int(c[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(v * k))) for v in (r, g, b))


def box(x, y, s, color, sid):
    d = s * 0.45
    f = f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{color}" stroke="{INK}" stroke-width="3"/>'
    t = f'<polygon points="{x},{y} {x + d},{y - d} {x + s + d},{y - d} {x + s},{y}" fill="{_shade(color, 1.2)}" stroke="{INK}" stroke-width="3"/>'
    r = f'<polygon points="{x + s},{y} {x + s + d},{y - d} {x + s + d},{y + s - d} {x + s},{y + s}" fill="{_shade(color, 0.75)}" stroke="{INK}" stroke-width="3"/>'
    return f'<g id="{sid}">{f}{t}{r}</g>'


def ball(cx, cy, r, color, sid):
    return (f'<g id="{sid}"><circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" stroke="{INK}" stroke-width="3"/>'
            f'<ellipse cx="{cx - r * 0.3}" cy="{cy - r * 0.35}" rx="{r * 0.28}" ry="{r * 0.18}" fill="#ffffff" opacity="0.55"/></g>')


def can(cx, cy, w, h, color, sid, lying=False):
    if lying:
        rx = h * 0.18
        return (f'<g id="{sid}"><rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" fill="{color}" stroke="{INK}" stroke-width="3"/>'
                f'<ellipse cx="{cx - w / 2}" cy="{cy}" rx="{rx}" ry="{h / 2}" fill="{_shade(color, 0.8)}" stroke="{INK}" stroke-width="3"/>'
                f'<ellipse cx="{cx + w / 2}" cy="{cy}" rx="{rx}" ry="{h / 2}" fill="{_shade(color, 1.2)}" stroke="{INK}" stroke-width="3"/></g>')
    ry = w * 0.18
    return (f'<g id="{sid}"><rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" fill="{color}" stroke="{INK}" stroke-width="3"/>'
            f'<ellipse cx="{cx}" cy="{cy + h / 2}" rx="{w / 2}" ry="{ry}" fill="{color}" stroke="{INK}" stroke-width="3"/>'
            f'<ellipse cx="{cx}" cy="{cy - h / 2}" rx="{w / 2}" ry="{ry}" fill="{_shade(color, 1.2)}" stroke="{INK}" stroke-width="3"/></g>')


R, B, G, Y = "#e53935", "#1e63d6", "#43a047", "#fbc02d"


def sc(items):
    return scene("".join(i for i in items), [f"i{k}" for k in range(len(items))]) if False else None


def make(parts):
    """parts: list of svg-strings each starting with <g id=..>; ids taken from them"""
    import re
    ids = [re.search(r'id="([^"]+)"', p).group(1) for p in parts]
    return scene("".join(parts), ids)


def trio(a, b, c):
    return make([a, b, c])


THEORY = [
    ("Look at the form, not the color or use", "ننظر إلى الشكل لا إلى اللون أو الاستعمال", "Regarder la forme, pas la couleur ni l'usage", "80", [
        T("Hello! Today we work with things that are not flat on paper. We look at objects that have a form from every side. Do not sort them by color, or by which one is a toy and which one is a box. Look at the form itself. Which objects look alike?",
          "مرحبًا! اليوم نعمل مع أشياء ليست مسطّحة على الورقة. ننظر إلى أشياء لها شكل من كل الجهات. لا ترتّبها حسب اللون ولا حسب أيها لعبة وأيها علبة. انظر إلى الشكل نفسه. أي الأشياء تتشابه؟",
          "Bonjour ! Aujourd'hui on travaille avec des objets qui ne sont pas plats sur le papier. On regarde des objets qui ont une forme de tous les côtés. Ne les trie pas par couleur, ni selon jouet ou boîte. Regarde la forme elle-même. Quels objets se ressemblent ?"),
        make([box(80, 230, 110, R, "a"), box(260, 230, 110, B, "b"), ball(500, 240, 70, G, "c"), can(610, 240, 70, 120, Y, "d")]),
        T("This one is red and this one is blue. Does a different color mean a different form? No. Color is decoration. Two objects can differ in size, color and use, and still have the same solid form.",
          "هذا أحمر وهذا أزرق. هل اختلاف اللون يعني شكلًا مختلفًا؟ لا. اللون زينة. قد يختلف شيئان في الحجم واللون والاستعمال ويكون لهما الشكل المجسّم نفسه.",
          "Celui-ci est rouge, celui-là bleu. Une couleur différente veut-elle dire une forme différente ? Non. La couleur est une décoration. Deux objets peuvent différer par la taille, la couleur et l'usage, et avoir la même forme."),
    ]),
    ("Observe surfaces", "نلاحظ الأسطح", "Observer les surfaces", "80", [
        make([box(110, 280, 150, B, "a"), ball(480, 250, 100, B, "b")]),
        T("Now we look at, or touch, the surfaces. Some models have surfaces that look flat, and some have parts that are curved. We only describe what we see. Look at model A: are all its surfaces like those of model B? This visible description helps us decide whether two forms are the same or different.",
          "الآن ننظر إلى الأسطح أو نلمسها. بعض النماذج أسطحها تبدو مسطّحة، وبعضها فيه أجزاء منحنية. نصف فقط ما نراه. انظر إلى النموذج A: هل كل أسطحه مثل أسطح النموذج B؟ هذا الوصف المرئي يساعدنا على معرفة هل الشكلان نفسه أم مختلفان.",
          "Maintenant on regarde ou on touche les surfaces. Certains modèles ont des surfaces qui paraissent plates, d'autres ont des parties courbes. On décrit seulement ce qu'on voit. Regarde le modèle A : toutes ses surfaces ressemblent-elles à celles de B ? Cette description visible nous aide à savoir si les formes sont pareilles ou différentes."),
    ]),
    ("Turning does not change the solid", "التدوير لا يغيّر المجسّم", "Tourner ne change pas le solide", "81", [
        make([can(180, 240, 100, 170, G, "a"), can(470, 260, 170, 100, G, "b", lying=True)]),
        T("Now I turn the solid. Did it become a new solid just because we changed its orientation? No. It is the same object, seen from another side. If the direction confuses you, turn the model; do not change your sorting.",
          "الآن أدوّر المجسّم. هل صار مجسّمًا جديدًا لمجرد أننا غيّرنا اتجاهه؟ لا. هو الشيء نفسه نراه من جهة أخرى. إذا حيّرك الاتجاه فدوّر النموذج ولا تغيّر تصنيفك.",
          "Maintenant je tourne le solide. Est-il devenu un nouveau solide parce qu'on a changé son orientation ? Non. C'est le même objet vu d'un autre côté. Si la direction te trouble, tourne le modèle ; ne change pas ton classement."),
    ]),
    ("Placing and rolling", "الوضع والتدحرج", "Poser et rouler", "81", [
        make([box(100, 300, 120, B, "a"), ball(430, 260, 80, B, "b")]),
        T("Some forms stay steady when we put them down, and some may move or roll in a different way. We only use what we see. Try, or look: what happens when we place the model like this? What we observe is the evidence; guessing is not.",
          "بعض الأشكال تبقى ثابتة عندما نضعها وبعضها قد يتحرك أو يتدحرج بطريقة مختلفة. نستعمل فقط ما نراه. جرّب أو انظر: ماذا يحدث عندما نضع النموذج هكذا؟ الملاحظة هي الدليل لا التخمين.",
          "Certaines formes restent stables quand on les pose, d'autres peuvent bouger ou rouler autrement. On n'utilise que ce qu'on voit. Essaie ou regarde : que se passe-t-il quand on pose le modèle ainsi ? Ce qu'on observe est la preuve ; deviner n'en est pas une."),
    ]),
    ("Real objects and solid forms", "الأشياء الحقيقية وأشكالها المجسّمة", "Objets réels et formes", "81", [
        make([box(110, 300, 120, Y, "a"), ball(400, 260, 80, R, "b"), can(580, 250, 80, 140, B, "c")]),
        T("Things in life have different uses, but they can share the same geometric form. Which object in life is closest to this model? Say why: because of its visible form, not its color or its use.",
          "للأشياء في الحياة استعمالات مختلفة لكنها قد تشترك في الشكل الهندسي نفسه. أي شيء في الحياة أقرب إلى هذا النموذج؟ قل لماذا: بسبب شكله المرئي لا لونه أو استعماله.",
          "Les objets de la vie ont des usages différents, mais peuvent partager la même forme géométrique. Quel objet de la vie est le plus proche de ce modèle ? Dis pourquoi : à cause de sa forme visible, pas de sa couleur ni de son usage."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Solids are three-dimensional forms that we can see from more than one side. To sort them, we look at the form, turn it if needed, compare the surfaces and visible features, group, and explain. We do not let color, size or use fool us.",
          "المجسّمات أشكال ثلاثية الأبعاد نراها من أكثر من جهة. لنصنّفها ننظر إلى الشكل ونديره إذا لزم ونقارن الأسطح والخصائص المرئية ثم نجمع ونشرح. ولا ندع اللون أو الحجم أو الاستعمال يخدعنا.",
          "Les solides sont des formes en trois dimensions qu'on voit de plusieurs côtés. Pour les trier : regarder la forme, la tourner si besoin, comparer les surfaces et les traits visibles, regrouper, expliquer. On ne se laisse pas tromper par la couleur, la taille ou l'usage."),
        F("LOOK AT THE FORM → ROTATE IF NEEDED → COMPARE → GROUP → EXPLAIN"),
    ]),
]

EXERCISES = [
    EX("1", "80", st("Choose the object whose form matches the target.", "اختر الشيء الذي يطابق شكله الهدف.", "Choisis l'objet dont la forme correspond à la cible."), [
        make([box(60, 180, 100, R, "t"), ball(300, 150, 55, R, "a"), box(400, 180, 80, B, "b"), can(590, 150, 60, 100, R, "c")]),
        T("Ignore the color. Imagine each object if we turned it. Which one keeps the same basic form? The blue one: the color changed, the form did not.",
          "تجاهل اللون. تخيّل كل شيء لو دوّرناه. أيها يحتفظ بالشكل الأساسي نفسه؟ الأزرق: اللون تغيّر والشكل لم يتغيّر.",
          "Ignore la couleur. Imagine chaque objet tourné. Lequel garde la même forme de base ? Le bleu : la couleur a changé, pas la forme."),
    ]),
    EX("2", "80", st("Sort the models by visible form.", "صنّف النماذج حسب شكلها المرئي.", "Trie les modèles selon leur forme visible."), [
        make([box(60, 200, 90, R, "a"), ball(280, 170, 50, B, "b"), box(380, 200, 90, G, "c"), ball(580, 170, 50, Y, "d")]),
        T("Do not use color. Look at the surfaces and the general form. The boxes go together and the balls go together.",
          "لا تستعمل اللون. انظر إلى الأسطح والشكل العام. الصناديق معًا والكرات معًا.",
          "N'utilise pas la couleur. Regarde les surfaces et la forme générale. Les boîtes ensemble, les balles ensemble."),
    ]),
    EX("3", "81", st("Which pictures show the same solid after turning?", "أي الصور تُظهر المجسّم نفسه بعد التدوير؟", "Quelles images montrent le même solide après rotation ?"), [
        make([can(110, 220, 70, 120, G, "a"), can(300, 230, 120, 70, G, "b", lying=True), ball(490, 220, 60, G, "c")]),
        T("The first two are the same solid, turned. The third has a different form. Compare the form, not the direction.",
          "الصورتان الأوليان هما المجسّم نفسه بعد تدويره. الثالثة شكلها مختلف. نقارن الشكل لا الاتجاه.",
          "Les deux premières sont le même solide, tourné. La troisième a une autre forme. Compare la forme, pas la direction."),
    ]),
    EX("4", "81", st("Observe four models and make groups by visible form. Say a simple reason.", "لاحظ أربعة نماذج وكوّن مجموعات حسب الشكل المرئي. قل سببًا بسيطًا.", "Observe quatre modèles et fais des groupes selon la forme visible. Dis une raison simple."), [
        make([box(70, 200, 90, B, "a"), can(280, 170, 60, 110, B, "b"), box(400, 200, 90, R, "c"), can(590, 170, 60, 110, R, "d")]),
        T("Same form, different form, or the same after turning. Color is not a reason.",
          "نفس الشكل أو شكل مختلف أو نفسه بعد التدوير. اللون ليس سببًا.",
          "Même forme, forme différente, ou pareil après rotation. La couleur n'est pas une raison."),
    ]),
    EX("5", "81", st("Match each real object to the solid model with a similar form.", "صل كل شيء حقيقي بالنموذج المجسّم الذي يشبه شكله.", "Associe chaque objet réel au modèle solide de forme semblable."), [
        make([box(90, 250, 110, Y, "a"), ball(360, 220, 70, R, "b"), can(570, 220, 80, 140, G, "c")]),
        T("Imagine the object without its picture or color. What is its form?",
          "تخيّل الشيء بلا صورته ولا لونه. ما شكله؟",
          "Imagine l'objet sans son image ni sa couleur. Quelle est sa forme ?"),
    ]),
    EX("6", "81", st("Error detective: a child grouped two models only because they have the same color, although their forms are different.", "المحقق: طفل جمع نموذجين فقط لأنهما بلون واحد مع أن شكليهما مختلفان.", "Détective : un enfant a groupé deux modèles seulement parce qu'ils ont la même couleur, alors que leurs formes diffèrent."), [
        make([box(110, 280, 120, R, "a"), ball(480, 240, 80, R, "b")]),
        T("Wrong. We must sort by form.",
          "خطأ. يجب أن نصنّف حسب الشكل.",
          "Faux. Il faut trier selon la forme."),
    ]),
    EX("7", "81", st("Challenge: three forms in unusual orientations. Match after imagining a rotation.", "تحدٍّ: ثلاثة أشكال باتجاهات غير مألوفة. طابقها بعد تخيّل التدوير.", "Défi : trois formes dans des orientations inhabituelles. Associe-les après avoir imaginé une rotation."), [
        make([can(110, 230, 120, 70, B, "a", lying=True), box(300, 260, 90, G, "b"), can(540, 230, 60, 120, B, "c")]),
        T("Ignore the direction. Compare the surfaces and the general form. Rotation did not change identity.",
          "تجاهل الاتجاه. قارن الأسطح والشكل العام. التدوير لم يغيّر الهوية.",
          "Ignore la direction. Compare les surfaces et la forme générale. La rotation n'a pas changé l'identité."),
    ]),
    EX("8", "81", st("Final check: why do two objects with the same form match even if the color and the use differ?", "تقييم أخير: لماذا يتطابق شيئان لهما الشكل نفسه حتى لو اختلف اللون والاستعمال؟", "Évaluation : pourquoi deux objets de même forme correspondent-ils même si la couleur et l'usage diffèrent ?"), [
        make([box(110, 270, 110, R, "a"), box(380, 250, 150, B, "b")]),
        T("Because the form is what counts in geometry, not the color or the use. If you give a reason from the form, you understood.",
          "لأن الشكل هو المهم في الهندسة لا اللون ولا الاستعمال. إذا ذكرت سببًا من الشكل فقد فهمت.",
          "Parce qu'en géométrie c'est la forme qui compte, pas la couleur ni l'usage. Si tu donnes une raison tirée de la forme, tu as compris."),
    ]),
]
