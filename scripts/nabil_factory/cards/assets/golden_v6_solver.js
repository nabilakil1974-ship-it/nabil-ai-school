/* NABIL Golden V6 — «حل التمارين | Solve Exercise».
   Lives inside the board (so it stays visible in full screen). It never changes the V6 engine's
   behaviour: it only (1) collects/reads a question, (2) asks the student to confirm it, (3) fetches a
   solution from /api/solver/* and (4) hands scenes to NABILWholeLessonOrchestrator.enterInterlude(). */
(()=>{
'use strict';
const root=document.getElementById('nabilWholeLessonSmartLab');
const btn=document.getElementById('nbSolveBtn');
if(!root||!btn)return;
const O=()=>window.NABILWholeLessonOrchestrator,G=()=>window.NABILGoldenV6;
const qs=new URLSearchParams(location.search),lessonId=qs.get('lesson_id')||'';
const T={
ar:{title:'حل التمارين',book:'📖 من الكتاب',type:'⌨ اكتب تمرينًا',up:'📷 صورة / PDF',close:'إغلاق',
 pick:'اختر تمرينًا من هذا الدرس',pickNone:'— اختر —',stored:'حلّ محفوظ',noStored:'بلا حل محفوظ',num:'رقم التمرين',page:'رقم الصفحة',find:'ابحث في الكتاب',
 typeHint:'اكتب السؤال أو المعادلة هنا…',read:'اقرأ السؤال',camera:'التقط صورة بالكاميرا',file:'اختر صورة أو PDF',reading:'جارٍ قراءة السؤال…',
 confirmT:'هل هذا هو السؤال؟ راجعه وصحّحه إن لزم',unclear:'أجزاء غير واضحة — صحّحها قبل الحل:',figure:'وصف الشكل (إن وُجد):',
 ok:'أؤكد أن هذا هو التمرين — حلّه',sure:'راجعتُ النص وأؤكده كما هو',solving:'جارٍ كتابة الحل…',clar:'أحتاج توضيحًا قبل الحل:',
 edit:'عدّل النص ثم أعد المحاولة',problem:'المسألة',given:'المعطيات',required:'المطلوب',step:'الخطوة',because:'لأن:',answer:'الجواب',
 verified:'✔ تحقّق آلي: الجواب يطابق حلّ المعادلة بالحاسوب.',mismatch:'⚠ تنبيه: التحقق الآلي لم يطابق الجواب، راجع الحل مع معلمك.',
 badgeStored:'✔ حلّ محفوظ من الكتاب',badgeNew:'⚙ حلّ جديد مُولَّد عند الطلب — راجعه مع معلمك',repeat:'↻ كرّر الخطوة',back:'↩ العودة إلى الدرس',
 noLesson:'البحث بالرقم والصفحة متاح داخل درس منصّة فقط.',src:{typed:'نص مكتوب',image:'صورة',pdf:'PDF ممسوح','pdf_text':'PDF',book_index:'الكتاب المفهرس'}},
fr:{title:'Résoudre un exercice',book:'📖 Du livre',type:'⌨ Écrire',up:'📷 Photo / PDF',close:'Fermer',
 pick:'Choisis un exercice de cette leçon',pickNone:'— choisir —',stored:'solution enregistrée',noStored:'sans solution enregistrée',num:"N° de l'exercice",page:'N° de page',find:'Chercher dans le livre',
 typeHint:"Écris la question ou l'équation ici…",read:'Lire la question',camera:'Prendre une photo',file:'Choisir une image ou un PDF',reading:'Lecture de la question…',
 confirmT:"C'est bien la question ? Relis et corrige si besoin",unclear:'Passages peu clairs — corrige avant de résoudre :',figure:'Description de la figure (si besoin) :',
 ok:"Je confirme que c'est mon exercice — résoudre",sure:'J’ai relu et je confirme le texte tel quel',solving:'Écriture de la solution…',clar:'Il me faut une précision avant de résoudre :',
 edit:'Modifie le texte puis réessaie',problem:'Énoncé',given:'Données',required:'À trouver',step:'Étape',because:'Car :',answer:'Réponse',
 verified:'✔ Vérification automatique : la réponse correspond à la résolution par ordinateur.',mismatch:"⚠ Attention : la vérification automatique ne correspond pas, vérifie avec ton professeur.",
 badgeStored:'✔ Solution enregistrée du livre',badgeNew:'⚙ Nouvelle solution générée à la demande — à vérifier avec ton professeur',repeat:"↻ Répéter l'étape",back:'↩ Retour à la leçon',
 noLesson:'La recherche par numéro et page est disponible dans une leçon de la plateforme.',src:{typed:'texte',image:'image',pdf:'PDF scanné','pdf_text':'PDF',book_index:'livre indexé'}},
en:{title:'Solve Exercise',book:'📖 From the book',type:'⌨ Type it',up:'📷 Photo / PDF',close:'Close',
 pick:'Pick an exercise from this lesson',pickNone:'— choose —',stored:'stored solution',noStored:'no stored solution',num:'Exercise number',page:'Page number',find:'Find in the book',
 typeHint:'Type the question or equation here…',read:'Read the question',camera:'Take a photo',file:'Choose an image or PDF',reading:'Reading the question…',
 confirmT:'Is this your question? Check it and fix it if needed',unclear:'Unclear parts — fix them before solving:',figure:'Figure description (if any):',
 ok:'I confirm this is my exercise — solve it',sure:'I checked the text and confirm it as it is',solving:'Writing the solution…',clar:'I need a clarification before solving:',
 edit:'Edit the text and try again',problem:'Problem',given:'Given',required:'Required',step:'Step',because:'Because:',answer:'Answer',
 verified:'✔ Automatic check: the answer matches the computer solution of the equation.',mismatch:'⚠ Warning: the automatic check did not match the answer; review it with your teacher.',
 badgeStored:'✔ Stored solution from the book',badgeNew:'⚙ New solution generated on demand — review it with your teacher',repeat:'↻ Repeat step',back:'↩ Back to the lesson',
 noLesson:'Lookup by number and page is available inside a platform lesson.',src:{typed:'typed text',image:'image',pdf:'scanned PDF','pdf_text':'PDF',book_index:'indexed book'}}};
const L=()=>{const l=(G()&&G().cur&&G().cur())||'ar';return T[l]?l:'ar'},t=()=>T[L()];
const el=(tag,attrs,kids)=>{const e=document.createElement(tag);Object.entries(attrs||{}).forEach(([k,v])=>{if(k==='text')e.textContent=v;else if(k==='class')e.className=v;else e.setAttribute(k,v)});(kids||[]).forEach(k=>e.append(k));return e};
const pretty=s=>String(s||'').replace(/sqrt\(([^()]*)\)/g,'√($1)').replace(/<=/g,'≤').replace(/>=/g,'≥').replace(/!=/g,'≠').replace(/\*/g,'×').replace(/\^(-?\d+|[a-zA-Z])/g,'^{$1}');
let modal=null,wasPlaying=false,pending={statement:'',source:'',unclear:[]},busy=false;

function open(){
  try{const st=O().state();wasPlaying=!!(st.started&&!st.paused&&!st.final);if(wasPlaying)O().pause()}catch(e){wasPlaying=false}
  if(modal)modal.remove();build();root.appendChild(modal);modal.hidden=false;
  const f=modal.querySelector('button');f&&f.focus&&f.focus()}
function close(resume){if(modal){modal.remove();modal=null}if(resume&&wasPlaying){try{O().resume()}catch(e){}}wasPlaying=false}
function build(){
  const x=t();modal=el('div',{id:'nbSolveModal',class:'nb-modal nb-solve',role:'dialog','aria-modal':'true','aria-label':x.title,dir:L()==='ar'?'rtl':'ltr'});
  const box=el('div',{class:'nb-modal-box nb-solve-box'});
  const bar=el('div',{class:'nb-modal-bar'},[el('b',{text:'🧮 '+x.title+' | Solve Exercise'}),el('button',{type:'button',id:'nbSolveClose',text:x.close})]);
  bar.lastChild.onclick=()=>close(true);
  const tabs=el('div',{class:'nb-solve-tabs',role:'tablist'});
  const body=el('div',{class:'nb-solve-body',id:'nbSolveBody'});
  const defs=[['book',x.book],['type',x.type],['up',x.up]];
  defs.forEach(([k,label],i)=>{const b=el('button',{type:'button',role:'tab',id:'nbSolveTab_'+k,'aria-selected':String(i===0),text:label});b.onclick=()=>{tabs.querySelectorAll('button').forEach(n=>n.setAttribute('aria-selected',String(n===b)));show(k,body)};tabs.append(b)});
  box.append(bar,tabs,body);modal.append(box);show('book',body)}
function status(body,msg,cls){let s=body.querySelector('.nb-solve-msg');if(!s){s=el('div',{class:'nb-solve-msg','aria-live':'polite'});body.append(s)}s.className='nb-solve-msg '+(cls||'');s.textContent=msg||''}
function show(kind,body){
  const x=t();body.replaceChildren();
  if(kind==='book'){
    const ex=(G().context().exercises)||[];
    const sel=el('select',{id:'nbSolveEx','aria-label':x.pick},[el('option',{value:'',text:x.pickNone})]);
    ex.forEach(e=>sel.append(el('option',{value:String(e.scene),text:e.n+' — '+(e.solved?x.stored:x.noStored)})));
    const go=el('button',{type:'button',class:'nb-solve-go',id:'nbSolveExGo',text:x.title});
    go.onclick=()=>{if(sel.value===''){status(body,x.pick,'err');return}
      const idx=+sel.value,e=ex.find(z=>z.scene===idx),sc=O().sceneAt(idx);
      if(e&&e.solved&&sc){const copy=Object.assign({},sc,{title:x.badgeStored});close(false);O().enterInterlude([copy],{kind:'stored'});return}
      /* no stored solution: take the exercise statement from the lesson and solve it on demand */
      const first=((sc&&sc.steps)||[]).find(s=>s.t==='text');
      confirmPane(body,{statement:first?first.text:'',source:'book_index',unclear:[]})};
    const num=el('input',{type:'text',id:'nbSolveNum',inputmode:'numeric','aria-label':x.num,placeholder:x.num}),pg=el('input',{type:'text',id:'nbSolvePage',inputmode:'numeric','aria-label':x.page,placeholder:x.page});
    const find=el('button',{type:'button',class:'nb-solve-go',id:'nbSolveFind',text:x.find});
    find.onclick=async()=>{
      if(!lessonId){status(body,x.noLesson,'err');return}
      if(!num.value.trim()&&!pg.value.trim()){status(body,x.num+' / '+x.page,'err');return}
      status(body,x.reading,'');const fd=new FormData();fd.append('lesson_id',lessonId);fd.append('number',num.value);fd.append('page',pg.value);
      try{const r=await fetch('/api/solver/book',{method:'POST',body:fd});const d=await r.json();
        if(d.status==='ok')confirmPane(body,{statement:d.statement,source:'book_index',unclear:d.heading_verified?[]:[d.message||''].filter(Boolean),image:d.page_image_url});
        else status(body,d.message||'—','err')}catch(e){status(body,String(e),'err')}};
    body.append(el('label',{text:x.pick}),sel,go,el('hr'),el('div',{class:'nb-solve-row'},[num,pg]),find);status(body,'','');return}
  if(kind==='type'){
    const ta=el('textarea',{id:'nbSolveText',rows:'5',placeholder:x.typeHint,dir:'auto'});
    const keys=el('div',{class:'nb-solve-keys'});
    ['√(',' ^ ','²','³','÷','×','±','≤','≥','≠','π','∞','(',')','/','='].forEach(k=>{const b=el('button',{type:'button',text:k.trim()||k});b.onclick=()=>{const s=ta.selectionStart||ta.value.length;ta.setRangeText(k,s,ta.selectionEnd||s,'end');ta.focus()};keys.append(b)});
    const go=el('button',{type:'button',class:'nb-solve-go',id:'nbSolveRead',text:x.read});
    go.onclick=()=>{if(ta.value.trim().length<3){status(body,x.typeHint,'err');return}confirmPane(body,{statement:ta.value.trim(),source:'typed',unclear:[]})};
    body.append(keys,ta,go);status(body,'','');return}
  /* upload */
  const cam=el('input',{type:'file',accept:'image/*',capture:'environment',id:'nbSolveCam',hidden:''});
  const fil=el('input',{type:'file',accept:'image/jpeg,image/png,image/webp,application/pdf',id:'nbSolveFile',hidden:''});
  const b1=el('button',{type:'button',class:'nb-solve-go',text:x.camera}),b2=el('button',{type:'button',class:'nb-solve-go',text:x.file});
  b1.onclick=()=>cam.click();b2.onclick=()=>fil.click();
  const prev=el('div',{class:'nb-solve-prev'});
  const pick=async f=>{if(!f)return;prev.replaceChildren();
    if(f.type.startsWith('image/')){const im=el('img',{alt:'',class:'nb-solve-thumb'});im.src=URL.createObjectURL(f);prev.append(im)}else prev.append(el('div',{text:'📄 '+f.name}));
    status(body,x.reading,'');const fd=new FormData();fd.append('file',f,f.name);fd.append('lang',L());
    try{const r=await fetch('/api/solver/read',{method:'POST',body:fd});const d=await r.json();
      if(!r.ok||d.status==='error'){status(body,d.message||('HTTP '+r.status),'err');return}
      if(d.status==='unreadable'){status(body,(d.unclear||[]).join(' · ')||x.edit,'err');return}
      confirmPane(body,{statement:d.statement+(d.has_figure&&d.figure_description?'\n['+x.figure+' '+d.figure_description+']':''),source:d.source,unclear:d.unclear||[]})}catch(e){status(body,String(e),'err')}};
  cam.onchange=()=>pick(cam.files[0]);fil.onchange=()=>pick(fil.files[0]);
  body.append(b1,b2,cam,fil,prev);status(body,'','')}

function confirmPane(body,p){
  const x=t();pending=p;body.replaceChildren();
  body.append(el('h4',{text:x.confirmT+' ('+((x.src||{})[p.source]||p.source)+')'}));
  if(p.image)body.append(el('a',{href:p.image,target:'_blank',rel:'noopener',text:'🖼'}));
  const ta=el('textarea',{id:'nbSolveConfirmText',rows:'6',dir:'auto'});ta.value=p.statement||'';
  const prevEl=el('div',{class:'nb-solve-render',id:'nbSolveRender',dir:'auto'});const draw=()=>{prevEl.textContent=pretty(ta.value)};draw();ta.oninput=draw;
  body.append(ta,prevEl);
  let sure=null;
  if((p.unclear||[]).length){
    body.append(el('div',{class:'nb-solve-unclear'},[el('b',{text:x.unclear}),el('ul',{},p.unclear.map(u=>el('li',{text:u})))]));
    sure=el('input',{type:'checkbox',id:'nbSolveSure'});body.append(el('label',{class:'nb-solve-sure'},[sure,document.createTextNode(' '+x.sure)]))}
  const go=el('button',{type:'button',class:'nb-solve-go',id:'nbSolveConfirm',text:x.ok});
  if(sure){go.disabled=true;sure.onchange=()=>{go.disabled=!sure.checked};ta.addEventListener('input',()=>{go.disabled=false},{once:true})}
  go.onclick=()=>run(body,ta.value.trim(),go);
  body.append(go);status(body,'','')}

async function run(body,statement,go){
  const x=t();if(busy||statement.length<3)return;busy=true;go.disabled=true;status(body,x.solving,'');
  const ctx=G().context();const meta=(ctx&&ctx.meta)||{};
  try{
    const r=await fetch('/api/solver/solve',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({statement,confirmed:true,lang:L(),grade:meta.grade||'',subject:meta.subject||''})});
    const d=await r.json();
    if(!r.ok||d.status==='error'){status(body,d.message||('HTTP '+r.status),'err');go.disabled=false;return}
    if(d.status==='needs_clarification'){body.append(el('div',{class:'nb-solve-unclear'},[el('b',{text:x.clar}),el('ul',{},d.questions.map(q=>el('li',{text:q})))]));status(body,x.edit,'err');go.disabled=false;return}
    const scenes=toScenes(d);close(false);O().enterInterlude(scenes,{kind:'solve'})}
  catch(e){status(body,String(e),'err');go.disabled=false}finally{busy=false}}

/* Property marks (equal ticks, equal-angle arcs, parallel arrows) are drawn by the shared `annotate` action:
   the hand points at the element and draws the mark while the lead-in sentence is spoken (NABIL rule LL-12). */
const PROP=new Set(['equal','equal_angle','parallel']);
function splitMarks(fig){
  const ms=(fig&&fig.marks)||[];
  const items=ms.filter(m=>PROP.has(m.type)).map(m=>m.type==='equal_angle'
    ?{kind:'arc',at:m.at,from:m.between[0],to:m.between[1],n:m.n,g:m.g}
    :{kind:m.type,segs:m.segs,n:m.n,g:m.g});
  return{rest:Object.assign({},fig,{marks:ms.filter(m=>!PROP.has(m.type))}),items}}
function toScenes(sol){
  const x=T[sol.lang]||t(),sl=sol.lang==='en'?undefined:sol.lang;
  const mk=(text,label,extra)=>Object.assign({t:'text',text:pretty(text),label:label||'',speech:String(text),speech_lang:sl},extra||{});
  const steps=[mk(sol.statement,x.problem)];
  const hasFig=!!(sol.figure&&Object.keys(sol.figure.points||{}).length>=2),fsteps=hasFig&&(sol.steps||[]).some(z=>z.figure_step);
  const baseSplit=hasFig?splitMarks(sol.figure):null;
  if(hasFig)steps.push({t:'draw',draw:'figure',args:baseSplit.rest});
  if(hasFig&&baseSplit.items.length)steps.push({t:'draw',draw:'annotate',clear:false,args:{items:baseSplit.items}});
  (sol.given||[]).forEach((g,i)=>steps.push(mk(g,i?'':x.given)));
  (sol.required||[]).forEach((g,i)=>steps.push(mk(g,i?'':x.required)));
  (sol.steps||[]).forEach((st,i)=>{
    const lead=st.say||(x.step+' '+(i+1));
    if(fsteps&&st.figure_step){
      const sp=splitMarks(st.figure_step),fa=Object.assign({points:sol.figure.points},sp.rest);
      if((fa.segments||[]).length||(fa.marks||[]).length||(fa.show||[]).length)steps.push({t:'draw',draw:'figure',clear:false,args:fa});
      if(sp.items.length)steps.push({t:'draw',draw:'annotate',clear:false,args:{items:sp.items},speech:st.say||'',speech_lang:sl})}
    if(st.construct&&st.construct.ops&&st.construct.ops.length)steps.push({t:'draw',draw:'construct',args:Object.assign({keep:true},st.construct),speech:st.say||st.text||'',speech_lang:sl});
    steps.push(mk(st.text||st.say,lead,Object.assign({speech:(st.say&&st.text?st.say+'. ':'')+(st.text||'')},st.justification?{hint:x.because+' '+st.justification}:{})));
    if(st.formula)steps.push({t:'formula',text:pretty(st.formula),speech:st.formula,speech_lang:sl})});
  String(sol.answer||'').split(/\s*\|\s*/).filter(Boolean).forEach((part,i)=>steps.push(mk(part,i?'':x.answer)));
  const v=(sol.verification||{}).status;
  if(v==='verified')steps.push(mk(x.verified,''));else if(v==='mismatch')steps.push(mk(x.mismatch,''));
  return [{id:'solve',title:x.badgeNew,start_mode:'single',steps,solved:true}]}

btn.addEventListener('click',open);
window.NABILSolver={open,close,toScenes,pretty,_state:()=>({pending})};
})();
