"""Grade 7 Mathematics — Chapter 4: Triangles, Case of Equality (congruent triangles)."""
import math
from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.draw import geo

LESSON_ID = "G07-MATH-EN-CH04"
GRADE = 7
SUBJECT = "math"
TITLES = {"en": "Triangles: Case of Equality", "ar": "المثلثات: حالات تساوي المثلثات", "fr": "Triangles : cas d'égalité"}

INK = "#0b3d5c"; RED = "#e53935"; BLUE = "#1e88e5"; GREEN = "#2e7d32"; ORG = "#fb8c00"; PUR = "#8e24aa"
BASE = [(55, -115), (0, 0), (180, 0)]  # A, B, C (apex above the base)


def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}


def place(pts, ang=0, dx=0, dy=0, flip=False, s=1.0):
    th = math.radians(ang); c, sn = math.cos(th), math.sin(th); out = []
    for x, y in pts:
        if flip: x = -x
        x *= s; y *= s
        out.append((x * c - y * sn + dx, x * sn + y * c + dy))
    return out


def tri(pts, names, col=INK, ticks=None, arcs=None, fill="rgba(30,136,229,.10)", acol=RED, tcol=GREEN):
    g = [("poly", pts, fill, col, 4)]
    for (i, j), n in (ticks or {}).items():
        g.append(("tick", pts[i], pts[j], n, tcol))
    for v, n in (arcs or {}).items():
        a, b = [k for k in range(3) if k != v]
        g.append(("arc", pts[v], pts[a], pts[b], 26, n, acol))
    cx = sum(p[0] for p in pts) / 3; cy = sum(p[1] for p in pts) / 3
    for p, nm in zip(pts, names):
        dx, dy = p[0] - cx, p[1] - cy; L = math.hypot(dx, dy) or 1
        g.append(("pt", p, nm, dx / L * 26, dy / L * 26 + 9, col))
    return g


L1 = place(BASE, 0, 40, 330, False, 1.3)
R1 = place(BASE, -12, 385, 335, False, 1.3)
R1m = place(BASE, 8, 600, 340, True, 1.3)  # mirrored copy (still equal)
TA = [(330, 70), (130, 330), (530, 330)]

# ---------------------------------------------------------------- drawings
def d_vocab():
    return geo([
        [("poly", TA, "rgba(30,136,229,.10)", INK, 5)],
        [("pt", TA[0], "A", 0, -18, INK), ("pt", TA[1], "B", -22, 10, INK), ("pt", TA[2], "C", 22, 10, INK)],
        [("text", ((TA[1][0] + TA[2][0]) / 2, 365), "side BC", 24, BLUE), ("text", (190, 190), "side AB", 24, BLUE), ("text", (470, 190), "side AC", 24, BLUE)],
        [("arc", TA[0], TA[1], TA[2], 40, 1, RED), ("arc", TA[1], TA[0], TA[2], 40, 2, RED), ("arc", TA[2], TA[0], TA[1], 40, 3, RED),
         ("text", (330, 405), "A + B + C = 180°", 30, RED)],
    ], "V")


def d_equal():
    t1 = tri(L1, "ABC", ticks={(0, 1): 1, (0, 2): 2, (1, 2): 3}, arcs={0: 1, 1: 2, 2: 3})
    t2 = tri(R1, "DEF", ticks={(0, 1): 1, (0, 2): 2, (1, 2): 3}, arcs={0: 1, 1: 2, 2: 3})
    return geo([[t for t in t1 if t[0] in ("poly", "pt")], [t for t in t2 if t[0] in ("poly", "pt")],
                [t for t in t1 + t2 if t[0] == "tick"], [t for t in t1 + t2 if t[0] == "arc"]], "EQ")


def d_homol():
    t1 = tri(L1, "ABC", col=INK); t2 = tri(R1, "DEF", col=INK)
    pair = lambda i: ("seg", L1[i], R1[i], ORG, 3, "8 6")
    return geo([t1, t2, [pair(0), ("text", (230, 40), "A ↔ D", 30, ORG)], [pair(1), ("text", (230, 85), "B ↔ E", 30, ORG)], [pair(2), ("text", (230, 130), "C ↔ F", 30, ORG)]], "HM")


def two(ticks, arcs, tag, extra_a=None):
    t1 = tri(L1, "ABC", ticks=ticks, arcs=arcs); t2 = tri(R1, "DEF", ticks=ticks, arcs=arcs)
    return t1, t2


def d_asa():
    t1, t2 = two({(1, 2): 1}, {1: 1, 2: 2}, "ASA")
    return geo([[t for t in t1 + t2 if t[0] in ("poly", "pt")], [t for t in t1 + t2 if t[0] == "tick"], [t for t in t1 + t2 if t[0] == "arc"]], "AS")


def d_sas():
    t1, t2 = two({(1, 0): 1, (0, 2): 2}, {0: 1}, "SAS")
    return geo([[t for t in t1 + t2 if t[0] in ("poly", "pt")], [t for t in t1 + t2 if t[0] == "tick"], [t for t in t1 + t2 if t[0] == "arc"]], "SA")


def d_sss():
    t1, t2 = two({(1, 0): 1, (0, 2): 2, (1, 2): 3}, {}, "SSS")
    return geo([[t for t in t1 + t2 if t[0] in ("poly", "pt")], [t for t in t1 + t2 if t[0] == "tick"]], "SS")


def d_aaa():
    big = [(330, 60), (60, 400), (600, 400)]
    k = 0.5; ox, oy = 215, 280
    small = [(ox + (x - 330) * k + 0, oy + (y - 400) * k + 120) for x, y in big]
    small = [(330 + (x - 330) * k, 400 + (y - 400) * k) for x, y in big]
    return geo([[("poly", big, "rgba(30,136,229,.08)", INK, 4)], [("poly", small, "rgba(229,57,53,.15)", RED, 4)],
                [("arc", big[1], big[0], big[2], 36, 1, GREEN), ("arc", big[2], big[0], big[1], 36, 2, GREEN), ("arc", big[0], big[1], big[2], 36, 3, GREEN)],
                [("arc", small[1], small[0], small[2], 22, 1, GREEN), ("arc", small[2], small[0], small[1], 22, 2, GREEN), ("arc", small[0], small[1], small[2], 22, 3, GREEN)]], "AA")


def d_constr_sas():
    A, B = (110, 340), (310, 340)
    C = (A[0] + 150 * math.cos(math.radians(45)), A[1] - 150 * math.sin(math.radians(45)))
    ray = (A[0] + 260 * math.cos(math.radians(45)), A[1] - 260 * math.sin(math.radians(45)))
    return geo([
        [("seg", A, B, INK, 4, None), ("pt", A, "A", -20, 10, INK), ("pt", B, "B", 20, 10, INK), ("text", (210, 385), "4 cm", 26, BLUE)],
        [("seg", A, ray, INK, 3, "6 5"), ("arc", A, B, ray, 46, 1, RED), ("text", (190, 325), "45°", 24, RED)],
        [("carc", A, 150, -62, -28, GREEN, "5 4"), ("text", (130, 215), "3 cm", 24, BLUE)],
        [("pt", C, "C", -6, -16, INK), ("seg", A, C, INK, 4, None), ("seg", B, C, INK, 4, None)],
    ], "K1")


def d_constr_asa():
    A, B = (110, 340), (310, 340)
    h = 200 / (math.tan(math.radians(60)) ** -1 + 1)  # tan(30)=1/1.732 -> x=h/tan30 ; tan45 = 1
    h = 200 / (1 / math.tan(math.radians(30)) + 1)
    C = (A[0] + h / math.tan(math.radians(30)), A[1] - h)
    rayA = (A[0] + 330 * math.cos(math.radians(30)), A[1] - 330 * math.sin(math.radians(30)))
    rayB = (B[0] - 260 * math.cos(math.radians(45)), B[1] - 260 * math.sin(math.radians(45)))
    return geo([
        [("seg", A, B, INK, 4, None), ("pt", A, "A", -20, 10, INK), ("pt", B, "B", 20, 10, INK), ("text", (210, 385), "4 cm", 26, BLUE)],
        [("seg", A, rayA, INK, 3, "6 5"), ("arc", A, B, rayA, 46, 1, RED), ("text", (170, 322), "30°", 22, RED)],
        [("seg", B, rayB, INK, 3, "6 5"), ("arc", B, rayB, A, 40, 1, RED), ("text", (270, 322), "45°", 22, RED)],
        [("pt", C, "C", 0, -16, INK), ("seg", A, C, INK, 4, None), ("seg", B, C, INK, 4, None), ("text", (460, 220), "C = 105°", 28, RED)],
    ], "K2")


def d_constr_sss():
    A, B = (110, 340), (310, 340)
    C = (110, 190)
    return geo([
        [("seg", A, B, INK, 4, None), ("pt", A, "A", -20, 10, INK), ("pt", B, "B", 20, 10, INK), ("text", (210, 385), "4 cm", 26, BLUE)],
        [("carc", A, 150, -100, -70, GREEN, "5 4"), ("text", (60, 230), "3 cm", 24, BLUE)],
        [("carc", B, 250, -170, -145, GREEN, "5 4"), ("text", (230, 170), "5 cm", 24, BLUE)],
        [("pt", C, "C", -8, -16, INK), ("seg", A, C, INK, 4, None), ("seg", B, C, INK, 4, None), ("right", A, B, C, 18, RED)],
    ], "K3")


def d_iso():
    A, B, C = (330, 55), (230, 330), (430, 330)
    M = (330, 330)
    return geo([
        [("poly", [A, B, C], "rgba(30,136,229,.10)", INK, 5), ("pt", A, "A", 0, -16, INK), ("pt", B, "B", -22, 10, INK), ("pt", C, "C", 22, 10, INK)],
        [("tick", A, B, 1, GREEN), ("tick", A, C, 1, GREEN), ("text", (560, 190), "AB = AC", 28, GREEN)],
        [("arc", B, A, C, 44, 1, RED), ("arc", C, A, B, 44, 1, RED), ("text", (176, 300), "70°", 26, RED), ("text", (490, 300), "70°", 26, RED)],
        [("arc", A, B, C, 50, 1, PUR), ("text", (330, 150), "A = ?", 26, PUR)],
    ], "IS")


def d_rect():
    A, B, C, D = (120, 90), (120, 320), (520, 320), (520, 90)
    return geo([
        [("poly", [A, B, C, D], "rgba(30,136,229,.08)", INK, 5), ("pt", A, "A", -18, -8, INK), ("pt", B, "B", -18, 22, INK), ("pt", C, "C", 20, 22, INK), ("pt", D, "D", 20, -8, INK)],
        [("right", A, B, D, 16, RED), ("right", B, A, C, 16, RED), ("right", C, B, D, 16, RED), ("right", D, A, C, 16, RED)],
        [("seg", A, C, ORG, 4, None), ("tick", A, C, 3, ORG)],
        [("tick", A, B, 1, GREEN), ("tick", D, C, 1, GREEN)],
        [("tick", B, C, 2, GREEN), ("tick", A, D, 2, GREEN)],
        [("poly", [A, B, C], "rgba(229,57,53,.15)", RED, 3), ("poly", [C, D, A], "rgba(30,136,229,.18)", BLUE, 3)],
    ], "RC")


def mf_geometry():
    O = (110, 330); u = (math.cos(math.radians(3)), math.sin(math.radians(3))); v = (math.cos(math.radians(-35)), math.sin(math.radians(-35)))
    P = lambda d, w: (O[0] + d * w[0], O[1] + d * w[1])
    return O, P(170, u), P(260, u), P(170, v), P(260, v), P(330, u), P(330, v)


def d_mf(upto):
    O, M, E, N, Fp, bx, ux = mf_geometry()
    g1 = [("seg", O, bx, "#6fa8dc", 4, None), ("seg", O, ux, "#6fa8dc", 4, None),
          ("pt", O, "O", -22, 22, INK), ("pt", M, "M", 4, 32, INK), ("pt", E, "E", 4, 32, INK), ("pt", N, "N", -22, -8, INK), ("pt", Fp, "F", 6, -14, INK)]
    g2 = [("tick", O, M, 1, GREEN), ("tick", O, N, 1, GREEN), ("tick", M, E, 2, GREEN), ("tick", N, Fp, 2, GREEN)]
    g3 = [("seg", O, E, ORG, 4, None), ("seg", O, Fp, ORG, 4, None), ("text", (240, 385), "OE = OM + ME", 22, ORG), ("text", (300, 130), "OF = ON + NF", 22, ORG)]
    g4 = [("arc", O, M, N, 46, 1, RED)]
    g5 = [("seg", M, Fp, PUR, 4, None), ("seg", N, E, "#d4a500", 4, None)]
    g6 = [("poly", [O, M, Fp], "rgba(142,36,170,.18)", PUR, 3), ("poly", [O, N, E], "rgba(251,192,45,.20)", "#d4a500", 3), ("tick", M, Fp, 3, PUR), ("tick", N, E, 3, "#d4a500")]
    return geo([g1, g2, g3, g4, g5, g6][:upto], "MF")


def d_iso_split():
    A, B, C, M = (330, 50), (120, 330), (540, 330), (330, 330)
    return geo([
        [("poly", [A, B, C], "rgba(30,136,229,.08)", INK, 5), ("pt", A, "A", 0, -16, INK), ("pt", B, "B", -22, 12, INK), ("pt", C, "C", 22, 12, INK), ("pt", M, "M", 0, 34, INK)],
        [("tick", A, B, 1, GREEN), ("tick", A, C, 1, GREEN), ("seg", A, M, ORG, 4, None)],
        [("tick", B, M, 2, GREEN), ("tick", M, C, 2, GREEN), ("tick", A, M, 3, ORG)],
        [("poly", [A, B, M], "rgba(229,57,53,.15)", RED, 3), ("poly", [A, M, C], "rgba(30,136,229,.18)", BLUE, 3)],
        [("arc", B, A, M, 40, 1, RED), ("arc", C, A, M, 40, 1, RED), ("right", M, A, B, 16, PUR), ("right", M, A, C, 16, PUR)],
    ], "IM")


def d_cross():
    O = (330, 220); A, B, C, D = (130, 120), (530, 320), (130, 330), (530, 110)
    O = (330, 220)
    A, B = (130, 120), (530, 320)   # AB through O
    C, D = (150, 350), (510, 90)    # CD through O
    # make O the true midpoint of both: A+B = 2O, C+D = 2O
    return geo([
        [("seg", A, B, INK, 4, None), ("seg", C, D, INK, 4, None), ("pt", O, "O", 6, -16, INK), ("pt", A, "A", -20, -8, INK), ("pt", B, "B", 20, 22, INK), ("pt", C, "C", -20, 22, INK), ("pt", D, "D", 20, -8, INK)],
        [("tick", A, O, 1, GREEN), ("tick", O, B, 1, GREEN), ("tick", C, O, 2, GREEN), ("tick", O, D, 2, GREEN)],
        [("seg", A, C, ORG, 4, None), ("seg", B, D, ORG, 4, None), ("poly", [O, A, C], "rgba(229,57,53,.15)", RED, 3), ("poly", [O, B, D], "rgba(30,136,229,.18)", BLUE, 3)],
        [("arc", O, A, C, 34, 1, PUR), ("arc", O, B, D, 34, 1, PUR)],
    ], "CR")


# ---------------------------------------------------------------- quiz
QUIZ = [
    {"q": "Triangle ABC has AB = DE, AC = DF and ∠A = ∠D (the angle between the two sides). Which case proves △ABC ≅ △DEF?", "opts": ["SAS", "ASA", "SSS", "AAA"], "a": 0,
     "why": {"ASA": _w("ASA needs one side between two equal angles.", "ASA يحتاج ضلعًا بين زاويتين متساويتين.", "ASA : un côté entre deux angles."),
             "SSS": _w("SSS needs all three pairs of sides.", "SSS يحتاج الأضلاع الثلاثة.", "SSS : trois côtés."),
             "AAA": _w("Equal angles alone never prove equal triangles.", "الزوايا وحدها لا تثبت التطابق.", "Pas un cas d'égalité.")}, "ok": "SAS"},
    {"q": "In an isosceles triangle the base angles are 70°. What is the vertex angle?", "opts": ["40°", "70°", "110°", "20°"], "a": 0,
     "why": {"70°": _w("70 + 70 = 140, the third angle is 180 − 140.", "70 + 70 = 140 والثالثة 180 − 140.", "180 − 140."),
             "110°": _w("110° would give a sum of 250°.", "110° تعطي مجموعًا 250°.", "Somme 250°."),
             "20°": _w("180 − 140 = 40, not 20.", "180 − 140 = 40 لا 20.", "40.")}, "ok": "40°"},
    {"q": "Two triangles have three pairs of equal angles (60°, 60°, 60°). Are they always equal?", "opts": ["No — they can have different sizes", "Yes, always", "Only if they are isosceles", "Only in a rectangle"], "a": 0,
     "why": {"Yes, always": _w("A big and a small equilateral triangle both have 60° angles.", "مثلث متساوي الأضلاع كبير وصغير كلاهما بزوايا 60°.", "Grand et petit triangle équilatéral."),
             "Only if they are isosceles": _w("Size is not fixed by angles.", "الأبعاد لا تحددها الزوايا.", "La taille n'est pas fixée."),
             "Only in a rectangle": _w("Rectangles are not involved.", "لا علاقة للمستطيل.", "Pas de rectangle.")}, "ok": "No — they can have different sizes"},
]

# ---------------------------------------------------------------- theory
THEORY = [
    ("Triangle vocabulary", "مفردات المثلث", "Vocabulaire du triangle", "39", [
        T("Hello, champion! A triangle has three vertices, A, B and C, three sides, AB, BC and AC, and three angles. Look: the side opposite vertex A is BC.",
          "مرحبًا يا بطل! للمثلث ثلاثة رؤوس A وB وC وثلاثة أضلاع AB وBC وAC وثلاث زوايا. انظر: الضلع المقابل للرأس A هو BC.",
          "Un triangle a trois sommets A, B, C, trois côtés et trois angles."),
        d_vocab(),
        T("The three angles of every triangle always add up to 180 degrees. We will use this fact many times to find a missing angle.",
          "مجموع زوايا أي مثلث يساوي دائمًا 180 درجة. سنستعمل هذه الحقيقة مرات كثيرة لإيجاد زاوية ناقصة.",
          "La somme des angles d'un triangle vaut 180°."),
        F("A + B + C = 180°"),
    ]),
    ("Equal (congruent) triangles", "المثلثات المتساوية (المتطابقة)", "Triangles égaux (superposables)", "41", [
        T("Two triangles are equal when one can be placed exactly on top of the other. They have the same shape and the same size. Here ABC and DEF are equal.",
          "يكون المثلثان متساويين (متطابقين) إذا أمكن وضع أحدهما تمامًا فوق الآخر، فلهما الشكل نفسه والحجم نفسه. هنا ABC وDEF متساويان.",
          "Deux triangles sont égaux s'ils se superposent exactement."),
        d_equal(),
        T("We mark equal sides with the same number of small strokes, and equal angles with the same number of arcs. One stroke on AB and DE, two strokes on AC and DF, three on BC and EF.",
          "نعلّم الأضلاع المتساوية بعدد الشرطات نفسه، والزوايا المتساوية بعدد الأقواس نفسه. شرطة واحدة على AB وDE وشرطتان على AC وDF وثلاث على BC وEF.",
          "Même nombre de traits pour des côtés égaux, même nombre d'arcs pour des angles égaux."),
        F("△ABC ≅ △DEF"),
    ]),
    ("Corresponding (homologous) elements", "العناصر المتناظرة", "Éléments homologues", "41", [
        T("When two triangles are equal, the vertices that match are called homologous. A matches D, B matches E and C matches F. We always write the letters in the matching order: ABC and DEF.",
          "عندما يتساوى مثلثان تُسمّى الرؤوس المتناظرة رؤوسًا متماثلة. A تقابل D وB تقابل E وC تقابل F. نكتب الحروف دائمًا بالترتيب المتناظر: ABC وDEF.",
          "A correspond à D, B à E, C à F : on écrit les lettres dans l'ordre."),
        d_homol(),
        T("The sides and angles between matching vertices are equal too: AB = DE, BC = EF, AC = DF, and angle A = angle D, angle B = angle E, angle C = angle F. This is the key use of equal triangles.",
          "والأضلاع والزوايا المحصورة بين رؤوس متناظرة متساوية أيضًا: AB = DE وBC = EF وAC = DF والزاوية A = الزاوية D والزاوية B = E وC = F. وهذا هو الاستعمال الأهم للمثلثات المتساوية.",
          "Côtés et angles homologues sont égaux."),
        F("AB = DE      BC = EF      AC = DF"),
        F("∠A = ∠D      ∠B = ∠E      ∠C = ∠F"),
    ]),
    ("Case 1: ASA", "الحالة الأولى: ASA", "Cas 1 : ASA", "42", [
        T("Case one, ASA: angle, side, angle. If a side and the two angles touching it are equal in both triangles, the triangles are equal. Here BC and DE... look at BC and EF with the angles at B, C and E, F.",
          "الحالة الأولى ASA: زاوية وضلع وزاوية. إذا تساوى ضلع والزاويتان المجاورتان له في المثلثين فالمثلثان متساويان. هنا الضلع BC مع الزاويتين عند B وC يساويان EF مع الزاويتين عند E وF.",
          "ASA : un côté égal et les deux angles adjacents égaux."),
        d_asa(),
        F("BC = EF   ,   ∠B = ∠E   ,   ∠C = ∠F   ⇒   △ABC ≅ △DEF  (ASA)"),
    ]),
    ("Case 2: SAS", "الحالة الثانية: SAS", "Cas 2 : SAS", "42", [
        T("Case two, SAS: side, angle, side. Two sides and the angle between them are equal. Here AB = DE, AC = DF, and the angle at A equals the angle at D. The angle must be between the two sides.",
          "الحالة الثانية SAS: ضلع وزاوية وضلع. ضلعان والزاوية المحصورة بينهما متساوية. هنا AB = DE وAC = DF والزاوية عند A تساوي الزاوية عند D. يجب أن تكون الزاوية محصورة بين الضلعين.",
          "SAS : deux côtés et l'angle compris entre eux."),
        d_sas(),
        F("AB = DE   ,   ∠A = ∠D   ,   AC = DF   ⇒   △ABC ≅ △DEF  (SAS)"),
    ]),
    ("Case 3: SSS", "الحالة الثالثة: SSS", "Cas 3 : SSS", "42", [
        T("Case three, SSS: three pairs of equal sides are enough. We do not even need the angles: the three sides decide the whole triangle.",
          "الحالة الثالثة SSS: تكفي ثلاثة أزواج من الأضلاع المتساوية. لا نحتاج إلى الزوايا فالأضلاع الثلاثة تحدد المثلث كله.",
          "SSS : trois côtés égaux suffisent."),
        d_sss(),
        F("AB = DE   ,   AC = DF   ,   BC = EF   ⇒   △ABC ≅ △DEF  (SSS)"),
    ]),
    ("Why equal angles are not enough", "لماذا لا تكفي الزوايا", "Pourquoi les angles ne suffisent pas", "42", [
        T("Careful! Three pairs of equal angles are not a case of equality. The small and the big triangle here have exactly the same angles, but they are not the same size.",
          "انتبه! ثلاثة أزواج من الزوايا المتساوية ليست حالة تساوٍ. المثلث الصغير والكبير هنا لهما الزوايا نفسها لكنهما مختلفا الحجم.",
          "Trois angles égaux ne prouvent pas l'égalité des triangles."),
        d_aaa(),
        F("equal angles  ⇏  equal triangles"),
    ]),
    ("Construct a triangle with ASA", "ارسم مثلثًا بحالة ASA", "Construire avec ASA", "43", [
        T("Construct a triangle with AB = 4 cm, angle A = 30 degrees and angle B = 45 degrees. First draw AB. Then draw a ray from A at 30 degrees and a ray from B at 45 degrees. Where they cross is C.",
          "ارسم مثلثًا فيه AB = 4 سم والزاوية A = 30° والزاوية B = 45°. نرسم أولًا AB ثم نصف مستقيم من A بزاوية 30° ونصف مستقيم من B بزاوية 45°. نقطة تقاطعهما هي C.",
          "On trace AB = 4 cm, puis deux demi-droites à 30° et 45° : leur intersection est C."),
        d_constr_asa(),
        F("C = 180° − (30° + 45°) = 105°"),
    ]),
    ("Construct a triangle with SAS", "ارسم مثلثًا بحالة SAS", "Construire avec SAS", "43", [
        T("Now sides 4 cm and 3 cm with the angle 45 degrees between them. Draw AB = 4 cm. At A draw a ray at 45 degrees. Measure 3 cm along it to find C. Join B to C.",
          "الآن ضلعان 4 سم و3 سم والزاوية 45° بينهما. نرسم AB = 4 سم وعند A نصف مستقيم بزاوية 45° ونقيس 3 سم عليه فنجد C ثم نصل B بـ C.",
          "AB = 4 cm, angle 45° en A, AC = 3 cm : on joint B et C."),
        d_constr_sas(),
        F("AB = 4 cm   ∠A = 45°   AC = 3 cm"),
    ]),
    ("Construct a triangle with SSS", "ارسم مثلثًا بحالة SSS", "Construire avec SSS", "43", [
        T("A triangle with sides 3, 4 and 5 centimetres. Draw AB = 4 cm. With the compass make an arc of radius 3 cm from A and an arc of radius 5 cm from B. They meet at C. This triangle has a right angle at A.",
          "مثلث أضلاعه 3 و4 و5 سنتيمترات. نرسم AB = 4 سم ثم بالفرجار قوسًا نصف قطره 3 سم من A وقوسًا نصف قطره 5 سم من B فيلتقيان في C. في هذا المثلث زاوية قائمة عند A.",
          "Avec le compas : arc de 3 cm depuis A et arc de 5 cm depuis B."),
        d_constr_sss(),
        F("AB = 4   AC = 3   BC = 5      3² + 4² = 9 + 16 = 25 = 5²"),
    ]),
    ("Calculating angles", "حساب الزوايا", "Calcul d'angles", "44", [
        T("Use the angle sum and equal sides. In an isosceles triangle ABC with AB = AC, the base angles are equal. If each is 70 degrees then angle A = 180 − (70 + 70) = 40 degrees.",
          "نستعمل مجموع الزوايا والأضلاع المتساوية. في مثلث متساوي الساقين ABC فيه AB = AC تتساوى زاويتا القاعدة. إذا كانت كل منهما 70° فإن الزاوية A = 180 − (70 + 70) = 40°.",
          "Triangle isocèle : angles à la base égaux, 70° chacun, donc A = 40°."),
        d_iso(),
        F("A = 180° − (70° + 70°) = 40°"),
    ]),
    ("Proof 1: the rectangle diagonal", "برهان 1: قطر المستطيل", "Démonstration 1 : diagonale du rectangle", "44", [
        T("ABCD is a rectangle and AC is a diagonal. Prove that the triangles ABC and CDA are equal. Opposite sides of a rectangle are equal: AB = DC and BC = AD. The side AC belongs to both triangles.",
          "ABCD مستطيل وAC قطر فيه. أثبت أن المثلثين ABC وCDA متساويان. الأضلاع المتقابلة في المستطيل متساوية: AB = DC وBC = AD. والضلع AC مشترك بين المثلثين.",
          "ABCD rectangle, AC diagonale : AB = DC, BC = AD et AC commun."),
        d_rect(),
        F("AB = DC   ,   BC = AD   ,   AC common   ⇒   △ABC ≅ △CDA  (SSS)"),
        T("Because the triangles are equal, homologous angles are equal: angle B = angle D, and the diagonal splits the rectangle into two equal triangles.",
          "ولأن المثلثين متساويان فالزوايا المتناظرة متساوية: الزاوية B = الزاوية D، والقطر يقسم المستطيل إلى مثلثين متساويين.",
          "Donc ∠B = ∠D : la diagonale partage le rectangle en deux triangles égaux."),
    ]),
    ("Proof 2: MF = NE", "برهان 2: MF = NE", "Démonstration 2 : MF = NE", "49", [
        T("Problem. On the sides of angle O we have OM = ON and ME = NF. The points O, M, E are on one ray and O, N, F are on the other. Prove that MF = NE. First we draw the angle and the points.",
          "مسألة. على ضلعي الزاوية O لدينا OM = ON وME = NF. النقاط O وM وE على نصف مستقيم واحد وO وN وF على الآخر. أثبت أن MF = NE. نرسم أولًا الزاوية والنقاط.",
          "Sur les côtés de l'angle O : OM = ON et ME = NF. Montrer que MF = NE."),
        d_mf(1),
        T("Step 1. The marks show the data: OM = ON with one stroke and ME = NF with two strokes.",
          "الخطوة 1. العلامات تبيّن المعطيات: OM = ON بشرطة واحدة وME = NF بشرطتين.",
          "Étape 1 : les données sont codées sur la figure."),
        T("Step 2. O, M, E are aligned, so OE = OM + ME. In the same way OF = ON + NF.",
          "الخطوة 2. O وM وE على استقامة واحدة فإن OE = OM + ME. وكذلك OF = ON + NF.",
          "Étape 2 : OE = OM + ME et OF = ON + NF."),
        F("OE = OM + ME      OF = ON + NF"),
        T("Step 3. Equal parts added to equal parts give equal wholes: since OM = ON and ME = NF, we conclude that OE = OF.",
          "الخطوة 3. أجزاء متساوية مجموعة إلى أجزاء متساوية تعطي كلًّا متساويًا: بما أن OM = ON وME = NF فإن OE = OF.",
          "Étape 3 : OE = OF."),
        F("OE = OF"),
        T("Step 4. Look at triangles OMF and ONE. They share the angle at O: angle MOF is the same angle as angle NOE.",
          "الخطوة 4. انظر إلى المثلثين OMF وONE. بينهما زاوية مشتركة عند O: الزاوية MOF هي نفسها الزاوية NOE.",
          "Étape 4 : les triangles OMF et ONE ont l'angle en O en commun."),
        d_mf(4),
        T("Step 5. In the triangles OMF and ONE we have two sides and the angle between them: OM = ON, the angle at O is common, and OF = OE.",
          "الخطوة 5. في المثلثين OMF وONE لدينا ضلعان والزاوية المحصورة بينهما: OM = ON والزاوية عند O مشتركة وOF = OE.",
          "Étape 5 : OM = ON, ∠MOF = ∠NOE, OF = OE."),
        d_mf(5),
        F("OM = ON   ;   ∠MOF = ∠NOE   ;   OF = OE"),
        T("Step 6. Therefore the triangles OMF and ONE are equal by the case SAS, and the side MF corresponds to NE. So MF = NE.",
          "الخطوة 6. إذن المثلثان OMF وONE متساويان بحالة SAS والضلع MF يقابل NE. إذن MF = NE.",
          "Étape 6 : par SAS, △OMF ≅ △ONE, donc MF = NE."),
        d_mf(6),
        F("△OMF ≅ △ONE   ⇒   MF = NE"),
    ]),
    ("Error detective", "المحقق", "Détective", "", [
        T("A learner says: AB = DE, BC = EF and angle A = angle D, so the triangles are equal by SAS. Is this right? No! The equal angle A is not between AB and BC. It is not an included angle, so SAS cannot be used. Always check where the angle is.",
          "قال متعلّم: AB = DE وBC = EF والزاوية A = D فالمثلثان متساويان بحالة SAS. هل هذا صحيح؟ لا! الزاوية A ليست محصورة بين AB وBC فلا يمكن استعمال SAS. تحقق دائمًا من موقع الزاوية.",
          "Erreur : l'angle égal n'est pas compris entre les deux côtés."),
        F("SAS needs the angle BETWEEN the two sides"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "45", [
        T("Two triangles are equal when they can be superposed. Three cases prove it: ASA, SAS and SSS. Equal triangles have equal homologous sides and angles. Equal angles alone are not enough. Use the cases to prove that segments or angles are equal.",
          "يتساوى مثلثان إذا أمكن تطابقهما. ثلاث حالات تثبت ذلك: ASA وSAS وSSS. والمثلثان المتساويان لهما أضلاع وزوايا متناظرة متساوية. الزوايا وحدها لا تكفي. نستعمل الحالات لنثبت تساوي قطع أو زوايا.",
          "Trois cas : ASA, SAS, SSS. Les éléments homologues sont égaux."),
        F("ASA      SAS      SSS"),
    ]),
]


def _ex(n, en, ar, fr, steps):
    return EX(n, "", st(en, ar, fr), steps)


EXERCISES = [
    _ex("1", "Triangles ABC and DEF: AB = DE = 5 cm, BC = EF = 7 cm and ∠B = ∠E = 50°. Which case proves they are equal?", "المثلثان ABC وDEF: AB = DE = 5 سم وBC = EF = 7 سم و∠B = ∠E = 50°. أي حالة تثبت تساويهما؟", "AB = DE = 5, BC = EF = 7, ∠B = ∠E = 50°. Quel cas ?",
        [T("The angle B is between the sides AB and BC, and E is between DE and EF. Two sides and the included angle: case SAS. Then AC = DF and ∠A = ∠D, ∠C = ∠F.", "الزاوية B محصورة بين AB وBC وE بين DE وEF. ضلعان والزاوية المحصورة: حالة SAS. ومنه AC = DF و∠A = ∠D و∠C = ∠F.", "SAS."), F("△ABC ≅ △DEF  (SAS)")]),
    _ex("2", "∠A = ∠D = 40°, ∠B = ∠E = 65°, AB = DE = 6 cm. Which case? Find ∠C and ∠F.", "∠A = ∠D = 40° و∠B = ∠E = 65° وAB = DE = 6 سم. أي حالة؟ جد ∠C و∠F.", "∠A = ∠D = 40°, ∠B = ∠E = 65°, AB = DE = 6. Quel cas ? ∠C, ∠F ?",
        [T("The side AB lies between the angles A and B, and DE between D and E: case ASA. The third angle: C = 180 − (40 + 65) = 75°, and F = C = 75° because homologous angles are equal.", "الضلع AB بين الزاويتين A وB وDE بين D وE: حالة ASA. الزاوية الثالثة C = 180 − (40 + 65) = 75° وF = C = 75° لأن الزوايا المتناظرة متساوية.", "ASA ; C = F = 75°."), F("C = 180° − 105° = 75°      F = 75°")]),
    _ex("3", "△ABC has AB = 3, BC = 4, CA = 5 cm. △DEF has DE = 5, EF = 3, FD = 4 cm. Are they equal? Write the correct order of letters.", "في △ABC: AB = 3 وBC = 4 وCA = 5 سم. وفي △DEF: DE = 5 وEF = 3 وFD = 4 سم. هل هما متساويان؟ اكتب ترتيب الحروف الصحيح.", "△ABC : 3, 4, 5. △DEF : DE = 5, EF = 3, FD = 4. Égaux ? Ordre des lettres ?",
        [T("The sides are 3, 4, 5 in both: case SSS. Match equal sides: AB = EF = 3 so A, B match E, F; BC = FD = 4 so B matches F and C matches D; CA = DE = 5 so C matches D and A matches E. The triangles are equal and △ABC ≅ △EFD.", "الأضلاع 3 و4 و5 في كليهما: حالة SSS. نقابل الأضلاع المتساوية: AB = EF = 3 وBC = FD = 4 وCA = DE = 5. إذن A تقابل E وB تقابل F وC تقابل D فيكون △ABC ≅ △EFD.", "SSS ; △ABC ≅ △EFD."), F("A↔E   B↔F   C↔D      △ABC ≅ △EFD")]),
    _ex("4", "In isosceles △ABC (AB = AC) the vertex angle A = 50°. Find the base angles.", "في مثلث متساوي الساقين ABC (AB = AC) الزاوية A = 50°. جد زاويتي القاعدة.", "△ABC isocèle (AB = AC), ∠A = 50°. Angles de base ?",
        [T("The base angles are equal and the three angles add up to 180°. B + C = 180 − 50 = 130, so each is 130 ÷ 2 = 65°. Check: 50 + 65 + 65 = 180 ✓.", "زاويتا القاعدة متساويتان ومجموع الزوايا 180°. B + C = 180 − 50 = 130 فكل منهما 130 ÷ 2 = 65°. تحقق: 50 + 65 + 65 = 180 ✓.", "65° chacun."), F("B = C = (180° − 50°) ÷ 2 = 65°")]),
    _ex("5", "△ABC ≅ △DEF, ∠A = 80° and ∠B = 45°. Find ∠F.", "△ABC ≅ △DEF و∠A = 80° و∠B = 45°. جد ∠F.", "△ABC ≅ △DEF, ∠A = 80°, ∠B = 45°. ∠F ?",
        [T("In △ABC, C = 180 − (80 + 45) = 55°. Homologous angles are equal and C matches F, so F = 55°.", "في △ABC: C = 180 − (80 + 45) = 55°. الزوايا المتناظرة متساوية وC تقابل F إذن F = 55°.", "55°."), F("∠F = ∠C = 55°")]),
    _ex("6", "△ABC ≅ △DEF, AB = 4, BC = 6, AC = 7. Find the perimeter of DEF and the length DF.", "△ABC ≅ △DEF وAB = 4 وBC = 6 وAC = 7. جد محيط DEF وطول DF.", "△ABC ≅ △DEF, AB = 4, BC = 6, AC = 7. Périmètre de DEF, DF ?",
        [T("Equal triangles have equal sides: DE = 4, EF = 6, DF = AC = 7. Perimeter 4 + 6 + 7 = 17.", "المثلثان المتساويان أضلاعهما متساوية: DE = 4 وEF = 6 وDF = AC = 7. المحيط 4 + 6 + 7 = 17.", "DF = 7 ; 17."), F("DF = 7      perimeter = 17")]),
    _ex("7", "Construct △ABC with AB = 4 cm, ∠A = 30°, ∠B = 45°. Find ∠C and estimate AC and BC.", "ارسم △ABC فيه AB = 4 سم و∠A = 30° و∠B = 45°. جد ∠C وقدّر AC وBC.", "Construis △ABC : AB = 4 cm, ∠A = 30°, ∠B = 45°. ∠C, AC, BC ?",
        [T("C = 180 − 75 = 105°. After drawing, measure: AC is about 2.9 cm and BC about 2.1 cm. Any other triangle with the same data is equal to it (ASA).", "C = 180 − 75 = 105°. بعد الرسم نقيس: AC ≈ 2.9 سم وBC ≈ 2.1 سم. وأي مثلث آخر له المعطيات نفسها يساويه (ASA).", "C = 105°, AC ≈ 2,9 cm, BC ≈ 2,1 cm."), d_constr_asa(), F("C = 105°      AC ≈ 2.9 cm      BC ≈ 2.1 cm")]),
    _ex("8", "Construct △ABC with AB = 4 cm, AC = 3 cm, ∠A = 45°, then measure BC.", "ارسم △ABC فيه AB = 4 سم وAC = 3 سم و∠A = 45° ثم قِس BC.", "Construis △ABC : AB = 4, AC = 3, ∠A = 45°. Mesure BC.",
        [T("SAS construction: BC measures about 2.8 cm. Anyone who follows these three data gets an equal triangle.", "رسم بحالة SAS: يقيس BC نحو 2.8 سم. وكل من يتبع المعطيات الثلاثة يحصل على مثلث مساوٍ.", "BC ≈ 2,8 cm."), d_constr_sas(), F("BC ≈ 2.8 cm")]),
    _ex("9", "Two triangles have angles 60°, 60°, 60° (sides 3 cm and 5 cm). Are they equal?", "مثلثان زواياهما 60° و60° و60° (أضلاع أحدهما 3 سم والآخر 5 سم). هل هما متساويان؟", "Deux triangles aux angles 60°, 60°, 60° (côtés 3 cm et 5 cm). Égaux ?",
        [T("No. They have the same shape but different sizes: 3 cm is not 5 cm. Equal angles are not a case of equality.", "لا. لهما الشكل نفسه لكن حجمين مختلفين: 3 سم لا تساوي 5 سم. تساوي الزوايا ليس حالة تساوٍ.", "Non, tailles différentes."), d_aaa(), F("AAA is not a case")]),
    _ex("10", "ABC is isosceles (AB = AC) and M is the midpoint of BC. Prove that ∠B = ∠C.", "ABC متساوي الساقين (AB = AC) وM منتصف BC. أثبت أن ∠B = ∠C.", "ABC isocèle (AB = AC), M milieu de BC. Montrer que ∠B = ∠C.",
        [T("Compare △ABM and △ACM. AB = AC (given). BM = MC (M is the midpoint). AM is common. Three pairs of equal sides: SSS.", "نقارن △ABM و△ACM. AB = AC (معطى) وBM = MC (M المنتصف) وAM مشترك. ثلاثة أزواج من الأضلاع: SSS.", "SSS : AB = AC, BM = MC, AM commun."), d_iso_split(), T("So △ABM ≅ △ACM and homologous angles are equal: ∠B = ∠C.", "إذن △ABM ≅ △ACM والزوايا المتناظرة متساوية: ∠B = ∠C.", "Donc ∠B = ∠C."), F("△ABM ≅ △ACM  (SSS)   ⇒   ∠B = ∠C")]),
    _ex("11", "In the same figure prove that AM is perpendicular to BC.", "في الشكل نفسه أثبت أن AM عمودي على BC.", "Dans la même figure, montrer que AM ⟂ BC.",
        [T("From the equal triangles, ∠AMB = ∠AMC. These two angles are next to each other on the line BC, so they add up to 180°. Each is 180 ÷ 2 = 90°. So AM ⟂ BC.", "من تساوي المثلثين ∠AMB = ∠AMC. وهاتان الزاويتان متجاورتان على المستقيم BC فمجموعهما 180°. كل منهما 180 ÷ 2 = 90°. إذن AM ⟂ BC.", "Angles égaux de somme 180° : 90°."), d_iso_split(), F("∠AMB = ∠AMC,  ∠AMB + ∠AMC = 180°  ⇒  90° each")]),
    _ex("12", "Segments AB and CD cross at O, the midpoint of both. Prove that AC = BD.", "القطعتان AB وCD تتقاطعان في O منتصف كل منهما. أثبت أن AC = BD.", "AB et CD se coupent en O, milieu de chacun. Montrer que AC = BD.",
        [T("Compare △OAC and △OBD. OA = OB and OC = OD (O is the midpoint of both). The angles AOC and BOD are vertical angles, so they are equal. Two sides and the included angle: SAS.", "نقارن △OAC و△OBD. OA = OB وOC = OD (O منتصف كل منهما). والزاويتان AOC وBOD متقابلتان بالرأس فهما متساويتان. ضلعان والزاوية المحصورة: SAS.", "OA = OB, OC = OD, angles opposés par le sommet : SAS."), d_cross(), T("So △OAC ≅ △OBD, and the homologous sides AC and BD are equal.", "إذن △OAC ≅ △OBD والضلعان المتناظران AC وBD متساويان.", "Donc AC = BD."), F("△OAC ≅ △OBD  (SAS)   ⇒   AC = BD")]),
    _ex("13", "Error detective: 'AB = DE, AC = DF and ∠B = ∠E, so the triangles are equal.' Why is it wrong?", "المحقق: «AB = DE وAC = DF و∠B = ∠E إذن المثلثان متساويان». لماذا هذا خطأ؟", "Détective : AB = DE, AC = DF, ∠B = ∠E donc égaux ?",
        [T("The equal angle B is not between the equal sides AB and AC (it is opposite AC). The angle must be included between the two sides for SAS. So we cannot conclude.", "الزاوية B ليست محصورة بين الضلعين AB وAC بل تقابل AC. يجب أن تكون الزاوية محصورة بين الضلعين في SAS. لذلك لا نستطيع الاستنتاج.", "L'angle n'est pas compris entre les deux côtés."), F("not SAS")]),
    _ex("14", "Rectangle ABCD with diagonals AC and BD crossing at O. Which triangles are equal to △ABC?", "المستطيل ABCD قطراه AC وBD يتقاطعان في O. أي المثلثات تساوي △ABC؟", "Rectangle ABCD, diagonales AC et BD. Quels triangles égaux à △ABC ?",
        [T("The diagonal AC cuts the rectangle into two equal triangles ABC and CDA (SSS, as in the lesson). In the same way BD gives ABD ≅ CDB, and ABC ≅ BAD because AB is common, BC = AD and the right angles at B and A are equal (SAS).", "القطر AC يقسم المستطيل إلى مثلثين متساويين ABC وCDA (SSS كما في الدرس). وكذلك BD يعطي ABD ≅ CDB. وABC ≅ BAD لأن AB مشترك وBC = AD والزاويتين القائمتين عند B وA متساويتان (SAS).", "△CDA, △BAD."), d_rect(), F("△ABC ≅ △CDA ≅ △BAD")]),
]
