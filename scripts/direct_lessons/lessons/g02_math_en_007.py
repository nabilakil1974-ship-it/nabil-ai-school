"""Grade 2 Mathematics — Order of Numbers up to 69."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G02-MATH-EN-007"
GRADE = 2
SUBJECT = "math"
TITLES = {"en": "Order of Numbers up to 69", "ar": "ترتيب الأعداد حتى 69", "fr": "Ordre des nombres jusqu'à 69"}


def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}


QUIZ = [
    {"q": "Which is true?", "opts": ["59 > 47", "59 < 47", "59 = 47", "47 > 59"], "a": 0,
     "why": {"59 < 47": _w("59 has 5 tens and 47 has 4 tens, so 59 is greater.", "59 فيه 5 عشرات و47 فيه 4 عشرات فـ59 أكبر.", "59 a 5 dizaines, 47 en a 4."),
             "59 = 47": _w("They are different numbers.", "عددان مختلفان.", "Nombres différents."),
             "47 > 59": _w("Compare tens first: 4 tens < 5 tens.", "نقارن العشرات أولًا: 4 < 5.", "On compare d'abord les dizaines.")}, "ok": "59 > 47"},
    {"q": "Which number is right before 50?", "opts": ["49", "40", "51", "5"], "a": 0,
     "why": {"40": _w("Right before means one less: 50 − 1.", "قبله مباشرة يعني أقل بواحد: 50 − 1.", "Juste avant = 1 de moins."),
             "51": _w("51 comes after 50.", "51 يأتي بعد 50.", "51 vient après."),
             "5": _w("5 is far from 50.", "5 بعيد عن 50.", "5 est loin de 50.")}, "ok": "49"},
    {"q": "Which is the correct order from smallest to greatest?", "opts": ["14, 23, 36, 37, 59", "59, 37, 36, 23, 14", "14, 36, 23, 37, 59", "23, 14, 36, 37, 59"], "a": 0,
     "why": {"59, 37, 36, 23, 14": _w("That goes from greatest to smallest.", "هذا من الأكبر إلى الأصغر.", "C'est du plus grand au plus petit."),
             "14, 36, 23, 37, 59": _w("23 has 2 tens, so it comes before 36.", "23 قبل 36.", "23 vient avant 36."),
             "23, 14, 36, 37, 59": _w("14 has only 1 ten, so it is first.", "14 أولًا.", "14 d'abord.")}, "ok": "14 < 23 < 36 < 37 < 59"},
]

THEORY = [
    ("Compare tens first", "نقارن العشرات أولًا", "On compare d'abord les dizaines", "24", [
        T("Hello, champion! Today we learn to order numbers up to 69. The smart rule: compare the tens first. If the tens are the same, compare the ones. 34 and 36 both have 3 tens; ones: 4 < 6, so 34 < 36. For 59 and 47: 5 tens > 4 tens, so 59 > 47.",
          "مرحبًا يا بطل! اليوم نتعلم ترتيب الأعداد حتى 69. القاعدة الذكية: نقارن العشرات أولًا. وإذا تساوت العشرات نقارن الآحاد. 34 و36 كلاهما 3 عشرات؛ الآحاد: 4 < 6 إذن 34 < 36. أما 59 و47: 5 عشرات > 4 عشرات إذن 59 > 47.",
          "Bonjour champion ! Aujourd'hui, ranger les nombres jusqu'à 69. Règle : on compare d'abord les dizaines ; si elles sont égales, les unités. 34 et 36 : 3 dizaines chacun, 4 < 6 donc 34 < 36. 59 et 47 : 5 dizaines > 4 dizaines donc 59 > 47."),
        F("34 < 36      59 > 47"),
        F("TENS FIRST → ONES IF NEEDED"),
    ]),
    ("Smallest and greatest", "الأصغر والأكبر", "Le plus petit et le plus grand", "24", [
        T("The smallest number has fewer tens, or fewer ones when the tens match. Between 52 and 42 the smaller is 42. Between 39 and 36 the smaller is 36. The greatest has more tens, or more ones when tens match: between 63 and 60 it is 63; between 45 and 55 it is 55.",
          "العدد الأصغر عشراته أقل، أو آحاده أقل إذا تساوت العشرات. بين 52 و42 الأصغر 42. بين 39 و36 الأصغر 36. والأكبر عشراته أكثر أو آحاده أكثر عند تساوي العشرات: بين 63 و60 هو 63؛ بين 45 و55 هو 55.",
          "Le plus petit a moins de dizaines, ou moins d'unités si les dizaines sont égales : entre 52 et 42, c'est 42 ; entre 39 et 36, c'est 36. Le plus grand : entre 63 et 60, c'est 63 ; entre 45 et 55, c'est 55."),
        F("smallest: 42, 36      greatest: 63, 55"),
    ]),
    ("Signs > and <", "إشارتا > و<", "Les signes > et <", "25", [
        T("We do not start from the sign. First decide which number is greater, then write the symbol. 19 < 49 because 1 ten < 4 tens. 24 > 21 because the tens match and 4 > 1. 26 < 62 because 2 tens < 6 tens.",
          "لا نبدأ من الإشارة. أولًا نقرر أي عدد أكبر ثم نكتب الرمز. 19 < 49 لأن عشرة واحدة < 4 عشرات. 24 > 21 لأن العشرات متساوية و4 > 1. 26 < 62 لأن عشرتين < 6 عشرات.",
          "On ne commence pas par le signe : on décide d'abord quel nombre est le plus grand. 19 < 49 ; 24 > 21 ; 26 < 62."),
        F("19 < 49      24 > 21      26 < 62"),
    ]),
    ("Before, after, between", "قبل وبعد وبين", "Avant, après, entre", "25", [
        T("Right before is one less. Right after is one more. Around 19: 18, 19, 20. The number between 25 and 27 is 26. Careful: right before 50 is 49, and between 59 and 61 is 60.",
          "قبله مباشرة أقل بواحد وبعده مباشرة أكثر بواحد. حول 19: 18 و19 و20. العدد بين 25 و27 هو 26. انتبه: قبل 50 مباشرة 49 وبين 59 و61 العدد 60.",
          "Juste avant : 1 de moins ; juste après : 1 de plus. Autour de 19 : 18, 19, 20. Entre 25 et 27 : 26. Juste avant 50 : 49 ; entre 59 et 61 : 60."),
        F("18, 19, 20      25, 26, 27      49, 50, 51"),
    ]),
    ("Riddles and ordering", "ألغاز وترتيب", "Devinettes et rangement", "25", [
        T("A riddle needs all the clues together. The ones digit is 8 and the number is more than 45 and less than 55. Numbers ending in 8: 8, 18, 28, 38, 48, 58. More than 45 leaves 48 and 58. Less than 55 leaves 48.",
          "اللغز يحتاج كل الدلائل معًا. رقم الآحاد 8 والعدد أكبر من 45 وأصغر من 55. الأعداد المنتهية بـ8: 8، 18، 28، 38، 48، 58. الأكبر من 45 يبقي 48 و58. والأصغر من 55 يبقي 48.",
          "Une devinette demande tous les indices. Unités 8, plus de 45, moins de 55. Nombres finissant par 8 : 8, 18, 28, 38, 48, 58. Plus de 45 : 48 et 58. Moins de 55 : 48."),
        F("answer: 48"),
        T("To order 37, 14, 59, 23, 36: 14 has 1 ten, 23 has 2, 36 and 37 have 3, 59 has 5. For 36 and 37 compare ones: 6 < 7.",
          "لترتيب 37 و14 و59 و23 و36: 14 فيه عشرة و23 عشرتان و36 و37 ثلاث عشرات و59 خمس. وبين 36 و37 نقارن الآحاد: 6 < 7.",
          "Pour ranger 37, 14, 59, 23, 36 : 14 (1 dizaine), 23 (2), 36 et 37 (3), 59 (5). Entre 36 et 37 : 6 < 7."),
        F("14 < 23 < 36 < 37 < 59"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Tens first, ones if needed, then choose < or >. We also learned right before, right after, between, open inequalities with many answers, riddles and ordering several numbers.",
          "العشرات أولًا ثم الآحاد عند الحاجة ثم نختار < أو >. وتعلمنا أيضًا قبل وبعد وبين والمتباينات المفتوحة ذات الإجابات الكثيرة والألغاز وترتيب عدة أعداد.",
          "Dizaines d'abord, unités si besoin, puis < ou >. Nous avons aussi vu avant, après, entre, les inégalités ouvertes, les devinettes et le rangement."),
    ]),
]

EXERCISES = [
    EX("1", "24", st("Write each number, then use > or <: 4 tens 1 one and 4 tens 8 ones; 4 tens 2 ones and 5 tens; 5 tens 1 one and 3 tens 3 ones; 4 tens 8 ones and 2 tens 8 ones.",
                    "اكتب كل عدد ثم استعمل > أو <: 4 عشرات وواحد و4 عشرات و8 آحاد؛ 4 عشرات وواحدان و5 عشرات؛ 5 عشرات وواحد و3 عشرات و3 آحاد؛ 4 عشرات و8 آحاد وعشرتان و8 آحاد.",
                    "Écris les nombres puis > ou < : 4d 1u et 4d 8u ; 4d 2u et 5d ; 5d 1u et 3d 3u ; 4d 8u et 2d 8u."), [
        F("41 < 48      42 < 50      51 > 33      48 > 28"),
    ]),
    EX("2", "24", st("Circle the smallest number: 39 and 36; 42 and 48; 52 and 42; 63 and 23; 25 and 46; 48 and 39.",
                    "ضع دائرة حول العدد الأصغر: 39 و36؛ 42 و48؛ 52 و42؛ 63 و23؛ 25 و46؛ 48 و39.",
                    "Entoure le plus petit : 39 et 36 ; 42 et 48 ; 52 et 42 ; 63 et 23 ; 25 et 46 ; 48 et 39."), [
        F("36   42   42   23   25   39"),
    ]),
    EX("3", "24", st("Circle the greatest number: 41 and 49; 63 and 60; 45 and 55; 69 and 36; 41 and 64; 65 and 56.",
                    "ضع دائرة حول العدد الأكبر: 41 و49؛ 63 و60؛ 45 و55؛ 69 و36؛ 41 و64؛ 65 و56.",
                    "Entoure le plus grand : 41 et 49 ; 63 et 60 ; 45 et 55 ; 69 et 36 ; 41 et 64 ; 65 et 56."), [
        F("49   63   55   69   64   65"),
    ]),
    EX("4", "25", st("Complete with > or <: 19 _ 49; 24 _ 21; 37 _ 29; 26 _ 62; 43 _ 36; 51 _ 45; 33 _ 49; 59 _ 42; 47 _ 39.",
                    "أكمل بـ > أو <: 19 _ 49؛ 24 _ 21؛ 37 _ 29؛ 26 _ 62؛ 43 _ 36؛ 51 _ 45؛ 33 _ 49؛ 59 _ 42؛ 47 _ 39.",
                    "Complète avec > ou < : 19 _ 49 ; 24 _ 21 ; 37 _ 29 ; 26 _ 62 ; 43 _ 36 ; 51 _ 45 ; 33 _ 49 ; 59 _ 42 ; 47 _ 39."), [
        F("19 < 49   24 > 21   37 > 29   26 < 62   43 > 36"),
        F("51 > 45   33 < 49   59 > 42   47 > 39"),
    ]),
    EX("5", "25", st("Write the number between: 25 _ 27; 39 _ 41; 41 _ 43; 55 _ 57; 59 _ 61; 63 _ 65. Then the number before and after each middle number: 19, 27, 50, 47, 58, 62.",
                    "اكتب العدد الذي بينهما: 25 _ 27؛ 39 _ 41؛ 41 _ 43؛ 55 _ 57؛ 59 _ 61؛ 63 _ 65. ثم العدد قبل كل عدد وبعده: 19، 27، 50، 47، 58، 62.",
                    "Écris le nombre entre : 25 _ 27 ; 39 _ 41 ; 41 _ 43 ; 55 _ 57 ; 59 _ 61 ; 63 _ 65. Puis avant et après : 19, 27, 50, 47, 58, 62."), [
        F("26   40   42   56   60   64"),
        F("18, 19, 20   26, 27, 28   49, 50, 51   46, 47, 48   57, 58, 59   61, 62, 63"),
    ]),
]
