"""Grade 1 Mathematics — Add with 6 and 7."""
from scripts.direct_lessons.common import T, F, EX, st, jumps, join

LESSON_ID = "G01-MATH-EN-032"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Add with 6 and 7", "ar": "الجمع مع 6 و7", "fr": "Additionner avec 6 et 7"}

THEORY = [
    ("Keep 6, count on", "نبقي 6 ونعدّ تصاعديًا", "Garder 6 et surcompter", "84", [
        T("Hello! Today we add starting numbers 6 and 7. We do not lose the first number and count again from one every time, if we can be smarter. If I know this is 6, and I am asked to add 2, I keep 6 in my head and count only the extra: seven, eight. So 6 + 2 = 8.",
          "مرحبًا! اليوم نجمع انطلاقًا من 6 و7. لا نضيّع العدد الأول ونعيد العدّ من الواحد كل مرة إذا استطعنا أن نكون أذكى. إذا عرفت أن هذه 6 وطُلب مني إضافة 2 فأبقي 6 في رأسي وأعدّ الزيادة فقط: سبعة، ثمانية. إذن 6 + 2 = 8.",
          "Bonjour ! Aujourd'hui on ajoute à partir de 6 et 7. On ne perd pas le premier nombre en recomptant depuis un à chaque fois, si on peut être plus malin. Si je sais que c'est 6 et qu'on me demande d'ajouter 2, je garde 6 en tête et je compte seulement le supplément : sept, huit. Donc 6 + 2 = 8."),
        join(6, 2, "circle", "circle", "#1e63d6", "#e53935"),
        T("Another one: 6 + 3. The first number is 6. Keep it in your head and count three steps: seven, eight, nine. We landed on 9. So 6 + 3 = 9.",
          "مثال آخر: 6 + 3. العدد الأول 6. أبقِه في رأسك وعدّ ثلاث خطوات: سبعة، ثمانية، تسعة. وصلنا إلى 9. إذن 6 + 3 = 9.",
          "Un autre : 6 + 3. Le premier nombre est 6. Garde-le en tête et compte trois pas : sept, huit, neuf. On est arrivé à 9. Donc 6 + 3 = 9."),
        jumps(6, 3),
    ]),
    ("Keep 7, count on", "نبقي 7 ونعدّ تصاعديًا", "Garder 7 et surcompter", "84", [
        jumps(7, 2),
        T("Now the same idea with 7. 7 + 2: keep 7 steady and count two more: eight, nine. So 7 + 2 = 9. The starting quantity was 7, the added quantity was 2, and the total is 9.",
          "الآن الفكرة نفسها مع 7. 7 + 2: نُبقي 7 ثابتة ونعدّ اثنين آخرين: ثمانية، تسعة. إذن 7 + 2 = 9. كانت الكمية الأولى 7 والمضافة 2 والمجموع 9.",
          "Maintenant la même idée avec 7. 7 + 2 : on garde 7 fixe et on compte deux de plus : huit, neuf. Donc 7 + 2 = 9. La quantité de départ était 7, la quantité ajoutée 2 et le total 9."),
    ]),
    ("Counters and the number line must agree", "العدّادات وخط الأعداد يجب أن يتفقا", "Jetons et droite doivent s'accorder", "85", [
        join(6, 2, "circle", "circle", "#1e63d6", "#e53935"),
        jumps(6, 2),
        T("Two different ways, but the same quantities, so they must give the same total. If the answer comes out different, there is a mistake in the way or in the counting.",
          "طريقتان مختلفتان لكن الكميات نفسها، لذلك يجب أن يخرج المجموع نفسه. إذا خرج جواب مختلف ففي الأمر خطأ في الطريقة أو في العدّ.",
          "Deux façons différentes mais les mêmes quantités : elles doivent donner le même total. Si la réponse est différente, il y a une erreur dans la méthode ou le comptage."),
    ]),
    ("Keep track of both parts", "نتابع الجزأين معًا", "Suivre les deux parties", "85", [
        jumps(7, 3),
        T("The biggest mistake is to forget the starting number or to count the added objects wrongly. For 7 + 3: start 7, added units 3, count on eight, nine, ten, total 10. Every part must stay clear.",
          "أكبر خطأ هنا أن ننسى العدد الأول أو نعدّ الأشياء المضافة بشكل خاطئ. في 7 + 3: البداية 7 والوحدات المضافة 3 ونعدّ ثمانية، تسعة، عشرة، فالمجموع 10. يجب أن يبقى كل جزء واضحًا.",
          "La plus grosse erreur est d'oublier le nombre de départ ou de mal compter les objets ajoutés. Pour 7 + 3 : départ 7, unités ajoutées 3, on compte huit, neuf, dix, total 10. Chaque partie doit rester claire."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("With 6 and 7 we can keep the starting number in our head and count only the added units. Then we say the total and verify with another model.",
          "مع 6 و7 نستطيع أن نُبقي العدد الأول في رأسنا ونعدّ الوحدات المضافة فقط. ثم نقول المجموع ونتحقق بنموذج آخر.",
          "Avec 6 et 7, on peut garder le nombre de départ en tête et compter seulement les unités ajoutées. Puis on dit le total et on vérifie avec un autre modèle."),
        F("KEEP THE START → COUNT ON THE EXTRA UNITS → SAY THE TOTAL → VERIFY WITH ANOTHER MODEL"),
    ]),
]

EXERCISES = [
    EX("1", "84", st("Count on from 6: 6 + 1, 6 + 2, 6 + 3.", "عدّ تصاعديًا من 6: 6 + 1 و6 + 2 و6 + 3.", "Surcompte depuis 6 : 6 + 1, 6 + 2, 6 + 3."), [
        jumps(6, 1), jumps(6, 2), jumps(6, 3),
        T("Do not count again from 1. Start with your voice at 6, then count the jumps.",
          "لا تعدّ من 1 مرة أخرى. ابدأ بصوتك من 6 ثم عدّ القفزات.",
          "Ne recompte pas depuis 1. Commence à voix haute à 6, puis compte les sauts."),
        F("7      8      9"),
    ]),
    EX("2", "84", st("Count on from 7: 7 + 1, 7 + 2, 7 + 3.", "عدّ تصاعديًا من 7: 7 + 1 و7 + 2 و7 + 3.", "Surcompte depuis 7 : 7 + 1, 7 + 2, 7 + 3."), [
        jumps(7, 1), jumps(7, 2), jumps(7, 3),
        T("Start at 7. Count only the added units. Check the landing.",
          "ابدأ من 7. عدّ الوحدات المضافة فقط. تحقّق من الهبوط.",
          "Pars de 7. Compte seulement les unités ajoutées. Vérifie l'atterrissage."),
        F("8      9      10"),
    ]),
    EX("3", "85", st("Solve 7 + 2 one way and check it another way.", "احسب 7 + 2 بطريقة وتحقّق بطريقة أخرى.", "Résous 7 + 2 d'une façon et vérifie d'une autre."), [
        join(7, 2, "circle", "circle", "#1e63d6", "#e53935"),
        jumps(7, 2),
        T("Same total: 9.",
          "المجموع نفسه: 9.",
          "Même total : 9."),
    ]),
    EX("4", "85", st("Choose a strategy for 6 + 2: counters, number line or counting on. Then verify another way.", "اختر طريقة لـ 6 + 2: عدّادات أو خط أعداد أو عدّ تصاعدي. ثم تحقّق بطريقة أخرى.", "Choisis une stratégie pour 6 + 2 : jetons, droite ou surcomptage. Puis vérifie autrement."), [
        join(6, 2, "square", "square", "#fb8c00", "#8e24aa"),
        T("The strategy can differ; the truth does not.",
          "قد تختلف الطريقة لكن الحقيقة لا تختلف.",
          "La stratégie peut changer ; la vérité, non."),
        F("6 + 2 = 8"),
    ]),
    EX("5", "85", st("Error detective: 7 + 2 = 10, because the child said 8, 9, 10 after starting at 7.", "المحقق: 7 + 2 = 10 لأن الطفل قال 8، 9، 10 بعد البداية من 7.", "Détective : 7 + 2 = 10, car l'enfant a dit 8, 9, 10 en partant de 7."), [
        jumps(7, 2),
        T("How many added units? Two. So after 7 we say only two numbers: 8, 9. The total is 9. We do not make an extra jump.",
          "كم وحدة مضافة؟ اثنتان. إذن بعد 7 نقول عددين فقط: 8، 9. المجموع 9. لا نقوم بقفزة زائدة.",
          "Combien d'unités ajoutées ? Deux. Après 7 on ne dit que deux nombres : 8, 9. Le total est 9. On ne fait pas de saut en plus."),
        F("7 + 2 = 9"),
    ]),
    EX("6", "85", st("Mixed practice: 6 + 2, 7 + 1, 6 + 3, 7 + 2, 7 + 3.", "تدريب مختلط: 6 + 2 و7 + 1 و6 + 3 و7 + 2 و7 + 3.", "Exercice mixte : 6 + 2, 7 + 1, 6 + 3, 7 + 2, 7 + 3."), [
        F("6 + 2 = 8      7 + 1 = 8      6 + 3 = 9      7 + 2 = 9      7 + 3 = 10"),
        T("For some of them, show a second representation.",
          "في بعضها نُظهر تمثيلًا ثانيًا.",
          "Pour certaines, montre une deuxième représentation."),
    ]),
    EX("7", "85", st("Challenge: on a number line I started at 7 and reached 10 with three unit jumps. What is the addition?", "تحدٍّ: على خط أعداد بدأت من 7 ووصلت إلى 10 بثلاث قفزات. ما عملية الجمع؟", "Défi : sur une droite, je suis parti de 7 et arrivé à 10 en trois sauts. Quelle est l'addition ?"), [
        jumps(7, 3),
        F("7 + 3 = 10"),
        T("Start 7, count the jumps: 3. You found the equation from the model.",
          "البداية 7 وعدد القفزات 3. استنتجت المعادلة من النموذج.",
          "Départ 7, sauts : 3. Tu as trouvé l'égalité à partir du modèle."),
    ]),
    EX("8", "85", st("Final check: 6 + 1, 6 + 3, 7 + 2, show 7 + 3 on a number line, and explain why counting on starts after the starting number.", "تقييم أخير: 6 + 1 و6 + 3 و7 + 2، ومثّل 7 + 3 على خط الأعداد، واشرح لماذا يبدأ العدّ التصاعدي بعد العدد الأول.", "Évaluation : 6 + 1, 6 + 3, 7 + 2, montre 7 + 3 sur une droite et explique pourquoi le surcomptage commence après le nombre de départ."), [
        F("6 + 1 = 7      6 + 3 = 9      7 + 2 = 9"),
        jumps(7, 3),
        T("Because the starting number is already there; only the added units are counted.",
          "لأن العدد الأول موجود أصلًا، ونعدّ الوحدات المضافة فقط.",
          "Parce que le nombre de départ est déjà là ; on ne compte que les unités ajoutées."),
    ]),
]
