from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import section, add_ex, add_sec, fn_graph
from scripts.direct_lessons.draw import vectors

R, B, G = "#e53935", "#1e88e5", "#2e7d32"


def upgrade(m):
    add_sec(m, ("A complete problem", "مسألة متكاملة", "Un problème complet"), [
        T("A(1, 1), B(7, 3), C(4, 7). Vectors: AB = (6, 2), AC = (3, 6), BC = (−3, 4). Lengths: AB = √40 ≈ 6.32, AC = √45 ≈ 6.71, BC = 5. Dot product at B: BA·BC = (−6, −2)·(−3, 4) = 18 − 8 = 10 ≠ 0, so no right angle at B. Midpoint of BC: (5.5, 5).",
          "A(1, 1) وB(7, 3) وC(4, 7). المتجهات: AB = (6, 2) وAC = (3, 6) وBC = (−3, 4). الأطوال: AB = √40 ≈ 6.32 وAC = √45 ≈ 6.71 وBC = 5. الجداء السلمي عند B: BA·BC = (−6, −2)·(−3, 4) = 18 − 8 = 10 ≠ 0 فلا زاوية قائمة عند B. منتصف BC: (5.5, 5).",
          "A(1 ; 1), B(7 ; 3), C(4 ; 7) : AB = (6 ; 2), AC = (3 ; 6), BC = (−3 ; 4) ; pas d'angle droit en B."),
        vectors([("AB", (1, 1), (7, 3), R), ("BC", (7, 3), (4, 7), B), ("AC", (1, 1), (4, 7), G)], lo=(-1, -1), hi=(9, 9), tag="W1"),
    ])
    add_ex(m, [
        EX("", "", st("A(−1, 2), B(3, 5), C(5, 1), D(1, −2). Show ABCD is a parallelogram and check whether it is a rectangle.", "A(−1, 2) وB(3, 5) وC(5, 1) وD(1, −2). بيّن أن ABCD متوازي أضلاع واختبر هل هو مستطيل.", "Montre que ABCD est un parallélogramme ; est-ce un rectangle ?"), [
            T("AB = (4, 3) and DC = (5 − 1, 1 + 2) = (4, 3), so AB = DC: parallelogram. AD = (2, −4).", "AB = (4, 3) وDC = (5 − 1, 1 + 2) = (4, 3) إذن AB = DC: متوازي أضلاع. AD = (2, −4).", "AB = DC = (4 ; 3)."), T("Rectangle test: AB·AD = 4 × 2 + 3 × (−4) = 8 − 12 = −4 ≠ 0, so the angle at A is not right: not a rectangle.", "اختبار المستطيل: AB·AD = 4 × 2 + 3 × (−4) = 8 − 12 = −4 ≠ 0 فالزاوية عند A ليست قائمة: ليس مستطيلًا.", "AB·AD = −4 ≠ 0 : pas un rectangle."), F("parallelogram, not a rectangle")]),
        EX("", "", st("Find the equation of the line through A(1, 1) and B(7, 3), and check that the midpoint of AB lies on it.", "جد معادلة المستقيم المار بـ A(1, 1) وB(7, 3) وتحقق أن منتصف AB عليه.", "Équation de (AB) et vérification du milieu."), [
            T("Slope = (3 − 1)/(7 − 1) = 1/3. y − 1 = (x − 1)/3, so y = x/3 + 2/3. Midpoint (4, 2): 4/3 + 2/3 = 2 ✓.", "الميل = (3 − 1)/(7 − 1) = 1/3. y − 1 = (x − 1)/3 إذن y = x/3 + 2/3. المنتصف (4, 2): 4/3 + 2/3 = 2 ✓.", "y = x/3 + 2/3 ; milieu (4 ; 2) ✓."), fn_graph(lambda x: x / 3 + 2 / 3, (-1, 9), (-1, 6), pts={"A": (1, 1), "B": (7, 3), "M": (4, 2)}, tag="X1", label="y = x/3 + 2/3"), F("y = x/3 + 2/3")]),
        EX("", "", st("Find the angle between u = (3, 4) and v = (4, −3).", "جد الزاوية بين u = (3, 4) وv = (4, −3).", "Angle entre (3 ; 4) et (4 ; −3)."), [
            T("u·v = 12 − 12 = 0, so the angle is 90°. They are perpendicular, both of length 5.", "u·v = 12 − 12 = 0 إذن الزاوية 90°. هما متعامدان وطول كل منهما 5.", "u·v = 0 : 90°."), F("90°")]),
    ])
