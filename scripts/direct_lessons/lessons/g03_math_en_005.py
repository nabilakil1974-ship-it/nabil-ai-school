"""Grade 3 Mathematics — Reading the Calendar."""
from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.draw import calendar

LESSON_ID = "G03-MATH-EN-005"
GRADE = 3
SUBJECT = "math"
TITLES = {"en": "Reading the Calendar", "ar": "قراءة التقويم", "fr": "Lire le calendrier"}

R = "#e53935"; B = "#1e88e5"; G = "#2e7d32"; O = "#fb8c00"


def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}


QUIZ = [
    {"q": "In our April calendar, day 1 is a Wednesday. What day is April 8?", "opts": ["Wednesday", "Thursday", "Tuesday", "Monday"], "a": 0,
     "why": {"Thursday": _w("8 is exactly 7 days after 1, so the weekday is the same, not the next one.", "8 بعد 1 بسبعة أيام بالضبط فاليوم نفسه لا التالي.", "8 = 1 + 7, même jour."),
             "Tuesday": _w("Moving 7 days forward never changes the weekday.", "التقدم 7 أيام لا يغيّر اليوم.", "+7 ne change pas le jour."),
             "Monday": _w("Check the column of 8: it is under Wed.", "تحقق من عمود 8: تحت الأربعاء.", "Colonne de Wed.")}, "ok": "Wednesday"},
    {"q": "Which date is the day after Sunday 12?", "opts": ["Monday 13", "Saturday 11", "Sunday 19", "Monday 6"], "a": 0,
     "why": {"Saturday 11": _w("That is the day BEFORE.", "هذا اليوم السابق.", "Veille."),
             "Sunday 19": _w("That is one week later.", "هذا بعد أسبوع.", "Une semaine plus tard."),
             "Monday 6": _w("That is one week before Monday 13.", "هذا قبل الاثنين 13 بأسبوع.", "Une semaine avant.")}, "ok": "Monday 13"},
    {"q": "How many days from the 6th to the 20th?", "opts": ["14", "13", "15", "7"], "a": 0,
     "why": {"13": _w("20 − 6 = 14. Do not count the starting day.", "20 − 6 = 14. لا نعدّ يوم البداية.", "20 − 6 = 14."),
             "15": _w("Do not count both ends.", "لا نعدّ الطرفين.", "Pas les deux bouts."),
             "7": _w("7 days is only one week; here we have two weeks.", "7 أيام أسبوع واحد وهنا أسبوعان.", "Deux semaines.")}, "ok": "14"},
]

THEORY = [
    ("The parts of a calendar", "أجزاء التقويم", "Les parties du calendrier", "20", [
        T("Hello, champion! A calendar is a table for one month. The month name is at the top. The row of names (Mon, Tue, Wed ...) shows the seven days of the week. Each line of numbers is one week. Each column belongs to one weekday. In this April, day 1 sits under Wednesday.",
          "مرحبًا يا بطل! التقويم جدول لشهر واحد. اسم الشهر في الأعلى. صف الأسماء (الاثنين، الثلاثاء، الأربعاء ...) يبيّن أيام الأسبوع السبعة. كل سطر من الأعداد هو أسبوع. وكل عمود يخص يومًا واحدًا من الأسبوع. في شهر نيسان هذا يقع اليوم 1 تحت الأربعاء.",
          "Un calendrier est un tableau d'un mois : les noms des jours en haut, chaque ligne est une semaine, chaque colonne un jour de la semaine."),
        calendar(2, 30, {1: R}, tag="C1"),
        T("Look at the first line: it starts with empty boxes because the month begins on Wednesday. Count the days of the week: Mon, Tue, Wed, Thu, Fri, Sat, Sun — seven. So each line has seven boxes.",
          "انظر إلى السطر الأول: يبدأ بخانات فارغة لأن الشهر يبدأ يوم الأربعاء. عدّ أيام الأسبوع: الاثنين، الثلاثاء، الأربعاء، الخميس، الجمعة، السبت، الأحد — سبعة. لذلك في كل سطر سبع خانات.",
          "Le mois commence un mercredi ; chaque ligne a sept cases."),
    ]),
    ("Find the weekday of a date", "جد يوم الأسبوع لتاريخ", "Trouver le jour d'une date", "20", [
        T("To find the weekday of the 17th: find 17 in the grid, then slide straight UP its column to the heading. The 17 is under Fri, so April 17 is a Friday. Do the same for the 22: it is under Wed, so it is a Wednesday.",
          "لإيجاد يوم 17: جد العدد 17 في الجدول ثم اصعد في عموده إلى العنوان. العدد 17 تحت الجمعة فهو يوم جمعة. وكذلك 22 تحت الأربعاء فهو يوم أربعاء.",
          "Pour le 17 : on remonte la colonne jusqu'à l'en-tête : vendredi."),
        calendar(2, 30, {17: R, 22: B}, tag="C2"),
        F("17 → Fri      22 → Wed"),
        T("Never guess from memory. Follow the grid: row for the week, column for the day. Which column would the 30 be in? Under Thu, the next box after Wed 29.",
          "لا تخمّن من الذاكرة. اتبع الجدول: السطر للأسبوع والعمود لليوم. في أي عمود يقع 30؟ تحت الخميس بعد الأربعاء 29.",
          "Suivre la grille : ligne = semaine, colonne = jour."),
    ]),
    ("The day before and the day after", "اليوم السابق واليوم التالي", "La veille et le lendemain", "21", [
        T("The day after a date is the next box to the right: after Thu 16 comes Fri 17. The day before is the box on the left: before Thu 16 is Wed 15. Careful at the end of a line! After Sunday 19 we jump to the start of the next line: Monday 20.",
          "اليوم التالي هو الخانة التالية إلى اليمين: بعد الخميس 16 يأتي الجمعة 17. واليوم السابق هو الخانة إلى اليسار: قبل الخميس 16 الأربعاء 15. انتبه عند نهاية السطر! بعد الأحد 19 نقفز إلى بداية السطر التالي: الاثنين 20.",
          "Après Thu 16 : Fri 17. Avant : Wed 15. Après Sun 19 : Mon 20 (ligne suivante)."),
        calendar(2, 30, {16: B, 17: G, 19: R, 20: G}, tag="C3"),
        F("after 16 → 17      before 16 → 15      after Sun 19 → Mon 20"),
        T("Error detective! A learner says: the day after Sunday 19 is Sunday 26. That is a whole week later. The next day is always date + 1, and the weekday moves one column: Sunday goes to Monday.",
          "المحقق! قال متعلّم: اليوم بعد الأحد 19 هو الأحد 26. هذا بعد أسبوع كامل. اليوم التالي دائمًا التاريخ + 1 ويتحرك اليوم عمودًا واحدًا: الأحد يصبح الاثنين.",
          "Erreur : lendemain du dimanche 19 ≠ dimanche 26. C'est lundi 20."),
    ]),
    ("Seven days later", "بعد سبعة أيام", "Sept jours plus tard", "21", [
        T("Move 7 days and you land exactly below the same weekday in the next line. Fridays: 3, 10, 17, 24. Each is 7 more than the one before: 3 + 7 = 10, 10 + 7 = 17, 17 + 7 = 24. A week later, same weekday!",
          "عند التقدم 7 أيام نقع تمامًا تحت اليوم نفسه في السطر التالي. أيام الجمعة: 3 و10 و17 و24. كل واحد يزيد 7 على السابق: 3 + 7 = 10 و10 + 7 = 17 و17 + 7 = 24. بعد أسبوع نحصل على اليوم نفسه!",
          "Les vendredis : 3, 10, 17, 24 ; chaque fois + 7."),
        calendar(2, 30, {3: R, 10: R, 17: R, 24: R}, tag="C4"),
        F("3 → 10 → 17 → 24      (+ 7 each time)"),
        T("The same works backward: 7 days before Fri 24 is Fri 17. And 14 days after Fri 3 is Fri 17, because 14 is two weeks: 3 + 14 = 17.",
          "ويصح ذلك إلى الخلف: قبل الجمعة 24 بسبعة أيام الجمعة 17. وبعد الجمعة 3 بأربعة عشر يومًا الجمعة 17 لأن 14 أسبوعان: 3 + 14 = 17.",
          "7 jours avant le vendredi 24 : vendredi 17 ; 3 + 14 = 17."),
    ]),
    ("Counting the days between", "عدّ الأيام بين تاريخين", "Compter les jours entre deux dates", "21", [
        T("How many days from Wed 8 to Sat 18? Subtract the dates: 18 − 8 = 10 days. We do not count the day we start from. Check with weeks: Wed 8 → Wed 15 is 7 days, then Wed 15 → Sat 18 is 3 more. 7 + 3 = 10 ✓.",
          "كم يومًا من الأربعاء 8 إلى السبت 18؟ نطرح التاريخين: 18 − 8 = 10 أيام. لا نعدّ يوم البداية. نتحقق بالأسابيع: من الأربعاء 8 إلى الأربعاء 15 سبعة أيام ثم من الأربعاء 15 إلى السبت 18 ثلاثة أيام. 7 + 3 = 10 ✓.",
          "18 − 8 = 10 jours ; contrôle : 7 + 3 = 10."),
        calendar(2, 30, {8: R, 15: O, 18: G}, tag="C5"),
        F("18 − 8 = 10      10 days = 1 week + 3 days"),
        T("A fast rule: days between = later date − earlier date. And to turn days into weeks: 14 days = 2 weeks, 21 days = 3 weeks, 17 days = 2 weeks and 3 days.",
          "قاعدة سريعة: الأيام بين تاريخين = التاريخ الأكبر − التاريخ الأصغر. ولتحويل الأيام إلى أسابيع: 14 يومًا = أسبوعان و21 يومًا = 3 أسابيع و17 يومًا = أسبوعان و3 أيام.",
          "Jours entre = date plus tard − date plus tôt."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Calendar reading: find the month and the weekday names, then find the date in its row and column. +1 goes one box right (or to the next line's start). −1 goes one box left. +7 and −7 keep the same weekday. Days between two dates = later date − earlier date. Always check by tracing the boxes.",
          "قراءة التقويم: جد الشهر وأسماء الأيام ثم جد التاريخ في سطره وعموده. +1 خانة إلى اليمين (أو بداية السطر التالي). −1 خانة إلى اليسار. و+7 و−7 يحفظان اليوم نفسه. الأيام بين تاريخين = الأكبر − الأصغر. تحقق دائمًا بتتبع الخانات.",
          "+1 : case suivante ; +7 : même jour ; jours entre = grande date − petite date."),
        F("LOCATE → TRACE → INTERPRET → VERIFY"),
    ]),
]


def _ex(n, en, ar, fr, steps):
    return EX(n, "", st(en, ar, fr), steps)


C = lambda hi, tag: calendar(2, 30, hi, tag=tag)

EXERCISES = [
    _ex("1", "In our April calendar (day 1 = Wednesday), which weekday is April 10?", "في تقويم نيسان (اليوم 1 = الأربعاء) ما يوم 10 نيسان؟", "Quel jour est le 10 avril ?", [T("Find 10 and go up its column: it is under Fri.", "نجد 10 ونصعد عموده: تحت الجمعة.", "Vendredi."), C({10: R}, "E1"), F("April 10 is a Friday")]),
    _ex("2", "Which weekday is April 22?", "ما يوم 22 نيسان؟", "Quel jour est le 22 ?", [T("22 is exactly 21 days (3 weeks) after 1, so it is the same weekday as 1: Wednesday.", "22 بعد 1 بـ 21 يومًا (3 أسابيع) فهو اليوم نفسه: الأربعاء.", "Mercredi."), C({1: B, 22: R}, "E2"), F("22 = 1 + 21 → Wednesday")]),
    _ex("3", "What is the day after Sunday 12?", "ما اليوم التالي للأحد 12؟", "Quel est le lendemain du dimanche 12 ?", [T("The next box is at the start of the next line: Monday 13.", "الخانة التالية في بداية السطر التالي: الاثنين 13.", "Lundi 13."), C({12: B, 13: R}, "E3"), F("Monday 13")]),
    _ex("4", "What is the day before Monday 20?", "ما اليوم السابق للاثنين 20؟", "Quelle est la veille du lundi 20 ?", [T("The box before Monday 20 is the end of the previous line: Sunday 19.", "الخانة قبل الاثنين 20 هي نهاية السطر السابق: الأحد 19.", "Dimanche 19."), C({19: R, 20: B}, "E4"), F("Sunday 19")]),
    _ex("5", "Seven days after Thursday 2 is which date and weekday?", "بعد سبعة أيام من الخميس 2 أي تاريخ وأي يوم؟", "Sept jours après le jeudi 2 ?", [T("2 + 7 = 9. Same weekday: Thursday 9.", "2 + 7 = 9 والأسبوع نفسه: الخميس 9.", "Jeudi 9."), C({2: B, 9: R}, "E5"), F("2 + 7 = 9 → Thursday 9")]),
    _ex("6", "List all the Saturdays in April.", "اذكر كل أيام السبت في نيسان.", "Liste tous les samedis d'avril.", [T("The first Saturday is 4 (Wed 1, Thu 2, Fri 3, Sat 4). Then add 7 each time: 4, 11, 18, 25. The next one would be 32 — too big.", "أول سبت هو 4 (الأربعاء 1 والخميس 2 والجمعة 3 والسبت 4). ثم نضيف 7: 4 و11 و18 و25. التالي 32 أكبر من الشهر.", "4, 11, 18, 25."), C({4: R, 11: R, 18: R, 25: R}, "E6"), F("4, 11, 18, 25")]),
    _ex("7", "How many days from the 6th to the 20th? How many weeks?", "كم يومًا من 6 إلى 20؟ وكم أسبوعًا؟", "Combien de jours de 6 à 20 ? Combien de semaines ?", [T("20 − 6 = 14 days. 14 = 7 + 7, so 2 weeks.", "20 − 6 = 14 يومًا. 14 = 7 + 7 فهما أسبوعان.", "14 jours = 2 semaines."), C({6: R, 13: O, 20: G}, "E7"), F("20 − 6 = 14 days = 2 weeks")]),
    _ex("8", "How many days from Tuesday 7 to Friday 24? Give weeks and days.", "كم يومًا من الثلاثاء 7 إلى الجمعة 24؟ بالأسابيع والأيام.", "Combien de jours du mardi 7 au vendredi 24 ?", [T("24 − 7 = 17 days. 17 = 14 + 3, so 2 weeks and 3 days. Check: Tue 7 → Tue 21 is 14 days; Tue 21 → Fri 24 is 3 days.", "24 − 7 = 17 يومًا. 17 = 14 + 3 أي أسبوعان و3 أيام. تحقق: من الثلاثاء 7 إلى الثلاثاء 21 أربعة عشر يومًا ثم 3 أيام إلى الجمعة 24.", "17 jours = 2 semaines et 3 jours."), C({7: R, 21: O, 24: G}, "E8"), F("24 − 7 = 17 = 2 weeks + 3 days")]),
    _ex("9", "A party is 3 weeks after Monday 6. Which date and weekday?", "حفلة بعد 3 أسابيع من الاثنين 6. ما التاريخ واليوم؟", "Une fête a lieu 3 semaines après le lundi 6. Quelle date ?", [T("3 weeks = 21 days. 6 + 21 = 27. It is still a Monday.", "3 أسابيع = 21 يومًا. 6 + 21 = 27 وهو اثنين أيضًا.", "Lundi 27."), C({6: B, 13: O, 20: O, 27: R}, "E9"), F("6 + 21 = 27 → Monday 27")]),
    _ex("10", "How many Wednesdays are in April?", "كم يوم أربعاء في نيسان؟", "Combien de mercredis en avril ?", [T("Start at 1 and add 7: 1, 8, 15, 22, 29. Next is 36 — too big. So 5 Wednesdays.", "نبدأ من 1 ونضيف 7: 1 و8 و15 و22 و29. التالي 36 كبير. إذن 5 أيام أربعاء.", "1, 8, 15, 22, 29 : 5."), C({1: R, 8: R, 15: R, 22: R, 29: R}, "E10"), F("5 Wednesdays")]),
    _ex("11", "The library opens every Friday. On which dates is it open in April?", "المكتبة تفتح كل جمعة. في أي تواريخ تفتح في نيسان؟", "La bibliothèque ouvre chaque vendredi. Quelles dates ?", [T("Fridays: 3, 10, 17, 24 (add 7 each time). Four days.", "أيام الجمعة: 3 و10 و17 و24 (نضيف 7). أربعة أيام.", "3, 10, 17, 24."), C({3: R, 10: R, 17: R, 24: R}, "E11"), F("3, 10, 17, 24")]),
    _ex("12", "Today is Friday 17. The school trip is in 11 days. What date and weekday?", "اليوم الجمعة 17. الرحلة المدرسية بعد 11 يومًا. ما التاريخ واليوم؟", "Aujourd'hui vendredi 17. La sortie est dans 11 jours. Quelle date ?", [T("17 + 11 = 28. Weekday: 7 days later is Fri 24, then 4 more days: Sat 25, Sun 26, Mon 27, Tue 28. So Tuesday 28.", "17 + 11 = 28. اليوم: بعد 7 أيام الجمعة 24 ثم 4 أيام: السبت 25 والأحد 26 والاثنين 27 والثلاثاء 28. إذن الثلاثاء 28.", "Mardi 28."), C({17: B, 24: O, 28: R}, "E12"), F("17 + 11 = 28 → Tuesday 28")]),
    _ex("13", "Error detective: 'April 14 is a Wednesday, because 1 is a Wednesday.' What went wrong?", "المحقق: «14 نيسان أربعاء لأن 1 أربعاء». ما الخطأ؟", "Détective : « le 14 est mercredi car le 1 l'est ».", [T("The learner forgot that only 7, 14, 21 ... days later give the SAME weekday. 14 is 13 days after 1, not 14. The Wednesdays are 1, 8, 15. So 14 is the day before Wednesday 15: Tuesday.", "نسي المتعلّم أن اليوم نفسه يتكرر بعد 7 و14 و21 يومًا فقط. 14 بعد 1 بـ 13 يومًا لا 14. أيام الأربعاء 1 و8 و15 فإن 14 هو الثلاثاء قبل الأربعاء 15.", "14 = mardi (veille du mercredi 15)."), C({15: B, 14: R}, "E13"), F("14 is a Tuesday")]),
]
