(() => {
  "use strict";
  const studentId = () => String(localStorage.getItem("nabil_student_id") || sessionStorage.getItem("nabil_student_id") || "").trim();
  function ensureBadge(){ let b=document.getElementById("nabilSubscriptionCountdown"); if(b)return b; b=document.createElement("div"); b.id="nabilSubscriptionCountdown"; b.style.cssText="position:fixed;top:8px;right:8px;z-index:2147483000;padding:8px 12px;border-radius:14px;background:#082f49;color:white;font:600 14px system-ui;box-shadow:0 4px 16px #0005"; document.body.appendChild(b); return b; }
  function render(s){ const b=ensureBadge(); if(!s||!s.expires_at){b.textContent="NABIL AI";return;} const end=new Date(s.expires_at).getTime(); const ms=Math.max(0,end-Date.now()); const d=Math.floor(ms/86400000), h=Math.floor((ms%86400000)/3600000); b.textContent=s.state==="trial"?`الفترة التجريبية: بقي ${d} يوم و${h} ساعة`:s.state==="active"?`الاشتراك: بقي ${d} يوم و${h} ساعة`:"انتهت مدة الاشتراك"; }
  async function refresh(){ const id=studentId(); if(!id)return; try{const r=await fetch(`/api/student/${encodeURIComponent(id)}/subscription`,{cache:"no-store"}); if(r.ok)render(await r.json());}catch(_){} }
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",refresh); else refresh(); setInterval(refresh,60000);
})();
