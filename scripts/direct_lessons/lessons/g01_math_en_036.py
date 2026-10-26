"""Grade 1 Mathematics — The numbers up to 69."""
from scripts.direct_lessons.common import T, F, EX, st, tens

LESSON_ID = "G01-MATH-EN-036"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "The numbers up to 69", "ar": "الأعداد حتى 69", "fr": "Les nombres jusqu'à 69"}

THEORY = [
    ("See the tens first, then the ones", "ننظر إلى العشرات أولًا ثم الآحاد", "On regarde d'abord les dizaines, puis les unités", "92", [
        T("Hello, champion! We know that 10 is one ten, 20 is two tens, and so on up to 60. Today not every number is a whole ten. We may have 4 tens and 3 more ones. We will not count from one up to 43; we will look at the structure of the number. How many full tens do you see? 4 tens, which is 40. How many single ones? 3. So the number is 43: 43 = 4 tens + 3 ones = 40 + 3.",
          "مرحبًا يا بطل! نعرف أن 10 عشرة واحدة و20 عشرتان وهكذا حتى 60. واليوم ليس كل عدد عشرات كاملة؛ قد يكون عندنا 4 عشرات ومعها 3 آحاد. لن نعدّ من الواحد حتى 43، بل سننظر إلى بنية العدد. كم عشرة كاملة ترى؟ 4 عشرات أي 40. وكم واحدًا منفردًا؟ 3. إذن العدد 43: 43 = 4 عشرات + 3 آحاد = 40 + 3.",
          "Bonjour champion ! On sait que 10, c'est une dizaine, 20, deux dizaines, jusqu'à 60. Aujourd'hui, tous les nombres ne sont pas des dizaines entières : on peut avoir 4 dizaines et 3 unités. On ne compte pas de un à 43 : on regarde la structure du nombre. Combien de dizaines entières ? 4, soit 40. Combien d'unités seules ? 3. Donc 43 = 4 dizaines + 3 unités = 40 + 3."),
        tens(4, 3, eq=True),
        F("43 = 4 tens + 3 ones = 40 + 3"),
    ]),
    ("Tens first, then ones", "العشرات أولًا ثم الآحاد", "Dizaines d'abord, puis unités", "92", [
        tens(3, 6, eq=True),
        T("Here are 3 bundles and 6 loose ones. Do not count every object. First count the tens: 3 tens = 30. Then count the loose ones: 6. Then join: 30 + 6 = 36. This is smarter because every bundle already holds 10, so there is no need to count everything again.",
          "هنا 3 حزم و6 آحاد منفردة. لا نعدّ كل شيء. أولًا نعدّ العشرات: 3 عشرات = 30. ثم نعدّ الآحاد المنفردة: 6. ثم نجمع: 30 + 6 = 36. هذه الطريقة أذكى لأن كل حزمة فيها 10 أصلًا، فلا حاجة لإعادة العدّ من البداية.",
          "Voici 3 paquets et 6 unités seules. On ne compte pas tout. D'abord les dizaines : 3 dizaines = 30. Puis les unités : 6. Puis on réunit : 30 + 6 = 36. C'est plus malin car chaque paquet contient déjà 10."),
        F("30 + 6 = 36"),
        T("Rule: first read the tens, then the ones, then build the number.",
          "القاعدة: نقرأ العشرات أولًا ثم الآحاد ثم نبني العدد.",
          "Règle : on lit les dizaines, puis les unités, puis on construit le nombre."),
    ]),
    ("Build a number from its numeral", "نبني عددًا من رمزه", "Construire un nombre à partir de son écriture", "93", [
        F("47"),
        T("Now the game is reversed: I give the numeral and you build the model. Look at the first digit of 47: it is 4, so we need 4 tens, 4 bundles. The second digit is 7, so we add 7 loose ones. Check: 4 tens = 40, 7 ones = 7, and 40 + 7 = 47. The model and the numeral match.",
          "الآن نعكس اللعبة: أعطيك الرمز وأنت تبني النموذج. انظر إلى الرقم الأول في 47: إنه 4، فنحتاج 4 عشرات أي 4 حزم. والرقم الثاني 7، فنضيف 7 آحاد منفردة. نتحقق: 4 عشرات = 40 و7 آحاد = 7 و40 + 7 = 47. النموذج والرمز متطابقان.",
          "Maintenant on inverse : je donne l'écriture, tu construis le modèle. Le premier chiffre de 47 est 4 : il faut 4 dizaines, 4 paquets. Le second est 7 : on ajoute 7 unités seules. Vérification : 4 dizaines = 40, 7 unités = 7, 40 + 7 = 47. Le modèle et l'écriture correspondent."),
        tens(4, 7, eq=True),
    ]),
    ("A whole ten has zero loose ones", "العشرة الكاملة لا آحاد معها", "Une dizaine entière n'a aucune unité seule", "93", [
        tens(6, 0, eq=True),
        T("Here are 6 tens and not a single loose one. The number is 60. Why is the last digit 0? Because there are no loose ones. 60 = 6 tens + 0 ones. In the same way 20 = 2 tens + 0 ones and 40 = 4 tens + 0 ones. The zero is not decoration: it tells us there are no extra ones after the full tens.",
          "هنا 6 عشرات ولا واحد منفرد. العدد 60. لماذا الرقم الأخير 0؟ لأنه لا آحاد منفردة. 60 = 6 عشرات + 0 آحاد. وكذلك 20 = عشرتان + 0 آحاد و40 = 4 عشرات + 0 آحاد. الصفر ليس للزينة، بل يخبرنا أنه لا توجد آحاد زائدة بعد العشرات الكاملة.",
          "Voici 6 dizaines et aucune unité seule. Le nombre est 60. Pourquoi le dernier chiffre est 0 ? Parce qu'il n'y a pas d'unités seules. 60 = 6 dizaines + 0 unité. De même 20 = 2 dizaines + 0 unité. Le zéro n'est pas une décoration : il dit qu'il n'y a pas d'unités en plus."),
        F("60 = 6 tens + 0 ones"),
    ]),
    ("Same tens, different ones", "عشرات متساوية وآحاد مختلفة", "Mêmes dizaines, unités différentes", "94", [
        tens(4, 2, eq=True),
        tens(4, 7, eq=True),
        T("Look at 42 and 47. What is the same? 4 tens. What is different? The ones: 42 has 2 ones and 47 has 7. So both are in the forties. Step by step: 40, 41, 42, 43, 44, 45, 46, 47, 48, 49 all have 4 tens; only the number of ones changes.",
          "انظر إلى 42 و47. ما المتشابه؟ 4 عشرات. وما المختلف؟ الآحاد: في 42 اثنان وفي 47 سبعة. فكلاهما في الأربعينات. خطوة خطوة: 40 و41 و42 و43 و44 و45 و46 و47 و48 و49 كلها فيها 4 عشرات، والذي يتغير هو عدد الآحاد فقط.",
          "Regarde 42 et 47. Qu'est-ce qui est pareil ? 4 dizaines. Qu'est-ce qui change ? Les unités : 2 pour 42, 7 pour 47. Les deux sont dans les quarante. 40, 41, 42 … 49 ont tous 4 dizaines ; seul le nombre d'unités change."),
    ]),
    ("The model must match the number exactly", "يجب أن يطابق النموذج العدد تمامًا", "Le modèle doit correspondre exactement au nombre", "94", [
        tens(5, 4, eq=True),
        tens(5, 3, eq=True),
        T("Is 5 tens and 4 ones a correct model for 54? Yes. Now the picture shows 5 tens and 3 ones, but the label still says 54. Is it still 54? No, there are only 3 ones. 5 tens + 3 ones = 53, not 54. The picture and the number must agree exactly.",
          "هل 5 عشرات و4 آحاد نموذج صحيح للعدد 54؟ نعم. الآن تُظهر الصورة 5 عشرات و3 آحاد لكن البطاقة ما زالت تقول 54. هل ما زالت 54؟ لا، فيها 3 آحاد فقط. 5 عشرات + 3 آحاد = 53 لا 54. يجب أن تتفق الصورة والعدد تمامًا.",
          "5 dizaines et 4 unités, est-ce un bon modèle de 54 ? Oui. Maintenant l'image montre 5 dizaines et 3 unités mais l'étiquette dit encore 54. C'est faux : 5 dizaines + 3 unités = 53. L'image et le nombre doivent correspondre exactement."),
    ]),
    ("Three ways to see one number", "ثلاث طرق لرؤية العدد نفسه", "Trois façons de voir un même nombre", "95", [
        tens(3, 6, eq=True),
        F("36 = 3 tens + 6 ones = 30 + 6"),
        T("We can see the same number in three ways: the numeral 36, tens and ones (3 tens + 6 ones), and the expanded meaning 30 + 6. They are not three different numbers; they all speak about the same quantity. If you can move between the three, you understand the number and have not just memorised it.",
          "نستطيع أن نرى العدد نفسه بثلاث طرق: الرمز 36، والعشرات والآحاد (3 عشرات + 6 آحاد)، والمعنى المفكوك 30 + 6. ليست ثلاثة أعداد مختلفة، فكلها تتحدث عن الكمية نفسها. إذا استطعت الانتقال بينها فقد فهمت العدد ولم تحفظه فقط.",
          "On peut voir le même nombre de trois façons : l'écriture 36, dizaines et unités (3 dizaines + 6 unités), et le sens développé 30 + 6. Ce ne sont pas trois nombres différents : tous parlent de la même quantité. Si tu passes de l'un à l'autre, tu as compris le nombre."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Today we read numbers up to 69 the smart way. We do not count everything from one. We ask: how many tens? how many ones? For example 43 = 4 tens + 3 ones, 58 = 5 tens + 8 ones, 60 = 6 tens + 0 ones, 69 = 6 tens + 9 ones. And the model and the numeral must always match exactly.",
          "اليوم قرأنا الأعداد حتى 69 بطريقة ذكية. لا نعدّ كل شيء من الواحد، بل نسأل: كم عشرة؟ وكم واحدًا؟ مثلًا 43 = 4 عشرات + 3 آحاد و58 = 5 عشرات + 8 آحاد و60 = 6 عشرات + 0 آحاد و69 = 6 عشرات + 9 آحاد. ويجب أن يطابق النموذج العدد دائمًا تمامًا.",
          "Aujourd'hui on a lu les nombres jusqu'à 69 intelligemment. On ne compte pas tout depuis un : combien de dizaines ? combien d'unités ? Par exemple 43 = 4 dizaines + 3 unités, 58 = 5 + 8, 60 = 6 + 0, 69 = 6 + 9. Le modèle et l'écriture doivent toujours correspondre exactement."),
        F("SEE THE TENS → COUNT THE ONES → BUILD OR READ THE NUMBER → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "92", st("Read the model: 5 tens and 2 ones.", "اقرأ النموذج: 5 عشرات وآحادان.", "Lis le modèle : 5 dizaines et 2 unités."), [
        tens(5, 2, eq=True),
        T("Do not say the number at once. How many tens? 5 tens = 50. How many ones? 2. 50 + 2 = 52, so 52 = 5 tens + 2 ones.",
          "لا تقل العدد فورًا. كم عشرة؟ 5 عشرات = 50. وكم واحدًا؟ 2. 50 + 2 = 52، إذن 52 = 5 عشرات + آحادان.",
          "Ne dis pas le nombre tout de suite. Combien de dizaines ? 5 = 50. Combien d'unités ? 2. 50 + 2 = 52."),
    ]),
    EX("2", "93", st("Build 58.", "ابنِ العدد 58.", "Construis 58."), [
        tens(5, 8, eq=True),
        T("Look at 58: the 5 means 5 tens, so build 5 bundles first. Then add 8 loose ones. Check: 50 + 8 = 58.",
          "انظر إلى 58: الرقم 5 يعني 5 عشرات، فنبني 5 حزم أولًا ثم نضيف 8 آحاد منفردة. نتحقق: 50 + 8 = 58.",
          "Regarde 58 : le 5 veut dire 5 dizaines, on construit d'abord 5 paquets, puis 8 unités. Vérification : 50 + 8 = 58."),
    ]),
    EX("3", "93", st("Which numbers are whole tens: 30, 34, 50, 59?", "أي الأعداد عشرات كاملة: 30 و34 و50 و59؟", "Quels nombres sont des dizaines entières : 30, 34, 50, 59 ?"), [
        F("30 = 3 tens + 0 ones      50 = 5 tens + 0 ones"),
        T("30 and 50 are whole tens because their ones digit is 0. 34 has 4 ones and 59 has 9 ones.",
          "30 و50 عشرات كاملة لأن رقم الآحاد فيهما 0. أما 34 ففيها 4 آحاد و59 فيها 9 آحاد.",
          "30 et 50 sont des dizaines entières car le chiffre des unités est 0. 34 a 4 unités et 59 a 9 unités."),
    ]),
    EX("4", "94", st("Complete the model: the target is 65 and 6 tens are ready.", "أكمل النموذج: الهدف 65 والعشرات الست جاهزة.", "Complète le modèle : la cible est 65 et 6 dizaines sont prêtes."), [
        tens(6, 5, eq=True),
        T("The second digit of 65 is 5, so we need 5 loose ones. Check: 60 + 5 = 65.",
          "الرقم الثاني في 65 هو 5، فنحتاج 5 آحاد منفردة. نتحقق: 60 + 5 = 65.",
          "Le second chiffre de 65 est 5 : il faut 5 unités seules. Vérification : 60 + 5 = 65."),
    ]),
    EX("5", "94", st("Error detective: the model has 6 tens and 8 ones, the label says 67.", "المحقق: النموذج فيه 6 عشرات و8 آحاد والبطاقة تقول 67.", "Détective : le modèle a 6 dizaines et 8 unités, l'étiquette dit 67."), [
        tens(6, 8, eq=True),
        T("Read the model, not the label. 6 tens = 60 and there are 8 ones, so the correct number is 68. The label 67 is wrong.",
          "نقرأ النموذج لا البطاقة. 6 عشرات = 60 وفيه 8 آحاد، فالعدد الصحيح 68. والبطاقة 67 خطأ.",
          "Lis le modèle, pas l'étiquette. 6 dizaines = 60 et 8 unités : le bon nombre est 68. L'étiquette 67 est fausse."),
    ]),
    EX("6", "95", st("Mixed practice: 2 tens + 4 ones; 5 tens + 1 one; 6 tens + 9 ones; build 32; build 60; 4 tens + 8 ones.", "تدريب مختلط: عشرتان + 4 آحاد؛ 5 عشرات + واحد؛ 6 عشرات + 9 آحاد؛ ابنِ 32؛ ابنِ 60؛ 4 عشرات + 8 آحاد.", "Pratique mixte : 2 dizaines + 4 unités ; 5 + 1 ; 6 + 9 ; construis 32 ; construis 60 ; 4 dizaines + 8 unités."), [
        F("20 + 4 = 24      50 + 1 = 51      60 + 9 = 69"),
        F("32 = 3 tens + 2 ones      60 = 6 tens + 0 ones      40 + 8 = 48"),
    ]),
    EX("7", "95", st("Challenge: 57 without its 7 ones. What is left?", "تحدٍّ: العدد 57 بعد إزالة آحاده السبعة. ماذا يبقى؟", "Défi : 57 sans ses 7 unités. Que reste-t-il ?"), [
        tens(5, 7, eq=True),
        tens(5, 0, eq=True),
        T("57 is 5 tens and 7 ones. Take away all 7 ones and 5 complete tens remain, which is 50.",
          "57 هي 5 عشرات و7 آحاد. نزيل الآحاد السبعة فتبقى 5 عشرات كاملة أي 50.",
          "57, c'est 5 dizaines et 7 unités. On enlève les 7 unités : il reste 5 dizaines entières, soit 50."),
    ]),
    EX("8", "95", st("Final check: build 26 and 43; read 5 tens + 6 ones; split 68; why does 60 have no loose ones; is 46 right for 4 tens + 5 ones; why is it 52 and not 25?", "تقييم أخير: ابنِ 26 و43؛ اقرأ 5 عشرات + 6 آحاد؛ حلّل 68؛ لماذا لا آحاد في 60؛ هل 46 صحيح لـ4 عشرات + 5 آحاد؛ ولماذا 52 لا 25؟", "Évaluation : construis 26 et 43 ; lis 5 dizaines + 6 unités ; décompose 68 ; pourquoi 60 n'a pas d'unités ; 46 est-il juste pour 4 dizaines + 5 unités ; pourquoi 52 et pas 25 ?"), [
        F("26 = 20 + 6      43 = 40 + 3      5 tens + 6 ones = 56      68 = 60 + 8"),
        T("60 has no loose ones because it is exactly 6 complete tens. 4 tens + 5 ones is 45, so 46 is wrong. A model with 5 tens and 2 ones is 52, not 25, because 5 tens are 50 and 2 ones are 2.",
          "في 60 لا آحاد منفردة لأنها 6 عشرات كاملة تمامًا. 4 عشرات + 5 آحاد = 45 فالعدد 46 خطأ. ونموذج فيه 5 عشرات وواحدان هو 52 لا 25 لأن 5 عشرات = 50 وواحدين = 2.",
          "60 n'a pas d'unités seules car c'est exactement 6 dizaines. 4 dizaines + 5 unités = 45, donc 46 est faux. 5 dizaines et 2 unités font 52 et non 25 : 5 dizaines = 50 et 2 unités = 2."),
    ]),
]
