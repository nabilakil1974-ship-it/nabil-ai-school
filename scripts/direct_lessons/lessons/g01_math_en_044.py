"""Grade 1 Mathematics — Addition of several numbers."""
from scripts.direct_lessons.common import T, F, EX, st, tens, jumps, numpath

LESSON_ID = "G01-MATH-EN-044"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Addition of several numbers", "ar": "جمع عدة أعداد", "fr": "Addition de plusieurs nombres"}

THEORY = [
    ("Three groups", "ثلاث مجموعات", "Trois groupes", "112", [
        F("2   +   3   +   4"),
        T("Hello, champion! Here are three groups: 2, 3 and 4. How many altogether? We do not restart from one each time. We join step by step: first 2 + 3 = 5. This is the running total. Then we add the next group: 5 + 4 = 9.",
          "مرحبًا يا بطل! هنا ثلاث مجموعات: 2 و3 و4. كم المجموع؟ لا نبدأ من الواحد في كل مرة. نجمع خطوة خطوة: أولًا 2 + 3 = 5. هذا هو المجموع الجاري. ثم نضيف المجموعة التالية: 5 + 4 = 9.",
          "Bonjour champion ! Trois groupes : 2, 3 et 4. Combien en tout ? On ne recommence pas à un à chaque fois. On réunit pas à pas : d'abord 2 + 3 = 5, c'est le total provisoire. Puis on ajoute le groupe suivant : 5 + 4 = 9."),
        jumps(5, 4, hi=10),
        F("2 + 3 = 5      5 + 4 = 9"),
    ]),
    ("Every group exactly once", "كل مجموعة مرة واحدة بالضبط", "Chaque groupe exactement une fois", "112", [
        T("The intermediate total 5 must contain exactly the groups already added: the 2 and the 3. The final total 9 contains all three groups, each one once. If we forget a group or count one twice, the answer is wrong.",
          "المجموع الجاري 5 يجب أن يحتوي بالضبط المجموعتين المضافتين: 2 و3. والمجموع النهائي 9 يحتوي المجموعات الثلاث كل واحدة مرة واحدة. إذا نسينا مجموعة أو عددنا واحدة مرتين صار الجواب خطأ.",
          "Le total provisoire 5 contient exactement les groupes déjà ajoutés : 2 et 3. Le total final 9 contient les trois groupes, chacun une fois. Si on oublie un groupe ou si on en compte un deux fois, la réponse est fausse."),
        F("2 + 3 + 4 = 9"),
    ]),
    ("Tens work too", "العشرات تصلح أيضًا", "Les dizaines aussi", "113", [
        tens(1, 0, tag="A", eq=True),
        tens(2, 0, tag="B", eq=True),
        tens(1, 5, tag="C", eq=True),
        T("10 + 20 + 5: first 10 + 20 = 30, then 30 + 5 = 35. The 5 is a loose one, so it goes after the tens. We kept every group once.",
          "10 + 20 + 5: أولًا 10 + 20 = 30 ثم 30 + 5 = 35. الـ5 آحاد منفردة فتأتي بعد العشرات. حافظنا على كل مجموعة مرة واحدة.",
          "10 + 20 + 5 : d'abord 10 + 20 = 30, puis 30 + 5 = 35. Le 5 est fait d'unités seules : on l'ajoute après les dizaines. Chaque groupe est pris une fois."),
        F("10 + 20 + 5 = 35"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("To add several numbers: add two groups, keep the running total, add the next group, and so on. Make sure every addend is used exactly once.",
          "لجمع عدة أعداد: نجمع مجموعتين ونحتفظ بالمجموع الجاري ثم نضيف المجموعة التالية وهكذا. ونتأكد أن كل عدد استُعمل مرة واحدة بالضبط.",
          "Pour additionner plusieurs nombres : on additionne deux groupes, on garde le total provisoire, on ajoute le suivant, etc. Chaque nombre est utilisé exactement une fois."),
        F("ADD TWO → KEEP THE TOTAL → ADD THE NEXT → CHECK EVERY GROUP"),
    ]),
]

EXERCISES = [
    EX("1", "112", st("Solve 1 + 2 + 3.", "احسب 1 + 2 + 3.", "Calcule 1 + 2 + 3."), [
        numpath(["1", "3", "6"], hi=2, size=60),
        T("1 + 2 = 3, then 3 + 3 = 6.", "1 + 2 = 3 ثم 3 + 3 = 6.", "1 + 2 = 3, puis 3 + 3 = 6."),
    ]),
    EX("2", "112", st("Solve 4 + 1 + 3.", "احسب 4 + 1 + 3.", "Calcule 4 + 1 + 3."), [
        T("4 + 1 = 5, then 5 + 3 = 8.", "4 + 1 = 5 ثم 5 + 3 = 8.", "4 + 1 = 5, puis 5 + 3 = 8."),
        F("4 + 1 + 3 = 8"),
    ]),
    EX("3", "112", st("Solve 2 + 2 + 2 + 2.", "احسب 2 + 2 + 2 + 2.", "Calcule 2 + 2 + 2 + 2."), [
        numpath(["2", "4", "6", "8"], hi=3, size=56),
        T("The running total grows by 2 each time: 2, 4, 6, 8.", "ينمو المجموع الجاري بمقدار 2 كل مرة: 2، 4، 6، 8.", "Le total augmente de 2 à chaque fois : 2, 4, 6, 8."),
    ]),
    EX("4", "113", st("Solve 10 + 10 + 10.", "احسب 10 + 10 + 10.", "Calcule 10 + 10 + 10."), [
        tens(3, 0, eq=True),
        T("3 tens = 30.", "3 عشرات = 30.", "3 dizaines = 30."),
    ]),
    EX("5", "113", st("Solve 20 + 10 + 4.", "احسب 20 + 10 + 4.", "Calcule 20 + 10 + 4."), [
        tens(3, 4, eq=True),
        T("20 + 10 = 30, then 30 + 4 = 34.", "20 + 10 = 30 ثم 30 + 4 = 34.", "20 + 10 = 30, puis 30 + 4 = 34."),
    ]),
    EX("6", "113", st("Error check: 3 + 2 + 4 = 5. Which group was left out?", "تحقّق من الخطأ: 3 + 2 + 4 = 5. أيّ مجموعة أُهملت؟", "Vérifie l'erreur : 3 + 2 + 4 = 5. Quel groupe a été oublié ?"), [
        T("3 + 2 = 5 and the child stopped. The group 4 was left out. The correct total is 5 + 4 = 9.", "3 + 2 = 5 وتوقف الطفل. أُهملت المجموعة 4. المجموع الصحيح 5 + 4 = 9.", "3 + 2 = 5 et l'enfant s'est arrêté : le groupe 4 est oublié. Le bon total est 5 + 4 = 9."),
        F("3 + 2 + 4 = 9"),
    ]),
    EX("7", "113", st("Challenge: 5 + 5 + 5 + 5.", "تحدٍّ: 5 + 5 + 5 + 5.", "Défi : 5 + 5 + 5 + 5."), [
        T("5 + 5 = 10, then 10 + 5 = 15, then 15 + 5 = 20.", "5 + 5 = 10 ثم 10 + 5 = 15 ثم 15 + 5 = 20.", "5 + 5 = 10, puis 15, puis 20."),
        F("5 + 5 + 5 + 5 = 20"),
    ]),
    EX("8", "113", st("Final check: solve 3 + 3 + 3 and explain the intermediate total.", "تقييم أخير: احسب 3 + 3 + 3 واشرح المجموع الجاري.", "Évaluation : calcule 3 + 3 + 3 et explique le total provisoire."), [
        numpath(["3", "6", "9"], hi=2, size=60),
        T("3 + 3 = 6 is the intermediate total (two groups). Then 6 + 3 = 9 includes all three groups once.", "3 + 3 = 6 هو المجموع الجاري (مجموعتان). ثم 6 + 3 = 9 يشمل المجموعات الثلاث مرة واحدة.", "3 + 3 = 6 est le total provisoire (deux groupes). Puis 6 + 3 = 9 contient les trois groupes une fois."),
    ]),
]
