"""Grade 1 Mathematics — Fast computation."""
from scripts.direct_lessons.common import T, F, EX, st, tens, numpath

LESSON_ID = "G01-MATH-EN-041"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Fast computation", "ar": "الحساب السريع", "fr": "Calcul rapide"}

THEORY = [
    ("Do not recount everything", "لا نعيد عدّ كل شيء", "Ne pas tout recompter", "106", [
        T("Hello, champion! Here we have 5 counters and 2 more. Do we have to count from one again? No! We keep the 5 in our head and count on: 6, 7. So 5 + 2 = 7. Fast does not mean guessing; fast means using something we already know.",
          "مرحبًا يا بطل! عندنا 5 قطع ومعها قطعتان. هل يجب أن نعدّ من الواحد من جديد؟ لا! نحتفظ بالعدد 5 في رأسنا ونكمل العدّ: 6، 7. إذن 5 + 2 = 7. السرعة لا تعني التخمين، بل تعني استعمال شيء نعرفه سابقًا.",
          "Bonjour champion ! Voici 5 jetons et 2 de plus. Faut-il recompter depuis un ? Non ! On garde 5 en tête et on compte en avant : 6, 7. Donc 5 + 2 = 7. Aller vite ne veut pas dire deviner : c'est utiliser ce qu'on sait déjà."),
        numpath(["5", "6", "7"], hi=2, size=64),
        F("5 + 2 = 7"),
    ]),
    ("Use a fact you know", "نستعمل حقيقة نعرفها", "Utiliser un fait connu", "106", [
        T("We know that 3 + 3 = 6. So 3 + 4 is just one more: 7. A known fact helps us find a new answer quickly, and we can explain why: 4 is 3 and 1 more.",
          "نعرف أن 3 + 3 = 6. إذن 3 + 4 أكبر بواحد فقط: 7. الحقيقة المعروفة تساعدنا على إيجاد جواب جديد بسرعة، ونستطيع أن نشرح السبب: 4 هي 3 وواحد زيادة.",
          "On sait que 3 + 3 = 6. Donc 3 + 4, c'est un de plus : 7. Un fait connu aide à trouver vite une nouvelle réponse, et on peut expliquer pourquoi : 4, c'est 3 et 1 de plus."),
        F("3 + 3 = 6   →   3 + 4 = 7"),
    ]),
    ("Use tens", "نستعمل العشرات", "Utiliser les dizaines", "107", [
        tens(3, 0, eq=True),
        tens(4, 0, eq=True),
        T("Even faster: we think in tens. In this part of the book we stay up to 69, so for example 20 + 40 = 60, because 2 tens + 4 tens = 6 tens.",
          "ولنكن أسرع: عندما نفكّر بالعشرات نجمع عدد العشرات. وفي هذا الجزء من الكتاب نبقى حتى 69، لذا نأخذ مثالًا أصغر: 20 + 40 = 60 لأن عشرتين + 4 عشرات = 6 عشرات.",
          "Encore plus vite : on pense en dizaines. Dans cette partie du livre, on reste jusqu'à 69, donc : 20 + 40 = 60 car 2 dizaines + 4 dizaines = 6 dizaines."),
        F("20 + 40 = 60"),
    ]),
    ("Check a fast answer", "نتحقق من الجواب السريع", "Vérifier une réponse rapide", "107", [
        numpath(["6", "7", "8", "9"], hi=3, size=60),
        T("If my fast answer to 6 + 3 is 9, I can check by counting on from 6: 7, 8, 9. A fast answer must always agree with a model or the number path.",
          "إذا كان جوابي السريع لـ6 + 3 هو 9 فأتحقق بالعدّ من 6: 7، 8، 9. يجب أن يتفق الجواب السريع دائمًا مع نموذج أو مع مسار الأعداد.",
          "Si ma réponse rapide pour 6 + 3 est 9, je vérifie en comptant à partir de 6 : 7, 8, 9. Une réponse rapide doit toujours s'accorder avec un modèle ou la droite."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Fast computation means choosing a smart strategy and keeping the answer correct: use a known fact, count on, or think in tens. Never guess; always be able to explain and check.",
          "الحساب السريع يعني اختيار طريقة ذكية مع بقاء الجواب صحيحًا: حقيقة معروفة، أو عدٌّ تصاعدي، أو التفكير بالعشرات. لا نخمّن أبدًا، بل نستطيع دائمًا أن نشرح ونتحقق.",
          "Calculer vite, c'est choisir une stratégie maline tout en restant exact : un fait connu, compter en avant, ou penser en dizaines. Jamais deviner : on sait expliquer et vérifier."),
        F("KNOWN FACT → COUNT ON → THINK IN TENS → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "106", st("Solve 4 + 2 by counting on.", "احسب 4 + 2 بالعدّ التصاعدي.", "Calcule 4 + 2 en comptant en avant."), [
        numpath(["4", "5", "6"], hi=2, size=64),
        T("Start at 4 and count on two: 5, 6. So 4 + 2 = 6.", "نبدأ من 4 ونعدّ اثنين: 5، 6. إذن 4 + 2 = 6.", "On part de 4 et on avance de deux : 5, 6. Donc 4 + 2 = 6."),
    ]),
    EX("2", "106", st("Use 5 + 5 = 10 to solve 5 + 6.", "استعمل 5 + 5 = 10 لحساب 5 + 6.", "Utilise 5 + 5 = 10 pour calculer 5 + 6."), [
        F("5 + 5 = 10   →   5 + 6 = 11"),
        T("6 is 5 and one more, so the answer is one more than 10: 11.", "6 هي 5 وواحد زيادة، فالجواب أكبر بواحد من 10: 11.", "6, c'est 5 et un de plus : un de plus que 10, soit 11."),
    ]),
    EX("3", "106", st("Solve 10 + 4 quickly.", "احسب 10 + 4 بسرعة.", "Calcule 10 + 4 vite."), [
        tens(1, 4, eq=True),
        T("10 and 4 ones make 14. We do not need to recount.", "10 مع 4 آحاد تعطي 14. لا حاجة لإعادة العدّ.", "10 et 4 unités font 14. Pas besoin de recompter."),
    ]),
    EX("4", "107", st("Solve 20 + 30 by thinking in tens.", "احسب 20 + 30 بالتفكير بالعشرات.", "Calcule 20 + 30 en pensant en dizaines."), [
        tens(5, 0, eq=True),
        T("2 tens + 3 tens = 5 tens = 50.", "عشرتان + 3 عشرات = 5 عشرات = 50.", "2 dizaines + 3 dizaines = 5 dizaines = 50."),
    ]),
    EX("5", "107", st("Check 7 + 2 = 9 on the number path.", "تحقّق من 7 + 2 = 9 على مسار الأعداد.", "Vérifie 7 + 2 = 9 sur la droite."), [
        numpath(["7", "8", "9"], hi=2, size=64),
        T("From 7 count on two: 8, 9. The fast answer is right.", "من 7 نعدّ اثنين: 8، 9. الجواب السريع صحيح.", "De 7 on avance de deux : 8, 9. La réponse rapide est juste."),
    ]),
    EX("6", "107", st("Error check: a child says 6 + 3 = 8 very fast. What should he do?", "تحقّق من الخطأ: قال طفل بسرعة إن 6 + 3 = 8. ماذا عليه أن يفعل؟", "Vérifie l'erreur : un enfant dit très vite 6 + 3 = 8. Que doit-il faire ?"), [
        numpath(["6", "7", "8", "9"], hi=3, size=60),
        T("He must check with a model: from 6 count on three: 7, 8, 9. The answer is 9. Speed without checking is not enough.", "عليه أن يتحقق بنموذج: من 6 نعدّ ثلاثة: 7، 8، 9. الجواب 9. السرعة دون تحقق لا تكفي.", "Il doit vérifier avec un modèle : de 6, trois pas : 7, 8, 9. La réponse est 9. La vitesse sans vérification ne suffit pas."),
    ]),
    EX("7", "107", st("Challenge: 10 + 10 + 4.", "تحدٍّ: 10 + 10 + 4.", "Défi : 10 + 10 + 4."), [
        tens(2, 4, eq=True),
        T("10 + 10 = 20, then 20 + 4 = 24.", "10 + 10 = 20 ثم 20 + 4 = 24.", "10 + 10 = 20, puis 20 + 4 = 24."),
    ]),
    EX("8", "107", st("Final check: solve 8 + 2 and 30 + 20 and say which relationship you used.", "تقييم أخير: احسب 8 + 2 و30 + 20 وقل أي علاقة استعملت.", "Évaluation : calcule 8 + 2 et 30 + 20 et dis quelle relation tu as utilisée."), [
        F("8 + 2 = 10      30 + 20 = 50"),
        T("8 + 2 makes ten, a known fact. 30 + 20 uses tens: 3 tens + 2 tens = 5 tens.", "8 + 2 تكوّن عشرة وهي حقيقة معروفة. و30 + 20 تستعمل العشرات: 3 عشرات + عشرتان = 5 عشرات.", "8 + 2 fait dix, un fait connu. 30 + 20 utilise les dizaines : 3 + 2 = 5 dizaines."),
    ]),
]
