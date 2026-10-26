"""Grade 1 Mathematics — Adding tens."""
from scripts.direct_lessons.common import T, F, EX, st, tens, numpath

LESSON_ID = "G01-MATH-EN-035"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Adding tens", "ar": "جمع العشرات", "fr": "Additionner des dizaines"}
TENS = ["20", "30", "40", "50", "60"]

THEORY = [
    ("A ten-bundle is one group of ten", "الحزمة عشرة واحدة", "Un paquet est un groupe de dix", "90", [
        T("Hello, champion! Last time we saw 20, 30, 40, 50, 60, and we knew that 20 is 2 tens, 30 is 3 tens, and so on. Today we do something new: we add tens to tens. Here are two bundles, each worth 10. If we put them together, how many tens do we have? Two tens, which is 20. So 10 + 10 = 20. And we did not count every stick one by one; we counted bundles of ten.",
          "مرحبًا يا بطل! في المرة الماضية رأينا 20 و30 و40 و50 و60 وعرفنا أن 20 هي عشرتان و30 ثلاث عشرات وهكذا. اليوم نفعل شيئًا جديدًا: نجمع عشرات مع عشرات. هنا حزمتان قيمة كل منهما 10. إذا جمعناهما فكم عشرة عندنا؟ عشرتان أي 20. إذن 10 + 10 = 20. ولم نعدّ كل عود وحده، بل عددنا حزم العشرات.",
          "Bonjour champion ! La dernière fois on a vu 20, 30, 40, 50, 60 et on a su que 20, c'est 2 dizaines, 30, 3 dizaines, etc. Aujourd'hui on fait du nouveau : on additionne des dizaines. Voici deux paquets, chacun vaut 10. Si on les réunit, combien de dizaines a-t-on ? Deux dizaines, soit 20. Donc 10 + 10 = 20. Et on n'a pas compté chaque bâton : on a compté des paquets de dix."),
        tens(2, 0, eq=True),
        F("10 + 10 = 20"),
    ]),
    ("Join tens, then count the bundles", "نجمع العشرات ثم نعدّ الحزم", "Réunir les dizaines puis compter les paquets", "90", [
        tens(2, 0, eq=True),
        tens(1, 0, eq=True),
        tens(3, 0, eq=True),
        T("Group A has 2 tens, which is 20. Group B has 1 ten, which is 10. When we join the two groups we get 3 bundles, so 3 tens, which is 30. So 20 + 10 = 30, because 2 tens + 1 ten = 3 tens.",
          "المجموعة A فيها عشرتان أي 20. والمجموعة B فيها عشرة واحدة أي 10. عندما نجمع المجموعتين نحصل على 3 حزم أي 3 عشرات أي 30. إذن 20 + 10 = 30 لأن عشرتين + عشرة = 3 عشرات.",
          "Le groupe A a 2 dizaines, soit 20. Le groupe B a 1 dizaine, soit 10. En réunissant on obtient 3 paquets, donc 3 dizaines, soit 30. Donc 20 + 10 = 30, car 2 dizaines + 1 dizaine = 3 dizaines."),
        F("20 + 10 = 30"),
    ]),
    ("20 + 20", "20 + 20", "20 + 20", "91", [
        tens(2, 0, eq=True),
        tens(2, 0, eq=True),
        tens(4, 0, eq=True),
        T("Each group has 20, that is 2 tens. 2 tens + 2 tens = 4 tens, and 4 tens is 40. So 20 + 20 = 40. We check by looking: one, two, three, four tens.",
          "في كل مجموعة 20 أي عشرتان. عشرتان + عشرتان = 4 عشرات، و4 عشرات تساوي 40. إذن 20 + 20 = 40. نتحقق بالنظر: عشرة، عشرتان، ثلاث، أربع عشرات.",
          "Chaque groupe a 20, soit 2 dizaines. 2 dizaines + 2 dizaines = 4 dizaines, et 4 dizaines, c'est 40. Donc 20 + 20 = 40. On vérifie en regardant : une, deux, trois, quatre dizaines."),
        F("2 tens + 2 tens = 4 tens      20 + 20 = 40"),
    ]),
    ("30 + 20", "30 + 20", "30 + 20", "91", [
        tens(3, 0, eq=True),
        tens(2, 0, eq=True),
        tens(5, 0, eq=True),
        T("30 is 3 tens and 20 is 2 tens. We join the bundles: 3 tens + 2 tens = 5 tens, and 5 tens is 50. So 30 + 20 = 50. Notice: we did not count 30 objects one by one. We thought in tens.",
          "30 هي 3 عشرات و20 هي عشرتان. نجمع الحزم: 3 عشرات + عشرتان = 5 عشرات، و5 عشرات تساوي 50. إذن 30 + 20 = 50. لاحظ: لم نعدّ 30 شيئًا واحدًا واحدًا بل فكّرنا بالعشرات.",
          "30, c'est 3 dizaines et 20, c'est 2 dizaines. On réunit les paquets : 3 dizaines + 2 dizaines = 5 dizaines, soit 50. Donc 30 + 20 = 50. Remarque : on n'a pas compté 30 objets un à un, on a pensé en dizaines."),
        F("30 + 20 = 50"),
    ]),
    ("Same total, a different view", "المجموع نفسه بنظرة مختلفة", "Même total, autre point de vue", "91", [
        tens(5, 0, eq=True),
        numpath(["20", "30", "40", "50"], hi=3, size=56),
        T("Let us check another way. With bundles: 3 tens and 2 tens together give 5 tens, which is 50. On the tens path: start at 30 and add two tens: 30, 40, 50. We reach the same answer. When two ways give the same total, that is a strong check.",
          "لنتحقق بطريقة أخرى. بالحزم: 3 عشرات وعشرتان معًا تعطيان 5 عشرات أي 50. وعلى مسار العشرات: نبدأ من 30 ونضيف عشرتين: 30، 40، 50. نصل إلى الجواب نفسه. عندما تعطي طريقتان المجموع نفسه فهذا تحقّق قوي.",
          "Vérifions autrement. Avec les paquets : 3 et 2 dizaines font 5 dizaines, soit 50. Sur la droite des dizaines : on part de 30 et on ajoute deux dizaines : 30, 40, 50. Même réponse. Quand deux façons donnent le même total, c'est une bonne vérification."),
    ]),
    ("Do not mix tens with ones", "لا نخلط العشرات بالآحاد", "Ne pas mélanger dizaines et unités", "91", [
        tens(4, 0, eq=True),
        tens(5, 0, eq=True),
        T("Here are 4 bundles: 40. If I add one bundle, what do we get? 50. Why not 41? Because we added one ten, not one object. One ten is 10. So 40 + 10 = 50.",
          "هنا 4 حزم: 40. إذا أضفت حزمة واحدة فماذا نحصل؟ 50. لماذا ليس 41؟ لأننا أضفنا عشرة واحدة لا شيئًا واحدًا. العشرة 10. إذن 40 + 10 = 50.",
          "Voici 4 paquets : 40. Si j'ajoute un paquet, qu'obtient-on ? 50. Pourquoi pas 41 ? Parce qu'on a ajouté une dizaine, pas un objet. Une dizaine vaut 10. Donc 40 + 10 = 50."),
        F("40 + 10 = 50"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("When we add tens, we do not have to count every object from the beginning. We think of the bundles. Every bundle is 10. So 20 + 30 means 2 tens + 3 tens = 5 tens = 50. If we doubt, we use another way: bundles or the tens path.",
          "عندما نجمع العشرات لا يلزم أن نعدّ كل شيء من البداية. نفكّر بالحزم. كل حزمة 10. إذن 20 + 30 تعني عشرتين + ثلاث عشرات = 5 عشرات = 50. وإذا شككنا نستعمل طريقة أخرى: الحزم أو مسار العشرات.",
          "Quand on additionne des dizaines, pas besoin de tout recompter. On pense aux paquets. Chaque paquet vaut 10. Donc 20 + 30, c'est 2 dizaines + 3 dizaines = 5 dizaines = 50. En cas de doute, on utilise une autre façon : les paquets ou la droite des dizaines."),
        F("SEE THE TENS → COUNT THE BUNDLES → JOIN → SAY THE TOTAL → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "90", st("Count the tens in 3 bundles.", "عدّ العشرات في 3 حزم.", "Compte les dizaines dans 3 paquets."), [
        tens(3, 0, eq=True),
        T("Count the bundles, not the small sticks: one ten, two tens, three tens. So 30.",
          "نعدّ الحزم لا الأعواد الصغيرة: عشرة، عشرتان، ثلاث عشرات. إذن 30.",
          "Compte les paquets, pas les petits bâtons : une dizaine, deux, trois. Donc 30."),
    ]),
    EX("2", "90", st("Build 20 + 10 with bundles.", "ابنِ 20 + 10 بالحزم.", "Construis 20 + 10 avec des paquets."), [
        tens(2, 0, eq=True),
        tens(3, 0, eq=True),
        T("Add a whole bundle, not one single object. Count all the bundles: 3 tens. Total 30.",
          "نضيف حزمة كاملة لا شيئًا واحدًا. نعدّ كل الحزم: 3 عشرات. المجموع 30.",
          "On ajoute un paquet entier, pas un seul objet. On compte tous les paquets : 3 dizaines. Total 30."),
        F("20 + 10 = 30"),
    ]),
    EX("3", "91", st("Solve 20 + 20 and say why.", "احسب 20 + 20 وقل السبب.", "Calcule 20 + 20 et dis pourquoi."), [
        tens(4, 0, eq=True),
        T("20 is 2 tens, and the other 20 is 2 tens. 2 tens + 2 tens = 4 tens, which is 40. Do not add digits quickly; turn each number into bundles.",
          "20 هي عشرتان والـ20 الأخرى عشرتان. عشرتان + عشرتان = 4 عشرات أي 40. لا تجمع الأرقام بسرعة، بل حوّل كل عدد إلى حزم.",
          "20, c'est 2 dizaines, et l'autre 20 aussi. 2 dizaines + 2 dizaines = 4 dizaines, soit 40. N'additionne pas les chiffres trop vite : transforme chaque nombre en paquets."),
        F("20 + 20 = 40"),
    ]),
    EX("4", "91", st("Your turn: 30 + 20.", "دورك: 30 + 20.", "À ton tour : 30 + 20."), [
        tens(5, 0, eq=True),
        T("30 is 3 tens. 20 is 2 tens. 3 tens + 2 tens = 5 tens. 5 tens is 50.",
          "30 هي 3 عشرات. و20 عشرتان. 3 عشرات + عشرتان = 5 عشرات. و5 عشرات تساوي 50.",
          "30, c'est 3 dizaines. 20, c'est 2 dizaines. 3 dizaines + 2 dizaines = 5 dizaines. 5 dizaines, c'est 50."),
        F("30 + 20 = 50"),
    ]),
    EX("5", "91", st("Check 20 + 30 with a second model.", "تحقّق من 20 + 30 بنموذج ثانٍ.", "Vérifie 20 + 30 avec un deuxième modèle."), [
        tens(5, 0, eq=True),
        numpath(["20", "30", "40", "50"], hi=3, size=56),
        T("Bundles: 2 tens + 3 tens = 5 tens = 50. Tens path: start at 20, add three tens: 30, 40, 50. We reached 50 again, so the answer is verified.",
          "بالحزم: عشرتان + 3 عشرات = 5 عشرات = 50. وعلى مسار العشرات: نبدأ من 20 ونضيف 3 عشرات: 30، 40، 50. وصلنا إلى 50 مرة ثانية، إذن الجواب محقَّق.",
          "Paquets : 2 dizaines + 3 dizaines = 5 dizaines = 50. Droite : on part de 20 et on ajoute trois dizaines : 30, 40, 50. On retrouve 50, la réponse est vérifiée."),
    ]),
    EX("6", "91", st("Error detective: which is right? A. 20 + 10 = 21. B. 20 + 10 = 30. C. 20 + 10 = 210.", "المحقق: أيها صحيح؟ A. 20 + 10 = 21. B. 20 + 10 = 30. C. 20 + 10 = 210.", "Détective : lequel est juste ? A. 20 + 10 = 21. B. 20 + 10 = 30. C. 20 + 10 = 210."), [
        tens(3, 0, eq=True),
        T("B is right. 20 is 2 tens, 10 is 1 ten, and 2 tens + 1 ten = 3 tens = 30. 10 is not one; 10 is one ten.",
          "B صحيحة. 20 هي عشرتان و10 عشرة واحدة، وعشرتان + عشرة = 3 عشرات = 30. العدد 10 ليس واحدًا بل عشرة واحدة.",
          "B est juste. 20, c'est 2 dizaines, 10, c'est 1 dizaine, et 2 dizaines + 1 dizaine = 3 dizaines = 30. 10 n'est pas un : 10, c'est une dizaine."),
    ]),
    EX("7", "91", st("Challenge: 20 cubes in tens, plus 20 cubes in tens, plus 10 cubes in one ten. How many in all?", "تحدٍّ: 20 مكعبًا في عشرات، و20 مكعبًا في عشرات، و10 مكعبات في عشرة. كم المجموع؟", "Défi : 20 cubes en dizaines, plus 20 cubes en dizaines, plus 10 cubes en une dizaine. Combien en tout ?"), [
        tens(5, 0, eq=True),
        T("Turn them into tens: 2 tens, 2 tens and 1 ten. 2 + 2 + 1 = 5 tens, which is 50.",
          "نحوّلها إلى عشرات: عشرتان وعشرتان وعشرة. 2 + 2 + 1 = 5 عشرات أي 50.",
          "Transforme en dizaines : 2, 2 et 1 dizaines. 2 + 2 + 1 = 5 dizaines, soit 50."),
        F("20 + 20 + 10 = 50"),
    ]),
    EX("8", "91", st("Final check: 10 + 10, 20 + 10, 20 + 20, 30 + 20, and why is 40 + 10 = 50?", "تقييم أخير: 10 + 10 و20 + 10 و20 + 20 و30 + 20، ولماذا 40 + 10 = 50؟", "Évaluation : 10 + 10, 20 + 10, 20 + 20, 30 + 20, et pourquoi 40 + 10 = 50 ?"), [
        F("10 + 10 = 20      20 + 10 = 30      20 + 20 = 40      30 + 20 = 50"),
        T("40 is 4 tens and 10 is 1 ten. 4 tens + 1 ten = 5 tens = 50.",
          "40 هي 4 عشرات و10 عشرة. 4 عشرات + عشرة = 5 عشرات = 50.",
          "40, c'est 4 dizaines et 10, c'est 1 dizaine. 4 dizaines + 1 dizaine = 5 dizaines = 50."),
    ]),
]
