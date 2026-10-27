"""Grade 10 Mathematics — Powers of a real number."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G10-MATH-EN-004"
GRADE = 10
SUBJECT = "math"
TITLES = {"en": "Powers of a real number", "ar": "قوى عدد حقيقي", "fr": "Puissances d'un réel"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "x⁴ · x⁷ = ?", "opts": ["x¹¹", "x²⁸", "x³", "2x¹¹"], "a": 0,
     "why": {"x²⁸": _w("Same base, product: ADD the exponents.", "الأساس نفسه والضرب: نجمع الأسس.", "Produit : on ajoute."),
             "x³": _w("That is subtraction. For a product, add.", "هذا طرح. في الضرب نجمع.", "Produit : on ajoute."),
             "2x¹¹": _w("The base stays x; no coefficient appears.", "يبقى الأساس x ولا يظهر معامل.", "Pas de coefficient.")}, "ok": "x⁴·x⁷ = x¹¹"},
    {"q": "3⁻⁴ = ?", "opts": ["1/81", "−81", "−12", "81"], "a": 0,
     "why": {"−81": _w("A negative exponent means reciprocal, not a negative number.", "الأس السالب يعني المقلوب لا عددًا سالبًا.", "Exposant négatif : inverse."),
             "−12": _w("Do not multiply 3 by −4.", "لا نضرب 3 في −4.", "Ne multiplie pas."),
             "81": _w("Close: the exponent is negative, so take the reciprocal.", "قريب: الأس سالب فنأخذ المقلوب.", "Prends l'inverse.")}, "ok": "3⁻⁴ = 1/81"},
    {"q": "(−3)² and −3²: which is −9?", "opts": ["−3²", "(−3)²", "both", "neither"], "a": 0,
     "why": {"(−3)²": _w("The parentheses make −3 the base: 9.", "الأقواس تجعل −3 أساسًا: الناتج 9.", "(−3)² = 9."),
             "both": _w("They are different.", "هما مختلفان.", "Différents."),
             "neither": _w("−3² = −(3²) = −9.", "−3² = −(3²) = −9.", "−3² = −9.")}, "ok": "−3² = −9"},
]

THEORY = [
    ("Repeated multiplication", "الضرب المتكرر", "Multiplication répétée", "45", [
        T("2×2×2×2×2 is long, so we write 2⁵. The base is 2; the exponent 5 says how many times the base is used as a factor. An exponent is a shortcut for repeated multiplication.",
          "الكتابة 2×2×2×2×2 طويلة فنكتب 2⁵. الأساس 2 والأس 5 يخبرنا كم مرة نستعمل الأساس عاملًا. فالأس اختصار للضرب المتكرر.",
          "2×2×2×2×2 = 2⁵ : base 2, exposant 5."),
        F("2 × 2 × 2 × 2 × 2 = 2⁵ = 32"),
    ]),
    ("Product law", "قانون الضرب", "Produit", "45", [
        T("a³ × a² = (a·a·a)(a·a) = a⁵: five factors. For the same base, add the exponents: aᵐ · aⁿ = aᵐ⁺ⁿ. Example: x⁴ · x⁷ = x¹¹. This does not apply to 2³ × 3² because the bases differ.",
          "a³ × a² = (a·a·a)(a·a) = a⁵: خمسة عوامل. عند الأساس نفسه نجمع الأسس: aᵐ · aⁿ = aᵐ⁺ⁿ. مثال: x⁴ · x⁷ = x¹¹. ولا ينطبق هذا على 2³ × 3² لاختلاف الأساسين.",
          "Même base : on ajoute les exposants."),
        F("aᵐ · aⁿ = aᵐ⁺ⁿ      x⁴ · x⁷ = x¹¹"),
    ]),
    ("Quotient law", "قانون القسمة", "Quotient", "46", [
        T("a⁵ / a² = (a·a·a·a·a)/(a·a) = a³, cancelling two factors, only if a ≠ 0. In general aᵐ / aⁿ = aᵐ⁻ⁿ with a ≠ 0. Example: y⁹ / y⁴ = y⁵ (y ≠ 0). The restriction is part of the mathematics.",
          "a⁵ / a² = (a·a·a·a·a)/(a·a) = a³ بحذف عاملين، بشرط a ≠ 0. وعمومًا aᵐ / aⁿ = aᵐ⁻ⁿ مع a ≠ 0. مثال: y⁹ / y⁴ = y⁵ (y ≠ 0). والشرط جزء من الرياضيات لا ملاحظة جانبية.",
          "aᵐ / aⁿ = aᵐ⁻ⁿ avec a ≠ 0."),
        F("aᵐ / aⁿ = aᵐ⁻ⁿ  (a ≠ 0)      y⁹ / y⁴ = y⁵"),
    ]),
    ("Zero and negative exponents", "الأس الصفري والأس السالب", "Exposants nul et négatif", "46", [
        T("a³ / a³ = 1 and the quotient law gives a³⁻³ = a⁰, so a⁰ = 1 for a ≠ 0. a² / a⁵ = 1/a³ and the law gives a⁻³, so a⁻ⁿ = 1/aⁿ (a ≠ 0). A negative exponent is not a negative number: 3⁻⁴ = 1/3⁴ = 1/81.",
          "a³ / a³ = 1 وقانون القسمة يعطي a³⁻³ = a⁰ إذن a⁰ = 1 حين a ≠ 0. وa² / a⁵ = 1/a³ والقانون يعطي a⁻³ إذن a⁻ⁿ = 1/aⁿ (a ≠ 0). الأس السالب ليس عددًا سالبًا: 3⁻⁴ = 1/3⁴ = 1/81.",
          "a⁰ = 1 ; a⁻ⁿ = 1/aⁿ."),
        F("a⁰ = 1      a⁻ⁿ = 1 / aⁿ      3⁻⁴ = 1/81"),
    ]),
    ("Power of a power and parentheses", "قوة القوة والأقواس", "Puissance de puissance et parenthèses", "47", [
        T("(a³)² = a³ · a³ = a⁶, so (aᵐ)ⁿ = aᵐⁿ: multiply the exponents. Parentheses decide the base: (−2)⁴ = 16 but −2⁴ = −(2⁴) = −16. And (−3)² = 9 while −3² = −9.",
          "(a³)² = a³ · a³ = a⁶ إذن (aᵐ)ⁿ = aᵐⁿ: نضرب الأسس. الأقواس تحدّد الأساس: (−2)⁴ = 16 أما −2⁴ = −(2⁴) = −16. وكذلك (−3)² = 9 بينما −3² = −9.",
          "(aᵐ)ⁿ = aᵐⁿ ; (−2)⁴ = 16, −2⁴ = −16."),
        F("(a³)² = a⁶      (−2)⁴ = 16      −2⁴ = −16"),
    ]),
    ("Addition is not multiplication", "الجمع ليس ضربًا", "L'addition n'est pas la multiplication", "47", [
        T("x² + x³ = x⁵ is false. Test x = 2: 4 + 8 = 12 but 2⁵ = 32. The rule of adding exponents comes from multiplying factors; there is no such structure in addition.",
          "المساواة x² + x³ = x⁵ خاطئة. نختبر x = 2: 4 + 8 = 12 بينما 2⁵ = 32. قاعدة جمع الأسس تأتي من ضرب العوامل ولا توجد هذه البنية في الجمع.",
          "x² + x³ ≠ x⁵ : avec x = 2, 12 ≠ 32."),
        F("2² + 2³ = 12      2⁵ = 32"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Identify the operation, the base and the restrictions BEFORE choosing a rule.", "نحدّد العملية والأساس والشروط قبل اختيار القاعدة.", "Opération, base, restrictions d'abord."),
        F("a^m·a^n = a^(m+n)    a^m/a^n = a^(m−n)    a^0 = 1    a^(−n) = 1/a^n    (a^m)^n = a^(mn)"),
    ]),
]

EXERCISES = [
    EX("1", "", st("Simplify a⁵ · a².", "بسّط a⁵ · a².", "Simplifie a⁵ · a²."), [F("a⁷")]),
    EX("2", "", st("Simplify b⁸ / b³ (b ≠ 0).", "بسّط b⁸ / b³ (b ≠ 0).", "Simplifie b⁸ / b³."), [F("b⁵  (b ≠ 0)")]),
    EX("3", "", st("Rewrite z⁻² (z ≠ 0).", "أعد كتابة z⁻² (z ≠ 0).", "Réécris z⁻²."), [F("1 / z²")]),
    EX("4", "", st("Compare (−3)² and −3².", "قارن بين (−3)² و−3².", "Compare (−3)² et −3²."), [F("(−3)² = 9      −3² = −9")]),
    EX("5", "", st("Simplify (x³)⁴.", "بسّط (x³)⁴.", "Simplifie (x³)⁴."), [F("x¹²")]),
    EX("6", "", st("Simplify (a⁵ · a⁻²) / a², a ≠ 0.", "بسّط (a⁵ · a⁻²) / a² مع a ≠ 0.", "Simplifie (a⁵·a⁻²)/a²."), [T("a⁵ · a⁻² = a³, then a³ / a² = a. Check: 5 + (−2) − 2 = 1.", "a⁵ · a⁻² = a³ ثم a³ / a² = a. تحقق: 5 + (−2) − 2 = 1.", "a³ / a² = a."), F("a")]),
    EX("7", "", st("Error detective: x² + x³ = x⁵.", "المحقق: x² + x³ = x⁵.", "Détective : x² + x³ = x⁵."), [F("x = 2:  4 + 8 = 12  ≠  32")]),
]
