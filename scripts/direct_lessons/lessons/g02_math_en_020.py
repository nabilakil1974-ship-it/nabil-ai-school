"""Grade 2 Mathematics — Problems (3)."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G02-MATH-EN-020"
GRADE = 2
SUBJECT = "math"
TITLES = {"en": "Problems (3)", "ar": "مسائل (3)", "fr": "Problèmes (3)"}


def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}


QUIZ = [
    {"q": "A box has 68 apples. Fadi takes 32. How many apples are left?",
     "opts": ["36", "100", "32", "46"], "a": 0,
     "why": {"100": _w("Fadi takes apples away, so we subtract. We do not add.", "فادي يأخذ تفاحًا فنطرح ولا نجمع.", "Fadi enlève des pommes : on soustrait, on n'additionne pas."),
             "32": _w("32 is the number taken, not the number left.", "32 هو ما أُخذ لا ما بقي.", "32 est ce qui est pris, pas ce qui reste."),
             "46": _w("Check: 46 + 32 = 78, not 68.", "نتحقق: 46 + 32 = 78 وليس 68.", "Vérification : 46 + 32 = 78, pas 68.")},
     "ok": "68 − 32 = 36"},
    {"q": "Maya has 54 chocolates and gives away 53. How many are left?",
     "opts": ["1", "0", "107", "2"], "a": 0,
     "why": {"0": _w("54 − 53 leaves 1, not 0.", "54 − 53 يبقى 1 وليس 0.", "54 − 53 il reste 1, pas 0."),
             "107": _w("She gives chocolates away, so we subtract.", "هي تعطي الشوكولا فنطرح.", "Elle donne des chocolats : on soustrait."),
             "2": _w("Check: 2 + 53 = 55, not 54.", "نتحقق: 2 + 53 = 55 وليس 54.", "Vérification : 2 + 53 = 55, pas 54.")},
     "ok": "54 − 53 = 1"},
    {"q": "Counting by twos: 14, 16, 18, 20, ... What comes next?",
     "opts": ["22", "21", "24", "30"], "a": 0,
     "why": {"21": _w("Counting by twos adds 2 each time: 20 + 2 = 22.", "العدّ بالاثنين يضيف 2 كل مرة: 20 + 2 = 22.", "On ajoute 2 à chaque fois : 20 + 2 = 22."),
             "24": _w("That skips 22. Do not jump over a number.", "هذا يقفز عن 22. لا نتخطى عددًا.", "On saute 22. On ne saute pas de nombre."),
             "30": _w("That adds 10, not 2.", "هذا يضيف 10 لا 2.", "C'est +10, pas +2.")},
     "ok": "20 + 2 = 22"},
]

THEORY = [
    ("\"Left\" asks what remains", "«بقي» تسأل عمّا تبقّى", "« Il reste » demande ce qui reste", "46", [
        T("Hello, champion! In these stories we ask three things: what was the whole, what was taken away, and what is left? A box has 68 apples and Fadi takes 32. The whole is 68, taken is 32, and we want what is left. We subtract: 68 − 32 = 36. Check by adding back: 36 + 32 = 68. There are 36 apples left.",
          "مرحبًا يا بطل! في هذه القصص نسأل ثلاثة أشياء: ما هو الكل؟ ماذا أُخذ؟ وماذا بقي؟ في الصندوق 68 تفاحة وفادي أخذ 32. الكل هو 68 والمأخوذ 32 ونريد الباقي. نطرح: 68 − 32 = 36. نتحقق بالجمع: 36 + 32 = 68. بقيت 36 تفاحة.",
          "Bonjour, champion ! Dans ces histoires on demande : quel est le tout, qu'est-ce qu'on enlève, et que reste-t-il ? Une boîte a 68 pommes, Fadi en prend 32. Le tout est 68, on enlève 32. On soustrait : 68 − 32 = 36. Vérification : 36 + 32 = 68. Il reste 36 pommes."),
        F("68 − 32 = 36      check: 36 + 32 = 68"),
    ]),
    ("Same structure, different stories", "البنية نفسها في قصص مختلفة", "Même structure, histoires différentes", "46", [
        T("Flowers, marbles, chocolates and a bus all have the same shape: start, remove, left. Mother buys 48 flowers and gives 25 away: 48 − 25 = 23. We always write the whole first, then take away. 25 − 48 would be wrong.",
          "الأزهار والبلايا والشوكولا والحافلة كلها بالشكل نفسه: البداية ثم ما أُخذ ثم الباقي. الأم تشتري 48 زهرة وتعطي 25: 48 − 25 = 23. نكتب الكل أولًا ثم نطرح. أما 25 − 48 فخطأ.",
          "Fleurs, billes, chocolats, autobus : même forme : départ, on enlève, il reste. Maman achète 48 fleurs et en donne 25 : 48 − 25 = 23. On écrit le tout d'abord. 25 − 48 serait faux."),
        F("start → remove → left      48 − 25 = 23"),
    ]),
    ("A path with a condition", "طريق له شرط", "Un chemin avec une condition", "47", [
        T("In the rabbit puzzle the rabbit must reach the carrot without passing in front of a triangle. Look for the triangles first. Try a route through the free spaces. After every move ask: does this move break the rule? If it does, choose another way. A good path starts at the rabbit, ends at the carrot, and never crosses a colored shape.",
          "في لغز الأرنب يجب أن يصل الأرنب إلى الجزرة دون أن يمر أمام مثلث. نبحث أولًا عن المثلثات. نجرّب طريقًا في المساحات الحرة. وبعد كل خطوة نسأل: هل تخالف هذه الخطوة الشرط؟ إذا خالفته نختار طريقًا آخر. الطريق الجيد يبدأ من الأرنب وينتهي عند الجزرة ولا يعبر أي شكل ملوّن.",
          "Dans le jeu du lapin, il doit atteindre la carotte sans passer devant un triangle. On repère d'abord les triangles, on essaie un chemin dans les espaces libres, et après chaque pas on demande : ce pas brise-t-il la règle ? Si oui, on change. Un bon chemin part du lapin, arrive à la carotte et ne traverse aucune forme colorée."),
    ]),
    ("Counting by twos", "العدّ بالاثنين", "Compter de deux en deux", "47", [
        T("Counting by twos means adding 2 each step: 4, 6, 8, 10, 12, 14. In the dot picture we do not join the nearest dot. We join the next label, 2 more than the one before. The numbers go 4, 6, 8 and so on up to 84.",
          "العدّ بالاثنين يعني أن نضيف 2 في كل خطوة: 4 ثم 6 ثم 8 ثم 10 ثم 12 ثم 14. في لوحة النقاط لا نصل أقرب نقطة بل النقطة التي رقمها أكبر بـ2. تسير الأعداد 4 و6 و8 وهكذا حتى 84.",
          "Compter de deux en deux, c'est ajouter 2 à chaque pas : 4, 6, 8, 10, 12, 14. Dans le dessin à points, on ne relie pas le point le plus proche mais le suivant, 2 de plus. Les nombres vont 4, 6, 8 ... jusqu'à 84."),
        F("4 → 6 → 8 → 10 → 12 → 14 → ... → 84      each step: +2"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("In stories: whole, remove, left, check. In the rabbit path: look at the condition, test each move, reject bad moves, reach the goal. With dots: read the label, add 2, connect, check.",
          "في القصص: الكل ثم نطرح ثم الباقي ثم نتحقق. في طريق الأرنب: ننظر إلى الشرط ونختبر كل خطوة ونرفض الخطوات الخاطئة ونصل إلى الهدف. في النقاط: نقرأ الرقم ونضيف 2 ونصل ونتحقق.",
          "Dans les histoires : tout, on enlève, reste, vérification. Pour le lapin : regarder la condition, tester chaque pas, refuser les mauvais pas, atteindre le but. Avec les points : lire le nombre, ajouter 2, relier, vérifier."),
        F("WHOLE → REMOVE → LEFT → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "46", st("A box has 68 apples. Fadi takes 32. How many apples are left?",
                     "في الصندوق 68 تفاحة. أخذ فادي 32. كم تفاحة بقيت؟",
                     "Une boîte contient 68 pommes. Fadi en prend 32. Combien en reste-t-il ?"), [
        F("68 − 32 = 36      check: 36 + 32 = 68"),
        T("There are 36 apples left.", "بقيت 36 تفاحة.", "Il reste 36 pommes."),
    ]),
    EX("2", "46", st("Mother buys 48 flowers and gives 25 to Dida. How many flowers does she have left?",
                     "اشترت الأم 48 زهرة وأعطت دِيدا 25. كم زهرة بقيت معها؟",
                     "Maman achète 48 fleurs et en donne 25 à Dida. Combien lui en reste-t-il ?"), [
        F("48 − 25 = 23      check: 23 + 25 = 48"),
        T("She has 23 flowers left.", "بقي معها 23 زهرة.", "Il lui reste 23 fleurs."),
    ]),
    EX("3", "46", st("There are 56 marbles. Ziad takes 25. How many marbles are left?",
                     "هناك 56 بلية. أخذ زياد 25. كم بلية بقيت؟",
                     "Il y a 56 billes. Ziad en prend 25. Combien en reste-t-il ?"), [
        F("56 − 25 = 31      check: 31 + 25 = 56"),
        T("There are 31 marbles left.", "بقيت 31 بلية.", "Il reste 31 billes."),
    ]),
    EX("4", "46", st("Maya has 54 chocolates and gives away 53. How many chocolates are left?",
                     "عند مايا 54 قطعة شوكولا وقد وزّعت 53. كم قطعة بقيت؟",
                     "Maya a 54 chocolats et en distribue 53. Combien lui en reste-t-il ?"), [
        F("54 − 53 = 1      check: 1 + 53 = 54"),
        T("She has 1 chocolate left.", "بقيت معها قطعة شوكولا واحدة.", "Il lui reste 1 chocolat."),
    ]),
    EX("5", "46", st("48 persons are on a bus going to Tripoli. 26 get off in Byblos. How many persons are left on the bus?",
                     "في الحافلة المتجهة إلى طرابلس 48 شخصًا. نزل 26 في جبيل. كم شخصًا بقي في الحافلة؟",
                     "48 personnes sont dans un autobus vers Tripoli. 26 descendent à Byblos. Combien en reste-t-il dans l'autobus ?"), [
        F("48 − 26 = 22      check: 22 + 26 = 48"),
        T("There are 22 persons left on the bus.", "بقي 22 شخصًا في الحافلة.", "Il reste 22 personnes dans l'autobus."),
    ]),
    EX("6", "47", st("Which path can the rabbit take to reach the carrot without passing in front of a triangle?",
                     "أي طريق يسلكه الأرنب ليصل إلى الجزرة دون أن يمر أمام مثلث؟",
                     "Quel chemin le lapin peut-il prendre pour atteindre la carotte sans passer devant un triangle ?"), [
        T("Find the triangles first. Draw a route from the rabbit through the free spaces. Check each move against the rule, and never cross a colored shape. The route must end at the carrot.",
          "نجد المثلثات أولًا. نرسم طريقًا من الأرنب عبر المساحات الحرة. نختبر كل خطوة بالنسبة إلى الشرط ولا نعبر أي شكل ملوّن. يجب أن ينتهي الطريق عند الجزرة.",
          "On repère d'abord les triangles. On trace un chemin depuis le lapin dans les espaces libres, on teste chaque pas avec la règle, sans traverser de forme colorée. Le chemin finit à la carotte."),
    ]),
    EX("7", "47", st("Join the dots by counting by twos, starting at 4.",
                     "صِل النقاط بالعدّ بالاثنين بدءًا من 4.",
                     "Relie les points en comptant de deux en deux à partir de 4."), [
        F("4 → 6 → 8 → 10 → 12 → 14 → 16 → 18 → 20"),
        T("Always join the next label, 2 more than the one before. For example 20 goes to 22, never straight to 24. The numbers continue up to 84.",
          "نصل دائمًا الرقم التالي الذي هو أكبر بـ2. مثلًا 20 إلى 22 وليس مباشرة إلى 24. وتستمر الأعداد حتى 84.",
          "On relie toujours le nombre suivant, 2 de plus. Par exemple 20 va à 22, jamais directement à 24. Les nombres continuent jusqu'à 84."),
    ]),
    EX("8", "", st("(our own) A bag has 75 cards. 24 are given away. How many cards are left?",
                   "(من عندنا) في الكيس 75 بطاقة. أُعطيت 24. كم بطاقة بقيت؟",
                   "(notre exemple) Un sac contient 75 cartes. On en donne 24. Combien en reste-t-il ?"), [
        F("75 − 24 = 51      check: 51 + 24 = 75"),
        T("There are 51 cards left.", "بقيت 51 بطاقة.", "Il reste 51 cartes."),
    ]),
]
