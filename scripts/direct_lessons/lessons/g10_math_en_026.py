"""Grade 10 Mathematics — Parallel planes."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G10-MATH-EN-026"
GRADE = 10
SUBJECT = "math"
TITLES = {"en": "Parallel planes", "ar": "المستويات المتوازية", "fr": "Plans parallèles"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "Two planes look parallel in a perspective drawing. Enough to conclude?", "opts": ["No: go back to the givens", "Yes", "Yes if the picture is neat", "Only for horizontal planes"], "a": 0,
     "why": {"Yes": _w("Appearance is never enough.", "المظهر لا يكفي أبدًا.", "Jamais suffisant."),
             "Yes if the picture is neat": _w("A neat drawing is not a proof.", "الرسم الأنيق ليس برهانًا.", "Pas une preuve."),
             "Only for horizontal planes": _w("Same rule for all planes.", "القاعدة نفسها.", "Même règle.")}, "ok": "need a theorem"},
    {"q": "Before using a theorem we must …", "opts": ["check every hypothesis", "use it at once", "draw a bigger figure", "measure"], "a": 0,
     "why": {"use it at once": _w("A missing hypothesis breaks the proof.", "فرضية ناقصة تكسر البرهان.", "Hypothèse manquante."),
             "draw a bigger figure": _w("Drawing is not proof.", "الرسم ليس برهانًا.", "Non."),
             "measure": _w("Do not measure a drawing.", "لا نقيس الرسم.", "Non.")}, "ok": "check hypotheses"},
    {"q": "Rotating the camera around two fixed planes changes …", "opts": ["only how parallel they look", "whether they are parallel", "their distance", "the givens"], "a": 0,
     "why": {"whether they are parallel": _w("The spatial relation is fixed.", "العلاقة المكانية ثابتة.", "Fixe."),
             "their distance": _w("The planes are fixed.", "المستويان ثابتان.", "Fixes."),
             "the givens": _w("They stay.", "تبقى.", "Restent.")}, "ok": "projection only"},
]

THEORY = [
    ("An intuition, then proof", "حدس ثم برهان", "Intuition puis preuve", "261", [
        T("Hello! Picture two different horizontal floors in an ideal building. However far we extend them, they never meet. That is a good intuition for parallel planes, but in mathematics a picture is not enough: we need conditions and relations that let us prove the parallelism.",
          "مرحبًا! تخيّل طابقين أفقيين مختلفين في مبنى مثالي. مهما مددناهما لا يلتقيان. هذا حدس جيد لفكرة المستويات المتوازية، لكن في الرياضيات لا نكتفي بالصورة: نحتاج الشروط والعلاقات التي تسمح بإثبات التوازي.",
          "Deux plans distincts qui ne se coupent pas."),
    ]),
    ("Before any proof", "قبل أي برهان", "Avant toute preuve", "261", [
        T("Write first: what is the first plane? the second? which lines or points are given in each? which parallelism or incidence relations are established? Only then choose the logical route.",
          "نكتب أولًا: ما المستوي الأول؟ والثاني؟ ما المستقيمات أو النقاط المعطاة في كل منهما؟ وما علاقات التوازي أو الاتصال المثبتة؟ بعد ذلك فقط نختار الطريق المنطقي.",
          "Plans, objets, relations."),
    ]),
    ("A drawing does not prove", "الرسم لا يبرهن", "Un dessin ne prouve pas", "262", [
        T("Drawing two separated parallelograms and calling them parallel planes is not enough. The drawing represents the conclusion or helps us understand it, but it does not make a proof. If two planes look parallel in perspective, return to the givens and find the relation or theorem that proves it.",
          "لا يكفي أن نرسم متوازيي أضلاع متباعدين ونسميهما مستويين متوازيين. الرسم يمثل الاستنتاج أو يساعد على فهمه لكنه لا يصنع برهانًا. وإذا بدا مستويان متوازيين في الرسم المنظوري فنعود إلى المعطيات ونبحث عن علاقة أو مبرهنة تثبت ذلك.",
          "Retourne aux données."),
    ]),
    ("General reasoning", "استدلال عام", "Raisonnement général", "262", [
        T("If lines in plane α and corresponding lines in plane β are given, look for a suitable, established theorem before concluding α ∥ β. Never use a criterion we have not verified as if it were established.",
          "إذا أُعطيت علاقات بين مستقيمات في المستوي α وعلاقات مقابلة في المستوي β نبحث عن مبرهنة مناسبة ومثبتة قبل أن نستنتج α ∥ β. ولا نستعمل معيارًا لم نتحقق منه كأنه مثبت.",
          "Théorème établi d'abord."),
    ]),
    ("Error detective", "المحقق", "Détective", "263", [
        T("A student uses one single line and jumps to parallel planes with no further conditions. We stop him at the jump: which theorem allows this result? Were all its hypotheses checked? If not, the proof is incomplete.",
          "استعمل طالب مستقيمًا واحدًا فقط وقفز إلى المستويات المتوازية دون شروط إضافية. نوقفه عند القفزة نفسها: ما المبرهنة التي تسمح بهذه النتيجة؟ وهل تحققت كل فرضياتها؟ إن لم يكن فالبرهان ناقص.",
          "Une seule droite ne suffit pas."),
    ]),
    ("Camera experiment", "تجربة الكاميرا", "Expérience", "263", [
        T("Change the camera angle around two fixed planes. They may look more or less parallel on the screen, while the real spatial relation does not change. We separate projection from geometry.",
          "غيّر زاوية الكاميرا حول مستويين ثابتين. قد يبدوان أكثر أو أقل توازيًا على الشاشة بينما العلاقة المكانية الحقيقية لا تتغير. نفصل الإسقاط عن الهندسة.",
          "Projection ≠ géométrie."),
    ]),
    ("Challenge: proof skeleton", "تحدٍّ: هيكل البرهان", "Défi : squelette", "264", [
        T("Write a four-box skeleton. If you cannot fill the theorem-conditions box, you may not move to the conclusion.",
          "نكتب هيكلًا من أربع خانات. إذا لم تستطع ملء خانة شروط المبرهنة فلا يجوز الانتقال إلى الاستنتاج.",
          "Quatre cases."),
        F("GIVEN → THEOREM CONDITIONS → CHECK EACH CONDITION → CONCLUSION"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Parallel planes need proof. Perspective appearance is never enough. Auxiliary lines help only with justified relations. Check every hypothesis of a theorem before using it.",
          "المستويات المتوازية علاقة تحتاج برهانًا. المظهر المنظوري لا يكفي أبدًا. المستقيمات المساعدة مفيدة فقط مع علاقات مبرَّرة. نتحقق من كل فرضية في المبرهنة قبل استعمالها.",
          "Vérifie chaque hypothèse."),
    ]),
]

EXERCISES = [
    EX("1", "", st("What does it mean for two distinct planes to be parallel?", "ماذا يعني أن يكون مستويان متمايزان متوازيين؟", "Plans parallèles ?"), [T("They have no common point.", "لا نقطة مشتركة بينهما.", "Aucun point commun.")]),
    EX("2", "", st("Why must a conclusion follow from the givens, not perspective?", "لماذا يجب أن يأتي الاستنتاج من المعطيات لا من المنظور؟", "Pourquoi les données ?"), [T("Perspective can mislead.", "المنظور قد يخدع.", "Peut tromper.")]),
    EX("3", "", st("Error detective: one line, then parallel planes.", "المحقق: مستقيم واحد ثم مستويان متوازيان.", "Détective."), [T("Which theorem? Are its hypotheses checked?", "أي مبرهنة؟ وهل تحققت فرضياتها؟", "Quel théorème ?")]),
    EX("4", "", st("Write the proof skeleton.", "اكتب هيكل البرهان.", "Squelette."), [F("GIVEN → CONDITIONS → CHECK → CONCLUSION")]),
]
