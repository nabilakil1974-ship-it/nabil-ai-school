from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import section, add_ex, add_sec
from scripts.direct_lessons.draw import vectors

R, B, G = "#e53935", "#1e88e5", "#2e7d32"


def upgrade(m):
    s = section(m, "The sign carries meaning")
    s.append(vectors([("u", (0, 0), (4, 0), R), ("acute", (0, 0), (3, 3), B), ("right", (0, 0), (0, 4), G), ("obtuse", (0, 0), (-3, 3), "#8e24aa")], lo=(-4, -1), hi=(6, 5), tag="D1"))
    s.append(T("Fix u along the x-axis. A vector at an acute angle (blue) makes u·v positive. At exactly 90° (green) the product is 0. At an obtuse angle (purple) the product is negative. The sign tells you which side of the right angle you are on.",
               "نثبّت u على محور الفواصل. متجه بزاوية حادة (الأزرق) يجعل u·v موجبًا. وعند 90° تمامًا (الأخضر) يكون الجداء 0. وبزاوية منفرجة (البنفسجي) يكون الجداء سالبًا. الإشارة تخبرك في أي جانب من الزاوية القائمة أنت.",
               "u fixe sur l'axe : angle aigu → u·v > 0 ; droit → 0 ; obtus → < 0."))
    add_ex(m, [
        EX("", "", st("|u| = 4, |v| = 6, θ = 120°. Find u·v.", "|u| = 4 وَ|v| = 6 وθ = 120°. جد u·v.", "|u| = 4, |v| = 6, θ = 120° : u·v."), [
            T("cos 120° = −1/2. So u·v = 4 × 6 × (−1/2) = −12. Negative, as expected for an obtuse angle.", "cos 120° = −1/2 إذن u·v = 4 × 6 × (−1/2) = −12. سالب كما نتوقع لزاوية منفرجة.", "cos 120° = −1/2 → −12."), F("u·v = −12")]),
        EX("", "", st("|u| = 2, |v| = 5, u·v = 5. Find the angle between u and v.", "|u| = 2 وَ|v| = 5 وَu·v = 5. جد الزاوية بين u وv.", "|u| = 2, |v| = 5, u·v = 5 : angle."), [
            T("cos θ = 5/(2 × 5) = 1/2, so θ = 60°.", "cos θ = 5/(2 × 5) = 1/2 إذن θ = 60°.", "cos θ = 1/2 → 60°."), F("θ = 60°")]),
        EX("", "", st("Find u·u for a vector of length 7. What does it equal in general?", "جد u·u لمتجه طوله 7. وماذا يساوي عمومًا؟", "u·u pour |u| = 7 ?"), [
            T("The angle between u and itself is 0°, so u·u = |u||u|cos 0° = 7 × 7 × 1 = 49.", "الزاوية بين u ونفسه 0° إذن u·u = |u||u|cos 0° = 7 × 7 × 1 = 49.", "θ = 0° : 49."), F("u·u = |u|²")]),
        EX("", "", st("A force of 10 N pulls a trolley 3 m at 60° to the motion. Find the work W = F·d.", "قوة 10 نيوتن تسحب عربة 3 م بزاوية 60° مع الحركة. جد الشغل W = F·d.", "Force 10 N, déplacement 3 m, 60° : travail."), [
            T("W = 10 × 3 × cos 60° = 30 × 1/2 = 15 joules. Only the part of the force along the motion does work.", "W = 10 × 3 × cos 60° = 30 × 1/2 = 15 جول. الجزء من القوة الموازي للحركة هو وحده الذي يبذل شغلًا.", "W = 15 J."), F("W = 15 J")]),
    ])
