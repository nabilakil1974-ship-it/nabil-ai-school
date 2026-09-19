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
note.textContent="يكفي عنوان الرسالة. سيقترح نبيل بقية المحاور والأسئلة والمنهجية ويكتب كل فصل على مراحل متتابعة؛ قسم النتائج الميدانية لا يُملأ إلا بإجابات حقيقية. Google Form يُنشأ بعد تشغيل السكربت والموافقة في حسابك.";
panel.append(note);
function label(text, control){const box=document.createElement("label");box.style.cssText="display:block;margin:10px 0";box.append(document.createTextNode(text));control.style.cssText="display:block;box-sizing:border-box;width:100%;min-width:0;margin-top:5px;padding:9px;background:#091b2a;color:white;border:1px solid #3882af;border-radius:6px;font:inherit";box.append(control);panel.append(box);return control;}
const degree=document.createElement("select");
for(const [value,name] of [["masters","ماجستير"],["doctorate","دكتوراه"]]){const o=document.createElement("option");o.value=value;o.textContent=name;degree.append(o);}
label("الدرجة العلمية",degree);
const title=label("عنوان الرسالة",document.createElement("input"));
title.maxLength=500;title.placeholder="اكتب عنوان البحث";
const outline=label("الخطوط العريضة وأفكار الباحث",document.createElement("textarea"));
outline.rows=5;outline.maxLength=12000;outline.placeholder="اختياري — يستنتج نبيل خطة مبدئية من العنوان إن تُرك فارغًا";
const questions=label("أسئلة البحث الأساسية (كل سؤال في سطر)",document.createElement("textarea"));
questions.rows=4;questions.maxLength=12000;questions.placeholder="ما أثر ...؟\nما العلاقة بين ...؟";
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
output.style.cssText="white-space:pre-wrap;word-break:break-word;max-width:100%;font:inherit;line-height:1.8;background:#091b2a;padding:12px;border:1px solid #22648d;border-radius:8px;max-height:none;overflow:visible";
output.textContent="اختر المرحلة للبدء.";
output.contentEditable="true";output.setAttribute("aria-label","مسودة بحث قابلة للتحرير؛ أدرج [FN:1] لربط أول مرجع من قائمة المراجع بهامش Word");
output.addEventListener("input",()=>{manuscript=output.innerText.slice(0,650000);});
const status=document.createElement("p");status.setAttribute("role","status");panel.append(status);
let manuscript="";
let observedAggregates="";
let chapterPlan="";
let nextTheoryPart=1;
let stopped=false;
let generatedQuestionnaire="";
let busy=false;
function setStatus(t){status.textContent=t;}
function validate(){if(title.value.trim().length<8){setStatus("اكتب عنوان البحث فقط؛ المحاور والأسئلة اختيارية.");return false;}return true;}
async function post(path,payload){
 const response=await fetch(path,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});
 if(!response.ok){let message="تعذّر تنفيذ الطلب. حاول مجددًا.";try{const data=await response.json();message=String(data.detail||message)}catch(_){}throw Error(message);}
 return response;
}
function state(){return {degree:degree.value,title:title.value.trim(),outline:outline.value.trim(),sources:sources.value.trim(),guidance:guidance.value.trim(),research_questions:questions.value.trim(),observed_aggregates:observedAggregates,chapter_plan:chapterPlan,language:language.value};}
const stageLabels=[["structure","الخطة التفصيلية والمحاور"],["proposal","المقدمة وخطة البحث"],["theoretical","الإطار النظري"],["questionnaire","الاستبيان"],["sampling","العينة والمنهجية"],["practical","الإطار التطبيقي"],["results","تحليل النتائج والجداول"],["conclusion","الاستنتاجات والتوصيات"],["summary","الخاتمة والخلاصة"],["revision","المراجعة"]];
for(const [stage,name] of stageLabels){
 const action=document.createElement("button");action.type="button";action.textContent=name;
 action.style.cssText="padding:9px;border:1px solid #2baee8;border-radius:7px;background:#14619a;color:white;cursor:pointer;font:inherit";
 action.addEventListener("click",async()=>{
   if(busy||!validate())return;
   busy=true;setStatus("جارٍ إعداد "+name+"... احتفظ بنصوص الباحث ومراجعها.");
   try{
     const payload={...state(),stage,previous_text:manuscript.slice(-18000)};
     const result=await (await post("/api/research/draft",payload)).json();
     if(!result.text)throw Error("لم يصل نص من الخدمة.");
     manuscript+=(manuscript?"\n\n":"")+"# "+name+"\n"+result.text;
     if(stage==="structure")chapterPlan=result.text.slice(0,12000);
     if(stage==="questionnaire"){generatedQuestionnaire=result.text;populateGeneratedQuestions(result.text);}
     output.textContent=manuscript;
     setStatus("تم إنشاء "+name+". هذه مسودة، وليست رسالة مكتملة أو مصادر متحققة.");
   }catch(err){setStatus(err.message||"حدث خطأ ولم تُفقد المسودة.");}
   finally{busy=false;}
 });
 stages.append(action);
}
const full=document.createElement("button");
full.id="nabilResearchFullThesis";full.type="button";
full.textContent="📚 إعداد الرسالة من المقدمة إلى الخاتمة";
full.style.cssText="display:block;width:100%;margin:10px 0;padding:13px;background:#168360;color:white;border:0;border-radius:8px;font:inherit;cursor:pointer";
const halt=document.createElement("button");
halt.type="button";halt.textContent="⏸ إيقاف بعد القسم الجاري";
halt.style.cssText="margin:8px;padding:10px;background:#884d15;color:#fff;border:0;border-radius:8px;font:inherit;cursor:pointer";
halt.addEventListener("click",()=>{stopped=true;setStatus("سيُحفظ ما أُنجز ويتوقف بعد القسم الحالي؛ يمكن الضغط على إعداد الرسالة لاستئناف الباقي.");});
full.addEventListener("click",async()=>{
 if(busy||!validate())return;
 busy=true;stopped=false;full.disabled=true;
 const sections=[["structure","الخطة التفصيلية"],["proposal","المقدمة وخطة البحث"]];
 const finalSections=[["questionnaire","الاستبيان"],["sampling","العينة والمنهجية"],["practical","الإطار التطبيقي"],
 ...(observedAggregates?[["results","الجداول وتحليل النتائج"]]:[]),
 ["conclusion",observedAggregates?"الاستنتاج العام بعد تحليل الاستبيان":"الاستنتاج النظري والتوصيات"],["summary",observedAggregates?"الخاتمة النهائية بعد التحليل":"الخاتمة والخلاصة والمراجع المطلوب استكمالها"]];
 async function appendStage(stage,name,index,total,part=null){
  if(manuscript.length>630000)throw Error("وصلت المسودة إلى حد التخزين؛ صدّرها إلى Word قبل المتابعة.");
  setStatus("إعداد "+name+" ("+index+"/"+total+") — لا تغلق الصفحة قبل اكتمال القسم");
  const response=await (await post("/api/research/draft",{
   ...state(),stage,theoretical_part_index:part,
   previous_text:manuscript.slice(-18000)
  })).json();
  if(!response.text)throw Error("لم يصل "+name);
  const words=response.text.trim().split(/\s+/).filter(Boolean).length;
  if(stage==="theoretical"&&words<250)throw Error("القسم النظري "+part+" قصير جدًا ("+words+" كلمة). لم نعتبره صفحة مكتملة؛ اضغط مجددًا للمحاولة.");
  const start=stage==="theoretical"?"[THEORETICAL_PAGE_BREAK]\n## المحور النظري "+part+"\n":"# "+name+"\n";
  manuscript+=(manuscript?"\n\n":"")+start+response.text;
  if(stage==="structure")chapterPlan=response.text.slice(0,12000);
  if(stage==="questionnaire"){generatedQuestionnaire=response.text;populateGeneratedQuestions(response.text);}
  output.textContent=manuscript;
 }
 try{
  let index=0;const total=sections.length+22+finalSections.length;
  for(const [stage,name] of sections){
   if(stopped)break;index++;
   if(stage==="structure"&&chapterPlan)continue;
   if(stage==="proposal"&&manuscript.includes("# المقدمة وخطة البحث"))continue;
   await appendStage(stage,name,index,total);
  }
  if(!stopped&&!manuscript.includes("# الإطار النظري")){manuscript+="\n\n# الإطار النظري — 22 قسمًا مفصلًا";output.textContent=manuscript;}
  while(!stopped&&nextTheoryPart<=22){
   await appendStage("theoretical","المحور النظري "+nextTheoryPart,sections.length+nextTheoryPart,total,nextTheoryPart);
   nextTheoryPart++;
  }
  for(let j=0;j<finalSections.length&&!stopped&&nextTheoryPart>22;j++){
   const [stage,name]=finalSections[j];
   if(manuscript.includes("# "+name))continue;
   await appendStage(stage,name,sections.length+22+j+1,total);
  }
  if(!stopped&&!observedAggregates&&!manuscript.includes("# نتائج الاستبيان")){
   manuscript+="\n\n# نتائج الاستبيان — تستكمل بعد جمع الإجابات الفعلية\nلم تُجمع بعد بيانات مشاركين، لذلك لا يمكن ادعاء نتائج أو اختبارات دلالة أو SPSS منفذة. يتضمن فصل التطبيق خطة العينة والاستبيان والتحليل، وتكتمل النتائج بعد رفع ملف الإجابات.";
   output.textContent=manuscript;
  }
  setStatus(stopped?"تم الإيقاف مع حفظ جميع الأقسام المنجزة في المسودة؛ اضغط إعداد الرسالة لاستكمال الباقي.":"أُنجزت فصول المسودة المتاحة. 22 قسمًا نظريًا منفصلًا بخط Word 14؛ راجع الصفحات والمصادر، وتستكمل النتائج الفعلية من الاستبيان.");
 }catch(err){setStatus("توقف التوليد مع الاحتفاظ بالنص المنجز: "+String(err.message||err));}
 finally{busy=false;full.disabled=false;}
});
panel.append(full);panel.append(halt);
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
const footnoteHelp=document.createElement("p");footnoteHelp.textContent="يمكنك تعديل المسودة مباشرة. لهامش Word حقيقي، اكتب [FN:1] عند موضع الاستشهاد، وضع المرجع الأول في السطر الأول من قائمة المراجع. راجع صحة المرجع قبل التسليم.";panel.append(footnoteHelp);
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
const actualQuestions=label("أسئلة Google Form: كل سطر «المحور | نص السؤال»",document.createElement("textarea"));
function populateGeneratedQuestions(source){
 const result=[];
 for(const line of source.split(/\r?\n/)){
  const cleaned=line.trim().replace(/^[-*\d.)\s]+/,"");
  if(cleaned.includes("|")){
   const index=cleaned.indexOf("|");
   const axis=cleaned.slice(0,index).replace(/\*\*/g,"").trim();
   const item=cleaned.slice(index+1).replace(/\*\*/g,"").trim();
   if(axis&&item&&axis.length<=160&&item.length<=600&&axis.toLowerCase()!=="axis"&&axis!=="المحور")result.push(axis+" | "+item);
  }
 }
 if(result.length)actualQuestions.value=result.slice(0,120).join("\n");
 if(result.length){
  const names=[...new Set(result.map(v=>v.split("|")[0].trim()))];
  axes.value=names.join("\n");
 }
}
actualQuestions.rows=5;actualQuestions.placeholder="القيادة المدرسية | يشارك المدير المعلمين في اتخاذ القرارات.\nالتطوير المهني | أحصل على فرص تدريب تلائم احتياجاتي.";
const formsScript=document.createElement("button");
formsScript.type="button";formsScript.textContent="⬇ سكربت إنشاء Google Form بمحاورك";
formsScript.style.cssText="margin:8px;padding:10px;background:#654eb7;color:white;border:0;border-radius:8px;font:inherit;cursor:pointer";
formsScript.addEventListener("click",async()=>{
 const questions=actualQuestions.value.split(/\r?\n/).map(line=>line.trim()).filter(Boolean).map(line=>{
  const sep=line.indexOf("|");
  return sep<0?null:{axis:line.slice(0,sep).trim(),item:line.slice(sep+1).trim()};
 });
 if(title.value.trim().length<8||!questions.length||questions.some(q=>!q||!q.axis||!q.item)){
   setStatus("أدخل عنوان البحث والأسئلة بصيغة: المحور | نص السؤال.");return;
 }
 try{
  await saveResponse(await post("/api/research/survey/google-forms-script",
   {title:title.value.trim(),language:language.value,questions}),"nabil-create-google-form.gs");
  setStatus("تم تنزيل سكربت Google Apps Script. افتحه في حسابك وشغّل createNabilResearchForm ووافق على صلاحيات Google؛ التنزيل وحده لا ينشئ فورم.");
 }catch(err){setStatus(err.message||"تعذر تجهيز سكربت Google Form.");}
});
panel.append(formsScript);
const portals=document.createElement("details"),summary=document.createElement("summary");
summary.textContent="🔎 مستودعات الرسائل الجامعية الموثوقة";portals.append(summary);
for(const [name,url] of [["OATD","https://www.oatd.org/"],["White Rose eTheses","https://etheses.whiterose.ac.uk/"],["AUC Knowledge Fountain","https://fount.aucegypt.edu/"],["Saudi Digital Library","https://sdl.edu.sa/"],["ProQuest Dissertations & Theses","https://about.proquest.com/en/products-services/pqdtglobal/"]]){
 const link=document.createElement("a");link.href=url;link.target="_blank";link.rel="noopener noreferrer";link.textContent=name;
 link.style.cssText="display:block;margin:8px;color:#80d8ff";portals.append(link);
}
const caution=document.createElement("p");caution.textContent="روابط بحث وليست مراجع تم الاطلاع عليها تلقائيًا. تحقق من النص والصفحة والباحث والسنة قبل التوثيق.";portals.append(caution);
panel.append(portals);
const statsHead=document.createElement("h3");statsHead.textContent="📊 العينة والجداول والتحليل الإحصائي";panel.append(statsHead);
const upload=label("ارفع CSV لإجابات حقيقية بلا أسماء أو بيانات شخصية",document.createElement("input"));
upload.type="file";upload.accept=".csv,text/csv";
const mapping=label("ربط المحاور بأعمدة CSV — كل سطر: المحور | Q1,Q2,Q3",document.createElement("textarea"));
mapping.rows=3;mapping.placeholder="القيادة | Q1,Q2,Q3\nالتدريب | Q4,Q5,Q6";
function axesMap(){
 const result={};
 for(const line of mapping.value.split(/\r?\n/).map(v=>v.trim()).filter(Boolean)){
  const sep=line.indexOf("|");if(sep<1)throw Error("صيغة المحور | Q1,Q2");
  const key=line.slice(0,sep).trim(),cols=line.slice(sep+1).split(",").map(v=>v.trim()).filter(Boolean);
  if(!key||!cols.length||result[key])throw Error("محور فارغ أو مكرر");
  result[key]=cols;
 }
 if(!Object.keys(result).length)throw Error("أدخل المحاور وأعمدة أسئلتها");
 return result;
}
async function analysisRequest(path){
 if(!upload.files?.length)throw Error("ارفع ملف الإجابات الحقيقية أولًا");
 const form=new FormData();form.append("file",upload.files[0]);
 form.append("axes_json",JSON.stringify(axesMap()));form.append("language",language.value);
 const response=await fetch(path,{method:"POST",body:form});
 if(!response.ok){let message="تعذر تحليل البيانات";try{message=(await response.json()).detail||message}catch(_){}throw Error(message);}
 return response;
}
const analyze=document.createElement("button");analyze.type="button";analyze.textContent="📈 حساب الجداول وتحليل إجابات العينة";
analyze.style.cssText="padding:10px;background:#136db0;color:white;border:0;border-radius:8px;font:inherit;cursor:pointer";
analyze.addEventListener("click",async()=>{
 if(busy)return;busy=true;setStatus("تحليل إحصائي لإجابات العينة الحقيقية...");
 try{
  const data=await (await analysisRequest("/api/research/survey/analyze")).json();
  observedAggregates=JSON.stringify(data.summary);
  manuscript+="\n\n# الجداول والتحليل الوصفي للعينة\n"+data.markdown;
  output.textContent=manuscript;
  setStatus("الجداول أُنتجت من البيانات المرفوعة؛ لم يُشغَّل SPSS نفسه. يمكن تنزيل ملف .sps وتشغيله في SPSS.");
 }catch(err){setStatus(String(err.message||err));}finally{busy=false;}
});
panel.append(analyze);
for(const [labelText,path,filename] of [["⬇ تنزيل جداول التحليل CSV","/api/research/survey/analysis-tables.csv","nabil-survey-tables.csv"],["⬇ تنزيل أوامر SPSS","/api/research/survey/analysis.sps","nabil-survey-analysis.sps"]]){
 const btn=document.createElement("button");btn.type="button";btn.textContent=labelText;
 btn.style.cssText="margin:8px;padding:10px;background:#247fc3;color:white;border:0;border-radius:8px;font:inherit;cursor:pointer";
 btn.addEventListener("click",async()=>{try{await saveResponse(await analysisRequest(path),filename);setStatus("تم تنزيل "+filename);}catch(err){setStatus(String(err.message||err));}});
 panel.append(btn);
}
button.after(panel);
button.addEventListener("click",()=>{panel.hidden=!panel.hidden;button.setAttribute("aria-expanded",String(!panel.hidden));});
button.setAttribute("aria-expanded","false");
})();
