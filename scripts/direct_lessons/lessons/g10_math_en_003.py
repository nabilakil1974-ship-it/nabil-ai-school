"""Grade 10 Mathematics — Sets."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G10-MATH-EN-003"
GRADE = 10
SUBJECT = "math"
TITLES = {"en": "Sets", "ar": "المجموعات", "fr": "Les ensembles"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "C = {a, b, c}.  a ? C", "opts": ["∈", "⊂", "∪", "∩"], "a": 0,
     "why": {"⊂": _w("a is an element, not a set: use ∈.", "a عنصر وليس مجموعة: نستعمل ∈.", "a est un élément : ∈."),
             "∪": _w("∪ joins two sets.", "∪ تجمع مجموعتين.", "∪ réunit deux ensembles."),
             "∩": _w("∩ keeps the common part of two sets.", "∩ تأخذ الجزء المشترك بين مجموعتين.", "∩ garde le commun.")}, "ok": "a ∈ C"},
    {"q": "A = {1,2,3,5}, B = {2,4,5,6}.  A ∩ B = ?", "opts": ["{2,5}", "{1,2,3,4,5,6}", "{1,3}", "{4,6}"], "a": 0,
     "why": {"{1,2,3,4,5,6}": _w("That is the union.", "هذه هي الاتحاد.", "C'est la réunion."),
             "{1,3}": _w("Those are only in A.", "هذان في A فقط.", "Seulement dans A."),
             "{4,6}": _w("Those are only in B.", "هذان في B فقط.", "Seulement dans B.")}, "ok": "{2,5}"},
    {"q": "A = {2,3,5,7}, B = {1,3,5,8}.  A ∪ B = ?", "opts": ["{1,2,3,5,7,8}", "{3,5}", "{1,2,3,3,5,5,7,8}", "{2,7}"], "a": 0,
     "why": {"{3,5}": _w("That is the intersection.", "هذه هي التقاطع.", "C'est l'intersection."),
             "{1,2,3,3,5,5,7,8}": _w("Do not repeat elements in a set.", "لا نكرّر العناصر في المجموعة.", "Pas de doublons."),
             "{2,7}": _w("Those are only in A.", "هذان في A فقط.", "Seulement dans A.")}, "ok": "{1,2,3,5,7,8}"},
]

THEORY = [
    ("What is a set?", "ما المجموعة؟", "Qu'est-ce qu'un ensemble ?", "37", [
        T("Hello! A set is a well-defined collection of objects called elements. \"Even numbers smaller than 10\" is well-defined: 2, 4, 6, 8. \"Beautiful numbers\" is not, because people disagree. If A = {1, 2, 3, 4} then 3 ∈ A (3 is an element of A) and 7 ∉ A.",
          "مرحبًا! المجموعة تجمّع جيّد التحديد لأشياء تسمّى عناصر. «الأعداد الزوجية الأصغر من 10» محدّدة جيدًا: 2 و4 و6 و8، أما «الأعداد الجميلة» فلا لأن الناس يختلفون. إذا كانت A = {1, 2, 3, 4} فإن 3 ∈ A (3 عنصر في A) و7 ∉ A.",
          "Un ensemble est une collection bien définie. Si A = {1,2,3,4}, alors 3 ∈ A et 7 ∉ A."),
        F("A = {1, 2, 3, 4}      3 ∈ A      7 ∉ A"),
    ]),
    ("Writing a set", "كتابة المجموعة", "Écrire un ensemble", "37", [
        T("Roster notation lists the elements between braces: B = {2, 4, 6, 8}. Repeating an element changes nothing: {1, 2, 2, 3} = {1, 2, 3}. Order does not matter: {1, 2, 3} = {3, 1, 2}. A set asks who is present, not how many times or in what order.",
          "في الكتابة بالسرد نضع العناصر بين قوسين معقوفين: B = {2, 4, 6, 8}. تكرار العنصر لا يغيّر شيئًا: {1, 2, 2, 3} = {1, 2, 3}. والترتيب لا يهمّ: {1, 2, 3} = {3, 1, 2}. المجموعة تسأل من الموجود لا كم مرة ولا بأي ترتيب.",
          "{1,2,2,3} = {1,2,3} ; l'ordre ne compte pas."),
        F("{1, 2, 2, 3} = {1, 2, 3} = {3, 1, 2}"),
    ]),
    ("Membership is not inclusion", "الانتماء غير الاحتواء", "Appartenance et inclusion", "38", [
        T("∈ relates an element to a set; ⊂ relates a set to a set. With A = {1, 2, 3} and B = {1, 2, 3, 4, 5}: 2 ∈ A, and A ⊂ B because every element of A is in B. {2} is a set, so {2} ⊂ A. To check inclusion, test each element of A: if one fails, there is no inclusion.",
          "الرمز ∈ يربط عنصرًا بمجموعة والرمز ⊂ يربط مجموعة بمجموعة. إذا كانت A = {1, 2, 3} وB = {1, 2, 3, 4, 5} فإن 2 ∈ A وA ⊂ B لأن كل عنصر من A موجود في B. و{2} مجموعة فنكتب {2} ⊂ A. لفحص الاحتواء نختبر عناصر A واحدًا واحدًا: إن فشل عنصر واحد سقط الاحتواء.",
          "∈ : élément-ensemble ; ⊂ : ensemble-ensemble."),
        F("2 ∈ A      {2} ⊂ A      A ⊂ B"),
        F("D = {2, 6}:  2 ∈ B but 6 ∉ B  →  D ⊄ B"),
    ]),
    ("Union and intersection", "الاتحاد والتقاطع", "Réunion et intersection", "39", [
        T("With A = {1, 2, 3, 4} and B = {3, 4, 5, 6}. The union A ∪ B gathers all elements of A or B (or both), without duplicates: {1, 2, 3, 4, 5, 6}. The intersection A ∩ B keeps only elements in both: {3, 4}. Union = gather. Intersection = common part.",
          "لتكن A = {1, 2, 3, 4} وB = {3, 4, 5, 6}. اتحاد A ∪ B يجمع كل عناصر A أو B (أو كليهما) دون تكرار: {1, 2, 3, 4, 5, 6}. وتقاطع A ∩ B يحتفظ بالعناصر الموجودة في المجموعتين: {3, 4}. الاتحاد جمع والتقاطع جزء مشترك.",
          "A ∪ B = {1,2,3,4,5,6} ; A ∩ B = {3,4}."),
        F("A ∪ B = {1, 2, 3, 4, 5, 6}      A ∩ B = {3, 4}"),
    ]),
    ("Venn diagram", "مخطط فن", "Diagramme de Venn", "39", [
        T("Two overlapping circles: the middle region is A ∩ B, and everything inside the two circles together is A ∪ B. An element that belongs to both goes in the overlap. The diagram follows the definitions, not the size of the circles.",
          "دائرتان متداخلتان: المنطقة الوسطى هي A ∩ B وكل ما في الدائرتين معًا هو A ∪ B. العنصر الذي ينتمي إلى المجموعتين يوضع في التداخل. المخطط يتبع التعريفات لا حجم الدائرتين.",
          "Zone commune = A ∩ B."),
    ]),
    ("From a condition to a set", "من الشرط إلى المجموعة", "De la condition à l'ensemble", "39", [
        T("U = {1, …, 10}. A = the even numbers: {2, 4, 6, 8, 10}. B = the numbers greater than 5: {6, 7, 8, 9, 10}. A ∩ B (even AND greater than 5) = {6, 8, 10}. A ∪ B (even OR greater than 5) = {2, 4, 6, 7, 8, 9, 10}. Clubs: M = {Ali, Sara, Maya, Jad}, S = {Maya, Jad, Rami}: \"both clubs\" is M ∩ S = {Maya, Jad}; \"at least one club\" is M ∪ S.",
          "U = {1, …, 10}. A الأعداد الزوجية: {2, 4, 6, 8, 10}. B الأعداد الأكبر من 5: {6, 7, 8, 9, 10}. A ∩ B (زوجي «و» أكبر من 5) = {6, 8, 10}. A ∪ B (زوجي «أو» أكبر من 5) = {2, 4, 6, 7, 8, 9, 10}. في النوادي: M = {Ali, Sara, Maya, Jad} وS = {Maya, Jad, Rami}؛ «في النادي معًا» هو M ∩ S = {Maya, Jad} و«في نادٍ واحد على الأقل» هو M ∪ S.",
          "Pair : ET = intersection, OU = réunion."),
        F("A ∩ B = {6, 8, 10}      A ∪ B = {2, 4, 6, 7, 8, 9, 10}"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Ask first: am I relating an element to a set (∈) or a set to a set (⊂)? Do I gather (∪) or keep what is common (∩)? No duplicates, order is irrelevant.",
          "أسأل أولًا: هل أربط عنصرًا بمجموعة (∈) أم مجموعة بمجموعة (⊂)؟ وهل أجمع (∪) أم آخذ المشترك (∩)؟ لا تكرار للعناصر والترتيب غير مهم.",
          "Élément→ensemble ∈ ; ensemble→ensemble ⊂ ; ∪ réunit ; ∩ commun."),
        F("x ∈ A      A ⊂ B      A ∪ B      A ∩ B"),
    ]),
]

EXERCISES = [
    EX("1", "", st("A = {1, 3, 5, 7}: is 5 ∈ A? is 2 ∈ A?", "A = {1, 3, 5, 7}: هل 5 ∈ A؟ وهل 2 ∈ A؟", "A = {1,3,5,7} : 5 ∈ A ? 2 ∈ A ?"), [F("5 ∈ A      2 ∉ A")]),
    EX("2", "", st("A = {1, 2}, B = {1, 2, 3, 4}: is A ⊂ B?", "A = {1, 2} وB = {1, 2, 3, 4}: هل A ⊂ B؟", "A ⊂ B ?"), [T("1 ∈ B and 2 ∈ B: no element of A fails.", "1 ∈ B و2 ∈ B: لا يفشل أي عنصر من A.", "Aucun élément ne manque."), F("A ⊂ B")]),
    EX("3", "", st("A = {1, 2, 3, 5}, B = {2, 4, 5, 6}: find A ∪ B and A ∩ B.", "A = {1, 2, 3, 5} وB = {2, 4, 5, 6}: أوجد A ∪ B وA ∩ B.", "Trouve A ∪ B et A ∩ B."), [F("A ∪ B = {1, 2, 3, 4, 5, 6}      A ∩ B = {2, 5}")]),
    EX("4", "", st("U = {1, …, 12}, A = multiples of 2, B = multiples of 3: find A ∩ B.", "U = {1, …, 12}، A مضاعفات 2 وB مضاعفات 3: أوجد A ∩ B.", "A ∩ B ?"), [F("A = {2, 4, 6, 8, 10, 12}      B = {3, 6, 9, 12}"), F("A ∩ B = {6, 12}")]),
    EX("5", "", st("Error detective: A = {1, 2, 3}, B = {3, 4}, \"A ∩ B = {1, 2, 3, 4}\".", "المحقق: A = {1, 2, 3} وB = {3, 4} و«A ∩ B = {1, 2, 3, 4}».", "Détective : A ∩ B = {1,2,3,4} ?"), [T("That is the union. The only common element is 3.", "هذا هو الاتحاد. العنصر المشترك الوحيد هو 3.", "C'est la réunion."), F("A ∩ B = {3}      A ∪ B = {1, 2, 3, 4}")]),
    EX("6", "", st("A = {2, 3, 5, 7}, B = {1, 3, 5, 8}: find A ∪ B and A ∩ B.", "A = {2, 3, 5, 7} وB = {1, 3, 5, 8}: أوجد A ∪ B وA ∩ B.", "Trouve A ∪ B et A ∩ B."), [F("A ∪ B = {1, 2, 3, 5, 7, 8}      A ∩ B = {3, 5}")]),
    EX("7", "", st("Challenge: U = {1, …, 20}, A multiples of 2, B multiples of 5: find A ∩ B.", "تحدٍّ: U = {1, …, 20}، A مضاعفات 2 وB مضاعفات 5: أوجد A ∩ B.", "Défi : multiples de 2 et de 5."), [F("B = {5, 10, 15, 20}      A ∩ B = {10, 20}")]),
]
