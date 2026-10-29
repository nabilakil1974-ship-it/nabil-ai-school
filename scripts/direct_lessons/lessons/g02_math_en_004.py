"""Grade 2 Mathematics — Adding or Subtracting."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G02-MATH-EN-004"
GRADE = 2
SUBJECT = "math"
TITLES = {"en": "Adding or Subtracting", "ar": "الجمع أم الطرح", "fr": "Additionner ou soustraire"}


def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}


QUIZ = [
    {"q": "There are 8 counters and 3 are crossed out. How many are left?", "opts": ["5", "11", "3", "6"], "a": 0,
     "why": {"11": _w("Crossed-out counters are taken away, so we subtract: 8 − 3.", "الفيشات المشطوبة نزعناها فنطرح: 8 − 3.", "Les jetons barrés sont enlevés : on soustrait 8 − 3."),
             "3": _w("3 is how many were taken away, not how many are left.", "3 هو عدد ما أُخذ لا ما بقي.", "3 est ce qu'on a enlevé, pas ce qui reste."),
             "6": _w("Check: 6 + 3 = 9, not 8.", "تحقق: 6 + 3 = 9 وليس 8.", "Vérifie : 6 + 3 = 9, pas 8.")}, "ok": "8 − 3 = 5"},
    {"q": "On a number line you start at 12 and jump 4 to the left. Where do you land?", "opts": ["8", "16", "4", "9"], "a": 0,
     "why": {"16": _w("Left means subtract, so the number gets smaller.", "اليسار يعني طرحًا فالعدد يصغر.", "Gauche veut dire soustraire : le nombre diminue."),
             "4": _w("4 is the number of jumps, not the landing number.", "4 عدد القفزات لا العدد الذي نصل إليه.", "4 est le nombre de sauts."),
             "9": _w("Count four jumps: 11, 10, 9, 8.", "عدّ أربع قفزات: 11، 10، 9، 8.", "Compte quatre sauts : 11, 10, 9, 8.")}, "ok": "12 − 4 = 8"},
    {"q": "Which subtraction belongs to the same family as 4 + 3 = 7?", "opts": ["7 − 4 = 3", "7 − 3 = 7", "4 − 3 = 7", "3 − 4 = 7"], "a": 0,
     "why": {"7 − 3 = 7": _w("7 − 3 = 4.", "7 − 3 = 4.", "7 − 3 = 4."),
             "4 − 3 = 7": _w("4 − 3 = 1; the whole 7 comes first.", "4 − 3 = 1؛ الكل 7 يأتي أولًا.", "Le tout 7 vient en premier."),
             "3 − 4 = 7": _w("Start from the whole, 7.", "نبدأ من الكل 7.", "On part du tout, 7.")}, "ok": "7 − 4 = 3"},
]

THEORY = [
    ("Look at the action", "انظر إلى ما يحدث", "Regarde l'action", "18", [
        T("Hello, champion! Today we make an important choice: do I add or do I subtract? We do not choose because of a word. We look at what happened to the quantity. I had 5 counters and I added 2. The quantity became bigger: 5 + 2 = 7.",
          "مرحبًا يا بطل! اليوم عندنا قرار مهم: هل أجمع أم أطرح؟ لا نختار من كلمة معيّنة، بل ننظر ماذا حصل للكمية. كان عندي 5 فيشات وأضفت 2. صارت الكمية أكبر: 5 + 2 = 7.",
          "Bonjour champion ! Aujourd'hui, un choix important : j'additionne ou je soustrais ? On ne choisit pas à cause d'un mot, on regarde ce qui est arrivé à la quantité. J'avais 5 jetons et j'en ai ajouté 2 : 5 + 2 = 7."),
        F("5 + 2 = 7"),
        T("Now I have 7 and I take away 2. The quantity became smaller: 7 − 2 = 5.",
          "الآن عندي 7 وأخذت 2. صارت الكمية أصغر: 7 − 2 = 5.",
          "Maintenant j'ai 7 et j'en enlève 2. La quantité diminue : 7 − 2 = 5."),
        F("7 − 2 = 5"),
        T("Two groups joining together: use +. Objects that are there and then some are taken away: use −.",
          "مجموعتان تنضمّان معًا: نستعمل +. أشياء موجودة ثم أُخذ بعضها: نستعمل −.",
          "Deux groupes qui se joignent : +. Des objets enlevés : −."),
    ]),
    ("Number-line jumps", "القفزات على خط الأعداد", "Les sauts sur la droite numérique", "18", [
        T("On a number line, a jump to the right makes the number bigger: that is addition. A jump to the left makes it smaller: that is subtraction. Every jump here is worth 1. Start at 8 and make four jumps to the right: 9, 10, 11, 12.",
          "على خط الأعداد، القفز إلى اليمين يكبّر العدد: هذا جمع. والقفز إلى اليسار يصغّره: هذا طرح. كل قفزة قيمتها 1. نبدأ من 8 ونقفز أربع قفزات إلى اليمين: 9، 10، 11، 12.",
          "Sur la droite numérique, un saut vers la droite agrandit le nombre : c'est une addition. Un saut vers la gauche le diminue : c'est une soustraction. Chaque saut vaut 1. De 8, quatre sauts à droite : 9, 10, 11, 12."),
        F("8 + 4 = 12"),
        T("Now start at 12 and jump four to the left: 11, 10, 9, 8.",
          "الآن نبدأ من 12 ونقفز أربعًا إلى اليسار: 11، 10، 9، 8.",
          "Maintenant de 12, quatre sauts à gauche : 11, 10, 9, 8."),
        F("12 − 4 = 8"),
        F("RIGHT = +      LEFT = −"),
    ]),
    ("Read the picture", "اقرأ الصورة", "Lis l'image", "19", [
        T("Ask yourself: are two groups joining, or are some counters crossed out? Eight counters with 2 crossed out: 8 − 2 = 6. A group of 6 and a group of 5 joining: 6 + 5 = 11. If we cross out all 6 of 6 counters, nothing is left: 6 − 6 = 0.",
          "اسأل نفسك: هل مجموعتان تنضمّان أم فيشات مشطوبة؟ ثمانية فيشات شُطب منها 2: 8 − 2 = 6. مجموعة من 6 ومجموعة من 5 تنضمّان: 6 + 5 = 11. وإذا شطبنا كل الفيشات الـ6 لا يبقى شيء: 6 − 6 = 0.",
          "Demande-toi : deux groupes se joignent-ils, ou des jetons sont-ils barrés ? Huit jetons dont 2 barrés : 8 − 2 = 6. Un groupe de 6 et un groupe de 5 : 6 + 5 = 11. Si on barre les 6 jetons sur 6, il ne reste rien : 6 − 6 = 0."),
        F("8 − 2 = 6      6 + 5 = 11      6 − 6 = 0"),
    ]),
    ("Checking with the opposite", "نتحقق بالعملية المعاكسة", "Vérifier avec l'opération inverse", "19", [
        T("Addition and subtraction check each other. We found 8 − 3 = 5. To check, ask: is 5 + 3 equal to 8? Yes, so our answer is right.",
          "الجمع والطرح يتحققان من بعضهما. وجدنا 8 − 3 = 5. للتحقق نسأل: هل 5 + 3 = 8؟ نعم، إذن جوابنا صحيح.",
          "L'addition et la soustraction se vérifient l'une l'autre. 8 − 3 = 5. Pour vérifier : 5 + 3 = 8 ? Oui, donc c'est juste."),
        F("8 − 3 = 5      5 + 3 = 8"),
        F("10 − 6 = 4      4 + 6 = 10"),
    ]),
    ("Fact family", "عائلة الحقائق", "La famille de faits", "19", [
        T("Three numbers can tell several stories: part + part = whole, and whole − one part = the other part. With 4, 3 and 7 we get 4 + 3 = 7, 7 − 4 = 3 and 7 − 3 = 4.",
          "ثلاثة أعداد تحكي عدة حكايات: جزء + جزء = الكل، والكل − جزء = الجزء الآخر. مع 4 و3 و7 نحصل على 4 + 3 = 7 و7 − 4 = 3 و7 − 3 = 4.",
          "Trois nombres racontent plusieurs histoires : partie + partie = tout, et tout − une partie = l'autre partie. Avec 4, 3 et 7 : 4 + 3 = 7, 7 − 4 = 3 et 7 − 3 = 4."),
        F("4 + 3 = 7      7 − 4 = 3      7 − 3 = 4"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Watch the change, choose + or −, calculate, then check with the opposite operation. Joining means addition, taking away means subtraction. On a number line, right is + and left is −.",
          "نراقب التغيّر، نختار + أو −، نحسب، ثم نتحقق بالعملية المعاكسة. الضم جمع والأخذ طرح. على خط الأعداد اليمين + واليسار −.",
          "On observe le changement, on choisit + ou −, on calcule, puis on vérifie avec l'opération inverse. Joindre : addition ; enlever : soustraction. Droite : + ; gauche : −."),
        F("WATCH THE CHANGE → CHOOSE + OR − → CALCULATE → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "18", st("Complete: 6 and 5 join; 11 counters with 5 crossed out; 10 counters with 4 crossed out; 4 and 6 join.",
                    "أكمل: ضمّ 6 و5؛ 11 فيشة شُطب منها 5؛ 10 فيشات شُطب منها 4؛ ضمّ 4 و6.",
                    "Complète : 6 et 5 se joignent ; 11 jetons dont 5 barrés ; 10 jetons dont 4 barrés ; 4 et 6 se joignent."), [
        T("Two groups join, so we add: 6 + 4 = 10, one more is 11.", "مجموعتان تنضمّان فنجمع: 6 + 4 = 10 وواحد آخر يصبح 11.", "Deux groupes se joignent : 6 + 4 = 10, plus 1 = 11."),
        F("6 + 5 = 11      11 − 5 = 6      10 − 4 = 6      4 + 6 = 10"),
        T("Check: 6 + 5 = 11 and 6 + 4 = 10.", "تحقق: 6 + 5 = 11 و6 + 4 = 10.", "Vérification : 6 + 5 = 11 et 6 + 4 = 10."),
    ]),
    EX("2", "18", st("Use the number line: 8 + 4, 12 − 4, 8 + 6, 14 − 6.",
                    "استعمل خط الأعداد: 8 + 4، 12 − 4، 8 + 6، 14 − 6.",
                    "Avec la droite numérique : 8 + 4, 12 − 4, 8 + 6, 14 − 6."), [
        T("Right jumps add, left jumps subtract. From 8, six jumps right: 9, 10, 11, 12, 13, 14. From 14, six jumps left: back to 8.",
          "القفز يمينًا جمع ويسارًا طرح. من 8 ست قفزات يمينًا: 9، 10، 11، 12، 13، 14. ومن 14 ست قفزات يسارًا نعود إلى 8.",
          "Droite : on ajoute ; gauche : on soustrait. De 8, six sauts à droite : 14. De 14, six sauts à gauche : 8."),
        F("8 + 4 = 12      12 − 4 = 8      8 + 6 = 14      14 − 6 = 8"),
    ]),
    EX("3", "19", st("Write the equation for each picture: 8 counters, 2 crossed; groups 6 and 5; groups 5 and 3; 6 counters, all crossed.",
                    "اكتب المعادلة لكل صورة: 8 فيشات شُطب 2؛ مجموعتان 6 و5؛ مجموعتان 5 و3؛ 6 فيشات شُطبت كلها.",
                    "Écris l'égalité : 8 jetons dont 2 barrés ; groupes 6 et 5 ; groupes 5 et 3 ; 6 jetons tous barrés."), [
        F("8 − 2 = 6      6 + 5 = 11      5 + 3 = 8      6 − 6 = 0"),
        T("When we take away everything, 0 is left.", "إذا أخذنا كل الأشياء يبقى 0.", "Si on enlève tout, il reste 0."),
    ]),
    EX("4", "19", st("Write the equation: start 8, 8 jumps right; start 8, 5 jumps left; start 10, 4 right; start 5, 5 left.",
                    "اكتب المعادلة: ابدأ 8 و8 قفزات يمينًا؛ ابدأ 8 و5 قفزات يسارًا؛ ابدأ 10 و4 يمينًا؛ ابدأ 5 و5 يسارًا.",
                    "Écris l'égalité : départ 8, 8 sauts à droite ; 8, 5 à gauche ; 10, 4 à droite ; 5, 5 à gauche."), [
        F("8 + 8 = 16      8 − 5 = 3      10 + 4 = 14      5 − 5 = 0"),
    ]),
    EX("5", "19", st("Complete the pairs: 8 − 3 and 5 + 3; 10 − 6 and 4 + 6; 9 − 4 and 5 + 4.",
                    "أكمل الأزواج: 8 − 3 و5 + 3؛ 10 − 6 و4 + 6؛ 9 − 4 و5 + 4.",
                    "Complète les paires : 8 − 3 et 5 + 3 ; 10 − 6 et 4 + 6 ; 9 − 4 et 5 + 4."), [
        F("8 − 3 = 5      5 + 3 = 8"),
        F("10 − 6 = 4      4 + 6 = 10"),
        F("9 − 4 = 5      5 + 4 = 9"),
        T("Each pair checks the other one.", "كل زوج يتحقق من الآخر.", "Chaque paire vérifie l'autre."),
    ]),
    EX("6", "19", st("Fill in +, − or =: 7 _ 4 _ 3; 4 _ 3 _ 7; 7 _ 3 _ 4.",
                    "ضع +، − أو =: 7 _ 4 _ 3؛ 4 _ 3 _ 7؛ 7 _ 3 _ 4.",
                    "Mets +, − ou = : 7 _ 4 _ 3 ; 4 _ 3 _ 7 ; 7 _ 3 _ 4."), [
        F("7 − 4 = 3      4 + 3 = 7      7 − 3 = 4"),
    ]),
]
