"""Grade 10 Mathematics — Cartesian product – Mappings (source-controlled; NABIL's own examples)."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G10-MATH-EN-011"
GRADE = 10
SUBJECT = "math"
TITLES = {"en": "Cartesian product – Mappings", "ar": "الجداء الديكارتي والتطبيقات", "fr": "Produit cartésien – Applications"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "A = {a, b}, B = {1, 2, 3}: how many pairs in A × B?", "opts": ["6", "5", "3", "2"], "a": 0,
     "why": {"5": _w("Multiply the sizes: 2 × 3.", "نضرب عدد العناصر: 2 × 3.", "Multiplie : 2 × 3."),
             "3": _w("Each of the 2 elements of A pairs with 3.", "كل عنصر من A يُقرن بـ3.", "Chaque élément de A avec 3."),
             "2": _w("Each of the 2 elements of A pairs with 3.", "كل عنصر من A يُقرن بـ3.", "Chaque élément de A avec 3.")}, "ok": "2 × 3 = 6"},
    {"q": "Rule x → 2x on {1,2,3}: the image of 3 is?", "opts": ["6", "5", "3", "9"], "a": 0,
     "why": {"5": _w("Apply the rule: 2 × 3.", "نطبّق القاعدة: 2 × 3.", "Applique : 2 × 3."),
             "3": _w("That is the source element.", "هذا هو العنصر الأصلي.", "C'est l'antécédent."),
             "9": _w("The rule doubles, not triples.", "القاعدة تضاعف لا تثلّث.", "Double, pas triple.")}, "ok": "2 × 3 = 6"},
    {"q": "Is (2,5) = (5,2)?", "opts": ["No", "Yes", "Sometimes always", "Only for sets"], "a": 0,
     "why": {"Yes": _w("Order matters: compare place by place.", "الترتيب مهم: نقارن مكانًا مكانًا.", "L'ordre compte."),
             "Sometimes always": _w("They are not equal.", "ليسا متساويين.", "Pas égaux."),
             "Only for sets": _w("These are ordered pairs, not sets.", "هذان زوجان مرتبان لا مجموعتان.", "Couples, pas ensembles.")}, "ok": "No"},
]

THEORY = [
    ("Ordered pairs", "الأزواج المرتبة", "Les couples", "113", [
        T("Hello! Imagine two boxes: A = {red, blue} and B = {1, 2}. We want every choice made of one element from A first and one from B second. The pair (red, 1) says: the first component comes from A, the second from B. We cannot turn it into (1, red). Two ordered pairs are equal only if the first components match and the second components match: (2, 5) ≠ (5, 2).",
          "مرحبًا! تخيّل صندوقين: A = {red, blue} وB = {1, 2}. نريد كل اختيار يؤخذ عنصره الأول من A والثاني من B. الزوج (red, 1) يقول: المركّبة الأولى من A والثانية من B. ولا نستطيع قلبه إلى (1, red). والزوجان المرتبان يتساويان فقط إذا تطابقت المركّبتان الأولى والثانية: (2, 5) ≠ (5, 2).",
          "Un couple (a, b) : l'ordre compte. (2,5) ≠ (5,2)."),
        F("(2, 5) ≠ (5, 2)"),
    ]),
    ("The Cartesian product A × B", "الجداء الديكارتي A × B", "Le produit cartésien", "113", [
        T("A × B is the set of all ordered pairs (a, b) with a in A and b in B. For A = {a, b} and B = {1, 2, 3}: fix a, pair it with each element of B: (a,1), (a,2), (a,3); then fix b: (b,1), (b,2), (b,3). We expect 2 × 3 = 6 pairs: a good check that none was forgotten. A × B and B × A are different in general, because the first component comes from a different set.",
          "A × B هي مجموعة كل الأزواج المرتبة (a, b) حيث a من A وb من B. إذا كانت A = {a, b} وB = {1, 2, 3} فنثبّت a ونقرنه بكل عنصر من B: (a,1) و(a,2) و(a,3)، ثم نثبّت b: (b,1) و(b,2) و(b,3). نتوقع 2 × 3 = 6 أزواج: تحقق جيد أننا لم ننسَ زوجًا. وA × B تختلف عن B × A عمومًا لأن المركّبة الأولى تأتي من مجموعة مختلفة.",
          "A×B : 2 × 3 = 6 couples."),
        F("2 × 3 = 6"),
        F("A × B = {(a,1), (a,2), (a,3), (b,1), (b,2), (b,3)}"),
    ]),
    ("Reading a pair", "قراءة الزوج", "Lire un couple", "113", [
        T("(x, y) ∈ A × B means x ∈ A and y ∈ B. With A = {1, 2} and B = {p, q}: A × B = {(1,p), (1,q), (2,p), (2,q)}. The pair (p, 1) is not in A × B, because p is not in A. It could belong to B × A, but that is another question.",
          "(x, y) ∈ A × B تعني x ∈ A وy ∈ B. مع A = {1, 2} وB = {p, q}: A × B = {(1,p), (1,q), (2,p), (2,q)}. الزوج (p, 1) ليس في A × B لأن p ليس في A. وقد يكون في B × A لكن هذا سؤال آخر.",
          "(x,y) ∈ A×B ⇔ x ∈ A et y ∈ B."),
        F("2 × 2 = 4 pairs"),
    ]),
    ("A mapping: source, target, rule", "التطبيق: المصدر والهدف والقاعدة", "Application : source, but, règle", "114", [
        T("A mapping associates elements of a source set to elements of a target set by a stated rule. Before following arrows ask: what is the source? the target? the rule? Example: source {1, 2, 3}, target {2, 4, 6}, rule x → 2x. So 1 → 2, 2 → 4, 3 → 6. An arrow 2 → 6 is rejected because the rule gives 2 × 2 = 4. The rule is the judge, not the picture.",
          "التطبيق يقرن عناصر مجموعة المصدر بعناصر مجموعة الهدف بقاعدة معلنة. قبل أن نتبع الأسهم نسأل: ما المصدر؟ وما الهدف؟ وما القاعدة؟ مثال: المصدر {1, 2, 3} والهدف {2, 4, 6} والقاعدة x → 2x. إذن 1 → 2 و2 → 4 و3 → 6. والسهم 2 → 6 مرفوض لأن القاعدة تعطي 2 × 2 = 4. القاعدة هي الحكم لا الرسم.",
          "Source, but, règle : x → 2x."),
        F("1 → 2      2 → 4      3 → 6"),
    ]),
    ("Image and preimage", "الصورة والسابقة", "Image et antécédent", "114", [
        T("The image of 3 under x → 2x: apply the rule forward, 2 × 3 = 6. A preimage of 4: find x in the source with 2x = 4, so x = 2; check forward: 2 → 4. With source {0, 1, 2}, target {1, 3, 5}, rule x → 2x + 1: 0 → 1, 1 → 3, 2 → 5, giving the pairs (0,1), (1,3), (2,5).",
          "صورة 3 بالقاعدة x → 2x: نطبّق القاعدة 2 × 3 = 6. وسابقة 4: نبحث عن x في المصدر حيث 2x = 4 فيكون x = 2 ونتحقق: 2 → 4. ومع المصدر {0, 1, 2} والهدف {1, 3, 5} والقاعدة x → 2x + 1: 0 → 1 و1 → 3 و2 → 5 فنحصل على الأزواج (0,1) و(1,3) و(2,5).",
          "Image : appliquer la règle ; antécédent : résoudre."),
        F("2 × 3 = 6      2 × 2 = 4"),
        F("(0,1), (1,3), (2,5)"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Identify the roles and the order BEFORE following arrows. The same mapping can be a rule, an arrow diagram, or a set of ordered pairs.",
          "نحدّد الأدوار والترتيب قبل أن نتبع الأسهم. والتطبيق نفسه يُعرض بقاعدة أو بمخطط أسهم أو بمجموعة أزواج مرتبة.",
          "Rôles et ordre d'abord."),
        F("(a, b)  ·  A × B  ·  source + target + rule"),
    ]),
]

EXERCISES = [
    EX("1", "", st("A = {1, 2}, B = {p, q}: build A × B.", "A = {1, 2} وB = {p, q}: كوّن A × B.", "Construis A × B."), [F("{(1,p), (1,q), (2,p), (2,q)}      2 × 2 = 4")]),
    EX("2", "", st("Is (p, 1) in A × B above?", "هل (p, 1) في A × B أعلاه؟", "(p, 1) est-il dans A × B ?"), [T("No: p is not in A.", "لا: p ليس في A.", "Non : p n'est pas dans A.")]),
    EX("3", "", st("Is (a, b) = (a, c)?", "هل (a, b) = (a, c)؟", "(a, b) = (a, c) ?"), [T("Only if b = c.", "فقط إذا كان b = c.", "Seulement si b = c.")]),
    EX("4", "", st("Source {0, 1, 2}, target {1, 3, 5}, rule x → 2x + 1: list the pairs.", "المصدر {0, 1, 2} والهدف {1, 3, 5} والقاعدة x → 2x + 1: اكتب الأزواج.", "Liste les couples."), [F("(0,1), (1,3), (2,5)")]),
    EX("5", "", st("Error detective: A × B written with elements of B first.", "المحقق: كُتبت A × B وعناصر B أولًا.", "Détective : A × B avec B en premier."), [T("The first component must come from A: fix an element of A, then go through B.", "المركّبة الأولى يجب أن تكون من A: نثبّت عنصرًا من A ثم نمرّ على B.", "La première composante vient de A.")]),
    EX("6", "", st("Source {1, 2, 3}, rule x → 2x: image of 3 and a preimage of 4.", "المصدر {1, 2, 3} والقاعدة x → 2x: صورة 3 وسابقة 4.", "Image de 3 et antécédent de 4."), [F("2 × 3 = 6      2x = 4  ⇒  x = 2      2 → 4")]),
]
