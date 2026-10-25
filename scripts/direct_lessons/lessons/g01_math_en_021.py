"""Grade 1 Mathematics — Tens and ones (continuation)."""
from scripts.direct_lessons.common import T, F, EX, st, tens, objects

LESSON_ID = "G01-MATH-EN-021"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Tens and ones (continuation)", "ar": "العشرات والآحاد (تتمة)", "fr": "Dizaines et unités (suite)"}

THEORY = [
    ("Same quantity, different representation", "الكمية نفسها بتمثيل مختلف", "Même quantité, autre représentation", "58", [
        T("Hello! Do you remember the rule? Ten ones make one ten. Today we show the same quantity in more than one way: once as a bundle and once as separate ones. And we prove the quantity is the same.",
          "مرحبًا! هل تذكر القاعدة؟ عشرة آحاد تصنع عشرة واحدة. اليوم نعرض الكمية نفسها بأكثر من شكل: مرة حزمة ومرة آحادًا منفصلة، ونثبت أن الكمية نفسها.",
          "Bonjour ! Tu te souviens de la règle ? Dix unités font une dizaine. Aujourd'hui on montre la même quantité de plusieurs façons : en paquet, puis en unités séparées. Et on prouve que la quantité est la même."),
        tens(1, 3),
        T("Model A: one ten and three ones. Now we open the ten.",
          "النموذج A: عشرة واحدة وثلاثة آحاد. الآن نفتح العشرة.",
          "Modèle A : une dizaine et trois unités. Maintenant on ouvre la dizaine."),
        tens(1, 3, bundled=False),
        T("Did we add an object? No. Did we remove one? No. So the quantity is the same; only the representation changed.",
          "هل أضفنا شيئًا؟ لا. هل حذفنا شيئًا؟ لا. إذن الكمية نفسها، والتمثيل فقط تغيّر.",
          "A-t-on ajouté un objet ? Non. En a-t-on enlevé ? Non. La quantité est la même ; seule la représentation a changé."),
    ]),
    ("Read a tens-and-ones model", "نقرأ نموذج العشرات والآحاد", "Lire un modèle de dizaines et unités", "58", [
        tens(1, 6),
        T("Do not count every unit at once. Read the organization: how many tens? One. How many loose ones? Six. So: 1 ten and 6 ones. To verify, we open the ten and count.",
          "لا نعدّ كل الوحدات فورًا. نقرأ التنظيم: كم عشرة؟ واحدة. كم واحدًا منفردًا؟ ستة. إذن: عشرة واحدة وستة آحاد. وللتحقق نفتح العشرة ونعدّ.",
          "Ne compte pas toutes les unités tout de suite. Lis l'organisation : combien de dizaines ? Une. Combien d'unités seules ? Six. Donc : 1 dizaine et 6 unités. Pour vérifier, on ouvre la dizaine et on compte."),
    ]),
    ("Build from a spoken representation", "نبني من تمثيل منطوق", "Construire à partir d'une représentation dite", "59", [
        F("one ten and five ones"),
        T("I say: one ten and five ones. You build it. Is the bundle exactly ten? Are the loose ones exactly five? Make the ten first. Count only the loose ones. Do not put another loose one inside a bundle that is already full.",
          "أقول: عشرة واحدة وخمسة آحاد. وأنت تبنيها. هل الحزمة عشرة بالضبط؟ هل الآحاد المنفردة خمسة بالضبط؟ اصنع العشرة أولًا، وعدّ الآحاد المنفردة فقط، ولا تضع واحدًا منفردًا داخل حزمة اكتملت.",
          "Je dis : une dizaine et cinq unités. Tu construis. Le paquet fait-il exactement dix ? Y a-t-il exactement cinq unités seules ? Fais d'abord la dizaine. Compte seulement les unités seules. N'ajoute pas d'unité dans un paquet déjà plein."),
        tens(1, 5),
    ]),
    ("Exchange ten ones for one ten", "نبادل عشرة آحاد بعشرة واحدة", "Échanger dix unités contre une dizaine", "59", [
        tens(1, 0, bundled=False),
        T("Ten loose ones become one ten. And the other way round: one ten becomes ten ones. No object appears and no object disappears.",
          "عشرة آحاد منفردة تصبح عشرة واحدة. وبالعكس: عشرة واحدة تصبح عشرة آحاد. لا يظهر شيء ولا يختفي شيء.",
          "Dix unités seules deviennent une dizaine. Et inversement : une dizaine devient dix unités. Aucun objet n'apparaît, aucun ne disparaît."),
        tens(1, 0),
    ]),
    ("Complete a missing representation", "نكمل تمثيلًا ناقصًا", "Compléter une représentation manquante", "59", [
        tens(1, 3, label=False),
        F("1 ten and __ ones"),
        T("A part is missing. We do not guess. Count the loose objects we can see: three. So 1 ten and 3 ones. The answer is tied to the visual evidence.",
          "هناك جزء ناقص. لا نخمّن. نعدّ الأشياء المنفردة الظاهرة: ثلاثة. إذن عشرة واحدة وثلاثة آحاد. الجواب مرتبط بالدليل المرئي.",
          "Une partie manque. On ne devine pas. On compte les objets seuls visibles : trois. Donc 1 dizaine et 3 unités. La réponse est liée à la preuve visuelle."),
    ]),
    ("Why does the quantity stay the same?", "لماذا تبقى الكمية نفسها؟", "Pourquoi la quantité reste-t-elle la même ?", "59", [
        T("Why are one ten and ten loose ones the same quantity? Because the ten is made of exactly ten ones. When we bundle or unbundle, the organization changes, but the quantity does not.",
          "لماذا عشرة واحدة وعشرة آحاد منفردة هما الكمية نفسها؟ لأن العشرة مصنوعة من عشرة آحاد بالضبط. عندما نحزم أو نفكّ يتغير التنظيم لا الكمية.",
          "Pourquoi une dizaine et dix unités seules sont-elles la même quantité ? Parce que la dizaine est faite d'exactement dix unités. Quand on lie ou qu'on défait, l'organisation change, pas la quantité."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("One ten and ten ones are the same units, organized in a different way.",
          "عشرة واحدة وعشرة آحاد هما الوحدات نفسها منظّمة بطريقة مختلفة.",
          "Une dizaine et dix unités, ce sont les mêmes unités rangées autrement."),
        F("READ TENS → READ ONES → EXCHANGE EXACTLY 10 → REBUILD → UNBUNDLE TO VERIFY → EXPLAIN"),
    ]),
]

EXERCISES = [
    EX("1", "58", st("A: one ten and 2 ones. B: twelve loose ones from the same model. Same quantity?", "A: عشرة واحدة وواحدان. B: اثنا عشر واحدًا منفردًا من النموذج نفسه. هل الكمية نفسها؟", "A : une dizaine et 2 unités. B : douze unités seules du même modèle. Même quantité ?"), [
        tens(1, 2),
        tens(1, 2, bundled=False),
        T("Same. Prove it: unbundle and count twelve.",
          "نفسها. نثبت: نفكّ ونعدّ اثني عشر.",
          "Pareil. Preuve : on défait et on compte douze."),
    ]),
    EX("2", "58", st("Read the model: how many tens and ones?", "اقرأ النموذج: كم عشرة وكم واحدًا؟", "Lis le modèle : combien de dizaines et d'unités ?"), [
        tens(1, 4, label=False),
        F("one ten and four ones"),
    ]),
    EX("3", "59", st("Build one ten and seven ones.", "ابنِ عشرة واحدة وسبعة آحاد.", "Construis une dizaine et sept unités."), [
        tens(1, 7),
        T("Make the ten first. Count only the loose ones. Do not put a loose one inside a full bundle.",
          "اصنع العشرة أولًا. عدّ الآحاد المنفردة فقط. لا تضع واحدًا في حزمة مكتملة.",
          "Fais d'abord la dizaine. Compte seulement les unités seules. N'en mets pas dans un paquet plein."),
    ]),
    EX("4", "59", st("Take exactly ten of 13 loose counters and exchange.", "خذ عشرة بالضبط من 13 عدّادًا منفردًا وبادل.", "Prends exactement dix parmi 13 jetons seuls et échange."), [
        tens(1, 3, bundled=False, label=False),
        tens(1, 3),
        T("What is left? Three ones. Open the ten: we get back the same collection.",
          "ماذا بقي؟ ثلاثة آحاد. نفتح العشرة فنعود إلى المجموعة نفسها.",
          "Que reste-t-il ? Trois unités. On ouvre la dizaine : on retrouve la même collection."),
    ]),
    EX("5", "59", st("Fill in the missing numbers: 1 ten and __ ones; then __ ten and 5 ones.", "املأ الناقص: عشرة واحدة و__ آحاد؛ ثم __ عشرة وخمسة آحاد.", "Complète : 1 dizaine et __ unités ; puis __ dizaine et 5 unités."), [
        tens(1, 3, label=False),
        F("1 ten and 3 ones"),
        tens(1, 5, label=False),
        F("1 ten and 5 ones"),
    ]),
    EX("6", "59", st("Error detective: the child says there are only 1 + 4 objects.", "المحقق: قال الطفل إن هناك 1 + 4 أشياء فقط.", "Détective : l'enfant dit qu'il n'y a que 1 + 4 objets."), [
        tens(1, 4),
        T("The child counted the ten as one unit. But one ten is ten ones. So the total is fourteen.",
          "عدّ الطفل العشرة كوحدة واحدة. لكن العشرة الواحدة هي عشرة آحاد. إذن المجموع أربعة عشر.",
          "L'enfant a compté la dizaine comme une seule unité. Mais une dizaine, c'est dix unités. Le total est quatorze."),
        F("10 + 4 = 14"),
    ]),
    EX("7", "59", st("Challenge: show one ten and 2 ones with no bundle, and prove it is the same quantity.", "تحدٍّ: مثّل عشرة وواحدين دون حزمة وأثبت أن الكمية نفسها.", "Défi : montre une dizaine et 2 unités sans paquet et prouve que c'est la même quantité."), [
        tens(1, 2),
        tens(1, 2, bundled=False),
        T("Open the ten. Count all the objects: twelve both times.",
          "نفتح العشرة. نعدّ كل الأشياء: اثنا عشر في الحالتين.",
          "On ouvre la dizaine. On compte tout : douze dans les deux cas."),
    ]),
    EX("8", "59", st("Final check: read one ten and 3 ones, build one ten and 6 ones, and explain why the quantity stays the same.", "تقييم أخير: اقرأ عشرة وثلاثة آحاد، وابنِ عشرة وستة آحاد، واشرح لماذا تبقى الكمية نفسها.", "Évaluation : lis une dizaine et 3 unités, construis une dizaine et 6 unités, explique pourquoi la quantité reste la même."), [
        tens(1, 3),
        tens(1, 6),
        T("Because the ten is made of exactly ten ones. Bundling and unbundling change the organization, not the quantity.",
          "لأن العشرة مصنوعة من عشرة آحاد بالضبط. الحزم والفكّ يغيّران التنظيم لا الكمية.",
          "Parce que la dizaine est faite d'exactement dix unités. Lier et défaire changent l'organisation, pas la quantité."),
    ]),
]
