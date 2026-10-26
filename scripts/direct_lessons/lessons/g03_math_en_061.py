"""Grade 3 Mathematics — Problems (7) (method lesson from the teacher plan; book problems not reproduced)."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G03-MATH-EN-061"
GRADE = 3
SUBJECT = "math"
TITLES = {"en": "Problems (7)", "ar": "مسائل (7)", "fr": "Problèmes (7)"}

THEORY = [
    ("Before choosing an operation", "قبل اختيار العملية", "Avant de choisir l'opération", "128", [
        T("Hello, champion! First find the question and the unknown, then keep only the data that helps. A shop has 36 red and 28 blue balloons; 15 red are sold. How many red are left? Blue is not needed. 36 − 15 = 21.",
          "مرحبًا يا بطل! نجد السؤال والمجهول أولًا ثم نحتفظ بالمعطيات المفيدة فقط. في متجر 36 بالونًا أحمر و28 أزرق، وبيع 15 أحمر. كم بقي من الأحمر؟ الأزرق غير لازم. 36 − 15 = 21.",
          "Question, inconnue, données utiles. 36 − 15 = 21 ; le bleu est inutile."),
        F("36 − 15 = 21"),
    ]),
    ("The solution path", "مسار الحل", "Le chemin de résolution", "128", [
        T("Read → select evidence → model → plan → calculate → interpret → verify. Always go back to the story and ask: does my answer make sense, with its unit?",
          "نقرأ ثم نختار المعطيات ثم نمثّل ثم نخطّط ثم نحسب ثم نفسّر ثم نتحقق. ونعود دائمًا إلى القصة: هل الجواب معقول مع وحدته؟",
          "Lire, choisir, modéliser, planifier, calculer, interpréter, vérifier."),
        F("READ → SELECT → MODEL → PLAN → CALCULATE → INTERPRET → VERIFY"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("An answer is valid only if every step is supported by the problem. Never invent missing data.", "الجواب صحيح فقط إذا كانت كل خطوة مدعومة بالمسألة. لا نخترع معطيات ناقصة.", "On n'invente pas de données."),
    ]),
]

EXERCISES = [
    EX("1", "128", st("A box holds 6 pens. How many pens in 7 boxes?", "في العلبة 6 أقلام. كم قلمًا في 7 علب؟", "6 stylos par boîte : 7 boîtes ?"), [F("6 × 7 = 42")]),
    EX("2", "128", st("48 stickers are shared equally among 6 children: how many each? Check.", "تُوزَّع 48 ملصقًا بالتساوي على 6 أطفال: كم لكل طفل؟ تحقق.", "48 vignettes entre 6 enfants."), [F("48 ÷ 6 = 8      8 × 6 = 48")]),
    EX("3", "128", st("Error detective: 36 red, 28 blue, 15 red sold, answer 36 + 28 − 15.", "المحقق: 36 أحمر و28 أزرق وبيع 15 أحمر، والجواب 36 + 28 − 15.", "Détective : 36 + 28 − 15."), [F("36 − 15 = 21"), T("Blue is irrelevant to the question.", "الأزرق لا علاقة له بالسؤال.", "Le bleu est inutile.")]),
]
