"""Grade 10 Mathematics — Trigonometric functions (right-triangle ratios; source-controlled)."""
from scripts.direct_lessons.common import T, F, EX, st, scene

LESSON_ID = "G10-MATH-EN-007"
GRADE = 10
SUBJECT = "math"
TITLES = {"en": "Trigonometric functions", "ar": "الدوال المثلثية", "fr": "Fonctions trigonométriques"}


def tri(show=("opp", "adj", "hyp"), tag="R"):
    """Right triangle with the right angle at bottom-right, reference angle θ at bottom-left."""
    A, B, C = (90, 330), (500, 330), (500, 90)
    svg = (f'<g id="{tag}t"><polygon points="{A[0]},{A[1]} {B[0]},{B[1]} {C[0]},{C[1]}" fill="#e3f2fd" stroke="#0b3d5c" stroke-width="5"/>'
           f'<rect x="{B[0]-26}" y="{B[1]-26}" width="26" height="26" fill="none" stroke="#0b3d5c" stroke-width="3"/>'
           f'<text x="{A[0]+46}" y="{A[1]-8}" font-size="34" font-weight="700" fill="#e53935" font-family="sans-serif">θ</text></g>')
    ids = [tag + "t"]
    lab = {"adj": (295, 372, "adjacent", "#2e7d32"), "opp": (545, 215, "opposite", "#e53935"), "hyp": (260, 190, "hypotenuse", "#1565c0")}
    for k in show:
        x, y, t, c = lab[k]
        svg += f'<text id="{tag}{k}" x="{x}" y="{y}" font-size="28" font-weight="700" text-anchor="middle" fill="{c}" font-family="sans-serif">{t}</text>'
        ids.append(tag + k)
    return scene(svg, ids)


def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "opposite = 5, hypotenuse = 13: sin θ = ?", "opts": ["5/13", "13/5", "12/13", "5/12"], "a": 0,
     "why": {"13/5": _w("sin = opposite / hypotenuse, not upside down.", "الجيب = المقابل ÷ الوتر لا العكس.", "sin = opposé / hypoténuse."),
             "12/13": _w("12 is not given.", "العدد 12 غير معطى.", "12 n'est pas donné."),
             "5/12": _w("That would use the adjacent side.", "هذا يستعمل المجاور.", "Cela utilise l'adjacent.")}, "ok": "sin θ = 5/13"},
    {"q": "opposite = 9, adjacent = 12: tan θ = ?", "opts": ["3/4", "4/3", "9/15", "12/9"], "a": 0,
     "why": {"4/3": _w("tan = opposite / adjacent.", "الظل = المقابل ÷ المجاور.", "tan = opposé / adjacent."),
             "9/15": _w("The hypotenuse is not used in tan.", "الوتر لا يدخل في الظل.", "Pas l'hypoténuse."),
             "12/9": _w("Swapped: opposite goes on top.", "المقابل في البسط.", "L'opposé en haut.")}, "ok": "tan θ = 9/12 = 3/4"},
    {"q": "cos θ = 4/5, hypotenuse = 15: adjacent = ?", "opts": ["12", "20", "19", "3"], "a": 0,
     "why": {"20": _w("The adjacent side is shorter than the hypotenuse.", "المجاور أقصر من الوتر.", "Plus court que l'hypoténuse."),
             "19": _w("Use adjacent = 15 × 4/5.", "نستعمل المجاور = 15 × 4/5.", "15 × 4/5."),
             "3": _w("Use adjacent = 15 × 4/5.", "نستعمل المجاور = 15 × 4/5.", "15 × 4/5.")}, "ok": "15 × 4 / 5 = 12"},
]

THEORY = [
    ("Mark the reference angle first", "نحدّد الزاوية المرجعية أولًا", "Repérer l'angle de référence", "", [
        T("Hello! Before any formula, mark the acute angle θ. The hypotenuse is opposite the right angle and is the longest side. The opposite side faces θ; the adjacent side touches θ. If you change the reference angle, opposite and adjacent usually swap roles.",
          "مرحبًا! قبل أي قانون نحدّد الزاوية الحادة θ. الوتر مقابل للزاوية القائمة وهو أطول ضلع. الضلع المقابل هو الذي يواجه θ والمجاور هو الذي يلامسها. وإذا غيّرنا الزاوية المرجعية يتبادل المقابل والمجاور غالبًا.",
          "On repère θ : l'hypoténuse est en face de l'angle droit ; l'opposé fait face à θ ; l'adjacent touche θ."),
        tri(),
    ]),
    ("Sine, cosine, tangent", "الجيب وجيب التمام والظل", "Sinus, cosinus, tangente", "", [
        T("sin θ = opposite / hypotenuse, cos θ = adjacent / hypotenuse, tan θ = opposite / adjacent. We choose the ratio that contains exactly the data we have and the quantity we want, not by the name of a formula.",
          "جا θ = المقابل ÷ الوتر، وجتا θ = المجاور ÷ الوتر، وظا θ = المقابل ÷ المجاور. نختار النسبة التي تحوي بالضبط ما نعرفه وما نبحث عنه، لا باسم القانون.",
          "sin = opposé/hypoténuse ; cos = adjacent/hypoténuse ; tan = opposé/adjacent."),
        F("sin θ = opposite / hypotenuse"), F("cos θ = adjacent / hypotenuse"), F("tan θ = opposite / adjacent"),
    ]),
    ("Choose, then calculate", "نختار ثم نحسب", "Choisir puis calculer", "", [
        T("Opposite 6 and hypotenuse 10: sin θ = 6/10 = 3/5. We keep the exact value 3/5; it lies between 0 and 1, as it should. If cos θ = 4/5 and the hypotenuse is 15, then adjacent = 15 × 4/5 = 12, shorter than 15: plausible. If tan θ = 3/4 and adjacent = 8, then opposite = 8 × 3/4 = 6; the hypotenuse is not needed.",
          "المقابل 6 والوتر 10: جا θ = 6/10 = 3/5. نحتفظ بالقيمة الدقيقة 3/5 وهي بين 0 و1 كما يجب. وإذا كان جتا θ = 4/5 والوتر 15 فالمجاور = 15 × 4/5 = 12 وهو أقصر من 15: معقول. وإذا كان ظا θ = 3/4 والمجاور 8 فالمقابل = 8 × 3/4 = 6 ولا نحتاج الوتر.",
          "sin θ = 3/5 ; adjacent = 12 ; opposé = 6."),
        F("6 / 10 = 3/5"), F("15 × 4 / 5 = 12"), F("8 × 3 / 4 = 6"),
    ]),
    ("The identity sin² + cos² = 1", "المتطابقة جا² + جتا² = 1", "L'identité sin² + cos² = 1", "", [
        T("When the definitions allow it, sin²θ + cos²θ = 1. If sin θ = 3/5 then cos²θ = 1 − 9/25 = 16/25, so |cos θ| = 4/5. A square does not tell + from −: we use the angle information to choose the sign.",
          "عندما تسمح التعريفات فإن جا²θ + جتا²θ = 1. إذا كان جا θ = 3/5 فإن جتا²θ = 1 − 9/25 = 16/25 إذن |جتا θ| = 4/5. والتربيع لا يميّز + من −: نستعمل معلومات الزاوية لاختيار الإشارة.",
          "sin² + cos² = 1 ; le signe vient de l'angle."),
        F("1 − 9/25 = 16/25"),
    ]),
    ("Do not trust the picture", "لا نثق بالرسم وحده", "Ne pas se fier au dessin", "", [
        T("A triangle that looks right-angled is not a right triangle unless the right angle is marked or proved. And a side that looks opposite is opposite only relative to θ. Calculate with approximations only at the end, with the calculator in the right mode.",
          "المثلث الذي يبدو قائمًا ليس قائمًا ما لم تُعلَّم الزاوية القائمة أو تُثبَت. والضلع الذي يبدو مقابلًا مقابلٌ فقط بالنسبة إلى θ. ونستعمل التقريب في النهاية فقط والآلة الحاسبة على النمط الصحيح.",
          "Un angle droit doit être codé ou démontré."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Label the geometry first, the formula second.", "نعلّم الهندسة أولًا والقانون ثانيًا.", "La figure d'abord, la formule ensuite."),
        F("θ → OPP / ADJ / HYP → choose ratio → calculate → check"),
    ]),
]

EXERCISES = [
    EX("1", "", st("opposite = 5, hypotenuse = 13: find sin θ.", "المقابل 5 والوتر 13: أوجد جا θ.", "opposé 5, hypoténuse 13 : sin θ."), [F("sin θ = 5/13")]),
    EX("2", "", st("adjacent = 7, hypotenuse = 25: find cos θ.", "المجاور 7 والوتر 25: أوجد جتا θ.", "adjacent 7, hypoténuse 25 : cos θ."), [F("cos θ = 7/25")]),
    EX("3", "", st("opposite = 9, adjacent = 12: find tan θ.", "المقابل 9 والمجاور 12: أوجد ظا θ.", "opposé 9, adjacent 12 : tan θ."), [F("tan θ = 9/12 = 3/4")]),
    EX("4", "", st("cos θ = 12/13, hypotenuse = 26: find the adjacent side.", "جتا θ = 12/13 والوتر 26: أوجد المجاور.", "cos θ = 12/13, hypoténuse 26 : adjacent."), [F("12/13 = adjacent / 26      adjacent = 24"), T("24 < 26, plausible.", "24 < 26 معقول.", "24 < 26.")]),
    EX("5", "", st("Error detective: opposite = 8, hypotenuse = 10 and \"cos θ = 8/10\".", "المحقق: المقابل 8 والوتر 10 و«جتا θ = 8/10».", "Détective : cos θ = 8/10 ?"), [T("8 is the opposite side, so 8/10 is sin θ, not cos θ.", "8 هو المقابل فالنسبة 8/10 هي جا θ لا جتا θ.", "8/10 = sin θ."), F("sin θ = 8/10 = 4/5")]),
    EX("6", "", st("sin θ = 3/5: find cos²θ.", "جا θ = 3/5: أوجد جتا²θ.", "sin θ = 3/5 : cos²θ."), [F("cos²θ = 1 − 9/25 = 16/25      |cos θ| = 4/5")]),
]
