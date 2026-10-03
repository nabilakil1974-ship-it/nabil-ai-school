/* NABIL AI — Golden teacher runtime v7
 * Fusha-first teaching voice, English scientific terms, sentence-synced pointer,
 * and guaranteed Golden Card access. Does not alter verified lesson facts.
 */
(()=>{"use strict";
if(window.__NABIL_GOLDEN_TEACHER_V7__)return;window.__NABIL_GOLDEN_TEACHER_V7__=true;
const qs=(s,r=document)=>r.querySelector(s),qsa=(s,r=document)=>[...r.querySelectorAll(s)];
let token=0;
function stop(){token++;try{speechSynthesis.cancel()}catch(_){}}
function voice(lang){const vs=speechSynthesis.getVoices?.()||[],p=lang==='ar'?'ar':'en';return vs.find(v=>String(v.lang||'').toLowerCase().startsWith(p)&&/male|hamed|naayf|maged|tarik|guy|david|mark|ryan|george/i.test(v.name))||vs.find(v=>String(v.lang||'').toLowerCase().startsWith(p))||null;}
function clean(t){return String(t||'').replace(/\s+/g,' ').trim();}
function fusha(t){let s=clean(t);const map=[[/\bMove x and watch\b/gi,'حرّك قيمة x ولاحظ'],[/\bcandidate\b/gi,'المستقيم المرشّح'],[/\bThe curve approaches the reference line only after\b/gi,'يقترب المنحنى من المستقيم المرجعي فقط بعد التحقق من'],[/\bis verified\b/gi,''],[/\bkeep only where the radicand is\b/gi,'نحتفظ فقط بالقيم التي يكون فيها radicand'],[/\ballowed\b/gi,'مسموح'],[/\bforbidden\b/gi,'غير مسموح']];for(const [a,b] of map)s=s.replace(a,b);return s;}
function chunks(t){return fusha(t).split(/(?<=[.!؟؛])\s+/).map(clean).filter(Boolean);}
function pointer(){let p=qs('#nabilTeacherPointerV7');if(!p){p=document.createElement('div');p.id='nabilTeacherPointerV7';p.innerHTML='<span></span>';document.body.appendChild(p);}return p;}
function point(el){const p=pointer(),r=el.getBoundingClientRect();p.style.left=Math.max(8,Math.min(innerWidth-54,r.left+Math.min(42,r.width*.18)))+'px';p.style.top=Math.max(8,Math.min(innerHeight-54,r.top-22))+'px';p.classList.add('on');qsa('.nabil-teaching-now').forEach(x=>x.classList.remove('nabil-teaching-now'));el.classList.add('nabil-teaching-now');el.scrollIntoView({behavior:'smooth',block:'center'});}
function unpoint(){pointer().classList.remove('on');qsa('.nabil-teaching-now').forEach(x=>x.classList.remove('nabil-teaching-now'));}
function say(text,el){const my=++token,parts=chunks(text);return new Promise(resolve=>{let i=0;const run=()=>{if(my!==token||i>=parts.length){unpoint();resolve();return;}if(el)point(el);const part=parts[i++],u=new SpeechSynthesisUtterance(part);u.lang=/[\u0600-\u06ff]/.test(part)?'ar-SA':'en-US';u.voice=voice(u.lang.startsWith('ar')?'ar':'en');u.rate=.72;u.pitch=.95;u.onend=run;u.onerror=run;speechSynthesis.speak(u);};run();});}
function readable(card){return qsa('h2,.line,.turn p,.reference-visual figcaption,.reference-visual p,.golden-block b,.golden-block p',card).filter(x=>clean(x.textContent));}
async function teachCard(card){stop();for(const el of readable(card)){await say(el.textContent,el);}}
async function teachLab(lab){stop();const steps=qsa('[data-teach-step],.reference-visual figcaption,.reference-visual p,.reference-visual svg,output',lab).filter((x,i,a)=>a.indexOf(x)===i);for(const el of steps){let text=el.getAttribute('aria-label')||el.textContent||'';if(el.tagName==='SVG')text=el.closest('.reference-visual')?.querySelector('figcaption')?.textContent||'الرسم المرجعي';if(clean(text))await say(text,el);}}
function golden(){return qs('.golden-card');}
function showGolden(){const g=golden();if(!g)return;stop();qsa('.card').forEach(c=>c.hidden=c!==g);g.hidden=false;g.scrollIntoView({behavior:'smooth',block:'start'});setTimeout(()=>teachCard(g),450);}
function install(){const st=document.createElement('style');st.textContent=`#nabilTeacherPointerV7{position:fixed;z-index:2147483600;width:46px;height:46px;pointer-events:none;opacity:0;transition:left .32s ease,top .32s ease,opacity .15s ease;filter:drop-shadow(0 3px 4px #0009)}#nabilTeacherPointerV7 span{display:block;width:44px;height:18px;background:#ffd447;border-radius:12px 3px 3px 12px;position:relative;transform:rotate(8deg)}#nabilTeacherPointerV7 span:after{content:'';position:absolute;right:-18px;top:-7px;border-left:22px solid #ffd447;border-top:16px solid transparent;border-bottom:16px solid transparent}#nabilTeacherPointerV7.on{opacity:1}.nabil-teaching-now{outline:4px solid #ffd447!important;outline-offset:5px!important}.nabil-golden-jump{position:fixed;right:12px;bottom:78px;z-index:2147483500;border:2px solid #ffd447;background:#123d34;color:#fff;border-radius:999px;padding:11px 15px;font-weight:900;box-shadow:0 6px 24px #0008}@media(max-width:520px){.nabil-golden-jump{right:8px;bottom:70px;max-width:56vw;font-size:14px}}`;document.head.appendChild(st);
qsa('[data-speak]').forEach(b=>{b.textContent='🔊 نبيل يشرح بالفصحى';b.onclick=e=>{e.preventDefault();e.stopImmediatePropagation();teachCard(b.closest('.card'));};});
qsa('[data-teach-lab]').forEach(b=>{b.textContent='▶ نبيل يشرح المختبر بالمؤشر';b.onclick=e=>{e.preventDefault();e.stopImmediatePropagation();teachLab(b.closest('.lab'));};});
if(golden()&&!qs('.nabil-golden-jump')){const b=document.createElement('button');b.className='nabil-golden-jump';b.textContent='★ البطاقة الذهبية';b.onclick=showGolden;document.body.appendChild(b);}
document.addEventListener('click',e=>{if(e.target.matches('[data-finish]'))stop();},true);
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install,{once:true});else install();
window.NABILGoldenTeacherV7={teachCard,teachLab,showGolden,stop};
})();