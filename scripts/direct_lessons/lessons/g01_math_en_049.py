"""Grade 1 Mathematics — The sign “-”."""
from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.lessons.g01_math_en_048 import takeaway

LESSON_ID = "G01-MATH-EN-049"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "The sign “−”", "ar": "إشارة «−»", "fr": "Le signe « − »"}

THEORY = [
    ("A sign for taking away", "إشارة للأخذ", "Un signe pour retirer", "124", [
        takeaway(6, 2),
        T("Hello, champion! Here we start with 6 counters and take away 2. 4 remain. Mathematics has a short sign to write this action: the minus sign “−”. It means: take away.",
          "مرحبًا يا بطل! نبدأ هنا بـ6 قطع ونأخذ منها 2. يبقى 4. وللرياضيات إشارة قصيرة لكتابة هذا الفعل: إشارة الناقص «−». ومعناها: نأخذ.",
          "Bonjour champion ! On part de 6 jetons et on en retire 2. Il en reste 4. En mathématiques, un petit signe écrit cette action : le signe moins « − ». Il veut dire : retirer."),
        F("6 − 2 = 4"),
    ]),
    ("How to read it, in order", "كيف نقرؤها بالترتيب", "Comment la lire, dans l'ordre", "124", [
        F("6 − 2 = 4"),
        T("The number before “−” is the starting quantity: 6. The number after “−” is the quantity removed: 2. The number after “=” is what remains: 4. We read it: six minus two equals four, or six take away two leaves four.",
          "العدد قبل «−» هو الكمية الأولى: 6. والعدد بعد «−» هو الكمية المأخوذة: 2. والعدد بعد «=» هو الباقي: 4. نقرؤها: ستة ناقص اثنين يساوي أربعة، أو ستة نأخذ منها اثنين يبقى أربعة.",
          "Le nombre avant « − » est la quantité de départ : 6. Celui après est la quantité retirée : 2. Celui après « = » est le reste : 4. On lit : six moins deux égale quatre."),
    ]),
    ("Order matters", "الترتيب مهم", "L'ordre compte", "125", [
        F("6 − 2 = 4        but not        2 − 6"),
        T("We always write the starting quantity first. 6 − 2 is right for starting with 6 and removing 2. 2 − 6 would mean starting with 2 and removing 6, which is a different story. The minus sign is only for taking away, never for putting quantities together.",
          "نكتب الكمية الأولى دائمًا أولًا. 6 − 2 صحيحة لمن يبدأ بـ6 ويأخذ 2. أما 2 − 6 فتعني أن نبدأ بـ2 ونأخذ 6، وهذه قصة أخرى. إشارة الناقص للأخذ فقط وليست لضمّ الكميات.",
          "On écrit toujours la quantité de départ en premier. 6 − 2 convient si on part de 6 et retire 2. 2 − 6 raconterait une autre histoire. Le signe moins sert à retirer, jamais à réunir."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("The sign “−” records subtraction. Start number, minus sign, removed number, equals, what remains.",
          "إشارة «−» تسجّل الطرح: العدد الأول، ثم الناقص، ثم العدد المأخوذ، ثم يساوي، ثم الباقي.",
          "Le signe « − » note la soustraction : nombre de départ, moins, nombre retiré, égale, reste."),
        F("START − REMOVED = REMAINS"),
    ]),
]

EXERCISES = [
    EX("1", "124", st("Write the subtraction: 5 counters, 1 removed.", "اكتب عملية الطرح: 5 قطع أُخذت منها 1.", "Écris la soustraction : 5 jetons, 1 retiré."), [
        takeaway(5, 1),
        F("5 − 1 = 4"),
    ]),
    EX("2", "124", st("Write the subtraction: 8 counters, 3 removed.", "اكتب عملية الطرح: 8 قطع أُخذت منها 3.", "Écris la soustraction : 8 jetons, 3 retirés."), [
        takeaway(8, 3),
        F("8 − 3 = 5"),
    ]),
    EX("3", "124", st("Read 9 − 4 = 5 aloud.", "اقرأ 9 − 4 = 5 بصوت عالٍ.", "Lis 9 − 4 = 5 à voix haute."), [
        F("9 − 4 = 5"),
        T("Nine minus four equals five: start with 9, take away 4, 5 remain.", "تسعة ناقص أربعة يساوي خمسة: نبدأ بـ9 ونأخذ 4 فيبقى 5.", "Neuf moins quatre égale cinq : on part de 9, on retire 4, il reste 5."),
    ]),
    EX("4", "125", st("Which number is the starting quantity in 7 − 2 = 5?", "أيّ عدد هو الكمية الأولى في 7 − 2 = 5؟", "Quel nombre est la quantité de départ dans 7 − 2 = 5 ?"), [
        F("7 − 2 = 5"),
        T("The first one: 7. The 2 is removed and the 5 remains.", "الأول: 7. والـ2 هي المأخوذة والـ5 هي الباقية.", "Le premier : 7. Le 2 est retiré et le 5 reste."),
    ]),
    EX("5", "125", st("Match: 10 counters, 4 removed. Which sentence is right: 4 − 10 or 10 − 4?", "طابق: 10 قطع أُخذت منها 4. أيّ جملة صحيحة: 4 − 10 أم 10 − 4؟", "Associe : 10 jetons, 4 retirés. Quelle écriture est juste : 4 − 10 ou 10 − 4 ?"), [
        takeaway(10, 4),
        F("10 − 4 = 6"),
    ]),
    EX("6", "125", st("Error check: 3 counters and 2 more are put together. A child writes 3 − 2. Is that right?", "تحقّق من الخطأ: 3 قطع ونضم إليها 2. كتب طفل 3 − 2. هل هذا صحيح؟", "Vérifie l'erreur : 3 jetons et on en réunit 2 de plus. Un enfant écrit 3 − 2. Est-ce juste ?"), [
        F("3 + 2 = 5"),
        T("No. We are putting together, not taking away, so the sign must be plus.", "لا. نحن نضمّ لا نأخذ، فالإشارة يجب أن تكون زائد.", "Non. On réunit, on ne retire pas : le signe doit être plus."),
    ]),
    EX("7", "125", st("Challenge: 12 counters, 2 removed. Write the sentence.", "تحدٍّ: 12 قطعة أُخذت منها 2. اكتب الجملة.", "Défi : 12 jetons, 2 retirés. Écris l'égalité."), [
        takeaway(12, 2),
        F("12 − 2 = 10"),
    ]),
    EX("8", "125", st("Final check: write the sentence for 7 counters with 5 removed.", "تقييم أخير: اكتب الجملة لـ7 قطع أُخذت منها 5.", "Évaluation : écris l'égalité pour 7 jetons dont 5 retirés."), [
        takeaway(7, 5),
        F("7 − 5 = 2"),
    ]),
]
