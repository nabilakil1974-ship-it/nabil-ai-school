"""Direct lesson data: Grade 1 Mathematics — Addition.

Written once in three languages; every text step carries its own ar/en/fr twin."""
from __future__ import annotations

LESSON_ID = 'G01-MATH-EN-006'
GRADE = 1
SUBJECT = "math"
TITLES = {'en': 'Addition', 'ar': 'الجمع', 'fr': "L'addition"}

from scripts.direct_lessons.common import T, F, D, EX, st, S, make_scenes


THEORY = [('A group joins another group',
  'مجموعة تنضمّ إلى مجموعة',
  'Un groupe en rejoint un autre',
  '26',
  [{'k': 't',
    'en': 'Hello! Last time we learned the word total. Today we take a new step. First we have one group, and then a new group comes and '
          'joins it.',
    'ar': 'مرحبًا! في المرة الماضية تعلّمنا كلمة total. اليوم نخطو خطوة جديدة. عندنا أولًا مجموعة، ثم تأتي مجموعة جديدة وتنضم إليها.',
    'fr': "Bonjour ! La dernière fois, nous avons appris le mot total. Aujourd'hui, nouvelle étape. Il y a d'abord un groupe, puis un "
          'nouveau groupe arrive et le rejoint.',
    'label': None},
   {'k': 't',
    'en': 'Here are two teddy bears. Count them: one, two.',
    'ar': 'هنا دبّان. عدّهما: one، two.',
    'fr': 'Voici deux nounours. Compte-les : one, two.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<g id="e1"><circle cx="230" cy="165" r="18" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="300" '
                    'cy="165" r="18" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="265" cy="200" r="44" fill="#c98f55" '
                    'stroke="#0b3d5c" stroke-width="3"/><circle cx="258" cy="196" r="3" fill="#0b3d5c"/><circle cx="272" cy="196" r="3" '
                    'fill="#0b3d5c"/><ellipse cx="265" cy="207" rx="6" ry="4" fill="#f1d3a8" stroke="#0b3d5c" stroke-width="2"/></g><g '
                    'id="e2"><circle cx="360" cy="165" r="18" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="430" cy="165" '
                    'r="18" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="395" cy="200" r="44" fill="#c98f55" '
                    'stroke="#0b3d5c" stroke-width="3"/><circle cx="388" cy="196" r="3" fill="#0b3d5c"/><circle cx="402" cy="196" r="3" '
                    'fill="#0b3d5c"/><ellipse cx="395" cy="207" rx="6" ry="4" fill="#f1d3a8" stroke="#0b3d5c" stroke-width="2"/></g>',
             'vb': [660, 440],
             'show': ['e1', 'e2']}},
   {'k': 't',
    'en': 'Now watch. A new teddy bear comes and joins them. How many teddy bears are there now?',
    'ar': 'الآن انظر. جاء دبّ جديد وانضمّ إليهما. كم دبًّا يوجد الآن؟',
    'fr': 'Regarde maintenant. Un nouveau nounours arrive et les rejoint. Combien de nounours y a-t-il maintenant ?',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<g id="e1"><circle cx="165" cy="165" r="18" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="235" '
                    'cy="165" r="18" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="200" cy="200" r="44" fill="#c98f55" '
                    'stroke="#0b3d5c" stroke-width="3"/><circle cx="193" cy="196" r="3" fill="#0b3d5c"/><circle cx="207" cy="196" r="3" '
                    'fill="#0b3d5c"/><ellipse cx="200" cy="207" rx="6" ry="4" fill="#f1d3a8" stroke="#0b3d5c" stroke-width="2"/></g><g '
                    'id="e2"><circle cx="295" cy="165" r="18" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="365" cy="165" '
                    'r="18" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="330" cy="200" r="44" fill="#c98f55" '
                    'stroke="#0b3d5c" stroke-width="3"/><circle cx="323" cy="196" r="3" fill="#0b3d5c"/><circle cx="337" cy="196" r="3" '
                    'fill="#0b3d5c"/><ellipse cx="330" cy="207" rx="6" ry="4" fill="#f1d3a8" stroke="#0b3d5c" stroke-width="2"/></g><g '
                    'id="e3"><circle cx="425" cy="165" r="18" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="495" cy="165" '
                    'r="18" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="460" cy="200" r="44" fill="#c98f55" '
                    'stroke="#0b3d5c" stroke-width="3"/><circle cx="453" cy="196" r="3" fill="#0b3d5c"/><circle cx="467" cy="196" r="3" '
                    'fill="#0b3d5c"/><ellipse cx="460" cy="207" rx="6" ry="4" fill="#f1d3a8" stroke="#0b3d5c" stroke-width="2"/></g>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3']}},
   {'k': 't',
    'en': 'When a group joins another group to find the total, the idea is called addition.',
    'ar': 'عندما تنضم مجموعة إلى مجموعة أخرى لنجد المجموع فهذه الفكرة اسمها addition (الجمع).',
    'fr': "Quand un groupe en rejoint un autre pour trouver le total, cette idée s'appelle l'addition.",
    'label': None}]),
 ('Addition means joining groups',
  'الجمع يعني ضمّ المجموعات',
  "Additionner, c'est réunir des groupes",
  '26',
  [{'k': 't',
    'en': 'Watch the movement, because it matters more than any sign. The first group has 2 blue circles. The second group has 1 circle.',
    'ar': 'انظر إلى الحركة فهي أهم من أي رمز. المجموعة الأولى فيها دائرتان زرقاوان. والثانية فيها دائرة.',
    'fr': "Regarde le mouvement, il compte plus que n'importe quel signe. Le premier groupe a 2 cercles bleus. Le deuxième a 1 cercle.",
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<rect id="e1" x="30" y="110" width="290" height="180" rx="10" fill="none" stroke="#0b3d5c" stroke-width="4" '
                    'stroke-dasharray="10 8"/><rect id="e2" x="340" y="110" width="290" height="180" rx="10" fill="none" stroke="#0b3d5c" '
                    'stroke-width="4" stroke-dasharray="10 8"/><circle id="e3" cx="130" cy="200" r="32" fill="#4dabf7" stroke="#0b3d5c" '
                    'stroke-width="3"/><circle id="e4" cx="220" cy="200" r="32" fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/><circle '
                    'id="e5" cx="485" cy="200" r="32" fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5']}},
   {'k': 't',
    'en': 'The second group moves to the first group. Now they are one whole. Count: one, two, three.',
    'ar': 'تتحرّك المجموعة الثانية إلى الأولى. صارتا كلًّا واحدًا. عدّ: one، two، three.',
    'fr': 'Le deuxième groupe va vers le premier. Ils forment un seul tout. Compte : one, two, three.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<circle id="e1" cx="230" cy="200" r="32" fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/><circle id="e2" cx="330" '
                    'cy="200" r="32" fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/><circle id="e3" cx="430" cy="200" r="32" '
                    'fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3']}},
   {'k': 't',
    'en': 'So the total is 3. This is addition: group + group → one whole.',
    'ar': 'إذن المجموع 3. هذا هو الجمع: مجموعة + مجموعة ← كلٌّ واحد.',
    'fr': "Le total est donc 3. C'est l'addition : groupe + groupe → un seul tout.",
    'label': None},
   {'k': 't',
    'en': 'You do not need to memorise the plus sign before you understand the movement.',
    'ar': 'لا حاجة لأن تحفظ إشارة الجمع قبل أن تفهم الحركة.',
    'fr': "Pas besoin de retenir le signe plus avant d'avoir compris le mouvement.",
    'label': None},
   {'k': 't',
    'en': 'Addition means: quantities join together to find a total.',
    'ar': 'الجمع يعني: كميات تنضم معًا لنجد المجموع.',
    'fr': 'Additionner veut dire : des quantités se réunissent pour trouver un total.',
    'label': None}]),
 ('A story, an action, a total',
  'قصة ثم حركة ثم مجموع',
  'Une histoire, une action, un total',
  '27',
  [{'k': 't',
    'en': 'Here is a little story. There are 3 birds in the tree.',
    'ar': 'هذه قصة صغيرة. يوجد 3 عصافير على الشجرة.',
    'fr': "Voici une petite histoire. Il y a 3 oiseaux dans l'arbre.",
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<g id="e1"><ellipse cx="190" cy="204" rx="34" ry="24" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><circle '
                    'cx="214" cy="180" r="17" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon points="227,176 244,181 227,186" '
                    'fill="#ff922b" stroke="#0b3d5c" stroke-width="2"/><circle cx="217" cy="176" r="2.5" fill="#0b3d5c"/></g><g '
                    'id="e2"><ellipse cx="300" cy="204" rx="34" ry="24" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><circle cx="324" '
                    'cy="180" r="17" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon points="337,176 354,181 337,186" '
                    'fill="#ff922b" stroke="#0b3d5c" stroke-width="2"/><circle cx="327" cy="176" r="2.5" fill="#0b3d5c"/></g><g '
                    'id="e3"><ellipse cx="410" cy="204" rx="34" ry="24" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><circle cx="434" '
                    'cy="180" r="17" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon points="447,176 464,181 447,186" '
                    'fill="#ff922b" stroke="#0b3d5c" stroke-width="2"/><circle cx="437" cy="176" r="2.5" fill="#0b3d5c"/></g>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3']}},
   {'k': 't',
    'en': 'A new bird comes. What happened? One more bird joined the others.',
    'ar': 'جاء عصفور جديد. ماذا حدث؟ انضمّ عصفور آخر إلى العصافير.',
    'fr': "Un nouvel oiseau arrive. Que s'est-il passé ? Un oiseau de plus a rejoint les autres.",
    'label': None},
   {'k': 't',
    'en': 'Will the number get smaller? No, because a new bird came. It will get bigger.',
    'ar': 'هل سيصبح العدد أقل؟ لا، لأن عصفورًا جديدًا جاء. سيصبح أكبر.',
    'fr': "Le nombre va-t-il diminuer ? Non, parce qu'un nouvel oiseau est venu. Il va augmenter.",
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<g id="e1"><ellipse cx="172" cy="204" rx="34" ry="24" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><circle '
                    'cx="196" cy="180" r="17" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon points="209,176 226,181 209,186" '
                    'fill="#ff922b" stroke="#0b3d5c" stroke-width="2"/><circle cx="199" cy="176" r="2.5" fill="#0b3d5c"/></g><g '
                    'id="e2"><ellipse cx="278" cy="204" rx="34" ry="24" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><circle cx="302" '
                    'cy="180" r="17" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon points="315,176 332,181 315,186" '
                    'fill="#ff922b" stroke="#0b3d5c" stroke-width="2"/><circle cx="305" cy="176" r="2.5" fill="#0b3d5c"/></g><g '
                    'id="e3"><ellipse cx="382" cy="204" rx="34" ry="24" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><circle cx="406" '
                    'cy="180" r="17" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon points="419,176 436,181 419,186" '
                    'fill="#ff922b" stroke="#0b3d5c" stroke-width="2"/><circle cx="409" cy="176" r="2.5" fill="#0b3d5c"/></g><g '
                    'id="e4"><ellipse cx="488" cy="204" rx="34" ry="24" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><circle cx="512" '
                    'cy="180" r="17" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon points="525,176 542,181 525,186" '
                    'fill="#ff922b" stroke="#0b3d5c" stroke-width="2"/><circle cx="515" cy="176" r="2.5" fill="#0b3d5c"/></g>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4']}},
   {'k': 't',
    'en': 'Now count them all: one, two, three, four. The new total is 4.',
    'ar': 'الآن عدّها كلها: one، two، three، four. المجموع الجديد 4.',
    'fr': 'Compte-les tous : one, two, three, four. Le nouveau total est 4.',
    'label': None},
   {'k': 'f', 'f': '3 birds, 1 more bird → 4 birds'}]),
 ('Parts and whole',
  'الأجزاء والكل',
  'Les parties et le tout',
  '27',
  [{'k': 't',
    'en': 'Addition has parts and a whole. Here is the first part: 2 apples. Here is the second part: 1 apple. The whole area is empty.',
    'ar': 'في الجمع أجزاء وكلّ. هذا الجزء الأول: تفاحتان. وهذا الجزء الثاني: تفاحة. ومكان الكل فارغ.',
    'fr': "Dans l'addition, il y a des parties et un tout. Voici la première partie : 2 pommes. Voici la deuxième : 1 pomme. La zone du "
          'tout est vide.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<rect id="e1" x="60" y="40" width="230" height="130" rx="10" fill="#e7f5ff" stroke="#0b3d5c" stroke-width="4"/><rect '
                    'id="e2" x="370" y="40" width="230" height="130" rx="10" fill="#fff3bf" stroke="#0b3d5c" stroke-width="4"/><rect '
                    'id="e3" x="165" y="250" width="330" height="140" rx="10" fill="#d3f9d8" stroke="#0b3d5c" stroke-width="4"/><g '
                    'id="e4"><circle cx="135" cy="108" r="28" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><line x1="135" y1="80" '
                    'x2="140" y2="68" stroke="#7a4a1d" stroke-width="4"/><ellipse cx="146" cy="73" rx="8" ry="4" fill="#40c057" '
                    'stroke="#0b3d5c" stroke-width="2"/></g><g id="e5"><circle cx="215" cy="108" r="28" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><line x1="215" y1="80" x2="220" y2="68" stroke="#7a4a1d" stroke-width="4"/><ellipse cx="226" '
                    'cy="73" rx="8" ry="4" fill="#40c057" stroke="#0b3d5c" stroke-width="2"/></g><g id="e6"><circle cx="485" cy="108" '
                    'r="28" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><line x1="485" y1="80" x2="490" y2="68" stroke="#7a4a1d" '
                    'stroke-width="4"/><ellipse cx="496" cy="73" rx="8" ry="4" fill="#40c057" stroke="#0b3d5c" stroke-width="2"/></g>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6']}},
   {'k': 't',
    'en': 'When we join them, we get a whole. The apples move into the whole.',
    'ar': 'عندما نضمّهما يصير عندنا كلّ. تنتقل التفاحات إلى الكل.',
    'fr': 'Quand on les réunit, on obtient un tout. Les pommes vont dans le tout.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<rect id="e1" x="165" y="100" width="330" height="140" rx="10" fill="#d3f9d8" stroke="#0b3d5c" stroke-width="4"/><g '
                    'id="e2"><circle cx="240" cy="173" r="28" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><line x1="240" y1="145" '
                    'x2="245" y2="133" stroke="#7a4a1d" stroke-width="4"/><ellipse cx="251" cy="138" rx="8" ry="4" fill="#40c057" '
                    'stroke="#0b3d5c" stroke-width="2"/></g><g id="e3"><circle cx="330" cy="173" r="28" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><line x1="330" y1="145" x2="335" y2="133" stroke="#7a4a1d" stroke-width="4"/><ellipse cx="341" '
                    'cy="138" rx="8" ry="4" fill="#40c057" stroke="#0b3d5c" stroke-width="2"/></g><g id="e4"><circle cx="420" cy="173" '
                    'r="28" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><line x1="420" y1="145" x2="425" y2="133" stroke="#7a4a1d" '
                    'stroke-width="4"/><ellipse cx="431" cy="138" rx="8" ry="4" fill="#40c057" stroke="#0b3d5c" stroke-width="2"/></g>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4']}},
   {'k': 't', 'en': 'Count the whole: three.', 'ar': 'عدّ الكل: ثلاثة.', 'fr': 'Compte le tout : trois.', 'label': None},
   {'k': 'f', 'f': 'part + part → whole      2 + 1 → 3'},
   {'k': 't', 'en': 'The whole is the total.', 'ar': 'الكل هو المجموع.', 'fr': "Le tout, c'est le total.", 'label': None}]),
 ('The order can change, the total stays',
  'يتغيّر الترتيب ويبقى المجموع',
  "L'ordre change, le total reste",
  '27',
  [{'k': 't',
    'en': 'Let us do an experiment. Scene A: 2 blue blocks, then 1 red block joins.',
    'ar': 'لنجرِ تجربة. المشهد A: مكعبان أزرقان ثم ينضم مكعب أحمر.',
    'fr': 'Faisons une expérience. Scène A : 2 blocs bleus, puis 1 bloc rouge les rejoint.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<rect id="e1" x="208" y="168" width="64" height="64" fill="#339af0" stroke="#0b3d5c" stroke-width="3"/><rect id="e2" '
                    'x="298" y="168" width="64" height="64" fill="#339af0" stroke="#0b3d5c" stroke-width="3"/><rect id="e3" x="388" '
                    'y="168" width="64" height="64" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3']}},
   {'k': 't',
    'en': 'Count the total: one, two, three. It is 3.',
    'ar': 'عدّ المجموع: one، two، three. إنه 3.',
    'fr': "Compte le total : one, two, three. C'est 3.",
    'label': None},
   {'k': 't',
    'en': 'Scene B: now the red block is first, and 2 blue blocks join it.',
    'ar': 'المشهد B: الآن المكعب الأحمر أولًا ثم ينضم إليه مكعبان أزرقان.',
    'fr': 'Scène B : maintenant, le bloc rouge est le premier et 2 blocs bleus le rejoignent.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<rect id="e1" x="208" y="168" width="64" height="64" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><rect id="e2" '
                    'x="298" y="168" width="64" height="64" fill="#339af0" stroke="#0b3d5c" stroke-width="3"/><rect id="e3" x="388" '
                    'y="168" width="64" height="64" fill="#339af0" stroke="#0b3d5c" stroke-width="3"/>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3']}},
   {'k': 't',
    'en': 'We changed who came first. Count the total: one, two, three. It is still 3.',
    'ar': 'غيّرنا من جاء أولًا. عدّ المجموع: one، two، three. ما زال 3.',
    'fr': "On a changé qui est arrivé en premier. Compte le total : one, two, three. C'est encore 3.",
    'label': None},
   {'k': 't',
    'en': 'The same objects joined together, so the total did not change.',
    'ar': 'انضمّت الأشياء نفسها بعضها إلى بعض، لذلك لم يتغيّر المجموع.',
    'fr': "Les mêmes objets se sont réunis, donc le total n'a pas changé.",
    'label': None},
   {'k': 'f', 'f': '2 + 1 = 3      1 + 2 = 3'}]),
 ('The action comes before the symbol',
  'الحركة قبل الرمز',
  "L'action avant le symbole",
  '27',
  [{'k': 't',
    'en': 'Now that we understand the movement, we can use a simpler picture. Two dots.',
    'ar': 'بعد أن فهمنا الحركة نستطيع استعمال تمثيل أبسط. نقطتان.',
    'fr': 'Maintenant que nous avons compris le mouvement, nous pouvons utiliser un dessin plus simple. Deux points.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<circle id="e1" cx="280" cy="200" r="20" fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle id="e2" cx="380" '
                    'cy="200" r="20" fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/>',
             'vb': [660, 440],
             'show': ['e1', 'e2']}},
   {'k': 't',
    'en': 'A new dot joins them. What happened? A new dot joined. The whole is now 3.',
    'ar': 'تنضم نقطة جديدة. ماذا حدث؟ انضمّت نقطة جديدة. الكل الآن 3.',
    'fr': "Un nouveau point les rejoint. Que s'est-il passé ? Un nouveau point est venu. Le tout est maintenant 3.",
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<rect id="e1" x="60" y="40" width="230" height="130" rx="10" fill="#e7f5ff" stroke="#0b3d5c" stroke-width="4"/><rect '
                    'id="e2" x="370" y="40" width="230" height="130" rx="10" fill="#fff3bf" stroke="#0b3d5c" stroke-width="4"/><rect '
                    'id="e3" x="165" y="250" width="330" height="140" rx="10" fill="#d3f9d8" stroke="#0b3d5c" stroke-width="4"/><text '
                    'id="e4" x="175" y="30" font-size="24" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                    'fill="#0b3d5c">part 1</text><text id="e5" x="485" y="30" font-size="24" font-family="sans-serif" font-weight="bold" '
                    'text-anchor="middle" fill="#0b3d5c">part 2</text><text id="e6" x="330" y="240" font-size="24" '
                    'font-family="sans-serif" font-weight="bold" text-anchor="middle" fill="#0b3d5c">whole</text><circle id="e7" cx="153" '
                    'cy="105" r="8" fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle id="e8" cx="197" cy="105" r="8" '
                    'fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle id="e9" cx="485" cy="105" r="8" fill="#0b3d5c" '
                    'stroke="#0b3d5c" stroke-width="3"/><circle id="e10" cx="278" cy="320" r="8" fill="#0b3d5c" stroke="#0b3d5c" '
                    'stroke-width="3"/><circle id="e11" cx="330" cy="320" r="8" fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle '
                    'id="e12" cx="382" cy="320" r="8" fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10', 'e11', 'e12']}},
   {'k': 't',
    'en': 'The picture tells the same story: 2 objects, joined by 1 object, total 3. The meaning comes first, then the picture.',
    'ar': 'الصورة تحكي القصة نفسها: شيئان، انضمّ إليهما شيء واحد، المجموع 3. المعنى أولًا ثم التمثيل.',
    'fr': "Le dessin raconte la même histoire : 2 objets, 1 objet les rejoint, total 3. Le sens vient d'abord, ensuite la représentation.",
    'label': None},
   {'k': 'f', 'f': '2 and 1 → 3'}]),
 ('Explain the addition',
  'نشرح عملية الجمع',
  "Expliquer l'addition",
  '27',
  [{'k': 't',
    'en': 'Look. There is 1 balloon. Then 2 balloons join.',
    'ar': 'انظر. هناك بالون واحد. ثم ينضم بالونان.',
    'fr': 'Regarde. Il y a 1 ballon. Puis 2 ballons le rejoignent.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<g id="e1"><ellipse cx="150" cy="186" rx="32" ry="40" fill="#f06595" stroke="#0b3d5c" stroke-width="3"/><line '
                    'x1="150" y1="226" x2="150" y2="262" stroke="#0b3d5c" stroke-width="2"/></g><g id="e2"><ellipse cx="345" cy="186" '
                    'rx="32" ry="40" fill="#f06595" stroke="#0b3d5c" stroke-width="3"/><line x1="345" y1="226" x2="345" y2="262" '
                    'stroke="#0b3d5c" stroke-width="2"/></g><g id="e3"><ellipse cx="455" cy="186" rx="32" ry="40" fill="#f06595" '
                    'stroke="#0b3d5c" stroke-width="3"/><line x1="455" y1="226" x2="455" y2="262" stroke="#0b3d5c" stroke-width="2"/></g>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3']}},
   {'k': 't',
    'en': 'How many balloons now? Three. And now tell the story, not only the number: "There was 1 balloon. 2 more joined. Now there are 3 '
          'altogether."',
    'ar': 'كم بالونًا الآن؟ ثلاثة. والآن احكِ القصة وليس العدد فقط: «كان هناك بالون واحد. انضمّ بالونان. الآن يوجد 3 كلها».',
    'fr': "Combien de ballons maintenant ? Trois. Et maintenant raconte l'histoire, pas seulement le nombre : « Il y avait 1 ballon. 2 de "
          'plus sont venus. Maintenant, il y en a 3 en tout. »',
    'label': None},
   {'k': 't',
    'en': 'An addition is not only a number. It is a story: the first group, the new group that joins, and the total.',
    'ar': 'الجمع ليس رقمًا فقط. إنه قصة: المجموعة الأولى، والمجموعة الجديدة التي تنضم، والمجموع.',
    'fr': "Une addition n'est pas seulement un nombre. C'est une histoire : le premier groupe, le nouveau groupe qui arrive, et le total.",
    'label': None}]),
 ('Mistakes to avoid',
  'أخطاء يجب تجنّبها',
  'Erreurs à éviter',
  '27',
  [{'k': 't',
    'en': 'Mistake 1: counting only the new group. There are 3 objects, 1 joins, and you say "1". But 1 is only the new group. The '
          'question asks: how many are there now, after joining?',
    'ar': 'الخطأ 1: عدّ المجموعة الجديدة فقط. هناك 3 أشياء وانضمّ 1 وأنت تقول «1». لكن 1 هو المجموعة الجديدة فقط. السؤال: كم صار العدد بعد '
          'الانضمام؟',
    'fr': "Erreur 1 : ne compter que le nouveau groupe. Il y a 3 objets, 1 arrive, et tu dis « 1 ». Mais 1 n'est que le nouveau groupe. La "
          "question : combien y en a-t-il maintenant, après l'arrivée ?",
    'label': None},
   {'k': 't',
    'en': 'Mistake 2: forgetting the first group. When new objects come, we do not forget the ones that were already there. All of them go '
          'into the total.',
    'ar': 'الخطأ 2: نسيان المجموعة الأولى. عندما تأتي أشياء جديدة لا ننسى الأشياء التي كانت موجودة. كلها تدخل في المجموع.',
    'fr': "Erreur 2 : oublier le premier groupe. Quand de nouveaux objets arrivent, on n'oublie pas ceux qui étaient déjà là. Tous entrent "
          'dans le total.',
    'label': None},
   {'k': 't',
    'en': 'Mistake 3: counting an object twice. After the groups join, count each object once.',
    'ar': 'الخطأ 3: عدّ الشيء مرتين. بعد أن تنضم المجموعات نعدّ كل شيء مرة واحدة.',
    'fr': 'Erreur 3 : compter un objet deux fois. Après la réunion des groupes, on compte chaque objet une fois.',
    'label': None},
   {'k': 't',
    'en': 'Mistake 4: thinking addition is only a sign. Addition is not a sign to memorise. It is an action: objects join objects. If we '
          'do not understand the action, the sign alone is not enough.',
    'ar': 'الخطأ 4: ظن أن الجمع مجرد إشارة. الجمع ليس إشارة نحفظها. إنه حركة: أشياء تنضم إلى أشياء. إذا لم نفهم الحركة فالإشارة وحدها لا '
          'تكفي.',
    'fr': "Erreur 4 : croire que l'addition n'est qu'un signe. L'addition n'est pas un signe à retenir. C'est une action : des objets "
          "rejoignent des objets. Sans comprendre l'action, le signe seul ne suffit pas.",
    'label': None}]),
 ('Summary',
  'الخلاصة',
  'Résumé',
  '27',
  [{'k': 't',
    'en': 'Well done! Today we learned ADDITION.',
    'ar': 'أحسنت! تعلّمنا اليوم الجمع ADDITION.',
    'fr': "Bravo ! Aujourd'hui, nous avons appris l'ADDITION.",
    'label': None},
   {'k': 't',
    'en': 'Addition means: quantities join together to find a total.',
    'ar': 'الجمع يعني: كميات تنضم معًا لنجد المجموع.',
    'fr': 'Additionner veut dire : des quantités se réunissent pour trouver un total.',
    'label': None},
   {'k': 'f', 'f': 'SEE THE FIRST GROUP → SEE WHAT JOINS → PUT THEM TOGETHER → COUNT ALL ONCE → SAY THE TOTAL → CHECK'},
   {'k': 't',
    'en': 'Remember: addition is not only a sign. Addition is an action.',
    'ar': 'تذكّر: الجمع ليس رمزًا فقط. الجمع حركة.',
    'fr': "Retiens : l'addition n'est pas seulement un signe. L'addition est une action.",
    'label': None}])]


EXERCISES = [{'n': '1',
  'page': '26',
  'stmt': ('Group A has 2 stars. Group B has 2 stars. Join group B to group A, then count the total.',
           'المجموعة A فيها نجمتان والمجموعة B فيها نجمتان. ضمّ B إلى A ثم عدّ المجموع.',
           'Le groupe A a 2 étoiles. Le groupe B a 2 étoiles. Joins B à A, puis compte le total.'),
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
             'en': 'We move group B next to group A. Now they are one group.',
             'ar': 'ننقل المجموعة B بجانب A. صارتا مجموعة واحدة.',
             'fr': 'On déplace le groupe B à côté de A. Ils forment un seul groupe.',
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
             'en': 'Count all, starting from the first star: one, two, three, four.',
             'ar': 'عدّ الكل ابتداءً من أول نجمة: one، two، three، four.',
             'fr': 'Compte tout, en partant de la première étoile : one, two, three, four.',
             'label': None},
            {'k': 'f', 'f': '2 + 2 → total 4'},
            {'k': 't',
             'en': 'When two groups join, the total includes the objects of both. Counting only group B would be a mistake.',
             'ar': 'عندما تنضم مجموعتان يشمل المجموع أشياء الاثنتين. عدّ B فقط خطأ.',
             'fr': 'Quand deux groupes se réunissent, le total comprend les objets des deux. Compter seulement B serait une erreur.',
             'label': None}]},
 {'n': '2',
  'page': '27',
  'stmt': ('There are 2 cars. A new car comes. How many cars are there now?',
           'هناك سيارتان. جاءت سيارة جديدة. كم سيارة الآن؟',
           'Il y a 2 voitures. Une nouvelle voiture arrive. Combien de voitures y a-t-il maintenant ?'),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<g id="e1"><rect x="62" y="184" width="96" height="36" rx="6" fill="#e03131" stroke="#0b3d5c" '
                             'stroke-width="3"/><rect x="86" y="162" width="48" height="24" rx="5" fill="#e03131" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle cx="86" cy="222" r="12" fill="#0b3d5c"/><circle cx="134" cy="222" r="12" '
                             'fill="#0b3d5c"/></g><g id="e2"><rect x="222" y="184" width="96" height="36" rx="6" fill="#e03131" '
                             'stroke="#0b3d5c" stroke-width="3"/><rect x="246" y="162" width="48" height="24" rx="5" fill="#e03131" '
                             'stroke="#0b3d5c" stroke-width="3"/><circle cx="246" cy="222" r="12" fill="#0b3d5c"/><circle cx="294" '
                             'cy="222" r="12" fill="#0b3d5c"/></g><g id="e3"><rect x="472" y="184" width="96" height="36" rx="6" '
                             'fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><rect x="496" y="162" width="48" height="24" rx="5" '
                             'fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><circle cx="496" cy="222" r="12" fill="#0b3d5c"/><circle '
                             'cx="544" cy="222" r="12" fill="#0b3d5c"/></g>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3']}},
            {'k': 't',
             'en': 'First count the cars that were there: two.',
             'ar': 'عدّ أولًا السيارات الموجودة: اثنتان.',
             'fr': "Compte d'abord les voitures qui étaient là : deux.",
             'label': None},
            {'k': 't',
             'en': 'Now add the new car and count from the beginning: one, two, three.',
             'ar': 'الآن أضف السيارة الجديدة وعدّ من البداية: one، two، three.',
             'fr': 'Ajoute maintenant la nouvelle voiture et compte depuis le début : one, two, three.',
             'label': None},
            {'k': 'f', 'f': '2 + 1 = 3'},
            {'k': 't',
             'en': 'The total is 3. How did we know? We joined the new car and counted them all.',
             'ar': 'المجموع 3. كيف عرفنا؟ ضممنا السيارة الجديدة وعددنا الكل.',
             'fr': 'Le total est 3. Comment le sait-on ? On a ajouté la nouvelle voiture et on les a toutes comptées.',
             'label': None}]},
 {'n': '3',
  'page': '27',
  'stmt': ('Part A has 3 donuts. Part B has 1 donut. Find the whole.',
           'الجزء A فيه 3 حلقات دونات والجزء B فيه واحدة. أوجد الكل.',
           'La partie A a 3 beignets. La partie B a 1 beignet. Trouve le tout.'),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<rect id="e1" x="60" y="40" width="230" height="130" rx="10" fill="#e7f5ff" stroke="#0b3d5c" '
                             'stroke-width="4"/><rect id="e2" x="370" y="40" width="230" height="130" rx="10" fill="#fff3bf" '
                             'stroke="#0b3d5c" stroke-width="4"/><rect id="e3" x="165" y="250" width="330" height="140" rx="10" '
                             'fill="#d3f9d8" stroke="#0b3d5c" stroke-width="4"/><text id="e4" x="175" y="30" font-size="24" '
                             'font-family="sans-serif" font-weight="bold" text-anchor="middle" fill="#0b3d5c">part 1</text><text id="e5" '
                             'x="485" y="30" font-size="24" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                             'fill="#0b3d5c">part 2</text><text id="e6" x="330" y="240" font-size="24" font-family="sans-serif" '
                             'font-weight="bold" text-anchor="middle" fill="#0b3d5c">whole</text><circle id="e7" cx="131" cy="105" r="16" '
                             'fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/><circle id="e8" cx="175" cy="105" r="16" fill="#4dabf7" '
                             'stroke="#0b3d5c" stroke-width="3"/><circle id="e9" cx="219" cy="105" r="16" fill="#4dabf7" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle id="e10" cx="485" cy="105" r="16" fill="#4dabf7" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle id="e11" cx="252" cy="320" r="16" fill="#4dabf7" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle id="e12" cx="304" cy="320" r="16" fill="#4dabf7" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle id="e13" cx="356" cy="320" r="16" fill="#4dabf7" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle id="e14" cx="408" cy="320" r="16" fill="#4dabf7" stroke="#0b3d5c" '
                             'stroke-width="3"/>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10', 'e11', 'e12', 'e13', 'e14']}},
            {'k': 't',
             'en': 'Point to the first part: 3. Point to the second part: 1.',
             'ar': 'أشِر إلى الجزء الأول: 3. وأشِر إلى الجزء الثاني: 1.',
             'fr': 'Montre la première partie : 3. Montre la deuxième partie : 1.',
             'label': None},
            {'k': 't',
             'en': 'Join them and count the whole: one, two, three, four.',
             'ar': 'ضمّهما وعدّ الكل: one، two، three، four.',
             'fr': 'Réunis-les et compte le tout : one, two, three, four.',
             'label': None},
            {'k': 'f', 'f': '3 + 1 → whole 4'},
            {'k': 't', 'en': 'The whole is 4.', 'ar': 'الكل هو 4.', 'fr': 'Le tout est 4.', 'label': None}]},
 {'n': '4',
  'page': '27',
  'stmt': ('Scene A: 1 star joins 3 stars. Scene B: 3 stars join 1 star. Are the totals the same?',
           'المشهد A: نجمة تنضم إلى 3 نجوم. المشهد B: 3 نجوم تنضم إلى نجمة. هل المجموعان نفسهما؟',
           'Scène A : 1 étoile rejoint 3 étoiles. Scène B : 3 étoiles rejoignent 1 étoile. Les totaux sont-ils les mêmes ?'),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<polygon id="e1" points="100.0,84.7 106.7,100.8 124.1,102.2 110.8,113.5 114.9,130.5 100.0,121.4 85.1,130.5 '
                             '89.2,113.5 75.9,102.2 93.3,100.8" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e2" '
                             'points="160.0,84.7 166.7,100.8 184.1,102.2 170.8,113.5 174.9,130.5 160.0,121.4 145.1,130.5 149.2,113.5 '
                             '135.9,102.2 153.3,100.8" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e3" '
                             'points="220.0,84.7 226.7,100.8 244.1,102.2 230.8,113.5 234.9,130.5 220.0,121.4 205.1,130.5 209.2,113.5 '
                             '195.9,102.2 213.3,100.8" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e4" '
                             'points="400.0,84.7 406.7,100.8 424.1,102.2 410.8,113.5 414.9,130.5 400.0,121.4 385.1,130.5 389.2,113.5 '
                             '375.9,102.2 393.3,100.8" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e5" '
                             'points="160.0,274.7 166.7,290.8 184.1,292.2 170.8,303.5 174.9,320.5 160.0,311.4 145.1,320.5 149.2,303.5 '
                             '135.9,292.2 153.3,290.8" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e6" '
                             'points="340.0,274.7 346.7,290.8 364.1,292.2 350.8,303.5 354.9,320.5 340.0,311.4 325.1,320.5 329.2,303.5 '
                             '315.9,292.2 333.3,290.8" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e7" '
                             'points="400.0,274.7 406.7,290.8 424.1,292.2 410.8,303.5 414.9,320.5 400.0,311.4 385.1,320.5 389.2,303.5 '
                             '375.9,292.2 393.3,290.8" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e8" '
                             'points="460.0,274.7 466.7,290.8 484.1,292.2 470.8,303.5 474.9,320.5 460.0,311.4 445.1,320.5 449.2,303.5 '
                             '435.9,292.2 453.3,290.8" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8']}},
            {'k': 't',
             'en': 'Let us check by counting. Scene A: one, two, three, four.',
             'ar': 'لنتحقّق بالعدّ. المشهد A: one، two، three، four.',
             'fr': 'Vérifions en comptant. Scène A : one, two, three, four.',
             'label': None},
            {'k': 't',
             'en': 'Scene B: one, two, three, four.',
             'ar': 'المشهد B: one، two، three، four.',
             'fr': 'Scène B : one, two, three, four.',
             'label': None},
            {'k': 'f', 'f': '3 + 1 = 4      1 + 3 = 4'},
            {'k': 't', 'en': 'Yes, the same total: 4.', 'ar': 'نعم، المجموع نفسه: 4.', 'fr': 'Oui, le même total : 4.', 'label': None}]},
 {'n': '5',
  'page': '27',
  'stmt': ('The story: 2 ducks are in the pond. 2 more ducks come. Which picture tells this story? A: 2 ducks only. B: 2 ducks and 2 ducks '
           'joined, making 4. C: 1 duck leaving.',
           'القصة: بطّتان في البركة. تأتي بطّتان أخريان. أي صورة تحكي هذه القصة؟ A: بطّتان فقط. B: بطّتان وبطّتان انضمّتا فصار 4. C: بطة '
           'تغادر.',
           "L'histoire : 2 canards sont dans la mare. 2 autres canards arrivent. Quel dessin raconte cette histoire ? A : 2 canards "
           "seulement. B : 2 canards et 2 canards réunis, 4 en tout. C : 1 canard s'en va."),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<text id="e1" x="40" y="120" font-size="36" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                             'fill="#0b3d5c">B</text><g id="e2"><ellipse cx="140" cy="114" rx="32" ry="22" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle cx="162" cy="91" r="16" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon '
                             'points="175,88 191,92 175,97" fill="#ff922b" stroke="#0b3d5c" stroke-width="2"/><circle cx="166" cy="88" '
                             'r="2.5" fill="#0b3d5c"/></g><g id="e3"><ellipse cx="240" cy="114" rx="32" ry="22" fill="#ffd43b" '
                             'stroke="#0b3d5c" stroke-width="3"/><circle cx="262" cy="91" r="16" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/><polygon points="275,88 291,92 275,97" fill="#ff922b" stroke="#0b3d5c" '
                             'stroke-width="2"/><circle cx="266" cy="88" r="2.5" fill="#0b3d5c"/></g><text id="e4" x="330" y="130" '
                             'font-size="50" font-family="sans-serif" font-weight="bold" text-anchor="middle" fill="#0b3d5c">+</text><g '
                             'id="e5"><ellipse cx="410" cy="114" rx="32" ry="22" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><circle '
                             'cx="432" cy="91" r="16" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon points="445,88 461,92 '
                             '445,97" fill="#ff922b" stroke="#0b3d5c" stroke-width="2"/><circle cx="436" cy="88" r="2.5" '
                             'fill="#0b3d5c"/></g><g id="e6"><ellipse cx="510" cy="114" rx="32" ry="22" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle cx="532" cy="91" r="16" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon '
                             'points="545,88 561,92 545,97" fill="#ff922b" stroke="#0b3d5c" stroke-width="2"/><circle cx="536" cy="88" '
                             'r="2.5" fill="#0b3d5c"/></g><text id="e7" x="600" y="130" font-size="40" font-family="sans-serif" '
                             'font-weight="bold" text-anchor="middle" fill="#0b3d5c">= 4</text>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7']}},
            {'k': 't',
             'en': 'A shows only the first group. C shows a duck leaving, which is not joining.',
             'ar': 'الصورة A تُظهر المجموعة الأولى فقط. والصورة C تُظهر بطة تغادر وهذا ليس انضمامًا.',
             'fr': "Le dessin A ne montre que le premier groupe. Le dessin C montre un canard qui part, ce n'est pas une réunion.",
             'label': None},
            {'k': 't',
             'en': 'B is right. Why? Because there is a group already there, and a new group came and joined it.',
             'ar': 'الصورة B هي الصحيحة. لماذا؟ لأن هناك مجموعة موجودة ومجموعة جديدة جاءت وانضمّت.',
             'fr': "B est juste. Pourquoi ? Parce qu'il y a un groupe déjà là, et un nouveau groupe est venu le rejoindre.",
             'label': None},
            {'k': 'f', 'f': 'B: 2 ducks + 2 ducks → 4'}]},
 {'n': '6',
  'page': '27',
  'stmt': ('The story: 2 cats are sitting. 2 more cats come. Someone says: "Total = 2." Right or wrong?',
           'القصة: قطتان جالستان. تأتي قطتان أخريان. قال أحدهم: «المجموع = 2». صح أم خطأ؟',
           "L'histoire : 2 chats sont assis. 2 autres chats arrivent. Quelqu'un dit : « Total = 2. » Juste ou faux ?"),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<circle id="e1" cx="115" cy="190" r="30" fill="#adb5bd" stroke="#0b3d5c" stroke-width="3"/><circle id="e2" '
                             'cx="205" cy="190" r="30" fill="#adb5bd" stroke="#0b3d5c" stroke-width="3"/><circle id="e3" cx="435" cy="190" '
                             'r="30" fill="#adb5bd" stroke="#0b3d5c" stroke-width="3"/><circle id="e4" cx="525" cy="190" r="30" '
                             'fill="#adb5bd" stroke="#0b3d5c" stroke-width="3"/>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4']}},
            {'k': 't',
             'en': 'It is wrong, because only one group was counted.',
             'ar': 'هذا خطأ لأنه عدّ مجموعة واحدة فقط.',
             'fr': "C'est faux, parce qu'un seul groupe a été compté.",
             'label': None},
            {'k': 't',
             'en': 'Let us do the action: 2 cats and 2 more cats join. Count: one, two, three, four.',
             'ar': 'لنقم بالحركة: قطتان وتنضم قطتان. عدّ: one، two، three، four.',
             'fr': "Faisons l'action : 2 chats et 2 autres chats les rejoignent. Compte : one, two, three, four.",
             'label': None},
            {'k': 'f', 'f': '2 + 2 = 4'},
            {'k': 't', 'en': 'The total is 4.', 'ar': 'المجموع 4.', 'fr': 'Le total est 4.', 'label': None}]},
 {'n': '7',
  'page': '27',
  'stmt': ('There is 1 red block. Then 1 blue block comes. Then 1 green block comes. How many blocks are there now?',
           'هناك مكعب أحمر واحد. ثم يأتي مكعب أزرق. ثم يأتي مكعب أخضر. كم مكعبًا الآن؟',
           'Il y a 1 bloc rouge. Puis 1 bloc bleu arrive. Puis 1 bloc vert arrive. Combien de blocs y a-t-il maintenant ?'),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<rect id="e1" x="184" y="164" width="72" height="72" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><rect '
                             'id="e2" x="294" y="164" width="72" height="72" fill="#339af0" stroke="#0b3d5c" stroke-width="3"/><rect '
                             'id="e3" x="404" y="164" width="72" height="72" fill="#51cf66" stroke="#0b3d5c" stroke-width="3"/>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3']}},
            {'k': 't',
             'en': 'Put all the blocks in one place.',
             'ar': 'نضع كل المكعبات في مكان واحد.',
             'fr': 'On met tous les blocs au même endroit.',
             'label': None},
            {'k': 't',
             'en': 'Count each block once: one, two, three.',
             'ar': 'عدّ كل مكعب مرة: one، two، three.',
             'fr': 'Compte chaque bloc une fois : one, two, three.',
             'label': None},
            {'k': 'f', 'f': '1 + 1 + 1 = 3'},
            {'k': 't',
             'en': 'The total is 3. Addition can describe more than one joining, but the idea is the same: they all become one whole.',
             'ar': 'المجموع 3. يمكن للجمع أن يصف أكثر من انضمام، لكن الفكرة نفسها: كلها تصير كلًّا واحدًا.',
             'fr': "Le total est 3. L'addition peut décrire plusieurs réunions, mais l'idée est la même : tout devient un seul tout.",
             'label': None}]},
 {'n': '8',
  'page': '27',
  'stmt': ('Final challenge. 1) 2 objects, 1 joins: how many now? 2) 1 object, 3 join: how many altogether? 3) 2 objects, 2 join: total? '
           '4) 3 birds on a fence, 1 more comes: what happens, and how many now? 5) 1 car, 2 cars join: what was there, what joined, what '
           'is the total?',
           'التحدي الأخير. 1) شيئان وينضم 1: كم الآن؟ 2) شيء وينضم 3: كم كلها؟ 3) شيئان وينضم شيئان: المجموع؟ 4) 3 عصافير على سور وجاء '
           'عصفور: ماذا يحدث وكم الآن؟ 5) سيارة وتنضم سيارتان: ماذا كان؟ وماذا انضمّ؟ وما المجموع؟',
           'Défi final. 1) 2 objets, 1 arrive : combien maintenant ? 2) 1 objet, 3 arrivent : combien en tout ? 3) 2 objets, 2 arrivent : '
           'total ? 4) 3 oiseaux sur une clôture, 1 de plus arrive : que se passe-t-il, combien maintenant ? 5) 1 voiture, 2 voitures '
           "arrivent : qu'y avait-il, qu'est-ce qui est arrivé, quel est le total ?"),
  'steps': [{'k': 't',
             'en': 'Task 1: 2 and 1 joins: one, two, three.',
             'ar': 'المهمة 1: 2 وينضم 1: one، two، three.',
             'fr': 'Tâche 1 : 2 et 1 arrive : one, two, three.',
             'label': None},
            {'k': 'f', 'f': '2 + 1 = 3'},
            {'k': 't',
             'en': 'Task 2: 1 and 3 join: one, two, three, four.',
             'ar': 'المهمة 2: 1 وينضم 3: one، two، three، four.',
             'fr': 'Tâche 2 : 1 et 3 arrivent : one, two, three, four.',
             'label': None},
            {'k': 'f', 'f': '1 + 3 = 4'},
            {'k': 't',
             'en': 'Task 3: 2 and 2 join: one, two, three, four.',
             'ar': 'المهمة 3: 2 وينضم 2: one، two، three، four.',
             'fr': 'Tâche 3 : 2 et 2 arrivent : one, two, three, four.',
             'label': None},
            {'k': 'f', 'f': '2 + 2 = 4'},
            {'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<g id="e1"><ellipse cx="150" cy="204" rx="30" ry="21" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle cx="171" cy="182" r="15" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/><polygon points="183,179 198,184 183,188" fill="#ff922b" stroke="#0b3d5c" '
                             'stroke-width="2"/><circle cx="174" cy="179" r="2.5" fill="#0b3d5c"/></g><g id="e2"><ellipse cx="250" '
                             'cy="204" rx="30" ry="21" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><circle cx="271" cy="182" r="15" '
                             'fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon points="283,179 298,184 283,188" fill="#ff922b" '
                             'stroke="#0b3d5c" stroke-width="2"/><circle cx="274" cy="179" r="2.5" fill="#0b3d5c"/></g><g id="e3"><ellipse '
                             'cx="350" cy="204" rx="30" ry="21" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><circle cx="371" '
                             'cy="182" r="15" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon points="383,179 398,184 383,188" '
                             'fill="#ff922b" stroke="#0b3d5c" stroke-width="2"/><circle cx="374" cy="179" r="2.5" fill="#0b3d5c"/></g><g '
                             'id="e4"><ellipse cx="560" cy="204" rx="30" ry="21" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><circle '
                             'cx="581" cy="182" r="15" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon points="593,179 608,184 '
                             '593,188" fill="#ff922b" stroke="#0b3d5c" stroke-width="2"/><circle cx="584" cy="179" r="2.5" '
                             'fill="#0b3d5c"/></g>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4']}},
            {'k': 't',
             'en': 'Task 4: the group gets bigger. 3 birds and 1 more bird: one, two, three, four.',
             'ar': 'المهمة 4: تصبح المجموعة أكبر. 3 عصافير وعصفور آخر: one، two، three، four.',
             'fr': 'Tâche 4 : le groupe devient plus grand. 3 oiseaux et 1 oiseau de plus : one, two, three, four.',
             'label': None},
            {'k': 'f', 'f': '3 + 1 = 4'},
            {'k': 't',
             'en': 'Task 5: 1 car was there. 2 cars joined. The total is 3.',
             'ar': 'المهمة 5: كانت هناك سيارة واحدة. انضمّت سيارتان. المجموع 3.',
             'fr': 'Tâche 5 : il y avait 1 voiture. 2 voitures sont arrivées. Le total est 3.',
             'label': None},
            {'k': 'f', 'f': '1 + 2 = 3'}]}]


def scenes():
    return make_scenes(THEORY, EXERCISES)
