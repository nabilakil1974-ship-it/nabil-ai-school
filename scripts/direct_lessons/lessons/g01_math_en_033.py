"""Grade 1 Mathematics — Comparing lengths."""
from scripts.direct_lessons.common import T, F, EX, st, strips

LESSON_ID = "G01-MATH-EN-033"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Comparing lengths", "ar": "مقارنة الأطوال", "fr": "Comparer des longueurs"}
R, B, G = "#e53935", "#1e63d6", "#43a047"

THEORY = [
    ("Align the starting points", "نضبط نقطتي البداية", "Aligner les points de départ", "86", [
        T("Hello! Today we compare lengths. But be careful: if we put two objects with different starts, our eyes can be fooled. Which is longer? Do not answer from the end points alone. First we must make a fair comparison.",
          "مرحبًا! اليوم نقارن الأطوال. لكن انتبه: إذا وضعنا شيئين ببدايتين مختلفتين فقد تُخدع عيوننا. أيهما أطول؟ لا تجب من نقطتي النهاية وحدهما. أولًا يجب أن نجري مقارنة عادلة.",
          "Bonjour ! Aujourd'hui on compare des longueurs. Mais attention : si on place deux objets avec des départs différents, nos yeux peuvent être trompés. Lequel est le plus long ? Ne réponds pas d'après les bouts seulement. D'abord, il faut une comparaison équitable."),
        strips([("A", 0, 5, R), ("B", 3, 4, B)]),
        T("We slide them so that they start from the same place.",
          "نسحبهما حتى يبدآ من المكان نفسه.",
          "On les glisse pour qu'ils partent du même endroit."),
        strips([("A", 0, 5, R), ("B", 0, 4, B)], ref=0),
        T("Now we can compare the end points. Which one extends farther? A. The one that extends farther from the same start is longer, and the other is shorter.",
          "الآن نستطيع مقارنة نقطتي النهاية. أيهما يمتدّ أبعد؟ A. الذي يمتدّ أبعد من البداية نفسها هو الأطول، والآخر هو الأقصر.",
          "Maintenant on peut comparer les bouts. Lequel va plus loin ? A. Celui qui va plus loin à partir du même départ est le plus long, l'autre est le plus court."),
    ]),
    ("Longer, shorter or equal", "أطول أو أقصر أو مساوٍ", "Plus long, plus court ou égal", "86", [
        strips([("A", 0, 5, R), ("B", 0, 3, B)], ref=0),
        strips([("A", 0, 4, R), ("B", 0, 4, B)], ref=0),
        T("There are three possible answers: longer, shorter, equal. If strip A extends farther, A is longer and B is shorter. If the end points match after the same start, the lengths are equal. Equal does not mean the same color or the same place; it means the same length.",
          "هناك ثلاثة أجوبة ممكنة: أطول، أقصر، مساوٍ. إذا امتد الشريط A أبعد فهو الأطول وB أقصر. وإذا تطابقت نقطتا النهاية بعد البداية نفسها فالطولان متساويان. المساواة لا تعني اللون نفسه أو المكان نفسه، بل الطول نفسه.",
          "Il y a trois réponses possibles : plus long, plus court, égal. Si la bande A va plus loin, A est plus longue et B plus courte. Si les bouts coïncident à partir du même départ, les longueurs sont égales. Égal ne veut pas dire même couleur ou même place, mais même longueur."),
    ]),
    ("Different starts can fool the eye", "البدايات المختلفة تخدع العين", "Des départs différents trompent l'œil", "87", [
        strips([("A", 0, 5, R), ("B", 3, 3, B)]),
        T("This is tricky. One end point is farther to the right, but its start is also farther to the right. Can we say it is longer right away? No. The end points alone are not enough if the starts are different.",
          "هذا مخادع. نقطة نهاية أبعد إلى اليمين، لكن بدايتها أيضًا أبعد إلى اليمين. هل نقول إنه أطول فورًا؟ لا. نقطتا النهاية وحدهما لا تكفيان إذا اختلفت البدايتان.",
          "C'est piégeux. Un bout est plus à droite, mais son départ aussi. Peut-on dire qu'elle est plus longue tout de suite ? Non. Les bouts seuls ne suffisent pas si les départs diffèrent."),
        strips([("A", 0, 5, R), ("B", 0, 3, B)], ref=0),
        T("After aligning, the truth appears.",
          "بعد الضبط تظهر الحقيقة.",
          "Après l'alignement, la vérité apparaît."),
    ]),
    ("Turning does not change the length", "التدوير لا يغيّر الطول", "Tourner ne change pas la longueur", "87", [
        strips([("A", 0, 5, R), ("B", 0, 5, B)], rot={1: 12}),
        T("If I turn a strip, did its length change? No. Rotation changes the direction, not the length. To compare, we turn it back, or we use a common reference, without changing the real length.",
          "إذا دوّرت شريطًا فهل تغيّر طوله؟ لا. التدوير يغيّر الاتجاه لا الطول. وللمقارنة نعيده كما كان أو نستعمل مرجعًا مشتركًا دون تغيير الطول الحقيقي.",
          "Si je tourne une bande, sa longueur a-t-elle changé ? Non. Tourner change la direction, pas la longueur. Pour comparer, on la remet droite ou on utilise une référence commune, sans changer la vraie longueur."),
        strips([("A", 0, 5, R), ("B", 0, 5, B)], ref=0),
        F("equal length"),
    ]),
    ("A common reference", "مرجع مشترك", "Une référence commune", "87", [
        strips([("ref", 0, 4, G), ("A", 0, 5, R), ("B", 0, 3, B)], ref=0),
        T("Sometimes we cannot put two objects on top of each other. We use the same reference strip for both. What matters is that the reference is the same for the two. Then the comparison stays fair: A goes past the reference, B stays short of it.",
          "أحيانًا لا نستطيع وضع شيئين فوق بعضهما. نستعمل شريط مرجع واحدًا للاثنين. المهم أن يكون المرجع نفسه للاثنين. عندها تبقى المقارنة عادلة: A يتجاوز المرجع وB لا يصل إليه.",
          "Parfois on ne peut pas poser deux objets l'un sur l'autre. On utilise la même bande de référence pour les deux. Ce qui compte, c'est que la référence soit la même. La comparaison reste équitable : A dépasse la référence, B reste en deçà."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("When we compare length, we do not look at one end point alone. We use the same start, look at the end points, say longer, shorter or equal, and check. If we cannot align directly, we use the same reference.",
          "عندما نقارن الطول لا ننظر إلى نقطة نهاية وحدها. نستعمل البداية نفسها وننظر إلى نقطتي النهاية ونقول أطول أو أقصر أو مساوٍ ونتحقق. وإذا لم نستطع الضبط مباشرة نستعمل المرجع نفسه.",
          "Pour comparer des longueurs, on ne regarde pas un seul bout. On prend le même départ, on regarde les bouts, on dit plus long, plus court ou égal, et on vérifie. Si on ne peut pas aligner directement, on utilise la même référence."),
        F("SAME START → LOOK AT ENDPOINTS → LONGER / SHORTER / EQUAL → CHECK"),
    ]),
]

EXERCISES = [
    EX("1", "86", st("Two strips are not aligned. Align them first, then say which is longer.", "الشريطان غير مضبوطين. اضبطهما أولًا ثم قل أيهما أطول.", "Deux bandes ne sont pas alignées. Aligne-les d'abord, puis dis laquelle est plus longue."), [
        strips([("A", 1, 4, R), ("B", 3, 3, B)]),
        strips([("A", 0, 4, R), ("B", 0, 3, B)], ref=0),
        T("A is longer. You made a fair comparison. Check that the two starts are in the same place.",
          "A أطول. أجريت مقارنة عادلة. تأكد أن البدايتين في المكان نفسه.",
          "A est plus longue. Tu as fait une comparaison équitable. Vérifie que les deux départs sont au même endroit."),
    ]),
    EX("2", "86", st("After alignment, choose the relation: A longer, equal, or A shorter.", "بعد الضبط اختر العلاقة: A أطول أو مساوٍ أو A أقصر.", "Après alignement, choisis la relation : A plus longue, égal, ou A plus courte."), [
        strips([("A", 0, 5, R), ("B", 0, 3, B)], ref=0),
        strips([("A", 0, 4, R), ("B", 0, 4, B)], ref=0),
        strips([("A", 0, 2, R), ("B", 0, 4, B)], ref=0),
        F("A longer      equal      A shorter"),
        T("The answer always comes after alignment.",
          "الجواب يأتي دائمًا بعد الضبط.",
          "La réponse vient toujours après l'alignement."),
    ]),
    EX("3", "87", st("Do not trust the position: slide the two strips to the same start, then decide.", "لا تثق بالموضع: اسحب الشريطين إلى البداية نفسها ثم قرّر.", "Ne te fie pas à la position : glisse les deux bandes vers le même départ, puis décide."), [
        strips([("A", 0, 4, R), ("B", 3, 3, B)]),
        T("Stop a moment. We need a fair start first.",
          "قف قليلًا. نحتاج إلى بداية عادلة أولًا.",
          "Arrête-toi un instant. Il faut d'abord un départ équitable."),
        strips([("A", 0, 4, R), ("B", 0, 3, B)], ref=0),
    ]),
    EX("4", "87", st("Two equal strips, one of them turned. Did the turned one become shorter?", "شريطان متساويان وأحدهما مدوَّر. هل صار المدوَّر أقصر؟", "Deux bandes égales, l'une est tournée. La tournée est-elle devenue plus courte ?"), [
        strips([("A", 0, 5, R), ("B", 0, 5, B)], rot={1: 12}),
        T("No. Let us turn it back and align: the ends match. Equal length.",
          "لا. لنُعدها ونضبطها: تتطابق النهايتان. الطولان متساويان.",
          "Non. Remettons-la droite et alignons : les bouts coïncident. Longueurs égales."),
        strips([("A", 0, 5, R), ("B", 0, 5, B)], ref=0),
    ]),
    EX("5", "87", st("Compare A and B using the same reference.", "قارن A وB باستعمال المرجع نفسه.", "Compare A et B avec la même référence."), [
        strips([("ref", 0, 4, G), ("A", 0, 3, R), ("B", 0, 5, B)], ref=0),
        T("Who goes past the reference more? Who is shorter? Or are they the same? Is the reference the same for both? If so, the comparison is honest.",
          "من يتجاوز المرجع أكثر؟ ومن أقصر؟ أم هما متساويان؟ هل المرجع نفسه للاثنين؟ إذا كان كذلك فالمقارنة صادقة.",
          "Qui dépasse le plus la référence ? Qui est plus court ? Ou sont-elles pareilles ? La référence est-elle la même ? Alors la comparaison est honnête."),
    ]),
    EX("6", "87", st("Error detective: “B is longer because its end point is farther to the right.” Is that reason enough?", "المحقق: «B أطول لأن نقطة نهايتها أبعد إلى اليمين». هل هذا السبب كافٍ؟", "Détective : « B est plus longue parce que son bout est plus à droite ». Est-ce une raison suffisante ?"), [
        strips([("A", 0, 5, R), ("B", 3, 4, B)]),
        T("No. The starts are different. Align first.",
          "لا. البدايتان مختلفتان. نضبط أولًا.",
          "Non. Les départs sont différents. On aligne d'abord."),
        strips([("A", 0, 5, R), ("B", 0, 4, B)], ref=0),
        T("Position on the screen is not length.",
          "الموضع على الشاشة ليس طولًا.",
          "La position à l'écran n'est pas la longueur."),
    ]),
    EX("7", "87", st("Challenge: three strips A, B, C. After aligning, A and C end together and B goes farther. Which is longest? Which are equal? Compare A with B.", "تحدٍّ: ثلاثة أشرطة A وB وC. بعد الضبط ينتهي A وC معًا ويمتدّ B أبعد. أيها الأطول؟ وأيها متساويان؟ قارن A مع B.", "Défi : trois bandes A, B, C. Après alignement, A et C finissent ensemble et B va plus loin. Laquelle est la plus longue ? Lesquelles sont égales ? Compare A et B."), [
        strips([("A", 0, 4, R), ("B", 0, 6, B), ("C", 0, 4, G)], ref=0),
        F("longest: B      equal: A and C      A is shorter than B"),
    ]),
    EX("8", "87", st("Final check: why do we align the starts?", "تقييم أخير: لماذا نضبط البدايات؟", "Évaluation : pourquoi aligne-t-on les départs ?"), [
        strips([("A", 0, 5, R), ("B", 0, 3, B)], ref=0),
        T("So that we compare fairly, and the position does not fool us.",
          "حتى نقارن بعدل ولا يخدعنا الموضع.",
          "Pour comparer équitablement et ne pas être trompé par la position."),
    ]),
]
