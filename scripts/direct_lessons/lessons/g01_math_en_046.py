"""Grade 1 Mathematics — Add by grouping by 10."""
from scripts.direct_lessons.common import T, F, EX, st, tens

LESSON_ID = "G01-MATH-EN-046"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Add by grouping by 10", "ar": "الجمع بالتجميع في عشرات", "fr": "Additionner en groupant par 10"}

THEORY = [
    ("Ten ones make one ten", "عشرة آحاد تصنع عشرة واحدة", "Dix unités font une dizaine", "116", [
        tens(0, 10, bundled=False, eq=True),
        T("Hello, champion! Look at these 10 loose ones. If we tie exactly 10 loose ones together, we get 1 bundle: one ten. The quantity did not change; it only changed shape. 10 ones = 1 ten.",
          "مرحبًا يا بطل! انظر إلى هذه الآحاد العشرة المنفردة. إذا ربطنا 10 آحاد بالضبط معًا نحصل على حزمة واحدة: عشرة واحدة. الكمية لم تتغير، تغيّر شكلها فقط. 10 آحاد = عشرة واحدة.",
          "Bonjour champion ! Regarde ces 10 unités seules. Si on attache exactement 10 unités, on obtient 1 paquet : une dizaine. La quantité n'a pas changé, seulement sa forme. 10 unités = 1 dizaine."),
        tens(1, 0, eq=True),
    ]),
    ("Join and regroup", "نجمع ثم نعيد التجميع", "Réunir puis regrouper", "116", [
        tens(1, 6, tag="A", eq=True),
        T("Let us join 6 ones and 7 ones. Together we have 13 loose ones. We can tie 10 of them into a new ten. Then we have 1 ten and 3 ones left: 13.",
          "لنجمع 6 آحاد و7 آحاد. عندنا معًا 13 واحدًا منفردًا. نستطيع ربط 10 منها في عشرة جديدة. فيصير عندنا عشرة واحدة و3 آحاد: 13.",
          "Réunissons 6 unités et 7 unités. Ensemble, 13 unités seules. On en attache 10 en une nouvelle dizaine. Il reste 1 dizaine et 3 unités : 13."),
        tens(1, 3, tag="B", eq=True),
        F("6 + 7 = 13 = 1 ten + 3 ones"),
    ]),
    ("Tens and ones after regrouping", "العشرات والآحاد بعد التجميع", "Dizaines et unités après regroupement", "117", [
        tens(3, 8, tag="A", eq=True),
        T("Now 28 + 10 is easy, and so is 25 + 7: the ones 5 + 7 make 12, which is 1 ten and 2 ones. The tens: 2 + 1 = 3 tens. So the answer is 3 tens and 2 ones = 32.",
          "الآن 25 + 7: الآحاد 5 + 7 = 12 وهي عشرة واحدة وواحدان. العشرات: 2 + 1 = 3 عشرات. إذن الجواب 3 عشرات وواحدان = 32.",
          "25 + 7 : les unités 5 + 7 = 12, soit 1 dizaine et 2 unités. Les dizaines : 2 + 1 = 3. Réponse : 3 dizaines et 2 unités = 32."),
        tens(3, 2, tag="B", eq=True),
        F("25 + 7 = 32"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Exactly ten ones can be regrouped as one ten without changing the total. Count the new tens and the remaining ones, and never count the regrouped ones again.",
          "يمكن تجميع عشرة آحاد بالضبط في عشرة واحدة دون أن يتغير المجموع. نعدّ العشرات الجديدة والآحاد الباقية، ولا نعدّ الآحاد المجمّعة مرة ثانية.",
          "Dix unités exactement peuvent devenir une dizaine sans changer le total. On compte les nouvelles dizaines et les unités restantes, sans recompter celles regroupées."),
        F("JOIN → TIE EXACTLY TEN → COUNT TENS → COUNT THE REST"),
    ]),
]

EXERCISES = [
    EX("1", "116", st("Exchange 10 loose ones for a ten.", "بدّل 10 آحاد منفردة بعشرة واحدة.", "Échange 10 unités seules contre une dizaine."), [
        tens(0, 10, bundled=False, eq=True),
        tens(1, 0, eq=True),
        T("10 ones = 1 ten.", "10 آحاد = عشرة واحدة.", "10 unités = 1 dizaine."),
    ]),
    EX("2", "116", st("Join 8 ones and 5 ones. Regroup.", "اجمع 8 آحاد و5 آحاد ثم أعد التجميع.", "Réunis 8 et 5 unités. Regroupe."), [
        tens(1, 3, eq=True),
        T("8 + 5 = 13 loose ones. Tie 10: 1 ten and 3 ones.", "8 + 5 = 13 واحدًا. نربط 10: عشرة و3 آحاد.", "8 + 5 = 13 unités. On attache 10 : 1 dizaine et 3 unités."),
    ]),
    EX("3", "116", st("Join 9 and 9.", "اجمع 9 و9.", "Réunis 9 et 9."), [
        tens(1, 8, eq=True),
        T("18 loose ones: 1 ten and 8 ones.", "18 واحدًا: عشرة و8 آحاد.", "18 unités : 1 dizaine et 8 unités."),
    ]),
    EX("4", "117", st("Solve 14 + 6.", "احسب 14 + 6.", "Calcule 14 + 6."), [
        tens(2, 0, eq=True),
        T("4 + 6 = 10 ones, which makes a new ten: 1 ten + 1 ten = 2 tens = 20.", "4 + 6 = 10 آحاد تكوّن عشرة جديدة: عشرة + عشرة = عشرتان = 20.", "4 + 6 = 10 unités, une nouvelle dizaine : 1 + 1 = 2 dizaines = 20."),
    ]),
    EX("5", "117", st("Solve 27 + 5.", "احسب 27 + 5.", "Calcule 27 + 5."), [
        tens(3, 2, eq=True),
        T("7 + 5 = 12 ones = 1 ten and 2 ones. 2 tens + 1 ten = 3 tens, and 2 ones: 32.", "7 + 5 = 12 واحدًا = عشرة وواحدان. عشرتان + عشرة = 3 عشرات وواحدان: 32.", "7 + 5 = 12 unités = 1 dizaine et 2 unités. 2 + 1 = 3 dizaines et 2 unités : 32."),
    ]),
    EX("6", "117", st("Error check: 15 + 7 = 112. What went wrong?", "تحقّق من الخطأ: 15 + 7 = 112. ما الخطأ؟", "Vérifie l'erreur : 15 + 7 = 112. Où est l'erreur ?"), [
        tens(2, 2, eq=True),
        T("The child wrote 5 + 7 = 12 next to the tens digit. 12 ones are 1 ten and 2 ones, so we add the ten: 1 + 1 = 2 tens and 2 ones = 22.", "كتب الطفل 5 + 7 = 12 بجانب رقم العشرات. 12 واحدًا هي عشرة وواحدان فنضيف العشرة: 1 + 1 = عشرتان وواحدان = 22.", "L'enfant a collé 12 à côté du chiffre des dizaines. 12 unités = 1 dizaine + 2 unités : 1 + 1 = 2 dizaines et 2 unités = 22."),
    ]),
    EX("7", "117", st("Challenge: 36 + 4.", "تحدٍّ: 36 + 4.", "Défi : 36 + 4."), [
        tens(4, 0, eq=True),
        T("6 + 4 = 10 ones = 1 new ten. 3 tens + 1 ten = 4 tens = 40.", "6 + 4 = 10 آحاد = عشرة جديدة. 3 عشرات + عشرة = 4 عشرات = 40.", "6 + 4 = 10 unités = 1 nouvelle dizaine. 3 + 1 = 4 dizaines = 40."),
    ]),
    EX("8", "117", st("Final check: regroup 7 + 8 and state the result.", "تقييم أخير: أعد تجميع 7 + 8 وقل النتيجة.", "Évaluation : regroupe 7 + 8 et donne le résultat."), [
        tens(1, 5, eq=True),
        T("15 ones: tie 10 into 1 ten, 5 ones remain. 7 + 8 = 15.", "15 واحدًا: نربط 10 في عشرة ويبقى 5 آحاد. 7 + 8 = 15.", "15 unités : on attache 10 en 1 dizaine, il reste 5. 7 + 8 = 15."),
    ]),
]
