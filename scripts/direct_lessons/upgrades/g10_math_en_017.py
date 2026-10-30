from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import fn_graph, section, add_ex, add_sec


def upgrade(m):
    s = section(m, "Worked example")
    s.append(fn_graph(lambda x: 3 * x - 5, (-2, 8), (-12, 14), hlines=[10], vlines=[5], pts={"A": (5, 10)}, tag="N1", label="y = 3x − 5 against the level y = 10"))
    s.append(T("To solve 3x − 5 < 10 we ask: where is the line y = 3x − 5 below the level y = 10? They meet at x = 5. To the left of 5 the line is lower, so the solutions are x < 5. This picture and the algebra (3x < 15, x < 5) agree.",
               "لحل 3x − 5 < 10 نسأل: أين يكون المستقيم y = 3x − 5 تحت المستوى y = 10؟ يلتقيان عند x = 5. يسار 5 يكون المستقيم أخفض فالحلول x < 5. الرسم والجبر (3x < 15 وx < 5) متفقان.",
               "3x − 5 < 10 : la droite est sous le niveau y = 10 à gauche de x = 5. Donc x < 5."))
    s = section(m, "Negative coefficient")
    s.append(fn_graph(lambda x: -2 * x + 1, (-6, 4), (-8, 14), hlines=[7], vlines=[-3], pts={"A": (-3, 7)}, tag="N2", label="y = −2x + 1 against y = 7"))
    s.append(T("Here the line goes down to the right. −2x + 1 ≥ 7 asks where the line is at or above y = 7. They meet at x = −3, and the line is higher to the LEFT. So x ≤ −3: the sign flipped when we divided by −2.",
               "هنا ينزل المستقيم نحو اليمين. −2x + 1 ≥ 7 تسأل أين يكون المستقيم عند المستوى y = 7 أو فوقه. يلتقيان عند x = −3 ويكون المستقيم أعلى إلى اليسار. إذن x ≤ −3: انقلبت الإشارة عندما قسمنا على −2.",
               "−2x + 1 ≥ 7 : la droite est au-dessus à gauche de x = −3, donc x ≤ −3 (le sens s'inverse)."))
    add_ex(m, [
        EX("", "", st("Solve 2x + 3 > 11 and show the solution as an interval.", "حلّ 2x + 3 > 11 واكتب المجموعة كمجال.", "Résous 2x + 3 > 11, écris l'intervalle."), [
            T("Subtract 3: 2x > 8. Divide by 2 (positive, so the sign stays): x > 4.", "نطرح 3: 2x > 8. نقسم على 2 (موجب فتبقى الإشارة): x > 4.", "2x > 8 → x > 4."), F("S = (4, +∞)"), F("Check x = 5: 13 > 11 ✓")]),
        EX("", "", st("Solve 7 − 2x ≤ 1.", "حلّ 7 − 2x ≤ 1.", "Résous 7 − 2x ≤ 1."), [
            T("Subtract 7: −2x ≤ −6. Divide by −2 and flip the sign: x ≥ 3.", "نطرح 7: −2x ≤ −6. نقسم على −2 ونعكس الإشارة: x ≥ 3.", "−2x ≤ −6 → x ≥ 3."), F("S = [3, +∞)"), F("Check x = 3: 7 − 6 = 1 ≤ 1 ✓")]),
        EX("", "", st("Solve the double inequality −3 < 2x − 1 ≤ 5.", "حلّ المتراجحة المزدوجة −3 < 2x − 1 ≤ 5.", "Résous −3 < 2x − 1 ≤ 5."), [
            T("Add 1 to all three parts: −2 < 2x ≤ 6. Divide all by 2: −1 < x ≤ 3.", "نضيف 1 إلى الأطراف الثلاثة: −2 < 2x ≤ 6. نقسم الكل على 2: −1 < x ≤ 3.", "−2 < 2x ≤ 6 → −1 < x ≤ 3."), F("S = (−1, 3]"), F("Check x = 3: 2·3 − 1 = 5 ✓ ; x = −1 is excluded: −3 < −3 is false")]),
        EX("", "", st("A phone plan costs 12 + 0.5t dollars for t minutes. For how many minutes does it cost at most 30 dollars?", "تكلفة باقة هاتف 12 + 0.5t دولارًا لمدة t دقيقة. لأي عدد من الدقائق تكون التكلفة 30 دولارًا على الأكثر؟", "Un forfait coûte 12 + 0,5t dollars. Pour quelle durée ≤ 30 dollars ?"), [
            T("We need 12 + 0.5t ≤ 30. Subtract 12: 0.5t ≤ 18. Divide by 0.5: t ≤ 36.", "نريد 12 + 0.5t ≤ 30. نطرح 12: 0.5t ≤ 18. نقسم على 0.5: t ≤ 36.", "0,5t ≤ 18 → t ≤ 36."), T("Time cannot be negative, so 0 ≤ t ≤ 36 minutes.", "الزمن لا يكون سالبًا إذن 0 ≤ t ≤ 36 دقيقة.", "0 ≤ t ≤ 36 min."), F("t ∈ [0, 36]")]),
        EX("", "", st("Solve the system of inequalities x − 2 > 1 and 3x ≤ 15.", "حلّ جملة المتراجحتين x − 2 > 1 وَ3x ≤ 15.", "Résous x − 2 > 1 et 3x ≤ 15."), [
            T("First: x > 3. Second: x ≤ 5. Both must hold, so we take the overlap of the two sets.", "الأولى: x > 3. الثانية: x ≤ 5. يجب أن تتحققا معًا فنأخذ تقاطع المجموعتين.", "x > 3 et x ≤ 5 : intersection."), F("S = (3, 5]")]),
    ])
