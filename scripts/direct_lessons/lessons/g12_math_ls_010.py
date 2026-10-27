"""Grade 12 (LS) Mathematics — Power functions."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G12-MATH-LS-010"
GRADE = 12
SUBJECT = "math"
TITLES = {"en": "Power functions", "ar": "الدوال القوى", "fr": "Fonctions puissances"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "Domain of x^(−3/2) ?", "opts": ["(0, +∞)", "[0, +∞)", "ℝ", "ℝ \\ {0}"], "a": 0,
     "why": {"[0, +∞)": _w("Negative exponent also excludes 0.", "الأس السالب يستبعد 0 أيضًا.", "Exclut 0."),
             "ℝ": _w("A square root is involved.", "هناك جذر تربيعي.", "Racine."),
             "ℝ \\ {0}": _w("Even root also requires x ≥ 0.", "الجذر الزوجي يشترط x ≥ 0.", "x ≥ 0 aussi.")}, "ok": "x > 0"},
    {"q": "d/dx (x^a) for x > 0 = ?", "opts": ["a·x^(a−1)", "x^(a−1)", "a·x^a", "(a−1)x^a"], "a": 0,
     "why": {"x^(a−1)": _w("Do not forget the factor a.", "لا تنسَ العامل a.", "Facteur a."),
             "a·x^a": _w("Lower the exponent by 1.", "ننقص الأس 1.", "Exposant − 1."),
             "(a−1)x^a": _w("Mixed up the rule.", "خلطت القاعدة.", "Règle.")}, "ok": "a x^(a−1)"},
    {"q": "On (0, +∞), x^a with a < 0 is …", "opts": ["decreasing", "increasing", "constant", "not defined"], "a": 0,
     "why": {"increasing": _w("The derivative a x^(a−1) has the sign of a.", "المشتقة لها إشارة a.", "Signe de a."),
             "constant": _w("Only a = 0.", "فقط a = 0.", "a = 0."),
             "not defined": _w("Defined for x > 0.", "معرّفة عند x > 0.", "Définie.")}, "ok": "decreasing"},
]

THEORY = [
    ("One symbol, many behaviours", "رمز واحد وسلوكات كثيرة", "Un symbole, plusieurs comportements", "", [
        T("Hello! x², x³, x^(1/2), x^(−1), x^(3/2): are all of these power functions? Yes, they have the form xᵃ. But the value of a changes the domain and the behaviour radically. x² is defined for every real x, while √x is real only for x ≥ 0. So before differentiating or drawing, read the exponent and decide its type.",
          "مرحبًا! x² وx³ وx^(1/2) وx^(−1) وx^(3/2): هل كلها دوال قوى؟ نعم فهي من الشكل xᵃ. لكن قيمة a تغيّر المجال والسلوك جذريًا. x² معرّفة لكل x حقيقي أما √x فحقيقية فقط عند x ≥ 0. لذلك قبل الاشتقاق أو الرسم نقرأ الأس ونحدد نوعه.",
          "L'exposant gouverne."),
    ]),
    ("Integer exponents and parity", "الأسس الصحيحة والزوجية", "Exposants entiers et parité", "", [
        T("For integer n: (−x)ⁿ = (−1)ⁿxⁿ. Even n gives an even function (symmetric about the y-axis); odd n gives an odd function (symmetric about the origin). So x⁷ is odd. Example f(x) = x⁴: domain ℝ, even, f′(x) = 4x³, negative for x < 0 and positive for x > 0, so decreasing on (−∞, 0], increasing on [0, +∞), limits +∞ at ±∞, minimum f(0) = 0.",
          "لعدد صحيح n: (−x)ⁿ = (−1)ⁿxⁿ. n زوجي يعطي دالة زوجية (متناظرة حول محور التراتيب) وn فردي يعطي دالة فردية (متناظرة حول المبدأ). إذن x⁷ فردية. مثال f(x) = x⁴: المجال ℝ زوجية وf′(x) = 4x³ سالبة عندما x < 0 وموجبة عندما x > 0 فهي متناقصة على (−∞, 0] ومتزايدة على [0, +∞) والنهايتان +∞ عند ±∞ والصغرى f(0) = 0.",
          "Paire ou impaire."),
        F("f(x) = x⁴      f′(x) = 4x³      min f(0) = 0"),
    ]),
    ("Negative integer powers", "القوى الصحيحة السالبة", "Puissances entières négatives", "", [
        T("x^(−n) = 1/xⁿ with x ≠ 0, so the domain of x^(−4) is ℝ \\ {0}. Example g(x) = x^(−2) = 1/x²: even, g′(x) = −2/x³, positive for x < 0 and negative for x > 0. Limits: +∞ at 0 from both sides (a positive denominator tending to zero) and 0⁺ at ±∞. So x = 0 is a vertical asymptote and y = 0 a horizontal asymptote.",
          "x^(−n) = 1/xⁿ مع x ≠ 0 فمجال x^(−4) هو ℝ \\ {0}. مثال g(x) = x^(−2) = 1/x²: زوجية وg′(x) = −2/x³ موجبة عندما x < 0 وسالبة عندما x > 0. النهايات: +∞ عند 0 من الجهتين (مقام موجب يؤول إلى الصفر) و0⁺ عند ±∞. فالمستقيم x = 0 مقارب رأسي وy = 0 مقارب أفقي.",
          "Asymptotes x = 0, y = 0."),
        F("g′(x) = −2 / x³"),
    ]),
    ("Rational exponents", "الأسس الكسرية", "Exposants rationnels", "", [
        T("For x^(p/q) in reduced form with q > 0: if q is even we need x ≥ 0 (and x > 0 when the exponent is negative); if q is odd, negative x may be allowed. Domains: x^(3/2) is [0, +∞); x^(−3/2) is (0, +∞). Also (−8)^(2/3) is possible since the denominator 3 is odd: the cube root is −2 and its square is 4.",
          "في x^(p/q) بصيغة مختزلة وq > 0: إذا كان q زوجيًا نشترط x ≥ 0 (وx > 0 عندما يكون الأس سالبًا)، وإذا كان q فرديًا فقد يُسمح بـ x السالب. المجالات: x^(3/2) هو [0, +∞)؛ وx^(−3/2) هو (0, +∞). كذلك (−8)^(2/3) ممكن لأن المقام 3 فردي: الجذر التكعيبي −2 ومربعه 4.",
          "Parité du dénominateur."),
        T("Example h(x) = x^(3/2): domain x ≥ 0; for x > 0, h′(x) = (3/2)x^(1/2) > 0 so h is increasing; h″(x) = 3/(4√x) > 0 so it is concave up; h(0) = 0. Domain controls where derivative formulas may be used.",
          "مثال h(x) = x^(3/2): المجال x ≥ 0؛ عندما x > 0 فإن h′(x) = (3/2)x^(1/2) > 0 فهي متزايدة؛ وh″(x) = 3/(4√x) > 0 فهي مقعّرة نحو الأعلى؛ وh(0) = 0. المجال يتحكم في أين تُستعمل صيغ المشتقة.",
          "h′ > 0, h″ > 0."),
        F("h′(x) = (3/2)√x      h″(x) = 3 / (4√x)"),
    ]),
    ("Real exponent on x > 0", "أس حقيقي على x > 0", "Exposant réel", "", [
        T("For x > 0, xᵃ = e^(a ln x). Differentiate: e^(a ln x) · a/x = a xᵃ/x = a x^(a−1). So d/dx(xᵃ) = a x^(a−1); for example the derivative of x^π is πx^(π−1). This representation is for x > 0 only.",
          "من أجل x > 0: xᵃ = e^(a ln x). نشتق: e^(a ln x) · a/x = a xᵃ/x = a x^(a−1). إذن d/dx(xᵃ) = a x^(a−1)؛ مثلًا مشتقة x^π هي πx^(π−1). هذا التمثيل لـ x > 0 فقط.",
          "xᵃ = e^(a ln x)."),
        F("(xᵃ)′ = a · x^(a−1),   x > 0"),
    ]),
    ("Monotonicity, concavity, limits", "الرتابة والتقعر والنهايات", "Monotonie, concavité, limites", "", [
        T("For x > 0, x^(a−1) > 0 so the sign of f′ is the sign of a: a > 0 increasing, a < 0 decreasing, a = 0 constant. Also f″ = a(a−1)x^(a−2): concave down when 0 < a < 1, concave up when a > 1 or a < 0. Limits: for a > 0, x → 0⁺ gives 0 and x → +∞ gives +∞; for a < 0 they reverse, because xᵃ = 1/x^(−a). All these curves pass through (1, 1).",
          "من أجل x > 0 فإن x^(a−1) > 0 فإشارة f′ هي إشارة a: a > 0 متزايدة وa < 0 متناقصة وa = 0 ثابتة. وكذلك f″ = a(a−1)x^(a−2): مقعّرة نحو الأسفل عندما 0 < a < 1 ونحو الأعلى عندما a > 1 أو a < 0. النهايات: لـ a > 0 يعطي x → 0⁺ القيمة 0 وx → +∞ القيمة +∞؛ ولـ a < 0 ينعكس ذلك لأن xᵃ = 1/x^(−a). وكل هذه المنحنيات تمر بالنقطة (1, 1).",
          "Signe de a et de a(a−1)."),
        F("f″(x) = a(a − 1) x^(a−2)"),
    ]),
    ("Comparing powers", "مقارنة القوى", "Comparer des puissances", "", [
        T("If a > b then xᵃ/xᵇ = x^(a−b) → +∞ as x → +∞, so the larger positive exponent dominates for large x. Near 0⁺ the order reverses: x⁵ is smaller than x² there. A larger exponent does not always give a larger value: for 0 < x < 1 a larger positive exponent gives a smaller value.",
          "إذا كان a > b فإن xᵃ/xᵇ = x^(a−b) → +∞ عندما x → +∞ فيغلب الأس الموجب الأكبر عند x الكبيرة. وقرب 0⁺ ينعكس الترتيب: x⁵ أصغر من x² هناك. الأس الأكبر لا يعطي دائمًا قيمة أكبر: عندما 0 < x < 1 يعطي الأس الموجب الأكبر قيمة أصغر.",
          "x⁵ domine à l'infini."),
    ]),
    ("Complete study of x^(−3/2)", "دراسة كاملة لـ x^(−3/2)", "Étude complète", "", [
        T("Domain: x > 0 (negative exponent and even root), so D = (0, +∞). f′(x) = −(3/2)x^(−5/2) < 0, so f is strictly decreasing. Limits: +∞ at 0⁺ and 0 at +∞. Asymptotes: x = 0 vertical and y = 0 horizontal. Check: f(1) = 1 and f(4) = 1/8, consistent with a decreasing function.",
          "المجال: x > 0 (أس سالب وجذر زوجي) فيكون D = (0, +∞). f′(x) = −(3/2)x^(−5/2) < 0 فالدالة متناقصة تمامًا. النهايات: +∞ عند 0⁺ و0 عند +∞. المقاربات: x = 0 رأسي وy = 0 أفقي. تحقق: f(1) = 1 وf(4) = 1/8 وهذا يوافق دالة متناقصة.",
          "D = ]0, +∞[."),
        F("f′(x) = −(3/2) x^(−5/2) < 0"),
    ]),
    ("Error detectives", "المحققون", "Détectives", "", [
        T("1) “x^(1/2) has domain ℝ”: wrong, the even root needs x ≥ 0. 2) Differentiating x^(−2) at x = 0: undefined there. 3) Using x^a = e^(a ln x) for negative x. 4) Thinking (−8)^(2/3) is impossible: the denominator 3 is odd. 5) Saying a larger exponent always gives a larger value.",
          "1) «x^(1/2) مجالها ℝ»: خطأ، الجذر الزوجي يشترط x ≥ 0. 2) اشتقاق x^(−2) عند x = 0: غير معرّفة هناك. 3) استعمال x^a = e^(a ln x) من أجل x سالب. 4) ظن أن (−8)^(2/3) مستحيل: المقام 3 فردي. 5) القول إن الأس الأكبر يعطي دائمًا قيمة أكبر.",
          "Cinq erreurs types."),
    ]),
    ("Memory line", "جملة الذاكرة", "Fil conducteur", "", [
        T("Do not memorise the shape of xᵃ. Read a first, then ask: where does the function exist? does it rise or fall? how does it bend? what does it do near zero and infinity? The graph becomes a result of understanding.",
          "لا تحفظ شكل xᵃ. اقرأ a أولًا ثم اسأل: أين الدالة موجودة؟ هل تصعد أم تنزل؟ كيف تنحني؟ ماذا تفعل قرب الصفر واللانهاية؟ عندها يصبح الرسم نتيجة للفهم.",
          "Exposant, domaine, dérivée, signe, limites, forme."),
        F("EXPONENT → DOMAIN → DERIVATIVE → SIGN → LIMITS → SHAPE"),
    ]),
]

EXERCISES = [
    EX("1", "", st("Domains of x^(5/2), x^(−4), x^(2/3), x^(−2/3).", "مجالات x^(5/2) وx^(−4) وx^(2/3) وx^(−2/3).", "Domaines."), [F("[0,+∞)      ℝ\\{0}      ℝ      ℝ\\{0}")]),
    EX("2", "", st("Differentiate x^(7/3), x^(−5/2), x^√3 on x > 0.", "اشتق x^(7/3) وx^(−5/2) وx^√3 عندما x > 0.", "Dérive."), [F("(7/3)x^(4/3)      −(5/2)x^(−7/2)      √3·x^(√3−1)")]),
    EX("3", "", st("Concavity for a < 0, 0 < a < 1, a > 1.", "التقعر عندما a < 0 و0 < a < 1 وa > 1.", "Concavité."), [F("up      down      up")]),
    EX("4", "", st("Analyse f(x) = x^(−1/2) completely.", "ادرس f(x) = x^(−1/2) كاملًا.", "Étude complète."), [F("D = (0, +∞)      f′ = −(1/2)x^(−3/2) < 0      x = 0, y = 0")]),
    EX("5", "", st("Compare x⁴ and x^(3/2) near 0⁺ and at +∞.", "قارن x⁴ وx^(3/2) قرب 0⁺ وعند +∞.", "Compare."), [T("At +∞, x⁴ dominates; near 0⁺, x⁴ is smaller.", "عند +∞ يغلب x⁴ وقرب 0⁺ هو الأصغر.", "x⁴ domine en +∞.")]),
]
