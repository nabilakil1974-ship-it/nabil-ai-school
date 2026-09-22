/* NABIL learning path v136: genuine AI activities, no invented XP or mastery. */
(()=>{
"use strict";
const dock=document.getElementById("nabilLearningDock");
if(!dock)return;
const byId=id=>document.getElementById(id);
// The owner wants the smart-learning dock BELOW the answer-copy/action bar.
// Move its real DOM node (not a duplicate) into the lesson column.
const lessonColumn=document.querySelector(".lesson-main-column");
const chat=byId("chat");
function placeDock(){
 // Keep the question box directly BELOW the learning path, not above it.
 const input=byId("messageInput");
 const composer=input?.closest(".input-area")||input?.closest("form")||input?.parentElement?.parentElement;
 if(composer&&composer.parentElement){
  if(composer.previousElementSibling!==dock)composer.insertAdjacentElement("beforebegin",dock);
 }else if(lessonColumn&&dock.parentElement!==lessonColumn){
  lessonColumn.appendChild(dock);
 }
}

placeDock();
const scope=()=>({
 grade:byId("gradeSelect")?.value||"",
 subject:byId("subjectSelect")?.value||"",
 lesson:byId("lessonSelect")?.value||"",
 language:byId("languageSelect")?.value||"العربية"
});
const gradeLevel=g=>{
 if(/روضة|تمهيد|kindergarten/i.test(g))return 0;
 if(/الأول|الثاني|الثالث/.test(g)&&!/ثانوي/.test(g))return 1;
 if(/الرابع|الخامس|السادس/.test(g))return 2;
 if(/السابع|الثامن|التاسع/.test(g))return 3;
 return 4;
};
const shortFor=level=>level<=1?"بكلمات قصيرة ومثال محسوس وسؤال واحد":level===2?"بمثال مرئي وتطبيق قصير":level===3?"بشرح السبب وخطوات الحل ثم سؤال": "بالمفاهيم والشروط والتحليل والتطبيق";
const hintFor=level=>level<=1?"3–5 دقائق":level===2?"5–8 دقائق":level===3?"8–12 دقيقة":"10–15 دقيقة";
const htmlEscape=text=>String(text??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
let currentProfile=null, busy=false, awaitingAnswer=false, lastAction="", lastScope="";
const controls=[
 ["solve_exercise","✍️ حلّ التمرين","حلّ التمرين الأخير الذي أعطيتك إياه أو الذي أرسلته. ابدأ بالمعطيات ثم خطوات الحل والتحقق والجواب النهائي. لا تعرض قالبًا عامًا أو عبارة Given data will appear here. أرفق رسمة حقيقية ودقيقة في بطاقة مستقلة إذا كان التمرين يتطلّب رسمًا؛ لا تخترع قياسات أو بيانات غير معطاة."],
 ["checkpoint","✓ تحقق من فهمي","اسألني سؤالاً واحداً عن الفكرة الأخيرة ولا تعطِ الحل قبل أن أحاول."],
 ["explain_another_way","🔄 اشرح بطريقة أخرى","ما فهمت الفكرة الأخيرة؛ بسّطها بطريقة مختلفة ومثال مناسب لمستواي، ولا تعيد الشرح حرفيًا."],
 ["adaptive_practice","🎯 تدريب يناسبني","اعطني تمريناً جديداً مناسباً لمستواي والدرس الحالي؛ لا تعطِ الجواب قبل محاولتي، وأرفق رسماً صحيحاً إن احتاجه السؤال."],
 ["flashcards","🗂️ بطاقات مراجعة","اعمل لي بطاقات سؤال وجواب قصيرة عن الدرس الحالي، مع مصطلحات الكتاب الأصلية."],
 ["quick_quiz","🏆 اختبار قصير","اعمل اختباراً قصيراً مناسباً لصفّي، ولا تكشف الحلول قبل ما أجيب."],
 ["study_plan","🧭 خطوتي التالية","اقترح لي خطوة عملية قصيرة لدراسة هذا الدرس بناءً فقط على أدائي المثبت. إذا ما عندك تقييم اطلب سؤال تحقق."],
 ["projector","🖥️ عرض على البروجكتور",""],
 ["dashboard","📊 تقدّمي",""]
];
dock.innerHTML='<div class="nv132-header"><strong>🧠 مسار التعلّم الذكي</strong><span id="nv132Context"></span><span id="nv132Evidence">بانتظار أول تقييم</span></div>'
 +'<p id="nv132Hint" class="nv132-hint"></p><div class="nv132-grid">'
 +controls.map(([id,label])=>'<button type="button" data-nv132="'+id+'">'+label+'</button>').join("")
 +'</div><p id="nv132Status" role="status" aria-live="polite">كل زر يبدأ نشاطًا حقيقيًا مع الأستاذ النبيل، ويتابع جوابك في المحادثة.</p>'
 +'<section id="nv132Result" aria-label="نتيجة نشاط التعلم الذكي" aria-live="polite" hidden></section>';
const css=document.createElement("style");
css.id="nabilLearningV132Style";
css.textContent='#nabilLearningDock{max-width:100%;height:auto!important;overflow:visible!important;background:#102940!important;border:1px solid #244e70!important;border-radius:15px!important;margin:12px auto!important;padding:14px!important;color:#f1f8ff!important;position:relative;z-index:2}#nabilLearningDock .nv132-header{display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:space-between}#nabilLearningDock .nv132-header strong{font-size:15px}#nv132Context,#nv132Evidence{border:1px solid #3b6d86;border-radius:20px;padding:4px 10px;font-size:12px}#nv132Evidence{color:#d9f4ff}#nabilLearningDock .nv132-hint{font-size:13px;line-height:1.65;margin:9px 0;color:#d4e5ef}#nabilLearningDock .nv132-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}#nabilLearningDock .nv132-grid button{border:1px solid #32678d;background:#123957;color:#fff;border-radius:10px;font:inherit;font-size:13px;min-height:42px;padding:8px 5px;cursor:pointer;white-space:normal}#nabilLearningDock .nv132-grid button:hover{background:#2670a0}#nabilLearningDock .nv132-grid button:disabled{opacity:.55;cursor:wait}#nv132Status{font-size:12px;line-height:1.55;margin:10px 0 0;color:#d7eaf5}#nv132Result{margin-top:12px;padding:12px;background:#0a2036;border:1px solid #32678d;border-radius:12px;max-height:none!important;overflow:visible!important}#nv132Result[hidden]{display:none!important}#nv132Result h3{margin:0 0 9px;color:#79d9ff}#nv132Result h4{color:#79d9ff;margin:12px 0 6px}#nv132Result .nv132-dashboard{line-height:1.65}#nv132Result .nv132-evidence-note{color:#b9d7e8;font-size:12px}#nv132Result .bubble{width:100%;max-width:100%;overflow-wrap:anywhere}#nv132Result svg{max-width:100%;height:auto}#nv132Result .nv132-figure-card{margin:16px 0 6px;padding:clamp(12px,2vw,24px);border:2px solid #2694c7;border-radius:16px;background:#081d32}#nv132Result .nv132-figure-card h3{margin:0 0 12px;font-size:clamp(17px,2vw,25px);color:#e9f9ff}#nv132Result .nv132-figure-item{padding:12px;background:#0a2945;border:1px solid #246c98;border-radius:12px;margin:8px auto}#nv132Result .nv132-figure-item svg,#nv132Result .nv132-figure-item canvas,#nv132Result .nv132-figure-item img{display:block;width:100%!important;max-width:100%!important;height:auto!important;min-height:clamp(240px,32vw,480px);object-fit:contain!important;margin:auto!important}#nv130Modal[hidden]{display:none!important}@media(max-width:720px){#nabilLearningDock .nv132-grid{grid-template-columns:repeat(2,minmax(0,1fr))}#nabilLearningDock{margin:8px 4px!important;padding:10px!important}#nabilLearningDock .nv132-grid button{font-size:12px;min-height:47px}}';
document.head.appendChild(css);
const status=t=>{let n=byId("nv132Status");if(n)n.textContent=t};
function markKeyRules(root=document){
 for(const node of root.querySelectorAll?.("h1,h2,h3,h4,strong,p")||[]){
  const t=String(node.textContent||"").trim();
  if(/^(?:🔴\s*)?(?:قاعدة أساسية|Key Rule|Règle essentielle)\s*[:：]?/i.test(t)){
   node.classList.add("nabil-key-rule");
  }
 }
}
async function toggleProjector(){
 const root=document.documentElement;
 try{
  if(!document.fullscreenElement){
   await root.requestFullscreen?.();
   document.body.classList.add("nabil-projector-mode");
   status("🖥️ وضع البروجكتور: الدرس يملأ الشاشة. اضغط نفس الزر أو Esc للخروج.");
  }else{
   await document.exitFullscreen?.();
   document.body.classList.remove("nabil-projector-mode");
   status("تم الخروج من وضع البروجكتور.");
  }
 }catch(_e){status("تعذّر فتح ملء الشاشة؛ اسمح للمتصفح بميزة Full Screen ثم جرّب مجددًا.");}
}
document.addEventListener("fullscreenchange",()=>{
 if(!document.fullscreenElement)document.body.classList.remove("nabil-projector-mode");
});

function showLastActivity(previous){
 const results=Array.from(document.querySelectorAll("#chat .message.teacher .bubble"));
 const latest=results[results.length-1];
 const panel=byId("nv132Result");
 if(!panel||!latest||latest===previous)return false;
 const latestText=String(latest.innerText||latest.textContent||"").trim();
 if(/حدث خطأ أثناء تنفيذ الطلب|تعذّر الاتصال|فشل إرسال|خطأ في الاتصال|server error|internal server error|given data will appear here/i.test(latestText)){
   throw Error("لم يصل حلّ صالح من الخادم. لم نعرض رسالة الخطأ كأنها حلّ تمرين.");
 }
 panel.replaceChildren();
 const header=document.createElement("h3");
 header.textContent="📘 نتيجة النشاط";
 const copy=latest.cloneNode(true);
 copy.removeAttribute("id");
 copy.querySelectorAll("[id]").forEach(node=>node.removeAttribute("id"));
 // Move actual diagram nodes into a separate full-width card rather than
 // shrinking a figure inside text, tables or the previous message wrapper.
 const figureNodes=[...copy.querySelectorAll("svg,canvas,img")].filter(el=>
   !el.closest("button") && !el.closest(".avatar,.teacher-avatar") &&
   (el.tagName.toLowerCase()!=="img"||/diagram|drawing|figure|visual|graph/i.test(el.className+" "+el.alt))
 );
 if(figureNodes.length){
   const card=document.createElement("section");
   card.className="nv132-figure-card";
   const title=document.createElement("h3");title.textContent="📐 الرسم التوضيحي";
   card.append(title);
   figureNodes.forEach(node=>{
     const holder=document.createElement("div");holder.className="nv132-figure-item";
     holder.append(node);card.append(holder);
   });
   panel.append(header,copy,card);
 }else{
   panel.append(header,copy);
 }
 panel.hidden=false;
 markKeyRules(panel);
 try{window.MathJax?.typesetPromise?.([panel])}catch(_e){}
 panel.scrollIntoView({behavior:"smooth",block:"nearest"});
 return true;
}
const setBusy=x=>{busy=x;dock.querySelectorAll("button").forEach(b=>b.disabled=x)};
function refresh(){
 const v=scope(),level=gradeLevel(v.grade),key=[v.grade,v.subject,v.lesson].join("|");
 if(lastScope&&lastScope!==key)awaitingAnswer=false;
 lastScope=key;
 byId("nv132Context").textContent=[v.grade,v.subject,v.lesson].filter(Boolean).join(" · ")||"حدّد الصف والدرس";
 byId("nv132Hint").textContent=level<=1?"نتعلّم بفكرة واحدة وصورة أو مثال وسؤال بسيط.":level===2?"نشوف المثال، نجرّب، ومنصحّح أول خطأ.":level===3?"منفهم السبب، منحلّ خطوة خطوة، وبعدها منتدرّب.":"نحلّل الفكرة وشروطها، نطبّق، ونتحقق بالدليل.";
 const marks=(currentProfile?.test_results||[]).filter(x=>x&&x.grade===v.grade&&x.subject===v.subject&&x.lesson===v.lesson&&typeof x.percent==="number");
 byId("nv132Evidence").textContent=marks.length?("آخر تقييم: "+Math.round(marks[marks.length-1].percent)+"% · "+marks.length+" تقييم"):"بانتظار تقييم فعلي";
}
function relevantProfile(p){
 const v=scope(), tests=(p.test_results||[]).filter(x=>x?.grade===v.grade&&x?.subject===v.subject&&x?.lesson===v.lesson);
 const review=(p.concepts_to_review||[]).slice(-6), errors=(p.frequent_mistakes||[]).slice(-6);
 return {tests,review,errors};
}
function dashboard(){
 const panel=byId("nv132Result");
 if(!panel){status("لوحة التقدّم غير متاحة حالياً.");return}
 const p=currentProfile;
 panel.hidden=false;
 panel.replaceChildren();
 const h=document.createElement("h3");h.textContent="📊 تقدّمي بالأدلة";panel.appendChild(h);
 if(!p){
   const note=document.createElement("p");
   note.textContent="ما في تقييم موثّق بعد. ابدأ بـ «تحقق من فهمي» أو «اختبار قصير»، وجاوب ليظهر تقدّم حقيقي.";
   panel.appendChild(note);
 }else{
   const {tests,review,errors}=relevantProfile(p),t=tests[tests.length-1];
   const box=document.createElement("div");
   box.className="nv132-dashboard";
   box.innerHTML="<p><strong>آخر تقييم لهذا الدرس:</strong> "+(t?htmlEscape(t.score)+" / "+htmlEscape(t.out_of)+" ("+Math.round(t.percent)+"%)":"لم يجر تقييم بعد")+"</p>"
    +"<p><strong>عدد التقييمات الموثّقة:</strong> "+tests.length+"</p>"
    +"<h4>مفاهيم تحتاج مراجعة</h4>"+(review.length?"<ul>"+review.map(x=>"<li>"+htmlEscape(x)+"</li>").join("")+"</ul>":"<p>لم تُسجّل مفاهيم تحتاج مراجعة بعد.</p>")
    +"<h4>أخطاء موثّقة</h4>"+(errors.length?"<ul>"+errors.map(x=>"<li>"+htmlEscape(x)+"</li>").join("")+"</ul>":"<p>لا توجد أخطاء مصحّحة مسجّلة بعد.</p>")
    +"<p class='nv132-evidence-note'>لا نحسب الإتقان من عدد النقرات؛ نعرض فقط نتائج تقييم حقيقية محفوظة.</p>";
   panel.appendChild(box);
 }
 status("عرضت التقدّم الموثّق لهذا الدرس.");
 panel.scrollIntoView({behavior:"smooth",block:"nearest"});
}
async function act(action){
 if(busy)return;
 if(action==="projector"){toggleProjector();return}
 if(action==="dashboard"){dashboard();return}
 const v=scope(),level=gradeLevel(v.grade);
 const latestQuestion=String(typeof nabilCurrentQuestionText!=="undefined"?nabilCurrentQuestionText:"").trim();
 const teacherBubbles=[...document.querySelectorAll("#chat .message.teacher .bubble")];
 const lastTeacher=teacherBubbles[teacherBubbles.length-1]||null;
 if(!v.grade&&!v.subject&&!latestQuestion&&!lastTeacher){
  status("اسأل الأستاذ نبيل سؤالك أولًا؛ بعدها كل زر يبني نشاطًا على جوابك.");return;
 }
 const item=controls.find(x=>x[0]===action),period=v.grade?hintFor(level):"حسب مستوى السؤال";
 if(action==="solve_exercise"&&!latestQuestion&&!lastTeacher){
   status("اكتب التمرين أو ارفع صورته أولًا، ثم اضغط «حلّ التمرين».");return;
 }
 const question=item[2]+" مراعاة العمر: "+(v.grade?shortFor(level):"لا تفترض عمر الطالب؛ تكيّف مع مستوى آخر سؤال")+ ". وقت النشاط المقترح "+period+". "+(v.lesson?"الدرس: "+v.lesson+". ":"")+(latestQuestion?"السؤال الذي نتعلّم منه: "+latestQuestion.slice(0,650)+". ":"")+"افهم كلامي العربي ولو كانت مادة الدرس "+v.language+"؛ احتفظ بالمصطلحات العلمية بلغة الكتاب. وإذا كان السؤال الأصلي English أو Français، اسأل وقدّم النشاط بلغته.";
 const previousAnswer=Array.from(document.querySelectorAll("#chat .message.teacher .bubble")).at(-1);
 byId("nv132Result").hidden=true;
 setBusy(true);lastAction=action;status("الأستاذ نبيل عم يحضّر "+item[1]+(v.grade?(" للصف "+v.grade):"")+" من نفس محتوى الدرس/السؤال…");
 window.nabilPendingLearningAction=action;
 try{
  // A silent legacy send must not leave the student waiting without feedback.
  // The request can take time for lesson grounding and drawing; keep the
  // status visible at 20s and apply a terminal UI timeout after 85s.
  let waiting=true;
  const lateNotice=setTimeout(()=>{
   if(waiting)status("⏳ ما زلنا بانتظار حلّ التمرين. إذا تأخر، سيظهر تنبيه ويمكنك إعادة المحاولة.");
  },20000);
  try{
   await Promise.race([
    Promise.resolve().then(()=>sendToAI(question,false)),
    new Promise((_,reject)=>setTimeout(()=>reject(Error("تأخر حل التمرين أكثر من 85 ثانية؛ لم يتم تسليم جواب، جرّب مجددًا.")),85000))
   ]);
  }finally{waiting=false;clearTimeout(lateNotice);}
  if(!showLastActivity(previousAnswer))throw Error("لم يصل حلّ جديد. تأكد من اتصال الخادم وأعد إرسال التمرين.");
  awaitingAnswer=["checkpoint","adaptive_practice","quick_quiz"].includes(action);
  status(awaitingAnswer?"جاوب داخل خانة السؤال، والأستاذ نبيل بيصحّح محاولتك قبل الانتقال.":"حلّ التمرين ظاهر في بطاقة منسّقة، والرسم في بطاقة مستقلة إن عاد من الخادم.");
 }catch(e){status("ما اكتمل الطلب: "+String(e?.message||"تعذر الاتصال").slice(0,160))}
 finally{window.nabilPendingLearningAction="";setBusy(false)}
}
dock.addEventListener("click",ev=>{const b=ev.target.closest("[data-nv132]");if(b)act(b.dataset.nv132)});
for(const id of ["gradeSelect","subjectSelect","lessonSelect","languageSelect"])byId(id)?.addEventListener("change",refresh);
const previous=window.addMessage;
if(typeof previous==="function")window.addMessage=function(role,text,...rest){
 const value=previous.call(this,role,text,...rest);
 if(role==="teacher"){refresh();setTimeout(()=>{placeDock();markKeyRules(document)},0)}
 return value;
};
const originalSend=window.sendToAI;
if(typeof originalSend==="function")window.sendToAI=async function(message,showStudentMessage=true){
 if(awaitingAnswer&&showStudentMessage&&String(message||"").trim()&&!window.nabilPendingLearningAction){
  awaitingAnswer=false;
  window.nabilPendingLearningAction="assess_answer";
  try{return await originalSend.apply(this,arguments)}
  finally{window.nabilPendingLearningAction="";status("إذا كانت إجابتك مصحّحة، راجع التقدّم أو اطلب تدريبًا إضافيًا.")}
 }
 return originalSend.apply(this,arguments);
};
const oldMerge=window.NABIL130?.mergeProfile;
window.NABIL130={
 ...(window.NABIL130||{}),
 checkpoint:()=>act("checkpoint"),explainAgain:()=>act("explain_another_way"),
 practice:()=>act("adaptive_practice"),flashcards:()=>act("flashcards"),
 quickQuiz:()=>act("quick_quiz"),dashboard,studyPlan:()=>act("study_plan"),
 mergeProfile:p=>{if(p&&typeof p==="object"){currentProfile=p;refresh()}},
 state:()=>({profile:currentProfile,awaitingAnswer}),
 reset:()=>status("نتائج التعلّم محفوظة في حساب الطالب ولا تُصفّر بالنقر.")
};
refresh();
placeDock();
if(chat){
 const observer=new MutationObserver(()=>placeDock());
 observer.observe(chat,{childList:true});
}
})();
