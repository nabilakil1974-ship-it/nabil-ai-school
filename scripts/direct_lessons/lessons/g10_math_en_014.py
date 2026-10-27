"""Grade 10 Mathematics — Scalar product (Dot product)."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G10-MATH-EN-014"
GRADE = 10
SUBJECT = "math"
TITLES = {"en": "Scalar product (Dot product)", "ar": "الجداء السلمي", "fr": "Produit scalaire"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "|u| = 3, |v| = 4, θ = 60°: u·v = 3 × 4 × ½ = ?", "opts": ["6", "12", "24", "7"], "a": 0,
     "why": {"12": _w("Do not forget cos 60° = ½.", "لا تنسَ أن cos 60° = ½.", "N'oublie pas cos 60° = ½."),
             "24": _w("Multiply by cos 60° = ½, not 2.", "نضرب في cos 60° = ½ لا 2.", "× ½."),
             "7": _w("It is a product, not 3 + 4.", "هو جداء لا 3 + 4.", "Produit, pas somme.")}, "ok": "u·v = 6"},
    {"q": "The result of u·v is a …", "opts": ["number (scalar)", "vector", "point", "line"], "a": 0,
     "why": {"vector": _w("A scalar product gives a number.", "الجداء السلمي يعطي عددًا.", "Un nombre."),
             "point": _w("It is a number.", "هو عدد.", "Un nombre."),
             "line": _w("It is a number.", "هو عدد.", "Un nombre.")}, "ok": "scalar"},
    {"q": "Nonzero u ⊥ v. Then u·v = ?", "opts": ["0", "1", "|u||v|", "−1"], "a": 0,
     "why": {"1": _w("cos 90° = 0.", "cos 90° = 0.", "cos 90° = 0."),
             "|u||v|": _w("That is for θ = 0°.", "هذا عند θ = 0°.", "Pour θ = 0°."),
             "−1": _w("cos 90° = 0.", "cos 90° = 0.", "cos 90° = 0.")}, "ok": "0"},
]

THEORY = [
    ("Two vectors, one number", "متجهان وعدد واحد", "Deux vecteurs, un nombre", "147", [
        T("Hello! The dot product takes two vectors and gives a number. For nonzero u and v: u·v = |u| |v| cos θ, where θ is the angle between them. The angle is the heart of the idea: it measures how much one vector points toward the other.",
          "مرحبًا! الجداء السلمي يأخذ متجهين ويعطي عددًا. لمتجهين غير معدومين u وv: u·v = |u| |v| cos θ حيث θ الزاوية بينهما. الزاوية هي قلب الفكرة: تقيس كم يتجه أحد المتجهين نحو الآخر.",
          "u·v = |u||v|cos θ : un nombre."),
        F("u · v = |u| |v| cos θ"),
    ]),
    ("The sign carries meaning", "للإشارة معنى", "Le signe a un sens", "147", [
        T("If θ is acute, cos θ > 0 and the product is positive. If θ = 90°, cos θ = 0 and the product is zero. If θ is obtuse, cos θ < 0 and the product is negative. So the sign gives geometric information about the angle.",
          "إذا كانت θ حادة فإن cos θ > 0 والجداء موجب. وإذا كانت θ = 90° فإن cos θ = 0 والجداء معدوم. وإذا كانت θ منفرجة فإن cos θ < 0 والجداء سالب. إذن الإشارة تعطي معلومة هندسية عن الزاوية.",
          "Aigu : positif ; droit : nul ; obtus : négatif."),
        F("θ acute → u·v > 0      θ = 90° → u·v = 0      θ obtuse → u·v < 0"),
    ]),
    ("Worked example", "مثال محلول", "Exemple", "148", [
        T("|u| = 3, |v| = 4, θ = 60°. First list the data, then substitute: u·v = 3 × 4 × cos 60° = 12 × ½ = 6. The result is a scalar, so no arrow is placed over 6.",
          "|u| = 3 وv = 4 وθ = 60°. نكتب المعطيات أولًا ثم نعوّض: u·v = 3 × 4 × cos 60° = 12 × ½ = 6. النتيجة عدد فلا نضع سهمًا فوق 6.",
          "3 × 4 × ½ = 6."),
        F("3 × 4 × 1/2 = 6"),
    ]),
    ("Perpendicular vectors", "المتجهان المتعامدان", "Vecteurs perpendiculaires", "148", [
        T("Two nonzero perpendicular vectors have θ = 90°, so u·v = 0. The converse is used under the right conditions: a zero dot product of nonzero vectors shows they are perpendicular. We translate the zero into geometry.",
          "إذا كان المتجهان غير معدومين ومتعامدين فإن θ = 90° وu·v = 0. ويُستعمل العكس بالشروط المناسبة: جداء سلمي معدوم لمتجهين غير معدومين يعني تعامدهما. نترجم الصفر إلى هندسة.",
          "u·v = 0 ⇒ u ⊥ v (vecteurs non nuls)."),
    ]),
    ("Reading the angle from the product", "قراءة الزاوية من الجداء", "Lire l'angle", "148", [
        T("|u| = 5, |v| = 2 and u·v = −5. Then cos θ = −5 / 10 = −½. The cosine is negative, so θ is obtuse (θ = 120°).",
          "|u| = 5 و|v| = 2 وu·v = −5. إذن cos θ = −5 / 10 = −½. جيب التمام سالب فالزاوية منفرجة (θ = 120°).",
          "cos θ = −1/2 : angle obtus."),
        F("cos θ = −5 / 10 = −1/2"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Identify the vectors, the angle and the type of the output (a number) before calculating.", "نحدّد المتجهين والزاوية ونوع الناتج (عدد) قبل الحساب.", "Vecteurs, angle, type du résultat."),
        F("u·v = |u||v|cos θ"),
    ]),
]

EXERCISES = [
    EX("1", "", st("|u| = 3, |v| = 4, θ = 60°: find u·v.", "|u| = 3 وv = 4 وθ = 60°: أوجد u·v.", "Calcule u·v."), [F("3 × 4 × 1/2 = 6")]),
    EX("2", "", st("Predict the sign of u·v for an acute angle, a right angle and an obtuse angle.", "تنبّأ بإشارة u·v لزاوية حادة وقائمة ومنفرجة.", "Signe de u·v : aigu, droit, obtus."), [F("+      0      −")]),
    EX("3", "", st("Error detective: a student writes u·v as a vector.", "المحقق: كتب طالب u·v على أنه متجه.", "Détective : u·v écrit comme un vecteur."), [T("The name scalar product says the result is a number.", "اسم الجداء السلمي يذكّرنا أن الناتج عدد.", "Le résultat est un nombre.")]),
    EX("4", "", st("|u| = 5, |v| = 2, u·v = −5: what does the sign say about θ?", "|u| = 5 و|v| = 2 وu·v = −5: ماذا تقول الإشارة عن θ؟", "Que dit le signe de θ ?"), [F("cos θ = −5 / 10 = −1/2"), T("Negative cosine: θ is obtuse.", "جيب التمام سالب: θ منفرجة.", "Angle obtus.")]),
]
