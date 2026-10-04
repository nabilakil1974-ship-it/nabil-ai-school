(()=>{
"use strict";
const byId=id=>document.getElementById(id), clean=v=>String(v??"").trim();
const grade=()=>byId("gradeSelect"), subject=()=>byId("subjectSelect"), language=()=>byId("languageSelect"), branch=()=>byId("branchSelect"), lesson=()=>byId("lessonSelect");
let requestSeq=0;

function canonicalGrade(v){
    const raw=clean(v),x=raw.replace(/\s+/g,"");
    if(/^(10|11|12|[1-9])$/.test(raw))return raw;
    if(x.includes("الثالثثانوي")||x.includes("الثانيعشر")||x.includes("12"))return"12";
    if(x.includes("الثانيثانوي")||x.includes("الحاديعشر")||x.includes("11"))return"11";
    if(x.includes("الأولثانوي")||x.includes("الاولثانوي")||x.includes("العاشر")||x.includes("10"))return"10";
    const m=raw.match(/(?:grade|eb|g)\s*0?([1-9]|1[0-2])/i);
    if(m)return String(Number(m[1]));
    const ar=[["التاسع","9"],["الثامن","8"],["السابع","7"],["السادس","6"],["الخامس","5"],["الرابع","4"],["الثالث","3"],["الثاني","2"],["الأول","1"],["الاول","1"]];
    for(const[k,n]of ar)if(x.includes(k))return n;
    return raw;
}

function canonicalBranch(v){
    const x=clean(v),u=x.toUpperCase();
    if(!x)return "";
    if(u==="GS"||x.includes("علوم عامة")||u.includes("GENERAL")||u.includes("GS"))return"GS";
    if(u==="LS"||u==="SV"||x.includes("علوم الحياة")||u.includes("LIFE"))return"LS";
    if(u==="SE"||u==="ES"||x.includes("اجتماع")||x.includes("اقتصاد")||u.includes("ECONOMICS"))return"SE";
    if(u==="LH"||u==="HUM"||x.includes("آداب")||x.includes("انساني")||u.includes("HUMANITIES"))return"LH";
    return u;
}

function resetLessons(message="اختر الدرس"){
    const el=lesson();
    if(!el)return;
    el.replaceChildren();
    const o=document.createElement("option");
    o.value="";
    o.textContent=message;
    o.dataset.lessonId="";
    o.dataset.packageVersion="";
    el.appendChild(o);
    el.dataset.lessonId="";
    el.dataset.packageVersion="";
    el.dataset.strictCurriculum="1";
    syncSelected();
}

function syncSelected(){
    const el=lesson();
    if(!el)return;
    const o=el.options?.[el.selectedIndex];
    el.dataset.lessonId=clean(o?.dataset?.lessonId);
    el.dataset.packageVersion=clean(o?.dataset?.packageVersion);
    window.NABILSelectedLesson={title:clean(o?.value||el.value),lesson_id:clean(el.dataset.lessonId),version:clean(el.dataset.packageVersion)};
    try{window.dispatchEvent(new CustomEvent("nabil:lesson-selected",{detail:window.NABILSelectedLesson}));}catch(_){}
}

async function serverLessons(q){
    for(const url of["/api/chat/curriculum/lessons?"+q,"/api/curriculum/lessons?"+q]){
        const r=await fetch(url,{cache:"no-store",headers:{Accept:"application/json"}});
        if(r.status===404)continue;
        if(!r.ok)throw Error(`Golden catalogue HTTP ${r.status}`);
        const d=await r.json();
        return Array.isArray(d.lessons)?d.lessons:[];
    }
    throw Error("Golden catalogue route not installed");
}

function installRows(rows){
    const seen=new Set(),items=[];
    for(const x of rows||[]){
        if(!x)continue;
        const id=clean(x.lesson_id),title=clean(x.title);
        if(!id||!title||seen.has(id))continue;
        seen.add(id);
        items.push({title,lesson_id:id.toUpperCase(),version:clean(x.version)||"0.01"});
    }
    items.sort((a,b)=>a.lesson_id.localeCompare(b.lesson_id,undefined,{numeric:true}));
    resetLessons(items.length?"اختر الدرس":"لا توجد دروس منشورة لهذا الاختيار");
    const el=lesson();
    if(!el)return;
    for(const x of items){
        const o=document.createElement("option");
        o.value=x.title;
        o.textContent=x.title;
        o.dataset.lessonId=x.lesson_id;
        o.dataset.packageVersion=x.version;
        el.appendChild(o);
    }
    syncSelected();
}

async function refresh(){
    const rawG=clean(grade()?.value),g=canonicalGrade(rawG);
    const s=clean(subject()?.value),l=clean(language()?.value);
    const rawB=clean(branch()?.value),b=canonicalBranch(rawB);
    const seq=++requestSeq;
    resetLessons();
    if(!g||!s)return;
    const q=new URLSearchParams({grade:g,subject:s});
    if(l)q.set("language",l);
    if(b)q.set("branch",b);
    try{
        const rows=await serverLessons(q.toString());
        if(seq!==requestSeq)return;
        installRows(rows);
    }catch(e){
        if(seq!==requestSeq)return;
        console.error("NABIL canonical Golden curriculum:",e);
        resetLessons("تعذر تحميل الفهرس — تحقق من الاتصال");
    }
}

function bind(){
    for(const el of[grade(),subject(),language(),branch()]){
        if(!el||el.dataset.strictCurriculumBound)continue;
        el.dataset.strictCurriculumBound="1";
        el.addEventListener("change",()=>setTimeout(refresh,0));
    }
    const le=lesson();
    if(le&&!le.dataset.nabilLessonIdentityBound){
        le.dataset.nabilLessonIdentityBound="1";
        le.addEventListener("change",syncSelected);
    }
    syncSelected();
}

function start(){bind();setTimeout(refresh,150);}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",start,{once:true});else start();setTimeout(()=>{bind();refresh();},900);
window.NABILStrictCurriculum={refresh,getSelectedLessonId(){return clean(window.NABILSelectedLesson?.lesson_id);},getSelectedLesson(){return{...(window.NABILSelectedLesson||{title:"",lesson_id:"",version:""})};}};
})();
