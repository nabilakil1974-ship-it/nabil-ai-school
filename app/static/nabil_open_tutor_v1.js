/* NABIL open tutor v5 — the blue robot is the only landing page.
   Spoken and typed questions use the SAME /api/chat reasoning path, renderer and TTS.
   Open mode is intentionally independent from grade/subject/lesson selectors.
*/
(()=>{
"use strict";
const el=id=>document.getElementById(id);
const home=el("nabilHome"), main=document.querySelector(".lesson-main-column"), chat=el("chat");
if(!home||!main||!chat)return;

// Remove the obsolete separate gateway if legacy HTML created it before this script.
el("nabilProfessorGateway")?.remove();
const gatewayStyle=el("nabil-v105-startup-style");
if(gatewayStyle)gatewayStyle.disabled=true;

// The landing page never asks for a grade. Grade/subject/language/lesson remain
// available only after the learner explicitly enters the lesson page.
const stage=el("homeStage");
if(stage){stage.replaceChildren();stage.hidden=true;}

const card=document.createElement("section");
card.id="nabilOpenTutor";
card.setAttribute("aria-label","NABIL AI — open tutor");
card.innerHTML=
 '<div class="nabil-open-head">'+
   '<img class="nabil-open-mini-avatar" src="/static/nabil-profile.jpg" alt="NABIL AI robot">'+
   '<div><h2>أهلًا! أنا الأستاذ نبيل 👋</h2>'+
   '<p>اسألني مباشرة كتابةً أو صوتًا. بفهم اللبناني، English وFrançais، وبجاوب بلغة السؤال.</p></div>'+
 '</div>'+
 '<div id="nabilOpenConversation" class="nabil-open-conversation" aria-live="polite">'+
   '<div class="nabil-open-welcome">جاهز نحل ونشرح ونرسم سوا — من دون اختيار صف أو مادة.</div>'+
 '</div>'+
 '<div id="nabilOpenAnswer" aria-label="بطاقة جواب الأستاذ نبيل">'+
   '<div id="nabilOpenLiveType" class="nabil-open-live-type" hidden aria-live="polite"></div>'+
   '<div id="nabilOpenExplanation" class="nabil-open-explanation"></div>'+
   '<div id="nabilOpenVisuals" class="nabil-open-visuals" hidden></div>'+
   '<div id="nabilOpenTools" class="nabil-open-tools"></div>'+
   '<div id="nabilOpenAnswerNav" class="nabil-open-answer-nav" hidden>'+
     '<button id="nabilOpenExplainBtn" type="button">📘 عرض الشرح</button>'+
     '<button id="nabilOpenVisualBtn" type="button" hidden>📐 عرض الرسمة</button>'+
   '</div>'+
 '</div>'+
 '<div class="nabil-open-composer">'+
   '<textarea id="nabilOpenInput" rows="2" placeholder="اكتب سؤالك هنا… / Type your question… / Écris ta question…"></textarea>'+
   '<button id="nabilOpenTalk" type="button" title="سؤال صوتي">🎙️ سؤال صوتي</button>'+
   '<button id="nabilOpenSend" type="button">➤ إرسال</button>'+
 '</div>'+
 '<label class="nabil-open-pace" for="nabilOpenPace">🔊 سرعة الشرح <input id="nabilOpenPace" aria-label="سرعة صوت الأستاذ نبيل" type="range" min="0.70" max="1.15" step="0.05" value="0.90"><output id="nabilOpenPaceValue">0.90×</output></label>'+ 
 '<div id="nabilOpenStatus" role="status" aria-live="polite">جاهز لسؤالك.</div>';

let homeHost=el("nabilHomeTutorHost");
if(!homeHost){homeHost=document.createElement("div");homeHost.id="nabilHomeTutorHost";home.appendChild(homeHost);}
homeHost.replaceChildren(card);

const status=el("nabilOpenStatus"), board=el("nabilOpenAnswer"), convo=el("nabilOpenConversation"),
      input=el("nabilOpenInput"), talk=el("nabilOpenTalk"), send=el("nabilOpenSend"),
      nav=el("nabilOpenAnswerNav"), explainBtn=el("nabilOpenExplainBtn"), visualBtn=el("nabilOpenVisualBtn"),
      explanation=el("nabilOpenExplanation"), visuals=el("nabilOpenVisuals"), toolsHost=el("nabilOpenTools"), liveType=el("nabilOpenLiveType");
let recorder=null,stream=null,chunks=[],recording=false,busy=false,openConversationId="";
/* Figure preview must always have working close controls after dynamic
   answer-card rerenders, including Escape and tapping outside the dialog. */
const drawingModal=el("drawingPreviewModal");
if(drawingModal&&!drawingModal.dataset.nabilCloseBound){
 drawingModal.dataset.nabilCloseBound="1";
 const closeFigure=()=>{drawingModal.hidden=true;el("drawingPreviewContent")?.replaceChildren()};
 el("closeDrawingPreviewBtn")?.addEventListener("click",closeFigure);
 drawingModal.addEventListener("click",e=>{
   if(e.target===drawingModal)closeFigure();
 });
 document.addEventListener("keydown",e=>{
   if(e.key==="Escape"&&!drawingModal.hidden)closeFigure();
 });
}

let greetingSpoken=false;
const pace=el("nabilOpenPace"),paceValue=el("nabilOpenPaceValue");
try{
 const saved=Number(localStorage.getItem("nabil_voice_pace"));
 if(Number.isFinite(saved)&&saved>=0.7&&saved<=1.15)pace.value=String(saved);
}catch(_e){}
function syncPace(){
 const v=Math.max(0.7,Math.min(1.15,Number(pace.value)||0.9));
 window.nabilVoicePace=v;
 paceValue.textContent=v.toFixed(2)+"×";
 try{if(typeof nabilNeuralAudio!=="undefined"&&nabilNeuralAudio)nabilNeuralAudio.playbackRate=v}catch(_e){}
 try{localStorage.setItem("nabil_voice_pace",String(v))}catch(_e){}
}
pace.addEventListener("input",syncPace);
syncPace();
function speakGreetingOnce(){
 if(greetingSpoken||home.style.display==="none")return;
 greetingSpoken=true;
 const greeting="أهلًا وسهلًا. أنا الأستاذ نبيل. اسألني كتابة أو صوت، وبشرحلك وبحل معك خطوة خطوة.";
 try{
   const spoken=typeof nabilBoardPlainSpeech==="function"?nabilBoardPlainSpeech(greeting):greeting;
   if(typeof nabilSpeakClear==="function")Promise.resolve(nabilSpeakClear(spoken,"العربية",{})).catch(()=>{});
 }catch(_e){}
}

const setStatus=(t,error=false)=>{status.textContent=t;status.classList.toggle("error",!!error)};
const setBusy=x=>{busy=x;send.disabled=x;talk.disabled=x&&!recording;card.classList.toggle("is-busy",x)};
const escapeHTML=t=>String(t??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));

/* A data-faithful, scalable 3D-perspective SVG if the legacy renderer does not
   support sphere. Use ONLY the radius already validated by the backend. */
function renderVerifiedSphereFallback(d){
 if(String(d?.type||"").toLowerCase()!=="sphere")return "";
 const radius=Number(d.radius);
 if(!Number.isFinite(radius)||radius<=0||radius>=1000000)return "";
 const label=String(d.radius_label||d.labels?.radius||("r = "+radius.toString()));
 const title=escapeHTML(String(d.title||"Sphere"));
 const safeLabel=escapeHTML(label);
 return '<svg class="nabil-open-sphere-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 680 520" role="img" aria-label="'+title+", "+safeLabel+'">'+
  '<defs><radialGradient id="nabilSphereFill" cx="32%" cy="26%" r="76%"><stop stop-color="#74d9ff"/><stop offset=".52" stop-color="#2482d9"/><stop offset="1" stop-color="#082b58"/></radialGradient></defs>'+
  '<rect width="680" height="520" rx="22" fill="#081e33"/>'+
  '<circle cx="340" cy="245" r="172" fill="url(#nabilSphereFill)" stroke="#53cbff" stroke-width="3"/>'+
  '<path d="M168 245 A172 57 0 0 1 512 245" fill="none" stroke="#e0f7ff" stroke-width="2" stroke-dasharray="8 7" opacity=".8"/>'+
  '<path d="M168 245 A172 57 0 0 0 512 245" fill="none" stroke="#d8f6ff" stroke-width="3"/>'+
  '<circle cx="340" cy="245" r="5" fill="#fff"/>'+
  '<line x1="340" y1="245" x2="512" y2="245" stroke="#ffdb54" stroke-width="4"/>'+
  '<circle cx="512" cy="245" r="5" fill="#ffdb54"/>'+
  '<text x="328" y="231" fill="#fff" font-size="23" text-anchor="end">O</text>'+
  '<text x="425" y="221" fill="#ffeb87" font-size="23" text-anchor="middle" direction="ltr">'+safeLabel+'</text>'+
  '</svg>';
}


/* A verified-series fallback when the older lesson diagram renderer returns
   markup without an actual image. Coordinates are taken ONLY from backend
   validated numeric data. No invented point, radius or dimension. */
function renderVerifiedCoordinateFallback(d){
 if(!["coordinate_plane","function","graph"].includes(String(d?.type||"").toLowerCase()))return "";
 const series=(d.series||[]).map(part=>Array.isArray(part)?part:part?.points||[]);
 if(!series.some(part=>part.length>=2))return "";
 const xmin=Number(d.xmin??d.x_min),xmax=Number(d.xmax??d.x_max);
 const ymin=Number(d.ymin??d.y_min),ymax=Number(d.ymax??d.y_max);
 if(![xmin,xmax,ymin,ymax].every(Number.isFinite)||xmin>=xmax||ymin>=ymax)return "";
 const left=44,top=25,width=570,height=375;
 const px=x=>left+(Number(x)-xmin)*width/(xmax-xmin);
 const py=y=>top+height-(Number(y)-ymin)*height/(ymax-ymin);
 const fmt=n=>Math.round(n*100)/100;
 let shapes='<rect width="680" height="440" fill="#081e33"/>';
 const stroke='#85bdd4';
 if(xmin<=0&&xmax>=0)shapes+='<line x1="'+fmt(px(0))+'" x2="'+fmt(px(0))+'" y1="'+top+'" y2="'+(top+height)+'" stroke="'+stroke+'"/>';
 if(ymin<=0&&ymax>=0)shapes+='<line x1="'+left+'" x2="'+(left+width)+'" y1="'+fmt(py(0))+'" y2="'+fmt(py(0))+'" stroke="'+stroke+'"/>';
 (d.vertical_asymptotes||[]).forEach(item=>{
   const x=Number(item?.x??item);if(!Number.isFinite(x)||x<xmin||x>xmax)return;
   shapes+='<line x1="'+fmt(px(x))+'" x2="'+fmt(px(x))+'" y1="'+top+'" y2="'+(top+height)+'" stroke="#ff7b82" stroke-width="2" stroke-dasharray="8 5"/>';
 });
 series.forEach((part,index)=>{
  let pts=part.filter(v=>Array.isArray(v)&&v.length>=2&&Number.isFinite(Number(v[0]))&&Number.isFinite(Number(v[1]))&&v[0]>=xmin&&v[0]<=xmax&&v[1]>=ymin&&v[1]<=ymax);
  if(pts.length<2)return;
  const points=pts.map(v=>fmt(px(v[0]))+','+fmt(py(v[1]))).join(' ');
  const color=index%2===0?'#39c9ff':'#ffd66a';
  shapes+='<polyline points="'+points+'" fill="none" stroke="'+color+'" stroke-width="3"/>';
 });
 (d.markers||[]).forEach(pt=>{
   const x=Number(pt.x),y=Number(pt.y);
   if(!Number.isFinite(x)||!Number.isFinite(y)||x<xmin||x>xmax||y<ymin||y>ymax)return;
   shapes+='<circle cx="'+fmt(px(x))+'" cy="'+fmt(py(y))+'" r="4" fill="#ffdb60"/>';
   if(pt.label)shapes+='<text x="'+fmt(px(x)+7)+'" y="'+fmt(py(y)-8)+'" fill="#ffffff" font-size="13">'+escapeHTML(String(pt.label))+'</text>';
 });
 return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 680 440" role="img" aria-label="'+escapeHTML(String(d.title||"Verified function graph"))+'">'+shapes+'</svg>';
}

function detectLanguage(q){
 const t=String(q||"").trim();
 // Technical school content dominates a casual Lebanese interjection.
 // The teaching voice must not switch to Arabic merely because a learner
 // starts with "بدي" or says "هلق" in an English/French lesson.
 const french=/\b(bonjour|explique|étudie|etudie|fonction|dérivée|derivee|tracer|courbe|résoudre|resoudre|dessine|dessiner|calcule|montrer|démontrer|demontrer|rayon|sphère|domaine|limite|numérateur|denominateur|dénominateur|croissante|décroissante|schéma|exercice)\b/i;
 if(french.test(t))return "Français";
 const english=/\b(study|function|numerator|denominator|derivative|increasing|decreasing|domain|limit|graph|draw|sphere|radius|physics|chemistry|biology|voltage|current|resistance|exercise|equation|fraction|asymptote|variation|solve|explain|please|show|figure)\b/i;
 if(english.test(t))return "English";
 const arWords=(t.match(/[\u0600-\u06ff]+/g)||[]).length;
 const foreignWords=(t.match(/[a-zà-ÿ]{2,}/gi)||[]).length;
 if(foreignWords>arWords)return "English";
 if(arWords)return "العربية";
 if(foreignWords)return "English";
 return "العربية";
}
function addLine(role,text){
 if(!text)return;
 const row=document.createElement("div");
 row.className="nabil-open-line "+role;
 const lang=detectLanguage(text);
 row.dir=lang==="العربية"?"rtl":"ltr";
 row.lang=lang==="العربية"?"ar":lang==="English"?"en":"fr";
 const who=document.createElement("strong");
 who.textContent=role==="student"?(lang==="English"?"Student: ":lang==="Français"?"Élève : ":"الطالب: "):(lang==="English"?"NABIL: ":lang==="Français"?"NABIL : ":"الأستاذ نبيل: ");
 row.append(who,document.createTextNode(String(text)));
 convo.appendChild(row);
 convo.scrollTop=convo.scrollHeight;
}
function prepareSpeechTypewriter(text,lang){
 const words=String(text||"").replace(/\s+/g," ").trim().split(" ").filter(Boolean);
 let timer=0,index=0,duration=0,started=false;
 const dir=lang==="العربية"?"rtl":"ltr";
 liveType.dir=dir;liveType.lang=lang==="العربية"?"ar":lang==="English"?"en":"fr";
 liveType.textContent="";liveType.hidden=!words.length;
 const interval=()=>duration>0?Math.max(55,Math.min(420,(duration*1000)/Math.max(words.length,1))):Math.max(75,Math.round(245/(Number(window.nabilVoicePace)||0.9)));
 const tick=()=>{
  if(index>=words.length){finish();return}
  liveType.textContent+=(index?" ":"")+words[index++];
  timer=window.setTimeout(tick,interval());
 };
 const start=()=>{if(started||!words.length)return;started=true;tick()};
 const finish=()=>{if(timer)clearTimeout(timer);timer=0;liveType.textContent=words.join(" ");window.setTimeout(()=>{liveType.hidden=true},700)};
 return {start,finish,setDuration:d=>{if(Number.isFinite(Number(d))&&Number(d)>0)duration=Number(d)}};
}

function renderAnswer(result,question){
 const rawReply=String(result?.reply||"").trim();
 // Defence in depth while a rolling Railway deploy may serve an old backend:
 // no internal drawing transport belongs in student-visible HTML or speech.
 const cleanReply=rawReply
   .replace(/<_?DRAWINGS?_JSON>[\s\S]*?<\/DRAWINGS?_JSON>/gi,"")
   .replace(/(?:^|\n)\s*DRAWINGS?_JSON\s*[:：][\s\S]*$/i,"")
   .replace(/```(?:json|nabil-draw)\s*[\[{][\s\S]*?```/gi,"")
   .replace(/^\s*(?:Let's check the drawing requirements|The drawing must contain|Below are the sketches for each exercise|"?(?:scope|exercise_index|card_index|color|type)"?\s*:).*$/gmi,"")
   .replace(/\n{3,}/g,"\n\n").trim();
 const drawings=Array.isArray(result?.drawings)?result.drawings.slice():[];
 const questionText=String(question||"");
 const sphereMatch=/\b(?:sphere|sph[èe]re)\b|كرة/i.test(questionText)
   && questionText.match(/(?:\bradius\b|\brayon\b|نصف\s*القطر|نصف\s*قطر)\s*(?:equal\s+to|égal\s+à|egal\s+a|يساوي|=|:|of|de)?\s*(\d+(?:[.,]\d+)?)\s*(cm|mm|m)?\b/i);
 const exactRadius=sphereMatch?Number(sphereMatch[1].replace(",",".")):NaN;
 if(!drawings.length&&Number.isFinite(exactRadius)&&exactRadius>0&&exactRadius<1000000
    &&/\b(?:draw|figure|sketch|dessin(?:er)?|tracer)\b|ارسم|رسمة|الرسم|الشكل/i.test(questionText)){
   const unit=sphereMatch[2]||"";
   drawings.push({type:"sphere",radius:exactRadius,radius_label:"r = "+exactRadius+(unit?" "+unit:""),title:"Sphere"});
 }
 const visualOnlyRequested=/\b(?:only\s+the\s+(?:figure|drawing|graph)|figure\s+only|just\s+(?:the\s+)?(?:figure|drawing)|draw\s+only|seulement\s+(?:la\s+)?figure|dessin\s+seulement)\b|(?:الرسمة|الرسم|الشكل)\s*(?:فقط|بس)|(?:فقط|بس)\s*(?:الرسمة|الرسم|الشكل)/i.test(questionText);
 const figureOnly=drawings.length>0&&(visualOnlyRequested||!cleanReply);
 const reply=figureOnly?"":cleanReply;
 if(!reply&&!drawings.length)throw Error("الخادم لم يرجع جوابًا صالحًا.");
 const lang=detectLanguage(reply&&detectLanguage(reply)!=="العربية"?reply:(question||result?.transcribed_text||reply));
 const dir=lang==="العربية"?"rtl":"ltr";
 board.dir=dir;
 board.lang=lang==='العربية'?'ar':lang==='English'?'en':'fr';
 board.classList.add("has-answer");
 explanation.replaceChildren();
 visuals.replaceChildren();
 toolsHost.replaceChildren();

 // Same academic renderer used by the lesson page. Keep text and drawings in
 // separate panes so the learner can switch between explanation and figure.
 let text=document.createElement("div");
 text.className="nabil-open-answer-text";
 text.dir=dir;
 text.lang=board.lang;
 try{
   if(typeof renderAIText==="function")text.innerHTML=renderAIText(reply);
   else text.innerHTML="<div>"+escapeHTML(reply).replace(/\n/g,"<br>")+"</div>";
 }catch(_e){text.innerHTML="<div>"+escapeHTML(reply).replace(/\n/g,"<br>")+"</div>"}
 // The shared Markdown renderer can return an empty fragment for unusual
 // model output. Never silently hide the solution when the reply exists.
 if(reply&&!(text.textContent||"").trim()&&!text.querySelector("svg,canvas,img,mjx-container")){
   text.innerHTML="<div>"+escapeHTML(reply).replace(/\n/g,"<br>")+"</div>";
 }
 // Math and tables belong in the formatted solution, not in a raw transcript.
 if(!figureOnly)explanation.appendChild(text);

 drawings.forEach(d=>{
   try{
     const primary=typeof renderNabilDiagram==="function"?(renderNabilDiagram(d)||""):"";
     const html=/<(?:svg|canvas|img)\b/i.test(primary)?primary:(renderVerifiedSphereFallback(d)||renderVerifiedCoordinateFallback(d));
     if(!html)return;
     const pane=document.createElement("div");
     pane.className="nabil-open-visual";
     pane.innerHTML=html;
     pane.tabIndex=0;
     pane.setAttribute("role","button");
     pane.setAttribute("aria-label","تكبير هذه الرسمة وحدها");
     const previewOne=()=>{
       const modal=el("drawingPreviewModal"),content=el("drawingPreviewContent");
       if(!modal||!content)return;
       const clone=pane.cloneNode(true);
       clone.removeAttribute("tabindex");clone.removeAttribute("role");
       clone.querySelectorAll("[id]").forEach(n=>n.removeAttribute("id"));
       content.replaceChildren(clone);modal.hidden=false;
       el("closeDrawingPreviewBtn")?.focus();
     };
     pane.addEventListener("click",previewOne);
     pane.addEventListener("keydown",e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();previewOne()}});
     visuals.appendChild(pane);
   }catch(_e){}
 });
 const hasVisual=visuals.childElementCount>0;
 if(hasVisual){
   // A distinct labelled figure card, not an inline decoration or a small
   // drawing mixed into the text/working steps.
   const title=document.createElement("h3");
   title.className="nabil-open-figure-card-title";
   title.textContent=lang==="English"?"📐 Figure":lang==="Français"?"📐 Schéma":"📐 الرسمة";
   visuals.prepend(title);
   visuals.setAttribute("role","region");
   visuals.setAttribute("aria-label",title.textContent);
   board.classList.add("has-figure-card");
 }else{
   board.classList.remove("has-figure-card");
 }
 if(figureOnly&&!hasVisual)throw Error("المحرّك لم يعرض الرسمة المطلوبة. جرّب مجددًا أو اكتب قياسات الشكل.");
 const wantsVisual=/draw|plot|graph|figure|diagram|sketch|tracer|dessiner|schéma|schema|ارسم|اعرض الرسم|اعرض الرسمة|ورجيني الرسمة|رسم بياني|مخطط/i.test(String(question||""));
 if(wantsVisual&&!hasVisual){
  const note=document.createElement("p");
  note.className="nabil-open-missing-visual";
  note.textContent=lang==="English"
   ?"No verified drawing was returned. Please provide the function or the figure's givens so I can draw it accurately."
   :lang==="Français"
    ?"Aucun dessin vérifié n’a été retourné. Précise la fonction ou les données de la figure pour la tracer correctement."
    :"ما وصل رسم دقيق لهالسؤال. اكتب الدالة أو معطيات الشكل حتى نرسمه بلا اختراع معلومات.";
  explanation.append(note);
 }
 nav.hidden=false;
 visualBtn.hidden=!hasVisual;
 explanation.hidden=figureOnly;
 visuals.hidden=!hasVisual;
 explainBtn.hidden=figureOnly;
 explainBtn.textContent=lang==="English"?"📘 Hide explanation":lang==="Français"?"📘 Masquer l’explication":"📘 إخفاء الشرح";
 visualBtn.textContent=lang==="English"?"📐 Show figure":lang==="Français"?"📐 Afficher le schéma":"📐 عرض الرسمة";
 explainBtn.onclick=()=>{
   explanation.hidden=!explanation.hidden;
   explainBtn.textContent=explanation.hidden
     ?(lang==="English"?"📘 Show explanation":lang==="Français"?"📘 Afficher l’explication":"📘 عرض الشرح")
     :(lang==="English"?"📘 Hide explanation":lang==="Français"?"📘 Masquer l’explication":"📘 إخفاء الشرح");
   if(!explanation.hidden)explanation.scrollIntoView({behavior:"smooth",block:"nearest"});
 };
 visualBtn.onclick=()=>{if(hasVisual){visuals.hidden=false;visuals.scrollIntoView({behavior:"smooth",block:"nearest"});}};

 const copy=document.createElement("button");
 copy.type="button";copy.textContent="📋 نسخ الإجابة";
 copy.addEventListener("click",async()=>{
   try{await navigator.clipboard.writeText(reply);copy.textContent="✅ تم النسخ";setTimeout(()=>copy.textContent="📋 نسخ الإجابة",1400)}
   catch(_e){copy.textContent="تعذّر النسخ"}
 });
 const read=document.createElement("button");
 read.type="button";read.textContent=lang==="English"?"🔊 Read answer":lang==="Français"?"🔊 Lire la réponse":"🔊 اقرأ الإجابة";
 read.addEventListener("click",()=>{
   const spoken=typeof nabilBoardPlainSpeech==="function"?nabilBoardPlainSpeech(reply):reply;
   Promise.resolve(nabilSpeakClear?.(spoken,lang,{})).catch(()=>{});
 });
 const stop=document.createElement("button");
 stop.type="button";stop.textContent=lang==="English"?"⏹ Stop voice":lang==="Français"?"⏹ Arrêter la voix":"⏹ أوقف الصوت";
 stop.addEventListener("click",()=>{try{stopNabilNeuralVoice?.();speechSynthesis?.cancel?.()}catch(_e){}});
 if(!figureOnly){
   toolsHost.append(copy);
   const exportMenu=document.createElement("select");
   exportMenu.id="nabilAnswerExport";
   exportMenu.setAttribute("aria-label","تصدير الإجابة");
   exportMenu.style.cssText="max-width:100%;padding:8px;border-radius:8px;background:#123f65;color:#fff;border:1px solid #43bceb;font:inherit";
   for(const [value,label] of [["","⬇ تصدير الإجابة"],["docx","📄 Word"],["xlsx","📊 Excel"],["google-forms-script","📝 Google Form"]]){
     const option=document.createElement("option");option.value=value;option.textContent=label;exportMenu.appendChild(option);
   }
   exportMenu.addEventListener("change",async()=>{
     const choice=exportMenu.value;exportMenu.value="";if(!choice)return;
     const langKey=lang==="English"?"en":lang==="Français"?"fr":"ar";
     const name=choice==="docx"?"nabil-answer.docx":choice==="xlsx"?"nabil-answer-tables.xlsx":"nabil-create-google-form.gs";
     const label=exportMenu.options[0].textContent;
     exportMenu.disabled=true;exportMenu.options[0].textContent="⏳ جارٍ التحضير...";
     try{
       const response=await fetch("/api/research/answer/"+choice,{
         method:"POST",headers:{"Content-Type":"application/json"},
         body:JSON.stringify({title:questionText.slice(0,500)||"NABIL AI answer",answer:reply,language:langKey})
       });
       if(!response.ok){
         let reason="تعذر التصدير";try{reason=String((await response.json()).detail||reason)}catch(_){}
         throw Error(reason);
       }
       const blob=await response.blob(),url=URL.createObjectURL(blob),link=document.createElement("a");
       link.href=url;link.download=name;document.body.appendChild(link);link.click();link.remove();
       window.setTimeout(()=>URL.revokeObjectURL(url),30000);
       setStatus(choice==="google-forms-script"
         ?"تم تنزيل سكربت Google Forms؛ شغّله من حسابك مع الموافقة على الصلاحيات. لم يُنشأ النموذج تلقائيًا."
         :"✅ تم تجهيز ملف "+name);
     }catch(error){setStatus("⚠️ "+String(error?.message||"تعذر التصدير"),true)}
     finally{exportMenu.disabled=false;exportMenu.options[0].textContent=label;}
   });
   toolsHost.append(exportMenu,read,stop);
 }
 if(hasVisual){
   const preview=document.createElement("button");
   preview.type="button";
   preview.textContent=lang==="English"?"🔎 Enlarge figure":lang==="Français"?"🔎 Agrandir le schéma":"🔎 معاينة الرسمة كبيرة";
   preview.addEventListener("click",()=>{
     const modal=el("drawingPreviewModal"),content=el("drawingPreviewContent");
     if(!modal||!content){visualBtn.click();return}
     content.replaceChildren();
     const clone=visuals.cloneNode(true);
     clone.hidden=false;
     clone.removeAttribute("id");
     clone.querySelectorAll("[id]").forEach(n=>n.removeAttribute("id"));
     clone.classList.add("nabil-open-enlarged-visuals");
     content.appendChild(clone);
     modal.hidden=false;
     el("closeDrawingPreviewBtn")?.focus();
   });
   toolsHost.appendChild(preview);
 }
 try{window.MathJax?.typesetPromise?.([board])}catch(_e){}
 // The formatted answer card already shows the teacher response. Do not duplicate\n // unrendered Markdown/LaTeX in the transcript above it.
 board.scrollIntoView({behavior:"smooth",block:"nearest"});
 return {reply,lang,hasVisual,figureOnly};
}
function getStudent(){
 try{return typeof getStudentId==="function"?getStudentId():(localStorage.getItem("nabil_student_id")||"nabil_open_student")}
 catch(_e){return "nabil_open_student"}
}
async function request({question="",audio=null}){
 if(busy)return;
 const command=String(question||"").trim();
 const isVisualCommand=/^(?:اعرض|ورجيني|فرجيني|اريني|بدي|show|display|affiche|montre).{0,35}(?:رسم|رسمة|الشكل|graph|figure|drawing|schéma|schema|courbe)/i.test(command);
 const isExplanationCommand=/^(?:اعرض|ورجيني|فرجيني|اريني|بدي|show|display|affiche|montre).{0,35}(?:شرح|حل|explanation|solution|explication)/i.test(command);
 if(!audio&&board.classList.contains("has-answer")&&isExplanationCommand){
   explainBtn.click();setStatus("📘 زر الشرح في أسفل البطاقة.");return;
 }
 if(!audio&&board.classList.contains("has-answer")&&isVisualCommand&&!visualBtn.hidden){
   visualBtn.click();setStatus("📐 الرسمة ظاهرة ببطاقة الأستاذ نبيل.");return;
 }
 if(!audio&&!String(question).trim())return;
 setBusy(true);setStatus(audio?"🧠 عم بفهم التسجيل وبحضّر الجواب…":"🧠 عم بفهم سؤالك وبحضّر الجواب والرسم إذا لازم…");
 try{
   const data=new FormData();
   data.append("student_id",getStudent());
   data.append("activity_mode","general_exercises");
   data.append("teaching_mode","home_live_tutor");
   data.append("language","AUTO");
   if(openConversationId)data.append("conversation_id",openConversationId);
   if(audio){
     const mime=audio.type||"audio/webm",ext=/mp4|m4a/.test(mime)?"m4a":/ogg/.test(mime)?"ogg":"webm";
     data.append("audio",audio,"student_voice."+ext);
   }else{
     data.append("message",String(question).trim());
     addLine("student",String(question).trim());
   }
   // Reveal the in-progress state in the actual answer card immediately.
   board.classList.add("is-waiting");
   const aborter=new AbortController();
   const timeout=setTimeout(()=>aborter.abort(),90000);
   let response;
   try{response=await fetch("/api/chat",{method:"POST",body:data,signal:aborter.signal})}
   finally{clearTimeout(timeout)}
   const result=await response.json().catch(()=>({detail:"الخادم لم يرجع JSON صالحًا"}));
   if(!response.ok)throw Error(String(result.detail||"تعذّر إرسال السؤال").slice(0,200));
   if(result.conversation_id)openConversationId=result.conversation_id;
   const heard=String(result.transcribed_text||question||"").trim();
   if(audio&&heard)addLine("student",heard);
   setStatus("✅ وصل الجواب؛ عم بعرض الشرح والرسومات…");
   const shown=renderAnswer(result,heard);
   if(result.student_profile&&window.NABIL130?.mergeProfile)window.NABIL130.mergeProfile(result.student_profile);
   const spoken=typeof nabilBoardPlainSpeech==="function"?nabilBoardPlainSpeech(shown.reply):shown.reply;
   try{stopNabilNeuralVoice?.();speechSynthesis?.cancel?.()}catch(_e){}
   if(!shown.figureOnly&&spoken&&typeof nabilSpeakClear==="function"){
     const typer=prepareSpeechTypewriter(spoken,shown.lang);
     Promise.resolve(nabilSpeakClear(spoken,shown.lang,{
       onduration:d=>typer.setDuration(d),
       onstart:()=>typer.start(),
       onend:()=>typer.finish(),
       onerror:()=>typer.finish()
     })).catch(()=>typer.finish());
   }
   setStatus(shown.figureOnly?"✅ الرسمة ظاهرة. فيك تكبّرها بزر المعاينة.":shown.hasVisual?"✅ الجواب جاهز. الشرح والرسمة في بطاقتين منفصلتين.":"✅ الجواب جاهز لسؤالك التالي.");
   return true;
 }catch(e){
   const aborted=e?.name==="AbortError";
   if(!audio&&String(question||"").trim()&&!input.value.trim())input.value=String(question).trim();
   setStatus("⚠️ "+(aborted?"تأخر الجواب أكثر من المتوقع. جرّب إرسال السؤال مرة ثانية.":String(e?.message||"تعذّر الاتصال").slice(0,180)),true)
   return false;
 }
 finally{board.classList.remove("is-waiting");setBusy(false);send.disabled=false;talk.disabled=false;if(!recording)talk.textContent="🎙️ سؤال صوتي"}
}
async function startRecording(){
 if(busy||recording)return;
 if(!navigator.mediaDevices?.getUserMedia||!window.MediaRecorder){setStatus("الميكروفون غير مدعوم؛ اكتب سؤالك أو افتح الموقع عبر HTTPS.",true);return}
 try{
   stream=await navigator.mediaDevices.getUserMedia({audio:{echoCancellation:true,noiseSuppression:true,autoGainControl:true}});
   const mime=["audio/webm;codecs=opus","audio/mp4","audio/ogg;codecs=opus"].find(x=>MediaRecorder.isTypeSupported?.(x));
   recorder=new MediaRecorder(stream,mime?{mimeType:mime}:undefined);chunks=[];
   recorder.ondataavailable=e=>{if(e.data?.size)chunks.push(e.data)};
   recorder.onstop=()=>{const blob=new Blob(chunks,{type:recorder?.mimeType||"audio/webm"});chunks=[];stream?.getTracks().forEach(t=>t.stop());stream=null;recorder=null;recording=false;request({audio:blob})};
   try{stopNabilNeuralVoice?.();speechSynthesis?.cancel?.()}catch(_e){}
   recorder.start();recording=true;send.disabled=true;talk.textContent="⏹ إيقاف وإرسال";setStatus("🎙️ احكي براحتك، وبس تخلص اضغط إيقاف وإرسال.");
 }catch(_e){stream?.getTracks().forEach(t=>t.stop());stream=null;setStatus("اسمح للميكروفون من إعدادات المتصفح وجرّب مرة ثانية.",true)}
}
function stopRecording(){if(!recording||!recorder)return;talk.textContent="⏳ جارٍ الإرسال";setStatus("⏳ عم برسل التسجيل…");try{recorder.stop()}catch(_e){recording=false;setStatus("تعذّر إنهاء التسجيل.",true)}}
talk.addEventListener("click",()=>{recording?stopRecording():startRecording()});
send.addEventListener("click",()=>{if(recording||busy)return; // Do not duplicate pending requests.
 const q=input.value.trim();if(!q)return;
 input.value="";
 Promise.resolve(request({question:q})).then(ok=>{
   if(ok===false&&!input.value.trim())input.value=q;
 }).catch(e=>{
   if(!input.value.trim())input.value=q;
   setStatus("⚠️ تعذّر إرسال السؤال: "+String(e?.message||e).slice(0,150),true);
 });
});
input.addEventListener("input",()=>{
 const lang=detectLanguage(input.value);
 input.dir=lang==="العربية"?"rtl":"ltr";
 input.lang=lang==="العربية"?"ar":lang==="English"?"en":"fr";
});
input.addEventListener("keydown",e=>{if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();send.click()}});

// Suppress the old home browser-SpeechRecognition handler; the landing microphone
// must always use server transcription exactly like the platform voice path.
document.addEventListener("click",e=>{
 const old=e.target.closest?.("#homeVoiceBtn");
 if(!old)return;
 e.preventDefault();e.stopImmediatePropagation();
 if(recording)stopRecording();else startRecording();
},true);

// Keep legacy red microphone as a large, accessible shortcut to the same recorder.
const legacyMic=el("homeVoiceBtn");
if(legacyMic){legacyMic.hidden=false;legacyMic.title="سؤال صوتي — نفس محرّك الأستاذ نبيل";legacyMic.querySelector("span:last-child")?.replaceChildren("سؤال صوتي")}

// Stable TWO-VIEW navigation: the retired legacy home click listener and
// delayed splash/mobile callbacks must not hide the lesson after a moment.
const returnHome=document.createElement("button");
returnHome.id="nabilReturnHomeFloating";
returnHome.type="button";
returnHome.textContent="Home";
returnHome.setAttribute("aria-label","العودة إلى الأستاذ نبيل");
// Navigation belongs inside the visible lesson header, never over the
// fixed exercise composer or Send button. If the header is unavailable,
// keep the control in normal document flow instead of floating.
const lessonHeader=document.querySelector("body > .header")||document.querySelector(".header");
const lessonColumnForHome=document.querySelector(".lesson-main-column");
if(lessonHeader)lessonHeader.appendChild(returnHome);
else if(lessonColumnForHome)lessonColumnForHome.prepend(returnHome);
else document.body.appendChild(returnHome);

function showStructuredLesson(){
 try{stopNabilNeuralVoice?.();speechSynthesis?.cancel?.()}catch(_e){}
 document.body.classList.remove("nabil-home-lock");
 document.body.classList.add("nabil-lesson-active");
 home.setAttribute("aria-hidden","true");
 home.hidden=true;
 home.style.setProperty("display","none","important");
 homeHost.style.display="none";
 stage&&(stage.hidden=true);
 window.scrollTo({top:0,behavior:"instant"});
}
function showBlueRobotHome(){
 document.body.classList.remove("nabil-lesson-active");
 document.body.classList.add("nabil-home-lock");
 home.hidden=false;
 home.removeAttribute("aria-hidden");
 home.style.removeProperty("display");
 home.style.display="block";
 home.style.opacity="1";
 homeHost.style.display="block";
 stage&&(stage.hidden=true);
 window.scrollTo({top:0,behavior:"instant"});
}
// Capture and consume the event BEFORE the obsolete listener on the green
// button: it can otherwise re-enter the retired grade screen or re-lock scroll.
document.addEventListener("click",e=>{
 if(e.target.closest?.("#homeStartShortcut")){
   e.preventDefault();
   e.stopImmediatePropagation();
   showStructuredLesson();
 }else if(e.target.closest?.("#nabilReturnHomeFloating,#backToInterfaceBtn,#lessonHomeBtn")){
   e.preventDefault();
   e.stopImmediatePropagation();
   showBlueRobotHome();
 }
},true);
returnHome.addEventListener("click",showBlueRobotHome);
window.nabilShowProfessorGateway=showBlueRobotHome;
try{if(typeof nabilActivityMode!=="undefined")nabilActivityMode="general_exercises"}catch(_e){}
// Do not let the retired home script speak using a second browser-only voice.
try{if(typeof homeWelcomeSpoken!=="undefined")homeWelcomeSpoken=true}catch(_e){}
document.body.classList.add("nabil-home-lock");
// Browsers normally block autoplay. Greet on the learner's first intentional interaction,
// using the exact same neural TTS function as the lesson page.
home.addEventListener("pointerdown",e=>{
 // Do not play greeting over microphone recording or while typing a question.
 if(e.target.closest("button,textarea,input,select,label"))return;
 speakGreetingOnce();
},{once:true,passive:true});
input.addEventListener("input",()=>{
 const lang=detectLanguage(input.value);
 input.dir=lang==="العربية"?"rtl":"ltr";
 input.lang=lang==="العربية"?"ar":lang==="English"?"en":"fr";
});
window.NabilOpenTutor={
 start:startRecording,stop:stopRecording,ask:q=>request({question:q}),
 showExplanation:()=>explainBtn.click(),
 showDrawing:()=>{if(!visualBtn.hidden)visualBtn.click();else setStatus("ما في رسمة مرتبطة بآخر جواب. اطلب رسمًا مع معطيات السؤال.",true)},
 setPace:n=>{pace.value=String(n);syncPace()}
};
})();
