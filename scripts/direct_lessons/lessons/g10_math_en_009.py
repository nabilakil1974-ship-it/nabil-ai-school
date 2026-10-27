"""Grade 10 Mathematics — Applications of vector operations (source-controlled; general examples)."""
from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.lessons.g10_math_en_008 import arrows

LESSON_ID = "G10-MATH-EN-009"
GRADE = 10
SUBJECT = "math"
TITLES = {"en": "Applications of vector operations", "ar": "تطبيقات العمليات على المتجهات", "fr": "Applications des opérations sur les vecteurs"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "A→B, B→C, C→E: the resultant is ?", "opts": ["AE", "AC", "BE", "CE"], "a": 0,
     "why": {"AC": _w("The last step reaches E, not C.", "الخطوة الأخيرة تصل إلى E لا C.", "On arrive en E."),
             "BE": _w("The start point is A.", "نقطة البداية A.", "Le départ est A."),
             "CE": _w("That is only the last step.", "هذه الخطوة الأخيرة فقط.", "Dernière étape seule.")}, "ok": "AB + BC + CE = AE"},
    {"q": "Does AB = CD (lengths) prove vector AB = vector CD?", "opts": ["No", "Yes", "Only if drawn well", "Always"], "a": 0,
     "why": {"Yes": _w("Vectors also need the same direction and sense.", "المتجهان يحتاجان الحامل والمنحى نفسيهما أيضًا.", "Direction et sens aussi."),
             "Only if drawn well": _w("A drawing is not proof.", "الرسم ليس برهانًا.", "Un dessin n'est pas une preuve."),
             "Always": _w("Equal lengths can have different senses.", "قد تتساوى الأطوال وتختلف الأحناء.", "Sens possibles différents.")}, "ok": "equal lengths ≠ equal vectors"},
]

THEORY = [
    ("Three columns", "ثلاثة أعمدة", "Trois colonnes", "", [
        T("Hello! In this lesson we use vectors to prove geometry. Think in three columns: GIVEN GEOMETRY → VECTOR LANGUAGE → GEOMETRIC CONCLUSION. A fact enters the middle column only if it is given or already proved, never because the drawing suggests it.",
          "مرحبًا! نستعمل المتجهات هنا لإثبات خصائص هندسية. نفكر في ثلاثة أعمدة: معطى هندسي ← لغة المتجهات ← نتيجة هندسية. ولا تدخل معلومة إلى العمود الأوسط إلا إذا كانت معطاة أو مثبتة، لا لأن الرسم يوحي بها.",
          "Donné → langage vectoriel → conclusion."),
    ]),
    ("Chains of displacements", "سلاسل الانتقالات", "Chaînes de déplacements", "", [
        T("A→B, B→C, C→E: we start at A and finish at E, so the resultant is AE. Each step connects head to tail. We do not need the lengths for this.",
          "A→B وB→C وC→E: نبدأ من A وننتهي عند E فالمحصّلة AE. كل خطوة تتصل بالتي قبلها (رأس بذيل). ولا نحتاج الأطوال لذلك.",
          "AB + BC + CE = AE."),
        arrows({"A": (60, 300), "B": (220, 130), "C": (420, 250), "E": (590, 100)}, ["A", "B", "C", "E"], res=("A", "E")),
        F("AB + BC + CE = AE"),
    ]),
    ("Vector equality versus length equality", "تساوي المتجهات وتساوي الأطوال", "Égalité de vecteurs ou de longueurs", "", [
        T("Knowing only that the lengths AB and CD are equal does not give vector AB = vector CD: a vector also has direction and sense. Always ask: is the given about lengths or about vectors?",
          "معرفة أن الطولين AB وCD متساويان فقط لا تعطي المتجه AB = المتجه CD: فللمتجه حامل ومنحى أيضًا. نسأل دائمًا: هل المعطى عن أطوال أم عن متجهات؟",
          "Longueurs égales ≠ vecteurs égaux."),
    ]),
    ("Six proof questions", "ستة أسئلة للبرهان", "Six questions", "", [
        T("(1) What exactly is given? (2) What must be proved? (3) Which vectors represent the data? (4) Which equality can I justify? (5) What does it give after simplifying? (6) What does the result mean geometrically? Final check: did anything slip in from the drawing alone?",
          "(1) ما المعطيات حرفيًا؟ (2) ما المطلوب إثباته؟ (3) أي متجهات تمثّل المعطيات؟ (4) أي مساواة أستطيع تبريرها؟ (5) ماذا تعطي بعد التبسيط؟ (6) ما معنى النتيجة هندسيًا؟ وفحص أخير: هل تسللت معلومة من الرسم وحده؟",
          "Six questions avant chaque preuve."),
        F("GIVEN → WANT → VECTOR RELATIONS → CONCLUSION"),
    ]),
    ("Traps", "فخاخ", "Pièges", "", [
        T("The drawing trap: two segments that look parallel are not proved parallel. The label trap: AB + BC = AC is not \"cancelling B\"; the two moves connect at B. A proof is complete only when we translate the vector result back into geometry.",
          "فخ الرسم: قطعتان تبدوان متوازيتين لم يثبت توازيهما. وفخ الحروف: AB + BC = AC ليس «حذف B»؛ بل الانتقالان يتصلان عند B. ولا يكتمل البرهان إلا بترجمة النتيجة المتجهية إلى لغة الهندسة.",
          "Un dessin n'est pas une preuve."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Every statement needs a given, a definition or a proved reason.", "كل عبارة تحتاج إلى معطى أو تعريف أو سبب مثبت.", "Chaque affirmation a une raison."),
        F("Vector equality ≠ length equality      Drawing = visualization, not proof"),
    ]),
]

EXERCISES = [
    EX("1", "", st("A→B, B→C, C→E: express the resultant.", "A→B وB→C وC→E: عبّر عن المحصّلة.", "Exprime la résultante."), [F("AB + BC + CE = AE")]),
    EX("2", "", st("Error detective: \"these segments look parallel, so their vectors are parallel\".", "المحقق: «القطعتان تبدوان متوازيتين فمتجهاهما متوازيان».", "Détective : elles semblent parallèles."), [T("Where is the given or the proof? Without it the sentence is unjustified: the drawing is not a premise.", "أين المعطى أو البرهان؟ بدونه العبارة غير مبرَّرة: الرسم ليس مقدمة.", "Le dessin n'est pas une hypothèse.")]),
    EX("3", "", st("Error detective: \"AB + BC = AC because the B's cancel\".", "المحقق: «AB + BC = AC لأن الحرفين B يُحذفان».", "Détective : les B se simplifient."), [T("The real reason: the first move ends at B and the second starts at B.", "السبب الحقيقي: الانتقال الأول ينتهي عند B والثاني يبدأ من B.", "Le premier déplacement finit en B, le second y commence.")]),
    EX("4", "", st("Does AB = CD (lengths) prove vector AB = vector CD?", "هل يثبت AB = CD (طولان) أن المتجه AB = المتجه CD؟", "AB = CD (longueurs) prouve-t-il l'égalité des vecteurs ?"), [T("No: direction and sense are needed too.", "لا: يلزم الحامل والمنحى أيضًا.", "Non : direction et sens aussi.")]),
    EX("5", "", st("Fill the four boxes for a problem: GIVEN / WANT / VECTOR RELATIONS / CONCLUSION.", "املأ الخانات الأربع: المعطى / المطلوب / العلاقات المتجهية / النتيجة.", "Remplis : donné / à prouver / relations / conclusion."), [T("If you are stuck, name which box is missing before looking at the next line.", "إن تعثّرت فسمِّ الخانة الناقصة قبل أن تنظر إلى السطر التالي.", "Nomme la case manquante.")]),
]
