"""Grade 2 Mathematics — Order of numbers up to 199."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G02-MATH-EN-032"
GRADE = 2
SUBJECT = "math"
TITLES = {"en": "Order of numbers up to 199", "ar": "ترتيب الأعداد حتى 199", "fr": "Ordre des nombres jusqu'à 199"}


def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}


QUIZ = [
    {"q": "Compare 147 and 174.", "opts": ["147 < 174", "147 > 174", "147 = 174", "We cannot tell"], "a": 0,
     "why": {"147 > 174": _w("The hundreds are equal, so look at the tens: 4 tens is less than 7 tens.", "المئات متساوية فننظر إلى العشرات: 4 عشرات أقل من 7 عشرات.", "Les centaines sont égales ; on regarde les dizaines : 4 < 7."),
             "147 = 174": _w("The tens are different (4 and 7), so the numbers are not equal.", "العشرات مختلفة (4 و7) فالعددان غير متساويين.", "Les dizaines sont différentes (4 et 7)."),
             "We cannot tell": _w("We can always tell: compare hundreds, then tens, then ones.", "نستطيع دائمًا: نقارن المئات ثم العشرات ثم الآحاد.", "On compare centaines, puis dizaines, puis unités.")},
     "ok": "147 < 174"},
    {"q": "What number comes right after 179?", "opts": ["180", "1710", "178", "189"], "a": 0,
     "why": {"1710": _w("Right after means plus 1: 179 + 1 = 180.", "بعده مباشرة يعني زيادة 1: 179 + 1 = 180.", "Juste après : 179 + 1 = 180."),
             "178": _w("178 is right before 179.", "178 هو العدد قبل 179 مباشرة.", "178 est juste avant 179."),
             "189": _w("189 is 10 more, not 1 more.", "189 أكبر بـ 10 لا بـ 1.", "189 a 10 de plus, pas 1.")},
     "ok": "179 + 1 = 180"},
    {"q": "Which number is between 168 and 170?", "opts": ["169", "167", "171", "168"], "a": 0,
     "why": {"167": _w("167 is smaller than 168.", "167 أصغر من 168.", "167 est plus petit que 168."),
             "171": _w("171 is bigger than 170.", "171 أكبر من 170.", "171 est plus grand que 170."),
             "168": _w("168 is one of the two numbers, not between them.", "168 أحد العددين وليس بينهما.", "168 est l'un des deux nombres.")},
     "ok": "168, 169, 170"},
]

THEORY = [
    ("Compare from the biggest place", "نقارن من أكبر منزلة", "On compare à partir de la plus grande position", "70", [
        T("Hello, little mathematician! Which is bigger, 132 or 124? Look at the digits from the left. The hundreds are equal: 1 and 1. So we go to the tens: 3 tens is more than 2 tens. So 132 > 124.",
          "مرحبًا يا رياضي صغير! أيهما أكبر 132 أم 124؟ ننظر إلى الأرقام من اليسار. المئات متساوية: 1 و1. ننتقل إلى العشرات: 3 عشرات أكثر من 2 عشرات. إذن 132 > 124.",
          "Bonjour ! Quel nombre est le plus grand, 132 ou 124 ? Les centaines sont égales (1 et 1). On regarde les dizaines : 3 dizaines > 2 dizaines. Donc 132 > 124."),
        F("132 > 124"),
        T("Our rule: hundreds first, then tens, then ones only if we still need them.",
          "قاعدتنا: المئات أولًا ثم العشرات ثم الآحاد إذا بقينا بحاجة إليها.",
          "Notre règle : centaines d'abord, puis dizaines, puis unités si besoin."),
        F("hundreds → tens → ones"),
    ]),
    ("Ones cannot beat bigger tens", "الآحاد لا تغلب عشرات أكبر", "Les unités ne battent pas des dizaines plus grandes", "70", [
        T("Compare 126 and 141. Some children look at the ones and say 6 is more than 1. Stop! We look at the tens first: 2 tens is less than 4 tens. So 126 < 141.",
          "قارن 126 و141. بعض الأطفال ينظرون إلى الآحاد ويقولون 6 أكبر من 1. قف! ننظر إلى العشرات أولًا: 2 عشرات أقل من 4 عشرات. إذن 126 < 141.",
          "Compare 126 et 141. Attention : on regarde d'abord les dizaines : 2 < 4. Donc 126 < 141."),
        F("126 < 141"),
        T("Another one: 140 and 116. 4 tens is more than 1 ten, so 140 > 116.",
          "مثال آخر: 140 و116. 4 عشرات أكثر من عشرة واحدة، إذن 140 > 116.",
          "Autre exemple : 140 et 116. 4 dizaines > 1 dizaine, donc 140 > 116."),
        F("140 > 116"),
    ]),
    ("Calculate first, then compare", "نحسب أولًا ثم نقارن", "On calcule d'abord, puis on compare", "70", [
        T("Sometimes one side is a sum. We calculate it first. Compare 173 and 100 + 43. First 100 + 43 = 143. Then 173 > 143.",
          "أحيانًا يكون أحد الطرفين مجموعًا، فنحسبه أولًا. قارن 173 و100 + 43. أولًا 100 + 43 = 143. ثم 173 > 143.",
          "Parfois un côté est une somme : on la calcule d'abord. 100 + 43 = 143, donc 173 > 143."),
        F("173 > 100 + 43      because 100 + 43 = 143"),
        T("And 182 and 100 + 82: since 100 + 82 = 182, the two sides are equal.",
          "و182 مع 100 + 82: بما أن 100 + 82 = 182 فالطرفان متساويان.",
          "Et 182 avec 100 + 82 : 100 + 82 = 182, donc égalité."),
        F("182 = 100 + 82"),
    ]),
    ("Right before, right after, between", "قبل مباشرة وبعد مباشرة وبين", "Juste avant, juste après, entre", "71", [
        T("Right before a number means one less. Right after means one more. For 179: right before is 178, right after is 180. For 100: right before is 99.",
          "قبل العدد مباشرة يعني أقل بواحد وبعده مباشرة يعني أكثر بواحد. للعدد 179: قبله 178 وبعده 180. وللعدد 100: قبله 99.",
          "Juste avant : 1 de moins. Juste après : 1 de plus. Pour 179 : 178 et 180. Avant 100 : 99."),
        F("178, 179, 180"),
        T("A number between two numbers is the one missing in the counting. Between 168 and 170 we count 168, 169, 170, so the missing one is 169.",
          "العدد الذي بين عددين هو العدد الناقص في العدّ. بين 168 و170 نعدّ 168 ثم 169 ثم 170، فالناقص هو 169.",
          "Entre 168 et 170, on compte 168, 169, 170 : le nombre manquant est 169."),
        F("168, 169, 170"),
    ]),
    ("Riddles and ordering", "ألغاز وترتيب", "Devinettes et rangement", "71", [
        T("In a riddle we must use every clue at the same time. I am greater than 120 and less than 130, and my ones digit is 5. The numbers between are 121 to 129, and only one ends in 5: it is 125.",
          "في اللغز نستعمل كل الدلائل معًا. أنا أكبر من 120 وأصغر من 130 ورقم آحادي 5. الأعداد من 121 إلى 129 ولا يُنتهي بـ 5 منها إلا 125.",
          "Dans une devinette, on utilise tous les indices : plus grand que 120, plus petit que 130, unités = 5 : c'est 125."),
        F("120 < 125 < 130"),
        T("To put numbers in order, all of 132, 159, 168, 172, 193 have 1 hundred, so we compare the tens: 3, 5, 6, 7, 9. The order from smallest to greatest is 132 < 159 < 168 < 172 < 193.",
          "لترتيب الأعداد 132 و159 و168 و172 و193: كلها فيها مئة واحدة فنقارن العشرات: 3 و5 و6 و7 و9. الترتيب من الأصغر إلى الأكبر: 132 < 159 < 168 < 172 < 193.",
          "Toutes ont 1 centaine ; on compare les dizaines : 3, 5, 6, 7, 9. Donc 132 < 159 < 168 < 172 < 193."),
        F("132 < 159 < 168 < 172 < 193"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Well done! To compare, start with the hundreds, then the tens, then the ones. Calculate sums before comparing. Right before is one less, right after is one more. In a riddle, check every clue.",
          "أحسنت! للمقارنة نبدأ بالمئات ثم العشرات ثم الآحاد. نحسب المجاميع قبل المقارنة. قبله مباشرة أقل بواحد وبعده مباشرة أكثر بواحد. وفي اللغز نتحقق من كل دليل.",
          "Bravo ! On compare centaines, dizaines, unités ; on calcule avant de comparer ; on vérifie chaque indice."),
        F("hundreds → tens → ones → check every clue"),
    ]),
]

EXERCISES = [
    EX("1", "70", st("Compare: 126 and 141; 140 and 116.", "قارن: 126 و141؛ 140 و116.", "Compare : 126 et 141 ; 140 et 116."), [
        T("Same hundreds. 2 tens < 4 tens, so 126 < 141. Then 4 tens > 1 ten, so 140 > 116.",
          "المئات متساوية. 2 عشرات < 4 عشرات إذن 126 < 141. ثم 4 عشرات > عشرة واحدة إذن 140 > 116.",
          "Mêmes centaines. 2 < 4 donc 126 < 141. 4 > 1 donc 140 > 116."),
        F("126 < 141      140 > 116"),
    ]),
    EX("2", "70", st("Compare: 138 and 154; 102 and 136; 185 and 158.", "قارن: 138 و154؛ 102 و136؛ 185 و158.", "Compare : 138 et 154 ; 102 et 136 ; 185 et 158."), [
        T("Look at the tens each time: 3 < 5, 0 < 3, and 8 > 5.", "ننظر إلى العشرات: 3 < 5 و0 < 3 و8 > 5.", "On regarde les dizaines : 3 < 5, 0 < 3, 8 > 5."),
        F("138 < 154      102 < 136      185 > 158"),
    ]),
    EX("3", "70", st("Use <, > or =: 112 _ 138; 123 _ 100 + 38; 182 _ 100 + 82; 173 _ 100 + 43.", "استعمل <، > أو =: 112 _ 138؛ 123 _ 100 + 38؛ 182 _ 100 + 82؛ 173 _ 100 + 43.", "Utilise <, > ou = : 112 _ 138 ; 123 _ 100 + 38 ; 182 _ 100 + 82 ; 173 _ 100 + 43."), [
        T("Calculate the sums first: 100 + 38 = 138, 100 + 82 = 182, 100 + 43 = 143.", "نحسب المجاميع أولًا: 100 + 38 = 138 و100 + 82 = 182 و100 + 43 = 143.", "On calcule d'abord : 138, 182, 143."),
        F("112 < 138      123 < 138      182 = 182      173 > 143"),
    ]),
    EX("4", "70", st("Complete with an appropriate number: 112 < __ ; 100 + 25 < __.", "أكمل بعدد مناسب: 112 < __ ؛ 100 + 25 < __.", "Complète avec un nombre qui convient : 112 < __ ; 100 + 25 < __."), [
        T("There is more than one correct answer. 113 works for the first one. For the second, 100 + 25 = 125, so 126 works.",
          "توجد أكثر من إجابة صحيحة. 113 تناسب الأولى. وفي الثانية 100 + 25 = 125 فالعدد 126 يناسب.",
          "Plusieurs réponses sont possibles : 113 convient ; 100 + 25 = 125, donc 126 convient."),
        F("112 < 113      100 + 25 < 126"),
    ]),
    EX("5", "71", st("Write the number right before and right after: 132, 120, 109, 179, 100, 141.", "اكتب العدد قبله مباشرة وبعده مباشرة: 132، 120، 109، 179، 100، 141.", "Écris le nombre juste avant et juste après : 132, 120, 109, 179, 100, 141."),  [
        F("131, 132, 133      119, 120, 121      108, 109, 110"),
        F("178, 179, 180      99, 100, 101      140, 141, 142"),
    ]),
    EX("6", "71", st("Find the number between: 109 _ 111; 100 _ 102; 168 _ 170; 150 _ 152.", "جد العدد الذي بين: 109 _ 111؛ 100 _ 102؛ 168 _ 170؛ 150 _ 152.", "Trouve le nombre entre : 109 _ 111 ; 100 _ 102 ; 168 _ 170 ; 150 _ 152."), [
        F("110      101      169      151"),
    ]),
    EX("7", "71", st("Riddle: I am greater than 120 and less than 130. My ones digit is 5. Who am I?", "لغز: أنا أكبر من 120 وأصغر من 130 ورقم آحادي 5. من أنا؟", "Devinette : je suis plus grand que 120, plus petit que 130, mon chiffre des unités est 5."), [
        F("125"),
    ]),
    EX("8", "71", st("Riddle: I am greater than 100. My tens digit is between 5 and 7 and my ones digit is between 7 and 9.", "لغز: أنا أكبر من 100، رقم عشراتي بين 5 و7 ورقم آحادي بين 7 و9.", "Devinette : plus grand que 100, dizaines entre 5 et 7, unités entre 7 et 9."), [
        T("Between 5 and 7 is 6. Between 7 and 9 is 8. The hundreds digit is 1.", "بين 5 و7 هو 6، وبين 7 و9 هو 8، ورقم المئات 1.", "Entre 5 et 7 : 6. Entre 7 et 9 : 8. Centaines : 1."),
        F("168"),
    ]),
    EX("9", "71", st("Arrange from smallest to greatest: 132, 172, 193, 168, 159. Then circle the numbers greater than 125 and less than 168 in: 122, 186, 152, 148, 193, 119.", "رتّب من الأصغر إلى الأكبر: 132، 172، 193، 168، 159. ثم حدد الأعداد الأكبر من 125 والأصغر من 168 في: 122، 186، 152، 148، 193، 119.", "Range du plus petit au plus grand : 132, 172, 193, 168, 159. Puis entoure ceux entre 125 et 168 dans : 122, 186, 152, 148, 193, 119."), [
        F("132 < 159 < 168 < 172 < 193"),
        T("For the list: 122 is less than 125, 186 and 193 are too big, 119 is too small. Only 148 and 152 are between 125 and 168.",
          "في القائمة: 122 أصغر من 125 و186 و193 كبيران و119 صغير. فقط 148 و152 بين 125 و168.",
          "122 est trop petit, 186 et 193 trop grands, 119 trop petit : seuls 148 et 152 conviennent."),
        F("148, 152"),
    ]),
    EX("10", "71", st("Riddle: I am greater than 110 and less than 120. The sum of my digits is 3.", "لغز: أنا أكبر من 110 وأصغر من 120 ومجموع أرقامي 3.", "Devinette : plus grand que 110, plus petit que 120, somme des chiffres 3."), [
        T("The hundreds digit is 1 and the tens digit is 1. We need 3 in all, so the ones digit is 1. Check: 111 > 110, 111 < 120, 1 + 1 + 1 = 3.",
          "رقم المئات 1 ورقم العشرات 1. نحتاج المجموع 3 فرقم الآحاد 1. تحقق: 111 > 110 و111 < 120 و1 + 1 + 1 = 3.",
          "Centaines 1, dizaines 1 ; il faut 3 en tout donc unités 1. Vérification : 111 convient."),
        F("111"),
    ]),
]
