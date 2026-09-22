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
   const chat=document.getElementById("chat");
   if(chat){
    document.getElementById("nabilDriveInteractiveLesson")?.remove();
    const card=document.createElement("section");
    card.id="nabilDriveInteractiveLesson";
    card.style.cssText="width:100%;max-width:100%;box-sizing:border-box;background:#081f34;border:2px solid #37c3e5;border-radius:16px;padding:12px;margin:14px auto;color:#fff";
    const title=document.createElement("strong");
    title.textContent="📘 "+data.title+" — الدرس التفاعلي من Google Drive";
    title.style.cssText="display:block;color:#8eeaff;margin-bottom:10px";
    const frame=document.createElement("iframe");
    frame.title="NABIL interactive lesson — "+data.title;
    frame.src=data.url;
    frame.style.cssText="display:block;width:100%;min-height:75vh;border:0;border-radius:10px;background:#09263f";
    frame.setAttribute("loading","eager");
    frame.addEventListener("load",()=>trace("DRIVE_IFRAME_LOADED","trace="+data.trace));
    frame.addEventListener("error",()=>trace("DRIVE_IFRAME_ERROR","trace="+data.trace));
    frame.setAttribute("sandbox","allow-scripts allow-forms allow-modals allow-downloads allow-popups");
    const open=document.createElement("a");
    open.href=data.url;open.target="_blank";open.rel="noopener";
    open.textContent="↗ افتح الدرس بصفحة كاملة";
    open.style.cssText="display:inline-block;margin:10px 0;color:#8eeaff";
    const hint=document.createElement("p");
    hint.textContent="💬 الدرس جاهز من Google Drive؛ اسأل نبيل في خانة المحادثة لأي شرح إضافي أو تفاعل بالذكاء الاصطناعي.";
    hint.style.cssText="color:#a8eaff;font-size:14px;margin:8px 0";
    card.append(title,frame,open,hint);
    trace("DRIVE_DISPLAY_SELECTED","AI generation skipped");
    chat.append(card);card.scrollIntoView({behavior:"smooth",block:"start"});
    return;
   }
   window.location.assign(data.url);
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