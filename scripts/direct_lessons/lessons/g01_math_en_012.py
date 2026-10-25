"""Grade 1 Mathematics — As many as."""
from scripts.direct_lessons.common import T, F, EX, st, pairs, spread, objects

LESSON_ID = "G01-MATH-EN-012"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "As many as", "ar": "بقدر", "fr": "Autant que"}

THEORY = [
    ("One object with one partner", "كل شيء مع شريك واحد", "Un objet avec un partenaire", "38", [
        T("Hello! Today I have two groups that do not look the same. One is close together and the other is spread out. Does one of them have more objects?",
          "مرحبًا! اليوم عندي مجموعتان لا تبدوان متشابهتين: واحدة متقاربة والأخرى متباعدة. هل في إحداهما أشياء أكثر؟",
          "Bonjour ! Aujourd'hui j'ai deux groupes qui ne se ressemblent pas : l'un est serré, l'autre est espacé. L'un a-t-il plus d'objets ?"),
        pairs(4, 4, lines=False),
        T("We will not decide from the look of the row. Today we learn how to prove that two groups have as many as each other.",
          "لن نحكم من شكل الصف. اليوم نتعلّم كيف نثبت أن مجموعتين فيهما العدد نفسه، أي بقدر بعضهما.",
          "On ne décide pas d'après l'aspect de la rangée. Aujourd'hui on apprend à prouver que deux groupes ont autant d'objets l'un que l'autre."),
        pairs(4, 4),
        T("We connect each star with one circle. Is any star left without a partner? No. Is any circle left without a partner? No.",
          "نصل كل نجمة بدائرة واحدة. هل بقيت نجمة بلا شريك؟ لا. هل بقيت دائرة بلا شريك؟ لا.",
          "On relie chaque étoile à un cercle. Reste-t-il une étoile sans partenaire ? Non. Reste-t-il un cercle sans partenaire ? Non."),
        T("So the two groups have the same number. We say: A has as many objects as B, because each object took one partner and nothing was left.",
          "إذن للمجموعتين العدد نفسه. نقول: في A أشياء بقدر ما في B، لأن كل شيء أخذ شريكًا واحدًا ولم يبقَ شيء.",
          "Les deux groupes ont donc le même nombre. On dit : A a autant d'objets que B, car chaque objet a pris un partenaire et il ne reste rien."),
    ]),
    ("Spacing does not prove the quantity", "المسافة لا تثبت الكمية", "L'espacement ne prouve pas la quantité", "38", [
        spread(5, 62, "circle", "#e53935", 200, "C"),
        T("Here are five dots close together and five dots very spread out. The spread-out row looks longer. But does it have more objects?",
          "هنا خمس نقاط متقاربة وخمس نقاط متباعدة جدًا. الصف المتباعد يبدو أطول. لكن هل فيه أشياء أكثر؟",
          "Voici cinq points serrés et cinq points très espacés. La rangée espacée paraît plus longue. Mais a-t-elle plus d'objets ?"),
        pairs(5, 5, "circle", "circle", "#e53935", "#1e63d6", gap=120, r=22),
        T("We do not guess. We pair them. Nothing is left, so the quantity is the same. Distance changes the look of a group, not its number.",
          "لا نخمّن، بل نُقرن. لم يبقَ شيء، إذن الكمية نفسها. المسافة تغيّر شكل المجموعة لا عددها.",
          "On ne devine pas : on apparie. Il ne reste rien, donc la quantité est la même. La distance change l'aspect d'un groupe, pas son nombre."),
    ]),
    ("Build a collection with as many objects", "نبني مجموعة بقدر مجموعة أخرى", "Construire une collection avec autant d'objets", "39", [
        objects(5, "tri", "#e53935"),
        T("Here is a reference collection of five strawberries. We want a new collection with as many objects. First we use pairing, not numbers.",
          "هذه مجموعة مرجعية فيها خمس فراولات. نريد مجموعة جديدة فيها أشياء بقدرها. نستعمل الإقران أولًا لا الأعداد.",
          "Voici une collection de référence de cinq fraises. On veut une nouvelle collection avec autant d'objets. On utilise d'abord l'appariement, pas les nombres."),
        pairs(5, 5, "tri", "circle", "#e53935", "#43a047"),
        T("For each strawberry we place one object. Does every strawberry have a partner? Yes. Is any partner extra? No. We built an equal collection.",
          "لكل فراولة نضع شيئًا واحدًا. هل لكل فراولة شريك؟ نعم. هل زاد شريك؟ لا. بنينا مجموعة مساوية.",
          "Pour chaque fraise on place un objet. Chaque fraise a-t-elle un partenaire ? Oui. Un partenaire est-il en trop ? Non. On a construit une collection égale."),
    ]),
    ("Pairing first, counting as a check", "الإقران أولًا والعدّ للتحقق", "Apparier d'abord, compter pour vérifier", "39", [
        pairs(6, 6, "square", "square", "#fb8c00", "#8e24aa", gap=80, r=22),
        T("There are two ways to help us. The stronger way is pairing. After that we can count to check.",
          "هناك طريقتان تساعدنا. الأقوى هي الإقران، وبعدها نعدّ للتحقق.",
          "Deux façons nous aident. La plus forte est l'appariement. Ensuite on peut compter pour vérifier."),
        T("Count the top group: one, two, three, four, five, six. Count the bottom group: six too. The two ways agree.",
          "نعدّ المجموعة العليا: واحد، اثنان، ثلاثة، أربعة، خمسة، ستة. ونعدّ السفلى: ستة أيضًا. الطريقتان متفقتان.",
          "On compte le groupe du haut : un, deux, trois, quatre, cinq, six. Celui du bas : six aussi. Les deux façons s'accordent."),
        F("6 and 6 → as many as"),
    ]),
    ("Same number, different objects", "العدد نفسه وأشياء مختلفة", "Même nombre, objets différents", "39", [
        pairs(3, 3, "circle", "square", "#e53935", "#1e63d6"),
        T("Do the objects have to be the same kind? No. Here are three apples and three cars. The kinds differ, but the quantity is the same: there are as many apples as cars.",
          "هل يجب أن تكون الأشياء من النوع نفسه؟ لا. هنا ثلاث تفاحات وثلاث سيارات. النوع مختلف لكن الكمية نفسها: التفاحات بقدر السيارات.",
          "Les objets doivent-ils être du même type ? Non. Ici trois pommes et trois voitures. Les types diffèrent mais la quantité est la même : autant de pommes que de voitures."),
    ]),
    ("Explain the proof", "نشرح الدليل", "Expliquer la preuve", "39", [
        T("A good answer has two parts: the answer and the reason. Are there as many blocks as balls? Yes, because I made pairs and nothing was left, or because I counted five and five.",
          "الجواب الجيد له جزءان: الجواب والسبب. هل المكعبات بقدر الكرات؟ نعم، لأني كوّنت أزواجًا ولم يبقَ شيء، أو لأني عددت خمسة وخمسة.",
          "Une bonne réponse a deux parties : la réponse et la raison. Y a-t-il autant de cubes que de balles ? Oui, car j'ai fait des paires et il ne reste rien, ou car j'ai compté cinq et cinq."),
        F("answer + reason"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("As many as means two groups have the same number. We prove it by giving each object one partner. If nothing is left on either side, they are as many.",
          "بقدر تعني أن للمجموعتين العدد نفسه. نثبت ذلك بإعطاء كل شيء شريكًا واحدًا. إذا لم يبقَ شيء في أي جهة فهما بقدر بعضهما.",
          "Autant que veut dire que deux groupes ont le même nombre. On le prouve en donnant un partenaire à chaque objet. S'il ne reste rien, ils sont égaux."),
        F("LOOK → PAIR ONE-TO-ONE → CHECK WHAT REMAINS → COUNT → EXPLAIN"),
    ]),
]

EXERCISES = [
    EX("1", "38", st("Pair each apple with a teddy bear. Are there as many apples as teddy bears?", "اقرن كل تفاحة بدبّ. هل التفاحات بقدر الدببة؟", "Apparie chaque pomme avec un ourson. Y a-t-il autant de pommes que d'oursons ?"), [
        pairs(3, 3, "circle", "tri", "#e53935", "#8d6e63"),
        T("Every apple has one teddy bear. Nothing is left on either side.",
          "لكل تفاحة دبّ واحد. لم يبقَ شيء في أي جهة.",
          "Chaque pomme a un ourson. Il ne reste rien d'aucun côté."),
        F("Yes: as many as."),
    ]),
    EX("2", "38", st("Four stars close together and four stars far apart. Does the spread-out group have more?", "أربع نجوم متقاربة وأربع نجوم متباعدة. هل المتباعدة أكثر؟", "Quatre étoiles serrées et quatre étoiles espacées. Les espacées sont-elles plus nombreuses ?"), [
        pairs(4, 4, "star", "star", "#fbc02d", "#fbc02d", gap=130, r=22),
        T("Do not trust the look. Pair them: every star has a partner and none is left.",
          "لا نثق بالمظهر. نُقرن: لكل نجمة شريك ولم يبقَ شيء.",
          "Ne te fie pas à l'aspect. Apparie : chaque étoile a un partenaire et il n'en reste aucune."),
        F("4 and 4 → as many as"),
    ]),
    EX("3", "39", st("Make a collection with as many circles as the 4 green blocks.", "كوّن مجموعة فيها دوائر بقدر المكعبات الخضراء الأربعة.", "Fais une collection avec autant de cercles que les 4 cubes verts."), [
        pairs(4, 4, "square", "circle", "#43a047", "#1e63d6"),
        T("Place one circle for each green block. If only three circles, one block has no partner. If five, one circle is extra.",
          "نضع دائرة لكل مكعب أخضر. إذا وضعنا ثلاث دوائر فقط بقي مكعب بلا شريك. وإذا وضعنا خمسًا زادت دائرة.",
          "On place un cercle pour chaque cube vert. Avec trois cercles, un cube reste sans partenaire. Avec cinq, un cercle est en trop."),
        F("4 circles"),
    ]),
    EX("4", "39", st("Prove in two ways that 7 objects and 7 objects are as many.", "أثبت بطريقتين أن 7 أشياء و7 أشياء بقدر بعضهما.", "Prouve de deux façons que 7 objets et 7 objets sont autant."), [
        pairs(7, 7, "circle", "circle", "#fb8c00", "#8e24aa", gap=80, r=20),
        T("Method one: pair them and nothing is left. Method two: count them, seven and seven.",
          "الطريقة الأولى: نُقرن ولا يبقى شيء. الطريقة الثانية: نعدّ، سبعة وسبعة.",
          "Première façon : on apparie et il ne reste rien. Deuxième façon : on compte, sept et sept."),
        F("7 and 7 → as many as"),
    ]),
    EX("5", "39", st("Are there as many fish as flowers? Four fish and four flowers.", "هل الأسماك بقدر الزهور؟ أربع أسماك وأربع زهور.", "Y a-t-il autant de poissons que de fleurs ? Quatre poissons et quatre fleurs."), [
        pairs(4, 4, "tri", "circle", "#1e63d6", "#e53935"),
        T("Each fish has a flower partner, and the count is four and four.",
          "لكل سمكة زهرة شريكة، والعدّ أربعة وأربعة.",
          "Chaque poisson a une fleur partenaire, et on compte quatre et quatre."),
        F("Yes: as many as."),
    ]),
    EX("6", "39", st("Error detective: 4 stars and 3 circles. Someone says A has as many objects as B. Is it right?", "المحقق: 4 نجوم و3 دوائر. قال أحدهم إن A بقدر B. هل هذا صحيح؟", "Détective : 4 étoiles et 3 cercles. Quelqu'un dit que A a autant que B. Est-ce juste ?"), [
        pairs(4, 3, "star", "circle", "#fbc02d", "#1e63d6"),
        T("Pair them. One star is left without a partner. So it is not as many.",
          "نُقرن. تبقى نجمة بلا شريك. إذن ليستا بقدر بعضهما.",
          "Apparie. Une étoile reste sans partenaire. Ce n'est donc pas autant."),
        F("Wrong: 4 and 3 are not as many."),
    ]),
    EX("7", "39", st("Challenge: 6 children and each wants one balloon. How many balloons must I bring?", "تحدٍّ: 6 أطفال وكل طفل يريد بالونًا. كم بالونًا أحضر؟", "Défi : 6 enfants et chacun veut un ballon. Combien de ballons dois-je apporter ?"), [
        pairs(6, 6, "circle", "circle", "#8e24aa", "#e53935", gap=80, r=20),
        T("Each child takes one balloon, so imagine pairs. For as many balloons as children, I need the same number.",
          "كل طفل يأخذ بالونًا، فنتخيّل الأزواج. لتكون البالونات بقدر الأطفال أحتاج العدد نفسه.",
          "Chaque enfant prend un ballon : imagine des paires. Pour autant de ballons que d'enfants, il en faut le même nombre."),
        F("6 balloons"),
    ]),
    EX("8", "39", st("Why are 4 objects and 5 objects not as many?", "لماذا 4 أشياء و5 أشياء ليست بقدر بعضهما؟", "Pourquoi 4 objets et 5 objets ne sont-ils pas autant ?"), [
        pairs(4, 5, "square", "circle", "#fb8c00", "#1e63d6"),
        T("After pairing, one object is left without a partner. As many as needs that nothing is left on either side.",
          "بعد الإقران يبقى شيء بلا شريك. أما بقدر فتحتاج ألّا يبقى شيء في أي جهة.",
          "Après l'appariement, un objet reste sans partenaire. Autant que demande qu'il ne reste rien d'aucun côté."),
    ]),
]
