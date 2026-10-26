"""Grade 1 Mathematics — Reproduction of figures."""
from scripts.direct_lessons.common import T, F, EX, st, scene

HOUSE = [(1, 4), (1, 2), (3, 2), (3, 4), (2, 5), (1, 4), (3, 4)]
STAIR = [(0, 4), (0, 3), (1, 3), (1, 2), (2, 2), (2, 1), (3, 1), (3, 4), (0, 4)]
ARROW = [(1, 5), (1, 3), (0, 3), (2, 1), (4, 3), (3, 3), (3, 5), (1, 5)]
SQUARE = [(1, 1), (4, 1), (4, 4), (1, 4), (1, 1)]


def grid(model=None, copy=None, tag="G", dots=True, mark=False, upto=None):
    """Dot grid 6x6. `model` drawn in orange, `copy` in blue (side by side if both)."""
    cell, ox, oy = 42, 40, 30
    panels = [("model", model, "#f57c00")] if copy is None else [("model", model, "#f57c00"), ("copy", copy, "#1e63d6")]
    svg, ids = "", []
    for pi, (nm, pts, col) in enumerate(panels):
        px = ox + pi * 310
        d = ""
        for i in range(6):
            for j in range(6):
                d += f'<circle cx="{px + i*cell}" cy="{oy + j*cell}" r="4" fill="#78909c"/>'
        svg += f'<g id="{tag}d{pi}">{d}</g>'
        ids.append(f"{tag}d{pi}")
        if pts:
            seq = pts if upto is None or pi == 0 else pts[:upto]
            poly = " ".join(f"{px + x*cell},{oy + (5 - y)*cell}" for x, y in seq)
            svg += f'<polyline id="{tag}p{pi}" points="{poly}" fill="none" stroke="{col}" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"/>'
            ids.append(f"{tag}p{pi}")
            if mark:
                m = "".join(f'<circle cx="{px + x*cell}" cy="{oy + (5 - y)*cell}" r="9" fill="#e53935"/>' for x, y in seq)
                svg += f'<g id="{tag}m{pi}">{m}</g>'
                ids.append(f"{tag}m{pi}")
    return scene(svg, ids)


LESSON_ID = "G01-MATH-EN-060"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Reproduction of figures", "ar": "إعادة رسم الأشكال", "fr": "Reproduction de figures"}

THEORY = [
    ("Observe before drawing", "نلاحظ قبل أن نرسم", "Observer avant de dessiner", "154", [
        grid(HOUSE, mark=True),
        T("Hello, champion! We want to draw a second figure exactly like this house. First we look carefully: what shapes do we see, where are the corners, and which dots do the lines join? The red dots are our reference points.",
          "مرحبًا يا بطل! نريد أن نرسم شكلًا ثانيًا مطابقًا تمامًا لهذا البيت. أولًا ننظر بانتباه: أيّ أشكال نرى، وأين الزوايا، وأيّ نقاط تصل بينها الخطوط؟ النقاط الحمراء هي نقاط مرجعنا.",
          "On veut dessiner une seconde figure exactement comme cette maison. D'abord on observe : quelles formes, où sont les coins, quels points les traits relient-ils ? Les points rouges sont nos repères."),
    ]),
    ("Copy one segment at a time", "ننسخ قطعة بعد قطعة", "Copier un segment à la fois", "154", [
        grid(HOUSE, HOUSE, upto=3),
        T("We copy from one reference point to the next, keeping the same direction and the same length. Left: the model. Right: our copy so far. Next we continue to the following dot.",
          "ننسخ من نقطة مرجعية إلى التي تليها مع الحفاظ على الاتجاه نفسه والطول نفسه. على اليسار النموذج وعلى اليمين نسختنا حتى الآن. ثم نكمل إلى النقطة التالية.",
          "On copie d'un repère au suivant, en gardant la même direction et la même longueur. À gauche : le modèle. À droite : notre copie jusqu'ici. On continue vers le point suivant."),
        grid(HOUSE, HOUSE),
    ]),
    ("Compare the copy with the model", "نقارن النسخة بالنموذج", "Comparer la copie au modèle", "155", [
        grid(STAIR, STAIR),
        T("When we finish, we compare. Are all the corners at the same dots? Are all lines in the same direction? If one point is wrong, we correct that first point and do not redraw everything.",
          "عندما ننتهي نقارن. هل كل الزوايا عند النقاط نفسها؟ وهل كل الخطوط في الاتجاه نفسه؟ إذا كانت نقطة خاطئة نصحّح تلك النقطة أولًا ولا نعيد رسم كل شيء.",
          "Quand on a fini, on compare. Tous les coins sont-ils aux mêmes points ? Tous les traits ont-ils la même direction ? S'il y a une erreur, on corrige d'abord ce point, sans tout redessiner."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("To reproduce a figure: observe the parts and reference points, draw one segment at a time, then compare with the model and correct the first mismatch.",
          "لإعادة رسم شكل: نلاحظ الأجزاء والنقاط المرجعية ونرسم قطعة قطعة ثم نقارن بالنموذج ونصحّح أول خطأ.",
          "Pour reproduire une figure : observer les parties et les repères, tracer segment par segment, comparer au modèle et corriger la première erreur."),
        F("OBSERVE → REFERENCE POINTS → DRAW → COMPARE → CORRECT"),
    ]),
]

EXERCISES = [
    EX("1", "154", st("Look at the model: which dots are the corners?", "انظر إلى النموذج: أيّ النقاط هي الزوايا؟", "Regarde le modèle : quels points sont les coins ?"), [
        grid(SQUARE, mark=True),
        T("The 4 red dots are the corners of the square.", "النقاط الحمراء الأربع هي زوايا المربع.", "Les 4 points rouges sont les coins du carré."),
    ]),
    EX("2", "154", st("Copy the square on the second grid.", "انسخ المربع على الشبكة الثانية.", "Copie le carré sur la seconde grille."), [
        grid(SQUARE, SQUARE),
        T("Same four dots, same four sides.", "النقاط الأربع نفسها والأضلاع الأربعة نفسها.", "Mêmes quatre points, mêmes quatre côtés."),
    ]),
    EX("3", "155", st("Copy the house.", "انسخ البيت.", "Copie la maison."), [
        grid(HOUSE, HOUSE),
    ]),
    EX("4", "155", st("Copy the staircase.", "انسخ الدرج.", "Copie l'escalier."), [
        grid(STAIR, STAIR),
    ]),
    EX("5", "156", st("Copy the arrow.", "انسخ السهم.", "Copie la flèche."), [
        grid(ARROW, ARROW),
    ]),
    EX("6", "156", st("Error check: the copy of the house has its roof one dot too low. What do we do?", "تحقّق من الخطأ: نسخة البيت سقفها أخفض بنقطة. ماذا نفعل؟", "Vérifie l'erreur : dans la copie de la maison, le toit est un point trop bas. Que fait-on ?"), [
        grid(HOUSE, [(1, 4), (1, 2), (3, 2), (3, 4), (2, 4), (1, 4), (3, 4)]),
        T("We compare point by point and find the first mismatch: the roof tip. We move only that point up one dot.", "نقارن نقطة نقطة فنجد أول اختلاف: رأس السقف. نرفع تلك النقطة فقط بمقدار نقطة.", "On compare point par point : la première erreur est le sommet du toit. On remonte seulement ce point d'un cran."),
    ]),
    EX("7", "157", st("Challenge: say which reference points the arrow uses.", "تحدٍّ: قل أيّ نقاط مرجعية يستعملها السهم.", "Défi : dis quels repères la flèche utilise."), [
        grid(ARROW, mark=True),
        T("The arrow has 7 corners; the red dots show them all.", "للسهم 7 زوايا والنقاط الحمراء تُظهرها كلها.", "La flèche a 7 coins ; les points rouges les montrent tous."),
    ]),
    EX("8", "157", st("Final check: copy the house and name the reference points.", "تقييم أخير: انسخ البيت وسمِّ النقاط المرجعية.", "Évaluation : copie la maison et nomme les repères."), [
        grid(HOUSE, HOUSE, mark=True),
        T("Reference points: the four corners of the walls and the tip of the roof.", "النقاط المرجعية: زوايا الجدران الأربع ورأس السقف.", "Repères : les quatre coins des murs et le sommet du toit."),
    ]),
]
