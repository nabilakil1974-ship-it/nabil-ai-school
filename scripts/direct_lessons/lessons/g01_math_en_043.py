"""Grade 1 Mathematics — Problems."""
from scripts.direct_lessons.common import T, F, EX, st, tens, jumps, numpath

LESSON_ID = "G01-MATH-EN-043"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Problems", "ar": "مسائل", "fr": "Problèmes"}

THEORY = [
    ("What do we know? What is asked?", "ماذا نعرف؟ وماذا يُطلب؟", "Que sait-on ? Que demande-t-on ?", "110", [
        T("Hello, champion! Here is a story: Layla has 4 apples. Her mother gives her 3 more apples. How many apples does Layla have now? First we do not calculate. We ask: what do we know? 4 apples and 3 more apples. What is asked? How many apples altogether.",
          "مرحبًا يا بطل! إليك قصة: عند ليلى 4 تفاحات. تعطيها أمها 3 تفاحات أخرى. كم تفاحة عند ليلى الآن؟ أولًا لا نحسب. نسأل: ماذا نعرف؟ 4 تفاحات و3 تفاحات إضافية. وماذا يُطلب؟ كم تفاحة في المجموع.",
          "Bonjour champion ! Une histoire : Layla a 4 pommes. Sa mère lui en donne 3 de plus. Combien de pommes Layla a-t-elle maintenant ? D'abord on ne calcule pas. On se demande : que sait-on ? 4 pommes et 3 de plus. Que demande-t-on ? Combien de pommes en tout."),
        F("KNOWN: 4 and 3 more      ASKED: how many in all?"),
    ]),
    ("Draw the story", "نرسم القصة", "Dessiner l'histoire", "110", [
        jumps(4, 3, hi=10),
        T("We draw the story on the number path: start at 4 and add 3 more: 5, 6, 7. The drawing must match the story: 4 first, then 3 more. Layla now has 7 apples.",
          "نرسم القصة على مسار الأعداد: نبدأ من 4 ونضيف 3: 5، 6، 7. يجب أن يطابق الرسم القصة: 4 أولًا ثم 3 أخرى. عند ليلى الآن 7 تفاحات.",
          "On dessine l'histoire sur la droite : on part de 4 et on ajoute 3 : 5, 6, 7. Le dessin doit suivre l'histoire : 4 d'abord, puis 3 de plus. Layla a maintenant 7 pommes."),
        F("4 + 3 = 7"),
    ]),
    ("Check the answer", "نتحقق من الجواب", "Vérifier la réponse", "111", [
        T("Does 7 make sense? Layla had 4 and received more, so she must have more than 4. 7 is more than 4, so it fits the story. Answer in a sentence: Layla has 7 apples now.",
          "هل 7 منطقي؟ كان عند ليلى 4 وحصلت على المزيد، فلا بد أن يكون عندها أكثر من 4. و7 أكثر من 4، فهو يناسب القصة. نكتب الجواب بجملة: عند ليلى الآن 7 تفاحات.",
          "7 a-t-il du sens ? Layla avait 4 et en a reçu d'autres : elle doit en avoir plus de 4. 7 > 4, ça colle à l'histoire. On répond par une phrase : Layla a maintenant 7 pommes."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("To solve a problem: understand the story, say what is known and what is asked, draw or represent it, calculate, then check that the answer fits the story.",
          "لحلّ مسألة: نفهم القصة، ونقول ما المعلوم وما المطلوب، ونرسم أو نمثّل، ثم نحسب، ثم نتحقق من أن الجواب يناسب القصة.",
          "Pour résoudre un problème : comprendre l'histoire, dire ce qu'on sait et ce qu'on cherche, représenter, calculer, puis vérifier que la réponse colle à l'histoire."),
        F("UNDERSTAND → KNOWN & ASKED → DRAW → CALCULATE → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "110", st("Sami has 5 marbles and finds 2 more. How many now?", "عند سامي 5 كرات ويجد كرتين أخريين. كم كرة عنده الآن؟", "Sami a 5 billes et en trouve 2 de plus. Combien en a-t-il maintenant ?"), [
        jumps(5, 2, hi=10),
        T("Known: 5 and 2 more. Asked: how many in all. 5 + 2 = 7. Sami has 7 marbles.", "المعلوم: 5 ثم 2 أخريان. المطلوب: كم المجموع. 5 + 2 = 7. عند سامي 7 كرات.", "Connu : 5 et 2 de plus. Cherché : combien en tout. 5 + 2 = 7. Sami a 7 billes."),
    ]),
    EX("2", "110", st("A box has 10 pencils and another box has 20. How many pencils?", "في علبة 10 أقلام وفي علبة أخرى 20. كم قلمًا؟", "Une boîte a 10 crayons et une autre 20. Combien de crayons ?"), [
        tens(3, 0, eq=True),
        T("1 ten + 2 tens = 3 tens. 10 + 20 = 30 pencils.", "عشرة + عشرتان = 3 عشرات. 10 + 20 = 30 قلمًا.", "1 dizaine + 2 dizaines = 3 dizaines. 10 + 20 = 30 crayons."),
    ]),
    EX("3", "110", st("There are 6 birds on a tree and 3 more arrive. How many birds?", "على الشجرة 6 عصافير ويصل 3 أخرى. كم عصفورًا؟", "6 oiseaux sont sur un arbre et 3 autres arrivent. Combien d'oiseaux ?"), [
        jumps(6, 3, hi=10),
        T("6 + 3 = 9 birds.", "6 + 3 = 9 عصافير.", "6 + 3 = 9 oiseaux."),
    ]),
    EX("4", "111", st("Ali has 23 stickers and gets 4 more. How many stickers?", "عند علي 23 ملصقًا ويحصل على 4 أخرى. كم ملصقًا؟", "Ali a 23 autocollants et en reçoit 4. Combien en a-t-il ?"), [
        tens(2, 3, eq=True),
        tens(2, 7, eq=True),
        T("23 is 2 tens and 3 ones. Add 4 ones: 7 ones. So 27 stickers.", "23 هي عشرتان و3 آحاد. نضيف 4 آحاد: 7 آحاد. إذن 27 ملصقًا.", "23, c'est 2 dizaines et 3 unités. On ajoute 4 unités : 7 unités. Donc 27 autocollants."),
    ]),
    EX("5", "111", st("What is known and what is asked: 'There are 8 cups and 2 more cups. How many cups?'", "ما المعلوم وما المطلوب: «هناك 8 أكواب و2 أخريان. كم كوبًا؟»", "Qu'est-ce qui est connu et cherché : « 8 tasses et 2 de plus. Combien de tasses ? »"), [
        F("KNOWN: 8 and 2      ASKED: how many cups in all"),
        T("We join the two quantities: 8 + 2 = 10 cups.", "نضمّ الكميتين: 8 + 2 = 10 أكواب.", "On réunit les deux quantités : 8 + 2 = 10 tasses."),
    ]),
    EX("6", "111", st("Error check: a child answers 3 for '5 apples and 2 more'. Does it fit the story?", "تحقّق من الخطأ: أجاب طفل 3 عن «5 تفاحات و2 أخريان». هل يناسب القصة؟", "Vérifie l'erreur : un enfant répond 3 pour « 5 pommes et 2 de plus ». Cela colle-t-il à l'histoire ?"), [
        jumps(5, 2, hi=10),
        T("No. There were 5 and more came, so the answer must be more than 5. The correct answer is 7.", "لا. كان هناك 5 وجاء المزيد، فيجب أن يكون الجواب أكبر من 5. الجواب الصحيح 7.", "Non. Il y en avait 5 et il en vient d'autres : la réponse doit dépasser 5. La bonne réponse est 7."),
    ]),
    EX("7", "111", st("Challenge: 20 books on one shelf, 20 on another, and 10 on a third. How many books?", "تحدٍّ: 20 كتابًا على رف و20 على رف آخر و10 على رف ثالث. كم كتابًا؟", "Défi : 20 livres sur une étagère, 20 sur une autre et 10 sur une troisième. Combien de livres ?"), [
        tens(5, 0, eq=True),
        T("2 + 2 + 1 = 5 tens = 50 books.", "2 + 2 + 1 = 5 عشرات = 50 كتابًا.", "2 + 2 + 1 = 5 dizaines = 50 livres."),
    ]),
    EX("8", "111", st("Final check: make up the steps for '7 fish and 3 more fish'.", "تقييم أخير: اذكر الخطوات لـ«7 أسماك و3 أسماك أخرى».", "Évaluation : donne les étapes pour « 7 poissons et 3 de plus »."), [
        jumps(7, 3, hi=10),
        T("Known: 7 and 3 more. Asked: how many fish. Draw: start at 7, jump 3. Calculate: 7 + 3 = 10. Check: more than 7, so it fits. Answer: 10 fish.", "المعلوم: 7 و3 أخرى. المطلوب: كم سمكة. نرسم: نبدأ من 7 ونقفز 3. نحسب: 7 + 3 = 10. نتحقق: أكبر من 7 فيناسب. الجواب: 10 أسماك.", "Connu : 7 et 3 de plus. Cherché : combien de poissons. Dessin : départ 7, 3 sauts. Calcul : 7 + 3 = 10. Vérification : plus que 7, ça colle. Réponse : 10 poissons."),
    ]),
]
