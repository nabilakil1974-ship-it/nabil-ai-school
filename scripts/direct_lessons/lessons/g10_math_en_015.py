"""Grade 10 Mathematics — Analytic form of the scalar product."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G10-MATH-EN-015"
GRADE = 10
SUBJECT = "math"
TITLES = {"en": "Analytic form of the scalar product", "ar": "الصيغة التحليلية للجداء السلمي", "fr": "Expression analytique du produit scalaire"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "u = (2, 3), v = (4, −1): u·v = 2×4 + 3×(−1) = ?", "opts": ["5", "7", "11", "−5"], "a": 0,
     "why": {"7": _w("3 × (−1) = −3, not −1.", "3 × (−1) = −3 لا −1.", "3 × (−1) = −3."),
             "11": _w("Watch the sign: 8 − 3.", "انتبه للإشارة: 8 − 3.", "8 − 3."),
             "−5": _w("8 − 3 is positive.", "8 − 3 موجبة.", "8 − 3 > 0.")}, "ok": "8 − 3 = 5"},
    {"q": "u = (2, 1), v = (1, −2): are they perpendicular?", "opts": ["Yes: u·v = 0", "No: u·v = 4", "No: u·v = 5", "Cannot tell"], "a": 0,
     "why": {"No: u·v = 4": _w("2×1 + 1×(−2) = 0.", "2×1 + 1×(−2) = 0.", "= 0."),
             "No: u·v = 5": _w("2×1 + 1×(−2) = 0.", "2×1 + 1×(−2) = 0.", "= 0."),
             "Cannot tell": _w("The test is algebraic.", "الاختبار جبري.", "Test algébrique.")}, "ok": "2 − 2 = 0"},
    {"q": "u = (k, 2) ⊥ v = (3, −6): k = ?", "opts": ["4", "−4", "2", "12"], "a": 0,
     "why": {"−4": _w("3k − 12 = 0 gives k = +4.", "3k − 12 = 0 تعطي k = +4.", "k = +4."),
             "2": _w("Solve 3k − 12 = 0.", "نحلّ 3k − 12 = 0.", "3k − 12 = 0."),
             "12": _w("3k = 12, so k = 4.", "3k = 12 إذن k = 4.", "k = 4.")}, "ok": "k = 4"},
]

THEORY = [
    ("From geometry to coordinates", "من الهندسة إلى الإحداثيات", "De la géométrie aux coordonnées", "157", [
        T("Hello! Last lesson the dot product came from lengths and the angle. Now we compute it straight from coordinates. In an orthonormal reference, if u = (x₁, y₁) and v = (x₂, y₂) then u·v = x₁x₂ + y₁y₂. It is the same quantity written in the language of analytic geometry.",
          "مرحبًا! في الدرس السابق جاء الجداء السلمي من الأطوال والزاوية. الآن نحسبه مباشرة من الإحداثيات. في معلم متعامد ومتجانس إذا كان u = (x₁, y₁) وv = (x₂, y₂) فإن u·v = x₁x₂ + y₁y₂. هي الكمية نفسها مكتوبة بلغة الهندسة التحليلية.",
          "u·v = x₁x₂ + y₁y₂."),
        F("u·v = x₁·x₂ + y₁·y₂"),
    ]),
    ("Worked example", "مثال محلول", "Exemple", "157", [
        T("u = (2, 3), v = (4, −1). Pair first with first and second with second, multiply, then add: 2×4 + 3×(−1) = 8 − 3 = 5. The result is a scalar.",
          "u = (2, 3) وv = (4, −1). نقرن الأولى بالأولى والثانية بالثانية ونضرب ثم نجمع: 2×4 + 3×(−1) = 8 − 3 = 5. والناتج عدد.",
          "2×4 + 3×(−1) = 5."),
        F("2 × 4 + 3 × (−1) = 8 − 3 = 5"),
    ]),
    ("A perpendicularity test", "اختبار التعامد", "Test de perpendicularité", "158", [
        T("u = (2, 1), v = (1, −2): u·v = 2×1 + 1×(−2) = 0. Instead of \"the drawing looks right-angled\", we have an algebraic test: for nonzero vectors, a zero dot product proves they are perpendicular.",
          "u = (2, 1) وv = (1, −2): u·v = 2×1 + 1×(−2) = 0. بدل «الرسم يبدو قائمًا» صار عندنا اختبار جبري: لمتجهين غير معدومين الجداء السلمي المعدوم يثبت تعامدهما.",
          "u·v = 0 : u ⊥ v."),
        F("2 × 1 + 1 × (−2) = 0"),
    ]),
    ("Find an unknown component", "إيجاد مركّبة مجهولة", "Trouver une composante", "158", [
        T("Find k so that u = (k, 2) is perpendicular to v = (3, −6). Perpendicular means u·v = 0: 3k + 2×(−6) = 0, so 3k − 12 = 0 and k = 4. Check: (4, 2)·(3, −6) = 12 − 12 = 0.",
          "أوجد k ليتعامد u = (k, 2) مع v = (3, −6). التعامد يعني u·v = 0: 3k + 2×(−6) = 0 إذن 3k − 12 = 0 وk = 4. نتحقق: (4, 2)·(3, −6) = 12 − 12 = 0.",
          "3k − 12 = 0, k = 4."),
        F("3k − 12 = 0  ⇒  k = 4"),
        F("4 × 3 + 2 × (−6) = 0"),
    ]),
    ("Bridge back to geometry", "الجسر إلى الهندسة", "Retour à la géométrie", "158", [
        T("The coordinate result also equals |u||v|cos θ, so we can recover the angle or check perpendicularity. Two languages, one quantity.",
          "ناتج الإحداثيات يساوي أيضًا |u||v|cos θ فنستخرج الزاوية أو نتحقق من التعامد. لغتان لكمية واحدة.",
          "Deux écritures, une seule quantité."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Pair the components, multiply, add. The result is a scalar. Zero means perpendicular (nonzero vectors).", "نقرن المركّبات ونضرب ونجمع. الناتج عدد. والصفر يعني التعامد (متجهان غير معدومين).", "Apparier, multiplier, additionner."),
        F("(x₁, y₁)·(x₂, y₂) = x₁x₂ + y₁y₂"),
    ]),
]

EXERCISES = [
    EX("1", "", st("Calculate (2, 3)·(4, −1).", "احسب (2, 3)·(4, −1).", "Calcule (2,3)·(4,−1)."), [F("2 × 4 + 3 × (−1) = 5")]),
    EX("2", "", st("Are u = (2, 1) and v = (1, −2) perpendicular?", "هل u = (2, 1) وv = (1, −2) متعامدان؟", "u et v sont-ils perpendiculaires ?"), [F("2 × 1 + 1 × (−2) = 0  ⇒  yes")]),
    EX("3", "", st("Error detective: (2, 3)·(4, −1) = 8 − 1.", "المحقق: (2, 3)·(4, −1) = 8 − 1.", "Détective : 8 − 1."), [F("3 × (−1) = −3      8 − 3 = 5"), T("Check each pair of components before adding.", "نراجع كل زوج من المركّبات قبل الجمع.", "Vérifie chaque produit.")]),
    EX("4", "", st("Find k so that (k, 2) is perpendicular to (3, −6).", "أوجد k ليتعامد (k, 2) مع (3, −6).", "Trouve k pour (k,2) ⊥ (3,−6)."), [F("3k − 12 = 0      k = 4")]),
]
