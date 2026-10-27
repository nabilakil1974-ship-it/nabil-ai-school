"""Grade 11 Mathematics — Systems of linear equations (Gaussian elimination)."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G11-MATH-EN-001"
GRADE = 11
SUBJECT = "math"
TITLES = {"en": "Systems of linear equations", "ar": "جمل المعادلات الخطية", "fr": "Systèmes d'équations linéaires"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "x + y + z = 6, 2x − y + z = 3, 3x + y − z = 2. Which triple is the solution?", "opts": ["(1, 2, 3)", "(3, 2, 1)", "(2, 2, 2)", "(1, 1, 4)"], "a": 0,
     "why": {"(3, 2, 1)": _w("Check the 2nd equation: 6 − 2 + 1 = 5 ≠ 3.", "المعادلة الثانية: 6 − 2 + 1 = 5 ≠ 3.", "2e équation : 5 ≠ 3."),
             "(2, 2, 2)": _w("3x + y − z = 6 ≠ 2.", "3x + y − z = 6 ≠ 2.", "6 ≠ 2."),
             "(1, 1, 4)": _w("2x − y + z = 5 ≠ 3.", "2x − y + z = 5 ≠ 3.", "5 ≠ 3.")}, "ok": "(1, 2, 3)"},
    {"q": "A reduction ends with 0 = 5. The system has …", "opts": ["no solution", "one solution", "infinitely many", "z = 5"], "a": 0,
     "why": {"one solution": _w("0 = 5 is a contradiction.", "0 = 5 تناقض.", "Contradiction."),
             "infinitely many": _w("That is 0 = 0.", "هذا 0 = 0.", "C'est 0 = 0."),
             "z = 5": _w("No unknown remains in 0 = 5.", "لا مجهول في 0 = 5.", "Aucune inconnue.")}, "ok": "inconsistent"},
    {"q": "A reduction ends with 0 = 0 and a free unknown. The system has …", "opts": ["infinitely many solutions", "no solution", "exactly one", "exactly two"], "a": 0,
     "why": {"no solution": _w("0 = 0 is always true.", "0 = 0 صحيحة دائمًا.", "Toujours vraie."),
             "exactly one": _w("A free parameter remains.", "يبقى وسيط حر.", "Paramètre libre."),
             "exactly two": _w("Linear systems: 0, 1 or infinitely many.", "0 أو 1 أو لا نهاية.", "0, 1 ou ∞.")}, "ok": "family of solutions"},
]

THEORY = [
    ("What is a linear system?", "ما هي الجملة الخطية؟", "Qu'est-ce qu'un système ?", "11", [
        T("Hello! Before we eliminate, I do not want you to memorise steps without meaning. Imagine three pieces of information about three unknown quantities x, y, z. Each equation restricts the possibilities. We look for the values that satisfy all three equations at the same time. Values that satisfy two equations but not the third are not a solution.",
          "مرحبًا! قبل أن نبدأ بالحذف لا أريدك أن تحفظ خطوات بلا معنى. تخيّل ثلاث معلومات عن ثلاث كميات مجهولة x وy وz. كل معادلة تقيّد الاحتمالات. نبحث عن القيم التي تحقق المعادلات الثلاث معًا في الوقت نفسه. قيم تحقق معادلتين ولا تحقق الثالثة ليست حلًّا للجملة.",
          "Les trois équations en même temps."),
        F("2x + y − z = 5"),
        F("x − y + 2z = 1"),
        F("3x + 2y + z = 10"),
        T("Checkpoint: if I give you (1, 2, 0), substitute it in all three equations, not in one only.",
          "نقطة تحقق: إذا أعطيتك (1, 2, 0) فعوّضها في المعادلات الثلاث لا في واحدة فقط.",
          "Teste dans les trois."),
    ]),
    ("Why Gaussian elimination?", "لماذا طريقة غاوس؟", "Pourquoi Gauss ?", "12", [
        T("Instead of solving three equations at once, we transform the system into an easier equivalent one, usually triangular (echelon) form, without changing the solution set. We then start from the last equation, find z, go up to find y, then x. This is back-substitution.",
          "بدل حل المعادلات الثلاث دفعة واحدة نحوّل الجملة إلى جملة مكافئة أسهل، غالبًا مثلثية (سلّمية)، دون تغيير مجموعة الحلول. ثم نبدأ من المعادلة الأخيرة فنجد z ثم نصعد لنجد y ثم x. هذا هو التعويض الرجعي.",
          "Forme triangulaire puis remontée."),
        F("ax + by + cz = d"),
        F("      ey + fz = g"),
        F("           hz = k"),
    ]),
    ("Safe operations", "العمليات المأمونة", "Opérations sûres", "14", [
        T("Two operations protect the solution: interchange two equations; replace an equation by itself plus a multiple of another. A non-equivalent transformation may give pretty numbers that do not solve the original system.",
          "عمليتان تحميان الحل: تبديل معادلتين، واستبدال معادلة بنفسها زائد مضاعف لمعادلة أخرى. أي تحويل غير مكافئ قد يعطي أرقامًا جميلة لا تحل الجملة الأصلية.",
          "Échange ; Li ← Li + k·Lj."),
        T("Error detective: a student changed L2 into 2·L2 but forgot to multiply every term. That changes its meaning. An operation on an equation applies to the whole equation.",
          "المحقق: حوّل طالب L2 إلى 2·L2 لكنه نسي ضرب كل الحدود. هذا غيّر معناها. العملية على المعادلة تطبق على المعادلة كلها.",
          "Toute l'équation."),
    ]),
    ("Guided example", "مثال موجَّه", "Exemple guidé", "15", [
        T("Solve x + y + z = 6, 2x − y + z = 3, 3x + y − z = 2. L1 is the pivot equation because the coefficient of x is 1. L2 ← L2 − 2L1 gives −3y − z = −9. L3 ← L3 − 3L1 gives −2y − 4z = −16.",
          "حلّ x + y + z = 6 و2x − y + z = 3 و3x + y − z = 2. نختار L1 معادلة ارتكاز لأن معامل x فيها 1. L2 ← L2 − 2L1 تعطي −3y − z = −9. وL3 ← L3 − 3L1 تعطي −2y − 4z = −16.",
          "Pivot L1."),
        F("x + y + z = 6"),
        F("−3y − z = −9"),
        F("−2y − 4z = −16"),
        T("From the second: 3y + z = 9. The third divided by −2: y + 2z = 8, so y = 8 − 2z. Substitute: 3(8 − 2z) + z = 9, so 24 − 5z = 9 and z = 3. Then y = 2 and x = 1.",
          "من الثانية: 3y + z = 9. والثالثة بعد القسمة على −2: y + 2z = 8 أي y = 8 − 2z. نعوّض: 3(8 − 2z) + z = 9 إذن 24 − 5z = 9 وz = 3. ثم y = 2 وx = 1.",
          "z = 3, y = 2, x = 1."),
        F("(x, y, z) = (1, 2, 3)"),
        T("We do not stop: check in the ORIGINAL system. 1 + 2 + 3 = 6, 2 − 2 + 3 = 3, 3 + 2 − 3 = 2. All true.",
          "لا نتوقف: نتحقق في الجملة الأصلية. 1 + 2 + 3 = 6 و2 − 2 + 3 = 3 و3 + 2 − 3 = 2. كلها صحيحة.",
          "Vérifie."),
    ]),
    ("The pivot", "عنصر الارتكاز", "Le pivot", "16", [
        T("The pivot is the coefficient we use as a support for elimination. If it is zero, we do not give up: we may interchange equations to get a usable pivot. Error detective: a student reached pivot 0 and said “no solution”. Wrong! A zero pivot alone does not mean no solution. Can I interchange? What do the other equations say?",
          "عنصر الارتكاز هو المعامل الذي نتكئ عليه في الحذف. إذا كان صفرًا فلا نستسلم: قد نبدّل المعادلات لنحصل على ارتكاز صالح. المحقق: وصل طالب إلى ارتكاز 0 وقال «لا حل». خطأ! الارتكاز الصفري وحده لا يعني انعدام الحل. هل أستطيع التبديل؟ وماذا تقول بقية المعادلات؟",
          "Pivot nul : échanger."),
    ]),
    ("Three possible outcomes", "ثلاث نتائج ممكنة", "Trois issues", "17", [
        T("A) One solution: three independent pieces of information fix x, y, z uniquely. B) No solution: the reduction produces an impossible equation 0x + 0y + 0z = 5, that is 0 = 5. That is a contradiction: the system is inconsistent. C) Infinitely many solutions: an equation 0 = 0 appears while an unknown stays free.",
          "أ) حل وحيد: ثلاث معلومات مستقلة تحدد x وy وz بصورة وحيدة. ب) لا حل: يظهر في الاختزال معادلة مستحيلة 0x + 0y + 0z = 5 أي 0 = 5. هذا تناقض: الجملة غير متسقة. ج) عدد لا نهائي من الحلول: تظهر معادلة 0 = 0 مع بقاء مجهول حر.",
          "Un, aucun, une infinité."),
        T("Example: x + y + z = 4, y + z = 2, 2y + 2z = 4. The third repeats the second. Put z = t: y = 2 − t, and from the first x = 2. So (x, y, z) = (2, 2 − t, t) for every real t.",
          "مثال: x + y + z = 4 وy + z = 2 و2y + 2z = 4. الثالثة تكرر الثانية. نضع z = t فيكون y = 2 − t ومن الأولى x = 2. إذن (x, y, z) = (2, 2 − t, t) لكل عدد حقيقي t.",
          "Famille de solutions."),
        F("(x, y, z) = (2, 2 − t, t),  t ∈ ℝ"),
    ]),
    ("Geometric picture", "الصورة الهندسية", "Image géométrique", "18", [
        T("Each linear equation in three unknowns is a plane in space. The common solution is what the three planes share: one point, no common point, or a shared intersection with infinitely many points. The drawing helps understanding, but elimination gives the verdict algebraically.",
          "كل معادلة خطية بثلاثة مجاهيل يمكن أن نفكر فيها كمستوٍ في الفضاء. الحل المشترك هو ما تشترك فيه المستويات الثلاثة: نقطة واحدة أو لا نقطة مشتركة أو تقاطع مشترك فيه عدد لا نهائي من النقاط. الرسم يساعد على الفهم أما الحذف فيعطي الحكم جبريًا.",
          "Trois plans."),
    ]),
    ("Word problem", "مسألة لفظية", "Problème", "19", [
        T("The hardest step is often building the equations. A class bought 29 items: notebooks n, pens p, rulers r. Notebooks exceed pens by 4, and rulers are half the pens. So n + p + r = 29, n − p = 4, 2r − p = 0. From n = p + 4 and r = p/2: p + 4 + p + p/2 = 29, so (5/2)p = 25, p = 10, n = 14, r = 5. Check: 14 + 10 + 5 = 29.",
          "أصعب خطوة غالبًا بناء المعادلات. اشترى صف 29 قطعة: دفاتر n وأقلام p ومساطر r. الدفاتر تزيد 4 عن الأقلام والمساطر نصف الأقلام. إذن n + p + r = 29 وn − p = 4 و2r − p = 0. من n = p + 4 وr = p/2: p + 4 + p + p/2 = 29 إذن (5/2)p = 25 وp = 10 وn = 14 وr = 5. نتحقق: 14 + 10 + 5 = 29.",
          "n = 14, p = 10, r = 5."),
        F("n + p + r = 29   n − p = 4   2r − p = 0"),
        T("With a total of 30 we would get p = 52/5, not a whole number of objects. That does not mean algebra failed: the model itself gives no valid counts. Always ask: is the result sensible in context?",
          "لو كان المجموع 30 لحصلنا على p = 52/5 وهو ليس عددًا صحيحًا من الأشياء. هذا لا يعني فشل الجبر بل أن النموذج لا يعطي أعدادًا صالحة. نسأل دائمًا: هل النتيجة منطقية في السياق؟",
          "Résultat sensé ?"),
    ]),
    ("Challenge", "تحدٍّ", "Défi", "20", [
        T("Solve x + y + z = 6, 2x + 3y + z = 11, x + 2y + 3z = 14. First move: use L1 to remove x from L2 and L3. L2 − 2L1: y − z = −1. L3 − L1: y + 2z = 8. Then y = z − 1, so 3z − 1 = 8, z = 3, y = 2, x = 1.",
          "حلّ x + y + z = 6 و2x + 3y + z = 11 وx + 2y + 3z = 14. أول حركة: نستعمل L1 لحذف x من L2 وL3. L2 − 2L1: y − z = −1. L3 − L1: y + 2z = 8. ثم y = z − 1 فيكون 3z − 1 = 8 وz = 3 وy = 2 وx = 1.",
          "(1, 2, 3)."),
        F("y − z = −1      y + 2z = 8"),
        F("(1, 2, 3)"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("System: all equations hold simultaneously. Gauss: transform into an easier equivalent system. Safe moves: interchange, add a multiple. Contradiction means no solution; 0 = 0 with a free unknown means infinitely many. Final habit: reduce, solve, check in the original, interpret.",
          "الجملة: كل المعادلات تتحقق معًا. غاوس: نحوّل إلى جملة مكافئة أسهل. حركات مأمونة: التبديل وإضافة مضاعف. التناقض يعني لا حل، و0 = 0 مع مجهول حر يعني عددًا لا نهائيًا. العادة الأخيرة: نختزل ونحلّ ونتحقق في الأصل ونفسّر.",
          "Réduire, résoudre, vérifier."),
    ]),
]

EXERCISES = [
    EX("1", "", st("Solve x + y + z = 6, 2x − y + z = 3, 3x + y − z = 2.", "حلّ x + y + z = 6 و2x − y + z = 3 و3x + y − z = 2.", "Résous le système."), [F("(1, 2, 3)")]),
    EX("2", "", st("A reduction ends with 0 = 9. Classify and explain.", "ينتهي الاختزال بـ 0 = 9. صنّف واشرح.", "0 = 9 : que conclure ?"), [T("Contradiction: no solution.", "تناقض: لا حل.", "Aucune solution.")]),
    EX("3", "", st("x + y + z = 4, y + z = 2, 2y + 2z = 4: write the family of solutions.", "اكتب عائلة حلول الجملة x + y + z = 4 وy + z = 2 و2y + 2z = 4.", "Famille de solutions."), [F("(2, 2 − t, t)")]),
    EX("4", "", st("Solve x + y + z = 6, 2x + 3y + z = 11, x + 2y + 3z = 14.", "حلّ x + y + z = 6 و2x + 3y + z = 11 وx + 2y + 3z = 14.", "Résous."), [F("(1, 2, 3)")]),
    EX("5", "", st("Why do we check in the original system?", "لماذا نتحقق في الجملة الأصلية؟", "Pourquoi vérifier ?"), [T("The reduction may hide an arithmetic error.", "قد يخفي الاختزال خطأ حسابيًا.", "Erreur de calcul.")]),
]
