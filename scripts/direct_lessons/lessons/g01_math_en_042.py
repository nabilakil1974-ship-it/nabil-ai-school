"""Grade 1 Mathematics — Add a number of one digit."""
from scripts.direct_lessons.common import T, F, EX, st, tens, numpath, jumps

LESSON_ID = "G01-MATH-EN-042"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Add a number of one digit", "ar": "جمع عدد من رقم واحد", "fr": "Additionner un nombre d'un chiffre"}

THEORY = [
    ("Keep the start, count on the ones", "نحتفظ بالبداية ونعدّ الآحاد", "Garder le départ, compter les unités", "108", [
        jumps(3, 4, hi=10),
        T("Hello, champion! We start with 3 and add 4. We keep the 3 and make 4 jumps, one for each added one: 4, 5, 6, 7. We land on 7, so 3 + 4 = 7. Mark the starting point first, and then count only the added ones.",
          "مرحبًا يا بطل! نبدأ بـ3 ونضيف 4. نحتفظ بالعدد 3 ونقفز 4 قفزات، قفزة لكل واحد مضاف: 4، 5، 6، 7. نصل إلى 7، إذن 3 + 4 = 7. نضع علامة على نقطة البداية أولًا ثم نعدّ الآحاد المضافة فقط.",
          "Bonjour champion ! On part de 3 et on ajoute 4. On garde 3 et on fait 4 sauts, un par unité ajoutée : 4, 5, 6, 7. On arrive à 7 : 3 + 4 = 7. On marque d'abord le départ, puis on ne compte que les unités ajoutées."),
    ]),
    ("A bigger start", "بداية أكبر", "Un départ plus grand", "108", [
        jumps(8, 5, hi=13),
        T("Start at 8 and add 5: 9, 10, 11, 12, 13. Five jumps, and we land on 13. So 8 + 5 = 13. The number of jumps equals the number we add.",
          "نبدأ من 8 ونضيف 5: 9، 10، 11، 12، 13. خمس قفزات ونهبط عند 13. إذن 8 + 5 = 13. عدد القفزات يساوي العدد الذي نضيفه.",
          "On part de 8 et on ajoute 5 : 9, 10, 11, 12, 13. Cinq sauts, et on arrive à 13. Donc 8 + 5 = 13. Le nombre de sauts est égal au nombre ajouté."),
    ]),
    ("Tens and ones", "العشرات والآحاد", "Dizaines et unités", "109", [
        tens(3, 4, eq=True),
        tens(3, 9, eq=True),
        T("Now a bigger number: 34 + 5. 34 is 3 tens and 4 ones. We keep the tens and add the 5 ones: 4 + 5 = 9 ones. So we get 3 tens and 9 ones, which is 39.",
          "الآن عدد أكبر: 34 + 5. العدد 34 هو 3 عشرات و4 آحاد. نحتفظ بالعشرات ونضيف 5 آحاد: 4 + 5 = 9 آحاد. فنحصل على 3 عشرات و9 آحاد أي 39.",
          "Un nombre plus grand : 34 + 5. 34, c'est 3 dizaines et 4 unités. On garde les dizaines et on ajoute 5 unités : 4 + 5 = 9 unités. On obtient 3 dizaines et 9 unités, soit 39."),
        numpath(["34", "35", "36", "37", "38", "39"], hi=5, size=44),
        F("34 + 5 = 39"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("To add a one-digit number, keep the starting number and count on the added ones. Each jump is one. At the end, check that the starting number plus the jumps gives the sum.",
          "لجمع عدد من رقم واحد نحتفظ بالعدد الأول ونعدّ الآحاد المضافة. كل قفزة تساوي واحدًا. وفي النهاية نتحقق أن العدد الأول مع القفزات يعطي المجموع.",
          "Pour ajouter un nombre d'un chiffre, on garde le nombre de départ et on compte les unités ajoutées. Chaque saut vaut un. À la fin, on vérifie."),
        F("MARK THE START → JUMP ONE BY ONE → LAND → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "108", st("Solve 2 + 5 with jumps.", "احسب 2 + 5 بالقفزات.", "Calcule 2 + 5 avec des sauts."), [
        jumps(2, 5, hi=10),
        T("Start at 2 and jump 5 times: 3, 4, 5, 6, 7. So 2 + 5 = 7.", "نبدأ من 2 ونقفز 5 مرات: 3، 4، 5، 6، 7. إذن 2 + 5 = 7.", "On part de 2 et on saute 5 fois : 3, 4, 5, 6, 7. Donc 2 + 5 = 7."),
    ]),
    EX("2", "108", st("Solve 6 + 3.", "احسب 6 + 3.", "Calcule 6 + 3."), [
        jumps(6, 3, hi=10),
        T("From 6 jump three times: 7, 8, 9. So 6 + 3 = 9.", "من 6 نقفز ثلاث مرات: 7، 8، 9. إذن 6 + 3 = 9.", "De 6, trois sauts : 7, 8, 9. Donc 6 + 3 = 9."),
    ]),
    EX("3", "108", st("Solve 9 + 4.", "احسب 9 + 4.", "Calcule 9 + 4."), [
        jumps(9, 4, hi=13),
        T("From 9 jump four times: 10, 11, 12, 13. So 9 + 4 = 13.", "من 9 نقفز أربع مرات: 10، 11، 12، 13. إذن 9 + 4 = 13.", "De 9, quatre sauts : 10, 11, 12, 13. Donc 9 + 4 = 13."),
    ]),
    EX("4", "109", st("Solve 21 + 3 with tens and ones.", "احسب 21 + 3 بالعشرات والآحاد.", "Calcule 21 + 3 avec dizaines et unités."), [
        tens(2, 1, eq=True),
        tens(2, 4, eq=True),
        T("21 is 2 tens and 1 one. Add 3 ones: 1 + 3 = 4 ones. So 2 tens and 4 ones, which is 24.", "21 هي عشرتان وواحد. نضيف 3 آحاد: 1 + 3 = 4 آحاد. فنحصل على عشرتين و4 آحاد أي 24.", "21, c'est 2 dizaines et 1 unité. On ajoute 3 unités : 4 unités. Donc 24."),
    ]),
    EX("5", "109", st("Solve 45 + 4.", "احسب 45 + 4.", "Calcule 45 + 4."), [
        tens(4, 5, eq=True),
        tens(4, 9, eq=True),
        T("5 ones + 4 ones = 9 ones, and the 4 tens stay. The answer is 49.", "5 آحاد + 4 آحاد = 9 آحاد وتبقى 4 العشرات. الجواب 49.", "5 unités + 4 unités = 9 unités, les 4 dizaines restent. Réponse : 49."),
    ]),
    EX("6", "109", st("Error check: a child says 3 + 4 = 6 because he counted the 3 as a jump. What went wrong?", "تحقّق من الخطأ: قال طفل 3 + 4 = 6 لأنه عدّ الرقم 3 قفزة. ما الخطأ؟", "Vérifie l'erreur : un enfant dit 3 + 4 = 6 car il a compté le 3 comme un saut. Où est l'erreur ?"), [
        jumps(3, 4, hi=10),
        T("He counted the starting point as a jump. The start is marked first and is not counted. Only 4 jumps: 7.", "عدّ نقطة البداية قفزة. البداية تُعلَّم أولًا ولا تُعدّ. هناك 4 قفزات فقط: 7.", "Il a compté le départ comme un saut. Le départ est marqué mais pas compté. Seulement 4 sauts : 7."),
    ]),
    EX("7", "109", st("Challenge: 50 + 6.", "تحدٍّ: 50 + 6.", "Défi : 50 + 6."), [
        tens(5, 6, eq=True),
        T("50 is 5 tens and no ones. Add 6 ones: 56.", "العدد 50 هو 5 عشرات وبلا آحاد. نضيف 6 آحاد: 56.", "50, c'est 5 dizaines sans unité. On ajoute 6 unités : 56."),
    ]),
    EX("8", "109", st("Final check: solve 7 + 5 and 32 + 6 and verify with jumps or models.", "تقييم أخير: احسب 7 + 5 و32 + 6 وتحقّق بالقفزات أو بالنماذج.", "Évaluation : calcule 7 + 5 et 32 + 6 et vérifie avec des sauts ou des modèles."), [
        jumps(7, 5, hi=12),
        tens(3, 8, eq=True),
        F("7 + 5 = 12      32 + 6 = 38"),
    ]),
]
