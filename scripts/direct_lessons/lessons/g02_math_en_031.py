"""Grade 2 Mathematics — Numbers up to 199."""
from scripts.direct_lessons.common import T, F, EX, st, scene

LESSON_ID = "G02-MATH-EN-031"
GRADE = 2
SUBJECT = "math"
TITLES = {"en": "Numbers up to 199", "ar": "الأعداد حتى 199", "fr": "Les nombres jusqu'à 199"}


def blocks(t, o, tag="B"):
    """1 hundred square + t tens rods + o ones cubes."""
    svg = f'<g id="{tag}h"><rect x="30" y="60" width="150" height="150" fill="#bbdefb" stroke="#0b3d5c" stroke-width="4"/><text x="105" y="145" font-size="46" font-weight="700" text-anchor="middle" fill="#0b3d5c" font-family="sans-serif">100</text></g>'
    ids = [tag + "h"]
    for i in range(t):
        x = 210 + i * 24
        svg += f'<g id="{tag}t{i}"><rect x="{x}" y="60" width="18" height="150" fill="#ffcc80" stroke="#0b3d5c" stroke-width="3"/></g>'
        ids.append(f"{tag}t{i}")
    ox = 210 + t * 24 + 20
    for i in range(o):
        svg += f'<g id="{tag}o{i}"><rect x="{ox + (i%5)*26}" y="{150 + (i//5)*32}" width="20" height="20" fill="#a5d6a7" stroke="#0b3d5c" stroke-width="3"/></g>'
        ids.append(f"{tag}o{i}")
    svg += f'<text id="{tag}n" x="330" y="330" font-size="90" font-weight="700" text-anchor="middle" fill="#e53935" font-family="sans-serif">{100+t*10+o}</text>'
    ids.append(tag + "n")
    return scene(svg, ids)


THEORY = [
    ("Build a number from 1 hundred, tens and ones", "نبني عددًا من مئة وعشرات وآحاد", "Construire un nombre", "66", [
        T("Hello, champion! Now we enter the numbers from 100 to 199. 1 hundred + 5 tens + 7 ones = 157, read one hundred fifty-seven. In this range the hundreds digit is always 1; the tens and ones decide which number it is.",
          "مرحبًا يا بطل! دخلنا الآن الأعداد من 100 إلى 199. مئة + 5 عشرات + 7 آحاد = 157 ونقرأه مئة وسبعة وخمسون. في هذا المدى رقم المئات دائمًا 1، والعشرات والآحاد تحدّدان أيّ عدد هو.",
          "Les nombres de 100 à 199. 1 centaine + 5 dizaines + 7 unités = 157, cent cinquante-sept. Le chiffre des centaines est toujours 1."),
        blocks(5, 7),
        F("1 / 5 / 7  →  157"),
    ]),
    ("Zero keeps the place", "الصفر يحفظ المنزلة", "Le zéro garde la place", "66", [
        T("If a place is empty we write 0. One hundred six is 106, not 16. 1 hundred + 5 ones = 105, and 1 hundred + 9 tens = 190.",
          "إذا خلت منزلة كتبنا 0. مئة وستة تُكتب 106 لا 16. مئة + 5 آحاد = 105 ومئة + 9 عشرات = 190.",
          "Si une place est vide, on écrit 0 : cent six = 106, pas 16."),
        F("106      105      190"),
    ]),
    ("Many ways to write one number", "طرق كثيرة لكتابة عدد واحد", "Plusieurs écritures d'un nombre", "67", [
        T("A number can be shown with blocks, digits, words or expanded form. 169 = one hundred sixty-nine = 100 + 60 + 9 = 1 hundred, 6 tens, 9 ones.",
          "يمكن تمثيل العدد بالمكعبات أو بالأرقام أو بالكلمات أو بالتحليل. 169 = مئة وتسعة وستون = 100 + 60 + 9 = مئة و6 عشرات و9 آحاد.",
          "Un nombre s'écrit avec des blocs, des chiffres, des mots ou une décomposition."),
        blocks(6, 9),
        F("169 = 100 + 60 + 9"),
    ]),
    ("Read a digit by its place", "نقرأ الرقم حسب منزلته", "Lire un chiffre selon sa place", "68", [
        T("In 178 the tens digit is 7 and the ones digit is 8. Do not say 8 is the tens digit. And 100 + 70 + 8 = 178, not 1078.",
          "في 178 رقم العشرات 7 ورقم الآحاد 8. لا نقول إن 8 رقم العشرات. و100 + 70 + 8 = 178 لا 1078.",
          "Dans 178, chiffre des dizaines 7, des unités 8. 100 + 70 + 8 = 178."),
        F("178:  tens 7,  ones 8"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("From 100 to 199 there is always one hundred; tens and ones decide the rest. We can show the same number with blocks, digits, words or expanded form.",
          "من 100 إلى 199 مئة واحدة ثابتة والعشرات والآحاد تحدّد الباقي. نمثّل العدد نفسه بالمكعبات أو الأرقام أو الكلمات أو التحليل.",
          "De 100 à 199 : une centaine fixe ; dizaines et unités décident."),
        F("READ h/t/o → BUILD → SWITCH REPRESENTATIONS → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "66", st("Write the number: one hundred twenty, twenty-four, six, nine, fifty, thirteen.", "اكتب العدد: مئة وعشرون، مئة وأربعة وعشرون، مئة وستة، مئة وتسعة، مئة وخمسون، مئة وثلاثة عشر.", "Écris : cent vingt, cent vingt-quatre, cent six, cent neuf, cent cinquante, cent treize."), [
        F("120   124   106   109   150   113"),
    ]),
    EX("2", "66", st("Digits: 1h2t, 1h5o, 1h8t, 1h8o; 1h2t8o, 1h9t5o, 1h3o, 1h9t.", "بالأرقام: مئة و2 عشرتان … إلخ.", "En chiffres : 1c2d, 1c5u, 1c8d, 1c8u ; 1c2d8u, 1c9d5u, 1c3u, 1c9d."), [
        F("120   105   180   108"),
        F("128   195   103   190"),
    ]),
    EX("3", "67", st("Write in digits: 123, 108, 178, 107, 190, 192, 110, 103 (given in words).", "اكتب بالأرقام (معطاة بالكلمات).", "Écris en chiffres (donnés en lettres)."), [
        F("123   108   178   107   190   192   110   103"),
    ]),
    EX("4", "67", st("Match: one hundred twenty, two, ninety, eighty.", "صِل: مئة وعشرون، مئة واثنان، مئة وتسعون، مئة وثمانون.", "Relie : cent vingt, deux, quatre-vingt-dix, quatre-vingts."), [
        F("120   102   190   180"),
    ]),
    EX("5", "67", st("Complete: 134, 156, 106, 183, 130, 198, 170, 104.", "أكمل التحليل.", "Complète la décomposition."), [
        F("134 = 100 + 30 + 4      156 = 100 + 50 + 6"),
        F("106 = 100 + 6           183 = 100 + 80 + 3"),
        F("130 = 100 + 30          198 = 100 + 90 + 8"),
        F("170 = 100 + 70          104 = 100 + 4"),
        T("A zero place needs no term: 106 = 100 + 6.", "المنزلة الصفرية لا تحتاج حدًّا: 106 = 100 + 6.", "Une place à zéro n'a pas de terme."),
    ]),
    EX("6", "67", st("Complete the sums.", "أكمل المجاميع.", "Complète les sommes."), [
        F("100 + 20 = 120   100 + 6 = 106   100 + 30 = 130"),
        F("100 + 10 + 5 = 115   100 + 30 + 8 = 138   100 + 60 + 5 = 165"),
        F("100 + 3 = 103   100 + 10 = 110   100 + 9 = 109"),
    ]),
    EX("7", "67", st("Color the balls where the tens digit is 7.", "لوّن الكرات التي رقم عشراتها 7.", "Colorie quand le chiffre des dizaines est 7."), [
        F("157 no · 175 YES · 167 no · 178 YES · 107 no · 172 YES · 170 YES"),
        F("175, 178, 172, 170"),
    ]),
    EX("8", "68", st("Circle the tens digit: 125, 106, 100, 170.", "ضع دائرة على رقم العشرات.", "Entoure le chiffre des dizaines."), [
        F("2   0   0   7"),
    ]),
    EX("9", "68", st("Circle the ones digit: 139, 100, 197, 180.", "ضع دائرة على رقم الآحاد.", "Entoure le chiffre des unités."), [
        F("9   0   7   0"),
    ]),
    EX("10", "68", st("Complete with the appropriate number.", "أكمل بالعدد المناسب.", "Complète."), [
        F("100 + 20 = 120   100 + 2 = 102   100 + 25 = 125"),
        F("120 + 8 = 128   190 + 7 = 197   100 + 10 = 110"),
        F("150 + 8 = 158   160 + 4 = 164   180 + 15 = 195"),
    ]),
    EX("11", "68", st("Riddle 1: hundreds 1, tens 8, ones 5.", "لغز 1: مئات 1، عشرات 8، آحاد 5.", "Devinette 1 : c 1, d 8, u 5."), [F("185")]),
    EX("12", "68", st("Riddle 2: ones 5, tens 0, hundreds 1.", "لغز 2: آحاد 5، عشرات 0، مئات 1.", "Devinette 2 : u 5, d 0, c 1."), [F("105")]),
    EX("13", "68", st("Riddle 3: tens 7, ones 3, hundreds 1.", "لغز 3: عشرات 7، آحاد 3، مئات 1.", "Devinette 3 : d 7, u 3, c 1."), [F("173")]),
    EX("14", "68", st("Same number, same color: 100, 105, 169.", "العدد نفسه باللون نفسه: 100 و105 و169.", "Même nombre, même couleur : 100, 105, 169."), [
        F("100:  90 + 10 · 99 + 1 · one hundred · 97 + 3 · 70 + 30"),
        F("105:  1 hundred 5 ones · one hundred five · 100 + 5 · 105"),
        F("169:  169 · one hundred sixty-nine · 100 + 60 + 9 · 1h 6t 9o"),
        T("Value matters, not whether \"100\" appears: 100 + 5 is 105, not 100.", "المهم القيمة لا ظهور «100»: 100 + 5 = 105 لا 100.", "La valeur compte : 100 + 5 = 105."),
    ]),
    EX("15", "69", st("Number the six drawing stages in order.", "رقّم مراحل الرسم الست بالترتيب.", "Numérote les six étapes du dessin."), [
        T("Each stage contains the previous stage plus one new segment. The first stage is the front rectangle only; we order by construction, not by position on the page.",
          "كل مرحلة تحوي السابقة مع جزء جديد. المرحلة الأولى المستطيل الأمامي فقط. نرتّب حسب البناء لا حسب مكان الصورة في الصفحة.",
          "Chaque étape contient la précédente + un nouveau segment. La première : le rectangle de face."),
        F("order on the page: 3 · 1 · 4 / 5 · 6 · 2  →  start with the front rectangle"),
    ]),
    EX("16", "69", st("Maze: help the child find his house.", "المتاهة: ساعد الطفل ليجد بيته.", "Labyrinthe : aide l'enfant à trouver sa maison."), [
        T("Trace a continuous route through the open corridors, never across a wall. If you hit a wall, go back to the last junction and try another branch.",
          "ارسم طريقًا متصلًا عبر الممرات المفتوحة ولا تقطع جدارًا. إذا اصطدمت بجدار فارجع إلى آخر مفترق وجرّب فرعًا آخر.",
          "Trace un chemin continu sans traverser de mur ; au mur, reviens au dernier carrefour."),
    ]),
    EX("17", "", st("Guided practice: build 146.", "تدريب: ابنِ العدد 146.", "Entraînement : construis 146."), [
        blocks(4, 6),
        F("1 hundred + 4 tens + 6 ones = 100 + 40 + 6 = 146      tens 4,  ones 6"),
    ]),
    EX("18", "", st("Transfer: 1 hundred, tens digit 6, ones digit 2. Give two other writings.", "تحدٍّ: مئة، رقم عشراته 6 وآحاده 2. اكتب كتابتين أخريين.", "Défi : une centaine, dizaines 6, unités 2. Deux autres écritures."), [
        F("162 = 100 + 60 + 2 = one hundred sixty-two"),
    ]),
    EX("19", "", st("Error detective: \"190 = 1 hundred + 9 ones\".", "المحقق: «190 = مئة + 9 آحاد».", "Détective : « 190 = 1 centaine + 9 unités »."), [
        F("190 = 1 hundred + 9 tens + 0 ones"),
    ]),
    EX("20", "", st("Final check.", "تقييم أخير.", "Évaluation finale."), [
        F("124 · 195 · 183 · 7 · 7 · 8 · 185 · 105 · 173"),
        T("Zero must stay: 105, not 15. A maze route must never cross a wall.", "يبقى الصفر: 105 لا 15. ولا يقطع طريق المتاهة أي جدار.", "Le zéro reste : 105. Jamais à travers un mur."),
    ]),
]
