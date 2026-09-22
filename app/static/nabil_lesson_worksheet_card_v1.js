/* Universal end-of-lesson worksheet card: no hardcoded lesson content. */
(()=>{
"use strict";
const chat=document.getElementById("chat");
if(!chat)return;
const id=x=>document.getElementById(x);
const card=document.createElement("section");
card.id="nabilLessonWorksheetCard";
card.dir="rtl";
card.hidden=true;
card.innerHTML='<strong>📘 اكتمل شرح الدرس — تابع بالتطبيق</strong><p>🧩 ورقة عمل تفاعلية لهذا الدرس: أنشطة وأسئلة وتصحيح محاولاتك خطوة بخطوة، بالاعتماد على صفحات الكتاب المسترجعة عند توفرها.</p><button type="button" id="nabilOpenLessonWorksheet">📝 افتح ورقة العمل التفاعلية</button>';
const style=document.createElement("style");
style.textContent='#nabilLessonWorksheetCard{box-sizing:border-box;width:100%;max-width:100%;margin:12px 0;padding:16px;border:2px solid #27b7db;border-radius:17px;background:#09263f;color:#effaff;line-height:1.65;overflow-wrap:anywhere}#nabilLessonWorksheetCard[hidden]{display:none!important}#nabilLessonWorksheetCard strong{color:#7ce9ff;font-size:clamp(16px,3vw,21px)}#nabilLessonWorksheetCard p{margin:10px 0}#nabilOpenLessonWorksheet{border:1px solid #6ee9ff;border-radius:12px;background:#087c9f;color:white;padding:12px 17px;font:inherit;font-weight:700;cursor:pointer;max-width:100%;white-space:normal}';
document.head.append(style);
let previous=null;
function place(){
 const teachers=[...chat.querySelectorAll(".message.teacher")];
 const latest=teachers[teachers.length-1];
 const selected=!!id("gradeSelect")?.value&&!!id("subjectSelect")?.value&&!!id("lessonSelect")?.value;
 const body=latest?.innerText||"";
 // Show after a complete lesson, not after a short page/exercise answer.
 const full=/(خلاصة الدرس|ملخص الدرس|lesson summary|résumé de la leçon|récapitulatif du cours)/i.test(body);
 if(!latest||!selected||!full){card.hidden=true;return}
 card.hidden=false;
 const dock=id("nabilLearningDock");
 const anchor=dock&&dock.previousElementSibling===latest?dock:latest;
 if(card.previousElementSibling!==anchor)anchor.insertAdjacentElement("afterend",card);
 previous=latest;
}
card.querySelector("button").addEventListener("click",()=>{
 const button=id("nabilWorksheetBtn");
 if(!button){alert("ورقة العمل غير متاحة حاليًا. أعد تحميل الصفحة.");return}
 button.click();
});
const observer=new MutationObserver(()=>place());
observer.observe(chat,{childList:true,subtree:true,characterData:true});
["gradeSelect","subjectSelect","lessonSelect"].forEach(name=>id(name)?.addEventListener("change",place));
place();
})();