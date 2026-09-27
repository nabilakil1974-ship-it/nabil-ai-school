/* NABIL AI — generated lesson End-to-End runtime v1.
 * Shared by every factory-produced lesson/exercise page.
 * Real contracts only: /api/chat + approved Scientific Solution Card renderer.
 */
(()=>{
"use strict";

const qs=(s,r=document)=>r.querySelector(s);
const qsa=(s,r=document)=>[...r.querySelectorAll(s)];
const meta=name=>qs('meta[name="'+name+'"]')?.content||"";
const lessonMeta={
  lessonId:meta("nabil-lesson-id"),
  lesson:meta("nabil-canonical-title")||document.title,
  grade:meta("nabil-grade"),
  subject:meta("nabil-subject"),
  bookId:meta("nabil-source-book-id"),
  pages:meta("nabil-source-pages")
};
if(!lessonMeta.lessonId)return;

const langRaw=(document.documentElement.lang||"en").toLowerCase();
const lang=langRaw.startsWith("ar")?"ar":langRaw.startsWith("fr")?"fr":"en";
const L={
 ar:{
  title:"الأستاذ نبيل — اسأل، ارفع تمرينًا، واسمع الشرح",
  ask:"اكتب سؤالك عن هذا الدرس أو اطلب حل الملف المرفق…",
  send:"إرسال وحل",
  file:"📎 صورة / PDF / Word",
  mic:"🎙️ سؤال صوتي",
  stopMic:"⏹ إرسال الصوت",
  read:"🔊 اقرأ",
  stop:"⏹ إيقاف الصوت",
  readPage:"🔊 اقرأ الصفحة",
  auto:"لغة الشرح تلقائيًا",
  busy:"🧠 الأستاذ نبيل يقرأ المصدر ويحضّر جوابًا موثوقًا…",
  ready:"جاهز.",
  badFile:"الملف المدعوم: صورة أو PDF أو DOCX.",
  noResponse:"لم يصل جواب صالح من الخادم.",
  network:"تعذّر الاتصال بمحرك NABIL AI.",
  result:"حل الأستاذ نبيل",
  uploadPrompt:"حلّ أو اشرح محتوى الملف المرفق اعتمادًا على معطياته فقط، ولا تخترع أي معلومة ناقصة."
 },
 fr:{
  title:"NABIL — question, fichier et lecture synchronisée",
  ask:"Pose une question sur cette leçon ou demande la résolution du fichier…",
  send:"Envoyer / Résoudre",
  file:"📎 Image / PDF / Word",
  mic:"🎙️ Question vocale",
  stopMic:"⏹ Envoyer l’audio",
  read:"🔊 Lire",
  stop:"⏹ Arrêter",
  readPage:"🔊 Lire la page",
  auto:"Langue automatique",
  busy:"🧠 NABIL lit la source et prépare une réponse vérifiée…",
  ready:"Prêt.",
  badFile:"Formats acceptés : image, PDF ou DOCX.",
  noResponse:"Le serveur n’a pas renvoyé de réponse valide.",
  network:"Impossible de joindre le moteur NABIL AI.",
  result:"Solution NABIL",
  uploadPrompt:"Résous ou explique le fichier joint en utilisant uniquement ses données, sans inventer d’information manquante."
 },
 en:{
  title:"NABIL — ask, upload, and synchronized read-aloud",
  ask:"Ask about this lesson or request a solution for the attached file…",
  send:"Send / Solve",
  file:"📎 Image / PDF / Word",
  mic:"🎙️ Voice question",
  stopMic:"⏹ Send voice",
  read:"🔊 Read",
  stop:"⏹ Stop voice",
  readPage:"🔊 Read page",
  auto:"Automatic language",
  busy:"🧠 NABIL is reading the source and preparing a verified answer…",
  ready:"Ready.",
  badFile:"Supported files: image, PDF, or DOCX.",
  noResponse:"The server returned no valid answer.",
  network:"Could not reach the NABIL AI engine.",
  result:"NABIL solution",
  uploadPrompt:"Solve or explain the attached file using only its actual givens. Do not invent missing information."
 }
}[lang];

let recorder=null,micStream=null,micChunks=[],recording=false,busy=false;
let speechTimer=0,speechToken=0,lastAnswerText="";

function esc(v){return String(v??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));}
function stripSpeech(text){
 return String(text||"")
  .replace(/<_?DRAWINGS?_JSON>[\s\S]*?<\/?_?DRAWINGS?_JSON>/gi," ")
  .replace(/<PROGRESS_JSON>[\s\S]*?<\/PROGRESS_JSON>/gi," ")
  .replace(/\\\[|\\\]|\\\(|\\\)/g," ")
  .replace(/\\(?:frac|sqrt|text|mathrm|mathbf)\b/g," ")
  .replace(/[*#_~]/g," ")
  .replace(/\x60/g," ")
  .replace(/\s+/g," ").trim();
}
function langLabel(code){return code==="ar"?"العربية":code==="fr"?"Français":"English";}
function preferredVoice(code){
 const prefix=code==="ar"?"ar":code==="fr"?"fr":"en";
 const voices=window.speechSynthesis?.getVoices?.()||[];
 return voices.find(v=>String(v.lang||"").toLowerCase().startsWith(prefix)&&v.localService)
     ||voices.find(v=>String(v.lang||"").toLowerCase().startsWith(prefix))||null;
}
function tokenizeSegments(text,base){
 if(base!=="ar")return [{text,lang:base}];
 const parts=String(text).split(/(\s+)/);
 const groups=[];
 for(const p of parts){
   if(!p)continue;
   const target=/[A-Za-zÀ-ÿ]/.test(p)
     ?(lessonMeta.subject.toLowerCase().includes("fr")?"fr":"en")
     :"ar";
   const last=groups[groups.length-1];
   if(last&&last.lang===target)last.text+=p;else groups.push({text:p,lang:target});
 }
 return groups.filter(x=>x.text.trim());
}
function liveNode(){
 let n=qs("#nabilE2ELiveSpeech");
 if(!n){
   n=document.createElement("div");n.id="nabilE2ELiveSpeech";n.setAttribute("aria-live","polite");
   n.style.cssText="position:fixed;left:12px;right:12px;bottom:12px;z-index:2147483000;max-height:26vh;overflow:auto;background:#071d31;color:#f4fbff;border:1px solid #4bcdf4;border-radius:14px;padding:10px 12px;box-shadow:0 8px 30px #0008;font:600 15px/1.65 system-ui;display:none";
   document.body.appendChild(n);
 }
 return n;
}
function stopSpeech(){
 speechToken++;
 if(speechTimer){clearTimeout(speechTimer);speechTimer=0;}
 try{window.stopNabilNeuralVoice?.()}catch(_e){}
 try{window.speechSynthesis?.cancel?.()}catch(_e){}
 const live=liveNode();live.style.display="none";live.textContent="";
}
function progressive(text,duration,token){
 const live=liveNode();const words=String(text).split(/\s+/).filter(Boolean);
 live.style.display=words.length?"block":"none";live.textContent="";
 let i=0;
 const step=Math.max(65,Math.round(((Number(duration)||Math.max(2,words.length*.32))*1000)/Math.max(1,words.length)));
 const tick=()=>{
  if(token!==speechToken)return;
  if(i>=words.length)return;
  live.textContent+=(i?" ":"")+words[i++];
  live.scrollTop=live.scrollHeight;
  if(i<words.length)speechTimer=setTimeout(tick,step);
 };
 tick();
}
async function speak(text,requested=lang){
 const clean=stripSpeech(text);if(!clean)return;
 stopSpeech();const token=++speechToken;
 if(typeof window.nabilSpeakClear==="function"){
   let duration=0,started=false;
   try{
    await Promise.resolve(window.nabilSpeakClear(clean,langLabel(requested),{
      onduration:d=>{duration=Number(d)||0;},
      onstart:()=>{if(!started){started=true;progressive(clean,duration,token);}},
      onend:()=>{if(token===speechToken){const n=liveNode();n.textContent=clean;setTimeout(()=>{if(token===speechToken)n.style.display="none";},900);}},
      onerror:()=>{if(token===speechToken)liveNode().style.display="none";}
    }));
    return;
   }catch(_e){}
 }
 const synth=window.speechSynthesis;
 if(!synth||!window.SpeechSynthesisUtterance)return;
 const segments=tokenizeSegments(clean,requested);
 let shown="";
 const live=liveNode();live.style.display="block";live.textContent="";
 const run=i=>{
   if(token!==speechToken||i>=segments.length){if(token===speechToken)setTimeout(()=>{if(token===speechToken)live.style.display="none";},900);return;}
   const seg=segments[i],u=new SpeechSynthesisUtterance(seg.text);
   u.lang=seg.lang==="ar"?"ar-SA":seg.lang==="fr"?"fr-FR":"en-US";
   u.voice=preferredVoice(seg.lang);u.rate=Math.max(.72,Math.min(1.12,Number(window.nabilVoicePace||.9)));
   u.onstart=()=>{shown+=seg.text;live.textContent=shown;live.scrollTop=live.scrollHeight;};
   u.onboundary=e=>{
     if(token!==speechToken)return;
     const before=shown.slice(0,Math.max(0,shown.length-seg.text.length));
     live.textContent=before+seg.text.slice(0,(e.charIndex||0)+1);
   };
   u.onend=()=>run(i+1);u.onerror=()=>run(i+1);
   synth.speak(u);
 };
 run(0);
}

function getStudentId(){
 try{
  if(typeof window.getStudentId==="function")return window.getStudentId();
  let id=localStorage.getItem("nabil_student_id");
  if(!id){id="lesson_"+(crypto.randomUUID?.()||Date.now().toString(36));localStorage.setItem("nabil_student_id",id);}
  return id;
 }catch(_e){return "nabil_lesson_student";}
}
function uiLanguageCode(){
 const v=qs("#nabilE2ELanguage")?.value||"";
 return ["ar","fr","en"].includes(v)?v:"";
}
function setStatus(text,error=false){
 const n=qs("#nabilE2EStatus");if(!n)return;n.textContent=text;n.style.color=error?"#b91c1c":"#475569";
}
function setBusy(value){
 busy=!!value;
 qsa("#nabilE2ESend,#nabilE2EFileButton,#nabilE2EMic").forEach(b=>b.disabled=busy&&!recording);
}
function currentPageText(){
 const clone=document.querySelector(".container")?.cloneNode(true);if(!clone)return "";
 qsa("button,input,textarea,select,script,style,#nabilE2ETools",clone).forEach(n=>n.remove());
 return clone.innerText.replace(/\s+/g," ").trim().slice(0,12000);
}
function addReadButtons(){
 qsa(".card,.interactive-lab,#goldenReferenceCard,.nabil-sci-card").forEach(card=>{
  if(card.closest("#nabilE2ETools")||card.dataset.nabilReadReady==="1")return;
  card.dataset.nabilReadReady="1";card.style.position=card.style.position||"relative";
  const b=document.createElement("button");b.type="button";b.textContent="🔊";b.title=L.read;b.setAttribute("aria-label",L.read);
  b.style.cssText="position:absolute;top:7px;inset-inline-end:7px;z-index:5;border:1px solid #7dd3fc;background:#e0f2fe;color:#075985;border-radius:9px;min-width:38px;min-height:38px;cursor:pointer";
  b.addEventListener("click",e=>{e.stopPropagation();const copy=card.cloneNode(true);qsa("button,script,style",copy).forEach(n=>n.remove());speak(copy.innerText,lang);});
  card.appendChild(b);
 });
}

function renderResult(result,question,file){
 const host=qs("#nabilE2EResult");host.hidden=false;host.replaceChildren();
 const reply=String(result?.reply||"").trim();lastAnswerText=reply;
 let visualHtml="";
 if(file&&String(file.type||"").startsWith("image/")){
   const url=URL.createObjectURL(file);
   visualHtml='<img src="'+esc(url)+'" alt="Student source image" style="display:block;max-width:100%;max-height:520px;object-fit:contain;margin:auto">';
   setTimeout(()=>URL.revokeObjectURL(url),120000);
 }
 try{
  if(window.NABILScientificCards?.renderCard&&result?.solution_card){
    const spec=Object.assign({},result.solution_card,{drawings:Array.isArray(result.drawings)?result.drawings:(result.solution_card.drawings||[])});
    if(visualHtml&&!spec.visual_html)spec.visual_html=visualHtml;
    window.NABILScientificCards.renderCard(spec,host);
  }else if(window.NABILScientificCards?.deriveSpecFromChat&&reply){
    const spec=window.NABILScientificCards.deriveSpecFromChat(result,question);
    if(visualHtml)spec.visual_html=visualHtml;
    window.NABILScientificCards.renderCard(spec,host);
  }else{
    const box=document.createElement("div");box.className="card";box.style.marginTop="12px";box.style.whiteSpace="pre-wrap";box.textContent=reply||L.noResponse;host.append(box);
  }
 }catch(_e){
  const box=document.createElement("div");box.className="card";box.style.marginTop="12px";box.style.whiteSpace="pre-wrap";box.textContent=reply||L.noResponse;host.append(box);
 }
 const actions=document.createElement("div");actions.style.cssText="display:flex;gap:8px;flex-wrap:wrap;margin-top:10px";
 const read=document.createElement("button");read.className="nabil-e2e-btn";read.type="button";read.textContent=L.read;read.onclick=()=>speak(reply||host.innerText,uiLanguageCode()||lang);
 const stop=document.createElement("button");stop.className="nabil-e2e-btn";stop.type="button";stop.textContent=L.stop;stop.onclick=stopSpeech;
 actions.append(read,stop);host.append(actions);
 addReadButtons();
 try{window.MathJax?.typesetPromise?.([host])}catch(_e){}
 if(reply)speak(reply,uiLanguageCode()||lang);
}

async function sendPayload({audio=null}={}){
 if(busy)return;
 const input=qs("#nabilE2EQuestion"),fileInput=qs("#nabilE2EFile"),file=fileInput?.files?.[0]||null;
 const question=String(input?.value||"").trim()||(file?L.uploadPrompt:"");
 if(!question&&!file&&!audio)return;
 if(file&&!String(file.type||"").startsWith("image/")&&!/\.(pdf|docx)$/i.test(file.name||"")){setStatus(L.badFile,true);return;}
 const fd=new FormData();
 fd.append("student_id",getStudentId());
 fd.append("activity_mode","general_exercises");
 fd.append("teaching_mode","lesson_e2e");
 fd.append("grade",lessonMeta.grade);
 fd.append("subject",lessonMeta.subject);
 fd.append("lesson",lessonMeta.lesson);
 fd.append("language",langLabel(lang));
 fd.append("message",question||L.uploadPrompt);
 const override=uiLanguageCode();if(override)fd.append("nabil_explanation_language",override);
 if(audio)fd.append("audio",audio,audio.name||"lesson_voice.webm");
 if(file){
   if(String(file.type||"").startsWith("image/"))fd.append("image",file,file.name||"exercise-image");
   else fd.append("document",file,file.name||"exercise-document");
 }
 setBusy(true);setStatus(L.busy);
 try{
   const ctl=new AbortController(),timer=setTimeout(()=>ctl.abort(),90000);
   let response;
   try{response=await fetch("/api/chat",{method:"POST",body:fd,signal:ctl.signal});}finally{clearTimeout(timer);}
   const data=await response.json().catch(()=>({detail:L.noResponse}));
   if(!response.ok)throw Error(String(data.detail||L.network).slice(0,260));
   renderResult(data,String(data.transcribed_text||question||""),file);
   if(input&&data.transcribed_text)input.value=String(data.transcribed_text);
   setStatus(L.ready);
 }catch(e){setStatus(e?.name==="AbortError"?L.network:String(e?.message||L.network),true);}
 finally{setBusy(false);}
}

async function toggleMic(){
 if(recording&&recorder){
   recording=false;qs("#nabilE2EMic").textContent=L.mic;
   try{recorder.stop();}catch(_e){}
   return;
 }
 if(busy||!navigator.mediaDevices?.getUserMedia||!window.MediaRecorder){setStatus(L.network,true);return;}
 try{
  micStream=await navigator.mediaDevices.getUserMedia({audio:{echoCancellation:true,noiseSuppression:true,autoGainControl:true}});
  const mime=["audio/webm;codecs=opus","audio/mp4","audio/ogg;codecs=opus"].find(t=>MediaRecorder.isTypeSupported?.(t));
  recorder=new MediaRecorder(micStream,mime?{mimeType:mime}:undefined);micChunks=[];
  recorder.ondataavailable=e=>{if(e.data?.size)micChunks.push(e.data);};
  recorder.onstop=()=>{
    const blob=new Blob(micChunks,{type:recorder?.mimeType||"audio/webm"});
    const ext=/mp4/.test(blob.type)?"m4a":/ogg/.test(blob.type)?"ogg":"webm";
    const file=new File([blob],"lesson_voice."+ext,{type:blob.type});
    micChunks=[];micStream?.getTracks().forEach(t=>t.stop());micStream=null;recorder=null;sendPayload({audio:file});
  };
  stopSpeech();recorder.start();recording=true;qs("#nabilE2EMic").textContent=L.stopMic;setStatus("🎙️");
 }catch(e){micStream?.getTracks().forEach(t=>t.stop());micStream=null;setStatus(String(e?.message||L.network),true);}
}

function install(){
 if(qs("#nabilE2ETools"))return;
 const style=document.createElement("style");style.id="nabil-e2e-runtime-style";style.textContent=
  "#nabilE2ETools{margin:14px 0;padding:13px;background:#fff;border:1px solid #bae6fd;border-radius:12px;box-shadow:0 2px 8px #0f172a12}"+
  ".nabil-e2e-row{display:flex;gap:8px;flex-wrap:wrap;align-items:center}.nabil-e2e-btn{border:1px solid #0284c7;background:#0369a1;color:#fff;border-radius:8px;min-height:42px;padding:8px 12px;cursor:pointer;font:600 13px system-ui}"+
  "#nabilE2EQuestion{width:100%;min-height:64px;box-sizing:border-box;margin:8px 0;padding:9px;border:1px solid #cbd5e1;border-radius:8px;font:14px/1.5 system-ui}"+
  "#nabilE2EResult{margin-top:12px}#nabilE2EStatus{font-size:12px;margin-top:7px;color:#475569}@media(max-width:520px){#nabilE2ETools{padding:10px}.nabil-e2e-btn{flex:1 1 auto}}";
 document.head.appendChild(style);
 const panel=document.createElement("section");panel.id="nabilE2ETools";panel.setAttribute("aria-label",L.title);
 panel.innerHTML='<strong>'+esc(L.title)+'</strong>'+
  '<textarea id="nabilE2EQuestion" placeholder="'+esc(L.ask)+'"></textarea>'+
  '<div class="nabil-e2e-row">'+
   '<label class="nabil-e2e-btn" id="nabilE2EFileButton">'+esc(L.file)+'<input id="nabilE2EFile" type="file" accept="image/*,.pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document" hidden></label>'+
   '<select id="nabilE2ELanguage" class="nabil-e2e-btn" aria-label="'+esc(L.auto)+'"><option value="">'+esc(L.auto)+'</option><option value="ar">العربية</option><option value="en">English</option><option value="fr">Français</option></select>'+
   '<button id="nabilE2EMic" type="button" class="nabil-e2e-btn">'+esc(L.mic)+'</button>'+
   '<button id="nabilE2ESend" type="button" class="nabil-e2e-btn">'+esc(L.send)+'</button>'+
   '<button id="nabilE2EReadPage" type="button" class="nabil-e2e-btn">'+esc(L.readPage)+'</button>'+
   '<button id="nabilE2EStop" type="button" class="nabil-e2e-btn">'+esc(L.stop)+'</button>'+
  '</div><div id="nabilE2EStatus" role="status" aria-live="polite">'+esc(L.ready)+'</div><div id="nabilE2EResult" hidden></div>';
 const host=qs(".header")||qs(".container")||document.body;
 if(host.classList?.contains("header"))host.insertAdjacentElement("afterend",panel);else host.prepend(panel);
 qs("#nabilE2ESend").addEventListener("click",()=>sendPayload());
 qs("#nabilE2EMic").addEventListener("click",toggleMic);
 qs("#nabilE2EReadPage").addEventListener("click",()=>speak(currentPageText(),uiLanguageCode()||lang));
 qs("#nabilE2EStop").addEventListener("click",stopSpeech);
 qs("#nabilE2EFile").addEventListener("change",()=>{
   const f=qs("#nabilE2EFile").files?.[0];if(f)setStatus("📎 "+f.name);
 });
 addReadButtons();
 const observer=new MutationObserver(()=>addReadButtons());observer.observe(document.body,{subtree:true,childList:true});
 window.NABILLessonE2E={sendPayload,speak,stopSpeech,renderResult,lessonMeta};
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",install,{once:true});else install();
})();