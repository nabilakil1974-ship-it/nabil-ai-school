/* Persistent in-lesson language switch; no AI or Google Translate needed. */
(()=>{
"use strict";
function init(){
 const select=document.getElementById("lesson-language");
 if(!select||document.getElementById("nabil-sticky-language"))return;
 const bar=document.createElement("div");
 bar.id="nabil-sticky-language";
 bar.setAttribute("role","group");
 bar.setAttribute("aria-label","Lesson language / Langue du cours");
 bar.style.cssText="position:fixed;right:14px;bottom:18px;z-index:2147483000;display:flex;gap:6px;align-items:center;background:#09243d;border:2px solid #56d7fa;border-radius:16px;padding:8px;box-shadow:0 5px 24px #0009;font:600 14px Arial,sans-serif;direction:ltr";
 const label=document.createElement("span");label.textContent="🌐";label.style.fontSize="20px";bar.append(label);
 const buttons={};
 for(const [lang,title] of [["fr","Français"],["en","English"]]){
  const button=document.createElement("button");button.type="button";button.textContent=title;
  button.style.cssText="padding:9px 12px;border-radius:10px;border:1px solid #70c8ee;background:#123a5a;color:#fff;cursor:pointer;font:600 14px Arial,sans-serif;min-height:42px";
  button.addEventListener("click",()=>{
   select.value=lang;
   select.dispatchEvent(new Event("change",{bubbles:true}));
   update();
  });
  buttons[lang]=button;bar.append(button);
 }
 function update(){
  for(const [lang,button] of Object.entries(buttons)){
   const active=select.value===lang;
   button.style.background=active?"#2d9fca":"#123a5a";
   button.style.borderColor=active?"#fff":"#70c8ee";
   button.setAttribute("aria-pressed",String(active));
  }
 }
 select.addEventListener("change",update);
 document.body.append(bar);update();
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);
else init();
})();