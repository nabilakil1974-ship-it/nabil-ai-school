from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import section, add_ex, add_sec, fn_graph


def upgrade(m):
    add_sec(m, ("The four quadrants", "الأرباع الأربعة", "Les quatre quadrants"), [
        T("The axes cut the plane into four quadrants. Quadrant I (x > 0, y > 0) is top right; II (x < 0, y > 0) is top left; III (x < 0, y < 0) is bottom left; IV (x > 0, y < 0) is bottom right. A(3, 2) is in I, B(−2, 3) in II, C(−3, −2) in III, D(4, −3) in IV.",
          "يقسم المحوران المستوي إلى أربعة أرباع. الربع I (x > 0, y > 0) أعلى اليمين؛ وII (x < 0, y > 0) أعلى اليسار؛ وIII (x < 0, y < 0) أسفل اليسار؛ وIV (x > 0, y < 0) أسفل اليمين. A(3, 2) في I وB(−2, 3) في II وC(−3, −2) في III وD(4, −3) في IV.",
          "Quatre quadrants selon les signes de x et y. A en I, B en II, C en III, D en IV."),
        fn_graph(lambda x: float("nan"), (-5, 5), (-4, 4), pts={"A": (3, 2), "B": (-2, 3), "C": (-3, -2), "D": (4, -3)}, tag="Q1", label="I (top right) II (top left)"),
        F("I: (+, +)   II: (−, +)   III: (−, −)   IV: (+, −)"),
    ])
    add_ex(m, [
        EX("", "", st("In which quadrant is each point: (5, −2), (−1, −7), (0, 4), (−3, 6)?", "في أي ربع تقع كل نقطة: (5, −2) و(−1, −7) و(0, 4) و(−3, 6)؟", "Dans quel quadrant : (5 ; −2), (−1 ; −7), (0 ; 4), (−3 ; 6) ?"), [
            T("(5, −2): x > 0, y < 0 → IV. (−1, −7): both negative → III. (−3, 6): x < 0, y > 0 → II.", "(5, −2): x > 0 وy < 0 → IV. (−1, −7): كلاهما سالب → III. (−3, 6): x < 0 وy > 0 → II.", "IV ; III ; II."), T("(0, 4) has x = 0, so it lies on the y-axis, not inside any quadrant.", "النقطة (0, 4) فاصلتها 0 فهي على محور التراتيب لا داخل أي ربع.", "(0 ; 4) est sur l'axe des ordonnées."), F("IV, III, on the y-axis, II")]),
        EX("", "", st("Reflect P(3, −2) across the x-axis, the y-axis and the origin.", "جد نظير P(3, −2) بالنسبة إلى محور الفواصل ومحور التراتيب والمبدأ.", "Symétriques de P(3 ; −2) par rapport aux axes et à l'origine."), [
            T("Across the x-axis the y changes sign: (3, 2). Across the y-axis the x changes sign: (−3, −2). Across the origin both change: (−3, 2).", "بالنسبة إلى محور الفواصل تتغير إشارة y: (3, 2). وبالنسبة إلى محور التراتيب تتغير إشارة x: (−3, −2). وبالنسبة إلى المبدأ تتغيران: (−3, 2).", "(3 ; 2), (−3 ; −2), (−3 ; 2)."), fn_graph(lambda x: float("nan"), (-5, 5), (-4, 4), pts={"P": (3, -2), "P1": (3, 2), "P2": (-3, -2), "P3": (-3, 2)}, tag="X1", label="P and its three reflections"), F("(3, 2)   (−3, −2)   (−3, 2)")]),
        EX("", "", st("Three vertices of a rectangle are (1, 1), (5, 1), (5, 4). Find the fourth vertex, the perimeter and the area.", "ثلاثة رؤوس لمستطيل هي (1, 1) و(5, 1) و(5, 4). جد الرأس الرابع والمحيط والمساحة.", "Trois sommets d'un rectangle (1 ; 1), (5 ; 1), (5 ; 4) : quatrième, périmètre, aire."), [
            T("The sides are horizontal and vertical, so the fourth vertex is (1, 4). Width 4, height 3.", "الأضلاع أفقية وشاقولية إذن الرأس الرابع (1, 4). العرض 4 والارتفاع 3.", "(1 ; 4)."), F("perimeter = 2(4 + 3) = 14      area = 4 × 3 = 12")]),
    ])
