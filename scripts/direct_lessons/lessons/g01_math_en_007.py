"""Grade 1 Mathematics — Additive writings."""
from scripts.direct_lessons.common import T, F, D, EX, st, S, objects, row, numeral, scene

LESSON_ID = "G01-MATH-EN-007"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Additive writings", "ar": "الكتابة الجمعية", "fr": "Écritures additives"}


from scripts.direct_lessons.common import join


THEORY = [
    ("First part + second part = total", "الجزء الأول + الجزء الثاني = المجموع", "Première partie + deuxième partie = total", "28", [
        T("Hello! Addition is a story: one group joins another group, and then we find the total. Today we learn to write this story in a short way.",
          "مرحبًا! الجمع قصّة: مجموعة تنضمّ إلى مجموعة أخرى ثم نجد المجموع. اليوم نتعلّم كيف نكتب هذه القصة بشكل قصير.",
          "Bonjour ! Additionner, c'est une histoire : un groupe en rejoint un autre, puis on trouve le total. Aujourd'hui, on apprend à l'écrire en bref."),
        join(2, 1, total=False),
        T("There were two apples, then one more apple came. The first part is 2, the second part is 1.",
          "كان هناك تفاحتان ثم جاءت تفاحة. الجزء الأول 2 والجزء الثاني 1.",
          "Il y avait deux pommes, puis une pomme de plus est arrivée. La première partie est 2, la deuxième est 1."),
        join(2, 1),
        T("We read it from left to right: two plus one equals three. The 2 comes from the first part, the 1 from the second part, and the 3 is the total.",
          "نقرؤها من اليسار إلى اليمين: two plus one equals three. العدد 2 من الجزء الأول، و1 من الجزء الثاني، و3 هو المجموع.",
          "On lit de gauche à droite : two plus one equals three. Le 2 vient de la première partie, le 1 de la deuxième, et le 3 est le total."),
        F("2 + 1 = 3"),
        T("Every number in the writing must have a meaning in the picture.",
          "كل عدد في الكتابة يجب أن يكون له معنى في الصورة.",
          "Chaque nombre de l'écriture doit avoir un sens dans l'image."),
    ]),
    ("What does plus mean?", "ماذا يعني الرمز +؟", "Que veut dire plus ?", "28", [
        join(2, 2, "square", "square", "#1e63d6", "#e53935", total=False),
        T("The plus sign is not just a mark. It tells us that one quantity joins another quantity.",
          "الرمز + ليس مجرد علامة، إنه يخبرنا أن كمية تنضمّ إلى كمية أخرى.",
          "Le signe plus n'est pas juste une marque : il dit qu'une quantité en rejoint une autre."),
        T("When we see plus, we ask: what is joining what? Here two blue blocks join two red blocks. Then we find the whole.",
          "عندما نرى + نسأل: ماذا ينضمّ إلى ماذا؟ هنا مكعبان أزرقان ينضمّان إلى مكعبين أحمرين. بعدها نجد المجموع الكلي.",
          "Quand on voit plus, on demande : qu'est-ce qui rejoint quoi ? Ici deux cubes bleus rejoignent deux cubes rouges. Puis on trouve le tout."),
    ]),
    ("What does equals mean?", "ماذا يعني الرمز =؟", "Que veut dire égal ?", "29", [
        join(2, 1),
        T("The equals sign tells us that what is on the left has the same value as what is on the right.",
          "الرمز = يخبرنا أن ما على اليسار له القيمة نفسها لما على اليمين.",
          "Le signe égal dit que ce qui est à gauche a la même valeur que ce qui est à droite."),
        F("2 + 1 and 3 are the same total"),
        T("Equals means: has the same value as. Both sides speak about the same quantity.",
          "تعني equals: له القيمة نفسها. الجهتان تتحدثان عن الكمية نفسها.",
          "Égal veut dire : a la même valeur que. Les deux côtés parlent de la même quantité."),
    ]),
    ("From the model to the writing", "من النموذج إلى الكتابة", "Du modèle à l'écriture", "29", [
        join(2, 3, "circle", "circle", "#fb8c00", "#8e24aa", total=False),
        T("We do four things: see the first part, see the second part, find the total, then write first part plus second part equals total.",
          "نفعل أربع خطوات: نرى الجزء الأول، ونرى الجزء الثاني، ونجد المجموع، ثم نكتب الجزء الأول + الجزء الثاني = المجموع.",
          "On fait quatre choses : voir la première partie, voir la deuxième, trouver le total, puis écrire première partie plus deuxième partie égale total."),
        T("First part: 2. Second part: 3. Total: 5.",
          "الجزء الأول: 2. الجزء الثاني: 3. المجموع: 5.",
          "Première partie : 2. Deuxième partie : 3. Total : 5."),
        F("2 + 3 = 5"),
    ]),
    ("From the writing to the model", "من الكتابة إلى النموذج", "De l'écriture au modèle", "29", [
        F("3 + 1 = 4"),
        T("We do not memorize it. We build it: put three in the first part, one in the second part, join them and count the total.",
          "لا نحفظها، بل نبنيها: نضع 3 في الجزء الأول و1 في الجزء الثاني، ثم نضمّهما ونعدّ المجموع.",
          "On ne la mémorise pas, on la construit : trois dans la première partie, un dans la deuxième, on les réunit et on compte le total."),
        join(3, 1),
        T("The writing and the picture tell the same story.",
          "الكتابة والصورة تحكيان القصة نفسها.",
          "L'écriture et l'image racontent la même histoire."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        F("first part + second part = total"),
        T("Plus means join. Equals means both sides have the same value. Every number in the writing must match a quantity in the picture.",
          "الجمع يعني الضم. والمساواة تعني أن الجهتين لهما القيمة نفسها. وكل عدد في الكتابة يجب أن يطابق كمية في الصورة.",
          "Plus veut dire réunir. Égal veut dire que les deux côtés ont la même valeur. Chaque nombre de l'écriture correspond à une quantité de l'image."),
        F("SEE THE PARTS → JOIN → FIND THE TOTAL → WRITE → READ → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "28", st("Group A has 3 stars and group B has 1 star. Write the addition.", "المجموعة A فيها 3 نجوم والمجموعة B فيها نجمة. اكتب عملية الجمع.", "Le groupe A a 3 étoiles et le groupe B a 1 étoile. Écris l'addition."), [
        join(3, 1, total=False),
        T("First part: 3. Second part: 1. Join them and count: one, two, three, four. The total is 4.",
          "الجزء الأول: 3. الجزء الثاني: 1. نضمّهما ونعدّ: واحد، اثنان، ثلاثة، أربعة. المجموع 4.",
          "Première partie : 3. Deuxième partie : 1. On réunit et on compte : un, deux, trois, quatre. Le total est 4."),
        F("3 + 1 = 4"),
        T("We read it: three plus one equals four.",
          "نقرؤها: three plus one equals four.",
          "On la lit : three plus one equals four."),
    ]),
    EX("2", "28", st("Which story fits 2 + 1 = 3? A: 2 birds, then 1 flies away. B: 2 birds, then 1 bird comes. C: 2 birds stay alone.", "أي قصة تناسب 2 + 1 = 3؟ A: عصفوران ثم يطير واحد. B: عصفوران ثم يأتي عصفور. C: عصفوران يبقيان وحدهما.", "Quelle histoire va avec 2 + 1 = 3 ? A : 2 oiseaux, un s'envole. B : 2 oiseaux, un oiseau arrive. C : 2 oiseaux restent seuls."), [
        T("Plus means a new group joins. In story B a new bird comes, so there are three birds.",
          "الجمع يعني انضمام مجموعة جديدة. في القصة B يأتي عصفور جديد فيصبح العدد ثلاثة.",
          "Plus veut dire qu'un nouveau groupe arrive. Dans l'histoire B, un oiseau arrive : il y a trois oiseaux."),
        F("The answer is B."),
        T("In story A a bird leaves, so it is not a joining story.",
          "في القصة A يطير عصفور، فليست قصة ضمّ.",
          "Dans l'histoire A, un oiseau part : ce n'est pas une histoire de réunion."),
    ]),
    EX("3", "29", st("Check: is 2 + 2 = 3 true?", "تحقّق: هل 2 + 2 = 3 صحيحة؟", "Vérifie : est-ce que 2 + 2 = 3 est vrai ?"), [
        join(2, 2, "square", "square", "#1e63d6", "#e53935", total=False),
        T("Build the left side: two objects and two objects. Count: one, two, three, four.",
          "نبني الجهة اليسرى: شيئان وشيئان. نعدّ: واحد، اثنان، ثلاثة، أربعة.",
          "On construit le côté gauche : deux objets et deux objets. On compte : un, deux, trois, quatre."),
        T("The total is 4, not 3. So the writing 2 + 2 = 3 is wrong.",
          "المجموع 4 وليس 3. إذن الكتابة 2 + 2 = 3 خاطئة.",
          "Le total est 4, pas 3. L'écriture 2 + 2 = 3 est donc fausse."),
        F("2 + 2 = 4"),
    ]),
    EX("4", "29", st("Model to writing: one teddy bear and two teddy bears.", "من النموذج إلى الكتابة: دبّ واحد ودبّان.", "Du modèle à l'écriture : un ourson et deux oursons."), [
        join(1, 2, "tri", "tri", "#8d6e63", "#8d6e63", total=False),
        T("First part: 1. Second part: 2. Total: 3.",
          "الجزء الأول: 1. الجزء الثاني: 2. المجموع: 3.",
          "Première partie : 1. Deuxième partie : 2. Total : 3."),
        F("1 + 2 = 3"),
    ]),
    EX("5", "29", st("Writing to model: build 2 + 2 = 4 with blocks.", "من الكتابة إلى النموذج: ابنِ 2 + 2 = 4 بالمكعبات.", "De l'écriture au modèle : construis 2 + 2 = 4 avec des cubes."), [
        join(2, 2, "square", "square", "#1e63d6", "#e53935"),
        T("The first part has 2 blocks, the second part has 2 blocks, and after joining the whole has 4.",
          "في الجزء الأول مكعبان، وفي الثاني مكعبان، وبعد الضمّ يصبح الكل 4.",
          "La première partie a 2 cubes, la deuxième 2 cubes, et après réunion le tout fait 4."),
    ]),
    EX("6", "29", st("Error detective: the picture shows 2 + 3 objects, but the writing says 2 + 3 = 4.", "المحقق: الصورة فيها 2 و3 أشياء، لكن المكتوب 2 + 3 = 4.", "Détective : l'image montre 2 + 3 objets, mais l'écriture dit 2 + 3 = 4."), [
        join(2, 3, "circle", "circle", "#fb8c00", "#8e24aa", total=False),
        T("The first part 2 is right and the second part 3 is right. The mistake must be in the total.",
          "الجزء الأول 2 صحيح والجزء الثاني 3 صحيح. إذن الخطأ في المجموع.",
          "La première partie 2 est juste, la deuxième 3 aussi. L'erreur est dans le total."),
        T("Count them all: one, two, three, four, five. The total is 5.",
          "نعدّ الكل: واحد، اثنان، ثلاثة، أربعة، خمسة. المجموع 5.",
          "On compte tout : un, deux, trois, quatre, cinq. Le total est 5."),
        F("2 + 3 = 5"),
    ]),
    EX("7", "29", st("Challenge: 1 red cube, 1 blue cube and 2 green cubes join into one whole. How many cubes?", "تحدٍّ: مكعب أحمر ومكعب أزرق ومكعبان أخضران ينضمّون في كلّ واحد. كم مكعبًا؟", "Défi : 1 cube rouge, 1 cube bleu et 2 cubes verts sont réunis. Combien de cubes ?"), [
        T("First join the two single cubes: 1 + 1 = 2. Then add the two green cubes: 2 + 2 = 4.",
          "نجمع أولًا المكعبين المنفردين: 1 + 1 = 2. ثم نضيف المكعبين الأخضرين: 2 + 2 = 4.",
          "On réunit d'abord les deux cubes seuls : 1 + 1 = 2. Puis on ajoute les deux cubes verts : 2 + 2 = 4."),
        F("1 + 1 = 2      2 + 2 = 4"),
        T("There are 4 cubes in all. Every number stays linked to a real quantity.",
          "يوجد 4 مكعبات في المجموع. وكل عدد يبقى مرتبطًا بكمية حقيقية.",
          "Il y a 4 cubes en tout. Chaque nombre reste lié à une vraie quantité."),
    ]),
    EX("8", "29", st("Read 3 + 1 = 4 and say what each number represents.", "اقرأ 3 + 1 = 4 وقل ماذا يمثّل كل عدد.", "Lis 3 + 1 = 4 et dis ce que représente chaque nombre."), [
        F("3 + 1 = 4"),
        T("Three plus one equals four. The 3 is the first part, the 1 is the second part, and the 4 is the total.",
          "three plus one equals four. العدد 3 هو الجزء الأول، و1 هو الجزء الثاني، و4 هو المجموع.",
          "Three plus one equals four. Le 3 est la première partie, le 1 la deuxième, et le 4 est le total."),
        T("Check with objects: 1 + 2 objects give 3, so writing 1 + 2 = 4 would be wrong.",
          "نتحقق بالأشياء: 1 و2 تعطيان 3، فالكتابة 1 + 2 = 4 تكون خاطئة.",
          "On vérifie avec des objets : 1 et 2 font 3, donc écrire 1 + 2 = 4 serait faux."),
    ]),
]
