"""Grade 10 Mathematics — Cumulative review: Solid geometry (supplementary)."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G10-MATH-EN-030"
GRADE = 10
SUBJECT = "math"
TITLES = {"en": "Cumulative review: Solid geometry", "ar": "مراجعة شاملة: الهندسة الفضائية", "fr": "Révision : géométrie dans l'espace"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "Two edges look equal in the drawing. We should …", "opts": ["find a given or theorem", "assume they are equal", "measure the page", "ignore them"], "a": 0,
     "why": {"assume they are equal": _w("It only looks true.", "تبدو صحيحة فقط.", "Semble."),
             "measure the page": _w("The page is 2D.", "الورقة ثنائية البعد.", "2D."),
             "ignore them": _w("Look for evidence.", "نبحث عن دليل.", "Cherche.")}, "ok": "evidence first"},
    {"q": "Two section points may be joined if they lie …", "opts": ["on one face the plane cuts", "close on the page", "on opposite faces", "anywhere"], "a": 0,
     "why": {"close on the page": _w("Closeness is not proof.", "القرب ليس برهانًا.", "Non."),
             "on opposite faces": _w("No common face.", "لا وجه مشترك.", "Non."),
             "anywhere": _w("Segments must lie in faces.", "القطع في الأوجه.", "Dans une face.")}, "ok": "same face"},
    {"q": "Rotating a solid changes …", "opts": ["visibility", "incidence", "the faces", "the vertices' names"], "a": 0,
     "why": {"incidence": _w("Incidence stays.", "الاتصال يبقى.", "Reste."),
             "the faces": _w("The solid is the same.", "المجسم نفسه.", "Même."),
             "the vertices' names": _w("Labels stay.", "الأسماء تبقى.", "Restent.")}, "ok": "visibility"},
]

THEORY = [
    ("The biggest trap", "أكبر فخ", "Le plus grand piège", "", [
        T("Hello! The biggest trap in solid geometry is forgetting that the paper is 2D while the problem is 3D. Before any proof, rebuild the solid in your mind: vertices, edges, faces, and what is visible or hidden.",
          "مرحبًا! أكبر فخ في الهندسة الفضائية أن تنسى أن الورقة ثنائية الأبعاد بينما المسألة ثلاثية الأبعاد. قبل أي برهان أعد بناء المجسم في ذهنك: الرؤوس والحروف والأوجه وما هو مرئي أو مخفي.",
          "Reconstruire le solide."),
    ]),
    ("Read the solid, separate fact from look", "نقرأ المجسم ونفصل الحقيقة عن المظهر", "Lire le solide", "", [
        T("Start from the labels, not the appearance: which vertices are joined, which edges bound each face. Changing the viewpoint does not change incidence. If two edges look equal or two lines look parallel, put that in a box called “looks true” until a given or a theorem appears. The drawing is a way of seeing, not a source of new facts.",
          "نبدأ من الأسماء لا من المظهر: أي رؤوس موصولة وأي حروف تحد كل وجه. تغيير زاوية الرسم لا يغيّر الاتصال. وإذا بدا حرفان متساويين أو مستقيمان متوازيين نضع ذلك مؤقتًا في خانة «يبدو صحيحًا» حتى نجد معطى أو مبرهنة. الرسم وسيلة رؤية لا مصدر حقائق جديدة.",
          "« Semble vrai » ≠ vrai."),
    ]),
    ("Plane sections", "المقاطع المستوية", "Sections planes", "", [
        T("A section starts from the intersection points between the cutting plane and the boundary of the solid. Join points only through faces the cut passes through. Never draw a polygon because its shape “looks logical”.",
          "يبدأ المقطع من نقاط التقاطع بين مستوي القطع وحدود المجسم. نصل النقاط فقط عبر أوجه يمر بها القطع. ولا نرسم مضلعًا لأن شكله «يبدو منطقيًا».",
          "Relier par des faces valides."),
    ]),
    ("Lines, planes and parallel planes", "المستقيمات والمستويات والتوازي", "Droites, plans, parallélisme", "", [
        T("Name the line and the plane exactly, write the incidence data, then conclude. In space, projection can fool the eye about an intersection, so look for a proved common point or an explicit relation. And never deduce parallelism from the apparent distance in a drawing: use a criterion only after checking every hypothesis.",
          "نسمّي المستقيم والمستوي بدقة ونكتب معطيات الاتصال ثم نستنتج. في الفضاء قد يخدع الإسقاط العين في التقاطع، فنبحث عن نقطة مشتركة مثبتة أو علاقة صريحة. ولا نستنتج التوازي من المسافة الظاهرة في الرسم: نستعمل معيارًا بعد التحقق من كل فرضياته.",
          "Vérifie chaque hypothèse."),
    ]),
    ("Two error detectives", "محققان", "Deux détectives", "", [
        T("First: a student joined two section points because they were closest on the page. The right question: do they lie on one face cut by the plane? If not, the segment is unjustified. Second: a student said two planes are parallel because they are drawn as two separated parallelograms. We ask for a criterion, not an impression.",
          "الأول: وصل طالب نقطتي مقطع لأنهما الأقرب على الصفحة. السؤال الصحيح: هل تقعان على وجه واحد يقطعه المستوي؟ إن لم يكن فالقطعة غير مبرَّرة. الثاني: قال طالب إن مستويين متوازيان لأنهما مرسومان كمتوازيي أضلاع متباعدين. نطلب معيارًا لا انطباعًا.",
          "Un critère, pas une impression."),
    ]),
    ("Final challenge", "التحدي الأخير", "Défi final", "", [
        T("Given a solid, a cutting plane and some relations, write the chain. Any step that relies on the drawing alone is rejected until you justify it. Perspective helps you see; proof tells you what is true.",
          "إذا أُعطيت مجسمًا ومستوي قطع وبعض العلاقات اكتب السلسلة. وكل خطوة تعتمد على الرسم وحده تُرفض حتى تبررها. المنظور يساعدك على الرؤية، والبرهان يقول لك ما هو صحيح.",
          "La preuve dit le vrai."),
        F("GIVEN → spatial interpretation → justified construction → verification → conclusion"),
    ]),
]

EXERCISES = [
    EX("1", "", st("What changes when we rotate a solid, and what stays?", "ماذا يتغير وماذا يبقى عند تدوير المجسم؟", "Que change une rotation ?"), [T("Visibility changes; incidence stays.", "الرؤية تتغير والاتصال يبقى.", "Visibilité / incidence.")]),
    EX("2", "", st("When may two section points be joined?", "متى نصل بين نقطتي مقطع؟", "Relier deux points ?"), [T("When they lie on one face the plane cuts.", "عندما يقعان على وجه واحد يقطعه المستوي.", "Même face.")]),
    EX("3", "", st("Why is “they look parallel” not enough?", "لماذا لا تكفي عبارة «يبدوان متوازيين»؟", "Pourquoi pas assez ?"), [T("We need a criterion with checked hypotheses.", "نحتاج معيارًا بفرضيات متحققة.", "Critère.")]),
    EX("4", "", st("Write the final chain of reasoning.", "اكتب سلسلة الاستدلال النهائية.", "Chaîne finale."), [F("GIVEN → interpretation → construction → verification → conclusion")]),
]
