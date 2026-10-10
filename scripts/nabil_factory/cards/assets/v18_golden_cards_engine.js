/* NABIL AI — Scientific Solution Cards E2E  (GOLDEN V18 layout)
 * Shared renderer for Root Chat and the General Exercises page.
 * Every card = Golden visual language:
 *   header strip -> [ Given/Study | Diagram panels (+calc) | NABIL AI teacher ] -> Final Card — Rule Summary -> toolbar
 * Function-study values/graph come from the deterministic backend card engine.
 * Optional spec fields (all backward compatible):
 *   subtitle, estimated_time, objectives, main_formula, left_title, goal,
 *   panels:[{title,icon,drawings,visual_html,calc:[..],note,table:true}],
 *   rule_summary, quick_check, teacher_note, avatar_src
 */
(()=>{
"use strict";

const STYLE_ID="nabil-scientific-solution-cards-e2e";
const esc=v=>String(v??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const arr=v=>Array.isArray(v)?v.filter(x=>x!==null&&x!==undefined&&String(x).trim()!==""):[];
const text=v=>String(v??"").trim();

function langOf(spec={}){
 const v=text(spec.language).toLowerCase();
 if(v==="fr"||v.includes("fran"))return "fr";
 if(v==="ar"||v.includes("عرب"))return "ar";
 return "en";
}
function labelsFor(spec={}){
 const l=langOf(spec);
 if(l==="fr")return {given:"Données",study:"Étude de la fonction",goal:"Objectif",visual:"Graphe et variations",final:"Carte finale — Résumé de la règle",verify:"Vérification",time:"Durée estimée",obj:"Objectifs d’apprentissage",teacher:"Votre assistant d’apprentissage",quick:"Vérification rapide",talk:"Parle-moi",stop:"Arrêter",copy:"Copier la conversation",word:"Exporter Word",wa:"Partager sur WhatsApp",prev:"Aperçu du dessin",dl:"Télécharger le dessin",ph:"Tapez votre réponse…",send:"Envoyer",missing:"Aucun visuel vérifié n’a été fourni.",vlabel:"Asymptote verticale",olabel:"Asymptote oblique"};
 if(l==="ar")return {given:"المعطيات",study:"دراسة الدالة",goal:"المطلوب",visual:"الرسم وجدول التغيّرات",final:"البطاقة النهائية — ملخص القاعدة",verify:"التحقق",time:"الوقت المقدّر",obj:"أهداف التعلّم",teacher:"مساعدك في التعلّم",quick:"تحقق سريع",talk:"تكلّم معي",stop:"إيقاف",copy:"نسخ المحادثة",word:"تصدير Word",wa:"مشاركة عبر واتساب",prev:"معاينة الرسم",dl:"تنزيل الرسم",ph:"اكتب إجابتك…",send:"إرسال",missing:"لم يصل رسم علمي موثّق لهذه البطاقة.",vlabel:"مستقيم مقارب عمودي",olabel:"مستقيم مقارب مائل"};
 return {given:"Given",study:"Study of the Function",goal:"Goal",visual:"Graph & Variation",final:"Final Card — Rule Summary",verify:"Verification",time:"Estimated time",obj:"Learning objectives",teacher:"Your Learning Assistant",quick:"Quick Check",talk:"Talk to Me",stop:"Stop",copy:"Copy Conversation",word:"Export Word",wa:"Share via WhatsApp",prev:"Preview Drawing",dl:"Download Drawing",ph:"Type your answer…",send:"Send",missing:"No verified visual was supplied for this card.",vlabel:"Vertical asymptote",olabel:"Oblique asymptote"};
}
function playbackLanguage(spec={}){
 const l=langOf(spec);
 return l==="fr"?"Français":l==="ar"?"العربية":"English";
}

const rich=v=>esc(v).replace(/\*\*(.+?)\*\*/g,"<b>$1</b>");
const SUBJECTS={
 math:{icon:"📈",cy:"#52d7ff",n:{en:"Mathematics",fr:"les mathématiques",ar:"الرياضيات"}},
 physics:{icon:"⚡",cy:"#4fd1ff",n:{en:"Physics",fr:"la physique",ar:"الفيزياء"}},
 chemistry:{icon:"⚗️",cy:"#6ff0b5",n:{en:"Chemistry",fr:"la chimie",ar:"الكيمياء"}},
 biology:{icon:"🧬",cy:"#a6e86a",n:{en:"Biology",fr:"la biologie",ar:"الأحياء"}},
 science:{icon:"🔬",cy:"#7fd0ff",n:{en:"Science",fr:"les sciences",ar:"العلوم"}}
};
function profileOf(kind,spec){
 const m={function_study:"math",mathematics:"math",physics:"physics",chemistry:"chemistry",biology:"biology",general_science:"science"};
 let key=m[kind];
 if(!key){const q=(text(spec.subject)+" "+kind).toLowerCase();key=/math|رياض/.test(q)?"math":/phys|فيز/.test(q)?"physics":/chem|كيم/.test(q)?"chemistry":/bio|أحياء|احياء/.test(q)?"biology":"science"}
 const P=SUBJECTS[key],l=langOf(spec),n=P.n[l];
 const bubble=l==="fr"?`Je suis là pour t’aider à comprendre ${n}. Pose-moi n’importe quelle question !`:l==="ar"?`أنا هنا لمساعدتك على فهم ${n}. اسألني أي سؤال في أي وقت!`:`I'm here to help you understand ${n}. Ask me any question, anytime!`;
 return {icon:P.icon,cy:P.cy,bubble};
}

function ensureStyle(){
 if(document.getElementById(STYLE_ID))return;
 const s=document.createElement("style");
 s.id=STYLE_ID;
 s.textContent=`
 .nabil-sci-card{--bg:#04142b;--panel:#08284d;--panel2:#061b38;--line:#1c63a8;--cy:#52d7ff;--gold:#ffd23f;--green:#22c55e;--red:#ff8b98;--txt:#eaf6ff;--muted:#a9c7de;background:linear-gradient(180deg,#051a36,#031025);color:var(--txt);border:1px solid #1b4f86;border-radius:18px;padding:12px;margin:14px 0;width:100%;box-sizing:border-box;overflow:hidden;font-family:system-ui,Segoe UI,Arial,sans-serif;box-shadow:0 16px 44px rgba(0,0,0,.3)}
 .nabil-sci-card *{box-sizing:border-box}
 .nabil-sci-math{direction:ltr;unicode-bidi:isolate;font-family:"Cambria Math","STIX Two Math","Times New Roman",serif}
 .nabil-sci-head{display:flex;align-items:center;gap:14px;background:linear-gradient(90deg,#072a52,#06203f);border:1px solid var(--line);border-radius:14px;padding:10px 14px;flex-wrap:wrap}
 .nabil-sci-head-ico{font-size:2rem;line-height:1}
 .nabil-sci-head-main{flex:1 1 260px;min-width:0}
 .nabil-sci-title{margin:0;font-size:clamp(1.15rem,2.6vw,1.6rem);font-weight:800;line-height:1.25;overflow-wrap:anywhere}
 .nabil-sci-sub{color:var(--muted);font-size:.9rem;margin-top:2px}
 .nabil-sci-meta{display:flex;gap:10px;align-items:center;border-inline-start:1px solid #24629a;padding-inline-start:14px;font-size:.82rem;max-width:300px}
 .nabil-sci-meta b{display:block;color:var(--cy);font-size:.9rem}.nabil-sci-meta span{color:var(--muted)}
 .nabil-sci-grid{display:grid;grid-template-columns:minmax(330px,1.02fr) minmax(0,2.15fr) minmax(215px,.72fr);gap:10px;margin-top:10px;align-items:stretch}
 .nabil-sci-panel{background:linear-gradient(170deg,var(--panel),var(--panel2));border:1px solid var(--line);border-radius:14px;padding:12px;min-width:0}
 .nabil-sci-bar{margin:0 0 10px;font-size:1.25rem;font-weight:800;color:var(--cy);border-inline-start:5px solid #29b6ff;padding-inline-start:10px;line-height:1.2}
 .nabil-sci-formula{border:1px solid #2a7bc0;background:#06213f;border-radius:10px;padding:14px 12px;text-align:center;font-size:1.7rem;margin-bottom:16px;white-space:nowrap;overflow:hidden;overflow-wrap:normal;word-break:normal;max-width:100%;line-height:1.25}
 .nabil-sci-rows{display:flex;flex-direction:column;gap:9px}.nabil-sci-row{display:flex;align-items:flex-start;gap:8px;min-width:0;flex-wrap:nowrap}.nabil-sci-row .nabil-sci-rlabel{flex:0 0 auto}.nabil-sci-row .nabil-sci-rval{flex:1 1 auto;min-width:0}.nabil-sci-row.stack{display:block}.nabil-sci-row.stack .nabil-sci-rval{margin-top:4px;padding-inline-start:0}
 .nabil-sci-rlabel{color:var(--cy);font-weight:800}.nabil-sci-rval{color:#fff;overflow-wrap:anywhere;line-height:1.5}.nabil-sci-rval div+div{margin-top:3px}
 .nabil-sci-goal{margin-top:12px;border:1px solid #1f8a8a;background:#07303a;border-radius:12px;padding:10px}
 .nabil-sci-goal b{color:#6ff0d0;display:block;margin-bottom:4px}
 .nabil-sci-center{display:grid;gap:10px;grid-template-columns:repeat(var(--cols,1),minmax(0,1fr));min-width:0}.nabil-sci-card.nabil-sci-long .nabil-sci-grid{grid-template-columns:minmax(0,2.2fr) minmax(215px,.72fr)}.nabil-sci-card.nabil-sci-long .nabil-sci-analysis{grid-column:1/-1}.nabil-sci-card.nabil-sci-long .nabil-sci-center{grid-column:1}.nabil-sci-card.nabil-sci-long .nabil-sci-teacher-panel{grid-column:2}.nabil-sci-card.nabil-sci-long .nabil-sci-rows{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px 18px}.nabil-sci-card.nabil-sci-long .nabil-sci-row{display:block;border:1px solid #1e5f92;background:#061f3d;border-radius:10px;padding:9px 10px}.nabil-sci-card.nabil-sci-long .nabil-sci-row .nabil-sci-rval{margin-top:4px}
 .nabil-sci-visual{display:flex;flex-direction:column;gap:10px}
 .nabil-sci-visual h3{margin:0;color:var(--cy);font-size:1.15rem;display:flex;gap:8px;align-items:center}
 .nabil-sci-stage{flex:1;display:grid;place-items:center;background:#051728;border:1px solid #1f5a90;border-radius:12px;padding:6px;overflow:auto;min-height:230px}
 .nabil-sci-stage svg,.nabil-sci-stage canvas,.nabil-sci-stage img{display:block;max-width:100%;height:auto;max-height:480px}
 .nabil-sci-calc{border:2px solid #1e86d8;background:#061f3d;border-radius:12px;padding:10px 12px}
 .nabil-sci-rfull{grid-column:1/-1;font-size:1.05rem;line-height:1.6}.nabil-sci-steps{margin:4px 0 0;padding-inline-start:22px;line-height:1.7}
 .nabil-sci-calc h4{margin:0 0 6px;color:var(--cy);font-size:1.05rem}.nabil-sci-calc p{margin:3px 0;font-size:1.02rem;overflow-wrap:anywhere}.nabil-sci-calc .note{color:var(--muted);font-size:.9rem;margin-top:6px}
 .nabil-sci-table-wrap{overflow-x:auto;border-radius:8px;border:1px solid #2a6aa5}
 .nabil-sci-table{width:100%;border-collapse:collapse;table-layout:fixed;min-width:560px;background:#061b36;direction:ltr}
 .nabil-sci-table th,.nabil-sci-table td{border:1px solid #2a6aa5;padding:7px 4px;text-align:center;vertical-align:middle;font-size:.88rem}
 .nabil-sci-table th{width:84px;color:#dff3ff;font-style:italic;background:#08284d}.nabil-sci-table .hx td{font-weight:700;background:#08284d}
 .nabil-sci-critical{color:var(--gold)!important;font-weight:800}.nabil-sci-asym{color:var(--red)!important;font-weight:800}
 .nabil-sci-arrow{font-size:1.5rem;line-height:1}.nabil-sci-dbar{display:inline-block;width:7px;height:2.1em;border-inline:2px solid #fff;vertical-align:middle}
 .nabil-sci-teacher-panel{display:flex;flex-direction:column;gap:8px;align-items:center;text-align:center}
 .nabil-sci-teacher-panel .tt{color:var(--cy);font-size:1.5rem;font-weight:900;line-height:1}.nabil-sci-teacher-panel .ts{color:#8fd8ff;font-size:.9rem}
 .nabil-sci-avatar{width:min(100%,170px);max-height:220px;object-fit:contain;filter:drop-shadow(0 10px 18px rgba(0,0,0,.35))}
 .nabil-sci-bubble{width:100%;border:1px solid #2a7bc0;background:#06213f;border-radius:10px;padding:8px 10px;font-size:.88rem;line-height:1.45}
 .nabil-sci-talk{width:100%;border:0;border-radius:10px;padding:11px;background:linear-gradient(#f13a45,#d81f2c);color:#fff;font:inherit;font-weight:800;font-size:1.1rem;cursor:pointer}
 .nabil-sci-stopv{border:0;background:none;color:#8fd8ff;cursor:pointer;font:inherit;font-size:.82rem;text-decoration:underline}
 .nabil-sci-quick{width:100%;border:2px solid #b98a00;background:#2a2210;border-radius:10px;padding:8px 10px;text-align:start}
 .nabil-sci-quick b{color:var(--gold);display:block;margin-bottom:3px}.nabil-sci-quick span{font-size:.9rem}
 .nabil-sci-final{margin-top:10px;display:flex;gap:14px;align-items:center;flex-wrap:wrap;border:2px solid var(--green);background:linear-gradient(90deg,#06304a,#073b34);border-radius:12px;padding:10px 14px}
 .nabil-sci-final-t{color:#8ff3b8;font-weight:800;font-size:1.05rem;white-space:nowrap}
 .nabil-sci-final-b{flex:1 1 280px;min-width:0;border-inline-start:1px solid #3a8f78;padding-inline-start:14px;overflow-wrap:anywhere;line-height:1.5}
 .nabil-sci-final-b .chips{display:flex;gap:6px;flex-wrap:wrap;margin-top:6px}.nabil-sci-chip{border:1px solid #3d8d8a;background:#0a2f3c;border-radius:999px;padding:3px 10px;font-size:.84rem}
 .nabil-sci-final-b .ver{margin-top:6px;color:#bfe9d6;font-size:.86rem}
 .nabil-sci-tools{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px;align-items:stretch}
 .nabil-sci-tools button{border:1px solid rgba(255,255,255,.18);color:#fff;border-radius:9px;padding:9px 13px;cursor:pointer;font:inherit;font-weight:600;background:#0f3c73}
 .nabil-sci-tools .wa{background:#19a35a}.nabil-sci-tools .pv{background:#5b2fd1}.nabil-sci-tools .dl{background:#1673d6}.nabil-sci-tools .sd{background:#1e6fe8;min-width:90px}
 .nabil-sci-tools input{flex:1 1 160px;min-width:0;border:1px solid #1f5a90;background:#06213f;color:#fff;border-radius:9px;padding:9px 12px;font:inherit}
 .nabil-sci-card button:focus-visible,.nabil-sci-card input:focus-visible{outline:3px solid #ffe084;outline-offset:2px}
 .nabil-sci-missing{color:#ffd7a0;border:1px dashed #84633d;padding:10px;border-radius:10px;text-align:center}
 .nabil-general-scientific-host{width:100%;max-width:100%;box-sizing:border-box}
 @media(max-width:1080px){.nabil-sci-grid{grid-template-columns:minmax(260px,.9fr) minmax(0,1.8fr)}.nabil-sci-teacher-panel{grid-column:1/-1;flex-direction:row;flex-wrap:wrap;justify-content:center}.nabil-sci-teacher-panel .nabil-sci-avatar{width:110px}}
 @media(max-width:760px){.nabil-sci-card.nabil-sci-long .nabil-sci-grid{grid-template-columns:1fr}.nabil-sci-card.nabil-sci-long .nabil-sci-analysis,.nabil-sci-card.nabil-sci-long .nabil-sci-center,.nabil-sci-card.nabil-sci-long .nabil-sci-teacher-panel{grid-column:auto}.nabil-sci-card.nabil-sci-long .nabil-sci-rows{grid-template-columns:1fr}.nabil-sci-row{display:block}.nabil-sci-row .nabil-sci-rval{margin-top:4px}.nabil-sci-formula{font-size:1.12rem}.nabil-sci-card{padding:9px;border-radius:14px}.nabil-sci-grid{grid-template-columns:1fr}.nabil-sci-center{grid-template-columns:1fr}.nabil-sci-teacher-panel{grid-column:auto}.nabil-sci-meta{border:0;padding:0;max-width:none}.nabil-sci-final-b{border:0;padding:0}.nabil-sci-tools button{flex:1 1 44%}}
 `;
 document.head.appendChild(s);
}

function detectKind(question="",subject="",spec={}){
 const declared=text(spec.kind||spec.card_type||subject).toLowerCase();
 const k0=text(spec.kind).toLowerCase();
 if(["function_study","physics","chemistry","biology","general_science","mathematics"].includes(k0))return k0;
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
   .filter(x=>x&&arr(x.items).length)
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

/* ---------- Coordinate plane (golden style: ticks, legend, labelled markers) ---------- */
function svgCoordinatePlane(d,labels={}){
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
 const nice=r=>{const e=Math.pow(10,Math.floor(Math.log10(r))),m=r/e;return (m<1.5?1:m<3.5?2:m<7.5?5:10)*e};
 const fmt=n=>String(+n.toFixed(4)).replace("-","−");
 let body=`<rect width="${W}" height="${H}" rx="14" fill="#051728"/>`;
 for(let i=1;i<10;i++){
   const gx=L+w*i/10,gy=T+h*i/10;
   body+=`<line x1="${f(gx)}" x2="${f(gx)}" y1="${T}" y2="${T+h}" stroke="#12385a" stroke-width="1"/>`;
   body+=`<line x1="${L}" x2="${L+w}" y1="${f(gy)}" y2="${f(gy)}" stroke="#12385a" stroke-width="1"/>`;
 }
 const x0in=xmin<=0&&xmax>=0,y0in=ymin<=0&&ymax>=0;
 if(x0in)body+=`<line x1="${f(px(0))}" x2="${f(px(0))}" y1="${T}" y2="${T+h}" stroke="#e8f4ff" stroke-width="1.8"/>`;
 if(y0in)body+=`<line x1="${L}" x2="${L+w}" y1="${f(py(0))}" y2="${f(py(0))}" stroke="#e8f4ff" stroke-width="1.8"/>`;
 const sx=nice((xmax-xmin)/9),sy=nice((ymax-ymin)/9);
 for(let v=Math.ceil(xmin/sx)*sx;v<=xmax+1e-9;v+=sx){
   if(Math.abs(v)<1e-9)continue;
   body+=`<text x="${f(px(v))}" y="${f(y0in?Math.min(py(0)+17,T+h-4):T+h+18)}" fill="#cfe8f7" font-size="13" text-anchor="middle">${fmt(v)}</text>`;
 }
 for(let v=Math.ceil(ymin/sy)*sy;v<=ymax+1e-9;v+=sy){
   if(Math.abs(v)<1e-9)continue;
   body+=`<text x="${f(x0in?Math.max(px(0)-7,L+14):L-8)}" y="${f(py(v)+4)}" fill="#cfe8f7" font-size="13" text-anchor="end">${fmt(v)}</text>`;
 }
 const legend=[];
 legend.push({c:"#39c9ff",dash:"",t:text(d.curve_label)||"f(x)"});
 (d.vertical_asymptotes||[]).forEach(a=>{
   const x=Number(a?.x??a);if(!Number.isFinite(x)||x<xmin||x>xmax)return;
   const lab=a?.label||("x = "+fmt(x));
   body+=`<line x1="${f(px(x))}" x2="${f(px(x))}" y1="${T}" y2="${T+h}" stroke="#ff5b6b" stroke-width="2.2" stroke-dasharray="9 7"/>`;
   body+=`<text x="${f(px(x)+6)}" y="${T+h-8}" fill="#ff9aa5" font-size="13">${esc(lab)}</text>`;
   if(!legend.some(l=>l.k==="v"))legend.push({k:"v",c:"#ff5b6b",dash:"6 4",t:(labels.vlabel||"Vertical asymptote")+": "+lab});
 });
 (d.oblique_asymptotes||[]).forEach(a=>{
   const m=Number(a?.m),b=Number(a?.b);if(!Number.isFinite(m)||!Number.isFinite(b))return;
   const y1=m*xmin+b,y2=m*xmax+b;
   const lab=a?.label||("y = "+fmt(m)+"x "+(b<0?"−":"+")+" "+fmt(Math.abs(b)));
   body+=`<line x1="${L}" x2="${L+w}" y1="${f(py(y1))}" y2="${f(py(y2))}" stroke="#ffe14d" stroke-width="2.2" stroke-dasharray="9 7"/>`;
   legend.push({c:"#ffe14d",dash:"6 4",t:(labels.olabel||"Oblique asymptote")+": "+lab});
 });
 series.forEach((part,index)=>{
   const pts=part.filter(v=>Array.isArray(v)&&v.length>=2&&Number.isFinite(Number(v[0]))&&Number.isFinite(Number(v[1])))
     .filter(v=>Number(v[0])>=xmin&&Number(v[0])<=xmax&&Number(v[1])>=ymin&&Number(v[1])<=ymax);
   if(pts.length<2)return;
   const p=pts.map(v=>f(px(v[0]))+","+f(py(v[1]))).join(" ");
   body+=`<polyline points="${p}" fill="none" stroke="#39c9ff" stroke-width="3.2" stroke-linejoin="round" stroke-linecap="round"/>`;
 });
 (d.markers||[]).forEach(pt=>{
   const x=Number(pt.x),y=Number(pt.y);if(!Number.isFinite(x)||!Number.isFinite(y)||x<xmin||x>xmax||y<ymin||y>ymax)return;
   const cx=f(px(x)),cy=f(py(y));
   body+=`<circle cx="${cx}" cy="${cy}" r="5.5" fill="#fff" stroke="#39c9ff" stroke-width="2.5"/>`;
   const anchor=px(x)>W-150?"end":"start",dx=anchor==="end"?-9:9;
   body+=`<text x="${f(px(x)+dx)}" y="${f(py(y)-22)}" fill="#fff" font-size="13" text-anchor="${anchor}">(${fmt(x)}, ${fmt(y)})</text>`;
   if(pt.label)body+=`<text x="${f(px(x)+dx)}" y="${f(py(y)-8)}" fill="#7fe0ff" font-size="12" text-anchor="${anchor}">${esc(pt.label)}</text>`;
 });
 body+=`<text x="${W-14}" y="${f((y0in?py(0):T+h)-8)}" fill="#e8f4ff" font-size="15" font-style="italic" text-anchor="end">x</text>`;
 body+=`<text x="${f((x0in?px(0):L)+8)}" y="${T+14}" fill="#e8f4ff" font-size="15" font-style="italic">y</text>`;
 const lw=Math.min(300,Math.max(...legend.map(l=>l.t.length))*7.2+64),lh=legend.length*24+10,lx=W-R-lw-6,ly=T+6;
 body+=`<rect x="${f(lx)}" y="${ly}" width="${f(lw)}" height="${lh}" rx="8" fill="#061b36" fill-opacity=".94" stroke="#2a7bc0"/>`;
 legend.forEach((l,i)=>{
   const yy=ly+22+i*24;
   body+=`<line x1="${f(lx+10)}" x2="${f(lx+44)}" y1="${yy-4}" y2="${yy-4}" stroke="${l.c}" stroke-width="2.6"${l.dash?` stroke-dasharray="${l.dash}"`:""}/>`;
   body+=`<text x="${f(lx+52)}" y="${yy}" fill="#eaf6ff" font-size="13">${esc(l.t)}</text>`;
 });
 return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(d.title||"Function graph")}">${body}</svg>`;
}


function svgCircuit(d){
 const kind=text(d?.type||"").toLowerCase();
 const topology=text(d?.topology||d?.mode||"").toLowerCase();
 const isSeries=/series/.test(kind+" "+topology);
 const isParallel=/parallel/.test(kind+" "+topology);
 if(!isSeries&&!isParallel)return "";
 const U=text(d.voltage||d.U||"6 V");
 const R1=text(d.r1||d.R1||"6 Ω");
 const R2=text(d.r2||d.R2||"3 Ω");
 const I=text(d.current||d.I||"");
 const I1=text(d.i1||d.I1||"");
 const I2=text(d.i2||d.I2||"");
 const W=720,H=330;
 const line=(x1,y1,x2,y2,c="#dff6ff",w=4)=>`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${w}" stroke-linecap="round"/>`;
 const txt=(x,y,s,c="#eaf6ff",size=22,anchor="middle")=>`<text x="${x}" y="${y}" fill="${c}" font-size="${size}" font-family="Segoe UI,Arial,sans-serif" text-anchor="${anchor}">${esc(s)}</text>`;
 const zig=(x1,y,x2,c)=>{let p=`${x1},${y}`;const n=8,dx=(x2-x1)/n;for(let k=1;k<n;k++)p+=` ${x1+k*dx},${y+(k%2?-18:18)}`;p+=` ${x2},${y}`;return `<polyline points="${p}" fill="none" stroke="${c}" stroke-width="5" stroke-linejoin="round"/>`;};
 let b="";
 // Battery + left/right rails
 b+=line(70,100,70,255); b+=line(70,255,650,255); b+=line(650,255,650,100);
 b+=line(48,205,92,205,"#ff6574",5); b+=line(56,222,84,222,"#61bfff",3);
 b+=txt(110,220,`U = ${U}`,"#ffd166",20,"start");
 if(isSeries){
   b+=line(70,100,145,100);
   b+=`<circle cx="170" cy="100" r="22" fill="#08284d" stroke="#6fe8ff" stroke-width="4"/>${txt(170,108,"A","#dffaff",20)}`;
   b+=line(192,100,250,100);
   b+=zig(250,100,365,"#ec8cff"); b+=txt(307,145,`R₁ = ${R1}`,"#f5a4ff",18);
   b+=line(365,100,420,100);
   b+=zig(420,100,535,"#8df06d"); b+=txt(477,145,`R₂ = ${R2}`,"#a9ff8f",18);
   b+=line(535,100,650,100);
   if(I){ b+=line(315,64,430,64,"#56e2ff",4); b+=`<polygon points="430,64 416,56 416,72" fill="#56e2ff"/>`; b+=txt(372,50,`I = ${I}`,"#69edff",19); }
   b+=txt(360,305,"Series connection","#76e6ff",22);
 }else{
   b+=line(70,100,180,100); b+=line(180,100,650,100);
   b+=line(250,100,250,205); b+=line(540,100,540,205);
   b+=line(250,150,330,150); b+=zig(330,150,455,"#ec8cff"); b+=line(455,150,540,150);
   b+=line(250,205,330,205); b+=zig(330,205,455,"#8df06d"); b+=line(455,205,540,205);
   b+=txt(392,135,`R₁ = ${R1}`,"#f5a4ff",18);
   b+=txt(392,240,`R₂ = ${R2}`,"#a9ff8f",18);
   if(I1){ b+=line(350,125,455,125,"#56e2ff",4); b+=`<polygon points="455,125 441,117 441,133" fill="#56e2ff"/>`; b+=txt(402,112,`I₁ = ${I1}`,"#69edff",18); }
   if(I2){ b+=line(350,180,455,180,"#56e2ff",4); b+=`<polygon points="455,180 441,172 441,188" fill="#56e2ff"/>`; b+=txt(402,168,`I₂ = ${I2}`,"#69edff",18); }
   b+=txt(360,305,"Parallel connection","#76e6ff",22);
 }
 return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" role="img" aria-label="${isSeries?"Series":"Parallel"} resistor circuit">${b}</svg>`;
}

function renderDrawing(d,labels){
 try{
  if(typeof window.renderNabilDiagram==="function"){
   const html=window.renderNabilDiagram(d)||"";
   if(/<(?:svg|canvas|img)\b/i.test(html))return html;
  }
 }catch(_e){}
 const circuit=svgCircuit(d);
 if(circuit)return circuit;
 return svgCoordinatePlane(d,labels);
}

function renderVisual(p,spec){
 const L=labelsFor(spec);
 const rendered=arr(p.drawings).map(d=>renderDrawing(d,L)).filter(Boolean);
 if(rendered.length)return rendered.join("");
 if(text(p.visual_html))return p.visual_html;
 return `<div class="nabil-sci-missing">${esc(L.missing)}</div>`;
}

function renderVariationTable(table){
 if(!table||!Array.isArray(table.columns)||!Array.isArray(table.rows))return "";
 const cols=table.columns.map(text);
 if(!cols.length)return "";
 const cell=v=>{
   const t=text(v);
   if(t==="∥"||t==="||")return '<td><span class="nabil-sci-dbar"></span></td>';
   const cls=/^[↗↘↑↓→↔]$/.test(t)?"nabil-sci-arrow":/asym|∞|parallel/i.test(t)?"nabil-sci-asym":(t==="0"||/max|min|critical/i.test(t)?"nabil-sci-critical":"");
   return '<td class="'+cls+'">'+esc(t)+'</td>';
 };
 const colgroup='<colgroup><col style="width:84px">'+cols.map(()=>"<col>").join("")+"</colgroup>";
 const rows=table.rows.map(row=>{
   const cells=Array.isArray(row.cells)?row.cells.map(text):[];
   if(cells.length!==cols.length)return "";
   return '<tr><th>'+esc(row.label||"")+'</th>'+cells.map(cell).join("")+"</tr>";
 }).join("");
 return '<div class="nabil-sci-table-wrap"><table class="nabil-sci-table">'+colgroup+
        '<tr class="hx"><th>x</th>'+cols.map(c=>'<td>'+esc(c)+'</td>').join("")+'</tr>'+rows+'</table></div>';
}

function ruleSummaryOf(spec){
 return text(spec.rule_summary);
}

function speechTextFromSpec(spec={}){
 const sections=normalizeSections(spec);
 const results=arr(spec.key_results||spec.final_results||spec.final_answer);
 const verification=arr(spec.verification);
 const parts=[text(spec.title)];
 sections.forEach(s=>{parts.push(text(s.label));s.items.forEach(v=>parts.push(text(v)))});
 arr(spec.panels).forEach(p=>{parts.push(text(p.title));arr(p.calc).forEach(v=>parts.push(text(v)));parts.push(text(p.note))});
 if(text(spec.teacher_note))parts.push(text(spec.teacher_note));
 if(ruleSummaryOf(spec))parts.push(ruleSummaryOf(spec));
 results.forEach(v=>parts.push(text(v)));
 verification.forEach(v=>parts.push(text(v)));
 return parts.filter(Boolean).join(". ").replace(/\s+/g," ").trim();
}

function download(name,blob){
 const a=document.createElement("a");
 a.href=URL.createObjectURL(blob);a.download=name;
 document.body.appendChild(a);a.click();a.remove();
 setTimeout(()=>URL.revokeObjectURL(a.href),4000);
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
 const isFn=kind==="function_study";
 const panels=Array.isArray(spec.panels)&&spec.panels.length?spec.panels:[{title:L.visual,drawings:spec.drawings,visual_html:spec.visual_html,table:isFn}];
 const formula=text(spec.main_formula||fs.expression);
 const goal=text(spec.goal);
 const rule=ruleSummaryOf(spec);
 const sub=profileOf(kind,spec);
 const bubble=text(spec.teacher_note)||sub.bubble;
 const hasVisual=p=>arr(p.drawings).length||text(p.visual_html);
 const hasBody=p=>arr(p.calc).length||arr(p.steps).length||text(p.text);
 const avatar=spec.avatar_src||window.NABIL_AVATAR_SRC||"/static/nabil-avatar.png";
 const sectionChars=sections.reduce((n,s)=>n+text(s.label).length+s.items.reduce((m,v)=>m+text(v).length,0),0);
 const panelChars=panels.reduce((n,p)=>n+text(p.title).length+text(p.text).length+text(p.note).length+arr(p.calc).join(" ").length+arr(p.steps).join(" ").length,0);
 const explicitLayout=text(spec.layout_mode||spec.layout);
 const longLayout=explicitLayout==="long"||spec.long_layout===true||
   (explicitLayout!=="compact"&&(sectionChars>520||panelChars>900||sections.length>7||
    sections.some(s=>s.items.join(" ").length>150)||panels.length>3));
 const card=document.createElement("section");
 card.className="nabil-sci-card"+(longLayout?" nabil-sci-long":"");
 card.dataset.cardKind=kind;
 card.dataset.layoutMode=longLayout?"long":"compact";
 card.dir=rtl?"rtl":"ltr";
 card.lang=langOf(spec);
 card.style.setProperty("--cy",sub.cy);
 const calcBox=p=>{
   const calc=arr(p.calc),steps=arr(p.steps);
   if(!calc.length&&!steps.length&&!text(p.note)&&!text(p.text))return "";
   return `<div class="nabil-sci-calc">${text(p.calc_title)?`<h4>🧮 ${esc(p.calc_title)}</h4>`:""}${text(p.text)?`<p>${rich(p.text)}</p>`:""}${calc.map(v=>`<p class="nabil-sci-math">${esc(v)}</p>`).join("")}${steps.length?`<ol class="nabil-sci-steps">${steps.map(v=>`<li>${rich(v)}</li>`).join("")}</ol>`:""}${text(p.note)?`<div class="note">${esc(p.note)}</div>`:""}</div>`;
 };
 card.innerHTML=
 `<div class="nabil-sci-head">
   <div class="nabil-sci-head-ico">📖</div>
   <div class="nabil-sci-head-main"><h2 class="nabil-sci-title">${esc(spec.title||"Scientific Solution")}</h2>${text(spec.subtitle)?`<div class="nabil-sci-sub">${esc(spec.subtitle)}</div>`:""}</div>
   ${text(spec.estimated_time)?`<div class="nabil-sci-meta"><span>🕒</span><div><span>${esc(L.time)}</span><b>${esc(spec.estimated_time)}</b></div></div>`:""}
   ${text(spec.objectives)?`<div class="nabil-sci-meta"><span>🎯</span><div><span>${esc(L.obj)}</span><b>${esc(spec.objectives)}</b></div></div>`:""}
 </div>
 <div class="nabil-sci-grid">
   <div class="nabil-sci-panel nabil-sci-analysis">
     <h3 class="nabil-sci-bar">${esc(spec.left_title||(isFn?L.study:L.given))}</h3>
     ${formula?`<div class="nabil-sci-formula nabil-sci-math">${esc(formula)}</div>`:""}
     <div class="nabil-sci-rows">${sections.map(s=>{
       if(!text(s.label))return `<div class="nabil-sci-rfull nabil-sci-math">${s.items.map(v=>`<div>${esc(v)}</div>`).join("")}</div>`;
       const joined=s.items.join(" ");
       const stack=(text(s.label).length>19||joined.length>56)?" stack":"";
       return `<div class="nabil-sci-row${stack}"><div class="nabil-sci-rlabel">${esc(s.label)}</div><div class="nabil-sci-rval nabil-sci-math">${s.items.map(v=>`<div>${esc(v)}</div>`).join("")}</div></div>`;
     }).join("")}</div>
     ${goal?`<div class="nabil-sci-goal"><b>🎯 ${esc(L.goal)}</b>${esc(goal)}</div>`:""}
   </div>
   <div class="nabil-sci-center" style="--cols:${panels.length}">
     ${panels.map(p=>`<div class="nabil-sci-panel nabil-sci-visual">
       <h3>${esc(p.icon||sub.icon)} ${esc(p.title||L.visual)}</h3>
       ${hasVisual(p)||!hasBody(p)?`<div class="nabil-sci-stage">${renderVisual(p,spec)}</div>`:""}
       ${p.table&&isFn?(fs.variation_table?renderVariationTable(fs.variation_table):(text(fs.variation_text)?`<div class="nabil-sci-table-wrap"><div style="padding:10px;white-space:pre-wrap">${esc(fs.variation_text)}</div></div>`:"")):""}
       ${calcBox(p)}
     </div>`).join("")}
   </div>
   <div class="nabil-sci-panel nabil-sci-teacher-panel">
     <div class="tt">NABIL AI</div><div class="ts">${esc(L.teacher)}</div>
     <img class="nabil-sci-avatar" src="${esc(avatar)}" alt="NABIL AI" onerror="this.style.display='none'">
     <div class="nabil-sci-bubble">${esc(bubble)}</div>
     <button type="button" class="nabil-sci-talk" data-nabil-read>🎙 ${esc(L.talk)}</button>
     <button type="button" class="nabil-sci-stopv" data-nabil-stop>⏹ ${esc(L.stop)}</button>
     ${text(spec.quick_check)?`<div class="nabil-sci-quick"><b>❓ ${esc(L.quick)}</b><span>${esc(spec.quick_check)}</span></div>`:""}
   </div>
 </div>
 <div class="nabil-sci-final">
   <div class="nabil-sci-final-t">💡 ${esc(L.final)}</div>
   <div class="nabil-sci-final-b">
     ${rule?`<div>${rich(rule)}</div>`:""}
     ${results.length?`<div class="chips">${results.map(v=>`<span class="nabil-sci-chip nabil-sci-math">${esc(v)}</span>`).join("")}</div>`:""}
     ${verification.length?`<div class="ver"><b>${esc(L.verify)}:</b> ${verification.map(esc).join(" • ")}</div>`:""}
   </div>
 </div>
 <div class="nabil-sci-tools">
   <button type="button" data-nabil-copy>📋 ${esc(L.copy)}</button>
   <button type="button" data-nabil-word>📄 ${esc(L.word)}</button>
   <button type="button" class="wa" data-nabil-wa>💬 ${esc(L.wa)}</button>
   <button type="button" class="pv" data-nabil-enlarge>🖼 ${esc(L.prev)}</button>
   <button type="button" class="dl" data-nabil-dl>⬇ ${esc(L.dl)}</button>
   <input type="text" data-nabil-answer placeholder="${esc(L.ph)}" aria-label="${esc(L.ph)}">
   <button type="button" class="sd" data-nabil-send>➤ ${esc(L.send)}</button>
 </div>`;
 host.replaceChildren(card);
 const spoken=speechTextFromSpec(spec);
 card.dataset.nabilSpeechText=spoken;
 card.dataset.nabilSpeechLanguage=playbackLanguage(spec);
 const on=(sel,fn)=>card.querySelector(sel)?.addEventListener("click",fn);
 const stage=()=>card.querySelector(".nabil-sci-stage");

 on("[data-nabil-enlarge]",()=>{
   const st=stage();if(!st)return;
   const modal=document.getElementById("drawingPreviewModal");
   const content=document.getElementById("drawingPreviewContent");
   if(modal&&content){content.replaceChildren(st.cloneNode(true));modal.hidden=false;return}
   if(st.requestFullscreen)st.requestFullscreen().catch(()=>{});
 });
 on("[data-nabil-read]",()=>speakCard(card));
 on("[data-nabil-stop]",()=>{try{window.stopNabilNeuralVoice?.();window.speechSynthesis?.cancel?.()}catch(_e){}});
 on("[data-nabil-copy]",()=>{
   try{navigator.clipboard.writeText(spoken)}catch(_e){
     const t=document.createElement("textarea");t.value=spoken;document.body.appendChild(t);t.select();document.execCommand("copy");t.remove();
   }
 });
 on("[data-nabil-word]",()=>{
   if(typeof window.nabilExportWord==="function"){try{return window.nabilExportWord(spec,spoken)}catch(_e){}}
   const html=`<html dir="${rtl?"rtl":"ltr"}"><head><meta charset="utf-8"></head><body><h1>${esc(spec.title||"")}</h1>${sections.map(s=>`<h3>${esc(s.label)}</h3>${s.items.map(v=>`<p>${esc(v)}</p>`).join("")}`).join("")}${rule?`<h3>${esc(L.final)}</h3><p>${esc(rule)}</p>`:""}${results.map(v=>`<p><b>${esc(v)}</b></p>`).join("")}</body></html>`;
   download("nabil-solution.doc",new Blob(["\ufeff"+html],{type:"application/msword"}));
 });
 on("[data-nabil-wa]",()=>window.open("https://wa.me/?text="+encodeURIComponent(spoken.slice(0,1500)),"_blank","noopener"));
 on("[data-nabil-dl]",()=>{
   const st=stage();if(!st)return;
   const svg=st.querySelector("svg"),cv=st.querySelector("canvas");
   if(svg){
     const x=new XMLSerializer().serializeToString(svg);
     download("nabil-drawing.svg",new Blob([x.includes("xmlns=")?x:x.replace("<svg",'<svg xmlns="http://www.w3.org/2000/svg"')],{type:"image/svg+xml"}));
   }else if(cv){cv.toBlob(b=>b&&download("nabil-drawing.png",b))}
 });
 const input=card.querySelector("[data-nabil-answer]");
 const send=()=>{
   const answer=text(input?.value);if(!answer)return;
   card.dispatchEvent(new CustomEvent("nabil-card-answer",{bubbles:true,detail:{answer,spec}}));
   try{window.nabilSendAnswer?.(answer,spec)}catch(_e){}
   input.value="";
 };
 on("[data-nabil-send]",send);
 input?.addEventListener("keydown",e=>{if(e.key==="Enter")send()});
 
 const fitFormula=()=>{
   const el=card.querySelector(".nabil-sci-formula");
   if(!el)return;
   let size=27.2;
   el.style.fontSize=size+"px";
   while(el.scrollWidth>el.clientWidth-4 && size>17){
     size-=0.5; el.style.fontSize=size+"px";
   }
 };
 fitFormula();
 try{new ResizeObserver(fitFormula).observe(card.querySelector(".nabil-sci-analysis"))}catch(_e){}
 try{window.MathJax?.typesetPromise?.([card]).then(fitFormula)}catch(_e){}
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
 try{window.stopNabilNeuralVoice?.();window.speechSynthesis?.cancel?.()}catch(_e){}
 const fn=window.__nabilScientificNativeSpeak||window.nabilSpeakClear;
 if(typeof fn==="function"){
   try{return Promise.resolve(fn(spoken,language,{nabilScientificCard:true})).catch(()=>{})}catch(_e){}
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
 * General Exercises integration (unchanged behaviour)
 * When the backend returns solution_card, replace the legacy teacher bubble
 * with this one canonical golden card.
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
           window.setTimeout(()=>{
             const panel=document.getElementById("nv132Result");
             if(panel&&!panel.hidden){
               const panelHost=document.createElement("div");
               panelHost.className="nabil-general-scientific-panel-host";
               panel.replaceChildren(panelHost);
               try{renderFromChat(data,question,panelHost)}catch(_e){}
             }
           },220);
           window.__nabilScientificGeneralPending=false;
           try{window.stopNabilNeuralVoice?.();window.speechSynthesis?.cancel?.()}catch(_e){}
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

/* Any lesson, any subject: pass a plain lesson object; aliases are mapped to the card spec. */
function fromLesson(l={},target){
 const spec=Object.assign({},l);
 spec.estimated_time=l.estimated_time||l.time;
 spec.objectives=l.objectives||l.objective;
 spec.rule_summary=l.rule_summary||l.rule;
 spec.kind=l.kind||l.subject;
 spec.layout_mode=l.layout_mode||l.layout;
 if(l.long_layout===true)spec.long_layout=true;
 if(!Array.isArray(l.sections)){const g=arr(l.given||l.givens);spec.sections=g.length?[{label:"",items:g.map(text)}]:[]}
 return target?renderCard(spec,target):spec;
}

window.NABILScientificCards={fromLesson,
 renderCard,renderFromChat,deriveSpecFromChat,hydrate,detectKind,
 speechTextFromSpec,speakCard,resultSpec
};
installGeneralExercisesBridge();
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",()=>hydrate(document),{once:true});
else hydrate(document);
})();
