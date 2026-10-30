from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import fn_graph, section, add_ex, add_sec


def upgrade(m):
    s = section(m, "Common factor")
    s.append(fn_graph(lambda x: 6 * x ** 3 + 9 * x ** 2, (-3, 1.5), (-10, 25), pts={"A": (-1.5, 0), "O": (0, 0)}, tag="Z1", label="6x³ + 9x² = 3x²(2x + 3)"))
    s.append(T("Factoring 3x²(2x + 3) shows the zeros: x = 0 (from x², a double zero) and x = −3/2. On the graph the curve touches the axis at the origin without crossing it, which is typical of a double zero, and crosses at −1.5.",
               "التحليل 3x²(2x + 3) يظهر الأصفار: x = 0 (من x² أي صفر مضاعف) وx = −3/2. في الرسم يلمس المنحنى المحور عند المبدأ دون أن يعبره وهذا نموذجي للصفر المضاعف، ويعبره عند −1.5.",
               "3x²(2x + 3) : zéros x = 0 (double, la courbe touche l'axe) et x = −3/2 (elle le traverse)."))
    s = section(m, "Strategy and challenge")
    s.append(fn_graph(lambda x: x * x + x - 6, (-5, 4), (-8, 12), pts={"A": (-3, 0), "B": (2, 0), "V": (-0.5, -6.25)}, tag="Z2", label="x² + x − 6 = (x + 3)(x − 2)"))
    s.append(T("Factoring x² + x − 6 = (x + 3)(x − 2) gives the zeros −3 and 2: the parabola crosses the x-axis exactly there. Between the zeros the polynomial is negative, outside it is positive. The vertex is at x = −1/2, halfway between the zeros.",
               "تحليل x² + x − 6 = (x + 3)(x − 2) يعطي الصفرين −3 و2: يقطع القطع المكافئ محور الفواصل هناك تمامًا. بين الصفرين تكون الكثيرة سالبة وخارجهما موجبة. والرأس عند x = −1/2 في منتصف الصفرين.",
               "(x + 3)(x − 2) : zéros −3 et 2 ; négatif entre les zéros, positif à l'extérieur ; sommet en x = −1/2."))
    add_ex(m, [
        EX("", "", st("Expand (x + 3)(x − 5) and (2x − 1)².", "انشر (x + 3)(x − 5) وَ(2x − 1)².", "Développe (x + 3)(x − 5) et (2x − 1)²."), [
            T("(x + 3)(x − 5) = x² − 5x + 3x − 15 = x² − 2x − 15.", "(x + 3)(x − 5) = x² − 5x + 3x − 15 = x² − 2x − 15.", "= x² − 2x − 15."), T("(2x − 1)² = 4x² − 4x + 1 (square of a difference: a² − 2ab + b²).", "(2x − 1)² = 4x² − 4x + 1 (مربع فرق: a² − 2ab + b²).", "= 4x² − 4x + 1."), F("x² − 2x − 15      4x² − 4x + 1"), F("Check at x = 1: (4)(−4) = −16 = 1 − 2 − 15 ✓")]),
        EX("", "", st("Factor x² − 49 and 4x² − 25, then solve x² − 49 = 0.", "حلّل x² − 49 وَ4x² − 25 ثم حلّ x² − 49 = 0.", "Factorise x² − 49 et 4x² − 25 ; résous x² − 49 = 0."), [
            T("Difference of squares: a² − b² = (a − b)(a + b). So x² − 49 = (x − 7)(x + 7) and 4x² − 25 = (2x − 5)(2x + 5).", "فرق مربعين: a² − b² = (a − b)(a + b). إذن x² − 49 = (x − 7)(x + 7) وَ4x² − 25 = (2x − 5)(2x + 5).", "a² − b² = (a − b)(a + b)."), T("Zero product rule: (x − 7)(x + 7) = 0 gives x = 7 or x = −7.", "قاعدة الجداء المعدوم: (x − 7)(x + 7) = 0 تعطي x = 7 أو x = −7.", "x = 7 ou x = −7."), F("x = ±7")]),
        EX("", "", st("Factor x² − 5x + 6 and solve x² − 5x + 6 = 0.", "حلّل x² − 5x + 6 وحلّ x² − 5x + 6 = 0.", "Factorise x² − 5x + 6 et résous."), [
            T("We need two numbers with product 6 and sum −5: −2 and −3. So x² − 5x + 6 = (x − 2)(x − 3).", "نبحث عن عددين جداؤهما 6 ومجموعهما −5: إنهما −2 و−3. إذن x² − 5x + 6 = (x − 2)(x − 3).", "Produit 6, somme −5 : −2 et −3."), F("x = 2 or x = 3"), F("Check: 4 − 10 + 6 = 0 ✓   9 − 15 + 6 = 0 ✓")]),
        EX("", "", st("A rectangular garden has length x + 4 and width x. Its area is 96. Find x.", "حديقة مستطيلة طولها x + 4 وعرضها x ومساحتها 96. جد x.", "Jardin rectangulaire de longueur x + 4, largeur x, aire 96. Trouve x."), [
            T("x(x + 4) = 96, so x² + 4x − 96 = 0. Two numbers with product −96 and sum 4: 12 and −8. So (x + 12)(x − 8) = 0.", "x(x + 4) = 96 إذن x² + 4x − 96 = 0. عددان جداؤهما −96 ومجموعهما 4: 12 و−8. إذن (x + 12)(x − 8) = 0.", "x² + 4x − 96 = (x + 12)(x − 8)."), T("x = −12 is impossible for a length, so x = 8. The garden is 8 by 12: area 96 ✓.", "x = −12 مستحيل لطول إذن x = 8. الحديقة 8 في 12 ومساحتها 96 ✓.", "x = 8 : jardin 8 × 12 = 96 ✓."), F("x = 8 m")]),
    ])
