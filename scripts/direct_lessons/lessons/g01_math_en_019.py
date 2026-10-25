"""Grade 1 Mathematics — Grouping."""
from scripts.direct_lessons.common import T, F, EX, st, scene, _shape

LESSON_ID = "G01-MATH-EN-019"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Grouping", "ar": "التجميع", "fr": "Regrouper"}


def grouped(n, k, color="#e53935", tag="g", scattered=False, r=22):
    """n counters; boxes of k; leftovers outside."""
    svg, ids = "", []
    if scattered:
        pos = [(90, 90), (300, 150), (520, 80), (170, 300), (420, 260), (570, 350), (60, 200), (360, 60), (250, 390), (480, 160)]
        for i in range(n):
            x, y = pos[i % len(pos)]
            sid = f"{tag}{i}"; svg += _shape("circle", x, y, r, color, sid); ids.append(sid)
        return scene(svg, ids)
    full, rest = divmod(n, k)
    boxes = full + (1 if rest else 0)
    bw = k * 2 * r + (k + 1) * 10
    gap = 24
    total_w = boxes * bw + (boxes - 1) * gap
    x0 = (660 - total_w) / 2
    idx = 0
    for b in range(boxes):
        bx = x0 + b * (bw + gap)
        cnt = k if b < full else rest
        dash = "" if b < full else ' stroke-dasharray="8 6"'
        bid = f"{tag}box{b}"
        svg += (f'<rect id="{bid}" x="{bx}" y="150" width="{bw}" height="{2*r+30}" rx="14" fill="#fff8e1" '
                f'stroke="#0b3d5c" stroke-width="3"{dash}/>')
        ids.append(bid)
        for j in range(cnt):
            sid = f"{tag}{idx}"; idx += 1
            svg += _shape("circle", bx + 10 + r + j * (2 * r + 10), 150 + r + 15, r, color, sid); ids.append(sid)
    return scene(svg, ids)


THEORY = [
    ("Grouping organizes; it does not change the total", "التجميع ينظّم ولا يغيّر المجموع", "Regrouper organise, sans changer le total", "54", [
        T("Hello! Look at these things. When they are scattered, we might make a mistake counting. What if we arrange them in a way that helps? Today we learn grouping: organizing objects into groups by a clear rule. But when we organize, the quantity must not change.",
          "مرحبًا! انظر إلى هذه الأشياء. عندما تكون مبعثرة قد نخطئ في العدّ. ماذا لو رتّبناها بطريقة تساعدنا؟ اليوم نتعلّم التجميع: ننظّم الأشياء في مجموعات حسب قاعدة واضحة. لكن عندما ننظّم يجب ألّا تتغير الكمية.",
          "Bonjour ! Regarde ces objets. Éparpillés, on peut se tromper en comptant. Et si on les rangeait pour mieux compter ? Aujourd'hui : regrouper, c'est organiser des objets en groupes selon une règle claire. Mais en rangeant, la quantité ne doit pas changer."),
        grouped(6, 6, scattered=True),
        T("Count them before grouping: six. Now we arrange them in groups, without adding or removing anything.",
          "نعدّها قبل التجميع: ستة. الآن نرتّبها في مجموعات دون أن نضيف أو نحذف شيئًا.",
          "On les compte avant : six. Maintenant on les range en groupes, sans rien ajouter ni enlever."),
        grouped(6, 2),
        T("Count again: six. What changed? The arrangement. What did not change? The number.",
          "نعدّ مرة أخرى: ستة. ما الذي تغيّر؟ الترتيب. وما الذي لم يتغيّر؟ العدد.",
          "On recompte : six. Qu'est-ce qui a changé ? Le rangement. Qu'est-ce qui n'a pas changé ? Le nombre."),
    ]),
    ("Every complete group follows the same rule", "كل مجموعة كاملة تتبع القاعدة نفسها", "Chaque groupe complet suit la même règle", "54", [
        grouped(5, 2),
        T("If the rule says 2 in each group, every complete group must have 2. The first two groups are complete. The last one has a remaining object.",
          "إذا قالت القاعدة 2 في كل مجموعة، فكل مجموعة كاملة يجب أن يكون فيها 2. أول مجموعتين كاملتان، والأخيرة فيها شيء متبقٍّ.",
          "Si la règle dit 2 dans chaque groupe, chaque groupe complet doit en avoir 2. Les deux premiers sont complets. Le dernier a un objet restant."),
    ]),
    ("Remaining objects still belong to the total", "الأشياء المتبقية تبقى من المجموع", "Les objets restants font partie du total", "55", [
        grouped(7, 2),
        T("Seven counters with the rule 2 in each group: three complete groups and one remaining. We do not throw away the remaining object. It is still part of the collection. Grouping describes organization; it does not cancel objects.",
          "سبعة عدّادات والقاعدة 2 في كل مجموعة: ثلاث مجموعات كاملة وواحد متبقٍّ. لا نرمي الشيء المتبقي. إنه ما زال جزءًا من المجموعة. التجميع يصف التنظيم ولا يلغي الأشياء.",
          "Sept jetons avec la règle 2 par groupe : trois groupes complets et un restant. On ne jette pas l'objet restant. Il fait toujours partie de la collection. Regrouper décrit l'organisation, ça n'efface pas d'objets."),
        F("3 groups + 1 remaining = 7"),
    ]),
    ("Grouping can make counting easier", "التجميع قد يسهّل العدّ", "Regrouper peut faciliter le comptage", "55", [
        grouped(8, 8, scattered=True),
        T("Try counting these scattered ones. Now we organize them.",
          "جرّب عدّ هذه المبعثرة. الآن ننظّمها.",
          "Essaie de compter ceux-ci éparpillés. Maintenant on les organise."),
        grouped(8, 4),
        T("Which picture is easier to check? The grouped one. Grouping lowers the chance of forgetting an object or counting it twice.",
          "أي صورة أسهل في التحقق؟ المجمَّعة. التجميع يقلّل احتمال نسيان شيء أو عدّه مرتين.",
          "Quelle image est plus facile à vérifier ? La regroupée. Regrouper réduit le risque d'oublier un objet ou de le compter deux fois."),
    ]),
    ("Different organizations, the same quantity", "تنظيمات مختلفة والكمية نفسها", "Des organisations différentes, la même quantité", "55", [
        grouped(8, 2),
        grouped(8, 4),
        T("The same quantity can be arranged in different ways. As long as we did not add or remove objects, the total is the same. If we doubt, we count all the objects.",
          "يمكن ترتيب الكمية نفسها بطرق مختلفة. ما دمنا لم نضف أو نحذف أشياء فالمجموع نفسه. وإذا شككنا نعدّ كل الأشياء.",
          "La même quantité peut être rangée de plusieurs façons. Tant qu'on n'ajoute ni n'enlève rien, le total est le même. En cas de doute, on compte tous les objets."),
    ]),
    ("Explain your grouping", "نشرح تجميعنا", "Expliquer ton regroupement", "55", [
        T("Say: what is the rule? How many complete groups? Is anything remaining? What is the total? Then your grouping is clear to someone else.",
          "قل: ما القاعدة؟ كم مجموعة كاملة؟ هل يوجد متبقٍّ؟ ما المجموع؟ هكذا يكون تجميعك واضحًا لشخص آخر.",
          "Dis : quelle est la règle ? Combien de groupes complets ? Reste-t-il quelque chose ? Quel est le total ? Alors ton regroupement est clair pour quelqu'un d'autre."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Grouping helps us organize a collection. Each group follows a rule, we do not forget the remaining objects, and most important, grouping does not change the total.",
          "التجميع يساعدنا على تنظيم المجموعة. كل مجموعة تتبع قاعدة، ولا ننسى المتبقي، والأهم أن التجميع لا يغيّر المجموع.",
          "Regrouper aide à organiser une collection. Chaque groupe suit une règle, on n'oublie pas les restants et surtout, regrouper ne change pas le total."),
        F("COUNT → READ THE RULE → GROUP EACH OBJECT ONCE → FIND REMAINING → RECOUNT → EXPLAIN"),
    ]),
]

EXERCISES = [
    EX("1", "54", st("Make groups of 2 from 8 counters without changing the total.", "كوّن مجموعات من 2 من 8 عدّادات دون أن يتغير المجموع.", "Fais des groupes de 2 avec 8 jetons sans changer le total."), [
        grouped(8, 2),
        T("Is every complete group made of 2? Was anything lost? Was anything counted twice? The total after grouping is still 8.",
          "هل كل مجموعة كاملة من 2؟ هل ضاع شيء؟ هل عُدّ شيء مرتين؟ المجموع بعد التجميع ما زال 8.",
          "Chaque groupe complet a-t-il 2 ? Y a-t-il une perte ? Un objet compté deux fois ? Le total après regroupement est toujours 8."),
        F("organization changed; total stayed 8"),
    ]),
    EX("2", "54", st("7 counters, the rule is 2 in each group. How many complete groups? How many remaining?", "7 عدّادات والقاعدة 2 في كل مجموعة. كم مجموعة كاملة؟ كم متبقٍّ؟", "7 jetons, la règle est 2 par groupe. Combien de groupes complets ? Combien de restants ?"), [
        grouped(7, 2),
        F("3 complete groups      1 remaining"),
    ]),
    EX("3", "55", st("Count the grouped objects and the remaining one. What is the total?", "عدّ الأشياء المجمَّعة والمتبقية. ما المجموع؟", "Compte les objets groupés et le restant. Quel est le total ?"), [
        grouped(9, 4),
        T("Two groups of four make eight, and one remaining makes nine. An object outside the group has not disappeared, so it must be in the total.",
          "مجموعتان من أربعة تعطيان ثمانية، والمتبقي يجعلها تسعة. الشيء خارج المجموعة لم يختفِ، فيجب أن يدخل في المجموع.",
          "Deux groupes de quatre font huit, et le restant fait neuf. Un objet hors du groupe n'a pas disparu : il compte dans le total."),
        F("4 + 4 + 1 = 9"),
    ]),
    EX("4", "55", st("Count 8 scattered objects, then organize them and count again. Is the total the same?", "عدّ 8 أشياء مبعثرة ثم نظّمها وعدّها مرة أخرى. هل المجموع نفسه؟", "Compte 8 objets éparpillés, puis range-les et recompte. Le total est-il le même ?"), [
        grouped(8, 8, scattered=True),
        grouped(8, 4),
        T("Yes, the total is the same: 8. The grouped arrangement is easier to check.",
          "نعم، المجموع نفسه: 8. والترتيب المجمَّع أسهل في التحقق.",
          "Oui, le total est le même : 8. Le rangement en groupes est plus facile à vérifier."),
    ]),
    EX("5", "55", st("The same 6 objects are organized in two ways. Did the total change?", "الأشياء الستة نفسها نُظّمت بطريقتين. هل تغيّر المجموع؟", "Les mêmes 6 objets sont rangés de deux façons. Le total a-t-il changé ?"), [
        grouped(6, 2),
        grouped(6, 3),
        T("No. Prove it by recounting: six both times.",
          "لا. نثبت بإعادة العدّ: ستة في المرتين.",
          "Non. On le prouve en recomptant : six les deux fois."),
    ]),
    EX("6", "55", st("Error detective: one counter was drawn inside two groups. What is wrong?", "المحقق: رُسم عدّاد داخل مجموعتين. ما الخطأ؟", "Détective : un jeton est dessiné dans deux groupes. Qu'est-ce qui ne va pas ?"), [
        T("The same object was counted twice. Each object belongs to one group only.",
          "عُدّ الشيء نفسه مرتين. كل شيء ينتمي إلى مجموعة واحدة فقط.",
          "Le même objet a été compté deux fois. Chaque objet appartient à un seul groupe."),
        F("each object once"),
    ]),
    EX("7", "55", st("Challenge: choose an organization that helps a friend count a scattered collection, then explain the rule.", "تحدٍّ: اختر تنظيمًا يساعد صديقك على عدّ مجموعة مبعثرة ثم اشرح القاعدة.", "Défi : choisis un rangement qui aide un ami à compter une collection éparpillée, puis explique la règle."), [
        grouped(10, 10, scattered=True),
        grouped(10, 5),
        T("The rule: 5 in each group. Two complete groups, nothing remaining, total 10. If your friend can rebuild the same grouping from your words, your explanation is clear.",
          "القاعدة: 5 في كل مجموعة. مجموعتان كاملتان ولا شيء متبقٍّ والمجموع 10. إذا استطاع صديقك إعادة التجميع نفسه من كلامك فشرحك واضح.",
          "La règle : 5 par groupe. Deux groupes complets, rien de restant, total 10. Si ton ami peut refaire le même regroupement avec tes mots, ton explication est claire."),
    ]),
    EX("8", "55", st("Final check: why does grouping not change the quantity?", "تقييم أخير: لماذا لا يغيّر التجميع الكمية؟", "Évaluation : pourquoi regrouper ne change-t-il pas la quantité ?"), [
        grouped(7, 3),
        T("Because grouping changes only the organization. We did not add objects and we did not remove any.",
          "لأن التجميع يغيّر التنظيم فقط. لم نضف أشياء ولم نحذف أي شيء.",
          "Parce que regrouper ne change que l'organisation. On n'a ajouté ni enlevé aucun objet."),
        F("3 + 3 + 1 = 7"),
    ]),
]
