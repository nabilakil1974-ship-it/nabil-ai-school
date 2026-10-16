/* NABIL AI — "تحضير الدرس | Lesson Plan | Fiche de préparation".
   Static module: renders the plan from the lesson's own data (DATA.plan), lets the
   teacher edit period length / number of periods and the text, prints it and exports
   a real .docx (WordprocessingML + stored ZIP, no external library). */
(()=>{
'use strict';
const root=document.getElementById('nabilWholeLessonSmartLab');
const dataEl=document.getElementById('nabilV6Data');
if(!root||!dataEl)return;
const DATA=JSON.parse(dataEl.textContent);const PLAN=DATA.plan;if(!PLAN)return;
const $=id=>document.getElementById(id);
const modal=$('nbPlanModal'),doc=$('nbPlanDoc'),langSel=$('nbPlanLang'),minIn=$('nbPlanMin'),sesIn=$('nbPlanSes'),note=$('nbPlanNote');

const L={
ar:{dir:'rtl',plan:'تحضير الدرس',school:'المؤسسة التعليمية',teacher:'اسم الأستاذ',date:'التاريخ',klass:'الصف والشعبة',subject:'المادة',lesson:'عنوان الدرس',
 ref:'المرجع وصفحات الكتاب',book:'كتاب الطالب',pages:'الصفحات',comp:'الكفايات المستهدفة',compHint:'يُدخلها الأستاذ من وثيقة المركز التربوي للبحوث والإنماء (CRDP) للصف والمادة.',
 obj:'الأهداف التعليمية والإجرائية',objItem:'أن يشرح المتعلم ويطبّق: ',prior:'المكتسبات السابقة',priorHint:'يحدّدها الأستاذ بحسب صفه.',
 means:'الوسائل التعليمية',meansItems:['كتاب الطالب','سبورة NABIL AI التفاعلية (الكتابة والرسم والصوت)','دفتر الطالب والأدوات الهندسية عند الحاجة'],
 time:'عدد الحصص والمدة',periods:'عدد الحصص',duration:'مدة الحصة',min:'دقيقة',
 intro:'التمهيد والتحفيز',explore:'الأنشطة الاستكشافية وبناء المفاهيم',build:'شرح الدرس خطوة بخطوة',apply:'تطبيقات وتمارين الكتاب',
 eval:'التقويم',diag:'التقويم التشخيصي',form:'التقويم التكويني',summ:'التقويم الختامي',remed:'معالجة الصعوبات والفروق الفردية',
 hw:'الواجب المنزلي',concl:'الخلاصة',notes:'ملاحظات الأستاذ بعد الحصة',flow:'جدول سير الحصة',session:'الحصة',
 cols:['الزمن','المرحلة','نشاط الأستاذ','نشاط المتعلم','الوسائل','التقويم'],
 phases:['التمهيد','الاستكشاف','بناء المعرفة','التطبيق','التقويم والخلاصة'],
 tIntro:'يعلن عنوان الدرس وهدفه ويستحضر المكتسبات السابقة بأسئلة قصيرة.',lIntro:'يجيب ويستذكر ما تعلّمه سابقًا.',eIntro:'أسئلة تشخيصية شفهية.',
 tExp:'يفتح السبورة التفاعلية على الفكرة: ',lExp:'يلاحظ، يجرّب ويدوّن ملاحظاته.',eExp:'ملاحظة مشاركة المتعلمين.',
 tBuild:'يشرح خطوة بخطوة: ',lBuild:'يتابع، يكتب ويجيب عن الأسئلة التكوينية.',eBuild:'أسئلة تكوينية أثناء الشرح.',
 tApply:'يوجّه حلّ التمارين: ',lApply:'يحلّ التمارين ويقارن حلّه بالحل المشروح.',eApply:'تصحيح جماعي وفردي.',
 tEnd:'يلخّص مع المتعلمين ويطرح أسئلة ختامية قصيرة.',lEnd:'يعيد صياغة الخلاصة ويجيب.',eEnd:'سؤال ختامي قصير.',
 remedHint:'تمارين تدعيم للمتعثرين، وتمارين إثراء للمتفوقين، وتنويع الأمثلة والرسوم.',
 hwHint:'تمارين من الكتاب لم تُحَلّ في الحصة: ',blank:'………………',
 noEx:'لم تُدرج تمارين الكتاب في هذه الصفحة؛ يحدّدها الأستاذ من الكتاب.',
 crdp:'تنبيه: لم يُتحقَّق من مطابقة هذا النموذج لصيغة التحضير الرسمية للمركز التربوي للبحوث والإنماء؛ يراجعه الأستاذ قبل الاعتماد.',
 translated:'نصوص الشرح مأخوذة من لغة الدرس الأصلية ما لم تتوفر ترجمتها.',lessonLang:'لغة الدرس'},
en:{dir:'ltr',plan:'Lesson Plan',school:'School',teacher:'Teacher',date:'Date',klass:'Grade and section',subject:'Subject',lesson:'Lesson title',
 ref:'Reference and textbook pages',book:'Student textbook',pages:'Pages',comp:'Targeted competencies',compHint:'To be entered by the teacher from the CRDP (Lebanese curriculum) document for this grade and subject.',
 obj:'Learning and procedural objectives',objItem:'The learner explains and applies: ',prior:'Prior knowledge',priorHint:'To be set by the teacher for the class.',
 means:'Teaching aids',meansItems:['Student textbook','NABIL AI interactive board (writing, drawing, voice)','Notebook and geometry tools when needed'],
 time:'Number of periods and duration',periods:'Periods',duration:'Period length',min:'min',
 intro:'Introduction and motivation',explore:'Exploratory activities and concept building',build:'Step-by-step explanation',apply:'Textbook applications and exercises',
 eval:'Assessment',diag:'Diagnostic assessment',form:'Formative assessment',summ:'Summative assessment',remed:'Difficulties and individual differences',
 hw:'Homework',concl:'Conclusion',notes:'Teacher notes after the lesson',flow:'Lesson flow table',session:'Period',
 cols:['Time','Stage','Teacher activity','Learner activity','Aids','Assessment'],
 phases:['Introduction','Exploration','Building knowledge','Application','Assessment and conclusion'],
 tIntro:'States the title and goal and recalls prior knowledge with short questions.',lIntro:'Answers and recalls earlier learning.',eIntro:'Oral diagnostic questions.',
 tExp:'Opens the interactive board on the idea: ',lExp:'Observes, experiments and notes findings.',eExp:'Observing learner participation.',
 tBuild:'Explains step by step: ',lBuild:'Follows, writes and answers the formative questions.',eBuild:'Formative questions during the explanation.',
 tApply:'Guides the solving of: ',lApply:'Solves the exercises and compares with the worked solution.',eApply:'Class and individual correction.',
 tEnd:'Summarises with the learners and asks short closing questions.',lEnd:'Restates the conclusion and answers.',eEnd:'Short closing question.',
 remedHint:'Support exercises for learners who struggle, enrichment for advanced learners, varied examples and drawings.',
 hwHint:'Textbook exercises not solved in class: ',blank:'………………',
 noEx:'Textbook exercises are not listed on this page; the teacher selects them from the book.',
 crdp:'Notice: conformity of this template with the official CRDP lesson-plan format has not been verified; the teacher must review it before use.',
 translated:'Explanation text is taken from the lesson language unless a translation is available.',lessonLang:'Lesson language'},
fr:{dir:'ltr',plan:'Fiche de préparation',school:'Établissement',teacher:'Nom de l’enseignant',date:'Date',klass:'Classe et section',subject:'Matière',lesson:'Titre de la leçon',
 ref:'Référence et pages du manuel',book:'Manuel de l’élève',pages:'Pages',comp:'Compétences visées',compHint:'À renseigner par l’enseignant d’après le document du CRDP pour cette classe et cette matière.',
 obj:'Objectifs d’apprentissage et opérationnels',objItem:'L’élève explique et applique : ',prior:'Acquis antérieurs',priorHint:'À préciser par l’enseignant selon sa classe.',
 means:'Moyens didactiques',meansItems:['Manuel de l’élève','Tableau interactif NABIL AI (écriture, dessin, voix)','Cahier et instruments de géométrie si besoin'],
 time:'Nombre de séances et durée',periods:'Séances',duration:'Durée d’une séance',min:'min',
 intro:'Introduction et motivation',explore:'Activités d’exploration et construction des notions',build:'Explication pas à pas',apply:'Applications et exercices du manuel',
 eval:'Évaluation',diag:'Évaluation diagnostique',form:'Évaluation formative',summ:'Évaluation finale',remed:'Difficultés et différences individuelles',
 hw:'Devoir à la maison',concl:'Synthèse',notes:'Remarques de l’enseignant après la séance',flow:'Déroulement de la séance',session:'Séance',
 cols:['Durée','Phase','Activité de l’enseignant','Activité de l’élève','Moyens','Évaluation'],
 phases:['Introduction','Exploration','Construction du savoir','Application','Évaluation et synthèse'],
 tIntro:'Annonce le titre et l’objectif et rappelle les acquis par de courtes questions.',lIntro:'Répond et se rappelle ses acquis.',eIntro:'Questions diagnostiques orales.',
 tExp:'Ouvre le tableau interactif sur l’idée : ',lExp:'Observe, expérimente et note ses constats.',eExp:'Observation de la participation.',
 tBuild:'Explique pas à pas : ',lBuild:'Suit, écrit et répond aux questions formatives.',eBuild:'Questions formatives pendant l’explication.',
 tApply:'Guide la résolution de : ',lApply:'Résout les exercices et compare avec la solution expliquée.',eApply:'Correction collective et individuelle.',
 tEnd:'Fait la synthèse avec les élèves et pose de courtes questions finales.',lEnd:'Reformule la synthèse et répond.',eEnd:'Courte question finale.',
 remedHint:'Exercices de soutien pour les élèves en difficulté, d’approfondissement pour les plus avancés, exemples et dessins variés.',
 hwHint:'Exercices du manuel non résolus en classe : ',blank:'………………',
 noEx:'Les exercices du manuel ne sont pas listés sur cette page ; l’enseignant les choisit dans le livre.',
 crdp:'Avertissement : la conformité de ce modèle au format officiel de fiche du CRDP n’a pas été vérifiée ; l’enseignant doit le relire avant usage.',
 translated:'Le texte explicatif provient de la langue de la leçon, sauf traduction disponible.',lessonLang:'Langue de la leçon'}};

const PL=()=>window.NABILPageLanguage;
function trTo(s,lang){s=String(s||'');
  if(lang===(DATA.lang||'en'))return s;
  try{const t=PL()&&PL().translateText?PL().translateText(s,lang):s;return t||s}catch(e){return s}}
const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
/* canonical base^{exp} -> <sup> */
const mathHtml=s=>esc(s).replace(/([^\s^{}]*)\^\{([^{}]*)\}/g,(m,b,e)=>b+'<sup>'+e+'</sup>');
const blank=(l)=>'<span class="nb-blank">'+esc(L[l].blank)+'</span>';

function splitMinutes(total){
  const fr=[5,10,15,10,5],sum=45;let m=fr.map(f=>Math.max(1,Math.round(f*total/sum)));
  const diff=total-m.reduce((a,b)=>a+b,0);m[2]+=diff;return m}
function chunk(arr,n){const out=Array.from({length:n},()=>[]);arr.forEach((x,i)=>out[Math.min(n-1,Math.floor(i*n/arr.length))].push(x));return out}

function buildHtml(lang,minutes,sessions){
  const T=L[lang],P=PLAN,tr=s=>trTo(s,lang);
  const ideas=P.ideas.map(i=>({...i,title:tr(i.title),steps:i.steps.map(tr)}));
  const exs=P.exercises||[];
  const pages=P.pages&&P.pages.length?P.pages.join(', '):'';
  let h='<h1>'+esc(T.plan)+' — '+mathHtml(tr(P.title))+'</h1>';
  h+='<table><tr><th>'+esc(T.school)+'</th><td>'+blank(lang)+'</td><th>'+esc(T.teacher)+'</th><td>'+blank(lang)+'</td></tr>'
   +'<tr><th>'+esc(T.date)+'</th><td>'+blank(lang)+'</td><th>'+esc(T.klass)+'</th><td>'+(P.grade?esc(P.grade)+' — ':'')+blank(lang)+'</td></tr>'
   +'<tr><th>'+esc(T.subject)+'</th><td>'+(esc(P.subject)||blank(lang))+'</td><th>'+esc(T.lesson)+'</th><td>'+mathHtml(tr(P.title))+'</td></tr>'
   +'<tr><th>'+esc(T.ref)+'</th><td colspan="3">'+esc(T.book)+(pages?' — '+esc(T.pages)+': '+esc(pages):' — '+esc(T.pages)+': ')+(pages?'':blank(lang))+'</td></tr></table>';
  h+='<h2>'+esc(T.comp)+'</h2><p>'+blank(lang)+' <small>'+esc(T.compHint)+'</small></p>';
  h+='<h2>'+esc(T.obj)+'</h2><ul>'+ideas.map(i=>'<li>'+esc(T.objItem)+mathHtml(i.title)+'</li>').join('')+'</ul>';
  h+='<h2>'+esc(T.prior)+'</h2><p>'+blank(lang)+' <small>'+esc(T.priorHint)+'</small></p>';
  h+='<h2>'+esc(T.means)+'</h2><ul>'+T.meansItems.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul>';
  h+='<h2>'+esc(T.time)+'</h2><p>'+esc(T.periods)+': '+sessions+' — '+esc(T.duration)+': '+minutes+' '+esc(T.min)+'</p>';
  const m=splitMinutes(minutes),parts=chunk(ideas,sessions),exParts=chunk(exs,sessions);
  h+='<h2>'+esc(T.flow)+'</h2>';
  for(let s=0;s<sessions;s++){
    const idea=parts[s]||[],ex=exParts[s]||[];
    const titles=idea.map(i=>mathHtml(i.title)).join('; ')||blank(lang);
    const stepsTxt=idea.map(i=>mathHtml(i.title)+(i.formulas&&i.formulas.length?' ('+i.formulas.slice(0,2).map(mathHtml).join('، ')+')':'')).join('; ')||blank(lang);
    const exTxt=ex.length?ex.map(e=>esc(e.n)+(e.page?' ('+esc(T.pages)+' '+esc(e.page)+')':'')).join('، '):esc(T.noEx);
    const chk=(P.checks||[]).slice(0,2).map(mathHtml).join(' / ');
    if(sessions>1)h+='<h3>'+esc(T.session)+' '+(s+1)+'</h3>';
    const rows=[
     [T.tIntro,T.lIntro,esc(T.meansItems[1]),T.eIntro],
     [T.tExp+(idea[0]?idea[0].title:''),T.lExp,esc(T.meansItems[1]),T.eExp],
     [T.tBuild+stepsTxt,T.lBuild,esc(T.meansItems[1]),T.eBuild+(chk?' — '+chk:'')],
     [T.tApply+exTxt,T.lApply,esc(T.meansItems[0]),T.eApply],
     [T.tEnd,T.lEnd,esc(T.meansItems[0]),T.eEnd]];
    h+='<table><tr>'+T.cols.map(c=>'<th>'+esc(c)+'</th>').join('')+'</tr>';
    rows.forEach((r,i)=>{
      const cell=(x,raw)=>'<td>'+(i===1||i===2||i===3?x:esc(x))+'</td>';
      h+='<tr><td>'+m[i]+' '+esc(T.min)+'</td><td>'+esc(T.phases[i])+'</td>'
        +'<td>'+(i===1?esc(T.tExp)+(idea[0]?mathHtml(idea[0].title):''):i===2?esc(T.tBuild)+stepsTxt:i===3?esc(T.tApply)+exTxt:esc(r[0]))+'</td>'
        +'<td>'+esc(r[1])+'</td><td>'+r[2]+'</td><td>'+(i===2?esc(T.eBuild)+(chk?' — '+chk:''):esc(r[3]))+'</td></tr>'});
    h+='</table>'}
  h+='<h2>'+esc(T.intro)+'</h2><p>'+esc(T.tIntro)+'</p>';
  h+='<h2>'+esc(T.explore)+'</h2><ul>'+ideas.map(i=>'<li>'+mathHtml(i.title)+(i.has_drawing?' ✎':'')+'</li>').join('')+'</ul>';
  h+='<h2>'+esc(T.build)+'</h2>'+ideas.map(i=>'<p><b>'+mathHtml(i.title)+'</b></p><ul>'+i.steps.map(x=>'<li>'+mathHtml(x)+'</li>').join('')
     +(i.formulas&&i.formulas.length?'<li>'+i.formulas.map(mathHtml).join(' ; ')+'</li>':'')+'</ul>').join('');
  h+='<h2>'+esc(T.apply)+'</h2>'+(exs.length?'<ul>'+exs.map(e=>'<li>'+esc(e.n)+(e.page?' — '+esc(T.pages)+' '+esc(e.page):'')+(e.statement?': '+mathHtml(tr(e.statement)):'')+'</li>').join('')+'</ul>':'<p>'+esc(T.noEx)+'</p>');
  h+='<h2>'+esc(T.eval)+'</h2><ul><li><b>'+esc(T.diag)+':</b> '+esc(T.eIntro)+'</li><li><b>'+esc(T.form)+':</b> '+((P.checks||[]).length?(P.checks||[]).map(c=>mathHtml(tr(c))).join(' / '):esc(T.eBuild))+'</li><li><b>'+esc(T.summ)+':</b> '+esc(T.eEnd)+'</li></ul>';
  h+='<h2>'+esc(T.remed)+'</h2><p>'+esc(T.remedHint)+'</p>';
  h+='<h2>'+esc(T.hw)+'</h2><p>'+esc(T.hwHint)+blank(lang)+'</p>';
  h+='<h2>'+esc(T.concl)+'</h2>'+((P.key_results||[]).length?'<ul>'+P.key_results.map(x=>'<li>'+mathHtml(tr(x))+'</li>').join('')+'</ul>':'<p>'+blank(lang)+'</p>');
  h+='<h2>'+esc(T.notes)+'</h2><p>'+blank(lang)+'</p><p>'+blank(lang)+'</p>';
  return h}

/* ---------- cache: one plan per lesson_id + language (+ period settings) ---------- */
const key=(lang,m,s)=>'nabilPlan:'+PLAN.lesson_id+':'+lang+':'+m+'x'+s;
function cacheGet(k){try{return localStorage.getItem(k)}catch(e){return null}}
function cacheSet(k,v){try{localStorage.setItem(k,v)}catch(e){}}
let curKey='',fromCache=false;
function render(force){
  const lang=langSel.value,m=Math.max(20,Math.min(180,parseInt(minIn.value,10)||45)),s=Math.max(1,Math.min(10,parseInt(sesIn.value,10)||1));
  curKey=key(lang,m,s);const cached=force?null:cacheGet(curKey);
  fromCache=!!cached;doc.innerHTML=cached||buildHtml(lang,m,s);if(!cached)cacheSet(curKey,doc.innerHTML);
  doc.dir=L[lang].dir;doc.lang=lang;
  note.textContent=L[lang].crdp+' '+(lang!==(DATA.lang||'en')?L[lang].translated:'');
  window.__nbPlanState={lang,minutes:m,sessions:s,fromCache,key:curKey}}
let saveT=null;
doc.addEventListener('input',()=>{clearTimeout(saveT);saveT=setTimeout(()=>cacheSet(curKey,doc.innerHTML),300)});

/* ---------- DOCX (WordprocessingML, stored zip) ---------- */
const CRC=(()=>{const t=new Uint32Array(256);for(let n=0;n<256;n++){let c=n;for(let k=0;k<8;k++)c=c&1?0xEDB88320^(c>>>1):c>>>1;t[n]=c>>>0}return t})();
const crc32=b=>{let c=0xFFFFFFFF;for(let i=0;i<b.length;i++)c=CRC[(c^b[i])&255]^(c>>>8);return(c^0xFFFFFFFF)>>>0};
const enc=new TextEncoder();
function zip(files){
  const parts=[],central=[];let off=0;
  const u16=v=>[v&255,(v>>8)&255],u32=v=>[v&255,(v>>8)&255,(v>>16)&255,(v>>24)&255];
  for(const [name,text] of files){
    const nb=enc.encode(name),data=enc.encode(text),crc=crc32(data);
    const lh=new Uint8Array([0x50,0x4b,3,4,...u16(20),...u16(0x0800),...u16(0),...u16(0),...u16(0x21),...u32(crc),...u32(data.length),...u32(data.length),...u16(nb.length),...u16(0)]);
    parts.push(lh,nb,data);
    central.push(new Uint8Array([0x50,0x4b,1,2,...u16(20),...u16(20),...u16(0x0800),...u16(0),...u16(0),...u16(0x21),...u32(crc),...u32(data.length),...u32(data.length),...u16(nb.length),...u16(0),...u16(0),...u16(0),...u16(0),...u32(0),...u32(off)]),nb);
    off+=lh.length+nb.length+data.length}
  const csz=central.reduce((a,b)=>a+b.length,0);
  const end=new Uint8Array([0x50,0x4b,5,6,...u16(0),...u16(0),...u16(files.length),...u16(files.length),...u32(csz),...u32(off),...u16(0)]);
  return new Blob([...parts,...central,end],{type:'application/vnd.openxmlformats-officedocument.wordprocessingml.document'})}
const xe=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
function runs(node,rtl,base){
  /* inline content of node -> <w:r> list (sup, bold, br preserved) */
  let out='';
  const walk=(n,st)=>{
    if(n.nodeType===3){const t=n.nodeValue.replace(/\s+/g,' ');if(!t.trim()&&!t)return;
      out+='<w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/>'+(st.b?'<w:b/><w:bCs/>':'')+(st.sup?'<w:vertAlign w:val="superscript"/>':'')+(rtl?'<w:rtl/>':'')+'<w:sz w:val="'+(st.sz||22)+'"/><w:szCs w:val="'+(st.sz||22)+'"/></w:rPr><w:t xml:space="preserve">'+xe(t)+'</w:t></w:r>';return}
    if(n.nodeType!==1)return;const tag=n.tagName;
    if(tag==='BR'){out+='<w:r><w:br/></w:r>';return}
    if(tag==='UL'||tag==='TABLE')return;
    const ns={...st};if(tag==='B'||tag==='STRONG'||tag==='TH')ns.b=true;if(tag==='SUP')ns.sup=true;if(tag==='SMALL')ns.sz=18;
    n.childNodes.forEach(c=>walk(c,ns))};
  node.childNodes.forEach(c=>walk(c,{b:base&&base.b,sz:base&&base.sz}));return out}
const para=(inner,rtl,o)=>{o=o||{};return '<w:p><w:pPr>'+(o.style?'<w:pStyle w:val="'+o.style+'"/>':'')+(o.bullet?'<w:ind w:'+(rtl?'right':'left')+'="540" w:hanging="270"/>':'')+(rtl?'<w:bidi/>':'')+(o.jc?'<w:jc w:val="'+o.jc+'"/>':'')+'</w:pPr>'+(o.bullet?'<w:r><w:t xml:space="preserve">• </w:t></w:r>':'')+inner+'</w:p>'};
function cellXml(td,rtl,w,hdr){
  const lines=[];let cur=document.createElement('div');
  /* split on <br> and nested block lines into paragraphs */
  const flush=()=>{lines.push(cur);cur=document.createElement('div')};
  td.childNodes.forEach(c=>{if(c.nodeType===1&&c.tagName==='BR')flush();else cur.appendChild(c.cloneNode(true))});flush();
  const ps=lines.map(l=>para(runs(l,rtl,{b:hdr,sz:20}),rtl)).join('')||para('',rtl);
  const cs=td.getAttribute('colspan');
  return '<w:tc><w:tcPr><w:tcW w:w="'+w+'" w:type="dxa"/>'+(cs?'<w:gridSpan w:val="'+cs+'"/>':'')+(hdr?'<w:shd w:val="clear" w:color="auto" w:fill="E6F0F8"/>':'')+'</w:tcPr>'+ps+'</w:tc>'}
function tableXml(t,rtl){
  const rows=[...t.rows];const ncols=Math.max(...rows.map(r=>[...r.cells].reduce((a,c)=>a+(parseInt(c.getAttribute('colspan')||'1',10)),0)));
  const total=9600,w=Math.floor(total/ncols);
  let x='<w:tbl><w:tblPr><w:tblW w:w="'+total+'" w:type="dxa"/>'+(rtl?'<w:bidiVisual/>':'')+'<w:tblBorders>'+['top','left','bottom','right','insideH','insideV'].map(b=>'<w:'+b+' w:val="single" w:sz="4" w:space="0" w:color="777777"/>').join('')+'</w:tblBorders><w:tblLayout w:type="fixed"/></w:tblPr><w:tblGrid>'+Array.from({length:ncols},()=>'<w:gridCol w:w="'+w+'"/>').join('')+'</w:tblGrid>';
  rows.forEach(r=>{x+='<w:tr>'+[...r.cells].map(c=>cellXml(c,rtl,w*(parseInt(c.getAttribute('colspan')||'1',10)),c.tagName==='TH')).join('')+'</w:tr>'});
  return x+'</w:tbl>'+para('',rtl)}
function bodyXml(rtl){
  let b='';
  doc.childNodes.forEach(n=>{
    if(n.nodeType!==1)return;const tag=n.tagName;
    if(tag==='H1')b+=para(runs(n,rtl,{b:true,sz:36}),rtl,{style:'Heading1'});
    else if(tag==='H2')b+=para(runs(n,rtl,{b:true,sz:28}),rtl,{style:'Heading2'});
    else if(tag==='H3')b+=para(runs(n,rtl,{b:true,sz:24}),rtl,{style:'Heading3'});
    else if(tag==='P')b+=para(runs(n,rtl),rtl);
    else if(tag==='UL')n.querySelectorAll(':scope>li').forEach(li=>{b+=para(runs(li,rtl),rtl,{bullet:true})});
    else if(tag==='TABLE')b+=tableXml(n,rtl)});
  return b}
function buildDocx(){
  const lang=langSel.value,rtl=L[lang].dir==='rtl';
  const W='xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"';
  const document_='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document '+W+'><w:body>'+bodyXml(rtl)+'<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1000" w:right="1100" w:bottom="1000" w:left="1100" w:header="500" w:footer="500" w:gutter="0"/>'+(rtl?'<w:bidi/>':'')+'</w:sectPr></w:body></w:document>';
  const styles='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles '+W+'><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/><w:sz w:val="22"/><w:szCs w:val="22"/><w:lang w:val="'+lang+'" w:bidi="ar-SA"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="80"/></w:pPr></w:pPrDefault></w:docDefaults>'
    +'<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>'
    +['Heading1','Heading2','Heading3'].map((s,i)=>'<w:style w:type="paragraph" w:styleId="'+s+'"><w:name w:val="heading '+(i+1)+'"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="'+(i?200:0)+'" w:after="80"/><w:outlineLvl w:val="'+i+'"/></w:pPr><w:rPr><w:b/><w:color w:val="0B4F7A"/></w:rPr></w:style>').join('')+'</w:styles>';
  return zip([
   ['[Content_Types].xml','<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/></Types>'],
   ['_rels/.rels','<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'],
   ['word/_rels/document.xml.rels','<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>'],
   ['word/document.xml',document_],['word/styles.xml',styles]])}
function download(){
  const lang=langSel.value,blob=buildDocx(),a=document.createElement('a');
  const safe=String(PLAN.lesson_id).replace(/[^A-Za-z0-9_-]+/g,'_');
  a.href=URL.createObjectURL(blob);a.download='lesson-plan_'+safe+'_'+lang+'.docx';
  document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove()},1500)}

/* ---------- wiring ---------- */
function open(){
  try{window.NABILWholeLessonOrchestrator.pause()}catch(e){}
  const hand=document.getElementById('teacherHand');if(hand)hand.classList.remove('is-visible');
  const ui=(DATA.lang&&L[DATA.lang])?DATA.lang:'en';
  if(!modal.dataset.init){langSel.value=ui==='ar'||ui==='fr'||ui==='en'?ui:'en';modal.dataset.init='1'}
  $('nbPlanMinLab').textContent='⏱';$('nbPlanSesLab').textContent='#';
  modal.hidden=false;render(false)}
root.querySelectorAll('[data-nb-plan="open"]').forEach(b=>b.addEventListener('click',open));
$('nbPlanClose').onclick=()=>{modal.hidden=true};
$('nbPlanGen').onclick=()=>{if(!window.__nbPlanTouched||confirm(L[langSel.value].dir==='rtl'?'سيُستبدل النص المعدّل. متابعة؟':'Edited text will be replaced. Continue?'))render(true)};
doc.addEventListener('input',()=>{window.__nbPlanTouched=true});
[langSel,minIn,sesIn].forEach(e=>e.addEventListener('change',()=>{window.__nbPlanTouched=false;render(false)}));
$('nbPlanPrint').onclick=()=>window.print();
$('nbPlanDocx').onclick=download;
window.NABILLessonPlan={open,render,buildDocx,html:()=>doc.innerHTML};
})();
