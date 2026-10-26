"""Grade 3 Mathematics — Writing a Problem (from the teacher plan)."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G03-MATH-EN-059"
GRADE = 3
SUBJECT = "math"
TITLES = {"en": "Writing a Problem", "ar": "كتابة مسألة", "fr": "Écrire un problème"}

THEORY = [
    ("What a good problem needs", "ما تحتاجه المسألة الجيدة", "Ce qu'il faut à un bon problème", "124", [
        T("Hello, champion! A good problem has coherent data, a clear relationship and a question that can be answered from the given information alone. Data: 24 pencils and 6 children. Question: how many pencils does each child get? 24 ÷ 6 = 4.",
          "مرحبًا يا بطل! المسألة الجيدة فيها معطيات متناسقة وعلاقة واضحة وسؤال يمكن الإجابة عنه من المعطيات وحدها. المعطيات: 24 قلمًا و6 أطفال. السؤال: كم قلمًا لكل طفل؟ 24 ÷ 6 = 4.",
          "Un bon problème : données cohérentes, relation claire, question à laquelle on peut répondre. 24 crayons, 6 enfants : 24 ÷ 6 = 4."),
        F("24 ÷ 6 = 4"),
    ]),
    ("Steps to write one", "خطوات كتابة مسألة", "Étapes", "124", [
        T("1) Look at the data you have. 2) Choose the unknown. 3) Write a context and a clear question. 4) Check that nothing needed is missing and nothing extra is invented. 5) Solve it to check it works.",
          "1) ننظر إلى المعطيات. 2) نختار المجهول. 3) نكتب سياقًا وسؤالًا واضحًا. 4) نتأكد أنه لا ينقص شيء ولا نخترع معطيات زائدة. 5) نحلّها لنتأكد من صحتها.",
          "Données, inconnue, contexte + question, vérifier, résoudre."),
    ]),
    ("Missing information", "معلومة ناقصة", "Information manquante", "125", [
        T("\"Sara has 12 stickers. How many does she have left?\" has no answer: we do not know how many she gave away. Add the missing relationship: she gave 5 away. 12 − 5 = 7.",
          "«عند سارة 12 ملصقًا. كم بقي معها؟» لا جواب لها لأننا لا نعرف كم أعطت. نضيف العلاقة الناقصة: أعطت 5. 12 − 5 = 7.",
          "Il manque une donnée : elle en donne 5. 12 − 5 = 7."),
        F("12 − 5 = 7"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Use the data, choose the unknown, write it clearly, check it, solve it, revise.", "نستعمل المعطيات ونختار المجهول ونكتب بوضوح ونتحقق ونحلّ ونعدّل.", "Données, inconnue, rédiger, vérifier, résoudre."),
        F("DATA → UNKNOWN → WRITE → SOLVE → REVISE"),
    ]),
]

EXERCISES = [
    EX("1", "124", st("Write a problem for 15 and 3 using division, then solve it.", "اكتب مسألة بالعددين 15 و3 تستعمل القسمة ثم حلّها.", "Écris un problème avec 15 et 3 (division) et résous-le."), [
        T("For example: 15 apples are shared among 3 children. How many each? 15 ÷ 3 = 5.", "مثلًا: وُزّعت 15 تفاحة على 3 أطفال. كم لكل طفل؟ 15 ÷ 3 = 5.", "15 pommes pour 3 enfants : 5."),
    ]),
    EX("2", "125", st("What is missing: \"Omar had 20 marbles and lost some. How many are left?\"", "ما الناقص: «كان عند عمر 20 كرة وضاع بعضها. كم بقي؟»", "Que manque-t-il ?"), [T("How many he lost.", "عدد ما ضاع.", "Combien il en a perdu.")]),
    EX("3", "125", st("Error detective: a problem gives 8 and 4 and asks for the colour of the ball.", "المحقق: مسألة معطياتها 8 و4 وتسأل عن لون الكرة.", "Détective : question sans rapport avec les données."), [T("The question cannot be answered from the data.", "لا يمكن الإجابة عن السؤال من المعطيات.", "Impossible de répondre.")]),
]
