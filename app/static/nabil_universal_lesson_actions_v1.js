/* Universal lesson tools: existing answer -> PPTX / printable cards; exact exercise request. */
(()=>{
"use strict";
const $=id=>document.getElementById(id);
const chat=$("chat");
const scope=()=>({grade:$("gradeSelect")?.value||"",subject:$("subjectSelect")?.value||"",lesson:$("lessonSelect")?.value||"",language:$("languageSelect")?.value||""});
const button=(label,action)=>{const b=document.createElement("button");b.type="button";b.textContent=label;b.onclick=action;b.style.cssText="min-height:40px;max-width:100%;padding:8px 12px;border-radius:10px;border:1px solid #67dfda;background:#125268;color:#fff;cursor:pointer;white-space:normal";return b};
function answerNodes(){
 const result=$("nv132Result");
 const root=result&&!result.hidden?result:chat;
 if(!root)return [];
 const selectors=".message.teacher .bubble,.message.assistant .bubble,.teacher-message,.assistant-message,.nabil-answer-card,.lesson-card";
 const nodes=[...root.querySelectorAll(selectors)].filter(n=>!n.closest("#nabilUniversalLessonActions"));
 if(nodes.length)return nodes.slice(-20);
 // Never export the entire chat chrome or unverified text as if it were a lesson.
 const direct=[...root.children].filter(n=>n.matches?.(".message.teacher,.message.assistant,.lesson-card,.nabil-open-answer,.nv132-figure-card"));
 return direct.slice(-20);
}
async function figures(node){
 const output=[];
 for(const el of [...node.querySelectorAll("img,canvas,svg")].slice(0,4)){
  try{
   const canvas=document.createElement("canvas");
   let w=el.naturalWidth||el.width?.baseVal?.value||el.width||el.clientWidth||700;
   let h=el.naturalHeight||el.height?.baseVal?.value||el.height||el.clientHeight||450;
   w=Number(w)||700;h=Number(h)||450;
   const scale=Math.min(1,1200/Math.max(w,h));
   canvas.width=Math.max(1,Math.round(w*scale));canvas.height=Math.max(1,Math.round(h*scale));
   const ctx=canvas.getContext("2d");
   ctx.fillStyle="#ffffff";ctx.fillRect(0,0,canvas.width,canvas.height);
   if(el.tagName.toLowerCase()==="svg"){
    const xml=new XMLSerializer().serializeToString(el);
    const url=URL.createObjectURL(new Blob([xml],{type:"image/svg+xml"}));
    try{
     const img=new Image();img.src=url;await img.decode();
     ctx.drawImage(img,0,0,canvas.width,canvas.height);
    }finally{URL.revokeObjectURL(url)}
   }else ctx.drawImage(el,0,0,canvas.width,canvas.height);
   const png=canvas.toDataURL("image/png");
   if(png.length<3900000)output.push(png);
  }catch(e){console.info("[NABIL_EXPORT] Figure unavailable without inventing replacement",e)}
 }
 return output;
}
async function answers(){
 const nodes=answerNodes(),cards=[],images=[];
 for(const node of nodes){
  const copy=node.cloneNode(true);
  copy.querySelectorAll("button,script,style,nav,footer,.nabil-export-tools").forEach(n=>n.remove());
  const html=copy.innerHTML||copy.textContent||"";
  if(html.replace(/<[^>]+>/g,"").trim().length<15&&!node.querySelector("img,svg,canvas"))continue;
  cards.push(html);images.push(await figures(node));
 }
 return {cards,images};
}
async function exportCards(format,status){
 const v=scope();
 status.textContent="⏳ جارٍ تجهيز "+(format==="pptx"?"PowerPoint":"البطاقة المرجعية")+"…";
 try{
  let response;
  // When a textbook lesson is selected, export the authenticated Drive lesson,
  // not the unrelated last 20 chat messages or an AI answer about an error.
  if(v.grade&&v.subject&&v.lesson){
   const qs=new URLSearchParams({...v,format});
   response=await fetch("/api/lesson-export/prepared?"+qs.toString());
   if(!response.ok)throw Error("تعذّر تحميل الدرس الأصلي للتصدير (HTTP "+response.status+"). لم نصدّر محادثة بديلة.");
  }else{
   const {cards,images}=await answers();
   if(!cards.length){status.textContent="اعرض الدرس أو حلّ التمرين أولًا ثم جرّب التصدير.";return;}
   const title=[v.grade,v.subject,v.lesson].filter(Boolean).join(" — ")||"جواب الأستاذ نبيل";
   response=await fetch("/api/lesson-export/cards?format="+format,{
    method:"POST",headers:{"Content-Type":"application/json"},
    body:JSON.stringify({title,cards,images,source:"بطاقات جواب المحادثة، وليست نسخة موثّقة من الكتاب"})
   });
   if(!response.ok)throw Error("HTTP "+response.status);
  }
  const blob=await response.blob(),url=URL.createObjectURL(blob);
  const a=document.createElement("a");a.href=url;a.target="_blank";a.rel="noopener";
  if(format==="pptx"){a.download="NABIL_Lesson.pptx";a.click()}
  else{const opened=window.open(url,"_blank","noopener");if(!opened)status.textContent="اسمح بفتح نافذة البطاقة المرجعية."}
  status.textContent="✓ "+(format==="pptx"?"تم تجهيز PowerPoint":"فُتحت البطاقة المرجعية للطباعة");
  setTimeout(()=>URL.revokeObjectURL(url),120000);
 }catch(e){status.textContent="تعذّر التصدير: "+e.message}
}

function install(){
 if($("nabilUniversalLessonActions"))return;
 const dock=$("nabilLearningDock"),input=$("messageInput");
 if(!dock&&!input)return;
 const panel=document.createElement("section");panel.id="nabilUniversalLessonActions";
 panel.style.cssText="width:100%;max-width:100%;min-width:0;box-sizing:border-box;margin:10px 0;padding:12px;border:1px solid #357e91;border-radius:13px;background:#0d3047;color:#fff;display:flex;flex-wrap:wrap;align-items:center;gap:8px;overflow-wrap:anywhere";
 const heading=document.createElement("strong");heading.textContent="📘 أدوات الدرس والتمارين";heading.style.width="100%";
 const status=document.createElement("small");status.style.cssText="width:100%;color:#a9eae9;overflow-wrap:anywhere";
 panel.append(heading,button("📊 PowerPoint للدرس",()=>exportCards("pptx",status)),button("🗂️ البطاقة المرجعية",()=>exportCards("reference",status)));
 const row=document.createElement("div");row.style.cssText="display:flex;flex-wrap:wrap;gap:6px;width:100%;min-width:0;align-items:center";
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
const mobileStyle=document.createElement("style");mobileStyle.textContent="@media(max-width:900px){#nabilUniversalLessonActions{padding:10px!important;gap:7px!important}#nabilUniversalLessonActions>button{flex:1 1 140px!important;min-width:0!important}#nabilUniversalLessonActions input{flex:1 1 100px!important;min-width:0!important}#nabilUniversalLessonActions div button{flex:2 1 170px!important;min-width:0!important}}";document.head.appendChild(mobileStyle);
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",install);else install();
const observer=new MutationObserver(()=>{if(!$("nabilUniversalLessonActions"))install()});
observer.observe(document.body,{childList:true,subtree:false});
})();