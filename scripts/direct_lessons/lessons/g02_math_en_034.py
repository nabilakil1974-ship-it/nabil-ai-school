"""Grade 2 Mathematics — Following visual instructions."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G02-MATH-EN-034"
GRADE = 2
SUBJECT = "math"
TITLES = {"en": "Following visual instructions", "ar": "اتباع التعليمات المصوّرة", "fr": "Suivre des consignes en images"}


def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}


QUIZ = [
    {"q": "What is the first action in the paper activity?", "opts": ["Fold the paper in two", "Cut the paper", "Trace the figure", "Open the paper"], "a": 0,
     "why": {"Cut the paper": _w("We cut only at the end, after the folds and the tracing.", "نقصّ في النهاية فقط بعد الطي والرسم.", "On coupe à la fin."),
             "Trace the figure": _w("We trace after all the folds are done.", "نرسم الشكل بعد انتهاء الطيّات.", "On trace après les pliages."),
             "Open the paper": _w("The paper stays folded until after the cut.", "تبقى الورقة مطوية حتى بعد القصّ.", "Le papier reste plié jusqu'après la coupe.")},
     "ok": "Step 1: fold the paper in two."},
    {"q": "How many fold steps come before tracing?", "opts": ["3", "1", "2", "5"], "a": 0,
     "why": {"1": _w("There are more: fold, fold again, fold again.", "هناك أكثر: طيّة ثم طيّة ثم طيّة.", "Il y en a trois."),
             "2": _w("Count again: the book shows three folding steps.", "عُدّ ثانية: الكتاب يعرض ثلاث خطوات طيّ.", "Le livre montre trois pliages."),
             "5": _w("5 is the total number of steps, not only the folds.", "5 هو عدد كل الخطوات لا الطيّات فقط.", "5 est le nombre total d'étapes.")},
     "ok": "Three folds, then trace, then cut."},
    {"q": "Where do we cut?", "opts": ["Along the black lines only", "Along every edge", "Anywhere we like", "Across the fold connections"], "a": 0,
     "why": {"Along every edge": _w("Cutting every edge would separate the figures.", "قصّ كل الحواف يفصل الأشكال.", "Couper partout sépare les figures."),
             "Anywhere we like": _w("We follow the picture exactly.", "نتبع الصورة تمامًا.", "On suit l'image."),
             "Across the fold connections": _w("The connections stay uncut so the figures remain linked.", "نترك الوصلات دون قصّ لتبقى الأشكال متصلة.", "On ne coupe pas les liaisons.")},
     "ok": "Cut only along the black lines."},
]

THEORY = [
    ("A picture procedure has an order", "للتعليمات المصوّرة ترتيب", "Une consigne en images a un ordre", "73", [
        T("Hello! Today we do not have an equation. We have pictures that tell us what to do. Success means doing the steps in order, because if we swap a step, the result changes.",
          "مرحبًا! اليوم ليس عندنا معادلة بل صور تقول لنا ماذا نفعل. النجاح يعني تنفيذ الخطوات بالترتيب لأننا إن بدّلنا خطوة تغيّرت النتيجة.",
          "Aujourd'hui, pas d'équation : des images nous disent quoi faire, dans l'ordre."),
        F("LOOK → DO ONE STEP → CHECK THE PICTURE → CONTINUE"),
    ]),
    ("Three folds", "ثلاث طيّات", "Trois pliages", "73", [
        T("Step 1: fold the paper in two. The two halves must fit exactly. If the edges do not match, open it and fix it before going on.",
          "الخطوة 1: اطوِ الورقة نصفين. يجب أن ينطبق النصفان تمامًا. إن لم تنطبق الحواف افتحها وعدّلها قبل أن تتابع.",
          "Étape 1 : plie la feuille en deux, les deux moitiés doivent coïncider."),
        T("Step 2: fold the folded paper in two again. It becomes a smaller rectangle, like in the picture. Step 3: fold it in two once more. Do not open the paper between the folds.",
          "الخطوة 2: اطوِ الورقة المطوية نصفين مرة ثانية فتصبح مستطيلًا أصغر كما في الصورة. الخطوة 3: اطوِها نصفين مرة أخرى. لا تفتح الورقة بين الطيّات.",
          "Étape 2 : replie en deux encore. Étape 3 : encore une fois, sans rouvrir."),
        F("fold → fold → fold"),
    ]),
    ("Trace, then cut the black lines", "نرسم ثم نقصّ الخطوط السوداء", "On trace puis on découpe", "73", [
        T("Step 4: trace the figure shown in the book onto the folded paper. Use the book's outline, not a different shape, because the outline decides the result after opening.",
          "الخطوة 4: ارسم الشكل الموجود في الكتاب على الورقة المطوية. استعمل خط الكتاب لا شكلًا آخر لأن الخط هو الذي يحدد الشكل بعد الفتح.",
          "Étape 4 : trace la figure du livre sur le papier plié, sans en changer."),
        T("Step 5: keep the paper folded and cut only along the black lines. Do not cut the parts that the picture leaves joined. Always cut slowly, away from your fingers, and ask a grown-up to be near.",
          "الخطوة 5: أبقِ الورقة مطوية وقصّ على الخطوط السوداء فقط. لا تقصّ الأجزاء التي تتركها الصورة متصلة. قصّ ببطء وبعيدًا عن أصابعك واطلب من شخص كبير أن يكون قريبًا.",
          "Étape 5 : coupe seulement les traits noirs, lentement, loin des doigts, avec un adulte près de toi."),
        F("trace → cut the black lines → open"),
    ]),
    ("Why do we get a chain?", "لماذا تظهر سلسلة؟", "Pourquoi une guirlande ?", "73", [
        T("We traced only one figure, but many appear! Why? The paper had several layers. One cut goes through all the stacked layers, and when we unfold, the figure repeats where the folds were. Folding created repetition.",
          "رسمنا شكلًا واحدًا لكن ظهرت أشكال كثيرة! لماذا؟ لأن الورقة كانت من طبقات عدّة. القصّ الواحد يمرّ عبر كل الطبقات، وعند الفتح يتكرر الشكل عند أماكن الطيّ. الطيّ صنع التكرار.",
          "Une seule coupe traverse toutes les couches ; en dépliant, la figure se répète."),
        T("(our own) Fold in half three times and you get 2, then 4, then 8 layers.",
          "(من عندنا) إذا طويتَ الورقة نصفين ثلاث مرات تحصل على 2 ثم 4 ثم 8 طبقات.",
          "(à nous) Trois pliages en deux donnent 2, puis 4, puis 8 couches."),
        F("2 → 4 → 8 layers"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Visual instructions are like a little recipe. Follow the order, match the picture, change nothing that is not shown, and check the result. Step 1, check, step 2, check.",
          "التعليمات المصوّرة مثل وصفة صغيرة. نتبع الترتيب ونطابق الصورة ولا نغيّر شيئًا غير مرسوم ونتحقق من النتيجة. خطوة 1 ثم تحقّق ثم خطوة 2 ثم تحقّق.",
          "Suivre l'ordre, imiter l'image, ne rien changer, vérifier le résultat."),
        F("FOLLOW THE ORDER → MATCH THE PICTURE → CHECK THE RESULT"),
    ]),
]

EXERCISES = [
    EX("1", "73", st("Step 1. What does the picture ask?", "الخطوة 1. ماذا تطلب الصورة؟", "Étape 1. Que demande l'image ?"), [
        T("Fold the paper in two along the line. Check that the two halves match exactly.", "اطوِ الورقة نصفين على الخط وتحقق من انطباق النصفين.", "Plie en deux sur la ligne et vérifie que les moitiés coïncident."),
    ]),
    EX("2", "73", st("Steps 2 and 3. What do we do?", "الخطوتان 2 و3. ماذا نفعل؟", "Étapes 2 et 3. Que fait-on ?"), [
        T("Fold the folded paper in two again, then once more. We now have a narrow rectangle and we have not opened the paper.",
          "نطوي الورقة المطوية نصفين مرة ثانية ثم مرة أخرى فيصير عندنا مستطيل ضيق ولم نفتح الورقة.",
          "On replie deux fois ; on obtient un rectangle étroit sans rouvrir."),
        F("3 folds"),
    ]),
    EX("3", "73", st("Steps 4 and 5. What do we do?", "الخطوتان 4 و5. ماذا نفعل؟", "Étapes 4 et 5. Que fait-on ?"), [
        T("Trace the book's figure on the folded paper. Then cut only along the black lines, keeping the joined parts, and open the paper carefully.",
          "نرسم شكل الكتاب على الورقة المطوية ثم نقصّ على الخطوط السوداء فقط ونحافظ على الأجزاء المتصلة ثم نفتح الورقة بحذر.",
          "On trace, on coupe les traits noirs, on garde les parties liées, on ouvre doucement."),
    ]),
    EX("4", "", st("(our own) Put in order: cut and open; fold; trace; flat sheet.", "(من عندنا) رتّب: قصّ وفتح؛ طيّ؛ رسم؛ ورقة مسطّحة.", "(à nous) Mets dans l'ordre : couper et ouvrir ; plier ; tracer ; feuille plate."), [
        T("Each step needs the one before it. We start with the flat sheet, then fold, then trace, then cut and open.",
          "كل خطوة تحتاج إلى التي قبلها. نبدأ بالورقة المسطّحة ثم نطوي ثم نرسم ثم نقصّ ونفتح.",
          "On commence par la feuille plate, puis plier, tracer, couper et ouvrir."),
        F("flat sheet → fold → trace → cut and open"),
    ]),
    EX("5", "", st("(our own) A child traces the figure and then folds the paper. What went wrong?", "(من عندنا) رسم طفل الشكل ثم طوى الورقة. ما الخطأ؟", "(à nous) Un enfant trace puis plie. Quelle est l'erreur ?"), [
        T("The tracing happened before the folds were finished. Correct way: do the three folds first, then trace and cut.",
          "حدث الرسم قبل انتهاء الطيّات. الصحيح: نعمل الطيّات الثلاث أولًا ثم نرسم ونقصّ.",
          "Il a tracé avant de finir les pliages : d'abord les trois pliages, puis tracer et couper."),
    ]),
]
