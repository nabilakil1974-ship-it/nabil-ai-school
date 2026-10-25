"""Grade 1 Mathematics — Add (continuation)."""
from scripts.direct_lessons.common import T, F, EX, st, join, numpath

LESSON_ID = "G01-MATH-EN-017"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Add (continuation)", "ar": "الجمع (تتمة)", "fr": "Additionner (suite)"}
P = list("123456789")

THEORY = [
    ("Identify the two parts", "نحدّد الجزأين", "Repérer les deux parties", "48", [
        T("Hello! We now have more than one way to solve an addition: build objects, draw, count all, and when we are ready, count on. Today the most important thing: choose a strategy you understand, then check.",
          "مرحبًا! صار عندنا أكثر من طريقة لحلّ الجمع: نبني أشياء، نرسم، نعدّ الكل، وعندما نكون جاهزين نعدّ تصاعديًا. اليوم أهم شيء: نختار طريقة نفهمها ثم نتحقق.",
          "Bonjour ! On a plusieurs façons de résoudre une addition : construire, dessiner, tout compter et, quand on est prêt, surcompter. Aujourd'hui l'essentiel : choisir une stratégie qu'on comprend, puis vérifier."),
        join(3, 2, "circle", "circle", "#1e63d6", "#e53935", total=False),
        T("Story: three birds are on a branch, and two more birds come. Before calculating we find the parts: three were there, two came. The parts are 3 and 2.",
          "قصة: ثلاثة عصافير على غصن، ثم يأتي عصفوران آخران. قبل الحساب نحدّد الجزأين: كان هناك ثلاثة وجاء اثنان. الجزآن 3 و2.",
          "Histoire : trois oiseaux sont sur une branche, deux autres arrivent. Avant de calculer, on repère les parties : trois étaient là, deux sont arrivés. Les parties sont 3 et 2."),
    ]),
    ("Choose a strategy", "نختار طريقة", "Choisir une stratégie", "48", [
        F("3 + 2 = ?"),
        T("What can we do? Build and count all, draw, or count on. If counting on does not feel comfortable, that is fine. The strategy must help you.",
          "ماذا نفعل؟ نبني ونعدّ الكل، أو نرسم، أو نعدّ تصاعديًا. إذا لم ترتح للعدّ التصاعدي فلا مشكلة. الطريقة يجب أن تساعدك.",
          "Que faire ? Construire et tout compter, dessiner, ou surcompter. Si surcompter ne te convient pas, ce n'est pas grave. La stratégie doit t'aider."),
        join(3, 2),
        T("Count all gives 5. Count on from three: four, five, also 5. Both ways give the same total.",
          "عدّ الكل يعطي 5. والعدّ التصاعدي من ثلاثة: أربعة، خمسة، أيضًا 5. الطريقتان تعطيان المجموع نفسه.",
          "Tout compter donne 5. Surcompter depuis trois : quatre, cinq, aussi 5. Les deux façons donnent le même total."),
    ]),
    ("Count on correctly", "نعدّ تصاعديًا بشكل صحيح", "Surcompter correctement", "49", [
        numpath(P, hi=4),
        T("If the first part is 5 and we add 2, we do not say five, five, six. The 5 is already counted. We start after it: six, seven. So 5 + 2 = 7.",
          "إذا كان الجزء الأول 5 ونضيف 2، لا نقول خمسة، خمسة، ستة. الـ5 معدود أصلًا. نبدأ بعده: ستة، سبعة. إذن 5 + 2 = 7.",
          "Si la première partie est 5 et qu'on ajoute 2, on ne dit pas cinq, cinq, six. Le 5 est déjà compté. On commence après : six, sept. Donc 5 + 2 = 7."),
        numpath(P, hi=6),
        F("5 + 2 = 7"),
    ]),
    ("The same addition in different ways", "الجمع نفسه بطرق مختلفة", "La même addition de plusieurs façons", "49", [
        join(2, 4, "square", "square", "#1e63d6", "#e53935", total=False),
        T("2 + 4 = 6 can be seen as objects, as a drawing, and as a writing. Three representations, the same relationship.",
          "يمكن رؤية 2 + 4 = 6 كأشياء وكرسم وككتابة. ثلاث تمثيلات والعلاقة نفسها.",
          "2 + 4 = 6 se voit en objets, en dessin et en écriture. Trois représentations, la même relation."),
        F("2 + 4 = 6"),
    ]),
    ("Check the total", "نتحقق من المجموع", "Vérifier le total", "50", [
        join(4, 3, "circle", "circle", "#fb8c00", "#8e24aa"),
        T("Example: 4 + 3 = 7. Check with the objects: count seven. Or count on from four: five, six, seven. The two ways agree.",
          "مثال: 4 + 3 = 7. نتحقق بالأشياء: نعدّ سبعة. أو نعدّ تصاعديًا من أربعة: خمسة، ستة، سبعة. الطريقتان متفقتان.",
          "Exemple : 4 + 3 = 7. On vérifie avec les objets : on compte sept. Ou on surcompte depuis quatre : cinq, six, sept. Les deux s'accordent."),
    ]),
    ("Explain the strategy", "نشرح الطريقة", "Expliquer la stratégie", "50", [
        T("For 3 + 4 = 7 we say: the parts are 3 and 4. I counted on from 3: four, five, six, seven. The total is 7. I checked with counters. We say what the parts are, what strategy we used, the total, and how we checked.",
          "في 3 + 4 = 7 نقول: الجزآن 3 و4. عددت تصاعديًا من 3: أربعة، خمسة، ستة، سبعة. المجموع 7. تحققت بالعدّادات. نذكر الجزأين والطريقة والمجموع وكيف تحققنا.",
          "Pour 3 + 4 = 7 on dit : les parties sont 3 et 4. J'ai surcompté depuis 3 : quatre, cinq, six, sept. Le total est 7. J'ai vérifié avec des jetons."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Addition means parts join to find a total. We can build and count all, or count on. The strongest answer has a check.",
          "الجمع يعني أن تنضمّ الأجزاء لنجد المجموع. نستطيع أن نبني ونعدّ الكل أو نعدّ تصاعديًا. والجواب الأقوى فيه تحقّق.",
          "Additionner, c'est réunir des parties pour trouver un total. On peut construire et tout compter, ou surcompter. La meilleure réponse a une vérification."),
        F("FIND PARTS → CHOOSE STRATEGY → ADD → WRITE → CHECK WITH ANOTHER WAY → EXPLAIN"),
    ]),
]

EXERCISES = [
    EX("1", "48", st("Find the parts: 4 blocks are on the table and 1 more block is added.", "جد الجزأين: 4 مكعبات على الطاولة ويُضاف مكعب.", "Trouve les parties : 4 cubes sont sur la table et on en ajoute 1."), [
        join(4, 1, "square", "square", "#1e63d6", "#e53935", total=False),
        T("First part: 4. Second part: 1. The action is joining. Now we are ready to calculate.",
          "الجزء الأول: 4. الجزء الثاني: 1. الفعل هو الضمّ. نحن جاهزون للحساب.",
          "Première partie : 4. Deuxième partie : 1. L'action est la réunion. On est prêt à calculer."),
    ]),
    EX("2", "49", st("Solve 4 + 2 in your way, then check with another way.", "احسب 4 + 2 بطريقتك ثم تحقّق بطريقة أخرى.", "Calcule 4 + 2 à ta façon, puis vérifie d'une autre façon."), [
        join(4, 2),
        T("Build and count all: 6. Count on from four: five, six. Same total.",
          "نبني ونعدّ الكل: 6. العدّ التصاعدي من أربعة: خمسة، ستة. المجموع نفسه.",
          "Construire et tout compter : 6. Surcompter depuis quatre : cinq, six. Même total."),
    ]),
    EX("3", "49", st("Count on without counting the start again: 6 + 2.", "عدّ تصاعديًا دون عدّ البداية مرة ثانية: 6 + 2.", "Surcompte sans recompter le départ : 6 + 2."), [
        numpath(P, hi=5),
        T("Start from six. There are two more: seven, eight. So 6 + 2 = 8. If you said six, seven, you counted the starting quantity as an added object.",
          "نبدأ من ستة. هناك اثنان آخران: سبعة، ثمانية. إذن 6 + 2 = 8. إذا قلت ستة، سبعة فقد عددت الكمية الأولى كأنها شيء مضاف.",
          "On part de six. Il y en a deux de plus : sept, huit. Donc 6 + 2 = 8. Si tu as dit six, sept, tu as compté la quantité de départ comme un objet ajouté."),
        F("6 + 2 = 8"),
    ]),
    EX("4", "49", st("Match the writing 3 + 3 = 6 with a model: A: 3 and 3. B: 2 and 3. C: 6 and 1.", "طابق الكتابة 3 + 3 = 6 مع نموذج: A: 3 و3. B: 2 و3. C: 6 و1.", "Associe l'écriture 3 + 3 = 6 à un modèle : A : 3 et 3. B : 2 et 3. C : 6 et 1."), [
        join(3, 3, "circle", "circle", "#e53935", "#1e63d6"),
        T("The answer is A: it has part 3, part 3 and total 6.",
          "الجواب A: فيه جزء 3 وجزء 3 ومجموع 6.",
          "La réponse est A : elle a la partie 3, la partie 3 et le total 6."),
    ]),
    EX("5", "50", st("Check with a second method: 5 + 3.", "تحقّق بطريقة ثانية: 5 + 3.", "Vérifie avec une deuxième méthode : 5 + 3."), [
        numpath(P, hi=7),
        T("Count on from five: six, seven, eight. Now check with the model.",
          "نعدّ تصاعديًا من خمسة: ستة، سبعة، ثمانية. الآن نتحقق بالنموذج.",
          "Surcompte depuis cinq : six, sept, huit. Maintenant on vérifie avec le modèle."),
        join(5, 3, "circle", "circle", "#fb8c00", "#8e24aa"),
    ]),
    EX("6", "50", st("Error detective: “5 + 2 = 6 because I counted 5, 6.”", "المحقق: «5 + 2 = 6 لأني عددت 5، 6».", "Détective : « 5 + 2 = 6 parce que j'ai compté 5, 6 »."), [
        T("The child counted only one added step. After five we need two counts: six, seven.",
          "الطفل عدّ خطوة واحدة فقط. بعد خمسة نحتاج عدّتين: ستة، سبعة.",
          "L'enfant n'a compté qu'un pas ajouté. Après cinq il faut deux comptes : six, sept."),
        F("5 + 2 = 7"),
    ]),
    EX("7", "50", st("Challenge: solve 4 + 3 in two ways.", "تحدٍّ: احسب 4 + 3 بطريقتين.", "Défi : calcule 4 + 3 de deux façons."), [
        join(4, 3, "circle", "circle", "#e53935", "#1e63d6"),
        T("Method one: model and count all: 7. Method two: count on: five, six, seven. Strategies may differ as long as the quantities are kept and the answer is checked.",
          "الطريقة الأولى: النموذج وعدّ الكل: 7. الطريقة الثانية: العدّ التصاعدي: خمسة، ستة، سبعة. قد تختلف الطرق ما دامت الكميات محفوظة والجواب محقَّقًا.",
          "Première façon : modèle et tout compter : 7. Deuxième façon : surcompter : cinq, six, sept. Les stratégies peuvent différer tant que les quantités sont gardées et la réponse vérifiée."),
        F("4 + 3 = 7"),
    ]),
    EX("8", "50", st("Final check: parts of 5 + 2, solve 4 + 3, solve 6 + 2, and explain one strategy.", "تقييم أخير: جزآ 5 + 2، احسب 4 + 3، احسب 6 + 2، واشرح طريقة واحدة.", "Évaluation : parties de 5 + 2, calcule 4 + 3, calcule 6 + 2 et explique une stratégie."), [
        join(5, 2, "circle", "circle", "#1e63d6", "#e53935"),
        F("5 + 2 = 7      4 + 3 = 7      6 + 2 = 8"),
        T("Explain: the parts are 6 and 2. I counted on from six: seven, eight. The total is 8. I checked with counters.",
          "نشرح: الجزآن 6 و2. عددت تصاعديًا من ستة: سبعة، ثمانية. المجموع 8. تحققت بالعدّادات.",
          "J'explique : les parties sont 6 et 2. J'ai surcompté depuis six : sept, huit. Le total est 8. J'ai vérifié avec des jetons."),
    ]),
]
