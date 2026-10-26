"""Grade 2 Mathematics — Addition: calculation technique (1), with regrouping."""
from scripts.direct_lessons.common import T, F, EX, st, tens
from scripts.direct_lessons.lessons.g02_math_en_008 import vert

LESSON_ID = "G02-MATH-EN-014"
GRADE = 2
SUBJECT = "math"
TITLES = {"en": "Addition: calculation technique (1)", "ar": "الجمع: تقنية الحساب (1)", "fr": "Addition : technique de calcul (1)"}

THEORY = [
    ("Ten ones become one ten", "عشرة آحاد تصبح عشرة واحدة", "Dix unités deviennent une dizaine", "36", [
        tens(3, 5, tag="A", eq=True),
        tens(2, 8, tag="B", eq=True),
        T("Hello, champion! A new way to add: 35 + 28. 35 is 3 tens and 5 ones. 28 is 2 tens and 8 ones. Ones first: 5 + 8 = 13 ones. 13 ones cannot stay loose: we trade 10 ones for 1 ten. So 13 ones = 1 ten and 3 ones.",
          "مرحبًا يا بطل! طريقة جديدة للجمع: 35 + 28. 35 هي 3 عشرات و5 آحاد. و28 هي عشرتان و8 آحاد. الآحاد أولًا: 5 + 8 = 13 واحدًا. لا تبقى 13 واحدًا منفردة: نبدّل 10 آحاد بعشرة واحدة. إذن 13 واحدًا = عشرة و3 آحاد.",
          "Une nouvelle façon d'additionner : 35 + 28. 35 = 3 dizaines et 5 unités. 28 = 2 dizaines et 8 unités. Les unités d'abord : 5 + 8 = 13 unités. On échange 10 unités contre 1 dizaine : 13 unités = 1 dizaine et 3 unités."),
        tens(1, 3, tag="C", eq=True),
    ]),
    ("Write the ones, add the new ten", "نكتب الآحاد ونضيف العشرة الجديدة", "On écrit les unités, on ajoute la nouvelle dizaine", "36", [
        vert([35, 28], 63),
        T("We write 3 in the ones column. The new ten joins the tens: 3 + 2 + 1 = 6 tens. So 35 + 28 = 63. The small 1 is not a magic digit and not one unit. It is one real ten, made from 10 ones.",
          "نكتب 3 في عمود الآحاد. والعشرة الجديدة تنضم إلى العشرات: 3 + 2 + 1 = 6 عشرات. إذن 35 + 28 = 63. الرقم 1 الصغير ليس رقمًا سحريًا وليس واحدًا. إنه عشرة حقيقية تكوّنت من 10 آحاد.",
          "On écrit 3 aux unités. La nouvelle dizaine rejoint les dizaines : 3 + 2 + 1 = 6 dizaines. Donc 35 + 28 = 63. Le petit 1 n'est pas magique et n'est pas une unité : c'est une vraie dizaine, faite de 10 unités."),
        F("35 + 28 = 63"),
    ]),
    ("Steps", "الخطوات", "Les étapes", "36", [
        T("1) Align ones under ones and tens under tens. 2) Add the ones. 3) If there are 10 ones or more, regroup 10 ones as 1 ten. 4) Write the remaining ones. 5) Add the tens and the new ten. 6) Check.",
          "1) نحاذي الآحاد تحت الآحاد والعشرات تحت العشرات. 2) نجمع الآحاد. 3) إن كان عندنا 10 آحاد أو أكثر نحوّل 10 آحاد إلى عشرة واحدة. 4) نكتب الآحاد الباقية. 5) نجمع العشرات مع العشرة الجديدة. 6) نتحقق.",
          "1) Aligner unités sous unités, dizaines sous dizaines. 2) Additionner les unités. 3) S'il y en a 10 ou plus, regrouper 10 unités en 1 dizaine. 4) Écrire les unités restantes. 5) Additionner les dizaines et la nouvelle. 6) Vérifier."),
        vert([24, 17], 41),
    ]),
    ("Three numbers", "ثلاثة أعداد", "Trois nombres", "37", [
        vert([34, 45, 7], 86),
        T("34 + 45 + 7. The 7 is 7 ones, so it goes in the ones column. Ones: 4 + 5 + 7 = 16 = 1 ten + 6 ones. Write 6. Tens: 3 + 4 + 0 + 1 = 8. The answer is 86.",
          "34 + 45 + 7. العدد 7 هو 7 آحاد فيوضع في عمود الآحاد. الآحاد: 4 + 5 + 7 = 16 = عشرة و6 آحاد. نكتب 6. العشرات: 3 + 4 + 0 + 1 = 8. الجواب 86.",
          "34 + 45 + 7. Le 7 est 7 unités : colonne des unités. Unités : 4 + 5 + 7 = 16 = 1 dizaine + 6 unités. On écrit 6. Dizaines : 3 + 4 + 0 + 1 = 8. Réponse : 86."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("When the ones make 10 or more, we trade 10 ones for 1 ten, write the remaining ones, and add the new ten to the tens.",
          "عندما تبلغ الآحاد 10 أو أكثر نبدّل 10 آحاد بعشرة واحدة ونكتب الآحاد الباقية ونضيف العشرة الجديدة إلى العشرات.",
          "Quand les unités font 10 ou plus, on échange 10 unités contre 1 dizaine, on écrit les unités restantes et on ajoute la nouvelle dizaine."),
        F("ALIGN → ADD ONES → REGROUP 10 ONES → ADD TENS + NEW TEN → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "36", st("Calculate: 5+7, 8+6, 7+8, 6+9, 15+7, 17+7, 13+9, 14+8, 11+9, 15+5, 14+6, 13+7, 16+9, 19+9, 15+8, 13+8.", "احسب: 5+7، 8+6، 7+8، 6+9، 15+7، 17+7، 13+9، 14+8، 11+9، 15+5، 14+6، 13+7، 16+9، 19+9، 15+8، 13+8.", "Calcule : 5+7, 8+6, 7+8, 6+9, 15+7, 17+7, 13+9, 14+8, 11+9, 15+5, 14+6, 13+7, 16+9, 19+9, 15+8, 13+8."), [
        F("12  14  15  15  22  24  22  22"),
        F("20  20  20  20  25  28  23  21"),
    ]),
    EX("2", "36", st("Write in vertical form and calculate: 24 + 17; 36 + 29; 55 + 28.", "اكتب عموديًا واحسب: 24 + 17؛ 36 + 29؛ 55 + 28.", "Pose et calcule : 24 + 17 ; 36 + 29 ; 55 + 28."), [
        vert([24, 17], 41), vert([36, 29], 65), vert([55, 28], 83),
    ]),
    EX("3", "36", st("Calculate: 25 + 47, 38 + 45, 46 + 25, 37 + 18, 26 + 27, 63 + 17.", "احسب: 25 + 47، 38 + 45، 46 + 25، 37 + 18، 26 + 27، 63 + 17.", "Calcule : 25 + 47, 38 + 45, 46 + 25, 37 + 18, 26 + 27, 63 + 17."), [
        F("72   83   71   55   53   80"),
        T("For 63 + 17: 3 + 7 = 10 ones → 0 ones and 1 new ten; 6 + 1 + 1 = 8 tens.", "في 63 + 17: 3 + 7 = 10 آحاد → 0 آحاد وعشرة جديدة؛ 6 + 1 + 1 = 8 عشرات.", "Pour 63 + 17 : 3 + 7 = 10 unités → 0 unité et 1 dizaine ; 6 + 1 + 1 = 8 dizaines."),
    ]),
    EX("4", "36", st("Vertical form: 26 + 38, 46 + 36, 55 + 27, 68 + 14, 59 + 23.", "عموديًا: 26 + 38، 46 + 36، 55 + 27، 68 + 14، 59 + 23.", "Posées : 26 + 38, 46 + 36, 55 + 27, 68 + 14, 59 + 23."), [
        F("64   82   82   82   82"),
        T("Different additions can have the same sum.", "عمليات جمع مختلفة قد يكون لها المجموع نفسه.", "Des additions différentes peuvent avoir la même somme."),
    ]),
    EX("5", "37", st("Replace the dots: 47 + 25; 36 + 47; 46 + 39; 48 + 37; 53 + 18 (each with its sum).", "استبدل النقاط: 47 + 25؛ 36 + 47؛ 46 + 39؛ 48 + 37؛ 53 + 18 (مع مجموع كل منها).", "Remplace les points : 47 + 25 ; 36 + 47 ; 46 + 39 ; 48 + 37 ; 53 + 18 (avec chaque somme)."), [
        F("47 + 25 = 72      36 + 47 = 83      46 + 39 = 85"),
        F("48 + 37 = 85      53 + 18 = 71"),
        T("Column by column: for 47 + 25, 7 + 5 = 12 → write 2, regroup 1; 4 + 2 + 1 = 7.", "عمودًا عمودًا: في 47 + 25، 7 + 5 = 12 → نكتب 2 ونحمل 1؛ 4 + 2 + 1 = 7.", "Colonne par colonne : 47 + 25, 7 + 5 = 12 → on écrit 2, on retient 1 ; 4 + 2 + 1 = 7."),
    ]),
    EX("6", "37", st("Calculate: 43 + 15 + 24; 43 + 21 + 28; 34 + 45 + 7; 36 + 25 + 4; 48 + 22 + 25.", "احسب: 43 + 15 + 24؛ 43 + 21 + 28؛ 34 + 45 + 7؛ 36 + 25 + 4؛ 48 + 22 + 25.", "Calcule : 43 + 15 + 24 ; 43 + 21 + 28 ; 34 + 45 + 7 ; 36 + 25 + 4 ; 48 + 22 + 25."), [
        F("82   92   86   65   95"),
    ]),
    EX("7", "37", st("The baker sold 48 thyme croissants and 36 cheese croissants. How many in all?", "باع الخبّاز 48 كرواسان بالزعتر و36 بالجبن. كم كرواسان باع؟", "Le boulanger a vendu 48 croissants au thym et 36 au fromage. Combien en tout ?"), [
        vert([48, 36], 84),
        T("Given: 48 and 36. Asked: the total. Two groups are combined, so we add. 8 + 6 = 14 → write 4, regroup 1; 4 + 3 + 1 = 8. He sold 84 croissants.", "المعطى: 48 و36. المطلوب: المجموع. جمعنا مجموعتين فنجمع. 8 + 6 = 14 → نكتب 4 ونحمل 1؛ 4 + 3 + 1 = 8. باع 84 كرواسان.", "Donné : 48 et 36. Cherché : le total. On réunit deux groupes : addition. 8 + 6 = 14 → 4 et on retient 1 ; 4 + 3 + 1 = 8. Il a vendu 84 croissants."),
    ]),
    EX("8", "37", st("Sami has 32 red, 25 blue and 18 yellow balloons. How many in all?", "عند سامي 32 بالونًا أحمر و25 أزرق و18 أصفر. كم بالونًا عنده؟", "Sami a 32 ballons rouges, 25 bleus et 18 jaunes. Combien en tout ?"), [
        vert([32, 25, 18], 75),
        T("2 + 5 + 8 = 15 → write 5, regroup 1; 3 + 2 + 1 + 1 = 7 tens. Sami has 75 balloons.", "2 + 5 + 8 = 15 → نكتب 5 ونحمل 1؛ 3 + 2 + 1 + 1 = 7 عشرات. عند سامي 75 بالونًا.", "2 + 5 + 8 = 15 → 5 et on retient 1 ; 3 + 2 + 1 + 1 = 7. Sami a 75 ballons."),
    ]),
    EX("9", "37", st("Colour the circles with the same sum: 35+28, 36+19, 46+17, 14+8+43, 42+5+16, 34+25+4, 63+19.", "لوّن الدوائر ذات المجموع نفسه: 35+28، 36+19، 46+17، 14+8+43، 42+5+16، 34+25+4، 63+19.", "Colorie les cercles de même somme : 35+28, 36+19, 46+17, 14+8+43, 42+5+16, 34+25+4, 63+19."), [
        F("63   55   63   65   63   63   82"),
        T("The sums equal to 63: 35 + 28, 46 + 17, 42 + 5 + 16, 34 + 25 + 4.", "المجاميع التي تساوي 63: 35 + 28 و46 + 17 و42 + 5 + 16 و34 + 25 + 4.", "Les sommes égales à 63 : 35 + 28, 46 + 17, 42 + 5 + 16, 34 + 25 + 4."),
    ]),
    EX("10", "", st("Guided practice: 27 + 18; 46 + 29; 28 + 36 + 5.", "تدريب موجَّه: 27 + 18؛ 46 + 29؛ 28 + 36 + 5.", "Entraînement : 27 + 18 ; 46 + 29 ; 28 + 36 + 5."), [
        F("45      75      69"),
    ]),
    EX("11", "", st("Transfer: 58 + 27. Where does the 1 come from?", "تحدٍّ: 58 + 27. من أين جاء الرقم 1؟", "Défi : 58 + 27. D'où vient le 1 ?"), [
        vert([58, 27], 85),
        T("8 + 7 = 15 = 1 ten + 5 ones. The 1 comes from 10 of the 15 ones. Tens: 5 + 2 + 1 = 8.", "8 + 7 = 15 = عشرة و5 آحاد. الرقم 1 جاء من 10 آحاد داخل الـ15. العشرات: 5 + 2 + 1 = 8.", "8 + 7 = 15 = 1 dizaine + 5 unités. Le 1 vient de 10 des 15 unités. Dizaines : 5 + 2 + 1 = 8."),
    ]),
    EX("12", "", st("Error detective: 46 + 25 = 61; 63 + 17 = 710.", "المحقق: 46 + 25 = 61؛ 63 + 17 = 710.", "Détective : 46 + 25 = 61 ; 63 + 17 = 710."), [
        F("46 + 25 = 71      63 + 17 = 80"),
        T("6 + 5 = 11 → 1 one remains and 1 ten joins the tens. And 3 + 7 = 10 ones is 1 new ten with 0 ones, not 10 in the ones column.", "6 + 5 = 11 → يبقى واحد وتنضم عشرة إلى العشرات. و3 + 7 = 10 آحاد هي عشرة جديدة و0 آحاد لا 10 في عمود الآحاد.", "6 + 5 = 11 → 1 unité reste et 1 dizaine rejoint les dizaines. 3 + 7 = 10 unités = 1 dizaine et 0 unité."),
    ]),
    EX("13", "", st("Final check: 24+17; 36+29; 38+45; 63+17; 47+25; 43+21+28; croissants; balloons; why does the regrouped 1 belong in tens?", "تقييم أخير: 24+17؛ 36+29؛ 38+45؛ 63+17؛ 47+25؛ 43+21+28؛ الكرواسان؛ البالونات؛ ولماذا يُوضع الـ1 المحمول في العشرات؟", "Évaluation : 24+17 ; 36+29 ; 38+45 ; 63+17 ; 47+25 ; 43+21+28 ; croissants ; ballons ; pourquoi le 1 retenu va aux dizaines ?"), [
        F("41   65   83   80   72   92   84   75"),
        T("Because it represents one group of ten made from 10 ones.", "لأنه يمثل مجموعة عشرة تكوّنت من 10 آحاد.", "Parce qu'il représente un groupe de dix fait de 10 unités."),
    ]),
]
