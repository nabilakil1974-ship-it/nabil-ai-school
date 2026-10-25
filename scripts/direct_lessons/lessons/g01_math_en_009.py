"""Grade 1 Mathematics — Lines (following and drawing paths)."""
from scripts.direct_lessons.common import T, F, D, EX, st, S, scene

LESSON_ID = "G01-MATH-EN-009"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Lines", "ar": "الخطوط", "fr": "Les lignes"}


def path(d, pid, color="#1e63d6", w=10):
    return f'<path id="{pid}" d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'


def dot(x, y, pid, color):
    return f'<circle id="{pid}" cx="{x}" cy="{y}" r="22" fill="{color}" stroke="#0b3d5c" stroke-width="3"/>'


def lab(txt, x, y, pid):
    return (f'<text id="{pid}" x="{x}" y="{y}" font-size="30" font-weight="700" text-anchor="middle" '
            f'fill="#0b3d5c" font-family="sans-serif">{txt}</text>')


STRAIGHT = "M 90 230 L 570 230"
CURVE = "M 90 300 C 200 90, 330 90, 400 220 S 520 340, 570 150"
TURN = "M 100 340 L 100 140 L 330 140 L 330 300 L 560 300"

THEORY = [
    ("A path has a start and an end", "للمسار بداية ونهاية", "Un chemin a un départ et une arrivée", "32", [
        T("Hello! Today we do not count. We work with our hand and our eyes together. Look: a mouse and a cheese, and a path between them.",
          "مرحبًا! اليوم لا نعدّ، بل نعمل بيدنا وعيننا معًا. انظر: فأر وقطعة جبن وبينهما مسار.",
          "Bonjour ! Aujourd'hui, on ne compte pas : on travaille avec la main et les yeux. Regarde : une souris, un fromage et un chemin entre les deux."),
        scene(path(CURVE, "p1") + dot(90, 300, "s1", "#9e9e9e") + dot(570, 150, "e1", "#fdd835") + lab("start", 90, 360, "t1") + lab("end", 570, 110, "t2"),
              ["p1", "s1", "e1", "t1", "t2"]),
        T("The mouse starts here and must reach the cheese. Where is the start? Where is the end? Before we move, we always find both.",
          "يبدأ الفأر من هنا ويجب أن يصل إلى الجبن. أين البداية؟ وأين النهاية؟ قبل أن نتحرك نجد دائمًا الاثنين.",
          "La souris part d'ici et doit atteindre le fromage. Où est le départ ? Où est l'arrivée ? Avant de bouger, on cherche toujours les deux."),
        T("We do not begin in the middle of the line. We know the start and the end.",
          "لا نبدأ من منتصف الخط. نعرف البداية والنهاية.",
          "On ne commence pas au milieu de la ligne. On connaît le départ et l'arrivée."),
    ]),
    ("Follow the path without stopping", "نتبع المسار دون انقطاع", "Suivre le chemin sans s'arrêter", "32", [
        scene(path(STRAIGHT, "q1") + dot(90, 230, "q2", "#9e9e9e") + dot(570, 230, "q3", "#fdd835"), ["q1", "q2", "q3"]),
        T("When we trace a line, we try not to lift the finger again and again. Start here, keep going, and go on until the end. The line is not broken in the middle.",
          "عندما نتتبّع خطًّا نحاول ألا نرفع الإصبع كل لحظة. نبدأ من هنا ونكمل حتى النهاية. الخط لا ينقطع في الوسط.",
          "Quand on suit une ligne, on essaie de ne pas lever le doigt à chaque instant. On part d'ici, on continue jusqu'à l'arrivée. La ligne ne s'arrête pas au milieu."),
        T("Accuracy matters more than speed. Go slowly, so you do not leave the path.",
          "الدقّة أهمّ من السرعة. نمشي ببطء حتى لا نخرج عن المسار.",
          "La précision compte plus que la vitesse. On va doucement pour ne pas sortir du chemin."),
    ]),
    ("Watch the direction: turns", "ننتبه إلى الاتجاه: المنعطفات", "Faire attention à la direction : les virages", "33", [
        scene(path(TURN, "r1") + dot(100, 340, "r2", "#9e9e9e") + dot(560, 300, "r3", "#fdd835"), ["r1", "r2", "r3"]),
        T("Not every line goes the same way. This path goes up first, then it turns. What must we do? We turn with the line.",
          "ليست كل الخطوط تسير بالطريقة نفسها. هذا المسار يصعد أولًا ثم ينعطف. ماذا نفعل؟ نلتفّ مع الخط.",
          "Toutes les lignes ne vont pas pareil. Ce chemin monte d'abord, puis tourne. Que faire ? On tourne avec la ligne."),
        T("Before a turn we slow down and look ahead. We do not continue straight when the line changes direction.",
          "قبل المنعطف نخفّف السرعة وننظر إلى الأمام. لا نكمل مستقيمًا إذا غيّر الخط اتجاهه.",
          "Avant un virage, on ralentit et on regarde devant. On ne continue pas tout droit quand la ligne change de direction."),
    ]),
    ("Different paths look different", "المسارات المختلفة تبدو مختلفة", "Des chemins différents se ressemblent peu", "33", [
        scene(path("M 60 100 L 600 100", "a1", "#1e63d6") + path("M 60 220 C 200 140, 320 300, 600 220", "a2", "#e53935") + path("M 60 360 L 200 360 L 200 300 L 400 300 L 400 380 L 600 380", "a3", "#43a047"),
              ["a1", "a2", "a3"]),
        T("Look at three paths. One is straight. One is curved. One changes direction several times. They do not look the same.",
          "انظر إلى ثلاثة مسارات. أحدها مستقيم، وآخر منحنٍ، وآخر يغيّر اتجاهه عدة مرات. ليست متشابهة.",
          "Regarde trois chemins. L'un est droit, l'autre courbe, le troisième change plusieurs fois de direction. Ils ne se ressemblent pas."),
        T("We do not need big geometry words now. We only need to see the difference and follow each path correctly.",
          "لا نحتاج الآن إلى كلمات هندسية كبيرة. يكفي أن نرى الفرق ونتبع كل مسار بشكل صحيح.",
          "On n'a pas besoin de grands mots de géométrie. Il suffit de voir la différence et de suivre chaque chemin correctement."),
    ]),
    ("Trace first, then draw the same line", "نتتبّع أولًا ثم نرسم الخط نفسه", "D'abord suivre, puis dessiner la même ligne", "33", [
        scene(path(TURN, "m1", "#9e9e9e", 8), ["m1"]),
        T("First we trace the model. Where does it start? Where does it change direction? Where does it end?",
          "نتتبّع النموذج أولًا. أين يبدأ؟ أين يغيّر الاتجاه؟ أين ينتهي؟",
          "D'abord on suit le modèle. Où commence-t-il ? Où change-t-il de direction ? Où finit-il ?"),
        scene(path(TURN, "m2", "#e53935", 10), ["m2"]),
        T("Now we draw a similar line next to it. It must look like the original in direction and shape. Then we compare and fix any part that is different.",
          "الآن نرسم خطًّا مشابهًا بجانبه. يجب أن يشبه الأصل في الاتجاه والشكل. ثم نقارن ونصلح أي جزء مختلف.",
          "Maintenant on dessine à côté une ligne semblable. Elle doit ressembler à l'original par la direction et la forme. Puis on compare et on corrige."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        F("FIND START → LOOK AHEAD → FOLLOW THE PATH → TURN WHEN IT TURNS → REACH THE END → CHECK THE MODEL"),
        T("To draw a line like a model: trace first, observe, draw, compare, and fix. Accuracy is more important than speed.",
          "لرسم خط مثل النموذج: نتتبّع أولًا، ثم نلاحظ، ثم نرسم، ثم نقارن ونصلح. الدقّة أهمّ من السرعة.",
          "Pour dessiner une ligne comme le modèle : suivre, observer, dessiner, comparer, corriger. La précision compte plus que la vitesse."),
    ]),
]

EXERCISES = [
    EX("1", "32", st("Find the start and the end of the path from the car to the house.", "جد بداية المسار ونهايته من السيارة إلى البيت.", "Trouve le départ et l'arrivée du chemin entre la voiture et la maison."), [
        scene(path(CURVE, "z1") + dot(90, 300, "z2", "#1e63d6") + dot(570, 150, "z3", "#e53935") + lab("car", 90, 360, "z4") + lab("house", 570, 110, "z5"),
              ["z1", "z2", "z3", "z4", "z5"]),
        T("The car is the one that moves, so the car is the start. The house is the end.",
          "السيارة هي التي تتحرّك، إذن السيارة هي البداية والبيت هو النهاية.",
          "La voiture est celle qui bouge : c'est le départ. La maison est l'arrivée."),
        T("Now we trace from the car to the house with the finger.",
          "الآن نتتبّع من السيارة إلى البيت بالإصبع.",
          "Maintenant on suit le chemin du doigt, de la voiture à la maison."),
    ]),
    EX("2", "32", st("Trace the curved path without leaving it.", "تتبّع المسار المنحني دون الخروج منه.", "Suis le chemin courbe sans en sortir."), [
        scene(path(CURVE, "c1") + dot(90, 300, "c2", "#9e9e9e") + dot(570, 150, "c3", "#fdd835"), ["c1", "c2", "c3"]),
        T("Put the finger on the start and go slowly. If you leave the path, stop, go back to that point and try slower.",
          "ضع إصبعك على البداية وامشِ ببطء. إذا خرجت عن المسار فتوقّف وارجع إلى تلك النقطة وجرّب بشكل أبطأ.",
          "Mets le doigt sur le départ et avance doucement. Si tu sors du chemin, arrête-toi, reviens à ce point et essaie plus lentement."),
    ]),
    EX("3", "33", st("Follow the path that has a clear turn.", "اتبع المسار الذي فيه منعطف واضح.", "Suis le chemin qui a un virage net."), [
        scene(path(TURN, "t1") + dot(100, 340, "t2", "#9e9e9e") + dot(560, 300, "t3", "#fdd835"), ["t1", "t2", "t3"]),
        T("Before the turn we ask: what comes next? A turn. So we slow down and follow the new direction.",
          "قبل المنعطف نسأل: ماذا سيأتي؟ منعطف. لذلك نخفّف السرعة ونتابع الاتجاه الجديد.",
          "Avant le virage on se demande : qu'est-ce qui vient ? Un virage. On ralentit et on suit la nouvelle direction."),
    ]),
    EX("4", "33", st("Which path has the same shape as the model: A straight, B curved, C with turns?", "أي مسار يطابق شكل النموذج: A مستقيم، B منحنٍ، C فيه منعطفات؟", "Quel chemin a la même forme que le modèle : A droit, B courbe, C avec des virages ?"), [
        scene(path(TURN, "n1", "#9e9e9e", 8), ["n1"]),
        T("The model goes up, then turns right, then goes down, then turns right again. Compare from the start to the first turn, then compare the end.",
          "النموذج يصعد ثم ينعطف يمينًا ثم ينزل ثم ينعطف يمينًا مرة أخرى. نقارن من البداية إلى أول منعطف ثم نقارن النهاية.",
          "Le modèle monte, tourne à droite, descend, puis tourne encore à droite. On compare du départ au premier virage, puis la fin."),
        F("The answer is C."),
        T("C has the same turns, in the same order.",
          "للمسار C المنعطفات نفسها بالترتيب نفسه.",
          "C a les mêmes virages dans le même ordre."),
    ]),
    EX("5", "33", st("Reproduce the model line.", "أعد رسم الخط النموذجي.", "Reproduis la ligne modèle."), [
        scene(path("M 100 300 L 100 140 L 300 140 L 300 300", "k1", "#9e9e9e", 8), ["k1"]),
        T("Look at the model for three seconds: it starts at the bottom left, goes up, turns right, then goes down. Now draw it.",
          "انظر إلى النموذج ثلاث ثوانٍ: يبدأ من أسفل اليسار ويصعد ثم ينعطف يمينًا ثم ينزل. الآن ارسمه.",
          "Regarde le modèle trois secondes : il part en bas à gauche, monte, tourne à droite, puis descend. Maintenant, dessine-le."),
        scene(path("M 360 300 L 360 140 L 560 140 L 560 300", "k2", "#e53935", 10), ["k2"]),
        T("We put our drawing next to the model and compare. If a turn comes too early, we fix that part.",
          "نضع رسمنا بجانب النموذج ونقارن. إذا جاء منعطف مبكرًا نصلح ذلك الجزء.",
          "On met notre dessin à côté du modèle et on compare. Si un virage est trop tôt, on corrige cette partie."),
    ]),
    EX("6", "33", st("Error detective: one part of the student's line does not look like the model.", "المحقق: جزء واحد من خط الطالب لا يشبه النموذج.", "Détective : une partie de la ligne de l'élève ne ressemble pas au modèle."), [
        scene(path(TURN, "e1", "#9e9e9e", 8) + path("M 100 340 L 100 140 L 330 140 L 330 300 L 330 420", "e2", "#e53935", 8), ["e1", "e2"]),
        T("The last turn went the wrong way: the red line should turn right after going down, but it kept going down.",
          "المنعطف الأخير ذهب في الاتجاه الخاطئ: كان يجب أن يلتفّ الخط الأحمر يمينًا بعد النزول، لكنه تابع النزول.",
          "Le dernier virage est parti du mauvais côté : la ligne rouge devait tourner à droite après la descente, mais elle a continué."),
        T("We fix only that part.",
          "نصلح هذا الجزء فقط.",
          "On corrige seulement cette partie."),
    ]),
    EX("7", "33", st("Challenge: which of two paths reaches the goal with the same sequence as the model?", "تحدٍّ: أي مسارين يصل إلى الهدف بالتسلسل نفسه للنموذج؟", "Défi : lequel des deux chemins atteint le but avec la même suite que le modèle ?"), [
        T("We watch: start, direction, turns, end. Compare the first turn, then compare the last direction.",
          "نراقب: البداية، الاتجاه، المنعطفات، النهاية. نقارن أول منعطف ثم آخر اتجاه.",
          "On observe : départ, direction, virages, arrivée. On compare le premier virage, puis la dernière direction."),
        F("start → direction → turns → end"),
        T("The path with the same turns in the same order is the answer.",
          "المسار الذي له المنعطفات نفسها بالترتيب نفسه هو الجواب.",
          "Le chemin qui a les mêmes virages dans le même ordre est la bonne réponse."),
    ]),
    EX("8", "33", st("What do you do first before drawing a line like the model?", "ماذا تفعل أولًا قبل رسم خط مثل النموذج؟", "Que fais-tu d'abord avant de dessiner une ligne comme le modèle ?"), [
        T("We look at the start, the direction, the turns and the end.",
          "ننظر إلى البداية والاتجاه والمنعطفات والنهاية.",
          "On regarde le départ, la direction, les virages et l'arrivée."),
        F("LOOK → START → FOLLOW → TURN → END → CHECK"),
    ]),
]
