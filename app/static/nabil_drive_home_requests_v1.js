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
// Multiple colloquial exercise requests: keep subjects separate and never invent an unseen textbook question.
const subjectAliases=[
 {name:"الفيزياء",key:"physics",color:"#1786c7",rx:/(?:فيزيا|فيزياء|الفيزيا|physique|physics|phys)/i},
 {name:"الكيمياء",key:"chemistry",color:"#15946d",rx:/(?:كيميا|كيمياء|الكيميا|chimie|chemistry|chem)/i},
 {name:"الرياضيات",key:"mathematics",color:"#8655c8",rx:/(?:رياضيات|الرياضيات|رياضة|maths?|mathematics|mathématiques)/i}
];
let lastExerciseBatch=[];
function parseExerciseBatch(message){
 const normalized=message.replace(/[٠-٩]/g,c=>String("٠١٢٣٤٥٦٧٨٩".indexOf(c))).replace(/[۰-۹]/g,c=>String("۰۱۲۳۴۵۶۷۸۹".indexOf(c)));
 const pattern=/(?:التمرين\s*)?(?:رقم\s*)?(\d{1,3})\s*(?:ب?ال?\s*)?(فيزيا|فيزياء|physique|physics|phys|كيميا|كيمياء|chimie|chemistry|chem|رياضيات|رياضة|maths?|mathematics|mathématiques)|(?:فيزيا|فيزياء|physique|physics|phys|كيميا|كيمياء|chimie|chemistry|chem|رياضيات|رياضة|maths?|mathematics|mathématiques)\s*(?:التمرين\s*)?(?:رقم\s*)?(\d{1,3})/gi;
 const found=[];let match;
 while((match=pattern.exec(normalized))){
  const number=Number(match[1]||match[3]),word=match[2]||match[0].replace(/[\d\s]/g,"");
  const subject=subjectAliases.find(item=>item.rx.test(word));
  if(subject&&number>0&&!found.some(item=>item.key===subject.key&&item.number===number))
   found.push({...subject,number});
 }
 return found.length>=2?found:[];
}
function showExerciseBatch(items){
 const chat=document.getElementById("chat");if(!chat)return;
 document.getElementById("nabilMultiExerciseQueue")?.remove();
 const panel=document.createElement("section");panel.id="nabilMultiExerciseQueue";
 panel.style.cssText="width:100%;box-sizing:border-box;margin:12px 0;padding:12px;background:#092238;border-radius:14px;border:1px solid #80d9ef;color:white";
 const heading=document.createElement("strong");heading.textContent="📚 صفحة التمارين · حسب ترتيب طلبك";
 panel.append(heading);
 for(const item of items){
  const card=document.createElement("div");card.dataset.subject=item.key;card.dataset.exercise=String(item.number);
  card.style.cssText="margin:10px 0;padding:12px;border-radius:12px;border-inline-start:7px solid "+item.color+";background:#17334b;color:#fff";
  const label=document.createElement("strong");label.textContent=item.name+" — التمرين "+item.number;
  const note=document.createElement("p");note.style.cssText="font-size:13px;margin:6px 0 0;color:#d5eaf6";
  note.textContent="سيعالج نبيل هذا التمرين مستقلًا، بحسب الكتاب والصف المحدّدين؛ إن لم يتوفر نص السؤال يطلب صورته ولا يخترعه.";
  card.append(label,note);panel.append(card);
 }
 chat.append(panel);panel.scrollIntoView({behavior:"smooth",block:"start"});
}
function batchInstruction(items,grade,original){
 return "[MULTI-SUBJECT EXERCISE REQUEST — user text follows]\n"+original+
 "\n[END USER TEXT]\nطلب الطالب "+items.length+" تمارين مستقلة بالترتيب التالي:\n"+
 items.map((item,i)=>(i+1)+". "+item.name+" — التمرين "+item.number).join("\n")+
 "\nالصف المحدد: "+(grade||"غير محدد")+
 "\nتعليمات إلزامية: لا تخلط المواد ولا تغيّر أرقام التمارين أو ترتيبها. ضع عنوانًا واضحًا لكل مادة ورقم تمرين، واستخرج السؤال الحقيقي من كتاب تلك المادة والصف إذا كان متاحًا وموثقًا؛ إذا لم تتمكن من تحديد نص تمرين بعينه فلا تخترع معطياته أو حلًا مفترضًا، بل اطلب صورة التمرين أو اسم الكتاب/الصف عند الحاجة. لا تعتبر الدرس المحدد في واجهة مادة أخرى مصدرًا لجميع التمارين. كل تمرين ببطاقة مستقلة ورسوماته وخطواته العلمية الصحيحة؛ استخدم LaTeX للكسور والجذور والأسس والوحدات. فهم العامية مسموح، أما قراءة الأعداد بالعربية فصيحة: اثنا عشر لا اتناش. الصوت لا يقرأ علامات LaTeX أو شرطات أو أوامر تنسيق.\n";
}
// PDF/Word exercise upload uses the existing /api/chat conversation and textbook RAG.
let selectedDocument=null;
function installDocumentUpload(){
 if(document.getElementById("nabilExerciseDocumentInput"))return;
 const input=document.getElementById("messageInput");if(!input)return;
 const row=input.closest(".input-area")||input.parentElement;
 if(!row)return;
 const picker=document.createElement("input");picker.id="nabilExerciseDocumentInput";picker.type="file";
 picker.accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document";
 picker.style.display="none";
 const button=document.createElement("button");button.type="button";button.id="nabilExerciseDocumentButton";
 button.textContent="📄 PDF / Word";button.title="ارفع تمارين PDF أو Word ليحلها نبيل";
 button.style.cssText="background:#225c65;color:#fff;border:2px solid #6ee6cb;border-radius:10px;padding:10px;cursor:pointer;min-height:44px";
 const label=document.createElement("span");label.id="nabilExerciseDocumentStatus";
 label.style.cssText="color:#a6ffe3;font:12px Arial;max-width:200px;overflow-wrap:anywhere";
 button.onclick=()=>picker.click();
 picker.onchange=()=>{
  const file=picker.files?.[0];if(!file)return;
  if(!/\.(pdf|docx)$/i.test(file.name)||file.size>12000000){
   alert("ارفع PDF أو DOCX بحجم لا يتجاوز 12 MB.");picker.value="";return;
  }
  selectedDocument=file;label.textContent="📎 "+file.name+" · جاهز للإرسال";
  if(!input.value.trim())input.value="حل تمارين هذا الملف بالمعطيات والمطلوب والقانون وخطوات الحل.";
 };
 row.append(button,picker,label);
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",installDocumentUpload);
else installDocumentUpload();
window.fetch=async function(input,options){
 const url=typeof input==="string"?input:input?.url||"";
 const body=options?.body;
 if(!/\/api\/chat(?:\?|$)/.test(url)||!(body instanceof FormData)||busy)return originalFetch(input,options);
 if(selectedDocument){
  body.set("document",selectedDocument,selectedDocument.name);
  const sent=selectedDocument;selectedDocument=null;
  document.getElementById("nabilExerciseDocumentStatus").textContent="📄 جارٍ إرسال "+sent.name;
  try{
   const response=await originalFetch(input,options);
   if(!response.ok){selectedDocument=sent;document.getElementById("nabilExerciseDocumentStatus").textContent="⚠️ تعذّر الإرسال؛ الملف محفوظ لإعادة المحاولة";}
   else{document.getElementById("nabilExerciseDocumentStatus").textContent="✓ تم إرسال "+sent.name;document.getElementById("nabilExerciseDocumentInput").value="";}
   return response;
  }catch(error){selectedDocument=sent;throw error;}
 }
 const message=String(body.get("message")||"").trim();
 const batch=parseExerciseBatch(message);
 if(batch.length){
  lastExerciseBatch=batch;showExerciseBatch(batch);
  body.set("message",batchInstruction(batch,field("gradeSelect")||String(body.get("grade")||""),message));
  body.set("lesson","");body.set("subject","");
  return originalFetch(input,options);
 }
 const active=document.getElementById("nabilDriveInteractiveLesson");
 const requestedNumber=message.match(/(?:التمرين|تمرين|رقم|exercise|exercice|ex\.?|number)\s*(?:رقم|number|no\.?|n°)?\s*[:#-]?\s*(\d{1,3})/i)?.[1];
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