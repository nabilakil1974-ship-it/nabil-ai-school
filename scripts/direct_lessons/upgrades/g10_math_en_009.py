from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import section, add_ex, add_sec
from scripts.direct_lessons.draw import vectors

R, B, G = "#e53935", "#1e88e5", "#2e7d32"


def upgrade(m):
    add_sec(m, ("The parallelogram rule", "قاعدة متوازي الأضلاع", "La règle du parallélogramme"), [
        T("Two vectors u and v starting from the same point: draw the parallelogram they span. The diagonal from the start is u + v. Here u = (4, 1), v = (1, 3): the diagonal is (5, 4). The opposite sides are equal vectors, which is why a quadrilateral with AB = DC is a parallelogram.",
          "متجهان u وv ينطلقان من النقطة نفسها: نرسم متوازي الأضلاع الذي يولّدانه. القطر الخارج من نقطة البداية هو u + v. هنا u = (4, 1) وv = (1, 3): القطر (5, 4). الضلعان المتقابلان متجهان متساويان ولهذا يكون الرباعي الذي فيه AB = DC متوازي أضلاع.",
          "Le parallélogramme construit sur u = (4 ; 1) et v = (1 ; 3) a pour diagonale u + v = (5 ; 4)."),
        vectors([("u", (0, 0), (4, 1), R), ("v", (0, 0), (1, 3), B), ("u+v", (0, 0), (5, 4), G), ("", (4, 1), (5, 4), B), ("", (1, 3), (5, 4), R)], tag="P1", lo=(-1, -1), hi=(7, 6)),
        F("u + v = (4 + 1, 1 + 3) = (5, 4)"),
    ])
    add_ex(m, [
        EX("", "", st("A(0, 0), B(4, 1), C(5, 4), D(1, 3). Show ABCD is a parallelogram.", "A(0, 0) وB(4, 1) وC(5, 4) وD(1, 3). بيّن أن ABCD متوازي أضلاع.", "Montre que ABCD est un parallélogramme."), [
            T("AB = (4, 1) and DC = (5 − 1, 4 − 3) = (4, 1). So AB = DC as vectors.", "AB = (4, 1) وDC = (5 − 1, 4 − 3) = (4, 1). إذن AB = DC كمتجهين.", "AB = (4 ; 1) = DC."), T("Two opposite sides equal and parallel means ABCD is a parallelogram. Check the other pair: AD = (1, 3) and BC = (1, 3) ✓.", "ضلعان متقابلان متساويان ومتوازيان يعني أن ABCD متوازي أضلاع. نتحقق من الزوج الآخر: AD = (1, 3) وBC = (1, 3) ✓.", "AD = BC = (1 ; 3)."), F("AB = DC and AD = BC")]),
        EX("", "", st("The midpoint of A(2, 6) and B(8, 2). Then find D so that ABCD is a parallelogram with C(10, 5).", "منتصف A(2, 6) وB(8, 2). ثم جد D ليكون ABCD متوازي أضلاع علمًا أن C(10, 5).", "Milieu de A(2 ; 6), B(8 ; 2) puis D pour que ABCD soit un parallélogramme, C(10 ; 5)."), [
            T("Midpoint M = ((2 + 8)/2, (6 + 2)/2) = (5, 4).", "المنتصف M = ((2 + 8)/2, (6 + 2)/2) = (5, 4).", "M = (5 ; 4)."), T("For a parallelogram AB = DC: (6, −4) = (10 − x, 5 − y), so x = 4 and y = 9. D = (4, 9).", "لمتوازي الأضلاع AB = DC: (6, −4) = (10 − x, 5 − y) إذن x = 4 وy = 9. D = (4, 9).", "AB = DC → D = (4 ; 9)."), F("M = (5, 4)      D = (4, 9)")]),
        EX("", "", st("Does AB = CD (as lengths) prove vector AB = vector CD? Give an example.", "هل AB = CD (طولًا) تثبت أن المتجه AB = المتجه CD؟ أعطِ مثالًا.", "AB = CD en longueur prouve-t-il l'égalité vectorielle ?"), [
            T("No. Take A(0, 0), B(3, 0) and C(0, 0), D(0, 3): both lengths are 3, but AB = (3, 0) and CD = (0, 3) point in different directions.", "لا. خذ A(0, 0) وB(3, 0) وC(0, 0) وD(0, 3): الطولان 3 لكن AB = (3, 0) وCD = (0, 3) باتجاهين مختلفين.", "AB = (3 ; 0), CD = (0 ; 3) : même longueur, vecteurs différents."), F("equal vectors need equal direction, sense AND length")]),
        EX("", "", st("Three forces act on a point: (3, 0), (0, 4) and (−3, −4). What is the resultant? What does it mean?", "ثلاث قوى تؤثر في نقطة: (3, 0) و(0, 4) و(−3, −4). ما المحصلة؟ وماذا تعني؟", "Trois forces (3 ; 0), (0 ; 4), (−3 ; −4) : résultante ?"), [
            T("Sum = (3 + 0 − 3, 0 + 4 − 4) = (0, 0). The resultant is the zero vector: the forces balance and the point stays still.", "المجموع = (3 + 0 − 3, 0 + 4 − 4) = (0, 0). المحصلة هي المتجه المعدوم: القوى متوازنة وتبقى النقطة ساكنة.", "Somme nulle : équilibre."), F("resultant = (0, 0)")]),
    ])
