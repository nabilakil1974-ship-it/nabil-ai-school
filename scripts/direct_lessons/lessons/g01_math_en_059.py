"""Grade 1 Mathematics — Comparing numbers."""
from scripts.direct_lessons.common import T, F, EX, st, tens, numpath

LESSON_ID = "G01-MATH-EN-059"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Comparing numbers", "ar": "مقارنة الأعداد", "fr": "Comparer les nombres"}

THEORY = [
    ("More tens means greater", "عشرات أكثر تعني عددًا أكبر", "Plus de dizaines, plus grand", "152", [
        tens(5, 2, eq=True),
        tens(3, 9, eq=True),
        T("Hello, champion! Which is greater, 52 or 39? We compare the tens first. 52 has 5 tens and 39 has 3 tens. 5 tens are more than 3 tens, so 52 is greater than 39, even though 9 ones is more than 2 ones.",
          "مرحبًا يا بطل! أيهما أكبر 52 أم 39؟ نقارن العشرات أولًا. في 52 خمس عشرات وفي 39 ثلاث عشرات. 5 عشرات أكثر من 3 عشرات إذن 52 أكبر من 39، مع أن 9 آحاد أكثر من آحادين.",
          "Lequel est plus grand, 52 ou 39 ? On compare d'abord les dizaines. 52 a 5 dizaines, 39 en a 3. 5 > 3, donc 52 est plus grand que 39, même si 9 unités > 2 unités."),
        F("52 > 39      (5 tens > 3 tens)"),
    ]),
    ("Equal tens: compare the ones", "إذا تساوت العشرات نقارن الآحاد", "Dizaines égales : on compare les unités", "152", [
        tens(6, 3, eq=True),
        tens(6, 7, eq=True),
        T("63 and 67 both have 6 tens. The tens are equal, so we look at the ones: 3 ones are fewer than 7 ones. So 63 is smaller than 67.",
          "في 63 و67 ست عشرات في كليهما. العشرات متساوية فننظر إلى الآحاد: 3 آحاد أقل من 7 آحاد. إذن 63 أصغر من 67.",
          "63 et 67 ont 6 dizaines. Elles sont égales, on regarde les unités : 3 < 7. Donc 63 est plus petit que 67."),
        F("63 < 67      (6 tens = 6 tens, 3 ones < 7 ones)"),
    ]),
    ("Check on the number path", "نتحقق على مسار الأعداد", "Vérifier sur la droite", "153", [
        numpath(["63", "64", "65", "66", "67"], hi=None, size=52),
        T("On an increasing number path, the number farther to the right is greater. 67 is to the right of 63, so 67 is greater.",
          "على مسار أعداد متزايد يكون العدد الأبعد إلى اليمين هو الأكبر. 67 على يمين 63 إذن 67 أكبر.",
          "Sur une droite croissante, le nombre le plus à droite est le plus grand. 67 est à droite de 63 : il est plus grand."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("To compare two-digit numbers, compare the tens first. If the tens are equal, compare the ones. Never compare only the ones digits.",
          "لمقارنة عددين من رقمين نقارن العشرات أولًا. وإذا تساوت نقارن الآحاد. لا نقارن رقمي الآحاد فقط أبدًا.",
          "Pour comparer deux nombres à deux chiffres : d'abord les dizaines, puis les unités si elles sont égales. Jamais seulement les unités."),
        F("TENS FIRST → THEN ONES → CHECK ON THE PATH"),
    ]),
]

EXERCISES = [
    EX("1", "152", st("Which is greater: 48 or 84?", "أيهما أكبر: 48 أم 84؟", "Lequel est plus grand : 48 ou 84 ?"), [
        tens(4, 8, eq=True), tens(8, 4, eq=True),
        T("8 tens are more than 4 tens: 84 is greater.", "8 عشرات أكثر من 4 عشرات: 84 أكبر.", "8 dizaines > 4 dizaines : 84 est plus grand."),
    ]),
    EX("2", "152", st("Which is smaller: 71 or 69?", "أيهما أصغر: 71 أم 69؟", "Lequel est plus petit : 71 ou 69 ?"), [
        tens(7, 1, eq=True), tens(6, 9, eq=True),
        T("6 tens are fewer than 7 tens: 69 is smaller.", "6 عشرات أقل من 7 عشرات: 69 أصغر.", "6 dizaines < 7 dizaines : 69 est plus petit."),
    ]),
    EX("3", "152", st("Compare 55 and 58.", "قارن بين 55 و58.", "Compare 55 et 58."), [
        tens(5, 5, eq=True), tens(5, 8, eq=True),
        T("Same tens, 5 ones < 8 ones: 55 < 58.", "العشرات نفسها و5 آحاد < 8 آحاد: 55 < 58.", "Mêmes dizaines, 5 < 8 unités : 55 < 58."),
    ]),
    EX("4", "153", st("Compare 90 and 89.", "قارن بين 90 و89.", "Compare 90 et 89."), [
        tens(9, 0, eq=True), tens(8, 9, eq=True),
        T("9 tens are more than 8 tens. 90 > 89, even though 9 ones is the most.", "9 عشرات أكثر من 8 عشرات. 90 > 89 مع أن 9 آحاد أكثر عدد.", "9 dizaines > 8 dizaines. 90 > 89."),
    ]),
    EX("5", "153", st("Fill in: 36 __ 63.", "أكمل: 36 __ 63.", "Complète : 36 __ 63."), [
        F("36 < 63"),
        T("3 tens < 6 tens.", "3 عشرات < 6 عشرات.", "3 dizaines < 6 dizaines."),
    ]),
    EX("6", "153", st("Error check: a child says 29 > 41 because 9 > 1. What is wrong?", "تحقّق من الخطأ: يقول طفل إن 29 > 41 لأن 9 > 1. ما الخطأ؟", "Vérifie l'erreur : un enfant dit 29 > 41 car 9 > 1. Où est l'erreur ?"), [
        tens(2, 9, eq=True), tens(4, 1, eq=True),
        T("He compared only the ones. The tens decide first: 2 tens < 4 tens, so 29 < 41.", "قارن الآحاد فقط. العشرات تحسم أولًا: 2 عشرات < 4 عشرات إذن 29 < 41.", "Il n'a comparé que les unités. Les dizaines décident : 2 < 4, donc 29 < 41."),
    ]),
    EX("7", "153", st("Challenge: write a number greater than 76 and less than 79.", "تحدٍّ: اكتب عددًا أكبر من 76 وأصغر من 79.", "Défi : écris un nombre plus grand que 76 et plus petit que 79."), [
        numpath(["76", "77", "78", "79"], hi=None, size=56),
        T("77 or 78.", "77 أو 78.", "77 ou 78."),
    ]),
    EX("8", "153", st("Final check: compare 65 and 56 and say which place decided.", "تقييم أخير: قارن 65 و56 وقل أيّ خانة حسمت.", "Évaluation : compare 65 et 56 et dis quelle place a décidé."), [
        tens(6, 5, eq=True), tens(5, 6, eq=True),
        T("The tens decided: 6 tens > 5 tens, so 65 > 56.", "العشرات حسمت: 6 عشرات > 5 عشرات إذن 65 > 56.", "Les dizaines ont décidé : 6 > 5, donc 65 > 56."),
    ]),
]
