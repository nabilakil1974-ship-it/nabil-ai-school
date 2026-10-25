"""Grade 1 Mathematics — Comparing numbers up to 19."""
from scripts.direct_lessons.common import T, F, EX, st, numpath, tens

LESSON_ID = "G01-MATH-EN-029"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Comparing numbers up to 19", "ar": "مقارنة الأعداد حتى 19", "fr": "Comparer les nombres jusqu'à 19"}


def path(hi_i=None, lo=10, hi=19):
    return numpath([str(i) for i in range(lo, hi + 1)], hi=hi_i, size=56)


THEORY = [
    ("Compare the quantities the numerals represent", "نقارن الكميات التي تمثّلها الأعداد", "Comparer les quantités représentées", "78", [
        T("Hello! Now we know the numbers up to 19 and their order. Today when I give you two numbers, I do not want only a quick answer. Say which one represents more, and prove why. Do not answer from the shape of the digits. Choose evidence: a model or the number path.",
          "مرحبًا! الآن نعرف الأعداد حتى 19 وترتيبها. اليوم عندما أعطيك عددين لا أريد جوابًا سريعًا فقط. قل أيهما يمثّل كمية أكبر وأثبت السبب. لا تجب من شكل الأرقام، بل اختر دليلًا: نموذجًا أو مسار الأعداد.",
          "Bonjour ! On connaît maintenant les nombres jusqu'à 19 et leur ordre. Aujourd'hui, quand je te donne deux nombres, je ne veux pas seulement une réponse rapide. Dis lequel représente le plus et prouve-le. Ne réponds pas d'après la forme des chiffres. Choisis une preuve : un modèle ou la droite des nombres."),
        tens(1, 6), tens(1, 9),
        T("Both have one ten. So what makes them different? The loose ones. 16 has 6 ones and 19 has 9 ones. So 19 represents more than 16, and 16 represents fewer.",
          "كلاهما فيه عشرة واحدة. فما الذي يفرّق بينهما؟ الآحاد المنفردة. في 16 ستة آحاد وفي 19 تسعة آحاد. إذن 19 تمثّل أكثر من 16، و16 تمثّل أقل.",
          "Les deux ont une dizaine. Qu'est-ce qui les distingue ? Les unités seules. 16 a 6 unités et 19 en a 9. Donc 19 représente plus que 16, et 16 représente moins."),
    ]),
    ("The number path gives evidence", "مسار الأعداد يعطي دليلًا", "La droite donne une preuve", "78", [
        path(8),
        T("On the number path, which of 13 and 18 is farther forward? 18. So 18 represents more than 13, because we reach 18 after 13 by adding one at a time.",
          "على مسار الأعداد أيهما أبعد إلى الأمام، 13 أم 18؟ 18. إذن 18 تمثّل أكثر من 13، لأننا نصل إلى 18 بعد 13 ونحن نزيد واحدًا واحدًا.",
          "Sur la droite, lequel est plus avancé, 13 ou 18 ? 18. Donc 18 représente plus que 13, car on atteint 18 après 13 en ajoutant un à la fois."),
    ]),
    ("Same number, same quantity", "العدد نفسه والكمية نفسها", "Même nombre, même quantité", "79", [
        tens(1, 5),
        tens(1, 5, bundled=False),
        T("These two look different. Is one of them more? No. We count or unbundle: each one is one ten and 5 ones. Same number, same quantity.",
          "هذان يبدوان مختلفين. هل أحدهما أكثر؟ لا. نعدّ أو نفكّ البنية: كل واحد عشرة واحدة وخمسة آحاد. العدد نفسه والكمية نفسها.",
          "Ces deux-là semblent différents. L'un est-il plus grand ? Non. On compte ou on défait : chacun est une dizaine et 5 unités. Même nombre, même quantité."),
    ]),
    ("For teen numbers, check the ten and then the ones", "في الأعداد المركّبة نفحص العشرة ثم الآحاد", "Pour les nombres de 11 à 19 : la dizaine puis les unités", "79", [
        tens(1, 4), tens(1, 8),
        T("Every number from 10 to 19 has one ten. So when we compare 14 and 18, the ten is the same. We compare the extra ones: 4 against 8. 8 is more than 4, so 18 is more than 14. This is a quick way, but its meaning is built on quantity.",
          "كل عدد من 10 إلى 19 فيه عشرة واحدة. لذلك عندما نقارن 14 و18 تكون العشرة نفسها. نقارن الآحاد الزائدة: 4 مقابل 8. 8 أكثر من 4، إذن 18 أكثر من 14. هذه طريقة سريعة لكن معناها مبني على الكمية.",
          "Chaque nombre de 10 à 19 a une dizaine. Quand on compare 14 et 18, la dizaine est la même. On compare les unités en plus : 4 contre 8. 8 est plus que 4, donc 18 est plus que 14. C'est rapide, mais le sens repose sur la quantité."),
    ]),
    ("Answer plus a visible reason", "الجواب مع سبب ظاهر", "Réponse et raison visible", "79", [
        T("If I say 17 is more than 15, I want a small proof. Good reasons: 17 is farther forward on the number path; 17 is ten and 7, while 15 is ten and 5; if we build them, 17 has two more objects. A strong answer is the answer plus the evidence.",
          "إذا قلت إن 17 أكثر من 15 أريد برهانًا صغيرًا. من الأسباب الجيدة: 17 أبعد إلى الأمام على المسار؛ 17 هي عشرة و7 بينما 15 عشرة و5؛ ولو بنيناهما لكان في 17 شيئان أكثر. الجواب القوي هو الجواب مع الدليل.",
          "Si je dis que 17 est plus que 15, je veux une petite preuve. Bonnes raisons : 17 est plus avancé sur la droite ; 17 c'est dix et 7, 15 c'est dix et 5 ; en les construisant, 17 a deux objets de plus. Une bonne réponse, c'est la réponse et la preuve."),
        F("answer + evidence"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("When we compare numbers, we are really comparing quantities. We can use a tens-and-ones model, counting, or the number path. For numbers from 11 to 19, check the ten, then the loose ones.",
          "عندما نقارن الأعداد فنحن في الحقيقة نقارن كميات. نستطيع أن نستعمل نموذج العشرات والآحاد أو العدّ أو مسار الأعداد. وللأعداد من 11 إلى 19 نفحص العشرة ثم الآحاد المنفردة.",
          "Quand on compare des nombres, on compare en fait des quantités. On peut utiliser un modèle dizaines-unités, le comptage ou la droite. Pour 11 à 19, on regarde la dizaine puis les unités seules."),
        F("READ → SHOW / LOCATE → COMPARE → MORE / FEWER / SAME → REASON → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "78", st("Compare 14 and 17 with models.", "قارن 14 و17 بالنماذج.", "Compare 14 et 17 avec des modèles."), [
        tens(1, 4), tens(1, 7),
        T("Same ten. Count the loose ones only: 7 is more than 4. So 17 is more.",
          "العشرة نفسها. نعدّ الآحاد المنفردة فقط: 7 أكثر من 4. إذن 17 أكثر.",
          "La même dizaine. On compte seulement les unités seules : 7 est plus que 4. Donc 17 est plus."),
        F("17 > 14"),
    ]),
    EX("2", "78", st("Compare on the path: 12 and 15; 18 and 17; 11 and 11.", "قارن على المسار: 12 و15؛ 18 و17؛ 11 و11.", "Compare sur la droite : 12 et 15 ; 18 et 17 ; 11 et 11."), [
        path(5),
        F("15 > 12      18 > 17      11 = 11"),
        T("The path gives us evidence: whoever is farther forward represents more.",
          "المسار يعطينا الدليل: الأبعد إلى الأمام يمثّل أكثر.",
          "La droite nous donne la preuve : le plus avancé représente plus."),
    ]),
    EX("3", "79", st("More, fewer or same? 13 and 16; 18 and 18; 19 and 15. Say the reason too.", "أكثر أم أقل أم نفسه؟ 13 و16؛ 18 و18؛ 19 و15. قل السبب أيضًا.", "Plus, moins ou pareil ? 13 et 16 ; 18 et 18 ; 19 et 15. Dis aussi la raison."), [
        F("13 < 16      18 = 18      19 > 15"),
        T("13 is fewer and 16 is more; 18 and 18 are the same; 19 is more and 15 is fewer. Always say the answer and the reason, not the answer alone.",
          "13 أقل و16 أكثر؛ 18 و18 متساويان؛ 19 أكثر و15 أقل. نقول دائمًا الجواب والسبب لا الجواب وحده.",
          "13 est moins et 16 est plus ; 18 et 18 sont pareils ; 19 est plus et 15 est moins. Dis toujours la réponse et la raison."),
    ]),
    EX("4", "79", st("Model A is one ten and 3 ones. Model B is one ten and 6 ones. Which has more?", "النموذج A عشرة وثلاثة آحاد. النموذج B عشرة وستة آحاد. أيهما أكثر؟", "Le modèle A est une dizaine et 3 unités. Le modèle B une dizaine et 6 unités. Lequel a plus ?"), [
        tens(1, 3), tens(1, 6),
        F("13 and 16      16 > 13"),
        T("Because 6 loose ones are more than 3.",
          "لأن 6 آحاد منفردة أكثر من 3.",
          "Parce que 6 unités seules, c'est plus que 3."),
    ]),
    EX("5", "79", st("Compare 12 and 18 and give one reason.", "قارن 12 و18 وأعطِ سببًا واحدًا.", "Compare 12 et 18 et donne une raison."), [
        tens(1, 2), tens(1, 8),
        F("18 > 12"),
        T("Reason: 18 is farther forward on the path, or 18 has 8 ones after the ten while 12 has only 2.",
          "السبب: 18 أبعد إلى الأمام على المسار، أو في 18 ثمانية آحاد بعد العشرة بينما في 12 اثنان فقط.",
          "Raison : 18 est plus avancé sur la droite, ou 18 a 8 unités après la dizaine alors que 12 n'en a que 2."),
    ]),
    EX("6", "79", st("Error detective: “14 has more than 18 because the digit 4 looks bigger than 8 on this card.”", "المحقق: «14 أكثر من 18 لأن الرقم 4 يبدو أكبر من 8 على هذه البطاقة».", "Détective : « 14 est plus que 18 parce que le chiffre 4 paraît plus grand que 8 sur cette carte »."), [
        tens(1, 4), tens(1, 8),
        T("This reasoning is wrong. We do not compare the look of the digits. 14 is ten and 4. 18 is ten and 8. 18 is farther forward and has more ones.",
          "هذا التفكير خاطئ. لا نقارن شكل الأرقام. 14 هي عشرة و4. و18 عشرة و8. 18 أبعد إلى الأمام وفيها آحاد أكثر.",
          "Ce raisonnement est faux. On ne compare pas l'aspect des chiffres. 14, c'est dix et 4. 18, c'est dix et 8. 18 est plus avancé et a plus d'unités."),
        F("18 > 14"),
    ]),
    EX("7", "79", st("Challenge: 11, 17 and 19. Which is most, which is fewest? Order them.", "تحدٍّ: 11 و17 و19. أيها الأكثر وأيها الأقل؟ رتّبها.", "Défi : 11, 17 et 19. Lequel est le plus, lequel le moins ? Range-les."), [
        numpath(["11", "17", "19"], size=56),
        F("most: 19      fewest: 11"),
        F("11 → 17 → 19"),
    ]),
    EX("8", "79", st("Final check: compare 16 and 19; 13 and 13; 18 and 15 with a tens-and-ones reason; which is farther forward, 12 or 17?", "تقييم أخير: قارن 16 و19؛ 13 و13؛ 18 و15 بسبب من العشرات والآحاد؛ أيهما أبعد إلى الأمام، 12 أم 17؟", "Évaluation : compare 16 et 19 ; 13 et 13 ; 18 et 15 avec une raison dizaines-unités ; lequel est plus avancé, 12 ou 17 ?"), [
        F("19 > 16      13 = 13      18 > 15      17 is farther forward"),
        T("18 is ten and 8 and 15 is ten and 5, so 18 has three more ones.",
          "18 هي عشرة و8 و15 عشرة و5، إذن في 18 ثلاثة آحاد أكثر.",
          "18, c'est dix et 8 ; 15, c'est dix et 5. 18 a donc trois unités de plus."),
    ]),
]
