"""Grade 1 Mathematics — Writing 10."""
from scripts.direct_lessons.common import T, F, EX, st, tens, objects, numeral, scene, numpath

LESSON_ID = "G01-MATH-EN-022"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Writing 10", "ar": "كتابة العدد 10", "fr": "Écrire 10"}


def big(txt, tag="w"):
    return scene(numeral(txt, 330, 290, 220, tag), [tag])


THEORY = [
    ("10 means ten objects", "10 تعني عشرة أشياء", "10 veut dire dix objets", "60", [
        T("Hello! Today we write a new number in its full form. Before writing, I do not want a pencil. Look at ten counters and count them: one to ten. The quantity is ten.",
          "مرحبًا! اليوم نكتب عددًا جديدًا بشكله الكامل. قبل الكتابة لا أريد قلمًا. انظر إلى عشرة عدّادات وعدّها: من واحد إلى عشرة. الكمية عشرة.",
          "Bonjour ! Aujourd'hui on écrit un nouveau nombre en entier. Avant d'écrire, pas de crayon. Regarde dix jetons et compte : de un à dix. La quantité est dix."),
        objects(10, "circle", "#1e63d6", prefix="u", r=24),
        tens(1, 0),
        T("We made one complete ten. The quantity did not change. And this is the writing that records ten:",
          "كوّنا عشرة كاملة. الكمية لم تتغير. وهذه هي الكتابة التي تسجّل العشرة:",
          "On a fait une dizaine complète. La quantité n'a pas changé. Et voici l'écriture qui note dix :"),
        big("10"),
        F("10 objects = one ten = the numeral 10"),
    ]),
    ("10 uses two digits in this order", "10 تستعمل رقمين بهذا الترتيب", "10 utilise deux chiffres dans cet ordre", "60", [
        big("10"),
        T("Look: 10. The first digit is 1, and after it comes 0. The order matters. We read them together as ten. We do not swap their places.",
          "انظر: 10. الرقم الأول 1 وبعده 0. الترتيب مهم. نقرؤهما معًا عشرة. ولا نبدّل مكانيهما.",
          "Regarde : 10. Le premier chiffre est 1, puis vient 0. L'ordre compte. On les lit ensemble : dix. On n'échange pas leurs places."),
    ]),
    ("Trace before writing", "نتتبّع قبل أن نكتب", "Suivre avant d'écrire", "61", [
        scene('<text id="d" x="330" y="290" font-size="220" font-weight="700" text-anchor="middle" fill="none" stroke="#0b3d5c" stroke-width="4" stroke-dasharray="10 8" font-family="sans-serif">10</text>', ["d"]),
        T("Trace the digit 1 first. Now the digit 0. The 1 is first and the 0 is second. It does not have to be a perfect decoration; what matters is that the numeral is readable and correct.",
          "تتبّع الرقم 1 أولًا. الآن الرقم 0. الـ1 أولًا والـ0 ثانيًا. لا يلزم أن تكون الزخرفة مثالية، المهم أن يكون الرقم مقروءًا وصحيحًا.",
          "Suis d'abord le chiffre 1. Maintenant le chiffre 0. Le 1 d'abord, le 0 ensuite. Pas besoin d'une décoration parfaite : le nombre doit être lisible et juste."),
    ]),
    ("Write 10 from a model", "نكتب 10 من نموذج", "Écrire 10 à partir d'un modèle", "61", [
        tens(1, 0),
        T("What quantity is inside the bundle? Ten. Now write it: 10. If you wrote only 1, remember that the numeral ten has two digits. If you wrote 01, ask: which comes first? The 1. And after it? The 0.",
          "ما الكمية داخل الحزمة؟ عشرة. الآن اكتبها: 10. إذا كتبت 1 فقط تذكّر أن عدد العشرة فيه رقمان. وإذا كتبت 01 فاسأل: من الأول؟ الـ1. وبعده؟ الـ0.",
          "Quelle quantité y a-t-il dans le paquet ? Dix. Maintenant écris-la : 10. Si tu as écrit seulement 1, souviens-toi que dix a deux chiffres. Si tu as écrit 01, demande : qui vient d'abord ? Le 1. Et après ? Le 0."),
        big("10"),
    ]),
    ("Write 10 from memory, then verify", "نكتب 10 من الذاكرة ثم نتحقق", "Écrire 10 de mémoire puis vérifier", "61", [
        T("I hide the model. Write ten from memory. We do not say right away if it is correct. Look at ten objects: what numeral should stand for this quantity? 10. Compare it with what you wrote. Checking yourself is excellent.",
          "أخفي النموذج. اكتب عشرة من الذاكرة. لا نقول فورًا إن كانت صحيحة. انظر إلى عشرة أشياء: ما العدد الذي يجب أن يمثّل هذه الكمية؟ 10. قارنه بما كتبته. التحقق الذاتي ممتاز.",
          "Je cache le modèle. Écris dix de mémoire. On ne dit pas tout de suite si c'est juste. Regarde dix objets : quel nombre doit représenter cette quantité ? 10. Compare avec ce que tu as écrit. Se corriger soi-même, c'est excellent."),
        objects(10, "circle", "#43a047", prefix="m", r=24),
        big("10"),
    ]),
    ("Understanding is not the same as handwriting", "الفهم ليس مثل شكل الكتابة", "Comprendre n'est pas écrire joliment", "61", [
        T("If a child makes ten objects correctly but writes a 0 that is not neat, is their idea of 10 wrong? Not necessarily. There is a difference between understanding the quantity and the shape of the handwriting. We fix each one on its own.",
          "إذا صنع طفل عشرة أشياء بشكل صحيح لكن كتب الصفر غير مرتّب، هل فهمه لـ10 خاطئ؟ ليس بالضرورة. هناك فرق بين فهم الكمية وشكل الخط. نصلح كلًّا منهما على حدة.",
          "Si un enfant fait bien dix objets mais écrit un 0 peu soigné, a-t-il mal compris 10 ? Pas forcément. Comprendre la quantité et la forme de l'écriture sont deux choses. On corrige chacune séparément."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("10 is the numeral for ten objects. It has 1 first and then 0. One complete ten is the same quantity.",
          "10 هو الرقم الذي يمثّل عشرة أشياء. فيه 1 أولًا ثم 0. والعشرة الكاملة هي الكمية نفسها.",
          "10 est le nombre qui représente dix objets. Il a 1 d'abord puis 0. Une dizaine complète est la même quantité."),
        F("BUILD TEN → COUNT → LOOK AT 10 → TRACE → WRITE 1 THEN 0 → VERIFY WITH TEN OBJECTS"),
    ]),
]

EXERCISES = [
    EX("1", "60", st("Which collection matches the numeral 10: 9, 10 or 8 objects?", "أي مجموعة تطابق العدد 10: 9 أم 10 أم 8 أشياء؟", "Quelle collection correspond au nombre 10 : 9, 10 ou 8 objets ?"), [
        objects(9, "circle", "#e53935", prefix="a", r=22),
        objects(10, "circle", "#43a047", prefix="b", r=22),
        objects(8, "circle", "#fb8c00", prefix="c", r=22),
        T("Count each collection. Only the one with ten matches 10.",
          "نعدّ كل مجموعة. فقط التي فيها عشرة تطابق 10.",
          "On compte chaque collection. Seule celle qui en a dix correspond à 10."),
    ]),
    EX("2", "60", st("Cards: 10, 01, 1, 0. Which one is ten?", "البطاقات: 10، 01، 1، 0. أيها عشرة؟", "Cartes : 10, 01, 1, 0. Laquelle est dix ?"), [
        numpath(["10", "01", "1", "0"], hi=0, size=44),
        T("It is 10. Why not 01? Because the order of the digits is wrong.",
          "إنها 10. لماذا ليست 01؟ لأن ترتيب الرقمين خاطئ.",
          "C'est 10. Pourquoi pas 01 ? Parce que l'ordre des chiffres est faux."),
    ]),
    EX("3", "61", st("Trace 10 several times.", "تتبّع 10 عدة مرات.", "Suis 10 plusieurs fois."), [
        scene('<text id="d" x="330" y="290" font-size="220" font-weight="700" text-anchor="middle" fill="none" stroke="#0b3d5c" stroke-width="4" stroke-dasharray="10 8" font-family="sans-serif">10</text>', ["d"]),
        T("Check the digit order, the direction, that it is readable, and that no digit is missing.",
          "نتحقق من ترتيب الرقمين واتجاههما ووضوحهما وألّا ينقص رقم.",
          "Vérifie l'ordre des chiffres, le sens, la lisibilité, et qu'aucun chiffre ne manque."),
    ]),
    EX("4", "61", st("One ten bundle: what is the quantity inside? Write it.", "حزمة عشرة واحدة: ما الكمية داخلها؟ اكتبها.", "Un paquet de dix : quelle quantité à l'intérieur ? Écris-la."), [
        tens(1, 0),
        F("10"),
        T("To check, unbundle and count ten.",
          "للتحقق نفكّ ونعدّ عشرة.",
          "Pour vérifier, on défait et on compte dix."),
    ]),
    EX("5", "61", st("Write 10 from memory, then show ten dots and check that they match.", "اكتب 10 من الذاكرة ثم اعرض عشر نقاط وتحقق من التطابق.", "Écris 10 de mémoire, puis montre dix points et vérifie la correspondance."), [
        big("10"),
        objects(10, "circle", "#1e63d6", prefix="p", r=24),
        T("If it does not match, fix the digit order or direction, while remembering that the quantity is ten.",
          "إذا لم يتطابق نصحّح ترتيب الرقمين أو اتجاههما مع تذكّر أن الكمية عشرة.",
          "Si ça ne correspond pas, corrige l'ordre ou le sens des chiffres, en gardant en tête que la quantité est dix."),
    ]),
    EX("6", "61", st("Error detective: ten objects were drawn, and the child wrote 01.", "المحقق: رُسمت عشرة أشياء وكتب الطفل 01.", "Détective : dix objets sont dessinés et l'enfant a écrit 01."), [
        objects(10, "circle", "#43a047", prefix="e", r=24),
        T("Is the quantity right? Yes. Is the writing right? No. What do we fix? The digit order: 10.",
          "هل الكمية صحيحة؟ نعم. هل الكتابة صحيحة؟ لا. ماذا نصلح؟ ترتيب الرقمين: 10.",
          "La quantité est-elle juste ? Oui. L'écriture est-elle juste ? Non. Que corrige-t-on ? L'ordre des chiffres : 10."),
        big("10"),
    ]),
    EX("7", "61", st("Challenge: A is 10 loose counters, B is one ten bundle, C is the numeral 10. Are they three different quantities?", "تحدٍّ: A عشرة عدّادات منفردة، B حزمة عشرة، C العدد 10. هل هي ثلاث كميات مختلفة؟", "Défi : A est 10 jetons seuls, B un paquet de dix, C le nombre 10. Sont-ce trois quantités différentes ?"), [
        objects(10, "circle", "#1e63d6", prefix="a", r=24),
        tens(1, 0),
        big("10"),
        T("No. All three represent ten.",
          "لا. الثلاثة تمثّل عشرة.",
          "Non. Les trois représentent dix."),
    ]),
    EX("8", "61", st("Final check: why does 10 represent ten objects?", "تقييم أخير: لماذا يمثّل 10 عشرة أشياء؟", "Évaluation : pourquoi 10 représente-t-il dix objets ?"), [
        tens(1, 0),
        T("Because one complete ten holds exactly ten ones, and the numeral 10 records that quantity: 1 first, then 0.",
          "لأن العشرة الكاملة فيها عشرة آحاد بالضبط، والعدد 10 يسجّل هذه الكمية: 1 أولًا ثم 0.",
          "Parce qu'une dizaine complète contient exactement dix unités, et le nombre 10 note cette quantité : 1 d'abord, puis 0."),
        F("ten objects ↔ one ten ↔ 10"),
    ]),
]
