"""Grade 2 Mathematics — Problems (6)."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G02-MATH-EN-033"
GRADE = 2
SUBJECT = "math"
TITLES = {"en": "Problems (6)", "ar": "مسائل (6)", "fr": "Problèmes (6)"}


def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}


QUIZ = [
    {"q": "Ramzi has 48 balls and Ziad has 35. How many more balls does Ramzi have?", "opts": ["13", "83", "23", "12"], "a": 0,
     "why": {"83": _w("83 is 48 + 35. 'How many more' asks for the difference.", "83 هو 48 + 35. 'كم أكثر' تسأل عن الفرق.", "83 = 48 + 35. 'Combien de plus' demande la différence."),
             "23": _w("Check: 35 + 23 = 58, not 48.", "تحقق: 35 + 23 = 58 لا 48.", "35 + 23 = 58, pas 48."),
             "12": _w("Check: 35 + 12 = 47, not 48.", "تحقق: 35 + 12 = 47 لا 48.", "35 + 12 = 47, pas 48.")},
     "ok": "48 − 35 = 13"},
    {"q": "Nour had 36 chocolates. Now she has 25. How many did she eat?", "opts": ["11", "25", "61", "10"], "a": 0,
     "why": {"25": _w("25 is what is left, not what she ate.", "25 هو ما تبقى لا ما أكلته.", "25 est ce qui reste."),
             "61": _w("61 is more than the 36 she started with. Impossible.", "61 أكبر من 36 التي بدأت بها. مستحيل.", "61 dépasse 36 : impossible."),
             "10": _w("Check: 25 + 10 = 35, not 36.", "تحقق: 25 + 10 = 35 لا 36.", "25 + 10 = 35, pas 36.")},
     "ok": "36 − 25 = 11"},
    {"q": "How can we check that 58 − 12 = 46?", "opts": ["12 + 46 = 58", "58 + 12 = 70", "46 − 12 = 58", "58 + 46 = 12"], "a": 0,
     "why": {"58 + 12 = 70": _w("That is a different sum, it does not check the answer.", "هذا مجموع آخر لا يتحقق من الجواب.", "Autre somme : ça ne vérifie pas."),
             "46 − 12 = 58": _w("46 − 12 is 34, not 58.", "46 − 12 = 34 لا 58.", "46 − 12 = 34."),
             "58 + 46 = 12": _w("That is false.", "هذا خطأ.", "C'est faux.")},
     "ok": "The small part plus the difference gives back the big number."},
]

THEORY = [
    ("Read the story first", "نقرأ القصة أولًا", "On lit d'abord l'histoire", "72", [
        T("Hello! Before we calculate, we ask three questions. What is the total or the bigger number? What do we already know? What is the question asking?",
          "مرحبًا! قبل أن نحسب نسأل ثلاثة أسئلة. ما المجموع أو العدد الأكبر؟ ماذا نعرف؟ ماذا يطلب السؤال؟",
          "Avant de calculer, trois questions : quel est le total ? que sait-on ? que demande-t-on ?"),
        F("Understand → Given → Asked → Relation → Solve → Check"),
    ]),
    ("How many more is a difference", "كم أكثر تعني الفرق", "« Combien de plus » est une différence", "72", [
        T("Ramzi has 48 balls. Ziad has 35. How many more has Ramzi? The word 'more' does not mean we add. We are comparing two numbers, so we find the difference: 48 − 35. Units: 8 − 5 = 3. Tens: 4 − 3 = 1. So 48 − 35 = 13.",
          "عند رمزي 48 كرة وعند زياد 35. كم كرة أكثر عند رمزي؟ كلمة 'أكثر' لا تعني أننا نجمع. نحن نقارن عددين فنجد الفرق: 48 − 35. الآحاد: 8 − 5 = 3. العشرات: 4 − 3 = 1. إذن 48 − 35 = 13.",
          "Ramzi a 48 billes, Ziad 35. On compare : différence 48 − 35 = 13."),
        F("48 − 35 = 13"),
        T("Check: 35 + 13 = 48. Ramzi has 13 more balls than Ziad.", "نتحقق: 35 + 13 = 48. عند رمزي 13 كرة أكثر من زياد.", "Vérification : 35 + 13 = 48. Ramzi a 13 billes de plus."),
        F("35 + 13 = 48"),
    ]),
    ("Ate and removed: find the missing part", "أكل وأُزيل: نجد الجزء الناقص", "Mangé et enlevé : la partie manquante", "72", [
        T("Nour had 36 chocolates. Now she has 25. How many did she eat? We know the start (36) and what remains (25). The missing part is 36 − 25 = 11.",
          "عند نور 36 شوكولاتة وصار عندها 25. كم أكلت؟ نعرف البداية (36) والباقي (25). الجزء الناقص هو 36 − 25 = 11.",
          "Nour avait 36 chocolats, il lui en reste 25 : 36 − 25 = 11."),
        F("36 − 25 = 11"),
        T("Check: 25 + 11 = 36. She ate 11 chocolates. Careful: 25 is what is left, not what she ate!",
          "نتحقق: 25 + 11 = 36. أكلت 11 قطعة. انتبه: 25 هو الباقي لا ما أكلته!",
          "Vérification : 25 + 11 = 36. Elle en a mangé 11."),
        F("25 + 11 = 36"),
    ]),
    ("The operation follows the relation", "العملية تتبع العلاقة", "L'opération suit la relation", "72", [
        T("A single word never decides the operation. 'More' in a difference question means subtract. 'Ate' and 'removed' mean we find a missing part by subtracting. We always say the unit in the answer: balls, chocolates, marbles, stamps, stars.",
          "كلمة واحدة لا تحدد العملية. 'أكثر' في سؤال الفرق تعني نطرح. و'أكل' و'أُزيل' تعني أننا نجد الجزء الناقص بالطرح. ونذكر الوحدة دائمًا في الجواب: كرات أو شوكولاتة أو بلورات أو طوابع أو نجوم.",
          "Un mot ne décide pas de l'opération : on regarde la relation, et on écrit l'unité dans la réponse."),
        F("difference = bigger − smaller"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Great job! Read the story, find what we know and what is asked, choose the operation from the relation, solve, then check with an addition. Our rule: relation first, calculation second, check the story.",
          "أحسنت! نقرأ القصة ونحدد المعطيات والمطلوب ونختار العملية من العلاقة ثم نحلّ ونتحقق بالجمع. قاعدتنا: العلاقة أولًا ثم الحساب ثم نتحقق من القصة.",
          "Bravo ! Lire, repérer les données, choisir l'opération, calculer, vérifier avec une addition."),
        F("Relation first → calculate → check"),
    ]),
]

EXERCISES = [
    EX("1", "72", st("Ramzi has 48 balls. Ziad has 35. How many more balls does Ramzi have than Ziad?", "عند رمزي 48 كرة وعند زياد 35. كم كرة أكثر عند رمزي من زياد؟", "Ramzi a 48 billes, Ziad 35. Combien de billes Ramzi a-t-il de plus ?"), [
        T("Asked: the difference. Plan: 48 − 35. 8 − 5 = 3 and 4 − 3 = 1, so 13.", "المطلوب الفرق. الخطة: 48 − 35. 8 − 5 = 3 و4 − 3 = 1 إذن 13.", "On cherche la différence : 48 − 35 = 13."),
        F("48 − 35 = 13      check: 35 + 13 = 48"),
        T("Ramzi has 13 more balls than Ziad.", "عند رمزي 13 كرة أكثر من زياد.", "Ramzi a 13 billes de plus."),
    ]),
    EX("2", "72", st("Nour had 36 chocolates. She now has 25. How many chocolates did she eat?", "كان عند نور 36 شوكولاتة وصار عندها 25. كم شوكولاتة أكلت؟", "Nour avait 36 chocolats, il lui en reste 25. Combien en a-t-elle mangé ?"), [
        F("36 − 25 = 11      check: 25 + 11 = 36"),
        T("She ate 11 chocolates.", "أكلت 11 شوكولاتة.", "Elle a mangé 11 chocolats."),
    ]),
    EX("3", "72", st("Sami has 58 marbles. Dani has 12 marbles. What is the difference?", "عند سامي 58 بلورة وعند داني 12 بلورة. ما الفرق؟", "Sami a 58 billes, Dani 12. Quelle est la différence ?"), [
        T("Always take the smaller from the larger: 58 − 12.", "نطرح الأصغر من الأكبر دائمًا: 58 − 12.", "On retire le petit du grand : 58 − 12."),
        F("58 − 12 = 46      check: 12 + 46 = 58"),
        T("The difference is 46 marbles.", "الفرق 46 بلورة.", "La différence est de 46 billes."),
    ]),
    EX("4", "72", st("There were 45 stamps in an album. There are 23 left. How many were removed?", "كان في الألبوم 45 طابعًا وبقي 23. كم طابعًا أُزيل؟", "Il y avait 45 timbres, il en reste 23. Combien ont été enlevés ?"), [
        F("45 − 23 = 22      check: 23 + 22 = 45"),
        T("22 stamps were removed.", "أُزيل 22 طابعًا.", "22 timbres ont été enlevés."),
    ]),
    EX("5", "72", st("Nada put 64 stars on a tree. Her sister put 23. How many more stars did Nada put?", "وضعت ندى 64 نجمة على الشجرة ووضعت أختها 23. كم نجمة أكثر وضعت ندى؟", "Nada a mis 64 étoiles, sa sœur 23. Combien de plus Nada a-t-elle mises ?"), [
        F("64 − 23 = 41      check: 23 + 41 = 64"),
        T("Nada put 41 more stars than her sister.", "وضعت ندى 41 نجمة أكثر من أختها.", "Nada a mis 41 étoiles de plus."),
    ]),
    EX("6", "", st("(our own) Maya has 73 cards and Lina has 41. What is the difference?", "(من عندنا) عند مايا 73 بطاقة وعند لينا 41. ما الفرق؟", "(à nous) Maya a 73 cartes, Lina 41. Quelle est la différence ?"), [
        F("73 − 41 = 32      check: 41 + 32 = 73"),
        T("The difference is 32 cards.", "الفرق 32 بطاقة.", "La différence est de 32 cartes."),
    ]),
]
