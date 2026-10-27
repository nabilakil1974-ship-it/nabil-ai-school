"""Grade 12 (GS) Mathematics — Differential calculus (Rolle, MVT, L'Hôpital)."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G12-MATH-GS-004"
GRADE = 12
SUBJECT = "math"
TITLES = {"en": "Differential calculus", "ar": "التفاضل", "fr": "Calcul différentiel"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "Rolle: f(x) = x² − 4x + 3 on [1, 3]. c = ?", "opts": ["2", "1", "3", "0"], "a": 0,
     "why": {"1": _w("c must be interior.", "يجب أن تكون c داخلية.", "Intérieur."),
             "3": _w("c must be interior.", "يجب أن تكون c داخلية.", "Intérieur."),
             "0": _w("f′(c) = 2c − 4 = 0 gives 2.", "2c − 4 = 0 تعطي 2.", "c = 2.")}, "ok": "c = 2"},
    {"q": "f(a) = f(b). Does Rolle apply automatically?", "opts": ["No: check continuity and differentiability", "Yes", "Only for polynomials", "Only if f′ > 0"], "a": 0,
     "why": {"Yes": _w("|x| on [−1, 1] is a counterexample.", "|x| على [−1, 1] مثال مضاد.", "Contre-exemple |x|."),
             "Only for polynomials": _w("Polynomials qualify, but so do others.", "كثيرات الحدود تحقق وغيرها أيضًا.", "Autres aussi."),
             "Only if f′ > 0": _w("Then equal endpoints are impossible.", "عندها لا تتساوى الأطراف.", "Impossible.")}, "ok": "check hypotheses"},
    {"q": "lim x→2 (x² − 4)/(x − 2) = ?", "opts": ["4", "0", "2", "∞"], "a": 0,
     "why": {"0": _w("Form 0/0: factor (x−2)(x+2).", "الشكل 0/0: نحلّل.", "0/0."),
             "2": _w("x + 2 → 4.", "x + 2 → 4.", "x + 2 → 4."),
             "∞": _w("The factor x − 2 cancels.", "العامل x − 2 يُختصر.", "Se simplifie.")}, "ok": "4"},
]

THEORY = [
    ("A local slope controls an interval", "ميل محلي يتحكم في مجال", "Une pente locale contrôle un intervalle", "49", [
        T("Hello! A derivative is local: it describes one point. Yet Rolle's theorem and the Mean Value Theorem make statements about a whole interval. Draw a smooth curve from A to B and the secant AB. If the curve begins and ends at the same height, the secant slope is 0, and intuition says some tangent is horizontal. Rolle makes that precise.",
          "مرحبًا! المشتقة محلية: تصف نقطة واحدة. ومع ذلك فإن مبرهنة رول ومبرهنة القيمة المتوسطة تتحدثان عن مجال كامل. ارسم منحنى أملس من A إلى B والقاطع AB. إذا بدأ المنحنى وانتهى بالارتفاع نفسه فميل القاطع 0 ويقول الحدس إن مماسًا ما أفقي. رول تجعل ذلك دقيقًا.",
          "Pente locale, intervalle global."),
    ]),
    ("Rolle: hypotheses first", "رول: الفرضيات أولًا", "Rolle : hypothèses", "50", [
        T("If f is continuous on [a, b], differentiable on ]a, b[, and f(a) = f(b), then there is at least one c ∈ ]a, b[ with f′(c) = 0. The theorem is a contract: three hypotheses buy one conclusion. Continuity prevents jumps; differentiability prevents corners; equal endpoints make the secant slope 0. It guarantees at least one c, not a unique one.",
          "إذا كانت f مستمرة على [a, b] وقابلة للاشتقاق على ]a, b[ وf(a) = f(b) فإنه يوجد c واحدة على الأقل في ]a, b[ تحقق f′(c) = 0. المبرهنة عقد: ثلاث فرضيات تشتري نتيجة واحدة. الاستمرار يمنع القفزات والاشتقاق يمنع الزوايا وتساوي الطرفين يجعل ميل القاطع 0. وهي تضمن c واحدة على الأقل لا وحيدة.",
          "Trois hypothèses, une conclusion."),
        F("f continuous, differentiable, f(a) = f(b)  ⇒  ∃ c : f′(c) = 0"),
    ]),
    ("Verify Rolle", "نتحقق من رول", "Vérifier Rolle", "51", [
        T("f(x) = x² − 4x + 3 on [1, 3]. A polynomial is continuous and differentiable. f(1) = 0 and f(3) = 0. f′(x) = 2x − 4, so 2c − 4 = 0 and c = 2, which lies in ]1, 3[. We started from the hypotheses, not from the derivative.",
          "f(x) = x² − 4x + 3 على [1, 3]. كثير الحدود مستمر وقابل للاشتقاق. f(1) = 0 وf(3) = 0. f′(x) = 2x − 4 إذن 2c − 4 = 0 وc = 2 وهي تنتمي إلى ]1, 3[. بدأنا من الفرضيات لا من المشتقة.",
          "c = 2."),
        F("f(1) = f(3) = 0      f′(c) = 2c − 4 = 0  →  c = 2"),
    ]),
    ("Mean Value Theorem", "مبرهنة القيمة المتوسطة", "Théorème des accroissements finis", "52", [
        T("If f is continuous on [a, b] and differentiable on ]a, b[, there is c ∈ ]a, b[ with f′(c) = [f(b) − f(a)] / (b − a): a tangent parallel to the secant AB. Rolle is the special case f(a) = f(b). Example: f(x) = x² on [1, 3]. Average slope (9 − 1)/2 = 4, f′(c) = 2c = 4, so c = 2.",
          "إذا كانت f مستمرة على [a, b] وقابلة للاشتقاق على ]a, b[ فيوجد c ∈ ]a, b[ يحقق f′(c) = [f(b) − f(a)] / (b − a): مماس موازٍ للقاطع AB. رول حالة خاصة حيث f(a) = f(b). مثال: f(x) = x² على [1, 3]. الميل المتوسط (9 − 1)/2 = 4 وf′(c) = 2c = 4 إذن c = 2.",
          "Tangente parallèle."),
        F("f′(c) = (f(b) − f(a)) / (b − a)"),
    ]),
    ("Monotonicity and comparison", "الرتابة والمقارنة", "Monotonie et comparaison", "53", [
        T("Suppose f′ > 0 on an interval and x₁ < x₂. The theorem gives c with [f(x₂) − f(x₁)] / (x₂ − x₁) = f′(c) > 0, so f(x₂) > f(x₁). Hence f′ > 0 ⇒ strictly increasing; f′ < 0 ⇒ strictly decreasing; f′ = 0 everywhere ⇒ constant. If f′ = g′ on an interval, then f − g is constant. And a strictly increasing function takes each value at most once.",
          "لنفرض f′ > 0 على مجال وx₁ < x₂. تعطي المبرهنة c بحيث [f(x₂) − f(x₁)] / (x₂ − x₁) = f′(c) > 0 فيكون f(x₂) > f(x₁). إذن f′ > 0 ⇒ متزايدة تمامًا؛ f′ < 0 ⇒ متناقصة تمامًا؛ f′ = 0 في كل مكان ⇒ ثابتة. وإذا كانت f′ = g′ على مجال فإن f − g ثابتة. والدالة المتزايدة تمامًا تأخذ كل قيمة مرة واحدة على الأكثر.",
          "Signe de f′."),
    ]),
    ("L'Hôpital: name the form first", "لوبيتال: نسمّي الشكل أولًا", "L'Hôpital : nommer la forme", "54", [
        T("Before touching derivatives, substitute and say the form aloud. Valid targets: 0/0 or ∞/∞, under the theorem's conditions. The rule: lim f/g = lim f′/g′ when the derivative quotient has a limit. It means differentiate numerator and denominator separately, not the quotient. Nonzero/0 is not an indeterminate form.",
          "قبل أن نشتق نعوّض ونقول الشكل بصوت عالٍ. الأشكال الصالحة: 0/0 أو ∞/∞ بشروط المبرهنة. القاعدة: lim f/g = lim f′/g′ عندما يكون لحاصل المشتقتين نهاية. أي نشتق البسط والمقام كلًّا على حدة لا حاصل القسمة. والشكل غير الصفري/0 ليس شكلًا غير معيّن.",
          "0/0 ou ∞/∞."),
        F("lim f/g = lim f′/g′"),
    ]),
    ("Factor or L'Hôpital?", "نحلّل أم لوبيتال؟", "Factoriser ou L'Hôpital ?", "55", [
        T("lim x→2 (x² − 4)/(x − 2): substituting gives 0/0. Factor: (x − 2)(x + 2)/(x − 2) = x + 2 → 4. L'Hôpital gives 2x/1 → 4. Both agree: the tool is not a reflex. Second example: lim x→0 [√(1 + x) − 1]/x is 0/0. L'Hôpital: 1/[2√(1 + x)] → 1/2; or multiply by the conjugate to get 1/[√(1 + x) + 1] → 1/2.",
          "lim x→2 (x² − 4)/(x − 2): التعويض يعطي 0/0. نحلّل: (x − 2)(x + 2)/(x − 2) = x + 2 → 4. ولوبيتال تعطي 2x/1 → 4. الطريقتان تتفقان: الأداة ليست ردّة فعل. مثال ثانٍ: lim x→0 [√(1 + x) − 1]/x هو 0/0. لوبيتال: 1/[2√(1 + x)] → 1/2؛ أو نضرب في المرافق فنحصل 1/[√(1 + x) + 1] → 1/2.",
          "Deux méthodes, même résultat."),
        F("(x² − 4)/(x − 2) = x + 2 → 4"),
        F("[√(1 + x) − 1]/x = 1/(√(1 + x) + 1) → 1/2"),
    ]),
    ("MVT as an estimate", "المبرهنة كتقدير", "TAF comme majoration", "56", [
        T("Prove that for x > 0 and h > 0: √(x + h) − √x < h / (2√x). Take f(t) = √t on [x, x + h]. For some c ∈ (x, x + h): √(x + h) − √x = h/(2√c). Since c > x, √c > √x, so 1/(2√c) < 1/(2√x). The derivative gives a bound on a finite change.",
          "أثبت أنه من أجل x > 0 وh > 0: √(x + h) − √x < h / (2√x). نأخذ f(t) = √t على [x, x + h]. يوجد c ∈ (x, x + h) بحيث √(x + h) − √x = h/(2√c). وبما أن c > x فإن √c > √x فيكون 1/(2√c) < 1/(2√x). المشتقة تعطينا حدًّا لتغيّر منتهٍ.",
          "Majoration par f′."),
    ]),
    ("Existence and uniqueness", "الوجود والوحدانية", "Existence et unicité", "57", [
        T("Show that x³ + x − 1 has exactly one real root. Uniqueness: f′(x) = 3x² + 1 > 0, so f is strictly increasing and crosses the x-axis at most once. Existence: f(0) = −1 and f(1) = 1, and by continuity there is a root in (0, 1). At least one plus at most one gives exactly one. Derivative alone does not prove existence.",
          "بيّن أن x³ + x − 1 لها جذر حقيقي واحد بالضبط. الوحدانية: f′(x) = 3x² + 1 > 0 فالدالة متزايدة تمامًا وتقطع محور الفواصل مرة واحدة على الأكثر. الوجود: f(0) = −1 وf(1) = 1 وبالاستمرار يوجد جذر في (0, 1). واحد على الأقل مع واحد على الأكثر يعطي واحدًا بالضبط. والمشتقة وحدها لا تثبت الوجود.",
          "Existence + unicité."),
        F("f′(x) = 3x² + 1 > 0      f(0) = −1      f(1) = 1"),
    ]),
    ("Error detectives", "المحققون", "Détectives", "58", [
        T("A) “f(a) = f(b) so Rolle applies”: |x| on [−1, 1] has equal endpoints but is not differentiable at 0 and no c has f′(c) = 0. B) Applying L'Hôpital to nonzero/0. C) Differentiating the whole quotient: it is f′/g′, not (f/g)′.",
          "أ) «f(a) = f(b) إذن رول تنطبق»: الدالة |x| على [−1, 1] لها طرفان متساويان لكنها غير قابلة للاشتقاق عند 0 ولا توجد c بها f′(c) = 0. ب) تطبيق لوبيتال على غير صفري/0. ج) اشتقاق حاصل القسمة كله: هو f′/g′ لا (f/g)′.",
          "Trois erreurs."),
    ]),
    ("Practice and challenge", "تدريب وتحدٍّ", "Entraînement et défi", "59", [
        T("f(x) = 1/x on [1, 2]: secant slope −1/2, f′(x) = −1/x², so −1/c² = −1/2, c² = 2, c = √2 ∈ (1, 2). lim x→1 (x³ − 1)/(x² − 1): 0/0, L'Hôpital 3x²/(2x) → 3/2. Challenge: if f is continuous on [0, 1], differentiable on (0, 1), f(0) = 0 and f(1) = 1, the secant slope is 1, so by the Mean Value Theorem some c ∈ (0, 1) has f′(c) = 1.",
          "f(x) = 1/x على [1, 2]: ميل القاطع −1/2 وf′(x) = −1/x² إذن −1/c² = −1/2 وc² = 2 وc = √2 ∈ (1, 2). lim x→1 (x³ − 1)/(x² − 1): الشكل 0/0 ولوبيتال 3x²/(2x) → 3/2. تحدٍّ: إذا كانت f مستمرة على [0, 1] وقابلة للاشتقاق على (0, 1) وf(0) = 0 وf(1) = 1 فميل القاطع 1 وبمبرهنة القيمة المتوسطة يوجد c ∈ (0, 1) بحيث f′(c) = 1.",
          "c = √2 ; limite 3/2."),
        F("c = √2      3/2"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Hypotheses first, theorem second, calculation third, check last. For limits: form first, method second.",
          "الفرضيات أولًا والمبرهنة ثانيًا والحساب ثالثًا والتحقق أخيرًا. وفي النهايات: الشكل أولًا والطريقة ثانيًا.",
          "Hypothèses, théorème, calcul, vérification."),
    ]),
]

EXERCISES = [
    EX("1", "", st("f(x) = x² − 6x + 8 on [2, 4]: verify Rolle and find c.", "f(x) = x² − 6x + 8 على [2, 4]: تحقق من رول وأوجد c.", "Vérifie Rolle."), [F("f(2) = f(4) = 0      f′ = 2x − 6      c = 3")]),
    EX("2", "", st("f(x) = x³ on [0, 2]: find an MVT point.", "f(x) = x³ على [0, 2]: أوجد نقطة المبرهنة.", "Trouve c."), [F("3c² = 4      c = 2/√3")]),
    EX("3", "", st("Evaluate lim x→3 (x² − 9)/(x − 3).", "احسب lim x→3 (x² − 9)/(x − 3).", "Calcule."), [F("x + 3 → 6")]),
    EX("4", "", st("Why does Rolle fail for |x| on [−1, 1]?", "لماذا تفشل رول للدالة |x| على [−1, 1]؟", "Pourquoi Rolle échoue ?"), [T("Not differentiable at 0.", "غير قابلة للاشتقاق عند 0.", "Non dérivable en 0.")]),
    EX("5", "", st("If f′ > 0 on ℝ, what about f(x) = k?", "إذا كانت f′ > 0 على ℝ فماذا عن f(x) = k؟", "Si f′ > 0."), [T("At most one real solution.", "حل حقيقي واحد على الأكثر.", "Au plus une solution.")]),
]
