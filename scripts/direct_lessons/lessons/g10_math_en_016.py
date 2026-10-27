"""Grade 10 Mathematics — Linear equations."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G10-MATH-EN-016"
GRADE = 10
SUBJECT = "math"
TITLES = {"en": "Linear equations", "ar": "المعادلات من الدرجة الأولى", "fr": "Équations du premier degré"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "3x + 5 = 20 → 3x = ?", "opts": ["15", "25", "17", "5"], "a": 0,
     "why": {"25": _w("To remove +5 we subtract 5 from both sides.", "لإزالة +5 نطرح 5 من الطرفين.", "On retire 5 des deux côtés."),
             "17": _w("20 − 3 is not the step.", "ليست الخطوة.", "Pas cette étape."),
             "5": _w("That is the number we removed.", "هذا ما أزلناه.", "C'est ce qu'on a retiré.")}, "ok": "3x = 15, x = 5"},
    {"q": "2x + 7 = 15 → 2x = ?", "opts": ["8", "22", "−8", "9"], "a": 0,
     "why": {"22": _w("Do not add 7: subtract 7 from both sides.", "لا نجمع 7: نطرح 7 من الطرفين.", "Soustrais 7."),
             "−8": _w("15 − 7 = 8.", "15 − 7 = 8.", "15 − 7 = 8."),
             "9": _w("15 − 7 = 8.", "15 − 7 = 8.", "15 − 7 = 8.")}, "ok": "2x = 8, x = 4"},
    {"q": "x/3 + 2 = 6 → x = ?", "opts": ["12", "4", "24", "8"], "a": 0,
     "why": {"4": _w("x/3 = 4; multiply both sides by 3.", "x/3 = 4؛ نضرب الطرفين في 3.", "Multiplie par 3."),
             "24": _w("x/3 = 4, so x = 12.", "x/3 = 4 إذن x = 12.", "x = 12."),
             "8": _w("x/3 = 4, so x = 12.", "x/3 = 4 إذن x = 12.", "x = 12.")}, "ok": "x = 12"},
]

THEORY = [
    ("An equation is a balance", "المعادلة ميزان", "Une équation est une balance", "167", [
        T("Hello! An equation is not a game of \"move it and change the sign\". It is a balance. Our goal is to keep both sides equal while we simplify until the unknown stands alone. Adding or subtracting the same number on both sides keeps the equality; so does multiplying or dividing both sides by an allowed nonzero number.",
          "مرحبًا! المعادلة ليست لعبة «انقل وغيّر الإشارة» بل هي ميزان. هدفنا أن نبقي الطرفين متساويين ونحن نبسّطهما حتى يظهر المجهول وحده. إضافة العدد نفسه إلى الطرفين أو طرحه منهما تُبقي المساواة، وكذلك ضرب الطرفين أو قسمتهما على عدد غير معدوم مسموح.",
          "Une équation est une balance : mêmes opérations des deux côtés."),
    ]),
    ("A first example", "مثال أول", "Premier exemple", "167", [
        T("3x + 5 = 20. Subtract 5 from both sides: 3x = 15. Divide both sides by 3: x = 5. We do not stop: substitute into the original equation: 3 × 5 + 5 = 20, true.",
          "3x + 5 = 20. نطرح 5 من الطرفين: 3x = 15. نقسم الطرفين على 3: x = 5. ولا نتوقف: نعوّض في المعادلة الأصلية: 3 × 5 + 5 = 20 صحيح.",
          "3x + 5 = 20 ⇒ x = 5."),
        F("3x + 5 = 20  →  3x = 15  →  x = 5"),
        F("3 × 5 + 5 = 20"),
    ]),
    ("With a fraction", "مع كسر", "Avec une fraction", "168", [
        T("x/3 + 2 = 6. Subtract 2: x/3 = 4. Multiply both sides by 3: x = 12. Check: 12/3 + 2 = 6.",
          "x/3 + 2 = 6. نطرح 2: x/3 = 4. نضرب الطرفين في 3: x = 12. نتحقق: 12/3 + 2 = 6.",
          "x/3 + 2 = 6 ⇒ x = 12."),
        F("12 / 3 + 2 = 6"),
    ]),
    ("Unknown on both sides", "المجهول في الطرفين", "Inconnue des deux côtés", "168", [
        T("4(2x − 1) = 3x + 11. Distribute: 8x − 4 = 3x + 11. Subtract 3x from both sides: 5x − 4 = 11. Add 4: 5x = 15. Divide by 5: x = 3. Check: 4(6 − 1) = 20 and 9 + 11 = 20.",
          "4(2x − 1) = 3x + 11. ننشر: 8x − 4 = 3x + 11. نطرح 3x من الطرفين: 5x − 4 = 11. نضيف 4: 5x = 15. نقسم على 5: x = 3. نتحقق: 4(6 − 1) = 20 و9 + 11 = 20.",
          "x = 3."),
        F("8x − 4 = 3x + 11      5x = 15      x = 3"),
        F("4 × 5 = 20      9 + 11 = 20"),
    ]),
    ("Special cases", "حالات خاصة", "Cas particuliers", "168", [
        T("If x disappears during simplification, we do not invent a value. We may reach a statement that is always true (every number is a solution) or a contradiction (no solution). We then describe the solution set accordingly.",
          "إذا اختفى x أثناء التبسيط فلا نخترع قيمة. قد نصل إلى عبارة صحيحة دائمًا (كل عدد حل) أو إلى تناقض (لا حل). عندها نصف مجموعة الحلول وفق ذلك.",
          "Identité ou contradiction."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Every transformation preserves equivalence. Isolate the unknown. Always substitute into the original equation.", "كل تحويل يحفظ التكافؤ. نعزل المجهول. ونعوّض دائمًا في المعادلة الأصلية.", "Équivalence, isoler, vérifier."),
        F("EQUATION = BALANCE"),
    ]),
]

EXERCISES = [
    EX("1", "", st("Solve 3x + 5 = 20 and check.", "حلّ 3x + 5 = 20 وتحقق.", "Résous 3x + 5 = 20."), [F("3x = 15      x = 5      3 × 5 + 5 = 20")]),
    EX("2", "", st("Solve x/3 + 2 = 6.", "حلّ x/3 + 2 = 6.", "Résous x/3 + 2 = 6."), [F("x/3 = 4      x = 12")]),
    EX("3", "", st("Error detective: 2x + 7 = 15 solved as 2x = 15 + 7.", "المحقق: حُلّت 2x + 7 = 15 هكذا 2x = 15 + 7.", "Détective : 2x = 15 + 7."), [T("Subtract 7 from both sides: 2x = 8, then x = 4. The check exposes the error at once.", "نطرح 7 من الطرفين: 2x = 8 ثم x = 4. والتحقق يكشف الخطأ فورًا.", "On retire 7 : 2x = 8."), F("2x = 8      x = 4      2 × 4 + 7 = 15")]),
    EX("4", "", st("Solve 4(2x − 1) = 3x + 11.", "حلّ 4(2x − 1) = 3x + 11.", "Résous 4(2x − 1) = 3x + 11."), [F("8x − 4 = 3x + 11      5x = 15      x = 3")]),
    EX("5", "", st("Why is \"move it and change the sign\" risky?", "لماذا تكون عبارة «انقل وغيّر الإشارة» خطرة؟", "Pourquoi « change de côté, change de signe » est risqué ?"), [T("Because the real reason is an operation done to both sides; without it, mistakes appear.", "لأن السبب الحقيقي عملية نجريها على الطرفين، وبدونها تظهر الأخطاء.", "La vraie raison est l'opération des deux côtés.")]),
]
