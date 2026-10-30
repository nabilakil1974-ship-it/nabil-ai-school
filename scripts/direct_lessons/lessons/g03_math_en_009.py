"""Grade 3 Mathematics — Subtracting with regrouping."""
from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.draw import blocks, vsub, bar_model

LESSON_ID = "G03-MATH-EN-009"
GRADE = 3
SUBJECT = "math"
TITLES = {"en": "Subtracting", "ar": "الطرح مع الاستلاف", "fr": "Soustraire avec échange"}


def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}


QUIZ = [
    {"q": "In 345 − 128, the ones digit 5 is smaller than 8. What do we do?", "opts": ["Exchange 1 ten for 10 ones", "Subtract 5 from 8", "Add 128", "Ignore the ones"], "a": 0,
     "why": {"Subtract 5 from 8": _w("That reverses the numbers: 8 − 5 gives 3 but 5 is the amount we start with.", "هذا يعكس العددين: نبدأ بـ 5 لا بـ 8.", "On part de 5."),
             "Add 128": _w("We are subtracting.", "نحن نطرح.", "On soustrait."),
             "Ignore the ones": _w("Every column must be used.", "كل عمود يجب أن يُستعمل.", "Chaque colonne compte.")}, "ok": "Exchange 1 ten for 10 ones"},
    {"q": "Calculate 472 − 185.", "opts": ["287", "313", "397", "293"], "a": 0,
     "why": {"313": _w("313 comes from subtracting the smaller digit from the larger in every column.", "313 تأتي من طرح الرقم الأصغر من الأكبر في كل عمود.", "Erreur de colonnes."),
             "397": _w("Check: 397 + 185 = 582, not 472.", "تحقق: 397 + 185 = 582 لا 472.", "397 + 185 = 582."),
             "293": _w("Check: 293 + 185 = 478, not 472.", "تحقق: 293 + 185 = 478.", "478.")}, "ok": "287"},
    {"q": "Calculate 302 − 147.", "opts": ["155", "245", "165", "255"], "a": 0,
     "why": {"245": _w("There is a zero in the tens: borrow from the hundreds first, then the tens become 9 after lending.", "في العشرات صفر: نستلف من المئات أولًا.", "Il y a un 0."),
             "165": _w("Check: 165 + 147 = 312.", "تحقق: 165 + 147 = 312.", "312."),
             "255": _w("Check: 255 + 147 = 402.", "تحقق: 255 + 147 = 402.", "402.")}, "ok": "155"},
]

THEORY = [
    ("Why we exchange", "لماذا نستلف", "Pourquoi échanger", "28", [
        T("Hello, champion! Look at 345 − 128. In the ones column we need 5 − 8, but 5 is too small. We cannot take 8 ones from 5 ones. So we exchange: 1 ten is the same value as 10 ones. We take 1 ten from 4 tens (3 tens remain) and put the 10 ones with the 5 ones: 15 ones.",
          "مرحبًا يا بطل! انظر إلى 345 − 128. في عمود الآحاد نحتاج 5 − 8 لكن 5 صغيرة. لا نستطيع أخذ 8 آحاد من 5 آحاد. لذلك نستبدل: عشرة واحدة تساوي 10 آحاد. نأخذ عشرة من 4 عشرات فتبقى 3 عشرات ونضيف 10 آحاد إلى 5 آحاد فتصبح 15 آحادًا.",
          "5 − 8 impossible : on échange 1 dizaine contre 10 unités → 15 unités."),
        blocks(3, 3, 15, tag="B1", label=False),
        T("The total is the same: 3 hundreds, 3 tens and 15 ones is still 345. The exchange changes how we group the value, not the value. Same value, new grouping.",
          "المجموع لم يتغير: 3 مئات و3 عشرات و15 آحادًا ما زالت 345. الاستبدال يغيّر طريقة تجميع القيمة لا القيمة. القيمة نفسها بتجميع جديد.",
          "Même valeur, nouveau groupement : 345."),
        F("1 hundred = 10 tens      1 ten = 10 ones"),
    ]),
    ("Regroup the ones", "استلاف من العشرات", "Échanger les unités", "28", [
        T("Now finish 345 − 128 column by column. Ones: 15 − 8 = 7. Tens: 3 − 2 = 1 (we only have 3 tens left). Hundreds: 3 − 1 = 2. The difference is 217. Check: 217 + 128 = 345 ✓.",
          "نكمل 345 − 128 عمودًا بعد عمود. الآحاد: 15 − 8 = 7. العشرات: 3 − 2 = 1 (بقيت 3 عشرات فقط). المئات: 3 − 1 = 2. الفرق 217. تحقق: 217 + 128 = 345 ✓.",
          "15 − 8 = 7 ; 3 − 2 = 1 ; 3 − 1 = 2 : 217."),
        vsub(345, 128, tag="B2"),
        F("345 − 128 = 217      217 + 128 = 345 ✓"),
    ]),
    ("Regroup the tens", "استلاف من المئات", "Échanger les dizaines", "28", [
        T("Sometimes we exchange twice. 472 − 185. Ones: 2 is smaller than 5, so take 1 ten from 7 tens (6 remain): 12 − 5 = 7. Tens: now 6 is smaller than 8, so take 1 hundred from 4 hundreds (3 remain) and make 16 tens: 16 − 8 = 8. Hundreds: 3 − 1 = 2. The answer is 287.",
          "أحيانًا نستلف مرتين. 472 − 185. الآحاد: 2 أصغر من 5 فنأخذ عشرة من 7 عشرات (تبقى 6): 12 − 5 = 7. العشرات: الآن 6 أصغر من 8 فنأخذ مئة من 4 مئات (تبقى 3) ونجعلها 16 عشرة: 16 − 8 = 8. المئات: 3 − 1 = 2. الجواب 287.",
          "Deux échanges : 12 − 5 = 7 ; 16 − 8 = 8 ; 3 − 1 = 2 → 287."),
        vsub(472, 185, tag="B3"),
        F("472 − 185 = 287      287 + 185 = 472 ✓"),
    ]),
    ("A zero in the middle", "صفر في المنتصف", "Un zéro au milieu", "29", [
        T("302 − 147 has a zero in the tens. The ones need a ten but there are 0 tens. So first exchange 1 hundred for 10 tens: 2 hundreds and 10 tens. Then exchange 1 ten for 10 ones: 9 tens and 12 ones. Now subtract: 12 − 7 = 5, 9 − 4 = 5, 2 − 1 = 1. The answer is 155.",
          "في 302 − 147 صفر في العشرات. الآحاد تحتاج عشرة لكن لا عشرات. لذلك نستبدل أولًا مئة بـ 10 عشرات: مئتان و10 عشرات. ثم نستبدل عشرة بـ 10 آحاد: 9 عشرات و12 آحادًا. نطرح الآن: 12 − 7 = 5 و9 − 4 = 5 و2 − 1 = 1. الجواب 155.",
          "302 : échanger 1 centaine → 10 dizaines, puis 1 dizaine → 10 unités : 155."),
        vsub(302, 147, tag="B4"),
        F("302 − 147 = 155      155 + 147 = 302 ✓"),
        T("Error detective! A learner calculates 345 − 128 as 223 by always subtracting the smaller digit from the larger: 8 − 5 = 3, 4 − 2 = 2, 3 − 1 = 2. But the ones start with 5, so 5 cannot give away 8. Check: 223 + 128 = 351, not 345. So there is a mistake.",
          "المحقق! حسب متعلّم 345 − 128 فوجد 223 لأنه طرح الأصغر من الأكبر دائمًا: 8 − 5 = 3 و4 − 2 = 2 و3 − 1 = 2. لكن الآحاد تبدأ بـ 5 فلا تستطيع أن تعطي 8. التحقق: 223 + 128 = 351 لا 345. إذن في الحل خطأ.",
          "Erreur : 223 (223 + 128 = 351 ≠ 345). Juste : 217."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Written subtraction: align H, T, O. Start with the ones. If the top digit is smaller, exchange one unit from the next higher place for ten units here, and remember to lower the digit you took from. Subtract, then check by adding. The value never changes — only the grouping.",
          "الطرح الكتابي: نرتّب المئات والعشرات والآحاد. نبدأ بالآحاد. إذا كان الرقم العلوي أصغر نستبدل وحدة من المنزلة الأعلى بعشر وحدات هنا ونتذكر أن ننقص الرقم الذي أخذنا منه. نطرح ثم نتحقق بالجمع. القيمة لا تتغير بل التجميع فقط.",
          "Aligner, commencer par les unités, échanger si besoin, vérifier."),
        F("ALIGN → CHECK THE PLACE → EXCHANGE → SUBTRACT → CHECK"),
    ]),
]


def _ex(n, en, ar, fr, steps):
    return EX(n, "", st(en, ar, fr), steps)


EXERCISES = [
    _ex("1", "Calculate 253 − 126.", "احسب 253 − 126.", "Calcule 253 − 126.", [T("Ones: 3 < 6, exchange: 13 − 6 = 7 (tens 4 left). Tens 4 − 2 = 2. Hundreds 2 − 1 = 1. Answer 127.", "الآحاد: 3 < 6 نستلف: 13 − 6 = 7 (بقيت 4 عشرات). العشرات 4 − 2 = 2. المئات 2 − 1 = 1. الجواب 127.", "127."), vsub(253, 126, tag="Y1"), F("253 − 126 = 127      127 + 126 = 253 ✓")]),
    _ex("2", "Calculate 341 − 175.", "احسب 341 − 175.", "Calcule 341 − 175.", [T("Ones: 1 < 5: 11 − 5 = 6 (tens 3 left). Tens: 3 < 7: 13 − 7 = 6 (hundreds 2 left). Hundreds: 2 − 1 = 1. Answer 166.", "الآحاد 1 < 5: 11 − 5 = 6 (بقيت 3 عشرات). العشرات 3 < 7: 13 − 7 = 6 (بقيت مئتان). المئات 2 − 1 = 1. الجواب 166.", "166."), vsub(341, 175, tag="Y2"), F("341 − 175 = 166      166 + 175 = 341 ✓")]),
    _ex("3", "Calculate 500 − 238.", "احسب 500 − 238.", "Calcule 500 − 238.", [T("Two zeros: exchange a hundred for 10 tens, then a ten for 10 ones: 4 hundreds, 9 tens, 10 ones. 10 − 8 = 2, 9 − 3 = 6, 4 − 2 = 2. Answer 262.", "صفران: نستبدل مئة بـ 10 عشرات ثم عشرة بـ 10 آحاد: 4 مئات و9 عشرات و10 آحاد. 10 − 8 = 2 و9 − 3 = 6 و4 − 2 = 2. الجواب 262.", "262."), vsub(500, 238, tag="Y3"), F("500 − 238 = 262      262 + 238 = 500 ✓")]),
    _ex("4", "Calculate 624 − 358.", "احسب 624 − 358.", "Calcule 624 − 358.", [T("Ones: 4 < 8: 14 − 8 = 6 (tens 1 left). Tens: 1 < 5: 11 − 5 = 6 (hundreds 5 left). Hundreds 5 − 3 = 2. Answer 266.", "الآحاد 4 < 8: 14 − 8 = 6 (بقيت عشرة). العشرات 1 < 5: 11 − 5 = 6 (بقيت 5 مئات). المئات 5 − 3 = 2. الجواب 266.", "266."), vsub(624, 358, tag="Y4"), F("624 − 358 = 266      266 + 358 = 624 ✓")]),
    _ex("5", "Calculate 705 − 389.", "احسب 705 − 389.", "Calcule 705 − 389.", [T("Zero in the tens: exchange hundred then ten. 6 hundreds, 9 tens, 15 ones. 15 − 9 = 6, 9 − 8 = 1, 6 − 3 = 3. Answer 316.", "صفر في العشرات: نستبدل مئة ثم عشرة. 6 مئات و9 عشرات و15 آحادًا. 15 − 9 = 6 و9 − 8 = 1 و6 − 3 = 3. الجواب 316.", "316."), vsub(705, 389, tag="Y5"), F("705 − 389 = 316      316 + 389 = 705 ✓")]),
    _ex("6", "Calculate 900 − 467.", "احسب 900 − 467.", "Calcule 900 − 467.", [T("8 hundreds, 9 tens, 10 ones. 10 − 7 = 3, 9 − 6 = 3, 8 − 4 = 4. Answer 433.", "8 مئات و9 عشرات و10 آحاد. 10 − 7 = 3 و9 − 6 = 3 و8 − 4 = 4. الجواب 433.", "433."), vsub(900, 467, tag="Y6"), F("900 − 467 = 433      433 + 467 = 900 ✓")]),
    _ex("7", "Calculate 812 − 456.", "احسب 812 − 456.", "Calcule 812 − 456.", [T("Ones: 2 < 6: 12 − 6 = 6 (tens 0 left). Tens: 0 < 5: take a hundred: 10 − 5 = 5 (hundreds 7 left). Hundreds 7 − 4 = 3. Answer 356.", "الآحاد 2 < 6: 12 − 6 = 6 (بقي صفر من العشرات). العشرات 0 < 5: نستلف مئة: 10 − 5 = 5 (بقيت 7 مئات). المئات 7 − 4 = 3. الجواب 356.", "356."), vsub(812, 456, tag="Y7"), F("812 − 456 = 356      356 + 456 = 812 ✓")]),
    _ex("8", "A library has 432 books. 187 are lent. How many remain on the shelves?", "في مكتبة 432 كتابًا أُعير منها 187. كم بقي على الرفوف؟", "432 livres, 187 prêtés. Combien restent ?", [T("432 − 187: ones 12 − 7 = 5 (tens 2), tens 12 − 8 = 4 (hundreds 3), hundreds 3 − 1 = 2. Answer 245. Check: 245 + 187 = 432 ✓.", "432 − 187: آحاد 12 − 7 = 5 (بقيت عشرتان) وعشرات 12 − 8 = 4 (بقيت 3 مئات) ومئات 3 − 1 = 2. الجواب 245. تحقق: 245 + 187 = 432 ✓.", "245."), vsub(432, 187, tag="Y8"), F("245 books remain")]),
    _ex("9", "Sara had 600 stickers and gave 275 away. How many are left?", "عند سارة 600 ملصق أعطت منها 275. كم بقي؟", "600 autocollants, 275 donnés. Combien reste-t-il ?", [T("600 − 275 = 325. Exchange: 5 hundreds, 9 tens, 10 ones; 10 − 5 = 5, 9 − 7 = 2, 5 − 2 = 3. Check: 325 + 275 = 600 ✓.", "600 − 275 = 325. نستبدل: 5 مئات و9 عشرات و10 آحاد؛ 10 − 5 = 5 و9 − 7 = 2 و5 − 2 = 3. تحقق: 325 + 275 = 600 ✓.", "325."), bar_model(600, 275, 325, tag="Y9"), F("600 − 275 = 325")]),
    _ex("10", "Find the missing number: 503 − ? = 247.", "جد العدد الناقص: 503 − ؟ = 247.", "Trouve : 503 − ? = 247.", [T("503 − 247 = 256 (13 − 7 = 6, 9 − 4 = 5, 4 − 2 = 2). Check: 503 − 256 = 247 ✓.", "503 − 247 = 256 (13 − 7 = 6 و9 − 4 = 5 و4 − 2 = 2). تحقق: 503 − 256 = 247 ✓.", "256."), vsub(503, 247, tag="Y10"), F("256")]),
    _ex("11", "Error detective: 'I calculated 345 − 128 and got 223.' Find and fix the error.", "المحقق: «حسبت 345 − 128 فوجدت 223». جد الخطأ وصحّحه.", "Détective : 345 − 128 = 223 ?", [T("Check by adding: 223 + 128 = 351, not 345. The learner subtracted the smaller digit from the larger in each column (8 − 5, 4 − 2, 3 − 1). The correct way: exchange a ten, 15 − 8 = 7, 3 − 2 = 1, 3 − 1 = 2: 217.", "التحقق بالجمع: 223 + 128 = 351 لا 345. طرح المتعلّم الرقم الأصغر من الأكبر في كل عمود (8 − 5 و4 − 2 و3 − 1). الصحيح: نستلف عشرة 15 − 8 = 7 و3 − 2 = 1 و3 − 1 = 2: 217.", "217."), vsub(345, 128, tag="Y11"), F("345 − 128 = 217")]),
    _ex("12", "Explain: when we exchange 1 hundred for 10 tens, does the number change?", "فسّر: عندما نستبدل مئة بـ 10 عشرات هل يتغير العدد؟", "Explique : échanger 1 centaine contre 10 dizaines change-t-il le nombre ?", [T("No. 1 hundred is worth 100 and 10 tens are worth 10 × 10 = 100. The value stays the same; only the grouping changes. That is why the final answer is still correct.", "لا. المئة قيمتها 100 والعشر عشرات قيمتها 10 × 10 = 100. القيمة نفسها وتتغير طريقة التجميع فقط. لذلك يبقى الجواب النهائي صحيحًا.", "Non : 1 centaine = 100 = 10 dizaines."), F("1 hundred = 10 tens = 100")]),
]
