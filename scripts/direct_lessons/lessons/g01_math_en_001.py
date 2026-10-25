"""Grade 1 Mathematics — Positioning (golden lesson G01-MATH-EN-001)."""
from scripts.direct_lessons.common import T, F, D, EX, st, S

LESSON_ID = "G01-MATH-EN-001"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Positioning", "ar": "تحديد المواقع", "fr": "Se situer dans l'espace"}

_RED = '<rect id="r" x="250" y="{ry}" width="120" height="100" fill="#e53935" stroke="#0b3d5c" stroke-width="4"/>'
_BLUE = '<rect id="b" x="250" y="{by}" width="120" height="100" fill="#1e63d6" stroke="#0b3d5c" stroke-width="4"/>'


def two_cubes(red_y, blue_y):
    return (_RED.format(ry=red_y) + _BLUE.format(by=blue_y))


def lab(text, x, y, tid):
    return f'<text id="{tid}" x="{x}" y="{y}" font-size="28" fill="#0b3d5c" font-family="sans-serif">{text}</text>'


THEORY = [
    ("Above and below", "فوق وتحت", "Au-dessus et en dessous", "11", [
        T("Hello! Today we play, move things and discover where everything is.",
          "مرحبًا! اليوم نلعب ونحرّك الأشياء ونكتشف معًا أين يوجد كل شيء.",
          "Bonjour ! Aujourd'hui, on joue, on déplace des objets et on découvre où se trouve chaque chose."),
        D("svgScene", svg=two_cubes(60, 240), vb=[660, 440], show=["r", "b"]),
        T("Look at the red cube and the blue cube. The red cube is above the blue cube.",
          "انظر إلى المكعب الأحمر والمكعب الأزرق. المكعب الأحمر فوق المكعب الأزرق.",
          "Regarde le cube rouge et le cube bleu. Le cube rouge est au-dessus du cube bleu."),
        F("The red cube is above the blue cube."),
        T("Why do we say above? Because the red cube is higher than the blue cube.",
          "لماذا نقول فوق؟ لأن المكعب الأحمر أعلى من المكعب الأزرق.",
          "Pourquoi dit-on au-dessus ? Parce que le cube rouge est plus haut que le cube bleu."),
        D("svgScene", svg=two_cubes(240, 60), vb=[660, 440], show=["r", "b"]),
        T("Now the red cube moved. It is lower than the blue cube. The red cube is below the blue cube.",
          "الآن تحرّك المكعب الأحمر وصار أخفض من الأزرق. المكعب الأحمر تحت المكعب الأزرق.",
          "Maintenant le cube rouge a bougé. Il est plus bas que le cube bleu. Le cube rouge est en dessous du cube bleu."),
        F("The red cube is below the blue cube."),
        T("The word changes when the place of the object changes. Position tells where something is compared with something else.",
          "تتغيّر الكلمة عندما يتغيّر مكان الشيء. الموقع يخبرنا أين يوجد شيء بالنسبة إلى شيء آخر.",
          "Le mot change quand la place de l'objet change. La position dit où se trouve une chose par rapport à une autre."),
    ]),
    ("We need a reference object", "نحتاج إلى شيء نقارن به", "Il faut un objet de référence", "12", [
        T("Where is the red cube? You may say: here. But that is not a good answer.",
          "أين المكعب الأحمر؟ قد تقول: هنا. لكنه ليس جوابًا دقيقًا.",
          "Où est le cube rouge ? Tu peux dire : ici. Mais ce n'est pas une réponse précise."),
        D("svgScene", svg=_RED.format(ry=150), vb=[660, 440], show=["r"]),
        T("A blue cube appears. Now we can ask a clear question: where is the red cube compared with the blue cube?",
          "ظهر مكعب أزرق. الآن نستطيع طرح سؤال واضح: أين المكعب الأحمر بالنسبة إلى المكعب الأزرق؟",
          "Un cube bleu apparaît. On peut poser une question claire : où est le cube rouge par rapport au cube bleu ?"),
        D("svgScene", svg=two_cubes(60, 240), vb=[660, 440], show=["r", "b"]),
        T("To describe a position we need a second object to compare with. It is the reference object.",
          "لوصف الموقع نحتاج إلى شيء ثانٍ نقارن به. إنه الشيء المرجعي.",
          "Pour décrire une position, il faut un deuxième objet de comparaison : l'objet de référence."),
        T("Remember one question: which object am I comparing with?",
          "تذكّر سؤالًا واحدًا: مع أي شيء أقارن؟",
          "Retiens une seule question : avec quel objet est-ce que je compare ?"),
    ]),
    ("Inside and outside", "داخل وخارج", "Dans et en dehors", "13", [
        T("Look at the pencil. It is outside the pencil case.",
          "انظر إلى القلم. إنه خارج المقلمة.",
          "Regarde le crayon. Il est en dehors de la trousse."),
        D("svgScene", svg='<rect id="case" x="320" y="200" width="260" height="110" fill="#ffe08a" stroke="#0b3d5c" stroke-width="4"/>'
          '<line id="pen" x1="60" y1="150" x2="250" y2="150" stroke="#2e7d32" stroke-width="12"/>', vb=[660, 440], show=["case", "pen"]),
        F("The pencil is outside the pencil case."),
        T("Now the pencil is in the pencil case. It is inside.",
          "الآن صار القلم في المقلمة. إنه داخل المقلمة.",
          "Maintenant le crayon est dans la trousse. Il est à l'intérieur."),
        D("svgScene", svg='<rect id="case2" x="320" y="200" width="260" height="110" fill="#ffe08a" stroke="#0b3d5c" stroke-width="4"/>'
          '<line id="pen2" x1="350" y1="255" x2="550" y2="255" stroke="#2e7d32" stroke-width="12"/>', vb=[660, 440], show=["case2", "pen2"]),
        F("The pencil is inside the pencil case."),
        T("Inside means in the middle of something. Outside means not inside.",
          "داخل تعني أنه في جوف الشيء. وخارج تعني أنه ليس في جوفه.",
          "Dans veut dire à l'intérieur de quelque chose. En dehors veut dire pas à l'intérieur."),
    ]),
    ("Left and right: reverse the question", "اليمين واليسار: نعكس السؤال", "Gauche et droite : on inverse la question", "14", [
        T("The ball is to the left of the chair.",
          "الكرة على يسار الكرسي.",
          "Le ballon est à gauche de la chaise."),
        D("svgScene", svg='<circle id="ball" cx="170" cy="260" r="55" fill="#ff9800" stroke="#0b3d5c" stroke-width="4"/>'
          '<rect id="chair" x="400" y="190" width="110" height="130" fill="#8d6e63" stroke="#0b3d5c" stroke-width="4"/>', vb=[660, 440], show=["ball", "chair"]),
        F("The ball is to the left of the chair."),
        T("Now we reverse the question. Where is the chair compared with the ball? Look at the chair first, then at the ball.",
          "الآن نعكس السؤال. أين الكرسي بالنسبة إلى الكرة؟ انظر إلى الكرسي أولًا ثم إلى الكرة.",
          "Maintenant on inverse la question. Où est la chaise par rapport au ballon ? Regarde d'abord la chaise, puis le ballon."),
        F("The chair is to the right of the ball."),
        T("When we change what we describe and what we compare with, the answer can change.",
          "عندما نغيّر ما نصفه وما نقارن به، قد يتغيّر الجواب.",
          "Quand on change ce qu'on décrit et ce à quoi on compare, la réponse peut changer."),
    ]),
    ("My five steps", "خطواتي الخمس", "Mes cinq étapes", "", [
        T("Each time we answer a position question, we follow five steps.",
          "في كل مرة نجيب عن سؤال موقع نتبع خمس خطوات.",
          "À chaque question de position, on suit cinq étapes."),
        F("LOOK → POINT → COMPARE → SAY → CHECK"),
        T("LOOK carefully. POINT to the object we talk about. COMPARE: point to the object we compare with. SAY where it is. CHECK the picture again.",
          "انظر جيدًا. أشر إلى الشيء الذي نتحدث عنه. قارن: أشر إلى الشيء الذي نقارن به. قل أين يوجد. ثم تحقّق بالنظر إلى الصورة.",
          "REGARDE bien. MONTRE l'objet dont on parle. COMPARE : montre l'objet de comparaison. DIS où il est. VÉRIFIE avec l'image."),
        T("We do not guess. We look, think and answer.",
          "نحن لا نخمّن. ننظر ونفكّر ثم نجيب.",
          "On ne devine pas. On regarde, on réfléchit et on répond."),
    ]),
]


def _two(a_y, b_y):
    return two_cubes(a_y, b_y)


EXERCISES = [
    EX("1", "11", st("Put the ball above the box and say the sentence.", "ضع الكرة فوق الصندوق وقل الجملة.", "Place le ballon au-dessus de la boîte et dis la phrase."), [
        D("svgScene", svg='<rect id="box" x="240" y="250" width="180" height="110" fill="#bcaaa4" stroke="#0b3d5c" stroke-width="4"/>'
          '<circle id="bl" cx="330" cy="190" r="50" fill="#ff9800" stroke="#0b3d5c" stroke-width="4"/>', vb=[660, 440], show=["box", "bl"]),
        T("First look at the box: it is our reference. Then put the ball higher than the box.",
          "انظر أولًا إلى الصندوق: إنه الشيء الذي نقارن به. ثم ضع الكرة أعلى من الصندوق.",
          "Regarde d'abord la boîte : c'est notre référence. Puis place le ballon plus haut que la boîte."),
        F("The ball is above the box."),
        T("Why above? Because the ball is higher than the box.",
          "لماذا فوق؟ لأن الكرة أعلى من الصندوق.",
          "Pourquoi au-dessus ? Parce que le ballon est plus haut que la boîte."),
    ]),
    EX("2", "11", st("Where is the cat compared with the table?", "أين القطة بالنسبة إلى الطاولة؟", "Où est le chat par rapport à la table ?"), [
        D("svgScene", svg='<rect id="tb" x="180" y="150" width="300" height="30" fill="#8d6e63" stroke="#0b3d5c" stroke-width="4"/>'
          '<line id="l1" x1="200" y1="180" x2="200" y2="330" stroke="#0b3d5c" stroke-width="8"/>'
          '<line id="l2" x1="460" y1="180" x2="460" y2="330" stroke="#0b3d5c" stroke-width="8"/>'
          '<ellipse id="cat" cx="330" cy="290" rx="60" ry="35" fill="#9e9e9e" stroke="#0b3d5c" stroke-width="4"/>', vb=[660, 440], show=["tb", "l1", "l2", "cat"]),
        T("Point to the cat: it is what we describe. Point to the table: it is what we compare with.",
          "أشر إلى القطة: إنها ما نصفه. وأشر إلى الطاولة: إنها ما نقارن به.",
          "Montre le chat : c'est ce qu'on décrit. Montre la table : c'est ce qu'on compare."),
        T("The cat is lower than the table.",
          "القطة أخفض من الطاولة.",
          "Le chat est plus bas que la table."),
        F("The cat is below the table."),
        T("Check: the sentence matches the picture.",
          "نتحقق: الجملة تطابق الصورة.",
          "Vérification : la phrase correspond à l'image."),
    ]),
    EX("3", "12", st("Inside or outside? Put the pencil outside the pencil case.", "داخل أم خارج؟ أخرج القلم من المقلمة.", "Dedans ou dehors ? Mets le crayon en dehors de la trousse."), [
        T("The pencil must not be in the case. We move it out.",
          "يجب ألا يكون القلم في المقلمة. نُخرجه منها.",
          "Le crayon ne doit pas être dans la trousse. On le sort."),
        F("The pencil is outside the pencil case."),
    ]),
    EX("4", "13", st("Where is the toy compared with the shelf?", "أين اللعبة بالنسبة إلى الرف؟", "Où est le jouet par rapport à l'étagère ?"), [
        T("What do we describe? The toy. What do we compare with? The shelf.",
          "ماذا نصف؟ اللعبة. وبماذا نقارن؟ بالرف.",
          "Que décrit-on ? Le jouet. Avec quoi compare-t-on ? L'étagère."),
        T("The toy is lower than the shelf.",
          "اللعبة أخفض من الرف.",
          "Le jouet est plus bas que l'étagère."),
        F("The toy is below the shelf."),
        T("Check: the sentence matches the picture. Yes.",
          "نتحقق: الجملة تطابق الصورة. نعم.",
          "Vérification : la phrase correspond à l'image. Oui."),
    ]),
    EX("5", "13", st("Where is the cup compared with the cupboard?", "أين الكوب بالنسبة إلى الخزانة؟", "Où est la tasse par rapport au placard ?"), [
        T("The cup is in the cupboard.",
          "الكوب موجود في جوف الخزانة.",
          "La tasse est dans le placard."),
        F("The cup is inside the cupboard."),
        T("If we take the cup out, it is no longer inside, because its position changed.",
          "لو أخرجنا الكوب فلن يبقى داخل الخزانة، لأن موقعه تغيّر.",
          "Si on sort la tasse, elle n'est plus dedans, car sa position a changé."),
    ]),
    EX("6", "14", st("The child stands to the right of the tree. Where is the tree compared with the child?", "الطفل يقف على يمين الشجرة. أين الشجرة بالنسبة إلى الطفل؟", "L'enfant est à droite de l'arbre. Où est l'arbre par rapport à l'enfant ?"), [
        T("The question is about the tree, not about the child. Point to the tree first, then to the child.",
          "السؤال عن الشجرة وليس عن الطفل. أشر إلى الشجرة أولًا ثم إلى الطفل.",
          "La question porte sur l'arbre, pas sur l'enfant. Montre d'abord l'arbre, puis l'enfant."),
        T("The child is on the right of the tree, so the tree is on the left of the child.",
          "الطفل على يمين الشجرة، إذن الشجرة على يسار الطفل.",
          "L'enfant est à droite de l'arbre, donc l'arbre est à gauche de l'enfant."),
        F("The tree is to the left of the child."),
    ]),
    EX("7", "14", st("Error detective: the ball is below the chair. Which sentence is true?", "المحقق: الكرة تحت الكرسي. أي جملة صحيحة؟", "Détective : le ballon est sous la chaise. Quelle phrase est vraie ?"), [
        F("A. The ball is below the chair."),
        F("B. The ball is above the chair."),
        F("C. The chair is below the ball."),
        T("A is true: the ball is lower than the chair.",
          "الجملة A صحيحة: الكرة أخفض من الكرسي.",
          "A est vraie : le ballon est plus bas que la chaise."),
        T("B is false: the ball is not higher than the chair. C is false: the chair is higher, so it is above the ball.",
          "الجملة B خاطئة: الكرة ليست أعلى من الكرسي. والجملة C خاطئة: الكرسي هو الأعلى، فهو فوق الكرة.",
          "B est fausse : le ballon n'est pas plus haut que la chaise. C est fausse : la chaise est plus haute, elle est au-dessus du ballon."),
    ]),
    EX("8", "15", st("The yellow block is above the red block. The blue block is below the red block. Which block is highest? Which is lowest? Where is the red block compared with the yellow block?",
                      "المكعب الأصفر فوق الأحمر، والأزرق تحت الأحمر. أي مكعب هو الأعلى؟ وأيها الأخفض؟ وأين الأحمر بالنسبة إلى الأصفر؟",
                      "Le bloc jaune est au-dessus du rouge. Le bloc bleu est en dessous du rouge. Quel bloc est le plus haut ? Le plus bas ? Où est le rouge par rapport au jaune ?"), [
        D("svgScene", svg='<rect id="y" x="270" y="40" width="120" height="100" fill="#fdd835" stroke="#0b3d5c" stroke-width="4"/>'
          '<rect id="rd" x="270" y="150" width="120" height="100" fill="#e53935" stroke="#0b3d5c" stroke-width="4"/>'
          '<rect id="bu" x="270" y="260" width="120" height="100" fill="#1e63d6" stroke="#0b3d5c" stroke-width="4"/>', vb=[660, 440], show=["y", "rd", "bu"]),
        F("Highest: the yellow block."),
        F("Lowest: the blue block."),
        F("The red block is below the yellow block."),
    ]),
    EX("9", "15", st("Star above circle, circle above square: which shape is highest?", "النجمة فوق الدائرة والدائرة فوق المربع: أي شكل هو الأعلى؟", "L'étoile est au-dessus du cercle, le cercle au-dessus du carré : quelle forme est la plus haute ?"), [
        T("Start from the circle: something is above it and something is below it.",
          "نبدأ من الدائرة: يوجد شيء فوقها وشيء تحتها.",
          "Commençons par le cercle : il y a quelque chose au-dessus et quelque chose en dessous."),
        T("The star is above the circle, and nothing is above the star. So the star is the highest.",
          "النجمة فوق الدائرة ولا شيء فوق النجمة، إذن النجمة هي الأعلى.",
          "L'étoile est au-dessus du cercle et rien n'est au-dessus de l'étoile : l'étoile est la plus haute."),
        F("The star is the highest."),
    ]),
]
