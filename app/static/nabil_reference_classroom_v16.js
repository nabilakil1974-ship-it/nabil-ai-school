/* NABIL Reference Classroom v16 — Golden Reference Cards
 *
 * الهدف:
 * 1. يستقبل نص الدرس الكامل كما هو.
 * 2. لا يحذف الشرح ولا يختصره.
 * 3. يقسم الدرس بحسب عناوينه وأفكاره إلى بطاقات.
 * 4. يحافظ على ترتيب محتوى الدرس.
 * 5. يضع المختبر الموثق تحت موضعه.
 * 6. ينشئ بطاقة ختامية من محتوى الدرس نفسه فقط.
 * 7. لا يولد أي معلومة علمية جديدة.
 */

(()=>{
'use strict';


/* =========================================================
   BASIC HELPERS
========================================================= */

const esc=v=>String(v??'').replace(
  /[&<>"']/g,
  c=>({
    '&':'&amp;',
    '<':'&lt;',
    '>':'&gt;',
    '"':'&quot;',
    "'":'&#39;'
  }[c])
);


const ar=v=>
  /[\u0600-\u06ff]/.test(
    String(v||'')
  );


/* =========================================================
   CARD ROLES
========================================================= */

const roles=[

  [
    'prerequisite',
    /prereq|متطلبات/i,
    '🧭'
  ],

  [
    'hook',
    /hook|مدخل|تهيئة/i,
    '✨'
  ],

  [
    'discover',
    /discover|اكتشف|لاحظ|think|فكّر/i,
    '🔎'
  ],

  [
    'concept',
    /explain|concept|شرح|الفكرة|why|لماذا/i,
    '📘'
  ],

  [
    'rule',
    /rule|definition|theorem|property|قاعدة|تعريف|نظرية|خاصية/i,
    '📐'
  ],

  [
    'example',
    /worked example|example|مثال/i,
    '🧩'
  ],

  [
    'solution',
    /solution|الحل|answer|جواب/i,
    '✅'
  ],

  [
    'check',
    /checkpoint|check|تحقق|سؤال/i,
    '🎯'
  ],

  [
    'practice',
    /practice|exercise|student try|your turn|تمرين|تمارين|دورك|تطبيق/i,
    '✍️'
  ],

  [
    'assessment',
    /assessment|تقييم|challenge|تحدي/i,
    '🏁'
  ],

  [
    'visual',
    /visual|diagram|figure|graph|رسم|شاهد/i,
    '📊'
  ],

  [
    'lab',
    /\bLAB-\d+\b|FINAL MASTER LAB|experiment|lab|manipulat|مختبر|تجربة/i,
    '🧪'
  ],

  [
    'summary',
    /golden card|visual summary|summary|synthesis|الخلاصة|البطاقة|تركيب/i,
    '🌟'
  ]

];


function role(title){

  for(const [r,re,icon] of roles){

    if(
      re.test(
        String(title||'')
      )
    ){

      return {
        r,
        icon
      };

    }

  }

  return {
    r:'concept',
    icon:'📘'
  };

}


/* =========================================================
   HEADING DETECTION
========================================================= */

function isHeading(line){

  const x=
    String(line||'').trim();

  if(!x)
    return false;


  if(
    /^#{1,6}\s+/.test(x)
  )
    return true;


  const clean=
    x
      .replace(
        /^#{1,6}\s*/,
        ''
      )
      .trim();


  return (
    clean.length<=140
    &&
    roles.some(
      ([,re])=>re.test(clean)
    )
  );

}


/* =========================================================
   SUMMARY HELPERS
========================================================= */

function meaningful(lines){

  return (
    lines||[]
  )
  .map(
    x=>String(x||'').trim()
  )
  .filter(Boolean);

}


/*
  البطاقة النهائية لا تستخدم AI.

  نأخذ فقط جملاً موجودة بالفعل
  داخل الدرس المستدعى.

  لا نضيف حقيقة جديدة.
*/

function summaryFrom(sections){

  const seen=
    new Set();

  const items=[];


  for(const c of sections){


    /*
      لا نستخدم نصوص المختبر
      أو التمارين كأساس للخلاصة.
    */

    if(
      c.r==='lab'
      ||
      c.r==='practice'
      ||
      c.r==='assessment'
    )
      continue;


    for(
      const line
      of meaningful(c.lines)
    ){

      const clean=
        line
          .replace(
            /^[-•]\s*/,
            ''
          )
          .replace(
            /\s+/g,
            ' '
          )
          .trim();


      if(
        !clean
        ||
        clean.length<8
        ||
        clean.length>260
      )
        continue;


      const key=
        clean.toLowerCase();


      if(
        seen.has(key)
      )
        continue;


      seen.add(key);

      items.push(clean);


      if(
        items.length>=6
      )
        return items;

    }

  }


  return items;

}


/* =========================================================
   LESSON PARSER
========================================================= */

/*
  هنا يتم تحويل الدرس الكامل
  إلى بطاقات.

  لا نغير ترتيب الدرس.

  لا نحذف النص.

  العنوان الموجود في الدرس
  يبدأ بطاقة جديدة.
*/

function parse(text){

  const raw=
    String(text||'')
      .replace(
        /\r/g,
        ''
      );


  const lines=
    raw.split('\n');


  const sections=[];


  let current={
    title:'',
    lines:[]
  };


  const push=()=>{

    if(
      current.title
      ||
      current.lines.some(
        x=>x.trim()
      )
    ){

      const rr=
        role(
          current.title
        );


      sections.push({

        ...current,

        ...rr,

        index:
          sections.length

      });

    }


    current={
      title:'',
      lines:[]
    };

  };


  for(
    const original
    of lines
  ){

    const x=
      original.trim();


    if(!x){

      if(
        current.lines.length
        &&
        current.lines[
          current.lines.length-1
        ]!==''
      ){

        current.lines.push('');

      }

      continue;

    }


    if(
      isHeading(x)
    ){

      push();


      current.title=
        x
          .replace(
            /^#{1,6}\s*/,
            ''
          )
          .trim();

    }

    else{

      current.lines.push(
        original
      );

    }

  }


  push();


  /*
    إذا وصل نص بدون عناوين
    لا نخترع محتوى.

    نضع النص كاملًا
    في بطاقة شرح واحدة.
  */

  if(
    !sections.length
  ){

    sections.push({

      title:'',

      lines:[
        raw
      ],

      r:'concept',

      icon:'📘',

      index:0

    });

  }


  /*
    هل يحتوي الدرس أصلًا
    على Golden Card؟
  */

  const hasSummary=
    sections.some(
      c=>c.r==='summary'
    );


  /*
    إذا لم توجد بطاقة ختامية،
    نبنيها من نص الدرس نفسه.
  */

  if(
    !hasSummary
  ){

    const facts=
      summaryFrom(
        sections
      );


    if(
      facts.length
    ){

      sections.push({

        title:
          ar(raw)
          ?
          'البطاقة الختامية — خلاصة الدرس'
          :
          'Golden Final Card — Lesson Summary',

        lines:facts,

        r:'summary',

        icon:'🌟',

        index:
          sections.length,

        generatedSummary:true

      });

    }

  }


  return sections;

}


/* =========================================================
   DESIGN
========================================================= */

const CSS=`

:root{

  --bg:#04111f;

  --panel:#081d31;

  --card:#0a2238;

  --card2:#071a2c;

  --line:#315f82;

  --cyan:#67e8ff;

  --gold:#ffd36a;

  --txt:#f7fbff;

  --muted:#bfd4e4;

}


*{
  box-sizing:border-box;
}


html,
body{

  margin:0;

  background:
    var(--bg);

  color:
    var(--txt);

  font-family:
    system-ui,
    -apple-system,
    "Segoe UI",
    Tahoma,
    Arial,
    sans-serif;

}


.nrc{

  min-height:
    100vh;

  padding:
    18px;

}


.nrc-wrap{

  width:
    min(
      1180px,
      100%
    );

  margin:
    0 auto;

}


.nrc-title{

  text-align:
    center;

  color:
    var(--cyan);

  font-size:
    clamp(
      28px,
      4vw,
      46px
    );

  margin:
    16px 0 32px;

}


/* =========================================================
   LESSON AREA
========================================================= */

.nrc-lesson{

  width:
    100%;

}


/* =========================================================
   REFERENCE CARD
========================================================= */

.nrc-section{

  position:
    relative;

  width:
    100%;

  padding:
    clamp(
      20px,
      3vw,
      32px
    );

  margin:
    0 0 24px;

  border:
    1px solid
    var(--line);

  border-radius:
    20px;

  background:

    linear-gradient(
      180deg,
      var(--card) 0%,
      var(--card2) 100%
    );

  box-shadow:

    0 14px 32px
    #0004;

  overflow:
    hidden;

}


/*
  الشريط الجانبي المضيء
*/

.nrc-section::before{

  content:"";

  position:
    absolute;

  top:0;

  bottom:0;

  left:0;

  width:
    5px;

  background:
    var(--cyan);

  box-shadow:
    0 0 18px
    #67e8ff88;

}


/* =========================================================
   CARD HEADER
========================================================= */

.nrc-head{

  display:
    flex;

  gap:
    12px;

  align-items:
    center;

  margin:
    0 0 20px;

}


.nrc-icon{

  display:
    grid;

  place-items:
    center;

  flex:
    0 0 auto;

  width:
    46px;

  height:
    46px;

  border-radius:
    14px;

  background:
    #ffffff0c;

  border:
    1px solid
    #ffffff16;

  font-size:
    27px;

}


.nrc-head h2{

  margin:
    0;

  color:
    #a8efff;

  font-size:
    clamp(
      22px,
      3vw,
      31px
    );

  line-height:
    1.3;

}


/* =========================================================
   TEXT
========================================================= */

.nrc-line{

  font-size:
    clamp(
      18px,
      1.8vw,
      22px
    );

  line-height:
    2;

  margin:
    0 0 16px;

  white-space:
    pre-wrap;

  overflow-wrap:
    anywhere;

}


.nrc-line:last-child{

  margin-bottom:
    0;

}


.nrc-spacer{

  height:
    10px;

}


/* =========================================================
   ROLE DIFFERENCES
========================================================= */

.nrc-section[
  data-role="rule"
]::before{

  background:
    #7dd3fc;

}


.nrc-section[
  data-role="example"
]::before,

.nrc-section[
  data-role="solution"
]::before,

.nrc-section[
  data-role="check"
]::before{

  background:
    var(--gold);

  box-shadow:
    0 0 18px
    #ffd36a88;

}


.nrc-section[
  data-role="practice"
]::before{

  background:
    #c4b5fd;

}


.nrc-section[
  data-role="assessment"
]::before{

  background:
    #fb7185;

}


/* =========================================================
   LAB CARD
========================================================= */

.nrc-section[
  data-role="lab"
]{

  border-color:
    #4a7c9d;

  background:

    linear-gradient(
      180deg,
      #08243a 0%,
      #061725 100%
    );

}


.nrc-section[
  data-role="lab"
]::before{

  background:
    #5eead4;

  box-shadow:
    0 0 20px
    #5eead488;

}


/* =========================================================
   LAB SLOT
========================================================= */

.nrc-lab-slot{

  margin:
    24px 0 4px;

  border:
    1px solid
    #315f82;

  border-radius:
    16px;

  padding:
    12px;

  background:
    #061725;

  overflow:
    hidden;

}


.nrc-lab-slot > strong{

  display:
    block;

  color:
    var(--gold);

  font-size:
    18px;

  margin:
    2px 4px 12px;

}


.nrc-lab-mount{

  width:
    100%;

  min-height:
    90px;

}


.nrc-lab-frame{

  width:
    100%;

  min-height:
    720px;

  border:
    0;

  border-radius:
    12px;

  background:
    #020812;

  display:
    block;

}


.nrc-note{

  color:
    var(--muted);

  line-height:
    1.8;

  padding:
    12px;

}


/* =========================================================
   GOLDEN FINAL CARD
========================================================= */

.nrc-section[
  data-role="summary"
]{

  border:
    2px solid
    var(--gold);

  background:

    radial-gradient(
      circle at top right,
      #ffd36a20 0,
      transparent 38%
    ),

    linear-gradient(
      180deg,
      #10273a 0%,
      #091a29 100%
    );

  box-shadow:

    0 18px 42px
    #0006,

    0 0 30px
    #ffd36a18;

}


.nrc-section[
  data-role="summary"
]::before{

  width:
    7px;

  background:
    var(--gold);

  box-shadow:
    0 0 24px
    #ffd36aaa;

}


.nrc-section[
  data-role="summary"
]
.nrc-icon{

  background:
    #ffd36a18;

  border-color:
    #ffd36a44;

}


.nrc-section[
  data-role="summary"
]
.nrc-head h2{

  color:
    var(--gold);

}


.nrc-section[
  data-role="summary"
]
.nrc-line{

  position:
    relative;

  padding-inline-start:
    30px;

  font-weight:
    600;

}


.nrc-section[
  data-role="summary"
]
.nrc-line::before{

  content:
    "✓";

  position:
    absolute;

  inset-inline-start:
    0;

  color:
    var(--gold);

  font-weight:
    900;

}


/* =========================================================
   MOBILE
========================================================= */

@media(
  max-width:700px
){

  .nrc{

    padding:
      6px;

  }


  .nrc-title{

    margin:
      14px 8px 22px;

    font-size:
      29px;

  }


  .nrc-section{

    padding:
      17px 14px;

    border-radius:
      15px;

    margin-bottom:
      16px;

  }


  .nrc-head{

    gap:
      9px;

    margin-bottom:
      15px;

  }


  .nrc-icon{

    width:
      39px;

    height:
      39px;

    border-radius:
      11px;

    font-size:
      23px;

  }


  .nrc-head h2{

    font-size:
      22px;

  }


  .nrc-line{

    font-size:
      18px;

    line-height:
      1.9;

  }


  .nrc-lab-slot{

    padding:
      6px;

    margin-inline:
      -4px;

  }


  .nrc-lab-frame{

    min-height:
      680px;

  }

}

`;


/* =========================================================
   CARD MARKUP
========================================================= */

function sectionMarkup(
  c,
  i
){

  const heading=

    c.title

    ?

    `
    <div class="nrc-head">

      <span
        class="nrc-icon"
      >
        ${c.icon}
      </span>

      <h2>
        ${esc(c.title)}
      </h2>

    </div>
    `

    :

    '';


  const body=

    c.lines

      .map(

        x=>

          x.trim()

          ?

          `
          <p
            class="nrc-line"
            dir="${
              ar(x)
              ?
              'rtl'
              :
              'ltr'
            }"
          >
            ${esc(x)}
          </p>
          `

          :

          `
          <div
            class="nrc-spacer"
          ></div>
          `

      )

      .join('');


  /*
    المختبر لا يُولد هنا.

    إذا كانت البطاقة نفسها
    قسم مختبر، نترك موضعًا
    للمختبر الموثق.
  */

  const lab=

    c.r==='lab'

    ?

    `
    <div
      class="nrc-lab-slot"
      data-lab-slot="${i}"
      data-lab-title="${
        esc(c.title)
      }"
    >

      <strong>

        🧪 ${
          esc(
            c.title
            ||
            'NABIL Smart Lab'
          )
        }

      </strong>

      <div
        class="nrc-lab-mount"
        data-lab-mount="${i}"
      ></div>

    </div>
    `

    :

    '';


  return `

    <section

      class="nrc-section"

      data-section="${i}"

      data-role="${
        esc(c.r)
      }"

    >

      ${heading}

      ${body}

      ${lab}

    </section>

  `;

}


/* =========================================================
   PAGE MARKUP
========================================================= */

function markup(
  text,
  title
){

  const sections=
    parse(text);


  return `

  <style>
    ${CSS}
  </style>


  <div
    class="nrc"
  >

    <main
      class="nrc-wrap"
    >


      <h1
        class="nrc-title"
      >

        ${esc(title)}

      </h1>


      <article
        class="nrc-lesson"
      >

        ${
          sections
            .map(
              sectionMarkup
            )
            .join('')
        }

      </article>


    </main>

  </div>

  `;

}


/* =========================================================
   VERIFIED LABS
========================================================= */

/*
  هذا الجزء لا يولد مختبرات.

  يستدعي فقط المختبرات
  الموثقة الموجودة أصلًا.
*/

async function mountVerifiedLabs(
  root,
  meta
){

  const mounts=[

    ...root.querySelectorAll(
      '[data-lab-mount]'
    )

  ];


  if(
    !mounts.length
  )
    return;


  const lessonId=

    String(
      meta.lesson_id||''
    )
    .trim();


  const language=

    String(
      meta.language||''
    )
    .trim();


  if(
    !lessonId
  )
    return;


  try{


    const listRes=

      await fetch(

        `/api/interactive-lessons/verified-labs?lesson_id=${
          encodeURIComponent(
            lessonId
          )
        }&language=${
          encodeURIComponent(
            language
          )
        }`,

        {
          cache:'no-store'
        }

      );


    const list=
      await listRes.json();


    const labs=

      Array.isArray(
        list.labs
      )

      ?

      list.labs

      :

      [];


    for(
      let i=0;
      i<mounts.length;
      i++
    ){


      const mount=
        mounts[i];


      const rec=
        labs[i];


      if(
        !rec?.lab_id
      ){

        mount.innerHTML=

          '<div class="nrc-note">المختبر الموثق غير متوفر لهذا الموضع.</div>';

        continue;

      }


      const res=

        await fetch(

          `/api/interactive-lessons/verified-lab?lesson_id=${
            encodeURIComponent(
              lessonId
            )
          }&lab_id=${
            encodeURIComponent(
              rec.lab_id
            )
          }&language=${
            encodeURIComponent(
              language
            )
          }`,

          {
            cache:'no-store'
          }

        );


      const data=
        await res.json();


      if(
        !data?.found
        ||
        !data?.verified
        ||
        !data?.html
      ){

        mount.innerHTML=

          '<div class="nrc-note">المختبر الموثق غير جاهز.</div>';

        continue;

      }


      const frame=

        document.createElement(
          'iframe'
        );


      frame.className=
        'nrc-lab-frame';


      frame.title=

        String(

          data.title
          ||
          rec.lab_id
          ||
          'NABIL Smart Lab'

        );


      frame.setAttribute(
        'loading',
        'lazy'
      );


      frame.setAttribute(
        'allow',
        'fullscreen'
      );


      /*
        HTML المختبر يبقى
        كما هو دون تعديل.
      */

      frame.srcdoc=

        String(
          data.html
        );


      mount.replaceChildren(
        frame
      );

    }


  }

  catch(err){


    console.error(
      'Verified labs load failed',
      err
    );


    mounts.forEach(

      m=>{

        m.innerHTML=

          '<div class="nrc-note">تعذر تحميل المختبر الموثق.</div>';

      }

    );

  }

}


/* =========================================================
   PUBLIC RENDERER
========================================================= */

window.NABILReferenceClassroomV16={


  mount(
    root,
    text,
    title,
    meta={}
  ){


    /*
      text هنا هو الدرس الكامل
      الذي وصل من السيرفر.
    */

    root.innerHTML=

      markup(
        text,
        title
      );


    root.dataset.lessonId=

      meta.lesson_id
      ||
      '';


    root.dataset.renderer=

      'reference-v16-cards';


    /*
      بعد بناء البطاقات،
      نحمّل المختبرات الموثقة
      في مواضعها فقط.
    */

    mountVerifiedLabs(
      root,
      meta
    );

  },


  parse


};


})();
