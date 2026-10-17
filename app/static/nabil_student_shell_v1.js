/* NABIL AI — student shell: one compact selection card, then straight into the classroom.
   Uses the existing Golden path only:
     /api/interactive-lessons/resolve  ->  /api/interactive-lessons/golden-classroom?lesson_id=...
   Nothing is removed from the page; selections are never reset when the student goes back. */
(()=>{"use strict";
const $=id=>document.getElementById(id),val=id=>String($(id)?.value||"").trim();
let overlay=null,busy=false,openedFromHistory=false;
const T={start:"▶ ابدأ الدرس",choose:"اختر الدرس أولًا",back:"↩ رجوع للدروس",full:"⛶ ملء الشاشة",exit:"⤢ خروج",loading:"جارٍ فتح الدرس…",fail:"تعذّر فتح الدرس. حاول مرة أخرى."};
function selected(){const s=window.NABILStrictCurriculum?.getSelectedLesson?.()||{};return{title:String(s.title||"").trim(),lesson_id:String(s.lesson_id||"").trim()}}
function selectionMode(on){document.body.classList.toggle("nabil-selection-active",!!on)}
function relabel(){const b=$("startGoldenLesson");if(!b)return false;if(b.dataset.shell!=="1"){b.dataset.shell="1";b.textContent=T.start;b.title=T.start;
  b.addEventListener("click",ev=>{ev.preventDefault();ev.stopImmediatePropagation();start()},true)}
  const ok=!!selected().lesson_id;b.setAttribute("aria-disabled",ok?"false":"true");return true}
function overlayEl(){if(overlay)return overlay;overlay=document.createElement("div");overlay.id="nabilClassroomOverlay";overlay.hidden=true;
  overlay.innerHTML='<div id="nabilClassroomBar"><button type="button" id="nabilClassroomBack"></button><span class="t" id="nabilClassroomTitle"></span><button type="button" id="nabilClassroomFs"></button></div><iframe id="nabilClassroomFrame" title="NABIL classroom" allow="fullscreen; autoplay; microphone; camera" allowfullscreen></iframe>';
  document.body.appendChild(overlay);
  const fr=$("nabilClassroomFrame");[["position","static"],["inset","auto"],["flex","1 1 auto"],["width","100%"],["height","auto"],["min-height","0"],["max-width","none"],["transform","none"],["z-index","auto"],["border","0"]].forEach(([k,v])=>fr.style.setProperty(k,v,"important"));$("nabilClassroomBack").textContent=T.back;$("nabilClassroomFs").textContent=T.full;
  $("nabilClassroomBack").onclick=()=>close(true);$("nabilClassroomFs").onclick=toggleFs;
  document.addEventListener("fullscreenchange",()=>{const b=$("nabilClassroomFs");if(b)b.textContent=document.fullscreenElement?T.exit:T.full});
  window.addEventListener("message",e=>{const d=e.data||{};if(d.type==="nabil:back")close(true);else if(d.type==="nabil:fullscreen")toggleFs()});
  window.addEventListener("popstate",()=>{if(overlay&&!overlay.hidden)close(false)});return overlay}
function toggleFs(){try{if(document.fullscreenElement)document.exitFullscreen();else overlayEl().requestFullscreen?.().catch(()=>{})}catch(e){}}
function close(pop){if(!overlay||overlay.hidden)return;try{document.fullscreenElement&&document.exitFullscreen()}catch(e){}
  const f=$("nabilClassroomFrame");try{f.contentWindow.stop?.()}catch(e){}f.src="about:blank";overlay.hidden=true;document.documentElement.classList.remove("nabil-in-lesson");
  selectionMode(true);if(pop&&openedFromHistory){openedFromHistory=false;try{history.back()}catch(e){}}else openedFromHistory=false}
async function start(){
  if(busy)return;const s=selected();const b=$("startGoldenLesson");
  if(!s.lesson_id){const c=$("lessonSelect");c?.classList.remove("nabil-shake");void c?.offsetWidth;c?.classList.add("nabil-shake");c?.focus?.();return}
  busy=true;if(b){b.dataset.label=b.textContent;b.textContent=T.loading}
  /* the fullscreen request must happen inside the click gesture, before any await */
  const ov=overlayEl();try{ov.requestFullscreen?.().catch(()=>{})}catch(e){}
  try{
    const q=new URLSearchParams({grade:val("gradeSelect"),subject:val("subjectSelect"),language:val("languageSelect"),lesson:s.title,lesson_id:s.lesson_id});
    const r=await fetch("/api/interactive-lessons/resolve?"+q,{cache:"no-store",headers:{Accept:"application/json"}});
    if(!r.ok)throw Error("HTTP "+r.status);const d=await r.json();
    if(d.lesson_id!==s.lesson_id||d.zero_ai!==true||!d.url)throw Error("not canonical Golden");
    $("nabilClassroomTitle").textContent=d.title||s.title;
    const f=$("nabilClassroomFrame");const sep=d.url.includes("?")?"&":"?";
    f.src=d.url+sep+"embedded=1&autostart=1&_="+Date.now();
    ov.hidden=false;document.documentElement.classList.add("nabil-in-lesson");selectionMode(false);
    try{history.pushState({nabilLesson:s.lesson_id},"");openedFromHistory=true}catch(e){}
    f.addEventListener("load",()=>{try{f.contentWindow.postMessage({type:"nabil:autostart"},"*")}catch(e){}},{once:true});
  }catch(e){try{document.fullscreenElement&&document.exitFullscreen()}catch(_){}alert(T.fail);console.error("NABIL shell:",e)}
  finally{busy=false;if(b)b.textContent=T.start}}
function init(){selectionMode(true);let n=0;const t=setInterval(()=>{n++;if(relabel()||n>40)clearInterval(t)},250);
  ["gradeSelect","subjectSelect","languageSelect","lessonSelect","branchSelect"].forEach(id=>$(id)?.addEventListener("change",()=>setTimeout(relabel,50)));
  window.addEventListener("nabil:lesson-selected",relabel)}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init,{once:true});else init();
window.NABILStudentShell={start,close,selected};
})();
