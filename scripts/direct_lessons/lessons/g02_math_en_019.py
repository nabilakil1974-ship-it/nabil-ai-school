"""Grade 2 Mathematics — Reproducing figures."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G02-MATH-EN-019"
GRADE = 2
SUBJECT = "math"
TITLES = {"en": "Reproducing Figures", "ar": "إعادة رسم الأشكال", "fr": "Reproduire des figures"}


def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}


QUIZ = [
    {"q": "When we reproduce a figure, what must we copy?",
     "opts": ["The points, the connections and the colors in the right places", "Only the general look", "Only the colors", "Any shape we like"], "a": 0,
     "why": {"Only the general look": _w("A look-alike is not enough. We copy the exact points and connections.", "الشكل المشابه لا يكفي. ننقل النقاط والوصلات بالضبط.", "Une figure qui ressemble ne suffit pas : on copie les points et les liens exacts."),
             "Only the colors": _w("Colors matter, but the shape comes first.", "الألوان مهمة لكن الشكل أولًا.", "Les couleurs comptent, mais la forme d'abord."),
             "Any shape we like": _w("We must copy the model, not invent.", "ننسخ النموذج ولا نخترع.", "On copie le modèle, on n'invente pas.")},
     "ok": "Copy the points, the connections and the colors."},
    {"q": "One corner of the copy is one grid square away from where it should be. Is the copy exact?",
     "opts": ["No, it is not exact", "Yes, it is close enough", "Yes, if the colors are right", "We cannot tell"], "a": 0,
     "why": {"Yes, it is close enough": _w("Close is not exact. One square of shift changes the figure.", "القريب ليس مطابقًا. إزاحة مربع واحد تغيّر الشكل.", "Presque n'est pas exact : un carreau de décalage change la figure."),
             "Yes, if the colors are right": _w("Right colors cannot fix a wrong corner.", "الألوان الصحيحة لا تصلح رأسًا خاطئًا.", "De bonnes couleurs ne corrigent pas un coin faux."),
             "We cannot tell": _w("We can: count the grid squares and compare.", "نستطيع: نعدّ المربعات ونقارن.", "On peut : on compte les carreaux et on compare.")},
     "ok": "A shifted corner means the copy is not exact."},
    {"q": "What do we do first: draw the segments or color?",
     "opts": ["Draw the segments, then color", "Color, then draw the segments", "Color only", "It never matters"], "a": 0,
     "why": {"Color, then draw the segments": _w("We need the regions to exist before we color them.", "نحتاج أن تظهر المناطق قبل تلوينها.", "Il faut que les régions existent avant de les colorier."),
             "Color only": _w("The figure must be drawn first.", "يجب رسم الشكل أولًا.", "Il faut d'abord tracer la figure."),
             "It never matters": _w("It matters: geometry first, color second.", "الترتيب مهم: الشكل أولًا ثم اللون.", "L'ordre compte : forme d'abord, couleur ensuite.")},
     "ok": "Geometry first, color second."},
]

THEORY = [
    ("Copy the relationships", "ننقل العلاقات", "Copier les relations", "44", [
        T("Hello, champion! Today we do not draw from memory. We reproduce a figure. Look at the model. Find its corner points, its straight segments, which ones are flat and which ones slant, and where each color is. A good copy keeps the same connections, not just the same general look.",
          "مرحبًا يا بطل! اليوم لا نرسم من الذاكرة بل نعيد رسم شكل. انظر إلى النموذج. جد نقاط الزوايا والقطع المستقيمة، أيها أفقي وأيها مائل، وأين يقع كل لون. النسخة الجيدة تحافظ على الوصلات نفسها لا على الشكل العام فقط.",
          "Bonjour, champion ! Aujourd'hui on ne dessine pas de mémoire : on reproduit une figure. Regarde le modèle : ses points, ses segments droits (horizontaux ou penchés) et ses couleurs. Une bonne copie garde les mêmes liens, pas seulement l'allure générale."),
        F("LOOK → FIND THE KEY POINTS → CONNECT IN THE SAME WAY → CHECK → COLOR"),
    ]),
    ("Dots are anchors", "النقاط مرتكزات", "Les points sont des repères", "44", [
        T("Some dots are guides for the missing segments. But we do not join every dot to every other dot. We compare with the model part by part: take one segment you can see, find the next connected point, find its guide dot, and draw only that segment with a ruler. At the end check: same corners, same connections, straight lines, no extra line.",
          "بعض النقاط ترشدنا إلى القطع الناقصة. لكننا لا نصل كل نقطة بكل نقطة. نقارن بالنموذج جزءًا جزءًا: نأخذ قطعة ظاهرة ونجد النقطة التالية المتصلة بها ونحدد نقطتها المقابلة ونرسم هذه القطعة فقط بالمسطرة. في النهاية نتحقق: الزوايا نفسها والوصلات نفسها والخطوط مستقيمة ولا خط زائد.",
          "Certains points guident les segments manquants. Mais on ne relie pas tous les points entre eux. On compare avec le modèle morceau par morceau : un segment visible, le point suivant relié, son point repère, et on trace seulement ce segment à la règle. À la fin : mêmes sommets, mêmes liens, lignes droites, aucune ligne en trop."),
        F("same corners · same connections · straight lines · no extra line"),
    ]),
    ("A grid keeps position and size", "الشبكة تحفظ الموضع والحجم", "La quadrillage garde la position", "45", [
        T("On a grid we count squares. Put the first point on the blank grid. Then count how many squares to the next corner, exactly like in the model, mark it, and connect in the same order. For example (our own): start at a point, go 3 squares right, then 2 squares up, and join back to the start. That gives a triangle with one flat side. If a corner is one square off, the copy is not exact.",
          "على الشبكة نعدّ المربعات. نضع النقطة الأولى على الشبكة الفارغة ثم نعدّ كم مربعًا إلى الزاوية التالية تمامًا كما في النموذج، ونعلّمها ونصل بالترتيب نفسه. مثال (من عندنا): نبدأ من نقطة، ونسير 3 مربعات إلى اليمين ثم مربعين إلى الأعلى ونعود إلى البداية. نحصل على مثلث له ضلع أفقي. إذا كانت زاوية تبعد مربعًا واحدًا فالنسخة غير مطابقة.",
          "Sur un quadrillage, on compte les carreaux. On place le premier point, puis on compte les carreaux jusqu'au sommet suivant comme dans le modèle, on le marque et on relie dans le même ordre. Exemple (notre exemple) : départ, 3 carreaux à droite, 2 carreaux vers le haut, retour au départ : un triangle avec un côté horizontal. Un sommet décalé d'un carreau rend la copie inexacte."),
        F("start → 3 squares right → 2 squares up → back to start"),
    ]),
    ("Find the error", "نجد الخطأ", "Trouver l'erreur", "45", [
        T("To correct a copy, compare one feature at a time with the model: the outline, the top points, the wheels, the window square, the slanted sides. Find the one part that does not match and fix only that part. Leave the correct parts alone.",
          "لتصحيح نسخة نقارن ميزة واحدة في كل مرة مع النموذج: الإطار الخارجي، النقاط العليا، العجلات، مربع النافذة، الأضلاع المائلة. نجد الجزء الوحيد غير المطابق ونصلح هذا الجزء فقط. نترك الأجزاء الصحيحة كما هي.",
          "Pour corriger une copie, on compare un élément à la fois avec le modèle : contour, points du haut, roues, carré de la fenêtre, côtés penchés. On trouve la seule partie différente et on corrige seulement celle-ci."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("We did not draw something similar: we made an exact copy. Look at the model, anchor on a point, count or compare, connect, check, and only then color. Best habit: geometry first, color second.",
          "لم نرسم شكلًا مشابهًا بل نسخة مطابقة. ننظر إلى النموذج ونثبّت نقطة ونعدّ أو نقارن ونصل ونتحقق ثم نلوّن. أفضل عادة: الشكل أولًا ثم اللون.",
          "On n'a pas dessiné quelque chose de ressemblant : on a fait une copie exacte. On regarde, on se repère, on compte ou compare, on relie, on vérifie, puis on colorie. Bonne habitude : forme d'abord, couleur ensuite."),
        F("LOOK → ANCHOR → COUNT / COMPARE → CONNECT → CHECK → COLOR"),
    ]),
]

EXERCISES = [
    EX("1", "44", st("Color the figure on the right like the figure on the left.",
                     "لوّن الشكل الأيمن مثل الشكل الأيسر.",
                     "Colorie la figure de droite comme celle de gauche."), [
        T("Do not change the segments. Take one region of the model, find the same region on the right by its position and its borders, and give it the same color. Repeat for every region.",
          "لا نغيّر القطع. نأخذ منطقة من النموذج ونجد المنطقة المقابلة على اليمين من موضعها وحدودها ونعطيها اللون نفسه. نكرر لكل منطقة.",
          "On ne change pas les segments. On prend une région du modèle, on trouve la même région à droite grâce à sa place et ses bords, et on la colorie pareil. On recommence pour chaque région."),
        F("same region → same color → next region"),
    ]),
    EX("2", "44", st("Draw the missing segments to make a larger copy.",
                     "ارسم القطع الناقصة لتحصل على نسخة أكبر.",
                     "Trace les segments manquants pour obtenir une copie plus grande."), [
        T("Start from a segment you can see. Find the next connected point of the model and its guide dot. Draw only the segment the model shows, with a ruler. Continue until the outline and the inside lines match.",
          "نبدأ من قطعة ظاهرة. نجد النقطة التالية المتصلة في النموذج ونقطتها الإرشادية. نرسم القطعة التي يظهرها النموذج فقط بالمسطرة. نتابع حتى يتطابق الإطار والخطوط الداخلية.",
          "Pars d'un segment visible. Trouve le point suivant relié dans le modèle et son point repère. Trace seulement le segment du modèle, à la règle, jusqu'à ce que le contour et les lignes intérieures correspondent."),
        F("same corners · same connections · no extra line"),
    ]),
    EX("3", "44", st("Draw the missing segments, then color.",
                     "ارسم القطع الناقصة ثم لوّن.",
                     "Trace les segments manquants, puis colorie."), [
        T("First finish the drawing: same outline and same inside lines. Only then copy the colors into the matching regions. Check that no region is missing or added.",
          "أولًا نكمل الرسم: الإطار نفسه والخطوط الداخلية نفسها. بعدها فقط ننقل الألوان إلى المناطق المقابلة. نتأكد أنه لا توجد منطقة ناقصة أو زائدة.",
          "D'abord on termine le dessin : même contour, mêmes lignes intérieures. Ensuite seulement on copie les couleurs dans les régions correspondantes, sans région en plus ou en moins."),
    ]),
    EX("4", "45", st("Reproduce the green figure on the grid.",
                     "أعد رسم الشكل الأخضر على الشبكة.",
                     "Reproduis la figure verte sur le quadrillage."), [
        T("Choose one corner of the model and put the matching point on the blank grid. Count the squares from this corner to the next one in the model, and mark the same number on your grid. Connect in the same order, copy the inside segment, check, then color it green.",
          "نختار زاوية من النموذج ونضع النقطة المقابلة على الشبكة الفارغة. نعدّ المربعات من هذه الزاوية إلى الزاوية التالية في النموذج ونعلّم العدد نفسه على شبكتنا. نصل بالترتيب نفسه وننقل القطعة الداخلية ونتحقق ثم نلوّن بالأخضر.",
          "Choisis un sommet du modèle et place le point correspondant sur la grille vierge. Compte les carreaux jusqu'au sommet suivant et marque le même nombre. Relie dans le même ordre, copie le segment intérieur, vérifie, puis colorie en vert."),
        F("count squares → mark → connect → check → color green"),
    ]),
    EX("5", "45", st("(our own) Copy a triangle: first point, then 3 squares right, then 2 squares up, then close it.",
                     "(من عندنا) انسخ مثلثًا: نقطة أولى ثم 3 مربعات يمينًا ثم مربعين إلى الأعلى ثم أغلق الشكل.",
                     "(notre exemple) Copie un triangle : un premier point, 3 carreaux à droite, 2 carreaux vers le haut, puis ferme la figure."), [
        T("Mark the first point. Count 3 squares to the right and mark the second point. From there count 2 squares up and mark the third point. Join the three points and check that the figure is closed.",
          "نعلّم النقطة الأولى. نعدّ 3 مربعات يمينًا ونعلّم النقطة الثانية. ومنها نعدّ مربعين إلى الأعلى ونعلّم النقطة الثالثة. نصل النقاط الثلاث ونتحقق أن الشكل مغلق.",
          "Marque le premier point. Compte 3 carreaux vers la droite : deuxième point. De là, 2 carreaux vers le haut : troisième point. Relie les trois points et vérifie que la figure est fermée."),
        F("3 squares right + 2 squares up → 3 points → closed triangle"),
    ]),
]
