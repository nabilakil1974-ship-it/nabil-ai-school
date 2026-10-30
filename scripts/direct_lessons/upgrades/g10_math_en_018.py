from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import fn_graph, section, add_ex, add_sec


def upgrade(m):
    s = section(m, "Geometric meaning")
    s.append(fn_graph(lambda x: 9 - 2 * x, (-1, 7), (-3, 11), curves=[lambda x: x], pts={"P": (3, 3)}, tag="Q1", label="2x + y = 9 (red) and x − y = 0 (dashed)"))
    s.append(T("Each equation is a line. The solution of the system is the one point on both lines at once: P(3, 3). Check in 2x + y = 9: 6 + 3 = 9 ✓, and in x − y = 0: 3 − 3 = 0 ✓.",
               "كل معادلة مستقيم. حل الجملة هو النقطة الوحيدة الواقعة على المستقيمين معًا: P(3, 3). تحقق في 2x + y = 9: 6 + 3 = 9 ✓ وفي x − y = 0: 3 − 3 = 0 ✓.",
               "Chaque équation est une droite ; la solution est leur point commun P(3 ; 3). 6 + 3 = 9 ✓ ; 3 − 3 = 0 ✓."))
    add_ex(m, [
        EX("", "", st("Solve by substitution: y = 2x − 1 and x + y = 8.", "حلّ بالتعويض: y = 2x − 1 وَx + y = 8.", "Par substitution : y = 2x − 1 et x + y = 8."), [
            T("Replace y in the second equation: x + (2x − 1) = 8, so 3x = 9 and x = 3.", "نعوّض y في المعادلة الثانية: x + (2x − 1) = 8 إذن 3x = 9 وx = 3.", "x + 2x − 1 = 8 → x = 3."), T("Then y = 2 × 3 − 1 = 5.", "ثم y = 2 × 3 − 1 = 5.", "y = 5."), F("(3, 5)"), F("Check: 3 + 5 = 8 ✓")]),
        EX("", "", st("Solve by elimination: 3x + 2y = 16 and x − 2y = 0.", "حلّ بالحذف: 3x + 2y = 16 وَx − 2y = 0.", "Par élimination : 3x + 2y = 16 et x − 2y = 0."), [
            T("The y-terms are +2y and −2y: add the equations. 4x = 16, so x = 4.", "حدّا y هما +2y وَ−2y فنجمع المعادلتين. 4x = 16 إذن x = 4.", "On ajoute : 4x = 16."), T("From x − 2y = 0: y = x/2 = 2.", "من x − 2y = 0: y = x/2 = 2.", "y = 2."), F("(4, 2)"), F("Check: 12 + 4 = 16 ✓")]),
        EX("", "", st("Two numbers add to 25 and differ by 7. Find them.", "عددان مجموعهما 25 وفرقهما 7. جدهما.", "Deux nombres de somme 25 et de différence 7."), [
            T("x + y = 25 and x − y = 7. Add: 2x = 32, so x = 16. Then y = 25 − 16 = 9.", "x + y = 25 وَx − y = 7. نجمع: 2x = 32 إذن x = 16. ثم y = 25 − 16 = 9.", "2x = 32 → 16 et 9."), F("16 and 9"), F("Check: 16 + 9 = 25 ✓  16 − 9 = 7 ✓")]),
        EX("", "", st("3 pens and 2 notebooks cost 13 dollars; 2 pens and 3 notebooks cost 12 dollars. Find each price.", "3 أقلام ودفتران ثمنها 13 دولارًا؛ وقلمان و3 دفاتر ثمنها 12 دولارًا. جد سعر كل منهما.", "3 stylos + 2 cahiers = 13 $ ; 2 stylos + 3 cahiers = 12 $. Prix ?"), [
            T("Let p = pen, c = notebook: 3p + 2c = 13 and 2p + 3c = 12. Multiply the first by 3 and the second by 2: 9p + 6c = 39 and 4p + 6c = 24.", "ليكن p ثمن القلم وc ثمن الدفتر: 3p + 2c = 13 وَ2p + 3c = 12. نضرب الأولى في 3 والثانية في 2: 9p + 6c = 39 وَ4p + 6c = 24.", "×3 et ×2 : 9p + 6c = 39 ; 4p + 6c = 24."), T("Subtract: 5p = 15, so p = 3. Then 2c = 13 − 9 = 4, so c = 2.", "نطرح: 5p = 15 إذن p = 3. ثم 2c = 13 − 9 = 4 إذن c = 2.", "p = 3, c = 2."), F("pen = 3 $, notebook = 2 $"), F("Check: 9 + 4 = 13 ✓  6 + 6 = 12 ✓")]),
    ])
