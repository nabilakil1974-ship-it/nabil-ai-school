"""Grade 10 Mathematics — Statistical vocabulary and distribution (concept lesson; examples are NABIL's own, not textbook data)."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G10-MATH-EN-001"
GRADE = 10
SUBJECT = "math"
TITLES = {"en": "Statistical vocabulary and distribution", "ar": "مفردات الإحصاء والتوزيع الإحصائي", "fr": "Vocabulaire statistique et distribution"}

W = {"en": "Not quite: check the total of the frequencies.", "ar": "ليس تمامًا: راجع مجموع التكرارات.", "fr": "Pas tout à fait : vérifie le total des effectifs."}
QUIZ = [
    {"q": "3 + 7 + 6 + 3 + 1 = ?", "opts": ["20", "19", "21", "30"], "a": 0, "why": {"19": W, "21": W, "30": W}, "ok": "20 observations"},
    {"q": "Variable: number of siblings. Type?", "opts": ["Quantitative", "Qualitative", "Population", "Frequency"], "a": 0,
     "why": {"Qualitative": {"en": "Siblings are counted, so it is numerical.", "ar": "عدد الإخوة يُعدّ فهو كمّي.", "fr": "On compte : c'est numérique."},
             "Population": {"en": "Population is the group, not the variable.", "ar": "المجتمع هو المجموعة لا المتغيّر.", "fr": "La population est le groupe."},
             "Frequency": {"en": "Frequency is a count of a value.", "ar": "التكرار هو عدد مرات القيمة.", "fr": "L'effectif est un décompte."}}, "ok": "quantitative"},
]

THEORY = [
    ("Population, individual, variable", "المجتمع والفرد والمتغيّر", "Population, individu, caractère", "", [
        T("Hello! A statistical study begins by naming the population (the whole group studied), the individual (one member), and the variable, also called the character (what we observe on each individual). Example: we ask 20 students in a class how many siblings each has. Population: the 20 students. Individual: one student. Variable: number of siblings.",
          "مرحبًا! تبدأ الدراسة الإحصائية بتحديد المجتمع الإحصائي (المجموعة كلها)، والفرد (عضو واحد منها)، والمتغيّر أو الصفة (ما نلاحظه عند كل فرد). مثال: نسأل 20 تلميذًا في صف عن عدد إخوة كلٍّ منهم. المجتمع: التلاميذ العشرون. الفرد: تلميذ واحد. المتغيّر: عدد الإخوة.",
          "Une étude statistique commence par la population, l'individu et le caractère. Exemple : 20 élèves, nombre de frères et sœurs."),
    ]),
    ("Values and frequencies", "القيم والتكرارات", "Valeurs et effectifs", "", [
        T("The values the variable takes are its modalities. The frequency of a value is the number of individuals having it. Siblings: 0 → 3 students, 1 → 7, 2 → 6, 3 → 3, 4 → 1.",
          "القيم التي يأخذها المتغيّر هي نماذجه. وتكرار القيمة هو عدد الأفراد الذين لهم هذه القيمة. عدد الإخوة: 0 عند 3 تلاميذ و1 عند 7 و2 عند 6 و3 عند 3 و4 عند تلميذ واحد.",
          "Les valeurs prises sont les modalités ; l'effectif est le nombre d'individus."),
        F("value:  0   1   2   3   4"),
        F("frequency:  3   7   6   3   1"),
    ]),
    ("Check the total", "نتحقق من المجموع", "Vérifier le total", "", [
        T("The sum of all frequencies must equal the number of individuals.",
          "يجب أن يساوي مجموع التكرارات عدد الأفراد.",
          "La somme des effectifs égale le nombre d'individus."),
        F("3 + 7 + 6 + 3 + 1 = 20"),
    ]),
    ("Raw data and a distribution", "المعطيات الخام والتوزيع", "Données brutes et distribution", "", [
        T("Raw data is the list as collected: 2, 1, 0, 3, 1, 2, ... A distribution organizes it in a table of value and frequency, so it can be read at a glance. We then read only what the data support: for example, 7 students out of 20 have exactly 1 sibling. We cannot conclude anything about other classes.",
          "المعطيات الخام هي القائمة كما جُمعت: 2، 1، 0، 3، 1، 2 … والتوزيع ينظّمها في جدول قيمة/تكرار فيسهل قراءتها. ثم نقرأ ما تدعمه المعطيات فقط: مثلًا 7 تلاميذ من 20 لهم أخ واحد بالضبط. ولا نستنتج شيئًا عن صفوف أخرى.",
          "Données brutes puis tableau ; on conclut seulement ce que les données permettent."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Population → variable → values → frequencies → check the total → interpret carefully.",
          "المجتمع ثم المتغيّر ثم القيم ثم التكرارات ثم التحقق من المجموع ثم التفسير بحذر.",
          "Population, caractère, valeurs, effectifs, total, interprétation."),
        F("POPULATION → VARIABLE → VALUES → FREQUENCIES → TOTAL → INTERPRET"),
    ]),
]

EXERCISES = [
    EX("1", "", st("Survey: a school asks 120 pupils which sport they prefer. Give the population, individual and variable.", "في استبيان سألت مدرسة 120 تلميذًا عن رياضتهم المفضلة. حدّد المجتمع والفرد والمتغيّر.", "Enquête : 120 élèves, sport préféré. Population, individu, caractère ?"), [
        T("Population: the 120 pupils. Individual: one pupil. Variable: preferred sport (qualitative).", "المجتمع: التلاميذ الـ120. الفرد: تلميذ. المتغيّر: الرياضة المفضلة (وصفي).", "Population : 120 élèves ; caractère : sport (qualitatif)."),
    ]),
    EX("2", "", st("Values 1, 2, 2, 3, 1, 2, 3, 2: build the distribution.", "القيم 1، 2، 2، 3، 1، 2، 3، 2: كوّن التوزيع.", "Valeurs 1, 2, 2, 3, 1, 2, 3, 2 : distribution."), [
        F("1 → 2    2 → 4    3 → 2"), F("2 + 4 + 2 = 8"),
    ]),
    EX("3", "", st("A table shows frequencies 4, 9, 7 for a class of 21. Is it consistent?", "جدول فيه التكرارات 4 و9 و7 لصف عدده 21. هل هو متسق؟", "Effectifs 4, 9, 7 pour 21 élèves : cohérent ?"), [
        F("4 + 9 + 7 = 20"), T("No: 20 is not 21, one observation is missing.", "لا: 20 لا تساوي 21، ينقص ملاحظة واحدة.", "Non : il manque 1."),
    ]),
    EX("4", "", st("Which conclusion is supported: \"7 of the 20 students have 1 sibling\" or \"most students in the country have 1 sibling\"?", "أيّ الاستنتاجين تدعمه المعطيات: «7 من 20 تلميذًا لهم أخ واحد» أم «معظم تلاميذ البلد لهم أخ واحد»؟", "Quelle conclusion est justifiée ?"), [
        T("Only the first one. The data concern these 20 students.", "الأول فقط. المعطيات تخصّ هؤلاء العشرين.", "Seulement la première."),
    ]),
]
