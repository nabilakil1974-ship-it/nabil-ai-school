"""Direct lesson data: Grade 1 Mathematics — Total.

Written once in three languages; every text step carries its own ar/en/fr twin."""
from __future__ import annotations

LESSON_ID = 'G01-MATH-EN-005'
GRADE = 1
SUBJECT = "math"
TITLES = {'en': 'Total', 'ar': 'المجموع', 'fr': 'Le total'}

from scripts.direct_lessons.common import T, F, D, EX, st, S, make_scenes


THEORY = [('Two small groups',
  'مجموعتان صغيرتان',
  'Deux petits groupes',
  '24',
  [{'k': 't',
    'en': 'Hello! Today I have two small groups. Here is the first group, and here is the second group.',
    'ar': 'مرحبًا! اليوم عندي مجموعتان صغيرتان. هذه المجموعة الأولى، وهذه المجموعة الثانية.',
    'fr': "Bonjour ! Aujourd'hui, j'ai deux petits groupes. Voici le premier groupe, et voici le deuxième.",
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<rect id="e1" x="30" y="110" width="290" height="180" rx="10" fill="none" stroke="#0b3d5c" stroke-width="4" '
                    'stroke-dasharray="10 8"/><rect id="e2" x="340" y="110" width="290" height="180" rx="10" fill="none" stroke="#0b3d5c" '
                    'stroke-width="4" stroke-dasharray="10 8"/><g id="e3"><circle cx="130" cy="203" r="34" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><line x1="130" y1="169" x2="135" y2="157" stroke="#7a4a1d" stroke-width="4"/><ellipse cx="141" '
                    'cy="162" rx="8" ry="4" fill="#40c057" stroke="#0b3d5c" stroke-width="2"/></g><g id="e4"><circle cx="220" cy="203" '
                    'r="34" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><line x1="220" y1="169" x2="225" y2="157" stroke="#7a4a1d" '
                    'stroke-width="4"/><ellipse cx="231" cy="162" rx="8" ry="4" fill="#40c057" stroke="#0b3d5c" stroke-width="2"/></g><g '
                    'id="e5"><circle cx="485" cy="203" r="34" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><line x1="485" y1="169" '
                    'x2="490" y2="157" stroke="#7a4a1d" stroke-width="4"/><ellipse cx="496" cy="162" rx="8" ry="4" fill="#40c057" '
                    'stroke="#0b3d5c" stroke-width="2"/></g>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5']}},
   {'k': 't',
    'en': 'But today my question is not how many are in the first group, or how many are in the second group. My question is: how many are '
          'there altogether?',
    'ar': 'لكن سؤالي اليوم ليس كم في المجموعة الأولى، ولا كم في الثانية. سؤالي هو: كم يوجد كلها معًا؟',
    'fr': "Mais ma question n'est pas combien il y en a dans le premier groupe, ni dans le deuxième. Ma question est : combien y en a-t-il "
          'en tout ?',
    'label': None},
   {'k': 't',
    'en': 'I want to know how many we have all together.',
    'ar': 'أريد أن أعرف كم صار عندنا كلها معًا.',
    'fr': 'Je veux savoir combien nous en avons tous ensemble.',
    'label': None}]),
 ('Parts and whole',
  'الأجزاء والكل',
  'Les parties et le tout',
  '24',
  [{'k': 't',
    'en': 'Look with me. The first group has 2 apples. The second group has 1 apple.',
    'ar': 'انظر معي. المجموعة الأولى فيها تفاحتان. والثانية فيها تفاحة واحدة.',
    'fr': 'Regarde avec moi. Le premier groupe a 2 pommes. Le deuxième a 1 pomme.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<rect id="e1" x="30" y="110" width="290" height="180" rx="10" fill="none" stroke="#0b3d5c" stroke-width="4" '
                    'stroke-dasharray="10 8"/><rect id="e2" x="340" y="110" width="290" height="180" rx="10" fill="none" stroke="#0b3d5c" '
                    'stroke-width="4" stroke-dasharray="10 8"/><g id="e3"><circle cx="130" cy="203" r="34" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><line x1="130" y1="169" x2="135" y2="157" stroke="#7a4a1d" stroke-width="4"/><ellipse cx="141" '
                    'cy="162" rx="8" ry="4" fill="#40c057" stroke="#0b3d5c" stroke-width="2"/></g><g id="e4"><circle cx="220" cy="203" '
                    'r="34" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><line x1="220" y1="169" x2="225" y2="157" stroke="#7a4a1d" '
                    'stroke-width="4"/><ellipse cx="231" cy="162" rx="8" ry="4" fill="#40c057" stroke="#0b3d5c" stroke-width="2"/></g><g '
                    'id="e5"><circle cx="485" cy="203" r="34" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><line x1="485" y1="169" '
                    'x2="490" y2="157" stroke="#7a4a1d" stroke-width="4"/><ellipse cx="496" cy="162" rx="8" ry="4" fill="#40c057" '
                    'stroke="#0b3d5c" stroke-width="2"/></g>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5']}},
   {'k': 't',
    'en': 'Now we put them in one place and count them all: one, two, three.',
    'ar': 'الآن نجمعها في مكان واحد ونعدّها كلها: one، two، three.',
    'fr': 'Maintenant, on les met au même endroit et on les compte toutes : one, two, three.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<g id="e1"><circle cx="220" cy="203" r="36" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><line x1="220" y1="167" '
                    'x2="225" y2="155" stroke="#7a4a1d" stroke-width="4"/><ellipse cx="231" cy="160" rx="8" ry="4" fill="#40c057" '
                    'stroke="#0b3d5c" stroke-width="2"/></g><g id="e2"><circle cx="330" cy="203" r="36" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><line x1="330" y1="167" x2="335" y2="155" stroke="#7a4a1d" stroke-width="4"/><ellipse cx="341" '
                    'cy="160" rx="8" ry="4" fill="#40c057" stroke="#0b3d5c" stroke-width="2"/></g><g id="e3"><circle cx="440" cy="203" '
                    'r="36" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><line x1="440" y1="167" x2="445" y2="155" stroke="#7a4a1d" '
                    'stroke-width="4"/><ellipse cx="451" cy="160" rx="8" ry="4" fill="#40c057" stroke="#0b3d5c" stroke-width="2"/></g>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3']}},
   {'k': 't', 'en': 'So the total is 3.', 'ar': 'إذن المجموع (the total) هو 3.', 'fr': 'Le total est donc 3.', 'label': None},
   {'k': 'f', 'f': '2 apples and 1 apple → total 3'},
   {'k': 't',
    'en': 'The word total means: how many we have when we think of all the parts as one whole.',
    'ar': 'كلمة total تعني: كم صار عندي عندما أعتبر كل الأجزاء كلًّا واحدًا.',
    'fr': "Le mot total veut dire : combien j'en ai quand je considère toutes les parties comme un seul tout.",
    'label': None},
   {'k': 't',
    'en': 'The first part alone is not the total. The second part alone is not the total. The total is all of them together.',
    'ar': 'الجزء الأول وحده ليس المجموع. والجزء الثاني وحده ليس المجموع. المجموع هو كلها معًا.',
    'fr': "La première partie seule n'est pas le total. La deuxième partie seule n'est pas le total. Le total, c'est tout ensemble.",
    'label': None}]),
 ('Count everything once',
  'نعدّ كل شيء مرة واحدة',
  'Tout compter une seule fois',
  '24',
  [{'k': 't',
    'en': 'Pay attention to something important. Group A has 3 circles. Group B has 1 circle.',
    'ar': 'انتبه إلى أمر مهم. المجموعة A فيها 3 دوائر والمجموعة B فيها دائرة واحدة.',
    'fr': "Fais attention à quelque chose d'important. Le groupe A a 3 cercles. Le groupe B a 1 cercle.",
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<rect id="e1" x="30" y="110" width="290" height="180" rx="10" fill="none" stroke="#0b3d5c" stroke-width="4" '
                    'stroke-dasharray="10 8"/><rect id="e2" x="340" y="110" width="290" height="180" rx="10" fill="none" stroke="#0b3d5c" '
                    'stroke-width="4" stroke-dasharray="10 8"/><circle id="e3" cx="95" cy="200" r="30" fill="#4dabf7" stroke="#0b3d5c" '
                    'stroke-width="3"/><circle id="e4" cx="175" cy="200" r="30" fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/><circle '
                    'id="e5" cx="255" cy="200" r="30" fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/><circle id="e6" cx="485" cy="200" '
                    'r="30" fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6']}},
   {'k': 't',
    'en': 'If I ask for the total, can I count the first group and stop? No!',
    'ar': 'إذا سألتك عن المجموع، هل أعدّ المجموعة الأولى وأتوقف؟ لا!',
    'fr': "Si je demande le total, puis-je compter le premier groupe et m'arrêter ? Non !",
    'label': None},
   {'k': 't',
    'en': 'The total means all the objects that belong to the situation. We count: one, two, three, four.',
    'ar': 'المجموع يعني كل الأشياء التي تخص الموقف. نعدّ: one، two، three، four.',
    'fr': "Le total, c'est tous les objets de la situation. On compte : one, two, three, four.",
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<circle id="e1" cx="180" cy="200" r="30" fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/><circle id="e2" cx="280" '
                    'cy="200" r="30" fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/><circle id="e3" cx="380" cy="200" r="30" '
                    'fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/><circle id="e4" cx="480" cy="200" r="30" fill="#4dabf7" '
                    'stroke="#0b3d5c" stroke-width="3"/>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4']}},
   {'k': 't',
    'en': 'And we must not count the same object twice. Each object is counted once.',
    'ar': 'ولا يجوز أن نعدّ الشيء نفسه مرتين. كل شيء يُعدّ مرة واحدة.',
    'fr': 'Et on ne doit pas compter deux fois le même objet. Chaque objet est compté une fois.',
    'label': None}]),
 ('Different parts, the same total',
  'أجزاء مختلفة والمجموع نفسه',
  'Parties différentes, même total',
  '25',
  [{'k': 't',
    'en': 'A surprise! Scene 1: 2 blue circles and 2 blue circles. Count the total: 4.',
    'ar': 'مفاجأة! المشهد 1: دائرتان زرقاوان ودائرتان زرقاوان. عدّ المجموع: 4.',
    'fr': 'Une surprise ! Scène 1 : 2 cercles bleus et 2 cercles bleus. Compte le total : 4.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<rect id="e1" x="30" y="110" width="290" height="180" rx="10" fill="none" stroke="#0b3d5c" stroke-width="4" '
                    'stroke-dasharray="10 8"/><rect id="e2" x="340" y="110" width="290" height="180" rx="10" fill="none" stroke="#0b3d5c" '
                    'stroke-width="4" stroke-dasharray="10 8"/><circle id="e3" cx="130" cy="200" r="30" fill="#4dabf7" stroke="#0b3d5c" '
                    'stroke-width="3"/><circle id="e4" cx="220" cy="200" r="30" fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/><circle '
                    'id="e5" cx="440" cy="200" r="30" fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/><circle id="e6" cx="530" cy="200" '
                    'r="30" fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6']}},
   {'k': 't',
    'en': 'Scene 2: 1 blue circle and 3 blue circles. Count the total: 4 again!',
    'ar': 'المشهد 2: دائرة زرقاء و3 دوائر زرقاء. عدّ المجموع: 4 مرة أخرى!',
    'fr': 'Scène 2 : 1 cercle bleu et 3 cercles bleus. Compte le total : encore 4 !',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<rect id="e1" x="30" y="110" width="290" height="180" rx="10" fill="none" stroke="#0b3d5c" stroke-width="4" '
                    'stroke-dasharray="10 8"/><rect id="e2" x="340" y="110" width="290" height="180" rx="10" fill="none" stroke="#0b3d5c" '
                    'stroke-width="4" stroke-dasharray="10 8"/><circle id="e3" cx="175" cy="200" r="30" fill="#4dabf7" stroke="#0b3d5c" '
                    'stroke-width="3"/><circle id="e4" cx="405" cy="200" r="30" fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/><circle '
                    'id="e5" cx="485" cy="200" r="30" fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/><circle id="e6" cx="565" cy="200" '
                    'r="30" fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6']}},
   {'k': 't',
    'en': 'The groups are split in different ways, but the total is the same.',
    'ar': 'المجموعات مقسّمة بطرق مختلفة لكن المجموع نفسه.',
    'fr': 'Les groupes sont partagés différemment, mais le total est le même.',
    'label': None},
   {'k': 't',
    'en': 'A whole can be split into different parts, and when we put them together we get the same total again. We look at all the '
          'objects together, not at how they are split.',
    'ar': 'يمكن تقسيم الكل إلى أجزاء مختلفة، وعندما نجمعها نعود إلى المجموع نفسه. ننظر إلى كل الأشياء معًا وليس إلى طريقة تقسيمها.',
    'fr': 'Un tout peut être partagé en parties différentes, et en les réunissant on retrouve le même total. On regarde tous les objets '
          'ensemble, pas la façon de les partager.',
    'label': None}]),
 ('A part is not the whole',
  'الجزء ليس الكل',
  "Une partie n'est pas le tout",
  '25',
  [{'k': 't',
    'en': 'Group A has 2 cars. Group B has 3 cars. If I tell you the first part has 2, does the total mean 2?',
    'ar': 'المجموعة A فيها سيارتان والمجموعة B فيها 3 سيارات. إذا قلت لك إن الجزء الأول فيه 2 فهل المجموع يعني 2؟',
    'fr': 'Le groupe A a 2 voitures. Le groupe B a 3 voitures. Si je te dis que la première partie a 2, le total est-il 2 ?',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<rect id="e1" x="30" y="110" width="290" height="180" rx="10" fill="none" stroke="#0b3d5c" stroke-width="4" '
                    'stroke-dasharray="10 8"/><rect id="e2" x="340" y="110" width="290" height="180" rx="10" fill="none" stroke="#0b3d5c" '
                    'stroke-width="4" stroke-dasharray="10 8"/><g id="e3"><rect x="109" y="191" width="53" height="20" rx="6" '
                    'fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><rect x="122" y="179" width="26" height="13" rx="5" fill="#e03131" '
                    'stroke="#0b3d5c" stroke-width="3"/><circle cx="122" cy="212" r="7" fill="#0b3d5c"/><circle cx="148" cy="212" r="7" '
                    'fill="#0b3d5c"/></g><g id="e4"><rect x="189" y="191" width="53" height="20" rx="6" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><rect x="202" y="179" width="26" height="13" rx="5" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><circle cx="202" cy="212" r="7" fill="#0b3d5c"/><circle cx="228" cy="212" r="7" '
                    'fill="#0b3d5c"/></g><g id="e5"><rect x="379" y="191" width="53" height="20" rx="6" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><rect x="392" y="179" width="26" height="13" rx="5" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><circle cx="392" cy="212" r="7" fill="#0b3d5c"/><circle cx="418" cy="212" r="7" '
                    'fill="#0b3d5c"/></g><g id="e6"><rect x="459" y="191" width="53" height="20" rx="6" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><rect x="472" y="179" width="26" height="13" rx="5" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><circle cx="472" cy="212" r="7" fill="#0b3d5c"/><circle cx="498" cy="212" r="7" '
                    'fill="#0b3d5c"/></g><g id="e7"><rect x="539" y="191" width="53" height="20" rx="6" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><rect x="552" y="179" width="26" height="13" rx="5" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><circle cx="552" cy="212" r="7" fill="#0b3d5c"/><circle cx="578" cy="212" r="7" '
                    'fill="#0b3d5c"/></g>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7']}},
   {'k': 't',
    'en': 'No. 2 is only a part. 3 is also only a part. The total must include everything.',
    'ar': 'لا. 2 جزء فقط، و3 جزء أيضًا. المجموع يجب أن يشمل الكل.',
    'fr': "Non. 2 n'est qu'une partie. 3 aussi n'est qu'une partie. Le total doit tout inclure.",
    'label': None},
   {'k': 't',
    'en': 'We put the two groups together: one, two, three, four, five. The total is 5.',
    'ar': 'نضم المجموعتين: one، two، three، four، five. المجموع 5.',
    'fr': 'On réunit les deux groupes : one, two, three, four, five. Le total est 5.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<g id="e1"><rect x="104" y="191" width="53" height="20" rx="6" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><rect x="117" y="179" width="26" height="13" rx="5" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><circle cx="117" cy="212" r="7" fill="#0b3d5c"/><circle cx="143" cy="212" r="7" '
                    'fill="#0b3d5c"/></g><g id="e2"><rect x="204" y="191" width="53" height="20" rx="6" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><rect x="217" y="179" width="26" height="13" rx="5" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><circle cx="217" cy="212" r="7" fill="#0b3d5c"/><circle cx="243" cy="212" r="7" '
                    'fill="#0b3d5c"/></g><g id="e3"><rect x="304" y="191" width="53" height="20" rx="6" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><rect x="317" y="179" width="26" height="13" rx="5" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><circle cx="317" cy="212" r="7" fill="#0b3d5c"/><circle cx="343" cy="212" r="7" '
                    'fill="#0b3d5c"/></g><g id="e4"><rect x="404" y="191" width="53" height="20" rx="6" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><rect x="417" y="179" width="26" height="13" rx="5" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><circle cx="417" cy="212" r="7" fill="#0b3d5c"/><circle cx="443" cy="212" r="7" '
                    'fill="#0b3d5c"/></g><g id="e5"><rect x="504" y="191" width="53" height="20" rx="6" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><rect x="517" y="179" width="26" height="13" rx="5" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><circle cx="517" cy="212" r="7" fill="#0b3d5c"/><circle cx="543" cy="212" r="7" '
                    'fill="#0b3d5c"/></g>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5']}},
   {'k': 'f', 'f': '2 and 3 are parts.   The total is 5.'},
   {'k': 't',
    'en': 'Remember: a part is not the whole.',
    'ar': 'تذكّر: الجزء ليس الكل.',
    'fr': "Retiens : une partie n'est pas le tout.",
    'label': None}]),
 ('The total in objects, pictures and numeral',
  'المجموع بالأشياء والصور والرقم',
  'Le total en objets, en dessin et en chiffre',
  '25',
  [{'k': 't',
    'en': 'We can see the total in more than one way. First with objects: 2 cubes and 1 cube.',
    'ar': 'نستطيع أن نرى المجموع بأكثر من شكل. أولًا بالأشياء: مكعبان ومكعب واحد.',
    'fr': "On peut voir le total de plusieurs façons. D'abord avec des objets : 2 cubes et 1 cube.",
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<rect id="e1" x="30" y="110" width="290" height="180" rx="10" fill="none" stroke="#0b3d5c" stroke-width="4" '
                    'stroke-dasharray="10 8"/><rect id="e2" x="340" y="110" width="290" height="180" rx="10" fill="none" stroke="#0b3d5c" '
                    'stroke-width="4" stroke-dasharray="10 8"/><rect id="e3" x="109" y="174" width="52" height="52" fill="#e03131" '
                    'stroke="#0b3d5c" stroke-width="3"/><rect id="e4" x="189" y="174" width="52" height="52" fill="#e03131" '
                    'stroke="#0b3d5c" stroke-width="3"/><rect id="e5" x="459" y="174" width="52" height="52" fill="#e03131" '
                    'stroke="#0b3d5c" stroke-width="3"/>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5']}},
   {'k': 't',
    'en': 'After we put them together, what is the total? Three.',
    'ar': 'بعد أن نجمعها كم المجموع؟ ثلاثة.',
    'fr': 'Une fois réunis, quel est le total ? Trois.',
    'label': None},
   {'k': 't',
    'en': 'Now the same total as a picture of dots.',
    'ar': 'الآن المجموع نفسه كصورة من النقاط.',
    'fr': 'Maintenant, le même total en dessin de points.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<circle id="e1" cx="220" cy="200" r="24" fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle id="e2" cx="330" '
                    'cy="200" r="24" fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle id="e3" cx="440" cy="200" r="24" '
                    'fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3']}},
   {'k': 't', 'en': 'And the same total as a numeral.', 'ar': 'والمجموع نفسه كرقم.', 'fr': 'Et le même total en chiffre.', 'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<text id="e1" x="330" y="250" font-size="220" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                    'fill="#0b3d5c">3</text>',
             'vb': [660, 440],
             'show': ['e1']}},
   {'k': 'f', 'f': 'objects → picture → numeral'},
   {'k': 't',
    'en': 'All three show the same total.',
    'ar': 'كلها تمثّل المجموع نفسه.',
    'fr': 'Tous les trois montrent le même total.',
    'label': None}]),
 ('Explain how you found the total',
  'نشرح كيف وجدنا المجموع',
  'Expliquer comment trouver le total',
  '25',
  [{'k': 't',
    'en': 'Now I want a stronger answer. Group A has 1 ball. Group B has 3 balls. How many altogether? Four.',
    'ar': 'الآن أريد جوابًا أقوى. المجموعة A فيها كرة واحدة والمجموعة B فيها 3 كرات. كم يوجد كلها؟ أربع.',
    'fr': 'Maintenant, je veux une réponse plus solide. Le groupe A a 1 balle. Le groupe B a 3 balles. Combien en tout ? Quatre.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<rect id="e1" x="30" y="110" width="290" height="180" rx="10" fill="none" stroke="#0b3d5c" stroke-width="4" '
                    'stroke-dasharray="10 8"/><rect id="e2" x="340" y="110" width="290" height="180" rx="10" fill="none" stroke="#0b3d5c" '
                    'stroke-width="4" stroke-dasharray="10 8"/><g id="e3"><circle cx="175" cy="200" r="28" fill="#fff" stroke="#0b3d5c" '
                    'stroke-width="3"/><polygon points="175,187 187,196 183,210 167,210 163,196" fill="#0b3d5c"/></g><g id="e4"><circle '
                    'cx="405" cy="200" r="28" fill="#fff" stroke="#0b3d5c" stroke-width="3"/><polygon points="405,187 417,196 413,210 '
                    '397,210 393,196" fill="#0b3d5c"/></g><g id="e5"><circle cx="485" cy="200" r="28" fill="#fff" stroke="#0b3d5c" '
                    'stroke-width="3"/><polygon points="485,187 497,196 493,210 477,210 473,196" fill="#0b3d5c"/></g><g id="e6"><circle '
                    'cx="565" cy="200" r="28" fill="#fff" stroke="#0b3d5c" stroke-width="3"/><polygon points="565,187 577,196 573,210 '
                    '557,210 553,196" fill="#0b3d5c"/></g>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6']}},
   {'k': 't',
    'en': 'But how did you know? Good answers: "I put the groups together and counted them." "I counted each ball once." "There are four '
          'altogether."',
    'ar': 'لكن كيف عرفت؟ أجوبة جيدة: «جمعت المجموعتين وعددتهما». «عددت كل كرة مرة واحدة». «صار عندنا أربع كلها».',
    'fr': "Mais comment le sais-tu ? De bonnes réponses : « J'ai réuni les groupes et je les ai comptés. » « J'ai compté chaque balle une "
          'fois. » « Il y en a quatre en tout. »',
    'label': None},
   {'k': 't',
    'en': 'A strong answer is not only a number. It has the total and how you checked.',
    'ar': 'الجواب القوي ليس رقمًا فقط. فيه المجموع وكيف تحققت.',
    'fr': "Une réponse solide n'est pas seulement un nombre. Elle contient le total et comment tu as vérifié.",
    'label': None}]),
 ('Mistakes to avoid',
  'أخطاء يجب تجنّبها',
  'Erreurs à éviter',
  '25',
  [{'k': 't',
    'en': 'Mistake 1: counting only one group. 2 stars and 3 stars, and you say "3". You counted one group only. The word altogether means '
          'count everything.',
    'ar': 'الخطأ 1: عدّ مجموعة واحدة فقط. نجمتان و3 نجوم وتقول «3». لقد عددت مجموعة واحدة. كلمة altogether تعني: عدّ الكل.',
    'fr': "Erreur 1 : ne compter qu'un groupe. 2 étoiles et 3 étoiles, et tu dis « 3 ». Tu n'as compté qu'un groupe. Le mot « altogether » "
          'veut dire : compte tout.',
    'label': None},
   {'k': 't',
    'en': 'Mistake 2: counting one object twice. Then the total is bigger than the truth. Each object counts once.',
    'ar': 'الخطأ 2: عدّ الشيء نفسه مرتين. فيصير المجموع أكبر من الحقيقة. كل شيء يُعدّ مرة.',
    'fr': 'Erreur 2 : compter deux fois le même objet. Le total devient trop grand. Chaque objet est compté une fois.',
    'label': None},
   {'k': 't',
    'en': 'Mistake 3: thinking the bigger part is the total. Part A is 4 and part B is 1. 4 is the bigger part, but not the whole. The '
          'whole must include the 1 too.',
    'ar': 'الخطأ 3: ظن أن الجزء الأكبر هو المجموع. الجزء A هو 4 والجزء B هو 1. 4 هو الجزء الأكبر لكنه ليس الكل. يجب أن يشمل الكل الـ1 '
          'أيضًا.',
    'fr': 'Erreur 3 : croire que la plus grande partie est le total. La partie A est 4 et la partie B est 1. 4 est la plus grande partie, '
          'mais pas le tout. Le tout doit aussi inclure le 1.',
    'label': None},
   {'k': 't',
    'en': 'Mistake 4: counting things that do not belong to the question. If the question is about apples, we do not count a toy that sits '
          'beside them. We count the objects that belong to the question.',
    'ar': 'الخطأ 4: عدّ أشياء لا تخص السؤال. إذا كان السؤال عن التفاح فلا نعدّ لعبة موضوعة بجانبه. نعدّ الأشياء التي تخص السؤال.',
    'fr': 'Erreur 4 : compter des objets qui ne font pas partie de la question. Si la question porte sur les pommes, on ne compte pas un '
          'jouet posé à côté. On compte les objets de la question.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<g id="e1"><circle cx="155" cy="193" r="34" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><line x1="155" y1="159" '
                    'x2="160" y2="147" stroke="#7a4a1d" stroke-width="4"/><ellipse cx="166" cy="152" rx="8" ry="4" fill="#40c057" '
                    'stroke="#0b3d5c" stroke-width="2"/></g><g id="e2"><circle cx="245" cy="193" r="34" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><line x1="245" y1="159" x2="250" y2="147" stroke="#7a4a1d" stroke-width="4"/><ellipse cx="256" '
                    'cy="152" rx="8" ry="4" fill="#40c057" stroke="#0b3d5c" stroke-width="2"/></g><g id="e3"><circle cx="453" cy="163" '
                    'r="14" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="507" cy="163" r="14" fill="#a9703c" '
                    'stroke="#0b3d5c" stroke-width="3"/><circle cx="480" cy="190" r="34" fill="#c98f55" stroke="#0b3d5c" '
                    'stroke-width="3"/><circle cx="473" cy="186" r="3" fill="#0b3d5c"/><circle cx="487" cy="186" r="3" '
                    'fill="#0b3d5c"/><ellipse cx="480" cy="197" rx="6" ry="4" fill="#f1d3a8" stroke="#0b3d5c" stroke-width="2"/></g>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3']}}]),
 ('Summary',
  'الخلاصة',
  'Résumé',
  '25',
  [{'k': 't',
    'en': 'Well done! Today we learned an important word: TOTAL.',
    'ar': 'أحسنت! تعلّمنا اليوم كلمة مهمة: TOTAL (المجموع).',
    'fr': "Bravo ! Aujourd'hui, nous avons appris un mot important : TOTAL.",
    'label': None},
   {'k': 't',
    'en': 'Total means all the objects together. First we see the parts. Then we think of them as one whole. Then we count each object '
          'once.',
    'ar': 'Total يعني كل الأشياء معًا. أولًا نرى الأجزاء. ثم نعتبرها كلًّا واحدًا. ثم نعدّ كل شيء مرة واحدة.',
    'fr': "Total veut dire tous les objets ensemble. D'abord on voit les parties. Puis on les considère comme un seul tout. Puis on compte "
          'chaque objet une fois.',
    'label': None},
   {'k': 'f', 'f': 'SEE THE PARTS → PUT THEM TOGETHER → COUNT ALL ONCE → SAY THE TOTAL → CHECK'},
   {'k': 't',
    'en': 'Do not forget: a part is not the whole. And the word altogether means: count everything.',
    'ar': 'ولا تنسَ: الجزء ليس الكل. وكلمة altogether تعني: عدّ الكل.',
    'fr': "N'oublie pas : une partie n'est pas le tout. Et le mot « altogether » veut dire : compte tout.",
    'label': None}])]


EXERCISES = [{'n': '1',
  'page': '24',
  'stmt': ('Group A has 2 stars. Group B has 2 stars. Put them together and count the total.',
           'المجموعة A فيها نجمتان والمجموعة B فيها نجمتان. اجمعهما واعدّ المجموع.',
           'Le groupe A a 2 étoiles. Le groupe B a 2 étoiles. Réunis-les et compte le total.'),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<rect id="e1" x="30" y="110" width="290" height="180" rx="10" fill="none" stroke="#0b3d5c" stroke-width="4" '
                             'stroke-dasharray="10 8"/><rect id="e2" x="340" y="110" width="290" height="180" rx="10" fill="none" '
                             'stroke="#0b3d5c" stroke-width="4" stroke-dasharray="10 8"/><polygon id="e3" points="130.0,167.8 138.5,188.3 '
                             '160.6,190.0 143.8,204.5 148.9,226.1 130.0,214.5 111.1,226.1 116.2,204.5 99.4,190.0 121.5,188.3" '
                             'fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e4" points="220.0,167.8 228.5,188.3 '
                             '250.6,190.0 233.8,204.5 238.9,226.1 220.0,214.5 201.1,226.1 206.2,204.5 189.4,190.0 211.5,188.3" '
                             'fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e5" points="440.0,167.8 448.5,188.3 '
                             '470.6,190.0 453.8,204.5 458.9,226.1 440.0,214.5 421.1,226.1 426.2,204.5 409.4,190.0 431.5,188.3" '
                             'fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e6" points="530.0,167.8 538.5,188.3 '
                             '560.6,190.0 543.8,204.5 548.9,226.1 530.0,214.5 511.1,226.1 516.2,204.5 499.4,190.0 521.5,188.3" '
                             'fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6']}},
            {'k': 't',
             'en': 'We move both groups to the same place. Now they are one whole.',
             'ar': 'ننقل المجموعتين إلى المكان نفسه. صارتا كلًّا واحدًا.',
             'fr': 'On déplace les deux groupes au même endroit. Ils forment maintenant un seul tout.',
             'label': None},
            {'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<polygon id="e1" points="180.0,167.8 188.5,188.3 210.6,190.0 193.8,204.5 198.9,226.1 180.0,214.5 161.1,226.1 '
                             '166.2,204.5 149.4,190.0 171.5,188.3" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e2" '
                             'points="280.0,167.8 288.5,188.3 310.6,190.0 293.8,204.5 298.9,226.1 280.0,214.5 261.1,226.1 266.2,204.5 '
                             '249.4,190.0 271.5,188.3" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e3" '
                             'points="380.0,167.8 388.5,188.3 410.6,190.0 393.8,204.5 398.9,226.1 380.0,214.5 361.1,226.1 366.2,204.5 '
                             '349.4,190.0 371.5,188.3" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e4" '
                             'points="480.0,167.8 488.5,188.3 510.6,190.0 493.8,204.5 498.9,226.1 480.0,214.5 461.1,226.1 466.2,204.5 '
                             '449.4,190.0 471.5,188.3" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4']}},
            {'k': 't',
             'en': 'Count every star once: one, two, three, four.',
             'ar': 'عدّ كل نجمة مرة: one، two، three، four.',
             'fr': 'Compte chaque étoile une fois : one, two, three, four.',
             'label': None},
            {'k': 'f', 'f': '2 + 2 → total 4'},
            {'k': 't',
             'en': 'The total is 4. The two groups became one whole, and there are 4.',
             'ar': 'المجموع 4. صارت المجموعتان كلًّا واحدًا وعدده 4.',
             'fr': 'Le total est 4. Les deux groupes forment un seul tout et il y en a 4.',
             'label': None}]},
 {'n': '2',
  'page': '24',
  'stmt': ('Group A has 2 teddy bears. Group B has 3 teddy bears. How many teddy bears are there altogether?',
           'المجموعة A فيها دبّان والمجموعة B فيها 3 دببة. كم دبًّا يوجد كلها؟',
           'Le groupe A a 2 nounours. Le groupe B a 3 nounours. Combien de nounours y a-t-il en tout ?'),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<rect id="e1" x="30" y="110" width="290" height="180" rx="10" fill="none" stroke="#0b3d5c" stroke-width="4" '
                             'stroke-dasharray="10 8"/><rect id="e2" x="340" y="110" width="290" height="180" rx="10" fill="none" '
                             'stroke="#0b3d5c" stroke-width="4" stroke-dasharray="10 8"/><g id="e3"><circle cx="114" cy="179" r="10" '
                             'fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="156" cy="179" r="10" fill="#a9703c" '
                             'stroke="#0b3d5c" stroke-width="3"/><circle cx="135" cy="200" r="26" fill="#c98f55" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle cx="128" cy="196" r="3" fill="#0b3d5c"/><circle cx="142" cy="196" r="3" '
                             'fill="#0b3d5c"/><ellipse cx="135" cy="207" rx="6" ry="4" fill="#f1d3a8" stroke="#0b3d5c" '
                             'stroke-width="2"/></g><g id="e4"><circle cx="194" cy="179" r="10" fill="#a9703c" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle cx="236" cy="179" r="10" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle '
                             'cx="215" cy="200" r="26" fill="#c98f55" stroke="#0b3d5c" stroke-width="3"/><circle cx="208" cy="196" r="3" '
                             'fill="#0b3d5c"/><circle cx="222" cy="196" r="3" fill="#0b3d5c"/><ellipse cx="215" cy="207" rx="6" ry="4" '
                             'fill="#f1d3a8" stroke="#0b3d5c" stroke-width="2"/></g><g id="e5"><circle cx="384" cy="179" r="10" '
                             'fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="426" cy="179" r="10" fill="#a9703c" '
                             'stroke="#0b3d5c" stroke-width="3"/><circle cx="405" cy="200" r="26" fill="#c98f55" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle cx="398" cy="196" r="3" fill="#0b3d5c"/><circle cx="412" cy="196" r="3" '
                             'fill="#0b3d5c"/><ellipse cx="405" cy="207" rx="6" ry="4" fill="#f1d3a8" stroke="#0b3d5c" '
                             'stroke-width="2"/></g><g id="e6"><circle cx="464" cy="179" r="10" fill="#a9703c" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle cx="506" cy="179" r="10" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle '
                             'cx="485" cy="200" r="26" fill="#c98f55" stroke="#0b3d5c" stroke-width="3"/><circle cx="478" cy="196" r="3" '
                             'fill="#0b3d5c"/><circle cx="492" cy="196" r="3" fill="#0b3d5c"/><ellipse cx="485" cy="207" rx="6" ry="4" '
                             'fill="#f1d3a8" stroke="#0b3d5c" stroke-width="2"/></g><g id="e7"><circle cx="544" cy="179" r="10" '
                             'fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="586" cy="179" r="10" fill="#a9703c" '
                             'stroke="#0b3d5c" stroke-width="3"/><circle cx="565" cy="200" r="26" fill="#c98f55" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle cx="558" cy="196" r="3" fill="#0b3d5c"/><circle cx="572" cy="196" r="3" '
                             'fill="#0b3d5c"/><ellipse cx="565" cy="207" rx="6" ry="4" fill="#f1d3a8" stroke="#0b3d5c" '
                             'stroke-width="2"/></g>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7']}},
            {'k': 't',
             'en': 'First group: 2. Second group: 3. But the question is about all of them. If we say 3, we only counted the second group.',
             'ar': 'المجموعة الأولى: 2. الثانية: 3. لكن السؤال عن الجميع. لو قلنا 3 فقد عددنا الثانية فقط.',
             'fr': "Premier groupe : 2. Deuxième groupe : 3. Mais la question porte sur tous. Si on dit 3, on n'a compté que le deuxième "
                   'groupe.',
             'label': None},
            {'k': 't',
             'en': 'We count from the first teddy of the first group and continue to the second group: one, two, three, four, five.',
             'ar': 'نعدّ من أول دبّ في المجموعة الأولى ونكمل إلى المجموعة الثانية: one، two، three، four، five.',
             'fr': 'On compte depuis le premier nounours du premier groupe et on continue dans le deuxième : one, two, three, four, five.',
             'label': None},
            {'k': 'f', 'f': '2 + 3 → total 5'},
            {'k': 't', 'en': 'The total is 5.', 'ar': 'المجموع 5.', 'fr': 'Le total est 5.', 'label': None}]},
 {'n': '3',
  'page': '25',
  'stmt': ('Scene A: 3 cookies and 1 cookie. Scene B: 2 cookies and 2 cookies. Is the total the same or different?',
           'المشهد A: 3 بسكويتات وبسكويتة. المشهد B: بسكويتتان وبسكويتتان. هل المجموع نفسه أم مختلف؟',
           'Scène A : 3 biscuits et 1 biscuit. Scène B : 2 biscuits et 2 biscuits. Le total est-il le même ou différent ?'),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<g id="e1"><circle cx="70" cy="110" r="22" fill="#d9a05b" stroke="#0b3d5c" stroke-width="3"/><circle cx="63" '
                             'cy="105" r="3" fill="#5c3b1e"/><circle cx="76" cy="108" r="3" fill="#5c3b1e"/><circle cx="68" cy="118" r="3" '
                             'fill="#5c3b1e"/></g><g id="e2"><circle cx="130" cy="110" r="22" fill="#d9a05b" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle cx="123" cy="105" r="3" fill="#5c3b1e"/><circle cx="136" cy="108" r="3" '
                             'fill="#5c3b1e"/><circle cx="128" cy="118" r="3" fill="#5c3b1e"/></g><g id="e3"><circle cx="190" cy="110" '
                             'r="22" fill="#d9a05b" stroke="#0b3d5c" stroke-width="3"/><circle cx="183" cy="105" r="3" '
                             'fill="#5c3b1e"/><circle cx="196" cy="108" r="3" fill="#5c3b1e"/><circle cx="188" cy="118" r="3" '
                             'fill="#5c3b1e"/></g><line id="e4" x1="240" y1="70" x2="240" y2="150" stroke="#0b3d5c" stroke-width="3" '
                             'stroke-linecap="round"/><g id="e5"><circle cx="310" cy="110" r="22" fill="#d9a05b" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle cx="303" cy="105" r="3" fill="#5c3b1e"/><circle cx="316" cy="108" r="3" '
                             'fill="#5c3b1e"/><circle cx="308" cy="118" r="3" fill="#5c3b1e"/></g><g id="e6"><circle cx="100" cy="310" '
                             'r="22" fill="#d9a05b" stroke="#0b3d5c" stroke-width="3"/><circle cx="93" cy="305" r="3" '
                             'fill="#5c3b1e"/><circle cx="106" cy="308" r="3" fill="#5c3b1e"/><circle cx="98" cy="318" r="3" '
                             'fill="#5c3b1e"/></g><g id="e7"><circle cx="160" cy="310" r="22" fill="#d9a05b" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle cx="153" cy="305" r="3" fill="#5c3b1e"/><circle cx="166" cy="308" r="3" '
                             'fill="#5c3b1e"/><circle cx="158" cy="318" r="3" fill="#5c3b1e"/></g><line id="e8" x1="240" y1="270" x2="240" '
                             'y2="350" stroke="#0b3d5c" stroke-width="3" stroke-linecap="round"/><g id="e9"><circle cx="310" cy="310" '
                             'r="22" fill="#d9a05b" stroke="#0b3d5c" stroke-width="3"/><circle cx="303" cy="305" r="3" '
                             'fill="#5c3b1e"/><circle cx="316" cy="308" r="3" fill="#5c3b1e"/><circle cx="308" cy="318" r="3" '
                             'fill="#5c3b1e"/></g><g id="e10"><circle cx="370" cy="310" r="22" fill="#d9a05b" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle cx="363" cy="305" r="3" fill="#5c3b1e"/><circle cx="376" cy="308" r="3" '
                             'fill="#5c3b1e"/><circle cx="368" cy="318" r="3" fill="#5c3b1e"/></g>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10']}},
            {'k': 't',
             'en': 'Do not guess. Count scene A: one, two, three, four. The total is 4.',
             'ar': 'لا تخمّن. عدّ المشهد A: one، two، three، four. المجموع 4.',
             'fr': 'Ne devine pas. Compte la scène A : one, two, three, four. Le total est 4.',
             'label': None},
            {'k': 't',
             'en': 'Count scene B: one, two, three, four. The total is 4.',
             'ar': 'عدّ المشهد B: one، two، three، four. المجموع 4.',
             'fr': 'Compte la scène B : one, two, three, four. Le total est 4.',
             'label': None},
            {'k': 'f', 'f': '3 + 1 = 4      2 + 2 = 4'},
            {'k': 't',
             'en': 'The same total. The parts are different, but the total is the same.',
             'ar': 'المجموع نفسه. الأجزاء مختلفة لكن المجموع نفسه.',
             'fr': 'Le même total. Les parties sont différentes, mais le total est le même.',
             'label': None}]},
 {'n': '4',
  'page': '25',
  'stmt': ('Part A has 3 stars. Part B has 1 star. What is the total: 3, 4 or 5?',
           'الجزء A فيه 3 نجوم والجزء B فيه نجمة. ما المجموع: 3 أم 4 أم 5؟',
           'La partie A a 3 étoiles. La partie B a 1 étoile. Quel est le total : 3, 4 ou 5 ?'),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<rect id="e1" x="30" y="110" width="290" height="180" rx="10" fill="none" stroke="#0b3d5c" stroke-width="4" '
                             'stroke-dasharray="10 8"/><rect id="e2" x="340" y="110" width="290" height="180" rx="10" fill="none" '
                             'stroke="#0b3d5c" stroke-width="4" stroke-dasharray="10 8"/><polygon id="e3" points="105.0,170.1 112.9,189.1 '
                             '133.4,190.8 117.8,204.2 122.6,224.2 105.0,213.5 87.4,224.2 92.2,204.2 76.6,190.8 97.1,189.1" fill="#ffd43b" '
                             'stroke="#0b3d5c" stroke-width="3"/><polygon id="e4" points="175.0,170.1 182.9,189.1 203.4,190.8 187.8,204.2 '
                             '192.6,224.2 175.0,213.5 157.4,224.2 162.2,204.2 146.6,190.8 167.1,189.1" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/><polygon id="e5" points="245.0,170.1 252.9,189.1 273.4,190.8 257.8,204.2 262.6,224.2 '
                             '245.0,213.5 227.4,224.2 232.2,204.2 216.6,190.8 237.1,189.1" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/><polygon id="e6" points="485.0,170.1 492.9,189.1 513.4,190.8 497.8,204.2 502.6,224.2 '
                             '485.0,213.5 467.4,224.2 472.2,204.2 456.6,190.8 477.1,189.1" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6']}},
            {'k': 't',
             'en': '3 is only the first part. We join the second star to the group.',
             'ar': '3 هو الجزء الأول فقط. نضم النجمة الثانية إلى المجموعة.',
             'fr': "3 n'est que la première partie. On ajoute l'autre étoile au groupe.",
             'label': None},
            {'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<polygon id="e1" points="180.0,167.8 188.5,188.3 210.6,190.0 193.8,204.5 198.9,226.1 180.0,214.5 161.1,226.1 '
                             '166.2,204.5 149.4,190.0 171.5,188.3" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e2" '
                             'points="280.0,167.8 288.5,188.3 310.6,190.0 293.8,204.5 298.9,226.1 280.0,214.5 261.1,226.1 266.2,204.5 '
                             '249.4,190.0 271.5,188.3" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e3" '
                             'points="380.0,167.8 388.5,188.3 410.6,190.0 393.8,204.5 398.9,226.1 380.0,214.5 361.1,226.1 366.2,204.5 '
                             '349.4,190.0 371.5,188.3" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e4" '
                             'points="480.0,167.8 488.5,188.3 510.6,190.0 493.8,204.5 498.9,226.1 480.0,214.5 461.1,226.1 466.2,204.5 '
                             '449.4,190.0 471.5,188.3" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4']}},
            {'k': 't',
             'en': 'Count all: one, two, three, four.',
             'ar': 'عدّ الكل: one، two، three، four.',
             'fr': 'Compte tout : one, two, three, four.',
             'label': None},
            {'k': 'f', 'f': '3 + 1 → total 4'},
            {'k': 't',
             'en': '3 stars plus one more star make a whole of 4. Always ask yourself: am I counting a part, or the whole?',
             'ar': '3 نجوم ونجمة إضافية تعطي كلًّا هو 4. اسأل نفسك دائمًا: هل أعدّ جزءًا أم الكل؟',
             'fr': '3 étoiles et encore une étoile font un tout de 4. Demande-toi toujours : est-ce que je compte une partie ou le tout ?',
             'label': None}]},
 {'n': '5',
  'page': '25',
  'stmt': ('Group A has 2 flowers. Group B has 3 flowers. Put them together, count, and choose the numeral: 3, 4 or 5.',
           'المجموعة A فيها زهرتان والمجموعة B فيها 3 زهرات. اجمعهما وعدّ ثم اختر الرقم: 3 أو 4 أو 5.',
           'Le groupe A a 2 fleurs. Le groupe B a 3 fleurs. Réunis-les, compte, puis choisis le chiffre : 3, 4 ou 5.'),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<rect id="e1" x="30" y="110" width="290" height="180" rx="10" fill="none" stroke="#0b3d5c" stroke-width="4" '
                             'stroke-dasharray="10 8"/><rect id="e2" x="340" y="110" width="290" height="180" rx="10" fill="none" '
                             'stroke="#0b3d5c" stroke-width="4" stroke-dasharray="10 8"/><g id="e3"><circle cx="152" cy="200" r="13" '
                             'fill="#f783ac" stroke="#0b3d5c" stroke-width="2"/><circle cx="140" cy="216" r="13" fill="#f783ac" '
                             'stroke="#0b3d5c" stroke-width="2"/><circle cx="121" cy="210" r="13" fill="#f783ac" stroke="#0b3d5c" '
                             'stroke-width="2"/><circle cx="121" cy="190" r="13" fill="#f783ac" stroke="#0b3d5c" stroke-width="2"/><circle '
                             'cx="140" cy="184" r="13" fill="#f783ac" stroke="#0b3d5c" stroke-width="2"/><circle cx="135" cy="200" r="10" '
                             'fill="#ffd43b" stroke="#0b3d5c" stroke-width="2"/></g><g id="e4"><circle cx="232" cy="200" r="13" '
                             'fill="#f783ac" stroke="#0b3d5c" stroke-width="2"/><circle cx="220" cy="216" r="13" fill="#f783ac" '
                             'stroke="#0b3d5c" stroke-width="2"/><circle cx="201" cy="210" r="13" fill="#f783ac" stroke="#0b3d5c" '
                             'stroke-width="2"/><circle cx="201" cy="190" r="13" fill="#f783ac" stroke="#0b3d5c" stroke-width="2"/><circle '
                             'cx="220" cy="184" r="13" fill="#f783ac" stroke="#0b3d5c" stroke-width="2"/><circle cx="215" cy="200" r="10" '
                             'fill="#ffd43b" stroke="#0b3d5c" stroke-width="2"/></g><g id="e5"><circle cx="422" cy="200" r="13" '
                             'fill="#f783ac" stroke="#0b3d5c" stroke-width="2"/><circle cx="410" cy="216" r="13" fill="#f783ac" '
                             'stroke="#0b3d5c" stroke-width="2"/><circle cx="391" cy="210" r="13" fill="#f783ac" stroke="#0b3d5c" '
                             'stroke-width="2"/><circle cx="391" cy="190" r="13" fill="#f783ac" stroke="#0b3d5c" stroke-width="2"/><circle '
                             'cx="410" cy="184" r="13" fill="#f783ac" stroke="#0b3d5c" stroke-width="2"/><circle cx="405" cy="200" r="10" '
                             'fill="#ffd43b" stroke="#0b3d5c" stroke-width="2"/></g><g id="e6"><circle cx="502" cy="200" r="13" '
                             'fill="#f783ac" stroke="#0b3d5c" stroke-width="2"/><circle cx="490" cy="216" r="13" fill="#f783ac" '
                             'stroke="#0b3d5c" stroke-width="2"/><circle cx="471" cy="210" r="13" fill="#f783ac" stroke="#0b3d5c" '
                             'stroke-width="2"/><circle cx="471" cy="190" r="13" fill="#f783ac" stroke="#0b3d5c" stroke-width="2"/><circle '
                             'cx="490" cy="184" r="13" fill="#f783ac" stroke="#0b3d5c" stroke-width="2"/><circle cx="485" cy="200" r="10" '
                             'fill="#ffd43b" stroke="#0b3d5c" stroke-width="2"/></g><g id="e7"><circle cx="582" cy="200" r="13" '
                             'fill="#f783ac" stroke="#0b3d5c" stroke-width="2"/><circle cx="570" cy="216" r="13" fill="#f783ac" '
                             'stroke="#0b3d5c" stroke-width="2"/><circle cx="551" cy="210" r="13" fill="#f783ac" stroke="#0b3d5c" '
                             'stroke-width="2"/><circle cx="551" cy="190" r="13" fill="#f783ac" stroke="#0b3d5c" stroke-width="2"/><circle '
                             'cx="570" cy="184" r="13" fill="#f783ac" stroke="#0b3d5c" stroke-width="2"/><circle cx="565" cy="200" r="10" '
                             'fill="#ffd43b" stroke="#0b3d5c" stroke-width="2"/></g>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7']}},
            {'k': 't',
             'en': 'Put them together and count: one, two, three, four, five.',
             'ar': 'اجمعها وعدّ: one، two، three، four، five.',
             'fr': 'Réunis-les et compte : one, two, three, four, five.',
             'label': None},
            {'k': 't',
             'en': 'The last number is five. So the numeral for the total is 5.',
             'ar': 'آخر عدد five. إذن رقم المجموع هو 5.',
             'fr': 'Le dernier nombre est five. Le chiffre du total est donc 5.',
             'label': None},
            {'k': 'f', 'f': '2 + 3 → 5'}]},
 {'n': '6',
  'page': '25',
  'stmt': ('Group A: 2 balls. Group B: 3 balls. Someone says: "The total is 3." Is that true or false? Why?',
           'المجموعة A: كرتان. المجموعة B: 3 كرات. قال أحدهم: «المجموع 3». هل هذا صح أم خطأ؟ ولماذا؟',
           "Groupe A : 2 balles. Groupe B : 3 balles. Quelqu'un dit : « Le total est 3. » Est-ce vrai ou faux ? Pourquoi ?"),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<rect id="e1" x="30" y="110" width="290" height="180" rx="10" fill="none" stroke="#0b3d5c" stroke-width="4" '
                             'stroke-dasharray="10 8"/><rect id="e2" x="340" y="110" width="290" height="180" rx="10" fill="none" '
                             'stroke="#0b3d5c" stroke-width="4" stroke-dasharray="10 8"/><g id="e3"><circle cx="138" cy="200" r="24" '
                             'fill="#fff" stroke="#0b3d5c" stroke-width="3"/><polygon points="138,189 148,197 144,209 132,209 128,197" '
                             'fill="#0b3d5c"/></g><g id="e4"><circle cx="212" cy="200" r="24" fill="#fff" stroke="#0b3d5c" '
                             'stroke-width="3"/><polygon points="212,189 222,197 218,209 206,209 202,197" fill="#0b3d5c"/></g><g '
                             'id="e5"><circle cx="410" cy="200" r="24" fill="#fff" stroke="#0b3d5c" stroke-width="3"/><polygon '
                             'points="410,189 420,197 416,209 404,209 400,197" fill="#0b3d5c"/></g><g id="e6"><circle cx="485" cy="200" '
                             'r="24" fill="#fff" stroke="#0b3d5c" stroke-width="3"/><polygon points="485,189 495,197 491,209 479,209 '
                             '475,197" fill="#0b3d5c"/></g><g id="e7"><circle cx="560" cy="200" r="24" fill="#fff" stroke="#0b3d5c" '
                             'stroke-width="3"/><polygon points="560,189 570,197 566,209 554,209 550,197" fill="#0b3d5c"/></g>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7']}},
            {'k': 't',
             'en': 'It is false. The sentence counted only one group, the second one.',
             'ar': 'هذا خطأ. الجملة عدّت مجموعة واحدة فقط وهي الثانية.',
             'fr': "C'est faux. La phrase n'a compté qu'un groupe, le deuxième.",
             'label': None},
            {'k': 't',
             'en': 'Let us correct it. We count everything: one, two, three, four, five.',
             'ar': 'لنصحّح. نعدّ كل شيء: one، two، three، four، five.',
             'fr': 'Corrigeons. On compte tout : one, two, three, four, five.',
             'label': None},
            {'k': 'f', 'f': 'The total is 5.'}]},
 {'n': '7',
  'page': '25',
  'stmt': ('There are 3 plates. Plate A has 2 strawberries, plate B has 1, plate C has 2. How many strawberries are there altogether on '
           'all three plates?',
           'هناك 3 أطباق. في الطبق A فراولتان وفي B فراولة وفي C فراولتان. كم فراولة على الأطباق الثلاثة كلها؟',
           "Il y a 3 assiettes. L'assiette A a 2 fraises, la B en a 1, la C en a 2. Combien de fraises y a-t-il en tout sur les trois "
           'assiettes ?'),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<rect id="e1" x="10" y="110" width="200" height="160" rx="10" fill="none" stroke="#0b3d5c" stroke-width="4" '
                             'stroke-dasharray="10 8"/><g id="e2"><polygon points="62,177 106,177 84,214" fill="#e03131" stroke="#0b3d5c" '
                             'stroke-width="3"/><polygon points="69,177 84,166 99,177" fill="#40c057" stroke="#0b3d5c" '
                             'stroke-width="3"/></g><g id="e3"><polygon points="114,177 158,177 136,214" fill="#e03131" stroke="#0b3d5c" '
                             'stroke-width="3"/><polygon points="121,177 136,166 151,177" fill="#40c057" stroke="#0b3d5c" '
                             'stroke-width="3"/></g><rect id="e4" x="230" y="110" width="200" height="160" rx="10" fill="none" '
                             'stroke="#0b3d5c" stroke-width="4" stroke-dasharray="10 8"/><g id="e5"><polygon points="308,177 352,177 '
                             '330,214" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><polygon points="315,177 330,166 345,177" '
                             'fill="#40c057" stroke="#0b3d5c" stroke-width="3"/></g><rect id="e6" x="450" y="110" width="200" height="160" '
                             'rx="10" fill="none" stroke="#0b3d5c" stroke-width="4" stroke-dasharray="10 8"/><g id="e7"><polygon '
                             'points="502,177 546,177 524,214" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><polygon points="509,177 '
                             '524,166 539,177" fill="#40c057" stroke="#0b3d5c" stroke-width="3"/></g><g id="e8"><polygon points="554,177 '
                             '598,177 576,214" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><polygon points="561,177 576,166 591,177" '
                             'fill="#40c057" stroke="#0b3d5c" stroke-width="3"/></g>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8']}},
            {'k': 't',
             'en': 'This time there are 3 parts, not 2. Do not forget any plate.',
             'ar': 'هذه المرة 3 أجزاء وليس 2. لا تنسَ أي طبق.',
             'fr': "Cette fois, il y a 3 parties, pas 2. N'oublie aucune assiette.",
             'label': None},
            {'k': 't',
             'en': 'Count plate A: 2. Continue with plate B, then plate C: one, two, three, four, five.',
             'ar': 'عدّ الطبق A: 2. أكمل بالطبق B ثم الطبق C: one، two، three، four، five.',
             'fr': "Compte l'assiette A : 2. Continue avec l'assiette B, puis la C : one, two, three, four, five.",
             'label': None},
            {'k': 'f', 'f': '2 + 1 + 2 → total 5'},
            {'k': 't',
             'en': 'The total can come from more than one part.',
             'ar': 'قد يأتي المجموع من أكثر من جزأين.',
             'fr': 'Le total peut venir de plus de deux parties.',
             'label': None}]},
 {'n': '8',
  'page': '25',
  'stmt': ('Final challenge. 1) 1 object and 2 objects: how many altogether? 2) 2 and 2: total? 3) 3 and 2: total? 4) 4 and 1: is 4 the '
           'total? 5) 2 and 1: tell the total and how you checked.',
           'التحدي الأخير. 1) شيء واحد وشيئان: كم كلها؟ 2) 2 و2: المجموع؟ 3) 3 و2: المجموع؟ 4) 4 و1: هل 4 هو المجموع؟ 5) 2 و1: قل المجموع '
           'وكيف تحققت.',
           'Défi final. 1) 1 objet et 2 objets : combien en tout ? 2) 2 et 2 : total ? 3) 3 et 2 : total ? 4) 4 et 1 : 4 est-il le total ? '
           '5) 2 et 1 : dis le total et comment tu as vérifié.'),
  'steps': [{'k': 't',
             'en': 'Task 1: count all together: one, two, three. The total is 3.',
             'ar': 'المهمة 1: نعدّ الكل معًا: one، two، three. المجموع 3.',
             'fr': 'Tâche 1 : on compte tout ensemble : one, two, three. Le total est 3.',
             'label': None},
            {'k': 'f', 'f': '1 + 2 = 3'},
            {'k': 't',
             'en': 'Task 2: one, two, three, four. The total is 4.',
             'ar': 'المهمة 2: one، two، three، four. المجموع 4.',
             'fr': 'Tâche 2 : one, two, three, four. Le total est 4.',
             'label': None},
            {'k': 'f', 'f': '2 + 2 = 4'},
            {'k': 't',
             'en': 'Task 3: one, two, three, four, five. The total is 5.',
             'ar': 'المهمة 3: one، two، three، four، five. المجموع 5.',
             'fr': 'Tâche 3 : one, two, three, four, five. Le total est 5.',
             'label': None},
            {'k': 'f', 'f': '3 + 2 = 5'},
            {'k': 't',
             'en': 'Task 4: no. 4 is only one part. The other part has 1 object. The total is 5.',
             'ar': 'المهمة 4: لا. 4 جزء واحد فقط. والجزء الآخر فيه شيء واحد. المجموع 5.',
             'fr': "Tâche 4 : non. 4 n'est qu'une partie. L'autre partie a 1 objet. Le total est 5.",
             'label': None},
            {'k': 'f', 'f': '4 + 1 = 5'},
            {'k': 't',
             'en': 'Task 5: the total is 3, because I counted all the objects once.',
             'ar': 'المهمة 5: المجموع 3 لأنني عددت كل الأشياء مرة واحدة.',
             'fr': "Tâche 5 : le total est 3, parce que j'ai compté tous les objets une fois.",
             'label': None},
            {'k': 'f', 'f': '2 + 1 = 3'}]}]


def scenes():
    return make_scenes(THEORY, EXERCISES)
