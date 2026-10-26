"""Grade 1 Mathematics — Addition without carry-out."""
from scripts.direct_lessons.common import T, F, EX, st, tens

LESSON_ID = "G01-MATH-EN-050"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Addition without carry-out", "ar": "الجمع دون حمل", "fr": "Addition sans retenue"}

THEORY = [
    ("Tens with tens, ones with ones", "عشرات مع عشرات وآحاد مع آحاد", "Dizaines avec dizaines, unités avec unités", "126", [
        tens(2, 3, tag="A", eq=True),
        tens(1, 4, tag="B", eq=True),
        T("Hello, champion! Let us add 23 and 14. First we find the tens and the ones. 23 is 2 tens and 3 ones. 14 is 1 ten and 4 ones. Now: ones with ones: 3 + 4 = 7. Tens with tens: 2 + 1 = 3. The answer is 3 tens and 7 ones: 37.",
          "مرحبًا يا بطل! لنجمع 23 و14. أولًا نجد العشرات والآحاد. 23 هي عشرتان و3 آحاد. و14 هي عشرة و4 آحاد. الآن: آحاد مع آحاد: 3 + 4 = 7. وعشرات مع عشرات: 2 + 1 = 3. الجواب 3 عشرات و7 آحاد: 37.",
          "Additionnons 23 et 14. D'abord les dizaines et les unités. 23 = 2 dizaines et 3 unités. 14 = 1 dizaine et 4 unités. Unités avec unités : 3 + 4 = 7. Dizaines avec dizaines : 2 + 1 = 3. Réponse : 3 dizaines et 7 unités : 37."),
        tens(3, 7, tag="C", eq=True),
        F("23 + 14 = 37"),
    ]),
    ("No new ten is needed", "لا نحتاج إلى عشرة جديدة", "Pas de nouvelle dizaine", "126", [
        T("Why is it easy? Because 3 + 4 = 7 is less than 10. The ones did not make a new ten, so we did not need to regroup. We simply put the tens and the ones together.",
          "لماذا هو سهل؟ لأن 3 + 4 = 7 وهي أقل من 10. لم تكوّن الآحاد عشرة جديدة فلم نحتج إلى إعادة التجميع. وضعنا العشرات مع العشرات والآحاد مع الآحاد فقط.",
          "Pourquoi est-ce facile ? Parce que 3 + 4 = 7 est inférieur à 10. Les unités n'ont pas formé de nouvelle dizaine : pas de regroupement. On réunit simplement dizaines et unités."),
        F("ones: 3 + 4 = 7 < 10     tens: 2 + 1 = 3"),
    ]),
    ("Keep each place in its column", "كل رقم في خانته", "Chaque chiffre à sa place", "127", [
        tens(4, 2, tag="A", eq=True),
        tens(2, 5, tag="B", eq=True),
        T("42 + 25. The ones: 2 + 5 = 7. The tens: 4 + 2 = 6. So 67. We never add a tens digit to a ones digit.",
          "42 + 25. الآحاد: 2 + 5 = 7. والعشرات: 4 + 2 = 6. إذن 67. لا نجمع أبدًا رقم العشرات مع رقم الآحاد.",
          "42 + 25. Unités : 2 + 5 = 7. Dizaines : 4 + 2 = 6. Donc 67. On n'additionne jamais un chiffre des dizaines avec un chiffre des unités."),
        tens(6, 7, tag="C", eq=True),
        F("42 + 25 = 67"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("When the ones add up to less than ten, no new ten is formed. We add ones to ones and tens to tens, and write the number.",
          "عندما يكون مجموع الآحاد أقل من عشرة لا تتكوّن عشرة جديدة. نجمع الآحاد مع الآحاد والعشرات مع العشرات ثم نكتب العدد.",
          "Quand les unités font moins de dix, aucune nouvelle dizaine ne se forme. On additionne unités avec unités, dizaines avec dizaines, puis on écrit le nombre."),
        F("ONES + ONES → TENS + TENS → WRITE THE NUMBER"),
    ]),
]

EXERCISES = [
    EX("1", "126", st("Split 35 and 12 into tens and ones.", "حلّل 35 و12 إلى عشرات وآحاد.", "Décompose 35 et 12 en dizaines et unités."), [
        tens(3, 5, tag="A", eq=True),
        tens(1, 2, tag="B", eq=True),
        F("35 = 3 tens + 5 ones      12 = 1 ten + 2 ones"),
    ]),
    EX("2", "126", st("Solve 21 + 13.", "احسب 21 + 13.", "Calcule 21 + 13."), [
        tens(3, 4, eq=True),
        T("Ones: 1 + 3 = 4. Tens: 2 + 1 = 3. So 34.", "الآحاد: 1 + 3 = 4. العشرات: 2 + 1 = 3. إذن 34.", "Unités : 1 + 3 = 4. Dizaines : 2 + 1 = 3. Donc 34."),
    ]),
    EX("3", "126", st("Solve 32 + 15.", "احسب 32 + 15.", "Calcule 32 + 15."), [
        tens(4, 7, eq=True),
        T("Ones: 2 + 5 = 7. Tens: 3 + 1 = 4. So 47.", "الآحاد: 2 + 5 = 7. العشرات: 3 + 1 = 4. إذن 47.", "Unités : 2 + 5 = 7. Dizaines : 3 + 1 = 4. Donc 47."),
    ]),
    EX("4", "127", st("Solve 41 + 26.", "احسب 41 + 26.", "Calcule 41 + 26."), [
        tens(6, 7, eq=True),
        T("Ones: 1 + 6 = 7. Tens: 4 + 2 = 6. So 67.", "الآحاد: 1 + 6 = 7. العشرات: 4 + 2 = 6. إذن 67.", "Unités : 1 + 6 = 7. Dizaines : 4 + 2 = 6. Donc 67."),
    ]),
    EX("5", "127", st("Solve 50 + 18.", "احسب 50 + 18.", "Calcule 50 + 18."), [
        tens(6, 8, eq=True),
        T("Ones: 0 + 8 = 8. Tens: 5 + 1 = 6. So 68.", "الآحاد: 0 + 8 = 8. العشرات: 5 + 1 = 6. إذن 68.", "Unités : 0 + 8 = 8. Dizaines : 5 + 1 = 6. Donc 68."),
    ]),
    EX("6", "127", st("Error check: 23 + 14 = 10. A child added 2 + 3 + 1 + 4. What went wrong?", "تحقّق من الخطأ: 23 + 14 = 10. جمع الطفل 2 + 3 + 1 + 4. ما الخطأ؟", "Vérifie l'erreur : 23 + 14 = 10. L'enfant a fait 2 + 3 + 1 + 4. Où est l'erreur ?"), [
        tens(3, 7, eq=True),
        T("He mixed tens digits with ones digits. Tens go with tens (2 + 1 = 3 tens) and ones with ones (3 + 4 = 7). The answer is 37.", "خلط أرقام العشرات بأرقام الآحاد. العشرات مع العشرات (2 + 1 = 3 عشرات) والآحاد مع الآحاد (3 + 4 = 7). الجواب 37.", "Il a mélangé dizaines et unités. Dizaines avec dizaines (2 + 1 = 3), unités avec unités (3 + 4 = 7). Réponse : 37."),
    ]),
    EX("7", "127", st("Challenge: 16 + 22 + 11.", "تحدٍّ: 16 + 22 + 11.", "Défi : 16 + 22 + 11."), [
        tens(4, 9, eq=True),
        T("Ones: 6 + 2 + 1 = 9. Tens: 1 + 2 + 1 = 4. So 49.", "الآحاد: 6 + 2 + 1 = 9. العشرات: 1 + 2 + 1 = 4. إذن 49.", "Unités : 6 + 2 + 1 = 9. Dizaines : 1 + 2 + 1 = 4. Donc 49."),
    ]),
    EX("8", "127", st("Final check: solve 33 + 24 and explain why no regrouping is needed.", "تقييم أخير: احسب 33 + 24 واشرح لماذا لا حاجة إلى إعادة التجميع.", "Évaluation : calcule 33 + 24 et explique pourquoi aucun regroupement n'est nécessaire."), [
        tens(5, 7, eq=True),
        T("3 + 4 = 7 ones, fewer than ten, so no new ten. 3 + 2 = 5 tens. The answer is 57.", "3 + 4 = 7 آحاد وهي أقل من عشرة، فلا عشرة جديدة. 3 + 2 = 5 عشرات. الجواب 57.", "3 + 4 = 7 unités, moins de dix : pas de nouvelle dizaine. 3 + 2 = 5 dizaines. Réponse : 57."),
    ]),
]
