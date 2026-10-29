"""Grade 2 Mathematics — Understanding information."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G02-MATH-EN-018"
GRADE = 2
SUBJECT = "math"
TITLES = {"en": "Understanding Information", "ar": "فهم المعلومات", "fr": "Comprendre l'information"}


def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}


QUIZ = [
    {"q": "Lina has 7 red pencils and 12 blue pencils. What does the number 12 tell us?",
     "opts": ["12 blue pencils", "12 red pencils", "12 children", "12 days"], "a": 0,
     "why": {"12 red pencils": _w("The red pencils are 7. The 12 belongs to the blue ones.", "الأقلام الحمراء 7. أما 12 فهي للأقلام الزرقاء.", "Les crayons rouges sont 7. Le 12 est pour les bleus."),
             "12 children": _w("The story says nothing about 12 children.", "القصة لا تذكر 12 طفلًا.", "L'histoire ne parle pas de 12 enfants."),
             "12 days": _w("The story is about pencils, not days.", "القصة عن الأقلام لا عن الأيام.", "L'histoire parle de crayons, pas de jours.")},
     "ok": "12 blue pencils"},
    {"q": "Thursday: present 24, absent 4. Friday: present 21, absent 7. Which day has more absent students?",
     "opts": ["Friday", "Thursday", "Both the same", "We cannot know"], "a": 0,
     "why": {"Thursday": _w("Thursday has 4 absent. Friday has 7 absent, and 7 is more than 4.", "الخميس فيه 4 غائبين والجمعة فيها 7 غائبين، و7 أكبر من 4.", "Jeudi : 4 absents. Vendredi : 7 absents, et 7 > 4."),
             "Both the same": _w("4 and 7 are not the same.", "4 و7 ليسا متساويين.", "4 et 7 ne sont pas égaux."),
             "We cannot know": _w("We can: compare only the absent numbers, 4 and 7.", "نستطيع: نقارن أعداد الغائبين فقط 4 و7.", "On peut : on compare seulement les absents, 4 et 7.")},
     "ok": "Friday, because 7 is more than 4"},
    {"q": "Fadi is 8, Jihad is 5 and Naji is 4 years old. Who is the eldest?",
     "opts": ["Fadi", "Jihad", "Naji", "They are all the same age"], "a": 0,
     "why": {"Jihad": _w("5 is less than 8.", "5 أقل من 8.", "5 est plus petit que 8."),
             "Naji": _w("4 is the smallest age, so Naji is the youngest.", "4 أصغر عمر، فناجي هو الأصغر.", "4 est le plus petit âge : Naji est le plus jeune."),
             "They are all the same age": _w("8, 5 and 4 are different numbers.", "8 و5 و4 أعداد مختلفة.", "8, 5 et 4 sont différents.")},
     "ok": "Fadi is the eldest: 8 is the greatest age."},
]

THEORY = [
    ("A number needs its label", "العدد يحتاج إلى عنوانه", "Un nombre a besoin de son étiquette", "42", [
        T("Hello, champion! Today we understand information. A number alone is not enough. We must ask: what is this number about? Look at 6 pencils and 12 colored crayons. The 6 is about pencils. The 12 is about crayons. Are there more crayons than pencils? Yes, because 12 is more than 6.",
          "مرحبًا يا بطل! اليوم نفهم المعلومات. العدد وحده لا يكفي. يجب أن نسأل: عن ماذا يتحدث هذا العدد؟ انظر: 6 أقلام رصاص و12 قلم تلوين. العدد 6 عن أقلام الرصاص والعدد 12 عن أقلام التلوين. هل أقلام التلوين أكثر؟ نعم، لأن 12 أكبر من 6.",
          "Bonjour, champion ! Aujourd'hui on comprend l'information. Un nombre seul ne suffit pas : il faut demander de quoi il parle. 6 crayons et 12 crayons de couleur : le 6 parle des crayons, le 12 des crayons de couleur. Y a-t-il plus de crayons de couleur ? Oui, car 12 > 6."),
        F("6 → 6 pencils      12 → 12 colored crayons      12 > 6"),
    ]),
    ("Names, objects and days", "الأسماء والأشياء والأيام", "Noms, objets et jours", "42", [
        T("Each number can belong to a person, an object or a day. Jihad is 5 years old, Fadi is 8 and Naji is 4. The number 4 is Naji's age. The eldest child has the greatest age, so Fadi is the eldest.",
          "كل عدد قد يخص شخصًا أو شيئًا أو يومًا. جهاد عمره 5 سنوات وفادي 8 وناجي 4. العدد 4 هو عمر ناجي. الأكبر سنًّا هو صاحب أكبر عمر، إذن فادي هو الأكبر.",
          "Chaque nombre appartient à une personne, un objet ou un jour. Jihad a 5 ans, Fadi 8 ans et Naji 4 ans. Le 4 est l'âge de Naji. Le plus âgé a le plus grand âge : c'est Fadi."),
        F("Jihad 5      Fadi 8      Naji 4      eldest = 8 = Fadi"),
    ]),
    ("Reading a list", "قراءة قائمة", "Lire une liste", "43", [
        T("Look at Santa's gift list: 1 doll for Leila, 2 cars for Sami, 1 truck for Ziad, a bag of 50 marbles for Ramzi, 3 boxes of chocolate for Maya, a bag of 30 marbles for Houssam. The number 2 means 2 cars for Sami. The number 50 means 50 marbles inside one bag. Who gets more marbles? Only look at marbles: 50 and 30. Ramzi, because 50 is more than 30.",
          "انظر إلى قائمة هدايا بابا نويل: دمية لليلى، سيارتان لسامي، شاحنة لزياد، كيس فيه 50 بلية لرمزي، 3 علب شوكولا لمايا، وكيس فيه 30 بلية لحسّام. العدد 2 يعني سيارتين لسامي. والعدد 50 يعني 50 بلية داخل كيس واحد. من يأخذ بلايا أكثر؟ ننظر إلى البلايا فقط: 50 و30. رمزي، لأن 50 أكبر من 30.",
          "La liste du Père Noël : 1 poupée pour Leila, 2 voitures pour Sami, 1 camion pour Ziad, un sac de 50 billes pour Ramzi, 3 boîtes de chocolat pour Maya, un sac de 30 billes pour Houssam. Le 2 veut dire 2 voitures pour Sami. Le 50 veut dire 50 billes dans un sac. Qui a plus de billes ? On compare seulement les billes : 50 et 30. C'est Ramzi, car 50 > 30."),
        F("50 marbles > 30 marbles"),
    ]),
    ("Filter first, then compare", "نختار أولًا ثم نقارن", "D'abord trier, ensuite comparer", "43", [
        T("A table can hold many kinds of numbers. On Monday, April 5th: 25 present and 3 absent. Tuesday: 27 present and 1 absent. Wednesday: 23 present and 5 absent. If the question asks about absent students, we keep only the absent numbers: 3, 1 and 5. The greatest is 5, so Wednesday has the most absent students. Do not pick 27, because 27 is about present students.",
          "الجدول قد يحوي أنواعًا كثيرة من الأعداد. الاثنين 5 نيسان: 25 حاضرًا و3 غائبين. الثلاثاء: 27 حاضرًا وغائب واحد. الأربعاء: 23 حاضرًا و5 غائبين. إذا سألنا عن الغائبين نأخذ أعداد الغائبين فقط: 3 و1 و5. أكبرها 5 إذن الأربعاء فيه أكثر غائبين. لا نختار 27 لأنه عدد الحاضرين.",
          "Un tableau contient plusieurs sortes de nombres. Lundi 5 avril : 25 présents, 3 absents. Mardi : 27 présents, 1 absent. Mercredi : 23 présents, 5 absents. Si la question porte sur les absents, on garde seulement 3, 1 et 5. Le plus grand est 5 : mercredi. On ne prend pas 27, car il parle des présents."),
        F("absent: 3, 1, 5      greatest = 5 = Wednesday"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("A number has meaning only with its label. Read the question, find the number, find its label, filter, then compare if needed. Best habit: always say the number together with its label, like 50 marbles.",
          "العدد له معنى فقط مع عنوانه. نقرأ السؤال ثم نجد العدد ثم عنوانه ثم نختار المطلوب ونقارن إذا لزم. أفضل عادة: نقول العدد دائمًا مع عنوانه مثل 50 بلية.",
          "Un nombre n'a de sens qu'avec son étiquette. On lit la question, on trouve le nombre et son étiquette, on trie, puis on compare si besoin. Bonne habitude : dire le nombre avec son étiquette, comme 50 billes."),
        F("READ → FIND THE NUMBER → FIND ITS LABEL → FILTER → COMPARE → ANSWER"),
    ]),
]

EXERCISES = [
    EX("1", "42", st("There are 6 pencils and 12 colored crayons. What does 6 mean? What does 12 mean? Are there more crayons than pencils?",
                     "هناك 6 أقلام رصاص و12 قلم تلوين. ماذا يعني 6؟ وماذا يعني 12؟ هل أقلام التلوين أكثر؟",
                     "Il y a 6 crayons et 12 crayons de couleur. Que veut dire 6 ? Et 12 ? Y a-t-il plus de crayons de couleur ?"), [
        F("6 → 6 pencils      12 → 12 colored crayons"),
        T("Yes, there are more colored crayons, because 12 is more than 6.", "نعم، أقلام التلوين أكثر لأن 12 أكبر من 6.", "Oui, il y a plus de crayons de couleur, car 12 > 6."),
    ]),
    EX("2", "42", st("Jihad is 5 years old, Fadi is 8 and Naji is 4. How many children are there? Which number is Naji's age? Who is the eldest?",
                     "جهاد عمره 5 سنوات وفادي 8 وناجي 4. كم طفلًا هناك؟ أي عدد هو عمر ناجي؟ من الأكبر؟",
                     "Jihad a 5 ans, Fadi 8 ans, Naji 4 ans. Combien d'enfants ? Quel nombre est l'âge de Naji ? Qui est le plus âgé ?"), [
        F("3 children      Naji = 4 years      eldest = Fadi (8)"),
    ]),
    EX("3", "42", st("A box has 12 strawberry pies, 36 chocolate pies and 6 apple pies. What does 36 mean? What does 6 mean?",
                     "في الصندوق 12 فطيرة فريز و36 فطيرة شوكولا و6 فطائر تفاح. ماذا يعني 36؟ وماذا يعني 6؟",
                     "Une boîte contient 12 tartes aux fraises, 36 au chocolat et 6 aux pommes. Que veut dire 36 ? Et 6 ?"), [
        F("36 → chocolate pies      6 → apple pies      strawberry pies: 12"),
    ]),
    EX("4", "43", st("In Santa's list, who receives marbles, and who receives more?",
                     "في قائمة بابا نويل: من يأخذ بلايا ومن يأخذ أكثر؟",
                     "Dans la liste du Père Noël, qui reçoit des billes et qui en reçoit le plus ?"), [
        T("Only Ramzi and Houssam receive marbles: 50 and 30. Ramzi receives more, because 50 is more than 30.",
          "رمزي وحسّام فقط يأخذان بلايا: 50 و30. رمزي يأخذ أكثر لأن 50 أكبر من 30.",
          "Seuls Ramzi et Houssam reçoivent des billes : 50 et 30. Ramzi en reçoit plus, car 50 > 30."),
    ]),
    EX("5", "43", st("There are 25 red pearls, 68 yellow pearls, 46 blue pearls and 36 necklaces of 10 pearls each. What do 36 and 10 mean?",
                     "هناك 25 لؤلؤة حمراء و68 صفراء و46 زرقاء و36 عقدًا في كل عقد 10 لآلئ. ماذا يعنيان 36 و10؟",
                     "Il y a 25 perles rouges, 68 jaunes, 46 bleues et 36 colliers de 10 perles. Que veulent dire 36 et 10 ?"), [
        T("36 is the number of necklaces, not pearls. 10 is the number of pearls in each necklace.",
          "36 هو عدد العقود لا اللآلئ. و10 هو عدد اللآلئ في كل عقد.",
          "36 est le nombre de colliers, pas de perles. 10 est le nombre de perles dans chaque collier."),
    ]),
    EX("6", "43", st("Monday, April 5th: present 25, absent 3. Tuesday: present 27, absent 1. Wednesday: present 23, absent 5. Which day has the most absent students?",
                     "الاثنين 5 نيسان: حاضرون 25 وغائبون 3. الثلاثاء: حاضرون 27 وغائب 1. الأربعاء: حاضرون 23 وغائبون 5. أي يوم فيه أكبر عدد من الغائبين؟",
                     "Lundi 5 avril : 25 présents, 3 absents. Mardi : 27 présents, 1 absent. Mercredi : 23 présents, 5 absents. Quel jour y a-t-il le plus d'absents ?"), [
        F("absent: 3, 1, 5      greatest = 5"),
        T("Wednesday, April 7th has the most absent students.", "الأربعاء 7 نيسان فيه أكبر عدد من الغائبين.", "Le mercredi 7 avril, il y a le plus d'absents."),
    ]),
    EX("7", "", st("(our own) Thursday: present 24, absent 4. Friday: present 21, absent 7. Which day has more absent students?",
                   "(من عندنا) الخميس: حاضرون 24 وغائبون 4. الجمعة: حاضرون 21 وغائبون 7. أي يوم فيه غائبون أكثر؟",
                   "(notre exemple) Jeudi : 24 présents, 4 absents. Vendredi : 21 présents, 7 absents. Quel jour a plus d'absents ?"), [
        F("absent: 4 and 7      7 > 4"),
        T("Friday has more absent students.", "الجمعة فيها غائبون أكثر.", "Vendredi a plus d'absents."),
    ]),
]
