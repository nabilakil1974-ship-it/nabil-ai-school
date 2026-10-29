"""Grade 2 Mathematics — Finding Information."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G02-MATH-EN-009"
GRADE = 2
SUBJECT = "math"
TITLES = {"en": "Finding Information", "ar": "إيجاد المعلومات", "fr": "Trouver les informations"}


def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}


QUIZ = [
    {"q": "Sami put 3 red balls. Dalia put 32 red balls. Who put the greatest number of red balls?", "opts": ["Dalia", "Sami", "Both the same", "Maya"], "a": 0,
     "why": {"Sami": _w("3 is less than 32.", "3 أقل من 32.", "3 est plus petit que 32."),
             "Both the same": _w("3 and 32 are different.", "3 و32 مختلفان.", "3 et 32 sont différents."),
             "Maya": _w("Maya put yellow balls. Filter red first.", "مايا وضعت كرات صفراء. نصفّي الأحمر أولًا.", "Maya a mis des boules jaunes. Filtre le rouge d'abord.")}, "ok": "32 > 3"},
    {"q": "Ziad has 34 marbles. Makram has 5 marbles more than Ziad. How many does Makram have?", "opts": ["39", "5", "29", "34"], "a": 0,
     "why": {"5": _w("5 is only the extra amount, not Makram's total.", "5 هو الزيادة فقط وليس مجموع مكرم.", "5 est seulement la différence."),
             "29": _w("More than means add: 34 + 5.", "أكثر من يعني نجمع: 34 + 5.", "Plus que : on ajoute."),
             "34": _w("That is Ziad's amount.", "هذا عدد زياد.", "C'est le nombre de Ziad.")}, "ok": "34 + 5 = 39"},
    {"q": "Rami has 22 marbles. Bassem has as many marbles as Rami. How many does Bassem have?", "opts": ["22", "44", "0", "21"], "a": 0,
     "why": {"44": _w("As many as means the same number, not double.", "بقدر ما عند يعني العدد نفسه لا الضعف.", "Autant que : le même nombre."),
             "0": _w("Bassem has the same as Rami.", "عند باسم مثل رامي.", "Autant que Rami."),
             "21": _w("It is equal, not one less.", "متساوٍ لا أقل بواحد.", "Égal, pas un de moins.")}, "ok": "22"},
]

THEORY = [
    ("Find what the question asks", "ابحث عمّا يطلبه السؤال", "Trouve ce que la question demande", "28", [
        T("Hello, champion! Not every question needs a new calculation. Sometimes the answer is right in front of us, but we must know where to look. Our rule: read the question, find the name, number or colour, use only the information we need, answer, and check.",
          "مرحبًا يا بطل! ليس كل سؤال يحتاج حسابًا جديدًا. أحيانًا يكون الجواب أمامنا لكن علينا أن نعرف أين نبحث. قاعدتنا: نقرأ السؤال، نجد الاسم أو العدد أو اللون، نستعمل المعلومة اللازمة فقط، نجيب، ونتحقق.",
          "Bonjour champion ! Toutes les questions ne demandent pas un calcul. Parfois la réponse est devant nous, il faut savoir où chercher. Règle : lire la question, trouver le nom, le nombre ou la couleur, n'utiliser que ce qui sert, répondre, vérifier."),
        T("Look at the tree. Sami put 3 red balls, Dani 16 yellow, Dalia 32 red, Maya 23 yellow. If the question is how many balls Dani put, we look for Dani and find 16. We do not need the other numbers.",
          "انظر إلى الشجرة. سامي وضع 3 كرات حمراء وداني 16 صفراء ودالية 32 حمراء ومايا 23 صفراء. إذا سألنا كم كرة وضع داني نبحث عن داني فنجد 16. لا نحتاج الأعداد الأخرى.",
          "Regarde le sapin. Sami : 3 rouges, Dani : 16 jaunes, Dalia : 32 rouges, Maya : 23 jaunes. Combien de boules pour Dani ? On cherche Dani : 16."),
        F("Sami 3 red   Dani 16 yellow   Dalia 32 red   Maya 23 yellow"),
    ]),
    ("Filter, then compare", "نصفّي ثم نقارن", "Filtrer puis comparer", "28", [
        T("Look at the difference between two questions: who put the greatest number of balls, and who put the greatest number of red balls? The second needs a filter first: keep only red, Sami 3 and Dalia 32, then compare: 32 > 3, so Dalia. For yellow, 16 and 23: the smallest is 16, so Dani.",
          "لاحظ الفرق بين سؤالين: من وضع أكبر عدد من الكرات؟ ومن وضع أكبر عدد من الكرات الحمراء؟ الثاني يحتاج تصفية أولًا: نأخذ الأحمر فقط سامي 3 ودالية 32 ثم نقارن: 32 > 3 إذن دالية. وللأصفر 16 و23: الأصغر 16 إذن داني.",
          "Deux questions différentes : le plus grand nombre de boules, ou de boules rouges ? La seconde demande de filtrer : rouges seulement, Sami 3 et Dalia 32, 32 > 3 donc Dalia. Jaunes : 16 et 23, le plus petit est 16, Dani."),
        F("FILTER → COMPARE"),
        F("red: 3 < 32      yellow: 16 < 23"),
    ]),
    ("Information we must work out", "معلومات علينا استنتاجها", "Informations à déduire", "29", [
        T("Some information is written directly and some we must work out. Ziad has 34 marbles. Makram has 5 more than Ziad, so Makram has 34 + 5 = 39. Bassem has as many as Rami. Rami has 22, so Bassem has 22.",
          "بعض المعلومات مكتوبة مباشرة وبعضها نستنتجه. عند زياد 34 بلية. ومكرم عنده 5 أكثر من زياد إذن 34 + 5 = 39. وباسم عنده بقدر رامي. عند رامي 22 إذن عند باسم 22.",
          "Certaines informations sont écrites, d'autres se déduisent. Ziad : 34. Makram a 5 de plus : 34 + 5 = 39. Bassem a autant que Rami : 22."),
        F("Ziad 34   Rami 22   Makram 34 + 5 = 39   Bassem = Rami = 22"),
        T("More than means we add to the other amount. As many as means exactly the same amount. The 5 is not Makram's total. It is only how many more he has.",
          "أكثر من تعني أننا نضيف إلى الكمية الأخرى. وبقدر ما عند تعني الكمية نفسها تمامًا. والعدد 5 ليس مجموع مكرم، بل هو الزيادة فقط.",
          "Plus que : on ajoute. Autant que : la même quantité. Le 5 n'est pas le total de Makram, c'est seulement la différence."),
    ]),
    ("Answer only what is asked", "نجيب عمّا سُئلنا فقط", "Répondre seulement à la question", "29", [
        T("Answer exactly the type of thing the question asks for. What is the colour of Dani's balls? Yellow. Who put 23 yellow balls? Maya. How many did Dalia put? 32. And give a reason with yes or no questions: no, because 22 < 34.",
          "نجيب بنوع الجواب المطلوب تمامًا. ما لون كرات داني؟ أصفر. من وضع 23 كرة صفراء؟ مايا. كم وضعت دالية؟ 32. ونعلّل في أسئلة نعم أو لا: لا لأن 22 < 34.",
          "On répond au type de réponse demandé. Couleur des boules de Dani ? Jaune. Qui a mis 23 boules jaunes ? Maya. Combien Dalia ? 32. Pour oui/non, on explique : non, car 22 < 34."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Read the question first. Decide if you need a name, a number, a colour or a comparison. Filter if the question is about one group. More than means add; as many as means equal. Then answer and check.",
          "نقرأ السؤال أولًا. نحدد هل نريد اسمًا أم عددًا أم لونًا أم مقارنة. نصفّي إذا كان السؤال عن مجموعة معيّنة. أكثر من تعني نجمع؛ وبقدر ما عند تعني متساوٍ. ثم نجيب ونتحقق.",
          "On lit la question, on décide : nom, nombre, couleur ou comparaison. On filtre si la question concerne un groupe. Plus que : on ajoute ; autant que : égal. Puis on répond et on vérifie."),
    ]),
]

EXERCISES = [
    EX("1", "28", st("Tree decoration: Sami 3 red, Dani 16 yellow, Dalia 32 red, Maya 23 yellow. How many balls did Dani put? What colour are Dani's balls? Who put red balls?",
                    "تزيين الشجرة: سامي 3 حمراء وداني 16 صفراء ودالية 32 حمراء ومايا 23 صفراء. كم كرة وضع داني؟ ما لون كرات داني؟ من وضع كرات حمراء؟",
                    "Décoration du sapin : Sami 3 rouges, Dani 16 jaunes, Dalia 32 rouges, Maya 23 jaunes. Combien pour Dani ? Quelle couleur ? Qui a mis des rouges ?"), [
        F("Dani → 16 balls, yellow"),
        F("red: Sami and Dalia"),
    ]),
    EX("2", "28", st("Same tree. Who put the greatest number of red balls? Who put the smallest number of yellow balls? Who put the greatest number of balls?",
                    "الشجرة نفسها. من وضع أكبر عدد من الكرات الحمراء؟ من وضع أصغر عدد من الكرات الصفراء؟ من وضع أكبر عدد من الكرات؟",
                    "Même sapin. Qui a mis le plus de rouges ? Le moins de jaunes ? Le plus de boules en tout ?"), [
        F("red: 3 and 32 → 32 > 3 → Dalia"),
        F("yellow: 16 and 23 → 16 < 23 → Dani"),
        F("all: 3, 16, 32, 23 → greatest 32 → Dalia"),
        T("Who put 23 yellow balls? Maya. Who put 16 balls? Dani.", "من وضع 23 كرة صفراء؟ مايا. من وضع 16 كرة؟ داني.", "Qui a mis 23 boules jaunes ? Maya. Qui en a mis 16 ? Dani."),
    ]),
    EX("3", "29", st("Marbles: Ziad has 34, Rami has 22, Makram has 5 more than Ziad, Bassem has as many as Rami. How many marbles do Makram and Bassem have?",
                    "البلي: عند زياد 34 وعند رامي 22 وعند مكرم 5 أكثر من زياد وعند باسم بقدر رامي. كم بلية عند مكرم وباسم؟",
                    "Billes : Ziad 34, Rami 22, Makram 5 de plus que Ziad, Bassem autant que Rami. Combien pour Makram et Bassem ?"), [
        F("Makram: 34 + 5 = 39"),
        F("Bassem: same as Rami = 22"),
        T("Check: 39 is exactly 5 more than 34.", "تحقق: 39 يزيد 5 بالضبط على 34.", "Vérification : 39 a 5 de plus que 34."),
    ]),
    EX("4", "29", st("Same marbles. Does Rami have more than Ziad? Does Makram have more than Ziad? Does Ziad have more than Bassem? Who has the most?",
                    "البلي نفسه. هل عند رامي أكثر من زياد؟ هل عند مكرم أكثر من زياد؟ هل عند زياد أكثر من باسم؟ من عنده الأكثر؟",
                    "Mêmes billes. Rami a-t-il plus que Ziad ? Makram plus que Ziad ? Ziad plus que Bassem ? Qui en a le plus ?"), [
        F("22 < 34 → No, Rami has fewer than Ziad"),
        F("39 > 34 → Yes, Makram has more than Ziad"),
        F("34 > 22 → Yes, Ziad has more than Bassem"),
        F("34, 22, 39, 22 → greatest 39 → Makram has the most"),
    ]),
    EX("5", "29", st("Lina has 18 stickers, Omar 25, Rana has 4 more than Lina, Tarek has as many as Omar (our own). Who has the most?",
                    "عند لينا 18 ملصقًا وعند عمر 25 وعند رنا 4 أكثر من لينا وعند طارق بقدر عمر (مثالنا). من عنده الأكثر؟",
                    "Lina 18 autocollants, Omar 25, Rana 4 de plus que Lina, Tarek autant qu'Omar (exemple à nous). Qui en a le plus ?"), [
        F("Rana: 18 + 4 = 22      Tarek = Omar = 25"),
        F("18, 25, 22, 25 → greatest 25"),
        T("Omar and Tarek have the most.", "عمر وطارق عندهما الأكثر.", "Omar et Tarek en ont le plus."),
    ]),
]
