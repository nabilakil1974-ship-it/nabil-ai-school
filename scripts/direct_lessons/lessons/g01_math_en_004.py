"""Direct lesson data: Grade 1 Mathematics — Comparing the numbers from 1 to 5.

Written once in three languages; every text step carries its own ar/en/fr twin."""
from __future__ import annotations

LESSON_ID = 'G01-MATH-EN-004'
GRADE = 1
SUBJECT = "math"
TITLES = {'en': 'Comparing the numbers from 1 to 5', 'ar': 'مقارنة الأعداد من 1 إلى 5', 'fr': 'Comparer les nombres de 1 à 5'}

from scripts.direct_lessons.common import T, F, D, EX, st, S, make_scenes


THEORY = [('Which group has more?',
  'أي مجموعة فيها أكثر؟',
  'Quel groupe en a le plus ?',
  '22',
  [{'k': 't',
    'en': 'Hello! Today we do not learn a new number. We already know 1, 2, 3, 4 and 5.',
    'ar': 'مرحبًا! اليوم لا نتعلّم عددًا جديدًا. نحن نعرف 1 و2 و3 و4 و5.',
    'fr': "Bonjour ! Aujourd'hui, nous n'apprenons pas de nouveau nombre. Nous connaissons 1, 2, 3, 4 et 5.",
    'label': None},
   {'k': 't',
    'en': 'Today we learn something new. When we have two groups, how can we know which has more, which has fewer, or whether they have '
          'the same number?',
    'ar': 'اليوم نتعلّم شيئًا جديدًا. عندما يكون عندنا مجموعتان، كيف نعرف أيّهما فيها more (أكثر)، وأيّهما fewer (أقل)، أو هل لهما العدد '
          'نفسه same؟',
    'fr': "Aujourd'hui, nous apprenons quelque chose de nouveau. Avec deux groupes, comment savoir lequel en a plus (more), lequel en a "
          "moins (fewer), ou s'ils en ont autant (same) ?",
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<text id="e1" x="40" y="122" font-size="34" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                    'fill="#0b3d5c">A</text><text id="e2" x="40" y="312" font-size="34" font-family="sans-serif" font-weight="bold" '
                    'text-anchor="middle" fill="#0b3d5c">B</text><g id="e3"><circle cx="270" cy="113" r="28" fill="#e03131" '
                    'stroke="#0b3d5c" stroke-width="3"/><line x1="270" y1="85" x2="275" y2="73" stroke="#7a4a1d" '
                    'stroke-width="4"/><ellipse cx="281" cy="78" rx="8" ry="4" fill="#40c057" stroke="#0b3d5c" stroke-width="2"/></g><g '
                    'id="e4"><circle cx="360" cy="113" r="28" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><line x1="360" y1="85" '
                    'x2="365" y2="73" stroke="#7a4a1d" stroke-width="4"/><ellipse cx="371" cy="78" rx="8" ry="4" fill="#40c057" '
                    'stroke="#0b3d5c" stroke-width="2"/></g><g id="e5"><circle cx="450" cy="113" r="28" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><line x1="450" y1="85" x2="455" y2="73" stroke="#7a4a1d" stroke-width="4"/><ellipse cx="461" '
                    'cy="78" rx="8" ry="4" fill="#40c057" stroke="#0b3d5c" stroke-width="2"/></g><g id="e6"><circle cx="315" cy="303" '
                    'r="28" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><line x1="315" y1="275" x2="320" y2="263" stroke="#7a4a1d" '
                    'stroke-width="4"/><ellipse cx="326" cy="268" rx="8" ry="4" fill="#40c057" stroke="#0b3d5c" stroke-width="2"/></g><g '
                    'id="e7"><circle cx="405" cy="303" r="28" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><line x1="405" y1="275" '
                    'x2="410" y2="263" stroke="#7a4a1d" stroke-width="4"/><ellipse cx="416" cy="268" rx="8" ry="4" fill="#40c057" '
                    'stroke="#0b3d5c" stroke-width="2"/></g>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7']}},
   {'k': 't',
    'en': 'Look at the picture. Which group has more, in your opinion? Maybe A. But we do not want to guess. How can we be sure? We will '
          'discover a clever way.',
    'ar': 'انظر إلى الصورة. أي مجموعة فيها أكثر برأيك؟ ربما A. لكننا لا نريد التخمين. كيف نتأكد؟ سنكتشف طريقة ذكية.',
    'fr': "Regarde l'image. Quel groupe en a le plus, à ton avis ? Peut-être A. Mais on ne veut pas deviner. Comment être sûr ? Nous "
          'allons découvrir une façon astucieuse.',
    'label': None}]),
 ('Compare by pairing',
  'نقارن بالمزاوجة',
  'Comparer en formant des paires',
  '22',
  [{'k': 't',
    'en': 'Look at the two groups again. We take one apple from A and put one apple from B next to it. This is a pair.',
    'ar': 'انظر إلى المجموعتين من جديد. نأخذ تفاحة من A ونضع بجانبها تفاحة من B. هذا زوج.',
    'fr': "Regarde encore les deux groupes. On prend une pomme de A et on met à côté une pomme de B. C'est une paire.",
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<text id="e1" x="40" y="122" font-size="34" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                    'fill="#0b3d5c">A</text><text id="e2" x="40" y="312" font-size="34" font-family="sans-serif" font-weight="bold" '
                    'text-anchor="middle" fill="#0b3d5c">B</text><g id="e3"><circle cx="270" cy="113" r="28" fill="#e03131" '
                    'stroke="#0b3d5c" stroke-width="3"/><line x1="270" y1="85" x2="275" y2="73" stroke="#7a4a1d" '
                    'stroke-width="4"/><ellipse cx="281" cy="78" rx="8" ry="4" fill="#40c057" stroke="#0b3d5c" stroke-width="2"/></g><g '
                    'id="e4"><circle cx="360" cy="113" r="28" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><line x1="360" y1="85" '
                    'x2="365" y2="73" stroke="#7a4a1d" stroke-width="4"/><ellipse cx="371" cy="78" rx="8" ry="4" fill="#40c057" '
                    'stroke="#0b3d5c" stroke-width="2"/></g><g id="e5"><circle cx="450" cy="113" r="28" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><line x1="450" y1="85" x2="455" y2="73" stroke="#7a4a1d" stroke-width="4"/><ellipse cx="461" '
                    'cy="78" rx="8" ry="4" fill="#40c057" stroke="#0b3d5c" stroke-width="2"/></g><g id="e6"><circle cx="315" cy="303" '
                    'r="28" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><line x1="315" y1="275" x2="320" y2="263" stroke="#7a4a1d" '
                    'stroke-width="4"/><ellipse cx="326" cy="268" rx="8" ry="4" fill="#40c057" stroke="#0b3d5c" stroke-width="2"/></g><g '
                    'id="e7"><circle cx="405" cy="303" r="28" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><line x1="405" y1="275" '
                    'x2="410" y2="263" stroke="#7a4a1d" stroke-width="4"/><ellipse cx="416" cy="268" rx="8" ry="4" fill="#40c057" '
                    'stroke="#0b3d5c" stroke-width="2"/></g><line id="e8" x1="270" y1="146" x2="315" y2="264" stroke="#e8590c" '
                    'stroke-width="4" stroke-linecap="round" stroke-dasharray="10 8"/><line id="e9" x1="360" y1="146" x2="405" y2="264" '
                    'stroke="#e8590c" stroke-width="4" stroke-linecap="round" stroke-dasharray="10 8"/>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9']}},
   {'k': 't',
    'en': 'Now the second pair. Does every apple of B have a partner? Yes. Is there an apple of A left without a partner? Yes, one apple.',
    'ar': 'الآن الزوج الثاني. هل لكل تفاحة من B شريك؟ نعم. هل بقيت تفاحة من A بلا شريك؟ نعم، تفاحة واحدة.',
    'fr': 'Maintenant, la deuxième paire. Chaque pomme de B a-t-elle une partenaire ? Oui. Reste-t-il une pomme de A sans partenaire ? '
          'Oui, une pomme.',
    'label': None},
   {'k': 't',
    'en': 'When we pair and some objects are left in one group, that group has more. So: A has more. B has fewer.',
    'ar': 'عندما نزاوج وتبقى أشياء في مجموعة واحدة، فهذه المجموعة فيها more. إذن: A has more. B has fewer.',
    'fr': "Quand on forme des paires et qu'il reste des objets dans un groupe, ce groupe en a plus. Donc : A has more. B has fewer.",
    'label': None},
   {'k': 'f', 'f': 'A has more.   B has fewer.'},
   {'k': 't',
    'en': 'Why? Because after the pairs, one apple is left in A.',
    'ar': 'لماذا؟ لأنه بعد تكوين الأزواج بقيت تفاحة زائدة في A.',
    'fr': "Pourquoi ? Parce qu'après les paires, il reste une pomme en trop dans A.",
    'label': None},
   {'k': 't',
    'en': 'We do not decide from the look. We match one with one.',
    'ar': 'لا نقرّر من الشكل. نقابل واحدًا بواحد.',
    'fr': "On ne décide pas d'après l'aspect. On associe un à un.",
    'label': None}]),
 ('Same number: every object has a partner',
  'العدد نفسه: لكل شيء شريك',
  'Même nombre : chaque objet a un partenaire',
  '23',
  [{'k': 't',
    'en': 'Now two groups that look different: 3 green circles and 3 blue circles. We make pairs.',
    'ar': 'الآن مجموعتان شكلهما مختلف: 3 دوائر خضراء و3 دوائر زرقاء. نكوّن الأزواج.',
    'fr': "Maintenant, deux groupes d'aspect différent : 3 cercles verts et 3 cercles bleus. On forme des paires.",
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<text id="e1" x="40" y="122" font-size="34" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                    'fill="#0b3d5c">A</text><text id="e2" x="40" y="312" font-size="34" font-family="sans-serif" font-weight="bold" '
                    'text-anchor="middle" fill="#0b3d5c">B</text><circle id="e3" cx="240" cy="110" r="28" fill="#51cf66" stroke="#0b3d5c" '
                    'stroke-width="3"/><circle id="e4" cx="360" cy="110" r="28" fill="#51cf66" stroke="#0b3d5c" stroke-width="3"/><circle '
                    'id="e5" cx="480" cy="110" r="28" fill="#51cf66" stroke="#0b3d5c" stroke-width="3"/><circle id="e6" cx="240" cy="300" '
                    'r="28" fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/><circle id="e7" cx="360" cy="300" r="28" fill="#4dabf7" '
                    'stroke="#0b3d5c" stroke-width="3"/><circle id="e8" cx="480" cy="300" r="28" fill="#4dabf7" stroke="#0b3d5c" '
                    'stroke-width="3"/><line id="e9" x1="240" y1="146" x2="240" y2="264" stroke="#e8590c" stroke-width="4" '
                    'stroke-linecap="round" stroke-dasharray="10 8"/><line id="e10" x1="360" y1="146" x2="360" y2="264" stroke="#e8590c" '
                    'stroke-width="4" stroke-linecap="round" stroke-dasharray="10 8"/><line id="e11" x1="480" y1="146" x2="480" y2="264" '
                    'stroke="#e8590c" stroke-width="4" stroke-linecap="round" stroke-dasharray="10 8"/>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10', 'e11']}},
   {'k': 't',
    'en': 'Is there an object left without a partner in A? No. In B? No.',
    'ar': 'هل بقي شيء بلا شريك في A؟ لا. وفي B؟ لا.',
    'fr': 'Reste-t-il un objet sans partenaire dans A ? Non. Dans B ? Non.',
    'label': None},
   {'k': 't',
    'en': 'So both groups have the same number. Let us check by counting. A: one, two, three. B: one, two, three. Yes: 3 and 3, the same '
          'number.',
    'ar': 'إذن للمجموعتين العدد نفسه. لنتحقّق بالعدّ. A: one، two، three. B: one، two، three. نعم: 3 و3، العدد نفسه.',
    'fr': 'Les deux groupes ont donc le même nombre. Vérifions en comptant. A : one, two, three. B : one, two, three. Oui : 3 et 3, le '
          'même nombre.',
    'label': None},
   {'k': 'f', 'f': '3 = 3   same number'}]),
 ('Spacing can trick our eyes',
  'التباعد قد يخدع أعيننا',
  "L'espacement peut tromper nos yeux",
  '23',
  [{'k': 't',
    'en': 'A tricky question. Group A has 4 dots close together. Group B has 3 dots far apart. Which group looks bigger on the screen?',
    'ar': 'سؤال فيه خدعة. المجموعة A فيها 4 نقاط متقاربة، والمجموعة B فيها 3 نقاط متباعدة جدًا. أي مجموعة تبدو أكبر على الشاشة؟',
    'fr': 'Une question piège. Le groupe A a 4 points serrés. Le groupe B a 3 points très écartés. Quel groupe paraît le plus grand à '
          "l'écran ?",
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<text id="e1" x="40" y="115" font-size="34" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                    'fill="#0b3d5c">A</text><circle id="e2" cx="248" cy="110" r="14" fill="#0b3d5c" stroke="#0b3d5c" '
                    'stroke-width="3"/><circle id="e3" cx="302" cy="110" r="14" fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle '
                    'id="e4" cx="358" cy="110" r="14" fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle id="e5" cx="412" cy="110" '
                    'r="14" fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><text id="e6" x="40" y="315" font-size="34" '
                    'font-family="sans-serif" font-weight="bold" text-anchor="middle" fill="#0b3d5c">B</text><circle id="e7" cx="130" '
                    'cy="310" r="14" fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle id="e8" cx="340" cy="310" r="14" '
                    'fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle id="e9" cx="550" cy="310" r="14" fill="#0b3d5c" '
                    'stroke="#0b3d5c" stroke-width="3"/>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9']}},
   {'k': 't',
    'en': 'Yes, B takes more space. But the question is not who takes more space. The question is: who has more objects?',
    'ar': 'نعم، B تأخذ مساحة أكبر. لكن السؤال ليس من يأخذ مساحة أكبر. السؤال: من عنده أشياء أكثر؟',
    'fr': "Oui, B prend plus de place. Mais la question n'est pas qui prend plus de place. La question est : qui a plus d'objets ?",
    'label': None},
   {'k': 't',
    'en': 'Count A: one, two, three, four. Count B: one, two, three. So A has more.',
    'ar': 'عدّ A: one، two، three، four. عدّ B: one، two، three. إذن A has more.',
    'fr': 'Compte A : one, two, three, four. Compte B : one, two, three. A en a donc plus.',
    'label': None},
   {'k': 't',
    'en': 'B was spread out, so it tricked our eyes. But the number does not change because of the distance.',
    'ar': 'كانت B متباعدة فخدعت أعيننا. لكن العدد لا يتغيّر بسبب المسافة.',
    'fr': 'B était écartée, elle a donc trompé nos yeux. Mais le nombre ne change pas à cause de la distance.',
    'label': None},
   {'k': 't',
    'en': 'We compare quantities, not the space things take.',
    'ar': 'نقارن الكميات وليس المساحة التي تأخذها الأشياء.',
    'fr': 'On compare les quantités, pas la place que prennent les objets.',
    'label': None}]),
 ('More, fewer, same',
  'more و fewer و same',
  'More, fewer, same',
  '23',
  [{'k': 't',
    'en': 'Now we have three important words: MORE, FEWER, SAME.',
    'ar': 'الآن عندنا ثلاث كلمات مهمة: MORE (أكثر) و FEWER (أقل) و SAME (نفسه).',
    'fr': 'Nous avons maintenant trois mots importants : MORE (plus), FEWER (moins), SAME (autant).',
    'label': None},
   {'k': 't',
    'en': 'If some objects are left in a group after pairing, that group has more. The other group has fewer. If nothing is left in either '
          'group, they have the same number.',
    'ar': 'إذا بقيت أشياء في مجموعة بعد المزاوجة فهي فيها more، والمجموعة الأخرى فيها fewer. وإذا لم يبق شيء في أي مجموعة فالعدد نفسه '
          'same.',
    'fr': "S'il reste des objets dans un groupe après les paires, ce groupe en a plus. L'autre en a moins. S'il ne reste rien dans aucun "
          'groupe, les nombres sont les mêmes.',
    'label': None},
   {'k': 't',
    'en': 'Case 1: A has 5, B has 3. After pairing, A has extra. A has more. B has fewer.',
    'ar': 'الحالة 1: في A خمسة وفي B ثلاثة. بعد المزاوجة يبقى زائد في A. A has more. B has fewer.',
    'fr': 'Cas 1 : A a 5, B a 3. Après les paires, il reste des objets dans A. A a plus. B a moins.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<text id="e1" x="40" y="122" font-size="34" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                    'fill="#0b3d5c">A</text><text id="e2" x="40" y="312" font-size="34" font-family="sans-serif" font-weight="bold" '
                    'text-anchor="middle" fill="#0b3d5c">B</text><polygon id="e3" points="200.0,82.4 207.3,100.0 226.2,101.5 211.8,113.8 '
                    '216.2,132.3 200.0,122.4 183.8,132.3 188.2,113.8 173.8,101.5 192.7,100.0" fill="#ffd43b" stroke="#0b3d5c" '
                    'stroke-width="3"/><polygon id="e4" points="280.0,82.4 287.3,100.0 306.2,101.5 291.8,113.8 296.2,132.3 280.0,122.4 '
                    '263.8,132.3 268.2,113.8 253.8,101.5 272.7,100.0" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e5" '
                    'points="360.0,82.4 367.3,100.0 386.2,101.5 371.8,113.8 376.2,132.3 360.0,122.4 343.8,132.3 348.2,113.8 333.8,101.5 '
                    '352.7,100.0" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e6" points="440.0,82.4 447.3,100.0 '
                    '466.2,101.5 451.8,113.8 456.2,132.3 440.0,122.4 423.8,132.3 428.2,113.8 413.8,101.5 432.7,100.0" fill="#ffd43b" '
                    'stroke="#0b3d5c" stroke-width="3"/><polygon id="e7" points="520.0,82.4 527.3,100.0 546.2,101.5 531.8,113.8 '
                    '536.2,132.3 520.0,122.4 503.8,132.3 508.2,113.8 493.8,101.5 512.7,100.0" fill="#ffd43b" stroke="#0b3d5c" '
                    'stroke-width="3"/><polygon id="e8" points="280.0,272.4 287.3,290.0 306.2,291.5 291.8,303.8 296.2,322.3 280.0,312.4 '
                    '263.8,322.3 268.2,303.8 253.8,291.5 272.7,290.0" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e9" '
                    'points="360.0,272.4 367.3,290.0 386.2,291.5 371.8,303.8 376.2,322.3 360.0,312.4 343.8,322.3 348.2,303.8 333.8,291.5 '
                    '352.7,290.0" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e10" points="440.0,272.4 447.3,290.0 '
                    '466.2,291.5 451.8,303.8 456.2,322.3 440.0,312.4 423.8,322.3 428.2,303.8 413.8,291.5 432.7,290.0" fill="#ffd43b" '
                    'stroke="#0b3d5c" stroke-width="3"/><line id="e11" x1="200" y1="142" x2="280" y2="268" stroke="#e8590c" '
                    'stroke-width="4" stroke-linecap="round" stroke-dasharray="10 8"/><line id="e12" x1="280" y1="142" x2="360" y2="268" '
                    'stroke="#e8590c" stroke-width="4" stroke-linecap="round" stroke-dasharray="10 8"/><line id="e13" x1="360" y1="142" '
                    'x2="440" y2="268" stroke="#e8590c" stroke-width="4" stroke-linecap="round" stroke-dasharray="10 8"/>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10', 'e11', 'e12', 'e13']}},
   {'k': 't',
    'en': 'Case 2: A has 2, B has 4. Who has more? B. Who has fewer? A.',
    'ar': 'الحالة 2: في A اثنان وفي B أربعة. من عنده more؟ B. ومن عنده fewer؟ A.',
    'fr': 'Cas 2 : A a 2, B a 4. Qui en a plus ? B. Qui en a moins ? A.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<text id="e1" x="40" y="122" font-size="34" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                    'fill="#0b3d5c">A</text><text id="e2" x="40" y="312" font-size="34" font-family="sans-serif" font-weight="bold" '
                    'text-anchor="middle" fill="#0b3d5c">B</text><polygon id="e3" points="315.0,82.4 322.3,100.0 341.2,101.5 326.8,113.8 '
                    '331.2,132.3 315.0,122.4 298.8,132.3 303.2,113.8 288.8,101.5 307.7,100.0" fill="#ffd43b" stroke="#0b3d5c" '
                    'stroke-width="3"/><polygon id="e4" points="405.0,82.4 412.3,100.0 431.2,101.5 416.8,113.8 421.2,132.3 405.0,122.4 '
                    '388.8,132.3 393.2,113.8 378.8,101.5 397.7,100.0" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e5" '
                    'points="225.0,272.4 232.3,290.0 251.2,291.5 236.8,303.8 241.2,322.3 225.0,312.4 208.8,322.3 213.2,303.8 198.8,291.5 '
                    '217.7,290.0" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e6" points="315.0,272.4 322.3,290.0 '
                    '341.2,291.5 326.8,303.8 331.2,322.3 315.0,312.4 298.8,322.3 303.2,303.8 288.8,291.5 307.7,290.0" fill="#ffd43b" '
                    'stroke="#0b3d5c" stroke-width="3"/><polygon id="e7" points="405.0,272.4 412.3,290.0 431.2,291.5 416.8,303.8 '
                    '421.2,322.3 405.0,312.4 388.8,322.3 393.2,303.8 378.8,291.5 397.7,290.0" fill="#ffd43b" stroke="#0b3d5c" '
                    'stroke-width="3"/><polygon id="e8" points="495.0,272.4 502.3,290.0 521.2,291.5 506.8,303.8 511.2,322.3 495.0,312.4 '
                    '478.8,322.3 483.2,303.8 468.8,291.5 487.7,290.0" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><line id="e9" '
                    'x1="315" y1="142" x2="225" y2="268" stroke="#e8590c" stroke-width="4" stroke-linecap="round" stroke-dasharray="10 '
                    '8"/><line id="e10" x1="405" y1="142" x2="315" y2="268" stroke="#e8590c" stroke-width="4" stroke-linecap="round" '
                    'stroke-dasharray="10 8"/>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10']}},
   {'k': 't',
    'en': 'Case 3: A has 3 and B has 3. What do we say? Same number.',
    'ar': 'الحالة 3: في A ثلاثة وفي B ثلاثة. ماذا نقول؟ Same number.',
    'fr': 'Cas 3 : A a 3 et B a 3. Que dit-on ? Same number.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<text id="e1" x="40" y="122" font-size="34" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                    'fill="#0b3d5c">A</text><text id="e2" x="40" y="312" font-size="34" font-family="sans-serif" font-weight="bold" '
                    'text-anchor="middle" fill="#0b3d5c">B</text><polygon id="e3" points="250.0,82.4 257.3,100.0 276.2,101.5 261.8,113.8 '
                    '266.2,132.3 250.0,122.4 233.8,132.3 238.2,113.8 223.8,101.5 242.7,100.0" fill="#ffd43b" stroke="#0b3d5c" '
                    'stroke-width="3"/><polygon id="e4" points="360.0,82.4 367.3,100.0 386.2,101.5 371.8,113.8 376.2,132.3 360.0,122.4 '
                    '343.8,132.3 348.2,113.8 333.8,101.5 352.7,100.0" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e5" '
                    'points="470.0,82.4 477.3,100.0 496.2,101.5 481.8,113.8 486.2,132.3 470.0,122.4 453.8,132.3 458.2,113.8 443.8,101.5 '
                    '462.7,100.0" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e6" points="250.0,272.4 257.3,290.0 '
                    '276.2,291.5 261.8,303.8 266.2,322.3 250.0,312.4 233.8,322.3 238.2,303.8 223.8,291.5 242.7,290.0" fill="#ffd43b" '
                    'stroke="#0b3d5c" stroke-width="3"/><polygon id="e7" points="360.0,272.4 367.3,290.0 386.2,291.5 371.8,303.8 '
                    '376.2,322.3 360.0,312.4 343.8,322.3 348.2,303.8 333.8,291.5 352.7,290.0" fill="#ffd43b" stroke="#0b3d5c" '
                    'stroke-width="3"/><polygon id="e8" points="470.0,272.4 477.3,290.0 496.2,291.5 481.8,303.8 486.2,322.3 470.0,312.4 '
                    '453.8,322.3 458.2,303.8 443.8,291.5 462.7,290.0" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><line id="e9" '
                    'x1="250" y1="142" x2="250" y2="268" stroke="#e8590c" stroke-width="4" stroke-linecap="round" stroke-dasharray="10 '
                    '8"/><line id="e10" x1="360" y1="142" x2="360" y2="268" stroke="#e8590c" stroke-width="4" stroke-linecap="round" '
                    'stroke-dasharray="10 8"/><line id="e11" x1="470" y1="142" x2="470" y2="268" stroke="#e8590c" stroke-width="4" '
                    'stroke-linecap="round" stroke-dasharray="10 8"/>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10', 'e11']}},
   {'k': 'f', 'f': '5 > 3      2 < 4      3 = 3'}]),
 ('Connect the groups to the numbers',
  'نربط المجموعات بالأعداد',
  'Relier les groupes aux nombres',
  '23',
  [{'k': 't',
    'en': 'Now we connect the objects to the numbers we know. Collection A has 2 balls. Collection B has 5 balls.',
    'ar': 'الآن نربط الأشياء بالأعداد التي نعرفها. المجموعة A فيها كرتان. والمجموعة B فيها 5 كرات.',
    'fr': "Maintenant, on relie les objets aux nombres que l'on connaît. La collection A a 2 balles. La collection B a 5 balles.",
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<text id="e1" x="40" y="115" font-size="34" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                    'fill="#0b3d5c">A</text><g id="e2"><circle cx="290" cy="110" r="28" fill="#fff" stroke="#0b3d5c" '
                    'stroke-width="3"/><polygon points="290,97 302,106 298,120 282,120 278,106" fill="#0b3d5c"/></g><g id="e3"><circle '
                    'cx="370" cy="110" r="28" fill="#fff" stroke="#0b3d5c" stroke-width="3"/><polygon points="370,97 382,106 378,120 '
                    '362,120 358,106" fill="#0b3d5c"/></g><text id="e4" x="590" y="130" font-size="60" font-family="sans-serif" '
                    'font-weight="bold" text-anchor="middle" fill="#0b3d5c">2</text><text id="e5" x="40" y="315" font-size="34" '
                    'font-family="sans-serif" font-weight="bold" text-anchor="middle" fill="#0b3d5c">B</text><g id="e6"><circle cx="170" '
                    'cy="310" r="28" fill="#fff" stroke="#0b3d5c" stroke-width="3"/><polygon points="170,297 182,306 178,320 162,320 '
                    '158,306" fill="#0b3d5c"/></g><g id="e7"><circle cx="250" cy="310" r="28" fill="#fff" stroke="#0b3d5c" '
                    'stroke-width="3"/><polygon points="250,297 262,306 258,320 242,320 238,306" fill="#0b3d5c"/></g><g id="e8"><circle '
                    'cx="330" cy="310" r="28" fill="#fff" stroke="#0b3d5c" stroke-width="3"/><polygon points="330,297 342,306 338,320 '
                    '322,320 318,306" fill="#0b3d5c"/></g><g id="e9"><circle cx="410" cy="310" r="28" fill="#fff" stroke="#0b3d5c" '
                    'stroke-width="3"/><polygon points="410,297 422,306 418,320 402,320 398,306" fill="#0b3d5c"/></g><g id="e10"><circle '
                    'cx="490" cy="310" r="28" fill="#fff" stroke="#0b3d5c" stroke-width="3"/><polygon points="490,297 502,306 498,320 '
                    '482,320 478,306" fill="#0b3d5c"/></g><text id="e11" x="590" y="330" font-size="60" font-family="sans-serif" '
                    'font-weight="bold" text-anchor="middle" fill="#0b3d5c">5</text>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10', 'e11']}},
   {'k': 't',
    'en': 'Count A: 2. Count B: 5. Who has more? B.',
    'ar': 'عدّ A: 2. عدّ B: 5. من عنده more؟ B.',
    'fr': 'Compte A : 2. Compte B : 5. Qui en a plus ? B.',
    'label': None},
   {'k': 't',
    'en': 'So between 2 and 5, the number for the bigger collection is 5. We do not memorise it without meaning. We saw it with objects '
          'first.',
    'ar': 'إذن بين 2 و5 العدد الذي يمثّل المجموعة الأكبر هو 5. لا نحفظه بلا معنى. رأيناه بالأشياء أولًا.',
    'fr': "Entre 2 et 5, le nombre de la plus grande collection est 5. On ne le retient pas sans sens. On l'a d'abord vu avec des objets.",
    'label': None},
   {'k': 'f', 'f': 'objects → count → compare → numbers'}]),
 ('Explain how you know',
  'نشرح كيف عرفنا',
  'Expliquer comment on le sait',
  '23',
  [{'k': 't',
    'en': 'Now something even more important than the answer. Do not only say "A has more". Say how you know.',
    'ar': 'الآن شيء أهم من الجواب. لا تقل فقط «A فيها أكثر». قل كيف عرفت.',
    'fr': 'Maintenant, quelque chose de plus important que la réponse. Ne dis pas seulement « A en a plus ». Dis comment tu le sais.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<text id="e1" x="40" y="122" font-size="34" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                    'fill="#0b3d5c">A</text><text id="e2" x="40" y="312" font-size="34" font-family="sans-serif" font-weight="bold" '
                    'text-anchor="middle" fill="#0b3d5c">B</text><circle id="e3" cx="260" cy="110" r="28" fill="#ff922b" stroke="#0b3d5c" '
                    'stroke-width="3"/><circle id="e4" cx="360" cy="110" r="28" fill="#ff922b" stroke="#0b3d5c" stroke-width="3"/><circle '
                    'id="e5" cx="460" cy="110" r="28" fill="#ff922b" stroke="#0b3d5c" stroke-width="3"/><circle id="e6" cx="310" cy="300" '
                    'r="28" fill="#ff922b" stroke="#0b3d5c" stroke-width="3"/><circle id="e7" cx="410" cy="300" r="28" fill="#ff922b" '
                    'stroke="#0b3d5c" stroke-width="3"/>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7']}},
   {'k': 't',
    'en': 'Which group has more? A. Why? Here are good answers: "Because A has 3 and B has 2." Or: "Because we made pairs and one object '
          'was left in A."',
    'ar': 'أي مجموعة فيها أكثر؟ A. لماذا؟ هذه أجوبة جيدة: «لأن في A ثلاثة وفي B اثنين». أو: «لأننا كوّنا أزواجًا وبقي شيء في A».',
    'fr': "Quel groupe en a le plus ? A. Pourquoi ? Voici de bonnes réponses : « Parce que A en a 3 et B en a 2. » Ou : « Parce qu'on a "
          'fait des paires et il est resté un objet dans A. »',
    'label': None},
   {'k': 't',
    'en': 'A strong answer has two parts: the answer, and the reason.',
    'ar': 'الجواب القوي له جزءان: الجواب والسبب.',
    'fr': 'Une réponse solide a deux parties : la réponse et la raison.',
    'label': None},
   {'k': 'f', 'f': 'Answer + Why'}]),
 ('Mistakes to avoid',
  'أخطاء يجب تجنّبها',
  'Erreurs à éviter',
  '23',
  [{'k': 't',
    'en': 'Mistake 1: thinking bigger objects mean more. A has 2 big balls and B has 4 small balls. Big size does not decide the number. '
          'We count: B has 4, so B has more.',
    'ar': 'الخطأ 1: ظن أن الأشياء الأكبر تعني عددًا أكثر. في A كرتان كبيرتان وفي B أربع كرات صغيرة. الحجم لا يحدّد العدد. نعدّ: في B أربع، '
          'إذن B has more.',
    'fr': 'Erreur 1 : croire que de gros objets signifient plus. A a 2 grosses balles et B a 4 petites balles. La taille ne décide pas du '
          'nombre. On compte : B en a 4, B en a donc plus.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<text id="e1" x="40" y="115" font-size="34" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                    'fill="#0b3d5c">A</text><g id="e2"><circle cx="255" cy="110" r="55" fill="#fff" stroke="#0b3d5c" '
                    'stroke-width="3"/><polygon points="255,85 279,102 270,130 240,130 231,102" fill="#0b3d5c"/></g><g id="e3"><circle '
                    'cx="405" cy="110" r="55" fill="#fff" stroke="#0b3d5c" stroke-width="3"/><polygon points="405,85 429,102 420,130 '
                    '390,130 381,102" fill="#0b3d5c"/></g><text id="e4" x="40" y="315" font-size="34" font-family="sans-serif" '
                    'font-weight="bold" text-anchor="middle" fill="#0b3d5c">B</text><g id="e5"><circle cx="225" cy="310" r="24" '
                    'fill="#fff" stroke="#0b3d5c" stroke-width="3"/><polygon points="225,299 235,307 231,319 219,319 215,307" '
                    'fill="#0b3d5c"/></g><g id="e6"><circle cx="295" cy="310" r="24" fill="#fff" stroke="#0b3d5c" '
                    'stroke-width="3"/><polygon points="295,299 305,307 301,319 289,319 285,307" fill="#0b3d5c"/></g><g id="e7"><circle '
                    'cx="365" cy="310" r="24" fill="#fff" stroke="#0b3d5c" stroke-width="3"/><polygon points="365,299 375,307 371,319 '
                    '359,319 355,307" fill="#0b3d5c"/></g><g id="e8"><circle cx="435" cy="310" r="24" fill="#fff" stroke="#0b3d5c" '
                    'stroke-width="3"/><polygon points="435,299 445,307 441,319 429,319 425,307" fill="#0b3d5c"/></g>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8']}},
   {'k': 't',
    'en': 'Mistake 2: thinking the longer row has more. A row of 3 objects spread wide is not more than 4 objects close together. We count '
          'or we pair.',
    'ar': 'الخطأ 2: ظن أن الصف الأطول فيه أكثر. صف من 3 أشياء متباعدة ليس أكثر من 4 أشياء متقاربة. نعدّ أو نزاوج.',
    'fr': "Erreur 2 : croire que la plus longue rangée en a plus. Une rangée de 3 objets écartés n'en a pas plus que 4 objets serrés. On "
          'compte ou on forme des paires.',
    'label': None},
   {'k': 't',
    'en': 'Mistake 3: mixing up more and fewer. If A has more, what do we say about B? B has fewer. The two always go together.',
    'ar': 'الخطأ 3: خلط more مع fewer. إذا كانت A فيها more فماذا نقول عن B؟ B has fewer. الكلمتان مترابطتان دائمًا.',
    'fr': 'Erreur 3 : confondre more et fewer. Si A en a plus, que dit-on de B ? B en a moins. Les deux vont toujours ensemble.',
    'label': None},
   {'k': 't',
    'en': 'Mistake 4: saying "same" without checking. 4 and 5 look close, so we never say same quickly. We count or we make pairs.',
    'ar': 'الخطأ 4: قول same دون تحقّق. 4 و5 متقاربان في الشكل، لذلك لا نقول same بسرعة. نعدّ أو نكوّن أزواجًا.',
    'fr': 'Erreur 4 : dire « same » sans vérifier. 4 et 5 se ressemblent, on ne dit donc jamais same trop vite. On compte ou on forme des '
          'paires.',
    'label': None}]),
 ('Summary',
  'الخلاصة',
  'Résumé',
  '23',
  [{'k': 't',
    'en': 'Well done! Today we learned to compare quantities from 1 to 5.',
    'ar': 'أحسنت! تعلّمنا اليوم أن نقارن الكميات من 1 إلى 5.',
    'fr': "Bravo ! Aujourd'hui, nous avons appris à comparer des quantités de 1 à 5.",
    'label': None},
   {'k': 't',
    'en': 'We do not decide from the size, the distance or the length of the row. We do something sure: we PAIR or we COUNT.',
    'ar': 'لا نقرّر من الحجم ولا من المسافة ولا من طول الصف. نفعل شيئًا مضمونًا: نزاوج أو نعدّ.',
    'fr': "On ne décide ni d'après la taille, ni la distance, ni la longueur de la rangée. On fait quelque chose de sûr : on forme des "
          'paires ou on compte.',
    'label': None},
   {'k': 't',
    'en': 'If objects are left in a group, that group has more. The other has fewer. If every object has a partner, they have the same '
          'number.',
    'ar': 'إذا بقيت أشياء في مجموعة فهي فيها more والأخرى fewer. وإذا أخذ كل شيء شريكًا فالعدد نفسه same.',
    'fr': "S'il reste des objets dans un groupe, il en a plus. L'autre en a moins. Si chaque objet a un partenaire, les nombres sont les "
          'mêmes.',
    'label': None},
   {'k': 'f', 'f': 'LOOK → PAIR → SEE WHAT REMAINS → SAY MORE / FEWER / SAME → CHECK'},
   {'k': 't',
    'en': 'A strong answer always has: the answer and the reason.',
    'ar': 'الجواب القوي دائمًا فيه: الجواب والسبب.',
    'fr': 'Une réponse solide a toujours : la réponse et la raison.',
    'label': None}])]


EXERCISES = [{'n': '1',
  'page': '22',
  'stmt': ('Group A has 4 stars. Group B has 3 stars. Pair them and decide.',
           'المجموعة A فيها 4 نجوم والمجموعة B فيها 3 نجوم. زاوج بينها وقرّر.',
           'Le groupe A a 4 étoiles. Le groupe B a 3 étoiles. Forme des paires et décide.'),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<text id="e1" x="40" y="122" font-size="34" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                             'fill="#0b3d5c">A</text><text id="e2" x="40" y="312" font-size="34" font-family="sans-serif" '
                             'font-weight="bold" text-anchor="middle" fill="#0b3d5c">B</text><polygon id="e3" points="218.0,80.1 '
                             '225.9,99.1 246.4,100.8 230.8,114.2 235.6,134.2 218.0,123.5 200.4,134.2 205.2,114.2 189.6,100.8 210.1,99.1" '
                             'fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e4" points="312.0,80.1 319.9,99.1 340.4,100.8 '
                             '324.8,114.2 329.6,134.2 312.0,123.5 294.4,134.2 299.2,114.2 283.6,100.8 304.1,99.1" fill="#ffd43b" '
                             'stroke="#0b3d5c" stroke-width="3"/><polygon id="e5" points="408.0,80.1 415.9,99.1 436.4,100.8 420.8,114.2 '
                             '425.6,134.2 408.0,123.5 390.4,134.2 395.2,114.2 379.6,100.8 400.1,99.1" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/><polygon id="e6" points="502.0,80.1 509.9,99.1 530.4,100.8 514.8,114.2 519.6,134.2 '
                             '502.0,123.5 484.4,134.2 489.2,114.2 473.6,100.8 494.1,99.1" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/><polygon id="e7" points="265.0,270.1 272.9,289.1 293.4,290.8 277.8,304.2 282.6,324.2 '
                             '265.0,313.5 247.4,324.2 252.2,304.2 236.6,290.8 257.1,289.1" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/><polygon id="e8" points="360.0,270.1 367.9,289.1 388.4,290.8 372.8,304.2 377.6,324.2 '
                             '360.0,313.5 342.4,324.2 347.2,304.2 331.6,290.8 352.1,289.1" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/><polygon id="e9" points="455.0,270.1 462.9,289.1 483.4,290.8 467.8,304.2 472.6,324.2 '
                             '455.0,313.5 437.4,324.2 442.2,304.2 426.6,290.8 447.1,289.1" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/><line id="e10" x1="218" y1="144" x2="265" y2="266" stroke="#e8590c" stroke-width="4" '
                             'stroke-linecap="round" stroke-dasharray="10 8"/><line id="e11" x1="312" y1="144" x2="360" y2="266" '
                             'stroke="#e8590c" stroke-width="4" stroke-linecap="round" stroke-dasharray="10 8"/><line id="e12" x1="408" '
                             'y1="144" x2="455" y2="266" stroke="#e8590c" stroke-width="4" stroke-linecap="round" stroke-dasharray="10 '
                             '8"/>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10', 'e11', 'e12']}},
            {'k': 't',
             'en': 'Pair 1, pair 2, pair 3. Now every star of B has a partner.',
             'ar': 'الزوج 1 والزوج 2 والزوج 3. الآن لكل نجمة من B شريك.',
             'fr': 'Paire 1, paire 2, paire 3. Maintenant, chaque étoile de B a un partenaire.',
             'label': None},
            {'k': 't',
             'en': 'One star is left in A, without a partner.',
             'ar': 'بقيت نجمة واحدة في A بلا شريك.',
             'fr': 'Il reste une étoile dans A, sans partenaire.',
             'label': None},
            {'k': 't',
             'en': 'So who has more? A. And who has fewer? B.',
             'ar': 'إذن من عنده more؟ A. ومن عنده fewer؟ B.',
             'fr': 'Qui en a plus ? A. Qui en a moins ? B.',
             'label': None},
            {'k': 'f', 'f': 'A has more.   B has fewer.'}]},
 {'n': '2',
  'page': '23',
  'stmt': ('Group A: 4 cars. Group B: 4 teddy bears. Pair them. Same number or not? What is the number?',
           'المجموعة A: 4 سيارات. المجموعة B: 4 دببة. زاوج بينها. هل العدد نفسه؟ وما هو العدد؟',
           'Groupe A : 4 voitures. Groupe B : 4 nounours. Forme des paires. Même nombre ou non ? Quel est le nombre ?'),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<text id="e1" x="40" y="122" font-size="34" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                             'fill="#0b3d5c">A</text><text id="e2" x="40" y="312" font-size="34" font-family="sans-serif" '
                             'font-weight="bold" text-anchor="middle" fill="#0b3d5c">B</text><g id="e3"><rect x="134" y="100" width="62" '
                             'height="23" rx="6" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><rect x="149" y="85" width="31" '
                             'height="16" rx="5" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><circle cx="149" cy="124" r="8" '
                             'fill="#0b3d5c"/><circle cx="181" cy="124" r="8" fill="#0b3d5c"/></g><g id="e4"><rect x="264" y="100" '
                             'width="62" height="23" rx="6" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><rect x="279" y="85" '
                             'width="31" height="16" rx="5" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><circle cx="279" cy="124" '
                             'r="8" fill="#0b3d5c"/><circle cx="311" cy="124" r="8" fill="#0b3d5c"/></g><g id="e5"><rect x="394" y="100" '
                             'width="62" height="23" rx="6" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><rect x="409" y="85" '
                             'width="31" height="16" rx="5" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><circle cx="409" cy="124" '
                             'r="8" fill="#0b3d5c"/><circle cx="441" cy="124" r="8" fill="#0b3d5c"/></g><g id="e6"><rect x="524" y="100" '
                             'width="62" height="23" rx="6" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><rect x="539" y="85" '
                             'width="31" height="16" rx="5" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><circle cx="539" cy="124" '
                             'r="8" fill="#0b3d5c"/><circle cx="571" cy="124" r="8" fill="#0b3d5c"/></g><g id="e7"><circle cx="144" '
                             'cy="279" r="10" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="186" cy="279" r="10" '
                             'fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="165" cy="300" r="26" fill="#c98f55" '
                             'stroke="#0b3d5c" stroke-width="3"/><circle cx="158" cy="296" r="3" fill="#0b3d5c"/><circle cx="172" cy="296" '
                             'r="3" fill="#0b3d5c"/><ellipse cx="165" cy="307" rx="6" ry="4" fill="#f1d3a8" stroke="#0b3d5c" '
                             'stroke-width="2"/></g><g id="e8"><circle cx="274" cy="279" r="10" fill="#a9703c" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle cx="316" cy="279" r="10" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle '
                             'cx="295" cy="300" r="26" fill="#c98f55" stroke="#0b3d5c" stroke-width="3"/><circle cx="288" cy="296" r="3" '
                             'fill="#0b3d5c"/><circle cx="302" cy="296" r="3" fill="#0b3d5c"/><ellipse cx="295" cy="307" rx="6" ry="4" '
                             'fill="#f1d3a8" stroke="#0b3d5c" stroke-width="2"/></g><g id="e9"><circle cx="404" cy="279" r="10" '
                             'fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="446" cy="279" r="10" fill="#a9703c" '
                             'stroke="#0b3d5c" stroke-width="3"/><circle cx="425" cy="300" r="26" fill="#c98f55" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle cx="418" cy="296" r="3" fill="#0b3d5c"/><circle cx="432" cy="296" r="3" '
                             'fill="#0b3d5c"/><ellipse cx="425" cy="307" rx="6" ry="4" fill="#f1d3a8" stroke="#0b3d5c" '
                             'stroke-width="2"/></g><g id="e10"><circle cx="534" cy="279" r="10" fill="#a9703c" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle cx="576" cy="279" r="10" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle '
                             'cx="555" cy="300" r="26" fill="#c98f55" stroke="#0b3d5c" stroke-width="3"/><circle cx="548" cy="296" r="3" '
                             'fill="#0b3d5c"/><circle cx="562" cy="296" r="3" fill="#0b3d5c"/><ellipse cx="555" cy="307" rx="6" ry="4" '
                             'fill="#f1d3a8" stroke="#0b3d5c" stroke-width="2"/></g><line id="e11" x1="165" y1="144" x2="165" y2="266" '
                             'stroke="#e8590c" stroke-width="4" stroke-linecap="round" stroke-dasharray="10 8"/><line id="e12" x1="295" '
                             'y1="144" x2="295" y2="266" stroke="#e8590c" stroke-width="4" stroke-linecap="round" stroke-dasharray="10 '
                             '8"/><line id="e13" x1="425" y1="144" x2="425" y2="266" stroke="#e8590c" stroke-width="4" '
                             'stroke-linecap="round" stroke-dasharray="10 8"/><line id="e14" x1="555" y1="144" x2="555" y2="266" '
                             'stroke="#e8590c" stroke-width="4" stroke-linecap="round" stroke-dasharray="10 8"/>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10', 'e11', 'e12', 'e13', 'e14']}},
            {'k': 't',
             'en': 'After the pairs, is anything left without a partner? No.',
             'ar': 'بعد الأزواج، هل بقي شيء بلا شريك؟ لا.',
             'fr': 'Après les paires, reste-t-il quelque chose sans partenaire ? Non.',
             'label': None},
            {'k': 't',
             'en': 'So it is the same number. Count to check: one, two, three, four.',
             'ar': 'إذن العدد نفسه. نعدّ للتأكد: one، two، three، four.',
             'fr': "C'est donc le même nombre. On compte pour vérifier : one, two, three, four.",
             'label': None},
            {'k': 'f', 'f': '4 and 4 → same number'}]},
 {'n': '3',
  'page': '23',
  'stmt': ('Group A has 5 close stars. Group B has 4 stars far apart. Which has more?',
           'المجموعة A فيها 5 نجوم متقاربة، والمجموعة B فيها 4 نجوم متباعدة. أيّهما أكثر؟',
           'Le groupe A a 5 étoiles serrées. Le groupe B a 4 étoiles écartées. Lequel en a plus ?'),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<text id="e1" x="40" y="115" font-size="34" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                             'fill="#0b3d5c">A</text><polygon id="e2" points="230.0,87.0 236.1,101.6 251.9,102.9 239.8,113.2 243.5,128.6 '
                             '230.0,120.3 216.5,128.6 220.2,113.2 208.1,102.9 223.9,101.6" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/><polygon id="e3" points="280.0,87.0 286.1,101.6 301.9,102.9 289.8,113.2 293.5,128.6 '
                             '280.0,120.3 266.5,128.6 270.2,113.2 258.1,102.9 273.9,101.6" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/><polygon id="e4" points="330.0,87.0 336.1,101.6 351.9,102.9 339.8,113.2 343.5,128.6 '
                             '330.0,120.3 316.5,128.6 320.2,113.2 308.1,102.9 323.9,101.6" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/><polygon id="e5" points="380.0,87.0 386.1,101.6 401.9,102.9 389.8,113.2 393.5,128.6 '
                             '380.0,120.3 366.5,128.6 370.2,113.2 358.1,102.9 373.9,101.6" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/><polygon id="e6" points="430.0,87.0 436.1,101.6 451.9,102.9 439.8,113.2 443.5,128.6 '
                             '430.0,120.3 416.5,128.6 420.2,113.2 408.1,102.9 423.9,101.6" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/><text id="e7" x="40" y="315" font-size="34" font-family="sans-serif" font-weight="bold" '
                             'text-anchor="middle" fill="#0b3d5c">B</text><polygon id="e8" points="105.0,287.0 111.1,301.6 126.9,302.9 '
                             '114.8,313.2 118.5,328.6 105.0,320.4 91.5,328.6 95.2,313.2 83.1,302.9 98.9,301.6" fill="#ffd43b" '
                             'stroke="#0b3d5c" stroke-width="3"/><polygon id="e9" points="265.0,287.0 271.1,301.6 286.9,302.9 274.8,313.2 '
                             '278.5,328.6 265.0,320.4 251.5,328.6 255.2,313.2 243.1,302.9 258.9,301.6" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/><polygon id="e10" points="425.0,287.0 431.1,301.6 446.9,302.9 434.8,313.2 438.5,328.6 '
                             '425.0,320.4 411.5,328.6 415.2,313.2 403.1,302.9 418.9,301.6" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/><polygon id="e11" points="585.0,287.0 591.1,301.6 606.9,302.9 594.8,313.2 598.5,328.6 '
                             '585.0,320.4 571.5,328.6 575.2,313.2 563.1,302.9 578.9,301.6" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10', 'e11']}},
            {'k': 't',
             'en': 'B looks bigger because it is spread out. But we do not judge by the distance.',
             'ar': 'تبدو B أكبر لأنها متباعدة. لكننا لا نحكم من المسافة.',
             'fr': "B paraît plus grande car elle est écartée. Mais on ne juge pas d'après la distance.",
             'label': None},
            {'k': 't',
             'en': 'Count A: one, two, three, four, five. A has 5.',
             'ar': 'عدّ A: one، two، three، four، five. في A خمس.',
             'fr': 'Compte A : one, two, three, four, five. A en a 5.',
             'label': None},
            {'k': 't',
             'en': 'Count B: one, two, three, four. B has 4.',
             'ar': 'عدّ B: one، two، three، four. في B أربع.',
             'fr': 'Compte B : one, two, three, four. B en a 4.',
             'label': None},
            {'k': 'f', 'f': '5 > 4      A has more.'},
            {'k': 't',
             'en': 'Our eyes can be fooled. Counting tells the truth.',
             'ar': 'قد تُخدع أعيننا. والعدّ يقول الحقيقة.',
             'fr': 'Nos yeux peuvent être trompés. Compter dit la vérité.',
             'label': None}]},
 {'n': '4',
  'page': '23',
  'stmt': ('A has 5 cookies, B has 3 cookies. Say: A compared with B, then B compared with A (more, fewer or same).',
           'في A خمس بسكويتات وفي B ثلاث. قل: A بالنسبة إلى B، ثم B بالنسبة إلى A (more أو fewer أو same).',
           'A a 5 biscuits, B en a 3. Dis : A par rapport à B, puis B par rapport à A (more, fewer ou same).'),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<text id="e1" x="40" y="122" font-size="34" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                             'fill="#0b3d5c">A</text><text id="e2" x="40" y="312" font-size="34" font-family="sans-serif" '
                             'font-weight="bold" text-anchor="middle" fill="#0b3d5c">B</text><g id="e3"><circle cx="200" cy="110" r="28" '
                             'fill="#d9a05b" stroke="#0b3d5c" stroke-width="3"/><circle cx="193" cy="105" r="3" fill="#5c3b1e"/><circle '
                             'cx="206" cy="108" r="3" fill="#5c3b1e"/><circle cx="198" cy="118" r="3" fill="#5c3b1e"/></g><g '
                             'id="e4"><circle cx="280" cy="110" r="28" fill="#d9a05b" stroke="#0b3d5c" stroke-width="3"/><circle cx="273" '
                             'cy="105" r="3" fill="#5c3b1e"/><circle cx="286" cy="108" r="3" fill="#5c3b1e"/><circle cx="278" cy="118" '
                             'r="3" fill="#5c3b1e"/></g><g id="e5"><circle cx="360" cy="110" r="28" fill="#d9a05b" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle cx="353" cy="105" r="3" fill="#5c3b1e"/><circle cx="366" cy="108" r="3" '
                             'fill="#5c3b1e"/><circle cx="358" cy="118" r="3" fill="#5c3b1e"/></g><g id="e6"><circle cx="440" cy="110" '
                             'r="28" fill="#d9a05b" stroke="#0b3d5c" stroke-width="3"/><circle cx="433" cy="105" r="3" '
                             'fill="#5c3b1e"/><circle cx="446" cy="108" r="3" fill="#5c3b1e"/><circle cx="438" cy="118" r="3" '
                             'fill="#5c3b1e"/></g><g id="e7"><circle cx="520" cy="110" r="28" fill="#d9a05b" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle cx="513" cy="105" r="3" fill="#5c3b1e"/><circle cx="526" cy="108" r="3" '
                             'fill="#5c3b1e"/><circle cx="518" cy="118" r="3" fill="#5c3b1e"/></g><g id="e8"><circle cx="280" cy="300" '
                             'r="28" fill="#d9a05b" stroke="#0b3d5c" stroke-width="3"/><circle cx="273" cy="295" r="3" '
                             'fill="#5c3b1e"/><circle cx="286" cy="298" r="3" fill="#5c3b1e"/><circle cx="278" cy="308" r="3" '
                             'fill="#5c3b1e"/></g><g id="e9"><circle cx="360" cy="300" r="28" fill="#d9a05b" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle cx="353" cy="295" r="3" fill="#5c3b1e"/><circle cx="366" cy="298" r="3" '
                             'fill="#5c3b1e"/><circle cx="358" cy="308" r="3" fill="#5c3b1e"/></g><g id="e10"><circle cx="440" cy="300" '
                             'r="28" fill="#d9a05b" stroke="#0b3d5c" stroke-width="3"/><circle cx="433" cy="295" r="3" '
                             'fill="#5c3b1e"/><circle cx="446" cy="298" r="3" fill="#5c3b1e"/><circle cx="438" cy="308" r="3" '
                             'fill="#5c3b1e"/></g><line id="e11" x1="200" y1="146" x2="280" y2="264" stroke="#e8590c" stroke-width="4" '
                             'stroke-linecap="round" stroke-dasharray="10 8"/><line id="e12" x1="280" y1="146" x2="360" y2="264" '
                             'stroke="#e8590c" stroke-width="4" stroke-linecap="round" stroke-dasharray="10 8"/><line id="e13" x1="360" '
                             'y1="146" x2="440" y2="264" stroke="#e8590c" stroke-width="4" stroke-linecap="round" stroke-dasharray="10 '
                             '8"/>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10', 'e11', 'e12', 'e13']}},
            {'k': 't',
             'en': "Pair them: B's cookies all have a partner, and A has two cookies left. So A has more.",
             'ar': 'نزاوج: كل بسكويتات B لها شريك، وبقيت في A بسكويتتان. إذن A فيها more.',
             'fr': 'On forme des paires : tous les biscuits de B ont un partenaire, et il reste deux biscuits dans A. A en a plus.',
             'label': None},
            {'k': 'f', 'f': 'A has more cookies than B.'},
            {'k': 't',
             'en': 'Now the other way around. B is the group with the fewer cookies.',
             'ar': 'الآن بالعكس. B هي المجموعة الأقل بسكويتًا.',
             'fr': "Maintenant dans l'autre sens. B est le groupe qui a le moins de biscuits.",
             'label': None},
            {'k': 'f', 'f': 'B has fewer cookies than A.'}]},
 {'n': '5',
  'page': '23',
  'stmt': ('Compare 4 blue and 5 red objects with pairs. Which number is more?',
           'قارن 4 أشياء زرقاء و5 أشياء حمراء بالمزاوجة. أي عدد هو الأكثر؟',
           'Compare 4 objets bleus et 5 objets rouges avec des paires. Quel nombre est le plus grand ?'),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<text id="e1" x="40" y="122" font-size="34" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                             'fill="#0b3d5c">A</text><text id="e2" x="40" y="312" font-size="34" font-family="sans-serif" '
                             'font-weight="bold" text-anchor="middle" fill="#0b3d5c">B</text><circle id="e3" cx="225" cy="110" r="28" '
                             'fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/><circle id="e4" cx="315" cy="110" r="28" fill="#4dabf7" '
                             'stroke="#0b3d5c" stroke-width="3"/><circle id="e5" cx="405" cy="110" r="28" fill="#4dabf7" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle id="e6" cx="495" cy="110" r="28" fill="#4dabf7" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle id="e7" cx="180" cy="300" r="28" fill="#e03131" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle id="e8" cx="270" cy="300" r="28" fill="#e03131" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle id="e9" cx="360" cy="300" r="28" fill="#e03131" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle id="e10" cx="450" cy="300" r="28" fill="#e03131" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle id="e11" cx="540" cy="300" r="28" fill="#e03131" stroke="#0b3d5c" '
                             'stroke-width="3"/><line id="e12" x1="225" y1="146" x2="180" y2="264" stroke="#e8590c" stroke-width="4" '
                             'stroke-linecap="round" stroke-dasharray="10 8"/><line id="e13" x1="315" y1="146" x2="270" y2="264" '
                             'stroke="#e8590c" stroke-width="4" stroke-linecap="round" stroke-dasharray="10 8"/><line id="e14" x1="405" '
                             'y1="146" x2="360" y2="264" stroke="#e8590c" stroke-width="4" stroke-linecap="round" stroke-dasharray="10 '
                             '8"/><line id="e15" x1="495" y1="146" x2="450" y2="264" stroke="#e8590c" stroke-width="4" '
                             'stroke-linecap="round" stroke-dasharray="10 8"/>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10', 'e11', 'e12', 'e13', 'e14', 'e15']}},
            {'k': 't', 'en': 'Count A: 4. Count B: 5.', 'ar': 'عدّ A: 4. عدّ B: 5.', 'fr': 'Compte A : 4. Compte B : 5.', 'label': None},
            {'k': 't',
             'en': 'We pair them: 4 pairs form, and one red object is left in B.',
             'ar': 'نزاوجها: يتكوّن 4 أزواج وتبقى شيء أحمر واحد في B.',
             'fr': 'On forme des paires : 4 paires se forment, et il reste un objet rouge dans B.',
             'label': None},
            {'k': 't',
             'en': 'So B has more. 5 has more than 4. And 4 has fewer than 5.',
             'ar': 'إذن B فيها more. 5 أكثر من 4. و4 أقل من 5.',
             'fr': 'B en a donc plus. 5 est plus que 4. Et 4 est moins que 5.',
             'label': None},
            {'k': 'f', 'f': '5 > 4      4 < 5'},
            {'k': 't',
             'en': 'The proof: after pairing, one object is left in the group of 5.',
             'ar': 'الدليل: بعد المزاوجة بقي شيء في مجموعة الـ5.',
             'fr': 'La preuve : après les paires, il reste un objet dans le groupe de 5.',
             'label': None}]},
 {'n': '6',
  'page': '23',
  'stmt': ('A has 5 stars, B has 3 stars. Which is right? A. A has fewer. B. A has more. C. A and B have the same number.',
           'في A خمس نجوم وفي B ثلاث. أيّها صحيح؟ A. فيها fewer. B. فيها more. C. العدد نفسه.',
           'A a 5 étoiles, B en a 3. Laquelle est juste ? A. A en a moins. B. A en a plus. C. A et B en ont autant.'),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<text id="e1" x="40" y="122" font-size="34" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                             'fill="#0b3d5c">A</text><text id="e2" x="40" y="312" font-size="34" font-family="sans-serif" '
                             'font-weight="bold" text-anchor="middle" fill="#0b3d5c">B</text><polygon id="e3" points="200.0,82.4 '
                             '207.3,100.0 226.2,101.5 211.8,113.8 216.2,132.3 200.0,122.4 183.8,132.3 188.2,113.8 173.8,101.5 192.7,100.0" '
                             'fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e4" points="280.0,82.4 287.3,100.0 '
                             '306.2,101.5 291.8,113.8 296.2,132.3 280.0,122.4 263.8,132.3 268.2,113.8 253.8,101.5 272.7,100.0" '
                             'fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e5" points="360.0,82.4 367.3,100.0 '
                             '386.2,101.5 371.8,113.8 376.2,132.3 360.0,122.4 343.8,132.3 348.2,113.8 333.8,101.5 352.7,100.0" '
                             'fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e6" points="440.0,82.4 447.3,100.0 '
                             '466.2,101.5 451.8,113.8 456.2,132.3 440.0,122.4 423.8,132.3 428.2,113.8 413.8,101.5 432.7,100.0" '
                             'fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e7" points="520.0,82.4 527.3,100.0 '
                             '546.2,101.5 531.8,113.8 536.2,132.3 520.0,122.4 503.8,132.3 508.2,113.8 493.8,101.5 512.7,100.0" '
                             'fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e8" points="280.0,272.4 287.3,290.0 '
                             '306.2,291.5 291.8,303.8 296.2,322.3 280.0,312.4 263.8,322.3 268.2,303.8 253.8,291.5 272.7,290.0" '
                             'fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e9" points="360.0,272.4 367.3,290.0 '
                             '386.2,291.5 371.8,303.8 376.2,322.3 360.0,312.4 343.8,322.3 348.2,303.8 333.8,291.5 352.7,290.0" '
                             'fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e10" points="440.0,272.4 447.3,290.0 '
                             '466.2,291.5 451.8,303.8 456.2,322.3 440.0,312.4 423.8,322.3 428.2,303.8 413.8,291.5 432.7,290.0" '
                             'fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><line id="e11" x1="200" y1="142" x2="280" y2="268" '
                             'stroke="#e8590c" stroke-width="4" stroke-linecap="round" stroke-dasharray="10 8"/><line id="e12" x1="280" '
                             'y1="142" x2="360" y2="268" stroke="#e8590c" stroke-width="4" stroke-linecap="round" stroke-dasharray="10 '
                             '8"/><line id="e13" x1="360" y1="142" x2="440" y2="268" stroke="#e8590c" stroke-width="4" '
                             'stroke-linecap="round" stroke-dasharray="10 8"/>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10', 'e11', 'e12', 'e13']}},
            {'k': 't',
             'en': 'Count: A has 5 and B has 3. 5 is more than 3.',
             'ar': 'نعدّ: في A خمس وفي B ثلاث. 5 أكثر من 3.',
             'fr': 'On compte : A en a 5 et B en a 3. 5 est plus que 3.',
             'label': None},
            {'k': 'f', 'f': 'B. A has more.'},
            {'k': 't',
             'en': 'Why is A wrong? Because A has more, not fewer.',
             'ar': 'لماذا A خاطئة؟ لأن في A أكثر وليس أقل.',
             'fr': 'Pourquoi A est-elle fausse ? Parce que A en a plus, pas moins.',
             'label': None},
            {'k': 't',
             'en': 'Why is C wrong? Because 5 is not the same as 3.',
             'ar': 'لماذا C خاطئة؟ لأن 5 ليست مثل 3.',
             'fr': "Pourquoi C est-elle fausse ? Parce que 5 n'est pas pareil que 3.",
             'label': None},
            {'k': 't',
             'en': 'You knew the right one and you explained the wrong ones.',
             'ar': 'عرفت الصحيحة وشرحت الخاطئة.',
             'fr': 'Tu as trouvé la bonne réponse et tu as expliqué les fausses.',
             'label': None}]},
 {'n': '7',
  'page': '23',
  'stmt': ('Three groups: A has 2, B has 5, C has 3. Who has the most? Who has the fewest? Put them in order from fewer to more.',
           'ثلاث مجموعات: A فيها 2، B فيها 5، C فيها 3. من عنده الأكثر؟ من عنده الأقل؟ رتّبها من الأقل إلى الأكثر.',
           'Trois groupes : A a 2, B a 5, C a 3. Qui en a le plus ? Qui en a le moins ? Range-les du moins au plus.'),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<text id="e1" x="70" y="100" font-size="34" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                             'fill="#0b3d5c">A</text><circle id="e2" cx="40" cy="170" r="22" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle id="e3" cx="100" cy="170" r="22" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/><text id="e4" x="330" y="100" font-size="34" font-family="sans-serif" font-weight="bold" '
                             'text-anchor="middle" fill="#0b3d5c">B</text><circle id="e5" cx="226" cy="170" r="20" fill="#ff922b" '
                             'stroke="#0b3d5c" stroke-width="3"/><circle id="e6" cx="278" cy="170" r="20" fill="#ff922b" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle id="e7" cx="330" cy="170" r="20" fill="#ff922b" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle id="e8" cx="382" cy="170" r="20" fill="#ff922b" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle id="e9" cx="434" cy="170" r="20" fill="#ff922b" stroke="#0b3d5c" '
                             'stroke-width="3"/><text id="e10" x="590" y="100" font-size="34" font-family="sans-serif" font-weight="bold" '
                             'text-anchor="middle" fill="#0b3d5c">C</text><circle id="e11" cx="538" cy="170" r="20" fill="#51cf66" '
                             'stroke="#0b3d5c" stroke-width="3"/><circle id="e12" cx="590" cy="170" r="20" fill="#51cf66" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle id="e13" cx="642" cy="170" r="20" fill="#51cf66" stroke="#0b3d5c" '
                             'stroke-width="3"/>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10', 'e11', 'e12', 'e13']}},
            {'k': 't',
             'en': 'Count each group: A = 2, B = 5, C = 3.',
             'ar': 'نعدّ كل مجموعة: A = 2، B = 5، C = 3.',
             'fr': 'On compte chaque groupe : A = 2, B = 5, C = 3.',
             'label': None},
            {'k': 't',
             'en': 'Question 1: the most is B, with 5.',
             'ar': 'السؤال 1: الأكثر هو B ومعه 5.',
             'fr': 'Question 1 : le plus est B, avec 5.',
             'label': None},
            {'k': 't',
             'en': 'Question 2: the fewest is A, with 2.',
             'ar': 'السؤال 2: الأقل هو A ومعه 2.',
             'fr': 'Question 2 : le moins est A, avec 2.',
             'label': None},
            {'k': 't',
             'en': 'Question 3: from fewer to more.',
             'ar': 'السؤال 3: من الأقل إلى الأكثر.',
             'fr': 'Question 3 : du moins au plus.',
             'label': None},
            {'k': 'f', 'f': 'A → C → B'},
            {'k': 'f', 'f': '2 → 3 → 5'},
            {'k': 't',
             'en': 'How did we make sure? We counted the quantities.',
             'ar': 'كيف تأكدنا؟ عددنا الكميات.',
             'fr': "Comment s'en assurer ? On a compté les quantités.",
             'label': None}]},
 {'n': '8',
  'page': '23',
  'stmt': ('Final challenge. 1) A has 4, B has 2: who has more? 2) A has 1, B has 3: who has fewer? 3) A has 5, B has 5: more, fewer or '
           'same? 4) A has 4 close objects, B has 3 spread out: who has more? 5) A = 5, B = 4: say the answer and the reason.',
           'التحدي الأخير. 1) في A أربعة وفي B اثنان: من عنده more؟ 2) في A واحد وفي B ثلاثة: من عنده fewer؟ 3) في A خمسة وفي B خمسة: more '
           'أم fewer أم same؟ 4) في A أربعة أشياء متقاربة وفي B ثلاثة متباعدة: من عنده more؟ 5) A = 5 و B = 4: قل الجواب والسبب.',
           'Défi final. 1) A a 4, B a 2 : qui en a plus ? 2) A a 1, B a 3 : qui en a moins ? 3) A a 5, B a 5 : more, fewer ou same ? 4) A '
           'a 4 objets serrés, B en a 3 écartés : qui en a plus ? 5) A = 5, B = 4 : donne la réponse et la raison.'),
  'steps': [{'k': 't',
             'en': 'Task 1: 4 and 2. After pairing, A has two objects left. A has more.',
             'ar': 'المهمة 1: 4 و2. بعد المزاوجة يبقى في A شيئان. A has more.',
             'fr': 'Tâche 1 : 4 et 2. Après les paires, il reste deux objets dans A. A en a plus.',
             'label': None},
            {'k': 'f', 'f': 'A has more.'},
            {'k': 't',
             'en': 'Task 2: 1 and 3. A has only 1, B has 3. So A has fewer.',
             'ar': 'المهمة 2: 1 و3. في A واحد فقط وفي B ثلاثة. إذن A has fewer.',
             'fr': "Tâche 2 : 1 et 3. A n'en a qu'1, B en a 3. A en a donc moins.",
             'label': None},
            {'k': 'f', 'f': 'A has fewer.'},
            {'k': 't',
             'en': 'Task 3: 5 and 5. Every object has a partner and nothing is left. Same number.',
             'ar': 'المهمة 3: 5 و5. لكل شيء شريك ولا يبقى شيء. Same number.',
             'fr': 'Tâche 3 : 5 et 5. Chaque objet a un partenaire, il ne reste rien. Même nombre.',
             'label': None},
            {'k': 'f', 'f': '5 = 5   same'},
            {'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<text id="e1" x="40" y="115" font-size="34" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                             'fill="#0b3d5c">A</text><circle id="e2" cx="248" cy="110" r="14" fill="#0b3d5c" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle id="e3" cx="302" cy="110" r="14" fill="#0b3d5c" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle id="e4" cx="358" cy="110" r="14" fill="#0b3d5c" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle id="e5" cx="412" cy="110" r="14" fill="#0b3d5c" stroke="#0b3d5c" '
                             'stroke-width="3"/><text id="e6" x="40" y="315" font-size="34" font-family="sans-serif" font-weight="bold" '
                             'text-anchor="middle" fill="#0b3d5c">B</text><circle id="e7" cx="130" cy="310" r="14" fill="#0b3d5c" '
                             'stroke="#0b3d5c" stroke-width="3"/><circle id="e8" cx="340" cy="310" r="14" fill="#0b3d5c" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle id="e9" cx="550" cy="310" r="14" fill="#0b3d5c" stroke="#0b3d5c" '
                             'stroke-width="3"/>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9']}},
            {'k': 't',
             'en': 'Task 4: do not trust the spacing. Count: A has 4 and B has 3. So A has more.',
             'ar': 'المهمة 4: لا تثق بالتباعد. عدّ: في A أربعة وفي B ثلاثة. إذن A has more.',
             'fr': "Tâche 4 : ne fais pas confiance à l'espacement. Compte : A en a 4 et B en a 3. A en a donc plus.",
             'label': None},
            {'k': 'f', 'f': '4 > 3      A has more.'},
            {'k': 't',
             'en': 'Task 5: B has fewer, because after pairing one object remains in A.',
             'ar': 'المهمة 5: B has fewer لأنه بعد المزاوجة يبقى شيء واحد في A.',
             'fr': "Tâche 5 : B en a moins, parce qu'après les paires il reste un objet dans A.",
             'label': None},
            {'k': 'f', 'f': 'B has fewer because one object remains in A.'}]}]


def scenes():
    return make_scenes(THEORY, EXERCISES)
