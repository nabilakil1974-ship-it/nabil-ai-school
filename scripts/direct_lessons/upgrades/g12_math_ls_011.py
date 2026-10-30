"""Upgrade: Integrals — Riemann rectangles, signed area, many worked exercises."""
import math
from scripts.direct_lessons.common import T, F, EX, st, scene
from scripts.direct_lessons.graphs import fn_graph, section

W, H, M = 660, 440, 40


def rects(n, f=lambda x: x * x, a=0.0, b=2.0, ymax=4.4, tag="R", left=True):
    """Riemann rectangles under f on [a,b] (bars), with the curve."""
    X = lambda v: M + (v - 0) / 2.4 * (W - 2 * M)
    Y = lambda v: H - M - v / ymax * (H - 2 * M)
    s = f'<g id="{tag}a"><line x1="{X(0)}" y1="{Y(0)}" x2="{X(2.4)}" y2="{Y(0)}" stroke="#0b3d5c" stroke-width="4"/><line x1="{X(0)}" y1="{Y(0)}" x2="{X(0)}" y2="{Y(ymax)}" stroke="#0b3d5c" stroke-width="4"/>'
    for i in range(0, 3):
        s += f'<text x="{X(i)}" y="{Y(0)+22}" font-size="16" text-anchor="middle" fill="#0b3d5c" font-family="sans-serif">{i}</text>'
    s += '</g>'
    ids = [tag + "a"]
    dx = (b - a) / n
    bars = ""
    area = 0
    for k in range(n):
        xl = a + k * dx
        h = f(xl) if left else f(xl + dx)
        area += h * dx
        bars += f'<rect x="{X(xl):.1f}" y="{Y(h):.1f}" width="{X(xl+dx)-X(xl):.1f}" height="{Y(0)-Y(h):.1f}" fill="#90caf9" fill-opacity=".7" stroke="#1565c0" stroke-width="2"/>'
    s += f'<g id="{tag}b">{bars}</g>'; ids.append(tag + "b")
    pts = " L".join(f"{X(a+(b-a)*k/200):.1f},{Y(f(a+(b-a)*k/200)):.1f}" for k in range(201))
    s += f'<g id="{tag}c"><path d="M{pts}" fill="none" stroke="#e53935" stroke-width="5"/><text x="{X(2.3)}" y="{Y(4.2)}" font-size="20" font-weight="700" fill="#e53935" font-family="sans-serif">y = x²   sum = {area:.3f}</text></g>'
    ids.append(tag + "c")
    return scene(s, ids)


def upgrade(m):
    s = section(m, "Accumulation: Riemann rectangles")
    s.append(rects(4, tag="R4"))
    s.append(T("The curve is y = x² on [0, 2]. We cut the interval into 4 strips and build a rectangle on each, using the left end for the height: heights 0, 0.25, 1, 2.25. The sum of the rectangle areas is 0.5 × (0 + 0.25 + 1 + 2.25) = 1.75, less than the true area.",
               "المنحنى y = x² على [0, 2]. نقسم المجال إلى 4 شرائح ونبني على كل منها مستطيلًا ارتفاعه عند طرفه الأيسر: الارتفاعات 0 و0.25 و1 و2.25. مجموع مساحات المستطيلات 0.5 × (0 + 0.25 + 1 + 2.25) = 1.75 وهو أقل من المساحة الحقيقية.",
               "y = x² sur [0 ; 2], 4 bandes, hauteurs au bord gauche : 0 ; 0,25 ; 1 ; 2,25. Somme : 0,5 × 3,5 = 1,75, inférieure à l'aire réelle."))
    s.append(rects(16, tag="R16"))
    s.append(T("With 16 strips the staircase hugs the curve much better, and the sum becomes 2.421875. With more strips it keeps getting closer to 8/3 ≈ 2.667. That limit is the integral ∫₀² x² dx. Thin rectangles added up: this is the whole idea of the integral.",
               "مع 16 شريحة يلتصق الدرج بالمنحنى أكثر ويصبح المجموع 2.421875. وكلما زاد عدد الشرائح اقترب من 8/3 ≈ 2.667. هذه النهاية هي التكامل ∫₀² x² dx. مستطيلات رفيعة تُجمع: هذه هي فكرة التكامل كلها.",
               "Avec 16 bandes, l'escalier colle mieux : somme 2,46875. En augmentant, elle tend vers 8/3 ≈ 2,667 : c'est ∫₀² x² dx."))
    s.append(F("∫₀² x² dx = [x³/3]₀² = 8/3 ≈ 2.667"))

    s = section(m, "Signed area")
    s.append(fn_graph(lambda x: x, (-3, 4), (-3, 4), pts={"A": (-2, -2), "B": (3, 3)}, vlines=[-2, 3], tag="S1", label="y = x on [−2, 3]"))
    s.append(T("The line y = x between x = −2 and x = 3. Left of the origin the triangle lies below the axis: its signed value is −2. Right of the origin the triangle lies above: its value is +4.5. The integral adds them: −2 + 4.5 = 2.5. But the geometric area is 2 + 4.5 = 6.5, because area is never negative.",
               "المستقيم y = x بين x = −2 وx = 3. يسار المبدأ يقع المثلث تحت المحور وقيمته الجبرية −2. يمين المبدأ يقع فوق المحور وقيمته +4.5. التكامل يجمعهما: −2 + 4.5 = 2.5. أما المساحة الهندسية فهي 2 + 4.5 = 6.5 لأن المساحة لا تكون سالبة.",
               "La droite y = x entre −2 et 3 : le triangle de gauche vaut −2, celui de droite +4,5. L'intégrale : 2,5. L'aire géométrique : 2 + 4,5 = 6,5."))
    s.append(F("∫₋₂³ x dx = (9 − 4)/2 = 2.5      Area = 2 + 4.5 = 6.5"))

    s = section(m, "The fundamental connection")
    s.append(fn_graph(lambda x: 3 * x * x, (0, 3), (0, 28), pts={"A": (1, 3), "B": (2, 12)}, vlines=[1, 2], tag="F1", label="f(x) = 3x²"))
    s.append(T("For f(x) = 3x² a primitive is F(x) = x³. The area under f between 1 and 2 is F(2) − F(1) = 8 − 1 = 7. You do not need to add any rectangles: the primitive does the whole job in one subtraction.",
               "من أجل f(x) = 3x² أصلية هي F(x) = x³. المساحة تحت f بين 1 و2 تساوي F(2) − F(1) = 8 − 1 = 7. لا نحتاج إلى جمع أي مستطيلات: الأصلية تنجز العمل كله بطرح واحد.",
               "Pour f = 3x², F = x³. Aire entre 1 et 2 : F(2) − F(1) = 8 − 1 = 7."))

    m.EXERCISES[:] = [
        EX("1", "", st("Find primitives of 4x³, 6x and 5.", "جد أصليات 4x³ و6x و5.", "Primitives de 4x³, 6x et 5."), [
            T("Raise the power by 1 and divide by the new power. 4x³ → 4·x⁴/4 = x⁴.", "نزيد الأس 1 ونقسم على الأس الجديد. 4x³ → 4·x⁴/4 = x⁴.", "On augmente l'exposant de 1 et on divise : x⁴."),
            T("6x → 6·x²/2 = 3x². A constant 5 → 5x.", "6x → 6·x²/2 = 3x². والثابت 5 → 5x.", "6x → 3x² ; 5 → 5x."),
            F("x⁴ + C      3x² + C      5x + C"), F("Check by differentiating: (x⁴)′ = 4x³ ✓  (3x²)′ = 6x ✓  (5x)′ = 5 ✓")]),
        EX("2", "", st("Find ∫(3x² + 2x − 4) dx.", "جد ∫(3x² + 2x − 4) dx.", "Calcule ∫(3x² + 2x − 4) dx."), [
            T("Integrate term by term: 3x² → x³, 2x → x², −4 → −4x.", "نكامل حدًّا حدًّا: 3x² → x³ وَ2x → x² وَ−4 → −4x.", "Terme à terme : x³, x², −4x."),
            F("x³ + x² − 4x + C"), F("Check: (x³ + x² − 4x)′ = 3x² + 2x − 4 ✓")]),
        EX("3", "", st("F′(x) = 3x² + 1 and F(0) = 4. Find F and then F(2).", "F′(x) = 3x² + 1 وF(0) = 4. جد F ثم F(2).", "F′(x) = 3x² + 1, F(0) = 4 : trouve F puis F(2)."), [
            T("All primitives are x³ + x + C. The condition F(0) = 4 picks one: 0 + 0 + C = 4, so C = 4.", "كل الأصليات هي x³ + x + C. والشرط F(0) = 4 يختار واحدة: 0 + 0 + C = 4 إذن C = 4.", "F = x³ + x + C ; F(0) = 4 → C = 4."),
            F("F(x) = x³ + x + 4"), F("F(2) = 8 + 2 + 4 = 14")]),
        EX("4", "", st("Evaluate ∫₀¹ (4x³ + 2x) dx.", "احسب ∫₀¹ (4x³ + 2x) dx.", "Calcule ∫₀¹ (4x³ + 2x) dx."), [
            T("A primitive is F(x) = x⁴ + x². Then the integral is F(1) − F(0).", "أصلية هي F(x) = x⁴ + x². فالتكامل يساوي F(1) − F(0).", "F = x⁴ + x² ; I = F(1) − F(0)."),
            F("(1 + 1) − (0 + 0) = 2")]),
        EX("5", "", st("Find the geometric area bounded by y = x, the x-axis, x = −2 and x = 3.", "جد المساحة الهندسية المحصورة بين y = x ومحور الفواصل وx = −2 وx = 3.", "Aire entre y = x, l'axe des abscisses, x = −2 et x = 3."), [
            T("The line changes sign at 0. Split: on [−2, 0] the curve is below the axis; on [0, 3] above. Area = |∫₋₂⁰ x dx| + ∫₀³ x dx.", "المستقيم يغيّر إشارته عند 0. نجزّئ: على [−2, 0] المنحنى تحت المحور وعلى [0, 3] فوقه. المساحة = |∫₋₂⁰ x dx| + ∫₀³ x dx.", "Signe change en 0 : aire = |∫₋₂⁰| + ∫₀³."),
            F("∫₋₂⁰ x dx = −2      ∫₀³ x dx = 4.5"), F("Area = 2 + 4.5 = 6.5")]),
        EX("6", "", st("Compute ∫₀² x² dx using the primitive, and compare with the sum of 4 rectangles (1.75).", "احسب ∫₀² x² dx بالأصلية وقارنها بمجموع 4 مستطيلات (1.75).", "Calcule ∫₀² x² dx et compare avec 1,75."), [
            T("A primitive of x² is x³/3. So the integral is 2³/3 − 0 = 8/3 ≈ 2.667.", "أصلية x² هي x³/3. إذن التكامل 2³/3 − 0 = 8/3 ≈ 2.667.", "x³/3 : 8/3 ≈ 2,667."),
            T("The 4 left rectangles gave 1.75, an underestimate by 2.667 − 1.75 ≈ 0.917. The error shrinks as the strips get thinner.", "المستطيلات الأربعة اليسرى أعطت 1.75 أي أقل من الحقيقة بنحو 0.917. والخطأ يتناقص كلما صارت الشرائح أرفع.", "L'écart est ≈ 0,917, il diminue quand les bandes sont plus fines."),
            F("∫₀² x² dx = 8/3")]),
        EX("7", "", st("A car has speed v(t) = 6t m/s from t = 0 to t = 5 s. Find the distance travelled.", "سرعة سيارة v(t) = 6t م/ث من t = 0 إلى t = 5 ثوانٍ. جد المسافة المقطوعة.", "Une voiture a la vitesse v(t) = 6t pendant 5 s. Quelle distance ?"), [
            T("Distance is the area under the speed curve, so d = ∫₀⁵ 6t dt.", "المسافة هي المساحة تحت منحنى السرعة إذن d = ∫₀⁵ 6t dt.", "d = ∫₀⁵ 6t dt."),
            F("d = [3t²]₀⁵ = 3 × 25 = 75 m"), T("Check with a triangle: base 5, height v(5) = 30, area = (5 × 30)/2 = 75 ✓.", "تحقق بمثلث: القاعدة 5 والارتفاع v(5) = 30 والمساحة (5 × 30)/2 = 75 ✓.", "Triangle : (5 × 30)/2 = 75 ✓.")]),
        EX("8", "", st("Error detective: a student writes ∫₋₁¹ x dx = 2 as an area. What is wrong?", "المحقق: كتب طالب ∫₋₁¹ x dx = 2 على أنها مساحة. ما الخطأ؟", "Détective : ∫₋₁¹ x dx = 2 ?"), [
            T("A primitive is x²/2, so ∫₋₁¹ x dx = 1/2 − 1/2 = 0, not 2. The two triangles cancel because one is below the axis.", "الأصلية x²/2 إذن ∫₋₁¹ x dx = 1/2 − 1/2 = 0 لا 2. المثلثان يلغي أحدهما الآخر لأن أحدهما تحت المحور.", "= 1/2 − 1/2 = 0 : les deux triangles s'annulent."),
            T("The geometric area is 1/2 + 1/2 = 1: integral and area are different questions when the curve crosses the axis.", "المساحة الهندسية 1/2 + 1/2 = 1: التكامل والمساحة سؤالان مختلفان عندما يعبر المنحنى المحور.", "L'aire vaut 1 : intégrale ≠ aire quand la courbe traverse l'axe."),
            F("∫₋₁¹ x dx = 0      Area = 1")]),
    ]
