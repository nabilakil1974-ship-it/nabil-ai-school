from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import section, add_ex, add_sec
from scripts.direct_lessons.draw import numberline, bars


def upgrade(m):
    s = section(m, "The mean")
    s.append(numberline(0, 10, marks={"2": 2, "4": 4, "6": 6, "8": 8, "mean 5": 5}, tag="M1"))
    s.append(T("The data 2, 4, 6, 8 are the four dots. The mean is (2 + 4 + 6 + 8)/4 = 20/4 = 5, the balance point of the line: the distances to the left (3 + 1) equal the distances to the right (1 + 3).",
               "المعطيات 2 و4 و6 و8 هي النقاط الأربع. المتوسط (2 + 4 + 6 + 8)/4 = 20/4 = 5 وهو نقطة توازن الخط: مسافات اليسار (3 + 1) تساوي مسافات اليمين (1 + 3).",
               "Moyenne = 20/4 = 5 : point d'équilibre ; distances à gauche (3 + 1) = à droite (1 + 3)."))
    s = section(m, "Mode and median")
    s.append(bars(["3", "5", "7", "9", "12"], [1, 3, 2, 1, 1], tag="M2", color="#fb8c00", title="Frequency of each value"))
    s.append(T("The tallest bar is the mode: the value 5 appears most often (3 times). The median is the middle value after sorting. With 8 values 3, 5, 5, 5, 7, 7, 9, 12, the middle lies between the 4th and 5th: (5 + 7)/2 = 6.",
               "أطول عمود هو المنوال: القيمة 5 تظهر أكثر من غيرها (3 مرات). والوسيط هو القيمة الوسطى بعد الترتيب. مع 8 قيم 3, 5, 5, 5, 7, 7, 9, 12 يقع الوسط بين الرابعة والخامسة: (5 + 7)/2 = 6.",
               "Mode = 5 (3 fois). Médiane : entre la 4e et la 5e valeur : (5 + 7)/2 = 6."))
    add_ex(m, [
        EX("", "", st("Find the mean, median, mode and range of 3, 5, 5, 6, 9, 12.", "جد المتوسط والوسيط والمنوال والمدى لـ 3, 5, 5, 6, 9, 12.", "Moyenne, médiane, mode, étendue de 3, 5, 5, 6, 9, 12."), [
            T("Mean = (3 + 5 + 5 + 6 + 9 + 12)/6 = 40/6 ≈ 6.67.", "المتوسط = (3 + 5 + 5 + 6 + 9 + 12)/6 = 40/6 ≈ 6.67.", "40/6 ≈ 6,67."), T("Median: the data are sorted; the middle lies between 5 and 6, so (5 + 6)/2 = 5.5. Mode = 5. Range = 12 − 3 = 9.", "الوسيط: المعطيات مرتبة والوسط بين 5 و6 إذن (5 + 6)/2 = 5.5. المنوال 5. المدى = 12 − 3 = 9.", "Médiane 5,5 ; mode 5 ; étendue 9."), F("mean ≈ 6.67   median 5.5   mode 5   range 9")]),
        EX("", "", st("Frequency table: value 1 (2 times), 2 (5 times), 3 (3 times). Find the mean.", "جدول تكرارات: القيمة 1 (مرتان) و2 (5 مرات) و3 (3 مرات). جد المتوسط.", "Valeur 1 (2 fois), 2 (5 fois), 3 (3 fois) : moyenne."), [
            T("Weighted sum: 1×2 + 2×5 + 3×3 = 2 + 10 + 9 = 21. Total frequency = 2 + 5 + 3 = 10.", "المجموع المرجّح: 1×2 + 2×5 + 3×3 = 2 + 10 + 9 = 21. مجموع التكرارات = 2 + 5 + 3 = 10.", "1×2 + 2×5 + 3×3 = 21 ; total 10."), F("mean = 21/10 = 2.1")]),
        EX("", "", st("Five pupils have a mean mark of 12. A sixth pupil scores 18. What is the new mean?", "لخمسة تلاميذ متوسط علامات 12. حصل سادس على 18. ما المتوسط الجديد؟", "Cinq élèves ont une moyenne de 12. Un sixième a 18 : nouvelle moyenne ?"), [
            T("The old total is 5 × 12 = 60. The new total is 60 + 18 = 78 for 6 pupils.", "المجموع القديم 5 × 12 = 60. والجديد 60 + 18 = 78 لستة تلاميذ.", "Total 60 + 18 = 78."), F("new mean = 78/6 = 13")]),
        EX("", "", st("Why can the median be a better 'typical value' than the mean for 2, 3, 3, 4, 50?", "لماذا قد يكون الوسيط قيمة «نموذجية» أفضل من المتوسط لـ 2, 3, 3, 4, 50؟", "Pourquoi la médiane représente-t-elle mieux 2, 3, 3, 4, 50 ?"), [
            T("The mean is (2 + 3 + 3 + 4 + 50)/5 = 12.4, pulled up by the one extreme value 50. The median is 3, much closer to most of the data.", "المتوسط (2 + 3 + 3 + 4 + 50)/5 = 12.4 وقد شدّته القيمة الشاذة 50 إلى الأعلى. والوسيط 3 وهو أقرب بكثير إلى معظم المعطيات.", "Moyenne 12,4 tirée par 50 ; médiane 3."), F("median = 3, mean = 12.4")]),
    ])
