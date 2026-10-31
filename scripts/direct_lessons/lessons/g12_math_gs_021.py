"""Grade 12 (GS) Mathematics — Conditional probability (source: Building up Mathematics S3 GS, ch. 23)."""
import math
from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.draw import geo

LESSON_ID = "G12-MATH-GS-021"
GRADE = 12
SUBJECT = "math"
TITLES = {"en": "Conditional probability", "ar": "الاحتمال الشرطي", "fr": "Probabilité conditionnelle"}

INK = "#0b3d5c"; RED = "#e53935"; BLUE = "#1e88e5"; GREEN = "#2e7d32"; ORG = "#fb8c00"; PUR = "#8e24aa"


def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}


def _ell(cx, cy, rx, ry, fill, stroke, w=4):
    return ("raw", f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{w}"/>')


def _rect(x, y, w, h, fill, stroke, sw=4):
    return ("raw", f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')


def d_die():
    cells = []
    for i in range(6):
        x = 60 + i * 90
        cells.append(_rect(x, 150, 70, 70, "#fff", INK, 3))
        cells.append(("text", (x + 35, 197), str(i + 1), 34, INK))
    A = [("raw", f'<rect x="{60+i*90-6}" y="144" width="82" height="82" rx="8" fill="none" stroke="{GREEN}" stroke-width="5"/>') for i in (1, 3, 5)]
    B = [("raw", f'<rect x="{60+i*90-11}" y="139" width="92" height="92" rx="10" fill="none" stroke="{BLUE}" stroke-width="4" stroke-dasharray="8 5"/>') for i in (3, 4, 5)]
    both = [_rect(60 + i * 90, 150, 70, 70, "rgba(255,225,77,.55)", ORG, 4) for i in (3, 5)] + \
           [("text", (60 + i * 90 + 35, 197), str(i + 1), 34, INK) for i in (3, 5)]
    return geo([cells, [("text", (330, 110), "Ω = {1, 2, 3, 4, 5, 6}", 28, INK)], A + [("text", (330, 275), "A = even = {2, 4, 6}", 26, GREEN)],
                B + [("text", (330, 320), "B = more than 3 = {4, 5, 6}", 26, BLUE)], both + [("text", (330, 375), "A ∩ B = {4, 6}", 28, ORG)]], "DI")


def d_venn(stage=5):
    P = _ell(250, 230, 130, 120, "rgba(30,136,229,.12)", BLUE); C = _ell(410, 230, 130, 120, "rgba(46,125,50,.12)", GREEN)
    nums = [("text", (190, 240), "12", 34, INK), ("text", (330, 240), "12", 36, ORG), ("text", (470, 240), "6", 34, INK), ("text", (570, 340), "10 neither", 24, INK)]
    lab = [("text", (170, 98), "Physics: 24", 26, BLUE), ("text", (490, 98), "Chemistry: 18", 26, GREEN)]
    hl = _ell(250, 230, 130, 120, "rgba(251,192,45,.30)", ORG, 6)
    groups = [[_rect(30, 60, 600, 360, "none", INK, 4), ("text", (580, 395), "Ω = 40", 26, INK)], [P] + [lab[0]], [C] + [lab[1]], nums,
              [hl, ("text", (330, 412), "knowing Physics: the new universe = 24 students", 22, ORG)]]
    return geo(groups[:stage], "VE")


def tree(first, second, hi=None, tag="TR", roots="", prods=None):
    """first = [(label, prob)], second = [[(label, prob), ...] per first branch]"""
    R = (50, 220); g1 = []; g2 = []; g3 = []
    ys1 = [110, 330] if len(first) == 2 else [70, 220, 370]
    k = 0
    for i, (lab, pr) in enumerate(first):
        n1 = (240, ys1[i]); g1 += [("seg", R, n1, INK, 4, None), ("pt", n1, "", 0, 0, INK),
                                   ("text", ((R[0] + n1[0]) / 2 - 8, (R[1] + n1[1]) / 2 + (-14 if ys1[i] < 220 else 24)), pr, 22, BLUE),
                                   ("text", (n1[0] + 6, n1[1] - 14), lab, 26, INK)]
        m = len(second[i]); span = 120 if len(first) == 2 else 80
        for j, (l2, p2) in enumerate(second[i]):
            y2 = ys1[i] + (-34 if j == 0 else 34) if len(first) == 3 else ys1[i] + (-52 if j == 0 else 52)
            n2 = (470, y2); col = RED if hi == (i, j) else INK
            g2 += [("seg", n1, n2, col, 5 if hi == (i, j) else 3, None), ("pt", n2, "", 0, 0, col),
                   ("text", ((n1[0] + n2[0]) / 2, (n1[1] + n2[1]) / 2 - 10), p2, 20, BLUE), ("text", (n2[0] + 46, n2[1] + 8), l2, 24, INK)]
            if prods:
                g3.append(("text", (n2[0] + 140, n2[1] + 8), prods[k], 20, RED if hi == (i, j) else GREEN)); k += 1
    groups = [g1, g2] + ([g3] if prods else [])
    return geo(groups, tag)


def d_excl():
    return geo([[_ell(210, 220, 110, 100, "rgba(30,136,229,.15)", BLUE), _ell(450, 220, 110, 100, "rgba(46,125,50,.15)", GREEN), ("text", (210, 228), "A", 40, BLUE), ("text", (450, 228), "B", 40, GREEN)],
                [("text", (330, 360), "A ∩ B = ∅   →   P(A ∩ B) = 0", 28, RED), ("text", (330, 405), "but P(A) · P(B) > 0", 26, INK)]], "EX")


def d_bayes():
    # prior 2% -> posterior bars
    bars = [("raw", f'<rect x="120" y="{380-400*0.02:.0f}" width="120" height="{400*0.02:.0f}" fill="{BLUE}"/>'), ("text", (180, 365), "2%", 28, INK), ("text", (180, 415), "before the test", 22, INK),
            ]
    post = [("raw", f'<rect x="420" y="{380-400*0.393:.0f}" width="120" height="{400*0.393:.0f}" fill="{RED}"/>'), ("text", (480, 380 - 400 * 0.393 - 12), "39.3%", 28, RED), ("text", (480, 415), "after a positive test", 22, INK)]
    return geo([[("seg", (60, 380), (620, 380), INK, 3, None)] + bars, post, [("text", (330, 150), "the evidence re-weights the prior", 26, ORG)]], "BA")


# ---------------------------------------------------------------- quiz
QUIZ = [
    {"q": "A fair die is rolled. What is P(B | A) if A = {even} and B = {more than 3}?", "opts": ["2/3", "1/2", "1/3", "1/6"], "a": 0,
     "why": {"1/2": _w("A has 3 outcomes, not 6.", "A فيها 3 نتائج لا 6.", "A a 3 issues."),
             "1/3": _w("Divide by P(A) = 3/6, not by P(B).", "نقسم على P(A) لا على P(B).", "On divise par P(A)."),
             "1/6": _w("That is P(A ∩ B) over everything: 2/6 = 1/3.", "هذا ليس الاحتمال الشرطي.", "Pas conditionnelle.")}, "ok": "2/3"},
    {"q": "Two events with non-zero probabilities are mutually exclusive. Are they independent?", "opts": ["No — they are dependent", "Yes, always", "Only if P(A) = P(B)", "Only on a die"], "a": 0,
     "why": {"Yes, always": _w("Their intersection has probability 0, but P(A)P(B) > 0.", "تقاطعهما احتماله 0 لكن P(A)P(B) > 0.", "Intersection nulle."),
             "Only if P(A) = P(B)": _w("The product is still not 0.", "الجداء لا يساوي 0.", "Produit non nul."),
             "Only on a die": _w("The rule is general.", "القاعدة عامة.", "Règle générale.")}, "ok": "No — they are dependent"},
    {"q": "Along a probability tree we …", "opts": ["multiply along a path and add across paths", "add along a path and multiply across paths", "always multiply", "always add"], "a": 0,
     "why": {"add along a path and multiply across paths": _w("It is the opposite.", "العكس هو الصحيح.", "C'est l'inverse."),
             "always multiply": _w("Different paths to the same event are added.", "المسارات المختلفة تُجمع.", "On additionne."),
             "always add": _w("A path is an intersection: multiply.", "المسار تقاطع فنضرب.", "Intersection : produit.")}, "ok": "multiply along a path and add across paths"},
]

# ---------------------------------------------------------------- theory
THEORY = [
    ("Big question: how does knowing something change the sample space?", "السؤال الكبير: كيف تغيّر المعلومة فضاء العيّنة؟", "Grande question : comment une information change l'univers", "221", [
        T("Hello, champion! Roll a fair die. The sample space is the six outcomes 1 to 6. Let A be the event 'the number is even' and B the event 'the number is more than 3'. Here are the six outcomes and the two events.",
          "مرحبًا يا بطل! نرمي حجر نرد عادلًا. فضاء العيّنة هو النتائج الست من 1 إلى 6. ليكن A حدث «العدد زوجي» وB حدث «العدد أكبر من 3». هذه النتائج الست والحدثان.",
          "On lance un dé équilibré : six issues, A = pair, B = plus grand que 3."),
        d_die(),
        T("Now somebody tells you: the number is even. Only the outcomes 2, 4 and 6 are still possible. The sample space has shrunk from six outcomes to three. This is the heart of conditional probability.",
          "الآن قال لك أحدهم: العدد زوجي. لم يبقَ ممكنًا إلا 2 و4 و6. تقلّص فضاء العيّنة من ست نتائج إلى ثلاث. وهذه هي فكرة الاحتمال الشرطي.",
          "Si l'on sait que le nombre est pair, l'univers se réduit à trois issues."),
        T("Inside this new universe, how many outcomes are also more than 3? Only 4 and 6, that is two outcomes out of three. So the probability of B knowing A is two thirds.",
          "داخل هذا الفضاء الجديد كم نتيجة أكبر من 3 أيضًا؟ فقط 4 و6 أي نتيجتان من ثلاث. إذن احتمال B علمًا أن A وقع يساوي الثلثين.",
          "Parmi ces trois issues, deux sont plus grandes que 3 : 2/3."),
        F("P(B | A) = 2 / 3"),
    ]),
    ("Definition of conditional probability", "تعريف الاحتمال الشرطي", "Définition", "221", [
        T("Let A be an event with non-zero probability. The probability of B knowing that A has occurred is the probability of the intersection of A and B divided by the probability of A. We divide by the probability of the event we know, never of the other one.",
          "ليكن A حدثًا احتماله لا يساوي صفرًا. احتمال B علمًا أن A وقع يساوي احتمال تقاطع A وB مقسومًا على احتمال A. نقسم دائمًا على احتمال الحدث المعلوم لا على الآخر.",
          "P(B|A) = P(A∩B) / P(A), avec P(A) non nul."),
        F("P(B | A) = P(A ∩ B) / P(A)      P(A) > 0"),
        T("Check with the die. The intersection of A and B is the two outcomes 4 and 6, so its probability is two sixths. The probability of A is three sixths. Dividing, two sixths over three sixths gives two thirds, the same answer as before.",
          "نتحقق بالنرد. تقاطع A وB هو النتيجتان 4 و6 فاحتماله ستّان. واحتمال A ثلاثة أسداس. بالقسمة: (2/6) ÷ (3/6) = 2/3 وهي النتيجة نفسها.",
          "On retrouve (2/6) / (3/6) = 2/3."),
        F("P(B | A) = (2 / 6) / (3 / 6) = 2 / 3"),
    ]),
    ("A picture: students who study Physics and Chemistry", "صورة: طلاب الفيزياء والكيمياء", "Une figure : élèves de physique et de chimie", "221", [
        T("A class has 40 students. 24 study Physics, 18 study Chemistry and 12 study both. We draw the whole class as a rectangle and each subject as a circle. The overlap holds the 12 who study both.",
          "في صف 40 طالبًا: 24 يدرسون الفيزياء و18 الكيمياء و12 يدرسون الاثنين. نرسم الصف كله مستطيلًا وكل مادة دائرة، وفي منطقة التقاطع الـ 12 الذين يدرسون الاثنين.",
          "Classe de 40 : 24 en physique, 18 en chimie, 12 les deux."),
        d_venn(4),
        T("We pick a student who studies Physics. Now only the Physics circle matters: it becomes the new universe with 24 students. Among them 12 also study Chemistry.",
          "نختار طالبًا من الذين يدرسون الفيزياء. فتصبح دائرة الفيزياء وحدها هي الفضاء الجديد وفيها 24 طالبًا، منهم 12 يدرسون الكيمياء أيضًا.",
          "On choisit un élève de physique : l'univers est de 24 élèves."),
        d_venn(5),
        F("P(C | P) = 12 / 24 = 1 / 2"),
        T("The denominator changed from 40 to 24 because the condition changed the reference group. Be careful: the probability of Physics given Chemistry is not the same; it is twelve over eighteen, two thirds.",
          "تغيّر المقام من 40 إلى 24 لأن الشرط غيّر المجموعة المرجعية. وانتبه: احتمال الفيزياء علمًا بالكيمياء ليس نفسه، بل 12 على 18 أي الثلثان.",
          "P(P|C) = 12/18 = 2/3, différent de P(C|P)."),
        F("P(P | C) = 12 / 18 = 2 / 3"),
    ]),
    ("Multiplication rule", "قاعدة الضرب", "Règle du produit", "222", [
        T("From the definition we obtain the multiplication rule: the probability that A and B both occur equals the probability of A times the probability of B knowing A. It also equals the probability of B times the probability of A knowing B.",
          "من التعريف نحصل على قاعدة الضرب: احتمال وقوع A وB معًا يساوي احتمال A مضروبًا في احتمال B علمًا بوقوع A. ويساوي أيضًا احتمال B مضروبًا في احتمال A علمًا بوقوع B.",
          "P(A∩B) = P(A) P(B|A) = P(B) P(A|B)."),
        F("P(A ∩ B) = P(A) · P(B | A) = P(B) · P(A | B)"),
        T("Example. An urn holds 3 red and 5 white balls. We draw two balls without replacement. The first ball is red with probability three eighths. Then 7 balls remain, 5 of them white, so the second is white with probability five sevenths.",
          "مثال. صندوق فيه 3 كرات حمراء و5 بيضاء. نسحب كرتين دون إرجاع. الأولى حمراء باحتمال ثلاثة أثمان. بعدها يبقى 7 كرات منها 5 بيضاء فتكون الثانية بيضاء باحتمال خمسة أسباع.",
          "Urne : 3 rouges, 5 blanches, tirage sans remise."),
        tree([("R", "3/8"), ("W", "5/8")], [[("R", "2/7"), ("W", "5/7")], [("R", "3/7"), ("W", "4/7")]], hi=(0, 1), tag="UR"),
        F("P(R then W) = 3 / 8 · 5 / 7 = 15 / 56"),
    ]),
    ("Independent events", "الأحداث المستقلة", "Événements indépendants", "223", [
        T("Two events are independent when knowing that one occurred does not change the probability of the other. In symbols, the probability of B knowing A equals the probability of B. Equivalently, the probability of the intersection equals the product of the probabilities.",
          "يكون الحدثان مستقلين إذا كان العلم بوقوع أحدهما لا يغيّر احتمال الآخر. أي أن احتمال B علمًا بـ A يساوي احتمال B. ويكافئ ذلك أن احتمال التقاطع يساوي جداء الاحتمالين.",
          "A et B indépendants : P(B|A) = P(B), donc P(A∩B) = P(A)P(B)."),
        F("P(B | A) = P(B)      ⇔      P(A ∩ B) = P(A) · P(B)"),
        T("Test it with data: if the probability of A is 0.5, of B is 0.4 and of the intersection is 0.2, then the product is 0.5 times 0.4 equals 0.2. The events are independent. If the intersection were 0.3, they would be dependent.",
          "نختبر بالأرقام: إذا كان احتمال A يساوي 0.5 واحتمال B يساوي 0.4 واحتمال التقاطع 0.2 فإن الجداء 0.5 × 0.4 = 0.2 فالحدثان مستقلان. ولو كان التقاطع 0.3 لكانا غير مستقلين.",
          "0,5 × 0,4 = 0,2 : indépendants."),
        F("0.5 · 0.4 = 0.2 = P(A ∩ B)   ⇒   independent"),
    ]),
    ("Error trap: exclusive is not independent", "فخ الخطأ: التنافي ليس استقلالًا", "Piège : incompatibles ≠ indépendants", "223", [
        T("Mutually exclusive means the two events cannot happen together, so the intersection is empty and has probability zero. If both probabilities are non-zero, their product is not zero. So the events cannot be independent. In fact, if A happens we are sure that B does not.",
          "التنافي يعني أن الحدثين لا يقعان معًا فالتقاطع خالٍ واحتماله صفر. وإذا كان احتمالاهما غير صفرين فجداؤهما لا يساوي صفرًا. إذن لا يمكن أن يكونا مستقلين، فوقوع A يؤكد عدم وقوع B.",
          "Incompatibles et non nuls : dépendants."),
        d_excl(),
        F("exclusive and non-zero   ⇒   NOT independent"),
    ]),
    ("Total probability", "قانون الاحتمال الكلي", "Probabilités totales", "224", [
        T("Suppose the events A one to A n form a partition of the universe: they do not overlap and together they fill everything. Then the probability of any event B is the sum, over the parts, of the probability of the part times the probability of B knowing that part.",
          "لتكن الأحداث A1 إلى An تجزئة لفضاء العيّنة: لا تتقاطع وتملأ الفضاء كله. عندئذٍ احتمال أي حدث B يساوي مجموع، على كل الأجزاء، احتمال الجزء مضروبًا في احتمال B علمًا بذلك الجزء.",
          "Partition A1…An : P(B) = Σ P(Ai) P(B|Ai)."),
        F("P(B) = P(A₁) · P(B | A₁) + P(A₂) · P(B | A₂) + … + P(Aₙ) · P(B | Aₙ)"),
        T("Example. Machine A makes 40 percent of the items, with 1 percent defective. Machine B makes 60 percent, with 2.5 percent defective. We draw a tree and multiply along each path that ends in a defective item.",
          "مثال. الآلة A تنتج 40% من القطع وفيها 1% معيب. والآلة B تنتج 60% وفيها 2.5% معيب. نرسم شجرة ونضرب على كل مسار ينتهي بقطعة معيبة.",
          "Machine A : 40 %, 1 % défectueux ; B : 60 %, 2,5 %."),
        tree([("A", "0.4"), ("B", "0.6")], [[("D", "0.01"), ("OK", "0.99")], [("D", "0.025"), ("OK", "0.975")]], prods=["0.004", "", "0.015", ""], tag="MA"),
        T("Add the two paths that end in a defective item: 0.004 plus 0.015.",
          "نجمع المسارين اللذين ينتهيان بقطعة معيبة: 0.004 زائد 0.015.",
          "On additionne les deux chemins."),
        F("P(D) = 0.4 · 0.01 + 0.6 · 0.025 = 0.019"),
        T("Check: the branches that leave one node must add up to one. 0.4 plus 0.6 is one, and 0.01 plus 0.99 is one.",
          "تحقق: الفروع الخارجة من عقدة واحدة مجموعها يجب أن يساوي 1. 0.4 + 0.6 = 1 و0.01 + 0.99 = 1.",
          "Vérification : la somme des branches vaut 1."),
    ]),
    ("Reversing the condition: Bayes", "عكس الشرط: بايز", "Inverser la condition : Bayes", "225", [
        T("We found a defective item. What is the probability it came from machine A? We reverse the conditioning: it is the probability of the path A then defective, divided by the total probability of a defective item.",
          "وجدنا قطعة معيبة. ما احتمال أنها من الآلة A؟ نعكس الشرط: هو احتمال المسار A ثم معيب مقسومًا على الاحتمال الكلي للقطعة المعيبة.",
          "Une pièce défectueuse : quelle probabilité qu'elle vienne de A ?"),
        F("P(A | D) = P(A ∩ D) / P(D) = 0.004 / 0.019 = 4 / 19 ≈ 0.21"),
        T("Look at the change: before the evidence machine A had 40 percent. After finding a defective item it drops to about 21 percent, because machine A is the more reliable machine. The evidence re-weighted the causes.",
          "لاحظ التغيّر: قبل الدليل كان للآلة A نسبة 40%. وبعد العثور على قطعة معيبة صارت نحو 21% لأن الآلة A أكثر دقة. فالدليل أعاد توزيع الأوزان على الأسباب.",
          "L'information a modifié la probabilité de 40 % à 21 %."),
    ]),
    ("Error detective", "المحقق", "Détective", "", [
        T("Four mistakes to avoid. One: swapping P of B given A with P of A given B. Two: treating draws without replacement as independent. Three: confusing exclusive with independent. Four: adding along a path when the intersection needs a product.",
          "أربعة أخطاء يجب تجنّبها. الأول: تبديل P(B|A) بـ P(A|B). الثاني: اعتبار السحب دون إرجاع مستقلًّا. الثالث: الخلط بين التنافي والاستقلال. الرابع: الجمع على طول المسار بدل الضرب.",
          "Quatre erreurs à éviter."),
        F("P(A | B) ≠ P(B | A)      path → multiply      paths → add"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "226", [
        T("Conditioning changes the reference sample space. Intersections multiply along conditional branches. Independence means no change in probability after conditioning. Total probability adds all the paths that lead to an event. The habit: define the events, condition on the right one, multiply paths, add alternative paths, check the totals.",
          "الشرط يغيّر فضاء العيّنة المرجعي. التقاطعات تُضرب على الفروع الشرطية. الاستقلال يعني أن الاحتمال لا يتغيّر بعد الشرط. والاحتمال الكلي يجمع كل المسارات المؤدية إلى الحدث. والعادة: نعرّف الأحداث وننطلق من الحدث الصحيح ونضرب على المسار ونجمع المسارات البديلة ونتحقق من المجاميع.",
          "Définir, conditionner, multiplier, additionner, vérifier."),
        F("P(B | A) = P(A ∩ B) / P(A)      P(B) = Σ P(Aᵢ) · P(B | Aᵢ)"),
    ]),
]


def _ex(n, en, ar, fr, steps):
    return EX(n, "", st(en, ar, fr), steps)


EXERCISES = [
    _ex("1", "A fair die is rolled. A = {even}, B = {more than 4}. Find P(A | B) and P(B | A).",
        "نرمي حجر نرد عادلًا. A = {زوجي} وB = {أكبر من 4}. جد P(A|B) وP(B|A).", "Dé équilibré : A pair, B > 4. P(A|B), P(B|A) ?",
        [T("B = {5, 6} and A = {2, 4, 6}. The intersection is {6}, with probability 1/6. P(A | B) = (1/6) / (2/6) = 1/2. P(B | A) = (1/6) / (3/6) = 1/3. The two are different.",
           "B = {5, 6} وA = {2, 4, 6} والتقاطع {6} احتماله 1/6. P(A|B) = (1/6) ÷ (2/6) = 1/2 وP(B|A) = (1/6) ÷ (3/6) = 1/3. والنتيجتان مختلفتان.", "1/2 et 1/3."),
         F("P(A | B) = 1 / 2      P(B | A) = 1 / 3")]),
    _ex("2", "In a class of 40, 24 study Physics, 18 Chemistry and 12 both. A student is chosen at random. Find the probability of Physics knowing Chemistry, and of neither subject.",
        "في صف 40 طالبًا: 24 فيزياء و18 كيمياء و12 الاثنتان. نختار طالبًا. جد احتمال الفيزياء علمًا بالكيمياء، واحتمال ألّا يدرس أيًّا منهما.", "Classe de 40. P(P|C) et P(aucune matière) ?",
        [T("Chemistry has 18 students and 12 of them study Physics: P(P | C) = 12/18 = 2/3. Students in at least one subject: 24 + 18 − 12 = 30, so 10 study neither: 10/40 = 1/4.",
           "الكيمياء فيها 18 طالبًا منهم 12 يدرسون الفيزياء: P(P|C) = 12/18 = 2/3. من يدرس مادة واحدة على الأقل: 24 + 18 − 12 = 30 فيبقى 10 لا يدرسون أيًّا منهما: 10/40 = 1/4.", "2/3 et 1/4."),
         d_venn(4), F("P(P | C) = 2 / 3      P(neither) = 10 / 40 = 1 / 4")]),
    _ex("3", "An urn holds 3 red and 5 white balls. Two balls are drawn without replacement. Find the probability of two reds, of two whites, and check that the four cases add up to 1.",
        "صندوق فيه 3 كرات حمراء و5 بيضاء. نسحب كرتين دون إرجاع. جد احتمال كرتين حمراوين وكرتين بيضاوين، وتحقق أن الحالات الأربع مجموعها 1.", "Urne 3R 5B sans remise : RR, BB, somme = 1 ?",
        [T("RR: 3/8 · 2/7 = 6/56. WW: 5/8 · 4/7 = 20/56. RW: 15/56. WR: 5/8 · 3/7 = 15/56. The sum is (6 + 20 + 15 + 15) / 56 = 56/56 = 1.",
           "RR: 3/8 · 2/7 = 6/56. WW: 5/8 · 4/7 = 20/56. RW: 15/56. WR: 5/8 · 3/7 = 15/56. المجموع (6 + 20 + 15 + 15) / 56 = 56/56 = 1.", "Total 1."),
         tree([("R", "3/8"), ("W", "5/8")], [[("R", "2/7"), ("W", "5/7")], [("R", "3/7"), ("W", "4/7")]], tag="U3", prods=["6/56", "15/56", "15/56", "20/56"]),
         F("6/56 + 15/56 + 15/56 + 20/56 = 1")]),
    _ex("4", "Same urn but the ball is put back after each draw. Find the probability of two reds. Are the two draws independent?",
        "الصندوق نفسه لكن نُعيد الكرة بعد كل سحب. جد احتمال كرتين حمراوين. هل السحبان مستقلان؟", "Avec remise : RR ? indépendants ?",
        [T("With replacement the second draw is not affected by the first: P(R) = 3/8 each time, so P(RR) = 3/8 · 3/8 = 9/64. The draws are independent, unlike the case without replacement where the second probability changed to 2/7.",
           "مع الإرجاع لا يتأثر السحب الثاني بالأول: P(R) = 3/8 في كل مرة فيكون P(RR) = 3/8 · 3/8 = 9/64. السحبان مستقلان بعكس حالة عدم الإرجاع حيث تغيّر الاحتمال الثاني إلى 2/7.", "9/64, indépendants."),
         F("P(RR) = 3 / 8 · 3 / 8 = 9 / 64")]),
    _ex("5", "P(A) = 0.5, P(B) = 0.4 and P(A ∩ B) = 0.2. Are A and B independent? What if P(A ∩ B) = 0.3?",
        "P(A) = 0.5 وP(B) = 0.4 وP(A∩B) = 0.2. هل A وB مستقلان؟ وماذا لو كان P(A∩B) = 0.3؟", "Indépendance pour 0,2 puis 0,3 ?",
        [T("The product is 0.5 · 0.4 = 0.2. With 0.2 the events are independent. With 0.3, the intersection is not equal to the product, so the events are dependent.",
           "الجداء 0.5 · 0.4 = 0.2. مع 0.2 الحدثان مستقلان. ومع 0.3 لا يساوي التقاطع الجداء فالحدثان غير مستقلين.", "Oui puis non."),
         F("0.2 = 0.5 · 0.4   independent      0.3 ≠ 0.2   dependent")]),
    _ex("6", "P(A) = 0.3, P(B) = 0.5 and A, B are mutually exclusive. Are they independent?",
        "P(A) = 0.3 وP(B) = 0.5 وA وB متنافيان. هل هما مستقلان؟", "Incompatibles : indépendants ?",
        [T("P(A ∩ B) = 0 but P(A) · P(B) = 0.15. They are different, so the events are not independent.",
           "P(A∩B) = 0 بينما P(A) · P(B) = 0.15. هما مختلفان فالحدثان غير مستقلين.", "Non."), d_excl(), F("0 ≠ 0.3 · 0.5 = 0.15")]),
    _ex("7", "Machine A makes 40% of the items (1% defective); machine B makes 60% (2.5% defective). Find the probability that an item is defective.",
        "الآلة A تنتج 40% من القطع (1% معيب) والآلة B تنتج 60% (2.5% معيب). جد احتمال أن تكون قطعة معيبة.", "P(D) pour les deux machines ?",
        [T("Total probability: 0.4 · 0.01 + 0.6 · 0.025 = 0.004 + 0.015 = 0.019.",
           "الاحتمال الكلي: 0.4 · 0.01 + 0.6 · 0.025 = 0.004 + 0.015 = 0.019.", "0,019."),
         tree([("A", "0.4"), ("B", "0.6")], [[("D", "0.01"), ("OK", "0.99")], [("D", "0.025"), ("OK", "0.975")]], prods=["0.004", "", "0.015", ""], tag="E7"), F("P(D) = 0.019")]),
    _ex("8", "An item is found defective. What is the probability that it came from machine B?",
        "وُجدت قطعة معيبة. ما احتمال أنها من الآلة B؟", "Défectueuse : provient de B ?",
        [T("P(B | D) = P(B ∩ D) / P(D) = 0.015 / 0.019 = 15/19 ≈ 0.79. Check: P(A | D) + P(B | D) = 4/19 + 15/19 = 1.",
           "P(B|D) = P(B∩D) ÷ P(D) = 0.015 ÷ 0.019 = 15/19 ≈ 0.79. تحقق: P(A|D) + P(B|D) = 4/19 + 15/19 = 1.", "15/19."), F("P(B | D) = 0.015 / 0.019 = 15 / 19 ≈ 0.79")]),
    _ex("9", "A disease affects 2% of a population. A test is positive for 95% of the sick and for 3% of the healthy. A person tests positive. Find the probability that the person is sick.",
        "مرض يصيب 2% من السكان. الفحص إيجابي عند 95% من المرضى وعند 3% من الأصحاء. فحص شخص فكان إيجابيًا. جد احتمال أن يكون مريضًا.", "Maladie 2 %, test + : P(malade | +) ?",
        [T("Total probability of a positive test: 0.02 · 0.95 + 0.98 · 0.03 = 0.019 + 0.0294 = 0.0484. Then P(sick | +) = 0.019 / 0.0484 ≈ 0.39. A positive test raises the chance from 2% to only about 39%.",
           "الاحتمال الكلي لفحص إيجابي: 0.02 · 0.95 + 0.98 · 0.03 = 0.019 + 0.0294 = 0.0484. ثم P(مريض|+) = 0.019 ÷ 0.0484 ≈ 0.39. أي أن الفحص الإيجابي رفع الاحتمال من 2% إلى نحو 39% فقط.", "≈ 39 %."),
         tree([("S", "0.02"), ("H", "0.98")], [[("+", "0.95"), ("−", "0.05")], [("+", "0.03"), ("−", "0.97")]], prods=["0.019", "", "0.0294", ""], tag="E9"), d_bayes(),
         F("P(S | +) = 0.019 / 0.0484 ≈ 0.39")]),
    _ex("10", "Among 100 people, 30 smoke. 12 smokers and 14 non-smokers have a cough. Find P(cough) and the probability that a person with a cough is a smoker.",
        "بين 100 شخص 30 يدخّنون. 12 مدخّنًا و14 غير مدخّن يسعلون. جد P(سعال) واحتمال أن يكون من يسعل مدخّنًا.", "100 personnes, 30 fumeurs. P(toux), P(fumeur | toux) ?",
        [T("Non-smokers: 70. Coughers: 12 + 14 = 26, so P(cough) = 26/100. Smokers among coughers: 12 out of 26, so P(smoker | cough) = 12/26 = 6/13 ≈ 0.46.",
           "غير المدخّنين 70. من يسعلون 12 + 14 = 26 فـ P(سعال) = 26/100. المدخّنون بين من يسعلون: 12 من 26 فـ P(مدخّن|سعال) = 12/26 = 6/13 ≈ 0.46.", "6/13."), F("P(smoker | cough) = 12 / 26 = 6 / 13")]),
    _ex("11", "Two fair dice are rolled. Find the probability that the sum is 8 knowing that the first die shows an even number.",
        "نرمي حجري نرد عادلين. جد احتمال أن يكون المجموع 8 علمًا أن الحجر الأول يُظهر عددًا زوجيًّا.", "Deux dés : somme 8 sachant le premier pair ?",
        [T("The new universe: the first die is even, 3 · 6 = 18 outcomes. Favourable: (2, 6), (4, 4), (6, 2), that is 3 outcomes. So the probability is 3/18 = 1/6.",
           "الفضاء الجديد: الحجر الأول زوجي أي 3 · 6 = 18 نتيجة. المواتية: (2, 6) و(4, 4) و(6, 2) أي 3 نتائج. فالاحتمال 3/18 = 1/6.", "1/6."), F("P(sum 8 | first even) = 3 / 18 = 1 / 6")]),
    _ex("12", "P(A) = 0.6 and P(B | A) = 0.5, P(B) = 0.4. Find P(A ∩ B) and P(A | B).",
        "P(A) = 0.6 وP(B|A) = 0.5 وP(B) = 0.4. جد P(A∩B) وP(A|B).", "P(A)=0,6, P(B|A)=0,5, P(B)=0,4 : P(A∩B), P(A|B) ?",
        [T("Multiplication rule: P(A ∩ B) = 0.6 · 0.5 = 0.3. Then P(A | B) = 0.3 / 0.4 = 0.75.",
           "قاعدة الضرب: P(A∩B) = 0.6 · 0.5 = 0.3. ثم P(A|B) = 0.3 ÷ 0.4 = 0.75.", "0,3 et 0,75."), F("P(A ∩ B) = 0.3      P(A | B) = 0.3 / 0.4 = 0.75")]),
    _ex("13", "Three factories make 50%, 30% and 20% of the items, with 2%, 3% and 5% defective. Find the probability that an item is defective.",
        "ثلاثة مصانع تنتج 50% و30% و20% من القطع وفيها 2% و3% و5% معيب. جد احتمال أن تكون قطعة معيبة.", "Trois usines : P(D) ?",
        [T("The three parts partition the production. P(D) = 0.5 · 0.02 + 0.3 · 0.03 + 0.2 · 0.05 = 0.010 + 0.009 + 0.010 = 0.029.",
           "المصانع الثلاثة تجزئة للإنتاج. P(D) = 0.5 · 0.02 + 0.3 · 0.03 + 0.2 · 0.05 = 0.010 + 0.009 + 0.010 = 0.029.", "0,029."),
         tree([("X", "0.5"), ("Y", "0.3"), ("Z", "0.2")], [[("D", "0.02"), ("OK", "0.98")], [("D", "0.03"), ("OK", "0.97")], [("D", "0.05"), ("OK", "0.95")]], tag="E13"),
         F("P(D) = 0.010 + 0.009 + 0.010 = 0.029")]),
    _ex("14", "Error detective: 'The probability that a sick person tests positive is 0.95, so the probability that a person who tests positive is sick is also 0.95.' Why is it wrong?",
        "المحقق: «احتمال أن يكون الفحص إيجابيًّا عند المريض 0.95 إذن احتمال أن يكون من فحصه إيجابي مريضًا هو 0.95 أيضًا». لماذا هذا خطأ؟", "Pourquoi P(+|S) ≠ P(S|+) ?",
        [T("This swaps P(+ | sick) with P(sick | +). They are different: in exercise 9 the second is only about 0.39 because the disease is rare.",
           "هذا يبدّل P(+|مريض) بـ P(مريض|+). وهما مختلفان: في التمرين 9 الثاني نحو 0.39 فقط لأن المرض نادر.", "Non : 0,39."), F("P(+ | S) = 0.95   but   P(S | +) ≈ 0.39")]),
]
