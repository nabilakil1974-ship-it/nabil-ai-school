"""Grade 10 Mathematics — Lines and planes."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G10-MATH-EN-025"
GRADE = 10
SUBJECT = "math"
TITLES = {"en": "Lines and planes", "ar": "المستقيمات والمستويات", "fr": "Droites et plans"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "A line looks drawn inside a parallelogram that represents a plane. Is it in the plane?", "opts": ["Not proved by the drawing", "Yes", "No", "Always"], "a": 0,
     "why": {"Yes": _w("Appearance is not proof.", "المظهر ليس برهانًا.", "Pas une preuve."),
             "No": _w("We cannot say either.", "لا نستطيع الجزم.", "Indéterminé."),
             "Always": _w("Needs incidence data.", "يحتاج معطيات الاتصال.", "Données.")}, "ok": "needs incidence"},
    {"q": "Two distinct non-parallel planes meet along …", "opts": ["a line", "a point only", "a plane", "nothing"], "a": 0,
     "why": {"a point only": _w("Think of two walls: a common edge.", "فكّر بجدارين: حافة مشتركة.", "Arête commune."),
             "a plane": _w("They are distinct.", "متمايزان.", "Distincts."),
             "nothing": _w("They are not parallel.", "غير متوازيين.", "Non parallèles.")}, "ok": "a line"},
    {"q": "Change the viewpoint. The geometric relation …", "opts": ["stays the same", "changes", "disappears", "doubles"], "a": 0,
     "why": {"changes": _w("Only the visual projection changes.", "يتغير الإسقاط البصري فقط.", "Projection."),
             "disappears": _w("It stays.", "تبقى.", "Reste."),
             "doubles": _w("Nonsense.", "غير منطقي.", "Non.")}, "ok": "unchanged"},
]

THEORY = [
    ("Space needs precise words", "الفضاء يحتاج لغة دقيقة", "L'espace exige des mots précis", "251", [
        T("Hello! In plane geometry you saw everything on one sheet. In space, a line may lie in a plane, cross it, or be in a position that cannot be judged from the drawing alone. So we begin with precise language before the picture.",
          "مرحبًا! في الهندسة المستوية كنت ترى كل شيء على ورقة واحدة. في الفضاء قد يكون المستقيم داخل مستوٍ أو يقطعه أو في وضع لا يجوز الحكم عليه من الرسم وحده. لذلك نبدأ باللغة الدقيقة قبل الصورة.",
          "Langage précis avant l'image."),
    ]),
    ("The method", "الطريقة", "La méthode", "251", [
        T("Name the objects. Write the givens. Classify the requested relation. Use only established relations. Write the conclusion with its reason.",
          "نسمّي الكائنات. نكتب المعطيات. نصنّف العلاقة المطلوبة. نستعمل العلاقات المثبتة فقط. نكتب الاستنتاج مع السبب.",
          "Nommer, donner, relier, justifier."),
        F("name → given → relation → reason → conclusion"),
    ]),
    ("Incidence must be justified", "الاتصال يجب أن يُبرَّر", "L'incidence se justifie", "252", [
        T("If the question says line d is contained in plane α, then the points of d lie in α. If it gives two planes and a stated intersection, we treat the intersection as described; we do not draw a random line and call it the intersection. We never add containment from a sketch alone.",
          "إذا قال السؤال إن المستقيم d محتوى في المستوي α فنقاط d تقع في α. وإذا أعطى مستويين وتقاطعًا معلنًا نتعامل مع التقاطع كما تصفه المعطيات، ولا نرسم خطًا عشوائيًا ونسمّيه التقاطع. ولا نضيف الاحتواء من الرسم وحده.",
          "Jamais d'incidence par le dessin."),
    ]),
    ("Question", "سؤال", "Question", "252", [
        T("Can I prove that a line lies in a plane because it looks drawn inside the parallelogram representing the plane? No. The parallelogram is only a representation; a proof needs incidence data or an established result.",
          "هل أثبت أن مستقيمًا يقع في مستوٍ لأنه يبدو مرسومًا داخل متوازي الأضلاع الذي يمثل المستوي؟ لا. المتوازي مجرد تمثيل، والبرهان يحتاج معطيات اتصال أو نتيجة مثبتة.",
          "Le parallélogramme n'est qu'une représentation."),
    ]),
    ("Error detective", "المحقق", "Détective", "253", [
        T("In a perspective drawing two lines may seem to cross on paper while sitting in different positions in space. Always ask: is the intersection point really common, according to the givens?",
          "في الرسم المنظوري قد يبدو مستقيمان متقاطعين على الورقة بينما هما في وضعين مختلفين في الفضاء. نسأل دائمًا: هل نقطة التقاطع مشتركة فعلًا وفق المعطيات؟",
          "Le point commun est-il réel ?"),
    ]),
    ("Spatial challenge", "تحدٍّ فضائي", "Défi spatial", "253", [
        T("Imagine two rooms whose walls represent different planes. The common edge of two walls gives an intuition of an intersection line when the conditions fit. Now change your viewpoint: does the geometric relation change? No; only the visual projection does.",
          "تخيّل غرفتين تمثل جدرانهما مستويين مختلفين. الحافة المشتركة بين جدارين تعطي حدسًا عن مستقيم التقاطع عندما تكون الشروط مناسبة. الآن غيّر زاوية النظر: هل تتغير العلاقة الهندسية؟ لا، الذي يتغير هو الإسقاط البصري.",
          "Seule la projection change."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Line–plane relations need precise incidence information. A perspective sketch supports but does not prove. Always attach a justification to a spatial conclusion.",
          "علاقات المستقيم والمستوي تحتاج معلومات اتصال دقيقة. الرسم المنظوري يدعم ولا يبرهن. نرفق كل استنتاج فضائي بتبرير.",
          "Toujours justifier."),
    ]),
]

EXERCISES = [
    EX("1", "", st("What does it mean for a line to lie in a plane?", "ماذا يعني أن يقع مستقيم في مستوٍ؟", "Droite dans un plan ?"), [T("All its points belong to the plane.", "كل نقاطه تنتمي للمستوي.", "Tous ses points.")]),
    EX("2", "", st("What can two distinct non-parallel planes meet in?", "بماذا يتقاطع مستويان متمايزان غير متوازيين؟", "Intersection de deux plans."), [T("A line.", "مستقيم.", "Une droite.")]),
    EX("3", "", st("Why is a perspective drawing alone not proof?", "لماذا لا يكفي الرسم المنظوري برهانًا؟", "Pourquoi pas une preuve ?"), [T("Appearance can mislead.", "المظهر قد يخدع.", "Apparence trompeuse.")]),
    EX("4", "", st("Write the justification chain.", "اكتب سلسلة التبرير.", "Chaîne de justification."), [F("name → given → relation → reason → conclusion")]),
]
