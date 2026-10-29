"""Grade 2 Mathematics — The sign ×."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G02-MATH-EN-035"
GRADE = 2
SUBJECT = "math"
TITLES = {"en": "The sign “×”", "ar": "إشارة الضرب «×»", "fr": "Le signe « × »"}


def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}


QUIZ = [
    {"q": "5 + 5 + 5 written with ×:", "opts": ["5 × 3", "3 × 5", "5 × 5", "5 + 3"], "a": 0,
     "why": {"3 × 5": _w("In our lesson the first number is what repeats: 5 repeated 3 times is 5 × 3.", "في درسنا العدد الأول هو المتكرر: 5 مكررة 3 مرات هي 5 × 3.", "Dans notre leçon, le premier nombre est celui qui se répète : 5 × 3."),
             "5 × 5": _w("5 appears 3 times, not 5 times.", "العدد 5 ظهر 3 مرات لا 5.", "5 apparaît 3 fois."),
             "5 + 3": _w("That is an addition, not a repeated addition.", "هذا جمع وليس جمعًا متكررًا.", "C'est une addition simple.")},
     "ok": "5 + 5 + 5 = 5 × 3 = 15"},
    {"q": "4 × 9 means:", "opts": ["4 repeated 9 times = 36", "4 + 9 = 13", "9 repeated 4 times = 13", "4 − 9"], "a": 0,
     "why": {"4 + 9 = 13": _w("× is not +. 4 × 9 means 4 nine times.", "× ليست +. 4 × 9 تعني 4 تسع مرات.", "× n'est pas +."),
             "9 repeated 4 times = 13": _w("9 + 9 + 9 + 9 = 36, not 13.", "9 + 9 + 9 + 9 = 36 لا 13.", "9 + 9 + 9 + 9 = 36."),
             "4 − 9": _w("That is a subtraction.", "هذا طرح.", "C'est une soustraction.")},
     "ok": "4 × 9 = 36"},
    {"q": "Which can we write as a multiplication?", "opts": ["6 + 6 + 6 + 6", "6 + 5 + 4 + 3", "7 + 2 + 7 + 2", "1 + 9 + 4 + 6"], "a": 0,
     "why": {"6 + 5 + 4 + 3": _w("The groups are not equal.", "المجموعات غير متساوية.", "Les groupes ne sont pas égaux."),
             "7 + 2 + 7 + 2": _w("The numbers are not all the same.", "الأعداد ليست كلها متماثلة.", "Les nombres ne sont pas tous égaux."),
             "1 + 9 + 4 + 6": _w("The groups are not equal.", "المجموعات غير متساوية.", "Groupes inégaux.")},
     "ok": "6 + 6 + 6 + 6 = 6 × 4"},
]

THEORY = [
    ("A shortcut for equal groups", "اختصار للمجموعات المتساوية", "Un raccourci pour des groupes égaux", "74", [
        T("Hello! Look at 4 + 4 + 4 + 4 + 4. It is long! We have a new sign that makes it short: ×. We write 4 + 4 + 4 + 4 + 4 = 4 × 5. There are 4 objects in each group, and 5 equal groups.",
          "مرحبًا! انظر إلى 4 + 4 + 4 + 4 + 4. إنها طويلة! عندنا إشارة جديدة تختصرها: ×. نكتب 4 + 4 + 4 + 4 + 4 = 4 × 5. في كل مجموعة 4 أشياء وعدد المجموعات المتساوية 5.",
          "4 + 4 + 4 + 4 + 4 = 4 × 5 : 4 objets dans chaque groupe, 5 groupes égaux."),
        F("4 + 4 + 4 + 4 + 4 = 4 × 5"),
        T("In this lesson: the first number is how many in each group. The second number is how many equal groups.",
          "في هذا الدرس: العدد الأول هو عدد الأشياء في كل مجموعة، والعدد الثاني هو عدد المجموعات المتساوية.",
          "Premier nombre : objets par groupe. Second nombre : nombre de groupes."),
    ]),
    ("Equal groups first", "المجموعات المتساوية أولًا", "D'abord des groupes égaux", "74", [
        T("Before we write ×, count each group and check they are equal. Three bags of 5 marbles: 5 + 5 + 5 = 5 × 3 = 15. If the groups are not equal, we cannot use ×.",
          "قبل أن نكتب × نعدّ كل مجموعة ونتأكد أنها متساوية. ثلاثة أكياس في كل منها 5 بلورات: 5 + 5 + 5 = 5 × 3 = 15. وإن لم تكن المجموعات متساوية فلا نستعمل ×.",
          "On compte chaque groupe et on vérifie qu'ils sont égaux : 5 + 5 + 5 = 5 × 3 = 15."),
        F("5 + 5 + 5 = 5 × 3 = 15"),
    ]),
    ("From a picture to ×", "من الصورة إلى ×", "De l'image à ×", "75", [
        T("Look at a picture and say: how many in each group, how many groups. Erasers: 5 equal groups of 6 erasers, so 6 × 5 = 30. Cans: 9 groups of 4 cans, so 4 × 9 = 36.",
          "انظر إلى الصورة وقل: كم في كل مجموعة وكم مجموعة. الممحاة: 5 مجموعات متساوية في كل منها 6 ممحاوات إذن 6 × 5 = 30. العلب: 9 مجموعات في كل منها 4 علب إذن 4 × 9 = 36.",
          "Gommes : 5 groupes de 6 → 6 × 5 = 30. Boîtes : 9 groupes de 4 → 4 × 9 = 36."),
        F("6 × 5 = 30      4 × 9 = 36"),
    ]),
    ("Matching the two writings", "نطابق الكتابتين", "Associer les deux écritures", "75", [
        T("The number of times the added number repeats is the second number. 7 + 7 + 7 + 7 + 7 + 7 has 7 repeated 6 times, so it is 7 × 6. And 3 + 3 + 3 + 3 + 3 + 3 + 3 is 3 × 7.",
          "عدد المرات التي يتكرر فيها العدد المجموع هو العدد الثاني. في 7 + 7 + 7 + 7 + 7 + 7 يتكرر 7 ست مرات فهي 7 × 6. و3 + 3 + 3 + 3 + 3 + 3 + 3 هي 3 × 7.",
          "Le nombre de répétitions est le second facteur : 7 six fois = 7 × 6."),
        F("7+7+7+7+7+7 = 7 × 6      3+3+3+3+3+3+3 = 3 × 7"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Bravo! The sign × is a shortcut for repeated addition of equal groups. Count each group, check they are equal, write the repeated addition, rewrite it with ×, and check the total.",
          "أحسنت! إشارة × اختصار للجمع المتكرر لمجموعات متساوية. نعدّ كل مجموعة ونتأكد من تساويها ونكتب الجمع المتكرر ثم نكتبه بـ × ونتحقق من المجموع.",
          "× est un raccourci pour l'addition répétée de groupes égaux."),
        F("equal groups → repeated addition → × → total"),
    ]),
]

EXERCISES = [
    EX("1", "74", st("Write the number of objects using +: ladybugs (4 groups of 3), butterflies (4 groups of 4), sunflowers (3 groups of 5).", "اكتب عدد الأشياء بالجمع: الدعسوقات (4 مجموعات من 3)، الفراشات (4 مجموعات من 4)، عبّاد الشمس (3 مجموعات من 5).", "Écris avec + : coccinelles (4 groupes de 3), papillons (4 groupes de 4), tournesols (3 groupes de 5)."), [
        F("3 + 3 + 3 + 3 = 12"),
        F("4 + 4 + 4 + 4 = 16"),
        F("5 + 5 + 5 = 15"),
    ]),
    EX("2", "74", st("Write with + and ×: bottles (3 groups of 4), stars (4 groups of 5), bead chains (4 groups of 5), bouquets (3 groups of 6).", "اكتب بالجمع و×: القوارير (3 مجموعات من 4)، النجوم (4 مجموعات من 5)، عقود الخرز (4 مجموعات من 5)، باقات الزهور (3 مجموعات من 6).", "Écris avec + et × : bouteilles (3 de 4), étoiles (4 de 5), colliers (4 de 5), bouquets (3 de 6)."), [
        F("4 + 4 + 4 = 4 × 3 = 12"),
        F("5 + 5 + 5 + 5 = 5 × 4 = 20"),
        F("6 + 6 + 6 = 6 × 3 = 18"),
    ]),
    EX("3", "75", st("Write with ×: erasers (5 groups of 6), lollipops (4 groups of 5), cans (9 groups of 4), packets (7 groups of 6).", "اكتب بـ ×: الممحاة (5 مجموعات من 6)، المصّاصات (4 مجموعات من 5)، العلب (9 مجموعات من 4)، العبوات (7 مجموعات من 6).", "Écris avec × : gommes (5 de 6), sucettes (4 de 5), boîtes (9 de 4), paquets (7 de 6)."), [
        F("6 × 5 = 30      5 × 4 = 20"),
        F("4 × 9 = 36      6 × 7 = 42"),
        T("Check 6 × 7: 6, 12, 18, 24, 30, 36, 42.", "تحقق من 6 × 7: 6 و12 و18 و24 و30 و36 و42.", "Vérifie 6 × 7 : 6, 12, 18, 24, 30, 36, 42."),
    ]),
    EX("4", "75", st("Match: 7+7+7+7+7+7, 5+5+5, 3+3+3+3+3+3+3, 6+6+6+6+6 with 7×6, 5×3, 3×7, 6×5.", "طابق: 7+7+7+7+7+7 و5+5+5 و3+3+3+3+3+3+3 و6+6+6+6+6 مع 7×6 و5×3 و3×7 و6×5.", "Associe les additions aux multiplications."), [
        F("7+7+7+7+7+7 ↔ 7 × 6"),
        F("5+5+5 ↔ 5 × 3"),
        F("3+3+3+3+3+3+3 ↔ 3 × 7"),
        F("6+6+6+6+6 ↔ 6 × 5"),
    ]),
    EX("5", "75", st("Complete the equalities: 5×4, 8×3, 9×6, 4×2.", "أكمل المساويات: 5×4 و8×3 و9×6 و4×2.", "Complète : 5×4, 8×3, 9×6, 4×2."), [
        F("5 × 4 = 5 + 5 + 5 + 5"),
        F("8 × 3 = 8 + 8 + 8"),
        F("9 × 6 = 9 + 9 + 9 + 9 + 9 + 9"),
        F("4 × 2 = 4 + 4"),
    ]),
    EX("6", "", st("(our own) Three bags, 5 marbles in each. Write the repeated addition and the multiplication, and find the total.", "(من عندنا) ثلاثة أكياس في كل منها 5 بلورات. اكتب الجمع المتكرر والضرب وجد المجموع.", "(à nous) Trois sacs de 5 billes : écris l'addition répétée, la multiplication et le total."), [
        F("5 + 5 + 5 = 5 × 3 = 15"),
        T("There are 15 marbles.", "عدد البلورات 15.", "Il y a 15 billes."),
    ]),
]
