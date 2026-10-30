"""Upgrade: Exponential functions — real graphs, richer explanation, many fully worked exercises."""
import math
from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import fn_graph, section


def upgrade(m):
    sec = section(m, "Definition")
    sec.append(fn_graph(lambda x: 2 ** x, (-4, 4), (-1, 9), pts={"A": (0, 1), "B": (3, 8)},
                        curves=[lambda x: 0.5 ** x], hlines=[0], tag="E1", label="2ˣ (red) and (1/2)ˣ (dashed)"))
    sec.append(T("Look at the board. Both curves pass through (0, 1) because a⁰ = 1. The red curve climbs fast on the right: 2³ = 8. The dashed curve is its mirror image in the y-axis, because (1/2)ˣ = 2⁻ˣ. Both stay above the x-axis forever: the x-axis is a horizontal asymptote.",
                 "انظر إلى اللوح. المنحنيان يمران بالنقطة (0, 1) لأن a⁰ = 1. المنحنى الأحمر يصعد بسرعة نحو اليمين: 2³ = 8. والمنحنى المتقطع هو صورته في مرآة محور الترتيب لأن (1/2)ˣ = 2⁻ˣ. كلاهما يبقى فوق محور الفواصل دائمًا: محور الفواصل مقارب أفقي.",
                 "Regarde le tableau. Les deux courbes passent par (0 ; 1) car a⁰ = 1. La rouge monte vite à droite : 2³ = 8. La pointillée est son symétrique par rapport à l'axe des ordonnées, car (1/2)ˣ = 2⁻ˣ. Toutes deux restent au-dessus de l'axe des abscisses : c'est une asymptote horizontale."))

    sec = section(m, "Growth or decay")
    sec.append(fn_graph(lambda x: math.e ** x, (-3, 3), (-1, 12), pts={"A": (0, 1), "B": (1, round(math.e, 2)), "C": (2, round(math.e ** 2, 2))},
                        hlines=[0], tag="E2", label="eˣ"))
    sec.append(T("The most important base is e ≈ 2.718. On eˣ, each step of 1 to the right multiplies the height by about 2.7: from 1 to 2.72 to 7.39. This is why growth looks slow at first and then explodes. Variation table: eˣ is increasing on all of ℝ, tends to 0 on the left and to +∞ on the right.",
                 "أهم أساس هو e ≈ 2.718. على المنحنى eˣ كل خطوة بمقدار 1 نحو اليمين تضرب الارتفاع في 2.7 تقريبًا: من 1 إلى 2.72 إلى 7.39. لهذا يبدو النمو بطيئًا في البداية ثم ينفجر. جدول التغيرات: eˣ متزايدة على ℝ كلها، تؤول إلى 0 عند −∞ وإلى +∞ عند +∞.",
                 "La base la plus importante est e ≈ 2,718. Sur eˣ, chaque pas de 1 vers la droite multiplie la hauteur par environ 2,7 : de 1 à 2,72 puis 7,39. Tableau : eˣ est croissante sur ℝ, tend vers 0 en −∞ et vers +∞ en +∞."))
    sec.append(F("x → −∞ : eˣ → 0      x → +∞ : eˣ → +∞      (eˣ)′ = eˣ > 0"))

    sec = section(m, "Inverse of ln")
    sec.append(fn_graph(lambda x: math.e ** x, (-3, 5), (-3, 6), pts={"A": (0, 1), "B": (1, 0)},
                        curves=[lambda x: math.log(x), lambda x: x], hlines=[0], vlines=[0], tag="E3", label="eˣ (red), ln x and y = x (dashed)"))
    sec.append(T("The red curve eˣ and the dashed curve ln x are mirror images across the line y = x. The point (0, 1) on eˣ becomes (1, 0) on ln x: that is the same statement as e⁰ = 1 and ln 1 = 0. The y-axis is the asymptote of ln x.",
                 "المنحنى الأحمر eˣ والمنحنى المتقطع ln x صورتان متناظرتان بالنسبة إلى المستقيم y = x. النقطة (0, 1) على eˣ تصبح (1, 0) على ln x، وهذا هو نفسه e⁰ = 1 وln 1 = 0. محور الترتيب مقارب للمنحنى ln x.",
                 "La courbe rouge eˣ et la pointillée ln x sont symétriques par rapport à la droite y = x. Le point (0 ; 1) devient (1 ; 0) : c'est e⁰ = 1 et ln 1 = 0. L'axe des ordonnées est asymptote de ln x."))

    sec = section(m, "Graph transformations")
    sec.append(fn_graph(lambda x: math.e ** (x - 2) + 3, (-3, 6), (-1, 12), pts={"A": (2, 4)},
                        curves=[lambda x: math.e ** x], hlines=[3], tag="E4", label="e^(x−2) + 3 (red), eˣ (dashed)"))
    sec.append(T("Compare the red curve with the dashed eˣ. The whole picture slid 2 units right and 3 units up. The key point (0, 1) moved to (2, 4), and the asymptote moved from y = 0 to y = 3. Always move the asymptote with the curve.",
                 "قارن المنحنى الأحمر بالمنحنى المتقطع eˣ. الصورة كلها انزلقت وحدتين إلى اليمين وثلاث وحدات إلى الأعلى. النقطة (0, 1) انتقلت إلى (2, 4) والمقارب انتقل من y = 0 إلى y = 3. نحرّك المقارب دائمًا مع المنحنى.",
                 "Compare la rouge à eˣ en pointillés : tout a glissé de 2 vers la droite et de 3 vers le haut. Le point (0 ; 1) est devenu (2 ; 4) et l'asymptote est passée de y = 0 à y = 3. Déplace toujours l'asymptote avec la courbe."))

    sec = section(m, "Growth model")
    t800 = math.log(1.6) / 0.03
    sec.append(fn_graph(lambda t: 500 * math.exp(0.03 * t), (0, 30), (0, 1300), pts={"P": (0, 500), "Q": (round(t800, 1), 800)},
                        hlines=[800], tag="E5", label="P(t) = 500e^(0.03t)"))
    sec.append(T("The graph shows the population growing from 500. We read the answer on the graph first: the curve meets the level 800 near t ≈ 15.7. The algebra confirms it: t = ln 1.6 / 0.03 ≈ 15.67. A graph gives the idea, the equation gives the exact value.",
                 "يبيّن الرسم عددًا يتزايد من 500. نقرأ الجواب من الرسم أولًا: يقطع المنحنى المستوى 800 قرب t ≈ 15.7. والجبر يؤكد: t = ln 1.6 / 0.03 ≈ 15.67. الرسم يعطي الفكرة والمعادلة تعطي القيمة الدقيقة.",
                 "Le graphique montre une population qui croît depuis 500. On lit d'abord : la courbe atteint 800 vers t ≈ 15,7. Le calcul confirme : t = ln 1,6 / 0,03 ≈ 15,67. Le graphique donne l'idée, l'équation la valeur exacte."))

    sec = section(m, "Quadratic in eˣ")
    z1, z2 = math.log(2), math.log(3)
    sec.append(fn_graph(lambda x: math.exp(2 * x) - 5 * math.exp(x) + 6, (-1.5, 2), (-2, 8), pts={"A": (round(z1, 2), 0), "B": (round(z2, 2), 0)},
                        tag="E6", label="h(x) = e^(2x) − 5eˣ + 6"))
    sec.append(T("The curve crosses the x-axis exactly twice, at x = ln 2 ≈ 0.69 and x = ln 3 ≈ 1.10. That matches the two roots u = 2 and u = 3 we found. The dip between the roots is where u² − 5u + 6 is negative.",
                 "يقطع المنحنى محور الفواصل مرتين تمامًا عند x = ln 2 ≈ 0.69 وx = ln 3 ≈ 1.10. وهذا يوافق الجذرين u = 2 وu = 3 اللذين وجدناهما. المنطقة الواقعة بين الجذرين هي حيث u² − 5u + 6 سالب.",
                 "La courbe coupe l'axe des abscisses exactement deux fois, en x = ln 2 ≈ 0,69 et x = ln 3 ≈ 1,10, ce qui correspond aux racines u = 2 et u = 3. Entre les deux racines, u² − 5u + 6 est négatif."))

    m.EXERCISES[:] = [
        EX("1", "", st("Solve 2ˣ = 16 and 3^(x−1) = 9.", "حلّ 2ˣ = 16 و3^(x−1) = 9.", "Résous 2ˣ = 16 et 3^(x−1) = 9."), [
            T("Write each right side as a power of the same base. 16 = 2⁴, so 2ˣ = 2⁴ and x = 4.", "نكتب الطرف الأيمن قوة للأساس نفسه. 16 = 2⁴ فيكون 2ˣ = 2⁴ وx = 4.", "On écrit 16 = 2⁴, donc x = 4."),
            T("Second: 9 = 3², so 3^(x−1) = 3². Then x − 1 = 2 and x = 3.", "الثانية: 9 = 3² إذن 3^(x−1) = 3². فيكون x − 1 = 2 وx = 3.", "9 = 3² donc x − 1 = 2 et x = 3."),
            F("x = 4      x = 3"), F("Check: 2⁴ = 16 ✓      3^(3−1) = 3² = 9 ✓")]),
        EX("2", "", st("Solve e^(3x) = 7 and 4e^(−x) = 9.", "حلّ e^(3x) = 7 و4e^(−x) = 9.", "Résous e^(3x) = 7 et 4e^(−x) = 9."), [
            T("Take ln of both sides of e^(3x) = 7: 3x = ln 7, so x = (ln 7)/3 ≈ 0.649.", "نطبق ln على الطرفين: 3x = ln 7 إذن x = (ln 7)/3 ≈ 0.649.", "On applique ln : 3x = ln 7, x = (ln 7)/3 ≈ 0,649."),
            T("For the second, isolate the exponential first: e^(−x) = 9/4. Then −x = ln(9/4), so x = −ln(9/4) = ln(4/9) ≈ −0.811.", "للثانية نعزل الأسية أولًا: e^(−x) = 9/4. إذن −x = ln(9/4) وx = −ln(9/4) = ln(4/9) ≈ −0.811.", "On isole : e^(−x) = 9/4, donc x = −ln(9/4) = ln(4/9) ≈ −0,811."),
            F("x = (ln 7)/3 ≈ 0.649      x = ln(4/9) ≈ −0.811"), F("Check: e^(3·0.649) ≈ e^1.946 ≈ 7 ✓      4e^(0.811) ≈ 4 × 2.25 = 9 ✓")]),
        EX("3", "", st("Solve e^(2x) − 7eˣ + 12 = 0.", "حلّ e^(2x) − 7eˣ + 12 = 0.", "Résous e^(2x) − 7eˣ + 12 = 0."), [
            T("Put u = eˣ with u > 0. Then e^(2x) = u² and the equation becomes u² − 7u + 12 = 0.", "نضع u = eˣ مع u > 0. فيصبح e^(2x) = u² والمعادلة u² − 7u + 12 = 0.", "On pose u = eˣ > 0 : u² − 7u + 12 = 0."),
            T("Factor: (u − 3)(u − 4) = 0, so u = 3 or u = 4. Both are positive, so both are accepted.", "نحلّل: (u − 3)(u − 4) = 0 إذن u = 3 أو u = 4. كلاهما موجب فيُقبلان.", "(u − 3)(u − 4) = 0 : u = 3 ou 4, tous deux > 0."),
            T("Return to x: eˣ = 3 gives x = ln 3, and eˣ = 4 gives x = ln 4.", "نعود إلى x: eˣ = 3 تعطي x = ln 3 وeˣ = 4 تعطي x = ln 4.", "x = ln 3 ou x = ln 4."),
            F("x = ln 3 ≈ 1.099      x = ln 4 ≈ 1.386"), F("Check x = ln 3: 9 − 21 + 12 = 0 ✓")]),
        EX("4", "", st("For f(x) = 2e^(x−1) − 4 give the domain, the range and the horizontal asymptote, then the zero of f.", "أعطِ مجال f(x) = 2e^(x−1) − 4 ومداها ومقاربها الأفقي ثم صفرها.", "Pour f(x) = 2e^(x−1) − 4 : domaine, image, asymptote, puis zéro."), [
            T("The exponential is defined for every real x, so the domain is ℝ.", "الأسية معرّفة لكل x حقيقي فالمجال ℝ.", "Domaine : ℝ."),
            T("e^(x−1) > 0, so 2e^(x−1) > 0 and f(x) > −4. The range is (−4, +∞) and the asymptote is y = −4 (as x → −∞).", "e^(x−1) > 0 إذن 2e^(x−1) > 0 وf(x) > −4. المدى (−4, +∞) والمقارب y = −4 عند −∞.", "f(x) > −4 : image ]−4 ; +∞[, asymptote y = −4."),
            T("Zero: 2e^(x−1) = 4, e^(x−1) = 2, x − 1 = ln 2, so x = 1 + ln 2 ≈ 1.693.", "الصفر: 2e^(x−1) = 4 وe^(x−1) = 2 وx − 1 = ln 2 إذن x = 1 + ln 2 ≈ 1.693.", "2e^(x−1) = 4 → x = 1 + ln 2 ≈ 1,693."),
            fn_graph(lambda x: 2 * math.exp(x - 1) - 4, (-3, 4), (-6, 10), pts={"Z": (round(1 + math.log(2), 2), 0)}, hlines=[-4], tag="X4", label="f(x) = 2e^(x−1) − 4"),
            F("Dom = ℝ      Range = (−4, +∞)      asymptote y = −4      zero x = 1 + ln 2")]),
        EX("5", "", st("Solve 7e^(2x) = 20 exactly and give a decimal value.", "حلّ 7e^(2x) = 20 بدقة وأعطِ قيمة عشرية.", "Résous 7e^(2x) = 20 exactement puis en décimal."), [
            T("Divide by 7: e^(2x) = 20/7. Apply ln: 2x = ln(20/7). Divide by 2.", "نقسم على 7: e^(2x) = 20/7. نطبق ln: 2x = ln(20/7). ثم نقسم على 2.", "e^(2x) = 20/7 → 2x = ln(20/7)."),
            F("x = (1/2) ln(20/7) ≈ (1/2)(1.0498) ≈ 0.525"), F("Check: 7e^(1.0498) = 7 × 2.857 ≈ 20 ✓")]),
        EX("6", "", st("Solve the inequality eˣ > 5 and the inequality 3e^(−x) ≤ 1.", "حلّ المتراجحة eˣ > 5 والمتراجحة 3e^(−x) ≤ 1.", "Résous eˣ > 5 et 3e^(−x) ≤ 1."), [
            T("The function ln is increasing, so applying it keeps the direction: eˣ > 5 gives x > ln 5 ≈ 1.609.", "الدالة ln متزايدة فتحافظ على اتجاه المتراجحة: eˣ > 5 تعطي x > ln 5 ≈ 1.609.", "ln est croissante : x > ln 5 ≈ 1,609."),
            T("Second: e^(−x) ≤ 1/3, so −x ≤ ln(1/3) = −ln 3, and multiplying by −1 reverses the sign: x ≥ ln 3 ≈ 1.099.", "الثانية: e^(−x) ≤ 1/3 إذن −x ≤ ln(1/3) = −ln 3. وبضرب الطرفين في −1 ينعكس الاتجاه: x ≥ ln 3 ≈ 1.099.", "e^(−x) ≤ 1/3 → −x ≤ −ln 3 → x ≥ ln 3."),
            F("S₁ = (ln 5, +∞)      S₂ = [ln 3, +∞)")]),
        EX("7", "", st("A culture has 500 bacteria and grows as P(t) = 500e^(0.03t) (t in hours). When does it double? What is P(24)?", "مزرعة فيها 500 بكتيريا تنمو وفق P(t) = 500e^(0.03t) (t بالساعات). متى يتضاعف عددها؟ وما قيمة P(24)؟", "Une culture de 500 bactéries suit P(t) = 500e^(0,03t). Quand double-t-elle ? Que vaut P(24) ?"), [
            T("Doubling means P(t) = 1000, so e^(0.03t) = 2 and 0.03t = ln 2.", "التضاعف يعني P(t) = 1000 إذن e^(0.03t) = 2 وهذا يعطي 0.03t = ln 2.", "Doubler : e^(0,03t) = 2."),
            F("t = ln 2 / 0.03 ≈ 0.693 / 0.03 ≈ 23.1 hours"),
            T("For t = 24: P(24) = 500e^(0.72) ≈ 500 × 2.054 ≈ 1027 bacteria — just over double, matching the doubling time of 23.1 h.", "عند t = 24: P(24) = 500e^(0.72) ≈ 500 × 2.054 ≈ 1027 بكتيريا، أي أكثر قليلًا من الضعف وهذا يوافق زمن التضاعف 23.1 ساعة.", "P(24) = 500e^(0,72) ≈ 1027, cohérent avec 23,1 h."),
            F("P(24) ≈ 1027")]),
        EX("8", "", st("Error detective: a student solves e^(2x) − 5eˣ + 6 = 0 by writing 2x − 5x + 6 = 0. Find the mistake and solve correctly.", "المحقق: حلّ طالب e^(2x) − 5eˣ + 6 = 0 فكتب 2x − 5x + 6 = 0. جد الخطأ وحلّ بشكل صحيح.", "Détective : un élève écrit 2x − 5x + 6 = 0. Trouve l'erreur et résous."), [
            T("The student removed the letter e as if it were a common factor. But e^(2x) − 5eˣ + 6 is not a product: you cannot cancel e from a sum of different exponentials.", "حذف الطالب الحرف e وكأنه عامل مشترك. لكن المقدار ليس جداءً، ولا يمكن حذف e من مجموع أسّيات مختلفة.", "L'élève a supprimé e comme s'il était facteur commun : impossible dans une somme."),
            T("The correct method is u = eˣ: u² − 5u + 6 = 0 gives u = 2 or 3, hence x = ln 2 or x = ln 3. The graph of h(x) on the board crosses the x-axis at exactly these two points.", "الطريقة الصحيحة u = eˣ: u² − 5u + 6 = 0 تعطي u = 2 أو 3 فيكون x = ln 2 أو x = ln 3. ومنحنى h(x) على اللوح يقطع محور الفواصل عند هاتين النقطتين فقط.", "Bonne méthode : u = eˣ → x = ln 2 ou ln 3, comme le montre la courbe."),
            F("x = ln 2 ≈ 0.693      x = ln 3 ≈ 1.099")]),
    ]
