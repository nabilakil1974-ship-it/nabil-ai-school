/* NABIL AI — Scientific Solution Cards E2E
 * Canonical renderer used by:
 *   1) generated exercise pages from scripts/nabil_lesson_factory.py
 *   2) Root / Root Chat (nabil_open_tutor_v1.js)
 *
 * One card contract, many subject-specific renderers.
 * No renderer invents scientific values: it displays only fields supplied
 * by the verified backend/lesson factory and verified drawing payloads.
 */
(()=>{
"use strict";

const STYLE_ID="nabil-scientific-solution-cards-e2e";
const esc=v=>String(v??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const arr=v=>Array.isArray(v)?v.filter(x=>x!==null&&x!==undefined&&String(x).trim()!==""):[];
const text=v=>String(v??"").trim();

function ensureStyle(){
 if(document.getElementById(STYLE_ID))return;
 const s=document.createElement("style");
 s.id=STYLE_ID;
 s.textContent=`
 .nabil-sci-card{--bg:#07192d;--panel:#0d2945;--panel2:#0a2239;--line:#2f5f86;--cyan:#6ce7ff;--gold:#ffd36a;--green:#7ce6b8;--red:#ff8b98;--txt:#f4fbff;--muted:#bed4e5;background:radial-gradient(circle at 50% -20%,#153f68,#07192d 70%);color:var(--txt);border:1px solid #2d638d;border-radius:22px;padding:14px;box-shadow:0 16px 44px rgba(0,0,0,.24);margin:14px 0;overflow:hidden}
 .nabil-sci-top{display:flex;gap:12px;align-items:center;justify-content:space-between;border-bottom:1px solid #2a5479;padding:2px 4px 11px;flex-wrap:wrap}
 .nabil-sci-brand{font-weight:900;color:var(--cyan);letter-spacing:.7px}.nabil-sci-badge{font-size:.75rem;border:1px solid #46789e;border-radius:999px;padding:4px 10px;color:#d8efff}
 .nabil-sci-title{margin:9px 0 2px;font-size:clamp(1.15rem,3vw,1.65rem);line-height:1.25}
 .nabil-sci-grid{display:grid;grid-template-columns:minmax(250px,.92fr) minmax(390px,1.55fr) minmax(190px,.64fr);gap:12px;margin-top:12px;align-items:stretch}
 .nabil-sci-panel{background:linear-gradient(160deg,#0f3151,#0a2239);border:1px solid var(--line);border-radius:17px;padding:13px;min-width:0}
 .nabil-sci-panel h3{margin:0 0 9px;color:#9eeeff;font-size:1rem}.nabil-sci-list{margin:0;padding:0 18px 0 0;line-height:1.65}.nabil-sci-list li{margin:5px 0}
 .nabil-sci-section{border-top:1px solid #284e6f;padding-top:9px;margin-top:9px}.nabil-sci-label{font-weight:800;color:#8fe8ff}.nabil-sci-value{color:#fff;white-space:pre-wrap;overflow-wrap:anywhere}
 .nabil-sci-visual{min-height:310px;display:flex;flex-direction:column;gap:10px}.nabil-sci-visual-stage{flex:1;display:grid;place-items:center;background:#061827;border:1px solid #274d6d;border-radius:14px;padding:10px;overflow:auto}
 .nabil-sci-visual-stage svg,.nabil-sci-visual-stage canvas,.nabil-sci-visual-stage img{display:block;max-width:100%;height:auto;max-height:480px}
 .nabil-sci-visual-note{color:var(--muted);font-size:.82rem}
 .nabil-sci-teacher{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:8px;min-height:100%}.nabil-sci-avatar{width:min(100%,180px);max-height:230px;object-fit:contain;filter:drop-shadow(0 12px 22px rgba(0,0,0,.25))}
 .nabil-sci-teacher strong{color:var(--cyan);font-size:1.05rem}.nabil-sci-teacher p{margin:0;color:#d7e9f6;line-height:1.5}
 .nabil-sci-final{margin-top:12px;background:linear-gradient(145deg,#0e3547,#0b2939);border:1px solid #3b8b8a;border-radius:16px;padding:12px}
 .nabil-sci-final h3{margin:0 0 7px;color:#8ff3d7}.nabil-sci-results{display:flex;gap:8px;flex-wrap:wrap}.nabil-sci-chip{border:1px solid #41769a;background:#0c2a45;border-radius:999px;padding:5px 9px;font-size:.84rem}
 .nabil-sci-verify{margin-top:9px;border-right:4px solid var(--green);background:#0d2d36;border-radius:9px;padding:9px 10px}
 .nabil-sci-table-wrap{overflow-x:auto;border-radius:11px;border:1px solid #315a79}.nabil-sci-table{width:100%;border-collapse:collapse;table-layout:fixed;min-width:620px;background:#081d31}
 .nabil-sci-table th,.nabil-sci-table td{border:1px solid #315a79;padding:8px 5px;text-align:center;vertical-align:middle;white-space:normal;word-break:normal}
 .nabil-sci-table th{width:92px;color:#9eeeff;background:#0c2943}.nabil-sci-table td{color:#f4fbff}.nabil-sci-critical{color:var(--gold)!important;font-weight:800}.nabil-sci-asym{color:var(--red)!important;font-weight:800}
 .nabil-sci-tools{display:flex;gap:7px;flex-wrap:wrap;margin-top:10px}.nabil-sci-tools button{border:1px solid #4d80a5;background:#123d60;color:white;border-radius:10px;padding:8px 11px;cursor:pointer;font:inherit}
 .nabil-sci-tools button:focus-visible{outline:3px solid #ffe084;outline-offset:2px}
 .nabil-sci-missing{color:#ffd7a0;border:1px dashed #84633d;padding:10px;border-radius:10px;text-align:center}
 @media(max-width:1080px){.nabil-sci-grid{grid-template-columns:minmax(250px,.9fr) minmax(360px,1.5fr)}.nabil-sci-teacher-panel{grid-column:1/-1}.nabil-sci-teacher{flex-direction:row;text-align:start;justify-content:flex-start}.nabil-sci-avatar{width:110px}}
 @media(max-width:760px){.nabil-sci-card{padding:10px;border-radius:16px}.nabil-sci-grid{grid-template-columns:1fr}.nabil-sci-panel{padding:11px}.nabil-sci-teacher-panel{grid-column:auto}.nabil-sci-teacher{flex-direction:row;text-align:start}.nabil-sci-avatar{width:84px;max-height:112px}.nabil-sci-visual{min-height:250px}.nabil-sci-table{min-width:560px;font-size:.86rem}}
 `;
 document.head.appendChild(s);
}

function detectKind(question="",subject="",spec={}){
 const declared=text(spec.kind||spec.card_type||subject).toLowerCase();
 const q=(text(question)+" "+declared).toLowerCase();
 if(/function|fonction|دال|domain|domaine|derivative|dériv|asympt|variation/.test(q))return "function_study";
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

function renderDrawing(d){
 try{
  if(typeof window.renderNabilDiagram==="function"){
   const html=window.renderNabilDiagram(d)||"";
   if(/<(?:svg|canvas|img)\b/i.test(html))return html;
  }
 }catch(_e){}
 return "";
}

function copyFor(spec={}){
 const raw=text(spec.language||spec.lang).toLowerCase();
 const lang=/^ar|arab|العرب/.test(raw)?"ar":/^fr|french|fran/.test(raw)?"fr":"en";
 if(lang==="ar")return {
   analysis:"📘 الاستدلال العلمي", functionAnalysis:"📘 دراسة الدالة",
   visual:"🧭 التمثيل العلمي", graph:"📈 الرسم وجدول التغيّرات",
   missing:"لم يُرفق بهذه البطاقة رسم موثّق.",
   teacher:"نفهم المعطيات، نختار القاعدة المناسبة، نحل خطوة خطوة، ثم نتحقق.",
   final:"✅ البطاقة النهائية", verification:"التحقق", enlarge:"🔎 تكبير الرسم",
   fallback:"راجع الاستدلال الموثّق أعلاه."
 };
 if(lang==="fr")return {
   analysis:"📘 Raisonnement scientifique", functionAnalysis:"📘 Étude de fonction",
   visual:"🧭 Représentation scientifique", graph:"📈 Courbe et variations",
   missing:"Aucun visuel vérifié n’a été fourni pour cette carte.",
   teacher:"On lit les données, on choisit la règle, on résout étape par étape, puis on vérifie.",
   final:"✅ Carte finale", verification:"Vérification", enlarge:"🔎 Agrandir le schéma",
   fallback:"Voir le raisonnement vérifié ci-dessus."
 };
 return {
   analysis:"📘 Scientific Reasoning", functionAnalysis:"📘 Function Analysis",
   visual:"🧭 Scientific Visual", graph:"📈 Graph & Variation",
   missing:"No verified visual was supplied for this card.",
   teacher:"We read the givens, choose the right rule, solve step by step, then verify.",
   final:"✅ Final Card", verification:"Verification", enlarge:"🔎 Enlarge visual",
   fallback:"See the verified reasoning above."
 };
}

function renderVisual(spec,copy){
 const drawings=arr(spec.drawings);
 const rendered=drawings.map(renderDrawing).filter(Boolean);
 if(rendered.length)return rendered.join("");
 if(text(spec.visual_html))return spec.visual_html;
 return '<div class="nabil-sci-missing">'+esc(copy.missing)+'</div>';
}

function renderVariationTable(table){
 if(!table||!Array.isArray(table.columns)||!Array.isArray(table.rows))return "";
 const cols=table.columns.map(text);
 if(!cols.length)return "";
 const colgroup='<colgroup><col style="width:92px">'+cols.map(()=>"<col>").join("")+"</colgroup>";
 const rows=table.rows.map(row=>{
   const cells=arr(row.cells);
   if(cells.length!==cols.length)return "";
   return '<tr><th>'+esc(row.label||"")+'</th>'+cells.map((v,i)=>{
    const cls=/asym|∞|parallel|\\|\\|/i.test(text(v))?"nabil-sci-asym":(/0|max|min|critical/i.test(text(v))?"nabil-sci-critical":"");
    return '<td class="'+cls+'">'+esc(v)+'</td>';
   }).join("")+"</tr>";
 }).join("");
 return '<div class="nabil-sci-table-wrap"><table class="nabil-sci-table">'+colgroup+
        '<tr><th>x</th>'+cols.map(c=>'<td>'+esc(c)+'</td>').join("")+'</tr>'+rows+'</table></div>';
}

function renderCard(spec={},target){
 ensureStyle();
 const copy=copyFor(spec);
 const host=typeof target==="string"?document.querySelector(target):target;
 if(!host)throw Error("NABIL Scientific Card target missing");
 const kind=detectKind(spec.title||"",spec.subject||"",spec);
 const sections=normalizeSections(spec);
 const verification=arr(spec.verification);
 const results=arr(spec.key_results||spec.final_results||spec.final_answer);
 const fs=spec.function_study||{};
 const card=document.createElement("section");
 card.className="nabil-sci-card";
 card.dataset.cardKind=kind;
 card.innerHTML=
 `<div class="nabil-sci-top">
   <div><div class="nabil-sci-brand">منصة نبيل التعليمية الذكية | NABIL AI</div>
   <h2 class="nabil-sci-title">${esc(spec.title||"Scientific Solution")}</h2></div>
   <div class="nabil-sci-badge">${esc(kind.replaceAll("_"," ").toUpperCase())}</div>
 </div>
 <div class="nabil-sci-grid">
   <div class="nabil-sci-panel nabil-sci-analysis">
     <h3>${kind==="function_study"?copy.functionAnalysis:copy.analysis}</h3>
     ${sections.map(s=>`<div class="nabil-sci-section"><div class="nabil-sci-label">${esc(s.label)}</div><ul class="nabil-sci-list">${s.items.map(v=>`<li>${esc(v)}</li>`).join("")}</ul></div>`).join("")}
   </div>
   <div class="nabil-sci-panel nabil-sci-visual">
     <h3>${kind==="function_study"?copy.graph:copy.visual}</h3>
     <div class="nabil-sci-visual-stage">${renderVisual(spec,copy)}</div>
     ${kind==="function_study"&&fs.variation_table?renderVariationTable(fs.variation_table):
       (kind==="function_study"&&text(fs.variation_text)?`<div class="nabil-sci-table-wrap"><div style="padding:10px;white-space:pre-wrap">${esc(fs.variation_text)}</div></div>`:"")}
     <div class="nabil-sci-visual-note">Only verified/source-backed drawings are rendered here.</div>
   </div>
   <div class="nabil-sci-panel nabil-sci-teacher-panel">
     <div class="nabil-sci-teacher">
       <img class="nabil-sci-avatar" src="${esc(spec.avatar_src||"/static/nabil-avatar-v3.png")}" alt="NABIL AI" onerror="this.style.display='none'">
       <div><strong>NABIL AI</strong><p>${esc(spec.teacher_note||copy.teacher)}</p></div>
     </div>
   </div>
 </div>
 <div class="nabil-sci-final">
   <h3>${esc(copy.final)}</h3>
   ${results.length?`<div class="nabil-sci-results">${results.map(v=>`<span class="nabil-sci-chip">${esc(v)}</span>`).join("")}</div>`:
     `<div class="nabil-sci-results"><span class="nabil-sci-chip">${esc(copy.fallback)}</span></div>`}
   ${verification.length?`<div class="nabil-sci-verify"><b>${esc(copy.verification)}:</b><ul class="nabil-sci-list">${verification.map(v=>`<li>${esc(v)}</li>`).join("")}</ul></div>`:""}
   <div class="nabil-sci-tools"><button type="button" data-nabil-enlarge>${esc(copy.enlarge)}</button></div>
 </div>`;
 host.replaceChildren(card);
 const enlarge=card.querySelector("[data-nabil-enlarge]");
 enlarge?.addEventListener("click",()=>{
   const stage=card.querySelector(".nabil-sci-visual-stage");
   if(!stage)return;
   const modal=document.getElementById("drawingPreviewModal");
   const content=document.getElementById("drawingPreviewContent");
   if(modal&&content){content.replaceChildren(stage.cloneNode(true));modal.hidden=false;return}
   if(stage.requestFullscreen)stage.requestFullscreen().catch(()=>{});
 });
 try{window.MathJax?.typesetPromise?.([card])}catch(_e){}
 return card;
}

function renderFromChat(arg={},legacyQuestion="",legacyTarget=null){
 let result={},question="",target=null;
 if(arg&&typeof arg==="object"&&("reply" in arg||"solution_card" in arg)&&!("result" in arg)){
   result=arg;question=legacyQuestion||"";target=legacyTarget;
 }else{
   result=arg?.result||{};question=arg?.question||"";target=arg?.target||null;
 }
 const spec=(result&&result.solution_card&&typeof result.solution_card==="object")
   ?Object.assign({},result.solution_card,{drawings:Array.isArray(result.drawings)?result.drawings:(result.solution_card.drawings||[])})
   :deriveSpecFromChat(result,question);
 return renderCard(spec,target);
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

window.NABILScientificCards={renderCard,renderFromChat,deriveSpecFromChat,hydrate,detectKind};
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",()=>hydrate(document),{once:true});
else hydrate(document);
})();
