"""Grade 1 Mathematics — Order of numbers up to 69."""
from scripts.direct_lessons.common import T, F, EX, st, tens, numpath

LESSON_ID = "G01-MATH-EN-037"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Order of numbers up to 69", "ar": "ترتيب الأعداد حتى 69", "fr": "Ranger les nombres jusqu'à 69"}

THEORY = [
    ("Numbers out of order", "أعداد غير مرتبة", "Des nombres dans le désordre", "96", [
        F("52     38     61     45     29"),
        T("Hello, champion! Here are some numbers, all mixed up. We want to put them in order from the smallest to the largest. We will not guess by the shape of the digits. We will use the tens and the ones, and then check on the number path.",
          "مرحبًا يا بطل! هذه أعداد مختلطة. نريد ترتيبها من الأصغر إلى الأكبر. لن نخمّن من شكل الأرقام، بل نستعمل العشرات والآحاد ثم نتحقق على مسار الأعداد.",
          "Bonjour champion ! Voici des nombres en désordre. On veut les ranger du plus petit au plus grand. On ne devine pas d'après la forme des chiffres : on utilise les dizaines et les unités, puis on vérifie sur la droite numérique."),
        numpath(["29", "38", "45", "52", "61"], hi=None, size=56),
    ]),
    ("Compare the tens first", "نقارن العشرات أولًا", "On compare d'abord les dizaines", "96", [
        tens(3, 8, eq=True),
        tens(5, 2, eq=True),
        T("Compare 38 and 52. 38 has 3 tens; 52 has 5 tens. More tens means a greater number, so 52 is greater than 38. We do not even need to look at the ones.",
          "نقارن 38 و52. في 38 ثلاث عشرات وفي 52 خمس عشرات. عشرات أكثر تعني عددًا أكبر، إذن 52 أكبر من 38. ولا نحتاج حتى إلى النظر إلى الآحاد.",
          "Comparons 38 et 52. 38 a 3 dizaines ; 52 a 5 dizaines. Plus de dizaines, c'est un nombre plus grand : 52 est plus grand que 38. On n'a même pas besoin de regarder les unités."),
        F("3 tens < 5 tens, so 38 < 52"),
    ]),
    ("Equal tens: compare the ones", "إذا تساوت العشرات نقارن الآحاد", "Dizaines égales : on compare les unités", "97", [
        tens(4, 3, eq=True),
        tens(4, 7, eq=True),
        T("Compare 43 and 47. Both have 4 tens, so the tens are equal. Now compare the ones: 3 is less than 7. So 43 is less than 47.",
          "نقارن 43 و47. في كليهما 4 عشرات، فالعشرات متساوية. الآن نقارن الآحاد: 3 أصغر من 7. إذن 43 أصغر من 47.",
          "Comparons 43 et 47. Les deux ont 4 dizaines : égales. On compare alors les unités : 3 est plus petit que 7. Donc 43 < 47."),
        F("4 tens = 4 tens;  3 ones < 7 ones;  43 < 47"),
    ]),
    ("Before and after", "العدد قبل والعدد بعد", "Avant et après", "97", [
        numpath(["46", "47", "48"], hi=1, size=64),
        T("The number before 47 is 46, and the number after 47 is 48. We move one step back or one step forward on the counting sequence. Be careful when the ones reach 9: after 49 comes 50, a new ten.",
          "العدد الذي قبل 47 هو 46 والذي بعده 48. نتحرك خطوة إلى الوراء أو خطوة إلى الأمام في متتالية العد. وانتبه عندما تصل الآحاد إلى 9: بعد 49 يأتي 50، عشرة جديدة.",
          "Le nombre avant 47 est 46, après 47 c'est 48. On fait un pas en arrière ou en avant dans la suite. Attention quand les unités arrivent à 9 : après 49 vient 50, une nouvelle dizaine."),
        numpath(["48", "49", "50"], hi=2, size=64),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("To order two-digit numbers, compare the tens first. More tens means a greater number. If the tens are equal, compare the ones. Then check on the counting sequence or with tens-and-ones models.",
          "لترتيب الأعداد المكوّنة من رقمين نقارن العشرات أولًا. عشرات أكثر تعني عددًا أكبر. وإذا تساوت العشرات نقارن الآحاد. ثم نتحقق على متتالية العد أو بنماذج العشرات والآحاد.",
          "Pour ranger des nombres à deux chiffres, on compare d'abord les dizaines. Plus de dizaines, nombre plus grand. Si elles sont égales, on compare les unités. On vérifie ensuite sur la suite ou avec les modèles."),
        F("TENS FIRST → THEN ONES → CHECK ON THE PATH"),
    ]),
]

EXERCISES = [
    EX("1", "96", st("Put in order from smallest to largest: 52, 38, 61, 45, 29.", "رتّب من الأصغر إلى الأكبر: 52، 38، 61، 45، 29.", "Range du plus petit au plus grand : 52, 38, 61, 45, 29."), [
        T("Tens: 5, 3, 6, 4, 2. Smallest tens first: 29, 38, 45, 52, 61.",
          "العشرات: 5 و3 و6 و4 و2. نبدأ بأقل العشرات: 29، 38، 45، 52، 61.",
          "Dizaines : 5, 3, 6, 4, 2. On range : 29, 38, 45, 52, 61."),
        numpath(["29", "38", "45", "52", "61"], hi=None, size=56),
    ]),
    EX("2", "96", st("Put in order from largest to smallest: 34, 56, 41, 63.", "رتّب من الأكبر إلى الأصغر: 34، 56، 41، 63.", "Range du plus grand au plus petit : 34, 56, 41, 63."), [
        T("The greatest tens first: 63, 56, 41, 34.",
          "نبدأ بأكبر العشرات: 63، 56، 41، 34.",
          "On commence par les plus grandes dizaines : 63, 56, 41, 34."),
        numpath(["63", "56", "41", "34"], hi=None, size=56),
    ]),
    EX("3", "97", st("Which is greater, 47 or 43? Say why.", "أيهما أكبر 47 أم 43؟ اذكر السبب.", "Lequel est plus grand, 47 ou 43 ? Dis pourquoi."), [
        tens(4, 7, eq=True),
        tens(4, 3, eq=True),
        T("The tens are equal (4 tens), so compare the ones: 7 is more than 3. So 47 is greater.",
          "العشرات متساوية (4 عشرات) فنقارن الآحاد: 7 أكبر من 3. إذن 47 أكبر.",
          "Les dizaines sont égales (4), on compare les unités : 7 > 3. Donc 47 est plus grand."),
    ]),
    EX("4", "97", st("Give the number before and the number after: 29, 39, 59.", "اذكر العدد قبل والعدد بعد: 29، 39، 59.", "Donne le nombre avant et après : 29, 39, 59."), [
        F("28, 29, 30      38, 39, 40      58, 59, 60"),
        T("After a number ending in 9 comes the next whole ten.",
          "بعد العدد الذي ينتهي بـ9 تأتي العشرة الكاملة التالية.",
          "Après un nombre qui finit par 9 vient la dizaine entière suivante."),
    ]),
    EX("5", "97", st("Complete: 44, 45, __, 47, __, 49, __.", "أكمل: 44، 45، __، 47، __، 49، __.", "Complète : 44, 45, __, 47, __, 49, __."), [
        numpath(["44", "45", "?", "47", "?", "49", "?"], hi=None, size=48),
        F("46, 48, 50"),
    ]),
    EX("6", "97", st("Complete backwards: 62, 61, __, 59, __, 57.", "أكمل إلى الوراء: 62، 61، __، 59، __، 57.", "Complète en reculant : 62, 61, __, 59, __, 57."), [
        numpath(["62", "61", "?", "59", "?", "57"], hi=None, size=50),
        F("60, 58"),
    ]),
    EX("7", "97", st("Error check: a child says 29 is greater than 41 because 9 is greater than 4. Is the child right?", "تحقّق من الخطأ: يقول طفل إن 29 أكبر من 41 لأن 9 أكبر من 4. هل هو محق؟", "Vérifie l'erreur : un enfant dit que 29 est plus grand que 41 parce que 9 > 4. A-t-il raison ?"), [
        tens(2, 9, eq=True),
        tens(4, 1, eq=True),
        T("No. The child compared only the ones. We must compare the tens first: 2 tens are less than 4 tens, so 29 is less than 41.",
          "لا. قارن الطفل الآحاد فقط. يجب أن نقارن العشرات أولًا: عشرتان أقل من 4 عشرات، إذن 29 أصغر من 41.",
          "Non. L'enfant n'a comparé que les unités. Il faut comparer les dizaines d'abord : 2 dizaines < 4 dizaines, donc 29 < 41."),
    ]),
    EX("8", "97", st("Final check: order 58, 36, 47 from smallest to largest and justify the first comparison.", "تقييم أخير: رتّب 58، 36، 47 من الأصغر إلى الأكبر وبرّر أول مقارنة.", "Évaluation : range 58, 36, 47 du plus petit au plus grand et justifie la première comparaison."), [
        numpath(["36", "47", "58"], hi=None, size=60),
        T("3 tens are fewer than 4 tens and 5 tens, so 36 is the smallest. Then 47, then 58.",
          "3 عشرات أقل من 4 و5 عشرات، فـ36 هو الأصغر. ثم 47 ثم 58.",
          "3 dizaines < 4 et 5 dizaines : 36 est le plus petit. Puis 47, puis 58."),
    ]),
]
