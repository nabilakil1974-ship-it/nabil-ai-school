from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import fn_graph, section


def theory_extras(m, sec_geo, sec_outcomes, sec_word):
    s = section(m, sec_outcomes)
    s.append(fn_graph(lambda x: 5 - x, (-1, 6), (-1, 6), curves=[lambda x: x - 1], pts={"P": (3, 2)}, tag="Y1", label="x + y = 5 (red) and x − y = 1 (dashed)"))
    s.append(T("Case 1, a single solution: two lines cross at exactly one point P(3, 2). Reading the picture: x = 3 and y = 2 satisfy both equations at once. In three variables the same case is three planes meeting at one point.",
               "الحالة 1، حل وحيد: مستقيمان يتقاطعان في نقطة واحدة P(3, 2). قراءة الصورة: x = 3 وy = 2 يحققان المعادلتين معًا. وفي ثلاثة مجاهيل تكون الحالة نفسها ثلاثة مستويات تلتقي في نقطة واحدة.",
               "Cas 1 : une seule solution, droites sécantes en P(3 ; 2). En 3 variables : trois plans qui se coupent en un point."))
    s.append(fn_graph(lambda x: 5 - x, (-1, 6), (-1, 7), curves=[lambda x: 7 - x], tag="Y2", label="x + y = 5 and x + y = 7: parallel"))
    s.append(T("Case 2, no solution: the lines are parallel and never meet. Algebra shows the same thing as a contradiction: subtracting the equations gives 0 = 2. Parallel lines mean an impossible system.",
               "الحالة 2، لا حل: المستقيمان متوازيان ولا يلتقيان أبدًا. والجبر يظهر الشيء نفسه كتناقض: طرح المعادلتين يعطي 0 = 2. المستقيمان المتوازيان يعنيان جملة مستحيلة.",
               "Cas 2 : aucune solution, droites parallèles. L'algèbre donne 0 = 2."))
    s.append(fn_graph(lambda x: 5 - x, (-1, 6), (-1, 7), curves=[lambda x: 5 - x], pts={"A": (1, 4), "B": (2, 3), "C": (4, 1)}, tag="Y3", label="x + y = 5 and 2x + 2y = 10: the same line"))
    s.append(T("Case 3, infinitely many solutions: the second equation is just twice the first, so both are the same line. Every point of it is a solution, for example (1, 4), (2, 3), (4, 1). We describe them with a parameter: x = t, y = 5 − t.",
               "الحالة 3، حلول لا نهائية: المعادلة الثانية ضعف الأولى فهما المستقيم نفسه. كل نقطة منه حل مثل (1, 4) و(2, 3) و(4, 1). نصفها بوسيط: x = t وy = 5 − t.",
               "Cas 3 : une infinité de solutions, même droite. Paramétrage : x = t, y = 5 − t."))

    s = section(m, sec_word)
    s.append(fn_graph(lambda x: 10 - x, (0, 12), (0, 12), curves=[lambda x: (28 - 2 * x) / 4], pts={"P": (6, 4)}, tag="Y4", label="Chickens and rabbits: x + y = 10, 2x + 4y = 28"))
    s.append(T("A farm has 10 animals with 28 legs in total. The two lines cross at P(6, 4): 6 chickens and 4 rabbits. Check: 6 + 4 = 10 and 2·6 + 4·4 = 12 + 16 = 28.",
               "في مزرعة 10 حيوانات ومجموع أرجلها 28. يتقاطع المستقيمان في P(6, 4): 6 دجاجات و4 أرانب. تحقق: 6 + 4 = 10 و2·6 + 4·4 = 12 + 16 = 28.",
               "10 animaux et 28 pattes : P(6 ; 4), soit 6 poules et 4 lapins. 6 + 4 = 10 ; 12 + 16 = 28."))


def exercises():
    return [
        EX("1", "", st("Solve x + y + z = 6, 2x − y + z = 3, 3x + y − z = 2.", "حلّ x + y + z = 6 وَ2x − y + z = 3 وَ3x + y − z = 2.", "Résous x + y + z = 6, 2x − y + z = 3, 3x + y − z = 2."), [
            T("Add equations 1 and 3 to remove z: 4x + 2y = 8, so 2x + y = 4. Subtract equation 2 from equation 1: −x + 2y = 3.", "نجمع المعادلتين 1 و3 لحذف z: 4x + 2y = 8 إذن 2x + y = 4. ونطرح المعادلة 2 من 1: −x + 2y = 3.", "Éliminer z : 2x + y = 4 et −x + 2y = 3."),
            T("From 2x + y = 4 take y = 4 − 2x. Substitute: −x + 8 − 4x = 3, so −5x = −5 and x = 1. Then y = 2 and z = 6 − 1 − 2 = 3.", "من 2x + y = 4 نأخذ y = 4 − 2x. نعوّض: −x + 8 − 4x = 3 إذن −5x = −5 وx = 1. ثم y = 2 وz = 6 − 1 − 2 = 3.", "x = 1, y = 2, z = 3."),
            F("(x, y, z) = (1, 2, 3)"), F("Check: 1+2+3 = 6 ✓   2−2+3 = 3 ✓   3+2−3 = 2 ✓")]),
        EX("2", "", st("A reduction ends with 0 = 9. Classify the system and explain geometrically.", "تنتهي عملية اختزال إلى 0 = 9. صنّف الجملة وفسّر هندسيًا.", "Une réduction donne 0 = 9 : classe et explique."), [
            T("0 = 9 is false for every x, y, z, so no triple satisfies all the equations: the system is impossible (no solution).", "0 = 9 خاطئة مهما كانت x وy وz إذن لا ثلاثية تحقق كل المعادلات: الجملة مستحيلة (لا حل).", "Système impossible."),
            T("Geometrically, the planes have no common point, like the two parallel lines on the board: they never meet.", "هندسيًا لا توجد نقطة مشتركة بين المستويات، مثل المستقيمين المتوازيين على اللوح: لا يلتقيان أبدًا.", "Aucun point commun."),
            F("S = ∅")]),
        EX("3", "", st("x + y + z = 4, y + z = 2, 2y + 2z = 4: write the family of solutions.", "x + y + z = 4 وy + z = 2 و2y + 2z = 4: اكتب عائلة الحلول.", "x + y + z = 4, y + z = 2, 2y + 2z = 4 : famille de solutions."), [
            T("The third equation is twice the second, so it adds nothing. Two independent equations remain for three unknowns: one free parameter.", "المعادلة الثالثة ضعف الثانية فلا تضيف شيئًا. تبقى معادلتان مستقلتان لثلاثة مجاهيل: وسيط حر واحد.", "Deux équations indépendantes, un paramètre."),
            T("From y + z = 2 and x + y + z = 4 we get x = 2. Let z = t, then y = 2 − t.", "من y + z = 2 وx + y + z = 4 نجد x = 2. ليكن z = t فيكون y = 2 − t.", "x = 2, z = t, y = 2 − t."),
            F("(x, y, z) = (2, 2 − t, t), t ∈ ℝ"), T("Example t = 0: (2, 2, 0). Check: 2+2+0 = 4 ✓, 2+0 = 2 ✓.", "مثال t = 0: (2, 2, 0). تحقق: 2+2+0 = 4 ✓ وَ2+0 = 2 ✓.", "t = 0 : (2 ; 2 ; 0) ✓.")]),
        EX("4", "", st("Solve x + y + z = 6, 2x + 3y + z = 11, x + 2y + 3z = 14.", "حلّ x + y + z = 6 وَ2x + 3y + z = 11 وَx + 2y + 3z = 14.", "Résous x + y + z = 6, 2x + 3y + z = 11, x + 2y + 3z = 14."), [
            T("Subtract eq. 1 from eq. 2: x + 2y = 5. Subtract eq. 1 from eq. 3: y + 2z = 8.", "نطرح المعادلة 1 من 2: x + 2y = 5. ونطرح 1 من 3: y + 2z = 8.", "x + 2y = 5 et y + 2z = 8."),
            T("From x + 2y = 5: x = 5 − 2y. From y + 2z = 8: z = (8 − y)/2. Put into eq. 1: 5 − 2y + y + (8 − y)/2 = 6; multiply by 2: 10 − 4y + 2y + 8 − y = 12, so 18 − 3y = 12, y = 2.", "من x + 2y = 5: x = 5 − 2y. ومن y + 2z = 8: z = (8 − y)/2. نعوّض في المعادلة 1: 5 − 2y + y + (8 − y)/2 = 6؛ نضرب في 2: 10 − 4y + 2y + 8 − y = 12 أي 18 − 3y = 12 وy = 2.", "y = 2."),
            T("Then x = 5 − 4 = 1 and z = (8 − 2)/2 = 3.", "إذن x = 5 − 4 = 1 وz = (8 − 2)/2 = 3.", "x = 1, z = 3."),
            F("(1, 2, 3)"), F("Check: 1+2+3 = 6 ✓   2+6+3 = 11 ✓   1+4+9 = 14 ✓")]),
        EX("5", "", st("Why must we check the answer in the ORIGINAL system?", "لماذا يجب التحقق من الجواب في الجملة الأصلية؟", "Pourquoi vérifier dans le système ORIGINAL ?"), [
            T("A copying or arithmetic slip during elimination can still give numbers that fit the later, simplified equations. Only the original equations are the real problem.", "قد يحدث خطأ نسخ أو حساب أثناء الحذف فنحصل على أعداد تناسب المعادلات المبسّطة اللاحقة فقط. المعادلات الأصلية وحدها هي المسألة الحقيقية.", "Une erreur de calcul peut rester invisible dans les équations simplifiées."),
            T("Example: if we had wrongly found y = 3 above, the check 2 − 3 + 3 = 2 ≠ 3 in the original equation 2 would expose it immediately.", "مثال: لو وجدنا خطأً y = 3 في التمرين 1 لكشف التحقق 2 − 3 + 3 = 2 ≠ 3 في المعادلة الأصلية 2 الخطأ فورًا.", "Un test dans l'équation d'origine révèle l'erreur."),
            F("Always substitute into every original equation")]),
        EX("6", "", st("Word problem: 10 animals, 28 legs (chickens 2 legs, rabbits 4 legs). How many of each?", "مسألة: 10 حيوانات و28 رجلًا (للدجاجة رجلان وللأرنب 4). كم من كل نوع؟", "10 animaux, 28 pattes : combien de chaque ?"), [
            T("Let x = chickens and y = rabbits. Equations: x + y = 10 and 2x + 4y = 28.", "ليكن x عدد الدجاجات وy عدد الأرانب. المعادلتان: x + y = 10 وَ2x + 4y = 28.", "x + y = 10 ; 2x + 4y = 28."),
            T("Multiply the first by 2: 2x + 2y = 20. Subtract from the second: 2y = 8, so y = 4 and x = 6.", "نضرب الأولى في 2: 2x + 2y = 20. نطرحها من الثانية: 2y = 8 إذن y = 4 وx = 6.", "2y = 8 → y = 4, x = 6."),
            F("6 chickens and 4 rabbits"), F("Check: 6 + 4 = 10 ✓   12 + 16 = 28 ✓")]),
        EX("7", "", st("Solve 2x + 3y = 12 and x − y = 1, and describe the picture.", "حلّ 2x + 3y = 12 وَx − y = 1 وصف الصورة.", "Résous 2x + 3y = 12 et x − y = 1 et décris le graphique."), [
            T("From x − y = 1, x = y + 1. Substitute: 2(y + 1) + 3y = 12, so 5y + 2 = 12 and y = 2, x = 3.", "من x − y = 1 نأخذ x = y + 1. نعوّض: 2(y + 1) + 3y = 12 إذن 5y + 2 = 12 وy = 2 وx = 3.", "y = 2, x = 3."),
            T("Two lines with different slopes (−2/3 and 1) cross at one point (3, 2): a single solution.", "مستقيمان مختلفا الميل (−2/3 و1) يتقاطعان في نقطة واحدة (3, 2): حل وحيد.", "Pentes différentes : un seul point (3 ; 2)."),
            F("(3, 2)")]),
        EX("8", "", st("For which value of k does x + y = 5, 2x + 2y = k have infinitely many solutions? None?", "من أجل أي قيمة لـ k تكون للجملة x + y = 5 وَ2x + 2y = k حلول لا نهائية؟ ومتى لا حل؟", "Pour quel k : une infinité de solutions ? aucune ?"), [
            T("Doubling the first equation gives 2x + 2y = 10. If k = 10 the second equation is the same line: infinitely many solutions.", "ضعف المعادلة الأولى يعطي 2x + 2y = 10. إذا كان k = 10 فالمعادلة الثانية هي المستقيم نفسه: حلول لا نهائية.", "k = 10 : même droite."),
            T("If k ≠ 10 the lines are parallel and distinct (0 = k − 10 ≠ 0): no solution. There is never exactly one solution here, because the slopes are equal.", "إذا كان k ≠ 10 فالمستقيمان متوازيان ومختلفان (0 = k − 10 ≠ 0): لا حل. ولا يوجد حل وحيد هنا لأن الميلين متساويان.", "k ≠ 10 : parallèles, aucune solution."),
            F("k = 10: infinitely many      k ≠ 10: none")]),
    ]
