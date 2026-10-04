/* NABIL Reference Classroom v16 — Continuous Golden Lesson
 * صفحة Golden واحدة كاملة.
 * لا يغيّر توليد المختبرات أو التحقق منها.
 */
(()=>{'use strict';

const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({
  '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
}[c]));

const ar=v=>/[\u0600-\u06ff]/.test(String(v||''));

const roles=[
 ['prerequisite',/prereq|متطلبات/i,'🧭'],
 ['hook',/hook|مدخل|تهيئة/i,'✨'],
 ['discover',/discover|اكتشف|لاحظ|think|فكّر/i,'🔎'],
 ['concept',/explain|concept|شرح|الفكرة|why|لماذا/i,'📘'],
 ['rule',/rule|definition|theorem|property|قاعدة|تعريف|نظرية|خاصية/i,'📐'],
 ['example',/worked example|example|مثال/i,'🧩'],
 ['solution',/solution|الحل|answer|جواب/i,'✅'],
 ['check',/checkpoint|check|تحقق|سؤال/i,'🎯'],
 ['practice',/practice|exercise|student try|your turn|تمرين|تمارين|دورك|تطبيق/i,'✍️'],
 ['assessment',/assessment|تقييم|challenge|تحدي/i,'🏁'],
 ['visual',/visual|diagram|figure|graph|رسم|شاهد/i,'📊'],
 ['lab',/\bLAB-\d+\b|FINAL MASTER LAB|experiment|lab|manipulat|مختبر|تجربة/i,'🧪'],
 ['summary',/golden card|visual summary|summary|synthesis|الخلاصة|البطاقة|تركيب/i,'🌟']
];

function role(title){
  for(const [r,re,icon] of roles){
    if(re.test(String(title||''))) return {r,icon};
  }
  return {r:'concept',icon:'📘'};
}

function isHeading(line){
  const x=String(line||'').trim();

  if(!x) return false;

  if(/^#{1,6}\s+/.test(x)) return true;

  const clean=x.replace(/^#{1,6}\s*/,'').trim();

  return clean.length<=140 &&
    roles.some(([,re])=>re.test(clean));
}

/*
  مهم:
  لا نقطّع الشرح إلى بطاقات.
  لا نختصر النص.
  لا ننشئ "الفكرة الأولى".
  لا ننشئ بطاقة نهائية من عندنا.
  نحافظ على ترتيب النص الأصلي.
*/
function parse(text){

  const raw=String(text||'').replace(/\r/g,'');

  const lines=raw.split('\n');

  const sections=[];

  let current={
    title:'',
    lines:[]
  };

  const push=()=>{

    if(
      current.title ||
      current.lines.some(x=>x.trim())
    ){
      const rr=role(current.title);

      sections.push({
        ...current,
        ...rr,
        index:sections.length
      });
    }

    current={
      title:'',
      lines:[]
    };
  };

  for(const original of lines){

    const x=original.trim();

    if(!x){

      if(
        current.lines.length &&
        current.lines[current.lines.length-1]!==''
      ){
        current.lines.push('');
      }

      continue;
    }

    if(isHeading(x)){

      push();

      current.title=
        x.replace(/^#{1,6}\s*/,'').trim();

    }else{

      current.lines.push(original);

    }
  }

  push();

  if(!sections.length){

    sections.push({
      title:'',
      lines:[raw],
      r:'concept',
      icon:'📘',
      index:0
    });

  }

  return sections;
}


const CSS=`

:root{
  --bg:#04111f;
  --panel:#081d31;
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
  background:#04111f;
  color:var(--txt);
  font-family:
    system-ui,
    -apple-system,
    "Segoe UI",
    Tahoma,
    Arial,
    sans-serif;
}

.nrc{
  min-height:100vh;
  padding:18px;
}

.nrc-wrap{
  width:min(1180px,100%);
  margin:0 auto;
}

.nrc-title{
  text-align:center;
  color:var(--cyan);
  font-size:clamp(28px,4vw,46px);
  margin:16px 0 32px;
}

.nrc-lesson{
  background:var(--panel);
  border:1px solid var(--line);
  border-radius:18px;

  padding:
    clamp(20px,4vw,48px);

  box-shadow:
    0 18px 44px #0005;
}


/* كل فقرة تظهر بالتسلسل داخل نفس الصفحة */

.nrc-section{
  padding:0 0 28px;
  margin:0 0 28px;

  border-bottom:
    1px solid #ffffff18;
}

.nrc-section:last-child{
  border-bottom:0;
  margin-bottom:0;
}


/* عنوان الفكرة */

.nrc-head{
  display:flex;
  gap:10px;
  align-items:center;

  margin:
    0 0 18px;
}

.nrc-icon{
  font-size:27px;
}

.nrc-head h2{
  margin:0;

  color:#a8efff;

  font-size:
    clamp(22px,3vw,31px);
}


/* الشرح الكتابي */

.nrc-line{

  font-size:
    clamp(18px,1.8vw,22px);

  line-height:2;

  margin:
    0 0 16px;

  white-space:
    pre-wrap;

  overflow-wrap:
    anywhere;
}

.nrc-spacer{
  height:8px;
}


/* المختبر تحت الفكرة مباشرة */

.nrc-lab-slot{

  margin:
    26px 0 8px;

  border:
    1px solid #315f82;

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

  display:block;

  color:
    var(--gold);

  font-size:
    18px;

  margin:
    2px 4px 12px;
}

.nrc-lab-mount{

  width:100%;

  min-height:
    90px;
}

.nrc-lab-frame{

  width:100%;

  min-height:
    720px;

  border:0;

  border-radius:
    12px;

  background:
    #020812;

  display:block;
}

.nrc-note{

  color:
    var(--muted);

  line-height:
    1.8;

  padding:
    12px;
}


/* الهاتف */

@media(max-width:700px){

  .nrc{
    padding:5px;
  }

  .nrc-title{
    margin:
      14px 8px 22px;
  }

  .nrc-lesson{
    padding:15px;
    border-radius:10px;
  }

  .nrc-line{
    font-size:18px;
    line-height:1.9;
  }

  .nrc-lab-slot{
    padding:6px;
    margin-inline:-5px;
  }

  .nrc-lab-frame{
    min-height:680px;
  }

}
`;


function sectionMarkup(c,i){

  const heading=
    c.title
      ?
      `
      <div class="nrc-head">

        <span class="nrc-icon">
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
      .map(x=>

        x.trim()

        ?

        `
        <p
          class="nrc-line"
          dir="${ar(x)?'rtl':'ltr'}"
        >
          ${esc(x)}
        </p>
        `

        :

        `
        <div class="nrc-spacer"></div>
        `

      )
      .join('');


  const lab=
    c.r==='lab'

      ?

      `
      <div
        class="nrc-lab-slot"
        data-lab-slot="${i}"
        data-lab-title="${esc(c.title)}"
      >

        <strong>
          🧪 ${esc(c.title||'NABIL Smart Lab')}
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
      data-role="${c.r}"
    >

      ${heading}

      ${body}

      ${lab}

    </section>
  `;
}


function markup(text,title){

  const sections=
    parse(text);

  return `

  <style>
    ${CSS}
  </style>

  <div class="nrc">

    <main class="nrc-wrap">

      <h1 class="nrc-title">
        ${esc(title)}
      </h1>

      <article class="nrc-lesson">

        ${
          sections
            .map(sectionMarkup)
            .join('')
        }

      </article>

    </main>

  </div>

  `;
}


/*
  لا ننشئ مختبرًا هنا.

  نطلب فقط المختبرات المنشورة
  والموثقة الموجودة أصلًا.
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

  if(!mounts.length)
    return;


  const lessonId=
    String(
      meta.lesson_id||''
    ).trim();


  const language=
    String(
      meta.language||''
    ).trim();


  if(!lessonId)
    return;


  try{


    const listRes=
      await fetch(

        `/api/interactive-lessons/verified-labs?lesson_id=${
          encodeURIComponent(lessonId)
        }&language=${
          encodeURIComponent(language)
        }`,

        {
          cache:'no-store'
        }

      );


    const list=
      await listRes.json();


    const labs=
      Array.isArray(list.labs)
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


      if(!rec?.lab_id){

        mount.innerHTML=
          '<div class="nrc-note">المختبر الموثق غير متوفر لهذا الموضع.</div>';

        continue;

      }


      const res=
        await fetch(

          `/api/interactive-lessons/verified-lab?lesson_id=${
            encodeURIComponent(lessonId)
          }&lab_id=${
            encodeURIComponent(rec.lab_id)
          }&language=${
            encodeURIComponent(language)
          }`,

          {
            cache:'no-store'
          }

        );


      const data=
        await res.json();


      if(
        !data?.found ||
        !data?.verified ||
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
          data.title ||
          rec.lab_id ||
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
        نعرض HTML المختبر
        كما هو.

        لا نعدله.
      */

      frame.srcdoc=
        String(
          data.html
        );


      mount.replaceChildren(
        frame
      );

    }


  }catch(err){


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


window.NABILReferenceClassroomV16={

  mount(
    root,
    text,
    title,
    meta={}
  ){

    /*
      صفحة واحدة كاملة.
    */

    root.innerHTML=
      markup(
        text,
        title
      );


    root.dataset.lessonId=
      meta.lesson_id||'';


    root.dataset.renderer=
      'reference-v16-continuous';


    /*
      تحميل المختبرات الموجودة فقط.
    */

    mountVerifiedLabs(
      root,
      meta
    );

  },


  parse

};


})();
