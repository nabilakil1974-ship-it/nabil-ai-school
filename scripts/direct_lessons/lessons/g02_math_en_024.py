"""Grade 2 Mathematics — Subtraction: calculation technique (1), with exchange."""
from scripts.direct_lessons.common import T, F, EX, st, tens
from scripts.direct_lessons.lessons.g02_math_en_017 import sub

LESSON_ID = "G02-MATH-EN-024"
GRADE = 2
SUBJECT = "math"
TITLES = {"en": "Subtraction: calculation technique (1)", "ar": "الطرح: تقنية الحساب (1)", "fr": "Soustraction : technique de calcul (1)"}

THEORY = [
    ("When the ones are not enough", "عندما لا تكفي الآحاد", "Quand les unités ne suffisent pas", "52", [
        tens(3, 4, eq=True),
        T("Hello, champion! 34 − 16. I have 3 tens and 4 ones, and I want to take away 6 ones. But 4 ones are not enough! What can one ten become? Ten ones. So 34 = 2 tens + 14 ones. Now 14 − 6 = 8 ones, and 2 − 1 = 1 ten. The answer is 18.",
          "مرحبًا يا بطل! 34 − 16. عندي 3 عشرات و4 آحاد وأريد أن آخذ 6 آحاد. لكن 4 آحاد لا تكفي! ماذا تصبح عشرة واحدة؟ تصبح عشرة آحاد. إذن 34 = عشرتان + 14 واحدًا. الآن 14 − 6 = 8 آحاد و2 − 1 = عشرة. الجواب 18.",
          "34 − 16. J'ai 3 dizaines et 4 unités et je veux retirer 6 unités. Mais 4 unités ne suffisent pas ! Que peut devenir une dizaine ? Dix unités. Donc 34 = 2 dizaines + 14 unités. Alors 14 − 6 = 8 unités et 2 − 1 = 1 dizaine. Réponse : 18."),
        tens(2, 14, eq=True),
        sub(34, 16),
    ]),
    ("Exchange does not change the value", "التبديل لا يغيّر القيمة", "L'échange ne change pas la valeur", "52", [
        F("43 = 4 tens + 3 ones = 3 tens + 13 ones"),
        T("Exchanging one ten for ten ones changes the form, not the value. The tens go down by exactly 1 and the ones go up by exactly 10. So 56 = 4 tens + 16 ones and 78 = 6 tens + 18 ones.",
          "تبديل عشرة واحدة بعشرة آحاد يغيّر الشكل لا القيمة. تنقص العشرات بواحدة بالضبط وتزيد الآحاد بعشرة بالضبط. إذن 56 = 4 عشرات + 16 واحدًا و78 = 6 عشرات + 18 واحدًا.",
          "Échanger une dizaine contre dix unités change la forme, pas la valeur. Les dizaines baissent d'exactement 1, les unités montent de 10. Donc 56 = 4 dizaines + 16 unités et 78 = 6 dizaines + 18 unités."),
    ]),
    ("Do I need to exchange?", "هل أحتاج إلى التبديل؟", "Faut-il échanger ?", "52", [
        F("5 − 3 ✓      8 − 5 ✓      9 − 3 ✓"),
        F("3 − 7 ✗      4 − 7 ✗      7 − 9 ✗"),
        T("First look at the ones. If the top ones are enough (5 − 3), subtract directly. If not (3 − 7), exchange one ten first. We never subtract the smaller digit from the bigger one by reversing the order.",
          "ننظر أولًا إلى الآحاد. إذا كانت آحاد العدد العلوي كافية (5 − 3) نطرح مباشرة. وإن لم تكف (3 − 7) نبدّل عشرة أولًا. ولا نطرح العدد الأصغر من الأكبر بقلب الترتيب أبدًا.",
          "On regarde d'abord les unités. Si celles du haut suffisent (5 − 3), on soustrait directement. Sinon (3 − 7), on échange d'abord une dizaine. On n'inverse jamais l'ordre pour soustraire."),
    ]),
    ("The written method", "الطريقة المكتوبة", "La méthode écrite", "53", [
        sub(63, 38),
        T("63 − 38. Ones: 3 is less than 8, so exchange: 63 = 5 tens + 13 ones. 13 − 8 = 5. Tens: 5 − 3 = 2. The answer is 25. Check: 25 + 38 = 63.",
          "63 − 38. الآحاد: 3 أقل من 8 فنبدّل: 63 = 5 عشرات + 13 واحدًا. 13 − 8 = 5. العشرات: 5 − 3 = 2. الجواب 25. نتحقق: 25 + 38 = 63.",
          "63 − 38. Unités : 3 < 8, on échange : 63 = 5 dizaines + 13 unités. 13 − 8 = 5. Dizaines : 5 − 3 = 2. Réponse : 25. Vérification : 25 + 38 = 63."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("If the ones above are not enough, one ten becomes ten ones. The value does not change. Subtract the ones, then the tens, and check with addition.",
          "إذا لم تكف الآحاد في الأعلى تصبح عشرة واحدة عشرة آحاد. لا تتغير القيمة. نطرح الآحاد ثم العشرات ونتحقق بالجمع.",
          "Si les unités du haut ne suffisent pas, une dizaine devient dix unités. La valeur ne change pas. On soustrait les unités puis les dizaines, et on vérifie par l'addition."),
        F("NEED MORE ONES? → EXCHANGE ONE TEN → SUBTRACT → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "52", st("Exchange one ten into ones: 43, 56, 78, 62.", "بدّل عشرة واحدة بآحاد: 43، 56، 78، 62.", "Échange une dizaine contre des unités : 43, 56, 78, 62."), [
        F("43 → 3 tens and 13 ones      56 → 4 tens and 16 ones"),
        F("78 → 6 tens and 18 ones      62 → 5 tens and 12 ones"),
    ]),
    EX("2", "52", st("Put ✓ if the subtraction is possible directly: 3−7, 5−3, 6−4, 8−5, 4−7, 7−9, 9−3, 6−7, 2−8.", "ضع ✓ إذا كان الطرح ممكنًا مباشرة: 3−7، 5−3، 6−4، 8−5، 4−7، 7−9، 9−3، 6−7، 2−8.", "Mets ✓ si la soustraction est possible directement : 3−7, 5−3, 6−4, 8−5, 4−7, 7−9, 9−3, 6−7, 2−8."), [
        F("no  ✓  ✓  ✓  no  no  ✓  no  no"),
    ]),
    EX("3", "53", st("Subtract from 11 (8, 9, 2, 3, 4, 5, 6, 7) and from 15 (9, 6, 7, 8).", "اطرح من 11 (8 و9 و2 و3 و4 و5 و6 و7) ومن 15 (9 و6 و7 و8).", "Soustrais de 11 (8, 9, 2, 3, 4, 5, 6, 7) et de 15 (9, 6, 7, 8)."), [
        F("3   2   9   8   7   6   5   4"),
        F("6   9   8   7"),
    ]),
    EX("4", "53", st("Calculate: 12−7, 15−8, 14−6, 16−9, 11−8, 13−5.", "احسب: 12−7، 15−8، 14−6، 16−9، 11−8، 13−5.", "Calcule : 12−7, 15−8, 14−6, 16−9, 11−8, 13−5."), [
        F("5   7   8   7   3   8"),
    ]),
    EX("5", "53", st("Vertical form: 63−38, 71−49, 85−47.", "عموديًا: 63−38، 71−49، 85−47.", "Posées : 63−38, 71−49, 85−47."), [
        sub(63, 38), sub(71, 49), sub(85, 47),
        F("25      22      38"),
    ]),
    EX("6", "53", st("Calculate: 54−29, 61−37, 75−48, 86−59, 64−47.", "احسب: 54−29، 61−37، 75−48، 86−59، 64−47.", "Calcule : 54−29, 61−37, 75−48, 86−59, 64−47."), [
        F("25   24   27   27   17"),
    ]),
    EX("7", "53", st("Vertical form and calculate: 47−29, 32−19, 51−28, 82−49, 74−37, 93−68, 85−56, 41−23, 72−54, 65−28.", "عموديًا واحسب: 47−29، 32−19، 51−28، 82−49، 74−37، 93−68، 85−56، 41−23، 72−54، 65−28.", "Pose et calcule : 47−29, 32−19, 51−28, 82−49, 74−37, 93−68, 85−56, 41−23, 72−54, 65−28."), [
        F("18   13   23   33   37"),
        F("25   29   18   18   37"),
    ]),
    EX("8", "53", st("Which balls have the same difference: 76−59, 86−18, 61−44, 34−17, 83−25, 58−19?", "أيّ الكرات لها الفرق نفسه: 76−59، 86−18، 61−44، 34−17، 83−25، 58−19؟", "Quelles balles ont la même différence : 76−59, 86−18, 61−44, 34−17, 83−25, 58−19 ?"), [
        F("17   68   17   17   58   39"),
        T("76 − 59, 61 − 44 and 34 − 17 all equal 17.", "76 − 59 و61 − 44 و34 − 17 كلها تساوي 17.", "76 − 59, 61 − 44 et 34 − 17 valent tous 17."),
    ]),
    EX("9", "53", st("Riddle: a number between 70 and 80; if 6 is subtracted, the ones digit becomes 8.", "لغز: عدد بين 70 و80؛ إذا طرحنا منه 6 صار رقم آحاده 8.", "Devinette : un nombre entre 70 et 80 ; si on retire 6, le chiffre des unités devient 8."),  [
        F("74 − 6 = 68"),
        T("The answer is 74.", "الجواب 74.", "La réponse est 74."),
    ]),
    EX("10", "", st("Guided practice: 52 − 27, then check.", "تدريب موجَّه: 52 − 27 ثم التحقق.", "Entraînement : 52 − 27, puis vérification."), [
        sub(52, 27),
        T("52 = 4 tens + 12 ones. 12 − 7 = 5 and 4 − 2 = 2. The answer is 25. Check: 25 + 27 = 52.", "52 = 4 عشرات + 12 واحدًا. 12 − 7 = 5 و4 − 2 = 2. الجواب 25. نتحقق: 25 + 27 = 52.", "52 = 4 dizaines + 12 unités. 12 − 7 = 5 et 4 − 2 = 2. Réponse : 25. Vérification : 25 + 27 = 52."),
    ]),
    EX("11", "", st("Transfer: why does 70 − 26 need an exchange?", "تحدٍّ: لماذا يحتاج 70 − 26 إلى تبديل؟", "Défi : pourquoi 70 − 26 demande-t-il un échange ?"), [
        F("70 = 6 tens + 10 ones      70 − 26 = 44"),
        T("0 ones cannot remove 6 ones, so one ten becomes 10 ones.", "صفر آحاد لا يكفي لأخذ 6 آحاد فتصبح عشرة 10 آحاد.", "0 unité ne permet pas de retirer 6 unités : une dizaine devient 10 unités."),
    ]),
    EX("12", "", st("Error detective: 71 − 49 = 32; 54 = 5 tens + 14 ones.", "المحقق: 71 − 49 = 32؛ 54 = 5 عشرات + 14 واحدًا.", "Détective : 71 − 49 = 32 ; 54 = 5 dizaines + 14 unités."), [
        F("71 − 49 = 22      54 = 4 tens + 14 ones"),
        T("When a ten is exchanged, the tens go down by one: 5 tens becomes 4 tens.", "عند تبديل عشرة تنقص العشرات واحدة: 5 عشرات تصبح 4.", "Quand on échange une dizaine, les dizaines baissent de un : 5 devient 4."),
    ]),
    EX("13", "", st("Final check: 43 and 78 exchanged; 63−38; 71−49; 85−47; 54−29; 64−47; same-difference balls; riddle; why does exchange keep the value?", "تقييم أخير: تبديل 43 و78؛ 63−38؛ 71−49؛ 85−47؛ 54−29؛ 64−47؛ الكرات؛ اللغز؛ ولماذا يحفظ التبديل القيمة؟", "Évaluation : échange de 43 et 78 ; 63−38 ; 71−49 ; 85−47 ; 54−29 ; 64−47 ; balles ; devinette ; pourquoi l'échange garde la valeur ?"), [
        F("3 tens 13 ones; 6 tens 18 ones; 25; 22; 38; 25; 17; 74"),
        T("Because one ten equals ten ones.", "لأن العشرة الواحدة تساوي عشرة آحاد.", "Parce qu'une dizaine égale dix unités."),
    ]),
]
