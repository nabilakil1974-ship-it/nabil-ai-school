"""Upgrade: Differential calculus — Rolle, MVT, monotonicity pictures and worked exercises."""
import math
from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import fn_graph, section


def upgrade(m):
    s = section(m, "Verify Rolle")
    f = lambda x: x * x - 6 * x + 8
    s.append(fn_graph(f, (0, 6), (-2, 9), pts={"A": (2, 0), "B": (4, 0), "C": (3, -1)}, curves=[lambda x: -1], tag="D1", label="f(x) = x² − 6x + 8"))
    s.append(T("The parabola cuts the x-axis at 2 and 4, so f(2) = f(4) = 0. It is continuous and differentiable everywhere. Rolle says there is a c between 2 and 4 with f′(c) = 0. The dashed horizontal line touches the vertex C(3, −1): there the tangent is horizontal, and f′(x) = 2x − 6 = 0 gives c = 3.",
               "القطع المكافئ يقطع محور الفواصل عند 2 و4 إذن f(2) = f(4) = 0. وهو مستمر وقابل للاشتقاق في كل مكان. تقول مبرهنة رول إنه يوجد c بين 2 و4 يحقق f′(c) = 0. المستقيم الأفقي المتقطع يمسّ الرأس C(3, −1): هناك المماس أفقي، وf′(x) = 2x − 6 = 0 تعطي c = 3.",
               "La parabole coupe l'axe en 2 et 4 : f(2) = f(4) = 0. Rolle : il existe c ∈ ]2 ; 4[ avec f′(c) = 0. La droite pointillée touche le sommet C(3 ; −1) : c = 3."))
    s = section(m, "Mean Value Theorem")
    g = lambda x: x ** 3
    s.append(fn_graph(g, (-0.5, 2.5), (-1, 9), pts={"A": (0, 0), "B": (2, 8), "C": (round(2 / math.sqrt(3), 3), round((2 / math.sqrt(3)) ** 3, 3))},
                      curves=[lambda x: 4 * x, lambda x: 4 * (x - 2 / math.sqrt(3)) + (2 / math.sqrt(3)) ** 3], tag="D2", label="f(x) = x³ on [0, 2]"))
    s.append(T("The chord from A(0, 0) to B(2, 8) has slope (8 − 0)/(2 − 0) = 4. The Mean Value Theorem says some point C in between has a tangent with the same slope. Since f′(x) = 3x² = 4, c = 2/√3 ≈ 1.155. The two dashed lines are parallel: the chord and the tangent at C.",
               "الوتر من A(0, 0) إلى B(2, 8) ميله (8 − 0)/(2 − 0) = 4. تقول مبرهنة القيمة المتوسطة إن نقطة C بينهما مماسها له الميل نفسه. وبما أن f′(x) = 3x² = 4 فإن c = 2/√3 ≈ 1.155. المستقيمان المتقطعان متوازيان: الوتر والمماس عند C.",
               "La corde de A(0 ; 0) à B(2 ; 8) a pour pente 4. Il existe C avec f′(c) = 3c² = 4 : c = 2/√3 ≈ 1,155. Corde et tangente sont parallèles."))
    s = section(m, "Rolle: hypotheses first")
    s.append(fn_graph(lambda x: abs(x), (-2, 2), (-0.5, 2.5), pts={"A": (-1, 1), "B": (1, 1), "O": (0, 0)}, tag="D3", label="f(x) = |x| on [−1, 1]"))
    s.append(T("Here f(−1) = f(1) = 1, and f is continuous. But there is a sharp corner at 0, so f is not differentiable there, and the tangent is never horizontal anywhere. The conclusion of Rolle fails because one hypothesis fails. Always check all three hypotheses.",
               "هنا f(−1) = f(1) = 1 والدالة مستمرة. لكن عند 0 زاوية حادة فالدالة غير قابلة للاشتقاق هناك ولا يوجد مماس أفقي في أي نقطة. تفشل خلاصة رول لأن أحد الشروط فشل. نتحقق دائمًا من الشروط الثلاثة.",
               "f(−1) = f(1) = 1 et f continue, mais pas dérivable en 0 : aucune tangente horizontale. Il faut vérifier les trois hypothèses."))
    s = section(m, "Monotonicity and comparison")
    s.append(fn_graph(lambda x: x ** 3 - 3 * x, (-3, 3), (-5, 5), pts={"A": (-1, 2), "B": (1, -2)}, tag="D4", label="f(x) = x³ − 3x"))
    s.append(T("f′(x) = 3x² − 3 = 3(x − 1)(x + 1). The sign of f′ gives the shape: f′ > 0 on (−∞, −1), so f rises up to the maximum A(−1, 2); f′ < 0 on (−1, 1), so f falls down to the minimum B(1, −2); f′ > 0 again after 1. The graph and the sign table tell the same story.",
               "f′(x) = 3x² − 3 = 3(x − 1)(x + 1). إشارة f′ تعطي الشكل: f′ > 0 على (−∞, −1) فترتفع f حتى القيمة العظمى A(−1, 2)؛ f′ < 0 على (−1, 1) فتنخفض حتى القيمة الصغرى B(1, −2)؛ ثم f′ > 0 بعد 1. الرسم وجدول الإشارة يرويان القصة نفسها.",
               "f′ = 3(x − 1)(x + 1) : f croît jusqu'à A(−1 ; 2), décroît jusqu'à B(1 ; −2), puis croît."))
    s.append(F("x: −∞ → −1 → 1 → +∞      f′: +  0  −  0  +      f: ↗ 2 ↘ −2 ↗"))

    m.EXERCISES[:] = [
        EX("1", "", st("f(x) = x² − 6x + 8 on [2, 4]: verify Rolle's hypotheses and find c.", "f(x) = x² − 6x + 8 على [2, 4]: تحقق من شروط رول وجد c.", "Vérifie Rolle pour f(x) = x² − 6x + 8 sur [2 ; 4] et trouve c."), [
            T("f is a polynomial, so continuous on [2, 4] and differentiable on (2, 4).", "f كثير حدود إذن مستمرة على [2, 4] وقابلة للاشتقاق على (2, 4).", "Polynôme : continue et dérivable."),
            T("f(2) = 4 − 12 + 8 = 0 and f(4) = 16 − 24 + 8 = 0, so f(2) = f(4).", "f(2) = 4 − 12 + 8 = 0 وf(4) = 16 − 24 + 8 = 0 إذن f(2) = f(4).", "f(2) = f(4) = 0."),
            T("f′(x) = 2x − 6 = 0 gives c = 3, which lies in (2, 4).", "f′(x) = 2x − 6 = 0 تعطي c = 3 وهو في (2, 4).", "f′(c) = 0 → c = 3 ∈ ]2 ; 4[."),
            F("c = 3")]),
        EX("2", "", st("f(x) = x³ on [0, 2]: find the point guaranteed by the Mean Value Theorem.", "f(x) = x³ على [0, 2]: جد النقطة التي تضمنها مبرهنة القيمة المتوسطة.", "TAF pour x³ sur [0 ; 2] : trouve c."), [
            T("Slope of the chord: (f(2) − f(0))/(2 − 0) = 8/2 = 4.", "ميل الوتر: (f(2) − f(0))/(2 − 0) = 8/2 = 4.", "Pente de la corde : 4."),
            T("Solve f′(c) = 3c² = 4: c² = 4/3, c = 2/√3 ≈ 1.155 (the positive root, inside (0, 2)).", "نحلّ f′(c) = 3c² = 4: c² = 4/3 وc = 2/√3 ≈ 1.155 (الجذر الموجب داخل (0, 2)).", "3c² = 4 → c = 2/√3 ≈ 1,155."),
            F("c = 2/√3")]),
        EX("3", "", st("Evaluate lim x→3 (x² − 9)/(x − 3) by factoring and by L'Hôpital.", "احسب lim x→3 (x² − 9)/(x − 3) بالتحليل وبقاعدة لوبيتال.", "Calcule lim x→3 (x² − 9)/(x − 3) de deux façons."), [
            T("At x = 3 we get 0/0, an indeterminate form.", "عند x = 3 نحصل على 0/0 وهي صيغة غير معيّنة.", "Forme 0/0."),
            T("Factoring: (x − 3)(x + 3)/(x − 3) = x + 3 → 6.", "بالتحليل: (x − 3)(x + 3)/(x − 3) = x + 3 → 6.", "Factorisation : x + 3 → 6."),
            T("L'Hôpital: differentiate top and bottom: 2x/1 → 6. Same answer, which is a good check.", "لوبيتال: نشتق البسط والمقام: 2x/1 → 6. الجواب نفسه وهذا تحقق جيد.", "L'Hôpital : 2x → 6."),
            F("limit = 6")]),
        EX("4", "", st("Why does Rolle fail for f(x) = |x| on [−1, 1]?", "لماذا تفشل مبرهنة رول من أجل f(x) = |x| على [−1, 1]؟", "Pourquoi Rolle échoue-t-il pour |x| sur [−1 ; 1] ?"), [
            T("f(−1) = f(1) = 1 and f is continuous, but f is not differentiable at 0 (left slope −1, right slope +1).", "f(−1) = f(1) = 1 والدالة مستمرة لكنها غير قابلة للاشتقاق عند 0 (ميل اليسار −1 وميل اليمين +1).", "Pas dérivable en 0."),
            T("The graph on the board shows the corner: no horizontal tangent exists, so the conclusion fails. Rolle needs all three hypotheses.", "الرسم على اللوح يبيّن الزاوية: لا يوجد مماس أفقي فتفشل الخلاصة. رول يحتاج إلى الشروط الثلاثة.", "Aucune tangente horizontale."),
            F("Hypothesis 'differentiable on (−1, 1)' fails")]),
        EX("5", "", st("If f′(x) > 0 on ℝ, can f(x) = k (a constant) be f? Study f(x) = x³ − 3x: find its extrema.", "إذا كانت f′(x) > 0 على ℝ فهل يمكن أن تكون f ثابتة؟ ثم ادرس f(x) = x³ − 3x وجد قيمها القصوى.", "Si f′ > 0 sur ℝ, f peut-elle être constante ? Extrema de x³ − 3x ?"), [
            T("A constant function has f′ = 0 everywhere, not f′ > 0. So f is strictly increasing, never constant.", "الدالة الثابتة مشتقتها 0 في كل مكان لا f′ > 0. إذن f متزايدة تمامًا وليست ثابتة.", "Constante ⇒ f′ = 0 : impossible."),
            T("For x³ − 3x: f′ = 3(x − 1)(x + 1). Local maximum f(−1) = −1 + 3 = 2. Local minimum f(1) = 1 − 3 = −2.", "من أجل x³ − 3x: f′ = 3(x − 1)(x + 1). قيمة عظمى محلية f(−1) = −1 + 3 = 2 وقيمة صغرى محلية f(1) = 1 − 3 = −2.", "Max local f(−1) = 2, min local f(1) = −2."),
            F("max 2 at x = −1      min −2 at x = 1")]),
        EX("6", "", st("Use the Mean Value Theorem to prove |sin a − sin b| ≤ |a − b|.", "استعمل مبرهنة القيمة المتوسطة لإثبات |sin a − sin b| ≤ |a − b|.", "Prouve |sin a − sin b| ≤ |a − b| avec le TAF."), [
            T("Take a < b. sin is differentiable everywhere, so there is c between a and b with (sin b − sin a)/(b − a) = cos c.", "ناخذ a < b. sin قابلة للاشتقاق في كل مكان إذن يوجد c بين a وb بحيث (sin b − sin a)/(b − a) = cos c.", "∃c : (sin b − sin a)/(b − a) = cos c."),
            T("Since |cos c| ≤ 1, we get |sin b − sin a| ≤ |b − a|.", "وبما أن |cos c| ≤ 1 نجد |sin b − sin a| ≤ |b − a|.", "|cos c| ≤ 1."),
            F("|sin a − sin b| ≤ |a − b|")]),
        EX("7", "", st("Show that x³ + x − 1 = 0 has exactly one real root and locate it between two integers.", "بيّن أن المعادلة x³ + x − 1 = 0 لها جذر حقيقي واحد فقط وعيّن موضعه بين عددين صحيحين.", "Montre que x³ + x − 1 = 0 a une seule racine réelle et situe-la."), [
            T("Let f(x) = x³ + x − 1. Then f′(x) = 3x² + 1 > 0 for all x, so f is strictly increasing: it can cross zero at most once.", "ليكن f(x) = x³ + x − 1. f′(x) = 3x² + 1 > 0 لكل x فالدالة متزايدة تمامًا: تقطع الصفر مرة واحدة على الأكثر.", "f′ > 0 : au plus une racine."),
            T("f(0) = −1 < 0 and f(1) = 1 > 0 and f is continuous, so by the Intermediate Value Theorem there is a root in (0, 1). Numerically it is about 0.682.", "f(0) = −1 < 0 وf(1) = 1 > 0 والدالة مستمرة فبمبرهنة القيم المتوسطة يوجد جذر في (0, 1). عدديًا يساوي نحو 0.682.", "TVI : racine dans ]0 ; 1[, ≈ 0,682."),
            F("exactly one root, in (0, 1)")]),
        EX("8", "", st("Error detective: 'f′(c) = 0, so f has a maximum or minimum at c.' Give a counterexample.", "المحقق: «f′(c) = 0 إذن f لها قيمة عظمى أو صغرى عند c». أعطِ مثالًا مضادًا.", "Détective : « f′(c) = 0 ⇒ extremum ». Contre-exemple ?"), [
            T("Take f(x) = x³ and c = 0. We have f′(0) = 0, but f is increasing on both sides of 0, so there is no extremum.", "نأخذ f(x) = x³ وc = 0. f′(0) = 0 لكن f متزايدة على جانبي 0 إذن لا توجد قيمة قصوى.", "x³ en 0 : f′(0) = 0 sans extremum."),
            T("An extremum requires f′ to change sign. Always check the sign on both sides.", "القيمة القصوى تتطلب أن تغيّر f′ إشارتها. نتحقق دائمًا من الإشارة على الجانبين.", "Il faut un changement de signe de f′."),
            F("f′(c) = 0 is necessary, not sufficient")]),
    ]
