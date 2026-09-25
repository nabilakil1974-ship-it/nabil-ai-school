/* NABIL lesson picker -> source-locked factory -> actual interactive lesson.
   This is an owner-controlled pilot, not a claim that 105 gates passed. */
(()=>{
"use strict";
const PREFIX="__nabil_factory__:";
const nativeFetch=window.fetch.bind(window);
let loading=false,loadingCatalog=false, signature="";
const field=id=>String(document.getElementById(id)?.value||"").trim();
const sleep=ms=>new Promise(resolve=>setTimeout(resolve,ms));

function showProgress(title){
 let host=document.getElementById("nabilFactoryJob");
 if(!host){
  host=document.createElement("section");
  host.id="nabilFactoryJob";
  host.style.cssText="box-sizing:border-box;max-width:100%;min-width:0;width:100%;margin:12px 0;padding:16px;background:#0c2841;color:#eefaff;border:2px solid #40ccdc;border-radius:14px;overflow-wrap:anywhere;grid-column:1/-1";
  (document.getElementById("chat")||document.getElementById("startLesson")?.parentElement||document.body).append(host);
 }
 host.replaceChildren();
 const heading=document.createElement("h3");heading.textContent="🧪 الأستاذ نبيل عم يحضّر: "+title;
 const state=document.createElement("p");state.id="nabilFactoryStage";state.textContent="بانتظار تشغيل المصنع…";
 state.setAttribute("role","status");state.setAttribute("aria-live","polite");
 host.append(heading,state);
 host.scrollIntoView({behavior:"smooth",block:"nearest"});
 return {host,state};
}
function displayLesson(info,title){
 const {host,state}=showProgress(title);
 state.textContent="✅ اجتازت النسخة الاختبارات الآلية المحلية. راجع الدرس علميًا وبصريًا قبل اعتماده.";
 const link=document.createElement("a");
 link.href=info.url;link.target="_blank";link.rel="noopener";
 link.textContent="↗ افتح الدرس كاملًا";
 link.style.cssText="display:inline-block;box-sizing:border-box;padding:12px;margin:8px 0;border-radius:9px;background:#047c9b;color:white;text-decoration:none;min-height:44px";
 const frame=document.createElement("iframe");
 frame.title="درس "+title+" — نسخة QA للمراجعة";
 frame.src=info.url;
 frame.style.cssText="display:block;box-sizing:border-box;width:100%;max-width:100%;height:min(78vh,900px);min-height:420px;border:0;border-radius:10px;background:white";
 frame.setAttribute("sandbox","allow-scripts allow-forms allow-modals allow-downloads allow-popups");
 host.append(link,frame);
 host.scrollIntoView({behavior:"smooth",block:"start"});
}
async function fetchCatalog(){
 if(loadingCatalog)return;
 const select=document.getElementById("lessonSelect"),grade=field("gradeSelect"),subject=field("subjectSelect");
 if(!select||!grade||!subject)return;
 const sig=[grade,subject,[...select.options].filter(o=>!o.dataset.nabilFactory).map(o=>o.value).join("|")].join("::");
 if(sig===signature)return;
 loadingCatalog=true;
 try{
  const q=new URLSearchParams({grade,subject});
  const response=await nativeFetch("/api/interactive-lessons/factory/catalog?"+q,{cache:"no-store"});
  if(!response.ok)return;
  const data=await response.json();
  if(grade!==field("gradeSelect")||subject!==field("subjectSelect")||select!==document.getElementById("lessonSelect"))return;
  const selected=select.value;
  select.querySelectorAll("option[data-nabil-factory]").forEach(option=>option.remove());
  for(const lesson of data.lessons||[]){
   const option=new Option("🧪 حضّر بالسكربت: "+lesson.title,PREFIX+lesson.lesson_id);
   option.dataset.nabilFactory=lesson.lesson_id;
   select.add(option);
  }
  if(selected.startsWith(PREFIX)&&[...select.options].some(o=>o.value===selected))select.value=selected;
  signature=sig;
 }catch(err){console.warn("[NABIL_FACTORY] Catalog unavailable",err);}
 finally{loadingCatalog=false;}
}
async function requestFactory(lessonId,title){
 if(loading)return;
 loading=true;
 const {state}=showProgress(title);
 try{
  let token=sessionStorage.getItem("nabilFactoryOwnerToken")||"";
  if(!token){
   token=window.prompt("رمز صاحب المنصة لتحضير الدرس (ليس مفتاح AI):")||"";
   if(!token){state.textContent="لم يبدأ التحضير: رمز صاحب المنصة مطلوب.";return;}
   sessionStorage.setItem("nabilFactoryOwnerToken",token);
  }
  const headers={"Content-Type":"application/json","X-Nabil-Factory-Token":token};
  const start=await nativeFetch("/api/interactive-lessons/factory/prepare",{
   method:"POST",headers,body:JSON.stringify({lesson_id:lessonId})
  });
  const info=await start.json().catch(()=>({}));
  if(!start.ok){
   if(start.status===403)sessionStorage.removeItem("nabilFactoryOwnerToken");
   state.textContent="لم يبدأ التحضير: "+(typeof info.detail==="string"?info.detail:"HTTP "+start.status);
   return;
  }
  for(let tries=0;tries<400;tries++){
   const q=new URLSearchParams({lesson_id:lessonId});
   const resp=await nativeFetch("/api/interactive-lessons/factory/status?"+q,{
    headers:{"X-Nabil-Factory-Token":token},cache:"no-store"
   });
   if(!resp.ok){state.textContent="تعذّر متابعة التحضير: HTTP "+resp.status;return;}
   const data=await resp.json();
   state.textContent="⏳ "+(data.stage||"GENERATING")+" — التحضير والاختبارات قيد التنفيذ…";
   if(data.status==="QA_PASSED_LOCAL"){displayLesson(data,title);return;}
   if(data.status==="FAILED"){
    state.textContent="❌ توقف المصنع دون نشر الدرس. السبب: "+String(data.message||"UNKNOWN").slice(-1300);
    return;
   }
   if(data.status==="NOT_STARTED"){
    state.textContent="توقّفت الحاوية أثناء التحضير؛ لم يُعلن نجاح درس غير مُتحقق منه.";
    return;
   }
   await sleep(3000);
  }
  state.textContent="انتهت مهلة الانتظار في المتصفح؛ تحقّق من حالة التحضير. لم نعلن نجاحًا غير مثبت.";
 }catch(error){
  state.textContent="تعذّر الاتصال بمصنع الدروس: "+String(error.message||error);
 }finally{loading=false;}
}
// Register before the pre-existing Drive-first click handler. Ordinary lesson
// selections still use the original Drive -> textbook tutor flow unmodified.
document.addEventListener("click",event=>{
 const start=event.target?.closest?.("#startLesson");
 if(!start)return;
 const value=field("lessonSelect");
 if(!value.startsWith(PREFIX))return;
 event.preventDefault();
 event.stopImmediatePropagation();
 const lid=value.slice(PREFIX.length);
 const option=document.getElementById("lessonSelect")?.selectedOptions?.[0];
 const title=option?.textContent?.replace(/^🧪\s*حضّر بالسكربت:\s*/,"")||lid;
 requestFactory(lid,title);
},true);
document.addEventListener("change",event=>{
 if(["gradeSelect","subjectSelect","languageSelect"].includes(event.target?.id)){
  signature="";
  setTimeout(fetchCatalog,400);
  setTimeout(fetchCatalog,1100);
 }
},true);
if(document.readyState==="loading")
 document.addEventListener("DOMContentLoaded",()=>setTimeout(fetchCatalog,900));
else setTimeout(fetchCatalog,900);
setInterval(fetchCatalog,5500);
})();
