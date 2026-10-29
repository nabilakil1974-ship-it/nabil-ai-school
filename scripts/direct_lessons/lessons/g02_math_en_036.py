"""Grade 2 Mathematics — Product."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G02-MATH-EN-036"
GRADE = 2
SUBJECT = "math"
TITLES = {"en": "Product", "ar": "الجداء (ناتج الضرب)", "fr": "Le produit"}


def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}


QUIZ = [
    {"q": "3 × 8 = ?", "opts": ["24", "11", "38", "21"], "a": 0,
     "why": {"11": _w("That is 3 + 8. 3 × 8 is 3 repeated 8 times.", "هذا 3 + 8. أما 3 × 8 فهي 3 مكررة 8 مرات.", "C'est 3 + 8."),
             "38": _w("Do not put the digits side by side.", "لا نضع الرقمين بجانب بعضهما.", "On ne juxtapose pas les chiffres."),
             "21": _w("Count again: 3, 6, 9, 12, 15, 18, 21, 24.", "عُدّ ثانية: 3 و6 و9 و12 و15 و18 و21 و24.", "Recompte : ..., 21, 24.")},
     "ok": "3 × 8 = 24"},
    {"q": "A picture shows 5 columns with 3 soldiers in each. How many soldiers?", "opts": ["15", "8", "35", "53"], "a": 0,
     "why": {"8": _w("That is 5 + 3. We have equal groups, so we multiply.", "هذا 5 + 3. المجموعات متساوية فنضرب.", "C'est 5 + 3 ; on multiplie."),
             "35": _w("Not a number made by writing 3 and 5 together.", "ليس بكتابة 3 و5 معًا.", "On ne juxtapose pas."),
             "53": _w("Not a number made by writing 5 and 3 together.", "ليس بكتابة 5 و3 معًا.", "On ne juxtapose pas.")},
     "ok": "3 × 5 = 15"},
    {"q": "The product is …", "opts": ["the result of a multiplication", "the × sign", "the first number", "the number of groups"], "a": 0,
     "why": {"the × sign": _w("× is the sign; the product is the result.", "× هي الإشارة والجداء هو الناتج.", "× est le signe."),
             "the first number": _w("The numbers we multiply are called factors.", "الأعداد التي نضربها تسمى عوامل.", "Ce sont les facteurs."),
             "the number of groups": _w("That is one of the factors.", "هذا أحد العاملين.", "C'est un facteur.")},
     "ok": "The product is the total."},
]

THEORY = [
    ("The product is the total", "الجداء هو المجموع الكلي", "Le produit est le total", "76", [
        T("Hello! We know the sign ×. Today we find the product. Look: 3 + 3 + 3 + 3 + 3 + 3 + 3 + 3 = 3 × 8 = 24. The product is the result of the multiplication.",
          "مرحبًا! نعرف إشارة ×. اليوم نجد الجداء. انظر: 3 + 3 + 3 + 3 + 3 + 3 + 3 + 3 = 3 × 8 = 24. الجداء هو ناتج عملية الضرب.",
          "Le produit est le résultat de la multiplication : 3 × 8 = 24."),
        F("3 × 8 = 24"),
        T("Whether we use repeated addition or ×, the total is the same.", "سواء استعملنا الجمع المتكرر أو × يبقى المجموع نفسه.", "Addition répétée ou ×, le total est le même."),
    ]),
    ("Pictures and equal groups", "الصور والمجموعات المتساوية", "Images et groupes égaux", "76", [
        T("Red flowers: 4 groups of 3, so 3 × 4 = 12. Planes: 5 groups of 2, so 2 × 5 = 10. Two bouquets of 6: 6 × 2 = 12. Three bouquets of 5: 5 × 3 = 15.",
          "الزهور الحمراء: 4 مجموعات من 3 إذن 3 × 4 = 12. الطائرات: 5 مجموعات من 2 إذن 2 × 5 = 10. باقتان من 6: 6 × 2 = 12. ثلاث باقات من 5: 5 × 3 = 15.",
          "Fleurs : 3 × 4 = 12 ; avions : 2 × 5 = 10 ; 6 × 2 = 12 ; 5 × 3 = 15."),
        F("3 × 4 = 12   2 × 5 = 10   6 × 2 = 12   5 × 3 = 15"),
    ]),
    ("Rows and columns", "الصفوف والأعمدة", "Lignes et colonnes", "76", [
        T("Soldiers stand in a formation. 5 columns with 3 soldiers each: 3 × 5 = 15. 2 rows of 6: 6 × 2 = 12. Squares in an array work the same way: 7 columns of 2 give 2 × 7 = 14, and 6 columns of 4 give 4 × 6 = 24. We never guess: we count the groups.",
          "يقف الجنود في تشكيل. 5 أعمدة في كل منها 3 جنود: 3 × 5 = 15. صفّان من 6: 6 × 2 = 12. والمربعات في الشبكة بالطريقة نفسها: 7 أعمدة من 2 تعطي 2 × 7 = 14 و6 أعمدة من 4 تعطي 4 × 6 = 24. لا نخمّن بل نعدّ المجموعات.",
          "5 colonnes de 3 : 3 × 5 = 15 ; 2 lignes de 6 : 6 × 2 = 12 ; 2 × 7 = 14 ; 4 × 6 = 24."),
        F("3 × 5 = 15   6 × 2 = 12   2 × 7 = 14   4 × 6 = 24"),
    ]),
    ("Draw a model", "نرسم نموذجًا", "On dessine un modèle", "77", [
        T("To find 3 × 4, draw 4 equal groups of 3 circles and count them: 12. To find 5 × 2, draw 2 groups of 5 circles: 10. A box of chocolates with 5 equal groups of 4 has 4 × 5 = 20 chocolates.",
          "لنجد 3 × 4 نرسم 4 مجموعات متساوية في كل منها 3 دوائر ونعدّها: 12. ولنجد 5 × 2 نرسم مجموعتين من 5 دوائر: 10. وعلبة شوكولاتة فيها 5 مجموعات متساوية من 4 فيها 4 × 5 = 20 قطعة.",
          "3 × 4 : 4 groupes de 3 ronds = 12. 5 × 2 = 10. La boîte : 4 × 5 = 20."),
        F("3 × 4 = 12   5 × 2 = 10   4 × 5 = 20"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Great! The product is the total after multiplying. We see equal groups, write ×, calculate the total, and check by counting. Different arrangements can have the same product: 2 × 6 = 12 and 4 × 3 = 12.",
          "أحسنت! الجداء هو المجموع بعد الضرب. نرى مجموعات متساوية ونكتب × ونحسب المجموع ونتحقق بالعدّ. ترتيبات مختلفة قد يكون لها الجداء نفسه: 2 × 6 = 12 و4 × 3 = 12.",
          "Le produit est le total. 2 × 6 = 12 et 4 × 3 = 12."),
        F("group size × number of groups = product"),
    ]),
]

EXERCISES = [
    EX("1", "76", st("Calculate: red flowers (4 groups of 3), airplanes (5 groups of 2), purple bouquets (2 of 6), yellow bouquets (3 of 5).", "احسب: الزهور الحمراء (4 مجموعات من 3)، الطائرات (5 من 2)، الباقات البنفسجية (2 من 6)، الباقات الصفراء (3 من 5).", "Calcule : fleurs rouges, avions, bouquets violets, bouquets jaunes."), [
        F("3 + 3 + 3 + 3 = 3 × 4 = 12"),
        F("2 + 2 + 2 + 2 + 2 = 2 × 5 = 10"),
        F("6 + 6 = 6 × 2 = 12"),
        F("5 + 5 + 5 = 5 × 3 = 15"),
    ]),
    EX("2", "76", st("How many soldiers? Left: 5 columns of 3. Right: 2 rows of 6.", "كم جنديًا؟ على اليسار: 5 أعمدة من 3. على اليمين: صفّان من 6.", "Combien de soldats ? À gauche : 5 colonnes de 3. À droite : 2 lignes de 6."), [
        F("3 × 5 = 3 + 3 + 3 + 3 + 3 = 15"),
        F("6 × 2 = 6 + 6 = 12"),
        T("There are 15 soldiers on the left and 12 on the right.", "على اليسار 15 جنديًا وعلى اليمين 12.", "15 soldats à gauche, 12 à droite."),
    ]),
    EX("3", "77", st("Calculate the number of squares: 7 columns of 2; 2 columns of 3; 1 column of 3; 6 columns of 4.", "احسب عدد المربعات: 7 أعمدة من 2؛ عمودان من 3؛ عمود واحد من 3؛ 6 أعمدة من 4.", "Calcule le nombre de carrés : 7 colonnes de 2 ; 2 de 3 ; 1 de 3 ; 6 de 4."), [
        F("2 × 7 = 14      3 × 2 = 6"),
        F("3 × 1 = 3       4 × 6 = 24"),
    ]),
    EX("4", "77", st("Draw circles to calculate 3 × 4 and 5 × 2.", "ارسم دوائر لتحسب 3 × 4 و5 × 2.", "Dessine des ronds pour calculer 3 × 4 et 5 × 2."), [
        T("For 3 × 4 draw 4 groups of 3 circles: we count 12. For 5 × 2 draw 2 groups of 5 circles: we count 10.",
          "لـ 3 × 4 نرسم 4 مجموعات من 3 دوائر ونعدّ 12. ولـ 5 × 2 نرسم مجموعتين من 5 دوائر ونعدّ 10.",
          "3 × 4 : 4 groupes de 3 = 12. 5 × 2 : 2 groupes de 5 = 10."),
        F("3 × 4 = 12      5 × 2 = 10"),
    ]),
    EX("5", "77", st("A chocolate box has 20 chocolates in an equal pattern (4 in each of 5 columns). Colour 15 squares as 5 × 3 and 24 squares as 4 × 6.", "في علبة شوكولاتة 20 قطعة بنمط متساوٍ (4 في كل من 5 أعمدة). لوّن 15 مربعًا على شكل 5 × 3 و24 مربعًا على شكل 4 × 6.", "Une boîte de 20 chocolats (5 colonnes de 4). Colorie 15 carrés (5 × 3) et 24 carrés (4 × 6)."), [
        F("4 × 5 = 20"),
        T("Colour 3 equal groups of 5 squares: 5 × 3 = 15. Colour 6 equal groups of 4 squares: 4 × 6 = 24. Count the coloured squares to check.",
          "لوّن 3 مجموعات متساوية من 5 مربعات: 5 × 3 = 15. ولوّن 6 مجموعات متساوية من 4 مربعات: 4 × 6 = 24. عُدّ المربعات الملونة للتحقق.",
          "3 groupes de 5 : 15 carrés ; 6 groupes de 4 : 24 carrés. Compte pour vérifier."),
        F("5 × 3 = 15      4 × 6 = 24"),
    ]),
    EX("6", "", st("(our own) A shelf has 7 boxes with 3 toys in each. How many toys?", "(من عندنا) على الرف 7 صناديق في كل منها 3 ألعاب. كم لعبة؟", "(à nous) Une étagère a 7 boîtes de 3 jouets. Combien de jouets ?"), [
        F("3 × 7 = 21"),
        F("check: 3 + 3 + 3 + 3 + 3 + 3 + 3 = 21"),
        T("There are 21 toys.", "عدد الألعاب 21.", "Il y a 21 jouets."),
    ]),
]
