"""Grade 3 Mathematics — Adding (mental strategies with tens, hundreds and friendly numbers)."""
from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.draw import hops, blocks

LESSON_ID = "G03-MATH-EN-004"
GRADE = 3
SUBJECT = "math"
TITLES = {"en": "Adding", "ar": "الجمع", "fr": "Additionner"}


def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}


QUIZ = [
    {"q": "325 + 100 = ?", "opts": ["425", "335", "326", "525"], "a": 0,
     "why": {"335": _w("335 is 325 + 10. Adding 100 changes the hundreds digit.", "335 هو 325 + 10. إضافة 100 تغيّر رقم المئات.", "335 = 325 + 10."),
             "326": _w("That is 325 + 1.", "هذا 325 + 1.", "325 + 1."),
             "525": _w("We add one hundred, not two.", "نضيف مئة واحدة لا مئتين.", "Une centaine.")}, "ok": "425"},
    {"q": "Which pair makes 100 in 98 + 2 + 594?", "opts": ["98 and 2", "2 and 594", "98 and 594", "none"], "a": 0,
     "why": {"2 and 594": _w("2 + 594 = 596, not a friendly number.", "2 + 594 = 596 وليس عددًا سهلًا.", "596."),
             "98 and 594": _w("98 + 594 = 692, not a friendly number.", "98 + 594 = 692.", "692."),
             "none": _w("98 + 2 = 100 is a friendly pair.", "98 + 2 = 100 زوج سهل.", "98 + 2 = 100.")}, "ok": "98 + 2 = 100"},
    {"q": "If 679 + 100 = 779, then 679 + 99 = ?", "opts": ["778", "780", "769", "679"], "a": 0,
     "why": {"780": _w("99 is one LESS than 100, so the answer is one less.", "99 أقل من 100 بواحد فالناتج أقل بواحد.", "99 < 100."),
             "769": _w("That would be 679 + 90.", "هذا 679 + 90.", "679 + 90."),
             "679": _w("We still add almost 100.", "ما زلنا نضيف قرابة 100.", "On ajoute presque 100.")}, "ok": "778"},
]

THEORY = [
    ("Adding tens and hundreds", "جمع العشرات والمئات", "Ajouter des dizaines et des centaines", "18", [
        T("Hello, champion! Look at 325. Add one ten: 325 + 10 = 335. Only the tens digit changed. Add one hundred: 325 + 100 = 425. Only the hundreds digit changed. The other digits stay because we are not touching them. Adding 10 adds one ten, not one one.",
          "مرحبًا يا بطل! انظر إلى 325. أضف عشرة: 325 + 10 = 335. تغيّر رقم العشرات فقط. أضف مئة: 325 + 100 = 425. تغيّر رقم المئات فقط. بقية الأرقام لا تتغير لأننا لم نلمسها. إضافة 10 تضيف عشرة واحدة لا واحدًا واحدًا.",
          "325 + 10 = 335 (seul le chiffre des dizaines change) ; 325 + 100 = 425 (seul celui des centaines change)."),
        blocks(3, 2, 5, tag="B1"),
        F("325 + 10 = 335      325 + 100 = 425"),
        T("More: 368 + 10 = 378. 432 + 40 = 472. 568 + 30 = 598. 825 + 100 = 925. 736 + 200 = 936. 264 + 400 = 664. In every case, say which digit changes: tens for +10, +30, +40 and hundreds for +100, +200, +400.",
          "أمثلة أخرى: 368 + 10 = 378. 432 + 40 = 472. 568 + 30 = 598. 825 + 100 = 925. 736 + 200 = 936. 264 + 400 = 664. في كل مرة قل أي رقم يتغير: العشرات عند +10 و+30 و+40 والمئات عند +100 و+200 و+400.",
          "368 + 10 = 378 ; 432 + 40 = 472 ; 825 + 100 = 925 ; 736 + 200 = 936."),
    ]),
    ("Hundreds and tens together", "المئات والعشرات معًا", "Centaines et dizaines ensemble", "18", [
        T("To add 100 and 10 together, add each part in turn. 321 + 100 = 421, then 421 + 10 = 431. Another: 469 + 200 + 20. First 469 + 200 = 669, then 669 + 20 = 689. Hundreds first, then tens.",
          "لجمع 100 و10 معًا نضيف كل جزء بدوره. 321 + 100 = 421 ثم 421 + 10 = 431. مثال آخر: 469 + 200 + 20. أولًا 469 + 200 = 669 ثم 669 + 20 = 689. المئات أولًا ثم العشرات.",
          "321 + 100 + 10 : 421 puis 431. 469 + 200 + 20 : 669 puis 689."),
        hops(469, [200, 20], tag="H1"),
        F("469 + 200 + 20 = 689"),
        T("Error detective! A learner writes 325 + 100 = 335. The result 335 is what you get by adding 10. Adding 100 gives 425. Always ask: am I adding tens or hundreds?",
          "المحقق! كتب متعلّم 325 + 100 = 335. العدد 335 هو ناتج إضافة 10. إضافة 100 تعطي 425. اسأل دائمًا: هل أضيف عشرات أم مئات؟",
          "Détective : 325 + 100 ≠ 335 ; 335 vient de + 10. Le bon résultat est 425."),
    ]),
    ("Combine place-value parts", "اجمع أجزاء المنازل", "Combiner les valeurs de position", "18", [
        T("Sometimes we add many parts: 300 + 40 + 500 + 50. Group hundreds with hundreds and tens with tens: (300 + 500) + (40 + 50) = 800 + 90 = 890. Which parts can you combine first so the work becomes easy? The ones that are the same kind.",
          "أحيانًا نجمع أجزاء كثيرة: 300 + 40 + 500 + 50. نجمع المئات مع المئات والعشرات مع العشرات: (300 + 500) + (40 + 50) = 800 + 90 = 890. أي الأجزاء نجمعها أولًا ليسهل العمل؟ المتشابهة.",
          "300 + 40 + 500 + 50 = (300 + 500) + (40 + 50) = 890."),
        F("300 + 40 + 500 + 50 = 800 + 90 = 890"),
        F("500 + 100 + 70 + 20 = 600 + 90 = 690"),
        F("200 + 500 + 80 + 40 = 700 + 120 = 820"),
    ]),
    ("Decompose one addend", "حلّل أحد المجموعين", "Décomposer un terme", "19", [
        T("To add 234 + 152, start at 234 and add the parts of 152 one at a time: +100 gives 334, +50 gives 384, +2 gives 386. So 234 + 152 = 386. Each hop is easy because it only changes one place.",
          "لجمع 234 + 152 نبدأ من 234 ونضيف أجزاء 152 واحدًا بعد الآخر: +100 تعطي 334 و+50 تعطي 384 و+2 تعطي 386. إذن 234 + 152 = 386. كل قفزة سهلة لأنها تغيّر منزلة واحدة.",
          "234 + 152 : +100 → 334, +50 → 384, +2 → 386."),
        hops(234, [100, 50, 2], tag="H2"),
        T("Your turn: 451 + 327. Break 327 into 300 + 20 + 7. 451 + 300 = 751, then +20 = 771, then +7 = 778. So 451 + 327 = 778.",
          "دورك: 451 + 327. حلّل 327 إلى 300 + 20 + 7. 451 + 300 = 751 ثم +20 = 771 ثم +7 = 778. إذن 451 + 327 = 778.",
          "451 + 327 : 751, 771, 778."),
        hops(451, [300, 20, 7], tag="H3"),
        F("306 + 504 = 810      520 + 240 = 760"),
    ]),
    ("Make a ten first", "كوّن عشرة أولًا", "Faire une dizaine d'abord", "19", [
        T("Look for numbers that make a ten. 18 + 42 = 60. 69 + 81 = 150. With three numbers: 36 + 15 + 24. Do not go left to right. See that 36 + 24 = 60, then 60 + 15 = 75. Reordering keeps the same total, because addition can be done in any order.",
          "ابحث عن أعداد تكوّن عشرة. 18 + 42 = 60. 69 + 81 = 150. ومع ثلاثة أعداد: 36 + 15 + 24. لا نسير من اليسار إلى اليمين. نلاحظ أن 36 + 24 = 60 ثم 60 + 15 = 75. تغيير الترتيب يحفظ المجموع لأن الجمع يتم بأي ترتيب.",
          "36 + 15 + 24 = (36 + 24) + 15 = 60 + 15 = 75. Réordonner garde le total."),
        F("17 + 23 + 68 = 40 + 68 = 108"),
        F("28 + 42 + 15 + 35 = 70 + 50 = 120"),
        F("19 + 26 + 31 + 44 = 50 + 70 = 120"),
        T("Why does it work? The sum does not depend on the order. We choose the order that gives friendly numbers like 60, 100 and 120.",
          "لماذا تنجح؟ المجموع لا يتعلق بالترتيب. نختار الترتيب الذي يعطي أعدادًا سهلة مثل 60 و100 و120.",
          "La somme ne dépend pas de l'ordre."),
    ]),
    ("Make a hundred first", "كوّن مئة أولًا", "Faire une centaine d'abord", "19", [
        T("Now look for pairs that make 100. 99 + 327 + 1: pair 99 and 1 first. 99 + 1 = 100, then 100 + 327 = 427. 98 + 2 + 594: 98 + 2 = 100, then 100 + 594 = 694. 80 + 768 + 20: 80 + 20 = 100, then 100 + 768 = 868.",
          "الآن نبحث عن أزواج تكوّن 100. 99 + 327 + 1: نزاوج 99 و1 أولًا. 99 + 1 = 100 ثم 100 + 327 = 427. 98 + 2 + 594: 98 + 2 = 100 ثم 100 + 594 = 694. 80 + 768 + 20: 80 + 20 = 100 ثم 100 + 768 = 868.",
          "99 + 1 = 100 puis 100 + 327 = 427 ; 98 + 2 + 594 = 694."),
        F("236 + 50 + 50 = 236 + 100 = 336"),
        F("389 + 40 + 60 = 489"),
        F("30 + 125 + 70 = 100 + 125 = 225"),
    ]),
    ("Use a known fact for a nearby fact", "استعمل معلومة معروفة لمعلومة قريبة", "Un fait connu pour un fait voisin", "19", [
        T("We know 527 + 10 = 537. Then 527 + 9 is one less: 536. And 527 + 11 is one more: 538. Do the same with hundreds: 679 + 100 = 779, so 679 + 99 = 778 (one less) and 679 + 101 = 780 (one more).",
          "نعرف أن 527 + 10 = 537. إذن 527 + 9 أقل بواحد: 536. و527 + 11 أكثر بواحد: 538. وكذلك مع المئات: 679 + 100 = 779 فإن 679 + 99 = 778 (أقل بواحد) و679 + 101 = 780 (أكثر بواحد).",
          "527 + 10 = 537 → 527 + 9 = 536 et 527 + 11 = 538. 679 + 100 = 779 → 679 + 99 = 778."),
        F("425 + 100 = 525      425 + 99 = 524      425 + 98 = 523"),
        T("Three questions help: What easy fact do I know? How far is my number from it? Should the answer be more or less? Then check by adding directly.",
          "ثلاثة أسئلة تساعد: ما المعلومة السهلة التي أعرفها؟ كم يبعد عددي عنها؟ هل يكون الجواب أكبر أم أقل؟ ثم نتحقق بالجمع المباشر.",
          "Quel fait connais-je ? À quelle distance ? Plus ou moins ? Puis vérifier."),
    ]),
    ("The bee path: count by 10", "طريق النحلة: العدّ بالعشرات", "Le chemin de l'abeille : compter de 10 en 10", "19", [
        T("A bee must reach its hive by moving through numbers that increase by 10 each time. If the bee is on 130, the next stop is 140, then 150, 160. A neighbour is correct only when it is exactly 10 more than the number you are on.",
          "على النحلة أن تصل إلى خليتها عبر أعداد تزيد 10 في كل مرة. إذا كانت على 130 فالمحطة التالية 140 ثم 150 ثم 160. الجار صحيح فقط عندما يكون أكبر من عددك بعشرة بالضبط.",
          "130 → 140 → 150 → 160 : chaque pas ajoute exactement 10."),
        hops(130, [10, 10, 10, 10], tag="H4"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Add smartly and keep the same total. +10 changes the tens and +100 changes the hundreds. Decompose: hundreds, then tens, then ones. Pair numbers that make 10 or 100. Use nearby facts: +99 is +100 − 1. And always check your shortcut.",
          "نجمع بذكاء مع حفظ المجموع نفسه. +10 تغيّر العشرات و+100 تغيّر المئات. نحلّل: مئات ثم عشرات ثم آحاد. نزاوج الأعداد التي تكوّن 10 أو 100. نستعمل معلومات قريبة: +99 هي +100 − 1. وننتبه دائمًا إلى التحقق.",
          "+10 : dizaines ; +100 : centaines ; faire 10 ou 100 ; +99 = +100 − 1 ; vérifier."),
        F("+99 = +100 − 1      98 + 2 + 594 = 100 + 594 = 694"),
    ]),
]


def _ex(n, en, ar, fr, steps):
    return EX(n, "", st(en, ar, fr), steps)


EXERCISES = [
    _ex("1", "Calculate 568 + 30.", "احسب 568 + 30.", "Calcule 568 + 30.", [T("30 is three tens. 568 + 30: the tens digit 6 becomes 9. The answer is 598.", "30 هي ثلاث عشرات. في 568 + 30 يصبح رقم العشرات 6 إلى 9. الجواب 598.", "598."), F("568 + 30 = 598")]),
    _ex("2", "Calculate 264 + 400.", "احسب 264 + 400.", "Calcule 264 + 400.", [T("400 is four hundreds: the hundreds digit 2 becomes 6. The answer is 664.", "400 أربع مئات: يصبح رقم المئات 2 إلى 6. الجواب 664.", "664."), F("264 + 400 = 664")]),
    _ex("3", "Calculate 534 + 300 + 50.", "احسب 534 + 300 + 50.", "Calcule 534 + 300 + 50.", [T("534 + 300 = 834. Then 834 + 50 = 884.", "534 + 300 = 834 ثم 834 + 50 = 884.", "834 puis 884."), hops(534, [300, 50], tag="X1"), F("534 + 300 + 50 = 884")]),
    _ex("4", "Calculate 300 + 400 + 50 + 70.", "احسب 300 + 400 + 50 + 70.", "Calcule 300 + 400 + 50 + 70.", [T("Hundreds: 300 + 400 = 700. Tens: 50 + 70 = 120. Total 700 + 120 = 820.", "المئات: 300 + 400 = 700. العشرات: 50 + 70 = 120. المجموع 700 + 120 = 820.", "700 + 120 = 820."), F("= 820")]),
    _ex("5", "Calculate 451 + 327 by decomposing 327.", "احسب 451 + 327 بتحليل 327.", "Calcule 451 + 327 en décomposant 327.", [T("327 = 300 + 20 + 7. 451 + 300 = 751; 751 + 20 = 771; 771 + 7 = 778.", "327 = 300 + 20 + 7. 451 + 300 = 751؛ 751 + 20 = 771؛ 771 + 7 = 778.", "778."), F("451 + 327 = 778"), F("Check: 778 − 327 = 451 ✓")]),
    _ex("6", "Calculate 28 + 42 + 15 + 35 with friendly totals.", "احسب 28 + 42 + 15 + 35 بأعداد سهلة.", "Calcule 28 + 42 + 15 + 35.", [T("28 + 42 = 70 and 15 + 35 = 50. Then 70 + 50 = 120.", "28 + 42 = 70 و15 + 35 = 50. ثم 70 + 50 = 120.", "70 + 50 = 120."), F("= 120")]),
    _ex("7", "Calculate 99 + 327 + 1.", "احسب 99 + 327 + 1.", "Calcule 99 + 327 + 1.", [T("99 + 1 = 100. Then 100 + 327 = 427.", "99 + 1 = 100 ثم 100 + 327 = 427.", "427."), F("= 427")]),
    _ex("8", "If 425 + 100 = 525, find 425 + 98.", "إذا كان 425 + 100 = 525 فجد 425 + 98.", "Si 425 + 100 = 525, trouve 425 + 98.", [T("98 is 2 less than 100, so the answer is 2 less than 525: 523.", "98 أقل من 100 باثنين فالجواب أقل من 525 باثنين: 523.", "523."), F("425 + 98 = 523"), F("Check: 425 + 98 = 425 + 100 − 2 = 523 ✓")]),
    _ex("9", "From 527 + 10 = 537, find 527 + 9 and 527 + 11.", "من 527 + 10 = 537 جد 527 + 9 و527 + 11.", "À partir de 527 + 10 = 537, trouve 527 + 9 et 527 + 11.", [T("527 + 9 is one less than 537: 536. 527 + 11 is one more: 538.", "527 + 9 أقل من 537 بواحد: 536. و527 + 11 أكثر بواحد: 538.", "536 et 538."), F("536      538")]),
    _ex("10", "Calculate 234 + 152 with three hops and 306 + 504 with two hops.", "احسب 234 + 152 بثلاث قفزات و306 + 504 بقفزتين.", "Calcule 234 + 152 en trois sauts, 306 + 504 en deux.", [T("234 + 100 = 334; + 50 = 384; + 2 = 386.", "234 + 100 = 334؛ + 50 = 384؛ + 2 = 386.", "386."), T("306 + 500 = 806; + 4 = 810.", "306 + 500 = 806؛ + 4 = 810.", "810."), hops(306, [500, 4], tag="X2"), F("386      810")]),
    _ex("11", "Real life: Sami has 245 stickers. He gets 100 from his sister and 30 from a friend. How many now?", "حياتي: عند سامي 245 ملصقًا. أخذ 100 من أخته و30 من صديق. كم أصبح عنده؟", "Sami a 245 autocollants, reçoit 100 puis 30. Combien ?", [T("245 + 100 = 345. Then 345 + 30 = 375.", "245 + 100 = 345 ثم 345 + 30 = 375.", "375."), F("Sami has 375 stickers")]),
    _ex("12", "Error detective: 'I did 469 + 200 + 20 and got 489.' What went wrong?", "المحقق: «حسبت 469 + 200 + 20 فوجدت 489». ما الخطأ؟", "Détective : « 469 + 200 + 20 = 489 ». Où est l'erreur ?", [T("The learner added 20 but not the 200 correctly: 469 + 20 = 489. The right order: 469 + 200 = 669, then + 20 = 689.", "أضاف المتعلّم 20 فقط: 469 + 20 = 489 ونسي المئتين. الصحيح: 469 + 200 = 669 ثم + 20 = 689.", "Il a oublié le 200. Correct : 689."), F("689")]),
]
