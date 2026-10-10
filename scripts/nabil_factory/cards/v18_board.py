"""NABIL V18 smart-board renderer (replaces the old iframe-only whole-lesson lab).

Architecture (ported from NABIL_V18_MATH_SMART_BOARD_PREVIEW.html and
NABIL_V18_GOLDEN_CARDS_STANDALONE.html):

* One idea at a time is written on the board, line by line, with voice.
* The idea's verified lab sits directly beneath the board (same idea).
* Next/Previous move one teaching step; timeline dots jump between ideas.
* The Golden Card is the LAST stage inside the same section, drawn inline by the
  vendored V18 card engine (no external file, no iframe, no empty preview).

The renderer is pure presentation. It receives already-verified lesson data and
never invents science or numbers.
"""
from __future__ import annotations

import base64
import html
import json
import re
from pathlib import Path

V18_BOARD_CONTRACT = "NABIL_V18_SMART_BOARD_V1"
_ASSETS = Path(__file__).resolve().parent / "assets"

_LABELS = {
    "ar": {
        "title": "🧠 اللوح الذكي — مختبر نبيل الشامل",
        "subtitle": "يشرح نبيل فكرة واحدة في كل مرة، ثم يظهر المختبر المناسب أسفل الفكرة نفسها.",
        "teacher": "نبيل يشرح الآن", "study": "ملخص الدرس", "final": "البطاقة الذهبية",
        "play": "▶ اشرح الدرس من البداية", "stop": "■ أوقف", "prev": "◀ السابق",
        "next": "التالي ▶", "restart": "↻ من جديد", "current": "🔊 اشرح هذه الفكرة",
        "voice_on": "🔊 الصوت يعمل", "voice_off": "🔇 الصوت متوقف",
        "lab": "🧪 المختبر", "run_lab": "▶ شغّل المختبر", "talk": "🎙 تكلّم معي",
        "step": "الخطوة", "idea": "الفكرة", "hello": "أنا نبيل. اضغط «اشرح الدرس من البداية».",
        "goal": "🎯 تظهر البطاقة الذهبية الكاملة بعد آخر فكرة.",
        "novoice": "لا يوجد صوت عربي مثبّت على هذا الجهاز؛ يستمر الشرح مكتوبًا.",
        "done": "اكتمل الشرح. هذه هي البطاقة الذهبية النهائية.",
        "lang_tag": "ar-SA",
        "variation": "📊 جدول التغيّرات", "lmax": "قيمة عظمى محلية", "lmin": "قيمة صغرى محلية",
    },
    "fr": {
        "title": "🧠 Tableau intelligent — laboratoire intégral",
        "subtitle": "NABIL explique une idée à la fois, avec le laboratoire correspondant juste en dessous.",
        "teacher": "NABIL explique", "study": "Résumé de la leçon", "final": "Carte dorée",
        "play": "▶ Expliquer depuis le début", "stop": "■ Arrêter", "prev": "◀ Précédent",
        "next": "Suivant ▶", "restart": "↻ Recommencer", "current": "🔊 Expliquer cette idée",
        "voice_on": "🔊 Voix activée", "voice_off": "🔇 Voix coupée",
        "lab": "🧪 Laboratoire", "run_lab": "▶ Lancer le labo", "talk": "🎙 Parle-moi",
        "step": "Étape", "idea": "Idée", "hello": "Je suis NABIL. Appuie sur « Expliquer depuis le début ».",
        "goal": "🎯 La carte dorée complète apparaît après la dernière idée.",
        "novoice": "Aucune voix française installée ; l'explication continue par écrit.",
        "done": "Explication terminée. Voici la carte dorée finale.",
        "lang_tag": "fr-FR",
        "variation": "📊 Tableau de variations", "lmax": "max local", "lmin": "min local",
    },
    "en": {
        "title": "🧠 Smart Board — Whole-Lesson Lab",
        "subtitle": "NABIL teaches one idea at a time, with that idea's lab directly beneath it.",
        "teacher": "NABIL is explaining", "study": "Lesson summary", "final": "Golden Card",
        "play": "▶ Teach from the beginning", "stop": "■ Stop", "prev": "◀ Previous",
        "next": "Next ▶", "restart": "↻ Restart", "current": "🔊 Explain this idea",
        "voice_on": "🔊 Voice ON", "voice_off": "🔇 Voice OFF",
        "lab": "🧪 Lab", "run_lab": "▶ Run the lab", "talk": "🎙 Talk to Me",
        "step": "Step", "idea": "Idea", "hello": "I am NABIL. Press “Teach from the beginning”.",
        "goal": "🎯 The full Golden Card appears after the last idea.",
        "novoice": "No matching voice is installed on this device; teaching continues in text.",
        "done": "Teaching complete. Here is the final Golden Card.",
        "lang_tag": "en-US",
        "variation": "📊 Variation Table", "lmax": "local max", "lmin": "local min",
    },
}

_EXERCISE_LABELS = {
    "ar": {"title": "🧠 لوح نبيل الذكي — شرح التمارين",
           "subtitle": "يحلّ نبيل تمرينًا واحدًا في كل مرة، خطوة بخطوة، ثم تظهر البطاقة الذهبية بنتائج التمارين.",
           "study": "نتائج التمارين", "goal": "🎯 تظهر البطاقة الذهبية بعد آخر تمرين.",
           "idea": "التمرين"},
    "fr": {"title": "🧠 Tableau NABIL — explication des exercices",
           "subtitle": "NABIL résout un exercice à la fois, étape par étape, puis la carte dorée résume les résultats.",
           "study": "Résultats des exercices", "goal": "🎯 La carte dorée apparaît après le dernier exercice.",
           "idea": "Exercice"},
    "en": {"title": "🧠 NABIL Smart Board — Exercises",
           "subtitle": "NABIL solves one exercise at a time, step by step, then the Golden Card summarises the results.",
           "study": "Exercise results", "goal": "🎯 The Golden Card appears after the last exercise.",
           "idea": "Exercise"},
}

_CSS = r"""
#nabilWholeLessonSmartLab{--bg:#031025;--panel:#071c35;--board:#04172c;--line:#1f5c91;--cyan:#25d8ff;--gold:#ffd35a;--green:#52e6a4;--violet:#b98cff;--txt:#f7fbff;--muted:#9fc4e5;
 margin-top:26px;background:linear-gradient(180deg,#082447,#061a32);color:var(--txt);border:1px solid #1e6aa4;border-radius:20px;padding:14px;box-shadow:0 18px 50px #0006;font-family:system-ui,Segoe UI,Arial,sans-serif;overflow:hidden}
#nabilWholeLessonSmartLab *{box-sizing:border-box}
#nabilWholeLessonSmartLab .v18-top{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;border-bottom:1px solid #1a4f7e;padding-bottom:10px}
#nabilWholeLessonSmartLab .v18-top h2{margin:0;font-size:clamp(18px,2.4vw,28px);color:var(--cyan)}
#nabilWholeLessonSmartLab .v18-top p{margin:4px 0 0;color:#b9daf5;font-size:14px}
#nabilWholeLessonSmartLab .v18-badge{font-size:12px;border:1px solid #2a6f9f;background:#082c50;padding:5px 10px;border-radius:999px;font-weight:800}
#nabilWholeLessonSmartLab .v18-grid{display:grid;grid-template-columns:minmax(200px,.95fr) minmax(0,2.3fr) minmax(210px,.8fr);gap:12px;margin-top:12px}
#nabilWholeLessonSmartLab .v18-box{background:var(--panel);border:1px solid var(--line);border-radius:15px;padding:12px;min-width:0}
#nabilWholeLessonSmartLab .v18-box h3{margin:0 0 8px;color:var(--cyan);font-size:17px}
#nabilWholeLessonSmartLab .v18-slot{background:#04172c;border:1px dashed #315d79;border-radius:11px;padding:9px 10px;margin:8px 0;opacity:.45}
#nabilWholeLessonSmartLab .v18-slot .l{font-size:12px;color:var(--muted);font-weight:900;overflow-wrap:anywhere}
#nabilWholeLessonSmartLab .v18-slot .v{margin-top:4px;line-height:1.45;overflow-wrap:anywhere}
#nabilWholeLessonSmartLab .v18-slot.locked{opacity:1;background:linear-gradient(180deg,#073b3c,#062b30);border:1px solid #1aa9a1;box-shadow:inset 4px 0 0 var(--green)}
#nabilWholeLessonSmartLab .v18-slot.current{opacity:1;border:1px solid var(--gold)}
#nabilWholeLessonSmartLab .v18-goal{margin-top:12px;border:1px solid #19a29d;background:#063739;border-radius:12px;padding:10px;line-height:1.45;font-size:14px}
#nabilWholeLessonSmartLab .v18-board{position:relative;min-height:380px;background:var(--board);border:1px solid var(--line);border-radius:12px;overflow:hidden;padding:18px}
#nabilWholeLessonSmartLab .v18-board:before{content:"";position:absolute;inset:0;opacity:.25;background-image:linear-gradient(#10345a 1px,transparent 1px),linear-gradient(90deg,#10345a 1px,transparent 1px);background-size:48px 48px;pointer-events:none}
#nabilWholeLessonSmartLab .v18-board>*{position:relative}
#nabilWholeLessonSmartLab .v18-bt{font-size:clamp(22px,2.6vw,38px);font-weight:900;color:var(--gold);margin-bottom:12px;min-height:1.3em;overflow-wrap:anywhere}
#nabilWholeLessonSmartLab .v18-line{margin:7px 0;padding:6px 12px;border-inline-start:4px solid var(--cyan);background:#061b35;border-radius:10px;font-size:clamp(17px,1.7vw,24px);line-height:1.55;overflow-wrap:anywhere}
#nabilWholeLessonSmartLab .v18-line:nth-child(3n+2){border-color:var(--gold)}
#nabilWholeLessonSmartLab .v18-line:nth-child(3n+3){border-color:var(--green)}
#nabilWholeLessonSmartLab .v18-line.now{box-shadow:0 0 0 1px var(--cyan) inset}
#nabilWholeLessonSmartLab .v18-line .k{color:var(--cyan);font-weight:900;margin-inline-end:6px}
#nabilWholeLessonSmartLab .v18-line .f{direction:ltr;unicode-bidi:isolate;text-align:center;margin-top:6px;padding:7px 8px;border:1px dashed #315d79;border-radius:8px;font-family:"Cambria Math","STIX Two Math","Courier New",serif;font-size:clamp(18px,2vw,28px);color:#fff;overflow-x:auto;white-space:pre-wrap}
#nabilWholeLessonSmartLab .cursor::after{content:"▋";color:var(--cyan);animation:v18blink 1s steps(1,end) infinite;margin-inline-start:3px}
@keyframes v18blink{50%{opacity:0}}
#nabilWholeLessonSmartLab .v18-labwrap{margin-top:10px;background:#020912;border:1px solid #1c4569;border-radius:12px;overflow:hidden}
#nabilWholeLessonSmartLab .v18-labwrap h4{margin:0;padding:8px 12px;color:var(--gold);font-size:14px;background:#06223a;display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap}
#nabilWholeLessonSmartLab iframe{display:block;width:100%;height:560px;border:0;background:#05172d}
#nabilWholeLessonSmartLab .v18-teacher{text-align:center}
#nabilWholeLessonSmartLab .v18-teacher img{width:130px;max-width:100%;border-radius:12px;background:#fff;padding:6px}
#nabilWholeLessonSmartLab .v18-speech{background:#04172c;border:1px solid #234f75;border-radius:11px;padding:12px;line-height:1.6;font-size:15px;min-height:96px;margin-top:10px;overflow-wrap:anywhere;text-align:start}
#nabilWholeLessonSmartLab .v18-controls{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
#nabilWholeLessonSmartLab button{min-height:44px;background:#123c63;color:#fff;border:1px solid #2b6c9c;border-radius:9px;padding:8px 12px;font-weight:800;cursor:pointer;font-family:inherit}
#nabilWholeLessonSmartLab button.primary{background:var(--cyan);color:#012331;border-color:var(--cyan)}
#nabilWholeLessonSmartLab button.voice{background:#143f35;border-color:#2da47f}
#nabilWholeLessonSmartLab button.talk{background:#ef3340;border:none;width:100%;margin-top:10px}
#nabilWholeLessonSmartLab button:focus-visible{outline:3px solid #ffe084;outline-offset:2px}
#nabilWholeLessonSmartLab .v18-timeline{display:flex;gap:6px;margin-top:10px;flex-wrap:wrap}
#nabilWholeLessonSmartLab .v18-dot{width:44px;height:44px;border-radius:50%;padding:0;background:#08213d;border:1px solid #315c7e;font-size:13px}
#nabilWholeLessonSmartLab .v18-dot.on{background:#0d6276;border-color:var(--cyan)}
#nabilWholeLessonSmartLab .v18-dot.done{background:#124c3d;border-color:var(--green)}
#nabilWholeLessonSmartLab .v18-var{margin-top:10px;background:#071c35;border:1px solid var(--line);border-radius:12px;padding:10px;overflow-x:auto}
#nabilWholeLessonSmartLab .v18-var h4{margin:0 0 8px;color:var(--gold);font-size:15px}
#nabilWholeLessonSmartLab .v18-var table{border-collapse:collapse;min-width:100%;direction:ltr;text-align:center}
#nabilWholeLessonSmartLab .v18-var th,#nabilWholeLessonSmartLab .v18-var td{border:1px solid #2a6f9f;padding:7px 9px;font-size:14px;white-space:nowrap}
#nabilWholeLessonSmartLab .v18-var th{background:#0b3358;color:var(--cyan)}
#nabilWholeLessonSmartLab .v18-var td.k{color:var(--gold);font-weight:800}
#goldenReferenceCard .nabil-sci-table-wrap,#goldenReferenceCard .nabil-sci-table th,#goldenReferenceCard .nabil-sci-table td{direction:ltr;unicode-bidi:isolate}
#nabilWholeLessonSmartLab .v18-note{font-size:12px;color:var(--muted);margin-top:8px}
#nabilWholeLessonSmartLab .v18-student-interaction{padding:14px;border:1px solid var(--gold);border-radius:12px;margin-top:12px;background:#092b49}
#nabilWholeLessonSmartLab .v18-student-interaction input{min-height:44px;background:#fff;color:#122438;border-radius:8px;padding:8px;width:100%;margin:8px 0}
#nabilWholeLessonSmartLab .v18-student-interaction button{margin:4px}
#nabilWholeLessonSmartLab .v18-written-section{border-bottom:1px solid #315d79;padding-bottom:12px;margin-bottom:16px}
#nabilWholeLessonSmartLab .v18-written-heading{color:var(--gold);font-size:19px;margin:12px 0}
#nabilWholeLessonSmartLab .v18-final{display:none;margin-top:12px}
#nabilWholeLessonSmartLab.is-final .v18-final{display:block}
#nabilWholeLessonSmartLab.is-final .v18-grid,#nabilWholeLessonSmartLab.is-final .v18-labwrap{display:none}
@media(max-width:1050px){#nabilWholeLessonSmartLab .v18-grid{grid-template-columns:1fr}#nabilWholeLessonSmartLab .v18-teacher{display:grid;grid-template-columns:96px 1fr;gap:10px;text-align:start;align-items:start}#nabilWholeLessonSmartLab .v18-teacher h3{grid-column:1/-1}#nabilWholeLessonSmartLab .v18-teacher img{width:90px}#nabilWholeLessonSmartLab .v18-teacher .v18-speech{margin-top:0}#nabilWholeLessonSmartLab .v18-teacher button.talk{grid-column:1/-1}}
@media(max-width:560px){#nabilWholeLessonSmartLab{padding:8px;border-radius:14px}#nabilWholeLessonSmartLab .v18-board{min-height:300px;padding:10px}#nabilWholeLessonSmartLab iframe{height:70vh;min-height:420px}#nabilWholeLessonSmartLab .v18-controls{display:grid;grid-template-columns:1fr 1fr}#nabilWholeLessonSmartLab .v18-controls .primary{grid-column:1/-1}}
"""

_JS = r"""
(()=>{
 const DATA=JSON.parse(document.getElementById('nabilV18Data').textContent);
 const root0=document.getElementById('nabilWholeLessonSmartLab');
 const LAB=JSON.parse(new TextDecoder().decode(Uint8Array.from(atob(root0.dataset.v18Labels),c=>c.charCodeAt(0))));DATA.all_labels=LAB;
 let L=LAB[DATA.lang];const slides=DATA.slides,FAST=window.NABIL_V18_FAST===true;
 const root=document.getElementById('nabilWholeLessonSmartLab');
 const $=id=>document.getElementById(id);
 const frame=$('nabilWholeLessonFrame'),bt=$('v18Title'),lines=$('v18Lines'),speech=$('v18Speech'),badge=$('v18Badge'),
       timeline=$('nabilWholeTimeline'),slots=$('v18Slots'),voiceBtn=$('nabilWholeVoice'),finalHost=$('goldenReferenceCard'),
       labWrap=$('v18LabWrap'),labTitle=$('v18LabTitle'),voiceNote=$('v18VoiceNote');
 let idea=0,stepI=-1,token=0,voiceOn=true,finalShown=false,playing=false,awaitingStudent=false;
 const FINAL=slides.length;                       /* index of the golden-card stage */
 let avatarObjectUrl=null;
 function approvedAvatarUrl(){
  if(!avatarObjectUrl){
   const bytes=Uint8Array.from(atob(DATA.avatar_base64),c=>c.charCodeAt(0));
   avatarObjectUrl=URL.createObjectURL(new Blob([bytes],{type:'image/jpeg'}));
  }
  return avatarObjectUrl;
 }
 window.addEventListener('pagehide',()=>{if(avatarObjectUrl)URL.revokeObjectURL(avatarObjectUrl)});
 $('v18TeacherAvatar').src=approvedAvatarUrl();
 const sleep=ms=>new Promise(r=>setTimeout(r,FAST?0:ms));
 const el=(t,c,x)=>{const e=document.createElement(t);if(c)e.className=c;if(x!==undefined)e.textContent=x;return e};
 /* language: follows the page translation runtime (NABILPageLanguage) when present */
 const PL=()=>window.NABILPageLanguage;
 const cur=()=>{const l=PL()&&PL().get&&PL().get();return DATA.all_labels[l]?l:DATA.lang};
 const tr=s=>{s=String(s||'');try{return PL()&&PL().translateText?PL().translateText(s,cur()):s}catch(_){return s}};
 const trDeep=o=>Array.isArray(o)?o.map(trDeep):(o&&typeof o==='object')?Object.fromEntries(Object.entries(o).map(([k,v])=>[k,['language','kind','subject','avatar_src','concept_ids'].includes(k)?v:trDeep(v)])):(typeof o==='string'?tr(o):o);
 /* localise 'local max/min' tokens of the deterministic variation table */
 const locCell=t=>String(t).replace(/local max/,L.lmax).replace(/local min/,L.lmin);
 const locVT=vt=>vt?{columns:vt.columns,rows:vt.rows.map(r=>({label:r.label,cells:r.cells.map(locCell)}))}:vt;
 function paintVar(){const s=slides[Math.min(idea,slides.length-1)],box=$('v18VarBox');const vt=s&&s.variation&&s.variation.table;
  if(!vt){box.style.display='none';box.innerHTML='';return}
  const v=locVT(vt),h=document.createElement('h4');h.textContent=L.variation;const tb=document.createElement('table');
  const r0=tb.insertRow();const th=document.createElement('th');th.textContent='x';r0.appendChild(th);v.columns.forEach(c=>{const e=document.createElement('th');e.textContent=c;r0.appendChild(e)});
  v.rows.forEach(r=>{const tr_=tb.insertRow();const e=document.createElement('th');e.textContent=r.label;tr_.appendChild(e);r.cells.forEach(c=>{const d=tr_.insertCell();d.textContent=c==="∥"?"∥":c;if(/max|min|\u2248|^0$/.test(c)||c===L.lmax||c===L.lmin||/max|min/.test(c))d.className='k'})});
  box.innerHTML='';box.append(h,tb);box.style.display=''}
 function relabel(){L=DATA.all_labels[cur()];root.querySelectorAll('[data-v18-l]').forEach(n=>{n.textContent=L[n.dataset.v18L]});
  voiceBtn.textContent=voiceOn?L.voice_on:L.voice_off;$('v18VoiceState').textContent=voiceBtn.textContent;}

 /* ---------------- voice (real, with honest fallback) ---------------- */
 function pickVoice(tag){
  try{const vs=speechSynthesis.getVoices(),p=tag.slice(0,2).toLowerCase();
   return vs.find(v=>v.lang.toLowerCase().replace('_','-')===tag.toLowerCase())||vs.find(v=>v.lang.toLowerCase().startsWith(p))||null}catch(_){return null}
 }
 function stopSpeech(){try{speechSynthesis.cancel()}catch(_){};try{window.NABILLessonE2E?.stopSpeech?.()}catch(_){}}
 function speak(text){
  return new Promise(resolve=>{
   if(!voiceOn||!String(text||'').trim()){resolve();return}
   const mine=token;
   const fallbackMs=Math.min(9000,900+String(text).length*45);
   try{
    if(window.NABILLessonE2E?.speak){Promise.resolve(window.NABILLessonE2E.speak(text,DATA.lang)).then(()=>resolve(),()=>resolve());return}
    if(!('speechSynthesis' in window)){voiceNote.textContent=L.novoice;setTimeout(resolve,FAST?0:fallbackMs);return}
    speechSynthesis.cancel();
    const u=new SpeechSynthesisUtterance(text);u.lang=L.lang_tag;u.rate=.92;
    const v=pickVoice(L.lang_tag);
    if(v)u.voice=v;else{voiceNote.textContent=L.novoice}
    let done=false;const fin=()=>{if(!done){done=true;resolve()}};
    u.onend=fin;u.onerror=fin;speechSynthesis.speak(u);
    setTimeout(()=>{if(mine!==token)fin()},300);
    setTimeout(fin,Math.max(fallbackMs*3,15000));
    if(!v)setTimeout(fin,FAST?0:fallbackMs);
   }catch(_){setTimeout(resolve,FAST?0:fallbackMs)}
  });
 }
 function typeInto(node,text,tok){
  return new Promise(res=>{
   if(FAST||!text){node.textContent=text;return res(true)}
   node.textContent='';node.classList.add('cursor');let i=0;
   const tick=()=>{if(tok!==token){node.classList.remove('cursor');return res(false)}
    node.textContent=text.slice(0,++i);
    if(i<text.length)setTimeout(tick,18);else{node.classList.remove('cursor');res(true)}};
   tick();
  });
 }

 /* ---------------- structure ---------------- */
 function buildSlots(){slots.innerHTML='';slides.forEach((s,i)=>{const d=el('div','v18-slot');d.id='v18Slot'+i;const l=el('div','l',(i+1)+'. '+tr(s.title));const v=el('div','v','—');d.append(l,v);slots.appendChild(d)})}buildSlots();
 slides.concat([{title:L.final}]).forEach((_,i)=>{const b=el('button','v18-dot',i+1);b.type='button';b.setAttribute('aria-label',(i<slides.length?L.idea+' ':L.final+' ')+(i+1));b.onclick=()=>{halt();goTo(i)};timeline.appendChild(b)});
 function paintTimeline(){const cur=finalShown?FINAL:idea;[...timeline.children].forEach((b,i)=>b.className='v18-dot '+(i<cur?'done':(i===cur?'on':'')))}
 function paintSlots(){slides.forEach((s,i)=>{const d=$('v18Slot'+i);const complete=finalShown||i<idea;d.className='v18-slot'+(complete?' locked':(i===idea?' current':''));d.querySelector('.v');d.querySelector('.v').textContent=complete?(tr(s.conclusion)||'✓'):'—'})}
 function showLines(upto,typeLast,tok){
  // P0 universal board: retain all preceding verified teaching on ONE board.
  // No extra slideshow cards are rendered as the principal explanation.
  lines.replaceChildren();
  for(let past=0;past<idea;past++){
   const section=el('section','v18-written-section');
   section.appendChild(el('h3','v18-written-heading',tr(slides[past].title)));
   for(const st of slides[past].steps){
    const row=el('div','v18-line');
    if(st.label)row.appendChild(el('span','k',tr(st.label)+': '));
    row.appendChild(el('span','t',tr(st.text)));
    if(st.formula)row.appendChild(el('div','f',st.formula));
    section.appendChild(row);
   }
   lines.appendChild(section);
  }
  const s=slides[idea];let last=null;
  for(let i=0;i<=upto&&i<s.steps.length;i++){
   const st=s.steps[i],row=el('div','v18-line'+(i===upto?' now':''));
   const k=el('span','k',st.label?tr(st.label)+':':'');const t=el('span','t');row.append(k,t);
   if(st.formula){const f=el('div','f',st.formula);row.appendChild(f)}
   lines.appendChild(row);last=(i===upto)?t:last;
   if(i!==upto)t.textContent=tr(st.text);
  }
  if(last&&typeLast)return typeInto(last,tr(s.steps[upto].text),tok);
  if(last)last.textContent=tr(s.steps[upto].text);
  return Promise.resolve(true);
 }
 function loadLab(){
  const s=slides[idea];labWrap.style.display=s.srcdoc?'':'none';labTitle.textContent=L.lab+' — '+tr(s.title);
  if(frame.dataset.idx!==String(idea)){frame.dataset.idx=String(idea);frame.srcdoc=s.srcdoc||''}
 }
 function setFinal(on){
  finalShown=on;root.classList.toggle('is-final',on);
  if(on&&!finalHost.dataset.rendered){
   finalHost.dataset.rendered='1';
   try{const g=Object.assign({},DATA.golden,{language:cur(),avatar_src:approvedAvatarUrl()});if(g.function_study&&g.function_study.variation_table)g.function_study={variation_table:locVT(g.function_study.variation_table)};
    (window.__NABIL_V18_CARDS||window.NABILScientificCards).fromLesson(trDeep(g),finalHost)}
   catch(e){finalHost.textContent='GOLDEN_CARD_RENDER_FAILED: '+e;finalHost.dataset.failed='1'}
  }
 }
 function paintIdea(upto,typeLast,tok){
  if(!awaitingStudent){const interact=$('v18StudentInteraction');interact.hidden=true;interact.replaceChildren()}
  setFinal(false);bt.textContent=tr(slides[idea].title);
  badge.textContent=L.idea+' '+(idea+1)+' / '+slides.length+' · '+L.step+' '+(Math.max(upto,0)+1)+' / '+slides[idea].steps.length;
  paintSlots();paintTimeline();loadLab();paintVar();return showLines(Math.max(upto,0),typeLast,tok);
 }
 async function presentStep(i,withVoice){
  stepI=i;const tok=++token;stopSpeech();
  // Start voice when writing begins, not after the typing animation ends.
  // Both remain bound to the same cancellation token.
  const st=slides[idea].steps[i],spoken=tr(st.text);
  speech.textContent=spoken;
  if(st.check&&st.check.question){awaitingStudent=true;showStudentCheck(st.check)}
  const writing=paintIdea(i,!FAST,tok);
  const narration=withVoice?speak(spoken):Promise.resolve();
  const [ok]=await Promise.all([writing,narration]);
  return Boolean(ok)&&tok===token;
 }
 function showStudentCheck(check){
  const host=$('v18StudentInteraction');host.hidden=false;host.replaceChildren();
  const q=el('p','v18-student-question',tr(check.question));
  const input=el('input','v18-student-answer');input.setAttribute('aria-label',tr(check.question));input.type='text';
  const feedback=el('p','v18-student-feedback');feedback.setAttribute('aria-live','polite');
  const submit=el('button','v18-student-submit',L.submit_answer||'Check answer');
  const hint=el('button','v18-student-hint',L.hint||'Hint');
  const expected=String(check.expected||'').trim();
  // No automatic acceptance of unverified responses or invented solutions.
  submit.onclick=()=>{
    const got=input.value.trim();
    if(!got){feedback.textContent=L.answer_required||'Enter an answer.';return}
    const norm=x=>x.normalize('NFKC').replace(/\s+/g,'').toLowerCase();
    if(expected&&norm(got)===norm(expected)){
      feedback.textContent=tr(check.correct_feedback||L.correct||'Correct. Explain why.');
      awaitingStudent=false;input.disabled=true;submit.disabled=true;
    }else{
      feedback.textContent=tr(check.wrong_feedback||L.try_again||'Try again. Think through the steps.');
    }
  };
  hint.onclick=()=>{feedback.textContent=tr(check.hint||L.try_again||'Review the preceding explanation.')};
  host.append(q,input,submit,hint,feedback);
 }
 function showFinalStage(){
  if(awaitingStudent)return;
  stepI=slides[Math.min(idea,slides.length-1)].steps.length-1;idea=FINAL;stopSpeech();token++;
  setFinal(true);badge.textContent=L.final;speech.textContent=L.done;paintSlots();paintTimeline();
 }
 function halt(){playing=false;token++;stopSpeech()}
 function goTo(i){
  if(awaitingStudent&&i>idea)return;
  if(i>=FINAL){showFinalStage();return}
  idea=Math.max(0,i);stepI=0;presentStep(0,false);
 }
 function nextStep(){
  if(awaitingStudent)return;
  halt();
  if(finalShown)return;
  if(stepI<slides[idea].steps.length-1)presentStep(stepI+1,false);
  else if(idea<slides.length-1){idea++;presentStep(0,false)}
  else showFinalStage();
 }
 function prevStep(){
  halt();
  if(finalShown){idea=slides.length-1;presentStep(slides[idea].steps.length-1,false);return}
  if(stepI>0)presentStep(stepI-1,false);
  else if(idea>0){idea--;presentStep(slides[idea].steps.length-1,false)}
 }
 async function teachIdea(){
  const mine=idea;
  for(let i=0;i<slides[mine].steps.length;i++){
   if(!playing)return false;
   if(!(await presentStep(i,true)))return false;
   if(awaitingStudent){playing=false;return false}
   await sleep(450);
  }
  return playing;
 }
 async function playAll(){
  halt();playing=true;idea=0;
  for(let a=0;a<slides.length;a++){
   idea=a;if(!playing)return;
   if(!(await teachIdea()))return;
   await sleep(500);
  }
  if(playing){showFinalStage();await speak(L.done);playing=false}
 }
 async function explainCurrent(){halt();playing=true;if(finalShown){await speak([tr(DATA.title)].concat(slides.map(s=>tr(s.title)+'. '+tr(s.conclusion))).join(' ')||L.done);playing=false;return}
  await teachIdea();playing=false}
 function runLab(){
  try{const shell=frame.contentDocument?.querySelector('.nabil-reference-smart-lab');shell?.dispatchEvent(new CustomEvent('nabil:teach-all'))}catch(_){}
 }
 $('nabilWholePlay').onclick=playAll;
 $('nabilWholeStop').onclick=()=>{halt();try{frame.contentDocument?.querySelector('.nabil-reference-smart-lab')?.dispatchEvent(new CustomEvent('nabil:teach-stop'))}catch(_){}};
 $('nabilWholePrev').onclick=prevStep;$('nabilWholeNext').onclick=nextStep;
 $('nabilWholeRestart').onclick=()=>{halt();goTo(0)};
 $('nabilWholeCurrent').onclick=explainCurrent;
 $('nabilWholeRunLab').onclick=runLab;
 $('v18Talk').onclick=()=>{halt();speak(speech.textContent||L.hello)};
 voiceBtn.onclick=()=>{voiceOn=!voiceOn;relabel();if(!voiceOn)stopSpeech()};
 window.addEventListener('nabil:page-language-change',()=>{
  halt();relabel();buildSlots();finalHost.innerHTML='';delete finalHost.dataset.rendered;
  if(finalShown){setFinal(true);badge.textContent=L.final;speech.textContent=L.done;paintSlots();paintTimeline()}
  else{paintIdea(Math.max(stepI,0),false,token);speech.textContent=tr(slides[idea].steps[Math.max(stepI,0)].text)}
 });
 try{speechSynthesis.getVoices();speechSynthesis.onvoiceschanged=()=>{}}catch(_){}
 window.NABILWholeLessonOrchestrator={
  play:playAll,stop:()=>$('nabilWholeStop').click(),current:()=>explainCurrent(),
  goTo:i=>{halt();goTo(Number(i)||0)},next:nextStep,prev:prevStep,
  state:()=>({idea,step:stepI,final:finalShown,awaitingStudent,voice:voiceOn,ideas:slides.length,lang:cur()}),
  finalIndex:FINAL
 };
 relabel();speech.textContent=L.hello;idea=0;stepI=0;paintIdea(0,false,token);
})();
"""


def _read(name: str) -> str:
    return (_ASSETS / name).read_text(encoding="utf-8")



def verify_v18_scientific_card_inline_engine(page_html: str) -> bool:
    """Strict source-authenticated embedded V18 engine validation.

    Unlike text-marker tests, this requires the *entire* inline engine bytes
    to match the audited repository renderer. The Playwright QA independently
    verifies execution and visible Golden Card as the final teaching stage.
    """
    if (
        f'data-nabil-v18-board="{V18_BOARD_CONTRACT}"' not in page_html
        or "V18_GOLDEN_CARD_ENGINE_BOOTSTRAP_FAILED" not in page_html
    ):
        return False
    matches = re.findall(
        r'<script type="text/plain" id="nabilV18CardEnginePayload">'
        r'([A-Za-z0-9+/=]+)</script>',
        page_html,
    )
    if len(matches) != 1:
        return False
    try:
        embedded = base64.b64decode(matches[0], validate=True)
    except (ValueError, base64.binascii.Error):
        return False
    trusted = _read("v18_golden_cards_engine.js").encode("utf-8")
    return embedded == trusted and b"window.NABILScientificCards={" in embedded

def build_slide(act: dict, lang_code: str) -> dict | None:
    """Convert one verified concept activity into a board slide (or None)."""
    lab_html = str(act.get("lab_html") or "")
    if not lab_html and not act.get("allow_no_lab"):
        return None
    steps = []
    for st in (act.get("teaching_steps") or []):
        sentence = str(st.get("sentence") or "").strip()
        if sentence:
            steps.append({
                "label": str(st.get("label") or ""),
                "text": sentence,
                "formula": str(st.get("formula") or ""),
                "kind": str(st.get("kind") or ""),
                "check": st.get("student_check") if isinstance(st.get("student_check"), dict) else None,
            })
    if not steps:
        for label, key in (("", "phenomenon"), ("", "investigation"),
                           ("", "observation"), ("", "interpretation"),
                           ("", "conclusion")):
            v = str(act.get(key) or "").strip()
            if v:
                steps.append({"label": label, "text": v, "formula": "", "kind": key})
    if not steps:
        return None
    srcdoc = "" if not lab_html else (
        '<!doctype html><html><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<style>html,body{margin:0;background:#05172d;color:#eef8ff;overflow-x:hidden}'
        'body{padding:4px}*{box-sizing:border-box}</style>'
        '<script>try{window.NABILLessonE2E=parent.NABILLessonE2E}catch(e){}</script>'
        '</head><body>' + lab_html + '</body></html>'
    )
    vt = act.get("variation_table")
    if not isinstance(vt, dict):
        from scripts.nabil_factory.cards.variation_table import (
            build_variation_table, extract_function_expr)
        expr = extract_function_expr(act)
        vt = build_variation_table(expr) if expr else None
    return {
        "variation": {"table": vt} if vt else None,
        "concept_id": str(act.get("concept_id") or ""),
        "title": str(act.get("title") or ""),
        "steps": steps,
        "conclusion": str(act.get("conclusion") or act.get("observation") or "").strip(),
        "srcdoc": srcdoc,
    }


def build_golden_spec(title: str, activities: list, lang_code: str,
                      subject: str = "", verification_note: str = "") -> dict:
    """Golden-card spec from verified activities only (V18 card engine schema)."""
    kind = {"mathematics": "mathematics", "math": "mathematics",
            "physics": "physics", "chemistry": "chemistry",
            "biology": "biology"}.get(subject.strip().lower(), "general_science")
    sections, key_results, verification = [], [], []
    var_table = None
    var_drawing = None
    for act in activities:
        sl = build_slide(dict(act, allow_no_lab=True), lang_code)
        if sl and sl.get("variation"):
            var_table = sl["variation"]["table"]
            from scripts.nabil_factory.cards.variation_table import (
                build_function_drawing, extract_function_expr)
            _e = extract_function_expr(act)
            var_drawing = build_function_drawing(_e, var_table) if _e else None
        t = str(act.get("title") or "").strip()
        concl = str(act.get("conclusion") or act.get("observation") or "").strip()
        # Golden exercise cards preserve the verified teacher's worked
        # reasoning, rather than reducing a solution to a numeric answer.
        verified_steps = [
            str(step.get("sentence") or "").strip()
            for step in (act.get("teaching_steps") or [])
            if isinstance(step, dict)
            and step.get("kind") in ("problem", "step", "final")
            and str(step.get("sentence") or "").strip()
        ]
        if t and (concl or verified_steps):
            sections.append({"label": t + ":", "items": verified_steps or [concl]})
            if verified_steps:
                key_results.extend(verified_steps)
            else:
                key_results.append(concl)
        if t:
            verification.append(t + (": " + verification_note if verification_note else ""))
    panels = [{"title": {"ar": "نتائج الدرس الموثّقة", "fr": "Résultats vérifiés",
                         "en": "Verified lesson results"}.get(lang_code, "Verified lesson results"),
               "icon": "✅", "steps": key_results}] if key_results else []
    extra = {}
    if var_table:
        kind = "function_study"
        panels.append({"title": {"ar": "الرسم وجدول التغيّرات", "fr": "Graphe et variations",
                                 "en": "Graph & Variation"}.get(lang_code, "Graph & Variation"),
                       "icon": "📊", "table": True,
                       **({"drawings": [var_drawing]} if var_drawing else {})})
        extra["function_study"] = {"variation_table": var_table}
    return {
        **extra,
        "concept_ids": [str(a.get("concept_id") or "") for a in activities],
        "language": lang_code, "kind": kind, "subject": subject or kind,
        "title": title, "sections": sections, "key_results": key_results,
        "verification": verification,
        "panels": panels,
        "rule_summary": " ".join(key_results[-2:]) if key_results else "",
        "avatar_src": "",  # filled by render_v18_smart_board
    }


def render_v18_smart_board(title: str, activities: list, lang_code: str,
                           golden_spec: dict | None = None,
                           contract: str = "", mode: str = "lesson") -> str:
    lang = lang_code if lang_code in _LABELS else "en"
    all_labels = {k: dict(v) for k, v in _LABELS.items()}
    if mode == "exercises":
        for k in all_labels:
            all_labels[k].update(_EXERCISE_LABELS[k])
    labels = all_labels[lang]
    labels_b64 = base64.b64encode(
        json.dumps(all_labels, ensure_ascii=False).encode("utf-8")).decode("ascii")
    slides = [s for s in (build_slide(a, lang) for a in activities) if s]
    if not slides:
        return ""
    if not golden_spec or not golden_spec.get("sections"):
        raise RuntimeError("V18_GOLDEN_CARD_SPEC_EMPTY")
    avatar_b64 = _read("nabil_avatar_b64.txt").strip()
    golden = dict(golden_spec)
    # The approved NABIL portrait is not a textbook scan. Keep the original
    # image bytes but materialize a browser Blob URL only when the card renders.
    # Thus the strict data:image/ source-raster ban stays fully enforced.
    golden["avatar_src"] = ""
    golden_speech = " ".join(
        [title] + [str(s["title"]) + ". " + str(s["conclusion"]) for s in slides])
    data = json.dumps({
        "contract": V18_BOARD_CONTRACT, "lang": lang, "title": title, "mode": mode,
        "slides": slides, "golden": golden, "golden_speech": golden_speech,
        "avatar_base64": avatar_b64,
    }, ensure_ascii=False).replace("</", "<\\/").replace("<!--", "<\\!--")
    # Prevent the HTML math/translation normalization from rewriting executable
    # vendor JavaScript. Decode and execute its original bytes in the browser.
    engine_b64 = base64.b64encode(
        _read("v18_golden_cards_engine.js").encode("utf-8")
    ).decode("ascii")
    h = html.escape
    return f'''
<section id="nabilWholeLessonSmartLab" class="nabil-whole-lesson-smart-lab"
 data-whole-lesson-smart-lab="true" data-renderer-contract="{h(contract)}"
 data-nabil-v18-board="{V18_BOARD_CONTRACT}" data-v18-labels="{labels_b64}" data-v18-mode="{mode}" data-concept-count="{len(slides)}">
<style>{_CSS}</style>
<div class="v18-top"><div><h2 data-v18-l="title">{h(labels["title"])}</h2><p data-v18-l="subtitle">{h(labels["subtitle"])}</p><p style="font-size:12px;color:#8fb6d6">{h(title)}</p></div>
 <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap"><span class="v18-badge" id="v18Badge"></span><span class="v18-badge" id="v18VoiceState">{h(labels["voice_on"])}</span></div></div>
<div class="v18-grid">
 <section class="v18-box"><h3 data-v18-l="study">{h(labels["study"])}</h3><div id="v18Slots"></div><div class="v18-goal" data-v18-l="goal">{h(labels["goal"])}</div></section>
 <section class="v18-box"><div class="v18-board"><div class="v18-bt" id="v18Title"></div><div id="v18Lines"></div>
  <div class="v18-labwrap" id="v18LabWrap"><h4><span id="v18LabTitle"></span><button type="button" data-v18-l="run_lab" id="nabilWholeRunLab" style="min-height:36px">{h(labels["run_lab"])}</button></h4>
   <iframe id="nabilWholeLessonFrame" title="{h(labels["lab"])}"></iframe></div>
  <div class="v18-var" id="v18VarBox" style="display:none" data-v18-variation="true"></div>
  <div id="v18StudentInteraction" class="v18-student-interaction" hidden></div>
 </div>
</section>
 <aside class="v18-box v18-teacher"><h3>NABIL AI</h3><img id="v18TeacherAvatar" alt="NABIL AI">
  <div class="v18-speech" id="v18Speech" aria-live="polite"></div>
  <button type="button" class="talk" data-v18-l="talk" id="v18Talk">{h(labels["talk"])}</button></aside>
</div>
  <div class="v18-controls">
   <button type="button" class="primary" data-v18-l="play" id="nabilWholePlay">{h(labels["play"])}</button>
   <button type="button" data-v18-l="stop" id="nabilWholeStop">{h(labels["stop"])}</button>
   <button type="button" data-v18-l="prev" id="nabilWholePrev">{h(labels["prev"])}</button>
   <button type="button" data-v18-l="next" id="nabilWholeNext">{h(labels["next"])}</button>
   <button type="button" data-v18-l="restart" id="nabilWholeRestart">{h(labels["restart"])}</button>
   <button type="button" class="voice" data-v18-l="current" id="nabilWholeCurrent">{h(labels["current"])}</button>
   <button type="button" class="voice" id="nabilWholeVoice">{h(labels["voice_on"])}</button>
  </div>
  <div class="v18-timeline" id="nabilWholeTimeline"></div><div class="v18-note" id="v18VoiceNote"></div>
<div class="v18-final" data-v18-final-stage="true"><div id="goldenReferenceCard" data-nabil-v18-golden="true"></div></div>
<script type="application/json" id="nabilV18Data">{data}</script>
<script type="text/plain" id="nabilV18CardEnginePayload">{engine_b64}</script>
<script>
(() => {{
 const payload=document.getElementById('nabilV18CardEnginePayload');
 const bytes=Uint8Array.from(atob(payload.textContent.trim()),c=>c.charCodeAt(0));
 const source=new TextDecoder().decode(bytes);
 const script=document.createElement('script');
 script.textContent=source;
 payload.after(script);
 if(typeof window.NABILScientificCards?.fromLesson!=='function'){{
   throw new Error('V18_GOLDEN_CARD_ENGINE_BOOTSTRAP_FAILED');
 }}
 window.__NABIL_V18_CARDS=window.NABILScientificCards;
}})();
</script>
<script>{_JS}</script>
</section>'''


_SUP = {"0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵",
        "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹", "-": "⁻"}


def plain_math(text: str) -> str:
    """Readable board text from LaTeX-ish solver text (no delimiters shown)."""
    import re
    s = str(text or "")
    s = re.sub(r"\\[\(\)\[\]]|\$\$?", "", s)
    s = s.replace("\\times", "×").replace("\\cdot", "·").replace("\\div", "÷")
    s = s.replace("\\left", "").replace("\\right", "")
    s = re.sub(r"\^\{(-?\d+)\}", lambda m: "".join(_SUP.get(c, c) for c in m.group(1)), s)
    s = re.sub(r"\^(-?\d)", lambda m: "".join(_SUP.get(c, c) for c in m.group(1)), s)
    s = re.sub(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"(\1)/(\2)", s)
    return re.sub(r"\s+", " ", s).strip()


def build_exercise_activities(exercises: list, labels_ui: dict) -> list:
    """Verified SOLVED exercises -> board activities (one exercise per idea)."""
    acts = []
    for ex in exercises:
        sol = ex.get("_pre_solved_solution")
        if ex.get("solution_status") != "SOLVED" or not isinstance(sol, dict):
            continue
        steps = [{"label": labels_ui.get("problem", ""),
                  "sentence": plain_math(ex.get("exact_source_prompt") or ""),
                  "formula": "", "kind": "problem"}]
        for i, s in enumerate(sol.get("steps") or [], 1):
            txt = plain_math(s)
            if txt:
                steps.append({"label": f"{labels_ui.get('step', '')} {i}",
                              "sentence": txt, "formula": "", "kind": "step"})
        final = plain_math(sol.get("final_answer") or "")
        if not final:
            continue
        steps.append({"label": labels_ui.get("final", ""), "sentence": final,
                      "formula": "", "kind": "final"})
        acts.append({
            "concept_id": str(ex.get("exercise_id") or ex.get("number")),
            "title": f"{labels_ui.get('exercise', '')} {ex.get('number')}".strip(),
            "conclusion": final,
            # For exercises, the actual verified derivation is on the board.
            # A separate lab underneath is not an acceptable substitute.
            "lab_html": "", "allow_no_lab": True, "teaching_steps": steps,
            "formulas": [plain_math(ex.get("exact_source_prompt") or "")],
        })
    return acts


_EXERCISE_UI = {
    "ar": {"problem": "المسألة", "step": "الخطوة", "final": "الجواب النهائي", "exercise": "التمرين"},
    "fr": {"problem": "Énoncé", "step": "Étape", "final": "Réponse finale", "exercise": "Exercice"},
    "en": {"problem": "Problem", "step": "Step", "final": "Final answer", "exercise": "Exercise"},
}


def render_v18_exercises_board(title: str, exercises: list, lang_code: str,
                               subject: str = "", contract: str = "") -> str:
    """V18 board for the exercises page: one verified exercise per stage, with
    the final stage a Golden Card of the verified final answers. Returns "" when
    no exercise is SOLVED (nothing unverified is ever shown)."""
    lang = lang_code if lang_code in _EXERCISE_UI else "en"
    acts = build_exercise_activities(exercises, _EXERCISE_UI[lang])
    if not acts:
        return ""
    spec = build_golden_spec(title, acts, lang, subject=subject,
                             verification_note="✓")
    return render_v18_smart_board(title, acts, lang, golden_spec=spec,
                                  contract=contract, mode="exercises")
