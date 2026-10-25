"""Grade 1 Mathematics — The numbers from 1 to 5."""
from scripts.direct_lessons.common import T, F, D, EX, st, S, objects, row, numeral, scene

LESSON_ID = "G01-MATH-EN-003"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "The numbers from 1 to 5", "ar": "الأعداد من 1 إلى 5", "fr": "Les nombres de 1 à 5"}

THEORY = [
    ("Making 4: three and one more", "نصنع العدد 4: ثلاثة وواحد آخر", "Faire 4 : trois et encore un", "18", [
        T("Hello again! We already know 1, 2 and 3. Today we meet two new friends: 4 and 5. We first understand what they mean.",
          "مرحبًا من جديد! نعرف 1 و2 و3. اليوم نتعرّف على صديقين جديدين: 4 و5. نفهم أولًا ماذا يعنيان.",
          "Bonjour encore ! On connaît 1, 2 et 3. Aujourd'hui, deux nouveaux amis : 4 et 5. D'abord, on comprend ce qu'ils veulent dire."),
        objects(3, "square", "#1e63d6", None, prefix="a"),
        T("Count the blocks: one, two, three. There are three.",
          "عُدّ المكعبات: واحد، اثنان، ثلاثة. يوجد ثلاثة.",
          "Compte les cubes : un, deux, trois. Il y en a trois."),
        objects(4, "square", "#1e63d6", 4, prefix="b"),
        T("We add one more block. Count all of them again: one, two, three, four. The last number is four.",
          "أضفنا مكعبًا واحدًا. نعدّ الكل من جديد: واحد، اثنان، ثلاثة، أربعة. آخر عدد هو four.",
          "On ajoute un cube. On recompte tout : un, deux, trois, quatre. Le dernier nombre est four."),
        F("3 blocks + 1 block = four = 4"),
        T("The number 4 means a collection of four things.",
          "العدد 4 يعني مجموعة فيها أربعة أشياء.",
          "Le nombre 4 veut dire une collection de quatre choses."),
    ]),
    ("Making 5: four and one more", "نصنع العدد 5: أربعة وواحد آخر", "Faire 5 : quatre et encore un", "19", [
        objects(4, "circle", "#d81b60", None, prefix="c"),
        T("Four strawberries: one, two, three, four.",
          "أربع فراولات: واحد، اثنان، ثلاثة، أربعة.",
          "Quatre fraises : un, deux, trois, quatre."),
        objects(5, "circle", "#d81b60", 5, prefix="d"),
        T("We add one new strawberry and count again: one, two, three, four, five. The new number is 5.",
          "أضفنا فراولة جديدة ونعدّ من جديد: واحد، اثنان، ثلاثة، أربعة، خمسة. العدد الجديد هو 5.",
          "On ajoute une fraise et on recompte : un, deux, trois, quatre, cinq. Le nouveau nombre est 5."),
        F("4 + 1 more = five = 5"),
    ]),
    ("The last counting word tells how many", "آخر كلمة عدّ تخبرنا بالمجموع", "Le dernier mot du comptage donne le total", "19", [
        objects(4, "tri", "#fb8c00", None, prefix="e", r=38),
        T("We count the fish: one, two, three, four. The last word is four. So the total number of fish is four.",
          "نعدّ الأسماك: واحد، اثنان، ثلاثة، أربعة. آخر كلمة four. إذن مجموع الأسماك أربعة.",
          "On compte les poissons : un, deux, trois, quatre. Le dernier mot est four. Il y a donc quatre poissons en tout."),
        T("The last counting word is not only the last sound. It tells the whole quantity.",
          "آخر كلمة عدّ ليست مجرد آخر صوت، إنها تخبرنا بالكمية كلها.",
          "Le dernier mot n'est pas juste le dernier son : il donne toute la quantité."),
        objects(5, "tri", "#fb8c00", None, prefix="f", r=38),
        T("We add a fifth fish and count again: one, two, three, four, five. The total is now five.",
          "أضفنا سمكة خامسة ونعدّ من جديد: واحد… خمسة. المجموع الآن five.",
          "On ajoute un cinquième poisson et on recompte : un… cinq. Le total est maintenant five."),
    ]),
    ("Same quantity, different arrangement", "الكمية نفسها بترتيب مختلف", "Même quantité, autre disposition", "20", [
        scene(*row(5, "circle", "#8e24aa", 220, "g", r=26)),
        T("Five dots in a row: one, two, three, four, five.",
          "خمس نقاط في صف: واحد، اثنان، ثلاثة، أربعة، خمسة.",
          "Cinq points alignés : un, deux, trois, quatre, cinq."),
        scene('<circle id="h1" cx="330" cy="90" r="26" fill="#8e24aa" stroke="#0b3d5c" stroke-width="3"/>'
              '<circle id="h2" cx="200" cy="200" r="26" fill="#8e24aa" stroke="#0b3d5c" stroke-width="3"/>'
              '<circle id="h3" cx="460" cy="200" r="26" fill="#8e24aa" stroke="#0b3d5c" stroke-width="3"/>'
              '<circle id="h4" cx="250" cy="330" r="26" fill="#8e24aa" stroke="#0b3d5c" stroke-width="3"/>'
              '<circle id="h5" cx="410" cy="330" r="26" fill="#8e24aa" stroke="#0b3d5c" stroke-width="3"/>', ["h1", "h2", "h3", "h4", "h5"]),
        T("The dots moved into a new shape. Are there 4, 5 or 6? Still five, because we added none and removed none.",
          "تحرّكت النقاط إلى شكل جديد. هل هي 4 أم 5 أم 6؟ ما زالت خمسًا، لأننا لم نضف ولم نحذف شيئًا.",
          "Les points ont pris une nouvelle forme. 4, 5 ou 6 ? Toujours cinq, car on n'a rien ajouté ni enlevé."),
        T("Spreading objects out does not make more of them. When in doubt, we count.",
          "تباعد الأشياء لا يجعلها أكثر. وعند الشك نعدّ.",
          "Écarter les objets n'en fait pas plus. Dans le doute, on compte."),
    ]),
    ("Matching 1, 2, 3, 4, 5", "نصل الكميات بالأعداد 1 إلى 5", "Associer les nombres 1 à 5", "20", [
        F("⭐ → 1      ⭐⭐ → 2      ⭐⭐⭐ → 3      ⭐⭐⭐⭐ → 4      ⭐⭐⭐⭐⭐ → 5"),
        T("We match group by group, never all at once. We count each group and choose the numeral that has the same quantity.",
          "نصل مجموعة مجموعة، وليس دفعة واحدة. نعدّ كل مجموعة ونختار الرقم الذي يعبّر عن كميتها.",
          "On associe groupe par groupe, jamais tout d'un coup. On compte chaque groupe et on choisit le chiffre de même quantité."),
        F("1 → one      2 → two      3 → three      4 → four      5 → five"),
    ]),
    ("Reading and writing 4 and 5", "قراءة العددين 4 و5 وكتابتهما", "Lire et écrire 4 et 5", "21", [
        scene(numeral(4, 170, 250, 150, "r4") + numeral(5, 490, 250, 150, "r5"), ["r4", "r5"]),
        T("This is the numeral 4: four. This is the numeral 5: five. The shape alone is not enough.",
          "هذا هو الرقم 4: four. وهذا هو الرقم 5: five. الشكل وحده لا يكفي.",
          "Voici le chiffre 4 : four. Voici le chiffre 5 : five. La forme seule ne suffit pas."),
        T("The numeral 4 reminds us of four things, and the numeral 5 reminds us of five things. Now we trace them with the finger.",
          "الرقم 4 يذكّرنا بأربعة أشياء، والرقم 5 يذكّرنا بخمسة أشياء. والآن نتتبّعهما بالإصبع.",
          "Le chiffre 4 rappelle quatre choses, le chiffre 5 cinq choses. Maintenant, on les suit avec le doigt."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        F("1 — 2 — 3 — 4 — 5"),
        T("Every numeral has a quantity. When we count, we touch each object once, and the last number tells the total.",
          "لكل رقم كمية. وعندما نعدّ نلمس كل شيء مرة واحدة، وآخر عدد يخبرنا بالمجموع.",
          "Chaque chiffre a une quantité. En comptant, on touche chaque objet une fois, et le dernier nombre donne le total."),
        F("TOUCH → COUNT → LAST NUMBER → MATCH → CHECK"),
        T("If the objects move but we add nothing and take nothing away, the number does not change.",
          "إذا تحرّكت الأشياء ولم نضف ولم نحذف فالعدد لا يتغيّر.",
          "Si les objets bougent sans qu'on ajoute ou enlève rien, le nombre ne change pas."),
    ]),
]

EXERCISES = [
    EX("1", "18", st("Make 4: put exactly 4 stars in the box.", "كوّن 4: ضع 4 نجوم بالضبط في الصندوق.", "Fais 4 : mets exactement 4 étoiles dans la boîte."), [
        objects(4, "star", "#fbc02d", 4, prefix="p"),
        T("Count as you put them in: one, two, three, four. If we have 3, we add one. If we have more than 4, we take the extra away.",
          "نعدّ ونحن نضع: واحد، اثنان، ثلاثة، أربعة. إذا كان عندنا 3 نضيف واحدة، وإذا زادت عن 4 نُخرج الزائد.",
          "On compte en posant : un, deux, trois, quatre. S'il y en a 3, on en ajoute une. S'il y en a plus de 4, on enlève le surplus."),
    ]),
    EX("2", "19", st("Count five circles and choose the right numeral: 3, 4 or 5.", "عُدّ خمس دوائر واختر الرقم الصحيح: 3 أو 4 أو 5.", "Compte cinq cercles et choisis le bon chiffre : 3, 4 ou 5."), [
        objects(5, "circle", "#1e63d6", None, prefix="q"),
        T("Touch each circle once: one, two, three, four, five.",
          "المس كل دائرة مرة واحدة: واحد، اثنان، ثلاثة، أربعة، خمسة.",
          "Touche chaque cercle une fois : un, deux, trois, quatre, cinq."),
        T("The last number is five, so the right numeral is 5.",
          "آخر عدد هو five، إذن الرقم الصحيح هو 5.",
          "Le dernier nombre est five, donc le bon chiffre est 5."),
        F("🔵🔵🔵🔵🔵 = 5"),
    ]),
    EX("3", "19", st("Count the yellow circles and tell how many there are.", "عُدّ الدوائر الصفراء وقل كم عددها.", "Compte les cercles jaunes et dis combien il y en a."), [
        objects(4, "circle", "#fdd835", None, prefix="y"),
        T("One, two, three, four. The last word is four, so there are four yellow circles.",
          "واحد، اثنان، ثلاثة، أربعة. آخر كلمة four، إذن توجد أربع دوائر صفراء.",
          "Un, deux, trois, quatre. Le dernier mot est four : il y a quatre cercles jaunes."),
        F("🟡🟡🟡🟡 = 4"),
    ]),
    EX("4", "20", st("Same or different? Four stars close together and four stars far apart.", "متساويتان أم مختلفتان؟ أربع نجوم متقاربة وأربع نجوم متباعدة.", "Pareil ou différent ? Quatre étoiles proches et quatre étoiles éloignées."), [
        T("The spread-out group looks bigger, but we count: group A one, two, three, four. Group B one, two, three, four.",
          "تبدو المجموعة المتباعدة أكبر، لكننا نعدّ: المجموعة A واحد، اثنان، ثلاثة، أربعة. والمجموعة B كذلك.",
          "Le groupe écarté semble plus grand, mais on compte : groupe A un, deux, trois, quatre. Groupe B pareil."),
        F("4 = 4"),
        T("Both groups have four. The distance does not change the quantity.",
          "في المجموعتين أربعة. المسافة لا تغيّر الكمية.",
          "Les deux groupes en ont quatre. La distance ne change pas la quantité."),
    ]),
    EX("5", "20", st("Show the numeral 4, then the numeral 5, with blocks.", "أظهر الرقم 4 ثم الرقم 5 بالمكعبات.", "Montre le chiffre 4, puis le chiffre 5, avec des cubes."), [
        objects(4, "square", "#43a047", 4, prefix="u"),
        T("For 4 we build four blocks and check by counting: one, two, three, four.",
          "للرقم 4 نبني أربعة مكعبات ونتحقق بالعدّ: واحد، اثنان، ثلاثة، أربعة.",
          "Pour 4, on construit quatre cubes et on vérifie en comptant : un, deux, trois, quatre."),
        objects(5, "square", "#43a047", 5, prefix="v"),
        T("For 5 we build five blocks and check: one, two, three, four, five. We count first, then decide whether to add or remove.",
          "للرقم 5 نبني خمسة مكعبات ونتحقق: واحد… خمسة. نعدّ أولًا ثم نقرّر هل نزيد أم ننقص.",
          "Pour 5, on construit cinq cubes et on vérifie : un… cinq. On compte d'abord, puis on décide d'ajouter ou d'enlever."),
    ]),
    EX("6", "21", st("Error detective: four teddy bears and the numeral 5.", "المحقق: أربعة دببة والرقم المكتوب 5.", "Détective : quatre oursons et le chiffre 5."), [
        objects(4, "tri", "#8d6e63", 5, prefix="w"),
        T("Count the bears: one, two, three, four. There are four. The written numeral is 5. They do not match.",
          "عُدّ الدببة: واحد، اثنان، ثلاثة، أربعة. يوجد أربعة، والمكتوب 5. لا يتطابقان.",
          "Compte les oursons : un, deux, trois, quatre. Il y en a quatre. Le chiffre écrit est 5 : ça ne correspond pas."),
        T("The correction: write 4 instead of 5.",
          "التصحيح: نكتب 4 بدل 5.",
          "Correction : on écrit 4 au lieu de 5."),
        F("🧸🧸🧸🧸 → 4"),
    ]),
    EX("7", "21", st("Order the boxes from the fewest to the most: A has 2, B has 5, C has 4, D has 1, E has 3.", "رتّب الصناديق من الأقل إلى الأكثر: A فيه 2، B فيه 5، C فيه 4، D فيه 1، E فيه 3.", "Range les boîtes du moins au plus : A en a 2, B en a 5, C en a 4, D en a 1, E en a 3."), [
        F("A = 2      B = 5      C = 4      D = 1      E = 3"),
        T("The smallest is 1, then 2, then 3, then 4, then 5.",
          "الأصغر هو 1 ثم 2 ثم 3 ثم 4 ثم 5.",
          "Le plus petit est 1, puis 2, puis 3, puis 4, puis 5."),
        F("D → A → E → C → B"),
        F("1 → 2 → 3 → 4 → 5"),
    ]),
    EX("8", "21", st("Final check: count 5 objects, choose the numeral for 4 circles, read 5, 2, 4, 1, 3.", "تحقّق نهائي: عُدّ 5 أشياء، اختر رقم 4 دوائر، اقرأ 5 و2 و4 و1 و3.", "Vérification finale : compte 5 objets, choisis le chiffre de 4 cercles, lis 5, 2, 4, 1, 3."), [
        F("5 objects → 5      4 circles → 4"),
        F("five, two, four, one, three"),
        T("Four dots in a row and four dots in a square are the same number: 4.",
          "أربع نقاط في صف وأربع نقاط في مربع هما العدد نفسه: 4.",
          "Quatre points en ligne et quatre points en carré font le même nombre : 4."),
    ]),
]
