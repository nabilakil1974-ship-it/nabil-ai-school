from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import section, add_ex, add_sec
from scripts.direct_lessons.draw import vectors

R, B, G = "#e53935", "#1e88e5", "#2e7d32"


def upgrade(m):
    s = section(m, "A vector is a displacement")
    s.append(vectors([("u = AB", (1, 1), (4, 3), R)], tag="V1"))
    s.append(T("A vector has a direction, a sense and a length. Here u goes from A(1, 1) to B(4, 3): 3 units right and 2 units up, so u = (3, 2). Its length is √(3² + 2²) = √13 ≈ 3.61. The arrow head shows the sense.",
               "للمتجه اتجاه ومنحى وطول. هنا u يذهب من A(1, 1) إلى B(4, 3): 3 وحدات يمينًا ووحدتان للأعلى إذن u = (3, 2). طوله √(3² + 2²) = √13 ≈ 3.61. رأس السهم يبيّن المنحى.",
               "u va de A(1 ; 1) à B(4 ; 3) : 3 à droite, 2 en haut, u = (3 ; 2), longueur √13 ≈ 3,61."))
    s = section(m, "AB and BA")
    s.append(vectors([("AB", (1, 1), (4, 3), R), ("BA", (4, 3), (1, 1), B)], tag="V2"))
    s.append(T("AB and BA lie on the same line and have the same length, but opposite senses: BA = −AB. If AB = (3, 2) then BA = (−3, −2). Same length, different vectors.",
               "AB وBA على المستقيم نفسه وبالطول نفسه لكن بمنحيين متعاكسين: BA = −AB. إذا كان AB = (3, 2) فإن BA = (−3, −2). الطول نفسه لكن المتجهان مختلفان.",
               "BA = −AB : même longueur, sens opposé. AB = (3 ; 2) → BA = (−3 ; −2)."))
    s = section(m, "Addition: successive displacements")
    s.append(vectors([("AB", (0, 0), (3, 2), R), ("BC", (3, 2), (5, 1), B), ("AC", (0, 0), (5, 1), G)], tag="V3"))
    s.append(T("Chasles relation: walk A to B, then B to C. The shortcut A to C is the sum: AB + BC = AC. In numbers: (3, 2) + (2, −1) = (5, 1). Add the x-coordinates together and the y-coordinates together.",
               "علاقة شال: نمشي من A إلى B ثم من B إلى C. الطريق المختصر من A إلى C هو المجموع: AB + BC = AC. بالأعداد: (3, 2) + (2, −1) = (5, 1). نجمع الإحداثيات السينية معًا والصادية معًا.",
               "Chasles : AB + BC = AC. (3 ; 2) + (2 ; −1) = (5 ; 1)."))
    add_ex(m, [
        EX("", "", st("A(1, 2), B(5, 5), C(7, 1). Find the coordinates of AB, BC and AC and check AB + BC = AC.", "A(1, 2) وB(5, 5) وC(7, 1). جد إحداثيات AB وBC وAC وتحقق أن AB + BC = AC.", "A(1 ; 2), B(5 ; 5), C(7 ; 1) : AB, BC, AC et vérifie Chasles."), [
            T("AB = (5 − 1, 5 − 2) = (4, 3). BC = (7 − 5, 1 − 5) = (2, −4). AC = (7 − 1, 1 − 2) = (6, −1).", "AB = (5 − 1, 5 − 2) = (4, 3). BC = (7 − 5, 1 − 5) = (2, −4). AC = (7 − 1, 1 − 2) = (6, −1).", "AB = (4 ; 3) ; BC = (2 ; −4) ; AC = (6 ; −1)."),
            vectors([("AB", (1, 2), (5, 5), R), ("BC", (5, 5), (7, 1), B), ("AC", (1, 2), (7, 1), G)], tag="X1", lo=(-1, -1), hi=(8, 6)),
            F("(4, 3) + (2, −4) = (6, −1) = AC ✓")]),
        EX("", "", st("Find the length of the vector (5, 12) and of (−6, 8).", "جد طول المتجه (5, 12) وطول (−6, 8).", "Longueur de (5 ; 12) et de (−6 ; 8)."), [
            T("|(5, 12)| = √(25 + 144) = √169 = 13. |(−6, 8)| = √(36 + 64) = √100 = 10.", "|(5, 12)| = √(25 + 144) = √169 = 13. |(−6, 8)| = √(36 + 64) = √100 = 10.", "13 et 10."), F("13      10")]),
        EX("", "", st("If u = (2, −3) and v = (−1, 4), find u + v, u − v and 2u.", "إذا كان u = (2, −3) وv = (−1, 4) فجد u + v وu − v وَ2u.", "u = (2 ; −3), v = (−1 ; 4) : u + v, u − v, 2u."), [
            T("u + v = (2 − 1, −3 + 4) = (1, 1). u − v = (2 + 1, −3 − 4) = (3, −7). 2u = (4, −6).", "u + v = (2 − 1, −3 + 4) = (1, 1). u − v = (2 + 1, −3 − 4) = (3, −7). 2u = (4, −6).", "(1 ; 1), (3 ; −7), (4 ; −6)."), F("(1, 1)      (3, −7)      (4, −6)")]),
        EX("", "", st("A boat sails 6 km east then 8 km north. What is its displacement from the start, and how far is it in a straight line?", "تبحر سفينة 6 كم شرقًا ثم 8 كم شمالًا. ما إزاحتها عن نقطة البدء وكم تبعد بخط مستقيم؟", "Un bateau fait 6 km à l'est puis 8 km au nord : déplacement et distance directe ?"), [
            T("Displacement = (6, 0) + (0, 8) = (6, 8). Straight-line distance = √(36 + 64) = 10 km.", "الإزاحة = (6, 0) + (0, 8) = (6, 8). المسافة بخط مستقيم = √(36 + 64) = 10 كم.", "(6 ; 8) ; distance 10 km."), F("(6, 8)      10 km")]),
    ])
