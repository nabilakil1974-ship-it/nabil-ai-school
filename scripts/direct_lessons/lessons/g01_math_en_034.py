"""Grade 1 Mathematics — The tens from 20 up to 60."""
from scripts.direct_lessons.common import T, F, EX, st, tens, numpath

LESSON_ID = "G01-MATH-EN-034"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "The tens from 20 up to 60", "ar": "العشرات من 20 إلى 60", "fr": "Les dizaines de 20 à 60"}
TENS = ["20", "30", "40", "50", "60"]

THEORY = [
    ("Two tens make 20", "عشرتان تصنعان 20", "Deux dizaines font 20", "88", [
        T("Hello! Do you remember one ten? One ten is 10 ones. Today, instead of counting every object one by one, we count bundles of ten. Here are two bundles. Each bundle has 10. How many in all? Do not open a bundle if there is no need. Count by tens: ten, twenty.",
          "مرحبًا! هل تذكر العشرة الواحدة؟ العشرة الواحدة هي 10 آحاد. اليوم بدل أن نعدّ كل شيء واحدًا واحدًا نعدّ حزم العشرات. هنا حزمتان. في كل حزمة 10. كم المجموع؟ لا نفتح حزمة إذا لم يكن هناك داعٍ. نعدّ بالعشرات: عشرة، عشرون.",
          "Bonjour ! Tu te souviens d'une dizaine ? Une dizaine, c'est 10 unités. Aujourd'hui, au lieu de compter chaque objet, on compte des paquets de dix. Voici deux paquets. Chaque paquet a 10. Combien en tout ? N'ouvre pas un paquet sans raison. Compte par dizaines : dix, vingt."),
        tens(1, 0, label=False),
        tens(2, 0, eq=True),
        T("One ten is 10. Two tens are 20. So 20 is not twenty loose objects that we must count each time; we can see two complete tens.",
          "عشرة واحدة 10. وعشرتان 20. إذن 20 ليست عشرين شيئًا منفردًا نعدّها كل مرة، بل نرى عشرتين كاملتين.",
          "Une dizaine, c'est 10. Deux dizaines, c'est 20. Donc 20 n'est pas vingt objets seuls à recompter ; on voit deux dizaines complètes."),
    ]),
    ("30, 40, 50, 60 as complete tens", "30 و40 و50 و60 عشرات كاملة", "30, 40, 50, 60 : des dizaines complètes", "88", [
        tens(3, 0, eq=True),
        tens(4, 0, eq=True),
        tens(5, 0, eq=True),
        tens(6, 0, eq=True),
        T("Two tens are 20. Add a complete ten: three tens are 30. Another ten: four tens are 40. Five tens are 50. Six tens are 60. Each step here is not one more. It is one ten more.",
          "عشرتان 20. نضيف عشرة كاملة: ثلاث عشرات 30. عشرة أخرى: أربع عشرات 40. خمس عشرات 50. ست عشرات 60. كل خطوة هنا ليست واحدًا أكثر بل عشرة أكثر.",
          "Deux dizaines, 20. On ajoute une dizaine complète : trois dizaines, 30. Une autre : quatre dizaines, 40. Cinq dizaines, 50. Six dizaines, 60. Chaque pas n'est pas un de plus, c'est une dizaine de plus."),
    ]),
    ("Match the numeral to the number of tens", "نطابق العدد مع عدد العشرات", "Associer le nombre au nombre de dizaines", "89", [
        numpath(TENS, size=56),
        T("Each numeral must match the exact number of ten-groups. 50 is 5 bundles. 30 is 3 bundles. We read them by tens: twenty, thirty, forty, fifty, sixty.",
          "كل عدد يجب أن يطابق عدد مجموعات العشرة بالضبط. 50 هي 5 حزم. و30 هي 3 حزم. نقرؤها بالعشرات: عشرون، ثلاثون، أربعون، خمسون، ستون.",
          "Chaque nombre doit correspondre au nombre exact de groupes de dix. 50, c'est 5 paquets. 30, c'est 3 paquets. On les lit par dizaines : vingt, trente, quarante, cinquante, soixante."),
    ]),
    ("Order the whole tens", "نرتّب العشرات الكاملة", "Ranger les dizaines entières", "89", [
        numpath(TENS, size=56),
        T("Each step adds one complete ten. After 30 comes 40. Before 50 comes 40. After 50 comes 60.",
          "كل خطوة تزيد عشرة كاملة. بعد 30 يأتي 40. وقبل 50 يأتي 40. وبعد 50 يأتي 60.",
          "Chaque pas ajoute une dizaine complète. Après 30 vient 40. Avant 50 vient 40. Après 50 vient 60."),
    ]),
    ("One more ten changes the tens number", "عشرة أخرى تغيّر عدد العشرات", "Une dizaine de plus change le nombre de dizaines", "89", [
        tens(4, 0, eq=True),
        T("I have 40, that is 4 tens. If I add a complete bundle of ten, what happens? We get 50: 4 tens plus 1 ten is 5 tens, which is 50.",
          "عندي 40 أي 4 عشرات. إذا أضفت حزمة كاملة من عشرة فماذا يحدث؟ نحصل على 50: 4 عشرات و1 عشرة تساوي 5 عشرات أي 50.",
          "J'ai 40, soit 4 dizaines. Si j'ajoute un paquet complet de dix, que se passe-t-il ? On obtient 50 : 4 dizaines plus 1 dizaine font 5 dizaines, soit 50."),
        tens(5, 0, eq=True),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Whole tens are complete groups of ten: 20 is 2 tens, 30 is 3 tens, 40 is 4 tens, 50 is 5 tens, 60 is 6 tens.",
          "العشرات الكاملة مجموعات كاملة من عشرة: 20 هي عشرتان، و30 ثلاث عشرات، و40 أربع عشرات، و50 خمس عشرات، و60 ست عشرات.",
          "Les dizaines entières sont des groupes complets de dix : 20, c'est 2 dizaines ; 30, 3 dizaines ; 40, 4 ; 50, 5 ; 60, 6."),
        F("COUNT THE BUNDLES → COUNT BY TENS → MATCH THE NUMERAL → ORDER → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "88", st("Build 20 using complete ten-bundles.", "ابنِ 20 بحزم عشرات كاملة.", "Construis 20 avec des paquets de dix complets."), [
        tens(2, 0, eq=True),
        T("Each bundle is 10. Ten, twenty: how many bundles did you say? Two.",
          "كل حزمة 10. عشرة، عشرون: كم حزمة قلت؟ اثنتان.",
          "Chaque paquet vaut 10. Dix, vingt : combien de paquets as-tu dits ? Deux."),
    ]),
    EX("2", "88", st("Count the bundles by tens: 4 bundles and 6 bundles.", "عدّ الحزم بالعشرات: 4 حزم و6 حزم.", "Compte les paquets par dizaines : 4 paquets et 6 paquets."), [
        tens(4, 0, eq=True),
        tens(6, 0, eq=True),
        F("10, 20, 30, 40 → 40      10, 20, 30, 40, 50, 60 → 60"),
        T("If you counted 1, 2, 3, 4, that is the number of bundles. But each bundle is worth 10. Now count by tens.",
          "إذا عددت 1، 2، 3، 4 فهذا عدد الحزم. لكن قيمة كل حزمة 10. الآن عدّ بالعشرات.",
          "Si tu as compté 1, 2, 3, 4, c'est le nombre de paquets. Mais chaque paquet vaut 10. Compte maintenant par dizaines."),
    ]),
    EX("3", "89", st("Match: 2 tens ↔ 20, 3 tens ↔ 30, 4 tens ↔ 40, 5 tens ↔ 50, 6 tens ↔ 60.", "طابق: عشرتان ↔ 20، ثلاث عشرات ↔ 30، أربع ↔ 40، خمس ↔ 50، ست ↔ 60.", "Associe : 2 dizaines ↔ 20, 3 ↔ 30, 4 ↔ 40, 5 ↔ 50, 6 ↔ 60."), [
        tens(5, 0, eq=True),
        F("2 tens = 20   3 tens = 30   4 tens = 40   5 tens = 50   6 tens = 60"),
        T("Read them by tens: twenty, thirty, forty, fifty, sixty.",
          "اقرأها بالعشرات: عشرون، ثلاثون، أربعون، خمسون، ستون.",
          "Lis-les par dizaines : vingt, trente, quarante, cinquante, soixante."),
    ]),
    EX("4", "89", st("Missing tens: 20 _ 40 _ 60, and backward 60 50 _ 30 _.", "عشرات ناقصة: 20 _ 40 _ 60 وإلى الخلف 60 50 _ 30 _.", "Dizaines manquantes : 20 _ 40 _ 60, et en arrière 60 50 _ 30 _."), [
        numpath(["20", "?", "40", "?", "60"], size=56),
        numpath(["60", "50", "?", "30", "?"], size=56),
        F("30, 50      40, 20"),
        T("Count by tens, not by ones.",
          "عدّ بالعشرات لا بالآحاد.",
          "Compte par dizaines, pas par unités."),
    ]),
    EX("5", "89", st("One ten more, one ten less: 30 + one ten, 50 + one ten, 60 − one ten, 40 − one ten.", "عشرة أكثر وعشرة أقل: 30 + عشرة، 50 + عشرة، 60 − عشرة، 40 − عشرة.", "Une dizaine de plus, une de moins : 30 + une dizaine, 50 + une dizaine, 60 − une dizaine, 40 − une dizaine."), [
        F("30 → 40      50 → 60      60 → 50      40 → 30"),
        T("We are not adding 1. We are adding a complete group of 10.",
          "نحن لا نضيف 1 بل مجموعة كاملة من 10.",
          "On n'ajoute pas 1. On ajoute un groupe complet de 10."),
    ]),
    EX("6", "89", st("Error detective: 5 bundles are labeled 40.", "المحقق: 5 حزم كُتب عليها 40.", "Détective : 5 paquets portent l'étiquette 40."), [
        tens(5, 0),
        T("Wrong. Count the tens: ten, twenty, thirty, forty, fifty. The right label is 50.",
          "خطأ. نعدّ العشرات: عشرة، عشرون، ثلاثون، أربعون، خمسون. العنوان الصحيح 50.",
          "Faux. Compte les dizaines : dix, vingt, trente, quarante, cinquante. La bonne étiquette est 50."),
        F("5 tens = 50"),
    ]),
    EX("7", "89", st("Challenge: I have 60 and I take away two complete tens. What is left?", "تحدٍّ: عندي 60 وأخذت عشرتين كاملتين. ماذا بقي؟", "Défi : j'ai 60 et j'enlève deux dizaines complètes. Que reste-t-il ?"), [
        tens(6, 0, eq=True),
        T("60 is 6 tens. 6 tens minus 2 tens is 4 tens. So 40 is left.",
          "60 هي 6 عشرات. 6 عشرات ناقص عشرتين تساوي 4 عشرات. إذن بقي 40.",
          "60, c'est 6 dizaines. 6 dizaines moins 2 dizaines font 4 dizaines. Il reste donc 40."),
        tens(4, 0, eq=True),
    ]),
    EX("8", "89", st("Final check: build 20 and 50, read 6 bundles, fill 20 30 _ 50, one ten more than 40, one ten less than 60, and explain why 3 bundles are 30.", "تقييم أخير: ابنِ 20 و50، واقرأ 6 حزم، واملأ 20 30 _ 50، وعشرة أكثر من 40، وعشرة أقل من 60، واشرح لماذا 3 حزم تساوي 30.", "Évaluation : construis 20 et 50, lis 6 paquets, complète 20 30 _ 50, une dizaine de plus que 40, une de moins que 60, explique pourquoi 3 paquets font 30."), [
        tens(3, 0, eq=True),
        F("6 bundles = 60      20 30 40 50      40 → 50      60 → 50"),
        T("Three is the count of bundles. But each bundle is 10, so the whole quantity is 30.",
          "3 هو عدد الحزم. لكن كل حزمة 10، فالكمية كلها 30.",
          "Trois est le nombre de paquets. Mais chaque paquet vaut 10, donc la quantité entière est 30."),
    ]),
]
