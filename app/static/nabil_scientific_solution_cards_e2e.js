/* NABIL AI — Scientific Solution Cards E2E
 * Shared renderer for Root Chat and the General Exercises page.
 * Function-study values/graph come from the deterministic backend card engine.
 */
(()=>{
"use strict";

const STYLE_ID="nabil-scientific-solution-cards-e2e";
const esc=v=>String(v??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const arr=v=>Array.isArray(v)?v.filter(x=>x!==null&&x!==undefined&&String(x).trim()!==""):[];
const text=v=>String(v??"").trim();

function runtimeLabKey(question){
 let h=2166136261;
 const value=String(question||"");
 for(let i=0;i<value.length;i++){h^=value.charCodeAt(i);h=Math.imul(h,16777619);}
 return "runtime-question:"+((h>>>0).toString(16));
}

function langOf(spec={}){
 const v=text(spec.language).toLowerCase();
 if(v==="fr"||v.includes("fran"))return "fr";
 if(v==="ar"||v.includes("عرب"))return "ar";
 return "en";
}
function labelsFor(spec={}){
 const l=langOf(spec);
 if(l==="fr")return {analysis:"📘 Analyse",visual:"📈 Graphe et variations",final:"✅ Carte finale",verify:"Vérification",enlarge:"🔎 Agrandir le graphe",read:"🔊 Lire la solution",stop:"⏹ Arrêter",missing:"Aucun visuel vérifié n’a été fourni."};
 if(l==="ar")return {analysis:"📘 التحليل",visual:"📈 الرسم وجدول التغيّرات",final:"✅ البطاقة النهائية",verify:"التحقق",enlarge:"🔎 تكبير الرسم",read:"🔊 قراءة الحل",stop:"⏹ إيقاف الصوت",missing:"لم يصل رسم علمي موثّق لهذه البطاقة."};
 return {analysis:"📘 Function Analysis",visual:"📈 Graph & Variation",final:"✅ Final Card",verify:"Verification",enlarge:"🔎 Enlarge visual",read:"🔊 Read solution",stop:"⏹ Stop voice",missing:"No verified visual was supplied for this card."};
}
function playbackLanguage(spec={}){
 const l=langOf(spec);
 return l==="fr"?"Français":l==="ar"?"العربية":"English";
}

function ensureStyle(){
 if(document.getElementById(STYLE_ID))return;
 const s=document.createElement("style");
 s.id=STYLE_ID;
 s.textContent=`
 .nabil-sci-card{--bg:#07192d;--panel:#0d2945;--panel2:#0a2239;--line:#2f5f86;--cyan:#6ce7ff;--gold:#ffd36a;--green:#7ce6b8;--red:#ff8b98;--txt:#f4fbff;--muted:#bed4e5;background:radial-gradient(circle at 50% -20%,#153f68,#07192d 70%);color:var(--txt);border:1px solid #2d638d;border-radius:22px;padding:14px;box-shadow:0 16px 44px rgba(0,0,0,.24);margin:14px 0;overflow:hidden;width:100%;box-sizing:border-box}
 .nabil-sci-top{display:flex;gap:12px;align-items:center;justify-content:space-between;border-bottom:1px solid #2a5479;padding:2px 4px 11px;flex-wrap:wrap}
 .nabil-sci-brand{font-weight:900;color:var(--cyan);letter-spacing:.7px}.nabil-sci-badge{font-size:.75rem;border:1px solid #46789e;border-radius:999px;padding:4px 10px;color:#d8efff}
 .nabil-sci-title{margin:9px 0 2px;font-size:clamp(1.15rem,3vw,1.65rem);line-height:1.25;overflow-wrap:anywhere}
 .nabil-sci-grid{display:grid;grid-template-columns:minmax(250px,.92fr) minmax(390px,1.55fr) minmax(190px,.64fr);gap:12px;margin-top:12px;align-items:stretch}
 .nabil-sci-panel{background:linear-gradient(160deg,#0f3151,#0a2239);border:1px solid var(--line);border-radius:17px;padding:13px;min-width:0}
 .nabil-sci-panel h3{margin:0 0 9px;color:#9eeeff;font-size:1rem}.nabil-sci-list{margin:0;padding-inline-start:18px;line-height:1.65}.nabil-sci-list li{margin:5px 0;overflow-wrap:anywhere}
 .nabil-sci-section{border-top:1px solid #284e6f;padding-top:9px;margin-top:9px}.nabil-sci-label{font-weight:800;color:#8fe8ff}.nabil-sci-value{color:#fff;white-space:pre-wrap;overflow-wrap:anywhere}
 .nabil-sci-visual{min-height:310px;display:flex;flex-direction:column;gap:10px}.nabil-sci-visual-stage{flex:1;display:grid;place-items:center;background:#061827;border:1px solid #274d6d;border-radius:14px;padding:10px;overflow:auto}
 .nabil-sci-visual-stage svg,.nabil-sci-visual-stage canvas,.nabil-sci-visual-stage img{display:block;max-width:100%;height:auto;max-height:480px}
 .nabil-sci-visual-note{color:var(--muted);font-size:.82rem}
 .nabil-sci-teacher{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:8px;min-height:100%}.nabil-sci-avatar{width:min(100%,180px);max-height:230px;object-fit:contain;filter:drop-shadow(0 12px 22px rgba(0,0,0,.25))}
 .nabil-sci-teacher strong{color:var(--cyan);font-size:1.05rem}.nabil-sci-teacher p{margin:0;color:#d7e9f6;line-height:1.5}
 .nabil-sci-final{margin-top:12px;background:linear-gradient(145deg,#0e3547,#0b2939);border:1px solid #3b8b8a;border-radius:16px;padding:12px}
 .nabil-sci-final h3{margin:0 0 7px;color:#8ff3d7}.nabil-sci-results{display:flex;gap:8px;flex-wrap:wrap}.nabil-sci-chip{border:1px solid #41769a;background:#0c2a45;border-radius:999px;padding:5px 9px;font-size:.84rem;overflow-wrap:anywhere}
 .nabil-sci-verify{margin-top:9px;border-inline-start:4px solid var(--green);background:#0d2d36;border-radius:9px;padding:9px 10px}
 .nabil-sci-table-wrap{overflow-x:auto;border-radius:11px;border:1px solid #315a79}.nabil-sci-table{width:100%;border-collapse:collapse;table-layout:fixed;min-width:620px;background:#081d31}
 .nabil-sci-table th,.nabil-sci-table td{border:1px solid #315a79;padding:8px 5px;text-align:center;vertical-align:middle;white-space:normal;word-break:normal}
 .nabil-sci-table th{width:92px;color:#9eeeff;background:#0c2943}.nabil-sci-table td{color:#f4fbff}.nabil-sci-critical{color:var(--gold)!important;font-weight:800}.nabil-sci-asym{color:var(--red)!important;font-weight:800}
 .nabil-sci-tools{display:flex;gap:7px;flex-wrap:wrap;margin-top:10px}.nabil-sci-tools button{border:1px solid #4d80a5;background:#123d60;color:white;border-radius:10px;padding:8px 11px;cursor:pointer;font:inherit}
 .nabil-sci-tools button:focus-visible{outline:3px solid #ffe084;outline-offset:2px}
 .nabil-sci-missing{color:#ffd7a0;border:1px dashed #84633d;padding:10px;border-radius:10px;text-align:center}
 .nabil-general-scientific-host{width:100%;max-width:100%;box-sizing:border-box}
 @media(max-width:1080px){.nabil-sci-grid{grid-template-columns:minmax(250px,.9fr) minmax(360px,1.5fr)}.nabil-sci-teacher-panel{grid-column:1/-1}.nabil-sci-teacher{flex-direction:row;text-align:start;justify-content:flex-start}.nabil-sci-avatar{width:110px}}
 @media(max-width:760px){.nabil-sci-card{padding:10px;border-radius:16px}.nabil-sci-grid{grid-template-columns:1fr}.nabil-sci-panel{padding:11px}.nabil-sci-teacher-panel{grid-column:auto}.nabil-sci-teacher{flex-direction:row;text-align:start}.nabil-sci-avatar{width:84px;max-height:112px}.nabil-sci-visual{min-height:250px}.nabil-sci-table{min-width:560px;font-size:.86rem}}
 `;
 document.head.appendChild(s);
}

function detectKind(question="",subject="",spec={}){
 const declared=text(spec.kind||spec.card_type||subject).toLowerCase();
 const q=(text(question)+" "+declared).toLowerCase();
 if(/function|fonction|دال|domain|domaine|derivative|dériv|asympt|variation|(?:^|\s)(?:fx|f\s*x)\s*=/.test(q))return "function_study";
 if(/physics|physique|فيز/.test(q))return "physics";
 if(/chem|chim|كيمي/.test(q))return "chemistry";
 if(/biology|biologie|أحياء|احياء/.test(q))return "biology";
 if(/science|علوم/.test(q))return "general_science";
 return declared||"mathematics";
}

function normalizeSections(spec){
 if(Array.isArray(spec.sections))return spec.sections
   .filter(x=>x&&text(x.label)&&arr(x.items).length)
   .map(x=>({label:text(x.label),items:arr(x.items).map(text)}));
 const out=[];
 const push=(label,v)=>{const xs=arr(v);if(xs.length)out.push({label,items:xs.map(text)})};
 push("Given",spec.given||spec.givens);
 push("Required",spec.required);
 push("Rule / Method",spec.method||spec.rules||spec.formulae);
 push("Steps",spec.steps);
 return out;
}

function extractBlock(reply,labels){
 const src=text(reply);
 for(const label of labels){
   const re=new RegExp("(?:^|\\n)\\s*(?:#{1,5}\\s*)?"+label+"\\s*[:：]?\\s*([^\\n]*(?:\\n(?!\\s*(?:#{1,5}\\s*)?[A-Za-zÀ-ÿ\\u0600-\\u06ff][^\\n]{0,50}:)[^\\n]*){0,4})","i");
   const m=src.match(re);
   if(m&&text(m[1]))return text(m[1]);
 }
 return "";
}

function deriveSpecFromChat(result={},question=""){
 const reply=text(result.reply);
 const subject=text(result.subject||result.current_subject||"");
 const kind=detectKind(question,subject,{});
 const spec={kind,subject,title:text(question)||"Scientific Solution",sections:[],key_results:[],verification:[]};
 const final=extractBlock(reply,["Final Answer","Answer","Réponse finale","الجواب النهائي","النتيجة النهائية"]);
 if(final)spec.key_results=[final];
 if(kind==="function_study"){
   const f={
     expression:extractBlock(reply,["Function","Fonction","الدالة"]),
     domain:extractBlock(reply,["Domain","Domaine","مجال التعريف"]),
     limits:extractBlock(reply,["Limits?","Limites?","النهايات"]),
     asymptotes:extractBlock(reply,["Asymptotes?","Asymptotes","المقارب(?:ات)?"]),
     derivative:extractBlock(reply,["Derivative","Dérivée","المشتقة"]),
     critical_points:extractBlock(reply,["Critical points?","Points critiques?","النقاط الحرجة"]),
     monotonicity:extractBlock(reply,["Increasing.*decreasing","Variations?","التزايد.*التناقص"]),
     extrema:extractBlock(reply,["Extrema","Maximum.*Minimum","القيم القصوى"]),
     variation_text:extractBlock(reply,["Variation Table","Tableau de variations","جدول التغيرات"])
   };
   spec.function_study=f;
   spec.sections=[
    {label:"Domain",items:f.domain?[f.domain]:[]},
    {label:"Limits / Asymptotes",items:[f.limits,f.asymptotes].filter(Boolean)},
    {label:"Derivative / Critical points",items:[f.derivative,f.critical_points].filter(Boolean)},
    {label:"Variation / Extrema",items:[f.monotonicity,f.extrema].filter(Boolean)}
   ].filter(s=>s.items.length);
 }else{
   const given=extractBlock(reply,["Given","Données","المعطيات"]);
   const required=extractBlock(reply,["Required","Demandé","المطلوب"]);
   const rule=extractBlock(reply,["Formula","Law","Rule","Loi","Règle","القانون","القاعدة"]);
   const verification=extractBlock(reply,["Verification","Check","Vérification","التحقق"]);
   spec.sections=[
     {label:"Given",items:given?[given]:[]},
     {label:"Required",items:required?[required]:[]},
     {label:"Rule / Method",items:rule?[rule]:[]},
     {label:"Solution",items:reply?[reply]:[]}
   ].filter(s=>s.items.length);
   if(verification)spec.verification=[verification];
 }
 spec.drawings=Array.isArray(result.drawings)?result.drawings:[];
 return spec;
}

function svgCoordinatePlane(d){
 if(!d||!["coordinate_plane","function","graph"].includes(text(d.type).toLowerCase()))return "";
 const rawSeries=Array.isArray(d.series)?d.series:[];
 const series=rawSeries.map(part=>Array.isArray(part)?part:(Array.isArray(part?.points)?part.points:[])).filter(part=>part.length>=2);
 if(!series.length)return "";
 const xmin=Number(d.xmin??d.x_min),xmax=Number(d.xmax??d.x_max),ymin=Number(d.ymin??d.y_min),ymax=Number(d.ymax??d.y_max);
 if(![xmin,xmax,ymin,ymax].every(Number.isFinite)||xmin>=xmax||ymin>=ymax)return "";
 const W=760,H=500,L=58,R=24,T=24,B=48,w=W-L-R,h=H-T-B;
 const px=x=>L+(Number(x)-xmin)*w/(xmax-xmin);
 const py=y=>T+h-(Number(y)-ymin)*h/(ymax-ymin);
 const f=n=>Math.round(n*100)/100;
 let body=`<rect width="${W}" height="${H}" rx="18" fill="#061827"/>`;
 for(let i=1;i<10;i++){
   const gx=L+w*i/10,gy=T+h*i/10;
   body+=`<line x1="${f(gx)}" x2="${f(gx)}" y1="${T}" y2="${T+h}" stroke="#173b58" stroke-width="1"/>`;
   body+=`<line x1="${L}" x2="${L+w}" y1="${f(gy)}" y2="${f(gy)}" stroke="#173b58" stroke-width="1"/>`;
 }
 if(xmin<=0&&xmax>=0)body+=`<line x1="${f(px(0))}" x2="${f(px(0))}" y1="${T}" y2="${T+h}" stroke="#b9d8e9" stroke-width="1.7"/>`;
 if(ymin<=0&&ymax>=0)body+=`<line x1="${L}" x2="${L+w}" y1="${f(py(0))}" y2="${f(py(0))}" stroke="#b9d8e9" stroke-width="1.7"/>`;
 (d.vertical_asymptotes||[]).forEach(a=>{
   const x=Number(a?.x??a);if(!Number.isFinite(x)||x<xmin||x>xmax)return;
   body+=`<line x1="${f(px(x))}" x2="${f(px(x))}" y1="${T}" y2="${T+h}" stroke="#ff8b98" stroke-width="2" stroke-dasharray="9 7"/>`;
   body+=`<text x="${f(px(x)+6)}" y="${T+18}" fill="#ffb0b8" font-size="13">${esc(a?.label||("x = "+x))}</text>`;
 });
 (d.oblique_asymptotes||[]).forEach(a=>{
   const m=Number(a?.m),b=Number(a?.b);if(!Number.isFinite(m)||!Number.isFinite(b))return;
   const y1=m*xmin+b,y2=m*xmax+b;
   body+=`<line x1="${L}" x2="${L+w}" y1="${f(py(y1))}" y2="${f(py(y2))}" stroke="#ff8b98" stroke-width="2" stroke-dasharray="9 7"/>`;
 });
 series.forEach((part,index)=>{
   const pts=part.filter(v=>Array.isArray(v)&&v.length>=2&&Number.isFinite(Number(v[0]))&&Number.isFinite(Number(v[1])))
     .filter(v=>Number(v[0])>=xmin&&Number(v[0])<=xmax&&Number(v[1])>=ymin&&Number(v[1])<=ymax);
   if(pts.length<2)return;
   const p=pts.map(v=>f(px(v[0]))+","+f(py(v[1]))).join(" ");
   const stroke=index%2===0?"#39c9ff":"#ffd36a";
   body+=`<polyline points="${p}" fill="none" stroke="${stroke}" stroke-width="3.2" stroke-linejoin="round" stroke-linecap="round"/>`;
 });
 (d.markers||[]).forEach(pt=>{
   const x=Number(pt.x),y=Number(pt.y);if(!Number.isFinite(x)||!Number.isFinite(y)||x<xmin||x>xmax||y<ymin||y>ymax)return;
   body+=`<circle cx="${f(px(x))}" cy="${f(py(y))}" r="5" fill="#ffd36a" stroke="#07192d" stroke-width="2"/>`;
   if(pt.label)body+=`<text x="${f(px(x)+8)}" y="${f(py(y)-9)}" fill="#fff" font-size="13">${esc(pt.label)}</text>`;
 });
 body+=`<text x="${W-26}" y="${f(py(0)-8)}" fill="#d9f1ff" font-size="14">x</text>`;
 body+=`<text x="${f(px(0)+8)}" y="${T+15}" fill="#d9f1ff" font-size="14">y</text>`;
 return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(d.title||"Function graph")}">${body}</svg>`;
}

function renderDrawing(d){
 try{
  if(typeof window.renderNabilDiagram==="function"){
   const html=window.renderNabilDiagram(d)||"";
   if(/<(?:svg|canvas|img)\b/i.test(html))return html;
  }
 }catch(_e){}
 return svgCoordinatePlane(d);
}

function renderVisual(spec){
 const drawings=arr(spec.drawings);
 const rendered=drawings.map(renderDrawing).filter(Boolean);
 if(rendered.length)return rendered.join("");
 if(text(spec.visual_html))return spec.visual_html;
 return `<div class="nabil-sci-missing">${esc(labelsFor(spec).missing)}</div>`;
}

function renderVariationTable(table){
 if(!table||!Array.isArray(table.columns)||!Array.isArray(table.rows))return "";
 const cols=table.columns.map(text);
 if(!cols.length)return "";
 const colgroup='<colgroup><col style="width:92px">'+cols.map(()=>"<col>").join("")+"</colgroup>";
 const rows=table.rows.map(row=>{
   const cells=Array.isArray(row.cells)?row.cells.map(text):[];
   if(cells.length!==cols.length)return "";
   return '<tr><th>'+esc(row.label||"")+'</th>'+cells.map(v=>{
    const cls=/asym|∞|parallel|\\|\\|/i.test(text(v))?"nabil-sci-asym":(/0|max|min|critical/i.test(text(v))?"nabil-sci-critical":"");
    return '<td class="'+cls+'">'+esc(v)+'</td>';
   }).join("")+"</tr>";
 }).join("");
 return '<div class="nabil-sci-table-wrap"><table class="nabil-sci-table">'+colgroup+
        '<tr><th>x</th>'+cols.map(c=>'<td>'+esc(c)+'</td>').join("")+'</tr>'+rows+'</table></div>';
}

function speechTextFromSpec(spec={}){
 const sections=normalizeSections(spec);
 const results=arr(spec.key_results||spec.final_results||spec.final_answer);
 const verification=arr(spec.verification);
 const parts=[text(spec.title)];
 sections.forEach(s=>{parts.push(text(s.label));s.items.forEach(v=>parts.push(text(v)))});
 if(text(spec.teacher_note))parts.push(text(spec.teacher_note));
 results.forEach(v=>parts.push(text(v)));
 verification.forEach(v=>parts.push(text(v)));
 return parts.filter(Boolean).join(". ").replace(/\s+/g," ").trim();
}

function renderCard(spec={},target){
 ensureStyle();
 const host=typeof target==="string"?document.querySelector(target):target;
 if(!host)throw Error("NABIL Scientific Card target missing");
 const kind=detectKind(spec.title||"",spec.subject||"",spec);
 const sections=normalizeSections(spec);
 const verification=arr(spec.verification);
 const results=arr(spec.key_results||spec.final_results||spec.final_answer);
 const fs=spec.function_study||{};
 const L=labelsFor(spec);
 const rtl=langOf(spec)==="ar";
 const card=document.createElement("section");
 card.className="nabil-sci-card";
 card.dataset.cardKind=kind;
 card.dir=rtl?"rtl":"ltr";
 card.lang=langOf(spec)==="fr"?"fr":langOf(spec)==="ar"?"ar":"en";
 card.innerHTML=
 `<div class="nabil-sci-top">
   <div><div class="nabil-sci-brand">NABIL AI | منصة نبيل التعليمية الذكية</div>
   <h2 class="nabil-sci-title">${esc(spec.title||"Scientific Solution")}</h2></div>
   <div class="nabil-sci-badge">${esc(kind.replaceAll("_"," ").toUpperCase())}</div>
 </div>
 <div class="nabil-sci-grid">
   <div class="nabil-sci-panel nabil-sci-analysis">
     <h3>${esc(L.analysis)}</h3>
     ${sections.map(s=>`<div class="nabil-sci-section"><div class="nabil-sci-label">${esc(s.label)}</div><ul class="nabil-sci-list">${s.items.map(v=>`<li>${esc(v)}</li>`).join("")}</ul></div>`).join("")}
   </div>
   <div class="nabil-sci-panel nabil-sci-visual">
     <h3>${esc(L.visual)}</h3>
     <div class="nabil-sci-visual-stage">${renderVisual(spec)}</div>
     ${kind==="function_study"&&fs.variation_table?renderVariationTable(fs.variation_table):
       (kind==="function_study"&&text(fs.variation_text)?`<div class="nabil-sci-table-wrap"><div style="padding:10px;white-space:pre-wrap">${esc(fs.variation_text)}</div></div>`:"")}
   </div>
   <div class="nabil-sci-panel nabil-sci-teacher-panel">
     <div class="nabil-sci-teacher">
       <img class="nabil-sci-avatar" src="${esc(spec.avatar_src||"/static/nabil-profile.jpg")}" alt="NABIL AI" onerror="this.style.display='none'">
       <div><strong>NABIL AI</strong><p>${esc(spec.teacher_note||"")}</p></div>
     </div>
   </div>
 </div>
 <div class="nabil-sci-final">
   <h3>${esc(L.final)}</h3>
   ${results.length?`<div class="nabil-sci-results">${results.map(v=>`<span class="nabil-sci-chip">${esc(v)}</span>`).join("")}</div>`:""}
   ${verification.length?`<div class="nabil-sci-verify"><b>${esc(L.verify)}:</b><ul class="nabil-sci-list">${verification.map(v=>`<li>${esc(v)}</li>`).join("")}</ul></div>`:""}
   <div class="nabil-sci-tools">
     <button type="button" data-nabil-enlarge>${esc(L.enlarge)}</button>
     <button type="button" data-nabil-read>${esc(L.read)}</button>
     <button type="button" data-nabil-stop>${esc(L.stop)}</button>
   </div>
 </div>`;
 host.replaceChildren(card);
 card.dataset.nabilSpeechText=speechTextFromSpec(spec);
 card.dataset.nabilSpeechLanguage=playbackLanguage(spec);
 if(text(spec.lab_key))card.dataset.nabilSolutionLabKey=text(spec.lab_key);
 if(text(spec.renderer_contract))card.dataset.nabilRendererContract=text(spec.renderer_contract);

 card.querySelector("[data-nabil-enlarge]")?.addEventListener("click",()=>{
   const stage=card.querySelector(".nabil-sci-visual-stage");
   if(!stage)return;
   const modal=document.getElementById("drawingPreviewModal");
   const content=document.getElementById("drawingPreviewContent");
   if(modal&&content){content.replaceChildren(stage.cloneNode(true));modal.hidden=false;return}
   if(stage.requestFullscreen)stage.requestFullscreen().catch(()=>{});
 });
 card.querySelector("[data-nabil-read]")?.addEventListener("click",()=>{
   speakCard(card);
 });
 card.querySelector("[data-nabil-stop]")?.addEventListener("click",()=>{
   try{window.NABILBrowserTTS?.stop?.();window.stopNabilNeuralVoice?.();window.speechSynthesis?.cancel?.()}catch(_e){}
 try{card.dispatchEvent(new CustomEvent("nabil:teach-stop",{bubbles:true}))}catch(_e){}
  });
 try{window.MathJax?.typesetPromise?.([card])}catch(_e){}
 return card;
}

function resultSpec(result={},question=""){
 if(result&&result.solution_card&&typeof result.solution_card==="object"){
   const serverDrawings=Array.isArray(result.drawings)&&result.drawings.length?result.drawings:null;
   const cardDrawings=Array.isArray(result.solution_card.drawings)?result.solution_card.drawings:[];
   return Object.assign({},result.solution_card,{drawings:serverDrawings||cardDrawings});
 }
 return deriveSpecFromChat(result,question);
}

function renderFromChat(resultOrArgs={},questionArg="",targetArg=null){
 let result,question,target;
 if(arguments.length===1&&resultOrArgs&&("result" in resultOrArgs||"target" in resultOrArgs)){
   ({result={},question="",target} = resultOrArgs);
 }else{
   result=resultOrArgs||{};question=questionArg||"";target=targetArg;
 }
 return renderCard(resultSpec(result,question),target);
}

function speakCard(card){
  if(!card)return;
  const spoken=text(card.dataset.nabilSpeechText);
  const language=text(card.dataset.nabilSpeechLanguage)||"English";
  if(!spoken)return;
  try{window.NABILBrowserTTS?.stop?.();window.stopNabilNeuralVoice?.();window.speechSynthesis?.cancel?.()}catch(_e){}
  const fn=window.NABILBrowserTTS?.speak||window.__nabilScientificNativeSpeak||window.nabilSpeakClear;
  if(typeof fn==="function"){
    try{
      return Promise.resolve(fn(spoken,language,{
        nabilScientificCard:true,
        onstart:()=>{try{card.dispatchEvent(new CustomEvent("nabil:card-speech-start",{bubbles:true,detail:{language}}))}catch(_e){}},
        onend:()=>{try{card.dispatchEvent(new CustomEvent("nabil:card-speech-complete",{bubbles:true,detail:{language}}))}catch(_e){}}
      })).catch(()=>{})
    }catch(_e){}
  }
}

function hydrate(root=document){
 root.querySelectorAll("[data-nabil-solution-card]").forEach(node=>{
   if(node.dataset.hydrated==="1")return;
   let spec={};
   try{spec=JSON.parse(node.dataset.nabilSolutionCard||"{}")}catch(_e){return}
   node.dataset.hydrated="1";
   renderCard(spec,node);
 });
}

/* --------------------------------------------------------------------------
 * General Exercises integration
 * The old inline sendToAI can still create a legacy teacher bubble.  When the
 * backend returns solution_card, replace that bubble with this one canonical
 * card.  The provider's extra prose is no longer the student-visible solution.
 * -------------------------------------------------------------------------- */
function installGeneralExercisesBridge(){
 if(window.__nabilScientificGeneralBridgeInstalled)return;
 window.__nabilScientificGeneralBridgeInstalled=true;
 const originalFetch=window.fetch?.bind(window);
 if(typeof originalFetch!=="function")return;

 if(typeof window.nabilSpeakClear==="function"&&!window.__nabilScientificNativeSpeak){
   window.__nabilScientificNativeSpeak=window.nabilSpeakClear.bind(window);
   const native=window.__nabilScientificNativeSpeak;
   window.nabilSpeakClear=function(spoken,language,options={}){
     if(window.__nabilScientificGeneralPending&&!options?.nabilScientificCard)return Promise.resolve();
     return native(spoken,language,options);
   };
 }

 window.fetch=async function(input,init={}){
   const url=typeof input==="string"?input:String(input?.url||"");
   const body=init?.body;
   const general=url.includes("/api/chat")&&body instanceof FormData&&String(body.get("activity_mode")||"")==="general_exercises";
   const home=general&&String(body.get("teaching_mode")||"")==="home_live_tutor";
   if(!general||home)return originalFetch(input,init);

   // Legacy "General Exercises" used the full-lesson backend path, which could
   // invent extra practice exercises. Route the SAME student question through
   // the already-existing open tutor mode instead: one request -> one solution.
   body.set("teaching_mode","home_live_tutor");
   body.set("language","AUTO");

   const question=String(body.get("message")||"").trim();
   const beforeCount=document.querySelectorAll("#chat .message.teacher .bubble").length;
   window.__nabilScientificGeneralPending=true;
   let response;
   try{
     response=await originalFetch(input,init);
   }catch(error){
     window.__nabilScientificGeneralPending=false;
     throw error;
   }

   let data=null;
   try{data=await response.clone().json()}catch(_e){}
   if(!data||!data.solution_card||typeof data.solution_card!=="object"){
     window.__nabilScientificGeneralPending=false;
     return response;
   }

   const mount=()=>{
     let tries=0;
     const tick=()=>{
       const bubbles=[...document.querySelectorAll("#chat .message.teacher .bubble")];
       if(bubbles.length>beforeCount){
         const bubble=bubbles[bubbles.length-1];
         const host=document.createElement("div");
         host.className="nabil-general-scientific-host";
         bubble.replaceChildren(host);
         try{
           const card=renderFromChat(data,question,host);
           const labKey=runtimeLabKey(question);
           card.dataset.nabilSolutionLabKey=labKey;
           card.dataset.nabilRuntimeQuestion=question;
           try{
             window.dispatchEvent(new CustomEvent("nabil:solution-ready",{
               detail:{question,card,labKey,mode:"general_exercises",result:data}
             }));
           }catch(_e){}

           // The smart-learning panel clones the legacy bubble. If it has already
           // rendered, replace its old prose with the same canonical card too.
           window.setTimeout(()=>{
             const panel=document.getElementById("nv132Result");
             if(panel&&!panel.hidden){
               const panelHost=document.createElement("div");
               panelHost.className="nabil-general-scientific-panel-host";
               panel.replaceChildren(panelHost);
               try{
                 const panelCard=renderFromChat(data,question,panelHost);
                 panelCard.dataset.nabilSolutionLabKey=labKey;
                 panelCard.dataset.nabilRuntimeQuestion=question;
               }catch(_e){}
             }
           },220);

           window.__nabilScientificGeneralPending=false;
           try{window.NABILBrowserTTS?.stop?.();window.stopNabilNeuralVoice?.();window.speechSynthesis?.cancel?.()}catch(_e){}
           window.setTimeout(()=>speakCard(card),120);
           card.scrollIntoView({behavior:"smooth",block:"nearest"});
         }catch(error){
           window.__nabilScientificGeneralPending=false;
           console.warn("[NABIL_SCI_CARD] general exercise render fallback",error);
         }
         return;
       }
       tries++;
       if(tries<50)window.setTimeout(tick,40);
       else window.__nabilScientificGeneralPending=false;
     };
     tick();
   };
   window.setTimeout(mount,0);
   return response;
 };
}

window.NABILScientificCards={
 renderCard,renderFromChat,deriveSpecFromChat,hydrate,detectKind,
 speechTextFromSpec,speakCard,resultSpec
};
installGeneralExercisesBridge();
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",()=>hydrate(document),{once:true});
else hydrate(document);
})();
