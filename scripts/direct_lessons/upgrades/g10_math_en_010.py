from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import section, add_ex, add_sec, fn_graph

N = lambda x: float("nan")


def upgrade(m):
    s = section(m, "Do not measure a sketch")
    s.append(fn_graph(lambda x: 2 * x / 3 + 4 / 3, (-1, 9), (-1, 8), curves=[], pts={"A": (1, 2), "B": (7, 6), "M": (4, 4), "N": (4, 5)}, tag="K1", label="A(1, 2), B(7, 6)"))
    s.append(T("N looks like the middle of AB, but the picture can fool us. Use coordinates: the midpoint of A(1, 2) and B(7, 6) is M((1 + 7)/2, (2 + 6)/2) = (4, 4). N(4, 5) has the right x but the wrong y, so N is not the midpoint. Proof beats appearance.",
               "تبدو N وسط AB لكن الرسم قد يخدعنا. نستعمل الإحداثيات: منتصف A(1, 2) وB(7, 6) هو M((1 + 7)/2, (2 + 6)/2) = (4, 4). للنقطة N(4, 5) الفاصلة الصحيحة لكن الترتيب خطأ فهي ليست المنتصف. البرهان أقوى من المظهر.",
               "N semble être le milieu, mais M = (4 ; 4). N(4 ; 5) n'est pas le milieu : on prouve, on ne mesure pas."))
    add_ex(m, [
        EX("", "", st("A(−2, 1), B(4, 5). Find the midpoint M and the length AB.", "A(−2, 1) وB(4, 5). جد المنتصف M وطول AB.", "A(−2 ; 1), B(4 ; 5) : milieu M et longueur AB."), [
            T("M = ((−2 + 4)/2, (1 + 5)/2) = (1, 3).", "M = ((−2 + 4)/2, (1 + 5)/2) = (1, 3).", "M = (1 ; 3)."), T("AB = √((4 + 2)² + (5 − 1)²) = √(36 + 16) = √52 = 2√13 ≈ 7.21.", "AB = √((4 + 2)² + (5 − 1)²) = √(36 + 16) = √52 = 2√13 ≈ 7.21.", "AB = √52 ≈ 7,21."), F("M(1, 3)      AB = 2√13")]),
        EX("", "", st("Are A(0, 1), B(2, 5), C(3, 7) aligned? Prove it.", "هل A(0, 1) وB(2, 5) وC(3, 7) على استقامة واحدة؟ برهن.", "A(0 ; 1), B(2 ; 5), C(3 ; 7) sont-ils alignés ?"), [
            T("AB = (2, 4) and AC = (3, 6). Since AC = 1.5 × AB, the vectors are parallel and share the point A, so the points are aligned.", "AB = (2, 4) وAC = (3, 6). وبما أن AC = 1.5 × AB فالمتجهان متوازيان ويشتركان في A إذن النقاط على استقامة واحدة.", "AC = 1,5 AB : alignés."), F("aligned")]),
        EX("", "", st("Show that the triangle A(1, 1), B(4, 1), C(1, 5) is right-angled and find its area.", "بيّن أن المثلث A(1, 1) وB(4, 1) وC(1, 5) قائم وجد مساحته.", "Montre que le triangle est rectangle et calcule son aire."), [
            T("AB = (3, 0) and AC = (0, 4); their dot product is 0, so the angle at A is right. Legs 3 and 4, hypotenuse BC = 5.", "AB = (3, 0) وAC = (0, 4) وجداؤهما السلمي 0 إذن الزاوية عند A قائمة. الضلعان 3 و4 والوتر BC = 5.", "AB·AC = 0 : angle droit en A."), F("area = 3 × 4 / 2 = 6")]),
    ])
