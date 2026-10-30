from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import section, add_ex, add_sec
from scripts.direct_lessons.draw import numberline


def upgrade(m):
    add_sec(m, ("Practice: solve, check, reflect", "تدرّب: حلّ وتحقق وتأمّل", "Pratique : résous, vérifie, réfléchis"), [
        T("A full cycle on 3x − 4 ≤ 11. Step 1, work: 3x ≤ 15, so x ≤ 5. Step 2, check: test x = 5 → 15 − 4 = 11 ≤ 11 ✓ and test x = 6 → 14 > 11 so 6 is outside ✓. Step 3, reflect: dividing by a positive number kept the sign. Writing the check makes the answer yours.",
          "دورة كاملة على 3x − 4 ≤ 11. الخطوة 1 الحل: 3x ≤ 15 إذن x ≤ 5. الخطوة 2 التحقق: نجرّب x = 5 → 15 − 4 = 11 ≤ 11 ✓ ونجرّب x = 6 → 14 > 11 فهو خارج الحل ✓. الخطوة 3 التأمل: القسمة على عدد موجب أبقت الإشارة. كتابة التحقق تجعل الجواب لك.",
          "Résoudre, vérifier avec deux valeurs, réfléchir : 3x − 4 ≤ 11 → x ≤ 5."),
        numberline(0, 8, intervals=[(None, 5, False, True, "#2e7d32")], marks={"test 5": 5}, tag="Z1"),
    ])
    add_ex(m, [
        EX("", "", st("Solve 4x − 9 = 3 and write one sentence about what you checked.", "حلّ 4x − 9 = 3 واكتب جملة عمّا تحققت منه.", "Résous 4x − 9 = 3 et écris ce que tu as vérifié."), [
            T("4x = 12, so x = 3. Check: 4 × 3 − 9 = 3 ✓.", "4x = 12 إذن x = 3. تحقق: 4 × 3 − 9 = 3 ✓.", "x = 3."), F("x = 3")]),
        EX("", "", st("Classify the error: 3(x + 2) = 15 → 3x + 2 = 15 → x = 13/3.", "صنّف الخطأ: 3(x + 2) = 15 → 3x + 2 = 15 → x = 13/3.", "Classe l'erreur : 3(x + 2) = 15 → 3x + 2 = 15."), [
            T("This is a distribution error: 3 multiplies both terms, so 3(x + 2) = 3x + 6. The correct line is 3x + 6 = 15, so x = 3.", "هذا خطأ في التوزيع: 3 تضرب الحدين فيكون 3(x + 2) = 3x + 6. والسطر الصحيح 3x + 6 = 15 إذن x = 3.", "Erreur de distribution : 3x + 6 = 15 → x = 3."), F("x = 3")]),
        EX("", "", st("Write your own error journal entry for this one: 'I wrote −2x < 6 and answered x < −3'.", "اكتب سطرًا في دفتر أخطائك لهذا: «كتبت −2x < 6 وأجبت x < −3».", "Écris une ligne de carnet d'erreurs : « −2x < 6 donne x < −3 »."), [
            T("Mistake: I forgot to flip the sign when dividing by −2. Fix: −2x < 6 gives x > −3. Rule: dividing by a negative reverses the inequality. Check: x = 0 → 0 < 6 ✓.", "الخطأ: نسيت عكس الإشارة عند القسمة على −2. التصحيح: −2x < 6 تعطي x > −3. القاعدة: القسمة على عدد سالب تعكس المتراجحة. تحقق: x = 0 → 0 < 6 ✓.", "Oublié d'inverser : x > −3."), F("x > −3")]),
    ])
