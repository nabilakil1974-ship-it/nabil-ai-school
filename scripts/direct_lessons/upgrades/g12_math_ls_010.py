"""Upgrade: Power functions — graphs for every family and many worked exercises."""
import math
from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import fn_graph, section


def _t(en, ar, fr):
    return T(en, ar, fr)


def upgrade(m):
    s = section(m, "Integer exponents and parity")
    s.append(fn_graph(lambda x: x ** 2, (-3, 3), (-1, 9), curves=[lambda x: x ** 4], pts={"O": (0, 0), "A": (1, 1), "B": (-1, 1)}, tag="P1", label="x² (red), x⁴ (dashed)"))
    s.append(_t("Both curves are even: the left half is the mirror of the right half in the y-axis. They share the points (−1, 1), (0, 0) and (1, 1). Between −1 and 1, x⁴ is flatter (closer to the axis); outside, x⁴ climbs faster.",
                "كلا المنحنيين زوجي: النصف الأيسر صورة النصف الأيمن في مرآة محور التراتيب. يشتركان في النقاط (−1, 1) و(0, 0) و(1, 1). بين −1 و1 يكون x⁴ أكثر تسطحًا (أقرب إلى المحور)، وخارج هذا المجال يصعد أسرع.",
                "Les deux courbes sont paires, symétriques par rapport à l'axe des ordonnées, et passent par (−1 ; 1), (0 ; 0), (1 ; 1). Entre −1 et 1, x⁴ est plus plate ; au-delà, elle monte plus vite."))
    s.append(fn_graph(lambda x: x ** 3, (-3, 3), (-8, 8), curves=[lambda x: x ** 5], pts={"O": (0, 0), "A": (1, 1), "B": (-1, -1)}, tag="P2", label="x³ (red), x⁵ (dashed)"))
    s.append(_t("Odd powers are symmetric about the origin: rotate the right half by 180° to get the left half. They are increasing on all of ℝ and pass through (−1, −1), (0, 0), (1, 1). At 0 the tangent is the x-axis, so the curve flattens as it crosses.",
                "القوى الفردية متناظرة حول المبدأ: ندير النصف الأيمن 180° فنحصل على النصف الأيسر. وهي متزايدة على ℝ وتمر بالنقاط (−1, −1) و(0, 0) و(1, 1). عند 0 يكون المماس هو محور الفواصل فيتسطح المنحنى وهو يعبر.",
                "Les puissances impaires sont symétriques par rapport à l'origine, croissantes sur ℝ, et passent par (−1 ; −1), (0 ; 0), (1 ; 1). En 0 la tangente est l'axe des abscisses."))

    s = section(m, "Negative integer powers")
    s.append(fn_graph(lambda x: 1 / x ** 2, (-4, 4), (-1, 8), curves=[], pts={"A": (1, 1), "B": (-1, 1), "C": (2, 0.25)}, vlines=[0], hlines=[0], poles=[0], tag="P3", label="x⁻² = 1/x²"))
    s.append(_t("1/x² is even and always positive. It has two asymptotes: the y-axis (x = 0), where the curve shoots to +∞ on both sides, and the x-axis (y = 0), which it approaches as |x| grows. The curve never touches either.",
                "1/x² زوجية وموجبة دائمًا. لها مقاربان: محور التراتيب (x = 0) حيث يصعد المنحنى إلى +∞ من الجهتين، ومحور الفواصل (y = 0) الذي يقترب منه كلما كبر |x|. لا يلمس المنحنى أيًّا منهما.",
                "1/x² est paire et positive. Deux asymptotes : l'axe des ordonnées (la courbe tend vers +∞ des deux côtés) et l'axe des abscisses. Elle ne les touche jamais."))
    s.append(fn_graph(lambda x: 1 / x ** 3, (-4, 4), (-6, 6), pts={"A": (1, 1), "B": (-1, -1)}, vlines=[0], hlines=[0], poles=[0], tag="P4", label="x⁻³ = 1/x³"))
    s.append(_t("1/x³ is odd: its two branches are in opposite quadrants. Near 0 from the right it goes to +∞, from the left to −∞. It is decreasing on each of (−∞, 0) and (0, +∞), but not on their union.",
                "1/x³ فردية: فرعاها في ربعين متقابلين. قرب 0 من اليمين تؤول إلى +∞ ومن اليسار إلى −∞. وهي متناقصة على كل من (−∞, 0) و(0, +∞) لكن ليس على اتحادهما.",
                "1/x³ est impaire : deux branches dans des quadrants opposés. Décroissante sur chaque intervalle, mais pas sur leur réunion."))

    s = section(m, "Rational exponents")
    s.append(fn_graph(lambda x: math.sqrt(x), (0, 9), (-1, 4), curves=[lambda x: x ** (1 / 3)], pts={"A": (1, 1), "B": (4, 2), "C": (9, 3)}, tag="P5", label="√x (red), ∛x (dashed)"))
    s.append(_t("√x starts at the origin and rises slowly: (1, 1), (4, 2), (9, 3). Its tangent at 0 is vertical. Compare with the cube root (dashed): for 0 < x < 1 it is above √x, and for x > 1 it is below √x.",
                "√x يبدأ من المبدأ ويرتفع ببطء: (1, 1) و(4, 2) و(9, 3). مماسه عند 0 شاقولي. قارنه بالجذر التكعيبي (المتقطع): من أجل 0 < x < 1 يكون فوق √x ومن أجل x > 1 يكون تحته.",
                "√x part de l'origine et monte lentement : (1 ; 1), (4 ; 2), (9 ; 3). Tangente verticale en 0. Pour 0 < x < 1, ∛x est au-dessus de √x ; pour x > 1 en dessous."))
    s.append(fn_graph(lambda x: x ** 1.5, (0, 4), (-1, 9), pts={"A": (1, 1), "B": (4, 8)}, tag="P6", label="x^(3/2) = x√x"))
    s.append(_t("x^(3/2) = x√x grows faster than x but slower than x². At 0 the tangent is horizontal because the derivative (3/2)√x is 0 there. Check: at x = 4, 4 × 2 = 8.",
                "x^(3/2) = x√x تنمو أسرع من x وأبطأ من x². عند 0 المماس أفقي لأن المشتقة (3/2)√x تساوي 0 هناك. تحقق: عند x = 4 نجد 4 × 2 = 8.",
                "x^(3/2) = x√x croît plus vite que x, moins que x². Tangente horizontale en 0. Vérification : x = 4 → 4 × 2 = 8."))

    s = section(m, "Monotonicity, concavity, limits")
    s.append(fn_graph(lambda x: x ** 0.5, (0, 5), (0, 3), curves=[lambda x: x, lambda x: x ** 2], pts={"A": (1, 1)}, tag="P7", label="x^a: a=1/2 (red), a=1, a=2 (dashed)"))
    s.append(_t("All curves x^a pass through (1, 1). For a < 1 the curve is concave (bends down): √x. For a > 1 it is convex (bends up): x². The line y = x (a = 1) separates the two behaviours.",
                "كل منحنيات x^a تمر بالنقطة (1, 1). من أجل a < 1 يكون المنحنى مقعّرًا نحو الأسفل: √x. ومن أجل a > 1 يكون محدبًا نحو الأعلى: x². المستقيم y = x (a = 1) يفصل بين السلوكين.",
                "Toutes les courbes x^a passent par (1 ; 1). Pour a < 1 : concave (√x) ; pour a > 1 : convexe (x²). La droite y = x (a = 1) sépare les deux comportements."))

    s = section(m, "Complete study of x^(−3/2)")
    s.append(fn_graph(lambda x: x ** -1.5, (0, 5), (0, 6), pts={"A": (1, 1), "B": (4, 0.125)}, vlines=[0], hlines=[0], poles=[0], tag="P8", label="f(x) = x^(−3/2)"))
    s.append(_t("The study gives: domain (0, +∞); f′(x) = −(3/2)x^(−5/2) < 0, so f is decreasing; limit +∞ at 0⁺ and 0 at +∞; so both axes are asymptotes. The graph confirms every line: a falling curve hugging the y-axis then the x-axis.",
                "الدراسة تعطي: المجال (0, +∞)؛ f′(x) = −(3/2)x^(−5/2) < 0 إذن f متناقصة؛ النهاية +∞ عند 0⁺ و0 عند +∞؛ فكلا المحورين مقاربان. والرسم يؤكد كل سطر: منحنى هابط يلتصق بمحور التراتيب ثم بمحور الفواصل.",
                "Étude : domaine ]0 ; +∞[ ; f′(x) = −(3/2)x^(−5/2) < 0, f décroît ; limite +∞ en 0⁺ et 0 en +∞ ; les deux axes sont asymptotes. Le graphique confirme tout."))
    s.append(F("x: 0⁺ → +∞   f′ < 0   f: +∞ ↘ 0"))

    m.EXERCISES[:] = [
        EX("1", "", st("State the domain, parity and monotonicity of x⁶, x⁷ and x⁻⁵.", "عيّن المجال والزوجية والرتابة لكل من x⁶ وx⁷ وx⁻⁵.", "Domaine, parité et monotonie de x⁶, x⁷, x⁻⁵."), [
            T("x⁶: domain ℝ; (−x)⁶ = x⁶ so even; derivative 6x⁵ is negative for x < 0 and positive for x > 0: decreasing then increasing, minimum 0 at x = 0.", "x⁶: المجال ℝ؛ (−x)⁶ = x⁶ إذن زوجية؛ المشتقة 6x⁵ سالبة عند x < 0 وموجبة عند x > 0: متناقصة ثم متزايدة وللدالة قيمة صغرى 0 عند x = 0.", "x⁶ : ℝ, paire, décroît puis croît, minimum 0."),
            T("x⁷: domain ℝ; odd; derivative 7x⁶ ≥ 0 so increasing on all of ℝ.", "x⁷: المجال ℝ؛ فردية؛ المشتقة 7x⁶ ≥ 0 إذن متزايدة على ℝ.", "x⁷ : ℝ, impaire, croissante."),
            T("x⁻⁵: domain ℝ \\ {0}; odd; derivative −5x⁻⁶ < 0 so decreasing on (−∞, 0) and on (0, +∞).", "x⁻⁵: المجال ℝ \\ {0}؛ فردية؛ المشتقة −5x⁻⁶ < 0 إذن متناقصة على (−∞, 0) وعلى (0, +∞).", "x⁻⁵ : ℝ*, impaire, décroissante sur chaque intervalle."),
            F("x⁶: even, min at 0      x⁷: odd, increasing      x⁻⁵: odd, decreasing on each branch")]),
        EX("2", "", st("Compare 1.2³ᐟ² and 1.2² without a calculator.", "قارن بين 1.2^(3/2) و1.2² دون آلة حاسبة.", "Compare 1,2^(3/2) et 1,2² sans calculatrice."), [
            T("Both are powers of the same base 1.2 > 1. For a base greater than 1, the larger exponent gives the larger value.", "كلاهما قوة للأساس نفسه 1.2 > 1. وعندما يكون الأساس أكبر من 1 يعطي الأس الأكبر قيمة أكبر.", "Même base 1,2 > 1 : l'exposant le plus grand donne la plus grande valeur."),
            T("Since 3/2 = 1.5 < 2, we get 1.2^1.5 < 1.2². Numerically: 1.2^1.5 ≈ 1.315 and 1.2² = 1.44.", "بما أن 3/2 = 1.5 < 2 فإن 1.2^1.5 < 1.2². عدديًا: 1.2^1.5 ≈ 1.315 و1.2² = 1.44.", "1,5 < 2 donc 1,2^1,5 < 1,2² (≈ 1,315 < 1,44)."),
            F("1.2^(3/2) < 1.2²")]),
        EX("3", "", st("Differentiate f(x) = x^(5/2) and g(x) = 4x^(−1/2), x > 0.", "اشتق f(x) = x^(5/2) وg(x) = 4x^(−1/2) حيث x > 0.", "Dérive f(x) = x^(5/2) et g(x) = 4x^(−1/2)."), [
            T("Use (x^a)′ = a·x^(a−1). For f: a = 5/2, so f′(x) = (5/2)x^(3/2).", "نستعمل (x^a)′ = a·x^(a−1). لـ f: a = 5/2 فيكون f′(x) = (5/2)x^(3/2).", "(x^a)′ = a x^(a−1) : f′ = (5/2) x^(3/2)."),
            T("For g: a = −1/2, so g′(x) = 4 × (−1/2)x^(−3/2) = −2x^(−3/2) = −2/(x√x).", "لـ g: a = −1/2 فيكون g′(x) = 4 × (−1/2)x^(−3/2) = −2x^(−3/2) = −2/(x√x).", "g′ = 4(−1/2)x^(−3/2) = −2/(x√x)."),
            F("f′(x) = (5/2)x^(3/2)      g′(x) = −2x^(−3/2)"), F("Check at x = 4: f′(4) = (5/2)·8 = 20 ; g′(4) = −2/8 = −1/4")]),
        EX("4", "", st("Solve x^(3/2) = 8 and x^(−2) = 1/9 for x > 0.", "حلّ x^(3/2) = 8 وx^(−2) = 1/9 حيث x > 0.", "Résous x^(3/2) = 8 et x^(−2) = 1/9."), [
            T("Raise both sides to the power 2/3: x = 8^(2/3) = (∛8)² = 2² = 4. Check: 4^(3/2) = (√4)³ = 8 ✓.", "نرفع الطرفين إلى القوة 2/3: x = 8^(2/3) = (∛8)² = 2² = 4. تحقق: 4^(3/2) = (√4)³ = 8 ✓.", "x = 8^(2/3) = 4 ; 4^(3/2) = 8 ✓."),
            T("x^(−2) = 1/9 means 1/x² = 1/9, so x² = 9 and, with x > 0, x = 3.", "x^(−2) = 1/9 تعني 1/x² = 1/9 إذن x² = 9 ومع x > 0 نجد x = 3.", "1/x² = 1/9 → x = 3."),
            F("x = 4      x = 3")]),
        EX("5", "", st("Study f(x) = x^(2/3) on ℝ: domain, parity, limits, variations, and sketch it.", "ادرس f(x) = x^(2/3) على ℝ: المجال والزوجية والنهايات والتغيرات ثم ارسمها.", "Étudie f(x) = x^(2/3) sur ℝ et trace-la."), [
            T("x^(2/3) = (∛x)², defined for all real x. It is even because (−x)^(2/3) = (∛(−x))² = (∛x)². Limit at ±∞ is +∞.", "x^(2/3) = (∛x)² معرّفة لكل x حقيقي. وهي زوجية لأن (−x)^(2/3) = (∛(−x))² = (∛x)². النهاية عند ±∞ هي +∞.", "(∛x)² : définie sur ℝ, paire, limite +∞ en ±∞."),
            T("For x > 0: f′(x) = (2/3)x^(−1/3) > 0, increasing. At 0 the derivative blows up: a cusp pointing down at the origin. Minimum f(0) = 0.", "من أجل x > 0: f′(x) = (2/3)x^(−1/3) > 0 فالدالة متزايدة. عند 0 تؤول المشتقة إلى اللانهاية: نقطة رجوع (ذروة) نحو الأسفل عند المبدأ. قيمة صغرى f(0) = 0.", "f′ = (2/3)x^(−1/3) > 0 sur ]0 ; +∞[ ; point de rebroussement en 0, minimum 0."),
            fn_graph(lambda x: abs(x) ** (2 / 3), (-8, 8), (-1, 5), pts={"O": (0, 0), "A": (1, 1), "B": (8, 4)}, tag="X5", label="f(x) = x^(2/3)"),
            F("f: +∞ ↘ 0 (at x = 0) ↗ +∞")]),
        EX("6", "", st("Find the equation of the tangent to f(x) = √x at x = 4 and at x = 9, and draw them.", "جد معادلة المماس لـ f(x) = √x عند x = 4 وعند x = 9 وارسمهما.", "Tangente à √x en x = 4 et x = 9."), [
            T("f′(x) = 1/(2√x). At 4: f(4) = 2 and f′(4) = 1/4. Tangent: y = 2 + (x − 4)/4 = x/4 + 1.", "f′(x) = 1/(2√x). عند 4: f(4) = 2 وf′(4) = 1/4. المماس: y = 2 + (x − 4)/4 = x/4 + 1.", "f′(4) = 1/4 : y = x/4 + 1."),
            T("At 9: f(9) = 3 and f′(9) = 1/6. Tangent: y = 3 + (x − 9)/6 = x/6 + 3/2.", "عند 9: f(9) = 3 وf′(9) = 1/6. المماس: y = 3 + (x − 9)/6 = x/6 + 3/2.", "f′(9) = 1/6 : y = x/6 + 3/2."),
            fn_graph(lambda x: math.sqrt(x), (0, 12), (0, 5), curves=[lambda x: x / 4 + 1, lambda x: x / 6 + 1.5], pts={"A": (4, 2), "B": (9, 3)}, tag="X6", label="√x and its tangents"),
            T("The curve is concave, so it lies below each tangent: for example √12 ≈ 3.46 while the tangent at 4 gives 12/4 + 1 = 4.", "المنحنى مقعّر لذلك يقع تحت كل مماس: مثلًا √12 ≈ 3.46 بينما المماس عند 4 يعطي 12/4 + 1 = 4.", "Concave : la courbe est sous ses tangentes."),
            F("T₄: y = x/4 + 1      T₉: y = x/6 + 3/2")]),
        EX("7", "", st("Real-life: the time of one swing of a pendulum is T = 2π√(L/9.8). How does T change when L is multiplied by 4? What power function is T of L?", "حياتي: زمن نوسة واحدة لنواس هو T = 2π√(L/9.8). كيف يتغير T عندما يُضرب L في 4؟ وأي دالة قوة هي T بدلالة L؟", "Un pendule : T = 2π√(L/9,8). Que devient T si L est multiplié par 4 ?"), [
            T("T = (2π/√9.8) · L^(1/2): a power function of L with exponent 1/2.", "T = (2π/√9.8) · L^(1/2): دالة قوة في L أسها 1/2.", "T est proportionnelle à L^(1/2)."),
            T("Replace L by 4L: T′ = c·(4L)^(1/2) = c·2·L^(1/2) = 2T. Multiplying the length by 4 only doubles the time of a swing.", "نبدّل L بـ 4L: T′ = c·(4L)^(1/2) = c·2·L^(1/2) = 2T. ضرب الطول في 4 يضاعف زمن النوسة فقط.", "T′ = c(4L)^(1/2) = 2T : le temps double."),
            F("T(4L) = 2·T(L)")]),
        EX("8", "", st("Error detective: a student says that x^(1/2) is defined for negative x because (−4)^(1/2) = −2. Find the mistake.", "المحقق: يقول طالب إن x^(1/2) معرّفة عند x سالب لأن (−4)^(1/2) = −2. جد الخطأ.", "Détective : « (−4)^(1/2) = −2 ». Où est l'erreur ?"), [
            T("x^(1/2) means √x, the non-negative number whose square is x. No real number squared gives −4, so (−4)^(1/2) does not exist in ℝ.", "x^(1/2) تعني √x أي العدد غير السالب الذي مربعه x. ولا يوجد عدد حقيقي مربعه −4 إذن (−4)^(1/2) غير موجود في ℝ.", "x^(1/2) = √x n'existe pas pour x < 0."),
            T("The student confused it with the cube root: ∛(−8) = −2 does exist. The real power function xᵃ with non-integer a is defined only for x > 0 (or x ≥ 0).", "خلط الطالب بينها وبين الجذر التكعيبي: ∛(−8) = −2 موجود فعلًا. دالة القوة xᵃ لأس غير صحيح تُعرَّف فقط عند x > 0 (أو x ≥ 0).", "Il confond avec ∛(−8) = −2. Pour a non entier, xᵃ n'est définie que pour x > 0."),
            F("Domain of x^(1/2): [0, +∞)")]),
    ]
