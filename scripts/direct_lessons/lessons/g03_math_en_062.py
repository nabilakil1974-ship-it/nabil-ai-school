"""Grade 3 Mathematics — Problems (8) (method lesson from the teacher plan; book problems not reproduced)."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G03-MATH-EN-062"
GRADE = 3
SUBJECT = "math"
TITLES = {"en": "Problems (8)", "ar": "مسائل (8)", "fr": "Problèmes (8)"}

THEORY = [
    ("One step or several?", "خطوة واحدة أم عدة خطوات؟", "Une étape ou plusieurs ?", "129", [
        T("Hello, champion! Some problems need several connected steps. A class has 4 rows of 6 chairs and 5 more chairs are added. First 4 × 6 = 24, then 24 + 5 = 29 chairs. We name the intermediate unknown first.",
          "مرحبًا يا بطل! بعض المسائل تحتاج عدة خطوات مترابطة. في صف 4 صفوف من 6 كراسٍ ثم أُضيفت 5 كراسٍ. أولًا 4 × 6 = 24 ثم 24 + 5 = 29 كرسيًّا. نسمّي المجهول الوسيط أولًا.",
          "4 rangées de 6 chaises + 5 : 4 × 6 = 24, puis 24 + 5 = 29."),
        F("4 × 6 = 24      24 + 5 = 29"),
    ]),
    ("Check the whole chain", "نتحقق من السلسلة كلها", "Vérifier toute la chaîne", "129", [
        T("A final answer is valid only when the complete chain is consistent. If something is wrong, repair the first unsupported step, not only the final number.",
          "الجواب النهائي صحيح فقط إذا كانت السلسلة كلها متسقة. وإذا وُجد خطأ نصحّح أول خطوة غير مدعومة لا الرقم الأخير فقط.",
          "On corrige la première étape fautive."),
        F("READ → DECOMPOSE → CHOOSE → SOLVE → INTERPRET → VERIFY"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Break a big problem into small justified steps and write a short reasoning chain.", "نقسّم المسألة الكبيرة إلى خطوات صغيرة معلَّلة ونكتب سلسلة تفكير قصيرة.", "Découper en étapes justifiées."),
    ]),
]

EXERCISES = [
    EX("1", "129", st("3 bags of 8 apples; 5 apples are eaten. How many are left?", "3 أكياس في كلٍّ 8 تفاحات وأُكلت 5. كم بقي؟", "3 sacs de 8 pommes ; 5 mangées."), [F("3 × 8 = 24      24 − 5 = 19")]),
    EX("2", "130", st("72 pupils sit in groups of 8. How many groups?", "يجلس 72 تلميذًا في مجموعات من 8. كم مجموعة؟", "72 élèves par groupes de 8."), [F("72 ÷ 8 = 9      9 × 8 = 72")]),
    EX("3", "130", st("Summarize one multi-step solution in a short chain.", "لخّص حلًّا متعدد الخطوات في سلسلة قصيرة.", "Résume une solution en chaîne."), [T("For example: 4 rows × 6 = 24, plus 5 = 29.", "مثلًا: 4 صفوف × 6 = 24 ثم + 5 = 29.", "4 × 6 = 24, + 5 = 29.")]),
]
