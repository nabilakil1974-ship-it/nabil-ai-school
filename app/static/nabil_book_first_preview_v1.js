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
  el.style.cssText="position:fixed;z-index:2147483000;top:88px;left:50%;transform:translateX(-50%);width:min(92vw,640px);max-height:57vh;overflow:auto;background:#102a43;color:#f0fbff;border:2px solid #4cc6f5;border-radius:16px;padding:16px;box-shadow:0 8px 35px #0009;font:16px/1.5 Arial,sans-serif;direction:ltr";
  const head=document.createElement("strong");
  head.style.cssText="display:block;font-size:20px;color:#8ee7ff;margin-right:20px";
  head.textContent="📘 "+title;
  const status=document.createElement("div");
  status.textContent="Opening the textbook and preparing your lesson…";
  const content=document.createElement("p");
  content.textContent="Your lesson will appear when ready. You can inspect the original page meanwhile.";
  const page=document.createElement("strong");
  page.style.cssText="display:block;color:#a4f3d3";
  const img=document.createElement("img");
  img.alt="Original indexed textbook page, not an AI-generated drawing";
  img.loading="lazy";
  img.style.cssText="display:none;width:min(100%,395px);max-height:31vh;object-fit:contain;margin:9px auto;border:1px solid #7ad2ff;border-radius:8px;cursor:zoom-in";
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
  el.append(head,close,status,content,page,img,link);
  document.body.appendChild(el);
  const formData=new FormData();
  for(const key of ["grade","subject","curriculum","language","lesson"])
    formData.append(key,String(form.get(key)||""));
  const controller=new AbortController();
  originalFetch("/api/textbooks/lesson-preview",{
    method:"POST",body:formData,signal:controller.signal
  }).then(r=>r.ok?r.json():null).then(result=>{
    if(!el.isConnected||id!==pending)return;
    if(!result||result.status!=="indexed"){
      status.textContent="Preparing the selected lesson…";
      content.textContent="No verified original-page preview is available yet.";
      return;
    }
    status.textContent="✅ Official textbook excerpt retrieved";
    page.textContent=result.book_title+" | PRINTED PAGE "+result.printed_page;
    content.textContent=result.source_excerpt||"Open the original indexed page below.";
    const path=result.page_image_url;
    if(path&&/^\/api\/textbooks\/[a-z0-9-]+\/pages\/\d+\/image$/i.test(path)){
      img.src=path;
      img.style.display="block";
      link.href=path;
      link.style.display="inline";
      img.onclick=()=>window.open(path,"_blank","noopener");
    }
  }).catch(()=>{
    if(el.isConnected&&id===pending)
      status.textContent="Preparing the selected lesson…";
  });
  return ()=>{
    controller.abort();
    if(el.isConnected){
      status.textContent="✅ Your lesson response is ready";
      window.setTimeout(()=>{if(id===pending)el.remove();},2200);
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
