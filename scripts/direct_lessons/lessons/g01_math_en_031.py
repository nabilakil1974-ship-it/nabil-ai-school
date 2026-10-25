"""Grade 1 Mathematics — Add on the number line."""
from scripts.direct_lessons.common import T, F, EX, st, jumps

LESSON_ID = "G01-MATH-EN-031"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Add on the number line", "ar": "الجمع على خط الأعداد", "fr": "Additionner sur la droite des nombres"}

THEORY = [
    ("Find the starting number first", "نحدّد عدد البداية أولًا", "Trouver d'abord le nombre de départ", "82", [
        T("Hello! Today we make addition walk in front of our eyes. We have a number line, and a marker that moves step by step. Today's rule is simple: when we add, we start from the first number and walk forward by as many jumps as the second number.",
          "مرحبًا! اليوم نجعل الجمع يمشي أمام أعيننا. عندنا خط أعداد وعلامة تتحرك خطوة خطوة. قاعدة اليوم بسيطة: عندما نجمع نبدأ من العدد الأول ونمشي إلى الأمام بعدد قفزات يساوي العدد الثاني.",
          "Bonjour ! Aujourd'hui l'addition marche sous nos yeux. On a une droite des nombres et un repère qui avance pas à pas. La règle du jour est simple : quand on ajoute, on part du premier nombre et on avance d'autant de sauts que le second nombre."),
        jumps(4, 0, label=False),
        T("Before any jump, I must know where I start. If the question is 4 + 2, where do I put the marker first? On 4. The first number is the start. We do not count 4 as a jump; it is the starting point.",
          "قبل أي قفزة يجب أن أعرف من أين أبدأ. إذا كان السؤال 4 + 2 فأين أضع العلامة أولًا؟ على 4. العدد الأول هو البداية. لا نعدّ 4 قفزة، بل هي نقطة البداية.",
          "Avant tout saut, je dois savoir d'où je pars. Si la question est 4 + 2, où pose-t-on le repère d'abord ? Sur 4. Le premier nombre est le départ. On ne compte pas 4 comme un saut : c'est le point de départ."),
    ]),
    ("Each unit jump moves one number forward", "كل قفزة وحدة تتحرك عددًا واحدًا", "Chaque saut avance d'un nombre", "82", [
        jumps(4, 2),
        T("From 4 we add 2: two unit jumps forward. Jump one: 4 to 5. Jump two: 5 to 6. Where did we land? On 6. So 4 + 2 = 6. We started at 4, made 2 jumps, and the landing point was 6.",
          "من 4 نضيف 2: قفزتان وحدتان إلى الأمام. القفزة الأولى: من 4 إلى 5. والثانية: من 5 إلى 6. أين وصلنا؟ إلى 6. إذن 4 + 2 = 6. بدأنا من 4 وقفزنا قفزتين وكانت نقطة الهبوط 6.",
          "De 4 on ajoute 2 : deux sauts d'une unité en avant. Premier saut : de 4 à 5. Deuxième : de 5 à 6. Où a-t-on atterri ? Sur 6. Donc 4 + 2 = 6. On est parti de 4, on a fait 2 sauts et l'atterrissage était 6."),
    ]),
    ("Addition moves forward, not backward", "الجمع يتحرك إلى الأمام لا إلى الخلف", "L'addition avance, elle ne recule pas", "83", [
        jumps(6, 2),
        T("When we add, which direction do we go? Forward, to the right, where the numbers increase. Addition here makes the number bigger. For 6 + 2 we walk 6, 7, 8, not 6, 5, 4.",
          "عندما نجمع إلى أي اتجاه نسير؟ إلى الأمام، نحو اليمين، حيث تزيد الأعداد. الجمع هنا يزيد العدد. في 6 + 2 نمشي 6، 7، 8 لا 6، 5، 4.",
          "Quand on ajoute, dans quel sens va-t-on ? En avant, vers la droite, où les nombres augmentent. Ici l'addition agrandit le nombre. Pour 6 + 2 on marche 6, 7, 8, pas 6, 5, 4."),
    ]),
    ("The landing number is the sum", "نقطة الهبوط هي المجموع", "Le point d'atterrissage est la somme", "83", [
        jumps(2, 3),
        T("After the jumps, we do not count again from the beginning. The point we reached is the sum. For 2 + 3 we go 2, 3, 4, 5. The landing is 5, so the sum is 5.",
          "بعد القفزات لا نعيد العدّ من جديد. النقطة التي وصلنا إليها هي المجموع. في 2 + 3 نمشي 2، 3، 4، 5. الهبوط عند 5، إذن المجموع 5.",
          "Après les sauts, on ne recompte pas depuis le début. Le point atteint est la somme. Pour 2 + 3 on va 2, 3, 4, 5. L'atterrissage est 5, la somme est donc 5."),
    ]),
    ("The equation and the action must match", "المعادلة والحركة يجب أن تتطابقا", "L'égalité et le mouvement doivent correspondre", "83", [
        T("Every equation has a story on the number line: the first number is the start, the second number is the number of jumps, and the answer is the landing. If the picture does not match these three, there is a mistake.",
          "لكل معادلة قصة على خط الأعداد: العدد الأول هو البداية، والعدد الثاني هو عدد القفزات، والجواب هو الهبوط. إذا لم تطابق الصورة هذه الثلاثة ففي الأمر خطأ.",
          "Chaque égalité a une histoire sur la droite : le premier nombre est le départ, le second est le nombre de sauts, la réponse est l'atterrissage. Si l'image ne correspond pas à ces trois choses, il y a une erreur."),
        F("START → JUMPS → LAND"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Addition on the number line: start at the first number, move forward, count the jumps as the second number, land on the sum, and check that the equation and the picture agree.",
          "الجمع على خط الأعداد: نبدأ من العدد الأول، ونتحرك إلى الأمام، ونعدّ القفزات بعدد العدد الثاني، ونهبط عند المجموع، ونتحقق أن المعادلة والصورة متفقتان.",
          "Additionner sur la droite : partir du premier nombre, avancer, compter les sauts comme le second nombre, atterrir sur la somme et vérifier que l'égalité et l'image s'accordent."),
        F("START → FORWARD JUMPS → LAND → SUM → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "82", st("Choose the start for 5 + 3.", "اختر نقطة البداية في 5 + 3.", "Choisis le départ pour 5 + 3."), [
        jumps(5, 0, label=False),
        T("Look at the first number, before the plus sign. We start at 5.",
          "انظر إلى العدد الأول قبل علامة +. نبدأ من 5.",
          "Regarde le premier nombre, avant le signe plus. On part de 5."),
    ]),
    EX("2", "82", st("Make the jumps for 3 + 4.", "اصنع القفزات لـ 3 + 4.", "Fais les sauts pour 3 + 4."), [
        jumps(3, 4),
        T("Start: 3. Jumps: 4. We go 3, 4, 5, 6, 7. The landing is 7, so 3 + 4 = 7. Do not count the starting point as a jump. The first jump begins when we leave 3 and reach 4.",
          "البداية: 3. القفزات: 4. نمشي 3، 4، 5، 6، 7. الهبوط عند 7، إذن 3 + 4 = 7. لا نعدّ نقطة البداية قفزة. القفزة الأولى تبدأ عندما نترك 3 ونصل إلى 4.",
          "Départ : 3. Sauts : 4. On va 3, 4, 5, 6, 7. L'atterrissage est 7, donc 3 + 4 = 7. Ne compte pas le départ comme un saut. Le premier saut commence quand on quitte 3 pour arriver à 4."),
    ]),
    EX("3", "83", st("Two pictures for 5 + 2: A goes 5, 6, 7. B goes 5, 4, 3. Which one shows addition?", "صورتان لـ 5 + 2: A تمشي 5، 6، 7. وB تمشي 5، 4، 3. أيهما تمثّل الجمع؟", "Deux images pour 5 + 2 : A va 5, 6, 7. B va 5, 4, 3. Laquelle montre l'addition ?"), [
        jumps(5, 2),
        jumps(5, 2, back=True, label=False),
        T("A, because addition moves forward.",
          "A، لأن الجمع يتحرك إلى الأمام.",
          "A, car l'addition avance."),
    ]),
    EX("4", "83", st("The marker starts at 7, makes 2 forward jumps and lands on 9. Write the addition.", "تبدأ العلامة من 7 وتقفز قفزتين إلى الأمام وتهبط عند 9. اكتب الجمع.", "Le repère part de 7, fait 2 sauts en avant et atterrit sur 9. Écris l'addition."), [
        jumps(7, 2),
        T("Where is the start? 7. How many jumps? 2. Where is the landing? 9.",
          "أين البداية؟ 7. كم قفزة؟ 2. أين الهبوط؟ 9.",
          "Où est le départ ? 7. Combien de sauts ? 2. Où est l'atterrissage ? 9."),
        F("7 + 2 = 9"),
    ]),
    EX("5", "83", st("Error detective: the claim is 4 + 3 = 6, but the picture goes 4, 5, 6, 7.", "المحقق: الادعاء 4 + 3 = 6 لكن الصورة تمشي 4، 5، 6، 7.", "Détective : l'affirmation est 4 + 3 = 6, mais l'image va 4, 5, 6, 7."), [
        jumps(4, 3),
        T("The written answer is wrong, not the picture. Three jumps from 4 land on 7.",
          "الجواب المكتوب هو الخاطئ لا الصورة. ثلاث قفزات من 4 تهبط عند 7.",
          "La réponse écrite est fausse, pas l'image. Trois sauts depuis 4 atterrissent sur 7."),
        F("4 + 3 = 7"),
    ]),
    EX("6", "83", st("Mixed practice: 2 + 4, 6 + 3, picture 3 → 5, and start 8 with one jump.", "تدريب مختلط: 2 + 4، 6 + 3، صورة 3 ← 5، والبداية 8 مع قفزة واحدة.", "Exercice mixte : 2 + 4, 6 + 3, image 3 → 5, et départ 8 avec un saut."), [
        jumps(2, 4),
        jumps(6, 3),
        jumps(3, 2),
        jumps(8, 1),
        T("Each time: start, jumps, land.",
          "في كل مرة: بداية، قفزات، هبوط.",
          "Chaque fois : départ, sauts, atterrissage."),
    ]),
    EX("7", "83", st("Challenge: the marker starts at 5 and ends at 9. How many forward jumps did it make?", "تحدٍّ: بدأت العلامة عند 5 وانتهت عند 9. كم قفزة إلى الأمام قامت بها؟", "Défi : le repère part de 5 et finit à 9. Combien de sauts en avant a-t-il faits ?"), [
        jumps(5, 4),
        T("Count the moves: 5 to 6, 6 to 7, 7 to 8, 8 to 9. Four jumps. So 5 + 4 = 9. This time you found the second number from the movement.",
          "نعدّ الحركات: من 5 إلى 6، ومن 6 إلى 7، ومن 7 إلى 8، ومن 8 إلى 9. أربع قفزات. إذن 5 + 4 = 9. هذه المرة استنتجت العدد الثاني من الحركة.",
          "On compte les déplacements : 5 à 6, 6 à 7, 7 à 8, 8 à 9. Quatre sauts. Donc 5 + 4 = 9. Cette fois tu as trouvé le second nombre grâce au mouvement."),
    ]),
    EX("8", "83", st("Final check: show 4 + 2 and 5 + 3; write the equation for start 3 and two jumps; explain why the landing point is the sum.", "تقييم أخير: مثّل 4 + 2 و5 + 3؛ اكتب المعادلة للبداية 3 وقفزتين؛ واشرح لماذا نقطة الهبوط هي المجموع.", "Évaluation : montre 4 + 2 et 5 + 3 ; écris l'égalité pour le départ 3 et deux sauts ; explique pourquoi l'atterrissage est la somme."), [
        jumps(4, 2),
        jumps(5, 3),
        jumps(3, 2),
        T("Because after starting at the first number and adding the second number of jumps, the place where we stop shows how many there are altogether.",
          "لأننا بعد أن نبدأ من العدد الأول ونضيف عدد القفزات المطلوب فإن المكان الذي نتوقف عنده يُظهر العدد الكلي.",
          "Parce qu'après être parti du premier nombre et avoir fait autant de sauts que le second, l'endroit où l'on s'arrête montre combien il y en a en tout."),
    ]),
]
