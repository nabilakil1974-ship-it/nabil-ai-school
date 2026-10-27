"""Grade 12 (LS) Mathematics — Exponential functions."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G12-MATH-LS-009"
GRADE = 12
SUBJECT = "math"
TITLES = {"en": "Exponential functions", "ar": "الدوال الأسية", "fr": "Fonctions exponentielles"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "3e^(2x) = 12 → x = ?", "opts": ["ln 2", "ln 4", "2 ln 2", "4"], "a": 0,
     "why": {"ln 4": _w("e^(2x) = 4 gives 2x = ln 4, so x = ln 4 / 2.", "e^(2x) = 4 تعطي 2x = ln 4 إذن x = ln 4 / 2.", "x = (ln 4)/2."),
             "2 ln 2": _w("That is 2x, not x.", "هذه 2x لا x.", "C'est 2x."),
             "4": _w("e^(2x) = 4, not 2x = 4.", "e^(2x) = 4.", "e^(2x) = 4.")}, "ok": "x = ln 2"},
    {"q": "e^(2x) − 5e^x + 6 = 0 → x = ?", "opts": ["ln 2 or ln 3", "2 or 3", "ln 5", "ln 6"], "a": 0,
     "why": {"2 or 3": _w("Those are values of u = eˣ.", "هذه قيم u = eˣ.", "Valeurs de u."),
             "ln 5": _w("Substitute u = eˣ and factor.", "نعوّض u = eˣ ونحلّل.", "u = eˣ."),
             "ln 6": _w("Substitute u = eˣ and factor.", "نعوّض u = eˣ ونحلّل.", "u = eˣ.")}, "ok": "u = 2 or 3"},
    {"q": "e^x = −1 has …", "opts": ["no real solution", "x = 0", "x = −1", "x = ln(−1)"], "a": 0,
     "why": {"x = 0": _w("e⁰ = 1.", "e⁰ = 1.", "e⁰ = 1."),
             "x = −1": _w("e⁻¹ > 0.", "e⁻¹ > 0.", "Positif."),
             "x = ln(−1)": _w("ln of a negative is undefined.", "ln لعدد سالب غير معرّف.", "Non défini.")}, "ok": "eˣ > 0"},
]

THEORY = [
    ("When the unknown moves into the exponent", "عندما ينتقل المجهول إلى الأس", "L'inconnue dans l'exposant", "", [
        T("Hello! Quick check: 2³ · 2⁴ = 2⁷ (same base, add exponents). Now 2ˣ = 8: where is the unknown? In the exponent. Ordinary linear algebra does not isolate x directly; the exponent structure or logarithms will. An exponential function turns additive changes in x into multiplicative changes in the output. Try 3ˣ = 27: x = 3 by recognising the same base.",
          "مرحبًا! تحقق سريع: 2³ · 2⁴ = 2⁷ (أساس واحد نجمع الأسس). الآن 2ˣ = 8: أين المجهول؟ في الأس. الجبر الخطي العادي لا يعزل x مباشرة؛ بنية الأس أو اللوغاريتمات ستفعل. الدالة الأسية تحوّل التغيرات الجمعية في x إلى تغيرات ضربية في المخرج. جرّب 3ˣ = 27: x = 3 بملاحظة الأساس نفسه.",
          "Exposant inconnu."),
    ]),
    ("Definition", "التعريف", "Définition", "", [
        T("f(x) = aˣ with a > 0 and a ≠ 1. Domain ℝ, range (0, ∞), f(0) = 1. Why a ≠ 1? Because 1ˣ is constant and has no growth or decay. Every exponential graph passes through (0, 1) and approaches but never reaches y = 0, so aˣ = 0 has no solution.",
          "f(x) = aˣ حيث a > 0 وa ≠ 1. المجال ℝ والمدى (0, ∞) وf(0) = 1. لماذا a ≠ 1؟ لأن 1ˣ ثابتة بلا نمو ولا تناقص. كل منحنى أسي يمر بالنقطة (0, 1) ويقترب من y = 0 دون أن يبلغه فلا حل لـ aˣ = 0.",
          "Domaine ℝ, image ]0, ∞[."),
        F("f(x) = aˣ,  a > 0, a ≠ 1      f(0) = 1"),
    ]),
    ("Growth or decay", "نمو أم تناقص", "Croissance ou décroissance", "", [
        T("2ˣ grows; (1/2)ˣ decreases. For a > 1 the exponential is increasing; for 0 < a < 1 it is decreasing. Increasing x by 1 multiplies the output by a: a^(x+1) = a · aˣ. For f(x) = 5 · 2ˣ, f(x+1)/f(x) = 2.",
          "2ˣ تنمو و(1/2)ˣ تتناقص. إذا كان a > 1 فالدالة متزايدة؛ وإذا كان 0 < a < 1 فهي متناقصة. زيادة x بمقدار 1 تضرب المخرج في a: a^(x+1) = a · aˣ. وفي f(x) = 5 · 2ˣ يكون f(x+1)/f(x) = 2.",
          "Facteur constant a."),
    ]),
    ("Inverse of ln", "عكس اللوغاريتم", "Réciproque de ln", "", [
        T("y = eˣ reflected across y = x gives y = ln x. ln(eˣ) = x for every real x, and e^(ln x) = x for x > 0. Examples: e^(ln 7) = 7 and ln(e⁻³) = −3. Domain and range swap exactly as inverse functions require.",
          "المنحنى y = eˣ منعكسًا حول y = x يعطي y = ln x. ln(eˣ) = x لكل x حقيقي وe^(ln x) = x لكل x > 0. أمثلة: e^(ln 7) = 7 وln(e⁻³) = −3. المجال والمدى يتبادلان تمامًا كما تقتضي الدوال العكسية.",
          "exp et ln réciproques."),
        F("ln(eˣ) = x      e^(ln x) = x  (x > 0)"),
    ]),
    ("Same base first", "الأساس نفسه أولًا", "Même base d'abord", "", [
        T("2^(x+1) = 8. Inspect the bases before using logarithms: 8 = 2³, so 2^(x+1) = 2³ and, as 2ᵗ is one-to-one, x + 1 = 3 and x = 2. Check: 2^(2+1) = 8. Use structure before heavier tools.",
          "2^(x+1) = 8. نفحص الأسس قبل استعمال اللوغاريتمات: 8 = 2³ فيكون 2^(x+1) = 2³ وبما أن 2ᵗ متباينة نجد x + 1 = 3 وx = 2. التحقق: 2^(2+1) = 8. نستعمل البنية قبل الأدوات الأثقل.",
          "x = 2."),
        F("2^(x+1) = 2³  →  x + 1 = 3  →  x = 2"),
    ]),
    ("Different bases: use ln", "أسس مختلفة: نستعمل ln", "Bases différentes : ln", "", [
        T("3e^(2x) = 12. Isolate the exponential first: e^(2x) = 4. The right side 4 > 0, so ln is valid. Apply ln: 2x = ln 4, so x = (ln 4)/2 = ln 2. Independent check: 3e^(2 ln 2) = 3e^(ln 4) = 12. Keep the exact logarithmic form before any decimal. Beware: ln(3 + e^(2x)) is not ln 3 + 2x.",
          "3e^(2x) = 12. نعزل الأسية أولًا: e^(2x) = 4. الطرف الأيمن 4 > 0 فاللوغاريتم صالح. نطبق ln: 2x = ln 4 إذن x = (ln 4)/2 = ln 2. تحقق مستقل: 3e^(2 ln 2) = 3e^(ln 4) = 12. نحتفظ بالصيغة اللوغاريتمية الدقيقة قبل أي قيمة عشرية. انتبه: ln(3 + e^(2x)) ليست ln 3 + 2x.",
          "x = ln 2."),
        F("e^(2x) = 4  →  2x = ln 4  →  x = ln 2"),
    ]),
    ("Graph transformations", "تحويلات المنحنى", "Transformations", "", [
        T("g(x) = e^(x−2) + 3: shift right 2 and up 3; the horizontal asymptote moves from y = 0 to y = 3. For 2eˣ − 5 the asymptote is y = −5. Common mistake: calling x = −5 the asymptote.",
          "g(x) = e^(x−2) + 3: انسحاب 2 إلى اليمين و3 إلى الأعلى؛ والمقارب الأفقي ينتقل من y = 0 إلى y = 3. وفي 2eˣ − 5 المقارب y = −5. خطأ شائع: تسمية x = −5 مقاربًا.",
          "Asymptote y = 3."),
    ]),
    ("Growth model", "نموذج النمو", "Modèle de croissance", "", [
        T("P(t) = P₀ e^(kt): P₀ = P(0) is the initial amount, and the sign of k decides growth (k > 0) or decay (k < 0). When does P(t) = 500e^(0.03t) reach 800? Divide by 500: e^(0.03t) = 1.6, so 0.03t = ln 1.6 and t = ln(1.6)/0.03. The logarithm releases the unknown time from the exponent.",
          "P(t) = P₀ e^(kt): P₀ = P(0) هي الكمية الابتدائية وإشارة k تحدد النمو (k > 0) أو التناقص (k < 0). متى تبلغ P(t) = 500e^(0.03t) القيمة 800؟ نقسم على 500: e^(0.03t) = 1.6 إذن 0.03t = ln 1.6 وt = ln(1.6)/0.03. اللوغاريتم يحرّر الزمن المجهول من الأس.",
          "t = ln(1,6)/0,03."),
        F("e^(0.03t) = 1.6  →  t = ln(1.6) / 0.03"),
    ]),
    ("Quadratic in eˣ", "معادلة من الدرجة الثانية في eˣ", "Quadratique en eˣ", "", [
        T("e^(2x) − 5eˣ + 6 = 0. Since e^(2x) = (eˣ)², put u = eˣ with u > 0: u² − 5u + 6 = 0, so (u − 2)(u − 3) = 0, u = 2 or 3, both positive. Then x = ln 2 or x = ln 3. Check in the original: eˣ = 2 or 3 zeroes the quadratic.",
          "e^(2x) − 5eˣ + 6 = 0. بما أن e^(2x) = (eˣ)² نضع u = eˣ مع u > 0: u² − 5u + 6 = 0 إذن (u − 2)(u − 3) = 0 وu = 2 أو 3 وكلاهما موجب. ثم x = ln 2 أو x = ln 3. نتحقق في الأصل: eˣ = 2 أو 3 تصفّر المعادلة.",
          "x = ln 2 ou ln 3."),
        F("u² − 5u + 6 = 0  →  u = 2, 3  →  x = ln 2, ln 3"),
    ]),
    ("Error detectives", "المحققون", "Détectives", "", [
        T("1) e^(a+b) = eᵃ + eᵇ is false: it is eᵃ·eᵇ. 2) e^(2x) = 2eˣ is false. 3) Do not confuse ln(eˣ) = x (all real x) with e^(ln x) = x (only x > 0). 4) eˣ = −2: stop, no real solution. 5) Do not use a decimal before the exact answer. 6) With k < 0 the model is decay, not growth. 7) After a vertical shift +3 the asymptote is y = 3, not y = 0.",
          "1) e^(a+b) = eᵃ + eᵇ خطأ: الصحيح eᵃ·eᵇ. 2) e^(2x) = 2eˣ خطأ. 3) لا نخلط ln(eˣ) = x (لكل x) مع e^(ln x) = x (فقط x > 0). 4) eˣ = −2: نتوقف، لا حل حقيقي. 5) لا نستعمل العشري قبل الجواب الدقيق. 6) مع k < 0 النموذج تناقص لا نمو. 7) بعد انسحاب رأسي +3 يصبح المقارب y = 3 لا y = 0.",
          "Sept erreurs types."),
    ]),
    ("Student try", "جرّب بنفسك", "À toi", "", [
        T("5eˣ − 10 = 0: 5eˣ = 10, eˣ = 2, so x = ln 2. Check: 5e^(ln 2) − 10 = 10 − 10 = 0. Summary: see the exponent, choose the structure, isolate, invert with the logarithm, check in the original.",
          "5eˣ − 10 = 0: 5eˣ = 10 وeˣ = 2 إذن x = ln 2. التحقق: 5e^(ln 2) − 10 = 10 − 10 = 0. الخلاصة: نرى الأس ونختار البنية ونعزل ونعكس باللوغاريتم ونتحقق في الأصل.",
          "x = ln 2."),
        F("5e^(ln 2) − 10 = 0"),
    ]),
]

EXERCISES = [
    EX("1", "", st("Solve 2ˣ = 16 and 3^(x−1) = 9.", "حلّ 2ˣ = 16 و3^(x−1) = 9.", "Résous."), [F("x = 4      x = 3")]),
    EX("2", "", st("Solve e^(3x) = 7 and 4e^(−x) = 9.", "حلّ e^(3x) = 7 و4e^(−x) = 9.", "Résous."), [F("x = (ln 7)/3      x = ln(4/9)")]),
    EX("3", "", st("Solve e^(2x) − 7eˣ + 12 = 0.", "حلّ e^(2x) − 7eˣ + 12 = 0.", "Résous."), [F("u = 3, 4      x = ln 3, ln 4")]),
    EX("4", "", st("Domain, range, asymptote of 2e^(x−1) − 4.", "المجال والمدى والمقارب لـ 2e^(x−1) − 4.", "Domaine, image, asymptote."), [F("ℝ      (−4, +∞)      y = −4")]),
    EX("5", "", st("Solve 7e^(2x) = 20 exactly.", "حلّ 7e^(2x) = 20 بدقة.", "Résous exactement."), [F("x = (1/2) ln(20/7)")]),
]
