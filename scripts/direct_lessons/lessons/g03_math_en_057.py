"""Grade 3 Mathematics — Division Technique (2) (from the teacher plan)."""
from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.lessons.g03_math_en_053 import share

LESSON_ID = "G03-MATH-EN-057"
GRADE = 3
SUBJECT = "math"
TITLES = {"en": "Division Technique (2)", "ar": "تقنية القسمة (2)", "fr": "Technique de la division (2)"}

THEORY = [
    ("When tens do not share exactly", "عندما لا تنقسم العشرات تمامًا", "Quand les dizaines ne se partagent pas", "120", [
        T("Hello, champion! 52 ÷ 4. Share 5 tens among 4 groups: 1 ten each and 1 ten left. Exchange the left ten for 10 ones: now 10 + 2 = 12 ones. 12 ÷ 4 = 3 ones each. Each group has 1 ten and 3 ones: 13. Check: 13 × 4 = 52.",
          "مرحبًا يا بطل! 52 ÷ 4. نوزّع 5 عشرات على 4 مجموعات: عشرة لكل مجموعة وتبقى عشرة. نبدّل العشرة الباقية بعشرة آحاد: صار عندنا 10 + 2 = 12 واحدًا. 12 ÷ 4 = 3 آحاد لكل مجموعة. لكل مجموعة عشرة و3 آحاد: 13. نتحقق: 13 × 4 = 52.",
          "52 ÷ 4 : 5 dizaines entre 4 : 1 chacune, reste 1 dizaine = 10 unités ; 12 unités ÷ 4 = 3. Quotient 13."),
        share(4, 8, 4),
        F("52 ÷ 4 = 13      13 × 4 = 52"),
    ]),
    ("Each step in order", "كل خطوة بترتيبها", "Chaque étape dans l'ordre", "120", [
        T("1) Look at the tens and choose the quotient digit with a multiplication fact. 2) Multiply and subtract to find what is left. 3) Bring the left tens down as ones. 4) Divide the ones. 5) Check by multiplying.",
          "1) ننظر إلى العشرات ونختار رقم الناتج بحقيقة ضرب. 2) نضرب ونطرح لنعرف الباقي. 3) ننزل الباقي إلى الآحاد. 4) نقسم الآحاد. 5) نتحقق بالضرب.",
          "Choisir par la table, multiplier, soustraire, descendre, diviser les unités, vérifier."),
        F("75 ÷ 5 = 15      7 tens ÷ 5 = 1, left 2 tens = 20 ones, 25 ÷ 5 = 5"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Read the place, choose the digit with multiplication, subtract, regroup the rest, continue, check.", "نقرأ المنزلة ونختار الرقم بالضرب ونطرح ونعيد تجميع الباقي ونتابع ونتحقق.", "Lire, choisir, soustraire, regrouper, vérifier."),
        F("PLACE → FACT → SUBTRACT → REGROUP → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "120", st("Calculate 52 ÷ 4 and check.", "احسب 52 ÷ 4 وتحقق.", "Calcule 52 ÷ 4 et vérifie."), [F("13      13 × 4 = 52")]),
    EX("2", "120", st("Calculate 75 ÷ 5.", "احسب 75 ÷ 5.", "Calcule 75 ÷ 5."), [F("15      15 × 5 = 75")]),
    EX("3", "121", st("Calculate 91 ÷ 7 and 84 ÷ 6.", "احسب 91 ÷ 7 و84 ÷ 6.", "Calcule 91 ÷ 7 et 84 ÷ 6."), [F("13      14"), F("13 × 7 = 91      14 × 6 = 84")]),
    EX("4", "121", st("Error detective: 52 ÷ 4 = 12 because 5 ÷ 4 = 1 and 2 ÷ 4 = 2.", "المحقق: 52 ÷ 4 = 12 لأن 5 ÷ 4 = 1 و2 ÷ 4 = 2.", "Détective : 52 ÷ 4 = 12."), [
        F("52 ÷ 4 = 13"), T("The left ten must be regrouped as 10 ones: 12 ÷ 4 = 3.", "يجب تجميع العشرة الباقية آحادًا: 12 ÷ 4 = 3.", "La dizaine restante devient 10 unités."),
    ]),
]
