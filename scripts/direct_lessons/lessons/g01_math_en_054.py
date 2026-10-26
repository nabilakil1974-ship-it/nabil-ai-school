"""Grade 1 Mathematics — Add or subtract."""
from scripts.direct_lessons.common import T, F, EX, st, jumps
from scripts.direct_lessons.lessons.g01_math_en_048 import takeaway

LESSON_ID = "G01-MATH-EN-054"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Add or subtract", "ar": "نجمع أم نطرح", "fr": "Additionner ou soustraire"}

THEORY = [
    ("Look at the action first", "ننظر إلى الفعل أولًا", "On regarde d'abord l'action", "138", [
        T("Hello, champion! Before we write + or −, we ask: what is happening? If things are joined together or increased, we may add. If things are taken away, or we look for what remains, we may subtract. We never choose from one word alone; we look at the whole situation.",
          "مرحبًا يا بطل! قبل أن نكتب + أو − نسأل: ماذا يحدث؟ إذا ضُمّت الأشياء معًا أو زادت فقد نجمع. وإذا أُخذت أشياء أو بحثنا عمّا يبقى فقد نطرح. لا نختار من كلمة واحدة، بل ننظر إلى الموقف كله.",
          "Avant d'écrire + ou −, on se demande : que se passe-t-il ? Si on réunit ou si ça augmente, on peut additionner. Si on retire, ou si on cherche ce qui reste, on peut soustraire. On ne choisit pas d'après un seul mot : on regarde toute la situation."),
        F("JOIN / INCREASE → +        TAKE AWAY / WHAT REMAINS → −"),
    ]),
    ("A joining story", "قصة ضمّ", "Une histoire de réunion", "138", [
        jumps(4, 3, hi=10),
        T("There are 4 ducks on the pond, and 3 more come. The ducks are joined, so we add: 4 + 3 = 7 ducks.",
          "على البركة 4 بطات وتأتي 3 أخرى. البطات تنضمّ إلى بعضها فنجمع: 4 + 3 = 7 بطات.",
          "Il y a 4 canards sur l'étang et 3 autres arrivent. On réunit : 4 + 3 = 7 canards."),
    ]),
    ("A taking-away story", "قصة أخذ", "Une histoire de retrait", "139", [
        takeaway(7, 3),
        T("There are 7 ducks, and 3 swim away. Some are removed, so we subtract: 7 − 3 = 4 ducks remain.",
          "هناك 7 بطات وتسبح 3 منها بعيدًا. أُخذ بعضها فنطرح: 7 − 3 = 4 بطات تبقى.",
          "Il y a 7 canards et 3 s'éloignent. On en retire : 7 − 3 = 4 canards restent."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Understand the situation first. Choose + when quantities are joined or increased, and − when a part is taken away. Write the number sentence and check it against the story.",
          "نفهم الموقف أولًا. نختار + عندما تُضمّ الكميات أو تزيد، و− عندما يُؤخذ جزء. نكتب الجملة العددية ونتحقق منها مع القصة.",
          "On comprend d'abord la situation. + quand on réunit ou augmente, − quand on retire une partie. On écrit l'égalité et on vérifie avec l'histoire."),
        F("UNDERSTAND → CHOOSE + OR − → CALCULATE → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "138", st("5 apples and 2 more apples. + or −?", "5 تفاحات وتفاحتان أخريان. + أم −؟", "5 pommes et 2 pommes de plus. + ou − ?"), [
        jumps(5, 2, hi=10),
        F("5 + 2 = 7"),
    ]),
    EX("2", "138", st("8 cookies and 3 are eaten. + or −?", "8 بسكويت أُكل منها 3. + أم −؟", "8 biscuits, 3 sont mangés. + ou − ?"), [
        takeaway(8, 3),
        F("8 − 3 = 5"),
    ]),
    EX("3", "138", st("6 children and 4 more join them.", "6 أطفال ينضم إليهم 4.", "6 enfants et 4 autres les rejoignent."), [
        jumps(6, 4, hi=10),
        F("6 + 4 = 10"),
    ]),
    EX("4", "139", st("9 balloons and 5 fly away.", "9 بالونات طار منها 5.", "9 ballons, 5 s'envolent."), [
        takeaway(9, 5),
        F("9 − 5 = 4"),
    ]),
    EX("5", "139", st("There are 10 stickers and 6 are given away. How many are left?", "هناك 10 ملصقات أُعطي منها 6. كم تبقى؟", "10 autocollants, 6 sont donnés. Combien en reste-t-il ?"), [
        takeaway(10, 6),
        F("10 − 6 = 4"),
    ]),
    EX("6", "139", st("Error check: 'There are 6 birds; 2 fly away.' A child writes 6 + 2. Is the sign right?", "تحقّق من الخطأ: «6 عصافير طار منها 2». كتب طفل 6 + 2. هل الإشارة صحيحة؟", "Vérifie l'erreur : « 6 oiseaux, 2 s'envolent ». L'enfant écrit 6 + 2. Le signe est-il juste ?"), [
        takeaway(6, 2),
        T("No. Birds flew away, so some were taken away. The right sentence is 6 − 2 = 4.", "لا. العصافير طارت أي أُخذ بعضها. الجملة الصحيحة 6 − 2 = 4.", "Non. Des oiseaux sont partis : on retire. L'égalité juste est 6 − 2 = 4."),
    ]),
    EX("7", "139", st("Challenge: 12 cars; 5 more arrive, then 3 leave. How many?", "تحدٍّ: 12 سيارة، تصل 5 أخرى ثم تغادر 3. كم سيارة؟", "Défi : 12 voitures ; 5 arrivent puis 3 partent. Combien ?"), [
        F("12 + 5 = 17      17 − 3 = 14"),
        T("First joining (+5), then taking away (−3).", "أولًا ضمّ (+5) ثم أخذ (−3).", "D'abord réunir (+5), puis retirer (−3)."),
    ]),
    EX("8", "139", st("Final check: 13 crayons, 4 are lost. Choose the operation and justify.", "تقييم أخير: 13 قلم تلوين ضاع منها 4. اختر العملية وبرّر.", "Évaluation : 13 crayons, 4 sont perdus. Choisis l'opération et justifie."), [
        takeaway(13, 4),
        T("Lost means taken away, so we subtract: 13 − 4 = 9.", "الضياع يعني الأخذ، لذلك نطرح: 13 − 4 = 9.", "Perdu veut dire retiré : 13 − 4 = 9."),
    ]),
]
