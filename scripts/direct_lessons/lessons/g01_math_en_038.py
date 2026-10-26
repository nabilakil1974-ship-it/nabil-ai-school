"""Grade 1 Mathematics — Measure of lengths."""
from scripts.direct_lessons.common import T, F, EX, st, scene


def chain(n, obj=None, tag="M", unit=70, mode="ok"):
    """Object bar of `obj` units (default n) and a row of n numbered equal units placed end-to-end.
    mode: ok | gap (gaps between units) | over (overlaps)."""
    obj = obj if obj is not None else n
    x0 = 40
    svg = (f'<g id="{tag}o"><rect x="{x0}" y="50" width="{obj*unit}" height="44" rx="8" fill="#ffd54f" stroke="#0b3d5c" stroke-width="3"/>'
           f'<text x="{x0}" y="40" font-size="24" font-weight="700" fill="#0b3d5c" font-family="sans-serif">▼</text>'
           f'<text x="{x0+obj*unit}" y="40" font-size="24" font-weight="700" fill="#0b3d5c" font-family="sans-serif" text-anchor="end">▼</text></g>')
    ids = [tag + "o"]
    step = {"ok": unit, "gap": unit + 14, "over": unit - 16}[mode]
    for i in range(n):
        x = x0 + i * step
        svg += (f'<g id="{tag}{i}"><rect x="{x}" y="130" width="{unit}" height="44" rx="6" fill="#81d4fa" stroke="#0b3d5c" stroke-width="3"/>'
                f'<text x="{x+unit/2}" y="162" font-size="26" font-weight="700" text-anchor="middle" fill="#0b3d5c" font-family="sans-serif">{i+1}</text></g>')
        ids.append(f"{tag}{i}")
    return scene(svg, ids)


LESSON_ID = "G01-MATH-EN-038"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "Measure of lengths", "ar": "قياس الأطوال", "fr": "Mesurer des longueurs"}

THEORY = [
    ("How long is it?", "ما طول هذا الشيء؟", "Quelle est sa longueur ?", "98", [
        T("Hello, champion! Comparing two strips directly is easy, but what if we want to say how long one object is? We need a small measuring unit, like a little block. We place copies of the same block, one after another, from one end of the object to the other, and we count them.",
          "مرحبًا يا بطل! مقارنة شريطين مباشرة سهلة، لكن ماذا لو أردنا أن نقول كم طول شيء واحد؟ نحتاج إلى وحدة قياس صغيرة مثل قالب صغير. نضع نسخًا من القالب نفسه واحدًا بعد الآخر من طرف الشيء إلى طرفه الآخر ثم نعدّها.",
          "Bonjour champion ! Comparer deux bandes est facile, mais comment dire la longueur d'un seul objet ? Il faut une petite unité, comme un petit bloc. On place des copies du même bloc, l'une après l'autre, d'un bout à l'autre de l'objet, puis on les compte."),
        chain(5),
        T("The yellow bar is covered by 5 equal blocks, so its length is 5 blocks.",
          "الشريط الأصفر مغطّى بـ5 قوالب متساوية، إذن طوله 5 قوالب.",
          "La bande jaune est couverte par 5 blocs égaux : sa longueur est de 5 blocs."),
    ]),
    ("Start at one end and leave no gaps", "نبدأ من الطرف ولا نترك فراغات", "On commence au bout, sans trous", "98", [
        chain(4, mode="gap"),
        chain(4, mode="over"),
        chain(4),
        T("Look at the three rows. In the first there are gaps between the blocks. In the second the blocks overlap. Both give an unreliable result. In the third the blocks touch exactly end to end, so we can trust the count: 4 blocks.",
          "انظر إلى الصفوف الثلاثة. في الأول فراغات بين القوالب. وفي الثاني تتراكب القوالب. كلاهما يعطي نتيجة غير موثوقة. وفي الثالث تتلامس القوالب تمامًا طرفًا بطرف، فنثق بالعدد: 4 قوالب.",
          "Regarde les trois rangées. Dans la première, il y a des trous. Dans la deuxième, les blocs se chevauchent. Ces deux mesures ne sont pas fiables. Dans la troisième, les blocs se touchent exactement bout à bout : on peut se fier au compte, 4 blocs."),
    ]),
    ("Always the same unit", "الوحدة نفسها دائمًا", "Toujours la même unité", "99", [
        chain(3),
        chain(6),
        T("If I measure one bar with big blocks and another with small blocks, I cannot compare the numbers fairly. To compare lengths we must use the same unit. Here both use the same block: 3 blocks is shorter than 6 blocks.",
          "إذا قست شريطًا بقوالب كبيرة وآخر بقوالب صغيرة فلا أستطيع مقارنة العددين بإنصاف. لمقارنة الأطوال يجب أن نستعمل الوحدة نفسها. هنا استعملنا القالب نفسه: 3 قوالب أقصر من 6 قوالب.",
          "Si je mesure une bande avec de gros blocs et une autre avec de petits blocs, je ne peux pas comparer équitablement. Pour comparer, on utilise la même unité. Ici, c'est le même bloc : 3 blocs est plus court que 6 blocs."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("To measure a length: choose one unit, begin at one end, repeat the same unit with no gaps and no overlaps, and count how many units fit up to the other end. We can compare measurements only when we use the same unit.",
          "لقياس طول: نختار وحدة واحدة، ونبدأ من طرف، ونكرر الوحدة نفسها دون فراغات ودون تراكب، ونعدّ كم وحدة تصل إلى الطرف الآخر. ولا نقارن القياسات إلا إذا استعملنا الوحدة نفسها.",
          "Pour mesurer une longueur : choisir une unité, commencer à un bout, répéter la même unité sans trous ni chevauchements, et compter jusqu'à l'autre bout. On ne compare que des mesures faites avec la même unité."),
        F("ONE UNIT → START AT THE END → NO GAPS, NO OVERLAPS → COUNT"),
    ]),
]

EXERCISES = [
    EX("1", "98", st("Measure the yellow bar with the blocks.", "قِس الشريط الأصفر بالقوالب.", "Mesure la bande jaune avec les blocs."), [
        chain(6),
        T("The blocks cover the bar exactly, from one end to the other. Count them: 6 blocks.",
          "تغطي القوالب الشريط تمامًا من طرف إلى طرف. نعدّها: 6 قوالب.",
          "Les blocs couvrent exactement la bande d'un bout à l'autre. On les compte : 6 blocs."),
    ]),
    EX("2", "98", st("Is this measurement correct? There are gaps between the blocks.", "هل هذا القياس صحيح؟ بين القوالب فراغات.", "Cette mesure est-elle correcte ? Il y a des trous entre les blocs."), [
        chain(4, mode="gap"),
        T("No. Gaps make the blocks cover more room than they should. Push them together end to end, and then count.",
          "لا. الفراغات تجعل القوالب تأخذ مكانًا أكبر مما يلزم. نضمّها طرفًا بطرف ثم نعدّ.",
          "Non. Les trous font occuper plus de place aux blocs. On les rapproche bout à bout, puis on compte."),
    ]),
    EX("3", "98", st("Is this measurement correct? The blocks overlap.", "هل هذا القياس صحيح؟ القوالب متراكبة.", "Cette mesure est-elle correcte ? Les blocs se chevauchent."), [
        chain(4, mode="over"),
        T("No. Overlapping blocks hide part of the length, so the count is wrong. Place them side by side without covering each other.",
          "لا. القوالب المتراكبة تخفي جزءًا من الطول فيصير العدد خطأ. نضعها متجاورة دون أن تغطي بعضها.",
          "Non. Les blocs qui se chevauchent cachent une partie de la longueur. Il faut les placer côte à côte."),
    ]),
    EX("4", "99", st("Bar A is 3 blocks and bar B is 5 blocks. Which is longer?", "الشريط A طوله 3 قوالب والشريط B طوله 5 قوالب. أيهما أطول؟", "La bande A mesure 3 blocs et la bande B 5 blocs. Laquelle est plus longue ?"), [
        chain(3),
        chain(5),
        T("Same unit, so we can compare: 5 blocks is more than 3 blocks. Bar B is longer.",
          "الوحدة نفسها فنقارن: 5 قوالب أكثر من 3 قوالب. الشريط B أطول.",
          "Même unité, donc on compare : 5 blocs > 3 blocs. La bande B est plus longue."),
    ]),
    EX("5", "99", st("Measure this bar: it is 7 blocks long. How many blocks longer than a 4-block bar?", "هذا الشريط طوله 7 قوالب. كم قالبًا يزيد على شريط من 4 قوالب؟", "Cette bande mesure 7 blocs. De combien de blocs dépasse-t-elle une bande de 4 blocs ?"), [
        chain(7, unit=60),
        T("7 blocks, and the other has 4 blocks. 7 is 3 more than 4, so it is 3 blocks longer.",
          "7 قوالب مقابل 4 قوالب. 7 تزيد 3 على 4، إذن هو أطول بـ3 قوالب.",
          "7 blocs contre 4 blocs. 7, c'est 3 de plus que 4 : elle est plus longue de 3 blocs."),
        F("7 − 4 = 3"),
    ]),
    EX("6", "99", st("Why can we not compare a length in big blocks with a length in small blocks?", "لماذا لا نستطيع مقارنة طول مقيس بقوالب كبيرة بطول مقيس بقوالب صغيرة؟", "Pourquoi ne peut-on pas comparer une longueur en gros blocs et une en petits blocs ?"), [
        T("Because the two units are not the same size. A count is only fair when both measurements use the same unit.",
          "لأن الوحدتين ليستا بالحجم نفسه. لا يكون العدد منصفًا إلا إذا استعملنا الوحدة نفسها في القياسين.",
          "Parce que les deux unités n'ont pas la même taille. Un compte n'est juste que si la même unité est utilisée."),
    ]),
    EX("7", "99", st("A child says the bar is 5 blocks, but 6 blocks are drawn. Who is right?", "قال طفل إن الشريط 5 قوالب لكن المرسوم 6 قوالب. من المحق؟", "Un enfant dit 5 blocs mais 6 blocs sont dessinés. Qui a raison ?"), [
        chain(6),
        T("The number must equal the blocks we can see. Count again carefully, one by one: 6. The child must correct the answer to 6 blocks.",
          "يجب أن يساوي العدد القوالب التي نراها. نعدّ بانتباه واحدًا واحدًا: 6. على الطفل أن يصحّح الجواب إلى 6 قوالب.",
          "Le nombre doit être égal aux blocs visibles. On recompte soigneusement : 6. L'enfant doit corriger : 6 blocs."),
    ]),
    EX("8", "99", st("Final check: measure the bar with the unit and say the result.", "تقييم أخير: قِس الشريط بالوحدة وقل النتيجة.", "Évaluation : mesure la bande avec l'unité et donne le résultat."), [
        chain(8, unit=56),
        T("Start at the left end, no gaps, no overlaps, same unit, then count: the bar is 8 blocks long.",
          "نبدأ من الطرف الأيسر، بلا فراغات ولا تراكب، بالوحدة نفسها، ثم نعدّ: طول الشريط 8 قوالب.",
          "On part du bout gauche, sans trous ni chevauchements, avec la même unité, puis on compte : la bande mesure 8 blocs."),
    ]),
]
