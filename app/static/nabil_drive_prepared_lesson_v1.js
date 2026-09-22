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