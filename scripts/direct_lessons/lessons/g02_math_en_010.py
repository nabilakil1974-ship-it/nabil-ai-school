"""Grade 2 Mathematics — Locating the Squares of a Grid."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G02-MATH-EN-010"
GRADE = 2
SUBJECT = "math"
TITLES = {"en": "Locating the Squares of a Grid", "ar": "تحديد مربعات الشبكة", "fr": "Repérer les cases d'un quadrillage"}


def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}


QUIZ = [
    {"q": "What does the code B2 mean?", "opts": ["Row B, column 2", "Column B, row 2", "Row 2, column B", "Two squares B"], "a": 0,
     "why": {"Column B, row 2": _w("The letter names the row, the number names the column.", "الحرف للصف والرقم للعمود.", "La lettre est la ligne, le nombre la colonne."),
             "Row 2, column B": _w("In our book the letter comes first.", "في كتابنا الحرف أولًا.", "Dans notre livre, la lettre d'abord."),
             "Two squares B": _w("It is one square.", "إنها مربع واحد.", "C'est une seule case.")}, "ok": "row B, column 2"},
    {"q": "A drawing is in row F, column 7. What is its code?", "opts": ["F7", "7F", "F6", "E7"], "a": 0,
     "why": {"7F": _w("Write the letter first, then the number.", "نكتب الحرف ثم الرقم.", "Lettre puis nombre."),
             "F6": _w("The column is 7, not 6.", "العمود 7 لا 6.", "La colonne est 7."),
             "E7": _w("The row is F, not E.", "الصف F لا E.", "La ligne est F.")}, "ok": "F7"},
    {"q": "Colour A2 red. How many squares do you colour?", "opts": ["1", "2", "The whole row A", "The whole column 2"], "a": 0,
     "why": {"2": _w("A2 names one square only.", "A2 تسمّي مربعًا واحدًا فقط.", "A2 est une seule case."),
             "The whole row A": _w("Only the crossing of row A and column 2.", "فقط تقاطع الصف A والعمود 2.", "Seulement le croisement."),
             "The whole column 2": _w("Only one square.", "مربع واحد فقط.", "Une seule case.")}, "ok": "one square"},
]

THEORY = [
    ("Every square has an address", "لكل مربع عنوان", "Chaque case a une adresse", "30", [
        T("Hello, champion! Today we play a locating game on a grid. Every square has an address, but not a street address. It is a row letter plus a column number. The red triangle is in row B and column 2, so its code is B2.",
          "مرحبًا يا بطل! اليوم نلعب لعبة تحديد المواقع على شبكة. لكل مربع عنوان، لكنه ليس عنوان شارع بل حرف الصف مع رقم العمود. المثلث الأحمر في الصف B والعمود 2 إذن رمزه B2.",
          "Bonjour champion ! Aujourd'hui, un jeu de repérage sur un quadrillage. Chaque case a une adresse : une lettre pour la ligne et un nombre pour la colonne. Le triangle rouge est ligne B, colonne 2 : son code est B2."),
        F("B2 = row B, column 2"),
    ]),
    ("Code to square", "من الرمز إلى المربع", "Du code à la case", "30", [
        T("If I say C4, do not search at random. Step 1: find row C. Step 2: find column 4. Step 3: the square where they meet is C4. Row, column, square.",
          "إذا قلت C4 فلا نبحث عشوائيًا. الخطوة 1: نجد الصف C. الخطوة 2: نجد العمود 4. الخطوة 3: المربع الذي يلتقيان فيه هو C4. صف ثم عمود ثم مربع.",
          "Si je dis C4, on ne cherche pas au hasard. 1 : la ligne C. 2 : la colonne 4. 3 : la case où elles se croisent est C4."),
        F("ROW → COLUMN → SQUARE"),
        T("The order matters. In our book we read the letter first, then the number. B2 means row B, column 2. We colour only that one square, never a whole row.",
          "الترتيب مهم. في كتابنا نقرأ الحرف أولًا ثم الرقم. B2 تعني الصف B والعمود 2. نلوّن ذلك المربع وحده، وليس صفًا كاملًا.",
          "L'ordre compte : lettre d'abord, nombre ensuite. B2 : ligne B, colonne 2. On colorie cette seule case, pas toute une ligne."),
    ]),
    ("Square to code", "من المربع إلى الرمز", "De la case au code", "30", [
        T("Now the other way. A drawing is inside the grid and we write its code. Look at the object. Go left to the row letter. Go up to the column number. Write the letter, then the number.",
          "الآن بالعكس. هناك رسم داخل الشبكة ونريد كتابة رمزه. ننظر إلى الشكل، نذهب يسارًا إلى حرف الصف، ثم نصعد إلى رقم العمود، ونكتب الحرف ثم الرقم.",
          "Maintenant l'inverse : un dessin est dans le quadrillage, on écrit son code. On regarde l'objet, on va à gauche vers la lettre de la ligne, en haut vers le numéro de la colonne, et on écrit lettre puis nombre."),
        F("row F, column 7 → F7"),
        F("row D, column 5 → D5"),
    ]),
    ("Both directions", "في الاتجاهين", "Dans les deux sens", "30", [
        T("Locating works in both directions. Code to square: D3 is row D, column 3. Square to code: an object in row C, column 5 has the code C5. If you understand both directions, you understand a grid address.",
          "التحديد يعمل في الاتجاهين. من الرمز إلى المربع: D3 هي الصف D والعمود 3. ومن المربع إلى الرمز: شكل في الصف C والعمود 5 رمزه C5. إذا فهمت الاتجاهين فقد فهمت عنوان الشبكة.",
          "Le repérage marche dans les deux sens. Code vers case : D3 = ligne D, colonne 3. Case vers code : un objet ligne C, colonne 5 a pour code C5."),
        F("D3 → square      row C, column 5 → C5"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Every square has an address: a letter for the row and a number for the column. B2 means row B, column 2. Find the row, find the column, find where they meet, then check.",
          "لكل مربع عنوان: حرف للصف ورقم للعمود. B2 تعني الصف B والعمود 2. نجد الصف ثم العمود ثم نقطة التقائهما ثم نتحقق.",
          "Chaque case a une adresse : lettre = ligne, nombre = colonne. B2 : ligne B, colonne 2. On trouve la ligne, la colonne, leur croisement, puis on vérifie."),
    ]),
]

EXERCISES = [
    EX("1", "30", st("Colour the squares: A2 in red, B4 in blue, D1 in green, E5 in black.",
                    "لوّن المربعات: A2 بالأحمر وB4 بالأزرق وD1 بالأخضر وE5 بالأسود.",
                    "Colorie : A2 en rouge, B4 en bleu, D1 en vert, E5 en noir."), [
        T("For each code: find the row letter, find the column number, colour the crossing square only.",
          "لكل رمز: نجد حرف الصف ثم رقم العمود ثم نلوّن مربع التقاطع فقط.",
          "Pour chaque code : la ligne, la colonne, on colorie seulement la case du croisement."),
        F("A2 red   B4 blue   D1 green   E5 black"),
    ]),
    EX("2", "30", st("Write the code of the square of each drawing: the pepper (row B, column 2), the cherries (row C, column 6), the red fruit (row F, column 7), the orange fruit (row A, column 4), the yellow-green fruit (row F, column 3), the banana (row D, column 5).",
                    "اكتب رمز مربع كل رسم: الفلفل (الصف B والعمود 2) والكرز (الصف C والعمود 6) والثمرة الحمراء (الصف F والعمود 7) والثمرة البرتقالية (الصف A والعمود 4) والثمرة الصفراء الخضراء (الصف F والعمود 3) والموزة (الصف D والعمود 5).",
                    "Écris le code de la case de chaque dessin : poivron (B, 2), cerises (C, 6), fruit rouge (F, 7), fruit orange (A, 4), fruit jaune-vert (F, 3), banane (D, 5)."), [
        F("B2   C6   F7   A4   F3   D5"),
        T("Check: for each object the row and the column must meet in its own square.", "تحقق: صف كل شكل وعموده يلتقيان في مربعه.", "Vérifie : la ligne et la colonne se croisent dans la case de l'objet."),
    ]),
    EX("3", "30", st("Draw: a red triangle in A5, a blue circle in C3, green squares in D2 and E6, banana figures in B4 and A1.",
                    "ارسم: مثلثًا أحمر في A5 ودائرة زرقاء في C3 ومربعين أخضرين في D2 وE6 وموزتين في B4 وA1.",
                    "Dessine : triangle rouge en A5, cercle bleu en C3, carrés verts en D2 et E6, bananes en B4 et A1."), [
        F("red triangle → A5      blue circle → C3"),
        F("green squares → D2 and E6      bananas → B4 and A1"),
        T("Two codes mean two figures: one in each square.", "رمزان يعنيان شكلين: واحد في كل مربع.", "Deux codes, deux figures : une dans chaque case."),
    ]),
    EX("4", "30", st("Our own practice: colour C2 yellow; write the code of an object in row D, column 4; place a blue circle in B5.",
                    "تمرين من عندنا: لوّن C2 بالأصفر؛ اكتب رمز شكل في الصف D والعمود 4؛ ضع دائرة زرقاء في B5.",
                    "Exercice à nous : colorie C2 en jaune ; écris le code d'un objet ligne D, colonne 4 ; place un cercle bleu en B5."), [
        F("C2 yellow      D4      blue circle in B5"),
        T("(our own)", "(من عندنا)", "(exemple à nous)"),
    ]),
    EX("5", "30", st("Our own: a secret route A1, B2, C3, D4. What is the next square?",
                    "من عندنا: مسار سرّي A1، B2، C3، D4. ما المربع التالي؟",
                    "À nous : un parcours secret A1, B2, C3, D4. Quelle est la case suivante ?"), [
        T("Each step goes one row down and one column right. The row after D is E, and the column after 4 is 5.",
          "كل خطوة تنزل صفًا وتنتقل عمودًا إلى اليمين. الصف بعد D هو E والعمود بعد 4 هو 5.",
          "Chaque pas descend d'une ligne et avance d'une colonne. Après D : E ; après 4 : 5."),
        F("A1 → B2 → C3 → D4 → E5"),
    ]),
]
