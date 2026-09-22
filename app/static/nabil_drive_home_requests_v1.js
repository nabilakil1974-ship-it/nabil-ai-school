/* Route explicit homepage typed/spoken lesson, exercise, page and worksheet requests to verified Drive HTML first. */
(()=>{
"use strict";
const originalFetch=window.fetch.bind(window);
const field=id=>document.getElementById(id)?.value?.trim()||"";
const lessonPattern=/conducteurs?\s+ohmiques?|ohmic\s+conductors?/i;
const intentPattern=/اشرح|شرح|افتح|اعرض|ورقة|ملخص|ملخّص|تمرين|صفحة|درس|explain|show|open|lesson|exercise|exercice|page|worksheet|summary|fiche|résum/i;
const exercisePattern=/(?:تمرين|التمرين|exercise|exercice|ex\.?|رقم التمرين)\s*(?:رقم|number|no\.?|n°)?\s*[:#-]?\s*(\d{1,3})/i;
const pagePattern=/(?:صفحة|الصفحة|page|p\.)\s*(?:الكتاب|du livre|book|رقم|number|no\.?)?\s*[:#-]?\s*(\d{1,4})/i;
const worksheetPattern=/ورقة\s*(?:عمل|تفاعلية|العمل)|الورقة\s*التفاعلية|ملخص|ملخّص|worksheet|summary|fiche\s*(?:de\s*travail|résumé)/i;
let busy=false;
function render(data,mode,number){
 const chat=document.getElementById("chat");
 if(!chat){window.open(data.url,"_blank","noopener");return;}
 document.getElementById("nabilDriveInteractiveLesson")?.remove();
 const card=document.createElement("section");card.id="nabilDriveInteractiveLesson";card.dataset.lesson="Conducteurs ohmiques";card.dataset.mode=mode;card.dataset.exercise=mode==="exercise"?String(number):"";
 card.style.cssText="width:100%;max-width:100%;box-sizing:border-box;background:#081f34;border:2px solid #37c3e5;border-radius:16px;padding:12px;margin:14px auto;color:#fff";
 const title=document.createElement("strong");
 title.textContent="📘 "+data.title+(mode==="exercise"?" · التمرين "+number:mode==="page"?" · صفحة الكتاب "+number:mode==="worksheet"?" · الورقة التفاعلية":" · الدرس الكامل");
 title.style.cssText="display:block;color:#8eeaff;margin-bottom:10px";
 const frame=document.createElement("iframe");frame.title=title.textContent;frame.src=data.url;frame.setAttribute("loading","eager");
 frame.setAttribute("sandbox","allow-scripts allow-forms allow-modals allow-downloads allow-popups");
 frame.style.cssText="display:block;width:100%;min-height:78vh;border:0;border-radius:10px;background:#09263f";
 const link=document.createElement("a");link.href=data.url;link.target="_blank";link.rel="noopener";
 link.textContent="↗ افتح بصفحة كاملة";link.style.cssText="display:inline-block;margin:10px 0;color:#8eeaff";
 const sheet=document.createElement("button");sheet.type="button";sheet.textContent="📝 ورقة تفاعلية · البطاقة المرجعية";
 sheet.style.cssText="margin:8px;background:#127f83;color:white;border:1px solid #73ebdf;border-radius:9px;padding:10px;cursor:pointer";
 sheet.onclick=()=>{const u=new URL(data.url,location.origin);u.searchParams.delete("exercise");u.searchParams.delete("page");u.searchParams.set("worksheet","1");frame.src=u.pathname+u.search;link.href=frame.src;};
 const full=document.createElement("button");full.type="button";full.textContent="📚 الدرس كاملًا";
 full.style.cssText=sheet.style.cssText;
 full.onclick=()=>{const u=new URL(data.url,location.origin);for(const key of ["exercise","page","worksheet"])u.searchParams.delete(key);frame.src=u.pathname+u.search;link.href=frame.src;};
 card.append(title,frame,link,sheet,full);chat.append(card);card.scrollIntoView({behavior:"smooth",block:"start"});
}
function classify(body){
 const message=String(body.get("message")||"").trim();
 if(!intentPattern.test(message))return null;
 const lesson=field("lessonSelect")||String(body.get("lesson")||"");
 const isKnown=lessonPattern.test(message)||lessonPattern.test(lesson);
 if(!isKnown)return null; // Never route a different lesson to the Ohmic Conductors HTML.
 const exercise=message.match(exercisePattern)?.[1];
 const page=message.match(pagePattern)?.[1]||String(body.get("book_page")||"").trim();
 const worksheet=worksheetPattern.test(message);
 const mode=exercise?"exercise":page?"page":worksheet?"worksheet":"lesson";
 if(!lessonPattern.test(message)&&mode==="lesson")return null; // Avoid hijacking a generic chat.
 const grade=field("gradeSelect")||String(body.get("grade")||"");
 const subject=field("subjectSelect")||String(body.get("subject")||"");
 if(grade&&!/(?:التاسع|\b9\b|٩|ninth|neuvi)/i.test(grade))return null;
 if(subject&&!/(فيزياء|physique|physics)/i.test(subject))return null;
 return {grade:grade||"الصف التاسع",subject:subject||"فيزياء",lesson:"Conducteurs ohmiques",
  language:field("languageSelect")||String(body.get("language")||"Français"),mode,number:exercise||page};
}
// The existing worksheet button must open the authored Drive worksheet and reference summary first.
document.addEventListener("click",async event=>{
 const button=event.target?.closest?.("#nabilWorksheetBtn,#nabilOpenLessonWorksheet");
 if(!button)return;
 const selected=field("lessonSelect");
 if(!lessonPattern.test(selected))return; // Preserve existing AI worksheet for other lessons.
 event.preventDefault();event.stopImmediatePropagation();
 const grade=field("gradeSelect")||"الصف التاسع",subject=field("subjectSelect")||"فيزياء";
 const qs=new URLSearchParams({grade,subject,lesson:"Conducteurs ohmiques",language:field("languageSelect")||"Français"});
 try{
  const response=await originalFetch("/api/interactive-lessons/resolve?"+qs);
  if(!response.ok)throw Error("Drive worksheet not available");
  const data=await response.json(),u=new URL(data.url,location.origin);
  u.searchParams.set("worksheet","1");data.url=u.pathname+u.search;
  render(data,"worksheet","");
 }catch(error){
  console.warn("[NABIL_DRIVE_WORKSHEET] Using existing worksheet fallback",error);
  const fallback=document.getElementById("nabilWorksheetBtn");
  if(fallback){fallback.dataset.nabilDriveReplay="1";fallback.click();delete fallback.dataset.nabilDriveReplay;}
 }
},true);
window.fetch=async function(input,options){
 const url=typeof input==="string"?input:input?.url||"";
 const body=options?.body;
 if(!/\/api\/chat(?:\?|$)/.test(url)||!(body instanceof FormData)||busy)return originalFetch(input,options);
 const message=String(body.get("message")||"").trim();
 const active=document.getElementById("nabilDriveInteractiveLesson");
 const requestedNumber=message.match(/(?:التمرين|تمرين|رقم|exercise|exercice|ex\\.?|number)\\s*(?:رقم|number|no\\.?|n°)?\\s*[:#-]?\\s*(\\d{1,3})/i)?.[1];
 const isFollowup=/ما فهمت|مش فاهم|ما فهمنا|عيد|اعد|أعد|وضح|وضّح|بسط|بسّط|شرح تاني|explain again|don't understand|didn't understand|reexplain|réexplique|pas compris/i.test(message);
 if(active&&isFollowup&&(!requestedNumber||String(Number(requestedNumber))===String(Number(active.dataset.exercise)))){
  // The real AI can clarify the question, but must never replace the verified textbook exercise on screen.
  if(active.dataset.exercise&&!body.get("lesson"))body.set("lesson",active.dataset.lesson);
  if(active.dataset.exercise&&!body.get("grade"))body.set("grade","الصف التاسع");
  if(active.dataset.exercise&&!body.get("subject"))body.set("subject","فيزياء");
  console.info("[NABIL_HOME_DRIVE] Clarification keeps existing exercise visible",active.dataset.exercise);
  active.style.outline="3px solid #6fe2b9";
  active.scrollIntoView({behavior:"smooth",block:"start"});
  return originalFetch(input,options);
 }
 const request=classify(body);
 if(!request)return originalFetch(input,options);
 busy=true;
 try{
  const qs=new URLSearchParams({grade:request.grade,subject:request.subject,lesson:request.lesson,language:request.language});
  const result=await originalFetch("/api/interactive-lessons/resolve?"+qs);
  if(!result.ok){console.info("[NABIL_HOME_DRIVE] No verified prepared lesson; keeping existing AI fallback",result.status);return originalFetch(input,options);}
  const data=await result.json();
  const u=new URL(data.url,location.origin);
  if(request.mode==="exercise")u.searchParams.set("exercise",request.number);
  if(request.mode==="page")u.searchParams.set("page",request.number);
  if(request.mode==="worksheet")u.searchParams.set("worksheet","1");
  data.url=u.pathname+u.search;
  render(data,request.mode,request.number);
  console.info("[NABIL_HOME_DRIVE] Display verified Drive lesson without AI generation",request.mode,request.number||"");
  // Preserve the existing chat rendering contract, without starting a new AI generation.
  return new Response(JSON.stringify({conversation_id:String(body.get("conversation_id")||"drive-prepared-lesson"),
   reply:"📘 فتحت لك "+request.lesson+(request.mode==="exercise"?" — التمرين "+request.number:request.mode==="page"?" — صفحة الكتاب "+request.number:request.mode==="worksheet"?" — الورقة التفاعلية والبطاقة المرجعية":" — الدرس التفاعلي")+". الدرس جاهز من كتاب الدولة على Google Drive. اسألني عن أي فكرة إضافية.",
   sources:[],drawings:[]}),{status:200,headers:{"Content-Type":"application/json"}});
 }catch(error){
  console.warn("[NABIL_HOME_DRIVE] Lookup error; keeping existing AI fallback",error);
  return originalFetch(input,options);
 }finally{busy=false;}
};
})();