"""Grade 1 Mathematics — The writing of 10."""
from scripts.direct_lessons.common import T, F, EX, st, tens, objects, numeral, scene, join

LESSON_ID = "G01-MATH-EN-023"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "The writing of 10", "ar": "كتابة العدد 10", "fr": "L'écriture de 10"}


def big(txt, tag="w"):
    return scene(numeral(txt, 330, 290, 220, tag), [tag])


THEORY = [
    ("Ten ones make one ten", "عشرة آحاد تصنع عشرة واحدة", "Dix unités font une dizaine", "62", [
        T("Hello! Today we make an important idea about the number 10 firm. You can write 10, but I want to be sure you are not only memorizing its shape. The number 10 can appear in more than one form, but the quantity does not change.",
          "مرحبًا! اليوم نثبّت فكرة مهمة عن العدد 10. أنت تعرف كتابة 10، لكنني أريد أن أتأكد أنك لا تحفظ شكله فقط. العدد 10 قد يظهر بأكثر من شكل لكن الكمية لا تتغير.",
          "Bonjour ! Aujourd'hui on fixe une idée importante sur le nombre 10. Tu sais écrire 10, mais je veux être sûr que tu ne retiens pas seulement sa forme. Le nombre 10 peut apparaître sous plusieurs formes, mais la quantité ne change pas."),
        objects(10, "circle", "#1e63d6", prefix="u", r=24),
        T("Count with me and touch each one once: one, two, three, four, five, six, seven, eight, nine, ten. We have ten ones.",
          "عدّ معي والمس كل واحد مرة واحدة: واحد، اثنان، ثلاثة، أربعة، خمسة، ستة، سبعة، ثمانية، تسعة، عشرة. عندنا عشرة آحاد.",
          "Compte avec moi en touchant chaque objet une fois : un, deux, trois, quatre, cinq, six, sept, huit, neuf, dix. On a dix unités."),
        tens(1, 0),
        T("Now we gathered the same sticks into one bundle. We did not add or remove anything. Did the quantity change? No. The shape changed, but the number stayed 10.",
          "الآن جمعنا العيدان نفسها في حزمة واحدة. لم نزد ولم نُنقص شيئًا. هل تغيّرت الكمية؟ لا. الشكل تغيّر لكن العدد بقي 10.",
          "On a réuni les mêmes bâtons en un paquet. On n'a rien ajouté ni enlevé. La quantité a-t-elle changé ? Non. La forme a changé, mais le nombre est resté 10."),
        F("10 ones = 1 ten"),
    ]),
    ("The numeral 10 has two digits", "العدد 10 فيه رقمان", "Le nombre 10 a deux chiffres", "62", [
        big("10"),
        T("This is the numeral 10. Look closely: it is not one digit. It has a 1 and after it a 0. But do not say one and zero separately. The whole number word is ten.",
          "هذا العدد 10. انظر جيدًا: ليس رقمًا واحدًا. فيه 1 وبعده 0. لكن لا تقل واحد وصفر منفصلين. كلمة العدد كلها هي عشرة.",
          "Voici le nombre 10. Regarde bien : ce n'est pas un seul chiffre. Il y a un 1 puis un 0. Mais ne dis pas un et zéro séparément. Le mot du nombre entier est dix."),
        objects(10, "circle", "#43a047", prefix="d", r=22),
        T("Why does this numeral stand for this group? Because when we count all the objects, we reach ten.",
          "لماذا يمثّل هذا العدد هذه المجموعة؟ لأننا عندما نعدّ كل الأشياء نصل إلى عشرة.",
          "Pourquoi ce nombre représente-t-il ce groupe ? Parce qu'en comptant tous les objets, on arrive à dix."),
    ]),
    ("Different pictures can still mean 10", "صور مختلفة قد تعني 10", "Des images différentes peuvent signifier 10", "63", [
        tens(1, 0),
        objects(10, "square", "#fb8c00", prefix="s", r=22),
        T("Three pictures look different: a full ten-frame, one bundle of ten, and ten counters spread out. Can all of them mean 10? We do not rely on the look. We need proof: count the first, open the bundle in the mind to find ten ones, count the third. All three give ten.",
          "ثلاث صور تبدو مختلفة: إطار عشرة ممتلئ وحزمة عشرة واحدة وعشرة عدّادات موزّعة. هل تعني كلها 10؟ لا نعتمد على المظهر بل نحتاج دليلًا: نعدّ الأولى، ونفتح الحزمة في الذهن فنجد عشرة آحاد، ونعدّ الثالثة. الثلاث تعطي عشرة.",
          "Trois images paraissent différentes : un cadre de dix plein, un paquet de dix et dix jetons dispersés. Toutes peuvent-elles signifier 10 ? On ne se fie pas à l'aspect. Il faut une preuve : compter la première, ouvrir le paquet dans la tête pour trouver dix unités, compter la troisième. Les trois donnent dix."),
        T("The representation can change. The quantity stays the same if there are ten objects.",
          "التمثيل قد يتغيّر. والكمية تبقى نفسها إذا كانت الأشياء عشرة.",
          "La représentation peut changer. La quantité reste la même s'il y a dix objets."),
    ]),
    ("Write 10 after you know its meaning", "نكتب 10 بعد أن نعرف معناه", "Écrire 10 après avoir compris son sens", "63", [
        scene('<text id="d" x="330" y="290" font-size="220" font-weight="700" text-anchor="middle" fill="none" stroke="#0b3d5c" stroke-dasharray="10 8" stroke-width="4" font-family="sans-serif">10</text>', ["d"]),
        T("We know the meaning before the writing. Start with the 1, then write 0 to the right of it. Read what you wrote: ten. Now check with the quantity: does the numeral 10 match ten dots? Yes.",
          "عرفنا المعنى قبل الخط. ابدأ بالـ1 ثم اكتب 0 على يمينه. اقرأ ما كتبته: عشرة. الآن نتحقق بالكمية: هل العدد 10 يطابق عشر نقاط؟ نعم.",
          "On connaît le sens avant l'écriture. Commence par le 1 puis écris 0 à sa droite. Lis ce que tu as écrit : dix. Vérifie avec la quantité : le nombre 10 correspond-il à dix points ? Oui."),
        objects(10, "circle", "#e53935", prefix="q", r=22),
    ]),
    ("Break 10 apart and put it back together", "نفكّك 10 ونعيد جمعها", "Décomposer 10 puis le recomposer", "63", [
        join(6, 4, "circle", "circle", "#1e63d6", "#e53935"),
        T("We have ten all together. Now we split them into two groups: A has 6, B has 4. Did the total disappear? No. We put them back together and count: ten.",
          "عندنا عشرة معًا. الآن نقسمها إلى مجموعتين: A فيها 6 وB فيها 4. هل اختفى المجموع؟ لا. نعيد جمعها ونعدّ: عشرة.",
          "On a dix en tout. On les sépare en deux groupes : A en a 6, B en a 4. Le total a-t-il disparu ? Non. On les réunit et on compte : dix."),
        T("Today we do not have to memorize every split. We only need to understand that the same ten can be split in more than one way.",
          "اليوم لا يلزم أن نحفظ كل التفكيكات. المطلوب أن نفهم أن العشرة نفسها تنقسم بأكثر من طريقة.",
          "Aujourd'hui, pas besoin de retenir toutes les décompositions. Il faut comprendre que le même dix peut se partager de plusieurs façons."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Today we made the meaning of 10 firm. 10 can be ten ones, one bundle of ten, a full ten-frame, or the numeral 10. The look can change, but if the quantity is ten, the number is the same. And to write ten: 1 then 0.",
          "اليوم ثبّتنا معنى 10. قد يكون عشرة آحاد أو حزمة عشرة أو إطار عشرة ممتلئًا أو العدد 10. الشكل قد يتغيّر لكن إذا كانت الكمية عشرة فالعدد نفسه. ولكتابة عشرة: 1 ثم 0.",
          "Aujourd'hui on a fixé le sens de 10. Ce peut être dix unités, un paquet de dix, un cadre de dix plein ou le nombre 10. L'aspect change, mais si la quantité est dix, le nombre est le même. Pour écrire dix : 1 puis 0."),
        F("SEE THE REPRESENTATION → COUNT OR UNBUNDLE → CONFIRM TEN → READ / WRITE 10 → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "62", st("Build a collection of 10, then check by counting.", "كوّن مجموعة من 10 ثم تحقّق بالعدّ.", "Fais une collection de 10 puis vérifie en comptant."), [
        objects(10, "circle", "#1e63d6", prefix="b", r=24),
        T("One, two, three, four, five, six, seven, eight, nine, ten. Each object once, and the last number is ten.",
          "واحد، اثنان، ثلاثة، أربعة، خمسة، ستة، سبعة، ثمانية، تسعة، عشرة. كل شيء مرة واحدة وآخر عدد عشرة.",
          "Un, deux, trois, quatre, cinq, six, sept, huit, neuf, dix. Chaque objet une fois, et le dernier nombre est dix."),
    ]),
    EX("2", "63", st("Match the numeral 10 with the right group: 8, 10 or 9 objects.", "طابق العدد 10 مع المجموعة الصحيحة: 8 أو 10 أو 9 أشياء.", "Associe le nombre 10 au bon groupe : 8, 10 ou 9 objets."), [
        objects(8, "circle", "#e53935", prefix="a", r=22),
        objects(10, "circle", "#43a047", prefix="b", r=22),
        objects(9, "circle", "#fb8c00", prefix="c", r=22),
        T("Do not choose by the shape of the group. Count each one. The right group is the one whose last counting word is ten.",
          "لا نختار من شكل المجموعة. نعدّ كل واحدة. المجموعة الصحيحة هي التي آخر كلمة عدّ فيها عشرة.",
          "Ne choisis pas d'après l'aspect. Compte chaque groupe. Le bon groupe est celui dont le dernier mot de comptage est dix."),
    ]),
    EX("3", "63", st("Select all the representations of 10: 10 counters, 9 counters, one ten bundle, the numeral 10, 8 counters.", "اختر كل تمثيلات 10: 10 عدّادات، 9 عدّادات، حزمة عشرة، العدد 10، 8 عدّادات.", "Choisis toutes les représentations de 10 : 10 jetons, 9 jetons, un paquet de dix, le nombre 10, 8 jetons."), [
        objects(10, "circle", "#1e63d6", prefix="a", r=22),
        tens(1, 0),
        big("10"),
        T("Three different pictures, the same number. The 9 and the 8 are not ten: we check by counting instead of guessing.",
          "ثلاث صور مختلفة والعدد نفسه. التسعة والثمانية ليستا عشرة: نتحقق بالعدّ بدل التخمين.",
          "Trois images différentes, le même nombre. 9 et 8 ne font pas dix : on vérifie en comptant au lieu de deviner."),
    ]),
    EX("4", "63", st("Write the numeral ten, then build 10 objects to prove you know what you wrote.", "اكتب العدد عشرة ثم ابنِ 10 أشياء لتثبت أنك تعرف ما كتبته.", "Écris le nombre dix puis construis 10 objets pour prouver que tu sais ce que tu as écrit."), [
        big("10"),
        objects(10, "circle", "#e53935", prefix="c", r=22),
        T("If you wrote 01, the digits are in the wrong order: ten is 1 then 0. If you wrote only 1, that is the numeral one; ten needs another digit.",
          "إذا كتبت 01 فترتيب الرقمين خاطئ: عشرة هي 1 ثم 0. وإذا كتبت 1 فقط فهذا العدد واحد، وللعشرة رقم آخر.",
          "Si tu as écrit 01, l'ordre est faux : dix, c'est 1 puis 0. Si tu as écrit seulement 1, c'est le nombre un ; dix a un autre chiffre."),
    ]),
    EX("5", "63", st("Scene A: 5 + 5. Scene B: 7 + 3. Do they have the same total?", "المشهد A: 5 + 5. المشهد B: 7 + 3. هل لهما المجموع نفسه؟", "Scène A : 5 + 5. Scène B : 7 + 3. Ont-elles le même total ?"), [
        join(5, 5, "circle", "circle", "#1e63d6", "#e53935", total=False),
        join(7, 3, "circle", "circle", "#1e63d6", "#e53935", total=False),
        T("Do not decide from the shape of the parts. Count each scene: ten and ten. Different parts, the same total.",
          "لا نقرر من شكل الأجزاء. نعدّ كل مشهد: عشرة وعشرة. أجزاء مختلفة والمجموع نفسه.",
          "Ne décide pas d'après la forme des parties. Compte chaque scène : dix et dix. Parties différentes, même total."),
        F("5 + 5 = 10      7 + 3 = 10"),
    ]),
    EX("6", "63", st("Error detective: the numeral says 10, but the picture shows 9 counters.", "المحقق: العدد المكتوب 10 لكن الصورة فيها 9 عدّادات.", "Détective : le nombre écrit est 10, mais l'image montre 9 jetons."), [
        objects(9, "circle", "#fb8c00", prefix="e", r=22),
        T("Count: nine. The picture does not show ten. What can we do to make the numeral 10 correct? Add one object.",
          "نعدّ: تسعة. الصورة لا تُظهر عشرة. ماذا نفعل ليصبح العدد 10 صحيحًا؟ نضيف شيئًا واحدًا.",
          "On compte : neuf. L'image ne montre pas dix. Que faire pour que le nombre 10 soit juste ? Ajouter un objet."),
        objects(10, "circle", "#fb8c00", prefix="f", r=22),
    ]),
    EX("7", "63", st("Challenge: Box A has one ten bundle. Box B has 10 loose counters. Which has more?", "تحدٍّ: الصندوق A فيه حزمة عشرة. الصندوق B فيه 10 عدّادات منفردة. أيهما أكثر؟", "Défi : la boîte A contient un paquet de dix. La boîte B contient 10 jetons seuls. Laquelle en a plus ?"), [
        tens(1, 0),
        objects(10, "circle", "#1e63d6", prefix="g", r=22),
        T("Open the bundle in your mind: ten ones. Both boxes have the same quantity: 10. The way of showing did not fool you.",
          "افتح الحزمة في ذهنك: عشرة آحاد. في الصندوقين الكمية نفسها: 10. طريقة العرض لم تخدعك.",
          "Ouvre le paquet dans ta tête : dix unités. Les deux boîtes ont la même quantité : 10. La façon de montrer ne t'a pas trompé."),
    ]),
    EX("8", "63", st("Final check: build 10, read it, write it, and explain why a bundle and 10 loose objects mean the same number.", "تقييم أخير: ابنِ 10 واقرأها واكتبها واشرح لماذا الحزمة و10 أشياء منفردة تعنيان العدد نفسه.", "Évaluation : construis 10, lis-le, écris-le et explique pourquoi un paquet et 10 objets seuls veulent dire le même nombre."), [
        objects(10, "circle", "#43a047", prefix="h", r=22),
        big("10"),
        T("Read: ten. Write: 10. Explain: because the bundle has ten ones, and if we count everything we reach 10.",
          "نقرأ: عشرة. نكتب: 10. نشرح: لأن الحزمة فيها عشرة آحاد، وإذا عددنا الكل نصل إلى 10.",
          "On lit : dix. On écrit : 10. On explique : le paquet contient dix unités, et si on compte tout on arrive à 10."),
    ]),
]
