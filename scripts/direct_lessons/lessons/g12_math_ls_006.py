"""Grade 12 (LS) Mathematics — Inverse trigonometric functions."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G12-MATH-LS-006"
GRADE = 12
SUBJECT = "math"
TITLES = {"en": "Inverse trigonometric functions", "ar": "الدوال المثلثية العكسية", "fr": "Fonctions trigonométriques réciproques"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "arcsin(sin(5π/6)) = ?", "opts": ["π/6", "5π/6", "−π/6", "π/3"], "a": 0,
     "why": {"5π/6": _w("5π/6 is outside [−π/2, π/2].", "5π/6 خارج [−π/2, π/2].", "Hors de l'intervalle."),
             "−π/6": _w("sin(5π/6) = +1/2.", "sin(5π/6) = +1/2.", "+1/2."),
             "π/3": _w("sin(π/3) = √3/2.", "sin(π/3) = √3/2.", "√3/2.")}, "ok": "π/6"},
    {"q": "arccos(cos(5π/4)) = ?", "opts": ["3π/4", "5π/4", "−3π/4", "π/4"], "a": 0,
     "why": {"5π/4": _w("arccos returns a value in [0, π].", "arccos تعطي قيمة في [0, π].", "Dans [0, π]."),
             "−3π/4": _w("Negative is outside [0, π].", "السالب خارج [0, π].", "Hors de [0, π]."),
             "π/4": _w("cos(π/4) = +√2/2.", "cos(π/4) = +√2/2.", "Signe.")}, "ok": "3π/4"},
    {"q": "Does arcsin x = 2π/3 have a real solution?", "opts": ["No", "Yes, x = √3/2", "Yes, x = −√3/2", "Yes, x = 1"], "a": 0,
     "why": {"Yes, x = √3/2": _w("2π/3 is outside the range of arcsin.", "2π/3 خارج مدى arcsin.", "Hors du domaine."),
             "Yes, x = −√3/2": _w("Outside the range.", "خارج المدى.", "Hors du domaine."),
             "Yes, x = 1": _w("arcsin 1 = π/2.", "arcsin 1 = π/2.", "π/2.")}, "ok": "range of arcsin is [−π/2, π/2]"},
]

THEORY = [
    ("Why a principal range?", "لماذا مجال أساسي؟", "Pourquoi un intervalle principal ?", "", [
        T("Hello! Quick check: sin(π/6) = 1/2, sin(5π/6) = 1/2 and sin(13π/6) = 1/2. Different inputs give the same output, so sine is not one-to-one on ℝ. If 1/2 enters an inverse-sine machine, which angle should come out? We cannot choose a unique answer before restricting sine. An inverse must be a function: each input has exactly one output. So we do not remove periodicity; we choose one branch.",
          "مرحبًا! تحقق سريع: sin(π/6) = 1/2 وsin(5π/6) = 1/2 وsin(13π/6) = 1/2. مدخلات مختلفة تعطي المخرج نفسه فالجيب ليس متباينًا على ℝ. إذا دخل 1/2 إلى آلة الجيب العكسي فأي زاوية يجب أن تخرج؟ لا نستطيع اختيار جواب وحيد قبل تقييد الجيب. العكس يجب أن يكون دالة: لكل مدخل مخرج واحد. لذلك لا نلغي الدورية بل نختار فرعًا واحدًا.",
          "Une seule sortie."),
    ]),
    ("Restrict before inverting", "نقيّد قبل أن نعكس", "Restreindre puis inverser", "", [
        T("The graph of y = sin x is cut by the line y = 1/2 many times. Keep only x ∈ [−π/2, π/2]: every horizontal line between −1 and 1 cuts the branch once. Sine restricted there is one-to-one and covers [−1, 1]. Reflect across y = x: domain and range swap, so arcsin: [−1, 1] → [−π/2, π/2].",
          "منحنى y = sin x يقطعه المستقيم y = 1/2 مرات كثيرة. نبقي فقط x ∈ [−π/2, π/2]: كل مستقيم أفقي بين −1 و1 يقطع الفرع مرة واحدة. الجيب المقيّد هناك متباين ويغطي [−1, 1]. نعكس حول y = x فيتبادل المجال والمدى: arcsin: [−1, 1] → [−π/2, π/2].",
          "Réflexion par rapport à y = x."),
        F("y = arcsin x  ⇔  sin y = x  and  y ∈ [−π/2, π/2]"),
    ]),
    ("arcsin: worked example", "arcsin: مثال محلول", "arcsin : exemple", "", [
        T("arcsin(√3/2): we ask for the one angle inside [−π/2, π/2]. The reference angle with sine √3/2 is π/3, and π/3 lies in the range, so arcsin(√3/2) = π/3. Check: sin(π/3) = √3/2 and π/3 is in the range. Another: arcsin(−√2/2) = −π/4 (negative sign, choose the angle inside the range).",
          "arcsin(√3/2): نسأل عن الزاوية الوحيدة داخل [−π/2, π/2]. الزاوية المرجعية التي جيبها √3/2 هي π/3 وهي تقع في المدى إذن arcsin(√3/2) = π/3. التحقق: sin(π/3) = √3/2 وπ/3 في المدى. مثال آخر: arcsin(−√2/2) = −π/4 (الإشارة سالبة فنختار الزاوية داخل المدى).",
          "π/3."),
        F("arcsin(√3/2) = π/3      arcsin(−√2/2) = −π/4"),
    ]),
    ("arccos and arctan", "arccos وarctan", "arccos et arctan", "", [
        T("Cosine is not one-to-one on [−π/2, π/2] (its values are symmetric about zero), so we choose [0, π], where it decreases from 1 to −1: arccos: [−1, 1] → [0, π]. Example: arccos(−1/2) = π − π/3 = 2π/3. Tangent: take (−π/2, π/2), where it maps onto ℝ: arctan: ℝ → (−π/2, π/2). Example: arctan(−1) = −π/4. The endpoints ±π/2 are not included because tangent is undefined there.",
          "الجيب تمام ليس متباينًا على [−π/2, π/2] (قيمه متناظرة حول الصفر) لذلك نختار [0, π] حيث يتناقص من 1 إلى −1: arccos: [−1, 1] → [0, π]. مثال: arccos(−1/2) = π − π/3 = 2π/3. الظل: نأخذ (−π/2, π/2) حيث يطبق على ℝ: arctan: ℝ → (−π/2, π/2). مثال: arctan(−1) = −π/4. والنهايتان ±π/2 غير مشمولتين لأن الظل غير معرّف هناك.",
          "Trois intervalles principaux."),
        F("arcsin: [−1,1]→[−π/2,π/2]   arccos: [−1,1]→[0,π]   arctan: ℝ→(−π/2,π/2)"),
    ]),
    ("Two compositions, two different questions", "تركيبان وسؤالان مختلفان", "Deux compositions", "", [
        T("sin(arcsin x) = x for x ∈ [−1, 1]. But arcsin(sin θ) = θ only when θ ∈ [−π/2, π/2]. In the first, arcsin automatically outputs an angle inside the range; in the second, θ may start outside and must be folded back to its principal representative. Example: arcsin(sin(−π/3)) = −π/3 because it is already principal.",
          "sin(arcsin x) = x لكل x ∈ [−1, 1]. أما arcsin(sin θ) = θ فقط عندما θ ∈ [−π/2, π/2]. في الأولى تُخرج arcsin زاوية داخل المدى تلقائيًا، وفي الثانية قد تبدأ θ من خارج المدى فيجب إرجاعها إلى ممثّلها الأساسي. مثال: arcsin(sin(−π/3)) = −π/3 لأنها أساسية أصلًا.",
          "Ne pas simplifier à l'aveugle."),
    ]),
    ("The cancellation trap", "فخ الاختصار", "Le piège de la simplification", "", [
        T("arcsin(sin(5π/6)): is 5π/6 in [−π/2, π/2]? No, 5π/6 > π/2. First sin(5π/6) = 1/2, then arcsin(1/2) = π/6. Cancelling symbols to get 5π/6 ignores the range of the inverse. arccos(cos(5π/4)): 5π/4 is not in [0, π]; cos(5π/4) = −√2/2 and the angle in [0, π] with that cosine is 3π/4. And arcsin(sin(3π/4)) = arcsin(√2/2) = π/4.",
          "arcsin(sin(5π/6)): هل 5π/6 في [−π/2, π/2]؟ لا فإن 5π/6 > π/2. أولًا sin(5π/6) = 1/2 ثم arcsin(1/2) = π/6. اختصار الرموز للحصول على 5π/6 يتجاهل مدى العكس. arccos(cos(5π/4)): 5π/4 ليست في [0, π]؛ cos(5π/4) = −√2/2 والزاوية في [0, π] بهذا الجيب تمام هي 3π/4. وarcsin(sin(3π/4)) = arcsin(√2/2) = π/4.",
          "π/6, 3π/4, π/4."),
        F("arcsin(sin(5π/6)) = arcsin(1/2) = π/6"),
        F("arccos(cos(5π/4)) = 3π/4"),
    ]),
    ("Equations", "المعادلات", "Équations", "", [
        T("arctan x = π/6: π/6 belongs to the range of arctan, so apply tangent: x = tan(π/6) = 1/√3. But does arcsin x = 2π/3 have a real solution? No: 2π/3 is outside the range of arcsin, even though the sine of 2π/3 exists.",
          "arctan x = π/6: π/6 تنتمي إلى مدى arctan فنطبق الظل: x = tan(π/6) = 1/√3. أما هل لـ arcsin x = 2π/3 حل حقيقي؟ لا: 2π/3 خارج مدى arcsin ولو كان جيبها موجودًا.",
          "Vérifier le domaine d'abord."),
        F("arctan x = π/6  ⇒  x = 1/√3"),
    ]),
    ("Error detectives", "المحققون", "Détectives", "", [
        T("1) sin⁻¹x is not 1/sin x (that is csc x). 2) arcsin(2) is not an angle over the reals: 2 is outside [−1, 1]. 3) arcsin(sin θ) = θ is not true for every θ. 4) An arccos answer of −π/3 is impossible: the range is [0, π]. 5) An arctan answer of π/2 is impossible: tangent is undefined there. 6) Do not mix degrees and radians.",
          "1) sin⁻¹x ليست 1/sin x (تلك csc x). 2) arcsin(2) ليست زاوية في الأعداد الحقيقية لأن 2 خارج [−1, 1]. 3) arcsin(sin θ) = θ غير صحيحة لكل θ. 4) جواب arccos يساوي −π/3 مستحيل: المدى [0, π]. 5) جواب arctan يساوي π/2 مستحيل: الظل غير معرّف هناك. 6) لا نخلط الدرجات بالراديان.",
          "Six erreurs types."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Periodic trig functions fail the horizontal-line test; we restrict to a branch, which is one-to-one, then reflect across y = x. Memory line: range first, reference angle, sign or quadrant, principal value, verify.",
          "الدوال المثلثية الدورية تفشل في اختبار الخط الأفقي؛ نقيّدها على فرع متباين ثم نعكس حول y = x. جملة للذاكرة: المدى أولًا ثم الزاوية المرجعية ثم الإشارة أو الربع ثم القيمة الأساسية ثم التحقق.",
          "Intervalle, angle de référence, signe, valeur principale, vérification."),
    ]),
]

EXERCISES = [
    EX("1", "", st("Evaluate arcsin(0), arcsin(1/2), arccos(0), arctan(1).", "احسب arcsin(0) وarcsin(1/2) وarccos(0) وarctan(1).", "Calcule."), [F("0      π/6      π/2      π/4")]),
    EX("2", "", st("Simplify arcsin(sin(−π/4)), arcsin(sin(2π/3)), arccos(cos(4π/3)).", "بسّط arcsin(sin(−π/4)) وarcsin(sin(2π/3)) وarccos(cos(4π/3)).", "Simplifie."), [F("−π/4      π/3      2π/3")]),
    EX("3", "", st("Evaluate arccos(cos(7π/6)) and explain.", "احسب arccos(cos(7π/6)) واشرح.", "Calcule et explique."), [F("cos(7π/6) = −√3/2      arccos = 5π/6")]),
    EX("4", "", st("Solve arctan x = π/3 and arctan x = −π/4.", "حلّ arctan x = π/3 وarctan x = −π/4.", "Résous."), [F("x = √3      x = −1")]),
    EX("5", "", st("Why does arcsin x = 3π/4 have no real solution?", "لماذا لا يوجد حل حقيقي لـ arcsin x = 3π/4؟", "Pourquoi pas de solution ?"), [T("3π/4 is outside [−π/2, π/2].", "3π/4 خارج [−π/2, π/2].", "Hors de l'intervalle.")]),
]
