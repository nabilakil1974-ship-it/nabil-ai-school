/* NABIL Verified Lab Loader v18
 * Requirement 5 runtime bridge.
 * Loads only pre-published, verified lesson-aware labs. Never fabricates a lab,
 * never falls back to another lesson, and never calls an LLM at student runtime.
 */
(()=>{'use strict';
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const payload=()=>window.__NABIL_GOLDEN__||{};
const language=()=>String(payload().language||document.documentElement.lang||'ar').toLowerCase();
const lessonId=()=>String(payload().lesson_id||'').trim().toUpperCase();
function labId(card,index){return String(card.dataset.labId||card.getAttribute('data-lab-id')||`lab-${index+1}`).trim();}
function shell(card,id){let box=card.querySelector('.nrc-lab-placeholder,.nabil-verified-lab-slot');if(!box){box=document.createElement('div');card.appendChild(box)}box.className='nabil-verified-lab-slot';box.dataset.labId=id;return box}
function pending(box,id,reason){box.innerHTML=`<div style="border:1px dashed #56758d;border-radius:12px;padding:12px;color:#ffdca0;background:#081725;margin-top:14px"><b>🧪 Verified Lab · ${esc(id)}</b><div>${reason==='PUBLISHED_LAB_NOT_READY'?'المختبر الموثق لهذا الجزء لم يُنشر بعد. لن يعرض NABIL مختبرًا عامًا أو قيمًا مخترعة.':'تعذر تحميل المختبر الموثق. تم الإيقاف الآمن دون fallback.'}</div></div>`}
function mount(box,data){if(!data||data.found!==true||!data.verified||!data.html){pending(box,data?.lab_id||box.dataset.labId,data?.reason||'INVALID_VERIFIED_LAB');return}const frame=document.createElement('iframe');frame.className='nabil-smart-lab-frame';frame.title=data.title||'NABIL Verified Smart Lab';frame.setAttribute('sandbox','allow-scripts allow-same-origin');frame.setAttribute('loading','lazy');frame.style.cssText='width:100%;min-height:560px;border:0;border-radius:14px;background:#05172d;margin-top:12px';frame.srcdoc=data.html;box.replaceChildren(frame);box.dataset.verified='true';box.dataset.sourceSignature=String(data.source_signature||'');box.dataset.rendererContract=String(data.renderer_contract||'');}
async function load(card,index){const lid=lessonId(),id=labId(card,index),box=shell(card,id);if(!lid){pending(box,id,'LESSON_ID_REQUIRED');return}box.textContent='تحميل المختبر العلمي الموثق…';try{const u=`/api/interactive-lessons/verified-lab?lesson_id=${encodeURIComponent(lid)}&lab_id=${encodeURIComponent(id)}&language=${encodeURIComponent(language())}`;const r=await fetch(u,{headers:{Accept:'application/json'},cache:'no-store'});const data=await r.json().catch(()=>({found:false,reason:'INVALID_RESPONSE'}));if(!r.ok&&r.status!==404)throw new Error(data.detail||`HTTP_${r.status}`);mount(box,data)}catch(e){console.error('NABIL verified lab load failed',e);pending(box,id,'LOAD_FAILED')}}
function wire(){const cards=[...document.querySelectorAll('.nrc-card[data-role="lab"],.nrc-card[data-lab-id]')];cards.forEach((c,i)=>{if(c.dataset.nabilLabWired)return;c.dataset.nabilLabWired='1';load(c,i)});}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(wire,0));else setTimeout(wire,0);
new MutationObserver(()=>wire()).observe(document.documentElement,{subtree:true,childList:true});
window.NABILVerifiedLabLoaderV18={wire,load};
})();