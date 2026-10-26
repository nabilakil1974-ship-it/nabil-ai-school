"""Grade 3 Mathematics — Division Technique (1)."""
from scripts.direct_lessons.common import T, F, EX, st, scene

LESSON_ID = "G03-MATH-EN-053"
GRADE = 3
SUBJECT = "math"
TITLES = {"en": "Division Technique (1)", "ar": "تقنية القسمة (1)", "fr": "Technique de la division (1)"}


def share(t, o, k, tag="D"):
    """t tens rods and o ones cubes shared equally among k boxes (each box gets t/k rods, o/k cubes)."""
    pt, po = t // k, o // k
    w = 600 // k
    svg, ids = "", []
    for g in range(k):
        x = 30 + g * w
        svg += f'<g id="{tag}b{g}"><rect x="{x}" y="60" width="{w-14}" height="190" rx="10" fill="#fff8e1" stroke="#0b3d5c" stroke-width="3"/>'
        for i in range(pt):
            svg += f'<rect x="{x+12+i*22}" y="76" width="14" height="100" fill="#ffcc80" stroke="#0b3d5c" stroke-width="2"/>'
        for i in range(po):
            svg += f'<rect x="{x+12+(i%4)*22}" y="{190+(i//4)*22}" width="16" height="16" fill="#a5d6a7" stroke="#0b3d5c" stroke-width="2"/>'
        svg += '</g>'
        ids.append(f"{tag}b{g}")
    q = pt * 10 + po
    svg += f'<text id="{tag}q" x="330" y="340" font-size="64" font-weight="700" text-anchor="middle" fill="#e53935" font-family="sans-serif">{t*10+o} ÷ {k} = {q}</text>'
    ids.append(tag + "q")
    return scene(svg, ids)


THEORY = [
    ("Dividend, divisor, quotient", "المقسوم والمقسوم عليه والناتج", "Dividende, diviseur, quotient", "112", [
        T("Hello, champion! Division shares a total equally. The dividend is the total being divided, the divisor is the number of groups, and the quotient is the result. We will divide by place value, starting with the greatest place, and always check with multiplication.",
          "مرحبًا يا بطل! القسمة توزّع كمية على أجزاء متساوية. المقسوم هو الكمية الكلية، والمقسوم عليه عدد المجموعات، والناتج هو حاصل القسمة. سنقسم حسب قيمة المنزلة بادئين بالمنزلة الأكبر ونتحقق دائمًا بالضرب.",
          "Le dividende est le total, le diviseur le nombre de groupes, le quotient le résultat. On divise par position en commençant par la plus grande."),
    ]),
    ("84 ÷ 4 by place value", "84 ÷ 4 حسب المنزلة", "84 ÷ 4 par position", "112", [
        T("Share 8 tens among 4 groups: 2 tens each. Share 4 ones among 4 groups: 1 one each. Each group has 2 tens and 1 one: the quotient is 21.",
          "نوزّع 8 عشرات على 4 مجموعات: لكل مجموعة عشرتان. ثم نوزّع 4 آحاد على 4 مجموعات: لكل مجموعة واحد. لكل مجموعة عشرتان وواحد: الناتج 21.",
          "8 dizaines entre 4 groupes : 2 chacun ; 4 unités : 1 chacun. Quotient : 21."),
        share(8, 4, 4),
        F("84 ÷ 4 = 21      CHECK: 21 × 4 = 84"),
    ]),
    ("More examples", "أمثلة أخرى", "D'autres exemples", "113", [
        T("63 ÷ 3: 6 tens ÷ 3 = 2 tens, 3 ones ÷ 3 = 1 one, so 21. 96 ÷ 4: 9 tens ÷ 4 is 2 tens and 1 ten left; the left ten is 10 ones, so 16 ones ÷ 4 = 4: the answer is 24. Check: 24 × 4 = 96.",
          "63 ÷ 3: 6 عشرات ÷ 3 = عشرتان و3 آحاد ÷ 3 = واحد، إذن 21. 96 ÷ 4: 9 عشرات ÷ 4 = عشرتان ويبقى عشرة؛ العشرة 10 آحاد فيصير عندنا 16 واحدًا ÷ 4 = 4: الناتج 24. نتحقق: 24 × 4 = 96.",
          "63 ÷ 3 = 21 ; 96 ÷ 4 = 24 (reste 1 dizaine = 10 unités, 16 ÷ 4 = 4)."),
        F("63 ÷ 3 = 21      96 ÷ 4 = 24"),
    ]),
    ("Do not divide only the ones", "لا نقسم الآحاد وحدها", "Ne pas diviser que les unités", "113", [
        T("A common error is dividing only the ones digit. Division acts on the whole number, place by place, keeping place value.",
          "من الأخطاء الشائعة قسمة رقم الآحاد فقط. القسمة تعمل على العدد كله منزلةً منزلة مع حفظ قيمة المنزلة.",
          "La division porte sur le nombre entier, position par position."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Divide by place value, record each quotient digit, continue, and check: quotient × divisor = dividend.",
          "نقسم حسب المنزلة ونسجّل كل رقم من الناتج ونتابع ثم نتحقق: الناتج × المقسوم عليه = المقسوم.",
          "Diviser par position, noter, continuer, vérifier."),
        F("DIVIDE BY PLACE → RECORD → CONTINUE → CHECK: quotient × divisor = dividend"),
    ]),
]

EXERCISES = [
    EX("1", "112", st("Guided: 63 ÷ 3 and 96 ÷ 4.", "تدريب: 63 ÷ 3 و96 ÷ 4.", "Guidé : 63 ÷ 3 et 96 ÷ 4."), [F("63 ÷ 3 = 21      96 ÷ 4 = 24"), F("21 × 3 = 63      24 × 4 = 96")]),
    EX("2", "113", st("Calculate: 48 ÷ 2, 69 ÷ 3, 88 ÷ 4.", "احسب: 48 ÷ 2، 69 ÷ 3، 88 ÷ 4.", "Calcule : 48 ÷ 2, 69 ÷ 3, 88 ÷ 4."), [
        share(4, 8, 2), F("48 ÷ 2 = 24      69 ÷ 3 = 23      88 ÷ 4 = 22"),
    ]),
    EX("3", "113", st("Error detective: dividing only the ones digit.", "المحقق: قسمة رقم الآحاد فقط.", "Détective : diviser seulement les unités."), [
        T("Division acts on the entire number, place by place.", "القسمة تعمل على العدد كله منزلةً منزلة.", "On divise tout le nombre."),
    ]),
    EX("4", "113", st("Final check: 72 ÷ 3 and 64 ÷ 2, verify with multiplication.", "تقييم: 72 ÷ 3 و64 ÷ 2 وتحقق بالضرب.", "Évaluation : 72 ÷ 3 et 64 ÷ 2."), [
        F("72 ÷ 3 = 24      24 × 3 = 72"), F("64 ÷ 2 = 32      32 × 2 = 64"),
    ]),
]
