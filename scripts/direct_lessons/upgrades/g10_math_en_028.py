from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import section, add_ex, add_sec, fn_graph


def upgrade(m):
    add_sec(m, ("One picture for the whole chapter", "صورة واحدة للفصل كله", "Une image pour tout le chapitre"), [
        T("Put everything together. Take f(x) = x² − 2x − 3 and the line g(x) = x + 1. The equation f = g is x² − 3x − 4 = (x − 4)(x + 1) = 0, giving x = −1 and 4. The inequality f < g holds between them. A system, an equation, an inequality, a factorisation and a graph are all the same picture.",
          "نجمع كل شيء: f(x) = x² − 2x − 3 والمستقيم g(x) = x + 1. المعادلة f = g هي x² − 3x − 4 = (x − 4)(x + 1) = 0 فتعطي x = −1 وx = 4. والمتراجحة f < g تتحقق بينهما. الجملة والمعادلة والمتراجحة والتحليل والرسم كلها الصورة نفسها.",
          "f(x) = x² − 2x − 3 et g(x) = x + 1 : f = g en x = −1 et 4 ; f < g entre les deux."),
        fn_graph(lambda x: x * x - 2 * x - 3, (-3, 6), (-5, 14), curves=[lambda x: x + 1], pts={"A": (-1, 0), "B": (4, 5)}, tag="H1", label="f (red), g (dashed)"),
    ])
    add_ex(m, [
        EX("", "", st("Solve the system y = x + 1 and y = x² − 2x − 3 and say what the solutions mean on the graph.", "حلّ الجملة y = x + 1 وَy = x² − 2x − 3 وفسّر الحلول على الرسم.", "Résous le système et interprète sur le graphique."), [
            T("Equate: x + 1 = x² − 2x − 3, so x² − 3x − 4 = 0 and (x − 4)(x + 1) = 0: x = 4 or x = −1.", "نساوي: x + 1 = x² − 2x − 3 إذن x² − 3x − 4 = 0 وَ(x − 4)(x + 1) = 0 أي x = 4 أو x = −1.", "x = 4 ou x = −1."), T("Then y = 5 and y = 0. The solutions (4, 5) and (−1, 0) are the two points where the line meets the curve.", "ثم y = 5 وy = 0. الحلان (4, 5) و(−1, 0) هما نقطتا التقاء المستقيم بالمنحنى.", "Points (4 ; 5) et (−1 ; 0)."), F("(−1, 0) and (4, 5)")]),
        EX("", "", st("Simplify (2a³b)²/(4a⁴b) and give a reason for each step.", "بسّط (2a³b)²/(4a⁴b) مع ذكر السبب لكل خطوة.", "Simplifie (2a³b)²/(4a⁴b)."), [
            T("(2a³b)² = 4a⁶b² (power of a product). Divide: 4a⁶b²/(4a⁴b) = a^(6−4) b^(2−1) = a²b.", "(2a³b)² = 4a⁶b² (قوة جداء). نقسم: 4a⁶b²/(4a⁴b) = a^(6−4) b^(2−1) = a²b.", "= a²b."), F("a²b")]),
        EX("", "", st("Solve |2x − 3| ≤ 5 and graph the solution set.", "حلّ |2x − 3| ≤ 5 ومثّل مجموعة الحل.", "Résous |2x − 3| ≤ 5 et représente."), [
            T("−5 ≤ 2x − 3 ≤ 5 → −2 ≤ 2x ≤ 8 → −1 ≤ x ≤ 4.", "−5 ≤ 2x − 3 ≤ 5 → −2 ≤ 2x ≤ 8 → −1 ≤ x ≤ 4.", "−1 ≤ x ≤ 4."), F("S = [−1, 4]")]),
    ])
