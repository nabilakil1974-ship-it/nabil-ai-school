"""Grade 2 Mathematics — Measurement of length: the centimeter."""
from scripts.direct_lessons.common import T, F, EX, st, scene

LESSON_ID = "G02-MATH-EN-026"
GRADE = 2
SUBJECT = "math"
TITLES = {"en": "Measurement of length: the centimeter", "ar": "قياس الطول: السنتيمتر", "fr": "Mesure de longueur : le centimètre"}


def ruler(a, b, tag="R", top=None):
    """Ruler 0..10 cm with a segment from a to b (whole cm) drawn above it."""
    x0, w = 40, 58
    svg = f'<g id="{tag}r"><rect x="{x0-10}" y="200" width="{w*10+20}" height="70" rx="6" fill="#fff3c4" stroke="#0b3d5c" stroke-width="3"/>'
    for i in range(11):
        x = x0 + i * w
        svg += f'<line x1="{x}" y1="200" x2="{x}" y2="{238 if i % 5 else 250}" stroke="#0b3d5c" stroke-width="3"/>'
        svg += f'<text x="{x}" y="262" font-size="22" font-weight="700" text-anchor="middle" fill="#0b3d5c" font-family="sans-serif">{i}</text>'
    svg += f'<text x="{x0+w*10+4}" y="222" font-size="20" fill="#0b3d5c" font-family="sans-serif">cm</text></g>'
    ids = [tag + "r"]
    xa, xb = x0 + a * w, x0 + b * w
    svg += (f'<g id="{tag}s"><line x1="{xa}" y1="150" x2="{xb}" y2="150" stroke="#e53935" stroke-width="10" stroke-linecap="round"/>'
            f'<circle cx="{xa}" cy="150" r="10" fill="#e53935"/><circle cx="{xb}" cy="150" r="10" fill="#e53935"/>'
            f'<line x1="{xa}" y1="160" x2="{xa}" y2="200" stroke="#e53935" stroke-dasharray="6 5" stroke-width="3"/>'
            f'<line x1="{xb}" y1="160" x2="{xb}" y2="200" stroke="#e53935" stroke-dasharray="6 5" stroke-width="3"/></g>')
    ids.append(tag + "s")
    lab = top if top is not None else f"{b-a} cm"
    svg += (f'<text id="{tag}t" x="{(xa+xb)/2}" y="110" font-size="44" font-weight="700" text-anchor="middle" fill="#e53935" font-family="sans-serif">{lab}</text>')
    ids.append(tag + "t")
    return scene(svg, ids)


def square(side=3, tag="Q"):
    s = 60 * side
    x, y = 220, 60
    svg = f'<g id="{tag}a"><rect x="{x}" y="{y}" width="{s}" height="{s}" fill="#bbdefb" stroke="#0b3d5c" stroke-width="5"/></g>'
    ids = [tag + "a"]
    for k, (tx, ty) in enumerate([(x + s / 2, y - 10), (x + s + 50, y + s / 2 + 12), (x + s / 2, y + s + 36), (x - 50, y + s / 2 + 12)]):
        svg += f'<text id="{tag}{k}" x="{tx}" y="{ty}" font-size="34" font-weight="700" text-anchor="middle" fill="#e53935" font-family="sans-serif">{side} cm</text>'
        ids.append(f"{tag}{k}")
    return scene(svg, ids)


THEORY = [
    ("The centimeter, a standard unit", "السنتيمتر وحدة قياس موحّدة", "Le centimètre, unité standard", "56", [
        T("Hello, champion! Today we move from paper strips to one shared unit: the centimeter. This segment is 4 cm. That means from its start to its end there are 4 intervals, each 1 centimeter long. We do not count the marks, we count the spaces between them.",
          "مرحبًا يا بطل! اليوم ننتقل من الشرائط الورقية إلى وحدة موحّدة اسمها السنتيمتر. طول هذه القطعة 4 سم، أي من بدايتها إلى نهايتها 4 فواصل طول كلٍّ منها سنتيمتر واحد. لا نعدّ الخطوط بل نعدّ المسافات بينها.",
          "Aujourd'hui : une unité commune, le centimètre. Ce segment mesure 4 cm : 4 intervalles de 1 cm. On compte les intervalles, pas les traits."),
        ruler(0, 4),
        T("1 cm is the same length on every correct ruler. That is why it is a standard unit.",
          "1 سم هو الطول نفسه على كل مسطرة صحيحة، ولذلك هو وحدة موحّدة.",
          "1 cm est la même longueur sur toute règle correcte : c'est une unité standard."),
    ]),
    ("Start at zero", "نبدأ من الصفر", "Commencer à zéro", "56", [
        T("Put the first endpoint at 0. If you start at another mark, the number under the second endpoint is not the length: you must find the difference. From 2 to 7 the length is 7 − 2 = 5 cm.",
          "نضع النهاية الأولى عند 0. وإذا بدأنا من خط آخر فالعدد تحت النهاية الثانية ليس الطول، بل نحسب الفرق. من 2 إلى 7 الطول 7 − 2 = 5 سم.",
          "On place la première extrémité à 0. Sinon, il faut calculer la différence : de 2 à 7, 7 − 2 = 5 cm."),
        ruler(2, 7),
        F("7 − 2 = 5 cm"),
    ]),
    ("Direction does not change length", "الاتجاه لا يغيّر الطول", "La direction ne change pas la longueur", "56", [
        T("A horizontal, a slanted and a vertical segment can have the same length. We always measure between the same two endpoints.",
          "قد تتساوى أطوال قطعة أفقية ومائلة وعمودية. نقيس دائمًا بين النهايتين نفسيهما.",
          "Un segment horizontal, oblique ou vertical peut avoir la même longueur : on mesure entre les deux extrémités."),
        F("5 cm,  5 cm,  3 cm,  3 cm"),
    ]),
    ("Drawing a given length", "نرسم طولًا معطى", "Tracer une longueur donnée", "56", [
        T("The red point is the fixed start. Put 0 of the ruler on it, mark 3 cm on the line, draw only the part between the two points, and measure again. The directions may differ; the length must be 3 cm.",
          "النقطة الحمراء بداية ثابتة. نضع صفر المسطرة عليها ونعلّم 3 سم على الخط ونرسم الجزء بين النقطتين فقط ثم نعيد القياس. قد تختلف الاتجاهات لكن الطول يجب أن يكون 3 سم.",
          "Le point rouge est le départ. On place le 0 dessus, on marque 3 cm, on trace entre les deux points, puis on remesure."),
        ruler(0, 3),
        F("START POINT → MARK → DRAW STRAIGHT → RE-MEASURE"),
    ]),
    ("The square", "المربع", "Le carré", "56", [
        T("A square has four equal sides. Here every side is 3 cm. A square stays a square when it is rotated: only its direction changes, not its equal sides and square corners.",
          "للمربع أربعة أضلاع متساوية. هنا كل ضلع 3 سم. ويبقى المربع مربعًا إذا أدرناه: يتغيّر اتجاهه فقط لا تساوي أضلاعه ولا زواياه القائمة.",
          "Un carré a quatre côtés égaux. Ici chaque côté mesure 3 cm. Tourné, il reste un carré."),
        square(3),
    ]),
    ("Between two whole centimeters", "بين سنتيمترين صحيحين", "Entre deux centimètres entiers", "57", [
        T("Not every segment ends exactly on a mark. If its end is after 3 and before 4, we say its length is between 3 cm and 4 cm. We do not invent decimals.",
          "ليست كل قطعة تنتهي تمامًا عند خط. إذا انتهت بعد 3 وقبل 4 قلنا إن طولها بين 3 سم و4 سم. لا نخترع كسورًا عشرية.",
          "Si l'extrémité est après 3 et avant 4, la longueur est comprise entre 3 cm et 4 cm."),
        F("between 3 cm and 4 cm"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("To measure: align the start, count the intervals, write the number and cm, check. To draw: start point, mark the length, draw straight, re-measure.",
          "للقياس: نحاذي البداية ونعدّ الفواصل ونكتب العدد مع سم ونتحقق. وللرسم: نقطة البداية، نعلّم الطول، نرسم مستقيمًا، نعيد القياس.",
          "Mesurer : aligner, compter les intervalles, écrire nombre + cm, vérifier. Tracer : départ, marquer, tracer droit, remesurer."),
        F("ALIGN → MEASURE / MARK → NUMBER + cm → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "56", st("Measure the four segments.", "قِس القطع الأربع.", "Mesure les quatre segments."), [
        F("5 cm   5 cm   3 cm   3 cm"),
        T("Direction does not change length.", "الاتجاه لا يغيّر الطول.", "La direction ne change pas la longueur."),
    ]),
    EX("2", "56", st("Draw 3 cm from each red point along the printed line.", "ارسم 3 سم من كل نقطة حمراء على الخط المطبوع.", "Trace 3 cm depuis chaque point rouge."), [
        ruler(0, 3),
        T("Put 0 on the red point, mark 3 cm, draw, re-measure: exactly 3 cm.", "ضع الصفر على النقطة الحمراء وعلّم 3 سم وارسم وأعد القياس: 3 سم تمامًا.", "0 sur le point rouge, marque 3 cm, trace, remesure."),
    ]),
    EX("3", "56", st("Draw a 4 cm segment from each red point.", "ارسم قطعة طولها 4 سم من كل نقطة حمراء.", "Trace un segment de 4 cm depuis chaque point rouge."), [
        ruler(0, 4),
        T("Expected length: 4 cm.", "الطول المطلوب 4 سم.", "Longueur attendue : 4 cm."),
    ]),
    EX("4", "56", st("Measure the sides of the square.", "قِس أضلاع المربع.", "Mesure les côtés du carré."), [
        square(3),
        T("Top, right, bottom and left are all 3 cm. Each side of the square is 3 cm long.", "الأعلى واليمين والأسفل واليسار كلها 3 سم. كل ضلع في المربع طوله 3 سم.", "Chaque côté du carré mesure 3 cm."),
    ]),
    EX("5", "57", st("Complete: between … cm and … cm.", "أكمل: بين … سم و… سم.", "Complète : entre … cm et … cm."), [
        F("3 – 4 cm      4 – 5 cm      2 – 3 cm"),
    ]),
    EX("6", "57", st("Color the squares in red.", "لوّن المربعات بالأحمر.", "Colorie les carrés en rouge."), [
        T("Check equal sides and square corners. Shapes 2, 3 and 4 are squares; shape 1 is not. A tilted square is still a square.", "نفحص تساوي الأضلاع والزوايا القائمة. الأشكال 2 و3 و4 مربعات والأول ليس مربعًا. المربع المائل يبقى مربعًا.", "Les formes 2, 3 et 4 sont des carrés ; la 1 non."),
        F("2, 3, 4"),
    ]),
    EX("7", "57", st("Draw two segments from one red point: 5 cm, and one between 6 cm and 7 cm.", "ارسم من نقطة حمراء قطعتين: طول الأولى 5 سم وطول الثانية بين 6 و7 سم.", "Trace deux segments : 5 cm, et un entre 6 cm et 7 cm."), [
        ruler(0, 5),
        F("6 cm < length < 7 cm"),
    ]),
    EX("8", "57", st("Reproduce the Lebanese flag with a ruler.", "انسخ العلم اللبناني بالمسطرة.", "Reproduis le drapeau libanais avec la règle."), [
        T("Use the ruler for straight horizontal and vertical lines. Keep the three bands: red, white, red, and the cedar centered in the white band. Do not guess the proportions freehand.",
          "استعمل المسطرة للخطوط الأفقية والعمودية المستقيمة. احفظ الأشرطة الثلاثة: أحمر وأبيض وأحمر، والأرزة في وسط الشريط الأبيض. لا تخمّن النسب باليد.",
          "Règle pour les lignes droites. Trois bandes : rouge, blanc, rouge ; le cèdre au centre de la bande blanche."),
    ]),
    EX("9", "", st("Guided practice: a segment from 0 to 6, and one from 2 to 7.", "تدريب: قطعة من 0 إلى 6 وأخرى من 2 إلى 7.", "Entraînement : de 0 à 6, puis de 2 à 7."), [
        ruler(0, 6), ruler(2, 7, tag="S"),
        F("6 cm      7 − 2 = 5 cm"),
        T("The length is the difference between the readings.", "الطول هو الفرق بين القراءتين.", "La longueur est la différence des lectures."),
    ]),
    EX("10", "", st("Transfer: a segment is longer than 4 cm but shorter than 5 cm. Which is true?", "تحدٍّ: قطعة أطول من 4 سم وأقصر من 5 سم. أيّ الجمل صحيحة؟", "Défi : plus longue que 4 cm, plus courte que 5 cm. Quelle phrase est vraie ?"), [
        F("between 4 cm and 5 cm ✓      exactly 5 cm ✗      shorter than 4 cm ✗"),
    ]),
    EX("11", "", st("Error detective: start at 2, end at 7, and the child says 7 cm.", "المحقق: بدأت عند 2 وانتهت عند 7 وقال الطفل 7 سم.", "Détective : départ à 2, fin à 7, l'enfant dit 7 cm."), [
        ruler(2, 7, top="7 cm ?"),
        F("7 − 2 = 5 cm"),
        T("7 is the endpoint reading, not the length.", "العدد 7 قراءة النهاية وليس الطول.", "7 est la lecture de l'extrémité, pas la longueur."),
    ]),
    EX("12", "", st("Final check.", "تقييم أخير.", "Évaluation finale."), [
        F("5, 5, 3, 3 cm · 3 cm · 3–4, 4–5, 2–3 · squares 2, 3, 4 · 5 cm"),
        T("An answer needs cm because cm names the unit.", "يجب كتابة سم لأنها تسمّي الوحدة.", "On écrit cm car cm nomme l'unité."),
    ]),
]
