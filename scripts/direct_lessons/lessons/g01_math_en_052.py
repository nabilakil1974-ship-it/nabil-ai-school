"""Grade 1 Mathematics — Symmetry."""
from scripts.direct_lessons.common import T, F, EX, st, scene

AX = 330  # axis x
HALVES = {  # left half points (x < AX), listed top→bottom along the outline
    "house": [(AX, 40), (200, 120), (200, 250), (AX, 250)],
    "tree": [(AX, 40), (230, 130), (270, 130), (210, 200), (300, 200), (300, 260), (AX, 260)],
    "heart": [(AX, 90), (260, 40), (200, 70), (200, 130), (AX, 260)],
    "arrow": [(AX, 40), (230, 130), (290, 130), (290, 250), (AX, 250)],
}


def sym(kind, show="full", line=True, tag="Y", skew=False):
    """show: full | half (only the left half) | pair (left half + mirrored half in a lighter colour)."""
    left = HALVES[kind]
    right = [(2 * AX - x, y) for x, y in reversed(left)]
    svg, ids = "", []
    def pg(pid, pts, fill, op=1.0):
        return f'<polygon id="{pid}" points="{" ".join(f"{x},{y}" for x, y in pts)}" fill="{fill}" fill-opacity="{op}" stroke="#0b3d5c" stroke-width="4" stroke-linejoin="round"/>'
    if show == "full":
        pts = left + right
        if skew:
            pts = [(x + (y - 150) * 0.35, y) for x, y in pts]
        svg += pg(tag + "0", pts, "#ffb74d")
        ids.append(tag + "0")
    else:
        svg += pg(tag + "0", left + [(AX, left[0][1])], "#ffb74d")
        ids.append(tag + "0")
        if show == "pair":
            svg += pg(tag + "1", [(2 * AX - x, y) for x, y in left] + [(AX, left[0][1])], "#4fc3f7", 0.9)
            ids.append(tag + "1")
    if line:
        svg += f'<line id="{tag}L" x1="{AX}" y1="20" x2="{AX}" y2="280" stroke="#e53935" stroke-width="4" stroke-dasharray="10 8"/>'
        ids.append(tag + "L")
    return scene(svg, ids)


LESSON_ID = "G01-MATH-EN-052"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Symmetry", "ar": "التناظر", "fr": "La symétrie"}

THEORY = [
    ("Two matching halves", "نصفان متطابقان", "Deux moitiés identiques", "130", [
        sym("house", "full"),
        T("Hello, champion! Look at this house. If we fold it along the red dashed line, the left part falls exactly on the right part. We say the house is symmetric, and the red line is its line of symmetry.",
          "مرحبًا يا بطل! انظر إلى هذا البيت. إذا طويناه على الخط الأحمر المتقطع ينطبق الجزء الأيسر تمامًا على الجزء الأيمن. نقول إن البيت متناظر، والخط الأحمر هو محور التناظر.",
          "Regarde cette maison. Si on la plie le long du trait rouge pointillé, la partie gauche tombe exactement sur la partie droite. On dit que la maison est symétrique, et le trait rouge est son axe de symétrie."),
    ]),
    ("Complete the other half", "نكمل النصف الآخر", "Compléter l'autre moitié", "130", [
        sym("tree", "half"),
        T("Here only the left half of a tree is drawn. Every point on the left has a matching point on the right at the same distance from the line, on the opposite side. We draw the other half so that folding makes them coincide.",
          "هنا مرسوم النصف الأيسر فقط من شجرة. لكل نقطة على اليسار نقطة مقابلة على اليمين على البعد نفسه من الخط في الجهة المعاكسة. نرسم النصف الآخر بحيث ينطبق النصفان عند الطي.",
          "Seule la moitié gauche d'un arbre est dessinée. Chaque point à gauche a un point correspondant à droite, à la même distance de la ligne, de l'autre côté. On dessine l'autre moitié pour que le pli les fasse coïncider."),
        sym("tree", "pair"),
    ]),
    ("A figure that is not symmetric", "شكل غير متناظر", "Une figure non symétrique", "131", [
        sym("arrow", "full", skew=True),
        T("This arrow is leaning. If we fold it on the line, the two parts do not cover each other: one side sticks out. So it is not symmetric about this line. We check symmetry by folding, not only by looking.",
          "هذا السهم مائل. إذا طويناه على الخط لا ينطبق الجزءان: أحد الجانبين يبرز. إذن ليس متناظرًا حول هذا الخط. نتحقق من التناظر بالطي لا بالنظر فقط.",
          "Cette flèche est penchée. Si on plie sur la ligne, les deux parties ne se recouvrent pas : un côté dépasse. Elle n'est pas symétrique par rapport à cette ligne. On vérifie en pliant, pas seulement à l'œil."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("A symmetric figure has matching parts on both sides of a line. Each point has a partner at the same distance on the other side. Folding along the line makes the two parts coincide.",
          "الشكل المتناظر له جزآن متطابقان على جانبي خط. لكل نقطة شريكة على البعد نفسه في الجهة الأخرى. والطي على الخط يجعل الجزأين ينطبقان.",
          "Une figure symétrique a deux parties identiques de part et d'autre d'une ligne. Chaque point a un partenaire à la même distance de l'autre côté. Le pli sur la ligne fait coïncider les deux parties."),
        F("MATCHING PARTS → SAME DISTANCE → FOLD TO CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "130", st("Is the house symmetric about the red line?", "هل البيت متناظر حول الخط الأحمر؟", "La maison est-elle symétrique par rapport au trait rouge ?"), [
        sym("house", "full"),
        T("Yes. Folded on the line, the two halves coincide.", "نعم. عند الطي على الخط ينطبق النصفان.", "Oui. Pliées sur la ligne, les deux moitiés coïncident."),
    ]),
    EX("2", "130", st("Complete the heart.", "أكمل القلب.", "Complète le cœur."), [
        sym("heart", "half"),
        sym("heart", "pair"),
        T("Draw the mirror half on the right, at the same distances from the line.", "نرسم النصف المقابل على اليمين على الأبعاد نفسها من الخط.", "On dessine la moitié miroir à droite, aux mêmes distances de la ligne."),
    ]),
    EX("3", "130", st("Complete the tree.", "أكمل الشجرة.", "Complète l'arbre."), [
        sym("tree", "half"),
        sym("tree", "full"),
    ]),
    EX("4", "131", st("Is the leaning arrow symmetric about the line?", "هل السهم المائل متناظر حول الخط؟", "La flèche penchée est-elle symétrique par rapport à la ligne ?"), [
        sym("arrow", "full", skew=True),
        T("No. When we fold, one side sticks out.", "لا. عند الطي يبرز أحد الجانبين.", "Non. En pliant, un côté dépasse."),
    ]),
    EX("5", "131", st("Is this straight arrow symmetric?", "هل هذا السهم المستقيم متناظر؟", "Cette flèche droite est-elle symétrique ?"), [
        sym("arrow", "full"),
        T("Yes. Both halves match.", "نعم. النصفان متطابقان.", "Oui. Les deux moitiés correspondent."),
    ]),
    EX("6", "131", st("Error check: a child draws the other half of the tree closer to the line. Is it symmetric?", "تحقّق من الخطأ: رسم طفل النصف الآخر من الشجرة أقرب إلى الخط. هل هو متناظر؟", "Vérifie l'erreur : un enfant dessine l'autre moitié plus près de la ligne. Est-ce symétrique ?"), [
        sym("tree", "pair"),
        T("No. Matching points must be at the same distance from the line on both sides.", "لا. يجب أن تكون النقاط المتقابلة على البعد نفسه من الخط في الجهتين.", "Non. Les points correspondants doivent être à la même distance de la ligne de chaque côté."),
    ]),
    EX("7", "131", st("Challenge: draw the second half of the arrow.", "تحدٍّ: ارسم النصف الثاني من السهم.", "Défi : dessine la seconde moitié de la flèche."), [
        sym("arrow", "half"),
        sym("arrow", "pair"),
    ]),
    EX("8", "131", st("Final check: complete the house and verify by folding.", "تقييم أخير: أكمل البيت وتحقّق بالطي.", "Évaluation : complète la maison et vérifie par pliage."), [
        sym("house", "half"),
        sym("house", "pair"),
        T("Folding on the red line, the blue half falls on the orange half. The house is symmetric.", "عند الطي على الخط الأحمر يقع النصف الأزرق على النصف البرتقالي. البيت متناظر.", "En pliant sur la ligne rouge, la moitié bleue tombe sur l'orange. La maison est symétrique."),
    ]),
]
