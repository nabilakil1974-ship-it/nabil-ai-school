/* Opt-in postgraduate research workspace: independent of school grade selectors. */
(()=>{
"use strict";
const tutor=document.getElementById("nabilOpenTutor");
if(!tutor)return;
const button=document.createElement("button");
button.type="button";
button.id="nabilResearchToggle";
button.textContent="🎓 بحث ماجستير / دكتوراه";
button.style.cssText="margin:12px 0;padding:11px 15px;border:1px solid #37c6f2;border-radius:11px;background:#12395b;color:white;cursor:pointer;font:inherit";
const header=tutor.querySelector(".nabil-open-head");
(header||tutor).after(button);
const panel=document.createElement("section");
panel.id="nabilResearchWorkspace";
panel.hidden=true;
panel.dir="rtl";
panel.style.cssText="box-sizing:border-box;width:100%;max-width:100%;padding:14px;background:#0e2439;border:1px solid #237ba8;border-radius:12px;color:#fff;margin:10px 0;overflow-wrap:anywhere";
const heading=document.createElement("h3");
heading.textContent="🎓 مساحة البحث الأكاديمي — مسودة قابلة للمراجعة والتصدير";
panel.append(heading);
const note=document.createElement("p");
note.textContent="أدخل عنوان الرسالة وخطوطها العريضة. نعمل مرحلةً مرحلة؛ لا نختلق مصادر أو نتائج ميدانية. الإنشاء الحقيقي لـ Google Forms يحتاج ربط حساب مصرحًا به.";
panel.append(note);
function label(text, control){const box=document.createElement("label");box.style.cssText="display:block;margin:10px 0";box.append(document.createTextNode(text));control.style.cssText="display:block;box-sizing:border-box;width:100%;min-width:0;margin-top:5px;padding:9px;background:#091b2a;color:white;border:1px solid #3882af;border-radius:6px;font:inherit";box.append(control);panel.append(box);return control;}
const degree=document.createElement("select");
for(const [value,name] of [["masters","ماجستير"],["doctorate","دكتوراه"]]){const o=document.createElement("option");o.value=value;o.textContent=name;degree.append(o);}
label("الدرجة العلمية",degree);
const title=label("عنوان الرسالة",document.createElement("input"));
title.maxLength=500;title.placeholder="اكتب عنوان البحث";
const outline=label("الخطوط العريضة وأفكار الباحث",document.createElement("textarea"));
outline.rows=5;outline.maxLength=12000;outline.placeholder="مشكلة البحث، المحاور، الأهداف، الفرضيات، المنهج...";
const sources=label("مراجع ومقاطع يقدمها الباحث — لا تُعدّ متحققًا منها تلقائيًا",document.createElement("textarea"));
sources.rows=3;sources.maxLength=15000;
const language=document.createElement("select");
for(const [v,name] of [["ar","العربية"],["en","English"],["fr","Français"]]){const o=document.createElement("option");o.value=v;o.textContent=name;language.append(o);}
label("لغة البحث",language);
const guidance=label("ملاحظات الباحث أو متطلبات الجامعة",document.createElement("textarea"));
guidance.rows=2;guidance.maxLength=4000;
const stages=document.createElement("div");stages.style.cssText="display:flex;flex-wrap:wrap;gap:8px;margin:12px 0";panel.append(stages);
const output=document.createElement("pre");
output.id="nabilResearchDraft";
output.style.cssText="white-space:pre-wrap;word-break:break-word;max-width:100%;font:inherit;line-height:1.8;background:#091b2a;padding:12px;border:1px solid #22648d;border-radius:8px;max-height:55vh;overflow:auto";
output.textContent="اختر المرحلة للبدء.";
const status=document.createElement("p");status.setAttribute("role","status");panel.append(status);
let manuscript="";
let busy=false;
function setStatus(t){status.textContent=t;}
function validate(){if(title.value.trim().length<8||outline.value.trim().length<5){setStatus("أدخل عنوانًا واضحًا وخطوطًا عريضة للبحث أولًا.");return false;}return true;}
async function post(path,payload){
 const response=await fetch(path,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});
 if(!response.ok){let message="تعذّر تنفيذ الطلب. حاول مجددًا.";try{const data=await response.json();message=String(data.detail||message)}catch(_){}throw Error(message);}
 return response;
}
function state(){return {degree:degree.value,title:title.value.trim(),outline:outline.value.trim(),sources:sources.value.trim(),guidance:guidance.value.trim(),language:language.value};}
const stageLabels=[["proposal","خطة البحث"],["theoretical","الإطار النظري"],["practical","الإطار التطبيقي"],["questionnaire","أسئلة الاستبيان"],["revision","مراجعة المسودة"]];
for(const [stage,name] of stageLabels){
 const action=document.createElement("button");action.type="button";action.textContent=name;
 action.style.cssText="padding:9px;border:1px solid #2baee8;border-radius:7px;background:#14619a;color:white;cursor:pointer;font:inherit";
 action.addEventListener("click",async()=>{
   if(busy||!validate())return;
   busy=true;setStatus("جارٍ إعداد "+name+"... احتفظ بنصوص الباحث ومراجعها.");
   try{
     const payload={...state(),stage,previous_text:manuscript.slice(-35000)};
     const result=await (await post("/api/research/draft",payload)).json();
     if(!result.text)throw Error("لم يصل نص من الخدمة.");
     manuscript+=(manuscript?"\n\n":"")+"# "+name+"\n"+result.text;
     output.textContent=manuscript;
     setStatus("تم إنشاء "+name+". هذه مسودة، وليست رسالة مكتملة أو مصادر متحققة.");
   }catch(err){setStatus(err.message||"حدث خطأ ولم تُفقد المسودة.");}
   finally{busy=false;}
 });
 stages.append(action);
}
panel.append(output);
const download=document.createElement("button");download.type="button";download.textContent="⬇ تصدير المسودة Word";
download.style.cssText="margin:8px;padding:10px;background:#178d57;color:white;border:0;border-radius:8px;font:inherit;cursor:pointer";
async function saveResponse(response,name){
 const blob=await response.blob();const url=URL.createObjectURL(blob);const a=document.createElement("a");
 a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),30000);
}
download.addEventListener("click",async()=>{
 if(!manuscript||busy){setStatus("أنشئ مسودة أولًا.");return;}
 try{setStatus("جارٍ تجهيز ملف Word...");const data={degree:degree.value,title:title.value,language:language.value,manuscript,sources:sources.value};
 await saveResponse(await post("/api/research/export/docx",data),degree.value==="doctorate"?"nabil-doctorate-draft.docx":"nabil-masters-draft.docx");
 setStatus("Word جاهز للمراجعة؛ تحقق من كل إحالة قبل تسليم البحث.");
 }catch(err){setStatus(err.message||"تعذر تصدير Word.");}
});
panel.append(download);
const axes=label("محاور الاستبيان (كل محور بسطر مستقل)",document.createElement("textarea"));
axes.rows=3;axes.placeholder="المحور الأول\nالمحور الثاني\nالمحور الثالث";
const survey=document.createElement("button");survey.type="button";survey.textContent="⬇ تنزيل قالب استبيان CSV";
survey.style.cssText="margin:8px;padding:10px;background:#247fc3;color:white;border:0;border-radius:8px;font:inherit;cursor:pointer";
survey.addEventListener("click",async()=>{
 const names=axes.value.split(/\r?\n/).map(s=>s.trim()).filter(Boolean);
 if(title.value.trim().length<8||!names.length){setStatus("أدخل عنوان الرسالة ومحاور الاستبيان.");return;}
 try{await saveResponse(await post("/api/research/survey/csv",{title:title.value,axes:names,language:language.value,questions_per_axis:4}),"nabil-survey-template.csv");
 setStatus("تم تنزيل قالب محاور قابل للتحرير؛ ليس Google Form منشأً.");
 }catch(err){setStatus(err.message||"تعذر تنزيل الاستبيان.");}
});
panel.append(survey);
button.after(panel);
button.addEventListener("click",()=>{panel.hidden=!panel.hidden;button.setAttribute("aria-expanded",String(!panel.hidden));});
button.setAttribute("aria-expanded","false");
})();
