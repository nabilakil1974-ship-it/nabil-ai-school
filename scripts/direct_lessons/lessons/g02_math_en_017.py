"""Grade 2 Mathematics — Subtraction (1): without exchange."""
from scripts.direct_lessons.common import T, F, EX, st, tens
from scripts.direct_lessons.lessons.g02_math_en_008 import vert

LESSON_ID = "G02-MATH-EN-017"
GRADE = 2
SUBJECT = "math"
TITLES = {"en": "Subtraction (1)", "ar": "الطرح (1)", "fr": "Soustraction (1)"}


def sub(a, b):
    return vert([a, b], a - b, op="−")


THEORY = [
    ("Subtraction removes part of a quantity", "الطرح يزيل جزءًا من الكمية", "Soustraire, c'est retirer une partie", "40", [
        tens(4, 7, tag="A", eq=True),
        T("Hello, champion! Today: subtraction. whole − removed part = what remains. Start with 47: 4 tens and 7 ones. We take away 15: 1 ten and 5 ones. Ones: 7 − 5 = 2. Tens: 4 − 1 = 3. So 47 − 15 = 32.",
          "مرحبًا يا بطل! اليوم الطرح. الكل − الجزء المأخوذ = الباقي. نبدأ بـ47: 4 عشرات و7 آحاد. نأخذ 15: عشرة و5 آحاد. الآحاد: 7 − 5 = 2. العشرات: 4 − 1 = 3. إذن 47 − 15 = 32.",
          "Aujourd'hui : la soustraction. tout − partie retirée = reste. On part de 47 : 4 dizaines et 7 unités. On retire 15 : 1 dizaine et 5 unités. Unités : 7 − 5 = 2. Dizaines : 4 − 1 = 3. Donc 47 − 15 = 32."),
        tens(3, 2, tag="B", eq=True),
        sub(47, 15),
    ]),
    ("Ones from ones, tens from tens", "آحاد من آحاد وعشرات من عشرات", "Unités avec unités, dizaines avec dizaines", "40", [
        sub(79, 28),
        T("We align ones under ones and tens under tens. 9 − 8 = 1 one and 7 − 2 = 5 tens. So 79 − 28 = 51. In this lesson every subtraction can be done directly, with no need to take a ten apart.",
          "نحاذي الآحاد تحت الآحاد والعشرات تحت العشرات. 9 − 8 = 1 و7 − 2 = 5 عشرات. إذن 79 − 28 = 51. في هذا الدرس يمكن إجراء كل طرح مباشرة دون الحاجة إلى فكّ عشرة.",
          "On aligne unités sous unités et dizaines sous dizaines. 9 − 8 = 1 et 7 − 2 = 5 dizaines. Donc 79 − 28 = 51. Dans cette leçon, chaque soustraction se fait directement, sans casser une dizaine."),
    ]),
    ("Check with addition", "نتحقق بالجمع", "Vérifier avec l'addition", "40", [
        F("47 − 15 = 32      32 + 15 = 47"),
        T("To check a subtraction, add the remainder and the removed part. If we get the starting whole, the answer is right: 32 + 15 = 47.",
          "للتحقق من الطرح نجمع الباقي مع الجزء المأخوذ. إذا حصلنا على الكل الأول فالجواب صحيح: 32 + 15 = 47.",
          "Pour vérifier, on additionne le reste et la partie retirée. Si on retrouve le tout de départ, c'est juste : 32 + 15 = 47."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Align, subtract the ones, subtract the tens, and check with addition.",
          "نحاذي ثم نطرح الآحاد ثم نطرح العشرات ثم نتحقق بالجمع.",
          "On aligne, on soustrait les unités, puis les dizaines, et on vérifie par l'addition."),
        F("WHOLE → REMOVE → REMAINDER → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "40", st("Read the models and complete: 57 − 14, 48 − 16, 79 − 28, 46 − 23, 82 − 31, 69 − 7.", "اقرأ النماذج وأكمل: 57 − 14، 48 − 16، 79 − 28، 46 − 23، 82 − 31، 69 − 7.", "Lis les modèles et complète : 57 − 14, 48 − 16, 79 − 28, 46 − 23, 82 − 31, 69 − 7."), [
        F("43   32   51   23   51   62"),
        T("Crossed pieces are removed; the uncrossed pieces are the remainder.", "القطع المشطوبة أُزيلت والقطع غير المشطوبة هي الباقي.", "Les pièces barrées sont retirées ; les autres forment le reste."),
    ]),
    EX("2", "40", st("Calculate from the models: 43 − 12, 88 − 66, 74 − 42.", "احسب من النماذج: 43 − 12، 88 − 66، 74 − 42.", "Calcule d'après les modèles : 43 − 12, 88 − 66, 74 − 42."), [
        F("31      22      32"),
    ]),
    EX("3", "40", st("Calculate: 68 − 8, 57 − 7, 73 − 13, 42 − 2, 86 − 6, 35 − 5, 76 − 16, 64 − 4, 79 − 9.", "احسب: 68 − 8، 57 − 7، 73 − 13، 42 − 2، 86 − 6، 35 − 5، 76 − 16، 64 − 4، 79 − 9.", "Calcule : 68 − 8, 57 − 7, 73 − 13, 42 − 2, 86 − 6, 35 − 5, 76 − 16, 64 − 4, 79 − 9."), [
        F("60   50   60   40   80   30   60   60   70"),
    ]),
    EX("4", "41", st("Vertical form: 76 − 31, 84 − 53, 68 − 26, 57 − 24, 85 − 44, 49 − 39.", "عموديًا: 76 − 31، 84 − 53، 68 − 26، 57 − 24، 85 − 44، 49 − 39.", "Posées : 76 − 31, 84 − 53, 68 − 26, 57 − 24, 85 − 44, 49 − 39."), [
        sub(76, 31), sub(49, 39),
        F("45   31   42   33   41   10"),
        T("49 − 39: 9 − 9 = 0 ones and 4 − 3 = 1 ten. The answer is 10.", "49 − 39: 9 − 9 = 0 آحاد و4 − 3 = عشرة. الجواب 10.", "49 − 39 : 9 − 9 = 0 unité et 4 − 3 = 1 dizaine. Réponse : 10."),
    ]),
    EX("5", "41", st("Calculate: 59 − 36, 84 − 42, 76 − 51, 69 − 43, 86 − 43.", "احسب: 59 − 36، 84 − 42، 76 − 51، 69 − 43، 86 − 43.", "Calcule : 59 − 36, 84 − 42, 76 − 51, 69 − 43, 86 − 43."), [
        F("23   42   25   26   43"),
    ]),
    EX("6", "41", st("Vertical form: 87 − 33, 46 − 36, 55 − 23, 68 − 14, 59 − 23.", "عموديًا: 87 − 33، 46 − 36، 55 − 23، 68 − 14، 59 − 23.", "Posées : 87 − 33, 46 − 36, 55 − 23, 68 − 14, 59 − 23."), [
        F("54   10   32   54   36"),
    ]),
    EX("7", "41", st("Replace the dots: 75 − 43, 88 − 52, 69 − 43, 87 − 25, 74 − 21.", "استبدل النقاط: 75 − 43، 88 − 52، 69 − 43، 87 − 25، 74 − 21.", "Remplace les points : 75 − 43, 88 − 52, 69 − 43, 87 − 25, 74 − 21."), [
        F("32   36   26   62   53"),
        T("Solve the ones first, then the tens. No borrowing is needed here.", "نحلّ الآحاد أولًا ثم العشرات. لا حاجة إلى الاستلاف هنا.", "On résout d'abord les unités, puis les dizaines. Pas d'emprunt ici."),
    ]),
    EX("8", "41", st("Balloons: which have the same difference? 46−21, 28−3, 56−6, 30−5, 64−52.", "البالونات: أيها له الفرق نفسه؟ 46−21، 28−3، 56−6، 30−5، 64−52.", "Ballons : lesquels ont la même différence ? 46−21, 28−3, 56−6, 30−5, 64−52."), [
        F("25   25   50   25   12"),
        T("46 − 21, 28 − 3 and 30 − 5 all equal 25.", "46 − 21 و28 − 3 و30 − 5 كلها تساوي 25.", "46 − 21, 28 − 3 et 30 − 5 valent tous 25."),
    ]),
    EX("9", "", st("Guided practice: 67 − 24 and 95 − 52, each checked with addition.", "تدريب موجَّه: 67 − 24 و95 − 52 مع التحقق بالجمع.", "Entraînement : 67 − 24 et 95 − 52, vérifiés par l'addition."), [
        F("67 − 24 = 43   check 43 + 24 = 67"),
        F("95 − 52 = 43   check 43 + 52 = 95"),
    ]),
    EX("10", "", st("Transfer: 75 − ? = 32.", "تحدٍّ: 75 − ؟ = 32.", "Défi : 75 − ? = 32."), [
        F("5 − 3 = 2      7 − 4 = 3      75 − 43 = 32"),
        T("Ones: 5 − ? = 2 so 3. Tens: 7 − ? = 3 so 4. The missing number is 43.", "الآحاد: 5 − ؟ = 2 إذن 3. العشرات: 7 − ؟ = 3 إذن 4. العدد الناقص 43.", "Unités : 5 − ? = 2, donc 3. Dizaines : 7 − ? = 3, donc 4. Le nombre manquant est 43."),
    ]),
    EX("11", "", st("Error detective: 68 − 26 = 52; 46 − 36 = 20.", "المحقق: 68 − 26 = 52؛ 46 − 36 = 20.", "Détective : 68 − 26 = 52 ; 46 − 36 = 20."), [
        F("68 − 26 = 42      46 − 36 = 10"),
        T("8 − 6 = 2 and 6 − 2 = 4 gives 42. 6 − 6 = 0 and 4 − 3 = 1 gives 10.", "8 − 6 = 2 و6 − 2 = 4 فيكون 42. و6 − 6 = 0 و4 − 3 = 1 فيكون 10.", "8 − 6 = 2 et 6 − 2 = 4 donne 42. 6 − 6 = 0 et 4 − 3 = 1 donne 10."),
    ]),
    EX("12", "", st("Final check: 57−14; 48−16; 79−28; 43−12; 76−31; 85−44; 75−43; 87−25; same difference; check 68−26.", "تقييم أخير: 57−14؛ 48−16؛ 79−28؛ 43−12؛ 76−31؛ 85−44؛ 75−43؛ 87−25؛ الفرق نفسه؛ تحقّق من 68−26.", "Évaluation : 57−14 ; 48−16 ; 79−28 ; 43−12 ; 76−31 ; 85−44 ; 75−43 ; 87−25 ; même différence ; vérifie 68−26."), [
        F("43   32   51   31   45   41   32   62"),
        F("46−21, 28−3, 30−5      42 + 26 = 68"),
    ]),
]
