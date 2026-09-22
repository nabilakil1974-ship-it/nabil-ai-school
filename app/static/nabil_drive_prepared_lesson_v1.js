/* Prefer the author's finished interactive Drive lesson; fall back to AI textbook teaching. */
(()=>{
"use strict";
let replay=false,busy=false;
let debug=new URLSearchParams(location.search).has("nabil_debug_drive");
let panel;
function trace(stage,detail=""){
 const line=new Date().toLocaleTimeString()+" | "+stage+" | "+detail;
 console.info("[NABIL_DRIVE_TRACE]",line);
 if(!debug)return;
 if(!panel){
  panel=document.createElement("details");panel.open=true;
  panel.style.cssText="position:fixed;top:80px;left:10px;z-index:2147483000;width:min(480px,90vw);max-height:45vh;overflow:auto;background:#071d30;color:#b9f4ff;border:2px solid #4ac9ec;border-radius:10px;padding:10px;font:12px/1.6 monospace;direction:ltr";
  const title=document.createElement("summary");title.textContent="NABIL Drive diagnostic (temporary)";
  panel.append(title);document.body.append(panel);
 }
 const row=document.createElement("div");row.textContent=line;panel.append(row);
}
if(debug)trace("DIAGNOSTIC_READY");
const nativeFetch=window.fetch.bind(window);
window.fetch=async function(input,options){
 const url=typeof input==="string"?input:input?.url||"";
 const ai=url.includes("/api/chat");
 if(ai)trace("AI_REQUEST_STARTED",url.split("?")[0]);
 try{
  const response=await nativeFetch(input,options);
  if(ai)trace("AI_RESPONSE","HTTP "+response.status);
  return response;
 }catch(error){
  if(ai)trace("AI_REQUEST_FAILED",error?.name||"NetworkError");
  throw error;
 }
};

const field=id=>document.getElementById(id)?.value?.trim()||"";
/* Add actual prepared HTML lessons to the existing selector after grade/subject
   changes. No AI generation and no per-lesson frontend registry. */
let shelfBusy=false;
function ensureShelf(){
 let shelf=document.getElementById("nabilPreparedDriveShelf");
 if(shelf)return shelf;
 const anchor=document.getElementById("lessonSelect")||document.getElementById("startLesson");
 if(!anchor)return null;
 shelf=document.createElement("section");
 shelf.id="nabilPreparedDriveShelf";
 shelf.setAttribute("aria-label","الدروس المحضّرة من Google Drive");
 shelf.style.cssText="box-sizing:border-box;display:block;width:100%;max-width:100%;min-width:0;grid-column:1/-1;flex:1 1 100%;margin:12px 0;padding:12px;border:2px solid #39c5e4;border-radius:14px;background:#0b2842;color:white;overflow-wrap:anywhere";
 anchor.closest("section,fieldset,.card")?.append(shelf);
 if(!shelf.isConnected)anchor.parentElement?.append(shelf);
 return shelf;
}
function renderShelf(lessons,grade,subject){
 const shelf=ensureShelf();if(!shelf)return;
 shelf.replaceChildren();
 const h=document.createElement("h3");
 h.textContent="📚 دروس Google Drive الجاهزة — "+grade+" / "+subject;
 h.style.cssText="font-size:clamp(15px,3vw,21px);margin:0 0 10px;color:#9befff";
 shelf.append(h);
 if(!lessons.length){
  const p=document.createElement("p");p.textContent="لا توجد دروس HTML محضّرة لهذه المادة حاليًا.";shelf.append(p);return;
 }
 const actions=document.createElement("div");
 actions.style.cssText="display:flex;flex-wrap:wrap;gap:9px;max-width:100%";
 for(const item of lessons){
  const button=document.createElement("button");
  button.type="button";button.textContent="📘 "+item.title;
  button.style.cssText="flex:1 1 190px;min-width:0;max-width:100%;white-space:normal;overflow-wrap:anywhere;padding:12px;border-radius:10px;background:#087d9c;color:white;border:1px solid #7ce7fa;cursor:pointer;font:inherit;min-height:48px";
  button.onclick=()=>openPrepared(grade,subject,item.title);
  actions.append(button);
 }
 shelf.append(actions);
}
async function openPrepared(grade,subject,lesson){
 if(shelfBusy)return;
 shelfBusy=true;
 try{
  const qs=new URLSearchParams({grade,subject,lesson,language:field("languageSelect")});
  const response=await nativeFetch("/api/interactive-lessons/resolve?"+qs,{cache:"no-store"});
  if(!response.ok)throw Error("Drive HTTP "+response.status);
  const data=await response.json();
  showPrepared(data,grade,subject,lesson);
 }catch(error){
  const shelf=ensureShelf();
  const p=document.createElement("p");p.textContent="تعذّر فتح الدرس من Drive: "+error.message;
  p.style.color="#ffd28a";shelf?.append(p);
 }finally{shelfBusy=false;}
}
function showPrepared(data,grade,subject,lesson){
 const chat=document.getElementById("chat");
 const host=chat||ensureShelf()||document.body;
 document.getElementById("nabilDriveInteractiveLesson")?.remove();
 const card=document.createElement("section");
 card.id="nabilDriveInteractiveLesson";
 card.style.cssText="box-sizing:border-box;width:100%;max-width:100%;min-width:0;overflow:hidden;background:#081f34;border:2px solid #37c3e5;border-radius:16px;padding:clamp(8px,2vw,14px);margin:14px auto;color:white";
 const title=document.createElement("h2");title.textContent="📘 "+data.title+" — الدرس التفاعلي من Google Drive";
 title.style.cssText="font-size:clamp(17px,3vw,23px);color:#8eeaff;overflow-wrap:anywhere";
 const frame=document.createElement("iframe");frame.title=data.title;frame.src=data.url;
 frame.style.cssText="display:block;width:100%;max-width:100%;min-width:0;height:min(78vh,900px);min-height:430px;border:0;border-radius:10px;background:#09263f";
 frame.setAttribute("loading","eager");frame.setAttribute("sandbox","allow-scripts allow-forms allow-modals allow-downloads allow-popups");
 const buttons=document.createElement("div");buttons.style.cssText="display:flex;flex-wrap:wrap;gap:8px;margin:12px 0";
 function action(label,url,download=false){
  const link=document.createElement("a");link.textContent=label;link.href=url;
  if(!download){link.target="_blank";link.rel="noopener";}
  link.style.cssText="flex:1 1 180px;min-width:0;max-width:100%;box-sizing:border-box;padding:12px;border-radius:9px;background:#12577b;color:white;text-align:center;text-decoration:none;overflow-wrap:anywhere";
  buttons.append(link);
 }
 action("↗ عرض الدرس كاملًا",data.url);
 const ppt=new URL("/api/lesson-export/prepared",location.origin);
 for(const [key,value] of Object.entries({grade,subject,lesson,language:field("languageSelect"),format:"pptx"}))ppt.searchParams.set(key,value);
 action("📊 عرض PowerPoint / تنزيل PPTX",ppt.pathname+ppt.search,true);
 ppt.searchParams.set("format","reference");
 action("🗂️ البطاقة المرجعية للطباعة",ppt.pathname+ppt.search);
 card.append(title,buttons,frame);host.append(card);card.scrollIntoView({behavior:"smooth",block:"start"});
 trace("DRIVE_DISPLAY_SELECTED","No AI; PPTX and full-page links shown");
}
let availableSeq=0;
async function refreshPreparedLessons(){
 const seq=++availableSeq;
 const grade=field("gradeSelect"),subject=field("subjectSelect");
 const select=document.getElementById("lessonSelect");
 if(!grade||!subject||!select)return;
 try{
  const q=new URLSearchParams({grade,subject});
  const res=await nativeFetch("/api/interactive-lessons/available?"+q,{cache:"no-store"});
  if(!res.ok)throw Error("HTTP "+res.status);
  const data=await res.json();
  if(seq!==availableSeq||grade!==field("gradeSelect")||subject!==field("subjectSelect"))return;
  select.querySelectorAll("option[data-nabil-drive-prepared]").forEach(o=>o.remove());
  const normalize=t=>String(t||"").trim().toLocaleLowerCase();
  for(const lesson of data.lessons||[]){
   const names=new Set([lesson.title,...(lesson.aliases||[])].map(normalize));
   const matching=[...select.options].filter(o=>names.has(normalize(o.value))||names.has(normalize(o.textContent)));
   if(matching.length){
    const keep=matching.find(o=>normalize(o.value)===normalize(lesson.title))||matching[0];
    const wasSelected=matching.some(o=>o.selected);
    keep.value=lesson.title;
    keep.textContent="📘 "+lesson.title+" · Google Drive";
    keep.dataset.nabilDrivePrepared="1";
    for(const extra of matching)if(extra!==keep)extra.remove();
    if(wasSelected)keep.selected=true;
   }else{
    const option=new Option("📘 "+lesson.title+" · Google Drive",lesson.title);
    option.dataset.nabilDrivePrepared="1";
    select.add(option);
   }
  }
  renderShelf(data.lessons||[],grade,subject);
  trace("DRIVE_LESSONS_IN_SELECTOR",String((data.lessons||[]).length));
 }catch(error){trace("DRIVE_LESSON_SELECTOR_UNAVAILABLE",error.message||"network");}
}
// Delegation survives a curriculum UI that creates/replaces selectors after load.
document.addEventListener("change",event=>{
 if(["gradeSelect","subjectSelect","languageSelect"].includes(event.target?.id)){
  refreshPreparedLessons();
  setTimeout(refreshPreparedLessons,350);
  setTimeout(refreshPreparedLessons,1100);
 }
},true);
let lastSelectorSignature="";
async function refreshIfSelectorChanged(){
 const select=document.getElementById("lessonSelect");
 const signature=[field("gradeSelect"),field("subjectSelect"),
   select?.options?.length||0,[...(select?.options||[])].filter(o=>!o.dataset.nabilDrivePrepared).map(o=>o.value).join("|")].join("::");
 if(signature!==lastSelectorSignature){
  lastSelectorSignature=signature;
  await refreshPreparedLessons();
 }
}
if(document.readyState==="loading")
 document.addEventListener("DOMContentLoaded",()=>setTimeout(refreshIfSelectorChanged,400));
else setTimeout(refreshIfSelectorChanged,400);
setInterval(refreshIfSelectorChanged,4000);

document.addEventListener("click",async event=>{
 const start=event.target?.closest?.("#startLesson");
 if(!start||replay||busy)return;
 const grade=field("gradeSelect"),subject=field("subjectSelect"),lesson=field("lessonSelect");
 if(!grade||!subject||!lesson){trace("DRIVE_SKIPPED","Missing grade/subject/lesson");return;}
 // An optional printed page is NOT a reason to skip a named prepared lesson.
 // Exact-page-only requests retain the indexed textbook fallback.
 if(/^صفحة الكتاب المطبوعة/.test(lesson)){trace("DRIVE_SKIPPED","Exact page request");return;}
 event.preventDefault();event.stopImmediatePropagation();
 busy=true;
 trace("DRIVE_LOOKUP_FIRST",JSON.stringify({grade,subject,lesson,language:field("languageSelect")}));
 const previous=start.textContent;
 start.textContent="📚 عم فتّش عن الدرس التفاعلي على Google Drive…";
 try{
  const qs=new URLSearchParams({grade,subject,lesson,language:field("languageSelect")});
  if(debug){
   trace("DIAGNOSTIC_REQUEST","Live Drive check; no AI");
   try{
    const check=await nativeFetch("/api/interactive-lessons/diagnose?"+qs);
    trace("DIAGNOSTIC_HTTP",String(check.status));
    const report=await check.json();
    trace("DIAGNOSTIC_TRACE",report.trace||"none");
    for(const item of report.steps||[])trace("STEP "+item.step+" "+item.stage,JSON.stringify(item));
   }catch(error){trace("DIAGNOSTIC_FAILED",error?.message||"network");}
  }
  const response=await fetch("/api/interactive-lessons/resolve?"+qs);
  trace("DRIVE_LOOKUP_HTTP",String(response.status));
  if(response.ok){
   const data=await response.json();
   trace("DRIVE_FILE_VERIFIED","trace="+data.trace+" bytes="+data.bytes);
   showPrepared(data,grade,subject,lesson);
   return;
  }
  const error=await response.json().catch(()=>({}));
  trace("DRIVE_NOT_READY","HTTP "+response.status+" trace="+(error.detail?.trace||"none")+" stage="+(error.detail?.stage||"unknown")+" reason="+(error.detail?.reason||"unknown"));
 }catch(e){trace("DRIVE_NETWORK_ERROR",e?.name||"NetworkError");console.warn("Prepared Drive lesson lookup unavailable; using textbook teaching.",e)}
 finally{busy=false;start.textContent=previous}
 // A missing or inaccessible prepared lesson must NOT block normal textbook teaching.
 trace("FALLBACK_TO_EXISTING_AI","Prepared lesson unavailable");
 replay=true;
 try{start.click()}finally{replay=false}
},true);
})();