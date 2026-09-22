/* Prefer the author's finished interactive Drive lesson; fall back to AI textbook teaching. */
(()=>{
"use strict";
const start=document.getElementById("startLesson");
if(!start)return;
let replay=false,busy=false;
const field=id=>document.getElementById(id)?.value?.trim()||"";
start.addEventListener("click",async event=>{
 if(replay||busy)return;
 const grade=field("gradeSelect"),subject=field("subjectSelect"),lesson=field("lessonSelect");
 if(!grade||!subject||!lesson||field("nabilPrintedPageInput"))return;
 event.preventDefault();event.stopImmediatePropagation();
 busy=true;
 const previous=start.textContent;
 start.textContent="📚 عم فتّش عن الدرس التفاعلي على Google Drive…";
 try{
  const qs=new URLSearchParams({grade,subject,lesson,language:field("languageSelect")});
  const response=await fetch("/api/interactive-lessons/resolve?"+qs);
  if(response.ok){
   const data=await response.json();
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
    const open=document.createElement("a");
    open.href=data.url;open.target="_blank";open.rel="noopener";
    open.textContent="↗ افتح الدرس بصفحة كاملة";
    open.style.cssText="display:inline-block;margin:10px 0;color:#8eeaff";
    card.append(title,frame,open);
    chat.append(card);card.scrollIntoView({behavior:"smooth",block:"start"});
    return;
   }
   window.location.assign(data.url);
   return;
  }
 }catch(e){console.warn("Prepared Drive lesson lookup unavailable; using textbook teaching.",e)}
 finally{busy=false;start.textContent=previous}
 // A missing or inaccessible prepared lesson must NOT block normal textbook teaching.
 replay=true;
 try{start.click()}finally{replay=false}
},true);
})();