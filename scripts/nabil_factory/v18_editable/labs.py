"""NABIL V18 — audited interactive labs for lessons AND exercises.

Preserves real source-verified interactive HTML and scientific card specifications;
adds the V18 slow teaching, step controls, speech and progressive result gating.
No fabricated subject simulations, translation or result is introduced.
"""
from __future__ import annotations
import html
import json
import re

CONFIG = {"exercise_inline": True, "auto_scroll": True, "audio_on_open": False,
          "offline_browser_fallback": True, "guided_reveal": True,
          "whole_lesson_lab": True, "applies_to_exercises": True,
          "strict_verified_source": True}

_CSS = r"""<style>
.v18-lab-panel{background:linear-gradient(180deg,#082447,#061a32);color:#f7fbff;border:1px solid #1e6aa4;border-radius:16px;padding:14px;margin:12px 0;min-width:0}
.v18-lab-heading{color:#25d8ff;margin:0 0 9px}.v18-lab-progress{color:#ffd35a;font-weight:700}.v18-lab-teaching{white-space:pre-wrap;min-height:42px;font-size:1.1rem;line-height:1.6;margin:12px 0}
.v18-lab-stage{min-height:160px;background:#04172c;border:1px solid #1f5c91;border-radius:12px;overflow:auto;padding:9px}
.v18-lab-frame{width:100%;min-height:340px;border:0;border-radius:9px;background:#061a30}
.v18-lab-controls{display:flex;gap:7px;flex-wrap:wrap;margin:12px 0}.v18-lab-button{cursor:pointer;background:#123c63;color:white;border:1px solid #2b6c9c;border-radius:9px;padding:9px 11px;min-height:42px}.v18-lab-button:focus-visible{outline:3px solid #ffd35a}
.v18-lab-result{border-left:4px solid #52e6a4;padding:8px;margin-top:9px}.v18-lab-apply{border-left:4px solid #ffd35a;padding:8px}
@media(max-width:760px){.v18-lab-panel{padding:10px}.v18-lab-frame{min-height:280px}}
</style>"""
_JS = '(()=>{\n\'use strict\';\nconst ROOT=document.currentScript?.previousElementSibling;\nif(!ROOT||!ROOT.matches(\'[data-v18-lab-payload]\'))return;\nlet data;try{data=JSON.parse(ROOT.textContent)}catch(e){console.error(\'V18_LAB_DATA_INVALID\',e);return}\nconst uid=ROOT.dataset.v18LabPayload;\nconst host=document.querySelector(\'[data-v18-lab-host="\'+uid+\'"]\');if(!host)return;\nconst ui={\n en:{start:\'▶ Start experiment\',pause:\'Ⅱ Pause\',resume:\'▶ Resume\',reset:\'↻ Restart\',previous:\'◀ Previous\',next:\'Next ▶\',listen:\'🔊 Explain\',stop:\'■ Stop voice\',unavailable:\'No verified experiment was provided for this concept.\',result:\'Verified result\',apply:\'Try it\',finish:\'Experiment complete\',steps:\'Teaching steps\',experiment:\'Interactive experiment\'},\n ar:{start:\'▶ ابدأ التجربة\',pause:\'Ⅱ إيقاف مؤقت\',resume:\'▶ متابعة\',reset:\'↻ إعادة\',previous:\'◀ السابق\',next:\'التالي ▶\',listen:\'🔊 شرح صوتي\',stop:\'■ إيقاف الصوت\',unavailable:\'لا توجد تجربة موثّقة لهذا المفهوم.\',result:\'النتيجة الموثّقة\',apply:\'طبّق\',finish:\'اكتملت التجربة\',steps:\'خطوات التعلم\',experiment:\'مختبر تفاعلي\'},\n fr:{start:\'▶ Démarrer\',pause:\'Ⅱ Pause\',resume:\'▶ Reprendre\',reset:\'↻ Recommencer\',previous:\'◀ Précédent\',next:\'Suivant ▶\',listen:\'🔊 Expliquer\',stop:\'■ Arrêter la voix\',unavailable:\'Aucune expérience vérifiée pour ce concept.\',result:\'Résultat vérifié\',apply:\'À vous\',finish:\'Expérience terminée\',steps:\'Étapes pédagogiques\',experiment:\'Laboratoire interactif\'}\n};\nlet language=[\'ar\',\'en\',\'fr\'].includes(data.language)?data.language:\'en\';\nfunction tr(x){if(x&&typeof x===\'object\'&&!Array.isArray(x))return String(x[language]||x[data.source_language]||\'\');return String(x??\'\')}\nfunction textLang(x){if(x&&typeof x===\'object\'&&!Array.isArray(x)){return x[language]?language:data.source_language}return data.source_language}\nfunction say(s,lang=language){if(!s)return;if(!(\'speechSynthesis\'in window)){return}stopVoice();const u=new SpeechSynthesisUtterance(s);u.lang={ar:\'ar\',en:\'en\',fr:\'fr\'}[lang];u.rate=.82;try{speechSynthesis.speak(u)}catch(_){}}\nfunction stopVoice(){try{speechSynthesis.cancel()}catch(_){}}\nfunction el(tag,cls,text){const n=document.createElement(tag);if(cls)n.className=cls;if(text!=null)n.textContent=text;return n}\nfunction control(label,action){const b=el(\'button\',\'v18-lab-button\',label);b.type=\'button\';b.addEventListener(\'click\',action);return b}\nfunction panelForLab(item,mount){mount.replaceChildren();const spec=item.lab_spec;\n // Preserve simulations from the audited factory as executable isolated documents.\n if(item.lab_html){const frame=el(\'iframe\',\'v18-lab-frame\');frame.title=tr(item.title);frame.setAttribute(\'sandbox\',\'allow-scripts\');frame.srcdoc=\'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{margin:8px;background:#061a30;color:#f1faff;font:16px system-ui}button,input,select{font:inherit}</style></head><body>\'+item.lab_html+\'</bo\'+\'dy></ht\'+\'ml>\';mount.append(frame);return true}\n if(spec&&spec.kind==="EVIDENCE_REVEAL"&&spec.evidence_ref&&spec.evidence_quote){\n  const box=el(\'div\',\'v18-evidence\');box.setAttribute(\'data-evidence-ref\',spec.evidence_ref);\n  const button=control(language===\'ar\'?\'🔎 أظهر الدليل\':language===\'fr\'?\'🔎 Montrer la preuve\':\'🔎 Reveal evidence\',()=>{quote.hidden=!quote.hidden});\n  const quote=el(\'blockquote\',\'v18-evidence-quote\',spec.evidence_quote);quote.hidden=true;\n  box.append(button,quote);mount.append(box);return true;\n }\n // Render V18 scientific drawings/cards when available. This is not an invented simulation.\n if(spec&&window.NABILScientificCards?.renderCard){const normalized={...spec,language,subject:item.subject||spec.subject};window.NABILScientificCards.renderCard(normalized,mount);return true}\n if(spec&&Array.isArray(spec.drawings)&&typeof window.renderNabilDiagram===\'function\'){\n  for(const drawing of spec.drawings){const visual=window.renderNabilDiagram(drawing);if(visual){const d=el(\'div\');d.innerHTML=visual;mount.append(d)}}\n  if(mount.children.length)return true;\n }\n if(item.visual_html){const f=el(\'iframe\',\'v18-lab-frame\');f.title=tr(item.title);f.setAttribute(\'sandbox\',\'allow-scripts\');f.srcdoc=\'<!doctype html><html><body>\'+item.visual_html+\'</bo\'+\'dy></ht\'+\'ml>\';mount.append(f);return true}\n return false;\n}\nfunction setup(item){let position=0,finished=false,running=false,abort=0,stageMounted=false;const shell=el(\'section\',\'v18-lab-panel\'),heading=el(\'h3\',\'v18-lab-heading\',tr(item.title)),stage=el(\'div\',\'v18-lab-stage\'),lesson=el(\'div\',\'v18-lab-teaching\'),progress=el(\'div\',\'v18-lab-progress\'),results=el(\'div\',\'v18-lab-result\'),apply=el(\'div\',\'v18-lab-apply\'),bar=el(\'div\',\'v18-lab-controls\');\n shell.lang=language;shell.dir=language===\'ar\'?\'rtl\':\'ltr\';shell.dataset.conceptId=item.id;shell.dataset.v18Context=data.context;\n const buttons={};const t=()=>ui[language];\n function halt(){running=false;abort++;buttons.start.textContent=t().start;stopVoice()}\n function render(){shell.lang=language;shell.dir=language===\'ar\'?\'rtl\':\'ltr\';heading.textContent=tr(item.title);const lines=item.steps||[];progress.textContent=lines.length?`${Math.min(position+1,lines.length)} / ${lines.length}`:\'\';lesson.textContent=lines.length?tr(lines[Math.min(position,lines.length-1)]):\'\';\n  results.replaceChildren();if(finished&&tr(item.conclusion)){results.append(el(\'strong\',null,t().result+\': \'),el(\'span\',null,tr(item.conclusion)))}\n  apply.replaceChildren();if(finished&&tr(item.prompt)){apply.append(el(\'strong\',null,t().apply+\': \'),el(\'span\',null,tr(item.prompt)))}\n  buttons.start.textContent=running?t().pause:t().start;buttons.prev.textContent=t().previous;buttons.next.textContent=t().next;buttons.reset.textContent=t().reset;buttons.listen.textContent=t().listen;buttons.stop.textContent=t().stop;\n  buttons.prev.disabled=position===0;buttons.next.disabled=running||finished||position>=lines.length-1;\n  if(!stageMounted){stageMounted=true;if(!panelForLab(item,stage))stage.textContent=t().unavailable;}\n }\n async function play(){if(running){halt();render();return}if(finished){position=0;finished=false}running=true;const run=++abort;buttons.start.textContent=t().pause;const lines=item.steps||[];\n  while(running&&run===abort&&position<lines.length){render();say(tr(lines[position]),textLang(lines[position]));const wait=Math.min(14000,Math.max(1800,tr(lines[position]).length*75));let elapsed=0;while(running&&run===abort&&elapsed<wait){await new Promise(r=>setTimeout(r,100));elapsed+=100}if(!running||run!==abort)break;position++}\n  if(running&&run===abort){finished=true;position=Math.max(0,lines.length-1);running=false;stopVoice();render();shell.dispatchEvent(new CustomEvent(\'nabil:v18-lab-finished\',{bubbles:true,detail:{concept_id:item.id,context:data.context}}))}\n }\n buttons.start=control(t().start,play);buttons.prev=control(t().previous,()=>{halt();position=Math.max(0,position-1);finished=false;render()});buttons.next=control(t().next,()=>{halt();position=Math.min((item.steps||[]).length-1,position+1);finished=false;render()});buttons.reset=control(t().reset,()=>{halt();position=0;finished=false;render()});buttons.listen=control(t().listen,()=>say(tr((item.steps||[])[position]),textLang((item.steps||[])[position])));buttons.stop=control(t().stop,stopVoice);\n Object.values(buttons).forEach(b=>bar.append(b));shell.append(heading,progress,lesson,stage,bar,results,apply);host.append(shell);\n shell.addEventListener(\'nabil:v18-lab-language\',()=>{halt();stageMounted=false;render()});render();\n return {shell,halt,render};}\nconst nodes=data.activities.map(setup);const setLanguage=lang=>{if(!ui[lang])return;language=lang;nodes.forEach(n=>n.shell.dispatchEvent(new Event(\'nabil:v18-lab-language\')))};\ndocument.addEventListener(\'nabil:page-language-change\',e=>setLanguage(e.detail?.language||e.detail?.lang));\ndocument.addEventListener(\'nabil:v18-set-language\',e=>setLanguage(e.detail?.language));\nwindow.NABILV18Labs=window.NABILV18Labs||{setLanguage:(lang)=>document.dispatchEvent(new CustomEvent(\'nabil:v18-set-language\',{detail:{language:lang}}))};\n})();'

def _localized(value):
    if isinstance(value, dict):
        return {k: str(v) for k,v in value.items() if k in ("ar","en","fr") and v is not None}
    return str(value or "")

def _lines(activity):
    steps = []
    for row in activity.get("teaching_steps") or []:
        if isinstance(row, dict):
            for key in ("sentence_i18n", "sentence", "formula", "label"):
                if row.get(key): steps.append(_localized(row[key]))
        elif row: steps.append(_localized(row))
    if not steps:
        for key in ("phenomenon", "investigation", "observation", "interpretation", "conclusion"):
            if activity.get(key): steps.append(_localized(activity[key]))
    return steps

def _indexed_lab(row, lab_index):
    """Resolve a V17.7 prebuilt verified lab, never generate new scientific claims."""
    if not isinstance(lab_index, dict):
        return {}
    keys = [row.get('_prebuilt_lab_key'), row.get('lab_key')]
    rid = row.get('concept_id') or row.get('exercise_id') or row.get('id')
    keys.extend(('concept:' + str(rid), 'exercise:' + str(rid), str(rid)))
    for key in keys:
        match = lab_index.get(str(key)) if key else None
        if isinstance(match, dict) and match.get('active', True) is not False:
            return match
    return {}


def _verified_evidence(row, linked):
    """Create an evidence exploration, not a simulated experiment.

    Source evidence must already be supplied and explicitly source-linked by
    the audited producer; never invent a figure, value, physical behaviour,
    or translated text.
    """
    for obj in (row, linked):
        if not isinstance(obj, dict):
            continue
        ref = str(obj.get("evidence_ref") or obj.get("source_evidence_id") or "").strip()
        quote = str(obj.get("evidence_quote") or obj.get("verified_source_text") or "").strip()
        if ref and quote:
            return {"kind": "EVIDENCE_REVEAL", "evidence_ref": ref,
                    "evidence_quote": quote[:5000], "prebuilt": True,
                    "supported": True}
    return None


def _normalize(activities, context, lab_index=None):
    rows=[]
    for row in activities or []:
        if not isinstance(row, dict): continue
        linked = _indexed_lab(row, lab_index)
        source = (row.get("lab_html") or row.get("_prebuilt_lab_html")
                  or row.get("interactive_html") or linked.get("html")
                  or linked.get("lab_html") or linked.get("interactive_html") or "")
        spec = row.get("lab_spec") or row.get("scientific_lab_spec") or row.get("verified_lab_spec") or row.get("solution_card") or linked.get("spec") or linked.get("lab_spec")
        visual = row.get("visual_html") or linked.get("visual_html") or ""
        if isinstance(spec,dict):
            # Allow the audited factory to certify evidence; do not auto-assert verification.
            json.dumps(spec,ensure_ascii=False)
        else: spec=None
        if not (source or spec or visual):
            spec = _verified_evidence(row, linked)
        if not (source or spec or visual):
            # No trustworthy evidence is not permission to fabricate a lab.
            continue
        if row.get("_exercise_render_rejected") or row.get("scientific_review_rejected"): continue
        cid=str(row.get("concept_id") or row.get("exercise_id") or row.get("id") or "").strip()
        if not cid: raise RuntimeError("V18_LAB_CONCEPT_ID_REQUIRED")
        title=_localized(row.get("title_i18n") or row.get("title_translations") or row.get("title") or row.get("question") or cid)
        apply=row.get("student_apply_prompt") or row.get("student_question") or {}
        prompt=_localized(apply.get("prompt_translations") or apply.get("prompt_i18n") or apply.get("prompt") or apply.get("q") or row.get("prompt_translations") or row.get("prompt") or "") if isinstance(apply,dict) else ""
        steps=_lines(row)
        if isinstance(row.get("localized_lines"),dict) and steps:
            localized=row["localized_lines"]
            if all(isinstance(localized.get(lang),list) and len(localized[lang])==len(steps) for lang in localized if lang in ("ar","en","fr")):
                steps=[{lang:str(localized[lang][i]) for lang in ("ar","en","fr") if lang in localized} for i in range(len(steps))]
        if not steps and context=="exercise":
            for item in row.get("solution_steps") or []:
                if item:steps.append(_localized(item.get("text") or item.get("sentence")) if isinstance(item,dict) else _localized(item))
        if not steps and isinstance(spec,dict) and spec.get("kind")=="EVIDENCE_REVEAL":
            steps = [str(spec["evidence_quote"])]
        if not steps: raise RuntimeError("V18_LAB_VERIFIED_TEACHING_STEPS_MISSING:"+cid)
        rows.append({"id":cid,"title":title,"steps":steps,"prompt":prompt,
                     "conclusion":_localized(row.get("conclusion_translations") or row.get("conclusion_i18n") or row.get("conclusion") or row.get("result") or ""),
                     "subject":str(row.get("subject") or ""),"lab_html":str(source),
                     "visual_html":str(visual),"lab_spec":spec})
    return rows

def render_verified_labs(activities, *, context="lesson", language="en", lab_index=None, source_language=None):
    """Emit working V18 labs for lesson concepts or verified exercises.

    The returned fragment includes isolated lab HTML, teaching steps, controls,
    voice and scientific visual/card hooks. Interactive content must come from
    the vetted factory; the module does not manufacture textbook evidence.
    """
    if context not in ("lesson","exercise"):
        raise ValueError("V18_LAB_INVALID_CONTEXT")
    if language not in ("en","ar","fr"):
        raise ValueError("V18_LAB_INVALID_LANGUAGE")
    rows=_normalize(activities,context,lab_index)
    if not rows:return ""
    import hashlib
    payload={"activities":rows,"context":context,"language":language,"source_language":source_language if source_language in ("ar","en","fr") else language}
    uid=hashlib.sha256(json.dumps(payload,ensure_ascii=False,sort_keys=True).encode()).hexdigest()[:16]
    raw=json.dumps(payload,ensure_ascii=False,separators=(",",":")).replace("<","\\u003c").replace(">","\\u003e").replace("&","\\u0026")
    # No remote libraries and no dependency on a global page script.
    return (_CSS+'<div data-v18-lab-host="'+uid+'"></div>'
            +'<script type="application/json" data-v18-lab-payload="'+uid+'">'+raw+'</script>'
            +'<script>'+_JS.replace("</script", "<\/script")+'</script>')

def render_exercise_labs(exercises, *, language="en", lab_index=None, source_language=None):
    """V18 labs adjacent to every evidence-backed verified exercise."""
    return render_verified_labs(exercises, context="exercise",
                                language=language, lab_index=lab_index, source_language=source_language)


def render_lesson_and_exercise_labs(activities, exercises, *, language="en", lab_index=None, source_language=None):
    """Produce both contexts with consistent source lab lookup."""
    return (render_verified_labs(activities, context="lesson",language=language,lab_index=lab_index,source_language=source_language),
            render_exercise_labs(exercises,language=language,lab_index=lab_index,source_language=source_language))

__all__ = ["CONFIG", "render_verified_labs", "render_exercise_labs", "render_lesson_and_exercise_labs"]
