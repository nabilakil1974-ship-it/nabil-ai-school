"""Grade 1 Mathematics — Ordinal numbers."""
from scripts.direct_lessons.common import T, F, EX, st, scene

COLS = ["#ef9a9a", "#ffcc80", "#fff59d", "#a5d6a7", "#81d4fa", "#ce93d8", "#bcaaa4"]


def line(n, hi=None, tag="O", start="left", labels=False):
    """Row of n runners; a green START flag at the stated side; optional highlighted position (1-based from start)."""
    w, x0 = 84, 60
    svg = ""
    ids = []
    flag_x = x0 - 40 if start == "left" else x0 + n * w + 6
    svg += (f'<g id="{tag}s"><rect x="{flag_x}" y="40" width="6" height="110" fill="#0b3d5c"/>'
            f'<polygon points="{flag_x+6},40 {flag_x+46},56 {flag_x+6},72" fill="#2e7d32"/>'
            f'<text x="{flag_x+3}" y="172" font-size="20" font-weight="700" fill="#2e7d32" text-anchor="middle" font-family="sans-serif">START</text></g>')
    ids.append(tag + "s")
    for i in range(n):
        pos = i + 1 if start == "left" else n - i
        x = x0 + i * w + w / 2
        stroke = "#e53935" if hi == pos else "#0b3d5c"
        sw = 7 if hi == pos else 3
        svg += (f'<g id="{tag}{i}"><circle cx="{x}" cy="110" r="32" fill="{COLS[i % 7]}" stroke="{stroke}" stroke-width="{sw}"/>'
                + (f'<text x="{x}" y="120" font-size="28" font-weight="700" text-anchor="middle" fill="#0b3d5c" font-family="sans-serif">{pos}</text>' if labels else "")
                + '</g>')
        ids.append(f"{tag}{i}")
    return scene(svg, ids)


LESSON_ID = "G01-MATH-EN-039"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Ordinal numbers", "ar": "الأعداد الترتيبية", "fr": "Les nombres ordinaux"}

THEORY = [
    ("How many, or which place?", "كم العدد أم أي مكان؟", "Combien, ou quelle place ?", "100", [
        T("Hello, champion! Look at this row of 5 friends. If I ask how many friends there are, the answer is 5: that tells us the quantity. But if I ask which friend is the third, I am asking about a place in the row. Two different questions: how many? and which place?",
          "مرحبًا يا بطل! انظر إلى صف من 5 أصدقاء. إذا سألت كم صديقًا هنا فالجواب 5: هذا يخبرنا بالكمية. أما إذا سألت أيّ صديق هو الثالث فأنا أسأل عن مكان في الصف. سؤالان مختلفان: كم؟ وأيّ مكان؟",
          "Bonjour champion ! Voici une file de 5 amis. Si je demande combien d'amis il y a, la réponse est 5 : c'est la quantité. Mais si je demande quel ami est le troisième, je parle d'une place dans la file. Deux questions différentes : combien ? et quelle place ?"),
        line(5),
        F("5 friends  →  how many      3rd friend  →  which place"),
    ]),
    ("First, second, third", "الأول والثاني والثالث", "Premier, deuxième, troisième", "100", [
        line(5, hi=1, labels=True),
        line(5, hi=2, labels=True),
        line(5, hi=3, labels=True),
        T("We start at the START flag. The friend next to the flag is the first. Then the second, then the third, then the fourth and the fifth. The red circle shows the place we are talking about.",
          "نبدأ من علم البداية. الصديق الذي بجانب العلم هو الأول. ثم الثاني ثم الثالث ثم الرابع ثم الخامس. الدائرة الحمراء تُظهر المكان الذي نتحدث عنه.",
          "On commence au drapeau de DÉPART. L'ami à côté du drapeau est le premier, puis le deuxième, le troisième, le quatrième et le cinquième. Le cercle rouge montre la place dont on parle."),
        F("1st  first      2nd  second      3rd  third      4th  fourth      5th  fifth"),
    ]),
    ("The start matters", "نقطة البداية مهمة", "Le départ compte", "101", [
        line(5, hi=2, start="left", labels=True),
        line(5, hi=2, start="right", labels=True),
        T("Look carefully. It is the same row, but the START flag is on the other side. The friend who was fourth from the left is now second from the right. If we change the starting point or the direction, the place changes. That is why we always say where we start.",
          "انظر بانتباه. الصف نفسه لكن علم البداية في الجهة الأخرى. الصديق الذي كان الرابع من اليسار صار الثاني من اليمين. إذا غيّرنا نقطة البداية أو الاتجاه تغيّر المكان. لذلك نقول دائمًا من أين نبدأ.",
          "Regarde bien. C'est la même file, mais le drapeau est de l'autre côté. L'ami qui était quatrième en partant de la gauche est maintenant deuxième en partant de la droite. Si on change le départ ou le sens, la place change. On dit donc toujours d'où l'on part."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Cardinal numbers tell how many. Ordinal numbers tell the place in an order. Always find the starting point first, then count the places one by one.",
          "الأعداد الأصلية تخبر كم العدد، والأعداد الترتيبية تخبر المكان في الترتيب. نجد نقطة البداية أولًا ثم نعدّ الأماكن واحدًا واحدًا.",
          "Les nombres cardinaux disent combien. Les nombres ordinaux disent la place dans un ordre. On trouve d'abord le départ, puis on compte les places une à une."),
        F("FIND THE START → COUNT THE PLACES → NAME THE PLACE"),
    ]),
]

EXERCISES = [
    EX("1", "100", st("How many friends are in the row?", "كم صديقًا في الصف؟", "Combien d'amis y a-t-il dans la file ?"), [
        line(6),
        T("Count them one by one: 6 friends. This is a quantity, not a place.",
          "نعدّهم واحدًا واحدًا: 6 أصدقاء. هذه كمية وليست مكانًا.",
          "On les compte un à un : 6 amis. C'est une quantité, pas une place."),
    ]),
    EX("2", "100", st("Which friend is the second?", "أيّ صديق هو الثاني؟", "Quel ami est le deuxième ?"), [
        line(5, hi=2, labels=True),
        T("Start at the flag. The first is next to the flag, and the second is right after it: the red circle.",
          "نبدأ من العلم. الأول بجانب العلم والثاني بعده مباشرة: الدائرة الحمراء.",
          "On part du drapeau. Le premier est à côté, le deuxième juste après : le cercle rouge."),
    ]),
    EX("3", "100", st("Name the place of the red circle.", "سمِّ مكان الدائرة الحمراء.", "Nomme la place du cercle rouge."), [
        line(6, hi=4, labels=True),
        T("Count from the flag: first, second, third, fourth. It is the fourth.",
          "نعدّ من العلم: الأول والثاني والثالث والرابع. إنه الرابع.",
          "On compte depuis le drapeau : premier, deuxième, troisième, quatrième. C'est le quatrième."),
    ]),
    EX("4", "101", st("The flag is now on the right. Which place is the red circle?", "العلم الآن على اليمين. ما مكان الدائرة الحمراء؟", "Le drapeau est à droite. Quelle est la place du cercle rouge ?"), [
        line(5, hi=2, start="right", labels=True),
        T("Now we count from the right: first, second. The red circle is the second.",
          "الآن نعدّ من اليمين: الأول والثاني. الدائرة الحمراء هي الثانية.",
          "On compte maintenant depuis la droite : premier, deuxième. Le cercle rouge est le deuxième."),
    ]),
    EX("5", "101", st("Is the third from the left also the third from the right in a row of 5?", "هل الثالث من اليسار هو الثالث من اليمين في صف من 5؟", "Dans une file de 5, le troisième depuis la gauche est-il aussi le troisième depuis la droite ?"), [
        line(5, hi=3, start="left", labels=True),
        line(5, hi=3, start="right", labels=True),
        T("Yes, in a row of 5 the middle one is third from both sides. It does not work this way for the other places.",
          "نعم، في صف من 5 يكون الأوسط ثالثًا من الجهتين. ولا ينطبق هذا على الأماكن الأخرى.",
          "Oui, dans une file de 5 celui du milieu est troisième des deux côtés. Ce n'est pas vrai pour les autres places."),
    ]),
    EX("6", "101", st("Error check: a child says the row has 5 friends, so the red one is fifth. Is that right?", "تحقّق من الخطأ: قال طفل إن الصف فيه 5 أصدقاء فالأحمر هو الخامس. هل هذا صحيح؟", "Vérifie l'erreur : un enfant dit que la file a 5 amis, donc le rouge est le cinquième. Est-ce juste ?"), [
        line(5, hi=2, labels=True),
        T("No. The child mixed up quantity and place. The red circle is the second, even though there are 5 friends.",
          "لا. خلط الطفل بين الكمية والمكان. الدائرة الحمراء هي الثانية حتى لو كان في الصف 5 أصدقاء.",
          "Non. L'enfant a mélangé quantité et place. Le cercle rouge est le deuxième, même s'il y a 5 amis."),
    ]),
    EX("7", "102", st("Put the red circle at the fifth place.", "ضع الدائرة الحمراء في المكان الخامس.", "Place le cercle rouge à la cinquième place."), [
        line(7, hi=5, labels=True),
        T("Count five places from the flag: 1, 2, 3, 4, 5. The fifth circle is red.",
          "نعدّ خمسة أماكن من العلم: 1 و2 و3 و4 و5. الدائرة الخامسة هي الحمراء.",
          "On compte cinq places depuis le drapeau : 1, 2, 3, 4, 5. Le cinquième cercle est rouge."),
    ]),
    EX("8", "103", st("Final check: name the place of the red circle and say where counting begins.", "تقييم أخير: سمِّ مكان الدائرة الحمراء وقل من أين يبدأ العد.", "Évaluation : nomme la place du cercle rouge et dis où le compte commence."), [
        line(6, hi=3, labels=True),
        T("Counting begins at the green flag on the left. The red circle is the third.",
          "يبدأ العد من العلم الأخضر على اليسار. الدائرة الحمراء هي الثالثة.",
          "Le compte commence au drapeau vert à gauche. Le cercle rouge est le troisième."),
    ]),
]
