from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import section, add_ex, add_sec
from scripts.direct_lessons.draw import cube


def upgrade(m):
    s = section(m, "An intuition, then proof")
    s.append(cube(tag="N1", section=["A", "B", "C", "D"], sec_color="#1e88e5"))
    s.append(T("Look at the front face ABCD (blue) and the back face EFGH. They are parallel planes: they never meet, and the distance between them is the same everywhere, an edge length. The ceiling and the floor of a room are parallel planes in the same way.",
               "انظر إلى الوجه الأمامي ABCD (الأزرق) والوجه الخلفي EFGH. هما مستويان متوازيان: لا يلتقيان والمسافة بينهما واحدة في كل مكان وهي طول الحرف. سقف الغرفة وأرضها مستويان متوازيان بالطريقة نفسها.",
               "Les faces ABCD et EFGH sont des plans parallèles : jamais sécants, distance constante."))
    add_sec(m, ("A key theorem", "مبرهنة أساسية", "Un théorème clé"), [
        T("If a plane P contains two intersecting lines that are both parallel to a plane Q, then P and Q are parallel. In the cube, the front face ABCD contains AB and AD, which meet at A. AB ∥ EF and AD ∥ EH, and EF and EH lie in the back face EFGH. So the planes (ABCD) and (EFGH) are parallel. Notice the proof uses two intersecting lines: one line is not enough.",
          "إذا احتوى مستوٍ P مستقيمين متقاطعين كلاهما يوازي مستويًا Q فإن P وQ متوازيان. في المكعب يحوي الوجه الأمامي ABCD المستقيمين AB وAD المتقاطعين في A. AB ∥ EF وAD ∥ EH والمستقيمان EF وEH في الوجه الخلفي EFGH. إذن المستويان (ABCD) و(EFGH) متوازيان. لاحظ أن البرهان يستعمل مستقيمين متقاطعين: مستقيم واحد لا يكفي.",
          "Si un plan contient deux droites sécantes parallèles à un plan Q, il est parallèle à Q."),
        cube(tag="N2", extra_lines=[("A", "B", "#e53935"), ("A", "D", "#e53935"), ("E", "F", "#2e7d32"), ("E", "H", "#2e7d32")]),
        F("two intersecting lines of P, each parallel to Q ⇒ P ∥ Q"),
    ])
    add_ex(m, [
        EX("", "", st("In the cube name three pairs of parallel faces.", "في المكعب سمِّ ثلاثة أزواج من الوجوه المتوازية.", "Nomme trois paires de faces parallèles du cube."), [
            T("Front/back: (ABCD) and (EFGH). Left/right: (ADHE) and (BCGF). Bottom/top: (ABFE) and (DCGH).", "أمامي/خلفي: (ABCD) وَ(EFGH). أيسر/أيمن: (ADHE) وَ(BCGF). سفلي/علوي: (ABFE) وَ(DCGH).", "Trois paires."), F("3 pairs")]),
        EX("", "", st("Two parallel planes P ∥ Q are cut by a third plane R. What can you say about the two lines of intersection?", "مستويان متوازيان P ∥ Q يقطعهما مستوٍ ثالث R. ماذا تقول عن مستقيمي التقاطع؟", "P ∥ Q coupés par R : que dire des deux droites d'intersection ?"), [
            T("They are parallel. Both lines lie in the plane R, and they cannot meet because one is in P and the other in Q, and P and Q have no common point. Two lines in one plane with no common point are parallel.", "هما متوازيان. كلاهما في المستوي R ولا يلتقيان لأن أحدهما في P والآخر في Q ولا نقطة مشتركة بين P وQ. مستقيمان في مستوٍ واحد بلا نقطة مشتركة متوازيان.", "Parallèles."), F("the two intersection lines are parallel")]),
        EX("", "", st("A plane through the midpoint of AE parallel to the front face cuts the cube. What is the section and its area when a = 8?", "مستوٍ يمر بمنتصف AE ويوازي الوجه الأمامي يقطع المكعب. ما المقطع ومساحته إذا كان a = 8؟", "Plan parallèle à la face avant passant par le milieu de AE : section et aire pour a = 8."), [
            T("A plane parallel to a face cuts a square equal to that face: side 8, area 64. Its distance from the front face is 4.", "مستوٍ يوازي وجهًا يقطع مربعًا يطابق ذلك الوجه: الضلع 8 والمساحة 64. وبعده عن الوجه الأمامي 4.", "Carré de côté 8 : 64."), F("a square of area 64")]),
    ])
