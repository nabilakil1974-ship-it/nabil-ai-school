"""Grade 2 Mathematics — Segment."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G02-MATH-EN-005"
GRADE = 2
SUBJECT = "math"
TITLES = {"en": "Segment", "ar": "القطعة المستقيمة", "fr": "Le segment"}


def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}


QUIZ = [
    {"q": "What is a segment?", "opts": ["A straight part joining two endpoints", "A curved path between two points", "A closed round shape", "A single point"], "a": 0,
     "why": {"A curved path between two points": _w("A segment is straight, never curved.", "القطعة المستقيمة مستقيمة وليست منحنية.", "Un segment est droit, jamais courbe."),
             "A closed round shape": _w("A segment is a straight line part with two ends.", "هي جزء مستقيم له نهايتان.", "C'est un trait droit avec deux extrémités."),
             "A single point": _w("A segment needs two endpoints.", "تحتاج القطعة إلى نقطتي نهاية.", "Un segment a deux extrémités.")}, "ok": "straight with two endpoints"},
    {"q": "We draw a segment so that the red point P is an endpoint. Where is P?", "opts": ["At one end of the segment", "In the middle", "Far from the segment", "On a curve"], "a": 0,
     "why": {"In the middle": _w("In the middle it only passes through P.", "في المنتصف تمر بالنقطة فقط.", "Au milieu, il passe seulement par P."),
             "Far from the segment": _w("P must touch the segment.", "يجب أن تلمس P القطعة.", "P doit toucher le segment."),
             "On a curve": _w("A segment is straight.", "القطعة مستقيمة.", "Un segment est droit.")}, "ok": "P is at one end"},
    {"q": "We have 3 points A, B, C. How many segments join every pair?", "opts": ["3", "2", "6", "1"], "a": 0,
     "why": {"2": _w("List them: A–B, A–C, B–C.", "اكتبها: A–B وA–C وB–C.", "Liste : A–B, A–C, B–C."),
             "6": _w("A–B and B–A are the same segment, so draw it once.", "A–B وB–A هما القطعة نفسها.", "A–B et B–A sont le même segment."),
             "1": _w("There are three pairs.", "هناك ثلاثة أزواج.", "Il y a trois paires.")}, "ok": "A–B, A–C, B–C"},
]

THEORY = [
    ("What is a segment?", "ما هي القطعة المستقيمة؟", "Qu'est-ce qu'un segment ?", "20", [
        T("Hello, champion! Look: there is a point here, a point there, and a straight line between them. This is called a segment. The two points where it stops are its endpoints. So a segment is straight and has two endpoints.",
          "مرحبًا يا بطل! انظر: هنا نقطة وهناك نقطة وبينهما خط مستقيم. هذه تُسمّى قطعة مستقيمة. النقطتان اللتان تقف عندهما هما نهايتاها. إذن القطعة مستقيمة ولها نهايتان.",
          "Bonjour champion ! Ici un point, là un point, et entre eux un trait droit : c'est un segment. Les deux points où il s'arrête sont ses extrémités. Un segment est droit et a deux extrémités."),
        F("point → straight path → point"),
        T("If you draw a curve between two points, it is not a segment. Trace the straight path in the air with your finger.",
          "إذا رسمت خطًا منحنيًا بين نقطتين فهو ليس قطعة مستقيمة. ارسم المسار المستقيم في الهواء بإصبعك.",
          "Une courbe entre deux points n'est pas un segment. Trace le chemin droit dans l'air avec ton doigt."),
    ]),
    ("The ruler helps us", "المسطرة تساعدنا", "La règle nous aide", "20", [
        T("The ruler is not only for measuring. Here we use it to make the line straight. Follow these steps: put the ruler so its edge passes through both points, hold it firmly, draw along the edge, and stop exactly at the endpoint.",
          "المسطرة ليست للقياس فقط. هنا نستعملها لنجعل الخط مستقيمًا. الخطوات: ضع المسطرة بحيث تمر حافتها بالنقطتين، أمسكها جيدًا، ارسم على الحافة، وقف تمامًا عند نقطة النهاية.",
          "La règle ne sert pas qu'à mesurer. Ici elle rend le trait droit : place son bord sur les deux points, tiens-la bien, trace le long du bord et arrête-toi exactement à l'extrémité."),
        F("align → hold → draw → stop"),
    ]),
    ("Same colour, pass through, endpoint", "اللون نفسه، المرور، نقطة النهاية", "Même couleur, passer par, extrémité", "20", [
        T("To join points of the same colour, we do not join the nearest points. We join pink to pink, green to green, red to red, blue to blue and purple to purple, each with one straight segment.",
          "لوصل نقاط من اللون نفسه لا نصل أقرب نقطتين، بل نصل الوردي بالوردي والأخضر بالأخضر والأحمر بالأحمر والأزرق بالأزرق والبنفسجي بالبنفسجي، كلٌّ بقطعة مستقيمة واحدة.",
          "Pour relier des points de même couleur, on ne relie pas les plus proches : rose avec rose, vert avec vert, rouge avec rouge, bleu avec bleu, violet avec violet, par un segment droit."),
        T("A segment can pass through the red point: the point is inside the segment, between the ends. But if the red point must be an endpoint, the segment must start or stop exactly at it. These are two different jobs.",
          "يمكن للقطعة أن تمرّ بالنقطة الحمراء: تكون النقطة داخل القطعة بين نهايتيها. أما إذا طُلب أن تكون النقطة الحمراء نهاية فيجب أن تبدأ القطعة أو تنتهي عندها تمامًا. هذان عملان مختلفان.",
          "Un segment peut passer par le point rouge : le point est à l'intérieur. Mais si le point rouge doit être une extrémité, le segment commence ou finit exactement là. Ce sont deux tâches différentes."),
    ]),
    ("In order and all the pairs", "بالترتيب وكل الأزواج", "Dans l'ordre et toutes les paires", "21", [
        T("To join numbered points, follow the order: 1 to 2, 2 to 3, 3 to 4, and so on. Do not jump. With 11 points we draw 10 segments.",
          "لوصل النقاط المرقّمة نتبع الترتيب: 1 إلى 2 ثم 2 إلى 3 ثم 3 إلى 4 وهكذا. لا نقفز. مع 11 نقطة نرسم 10 قطع.",
          "Pour relier des points numérotés, on suit l'ordre : 1 à 2, 2 à 3, 3 à 4... Sans sauter. Avec 11 points : 10 segments."),
        T("To join every pair of 5 points A, B, C, D, E, work in an organised way. From A: 4 segments. From B, without repeating A–B: 3. From C: 2. From D: 1.",
          "لوصل كل أزواج 5 نقاط A وB وC وD وE نعمل بطريقة منظمة. من A: 4 قطع. من B دون تكرار A–B: 3. من C: 2. من D: 1.",
          "Pour relier toutes les paires de 5 points A, B, C, D, E, on s'organise. De A : 4 segments. De B sans répéter A–B : 3. De C : 2. De D : 1."),
        F("4 + 3 + 2 + 1 = 10"),
        T("A–B and B–A are the same segment, so we draw it only once.", "A–B وB–A هما القطعة نفسها فنرسمها مرة واحدة.", "A–B et B–A sont le même segment : on le trace une fois."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("A segment is straight and has two endpoints. We use the ruler: align, hold, draw, stop. Passing through a point is different from having the point as an endpoint. Same colour means match the colours; numbered points mean follow the order; all pairs means work in an organised way.",
          "القطعة مستقيمة ولها نهايتان. نستعمل المسطرة: نضع، نمسك، نرسم، نقف. المرور بنقطة يختلف عن كونها نهاية. اللون نفسه يعني نطابق الألوان؛ والنقاط المرقّمة تعني نتبع الترتيب؛ وكل الأزواج تعني نعمل بتنظيم.",
          "Un segment est droit et a deux extrémités. Avec la règle : placer, tenir, tracer, s'arrêter. Passer par un point n'est pas avoir ce point comme extrémité. Même couleur : on associe les couleurs ; points numérotés : on suit l'ordre ; toutes les paires : on s'organise."),
    ]),
]

EXERCISES = [
    EX("1", "20", st("Using the ruler, trace the dotted lines of the envelope, the arrow and the star.",
                    "بالمسطرة، مرّر على الخطوط المنقّطة في المغلف والسهم والنجمة.",
                    "Avec la règle, repasse les pointillés de l'enveloppe, de la flèche et de l'étoile."), [
        T("Trace one side at a time: from a point to the next point, stop, move the ruler, draw the next segment. Success is not finishing fast. Success is every segment being straight and ending at its marked point.",
          "نرسم ضلعًا واحدًا في كل مرة: من نقطة إلى النقطة التالية، نقف، ننقل المسطرة، ثم نرسم القطعة التالية. النجاح ليس بالسرعة بل بأن تكون كل قطعة مستقيمة وتنتهي عند نقطتها.",
          "Un côté à la fois : d'un point au suivant, on s'arrête, on déplace la règle, on trace le segment suivant. Réussir, c'est avoir des segments droits qui finissent au point marqué."),
    ]),
    EX("2", "20", st("Draw the segments that join points of the same colour.",
                    "ارسم القطع التي تصل بين النقاط من اللون نفسه.",
                    "Trace les segments qui relient les points de même couleur."), [
        T("For each colour: find the first point, find the matching point of the same colour, put the ruler through both, draw one straight segment and stop at the second point.",
          "لكل لون: ابحث عن النقطة الأولى ثم النقطة المطابقة من اللون نفسه، ضع المسطرة عليهما، ارسم قطعة مستقيمة واحدة وقف عند النقطة الثانية.",
          "Pour chaque couleur : trouve le premier point, puis celui de même couleur, place la règle sur les deux, trace un segment droit et arrête-toi au second."),
        F("pink–pink   green–green   red–red   blue–blue   purple–purple"),
    ]),
    EX("3", "20", st("Draw two segments that pass through the red point.",
                    "ارسم قطعتين مستقيمتين تمرّان بالنقطة الحمراء.",
                    "Trace deux segments qui passent par le point rouge."), [
        T("The red point does not have to be an endpoint; it can be inside the segment. Draw one horizontal segment through it and one slanted segment through it, with the red point between the ends each time. Many answers are correct.",
          "لا يلزم أن تكون النقطة الحمراء نهاية؛ يمكن أن تكون داخل القطعة. ارسم قطعة أفقية تمرّ بها وأخرى مائلة تمرّ بها، وتكون النقطة الحمراء بين النهايتين في كل مرة. هناك إجابات صحيحة كثيرة.",
          "Le point rouge n'est pas forcément une extrémité ; il peut être à l'intérieur. Trace un segment horizontal et un segment oblique qui passent par lui, le point entre les extrémités. Plusieurs réponses sont justes."),
    ]),
    EX("4", "21", st("In each box draw a segment whose endpoint is the red point.",
                    "في كل مربع ارسم قطعة مستقيمة نقطة نهايتها هي النقطة الحمراء.",
                    "Dans chaque cadre, trace un segment dont une extrémité est le point rouge."), [
        T("The red point is endpoint 1. Choose another point in the box as endpoint 2, put the ruler through both and draw one straight segment. Start or stop exactly at the red point. If the red point is in the middle, the job is not done.",
          "النقطة الحمراء هي النهاية الأولى. اختر نقطة أخرى في المربع نهاية ثانية، ضع المسطرة عليهما وارسم قطعة مستقيمة. ابدأ أو انتهِ عند النقطة الحمراء تمامًا. إذا كانت في المنتصف فلم ننجز المطلوب.",
          "Le point rouge est l'extrémité 1. Choisis un autre point du cadre comme extrémité 2, place la règle et trace un segment droit, en partant ou en finissant exactement au point rouge. S'il est au milieu, ce n'est pas ce qu'on demande."),
    ]),
    EX("5", "21", st("Join the numbered points in order, from 1 to 11.",
                    "صِل النقاط المرقّمة بالترتيب من 1 إلى 11.",
                    "Relie les points numérotés dans l'ordre, de 1 à 11."), [
        F("1→2   2→3   3→4   4→5   5→6   6→7   7→8   8→9   9→10   10→11"),
        T("That is 10 segments. Keep the segment already drawn between points 4 and 8; do not erase it.",
          "هذه 10 قطع. أبقِ القطعة المرسومة مسبقًا بين النقطتين 4 و8 ولا تمحها.",
          "Cela fait 10 segments. Garde le segment déjà tracé entre les points 4 et 8."),
    ]),
    EX("6", "21", st("Draw all the segments that join the 5 given points A, B, C, D, E.",
                    "ارسم كل القطع التي تصل بين النقاط الخمس A وB وC وD وE.",
                    "Trace tous les segments qui joignent les 5 points A, B, C, D, E."), [
        F("from A: AB, AC, AD, AE (4)"),
        F("from B: BC, BD, BE (3)      from C: CD, CE (2)      from D: DE (1)"),
        F("4 + 3 + 2 + 1 = 10 segments"),
    ]),
]
