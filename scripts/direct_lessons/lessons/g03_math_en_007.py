"""Grade 3 Mathematics — Addition and Subtraction (related operations)."""
from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.draw import hops, bar_model

LESSON_ID = "G03-MATH-EN-007"
GRADE = 3
SUBJECT = "math"
TITLES = {"en": "Adding and Subtraction", "ar": "الجمع والطرح", "fr": "Addition et soustraction"}


def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}


QUIZ = [
    {"q": "Tom has 35 cards. He gets 24 more. How many now?", "opts": ["59", "11", "49", "69"], "a": 0,
     "why": {"11": _w("11 is 35 − 24. Here we join, so we add.", "11 هو 35 − 24. هنا نضم فنجمع.", "On ajoute."),
             "49": _w("35 + 14 = 49. Add 24 exactly: 35 + 20 = 55, 55 + 4 = 59.", "35 + 14 = 49. أضف 24: 35 + 20 = 55 ثم + 4 = 59.", "35 + 24 = 59."),
             "69": _w("Too much: 35 + 24 = 59.", "كثير: 35 + 24 = 59.", "59.")}, "ok": "59"},
    {"q": "If 36 + 27 = 63, which subtraction is true?", "opts": ["63 − 27 = 36", "27 − 36 = 63", "36 − 63 = 27", "63 + 27 = 36"], "a": 0,
     "why": {"27 − 36 = 63": _w("A smaller number minus a bigger gives no 63.", "لا يعطي طرح الأكبر من الأصغر 63.", "Impossible."),
             "36 − 63 = 27": _w("The whole must come first: 63 − 36 = 27.", "الكل يأتي أولًا: 63 − 36 = 27.", "63 − 36 = 27."),
             "63 + 27 = 36": _w("Adding makes the number bigger than 63.", "الجمع يزيد على 63.", "Plus grand que 63.")}, "ok": "63 − 27 = 36"},
    {"q": "Ali has 35 stickers. He has 8 more than Sara. How many does Sara have?", "opts": ["27", "43", "8", "28"], "a": 0,
     "why": {"43": _w("The word more tempts us to add, but Ali has MORE, so Sara has fewer: 35 − 8.", "كلمة أكثر تغرينا بالجمع لكن علي هو الأكثر فسارة عندها أقل: 35 − 8.", "Sara en a moins."),
             "8": _w("8 is the difference, not Sara's number.", "8 هو الفرق لا عدد سارة.", "8 = différence."),
             "28": _w("35 − 8 = 27, not 28.", "35 − 8 = 27.", "27.")}, "ok": "27"},
]

THEORY = [
    ("Joining means adding", "الضم يعني الجمع", "Réunir = additionner", "24", [
        T("Hello, champion! When two parts are put together to make a whole, we add. Tom has 35 cards and gets 24 more. The parts are 35 and 24. The whole is unknown. 35 + 24: 35 + 20 = 55, then 55 + 4 = 59. Tom has 59 cards.",
          "مرحبًا يا بطل! عندما نضم جزأين لنصنع كلًّا نجمع. عند توم 35 بطاقة وأخذ 24 أخرى. الجزآن 35 و24 والكل مجهول. 35 + 24: 35 + 20 = 55 ثم 55 + 4 = 59. عند توم 59 بطاقة.",
          "Deux parties réunies : on additionne. 35 + 24 = 59."),
        bar_model("?", 35, 24, tag="M1"),
        F("35 + 24 = 59"),
        T("The bar model shows the picture: the two small boxes together are as long as the big box. Unknown whole → add the parts.",
          "يبيّن نموذج الأشرطة الصورة: الصندوقان الصغيران معًا بطول الصندوق الكبير. الكل مجهول ← نجمع الجزأين.",
          "Tout inconnu → on additionne les parties."),
    ]),
    ("Finding a missing part means subtracting", "إيجاد جزء ناقص يعني الطرح", "Chercher une partie = soustraire", "24", [
        T("Now the whole is known: 59 cards in all. Tom has 35 in his box. The rest are in his bag. How many in the bag? A part is missing. We take the known part away from the whole: 59 − 35 = 24. Count up to check: 35 + 24 = 59 ✓.",
          "الآن الكل معروف: 59 بطاقة. في علبة توم 35 والباقي في حقيبته. كم في الحقيبة؟ جزء ناقص. نطرح الجزء المعروف من الكل: 59 − 35 = 24. نتحقق بالعدّ إلى الأعلى: 35 + 24 = 59 ✓.",
          "Total 59, une partie 35 : 59 − 35 = 24."),
        bar_model(59, 35, "?", tag="M2"),
        F("59 − 35 = 24      check: 35 + 24 = 59 ✓"),
        T("Subtracting can also be a jump back on the number line: from 75 take away 40 to land on 35.",
          "ويمكن للطرح أن يكون قفزة إلى الخلف على خط الأعداد: من 75 نطرح 40 فنصل إلى 35.",
          "Soustraire = reculer sur la droite numérique."),
        hops(75, [-40], tag="H1"),
        F("75 − 40 = 35"),
    ]),
    ("Fact family: four related sentences", "أسرة الحقائق: أربع جمل مترابطة", "Famille de calculs : quatre égalités liées", "24", [
        T("Three numbers, 35, 24 and 59, give a family of four sentences. Two additions: 35 + 24 = 59 and 24 + 35 = 59. Two subtractions: 59 − 35 = 24 and 59 − 24 = 35. The biggest number, the whole, is at the start of every subtraction and at the end of every addition.",
          "ثلاثة أعداد 35 و24 و59 تعطي أسرة من أربع جمل. جمعان: 35 + 24 = 59 و24 + 35 = 59. وطرحان: 59 − 35 = 24 و59 − 24 = 35. العدد الأكبر، أي الكل، في أول كل طرح وفي آخر كل جمع.",
          "35 + 24 = 59 ; 24 + 35 = 59 ; 59 − 35 = 24 ; 59 − 24 = 35."),
        F("35 + 24 = 59      24 + 35 = 59"),
        F("59 − 35 = 24      59 − 24 = 35"),
        bar_model(59, 35, 24, tag="M3"),
    ]),
    ("Check with the inverse", "تحقق بالعملية العكسية", "Vérifier avec l'opération inverse", "25", [
        T("Addition and subtraction undo each other. If 36 + 27 = 63 then 63 − 27 must give back 36. Test: 63 − 27 = 36 ✓. A subtraction is checked with an addition: 82 − 45 = 37, and 37 + 45 = 82 ✓.",
          "الجمع والطرح يلغي أحدهما الآخر. إذا كان 36 + 27 = 63 فإن 63 − 27 يجب أن يعطي 36. نختبر: 63 − 27 = 36 ✓. ونتحقق من الطرح بالجمع: 82 − 45 = 37 و37 + 45 = 82 ✓.",
          "36 + 27 = 63 → 63 − 27 = 36 ; 82 − 45 = 37 → 37 + 45 = 82."),
        F("36 + 27 = 63  →  63 − 27 = 36"),
        F("82 − 45 = 37  →  37 + 45 = 82"),
        hops(36, [27], tag="H2"),
        T("If the check does not return to the starting number, there is a mistake. Look for it before you say 'finished'.",
          "إذا لم يعد التحقق إلى العدد الأول ففي الحل خطأ. ابحث عنه قبل أن تقول «انتهيت».",
          "Si le contrôle ne redonne pas le départ : erreur."),
    ]),
    ("How many more? Comparing", "كم أكثر؟ المقارنة", "De combien de plus ? Comparer", "25", [
        T("To compare, put two bars side by side. Mia has 52 stickers and Noor has 37. How many more has Mia? The difference is 52 − 37 = 15 (37 + 3 = 40, 40 + 12 = 52, and 3 + 12 = 15). Mia has 15 more than Noor, Noor has 15 fewer.",
          "للمقارنة نضع شريطين جنبًا إلى جنب. عند ميا 52 ملصقًا وعند نور 37. كم ملصقًا أكثر عند ميا؟ الفرق 52 − 37 = 15 (37 + 3 = 40 و40 + 12 = 52 و3 + 12 = 15). عند ميا 15 أكثر من نور وعند نور 15 أقل.",
          "52 − 37 = 15 : Mia en a 15 de plus."),
        bar_model(52, 37, 15, tag="M4"),
        F("52 − 37 = 15      37 + 15 = 52 ✓"),
        T("Error detective! 'Ali has 8 more than Sara. Ali has 35. How many has Sara?' The word 'more' tempts us to add 35 + 8 = 43, but Ali is the bigger number. Sara has less: 35 − 8 = 27. Do not choose the operation from one word alone; think of the picture.",
          "المحقق! «عند علي 8 أكثر من سارة. عند علي 35. كم عند سارة؟» كلمة «أكثر» تغري بجمع 35 + 8 = 43 لكن علي هو الأكبر. عند سارة أقل: 35 − 8 = 27. لا نختار العملية من كلمة واحدة بل نفكر في الصورة.",
          "« 8 de plus » mais Ali est le plus grand : Sara a 35 − 8 = 27."),
        F("Sara: 35 − 8 = 27      check: 27 + 8 = 35 ✓"),
    ]),
    ("Missing number in an addition", "العدد الناقص في جمع", "Terme manquant", "25", [
        T("What number goes in 40 + ? = 75? It is a missing part, so subtract: 75 − 40 = 35. Check: 40 + 35 = 75 ✓. And for ? + 18 = 50: 50 − 18 = 32, check 32 + 18 = 50 ✓.",
          "ما العدد في 40 + ؟ = 75؟ جزء ناقص إذن نطرح: 75 − 40 = 35. تحقق: 40 + 35 = 75 ✓. وفي ؟ + 18 = 50: 50 − 18 = 32 وتحقق 32 + 18 = 50 ✓.",
          "40 + ? = 75 → 75 − 40 = 35 ; ? + 18 = 50 → 32."),
        bar_model(75, 40, "?", tag="M5"),
        F("40 + 35 = 75      32 + 18 = 50"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Join parts to find the whole: add. Know the whole and one part: subtract to find the other. Compare: subtract the smaller from the bigger. Three numbers make a family of four sentences. Always check with the inverse operation, and think of the picture, not only of one keyword.",
          "نضم الأجزاء لنجد الكل: نجمع. نعرف الكل وجزءًا: نطرح لنجد الآخر. للمقارنة نطرح الأصغر من الأكبر. ثلاثة أعداد تصنع أسرة من أربع جمل. تحقق دائمًا بالعملية العكسية وفكر في الصورة لا في كلمة واحدة.",
          "Réunir : +. Partie manquante : −. Comparer : grand − petit. Vérifier par l'inverse."),
        F("whole = part + part        part = whole − part"),
    ]),
]


def _ex(n, en, ar, fr, steps):
    return EX(n, "", st(en, ar, fr), steps)


EXERCISES = [
    _ex("1", "Calculate 46 + 33 and check with the inverse.", "احسب 46 + 33 وتحقق بالعملية العكسية.", "Calcule 46 + 33 et vérifie.", [T("46 + 30 = 76, then 76 + 3 = 79. Check: 79 − 33 = 46 ✓.", "46 + 30 = 76 ثم 76 + 3 = 79. تحقق: 79 − 33 = 46 ✓.", "79."), bar_model("?", 46, 33, tag="X1"), F("46 + 33 = 79")]),
    _ex("2", "Calculate 90 − 36 and check.", "احسب 90 − 36 وتحقق.", "Calcule 90 − 36.", [T("90 − 30 = 60, then 60 − 6 = 54. Check: 54 + 36 = 90 ✓.", "90 − 30 = 60 ثم 60 − 6 = 54. تحقق: 54 + 36 = 90 ✓.", "54."), hops(90, [-30, -6], tag="X2"), F("90 − 36 = 54")]),
    _ex("3", "Write the four sentences of the family 28, 17, 45.", "اكتب الجمل الأربع لأسرة 28 و17 و45.", "Écris la famille de 28, 17, 45.", [T("The whole is 45 (biggest). 28 + 17 = 45; 17 + 28 = 45; 45 − 28 = 17; 45 − 17 = 28.", "الكل 45 (الأكبر). 28 + 17 = 45؛ 17 + 28 = 45؛ 45 − 28 = 17؛ 45 − 17 = 28.", "4 égalités."), bar_model(45, 28, 17, tag="X3"), F("28 + 17 = 45   17 + 28 = 45   45 − 28 = 17   45 − 17 = 28")]),
    _ex("4", "A farm has 64 hens and 29 ducks. How many birds in all?", "في مزرعة 64 دجاجة و29 بطة. كم طائرًا في المجموع؟", "64 poules et 29 canards : combien d'oiseaux ?", [T("Join → add. 64 + 29 = 64 + 30 − 1 = 93.", "ضم ← جمع. 64 + 29 = 64 + 30 − 1 = 93.", "93."), bar_model("?", 64, 29, tag="X4"), F("64 + 29 = 93      check: 93 − 29 = 64 ✓")]),
    _ex("5", "A box holds 85 pencils. 48 are red, the others blue. How many blue?", "في علبة 85 قلمًا. منها 48 حمراء والباقي زرقاء. كم الزرقاء؟", "85 crayons dont 48 rouges. Combien de bleus ?", [T("Whole 85, known part 48, missing part: 85 − 48 = 37 (85 − 50 = 35, plus 2).", "الكل 85 والجزء المعروف 48 والناقص: 85 − 48 = 37 (85 − 50 = 35 ثم + 2).", "37."), bar_model(85, 48, "?", tag="X5"), F("85 − 48 = 37      check: 48 + 37 = 85 ✓")]),
    _ex("6", "Mia has 52 stickers, Noor 37. How many more has Mia?", "عند ميا 52 ملصقًا وعند نور 37. كم أكثر عند ميا؟", "Mia 52, Noor 37 : de combien de plus ?", [T("Compare: 52 − 37 = 15.", "نقارن: 52 − 37 = 15.", "15."), bar_model(52, 37, 15, tag="X6"), F("52 − 37 = 15")]),
    _ex("7", "Find the missing number: 40 + ? = 75.", "جد العدد الناقص: 40 + ؟ = 75.", "Trouve le nombre manquant : 40 + ? = 75.", [T("75 − 40 = 35.", "75 − 40 = 35.", "35."), F("40 + 35 = 75 ✓")]),
    _ex("8", "Find the missing number: ? + 18 = 50.", "جد العدد الناقص: ؟ + 18 = 50.", "Trouve : ? + 18 = 50.", [T("50 − 18 = 32 (50 − 20 = 30, then + 2).", "50 − 18 = 32 (50 − 20 = 30 ثم + 2).", "32."), F("32 + 18 = 50 ✓")]),
    _ex("9", "Find the missing number: 63 − ? = 28.", "جد العدد الناقص: 63 − ؟ = 28.", "Trouve : 63 − ? = 28.", [T("The whole is 63, one part 28. The other part: 63 − 28 = 35. Check: 63 − 35 = 28 ✓.", "الكل 63 وأحد الجزأين 28. الجزء الآخر 63 − 28 = 35. تحقق: 63 − 35 = 28 ✓.", "35."), F("63 − 35 = 28")]),
    _ex("10", "Ali has 35 stickers, 8 more than Sara. How many has Sara?", "عند علي 35 ملصقًا أي 8 أكثر من سارة. كم عند سارة؟", "Ali a 35 autocollants, 8 de plus que Sara. Combien Sara ?", [T("Sara has less. 35 − 8 = 27. Check 27 + 8 = 35 ✓.", "عند سارة أقل. 35 − 8 = 27. تحقق 27 + 8 = 35 ✓.", "27."), F("27")]),
    _ex("11", "A shop had 120 notebooks, sold 45 on Monday and 30 on Tuesday. How many are left?", "في متجر 120 دفترًا باع 45 يوم الاثنين و30 يوم الثلاثاء. كم بقي؟", "120 cahiers, 45 puis 30 vendus. Combien reste-t-il ?", [T("Take away both: 120 − 45 = 75; then 75 − 30 = 45. Or add sold first: 45 + 30 = 75, and 120 − 75 = 45. Same answer.", "نطرح الاثنين: 120 − 45 = 75 ثم 75 − 30 = 45. أو نجمع المبيع 45 + 30 = 75 ثم 120 − 75 = 45. الجواب نفسه.", "45."), hops(120, [-45, -30], tag="X7"), F("120 − 45 − 30 = 45      check: 45 + 75 = 120 ✓")]),
    _ex("12", "Error detective: 'Hana did 82 − 45 and got 43.' Check with the inverse.", "المحقق: «حسبت هناء 82 − 45 فوجدت 43». تحقق بالعملية العكسية.", "Détective : 82 − 45 = 43 ?", [T("Inverse: 43 + 45 = 88, not 82. So it is wrong. Correct: 82 − 45 = 37, and 37 + 45 = 82 ✓. Hana subtracted the smaller digit from the bigger in the ones place (5 − 2) instead of borrowing.", "العكسي: 43 + 45 = 88 لا 82 فالجواب خاطئ. الصحيح: 82 − 45 = 37 و37 + 45 = 82 ✓. طرحت هناء الرقم الأصغر من الأكبر في خانة الآحاد (5 − 2) بدل الاستلاف.", "Faux : 43 + 45 = 88. Juste : 37."), F("82 − 45 = 37")]),
]
