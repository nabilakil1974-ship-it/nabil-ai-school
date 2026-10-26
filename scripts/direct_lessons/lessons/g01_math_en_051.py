"""Grade 1 Mathematics — Problems (continuation)."""
from scripts.direct_lessons.common import T, F, EX, st, jumps
from scripts.direct_lessons.lessons.g01_math_en_048 import takeaway

LESSON_ID = "G01-MATH-EN-051"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Problems (continuation)", "ar": "مسائل (تابع)", "fr": "Problèmes (suite)"}

THEORY = [
    ("What is happening in the story?", "ماذا يحدث في القصة؟", "Que se passe-t-il dans l'histoire ?", "128", [
        T("Hello, champion! Two stories. Story A: Nour has 5 pens and buys 3 more. Story B: Nour has 5 pens and gives away 3. In both there are 5 and 3, but the actions are different. In A pens are put together. In B pens are taken away. Before we calculate, we must find the action.",
          "مرحبًا يا بطل! قصتان. القصة A: عند نور 5 أقلام وتشتري 3 أخرى. القصة B: عند نور 5 أقلام وتعطي 3. في القصتين العددان 5 و3 لكن الفعل مختلف. في A تُضمّ الأقلام. وفي B تُؤخذ الأقلام. قبل أن نحسب علينا أن نجد الفعل.",
          "Deux histoires. A : Nour a 5 stylos et en achète 3 de plus. B : Nour a 5 stylos et en donne 3. Dans les deux, il y a 5 et 3, mais l'action est différente. Dans A, on réunit. Dans B, on retire. Avant de calculer, on cherche l'action."),
        F("A: put together      B: take away"),
    ]),
    ("Story A: addition", "القصة A: جمع", "Histoire A : addition", "128", [
        jumps(5, 3, hi=10),
        T("Combining or increasing leads to addition: 5 + 3 = 8. Nour has 8 pens. It makes sense: 8 is more than 5.",
          "الضمّ أو الزيادة يقودان إلى الجمع: 5 + 3 = 8. عند نور 8 أقلام. هذا منطقي: 8 أكبر من 5.",
          "Réunir ou augmenter conduit à l'addition : 5 + 3 = 8. Nour a 8 stylos. C'est logique : 8 est plus que 5."),
    ]),
    ("Story B: subtraction", "القصة B: طرح", "Histoire B : soustraction", "129", [
        takeaway(5, 3),
        jumps(5, 3, hi=10, back=True),
        T("Removing leads to subtraction: 5 − 3 = 2. Nour has 2 pens left. It makes sense: 2 is less than 5.",
          "الأخذ يقود إلى الطرح: 5 − 3 = 2. بقي عند نور قلمان. هذا منطقي: 2 أقل من 5.",
          "Retirer conduit à la soustraction : 5 − 3 = 2. Il reste 2 stylos à Nour. C'est logique : 2 est moins que 5."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Find the action in the story, choose addition or subtraction, calculate, and check that the answer fits the story.",
          "نجد الفعل في القصة ثم نختار الجمع أو الطرح ثم نحسب ونتحقق أن الجواب يناسب القصة.",
          "On trouve l'action, on choisit addition ou soustraction, on calcule et on vérifie que la réponse colle à l'histoire."),
        F("ACTION → OPERATION → CALCULATE → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "128", st("Rana has 6 balloons and gets 2 more. Addition or subtraction?", "عند رنا 6 بالونات وتحصل على 2 أخريين. جمع أم طرح؟", "Rana a 6 ballons et en reçoit 2. Addition ou soustraction ?"), [
        jumps(6, 2, hi=10),
        T("Getting more means addition: 6 + 2 = 8.", "الحصول على المزيد يعني جمعًا: 6 + 2 = 8.", "Recevoir plus, c'est une addition : 6 + 2 = 8."),
    ]),
    EX("2", "128", st("There are 9 birds and 4 fly away. How many remain?", "هناك 9 عصافير طار منها 4. كم يبقى؟", "9 oiseaux, 4 s'envolent. Combien en reste-t-il ?"), [
        takeaway(9, 4),
        T("Flying away is taking away: 9 − 4 = 5.", "الطيران بعيدًا هو أخذ: 9 − 4 = 5.", "S'envoler, c'est retirer : 9 − 4 = 5."),
    ]),
    EX("3", "128", st("Omar has 12 cars and gives 2 to his friend. How many does he have?", "عند عمر 12 سيارة ويعطي صديقه 2. كم سيارة عنده؟", "Omar a 12 voitures et en donne 2. Combien lui en reste-t-il ?"), [
        takeaway(12, 2),
        F("12 − 2 = 10"),
    ]),
    EX("4", "129", st("A shelf has 10 books. 5 more are added. How many books?", "على رف 10 كتب وأضيف 5. كم كتابًا؟", "Une étagère a 10 livres. On en ajoute 5. Combien de livres ?"), [
        F("10 + 5 = 15"),
        T("Adding books is addition: 15 books.", "إضافة الكتب جمع: 15 كتابًا.", "Ajouter, c'est additionner : 15 livres."),
    ]),
    EX("5", "129", st("There are 15 apples and 5 are eaten. How many remain?", "هناك 15 تفاحة أُكلت منها 5. كم تبقى؟", "15 pommes, 5 sont mangées. Combien en reste-t-il ?"), [
        takeaway(15, 5),
        F("15 − 5 = 10"),
    ]),
    EX("6", "129", st("Error check: 'There are 8 sweets and 3 are eaten.' A child writes 8 + 3 = 11. Does it fit?", "تحقّق من الخطأ: «هناك 8 حلوى أُكلت منها 3». كتب طفل 8 + 3 = 11. هل يناسب؟", "Vérifie l'erreur : « 8 bonbons, 3 sont mangés ». Un enfant écrit 8 + 3 = 11. Cela colle-t-il ?"), [
        takeaway(8, 3),
        T("No. After eating there are fewer than 8, but 11 is more. The action is taking away: 8 − 3 = 5.", "لا. بعد الأكل يصير العدد أقل من 8 لكن 11 أكبر. الفعل أخذ: 8 − 3 = 5.", "Non. Après avoir mangé, il y en a moins que 8, or 11 est plus. L'action est retirer : 8 − 3 = 5."),
    ]),
    EX("7", "129", st("Challenge: 7 red flowers and 6 yellow flowers. How many flowers?", "تحدٍّ: 7 أزهار حمراء و6 صفراء. كم زهرة؟", "Défi : 7 fleurs rouges et 6 jaunes. Combien de fleurs ?"), [
        jumps(7, 6, hi=13),
        F("7 + 6 = 13"),
    ]),
    EX("8", "129", st("Final check: choose and justify the operation: 14 stickers, 4 given away.", "تقييم أخير: اختر العملية وبرّر: 14 ملصقًا أُعطي منها 4.", "Évaluation : choisis et justifie l'opération : 14 autocollants, 4 donnés."),[
        takeaway(14, 4),
        T("Giving away is taking away, so we subtract: 14 − 4 = 10 stickers remain.", "الإعطاء أخذ، لذلك نطرح: 14 − 4 = 10 ملصقات تبقى.", "Donner, c'est retirer : on soustrait. 14 − 4 = 10 autocollants restent."),
    ]),
]
