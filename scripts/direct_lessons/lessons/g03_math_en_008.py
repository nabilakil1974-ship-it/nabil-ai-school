"""Grade 3 Mathematics — Subtraction (meaning and place value, no regrouping)."""
from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.draw import hops, bar_model, blocks, vsub

LESSON_ID = "G03-MATH-EN-008"
GRADE = 3
SUBJECT = "math"
TITLES = {"en": "Subtraction", "ar": "الطرح", "fr": "La soustraction"}


def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}


QUIZ = [
    {"q": "In 586 − 243 = 343, which number is the difference?", "opts": ["343", "586", "243", "829"], "a": 0,
     "why": {"586": _w("586 is the minuend: the amount we start with.", "586 هو المطروح منه: ما نبدأ به.", "586 = terme de départ."),
             "243": _w("243 is the subtrahend: the amount taken away.", "243 هو المطروح: ما نأخذه.", "243 = retiré."),
             "829": _w("829 = 586 + 243. That is an addition result.", "829 = 586 + 243 وهذا ناتج جمع.", "Somme.")}, "ok": "343"},
    {"q": "Calculate 475 − 152.", "opts": ["323", "627", "333", "313"], "a": 0,
     "why": {"627": _w("627 = 475 + 152, but we subtract.", "627 = 475 + 152 ونحن نطرح.", "C'est une somme."),
             "333": _w("Check tens: 7 − 5 = 2, not 3.", "تحقق من العشرات: 7 − 5 = 2 لا 3.", "7 − 5 = 2."),
             "313": _w("Check tens: 7 − 5 = 2, not 1.", "العشرات: 7 − 5 = 2 لا 1.", "7 − 5 = 2.")}, "ok": "323"},
    {"q": "586 − 43 = ? Where does the digit 4 of 43 belong?", "opts": ["Tens column: 586 − 43 = 543", "Hundreds column: 586 − 43 = 156", "Ones column: 586 − 43 = 583", "Anywhere"], "a": 0,
     "why": {"Hundreds column: 586 − 43 = 156": _w("43 has only two digits: 4 tens and 3 ones. Hundreds stay 5.", "العدد 43 فيه رقمان: 4 عشرات و3 آحاد والمئات تبقى 5.", "43 = 4 dizaines, 3 unités."),
             "Ones column: 586 − 43 = 583": _w("4 means four tens, not four ones.", "4 تعني أربع عشرات لا أربعة آحاد.", "4 dizaines."),
             "Anywhere": _w("Digits must be under the same place.", "الأرقام تحت المنزلة نفسها.", "Même colonne.")}, "ok": "Tens column: 586 − 43 = 543"},
]

THEORY = [
    ("What subtraction means", "ماذا يعني الطرح", "Le sens de la soustraction", "26", [
        T("Hello, champion! We subtract when we start with an amount and take a part away, or when we compare two amounts. Nour has 586 beads and gives 243 away. We start with 586 (the minuend), we take away 243 (the subtrahend), and what remains is the difference. 586 − 243 = 343.",
          "مرحبًا يا بطل! نطرح عندما نبدأ بكمية ونأخذ منها جزءًا أو عندما نقارن كميتين. عند نور 586 خرزة وأعطت 243. نبدأ بـ 586 (المطروح منه) ونأخذ 243 (المطروح) والباقي هو الفرق. 586 − 243 = 343.",
          "On part de 586, on retire 243, il reste la différence : 586 − 243 = 343."),
        bar_model(586, 243, 343, tag="A1"),
        F("586 − 243 = 343"),
        T("Always say what each number is before you calculate: the starting amount first, then the part taken away, then the difference. The sentence says: starting amount − part taken away = what remains.",
          "قل دائمًا ما هو كل عدد قبل أن تحسب: الكمية الأولى ثم الجزء المأخوذ ثم الفرق. الجملة: الكمية الأولى − الجزء المأخوذ = الباقي.",
          "Départ − retiré = reste."),
    ]),
    ("Subtract by place value", "اطرح بحسب المنازل", "Soustraire par position", "26", [
        T("Write the numbers in columns with hundreds under hundreds, tens under tens and ones under ones. Then subtract each column, starting with the ones: 6 − 3 = 3, 8 − 4 = 4, 5 − 2 = 3. The difference is 3 hundreds, 4 tens, 3 ones = 343.",
          "نكتب العددين في أعمدة: المئات تحت المئات والعشرات تحت العشرات والآحاد تحت الآحاد. ثم نطرح كل عمود مبتدئين بالآحاد: 6 − 3 = 3 و8 − 4 = 4 و5 − 2 = 3. الفرق 3 مئات و4 عشرات و3 آحاد = 343.",
          "On aligne C, D, U puis on soustrait chaque colonne : 343."),
        vsub(586, 243, tag="A2"),
        F("586 − 243 = 343"),
        T("Picture it with blocks: 343 is 3 hundred-squares, 4 ten-rods and 3 ones. Take away 2 hundreds, 4 tens and 3 ones from 586 and 3 hundreds, 4 tens, 3 ones are left.",
          "تخيّلها بالمكعبات: 343 هو 3 مربعات مئة و4 قضبان عشرة و3 آحاد. نأخذ من 586 مئتين و4 عشرات و3 آحاد فيبقى 3 مئات و4 عشرات و3 آحاد.",
          "343 = 3 centaines, 4 dizaines, 3 unités."),
        blocks(3, 4, 3, tag="A2b"),
    ]),
    ("A number with fewer digits", "عدد برقمين", "Un nombre à deux chiffres", "27", [
        T("Be careful with 586 − 43. The number 43 has no hundreds. Its 4 is in the tens column and its 3 in the ones column. Ones: 6 − 3 = 3. Tens: 8 − 4 = 4. Hundreds: nothing to take away, so it stays 5. The answer is 543.",
          "انتبه في 586 − 43. العدد 43 لا مئات فيه. الرقم 4 في عمود العشرات و3 في عمود الآحاد. الآحاد: 6 − 3 = 3. العشرات: 8 − 4 = 4. المئات: لا شيء نطرحه فتبقى 5. الجواب 543.",
          "43 n'a pas de centaines : 586 − 43 = 543."),
        vsub(586, 43, tag="A3"),
        F("586 − 43 = 543      check: 543 + 43 = 586 ✓"),
        T("Error detective! A learner writes 586 − 43 = 156, subtracting 4 from the hundreds digit. The 4 means four tens, not four hundreds. Always line the digits up from the right.",
          "المحقق! كتب متعلّم 586 − 43 = 156 فطرح 4 من رقم المئات. الرقم 4 يعني أربع عشرات لا أربع مئات. رتّب الأرقام دائمًا من اليمين.",
          "Erreur : 156. Il faut aligner à droite : 543."),
    ]),
    ("Round hundreds and tens", "مئات وعشرات كاملة", "Centaines et dizaines entières", "27", [
        T("Subtracting hundreds, tens or both is quick. 700 − 300 = 400 because 7 hundreds take away 3 hundreds leaves 4 hundreds. 750 − 430: take 4 hundreds and 3 tens away from 7 hundreds and 5 tens to get 3 hundreds and 2 tens: 320.",
          "طرح المئات أو العشرات سريع. 700 − 300 = 400 لأن 7 مئات ناقص 3 مئات يبقى 4 مئات. 750 − 430: نأخذ 4 مئات و3 عشرات من 7 مئات و5 عشرات فيبقى 3 مئات وعشرتان: 320.",
          "700 − 300 = 400 ; 750 − 430 = 320."),
        hops(750, [-400, -30], tag="A4"),
        F("750 − 430 = 320"),
    ]),
    ("Compare: how many more?", "قارن: كم أكثر؟", "Comparer : de combien de plus ?", "27", [
        T("Subtraction also compares. A school has 372 pupils in the morning and 140 in the afternoon. How many more in the morning? 372 − 140 = 232. We compare, so we subtract the smaller from the greater: ones 2 − 0 = 2, tens 7 − 4 = 3, hundreds 3 − 1 = 2.",
          "الطرح يقارن أيضًا. في مدرسة 372 تلميذًا صباحًا و140 بعد الظهر. كم تلميذًا أكثر صباحًا؟ 372 − 140 = 232. نقارن فنطرح الأصغر من الأكبر: آحاد 2 − 0 = 2 وعشرات 7 − 4 = 3 ومئات 3 − 1 = 2.",
          "372 − 140 = 232 élèves de plus le matin."),
        vsub(372, 140, tag="A5"),
        F("372 − 140 = 232      check: 140 + 232 = 372 ✓"),
    ]),
    ("Check with addition", "تحقق بالجمع", "Vérifier par l'addition", "27", [
        T("The difference plus the part taken away must give back the starting amount. 343 + 243 = 586 ✓. If you do not get the starting amount, go back and look at each column again.",
          "الفرق مع الجزء المأخوذ يجب أن يعيدا الكمية الأولى. 343 + 243 = 586 ✓. إذا لم نحصل على الكمية الأولى نعود فنراجع كل عمود.",
          "différence + retiré = départ : 343 + 243 = 586."),
        F("difference + taken away = start"),
        F("343 + 243 = 586 ✓"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Subtraction: starting amount − part taken away = difference. Write hundreds, tens and ones in columns, subtract from the right, and interpret the answer in words. Check by adding the difference to the part you took away.",
          "الطرح: الكمية الأولى − الجزء المأخوذ = الفرق. نكتب المئات والعشرات والآحاد في أعمدة ونطرح من اليمين ونفسّر الجواب بكلمات. نتحقق بجمع الفرق مع الجزء المأخوذ.",
          "Départ − retiré = différence ; colonnes ; vérifier par l'addition."),
        F("MEANING → H-T-O → SUBTRACT → EXPLAIN → CHECK"),
    ]),
]


def _ex(n, en, ar, fr, steps):
    return EX(n, "", st(en, ar, fr), steps)


EXERCISES = [
    _ex("1", "Calculate 497 − 264.", "احسب 497 − 264.", "Calcule 497 − 264.", [T("Ones 7 − 4 = 3. Tens 9 − 6 = 3. Hundreds 4 − 2 = 2. Answer 233.", "الآحاد 7 − 4 = 3. العشرات 9 − 6 = 3. المئات 4 − 2 = 2. الجواب 233.", "233."), vsub(497, 264, tag="X1"), F("497 − 264 = 233      233 + 264 = 497 ✓")]),
    _ex("2", "Calculate 658 − 327.", "احسب 658 − 327.", "Calcule 658 − 327.", [T("8 − 7 = 1; 5 − 2 = 3; 6 − 3 = 3. Answer 331.", "8 − 7 = 1؛ 5 − 2 = 3؛ 6 − 3 = 3. الجواب 331.", "331."), vsub(658, 327, tag="X2"), F("658 − 327 = 331      331 + 327 = 658 ✓")]),
    _ex("3", "Calculate 809 − 405.", "احسب 809 − 405.", "Calcule 809 − 405.", [T("9 − 5 = 4; 0 − 0 = 0; 8 − 4 = 4. Answer 404.", "9 − 5 = 4؛ 0 − 0 = 0؛ 8 − 4 = 4. الجواب 404.", "404."), vsub(809, 405, tag="X3"), F("809 − 405 = 404")]),
    _ex("4", "Calculate 750 − 430 and 900 − 600.", "احسب 750 − 430 و900 − 600.", "Calcule 750 − 430 et 900 − 600.", [T("750 − 430: 7 hundreds 5 tens minus 4 hundreds 3 tens = 3 hundreds 2 tens = 320. And 9 hundreds − 6 hundreds = 3 hundreds = 300.", "750 − 430: 7 مئات و5 عشرات ناقص 4 مئات و3 عشرات = 3 مئات وعشرتان = 320. و9 مئات − 6 مئات = 3 مئات = 300.", "320 et 300."), F("750 − 430 = 320      900 − 600 = 300")]),
    _ex("5", "Calculate 586 − 43 and explain where the 4 goes.", "احسب 586 − 43 واشرح أين يوضع الرقم 4.", "Calcule 586 − 43.", [T("43 is 4 tens and 3 ones. Ones 6 − 3 = 3, tens 8 − 4 = 4, hundreds stay 5. Answer 543.", "43 هو 4 عشرات و3 آحاد. الآحاد 6 − 3 = 3 والعشرات 8 − 4 = 4 والمئات تبقى 5. الجواب 543.", "543."), vsub(586, 43, tag="X5"), F("586 − 43 = 543")]),
    _ex("6", "A bus carries 345 passengers; 123 get off. How many are left?", "في حافلة 345 راكبًا نزل منهم 123. كم بقي؟", "345 passagers, 123 descendent. Combien reste-t-il ?", [T("We remove a part: 345 − 123 = 222. Check: 222 + 123 = 345 ✓.", "نأخذ جزءًا: 345 − 123 = 222. تحقق: 222 + 123 = 345 ✓.", "222."), vsub(345, 123, tag="X6"), F("222 passengers are left")]),
    _ex("7", "School A has 372 pupils, school B 140. How many more in A?", "في المدرسة أ 372 تلميذًا وفي ب 140. كم تلميذًا أكثر في أ؟", "École A : 372, école B : 140. De combien de plus ?", [T("Compare: 372 − 140 = 232.", "نقارن: 372 − 140 = 232.", "232."), bar_model(372, 140, 232, tag="X7"), F("372 − 140 = 232")]),
    _ex("8", "Find the missing number: 786 − ? = 543.", "جد العدد الناقص: 786 − ؟ = 543.", "Trouve : 786 − ? = 543.", [T("The missing number is what was taken away: 786 − 543 = 243. Check: 786 − 243 = 543 ✓.", "العدد الناقص هو المأخوذ: 786 − 543 = 243. تحقق: 786 − 243 = 543 ✓.", "243."), F("786 − 543 = 243")]),
    _ex("9", "Find the missing number: ? − 200 = 456.", "جد العدد الناقص: ؟ − 200 = 456.", "Trouve : ? − 200 = 456.", [T("The starting amount is missing: add back what was taken: 456 + 200 = 656. Check: 656 − 200 = 456 ✓.", "الكمية الأولى ناقصة: نعيد ما أخذناه: 456 + 200 = 656. تحقق: 656 − 200 = 456 ✓.", "656."), F("656")]),
    _ex("10", "Calculate 999 − 555 and check with addition.", "احسب 999 − 555 وتحقق بالجمع.", "Calcule 999 − 555.", [T("9 − 5 = 4 in every column: 444. Check: 444 + 555 = 999 ✓.", "9 − 5 = 4 في كل عمود: 444. تحقق: 444 + 555 = 999 ✓.", "444."), vsub(999, 555, tag="X10"), F("999 − 555 = 444")]),
    _ex("11", "Error detective: a learner writes 586 − 43 = 156. Find the mistake.", "المحقق: كتب متعلّم 586 − 43 = 156. جد الخطأ.", "Détective : 586 − 43 = 156.", [T("The 4 of 43 was put in the hundreds column. It is 4 tens. Correct: ones 6 − 3 = 3, tens 8 − 4 = 4, hundreds 5: 543.", "وضع الرقم 4 في عمود المئات وهو 4 عشرات. الصحيح: آحاد 6 − 3 = 3 وعشرات 8 − 4 = 4 ومئات 5: 543.", "543."), F("586 − 43 = 543")]),
    _ex("12", "Tell the story: write a subtraction story for 650 − 230 and solve it.", "اروِ قصة: اكتب قصة طرح لـ 650 − 230 واحلّها.", "Invente une histoire pour 650 − 230 et résous-la.", [T("For example: a shop has 650 notebooks and sells 230. 650 − 230: 6 hundreds 5 tens minus 2 hundreds 3 tens = 4 hundreds 2 tens = 420. 420 notebooks are left. Check: 420 + 230 = 650 ✓.", "مثال: متجر فيه 650 دفترًا باع 230. 650 − 230: 6 مئات و5 عشرات ناقص 2 مئتين و3 عشرات = 4 مئات وعشرتان = 420. بقي 420 دفترًا. تحقق: 420 + 230 = 650 ✓.", "420 cahiers."), F("650 − 230 = 420")]),
]
