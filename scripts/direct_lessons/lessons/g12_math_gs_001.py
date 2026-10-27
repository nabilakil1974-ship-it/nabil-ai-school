"""Grade 12 (GS) Mathematics — Irrational functions."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G12-MATH-GS-001"
GRADE = 12
SUBJECT = "math"
TITLES = {"en": "Irrational functions", "ar": "الدوال اللاجذرية", "fr": "Fonctions irrationnelles"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "Domain of f(x) = √((x − 1)(x + 3)) ?", "opts": ["(−∞, −3] ∪ [1, +∞)", "[−3, 1]", "ℝ", "[1, +∞)"], "a": 0,
     "why": {"[−3, 1]": _w("The product is NEGATIVE between −3 and 1.", "الجداء سالب بين −3 و1.", "Négatif entre."),
             "ℝ": _w("Require (x−1)(x+3) ≥ 0.", "نشترط (x−1)(x+3) ≥ 0.", "Condition ≥ 0."),
             "[1, +∞)": _w("x ≤ −3 also works.", "x ≤ −3 يصلح أيضًا.", "x ≤ −3 aussi.")}, "ok": "two branches"},
    {"q": "√(x²) = ?", "opts": ["|x|", "x", "−x", "x²"], "a": 0,
     "why": {"x": _w("Try x = −5: √25 = 5.", "جرّب x = −5: √25 = 5.", "x = −5."),
             "−x": _w("Only for x < 0.", "فقط عند x < 0.", "Si x < 0."),
             "x²": _w("The root undoes the square.", "الجذر يلغي التربيع.", "Racine.")}, "ok": "|x|"},
    {"q": "x = a is excluded from the domain. Is it automatically a vertical asymptote?", "opts": ["No: check a one-sided limit", "Yes", "Only for roots", "Always for 1/√"], "a": 0,
     "why": {"Yes": _w("It can be an endpoint.", "قد تكون نقطة طرف.", "Peut être une borne."),
             "Only for roots": _w("The limit decides.", "النهاية تحسم.", "La limite décide."),
             "Always for 1/√": _w("Still needs the limit.", "تحتاج النهاية.", "Limite.")}, "ok": "limit decides"},
]

THEORY = [
    ("Where does the function exist?", "أين توجد الدالة؟", "Où la fonction existe-t-elle ?", "", [
        T("Before any derivative or limit, one question only: where does the function exist at all? A radical means that the domain leads everything after it. If we are wrong here, every graph and derivative is built on a wrong ground.",
          "قبل أي مشتقة أو نهاية سؤال واحد فقط: أين توجد الدالة أصلًا؟ وجود جذر يعني أن المجال هو الذي يقود كل شيء بعده. إذا أخطأنا هنا بُني كل رسم وكل مشتقة بعده على أرض خاطئة.",
          "Le domaine d'abord."),
        F("√g(x): g(x) ≥ 0        1/√g(x): g(x) > 0"),
    ]),
    ("Domain with two branches", "مجال بفرعين", "Domaine à deux branches", "", [
        T("Take f(x) = √((x − 1)(x + 3)). Mark 1 and −3 on a number line and find the signs yourself: the product is ≥ 0 for D = (−∞, −3] ∪ [1, +∞). Geometrically the graph has two separate branches, and you may not join them with a line inside (−3, 1). This is the first drawing decision, not a minor detail.",
          "لتكن f(x) = √((x − 1)(x + 3)). نضع 1 و−3 على محور الأعداد ونحدد الإشارات بأنفسنا: الجداء ≥ 0 عندما D = (−∞, −3] ∪ [1, +∞). هندسيًا للرسم فرعان منفصلان ولا يحق لنا أن نصل بينهما بخط داخل (−3, 1). هذا أول قرار رسم لا تفصيل ثانوي.",
          "Deux branches."),
        F("D = (−∞, −3] ∪ [1, +∞)"),
        T("Endpoints: A(−3, 0) and B(1, 0). The two branches are studied separately.",
          "نقطتا الطرف: A(−3, 0) وB(1, 0). ندرس الفرعين كلًا على حدة.",
          "Bornes A et B."),
    ]),
    ("Why this order?", "لماذا هذا الترتيب؟", "Pourquoi cet ordre ?", "", [
        T("I do not want you to memorise the sequence because I said so. Domain tells us where to look. Endpoints tell where each branch starts or ends. Limits tell what happens near the boundaries. The derivative tells how the branch moves. An asymptote is accepted only with a limit proof. Only after all that do we draw.",
          "لا أريدك أن تحفظ التسلسل لأنني قلته. المجال يقول أين نبحث. نقاط الطرف تقول أين يبدأ الفرع أو ينتهي. النهايات تقول ما يحدث قرب الحدود. المشتقة تقول كيف يتحرك الفرع. والمقارب لا نقبله إلا ببرهان نهاية. وبعد كل ذلك فقط نرسم.",
          "Domaine → bornes → limites → dérivée → asymptotes."),
        F("DOMAIN → ENDPOINTS → LIMITS → DERIVATIVE → VARIATIONS → ASYMPTOTES → GRAPH → CHECK"),
    ]),
    ("Endpoint example", "مثال نقطة طرف", "Exemple : borne", "", [
        T("f(x) = √(x + 2). D = [−2, +∞), endpoint A(−2, 0). f′(x) = 1 / (2√(x + 2)) > 0 for x > −2, so f is increasing. As x → −2⁺, f′(x) → +∞: the curve has a vertical tangent at the endpoint.",
          "f(x) = √(x + 2). D = [−2, +∞) ونقطة الطرف A(−2, 0). f′(x) = 1 / (2√(x + 2)) > 0 عندما x > −2 فالدالة متزايدة. وعندما x → −2⁺ فإن f′(x) → +∞: للمنحنى مماس رأسي عند نقطة الطرف.",
          "Tangente verticale en A."),
        F("f′(x) = 1 / (2√(x + 2))"),
    ]),
    ("Asymptote test with a conjugate", "اختبار المقارب بالمرافق", "Test d'asymptote", "", [
        T("Study f(x) = √(x² + 2x + 5) at +∞. The dominant part looks like x, but that is not enough to prove an asymptote. Compare with x + 1, since x² + 2x + 5 is close to (x + 1)². Using the conjugate: f(x) − (x + 1) = 4 / [√(x² + 2x + 5) + x + 1] → 0. So y = x + 1 is an asymptote at +∞.",
          "ندرس f(x) = √(x² + 2x + 5) عند +∞. الجزء المهيمن يشبه x لكن هذا لا يكفي لإثبات مقارب. نقارن مع x + 1 لأن x² + 2x + 5 قريبة من (x + 1)². باستعمال المرافق: f(x) − (x + 1) = 4 / [√(x² + 2x + 5) + x + 1] → 0. إذن y = x + 1 مقارب عند +∞.",
          "y = x + 1 à +∞."),
        F("f(x) − (x + 1) = 4 / (√(x² + 2x + 5) + x + 1) → 0"),
        T("Check: we do not transfer the same result automatically to −∞, because √(x²) = |x| and there |x| = −x.",
          "تحقق: لا ننقل النتيجة نفسها تلقائيًا إلى −∞ لأن √(x²) = |x| وهناك |x| = −x.",
          "Traite −∞ séparément."),
    ]),
    ("Asymptote vs direction", "المقارب والاتجاه المقارب", "Asymptote et direction", "", [
        T("If lim f(x) = L as x → ±∞ then y = L is a horizontal asymptote in that direction. To test y = ax + b study f(x) − (ax + b): if it tends to 0, the line is an oblique asymptote. A curve can have an asymptotic direction of slope a even when f(x) − (ax + b) tends to no 0 for any b: same direction is weaker than same line.",
          "إذا كانت lim f(x) = L عندما x → ±∞ فإن y = L مقارب أفقي في ذلك الاتجاه. ولاختبار y = ax + b ندرس f(x) − (ax + b): إذا نزعت إلى 0 فالمستقيم مقارب مائل. وقد يكون للمنحنى اتجاه مقارب ميله a حتى لو لم تنتهِ f(x) − (ax + b) إلى 0 لأي b: «الاتجاه نفسه» أضعف من «المستقيم نفسه».",
          "Direction ≠ asymptote."),
    ]),
    ("Error detectives", "المحققون", "Détectives", "", [
        T("1) Differentiating √(x − 3) for every real x: first x − 3 ≥ 0, so D = [3, +∞), and the derivative is considered for x > 3. 2) Writing √(x²) = x for all x: try x = −5, √25 = 5 ≠ −5, so it is |x|. 3) “x = a is not in D, so it is a vertical asymptote”: only if the appropriate one-sided limit is infinite. 4) “The slope is a at infinity, so y = ax + b is an asymptote”: you must prove f(x) − (ax + b) → 0.",
          "1) اشتقاق √(x − 3) لكل عدد حقيقي: نشترط أولًا x − 3 ≥ 0 فيكون D = [3, +∞) وتُدرس المشتقة عندما x > 3. 2) كتابة √(x²) = x دائمًا: جرّب x = −5 فنجد √25 = 5 ≠ −5 فهي |x|. 3) «x = a ليست في D إذن مقارب رأسي»: فقط إذا كانت النهاية من جهة واحدة لا نهائية. 4) «الميل a عند اللانهاية إذن y = ax + b مقارب»: يجب إثبات f(x) − (ax + b) → 0.",
          "Quatre erreurs types."),
    ]),
    ("Practice ladder", "سلّم التدريب", "Entraînement", "", [
        T("Level 1: √(5 − x) gives x ≤ 5, D = (−∞, 5]. 1/√(x − 2) gives x > 2, D = (2, +∞). √(x² − 9) gives x ≤ −3 or x ≥ 3. Level 2: f(x) = √(x² + 4) is even, f′(x) = x / √(x² + 4), decreasing on (−∞, 0], increasing on [0, +∞), minimum f(0) = 2. Level 3: √(x² + 4) − x = 4 / [√(x² + 4) + x] → 0, so y = x is an asymptote at +∞; repeat at −∞ with |x|.",
          "المستوى 1: √(5 − x) تعطي x ≤ 5 أي D = (−∞, 5]. و1/√(x − 2) تعطي x > 2 أي D = (2, +∞). و√(x² − 9) تعطي x ≤ −3 أو x ≥ 3. المستوى 2: الدالة f(x) = √(x² + 4) زوجية وf′(x) = x / √(x² + 4) فهي متناقصة على (−∞, 0] ومتزايدة على [0, +∞) وصغراها f(0) = 2. المستوى 3: √(x² + 4) − x = 4 / [√(x² + 4) + x] → 0 إذن y = x مقارب عند +∞، ونكرر عند −∞ مع |x|.",
          "Niveaux 1 à 3."),
        F("f′(x) = x / √(x² + 4)      f(0) = 2"),
    ]),
    ("Transfer challenge", "تحدّي النقل", "Défi de transfert", "", [
        T("Study f(x) = √(x² − 4x + 8) without differentiating first. Rewrite the radicand as (x − 2)² + 4 > 0, so D = ℝ and there is no finite endpoint. From the structure f(x) ≥ 2 with equality at x = 2, so the minimum is 2. Use the derivative only to confirm the variation, and compare +∞ and −∞ separately with |x|. This is our own transfer problem, not a textbook question.",
          "ندرس f(x) = √(x² − 4x + 8) دون أن نشتق أولًا. نعيد كتابة ما تحت الجذر (x − 2)² + 4 > 0 فيكون D = ℝ ولا توجد نقطة طرف منتهية. ومن البنية f(x) ≥ 2 مع المساواة عند x = 2 فالصغرى 2. نستعمل المشتقة فقط لتأكيد التغيرات ونقارن +∞ و−∞ كلًّا على حدة مع |x|. هذه مسألة نقل من إعدادنا وليست من الكتاب.",
          "Minimum 2 en x = 2."),
        F("x² − 4x + 8 = (x − 2)² + 4"),
    ]),
    ("Final check and rule", "التحقق والقاعدة", "Vérification finale", "", [
        T("Before accepting a graph: every drawn x is in D; every endpoint is justified; one-sided limits respect the domain; derivative signs match the variations; asymptotes are proved by limits; +∞ and −∞ are treated separately; √(x²) is handled as |x|. Never draw first and justify later.",
          "قبل قبول الرسم: كل x مرسوم ينتمي إلى D؛ كل نقطة طرف مبررة؛ النهايات من جهة واحدة تحترم المجال؛ إشارات المشتقة تطابق التغيرات؛ المقاربات مثبتة بالنهايات؛ +∞ و−∞ يُعالجان كلًّا على حدة؛ √(x²) تُعالج كـ |x|. لا نرسم أولًا ونبرر لاحقًا.",
          "Ne jamais dessiner d'abord."),
    ]),
]

EXERCISES = [
    EX("1", "", st("Find the domain of √(5 − x), 1/√(x − 2) and √(x² − 9).", "أوجد مجال √(5 − x) و1/√(x − 2) و√(x² − 9).", "Domaines."), [F("(−∞, 5]      (2, +∞)      (−∞, −3] ∪ [3, +∞)")]),
    EX("2", "", st("Study the variations of √(x² + 4).", "ادرس تغيرات √(x² + 4).", "Variations."), [F("f′(x) = x / √(x² + 4)      min f(0) = 2")]),
    EX("3", "", st("Show √(x² + 4) − x → 0 at +∞.", "بيّن أن √(x² + 4) − x → 0 عند +∞.", "Montre la limite."), [F("4 / (√(x² + 4) + x) → 0")]),
    EX("4", "", st("Error detective: √(x²) = x for all x.", "المحقق: √(x²) = x لكل x.", "Détective."), [F("x = −5:  √25 = 5  ⇒  |x|")]),
    EX("5", "", st("Challenge: asymptote of √(x² + αx + β) at +∞.", "تحدٍّ: مقارب √(x² + αx + β) عند +∞.", "Défi."), [F("y = x + α/2")]),
]
