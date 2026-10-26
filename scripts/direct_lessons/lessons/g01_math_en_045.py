"""Grade 1 Mathematics — Add with 8 and 9."""
from scripts.direct_lessons.common import T, F, EX, st, tens, jumps

LESSON_ID = "G01-MATH-EN-045"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Add with 8 and 9", "ar": "الجمع مع 8 و9", "fr": "Additionner avec 8 et 9"}

THEORY = [
    ("8 and 9 are close to 10", "8 و9 قريبان من 10", "8 et 9 sont proches de 10", "114", [
        T("Hello, champion! Eight needs 2 more to make 10. Nine needs only 1 more to make 10. That is a great helper: when we add with 8 or 9, we can first complete a ten, and then add what is left.",
          "مرحبًا يا بطل! العدد 8 يحتاج إلى 2 ليصبح 10. والعدد 9 يحتاج إلى 1 فقط ليصبح 10. هذه مساعدة رائعة: عندما نجمع مع 8 أو 9 نكمل عشرة أولًا ثم نضيف الباقي.",
          "Bonjour champion ! 8 a besoin de 2 pour faire 10. 9 n'a besoin que de 1. C'est une belle aide : quand on additionne avec 8 ou 9, on complète d'abord une dizaine, puis on ajoute le reste."),
        F("8 + 2 = 10        9 + 1 = 10"),
    ]),
    ("9 + 4: move one counter", "9 + 4: ننقل قطعة واحدة", "9 + 4 : on déplace un jeton", "114", [
        T("9 + 4. The 9 needs 1 to reach 10, so we take 1 from the 4. Now the 4 becomes 3. So 9 + 4 is the same as 10 + 3 = 13. Nothing was created or lost: the one counter only moved.",
          "9 + 4. العدد 9 يحتاج إلى 1 ليبلغ 10، فنأخذ 1 من الـ4. فتصبح الـ4 ثلاثة. إذن 9 + 4 هي نفسها 10 + 3 = 13. لم يُخلق شيء ولم يضِع شيء: القطعة انتقلت فقط.",
          "9 + 4. Le 9 a besoin de 1 pour arriver à 10 : on prend 1 au 4, qui devient 3. Donc 9 + 4 = 10 + 3 = 13. Rien n'est créé ni perdu : le jeton a seulement changé de place."),
        tens(1, 3, eq=True),
        F("9 + 4 = 10 + 3 = 13"),
    ]),
    ("8 + 5: move two counters", "8 + 5: ننقل قطعتين", "8 + 5 : on déplace deux jetons", "115", [
        T("8 + 5. The 8 needs 2 to reach 10. We take 2 from the 5, and 3 remain. So 8 + 5 = 10 + 3 = 13. We can check on the number path: from 8 jump 5 times and land on 13.",
          "8 + 5. العدد 8 يحتاج إلى 2 ليبلغ 10. نأخذ 2 من الـ5 فيبقى 3. إذن 8 + 5 = 10 + 3 = 13. ونتحقق على مسار الأعداد: من 8 نقفز 5 مرات فنصل إلى 13.",
          "8 + 5. Le 8 a besoin de 2 : on les prend au 5, il reste 3. Donc 8 + 5 = 10 + 3 = 13. On vérifie sur la droite : de 8, cinq sauts, on arrive à 13."),
        tens(1, 3, eq=True),
        jumps(8, 5, hi=13),
        F("8 + 5 = 10 + 3 = 13"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Eight needs 2 to make 10; nine needs 1. Move that many units from the other number to complete the ten, then add what remains. The total stays the same.",
          "8 تحتاج إلى 2 لتصير 10 و9 تحتاج إلى 1. ننقل هذا العدد من العدد الآخر لإكمال العشرة ثم نضيف الباقي. ويبقى المجموع نفسه.",
          "8 a besoin de 2 pour faire 10, 9 de 1. On déplace ce nombre depuis l'autre nombre pour compléter la dizaine, puis on ajoute le reste. Le total ne change pas."),
        F("FIND WHAT MAKES TEN → MOVE IT → ADD THE REST → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "114", st("How many does 8 need to make 10? And 9?", "كم يحتاج 8 ليصبح 10؟ وكم يحتاج 9؟", "De combien 8 a-t-il besoin pour faire 10 ? Et 9 ?"), [
        F("8 + 2 = 10        9 + 1 = 10"),
        T("8 needs 2, 9 needs 1.", "8 تحتاج 2 و9 تحتاج 1.", "8 a besoin de 2, 9 de 1."),
    ]),
    EX("2", "114", st("Solve 9 + 3 by making ten.", "احسب 9 + 3 بإكمال العشرة.", "Calcule 9 + 3 en faisant dix."), [
        tens(1, 2, eq=True),
        T("Take 1 from the 3: 9 + 1 = 10, and 2 remain. 10 + 2 = 12.", "نأخذ 1 من الـ3: 9 + 1 = 10 ويبقى 2. 10 + 2 = 12.", "On prend 1 au 3 : 9 + 1 = 10, il reste 2. 10 + 2 = 12."),
    ]),
    EX("3", "114", st("Solve 9 + 6.", "احسب 9 + 6.", "Calcule 9 + 6."), [
        tens(1, 5, eq=True),
        T("Take 1 from the 6: 10, and 5 remain. 10 + 5 = 15.", "نأخذ 1 من الـ6: 10 ويبقى 5. 10 + 5 = 15.", "On prend 1 au 6 : 10, il reste 5. 10 + 5 = 15."),
    ]),
    EX("4", "115", st("Solve 8 + 4.", "احسب 8 + 4.", "Calcule 8 + 4."), [
        tens(1, 2, eq=True),
        T("Take 2 from the 4: 8 + 2 = 10, and 2 remain. 10 + 2 = 12.", "نأخذ 2 من الـ4: 8 + 2 = 10 ويبقى 2. 10 + 2 = 12.", "On prend 2 au 4 : 8 + 2 = 10, il reste 2. 10 + 2 = 12."),
    ]),
    EX("5", "115", st("Solve 8 + 7.", "احسب 8 + 7.", "Calcule 8 + 7."), [
        tens(1, 5, eq=True),
        T("Take 2 from the 7: 10, and 5 remain. 10 + 5 = 15.", "نأخذ 2 من الـ7: 10 ويبقى 5. 10 + 5 = 15.", "On prend 2 au 7 : 10, il reste 5. 10 + 5 = 15."),
    ]),
    EX("6", "115", st("Error check: 9 + 4 = 10 + 4 = 14. What went wrong?", "تحقّق من الخطأ: 9 + 4 = 10 + 4 = 14. ما الخطأ؟", "Vérifie l'erreur : 9 + 4 = 10 + 4 = 14. Où est l'erreur ?"), [
        T("The child added 1 to the 9 but did not take it from the 4. The 4 must become 3. The right way: 10 + 3 = 13.", "أضاف الطفل 1 إلى الـ9 لكنه لم ينقصه من الـ4. يجب أن تصبح الـ4 ثلاثة. الصحيح: 10 + 3 = 13.", "L'enfant a ajouté 1 au 9 sans l'enlever au 4. Le 4 doit devenir 3. Juste : 10 + 3 = 13."),
        tens(1, 3, eq=True),
    ]),
    EX("7", "115", st("Challenge: 9 + 9.", "تحدٍّ: 9 + 9.", "Défi : 9 + 9."), [
        tens(1, 8, eq=True),
        T("Take 1 from the second 9: 9 + 1 = 10, and 8 remain. 10 + 8 = 18.", "نأخذ 1 من الـ9 الثانية: 9 + 1 = 10 ويبقى 8. 10 + 8 = 18.", "On prend 1 au second 9 : 10, il reste 8. 10 + 8 = 18."),
    ]),
    EX("8", "115", st("Final check: solve 9 + 5 and explain the moved unit.", "تقييم أخير: احسب 9 + 5 واشرح الوحدة المنقولة.", "Évaluation : calcule 9 + 5 et explique l'unité déplacée."), [
        tens(1, 4, eq=True),
        T("One unit moved from the 5 to the 9, so 9 became 10 and 5 became 4. 10 + 4 = 14.", "انتقلت وحدة من الـ5 إلى الـ9 فصارت 9 عشرة وصارت 5 أربعة. 10 + 4 = 14.", "Une unité est passée du 5 au 9 : le 9 devient 10 et le 5 devient 4. 10 + 4 = 14."),
    ]),
]
