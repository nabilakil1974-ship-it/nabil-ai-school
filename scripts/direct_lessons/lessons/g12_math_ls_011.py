"""Grade 12 (LS) Mathematics — Integrals."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G12-MATH-LS-011"
GRADE = 12
SUBJECT = "math"
TITLES = {"en": "Integrals", "ar": "التكامل", "fr": "Intégrales"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "∫x⁴ dx = ?", "opts": ["x⁵/5 + C", "x⁴/4 + C", "4x³ + C", "x⁵ + C"], "a": 0,
     "why": {"x⁴/4 + C": _w("Increase the exponent, then divide by the new one.", "نزيد الأس ثم نقسم على الجديد.", "Exposant + 1."),
             "4x³ + C": _w("That is the derivative.", "هذه المشتقة.", "Dérivée."),
             "x⁵ + C": _w("Divide by 5.", "نقسم على 5.", "Divise par 5.")}, "ok": "x⁵/5 + C"},
    {"q": "∫₁³ (2x + 1) dx = ?", "opts": ["10", "12", "2", "8"], "a": 0,
     "why": {"12": _w("That is F(3) alone.", "هذه F(3) وحدها.", "F(3) seul."),
             "2": _w("That is F(1) alone.", "هذه F(1) وحدها.", "F(1) seul."),
             "8": _w("F(3) − F(1) = 12 − 2.", "F(3) − F(1) = 12 − 2.", "12 − 2.")}, "ok": "F(3) − F(1) = 10"},
    {"q": "∫₋₁¹ x dx = ?", "opts": ["0", "1", "2", "−1"], "a": 0,
     "why": {"1": _w("Positive and negative parts cancel.", "الجزآن الموجب والسالب يتلاشيان.", "Elles s'annulent."),
             "2": _w("[x²/2] from −1 to 1 is 0.", "[x²/2] من −1 إلى 1 تساوي 0.", "= 0."),
             "−1": _w("Signed areas cancel.", "المساحتان الموقّعتان تتلاشيان.", "S'annulent.")}, "ok": "signed integral"},
]

THEORY = [
    ("Reverse the derivative", "نعكس الاشتقاق", "Inverser la dérivation", "", [
        T("Hello! Let me start with a question, not a law. You know how to differentiate. Today I give you the derivative and ask you to go back to the function. (x³)′ = 3x². If f(x) = 3x² and F′(x) = f(x), what can F be? F(x) = x³. But it is not unique: x³ + 2 and x³ − 100 have the same derivative. Any constant may be added without changing the derivative.",
          "مرحبًا! أبدأ بسؤال لا بقانون. أنت تعرف كيف نشتق. اليوم أعطيك المشتقة وأطلب أن تعود إلى الدالة. (x³)′ = 3x². إذا كانت f(x) = 3x² وF′(x) = f(x) فماذا تكون F؟ F(x) = x³. لكنها ليست وحيدة: x³ + 2 وx³ − 100 لهما المشتقة نفسها. يمكن إضافة أي ثابت دون تغيير المشتقة.",
          "Primitive non unique."),
    ]),
    ("Primitive", "الدالة الأصلية", "Primitive", "", [
        T("F is a primitive of f on an interval I if F′(x) = f(x) for every x in I. So for f(x) = 3x²: F(x) = x³ + C, because (C)′ = 0. Check: the primitives of 2x are x² + C since (x² + C)′ = 2x. Compare y = x², y = x² + 2, y = x² − 3: vertical translations, yet the slope at the same x is 2x on all of them. A primitive is a family of curves differing by a constant.",
          "F أصيلة للدالة f على مجال I إذا كانت F′(x) = f(x) لكل x في I. إذن لـ f(x) = 3x²: F(x) = x³ + C لأن (C)′ = 0. تحقق: أصيلات 2x هي x² + C لأن (x² + C)′ = 2x. قارن y = x² وy = x² + 2 وy = x² − 3: انسحابات رأسية لكن الميل عند x نفسها هو 2x على كلها. الأصيلة عائلة منحنيات تختلف بثابت.",
          "Famille F + C."),
        F("F′ = f   ⇒   F(x) + C"),
    ]),
    ("Power rule for primitives", "قاعدة القوة للأصيلات", "Règle de puissance", "", [
        T("Since (x^(n+1))′ = (n+1)xⁿ, divide by n + 1: ∫xⁿ dx = x^(n+1)/(n+1) + C, n ≠ −1. Why n ≠ −1? The formula would divide by zero. Since (ln|x|)′ = 1/x on intervals not crossing zero, ∫(1/x) dx = ln|x| + C. Check: ∫x⁴ dx = x⁵/5 + C because (x⁵/5)′ = x⁴.",
          "بما أن (x^(n+1))′ = (n+1)xⁿ نقسم على n + 1: ∫xⁿ dx = x^(n+1)/(n+1) + C مع n ≠ −1. لماذا n ≠ −1؟ لأن الصيغة ستقسم على صفر. وبما أن (ln|x|)′ = 1/x على مجالات لا تقطع الصفر فإن ∫(1/x) dx = ln|x| + C. تحقق: ∫x⁴ dx = x⁵/5 + C لأن (x⁵/5)′ = x⁴.",
          "ln|x| pour 1/x."),
        F("∫ xⁿ dx = x^(n+1) / (n + 1) + C"),
        F("∫ (1/x) dx = ln|x| + C"),
    ]),
    ("Linearity and a full example", "الخطية ومثال كامل", "Linéarité et exemple", "", [
        T("∫(af + bg) = a∫f + b∫g. Example: f(x) = 3x² − 4x + 5. Split and integrate each term: ∫3x² = x³, ∫−4x = −2x², ∫5 = 5x. So F(x) = x³ − 2x² + 5x + C, with a single C (the sum of three constants is just another constant). Check: F′(x) = 3x² − 4x + 5.",
          "∫(af + bg) = a∫f + b∫g. مثال: f(x) = 3x² − 4x + 5. نفصل ونكامل كل حد: ∫3x² = x³ و∫−4x = −2x² و∫5 = 5x. إذن F(x) = x³ − 2x² + 5x + C بثابت واحد فقط (مجموع ثلاثة ثوابت هو ثابت آخر). التحقق: F′(x) = 3x² − 4x + 5.",
          "Un seul C."),
        F("F(x) = x³ − 2x² + 5x + C"),
    ]),
    ("A condition picks one primitive", "الشرط يختار أصيلة واحدة", "Une condition", "", [
        T("If F(x) = x³ + C and F(1) = 5, then 1 + C = 5, so C = 4. Another: F′(x) = 2x − 3 and F(2) = 7. Family first: F(x) = x² − 3x + C. Condition second: 4 − 6 + C = 7, so C = 9 and F(x) = x² − 3x + 9. Check: F′(x) = 2x − 3 and F(2) = 7.",
          "إذا كانت F(x) = x³ + C وF(1) = 5 فإن 1 + C = 5 إذن C = 4. مثال آخر: F′(x) = 2x − 3 وF(2) = 7. العائلة أولًا: F(x) = x² − 3x + C. والشرط ثانيًا: 4 − 6 + C = 7 إذن C = 9 وF(x) = x² − 3x + 9. تحقق: F′(x) = 2x − 3 وF(2) = 7.",
          "C = 9."),
        F("F(x) = x² − 3x + 9"),
    ]),
    ("Accumulation: Riemann rectangles", "التراكم: مستطيلات ريمان", "Accumulation : rectangles", "", [
        T("For f(x) ≥ 0 between a and b, divide the interval into thin strips. Each has approximate area f(xᵢ)Δx, and the sum Σ f(xᵢ)Δx approaches the exact accumulated area as the strips get thinner. Try f(x) = x² on [0, 2] with 2, 4, 8, 50 rectangles: as Δx decreases the approximation approaches a fixed value. This motivates ∫ₐᵇ f(x) dx.",
          "عندما f(x) ≥ 0 بين a وb نقسم المجال إلى شرائح رقيقة. لكل شريحة مساحة تقريبية f(xᵢ)Δx والمجموع Σ f(xᵢ)Δx يقترب من المساحة المتراكمة الدقيقة كلما رقّت الشرائح. جرّب f(x) = x² على [0, 2] بـ 2 و4 و8 و50 مستطيلًا: كلما نقصت Δx اقترب التقريب من قيمة ثابتة. هذا يبرر ∫ₐᵇ f(x) dx.",
          "Somme de Riemann."),
    ]),
    ("The fundamental connection", "الرابط الأساسي", "Lien fondamental", "", [
        T("If F is a primitive of f then ∫ₐᵇ f(x) dx = F(b) − F(a): find a primitive, evaluate at two endpoints, subtract. Example ∫₀² 3x² dx: F(x) = x³, so 8 − 0 = 8 (reasonable: 3x² ≥ 0 so the result is positive). Why does C disappear? [F(b) + C] − [F(a) + C] = F(b) − F(a).",
          "إذا كانت F أصيلة لـ f فإن ∫ₐᵇ f(x) dx = F(b) − F(a): نجد أصيلة ونحسبها عند الطرفين ونطرح. مثال ∫₀² 3x² dx: F(x) = x³ إذن 8 − 0 = 8 (معقول: 3x² ≥ 0 فالناتج موجب). لماذا يختفي C؟ [F(b) + C] − [F(a) + C] = F(b) − F(a).",
          "F(b) − F(a)."),
        F("∫₀² 3x² dx = [x³]₀² = 8 − 0 = 8"),
    ]),
    ("Signed area", "المساحة الموقّعة", "Aire algébrique", "", [
        T("∫₋₁¹ x dx = [x²/2]₋₁¹ = 0: positive and negative contributions cancel. A definite integral is signed accumulation. For f(x) = x on [−2, 3]: the signed integral is 9/2 − 4/2 = 5/2, but the geometric area is the left triangle 2 plus the right triangle 9/2, total 13/2. Signed integral ≠ geometric area whenever negative regions exist.",
          "∫₋₁¹ x dx = [x²/2]₋₁¹ = 0: المساهمتان الموجبة والسالبة تتلاشيان. التكامل المحدود تراكم موقّع. وفي f(x) = x على [−2, 3]: التكامل الموقّع 9/2 − 4/2 = 5/2 لكن المساحة الهندسية هي المثلث الأيسر 2 زائد الأيمن 9/2 أي 13/2. التكامل الموقّع ≠ المساحة الهندسية كلما وُجدت مناطق سالبة.",
          "Aire ≠ intégrale."),
        F("∫₋₂³ x dx = 5/2      aire = 2 + 9/2 = 13/2"),
    ]),
    ("Student try", "جرّب بنفسك", "À toi", "", [
        T("∫₁³ (2x + 1) dx. Primitive F(x) = x² + x. F(3) = 12, F(1) = 2, result 10. Independent geometric check: y = 2x + 1 has heights 3 and 7 at x = 1 and x = 3, so the trapezoid area is (3 + 7)/2 × 2 = 10. Strong solutions use two independent paths: calculus and geometry.",
          "∫₁³ (2x + 1) dx. الأصيلة F(x) = x² + x. F(3) = 12 وF(1) = 2 والناتج 10. تحقق هندسي مستقل: y = 2x + 1 ارتفاعاها 3 و7 عند x = 1 وx = 3 فمساحة شبه المنحرف (3 + 7)/2 × 2 = 10. الحلول القوية تستعمل طريقين مستقلين: التفاضل والهندسة.",
          "10 des deux façons."),
        F("F(3) − F(1) = 12 − 2 = 10"),
    ]),
    ("Error detectives", "المحققون", "Détectives", "", [
        T("1) ∫x² dx = x³ + C is false: it is x³/3 + C. 2) Forgetting +C in an indefinite integral. 3) ∫(1/x) dx = x⁰/0 is impossible: it is ln|x| + C. 4) Computing F(a) − F(b): the order is F(b) − F(a). 5) “The integral is always positive because area is positive”: a definite integral is signed. Also ∫₁² x² dx = 8/3 − 1/3 = 7/3.",
          "1) ∫x² dx = x³ + C خطأ: هي x³/3 + C. 2) نسيان +C في التكامل غير المحدود. 3) ∫(1/x) dx = x⁰/0 مستحيلة: هي ln|x| + C. 4) حساب F(a) − F(b): الترتيب F(b) − F(a). 5) «التكامل دائمًا موجب لأن المساحة موجبة»: التكامل المحدود موقّع. وكذلك ∫₁² x² dx = 8/3 − 1/3 = 7/3.",
          "Cinq erreurs types."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("The integral has two linked meanings: the reverse of the derivative (a primitive family F + C) and accumulation (the definite integral), connected by F(b) − F(a). Procedure: understand, plan, find a primitive, check by differentiation, apply endpoints or conditions, and check independently.",
          "للتكامل معنيان مترابطان: عكس الاشتقاق (عائلة أصيلات F + C) والتراكم (التكامل المحدود) ويربطهما F(b) − F(a). الإجراء: نفهم ونخطط ونجد أصيلة ونتحقق بالاشتقاق ونطبق الطرفين أو الشروط ونتحقق باستقلال.",
          "Primitive et accumulation."),
    ]),
]

EXERCISES = [
    EX("1", "", st("Find primitives of 4x³, 6x, 5.", "أوجد أصيلات 4x³ وـ 6x وـ 5.", "Primitives."), [F("x⁴ + C      3x² + C      5x + C")]),
    EX("2", "", st("Find ∫(3x² + 2x − 4) dx.", "أوجد ∫(3x² + 2x − 4) dx.", "Calcule."), [F("x³ + x² − 4x + C")]),
    EX("3", "", st("F′(x) = 3x² + 1 and F(0) = 4. Find F.", "F′(x) = 3x² + 1 وF(0) = 4. أوجد F.", "Trouve F."), [F("F(x) = x³ + x + 4")]),
    EX("4", "", st("Evaluate ∫₀¹ (4x³ + 2x) dx.", "احسب ∫₀¹ (4x³ + 2x) dx.", "Calcule."), [F("[x⁴ + x²]₀¹ = 2")]),
    EX("5", "", st("Geometric area bounded by y = x, the x-axis, x = −2, x = 3.", "المساحة المحصورة بين y = x ومحور الفواصل وx = −2 وx = 3.", "Aire géométrique."), [F("2 + 9/2 = 13/2")]),
]
