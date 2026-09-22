/* Universal lesson tools: existing answer -> PPTX / printable cards; exact exercise request. */
(()=>{
"use strict";
const $=id=>document.getElementById(id);
const chat=$("chat");
const scope=()=>({grade:$("gradeSelect")?.value||"",subject:$("subjectSelect")?.value||"",lesson:$("lessonSelect")?.value||"",language:$("languageSelect")?.value||""});
const button=(label,action)=>{const b=document.createElement("button");b.type="button";b.textContent=label;b.onclick=action;b.style.cssText="min-height:40px;max-width:100%;padding:8px 12px;border-radius:10px;border:1px solid #67dfda;background:#125268;color:#fff;cursor:pointer;white-space:normal";return b};
function answers(){
 const root=$("nv132Result")&&!$("nv132Result").hidden?$("nv132Result"):chat;
 if(!root)return [];
 const nodes=[...root.querySelectorAll(".message.teacher .bubble,.message.assistant .bubble,.teacher-message,.assistant-message,.nabil-answer-card,.lesson-card")];
 const selected=nodes.length?nodes.slice(-20):[root];
 return selected.map(node=>{
  const copy=node.cloneNode(true);
  copy.querySelectorAll("button,script,style,nav,footer,.nabil-export-tools").forEach(n=>n.remove());
  return copy.innerHTML||copy.textContent||"";
 }).filter(t=>t.replace(/<[^>]+>/g,"").trim().length>15);
}
async function exportCards(format,status){
 const cards=answers();
 if(!cards.length){status.textContent="اعرض الدرس أو حلّ التمرين أولًا ثم جرّب التصدير.";return;}
 status.textContent="⏳ جارٍ تجهيز "+(format==="pptx"?"PowerPoint":"البطاقة المرجعية")+"…";
 try{
  const v=scope(),title=[v.grade,v.subject,v.lesson].filter(Boolean).join(" — ")||"درس الأستاذ نبيل";
  const response=await fetch("/api/lesson-export/cards?format="+format,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({title,cards,source:"الجواب المعروض للطالب في منصة NABIL AI"})});
  if(!response.ok)throw Error("HTTP "+response.status);
  const blob=await response.blob(),url=URL.createObjectURL(blob);
  const a=document.createElement("a");a.href=url;a.target="_blank";a.rel="noopener";
  if(format==="pptx"){a.download="NABIL_Lesson.pptx";a.click()}else{a.click()}
  status.textContent="✓ "+(format==="pptx"?"تم تجهيز PowerPoint":"فُتحت البطاقة المرجعية للطباعة");
  setTimeout(()=>URL.revokeObjectURL(url),120000);
 }catch(e){status.textContent="تعذّر التصدير: "+e.message}
}
function install(){
 if($("nabilUniversalLessonActions"))return;
 const dock=$("nabilLearningDock"),input=$("messageInput");
 if(!dock&&!input)return;
 const panel=document.createElement("section");panel.id="nabilUniversalLessonActions";
 panel.style.cssText="width:100%;box-sizing:border-box;margin:10px 0;padding:12px;border:1px solid #357e91;border-radius:13px;background:#0d3047;color:#fff;display:flex;flex-wrap:wrap;align-items:center;gap:8px";
 const heading=document.createElement("strong");heading.textContent="📘 أدوات الدرس والتمارين";heading.style.width="100%";
 const status=document.createElement("small");status.style.cssText="width:100%;color:#a9eae9;overflow-wrap:anywhere";
 panel.append(heading,button("📊 PowerPoint للدرس",()=>exportCards("pptx",status)),button("🗂️ البطاقة المرجعية",()=>exportCards("reference",status)));
 const row=document.createElement("div");row.style.cssText="display:flex;flex-wrap:wrap;gap:6px;width:100%;align-items:center";
 const number=document.createElement("input");number.id="nabilExactExerciseNumber";number.type="number";number.min="1";number.max="999";number.placeholder="رقم التمرين";number.setAttribute("aria-label","رقم التمرين المحدد");
 number.style.cssText="width:120px;max-width:45%;min-height:42px;border:1px solid #77e0dc;border-radius:9px;padding:7px;color:#102d42;background:#fff;font-size:16px";
 const ask=button("✍️ حلّ تمرين الكتاب المحدّد",()=>{
  const n=Number(number.value),v=scope();
  if(!Number.isInteger(n)||n<1||n>999){status.textContent="أدخل رقم تمرين صحيحًا من 1 إلى 999.";number.focus();return}
  if(!v.grade||!v.subject){status.textContent="اختر الصف والمادة أولًا.";return}
  const message="حلّ التمرين رقم "+n+" من كتاب "+v.subject+" للصف "+v.grade+". اعرض نصّه الحقيقي وفروعه ورسمه من الكتاب قبل الحل؛ لا تخترع أي معطيات أو نقاط من رسم غير مقروء.";
  if(typeof window.sendToAI==="function"){window.sendToAI(message,true);status.textContent="جارٍ طلب التمرين "+n+" من الكتاب…"}
  else if(input){input.value=message;input.focus();status.textContent="اضغط إرسال لطلب التمرين "+n}
 });
 row.append(number,ask);panel.append(row,status);
 if(dock)dock.insertAdjacentElement("afterend",panel);
 else input.closest(".input-area")?.insertAdjacentElement("beforebegin",panel);
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",install);else install();
const observer=new MutationObserver(()=>{if(!$("nabilUniversalLessonActions"))install()});
observer.observe(document.body,{childList:true,subtree:false});
})();