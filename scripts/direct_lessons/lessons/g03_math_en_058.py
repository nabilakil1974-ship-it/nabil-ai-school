"""Grade 3 Mathematics — Reproduction of Figures (from the teacher plan)."""
from scripts.direct_lessons.common import T, F, EX, st, scene

LESSON_ID = "G03-MATH-EN-058"
GRADE = 3
SUBJECT = "math"
TITLES = {"en": "Reproduction of Figures", "ar": "إعادة رسم الأشكال", "fr": "Reproduction de figures"}


def grid(pts, close=True, tag="G", upto=None):
    """12x7 grid with a polygon through lattice points (col,row)."""
    s, x0, y0 = 46, 40, 20
    svg = f'<g id="{tag}g">'
    for i in range(13):
        svg += f'<line x1="{x0+i*s}" y1="{y0}" x2="{x0+i*s}" y2="{y0+7*s}" stroke="#cfd8dc" stroke-width="2"/>'
    for j in range(8):
        svg += f'<line x1="{x0}" y1="{y0+j*s}" x2="{x0+12*s}" y2="{y0+j*s}" stroke="#cfd8dc" stroke-width="2"/>'
    svg += '</g>'
    ids = [tag + "g"]
    P = [(x0 + c * s, y0 + r * s) for c, r in pts]
    n = len(P) if upto is None else upto
    for i in range(1, n):
        svg += f'<g id="{tag}l{i}"><line x1="{P[i-1][0]}" y1="{P[i-1][1]}" x2="{P[i][0]}" y2="{P[i][1]}" stroke="#e53935" stroke-width="6" stroke-linecap="round"/></g>'
        ids.append(f"{tag}l{i}")
    if close and n == len(P):
        svg += f'<g id="{tag}lc"><line x1="{P[-1][0]}" y1="{P[-1][1]}" x2="{P[0][0]}" y2="{P[0][1]}" stroke="#e53935" stroke-width="6" stroke-linecap="round"/></g>'
        ids.append(tag + "lc")
    for i in range(n):
        svg += f'<g id="{tag}p{i}"><circle cx="{P[i][0]}" cy="{P[i][1]}" r="9" fill="#1e88e5"/></g>'
        ids.append(f"{tag}p{i}")
    return scene(svg, ids)


FIG = [(2, 1), (6, 1), (6, 4), (2, 4)]
TRI = [(8, 6), (11, 2), (11, 6)]

THEORY = [
    ("What must stay the same", "ما الذي يجب أن يبقى ثابتًا", "Ce qui doit rester identique", "122", [
        T("Hello, champion! To reproduce a figure faithfully we keep its points, lengths, directions and relationships. Looking roughly alike is not enough. Here the rectangle is 4 squares wide and 3 squares high.",
          "مرحبًا يا بطل! لنعيد رسم شكل بأمانة نحافظ على نقاطه وأطوالـه واتجاهاته وعلاقاته. التشابه التقريبي لا يكفي. هذا المستطيل عرضه 4 مربعات وارتفاعه 3.",
          "Une reproduction fidèle garde points, longueurs, directions, relations. Ce rectangle : 4 carreaux sur 3."),
        grid(FIG),
    ]),
    ("Reproduce step by step", "نعيد الرسم خطوة خطوة", "Reproduire pas à pas", "122", [
        T("Find the landmark points on the grid, mark them, then join them in order. Count squares for each length.",
          "نحدّد النقاط المرجعية على الشبكة ونعلّمها ثم نصلها بالترتيب. نعدّ المربعات لكل طول.",
          "Repérer les points, les marquer, les relier dans l'ordre."),
        grid(FIG, upto=2), grid(FIG),
    ]),
    ("Compare and correct", "نقارن ونصحّح", "Comparer et corriger", "123", [
        T("Place the copy over the original, find the first mismatch in position, length or direction, and fix it. The right triangle below has a vertical side of 4 and a horizontal side of 3.",
          "نضع النسخة فوق الأصل ونجد أول اختلاف في الموضع أو الطول أو الاتجاه ونصحّحه. في المثلث القائم أدناه ضلع عمودي 4 وأفقي 3.",
          "On superpose, on trouve le premier écart, on corrige."),
        grid(TRI),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Landmarks, construct in order, keep the relationships, compare, correct.", "نقاط مرجعية، بناء بالترتيب، حفظ العلاقات، مقارنة، تصحيح.", "Repères, ordre, relations, comparaison, correction."),
        F("LANDMARKS → ORDER → KEEP RELATIONS → COMPARE → CORRECT"),
    ]),
]

EXERCISES = [
    EX("1", "122", st("Reproduce the rectangle: how many squares wide and high?", "أعد رسم المستطيل: كم مربعًا عرضه وارتفاعه؟", "Reproduis le rectangle : largeur et hauteur ?"), [grid(FIG), F("4 wide, 3 high")]),
    EX("2", "123", st("Reproduce the triangle: name its two perpendicular sides.", "أعد رسم المثلث وسمِّ ضلعيه المتعامدين.", "Reproduis le triangle : côtés perpendiculaires."), [grid(TRI), F("vertical side 4, horizontal side 3")]),
    EX("3", "123", st("Name one relationship that must be preserved.", "اذكر علاقة هندسية يجب حفظها.", "Une relation à conserver."), [T("For example: the sides are perpendicular, or two sides have equal length.", "مثلًا: الضلعان متعامدان أو لضلعين الطول نفسه.", "Par exemple : côtés perpendiculaires.")]),
]
