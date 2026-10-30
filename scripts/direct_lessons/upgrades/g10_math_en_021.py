from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import fn_graph, section, add_ex, add_sec


def upgrade(m):
    s = section(m, "Equation: all intersections")
    s.append(fn_graph(lambda x: x * x - 2 * x - 3, (-3, 6), (-5, 14), curves=[lambda x: x + 1], pts={"A": (-1, 0), "B": (4, 5)}, tag="U1", label="f(x) = x² − 2x − 3 (red), g(x) = x + 1 (dashed)"))
    s.append(T("Solving f(x) = g(x) means finding where the curves meet. On the board they meet at A(−1, 0) and B(4, 5), so the solutions are x = −1 and x = 4. Algebra confirms: x² − 2x − 3 = x + 1 becomes x² − 3x − 4 = (x − 4)(x + 1) = 0.",
               "حل f(x) = g(x) يعني إيجاد مكان التقاء المنحنيين. على اللوح يلتقيان في A(−1, 0) وB(4, 5) فالحلان x = −1 وx = 4. والجبر يؤكد: x² − 2x − 3 = x + 1 تصبح x² − 3x − 4 = (x − 4)(x + 1) = 0.",
               "f(x) = g(x) : les courbes se coupent en A(−1 ; 0) et B(4 ; 5), donc x = −1 ou x = 4. Algèbre : (x − 4)(x + 1) = 0."))
    s = section(m, "Inequality: intervals")
    s.append(fn_graph(lambda x: x * x - 2 * x - 3, (-3, 6), (-5, 14), curves=[lambda x: x + 1], vlines=[-1, 4], tag="U2", label="f(x) > g(x) where the red curve is ABOVE the dashed line"))
    s.append(T("For f(x) > g(x) we read where the red curve is above the dashed line: to the left of x = −1 and to the right of x = 4. Between −1 and 4 the red curve is below. So the solution is (−∞, −1) ∪ (4, +∞). The meeting points themselves are not included because the inequality is strict.",
               "لـ f(x) > g(x) نقرأ أين يكون المنحنى الأحمر فوق المستقيم المتقطع: يسار x = −1 ويمين x = 4. بين −1 و4 يكون المنحنى الأحمر تحته. فالحل (−∞, −1) ∪ (4, +∞). ولا تدخل نقطتا اللقاء لأن المتراجحة صارمة.",
               "f(x) > g(x) : la courbe rouge est au-dessus à gauche de −1 et à droite de 4. S = ]−∞ ; −1[ ∪ ]4 ; +∞[."))
    add_ex(m, [
        EX("", "", st("Using the graph, solve f(x) < g(x) and f(x) ≤ g(x).", "بالاعتماد على الرسم حلّ f(x) < g(x) وf(x) ≤ g(x).", "Avec le graphique, résous f(x) < g(x) et f(x) ≤ g(x)."), [
            T("f is below g between the meeting points: −1 < x < 4.", "f تحت g بين نقطتي اللقاء: −1 < x < 4.", "f sous g entre −1 et 4."), T("For ≤ we also include the meeting points: −1 ≤ x ≤ 4.", "من أجل ≤ ندخل نقطتي اللقاء أيضًا: −1 ≤ x ≤ 4.", "Avec ≤ on inclut −1 et 4."), F("(−1, 4)      [−1, 4]")]),
        EX("", "", st("Solve graphically x² = 4 and x² < 4 (draw y = x² and y = 4).", "حلّ بيانيًا x² = 4 وx² < 4 (ارسم y = x² وy = 4).", "Résous x² = 4 et x² < 4 graphiquement."), [
            fn_graph(lambda x: x * x, (-4, 4), (-1, 9), hlines=[4], vlines=[-2, 2], pts={"A": (-2, 4), "B": (2, 4)}, tag="X1", label="y = x² and y = 4"),
            T("The parabola meets y = 4 at x = −2 and x = 2. It is below the line between them.", "يلتقي القطع المكافئ بالمستقيم y = 4 عند x = −2 وx = 2 ويقع تحته بينهما.", "Rencontre en −2 et 2 ; en dessous entre les deux."), F("x² = 4: x = ±2      x² < 4: −2 < x < 2")]),
        EX("", "", st("Solve graphically |x| = 2 and |x| ≥ 2.", "حلّ بيانيًا |x| = 2 و|x| ≥ 2.", "Résous |x| = 2 et |x| ≥ 2."), [
            fn_graph(lambda x: abs(x), (-5, 5), (-1, 6), hlines=[2], vlines=[-2, 2], pts={"A": (-2, 2), "B": (2, 2)}, tag="X2", label="y = |x| and y = 2"),
            T("The V meets y = 2 at x = ±2. It is at or above y = 2 when x ≤ −2 or x ≥ 2.", "يلتقي شكل V بالمستقيم y = 2 عند x = ±2 ويكون عند y = 2 أو فوقه عندما x ≤ −2 أو x ≥ 2.", "V au-dessus de y = 2 si x ≤ −2 ou x ≥ 2."), F("|x| = 2: x = ±2      |x| ≥ 2: (−∞, −2] ∪ [2, +∞)")]),
        EX("", "", st("Check by substitution the two solutions of f(x) = g(x) found above.", "تحقق بالتعويض من حلّي المعادلة f(x) = g(x) أعلاه.", "Vérifie par substitution les deux solutions."), [
            T("x = −1: f(−1) = 1 + 2 − 3 = 0 and g(−1) = 0 ✓.", "x = −1: f(−1) = 1 + 2 − 3 = 0 وg(−1) = 0 ✓.", "x = −1 : 0 = 0 ✓."), T("x = 4: f(4) = 16 − 8 − 3 = 5 and g(4) = 5 ✓.", "x = 4: f(4) = 16 − 8 − 3 = 5 وg(4) = 5 ✓.", "x = 4 : 5 = 5 ✓."), F("both solutions verified")]),
    ])
