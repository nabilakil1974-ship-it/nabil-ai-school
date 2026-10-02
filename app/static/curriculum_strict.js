(() => {
  "use strict";
  const byId=id=>document.getElementById(id), clean=v=>String(v??"").trim();
  const grade=()=>byId("gradeSelect"), subject=()=>byId("subjectSelect"), language=()=>byId("languageSelect"), branch=()=>byId("branchSelect"), lesson=()=>byId("lessonSelect");
  let requestSeq=0;
  function resetLessons(message="اختر الدرس"){
    const el=lesson(); if(!el)return; el.innerHTML="";
    const opt=document.createElement("option"); opt.value=""; opt.textContent=message; opt.dataset.lessonId=""; opt.dataset.packageVersion=""; el.appendChild(opt);
    el.dataset.lessonId=""; el.dataset.packageVersion=""; el.dataset.strictCurriculum="1";
  }
  function normalizeLessonItem(item){
    // Golden-only: title-only legacy rows are intentionally rejected.
    if(typeof item==="string")return null;
    if(!item||typeof item!=="object")return null;
    const title=clean(item.title??item.lesson??item.name??item.canonical_title); if(!title)return null;
    return {title,lessonId:clean(item.lesson_id??item.lessonId??item.id),version:clean(item.version??item.package_version??item.published_version)};
  }
  function syncSelectedLessonIdentity(){
    const el=lesson(); if(!el)return; const opt=el.options?.[el.selectedIndex];
    el.dataset.lessonId=clean(opt?.dataset?.lessonId); el.dataset.packageVersion=clean(opt?.dataset?.packageVersion);
    window.NABILSelectedLesson={title:clean(el.value),lesson_id:clean(el.dataset.lessonId),version:clean(el.dataset.packageVersion)};
    try{window.dispatchEvent(new CustomEvent("nabil:lesson-selected",{detail:window.NABILSelectedLesson}));}catch(_){}
  }
  async function fetchCurriculumLessons(q){
    let res=await fetch("/api/chat/curriculum/lessons?"+q,{cache:"no-store"});
    if(res.status===404)res=await fetch("/api/curriculum/lessons?"+q,{cache:"no-store"});
    return res;
  }
  async function refreshStrictLessons(){
    const g=clean(grade()?.value),s=clean(subject()?.value),l=clean(language()?.value),b=clean(branch()?.value),seq=++requestSeq; resetLessons();
    if(g.startsWith("الثالث ثانوي")&&!g.includes(" - ")&&!b){resetLessons("اختر فرع الثالث ثانوي أولًا");return;}
    if(!g||!s||!l)return;
    const q=new URLSearchParams({grade:g,subject:s,language:l}); if(b)q.set("branch",b);
    try{
      const res=await fetchCurriculumLessons(q.toString()); if(!res.ok)throw Error("curriculum "+res.status); const data=await res.json(); if(seq!==requestSeq)return;
      const normalized=[],seen=new Set();
      for(const raw of (Array.isArray(data?.lessons)?data.lessons:[])){const item=normalizeLessonItem(raw);if(!item||!item.lessonId)continue;const key="id:"+item.lessonId;if(seen.has(key))continue;seen.add(key);normalized.push(item);}
      resetLessons(normalized.length?"اختر الدرس":"لا توجد دروس ذهبية منشورة بهذه اللغة"); const el=lesson(); if(!el)return;
      for(const item of normalized){const opt=document.createElement("option");opt.value=item.title;opt.textContent=item.title;opt.dataset.lessonId=item.lessonId;opt.dataset.packageVersion=item.version;el.appendChild(opt);} el.dataset.strictCurriculum="1";syncSelectedLessonIdentity();
    }catch(err){if(seq!==requestSeq)return;console.error("NABIL strict curriculum:",err);resetLessons("لا توجد دروس ذهبية منشورة لهذا الاختيار");}
  }
  function bind(){
    for(const el of [grade(),subject(),language(),branch()]){if(!el||el.dataset.strictCurriculumBound)continue;el.dataset.strictCurriculumBound="1";el.addEventListener("change",()=>setTimeout(refreshStrictLessons,0));}
    const le=lesson();if(le&&!le.dataset.nabilLessonIdentityBound){le.dataset.nabilLessonIdentityBound="1";le.addEventListener("change",syncSelectedLessonIdentity);} syncSelectedLessonIdentity();
  }
  // Golden identity is attached ONLY to the one request caused by pressing
  // "Start Lesson". Follow-up chat questions remain normal tutor requests and
  // therefore do not re-open the whole Golden package on every message.
  let goldenStartPending=false;
  function bindGoldenStart(){
    const btn=byId("startLesson");
    if(!btn||btn.dataset.nabilGoldenStartBound)return;
    btn.dataset.nabilGoldenStartBound="1";
    btn.addEventListener("click",()=>{
      const selected=window.NABILSelectedLesson||{};
      goldenStartPending=Boolean(clean(selected.lesson_id));
    },true);
  }
  const originalFetch=window.fetch.bind(window);
  window.fetch=function(input,init={}){
    try{
      const url=typeof input==="string"?input:String(input?.url||"");
      const body=init?.body;
      if(goldenStartPending&&/\/api\/chat(?:\?|$)/.test(url)&&body instanceof FormData){
        const selected=window.NABILSelectedLesson||{};
        const id=clean(selected.lesson_id),version=clean(selected.version);
        goldenStartPending=false;
        if(id)body.set("lesson_id",id);
        if(version)body.set("package_version",version);
      }
    }catch(err){goldenStartPending=false;console.error("NABIL Golden identity bridge:",err);}
    return originalFetch(input,init);
  };
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",()=>{bind();bindGoldenStart();setTimeout(refreshStrictLessons,250);});else{bind();bindGoldenStart();setTimeout(refreshStrictLessons,250);}
  setTimeout(()=>{bind();bindGoldenStart();refreshStrictLessons();},1200); setTimeout(()=>{bind();bindGoldenStart();refreshStrictLessons();},1800);
  window.NABILStrictCurriculum={refresh:refreshStrictLessons,getSelectedLessonId(){return clean(window.NABILSelectedLesson?.lesson_id);},getSelectedLesson(){return {...(window.NABILSelectedLesson||{title:"",lesson_id:"",version:""})};}};
})();
