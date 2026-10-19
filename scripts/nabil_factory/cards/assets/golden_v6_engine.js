/* NABIL AI Golden V6 engine — ONE static engine, lesson DATA only.
   Hand image, pen/hand travel, word-by-word writing, cube drawing actions and the
   SINGLE/DUAL board come from the approved
   NABIL_G07_CUBE_GOLDEN_V6_APPROVED_VOICE_ON_SIDES.html (reference copy kept in
   assets/golden_v6_reference). The factory never generates this code per lesson. */
(()=>{
'use strict';
const root=document.getElementById('nabilWholeLessonSmartLab');
if(!root)return;
const $=id=>document.getElementById(id);
const raw=$('nabilV6Data').textContent;
const DATA=JSON.parse(raw);
const LANG=DATA.lang||'en';
/* language follows the page translation runtime (NABILPageLanguage) when present */
const PL=()=>window.NABILPageLanguage;
const cur=()=>{const l=PL()&&PL().get&&PL().get();return(DATA.ui_all&&DATA.ui_all[l])?l:LANG};
const tr=s=>{s=String(s||'');try{return PL()&&PL().translateText?PL().translateText(s,cur()):s}catch(_){return s}};
const U=()=>(DATA.ui_all&&DATA.ui_all[cur()])||{};
const FAST=!!window.NABIL_V18_FAST;
const NS='http://www.w3.org/2000/svg';
let SCENES=DATA.scenes||[];
let FINAL=SCENES.length;
let INTER=null,saved=null,marks=[];
const stageEl=$('nbStage'),workspace=$('nbWorkspace'),writing=$('nbWriting'),
  ink=$('nbInk'),svg=$('nbBoard'),statusEl=$('nbStatus'),headTitle=$('nbHeadTitle'),
  progEl=$('nbProg'),hand=$('teacherHand'),voiceNote=$('nbVoiceNote'),golden=$('nbGolden');
const playBtn=$('nabilWholePlay'),voiceBtn=$('nabilWholeVoice'),speedSel=$('nbSpeed'),
  prevBtn=$('nabilWholePrev'),nextBtn=$('nabilWholeNext'),replayBtn=$('nabilWholeRestart'),
  lostBtn=$('nbLost'),arBtn=$('nbArVoice'),exSel=$('nbExercise'),fsBtn=$('nbFullscreen'),exitBtn=$('nbExit'),startBtn=$('nbStart'),avatarOpen=$('nbAvatarOpen');

let index=0,run=0,paused=false,voice=true,speed=0.7,started=false,speaking=false,boardMode='single',
    finished=false,activeAnchor=null,studentWait=false,lastText='',curStepNo=0,gotUnderstood=null;
let handUrl=null,avatarUrl=null;
const modeLog=[];

/* ---------- assets (Blob URLs, never data: URIs) ---------- */
function blobUrl(b64,type){const bytes=Uint8Array.from(atob(b64.trim()),c=>c.charCodeAt(0));return URL.createObjectURL(new Blob([bytes],{type}))}
try{handUrl=blobUrl($('nabilV6HandPayload').textContent,'image/png');hand.src=handUrl}catch(e){}
try{avatarUrl=blobUrl(DATA.avatar_base64||'','image/jpeg');avatarOpen.src=avatarUrl}catch(e){}
window.addEventListener('pagehide',()=>{[handUrl,avatarUrl].forEach(u=>u&&URL.revokeObjectURL(u))});

/* ---------- math: canonical base^{exp} -> real superscripts, LTR isolation ---------- */
function supNodes(txt,into){
  const re=/([^\s^{}]*)\^\{([^{}]*)\}/g;let last=0,m;
  while((m=re.exec(txt))){
    if(m.index>last)into.appendChild(document.createTextNode(txt.slice(last,m.index)));
    if(m[1])into.appendChild(document.createTextNode(m[1]));
    const s=document.createElement('sup');s.className='nb-sup';s.textContent=m[2];into.appendChild(s);last=re.lastIndex}
  if(last<txt.length)into.appendChild(document.createTextNode(txt.slice(last)));
}
/* text -> array of reveal units (DOM nodes) */
function unitsOf(text,rtl,formula){
  const units=[];
  const pushPlain=s=>{(s.match(/\S+\s*/g)||[]).forEach(w=>{const sp=document.createElement('span');sp.textContent=w;units.push(sp)})};
  if(formula){
    (String(text).match(/\S+\s*/g)||[]).forEach(w=>{const sp=document.createElement('span');supNodes(w,sp);units.push(sp)});
    return units}
  const words=String(text).match(/\S+\s*/g)||[];
  const isMath=w=>/[0-9^{}=+×÷−<>≤≥≠≈√]/.test(w);
  const isLatin=w=>/^[A-Za-z][A-Za-z'’-]*[.,;:!?]?\s*$/.test(w);
  let i=0;
  const bdiOf=str=>{const b=document.createElement('bdi');b.dir='ltr';b.className='nb-math';supNodes(str,b);return b};
  while(i<words.length){
    const w=words[i];
    if(rtl&&(isMath(w)||isLatin(w))){
      /* RTL page: keep a Latin/math run together, isolated LTR, so it never flips */
      let j=i,buf='';
      while(j<words.length&&(isMath(words[j])||isLatin(words[j]))){buf+=words[j];j++}
      const b=bdiOf(buf.replace(/\s+$/,''));units.push(b);
      const sp=document.createElement('span');sp.textContent=' ';units.push(sp);i=j}
    else if(isMath(w)){const b=bdiOf(w.replace(/\s+$/,''));units.push(b);
      const sp=document.createElement('span');sp.textContent=' ';units.push(sp);i++}
    else{const sp=document.createElement('span');sp.textContent=w;units.push(sp);i++}}
  return units}
/* Golden Card / vendored engine text: turn canonical base^{exp} into real superscripts */
function enhanceDom(host){
  const w=document.createTreeWalker(host,NodeFilter.SHOW_TEXT,null);const hits=[];
  while(w.nextNode()){const n=w.currentNode;if(/\^\{/.test(n.nodeValue)&&!n.parentElement.closest('script,style'))hits.push(n)}
  hits.forEach(n=>{const f=document.createDocumentFragment();
    const b=document.createElement('bdi');b.dir='ltr';b.className='nb-math';supNodes(n.nodeValue,b);f.appendChild(b);n.replaceWith(f)})}
function speakable(t){
  return String(t||'').replace(/\^\{\s*(-?[^{}]+)\s*\}/g,' to the power $1 ')
    .replace(/×/g,' times ').replace(/÷/g,' divided by ').replace(/−/g,' minus ')
    .replace(/=/g,' equals ').replace(/≠/g,' is not equal to ').replace(/\s+/g,' ').trim()}

/* ---------- timing: every wait honours pause + speed ---------- */
async function wait(ms,id){
  if(FAST)return id===run;
  let t=0;
  while(t<ms){
    if(id!==run)return false;
    if(paused){await new Promise(r=>setTimeout(r,60));continue}
    await new Promise(r=>setTimeout(r,25));t+=25*speed}
  return id===run}
async function tick(id){
  while(paused&&id===run)await new Promise(r=>setTimeout(r,60));
  return id===run}

/* ---------- the one photorealistic hand ---------- */
function handAtClient(x,y){hand.style.left=x+'px';hand.style.top=y+'px';hand.classList.add('is-visible')}
function hideHand(){hand.classList.remove('is-visible');activeAnchor=null}
function tipOf(node,rtl){const r=node.getBoundingClientRect();return{x:rtl?r.left+4:r.right-4,y:r.top+Math.min(r.height*.7,30)}}
function placeHandAtNode(node,rtl){activeAnchor={node,rtl};const p=tipOf(node,rtl);handAtClient(p.x,p.y);return p}
function svgPoint(x,y){
  const p=svg.createSVGPoint();p.x=x;p.y=y;const m=svg.getScreenCTM();
  if(m){const q=p.matrixTransform(m);handAtClient(q.x,q.y)}}
function relayout(){ /* coordinates are recomputed from live rectangles after any layout change */
  if(activeAnchor&&activeAnchor.node.isConnected){const p=tipOf(activeAnchor.node,activeAnchor.rtl);handAtClient(p.x,p.y)}}
window.addEventListener('resize',relayout);
try{new ResizeObserver(relayout).observe(workspace)}catch(e){}
async function glide(from,to,id,ms){
  const n=8;
  for(let k=1;k<=n;k++){
    if(id!==run)return false;
    const t=k/n,e=t*t*(3-2*t);
    handAtClient(from.x+(to.x-from.x)*e,from.y+(to.y-from.y)*e);
    if(!await wait(ms/n,id))return false}
  return true}

/* ---------- SINGLE / DUAL board: one engine, switch without reload ---------- */
function setBoardMode(mode,opts){
  opts=opts||{};
  if(mode!=='single'&&mode!=='dual')mode='single';
  if(boardMode!==mode||opts.force){
    boardMode=mode;workspace.setAttribute('data-board-mode',mode);root.setAttribute('data-board-mode',mode);
    modeLog.push({mode,scene:index,at:Date.now()});
    /* writing, ink, hand, audio and progress are NOT touched: preserveState */
    requestAnimationFrame(relayout)}
  return boardMode}

/* ---------- speech (English only by default) ---------- */
function enVoice(){
  const vs=(window.speechSynthesis&&speechSynthesis.getVoices())||[];
  return vs.find(v=>/^en[-_]US/i.test(v.lang))||vs.find(v=>/^en/i.test(v.lang))||null}
function rate(){return Math.min(1.6,0.55+speed*0.45)}
let arOn=false,lastAr='';
function arVoiceObj(){const vs=(window.speechSynthesis&&speechSynthesis.getVoices())||[];return vs.find(v=>/^ar/i.test(v.lang))||null}
const AR_LET={A:'إيه',B:'بي',C:'سي',D:'دي',E:'إي',F:'إف',G:'جي',H:'إتش',I:'آي',J:'جيه',K:'كيه',L:'إل',M:'إم',N:'إن',O:'أو',P:'بي',Q:'كيو',R:'آر',S:'إس',T:'تي',U:'يو',V:'في',W:'دبليو',X:'إكس',Y:'واي',Z:'زد'};
/* spoken form only: the board text is untouched. Capital-letter names (AH, BM, ABC) are spelled letter by letter so the
   Arabic voice never reads them as a word; degrees/operators are said in Arabic. */
function speakableAr(t){
  return String(t||'').replace(/\^\{\s*(-?[^{}]+)\s*\}/g,' أُس $1 ')
    .replace(/(\d+(?:[.,]\d+)?)\s*°/g,'$1 درجة ').replace(/°/g,' درجة ')
    .replace(/\b[A-Z]{1,4}\b/g,m=>' '+[...m].map(c=>AR_LET[c]||c).join(' ')+' ')
    .replace(/×/g,' ضرب ').replace(/÷/g,' تقسيم ').replace(/\+/g,' زائد ')
    .replace(/[−–]/g,' ناقص ').replace(/=/g,' يساوي ').replace(/[|✓✔]/g,' . ').replace(/[\[\]()]/g,' ').replace(/\s+/g,' ').trim()}
function arTextOf(step){
  if(step.t==='formula')return '';
  if(step.ar)return step.ar;
  if(cur()==='ar')return tr(step.text);
  try{const t=PL()&&PL().translateText?PL().translateText(String(step.text||''),'ar'):'';return(t&&t!==step.text&&/[\u0600-\u06FF]/.test(t))?t:''}catch(e){return ''}}
function speakFr(t){return String(t||'').replace(/\^\{\s*(-?[^{}]+)\s*\}/g,' puissance $1 ').replace(/×/g,' fois ').replace(/÷/g,' divisé par ').replace(/−/g,' moins ').replace(/=/g,' égale ').replace(/\s+/g,' ').trim()}
function voiceLang(l){const vs=(window.speechSynthesis&&speechSynthesis.getVoices())||[];return vs.find(v=>new RegExp('^'+l,'i').test(v.lang))||null}
function speakText(text,id,ar,sl){
  lastText=text;lastAr=ar||'';
  const enOk=!!(voice&&text),arOk=!!(arOn&&ar);
  if(FAST||!('speechSynthesis' in window)||(!enOk&&!arOk))return null;
  try{
    speechSynthesis.cancel();
    const h={done:false,started:false,t0:Date.now(),text:(enOk?text:'')+' '+(arOk?ar:''),pending:0};
    const add=u=>{h.pending++;
      u.onstart=()=>{h.started=true;speaking=true;voiceNote.classList.remove('on')};
      u.onend=u.onerror=()=>{h.pending--;if(h.pending<=0){h.done=true;speaking=false}};
      speechSynthesis.speak(u)};
    if(enOk&&(sl==='ar'||sl==='fr')){const u=new SpeechSynthesisUtterance(sl==='ar'?speakableAr(text):speakFr(text));u.lang=sl==='ar'?'ar-SA':'fr-FR';u.rate=rate();const v=voiceLang(sl);if(v)u.voice=v;add(u)}
    else if(enOk){const u=new SpeechSynthesisUtterance(speakable(text));u.lang='en-US';u.rate=rate();const v=enVoice();if(v)u.voice=v;add(u)}
    if(arOk){const u=new SpeechSynthesisUtterance(speakableAr(ar));u.lang='ar-SA';u.rate=rate();const v=arVoiceObj();if(v)u.voice=v;add(u)}
    setTimeout(()=>{if(!h.started&&!h.done&&id===run&&!paused){showVoiceNote()}},1600);
    return h}
  catch(e){return null}}
function showVoiceNote(){
  voiceNote.classList.add('on');
  if(!enVoice()&&(speechSynthesis.getVoices()||[]).length)voiceNote.firstElementChild.textContent=U().novoice||'No English voice installed.'}
async function waitVoice(h,id){
  if(!h)return true;
  const cap=Math.min(14000,Math.max(2200,h.text.length*95/rate()));let used=0;
  while(!h.done&&used<cap){
    if(id!==run)return false;
    if(paused){await new Promise(r=>setTimeout(r,60));continue}
    await new Promise(r=>setTimeout(r,50));used+=50}
  return id===run}
function stopSpeech(){speaking=false;try{speechSynthesis.cancel()}catch(e){}}

/* ---------- writing ---------- */
function clearWriting(){writing.replaceChildren()}
async function reveal(node,units,rtl,formula,id){
  let last=null;
  for(const u of units){
    if(id!==run)return false;
    if(!await tick(id))return false;
    u.style.opacity='0';node.appendChild(u);
    node.scrollIntoView({block:'nearest',behavior:FAST?'auto':'smooth'});
    if(!FAST){
      const p=tipOf(u,rtl);
      if(last&&!await glide(last,p,id,110))return false;
      u.style.opacity='1';handAtClient(p.x,p.y);last=p;activeAnchor={node:u,rtl};
      const len=(u.textContent||'').trim().length;
      if(!len){last=p;continue}
      if(!await wait(Math.max(formula?140:170,len*(formula?55:60)),id))return false}
    else u.style.opacity='1'}
  return true}
async function writeStep(step,id){
  const formula=step.t==='formula';
  const rtl=!formula&&cur()==='ar';
  const node=document.createElement('div');
  node.className='nb-step'+(formula?' nb-formula':'');
  node.dir=formula?'ltr':(rtl?'rtl':'ltr');
  if(step.label&&!formula){const lb=document.createElement('span');lb.className='nb-label';lb.textContent=tr(step.label);node.appendChild(lb)}
  if(step.hint&&!formula){const hc=document.createElement('span');hc.className='nb-hintchip';hc.textContent='💡 '+tr(step.hint);node.appendChild(hc)}
  writing.appendChild(node);
  node.scrollIntoView({block:'nearest',behavior:FAST?'auto':'smooth'});
  const text=formula?step.text:tr(step.text);
  const ar=arOn?arTextOf(step):'';
  const h=(formula&&!step.speech)?null:speakText(step.speech,id,ar,step.speech_lang);
  if(!FAST){placeHandAtNode(node,rtl);if(!await wait(300,id))return false}
  if(!await reveal(node,unitsOf(text,rtl,formula),rtl,formula,id))return false;
  if(arOn&&!formula&&cur()!=='ar'){
    const an=document.createElement('div');an.className='nb-ar';an.dir='rtl';writing.appendChild(an);
    if(ar){if(!await reveal(an,unitsOf(ar,true,false),true,false,id))return false}
    else{an.textContent=U().ar_missing||''}}
  if(!await waitVoice(h,id))return false;
  return true}

/* ---------- drawing library (approved V6 actions + generic) ---------- */
function el(tag,attrs,txt){const e=document.createElementNS(NS,tag);Object.entries(attrs||{}).forEach(([k,v])=>e.setAttribute(k,v));if(txt)e.textContent=txt;ink.appendChild(e);return e}
function label(text,x,y,color){el('text',{x,y,'font-size':27,fill:color||'#263b50','font-weight':'bold'},text)}
async function drawLine(x1,y1,x2,y2,color,id,dash){
  const e=el('line',{x1,y1,x2,y2,stroke:color,'stroke-width':4,'stroke-linecap':'round','stroke-dasharray':dash||''});
  const n=FAST?1:32;
  for(let i=0;i<=n;i++){
    if(id!==run)return false;
    e.setAttribute('x2',x1+(x2-x1)*i/n);e.setAttribute('y2',y1+(y2-y1)*i/n);
    svgPoint(x1+(x2-x1)*i/n,y1+(y2-y1)*i/n);
    if(!await wait(22,id))return false}
  return true}
const CUBE={A:[285,330],B:[455,330],C:[455,500],D:[285,500],E:[385,240],F:[555,240],G:[555,410],H:[385,410]};
async function cubePath(points,color,id,fill){
  const d='M'+points.map(p=>p.join(',')).join(' L')+' Z';
  const poly=el('path',{d,fill:fill||'none',stroke:color,'stroke-width':3.4,'stroke-linejoin':'round'});
  if(fill&&fill!=='none'){poly.setAttribute('fill-opacity','0');const n=FAST?1:25;
    for(let i=0;i<=n;i++){poly.setAttribute('fill-opacity',String(i/n*.85));if(!await wait(26,id))return}}
  return poly}
async function cubeOutline(id,a){
  const p=CUBE;
  for(const [x,y] of [['A','B'],['B','C'],['C','D'],['D','A'],['A','E'],['E','F'],['F','B'],['F','G'],['G','C'],['D','H']])
    if(!await drawLine(...p[x],...p[y],'#156fa9',id))return;
  await drawLine(...p.E,...p.H,'#8ba5b6',id,'8 7');await drawLine(...p.H,...p.G,'#8ba5b6',id,'8 7');
  label((a&&a.label)||'a',365,520,'#156fa9')}
async function cubeColor(id){
  const p=CUBE;
  await cubePath([p.A,p.B,p.C,p.D],'#d85870',id,'#e8798c');
  await cubePath([p.E,p.F,p.B,p.A],'#246fa8',id,'#8cc8f5');
  await cubePath([p.B,p.F,p.G,p.C],'#2b9979',id,'#75d9ad')}
async function cubeRotate(id){
  const g=el('g',{transform:'translate(420 375)'});
  const pts=[[-85,-65],[85,-65],[85,105],[-85,105],[-5,-145],[165,-145],[165,25]];
  for(const sh of [{ix:[0,1,2,3],c:'#e8798c'},{ix:[4,5,1,0],c:'#8cc8f5'},{ix:[1,5,6,2],c:'#75d9ad'}]){
    const e=document.createElementNS(NS,'path');e.setAttribute('d','M'+sh.ix.map(i=>pts[i].join(',')).join(' L')+' Z');
    e.setAttribute('fill',sh.c);e.setAttribute('stroke','#156fa9');e.setAttribute('stroke-width','3');g.appendChild(e)}
  const n=FAST?1:75;
  for(let i=0;i<=n;i++){
    if(id!==run)return;
    const a=i/n*42;
    g.setAttribute('transform','translate(420 375) rotate('+a+') scale('+(1-.07*Math.sin(i/n*Math.PI))+')');
    svgPoint(420+110*Math.cos(a*Math.PI/180),375+110*Math.sin(a*Math.PI/180));
    if(!await wait(32,id))return}}
async function cubeUnfold(id){
  const colors=['#e8798c','#8cc8f5','#75d9ad','#f6c66a','#b49cf0','#9dd6e5'];
  const sq=[[345,340],[445,340],[245,340],[145,340],[345,240],[345,440]];
  const nodes=sq.map((s,k)=>el('rect',{x:420,y:375,width:5,height:5,rx:2,fill:colors[k],stroke:'#156fa9','stroke-width':3,'fill-opacity':'.78'}));
  const n=FAST?1:75;
  for(let i=0;i<=n;i++){
    if(id!==run)return;
    const t=i/n,e=t*t*(3-2*t);
    nodes.forEach((nd,k)=>{const [x,y]=sq[k];nd.setAttribute('x',420+(x-420)*e);nd.setAttribute('y',375+(y-375)*e);nd.setAttribute('width',5+95*e);nd.setAttribute('height',5+95*e)});
    svgPoint(420+(sq[0][0]-420)*e,375+(sq[0][1]-375)*e);
    if(!await wait(35,id))return}
  label('Net of a Cube',295,205)}
/* Power factors: one box per factor, drawn by the pen, then the value */
async function powerFactors(id,a){
  const base=String(a.base),n=Math.max(1,Math.min(12,parseInt(a.exp,10)||1));
  const per=n>6?Math.ceil(n/2):n,bw=76,gap=34,x0=440-(per*bw+(per-1)*gap)/2;
  label(a.title||(base+' ^ '+n),x0,170,'#7a3fb0');
  for(let i=0;i<n;i++){
    const row=Math.floor(i/per),col=i%per,x=x0+col*(bw+gap),y=250+row*150;
    const pts=[[x,y],[x+bw,y],[x+bw,y+90],[x,y+90],[x,y]];
    for(let k=0;k<4;k++)if(!await drawLine(...pts[k],...pts[k+1],'#156fa9',id))return;
    el('text',{x:x+bw/2,y:y+62,'font-size':44,fill:'#b42350','font-weight':'bold','text-anchor':'middle'},base);
    if(i<n-1&&col<per-1)el('text',{x:x+bw+gap/2,y:y+60,'font-size':34,fill:'#263b50','font-weight':'bold','text-anchor':'middle'},'×');
    if(!await wait(120,id))return}
  if(a.value!=null)label('= '+a.value,x0,Math.min(600,250+Math.ceil(n/per)*150+30),'#16724a')}
/* Generic figure: points in maths coordinates (y up) are scaled to the board and drawn
   segment by segment with the pen. Used by the exercise solver for geometry figures. */
async function figure(id,a){
  const pts=a.points||{},names=Object.keys(pts).filter(n=>Array.isArray(pts[n])&&pts[n].every(Number.isFinite));
  if(!names.length)return;
  let minx=Math.min(...names.map(n=>pts[n][0])),maxx=Math.max(...names.map(n=>pts[n][0])),
      miny=Math.min(...names.map(n=>pts[n][1])),maxy=Math.max(...names.map(n=>pts[n][1]));
  const circles=(a.circles||[]).filter(c=>pts[c.center]&&Number.isFinite(c.r)&&c.r>0);
  circles.forEach(c=>{const p=pts[c.center];minx=Math.min(minx,p[0]-c.r);maxx=Math.max(maxx,p[0]+c.r);miny=Math.min(miny,p[1]-c.r);maxy=Math.max(maxy,p[1]+c.r)});
  const sx=(maxx-minx)||1,sy=(maxy-miny)||1,k=Math.min(430/sx,360/sy);
  const X=x=>250+(430-sx*k)/2+(x-minx)*k,Y=y=>190+(360-sy*k)/2+(maxy-y)*k;
  const P=n=>[X(pts[n][0]),Y(pts[n][1])];
  const cx=names.reduce((t,n)=>t+X(pts[n][0]),0)/names.length,cy=names.reduce((t,n)=>t+Y(pts[n][1]),0)/names.length;
  for(const seg of a.segments||[]){
    if(!pts[seg[0]]||!pts[seg[1]])continue;
    const [x1,y1]=P(seg[0]),[x2,y2]=P(seg[1]);
    if(!await drawLine(x1,y1,x2,y2,seg[3]==='dash'?'#8ba5b6':'#156fa9',id,seg[3]==='dash'?'8 7':''))return;
    if(seg[2])el('text',{x:(x1+x2)/2+8,y:(y1+y2)/2-8,'font-size':24,fill:'#b42350','font-weight':'bold'},String(seg[2]).slice(0,24))}
  for(const c of circles){
    const [x,y]=P(c.center),r=c.r*k,e=el('circle',{cx:x,cy:y,r,fill:'none',stroke:'#156fa9','stroke-width':4}),len=2*Math.PI*r,n=FAST?1:36;
    e.setAttribute('stroke-dasharray',len);
    for(let i=0;i<=n;i++){if(id!==run)return;e.setAttribute('stroke-dashoffset',len*(1-i/n));svgPoint(x+r*Math.cos(i/n*6.283),y+r*Math.sin(i/n*6.283));if(!await wait(24,id))return}
    e.removeAttribute('stroke-dasharray')}
  for(const m of a.marks||[]){
    if(m.type==='right_angle'&&pts[m.at]&&m.between&&pts[m.between[0]]&&pts[m.between[1]]){
      const [x,y]=P(m.at),u=P(m.between[0]),v=P(m.between[1]);
      const nu=Math.hypot(u[0]-x,u[1]-y)||1,nv=Math.hypot(v[0]-x,v[1]-y)||1,d=18;
      const a1=[x+(u[0]-x)/nu*d,y+(u[1]-y)/nu*d],a2=[x+(v[0]-x)/nv*d,y+(v[1]-y)/nv*d],a3=[a1[0]+a2[0]-x,a1[1]+a2[1]-y];
      el('path',{d:'M'+a1+' L'+a3+' L'+a2,fill:'none',stroke:'#b42350','stroke-width':3})}}
  /* Property marks, the textbook convention: equal segments = same number of ticks, equal angles = same number of
     arcs, parallel = arrow heads. Each group gets its own colour so the student can match them by eye. */
  const GRP=['#d6336c','#1c7ed6','#2f9e44','#e8590c','#7048e8'];let gi=0;
  for(const m of a.marks||[]){
    const col=GRP[(Number.isInteger(m.g)?m.g:gi++)%GRP.length],cnt=Math.max(1,Math.min(4,(m.n|0)||1));
    if((m.type==='equal'||m.type==='parallel')&&Array.isArray(m.segs)){
      for(const sg of m.segs){
        if(!pts[sg[0]]||!pts[sg[1]])continue;
        const [x1,y1]=P(sg[0]),[x2,y2]=P(sg[1]),mx=(x1+x2)/2,my=(y1+y2)/2,L=Math.hypot(x2-x1,y2-y1)||1,ux=(x2-x1)/L,uy=(y2-y1)/L,nx=-uy,ny=ux;
        for(let i=0;i<cnt;i++){
          const o=(i-(cnt-1)/2)*(m.type==='equal'?9:11);
          if(m.type==='equal'){el('line',{x1:mx+ux*o-nx*11,y1:my+uy*o-ny*11,x2:mx+ux*o+nx*11,y2:my+uy*o+ny*11,stroke:col,'stroke-width':4,'stroke-linecap':'round'})}
          else{const cx0=mx+ux*o,cy0=my+uy*o;el('path',{d:'M'+(cx0-ux*7+nx*8)+' '+(cy0-uy*7+ny*8)+' L'+(cx0+ux*5)+' '+(cy0+uy*5)+' L'+(cx0-ux*7-nx*8)+' '+(cy0-uy*7-ny*8),fill:'none',stroke:col,'stroke-width':3.5,'stroke-linecap':'round','stroke-linejoin':'round'})}}}
      if(!FAST&&!await wait(220,id))return}
    else if(m.type==='equal_angle'&&pts[m.at]&&m.between&&pts[m.between[0]]&&pts[m.between[1]]){
      const [x,y]=P(m.at),u=P(m.between[0]),v=P(m.between[1]);
      let a1=Math.atan2(u[1]-y,u[0]-x),a2=Math.atan2(v[1]-y,v[0]-x),d=a2-a1;while(d>Math.PI)d-=2*Math.PI;while(d<-Math.PI)d+=2*Math.PI;
      for(let i=0;i<cnt;i++){const r=26+i*8,sw=d>0?1:0;
        el('path',{d:'M'+(x+r*Math.cos(a1))+' '+(y+r*Math.sin(a1))+' A'+r+' '+r+' 0 0 '+sw+' '+(x+r*Math.cos(a1+d))+' '+(y+r*Math.sin(a1+d)),fill:'none',stroke:col,'stroke-width':3.5,'stroke-linecap':'round'})}
      if(!FAST&&!await wait(220,id))return}}
  for(const m of a.marks||[]){
    if(m.type==='angle'&&pts[m.at]&&m.text){
      const [x,y]=P(m.at),dx=cx-x,dy=cy-y,dn=Math.hypot(dx,dy)||1;
      el('text',{x:x+dx/dn*58-22,y:y+dy/dn*58+8,'font-size':23,fill:'#7a3fb0','font-weight':'bold'},String(m.text).slice(0,8))}}
  const only=Array.isArray(a.show)?new Set(a.show):null;
  for(const n of names){
    if(only&&!only.has(n))continue;
    const [x,y]=P(n),dx=x-cx,dy=y-cy,dn=Math.hypot(dx,dy)||1;
    el('circle',{cx:x,cy:y,r:4.5,fill:'#263b50'});
    el('text',{x:x+dx/dn*26-8,y:y+dy/dn*26+8,'font-size':28,fill:'#263b50','font-weight':'bold'},(a.labels&&a.labels[n])||n);
    if(!FAST&&!await wait(80,id))return}}
/* A pre-drawn SVG scene (original lab drawings): elements are allow-listed, then revealed by id with the pen. */
const SVG_OK=new Set(['g','line','polyline','polygon','path','circle','ellipse','rect','text','tspan','defs','marker']);
function cleanSvg(node){
  [...node.children].forEach(c=>{
    if(!SVG_OK.has(c.localName)){c.remove();return}
    [...c.attributes].forEach(at=>{if(/^on/i.test(at.name)||/javascript:/i.test(at.value))c.removeAttribute(at.name)});
    cleanSvg(c)})}
let sceneG=null,sceneK=1,sceneOff=[0,0];
async function svgScene(id,a){
  if(a.svg){
    ink.replaceChildren();
    const doc=new DOMParser().parseFromString('<svg xmlns="'+NS+'">'+a.svg+'</svg>','image/svg+xml');
    if(doc.querySelector('parsererror'))return;
    cleanSvg(doc.documentElement);
    const vw=(a.vb&&a.vb[0])||660,vh=(a.vb&&a.vb[1])||440;
    sceneK=Math.min(610/vw,540/vh);sceneOff=[170+(610-vw*sceneK)/2,105+(540-vh*sceneK)/2];
    sceneG=document.createElementNS(NS,'g');
    sceneG.setAttribute('transform','translate('+sceneOff[0]+' '+sceneOff[1]+') scale('+sceneK+')');
    [...doc.documentElement.children].forEach(c=>{const n=document.importNode(c,true);n.style.opacity='0';sceneG.appendChild(n)});
    ink.appendChild(sceneG)}
  if(!sceneG)return;
  for(const sid of a.show||[]){
    const n=sceneG.querySelector('[id="'+String(sid).replace(/"/g,'')+'"]');
    if(!n||n.style.opacity==='1')continue;
    let bb=null;try{bb=n.getBBox()}catch(e){}
    if(bb)svgPoint(sceneOff[0]+sceneK*(bb.x+bb.width/2),sceneOff[1]+sceneK*(bb.y+bb.height/2));
    const geo=typeof n.getTotalLength==='function'&&!FAST?n:null;let len=0;
    try{len=geo?geo.getTotalLength():0}catch(e){len=0}
    n.style.opacity='1';
    if(len>0&&len<5000){
      n.style.strokeDasharray=len;const steps=24;
      for(let i=0;i<=steps;i++){
        if(id!==run)return;n.style.strokeDashoffset=String(len*(1-i/steps));
        try{const q=n.getPointAtLength(len*i/steps);svgPoint(sceneOff[0]+sceneK*q.x,sceneOff[1]+sceneK*q.y)}catch(e){}
        if(!await wait(22,id))return}
      n.style.strokeDasharray='';n.style.strokeDashoffset=''}
    else if(!await wait(FAST?0:260,id))return}}
const CLEARING=new Set(['cubeOutline','cubeRotate','cubeUnfold','powerFactors','figure']);
const DRAW={cubeOutline,cubeColor,cubeRotate,cubeUnfold,powerFactors,figure,svgScene};
async function doDraw(step,id){
  const fn=DRAW[step.draw];
  if(!fn)return true;
  if(step.clear!==false&&CLEARING.has(step.draw))ink.replaceChildren();
  await fn(id,step.args||{});return id===run}

/* ---------- student checks and «I did not understand» ---------- */
function showCheck(check,id){
  return new Promise(resolve=>{
    studentWait=true;
    const box=document.createElement('div');box.className='nb-check';
    const q=document.createElement('p');q.dir=cur()==='ar'?'rtl':'ltr';q.textContent=tr(check.question);
    const inp=document.createElement('input');inp.type='text';inp.setAttribute('aria-label',tr(check.question));
    const ok=document.createElement('button');ok.type='button';ok.textContent=U().check||'Check';
    const fb=document.createElement('div');fb.className='nb-fb';fb.setAttribute('aria-live','polite');
    const go=document.createElement('button');go.type='button';go.textContent=U().understood||'Continue';
    box.append(q,inp,ok,fb,go);writing.appendChild(box);box.scrollIntoView({block:'nearest'});
    const norm=s=>String(s||'').replace(/\s+/g,'').toLowerCase();
    ok.onclick=()=>{fb.textContent=(norm(inp.value)&&norm(inp.value)===norm(check.expected))?tr(check.correct_feedback||'✓'):tr(check.wrong_feedback||U().try_again||'Try again.')};
    go.onclick=()=>{studentWait=false;resolve(id===run)};
    gotUnderstood=()=>{studentWait=false;resolve(id===run)}})}
function iDidNotUnderstand(){
  if(!started||studentWait)return;
  paused=true;try{speechSynthesis.pause()}catch(e){}
  playBtn.textContent=U().resume||'▶';
  const box=document.createElement('div');box.className='nb-lost';
  const p=document.createElement('p');p.textContent=U().lost_help||'';
  const again=document.createElement('button');again.type='button';again.textContent=U().repeat_scene||'Repeat';
  const go=document.createElement('button');go.type='button';go.id='nbUnderstood';go.textContent=U().understood||'Continue';
  box.append(p,again,document.createTextNode(' '),go);writing.appendChild(box);box.scrollIntoView({block:'nearest'});
  go.onclick=()=>{box.remove();resume()};
  again.onclick=()=>{box.remove();goTo(index)}}

/* ---------- lesson flow ---------- */
function relabel(){
  root.querySelectorAll('[data-nb-l]').forEach(n=>{const v=U()[n.dataset.nbL];if(v)n.textContent=v});
  voiceBtn.textContent=voice?(U().voice_on||'🔊'):(U().voice_off||'🔇');
  arBtn.textContent=arOn?(U().ar_voice_on||'🔊'):(U().ar_voice||'🔈');
  playBtn.textContent=(started&&!paused&&!finished)?(U().pause||'⏸'):(started&&paused?(U().resume||'▶'):(U().play||'▶'))}
function setStatus(){
  progEl.textContent=index<FINAL?((index+1)+' / '+FINAL):'✓';
  statusEl.textContent=paused?(U().paused||'Paused'):(U().playing||'')}
async function playScene(startStep){
  startStep=startStep|0;
  const id=++run;paused=false;studentWait=false;finished=false;golden.classList.remove('on');workspace.style.display='';
  if(INTER&&index>=FINAL){hideHand();stopSpeech();showInterludeEnd();return}   /* keep the finished solution on the board */
  if(!startStep){ink.replaceChildren();clearWriting();marks=[]}
  hideHand();stopSpeech();
  if(index>=FINAL){if(INTER){showInterludeEnd();return}showFinal();return}
  relabel();
  const sc=SCENES[index];
  if(exSel&&!INTER)exSel.value=sc.exercise?String(index):'';
  headTitle.textContent=tr(sc.title||DATA.title);setStatus();playBtn.textContent=U().pause||'⏸';
  setBoardMode(sc.start_mode||'single');
  curStepNo=startStep;
  for(let si=startStep;si<sc.steps.length;si++){
    const step=sc.steps[si];
    if(id!==run)return;
    marks[si]=writing.childNodes.length;
    curStepNo=si+1;
    if(step.t==='text'||step.t==='formula'){if(!await writeStep(step,id))return}
    else if(step.t==='draw'){setBoardMode('dual',{preserveState:true});await new Promise(r=>requestAnimationFrame(r));if(!await doDraw(step,id))return}
    else if(step.t==='mode'){setBoardMode(step.mode,{preserveState:true})}
    else if(step.t==='check'&&step.check){if(!await showCheck(step.check,id))return}
    if(!await wait(300,id))return}
  hideHand();
  if(!await wait(FAST?0:(INTER?600:1800),id))return;
  if(id===run){index++;playScene()}}
/* ---------- interlude: run another set of scenes (a solved exercise) on this same board ---------- */
function showInterludeEnd(){
  index=FINAL;finished=true;hideHand();stopSpeech();playBtn.textContent=U().play||'▶';paused=true;
  const box=document.createElement('div');box.className='nb-check';box.id='nbSolveDone';
  const p=document.createElement('p');p.dir=cur()==='ar'?'rtl':'ltr';p.textContent=U().solve_done||'✓';
  const back=document.createElement('button');back.type='button';back.textContent=U().back_to_lesson||'Back to the lesson';back.onclick=leaveInterlude;
  const again=document.createElement('button');again.type='button';again.textContent=U().replay||'Replay';again.onclick=()=>{finished=false;goTo(0)};
  box.append(p,back,document.createTextNode(' '),again);writing.appendChild(box);box.scrollIntoView({block:'nearest'});setStatus()}
function enterInterlude(scenes,opts){
  if(!Array.isArray(scenes)||!scenes.length)return false;
  if(!INTER){
    const wf=document.createDocumentFragment(),inkf=document.createDocumentFragment();
    if(started&&!finished){while(writing.firstChild)wf.appendChild(writing.firstChild);while(ink.firstChild)inkf.appendChild(ink.firstChild)}
    saved={SC:SCENES,FIN:FINAL,index,started,finished,wf,inkf,step:curStepNo,marks:marks.slice(),mode:boardMode,title:headTitle.textContent}}
  run++;stopSpeech();hideHand();
  INTER=opts||{};SCENES=scenes;FINAL=scenes.length;
  started=true;paused=false;finished=false;root.classList.add('nb-active','nb-solving');root.classList.remove('is-final');
  golden.classList.remove('on');workspace.style.display='';ink.replaceChildren();clearWriting();marks=[];
  index=0;playScene();return true}
function leaveInterlude(){
  if(!INTER||!saved)return;
  const s=saved;INTER=null;saved=null;run++;stopSpeech();hideHand();
  SCENES=s.SC;FINAL=s.FIN;root.classList.remove('nb-solving');golden.classList.remove('on');workspace.style.display='';
  if(!s.started){started=false;finished=false;root.classList.remove('nb-active');clearWriting();ink.replaceChildren();return}
  index=s.index;
  if(s.finished){root.classList.remove('is-final');showFinal();return}
  clearWriting();ink.replaceChildren();writing.appendChild(s.wf);ink.appendChild(s.inkf);marks=s.marks;
  setBoardMode(s.mode,{preserveState:true});
  const k=Math.max(0,s.step-1);
  while(writing.childNodes.length>(marks[k]!==undefined?marks[k]:writing.childNodes.length))writing.lastChild.remove();
  headTitle.textContent=s.title;paused=false;playScene(k)}
function repeatStep(){
  if(!started)return;
  const k=Math.max(0,curStepNo-1);
  run++;stopSpeech();hideHand();finished=false;
  while(writing.childNodes.length>(marks[k]!==undefined?marks[k]:writing.childNodes.length))writing.lastChild.remove();
  paused=false;playScene(k)}
function showFinal(){
  index=FINAL;finished=true;root.classList.add('is-final');hideHand();stopSpeech();setBoardMode('single');
  headTitle.textContent=DATA.title;progEl.textContent='✓';
  workspace.style.display='none';golden.classList.add('on');golden.replaceChildren();
  if(exSel)exSel.value='';
  if(!DATA.golden||!DATA.golden.sections){golden.textContent=U().done||'✓';playBtn.textContent=U().play||'▶';paused=true;return}
  const host=document.createElement('div');host.id='goldenReferenceCard';host.setAttribute('data-nabil-v18-golden','true');golden.appendChild(host);
  try{const g=Object.assign({},DATA.golden,{language:LANG,avatar_src:avatarUrl||''});
    (window.__NABIL_V18_CARDS||window.NABILScientificCards).fromLesson(g,host);enhanceDom(host)}catch(e){host.textContent=String(e)}
  playBtn.textContent=U().play||'▶';paused=true}
function stop(){run++;stopSpeech();hideHand();paused=false;playBtn.textContent=U().play||'▶'}
function goTo(i){if(!started){started=true;root.classList.add('nb-active')}stop();root.classList.remove('is-final');index=Math.max(0,Math.min(FINAL,i|0));paused=false;playScene()}
function pause(){if(!started||paused)return;paused=true;try{speechSynthesis.pause()}catch(e){}playBtn.textContent=U().resume||'▶';setStatus()}
function resume(){
  if(!started)return;
  paused=false;
  try{
    if(speechSynthesis.paused)speechSynthesis.resume();
    else if(voice&&lastText&&!speechSynthesis.speaking&&speaking){/* engine dropped the utterance: re-speak current step */ speakText(lastText,run)}
  }catch(e){}
  playBtn.textContent=U().pause||'⏸';setStatus()}
function begin(){
  started=true;root.classList.add('nb-active');
  try{const r=root.requestFullscreen&&root.requestFullscreen();if(r&&r.catch)r.catch(()=>{})}catch(e){}
  /* the click is the user gesture that also unlocks speech on mobile browsers */
  try{if(voice&&!FAST){const u=new SpeechSynthesisUtterance(' ');u.volume=0;speechSynthesis.speak(u)}}catch(e){}
  index=0;playScene()}
startBtn.onclick=begin;avatarOpen.onclick=begin;
playBtn.onclick=()=>{if(!started){begin();return}if(finished){goTo(0);return}paused?resume():pause()};
prevBtn.onclick=()=>goTo(Math.max(0,index-1));
nextBtn.onclick=()=>goTo(Math.min(FINAL,index+1));
replayBtn.onclick=()=>goTo(0);
lostBtn.onclick=iDidNotUnderstand;
voiceBtn.onclick=()=>{voice=!voice;voiceBtn.textContent=voice?(U().voice_on||'🔊'):(U().voice_off||'🔇');
  voiceBtn.setAttribute('aria-pressed',String(voice));
  if(!voice)stopSpeech();else if(lastText&&started&&!paused)speakText(lastText,run)};
arBtn.onclick=()=>{arOn=!arOn;arBtn.setAttribute('aria-pressed',String(arOn));
  arBtn.textContent=arOn?(U().ar_voice_on||'🔊'):(U().ar_voice||'🔈');
  if(!arOn&&!voice)stopSpeech()};
if(exSel)exSel.onchange=()=>{if(exSel.value!=='')goTo(+exSel.value)};
speedSel.onchange=()=>{speed=+speedSel.value};
voiceNote.querySelector('button').onclick=()=>{voiceNote.classList.remove('on');if(lastText)speakText(lastText,run)};
fsBtn.onclick=()=>{try{if(document.fullscreenElement)document.exitFullscreen();else root.requestFullscreen&&root.requestFullscreen().catch(()=>{})}catch(e){}};
exitBtn.onclick=()=>{stop();started=false;root.classList.remove('nb-active');try{document.fullscreenElement&&document.exitFullscreen()}catch(e){}};
document.addEventListener('visibilitychange',()=>{if(document.hidden&&started&&!paused)pause()});

{const bd=$('nbBadge'),st=DATA.meta&&DATA.meta.status_text;if(bd&&st){bd.textContent='⚠ '+st;bd.hidden=false;bd.dir=LANG==='ar'?'rtl':'ltr'}}
const toolsBtn=$('nbToolsToggle'),toolsBar=$('nbTools'),repBtn=$('nbRepeatStep'),backBtn=$('nbBackToLesson');
if(toolsBtn&&toolsBar)toolsBtn.onclick=()=>{const open=toolsBar.hidden;toolsBar.hidden=!open;toolsBtn.setAttribute('aria-expanded',String(open))};
if(repBtn)repBtn.onclick=repeatStep;
if(backBtn)backBtn.onclick=leaveInterlude;
window.NABILWholeLessonOrchestrator={
  enterInterlude,leaveInterlude,repeatStep,inInterlude:()=>!!INTER,
  play(){if(!started)begin();else if(paused)resume();else if(finished)goTo(0)},
  pause,resume,stop,
  current(){return SCENES[index]||null},
  sceneAt(i){return(saved?saved.SC:SCENES)[i]||null},
  goTo,next(){goTo(Math.min(FINAL,index+1))},prev(){goTo(Math.max(0,index-1))},
  setBoardMode,
  modeLog:()=>modeLog.slice(),
  state(){return{index,paused,started,final:finished,boardMode,voice,speed,speaking,scenes:FINAL,studentWait,
    handVisible:hand.classList.contains('is-visible')}},
  finalIndex:FINAL};
window.NABILGoldenV6={version:'V6',context:()=>({lang:LANG,title:DATA.title,exercises:(DATA.exercises||[]).map(e=>({n:e.n,scene:e.scene,solved:e.solved})),meta:DATA.meta||{}}),boardMode:()=>boardMode,setBoardMode,cur,tr};
})();
