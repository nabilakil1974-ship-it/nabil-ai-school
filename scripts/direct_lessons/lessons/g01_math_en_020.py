"""Grade 1 Mathematics — Tens and ones."""
from scripts.direct_lessons.common import T, F, EX, st, tens, objects, scene, _shape

LESSON_ID = "G01-MATH-EN-020"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Tens and ones", "ar": "العشرات والآحاد", "fr": "Dizaines et unités"}

THEORY = [
    ("Ten ones make one ten", "عشرة آحاد تصنع عشرة واحدة", "Dix unités font une dizaine", "56", [
        T("Hello! Do you remember grouping? Today we use grouping in a very special way. Here are ten counters. Count them: ten. We have ten ones. Now we tie them together as a bundle.",
          "مرحبًا! هل تذكر التجميع؟ اليوم نستعمله بطريقة خاصة جدًا. هنا عشرة عدّادات. نعدّها: عشرة. عندنا عشرة آحاد. الآن نربطها معًا في حزمة.",
          "Bonjour ! Tu te souviens du regroupement ? Aujourd'hui on l'utilise d'une façon spéciale. Voici dix jetons. Compte : dix. On a dix unités. Maintenant on les lie en un paquet."),
        objects(10, "circle", "#1e63d6", prefix="u", r=24),
        tens(1, 0),
        T("This bundle still has ten ones inside, but now we can call it one ten.",
          "هذه الحزمة ما زال فيها عشرة آحاد، لكن صار بإمكاننا أن نسمّيها عشرة واحدة.",
          "Ce paquet contient toujours dix unités, mais on peut maintenant l'appeler une dizaine."),
        F("10 ones = 1 ten"),
        T("To check, we open the bundle and count the ones inside: one to ten. When we make a bundle, the quantity does not change; the organization becomes easier.",
          "للتحقق نفتح الحزمة ونعدّ الآحاد داخلها: من واحد إلى عشرة. عندما نصنع حزمة لا تتغير الكمية، بل يصبح التنظيم أسهل.",
          "Pour vérifier, on ouvre le paquet et on compte les unités : de un à dix. Quand on fait un paquet, la quantité ne change pas ; l'organisation devient plus simple."),
    ]),
    ("Loose objects are ones", "الأشياء المنفردة آحاد", "Les objets seuls sont des unités", "56", [
        tens(1, 3),
        T("Here is one ten. And these objects that are not inside the ten we call ones. How many loose ones? Three. So: 1 ten and 3 ones.",
          "هنا عشرة واحدة. والأشياء التي ليست داخل العشرة نسمّيها آحادًا. كم واحدًا منفردًا؟ ثلاثة. إذن: عشرة واحدة وثلاثة آحاد.",
          "Voici une dizaine. Les objets qui ne sont pas dans la dizaine s'appellent des unités. Combien d'unités seules ? Trois. Donc : 1 dizaine et 3 unités."),
        T("Be careful: the bundle is called one ten, but inside it there are ten ones.",
          "انتبه: الحزمة اسمها عشرة واحدة، لكن بداخلها عشرة آحاد.",
          "Attention : le paquet s'appelle une dizaine, mais à l'intérieur il y a dix unités."),
    ]),
    ("Bundle without changing the quantity", "نحزم دون أن تتغير الكمية", "Grouper sans changer la quantité", "57", [
        objects(10, "circle", "#1e63d6", prefix="a", r=24),
        T("We have twelve counters. Take ten and bundle them. What is left loose? Two.",
          "عندنا اثنا عشر عدّادًا. نأخذ عشرة ونحزمها. ماذا بقي منفردًا؟ اثنان.",
          "On a douze jetons. On en prend dix et on les lie. Qu'est-ce qui reste seul ? Deux."),
        tens(1, 2),
        T("Before grouping, the same objects. After grouping: one ten and two ones. The quantity is the same.",
          "قبل التجميع الأشياء نفسها. وبعده: عشرة واحدة وآحاد اثنان. الكمية نفسها.",
          "Avant le regroupement, les mêmes objets. Après : une dizaine et deux unités. La quantité est la même."),
    ]),
    ("Unbundle to verify", "نفكّ الحزمة للتحقق", "Défaire le paquet pour vérifier", "57", [
        tens(1, 0),
        T("If we see a ten bundle and do not believe it has ten, we open it.",
          "إذا رأينا حزمة عشرة ولم نصدّق أن فيها عشرة، نفتحها.",
          "Si on voit un paquet de dix et qu'on n'y croit pas, on l'ouvre."),
        tens(1, 0, bundled=False),
        T("Count: ten. A bundle is not a magic symbol. We must always be able to go back from it to the single units.",
          "نعدّ: عشرة. الحزمة ليست رمزًا سحريًا. يجب أن نستطيع دائمًا الرجوع منها إلى الوحدات المنفردة.",
          "Compte : dix. Un paquet n'est pas un symbole magique. On doit toujours pouvoir revenir aux unités seules."),
    ]),
    ("Build from tens and ones", "نبني من العشرات والآحاد", "Construire avec dizaines et unités", "57", [
        F("1 ten and 3 ones"),
        T("Build it: take a bundle that has exactly ten, then add exactly three loose ones. Is the ten exactly ten? Are there exactly three loose? Then we understand the picture from the opposite direction.",
          "نبنيها: نأخذ حزمة فيها عشرة بالضبط، ثم نضيف ثلاثة آحاد منفردة بالضبط. هل العشرة عشرة تمامًا؟ هل المنفرد ثلاثة تمامًا؟ هكذا نفهم الصورة من الاتجاه المعاكس.",
          "On construit : on prend un paquet de dix exactement, puis on ajoute exactement trois unités seules. La dizaine est-elle exactement dix ? Y a-t-il exactement trois unités ? Alors on comprend l'image dans l'autre sens."),
        tens(1, 3),
    ]),
    ("Explain tens and ones", "نشرح العشرات والآحاد", "Expliquer dizaines et unités", "57", [
        tens(1, 4),
        T("There is one group of ten and four loose ones. How can we be sure the ten is right? We unbundle it and count ten.",
          "هناك مجموعة عشرة واحدة وأربعة آحاد منفردة. كيف نتأكد أن العشرة صحيحة؟ نفكّها ونعدّ عشرة.",
          "Il y a un groupe de dix et quatre unités seules. Comment être sûr que la dizaine est juste ? On la défait et on compte dix."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Ten ones make one ten. The objects that do not fill a complete ten stay ones. A bundle changes the organization, not the quantity.",
          "عشرة آحاد تصنع عشرة واحدة. والأشياء التي لا تكمّل عشرة تبقى آحادًا. الحزمة تغيّر التنظيم لا الكمية.",
          "Dix unités font une dizaine. Les objets qui ne complètent pas une dizaine restent des unités. Un paquet change l'organisation, pas la quantité."),
        F("COUNT → TAKE EXACTLY 10 → BUNDLE AS ONE TEN → KEEP THE REST AS ONES → UNBUNDLE TO CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "56", st("Make one ten from loose counters.", "كوّن عشرة واحدة من عدّادات منفردة.", "Fais une dizaine avec des jetons seuls."), [
        objects(10, "circle", "#1e63d6", prefix="a", r=24),
        T("A ten has exactly ten. With nine, one is missing. With eleven, the extra one stays loose.",
          "العشرة فيها عشرة بالضبط. مع تسعة ينقص واحد. ومع أحد عشر يبقى الزائد منفردًا.",
          "Une dizaine a exactement dix. Avec neuf, il en manque un. Avec onze, le surplus reste seul."),
        tens(1, 0),
        F("one ten"),
    ]),
    EX("2", "56", st("How many tens and how many ones?", "كم عشرة وكم واحدًا؟", "Combien de dizaines et combien d'unités ?"), [
        tens(1, 5),
        F("1 ten and 5 ones"),
        T("Remember: the bundle is called one ten, but inside it there are ten ones.",
          "تذكّر: الحزمة اسمها عشرة واحدة وبداخلها عشرة آحاد.",
          "Souviens-toi : le paquet s'appelle une dizaine, mais il contient dix unités."),
    ]),
    EX("3", "57", st("Bundle one ten from 14 counters and leave the rest.", "اربط عشرة واحدة من 14 عدّادًا واترك الباقي.", "Lie une dizaine parmi 14 jetons et laisse le reste."), [
        tens(1, 4),
        T("How many ones are left? Four. One ten and four ones. Unbundle and recount: the grouping kept the total.",
          "كم واحدًا بقي؟ أربعة. عشرة واحدة وأربعة آحاد. نفكّ ونعيد العدّ: التجميع حفظ المجموع.",
          "Combien d'unités restent ? Quatre. Une dizaine et quatre unités. On défait et on recompte : le regroupement a gardé le total."),
        F("14 = 1 ten and 4 ones"),
    ]),
    EX("4", "57", st("Open the ten in 1 ten and 2 ones. Did the quantity change?", "افتح العشرة في عشرة واحدة وواحدين. هل تغيّرت الكمية؟", "Ouvre la dizaine dans 1 dizaine et 2 unités. La quantité a-t-elle changé ?"), [
        tens(1, 2),
        tens(1, 2, bundled=False),
        T("Count all the objects: twelve. The quantity did not change.",
          "نعدّ كل الأشياء: اثنا عشر. الكمية لم تتغير.",
          "On compte tous les objets : douze. La quantité n'a pas changé."),
    ]),
    EX("5", "57", st("Build 1 ten and 6 ones.", "ابنِ عشرة واحدة وستة آحاد.", "Construis 1 dizaine et 6 unités."), [
        tens(1, 6),
        T("Start with the ten, then add the loose ones one by one. Check: the bundle is ten, six are loose, nothing counted twice.",
          "نبدأ بالعشرة ثم نضيف الآحاد المنفردة واحدًا واحدًا. نتحقق: الحزمة عشرة، وستة منفردة، ولا شيء عُدّ مرتين.",
          "On commence par la dizaine, puis on ajoute les unités une à une. Vérification : le paquet fait dix, six sont seules, rien n'est compté deux fois."),
    ]),
    EX("6", "57", st("Error detective: a bundle is called one ten, but it holds only 9.", "المحقق: حزمة سمّيناها عشرة لكن فيها 9 فقط.", "Détective : un paquet appelé une dizaine ne contient que 9."), [
        objects(9, "circle", "#1e63d6", prefix="n", r=24),
        T("Before we call it a ten, we count. There are nine. So it is not a complete ten. One is missing.",
          "قبل أن نسمّيها عشرة نعدّ. فيها تسعة. إذن ليست عشرة كاملة. ينقص واحد.",
          "Avant de l'appeler dizaine, on compte. Il y en a neuf. Ce n'est pas une dizaine complète. Il en manque un."),
    ]),
    EX("7", "57", st("Challenge: 10 pencils tied together and 3 loose pencils. Tell the organization.", "تحدٍّ: 10 أقلام مربوطة و3 أقلام منفردة. قل التنظيم.", "Défi : 10 crayons liés et 3 crayons seuls. Dis l'organisation."), [
        tens(1, 3),
        F("one ten and 3 ones"),
        T("Open the bundle and count as a check.",
          "نفتح الحزمة ونعدّ للتحقق.",
          "On ouvre le paquet et on compte pour vérifier."),
    ]),
    EX("8", "57", st("Final check: why is one ten made of ten ones?", "تقييم أخير: لماذا العشرة الواحدة مكوّنة من عشرة آحاد؟", "Évaluation : pourquoi une dizaine est-elle faite de dix unités ?"), [
        tens(1, 0),
        tens(1, 0, bundled=False),
        T("One ten is made of ten ones. When we open the bundle and count, we find ten single ones.",
          "العشرة الواحدة مكوّنة من عشرة آحاد. عندما نفتح الحزمة ونعدّ نجد عشرة آحاد منفردة.",
          "Une dizaine est faite de dix unités. Quand on ouvre le paquet et qu'on compte, on trouve dix unités seules."),
    ]),
]
