"""Grade 2 Mathematics — Numbers up to 69."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G02-MATH-EN-006"
GRADE = 2
SUBJECT = "math"
TITLES = {"en": "Numbers up to 69", "ar": "الأعداد حتى 69", "fr": "Les nombres jusqu'à 69"}


def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}


QUIZ = [
    {"q": "4 tens and 8 ones make which number?", "opts": ["48", "84", "12", "408"], "a": 0,
     "why": {"84": _w("That is 8 tens and 4 ones. Here 4 tens = 40, and 40 + 8 = 48.", "هذا 8 عشرات و4 آحاد. هنا 4 عشرات = 40 و40 + 8 = 48.", "C'est 8 dizaines et 4 unités. Ici 40 + 8 = 48."),
             "12": _w("We do not add the digits: 40 + 8 = 48.", "لا نجمع الرقمين: 40 + 8 = 48.", "On n'additionne pas les chiffres : 40 + 8 = 48."),
             "408": _w("40 + 8 = 48; a tens digit and a ones digit make two digits.", "40 + 8 = 48 عدد من رقمين.", "40 + 8 = 48.")}, "ok": "40 + 8 = 48"},
    {"q": "How do we write fifty in digits?", "opts": ["50", "15", "5", "500"], "a": 0,
     "why": {"15": _w("15 is fifteen. Fifty is 5 tens = 50.", "15 هو fifteen. أما fifty فهو 5 عشرات = 50.", "15 se dit fifteen. Fifty = 5 dizaines = 50."),
             "5": _w("Fifty is five tens, not five ones.", "fifty خمس عشرات لا خمسة آحاد.", "Fifty = cinq dizaines."),
             "500": _w("Too big: we only work up to 69.", "كبير جدًا: نعمل حتى 69.", "Trop grand.")}, "ok": "fifty = 50"},
    {"q": "50 + ? = 58. What is the missing number?", "opts": ["8", "5", "58", "108"], "a": 0,
     "why": {"5": _w("5 is the tens digit. We need the ones.", "5 رقم العشرات والمطلوب الآحاد.", "5 est le chiffre des dizaines."),
             "58": _w("58 is the total.", "58 هو المجموع.", "58 est le total."),
             "108": _w("Too big: 50 + 8 = 58.", "50 + 8 = 58.", "50 + 8 = 58.")}, "ok": "50 + 8 = 58"},
]

THEORY = [
    ("Tens digit and ones digit", "رقم العشرات ورقم الآحاد", "Chiffre des dizaines et des unités", "22", [
        T("Hello, champion! Today our numbers grow up to 69. We do not count every square from the start. We use tens and ones. 25 = 2 tens and 5 ones = twenty-five. 38 = 3 tens and 8 ones = thirty-eight. 52 = 5 tens and 2 ones = fifty-two.",
          "مرحبًا يا بطل! اليوم تكبر أعدادنا حتى 69. لا نعدّ كل مربع من البداية بل نستعمل العشرات والآحاد. 25 = عشرتان و5 آحاد = twenty-five. 38 = 3 عشرات و8 آحاد = thirty-eight. 52 = 5 عشرات وواحدان = fifty-two.",
          "Bonjour champion ! Aujourd'hui les nombres vont jusqu'à 69. On n'a pas besoin de compter chaque carré : on utilise dizaines et unités. 25 = 2 dizaines et 5 unités ; 38 = 3 dizaines et 8 unités ; 52 = 5 dizaines et 2 unités."),
        F("25 = 20 + 5      38 = 30 + 8      52 = 50 + 2"),
        T("The tens digit tells how many tens. The ones digit tells how many ones. 47 = 4 tens + 7 ones = 40 + 7. And 60 = 6 tens and 0 ones.",
          "رقم العشرات يخبرنا كم عشرة، ورقم الآحاد يخبرنا كم واحدًا. 47 = 4 عشرات + 7 آحاد = 40 + 7. و60 = 6 عشرات و0 آحاد.",
          "Le chiffre des dizaines dit combien de dizaines ; celui des unités, combien d'unités. 47 = 40 + 7. Et 60 = 6 dizaines et 0 unité."),
    ]),
    ("From words to digits", "من الكلمات إلى الأرقام", "Des mots aux chiffres", "23", [
        T("Be careful with the words. Fifty is 50, not 15. Sixty is 60, not 16. Fifteen is 15 and sixteen is 16. The ending -ty means tens.",
          "انتبه إلى الكلمات. fifty هو 50 وليس 15. sixty هو 60 وليس 16. أما fifteen فهو 15 وsixteen هو 16. النهاية -ty تعني عشرات.",
          "Attention aux mots. Fifty = 50, pas 15. Sixty = 60, pas 16. Fifteen = 15 et sixteen = 16. La fin -ty indique des dizaines."),
        F("sixteen 16   fifty 50   sixty 60   forty-nine 49   twenty-three 23"),
    ]),
    ("From digits to words", "من الأرقام إلى الكلمات", "Des chiffres aux mots", "23", [
        T("To write a number in words, say the tens part, then the ones part, joined by a hyphen. 35 is thirty-five. 61 is sixty-one. 52 is fifty-two. And 40 is just forty.",
          "لنكتب العدد بكلمات نقول جزء العشرات ثم جزء الآحاد بينهما شرطة. 35 هو thirty-five و61 هو sixty-one و52 هو fifty-two. أما 40 فهو forty فقط.",
          "Pour écrire en mots : la partie des dizaines puis celle des unités, avec un trait d'union. 35 : thirty-five ; 61 : sixty-one ; 52 : fifty-two ; 40 : forty."),
        F("35 thirty-five   19 nineteen   61 sixty-one   25 twenty-five   52 fifty-two   40 forty"),
    ]),
    ("One number, many forms", "عدد واحد بصور كثيرة", "Un nombre, plusieurs écritures", "23", [
        T("One number can be written in several equal ways. Take 37: it is 30 + 7, it is 3 tens and 7 ones, and it is thirty-seven. All of them show the same value.",
          "يمكن كتابة العدد الواحد بعدة طرق متساوية. خذ 37: هو 30 + 7 وهو 3 عشرات و7 آحاد وهو thirty-seven. كلها تدل على القيمة نفسها.",
          "Un même nombre s'écrit de plusieurs façons égales. Pour 37 : 30 + 7, 3 dizaines et 7 unités, thirty-seven. Même valeur."),
        F("37 = 30 + 7 = 3 tens and 7 ones = thirty-seven"),
        F("69 = 60 + 9 = 6 tens and 9 ones = sixty-nine"),
        T("When we colour by value, solve first, colour second. For example 24 + 2 = 26, so we use the colour for 26.",
          "عندما نلوّن حسب القيمة نحلّ أولًا ثم نلوّن. مثلًا 24 + 2 = 26 فنستعمل لون العدد 26.",
          "Pour colorier selon la valeur : calculer d'abord, colorier ensuite. 24 + 2 = 26, donc la couleur de 26."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Any number like 58 has 5 tens = 50 and 8 ones, so 50 + 8 = 58. We can write it as 58, fifty-eight, 5 tens and 8 ones, or 50 + 8. Read the tens, read the ones, build the number, then check the value.",
          "أي عدد مثل 58 فيه 5 عشرات = 50 و8 آحاد، إذن 50 + 8 = 58. نكتبه 58 أو fifty-eight أو 5 عشرات و8 آحاد أو 50 + 8. نقرأ العشرات ثم الآحاد ونبني العدد ثم نتحقق من القيمة.",
          "Un nombre comme 58 a 5 dizaines = 50 et 8 unités : 50 + 8 = 58. On l'écrit 58, fifty-eight, 5 dizaines et 8 unités, ou 50 + 8. On lit les dizaines, les unités, on construit, on vérifie."),
    ]),
]

EXERCISES = [
    EX("1", "22", st("Complete with the number: 3 tens 9 ones; 6 tens 2 ones; 4 tens 1 one; 2 tens 8 ones; 5 tens 4 ones; 1 ten 4 ones.",
                    "أكمل بالعدد: 3 عشرات و9 آحاد؛ 6 عشرات وواحدان؛ 4 عشرات وواحد؛ عشرتان و8 آحاد؛ 5 عشرات و4 آحاد؛ عشرة و4 آحاد.",
                    "Complète : 3 d 9 u ; 6 d 2 u ; 4 d 1 u ; 2 d 8 u ; 5 d 4 u ; 1 d 4 u."), [
        F("30 + 9 = 39      60 + 2 = 62      40 + 1 = 41"),
        F("20 + 8 = 28      50 + 4 = 54      10 + 4 = 14"),
    ]),
    EX("2", "23", st("Write in digits: sixteen, twenty-seven, fifty-five, sixty-eight, forty-one, fifty, forty-nine, sixty, twenty-three.",
                    "اكتب بالأرقام: sixteen وtwenty-seven وfifty-five وsixty-eight وforty-one وfifty وforty-nine وsixty وtwenty-three.",
                    "Écris en chiffres : sixteen, twenty-seven, fifty-five, sixty-eight, forty-one, fifty, forty-nine, sixty, twenty-three."), [
        F("16   27   55   68   41   50   49   60   23"),
        T("Remember: fifty is 50, not 15, and sixty is 60, not 16.", "تذكّر: fifty هو 50 لا 15 وsixty هو 60 لا 16.", "Souviens-toi : fifty = 50, sixty = 60."),
    ]),
    EX("3", "23", st("Write in words: 35, 19, 61, 25, 52, 40.",
                    "اكتب بالكلمات: 35، 19، 61، 25، 52، 40.",
                    "Écris en mots : 35, 19, 61, 25, 52, 40."), [
        F("thirty-five · nineteen · sixty-one · twenty-five · fifty-two · forty"),
    ]),
    EX("4", "23", st("Write the number in digits, then in words: 3 tens 1 one; 5 tens 6 ones; 6 tens 7 ones.",
                    "اكتب العدد بالأرقام ثم بالكلمات: 3 عشرات وواحد؛ 5 عشرات و6 آحاد؛ 6 عشرات و7 آحاد.",
                    "Écris en chiffres puis en mots : 3 d 1 u ; 5 d 6 u ; 6 d 7 u."), [
        F("30 + 1 = 31 → thirty-one"),
        F("50 + 6 = 56 → fifty-six"),
        F("60 + 7 = 67 → sixty-seven"),
    ]),
    EX("5", "23", st("Complete: 20 + _ = 27; 40 + _ = 49; 50 + _ = 58; 60 + _ = 69; 50 + _ = 53; 30 + _ = 32; 50 + _ = 56; 40 + _ = 47; 60 + _ = 64.",
                    "أكمل: 20 + _ = 27؛ 40 + _ = 49؛ 50 + _ = 58؛ 60 + _ = 69؛ 50 + _ = 53؛ 30 + _ = 32؛ 50 + _ = 56؛ 40 + _ = 47؛ 60 + _ = 64.",
                    "Complète : 20 + _ = 27 ; 40 + _ = 49 ; 50 + _ = 58 ; 60 + _ = 69 ; 50 + _ = 53 ; 30 + _ = 32 ; 50 + _ = 56 ; 40 + _ = 47 ; 60 + _ = 64."), [
        T("The missing number is the ones digit: the target number minus its tens.", "العدد الناقص هو رقم الآحاد: العدد المطلوب ناقص عشراته.", "Le nombre manquant est le chiffre des unités."),
        F("7   9   8   9   3   2   6   7   4"),
    ]),
]
