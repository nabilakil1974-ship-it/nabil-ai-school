"""Grade 3 Mathematics — Numbers up to 99 (built from the extracted book exercises)."""
from scripts.direct_lessons.common import T, F, EX, st, tens

LESSON_ID = "G03-MATH-EN-001"
GRADE = 3
SUBJECT = "math"
TITLES = {"en": "Numbers Up to 99", "ar": "الأعداد حتى 99", "fr": "Les nombres jusqu'à 99"}

THEORY = [
    ("Tens and ones", "العشرات والآحاد", "Dizaines et unités", "13", [
        T("Hello, champion! Every number up to 99 is made of tens and ones. 5 tens and 7 ones make 57.",
          "مرحبًا يا بطل! كل عدد حتى 99 يتكوّن من عشرات وآحاد. 5 عشرات و7 آحاد تُكوّن 57.",
          "Tout nombre jusqu'à 99 a des dizaines et des unités : 5 dizaines et 7 unités font 57."),
        tens(5, 7, "A", eq=True),
        F("5 tens + 7 ones = 57"),
    ]),
    ("Words and digits", "الكلمات والأرقام", "Mots et chiffres", "13", [
        T("We write a number in words by writing the tens part, then the ones part, joined by a hyphen: 27 = twenty-seven, 52 = fifty-two, 64 = sixty-four. We start with the big part, like in Arabic.",
          "نكتب العدد بالكلمات: أولًا جزء العشرات ثم جزء الآحاد بينهما شرطة: 27 twenty-seven و52 fifty-two و64 sixty-four. نبدأ بالجزء الكبير.",
          "On écrit d'abord les dizaines puis les unités : 27 twenty-seven, 52 fifty-two, 64 sixty-four."),
        F("64 = 60 + 4 = sixty-four"),
    ]),
    ("Decomposing a number", "تحليل العدد", "Décomposer un nombre", "13", [
        T("A number can be written as a sum in many ways: 29 = 10 + 10 + 9, and 73 = 60 + 13.",
          "يمكن كتابة العدد مجموعًا بطرق كثيرة: 29 = 10 + 10 + 9 و73 = 60 + 13.",
          "Un nombre s'écrit en somme de plusieurs façons : 29 = 10 + 10 + 9 ; 73 = 60 + 13."),
        F("29 = 10 + 10 + 9      73 = 60 + 13"),
    ]),
    ("Comparing", "المقارنة", "Comparer", "14", [
        T("To compare, first compute each side, then look at the tens. 57 < 75 because 5 tens is less than 7 tens. 80 + 8 = 88 and 90 + 8 = 98, so 88 < 98.",
          "للمقارنة نحسب كل طرف أولًا ثم ننظر إلى العشرات. 57 < 75 لأن 5 عشرات أقل من 7 عشرات. 80 + 8 = 88 و90 + 8 = 98 إذن 88 < 98.",
          "On calcule chaque côté puis on regarde les dizaines : 57 < 75 ; 88 < 98."),
        F("57 < 75      80 + 8 < 90 + 8"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Tens and ones build every number up to 99. We can write it in digits, in words, or as a sum, and we compare tens first.",
          "العشرات والآحاد تبني كل عدد حتى 99. نكتبه بالأرقام أو الكلمات أو مجموعًا، ونقارن العشرات أولًا.",
          "Dizaines et unités construisent les nombres ; on compare d'abord les dizaines."),
    ]),
]

EXERCISES = [
    EX("1", "13", st("Complete: 5 tens 7 ones; 3 tens 5 ones; ? tens 7 ones = 67; 9 tens ? ones = 92; ? tens ? ones = 82; = 28.", "أكمل: 5 عشرات و7 آحاد؛ 3 عشرات و5 آحاد؛ … عشرات و7 آحاد = 67؛ 9 عشرات و… آحاد = 92؛ 82؛ 28.", "Complète : 5d 7u ; 3d 5u ; ?d 7u = 67 ; 9d ?u = 92 ; 82 ; 28."), [
        F("57   35   6 tens   2 ones   8 tens 2 ones   2 tens 8 ones"),
    ]),
    EX("2", "13", st("Complete with the appropriate number.", "أكمل بالعدد المناسب.", "Complète avec le nombre qui convient."), [
        F("80 + 5 = 85    60 + 12 = 72    50 + 9 = 59"),
        F("80 + 15 = 95    52 + 12 = 64    10 + 60 = 70"),
        F("10+10+10+10+4 = 44    10+10+10+10+5 = 45"),
        T("For 10 + 10 + ? + ? = 50, for example 10 + 10 + 10 + 20 or 10 + 10 + 20 + 10.", "في 10 + 10 + … + … = 50 مثلًا 10 + 10 + 10 + 20.", "Par exemple 10 + 10 + 10 + 20 = 50."),
    ]),
    EX("3", "13", st("Write in words: 27, 52, 64, 40, 43, 80, 83, 95, 78.", "اكتب بالكلمات: 27، 52، 64، 40، 43، 80، 83، 95، 78.", "Écris en lettres : 27, 52, 64, 40, 43, 80, 83, 95, 78."), [
        F("twenty-seven · fifty-two · sixty-four · forty · forty-three"),
        F("eighty · eighty-three · ninety-five · seventy-eight"),
    ]),
    EX("4", "13", st("Write in digits.", "اكتب بالأرقام.", "Écris en chiffres."), [
        F("thirty-nine 39 · seventeen 17 · fifty-eight 58"),
        F("forty-seven 47 · sixty-five 65 · seventy-five 75"),
        F("eighty-three 83 · ninety-three 93 · seventy-nine 79"),
    ]),
    EX("5", "13", st("Decompose into a sum: 36, 43, 57, 18, 93, 81, 94.", "حلّل إلى مجموع: 36، 43، 57، 18، 93، 81، 94.", "Décompose en somme : 36, 43, 57, 18, 93, 81, 94."), [
        F("36 = 30 + 6    43 = 40 + 3    57 = 50 + 7    18 = 10 + 8"),
        F("93 = 90 + 3    81 = 80 + 1    94 = 90 + 4"),
        T("Other correct sums are accepted, such as 36 = 10 + 10 + 10 + 6.", "تُقبل مجاميع صحيحة أخرى مثل 36 = 10 + 10 + 10 + 6.", "D'autres sommes justes sont acceptées."),
    ]),
    EX("6", "14", st("Compare with <, > or =.", "قارن بـ <، > أو =.", "Compare avec <, > ou =."), [
        F("57 < 75      80 + 8 = 88 < 98 = 90 + 8"),
        F("64 + 4 = 68 > 46 = 40 + 6"),
        F("10 + 10 + 10 + 10 + 7 = 47 < 67"),
        F("10 + 10 + 10 + 50 = 80 < 82"),
    ]),
    EX("7", "14", st("Right before and right after a number.", "العدد الذي قبله مباشرة والذي بعده مباشرة.", "Juste avant et juste après."), [
        T("Right before means 1 less, right after means 1 more. Right before 49 is 48; right after 79 is 80.",
          "قبله مباشرة يعني أقل بواحد وبعده مباشرة يعني أكثر بواحد. قبل 49 هو 48 وبعد 79 هو 80.",
          "Juste avant : 1 de moins ; juste après : 1 de plus. Avant 49 : 48 ; après 79 : 80."),
    ]),
    EX("8", "14", st("Increasing order: numbers less than 100 with 4 as the ones digit.", "رتّب تصاعديًا الأعداد الأصغر من 100 التي رقم آحادها 4.", "Ordre croissant : nombres < 100 avec 4 aux unités."), [
        F("4, 14, 24, 34, 44, 54, 64, 74, 84, 94"),
    ]),
    EX("9", "14", st("Decreasing order: numbers less than 100 with 6 as the tens digit.", "رتّب تنازليًا الأعداد الأصغر من 100 التي رقم عشراتها 6.", "Ordre décroissant : nombres < 100 avec 6 aux dizaines."), [
        F("69, 68, 67, 66, 65, 64, 63, 62, 61, 60"),
    ]),
    EX("10", "14", st("Kamal has between 50 and 60 stamps; the ones digit is 6.", "عند كمال طوابع بين 50 و60 ورقم آحادها 6. كم طابعًا؟", "Kamal a entre 50 et 60 timbres, chiffre des unités 6."), [
        F("56"),
    ]),
    EX("11", "14", st("Place on the number line: 57, 69, 55, 74, 98, 81.", "ضع على خط الأعداد: 57، 69، 55، 74، 98، 81.", "Place sur la droite : 57, 69, 55, 74, 98, 81."), [
        T("Between 50 and 60: 55, 57. Between 60 and 70: 69. Between 70 and 80: 74. Between 80 and 90: 81. Between 90 and 100: 98.",
          "بين 50 و60: 55 و57. بين 60 و70: 69. بين 70 و80: 74. بين 80 و90: 81. بين 90 و100: 98.",
          "Entre 50 et 60 : 55, 57 ; 60-70 : 69 ; 70-80 : 74 ; 80-90 : 81 ; 90-100 : 98."),
    ]),
    EX("12", "14", st("Abou Saad has 4 cows and 8 tens of sheep; Abou Saber has eighty-nine heads. Who has more?", "عند أبي سعد 4 أبقار و8 عشرات من الغنم وعند أبي صابر تسعة وثمانون رأسًا. من عنده أكثر؟", "Abou Saad : 4 vaches et 8 dizaines de moutons ; Abou Saber : quatre-vingt-neuf. Qui en a le plus ?"), [
        F("4 + 80 = 84      84 < 89"),
        T("Abou Saber has more.", "أبو صابر عنده أكثر.", "Abou Saber en a plus."),
    ]),
    EX("13", "14", st("Use 60, 50, 40, 10, 1, 2 with + or − to write 53 in three ways.", "استعمل 60 و50 و40 و10 و1 و2 مع + أو − لكتابة 53 بثلاث طرق.", "Avec 60, 50, 40, 10, 1, 2 et + ou −, écris 53 de trois façons."), [
        F("50 + 1 + 2 = 53"),
        F("40 + 10 + 1 + 2 = 53"),
        F("60 − 10 + 1 + 2 = 53"),
    ]),
]
