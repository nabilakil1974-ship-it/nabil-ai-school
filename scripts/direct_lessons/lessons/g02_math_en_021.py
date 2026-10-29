"""Grade 2 Mathematics — Adding or subtracting ones and tens."""
from scripts.direct_lessons.common import T, F, EX, st, tens

LESSON_ID = "G02-MATH-EN-021"
GRADE = 2
SUBJECT = "math"
TITLES = {"en": "Adding or Subtracting Ones and Tens", "ar": "جمع أو طرح الآحاد والعشرات", "fr": "Ajouter ou soustraire des unités et des dizaines"}


def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}


QUIZ = [
    {"q": "42 + 20 = ?",
     "opts": ["62", "44", "40", "22"], "a": 0,
     "why": {"44": _w("20 is two tens, so the tens change, not the ones.", "20 هي عشرتان فتتغير العشرات لا الآحاد.", "20 = deux dizaines : ce sont les dizaines qui changent."),
             "40": _w("We add 20, we do not take 2 away.", "نجمع 20 ولا نطرح 2.", "On ajoute 20, on n'enlève pas 2."),
             "22": _w("That subtracts 20.", "هذا يطرح 20.", "Cela soustrait 20.")},
     "ok": "42 + 20 = 62"},
    {"q": "58 + 2 = ?",
     "opts": ["60", "50", "580", "56"], "a": 0,
     "why": {"50": _w("8 ones and 2 ones make 10 ones, a new ten.", "8 آحاد و2 آحاد تصنع 10 آحاد أي عشرة جديدة.", "8 unités + 2 unités = 10 unités, une nouvelle dizaine."),
             "580": _w("We are adding 2 ones, not writing 2 next to 58.", "نجمع 2 آحاد ولا نكتب 2 بجانب 58.", "On ajoute 2 unités, on n'écrit pas 2 à côté."),
             "56": _w("That subtracts 2.", "هذا يطرح 2.", "Cela soustrait 2.")},
     "ok": "58 + 2 = 60"},
    {"q": "63 − 40 = ?",
     "opts": ["23", "59", "103", "3"], "a": 0,
     "why": {"59": _w("40 is four tens, so the tens go down by 4.", "40 هي أربع عشرات فتنقص العشرات 4.", "40 = quatre dizaines : les dizaines baissent de 4."),
             "103": _w("We subtract, we do not add.", "نطرح ولا نجمع.", "On soustrait, on n'additionne pas."),
             "3": _w("The 3 ones stay. Only the tens change: 6 tens − 4 tens = 2 tens.", "الآحاد الثلاثة تبقى. تتغير العشرات فقط: 6 عشرات − 4 عشرات = عشرتان.", "Les 3 unités restent. 6 dizaines − 4 dizaines = 2 dizaines.")},
     "ok": "63 − 40 = 23"},
]

THEORY = [
    ("Ones or tens?", "آحاد أم عشرات؟", "Unités ou dizaines ?", "48", [
        T("Hello, champion! Before we calculate, we ask: am I changing ones or tens? 45 + 3: we add 3 ones, so the ones change and 45 + 3 = 48. 45 − 3 = 42, we take away 3 ones. But if we add 20, we add 2 tens: 46 + 20 = 66.",
          "مرحبًا يا بطل! قبل أن نحسب نسأل: هل أغيّر الآحاد أم العشرات؟ 45 + 3: نضيف 3 آحاد فتتغير الآحاد و45 + 3 = 48. و45 − 3 = 42 نأخذ 3 آحاد. أما إذا أضفنا 20 فنضيف عشرتين: 46 + 20 = 66.",
          "Bonjour, champion ! Avant de calculer, on demande : je change les unités ou les dizaines ? 45 + 3 : j'ajoute 3 unités, donc 45 + 3 = 48. 45 − 3 = 42. Mais si j'ajoute 20, j'ajoute 2 dizaines : 46 + 20 = 66."),
        tens(4, 5, eq=True),
        F("45 + 3 = 48      45 − 3 = 42      46 + 20 = 66"),
    ]),
    ("Ones that make a new ten", "آحاد تصنع عشرة جديدة", "Des unités qui font une dizaine", "48", [
        T("Sometimes the ones reach 10. Then a new ten forms. 27 + 3: 7 ones and 3 ones make 10 ones, which is one more ten. So 27 + 3 = 30. In the same way 58 + 2 = 60 and 46 + 4 = 50.",
          "أحيانًا تصل الآحاد إلى 10. فتتكوّن عشرة جديدة. 27 + 3: 7 آحاد و3 آحاد تصنع 10 آحاد أي عشرة إضافية. إذن 27 + 3 = 30. وكذلك 58 + 2 = 60 و46 + 4 = 50.",
          "Parfois les unités atteignent 10 : une nouvelle dizaine se forme. 27 + 3 : 7 unités + 3 unités = 10 unités, donc une dizaine de plus : 27 + 3 = 30. De même 58 + 2 = 60 et 46 + 4 = 50."),
        F("27 + 3 = 30      58 + 2 = 60      46 + 4 = 50"),
    ]),
    ("Whole tens", "العشرات الكاملة", "Les dizaines entières", "48", [
        T("When we add or subtract 10, 20, 30, we only move the tens digit. The ones stay the same. 85 − 40: 8 tens − 4 tens = 4 tens, and the 5 ones stay. So 85 − 40 = 45. And 38 + 30 = 68. Careful: 62 − 30 is 32, not 59.",
          "عندما نجمع أو نطرح 10 أو 20 أو 30 فإننا نغيّر رقم العشرات فقط والآحاد تبقى. 85 − 40: 8 عشرات − 4 عشرات = 4 عشرات والآحاد الخمسة تبقى. إذن 85 − 40 = 45. و38 + 30 = 68. انتبه: 62 − 30 = 32 وليس 59.",
          "Quand on ajoute ou retire 10, 20, 30, seul le chiffre des dizaines change. Les unités restent. 85 − 40 : 8 dizaines − 4 dizaines = 4 dizaines, et les 5 unités restent : 45. Et 38 + 30 = 68. Attention : 62 − 30 = 32, pas 59."),
        F("85 − 40 = 45      38 + 30 = 68      62 − 30 = 32"),
    ]),
    ("Houses and chains", "البيوت والسلاسل", "Maisons et chaînes", "49", [
        T("An operator house applies the same change to every row. In the house +6: 24 becomes 30, 62 becomes 68, 42 becomes 48, 70 becomes 76. A chain is different: each step uses the result of the step before. Start at 47: +20 gives 67, then −7 gives 60, then −10 gives 50, then +8 gives 58, then −3 gives 55.",
          "بيت العملية يطبّق التغيير نفسه على كل صف. في البيت +6: 24 تصبح 30 و62 تصبح 68 و42 تصبح 48 و70 تصبح 76. أما السلسلة فمختلفة: كل خطوة تستعمل نتيجة الخطوة السابقة. نبدأ من 47: +20 تعطي 67 ثم −7 تعطي 60 ثم −10 تعطي 50 ثم +8 تعطي 58 ثم −3 تعطي 55.",
          "Une maison d'opérateur applique le même changement à chaque ligne. Maison +6 : 24 donne 30, 62 donne 68, 42 donne 48, 70 donne 76. Dans une chaîne, chaque pas utilise le résultat du pas précédent. Départ 47 : +20 → 67, −7 → 60, −10 → 50, +8 → 58, −3 → 55."),
        F("47 → 67 → 60 → 50 → 58 → 55"),
    ]),
    ("A sum puzzle", "لغز المجموع", "Un puzzle de sommes", "49", [
        T("In the sum grid every line must add up to 18. The fixed numbers are 3, 6, 2 and 4. Middle row: ? + 6 + 2 = 18, so 10. Middle column: ? + 6 + 4 = 18, so 8. Left column: 3 + 10 + ? = 18, so 5. Top row: 3 + 8 + ? = 18, so 7. Bottom row: 5 + 4 + ? = 18, so 9. Check every row and column: they all give 18.",
          "في شبكة المجموع يجب أن يكون مجموع كل خط 18. الأعداد الثابتة 3 و6 و2 و4. الصف الأوسط: ؟ + 6 + 2 = 18 إذن 10. العمود الأوسط: ؟ + 6 + 4 = 18 إذن 8. العمود الأيسر: 3 + 10 + ؟ = 18 إذن 5. الصف الأعلى: 3 + 8 + ؟ = 18 إذن 7. الصف الأسفل: 5 + 4 + ؟ = 18 إذن 9. نتحقق من كل صف وعمود فنجد 18.",
          "Dans la grille, chaque ligne doit faire 18. Les nombres fixes : 3, 6, 2 et 4. Ligne du milieu : ? + 6 + 2 = 18, donc 10. Colonne du milieu : ? + 6 + 4 = 18, donc 8. Colonne de gauche : 3 + 10 + ? = 18, donc 5. Ligne du haut : 3 + 8 + ? = 18, donc 7. Ligne du bas : 5 + 4 + ? = 18, donc 9."),
        F("3 8 7  |  10 6 2  |  5 4 9      each line = 18"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("+3 means 3 ones, +30 means 3 tens. Find which place changes, apply the change, read the new number and check. Best habit: say the place out loud.",
          "+3 تعني 3 آحاد و+30 تعني 3 عشرات. نحدد أي مرتبة تتغير ونطبّق التغيير ونقرأ العدد الجديد ونتحقق. أفضل عادة: نقول اسم المرتبة بصوت عالٍ.",
          "+3 veut dire 3 unités, +30 veut dire 3 dizaines. On trouve quelle place change, on applique, on lit le nouveau nombre et on vérifie. Bonne habitude : dire la place à voix haute."),
        F("WHAT PLACE CHANGES? → APPLY → READ THE NEW NUMBER → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "48", st("Calculate: 35 + 5, 42 + 20, 39 − 3, 62 − 30.",
                     "احسب: 35 + 5، 42 + 20، 39 − 3، 62 − 30.",
                     "Calcule : 35 + 5, 42 + 20, 39 − 3, 62 − 30."), [
        F("35 + 5 = 40      42 + 20 = 62      39 − 3 = 36      62 − 30 = 32"),
    ]),
    EX("2", "48", st("Calculate with ones: 20+5, 56+3, 72+6, 54+5, 48−6, 79−3, 85−4, 68−5, 27+3, 46+4, 58+2, 65+5.",
                     "احسب مع الآحاد: 20+5، 56+3، 72+6، 54+5، 48−6، 79−3، 85−4، 68−5، 27+3، 46+4، 58+2، 65+5.",
                     "Calcule avec les unités : 20+5, 56+3, 72+6, 54+5, 48−6, 79−3, 85−4, 68−5, 27+3, 46+4, 58+2, 65+5."), [
        F("25   59   78   59   42   76"),
        F("81   63   30   50   60   70"),
    ]),
    EX("3", "48", st("Calculate with tens: 69+10, 46+20, 38+30, 63−20, 85−40, 72−50, 20+30, 40+10, 60−10.",
                     "احسب مع العشرات: 69+10، 46+20، 38+30، 63−20، 85−40، 72−50، 20+30، 40+10، 60−10.",
                     "Calcule avec les dizaines : 69+10, 46+20, 38+30, 63−20, 85−40, 72−50, 20+30, 40+10, 60−10."), [
        F("79   66   68   43   45   22"),
        F("50   50   50"),
    ]),
    EX("4", "49", st("Choose + or − to make the equation true: 30 _ 20 = 50, 25 _ 3 = 22, 58 _ 10 = 48, 50 _ 20 = 30, 74 _ 5 = 79, 65 _ 4 = 69, 65 _ 4 = 61.",
                     "اختر + أو − لتصح المعادلة: 30 _ 20 = 50، 25 _ 3 = 22، 58 _ 10 = 48، 50 _ 20 = 30، 74 _ 5 = 79، 65 _ 4 = 69، 65 _ 4 = 61.",
                     "Choisis + ou − pour que l'égalité soit vraie : 30 _ 20 = 50, 25 _ 3 = 22, 58 _ 10 = 48, 50 _ 20 = 30, 74 _ 5 = 79, 65 _ 4 = 69, 65 _ 4 = 61."), [
        F("30 + 20 = 50      25 − 3 = 22      58 − 10 = 48      50 − 20 = 30"),
        F("74 + 5 = 79      65 + 4 = 69      65 − 4 = 61"),
        T("If the answer is bigger than the first number we add. If it is smaller we subtract.",
          "إذا كان الجواب أكبر من العدد الأول نجمع وإذا كان أصغر نطرح.",
          "Si le résultat est plus grand que le premier nombre, on additionne ; s'il est plus petit, on soustrait."),
    ]),
    EX("5", "49", st("Complete with the right number: 46 + _ = 86, 58 + _ = 78, 73 + _ = 79, 57 − _ = 27, 89 − _ = 80, 78 − _ = 38, 46 − _ = 6, 63 − _ = 23, 82 − _ = 32.",
                     "أكمل بالعدد المناسب: 46 + _ = 86، 58 + _ = 78، 73 + _ = 79، 57 − _ = 27، 89 − _ = 80، 78 − _ = 38، 46 − _ = 6، 63 − _ = 23، 82 − _ = 32.",
                     "Complète avec le bon nombre : 46 + _ = 86, 58 + _ = 78, 73 + _ = 79, 57 − _ = 27, 89 − _ = 80, 78 − _ = 38, 46 − _ = 6, 63 − _ = 23, 82 − _ = 32."), [
        F("46 + 40 = 86      58 + 20 = 78      73 + 6 = 79"),
        F("57 − 30 = 27      89 − 9 = 80      78 − 40 = 38"),
        F("46 − 40 = 6      63 − 40 = 23      82 − 50 = 32"),
    ]),
    EX("6", "49", st("Operator houses. House +6: 24, 62, 42, 70. House −5: 47, 36, 59, 78.",
                     "بيوت العمليات. بيت +6: 24، 62، 42، 70. بيت −5: 47، 36، 59، 78.",
                     "Maisons d'opérateur. Maison +6 : 24, 62, 42, 70. Maison −5 : 47, 36, 59, 78."), [
        F("+6:   24 → 30   62 → 68   42 → 48   70 → 76"),
        F("−5:   47 → 42   36 → 31   59 → 54   78 → 73"),
        T("The pairs 26 → 36, 56 → 66, 71 → 81, 54 → 64 all follow +10.",
          "الأزواج 26 ← 36 و56 ← 66 و71 ← 81 و54 ← 64 كلها تتبع +10.",
          "Les couples 26 → 36, 56 → 66, 71 → 81, 54 → 64 suivent tous +10."),
    ]),
    EX("7", "49", st("Arrow chain: start at 47, then +20, −7, −10, +8, −3.",
                     "سلسلة الأسهم: نبدأ من 47 ثم +20 ثم −7 ثم −10 ثم +8 ثم −3.",
                     "Chaîne de flèches : départ 47, puis +20, −7, −10, +8, −3."), [
        F("47 + 20 = 67      67 − 7 = 60      60 − 10 = 50"),
        F("50 + 8 = 58      58 − 3 = 55"),
        T("Each step starts from the result of the step before.", "كل خطوة تبدأ من نتيجة الخطوة السابقة.", "Chaque pas part du résultat du pas précédent."),
    ]),
    EX("8", "", st("(our own) Chain: start at 52, then +20, −2, +10, −5.",
                   "(من عندنا) سلسلة: نبدأ من 52 ثم +20 ثم −2 ثم +10 ثم −5.",
                   "(notre exemple) Chaîne : départ 52, puis +20, −2, +10, −5."), [
        F("52 + 20 = 72      72 − 2 = 70      70 + 10 = 80      80 − 5 = 75"),
    ]),
]
