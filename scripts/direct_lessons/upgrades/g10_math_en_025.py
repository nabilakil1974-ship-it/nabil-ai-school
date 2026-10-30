from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import section, add_ex, add_sec
from scripts.direct_lessons.draw import cube


def upgrade(m):
    s = section(m, "Incidence must be justified")
    s.append(cube(tag="L1", extra_lines=[("A", "B", "#e53935"), ("D", "C", "#2e7d32")]))
    s.append(T("The red line AB and the green line DC lie in the same plane (the front face) and never meet: they are parallel. Compare AB with the edge CG: they do not meet either, but they are not in one plane, so they are skew lines, not parallel. In space, 'does not meet' is not enough to be parallel.",
               "المستقيم الأحمر AB والأخضر DC في المستوي نفسه (الوجه الأمامي) ولا يلتقيان: هما متوازيان. قارن AB بالحرف CG: لا يلتقيان أيضًا لكنهما ليسا في مستوٍ واحد فهما متخالفان لا متوازيان. في الفضاء «لا يلتقيان» لا يكفي ليكونا متوازيين.",
               "AB et DC sont coplanaires et ne se coupent pas : parallèles. AB et CG ne se coupent pas mais ne sont pas coplanaires : gauches."))
    add_sec(m, ("Three relations between two lines", "ثلاث علاقات بين مستقيمين", "Trois positions relatives de deux droites"), [
        T("Two lines in space can be: intersecting (one common point, like AB and AD at A), parallel (same plane, no point in common, like AB and DC), or skew (no common point and no plane containing both, like AB and CG). Only the first two are coplanar.",
          "يمكن لمستقيمين في الفضاء أن يكونا: متقاطعين (نقطة مشتركة واحدة مثل AB وAD في A) أو متوازيين (في مستوٍ واحد بلا نقطة مشتركة مثل AB وDC) أو متخالفين (لا نقطة مشتركة ولا يوجد مستوٍ يضمهما مثل AB وCG). الأولان فقط من مستوٍ واحد.",
          "Sécantes, parallèles ou gauches : seules les deux premières sont coplanaires."),
        cube(tag="L2", extra_lines=[("A", "B", "#e53935"), ("C", "G", "#1e88e5")]),
        F("intersecting  /  parallel  /  skew"),
    ])
    add_ex(m, [
        EX("", "", st("In the cube, classify each pair: (AB, AD), (AB, HG), (AB, CG), (AE, CG).", "في المكعب صنّف كل زوج: (AB, AD) و(AB, HG) و(AB, CG) و(AE, CG).", "Classe : (AB, AD), (AB, HG), (AB, CG), (AE, CG)."), [
            T("(AB, AD) meet at A: intersecting. (AB, HG): both are horizontal edges in opposite positions of the box and parallel, in the plane ABGH. (AB, CG): skew. (AE, CG): both are edges in the depth direction, parallel (in the plane AEGC).", "(AB, AD) يلتقيان في A: متقاطعان. (AB, HG): حرفان أفقيان متقابلان ومتوازيان في المستوي ABGH. (AB, CG): متخالفان. (AE, CG): كلاهما حرف في اتجاه العمق ومتوازيان في المستوي AEGC.", "sécantes ; parallèles ; gauches ; parallèles."), F("intersecting, parallel, skew, parallel")]),
        EX("", "", st("Why is the line AC contained in the plane ABCD? And is the point G in that plane?", "لماذا المستقيم AC محتوى في المستوي ABCD؟ وهل النقطة G في هذا المستوي؟", "Pourquoi (AC) est-elle dans le plan (ABCD) ? G y est-il ?"), [
            T("A and C are two points of the plane ABCD, so the whole line AC lies in the plane (a line with two points in a plane lies in it). G is a vertex of the back face and not on the front face plane, so G is not in the plane ABCD.", "A وC نقطتان من المستوي ABCD إذن المستقيم AC كله في المستوي (مستقيم له نقطتان في مستوٍ يقع فيه). أما G فرأس في الوجه الخلفي وليس في مستوي الوجه الأمامي فهي ليست في المستوي ABCD.", "Deux points du plan ⇒ la droite est dans le plan. G n'y est pas."), F("AC ⊂ (ABCD), G ∉ (ABCD)")]),
        EX("", "", st("How many planes pass through three non-aligned points? Through two points only?", "كم مستويًا يمر بثلاث نقاط ليست على استقامة واحدة؟ وبنقطتين فقط؟", "Combien de plans par trois points non alignés ? par deux points ?"), [
            T("Three non-aligned points fix exactly one plane (a stool with three legs never wobbles). Two points lie on infinitely many planes, like pages of a book turning about the spine.", "ثلاث نقاط ليست على استقامة واحدة تعيّن مستويًا واحدًا بالضبط (كرسي بثلاث أرجل لا يهتز). ونقطتان تقعان على عدد لا نهائي من المستويات مثل صفحات كتاب تدور حول عطفه.", "Un seul plan ; une infinité."), F("one plane; infinitely many")]),
    ])
