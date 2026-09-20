/* NABIL book-first preview: a fast book-backed entry while /api/chat runs.
 * Excerpt != verified visual analysis. The original page is offered for inspection.
 */
(()=>{
"use strict";
if(window.nabilBookFirstInstalled)return;
window.nabilBookFirstInstalled=true;
const originalFetch=window.fetch.bind(window);
let pending=0;
const printedPageFromMessage=message=>{
  const m=String(message||"").match(/(?:page|pages|صفحة|الصفحة|صفحه|ص\.)\s*(?:رقم|number|no\.?)?\s*[:#-]?\s*(\d{1,4})/i);
  return m?m[1]:"";
};
function installPagePicker(){
  if(document.getElementById("nabilPrintedPagePicker"))return;
  const select=document.getElementById("lessonSelect");
  if(!select)return;
  const wrap=document.createElement("label");
  wrap.id="nabilPrintedPagePicker";
  wrap.style.cssText="display:flex;align-items:center;gap:8px;padding:8px 11px;margin:7px 0;color:#a8eaff;font:14px Arial,sans-serif;max-width:100%;box-sizing:border-box";
  wrap.appendChild(document.createTextNode("📘 رقم صفحة كتاب الدولة المطبوعة (اختياري):"));
  const input=document.createElement("input");
  input.id="nabilPrintedPageInput";
  input.type="number";input.min="1";input.max="9999";input.step="1";
  input.placeholder="55";
  input.style.cssText="width:85px;min-width:65px;border:1px solid #50bff0;background:#0b2138;color:#fff;border-radius:9px;padding:9px;font-size:16px";
  input.setAttribute("aria-label","رقم صفحة الكتاب المطبوعة");
  wrap.appendChild(input);
  select.insertAdjacentElement("afterend",wrap);
}
// Exact printed-page requests are an alternative to imperfect lesson titles.
// The legacy start button still requires lessonSelect.value; provide a clearly
// labelled temporary PAGE selection at capture phase before its click handler.
// Never pretend it is an indexed chapter title: the server verifies the page.
function prepareExactPageLesson(){
  const input=document.getElementById("nabilPrintedPageInput");
  const select=document.getElementById("lessonSelect");
  if(!input||!select)return;
  const raw=String(input.value||"").trim();
  if(!/^\d{1,4}$/.test(raw)||Number(raw)<1){
    const temporary=select.selectedOptions?.[0];
    if(temporary?.dataset?.nabilPageTemporary==="yes"){
      temporary.remove(); select.selectedIndex=0;
    }
    return;
  }
  const existing=String(select.value||"").trim();
  if(existing&&existing!=="المحتوى قيد الفهرسة"&&!select.selectedOptions[0]?.dataset?.nabilPageTemporary)return;
  const synthetic="صفحة الكتاب المطبوعة "+Number(raw);
  let option=Array.from(select.options).find(o=>o.dataset.nabilPageTemporary==="yes");
  if(!option){
    option=document.createElement("option");
    option.dataset.nabilPageTemporary="yes";
    select.appendChild(option);
  }
  option.value=synthetic;
  option.textContent=synthetic+" (يتم التحقق من الكتاب)";
  select.value=synthetic;
}
document.addEventListener("click",event=>{
  if(event.target?.closest?.("#startLesson"))prepareExactPageLesson();
},true);
document.addEventListener("input",event=>{
  if(event.target?.id!=="nabilPrintedPageInput")return;
  const selected=document.getElementById("lessonSelect")?.selectedOptions?.[0];
  if(selected?.dataset?.nabilPageTemporary==="yes")prepareExactPageLesson();
},true);
if(document.readyState==="loading"){
  document.addEventListener("DOMContentLoaded",installPagePicker,{once:true});
}else installPagePicker();
// Reuse the single already-generated, verified lesson response. No second AI call.
function installNotebookSummary(reply){
  const raw=String(reply||"");
  const match=/^##\s*(?:Notebook Summary|ملخّص الدرس للدفتر|ملخص الدرس للدفتر|Résumé pour le cahier)\s*$/im.exec(raw);
  if(!match)return;
  const body=raw.slice(match.index+match[0].length).split(/\n(?=##\s)/)[0].trim();
  if(!body)return;
  document.getElementById("nabilNotebookSummary")?.remove();
  const box=document.createElement("details");
  box.id="nabilNotebookSummary";
  box.style.cssText="max-width:980px;margin:12px auto;border:2px solid #4cc6f5;border-radius:14px;padding:14px;background:#102a43;color:#fff;box-sizing:border-box";
  const title=document.createElement("summary");
  title.textContent="📘 ملخّص الدرس للدفتر | Notebook Summary";
  title.style.cssText="cursor:pointer;font-weight:bold;color:#a8eaff;font-size:18px";
  const content=document.createElement("pre");
  content.textContent=body;
  content.style.cssText="white-space:pre-wrap;overflow-wrap:anywhere;font:15px/1.65 Arial,sans-serif;direction:auto";
  const copy=document.createElement("button");
  copy.type="button";copy.textContent="📋 نسخ الملخّص";
  copy.onclick=()=>navigator.clipboard?.writeText(body);
  box.append(title,content,copy);
  const chat=document.getElementById("chat");
  if(chat)chat.appendChild(box);
}
function show(form,id){
  let lessonReady=false;
  let lessonFailed=false;
  let sourceIndexed=false;
  let sourceImageLoaded=false;
  const updateStatus=()=>{
    if(!el.isConnected||id!==pending)return;
    if(lessonFailed){
      status.textContent="⚠️ The original textbook page is available, but the AI explanation did not complete.";
      return;
    }
    if(lessonReady&&sourceIndexed)status.textContent=sourceImageLoaded
      ?"✅ The lesson and original textbook page are ready below."
      :"✅ The lesson is ready; the indexed textbook page is loading below.";
    else if(lessonReady)status.textContent="✅ The lesson is ready below; the textbook preview is separate.";
    else if(sourceIndexed)status.textContent="✅ Exact textbook page indexed; NABIL AI is preparing the explanation.";
  };
  const chosen=String(form.get("book_page")||"").trim()||
    printedPageFromMessage(form.get("message"));
  const title=chosen?"Printed textbook page "+chosen:String(form.get("lesson")||"").trim();
  if(!title)return {done:()=>{},fail:()=>{}};
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
  const originalPage=document.createElement("details");
  originalPage.style.cssText="margin:12px 0;border:1px solid #3984aa;border-radius:10px;padding:9px";
  originalPage.hidden=true;
  const pageToggle=document.createElement("summary");
  pageToggle.textContent="📷 عرض الصورة الأصلية لصفحة الكتاب";
  pageToggle.style.cssText="cursor:pointer;color:#a8eaff";
  const originalPageImage=document.createElement("img");
  originalPageImage.alt="Actual scanned page from the indexed government textbook";
  originalPageImage.loading="lazy";
  originalPageImage.style.cssText="display:block;max-width:100%;width:auto;height:auto;margin:12px auto;background:#fff";
  originalPageImage.onload=()=>{sourceImageLoaded=true;updateStatus()};
  originalPageImage.onerror=()=>{ originalPage.hidden=true; sourceImageLoaded=false; updateStatus(); };
  originalPage.append(pageToggle,originalPageImage);
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
  el.append(head,close,status,content,page,originalPage,figureWrap,link);
  const chat=document.getElementById("chat");
  if(chat)chat.appendChild(el); else document.body.appendChild(el);
  try{el.scrollIntoView({behavior:"smooth",block:"nearest"})}catch(_e){}
  const formData=new FormData();
  for(const key of ["grade","subject","curriculum","language","lesson","message","book_page"])
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
    if(chosen&&String(result.printed_page)!==String(Number(chosen))){
      status.textContent="⚠️ The indexed source does not match the requested printed page.";
      content.textContent="The page number has not been changed automatically. Please retry the exact requested page.";
      return;
    }
    sourceIndexed=true;
    updateStatus();
    page.textContent=result.book_title+" | PRINTED PAGE "+result.printed_page;
    // OCR is retrieval data, NOT verified student-facing prose: chemical shell
    // superscripts and mixed columns are frequently corrupted in raw excerpts.
    // Show the actual page image and let the separate tutor explain it.
    content.textContent="The original indexed page is available below. NABIL AI explains its actual concepts separately; raw PDF extraction is not a student explanation.";
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
      originalPage.hidden=false;
      originalPageImage.src=path;
      link.href=path;
      link.textContent="🔎 Open the original textbook page in full size";
      link.style.display="inline-block";
    }
  }).catch(()=>{
    window.clearTimeout(previewTimeout);
    if(el.isConnected&&id===pending){
      if(!lessonReady)status.textContent="The independent textbook preview timed out or failed";
      else updateStatus();
      content.textContent="The lesson request is separate. Open the sourced page links in the lesson when available; the preview failure does not mean the book was not indexed.";
    }
  });
  const fail=()=>{
    if(el.isConnected){lessonFailed=true;updateStatus()}
  };
  const done=()=>{
    // The AI request can complete before the independent book lookup. Keep
    // waiting for the source rather than aborting a valid citation request.
    if(el.isConnected){
      lessonReady=true;
      updateStatus();
    }
  };
  return {done,fail};
}
window.fetch=function(input,options){
  const url=typeof input==="string"?input:(input?.url||"");
  const body=options?.body;
  if(!/\/?api\/chat(?:\?|$)/.test(url)||!(body instanceof FormData)||
     String(body.get("activity_mode")||"lesson")!=="lesson"||
     !["full_lesson","board_lesson"].includes(String(body.get("teaching_mode")||"full_lesson"))){
    return originalFetch(input,options);
  }
  const picker=document.getElementById("nabilPrintedPageInput");
  const msg=String(body.get("message")||"");
  const isLessonStart=/begin\s+the\s+(?:complete\s+)?selected\s+lesson|ابدأ\s+الدرس|commence\s+maintenant/i.test(msg);
  const typedPage=printedPageFromMessage(msg);
  // Keep the exact printed page across transient provider failures and
  // automatic lesson retries. The student's explicit page in a NEW question
  // takes priority. Never silently fall back to a title-only first-match page.
  if(typedPage){
    body.set("book_page",typedPage);
    if(picker)picker.value=typedPage;
  }else if(picker?.value&&isLessonStart&&/^\d{1,4}$/.test(String(picker.value).trim())){
    body.set("book_page",String(Number(picker.value)));
  }
  const id=++pending;
  const {done,fail}=show(body,id);
  return originalFetch(input,options).then(result=>{
    if(result.ok){
      done();
      result.clone().json().then(data=>{
        if(id===pending)window.setTimeout(()=>installNotebookSummary(data?.reply),100);
      }).catch(()=>{});
    }else{
      fail();
    }
    return result;
  },error=>{fail();throw error;});
};
})();
