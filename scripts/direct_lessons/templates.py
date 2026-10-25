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
