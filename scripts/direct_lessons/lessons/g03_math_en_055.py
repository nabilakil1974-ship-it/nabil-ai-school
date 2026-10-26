"""Grade 3 Mathematics — Symmetry (from the teacher plan; book figures are not reproduced)."""
from scripts.direct_lessons.common import T, F, EX, st, scene

LESSON_ID = "G03-MATH-EN-055"
GRADE = 3
SUBJECT = "math"
TITLES = {"en": "Symmetry", "ar": "التناظر", "fr": "La symétrie"}


def sym(pts=((120, 90), (200, 150), (150, 250)), tag="S", pair=True):
    """Points on the left of a vertical axis x=330 and (optionally) their mirror images at equal distance."""
    svg = f'<g id="{tag}a"><line x1="330" y1="30" x2="330" y2="320" stroke="#e53935" stroke-width="5" stroke-dasharray="14 8"/></g>'
    ids = [tag + "a"]
    for i, (x, y) in enumerate(pts):
        svg += f'<g id="{tag}p{i}"><circle cx="{x}" cy="{y}" r="12" fill="#1e88e5"/></g>'
        ids.append(f"{tag}p{i}")
        if pair:
            mx = 660 - x
            svg += (f'<g id="{tag}m{i}"><line x1="{x}" y1="{y}" x2="{mx}" y2="{y}" stroke="#90a4ae" stroke-width="2" stroke-dasharray="4 5"/>'
                    f'<circle cx="{mx}" cy="{y}" r="12" fill="#43a047"/></g>')
            ids.append(f"{tag}m{i}")
    return scene(svg, ids)


THEORY = [
    ("The axis of symmetry", "محور التناظر", "L'axe de symétrie", "116", [
        T("Hello, champion! Fold a symmetrical figure along a line and the two halves match exactly. That line is the axis of symmetry. Looking alike is not enough: every part on one side must have a mirrored partner on the other side.",
          "مرحبًا يا بطل! اطوِ شكلًا متناظرًا على خط فينطبق النصفان تمامًا. هذا الخط هو محور التناظر. لا يكفي أن يتشابه الشكلان: لكل جزء في جهة نظيرٌ مقابل في الجهة الأخرى.",
          "Plie une figure symétrique le long d'une droite : les deux moitiés se superposent. C'est l'axe de symétrie."),
        sym(pair=False),
    ]),
    ("Corresponding points", "النقاط المتناظرة", "Points correspondants", "116", [
        T("A point and its mirror image are on opposite sides of the axis, at the same distance from it, on the same level line. Each blue point has a green partner.",
          "النقطة ونظيرتها على جانبي المحور وعلى البعد نفسه منه وعلى المستوى الأفقي نفسه. لكل نقطة زرقاء نظيرة خضراء.",
          "Un point et son symétrique sont de part et d'autre de l'axe, à la même distance."),
        sym(),
    ]),
    ("Complete a symmetrical figure", "نكمل شكلًا متناظرًا", "Compléter une figure symétrique", "117", [
        T("To complete a figure: find the axis, take each point, measure its distance to the axis, mark the same distance on the other side, then join the points in the same order. Check by folding.",
          "لإكمال الشكل: نجد المحور ونأخذ كل نقطة ونقيس بعدها عن المحور ونعلّم البعد نفسه في الجهة المقابلة ثم نصل النقاط بالترتيب نفسه. ونتحقق بالطيّ.",
          "On mesure la distance à l'axe, on la reporte de l'autre côté, on relie dans le même ordre, on vérifie par pliage."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Find the axis, pair the parts, complete the reflection, verify.", "نجد المحور ونقرن الأجزاء ونكمل الانعكاس ونتحقق.", "Axe, paires, compléter, vérifier."),
        F("AXIS → PAIR → COMPLETE → VERIFY"),
    ]),
]

EXERCISES = [
    EX("1", "116", st("Why is this line an axis of symmetry?", "لماذا هذا الخط محور تناظر؟", "Pourquoi cette droite est-elle un axe ?"), [
        sym(),
        T("Because every point has a partner at the same distance on the other side; folding makes the halves match.", "لأن لكل نقطة نظيرة على البعد نفسه في الجهة الأخرى، والطيّ يُطابق النصفين.", "Chaque point a son symétrique à la même distance."),
    ]),
    EX("2", "117", st("A point is 3 squares left of the axis. Where is its partner?", "نقطة تبعد 3 مربعات يسار المحور. أين نظيرتها؟", "Un point est à 3 carreaux à gauche. Où est son symétrique ?"), [
        F("3 squares right of the axis, on the same row"),
    ]),
    EX("3", "117", st("Error detective: \"the two shapes look alike, so the line is an axis.\"", "المحقق: «الشكلان متشابهان إذن الخط محور».", "Détective : « elles se ressemblent donc c'est un axe »."), [
        T("Visual similarity is not enough: check equal distances or fold.", "التشابه البصري لا يكفي: نتحقق من تساوي الأبعاد أو بالطيّ.", "Il faut vérifier les distances ou plier."),
    ]),
]
