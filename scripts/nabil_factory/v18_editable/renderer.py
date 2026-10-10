"""V18 presentation renderer — verified-content-only, isolated from scientific gates.
Uses the original V18 playback controller, bundled inline for offline HTML export.
"""
from __future__ import annotations
import html
import json
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_ENGINE = ("p3_lab_standard_v12.js", "scientific_models.js",
           "scientific_visual_router.js", "runtime_controller.js")
_MARKER = "nabil-v18-renderer"

def _script_bundle():
    items=[]
    for name in _ENGINE:
        path=_ROOT/"app"/"static"/"v18"/name
        if not path.is_file():
            raise RuntimeError("V18_ENGINE_ASSET_MISSING:"+name)
        items.append(path.read_text(encoding="utf-8").replace("</script", "<\\/script"))
    return "\n".join("<script>"+item+"</script>" for item in items)

def _steps(theory):
    results=[]
    for act in theory.get("activities", []):
        flow=[]
        for step in act.get("teaching_steps") or []:
            words=" ".join(str(step.get(k) or "") for k in ("label","sentence","formula")).strip()
            if words:flow.append(words)
        if not flow:
            for k in ("phenomenon","investigation","observation","interpretation","conclusion"):
                value=str(act.get(k) or "").strip()
                if value:flow.append(value)
        if not flow:
            raise RuntimeError("V18_UNGROUNDED_CONCEPT:"+str(act.get("concept_id")))
        apply = act.get("student_apply_prompt") or {}
        question = act.get("student_question") or {}
        prompt = str(apply.get("prompt") or question.get("q") or "").strip()
        if not prompt:
            raise RuntimeError("V18_VERIFIED_APPLY_MISSING:"+str(act.get("concept_id")))
        flow.append("Apply: " + prompt)
        results.append({"title":str(act.get("title") or "Concept"),
                        "lines":flow,
                        "lab":str(act.get("lab_html") or ""),
                        "visual":str(act.get("visual_html") or ""),
                        "concept_id":str(act.get("concept_id") or ""), "apply_verified":True})
    if not results:raise RuntimeError("V18_NO_VERIFIED_CONCEPTS")
    return results

def render_v18_lesson(entry, theory, ev_map, lab_index=None):
    steps=_steps(theory)
    title=html.escape(str(entry.get("canonical_title") or theory.get("title") or "Lesson"))
    language=str(entry.get("language") or "en").lower()
    lang="ar" if language.startswith("ar") else ("fr" if language.startswith("fr") else "en")
    content=json.dumps(steps,ensure_ascii=False).replace("<","\\u003c").replace("&","\\u0026")
    card=theory.get("reference_card_html") or ""
    # Preserve the verified golden card, and put it LAST in the teaching sequence.
    if not card and theory.get("whole_lesson_lab_html"):
        # No invented golden card: final frame is explicitly a recap of audited steps.
        card=""
    result=json.dumps({"title":"Golden Final Card","lines":[s["title"]+": "+s["lines"][-1] for s in steps],
                        "lab":card,"visual":"","concept_id":"GOLDEN-FINAL-CARD"},ensure_ascii=False).replace("<","\\u003c")
    apply_markers = "".join(
        '<template data-step="application" data-concept-id="' +
        html.escape(row["concept_id"],quote=True) + '"></template>'
        for row in steps
    )
    lab_index_json = json.dumps(lab_index or {}, ensure_ascii=False).replace("<", "\\u003c")
    # Preserve the source-audited quiz block, with its original interactive markup.
    quiz_html = str(theory.get("quiz_html") or "")
    if theory.get("quiz_eligible_count", 0) and "fullQuizBlock" not in quiz_html:
        raise RuntimeError("V18_VERIFIED_FULL_QUIZ_MISSING")
    scripts=_script_bundle()
    page=r'''<!doctype html><html lang="__LANG__"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="nabil-v18-renderer" content="original-runtime-integrated"><meta name="nabil-renderer-contract" content="NABIL_REFERENCE_RENDERER_V1"><meta name="nabil-lesson-id" content="__ID__">
<title>__TITLE__ — NABIL V18</title><style>
:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#031025;color:#edf9ff;font-family:system-ui,Arial,sans-serif}
header{background:#071b33;border-bottom:1px solid #1f5c91;padding:15px 22px;display:flex;gap:16px;justify-content:space-between;flex-wrap:wrap;align-items:center}
.brand{color:#25d8ff;font-weight:900;letter-spacing:.06em}.wrap{max-width:1460px;margin:auto;padding:18px}
.layout{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,.8fr);gap:16px}.layout>*{min-width:0}html,body{width:100%;max-width:100%;overflow-x:clip}.panel{min-width:0;max-width:100%;overflow-wrap:anywhere}#board,#boardWriting,#visual,#timeline,#v18VerifiedQuiz{min-width:0;max-width:100%;overflow-wrap:anywhere}#v18VerifiedQuiz{overflow-x:auto}#v18VerifiedQuiz img,#v18VerifiedQuiz svg,#v18VerifiedQuiz canvas,#v18VerifiedQuiz iframe{max-width:100%;height:auto}#v18VerifiedQuiz table,#v18VerifiedQuiz pre{display:block;max-width:100%;overflow-x:auto}.panel{background:#071c35;border:1px solid #1f5c91;border-radius:18px;padding:18px}
#board{background:repeating-linear-gradient(0deg,#04172c,#04172c 39px,#0c2340 40px);border:2px solid #2087ad;border-radius:14px;min-height:380px;padding:26px;box-shadow:inset 0 0 28px #010917}
#boardTitle{color:#ffd35a;font-size:clamp(22px,3vw,35px);margin:0 0 18px}#boardWriting{font-size:clamp(19px,2vw,27px);line-height:1.9;white-space:pre-wrap;min-height:220px}
#visual{background:#04172c;border-radius:12px;margin-top:14px;min-height:160px;padding:10px;overflow:auto}
#visual iframe{width:100%;height:360px;border:0;background:#061725}.controls{display:flex;flex-wrap:wrap;gap:9px;margin-top:16px}
button{cursor:pointer;min-height:46px;border:1px solid #267aa9;border-radius:10px;background:#133b5e;color:white;font-weight:bold;padding:9px 13px}
button.primary{background:#0b766d}button:focus-visible{outline:3px solid #ffd35a}
#timeline{display:flex;flex-wrap:wrap;gap:7px;margin-top:15px}#timeline button.active{background:#b88c27;color:#051126}
#concepts{list-style:none;padding:0;margin:0;display:grid;gap:9px}#concepts li{padding:12px;background:#0b2b4c;border-left:4px solid #25d8ff;border-radius:7px}
#status{color:#52e6a4;font-size:14px}.tag{color:#9fc4e5;font-size:12px;letter-spacing:.1em}
@media(max-width:800px){.layout{grid-template-columns:1fr}.wrap{padding:9px}#board{min-height:280px;padding:14px}}
</style></head><body><header><div><div class="brand">NABIL AI · V18 GOLDEN SMART BOARD</div><h2>__TITLE__</h2></div><div id="status">Ready · Verified textbook material</div></header>
<main class="wrap" data-whole-lesson-smart-lab="true">__APPLY_MARKERS__<div class="layout"><section class="panel"><div class="tag">TEACH · WRITE · SPEAK · VISUALIZE · VERIFY</div>
<div id="board"><h2 id="boardTitle"></h2><div id="boardWriting" aria-live="polite"></div></div>
<div id="visual"></div><div class="controls">
<button class="primary" id="play">▶ Teach entire lesson</button><button id="current">🔊 Explain this concept</button>
<button id="prev">◀ Previous</button><button id="next">Next ▶</button><button id="stop">■ Stop</button>
<button id="restart">↻ Restart</button><button id="voice">🔊 Voice ON</button>
<button id="exercises">Exercises →</button></div><div id="timeline"></div></section>
<aside class="panel"><div class="brand">Lesson concepts</div><ul id="concepts"></ul><p class="tag">The final reference card appears LAST.</p></aside></div><section class="panel" id="v18VerifiedQuiz" style="margin-top:16px" hidden><h3>Check your understanding after the lesson</h3>__VERIFIED_QUIZ__</section></main>
<script type="application/json" id="nabilLabIndex">__LAB_INDEX__</script>
<script src="/static/nabil_browser_tts_v1.js?v=1"></script>
<script src="/static/nabil_lesson_e2e_runtime_v1.js?v=1"></script>
<script src="/static/nabil_scientific_solution_cards_e2e.js?v=1"></script>
__SCRIPTS__
<script>
(function(){
'use strict';
const slides=__STEPS__;slides.push(__FINAL__);
if(!window.NabilRuntime?.TeacherPlaybackController)throw Error('V18_RUNTIME_NOT_AVAILABLE');
let index=0,voiceEnabled=true;
const board=document.getElementById('boardWriting'),title=document.getElementById('boardTitle'),visual=document.getElementById('visual'),status=document.getElementById('status'),timeline=document.getElementById('timeline');
const ctl=new window.NabilRuntime.TeacherPlaybackController({langCode:'__LANG__',rate:0.82,
onStep:(i,step)=>show(step.fullIndex??i,true),onState:(s)=>{if(s.event==='WRITE_LINE'){board.textContent=s.value;}if(s.event==='WRITE_TITLE')title.textContent=s.value;
if(s.finished)status.textContent='Lesson complete · Golden card last';}});
const safeText=t=>document.createTextNode(t);
function show(i,fromPlayback=false){index=i;const x=slides[index];if(!fromPlayback)ctl.stop();title.textContent=x.title;board.textContent=x.lines.join('\n\n');visual.replaceChildren();
if(x.lab){const f=document.createElement('iframe');f.title=x.title+' — verified interactive lab';f.srcdoc='<!doctype html><html><head><meta charset="utf-8"><style>body{margin:0;background:#061725;color:white}</style></head><body>'+x.lab+'<\/body><\/html>';visual.appendChild(f);}
else if(x.visual){const holder=document.createElement('div');holder.innerHTML=x.visual;visual.appendChild(holder);}
else{const p=document.createElement('p');p.textContent=x.lines.join(' · ');visual.appendChild(p);}
Array.from(timeline.children).forEach((b,j)=>b.classList.toggle('active',j===i));
status.textContent=(i+1)+' / '+slides.length+' · '+x.title;document.getElementById('v18VerifiedQuiz').hidden=index!==slides.length-1;}
slides.forEach((x,i)=>{const b=document.createElement('button');b.textContent=i+1;b.onclick=()=>show(i);timeline.appendChild(b);
const li=document.createElement('li');li.textContent=(i+1)+'. '+x.title;document.getElementById('concepts').appendChild(li);});
document.addEventListener('nabil:page-language-change',e=>{const code=e.detail?.language||'en';ctl.setLanguage(code);});
document.getElementById('play').onclick=()=>{const from=index;ctl.play(slides.slice(from).map((step,k)=>({...step,fullIndex:from+k})),0)};
document.getElementById('current').onclick=()=>{const selected=index;ctl.stop();show(selected);ctl.play([slides[selected]],0)};
document.getElementById('next').onclick=()=>show(Math.min(slides.length-1,index+1));
document.getElementById('prev').onclick=()=>show(Math.max(0,index-1));
document.getElementById('stop').onclick=()=>ctl.stop();
document.getElementById('restart').onclick=()=>{show(0);ctl.play(slides,0)};
document.getElementById('voice').onclick=()=>{voiceEnabled=!voiceEnabled;ctl.setVoiceEnabled(voiceEnabled);document.getElementById('voice').textContent=voiceEnabled?'🔊 Voice ON':'🔇 Voice OFF'};
function navigateToExercises(){location.href=location.href.replace(/\\.html(?:\\?.*)?$/i,'--EXERCISES.html')};
document.getElementById('exercises').onclick=()=>{location.href=location.href.replace(/\.html(?:\?.*)?$/i,'--EXERCISES.html')};
show(0);
})();
</script></body></html>'''
    return (page.replace("__LANG__",lang).replace("__ID__",html.escape(str(entry.get("lesson_id") or "")))
            .replace("__TITLE__",title).replace("__SCRIPTS__",scripts)
            .replace("__STEPS__",content).replace("__FINAL__",result).replace("__APPLY_MARKERS__",apply_markers).replace("__LAB_INDEX__",lab_index_json).replace("__VERIFIED_QUIZ__",quiz_html))
