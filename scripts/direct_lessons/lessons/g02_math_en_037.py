"""Grade 2 Mathematics — Multiplication: tables of 2 and 10."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G02-MATH-EN-037"
GRADE = 2
SUBJECT = "math"
TITLES = {"en": "Multiplication: tables of 2 and 10", "ar": "الضرب: جدولا 2 و10", "fr": "Multiplication : tables de 2 et de 10"}


def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}


QUIZ = [
    {"q": "2 × 9 = ?", "opts": ["18", "11", "16", "20"], "a": 0,
     "why": {"11": _w("That is 2 + 9. Count by twos nine times.", "هذا 2 + 9. عُدّ بالاثنين تسع مرات.", "C'est 2 + 9."),
             "16": _w("16 is 2 × 8.", "16 هي 2 × 8.", "16 = 2 × 8."),
             "20": _w("20 is 2 × 10.", "20 هي 2 × 10.", "20 = 2 × 10.")},
     "ok": "2, 4, 6, 8, 10, 12, 14, 16, 18"},
    {"q": "10 × 5 = ?", "opts": ["50", "15", "5", "105"], "a": 0,
     "why": {"15": _w("That is 10 + 5. Five groups of ten make 50.", "هذا 10 + 5. خمس عشرات تساوي 50.", "5 dizaines = 50."),
             "5": _w("5 is the number of groups, not the total.", "5 عدد المجموعات لا المجموع.", "5 est le nombre de groupes."),
             "105": _w("Count by tens: 10, 20, 30, 40, 50.", "عُدّ بالعشرات: 10 و20 و30 و40 و50.", "10, 20, 30, 40, 50.")},
     "ok": "10 × 5 = 50"},
    {"q": "Hani bought 8 bags with 10 marbles in each. How many marbles?", "opts": ["80", "18", "8", "108"], "a": 0,
     "why": {"18": _w("That is 10 + 8. We have 8 equal groups of 10.", "هذا 10 + 8. عندنا 8 مجموعات من 10.", "8 groupes de 10."),
             "8": _w("8 is the number of bags.", "8 هو عدد الأكياس.", "8 sacs."),
             "108": _w("Count by tens eight times: 80.", "عُدّ بالعشرات ثماني مرات: 80.", "8 dizaines = 80.")},
     "ok": "10 × 8 = 80"},
]

THEORY = [
    ("The table of 2: counting by twos", "جدول 2: العدّ بالاثنين", "Table de 2 : compter de 2 en 2", "78", [
        T("Hello! We do not memorise without understanding. We build the table of 2 from a pattern. On the number line start at 0 and jump +2 each time: 2, 4, 6, 8, 10, 12, 14, 16, 18, 20. Each jump is one more group of 2.",
          "مرحبًا! لا نحفظ بلا فهم. نبني جدول 2 من نمط. على خط الأعداد نبدأ من 0 ونقفز +2 كل مرة: 2 و4 و6 و8 و10 و12 و14 و16 و18 و20. كل قفزة هي مجموعة إضافية من 2.",
          "On construit la table de 2 avec des sauts de +2 depuis 0 : 2, 4, 6, ..., 20."),
        F("2×1=2  2×2=4  2×3=6  2×4=8  2×5=10"),
        F("2×6=12  2×7=14  2×8=16  2×9=18  2×10=20"),
        T("If you forget a fact, count by 2 from zero.", "إذا نسيت جداء عُدّ بالاثنين من الصفر.", "Si tu oublies, compte de 2 en 2 depuis 0."),
    ]),
    ("Pairs: using the table of 2", "الأزواج: استعمال جدول 2", "Les paires : utiliser la table de 2", "78", [
        T("Sixteen pearls. Put them in pairs: we get 8 groups of 2. So 2 × 8 = 16. Check: 2 + 2 + 2 + 2 + 2 + 2 + 2 + 2 = 16. All of these mean the same number: 2 + 2 + 2 + 2 + 2 + 2, 2 × 6, 12, twelve.",
          "ستة عشر لؤلؤة. نضعها أزواجًا فنحصل على 8 مجموعات من 2. إذن 2 × 8 = 16. تحقق: 2 + 2 + 2 + 2 + 2 + 2 + 2 + 2 = 16. وكل هذه تعني العدد نفسه: 2 + 2 + 2 + 2 + 2 + 2 و2 × 6 و12 و«اثنا عشر».",
          "16 perles en paires : 8 groupes de 2, donc 2 × 8 = 16."),
        F("2 × 8 = 16"),
    ]),
    ("The table of 10: counting by tens", "جدول 10: العدّ بالعشرات", "Table de 10 : compter de 10 en 10", "79", [
        T("Now count by tens: 10, 20, 30, 40, 50, 60, 70, 80, 90, 100. Each jump is one more group of 10.",
          "الآن نعدّ بالعشرات: 10 و20 و30 و40 و50 و60 و70 و80 و90 و100. كل قفزة مجموعة إضافية من 10.",
          "On compte de 10 en 10 : 10, 20, ..., 100."),
        F("10×1=10  10×2=20  10×3=30  10×4=40  10×5=50"),
        F("10×6=60  10×7=70  10×8=80  10×9=90  10×10=100"),
        T("An album with 50 stamps in groups of ten has 5 groups: 10 × 5 = 50. 40 marbles make 4 groups: 10 × 4 = 40.",
          "ألبوم فيه 50 طابعًا بمجموعات من عشرة فيه 5 مجموعات: 10 × 5 = 50. و40 بلورة تعطي 4 مجموعات: 10 × 4 = 40.",
          "50 timbres = 5 dizaines : 10 × 5 ; 40 billes = 10 × 4."),
    ]),
    ("Which multiplication gives this number?", "أي ضرب يعطي هذا العدد؟", "Quelle multiplication donne ce nombre ?", "79", [
        T("Some numbers can be made in more than one way. 20 = 2 × 10 and also 20 = 10 × 2. And 10 = 2 × 5 and also 10 = 10 × 1. Others are simple: 18 = 2 × 9, 12 = 2 × 6, 50 = 10 × 5, 70 = 10 × 7.",
          "بعض الأعداد نحصل عليها بأكثر من طريقة. 20 = 2 × 10 وأيضًا 20 = 10 × 2. و10 = 2 × 5 وأيضًا 10 = 10 × 1. وغيرها بسيط: 18 = 2 × 9 و12 = 2 × 6 و50 = 10 × 5 و70 = 10 × 7.",
          "20 = 2 × 10 = 10 × 2 ; 10 = 2 × 5 = 10 × 1 ; 18 = 2 × 9 ; 50 = 10 × 5."),
        F("20 = 2 × 10 = 10 × 2"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Bravo! The table of 2 is counting by twos. The table of 10 is counting by tens. If you forget a product, go back to the pattern or to equal groups, and check the groups.",
          "أحسنت! جدول 2 هو العدّ بالاثنين وجدول 10 هو العدّ بالعشرات. إذا نسيت ناتجًا فارجع إلى النمط أو إلى المجموعات المتساوية وتحقق من المجموعات.",
          "Table de 2 : de 2 en 2 ; table de 10 : de 10 en 10."),
        F("count by 2 / count by 10 → multiply → check the groups"),
    ]),
]

EXERCISES = [
    EX("1", "78", st("Complete: 2×6, 2×9, 2×5, 2×7, 2×8, 2×4, 2×2.", "أكمل: 2×6 و2×9 و2×5 و2×7 و2×8 و2×4 و2×2.", "Complète : 2×6, 2×9, 2×5, 2×7, 2×8, 2×4, 2×2."), [
        F("12   18   10   14   16   8   4"),
        T("If you forget, count by 2 from zero.", "إذا نسيت عُدّ بالاثنين من الصفر.", "Si tu oublies, compte de 2 en 2."),
    ]),
    EX("2", "78", st("Group the 16 pearls by twos.", "اجمع اللآلئ الـ 16 في أزواج.", "Groupe les 16 perles par deux."), [
        F("2 × 8 = 16"),
        F("check: 2+2+2+2+2+2+2+2 = 16"),
    ]),
    EX("3", "78", st("Complete the table of 2 from 1 to 10.", "أكمل جدول 2 من 1 إلى 10.", "Complète la table de 2 de 1 à 10."), [
        F("2  4  6  8  10  12  14  16  18  20"),
    ]),
    EX("4", "79", st("Count by 10 and complete 10×1 up to 10×10.", "عُدّ بالعشرات وأكمل من 10×1 إلى 10×10.", "Compte de 10 en 10 : de 10×1 à 10×10."), [
        F("10  20  30  40  50  60  70  80  90  100"),
    ]),
    EX("5", "79", st("An album contains 50 stamps; 40 marbles. Group them by 10.", "في ألبوم 50 طابعًا و40 بلورة. اجمعها في عشرات.", "Un album de 50 timbres ; 40 billes. Groupe par 10."), [
        F("10 × 5 = 50 stamps"),
        F("10 × 4 = 40 marbles"),
    ]),
    EX("6", "79", st("How many hands do 8 children have? Hani bought 8 bags of 10 marbles. How many marbles?", "كم يدًا عند 8 أطفال؟ اشترى هاني 8 أكياس في كل منها 10 بلورات. كم بلورة؟", "Combien de mains pour 8 enfants ? Hani achète 8 sacs de 10 billes. Combien de billes ?"), [
        T("Each child has 2 hands: 2 × 8 = 16 hands. 8 bags of 10 marbles: 10 × 8 = 80 marbles.",
          "لكل طفل يدان: 2 × 8 = 16 يدًا. و8 أكياس من 10 بلورات: 10 × 8 = 80 بلورة.",
          "2 × 8 = 16 mains ; 10 × 8 = 80 billes."),
        F("2 × 8 = 16      10 × 8 = 80"),
    ]),
    EX("7", "", st("(our own) 9 pairs of scissors with 2 blades each; 7 packs with 10 cards each.", "(من عندنا) 9 مقصات في كل منها شفرتان؛ 7 رزم في كل منها 10 بطاقات.", "(à nous) 9 ciseaux de 2 lames ; 7 paquets de 10 cartes."), [
        F("2 × 9 = 18 blades"),
        F("10 × 7 = 70 cards"),
    ]),
]
