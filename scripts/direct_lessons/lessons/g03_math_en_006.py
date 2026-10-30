"""Grade 3 Mathematics — Finding Information."""
from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.draw import table, bars

LESSON_ID = "G03-MATH-EN-006"
GRADE = 3
SUBJECT = "math"
TITLES = {"en": "Finding Information", "ar": "البحث عن المعلومات", "fr": "Trouver l'information"}


def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}


LIB = (["Books", "Number"], [["Stories", 46], ["Animals", 38], ["Science", 29], ["Sports", 17]])
SHOP = (["Item", "Price"], [["Sandwich", "3"], ["Juice", "2"], ["Apple", "1"], ["Cake", "4"]])
PETS = (["Cats", "Dogs", "Birds", "Fish"], [7, 9, 4, 6])

QUIZ = [
    {"q": "A table shows Stories 46, Animals 38, Science 29, Sports 17. How many Science books are there?", "opts": ["29", "46", "38", "17"], "a": 0,
     "why": {"46": _w("46 is the number of Stories books.", "46 عدد كتب القصص.", "46 = Stories."),
             "38": _w("38 is the number of Animals books.", "38 عدد كتب الحيوانات.", "38 = Animals."),
             "17": _w("17 is the number of Sports books.", "17 عدد كتب الرياضة.", "17 = Sports.")}, "ok": "29"},
    {"q": "Lina bought 3 apples for 6 coins. She is 8 years old. How much does one apple cost? Which information do we NOT need?", "opts": ["Her age, 8", "The 3 apples", "The 6 coins", "Nothing is extra"], "a": 0,
     "why": {"The 3 apples": _w("We need it: 6 coins for 3 apples.", "نحتاجه: 6 قطع لثلاث تفاحات.", "Nécessaire."),
             "The 6 coins": _w("We need the price paid.", "نحتاج المبلغ المدفوع.", "Nécessaire."),
             "Nothing is extra": _w("Her age has nothing to do with the price.", "عمرها لا علاقة له بالثمن.", "L'âge est inutile.")}, "ok": "Her age, 8"},
    {"q": "Sami has some marbles. He gives 5 away. How many are left?", "opts": ["We cannot know: the starting number is missing", "5", "0", "10"], "a": 0,
     "why": {"5": _w("5 is what he gave away, not what is left.", "5 ما أعطاه لا ما بقي.", "5 est donné."),
             "0": _w("We have no evidence he gave all.", "لا دليل أنه أعطى الكل.", "Pas de preuve."),
             "10": _w("Nothing in the text says 10.", "لا شيء يدل على 10.", "Rien ne dit 10.")}, "ok": "We cannot know: the starting number is missing"},
]

THEORY = [
    ("Read the question first", "اقرأ السؤال أولًا", "Lire d'abord la question", "22", [
        T("Hello, champion! Before looking for numbers, ask: what does the question want? Here is a table of the school library. If the question is 'How many Science books are there?', the key words are 'Science' and 'how many'. We look for the row called Science, then read its number: 29.",
          "مرحبًا يا بطل! قبل البحث عن الأعداد اسأل: ماذا يريد السؤال؟ هذا جدول مكتبة المدرسة. إذا كان السؤال «كم كتاب علوم؟» فالكلمات المهمة «علوم» و«كم». نبحث عن سطر العلوم ثم نقرأ عدده: 29.",
          "Que demande la question ? « Combien de livres de sciences ? » → ligne Science : 29."),
        table(LIB[0], LIB[1], hi=[(2, 1)], tag="T1"),
        F("Science → 29"),
        T("Tip: underline the key words of the question with your finger, then find the same word on the table. The answer is right next to it.",
          "نصيحة: ضع إصبعك تحت الكلمات المهمة في السؤال ثم جد الكلمة نفسها في الجدول. الجواب بجانبها مباشرة.",
          "Souligne les mots clés puis cherche-les dans le tableau."),
    ]),
    ("Locate the evidence in a table", "جد الدليل في الجدول", "Repérer la preuve dans un tableau", "22", [
        T("A table has rows and columns. To read one value, find the row (the name) and the column (what is measured), and read the box where they meet. In the canteen price list, the Cake row and the Price column meet at 4. So a cake costs 4.",
          "للجدول سطور وأعمدة. لقراءة قيمة نجد السطر (الاسم) والعمود (ما نقيسه) ونقرأ الخانة التي يلتقيان فيها. في لائحة أسعار المقصف يلتقي سطر الكعكة وعمود السعر عند 4. إذن ثمن الكعكة 4.",
          "Ligne Cake, colonne Price : 4."),
        table(SHOP[0], SHOP[1], hi=[(3, 1)], tag="T2"),
        F("Cake → 4"),
        T("Questions can use two pieces of evidence. 'What do a sandwich and a juice cost together?' Find both: 3 and 2. Then add: 3 + 2 = 5. Show where each number came from, then calculate.",
          "قد يحتاج السؤال إلى دليلين. «كم ثمن شطيرة وعصير معًا؟» نجد الاثنين: 3 و2 ثم نجمع: 3 + 2 = 5. نبيّن من أين جاء كل عدد ثم نحسب.",
          "Sandwich + juice : 3 + 2 = 5."),
        table(SHOP[0], SHOP[1], hi=[(0, 1), (1, 1)], tag="T2b"),
        F("3 + 2 = 5"),
    ]),
    ("Read a bar chart", "اقرأ المخطط بالأعمدة", "Lire un diagramme en bâtons", "23", [
        T("A chart tells the numbers with bars. Here are the pets of the children in class 3A. The taller the bar, the greater the number. The tallest bar is Dogs: 9. The shortest is Birds: 4. To read a value, follow the top of the bar across to the numbers on the side.",
          "المخطط يبيّن الأعداد بأعمدة. هذه الحيوانات الأليفة عند أطفال الصف 3أ. كلما كان العمود أطول كان العدد أكبر. أطول عمود الكلاب: 9 وأقصرها الطيور: 4. لقراءة قيمة تتبع رأس العمود إلى الأعداد على الجانب.",
          "Plus la barre est haute, plus le nombre est grand : chiens 9, oiseaux 4."),
        bars(PETS[0], PETS[1], tag="B1", ymax=10, title="Pets in class 3A"),
        F("Cats 7   Dogs 9   Birds 4   Fish 6"),
        T("Questions from the chart: How many more dogs than cats? 9 − 7 = 2. How many pets in all? 7 + 9 + 4 + 6 = 26. Always say which bars you used.",
          "أسئلة من المخطط: كم كلبًا أكثر من القطط؟ 9 − 7 = 2. كم حيوانًا في المجموع؟ 7 + 9 + 4 + 6 = 26. قل دائمًا أي الأعمدة استعملت.",
          "Chiens − chats : 9 − 7 = 2 ; total : 7 + 9 + 4 + 6 = 26."),
        F("9 − 7 = 2        7 + 9 + 4 + 6 = 26"),
    ]),
    ("Useful and useless details", "معلومات مفيدة وأخرى زائدة", "Informations utiles et inutiles", "23", [
        T("A story problem may hide details we do not need. 'Lina bought 3 apples for 6 coins. She is 8 years old and her bag is red. How much does 1 apple cost?' Useful: 3 apples, 6 coins. Useless: her age and the colour of the bag. Calculate 6 ÷ 3 = 2 coins, or think: 2 + 2 + 2 = 6.",
          "قد تحمل المسألة تفاصيل لا نحتاجها. «اشترت لينا 3 تفاحات بـ 6 قطع. عمرها 8 سنوات وحقيبتها حمراء. كم ثمن تفاحة؟» المفيد: 3 تفاحات و6 قطع. الزائد: عمرها ولون الحقيبة. 6 ÷ 3 = 2 قطعتان، أو نفكر: 2 + 2 + 2 = 6.",
          "Utile : 3 pommes, 6 pièces. Inutile : âge, couleur du sac. 6 ÷ 3 = 2."),
        F("useful: 3 apples, 6 coins      useless: age 8, red bag"),
        F("one apple costs 2 coins   (2 + 2 + 2 = 6 ✓)"),
        T("Error detective! A learner adds all the numbers: 3 + 6 + 8 = 17. But 17 does not answer 'the price of one apple'. Ask: does this number help answer THIS question?",
          "المحقق! جمع متعلّم كل الأعداد: 3 + 6 + 8 = 17. لكن 17 لا تجيب عن «ثمن تفاحة». اسأل: هل يساعد هذا العدد في الجواب عن هذا السؤال؟",
          "Il additionne tout : 17. Mais 17 ne répond pas à la question."),
    ]),
    ("When information is missing", "حين تنقص المعلومة", "Quand il manque une information", "23", [
        T("Sometimes the problem does not give enough. 'Sami gives away 5 marbles. How many are left?' We do not know how many he had at first. We cannot answer. A good mathematician says: the starting number is missing. If the text adds 'He had 12', then 12 − 5 = 7.",
          "أحيانًا لا تعطي المسألة ما يكفي. «أعطى سامي 5 كرات. كم بقي؟» لا نعرف كم كان عنده. لا يمكن الجواب. يقول الرياضي الجيد: ينقص العدد الأول. وإذا قال النص «كان عنده 12» فإن 12 − 5 = 7.",
          "Il manque le nombre de départ. Avec 12 : 12 − 5 = 7."),
        F("12 − 5 = 7      (only when 12 is given)"),
        T("Rule: never invent a number that the text or the picture does not give. Ask first: do I have all the evidence I need?",
          "قاعدة: لا تخترع عددًا لا يعطيه النص أو الصورة. اسأل أولًا: هل عندي كل الأدلة التي أحتاجها؟",
          "N'invente jamais un nombre."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("ASK → LOCATE → SELECT → ANSWER → VERIFY. Read what the question asks. Find the matching row, column or bar. Keep only the useful numbers. Calculate if needed. Check that the answer fits the question and say where it came from.",
          "اسأل ← جد ← اختر ← أجب ← تحقق. اقرأ ما يطلبه السؤال. جد السطر أو العمود أو العمود البياني المناسب. احتفظ بالأعداد المفيدة فقط. احسب إن لزم. تحقق أن الجواب يناسب السؤال وقل من أين أتى.",
          "Question → repérer → choisir → répondre → vérifier."),
        F("ASK → LOCATE → SELECT → ANSWER → VERIFY"),
    ]),
]


def _ex(n, en, ar, fr, steps):
    return EX(n, "", st(en, ar, fr), steps)


def L(hi, tag): return table(LIB[0], LIB[1], hi=hi, tag=tag)
def S(hi, tag): return table(SHOP[0], SHOP[1], hi=hi, tag=tag)
def P(tag): return bars(PETS[0], PETS[1], tag=tag, ymax=10, title="Pets in class 3A")


EXERCISES = [
    _ex("1", "Library table (Stories 46, Animals 38, Science 29, Sports 17): how many Animals books?", "جدول المكتبة (قصص 46، حيوانات 38، علوم 29، رياضة 17): كم كتاب حيوانات؟", "Combien de livres d'animaux ?", [T("Find the row Animals and read its number.", "نجد سطر الحيوانات ونقرأ عدده.", "Ligne Animals."), L([(1, 1)], "E1"), F("38")]),
    _ex("2", "Which kind of book is the most numerous? The least?", "أي نوع من الكتب هو الأكثر؟ وأيها الأقل؟", "Quel type est le plus nombreux ? le moins ?", [T("Compare 46, 38, 29, 17. The greatest is 46 (Stories). The smallest is 17 (Sports).", "نقارن 46 و38 و29 و17. الأكبر 46 (قصص) والأصغر 17 (رياضة).", "Stories (46) ; Sports (17)."), L([(0, 1), (3, 1)], "E2"), F("most: Stories 46      least: Sports 17")]),
    _ex("3", "How many more Stories books than Sports books?", "كم كتاب قصص أكثر من كتب الرياضة؟", "Combien de livres de contes de plus que de sport ?", [T("Evidence: 46 and 17. 'How many more' means subtract: 46 − 17 = 29.", "الدليل: 46 و17. «كم أكثر» يعني الطرح: 46 − 17 = 29.", "46 − 17 = 29."), L([(0, 1), (3, 1)], "E3"), F("46 − 17 = 29      check: 17 + 29 = 46 ✓")]),
    _ex("4", "How many Animals and Science books together?", "كم كتاب حيوانات وعلوم معًا؟", "Combien de livres d'animaux et de sciences ensemble ?", [T("Evidence: 38 and 29. Together means add: 38 + 29 = 67 (38 + 30 = 68, minus 1).", "الدليل: 38 و29. «معًا» تعني الجمع: 38 + 29 = 67 (38 + 30 = 68 ناقص 1).", "67."), L([(1, 1), (2, 1)], "E4"), F("38 + 29 = 67")]),
    _ex("5", "How many books does the library have in all?", "كم كتابًا في المكتبة كلها؟", "Combien de livres en tout ?", [T("Add all four numbers: 46 + 38 = 84; 29 + 17 = 46; 84 + 46 = 130.", "نجمع الأعداد الأربعة: 46 + 38 = 84؛ 29 + 17 = 46؛ 84 + 46 = 130.", "130."), L([(0, 1), (1, 1), (2, 1), (3, 1)], "E5"), F("46 + 38 + 29 + 17 = 130")]),
    _ex("6", "Canteen prices (Sandwich 3, Juice 2, Apple 1, Cake 4). Layla buys a cake and an apple. What does she pay?", "أسعار المقصف (شطيرة 3، عصير 2، تفاحة 1، كعكة 4). اشترت ليلى كعكة وتفاحة. كم تدفع؟", "Layla achète un gâteau et une pomme. Combien paie-t-elle ?", [T("Evidence: cake 4, apple 1. 4 + 1 = 5.", "الدليل: كعكة 4 وتفاحة 1. 4 + 1 = 5.", "5."), S([(3, 1), (2, 1)], "E6"), F("4 + 1 = 5")]),
    _ex("7", "Omar pays with 10 coins for a sandwich. How much change?", "دفع عمر 10 قطع ثمن شطيرة. كم يعود إليه؟", "Omar paie 10 pour un sandwich. Combien lui rend-on ?", [T("The sandwich costs 3 (from the table). 10 − 3 = 7. Check: 3 + 7 = 10 ✓.", "الشطيرة بـ 3 (من الجدول). 10 − 3 = 7. تحقق: 3 + 7 = 10 ✓.", "10 − 3 = 7."), S([(0, 1)], "E7"), F("10 − 3 = 7")]),
    _ex("8", "How many sandwiches can you buy with 9 coins?", "كم شطيرة نشتري بـ 9 قطع؟", "Combien de sandwichs avec 9 pièces ?", [T("One sandwich costs 3. 3, 6, 9: three sandwiches (3 × 3 = 9).", "ثمن الشطيرة 3. 3 و6 و9: ثلاث شطائر (3 × 3 = 9).", "3 sandwichs."), S([(0, 1)], "E8"), F("9 ÷ 3 = 3")]),
    _ex("9", "Pets chart (Cats 7, Dogs 9, Birds 4, Fish 6): which pet is chosen by exactly 6 children?", "مخطط الحيوانات (قطط 7، كلاب 9، طيور 4، أسماك 6): أي حيوان اختاره 6 أطفال بالضبط؟", "Quel animal est choisi par 6 enfants ?", [T("Find the bar whose top is at 6: Fish.", "نبحث عن العمود الذي يصل إلى 6: الأسماك.", "Fish."), P("E9"), F("Fish")]),
    _ex("10", "How many more dogs than birds? How many children in all?", "كم كلبًا أكثر من الطيور؟ وكم طفلًا في المجموع؟", "Combien de chiens de plus que d'oiseaux ? Combien d'enfants ?", [T("9 − 4 = 5 more dogs. In all: 7 + 9 + 4 + 6 = 26 (7 + 9 = 16; 4 + 6 = 10; 16 + 10 = 26).", "9 − 4 = 5 كلاب أكثر. في المجموع: 7 + 9 + 4 + 6 = 26 (7 + 9 = 16؛ 4 + 6 = 10؛ 16 + 10 = 26).", "5 de plus ; 26 en tout."), P("E10"), F("9 − 4 = 5        7 + 9 + 4 + 6 = 26")]),
    _ex("11", "Which information is useless? 'Ali has 12 pencils in a blue box. His sister is 6. He gives 4 pencils to a friend. How many pencils does Ali have now?'", "أي معلومة زائدة؟ «عند علي 12 قلمًا في علبة زرقاء. أخته عمرها 6. أعطى صديقه 4 أقلام. كم قلمًا عنده الآن؟»", "Quelle information est inutile ? Ali a 12 crayons dans une boîte bleue, sa sœur a 6 ans, il en donne 4.", [T("Useful: 12 pencils and 4 given away. Useless: the blue box and the sister's age 6. Calculation: 12 − 4 = 8.", "المفيد: 12 قلمًا و4 أعطاها. الزائد: العلبة الزرقاء وعمر الأخت 6. العملية: 12 − 4 = 8.", "Inutile : boîte bleue, âge 6. 12 − 4 = 8."), F("12 − 4 = 8      check: 8 + 4 = 12 ✓")]),
    _ex("12", "Can we answer? 'A bus carries 25 children. Some more get on. How many children are on the bus now?'", "هل نستطيع الجواب؟ «تحمل الحافلة 25 طفلًا. صعد بعضهم أيضًا. كم طفلًا في الحافلة الآن؟»", "Peut-on répondre ? « 25 enfants, d'autres montent. »", [T("No. We do not know how many got on. The number is missing. If 9 got on, then 25 + 9 = 34.", "لا. لا نعرف كم صعد. ينقص العدد. لو صعد 9 لكان 25 + 9 = 34.", "Il manque le nombre qui montent."), F("not enough information")]),
    _ex("13", "Error detective: for 'How many Science books?' a learner answers 46. Where is the mistake?", "المحقق: عن «كم كتاب علوم؟» أجاب متعلّم 46. أين الخطأ؟", "Détective : pour « combien de sciences ? » il répond 46.", [T("46 is the first number in the table (Stories). The learner did not match the word Science with its row. The right answer is 29.", "46 هو أول عدد في الجدول (قصص). لم يطابق المتعلّم كلمة علوم مع سطرها. الجواب الصحيح 29.", "46 = Stories. Bonne réponse : 29."), L([(2, 1)], "E13"), F("29")]),
]
