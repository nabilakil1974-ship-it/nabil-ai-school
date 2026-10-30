from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import section, add_ex, add_sec
from scripts.direct_lessons.draw import numberline


def upgrade(m):
    s = section(m, "Order on the real line")
    s.append(numberline(-8, 2, marks={"−7": -7, "−4": -4}, tag="O1"))
    s.append(T("On the number line, the number on the right is the greater one. −4 is to the right of −7, so −4 > −7, even though 7 > 4. Negative numbers: the bigger the digit, the smaller the number.",
               "على محور الأعداد العدد الأيمن هو الأكبر. −4 على يمين −7 إذن −4 > −7 مع أن 7 > 4. في الأعداد السالبة: كلما كبر الرقم صغر العدد.",
               "Plus on est à droite, plus le nombre est grand : −4 > −7."))
    s = section(m, "Inequalities and intervals")
    s.append(numberline(-6, 6, intervals=[(-3, None, False, False, "#e53935")], tag="O2"))
    s.append(T("The solution of −2x < 6 is x > −3. On the line: an open circle at −3 (not included, because the inequality is strict) and a thick bar going right forever. Remember: dividing by −2 flipped the sign.",
               "حل −2x < 6 هو x > −3. على المحور: دائرة مفتوحة عند −3 (غير مشمول لأن المتراجحة صارمة) وشريط سميك يمتد يمينًا بلا نهاية. تذكّر: القسمة على −2 عكست الإشارة.",
               "−2x < 6 donne x > −3 : cercle ouvert en −3, barre vers la droite ; le sens s'est inversé."))
    s.append(numberline(-6, 6, intervals=[(-3, 4, True, False, "#2e7d32")], tag="O3"))
    s.append(T("A closed circle includes the endpoint and an open circle excludes it. This green bar is [−3, 4): −3 is included, 4 is not.", "الدائرة المغلقة تُدخل الطرف والمفتوحة تستبعده. هذا الشريط الأخضر هو [−3, 4): −3 مشمول و4 غير مشمول.", "Cercle plein : inclus ; vide : exclu. [−3 ; 4[."))
    add_ex(m, [
        EX("", "", st("Compare 3/7 and 4/9 without decimals.", "قارن بين 3/7 وَ4/9 دون كتابة عشرية.", "Compare 3/7 et 4/9 sans décimaux."), [
            T("Common denominator 63: 3/7 = 27/63 and 4/9 = 28/63. Since 27 < 28, 3/7 < 4/9.", "المقام المشترك 63: 3/7 = 27/63 وَ4/9 = 28/63. وبما أن 27 < 28 فإن 3/7 < 4/9.", "27/63 < 28/63."), F("3/7 < 4/9")]),
        EX("", "", st("Compare √10 and 3.2 using squares.", "قارن بين √10 وَ3.2 باستعمال المربعات.", "Compare √10 et 3,2 avec les carrés."), [
            T("Both are positive, so we may compare squares: (√10)² = 10 and 3.2² = 10.24.", "كلاهما موجب فيمكن مقارنة المربعين: (√10)² = 10 وَ3.2² = 10.24.", "10 et 10,24."), F("10 < 10.24, so √10 < 3.2")]),
        EX("", "", st("Solve 2x − 3 < 7 and show the set on a number line.", "حلّ 2x − 3 < 7 ومثّل المجموعة على محور.", "Résous 2x − 3 < 7 et représente."), [
            T("2x < 10, so x < 5.", "2x < 10 إذن x < 5.", "x < 5."), numberline(-2, 8, intervals=[(None, 5, False, False, "#e53935")], tag="X1"), F("S = (−∞, 5)")]),
        EX("", "", st("If −2 < x < 3, between which numbers is 2x + 1?", "إذا كان −2 < x < 3 فبين أي عددين تقع 2x + 1؟", "Si −2 < x < 3, encadre 2x + 1."), [
            T("Multiply by 2: −4 < 2x < 6. Add 1: −3 < 2x + 1 < 7.", "نضرب في 2: −4 < 2x < 6. نضيف 1: −3 < 2x + 1 < 7.", "−4 < 2x < 6 → −3 < 2x + 1 < 7."), F("−3 < 2x + 1 < 7")]),
    ])
