"""Grade 10 Mathematics — Linear inequalities in one unknown."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G10-MATH-EN-017"
GRADE = 10
SUBJECT = "math"
TITLES = {"en": "Linear inequalities in one unknown", "ar": "المتراجحات من الدرجة الأولى بمجهول واحد", "fr": "Inéquations du premier degré"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "3x − 5 < 10 → x < ?", "opts": ["5", "15", "−5", "3"], "a": 0,
     "why": {"15": _w("3x < 15, then divide by 3.", "3x < 15 ثم نقسم على 3.", "Divise par 3."),
             "−5": _w("Add 5 to both sides first.", "نضيف 5 للطرفين أولًا.", "Ajoute 5."),
             "3": _w("Divide 15 by 3.", "نقسم 15 على 3.", "15 ÷ 3.")}, "ok": "x < 5"},
    {"q": "−2x + 1 ≥ 7 → x ? −3", "opts": ["≤", "≥", "<", ">"], "a": 0,
     "why": {"≥": _w("We divided by −2: the sign reverses.", "قسمنا على −2: ينعكس الرمز.", "Division par −2 : on inverse."),
             "<": _w("The boundary −3 is included (7 ≥ 7).", "الحد −3 مشمول (7 ≥ 7).", "−3 inclus."),
             ">": _w("Reverse, and keep the equality.", "ينعكس الرمز ويبقى التساوي.", "On inverse et garde =.")}, "ok": "x ≤ −3"},
    {"q": "−4x < 8 → x ? −2", "opts": [">", "<", "≤", "="], "a": 0,
     "why": {"<": _w("Dividing by −4 reverses <. Test x = 0.", "القسمة على −4 تعكس <. جرّب x = 0.", "Inverse <. Teste x = 0."),
             "≤": _w("The inequality is strict.", "المتراجحة صارمة.", "Stricte."),
             "=": _w("It is a range, not one value.", "مجال لا قيمة واحدة.", "Un intervalle.")}, "ok": "x > −2"},
]

THEORY = [
    ("A range of values", "مجموعة قيم", "Un ensemble de valeurs", "175", [
        T("Hello! An inequality usually does not look for one number; it looks for a whole set of values. So every step must keep the order, not just the equality. Adding or subtracting the same quantity keeps the direction. Multiplying or dividing by a positive number keeps it too.",
          "مرحبًا! المتراجحة لا تبحث عادةً عن عدد واحد بل عن مجموعة قيم. لذلك يجب أن تحافظ كل خطوة على الترتيب لا على المساواة فقط. إضافة الكمية نفسها أو طرحها تحافظ على الاتجاه، وكذلك الضرب أو القسمة على عدد موجب.",
          "On garde l'ordre à chaque étape."),
        T("But multiplying or dividing by a NEGATIVE number reverses the order. Imagine a reflection on the number line.",
          "أما الضرب أو القسمة على عدد سالب فتعكس الترتيب. تخيّل انعكاسًا على محور الأعداد.",
          "Par un négatif : on inverse."),
        F("× or ÷ by a negative  ⇒  reverse the sign"),
    ]),
    ("Worked example", "مثال محلول", "Exemple", "175", [
        T("3x − 5 < 10. Add 5: 3x < 15. Divide by +3, so we do not flip: x < 5. Test x = 0: −5 < 10 true. Test x = 6: 13 < 10 false.",
          "3x − 5 < 10. نضيف 5 للطرفين: 3x < 15. نقسم على +3 فلا نقلب الرمز: x < 5. نختبر x = 0: −5 < 10 صحيح. ونختبر x = 6: 13 < 10 خطأ.",
          "x < 5."),
        F("3x − 5 < 10  →  3x < 15  →  x < 5"),
    ]),
    ("Negative coefficient", "معامل سالب", "Coefficient négatif", "176", [
        T("−2x + 1 ≥ 7. Subtract 1: −2x ≥ 6. Now we divide by −2, and only here we flip ≥ into ≤. So x ≤ −3. Check the boundary: at −3 we get 7 ≥ 7, true.",
          "−2x + 1 ≥ 7. نطرح 1: −2x ≥ 6. الآن نقسم على −2 وهنا فقط نقلب ≥ إلى ≤. إذن x ≤ −3. نختبر الحد: عند −3 نحصل على 7 ≥ 7 صحيح.",
          "x ≤ −3."),
        F("−2x ≥ 6  →  x ≤ −3"),
    ]),
    ("Error detective", "المحقق", "Détective", "176", [
        T("A student solves −4x < 8 as x < −2. The error: dividing by −4 without reversing. The correct answer is x > −2. A simple value, x = 0, satisfies the original and shows at once that x < −2 cannot be the solution.",
          "حلّ طالب −4x < 8 فكتب x < −2. الخطأ: القسمة على −4 دون عكس الرمز. الصحيح x > −2. قيمة بسيطة مثل x = 0 تحقق الأصل وتكشف فورًا أن x < −2 لا يمكن أن يكون الحل.",
          "Correct : x > −2."),
        F("−4x < 8  →  x > −2"),
    ]),
    ("Represent the set", "تمثيل المجموعة", "Représenter l'ensemble", "177", [
        T("After the algebra, translate the result to a number line or an interval. A strict sign (<, >) gives an open endpoint; ≤ or ≥ gives a closed endpoint.",
          "بعد الجبر نترجم النتيجة إلى محور أعداد أو مجال. الرمز الصارم (<، >) يعطي طرفًا مفتوحًا، و≤ أو ≥ يعطي طرفًا مغلقًا.",
          "Crochet ouvert/fermé selon le signe."),
        F("x ≤ −3   ⇔   x ∈ ]−∞ ; −3]"),
    ]),
    ("Challenge", "تحدٍّ", "Défi", "177", [
        T("5 − 3x ≤ 14. Subtract 5: −3x ≤ 9. Divide by −3 and reverse: x ≥ −3. Check at −3 and with one value outside the set.",
          "5 − 3x ≤ 14. نطرح 5: −3x ≤ 9. نقسم على −3 ونعكس الرمز: x ≥ −3. نتحقق عند −3 وعند قيمة من خارج المجموعة.",
          "x ≥ −3."),
        F("−3x ≤ 9  →  x ≥ −3"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Inequality → solution set. Negative → reverse. Boundary → check inclusion. Verify one value inside and one outside.",
          "المتراجحة ← مجموعة حلول. السالب ← نعكس. الحد ← نتحقق من الشمول. نجرّب قيمة من الداخل وأخرى من الخارج.",
          "Négatif → inverser."),
    ]),
]

EXERCISES = [
    EX("1", "", st("Solve 3x − 5 < 10.", "حلّ 3x − 5 < 10.", "Résous 3x − 5 < 10."), [F("3x < 15      x < 5")]),
    EX("2", "", st("Solve −2x + 1 ≥ 7.", "حلّ −2x + 1 ≥ 7.", "Résous −2x + 1 ≥ 7."), [F("−2x ≥ 6      x ≤ −3")]),
    EX("3", "", st("Error detective: −4x < 8 ⇒ x < −2.", "المحقق: −4x < 8 ⇒ x < −2.", "Détective."), [F("x > −2"), T("Test x = 0.", "نجرّب x = 0.", "Teste x = 0.")]),
    EX("4", "", st("Solve 5 − 3x ≤ 14.", "حلّ 5 − 3x ≤ 14.", "Résous 5 − 3x ≤ 14."), [F("−3x ≤ 9      x ≥ −3")]),
]
