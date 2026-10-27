"""Grade 12 (GS) Mathematics — Inverse trigonometric functions."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G12-MATH-GS-003"
GRADE = 12
SUBJECT = "math"
TITLES = {"en": "Inverse trigonometric functions", "ar": "الدوال المثلثية العكسية", "fr": "Fonctions trigonométriques réciproques"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "arccos(cos(5π/3)) = ?", "opts": ["π/3", "5π/3", "−π/3", "2π/3"], "a": 0,
     "why": {"5π/3": _w("arccos returns a value in [0, π].", "arccos تعطي قيمة في [0, π].", "Dans [0, π]."),
             "−π/3": _w("Negative is outside [0, π].", "السالب خارج [0, π].", "Hors de [0, π]."),
             "2π/3": _w("cos(2π/3) = −1/2, not 1/2.", "cos(2π/3) = −1/2.", "−1/2.")}, "ok": "π/3"},
    {"q": "sin(arccos(3/5)) = ?", "opts": ["4/5", "−4/5", "±4/5", "3/5"], "a": 0,
     "why": {"−4/5": _w("θ ∈ [0, π], so sin θ ≥ 0.", "θ ∈ [0, π] إذن sin θ ≥ 0.", "sin ≥ 0."),
             "±4/5": _w("The principal range decides the sign.", "المجال الأساسي يحسم الإشارة.", "Le signe est décidé."),
             "3/5": _w("That is cos θ.", "هذا cos θ.", "C'est cos.")}, "ok": "4/5"},
    {"q": "(arctan x)′ = ?", "opts": ["1/(1 + x²)", "1/√(1 − x²)", "−1/(1 + x²)", "1 + x²"], "a": 0,
     "why": {"1/√(1 − x²)": _w("That is arcsin.", "هذه arcsin.", "arcsin."),
             "−1/(1 + x²)": _w("arctan is increasing.", "arctan متزايدة.", "Croissante."),
             "1 + x²": _w("That is the denominator.", "هذا المقام.", "Dénominateur.")}, "ok": "1/(1 + x²)"},
]

THEORY = [
    ("Can sine have an inverse?", "هل للجيب دالة عكسية؟", "Le sinus a-t-il une réciproque ?", "42", [
        T("Hello! Look: sin(π/6) = 1/2 and sin(5π/6) = 1/2. Given the value 1/2, can we recover one unique angle on all of ℝ? No. The problem is not algebra, it is uniqueness. An inverse must send each output back to exactly one input, so we first restrict the function to an interval where it is one-to-one. The horizontal-line test detects the problem.",
          "مرحبًا! انظر: sin(π/6) = 1/2 وsin(5π/6) = 1/2. إذا أعطيتك القيمة 1/2 فهل نستعيد زاوية واحدة على ℝ كلها؟ لا. المشكلة ليست جبرية بل هي الوحدانية. الدالة العكسية يجب أن تعيد كل مخرج إلى مدخل واحد فقط، لذلك نقيّد الدالة أولًا على مجال تكون فيه متباينة. ويكشف المشكلة اختبار الخط الأفقي.",
          "Il faut restreindre."),
    ]),
    ("Choosing the principal branches", "اختيار الفروع الأساسية", "Branches principales", "42", [
        T("sin x is restricted to [−π/2, π/2]: strictly increasing from −1 to 1. cos x is restricted to [0, π]: strictly decreasing from 1 to −1. tan x is restricted to ]−π/2, π/2[: strictly increasing from −∞ to +∞. Inverse trig functions are not obtained by blindly writing “−1”; they exist because we first choose one-to-one branches. Note: sin⁻¹x is not 1/sin x.",
          "نقيّد sin x على [−π/2, π/2]: متزايدة تمامًا من −1 إلى 1. ونقيّد cos x على [0, π]: متناقصة تمامًا من 1 إلى −1. ونقيّد tan x على ]−π/2, π/2[: متزايدة تمامًا من −∞ إلى +∞. الدوال العكسية لا تأتي من كتابة «−1» بعمى، بل توجد لأننا اخترنا أولًا فروعًا متباينة. تنبيه: sin⁻¹x ليست 1/sin x.",
          "Trois restrictions."),
        F("sin: [−π/2, π/2]      cos: [0, π]      tan: ]−π/2, π/2["),
    ]),
    ("arcsin", "arcsin", "arcsin", "43", [
        T("Reflect the points of the sine branch across y = x: (π/2, 1) becomes (1, π/2). So y = arcsin x means sin y = x with y ∈ [−π/2, π/2]; domain [−1, 1], range [−π/2, π/2]. sin(arcsin x) = x for x ∈ [−1, 1], but arcsin(sin x) = x only when x ∈ [−π/2, π/2]: otherwise arcsin returns the equivalent principal angle.",
          "نعكس نقاط فرع الجيب حول y = x: النقطة (π/2, 1) تصبح (1, π/2). إذن y = arcsin x تعني sin y = x مع y ∈ [−π/2, π/2]؛ المجال [−1, 1] والمدى [−π/2, π/2]. وsin(arcsin x) = x لكل x ∈ [−1, 1] أما arcsin(sin x) = x فقط عندما x ∈ [−π/2, π/2]، وإلا تعيد arcsin الزاوية الأساسية المكافئة.",
          "Domaine [−1, 1]."),
        T("Derivative: let y = arcsin x, so x = sin y and 1 = cos y · y′. Since y ∈ [−π/2, π/2], cos y ≥ 0 and cos y = √(1 − x²). Therefore:",
          "المشتقة: لتكن y = arcsin x إذن x = sin y فيكون 1 = cos y · y′. وبما أن y ∈ [−π/2, π/2] فإن cos y ≥ 0 وcos y = √(1 − x²). إذن:",
          "Dérivée."),
        F("(arcsin x)′ = 1 / √(1 − x²),   −1 < x < 1"),
    ]),
    ("arccos", "arccos", "arccos", "44", [
        T("y = arccos x means cos y = x with y ∈ [0, π]; domain [−1, 1], range [0, π]. A decreasing one-to-one function has a decreasing inverse, so arccos is decreasing and its derivative is negative. cos(arccos x) = x on [−1, 1]; arccos(cos x) = x only on [0, π].",
          "y = arccos x تعني cos y = x مع y ∈ [0, π]؛ المجال [−1, 1] والمدى [0, π]. الدالة المتباينة المتناقصة عكسها متناقص، فـ arccos متناقصة ومشتقتها سالبة. cos(arccos x) = x على [−1, 1]؛ وarccos(cos x) = x فقط على [0, π].",
          "arccos décroissante."),
        F("(arccos x)′ = −1 / √(1 − x²),   −1 < x < 1"),
    ]),
    ("arctan", "arctan", "arctan", "45", [
        T("y = arctan x means tan y = x with y ∈ ]−π/2, π/2[. Domain ℝ, range ]−π/2, π/2[. Derivative: x = tan y gives 1 = sec²y · y′ and sec²y = 1 + x². As x → +∞, arctan x → π/2; as x → −∞, arctan x → −π/2, so y = ±π/2 are horizontal asymptotes.",
          "y = arctan x تعني tan y = x مع y ∈ ]−π/2, π/2[. المجال ℝ والمدى ]−π/2, π/2[. المشتقة: x = tan y تعطي 1 = sec²y · y′ وsec²y = 1 + x². وعندما x → +∞ فإن arctan x → π/2 وعندما x → −∞ فإن arctan x → −π/2 فالمستقيمان y = ±π/2 مقاربان أفقيان.",
          "Asymptotes y = ±π/2."),
        F("(arctan x)′ = 1 / (1 + x²)"),
    ]),
    ("Principal-value map", "خريطة القيم الأساسية", "Valeurs principales", "46", [
        T("Do not memorise isolated answers. Always ask: what angle inside the principal range gives this value? arcsin: 0 → 0, 1/2 → π/6, √2/2 → π/4, √3/2 → π/3, 1 → π/2. arccos: 1 → 0, √3/2 → π/6, √2/2 → π/4, 1/2 → π/3, 0 → π/2, −1 → π. arctan: 0 → 0, 1/√3 → π/6, 1 → π/4, √3 → π/3.",
          "لا نحفظ إجابات معزولة. نسأل دائمًا: أي زاوية داخل المجال الأساسي تعطي هذه القيمة؟ arcsin: 0 → 0 و1/2 → π/6 و√2/2 → π/4 و√3/2 → π/3 و1 → π/2. arccos: 1 → 0 و√3/2 → π/6 و√2/2 → π/4 و1/2 → π/3 و0 → π/2 و−1 → π. arctan: 0 → 0 و1/√3 → π/6 و1 → π/4 و√3 → π/3.",
          "Angle dans l'intervalle principal."),
    ]),
    ("Exact value and composition", "قيمة دقيقة وتركيب", "Valeur exacte et composition", "47", [
        T("A = arcsin(−√3/2): search only inside [−π/2, π/2]. sin(π/3) = √3/2, so for the negative value choose y = −π/3. Check: sin(−π/3) = −√3/2. B = arccos(cos(5π/3)): do not cancel. First Range(arccos) = [0, π]. cos(5π/3) = 1/2, and the angle in [0, π] with cosine 1/2 is π/3. So B = π/3, not 5π/3.",
          "A = arcsin(−√3/2): نبحث فقط داخل [−π/2, π/2]. sin(π/3) = √3/2 فللقيمة السالبة نختار y = −π/3. التحقق: sin(−π/3) = −√3/2. B = arccos(cos(5π/3)): لا نختصر. أولًا Range(arccos) = [0, π]. cos(5π/3) = 1/2 والزاوية في [0, π] التي جيب تمامها 1/2 هي π/3. إذن B = π/3 لا 5π/3.",
          "Principal avant simplification."),
        F("arcsin(−√3/2) = −π/3"),
        F("arccos(cos(5π/3)) = arccos(1/2) = π/3"),
    ]),
    ("Sign reasoning and equations", "استدلال الإشارة والمعادلات", "Signe et équations", "48", [
        T("sin(arccos(3/5)): let θ = arccos(3/5), so cos θ = 3/5 and θ ∈ [0, π]. Cosine positive puts θ in the first quadrant, so sin θ > 0. sin²θ = 1 − 9/25 = 16/25, so sin θ = 4/5, not ±4/5. Equation: arctan(2x − 1) = π/4; π/4 is in the range, apply tan: 2x − 1 = 1, so x = 1. Check: arctan(1) = π/4.",
          "sin(arccos(3/5)): لتكن θ = arccos(3/5) إذن cos θ = 3/5 وθ ∈ [0, π]. جيب التمام الموجب يضع θ في الربع الأول فـ sin θ > 0. sin²θ = 1 − 9/25 = 16/25 إذن sin θ = 4/5 لا ±4/5. معادلة: arctan(2x − 1) = π/4؛ π/4 داخل المدى فنطبق tan: 2x − 1 = 1 إذن x = 1. التحقق: arctan(1) = π/4.",
          "sin θ = 4/5 ; x = 1."),
        F("sin²θ = 16/25  ⇒  sin θ = 4/5"),
    ]),
    ("Domain before derivative", "المجال قبل المشتقة", "Domaine avant dérivée", "49", [
        T("f(x) = arcsin(2x − 1). The input must satisfy −1 ≤ 2x − 1 ≤ 1, so 0 ≤ x ≤ 1 and Df = [0, 1]. For 0 < x < 1: f′(x) = 2 / √(1 − (2x − 1)²). The radicand: 1 − (4x² − 4x + 1) = 4x(1 − x). Hence f′(x) = 1 / √(x(1 − x)). Domain first, derivative second.",
          "f(x) = arcsin(2x − 1). يجب أن يحقق المدخل −1 ≤ 2x − 1 ≤ 1 إذن 0 ≤ x ≤ 1 وDf = [0, 1]. عندما 0 < x < 1: f′(x) = 2 / √(1 − (2x − 1)²). ما تحت الجذر: 1 − (4x² − 4x + 1) = 4x(1 − x). إذن f′(x) = 1 / √(x(1 − x)). المجال أولًا والمشتقة ثانيًا.",
          "Df = [0, 1]."),
        F("f′(x) = 1 / √(x(1 − x)),   0 < x < 1"),
    ]),
    ("A key identity", "متطابقة أساسية", "Une identité", "50", [
        T("Let α = arcsin x. Then sin α = x and cos(π/2 − α) = sin α. Since π/2 − α ∈ [0, π], arccos x = π/2 − α. Therefore arcsin x + arccos x = π/2. Test x = 0: 0 + π/2 = π/2.",
          "لتكن α = arcsin x. إذن sin α = x وcos(π/2 − α) = sin α. وبما أن π/2 − α ∈ [0, π] فإن arccos x = π/2 − α. إذن arcsin x + arccos x = π/2. نختبر x = 0: 0 + π/2 = π/2.",
          "arcsin + arccos = π/2."),
        F("arcsin x + arccos x = π/2"),
    ]),
    ("Error detectives", "المحققون", "Détectives", "51", [
        T("A) arcsin x is not 1/sin x (that is csc x). B) arccos(cos(7π/6)) is not 7π/6: cos(7π/6) = −√3/2 and the principal answer is 5π/6. C) For sin(arccos x), writing ±√(1 − x²) is unfinished: arccos x ∈ [0, π], so sine is nonnegative and sin(arccos x) = √(1 − x²).",
          "أ) arcsin x ليست 1/sin x (تلك csc x). ب) arccos(cos(7π/6)) ليست 7π/6: cos(7π/6) = −√3/2 والجواب الأساسي 5π/6. ج) في sin(arccos x) كتابة ±√(1 − x²) غير مكتملة: arccos x ∈ [0, π] فالجيب غير سالب وsin(arccos x) = √(1 − x²).",
          "Trois erreurs types."),
    ]),
    ("Challenge", "تحدٍّ", "Défi", "52", [
        T("Prove that for −1 < x < 1, arctan(x/√(1 − x²)) = arcsin x. Let θ = arcsin x: sin θ = x, θ ∈ [−π/2, π/2], and cos θ = √(1 − x²) > 0. Then tan θ = x/√(1 − x²), and θ already lies in the principal range of arctan, so arctan(x/√(1 − x²)) = θ = arcsin x.",
          "أثبت أن arctan(x/√(1 − x²)) = arcsin x عندما −1 < x < 1. لتكن θ = arcsin x: sin θ = x وθ ∈ [−π/2, π/2] وcos θ = √(1 − x²) > 0. إذن tan θ = x/√(1 − x²) وθ تقع أصلًا في المدى الأساسي لـ arctan فيكون arctan(x/√(1 − x²)) = θ = arcsin x.",
          "θ = arcsin x."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Principal range first, then algebra, then check. Never cancel a trig function with an inverse-trig function before checking the interval that defines the inverse.",
          "المجال الأساسي أولًا ثم الجبر ثم التحقق. لا نختصر دالة مثلثية مع عكسها قبل التحقق من المجال الذي يعرّف العكس.",
          "Intervalle principal d'abord."),
        F("arcsin: [−1,1]→[−π/2,π/2] ↑    arccos: [−1,1]→[0,π] ↓    arctan: ℝ→]−π/2,π/2[ ↑"),
    ]),
]

EXERCISES = [
    EX("1", "", st("Evaluate arcsin(−√3/2).", "احسب arcsin(−√3/2).", "Calcule arcsin(−√3/2)."), [F("−π/3")]),
    EX("2", "", st("Evaluate arccos(cos(5π/3)) and arccos(cos(4π/3)).", "احسب arccos(cos(5π/3)) وarccos(cos(4π/3)).", "Calcule."), [F("π/3      2π/3")]),
    EX("3", "", st("Compute sin(arccos(3/5)) and cos(arcsin(3/5)).", "احسب sin(arccos(3/5)) وcos(arcsin(3/5)).", "Calcule."), [F("4/5      4/5")]),
    EX("4", "", st("Solve arctan(2x − 1) = π/4 and arcsin(2x) = π/6.", "حلّ arctan(2x − 1) = π/4 وarcsin(2x) = π/6.", "Résous."), [F("x = 1      x = 1/4")]),
    EX("5", "", st("Domain and derivative of arcsin(2x − 1); derivative of arctan(3x).", "المجال والمشتقة لـ arcsin(2x − 1)؛ ومشتقة arctan(3x).", "Domaine et dérivée."), [F("[0, 1]      1/√(x(1 − x))      3/(1 + 9x²)")]),
    EX("6", "", st("Why is arcsin(sin(3π/4)) ≠ 3π/4?", "لماذا arcsin(sin(3π/4)) ≠ 3π/4؟", "Pourquoi ≠ ?"), [T("3π/4 is outside [−π/2, π/2]; the answer is π/4.", "3π/4 خارج [−π/2, π/2] والجواب π/4.", "Résultat π/4.")]),
]
