"""Grade 2 Mathematics — Addition (1)."""
from scripts.direct_lessons.common import T, F, EX, st, tens, numpath, jumps

LESSON_ID = "G02-MATH-EN-003"
GRADE = 2
SUBJECT = "math"
TITLES = {"en": "Addition (1)", "ar": "الجمع (1)", "fr": "Addition (1)"}

THEORY = [
    ("Addition joins two quantities", "الجمع يضمّ كميتين", "L'addition réunit deux quantités", "16", [
        tens(0, 8, bundled=False, tag="A", eq=True),
        tens(0, 4, bundled=False, tag="B", eq=True),
        T("Hello, champion! Today we do addition, and we start with the meaning. I have 8 objects, and I add 4 more. Did the quantity grow or shrink? It grew. When we join quantities: part + part = total. 8 + 4 = 12. Before writing, we find the first group, the second group, and then the total.",
          "مرحبًا يا بطل! اليوم نتعلم الجمع ونبدأ بالمعنى. عندي 8 أشياء وأضفت 4. هل كبرت الكمية أم صغرت؟ كبرت. عندما نضمّ الكميات: جزء + جزء = المجموع. 8 + 4 = 12. وقبل أن نكتب نحدّد المجموعة الأولى ثم الثانية ثم المجموع.",
          "Bonjour champion ! Aujourd'hui, l'addition, en commençant par le sens. J'ai 8 objets et j'en ajoute 4. La quantité a-t-elle augmenté ? Oui. Quand on réunit : partie + partie = total. 8 + 4 = 12. Avant d'écrire, on repère le premier groupe, le second, puis le total."),
        F("8 + 4 = 12"),
    ]),
    ("Use a fact you know: make ten", "نستعمل حقيقة معروفة: نكمل العشرة", "Utiliser un fait connu : faire dix", "17", [
        T("We could count one by one, but there are smarter ways. We know 7 + 3 = 10, so 7 + 4 is one more: 11. For 8 + 5: 8 needs 2 to make 10, and 5 = 2 + 3, so 8 + 5 = 8 + 2 + 3 = 10 + 3 = 13.",
          "نستطيع العدّ واحدًا واحدًا لكن هناك طرق أذكى. نعرف أن 7 + 3 = 10 فـ 7 + 4 أكبر بواحد: 11. وفي 8 + 5: العدد 8 يحتاج 2 ليصير 10 و5 = 2 + 3 إذن 8 + 5 = 8 + 2 + 3 = 10 + 3 = 13.",
          "On pourrait compter un par un, mais il y a plus malin. On sait 7 + 3 = 10 : 7 + 4 est un de plus : 11. Pour 8 + 5 : 8 a besoin de 2, et 5 = 2 + 3, donc 8 + 5 = 8 + 2 + 3 = 10 + 3 = 13."),
        tens(1, 3, eq=True),
        F("8 + 5 = 8 + 2 + 3 = 10 + 3 = 13"),
    ]),
    ("Find the missing addend", "نجد الحدّ الناقص", "Trouver le terme manquant", "17", [
        F("3 + ___ = 6"),
        T("3 + what = 6? We ask what part completes the total. 3 + 3 = 6, so the missing number is 3. We check: 3 + 3 = 6. Writing 9 would fail the check, because 3 + 9 = 12.",
          "3 + كم = 6؟ نسأل أيّ جزء يكمل المجموع. 3 + 3 = 6 إذن العدد الناقص 3. نتحقق: 3 + 3 = 6. كتابة 9 تفشل في التحقق لأن 3 + 9 = 12.",
          "3 + combien = 6 ? On cherche la partie qui complète le total. 3 + 3 = 6, le nombre manquant est 3. Vérification : 3 + 3 = 6. Écrire 9 échoue : 3 + 9 = 12."),
    ]),
    ("Compare the values", "نقارن القيم", "Comparer les valeurs", "17", [
        F("8 + 7 = 15      8 + 2 = 10      15 > 10"),
        T("To compare 8 + 7 and 8 + 2 we first calculate each side: 15 and 10. 15 > 10, so 8 + 7 > 8 + 2. We compare the values, not the look of the expressions.",
          "لمقارنة 8 + 7 و8 + 2 نحسب أولًا كل طرف: 15 و10. 15 > 10 إذن 8 + 7 > 8 + 2. نقارن القيم لا شكل العبارات.",
          "Pour comparer 8 + 7 et 8 + 2, on calcule d'abord chaque côté : 15 et 10. 15 > 10 donc 8 + 7 > 8 + 2. On compare les valeurs, pas l'apparence."),
    ]),
    ("A word problem", "مسألة كلامية", "Un problème", "17", [
        tens(1, 5, eq=True),
        T("There are 9 crayons in a box. Sami adds 6 crayons. How many are in the box now? Given: 9. Change: 6 are added, so the quantity increased. 9 + 6: 9 needs 1 to make 10, 6 = 1 + 5, so 9 + 6 = 10 + 5 = 15. There are 15 crayons in the box.",
          "في علبة 9 أقلام تلوين. أضاف سامي 6. كم قلمًا في العلبة الآن؟ المعطى: 9. التغيير: أضيف 6 فزادت الكمية. 9 + 6: العدد 9 يحتاج 1 ليصير 10 و6 = 1 + 5 إذن 9 + 6 = 10 + 5 = 15. في العلبة 15 قلمًا.",
          "Il y a 9 crayons dans une boîte. Sami en ajoute 6. Combien y en a-t-il maintenant ? Donné : 9. Changement : on ajoute 6, la quantité augmente. 9 + 6 : 9 a besoin de 1, 6 = 1 + 5, donc 9 + 6 = 10 + 5 = 15. Il y a 15 crayons."),
        F("9 + 6 = 15"),
    ]),
    ("Counting by 2", "العدّ بالاثنين", "Compter de 2 en 2", "17", [
        numpath(["4", "6", "8", "10", "12", "14", "16", "18"], hi=None, size=38),
        T("A butterfly flies from flower 4 to flower 18, counting by 2. Counting by 2 is adding 2 again and again: 4 + 2 = 6, 6 + 2 = 8, and so on up to 18.",
          "تطير فراشة من الزهرة 4 إلى الزهرة 18 وهي تعدّ بالاثنين. العدّ بالاثنين هو إضافة 2 مرة بعد مرة: 4 + 2 = 6 و6 + 2 = 8 وهكذا حتى 18.",
          "Un papillon vole de la fleur 4 à la fleur 18 en comptant de 2 en 2. C'est ajouter 2 encore et encore : 4 + 2 = 6, 6 + 2 = 8, … jusqu'à 18."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Addition is part + part = total. We can make ten to calculate easily, find missing addends, compare sums after calculating them, and turn a word problem into a quantity relation.",
          "الجمع هو جزء + جزء = المجموع. نستطيع إكمال العشرة لنحسب بسهولة، ونجد الحدّ الناقص، ونقارن المجاميع بعد حسابها، ونحوّل المسألة الكلامية إلى علاقة بين كميات.",
          "Additionner, c'est partie + partie = total. On peut faire dix pour calculer facilement, trouver un terme manquant, comparer des sommes après les avoir calculées, et traduire un problème."),
        F("SEE THE PARTS → JOIN → CALCULATE → CHECK THE TOTAL → EXPLAIN WHY"),
    ]),
]

EXERCISES = [
    EX("1", "16", st("Write the addition for each picture: 3 and 2 apples; 5 and 5 paper clips; 7 and 3 shapes; 12 beads and 4; 10 blocks and 6; a ten-rod and 8.", "اكتب عملية الجمع لكل صورة: 3 و2 تفاحات؛ 5 و5 مشابك؛ 7 و3 أشكال؛ 12 خرزة و4؛ 10 قوالب و6؛ عشرة و8.", "Écris l'addition de chaque image : 3 et 2 pommes ; 5 et 5 trombones ; 7 et 3 formes ; 12 perles et 4 ; 10 blocs et 6 ; une barre de dix et 8."), [
        F("3 + 2 = 5      5 + 5 = 10      7 + 3 = 10"),
        F("12 + 4 = 16      10 + 6 = 16      10 + 8 = 18"),
    ]),
    EX("2", "16", st("Calculate: 7 + 3, 7 + 4, 7 + 8, 7 + 9, 7 + 2; 8 + 5, 8 + 4, 8 + 6, 8 + 3, 8 + 9; 9 + 6, 9 + 9, 9 + 5, 9 + 4, 9 + 7.", "احسب: 7 + 3 و7 + 4 و7 + 8 و7 + 9 و7 + 2؛ 8 + 5 و8 + 4 و8 + 6 و8 + 3 و8 + 9؛ 9 + 6 و9 + 9 و9 + 5 و9 + 4 و9 + 7.", "Calcule : 7 + 3, 7 + 4, 7 + 8, 7 + 9, 7 + 2 ; 8 + 5, 8 + 4, 8 + 6, 8 + 3, 8 + 9 ; 9 + 6, 9 + 9, 9 + 5, 9 + 4, 9 + 7."), [
        F("10   11   15   16   9"),
        F("13   12   14   11   17"),
        F("15   18   14   13   16"),
        T("For example 7 + 8 = 7 + 3 + 5 = 10 + 5 = 15 and 9 + 6 = 9 + 1 + 5 = 10 + 5 = 15.", "مثلًا 7 + 8 = 7 + 3 + 5 = 10 + 5 = 15 و9 + 6 = 9 + 1 + 5 = 10 + 5 = 15.", "Par exemple 7 + 8 = 7 + 3 + 5 = 10 + 5 = 15 et 9 + 6 = 9 + 1 + 5 = 10 + 5 = 15."),
    ]),
    EX("3", "17", st("Add 5, add 4, add 6: 4, 3, 7 → +5; 8, 6, 5 → +4; 9, 6, 7 → +6.", "أضف 5 وأضف 4 وأضف 6: 4 و3 و7 → +5؛ 8 و6 و5 → +4؛ 9 و6 و7 → +6.", "Ajoute 5, ajoute 4, ajoute 6 : 4, 3, 7 → +5 ; 8, 6, 5 → +4 ; 9, 6, 7 → +6."), [
        F("4 + 5 = 9      3 + 5 = 8      7 + 5 = 12"),
        F("8 + 4 = 12      6 + 4 = 10      5 + 4 = 9"),
        F("9 + 6 = 15      6 + 6 = 12      7 + 6 = 13"),
    ]),
    EX("4", "17", st("Find the missing number: totals 6, 10 and 9.", "أوجد العدد الناقص: المجاميع 6 و10 و9.", "Trouve le nombre manquant : totaux 6, 10 et 9."), [
        F("3 + 3 = 6      4 + 2 = 6      1 + 5 = 6"),
        F("7 + 3 = 10      8 + 2 = 10      5 + 5 = 10"),
        F("4 + 5 = 9      8 + 1 = 9      3 + 6 = 9"),
    ]),
    EX("5", "17", st("Complete with < or >: 8 + 7 _ 8 + 2; 6 + 5 _ 19; 7 + 6 _ 11; 6 + 3 _ 6 + 5; 5 _ 2 + 1; 8 _ 3 + 9.", "أكمل بـ < أو >: 8 + 7 _ 8 + 2؛ 6 + 5 _ 19؛ 7 + 6 _ 11؛ 6 + 3 _ 6 + 5؛ 5 _ 2 + 1؛ 8 _ 3 + 9.", "Complète avec < ou > : 8 + 7 _ 8 + 2 ; 6 + 5 _ 19 ; 7 + 6 _ 11 ; 6 + 3 _ 6 + 5 ; 5 _ 2 + 1 ; 8 _ 3 + 9."), [
        F("8 + 7 > 8 + 2      6 + 5 < 19      7 + 6 > 11"),
        F("6 + 3 < 6 + 5      5 > 2 + 1      8 < 3 + 9"),
        T("We calculate each side first: 15 > 10, 11 < 19, 13 > 11, 9 < 11, 5 > 3, 8 < 12.", "نحسب كل طرف أولًا: 15 > 10 و11 < 19 و13 > 11 و9 < 11 و5 > 3 و8 < 12.", "On calcule chaque côté : 15 > 10, 11 < 19, 13 > 11, 9 < 11, 5 > 3, 8 < 12."),
    ]),
    EX("6", "17", st("There are 9 crayons in a box. Sami adds 6. How many now?", "في علبة 9 أقلام تلوين. أضاف سامي 6. كم قلمًا الآن؟", "Il y a 9 crayons dans une boîte. Sami en ajoute 6. Combien maintenant ?"), [
        tens(1, 5, eq=True),
        F("9 + 6 = 15"),
        T("There are 15 crayons in the box.", "في العلبة 15 قلمًا.", "Il y a 15 crayons dans la boîte."),
    ]),
    EX("7", "17", st("The butterfly flies from flower 4 to flower 18 counting by 2.", "تطير الفراشة من الزهرة 4 إلى الزهرة 18 بالعدّ بالاثنين.", "Le papillon vole de la fleur 4 à la fleur 18 en comptant de 2 en 2."), [
        numpath(["4", "6", "8", "10", "12", "14", "16", "18"], hi=None, size=38),
        F("4, 6, 8, 10, 12, 14, 16, 18"),
    ]),
    EX("8", "", st("Challenge: I have 8 stickers and my friend gives me 7 more. How many?", "تحدٍّ: عندي 8 ملصقات وأعطاني صديقي 7 أخرى. كم صار عندي؟", "Défi : j'ai 8 autocollants et mon ami m'en donne 7. Combien en ai-je ?"), [
        F("8 + 7 = 8 + 2 + 5 = 10 + 5 = 15"),
    ]),
    EX("9", "", st("Error detective: 7 + 3 = 73. And 3 + __ = 6, a child writes 9. What went wrong?", "المحقق: 7 + 3 = 73. وفي 3 + __ = 6 كتب طفل 9. ما الخطأ؟", "Détective : 7 + 3 = 73. Et dans 3 + __ = 6, un enfant écrit 9. Où est l'erreur ?"), [
        T("Writing numbers side by side is not addition: 7 + 3 = 10. And 3 + 9 = 12, not 6, so the missing part is 3.", "كتابة الأعداد جنبًا إلى جنب ليست جمعًا: 7 + 3 = 10. و3 + 9 = 12 لا 6 إذن الناقص هو 3.", "Écrire des nombres côte à côte n'est pas additionner : 7 + 3 = 10. Et 3 + 9 = 12, pas 6 : le terme manquant est 3."),
    ]),
    EX("10", "", st("Final check: 6 + 4; 8 + 6; 9 + 8; __ + 5 = 9; 7 + __ = 10; 7 + 8 _ 7 + 2; 6 birds and 5 more; continue 6, 8, 10, __, __.", "تقييم أخير: 6 + 4؛ 8 + 6؛ 9 + 8؛ __ + 5 = 9؛ 7 + __ = 10؛ 7 + 8 _ 7 + 2؛ 6 عصافير وتأتي 5؛ تابع 6، 8، 10، __، __.", "Évaluation : 6 + 4 ; 8 + 6 ; 9 + 8 ; __ + 5 = 9 ; 7 + __ = 10 ; 7 + 8 _ 7 + 2 ; 6 oiseaux et 5 de plus ; continue 6, 8, 10, __, __."), [
        F("10      14      17      4      3      7 + 8 > 7 + 2"),
        F("6 + 5 = 11 birds      12, 14"),
    ]),
]
