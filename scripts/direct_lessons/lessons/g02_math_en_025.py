"""Grade 2 Mathematics — Sorting the given."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G02-MATH-EN-025"
GRADE = 2
SUBJECT = "math"
TITLES = {"en": "Sorting the given", "ar": "ترتيب المعطيات", "fr": "Trier les données"}

THEORY = [
    ("Relevant information depends on the question", "المعلومة المفيدة يحددها السؤال", "L'information utile dépend de la question", "54", [
        T("Hello, champion! Today we have lots of information, but each question needs only some of it. Fouad has 5 flower pictures and 8 animal pictures. His brother gives him 4 flower pictures and 2 animal pictures. The question asks about animal pictures only, so we keep 8 and 2: 8 + 2 = 10.",
          "مرحبًا يا بطل! اليوم عندنا معلومات كثيرة، لكن كل سؤال لا يحتاج إلا إلى بعضها. عند فؤاد 5 صور زهور و8 صور حيوانات. أعطاه أخوه 4 صور زهور وصورتين للحيوانات. السؤال عن صور الحيوانات فقط، فنأخذ 8 و2: 8 + 2 = 10.",
          "Fouad a 5 images de fleurs et 8 images d'animaux. Son frère lui donne 4 images de fleurs et 2 d'animaux. La question porte sur les animaux seulement : 8 + 2 = 10."),
        F("8 + 2 = 10"),
    ]),
    ("Read the table and compare", "نقرأ الجدول ونقارن", "Lire le tableau et comparer", "54", [
        T("Maya has red 25, white 46 and blue 35 pearls. A necklace needs 30 pearls. White only: 46 ≥ 30, yes. Red only: 25 < 30, no. Blue left after one necklace: 35 − 30 = 5.",
          "عند مايا خرزات حمراء 25 وبيضاء 46 وزرقاء 35. القلادة تحتاج 30 خرزة. بيضاء فقط: 46 ≥ 30 نعم. حمراء فقط: 25 < 30 لا. تبقى من الزرقاء بعد قلادة: 35 − 30 = 5.",
          "Maya a 25 perles rouges, 46 blanches, 35 bleues. Un collier demande 30 perles. Blanches seules : 46 ≥ 30, oui. Rouges seules : 25 < 30, non. Bleues restantes : 35 − 30 = 5."),
        F("46 ≥ 30 ✓     25 < 30 ✗     35 − 30 = 5"),
    ]),
    ("One data set, different questions", "معطيات واحدة وأسئلة مختلفة", "Mêmes données, questions différentes", "54", [
        T("Mother has 5 strawberry and 6 apricot jars: 11 in all. Nour breaks 1 strawberry and 2 apricot: 3 jars. Strawberry left: 5 − 1 = 4. The same data answers different questions.",
          "عند الأم 5 برطمانات فراولة و6 مشمش: المجموع 11. كسرت نور واحدًا من الفراولة واثنين من المشمش: 3 برطمانات. بقي من الفراولة 5 − 1 = 4. المعطيات نفسها تجيب عن أسئلة مختلفة.",
          "Maman a 5 pots de fraise et 6 d'abricot : 11 en tout. Nour casse 1 fraise et 2 abricot : 3 pots. Fraise restants : 5 − 1 = 4."),
        F("5 + 6 = 11     1 + 2 = 3     5 − 1 = 4"),
    ]),
    ("Sort by category before subtracting", "نرتّب حسب الصنف قبل الطرح", "Trier par catégorie avant de soustraire", "55", [
        T("There are 46 hens and 15 rabbits. 10 hens and 3 rabbits ran away. We never mix hens with rabbits. Hens left: 46 − 10 = 36. Rabbits left: 15 − 3 = 12.",
          "هناك 46 دجاجة و15 أرنبًا. هربت 10 دجاجات و3 أرانب. لا نخلط الدجاج بالأرانب. بقي من الدجاج 46 − 10 = 36 ومن الأرانب 15 − 3 = 12.",
          "46 poules et 15 lapins. 10 poules et 3 lapins se sont enfuis. On ne mélange pas : poules 46 − 10 = 36, lapins 15 − 3 = 12."),
        F("46 − 10 = 36     15 − 3 = 12"),
    ]),
    ("Read the headings before the numbers", "نقرأ العناوين قبل الأعداد", "Lire les titres avant les nombres", "55", [
        T("Father bought orange juice 10, vanilla cookies 8, pineapple juice 6, chocolate cookies 7. Types of juice: 2 (types are categories, not totals). More juice: orange, 10 > 6. Cookie boxes: 8 + 7 = 15.",
          "اشترى الأب عصير برتقال 10، بسكويت فانيلا 8، عصير أناناس 6، بسكويت شوكولا 7. أنواع العصير: 2 (الأنواع أصناف لا مجاميع). الأكثر عصيرًا: البرتقال لأن 10 > 6. علب البسكويت: 8 + 7 = 15.",
          "Jus d'orange 10, biscuits vanille 8, jus d'ananas 6, biscuits chocolat 7. Types de jus : 2. Plus de jus : orange, 10 > 6. Boîtes de biscuits : 8 + 7 = 15."),
        F("types = 2     10 > 6     8 + 7 = 15"),
    ]),
    ("More than and less than", "أكثر من وأقل من", "Plus que et moins que", "55", [
        T("Sami has 17 marbles. Dani has 3 more: 17 + 3 = 20. Karim has 6 less: 17 − 6 = 11. The most marbles: Dani with 20. Careful: \"3 more\" is a difference, not Dani's total.",
          "عند سامي 17 كرة. عند داني 3 أكثر: 17 + 3 = 20. عند كريم 6 أقل: 17 − 6 = 11. الأكثر كرات داني بـ20. انتبه: «3 أكثر» فرق وليست مجموع داني.",
          "Sami a 17 billes. Dani en a 3 de plus : 17 + 3 = 20. Karim en a 6 de moins : 17 − 6 = 11. Le plus : Dani avec 20."),
        F("17 + 3 = 20     17 − 6 = 11"),
    ]),
    ("Row and column", "الصف والعمود", "Ligne et colonne", "55", [
        T("Nour: red 22, blue 8. Dalia: red 10, blue 30. A value needs both its row and its column. Nour's total: 22 + 8 = 30. Red together: 22 + 10 = 32. More blue: Dalia, 30 > 8.",
          "نور: أحمر 22 وأزرق 8. داليا: أحمر 10 وأزرق 30. القيمة تحتاج إلى الصف والعمود معًا. مجموع نور 22 + 8 = 30. الأحمر معًا 22 + 10 = 32. الأكثر أزرق: داليا لأن 30 > 8.",
          "Nour : rouge 22, bleu 8. Dalia : rouge 10, bleu 30. Total de Nour : 22 + 8 = 30. Rouge ensemble : 22 + 10 = 32. Plus de bleu : Dalia."),
        F("22 + 8 = 30     22 + 10 = 32     30 > 8"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Problem solving starts before calculation: read the question, sort the data, keep only what is needed, find the relation, solve, then check.",
          "حل المسألة يبدأ قبل الحساب: اقرأ السؤال، رتّب المعطيات، خذ المفيد فقط، ابنِ العلاقة، احسب ثم تحقق.",
          "Résoudre commence avant le calcul : lire, trier, choisir l'utile, relier, calculer, vérifier."),
        F("READ → SORT → SELECT → RELATE → SOLVE → CHECK"),
    ]),
]

def _e(n, pg, en, ar, fr, steps):
    return EX(n, pg, st(en, ar, fr), steps)

EXERCISES = [
    _e("1", "54", "Fouad: how many animal pictures?", "فؤاد: كم صورة حيوان عنده؟", "Fouad : combien d'images d'animaux ?",
       [F("8 + 2 = 10"), T("Fouad has 10 animal pictures.", "عند فؤاد 10 صور حيوانات.", "Fouad a 10 images d'animaux.")]),
    _e("2", "54", "Maya: white only? red only? blue left?", "مايا: بيضاء فقط؟ حمراء فقط؟ كم بقي من الزرقاء؟", "Maya : blanches seules ? rouges seules ? bleues restantes ?",
       [F("yes     no     35 − 30 = 5")]),
    _e("3", "54", "Jam jars: total, broken, strawberry left.", "البرطمانات: المجموع والمكسور وما بقي من الفراولة.", "Pots : total, cassés, fraise restants.",
       [F("11     3     5 − 1 = 4")]),
    _e("4", "55", "Hens and rabbits left.", "كم بقي من الدجاج والأرانب؟", "Poules et lapins restants.",
       [F("46 − 10 = 36     15 − 3 = 12")]),
    _e("5", "55", "Father's purchases: juice types, more juice, cookie boxes.", "مشتريات الأب: أنواع العصير والأكثر وعلب البسكويت.", "Achats du père : types de jus, plus de jus, boîtes.",
       [F("2     orange     8 + 7 = 15")]),
    _e("6", "55", "Marbles: Dani, Karim, who has the most?", "الكرات: داني وكريم ومن الأكثر؟", "Billes : Dani, Karim, qui en a le plus ?",
       [F("20     11     Dani")]),
    _e("7", "55", "Nour and Dalia's pearls.", "خرزات نور وداليا.", "Perles de Nour et Dalia.",
       [F("30     32     Dalia")]),
    _e("8", "", "Guided practice: Lina red 12, blue 7; Omar red 9, blue 15. Red total?", "تدريب: لينا أحمر 12 وأزرق 7؛ عمر أحمر 9 وأزرق 15. مجموع الأحمر؟", "Lina rouge 12, bleu 7 ; Omar rouge 9, bleu 15. Total rouge ?",
       [F("12 + 9 = 21"), T("Ignore the blue values.", "نتجاهل قيم الأزرق.", "On ignore le bleu.")]),
    _e("9", "", "Transfer: 18 apples, 25 oranges; 6 apples and 10 oranges sold. Oranges left?", "تحدٍّ: 18 تفاحة و25 برتقالة؛ بيعت 6 تفاحات و10 برتقالات. كم برتقالة بقيت؟", "Défi : 18 pommes, 25 oranges ; 6 pommes et 10 oranges vendues. Oranges restantes ?",
       [F("25 − 10 = 15")]),
    _e("10", "", "Error detective: 5+8+4+2 = 19 for animal pictures; 10+6 = 16 juice types.", "المحقق: 5+8+4+2 = 19 صور حيوانات؛ 10+6 = 16 نوع عصير.", "Détective : 5+8+4+2 = 19 ; 10+6 = 16 types de jus.",
       [F("10     2"), T("Flowers are irrelevant; types are categories, not totals.", "صور الزهور غير مفيدة، والأنواع أصناف لا مجاميع.", "Les fleurs sont inutiles ; les types sont des catégories.")]),
    _e("11", "", "Final check of all answers.", "تقييم أخير لكل الإجابات.", "Évaluation finale.",
       [F("10, yes, no, 5, 11, 3, 4, 36, 12, 15, 20, 11, Dani, 30, 32, Dalia")]),
]
