from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import section, add_ex, add_sec
from scripts.direct_lessons.draw import cube


def upgrade(m):
    add_sec(m, ("Review picture: lines and sections", "صورة مراجعة: المستقيمات والمقاطع", "Image de révision : droites et sections"), [
        T("One cube, many questions. The red edge AB and the blue edge CG are skew. The orange rectangle ACGE is the section by the diagonal plane. The planes of the front and back faces are parallel. If you can read all three facts from this single picture, you have the chapter.",
          "مكعب واحد وأسئلة كثيرة. الحرف الأحمر AB والأزرق CG متخالفان. المستطيل البرتقالي ACGE هو المقطع بالمستوي القطري. ومستويا الوجهين الأمامي والخلفي متوازيان. إن استطعت قراءة الحقائق الثلاث من هذه الصورة الواحدة فقد أتقنت الفصل.",
          "AB et CG gauches ; ACGE section diagonale ; faces avant et arrière parallèles."),
        cube(tag="R1", section=["A", "C", "G", "E"], extra_lines=[("A", "B", "#e53935"), ("C", "G", "#1e88e5")]),
    ])
    add_ex(m, [
        EX("", "", st("Cube of edge 4. Find the length of a face diagonal AC and of the space diagonal AG.", "مكعب حرفه 4. جد طول قطر الوجه AC وقطر المكعب AG.", "Cube d'arête 4 : diagonale AC de face et diagonale AG du cube."), [
            T("AC = 4√2 ≈ 5.66 (Pythagoras in the square ABCD). Then triangle ACG is right-angled at C: AG² = AC² + CG² = 32 + 16 = 48, so AG = 4√3 ≈ 6.93.", "AC = 4√2 ≈ 5.66 (فيثاغورس في المربع ABCD). المثلث ACG قائم في C: AG² = AC² + CG² = 32 + 16 = 48 إذن AG = 4√3 ≈ 6.93.", "AC = 4√2 ; AG² = 48 → AG = 4√3."), F("AC = 4√2      AG = 4√3")]),
        EX("", "", st("State whether each is true or false in the cube: AB ∥ GH, AB ∥ CG, (ABCD) ∥ (EFGH), AC and EG skew.", "بيّن صحة كل عبارة في المكعب: AB ∥ GH وAB ∥ CG و(ABCD) ∥ (EFGH) وAC وEG متخالفان.", "Vrai ou faux : AB ∥ GH, AB ∥ CG, (ABCD) ∥ (EFGH), AC et EG gauches."), [
            T("AB ∥ GH: true (opposite edges of a box). AB ∥ CG: false, they are skew. (ABCD) ∥ (EFGH): true. AC and EG: AC ∥ EG, both are face diagonals in parallel faces, in the plane ACGE, so they are parallel, not skew: false.", "AB ∥ GH: صحيحة (حرفان متقابلان). AB ∥ CG: خاطئة فهما متخالفان. (ABCD) ∥ (EFGH): صحيحة. AC وEG: AC ∥ EG وهما قطرا وجهين متوازيين في المستوي ACGE فهما متوازيان لا متخالفان: العبارة خاطئة.", "V ; F ; V ; F."), F("true, false, true, false")]),
        EX("", "", st("Give the justification chain that the triangle BDG is equilateral for any cube of edge a.", "اكتب سلسلة التبرير لإثبات أن المثلث BDG متساوي الأضلاع لأي مكعب حرفه a.", "Justifie que BDG est équilatéral."), [
            T("BD, DG and BG are diagonals of three faces of the cube. In each face (a square of side a), the diagonal is a√2 by Pythagoras. Three equal sides: the triangle is equilateral.", "BD وDG وBG أقطار لثلاثة أوجه من المكعب. في كل وجه (مربع ضلعه a) القطر a√2 بفيثاغورس. ثلاثة أضلاع متساوية: المثلث متساوي الأضلاع.", "Trois diagonales de faces : a√2."), F("BD = DG = BG = a√2")]),
    ])
