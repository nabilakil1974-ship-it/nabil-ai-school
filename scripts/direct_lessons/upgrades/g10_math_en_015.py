from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import section, add_ex, add_sec
from scripts.direct_lessons.draw import vectors

R, B, G = "#e53935", "#1e88e5", "#2e7d32"


def upgrade(m):
    s = section(m, "A perpendicularity test")
    s.append(vectors([("u(2,1)", (0, 0), (2, 1), R), ("v(1,−2)", (0, 0), (1, -2), B)], lo=(-2, -3), hi=(4, 3), tag="E1"))
    s.append(T("u = (2, 1) and v = (1, −2). Their dot product is 2 × 1 + 1 × (−2) = 0, so they are perpendicular. On the picture the red and blue arrows meet at a right angle. Zero is the test: you do not need to measure.",
               "u = (2, 1) وv = (1, −2). جداؤهما السلمي 2 × 1 + 1 × (−2) = 0 إذن متعامدان. في الصورة يلتقي السهمان الأحمر والأزرق بزاوية قائمة. الصفر هو الاختبار: لا حاجة إلى القياس.",
               "u·v = 2 − 2 = 0 : perpendiculaires, sans mesurer."))
    add_ex(m, [
        EX("", "", st("Find the angle between u = (1, 2) and v = (3, 1).", "جد الزاوية بين u = (1, 2) وv = (3, 1).", "Angle entre u = (1 ; 2) et v = (3 ; 1)."), [
            T("u·v = 1 × 3 + 2 × 1 = 5. |u| = √5, |v| = √10.", "u·v = 1 × 3 + 2 × 1 = 5. |u| = √5 وَ|v| = √10.", "u·v = 5 ; √5 ; √10."), T("cos θ = 5/(√5 √10) = 5/√50 = 1/√2, so θ = 45°.", "cos θ = 5/(√5 √10) = 5/√50 = 1/√2 إذن θ = 45°.", "cos θ = 1/√2 → 45°."), vectors([("u", (0, 0), (1, 2), R), ("v", (0, 0), (3, 1), B)], lo=(-1, -1), hi=(5, 4), tag="X1"), F("θ = 45°")]),
        EX("", "", st("Show that the triangle A(1, 1), B(4, 1), C(1, 5) has a right angle at A.", "بيّن أن المثلث A(1, 1) وB(4, 1) وC(1, 5) قائم في A.", "Montre que le triangle est rectangle en A."), [
            T("AB = (3, 0) and AC = (0, 4). AB·AC = 3 × 0 + 0 × 4 = 0, so AB ⊥ AC.", "AB = (3, 0) وAC = (0, 4). AB·AC = 3 × 0 + 0 × 4 = 0 إذن AB ⊥ AC.", "AB·AC = 0."), F("right angle at A")]),
        EX("", "", st("Find k so that (k, 2) is perpendicular to (3, −6).", "جد k ليكون (k, 2) عموديًا على (3, −6).", "Trouve k pour que (k ; 2) ⊥ (3 ; −6)."), [
            T("3k + 2 × (−6) = 0, so 3k = 12 and k = 4.", "3k + 2 × (−6) = 0 إذن 3k = 12 وk = 4.", "3k − 12 = 0 → k = 4."), F("k = 4"), F("Check: (4, 2)·(3, −6) = 12 − 12 = 0 ✓")]),
        EX("", "", st("A(0, 0), B(4, 3). Find a vector perpendicular to AB with length 10.", "A(0, 0) وB(4, 3). جد متجهًا عموديًا على AB طوله 10.", "Vecteur perpendiculaire à AB de longueur 10."), [
            T("AB = (4, 3). Swap and negate one: (−3, 4) gives 4 × (−3) + 3 × 4 = 0 ✓. Its length is √(9 + 16) = 5.", "AB = (4, 3). نبدّل الإحداثيتين ونعكس إشارة إحداهما: (−3, 4) يعطي 4 × (−3) + 3 × 4 = 0 ✓. طوله √(9 + 16) = 5.", "(−3 ; 4), longueur 5."), T("Multiply by 2 to get length 10: (−6, 8).", "نضرب في 2 لنحصل على الطول 10: (−6, 8).", "×2 : (−6 ; 8)."), F("(−6, 8) or (6, −8)")]),
    ])
