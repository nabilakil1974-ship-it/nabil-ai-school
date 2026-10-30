from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import section, add_ex, add_sec
from scripts.direct_lessons.draw import cube


def upgrade(m):
    s = section(m, "Visible and hidden")
    s.append(cube(tag="K1"))
    s.append(T("This is the standard drawing of a cube. Solid lines are edges we can see; dashed lines are hidden edges behind the cube: AE, EF and EH. The front face ABCD is drawn as a true square, but the side faces are squeezed into parallelograms. Real edge lengths are all equal, yet the drawing shows the oblique ones shorter.",
               "هذا هو الرسم المعتاد للمكعب. الخطوط المتصلة أحرف نراها والخطوط المتقطعة أحرف مخفية خلف المكعب: AE وEF وEH. الوجه الأمامي ABCD مرسوم مربعًا حقيقيًا أما الوجوه الجانبية فمضغوطة إلى متوازيات أضلاع. أطوال الأحرف الحقيقية كلها متساوية لكن الرسم يُظهر المائلة منها أقصر.",
               "Traits pleins : arêtes visibles ; pointillés : cachées (AE, EF, EH). La face ABCD est un vrai carré ; les faces latérales sont déformées."))
    add_sec(m, ("Counting vertices, edges and faces", "عدّ الرؤوس والأحرف والأوجه", "Sommets, arêtes, faces"), [
        T("A cube has 8 vertices (A to H), 12 edges (4 on the front face, 4 on the back face, 4 joining them) and 6 faces. Euler's relation for convex solids: vertices − edges + faces = 8 − 12 + 6 = 2. Use this to check any count you make.",
          "للمكعب 8 رؤوس (من A إلى H) و12 حرفًا (4 في الوجه الأمامي و4 في الخلفي و4 تصل بينهما) و6 أوجه. علاقة أويلر للمجسمات المحدبة: الرؤوس − الأحرف + الأوجه = 8 − 12 + 6 = 2. استعملها للتحقق من أي عدّ.",
          "8 sommets, 12 arêtes, 6 faces : 8 − 12 + 6 = 2 (Euler)."),
        cube(tag="K2", extra_lines=[("A", "B", "#e53935"), ("B", "C", "#e53935"), ("C", "D", "#e53935"), ("D", "A", "#e53935")]),
        F("V − E + F = 2"),
    ])
    add_ex(m, [
        EX("", "", st("A rectangular box has 8 vertices and 6 faces. How many edges? Check with Euler.", "علبة مستطيلة لها 8 رؤوس و6 أوجه. كم حرفًا؟ تحقق بعلاقة أويلر.", "Un pavé : 8 sommets, 6 faces : combien d'arêtes ?"), [
            T("V − E + F = 2 gives 8 − E + 6 = 2, so E = 12.", "V − E + F = 2 تعطي 8 − E + 6 = 2 إذن E = 12.", "E = 12."), F("12 edges")]),
        EX("", "", st("A cube has edge 5 cm. Find its total edge length, one face area, total surface area and volume.", "مكعب حرفه 5 سم. جد مجموع أطوال أحرفه ومساحة وجه ومساحته الكلية وحجمه.", "Cube d'arête 5 cm : longueur des arêtes, aire d'une face, aire totale, volume."), [
            T("12 edges × 5 = 60 cm. One face: 5² = 25 cm². Six faces: 150 cm². Volume 5³ = 125 cm³.", "12 حرفًا × 5 = 60 سم. وجه واحد: 5² = 25 سم². ستة أوجه: 150 سم². الحجم 5³ = 125 سم³.", "60 cm ; 25 ; 150 ; 125."), F("60 cm   25 cm²   150 cm²   125 cm³")]),
        EX("", "", st("In the drawing, which of the edges AB, AE, EH, CG are drawn dashed, and why?", "في الرسم أي الأحرف AB وAE وEH وCG مرسومة بخط متقطع ولماذا؟", "Dans le dessin, lesquelles de AB, AE, EH, CG sont en pointillés ?"), [
            T("AE and EH are hidden behind the front and bottom faces, so they are dashed. AB and CG are visible edges, drawn solid.", "AE وEH مخفيان خلف الوجهين الأمامي والسفلي فهما متقطعان. أما AB وCG فظاهران ومرسومان بخط متصل.", "AE et EH cachées ; AB et CG visibles."), F("dashed: AE, EH")]),
    ])
