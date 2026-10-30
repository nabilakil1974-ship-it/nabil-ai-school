from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import section, add_ex, add_sec
from scripts.direct_lessons.draw import venn


def upgrade(m):
    s = section(m, "Venn diagram")
    s.append(venn("A", "B", "1   3", "4   6", "2   5", outside="Outside both: 7, 8", tag="G1"))
    s.append(T("A = {1, 2, 3, 5} and B = {2, 4, 5, 6}. The overlap holds what is in both: A ∩ B = {2, 5}. Everything drawn in at least one circle is the union: A ∪ B = {1, 2, 3, 4, 5, 6}. Elements 7 and 8 are in the universe but in neither set.",
               "A = {1, 2, 3, 5} وB = {2, 4, 5, 6}. التقاطع يضم ما هو في الاثنين: A ∩ B = {2, 5}. وكل ما رُسم في دائرة واحدة على الأقل هو الاتحاد: A ∪ B = {1, 2, 3, 4, 5, 6}. العنصران 7 و8 في المجموعة الشاملة لكن في أيٍّ من المجموعتين لا.",
               "A ∩ B = {2 ; 5} ; A ∪ B = {1 ; 2 ; 3 ; 4 ; 5 ; 6}. 7 et 8 sont hors des deux ensembles."))
    add_sec(m, ("Counting with a Venn diagram", "العدّ بمخطط فن", "Dénombrer avec un diagramme"), [
        T("In a class of 30, 18 play football (F), 12 play basketball (B) and 5 play both. Start in the middle: 5 play both. Football only: 18 − 5 = 13. Basketball only: 12 − 5 = 7. So at least one sport: 13 + 5 + 7 = 25, and 30 − 25 = 5 play neither.",
          "في صف من 30 تلميذًا يلعب 18 كرة القدم (F) و12 كرة السلة (B) و5 يلعبون اللعبتين. نبدأ من الوسط: 5 يلعبون الاثنتين. كرة القدم فقط: 18 − 5 = 13. كرة السلة فقط: 12 − 5 = 7. إذن من يلعب لعبة على الأقل: 13 + 5 + 7 = 25 ومن لا يلعب شيئًا 30 − 25 = 5.",
          "30 élèves, 18 F, 12 B, 5 les deux : F seul 13, B seul 7, au moins un sport 25, aucun 5."),
        venn("Football", "Basketball", "13", "7", "5", outside="Neither: 5   (total 30)", tag="G2"),
        F("|F ∪ B| = |F| + |B| − |F ∩ B| = 18 + 12 − 5 = 25"),
    ])
    add_ex(m, [
        EX("", "", st("U = {1, …, 12}, A = multiples of 2, B = multiples of 3. Find A ∩ B, A ∪ B and the elements in neither.", "U = {1, …, 12} وA مضاعفات 2 وB مضاعفات 3. جد A ∩ B وA ∪ B والعناصر التي في أيٍّ منهما لا.", "U = {1..12}, A multiples de 2, B multiples de 3 : A ∩ B, A ∪ B, ni l'un ni l'autre."), [
            T("A = {2, 4, 6, 8, 10, 12} and B = {3, 6, 9, 12}. Common: A ∩ B = {6, 12}.", "A = {2, 4, 6, 8, 10, 12} وB = {3, 6, 9, 12}. المشترك: A ∩ B = {6, 12}.", "A ∩ B = {6 ; 12}."),
            venn("A (×2)", "B (×3)", "2 4 8 10", "3 9", "6   12", outside="Neither: 1, 5, 7, 11", tag="X1"),
            F("A ∪ B = {2, 3, 4, 6, 8, 9, 10, 12}      neither: {1, 5, 7, 11}"), F("Check: 6 + 4 − 2 = 8 elements in A ∪ B ✓")]),
        EX("", "", st("In a group of 40 students, 25 study English, 20 study French, 8 study neither. How many study both?", "في مجموعة من 40 طالبًا يدرس 25 الإنكليزية و20 الفرنسية و8 لا يدرسون أيًّا منهما. كم يدرس اللغتين؟", "40 élèves : 25 anglais, 20 français, 8 aucun. Combien les deux ?"), [
            T("At least one language: 40 − 8 = 32. Using |E ∪ F| = |E| + |F| − |E ∩ F|: 32 = 25 + 20 − x, so x = 13.", "من يدرس لغة على الأقل: 40 − 8 = 32. من |E ∪ F| = |E| + |F| − |E ∩ F|: 32 = 25 + 20 − x إذن x = 13.", "32 = 45 − x → x = 13."), F("13 study both"), F("Check: English only 12, French only 7, both 13: 12 + 7 + 13 = 32 ✓")]),
        EX("", "", st("List all subsets of {a, b, c}. How many are there?", "اكتب كل المجموعات الجزئية لـ {a, b, c}. كم عددها؟", "Liste les sous-ensembles de {a, b, c}."), [
            T("Size 0: ∅. Size 1: {a}, {b}, {c}. Size 2: {a, b}, {a, c}, {b, c}. Size 3: {a, b, c}.", "حجم 0: ∅. حجم 1: {a} و{b} و{c}. حجم 2: {a, b} و{a, c} و{b, c}. حجم 3: {a, b, c}.", "∅ ; 3 singletons ; 3 paires ; l'ensemble."), F("1 + 3 + 3 + 1 = 8 = 2³ subsets")]),
    ])
