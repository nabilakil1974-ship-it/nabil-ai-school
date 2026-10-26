"""Grade 1 Mathematics — The numbers up to 79."""
from scripts.direct_lessons.common import T, F, EX, st, tens, numpath

LESSON_ID = "G01-MATH-EN-053"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "The numbers up to 79", "ar": "الأعداد حتى 79", "fr": "Les nombres jusqu'à 79"}

THEORY = [
    ("Seven tens make 70", "سبع عشرات تساوي 70", "Sept dizaines font 70", "132", [
        tens(7, 0, eq=True),
        T("Hello, champion! We know numbers up to 69. Today we go further. Seven bundles of ten make 70. Count the tens: one, two, three, four, five, six, seven. 7 tens = 70.",
          "مرحبًا يا بطل! نعرف الأعداد حتى 69. اليوم نذهب أبعد. سبع حزم من العشرة تساوي 70. نعدّ العشرات: واحد، اثنان، ثلاثة، أربعة، خمسة، ستة، سبعة. 7 عشرات = 70.",
          "Bonjour champion ! On connaît les nombres jusqu'à 69. Aujourd'hui on va plus loin. Sept paquets de dix font 70. On compte les dizaines : une, deux, … sept. 7 dizaines = 70."),
        F("7 tens = 70"),
    ]),
    ("Add the ones: 71 to 79", "نضيف الآحاد: من 71 إلى 79", "Ajouter les unités : de 71 à 79", "132", [
        tens(7, 1, eq=True),
        tens(7, 4, eq=True),
        tens(7, 9, eq=True),
        T("Keep the 7 tens and add loose ones. One loose one: 71. Four loose ones: 74. Nine loose ones: 79. The numbers from 70 to 79 always have 7 tens and from 0 to 9 ones. The tens digit 7 tells the complete tens; the ones digit tells the loose ones.",
          "نحتفظ بالعشرات السبع ونضيف آحادًا منفردة. واحد منفرد: 71. أربعة آحاد: 74. تسعة آحاد: 79. الأعداد من 70 إلى 79 فيها دائمًا 7 عشرات ومن 0 إلى 9 آحاد. رقم العشرات 7 يخبرنا بالعشرات الكاملة ورقم الآحاد يخبرنا بالآحاد المنفردة.",
          "On garde les 7 dizaines et on ajoute des unités seules. Une unité : 71. Quatre : 74. Neuf : 79. Les nombres de 70 à 79 ont toujours 7 dizaines et de 0 à 9 unités. Le chiffre des dizaines dit les dizaines entières, celui des unités dit les unités seules."),
        F("71 = 70 + 1      74 = 70 + 4      79 = 70 + 9"),
    ]),
    ("On the number path", "على مسار الأعداد", "Sur la droite numérique", "133", [
        numpath(["69", "70", "71", "72", "73", "74"], hi=1, size=48),
        T("After 69 comes 70: nine ones and one more make a new ten, so we have 7 tens. Then 71, 72, 73, 74 and so on to 79.",
          "بعد 69 يأتي 70: تسعة آحاد وواحد آخر تكوّن عشرة جديدة فيصير عندنا 7 عشرات. ثم 71 و72 و73 و74 وهكذا حتى 79.",
          "Après 69 vient 70 : neuf unités et une de plus forment une nouvelle dizaine, donc 7 dizaines. Puis 71, 72, 73, 74 … jusqu'à 79."),
    ]),
    ("Do not swap the digits", "لا نبدّل الرقمين", "Ne pas inverser les chiffres", "133", [
        tens(7, 2, eq=True),
        tens(2, 7, eq=True),
        T("72 is 7 tens and 2 ones. 27 is 2 tens and 7 ones. They are different numbers. The first digit tells the tens, the second digit tells the ones.",
          "72 هي 7 عشرات وواحدان. و27 هي عشرتان و7 آحاد. هما عددان مختلفان. الرقم الأول يخبرنا بالعشرات والثاني يخبرنا بالآحاد.",
          "72, c'est 7 dizaines et 2 unités. 27, c'est 2 dizaines et 7 unités. Ce sont deux nombres différents. Le premier chiffre dit les dizaines, le second les unités."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Numbers up to 79 use the same structure: seven tens plus the ones. For example 73 = 7 tens + 3 ones = 70 + 3.",
          "الأعداد حتى 79 لها البنية نفسها: سبع عشرات مع الآحاد. مثلًا 73 = 7 عشرات + 3 آحاد = 70 + 3.",
          "Les nombres jusqu'à 79 ont la même structure : sept dizaines plus les unités. Par exemple 73 = 7 dizaines + 3 unités = 70 + 3."),
        F("SEE THE TENS → COUNT THE ONES → BUILD OR READ THE NUMBER"),
    ]),
]

EXERCISES = [
    EX("1", "132", st("Read the model: 7 tens and 5 ones.", "اقرأ النموذج: 7 عشرات و5 آحاد.", "Lis le modèle : 7 dizaines et 5 unités."), [
        tens(7, 5, eq=True),
        T("70 + 5 = 75.", "70 + 5 = 75.", "70 + 5 = 75."),
    ]),
    EX("2", "132", st("Build 78.", "ابنِ العدد 78.", "Construis 78."), [
        tens(7, 8, eq=True),
        T("7 tens and 8 ones.", "7 عشرات و8 آحاد.", "7 dizaines et 8 unités."),
    ]),
    EX("3", "132", st("Decompose 76.", "حلّل العدد 76.", "Décompose 76."), [
        tens(7, 6, eq=True),
        F("76 = 7 tens + 6 ones = 70 + 6"),
    ]),
    EX("4", "133", st("What comes after 69? After 74? Before 79?", "ماذا بعد 69؟ وبعد 74؟ وقبل 79؟", "Que vient-il après 69 ? Après 74 ? Avant 79 ?"), [
        F("69 → 70      74 → 75      78 ← 79"),
    ]),
    EX("5", "133", st("Which is greater, 72 or 68? Why?", "أيهما أكبر 72 أم 68؟ لماذا؟", "Lequel est plus grand, 72 ou 68 ? Pourquoi ?"), [
        tens(7, 2, eq=True),
        tens(6, 8, eq=True),
        T("7 tens are more than 6 tens, so 72 is greater.", "7 عشرات أكثر من 6 عشرات إذن 72 أكبر.", "7 dizaines > 6 dizaines : 72 est plus grand."),
    ]),
    EX("6", "133", st("Error check: a child reads 72 as two tens and seven ones. What is wrong?", "تحقّق من الخطأ: قرأ طفل 72 على أنها عشرتان و7 آحاد. ما الخطأ؟", "Vérifie l'erreur : un enfant lit 72 comme 2 dizaines et 7 unités. Où est l'erreur ?"), [
        tens(7, 2, eq=True),
        T("He swapped the digits. 7 is in the tens place, so 72 = 7 tens + 2 ones.", "بدّل الرقمين. الرقم 7 في خانة العشرات إذن 72 = 7 عشرات + آحادان.", "Il a inversé les chiffres. Le 7 est aux dizaines : 72 = 7 dizaines + 2 unités."),
    ]),
    EX("7", "133", st("Challenge: put in order 77, 70, 74, 79.", "تحدٍّ: رتّب 77 و70 و74 و79.", "Défi : range 77, 70, 74, 79."), [
        numpath(["70", "74", "77", "79"], hi=None, size=56),
    ]),
    EX("8", "133", st("Final check: represent and decompose 73.", "تقييم أخير: مثّل العدد 73 وحلّله.", "Évaluation : représente et décompose 73."), [
        tens(7, 3, eq=True),
        F("73 = 7 tens + 3 ones = 70 + 3"),
    ]),
]
