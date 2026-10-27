"""Grade 10 Mathematics — Absolute value – Approximation (source-controlled; general examples)."""
from scripts.direct_lessons.common import T, F, EX, st, scene

LESSON_ID = "G10-MATH-EN-006"
GRADE = 10
SUBJECT = "math"
TITLES = {"en": "Absolute value – Approximation", "ar": "القيمة المطلقة والتقريب", "fr": "Valeur absolue – Approximation"}


def nline(lo, hi, marks=(), center=None, tag="N"):
    """Number line lo..hi with highlighted points and an optional reference point."""
    x0, x1, y = 40, 620, 200
    step = (x1 - x0) / (hi - lo)
    px = lambda v: x0 + (v - lo) * step
    svg = f'<g id="{tag}l"><line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="#0b3d5c" stroke-width="5"/>'
    for v in range(lo, hi + 1):
        svg += (f'<line x1="{px(v)}" y1="{y-10}" x2="{px(v)}" y2="{y+10}" stroke="#0b3d5c" stroke-width="3"/>'
                f'<text x="{px(v)}" y="{y+40}" font-size="24" font-weight="700" text-anchor="middle" fill="#0b3d5c" font-family="sans-serif">{v}</text>')
    svg += '</g>'
    ids = [tag + "l"]
    if center is not None:
        svg += f'<g id="{tag}c"><circle cx="{px(center)}" cy="{y}" r="13" fill="#fbc02d" stroke="#0b3d5c" stroke-width="3"/></g>'
        ids.append(tag + "c")
        for i, m in enumerate(marks):
            xa, xb = sorted((px(center), px(m)))
            svg += (f'<g id="{tag}d{i}"><line x1="{xa}" y1="{y-45-30*i}" x2="{xb}" y2="{y-45-30*i}" stroke="#43a047" stroke-width="5"/></g>')
            ids.append(f"{tag}d{i}")
    for i, m in enumerate(marks):
        svg += f'<g id="{tag}p{i}"><circle cx="{px(m)}" cy="{y}" r="13" fill="#e53935" stroke="#0b3d5c" stroke-width="3"/></g>'
        ids.append(f"{tag}p{i}")
    return scene(svg, ids)


def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "|−8| = ?", "opts": ["8", "−8", "0", "16"], "a": 0,
     "why": {"−8": _w("A distance is never negative.", "المسافة لا تكون سالبة.", "Une distance est positive."),
             "0": _w("−8 is 8 units from 0.", "−8 تبعد 8 وحدات عن الصفر.", "−8 est à 8 de 0."),
             "16": _w("Distance from −8 to 0 is 8.", "المسافة من −8 إلى 0 هي 8.", "La distance est 8.")}, "ok": "|−8| = 8"},
    {"q": "Distance between −2 and 5 = ?", "opts": ["7", "3", "−7", "10"], "a": 0,
     "why": {"3": _w("Use |−2 − 5| = |−7|.", "نستعمل |−2 − 5| = |−7|.", "|−2 − 5| = 7."),
             "−7": _w("A distance is not negative.", "المسافة ليست سالبة.", "Distance positive."),
             "10": _w("Add 2 units (to 0) and 5 units (from 0): 7.", "وحدتان إلى الصفر و5 منه: 7.", "2 + 5 = 7.")}, "ok": "|−2 − 5| = 7"},
    {"q": "|x − 4| = 3 → x = ?", "opts": ["1 or 7", "7 only", "3 or −3", "4 or −4"], "a": 0,
     "why": {"7 only": _w("Also go 3 units to the left of 4.", "اذهب أيضًا 3 وحدات يسار 4.", "Aussi 3 à gauche."),
             "3 or −3": _w("The center is 4, not 0.", "المركز 4 وليس 0.", "Le centre est 4."),
             "4 or −4": _w("The distance is 3, from the point 4.", "المسافة 3 من النقطة 4.", "Distance 3 depuis 4.")}, "ok": "x = 1 or x = 7"},
]

THEORY = [
    ("Absolute value is a distance", "القيمة المطلقة مسافة", "La valeur absolue est une distance", "", [
        T("Hello! Forget \"absolute value removes the sign\". |x| is the distance from x to 0 on the number line, so it is never negative. |5| = 5 and |−5| = 5, because both points are 5 units from 0. That is why |−x| = |x|, |x| ≥ 0, and |x| = 0 only when x = 0.",
          "مرحبًا! انسَ عبارة «القيمة المطلقة تزيل الإشارة». |x| هي المسافة من x إلى 0 على مستقيم الأعداد فلا تكون سالبة أبدًا. |5| = 5 و|−5| = 5 لأن النقطتين تبعدان 5 وحدات عن الصفر. ولذلك |−x| = |x| و|x| ≥ 0 و|x| = 0 فقط عندما x = 0.",
          "|x| est la distance de x à 0 : |5| = |−5| = 5."),
        nline(-6, 6, marks=(-5, 5), center=0),
        F("|5| = 5      |−5| = 5      |x| ≥ 0"),
    ]),
    ("Distance between two numbers", "المسافة بين عددين", "Distance entre deux nombres", "", [
        T("The distance between a and b is |a − b|, and it does not matter which comes first. Between 2 and 7: |2 − 7| = |−5| = 5 = |7 − 2|. Between −2 and 5: |−2 − 5| = |−7| = 7.",
          "المسافة بين a وb هي |a − b| ولا يهم أيهما أولًا. بين 2 و7: |2 − 7| = |−5| = 5 = |7 − 2|. وبين −2 و5: |−2 − 5| = |−7| = 7.",
          "Distance entre a et b : |a − b|."),
        F("|2 − 7| = 5      |−2 − 5| = 7"),
    ]),
    ("The equation |x| = r", "المعادلة |x| = r", "L'équation |x| = r", "", [
        T("Ask: which points are r units from 0? For |x| = 4 there are two: 4 and −4. If r > 0 we get two points symmetric about 0.",
          "نسأل: ما النقاط التي تبعد r وحدة عن الصفر؟ في |x| = 4 نقطتان: 4 و−4. وإذا كان r > 0 نحصل على نقطتين متناظرتين حول الصفر.",
          "|x| = 4 donne x = 4 ou x = −4."),
        nline(-5, 5, marks=(-4, 4), center=0),
        F("|x| = 4  ⇒  x = 4  or  x = −4"),
    ]),
    ("The equation |x − a| = r", "المعادلة |x − a| = r", "L'équation |x − a| = r", "", [
        T("|x − 3| = 2 means: x is at distance 2 from 3. Move 2 left: 1. Move 2 right: 5. So x = 1 or x = 5. Check: |1 − 3| = 2 and |5 − 3| = 2.",
          "|x − 3| = 2 تعني: x على بعد 2 من النقطة 3. وحدتان يسارًا: 1. وحدتان يمينًا: 5. إذن x = 1 أو x = 5. نتحقق: |1 − 3| = 2 و|5 − 3| = 2.",
          "|x − 3| = 2 : x = 1 ou x = 5."),
        nline(0, 6, marks=(1, 5), center=3),
        F("|1 − 3| = 2      |5 − 3| = 2"),
    ]),
    ("Exact value or approximation?", "القيمة الدقيقة أم التقريبية؟", "Valeur exacte ou approchée ?", "", [
        T("The exact value √2 is not 1.41; 1.41 is an approximation to a given precision. Keep √2 during exact work and round once, at the end, to the requested precision. We must know the precision (integer, tenth, hundredth) before rounding. Rounding in the middle can accumulate error.",
          "القيمة الدقيقة √2 ليست 1.41؛ فـ1.41 تقريب بدقة معيّنة. نحتفظ بـ√2 أثناء الحساب الدقيق ونقرّب مرة واحدة في النهاية وفق الدقة المطلوبة. يجب أن نعرف الدقة (الوحدة أو العُشر أو المئة) قبل التقريب. والتقريب في منتصف الحل قد يراكم الخطأ.",
          "√2 est exact ; 1,41 est une valeur approchée."),
        F("√2 ≈ 1.41   (to the nearest hundredth)"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Interpret the distance first, calculate second. Verify both solutions. State the precision before rounding.", "نفسّر المسافة أولًا ثم نحسب. نتحقق من الحلين. ونحدّد الدقة قبل التقريب.", "Distance d'abord, calcul ensuite."),
        F("|x| → distance to 0      |a − b| → distance between a and b"),
    ]),
]

EXERCISES = [
    EX("1", "", st("Evaluate |−8|.", "احسب |−8|.", "Calcule |−8|."), [F("|−8| = 8")]),
    EX("2", "", st("Find the distance between −2 and 5.", "أوجد المسافة بين −2 و5.", "Distance entre −2 et 5."), [F("|−2 − 5| = |−7| = 7")]),
    EX("3", "", st("Solve |x| = 6.", "حلّ |x| = 6.", "Résous |x| = 6."), [F("x = 6  or  x = −6")]),
    EX("4", "", st("Solve |x − 4| = 3.", "حلّ |x − 4| = 3.", "Résous |x − 4| = 3."), [nline(0, 8, marks=(1, 7), center=4), F("x = 1  or  x = 7      |1 − 4| = 3      |7 − 4| = 3")]),
    EX("5", "", st("Error detective: \"|x| = 5 has only x = 5\".", "المحقق: «|x| = 5 لها حل واحد فقط x = 5».", "Détective : |x| = 5 a une seule solution."), [T("−5 is also 5 units from 0.", "العدد −5 يبعد أيضًا 5 وحدات عن الصفر.", "−5 aussi."), F("x = 5  or  x = −5")]),
    EX("6", "", st("Why must we know the precision before rounding?", "لماذا يجب معرفة الدقة قبل التقريب؟", "Pourquoi connaître la précision avant d'arrondir ?"), [T("The precision decides which digits we keep and where we look to round.", "الدقة تحدّد الأرقام التي نبقيها وموضع النظر لاتخاذ قرار التقريب.", "La précision décide des chiffres conservés.")]),
]
