"""Reusable lesson templates (data only)."""
from scripts.direct_lessons.common import T, F, D, EX, st, objects, row, numeral, scene

WORD = {
    1: ("one", "واحد", "un"), 2: ("two", "اثنان", "deux"), 3: ("three", "ثلاثة", "trois"), 4: ("four", "أربعة", "quatre"),
    5: ("five", "خمسة", "cinq"), 6: ("six", "ستة", "six"), 7: ("seven", "سبعة", "sept"), 8: ("eight", "ثمانية", "huit"),
    9: ("nine", "تسعة", "neuf"), 10: ("ten", "عشرة", "dix"),
}


def count_words(n):
    en = ", ".join(WORD[i][0] for i in range(1, n + 1))
    ar = "، ".join(WORD[i][1] for i in range(1, n + 1))
    fr = ", ".join(WORD[i][2] for i in range(1, n + 1))
    return en, ar, fr


def counting_lesson(lo, hi, p0):
    """Numbers up to `hi`; the new numbers are lo..hi. returns (THEORY, EXERCISES)."""
    th = []
    kinds = [("circle", "#e53935"), ("star", "#fbc02d"), ("square", "#1e63d6"), ("tri", "#43a047"), ("circle", "#8e24aa")]
    for k, n in enumerate(range(lo, hi + 1)):
        kd, col = kinds[k % len(kinds)]
        e, a, f = count_words(n)
        e0, a0, f0 = count_words(n - 1)
        wn, wa, wf = WORD[n]
        w0n, w0a, w0f = WORD[n - 1]
        th.append((f"Building {n}", f"نصنع العدد {n}", f"Faire {n}", str(p0 + k), [
            objects(n - 1, kd, col, None, prefix=f"b{n}a", r=24 if n > 7 else 30),
            T(f"Count the objects: {e0}. There are {n - 1}.",
              f"عُدّ الأشياء: {a0}. يوجد {n - 1}.",
              f"Compte les objets : {f0}. Il y en a {n - 1}."),
            objects(n, kd, col, n, prefix=f"b{n}b", r=24 if n > 7 else 30),
            T(f"We add one more and count again from the beginning: {e}. The last number is {wn}.",
              f"نضيف شيئًا واحدًا ونعدّ من البداية: {a}. آخر عدد هو {wn}.",
              f"On en ajoute un et on recompte depuis le début : {f}. Le dernier nombre est {wn}."),
            F(f"{n - 1} and one more = {wn} = {n}"),
            T(f"The numeral {n} means a collection of {n} things.",
              f"الرقم {n} يعني مجموعة فيها {n} من الأشياء.",
              f"Le chiffre {n} veut dire une collection de {n} choses."),
        ]))
    th.append(("The last counting word gives the total", "آخر كلمة عدّ تعطي المجموع", "Le dernier mot donne le total", str(p0 + hi - lo + 1), [
        T(f"When we count, we touch each object only once. The last number we say tells how many there are in all.",
          f"عندما نعدّ نلمس كل شيء مرة واحدة فقط. آخر عدد نقوله يخبرنا كم يوجد في المجموع.",
          f"Quand on compte, on touche chaque objet une seule fois. Le dernier nombre dit combien il y en a en tout."),
        T("If we touch an object twice the number is too big. If we skip one it is too small.",
          "إذا لمسنا شيئًا مرتين يصبح العدد أكبر من الحقيقة. وإذا نسينا شيئًا يصبح أصغر.",
          "Si on touche un objet deux fois, le nombre est trop grand. Si on en oublie un, il est trop petit."),
    ]))
    th.append(("The arrangement can change, the quantity stays", "يتغيّر الترتيب وتبقى الكمية", "La disposition change, la quantité reste", str(p0 + hi - lo + 2), [
        scene(*row(hi, "circle", "#8e24aa", 220, "g", r=18 if hi > 7 else 24, gap=60 if hi > 7 else 74)),
        T(f"{hi} dots in a row. We count: {count_words(hi)[0]}.",
          f"{hi} نقاط في صف. نعدّ: {count_words(hi)[1]}.",
          f"{hi} points alignés. On compte : {count_words(hi)[2]}."),
        T(f"If the dots move into a new shape, and we add none and take none away, there are still {hi}. Spreading out does not make more.",
          f"إذا تحرّكت النقاط إلى شكل جديد ولم نضف ولم نحذف، فما زالت {hi}. التباعد لا يزيد العدد.",
          f"Si les points prennent une autre forme sans qu'on en ajoute ou enlève, il y en a toujours {hi}. Écarter n'en fait pas plus."),
    ]))
    th.append(("Summary", "الخلاصة", "Résumé", "", [
        F(" — ".join(str(i) for i in range(1, hi + 1))),
        F("TOUCH → COUNT → LAST NUMBER → MATCH THE NUMERAL → CHECK"),
        T("Every numeral has a quantity. We count each object once, the last number tells the total, and moving objects around does not change the number.",
          "لكل رقم كمية. نعدّ كل شيء مرة واحدة، وآخر عدد يخبرنا بالمجموع، وتحريك الأشياء لا يغيّر العدد.",
          "Chaque chiffre a une quantité. On compte chaque objet une fois, le dernier nombre donne le total, et déplacer les objets ne change pas le nombre."),
    ]))
    ex = []
    n = lo
    e, a, f = count_words(n)
    ex.append(EX("1", "", st(f"Build {n} stars.", f"ابنِ {n} نجوم.", f"Construis {n} étoiles."), [
        objects(n, "star", "#fbc02d", n, prefix="x1", r=24 if n > 7 else 30),
        T(f"We put the stars one by one and count: {e}. If we have {n - 1} we add one more. If we have more than {n} we take the extra away.",
          f"نضع النجوم واحدة واحدة ونعدّ: {a}. إذا كان عندنا {n - 1} نضيف واحدة، وإذا زادت عن {n} نُخرج الزائد.",
          f"On pose les étoiles une à une et on compte : {f}. S'il y en a {n - 1}, on en ajoute une. S'il y en a plus de {n}, on enlève le surplus."),
    ]))
    n = hi
    e, a, f = count_words(n)
    ex.append(EX("2", "", st(f"Count the dots and choose the numeral: {n - 2}, {n - 1} or {n}.", f"عُدّ النقاط واختر الرقم: {n - 2} أو {n - 1} أو {n}.", f"Compte les points et choisis le chiffre : {n - 2}, {n - 1} ou {n}."), [
        objects(n, "circle", "#1e63d6", None, prefix="x2", r=24 if n > 7 else 30),
        T(f"Touch each dot once: {e}. The last number is {WORD[n][0]}, so the numeral is {n}.",
          f"المس كل نقطة مرة واحدة: {a}. آخر عدد {WORD[n][0]}، إذن الرقم هو {n}.",
          f"Touche chaque point une fois : {f}. Le dernier nombre est {WORD[n][0]}, donc le chiffre est {n}."),
        F(f"{n} dots = {n}"),
    ]))
    ex.append(EX("3", "", st(f"Same or different? {hi} stars close together and {hi} stars far apart.", f"متساويان أم مختلفان؟ {hi} نجوم متقاربة و{hi} نجوم متباعدة.", f"Pareil ou différent ? {hi} étoiles proches et {hi} étoiles éloignées."), [
        T(f"The spread-out group looks bigger, but we count both groups: {count_words(hi)[0]}.",
          f"تبدو المتباعدة أكبر، لكننا نعدّ المجموعتين: {count_words(hi)[1]}.",
          f"Le groupe écarté semble plus grand, mais on compte les deux : {count_words(hi)[2]}."),
        F(f"{hi} = {hi}"),
        T("The distance between the objects does not change how many there are.",
          "المسافة بين الأشياء لا تغيّر عددها.",
          "La distance entre les objets ne change pas leur nombre."),
    ]))
    ex.append(EX("4", "", st(f"Show the numeral {hi - 1}, then {hi}, with objects.", f"أظهر الرقم {hi - 1} ثم {hi} بأشياء.", f"Montre le chiffre {hi - 1}, puis {hi}, avec des objets."), [
        objects(hi - 1, "square", "#43a047", hi - 1, prefix="x4a", r=24 if hi > 7 else 30),
        objects(hi, "square", "#43a047", hi, prefix="x4b", r=24 if hi > 7 else 30),
        T(f"We build the quantity and check by counting up to {hi - 1}, then up to {hi}.",
          f"نبني الكمية ونتحقق بالعدّ حتى {hi - 1} ثم حتى {hi}.",
          f"On construit la quantité et on vérifie en comptant jusqu'à {hi - 1}, puis jusqu'à {hi}."),
    ]))
    ex.append(EX("5", "", st(f"Error detective: {hi - 1} objects and the numeral {hi}.", f"المحقق: {hi - 1} أشياء والرقم المكتوب {hi}.", f"Détective : {hi - 1} objets et le chiffre {hi}."), [
        objects(hi - 1, "tri", "#8d6e63", hi, prefix="x5", r=24 if hi > 7 else 30),
        T(f"Count: {count_words(hi - 1)[0]}. There are {hi - 1}, but the numeral is {hi}. They do not match.",
          f"نعدّ: {count_words(hi - 1)[1]}. يوجد {hi - 1} لكن المكتوب {hi}. لا يتطابقان.",
          f"On compte : {count_words(hi - 1)[2]}. Il y en a {hi - 1} mais le chiffre est {hi}. Ça ne correspond pas."),
        F(f"{hi - 1} objects → {hi - 1}"),
    ]))
    return th, ex


# ---------------------------------------------------------------- teens (11-19)
TEEN = {
    11: ("eleven", "أحد عشر", "onze"), 12: ("twelve", "اثنا عشر", "douze"), 13: ("thirteen", "ثلاثة عشر", "treize"),
    14: ("fourteen", "أربعة عشر", "quatorze"), 15: ("fifteen", "خمسة عشر", "quinze"), 16: ("sixteen", "ستة عشر", "seize"),
    17: ("seventeen", "سبعة عشر", "dix-sept"), 18: ("eighteen", "ثمانية عشر", "dix-huit"), 19: ("nineteen", "تسعة عشر", "dix-neuf"),
}


def teens_lesson(lo, hi, p0):
    """numbers lo..hi (11..19): one ten + extra ones. returns (THEORY, EXERCISES)."""
    from scripts.direct_lessons.common import T, F, EX, st, tens, numpath
    W = lambda n: TEEN[n] if n in TEEN else WORD[n]
    ones = {1: ("one", "واحد", "un"), 2: ("two", "اثنان", "deux"), 3: ("three", "ثلاثة", "trois"), 4: ("four", "أربعة", "quatre"),
            5: ("five", "خمسة", "cinq"), 6: ("six", "ستة", "six"), 7: ("seven", "سبعة", "sept"), 8: ("eight", "ثمانية", "huit"), 9: ("nine", "تسعة", "neuf")}
    nums = list(range(lo, hi + 1))
    seq = [str(x) for x in range(10, hi + 1)]
    theory = []
    theory.append(("Ten and more", "عشرة وأكثر", "Dix et plus", str(p0), [
        T(f"Hello! Do you remember 10? It is one ten, or ten ones. Today we walk after 10 step by step and discover {', '.join(str(n) for n in nums[:-1])} and {nums[-1]}.",
          f"مرحبًا! هل تذكر 10؟ إنها عشرة واحدة أو عشرة آحاد. اليوم نمشي بعد 10 خطوة خطوة ونكتشف {'، '.join(str(n) for n in nums[:-1])} و{nums[-1]}.",
          f"Bonjour ! Tu te souviens de 10 ? C'est une dizaine, ou dix unités. Aujourd'hui on avance après 10 pas à pas et on découvre {', '.join(str(n) for n in nums[:-1])} et {nums[-1]}."),
        tens(1, 0),
        T("This is one ten. We start counting from ten, not from one: we do not count the bundle again.",
          "هذه عشرة واحدة. نبدأ العدّ من العشرة لا من الواحد: لا نعيد عدّ الحزمة.",
          "Voici une dizaine. On compte à partir de dix, pas à partir de un : on ne recompte pas le paquet."),
    ]))
    for n in nums:
        e, a, f = W(n)
        o = n - 10
        oe, oa, of_ = ones[o]
        prev = W(n - 1)[0] if n - 1 > 10 else "ten"
        prev_f = W(n - 1)[2] if n - 1 > 10 else "dix"
        prev_a = W(n - 1)[1] if n - 1 > 10 else "عشرة"
        theory.append((f"{n} = one ten and {oe} {'one' if o == 1 else 'ones'}", f"{n} = عشرة واحدة و{oa}", f"{n} = une dizaine et {of_} unité" + ("s" if o > 1 else ""), str(p0), [
            tens(1, o),
            T(f"We have one ten, which is 10, and {o} loose {'one' if o == 1 else 'ones'}. We count from ten: {', '.join(['ten'] + [W(k)[0] for k in range(11, n + 1)])}. This is {n}, {e}.",
              f"عندنا عشرة واحدة أي 10، ومعها {o} {'واحد' if o == 1 else 'آحاد'} منفردة. نعدّ من العشرة: {'، '.join(['عشرة'] + [W(k)[1] for k in range(11, n + 1)])}. هذا {n}، {a}.",
              f"On a une dizaine, soit 10, et {o} unité{'s' if o > 1 else ''} seule{'s' if o > 1 else ''}. On compte à partir de dix : {', '.join(['dix'] + [W(k)[2] for k in range(11, n + 1)])}. C'est {n}, {f}."),
            F(f"one ten + {o} = {n}"),
            T(f"Look at the numeral {n}: the first 1 stands for the ten, and the {str(n)[1]} stands for the {o} loose ones.",
              f"انظر إلى العدد {n}: الـ1 الأول يمثّل العشرة، والـ{str(n)[1]} يمثّل الآحاد المنفردة وعددها {o}.",
              f"Regarde le nombre {n} : le premier 1 représente la dizaine et le {str(n)[1]} représente les {o} unités seules."),
        ])) 
    theory.append(("The number path", "مسار الأعداد", "La droite des nombres", str(p0), [
        numpath(seq),
        T("Each time we add one, we move one step forward. And when we remove one, we go one step back.",
          "كلما أضفنا واحدًا نتحرك خطوة إلى الأمام، وكلما أزلنا واحدًا نعود خطوة إلى الخلف.",
          "Chaque fois qu'on ajoute un, on avance d'un pas. Quand on enlève un, on recule d'un pas."),
    ]))
    theory.append(("Summary", "الخلاصة", "Résumé", "", [
        T(f"Today we walked after 10 and reached {hi}. Every number here is one ten and some extra ones. Each extra one moves us one step forward on the number path.",
          f"اليوم مشينا بعد 10 ووصلنا إلى {hi}. كل عدد هنا هو عشرة واحدة وبعض الآحاد الإضافية. كل واحد إضافي يحرّكنا خطوة إلى الأمام على مسار الأعداد.",
          f"Aujourd'hui on a avancé après 10 jusqu'à {hi}. Chaque nombre ici est une dizaine et quelques unités en plus. Chaque unité en plus nous fait avancer d'un pas."),
        F("SEE THE TEN → COUNT THE EXTRA ONES → SAY THE NUMBER → MATCH THE NUMERAL → CHECK"),
    ]))
    ex = []
    a, b, c = nums[0], nums[len(nums) // 2], nums[-1]
    ex.append(EX("1", str(p0), st(f"Build {a}: one ten and the loose ones.", f"ابنِ {a}: عشرة واحدة والآحاد المنفردة.", f"Construis {a} : une dizaine et les unités seules."), [
        tens(1, a - 10),
        T(f"One ten and {a - 10} loose: {a}.", f"عشرة واحدة و{a - 10} منفردة: {a}.", f"Une dizaine et {a - 10} seules : {a}."),
        F(f"10 + {a - 10} = {a}"),
    ]))
    ex.append(EX("2", str(p0), st(f"Match {b}: which card has one ten and {b - 10} ones?", f"طابق {b}: أي بطاقة فيها عشرة واحدة و{b - 10} آحاد؟", f"Associe {b} : quelle carte a une dizaine et {b - 10} unités ?"), [
        tens(1, b - 10),
        T(f"First look for the one ten, then count the loose ones: {b - 10}. So {b}.",
          f"نبحث أولًا عن العشرة الواحدة ثم نعدّ المنفردة: {b - 10}. إذن {b}.",
          f"On cherche d'abord la dizaine, puis on compte les unités seules : {b - 10}. Donc {b}."),
    ]))
    ex.append(EX("3", str(p0), st(f"Build {c} using one ten and loose ones.", f"ابنِ {c} بعشرة واحدة وآحاد منفردة.", f"Construis {c} avec une dizaine et des unités seules."), [
        tens(1, c - 10),
        T(f"Count from ten: {', '.join(['ten'] + [W(k)[0] for k in range(11, c + 1)])}. There are {c - 10} loose ones.",
          f"نعدّ من العشرة: {'، '.join(['عشرة'] + [W(k)[1] for k in range(11, c + 1)])}. المنفردة {c - 10}.",
          f"On compte à partir de dix : {', '.join(['dix'] + [W(k)[2] for k in range(11, c + 1)])}. Il y a {c - 10} unités seules."),
    ]))
    miss = seq[:]
    mi = len(miss) // 2
    shown = miss[:]; shown[mi] = "?"
    ex.append(EX("4", str(p0), st("Find the missing number.", "أوجد العدد الناقص.", "Trouve le nombre manquant."), [
        numpath(shown),
        T(f"Count step by step from 10. After {miss[mi - 1]} comes {miss[mi]}.",
          f"نعدّ خطوة خطوة من 10. بعد {miss[mi - 1]} يأتي {miss[mi]}.",
          f"On compte pas à pas depuis 10. Après {miss[mi - 1]} vient {miss[mi]}."),
        F(miss[mi]),
    ]))
    wrong = a if a != c else a + 1
    ex.append(EX("5", str(p0), st(f"Error detective: one ten and {c - 10} ones, but the numeral says {wrong}.", f"المحقق: عشرة واحدة و{c - 10} آحاد لكن العدد المكتوب {wrong}.", f"Détective : une dizaine et {c - 10} unités, mais le nombre écrit est {wrong}."), [
        tens(1, c - 10),
        T(f"One ten is 10, and {c - 10} more ones reach {c}. We do not accept a numeral that does not match the quantity.",
          f"العشرة 10 ومعها {c - 10} آحاد تصل إلى {c}. لا نقبل عددًا لا يطابق الكمية.",
          f"Une dizaine fait 10 et {c - 10} unités de plus arrivent à {c}. On n'accepte pas un nombre qui ne correspond pas à la quantité."),
        F(str(c)),
    ]))
    ex.append(EX("6", str(p0), st(f"Mixed practice: read the number, how many ones are outside the ten, and what comes just before {c}.", f"تدريب مختلط: اقرأ العدد، وكم آحادًا خارج العشرة، وماذا يأتي قبل {c}.", f"Exercice mixte : lis le nombre, combien d'unités hors de la dizaine, et qu'est-ce qui vient avant {c}."), [
        tens(1, b - 10),
        F(f"{b}      {b - 10} ones      before {c} comes {c - 1}"),
    ]))
    ex.append(EX("7", str(p0), st(f"Challenge: I have {c} counters and I make one ten bundle. How many stay loose?", f"تحدٍّ: عندي {c} عدّادًا وأصنع حزمة عشرة. كم يبقى منفردًا؟", f"Défi : j'ai {c} jetons et je fais un paquet de dix. Combien restent seuls ?"), [
        tens(1, c - 10),
        T(f"{c} is one ten and {c - 10} ones. So {c - 10} stay loose.",
          f"{c} هي عشرة واحدة و{c - 10} آحاد. إذن يبقى {c - 10} منفردًا.",
          f"{c}, c'est une dizaine et {c - 10} unités. Il en reste donc {c - 10} seules."),
    ]))
    ex.append(EX("8", str(p0), st(f"Final check: build {a}, {b} and {c}, and say what comes just before {c}.", f"تقييم أخير: ابنِ {a} و{b} و{c}، وقل ماذا يأتي قبل {c}.", f"Évaluation : construis {a}, {b} et {c}, et dis ce qui vient avant {c}."), [
        tens(1, a - 10), tens(1, b - 10), tens(1, c - 10),
        T(f"{c} is one ten and {c - 10} ones, because ten plus {c - 10} more objects gives {c}. Just before {c} comes {c - 1}.",
          f"{c} هي عشرة واحدة و{c - 10} آحاد، لأن عشرة و{c - 10} أشياء أخرى تعطي {c}. وقبل {c} يأتي {c - 1}.",
          f"{c} est une dizaine et {c - 10} unités, car dix plus {c - 10} objets de plus font {c}. Juste avant {c} vient {c - 1}."),
    ]))
    return theory, ex
