"""Direct lesson data: Grade 1 Mathematics — The numbers from 1 to 5.

Written once in three languages; every text step carries its own ar/en/fr twin."""
from __future__ import annotations

LESSON_ID = 'G01-MATH-EN-003'
GRADE = 1
SUBJECT = "math"
TITLES = {'en': 'The numbers from 1 to 5', 'ar': 'الأعداد من 1 إلى 5', 'fr': 'Les nombres de 1 à 5'}

from scripts.direct_lessons.common import T, F, D, EX, st, S, make_scenes


THEORY = [('Welcome back: warm-up',
  'أهلًا من جديد: تسخين',
  'De retour : échauffement',
  '18',
  [{'k': 't',
    'en': 'Welcome back! Last time we made friends with 1, 2 and 3. Today we add two new friends: 4 and 5.',
    'ar': 'أهلًا بك من جديد! في المرة الماضية صرنا أصدقاء مع 1 و2 و3. اليوم نضيف صديقين جديدين: 4 و5.',
    'fr': "Bon retour ! La dernière fois, nous avons rencontré 1, 2 et 3. Aujourd'hui, deux nouveaux amis arrivent : 4 et 5.",
    'label': None},
   {'k': 't',
    'en': 'As always, we do not memorise the shape of a number before we understand what it means.',
    'ar': 'وكما دائمًا لا نحفظ شكل الرقم قبل أن نفهم معناه.',
    'fr': "Comme toujours, on ne retient pas la forme d'un chiffre avant d'avoir compris son sens.",
    'label': None},
   {'k': 't',
    'en': 'Quick warm-up. Two stars: how many? Two.',
    'ar': 'تسخين سريع. نجمتان: كم نجمة؟ اثنتان.',
    'fr': 'Échauffement rapide. Deux étoiles : combien ? Deux.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<polygon id="e1" points="260.0,148.2 273.7,181.2 309.2,184.0 282.1,207.2 290.4,241.9 260.0,223.3 229.6,241.9 '
                    '237.9,207.2 210.8,184.0 246.3,181.2" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e2" '
                    'points="400.0,148.2 413.7,181.2 449.2,184.0 422.1,207.2 430.4,241.9 400.0,223.3 369.6,241.9 377.9,207.2 350.8,184.0 '
                    '386.3,181.2" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/>',
             'vb': [660, 440],
             'show': ['e1', 'e2']}},
   {'k': 't',
    'en': 'Three apples: how many? Three. Great, now we are ready to grow a little.',
    'ar': 'ثلاث تفاحات: كم تفاحة؟ ثلاث. ممتاز، نحن جاهزون لنكبر قليلًا.',
    'fr': 'Trois pommes : combien ? Trois. Très bien, nous sommes prêts à grandir un peu.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<g id="e1"><circle cx="200" cy="203" r="40" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><line x1="200" y1="163" '
                    'x2="205" y2="151" stroke="#7a4a1d" stroke-width="4"/><ellipse cx="211" cy="156" rx="8" ry="4" fill="#40c057" '
                    'stroke="#0b3d5c" stroke-width="2"/></g><g id="e2"><circle cx="330" cy="203" r="40" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><line x1="330" y1="163" x2="335" y2="151" stroke="#7a4a1d" stroke-width="4"/><ellipse cx="341" '
                    'cy="156" rx="8" ry="4" fill="#40c057" stroke="#0b3d5c" stroke-width="2"/></g><g id="e3"><circle cx="460" cy="203" '
                    'r="40" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><line x1="460" y1="163" x2="465" y2="151" stroke="#7a4a1d" '
                    'stroke-width="4"/><ellipse cx="471" cy="156" rx="8" ry="4" fill="#40c057" stroke="#0b3d5c" stroke-width="2"/></g>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3']}}]),
 ('Making 4 from 3 and 1 more',
  'نصنع 4 من 3 وواحد آخر',
  'Faire 4 avec 3 et 1 de plus',
  '18',
  [{'k': 't',
    'en': 'Here are 3 fish. Count them: one, two, three. We have 3.',
    'ar': 'هذه 3 أسماك. عدّها: one، two، three. عندنا 3.',
    'fr': 'Voici 3 poissons. Compte-les : one, two, three. Nous en avons 3.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<g id="e1"><polygon points="210,200 237,177 237,223" fill="#ff922b" stroke="#0b3d5c" stroke-width="3"/><ellipse '
                    'cx="180" cy="200" rx="38" ry="23" fill="#ffa94d" stroke="#0b3d5c" stroke-width="3"/><circle cx="161" cy="197" r="3" '
                    'fill="#0b3d5c"/></g><g id="e2"><polygon points="360,200 387,177 387,223" fill="#ff922b" stroke="#0b3d5c" '
                    'stroke-width="3"/><ellipse cx="330" cy="200" rx="38" ry="23" fill="#ffa94d" stroke="#0b3d5c" '
                    'stroke-width="3"/><circle cx="311" cy="197" r="3" fill="#0b3d5c"/></g><g id="e3"><polygon points="510,200 537,177 '
                    '537,223" fill="#ff922b" stroke="#0b3d5c" stroke-width="3"/><ellipse cx="480" cy="200" rx="38" ry="23" fill="#ffa94d" '
                    'stroke="#0b3d5c" stroke-width="3"/><circle cx="461" cy="197" r="3" fill="#0b3d5c"/></g>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3']}},
   {'k': 't',
    'en': 'Now I add one more fish. Do not answer too fast. We count all of them again: one, two, three, four.',
    'ar': 'الآن أضفت سمكة واحدة. لا تجب بسرعة. نعدّ كلها من جديد: one، two، three، four.',
    'fr': "Maintenant, j'ajoute un poisson de plus. Ne réponds pas trop vite. On les recompte tous : one, two, three, four.",
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<g id="e1"><polygon points="135,200 162,177 162,223" fill="#ff922b" stroke="#0b3d5c" stroke-width="3"/><ellipse '
                    'cx="105" cy="200" rx="38" ry="23" fill="#ffa94d" stroke="#0b3d5c" stroke-width="3"/><circle cx="86" cy="197" r="3" '
                    'fill="#0b3d5c"/></g><g id="e2"><polygon points="285,200 312,177 312,223" fill="#ff922b" stroke="#0b3d5c" '
                    'stroke-width="3"/><ellipse cx="255" cy="200" rx="38" ry="23" fill="#ffa94d" stroke="#0b3d5c" '
                    'stroke-width="3"/><circle cx="236" cy="197" r="3" fill="#0b3d5c"/></g><g id="e3"><polygon points="435,200 462,177 '
                    '462,223" fill="#ff922b" stroke="#0b3d5c" stroke-width="3"/><ellipse cx="405" cy="200" rx="38" ry="23" fill="#ffa94d" '
                    'stroke="#0b3d5c" stroke-width="3"/><circle cx="386" cy="197" r="3" fill="#0b3d5c"/></g><g id="e4"><polygon '
                    'points="585,200 612,177 612,223" fill="#ff922b" stroke="#0b3d5c" stroke-width="3"/><ellipse cx="555" cy="200" rx="38" '
                    'ry="23" fill="#ffa94d" stroke="#0b3d5c" stroke-width="3"/><circle cx="536" cy="197" r="3" fill="#0b3d5c"/></g>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4']}},
   {'k': 't',
    'en': 'What is the last number we said? Four. So how many fish are there now? Four.',
    'ar': 'ما آخر عدد قلناه؟ four. إذن كم سمكة الآن؟ أربع.',
    'fr': 'Quel est le dernier nombre dit ? Four. Combien y a-t-il de poissons maintenant ? Quatre.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<g id="e1"><polygon points="44,200 65,182 65,218" fill="#ff922b" stroke="#0b3d5c" stroke-width="3"/><ellipse cx="20" '
                    'cy="200" rx="30" ry="18" fill="#ffa94d" stroke="#0b3d5c" stroke-width="3"/><circle cx="5" cy="197" r="3" '
                    'fill="#0b3d5c"/></g><g id="e2"><polygon points="164,200 185,182 185,218" fill="#ff922b" stroke="#0b3d5c" '
                    'stroke-width="3"/><ellipse cx="140" cy="200" rx="30" ry="18" fill="#ffa94d" stroke="#0b3d5c" '
                    'stroke-width="3"/><circle cx="125" cy="197" r="3" fill="#0b3d5c"/></g><g id="e3"><polygon points="284,200 305,182 '
                    '305,218" fill="#ff922b" stroke="#0b3d5c" stroke-width="3"/><ellipse cx="260" cy="200" rx="30" ry="18" fill="#ffa94d" '
                    'stroke="#0b3d5c" stroke-width="3"/><circle cx="245" cy="197" r="3" fill="#0b3d5c"/></g><g id="e4"><polygon '
                    'points="404,200 425,182 425,218" fill="#ff922b" stroke="#0b3d5c" stroke-width="3"/><ellipse cx="380" cy="200" rx="30" '
                    'ry="18" fill="#ffa94d" stroke="#0b3d5c" stroke-width="3"/><circle cx="365" cy="197" r="3" fill="#0b3d5c"/></g><text '
                    'id="e5" x="480" y="225" font-size="60" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                    'fill="#0b3d5c">=</text><text id="e6" x="570" y="240" font-size="110" font-family="sans-serif" font-weight="bold" '
                    'text-anchor="middle" fill="#0b3d5c">4</text>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6']}},
   {'k': 'f', 'f': '3 fish + 1 fish = four = 4'},
   {'k': 't',
    'en': 'Notice: 3 objects, we add 1 object, and now we have 4. The number 4 means a collection with four things.',
    'ar': 'لاحظ: 3 أشياء، أضفنا شيئًا واحدًا، فصار عندنا 4. العدد 4 يعني مجموعة فيها أربعة أشياء.',
    'fr': 'Remarque : 3 objets, on en ajoute 1, et on en a 4. Le nombre 4 veut dire une collection de quatre objets.',
    'label': None}]),
 ('Making 5 from 4 and 1 more',
  'نصنع 5 من 4 وواحد آخر',
  'Faire 5 avec 4 et 1 de plus',
  '18',
  [{'k': 't',
    'en': 'Here are 4 strawberries. Count: one, two, three, four.',
    'ar': 'هنا 4 فراولات. عدّ: one، two، three، four.',
    'fr': 'Voici 4 fraises. Compte : one, two, three, four.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<g id="e1"><polygon points="116,180 184,180 150,237" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><polygon '
                    'points="126,180 150,163 174,180" fill="#40c057" stroke="#0b3d5c" stroke-width="3"/></g><g id="e2"><polygon '
                    'points="236,180 304,180 270,237" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><polygon points="246,180 270,163 '
                    '294,180" fill="#40c057" stroke="#0b3d5c" stroke-width="3"/></g><g id="e3"><polygon points="356,180 424,180 390,237" '
                    'fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><polygon points="366,180 390,163 414,180" fill="#40c057" '
                    'stroke="#0b3d5c" stroke-width="3"/></g><g id="e4"><polygon points="476,180 544,180 510,237" fill="#e03131" '
                    'stroke="#0b3d5c" stroke-width="3"/><polygon points="486,180 510,163 534,180" fill="#40c057" stroke="#0b3d5c" '
                    'stroke-width="3"/></g>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4']}},
   {'k': 't',
    'en': 'I add one new strawberry. We count again from the beginning: one, two, three, four, five.',
    'ar': 'أضفت فراولة جديدة. نعدّ من جديد من البداية: one، two، three، four، five.',
    'fr': "J'ajoute une fraise. On recompte depuis le début : one, two, three, four, five.",
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<g id="e1"><polygon points="78,181 142,181 110,235" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><polygon '
                    'points="88,181 110,165 132,181" fill="#40c057" stroke="#0b3d5c" stroke-width="3"/></g><g id="e2"><polygon '
                    'points="188,181 252,181 220,235" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><polygon points="198,181 220,165 '
                    '242,181" fill="#40c057" stroke="#0b3d5c" stroke-width="3"/></g><g id="e3"><polygon points="298,181 362,181 330,235" '
                    'fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><polygon points="308,181 330,165 352,181" fill="#40c057" '
                    'stroke="#0b3d5c" stroke-width="3"/></g><g id="e4"><polygon points="408,181 472,181 440,235" fill="#e03131" '
                    'stroke="#0b3d5c" stroke-width="3"/><polygon points="418,181 440,165 462,181" fill="#40c057" stroke="#0b3d5c" '
                    'stroke-width="3"/></g><g id="e5"><polygon points="518,181 582,181 550,235" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><polygon points="528,181 550,165 572,181" fill="#40c057" stroke="#0b3d5c" stroke-width="3"/></g>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5']}},
   {'k': 't',
    'en': 'The last number is five. So the new number is 5.',
    'ar': 'آخر عدد هو five. إذن العدد الجديد هو 5.',
    'fr': 'Le dernier nombre est five. Le nouveau nombre est donc 5.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<g id="e1"><polygon points="28,187 72,187 50,224" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><polygon '
                    'points="35,187 50,176 65,187" fill="#40c057" stroke="#0b3d5c" stroke-width="3"/></g><g id="e2"><polygon '
                    'points="98,187 142,187 120,224" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><polygon points="105,187 120,176 '
                    '135,187" fill="#40c057" stroke="#0b3d5c" stroke-width="3"/></g><g id="e3"><polygon points="168,187 212,187 190,224" '
                    'fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><polygon points="175,187 190,176 205,187" fill="#40c057" '
                    'stroke="#0b3d5c" stroke-width="3"/></g><g id="e4"><polygon points="238,187 282,187 260,224" fill="#e03131" '
                    'stroke="#0b3d5c" stroke-width="3"/><polygon points="245,187 260,176 275,187" fill="#40c057" stroke="#0b3d5c" '
                    'stroke-width="3"/></g><g id="e5"><polygon points="308,187 352,187 330,224" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><polygon points="315,187 330,176 345,187" fill="#40c057" stroke="#0b3d5c" '
                    'stroke-width="3"/></g><text id="e6" x="420" y="225" font-size="60" font-family="sans-serif" font-weight="bold" '
                    'text-anchor="middle" fill="#0b3d5c">=</text><text id="e7" x="530" y="240" font-size="110" font-family="sans-serif" '
                    'font-weight="bold" text-anchor="middle" fill="#0b3d5c">5</text>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7']}},
   {'k': 'f', 'f': '4 + 1 more = five = 5'},
   {'k': 't',
    'en': 'This is a collection of 5 strawberries: 4, and one more, gives 5.',
    'ar': 'هذه مجموعة من 5 فراولات: 4 وواحدة زيادة تعطينا 5.',
    'fr': 'Voici une collection de 5 fraises : 4 et une de plus font 5.',
    'label': None}]),
 ('The last counting word tells how many',
  'آخر كلمة في العدّ تخبرنا كم',
  'Le dernier mot du comptage dit combien',
  '19',
  [{'k': 't',
    'en': 'Here is a very important idea. Look at the fish and count: one, two, three, four.',
    'ar': 'هذه فكرة مهمة جدًا. انظر إلى السمك وعدّ: one، two، three، four.',
    'fr': 'Voici une idée très importante. Regarde les poissons et compte : one, two, three, four.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<g id="e1"><polygon points="135,200 162,177 162,223" fill="#ff922b" stroke="#0b3d5c" stroke-width="3"/><ellipse '
                    'cx="105" cy="200" rx="38" ry="23" fill="#ffa94d" stroke="#0b3d5c" stroke-width="3"/><circle cx="86" cy="197" r="3" '
                    'fill="#0b3d5c"/></g><g id="e2"><polygon points="285,200 312,177 312,223" fill="#ff922b" stroke="#0b3d5c" '
                    'stroke-width="3"/><ellipse cx="255" cy="200" rx="38" ry="23" fill="#ffa94d" stroke="#0b3d5c" '
                    'stroke-width="3"/><circle cx="236" cy="197" r="3" fill="#0b3d5c"/></g><g id="e3"><polygon points="435,200 462,177 '
                    '462,223" fill="#ff922b" stroke="#0b3d5c" stroke-width="3"/><ellipse cx="405" cy="200" rx="38" ry="23" fill="#ffa94d" '
                    'stroke="#0b3d5c" stroke-width="3"/><circle cx="386" cy="197" r="3" fill="#0b3d5c"/></g><g id="e4"><polygon '
                    'points="585,200 612,177 612,223" fill="#ff922b" stroke="#0b3d5c" stroke-width="3"/><ellipse cx="555" cy="200" rx="38" '
                    'ry="23" fill="#ffa94d" stroke="#0b3d5c" stroke-width="3"/><circle cx="536" cy="197" r="3" fill="#0b3d5c"/></g>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4']}},
   {'k': 't',
    'en': 'What is the last word? Four. This means the total number of fish is 4.',
    'ar': 'ما آخر كلمة؟ four. هذا يعني أن عدد السمك كله هو 4.',
    'fr': 'Quel est le dernier mot ? Four. Cela veut dire que le nombre total de poissons est 4.',
    'label': None},
   {'k': 't',
    'en': 'So the last counting word is not just the last sound we said. It tells us the whole quantity.',
    'ar': 'إذن آخر كلمة في العدّ ليست مجرد آخر صوت نقوله. إنها تخبرنا بالكمية كلها.',
    'fr': "Le dernier mot du comptage n'est donc pas seulement le dernier son prononcé. Il nous donne toute la quantité.",
    'label': None},
   {'k': 't',
    'en': 'Now a fifth fish joins. We count again: one, two, three, four, five. The last word is five, so the total is 5.',
    'ar': 'الآن انضمت سمكة خامسة. نعدّ من جديد: one، two، three، four، five. آخر كلمة five، إذن المجموع 5.',
    'fr': 'Maintenant, un cinquième poisson arrive. On recompte : one, two, three, four, five. Le dernier mot est five, le total est donc '
          '5.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<g id="e1"><polygon points="117,200 141,180 141,220" fill="#ff922b" stroke="#0b3d5c" stroke-width="3"/><ellipse '
                    'cx="90" cy="200" rx="34" ry="20" fill="#ffa94d" stroke="#0b3d5c" stroke-width="3"/><circle cx="73" cy="197" r="3" '
                    'fill="#0b3d5c"/></g><g id="e2"><polygon points="237,200 261,180 261,220" fill="#ff922b" stroke="#0b3d5c" '
                    'stroke-width="3"/><ellipse cx="210" cy="200" rx="34" ry="20" fill="#ffa94d" stroke="#0b3d5c" '
                    'stroke-width="3"/><circle cx="193" cy="197" r="3" fill="#0b3d5c"/></g><g id="e3"><polygon points="357,200 381,180 '
                    '381,220" fill="#ff922b" stroke="#0b3d5c" stroke-width="3"/><ellipse cx="330" cy="200" rx="34" ry="20" fill="#ffa94d" '
                    'stroke="#0b3d5c" stroke-width="3"/><circle cx="313" cy="197" r="3" fill="#0b3d5c"/></g><g id="e4"><polygon '
                    'points="477,200 501,180 501,220" fill="#ff922b" stroke="#0b3d5c" stroke-width="3"/><ellipse cx="450" cy="200" rx="34" '
                    'ry="20" fill="#ffa94d" stroke="#0b3d5c" stroke-width="3"/><circle cx="433" cy="197" r="3" fill="#0b3d5c"/></g><g '
                    'id="e5"><polygon points="597,200 621,180 621,220" fill="#ff922b" stroke="#0b3d5c" stroke-width="3"/><ellipse cx="570" '
                    'cy="200" rx="34" ry="20" fill="#ffa94d" stroke="#0b3d5c" stroke-width="3"/><circle cx="553" cy="197" r="3" '
                    'fill="#0b3d5c"/></g>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5']}}]),
 ('Moving things does not change how many',
  'تحريك الأشياء لا يغيّر العدد',
  'Déplacer ne change pas le nombre',
  '19',
  [{'k': 't',
    'en': 'Five dots stand in a row. Count: one, two, three, four, five. We have 5.',
    'ar': 'خمس نقاط في صف. عدّ: one، two، three، four، five. عندنا 5.',
    'fr': 'Cinq points sont alignés. Compte : one, two, three, four, five. Il y en a 5.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<circle id="e1" cx="130" cy="200" r="22" fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle id="e2" cx="230" '
                    'cy="200" r="22" fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle id="e3" cx="330" cy="200" r="22" '
                    'fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle id="e4" cx="430" cy="200" r="22" fill="#0b3d5c" '
                    'stroke="#0b3d5c" stroke-width="3"/><circle id="e5" cx="530" cy="200" r="22" fill="#0b3d5c" stroke="#0b3d5c" '
                    'stroke-width="3"/>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5']}},
   {'k': 't',
    'en': 'Now the dots move into a different shape. Is it 4 now? Is it 6? Let us not guess.',
    'ar': 'الآن تنتقل النقاط إلى شكل مختلف. هل صارت 4؟ أو 6؟ لا نخمّن.',
    'fr': 'Maintenant, les points forment une autre figure. Est-ce 4 ? Est-ce 6 ? Ne devinons pas.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<circle id="e1" cx="330" cy="80" r="23" fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle id="e2" cx="230" '
                    'cy="190" r="23" fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle id="e3" cx="430" cy="190" r="23" '
                    'fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle id="e4" cx="270" cy="320" r="23" fill="#0b3d5c" '
                    'stroke="#0b3d5c" stroke-width="3"/><circle id="e5" cx="390" cy="320" r="23" fill="#0b3d5c" stroke="#0b3d5c" '
                    'stroke-width="3"/>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5']}},
   {'k': 't',
    'en': 'We count: one, two, three, four, five. Still 5! We did not add a dot and we did not take one away.',
    'ar': 'نعدّ: one، two، three، four، five. ما زالت 5! لم نضف نقطة ولم نأخذ نقطة.',
    'fr': "On compte : one, two, three, four, five. Toujours 5 ! On n'a ni ajouté ni retiré de point.",
    'label': None},
   {'k': 't',
    'en': 'Same quantity, different arrangement.',
    'ar': 'الكمية نفسها والترتيب مختلف.',
    'fr': 'Même quantité, disposition différente.',
    'label': None},
   {'k': 't',
    'en': 'What about two groups of 4 stars, one close together and one spread out? Count each one: both have 4. The space does not change '
          'the quantity.',
    'ar': 'وماذا عن مجموعتين من 4 نجوم، واحدة متقاربة وواحدة متباعدة؟ عدّ كلًّا منهما: في كلتيهما 4. المسافة لا تغيّر الكمية.',
    'fr': "Et deux groupes de 4 étoiles, l'un serré, l'autre écarté ? Compte chacun : les deux en ont 4. L'espace ne change pas la "
          'quantité.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<polygon id="e1" points="248.0,82.4 255.3,100.0 274.2,101.5 259.8,113.8 264.2,132.3 248.0,122.4 231.8,132.3 '
                    '236.2,113.8 221.8,101.5 240.7,100.0" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e2" '
                    'points="302.0,82.4 309.3,100.0 328.2,101.5 313.8,113.8 318.2,132.3 302.0,122.4 285.8,132.3 290.2,113.8 275.8,101.5 '
                    '294.7,100.0" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e3" points="358.0,82.4 365.3,100.0 '
                    '384.2,101.5 369.8,113.8 374.2,132.3 358.0,122.4 341.8,132.3 346.2,113.8 331.8,101.5 350.7,100.0" fill="#ffd43b" '
                    'stroke="#0b3d5c" stroke-width="3"/><polygon id="e4" points="412.0,82.4 419.3,100.0 438.2,101.5 423.8,113.8 '
                    '428.2,132.3 412.0,122.4 395.8,132.3 400.2,113.8 385.8,101.5 404.7,100.0" fill="#ffd43b" stroke="#0b3d5c" '
                    'stroke-width="3"/><polygon id="e5" points="75.0,292.4 82.3,310.0 101.2,311.5 86.8,323.8 91.2,342.3 75.0,332.4 '
                    '58.8,342.3 63.2,323.8 48.8,311.5 67.7,310.0" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e6" '
                    'points="245.0,292.4 252.3,310.0 271.2,311.5 256.8,323.8 261.2,342.3 245.0,332.4 228.8,342.3 233.2,323.8 218.8,311.5 '
                    '237.7,310.0" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e7" points="415.0,292.4 422.3,310.0 '
                    '441.2,311.5 426.8,323.8 431.2,342.3 415.0,332.4 398.8,342.3 403.2,323.8 388.8,311.5 407.7,310.0" fill="#ffd43b" '
                    'stroke="#0b3d5c" stroke-width="3"/><polygon id="e8" points="585.0,292.4 592.3,310.0 611.2,311.5 596.8,323.8 '
                    '601.2,342.3 585.0,332.4 568.8,342.3 573.2,323.8 558.8,311.5 577.7,310.0" fill="#ffd43b" stroke="#0b3d5c" '
                    'stroke-width="3"/>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8']}}]),
 ('Matching 1, 2, 3, 4, 5',
  'نطابق 1 و2 و3 و4 و5',
  'Associer 1, 2, 3, 4, 5',
  '20',
  [{'k': 't',
    'en': 'Now we match groups with numbers, one group at a time. A has one star: we match it with 1. B has two stars: 2. C has three: 3. '
          'D has four: 4. E has five: 5.',
    'ar': 'الآن نطابق المجموعات بالأرقام، مجموعة بعد مجموعة. في A نجمة واحدة: نصلها بـ1. في B نجمتان: 2. في C ثلاث: 3. في D أربع: 4. في E '
          'خمس: 5.',
    'fr': 'Maintenant, on associe les groupes aux nombres, un groupe à la fois. A a une étoile : 1. B a deux étoiles : 2. C en a trois : '
          '3. D en a quatre : 4. E en a cinq : 5.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<text id="e1" x="40" y="60" font-size="28" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                    'fill="#0b3d5c">A</text><polygon id="e2" points="180.0,34.3 185.5,47.5 199.7,48.6 188.9,57.9 192.2,71.7 180.0,64.3 '
                    '167.8,71.7 171.1,57.9 160.3,48.6 174.5,47.5" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><text id="e3" x="520" '
                    'y="70" font-size="44" font-family="sans-serif" font-weight="bold" text-anchor="middle" fill="#0b3d5c">1</text><text '
                    'id="e4" x="40" y="135" font-size="28" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                    'fill="#0b3d5c">B</text><polygon id="e5" points="180.0,109.3 185.5,122.5 199.7,123.6 188.9,132.9 192.2,146.7 '
                    '180.0,139.3 167.8,146.7 171.1,132.9 160.3,123.6 174.5,122.5" fill="#ffd43b" stroke="#0b3d5c" '
                    'stroke-width="3"/><polygon id="e6" points="230.0,109.3 235.5,122.5 249.7,123.6 238.9,132.9 242.2,146.7 230.0,139.3 '
                    '217.8,146.7 221.1,132.9 210.3,123.6 224.5,122.5" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><text id="e7" '
                    'x="520" y="145" font-size="44" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                    'fill="#0b3d5c">2</text><text id="e8" x="40" y="210" font-size="28" font-family="sans-serif" font-weight="bold" '
                    'text-anchor="middle" fill="#0b3d5c">C</text><polygon id="e9" points="180.0,184.3 185.5,197.5 199.7,198.6 188.9,207.9 '
                    '192.2,221.7 180.0,214.3 167.8,221.7 171.1,207.9 160.3,198.6 174.5,197.5" fill="#ffd43b" stroke="#0b3d5c" '
                    'stroke-width="3"/><polygon id="e10" points="230.0,184.3 235.5,197.5 249.7,198.6 238.9,207.9 242.2,221.7 230.0,214.3 '
                    '217.8,221.7 221.1,207.9 210.3,198.6 224.5,197.5" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e11" '
                    'points="280.0,184.3 285.5,197.5 299.7,198.6 288.9,207.9 292.2,221.7 280.0,214.3 267.8,221.7 271.1,207.9 260.3,198.6 '
                    '274.5,197.5" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><text id="e12" x="520" y="220" font-size="44" '
                    'font-family="sans-serif" font-weight="bold" text-anchor="middle" fill="#0b3d5c">3</text><text id="e13" x="40" y="285" '
                    'font-size="28" font-family="sans-serif" font-weight="bold" text-anchor="middle" fill="#0b3d5c">D</text><polygon '
                    'id="e14" points="180.0,259.3 185.5,272.5 199.7,273.6 188.9,282.9 192.2,296.7 180.0,289.3 167.8,296.7 171.1,282.9 '
                    '160.3,273.6 174.5,272.5" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e15" points="230.0,259.3 '
                    '235.5,272.5 249.7,273.6 238.9,282.9 242.2,296.7 230.0,289.3 217.8,296.7 221.1,282.9 210.3,273.6 224.5,272.5" '
                    'fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e16" points="280.0,259.3 285.5,272.5 299.7,273.6 '
                    '288.9,282.9 292.2,296.7 280.0,289.3 267.8,296.7 271.1,282.9 260.3,273.6 274.5,272.5" fill="#ffd43b" stroke="#0b3d5c" '
                    'stroke-width="3"/><polygon id="e17" points="330.0,259.3 335.5,272.5 349.7,273.6 338.9,282.9 342.2,296.7 330.0,289.3 '
                    '317.8,296.7 321.1,282.9 310.3,273.6 324.5,272.5" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><text id="e18" '
                    'x="520" y="295" font-size="44" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                    'fill="#0b3d5c">4</text><text id="e19" x="40" y="360" font-size="28" font-family="sans-serif" font-weight="bold" '
                    'text-anchor="middle" fill="#0b3d5c">E</text><polygon id="e20" points="180.0,334.3 185.5,347.5 199.7,348.6 188.9,357.9 '
                    '192.2,371.7 180.0,364.3 167.8,371.7 171.1,357.9 160.3,348.6 174.5,347.5" fill="#ffd43b" stroke="#0b3d5c" '
                    'stroke-width="3"/><polygon id="e21" points="230.0,334.3 235.5,347.5 249.7,348.6 238.9,357.9 242.2,371.7 230.0,364.3 '
                    '217.8,371.7 221.1,357.9 210.3,348.6 224.5,347.5" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e22" '
                    'points="280.0,334.3 285.5,347.5 299.7,348.6 288.9,357.9 292.2,371.7 280.0,364.3 267.8,371.7 271.1,357.9 260.3,348.6 '
                    '274.5,347.5" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e23" points="330.0,334.3 335.5,347.5 '
                    '349.7,348.6 338.9,357.9 342.2,371.7 330.0,364.3 317.8,371.7 321.1,357.9 310.3,348.6 324.5,347.5" fill="#ffd43b" '
                    'stroke="#0b3d5c" stroke-width="3"/><polygon id="e24" points="380.0,334.3 385.5,347.5 399.7,348.6 388.9,357.9 '
                    '392.2,371.7 380.0,364.3 367.8,371.7 371.1,357.9 360.3,348.6 374.5,347.5" fill="#ffd43b" stroke="#0b3d5c" '
                    'stroke-width="3"/><text id="e25" x="520" y="370" font-size="44" font-family="sans-serif" font-weight="bold" '
                    'text-anchor="middle" fill="#0b3d5c">5</text>',
             'vb': [660, 440],
             'show': ['e1',
                      'e2',
                      'e3',
                      'e4',
                      'e5',
                      'e6',
                      'e7',
                      'e8',
                      'e9',
                      'e10',
                      'e11',
                      'e12',
                      'e13',
                      'e14',
                      'e15',
                      'e16',
                      'e17',
                      'e18',
                      'e19',
                      'e20',
                      'e21',
                      'e22',
                      'e23',
                      'e24',
                      'e25']}},
   {'k': 't',
    'en': 'Now we have a whole family of numbers.',
    'ar': 'صارت عندنا الآن عائلة كاملة من الأعداد.',
    'fr': 'Nous avons maintenant toute une famille de nombres.',
    'label': None},
   {'k': 'f', 'f': '1 → one      2 → two      3 → three      4 → four      5 → five'}]),
 ('Reading 4 and 5',
  'قراءة 4 و5',
  'Lire 4 et 5',
  '20',
  [{'k': 't',
    'en': 'This is the numeral 4. Say it with me: four.',
    'ar': 'هذا هو الرقم 4. قل معي: four.',
    'fr': 'Voici le chiffre 4. Dis avec moi : four.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<text id="e1" x="330" y="220" font-size="200" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                    'fill="#0b3d5c">4</text>',
             'vb': [660, 440],
             'show': ['e1']}},
   {'k': 't',
    'en': 'And this is the numeral 5. Say: five.',
    'ar': 'وهذا هو الرقم 5. قل: five.',
    'fr': 'Et voici le chiffre 5. Dis : five.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<text id="e1" x="330" y="220" font-size="200" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                    'fill="#0b3d5c">5</text>',
             'vb': [660, 440],
             'show': ['e1']}},
   {'k': 't',
    'en': 'The shape alone is not enough. 4 must remind you of four things, and 5 of five things.',
    'ar': 'الشكل وحده لا يكفي. يجب أن يذكّرك 4 بأربعة أشياء، و5 بخمسة أشياء.',
    'fr': 'La forme seule ne suffit pas. 4 doit te faire penser à quatre objets, et 5 à cinq objets.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<text id="e1" x="90" y="120" font-size="80" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                    'fill="#0b3d5c">4</text><circle id="e2" cx="210" cy="105" r="26" fill="#4dabf7" stroke="#0b3d5c" '
                    'stroke-width="3"/><circle id="e3" cx="290" cy="105" r="26" fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/><circle '
                    'id="e4" cx="370" cy="105" r="26" fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/><circle id="e5" cx="450" cy="105" '
                    'r="26" fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/><text id="e6" x="90" y="300" font-size="80" '
                    'font-family="sans-serif" font-weight="bold" text-anchor="middle" fill="#0b3d5c">5</text><circle id="e7" cx="170" '
                    'cy="285" r="26" fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/><circle id="e8" cx="250" cy="285" r="26" '
                    'fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/><circle id="e9" cx="330" cy="285" r="26" fill="#4dabf7" '
                    'stroke="#0b3d5c" stroke-width="3"/><circle id="e10" cx="410" cy="285" r="26" fill="#4dabf7" stroke="#0b3d5c" '
                    'stroke-width="3"/><circle id="e11" cx="490" cy="285" r="26" fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10', 'e11']}},
   {'k': 't',
    'en': 'Trace 4 and 5 with your finger on the dotted lines. Well done.',
    'ar': 'تتبّع 4 و5 بإصبعك على الخطوط المنقّطة. أحسنت.',
    'fr': 'Suis 4 et 5 du doigt sur les pointillés. Bravo.',
    'label': None}]),
 ('Mistakes to avoid',
  'أخطاء يجب تجنّبها',
  'Erreurs à éviter',
  '21',
  [{'k': 't',
    'en': 'Mistake 1: skipping an object. If you count one, two, three, four, but there are 5 stars, you probably forgot one. Touch each '
          'object once.',
    'ar': 'الخطأ 1: نسيان شيء. إذا عددت one، two، three، four وعندك 5 نجوم فربما نسيت نجمة. المس كل شيء مرة واحدة.',
    'fr': "Erreur 1 : oublier un objet. Si tu comptes one, two, three, four alors qu'il y a 5 étoiles, tu en as sans doute oublié une. "
          'Touche chaque objet une fois.',
    'label': None},
   {'k': 't',
    'en': 'Mistake 2: counting one object twice. If you touch the same star twice, your number is too big. Each object gets one count '
          'only.',
    'ar': 'الخطأ 2: عدّ الشيء نفسه مرتين. إذا لمست النجمة نفسها مرتين يصير عددك أكبر من الحقيقة. كل شيء يُعدّ مرة واحدة فقط.',
    'fr': 'Erreur 2 : compter deux fois le même objet. Si tu touches la même étoile deux fois, ton nombre est trop grand. Chaque objet est '
          'compté une seule fois.',
    'label': None},
   {'k': 't',
    'en': 'Mistake 3: thinking wide spacing means more. Look at 4 dots far apart and 5 dots close together. Which has more? Count: 4 and '
          '5. So 5 dots is more, even when they are close.',
    'ar': 'الخطأ 3: ظن أن التباعد يعني أكثر. انظر إلى 4 نقاط متباعدة و5 نقاط متقاربة. أيّهما أكثر؟ نعدّ: 4 و5. إذن 5 نقاط أكثر حتى لو كانت '
          'متقاربة.',
    'fr': "Erreur 3 : croire que l'écart signifie plus. Regarde 4 points écartés et 5 points serrés. Lequel en a plus ? On compte : 4 et "
          '5. Les 5 points sont donc plus nombreux, même serrés.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<circle id="e1" cx="105" cy="110" r="16" fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle id="e2" cx="255" '
                    'cy="110" r="16" fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle id="e3" cx="405" cy="110" r="16" '
                    'fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle id="e4" cx="555" cy="110" r="16" fill="#0b3d5c" '
                    'stroke="#0b3d5c" stroke-width="3"/><circle id="e5" cx="226" cy="320" r="16" fill="#0b3d5c" stroke="#0b3d5c" '
                    'stroke-width="3"/><circle id="e6" cx="278" cy="320" r="16" fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle '
                    'id="e7" cx="330" cy="320" r="16" fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle id="e8" cx="382" cy="320" '
                    'r="16" fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle id="e9" cx="434" cy="320" r="16" fill="#0b3d5c" '
                    'stroke="#0b3d5c" stroke-width="3"/>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9']}},
   {'k': 't',
    'en': 'Mistake 4: the numeral says 5 but we built 4. That is a mismatch. We always check by counting.',
    'ar': 'الخطأ 4: الرقم المكتوب 5 لكننا بنينا 4. هذا عدم تطابق. نتحقّق دائمًا بالعدّ.',
    'fr': 'Erreur 4 : le chiffre écrit est 5 mais on a construit 4. Cela ne correspond pas. On vérifie toujours en comptant.',
    'label': None}]),
 ('Summary',
  'الخلاصة',
  'Résumé',
  '21',
  [{'k': 't',
    'en': 'Excellent! Today we have 1, 2, 3, 4, 5.',
    'ar': 'ممتاز! صار عندنا اليوم 1 و2 و3 و4 و5.',
    'fr': "Excellent ! Aujourd'hui, nous avons 1, 2, 3, 4, 5.",
    'label': None},
   {'k': 'f', 'f': '1 — 2 — 3 — 4 — 5'},
   {'k': 't',
    'en': 'Every numeral has a quantity. When we count, each object is touched once, and the last number tells us the total.',
    'ar': 'لكل رقم كمية. وعندما نعدّ نلمس كل شيء مرة واحدة، وآخر عدد يخبرنا بالمجموع.',
    'fr': 'Chaque chiffre a une quantité. Quand on compte, on touche chaque objet une fois, et le dernier nombre donne le total.',
    'label': None},
   {'k': 't',
    'en': 'If things move, the number does not change unless we add or take away.',
    'ar': 'إذا تحرّكت الأشياء لا يتغيّر العدد ما لم نضف أو نأخذ.',
    'fr': 'Si les objets bougent, le nombre ne change pas, sauf si on ajoute ou on enlève.',
    'label': None},
   {'k': 'f', 'f': 'TOUCH → COUNT → LAST NUMBER → MATCH → CHECK'},
   {'k': 't',
    'en': 'And when you see a numeral: read it, build the quantity, count, and check.',
    'ar': 'وإذا رأيت رقمًا: اقرأه، ابنِ الكمية، عدّ، ثم تحقّق.',
    'fr': 'Et quand tu vois un chiffre : lis-le, construis la quantité, compte, puis vérifie.',
    'label': None},
   {'k': 'f', 'f': 'READ → BUILD THE QUANTITY → COUNT → CHECK'}])]


EXERCISES = [{'n': '1',
  'page': '18',
  'stmt': ('Make 4: build 4 stars in the box.', 'ابنِ 4 نجوم في الصندوق.', 'Fais 4 : construis 4 étoiles dans la boîte.'),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<rect id="e1" x="80" y="70" width="500" height="150" rx="10" fill="none" stroke="#0b3d5c" stroke-width="4" '
                             'stroke-dasharray="10 8"/><polygon id="e2" points="165.0,103.6 176.0,129.9 204.4,132.2 182.7,150.8 '
                             '189.3,178.5 165.0,163.6 140.7,178.5 147.3,150.8 125.6,132.2 154.0,129.9" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/><polygon id="e3" points="275.0,103.6 286.0,129.9 314.4,132.2 292.7,150.8 299.3,178.5 '
                             '275.0,163.6 250.7,178.5 257.3,150.8 235.6,132.2 264.0,129.9" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/><polygon id="e4" points="385.0,103.6 396.0,129.9 424.4,132.2 402.7,150.8 409.3,178.5 '
                             '385.0,163.6 360.7,178.5 367.3,150.8 345.6,132.2 374.0,129.9" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/><polygon id="e5" points="495.0,103.6 506.0,129.9 534.4,132.2 512.7,150.8 519.3,178.5 '
                             '495.0,163.6 470.7,178.5 477.3,150.8 455.6,132.2 484.0,129.9" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4', 'e5']}},
            {'k': 't',
             'en': 'We need four stars. Put them in one by one and count: one, two, three, four.',
             'ar': 'نحتاج إلى أربع نجوم. نضعها واحدة واحدة ونعدّ: one، two، three، four.',
             'fr': 'Il faut quatre étoiles. On les met une par une et on compte : one, two, three, four.',
             'label': None},
            {'k': 't',
             'en': 'If we had only 3 stars, we would add one more. If we had 5 or more, we would take away the extra star.',
             'ar': 'لو كان عندنا 3 نجوم فقط لأضفنا واحدة. ولو كان عندنا 5 أو أكثر لأزلنا النجمة الزائدة.',
             'fr': "Avec seulement 3 étoiles, on en ajouterait une. Avec 5 ou plus, on retirerait l'étoile en trop.",
             'label': None},
            {'k': 'f', 'f': '4 → ⭐ ⭐ ⭐ ⭐'},
            {'k': 't',
             'en': 'You understood 4 as a quantity, not only as a shape.',
             'ar': 'فهمت 4 ككمية وليس كشكل فقط.',
             'fr': 'Tu as compris 4 comme une quantité, pas seulement comme une forme.',
             'label': None}]},
 {'n': '2',
  'page': '18',
  'stmt': ('Count the circles with one touch for each, then choose the numeral: 3, 4 or 5.',
           'عدّ الدوائر بلمسة واحدة لكل دائرة، ثم اختر الرقم: 3 أو 4 أو 5.',
           'Compte les cercles en touchant chacun une fois, puis choisis le chiffre : 3, 4 ou 5.'),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<circle id="e1" cx="130" cy="110" r="34" fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/><circle id="e2" '
                             'cx="230" cy="110" r="34" fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/><circle id="e3" cx="330" cy="110" '
                             'r="34" fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/><circle id="e4" cx="430" cy="110" r="34" '
                             'fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/><circle id="e5" cx="530" cy="110" r="34" fill="#4dabf7" '
                             'stroke="#0b3d5c" stroke-width="3"/><rect id="e6" x="140" y="255" width="80" height="90" rx="10" '
                             'fill="#fff3bf" stroke="#0b3d5c" stroke-width="4"/><text id="e7" x="180" y="322" font-size="64" '
                             'font-family="sans-serif" font-weight="bold" text-anchor="middle" fill="#0b3d5c">3</text><rect id="e8" '
                             'x="290" y="255" width="80" height="90" rx="10" fill="#fff3bf" stroke="#0b3d5c" stroke-width="4"/><text '
                             'id="e9" x="330" y="322" font-size="64" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                             'fill="#0b3d5c">4</text><rect id="e10" x="440" y="255" width="80" height="90" rx="10" fill="#fff3bf" '
                             'stroke="#0b3d5c" stroke-width="4"/><text id="e11" x="480" y="322" font-size="64" font-family="sans-serif" '
                             'font-weight="bold" text-anchor="middle" fill="#0b3d5c">5</text>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10', 'e11']}},
            {'k': 't',
             'en': 'Touch each circle once: one, two, three, four, five.',
             'ar': 'المس كل دائرة مرة: one، two، three، four، five.',
             'fr': 'Touche chaque cercle une fois : one, two, three, four, five.',
             'label': None},
            {'k': 't',
             'en': 'The last number is five, so we choose the numeral 5.',
             'ar': 'آخر عدد هو five، إذن نختار الرقم 5.',
             'fr': 'Le dernier nombre est five, on choisit donc le chiffre 5.',
             'label': None},
            {'k': 'f', 'f': '🔵 🔵 🔵 🔵 🔵 = 5'}]},
 {'n': '3',
  'page': '19',
  'stmt': ('Count the yellow circles out loud. What is the last number? How many yellow circles are there?',
           'عدّ الدوائر الصفراء بصوتك. ما آخر عدد؟ وكم دائرة صفراء؟',
           'Compte les cercles jaunes à voix haute. Quel est le dernier nombre ? Combien y a-t-il de cercles jaunes ?'),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<circle id="e1" cx="150" cy="200" r="38" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><circle id="e2" '
                             'cx="270" cy="200" r="38" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><circle id="e3" cx="390" cy="200" '
                             'r="38" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><circle id="e4" cx="510" cy="200" r="38" '
                             'fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4']}},
            {'k': 't',
             'en': 'Count: one, two, three, four.',
             'ar': 'عدّ: one، two، three، four.',
             'fr': 'Compte : one, two, three, four.',
             'label': None},
            {'k': 't',
             'en': 'The last word we said is four. So there are four yellow circles.',
             'ar': 'آخر كلمة قلناها four. إذن توجد أربع دوائر صفراء.',
             'fr': 'Le dernier mot dit est four. Il y a donc quatre cercles jaunes.',
             'label': None},
            {'k': 'f', 'f': '4'}]},
 {'n': '4',
  'page': '19',
  'stmt': ('Group A has 4 close stars. Group B has 4 stars spread out. Which group has more?',
           'المجموعة A فيها 4 نجوم متقاربة، والمجموعة B فيها 4 نجوم متباعدة. أي مجموعة فيها أكثر؟',
           'Le groupe A a 4 étoiles serrées. Le groupe B a 4 étoiles écartées. Quel groupe en a le plus ?'),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<text id="e1" x="40" y="105" font-size="36" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                             'fill="#0b3d5c">A</text><polygon id="e2" points="248.0,72.4 255.3,90.0 274.2,91.5 259.8,103.8 264.2,122.3 '
                             '248.0,112.4 231.8,122.3 236.2,103.8 221.8,91.5 240.7,90.0" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/><polygon id="e3" points="302.0,72.4 309.3,90.0 328.2,91.5 313.8,103.8 318.2,122.3 '
                             '302.0,112.4 285.8,122.3 290.2,103.8 275.8,91.5 294.7,90.0" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/><polygon id="e4" points="358.0,72.4 365.3,90.0 384.2,91.5 369.8,103.8 374.2,122.3 '
                             '358.0,112.4 341.8,122.3 346.2,103.8 331.8,91.5 350.7,90.0" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/><polygon id="e5" points="412.0,72.4 419.3,90.0 438.2,91.5 423.8,103.8 428.2,122.3 '
                             '412.0,112.4 395.8,122.3 400.2,103.8 385.8,91.5 404.7,90.0" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/><text id="e6" x="40" y="305" font-size="36" font-family="sans-serif" font-weight="bold" '
                             'text-anchor="middle" fill="#0b3d5c">B</text><polygon id="e7" points="115.0,272.4 122.3,290.0 141.2,291.5 '
                             '126.8,303.8 131.2,322.3 115.0,312.4 98.8,322.3 103.2,303.8 88.8,291.5 107.7,290.0" fill="#ffd43b" '
                             'stroke="#0b3d5c" stroke-width="3"/><polygon id="e8" points="265.0,272.4 272.3,290.0 291.2,291.5 276.8,303.8 '
                             '281.2,322.3 265.0,312.4 248.8,322.3 253.2,303.8 238.8,291.5 257.7,290.0" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/><polygon id="e9" points="415.0,272.4 422.3,290.0 441.2,291.5 426.8,303.8 431.2,322.3 '
                             '415.0,312.4 398.8,322.3 403.2,303.8 388.8,291.5 407.7,290.0" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/><polygon id="e10" points="565.0,272.4 572.3,290.0 591.2,291.5 576.8,303.8 581.2,322.3 '
                             '565.0,312.4 548.8,322.3 553.2,303.8 538.8,291.5 557.7,290.0" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10']}},
            {'k': 't',
             'en': 'Group B looks bigger because it is spread out. But we do not decide from the space.',
             'ar': 'تبدو B أكبر لأنها متباعدة. لكننا لا نقرّر من المسافة.',
             'fr': "Le groupe B paraît plus grand car il est écarté. Mais on ne décide pas d'après l'espace.",
             'label': None},
            {'k': 't',
             'en': 'Count A: one, two, three, four. Count B: one, two, three, four.',
             'ar': 'عدّ A: one، two، three، four. عدّ B: one، two، three، four.',
             'fr': 'Compte A : one, two, three, four. Compte B : one, two, three, four.',
             'label': None},
            {'k': 'f', 'f': 'A = 4      B = 4'},
            {'k': 't',
             'en': 'Both have 4. The distance does not change the quantity.',
             'ar': 'في كلتيهما 4. المسافة لا تغيّر الكمية.',
             'fr': 'Les deux en ont 4. La distance ne change pas la quantité.',
             'label': None}]},
 {'n': '5',
  'page': '20',
  'stmt': ('A numeral is given. Build 4 blocks, then build 5 blocks.',
           'يظهر رقم. ابنِ 4 مكعبات، ثم ابنِ 5 مكعبات.',
           'Un chiffre est donné. Construis 4 blocs, puis 5 blocs.'),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<text id="e1" x="70" y="130" font-size="70" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                             'fill="#0b3d5c">4</text><rect id="e2" x="190" y="85" width="60" height="60" fill="#e03131" stroke="#0b3d5c" '
                             'stroke-width="3"/><rect id="e3" x="270" y="85" width="60" height="60" fill="#e03131" stroke="#0b3d5c" '
                             'stroke-width="3"/><rect id="e4" x="350" y="85" width="60" height="60" fill="#e03131" stroke="#0b3d5c" '
                             'stroke-width="3"/><rect id="e5" x="430" y="85" width="60" height="60" fill="#e03131" stroke="#0b3d5c" '
                             'stroke-width="3"/><text id="e6" x="70" y="320" font-size="70" font-family="sans-serif" font-weight="bold" '
                             'text-anchor="middle" fill="#0b3d5c">5</text><rect id="e7" x="150" y="275" width="60" height="60" '
                             'fill="#339af0" stroke="#0b3d5c" stroke-width="3"/><rect id="e8" x="230" y="275" width="60" height="60" '
                             'fill="#339af0" stroke="#0b3d5c" stroke-width="3"/><rect id="e9" x="310" y="275" width="60" height="60" '
                             'fill="#339af0" stroke="#0b3d5c" stroke-width="3"/><rect id="e10" x="390" y="275" width="60" height="60" '
                             'fill="#339af0" stroke="#0b3d5c" stroke-width="3"/><rect id="e11" x="470" y="275" width="60" height="60" '
                             'fill="#339af0" stroke="#0b3d5c" stroke-width="3"/>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10', 'e11']}},
            {'k': 't',
             'en': 'For 4 we build four blocks. Check: one, two, three, four.',
             'ar': 'من أجل 4 نبني أربعة مكعبات. تحقّق: one، two، three، four.',
             'fr': 'Pour 4, on construit quatre blocs. Vérifie : one, two, three, four.',
             'label': None},
            {'k': 't',
             'en': 'For 5 we build five blocks. Check: one, two, three, four, five.',
             'ar': 'من أجل 5 نبني خمسة مكعبات. تحقّق: one، two، three، four، five.',
             'fr': 'Pour 5, on construit cinq blocs. Vérifie : one, two, three, four, five.',
             'label': None},
            {'k': 't',
             'en': 'Always count what is already there first, then decide whether to add or take away. Do not keep dragging before '
                   'counting.',
             'ar': 'عدّ أولًا ما هو موجود، ثم قرّر هل تزيد أم تنقص. لا تستمر في السحب قبل العدّ.',
             'fr': "Compte d'abord ce qui est déjà là, puis décide s'il faut ajouter ou enlever. Ne continue pas à glisser avant d'avoir "
                   'compté.',
             'label': None}]},
 {'n': '6',
  'page': '21',
  'stmt': ('Find the mistake: four teddy bears and the numeral 5 under them.',
           'جد الخطأ: أربعة دببة وتحتها الرقم 5.',
           "Trouve l'erreur : quatre nounours et le chiffre 5 en dessous."),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<g id="e1"><circle cx="103" cy="118" r="16" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle '
                             'cx="167" cy="118" r="16" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="135" cy="150" r="40" '
                             'fill="#c98f55" stroke="#0b3d5c" stroke-width="3"/><circle cx="128" cy="146" r="3" fill="#0b3d5c"/><circle '
                             'cx="142" cy="146" r="3" fill="#0b3d5c"/><ellipse cx="135" cy="157" rx="6" ry="4" fill="#f1d3a8" '
                             'stroke="#0b3d5c" stroke-width="2"/></g><g id="e2"><circle cx="233" cy="118" r="16" fill="#a9703c" '
                             'stroke="#0b3d5c" stroke-width="3"/><circle cx="297" cy="118" r="16" fill="#a9703c" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle cx="265" cy="150" r="40" fill="#c98f55" stroke="#0b3d5c" stroke-width="3"/><circle '
                             'cx="258" cy="146" r="3" fill="#0b3d5c"/><circle cx="272" cy="146" r="3" fill="#0b3d5c"/><ellipse cx="265" '
                             'cy="157" rx="6" ry="4" fill="#f1d3a8" stroke="#0b3d5c" stroke-width="2"/></g><g id="e3"><circle cx="363" '
                             'cy="118" r="16" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="427" cy="118" r="16" '
                             'fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="395" cy="150" r="40" fill="#c98f55" '
                             'stroke="#0b3d5c" stroke-width="3"/><circle cx="388" cy="146" r="3" fill="#0b3d5c"/><circle cx="402" cy="146" '
                             'r="3" fill="#0b3d5c"/><ellipse cx="395" cy="157" rx="6" ry="4" fill="#f1d3a8" stroke="#0b3d5c" '
                             'stroke-width="2"/></g><g id="e4"><circle cx="493" cy="118" r="16" fill="#a9703c" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle cx="557" cy="118" r="16" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle '
                             'cx="525" cy="150" r="40" fill="#c98f55" stroke="#0b3d5c" stroke-width="3"/><circle cx="518" cy="146" r="3" '
                             'fill="#0b3d5c"/><circle cx="532" cy="146" r="3" fill="#0b3d5c"/><ellipse cx="525" cy="157" rx="6" ry="4" '
                             'fill="#f1d3a8" stroke="#0b3d5c" stroke-width="2"/></g><text id="e5" x="330" y="330" font-size="110" '
                             'font-family="sans-serif" font-weight="bold" text-anchor="middle" fill="#0b3d5c">5</text>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4', 'e5']}},
            {'k': 't',
             'en': 'Count the teddy bears: one, two, three, four. There are 4.',
             'ar': 'عدّ الدببة: one، two، three، four. عددها 4.',
             'fr': 'Compte les nounours : one, two, three, four. Il y en a 4.',
             'label': None},
            {'k': 't',
             'en': 'The numeral written is 5. Does 5 match 4? No.',
             'ar': 'الرقم المكتوب 5. هل يطابق 4؟ لا.',
             'fr': 'Le chiffre écrit est 5. 5 correspond-il à 4 ? Non.',
             'label': None},
            {'k': 't',
             'en': 'The correction: we write 4 instead of 5.',
             'ar': 'التصحيح: نكتب 4 بدل 5.',
             'fr': 'La correction : on écrit 4 à la place de 5.',
             'label': None},
            {'k': 'f', 'f': '🧸 🧸 🧸 🧸 → 4'}]},
 {'n': '7',
  'page': '21',
  'stmt': ('Put the boxes in order from the fewest to the most: A has 2, B has 5, C has 4, D has 1, E has 3.',
           'رتّب الصناديق من الأقل إلى الأكثر: A فيه 2، B فيه 5، C فيه 4، D فيه 1، E فيه 3.',
           'Range les boîtes du moins au plus : A a 2, B a 5, C a 4, D a 1, E a 3.'),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<text id="e1" x="66" y="70" font-size="30" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                             'fill="#0b3d5c">A</text><circle id="e2" cx="41" cy="120" r="16" fill="#0b3d5c" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle id="e3" cx="91" cy="120" r="16" fill="#0b3d5c" stroke="#0b3d5c" '
                             'stroke-width="3"/><text id="e4" x="198" y="70" font-size="30" font-family="sans-serif" font-weight="bold" '
                             'text-anchor="middle" fill="#0b3d5c">B</text><circle id="e5" cx="150" cy="120" r="8" fill="#0b3d5c" '
                             'stroke="#0b3d5c" stroke-width="3"/><circle id="e6" cx="174" cy="120" r="8" fill="#0b3d5c" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle id="e7" cx="198" cy="120" r="8" fill="#0b3d5c" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle id="e8" cx="222" cy="120" r="8" fill="#0b3d5c" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle id="e9" cx="246" cy="120" r="8" fill="#0b3d5c" stroke="#0b3d5c" '
                             'stroke-width="3"/><text id="e10" x="330" y="70" font-size="30" font-family="sans-serif" font-weight="bold" '
                             'text-anchor="middle" fill="#0b3d5c">C</text><circle id="e11" cx="288" cy="120" r="8" fill="#0b3d5c" '
                             'stroke="#0b3d5c" stroke-width="3"/><circle id="e12" cx="316" cy="120" r="8" fill="#0b3d5c" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle id="e13" cx="344" cy="120" r="8" fill="#0b3d5c" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle id="e14" cx="372" cy="120" r="8" fill="#0b3d5c" stroke="#0b3d5c" '
                             'stroke-width="3"/><text id="e15" x="462" y="70" font-size="30" font-family="sans-serif" font-weight="bold" '
                             'text-anchor="middle" fill="#0b3d5c">D</text><circle id="e16" cx="462" cy="120" r="16" fill="#0b3d5c" '
                             'stroke="#0b3d5c" stroke-width="3"/><text id="e17" x="594" y="70" font-size="30" font-family="sans-serif" '
                             'font-weight="bold" text-anchor="middle" fill="#0b3d5c">E</text><circle id="e18" cx="560" cy="120" r="8" '
                             'fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle id="e19" cx="594" cy="120" r="8" fill="#0b3d5c" '
                             'stroke="#0b3d5c" stroke-width="3"/><circle id="e20" cx="628" cy="120" r="8" fill="#0b3d5c" stroke="#0b3d5c" '
                             'stroke-width="3"/>',
                      'vb': [660, 440],
                      'show': ['e1',
                               'e2',
                               'e3',
                               'e4',
                               'e5',
                               'e6',
                               'e7',
                               'e8',
                               'e9',
                               'e10',
                               'e11',
                               'e12',
                               'e13',
                               'e14',
                               'e15',
                               'e16',
                               'e17',
                               'e18',
                               'e19',
                               'e20']}},
            {'k': 't',
             'en': 'First count each box: A is 2, B is 5, C is 4, D is 1, E is 3.',
             'ar': 'أولًا نعدّ كل صندوق: A هو 2، B هو 5، C هو 4، D هو 1، E هو 3.',
             'fr': "D'abord on compte chaque boîte : A est 2, B est 5, C est 4, D est 1, E est 3.",
             'label': None},
            {'k': 't',
             'en': 'Who has the smallest quantity? D, with 1. Then A with 2, then E with 3, then C with 4, then B with 5.',
             'ar': 'من عنده أصغر كمية؟ D ومعه 1. بعده A ومعه 2، ثم E ومعه 3، ثم C ومعه 4، ثم B ومعه 5.',
             'fr': 'Qui a la plus petite quantité ? D, avec 1. Puis A avec 2, puis E avec 3, puis C avec 4, puis B avec 5.',
             'label': None},
            {'k': 'f', 'f': 'D → A → E → C → B'},
            {'k': 'f', 'f': '1 → 2 → 3 → 4 → 5'}]},
 {'n': '8',
  'page': '21',
  'stmt': ('Final challenge. 1) Count 5 objects. 2) Choose the numeral for 4 circles. 3) Build 3. 4) 4 dots in a row and 4 dots in a '
           'square: same number or different? 5) Read 5, 2, 4, 1, 3.',
           'التحدي الأخير. 1) عدّ 5 أشياء. 2) اختر الرقم لـ4 دوائر. 3) ابنِ 3. 4) 4 نقاط في صف و4 نقاط في مربع: العدد نفسه أم مختلف؟ 5) '
           'اقرأ 5 و2 و4 و1 و3.',
           'Défi final. 1) Compte 5 objets. 2) Choisis le chiffre pour 4 cercles. 3) Construis 3. 4) 4 points en ligne et 4 points en '
           'carré : même nombre ou différent ? 5) Lis 5, 2, 4, 1, 3.'),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<polygon id="e1" points="130.0,163.2 139.7,186.6 165.0,188.6 145.7,205.1 151.6,229.8 130.0,216.6 108.4,229.8 '
                             '114.3,205.1 95.0,188.6 120.3,186.6" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e2" '
                             'points="230.0,163.2 239.7,186.6 265.0,188.6 245.7,205.1 251.6,229.8 230.0,216.6 208.4,229.8 214.3,205.1 '
                             '195.0,188.6 220.3,186.6" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e3" '
                             'points="330.0,163.2 339.7,186.6 365.0,188.6 345.7,205.1 351.6,229.8 330.0,216.6 308.4,229.8 314.3,205.1 '
                             '295.0,188.6 320.3,186.6" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e4" '
                             'points="430.0,163.2 439.7,186.6 465.0,188.6 445.7,205.1 451.6,229.8 430.0,216.6 408.4,229.8 414.3,205.1 '
                             '395.0,188.6 420.3,186.6" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e5" '
                             'points="530.0,163.2 539.7,186.6 565.0,188.6 545.7,205.1 551.6,229.8 530.0,216.6 508.4,229.8 514.3,205.1 '
                             '495.0,188.6 520.3,186.6" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4', 'e5']}},
            {'k': 't',
             'en': 'Task 1: touch each once: one, two, three, four, five. There are 5.',
             'ar': 'المهمة 1: المس كل شيء مرة: one، two، three، four، five. عددها 5.',
             'fr': 'Tâche 1 : touche chaque objet une fois : one, two, three, four, five. Il y en a 5.',
             'label': None},
            {'k': 'f', 'f': '5'},
            {'k': 't',
             'en': 'Task 2: four circles: count one, two, three, four. The numeral is 4.',
             'ar': 'المهمة 2: أربع دوائر: عدّ one، two، three، four. الرقم 4.',
             'fr': 'Tâche 2 : quatre cercles : compte one, two, three, four. Le chiffre est 4.',
             'label': None},
            {'k': 'f', 'f': '🔵 🔵 🔵 🔵 → 4'},
            {'k': 't',
             'en': 'Task 3: build three objects. Check: one, two, three.',
             'ar': 'المهمة 3: ابنِ ثلاثة أشياء. تحقّق: one، two، three.',
             'fr': 'Tâche 3 : construis trois objets. Vérifie : one, two, three.',
             'label': None},
            {'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<circle id="e1" cx="80" cy="130" r="13" fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle id="e2" '
                             'cx="140" cy="130" r="13" fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle id="e3" cx="200" cy="130" '
                             'r="13" fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle id="e4" cx="260" cy="130" r="13" '
                             'fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle id="e5" cx="430" cy="70" r="22" fill="#0b3d5c" '
                             'stroke="#0b3d5c" stroke-width="3"/><circle id="e6" cx="510" cy="70" r="22" fill="#0b3d5c" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle id="e7" cx="430" cy="150" r="22" fill="#0b3d5c" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle id="e8" cx="510" cy="150" r="22" fill="#0b3d5c" stroke="#0b3d5c" '
                             'stroke-width="3"/>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8']}},
            {'k': 't',
             'en': 'Task 4: count the dots in the row: 4. Count the dots in the square: 4. They have the same number.',
             'ar': 'المهمة 4: عدّ النقاط في الصف: 4. وعدّ النقاط في المربع: 4. العدد نفسه.',
             'fr': "Tâche 4 : compte les points de la ligne : 4. Compte les points du carré : 4. C'est le même nombre.",
             'label': None},
            {'k': 'f', 'f': '4 = 4'},
            {'k': 't',
             'en': 'Task 5: read the numerals: five, two, four, one, three.',
             'ar': 'المهمة 5: اقرأ الأرقام: five، two، four، one، three.',
             'fr': 'Tâche 5 : lis les chiffres : five, two, four, one, three.',
             'label': None},
            {'k': 'f', 'f': '5   2   4   1   3'}]}]


def scenes():
    return make_scenes(THEORY, EXERCISES)
