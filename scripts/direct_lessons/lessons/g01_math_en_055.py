"""Grade 1 Mathematics — Addition with carry-out."""
from scripts.direct_lessons.common import T, F, EX, st, tens

LESSON_ID = "G01-MATH-EN-055"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Addition with carry-out", "ar": "الجمع مع حمل", "fr": "Addition avec retenue"}

THEORY = [
    ("When the ones make ten or more", "عندما تبلغ الآحاد عشرة أو أكثر", "Quand les unités font dix ou plus", "140", [
        tens(2, 8, tag="A", eq=True),
        tens(1, 5, tag="B", eq=True),
        T("Hello, champion! Let us add 28 and 15. 28 is 2 tens and 8 ones. 15 is 1 ten and 5 ones. First the ones: 8 + 5 = 13. That is more than ten! 13 ones is too many to stay as loose ones.",
          "مرحبًا يا بطل! لنجمع 28 و15. العدد 28 هو عشرتان و8 آحاد. و15 هو عشرة و5 آحاد. أولًا الآحاد: 8 + 5 = 13. هذا أكثر من عشرة! 13 واحدًا كثيرة لتبقى آحادًا منفردة.",
          "Additionnons 28 et 15. 28 = 2 dizaines et 8 unités. 15 = 1 dizaine et 5 unités. D'abord les unités : 8 + 5 = 13. C'est plus que dix ! 13 unités, c'est trop pour rester seules."),
        F("8 + 5 = 13 ones"),
    ]),
    ("Exchange ten ones for one ten", "نبدّل عشرة آحاد بعشرة واحدة", "Échanger dix unités contre une dizaine", "140", [
        tens(0, 10, bundled=False, eq=True),
        tens(1, 0, eq=True),
        T("We take exactly ten of the 13 ones and tie them into a new ten. The 3 remaining ones stay in the ones place. So 13 ones = 1 ten and 3 ones. The total did not change.",
          "نأخذ عشرة آحاد بالضبط من الـ13 ونربطها في عشرة جديدة. تبقى 3 آحاد في خانة الآحاد. إذن 13 واحدًا = عشرة و3 آحاد. لم يتغير المجموع.",
          "On prend exactement dix des 13 unités et on les attache en une nouvelle dizaine. Les 3 unités restantes restent aux unités. Donc 13 unités = 1 dizaine et 3 unités. Le total n'a pas changé."),
    ]),
    ("Add all the tens", "نجمع كل العشرات", "Additionner toutes les dizaines", "141", [
        tens(4, 3, eq=True),
        T("Now the tens: 2 tens + 1 ten + the new ten = 4 tens. Ones left: 3. The answer is 43. So 28 + 15 = 43.",
          "الآن العشرات: عشرتان + عشرة + العشرة الجديدة = 4 عشرات. الآحاد الباقية: 3. الجواب 43. إذن 28 + 15 = 43.",
          "Maintenant les dizaines : 2 + 1 + la nouvelle = 4 dizaines. Unités restantes : 3. Réponse : 43. Donc 28 + 15 = 43."),
        F("28 + 15 = 43"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("When the ones add up to 10 or more, regroup exactly ten ones as one ten. The new ten joins the tens, and only the remaining ones stay as ones. Do not forget the carried ten, and do not count it twice.",
          "عندما يبلغ مجموع الآحاد 10 أو أكثر نعيد تجميع عشرة آحاد بالضبط في عشرة واحدة. تنضم العشرة الجديدة إلى العشرات وتبقى الآحاد المتبقية فقط. لا ننسى العشرة المحمولة ولا نعدّها مرتين.",
          "Quand les unités font 10 ou plus, on regroupe exactement dix unités en une dizaine. La nouvelle dizaine rejoint les dizaines, seules les unités restantes restent. On n'oublie pas la dizaine retenue et on ne la compte pas deux fois."),
        F("ADD THE ONES → TEN OR MORE? → EXCHANGE FOR A TEN → ADD ALL THE TENS"),
    ]),
]

EXERCISES = [
    EX("1", "140", st("Add the ones of 17 + 6. How many ones?", "اجمع آحاد 17 + 6. كم واحدًا؟", "Additionne les unités de 17 + 6. Combien ?"), [
        F("7 + 6 = 13 ones"),
        T("13 ones is more than ten, so we regroup.", "13 واحدًا أكثر من عشرة فنعيد التجميع.", "13 unités, plus de dix : on regroupe."),
    ]),
    EX("2", "140", st("Solve 17 + 6.", "احسب 17 + 6.", "Calcule 17 + 6."), [
        tens(2, 3, eq=True),
        T("13 ones = 1 ten + 3 ones. Tens: 1 + 1 = 2. Answer 23.", "13 واحدًا = عشرة + 3 آحاد. العشرات: 1 + 1 = 2. الجواب 23.", "13 unités = 1 dizaine + 3 unités. Dizaines : 1 + 1 = 2. Réponse : 23."),
    ]),
    EX("3", "141", st("Solve 25 + 17.", "احسب 25 + 17.", "Calcule 25 + 17."), [
        tens(4, 2, eq=True),
        T("5 + 7 = 12 ones = 1 ten + 2 ones. Tens: 2 + 1 + 1 = 4. Answer 42.", "5 + 7 = 12 واحدًا = عشرة + واحدان. العشرات: 2 + 1 + 1 = 4. الجواب 42.", "5 + 7 = 12 unités = 1 dizaine + 2 unités. Dizaines : 2 + 1 + 1 = 4. Réponse : 42."),
    ]),
    EX("4", "141", st("Solve 38 + 14.", "احسب 38 + 14.", "Calcule 38 + 14."), [
        tens(5, 2, eq=True),
        T("8 + 4 = 12 ones. Tens: 3 + 1 + 1 = 5. Answer 52.", "8 + 4 = 12 واحدًا. العشرات: 3 + 1 + 1 = 5. الجواب 52.", "8 + 4 = 12 unités. Dizaines : 3 + 1 + 1 = 5. Réponse : 52."),
    ]),
    EX("5", "142", st("Solve 29 + 9.", "احسب 29 + 9.", "Calcule 29 + 9."), [
        tens(3, 8, eq=True),
        T("9 + 9 = 18 ones = 1 ten + 8 ones. Tens: 2 + 1 = 3. Answer 38.", "9 + 9 = 18 واحدًا = عشرة + 8 آحاد. العشرات: 2 + 1 = 3. الجواب 38.", "9 + 9 = 18 unités = 1 dizaine + 8 unités. Dizaines : 2 + 1 = 3. Réponse : 38."),
    ]),
    EX("6", "142", st("Error check: 28 + 15 = 33. What was forgotten?", "تحقّق من الخطأ: 28 + 15 = 33. ماذا نُسي؟", "Vérifie l'erreur : 28 + 15 = 33. Qu'a-t-on oublié ?"), [
        tens(4, 3, eq=True),
        T("The child forgot the carried ten. 2 + 1 = 3 tens is not enough: we must add the new ten too, so 4 tens. The answer is 43.", "نسي الطفل العشرة المحمولة. 2 + 1 = 3 عشرات لا تكفي: يجب أن نضيف العشرة الجديدة أيضًا فتصير 4 عشرات. الجواب 43.", "L'enfant a oublié la dizaine retenue. 2 + 1 = 3 dizaines ne suffit pas : il faut ajouter la nouvelle, soit 4. Réponse : 43."),
    ]),
    EX("7", "143", st("Challenge: 36 + 27.", "تحدٍّ: 36 + 27.", "Défi : 36 + 27."), [
        tens(6, 3, eq=True),
        T("6 + 7 = 13 ones = 1 ten + 3 ones. Tens: 3 + 2 + 1 = 6. Answer 63.", "6 + 7 = 13 واحدًا = عشرة + 3 آحاد. العشرات: 3 + 2 + 1 = 6. الجواب 63.", "6 + 7 = 13 unités. Dizaines : 3 + 2 + 1 = 6. Réponse : 63."),
    ]),
    EX("8", "143", st("Final check: solve 19 + 14 and explain the regrouping.", "تقييم أخير: احسب 19 + 14 واشرح إعادة التجميع.", "Évaluation : calcule 19 + 14 et explique le regroupement."), [
        tens(3, 3, eq=True),
        T("9 + 4 = 13 ones: ten ones become one ten, 3 ones remain. Tens: 1 + 1 + 1 = 3. Answer 33.", "9 + 4 = 13 واحدًا: عشرة آحاد تصبح عشرة واحدة وتبقى 3 آحاد. العشرات: 1 + 1 + 1 = 3. الجواب 33.", "9 + 4 = 13 unités : dix unités deviennent une dizaine, 3 restent. Dizaines : 1 + 1 + 1 = 3. Réponse : 33."),
    ]),
]
