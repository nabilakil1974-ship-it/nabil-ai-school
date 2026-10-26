"""Grade 1 Mathematics — Add tens."""
from scripts.direct_lessons.common import T, F, EX, st, tens, numpath

LESSON_ID = "G01-MATH-EN-040"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Add tens", "ar": "جمع العشرات", "fr": "Additionner des dizaines"}

THEORY = [
    ("Two collections made of tens", "مجموعتان من العشرات", "Deux collections de dizaines", "104", [
        tens(2, 0, tag="A", eq=True),
        tens(3, 0, tag="B", eq=True),
        T("Hello, champion! Here are two collections made only of tens: 20 and 30. How many complete tens are there altogether? 2 tens and 3 tens make 5 tens. We do not need to count single units; we only add the number of tens.",
          "مرحبًا يا بطل! هنا مجموعتان من العشرات فقط: 20 و30. كم عشرة كاملة عندنا معًا؟ عشرتان و3 عشرات تعطي 5 عشرات. لا نحتاج إلى عدّ الآحاد، بل نجمع عدد العشرات فقط.",
          "Bonjour champion ! Voici deux collections de dizaines : 20 et 30. Combien de dizaines entières en tout ? 2 dizaines et 3 dizaines font 5 dizaines. On ne compte pas les unités : on additionne seulement le nombre de dizaines."),
        F("2 tens + 3 tens = 5 tens"),
    ]),
    ("5 tens is 50", "5 عشرات تساوي 50", "5 dizaines, c'est 50", "104", [
        tens(5, 0, eq=True),
        F("20 + 30 = 50"),
        T("Because each bundle is ten, 5 bundles are 50. So 20 + 30 = 50. The equation and the bundles tell the same story.",
          "ولأن كل حزمة عشرة فإن 5 حزم تساوي 50. إذن 20 + 30 = 50. المعادلة والحزم تحكيان القصة نفسها.",
          "Comme chaque paquet vaut dix, 5 paquets font 50. Donc 20 + 30 = 50. L'égalité et les paquets racontent la même histoire."),
    ]),
    ("The same addition on the tens path", "الجمع نفسه على مسار العشرات", "La même addition sur la droite des dizaines", "105", [
        numpath(["20", "30", "40", "50"], hi=3, size=56),
        T("On the tens path we start at 20 and jump three tens: 30, 40, 50. We land on 50, the same answer as the bundles. When bundles, path and equation agree, we are sure.",
          "على مسار العشرات نبدأ من 20 ونقفز 3 عشرات: 30 و40 و50. نصل إلى 50، الجواب نفسه كما في الحزم. وعندما تتفق الحزم والمسار والمعادلة نكون متأكدين.",
          "Sur la droite des dizaines on part de 20 et on saute trois dizaines : 30, 40, 50. On arrive à 50, comme avec les paquets. Quand paquets, droite et égalité sont d'accord, on est sûr."),
        F("20 + 30 = 50"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Adding tens means joining complete groups of ten. We add the number of tens, and each group stays a ten. For example 10 + 40 = 50 because 1 ten + 4 tens = 5 tens.",
          "جمع العشرات يعني ضمّ مجموعات كاملة من العشرة. نجمع عدد العشرات وتبقى كل مجموعة عشرة. مثلًا 10 + 40 = 50 لأن عشرة + 4 عشرات = 5 عشرات.",
          "Additionner des dizaines, c'est réunir des groupes entiers de dix. On additionne le nombre de dizaines. Par exemple 10 + 40 = 50 car 1 dizaine + 4 dizaines = 5 dizaines."),
        F("COUNT THE TENS → ADD THE TENS → SAY THE TOTAL → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "104", st("How many tens in 20 and 30 together?", "كم عشرة في 20 و30 معًا؟", "Combien de dizaines dans 20 et 30 ensemble ?"), [
        tens(5, 0, eq=True),
        T("2 tens + 3 tens = 5 tens.", "عشرتان + 3 عشرات = 5 عشرات.", "2 dizaines + 3 dizaines = 5 dizaines."),
    ]),
    EX("2", "104", st("Solve 10 + 30.", "احسب 10 + 30.", "Calcule 10 + 30."), [
        tens(4, 0, eq=True),
        T("1 ten + 3 tens = 4 tens, which is 40.", "عشرة + 3 عشرات = 4 عشرات أي 40.", "1 dizaine + 3 dizaines = 4 dizaines, soit 40."),
        F("10 + 30 = 40"),
    ]),
    EX("3", "104", st("Solve 20 + 40.", "احسب 20 + 40.", "Calcule 20 + 40."), [
        tens(6, 0, eq=True),
        T("2 tens + 4 tens = 6 tens, which is 60.", "عشرتان + 4 عشرات = 6 عشرات أي 60.", "2 dizaines + 4 dizaines = 6 dizaines, soit 60."),
        F("20 + 40 = 60"),
    ]),
    EX("4", "105", st("Show 30 + 20 on the tens path.", "أظهر 30 + 20 على مسار العشرات.", "Montre 30 + 20 sur la droite des dizaines."), [
        numpath(["30", "40", "50"], hi=2, size=60),
        T("Start at 30 and jump two tens: 40, 50. So 30 + 20 = 50.",
          "نبدأ من 30 ونقفز عشرتين: 40 و50. إذن 30 + 20 = 50.",
          "On part de 30 et on saute deux dizaines : 40, 50. Donc 30 + 20 = 50."),
    ]),
    EX("5", "105", st("Complete: 40 + __ = 60.", "أكمل: 40 + __ = 60.", "Complète : 40 + __ = 60."), [
        tens(4, 0, eq=True),
        tens(6, 0, eq=True),
        T("4 tens need 2 more tens to reach 6 tens. So 40 + 20 = 60.",
          "تحتاج 4 عشرات إلى عشرتين أخريين لتصل إلى 6 عشرات. إذن 40 + 20 = 60.",
          "4 dizaines + 2 dizaines = 6 dizaines. Donc 40 + 20 = 60."),
    ]),
    EX("6", "105", st("Error detective: 20 + 30 = 5. What was forgotten?", "المحقق: 20 + 30 = 5. ماذا نُسي؟", "Détective : 20 + 30 = 5. Qu'a-t-on oublié ?"), [
        tens(5, 0, eq=True),
        T("The child counted 5 bundles but forgot that each bundle is a ten. 5 tens is 50.",
          "عدّ الطفل 5 حزم لكنه نسي أن كل حزمة عشرة. 5 عشرات = 50.",
          "L'enfant a compté 5 paquets mais a oublié que chaque paquet vaut dix. 5 dizaines = 50."),
    ]),
    EX("7", "105", st("Challenge: 10 + 20 + 30.", "تحدٍّ: 10 + 20 + 30.", "Défi : 10 + 20 + 30."), [
        tens(6, 0, eq=True),
        T("1 ten + 2 tens + 3 tens = 6 tens = 60.", "عشرة + عشرتان + 3 عشرات = 6 عشرات = 60.", "1 + 2 + 3 dizaines = 6 dizaines = 60."),
        F("10 + 20 + 30 = 60"),
    ]),
    EX("8", "105", st("Final check: solve 30 + 30 and justify with groups of ten.", "تقييم أخير: احسب 30 + 30 وبرّر بمجموعات العشرة.", "Évaluation : calcule 30 + 30 et justifie avec des groupes de dix."), [
        tens(6, 0, eq=True),
        T("3 tens + 3 tens = 6 tens, and 6 tens is 60.", "3 عشرات + 3 عشرات = 6 عشرات، و6 عشرات تساوي 60.", "3 dizaines + 3 dizaines = 6 dizaines, soit 60."),
        F("30 + 30 = 60"),
    ]),
]
