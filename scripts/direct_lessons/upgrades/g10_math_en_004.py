from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import section, add_ex, add_sec, fn_graph
from scripts.direct_lessons.draw import bars


def upgrade(m):
    s = section(m, "Repeated multiplication")
    s.append(bars(["2⁰", "2¹", "2²", "2³", "2⁴", "2⁵"], [1, 2, 4, 8, 16, 32], tag="P1", title="Powers of 2"))
    s.append(T("Each bar is double the previous one: 1, 2, 4, 8, 16, 32. Repeated multiplication grows very fast. 2⁵ means 2 × 2 × 2 × 2 × 2 = 32: the exponent counts how many times the base is used as a factor.",
               "كل عمود ضعف سابقه: 1 و2 و4 و8 و16 و32. الضرب المتكرر ينمو بسرعة كبيرة. 2⁵ تعني 2 × 2 × 2 × 2 × 2 = 32: الأس يعدّ كم مرة يُستعمل الأساس عاملًا.",
               "Chaque barre double la précédente. 2⁵ = 2 × 2 × 2 × 2 × 2 = 32 : l'exposant compte les facteurs."))
    s = section(m, "Zero and negative exponents")
    s.append(fn_graph(lambda x: 2 ** x, (-4, 4), (-1, 17), pts={"A": (-2, 0.25), "B": (0, 1), "C": (3, 8)}, hlines=[0], tag="P2", label="2ˣ continued to the left"))
    s.append(T("Going left, each step halves the value: 2² = 4, 2¹ = 2, 2⁰ = 1, 2⁻¹ = 1/2, 2⁻² = 1/4. This is why a⁰ = 1 and a⁻ⁿ = 1/aⁿ: they keep the pattern going. The curve never reaches 0, and negative exponents give small positive numbers, never negative ones.",
               "عند التحرك يسارًا تنصف كل خطوة القيمة: 2² = 4 و2¹ = 2 و2⁰ = 1 و2⁻¹ = 1/2 و2⁻² = 1/4. لهذا a⁰ = 1 وa⁻ⁿ = 1/aⁿ: فهما يحافظان على النمط. لا يبلغ المنحنى 0 والأسس السالبة تعطي أعدادًا موجبة صغيرة لا سالبة.",
               "Vers la gauche, on divise par 2 à chaque pas : 2⁰ = 1, 2⁻¹ = 1/2, 2⁻² = 1/4. D'où a⁰ = 1 et a⁻ⁿ = 1/aⁿ."))
    add_sec(m, ("Scientific notation", "الكتابة العلمية", "Notation scientifique"), [
        T("Very big or very small numbers are written a × 10ⁿ with 1 ≤ a < 10. Example: 4 500 000 = 4.5 × 10⁶ (the decimal point moved 6 places left). And 0.00032 = 3.2 × 10⁻⁴ (moved 4 places right). The distance from the Earth to the Sun is about 1.5 × 10⁸ km.",
          "الأعداد الكبيرة جدًا أو الصغيرة جدًا تُكتب a × 10ⁿ حيث 1 ≤ a < 10. مثال: 4 500 000 = 4.5 × 10⁶ (انتقلت الفاصلة 6 منازل يسارًا). و0.00032 = 3.2 × 10⁻⁴ (انتقلت 4 منازل يمينًا). المسافة من الأرض إلى الشمس نحو 1.5 × 10⁸ كم.",
          "Notation a × 10ⁿ, 1 ≤ a < 10 : 4 500 000 = 4,5 × 10⁶ ; 0,00032 = 3,2 × 10⁻⁴."),
        F("(3 × 10⁴)(2 × 10³) = 6 × 10⁷"),
    ])
    add_ex(m, [
        EX("", "", st("Simplify (2x³)² and (a²b)³.", "بسّط (2x³)² وَ(a²b)³.", "Simplifie (2x³)² et (a²b)³."), [
            T("(2x³)² = 2² · (x³)² = 4x⁶.", "(2x³)² = 2² · (x³)² = 4x⁶.", "= 4x⁶."), T("(a²b)³ = (a²)³ · b³ = a⁶b³.", "(a²b)³ = (a²)³ · b³ = a⁶b³.", "= a⁶b³."), F("4x⁶      a⁶b³")]),
        EX("", "", st("Compute 2⁵ / 2⁷ and 3⁻².", "احسب 2⁵ / 2⁷ وَ3⁻².", "Calcule 2⁵ / 2⁷ et 3⁻²."), [
            T("2⁵/2⁷ = 2⁵⁻⁷ = 2⁻² = 1/4.", "2⁵/2⁷ = 2⁵⁻⁷ = 2⁻² = 1/4.", "2⁻² = 1/4."), T("3⁻² = 1/3² = 1/9.", "3⁻² = 1/3² = 1/9.", "1/9."), F("1/4      1/9")]),
        EX("", "", st("Write in scientific notation: 7 200 000 and 0.0045.", "اكتب بالكتابة العلمية: 7 200 000 وَ0.0045.", "Notation scientifique de 7 200 000 et 0,0045."), [
            T("7 200 000 = 7.2 × 10⁶ (6 places). 0.0045 = 4.5 × 10⁻³ (3 places to the right).", "7 200 000 = 7.2 × 10⁶ (6 منازل). 0.0045 = 4.5 × 10⁻³ (3 منازل يمينًا).", "7,2 × 10⁶ ; 4,5 × 10⁻³."), F("7.2 × 10⁶      4.5 × 10⁻³")]),
        EX("", "", st("A bacterium divides into 2 every hour. How many are there after 10 hours starting from one? After how many hours do we first exceed 1000?", "تنقسم بكتيريا إلى اثنتين كل ساعة. كم عددها بعد 10 ساعات إذا بدأنا بواحدة؟ بعد كم ساعة يتجاوز العدد 1000 لأول مرة؟", "Une bactérie double chaque heure : après 10 h ? Quand dépasse-t-on 1000 ?"), [
            T("After n hours there are 2ⁿ bacteria. After 10 hours: 2¹⁰ = 1024.", "بعد n ساعة يوجد 2ⁿ بكتيريا. بعد 10 ساعات: 2¹⁰ = 1024.", "2¹⁰ = 1024."), T("2⁹ = 512 < 1000 and 2¹⁰ = 1024 > 1000, so the first time is after 10 hours.", "2⁹ = 512 < 1000 وَ2¹⁰ = 1024 > 1000 إذن أول مرة بعد 10 ساعات.", "2⁹ = 512, 2¹⁰ = 1024 : 10 h."), F("1024 bacteria; more than 1000 first at n = 10")]),
    ])
