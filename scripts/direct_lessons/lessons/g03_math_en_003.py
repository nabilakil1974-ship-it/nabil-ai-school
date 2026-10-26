"""Grade 3 Mathematics — Addition."""
from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.lessons.g02_math_en_008 import vert

LESSON_ID = "G03-MATH-EN-003"
GRADE = 3
SUBJECT = "math"
TITLES = {"en": "Addition", "ar": "الجمع", "fr": "L'addition"}


def add(a, b, tag="V"):
    return vert([a, b], a + b, tag=tag)


THEORY = [
    ("Addition joins quantities", "الجمع يضمّ الكمّيات", "L'addition réunit des quantités", "16", [
        T("Hello, champion! Addition tells us that quantities are joined. 23 = 2 tens + 3 ones and 14 = 1 ten + 4 ones. Ones with ones: 3 + 4 = 7. Tens with tens: 2 + 1 = 3. So 23 + 14 = 37. Place value tells us which parts can be joined: ones with ones, tens with tens, hundreds with hundreds.",
          "مرحبًا يا بطل! الجمع يعني ضمّ كمّيات. 23 = عشرتان + 3 آحاد و14 = عشرة + 4 آحاد. الآحاد مع الآحاد: 3 + 4 = 7. العشرات مع العشرات: 2 + 1 = 3. إذن 23 + 14 = 37. قيمة المنزلة تحدد ما يُجمع معًا: آحاد مع آحاد وعشرات مع عشرات ومئات مع مئات.",
          "L'addition réunit des quantités : unités avec unités, dizaines avec dizaines. 23 + 14 = 37."),
        add(23, 14),
    ]),
    ("Add without regrouping", "الجمع دون إعادة تجميع", "Sans retenue", "16", [
        T("132 + 245. Ones: 2 + 5 = 7. Tens: 3 + 4 = 7. Hundreds: 1 + 2 = 3. The answer is 377. Always align the digits by place, never by the left edge.",
          "132 + 245. الآحاد: 2 + 5 = 7. العشرات: 3 + 4 = 7. المئات: 1 + 2 = 3. الجواب 377. نحاذي الأرقام حسب المنزلة لا حسب الحافة اليسرى.",
          "132 + 245 = 377 : on aligne par position."),
        add(132, 245),
    ]),
    ("Why regrouping works", "لماذا تنجح إعادة التجميع", "Pourquoi la retenue marche", "16", [
        T("28 + 17. Ones: 8 + 7 = 15 ones = 1 ten + 5 ones. Keep 5 ones and regroup the ten. Tens: 2 + 1 + 1 = 4. So 28 + 17 = 45. Regrouping does not change the value: 10 ones and 1 ten are the same amount.",
          "28 + 17. الآحاد: 8 + 7 = 15 واحدًا = عشرة + 5 آحاد. نبقي 5 آحاد ونجمّع العشرة. العشرات: 2 + 1 + 1 = 4. إذن 28 + 17 = 45. إعادة التجميع لا تغيّر القيمة: 10 آحاد وعشرة واحدة كمية واحدة.",
          "28 + 17 : 15 unités = 1 dizaine + 5 unités ; 45. La valeur ne change pas."),
        add(28, 17),
        F("46 + 27 = 73      6 + 7 = 13 = 1 ten + 3 ones"),
    ]),
    ("Regroup across hundreds", "إعادة التجميع إلى المئات", "Retenue vers les centaines", "17", [
        T("168 + 257. Ones: 8 + 7 = 15, write 5, regroup 1 ten. Tens: 6 + 5 + 1 = 12 tens, write 2, regroup 1 hundred. Hundreds: 1 + 2 + 1 = 4. The answer is 425. The 1 carried from the tens is worth 100, because it is 1 hundred.",
          "168 + 257. الآحاد: 8 + 7 = 15 نكتب 5 ونجمّع عشرة. العشرات: 6 + 5 + 1 = 12 عشرة نكتب 2 ونجمّع مئة. المئات: 1 + 2 + 1 = 4. الجواب 425. الواحد المحمول من العشرات قيمته 100 لأنه مئة.",
          "168 + 257 = 425 : 15 unités, 12 dizaines, 4 centaines."),
        add(168, 257),
        F("276 + 158 = 434"),
    ]),
    ("Zero in addition", "الصفر في الجمع", "Le zéro", "17", [
        T("304 + 25: write 25 as 025. Ones: 4 + 5 = 9. Tens: 0 + 2 = 2. Hundreds: 3 + 0 = 3. The answer is 329, not 554: the 2 is tens and the 5 is ones.",
          "304 + 25: نكتب 25 هكذا 025. الآحاد: 4 + 5 = 9. العشرات: 0 + 2 = 2. المئات: 3 + 0 = 3. الجواب 329 لا 554: 2 عشرات و5 آحاد.",
          "304 + 25 = 329 : 25 s'écrit 025."),
        add(304, 25),
    ]),
    ("Estimate before you trust", "نقدّر قبل أن نثق بالجواب", "Estimer d'abord", "17", [
        T("Someone says 198 + 203 = 4,010. Estimate: 198 ≈ 200 and 203 ≈ 200, so about 400. 4,010 cannot be right. The exact answer is 401. An estimate is not the exact answer; it detects unreasonable answers.",
          "قال أحدهم 198 + 203 = 4010. نقدّر: 198 ≈ 200 و203 ≈ 200 فالناتج نحو 400. إذن 4010 غير معقول. الجواب الدقيق 401. التقدير ليس الجواب الدقيق بل كاشف لعدم المعقولية.",
          "198 + 203 ≈ 400, donc 4010 est impossible ; exact : 401."),
        F("198 + 203 = 401"),
    ]),
    ("Addition in a problem", "الجمع في مسألة", "Dans un problème", "17", [
        T("A shelf has 126 books and 238 more are added. Quantities are joined, so we add: 126 + 238 = 364 books altogether. Check: about 100 + 200 = 300, so 364 is reasonable.",
          "على رفّ 126 كتابًا وأُضيف 238. الكمّيات تنضمّ فنجمع: 126 + 238 = 364 كتابًا في المجموع. نتحقق: نحو 100 + 200 = 300 فـ364 معقول.",
          "126 + 238 = 364 livres. Estimation : ≈ 300."),
        add(126, 238),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Say what the carried digit means. 8 + 7 = 15 ones is 1 ten and 5 ones. 12 tens is 1 hundred and 2 tens. Estimate before, regroup during, check after.",
          "نقول ما يعنيه الرقم المحمول. 8 + 7 = 15 واحدًا أي عشرة و5 آحاد، و12 عشرة أي مئة وعشرتان. نقدّر قبل ونعيد التجميع أثناء ونتحقق بعد.",
          "Estimer avant, regrouper pendant, vérifier après."),
        F("ALIGN → ONES → TENS → HUNDREDS → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "16", st("Calculate 214 + 163.", "احسب 214 + 163.", "Calcule 214 + 163."), [add(214, 163), F("377")]),
    EX("2", "16", st("Error detective: 24 + 103 with the 4 placed under the 0.", "المحقق: 24 + 103 وُضع 4 تحت 0.", "Détective : 24 + 103 mal aligné."), [
        T("Digits must be aligned by place: ones under ones, tens under tens.", "نحاذي الأرقام حسب المنزلة: آحاد تحت آحاد وعشرات تحت عشرات.", "Aligner par position."), add(24, 103),
    ]),
    EX("3", "16", st("Calculate 46 + 27 and check by decomposition.", "احسب 46 + 27 وتحقق بالتحليل.", "Calcule 46 + 27 et vérifie."), [
        add(46, 27), F("40 + 20 + 6 + 7 = 60 + 13 = 73"),
    ]),
    EX("4", "17", st("Calculate 276 + 158 and check.", "احسب 276 + 158 وتحقق.", "Calcule 276 + 158 et vérifie."), [
        add(276, 158), F("276 + 100 = 376 → 426 → 434"),
    ]),
    EX("5", "17", st("Error detective: 304 + 25 = 554.", "المحقق: 304 + 25 = 554.", "Détective : 304 + 25 = 554."), [F("304 + 25 = 329")]),
    EX("6", "17", st("Guided: 32+46, 125+243, 57+26, 184+239, 407+82.", "تدريب: 32+46، 125+243، 57+26، 184+239، 407+82.", "Guidé."), [
        F("78      368      83      423      489"),
        T("9 + 8 = 17 ones = 1 ten + 7 ones, so regrouping is needed.", "9 + 8 = 17 واحدًا = عشرة و7 آحاد لذلك نحتاج إعادة التجميع.", "9 + 8 = 17 : retenue."),
    ]),
    EX("7", "17", st("Ladder: 12+15; 213+354; 48+35; 176+248; 502+76; 389+205.", "سلّم: 12+15؛ 213+354؛ 48+35؛ 176+248؛ 502+76؛ 389+205.", "Échelle."), [
        F("27      567      83      424      578      594"),
        T("389 + 205 is closer to 600.", "389 + 205 أقرب إلى 600.", "Plus proche de 600."),
    ]),
    EX("8", "17", st("Error detective: 27 + 18 = 315.", "المحقق: 27 + 18 = 315.", "Détective : 27 + 18 = 315."), [
        F("27 + 18 = 45"),
        T("7 + 8 = 15 ones is 1 ten and 5 ones; carrying 1 ten adds 1 to the tens column.", "7 + 8 = 15 آحاد أي عشرة و5 آحاد، وحمل واحد يعني إضافة عشرة إلى عمود العشرات.", "15 unités = 1 dizaine + 5 unités."),
    ]),
    EX("9", "17", st("Calculate: 41+27, 132+256, 68+19, 275+148, 603+89.", "احسب: 41+27، 132+256، 68+19، 275+148، 603+89.", "Calcule."), [F("68      388      87      423      692")]),
    EX("10", "17", st("Missing addend: 34 + __ = 60; __ + 25 = 70.", "العدد الناقص: 34 + … = 60؛ … + 25 = 70.", "Terme manquant."), [F("26      45")]),
    EX("11", "17", st("147 caps on Monday and 186 on Tuesday. How many altogether?", "جُمع 147 غطاءً يوم الاثنين و186 يوم الثلاثاء. كم المجموع؟", "147 bouchons lundi, 186 mardi. Total ?"), [add(147, 186), F("333")]),
    EX("12", "17", st("Is 295 + 108 = 393 correct?", "هل 295 + 108 = 393 صحيح؟", "295 + 108 = 393 ?"), [F("No: 295 + 108 = 403"), F("295 + 100 = 395,  395 + 8 = 403")]),
    EX("13", "", st("Final check: 36+27; 158+267; estimate 397+204.", "تقييم: 36+27؛ 158+267؛ قدّر 397+204.", "Évaluation."), [F("63      425      about 600, exact 601")]),
]
