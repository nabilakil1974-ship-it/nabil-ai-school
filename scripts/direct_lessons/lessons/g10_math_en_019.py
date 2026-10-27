"""Grade 10 Mathematics — Functions."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G10-MATH-EN-019"
GRADE = 10
SUBJECT = "math"
TITLES = {"en": "Functions", "ar": "الدوال", "fr": "Fonctions"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "f(x) = 2x + 3. f(4) = ?", "opts": ["11", "9", "14", "8"], "a": 0,
     "why": {"9": _w("2 × 4 = 8, then + 3.", "2 × 4 = 8 ثم + 3.", "8 + 3."),
             "14": _w("Do not add 4 + 3 + 7.", "لا نجمع هكذا.", "2 × 4 + 3."),
             "8": _w("Do not forget +3.", "لا تنسَ +3.", "+3.")}, "ok": "f(4) = 11"},
    {"q": "f(x) = x². f(−3) = ?", "opts": ["9", "−9", "6", "−6"], "a": 0,
     "why": {"−9": _w("(−3)² = 9: brackets matter.", "(−3)² = 9: الأقواس مهمة.", "(−3)² = 9."),
             "6": _w("Square, do not double.", "نربّع لا نضاعف.", "Carré."),
             "−6": _w("Square, do not double.", "نربّع لا نضاعف.", "Carré.")}, "ok": "9"},
    {"q": "f(x) = 3x − 2 and f(x) = 13. x = ?", "opts": ["5", "11", "35", "3"], "a": 0,
     "why": {"11": _w("3x = 15, then divide by 3.", "3x = 15 ثم نقسم على 3.", "3x = 15."),
             "35": _w("Solve 3x − 2 = 13.", "نحلّ 3x − 2 = 13.", "3x − 2 = 13."),
             "3": _w("3x = 15 gives 5.", "3x = 15 تعطي 5.", "x = 5.")}, "ok": "x = 5"},
]

THEORY = [
    ("A rule, not only a formula", "قاعدة لا صيغة فقط", "Une règle", "193", [
        T("Hello! A function is not just a formula. It is a rule that gives each admissible input exactly one output. We can see it as a formula, a table or a graph; these are different representations of the same idea.",
          "مرحبًا! الدالة ليست صيغة فقط، هي قاعدة تربط كل مدخل مسموح به بمخرج واحد. يمكن أن نراها صيغة أو جدولًا أو رسمًا، وهذه تمثيلات مختلفة للفكرة نفسها.",
          "Chaque entrée admissible a une seule sortie."),
    ]),
    ("Input → output", "مدخل ← مخرج", "Entrée → sortie", "193", [
        T("Take f(x) = 2x + 3. When we ask for f(4), we are not looking for a new x. We give the function the input 4 and compute the output: f(4) = 2×4 + 3 = 11.",
          "لتكن f(x) = 2x + 3. عندما نسأل عن f(4) لا نبحث عن x جديد، بل نعطي الدالة المدخل 4 ونحسب المخرج: f(4) = 2×4 + 3 = 11.",
          "f(4) = 11."),
        F("f(4) = 2 × 4 + 3 = 11"),
    ]),
    ("Domain first", "المجال أولًا", "Le domaine d'abord", "194", [
        T("Before substituting, ask: is the input admissible? If the rule has a denominator or another condition, we never use a forbidden value. The domain is part of the definition, not decoration.",
          "قبل التعويض نسأل: هل المدخل مسموح؟ إذا احتوت القاعدة على مقام أو شرط آخر فلا نستعمل قيمة ممنوعة. المجال جزء من تعريف الدالة لا زينة.",
          "Domaine = partie de la définition."),
    ]),
    ("Image and preimage", "الصورة والسابقة", "Image et antécédent", "194", [
        T("f(4) = 11 means 11 is the image of 4. If we ask for the preimage of 11, we reverse the question: which input gives output 11? Solve 2x + 3 = 11 and find x = 4, inside the domain.",
          "f(4) = 11 تعني أن 11 هي صورة 4. وإذا سألنا عن سابقة 11 نعكس السؤال: أي مدخل يعطي المخرج 11؟ نحلّ 2x + 3 = 11 فنجد x = 4 ضمن المجال.",
          "Antécédent de 11 : 4."),
        F("2x + 3 = 11  →  x = 4"),
    ]),
    ("Tables and graphs", "الجداول والرسوم", "Tableaux et graphiques", "195", [
        T("In a table we do not mix the roles of row and column: identify the input, then read its linked output. On a graph we read coordinates with the scale, not from the rough shape of the curve.",
          "في الجدول لا نخلط دور السطر والعمود: نحدد المدخل ثم نقرأ المخرج المرتبط به. وفي الرسم نقرأ الإحداثيات مع السلّم لا من شكل المنحنى تقريبًا.",
          "Lis avec l'échelle."),
    ]),
    ("Error detective", "المحقق", "Détective", "195", [
        T("A student says f(x) = x² gives f(−3) = −9. Brackets matter: f(−3) = (−3)² = 9. The error came from not replacing x by the whole value.",
          "قال طالب إن f(x) = x² تعطي f(−3) = −9. الأقواس مهمة: f(−3) = (−3)² = 9. جاء الخطأ من عدم استبدال x بالقيمة كاملة.",
          "(−3)² = 9."),
        F("f(−3) = (−3)² = 9"),
    ]),
    ("Challenge", "تحدٍّ", "Défi", "196", [
        T("For f(x) = 3x − 2, find x if f(x) = 13. This time the output is given: 3x − 2 = 13, 3x = 15, x = 5. Check: f(5) = 13.",
          "لتكن f(x) = 3x − 2، أوجد x إذا كانت f(x) = 13. هذه المرة المخرج معطى: 3x − 2 = 13 إذن 3x = 15 وx = 5. نتحقق: f(5) = 13.",
          "x = 5."),
        F("3x − 2 = 13  →  x = 5"),
        F("f(5) = 3 × 5 − 2 = 13"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Function → each admissible input has one output. Domain → check before evaluating. f(a) → image. Preimage → input producing a stated output.",
          "دالة ← لكل مدخل مسموح مخرج واحد. المجال ← نتحقق قبل الحساب. f(a) ← الصورة. السابقة ← مدخل ينتج مخرجًا معلومًا.",
          "Image, antécédent, domaine."),
    ]),
]

EXERCISES = [
    EX("1", "", st("f(x) = 2x + 3: find f(4).", "f(x) = 2x + 3: أوجد f(4).", "Calcule f(4)."), [F("2 × 4 + 3 = 11")]),
    EX("2", "", st("Find the preimage of 11.", "أوجد سابقة 11.", "Antécédent de 11."), [F("2x + 3 = 11      x = 4")]),
    EX("3", "", st("Error detective: f(−3) = −9 for x².", "المحقق: f(−3) = −9 للدالة x².", "Détective."), [F("(−3)² = 9")]),
    EX("4", "", st("f(x) = 3x − 2: solve f(x) = 13.", "f(x) = 3x − 2: حلّ f(x) = 13.", "Résous f(x) = 13."), [F("3x = 15      x = 5")]),
]
