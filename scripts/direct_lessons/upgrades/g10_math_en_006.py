from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import section, add_ex, add_sec
from scripts.direct_lessons.draw import numberline


def upgrade(m):
    s = section(m, "The equation |x − a| = r")
    s.append(numberline(-2, 10, marks={"a = 4": 4, "1": 1, "7": 7}, tag="A1"))
    s.append(T("|x − 4| = 3 asks: which numbers are at distance 3 from 4? Walk 3 steps left to reach 1, and 3 steps right to reach 7. So x = 1 or x = 7. Distance is the key idea; the algebra x − 4 = ±3 says the same thing.",
               "|x − 4| = 3 تسأل: ما الأعداد التي تبعد 3 عن 4؟ نمشي 3 خطوات يسارًا فنصل 1 و3 خطوات يمينًا فنصل 7. إذن x = 1 أو x = 7. المسافة هي الفكرة الأساسية؛ والجبر x − 4 = ±3 يقول الشيء نفسه.",
               "|x − 4| = 3 : les nombres à distance 3 de 4 : 1 et 7."))
    add_sec(m, ("Inequalities with absolute value", "المتراجحات والقيمة المطلقة", "Inégalités avec valeur absolue"), [
        T("|x| < 2 means distance from 0 less than 2: −2 < x < 2, one interval between two open circles. But |x| > 2 means farther than 2 from 0: x < −2 or x > 2, two pieces going away in opposite directions.",
          "|x| < 2 تعني مسافة عن 0 أقل من 2: −2 < x < 2 أي مجال واحد بين دائرتين مفتوحتين. أما |x| > 2 فتعني أبعد من 2 عن 0: x < −2 أو x > 2 أي قطعتان تبتعدان في اتجاهين متعاكسين.",
          "|x| < 2 : −2 < x < 2. |x| > 2 : x < −2 ou x > 2."),
        numberline(-5, 5, intervals=[(-2, 2, False, False, "#2e7d32")], tag="A2"),
        numberline(-5, 5, intervals=[(None, -2, False, False, "#e53935"), (2, None, False, False, "#e53935")], tag="A3"),
        F("|x| < r ⟺ −r < x < r      |x| > r ⟺ x < −r or x > r"),
    ])
    add_ex(m, [
        EX("", "", st("Solve |x − 1| ≥ 3 and show it on a number line.", "حلّ |x − 1| ≥ 3 ومثّله على محور.", "Résous |x − 1| ≥ 3 et représente."), [
            T("Distance from 1 at least 3: x − 1 ≥ 3 or x − 1 ≤ −3, so x ≥ 4 or x ≤ −2.", "المسافة عن 1 لا تقل عن 3: x − 1 ≥ 3 أو x − 1 ≤ −3 إذن x ≥ 4 أو x ≤ −2.", "x ≥ 4 ou x ≤ −2."),
            numberline(-5, 7, intervals=[(None, -2, False, True, "#e53935"), (4, None, True, False, "#e53935")], tag="X1"), F("S = (−∞, −2] ∪ [4, +∞)")]),
        EX("", "", st("Solve |2x + 1| = 7.", "حلّ |2x + 1| = 7.", "Résous |2x + 1| = 7."), [
            T("2x + 1 = 7 gives x = 3, and 2x + 1 = −7 gives x = −4.", "2x + 1 = 7 تعطي x = 3 وَ2x + 1 = −7 تعطي x = −4.", "x = 3 ou x = −4."), F("x = 3 or x = −4"), F("Check: |7| = 7 ✓ and |−7| = 7 ✓")]),
        EX("", "", st("Round 3.14159 to the nearest hundredth and to 3 significant digits, then write the absolute error of 3.14.", "قرّب 3.14159 إلى أقرب جزء من مئة وإلى 3 أرقام معنوية ثم اكتب الخطأ المطلق للقيمة 3.14.", "Arrondis 3,14159 au centième ; erreur absolue de 3,14."), [
            T("Nearest hundredth: 3.14 (the next digit 1 is below 5). Three significant digits: 3.14 too.", "إلى أقرب جزء من مئة: 3.14 (الرقم التالي 1 أقل من 5). وبثلاثة أرقام معنوية: 3.14 أيضًا.", "3,14."), T("Absolute error = |3.14159 − 3.14| = 0.00159.", "الخطأ المطلق = |3.14159 − 3.14| = 0.00159.", "|3,14159 − 3,14| = 0,00159."), F("3.14      error 0.00159")]),
        EX("", "", st("A machine part must be 50 mm with tolerance 0.2 mm. Write the condition with |·| and the allowed interval.", "قطعة آلة يجب أن تكون 50 ملم بتفاوت 0.2 ملم. اكتب الشرط بالقيمة المطلقة والمجال المسموح.", "Pièce de 50 mm, tolérance 0,2 mm : condition et intervalle."), [
            T("|L − 50| ≤ 0.2 means 49.8 ≤ L ≤ 50.2.", "|L − 50| ≤ 0.2 تعني 49.8 ≤ L ≤ 50.2.", "|L − 50| ≤ 0,2."), numberline(49.4, 50.6, intervals=[(49.8, 50.2, True, True, "#2e7d32")], marks={"50": 50}, tag="X2", step=0.2), F("L ∈ [49.8, 50.2]")]),
    ])
