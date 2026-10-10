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

import html
import json
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
    },
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
#nabilWholeLessonSmartLab .v18-note{font-size:12px;color:var(--muted);margin-top:8px}
#nabilWholeLessonSmartLab .v18-final{display:none;margin-top:12px}
#nabilWholeLessonSmartLab.is-final .v18-final{display:block}
#nabilWholeLessonSmartLab.is-final .v18-grid,#nabilWholeLessonSmartLab.is-final .v18-labwrap{display:none}
@media(max-width:1050px){#nabilWholeLessonSmartLab .v18-grid{grid-template-columns:1fr}#nabilWholeLessonSmartLab .v18-teacher{display:grid;grid-template-columns:96px 1fr;gap:10px;text-align:start;align-items:start}#nabilWholeLessonSmartLab .v18-teacher h3{grid-column:1/-1}#nabilWholeLessonSmartLab .v18-teacher img{width:90px}#nabilWholeLessonSmartLab .v18-teacher .v18-speech{margin-top:0}#nabilWholeLessonSmartLab .v18-teacher button.talk{grid-column:1/-1}}
@media(max-width:560px){#nabilWholeLessonSmartLab{padding:8px;border-radius:14px}#nabilWholeLessonSmartLab .v18-board{min-height:300px;padding:10px}#nabilWholeLessonSmartLab iframe{height:70vh;min-height:420px}#nabilWholeLessonSmartLab .v18-controls{display:grid;grid-template-columns:1fr 1fr}#nabilWholeLessonSmartLab .v18-controls .primary{grid-column:1/-1}}
"""

_JS = r"""
(()=>{
 const DATA=JSON.parse(document.getElementById('nabilV18Data').textContent);
 const L=DATA.labels,slides=DATA.slides,FAST=window.NABIL_V18_FAST===true;
 const root=document.getElementById('nabilWholeLessonSmartLab');
 const $=id=>document.getElementById(id);
 const frame=$('nabilWholeLessonFrame'),bt=$('v18Title'),lines=$('v18Lines'),speech=$('v18Speech'),badge=$('v18Badge'),
       timeline=$('nabilWholeTimeline'),slots=$('v18Slots'),voiceBtn=$('nabilWholeVoice'),finalHost=$('goldenReferenceCard'),
       labTitle=$('v18LabTitle'),voiceNote=$('v18VoiceNote');
 let idea=0,stepI=-1,token=0,voiceOn=true,finalShown=false,playing=false;
 const FINAL=slides.length;                       /* index of the golden-card stage */
 const sleep=ms=>new Promise(r=>setTimeout(r,FAST?0:ms));
 const el=(t,c,x)=>{const e=document.createElement(t);if(c)e.className=c;if(x!==undefined)e.textContent=x;return e};

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
 slides.forEach((s,i)=>{const d=el('div','v18-slot');d.id='v18Slot'+i;const l=el('div','l',(i+1)+'. '+s.title);const v=el('div','v','—');d.append(l,v);slots.appendChild(d)});
 slides.concat([{title:L.final}]).forEach((_,i)=>{const b=el('button','v18-dot',i+1);b.type='button';b.setAttribute('aria-label',(i<slides.length?L.idea+' ':L.final+' ')+(i+1));b.onclick=()=>{halt();goTo(i)};timeline.appendChild(b)});
 function paintTimeline(){const cur=finalShown?FINAL:idea;[...timeline.children].forEach((b,i)=>b.className='v18-dot '+(i<cur?'done':(i===cur?'on':'')))}
 function paintSlots(){slides.forEach((s,i)=>{const d=$('v18Slot'+i);const complete=finalShown||i<idea;d.className='v18-slot'+(complete?' locked':(i===idea?' current':''));d.querySelector('.v');d.querySelector('.v').textContent=complete?(s.conclusion||'✓'):'—'})}
 function showLines(upto,typeLast,tok){
  lines.innerHTML='';const s=slides[idea];let last=null;
  for(let i=0;i<=upto&&i<s.steps.length;i++){
   const st=s.steps[i],row=el('div','v18-line'+(i===upto?' now':''));
   const k=el('span','k',st.label?st.label+':':'');const t=el('span','t');row.append(k,t);
   if(st.formula){const f=el('div','f',st.formula);row.appendChild(f)}
   lines.appendChild(row);last=(i===upto)?t:last;
   if(i!==upto)t.textContent=st.text;
  }
  if(last&&typeLast)return typeInto(last,s.steps[upto].text,tok);
  if(last)last.textContent=s.steps[upto].text;
  return Promise.resolve(true);
 }
 function loadLab(){
  const s=slides[idea];labTitle.textContent=L.lab+' — '+s.title;
  if(frame.dataset.idx!==String(idea)){frame.dataset.idx=String(idea);frame.srcdoc=s.srcdoc||''}
 }
 function setFinal(on){
  finalShown=on;root.classList.toggle('is-final',on);
  if(on&&!finalHost.dataset.rendered){
   finalHost.dataset.rendered='1';
   try{window.NABILScientificCards.fromLesson(DATA.golden,finalHost)}
   catch(e){finalHost.textContent='GOLDEN_CARD_RENDER_FAILED: '+e;finalHost.dataset.failed='1'}
  }
 }
 function paintIdea(upto,typeLast,tok){
  setFinal(false);bt.textContent=slides[idea].title;
  badge.textContent=L.idea+' '+(idea+1)+' / '+slides.length+' · '+L.step+' '+(Math.max(upto,0)+1)+' / '+slides[idea].steps.length;
  paintSlots();paintTimeline();loadLab();return showLines(Math.max(upto,0),typeLast,tok);
 }
 async function presentStep(i,withVoice){
  stepI=i;const tok=++token;stopSpeech();
  const ok=await paintIdea(i,!FAST,tok);if(!ok||tok!==token)return false;
  const st=slides[idea].steps[i];speech.textContent=st.text;
  if(withVoice)await speak(st.text);
  return tok===token;
 }
 function showFinalStage(){
  stepI=slides[Math.min(idea,slides.length-1)].steps.length-1;idea=FINAL;stopSpeech();token++;
  setFinal(true);badge.textContent=L.final;speech.textContent=L.done;paintSlots();paintTimeline();
 }
 function halt(){playing=false;token++;stopSpeech()}
 function goTo(i){
  if(i>=FINAL){showFinalStage();return}
  idea=Math.max(0,i);stepI=0;presentStep(0,false);
 }
 function nextStep(){
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
 async function explainCurrent(){halt();playing=true;if(finalShown){await speak(DATA.golden_speech||L.done);playing=false;return}
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
 voiceBtn.onclick=()=>{voiceOn=!voiceOn;voiceBtn.textContent=voiceOn?L.voice_on:L.voice_off;$('v18VoiceState').textContent=voiceOn?L.voice_on:L.voice_off;if(!voiceOn)stopSpeech()};
 try{speechSynthesis.getVoices();speechSynthesis.onvoiceschanged=()=>{}}catch(_){}
 window.NABILWholeLessonOrchestrator={
  play:playAll,stop:()=>$('nabilWholeStop').click(),current:()=>explainCurrent(),
  goTo:i=>{halt();goTo(Number(i)||0)},next:nextStep,prev:prevStep,
  state:()=>({idea,step:stepI,final:finalShown,voice:voiceOn,ideas:slides.length}),
  finalIndex:FINAL
 };
 speech.textContent=L.hello;idea=0;stepI=0;paintIdea(0,false,token);
})();
"""


def _read(name: str) -> str:
    return (_ASSETS / name).read_text(encoding="utf-8")


def build_slide(act: dict, lang_code: str) -> dict | None:
    """Convert one verified concept activity into a board slide (or None)."""
    lab_html = str(act.get("lab_html") or "")
    if not lab_html:
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
    srcdoc = (
        '<!doctype html><html><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<style>html,body{margin:0;background:#05172d;color:#eef8ff;overflow-x:hidden}'
        'body{padding:4px}*{box-sizing:border-box}</style>'
        '<script>try{window.NABILLessonE2E=parent.NABILLessonE2E}catch(e){}</script>'
        '</head><body>' + lab_html + '</body></html>'
    )
    return {
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
    for act in activities:
        t = str(act.get("title") or "").strip()
        concl = str(act.get("conclusion") or act.get("observation") or "").strip()
        if t and concl:
            sections.append({"label": t + ":", "items": [concl]})
            key_results.append(concl)
        if t:
            verification.append(t + (": " + verification_note if verification_note else ""))
    return {
        "concept_ids": [str(a.get("concept_id") or "") for a in activities],
        "language": lang_code, "kind": kind, "subject": subject or kind,
        "title": title, "sections": sections, "key_results": key_results,
        "verification": verification,
        "panels": [{"title": {"ar": "نتائج الدرس الموثّقة", "fr": "Résultats vérifiés",
                              "en": "Verified lesson results"}.get(lang_code, "Verified lesson results"),
                    "icon": "✅", "steps": key_results}] if key_results else [],
        "rule_summary": " ".join(key_results[-2:]) if key_results else "",
        "avatar_src": "",  # filled by render_v18_smart_board
    }


def render_v18_smart_board(title: str, activities: list, lang_code: str,
                           golden_spec: dict | None = None,
                           contract: str = "") -> str:
    lang = lang_code if lang_code in _LABELS else "en"
    labels = _LABELS[lang]
    slides = [s for s in (build_slide(a, lang) for a in activities) if s]
    if not slides:
        return ""
    if not golden_spec or not golden_spec.get("sections"):
        raise RuntimeError("V18_GOLDEN_CARD_SPEC_EMPTY")
    avatar = "data:image/jpeg;base64," + _read("nabil_avatar_b64.txt").strip()
    golden = dict(golden_spec)
    golden["avatar_src"] = avatar
    golden_speech = " ".join(
        [title] + [str(s["title"]) + ". " + str(s["conclusion"]) for s in slides])
    data = json.dumps({
        "contract": V18_BOARD_CONTRACT, "lang": lang, "labels": labels,
        "slides": slides, "golden": golden, "golden_speech": golden_speech,
    }, ensure_ascii=False).replace("</", "<\\/").replace("<!--", "<\\!--")
    engine = _read("v18_golden_cards_engine.js").replace("</script", "<\\/script")
    h = html.escape
    return f'''
<section id="nabilWholeLessonSmartLab" class="nabil-whole-lesson-smart-lab"
 data-whole-lesson-smart-lab="true" data-renderer-contract="{h(contract)}"
 data-nabil-v18-board="{V18_BOARD_CONTRACT}" data-concept-count="{len(slides)}">
<style>{_CSS}</style>
<div class="v18-top"><div><h2>{h(labels["title"])}</h2><p>{h(labels["subtitle"])}</p><p style="font-size:12px;color:#8fb6d6">{h(title)}</p></div>
 <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap"><span class="v18-badge" id="v18Badge"></span><span class="v18-badge" id="v18VoiceState">{h(labels["voice_on"])}</span></div></div>
<div class="v18-grid">
 <section class="v18-box"><h3>{h(labels["study"])}</h3><div id="v18Slots"></div><div class="v18-goal">{h(labels["goal"])}</div></section>
 <section class="v18-box"><div class="v18-board"><div class="v18-bt" id="v18Title"></div><div id="v18Lines"></div></div>
  <div class="v18-labwrap"><h4><span id="v18LabTitle"></span><button type="button" id="nabilWholeRunLab" style="min-height:36px">{h(labels["run_lab"])}</button></h4>
   <iframe id="nabilWholeLessonFrame" title="{h(labels["lab"])}"></iframe></div>
</section>
 <aside class="v18-box v18-teacher"><h3>NABIL AI</h3><img src="{avatar}" alt="NABIL AI">
  <div class="v18-speech" id="v18Speech" aria-live="polite"></div>
  <button type="button" class="talk" id="v18Talk">{h(labels["talk"])}</button></aside>
</div>
  <div class="v18-controls">
   <button type="button" class="primary" id="nabilWholePlay">{h(labels["play"])}</button>
   <button type="button" id="nabilWholeStop">{h(labels["stop"])}</button>
   <button type="button" id="nabilWholePrev">{h(labels["prev"])}</button>
   <button type="button" id="nabilWholeNext">{h(labels["next"])}</button>
   <button type="button" id="nabilWholeRestart">{h(labels["restart"])}</button>
   <button type="button" class="voice" id="nabilWholeCurrent">{h(labels["current"])}</button>
   <button type="button" class="voice" id="nabilWholeVoice">{h(labels["voice_on"])}</button>
  </div>
  <div class="v18-timeline" id="nabilWholeTimeline"></div><div class="v18-note" id="v18VoiceNote"></div>
<div class="v18-final" data-v18-final-stage="true"><div id="goldenReferenceCard" data-nabil-v18-golden="true"></div></div>
<script type="application/json" id="nabilV18Data">{data}</script>
<script>{engine}</script>
<script>{_JS}</script>
</section>'''
