/* NABIL Reference Classroom v16
 * Canonical Golden renderer for requirements 3, 4 and 6.
 * Requirement 5 (scientific lesson-aware lab behavior) is intentionally NOT implemented here.
 * This renderer never invents lesson facts: it only structures the already-audited Golden text.
 */
(()=>{'use strict';
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const ar=v=>/[\u0600-\u06ff]/.test(String(v||''));
const sentence=/[^.!?؟؛;:\n]+(?:[.!?؟؛;:]+|$)/g;
const roles=[
 ['prerequisite',/prereq|متطلبات/i,'🧭'],['hook',/hook|مدخل|تهيئة/i,'✨'],['discover',/discover|اكتشف|لاحظ|think|فكّر/i,'🔎'],
 ['concept',/explain|concept|شرح|الفكرة|why|لماذا/i,'📘'],['rule',/rule|definition|theorem|property|قاعدة|تعريف|نظرية|خاصية/i,'📐'],
 ['example',/worked example|example|مثال/i,'🧩'],['solution',/solution|الحل|answer|جواب/i,'✅'],['check',/checkpoint|check|تحقق|سؤال/i,'🎯'],
 ['practice',/practice|exercise|student try|your turn|تمرين|تمارين|دورك|تطبيق/i,'✍️'],['assessment',/assessment|تقييم|challenge|تحدي/i,'🏁'],
 ['visual',/visual|diagram|figure|graph|رسم|شاهد/i,'📊'],['lab',/experiment|lab|manipulat|مختبر|تجربة/i,'🧪'],
 ['summary',/golden card|visual summary|summary|synthesis|الخلاصة|البطاقة|تركيب/i,'🌟']
];
const heading=/^(?:#{1,6}\s*)?(.{1,100})$/;
function role(title){for(const [r,re,icon] of roles)if(re.test(title))return{r,icon};return{r:'concept',icon:'📘'}}
function split(text){return String(text||'').replace(/\r/g,'').split('\n').map(x=>x.trim()).filter(Boolean)}
function small(lines){const out=[];for(const line of lines){const p=(line.match(sentence)||[line]).map(x=>x.trim()).filter(Boolean);for(let i=0;i<p.length;i+=3)out.push(p.slice(i,i+3))}return out}
function isHeading(x){const s=x.replace(/^#{1,6}\s*/,'').trim();return /^#{1,6}\s/.test(x)||roles.some(([,re])=>re.test(s)&&s.length<100)}
function parse(text){const lines=split(text),cards=[];let cur=null;for(const x of lines){if(isHeading(x)){cur={title:x.replace(/^#{1,6}\s*/,''),lines:[]};cards.push(cur)}else{if(!cur){cur={title:ar(x)?'الفكرة الأولى':'First idea',lines:[]};cards.push(cur)}cur.lines.push(x)}}
 const normalized=[];for(const c of cards){const chunks=small(c.lines);if(!chunks.length){normalized.push({...c,lines:[]});continue}chunks.forEach((ls,i)=>normalized.push({title:i?`${c.title} · ${i+1}`:c.title,lines:ls}))}
 const usable=normalized.filter(c=>c.lines.length||['visual','lab'].includes(role(c.title).r));if(!usable.length)usable.push({title:'Golden lesson',lines:['No audited lesson text was supplied.']});
 if(!usable.some(c=>role(c.title).r==='summary')){const facts=usable.filter(c=>!['practice','assessment','lab'].includes(role(c.title).r)).flatMap(c=>c.lines).filter(x=>x.length<260).slice(-6);usable.push({title:ar(text)?'البطاقة النهائية — خلاصة الدرس':'Golden Final Card — Lesson Synthesis',lines:facts.length?facts:['Review the audited lesson ideas above.']})}
 return usable.map((c,i)=>({...c,index:i,...role(c.title)}));}
const CSS=`:root{--bg:#04111f;--panel:#081d31;--line:#315f82;--cyan:#67e8ff;--gold:#ffd36a;--txt:#f7fbff;--muted:#bfd4e4}*{box-sizing:border-box}html,body{margin:0;background:#04111f;color:var(--txt);font-family:system-ui,-apple-system,"Segoe UI",Tahoma,Arial,sans-serif}.nrc{min-height:100vh;padding:18px}.nrc-wrap{max-width:1100px;margin:auto}.nrc-title{text-align:center;color:var(--cyan);font-size:clamp(28px,4vw,46px);margin:18px 0 32px}.nrc-lesson{background:var(--panel);border:1px solid var(--line);border-radius:20px;padding:clamp(18px,4vw,46px);box-shadow:0 18px 44px #0005}.nrc-section{padding:8px 0 30px;margin-bottom:22px;border-bottom:1px solid #ffffff18}.nrc-section:last-child{border-bottom:0}.nrc-head{display:flex;gap:10px;align-items:center;margin-bottom:14px}.nrc-icon{font-size:28px}.nrc-head h2{margin:0;color:#a8efff;font-size:clamp(22px,3vw,31px)}.nrc-line{font-size:clamp(18px,2vw,22px);line-height:2;margin:12px 0;white-space:pre-wrap;overflow-wrap:anywhere}.nrc-lab-slot{margin:24px 0 4px;border:1px dashed #56758d;border-radius:14px;padding:14px;background:#061725}.nrc-lab-slot>strong{display:block;color:var(--gold);margin-bottom:8px}.nrc-lab-mount{min-height:70px}.nrc-note{color:var(--muted);line-height:1.8}@media(max-width:700px){.nrc{padding:6px}.nrc-lesson{padding:16px;border-radius:12px}.nrc-line{font-size:18px;line-height:1.9}}`;

function labSlot(c,i){
 return `<div class="nrc-lab-slot" data-lab-slot="${i}" data-lab-title="${esc(c.title)}"><strong>🧪 المختبر المرتبط بهذه الفكرة</strong><div class="nrc-lab-mount" data-lab-mount="${i}"></div></div>`
}
function markup(text,title){
 const cards=parse(text);
 return `<style>${CSS}</style><div class="nrc"><main class="nrc-wrap"><h1 class="nrc-title">${esc(title)}</h1><article class="nrc-lesson">${cards.map((c,i)=>`<section class="nrc-section" data-section="${i}" data-role="${c.r}"><div class="nrc-head"><span class="nrc-icon">${c.icon}</span><h2>${esc(c.title)}</h2></div>${c.lines.map(x=>`<p class="nrc-line" dir="${ar(x)?'rtl':'ltr'}">${esc(x)}</p>`).join('')}${c.r==='lab'?labSlot(c,i):''}</section>`).join('')}</article></main></div>`
}
function bind(root){
 /* Continuous-page renderer only.
    Existing lab runtime/generator is intentionally untouched.
    If the host exposes a verified lab mounting hook, call it for the matching
    audited lab section; otherwise leave the slot available rather than inventing content. */
 root.querySelectorAll('[data-lab-mount]').forEach(el=>{
   const section=el.closest('[data-section]');
   const payload=window.__NABIL_GOLDEN__||{};
   const hook=window.NABILMountVerifiedLab || window.mountNabilVerifiedLab;
   if(typeof hook==='function'){
     try{ hook(el,{lesson_id:payload.lesson_id||'',section_index:Number(section?.dataset.section||0),title:el.closest('[data-lab-slot]')?.dataset.labTitle||''}); }
     catch(e){ console.error('Verified lab mount failed',e); }
   } else {
     el.innerHTML='<div class="nrc-note">المختبر الموثق يظهر هنا عبر مشغّل المختبرات المعتمد.</div>';
   }
 });
}
window.NABILReferenceClassroomV16={mount(root,text,title,meta={}){root.innerHTML=markup(text,title);bind(root);root.dataset.lessonId=meta.lesson_id||'';root.dataset.renderer='reference-v16';},parse};
})();
