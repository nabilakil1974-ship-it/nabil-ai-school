"""Grade 1 Mathematics — Subtraction."""
from scripts.direct_lessons.common import T, F, EX, st, scene, jumps


def takeaway(n, k, tag="S"):
    """n counters in a row; the last k are crossed out (removed) and greyed; the rest stay coloured."""
    r, gap, x0 = 24, 62, 48
    svg, ids = "", []
    for i in range(n):
        x = x0 + i * gap
        gone = i >= n - k
        fill = "#e0e0e0" if gone else "#66bb6a"
        cross = (f'<line x1="{x-r}" y1="{150-r}" x2="{x+r}" y2="{150+r}" stroke="#e53935" stroke-width="6"/>'
                 f'<line x1="{x-r}" y1="{150+r}" x2="{x+r}" y2="{150-r}" stroke="#e53935" stroke-width="6"/>') if gone else ""
        svg += f'<g id="{tag}{i}"><circle cx="{x}" cy="150" r="{r}" fill="{fill}" stroke="#0b3d5c" stroke-width="3"/>{cross}</g>'
        ids.append(f"{tag}{i}")
    return scene(svg, ids)


LESSON_ID = "G01-MATH-EN-048"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Subtraction", "ar": "الطرح", "fr": "La soustraction"}

THEORY = [
    ("Start, take away, what remains", "نبدأ ونأخذ وننظر ما يبقى", "Départ, retrait, reste", "122", [
        takeaway(7, 0),
        T("Hello, champion! We start with 7 counters. This is the starting quantity.",
          "مرحبًا يا بطل! نبدأ بـ7 قطع. هذه هي الكمية الأولى.",
          "Bonjour champion ! On part de 7 jetons. C'est la quantité de départ."),
        takeaway(7, 3),
        T("Now we take away 3. The crossed counters are removed, and we do not count them any more. How many remain? We count only the green ones: 4. So from 7, taking away 3 leaves 4.",
          "الآن نأخذ 3 قطع. القطع المشطوبة أُزيلت ولا نعدّها بعد الآن. كم بقي؟ نعدّ الخضراء فقط: 4. إذن من 7 إذا أخذنا 3 يبقى 4.",
          "Maintenant on retire 3. Les jetons barrés sont enlevés, on ne les compte plus. Combien reste-t-il ? On ne compte que les verts : 4. De 7, si on retire 3, il reste 4."),
        F("7 take away 3 leaves 4"),
    ]),
    ("Going backward on the path", "نرجع إلى الوراء على المسار", "Reculer sur la droite", "123", [
        jumps(7, 3, hi=10, back=True),
        T("We can also show it on the number path: start at 7 and jump back 3 times: 6, 5, 4. We land on 4. The same answer!",
          "ونستطيع أن نبيّن ذلك على مسار الأعداد: نبدأ من 7 ونقفز إلى الوراء 3 مرات: 6، 5، 4. نصل إلى 4. الجواب نفسه!",
          "On peut aussi le montrer sur la droite : on part de 7 et on recule de 3 sauts : 6, 5, 4. On arrive à 4. Même réponse !"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("In subtraction we start with a quantity, take a part away, and find what remains. The removed objects are not counted in the remainder.",
          "في الطرح نبدأ بكمية ونأخذ منها جزءًا ونجد ما يبقى. الأشياء المأخوذة لا تدخل في العدّ الباقي.",
          "En soustraction, on part d'une quantité, on retire une partie et on trouve ce qui reste. Les objets retirés ne sont pas comptés dans le reste."),
        F("START → TAKE AWAY → COUNT WHAT REMAINS"),
    ]),
]

EXERCISES = [
    EX("1", "122", st("There are 5 counters. Take away 2. How many remain?", "هناك 5 قطع. خذ قطعتين. كم يبقى؟", "Il y a 5 jetons. Retire 2. Combien reste-t-il ?"), [
        takeaway(5, 2),
        T("Count the green ones: 3.", "نعدّ الخضراء: 3.", "On compte les verts : 3."),
    ]),
    EX("2", "122", st("There are 8 counters. Take away 4.", "هناك 8 قطع. خذ 4.", "Il y a 8 jetons. Retire 4."), [
        takeaway(8, 4),
        T("4 remain.", "يبقى 4.", "Il en reste 4."),
    ]),
    EX("3", "122", st("There are 6 counters. Take away all of them.", "هناك 6 قطع. خذها كلها.", "Il y a 6 jetons. Retire-les tous."), [
        takeaway(6, 6),
        T("Nothing remains: 0.", "لا يبقى شيء: 0.", "Il ne reste rien : 0."),
    ]),
    EX("4", "123", st("Start at 9 and jump back 2.", "ابدأ من 9 وارجع قفزتين.", "Pars de 9 et recule de 2."), [
        jumps(9, 2, hi=10, back=True),
        T("8, then 7. We land on 7.", "8 ثم 7. نصل إلى 7.", "8, puis 7. On arrive à 7."),
    ]),
    EX("5", "123", st("Start at 5 and take away 5.", "ابدأ من 5 وخذ 5.", "Pars de 5 et retire 5."), [
        jumps(5, 5, hi=10, back=True),
        T("Back to 0. If we take away everything, nothing is left.", "نعود إلى 0. إذا أخذنا كل شيء لا يبقى شيء.", "On revient à 0. Si on retire tout, il ne reste rien."),
    ]),
    EX("6", "123", st("Error check: 7 counters, 3 removed; a child counts all 7 again. What is wrong?", "تحقّق من الخطأ: 7 قطع أُخذ منها 3 وعدّ الطفل الـ7 كلها. ما الخطأ؟", "Vérifie l'erreur : 7 jetons, 3 retirés ; l'enfant compte encore les 7. Où est l'erreur ?"), [
        takeaway(7, 3),
        T("He counted the removed ones too. Only the 4 remaining ones must be counted.", "عدّ القطع المأخوذة أيضًا. يجب عدّ الأربع الباقية فقط.", "Il a compté aussi les jetons retirés. On ne compte que les 4 qui restent."),
    ]),
    EX("7", "123", st("Challenge: 10 counters, take away 6.", "تحدٍّ: 10 قطع نأخذ منها 6.", "Défi : 10 jetons, on retire 6."), [
        takeaway(10, 6),
        T("4 remain.", "يبقى 4.", "Il en reste 4."),
    ]),
    EX("8", "123", st("Final check: model 6 take away 2 and say what remains.", "تقييم أخير: مثّل 6 نأخذ منها 2 وقل ما يبقى.", "Évaluation : modélise 6 moins 2 et dis ce qui reste."), [
        takeaway(6, 2),
        T("6 counters, 2 removed, 4 remain.", "6 قطع أُخذت منها 2 فيبقى 4.", "6 jetons, 2 retirés, il en reste 4."),
    ]),
]
