"""Direct lesson data: Grade 7 Mathematics — Powers (book pp. 14-21).

Written once, in three languages, from the verified golden teaching-and-solutions
document (Drive: NABIL_G07_POWERS_GOLDEN_TEACHING_AND_SOLUTIONS_FOR_FACTORY).
No per-string machine translation: every text step carries its own ar/en/fr twin.
"""
from __future__ import annotations

LESSON_ID = "G07-MATHEMATICS-69B7C840-001"
GRADE = 7
SUBJECT = "math"
TITLES = {"en": "Powers", "ar": "القوى (الأسس)", "fr": "Les puissances"}


from scripts.direct_lessons.common import T, F, D, EX, st, S, make_scenes


# ---------------------------------------------------------------- theory
THEORY = [
    ("Discover powers: the chessboard", "نكتشف القوى: رقعة الشطرنج", "Découvrir les puissances : l'échiquier", "14", [
        T("Imagine a chessboard. The inventor asks the king for 1 grain of wheat on the first square and double the grains on each next square.",
          "تخيّل رقعة شطرنج. يطلب المخترع من الملك حبة قمح واحدة على المربع الأول، ثم يُضاعف العدد في كل مربع يليه.",
          "Imagine un échiquier. L'inventeur demande au roi 1 grain de blé sur la première case, puis le double sur chaque case suivante."),
        F("1, 2, 4, 8, 16, 32, ..."),
        T("What pattern do you see? Each square is the previous one multiplied by 2.",
          "ماذا تلاحظ؟ كل مربع يساوي السابق مضروبًا في 2.",
          "Quel motif vois-tu ? Chaque case vaut la précédente multipliée par 2."),
        D("powerFactors", base=2, exp=4, value="16", title="2⁴"),
        F("2^{4} = 2 × 2 × 2 × 2 = 16"),
        T("Square number n holds 2^{n-1} grains. Doubling again and again grows extremely fast: this is exponential growth.",
          "المربع رقم n يحوي 2^{n-1} حبة. التضعيف المتكرر ينمو بسرعة كبيرة جدًا، وهذا هو النمو الأسّي.",
          "La case n contient 2^{n-1} grains. Doubler sans cesse fait croître très vite : c'est la croissance exponentielle."),
    ]),
    ("Base and exponent", "الأساس والأس", "Base et exposant", "15", [
        T("When the same number is multiplied by itself, we write a power.",
          "عندما نضرب العدد نفسه بنفسه عدة مرات نكتب قوة.",
          "Quand on multiplie un même nombre par lui-même, on écrit une puissance."),
        D("powerFactors", base=3, exp=4, value="81", title="3⁴"),
        F("3^{4} = 3 × 3 × 3 × 3 = 81"),
        T("3 is the base (the repeated factor). 4 is the exponent (how many factors).",
          "العدد 3 هو الأساس (العامل المكرّر)، والعدد 4 هو الأس (عدد العوامل).",
          "3 est la base (le facteur répété). 4 est l'exposant (le nombre de facteurs)."),
        F("a^{n} = a × a × ... × a   (n factors)"),
        T("Two special cases: a power of 1 is the number itself, and any non-zero number to the power 0 equals 1.",
          "حالتان خاصتان: القوة 1 تساوي العدد نفسه، وأي عدد غير معدوم أُسّه 0 يساوي 1.",
          "Deux cas particuliers : l'exposant 1 donne le nombre lui-même, et tout nombre non nul à la puissance 0 vaut 1."),
        F("a^{1} = a        a^{0} = 1  (a ≠ 0)"),
        T("Careful: 4^{3} means 4 × 4 × 4 = 64, not 4 × 3 = 12.",
          "انتبه: 4^{3} تعني 4 × 4 × 4 = 64 وليست 4 × 3 = 12.",
          "Attention : 4^{3} signifie 4 × 4 × 4 = 64, pas 4 × 3 = 12."),
    ]),
    ("Product of two powers with the same base", "جداء قوتين لهما الأساس نفسه", "Produit de deux puissances de même base", "15", [
        T("Write each power as a string of factors, then join them.",
          "نكتب كل قوة كسلسلة عوامل ثم نجمع السلسلتين.",
          "Écris chaque puissance en facteurs, puis réunis-les."),
        F("2^{3} × 2^{2} = (2 × 2 × 2) × (2 × 2) = 2^{5}"),
        T("The two strings of factors join, so the exponents add. The base stays the same.",
          "السلسلتان تتصلان، فتُجمع الأسس ويبقى الأساس نفسه.",
          "Les deux suites de facteurs se rejoignent : on additionne les exposants, la base ne change pas."),
        F("a^{m} × a^{n} = a^{m+n}"),
        T("Example:", "مثال:", "Exemple :"),
        F("5^{3} × 5^{4} = 5^{3+4} = 5^{7}"),
    ]),
    ("Power of a power", "قوة قوة", "Puissance d'une puissance", "16", [
        T("(2^{3})^{2} means the power 2^{3} taken twice.",
          "العبارة (2^{3})^{2} تعني القوة 2^{3} مضروبة بنفسها مرتين.",
          "(2^{3})^{2} signifie la puissance 2^{3} prise deux fois."),
        F("(2^{3})^{2} = 2^{3} × 2^{3} = 2^{6}"),
        T("There are n groups of m factors, so the exponents multiply.",
          "لدينا n مجموعة من m عاملًا، لذلك تُضرب الأسس.",
          "Il y a n groupes de m facteurs : on multiplie les exposants."),
        F("(a^{m})^{n} = a^{m × n}"),
        F("(3^{2})^{4} = 3^{8} = 6561"),
    ]),
    ("Power of a product and of a quotient", "قوة جداء وقوة حاصل قسمة", "Puissance d'un produit et d'un quotient", "16", [
        T("A power of a product is the product of the powers.",
          "قوة الجداء تساوي جداء القوى.",
          "La puissance d'un produit est le produit des puissances."),
        F("(2 × 3)^{3} = (2 × 3)(2 × 3)(2 × 3) = 2^{3} × 3^{3} = 216"),
        F("(a × b)^{n} = a^{n} × b^{n}"),
        F("(4 × 5)^{2} = 4^{2} × 5^{2} = 400"),
        T("The same holds for a quotient, with the divisor different from zero.",
          "والأمر نفسه لحاصل القسمة بشرط أن يكون القاسم غير معدوم.",
          "C'est pareil pour un quotient, à condition que le diviseur soit non nul."),
        F("(2/3)^{2} = (2 × 2)/(3 × 3) = 4/9"),
        F("(a/b)^{n} = a^{n}/b^{n}   (b ≠ 0)"),
        F("(3/5)^{3} = 27/125"),
    ]),
    ("Priority of operations and parentheses", "أولوية العمليات والأقواس", "Priorité des opérations et parenthèses", "17", [
        T("The exponent acts first, only on the number right next to it. Parentheses change the grouping.",
          "الأس يُنفَّذ أولًا ويؤثر في العدد الملاصق له فقط، أما الأقواس فتغيّر التجميع.",
          "L'exposant agit en premier, seulement sur le nombre qui le touche. Les parenthèses changent le groupement."),
        F("3 × 2^{3} = 3 × 8 = 24"),
        F("(3 × 2)^{3} = 6^{3} = 216"),
        F("3 + 2^{3} = 3 + 8 = 11"),
        F("(3 + 2)^{3} = 5^{3} = 125"),
        T("Warning: a power does not distribute over a sum. (a + b)^{n} is not a^{n} + b^{n}.",
          "تحذير: القوة لا تتوزّع على المجموع. (a + b)^{n} لا تساوي a^{n} + b^{n}.",
          "Attention : la puissance ne se distribue pas sur une somme. (a + b)^{n} n'est pas a^{n} + b^{n}."),
    ]),
    ("Powers of ten and expanded form", "قوى العدد عشرة والكتابة التحليلية", "Puissances de dix et écriture développée", "18", [
        T("A power of ten is 1 followed by as many zeros as the exponent.",
          "قوة العشرة هي 1 يتبعه عدد من الأصفار يساوي الأس.",
          "Une puissance de dix est 1 suivi d'autant de zéros que l'exposant."),
        F("10^{1} = 10     10^{2} = 100     10^{3} = 1000"),
        F("25 000 = 25 × 10^{3}"),
        T("We can also write a number as a sum of units, tens, hundreds, tenths and hundredths.",
          "ويمكن كتابة العدد كمجموع آحاد وعشرات ومئات وأعشار وأجزاء من مئة.",
          "On peut aussi écrire un nombre comme somme d'unités, dizaines, centaines, dixièmes et centièmes."),
        F("354.16 = 3 × 10^{2} + 5 × 10 + 4 + 1/10 + 6/100"),
        F("7205 = 7 × 10^{3} + 2 × 10^{2} + 5"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        F("a^{n} = a × a × ... × a   (n factors)"),
        F("a^{1} = a        a^{0} = 1  (a ≠ 0)"),
        F("a^{m} × a^{n} = a^{m+n}"),
        F("(a^{m})^{n} = a^{m × n}"),
        F("(a × b)^{n} = a^{n} × b^{n}"),
        F("(a/b)^{n} = a^{n}/b^{n}   (b ≠ 0)"),
        T("Never confuse 3 × 2^{3} with (3 × 2)^{3}.",
          "لا تخلط بين 3 × 2^{3} و (3 × 2)^{3}.",
          "Ne confonds jamais 3 × 2^{3} et (3 × 2)^{3}."),
    ]),
]


# ------------------------------------------------------------- exercises
EXERCISES = [
    EX("1", "18", st("Compute each power.", "احسب كل قوة.", "Calcule chaque puissance."), [
        F("2^{3} = 8      3^{2} = 9      2^{4} = 16      4^{2} = 16"),
        F("4^{3} = 64      5^{3} = 125      2^{5} = 32      6^{2} = 36"),
        F("6^{3} = 216      (2.1)^{3} = 9.261      4^{4} = 256"),
        F("10^{3} = 1000      10^{4} = 10000      2^{6} = 64"),
    ]),
    EX("2", "18", st("Special cases: compute.", "حالات خاصة: احسب.", "Cas particuliers : calcule."), [
        S("A power of 1 is the number itself; a power of 0 is 1; 0 or 1 to any power stays 0 or 1.",
          "القوة 1 تعطي العدد نفسه، والقوة 0 تعطي 1، وصفر أو واحد مرفوعان لأي أس يبقيان كما هما.",
          "L'exposant 1 donne le nombre ; l'exposant 0 donne 1 ; 0 ou 1 à toute puissance restent 0 ou 1."),
        F("29^{1} = 29      52^{0} = 1      0^{14} = 0      1^{1998} = 1      1998^{0} = 1"),
    ]),
    EX("3", "18", st("Calculate.", "احسب.", "Calcule."), [
        F("6^{2} = 36      (2.7)^{2} = 7.29      (6.5)^{2} = 42.25      21^{2} = 441"),
        F("27^{2} = 729      121^{2} = 14641      (1.55)^{2} = 2.4025"),
        F("7^{3} = 343      (2.7)^{3} = 19.683      4^{4} = 256      5^{4} = 625"),
        F("2^{8} = 256      3^{5} = 243      7^{4} = 2401"),
        F("31^{3} = 31 × 31 × 31 = 29791      17^{3} = 17 × 17 × 17 = 4913"),
        F("9^{6} = 531441      8^{5} = 32768      (0.5)^{4} = 0.0625      (1.2)^{5} = 2.48832"),
    ]),
    EX("4", "18", st("Order of operations: calculate.", "أولوية العمليات: احسب.", "Priorité des opérations : calcule."), [
        S("Compute the power first, then the other operation.",
          "نحسب القوة أولًا ثم العملية الأخرى.",
          "On calcule d'abord la puissance, puis l'autre opération."),
        F("5 × 4^{2} = 5 × 16 = 80      (5 × 4)^{2} = 20^{2} = 400"),
        F("(3 × 4)^{2} = 12^{2} = 144      (8 + 5)^{2} = 13^{2} = 169"),
        F("8^{2} + 5^{2} = 64 + 25 = 89      8 + 5^{2} = 8 + 25 = 33"),
        F("(8 − 2)^{2} = 6^{2} = 36      8^{2} − 2^{2} = 64 − 4 = 60      8 − 2^{2} = 8 − 4 = 4"),
        F("2 × (3 × 4)^{2} = 2 × 12^{2} = 288      7 × 5^{2} = 7 × 25 = 175      (6 − 6)^{2} = 0^{2} = 0"),
    ]),
    EX("5", "18", st("Write as one power.", "اكتب على شكل قوة واحدة.", "Écris sous forme d'une seule puissance."), [
        S("Same base: keep the base and add the exponents.",
          "الأساس نفسه: نُبقي الأساس ونجمع الأسس.",
          "Même base : on garde la base et on additionne les exposants."),
        F("2^{3} × 2^{5} = 2^{3+5} = 2^{8}      2^{6} × 2^{3} = 2^{9}"),
        F("3^{2} × 3^{4} = 3^{6}      5 × 5^{7} = 5^{1} × 5^{7} = 5^{8}"),
    ]),
    EX("6", "18", st("Write as an integer.", "اكتب على شكل عدد صحيح.", "Écris sous forme d'un entier."), [
        F("10^{3} = 1000      10^{4} = 10000"),
        F("2 × 10^{2} = 200      3 × 10^{2} = 300      3 × 10 = 30"),
    ]),
    EX("7", "18", st("Write as a power of 10.", "اكتب على شكل قوة للعدد 10.", "Écris comme puissance de 10."), [
        F("10000 = 10^{4}      100000 = 10^{5}      100 = 10^{2}"),
        F("10 = 10^{1}      1 = 10^{0}      1000000 = 10^{6}"),
    ]),
    EX("8", "18", st("Simplify.", "بسّط.", "Simplifie."), [
        F("10^{2} × 10^{3} = 10^{5}      10^{4} × 10 = 10^{5}      10^{5} × 10^{2} = 10^{7}"),
        S("Same exponent: multiply the bases first.",
          "الأس نفسه: نضرب الأساسين أولًا.",
          "Même exposant : on multiplie d'abord les bases."),
        F("5^{3} × 2^{3} = (5 × 2)^{3} = 10^{3}"),
    ]),
    EX("9", "18", st("Write as an integer times a power of 10.", "اكتب على شكل عدد صحيح مضروب بقوة للعدد 10.", "Écris comme entier fois une puissance de 10."), [
        F("2000 = 2 × 10^{3}      25000 = 25 × 10^{3}      50000 = 5 × 10^{4}"),
        F("300000 = 3 × 10^{5}      4000000 = 4 × 10^{6}"),
    ]),
    EX("10", "18", st("Find the missing exponent.", "أوجد الأس المجهول.", "Trouve l'exposant manquant."), [
        F("4 × 10^{3} = 4000      36 × 10^{3} = 36000"),
        F("12 × 10^{0} = 12      50 × 10^{2} = 5000"),
    ]),
    EX("11", "18", st("Find the smallest natural exponent n.", "أوجد أصغر أس طبيعي n.", "Trouve le plus petit exposant naturel n."), [
        S("Multiply until the result is a whole number.",
          "نضرب حتى نحصل على عدد صحيح.",
          "On multiplie jusqu'à obtenir un entier."),
        F("3.75 × 10^{2} = 375      n = 2"),
        F("0.0025 × 10^{4} = 25      n = 4"),
        F("25.67 × 10^{2} = 2567      n = 2"),
        F("75.408 × 10^{3} = 75408      n = 3"),
    ]),
    EX("12", "18", st("Compute.", "احسب.", "Calcule."), [
        F("2 × 10^{2} + 5 × 10 + 3 = 200 + 50 + 3 = 253"),
        F("8 × 10^{3} + 3 × 10^{2} + 6 = 8000 + 300 + 6 = 8306"),
        F("9 × 10^{4} + 10^{3} + 7 × 10^{2} + 8 × 10 + 3 = 91783"),
        F("5 × 10^{2} + 4 × 10 + 7 + 1/10 + 3/100 + 8/1000 = 547.138"),
    ]),
    EX("13", "18", st("Write in expanded form.", "اكتب بالكتابة التحليلية.", "Écris en écriture développée."), [
        F("12.2 = 10 + 2 + 2/10"),
        F("25.234 = 20 + 5 + 2/10 + 3/100 + 4/1000"),
        F("108.251 = 100 + 8 + 2/10 + 5/100 + 1/1000"),
        F("0.37 = 3/10 + 7/100      0.052 = 5/100 + 2/1000"),
        F("2000.0002 = 2 × 10^{3} + 2/10^{4}"),
    ]),
    # ---- page 19: true/false and calculations
    EX("A", "19", st("True or false? Correct the false ones.", "صح أم خطأ؟ صحّح العبارات الخاطئة.", "Vrai ou faux ? Corrige les fausses."), [
        F("(0.000731)^{0} = 1      TRUE"),
        F("a^{1} = a      TRUE"),
        F("a^{3} × a^{5} = a^{15}      FALSE: a^{3} × a^{5} = a^{3+5} = a^{8}"),
        F("a^{3} × b^{3} = (ab)^{3}      TRUE"),
        F("10^{7} ÷ 10^{2} = 10^{7−2} = 10^{5}      TRUE"),
        F("10^{8} ÷ 10^{5} = 10^{3}      TRUE"),
        F("a^{7} ÷ a^{4} = a^{3}      TRUE   (a ≠ 0)"),
        F("7 × 5^{2} = 175      (7 × 5)^{2} = 1225      FALSE"),
        F("5 + 3^{2} = 14      (5 + 3)^{2} = 64      FALSE"),
        F("5^{2} + 4^{2} = 41      (5 + 4)^{2} = 81      FALSE"),
        F("1700 = 1.7 × 10^{3}      TRUE      1700 = 17 × 10^{2}      TRUE"),
        F("3 × 10^{2} + 4 × 10 + 2 × 10^{0} = 342      TRUE"),
        F("5 × 10^{2} + 3 + 1/10 + 3/10^{2} = 503.13      TRUE"),
    ]),
    EX("B", "19", st("Calculate and complete.", "احسب وأكمل.", "Calcule et complète."), [
        F("5^{4} = 625      4^{3} = 64      (3.1)^{0} = 1"),
        F("(0.1)^{4} = 0.0001      (0.015)^{3} = 0.000003375      (0.00076)^{0} = 1"),
        F("4 × 5^{2} = 100      4^{2} × 5^{2} = 400      (2 + 3)^{3} = 125"),
        F("2^{3} × 3^{3} = (2 × 3)^{3} = 216      2^{3} + 3^{3} = 8 + 27 = 35"),
        F("1000 = 10^{3}      10 × 10^{3} = 10^{4}      100 × 100 = 10^{4}      10^{2} × 10000 = 10^{6}"),
        F("4 × 2^{6} = 2^{2} × 2^{6} = 2^{8}"),
        F("4 × 10^{3} = 4000      3.6 × 10^{3} = 3600"),
        F("354.16 = 300 + 50 + 4 + 0.1 + 0.06      7205 = 7000 + 200 + 5"),
        F("306.25 = 300 + 6 + 0.2 + 0.05      1004 = 1000 + 4"),
    ]),
    # ---- page 20 supplementary
    EX("S1", "20", st("Compute.", "احسب.", "Calcule."), [
        F("67 × 10^{2} = 6700      0.2 × 10^{3} = 200"),
        F("2.25 × 10^{2} = 225      0.0425 × 10^{6} = 42500"),
    ]),
    EX("S2", "20", st("Write as one power.", "اكتب على شكل قوة واحدة.", "Écris sous forme d'une seule puissance."), [
        F("3^{4} × 5^{4} = (3 × 5)^{4} = 15^{4}      8^{3} × 5^{3} = 40^{3}"),
        F("5^{2} × 3^{2} × 4^{2} = (5 × 3 × 4)^{2} = 60^{2}"),
        F("3^{5}/4^{5} = (3/4)^{5}      8^{3}/2^{3} = (8/2)^{3} = 4^{3}      9^{4}/3^{4} = 3^{4}"),
        F("(2^{3})^{4} = 2^{12}      (5^{2})^{3} = 5^{6}      (10^{4})^{2} = 10^{8}"),
    ]),
    EX("S3", "20", st("Justify each equality.", "برّر كل مساواة.", "Justifie chaque égalité."), [
        F("2^{4} = 4^{2}  because (2^{2})^{2} = 2^{4}"),
        F("9^{3} = 3^{6}  since (3^{2})^{3} = 3^{6}"),
        F("16^{3} = 4^{6}  because (4^{2})^{3} = 4^{6}"),
        F("25^{4} = 5^{8}  because (5^{2})^{4} = 5^{8}"),
    ]),
    EX("S4", "20", st("Show that 3^{7} is divisible by 3, 3², 3⁵ and 3⁶.", "بيّن أن 3^{7} تقبل القسمة على 3 و 3² و 3⁵ و 3⁶.", "Montre que 3^{7} est divisible par 3, 3², 3⁵ et 3⁶."), [
        F("3^{7} = 3 × 3^{6} = 3^{2} × 3^{5} = 3^{5} × 3^{2} = 3^{6} × 3"),
    ]),
    EX("S5", "20", st("Show that 5^{6} is divisible by 5, 25 and 125.", "بيّن أن 5^{6} تقبل القسمة على 5 و 25 و 125.", "Montre que 5^{6} est divisible par 5, 25 et 125."), [
        F("5^{6} = 5 × 5^{5} = 5^{2} × 5^{4} = 5^{3} × 5^{3}"),
        F("25 = 5^{2}      125 = 5^{3}"),
    ]),
    EX("S6", "20", st("Write with base 2.", "اكتب بدلالة الأساس 2.", "Écris avec la base 2."), [
        F("4 = 2^{2}      8 = 2^{3}      16 = 2^{4}"),
        F("4^{3} = (2^{2})^{3} = 2^{6}      8^{2} = (2^{3})^{2} = 2^{6}      16^{4} = (2^{4})^{4} = 2^{16}"),
    ]),
    EX("S7", "20", st("Write with base 3.", "اكتب بدلالة الأساس 3.", "Écris avec la base 3."), [
        F("9 = 3^{2}      27 = 3^{3}      81 = 3^{4}"),
        F("9^{3} = 3^{6}      27^{2} = 3^{6}      81^{5} = (3^{4})^{5} = 3^{20}"),
    ]),
    EX("S8", "20", st("Write with base 5.", "اكتب بدلالة الأساس 5.", "Écris avec la base 5."), [
        F("25 = 5^{2}      125 = 5^{3}      625 = 5^{4}"),
        F("25^{2} = 5^{4}      125^{3} = 5^{9}      625^{2} = 5^{8}"),
    ]),
    EX("S9", "20", st("Order from smallest to largest.", "رتّب من الأصغر إلى الأكبر.", "Range du plus petit au plus grand."), [
        F("2^{5} = 32      8^{2} = 64      4^{4} = 256"),
        F("32 < 64 < 256"),
        F("5^{2} × 5^{4} = 5^{6}      5^{7}      25^{4} = (5^{2})^{4} = 5^{8}"),
        F("5^{6} < 5^{7} < 5^{8}"),
    ]),
    EX("S10", "20", st("A sum of 100 000 L.L. grows by 10% each year. Find its value after 1, 2 and 3 years.", "مبلغ 100 000 ل.ل. يزيد 10% كل سنة. أوجد قيمته بعد 1 و 2 و 3 سنوات.", "Une somme de 100 000 L.L. augmente de 10 % par an. Trouve sa valeur après 1, 2 et 3 ans."), [
        S("Each year the amount is multiplied by 1.1.",
          "في كل سنة يُضرب المبلغ في 1.1.",
          "Chaque année, on multiplie par 1,1."),
        F("100000 × 1.1 = 110000"),
        F("100000 × 1.1^{2} = 121000"),
        F("100000 × 1.1^{3} = 133100"),
    ]),
    EX("S11", "20", st("A water lily doubles its area every day and covers the lake on day 30. When does it cover half? And two lilies?", "زنبقة ماء تضاعف مساحتها كل يوم وتغطي البحيرة في اليوم 30. متى تغطي النصف؟ وماذا عن زنبقتين؟", "Un nénuphar double sa surface chaque jour et couvre le lac au jour 30. Quand couvre-t-il la moitié ? Et deux nénuphars ?"), [
        S("Doubling means that the day before the end it covered half.",
          "التضعيف يعني أنه في اليوم السابق للنهاية كانت التغطية نصفًا.",
          "Doubler signifie que la veille de la fin, il couvrait la moitié."),
        F("Half the lake: day 29"),
        S("Two lilies start with double the area, so they finish one day earlier.",
          "زنبقتان تبدآن بضعف المساحة، فتنتهيان قبل يوم.",
          "Deux nénuphars partent avec une surface double : ils finissent un jour plus tôt."),
        F("Two lilies: full lake on day 29"),
    ]),
    EX("S12", "20", st("Complete by a power of 10.", "أكمل بقوة للعدد 10.", "Complète par une puissance de 10."), [
        S("Lengths use the factor once, areas square it, volumes cube it.",
          "الأطوال تستعمل المعامل مرة، والمساحات تربّعه، والأحجام تكعّبه.",
          "Longueurs : le facteur une fois ; aires : au carré ; volumes : au cube."),
        F("1 m = 10^{3} mm      1 dam = 10^{3} cm      1 km = 10^{2} dam      1 hm = 10^{3} dm"),
        F("1 kg = 10^{3} g      1 kg = 10^{5} cg      1 l = 10^{3} ml"),
        F("1 m^{2} = 10^{4} cm^{2}      1 km^{2} = 10^{6} m^{2}      1 dam^{2} = 10^{4} dm^{2}"),
        F("1 m^{3} = 10^{6} cm^{3}      1 dam^{3} = 10^{3} m^{3}      1 km^{3} = 10^{3} hm^{3}"),
    ]),
    EX("S13", "20", st("2 500 000 L.L. in 250 L.L. bills, stacked to 50 cm. Find the number of bills and the thickness of one bill.", "2 500 000 ل.ل. بأوراق من 250 ل.ل. مكدّسة بارتفاع 50 سم. أوجد عدد الأوراق وسماكة الورقة.", "2 500 000 L.L. en billets de 250 L.L., empilés sur 50 cm. Trouve le nombre de billets et l'épaisseur d'un billet."), [
        F("2500000 ÷ 250 = 10000 bills"),
        F("50 ÷ 10000 = 0.005 cm = 0.05 mm"),
    ]),
    EX("S14", "20", st("Light travels at 300 000 km/s. Find the distance in one hour, one day, one year, and the Sun–Earth light time (149 500 000 km).", "سرعة الضوء 300 000 كم/ث. أوجد المسافة في ساعة ويوم وسنة، وزمن وصول ضوء الشمس إلى الأرض (149 500 000 كم).", "La lumière va à 300 000 km/s. Trouve la distance en une heure, un jour, un an, et le temps Soleil–Terre (149 500 000 km)."), [
        F("1 hour: 300000 × 3600 = 1.08 × 10^{9} km"),
        F("1 day: 1.08 × 10^{9} × 24 = 2.592 × 10^{10} km"),
        F("1 year (365 days): 9.4608 × 10^{12} km"),
        F("149500000 ÷ 300000 ≈ 498.33 s ≈ 8 min 18 s"),
    ]),
]

GOLDEN = {
    "kind": "mathematics", "subject": "mathematics", "language": "en", "title": "Powers",
    "sections": [{"label": "Results:", "items": [
        "a^{m} × a^{n} = a^{m+n}", "(a^{m})^{n} = a^{m × n}", "(ab)^{n} = a^{n} b^{n}", "a^{0} = 1 (a ≠ 0)"]}],
    "key_results": ["a^{m} × a^{n} = a^{m+n}", "(a^{m})^{n} = a^{m × n}"],
    "verification": ["checked"], "panels": [{"title": "Rules of powers", "icon": "✅", "steps": [
        "a^{m} × a^{n} = a^{m+n}", "(a^{m})^{n} = a^{m × n}", "(ab)^{n} = a^{n} b^{n}"]}],
    "rule_summary": "a^{m} × a^{n} = a^{m+n}", "concept_ids": ["P"], "avatar_src": "",
}




def scenes():
    return make_scenes(THEORY, EXERCISES)
