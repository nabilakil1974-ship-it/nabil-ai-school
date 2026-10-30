from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import fn_graph, section, add_ex, add_sec


def upgrade(m):
    s = section(m, "Tables and graphs")
    s.append(fn_graph(lambda x: 2 * x + 3, (-3, 5), (-4, 14), pts={"A": (0, 3), "B": (1, 5), "C": (4, 11)}, tag="W1", label="f(x) = 2x + 3"))
    s.append(T("Each input gives exactly one output, so each x has one point above it. A(0, 3): f(0) = 3. B(1, 5): f(1) = 5. C(4, 11): f(4) = 11, and 11 is the image of 4. Reading backwards: the preimage of 11 is 4.",
               "كل مدخل يعطي ناتجًا واحدًا فقط أي أن فوق كل x نقطة واحدة. A(0, 3): f(0) = 3. B(1, 5): f(1) = 5. C(4, 11): f(4) = 11 فالعدد 11 صورة العدد 4. بالقراءة العكسية: سابقة 11 هي 4.",
               "À chaque x correspond un seul point. C : f(4) = 11, donc 11 est l'image de 4 et 4 l'antécédent de 11."))
    add_sec(m, ("Is this a function? The vertical-line test", "هل هي دالة؟ اختبار المستقيم الشاقولي", "Est-ce une fonction ? Test de la verticale"), [
        T("A graph is the graph of a function only if every vertical line meets it at most once. The parabola y = x² passes the test. The circle x² + y² = 4 fails: the line x = 1 meets it twice, at y = √3 and y = −√3, so one input would have two outputs.",
          "يكون المنحنى تمثيلًا لدالة فقط إذا قطعه كل مستقيم شاقولي مرة واحدة على الأكثر. القطع المكافئ y = x² ينجح في الاختبار. أما الدائرة x² + y² = 4 فتفشل: المستقيم x = 1 يقطعها مرتين عند y = √3 وy = −√3 أي أن مدخلًا واحدًا له ناتجان.",
          "Une courbe représente une fonction si toute verticale la coupe au plus une fois. y = x² : oui ; le cercle x² + y² = 4 : non."),
        fn_graph(lambda x: x * x, (-3, 3), (-1, 9), pts={"A": (1, 1), "B": (-2, 4)}, tag="W2", label="y = x²: passes the test"),
        T("Each vertical line cuts y = x² once. Notice that two different inputs, −2 and 2, can share the same output 4. That is allowed. Two outputs for one input is not.",
          "كل مستقيم شاقولي يقطع y = x² مرة واحدة. لاحظ أن مدخلين مختلفين −2 و2 يمكن أن يشتركا في الناتج 4 وهذا مسموح. أما ناتجان لمدخل واحد فلا.",
          "Deux entrées (−2 et 2) peuvent avoir la même sortie : permis. Deux sorties pour une entrée : interdit."),
    ])
    add_ex(m, [
        EX("", "", st("f(x) = x² − 3x. Compute f(0), f(2), f(−1) and f(1/2).", "f(x) = x² − 3x. احسب f(0) وf(2) وf(−1) وf(1/2).", "f(x) = x² − 3x : f(0), f(2), f(−1), f(1/2)."), [
            T("f(0) = 0. f(2) = 4 − 6 = −2. f(−1) = 1 + 3 = 4.", "f(0) = 0. f(2) = 4 − 6 = −2. f(−1) = 1 + 3 = 4.", "f(0) = 0 ; f(2) = −2 ; f(−1) = 4."), T("f(1/2) = 1/4 − 3/2 = 1/4 − 6/4 = −5/4.", "f(1/2) = 1/4 − 3/2 = 1/4 − 6/4 = −5/4.", "f(1/2) = −5/4."), F("0, −2, 4, −5/4")]),
        EX("", "", st("Find the domain of f(x) = 1/(x − 2) and of g(x) = √(x − 1).", "جد مجال f(x) = 1/(x − 2) وg(x) = √(x − 1).", "Domaine de 1/(x − 2) et de √(x − 1)."), [
            T("1/(x − 2): the denominator cannot be 0, so x ≠ 2: ℝ \\ {2}.", "1/(x − 2): المقام لا يساوي 0 إذن x ≠ 2: ℝ \\ {2}.", "x ≠ 2."), T("√(x − 1): the radicand must be ≥ 0, so x ≥ 1: [1, +∞).", "√(x − 1): ما تحت الجذر ≥ 0 إذن x ≥ 1: [1, +∞).", "x ≥ 1."), F("ℝ \\ {2}      [1, +∞)")]),
        EX("", "", st("Find the preimages of 0 and of 5 for f(x) = x² − 4.", "جد سوابق 0 و5 للدالة f(x) = x² − 4.", "Antécédents de 0 et de 5 pour f(x) = x² − 4."), [
            T("f(x) = 0: x² = 4, so x = 2 or x = −2: two preimages.", "f(x) = 0: x² = 4 إذن x = 2 أو x = −2: سابقتان.", "x² = 4 : x = ±2."), T("f(x) = 5: x² = 9, so x = 3 or x = −3.", "f(x) = 5: x² = 9 إذن x = 3 أو x = −3.", "x² = 9 : x = ±3."), F("0: ±2      5: ±3")]),
        EX("", "", st("A taxi charges 2 dollars plus 1.5 dollars per km. Write the cost function and find the cost of 8 km and the distance for 20 dollars.", "سيارة أجرة تتقاضى 2 دولار زائد 1.5 دولار للكيلومتر. اكتب دالة التكلفة واحسب تكلفة 8 كم والمسافة لـ 20 دولارًا.", "Un taxi : 2 $ + 1,5 $/km. Fonction coût, coût de 8 km, distance pour 20 $."), [
            T("C(d) = 2 + 1.5d. For 8 km: C(8) = 2 + 12 = 14 dollars.", "C(d) = 2 + 1.5d. من أجل 8 كم: C(8) = 2 + 12 = 14 دولارًا.", "C(8) = 14 $."), T("For 20 dollars: 2 + 1.5d = 20, so 1.5d = 18 and d = 12 km.", "من أجل 20 دولارًا: 2 + 1.5d = 20 إذن 1.5d = 18 وd = 12 كم.", "1,5d = 18 → d = 12 km."), F("C(d) = 2 + 1.5d      C(8) = 14      d = 12")]),
    ])
