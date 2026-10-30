from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import section, add_ex, add_sec
from scripts.direct_lessons.draw import bars


def upgrade(m):
    s = section(m, "Values and frequencies")
    s.append(bars(["Football", "Basketball", "Swimming", "Tennis"], [48, 30, 24, 18], tag="S1", title="Favourite sport, 120 pupils"))
    s.append(T("This bar chart is a picture of a distribution: each bar is the frequency of one value. Football 48, basketball 30, swimming 24, tennis 18. Add the heights: 48 + 30 + 24 + 18 = 120, the whole population. If the total does not match, something is missing.",
               "هذا المخطط بالأعمدة صورة للتوزيع: كل عمود هو تكرار قيمة واحدة. كرة القدم 48 وكرة السلة 30 والسباحة 24 والتنس 18. نجمع الارتفاعات: 48 + 30 + 24 + 18 = 120 أي كل المجتمع. إن لم يطابق المجموع فهناك نقص.",
               "Chaque barre est l'effectif d'une valeur : 48 + 30 + 24 + 18 = 120, la population entière."))
    add_sec(m, ("Relative frequency", "التكرار النسبي", "Fréquence relative"), [
        T("The relative frequency of a value is its frequency divided by the total. Football: 48/120 = 0.40 = 40%. Basketball: 30/120 = 25%. Swimming: 24/120 = 20%. Tennis: 18/120 = 15%. The percentages always add up to 100%: 40 + 25 + 20 + 15 = 100.",
          "التكرار النسبي لقيمة هو تكرارها مقسومًا على المجموع. كرة القدم: 48/120 = 0.40 = 40%. كرة السلة: 30/120 = 25%. السباحة: 24/120 = 20%. التنس: 18/120 = 15%. ومجموع النسب دائمًا 100%: 40 + 25 + 20 + 15 = 100.",
          "Fréquence relative = effectif / total : 40 %, 25 %, 20 %, 15 %, somme 100 %."),
        bars(["Football", "Basketball", "Swimming", "Tennis"], [40, 25, 20, 15], tag="S2", color="#43a047", title="Percentage of pupils (%)"),
        F("relative frequency = frequency / total"),
    ])
    add_ex(m, [
        EX("", "", st("Complete: marks 5, 6, 6, 7, 7, 7, 8, 8, 9, 10. Make the distribution table and the relative frequencies.", "أكمل: العلامات 5, 6, 6, 7, 7, 7, 8, 8, 9, 10. كوّن جدول التوزيع والتكرارات النسبية.", "Notes 5, 6, 6, 7, 7, 7, 8, 8, 9, 10 : tableau et fréquences relatives."), [
            T("Count each mark: 5→1, 6→2, 7→3, 8→2, 9→1, 10→1. Total 10.", "نعدّ كل علامة: 5→1 و6→2 و7→3 و8→2 و9→1 و10→1. المجموع 10.", "5→1 ; 6→2 ; 7→3 ; 8→2 ; 9→1 ; 10→1."),
            bars(["5", "6", "7", "8", "9", "10"], [1, 2, 3, 2, 1, 1], tag="X1", title="Distribution of marks"),
            F("relative frequencies: 10%, 20%, 30%, 20%, 10%, 10%  (sum 100%)")]),
        EX("", "", st("In a survey of 80 people, 32 prefer tea, 28 coffee and the rest juice. How many prefer juice and what percentage?", "في استطلاع لـ 80 شخصًا فضّل 32 الشاي و28 القهوة والباقي العصير. كم يفضل العصير وما نسبتهم؟", "Sur 80 personnes, 32 thé, 28 café, le reste jus : combien et quel pourcentage ?"), [
            T("Juice = 80 − 32 − 28 = 20 people. Percentage = 20/80 = 25%.", "العصير = 80 − 32 − 28 = 20 شخصًا. النسبة = 20/80 = 25%.", "80 − 60 = 20 ; 20/80 = 25 %."), F("20 people, 25%"), F("Check: 40% + 35% + 25% = 100% ✓")]),
        EX("", "", st("What is wrong with the claim: 'Frequencies 12, 15, 9 for a class of 40'?", "ما الخطأ في العبارة: «التكرارات 12 و15 و9 لصف عدد تلاميذه 40»؟", "Que dire de : « effectifs 12, 15, 9 pour une classe de 40 » ?"), [
            T("The frequencies must add up to the class size: 12 + 15 + 9 = 36, not 40. Four pupils are missing from the table.", "يجب أن يساوي مجموع التكرارات عدد تلاميذ الصف: 12 + 15 + 9 = 36 لا 40. هناك أربعة تلاميذ غير ممثّلين.", "12 + 15 + 9 = 36 ≠ 40 : il manque 4 élèves."), F("total check fails: 36 ≠ 40")]),
    ])
