from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import fn_graph, section, add_ex, add_sec


def upgrade(m):
    s = section(m, "Point-on-line test")
    s.append(fn_graph(lambda x: 2 * x + 1, (-3, 5), (-4, 9), pts={"A": (3, 7), "B": (3, 6), "C": (0, 1)}, tag="L1", label="y = 2x + 1"))
    s.append(T("Look at the board. A(3, 7) sits exactly on the line: 2 × 3 + 1 = 7. B(3, 6) has the same x but is one unit below the line, because the line gives 7 there, not 6. Point C(0, 1) is where the line crosses the y-axis.",
               "انظر إلى اللوح. النقطة A(3, 7) تقع تمامًا على المستقيم: 2 × 3 + 1 = 7. أما B(3, 6) فلها الفاصلة نفسها لكنها أسفل المستقيم بوحدة واحدة لأن المستقيم يعطي 7 هناك لا 6. والنقطة C(0, 1) هي حيث يقطع المستقيم محور التراتيب.",
               "A(3 ; 7) est sur la droite : 2 × 3 + 1 = 7. B(3 ; 6) est une unité en dessous. C(0 ; 1) est l'ordonnée à l'origine."))
    add_sec(m, ("Slope and intercept", "الميل والمقطع", "Pente et ordonnée à l'origine"), [
        T("In y = mx + p, m is the slope and p is the y-intercept. For y = 2x + 1: every step of 1 to the right lifts the line by 2, and the line meets the y-axis at 1. A bigger |m| means a steeper line; a negative m means the line goes down to the right.",
          "في y = mx + p العدد m هو الميل وp هو المقطع على محور التراتيب. في y = 2x + 1: كل خطوة بمقدار 1 نحو اليمين ترفع المستقيم 2 ويقطع المحور عند 1. كلما كبر |m| صار المستقيم أشد انحدارًا، وm سالب يعني أن المستقيم ينزل نحو اليمين.",
          "y = mx + p : m pente, p ordonnée à l'origine. Ici, +1 en x donne +2 en y."),
        fn_graph(lambda x: 2 * x + 1, (-3, 4), (-6, 8), curves=[lambda x: -x + 3, lambda x: 0.5 * x - 1], pts={"P": (0, 1)}, tag="L2", label="m = 2 (red), m = −1 and m = ½ (dashed)"),
        F("slope m = (y₂ − y₁)/(x₂ − x₁)"),
        T("To find the slope from two points, A(0, 1) and B(3, 7): m = (7 − 1)/(3 − 0) = 2. Then the line is y = 2x + 1.", "لإيجاد الميل من نقطتين A(0, 1) وB(3, 7): m = (7 − 1)/(3 − 0) = 2. فالمستقيم y = 2x + 1.", "A(0 ; 1), B(3 ; 7) : m = 6/3 = 2."),
    ])
    add_ex(m, [
        EX("", "", st("Find the slope of the line through A(1, 2) and B(5, 10), then its equation.", "جد ميل المستقيم المار بالنقطتين A(1, 2) وB(5, 10) ثم معادلته.", "Pente de la droite (AB) avec A(1 ; 2), B(5 ; 10), puis équation."), [
            T("m = (10 − 2)/(5 − 1) = 8/4 = 2.", "m = (10 − 2)/(5 − 1) = 8/4 = 2.", "m = 8/4 = 2."),
            T("Use A: y − 2 = 2(x − 1), so y = 2x. Check B: 2 × 5 = 10 ✓.", "نستعمل A: y − 2 = 2(x − 1) إذن y = 2x. تحقق من B: 2 × 5 = 10 ✓.", "y = 2x ; B : 10 ✓."), F("m = 2      y = 2x")]),
        EX("", "", st("Where does y = −3x + 2 cross the two axes?", "أين يقطع المستقيم y = −3x + 2 المحورين؟", "Où y = −3x + 2 coupe-t-elle les axes ?"), [
            T("y-axis: x = 0 gives y = 2, so the point (0, 2).", "محور التراتيب: x = 0 يعطي y = 2 فالنقطة (0, 2).", "x = 0 → (0 ; 2)."),
            T("x-axis: y = 0 gives −3x + 2 = 0, so x = 2/3, the point (2/3, 0).", "محور الفواصل: y = 0 يعطي −3x + 2 = 0 إذن x = 2/3 والنقطة (2/3, 0).", "y = 0 → x = 2/3."), F("(0, 2)      (2/3, 0)")]),
        EX("", "", st("Are the lines y = 2x + 1 and y = 2x − 5 parallel? Do they ever meet?", "هل المستقيمان y = 2x + 1 وy = 2x − 5 متوازيان؟ وهل يلتقيان؟", "Les droites y = 2x + 1 et y = 2x − 5 sont-elles parallèles ?"), [
            T("Both have slope 2, so they are parallel. If they met, 2x + 1 = 2x − 5 would give 1 = −5, which is false. They never meet.", "ميلاهما 2 فهما متوازيان. لو التقيا لأعطت 2x + 1 = 2x − 5 النتيجة 1 = −5 وهذا خطأ. لا يلتقيان أبدًا.", "Même pente 2 : parallèles, 1 = −5 impossible."), F("parallel, no intersection")]),
        EX("", "", st("Find the intersection of y = 2x + 1 and y = −x + 7.", "جد نقطة تقاطع y = 2x + 1 وy = −x + 7.", "Intersection de y = 2x + 1 et y = −x + 7."), [
            T("Equal outputs: 2x + 1 = −x + 7, so 3x = 6 and x = 2. Then y = 2 × 2 + 1 = 5.", "نساوي الناتجين: 2x + 1 = −x + 7 إذن 3x = 6 وx = 2. ثم y = 2 × 2 + 1 = 5.", "3x = 6 → x = 2, y = 5."), F("(2, 5)"), F("Check: −2 + 7 = 5 ✓")]),
    ])
