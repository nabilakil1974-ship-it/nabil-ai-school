/* NABIL Lab Reference Theme v1 — exact visual language from Phase 4 Smart Board Proof Lab */
(function(){'use strict';
const css=`
:root{--nabil-bg:#030b14;--nabil-card:#0a1a2d;--nabil-line:#183b5a;--nabil-cyan:#2de1ff;--nabil-gold:#ffd76b;--nabil-green:#55e6a4;--nabil-red:#ff667c;--nabil-violet:#c891ff;--nabil-txt:#f8fbff;--nabil-muted:#9fb5c9}
.teach-lab{background:#0a1a2df6!important;border:1px solid var(--nabil-line)!important;border-radius:18px!important;box-shadow:0 18px 42px #0005!important;color:var(--nabil-txt)!important}
.teach-lab>header{background:#0a1a2df0!important;border-bottom:1px solid var(--nabil-line)!important;padding:13px 16px!important}
.teach-lab h3{color:var(--nabil-cyan)!important;font-weight:900!important}.teach-lab small{color:var(--nabil-muted)!important}.teach-lab .live{color:var(--nabil-green)!important}
.teacher-grid{gap:14px!important;padding:14px!important;background:radial-gradient(circle at top,#0d2a48,#06111f 48%,#02070d)!important}
.board{position:relative!important;overflow:hidden!important;border:1px solid #1c4569!important;border-radius:16px!important;background:linear-gradient(#0a2135 1px,transparent 1px),linear-gradient(90deg,#0a2135 1px,transparent 1px),#020912!important;background-size:32px 32px!important;min-height:450px!important}
.board canvas{display:block!important;width:100%!important;height:100%!important;min-height:450px!important;touch-action:none!important}
.teacher-grid aside{background:#0a1a2df6!important;border:1px solid var(--nabil-line)!important;border-radius:16px!important;padding:14px!important}
.speech{background:#071725!important;border:1px solid #1a3b55!important;border-inline-start:3px solid var(--nabil-cyan)!important;border-radius:13px!important;padding:13px!important;min-height:150px!important}
.speech b{color:var(--nabil-cyan)!important;font-size:20px!important}.speech p{color:var(--nabil-txt)!important;font-size:18px!important;line-height:1.75!important;margin:10px 0!important}
.live-values{direction:ltr!important;text-align:center!important;background:#03111d!important;border:1px dashed #315d79!important;border-radius:10px!important;color:var(--nabil-txt)!important;padding:12px!important;font-family:'Cambria Math',monospace!important;font-size:18px!important;line-height:1.65!important}
.teacher-grid input[type=range]{accent-color:var(--nabil-cyan)!important}
.lab-actions button{border:1px solid #426d8b!important;background:#153955!important;color:white!important;border-radius:10px!important;min-height:42px!important;font-weight:800!important}.lab-actions [data-demo]{background:var(--nabil-cyan)!important;color:#01232a!important;border-color:#7af3ff!important}.lab-actions [data-pause]{background:#6047a8!important;border-color:#a98cff!important}.lab-actions [data-reset]{background:#5a2330!important;border-color:#bd546b!important}
/* Reference teacher pointer: animated cyan dashed arrow, not the old yellow circle. */
.pointer{width:92px!important;height:0!important;border:0!important;border-top:3px dashed var(--nabil-cyan)!important;border-radius:0!important;box-shadow:none!important;transform:translate(-100%,-50%) rotate(-18deg)!important;transform-origin:right center!important;transition:left .35s ease,top .35s ease,transform .35s ease!important;filter:drop-shadow(0 0 7px rgba(45,225,255,.55))!important;animation:nabilDash .85s linear infinite!important;pointer-events:none!important;z-index:5!important}
.pointer:after{content:'';position:absolute;right:-3px;top:-9px;width:0;height:0;border-top:8px solid transparent;border-bottom:8px solid transparent;border-left:15px solid var(--nabil-cyan);filter:drop-shadow(0 0 5px rgba(45,225,255,.65))}
@keyframes nabilDash{to{border-top-color:var(--nabil-cyan);filter:drop-shadow(0 0 10px rgba(45,225,255,.95))}}
.teach-lab canvas{filter:drop-shadow(0 0 0 rgba(45,225,255,0))}.teach-lab[data-nabil-speaking='1'] canvas{filter:drop-shadow(0 0 7px rgba(45,225,255,.18))}
@media(max-width:920px){.teacher-grid{grid-template-columns:1fr!important}.board,.board canvas{min-height:360px!important}.teacher-grid aside{min-width:0!important}}
`;
function install(){if(document.getElementById('nabil-lab-reference-theme-v1'))return;const s=document.createElement('style');s.id='nabil-lab-reference-theme-v1';s.textContent=css;document.head.appendChild(s);document.querySelectorAll('[data-teach-lab]').forEach(l=>{l.dataset.nabilReferenceTheme='phase4'});}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install,{once:true});else install();
new MutationObserver(install).observe(document.documentElement,{childList:true,subtree:true});
window.NABILLabReferenceTheme={version:'1',install};
})();
