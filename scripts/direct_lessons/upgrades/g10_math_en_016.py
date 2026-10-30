from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import section, add_ex, add_sec, fn_graph


def upgrade(m):
    s = section(m, "Unknown on both sides")
    s.append(fn_graph(lambda x: 4 * (2 * x - 1), (-1, 6), (-8, 28), curves=[lambda x: 3 * x + 11], pts={"P": (3, 20)}, tag="L1", label="4(2x − 1) (red) and 3x + 11 (dashed)"))
    s.append(T("Solving 4(2x − 1) = 3x + 11 means finding where two lines cross. They meet at x = 3, where both equal 20. Algebra: 8x − 4 = 3x + 11, 5x = 15, x = 3. The picture and the algebra agree.",
               "حل 4(2x − 1) = 3x + 11 يعني إيجاد مكان تقاطع مستقيمين. يلتقيان عند x = 3 حيث يساوي كلاهما 20. جبريًا: 8x − 4 = 3x + 11 وَ5x = 15 وx = 3. الرسم والجبر متفقان.",
               "Les droites se coupent en x = 3 (valeur 20). 8x − 4 = 3x + 11 → x = 3."))
    add_ex(m, [
        EX("", "", st("Solve 2(x + 3) = 3x − 1.", "حلّ 2(x + 3) = 3x − 1.", "Résous 2(x + 3) = 3x − 1."), [
            T("Expand: 2x + 6 = 3x − 1. Collect x on one side: 6 + 1 = 3x − 2x, so x = 7.", "ننشر: 2x + 6 = 3x − 1. نجمع x في طرف: 6 + 1 = 3x − 2x إذن x = 7.", "2x + 6 = 3x − 1 → x = 7."), F("x = 7"), F("Check: 2 × 10 = 20 and 3 × 7 − 1 = 20 ✓")]),
        EX("", "", st("Solve (x + 1)/2 = (x − 1)/3 + 1.", "حلّ (x + 1)/2 = (x − 1)/3 + 1.", "Résous (x + 1)/2 = (x − 1)/3 + 1."), [
            T("Multiply everything by 6 to clear fractions: 3(x + 1) = 2(x − 1) + 6.", "نضرب كل شيء في 6 لإزالة الكسور: 3(x + 1) = 2(x − 1) + 6.", "×6 : 3(x + 1) = 2(x − 1) + 6."), T("3x + 3 = 2x − 2 + 6 = 2x + 4, so x = 1.", "3x + 3 = 2x − 2 + 6 = 2x + 4 إذن x = 1.", "x = 1."), F("x = 1"), F("Check: 2/2 = 1 and 0/3 + 1 = 1 ✓")]),
        EX("", "", st("Solve 5x − 2 = 5x + 3 and 3x + 6 = 3(x + 2). What happens?", "حلّ 5x − 2 = 5x + 3 وَ3x + 6 = 3(x + 2). ماذا يحدث؟", "Résous 5x − 2 = 5x + 3 et 3x + 6 = 3(x + 2)."), [
            T("First: subtract 5x from both sides: −2 = 3, which is false. No solution: the lines are parallel.", "الأولى: نطرح 5x من الطرفين: −2 = 3 وهذا خطأ. لا حل: المستقيمان متوازيان.", "−2 = 3 : aucune solution."), T("Second: 3x + 6 = 3x + 6 is always true. Every real number is a solution: the two lines are the same.", "الثانية: 3x + 6 = 3x + 6 صحيحة دائمًا. كل عدد حقيقي حل: المستقيمان منطبقان.", "Toujours vrai : tout réel."), F("S = ∅      S = ℝ")]),
        EX("", "", st("A rectangle's length is 4 more than its width and its perimeter is 40. Find its sides.", "طول مستطيل يزيد 4 على عرضه ومحيطه 40. جد ضلعيه.", "Longueur = largeur + 4, périmètre 40 : dimensions."), [
            T("Let the width be w. Length w + 4. Perimeter 2(w + w + 4) = 40, so 4w + 8 = 40 and w = 8.", "ليكن العرض w. الطول w + 4. المحيط 2(w + w + 4) = 40 إذن 4w + 8 = 40 وw = 8.", "4w + 8 = 40 → w = 8."), F("width 8, length 12"), F("Check: 2(8 + 12) = 40 ✓")]),
    ])
