/* NABIL book-first preview: a fast book-backed entry while /api/chat runs.
 * Excerpt != verified visual analysis. The original page is offered for inspection.
 */
(()=>{
"use strict";
if(window.nabilBookFirstInstalled)return;
window.nabilBookFirstInstalled=true;
const originalFetch=window.fetch.bind(window);
let pending=0;
function show(form,id){
  const title=String(form.get("lesson")||"").trim();
  if(!title)return ()=>{};
  document.getElementById("nabilBookFirstCard")?.remove();
  const el=document.createElement("aside");
  el.id="nabilBookFirstCard";
  el.setAttribute("role","status");
  el.setAttribute("aria-live","polite");
  el.style.cssText="position:relative;width:min(100%,980px);box-sizing:border-box;margin:12px auto;background:#102a43;color:#f0fbff;border:2px solid #4cc6f5;border-radius:16px;padding:16px;box-shadow:0 5px 22px #0005;font:16px/1.55 Arial,sans-serif;direction:ltr";
  const head=document.createElement("strong");
  head.style.cssText="display:block;font-size:20px;color:#8ee7ff;margin-right:20px";
  head.textContent="📘 Lesson Entrance — "+title;
  const status=document.createElement("div");
  status.textContent="Opening the textbook and preparing your lesson…";
  const content=document.createElement("p");
  content.textContent="I’m opening the official textbook first. This book-backed entrance appears immediately while NABIL AI prepares the full interactive explanation.";
  const page=document.createElement("strong");
  page.style.cssText="display:block;color:#a4f3d3";
  const figureWrap=document.createElement("div");
  figureWrap.style.cssText="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;margin-top:10px";
  const link=document.createElement("a");
  link.textContent="🔎 Open original textbook page at full size";
  link.rel="noopener noreferrer";
  link.target="_blank";
  link.style.cssText="display:none;color:#a8eaff";
  const close=document.createElement("button");
  close.type="button";
  close.setAttribute("aria-label","Close preview");
  close.textContent="×";
  close.onclick=()=>el.remove();
  close.style.cssText="position:absolute;right:8px;top:2px;background:transparent;color:#fff;font-size:27px;border:0;cursor:pointer";
  el.append(head,close,status,content,page,figureWrap,link);
  const chat=document.getElementById("chat");
  if(chat)chat.appendChild(el); else document.body.appendChild(el);
  try{el.scrollIntoView({behavior:"smooth",block:"nearest"})}catch(_e){}
  const formData=new FormData();
  for(const key of ["grade","subject","curriculum","language","lesson"])
    formData.append(key,String(form.get(key)||""));
  const controller=new AbortController();
  const previewTimeout=window.setTimeout(()=>controller.abort(),16000);
  originalFetch("/api/textbooks/lesson-preview",{
    method:"POST",body:formData,signal:controller.signal
  }).then(r=>r.ok?r.json():null).then(result=>{
    window.clearTimeout(previewTimeout);
    if(!el.isConnected||id!==pending)return;
    if(!result||result.status!=="indexed"){
      status.textContent="The full lesson is being prepared";
      content.textContent="The page lookup has not returned an indexed source yet. No page number or book figure will be invented.";
      return;
    }
    status.textContent="✅ Official textbook excerpt retrieved";
    page.textContent=result.book_title+" | PRINTED PAGE "+result.printed_page;
    content.textContent=result.source_excerpt||"Open the original indexed page below.";
    const path=result.page_image_url;
    const figures=Array.isArray(result.figure_image_urls)?result.figure_image_urls:[];
    figureWrap.replaceChildren();
    figures.slice(0,3).forEach((src,index)=>{
      if(!/^\/api\/textbooks\/[a-z0-9-]+\/pages\/\d+\/figures\/\d+\/image$/i.test(src))return;
      const holder=document.createElement("figure");
      holder.style.cssText="margin:0;background:#071d31;border:1px solid #3984aa;border-radius:10px;padding:8px";
      const original=document.createElement("img");
      original.loading="lazy";
      original.onerror=()=>holder.remove();
      original.src=src;
      original.alt="Original figure extracted from the verified textbook page";
      original.style.cssText="display:block;width:100%;height:220px;object-fit:contain;border-radius:7px;background:#fff";
      const cap=document.createElement("figcaption");
      cap.textContent="📐 Original textbook figure · printed page "+result.printed_page;
      cap.style.cssText="font-size:12px;margin-top:6px;color:#a8eaff";
      holder.append(original,cap); figureWrap.appendChild(holder);
    });
    if(path&&/^\/api\/textbooks\/[a-z0-9-]+\/pages\/\d+\/image$/i.test(path)){
      link.href=path;
      link.textContent="🔎 Inspect the complete original page (not shown on the lesson board)";
      link.style.display="inline-block";
    }
  }).catch(()=>{
    window.clearTimeout(previewTimeout);
    if(el.isConnected&&id===pending){
      status.textContent="The full lesson is still being prepared";
      content.textContent="The book preview did not finish. I will not show an unverified textbook page or figure.";
    }
  });
  return ()=>{
    // The AI request can complete before the independent book lookup. Keep
    // waiting for the source rather than aborting a valid citation request.
    if(el.isConnected){
      status.textContent="✅ The interactive lesson is ready below; verifying the original book page independently.";
    }
  };
}
window.fetch=function(input,options){
  const url=typeof input==="string"?input:(input?.url||"");
  const body=options?.body;
  if(!/\/?api\/chat(?:\?|$)/.test(url)||!(body instanceof FormData)||
     String(body.get("activity_mode")||"lesson")!=="lesson"||
     !["full_lesson","board_lesson"].includes(String(body.get("teaching_mode")||"full_lesson"))){
    return originalFetch(input,options);
  }
  const id=++pending;
  const done=show(body,id);
  return originalFetch(input,options).then(result=>{done();return result;},error=>{done();throw error;});
};
})();
