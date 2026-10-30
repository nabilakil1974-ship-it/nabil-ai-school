"""Upgrade: Irrational functions — graphs for domain, endpoints, asymptotes and 8 worked exercises."""
import math
from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import fn_graph, section


def upgrade(m):
    s = section(m, "Where does the function exist?")
    s.append(fn_graph(lambda x: math.sqrt(5 - x), (-4, 6), (-1, 4), pts={"A": (5, 0), "B": (1, 2), "C": (-4, 3)}, tag="I1", label="f(x) = √(5 − x)"))
    s.append(T("The curve stops at x = 5, where 5 − x = 0. To the right of 5 the radicand is negative and there is simply no graph. This is the picture of the rule: the domain is {x : 5 − x ≥ 0} = (−∞, 5]. The curve starts at the endpoint A(5, 0) and goes up as x decreases.",
               "ينتهي المنحنى عند x = 5 حيث 5 − x = 0. يمين 5 يكون ما تحت الجذر سالبًا فلا يوجد رسم أصلًا. هذه صورة القاعدة: المجال {x : 5 − x ≥ 0} = (−∞, 5]. يبدأ المنحنى من الطرف A(5, 0) ويصعد كلما نقص x.",
               "La courbe s'arrête en x = 5 : au-delà, 5 − x < 0, il n'y a pas de graphe. Domaine : ]−∞ ; 5]. Elle part de A(5 ; 0) et monte quand x diminue."))
    s = section(m, "Domain with two branches")
    s.append(fn_graph(lambda x: math.sqrt(x * x - 9), (-8, 8), (-1, 6), pts={"A": (3, 0), "B": (-3, 0), "C": (5, 4)}, vlines=[], tag="I2", label="f(x) = √(x² − 9)"))
    s.append(T("Two separate branches: one starts at B(−3, 0) and goes left, the other starts at A(3, 0) and goes right. Between −3 and 3 there is a gap, because x² − 9 < 0 there. The domain is (−∞, −3] ∪ [3, +∞). At C(5, 4): √(25 − 9) = 4.",
               "فرعان منفصلان: الأول يبدأ من B(−3, 0) ويتجه يسارًا والثاني يبدأ من A(3, 0) ويتجه يمينًا. بين −3 و3 فجوة لأن x² − 9 < 0 هناك. المجال (−∞, −3] ∪ [3, +∞). عند C(5, 4): √(25 − 9) = 4.",
               "Deux branches séparées, un vide entre −3 et 3 car x² − 9 < 0. Domaine ]−∞ ; −3] ∪ [3 ; +∞[. C : √(25 − 9) = 4."))
    s = section(m, "Endpoint example")
    s.append(fn_graph(lambda x: math.sqrt(x - 2), (2, 11), (-1, 4), pts={"A": (2, 0), "B": (3, 1), "C": (6, 2), "D": (11, 3)}, tag="I3", label="f(x) = √(x − 2)"))
    s.append(T("Notice the endpoint A(2, 0): the tangent there is vertical, because the slope 1/(2√(x − 2)) grows without bound near 2. Then the curve rises more and more slowly: (3, 1), (6, 2), (11, 3). It is increasing and concave.",
               "لاحظ الطرف A(2, 0): المماس هناك شاقولي لأن الميل 1/(2√(x − 2)) يكبر بلا حد قرب 2. ثم يرتفع المنحنى ببطء متزايد: (3, 1) و(6, 2) و(11, 3). الدالة متزايدة ومقعّرة.",
               "En A(2 ; 0) la tangente est verticale (pente 1/(2√(x − 2)) → +∞). Puis la courbe monte de plus en plus lentement. Croissante et concave."))
    s = section(m, "Asymptote test with a conjugate")
    s.append(fn_graph(lambda x: math.sqrt(x * x + 4), (-6, 6), (-1, 7), curves=[lambda x: abs(x)], pts={"V": (0, 2)}, tag="I4", label="√(x² + 4) (red) and |x| (dashed)"))
    s.append(T("The red curve √(x² + 4) has its minimum at V(0, 2). Far to the right it hugs the dashed line y = x, far to the left the line y = −x. The gap shrinks: √(x² + 4) − x = 4/(√(x² + 4) + x) → 0. So y = x is an oblique asymptote at +∞ and y = −x at −∞.",
               "المنحنى الأحمر √(x² + 4) له قيمة صغرى عند V(0, 2). بعيدًا يمينًا يلتصق بالمستقيم المتقطع y = x وبعيدًا يسارًا بالمستقيم y = −x. الفجوة تتلاشى: √(x² + 4) − x = 4/(√(x² + 4) + x) → 0. إذن y = x مقارب مائل عند +∞ وy = −x عند −∞.",
               "Minimum en V(0 ; 2). À l'infini, la courbe colle aux droites y = x et y = −x : la différence tend vers 0 (expression conjuguée)."))
    s = section(m, "Asymptote vs direction")
    s.append(fn_graph(lambda x: math.sqrt(x), (0, 25), (-1, 8), curves=[lambda x: x / 4 + 1], pts={"A": (4, 2)}, tag="I5", label="√x: a parabolic direction"))
    s.append(T("√x goes to +∞ and the ratio √x/x → 0: the curve has a direction (parabolic branch along the x-axis) but NO oblique asymptote. The dashed line is just a tangent at (4, 2). Tending to infinity is not the same as having an asymptote: you need f(x) − (ax + b) → 0.",
               "√x تؤول إلى +∞ والنسبة √x/x → 0: للمنحنى اتجاه (فرع مكافئ باتجاه محور الفواصل) لكن لا مقارب مائل. المستقيم المتقطع مجرد مماس عند (4, 2). الذهاب إلى اللانهاية لا يعني وجود مقارب: نحتاج f(x) − (ax + b) → 0.",
               "√x → +∞ mais √x/x → 0 : branche parabolique, pas d'asymptote oblique. Il faut f(x) − (ax + b) → 0."))

    m.EXERCISES[:] = [
        EX("1", "", st("Find the domain of √(5 − x), 1/√(x − 2) and √(x² − 9).", "جد مجال √(5 − x) و1/√(x − 2) و√(x² − 9).", "Domaine de √(5 − x), 1/√(x − 2), √(x² − 9)."), [
            T("√(5 − x): need 5 − x ≥ 0, so x ≤ 5: (−∞, 5].", "√(5 − x): نشترط 5 − x ≥ 0 إذن x ≤ 5: (−∞, 5].", "x ≤ 5."),
            T("1/√(x − 2): the radicand must be strictly positive because it is in a denominator: x > 2: (2, +∞).", "1/√(x − 2): ما تحت الجذر موجب تمامًا لأنه في المقام: x > 2: (2, +∞).", "Dénominateur : x > 2."),
            T("√(x² − 9): x² ≥ 9, so x ≤ −3 or x ≥ 3: (−∞, −3] ∪ [3, +∞).", "√(x² − 9): x² ≥ 9 إذن x ≤ −3 أو x ≥ 3: (−∞, −3] ∪ [3, +∞).", "x² ≥ 9 : ]−∞ ; −3] ∪ [3 ; +∞[."),
            F("(−∞, 5]      (2, +∞)      (−∞, −3] ∪ [3, +∞)")]),
        EX("2", "", st("Study the variations of g(x) = √(x² + 4).", "ادرس تغيرات g(x) = √(x² + 4).", "Étudie les variations de g(x) = √(x² + 4)."), [
            T("x² + 4 > 0 always, so the domain is ℝ. g is even because g(−x) = g(x).", "x² + 4 > 0 دائمًا فالمجال ℝ. وg زوجية لأن g(−x) = g(x).", "Domaine ℝ, paire."),
            T("g′(x) = x/√(x² + 4): negative for x < 0, zero at 0, positive for x > 0. So g decreases to the minimum g(0) = 2, then increases.", "g′(x) = x/√(x² + 4): سالبة عند x < 0 ومعدومة عند 0 وموجبة عند x > 0. فتتناقص g حتى القيمة الصغرى g(0) = 2 ثم تتزايد.", "g′ = x/√(x² + 4) : min g(0) = 2."),
            F("g: +∞ ↘ 2 ↗ +∞")]),
        EX("3", "", st("Show √(x² + 4) − x → 0 as x → +∞.", "بيّن أن √(x² + 4) − x → 0 عندما x → +∞.", "Montre √(x² + 4) − x → 0 en +∞."), [
            T("Multiply and divide by the conjugate √(x² + 4) + x: the numerator becomes (x² + 4) − x² = 4.", "نضرب ونقسم على المرافق √(x² + 4) + x: يصبح البسط (x² + 4) − x² = 4.", "Conjugué : numérateur = 4."),
            F("√(x² + 4) − x = 4/(√(x² + 4) + x) → 0"), T("The denominator tends to +∞, so the quotient tends to 0. Hence y = x is an oblique asymptote.", "المقام يؤول إلى +∞ فيؤول الكسر إلى 0. إذن y = x مقارب مائل.", "Donc y = x est asymptote oblique.")]),
        EX("4", "", st("Error detective: '√(x²) = x for all x'. Find the mistake and give the right statement.", "المحقق: «√(x²) = x لكل x». جد الخطأ واكتب العبارة الصحيحة.", "Détective : « √(x²) = x pour tout x »."), [
            T("Take x = −3: √((−3)²) = √9 = 3, but x = −3. A square root is never negative.", "نأخذ x = −3: √((−3)²) = √9 = 3 بينما x = −3. الجذر التربيعي لا يكون سالبًا.", "x = −3 : √9 = 3 ≠ −3."),
            F("√(x²) = |x|"), T("The picture: the graph of √(x²) is the V-shape of |x|, not the line y = x.", "الصورة: منحنى √(x²) هو شكل V للقيمة المطلقة وليس المستقيم y = x.", "Le graphe est celui de |x|.")]),
        EX("5", "", st("Find the oblique asymptote of √(x² + αx + β) at +∞ (α, β constants).", "جد المقارب المائل لـ √(x² + αx + β) عند +∞ (α وβ ثابتان).", "Asymptote oblique de √(x² + αx + β) en +∞."), [
            T("Write x² + αx + β = (x + α/2)² + (β − α²/4). For large x the square root is close to x + α/2.", "نكتب x² + αx + β = (x + α/2)² + (β − α²/4). من أجل x كبيرة يكون الجذر قريبًا من x + α/2.", "(x + α/2)² + (β − α²/4)."),
            T("Check with the conjugate: √(x² + αx + β) − (x + α/2) = (β − α²/4)/(√(…) + x + α/2) → 0.", "نتحقق بالمرافق: √(x² + αx + β) − (x + α/2) = (β − α²/4)/(√(…) + x + α/2) → 0.", "Le conjugué donne une limite nulle."),
            F("asymptote: y = x + α/2"), T("Example α = 4, β = 1: y = x + 2.", "مثال α = 4 وβ = 1: y = x + 2.", "Exemple : y = x + 2.")]),
        EX("6", "", st("Solve the equation √(x + 6) = x.", "حلّ المعادلة √(x + 6) = x.", "Résous √(x + 6) = x."), [
            T("Conditions: x + 6 ≥ 0 and x ≥ 0 (a root is never negative). Square both sides: x + 6 = x², so x² − x − 6 = 0, (x − 3)(x + 2) = 0.", "الشروط: x + 6 ≥ 0 وx ≥ 0 (الجذر غير سالب). نربّع الطرفين: x + 6 = x² إذن x² − x − 6 = 0 أي (x − 3)(x + 2) = 0.", "x ≥ 0 ; x² − x − 6 = 0."),
            T("The candidates are 3 and −2. We keep only x = 3, since x ≥ 0. Check: √9 = 3 ✓. Rejecting −2 matters: √4 = 2 ≠ −2.", "المرشحان 3 و−2. نبقي x = 3 فقط لأن x ≥ 0. تحقق: √9 = 3 ✓. ورفض −2 مهم: √4 = 2 ≠ −2.", "Solution : x = 3 ; −2 est extraneous."),
            F("S = {3}")]),
        EX("7", "", st("Solve the inequality √(x − 1) < 2.", "حلّ المتراجحة √(x − 1) < 2.", "Résous √(x − 1) < 2."), [
            T("Domain: x ≥ 1. Both sides are non-negative, so squaring keeps the direction: x − 1 < 4, x < 5.", "المجال: x ≥ 1. الطرفان غير سالبين فالتربيع يحفظ الاتجاه: x − 1 < 4 إذن x < 5.", "x ≥ 1 puis x − 1 < 4."),
            F("S = [1, 5)"), T("Check: x = 5 gives √4 = 2, not < 2, so 5 is excluded; x = 1 gives 0 < 2 ✓.", "تحقق: x = 5 تعطي √4 = 2 وليس < 2 فتُستبعد؛ وx = 1 تعطي 0 < 2 ✓.", "x = 5 exclu, x = 1 ok.")]),
        EX("8", "", st("A rectangle has area 100. Express its diagonal d as a function of the width w and find the minimum diagonal.", "مستطيل مساحته 100. عبّر عن قطره d بدلالة العرض w وجد أصغر قطر.", "Rectangle d'aire 100 : diagonale d(w) et minimum."), [
            T("Length = 100/w, so d(w) = √(w² + 10000/w²) for w > 0.", "الطول = 100/w إذن d(w) = √(w² + 10000/w²) من أجل w > 0.", "d(w) = √(w² + 10000/w²)."),
            T("Minimise the radicand r(w) = w² + 10000/w². r′(w) = 2w − 20000/w³ = 0 gives w⁴ = 10000, w = 10. So the rectangle is a square 10 × 10.", "نصغّر ما تحت الجذر r(w) = w² + 10000/w². r′(w) = 2w − 20000/w³ = 0 تعطي w⁴ = 10000 وw = 10. إذن المستطيل مربع 10 × 10.", "w = 10 : carré 10 × 10."),
            F("d_min = √(100 + 100) = √200 = 10√2 ≈ 14.14")]),
    ]
