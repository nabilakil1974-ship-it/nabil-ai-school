from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import section, add_ex, add_sec
from scripts.direct_lessons.draw import cube


def upgrade(m):
    s = section(m, "Conceptual example")
    s.append(cube(section=["A", "C", "G", "E"], tag="S1"))
    s.append(T("Cut the cube with the plane through A, C, G and E. The cut surface is the orange rectangle ACGE. Each side of a section is where the cutting plane meets one face of the cube: AC lies in the bottom face and CG in the right face. The sides are AC (a face diagonal, length a√2) and CG (an edge, length a), so it is a rectangle, not a square.",
               "نقطع المكعب بالمستوي المار بالنقاط A وC وG وE. السطح المقطوع هو المستطيل البرتقالي ACGE. أضلاعه تقع في أوجه المكعب: كل ضلع في المقطع هو حيث يلتقي المستوي القاطع بوجه واحد. أضلاعه AC (قطر طوله a√2) وCG (حرف طوله a) فهو مستطيل لا مربع.",
               "Le plan (ACGE) coupe le cube selon le rectangle ACGE : côtés AC = a√2 et CG = a."))
    s = section(m, "Why the shape changes")
    s.append(cube(section=["B", "D", "G"], tag="S2", sec_color="#8e24aa"))
    s.append(T("A different plane through B, D and G cuts off a corner and gives a triangle BDG. Its three sides are face diagonals, each of length a√2, so BDG is equilateral. Same cube, different plane, different section.",
               "مستوٍ آخر يمر بـ B وD وG يقطع ركنًا ويعطي المثلث BDG. أضلاعه الثلاثة أقطار أوجه طول كل منها a√2 فالمثلث BDG متساوي الأضلاع. المكعب نفسه ومستوٍ مختلف فمقطع مختلف.",
               "Le plan (BDG) donne le triangle BDG, équilatéral de côté a√2."))
    add_ex(m, [
        EX("", "", st("A cube has edge a = 6. Find the area of the section ACGE.", "حرف مكعب a = 6. جد مساحة المقطع ACGE.", "Cube d'arête 6 : aire de la section ACGE."), [
            T("The rectangle has sides AC = 6√2 and CG = 6. Area = 6√2 × 6 = 36√2 ≈ 50.9.", "المستطيل ضلعاه AC = 6√2 وCG = 6. المساحة = 6√2 × 6 = 36√2 ≈ 50.9.", "6√2 × 6 = 36√2 ≈ 50,9."), F("36√2 ≈ 50.9")]),
        EX("", "", st("For a = 6, find the side and area of the equilateral triangle BDG.", "من أجل a = 6 جد ضلع المثلث متساوي الأضلاع BDG ومساحته.", "a = 6 : côté et aire du triangle BDG."), [
            T("Side = 6√2 ≈ 8.49. Area of an equilateral triangle = (√3/4) × side² = (√3/4) × 72 = 18√3 ≈ 31.2.", "الضلع = 6√2 ≈ 8.49. مساحة مثلث متساوي الأضلاع = (√3/4) × الضلع² = (√3/4) × 72 = 18√3 ≈ 31.2.", "(√3/4) × 72 = 18√3 ≈ 31,2."), F("side 6√2      area 18√3")]),
        EX("", "", st("What shape results when a cube is cut by a plane parallel to a face? Give the side.", "ما شكل المقطع عندما يقطع مستوٍ مكعبًا موازيًا لأحد وجوهه؟ وما طول ضلعه؟", "Section par un plan parallèle à une face ?"), [
            T("The section is a square equal to the face, with side a. In a cube of edge a = 6 every such cut has area 36.", "المقطع مربع يطابق الوجه وضلعه a. في مكعب حرفه a = 6 تكون مساحة كل مقطع كهذا 36.", "Carré de côté a."), cube(section=[(150, 220), (360, 220), (470, 143), (260, 143)], tag="X1"), F("a square of side a")]),
    ])
