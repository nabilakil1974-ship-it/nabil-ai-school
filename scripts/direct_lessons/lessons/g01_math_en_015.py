"""Grade 1 Mathematics — Comparing numbers up to 9."""
from scripts.direct_lessons.common import T, F, EX, st, pairs, numpath, objects

LESSON_ID = "G01-MATH-EN-015"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Comparing numbers up to 9", "ar": "مقارنة الأعداد حتى 9", "fr": "Comparer les nombres jusqu'à 9"}
P = list("123456789")


def pr(a, b, g=62):
    return pairs(a, b, "circle", "circle", "#e53935", "#1e63d6", gap=g, r=18)


THEORY = [
    ("A number represents a quantity", "العدد يمثّل كمية", "Un nombre représente une quantité", "44", [
        T("Hello! We already know how to compare groups: more, fewer, same. Today we compare the numbers themselves. Which is the bigger number, 7 or 5? Before we answer, we want a proof, because a number is a symbol for a quantity.",
          "مرحبًا! صرنا نعرف مقارنة المجموعات: أكثر وأقل ومثل. اليوم نقارن الأعداد نفسها. أيهما العدد الأكبر، 7 أم 5؟ قبل الجواب نريد دليلًا، لأن العدد رمز لكمية.",
          "Bonjour ! On sait comparer des groupes : plus, moins, pareil. Aujourd'hui on compare les nombres eux-mêmes. Quel est le plus grand, 7 ou 5 ? Avant de répondre, on veut une preuve, car un nombre est le symbole d'une quantité."),
        pr(7, 5),
        T("We build 7 and we build 5, then we pair. After five pairs, two are left from the group of 7. So 7 stands for more objects than 5.",
          "نبني 7 ونبني 5 ثم نُقرن. بعد خمسة أزواج يبقى اثنان من مجموعة 7. إذن 7 تمثّل أشياء أكثر من 5.",
          "On construit 7 et 5, puis on apparie. Après cinq paires, il en reste deux dans le groupe de 7. Donc 7 représente plus d'objets que 5."),
        F("7 is greater than 5      5 is smaller than 7"),
    ]),
    ("Use the number path", "نستعمل مسار الأعداد", "Utiliser la droite des nombres", "44", [
        numpath(P, hi=3),
        T("There is another way. Put a finger on 4 and an eye on 8. Which one comes later when we count? 8. A number farther forward stands for a greater quantity.",
          "هناك طريقة أخرى. ضع إصبعك على 4 وعينك على 8. أيهما يأتي لاحقًا في العدّ؟ 8. العدد الأبعد إلى الأمام يمثّل كمية أكبر.",
          "Il y a une autre façon. Pose un doigt sur 4 et l'œil sur 8. Lequel vient plus tard quand on compte ? 8. Un nombre plus avancé représente une plus grande quantité."),
        numpath(P, hi=7),
        F("8 is greater than 4"),
    ]),
    ("Equal numbers", "الأعداد المتساوية", "Les nombres égaux", "45", [
        pr(5, 5, 70),
        T("What if both cards show the same number? We build 5 and 5 and pair them. Nothing is left, so the quantities are equal: 5 and 5 are equal.",
          "ماذا لو أظهرت البطاقتان العدد نفسه؟ نبني 5 و5 ونُقرن. لا يبقى شيء، فالكميتان متساويتان: 5 و5 متساويان.",
          "Et si les deux cartes montrent le même nombre ? On construit 5 et 5 et on apparie. Il ne reste rien : les quantités sont égales. 5 et 5 sont égaux."),
        F("5 = 5"),
    ]),
    ("Don't compare the shape of the numerals", "لا نقارن شكل الأرقام", "Ne compare pas la forme des chiffres", "45", [
        numpath(["1", "8"]),
        T("Here the 1 is written big and the 8 is written small. Does that make 1 greater? No. The size of the writing does not decide the quantity. 1 means one object, and 8 means eight objects. So 8 is greater.",
          "هنا كُتب 1 بحجم كبير وكُتب 8 أصغر. هل هذا يجعل 1 أكبر؟ لا. حجم الكتابة لا يحدد الكمية. 1 تعني شيئًا واحدًا و8 تعني ثمانية أشياء. إذن 8 أكبر.",
          "Ici le 1 est écrit grand et le 8 petit. Cela rend-il 1 plus grand ? Non. La taille de l'écriture ne décide pas la quantité. 1 veut dire un objet, 8 veut dire huit objets. Donc 8 est plus grand."),
    ]),
    ("Two ways to prove", "طريقتان للإثبات", "Deux façons de prouver", "45", [
        pr(6, 9, 62),
        T("Method one, quantities: build 6 and 9, and 9 has extra objects. Method two, number path: 6 comes before 9. The two ways agree.",
          "الطريقة الأولى، الكميات: نبني 6 و9 فتزيد أشياء في 9. الطريقة الثانية، مسار الأعداد: 6 تأتي قبل 9. الطريقتان متفقتان.",
          "Première façon, les quantités : on construit 6 et 9, et 9 a des objets en trop. Deuxième façon, la droite : 6 vient avant 9. Les deux s'accordent."),
        numpath(P, hi=8),
        F("9 is greater than 6"),
    ]),
    ("Explain the comparison", "نشرح المقارنة", "Expliquer la comparaison", "45", [
        T("Which is greater, 8 or 5? 8. Now the reason: 8 represents more objects than 5, or 8 comes after 5 on the number path, or after pairing three are left from the group of 8. A good answer has the answer and the reason.",
          "أيهما أكبر، 8 أم 5؟ 8. الآن السبب: 8 تمثّل أشياء أكثر من 5، أو 8 تأتي بعد 5 على مسار الأعداد، أو بعد الإقران يبقى 3 من مجموعة 8. الجواب الجيد فيه الجواب والسبب.",
          "Lequel est plus grand, 8 ou 5 ? 8. Maintenant la raison : 8 représente plus d'objets que 5, ou 8 vient après 5 sur la droite, ou après appariement il en reste 3 dans le groupe de 8. Une bonne réponse a la réponse et la raison."),
        F("answer + reason"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("When we compare numbers, we do not compare their shapes. We compare the quantities they stand for. Greater means more quantity, smaller means fewer, and equal means the same quantity.",
          "عندما نقارن الأعداد لا نقارن أشكالها بل الكميات التي تمثّلها. الأكبر يعني كمية أكثر، والأصغر كمية أقل، والمتساوي كمية مماثلة.",
          "Quand on compare des nombres, on ne compare pas leur forme mais les quantités qu'ils représentent. Plus grand : plus de quantité. Plus petit : moins. Égal : la même quantité."),
        F("READ → BUILD OR LOCATE → COMPARE → SAY → PROVE → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "44", st("Build 6 and 4 with counters and compare them.", "ابنِ 6 و4 بالعدّادات وقارن.", "Construis 6 et 4 avec des jetons et compare."), [
        pr(6, 4),
        T("After pairing, extra objects are left in the group of 6. So 6 is greater and 4 is smaller.",
          "بعد الإقران تبقى أشياء زائدة في مجموعة 6. إذن 6 أكبر و4 أصغر.",
          "Après appariement, il reste des objets en trop dans le groupe de 6. Donc 6 est plus grand et 4 plus petit."),
        F("6 > 4"),
    ]),
    EX("2", "44", st("Compare 3 and 7 on the number path.", "قارن 3 و7 على مسار الأعداد.", "Compare 3 et 7 sur la droite des nombres."), [
        numpath(P, hi=2),
        numpath(P, hi=6),
        T("7 is farther forward, so 7 is greater than 3, and 3 is smaller than 7.",
          "7 أبعد إلى الأمام، إذن 7 أكبر من 3 و3 أصغر من 7.",
          "7 est plus avancé, donc 7 est plus grand que 3, et 3 est plus petit que 7."),
        F("7 > 3"),
    ]),
    EX("3", "45", st("Greater, smaller or equal? 8 and 6; 2 and 5; 7 and 7.", "أكبر أم أصغر أم يساوي؟ 8 و6؛ 2 و5؛ 7 و7.", "Plus grand, plus petit ou égal ? 8 et 6 ; 2 et 5 ; 7 et 7."), [
        F("8 > 6      2 < 5      7 = 7"),
        T("Each time, check with quantities or with the number path.",
          "في كل مرة نتحقق بالكميات أو بمسار الأعداد.",
          "Chaque fois, on vérifie avec les quantités ou la droite des nombres."),
    ]),
    EX("4", "45", st("A small 9 and a big 4. Which is greater mathematically?", "9 صغيرة و4 كبيرة. أيهما أكبر رياضيًا؟", "Un petit 9 et un grand 4. Lequel est plus grand en mathématiques ?"), [
        numpath(["9", "4"]),
        T("9 stands for nine objects and comes later on the number path. The size of the writing does not matter.",
          "9 تمثّل تسعة أشياء وتأتي لاحقًا على مسار الأعداد. حجم الكتابة لا يهم.",
          "9 représente neuf objets et vient plus tard sur la droite. La taille de l'écriture ne compte pas."),
        F("9 > 4"),
    ]),
    EX("5", "45", st("Compare 7 and 4 in two ways.", "قارن 7 و4 بطريقتين.", "Compare 7 et 4 de deux façons."), [
        pr(7, 4),
        numpath(P, hi=6),
        T("With counters, 3 are left from 7. On the number path, 7 is after 4.",
          "بالعدّادات يبقى 3 من 7. وعلى المسار 7 بعد 4.",
          "Avec les jetons, il en reste 3 dans 7. Sur la droite, 7 est après 4."),
        F("7 > 4"),
    ]),
    EX("6", "45", st("Error detective: “4 is greater than 7.”", "المحقق: «4 أكبر من 7».", "Détective : « 4 est plus grand que 7 »."), [
        pr(4, 7),
        T("The sentence is wrong. After pairing, objects are left in 7.",
          "الجملة خاطئة. بعد الإقران تبقى أشياء في 7.",
          "La phrase est fausse. Après appariement, il reste des objets dans 7."),
        F("7 > 4      4 < 7"),
    ]),
    EX("7", "45", st("Challenge: 3, 8 and 6. Find the greatest, the smallest, and order them.", "تحدٍّ: 3 و8 و6. أوجد الأكبر والأصغر ورتّبها.", "Défi : 3, 8 et 6. Trouve le plus grand, le plus petit et range-les."), [
        numpath(["3", "6", "8"]),
        F("greatest: 8      smallest: 3"),
        F("3 → 6 → 8"),
    ]),
    EX("8", "45", st("Final check: why is 8 greater than 5? Order 4, 9, 6.", "تقييم أخير: لماذا 8 أكبر من 5؟ رتّب 4 و9 و6.", "Évaluation : pourquoi 8 est-il plus grand que 5 ? Range 4, 9, 6."), [
        pr(8, 5),
        T("8 represents more objects than 5: three are left over.",
          "8 تمثّل أشياء أكثر من 5: يبقى ثلاثة.",
          "8 représente plus d'objets que 5 : il en reste trois."),
        F("4 → 6 → 9"),
    ]),
]
