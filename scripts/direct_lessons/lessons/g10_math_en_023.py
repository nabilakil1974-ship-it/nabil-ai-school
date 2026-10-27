"""Grade 10 Mathematics — Plane representation of solids."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G10-MATH-EN-023"
GRADE = 10
SUBJECT = "math"
TITLES = {"en": "Plane representation of solids", "ar": "التمثيل المستوي للمجسمات", "fr": "Représentation plane des solides"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "Two edges are drawn with the same length. Are they equal?", "opts": ["Only if given or proved", "Always", "Never", "Yes, if they look equal"], "a": 0,
     "why": {"Always": _w("A drawing distorts lengths.", "الرسم يشوّه الأطوال.", "Le dessin déforme."),
             "Never": _w("They may be equal if given.", "قد يتساويان إن أُعطي ذلك.", "Si donné."),
             "Yes, if they look equal": _w("Appearance is not proof.", "المظهر ليس برهانًا.", "Pas une preuve.")}, "ok": "needs data"},
    {"q": "We rotate the solid. What may change?", "opts": ["Which edges are visible", "Names of vertices", "Which edge bounds which face", "Number of faces"], "a": 0,
     "why": {"Names of vertices": _w("Labels keep identity.", "الأسماء تحفظ الهوية.", "Identité."),
             "Which edge bounds which face": _w("Incidence stays.", "الاتصال يبقى.", "Incidence."),
             "Number of faces": _w("The solid is unchanged.", "المجسم لم يتغير.", "Inchangé.")}, "ok": "visibility only"},
    {"q": "Hidden edges are usually drawn …", "opts": ["dashed", "thicker", "in the same style", "not at all"], "a": 0,
     "why": {"thicker": _w("Visible edges are solid lines.", "المرئية خطوط متصلة.", "Traits pleins."),
             "in the same style": _w("We must tell them apart.", "يجب التمييز.", "Distinguer."),
             "not at all": _w("They still exist.", "ما زالت موجودة.", "Elles existent.")}, "ok": "dashed"},
]

THEORY = [
    ("A drawing is not a copy", "الرسم ليس نسخة", "Un dessin n'est pas une copie", "235", [
        T("Hello! When I draw a 3D solid on flat paper, I do not transport the solid itself. I make a representation that helps your mind rebuild the space. So the first rule: do not measure from the drawing unless the question allows it, and never treat an angle that looks right or two sides that look equal as a geometric fact.",
          "مرحبًا! عندما أرسم مجسمًا ثلاثي الأبعاد على ورقة مسطحة فأنا لا أنقل المجسم نفسه، بل أصنع تمثيلًا يساعد عقلك على إعادة بناء الفضاء. القاعدة الأولى: لا نقيس من الرسم ما لم يسمح السؤال، ولا نعدّ زاوية تبدو قائمة أو ضلعين يبدوان متساويين حقيقة هندسية تلقائيًا.",
          "Le dessin ne prouve rien."),
    ]),
    ("Visible and hidden", "المرئي والمخفي", "Visible et caché", "235", [
        T("Imagine a transparent box. Some edges are in front and some behind. A good drawing needs conventions that separate visible from hidden information, usually solid lines and dashed lines. Labels keep the identity of vertices and faces even if the viewpoint changes.",
          "تخيّل صندوقًا شفافًا. بعض الحروف أمامك وبعضها خلف المجسم. الرسم الجيد يحتاج اصطلاحات تميّز المرئي من المخفي، عادةً خط متصل وخط متقطع. والأسماء تحفظ هوية الرؤوس والأوجه ولو تغيّر المنظور.",
          "Traits pleins / pointillés."),
        F("visible edge ———      hidden edge - - - -"),
    ]),
    ("What stays, what changes", "ما يبقى وما يتغير", "Ce qui reste", "236", [
        T("If I change the viewing angle, do the vertex names change? Does a given edge stop belonging to a given face? No. What changes is appearance. The incidence structure stays.",
          "إذا غيّرت زاوية النظر هل تتغير أسماء الرؤوس؟ وهل يتوقف حرف معيّن عن الانتماء إلى وجه معيّن؟ لا. الذي يتغير هو المظهر، أما بنية الاتصال فتبقى.",
          "Apparence change, incidence reste."),
    ]),
    ("How to read a drawing", "كيف نقرأ الرسم", "Comment lire", "236", [
        T("(1) Identify the vertices. (2) Follow each edge between two vertices. (3) Gather the edges that bound one face. (4) Separate visible from hidden. (5) Reject any metric conclusion that comes from the shape of the drawing alone.",
          "(1) نحدد الرؤوس. (2) نتتبع كل حرف بين رأسين. (3) نجمع الحروف التي تحد وجهًا واحدًا. (4) نميّز المرئي من المخفي. (5) نرفض أي استنتاج قياسي جاء من شكل الرسم وحده.",
          "Cinq étapes de lecture."),
    ]),
    ("Error detective", "المحقق", "Détective", "237", [
        T("A student says two edges are equal because they are drawn with the same length. Ask: is the equality given? Does the type of solid announced force it? Have we proved it? If not, the drawing alone is not enough.",
          "قال طالب إن حرفين متساويان لأنهما مرسومان بالطول نفسه. نسأل: هل المساواة معطاة؟ هل يفرضها نوع المجسم المعلن؟ هل أثبتناها؟ إن لم يكن فالرسم وحده لا يكفي.",
          "Donné ? Imposé ? Prouvé ?"),
    ]),
    ("Challenge", "تحدٍّ", "Défi", "237", [
        T("Pick one vertex of a solid and list every edge that meets there and every face that contains it. Now imagine turning the solid by 90°. Which of these relations change? Visibility may change; incidence does not.",
          "اختر رأسًا واحدًا في مجسم واذكر كل الحروف المتصلة به وكل الأوجه التي تحتويه. الآن تخيّل دوران المجسم 90°: أي علاقة تتغير؟ الرؤية قد تتغير أما الاتصال فلا.",
          "Visibilité change, incidence non."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("2D sketch → representation of a 3D structure. Labels preserve identity. Visible or hidden depends on viewpoint. Apparent lengths and angles are not proof. Rebuild the solid before solving.",
          "رسم مستوٍ ← تمثيل لبنية ثلاثية الأبعاد. الأسماء تحفظ الهوية. المرئي والمخفي يتبعان المنظور. الأطوال والزوايا الظاهرة ليست برهانًا. نعيد بناء المجسم قبل الحل.",
          "Reconstruire le solide."),
    ]),
]

EXERCISES = [
    EX("1", "", st("Why is a plane drawing not a metric copy?", "لماذا الرسم المستوي ليس نسخة قياسية؟", "Pourquoi pas une copie ?"), [T("It distorts lengths and angles.", "يشوّه الأطوال والزوايا.", "Il déforme.")]),
    EX("2", "", st("What do labels preserve?", "ماذا تحفظ الأسماء؟", "Que gardent les noms ?"), [T("The identity of vertices and faces.", "هوية الرؤوس والأوجه.", "L'identité.")]),
    EX("3", "", st("Error detective: equal because drawn equal.", "المحقق: متساويان لأنهما مرسومان متساويين.", "Détective."), [T("Needs given data or proof.", "يحتاج معطى أو برهانًا.", "Donnée ou preuve.")]),
    EX("4", "", st("After a 90° turn, what changes and what stays?", "بعد دوران 90°: ما الذي يتغير وما الذي يبقى؟", "Après 90°."), [T("Visibility changes; incidence stays.", "الرؤية تتغير والاتصال يبقى.", "Visibilité / incidence.")]),
]
