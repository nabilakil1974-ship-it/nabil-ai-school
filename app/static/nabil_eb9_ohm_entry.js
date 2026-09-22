/* NABIL AI: source-verified bilingual EB9 Ohmic conductors lesson demo. */
(()=>{'use strict';
 const href='/lesson/eb9-ohm';
 const btn=document.createElement('a');btn.href=href;btn.target='_blank';btn.rel='noopener';
 btn.textContent='⚡ درس الفيزياء التاسع التفاعلي | Français / English';
 btn.setAttribute('aria-label','Open bilingual EB9 physics interactive lesson');
 btn.style.cssText='position:fixed;bottom:84px;right:12px;z-index:2147483000;background:#0757b2;color:white;border:1px solid #65ddff;border-radius:13px;padding:11px 14px;max-width:min(330px,90vw);font:600 14px system-ui;text-align:center;text-decoration:none;box-shadow:0 5px 22px #0008';
 btn.hidden=true;document.body.appendChild(btn);
 function check(){const selectors=[...document.querySelectorAll('select')];const vals=selectors.map(s=>String(s.value||'')+' '+(s.selectedOptions[0]?.textContent||'' )).join(' ').toLowerCase();const grade=/(التاسع|صف تاسع|grade\\s*9|eb\\s*0?9|g\\s*0?9)/i.test(vals);const physics=/(فيزياء|physics|physique)/i.test(vals);btn.hidden=!(grade&&physics);}
 document.addEventListener('change',check,true);document.addEventListener('click',()=>setTimeout(check,150),true);check();
})();
