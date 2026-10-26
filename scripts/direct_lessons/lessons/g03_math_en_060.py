"""Grade 3 Mathematics — Division Technique (3) (from the teacher plan)."""
from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.lessons.g03_math_en_053 import share

LESSON_ID = "G03-MATH-EN-060"
GRADE = 3
SUBJECT = "math"
TITLES = {"en": "Division Technique (3)", "ar": "تقنية القسمة (3)", "fr": "Technique de la division (3)"}

THEORY = [
    ("Plan the whole division", "نخطط للقسمة كاملة", "Planifier toute la division", "126", [
        T("Hello, champion! Before dividing, plan: look at the tens, choose the quotient digit with a multiplication fact, subtract, bring down the rest, divide the ones, check. Example 96 ÷ 3: 9 tens ÷ 3 = 3 tens; 6 ones ÷ 3 = 2 ones. The quotient is 32.",
          "مرحبًا يا بطل! قبل القسمة نخطّط: ننظر إلى العشرات ونختار رقم الناتج بحقيقة ضرب ونطرح وننزل الباقي ونقسم الآحاد ونتحقق. مثال 96 ÷ 3: 9 عشرات ÷ 3 = 3 عشرات و6 آحاد ÷ 3 = آحادان. الناتج 32.",
          "96 ÷ 3 : 9 dizaines ÷ 3 = 3, 6 unités ÷ 3 = 2. Quotient 32."),
        share(9, 6, 3),
    ]),
    ("Regrouping inside the division", "إعادة التجميع داخل القسمة", "Regrouper", "126", [
        T("92 ÷ 4: 9 tens ÷ 4 = 2 tens, 1 ten left. 1 ten + 2 ones = 12 ones. 12 ÷ 4 = 3. The quotient is 23. Check: 23 × 4 = 92.",
          "92 ÷ 4: 9 عشرات ÷ 4 = عشرتان وتبقى عشرة. عشرة + 2 آحاد = 12 واحدًا. 12 ÷ 4 = 3. الناتج 23. نتحقق: 23 × 4 = 92.",
          "92 ÷ 4 = 23 ; 23 × 4 = 92."),
        F("92 ÷ 4 = 23"),
    ]),
    ("Check a division", "نتحقق من القسمة", "Vérifier une division", "127", [
        T("To check a completed division, multiply the quotient by the divisor. You must get the dividend back.",
          "للتحقق من قسمة منتهية نضرب الناتج في المقسوم عليه فنعود إلى المقسوم.",
          "Quotient × diviseur = dividende."),
        F("QUOTIENT × DIVISOR = DIVIDEND"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Plan, divide by place, record each step, complete, verify.", "نخطّط ونقسم حسب المنزلة ونسجّل كل خطوة ونكمل ونتحقق.", "Planifier, diviser, noter, vérifier."),
    ]),
]

EXERCISES = [
    EX("1", "126", st("Calculate 96 ÷ 3 and 92 ÷ 4.", "احسب 96 ÷ 3 و92 ÷ 4.", "Calcule 96 ÷ 3 et 92 ÷ 4."), [F("32      23"), F("32 × 3 = 96      23 × 4 = 92")]),
    EX("2", "127", st("Calculate 84 ÷ 7, 78 ÷ 6, 95 ÷ 5.", "احسب 84 ÷ 7 و78 ÷ 6 و95 ÷ 5.", "Calcule 84 ÷ 7, 78 ÷ 6, 95 ÷ 5."), [F("12      13      19"), F("12 × 7 = 84      13 × 6 = 78      19 × 5 = 95")]),
    EX("3", "127", st("Explain how to check a completed division.", "اشرح كيف نتحقق من قسمة.", "Comment vérifier une division ?"), [T("Multiply the quotient by the divisor to get the dividend.", "نضرب الناتج في المقسوم عليه فنحصل على المقسوم.", "Quotient × diviseur = dividende.")]),
]
