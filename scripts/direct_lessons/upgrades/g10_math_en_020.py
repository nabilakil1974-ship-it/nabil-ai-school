from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import fn_graph, section, add_ex, add_sec


def upgrade(m):
    s = section(m, "Build a graph from values")
    s.append(fn_graph(lambda x: x * x, (-3, 3), (-1, 9), pts={"A": (-2, 4), "B": (-1, 1), "O": (0, 0), "C": (1, 1), "D": (2, 4)}, tag="B1", label="table of values for f(x) = x²"))
    s.append(T("Plot the values from the table: (−2, 4), (−1, 1), (0, 0), (1, 1), (2, 4). Join them with a smooth curve, not with straight segments. The symmetry is visible: the left half mirrors the right half.",
               "نعيّن قيم الجدول: (−2, 4) و(−1, 1) و(0, 0) و(1, 1) و(2, 4). نصلها بمنحنى ناعم لا بقطع مستقيمة. التناظر ظاهر: النصف الأيسر مرآة للنصف الأيمن.",
               "On place (−2 ; 4), (−1 ; 1), (0 ; 0), (1 ; 1), (2 ; 4) et on relie par une courbe lisse. La symétrie apparaît."))
    s = section(m, "Domain habit")
    s.append(fn_graph(lambda x: 1 / x, (-5, 5), (-5, 5), pts={"A": (1, 1), "B": (-1, -1), "C": (2, 0.5)}, vlines=[0], hlines=[0], poles=[0], tag="B2", label="f(x) = 1/x"))
    s.append(T("1/x has two separate branches. The input 0 is forbidden, so the curve never crosses the y-axis, and it never touches the x-axis either. Do not join the two branches across x = 0.",
               "1/x لها فرعان منفصلان. المدخل 0 ممنوع فلا يقطع المنحنى محور التراتيب ولا يلمس محور الفواصل أيضًا. لا نصل الفرعين عبر x = 0.",
               "1/x a deux branches séparées : 0 est interdit. On ne relie pas à travers x = 0."))
    s = section(m, "Absolute value")
    s.append(fn_graph(lambda x: abs(x), (-5, 5), (-1, 6), pts={"O": (0, 0), "A": (-3, 3), "B": (3, 3)}, tag="B3", label="f(x) = |x|"))
    s.append(T("|x| is the distance from x to 0, so it is never negative. The graph is a V with its corner at the origin: for x ≥ 0 it is the line y = x, and for x < 0 it is the line y = −x. Both (−3, 3) and (3, 3) lie on it.",
               "|x| هي المسافة من x إلى 0 فلا تكون سالبة أبدًا. منحناها حرف V زاويته عند المبدأ: من أجل x ≥ 0 هو المستقيم y = x ومن أجل x < 0 هو y = −x. تقع عليه النقطتان (−3, 3) و(3, 3).",
               "|x| est la distance à 0. Pour x ≥ 0 : y = x ; pour x < 0 : y = −x. (−3 ; 3) et (3 ; 3) sont sur la courbe."))
    add_sec(m, ("Square root and shifts", "الجذر التربيعي والانسحاب", "Racine carrée et translations"), [
        T("√x is defined only for x ≥ 0 and starts at the origin. Adding a number outside moves the graph up or down: √x + 2 is √x lifted by 2. Adding inside moves it sideways in the opposite direction: √(x − 3) is √x shifted 3 to the right.",
          "√x معرّفة فقط عند x ≥ 0 وتبدأ من المبدأ. إضافة عدد خارج الجذر تحرّك المنحنى إلى الأعلى أو الأسفل: √x + 2 هي √x مرفوعة 2. وإضافته داخله تحرّكه جانبيًا بعكس الإشارة: √(x − 3) هي √x منزاحة 3 إلى اليمين.",
          "√x : x ≥ 0. √x + 2 est √x montée de 2 ; √(x − 3) est √x décalée de 3 vers la droite."),
        fn_graph(lambda x: x ** 0.5, (0, 12), (0, 6), curves=[lambda x: x ** 0.5 + 2, lambda x: (x - 3) ** 0.5], pts={"A": (0, 0), "B": (3, 0), "C": (0, 2)}, tag="B4", label="√x (red), √x + 2 and √(x − 3) (dashed)"),
        T("Follow the key points: (0, 0) of √x goes to (0, 2) for √x + 2, and to (3, 0) for √(x − 3).", "تابع النقاط المميزة: النقطة (0, 0) في √x تذهب إلى (0, 2) في √x + 2 وإلى (3, 0) في √(x − 3).", "(0 ; 0) → (0 ; 2) et (3 ; 0)."),
    ])
    add_ex(m, [
        EX("", "", st("Complete a table and sketch f(x) = |x| − 2 for x from −4 to 4. Where does it cross the x-axis?", "أكمل جدولًا وارسم f(x) = |x| − 2 من x = −4 إلى 4. أين يقطع محور الفواصل؟", "Table et courbe de f(x) = |x| − 2. Où coupe-t-elle l'axe des abscisses ?"), [
            T("Values: f(−4) = 2, f(−2) = 0, f(0) = −2, f(2) = 0, f(4) = 2.", "القيم: f(−4) = 2 وf(−2) = 0 وf(0) = −2 وf(2) = 0 وf(4) = 2.", "f(−4) = 2, f(−2) = 0, f(0) = −2, f(2) = 0, f(4) = 2."),
            fn_graph(lambda x: abs(x) - 2, (-5, 5), (-3, 4), pts={"A": (-2, 0), "B": (2, 0), "C": (0, -2)}, tag="X3", label="f(x) = |x| − 2"),
            T("The V is the graph of |x| lowered by 2. It crosses the x-axis where |x| = 2, at x = −2 and x = 2.", "شكل V هو منحنى |x| منزلًا 2. يقطع محور الفواصل حيث |x| = 2 أي عند x = −2 وx = 2.", "|x| = 2 : x = ±2."), F("zeros: x = −2 and x = 2")]),
        EX("", "", st("Give the domain of √(x + 4) and of 1/(x + 4), and compare the two graphs' starting behaviour.", "أعطِ مجال √(x + 4) وَ1/(x + 4) وقارن سلوك المنحنيين عند البداية.", "Domaine de √(x + 4) et 1/(x + 4)."), [
            T("√(x + 4): x + 4 ≥ 0, so x ≥ −4. The graph starts at the point (−4, 0).", "√(x + 4): x + 4 ≥ 0 إذن x ≥ −4. يبدأ المنحنى من النقطة (−4, 0).", "x ≥ −4, départ en (−4 ; 0)."), T("1/(x + 4): x ≠ −4. The graph has a break at x = −4, with a vertical line the curve never touches.", "1/(x + 4): x ≠ −4. للمنحنى انقطاع عند x = −4 مع مستقيم شاقولي لا يلمسه.", "x ≠ −4 : coupure en −4."), F("[−4, +∞)      ℝ \\ {−4}")]),
        EX("", "", st("Solve |x − 1| = 3 and sketch y = |x − 1|.", "حلّ |x − 1| = 3 وارسم y = |x − 1|.", "Résous |x − 1| = 3 et trace y = |x − 1|."), [
            T("|x − 1| = 3 means x − 1 = 3 or x − 1 = −3, so x = 4 or x = −2.", "|x − 1| = 3 تعني x − 1 = 3 أو x − 1 = −3 إذن x = 4 أو x = −2.", "x − 1 = ±3 → x = 4 ou x = −2."),
            fn_graph(lambda x: abs(x - 1), (-4, 6), (-1, 6), hlines=[3], pts={"A": (-2, 3), "B": (4, 3), "V": (1, 0)}, tag="X4", label="y = |x − 1| and y = 3"),
            T("The V has its corner at (1, 0): |x| shifted 1 to the right. The line y = 3 meets it at x = −2 and x = 4.", "زاوية V عند (1, 0): هو |x| منزاحًا 1 إلى اليمين. يلتقيه المستقيم y = 3 عند x = −2 وx = 4.", "Sommet (1 ; 0) ; y = 3 coupe en −2 et 4."), F("x = −2 or x = 4")]),
    ])
