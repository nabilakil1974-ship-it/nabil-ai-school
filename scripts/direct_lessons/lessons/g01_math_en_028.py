"""Grade 1 Mathematics — Order of numbers up to 19."""
from scripts.direct_lessons.common import T, F, EX, st, numpath, tens

LESSON_ID = "G01-MATH-EN-028"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Order of numbers up to 19", "ar": "ترتيب الأعداد حتى 19", "fr": "L'ordre des nombres jusqu'à 19"}
P = [str(i) for i in range(10, 20)]


def path(lo, hi, hi_i=None, blank=()):
    seq = [("?" if i in blank else str(i)) for i in range(lo, hi + 1)]
    return numpath(seq, hi=hi_i, size=56)


THEORY = [
    ("The counting order is stable", "ترتيب العدّ ثابت", "L'ordre du comptage est stable", "76", [
        T("Hello! Today the numbers are all there, but some are out of place. We will put each number back in its true place on the number path up to 19. We do not order them by the shape of their digits; we use the counting order.",
          "مرحبًا! اليوم الأعداد كلها موجودة لكن بعضها خارج مكانه. سنعيد كل عدد إلى مكانه الصحيح على مسار الأعداد حتى 19. لا نرتّبها من شكل أرقامها بل نستعمل ترتيب العدّ.",
          "Bonjour ! Aujourd'hui tous les nombres sont là, mais certains sont mal placés. On remet chaque nombre à sa vraie place sur la droite jusqu'à 19. On ne les range pas d'après la forme des chiffres, mais d'après l'ordre du comptage."),
        numpath(["15", "13", "14", "16"]),
        T("Count with me from thirteen: thirteen, fourteen, fifteen, sixteen. Every number has a fixed place. If we mix up the cards, the true order does not change.",
          "عدّ معي من ثلاثة عشر: ثلاثة عشر، أربعة عشر، خمسة عشر، ستة عشر. لكل عدد مكان ثابت. وإذا خلطنا البطاقات فالترتيب الحقيقي لا يتغير.",
          "Compte avec moi depuis treize : treize, quatorze, quinze, seize. Chaque nombre a une place fixe. Si on mélange les cartes, l'ordre réel ne change pas."),
        path(13, 16),
    ]),
    ("Next number: one step forward", "العدد التالي: خطوة إلى الأمام", "Le nombre suivant : un pas en avant", "76", [
        path(10, 19, 4),
        T("If I stand on 14 and move one step forward, where do I arrive? At 15. The next number means one more. From 18, one step forward leads to 19.",
          "إذا وقفت على 14 وتحركت خطوة إلى الأمام فأين أصل؟ إلى 15. العدد التالي يعني واحدًا أكثر. ومن 18 خطوة إلى الأمام تصل إلى 19.",
          "Si je suis sur 14 et que j'avance d'un pas, où j'arrive ? À 15. Le nombre suivant veut dire un de plus. Depuis 18, un pas en avant mène à 19."),
    ]),
    ("Previous number: one step backward", "العدد السابق: خطوة إلى الخلف", "Le nombre précédent : un pas en arrière", "77", [
        path(10, 19, 7),
        T("Now the other way. If I am on 17 and go one step backward, I reach 16. The previous number means one less. Before 13 comes 12.",
          "الآن بالعكس. إذا كنت على 17 ورجعت خطوة إلى الخلف أصل إلى 16. العدد السابق يعني واحدًا أقل. وقبل 13 يأتي 12.",
          "Maintenant dans l'autre sens. Sur 17, un pas en arrière mène à 16. Le nombre précédent veut dire un de moins. Avant 13 vient 12."),
        path(16, 18, 1, blank=(16, 18)),
        T("The number in the middle has a neighbor before it and a neighbor after it.",
          "العدد الذي في الوسط له جار قبله وجار بعده.",
          "Le nombre du milieu a un voisin avant et un voisin après."),
    ]),
    ("Fill gaps by walking the path", "نملأ الفراغات بالمشي على المسار", "Combler les trous en suivant la droite", "77", [
        path(14, 18, blank=(15, 17)),
        T("We do not fill gaps by guessing; we walk. After 14 comes 15. After 16 comes 17. So the line is 14, 15, 16, 17, 18.",
          "لا نملأ الفراغات بالتخمين بل بالمشي. بعد 14 يأتي 15. وبعد 16 يأتي 17. إذن السطر 14، 15، 16، 17، 18.",
          "On ne comble pas les trous en devinant : on avance. Après 14 vient 15. Après 16 vient 17. La ligne est donc 14, 15, 16, 17, 18."),
        path(14, 18),
    ]),
    ("Use quantity as evidence", "نستعمل الكمية دليلًا", "Utiliser la quantité comme preuve", "77", [
        tens(1, 5), tens(1, 6),
        T("If I forget which comes first, 15 or 16, I can build the quantities. 16 has one more than 15, so 16 comes after it. The number path and the quantity confirm each other.",
          "إذا نسيت أيهما أولًا، 15 أم 16، أستطيع بناء الكميتين. 16 فيها واحد أكثر من 15، لذلك تأتي بعدها. مسار الأعداد والكمية يؤكدان بعضهما.",
          "Si j'oublie lequel vient d'abord, 15 ou 16, je peux construire les quantités. 16 a un de plus que 15, donc elle vient après. La droite et la quantité se confirment."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("The numbers have a fixed order up to 19. One step forward is the next number, one more. One step backward is the previous number, one less.",
          "للأعداد ترتيب ثابت حتى 19. خطوة إلى الأمام هي العدد التالي، واحد أكثر. وخطوة إلى الخلف هي العدد السابق، واحد أقل.",
          "Les nombres ont un ordre fixe jusqu'à 19. Un pas en avant : le nombre suivant, un de plus. Un pas en arrière : le nombre précédent, un de moins."),
        F("FIND THE NUMBER → SEE THE DIRECTION → MOVE ONE STEP → PLACE THE NUMBER → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "76", st("Order the cards from first to last: 18, 16, 19, 17.", "رتّب البطاقات من الأول إلى الأخير: 18، 16، 19، 17.", "Range les cartes du premier au dernier : 18, 16, 19, 17."), [
        numpath(["18", "16", "19", "17"]),
        T("Who comes first when we count from 16? Say it aloud: sixteen, seventeen, eighteen, nineteen.",
          "من يأتي أولًا عندما نعدّ من 16؟ قلها بصوتك: ستة عشر، سبعة عشر، ثمانية عشر، تسعة عشر.",
          "Qui vient d'abord quand on compte depuis 16 ? Dis-le : seize, dix-sept, dix-huit, dix-neuf."),
        path(16, 19),
    ]),
    EX("2", "76", st("What comes after 11? After 15? After 18?", "ماذا يأتي بعد 11؟ وبعد 15؟ وبعد 18؟", "Qu'est-ce qui vient après 11 ? Après 15 ? Après 18 ?"), [
        path(10, 19),
        F("after 11 → 12      after 15 → 16      after 18 → 19"),
    ]),
    EX("3", "77", st("What comes before and after 17? Before and after 12?", "ماذا يأتي قبل 17 وبعدها؟ وقبل 12 وبعدها؟", "Qu'est-ce qui vient avant et après 17 ? Avant et après 12 ?"), [
        path(16, 18, 1),
        path(11, 13, 1),
        F("16 — 17 — 18      11 — 12 — 13"),
    ]),
    EX("4", "77", st("Missing numbers forward and backward: 10 11 _ 13 _ and 19 18 _ 16 _.", "أعداد ناقصة إلى الأمام وإلى الخلف: 10 11 _ 13 _ و19 18 _ 16 _.", "Nombres manquants : 10 11 _ 13 _ et 19 18 _ 16 _."), [
        path(10, 14, blank=(12, 14)),
        numpath(["19", "18", "?", "16", "?"], size=56),
        F("12, 14      17, 15"),
        T("First decide the direction: forward or backward. Then move one step at a time.",
          "حدّد الاتجاه أولًا: إلى الأمام أم إلى الخلف. ثم تحرّك خطوة خطوة.",
          "Décide d'abord du sens : en avant ou en arrière. Puis avance d'un pas à la fois."),
    ]),
    EX("5", "77", st("Put 17 between its neighbors: 16, 17, 18.", "ضع 17 بين جاريها: 16، 17، 18.", "Place 17 entre ses voisins : 16, 17, 18."), [
        path(16, 18, 1),
        T("16 comes before it and 18 comes after it.",
          "16 قبلها و18 بعدها.",
          "16 vient avant et 18 vient après."),
    ]),
    EX("6", "77", st("Error detective: the sequence 14, 15, 17, 16.", "المحقق: التسلسل 14، 15، 17، 16.", "Détective : la suite 14, 15, 17, 16."), [
        numpath(["14", "15", "17", "16"], size=56),
        T("After 15 should come 16, then 17.",
          "بعد 15 يجب أن يأتي 16 ثم 17.",
          "Après 15 doit venir 16, puis 17."),
        path(14, 17),
    ]),
    EX("7", "77", st("Challenge: order 19, 11, 15, 13 even though they are not consecutive.", "تحدٍّ: رتّب 19 و11 و15 و13 مع أنها غير متتالية.", "Défi : range 19, 11, 15, 13 même s'ils ne se suivent pas."), [
        numpath(["19", "11", "15", "13"], size=56),
        T("Imagine each card on the number path. Even with gaps, the place of each number is fixed.",
          "تخيّل كل بطاقة على مسار الأعداد. حتى مع وجود فجوات، مكان كل عدد ثابت.",
          "Imagine chaque carte sur la droite. Même avec des trous, la place de chaque nombre est fixe."),
        F("11 → 13 → 15 → 19"),
    ]),
    EX("8", "77", st("Final check: order 12, 10, 11, 13; before 16; after 16; fill 15 _ 17; fill 19 _ 17; why does 18 come after 17?", "تقييم أخير: رتّب 12 و10 و11 و13؛ قبل 16؛ بعد 16؛ املأ 15 _ 17؛ املأ 19 _ 17؛ لماذا يأتي 18 بعد 17؟", "Évaluation : range 12, 10, 11, 13 ; avant 16 ; après 16 ; complète 15 _ 17 ; complète 19 _ 17 ; pourquoi 18 vient-il après 17 ?"), [
        path(10, 13),
        F("before 16 → 15      after 16 → 17      15 _ 17 → 16      19 _ 17 → 18"),
        T("18 comes after 17 because it is one more: one step forward.",
          "يأتي 18 بعد 17 لأنه واحد أكثر: خطوة إلى الأمام.",
          "18 vient après 17 parce que c'est un de plus : un pas en avant."),
    ]),
]
