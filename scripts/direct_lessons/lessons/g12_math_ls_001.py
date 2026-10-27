"""Grade 12 (LS) Mathematics — Systems of linear equations."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G12-MATH-LS-001"
GRADE = 12
SUBJECT = "math"
TITLES = {"en": "Systems of linear equations", "ar": "جمل المعادلات الخطية", "fr": "Systèmes d'équations linéaires"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "x + y = 5 and x − y = 1. Adding them gives …", "opts": ["2x = 6", "2y = 4", "x = 6", "0 = 6"], "a": 0,
     "why": {"2y = 4": _w("Adding removes y, not x.", "الجمع يحذف y لا x.", "Élimine y."),
             "x = 6": _w("(x + y) + (x − y) = 2x.", "الجمع يعطي 2x.", "2x."),
             "0 = 6": _w("No contradiction here.", "لا تناقض هنا.", "Non.")}, "ok": "2x = 6"},
    {"q": "Which operation is NOT allowed?", "opts": ["Multiply a row by 0", "Swap two rows", "Add a multiple of another row", "Multiply a row by 3"], "a": 0,
     "why": {"Swap two rows": _w("Allowed and reversible.", "مسموح وقابل للعكس.", "Permis."),
             "Add a multiple of another row": _w("Allowed and reversible.", "مسموح وقابل للعكس.", "Permis."),
             "Multiply a row by 3": _w("Allowed: non-zero factor.", "مسموح: عامل غير معدوم.", "Permis.")}, "ok": "×0 loses information"},
    {"q": "A reduction ends with 0 = 0 and a free unknown. This means …", "opts": ["infinitely many solutions", "no solution", "x = 0", "one solution"], "a": 0,
     "why": {"no solution": _w("Only 0 = k with k ≠ 0.", "فقط 0 = k مع k ≠ 0.", "k ≠ 0."),
             "x = 0": _w("0 = 0 does not give x = 0.", "0 = 0 لا تعطي x = 0.", "Non."),
             "one solution": _w("A free unknown remains.", "يبقى مجهول حر.", "Paramètre libre.")}, "ok": "family"},
]

THEORY = [
    ("Why a method?", "لماذا نحتاج طريقة؟", "Pourquoi une méthode ?", "", [
        T("Hello! Quick check first: x + y = 5 and x − y = 1. Adding them removes y and gives 2x = 6. That is the seed of elimination. Now look at 9x − 3y + 3z = 0, 5x + y − 6z = −1, x + y + z = 10. Are these three separate problems? No. We look for one triple that satisfies all three simultaneously. Success in two equations and failure in the third does not make a solution.",
          "مرحبًا! تحقق سريع أولًا: x + y = 5 وx − y = 1. جمعهما يحذف y ويعطي 2x = 6. هذه بذرة الحذف. الآن انظر إلى 9x − 3y + 3z = 0 و5x + y − 6z = −1 وx + y + z = 10. هل هي ثلاث مسائل منفصلة؟ لا. نبحث عن ثلاثية واحدة تحقق الثلاث معًا. النجاح في معادلتين والفشل في الثالثة لا يصنع حلًّا.",
          "Un seul triplet pour les trois."),
    ]),
    ("Three planes", "ثلاثة مستويات", "Trois plans", "", [
        T("Think of each linear equation in three unknowns as a plane. The common solution lives in the common intersection: one point, none, or infinitely many points. The picture builds intuition; elimination gives the verdict algebraically. Must any three planes meet in one point? No.",
          "تخيّل كل معادلة خطية بثلاثة مجاهيل مستويًا. الحل المشترك يقع في التقاطع المشترك: نقطة واحدة أو لا شيء أو عدد لا نهائي من النقاط. الرسم يبني الحدس والحذف يعطي الحكم جبريًا. هل يجب أن يلتقي أي ثلاثة مستويات في نقطة؟ لا.",
          "Un point, aucun, ou une infinité."),
    ]),
    ("Elimination and legal moves", "الحذف والحركات المسموحة", "Élimination et opérations", "", [
        T("We aim for a staircase: ax + by + cz = d, then ey + fz = g, then hz = k. We find z first, then back-substitute for y and x. The legal moves are Lᵢ ↔ Lⱼ, Lᵢ ← aLᵢ with a ≠ 0, and Lᵢ ← Lᵢ + aLⱼ with i ≠ j. Each is reversible, so the solution set is preserved. Multiplying a row by zero is blocked: the information is lost and cannot be reversed.",
          "نريد الوصول إلى شكل سلّمي: ax + by + cz = d ثم ey + fz = g ثم hz = k. نجد z أولًا ثم نعوّض رجعيًا لنجد y وx. الحركات المسموحة: Lᵢ ↔ Lⱼ وLᵢ ← aLᵢ مع a ≠ 0 وLᵢ ← Lᵢ + aLⱼ مع i ≠ j. كل منها قابلة للعكس فتُحفظ مجموعة الحلول. ضرب سطر في الصفر ممنوع: تضيع المعلومة ولا يمكن عكسه.",
          "Opérations réversibles."),
        F("Lᵢ ↔ Lⱼ      Lᵢ ← aLᵢ (a ≠ 0)      Lᵢ ← Lᵢ + aLⱼ"),
    ]),
    ("Plan before calculation", "الخطة قبل الحساب", "Le plan d'abord", "", [
        T("Plan: choose a pivot, make zeros below it, move diagonally, repeat, read the case, back-substitute, verify in the ORIGINAL system. A row with x-coefficient 1 is a comfortable pivot: fewer fractions and fewer errors. The choice of pivot does not change the solution; it is a calculation strategy.",
          "الخطة: نختار ارتكازًا ونصنع أصفارًا تحته ونتحرك قطريًا ونكرر ونقرأ الحالة ونعوّض رجعيًا ونتحقق في الجملة الأصلية. السطر الذي معامل x فيه 1 ارتكاز مريح: كسور أقل وأخطاء أقل. اختيار الارتكاز لا يغيّر الحل بل هو استراتيجية حساب.",
          "Pivot, zéros, remontée, vérifier."),
    ]),
    ("Full worked example", "مثال محلول كامل", "Exemple complet", "", [
        T("Solve x + y + z = 6, 2x − y + z = 3, 3x + y − z = 2. L₁ is the pivot. L₂ ← L₂ − 2L₁ gives −3y − z = −9, and L₃ ← L₃ − 3L₁ gives −2y − 4z = −16. Simplify the third: y + 2z = 8; the second: 3y + z = 9. Multiply y + 2z = 8 by 3: 3y + 6z = 24, subtract 3y + z = 9: 5z = 15, z = 3. Then y = 2 and x = 1.",
          "حلّ x + y + z = 6 و2x − y + z = 3 و3x + y − z = 2. L₁ هو الارتكاز. L₂ ← L₂ − 2L₁ تعطي −3y − z = −9 وL₃ ← L₃ − 3L₁ تعطي −2y − 4z = −16. نبسّط الثالثة: y + 2z = 8 والثانية: 3y + z = 9. نضرب y + 2z = 8 في 3: 3y + 6z = 24 ونطرح 3y + z = 9: 5z = 15 وz = 3. ثم y = 2 وx = 1.",
          "(1, 2, 3)."),
        F("−3y − z = −9      −2y − 4z = −16"),
        F("5z = 15  →  z = 3  →  y = 2  →  x = 1"),
        F("1 + 2 + 3 = 6      2 − 2 + 3 = 3      3 + 2 − 3 = 2"),
    ]),
    ("The pivot and the three cases", "الارتكاز والحالات الثلاث", "Pivot et trois cas", "", [
        T("A zero pivot does not mean no solution: look for another row with a non-zero coefficient and exchange. Reading the cases: unique, when the staircase fixes every unknown; none, when 0 = k with k ≠ 0 appears (a contradiction, so stop); infinite, when a redundant row 0 = 0 appears with free unknowns. 0 = 0 is not a contradiction and does not give unknown = 0.",
          "الارتكاز الصفري لا يعني انعدام الحل: نبحث عن سطر آخر بمعامل غير معدوم ونبدّل. قراءة الحالات: وحيد عندما يحدد الشكل السلّمي كل المجاهيل؛ لا حل عندما تظهر 0 = k مع k ≠ 0 (تناقض فنتوقف)؛ لا نهائي عندما يظهر سطر زائد 0 = 0 مع مجاهيل حرة. و0 = 0 ليست تناقضًا ولا تعطي مجهولًا = 0.",
          "Zéro pivot ≠ pas de solution."),
    ]),
    ("Infinite family", "عائلة لا نهائية", "Famille infinie", "", [
        T("x + y + z = 4, y + z = 2, 2y + 2z = 4. Notice the dependency before inventing a new equation: the third is 2 × the second. Choose z = t: y = 2 − t, x = 2. The family is (2, 2 − t, t), t ∈ ℝ. One free parameter generates infinitely many solutions; substitute symbolically in all three equations to check.",
          "x + y + z = 4 وy + z = 2 و2y + 2z = 4. نلاحظ الاعتماد قبل اختراع معادلة جديدة: الثالثة تساوي 2 × الثانية. نختار z = t فيكون y = 2 − t وx = 2. العائلة (2, 2 − t, t) حيث t ∈ ℝ. وسيط حر واحد يولّد عددًا لا نهائيًا من الحلول؛ نعوّض رمزيًا في المعادلات الثلاث للتحقق.",
          "(2, 2 − t, t)."),
        F("(x, y, z) = (2, 2 − t, t),  t ∈ ℝ"),
    ]),
    ("Error detectives", "المحققون", "Détectives", "", [
        T("1) Changing the left side but forgetting the right side: invalid operation; the whole row changes together. 2) Reading 0 = 0 as x = 0: false. 3) Continuing to solve 0 = 7: stop and classify as no solution. 4) Never checking in the original system. 5) Dividing by a parameter without checking it is non-zero: split cases first.",
          "1) تغيير الطرف الأيسر ونسيان الأيمن: عملية غير صالحة؛ السطر كله يتحول معًا. 2) قراءة 0 = 0 على أنها x = 0: خطأ. 3) متابعة حلّ 0 = 7: نتوقف ونصنّف لا حل. 4) عدم التحقق في الجملة الأصلية. 5) القسمة على وسيط دون التأكد أنه غير معدوم: نفصل الحالات أولًا.",
          "Cinq erreurs types."),
    ]),
    ("Student try", "جرّب بنفسك", "À toi", "", [
        T("Solve x + y + z = 6, 2x + 3y + z = 11, x + 2y + 3z = 14. L₂ ← L₂ − 2L₁ gives y − z = −1; L₃ ← L₃ − L₁ gives y + 2z = 8. Then y = z − 1, so 3z = 9, z = 3, y = 2, x = 1. Check: 1 + 2 + 3 = 6, 2 + 6 + 3 = 11, 1 + 4 + 9 = 14. Writing the plan first made the solution shorter and auditable.",
          "حلّ x + y + z = 6 و2x + 3y + z = 11 وx + 2y + 3z = 14. L₂ ← L₂ − 2L₁ تعطي y − z = −1؛ وL₃ ← L₃ − L₁ تعطي y + 2z = 8. ثم y = z − 1 فيكون 3z = 9 وz = 3 وy = 2 وx = 1. التحقق: 1 + 2 + 3 = 6 و2 + 6 + 3 = 11 و1 + 4 + 9 = 14. كتابة الخطة أولًا جعلت الحل أقصر وقابلًا للمراجعة.",
          "(1, 2, 3)."),
        F("1 + 2 + 3 = 6      2 + 6 + 3 = 11      1 + 4 + 9 = 14"),
    ]),
    ("Challenge and summary", "تحدٍّ وخلاصة", "Défi et résumé", "", [
        T("Challenge: build a system with exactly one solution, then change only one constant so it becomes impossible, and explain what changes in the echelon form. Summary: understand all the conditions, choose a pivot, zeros below, move diagonally, read the case (unique, none, infinite), back-substitute, verify in the original.",
          "تحدٍّ: ابنِ جملة لها حل واحد بالضبط ثم غيّر ثابتًا واحدًا فقط لتصبح مستحيلة واشرح ماذا تغيّر في الشكل السلّمي. الخلاصة: نفهم كل الشروط ونختار ارتكازًا ونصنع أصفارًا تحته ونتحرك قطريًا ونقرأ الحالة (وحيد أو لا شيء أو لا نهائي) ونعوّض رجعيًا ونتحقق في الأصل.",
          "Pivot, zéro, diagonale, cas, remontée, vérification."),
        F("PIVOT → ZERO BELOW → MOVE DIAGONALLY → READ THE CASE → SUBSTITUTE → VERIFY"),
    ]),
]

EXERCISES = [
    EX("1", "", st("Solve x + y + z = 6, 2x − y + z = 3, 3x + y − z = 2.", "حلّ x + y + z = 6 و2x − y + z = 3 و3x + y − z = 2.", "Résous."), [F("(1, 2, 3)")]),
    EX("2", "", st("A reduction ends with 0 = 9. Classify.", "ينتهي الاختزال بـ 0 = 9. صنّف.", "0 = 9."), [T("Contradiction: no solution.", "تناقض: لا حل.", "Aucune solution.")]),
    EX("3", "", st("Describe all solutions of x + y + z = 4, y + z = 2, 2y + 2z = 4.", "صف كل حلول x + y + z = 4 وy + z = 2 و2y + 2z = 4.", "Famille."), [F("(2, 2 − t, t)")]),
    EX("4", "", st("Solve x + y + z = 6, 2x + 3y + z = 11, x + 2y + 3z = 14.", "حلّ x + y + z = 6 و2x + 3y + z = 11 وx + 2y + 3z = 14.", "Résous."), [F("(1, 2, 3)")]),
    EX("5", "", st("Why does Lᵢ ← Lᵢ + aLⱼ preserve solutions?", "لماذا تحفظ Lᵢ ← Lᵢ + aLⱼ الحلول؟", "Pourquoi conserve ?"), [T("It is reversible: subtract aLⱼ again.", "قابلة للعكس: نطرح aLⱼ مجددًا.", "Réversible.")]),
]
