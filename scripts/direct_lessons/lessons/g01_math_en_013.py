"""Grade 1 Mathematics — More than / Fewer than."""
from scripts.direct_lessons.common import T, F, EX, st, pairs, spread, objects

LESSON_ID = "G01-MATH-EN-013"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "More than - Fewer than", "ar": "أكثر من - أقل من", "fr": "Plus que - Moins que"}

THEORY = [
    ("Pair first", "نُقرن أولًا", "Apparier d'abord", "40", [
        T("Hello! Last time we learned as many as, when two groups have the same number. Today we see what happens when the numbers are not equal.",
          "مرحبًا! في المرة الماضية تعلّمنا بقدر، عندما يكون للمجموعتين العدد نفسه. اليوم نرى ماذا يحدث عندما لا يكون العددان متساويين.",
          "Bonjour ! La dernière fois, nous avons vu autant que, quand deux groupes ont le même nombre. Aujourd'hui, voyons quand les nombres ne sont pas égaux."),
        pairs(5, 3, "star", "circle", "#fbc02d", "#1e63d6"),
        T("Your eyes may give you an answer, but we want a proof. We pair: one star with one circle. The circles run out, but two stars are left without partners.",
          "قد تعطيك عيناك جوابًا، لكننا نريد دليلًا. نُقرن: نجمة مع دائرة. تنتهي الدوائر وتبقى نجمتان بلا شريك.",
          "Tes yeux peuvent te donner une réponse, mais on veut une preuve. On apparie : une étoile avec un cercle. Les cercles sont finis, mais deux étoiles restent sans partenaire."),
        T("So group A has more objects, and group B has fewer. A has objects left over without partners.",
          "إذن المجموعة A فيها أشياء أكثر، والمجموعة B فيها أشياء أقل. في A أشياء بقيت بلا شريك.",
          "Donc le groupe A a plus d'objets et le groupe B en a moins. A a des objets restants sans partenaire."),
    ]),
    ("Fewer is the group that runs out first", "الأقل هي المجموعة التي تنتهي أولًا", "Moins : le groupe qui finit en premier", "40", [
        pairs(6, 4, "square", "circle", "#fb8c00", "#8e24aa"),
        T("A has six and B has four. When we make pairs, B runs out first. So B has fewer and A has more. More and fewer belong to the same comparison.",
          "في A ستة وفي B أربعة. عندما نُقرن تنتهي B أولًا. إذن B فيها أقل وA فيها أكثر. أكثر وأقل ينتميان إلى المقارنة نفسها.",
          "A en a six et B en a quatre. Quand on apparie, B finit en premier. B en a donc moins et A en a plus. Plus et moins appartiennent à la même comparaison."),
    ]),
    ("Spacing can fool us", "المسافة قد تخدعنا", "L'espacement peut nous tromper", "41", [
        spread(4, 120, "circle", "#1e63d6", 200, "W", ),
        T("Four dots are widely spaced, so their row looks longer. Six dots are close together. Does the long row have more? No.",
          "أربع نقاط متباعدة جدًا فصفّها يبدو أطول. وست نقاط متقاربة. هل الصف الطويل فيه أكثر؟ لا.",
          "Quatre points très espacés : leur rangée paraît plus longue. Six points serrés. La longue rangée en a-t-elle plus ? Non."),
        T("Let us count: the close group has six and the spread group has four. So the close group has more and the spread group has fewer. Distance does not decide.",
          "لنعدّ: المجموعة المتقاربة فيها ستة والمتباعدة فيها أربعة. إذن المتقاربة أكثر والمتباعدة أقل. المسافة لا تقرر.",
          "Comptons : le groupe serré en a six et l'espacé en a quatre. Le serré en a plus, l'espacé en a moins. La distance ne décide pas."),
        F("6 > 4"),
    ]),
    ("Use the words correctly", "نستعمل الكلمات بشكل صحيح", "Bien utiliser les mots", "41", [
        pairs(9, 6, "star", "star", "#fbc02d", "#43a047", gap=62, r=20),
        T("If I say A has more than B, then I also know that B has fewer than A. Here A is nine and B is six.",
          "إذا قلت إن A أكثر من B فأنا أعرف أيضًا أن B أقل من A. هنا A تسعة وB ستة.",
          "Si je dis que A a plus que B, je sais aussi que B a moins que A. Ici A est neuf et B est six."),
        F("A has more than B      B has fewer than A"),
    ]),
    ("Counting verifies pairing", "العدّ يتحقق من الإقران", "Compter vérifie l'appariement", "41", [
        pairs(8, 7, "circle", "circle", "#e53935", "#1e63d6", gap=70, r=20),
        T("Pairing gives us a visual proof. Counting gives us a check. After pairing, one object is left in A. Count A: eight. Count B: seven.",
          "الإقران يعطينا دليلًا بصريًا، والعدّ يعطينا تحقّقًا. بعد الإقران بقي شيء في A. نعدّ A: ثمانية. نعدّ B: سبعة.",
          "L'appariement donne une preuve visuelle, le comptage une vérification. Après appariement, un objet reste dans A. On compte A : huit. B : sept."),
        F("8 > 7"),
        T("Both ways say the same thing: A has more, B has fewer.",
          "الطريقتان تقولان الشيء نفسه: A أكثر وB أقل.",
          "Les deux façons disent la même chose : A en a plus, B en a moins."),
    ]),
    ("Explain why", "نشرح السبب", "Expliquer pourquoi", "41", [
        T("A good answer has the answer and the evidence. Seven cars and four cars: seven is more. The evidence: three cars are left without partners, or seven is more than four.",
          "الجواب الجيد فيه الجواب والدليل. سبع سيارات وأربع سيارات: السبع أكثر. الدليل: بقيت ثلاث سيارات بلا شريك، أو لأن سبعة أكبر من أربعة.",
          "Une bonne réponse a la réponse et la preuve. Sept voitures et quatre voitures : sept est plus. La preuve : trois voitures restent sans partenaire, ou sept est plus grand que quatre."),
        F("answer + evidence"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("When we compare two groups, we make pairs. The group with objects left over has more. The group that runs out first has fewer. We never trust size or spacing alone.",
          "عندما نقارن مجموعتين نُقرن. المجموعة التي تبقى فيها أشياء فيها أكثر. والمجموعة التي تنتهي أولًا فيها أقل. ولا نثق بالحجم أو المسافة وحدهما.",
          "Quand on compare deux groupes, on fait des paires. Le groupe qui a des restes en a plus. Celui qui finit en premier en a moins. On ne se fie jamais seulement à la taille ou à l'espacement."),
        F("LOOK → PAIR → SEE WHAT REMAINS → MORE / FEWER → COUNT → EXPLAIN"),
    ]),
]

EXERCISES = [
    EX("1", "40", st("Pair 4 apples with 2 teddy bears. Which group has more?", "أقرن 4 تفاحات مع دبّين. أي مجموعة فيها أكثر؟", "Apparie 4 pommes avec 2 oursons. Quel groupe en a plus ?"), [
        pairs(4, 2, "circle", "tri", "#e53935", "#8d6e63"),
        T("The teddy bears run out, and two apples are left. So the apples have more and the teddy bears have fewer.",
          "تنتهي الدببة وتبقى تفاحتان. إذن التفاح أكثر والدببة أقل.",
          "Les oursons sont finis et deux pommes restent. Les pommes sont plus nombreuses, les oursons moins."),
        F("A has more; B has fewer."),
    ]),
    EX("2", "40", st("A has 7 stars and B has 5 stars. Who has fewer?", "في A سبع نجوم وفي B خمس نجوم. من عنده أقل؟", "A a 7 étoiles et B a 5 étoiles. Qui en a moins ?"), [
        pairs(7, 5, "star", "star", "#fbc02d", "#43a047", gap=70, r=20),
        T("B runs out first after pairing, and 5 is less than 7.",
          "B تنتهي أولًا بعد الإقران، و5 أقل من 7.",
          "B finit en premier après appariement, et 5 est moins que 7."),
        F("B has fewer."),
    ]),
    EX("3", "41", st("Don't be fooled: 8 small close stars and 5 large spread circles. Which has more?", "لا تنخدع: 8 نجوم صغيرة متقاربة و5 دوائر كبيرة متباعدة. أيهما أكثر؟", "Ne te laisse pas tromper : 8 petites étoiles serrées et 5 grands cercles espacés. Lequel en a plus ?"), [
        pairs(8, 5, "star", "circle", "#fbc02d", "#1e63d6", gap=70, r=18),
        T("Count A: eight. Count B: five. Size and spacing do not matter.",
          "نعدّ A: ثمانية. ونعدّ B: خمسة. الحجم والمسافة لا يهمّان.",
          "On compte A : huit. B : cinq. La taille et l'espacement ne comptent pas."),
        F("A has more."),
    ]),
    EX("4", "41", st("A is 4 and B is 7. Say both sentences.", "A أربعة وB سبعة. قل الجملتين.", "A est 4 et B est 7. Dis les deux phrases."), [
        pairs(4, 7, "circle", "square", "#e53935", "#1e63d6", gap=62, r=20),
        F("B has more than A"),
        F("A has fewer than B"),
    ]),
    EX("5", "41", st("Prove in two ways: A is 5 and B is 3.", "أثبت بطريقتين: A خمسة وB ثلاثة.", "Prouve de deux façons : A est 5 et B est 3."), [
        pairs(5, 3, "star", "circle", "#fbc02d", "#1e63d6"),
        T("Method one: pair them, and two are left in A. Method two: count five and three.",
          "الطريقة الأولى: نُقرن فيبقى اثنان في A. الطريقة الثانية: نعدّ خمسة وثلاثة.",
          "Première façon : on apparie, il en reste deux dans A. Deuxième façon : on compte cinq et trois."),
        F("A has more; B has fewer."),
    ]),
    EX("6", "41", st("Error detective: A has 3 stars, B has 6 stars. Someone says A has more than B.", "المحقق: في A ثلاث نجوم وفي B ست نجوم. قال أحدهم إن A أكثر من B.", "Détective : A a 3 étoiles, B en a 6. Quelqu'un dit que A en a plus que B."), [
        pairs(3, 6, "star", "star", "#fbc02d", "#43a047", gap=70, r=20),
        T("The sentence is wrong. After pairing, B has objects left.",
          "الجملة خاطئة. بعد الإقران تبقى أشياء في B.",
          "La phrase est fausse. Après appariement, il reste des objets dans B."),
        F("A has fewer than B"),
        F("B has more than A"),
    ]),
    EX("7", "41", st("Challenge: A is 4, B is 9, C is 6. Who has the most? Who has the fewest? Order them.", "تحدٍّ: A أربعة وB تسعة وC ستة. من الأكثر؟ ومن الأقل؟ رتّبها.", "Défi : A est 4, B est 9, C est 6. Qui en a le plus ? Le moins ? Range-les."), [
        F("A = 4      B = 9      C = 6"),
        T("B has the most and A has the fewest. From fewer to more:",
          "B الأكثر وA الأقل. من الأقل إلى الأكثر:",
          "B en a le plus et A le moins. Du moins au plus :"),
        F("A → C → B"),
        F("4 → 6 → 9"),
    ]),
    EX("8", "41", st("Correct the sentence: “5 has more objects than 8.”", "صحّح الجملة: «5 أشياء أكثر من 8».", "Corrige la phrase : « 5 a plus d'objets que 8 »."), [
        pairs(5, 8, "circle", "circle", "#e53935", "#1e63d6", gap=70, r=18),
        T("Eight is greater than five. So five has fewer, and eight has more.",
          "ثمانية أكبر من خمسة. إذن 5 أقل و8 أكثر.",
          "Huit est plus grand que cinq. Donc 5 en a moins et 8 en a plus."),
        F("5 has fewer; 8 has more."),
    ]),
]
