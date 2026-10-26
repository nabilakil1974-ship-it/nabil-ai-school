"""Grade 2 Mathematics — Order of numbers up to 99."""
from scripts.direct_lessons.common import T, F, EX, st, tens, numpath

LESSON_ID = "G02-MATH-EN-013"
GRADE = 2
SUBJECT = "math"
TITLES = {"en": "Order of numbers up to 99", "ar": "ترتيب الأعداد حتى 99", "fr": "Ranger les nombres jusqu'à 99"}

THEORY = [
    ("Which chest has more?", "أيّ صندوق فيه أكثر؟", "Quel coffre en a le plus ?", "34", [
        tens(7, 8, tag="A", eq=True),
        tens(7, 4, tag="B", eq=True),
        T("Hello, champion! Two treasure chests: 78 coins and 74 coins. Which has more? Do not guess; prove it. Look at the tens first: both have 7 tens. When the tens are equal we compare the ones: 8 > 4. So 78 > 74.",
          "مرحبًا يا بطل! صندوقا كنز: في الأول 78 قطعة وفي الثاني 74. أيهما فيه أكثر؟ لا نخمّن بل نثبت. ننظر إلى العشرات أولًا: في كليهما 7 عشرات. وعندما تتساوى العشرات نقارن الآحاد: 8 > 4. إذن 78 > 74.",
          "Deux coffres : 78 pièces et 74 pièces. Lequel en a plus ? On ne devine pas, on prouve. Les dizaines d'abord : 7 dans les deux. Quand elles sont égales, on compare les unités : 8 > 4. Donc 78 > 74."),
        F("78 > 74"),
    ]),
    ("Tens decide first", "العشرات تحسم أولًا", "Les dizaines décident d'abord", "34", [
        tens(7, 3, tag="A", eq=True),
        tens(6, 9, tag="B", eq=True),
        T("73 and 69. Do we even need the ones? 7 tens are more than 6 tens, so 73 > 69 immediately. The rule: TENS FIRST; ONES ONLY IF THE TENS TIE. So 71 < 86 because 7 tens < 8 tens, and 83 > 38 because 8 tens > 3 tens.",
          "73 و69. هل نحتاج إلى الآحاد أصلًا؟ 7 عشرات أكثر من 6 عشرات فـ73 > 69 مباشرة. القاعدة: العشرات أولًا ولا نقارن الآحاد إلا إذا تساوت العشرات. إذن 71 < 86 لأن 7 عشرات < 8 عشرات، و83 > 38 لأن 8 عشرات > 3 عشرات.",
          "73 et 69. A-t-on besoin des unités ? 7 dizaines > 6 dizaines : 73 > 69 tout de suite. Règle : DIZAINES D'ABORD ; UNITÉS SEULEMENT SI LES DIZAINES SONT ÉGALES. Donc 71 < 86 et 83 > 38."),
        F("73 > 69        71 < 86        83 > 38"),
    ]),
    ("Calculate an expression first", "نحسب العبارة أولًا", "Calculer l'expression d'abord", "35", [
        F("93 ? 80 + 13"),
        T("When one side is an addition, we calculate it completely first: 80 + 13 = 93. So 93 = 80 + 13. And 80 + 4 < 80 + 9 because 84 < 89. We compare values, not the look of the expressions.",
          "عندما يكون أحد الطرفين عملية جمع نحسبه كاملًا أولًا: 80 + 13 = 93. إذن 93 = 80 + 13. و80 + 4 < 80 + 9 لأن 84 < 89. نقارن القيم لا شكل العبارات.",
          "Quand un côté est une addition, on la calcule d'abord : 80 + 13 = 93, donc 93 = 80 + 13. Et 80 + 4 < 80 + 9 car 84 < 89. On compare les valeurs."),
    ]),
    ("Between, before and after", "بين وقبل وبعد", "Entre, avant et après", "35", [
        numpath(["90", "91", "92"], hi=1, size=64),
        T("The number between 90 and 92 is 91, the middle of the counting sequence. Right before is one less, right after is one more. Right before 70 is 69, not 71. Right before 98 is 97 and right after 98 is 99.",
          "العدد بين 90 و92 هو 91، الواقع في وسط متتالية العدّ. قبل مباشرة أقل بواحد وبعد مباشرة أكبر بواحد. العدد قبل 70 مباشرة هو 69 لا 71. وقبل 98 مباشرة 97 وبعد 98 مباشرة 99.",
          "Entre 90 et 92, c'est 91, au milieu de la suite. Juste avant : un de moins ; juste après : un de plus. Juste avant 70, c'est 69, pas 71. Avant 98 : 97 ; après 98 : 99."),
    ]),
    ("Order from greatest to smallest", "الترتيب من الأكبر إلى الأصغر", "Ranger du plus grand au plus petit", "35", [
        numpath(["96", "83", "73", "68"], hi=None, size=56),
        T("Arrange 73, 96, 83, 68. The tens: 96 has 9, 83 has 8, 73 has 7, 68 has 6. From the greatest: 96 > 83 > 73 > 68.",
          "رتّب 73 و96 و83 و68. العشرات: في 96 تسع وفي 83 ثمان وفي 73 سبع وفي 68 ست. من الأكبر: 96 > 83 > 73 > 68.",
          "Range 73, 96, 83, 68. Dizaines : 9, 8, 7, 6. Du plus grand : 96 > 83 > 73 > 68."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Read the value, compare the tens, compare the ones only if the tens tie, choose the sign, and check. Calculate expressions first.",
          "نقرأ القيمة ونقارن العشرات ثم الآحاد إذا تساوت العشرات ونختار الإشارة ونتحقق. ونحسب العبارات أولًا.",
          "On lit la valeur, on compare les dizaines puis les unités si elles sont égales, on choisit le signe et on vérifie. On calcule d'abord les expressions."),
        F("VALUE → TENS → ONES → RELATION → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "34", st("Write each number, then use > or <: (7 tens 1 one, 8 tens 6 ones); (8 tens 6 ones, 7 tens 4 ones).", "اكتب كل عدد ثم استعمل > أو <: (7 عشرات وواحد، 8 عشرات و6 آحاد)؛ (8 عشرات و6 آحاد، 7 عشرات و4 آحاد).", "Écris chaque nombre puis > ou < : (7 dizaines 1 unité, 8 dizaines 6 unités) ; (8 dizaines 6, 7 dizaines 4)."), [
        tens(7, 1, tag="A", eq=True), tens(8, 6, tag="B", eq=True),
        F("71 < 86        86 > 74"),
    ]),
    EX("2", "34", st("Circle the smallest: 79 & 81, 88 & 43, 75 & 65, 92 & 72, 56 & 73, 68 & 95.", "ضع دائرة حول الأصغر: 79 و81، 88 و43، 75 و65، 92 و72، 56 و73، 68 و95.", "Entoure le plus petit : 79 & 81, 88 & 43, 75 & 65, 92 & 72, 56 & 73, 68 & 95."), [
        F("79   43   65   72   56   68"),
    ]),
    EX("3", "34", st("Complete with > or <: 85 _ 89, 70 _ 73, 63 _ 83, 56 _ 96, 93 _ 80, 65 _ 74, 87 _ 78, 63 _ 70, 70 _ 68, 83 _ 38, 56 _ 96, 71 _ 62.", "أكمل بـ > أو <: 85 _ 89، 70 _ 73، 63 _ 83، 56 _ 96، 93 _ 80، 65 _ 74، 87 _ 78، 63 _ 70، 70 _ 68، 83 _ 38، 56 _ 96، 71 _ 62.", "Complète avec > ou < : 85 _ 89, 70 _ 73, 63 _ 83, 56 _ 96, 93 _ 80, 65 _ 74, 87 _ 78, 63 _ 70, 70 _ 68, 83 _ 38, 56 _ 96, 71 _ 62."), [
        F("85 < 89    70 < 73    63 < 83    56 < 96"),
        F("93 > 80    65 < 74    87 > 78    63 < 70"),
        F("70 > 68    83 > 38    56 < 96    71 > 62"),
    ]),
    EX("4", "35", st("Complete with >, < or =: 65 _ 80 + 5; 79 _ 60 + 12; 86 _ 60 + 8; 93 _ 80 + 13; 80 + 4 _ 80 + 9; 80 + 2 _ 70 + 8; 70 + 7 _ 60 + 17; 50 + 9 _ 80 + 3.", "أكمل بـ > أو < أو =: 65 _ 80 + 5؛ 79 _ 60 + 12؛ 86 _ 60 + 8؛ 93 _ 80 + 13؛ 80 + 4 _ 80 + 9؛ 80 + 2 _ 70 + 8؛ 70 + 7 _ 60 + 17؛ 50 + 9 _ 80 + 3.", "Complète avec >, < ou = : 65 _ 80 + 5 ; 79 _ 60 + 12 ; 86 _ 60 + 8 ; 93 _ 80 + 13 ; 80 + 4 _ 80 + 9 ; 80 + 2 _ 70 + 8 ; 70 + 7 _ 60 + 17 ; 50 + 9 _ 80 + 3."), [
        F("65 < 80 + 5    79 > 60 + 12    86 > 60 + 8    93 = 80 + 13"),
        F("80 + 4 < 80 + 9    80 + 2 > 70 + 8    70 + 7 = 60 + 17    50 + 9 < 80 + 3"),
    ]),
    EX("5", "35", st("Write the number between: 90 _ 92, 69 _ 71, 86 _ 88, 78 _ 80, 70 _ 72, 89 _ 91.", "اكتب العدد بين: 90 _ 92، 69 _ 71، 86 _ 88، 78 _ 80، 70 _ 72، 89 _ 91.", "Écris le nombre entre : 90 _ 92, 69 _ 71, 86 _ 88, 78 _ 80, 70 _ 72, 89 _ 91."), [
        F("91   70   87   79   71   90"),
    ]),
    EX("6", "35", st("Complete: 89, __, 91; 82, __, 84; 70, __, 72; 68, 69, __; 88, 89, __; __, 70, 71; 65, 66, __; 97, 98, __.", "أكمل: 89، __، 91؛ 82، __، 84؛ 70، __، 72؛ 68، 69، __؛ 88، 89، __؛ __، 70، 71؛ 65، 66، __؛ 97، 98، __.", "Complète : 89, __, 91 ; 82, __, 84 ; 70, __, 72 ; 68, 69, __ ; 88, 89, __ ; __, 70, 71 ; 65, 66, __ ; 97, 98, __."), [
        F("90   83   71   70   90   69   67   99"),
        T("Before is one less; after is one more.", "قبل أقل بواحد وبعد أكبر بواحد.", "Avant : un de moins ; après : un de plus."),
    ]),
    EX("7", "35", st("Write an appropriate number: __ < 68, __ > 70, __ < 92, __ < 82, __ < 86, __ < 80.", "اكتب عددًا مناسبًا: __ < 68، __ > 70، __ < 92، __ < 82، __ < 86، __ < 80.", "Écris un nombre convenable : __ < 68, __ > 70, __ < 92, __ < 82, __ < 86, __ < 80."), [
        F("67 < 68    71 > 70    91 < 92    81 < 82    85 < 86    79 < 80"),
        T("These are valid examples, not the only answers.", "هذه أمثلة صحيحة وليست الأجوبة الوحيدة.", "Ce sont des exemples justes, pas les seules réponses."),
    ]),
    EX("8", "35", st("Nour has 86 pearls and Grace has 65. Who has fewer? Bassem has 73 marbles and Makram 82. Who has more?", "عند نور 86 لؤلؤة وعند غريس 65. من عنده أقل؟ وعند باسم 73 كرة وعند مكرم 82. من عنده أكثر؟", "Nour a 86 perles, Grace 65. Qui en a moins ? Bassem a 73 billes, Makram 82. Qui en a plus ?"), [
        F("65 < 86 → Grace has fewer.      82 > 73 → Makram has more."),
    ]),
    EX("9", "35", st("Arrange from greatest to smallest: 73, 96, 83, 68.", "رتّب من الأكبر إلى الأصغر: 73، 96، 83، 68.", "Range du plus grand au plus petit : 73, 96, 83, 68."), [
        numpath(["96", "83", "73", "68"], hi=None, size=56),
        F("96 > 83 > 73 > 68"),
    ]),
    EX("10", "", st("Mystery number: greater than 80, less than 90, ones digit 6.", "عدد غامض: أكبر من 80 وأصغر من 90 ورقم آحاده 6.", "Nombre mystère : plus grand que 80, plus petit que 90, chiffre des unités 6."), [
        F("86 > 80      86 < 90      ones digit 6"),
    ]),
    EX("11", "", st("Error detective: 83 < 38 because 3 < 8; and 70 + 7 > 60 + 17; and right before 70 is 71.", "المحقق: 83 < 38 لأن 3 < 8؛ و70 + 7 > 60 + 17؛ والعدد قبل 70 هو 71.", "Détective : 83 < 38 car 3 < 8 ; 70 + 7 > 60 + 17 ; juste avant 70 c'est 71."), [
        T("83 > 38 because 8 tens > 3 tens. 70 + 7 = 77 and 60 + 17 = 77, so they are equal. Right before 70 is 69.",
          "83 > 38 لأن 8 عشرات > 3 عشرات. و70 + 7 = 77 و60 + 17 = 77 فهما متساويان. والعدد قبل 70 هو 69.",
          "83 > 38 car 8 dizaines > 3. 70 + 7 = 77 = 60 + 17 : égaux. Juste avant 70 : 69."),
    ]),
    EX("12", "", st("Final check: 71 _ 86; 86 _ 74; 93 _ 80 + 13; between 89 and 91; before 98; after 98; fewer pearls; greatest to smallest; why 83 > 38?", "تقييم أخير: 71 _ 86؛ 86 _ 74؛ 93 _ 80 + 13؛ بين 89 و91؛ قبل 98؛ بعد 98؛ أقل لؤلؤ؛ من الأكبر إلى الأصغر؛ لماذا 83 > 38؟", "Évaluation : 71 _ 86 ; 86 _ 74 ; 93 _ 80 + 13 ; entre 89 et 91 ; avant 98 ; après 98 ; moins de perles ; du plus grand au plus petit ; pourquoi 83 > 38 ?"), [
        F("71 < 86   86 > 74   93 = 80 + 13   90   97   99"),
        T("83 has 8 tens and 38 has only 3 tens.", "في 83 ثماني عشرات وفي 38 ثلاث عشرات فقط.", "83 a 8 dizaines et 38 seulement 3."),
    ]),
]
