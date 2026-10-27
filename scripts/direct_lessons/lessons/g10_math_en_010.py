"""Grade 10 Mathematics — Position in the plane (source-controlled; general examples)."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G10-MATH-EN-010"
GRADE = 10
SUBJECT = "math"
TITLES = {"en": "Position in the plane", "ar": "الموضع في المستوي", "fr": "Position dans le plan"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "The sketch shows A, B, C almost on a line, but the text does not say so. It is…", "opts": ["ASSUMED", "GIVEN", "PROVED", "obvious"], "a": 0,
     "why": {"GIVEN": _w("Not written in the problem.", "غير مكتوب في المسألة.", "Pas écrit."),
             "PROVED": _w("Nothing proves it.", "لا شيء يثبته.", "Rien ne le prouve."),
             "obvious": _w("\"Looks true\" is not a reason.", "«يبدو صحيحًا» ليس سببًا.", "« Ça semble vrai » ne suffit pas.")}, "ok": "ASSUMED: cannot enter the proof"},
    {"q": "Can we call M the midpoint of [AB] because it looks halfway?", "opts": ["No", "Yes", "Only if measured", "Always"], "a": 0,
     "why": {"Yes": _w("A midpoint must be stated or proved.", "منتصف القطعة يجب أن يُذكر أو يُثبَت.", "À énoncer ou démontrer."),
             "Only if measured": _w("Measuring a sketch proves nothing.", "قياس رسم تخطيطي لا يثبت شيئًا.", "Mesurer un croquis ne prouve rien."),
             "Always": _w("Looks can mislead.", "المظهر قد يخدع.", "L'apparence trompe.")}, "ok": "No"},
]

THEORY = [
    ("Given or only looks true?", "معطى أم يبدو صحيحًا فقط؟", "Donné ou seulement apparent ?", "103", [
        T("Hello! In geometry the eye helps but can deceive. Three points may look aligned, two sides may look parallel, but \"looks\" is not a proof. The key habit: separate what is GIVEN from what is ASSUMED from the drawing. A diagram organizes information; it does not create facts.",
          "مرحبًا! في الهندسة تساعدنا العين لكنها قد تخدعنا. قد تبدو ثلاث نقاط على استقامة واحدة أو ضلعان متوازيين لكن «يبدو» ليس برهانًا. العادة الأساسية: نفصل ما هو معطى عمّا نفترضه من الرسم. المخطط ينظّم المعلومات ولا يخلق حقائق.",
          "Distinguer le donné de l'apparent : un dessin ne crée pas de faits."),
        F("GIVEN → may be used      ASSUMED from the drawing → cannot enter a proof"),
    ]),
    ("Point, vector, relation", "نقطة ومتجه وعلاقة", "Point, vecteur, relation", "103", [
        T("The letter A alone names a point. The vector AB is a displacement from A to B. A relation such as alignment or parallelism is a property that needs a given or a proof. Keeping these apart prevents meaningless notation.",
          "الحرف A وحده اسم نقطة. والمتجه AB انتقال من A إلى B. والعلاقة كالاستقامة أو التوازي خاصية تحتاج معطى أو برهانًا. الفصل بينها يمنع كتابة رموز بلا معنى.",
          "Point ≠ vecteur ≠ relation."),
    ]),
    ("Construct, then verify", "نبني ثم نتحقق", "Construire puis vérifier", "103", [
        T("If M is obtained from P by the displacement u, start at P and apply u exactly. Then go back to the original condition and check it. Construction first, verification second, never drawing and guessing.",
          "إذا كانت M تنتج عن P بالانتقال u فنبدأ من P ونطبّق u بدقة. ثم نعود إلى الشرط الأصلي ونتحقق منه. بناء ثم تحقق، لا رسم ثم تخمين.",
          "Construire à partir des conditions, puis vérifier."),
        F("M = P + u  →  verify PM = u"),
    ]),
    ("Do not measure a sketch", "لا نقيس رسمًا تخطيطيًا", "Ne pas mesurer un croquis", "104", [
        T("A schematic drawing may not be to scale, so measuring it proves nothing. A midpoint, equal lengths or parallelism must come from a given or a theorem. This habit prepares us for coordinates: instead of \"the point looks here\", we describe it exactly and test relations by calculation.",
          "قد لا يكون الرسم التخطيطي بمقياس صحيح فلا يثبت قياسُه شيئًا. المنتصف وتساوي الأطوال والتوازي يجب أن تأتي من معطى أو مبرهنة. وهذه العادة تُعدّنا للإحداثيات: بدل «النقطة تبدو هنا» نصفها بدقة ونختبر العلاقات بالحساب.",
          "Pas de preuve par la mesure du dessin."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("GIVEN first, representation second, conclusion last.", "المعطى أولًا ثم التمثيل ثم النتيجة.", "Donné, représentation, conclusion."),
        F("POINTS → GIVENS → WANT → ONE JUSTIFIED STEP AT A TIME → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "", st("Sort: \"A, B, C look aligned\" (not stated). GIVEN, PROVED or ASSUMED?", "صنّف: «A وB وC تبدو على استقامة» (غير مذكور). معطى أم مثبت أم مفترض؟", "« A, B, C semblent alignés » (non énoncé) ?"), [T("ASSUMED: it cannot be used unless proved.", "مفترض: لا يُستعمل إلا بعد إثباته.", "Supposé.")]),
    EX("2", "", st("M looks halfway between A and B. Is M the midpoint?", "M تبدو في منتصف AB. هل هي منتصفها؟", "M semble au milieu. Est-ce le milieu ?"), [T("Not until it is stated or proved.", "ليس قبل أن يُذكر أو يُثبَت.", "Pas sans énoncé ni preuve.")]),
    EX("3", "", st("A student measures a sketch and says two lengths are equal. What is wrong?", "قاس طالب رسمًا تخطيطيًا وقال إن طولين متساويان. ما الخطأ؟", "Un élève mesure un croquis. Quelle erreur ?"), [T("The sketch may not be to scale; look for a given or a theorem.", "قد لا يكون الرسم بمقياس؛ نبحث عن معطى أو مبرهنة.", "Le croquis n'est pas à l'échelle.")]),
    EX("4", "", st("Describe the steps to construct a point from a condition and verify it.", "صف خطوات بناء نقطة من شرط ثم التحقق منها.", "Décris : construire un point puis vérifier."), [T("Restate the condition, construct from the data only, then test the original condition.", "نعيد صياغة الشرط ثم نبني من المعطيات فقط ثم نختبر الشرط الأصلي.", "Reformuler, construire, tester.")]),
]
