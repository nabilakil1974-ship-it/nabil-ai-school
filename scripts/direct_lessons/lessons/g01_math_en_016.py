"""Grade 1 Mathematics — Additive writings (continuation)."""
from scripts.direct_lessons.common import T, F, EX, st, join

LESSON_ID = "G01-MATH-EN-016"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Additive writings (continuation)", "ar": "الكتابة الجمعية (تتمة)", "fr": "Écritures additives (suite)"}

THEORY = [
    ("From the model to the writing", "من النموذج إلى الكتابة", "Du modèle à l'écriture", "46", [
        T("Hello! Do you remember when we wrote 2 + 1 = 3? Today we get stronger at this writing. Sometimes I give you a picture and you write. Sometimes I give you the writing and you build the picture. We walk in both directions.",
          "مرحبًا! هل تذكر عندما كتبنا 2 + 1 = 3؟ اليوم نصبح أقوى في هذه الكتابة. أحيانًا أعطيك صورة وتكتب، وأحيانًا أعطيك الكتابة وتبني الصورة. نمشي في الاتجاهين.",
          "Bonjour ! Tu te souviens quand on a écrit 2 + 1 = 3 ? Aujourd'hui on devient plus fort. Parfois je te donne une image et tu écris, parfois je te donne l'écriture et tu construis l'image. On marche dans les deux sens."),
        join(3, 2, total=False),
        T("We do not write yet. First part: 3. Second part: 2. Join and count the total: 5.",
          "لا نكتب بعد. الجزء الأول: 3. الجزء الثاني: 2. نضمّ ونعدّ المجموع: 5.",
          "On n'écrit pas encore. Première partie : 3. Deuxième partie : 2. On réunit et on compte le total : 5."),
        join(3, 2),
        T("Now we write: 3 + 2 = 5. Every number comes from a quantity we saw.",
          "الآن نكتب: 3 + 2 = 5. كل عدد جاء من كمية رأيناها.",
          "Maintenant on écrit : 3 + 2 = 5. Chaque nombre vient d'une quantité qu'on a vue."),
    ]),
    ("From the writing to the model", "من الكتابة إلى النموذج", "De l'écriture au modèle", "46", [
        F("4 + 3 = 7"),
        T("What is the first number? 4. We build four counters. The second number? 3. We build three counters. What does plus mean? Join.",
          "ما العدد الأول؟ 4. نبني 4 عدّادات. والعدد الثاني؟ 3. نبني 3 عدّادات. وماذا يعني +؟ الضمّ.",
          "Quel est le premier nombre ? 4. On construit quatre jetons. Le deuxième ? 3. On construit trois jetons. Que veut dire plus ? Réunir."),
        join(4, 3, "circle", "circle", "#e53935", "#1e63d6"),
        T("We join them and count to check: 7. The model and the writing match.",
          "نضمّهما ونعدّ للتأكد: 7. النموذج والكتابة متطابقان.",
          "On les réunit et on compte pour vérifier : 7. Le modèle et l'écriture correspondent."),
    ]),
    ("Same writing, new arrangement", "الكتابة نفسها بترتيب جديد", "Même écriture, autre disposition", "47", [
        join(2, 3, "square", "square", "#1e63d6", "#e53935"),
        T("The objects do not have to be in a straight line. What matters is how the model is divided into parts: first part 2, second part 3, whole 5. The writing stays 2 + 3 = 5.",
          "لا يجب أن تكون الأشياء على صف مستقيم. المهم كيف ينقسم النموذج إلى أجزاء: الجزء الأول 2 والثاني 3 والكل 5. تبقى الكتابة 2 + 3 = 5.",
          "Les objets n'ont pas à être alignés. Ce qui compte, c'est comment le modèle est partagé : première partie 2, deuxième 3, tout 5. L'écriture reste 2 + 3 = 5."),
        T("The arrangement changed, the relationship did not.",
          "الترتيب تغيّر، والعلاقة لم تتغير.",
          "La disposition a changé, la relation non."),
    ]),
    ("Find a missing numeral from the model", "نجد عددًا ناقصًا من النموذج", "Trouver un chiffre manquant grâce au modèle", "47", [
        join(3, 2),
        F("3 + __ = 5"),
        T("A numeral is missing. We do not guess. We look at the second part in the model: two stars. So 3 + 2 = 5.",
          "هناك عدد ناقص. لا نخمّن، بل ننظر إلى الجزء الثاني في النموذج: نجمتان. إذن 3 + 2 = 5.",
          "Un chiffre manque. On ne devine pas : on regarde la deuxième partie du modèle : deux étoiles. Donc 3 + 2 = 5."),
    ]),
    ("Check every symbol", "نتحقق من كل رمز", "Vérifier chaque symbole", "47", [
        join(3, 4, "circle", "circle", "#fb8c00", "#8e24aa"),
        T("Is 3 there as a quantity? Yes. Is 4 there? Yes. Did joining happen? Yes. Is the total really 7? Yes. So the writing is verified.",
          "هل 3 موجودة ككمية؟ نعم. هل 4 موجودة؟ نعم. هل حدث الضمّ؟ نعم. هل المجموع فعلًا 7؟ نعم. إذن الكتابة محقَّقة.",
          "Le 3 est-il là comme quantité ? Oui. Le 4 ? Oui. La réunion a-t-elle eu lieu ? Oui. Le total est-il bien 7 ? Oui. L'écriture est vérifiée."),
    ]),
    ("Read the writing as a story", "نقرأ الكتابة كقصة", "Lire l'écriture comme une histoire", "47", [
        F("5 + 2 = 7"),
        T("Do not only read symbols. Tell the story: there were 5 objects, 2 more joined, and there are 7 altogether. The writing is a short story.",
          "لا تقرأ الرموز فقط، بل احكِ القصة: كان هناك 5 أشياء، وانضمّ 2 آخران، فصار المجموع 7. الكتابة قصة مختصرة.",
          "Ne lis pas seulement des symboles. Raconte : il y avait 5 objets, 2 de plus sont arrivés, il y en a 7 en tout. L'écriture est une histoire courte."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("An additive writing is not a memorized symbol. It records something real: part + part = total. We can go from model to writing or from writing to model. When we doubt, we return to the quantities.",
          "الكتابة الجمعية ليست رموزًا محفوظة، بل تسجيل لشيء حقيقي: جزء + جزء = مجموع. نستطيع أن نمشي من النموذج إلى الكتابة أو بالعكس. وعند الشك نرجع إلى الكميات.",
          "Une écriture additive n'est pas un symbole appris : elle note quelque chose de réel : partie + partie = total. On passe du modèle à l'écriture ou l'inverse. Au doute, on revient aux quantités."),
        F("SEE / BUILD PARTS → JOIN → FIND THE TOTAL → WRITE → REBUILD → CHECK EVERY NUMBER"),
    ]),
]

EXERCISES = [
    EX("1", "46", st("Model to writing: 2 stars and 4 stars.", "من النموذج إلى الكتابة: نجمتان و4 نجوم.", "Du modèle à l'écriture : 2 étoiles et 4 étoiles."), [
        join(2, 4, total=False),
        T("First part: 2. Second part: 4. Total: 6. Start with the parts, not the total.",
          "الجزء الأول: 2. الجزء الثاني: 4. المجموع: 6. نبدأ بالأجزاء لا بالمجموع.",
          "Première partie : 2. Deuxième partie : 4. Total : 6. On commence par les parties, pas par le total."),
        join(2, 4),
        F("2 + 4 = 6"),
    ]),
    EX("2", "46", st("Writing to model: build 2 + 5 = 7.", "من الكتابة إلى النموذج: ابنِ 2 + 5 = 7.", "De l'écriture au modèle : construis 2 + 5 = 7."), [
        join(2, 5, "circle", "circle", "#fb8c00", "#1e63d6"),
        T("Two objects, then five objects. Join and count: seven.",
          "شيئان ثم خمسة أشياء. نضمّ ونعدّ: سبعة.",
          "Deux objets, puis cinq objets. On réunit et on compte : sept."),
    ]),
    EX("3", "47", st("1 red and 4 blue make 5. If we rearrange them, does the writing change?", "1 أحمر و4 أزرق يصنعان 5. إذا غيّرنا ترتيبهما هل تتغير الكتابة؟", "1 rouge et 4 bleus font 5. Si on les range autrement, l'écriture change-t-elle ?"), [
        join(1, 4, "square", "square", "#e53935", "#1e63d6"),
        T("No. The quantities are the same, so the writing is still the same.",
          "لا. الكميات نفسها، فالكتابة نفسها.",
          "Non. Les quantités sont les mêmes, donc l'écriture est la même."),
        F("1 + 4 = 5"),
    ]),
    EX("4", "47", st("Missing number: __ + 3 = 7, and 2 + __ = 6.", "العدد الناقص: __ + 3 = 7، و2 + __ = 6.", "Nombre manquant : __ + 3 = 7, et 2 + __ = 6."), [
        join(4, 3, "circle", "circle", "#e53935", "#1e63d6"),
        T("The model is the proof: the first part has 4. So 4 + 3 = 7.",
          "النموذج هو الدليل: الجزء الأول فيه 4. إذن 4 + 3 = 7.",
          "Le modèle est la preuve : la première partie en a 4. Donc 4 + 3 = 7."),
        join(2, 4, "circle", "circle", "#e53935", "#1e63d6"),
        T("The second part shows 4. So 2 + 4 = 6.",
          "الجزء الثاني فيه 4. إذن 2 + 4 = 6.",
          "La deuxième partie en montre 4. Donc 2 + 4 = 6."),
    ]),
    EX("5", "47", st("Find the mismatch: the model shows 2 and 4 objects, but the writing says 2 + 3 = 6.", "جد عدم التطابق: النموذج فيه 2 و4 أشياء لكن الكتابة 2 + 3 = 6.", "Trouve l'erreur : le modèle montre 2 et 4 objets, mais l'écriture dit 2 + 3 = 6."), [
        join(2, 4, total=False),
        T("The first part 2 is right. The second part should be 4, not 3.",
          "الجزء الأول 2 صحيح. الجزء الثاني يجب أن يكون 4 لا 3.",
          "La première partie 2 est juste. La deuxième doit être 4, pas 3."),
        F("2 + 4 = 6"),
    ]),
    EX("6", "47", st("Error detective: 3 apples and 1 apple, total 4, but the writing says 3 + 1 = 5.", "المحقق: 3 تفاحات وتفاحة، المجموع 4، لكن الكتابة 3 + 1 = 5.", "Détective : 3 pommes et 1 pomme, total 4, mais l'écriture dit 3 + 1 = 5."), [
        join(3, 1, "circle", "circle", "#e53935", "#e53935"),
        T("The parts are correct. The total is wrong. Count the whole: four.",
          "الجزآن صحيحان والمجموع خاطئ. نعدّ الكل: أربعة.",
          "Les parties sont justes, le total est faux. On compte le tout : quatre."),
        F("3 + 1 = 4"),
    ]),
    EX("7", "47", st("Challenge: draw two different pictures for 2 + 3 = 5.", "تحدٍّ: ارسم صورتين مختلفتين تمثّلان 2 + 3 = 5.", "Défi : fais deux images différentes pour 2 + 3 = 5."), [
        join(2, 3, "star", "star", "#fbc02d", "#43a047"),
        join(2, 3, "square", "circle", "#1e63d6", "#e53935"),
        T("The pictures do not have to look alike. The quantities and the relationship must stay the same.",
          "لا يجب أن تتشابه الصورتان. يجب أن تبقى الكميات والعلاقة نفسها.",
          "Les images n'ont pas à se ressembler. Les quantités et la relation doivent rester les mêmes."),
    ]),
    EX("8", "47", st("Final check: write 4 + 2 = 6, build 3 + 4 = 7, and tell the story of 2 + 5 = 7.", "تقييم أخير: اكتب 4 + 2 = 6، وابنِ 3 + 4 = 7، واحكِ قصة 2 + 5 = 7.", "Évaluation : écris 4 + 2 = 6, construis 3 + 4 = 7 et raconte 2 + 5 = 7."), [
        join(4, 2),
        join(3, 4, "circle", "circle", "#fb8c00", "#8e24aa"),
        T("The story: there were 2 objects, 5 more joined, and there are 7 altogether. The 2 and the 5 are the parts, and the 7 is the total.",
          "القصة: كان هناك شيئان، وانضمّ 5 آخرون، فصار المجموع 7. العددان 2 و5 جزآن، و7 هو المجموع.",
          "L'histoire : il y avait 2 objets, 5 de plus sont arrivés, il y en a 7 en tout. 2 et 5 sont les parties, 7 est le total."),
    ]),
]
