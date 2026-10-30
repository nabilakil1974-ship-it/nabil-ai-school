import math
from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import fn_graph, section

PI = math.pi


def theory_extras(m, sec_sin, sec_arcsin, sec_arccos, sec_arctan, sec_comp):
    s = section(m, sec_sin)
    s.append(fn_graph(math.sin, (-PI, PI), (-1.6, 1.6), pts={"A": (round(PI / 2, 2), 1), "B": (round(-PI / 2, 2), -1)}, hlines=[1, -1], tag="T1", label="y = sin x"))
    s.append(T("Look at sin x. The horizontal line y = 0.5 cuts the curve many times, so one output comes from many inputs: sine is not one-to-one on ℝ. To invert it we keep only the piece from −π/2 to π/2 (between the two marked points), where it rises from −1 to 1 and is one-to-one.",
               "انظر إلى sin x. المستقيم الأفقي y = 0.5 يقطع المنحنى مرات كثيرة أي أن الناتج الواحد يأتي من مداخل كثيرة: الجيب ليس متباينًا على ℝ. لنعكسه نحتفظ بالقطعة من −π/2 إلى π/2 (بين النقطتين المعلّمتين) حيث ترتفع من −1 إلى 1 وتكون متباينة.",
               "Observe sin x : la droite y = 0,5 coupe la courbe plusieurs fois, sin n'est pas injective sur ℝ. On garde la portion de −π/2 à π/2, où elle monte de −1 à 1."))
    s = section(m, sec_arcsin)
    s.append(fn_graph(math.asin, (-1.4, 1.4), (-2, 2), curves=[math.sin, lambda x: x], pts={"A": (1, round(PI / 2, 2)), "B": (-1, round(-PI / 2, 2)), "C": (0.5, round(PI / 6, 2))}, tag="T2", label="arcsin x (red); sin x and y = x dashed"))
    s.append(T("The red curve arcsin x lives on [−1, 1] and its values go from −π/2 to π/2. It is the mirror image of the principal piece of sine across y = x. Point C: sin(π/6) = 0.5, so arcsin(0.5) = π/6 ≈ 0.52.",
               "المنحنى الأحمر arcsin x معرّف على [−1, 1] وقيمه من −π/2 إلى π/2. وهو صورة القطعة الأساسية من الجيب في مرآة y = x. النقطة C: sin(π/6) = 0.5 إذن arcsin(0.5) = π/6 ≈ 0.52.",
               "arcsin vit sur [−1 ; 1], ses valeurs sont dans [−π/2 ; π/2] ; symétrique de sin par rapport à y = x. C : arcsin(0,5) = π/6."))
    s = section(m, sec_arccos)
    s.append(fn_graph(math.acos, (-1.4, 1.4), (-0.5, 3.6), pts={"A": (1, 0), "B": (-1, round(PI, 2)), "C": (0, round(PI / 2, 2))}, tag="T3", label="arccos x"))
    s.append(T("arccos x goes from π at x = −1 down to 0 at x = 1, passing through (0, π/2). Its range is [0, π], not [−π/2, π/2]. It is decreasing, and arccos x + arcsin x = π/2 for every x in [−1, 1].",
               "arccos x ينزل من π عند x = −1 إلى 0 عند x = 1 مارًّا بـ (0, π/2). مداه [0, π] لا [−π/2, π/2]. وهو متناقص، وarccos x + arcsin x = π/2 لكل x في [−1, 1].",
               "arccos descend de π (x = −1) à 0 (x = 1), image [0 ; π] ; arccos x + arcsin x = π/2."))
    s = section(m, sec_arctan)
    s.append(fn_graph(math.atan, (-8, 8), (-2, 2), pts={"O": (0, 0), "A": (1, round(PI / 4, 2))}, hlines=[PI / 2, -PI / 2], tag="T4", label="arctan x"))
    s.append(T("arctan x is defined for every real x, increases slowly and flattens toward two horizontal asymptotes: y = π/2 on the right and y = −π/2 on the left. It never reaches them. Point A: tan(π/4) = 1, so arctan 1 = π/4.",
               "arctan x معرّف لكل x حقيقي، يتزايد ببطء ويتسطح نحو مقاربين أفقيين: y = π/2 يمينًا وy = −π/2 يسارًا ولا يبلغهما. النقطة A: tan(π/4) = 1 إذن arctan 1 = π/4.",
               "arctan est définie sur ℝ, croissante, avec deux asymptotes y = ±π/2. A : arctan 1 = π/4."))
    s = section(m, sec_comp)
    s.append(fn_graph(lambda x: math.asin(math.sin(x)), (-2 * PI, 2 * PI), (-2, 2), curves=[lambda x: x], tag="T5", label="arcsin(sin x): a zig-zag, not y = x"))
    s.append(T("This is the trap picture. arcsin(sin x) is NOT x for every x: it equals x only on [−π/2, π/2]. Outside, the graph zig-zags between −π/2 and π/2. For example sin(3π/4) = √2/2, and arcsin(√2/2) = π/4, not 3π/4.",
               "هذه صورة الفخ. arcsin(sin x) ليس x لكل x: يساوي x فقط على [−π/2, π/2]. خارجه يتعرّج المنحنى بين −π/2 وπ/2. مثلًا sin(3π/4) = √2/2 وarcsin(√2/2) = π/4 لا 3π/4.",
               "Piège : arcsin(sin x) = x seulement sur [−π/2 ; π/2] ; ailleurs, zigzag. arcsin(sin(3π/4)) = π/4."))


def exercises():
    return [
        EX("1", "", st("Evaluate arcsin(−√3/2), arccos(−1/2) and arctan(−1).", "احسب arcsin(−√3/2) وarccos(−1/2) وarctan(−1).", "Calcule arcsin(−√3/2), arccos(−1/2), arctan(−1)."), [
            T("arcsin asks: which angle in [−π/2, π/2] has sine −√3/2? It is −π/3.", "arcsin يسأل: أي زاوية في [−π/2, π/2] جيبها −√3/2؟ إنها −π/3.", "Angle de [−π/2 ; π/2] de sinus −√3/2 : −π/3."),
            T("arccos: which angle in [0, π] has cosine −1/2? It is 2π/3. arctan: which angle in (−π/2, π/2) has tangent −1? It is −π/4.", "arccos: أي زاوية في [0, π] جيب تمامها −1/2؟ إنها 2π/3. arctan: أي زاوية في (−π/2, π/2) ظلها −1؟ إنها −π/4.", "arccos : 2π/3 ; arctan : −π/4."),
            F("−π/3      2π/3      −π/4")]),
        EX("2", "", st("Simplify arcsin(sin(5π/6)), arccos(cos(−π/3)) and arctan(tan(π/3)).", "بسّط arcsin(sin(5π/6)) وarccos(cos(−π/3)) وarctan(tan(π/3)).", "Simplifie arcsin(sin(5π/6)), arccos(cos(−π/3)), arctan(tan(π/3))."), [
            T("5π/6 is outside [−π/2, π/2]. sin(5π/6) = 1/2, and the angle in the principal range with sine 1/2 is π/6. So the answer is π/6, not 5π/6.", "5π/6 خارج [−π/2, π/2]. sin(5π/6) = 1/2 والزاوية في المجال الأساسي التي جيبها 1/2 هي π/6. فالجواب π/6 لا 5π/6.", "5π/6 hors de [−π/2 ; π/2] : réponse π/6."),
            T("cos(−π/3) = 1/2 and π/3 is in [0, π], so arccos(cos(−π/3)) = π/3. Finally π/3 is in (−π/2, π/2), so arctan(tan(π/3)) = π/3.", "cos(−π/3) = 1/2 وπ/3 في [0, π] إذن arccos(cos(−π/3)) = π/3. وأخيرًا π/3 في (−π/2, π/2) إذن arctan(tan(π/3)) = π/3.", "π/3 ∈ [0 ; π] et ∈ ]−π/2 ; π/2[."),
            F("π/6      π/3      π/3")]),
        EX("3", "", st("Compute sin(arccos(3/5)) and cos(arcsin(3/5)).", "احسب sin(arccos(3/5)) وcos(arcsin(3/5)).", "Calcule sin(arccos(3/5)) et cos(arcsin(3/5))."), [
            T("Let θ = arccos(3/5): θ ∈ [0, π], cos θ = 3/5. Then sin θ ≥ 0 and sin θ = √(1 − 9/25) = √(16/25) = 4/5.", "ليكن θ = arccos(3/5): θ ∈ [0, π] وcos θ = 3/5. إذن sin θ ≥ 0 وsin θ = √(1 − 9/25) = √(16/25) = 4/5.", "θ = arccos(3/5) : sin θ = 4/5."),
            T("Let φ = arcsin(3/5): φ ∈ [−π/2, π/2], so cos φ ≥ 0 and cos φ = √(1 − 9/25) = 4/5.", "ليكن φ = arcsin(3/5): φ ∈ [−π/2, π/2] إذن cos φ ≥ 0 وcos φ = √(1 − 9/25) = 4/5.", "cos φ = 4/5."),
            F("sin(arccos(3/5)) = 4/5      cos(arcsin(3/5)) = 4/5"), T("Both equal 4/5 because θ + φ = π/2.", "كلاهما 4/5 لأن θ + φ = π/2.", "θ + φ = π/2.")]),
        EX("4", "", st("Solve arctan(2x − 1) = π/4 and arcsin(2x) = π/6.", "حلّ arctan(2x − 1) = π/4 وarcsin(2x) = π/6.", "Résous arctan(2x − 1) = π/4 et arcsin(2x) = π/6."), [
            T("Apply tan: 2x − 1 = tan(π/4) = 1, so x = 1. Check: arctan(1) = π/4 ✓.", "نطبق tan: 2x − 1 = tan(π/4) = 1 إذن x = 1. تحقق: arctan(1) = π/4 ✓.", "2x − 1 = 1 → x = 1."),
            T("Apply sin: 2x = sin(π/6) = 1/2, so x = 1/4. The value 1/2 is in [−1, 1], so the solution is valid.", "نطبق sin: 2x = sin(π/6) = 1/2 إذن x = 1/4. والقيمة 1/2 في [−1, 1] فالحل مقبول.", "2x = 1/2 → x = 1/4."),
            F("x = 1      x = 1/4")]),
        EX("5", "", st("Find the domain and the derivative of arcsin(2x − 1), and the derivative of arctan(3x).", "جد مجال ومشتقة arcsin(2x − 1) ومشتقة arctan(3x).", "Domaine et dérivée de arcsin(2x − 1) ; dérivée de arctan(3x)."), [
            T("Domain: −1 ≤ 2x − 1 ≤ 1 gives 0 ≤ x ≤ 1. Derivative by the chain rule: 2/√(1 − (2x − 1)²) = 2/√(4x − 4x²) = 1/√(x − x²), valid for 0 < x < 1.", "المجال: −1 ≤ 2x − 1 ≤ 1 تعطي 0 ≤ x ≤ 1. المشتقة بقاعدة السلسلة: 2/√(1 − (2x − 1)²) = 2/√(4x − 4x²) = 1/√(x − x²) وتصح لـ 0 < x < 1.", "Domaine [0 ; 1], dérivée 1/√(x − x²) sur ]0 ; 1[."),
            T("For arctan(3x): 3/(1 + 9x²), defined for every real x.", "من أجل arctan(3x): 3/(1 + 9x²) ومعرّفة لكل x حقيقي.", "3/(1 + 9x²)."),
            F("[arcsin(2x − 1)]′ = 1/√(x − x²)      [arctan(3x)]′ = 3/(1 + 9x²)")]),
        EX("6", "", st("Why is arcsin(sin(3π/4)) ≠ 3π/4? Compute it.", "لماذا arcsin(sin(3π/4)) ≠ 3π/4؟ احسبها.", "Pourquoi arcsin(sin(3π/4)) ≠ 3π/4 ? Calcule."), [
            T("3π/4 ≈ 2.36 is greater than π/2 ≈ 1.57, so it is outside the range of arcsin.", "3π/4 ≈ 2.36 أكبر من π/2 ≈ 1.57 فهي خارج مدى arcsin.", "3π/4 > π/2 : hors du domaine principal."),
            T("sin(3π/4) = √2/2, and the angle in [−π/2, π/2] with that sine is π/4. The zig-zag graph on the board shows exactly this fold.", "sin(3π/4) = √2/2 والزاوية في [−π/2, π/2] التي لها هذا الجيب هي π/4. والمنحنى المتعرّج على اللوح يبيّن هذا الانطواء تمامًا.", "sin(3π/4) = √2/2 → π/4."),
            F("arcsin(sin(3π/4)) = π/4")]),
        EX("7", "", st("Prove arcsin x + arccos x = π/2 for x in [−1, 1] using derivatives.", "أثبت أن arcsin x + arccos x = π/2 لكل x في [−1, 1] باستعمال المشتقات.", "Prouve arcsin x + arccos x = π/2 par dérivation."), [
            T("Let h(x) = arcsin x + arccos x on (−1, 1). Then h′(x) = 1/√(1 − x²) − 1/√(1 − x²) = 0, so h is constant.", "ليكن h(x) = arcsin x + arccos x على (−1, 1). h′(x) = 1/√(1 − x²) − 1/√(1 − x²) = 0 إذن h ثابتة.", "h′ = 0 : h constante."),
            T("Evaluate at x = 0: h(0) = 0 + π/2 = π/2. By continuity the identity also holds at x = ±1: arcsin 1 + arccos 1 = π/2 + 0.", "نحسب عند x = 0: h(0) = 0 + π/2 = π/2. وبالاستمرار تصح المتطابقة عند x = ±1: arcsin 1 + arccos 1 = π/2 + 0.", "h(0) = π/2, et la continuité donne ±1."),
            F("arcsin x + arccos x = π/2")]),
        EX("8", "", st("Why does arcsin x = 3π/4 have no real solution?", "لماذا ليس للمعادلة arcsin x = 3π/4 حل حقيقي؟", "Pourquoi arcsin x = 3π/4 n'a-t-elle pas de solution ?"), [
            T("The range of arcsin is [−π/2, π/2] ≈ [−1.57, 1.57]. The number 3π/4 ≈ 2.36 is not in that range.", "مدى arcsin هو [−π/2, π/2] ≈ [−1.57, 1.57]. والعدد 3π/4 ≈ 2.36 ليس فيه.", "Image [−π/2 ; π/2], et 3π/4 ≈ 2,36 n'y est pas."),
            T("If we applied sin anyway we would get x = √2/2, but then arcsin x = π/4, not 3π/4: the check fails.", "لو طبقنا sin لحصلنا على x = √2/2 لكن عندها arcsin x = π/4 لا 3π/4 فيفشل التحقق.", "Le test échoue : arcsin(√2/2) = π/4."),
            F("No solution: S = ∅")]),
    ]
