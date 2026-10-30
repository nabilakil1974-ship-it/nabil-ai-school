from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import section, add_ex, add_sec, fn_graph
from scripts.direct_lessons.draw import mapping


def upgrade(m):
    s = section(m, "A mapping: source, target, rule")
    s.append(mapping([0, 1, 2], [1, 3, 5, 7], [(0, 1), (1, 3), (2, 5)], tag="M1", rule="rule: x → 2x + 1"))
    s.append(T("Each element of the source has exactly one arrow, so this is a mapping. 0 goes to 1, 1 goes to 3, 2 goes to 5. The target element 7 receives no arrow: that is allowed. The image of 2 is 5, and a preimage of 5 is 2.",
               "لكل عنصر من المصدر سهم واحد بالضبط فهذا تطبيق. 0 يذهب إلى 1 و1 إلى 3 و2 إلى 5. العنصر 7 في الهدف لا يصله سهم وهذا مسموح. صورة 2 هي 5 وسابقة 5 هي 2.",
               "Chaque élément de la source a une seule flèche : application. 7 n'a pas d'antécédent : permis."))
    add_sec(m, ("Not a mapping", "ليس تطبيقًا", "Pas une application"), [
        T("Two things break a mapping: an element of the source with NO arrow, or an element with TWO arrows. In the diagram below, 1 sends arrows to two different targets, so it is not a mapping. But two different sources may share one target arrow: that is fine.",
          "أمران يفسدان التطبيق: عنصر من المصدر بلا سهم أو عنصر له سهمان. في الرسم التالي يخرج من 1 سهمان إلى هدفين مختلفين فهو ليس تطبيقًا. أما أن يشترك مصدران في سهم هدف واحد فلا بأس.",
          "Un élément sans flèche ou avec deux flèches : pas d'application. Deux sources vers la même cible : permis."),
        mapping([1, 2, 3], ["a", "b", "c"], [(1, "a"), (1, "b"), (2, "c")], tag="M2", rule="1 has two arrows and 3 has none: NOT a mapping"),
    ])
    add_ex(m, [
        EX("", "", st("A = {1, 2, 3}, B = {a, b}. List A × B and say how many elements it has.", "A = {1, 2, 3} وB = {a, b}. اكتب A × B وكم عدد عناصره.", "A = {1 ; 2 ; 3}, B = {a ; b} : liste A × B."), [
            T("Pair each element of A with each element of B: (1, a), (1, b), (2, a), (2, b), (3, a), (3, b).", "نقرن كل عنصر من A بكل عنصر من B: (1, a) و(1, b) و(2, a) و(2, b) و(3, a) و(3, b).", "6 couples."), F("3 × 2 = 6 pairs")]),
        EX("", "", st("f: {−1, 0, 1, 2} → ℝ, f(x) = x² − 1. List the images and say which elements share an image.", "f: {−1, 0, 1, 2} → ℝ حيث f(x) = x² − 1. اكتب الصور وبيّن العناصر التي تشترك في صورة.", "f(x) = x² − 1 sur {−1 ; 0 ; 1 ; 2} : images."), [
            T("f(−1) = 0, f(0) = −1, f(1) = 0, f(2) = 3. The elements −1 and 1 have the same image 0.", "f(−1) = 0 وf(0) = −1 وf(1) = 0 وf(2) = 3. العنصران −1 و1 لهما الصورة نفسها 0.", "−1 et 1 ont la même image 0."), mapping([-1, 0, 1, 2], [-1, 0, 3], [(-1, 0), (0, -1), (1, 0), (2, 3)], tag="X1", rule="f(x) = x² − 1"), F("images: 0, −1, 0, 3")]),
        EX("", "", st("Is 'each pupil → his or her mother' a mapping from pupils to people? Is 'each person → his or her child' one?", "هل «كل تلميذ ← أمه» تطبيق من التلاميذ إلى الأشخاص؟ وهل «كل شخص ← ابنه» تطبيق؟", "« élève → sa mère » est-ce une application ? « personne → son enfant » ?"), [
            T("Each pupil has exactly one mother: it is a mapping. A person may have several children or none, so the second relation is not a mapping.", "لكل تلميذ أم واحدة بالضبط فهو تطبيق. أما الشخص فقد يكون له عدة أبناء أو لا أبناء فالعلاقة الثانية ليست تطبيقًا.", "1re oui ; 2e non."), F("yes; no")]),
    ])
