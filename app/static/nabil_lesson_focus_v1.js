/* Show only the requested verified authored exercise or book page; never invent matches. */
(()=>{
"use strict";
const params=new URLSearchParams(location.search);
const exercise=params.get("exercise"),page=params.get("page");
if(!exercise&&!page)return;
function run(){
 const main=document.querySelector("main");
 if(!main)return;
 const sections=[...main.querySelectorAll("section.card,article.card")];
 const allExercises=[...main.querySelectorAll(".row")].filter(row=>/\b(?:Exercice|Exercise)\s*\d+\b/i.test(row.querySelector("h3")?.textContent||""));
 const num=v=>String(Number(v));
 let found=[];
 if(exercise){
  if(!/^\d{1,3}$/.test(exercise))return fail("Invalid exercise number");
  found=allExercises.filter(row=>{
   const h=row.querySelector("h3")?.textContent||"";
   const m=h.match(/\b(?:Exercice|Exercise)\s*(\d+)\b/i);
   return m&&num(m[1])===num(exercise);
  });
 }else{
  if(!/^\d{1,4}$/.test(page))return fail("Invalid printed book page");
  // Only accept explicit printed-book page labels; never treat PDF page as printed page.
  const regex=/(?:Livre\s*p\.?|Book\s*p\.?|Page\s+du\s+livre)\s*[:.]?\s*(\d{1,4})(?:\s*[–-]\s*(\d{1,4}))?/gi;
  found=sections.filter(section=>{
   const text=section.innerText||"";
   for(const m of text.matchAll(regex)){
    const n=Number(page);
    if(n>=Number(m[1])&&n<=Number(m[2]||m[1]))return true;
   }
   return false;
  });
 }
 if(!found.length)return fail(exercise?"Exercise "+exercise+" is not in this prepared lesson":"Printed book page "+page+" is not individually verified in this prepared lesson");
 const visible=new Set();
 for(const node of found){
  let p=node;
  while(p&&p!==main){visible.add(p);p=p.parentElement;}
 }
 // Keep introductory card for context; hide all other unrelated lesson sections.
 for(const section of sections){
  if(visible.has(section))continue;
  if([...found].some(node=>section.contains(node)))continue;
  section.hidden=true;section.style.display="none";
 }
 if(exercise){
  for(const row of allExercises)if(!found.includes(row)){row.hidden=true;row.style.display="none";}
 }
 const banner=document.createElement("aside");
 banner.id="nabil-focus-banner";
 banner.style.cssText="position:sticky;top:0;z-index:100;background:#104065;color:white;border:2px solid #60d8fb;border-radius:12px;padding:12px;margin:12px 0;font:600 16px Arial,sans-serif";
 banner.textContent=exercise?"📘 Exercice / تمرين "+exercise+" — السؤال والرسم والحل فقط":"📘 Page du livre / صفحة الكتاب "+page+" — المحتوى المطابق في الدرس الجاهز";
 const link=document.createElement("a");link.href=location.pathname+location.search.replace(/([?&])(exercise|page)=\d+&?/g,"$1").replace(/[?&]$/,"");
 link.textContent=" | عرض الدرس كاملًا";link.style.cssText="color:#9deaff;margin-inline-start:12px";
 banner.append(link);main.prepend(banner);
 found[0].scrollIntoView({block:"start"});
 console.info("[NABIL_FOCUS] FOUND",exercise?"exercise":"printed_page",exercise||page,"matches",found.length);
 function fail(reason){
  console.warn("[NABIL_FOCUS] NOT_FOUND",reason);
  const alert=document.createElement("aside");alert.style.cssText="background:#5a291f;color:#fff;padding:15px;border:2px solid #ffab85;border-radius:12px;margin:12px";
  alert.textContent="⚠️ "+reason+". No unrelated lesson has been substituted.";
  main.prepend(alert);
 }
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",run);else run();
})();