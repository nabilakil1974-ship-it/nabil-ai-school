"""Grade 10 Mathematics — Statistical indicators (concept lesson; examples are NABIL's own, not textbook data)."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G10-MATH-EN-002"
GRADE = 10
SUBJECT = "math"
TITLES = {"en": "Statistical indicators", "ar": "المؤشرات الإحصائية", "fr": "Indicateurs statistiques"}

W = {"en": "Check the sum of value × frequency.", "ar": "راجع مجموع القيمة × التكرار.", "fr": "Vérifie la somme valeur × effectif."}
QUIZ = [
    {"q": "0×3 + 1×7 + 2×6 + 3×3 + 4×1 = ?", "opts": ["32", "30", "28", "20"], "a": 0, "why": {"30": W, "28": W, "20": W}, "ok": "32"},
    {"q": "Range of values 0 to 4 = ?", "opts": ["4", "5", "2", "0"], "a": 0,
     "why": {"5": {"en": "Range = largest − smallest = 4 − 0.", "ar": "المدى = الأكبر − الأصغر = 4 − 0.", "fr": "Étendue = 4 − 0."},
             "2": {"en": "Range = largest − smallest.", "ar": "المدى = الأكبر − الأصغر.", "fr": "Étendue = max − min."},
             "0": {"en": "Range = largest − smallest.", "ar": "المدى = الأكبر − الأصغر.", "fr": "Étendue = max − min."}}, "ok": "4 − 0 = 4"},
]

THEORY = [
    ("Which indicator?", "أيّ مؤشر؟", "Quel indicateur ?", "", [
        T("An indicator summarizes a distribution by one number. Central tendency: mean, median, mode. Dispersion: range. We use the 20-student sibling survey: 0 → 3, 1 → 7, 2 → 6, 3 → 3, 4 → 1.",
          "المؤشر يلخّص التوزيع بعدد واحد. مؤشرات النزعة المركزية: المتوسط والوسيط والمنوال. ومؤشر التشتت: المدى. نستعمل استبيان إخوة التلاميذ العشرين: 0 عند 3 و1 عند 7 و2 عند 6 و3 عند 3 و4 عند 1.",
          "Un indicateur résume une distribution : moyenne, médiane, mode, étendue."),
        F("value:  0  1  2  3  4"), F("frequency:  3  7  6  3  1"),
    ]),
    ("The mean", "المتوسط الحسابي", "La moyenne", "", [
        T("Mean = (sum of value × frequency) ÷ total frequency. Total of values: 0 + 7 + 12 + 9 + 4 = 32. Mean = 32 ÷ 20 = 1.6 siblings. The mean need not be a possible value.",
          "المتوسط = (مجموع القيمة × التكرار) ÷ مجموع التكرارات. مجموع القيم: 0 + 7 + 12 + 9 + 4 = 32. المتوسط = 32 ÷ 20 = 1.6 أخ. ولا يلزم أن يكون المتوسط قيمة ممكنة.",
          "Moyenne = somme(valeur × effectif) ÷ total = 32 ÷ 20 = 1,6."),
        F("0×3 + 1×7 + 2×6 + 3×3 + 4×1 = 32"), F("mean = 32 / 20 = 1.6"),
    ]),
    ("Mode and median", "المنوال والوسيط", "Mode et médiane", "", [
        T("Mode: the value with the greatest frequency: 1 (7 students). Median: the middle of the ordered data. With 20 values, take the 10th and 11th. Cumulative frequencies: 3, 10, 16, 19, 20. The 10th is 1 and the 11th is 2, so the median is 1.5.",
          "المنوال: القيمة الأكثر تكرارًا: 1 (عند 7 تلاميذ). الوسيط: وسط المعطيات المرتّبة. مع 20 قيمة نأخذ العاشرة والحادية عشرة. التكرارات التراكمية: 3 و10 و16 و19 و20. العاشرة 1 والحادية عشرة 2 فالوسيط 1.5.",
          "Mode : 1. Médiane : 10e = 1, 11e = 2, donc 1,5."),
        F("cumulative: 3, 10, 16, 19, 20      median = (1 + 2) / 2 = 1.5"),
    ]),
    ("Range and interpretation", "المدى والتفسير", "Étendue et interprétation", "", [
        T("Range = largest value − smallest value = 4 − 0 = 4. Interpret: on average a student has about 1.6 siblings, and the numbers vary over a range of 4. A mean lying outside the data's range is impossible: always check plausibility.",
          "المدى = أكبر قيمة − أصغر قيمة = 4 − 0 = 4. التفسير: لدى التلميذ في المتوسط نحو 1.6 أخ، وتتفاوت الأعداد على مدى 4. أما متوسط خارج مجال القيم فمستحيل: نتحقق دائمًا من معقولية النتيجة.",
          "Étendue = 4 − 0 = 4. Une moyenne hors des données est impossible."),
        F("range = 4 − 0 = 4"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Name the indicator, apply the right formula, keep exact values, interpret in context, check plausibility.", "نسمّي المؤشر ونطبّق القانون المناسب ونحتفظ بالقيم الدقيقة ونفسّر في السياق ونتحقق من المعقولية.", "Nommer, calculer, interpréter, vérifier."),
        F("INDICATOR → FORMULA → CALCULATE → INTERPRET → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "", st("Mean of 2, 4, 6, 8.", "المتوسط للأعداد 2 و4 و6 و8.", "Moyenne de 2, 4, 6, 8."), [F("2 + 4 + 6 + 8 = 20"), F("20 / 4 = 5")]),
    EX("2", "", st("Median of 3, 9, 5, 7, 1.", "الوسيط للأعداد 3 و9 و5 و7 و1.", "Médiane de 3, 9, 5, 7, 1."), [T("Order: 1, 3, 5, 7, 9. The middle value is 5.", "نرتّب: 1 و3 و5 و7 و9. القيمة الوسطى 5.", "Ordonné : 1, 3, 5, 7, 9 ; médiane 5."), F("median = 5")]),
    EX("3", "", st("Mode and range of 4, 2, 4, 7, 4, 2.", "المنوال والمدى للأعداد 4 و2 و4 و7 و4 و2.", "Mode et étendue de 4, 2, 4, 7, 4, 2."), [F("mode = 4      range = 7 − 2 = 5")]),
    EX("4", "", st("Error detective: a mean of 12 for data between 3 and 9.", "المحقق: متوسط 12 لمعطيات بين 3 و9.", "Détective : moyenne 12 pour des données entre 3 et 9."), [T("Impossible: the mean lies between the smallest and the largest value.", "مستحيل: المتوسط يقع بين أصغر قيمة وأكبرها.", "Impossible : la moyenne est entre le min et le max.")]),
]
