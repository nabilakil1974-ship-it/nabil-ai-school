/* NABIL learning path v132: genuine AI activities, no invented XP or mastery. */
(()=>{
"use strict";
const dock=document.getElementById("nabilLearningDock");
if(!dock)return;
const byId=id=>document.getElementById(id);
// The owner wants the smart-learning dock BELOW the answer-copy/action bar.
// Move its real DOM node (not a duplicate) into the lesson column.
const answerActions=document.querySelector(".lesson-main-column .lesson-action-bar");
if(answerActions) answerActions.insertAdjacentElement("afterend",dock);
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
 ["checkpoint","✓ تحقق من فهمي","اسألني سؤالاً واحداً عن الفكرة الأخيرة ولا تعطِ الحل قبل أن أحاول."],
 ["explain_another_way","🔄 اشرح بطريقة أخرى","ما فهمت الفكرة الأخيرة؛ بسّطها بطريقة مختلفة ومثال مناسب لمستواي، ولا تعيد الشرح حرفيًا."],
 ["adaptive_practice","🎯 تدريب يناسبني","اعطني تمريناً جديداً مناسباً لمستواي والدرس الحالي؛ لا تعطِ الجواب قبل محاولتي، وأرفق رسماً صحيحاً إن احتاجه السؤال."],
 ["flashcards","🗂️ بطاقات مراجعة","اعمل لي بطاقات سؤال وجواب قصيرة عن الدرس الحالي، مع مصطلحات الكتاب الأصلية."],
 ["quick_quiz","🏆 اختبار قصير","اعمل اختباراً قصيراً مناسباً لصفّي، ولا تكشف الحلول قبل ما أجيب."],
 ["study_plan","🧭 خطوتي التالية","اقترح لي خطوة عملية قصيرة لدراسة هذا الدرس بناءً فقط على أدائي المثبت. إذا ما عندك تقييم اطلب سؤال تحقق."],
 ["dashboard","📊 تقدّمي",""]
];
dock.innerHTML='<div class="nv132-header"><strong>🧠 مسار التعلّم الذكي</strong><span id="nv132Context"></span><span id="nv132Evidence">بانتظار أول تقييم</span></div>'
 +'<p id="nv132Hint" class="nv132-hint"></p><div class="nv132-grid">'
 +controls.map(([id,label])=>'<button type="button" data-nv132="'+id+'">'+label+'</button>').join("")
 +'</div><p id="nv132Status" role="status" aria-live="polite">كل زر يبدأ نشاطًا حقيقيًا مع الأستاذ النبيل، ويتابع جوابك في المحادثة.</p>';
const css=document.createElement("style");
css.id="nabilLearningV132Style";
css.textContent='#nabilLearningDock{max-width:100%;height:auto!important;overflow:visible!important;background:#102940!important;border:1px solid #244e70!important;border-radius:15px!important;margin:12px auto!important;padding:14px!important;color:#f1f8ff!important;position:relative;z-index:2}#nabilLearningDock .nv132-header{display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:space-between}#nabilLearningDock .nv132-header strong{font-size:15px}#nv132Context,#nv132Evidence{border:1px solid #3b6d86;border-radius:20px;padding:4px 10px;font-size:12px}#nv132Evidence{color:#d9f4ff}#nabilLearningDock .nv132-hint{font-size:13px;line-height:1.65;margin:9px 0;color:#d4e5ef}#nabilLearningDock .nv132-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}#nabilLearningDock .nv132-grid button{border:1px solid #32678d;background:#123957;color:#fff;border-radius:10px;font:inherit;font-size:13px;min-height:42px;padding:8px 5px;cursor:pointer;white-space:normal}#nabilLearningDock .nv132-grid button:hover{background:#2670a0}#nabilLearningDock .nv132-grid button:disabled{opacity:.55;cursor:wait}#nv132Status{font-size:12px;line-height:1.55;margin:10px 0 0;color:#d7eaf5}#nv130Modal[hidden]{display:none!important}@media(max-width:720px){#nabilLearningDock .nv132-grid{grid-template-columns:repeat(2,minmax(0,1fr))}#nabilLearningDock{margin:8px 4px!important;padding:10px!important}#nabilLearningDock .nv132-grid button{font-size:12px;min-height:47px}}';
document.head.appendChild(css);
const status=t=>{let n=byId("nv132Status");if(n)n.textContent=t};
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
 const p=currentProfile;
 const old=byId("nv130Modal"),title=byId("nv130ModalTitle"),body=byId("nv130ModalBody");
 if(!old||!title||!body){status("لوحة التقدّم غير متاحة؛ اطلب اختبارًا لنقيس المستوى.");return}
 title.textContent="📊 تقدّمي بالأدلة";
 if(!p)body.innerHTML="<p>لم تصل نتائج من قاعدة بيانات التعلّم بعد. ابدأ بسؤال تحقق وجاوب عليه.</p>";
 else{
  const {tests,review,errors}=relevantProfile(p),t=tests[tests.length-1];
  body.innerHTML="<p><strong>آخر تقييم لهذا الدرس:</strong> "+(t?htmlEscape(t.score)+" / "+htmlEscape(t.out_of)+" ("+Math.round(t.percent)+"%)":"لم يجر تقييم بعد")+"</p>"
   +"<p><strong>عدد التقييمات:</strong> "+tests.length+"</p>"
   +"<h3>مفاهيم تحتاج مراجعة</h3>"+(review.length?"<ul>"+review.map(x=>"<li>"+htmlEscape(x)+"</li>").join("")+"</ul>":"<p>لم تُسجّل مفاهيم تحتاج مراجعة بعد.</p>")
   +"<h3>أخطاء موثّقة</h3>"+(errors.length?"<ul>"+errors.map(x=>"<li>"+htmlEscape(x)+"</li>").join("")+"</ul>":"<p>لا أخطاء مصحّحة مسجلة بعد، ولا يعني ذلك إتقان كل الأفكار.</p>")
   +"<p>النسبة ليست محسوبة من عدد النقرات أو طول المحادثة؛ تُعرض فقط نتائج التقييم الموثّقة.</p>";
 }
 old.hidden=false;
}
async function act(action){
 if(busy)return;
 if(action==="dashboard"){dashboard();return}
 const v=scope(),level=gradeLevel(v.grade);
 if(!v.grade||!v.subject){status("اختر الصف والمادة أولًا، لنحضّر نشاطًا مناسبًا.");return}
 const item=controls.find(x=>x[0]===action),period=hintFor(level);
 const question=item[2]+" مراعاة العمر: "+shortFor(level)+". وقت النشاط المقترح "+period+". "+(v.lesson?"الدرس: "+v.lesson+". ":"")+"افهم كلامي العربي ولو كانت مادة الدرس "+v.language+"؛ احتفظ بالمصطلحات العلمية بلغة الكتاب.";
 setBusy(true);lastAction=action;status("الأستاذ نبيل عم يحضّر نشاط "+item[1]+" للصف "+v.grade+"…");
 window.nabilPendingLearningAction=action;
 try{
  await sendToAI(question,false);
  awaitingAnswer=["checkpoint","adaptive_practice","quick_quiz"].includes(action);
  status(awaitingAnswer?"جاوب داخل خانة السؤال، والأستاذ نبيل بيصحّح محاولتك قبل الانتقال.":"النشاط ظهر بالمحادثة. إذا ما فهمت خطوة، اسأل عنها مباشرة.");
 }catch(e){status("ما اكتمل الطلب: "+String(e?.message||"تعذر الاتصال").slice(0,160))}
 finally{window.nabilPendingLearningAction="";setBusy(false)}
}
dock.addEventListener("click",ev=>{const b=ev.target.closest("[data-nv132]");if(b)act(b.dataset.nv132)});
for(const id of ["gradeSelect","subjectSelect","lessonSelect","languageSelect"])byId(id)?.addEventListener("change",refresh);
const previous=window.addMessage;
if(typeof previous==="function")window.addMessage=function(role,text,...rest){
 const value=previous.call(this,role,text,...rest);
 if(role==="teacher")refresh();
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
})();
