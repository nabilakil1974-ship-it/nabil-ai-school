"""Grade 3 Mathematics — Numbers up to 999."""
from scripts.direct_lessons.common import T, F, EX, st, scene

LESSON_ID = "G03-MATH-EN-002"
GRADE = 3
SUBJECT = "math"
TITLES = {"en": "Numbers Up to 999", "ar": "الأعداد حتى 999", "fr": "Les nombres jusqu'à 999"}


def htoblocks(h, t, o, tag="H"):
    """h flats, t rods, o cubes (compact), with the numeral."""
    svg, ids = "", []
    for i in range(h):
        svg += f'<g id="{tag}h{i}"><rect x="{20+i*62}" y="40" width="54" height="54" fill="#bbdefb" stroke="#0b3d5c" stroke-width="3"/></g>'
        ids.append(f"{tag}h{i}")
    tx = 20 + h * 62 + 20
    for i in range(t):
        svg += f'<g id="{tag}t{i}"><rect x="{tx+i*20}" y="40" width="14" height="110" fill="#ffcc80" stroke="#0b3d5c" stroke-width="3"/></g>'
        ids.append(f"{tag}t{i}")
    ox = tx + t * 20 + 20
    for i in range(o):
        svg += f'<g id="{tag}o{i}"><rect x="{ox+(i%5)*22}" y="{40+(i//5)*24}" width="16" height="16" fill="#a5d6a7" stroke="#0b3d5c" stroke-width="3"/></g>'
        ids.append(f"{tag}o{i}")
    n = h * 100 + t * 10 + o
    svg += (f'<text id="{tag}n" x="330" y="300" font-size="100" font-weight="700" text-anchor="middle" fill="#e53935" font-family="sans-serif">{n}</text>'
            f'<text id="{tag}c" x="330" y="360" font-size="34" text-anchor="middle" fill="#0b3d5c" font-family="sans-serif">H {h}   T {t}   O {o}</text>')
    ids += [tag + "n", tag + "c"]
    return scene(svg, ids)


THEORY = [
    ("Ten tens make one hundred", "عشر عشرات تساوي مئة", "Dix dizaines font une centaine", "14", [
        T("Hello, champion! Yesterday tens helped us build numbers up to 99. Today ten tens join and become one hundred. 10 ones = 1 ten, 10 tens = 1 hundred, so 100 = 1 hundred + 0 tens + 0 ones. We read every three-digit number with three questions: how many hundreds, how many tens, how many ones?",
          "مرحبًا يا بطل! بالأمس بنينا الأعداد حتى 99 بالعشرات. اليوم عشر عشرات تتحد فتصبح مئة. 10 آحاد = عشرة و10 عشرات = مئة، إذن 100 = مئة + 0 عشرات + 0 آحاد. نقرأ كل عدد من ثلاث منازل بثلاثة أسئلة: كم مئة؟ كم عشرة؟ كم واحدًا؟",
          "Dix dizaines forment une centaine : 100 = 1 centaine + 0 dizaine + 0 unité. On lit un nombre à trois chiffres avec trois questions : combien de centaines, de dizaines, d'unités ?"),
        htoblocks(1, 0, 0),
    ]),
    ("Hundreds, tens, ones", "المئات والعشرات والآحاد", "Centaines, dizaines, unités", "14", [
        T("Build 347: 3 hundreds = 300, 4 tens = 40, 7 ones = 7. So 300 + 40 + 7 = 347. In the chart H | T | O we have 3 | 4 | 7. Start from the right: ones, tens, then hundreds.",
          "نبني 347: 3 مئات = 300 و4 عشرات = 40 و7 آحاد = 7، إذن 300 + 40 + 7 = 347. في جدول م | ع | آ نجد 3 | 4 | 7. نبدأ من اليمين: الآحاد ثم العشرات ثم المئات.",
          "347 : 3 centaines = 300, 4 dizaines = 40, 7 unités = 7 ; 300 + 40 + 7 = 347."),
        htoblocks(3, 4, 7),
        F("H | T | O  =  3 | 4 | 7"),
    ]),
    ("Build from place value", "نبني العدد من قيم المنازل", "Construire avec la valeur de position", "14", [
        T("6 hundreds, 2 tens and 9 ones: 600 + 20 + 9 = 629. Careful: 4 hundreds, 7 tens, 3 ones is 473, not 437. Do not mix the tens and the ones.",
          "6 مئات و2 عشرتان و9 آحاد: 600 + 20 + 9 = 629. انتبه: 4 مئات و7 عشرات و3 آحاد هو 473 لا 437. لا نخلط العشرات بالآحاد.",
          "6 centaines 2 dizaines 9 unités : 629. 4 c, 7 d, 3 u = 473, pas 437."),
        F("600 + 20 + 9 = 629      400 + 70 + 3 = 473"),
    ]),
    ("Decompose a number", "نحلّل العدد", "Décomposer", "14", [
        T("764 = 700 + 60 + 4. The digit 7 is worth 700, not 7. The digit 6 is worth 60. The digit 4 is worth 4.",
          "764 = 700 + 60 + 4. قيمة الرقم 7 هي 700 لا 7، وقيمة الرقم 6 هي 60، وقيمة 4 هي 4.",
          "764 = 700 + 60 + 4. Le 7 vaut 700, le 6 vaut 60."),
        htoblocks(7, 6, 4),
    ]),
    ("Zero holds the place", "الصفر يحفظ المنزلة", "Le zéro garde la place", "15", [
        T("405 means 4 hundreds, 0 tens, 5 ones: 400 + 0 + 5. It is not 45. The zero holds the tens place and keeps the 4 worth four hundreds. And 530 means 5 hundreds, 3 tens, 0 ones.",
          "405 تعني 4 مئات و0 عشرات و5 آحاد: 400 + 0 + 5. وليست 45. الصفر يحفظ منزلة العشرات ويُبقي قيمة 4 أربعمئة. و530 تعني 5 مئات و3 عشرات و0 آحاد.",
          "405 = 400 + 0 + 5, pas 45. 530 = 5 centaines, 3 dizaines, 0 unité."),
        htoblocks(4, 0, 5),
    ]),
    ("Compare three-digit numbers", "نقارن الأعداد من ثلاث منازل", "Comparer", "15", [
        T("Compare hundreds first. If tied, compare tens. If still tied, compare ones. 386 < 421 because 3 hundreds < 4 hundreds. 572 > 548: hundreds tie, 7 tens > 4 tens. 634 < 639: hundreds and tens tie, 4 < 9.",
          "نقارن المئات أولًا، فإن تساوت قارنا العشرات، فإن تساوت قارنا الآحاد. 386 < 421 لأن 3 مئات < 4 مئات. 572 > 548: المئات متساوية و7 عشرات > 4. 634 < 639: المئات والعشرات متساوية و4 < 9.",
          "On compare les centaines, puis les dizaines, puis les unités."),
        F("386 < 421      572 > 548      634 < 639"),
        T("Never say 619 > 702 because 19 > 2: compare the hundreds first, 6 < 7.", "لا نقول 619 > 702 لأن 19 > 2؛ نقارن المئات أولًا 6 < 7.", "619 < 702 : on compare d'abord les centaines."),
    ]),
    ("Order numbers", "نرتّب الأعداد", "Ranger", "15", [
        T("Order 315, 299, 351, 305 from least to greatest. 299 has 2 hundreds, so it is first. The others have 3 hundreds: compare tens, 0 < 1 < 5.",
          "رتّب 315 و299 و351 و305 من الأصغر. 299 فيه مئتان فهو الأول. والباقي 3 مئات فنقارن العشرات: 0 < 1 < 5.",
          "299 d'abord, puis on compare les dizaines des autres."),
        F("299 < 305 < 315 < 351"),
        F("H → T → O"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Every digit has a place and every place gives the digit its value. Read from hundreds to tens to ones, and compare in the same order. Zero protects an empty place. To check, rebuild: hundreds + tens + ones.",
          "لكل رقم منزلة ولكل منزلة قيمة. نقرأ من المئات إلى العشرات إلى الآحاد ونقارن بالترتيب نفسه. الصفر يحمي المنزلة الفارغة. وللتحقق نعيد البناء: مئات + عشرات + آحاد.",
          "Chaque chiffre a une place qui lui donne sa valeur ; on lit et compare de gauche à droite."),
        F("347 = 300 + 40 + 7      COMPARE: H → T → O"),
    ]),
]

EXERCISES = [
    EX("1", "14", st("In 582 find H, T and O.", "في 582 حدّد المئات والعشرات والآحاد.", "Dans 582 trouve c, d, u."), [F("5 hundreds, 8 tens, 2 ones      500 + 80 + 2 = 582")]),
    EX("2", "14", st("4 hundreds, 7 tens, 3 ones = ?", "4 مئات و7 عشرات و3 آحاد = ؟", "4 c, 7 d, 3 u = ?"), [F("473")]),
    EX("3", "14", st("Error detective: 4 hundreds 7 tens 3 ones written as 437.", "المحقق: كُتبت 4 مئات و7 عشرات و3 آحاد هكذا 437.", "Détective : 4c 7d 3u écrit 437."), [F("473"), T("The tens and ones were mixed.", "اختلطت العشرات بالآحاد.", "Dizaines et unités mélangées.")]),
    EX("4", "14", st("Decompose 291.", "حلّل 291.", "Décompose 291."), [F("291 = 200 + 90 + 1")]),
    EX("5", "15", st("What does 530 mean? A: 5H 3T 0O, B: 5H 0T 3O.", "ماذا تعني 530؟ أ: 5 مئات 3 عشرات 0 آحاد، ب: 5 مئات 0 عشرات 3 آحاد.", "Que veut dire 530 ?"), [F("A")]),
    EX("6", "15", st("Compare 708 and 780.", "قارن 708 و780.", "Compare 708 et 780."), [F("708 < 780"), T("Hundreds tie; 0 tens < 8 tens.", "المئات متساوية و0 عشرات < 8.", "Centaines égales ; 0 < 8 dizaines.")]),
    EX("7", "15", st("Error detective: \"619 > 702 because 19 > 2\".", "المحقق: «619 > 702 لأن 19 > 2».", "Détective : « 619 > 702 car 19 > 2 »."), [F("619 < 702"), T("6 hundreds < 7 hundreds.", "6 مئات < 7 مئات.", "6 centaines < 7 centaines.")]),
    EX("8", "15", st("Guided practice: 8H 4T 6O; decompose 527; value of 6 in 361; 498 vs 501; 742 vs 724; order 612, 216, 621, 602.", "تدريب: 8 مئات 4 عشرات 6 آحاد؛ حلّل 527؛ قيمة 6 في 361؛ 498 و501؛ 742 و724؛ رتّب 612 و216 و621 و602.", "Entraînement guidé."), [
        F("846      500 + 20 + 7      60"),
        F("498 < 501      742 > 724"),
        F("216 < 602 < 612 < 621"),
    ]),
    EX("9", "15", st("Write the numeral: 3H 5T 2O; 7H 0T 4O; 9H 9T 0O.", "اكتب العدد: 3 مئات 5 عشرات 2 آحاد؛ 7 مئات 0 عشرات 4 آحاد؛ 9 مئات 9 عشرات 0 آحاد.", "Écris le nombre."), [F("352      704      990")]),
    EX("10", "15", st("Decompose 418, 700, 965.", "حلّل 418 و700 و965.", "Décompose 418, 700, 965."), [F("400 + 10 + 8      700 + 0 + 0      900 + 60 + 5")]),
    EX("11", "15", st("Compare: 609 _ 690; 875 _ 857; 432 _ 432.", "قارن: 609 _ 690؛ 875 _ 857؛ 432 _ 432.", "Compare."), [F("609 < 690      875 > 857      432 = 432")]),
    EX("12", "15", st("Order: 510, 105, 501, 150.", "رتّب: 510 و105 و501 و150.", "Range : 510, 105, 501, 150."), [F("105 < 150 < 501 < 510")]),
    EX("13", "15", st("Explain why 802 > 799.", "اشرح لماذا 802 > 799.", "Explique pourquoi 802 > 799."), [T("802 has 8 hundreds while 799 has 7 hundreds.", "في 802 ثماني مئات وفي 799 سبع مئات.", "802 a 8 centaines, 799 en a 7.")]),
    EX("14", "15", st("Regroup: 12 tens = ? hundred and ? tens. Repair: 306 = 30 + 6.", "أعد التجميع: 12 عشرة = … مئة و… عشرات. صحّح: 306 = 30 + 6.", "Regroupe : 12 dizaines. Corrige : 306 = 30 + 6."), [
        F("12 tens = 1 hundred and 2 tens      306 = 300 + 0 + 6"),
    ]),
    EX("15", "", st("Final check: 638; 904; 590 vs 509; value of 7 in 274; order 321, 312, 231.", "تقييم: 638؛ حلّل 904؛ 590 و509؛ قيمة 7 في 274؛ رتّب 321 و312 و231.", "Évaluation finale."), [
        F("638      900 + 0 + 4      590 > 509      70      231 < 312 < 321"),
    ]),
]
