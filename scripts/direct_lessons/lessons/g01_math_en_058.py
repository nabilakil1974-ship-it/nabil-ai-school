"""Grade 1 Mathematics — Order of numbers."""
from scripts.direct_lessons.common import T, F, EX, st, tens, numpath

LESSON_ID = "G01-MATH-EN-058"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Order of numbers", "ar": "ترتيب الأعداد", "fr": "Ranger les nombres"}

THEORY = [
    ("Ascending and descending", "ترتيب تصاعدي وتنازلي", "Ordre croissant et décroissant", "150", [
        numpath(["23", "47", "58", "72", "91"], hi=None, size=54),
        T("Hello, champion! Ascending order goes from the smaller number to the larger number: 23, 47, 58, 72, 91. Descending order goes the other way, from the larger to the smaller: 91, 72, 58, 47, 23. First we must know which direction is asked.",
          "مرحبًا يا بطل! الترتيب التصاعدي من العدد الأصغر إلى الأكبر: 23، 47، 58، 72، 91. والترتيب التنازلي في الاتجاه المعاكس، من الأكبر إلى الأصغر: 91، 72، 58، 47، 23. علينا أولًا أن نعرف الاتجاه المطلوب.",
          "L'ordre croissant va du plus petit au plus grand : 23, 47, 58, 72, 91. L'ordre décroissant va dans l'autre sens : 91, 72, 58, 47, 23. D'abord, on repère le sens demandé."),
        numpath(["91", "72", "58", "47", "23"], hi=None, size=54),
    ]),
    ("Compare the tens, then the ones", "نقارن العشرات ثم الآحاد", "On compare les dizaines puis les unités", "150", [
        tens(6, 4, eq=True),
        tens(6, 9, eq=True),
        tens(8, 1, eq=True),
        T("64 and 69 have the same tens (6), so we compare the ones: 4 < 9, so 64 < 69. 81 has 8 tens, more than 6 tens, so 81 is the greatest. Ascending: 64, 69, 81.",
          "في 64 و69 العشرات نفسها (6) فنقارن الآحاد: 4 < 9 إذن 64 < 69. وفي 81 ثماني عشرات وهي أكثر من 6 عشرات فـ81 هو الأكبر. تصاعديًا: 64، 69، 81.",
          "64 et 69 ont les mêmes dizaines (6) : on compare les unités, 4 < 9, donc 64 < 69. 81 a 8 dizaines, plus que 6 : c'est le plus grand. Croissant : 64, 69, 81."),
    ]),
    ("Check on the number path", "نتحقق على مسار الأعداد", "Vérifier sur la droite", "151", [
        numpath(["64", "69", "81"], hi=None, size=60),
        T("On the number path, the numbers further to the right are greater. Reading left to right is ascending; reading right to left is descending.",
          "على مسار الأعداد الأعداد الأبعد إلى اليمين هي الأكبر. القراءة من اليسار إلى اليمين تصاعدية ومن اليمين إلى اليسار تنازلية.",
          "Sur la droite, les nombres les plus à droite sont les plus grands. De gauche à droite : croissant ; de droite à gauche : décroissant."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("To order numbers: name the direction, compare the tens, and if they are equal compare the ones. Check on the number path.",
          "لترتيب الأعداد: نسمّي الاتجاه ثم نقارن العشرات وإذا تساوت نقارن الآحاد ثم نتحقق على المسار.",
          "Pour ranger : nommer le sens, comparer les dizaines, puis les unités si elles sont égales, et vérifier sur la droite."),
        F("DIRECTION → TENS → ONES → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "150", st("Order from smallest to greatest: 45, 12, 78, 30.", "رتّب من الأصغر إلى الأكبر: 45، 12، 78، 30.", "Range du plus petit au plus grand : 45, 12, 78, 30."), [
        numpath(["12", "30", "45", "78"], hi=None, size=56),
    ]),
    EX("2", "150", st("Order from greatest to smallest: 56, 91, 29, 63.", "رتّب من الأكبر إلى الأصغر: 56، 91، 29، 63.", "Range du plus grand au plus petit : 56, 91, 29, 63."), [
        numpath(["91", "63", "56", "29"], hi=None, size=56),
    ]),
    EX("3", "150", st("Which is greater, 74 or 47?", "أيهما أكبر 74 أم 47؟", "Lequel est plus grand, 74 ou 47 ?"), [
        tens(7, 4, eq=True),
        tens(4, 7, eq=True),
        T("7 tens are more than 4 tens, so 74 is greater.", "7 عشرات أكثر من 4 عشرات إذن 74 أكبر.", "7 dizaines > 4 dizaines : 74 est plus grand."),
    ]),
    EX("4", "151", st("Order ascending: 83, 38, 88, 80.", "رتّب تصاعديًا: 83، 38، 88، 80.", "Range dans l'ordre croissant : 83, 38, 88, 80."), [
        numpath(["38", "80", "83", "88"], hi=None, size=56),
        T("38 has the fewest tens. The three others have 8 tens, so compare ones: 0, 3, 8.", "في 38 أقل عشرات. والثلاثة الباقية فيها 8 عشرات فنقارن الآحاد: 0 ثم 3 ثم 8.", "38 a le moins de dizaines. Les trois autres ont 8 dizaines : on compare les unités 0, 3, 8."),
    ]),
    EX("5", "151", st("Write the number just before and just after 59.", "اكتب العدد قبل 59 مباشرة وبعدها مباشرة.", "Écris le nombre juste avant et juste après 59."), [
        F("58, 59, 60"),
    ]),
    EX("6", "151", st("Error check: a child says ascending for 40, 25, 61 is 61, 40, 25. What went wrong?", "تحقّق من الخطأ: قال طفل إن التصاعدي لـ40 و25 و61 هو 61، 40، 25. ما الخطأ؟", "Vérifie l'erreur : un enfant dit que croissant pour 40, 25, 61 est 61, 40, 25. Où est l'erreur ?"), [
        numpath(["25", "40", "61"], hi=None, size=60),
        T("He went in the descending direction. Ascending is from smallest: 25, 40, 61.", "سار في الاتجاه التنازلي. التصاعدي يبدأ بالأصغر: 25، 40، 61.", "Il est parti dans le sens décroissant. Croissant commence par le plus petit : 25, 40, 61."),
    ]),
    EX("7", "151", st("Challenge: put 99, 9, 90, 19 in descending order.", "تحدٍّ: رتّب 99 و9 و90 و19 تنازليًا.", "Défi : range 99, 9, 90, 19 dans l'ordre décroissant."), [
        numpath(["99", "90", "19", "9"], hi=None, size=56),
        T("9 has no tens, so it is the smallest.", "العدد 9 بلا عشرات فهو الأصغر.", "9 n'a pas de dizaine : c'est le plus petit."),
    ]),
    EX("8", "151", st("Final check: order 67, 76, 66 and name the direction.", "تقييم أخير: رتّب 67 و76 و66 وسمِّ الاتجاه.", "Évaluation : range 67, 76, 66 et nomme le sens."), [
        numpath(["66", "67", "76"], hi=None, size=60),
        T("Ascending: 66, 67, 76. 66 and 67 have the same tens, and 6 < 7. 76 has more tens.", "تصاعديًا: 66، 67، 76. في 66 و67 العشرات نفسها و6 < 7. وفي 76 عشرات أكثر.", "Croissant : 66, 67, 76. 66 et 67 ont les mêmes dizaines, 6 < 7. 76 a plus de dizaines."),
    ]),
]
