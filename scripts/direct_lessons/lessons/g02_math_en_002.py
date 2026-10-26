"""Grade 2 Mathematics — Order of numbers up to 20."""
from scripts.direct_lessons.common import T, F, EX, st, tens, numpath

LESSON_ID = "G02-MATH-EN-002"
GRADE = 2
SUBJECT = "math"
TITLES = {"en": "Order of numbers up to 20", "ar": "ترتيب الأعداد حتى 20", "fr": "Ranger les nombres jusqu'à 20"}

THEORY = [
    ("Greater and less", "أكبر وأصغر", "Plus grand et plus petit", "14", [
        tens(0, 5, bundled=False, tag="A", eq=True),
        tens(0, 3, bundled=False, tag="B", eq=True),
        T("Hello, champion! Now we have numbers up to 20, and we ask: which is smaller? which is greater? what comes before, after, between? Look: 5 cubes and 3 cubes. 5 is greater than 3, and we write 5 > 3. Now 2 cubes and 4 cubes: 2 is less than 4, and we write 2 < 4.",
          "مرحبًا يا بطل! صار عندنا الأعداد حتى 20 ونسأل: أيّها أصغر؟ وأيّها أكبر؟ وما الذي يأتي قبل وبعد وبين؟ انظر: 5 مكعبات و3 مكعبات. 5 أكبر من 3 ونكتب 5 > 3. والآن مكعبان و4 مكعبات: 2 أصغر من 4 ونكتب 2 < 4.",
          "Bonjour champion ! On a les nombres jusqu'à 20 et on se demande : lequel est plus petit ? plus grand ? ce qui vient avant, après, entre ? Regarde : 5 cubes et 3 cubes. 5 est plus grand que 3 : 5 > 3. Puis 2 cubes et 4 cubes : 2 est plus petit que 4 : 2 < 4."),
        F("5 > 3        2 < 4"),
    ]),
    ("Decide first, then choose the sign", "نقرّر أولًا ثم نختار الإشارة", "D'abord décider, puis choisir le signe", "14", [
        F("6 < 11        19 > 16"),
        T("The sign must speak about the quantities. 6 and 11: 6 is smaller, so 6 < 11. 19 and 16: 19 is greater, so 19 > 16. We never choose the sign by chance. First we decide which number is smaller and which is greater, then we write the sign. If we hesitate, we put both numbers on the number path: the one that comes first is smaller.",
          "يجب أن تتحدث الإشارة عن الكميتين. 6 و11: 6 أصغر إذن 6 < 11. و19 و16: 19 أكبر إذن 19 > 16. لا نختار الإشارة صدفة. نقرّر أولًا أيّ العددين أصغر وأيّهما أكبر ثم نكتب الإشارة. وإذا ترددنا نضع العددين على مسار الأعداد: الذي يأتي أولًا هو الأصغر.",
          "Le signe doit parler des quantités. 6 et 11 : 6 est plus petit, donc 6 < 11. 19 et 16 : 19 est plus grand, donc 19 > 16. On ne choisit jamais le signe au hasard : on décide d'abord, puis on écrit. En cas de doute, on place les deux nombres sur la droite : celui qui vient en premier est le plus petit."),
    ]),
    ("Models prove it", "النماذج تثبت ذلك", "Les modèles le prouvent", "14", [
        tens(1, 1, tag="A", eq=True),
        tens(0, 8, bundled=False, tag="B", eq=True),
        T("Sometimes we read models, not only digits. 1 ten + 1 one is 11. 8 ones is 8. So 11 > 8. When both numbers have the same number of tens, we compare the ones: 10 and 14 both have one ten, but 14 has 4 more ones, so 10 < 14.",
          "أحيانًا نقرأ النماذج لا الأرقام فقط. عشرة + واحد هي 11. و8 آحاد هي 8. إذن 11 > 8. وعندما يكون لدى العددين عدد العشرات نفسه نقارن الآحاد: في 10 و14 عشرة واحدة لكل منهما لكن في 14 أربعة آحاد زائدة فـ 10 < 14.",
          "On lit parfois des modèles. 1 dizaine + 1 unité = 11. 8 unités = 8. Donc 11 > 8. Quand les dizaines sont égales, on compare les unités : 10 et 14 ont une dizaine, mais 14 a 4 unités de plus, donc 10 < 14."),
    ]),
    ("Before, after and between", "قبل وبعد وبين", "Avant, après et entre", "15", [
        numpath(["12", "13", "14"], hi=1, size=64),
        T("Right before means one less. Right after means one more. In 12, 13, 14: 12 is right before 13 and 14 is right after 13. And the number between 5 and 7 is 6, because the counting sequence is 5, 6, 7. Between is not any smaller number: between 15 and 17 is 16, not 10.",
          "العدد الذي قبله مباشرة هو أقل بواحد، والعدد الذي بعده مباشرة هو أكبر بواحد. في 12 و13 و14: 12 قبل 13 مباشرة و14 بعد 13 مباشرة. والعدد بين 5 و7 هو 6 لأن متتالية العدّ 5 و6 و7. وبين ليست أي عدد أصغر: بين 15 و17 العدد 16 لا 10.",
          "Juste avant, c'est un de moins. Juste après, c'est un de plus. Dans 12, 13, 14 : 12 est juste avant 13 et 14 juste après. Entre 5 et 7, il y a 6 car la suite est 5, 6, 7. Entre 15 et 17, c'est 16 et non 10."),
    ]),
    ("Many numbers can fit", "عدة أعداد قد تناسب", "Plusieurs nombres peuvent convenir", "15", [
        F("___ < 16"),
        T("For ___ < 16, there is not only one answer. 15 < 16 is right, 14 < 16 is right, and 8 < 16 is right too. Any number that makes the statement true is acceptable.",
          "في ___ < 16 لا يوجد جواب واحد فقط. 15 < 16 صحيحة و14 < 16 صحيحة و8 < 16 صحيحة أيضًا. أي عدد يجعل العبارة صحيحة مقبول.",
          "Pour ___ < 16, il n'y a pas qu'une réponse. 15 < 16 est juste, 14 < 16 aussi, 8 < 16 aussi. Tout nombre qui rend l'égalité vraie convient."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("< means less than and > means greater than. Right before is one step back; right after is one step forward; between lies between two consecutive numbers. To order numbers we start with the smallest and go to the greatest.",
          "< تعني أصغر من و> تعني أكبر من. قبل مباشرة خطوة إلى الوراء وبعد مباشرة خطوة إلى الأمام وبين هو العدد الواقع بين عددين متتاليين. وعند الترتيب نبدأ بالأصغر ونمضي إلى الأكبر.",
          "< veut dire plus petit que, > plus grand que. Juste avant : un pas en arrière ; juste après : un pas en avant ; entre : au milieu de deux nombres consécutifs. Pour ranger, on part du plus petit vers le plus grand."),
        F("UNDERSTAND THE QUANTITY → COMPARE → CHOOSE THE SIGN → CHECK ON THE SEQUENCE"),
    ]),
]

EXERCISES = [
    EX("1", "14", st("Circle the smallest number in each pair: 6 & 11, 15 & 19, 17 & 14, 12 & 8, 11 & 15, 18 & 10, 6 & 2, 16 & 13, 14 & 19.", "ضع دائرة حول العدد الأصغر في كل زوج: 6 و11، 15 و19، 17 و14، 12 و8، 11 و15، 18 و10، 6 و2، 16 و13، 14 و19.", "Entoure le plus petit nombre de chaque paire : 6 & 11, 15 & 19, 17 & 14, 12 & 8, 11 & 15, 18 & 10, 6 & 2, 16 & 13, 14 & 19."), [
        F("6   15   14   8   11   10   2   13   14"),
        T("If you hesitate, put both numbers on the number path: the one that comes first is the smallest.", "إذا ترددت ضع العددين على مسار الأعداد: الذي يأتي أولًا هو الأصغر.", "En cas de doute, place les deux nombres sur la droite : celui qui vient en premier est le plus petit."),
    ]),
    EX("2", "14", st("Circle the greatest number in each pair: 14 & 17, 16 & 13, 6 & 9, 11 & 8, 10 & 13, 11 & 15, 16 & 12, 3 & 5, 18 & 11.", "ضع دائرة حول العدد الأكبر في كل زوج: 14 و17، 16 و13، 6 و9، 11 و8، 10 و13، 11 و15، 16 و12، 3 و5، 18 و11.", "Entoure le plus grand nombre de chaque paire : 14 & 17, 16 & 13, 6 & 9, 11 & 8, 10 & 13, 11 & 15, 16 & 12, 3 & 5, 18 & 11."), [
        F("17   16   9   11   13   15   16   5   18"),
    ]),
    EX("3", "14", st("Write each number, then use > or <: (9 blocks, 5 blocks), (1 ten + 1 one, 8 ones), (1 ten, 1 ten + 4 ones).", "اكتب كل عدد ثم استعمل > أو <: (9 قوالب، 5 قوالب)، (عشرة + واحد، 8 آحاد)، (عشرة، عشرة + 4 آحاد).", "Écris chaque nombre puis utilise > ou < : (9 blocs, 5 blocs), (1 dizaine + 1 unité, 8 unités), (1 dizaine, 1 dizaine + 4 unités)."), [
        F("9 > 5        11 > 8        10 < 14"),
        T("In the third item both have one ten, so we compare the ones: 14 has 4 extra ones.", "في الثالثة لدى كليهما عشرة واحدة فنقارن الآحاد: في 14 أربعة آحاد زائدة.", "Dans le troisième, les deux ont une dizaine : on compare les unités, 14 en a 4 de plus."),
    ]),
    EX("4", "15", st("Complete using > or <: 6 _ 11, 19 _ 16, 15 _ 10, 8 _ 10, 4 _ 9, 10 _ 18, 17 _ 14, 15 _ 19, 12 _ 9.", "أكمل مستعملًا > أو <: 6 _ 11، 19 _ 16، 15 _ 10، 8 _ 10، 4 _ 9، 10 _ 18، 17 _ 14، 15 _ 19، 12 _ 9.", "Complète avec > ou < : 6 _ 11, 19 _ 16, 15 _ 10, 8 _ 10, 4 _ 9, 10 _ 18, 17 _ 14, 15 _ 19, 12 _ 9."), [
        F("6 < 11     19 > 16     15 > 10"),
        F("8 < 10     4 < 9     10 < 18"),
        F("17 > 14     15 < 19     12 > 9"),
    ]),
    EX("5", "15", st("Write the number between: 5 _ 7, 9 _ 11, 15 _ 17, 14 _ 16, 17 _ 19, 8 _ 10.", "اكتب العدد الواقع بين: 5 _ 7، 9 _ 11، 15 _ 17، 14 _ 16، 17 _ 19، 8 _ 10.", "Écris le nombre entre : 5 _ 7, 9 _ 11, 15 _ 17, 14 _ 16, 17 _ 19, 8 _ 10."), [
        F("6   10   16   15   18   9"),
        T("The number between two numbers that differ by 2 is one step after the first.", "العدد بين عددين بينهما فرق 2 هو خطوة بعد الأول.", "Entre deux nombres qui diffèrent de 2, c'est un pas après le premier."),
    ]),
    EX("6", "15", st("Write an appropriate number: ___ < 16, ___ < 12, ___ < 15, ___ < 19, ___ < 6, ___ < 11.", "اكتب عددًا مناسبًا: ___ < 16، ___ < 12، ___ < 15، ___ < 19، ___ < 6، ___ < 11.", "Écris un nombre convenable : ___ < 16, ___ < 12, ___ < 15, ___ < 19, ___ < 6, ___ < 11."), [
        F("15 < 16     11 < 12     14 < 15     18 < 19     5 < 6     10 < 11"),
        T("These are not the only answers. Any number that makes the statement true is acceptable.", "هذه ليست الأجوبة الوحيدة. أي عدد يجعل العبارة صحيحة مقبول.", "Ce ne sont pas les seules réponses. Tout nombre qui rend l'égalité vraie convient."),
    ]),
    EX("7", "15", st("Complete with the number right before and right after: 13; 5; 9; 18; 11; 10.", "أكمل بالعدد قبله مباشرة وبعده مباشرة: 13؛ 5؛ 9؛ 18؛ 11؛ 10.", "Complète avec le nombre juste avant et juste après : 13 ; 5 ; 9 ; 18 ; 11 ; 10."), [
        F("12, 13, 14      4, 5, 6      8, 9, 10"),
        F("17, 18, 19      10, 11, 12      9, 10, 11"),
        T("Right before is one less. Right after is one more.", "قبل مباشرة هو أقل بواحد وبعد مباشرة هو أكبر بواحد.", "Juste avant : un de moins. Juste après : un de plus."),
    ]),
    EX("8", "15", st("Open comparison: complete with appropriate numbers: __ < __ and __ > __.", "مقارنة مفتوحة: أكمل بأعداد مناسبة: __ < __ و__ > __.", "Comparaison ouverte : complète avec des nombres convenables : __ < __ et __ > __."), [
        F("7 < 12        18 > 10"),
        T("There are other correct answers. The relation must be true.", "هناك أجوبة صحيحة أخرى. المهم أن تكون العلاقة صحيحة.", "D'autres réponses sont justes. La relation doit être vraie."),
    ]),
    EX("9", "15", st("Arrange from the smallest to the greatest: 12, 8, 1, 16, 5, 3, 10.", "رتّب من الأصغر إلى الأكبر: 12، 8، 1، 16، 5، 3، 10.", "Range du plus petit au plus grand : 12, 8, 1, 16, 5, 3, 10."), [
        numpath(["1", "3", "5", "8", "10", "12", "16"], hi=None, size=44),
        F("1 < 3 < 5 < 8 < 10 < 12 < 16"),
    ]),
    EX("10", "", st("Mystery number: greater than 14 and less than 16.", "عدد غامض: أكبر من 14 وأصغر من 16.", "Nombre mystère : plus grand que 14 et plus petit que 16."), [
        numpath(["14", "15", "16"], hi=1, size=64),
        F("14 < 15 < 16"),
    ]),
    EX("11", "", st("Final check: smaller of 13 & 18; greater of 9 & 17; 12 _ 15; 19 _ 11; 7 _ 9; _ 16 _; arrange 14, 2, 11, 7; a number for ___ < 10.", "تقييم أخير: الأصغر من 13 و18؛ الأكبر من 9 و17؛ 12 _ 15؛ 19 _ 11؛ 7 _ 9؛ _ 16 _؛ رتّب 14 و2 و11 و7؛ عدد يحقق ___ < 10.", "Évaluation : le plus petit de 13 & 18 ; le plus grand de 9 & 17 ; 12 _ 15 ; 19 _ 11 ; 7 _ 9 ; _ 16 _ ; range 14, 2, 11, 7 ; un nombre pour ___ < 10."), [
        F("13     17     12 < 15     19 > 11"),
        F("8     15, 16, 17     2 < 7 < 11 < 14     9"),
        T("For ___ < 10 any number from 1 to 9 works; one example is 9.", "في ___ < 10 يصلح أي عدد من 1 إلى 9، ومثال ذلك 9.", "Pour ___ < 10, tout nombre de 1 à 9 convient ; par exemple 9."),
    ]),
]
