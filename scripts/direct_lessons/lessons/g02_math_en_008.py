"""Grade 2 Mathematics — Addition (2): vertical addition without regrouping."""
from scripts.direct_lessons.common import T, F, EX, st, tens, scene


def vert(nums, total=None, tag="V", hi=None, op="+"):
    """Vertical addition: numbers right-aligned in tens/ones columns, plus sign, line, optional total."""
    cx_t, cx_o, y0, dy = 300, 360, 70, 62
    svg, ids = "", []
    for i, n in enumerate(nums):
        s = str(n)
        t, o = (s[:-1] or ""), s[-1]
        sid = f"{tag}{i}"
        txt = lambda x, v: f'<text x="{x}" y="{y0 + i*dy}" font-size="56" font-weight="700" text-anchor="middle" fill="#0b3d5c" font-family="sans-serif">{v}</text>'
        svg += f'<g id="{sid}">{txt(cx_t, t) if t else ""}{txt(cx_o, o)}'
        if i == len(nums) - 1:
            svg += f'<text x="{cx_t-90}" y="{y0 + i*dy}" font-size="56" font-weight="700" text-anchor="middle" fill="#e53935" font-family="sans-serif">{op}</text>'
        svg += "</g>"
        ids.append(sid)
    yl = y0 + (len(nums) - 1) * dy + 22
    svg += f'<g id="{tag}L"><line x1="{cx_t-120}" y1="{yl}" x2="{cx_o+50}" y2="{yl}" stroke="#0b3d5c" stroke-width="5"/>'
    svg += f'<text x="{cx_t}" y="{yl+22}" font-size="22" font-weight="700" text-anchor="middle" fill="#2e7d32" font-family="sans-serif">tens</text>'
    svg += f'<text x="{cx_o}" y="{yl+22}" font-size="22" font-weight="700" text-anchor="middle" fill="#2e7d32" font-family="sans-serif">ones</text></g>'
    ids.append(tag + "L")
    if total is not None:
        s = str(total)
        svg += (f'<g id="{tag}S"><text x="{cx_t}" y="{yl+78}" font-size="56" font-weight="700" text-anchor="middle" fill="#2e7d32" font-family="sans-serif">{s[:-1]}</text>'
                f'<text x="{cx_o}" y="{yl+78}" font-size="56" font-weight="700" text-anchor="middle" fill="#2e7d32" font-family="sans-serif">{s[-1]}</text></g>')
        ids.append(tag + "S")
    return scene(svg, ids)


LESSON_ID = "G02-MATH-EN-008"
GRADE = 2
SUBJECT = "math"
TITLES = {"en": "Addition (2)", "ar": "الجمع (2)", "fr": "Addition (2)"}

THEORY = [
    ("Tens under tens, ones under ones", "العشرات تحت العشرات والآحاد تحت الآحاد", "Dizaines sous dizaines, unités sous unités", "26", [
        tens(3, 5, tag="A", eq=True),
        tens(1, 4, tag="B", eq=True),
        vert([35, 14], 49),
        T("Hello, champion! Today we continue addition in an organised way. 35 is 3 tens and 5 ones. 14 is 1 ten and 4 ones. We write the second number under the first: tens under tens, ones under ones. Ones: 5 + 4 = 9. Tens: 3 + 1 = 4. So 35 + 14 = 49.",
          "مرحبًا يا بطل! اليوم نكمل الجمع بطريقة منظمة. 35 هي 3 عشرات و5 آحاد. و14 هي عشرة و4 آحاد. نكتب العدد الثاني تحت الأول: العشرات تحت العشرات والآحاد تحت الآحاد. الآحاد: 5 + 4 = 9. العشرات: 3 + 1 = 4. إذن 35 + 14 = 49.",
          "Bonjour champion ! Aujourd'hui on continue l'addition de façon organisée. 35 = 3 dizaines et 5 unités. 14 = 1 dizaine et 4 unités. On écrit le second nombre sous le premier : dizaines sous dizaines, unités sous unités. Unités : 5 + 4 = 9. Dizaines : 3 + 1 = 4. Donc 35 + 14 = 49."),
    ]),
    ("Steps of the vertical addition", "خطوات الجمع العمودي", "Les étapes de l'addition posée", "26", [
        vert([45, 22], 67),
        T("1) Write the first number. 2) Write the second under it. 3) Tens under tens. 4) Ones under ones. 5) Add the ones: 5 + 2 = 7. 6) Add the tens: 4 + 2 = 6. 7) Check. The answer is 67. Before calculating, always check the alignment: are the ones above each other, and the tens above each other?",
          "1) نكتب العدد الأول. 2) نكتب الثاني تحته. 3) العشرات تحت العشرات. 4) الآحاد تحت الآحاد. 5) نجمع الآحاد: 5 + 2 = 7. 6) نجمع العشرات: 4 + 2 = 6. 7) نتحقق. الجواب 67. وقبل الحساب نتأكد دائمًا من المحاذاة: هل الآحاد فوق بعضها والعشرات فوق بعضها؟",
          "1) On écrit le premier nombre. 2) Le second dessous. 3) Dizaines sous dizaines. 4) Unités sous unités. 5) Unités : 5 + 2 = 7. 6) Dizaines : 4 + 2 = 6. 7) On vérifie. Réponse : 67. Avant de calculer, on vérifie l'alignement."),
    ]),
    ("Find a missing digit column by column", "نجد الرقم الناقص عمودًا عمودًا", "Trouver un chiffre manquant colonne par colonne", "27", [
        F("24 + 4• = •7"),
        T("We do not guess. Ones first: 4 + ? = 7, so ? = 3. Tens: 2 + 4 = 6. So 24 + 43 = 67.",
          "لا نخمّن. الآحاد أولًا: 4 + ؟ = 7 إذن ؟ = 3. العشرات: 2 + 4 = 6. إذن 24 + 43 = 67.",
          "On ne devine pas. Unités d'abord : 4 + ? = 7, donc ? = 3. Dizaines : 2 + 4 = 6. Donc 24 + 43 = 67."),
        vert([24, 43], 67),
    ]),
    ("Three numbers", "ثلاثة أعداد", "Trois nombres", "27", [
        vert([41, 12, 5], 58),
        T("We can add three numbers by the same column rule. In 41 + 12 + 5, the 5 is 5 ones, so it goes in the ones column. Ones: 1 + 2 + 5 = 8. Tens: 4 + 1 + 0 = 5. The answer is 58. All three addends must be included.",
          "نجمع ثلاثة أعداد بقاعدة الأعمدة نفسها. في 41 + 12 + 5 العدد 5 هو 5 آحاد فيوضع في عمود الآحاد. الآحاد: 1 + 2 + 5 = 8. العشرات: 4 + 1 + 0 = 5. الجواب 58. ويجب إدخال الأعداد الثلاثة كلها.",
          "On additionne trois nombres avec la même règle. Dans 41 + 12 + 5, le 5 est 5 unités : colonne des unités. Unités : 1 + 2 + 5 = 8. Dizaines : 4 + 1 + 0 = 5. Réponse : 58. Les trois nombres doivent être comptés."),
    ]),
    ("Same sum, different additions", "مجموع واحد وعمليات مختلفة", "Même somme, additions différentes", "27", [
        F("22 + 4 + 43 = 69      54 + 15 = 69      42 + 27 = 69      but  34 + 21 + 13 = 68"),
        T("Different additions can have the same sum. We calculate first and colour second, never by the shape of the leaf.",
          "عمليات جمع مختلفة قد يكون لها المجموع نفسه. نحسب أولًا ونلوّن ثانيًا، لا حسب شكل الورقة.",
          "Des additions différentes peuvent avoir la même somme. On calcule d'abord, on colorie ensuite, jamais d'après la forme de la feuille."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Tens under tens and ones under ones. We add the ones, then the tens. We can add two or three numbers, find missing digits and compare sums.",
          "العشرات تحت العشرات والآحاد تحت الآحاد. نجمع الآحاد ثم العشرات. نستطيع جمع عددين أو ثلاثة وإيجاد أرقام ناقصة ومقارنة المجاميع.",
          "Dizaines sous dizaines, unités sous unités. On additionne les unités puis les dizaines. On peut additionner deux ou trois nombres, trouver des chiffres manquants et comparer des sommes."),
        F("ALIGN → ONES → TENS → SUM → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "26", st("Write the numbers and calculate: 3 tens 4 ones + 2 tens 2 ones; 2 tens 4 ones + 2 tens.", "اكتب العددين واحسب: 3 عشرات و4 آحاد + عشرتان وآحادان؛ عشرتان و4 آحاد + عشرتان.", "Écris les nombres et calcule : 3 dizaines 4 unités + 2 dizaines 2 unités ; 2 dizaines 4 unités + 2 dizaines."), [
        vert([34, 22], 56),
        vert([24, 20], 44),
        F("34 + 22 = 56      24 + 20 = 44"),
    ]),
    EX("2", "26", st("Write in vertical form and calculate: 45 + 22; 43 + 26; 57 + 12.", "اكتب عموديًا واحسب: 45 + 22؛ 43 + 26؛ 57 + 12.", "Pose et calcule : 45 + 22 ; 43 + 26 ; 57 + 12."), [
        vert([45, 22], 67),
        vert([43, 26], 69),
        vert([57, 12], 69),
    ]),
    EX("3", "26", st("Calculate: 45 + 22, 36 + 33, 23 + 44, 35 + 32, 41 + 28.", "احسب: 45 + 22، 36 + 33، 23 + 44، 35 + 32، 41 + 28.", "Calcule : 45 + 22, 36 + 33, 23 + 44, 35 + 32, 41 + 28."), [
        F("67      69      67      67      69"),
        T("Each time: ones column first, then tens column.", "في كل مرة: عمود الآحاد أولًا ثم عمود العشرات.", "À chaque fois : colonne des unités, puis des dizaines."),
    ]),
    EX("4", "26", st("Write in vertical form and calculate: 25 + 32, 43 + 26, 17 + 42, 53 + 15, 36 + 32.", "اكتب عموديًا واحسب: 25 + 32، 43 + 26، 17 + 42، 53 + 15، 36 + 32.", "Pose et calcule : 25 + 32, 43 + 26, 17 + 42, 53 + 15, 36 + 32."), [
        F("57      69      59      68      68"),
        vert([25, 32], 57),
    ]),
    EX("5", "27", st("Replace the dot by the appropriate number: 24 + 4• = •7; 37 + •2 = 5•; 4• + 23 = •9; 5• + •6 = 68; 43 + •• = 57.", "استبدل النقطة بالعدد المناسب: 24 + 4• = •7؛ 37 + •2 = 5•؛ 4• + 23 = •9؛ 5• + •6 = 68؛ 43 + •• = 57.", "Remplace le point par le nombre convenable : 24 + 4• = •7 ; 37 + •2 = 5• ; 4• + 23 = •9 ; 5• + •6 = 68 ; 43 + •• = 57."), [
        F("24 + 43 = 67      37 + 22 = 59      46 + 23 = 69"),
        F("52 + 16 = 68      43 + 14 = 57"),
        T("Each digit comes from its column: for the last one, 3 + 4 = 7 and 4 + 1 = 5, so the missing number is 14.", "كل رقم يأتي من عموده: في الأخيرة 3 + 4 = 7 و4 + 1 = 5 فالعدد الناقص 14.", "Chaque chiffre vient de sa colonne : pour la dernière, 3 + 4 = 7 et 4 + 1 = 5, le nombre manquant est 14."),
    ]),
    EX("6", "27", st("Write in vertical form and calculate: 31 + 15 + 12; 41 + 12 + 5.", "اكتب عموديًا واحسب: 31 + 15 + 12؛ 41 + 12 + 5.", "Pose et calcule : 31 + 15 + 12 ; 41 + 12 + 5."), [
        vert([31, 15, 12], 58),
        vert([41, 12, 5], 58),
    ]),
    EX("7", "27", st("Calculate: 24 + 12 + 33, 43 + 11 + 5, 25 + 12 + 21, 32 + 21 + 5, 13 + 32 + 21.", "احسب: 24 + 12 + 33، 43 + 11 + 5، 25 + 12 + 21، 32 + 21 + 5، 13 + 32 + 21.", "Calcule : 24 + 12 + 33, 43 + 11 + 5, 25 + 12 + 21, 32 + 21 + 5, 13 + 32 + 21."), [
        F("69      59      58      58      66"),
    ]),
    EX("8", "27", st("Write in vertical form and calculate: 41 + 5 + 23, 23 + 13 + 23, 51 + 12 + 4, 21 + 31 + 17.", "اكتب عموديًا واحسب: 41 + 5 + 23، 23 + 13 + 23، 51 + 12 + 4، 21 + 31 + 17.", "Pose et calcule : 41 + 5 + 23, 23 + 13 + 23, 51 + 12 + 4, 21 + 31 + 17."), [
        F("69      59      67      69"),
        vert([41, 5, 23], 69),
    ]),
    EX("9", "27", st("Colour in green the leaves with the same sum: 22 + 4 + 43; 34 + 21 + 13; 54 + 15; 14 + 35; 42 + 27.", "لوّن بالأخضر الأوراق التي لها المجموع نفسه: 22 + 4 + 43؛ 34 + 21 + 13؛ 54 + 15؛ 14 + 35؛ 42 + 27.", "Colorie en vert les feuilles de même somme : 22 + 4 + 43 ; 34 + 21 + 13 ; 54 + 15 ; 14 + 35 ; 42 + 27."), [
        F("69      68      69      49      69"),
        T("The sums 69 belong to leaves 1, 3 and 5.", "المجاميع 69 للأوراق 1 و3 و5.", "Les sommes 69 sont aux feuilles 1, 3 et 5."),
    ]),
    EX("10", "27", st("Riddle: I am a number between 50 and 60. If 7 is added to me, my ones digit becomes 9. Who am I?", "لغز: أنا عدد بين 50 و60. إذا أضفنا إليّ 7 صار رقم آحادي 9. من أنا؟", "Devinette : je suis un nombre entre 50 et 60. Si on m'ajoute 7, mon chiffre des unités devient 9. Qui suis-je ?"), [
        F("2 + 7 = 9      52 + 7 = 59"),
        T("The ones digit must be 2, and the number is in the 50s: 52.", "رقم الآحاد يجب أن يكون 2 والعدد في الخمسينات: 52.", "Le chiffre des unités est 2 et le nombre est dans les 50 : 52."),
    ]),
    EX("11", "", st("Guided practice: 32 + 24; 41 + 17; 22 + 13 + 24; 42 + __ = 57.", "تدريب موجَّه: 32 + 24؛ 41 + 17؛ 22 + 13 + 24؛ 42 + __ = 57.", "Entraînement : 32 + 24 ; 41 + 17 ; 22 + 13 + 24 ; 42 + __ = 57."), [
        F("56      58      59      15"),
    ]),
    EX("12", "", st("Transfer: 24 + 15 + 20. Does the order matter?", "تحدٍّ: 24 + 15 + 20. هل يهمّ الترتيب؟", "Défi : 24 + 15 + 20. L'ordre compte-t-il ?"), [
        vert([24, 15, 20], 59),
        T("The order does not change the sum: 20 + 24 + 15 is also 59.", "لا يغيّر الترتيب المجموع: 20 + 24 + 15 أيضًا 59.", "L'ordre ne change pas la somme : 20 + 24 + 15 = 59 aussi."),
    ]),
    EX("13", "", st("Error detective: 35 + 14 = 94; 43 + 14 = 56; 34 + 21 + 13 with the 69 leaves.", "المحقق: 35 + 14 = 94؛ 43 + 14 = 56؛ 34 + 21 + 13 مع أوراق الـ69.", "Détective : 35 + 14 = 94 ; 43 + 14 = 56 ; 34 + 21 + 13 avec les feuilles 69."), [
        F("35 + 14 = 49      43 + 14 = 57      34 + 21 + 13 = 68"),
        T("94 reversed the digits; 56 miscounted the ones; and 34 + 21 + 13 is 68, not 69.", "في 94 قُلبت الأرقام؛ وفي 56 أُخطئ عدّ الآحاد؛ و34 + 21 + 13 يساوي 68 لا 69.", "94 a inversé les chiffres ; 56 a mal compté les unités ; 34 + 21 + 13 = 68, pas 69."),
    ]),
    EX("14", "", st("Final check: 34 + 22; 43 + 26; 17 + 42; 24 + 43; 43 + __ = 57; 31 + 15 + 12; 23 + 13 + 23; why does the 5 in 41 + 12 + 5 go in the ones column?", "تقييم أخير: 34 + 22؛ 43 + 26؛ 17 + 42؛ 24 + 43؛ 43 + __ = 57؛ 31 + 15 + 12؛ 23 + 13 + 23؛ ولماذا يوضع 5 في عمود الآحاد في 41 + 12 + 5؟", "Évaluation : 34 + 22 ; 43 + 26 ; 17 + 42 ; 24 + 43 ; 43 + __ = 57 ; 31 + 15 + 12 ; 23 + 13 + 23 ; pourquoi le 5 de 41 + 12 + 5 va-t-il aux unités ?"), [
        F("56   69   59   67   14   58   59"),
        T("Because it means 5 ones, not 5 tens.", "لأنه يعني 5 آحاد لا 5 عشرات.", "Parce que c'est 5 unités, pas 5 dizaines."),
    ]),
]
