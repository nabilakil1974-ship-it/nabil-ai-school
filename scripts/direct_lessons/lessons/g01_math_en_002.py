"""Direct lesson data: Grade 1 Mathematics — The numbers from 1 to 3.

Written once in three languages; every text step carries its own ar/en/fr twin."""
from __future__ import annotations

LESSON_ID = 'G01-MATH-EN-002'
GRADE = 1
SUBJECT = "math"
TITLES = {'en': 'The numbers from 1 to 3', 'ar': 'الأعداد من 1 إلى 3', 'fr': 'Les nombres de 1 à 3'}

from scripts.direct_lessons.common import T, F, D, EX, st, S, make_scenes


THEORY = [('One star: quantity and numeral',
  'نجمة واحدة: الكمية والرقم',
  'Une étoile : quantité et chiffre',
  '16',
  [{'k': 't',
    'en': 'Hello, champion! Today we meet three small but very important numbers: 1, 2 and 3.',
    'ar': 'مرحبًا يا بطل! اليوم نتعرّف إلى ثلاثة أرقام صغيرة لكنها مهمة جدًا: 1 و2 و3.',
    'fr': "Bonjour, champion ! Aujourd'hui, nous découvrons trois petits nombres très importants : 1, 2 et 3.",
    'label': None},
   {'k': 't',
    'en': 'Do not only learn the shape of a number. Learn what the number means.',
    'ar': 'لا نحفظ شكل الرقم فقط. نريد أن نعرف ماذا يعني الرقم.',
    'fr': "Ne retiens pas seulement la forme du chiffre. Apprends ce qu'il veut dire.",
    'label': None},
   {'k': 't',
    'en': 'Look carefully. How many stars do you see? One star.',
    'ar': 'انظر جيدًا. كم نجمة ترى؟ نجمة واحدة.',
    'fr': "Regarde bien. Combien d'étoiles vois-tu ? Une étoile.",
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<polygon id="e1" points="330.0,131.0 348.3,174.9 395.6,178.7 359.5,209.6 370.6,255.8 330.0,231.1 289.4,255.8 '
                    '300.5,209.6 264.4,178.7 311.7,174.9" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/>',
             'vb': [660, 440],
             'show': ['e1']}},
   {'k': 't',
    'en': 'We say it in English: one. And the shape of the number for one is 1.',
    'ar': 'نقولها بالإنكليزية: one. وشكل الرقم الذي يمثّل one هو 1.',
    'fr': "On le dit en anglais : one. Et le chiffre qui représente one s'écrit 1.",
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<polygon id="e1" points="200.0,131.0 218.3,174.9 265.6,178.7 229.5,209.6 240.6,255.8 200.0,231.1 159.4,255.8 '
                    '170.5,209.6 134.4,178.7 181.7,174.9" fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><text id="e2" x="330" y="225" '
                    'font-size="64" font-family="sans-serif" font-weight="bold" text-anchor="middle" fill="#0b3d5c">=</text><text id="e3" '
                    'x="460" y="235" font-size="110" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                    'fill="#0b3d5c">1</text>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3']}},
   {'k': 't',
    'en': 'The star is the quantity: how many there are. The 1 is the numeral: how we write it.',
    'ar': 'النجمة هي الكمية: أي كم يوجد. والرقم 1 هو شكل الكتابة.',
    'fr': "L'étoile est la quantité : combien il y en a. Le 1 est le chiffre : comment on l'écrit.",
    'label': None},
   {'k': 'f', 'f': '⭐ = one = 1'}]),
 ('Number 1: one object',
  'العدد 1: شيء واحد',
  'Le nombre 1 : un objet',
  '16',
  [{'k': 't',
    'en': 'Let us try. One apple appears. How many apples? One.',
    'ar': 'لنجرّب. ظهرت تفاحة واحدة. كم تفاحة؟ واحدة.',
    'fr': 'Essayons. Une pomme apparaît. Combien de pommes ? Une.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<g id="e1"><circle cx="330" cy="203" r="60" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><line x1="330" y1="143" '
                    'x2="335" y2="131" stroke="#7a4a1d" stroke-width="4"/><ellipse cx="341" cy="136" rx="8" ry="4" fill="#40c057" '
                    'stroke="#0b3d5c" stroke-width="2"/></g>',
             'vb': [660, 440],
             'show': ['e1']}},
   {'k': 't',
    'en': 'Which number card goes next to it? We count first, then we choose.',
    'ar': 'أي بطاقة رقم نضع بجانبها؟ نعدّ أولًا ثم نختار.',
    'fr': "Quelle carte-nombre met-on à côté ? On compte d'abord, puis on choisit.",
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<rect id="e1" x="160" y="255" width="80" height="90" rx="10" fill="#fff3bf" stroke="#0b3d5c" stroke-width="4"/><text '
                    'id="e2" x="200" y="322" font-size="64" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                    'fill="#0b3d5c">1</text><rect id="e3" x="290" y="255" width="80" height="90" rx="10" fill="#fff3bf" stroke="#0b3d5c" '
                    'stroke-width="4"/><text id="e4" x="330" y="322" font-size="64" font-family="sans-serif" font-weight="bold" '
                    'text-anchor="middle" fill="#0b3d5c">2</text><rect id="e5" x="420" y="255" width="80" height="90" rx="10" '
                    'fill="#fff3bf" stroke="#0b3d5c" stroke-width="4"/><text id="e6" x="460" y="322" font-size="64" '
                    'font-family="sans-serif" font-weight="bold" text-anchor="middle" fill="#0b3d5c">3</text><g id="e7"><circle cx="330" '
                    'cy="123" r="45" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><line x1="330" y1="78" x2="335" y2="66" '
                    'stroke="#7a4a1d" stroke-width="4"/><ellipse cx="341" cy="71" rx="8" ry="4" fill="#40c057" stroke="#0b3d5c" '
                    'stroke-width="2"/></g>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7']}},
   {'k': 't',
    'en': 'One apple, so the card is 1. Why not 2? Because there is only one apple. The number must match how many things there are.',
    'ar': 'تفاحة واحدة، إذن البطاقة 1. لماذا ليس 2؟ لأن هناك تفاحة واحدة فقط. يجب أن يطابق الرقم عدد الأشياء.',
    'fr': "Une pomme, donc la carte est 1. Pourquoi pas 2 ? Parce qu'il n'y a qu'une pomme. Le nombre doit correspondre au nombre "
          "d'objets.",
    'label': None},
   {'k': 'f', 'f': '🍎 → 1'},
   {'k': 't',
    'en': 'First we find how many things there are. Then we choose the number.',
    'ar': 'أولًا نعرف كم شيئًا يوجد، ثم نختار الرقم.',
    'fr': "D'abord on trouve combien il y a d'objets, ensuite on choisit le nombre.",
    'label': None},
   {'k': 't',
    'en': 'The number 1 means: I have one thing.',
    'ar': 'الرقم 1 يعني: عندي شيء واحد.',
    'fr': "Le nombre 1 veut dire : j'ai un objet.",
    'label': None}]),
 ('Number 2: counting two objects',
  'العدد 2: عدّ شيئين',
  'Le nombre 2 : compter deux objets',
  '16',
  [{'k': 't',
    'en': 'Now there are more cars. Do not answer fast. We count together, and the rule is: touch each car only once.',
    'ar': 'الآن توجد سيارات أكثر. لا نجب بسرعة. نعدّ معًا، والقاعدة: نلمس كل سيارة مرة واحدة فقط.',
    'fr': 'Maintenant, il y a plus de voitures. Ne réponds pas vite. On compte ensemble, et la règle est : on touche chaque voiture une '
          'seule fois.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<g id="e1"><rect x="181" y="182" width="108" height="40" rx="6" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><rect x="208" y="157" width="54" height="27" rx="5" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><circle cx="208" cy="225" r="14" fill="#0b3d5c"/><circle cx="262" cy="225" r="14" '
                    'fill="#0b3d5c"/></g><g id="e2"><rect x="371" y="182" width="108" height="40" rx="6" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><rect x="398" y="157" width="54" height="27" rx="5" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><circle cx="398" cy="225" r="14" fill="#0b3d5c"/><circle cx="452" cy="225" r="14" '
                    'fill="#0b3d5c"/></g>',
             'vb': [660, 440],
             'show': ['e1', 'e2']}},
   {'k': 't',
    'en': 'The first car: one. The second car: two.',
    'ar': 'السيارة الأولى: one. السيارة الثانية: two.',
    'fr': 'La première voiture : one. La deuxième voiture : two.',
    'label': None},
   {'k': 't',
    'en': 'What is the last word we said? Two. The last number tells us how many cars there are in all.',
    'ar': 'ما آخر كلمة قلناها؟ two. آخر عدد نقوله يخبرنا كم سيارة يوجد كلها.',
    'fr': 'Quel est le dernier mot dit ? Two. Le dernier nombre nous dit combien il y a de voitures en tout.',
    'label': None},
   {'k': 'f', 'f': '🚗 🚗 = two = 2'},
   {'k': 't',
    'en': 'Say it with me: two cars, number 2.',
    'ar': 'قلها معي: two cars، العدد 2.',
    'fr': 'Dis-le avec moi : two cars, le nombre 2.',
    'label': None}]),
 ('Number 3: counting three objects',
  'العدد 3: عدّ ثلاثة أشياء',
  'Le nombre 3 : compter trois objets',
  '17',
  [{'k': 't',
    'en': 'Now we have teddy bears. I will not tell you the number before we count. Touch each teddy once.',
    'ar': 'الآن لدينا دببة. لن أخبرك بالعدد قبل أن نعدّ. المس كل دبّ مرة واحدة.',
    'fr': 'Maintenant, nous avons des nounours. Je ne te dis pas le nombre avant de compter. Touche chaque nounours une fois.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<g id="e1"><circle cx="140" cy="160" r="20" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="220" '
                    'cy="160" r="20" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="180" cy="200" r="50" fill="#c98f55" '
                    'stroke="#0b3d5c" stroke-width="3"/><circle cx="173" cy="196" r="3" fill="#0b3d5c"/><circle cx="187" cy="196" r="3" '
                    'fill="#0b3d5c"/><ellipse cx="180" cy="207" rx="6" ry="4" fill="#f1d3a8" stroke="#0b3d5c" stroke-width="2"/></g><g '
                    'id="e2"><circle cx="290" cy="160" r="20" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="370" cy="160" '
                    'r="20" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="330" cy="200" r="50" fill="#c98f55" '
                    'stroke="#0b3d5c" stroke-width="3"/><circle cx="323" cy="196" r="3" fill="#0b3d5c"/><circle cx="337" cy="196" r="3" '
                    'fill="#0b3d5c"/><ellipse cx="330" cy="207" rx="6" ry="4" fill="#f1d3a8" stroke="#0b3d5c" stroke-width="2"/></g><g '
                    'id="e3"><circle cx="440" cy="160" r="20" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="520" cy="160" '
                    'r="20" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="480" cy="200" r="50" fill="#c98f55" '
                    'stroke="#0b3d5c" stroke-width="3"/><circle cx="473" cy="196" r="3" fill="#0b3d5c"/><circle cx="487" cy="196" r="3" '
                    'fill="#0b3d5c"/><ellipse cx="480" cy="207" rx="6" ry="4" fill="#f1d3a8" stroke="#0b3d5c" stroke-width="2"/></g>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3']}},
   {'k': 't', 'en': 'One. Two. Three.', 'ar': 'one. two. three.', 'fr': 'One. Two. Three.', 'label': None},
   {'k': 't',
    'en': 'What was the last number we said? Three. So how many teddy bears are there? Three.',
    'ar': 'ما آخر عدد قلناه؟ three. إذن كم دبًّا يوجد؟ ثلاثة.',
    'fr': 'Quel est le dernier nombre dit ? Three. Combien y a-t-il de nounours ? Trois.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<g id="e1"><circle cx="81" cy="171" r="14" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="139" '
                    'cy="171" r="14" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="110" cy="200" r="36" fill="#c98f55" '
                    'stroke="#0b3d5c" stroke-width="3"/><circle cx="103" cy="196" r="3" fill="#0b3d5c"/><circle cx="117" cy="196" r="3" '
                    'fill="#0b3d5c"/><ellipse cx="110" cy="207" rx="6" ry="4" fill="#f1d3a8" stroke="#0b3d5c" stroke-width="2"/></g><g '
                    'id="e2"><circle cx="181" cy="171" r="14" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="239" cy="171" '
                    'r="14" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="210" cy="200" r="36" fill="#c98f55" '
                    'stroke="#0b3d5c" stroke-width="3"/><circle cx="203" cy="196" r="3" fill="#0b3d5c"/><circle cx="217" cy="196" r="3" '
                    'fill="#0b3d5c"/><ellipse cx="210" cy="207" rx="6" ry="4" fill="#f1d3a8" stroke="#0b3d5c" stroke-width="2"/></g><g '
                    'id="e3"><circle cx="281" cy="171" r="14" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="339" cy="171" '
                    'r="14" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="310" cy="200" r="36" fill="#c98f55" '
                    'stroke="#0b3d5c" stroke-width="3"/><circle cx="303" cy="196" r="3" fill="#0b3d5c"/><circle cx="317" cy="196" r="3" '
                    'fill="#0b3d5c"/><ellipse cx="310" cy="207" rx="6" ry="4" fill="#f1d3a8" stroke="#0b3d5c" stroke-width="2"/></g><text '
                    'id="e4" x="400" y="225" font-size="60" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                    'fill="#0b3d5c">=</text><text id="e5" x="510" y="235" font-size="110" font-family="sans-serif" font-weight="bold" '
                    'text-anchor="middle" fill="#0b3d5c">3</text>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5']}},
   {'k': 'f', 'f': '🧸 🧸 🧸 = three = 3'}]),
 ('Moving things does not change how many',
  'تحريك الأشياء لا يغيّر العدد',
  'Déplacer ne change pas le nombre',
  '17',
  [{'k': 't',
    'en': 'Three dots stand in a straight line. Count them: one, two, three. There are 3.',
    'ar': 'ثلاث نقاط على خط مستقيم. عدّها: one، two، three. عددها 3.',
    'fr': 'Trois points sont alignés. Compte-les : one, two, three. Il y en a 3.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<circle id="e1" cx="210" cy="200" r="24" fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle id="e2" cx="330" '
                    'cy="200" r="24" fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle id="e3" cx="450" cy="200" r="24" '
                    'fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3']}},
   {'k': 't',
    'en': 'Now the dots move and make a triangle. The shape of the group changed. Are there 2 dots now, or still 3?',
    'ar': 'الآن تتحرّك النقاط وتشكّل مثلثًا. تغيّر شكل المجموعة. هل صارت النقاط 2 أم ما زالت 3؟',
    'fr': 'Maintenant, les points bougent et forment un triangle. La forme du groupe a changé. Y a-t-il 2 points, ou encore 3 ?',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<circle id="e1" cx="330" cy="120" r="24" fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle id="e2" cx="240" '
                    'cy="290" r="24" fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle id="e3" cx="420" cy="290" r="24" '
                    'fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3']}},
   {'k': 't',
    'en': 'Still 3! We did not add a dot and we did not take one away. Let us prove it by counting: one, two, three.',
    'ar': 'ما زالت 3! لم نضف نقطة ولم نأخذ نقطة. لنثبت ذلك بالعدّ: one، two، three.',
    'fr': "Toujours 3 ! On n'a ni ajouté ni retiré de point. Prouvons-le en comptant : one, two, three.",
    'label': None},
   {'k': 't',
    'en': 'The arrangement changes, but the quantity stays the same.',
    'ar': 'يتغيّر الترتيب، لكن الكمية تبقى كما هي.',
    'fr': 'La disposition change, mais la quantité reste la même.',
    'label': None},
   {'k': 't',
    'en': 'Things can move and spread out. If we add nothing and take nothing, the number stays the same.',
    'ar': 'يمكن للأشياء أن تتحرّك وتتباعد. إذا لم نضف شيئًا ولم نأخذ شيئًا يبقى العدد نفسه.',
    'fr': "Les objets peuvent bouger et s'écarter. Si on n'ajoute rien et qu'on n'enlève rien, le nombre reste le même.",
    'label': None}]),
 ('Reading and writing 1, 2, 3',
  'قراءة وكتابة 1 و2 و3',
  'Lire et écrire 1, 2, 3',
  '17',
  [{'k': 't',
    'en': 'Now we know what the numbers mean. Let us read them.',
    'ar': 'صرنا نعرف معنى الأرقام. لنقرأها الآن.',
    'fr': 'Maintenant, nous savons ce que les nombres veulent dire. Lisons-les.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<text id="e1" x="160" y="250" font-size="130" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                    'fill="#0b3d5c">1</text><text id="e2" x="330" y="250" font-size="130" font-family="sans-serif" font-weight="bold" '
                    'text-anchor="middle" fill="#0b3d5c">2</text><text id="e3" x="500" y="250" font-size="130" font-family="sans-serif" '
                    'font-weight="bold" text-anchor="middle" fill="#0b3d5c">3</text>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3']}},
   {'k': 't',
    'en': 'This is one. This is two. This is three.',
    'ar': 'هذا one. وهذا two. وهذا three.',
    'fr': 'Voici one. Voici two. Voici three.',
    'label': None},
   {'k': 't',
    'en': 'If you know the name of a number but not how many it means, you have not understood it yet. So every number needs real things.',
    'ar': 'إذا عرفت اسم الرقم ولم تعرف كم يمثّل فلم تفهمه كاملًا بعد. لذلك نربط كل رقم بأشياء حقيقية.',
    'fr': "Si tu connais le nom du nombre mais pas la quantité qu'il représente, tu ne l'as pas encore compris. Chaque nombre doit donc "
          'être relié à de vrais objets.',
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<text id="e1" x="90" y="120" font-size="70" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                    'fill="#0b3d5c">1</text><g id="e2"><circle cx="250" cy="108" r="30" fill="#e03131" stroke="#0b3d5c" '
                    'stroke-width="3"/><line x1="250" y1="78" x2="255" y2="66" stroke="#7a4a1d" stroke-width="4"/><ellipse cx="261" '
                    'cy="71" rx="8" ry="4" fill="#40c057" stroke="#0b3d5c" stroke-width="2"/></g><text id="e3" x="90" y="250" '
                    'font-size="70" font-family="sans-serif" font-weight="bold" text-anchor="middle" fill="#0b3d5c">2</text><g '
                    'id="e4"><rect x="209" y="223" width="72" height="27" rx="6" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><rect '
                    'x="227" y="206" width="36" height="18" rx="5" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><circle cx="227" '
                    'cy="252" r="9" fill="#0b3d5c"/><circle cx="263" cy="252" r="9" fill="#0b3d5c"/></g><g id="e5"><rect x="319" y="223" '
                    'width="72" height="27" rx="6" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><rect x="337" y="206" width="36" '
                    'height="18" rx="5" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><circle cx="337" cy="252" r="9" '
                    'fill="#0b3d5c"/><circle cx="373" cy="252" r="9" fill="#0b3d5c"/></g><text id="e6" x="90" y="380" font-size="70" '
                    'font-family="sans-serif" font-weight="bold" text-anchor="middle" fill="#0b3d5c">3</text><g id="e7"><circle cx="186" '
                    'cy="341" r="12" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="234" cy="341" r="12" fill="#a9703c" '
                    'stroke="#0b3d5c" stroke-width="3"/><circle cx="210" cy="365" r="30" fill="#c98f55" stroke="#0b3d5c" '
                    'stroke-width="3"/><circle cx="203" cy="361" r="3" fill="#0b3d5c"/><circle cx="217" cy="361" r="3" '
                    'fill="#0b3d5c"/><ellipse cx="210" cy="372" rx="6" ry="4" fill="#f1d3a8" stroke="#0b3d5c" stroke-width="2"/></g><g '
                    'id="e8"><circle cx="276" cy="341" r="12" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="324" cy="341" '
                    'r="12" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="300" cy="365" r="30" fill="#c98f55" '
                    'stroke="#0b3d5c" stroke-width="3"/><circle cx="293" cy="361" r="3" fill="#0b3d5c"/><circle cx="307" cy="361" r="3" '
                    'fill="#0b3d5c"/><ellipse cx="300" cy="372" rx="6" ry="4" fill="#f1d3a8" stroke="#0b3d5c" stroke-width="2"/></g><g '
                    'id="e9"><circle cx="366" cy="341" r="12" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="414" cy="341" '
                    'r="12" fill="#a9703c" stroke="#0b3d5c" stroke-width="3"/><circle cx="390" cy="365" r="30" fill="#c98f55" '
                    'stroke="#0b3d5c" stroke-width="3"/><circle cx="383" cy="361" r="3" fill="#0b3d5c"/><circle cx="397" cy="361" r="3" '
                    'fill="#0b3d5c"/><ellipse cx="390" cy="372" rx="6" ry="4" fill="#f1d3a8" stroke="#0b3d5c" stroke-width="2"/></g>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9']}},
   {'k': 'f', 'f': '1 → 🍎      2 → 🚗 🚗      3 → 🧸 🧸 🧸'},
   {'k': 't',
    'en': 'Only after we understand the meaning, we write the numbers. Trace 1, 2 and 3 with your finger on the dotted lines. Each time '
          'you write a number, remember how many it means.',
    'ar': 'بعد أن نفهم المعنى نكتب الأرقام. تتبّع 1 و2 و3 بإصبعك على الخطوط المنقّطة. وفي كل مرة تكتب رقمًا تذكّر كم يمثّل.',
    'fr': 'Quand on a compris le sens, on écrit les nombres. Suis 1, 2 et 3 du doigt sur les pointillés. À chaque fois que tu écris un '
          "nombre, souviens-toi de ce qu'il représente.",
    'label': None},
   {'k': 'f', 'f': '1 = one object      2 = two objects      3 = three objects'}]),
 ('Mistakes to avoid',
  'أخطاء يجب تجنّبها',
  'Erreurs à éviter',
  '17',
  [{'k': 't',
    'en': 'Mistake 1: counting one object twice. If you say one, two, three, four, but there are only 3 balls, you probably touched one '
          'ball twice. Touch each object once.',
    'ar': 'الخطأ 1: عدّ الشيء نفسه مرتين. إذا قلت one، two، three، four وعندك 3 كرات فقط فغالبًا لمست كرة مرتين. المس كل شيء مرة واحدة.',
    'fr': "Erreur 1 : compter deux fois le même objet. Si tu dis one, two, three, four alors qu'il n'y a que 3 balles, tu as sans doute "
          'touché une balle deux fois. Touche chaque objet une seule fois.',
    'label': None},
   {'k': 't',
    'en': 'Mistake 2: skipping an object. If there are 3 stars and you say only one, two, you may have forgotten one. Touch every object '
          'while you count.',
    'ar': 'الخطأ 2: نسيان شيء. إذا كان عندك 3 نجوم وقلت one، two فقط فربما نسيت نجمة. المس كل شيء أثناء العدّ.',
    'fr': "Erreur 2 : oublier un objet. S'il y a 3 étoiles et que tu dis seulement one, two, tu as peut-être oublié une étoile. Touche "
          'chaque objet pendant que tu comptes.',
    'label': None},
   {'k': 't',
    'en': 'Mistake 3: choosing a numeral by its look. We do not choose 3 because it looks nice or because it is the last card. We count '
          'first, then choose the numeral that matches.',
    'ar': 'الخطأ 3: اختيار الرقم من شكله. لا نختار 3 لأن شكله جميل أو لأنه آخر بطاقة. نعدّ أولًا ثم نختار الرقم المطابق.',
    'fr': "Erreur 3 : choisir le chiffre d'après son aspect. On ne choisit pas 3 parce qu'il est joli ou parce que c'est la dernière "
          "carte. On compte d'abord, puis on choisit le chiffre qui correspond.",
    'label': None},
   {'k': 't',
    'en': 'Mistake 4: thinking spread-out things are more. Look at two groups of 3 dots: one close together, one far apart.',
    'ar': 'الخطأ 4: ظن أن الأشياء المتباعدة أكثر. انظر إلى مجموعتين من 3 نقاط: واحدة متقاربة وواحدة متباعدة.',
    'fr': "Erreur 4 : croire que des objets écartés sont plus nombreux. Regarde deux groupes de 3 points : l'un serré, l'autre écarté.",
    'label': None},
   {'k': 'd',
    'draw': 'svgScene',
    'args': {'svg': '<circle id="e1" cx="280" cy="120" r="17" fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle id="e2" cx="330" '
                    'cy="120" r="17" fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle id="e3" cx="380" cy="120" r="17" '
                    'fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/><circle id="e4" cx="80" cy="300" r="17" fill="#0b3d5c" '
                    'stroke="#0b3d5c" stroke-width="3"/><circle id="e5" cx="330" cy="300" r="17" fill="#0b3d5c" stroke="#0b3d5c" '
                    'stroke-width="3"/><circle id="e6" cx="580" cy="300" r="17" fill="#0b3d5c" stroke="#0b3d5c" stroke-width="3"/>',
             'vb': [660, 440],
             'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6']}},
   {'k': 't',
    'en': 'Count the first group: one, two, three. Count the second: one, two, three. Both have 3. The space between things does not '
          'change the number.',
    'ar': 'عدّ المجموعة الأولى: one، two، three. وعدّ الثانية: one، two، three. في كلتيهما 3. المسافة بين الأشياء لا تغيّر العدد.',
    'fr': "Compte le premier groupe : one, two, three. Compte le deuxième : one, two, three. Il y en a 3 dans les deux. L'espace entre les "
          'objets ne change pas le nombre.',
    'label': None}]),
 ('Summary',
  'الخلاصة',
  'Résumé',
  '17',
  [{'k': 't',
    'en': 'Well done! Today we learned three numbers.',
    'ar': 'أحسنت! تعلّمنا اليوم ثلاثة أرقام.',
    'fr': "Bravo ! Aujourd'hui, nous avons appris trois nombres.",
    'label': None},
   {'k': 'f', 'f': '⭐ = one = 1'},
   {'k': 'f', 'f': '⭐ ⭐ = two = 2'},
   {'k': 'f', 'f': '⭐ ⭐ ⭐ = three = 3'},
   {'k': 't',
    'en': 'When we count, we do two important things: we touch each object once, and the last number we say tells us how many.',
    'ar': 'عندما نعدّ نفعل أمرين مهمين: نلمس كل شيء مرة واحدة، وآخر عدد نقوله يخبرنا كم الأشياء.',
    'fr': 'Quand on compte, on fait deux choses importantes : on touche chaque objet une fois, et le dernier nombre dit nous donne combien '
          'il y en a.',
    'label': None},
   {'k': 't',
    'en': 'If things move but we add nothing and take nothing, the number stays the same.',
    'ar': 'إذا تحرّكت الأشياء ولم نضف ولم نأخذ شيئًا يبقى العدد نفسه.',
    'fr': "Si les objets bougent sans que l'on ajoute ni retire rien, le nombre reste le même.",
    'label': None},
   {'k': 'f', 'f': 'TOUCH → COUNT → LAST NUMBER → CHOOSE THE NUMERAL → CHECK'}])]


EXERCISES = [{'n': '1',
  'page': '16',
  'stmt': ('Count the circles and choose the right number card: 1, 2 or 3.',
           'عدّ الدائرتين واختر بطاقة الرقم الصحيحة: 1 أو 2 أو 3.',
           'Compte les cercles et choisis la bonne carte : 1, 2 ou 3.'),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<circle id="e1" cx="260" cy="120" r="45" fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/><circle id="e2" '
                             'cx="400" cy="120" r="45" fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/><rect id="e3" x="140" y="285" '
                             'width="80" height="90" rx="10" fill="#fff3bf" stroke="#0b3d5c" stroke-width="4"/><text id="e4" x="180" '
                             'y="352" font-size="64" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                             'fill="#0b3d5c">1</text><rect id="e5" x="290" y="285" width="80" height="90" rx="10" fill="#fff3bf" '
                             'stroke="#0b3d5c" stroke-width="4"/><text id="e6" x="330" y="352" font-size="64" font-family="sans-serif" '
                             'font-weight="bold" text-anchor="middle" fill="#0b3d5c">2</text><rect id="e7" x="440" y="285" width="80" '
                             'height="90" rx="10" fill="#fff3bf" stroke="#0b3d5c" stroke-width="4"/><text id="e8" x="480" y="352" '
                             'font-size="64" font-family="sans-serif" font-weight="bold" text-anchor="middle" fill="#0b3d5c">3</text>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8']}},
            {'k': 't',
             'en': 'Start at the first circle and touch each one once: one, two.',
             'ar': 'ابدأ من أول دائرة والمس كل واحدة مرة: one، two.',
             'fr': 'Commence par le premier cercle et touche-les une fois chacun : one, two.',
             'label': None},
            {'k': 't',
             'en': 'The last word is two. So we look for the numeral 2.',
             'ar': 'آخر كلمة هي two. إذن نبحث عن الرقم 2.',
             'fr': 'Le dernier mot est two. On cherche donc le chiffre 2.',
             'label': None},
            {'k': 'f', 'f': '🔵 🔵 = 2'},
            {'k': 't',
             'en': 'Why 2? Because there are two circles.',
             'ar': 'لماذا 2؟ لأن هناك دائرتين.',
             'fr': "Pourquoi 2 ? Parce qu'il y a deux cercles.",
             'label': None}]},
 {'n': '2',
  'page': '17',
  'stmt': ('The number 3 is shown. Build 3 stars in the box.',
           'ظهر الرقم 3. ابنِ 3 نجوم داخل الصندوق.',
           'Le nombre 3 est affiché. Construis 3 étoiles dans la boîte.'),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<text id="e1" x="120" y="130" font-size="110" font-family="sans-serif" font-weight="bold" '
                             'text-anchor="middle" fill="#0b3d5c">3</text><rect id="e2" x="220" y="60" width="380" height="160" rx="10" '
                             'fill="none" stroke="#0b3d5c" stroke-width="4" stroke-dasharray="10 8"/><polygon id="e3" points="300.0,98.6 '
                             '311.0,124.9 339.4,127.2 317.7,145.8 324.3,173.5 300.0,158.6 275.7,173.5 282.3,145.8 260.6,127.2 289.0,124.9" '
                             'fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e4" points="410.0,98.6 421.0,124.9 '
                             '449.4,127.2 427.7,145.8 434.3,173.5 410.0,158.6 385.7,173.5 392.3,145.8 370.6,127.2 399.0,124.9" '
                             'fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/><polygon id="e5" points="520.0,98.6 531.0,124.9 '
                             '559.4,127.2 537.7,145.8 544.3,173.5 520.0,158.6 495.7,173.5 502.3,145.8 480.6,127.2 509.0,124.9" '
                             'fill="#ffd43b" stroke="#0b3d5c" stroke-width="3"/>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4', 'e5']}},
            {'k': 't',
             'en': 'The number is 3, so we need three stars in the box.',
             'ar': 'الرقم 3، إذن نحتاج إلى ثلاث نجوم في الصندوق.',
             'fr': 'Le nombre est 3, il faut donc trois étoiles dans la boîte.',
             'label': None},
            {'k': 't',
             'en': 'Let us check by counting: one, two, three. Yes, 3 stars.',
             'ar': 'لنتحقّق بالعدّ: one، two، three. نعم، 3 نجوم.',
             'fr': 'Vérifions en comptant : one, two, three. Oui, 3 étoiles.',
             'label': None},
            {'k': 't',
             'en': 'If there were only 2 stars, we would add one. If there were more than 3, we would take the extra ones away and stop at '
                   '3.',
             'ar': 'لو كان فيه نجمتان فقط لأضفنا نجمة. ولو كان فيه أكثر من 3 لأزلنا الزائد ووقفنا عند 3.',
             'fr': "S'il n'y avait que 2 étoiles, on en ajouterait une. S'il y en avait plus de 3, on retirerait les étoiles en trop pour "
                   "s'arrêter à 3.",
             'label': None},
            {'k': 'f', 'f': '3 → ⭐ ⭐ ⭐'}]},
 {'n': '3',
  'page': '17',
  'stmt': ('Match each group to its number: A one star, B two apples, C three circles.',
           'صِل كل مجموعة بالرقم المناسب: A نجمة، B تفاحتان، C ثلاث دوائر.',
           'Relie chaque groupe à son nombre : A une étoile, B deux pommes, C trois cercles.'),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<text id="e1" x="70" y="120" font-size="40" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                             'fill="#0b3d5c">A</text><polygon id="e2" points="200.0,70.5 209.1,92.4 232.8,94.3 214.8,109.8 220.3,132.9 '
                             '200.0,120.5 179.7,132.9 185.2,109.8 167.2,94.3 190.9,92.4" fill="#ffd43b" stroke="#0b3d5c" '
                             'stroke-width="3"/><text id="e3" x="450" y="120" font-size="56" font-family="sans-serif" font-weight="bold" '
                             'text-anchor="middle" fill="#0b3d5c">→ 1</text><text id="e4" x="70" y="240" font-size="40" '
                             'font-family="sans-serif" font-weight="bold" text-anchor="middle" fill="#0b3d5c">B</text><g id="e5"><circle '
                             'cx="190" cy="238" r="30" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><line x1="190" y1="208" x2="195" '
                             'y2="196" stroke="#7a4a1d" stroke-width="4"/><ellipse cx="201" cy="201" rx="8" ry="4" fill="#40c057" '
                             'stroke="#0b3d5c" stroke-width="2"/></g><g id="e6"><circle cx="270" cy="238" r="30" fill="#e03131" '
                             'stroke="#0b3d5c" stroke-width="3"/><line x1="270" y1="208" x2="275" y2="196" stroke="#7a4a1d" '
                             'stroke-width="4"/><ellipse cx="281" cy="201" rx="8" ry="4" fill="#40c057" stroke="#0b3d5c" '
                             'stroke-width="2"/></g><text id="e7" x="450" y="250" font-size="56" font-family="sans-serif" '
                             'font-weight="bold" text-anchor="middle" fill="#0b3d5c">→ 2</text><text id="e8" x="70" y="370" font-size="40" '
                             'font-family="sans-serif" font-weight="bold" text-anchor="middle" fill="#0b3d5c">C</text><circle id="e9" '
                             'cx="170" cy="360" r="28" fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/><circle id="e10" cx="250" '
                             'cy="360" r="28" fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/><circle id="e11" cx="330" cy="360" r="28" '
                             'fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/><text id="e12" x="450" y="380" font-size="56" '
                             'font-family="sans-serif" font-weight="bold" text-anchor="middle" fill="#0b3d5c">→ 3</text>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10', 'e11', 'e12']}},
            {'k': 't',
             'en': 'Group A: how many stars? One. So the number is 1.',
             'ar': 'المجموعة A: كم نجمة؟ واحدة. إذن الرقم 1.',
             'fr': "Groupe A : combien d'étoiles ? Une. Le nombre est 1.",
             'label': None},
            {'k': 't',
             'en': 'Group B: count the apples: one, two. So the number is 2.',
             'ar': 'المجموعة B: عدّ التفاح: one، two. إذن الرقم 2.',
             'fr': 'Groupe B : compte les pommes : one, two. Le nombre est 2.',
             'label': None},
            {'k': 't',
             'en': 'Group C: count the circles: one, two, three. So the number is 3.',
             'ar': 'المجموعة C: عدّ الدوائر: one، two، three. إذن الرقم 3.',
             'fr': 'Groupe C : compte les cercles : one, two, three. Le nombre est 3.',
             'label': None},
            {'k': 'f', 'f': '⭐ → 1      🍎 🍎 → 2      🔵 🔵 🔵 → 3'},
            {'k': 't',
             'en': 'Each numeral must match its quantity.',
             'ar': 'يجب أن يطابق كل رقم كميته.',
             'fr': 'Chaque chiffre doit correspondre à sa quantité.',
             'label': None}]},
 {'n': '4',
  'page': '17',
  'stmt': ('A number appears. Show that many objects: 1, then 2, then 3.',
           'يظهر رقم. أظهر بالعدد نفسه من الأشياء: 1 ثم 2 ثم 3.',
           "Un nombre apparaît. Montre autant d'objets : 1, puis 2, puis 3."),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<text id="e1" x="90" y="120" font-size="70" font-family="sans-serif" font-weight="bold" text-anchor="middle" '
                             'fill="#0b3d5c">1</text><rect id="e2" x="272" y="82" width="56" height="56" fill="#e03131" stroke="#0b3d5c" '
                             'stroke-width="3"/><text id="e3" x="90" y="250" font-size="70" font-family="sans-serif" font-weight="bold" '
                             'text-anchor="middle" fill="#0b3d5c">2</text><rect id="e4" x="227" y="212" width="56" height="56" '
                             'fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><rect id="e5" x="317" y="212" width="56" height="56" '
                             'fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><text id="e6" x="90" y="380" font-size="70" '
                             'font-family="sans-serif" font-weight="bold" text-anchor="middle" fill="#0b3d5c">3</text><rect id="e7" '
                             'x="182" y="342" width="56" height="56" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><rect id="e8" '
                             'x="272" y="342" width="56" height="56" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><rect id="e9" '
                             'x="362" y="342" width="56" height="56" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9']}},
            {'k': 't',
             'en': 'Show me 1: one object. Check: one.',
             'ar': 'أظهر 1: شيء واحد. تحقّق: one.',
             'fr': 'Montre-moi 1 : un objet. Vérifie : one.',
             'label': None},
            {'k': 't',
             'en': 'Show me 2: two objects. Check: one, two.',
             'ar': 'أظهر 2: شيئان. تحقّق: one، two.',
             'fr': 'Montre-moi 2 : deux objets. Vérifie : one, two.',
             'label': None},
            {'k': 't',
             'en': 'Show me 3: three objects. Check: one, two, three.',
             'ar': 'أظهر 3: ثلاثة أشياء. تحقّق: one، two، three.',
             'fr': 'Montre-moi 3 : trois objets. Vérifie : one, two, three.',
             'label': None},
            {'k': 't',
             'en': 'You moved from the numeral to the quantity.',
             'ar': 'انتقلت من الرقم إلى الكمية.',
             'fr': 'Tu es passé du chiffre à la quantité.',
             'label': None}]},
 {'n': '5',
  'page': '17',
  'stmt': ('Find the mistake: three strawberries have the number 2 under them.',
           'جد الخطأ: ثلاث فراولات وتحتها الرقم 2.',
           "Trouve l'erreur : trois fraises et le nombre 2 en dessous."),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<g id="e1"><polygon points="158,125 242,125 200,196" fill="#e03131" stroke="#0b3d5c" '
                             'stroke-width="3"/><polygon points="171,125 200,104 229,125" fill="#40c057" stroke="#0b3d5c" '
                             'stroke-width="3"/></g><g id="e2"><polygon points="288,125 372,125 330,196" fill="#e03131" stroke="#0b3d5c" '
                             'stroke-width="3"/><polygon points="301,125 330,104 359,125" fill="#40c057" stroke="#0b3d5c" '
                             'stroke-width="3"/></g><g id="e3"><polygon points="418,125 502,125 460,196" fill="#e03131" stroke="#0b3d5c" '
                             'stroke-width="3"/><polygon points="431,125 460,104 489,125" fill="#40c057" stroke="#0b3d5c" '
                             'stroke-width="3"/></g><text id="e4" x="330" y="330" font-size="110" font-family="sans-serif" '
                             'font-weight="bold" text-anchor="middle" fill="#0b3d5c">2</text>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4']}},
            {'k': 't',
             'en': 'Count the strawberries: one, two, three. There are 3.',
             'ar': 'عدّ الفراولة: one، two، three. عددها 3.',
             'fr': 'Compte les fraises : one, two, three. Il y en a 3.',
             'label': None},
            {'k': 't',
             'en': 'Which number is written? 2. Does 2 match 3 strawberries? No.',
             'ar': 'ما الرقم المكتوب؟ 2. هل يطابق 2 ثلاث فراولات؟ لا.',
             'fr': 'Quel nombre est écrit ? 2. Est-ce que 2 correspond à 3 fraises ? Non.',
             'label': None},
            {'k': 't', 'en': 'So we change the 2 into a 3.', 'ar': 'إذن نبدّل 2 إلى 3.', 'fr': 'On change donc le 2 en 3.', 'label': None},
            {'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<g id="e1"><polygon points="158,125 242,125 200,196" fill="#e03131" stroke="#0b3d5c" '
                             'stroke-width="3"/><polygon points="171,125 200,104 229,125" fill="#40c057" stroke="#0b3d5c" '
                             'stroke-width="3"/></g><g id="e2"><polygon points="288,125 372,125 330,196" fill="#e03131" stroke="#0b3d5c" '
                             'stroke-width="3"/><polygon points="301,125 330,104 359,125" fill="#40c057" stroke="#0b3d5c" '
                             'stroke-width="3"/></g><g id="e3"><polygon points="418,125 502,125 460,196" fill="#e03131" stroke="#0b3d5c" '
                             'stroke-width="3"/><polygon points="431,125 460,104 489,125" fill="#40c057" stroke="#0b3d5c" '
                             'stroke-width="3"/></g><text id="e4" x="330" y="330" font-size="110" font-family="sans-serif" '
                             'font-weight="bold" text-anchor="middle" fill="#0b3d5c">3</text>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4']}},
            {'k': 'f', 'f': '🍓 🍓 🍓 → 3'},
            {'k': 't',
             'en': 'You did not only find the answer, you found why it was wrong.',
             'ar': 'لم تجد الجواب فقط، بل عرفت لماذا كان خاطئًا.',
             'fr': "Tu n'as pas seulement trouvé la réponse, tu as compris pourquoi c'était faux.",
             'label': None}]},
 {'n': '6',
  'page': '17',
  'stmt': ('Mixed practice. 1) Two fish: how many? 2) Build 3 cubes. 3) One flower: how many, say it in English. 4) Three dots move to '
           'another shape: did the number change?',
           'تمارين مختلطة. 1) سمكتان: كم سمكة؟ 2) ابنِ 3 مكعبات. 3) زهرة واحدة: كم زهرة؟ قلها بالإنكليزية. 4) تتحرّك ثلاث نقاط إلى شكل '
           'آخر: هل تغيّر العدد؟',
           'Exercices variés. 1) Deux poissons : combien ? 2) Construis 3 cubes. 3) Une fleur : combien ? Dis-le en anglais. 4) Trois '
           'points bougent vers une autre forme : le nombre a-t-il changé ?'),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<g id="e1"><polygon points="276,200 308,173 308,227" fill="#ff922b" stroke="#0b3d5c" '
                             'stroke-width="3"/><ellipse cx="240" cy="200" rx="45" ry="27" fill="#ffa94d" stroke="#0b3d5c" '
                             'stroke-width="3"/><circle cx="218" cy="197" r="3" fill="#0b3d5c"/></g><g id="e2"><polygon points="456,200 '
                             '488,173 488,227" fill="#ff922b" stroke="#0b3d5c" stroke-width="3"/><ellipse cx="420" cy="200" rx="45" '
                             'ry="27" fill="#ffa94d" stroke="#0b3d5c" stroke-width="3"/><circle cx="398" cy="197" r="3" '
                             'fill="#0b3d5c"/></g>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2']}},
            {'k': 't',
             'en': 'Question 1: count the fish: one, two. So 2, and we choose the numeral 2.',
             'ar': 'السؤال 1: عدّ السمك: one، two. إذن 2، ونختار الرقم 2.',
             'fr': 'Question 1 : compte les poissons : one, two. Donc 2, et on choisit le chiffre 2.',
             'label': None},
            {'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<rect id="e1" x="170" y="160" width="80" height="80" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><rect '
                             'id="e2" x="290" y="160" width="80" height="80" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><rect '
                             'id="e3" x="410" y="160" width="80" height="80" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3']}},
            {'k': 't',
             'en': 'Question 2: the number is 3, so we build three cubes. Check: one, two, three.',
             'ar': 'السؤال 2: الرقم 3، إذن نبني ثلاثة مكعبات. تحقّق: one، two، three.',
             'fr': 'Question 2 : le nombre est 3, on construit donc trois cubes. Vérifie : one, two, three.',
             'label': None},
            {'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<g id="e1"><circle cx="366" cy="200" r="27" fill="#f783ac" stroke="#0b3d5c" stroke-width="2"/><circle '
                             'cx="341" cy="234" r="27" fill="#f783ac" stroke="#0b3d5c" stroke-width="2"/><circle cx="301" cy="221" r="27" '
                             'fill="#f783ac" stroke="#0b3d5c" stroke-width="2"/><circle cx="301" cy="179" r="27" fill="#f783ac" '
                             'stroke="#0b3d5c" stroke-width="2"/><circle cx="341" cy="166" r="27" fill="#f783ac" stroke="#0b3d5c" '
                             'stroke-width="2"/><circle cx="330" cy="200" r="21" fill="#ffd43b" stroke="#0b3d5c" stroke-width="2"/></g>',
                      'vb': [660, 440],
                      'show': ['e1']}},
            {'k': 't',
             'en': 'Question 3: one flower. In English: one.',
             'ar': 'السؤال 3: زهرة واحدة. بالإنكليزية: one.',
             'fr': 'Question 3 : une fleur. En anglais : one.',
             'label': None},
            {'k': 'f', 'f': '🌼 → 1 → one'},
            {'k': 't',
             'en': 'Question 4: three dots moved to another shape. No, the number did not change. It is still 3, because we did not add a '
                   'dot and we did not take one away.',
             'ar': 'السؤال 4: انتقلت ثلاث نقاط إلى شكل آخر. لا، لم يتغيّر العدد. ما زال 3 لأننا لم نضف نقطة ولم نأخذ نقطة.',
             'fr': "Question 4 : trois points ont bougé vers une autre forme. Non, le nombre n'a pas changé. C'est toujours 3, car on n'a "
                   'ni ajouté ni retiré de point.',
             'label': None}]},
 {'n': '7',
  'page': '17',
  'stmt': ('Put the boxes in order from the fewest to the most: Box A has 1 apple, Box B has 3 apples, Box C has 2 apples.',
           'رتّب الصناديق من الأقل إلى الأكثر: الصندوق A فيه تفاحة، الصندوق B فيه 3 تفاحات، الصندوق C فيه تفاحتان.',
           'Range les boîtes du plus petit nombre au plus grand : la boîte A a 1 pomme, la B a 3 pommes, la C a 2 pommes.'),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<rect id="e1" x="40" y="60" width="170" height="120" rx="10" fill="none" stroke="#0b3d5c" '
                             'stroke-width="4"/><text id="e2" x="125" y="50" font-size="34" font-family="sans-serif" font-weight="bold" '
                             'text-anchor="middle" fill="#0b3d5c">A</text><g id="e3"><circle cx="125" cy="123" r="28" fill="#e03131" '
                             'stroke="#0b3d5c" stroke-width="3"/><line x1="125" y1="95" x2="130" y2="83" stroke="#7a4a1d" '
                             'stroke-width="4"/><ellipse cx="136" cy="88" rx="8" ry="4" fill="#40c057" stroke="#0b3d5c" '
                             'stroke-width="2"/></g><rect id="e4" x="245" y="60" width="170" height="120" rx="10" fill="none" '
                             'stroke="#0b3d5c" stroke-width="4"/><text id="e5" x="330" y="50" font-size="34" font-family="sans-serif" '
                             'font-weight="bold" text-anchor="middle" fill="#0b3d5c">B</text><g id="e6"><circle cx="282" cy="123" r="20" '
                             'fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><line x1="282" y1="103" x2="287" y2="91" stroke="#7a4a1d" '
                             'stroke-width="4"/><ellipse cx="293" cy="96" rx="8" ry="4" fill="#40c057" stroke="#0b3d5c" '
                             'stroke-width="2"/></g><g id="e7"><circle cx="330" cy="123" r="20" fill="#e03131" stroke="#0b3d5c" '
                             'stroke-width="3"/><line x1="330" y1="103" x2="335" y2="91" stroke="#7a4a1d" stroke-width="4"/><ellipse '
                             'cx="341" cy="96" rx="8" ry="4" fill="#40c057" stroke="#0b3d5c" stroke-width="2"/></g><g id="e8"><circle '
                             'cx="378" cy="123" r="20" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><line x1="378" y1="103" x2="383" '
                             'y2="91" stroke="#7a4a1d" stroke-width="4"/><ellipse cx="389" cy="96" rx="8" ry="4" fill="#40c057" '
                             'stroke="#0b3d5c" stroke-width="2"/></g><rect id="e9" x="450" y="60" width="170" height="120" rx="10" '
                             'fill="none" stroke="#0b3d5c" stroke-width="4"/><text id="e10" x="535" y="50" font-size="34" '
                             'font-family="sans-serif" font-weight="bold" text-anchor="middle" fill="#0b3d5c">C</text><g id="e11"><circle '
                             'cx="505" cy="123" r="24" fill="#e03131" stroke="#0b3d5c" stroke-width="3"/><line x1="505" y1="99" x2="510" '
                             'y2="87" stroke="#7a4a1d" stroke-width="4"/><ellipse cx="516" cy="92" rx="8" ry="4" fill="#40c057" '
                             'stroke="#0b3d5c" stroke-width="2"/></g><g id="e12"><circle cx="565" cy="123" r="24" fill="#e03131" '
                             'stroke="#0b3d5c" stroke-width="3"/><line x1="565" y1="99" x2="570" y2="87" stroke="#7a4a1d" '
                             'stroke-width="4"/><ellipse cx="576" cy="92" rx="8" ry="4" fill="#40c057" stroke="#0b3d5c" '
                             'stroke-width="2"/></g>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10', 'e11', 'e12']}},
            {'k': 't',
             'en': 'Count each box on its own. A: one. B: one, two, three. C: one, two.',
             'ar': 'عدّ كل صندوق وحده. A: one. B: one، two، three. C: one، two.',
             'fr': 'Compte chaque boîte seule. A : one. B : one, two, three. C : one, two.',
             'label': None},
            {'k': 't',
             'en': 'Who has the fewest? A, with 1. Next? C, with 2. And the most? B, with 3.',
             'ar': 'من عنده الأقل؟ A ومعه 1. بعده؟ C ومعه 2. والأكثر؟ B ومعه 3.',
             'fr': 'Qui en a le moins ? A, avec 1. Ensuite ? C, avec 2. Et le plus ? B, avec 3.',
             'label': None},
            {'k': 'f', 'f': 'A → C → B'},
            {'k': 'f', 'f': '1 → 2 → 3'},
            {'k': 't',
             'en': 'You used the meaning of the numbers, not only their shape.',
             'ar': 'استعملت معنى الأعداد وليس شكلها فقط.',
             'fr': 'Tu as utilisé le sens des nombres, pas seulement leur forme.',
             'label': None}]},
 {'n': '8',
  'page': '17',
  'stmt': ('Final challenge. 1) Count 3 things. 2) Match a group of 1 and a group of 2 with their numbers. 3) Build a collection of 2. 4) '
           'Read 1, 3, 2. 5) Two stars have the number 3 under them: right or wrong?',
           'التحدي الأخير. 1) عدّ 3 أشياء. 2) صِل مجموعة فيها 1 ومجموعة فيها 2 برقميهما. 3) ابنِ مجموعة فيها 2. 4) اقرأ 1 و3 و2. 5) نجمتان '
           'وتحتهما الرقم 3: صح أم خطأ؟',
           'Défi final. 1) Compte 3 objets. 2) Relie un groupe de 1 et un groupe de 2 à leurs nombres. 3) Construis une collection de 2. '
           '4) Lis 1, 3, 2. 5) Deux étoiles avec le nombre 3 en dessous : juste ou faux ?'),
  'steps': [{'k': 'd',
             'draw': 'svgScene',
             'args': {'svg': '<circle id="e1" cx="210" cy="200" r="40" fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/><circle id="e2" '
                             'cx="330" cy="200" r="40" fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/><circle id="e3" cx="450" cy="200" '
                             'r="40" fill="#4dabf7" stroke="#0b3d5c" stroke-width="3"/>',
                      'vb': [660, 440],
                      'show': ['e1', 'e2', 'e3']}},
            {'k': 't',
             'en': 'Task 1: touch each object once: one, two, three. There are 3.',
             'ar': 'المهمة 1: المس كل شيء مرة: one، two، three. العدد 3.',
             'fr': 'Tâche 1 : touche chaque objet une fois : one, two, three. Il y en a 3.',
             'label': None},
            {'k': 'f', 'f': '● ● ● → 3'},
            {'k': 't',
             'en': 'Task 2: one object goes with 1. Two objects go with 2.',
             'ar': 'المهمة 2: شيء واحد مع 1. وشيئان مع 2.',
             'fr': 'Tâche 2 : un objet va avec 1. Deux objets vont avec 2.',
             'label': None},
            {'k': 'f', 'f': '● → 1      ● ● → 2'},
            {'k': 't',
             'en': 'Task 3: the number is 2, so we build two objects. Check: one, two.',
             'ar': 'المهمة 3: الرقم 2، إذن نبني شيئين. تحقّق: one، two.',
             'fr': 'Tâche 3 : le nombre est 2, on construit donc deux objets. Vérifie : one, two.',
             'label': None},
            {'k': 't',
             'en': 'Task 4: read the numbers: one, three, two.',
             'ar': 'المهمة 4: اقرأ الأرقام: one، three، two.',
             'fr': 'Tâche 4 : lis les nombres : one, three, two.',
             'label': None},
            {'k': 'f', 'f': '1   3   2'},
            {'k': 't',
             'en': 'Task 5: two stars and the number 3. Count: one, two. The number must be 2. So it is wrong, and the right numeral is 2.',
             'ar': 'المهمة 5: نجمتان والرقم 3. عدّ: one، two. يجب أن يكون الرقم 2. إذن هذا خطأ، والرقم الصحيح هو 2.',
             'fr': "Tâche 5 : deux étoiles et le nombre 3. Compte : one, two. Le nombre doit être 2. C'est donc faux, et le bon chiffre "
                   'est 2.',
             'label': None},
            {'k': 'f', 'f': '⭐ ⭐ → 2'}]}]


def scenes():
    return make_scenes(THEORY, EXERCISES)
