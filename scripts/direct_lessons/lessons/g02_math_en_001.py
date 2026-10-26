"""Grade 2 Mathematics — Numbers up to 20."""
from scripts.direct_lessons.common import T, F, EX, st, tens

LESSON_ID = "G02-MATH-EN-001"
GRADE = 2
SUBJECT = "math"
TITLES = {"en": "Numbers up to 20", "ar": "الأعداد حتى 20", "fr": "Les nombres jusqu'à 20"}

THEORY = [
    ("One number, many pictures", "عدد واحد وصور كثيرة", "Un nombre, plusieurs images", "11", [
        tens(1, 5, eq=True),
        T("Hello, champion! Today we work on numbers up to 20. We do not just memorise them. We see each number in several ways: the quantity, tens and ones, the numeral, and the word. If I have one ten and 5 ones, then 10 + 5 = 15. So 15 = 1 ten and 5 ones.",
          "مرحبًا يا بطل! اليوم نعمل على الأعداد حتى 20. لا نحفظها فقط، بل نرى كل عدد بعدة صور: الكمية، والعشرات والآحاد، والرقم، والكلمة. إذا كان عندي عشرة و5 آحاد فإن 10 + 5 = 15. إذن 15 = عشرة و5 آحاد.",
          "Bonjour champion ! Aujourd'hui, les nombres jusqu'à 20. On ne les apprend pas seulement par cœur : on voit chaque nombre de plusieurs façons : la quantité, dizaines et unités, le chiffre et le mot. Une dizaine et 5 unités : 10 + 5 = 15. Donc 15 = 1 dizaine et 5 unités."),
        F("quantity → tens and ones → numeral → word"),
    ]),
    ("A number tells how many", "العدد يخبرنا كم", "Un nombre dit combien", "11", [
        tens(0, 9, bundled=False, eq=True),
        T("Here is a group of green objects. Do not write a number before you are sure. Count calmly, one by one: 9. The numeral must match the real quantity.",
          "هنا مجموعة أشياء خضراء. لا نكتب عددًا قبل أن نتأكد. نعدّ بهدوء واحدًا واحدًا: 9. يجب أن يطابق الرقم الكمية الحقيقية.",
          "Voici un groupe d'objets verts. On n'écrit pas de nombre avant d'être sûr. On compte calmement, un par un : 9. Le chiffre doit correspondre à la quantité réelle."),
    ]),
    ("Ten-blocks show numbers fast", "قوالب العشرة تُظهر الأعداد بسرعة", "Les barres de dix montrent vite les nombres", "12", [
        tens(1, 6, eq=True),
        T("The long rectangle has 10 unit squares: it is one ten. Each single square is one. If we see one ten and 6 ones, we do not count from 1 to 16. We say 10 + 6 = 16.",
          "المستطيل الطويل فيه 10 مربعات صغيرة: إنه عشرة واحدة. وكل مربع منفرد هو واحد. إذا رأينا عشرة و6 آحاد فلا نعدّ من 1 إلى 16، بل نقول 10 + 6 = 16.",
          "Le long rectangle a 10 petits carrés : c'est une dizaine. Chaque carré seul est une unité. Pour une dizaine et 6 unités, on ne compte pas de 1 à 16 : 10 + 6 = 16."),
        F("1 ten + 6 ones = 10 + 6 = 16"),
    ]),
    ("Digits and words mean the same", "الأرقام والكلمات تعني الكمية نفسها", "Chiffres et mots disent la même quantité", "13", [
        F("11 eleven   12 twelve   13 thirteen   14 fourteen   15 fifteen"),
        F("16 sixteen   17 seventeen   18 eighteen   19 nineteen   20 twenty"),
        T("A number can be written with digits, like 15, or with a word, like fifteen. Both show the same quantity. Be careful: nineteen is 19, not 90, and sixteen is 16, not 61. Also twelve is 12, and twenty is 20.",
          "يمكن كتابة العدد بالأرقام مثل 15 أو بالكلمة مثل fifteen. كلاهما يمثل الكمية نفسها. انتبه: nineteen هو 19 وليس 90 و sixteen هو 16 وليس 61. وكذلك twelve هو 12 و twenty هو 20. (بالعربية: خمسة عشر، ستة عشر، تسعة عشر، عشرون.)",
          "Un nombre s'écrit avec des chiffres, comme 15, ou avec un mot, comme quinze. C'est la même quantité. Attention : dix-neuf, c'est 19 et non 90 ; seize, c'est 16 et non 61. Douze, c'est 12 ; vingt, c'est 20."),
    ]),
    ("Teen numbers: one ten plus some ones", "أعداد العشرات: عشرة وبعض الآحاد", "Les nombres de 11 à 19 : une dizaine et des unités", "13", [
        tens(1, 1, tag="A", eq=True),
        tens(1, 4, tag="B", eq=True),
        tens(1, 9, tag="C", eq=True),
        T("Every number from 11 to 19 is 1 ten plus some ones: 11 = 10 + 1, 14 = 10 + 4, 19 = 10 + 9. And 20 is 2 tens and 0 ones.",
          "كل عدد من 11 إلى 19 هو عشرة وبعض الآحاد: 11 = 10 + 1 و14 = 10 + 4 و19 = 10 + 9. أما 20 فهي عشرتان وصفر آحاد.",
          "Chaque nombre de 11 à 19 est 1 dizaine plus des unités : 11 = 10 + 1, 14 = 10 + 4, 19 = 10 + 9. Et 20 = 2 dizaines et 0 unité."),
        F("20 = 2 tens + 0 ones"),
    ]),
    ("Find the missing ones", "نجد الآحاد الناقصة", "Trouver les unités manquantes", "13", [
        F("10 + ___ = 16"),
        T("We do not guess. We ask: 16 has one ten and how many ones? 6. So 10 + 6 = 16. Check: it works.",
          "لا نخمّن. نسأل: في 16 عشرة وكم واحدًا؟ 6. إذن 10 + 6 = 16. نتحقق: صحيح.",
          "On ne devine pas. On demande : 16, c'est une dizaine et combien d'unités ? 6. Donc 10 + 6 = 16. Vérification : c'est juste."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("The same number can be seen as a quantity, as tens and ones, as a numeral and as a word. For example 15 = fifteen = 10 + 5 = 1 ten and 5 ones. 20 is two tens.",
          "العدد نفسه يمكن أن نراه كمية أو عشرات وآحادًا أو رقمًا أو كلمة. مثلًا 15 = fifteen = 10 + 5 = عشرة و5 آحاد. والعدد 20 هو عشرتان.",
          "Un même nombre peut se voir comme quantité, dizaines et unités, chiffre ou mot. Par exemple 15 = quinze = 10 + 5 = 1 dizaine et 5 unités. 20, c'est deux dizaines."),
        F("SEE THE QUANTITY → FIND THE TENS → FIND THE ONES → NAME THE NUMBER → CHECK ANOTHER FORM"),
    ]),
]

EXERCISES = [
    EX("1", "12", st("Complete with the corresponding number: three pictures (9 objects, 15 strawberries, 18 beads).", "أكمل بالعدد المناسب: ثلاث صور (9 أشياء و15 فراولة و18 خرزة).", "Complète avec le nombre correspondant : trois images (9 objets, 15 fraises, 18 perles)."), [
        tens(0, 9, bundled=False, eq=True),
        tens(1, 5, eq=True),
        tens(1, 8, eq=True),
        T("Count each picture once: 9, 15, 18. For the beads, follow them around without counting any bead twice.",
          "نعدّ كل صورة مرة واحدة: 9 و15 و18. وفي الخرز نتبعها حول الشكل دون عدّ أي خرزة مرتين.",
          "On compte chaque image une fois : 9, 15, 18. Pour les perles, on fait le tour sans compter une perle deux fois."),
        F("9 — 15 — 18"),
    ]),
    EX("2", "12", st("Complete with the corresponding number: 5 squares, 9 squares, 1 ten + 6 ones, 1 ten + 1 one, 2 tens.", "أكمل بالعدد المناسب: 5 مربعات و9 مربعات وعشرة + 6 آحاد وعشرة + واحد وعشرتان.", "Complète avec le nombre : 5 carrés, 9 carrés, 1 dizaine + 6 unités, 1 dizaine + 1 unité, 2 dizaines."), [
        tens(1, 6, eq=True),
        F("5 — 9 — 16 — 11 — 20"),
        T("No full ten in the first two, so 0 tens + 5 ones = 5 and 0 tens + 9 ones = 9. Then 10 + 6 = 16, 10 + 1 = 11, and 10 + 10 = 20.",
          "في الأولين لا توجد عشرة كاملة فـ0 عشرات + 5 آحاد = 5 و0 عشرات + 9 آحاد = 9. ثم 10 + 6 = 16 و10 + 1 = 11 و10 + 10 = 20.",
          "Pas de dizaine entière pour les deux premiers : 5 et 9. Puis 10 + 6 = 16, 10 + 1 = 11, 10 + 10 = 20."),
    ]),
    EX("3", "12", st("Write in digits: seven, thirteen, fifteen, five, eighteen, fourteen, sixteen, four, eleven, nineteen, twelve, six.", "اكتب بالأرقام: سبعة، ثلاثة عشر، خمسة عشر، خمسة، ثمانية عشر، أربعة عشر، ستة عشر، أربعة، أحد عشر، تسعة عشر، اثنا عشر، ستة.", "Écris en chiffres : sept, treize, quinze, cinq, dix-huit, quatorze, seize, quatre, onze, dix-neuf, douze, six."), [
        F("7   13   15   5   18   14"),
        F("16   4   11   19   12   6"),
        T("Quick check: thirteen starts with 1 because it is more than 10 and less than 20. Nineteen is 19, not 90. Sixteen is 16, not 61.",
          "تحقّق سريع: ثلاثة عشر تبدأ بـ1 لأنها أكبر من 10 وأصغر من 20. وتسعة عشر هي 19 لا 90. وستة عشر هي 16 لا 61.",
          "Vérification rapide : treize commence par 1 car il est plus grand que 10 et plus petit que 20. Dix-neuf, c'est 19, pas 90. Seize, c'est 16, pas 61."),
    ]),
    EX("4", "12", st("Write the number: 1 ten and 5 ones; 1 ten; 1 ten and 6 ones; 1 ten and 9 ones; 3, 7, 4, 2 ones with a ten.", "اكتب العدد: عشرة و5 آحاد؛ عشرة؛ عشرة و6 آحاد؛ عشرة و9 آحاد؛ وعشرة مع 3 أو 7 أو 4 أو 2 آحاد.", "Écris le nombre : 1 dizaine et 5 unités ; 1 dizaine ; 1 dizaine et 6 ; 1 dizaine et 9 ; une dizaine avec 3, 7, 4, 2 unités."), [
        F("15   10   16   19"),
        F("13   17   14   12"),
        T("Each time: 10 + the ones.", "في كل مرة: 10 + الآحاد.", "À chaque fois : 10 + les unités."),
    ]),
    EX("5", "13", st("Copy the number words carefully: one, two, six, nine.", "انسخ كلمات الأعداد بعناية: one, two, six, nine.", "Recopie soigneusement les mots-nombres : one, two, six, nine."), [
        F("one   two   six   nine"),
        T("We keep the spelling exactly the same: one, two, six, nine.",
          "نحافظ على الإملاء نفسه تمامًا: one وtwo وsix وnine. (بالعربية: واحد، اثنان، ستة، تسعة.)",
          "On garde exactement la même orthographe : one, two, six, nine. (En français : un, deux, six, neuf.)"),
    ]),
    EX("6", "13", st("Write in words: 5, 10, 3, 8, 1, 13, 7, 16, 19, 14, 2, 6, 9, 11, 4, 12, 15, 17, 18, 20.", "اكتب بالكلمات: 5، 10، 3، 8، 1، 13، 7، 16، 19، 14، 2، 6، 9، 11، 4، 12، 15، 17، 18، 20.", "Écris en mots : 5, 10, 3, 8, 1, 13, 7, 16, 19, 14, 2, 6, 9, 11, 4, 12, 15, 17, 18, 20."), [
        F("five  ten  three  eight  one  thirteen  seven  sixteen  nineteen  fourteen"),
        F("two  six  nine  eleven  four  twelve  fifteen  seventeen  eighteen  twenty"),
        T("Watch the words we sometimes get wrong: twelve, thirteen, fifteen, eighteen, twenty.",
          "انتبه إلى الكلمات التي نخطئ فيها أحيانًا: twelve وthirteen وfifteen وeighteen وtwenty.",
          "Attention aux mots difficiles : twelve, thirteen, fifteen, eighteen, twenty."),
    ]),
    EX("7", "13", st("Write in words: 1 ten and 3 ones; 1 ten; 1 ten and 7 ones; 1 ten and 4 ones; 1 ten and 6 ones; 1 ten and 2 ones; 2 tens; 1 ten and 1 one; 1 ten and 5 ones; 1 ten and 8 ones.", "اكتب بالكلمات: عشرة و3 آحاد؛ عشرة؛ عشرة و7؛ عشرة و4؛ عشرة و6؛ عشرة و2؛ عشرتان؛ عشرة وواحد؛ عشرة و5؛ عشرة و8.", "Écris en mots : 1 dizaine et 3 unités ; 1 dizaine ; 1 et 7 ; 1 et 4 ; 1 et 6 ; 1 et 2 ; 2 dizaines ; 1 et 1 ; 1 et 5 ; 1 et 8."), [
        F("thirteen  ten  seventeen  fourteen  sixteen"),
        F("twelve  twenty  eleven  fifteen  eighteen"),
        T("The same number can be seen as objects, tens and ones, a digit, and a word.",
          "العدد نفسه يمكن أن نراه أشياء، وعشرات وآحادًا، ورقمًا، وكلمة.",
          "Le même nombre se voit en objets, dizaines et unités, chiffre et mot."),
    ]),
    EX("8", "13", st("Find the missing number: 10 + __ = 16, 19, 11, 15, 13, 12, 17, 14, 18.", "أوجد العدد الناقص: 10 + __ = 16، 19، 11، 15، 13، 12، 17، 14، 18.", "Trouve le nombre manquant : 10 + __ = 16, 19, 11, 15, 13, 12, 17, 14, 18."), [
        F("6   9   1   5   3   2   7   4   8"),
        T("Check each one: 10 + 6 = 16, 10 + 9 = 19, 10 + 1 = 11, and so on.",
          "نتحقق من كل واحدة: 10 + 6 = 16 و10 + 9 = 19 و10 + 1 = 11 وهكذا.",
          "On vérifie chacune : 10 + 6 = 16, 10 + 9 = 19, 10 + 1 = 11, etc."),
    ]),
    EX("9", "13", st("Use the same colour for equal numbers: 1 ten 5 ones, twenty, 15, nine, 2 tens, 10 + 5, 20, fifteen, 9.", "استعمل اللون نفسه للأعداد المتساوية: عشرة و5 آحاد، twenty، 15، nine، عشرتان، 10 + 5، 20، fifteen، 9.", "Même couleur pour les nombres égaux : 1 dizaine 5 unités, twenty, 15, nine, 2 dizaines, 10 + 5, 20, fifteen, 9."), [
        F("15 = 1 ten 5 ones = 10 + 5 = fifteen"),
        F("20 = 2 tens = twenty"),
        F("9 = nine"),
        T("The same number can appear in more than one form.",
          "العدد نفسه يمكن أن يظهر بأكثر من صورة.",
          "Le même nombre peut apparaître sous plusieurs formes."),
    ]),
    EX("10", "", st("Mystery number: it has 1 ten and 8 ones.", "عدد غامض: فيه عشرة و8 آحاد.", "Nombre mystère : il a 1 dizaine et 8 unités."), [
        tens(1, 8, eq=True),
        F("18 = eighteen = 10 + 8 = 1 ten and 8 ones"),
    ]),
    EX("11", "", st("Error detective: 1 ten and 7 ones = 71. And is 2 tens = 20 correct?", "المحقق: عشرة و7 آحاد = 71. وهل 2 عشرات = 20 صحيح؟", "Détective : 1 dizaine et 7 unités = 71. Et 2 dizaines = 20 est-il juste ?"), [
        tens(1, 7, eq=True),
        T("The first claim is wrong: 10 + 7 = 17, not 71. The second is right: 2 tens = 10 + 10 = 20.",
          "الادعاء الأول خطأ: 10 + 7 = 17 لا 71. والثاني صحيح: عشرتان = 10 + 10 = 20.",
          "La première affirmation est fausse : 10 + 7 = 17 et non 71. La seconde est juste : 2 dizaines = 10 + 10 = 20."),
    ]),
    EX("12", "", st("Final check: fourteen in digits; 18 in words; 1 ten and 2 ones; 2 tens; 10 + __ = 19; correct 1 ten and 6 ones = 61; why is 20 different from 19?", "تقييم أخير: fourteen بالأرقام؛ 18 بالكلمات؛ عشرة و2؛ عشرتان؛ 10 + __ = 19؛ صحّح عشرة و6 آحاد = 61؛ ولماذا 20 تختلف عن 19؟", "Évaluation : fourteen en chiffres ; 18 en mots ; 1 dizaine et 2 unités ; 2 dizaines ; 10 + __ = 19 ; corrige 1 dizaine et 6 = 61 ; pourquoi 20 est différent de 19 ?"), [
        F("14      eighteen      12      20      10 + 9 = 19      10 + 6 = 16"),
        T("20 is 2 complete tens and 0 ones. 19 is 1 ten and 9 ones.",
          "20 هي عشرتان كاملتان وبلا آحاد. و19 هي عشرة و9 آحاد.",
          "20, c'est 2 dizaines entières et 0 unité. 19, c'est 1 dizaine et 9 unités."),
    ]),
]
