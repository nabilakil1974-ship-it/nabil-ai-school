"""Grade 1 Mathematics — Order of numbers up to 9."""
from scripts.direct_lessons.common import T, F, EX, st, numpath, objects

LESSON_ID = "G01-MATH-EN-014"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Order of numbers up to 9", "ar": "ترتيب الأعداد حتى 9", "fr": "L'ordre des nombres jusqu'à 9"}
P = list("123456789")

THEORY = [
    ("The counting order is stable", "ترتيب العدّ ثابت", "L'ordre du comptage est stable", "42", [
        T("Hello! Every number we learned has a fixed place when we count. Here the cards are mixed up. We will put each number back in its place.",
          "مرحبًا! كل عدد تعلّمناه له مكان ثابت عند العدّ. هنا البطاقات مخلوطة، وسنعيد كل عدد إلى مكانه.",
          "Bonjour ! Chaque nombre appris a une place fixe quand on compte. Ici les cartes sont mélangées. On va remettre chaque nombre à sa place."),
        numpath(list("725194386")),
        T("Where do we start counting? From 1. And after 1 comes 2.",
          "من أين نبدأ العدّ؟ من 1. وبعد 1 يأتي 2.",
          "Par où commence-t-on à compter ? Par 1. Et après 1 vient 2."),
        numpath(P),
        F("1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9"),
        T("This order does not change when the cards are mixed. A card can move, but the place of the number in the counting sequence is fixed.",
          "هذا الترتيب لا يتغير عندما نخلط البطاقات. البطاقة قد تتحرك، لكن مكان العدد في سلسلة العدّ ثابت.",
          "Cet ordre ne change pas quand on mélange les cartes. Une carte peut bouger, mais la place du nombre dans la suite du comptage est fixe."),
    ]),
    ("What comes after?", "ماذا يأتي بعد؟", "Qu'est-ce qui vient après ?", "42", [
        numpath(P, hi=4),
        T("Choose the number 5. What comes right after 5? It is 6, because it is the next number when we count. One step forward gives the next number.",
          "نختار العدد 5. ما العدد الذي يأتي بعد 5 مباشرة؟ إنه 6، لأنه العدد التالي عند العدّ. خطوة واحدة إلى الأمام تعطينا العدد التالي.",
          "Choisis le nombre 5. Qu'est-ce qui vient juste après 5 ? C'est 6, car c'est le nombre suivant quand on compte. Un pas en avant donne le nombre suivant."),
        F("after 5 comes 6"),
    ]),
    ("What comes before?", "ماذا يأتي قبل؟", "Qu'est-ce qui vient avant ?", "42", [
        numpath(P, hi=5),
        T("Now the other way. What comes right before 6? It is 5. Before means one step back in the sequence.",
          "الآن بالعكس. ما العدد الذي يأتي قبل 6 مباشرة؟ إنه 5. قبل تعني خطوة واحدة إلى الخلف في السلسلة.",
          "Maintenant dans l'autre sens. Qu'est-ce qui vient juste avant 6 ? C'est 5. Avant veut dire un pas en arrière dans la suite."),
        F("before 6 comes 5"),
    ]),
    ("The next number means one more", "العدد التالي يعني واحدًا أكثر", "Le nombre suivant veut dire un de plus", "43", [
        objects(4, "circle", "#e53935", prefix="a"),
        T("This is 4. We add one more dot.",
          "هذا 4. نضيف نقطة واحدة.",
          "Voici 4. On ajoute un point de plus."),
        objects(5, "circle", "#e53935", prefix="b"),
        T("Now it is 5. When we moved from 4 to the next number 5, the quantity grew by one. So 5 → one more → 6.",
          "صار 5. عندما انتقلنا من 4 إلى العدد التالي 5 زادت الكمية واحدًا. إذن 5 ← واحد أكثر ← 6.",
          "Maintenant c'est 5. En passant de 4 au nombre suivant 5, la quantité a augmenté de un. Donc 5 → un de plus → 6."),
    ]),
    ("Fill a missing number", "نملأ عددًا ناقصًا", "Compléter un nombre manquant", "43", [
        numpath(["1", "2", "?", "4", "5"]),
        T("A number is lost. We do not guess; we read the sequence: one, two, ... The missing number is 3, because it comes after 2 and before 4.",
          "هناك عدد ضائع. لا نخمّن بل نقرأ السلسلة: واحد، اثنان، ... العدد الناقص 3، لأنه بعد 2 وقبل 4.",
          "Un nombre est perdu. On ne devine pas : on lit la suite : un, deux, ... Le nombre manquant est 3, car il vient après 2 et avant 4."),
        numpath(["1", "2", "3", "4", "5"], hi=2),
    ]),
    ("Order some of the numbers", "نرتّب بعض الأعداد", "Ranger quelques nombres", "43", [
        numpath(list("8465")),
        T("Not all the numbers have to be there. We place the ones we have by their true place in the counting: 4, 5, 6, 8.",
          "لا يجب أن تكون كل الأعداد موجودة. نضع الموجودة حسب مكانها الحقيقي في العدّ: 4، 5، 6، 8.",
          "Tous les nombres n'ont pas besoin d'être là. On place ceux qu'on a selon leur vraie place dans le comptage : 4, 5, 6, 8."),
        numpath(["4", "5", "6", "7", "8"], hi=3),
        T("The card 7 is not there, but we know its place: between 6 and 8.",
          "البطاقة 7 غير موجودة لكننا نعرف مكانها: بين 6 و8.",
          "La carte 7 n'est pas là, mais on connaît sa place : entre 6 et 8."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("The numbers from 1 to 9 have a fixed order. Before is one step back. After is one step forward. And the next number means one more.",
          "للأعداد من 1 إلى 9 ترتيب ثابت. قبل تعني خطوة إلى الخلف، وبعد تعني خطوة إلى الأمام، والعدد التالي يعني واحدًا أكثر.",
          "Les nombres de 1 à 9 ont un ordre fixe. Avant : un pas en arrière. Après : un pas en avant. Et le nombre suivant veut dire un de plus."),
        F("SAY THE SEQUENCE → FIND THE NUMBER → BACK FOR BEFORE → FORWARD FOR AFTER → CHECK WITH QUANTITY"),
    ]),
]

EXERCISES = [
    EX("1", "42", st("Put the cards in order: 5 2 4 1 3.", "رتّب البطاقات: 5 2 4 1 3.", "Range les cartes dans l'ordre : 5 2 4 1 3."), [
        numpath(list("52413")),
        T("Say the counting from 1: find 1 first, then 2, then 3.",
          "قل العدّ من 1: ابحث عن 1 أولًا ثم 2 ثم 3.",
          "Dis le comptage depuis 1 : trouve 1 d'abord, puis 2, puis 3."),
        numpath(list("12345")),
        F("1 → 2 → 3 → 4 → 5"),
    ]),
    EX("2", "42", st("What comes after 3? After 7? After 8?", "ماذا يأتي بعد 3؟ وبعد 7؟ وبعد 8؟", "Qu'est-ce qui vient après 3 ? Après 7 ? Après 8 ?"), [
        T("Put a finger on the number, then move one step forward.",
          "ضع إصبعك على العدد ثم تحرّك خطوة إلى الأمام.",
          "Pose un doigt sur le nombre, puis avance d'un pas."),
        F("after 3 → 4      after 7 → 8      after 8 → 9"),
    ]),
    EX("3", "42", st("What comes before 4? Before 9? Before 7?", "ماذا يأتي قبل 4؟ وقبل 9؟ وقبل 7؟", "Qu'est-ce qui vient avant 4 ? Avant 9 ? Avant 7 ?"), [
        T("Go back one step.",
          "ارجع خطوة واحدة.",
          "Recule d'un pas."),
        F("before 4 → 3      before 9 → 8      before 7 → 6"),
    ]),
    EX("4", "43", st("There are 6 objects. Add one more. How many now? What comes after 6?", "عندنا 6 أشياء. أضف واحدًا. كم صار؟ وماذا يأتي بعد 6؟", "Il y a 6 objets. Ajoute-en un. Combien maintenant ? Qu'est-ce qui vient après 6 ?"), [
        objects(6, "circle", "#43a047", prefix="a"),
        objects(7, "circle", "#43a047", prefix="b"),
        T("Six and one more is seven. So the number after 6 is 7. The sequence and the quantity agree.",
          "ستة وواحد أكثر تساوي سبعة. إذن العدد بعد 6 هو 7. السلسلة والكمية متفقتان.",
          "Six et un de plus font sept. Le nombre après 6 est donc 7. La suite et la quantité s'accordent."),
        F("6 + 1 = 7"),
    ]),
    EX("5", "43", st("Find the missing numbers: 4 _ 6, then _ 8 9, then 2 3 _.", "أوجد الأعداد الناقصة: 4 _ 6، ثم _ 8 9، ثم 2 3 _.", "Trouve les nombres manquants : 4 _ 6, puis _ 8 9, puis 2 3 _."), [
        numpath(["4", "?", "6"]),
        numpath(["?", "8", "9"]),
        numpath(["2", "3", "?"]),
        T("Each time use before and after together as a check.",
          "في كل مرة نستعمل قبل وبعد معًا للتحقق.",
          "Chaque fois, on utilise avant et après ensemble pour vérifier."),
        F("5      7      4"),
    ]),
    EX("6", "43", st("Error detective: the order shown is 1 2 4 3 5.", "المحقق: الترتيب المعروض 1 2 4 3 5.", "Détective : l'ordre montré est 1 2 4 3 5."), [
        numpath(list("12435")),
        T("Two cards are in the wrong place: 3 and 4 are reversed. Fix them.",
          "بطاقتان في غير مكانهما: 3 و4 معكوستان. نصحّحهما.",
          "Deux cartes sont mal placées : 3 et 4 sont inversées. On les corrige."),
        numpath(list("12345")),
    ]),
    EX("7", "43", st("Challenge: I hide a number. The number before it is 6 and the number after it is 8. What is it?", "تحدٍّ: أخفيت عددًا. العدد الذي قبله 6 والعدد الذي بعده 8. ما هو؟", "Défi : je cache un nombre. Celui d'avant est 6 et celui d'après est 8. Quel est-il ?"), [
        numpath(["6", "?", "8"]),
        T("Say the sequence: six, ..., eight. The hidden number is between them.",
          "قل السلسلة: ستة، ...، ثمانية. العدد المخفي بينهما.",
          "Dis la suite : six, ..., huit. Le nombre caché est entre les deux."),
        F("7"),
    ]),
    EX("8", "43", st("Final check: order 4 1 3 2; after 6; before 8; fill 5 _ 7.", "تقييم أخير: رتّب 4 1 3 2؛ بعد 6؛ قبل 8؛ املأ 5 _ 7.", "Évaluation : range 4 1 3 2 ; après 6 ; avant 8 ; complète 5 _ 7."), [
        numpath(list("4132")),
        numpath(list("1234")),
        F("after 6 → 7      before 8 → 7      5 _ 7 → 6"),
        T("Seven comes after 6 because it is the next counting number, and it means one more object.",
          "يأتي 7 بعد 6 لأنه العدد التالي في العدّ، ويعني شيئًا واحدًا أكثر.",
          "Sept vient après 6 car c'est le nombre suivant dans le comptage, et cela veut dire un objet de plus."),
    ]),
]
