#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Evidence-gated advanced Physics/Chemistry lab renderers for NABIL AI.

The lesson factory may select these renderers only after the corresponding
scientific claims are verified against textbook evidence. The renderers then
enforce deterministic invariants so presentation cannot contradict the lesson.

Key guards:
- OPEN DC switch => zero loop current and no current animation.
- Reflection angles are measured from the normal; theta_i == theta_r.
- Ionic animation requires a charge-neutral ion ratio and a consistent number
  of transferred electrons.
- A synchronized teacher pointer follows the concept being narrated.
"""
from __future__ import annotations

import html
import json
import math
import re
from typing import Any, Dict, Tuple

try:
    from scripts.nabil_geometry_lab import validate_geometry_proof_spec, render_geometry_proof_lab
except Exception:
    from nabil_geometry_lab import validate_geometry_proof_spec, render_geometry_proof_lab

ADVANCED_LAB_KINDS = {
    "DC_SERIES_CIRCUIT",
    "OPTICS_REFLECTION",
    "IONIC_COMPOUND",
    "GEOMETRY_PROOF",
}


def _safe_id(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_]", "_", str(value or "lab"))


def _labels(lang: str) -> Dict[str, str]:
    if lang == "ar":
        return {
            "close": "أغلق المفتاح", "open": "افتح المفتاح",
            "switch_open": "المفتاح مفتوح — لا يمر تيار كهربائي",
            "switch_closed": "المفتاح مغلق — يمر تيار كهربائي",
            "source_voltage": "توتر المصدر",
            "explain": "▶ اشرح من البداية", "stop": "■ أوقف الشرح",
            "drag_source": "حرّك مصدر الضوء",
            "transfer": "⚡ نفّذ انتقال الإلكترونات",
            "reset": "↺ أعد التجربة",
        }
    if lang == "fr":
        return {
            "close": "Fermer l’interrupteur", "open": "Ouvrir l’interrupteur",
            "switch_open": "OPEN — aucun courant",
            "switch_closed": "CLOSED — courant présent",
            "source_voltage": "Tension de la source",
            "explain": "▶ Expliquer depuis le début", "stop": "■ Arrêter",
            "drag_source": "Déplace la source lumineuse",
            "transfer": "⚡ Exécuter le transfert d’électrons",
            "reset": "↺ Réinitialiser",
        }
    return {
        "close": "Close switch", "open": "Open switch",
        "switch_open": "OPEN — no current",
        "switch_closed": "CLOSED — current flows",
        "source_voltage": "Source voltage",
        "explain": "▶ Explain from the beginning", "stop": "■ Stop explanation",
        "drag_source": "Drag the light source",
        "transfer": "⚡ Run electron transfer", "reset": "↺ Reset",
    }


def validate_advanced_lab_spec(spec: Dict[str, Any]) -> Dict[str, Any]:
    kind = str(spec.get("kind") or "").strip().upper()
    if kind not in ADVANCED_LAB_KINDS:
        return spec

    if kind == "DC_SERIES_CIRCUIT":
        resistors = spec.get("resistors")
        rules = spec.get("rules") or {}
        if not isinstance(resistors, list) or len(resistors) != 2:
            raise RuntimeError("LAB_CIRCUIT_REQUIRES_TWO_SERIES_RESISTORS")
        if any(not str(v or "").strip() for v in resistors):
            raise RuntimeError("LAB_CIRCUIT_RESISTOR_NAME_INVALID")
        if spec.get("switch_control") is not True:
            raise RuntimeError("LAB_CIRCUIT_SWITCH_REQUIRED")
        for rule in ("series_resistance_sum", "series_same_current", "ohms_law", "open_switch_zero_current"):
            if rules.get(rule) is not True:
                raise RuntimeError(f"LAB_CIRCUIT_SCIENTIFIC_RULE_MISSING:{rule}")
        if any(k in spec for k in ("min", "max", "default", "initial", "step")):
            raise RuntimeError("LAB_CIRCUIT_FAKE_RANGE_FORBIDDEN")

    elif kind == "OPTICS_REFLECTION":
        if spec.get("angles_measured_from_normal") is not True:
            raise RuntimeError("LAB_OPTICS_ANGLE_REFERENCE_MUST_BE_NORMAL")
        if spec.get("normal_perpendicular_surface") is not True:
            raise RuntimeError("LAB_OPTICS_NORMAL_MUST_BE_PERPENDICULAR")
        if str(spec.get("law") or "").strip().lower() != "angle_of_incidence_equals_angle_of_reflection":
            raise RuntimeError("LAB_OPTICS_REFLECTION_LAW_INVALID")

    elif kind == "IONIC_COMPOUND":
        cation = spec.get("cation") or {}
        anion = spec.get("anion") or {}
        try:
            cq = int(cation.get("charge"))
            aq = int(anion.get("charge"))
            cr = int(spec.get("cation_ratio"))
            ar = int(spec.get("anion_ratio"))
            transfer = int(spec.get("electron_transfer_count"))
        except Exception as exc:
            raise RuntimeError("LAB_IONIC_NUMERIC_SPEC_INVALID") from exc
        if cq <= 0 or aq >= 0:
            raise RuntimeError("LAB_IONIC_CHARGE_SIGN_INVALID")
        if not (1 <= cr <= 4 and 1 <= ar <= 4):
            raise RuntimeError("LAB_IONIC_RATIO_UNSUPPORTED")
        if not str(cation.get("symbol") or "").strip() or not str(anion.get("symbol") or "").strip():
            raise RuntimeError("LAB_IONIC_SYMBOL_MISSING")
        if str(spec.get("bond_type") or "").strip().lower() != "ionic":
            raise RuntimeError("LAB_IONIC_BOND_TYPE_INVALID")
        net = cr * cq + ar * aq
        if net != 0:
            raise RuntimeError(f"LAB_IONIC_CHARGE_NOT_NEUTRAL:net={net}")
        expected = cr * cq
        if transfer != expected or transfer != ar * abs(aq):
            raise RuntimeError(
                f"LAB_IONIC_ELECTRON_TRANSFER_INCONSISTENT:declared={transfer}:expected={expected}"
            )
        if transfer > 8:
            raise RuntimeError("LAB_IONIC_TRANSFER_COUNT_UNSUPPORTED")

    elif kind == "GEOMETRY_PROOF":
        validate_geometry_proof_spec(spec)

    return spec


def _voice_helpers(lang: str) -> str:
    return f"""
      const teacherLang={json.dumps(lang)};
      let teacherToken=0,teacherTimer=0;
      function teacherStop(){{
        teacherToken++;
        if(teacherTimer){{clearTimeout(teacherTimer);teacherTimer=0;}}
        try{{window.NABILLessonE2E?.stopSpeech?.();}}catch(_e){{}}
        try{{window.NABILBrowserTTS?.stop?.();}}catch(_e){{}}
        try{{window.speechSynthesis?.cancel?.();}}catch(_e){{}}
      }}
      function teacherSpeakCue(text,target,onDone){{
        const token=teacherToken;
        pointTeacher(target);
        const finish=()=>{{if(token===teacherToken&&onDone)onDone();}};
        try{{
          if(window.NABILLessonE2E?.speak){{
            Promise.resolve(window.NABILLessonE2E.speak(text,teacherLang)).then(finish).catch(finish);
            return;
          }}
          if(window.NABILBrowserTTS?.speak){{
            Promise.resolve(window.NABILBrowserTTS.speak(text,teacherLang)).then(finish).catch(finish);
            return;
          }}
        }}catch(_e){{}}
        const words=String(text||'').trim().split(/\\s+/).filter(Boolean).length;
        teacherTimer=setTimeout(finish,Math.max(1700,words*390));
      }}
      function playTeacherCues(cues,onComplete){{
        teacherStop();
        const token=teacherToken;
        let i=0;
        const next=()=>{{
          if(token!==teacherToken)return;
          if(i>=cues.length){{if(onComplete)onComplete();return;}}
          const cue=cues[i++];
          teacherSpeakCue(cue.text,cue.target,next);
        }};
        next();
      }}
    """


def _render_circuit(spec: Dict[str, Any], lang: str, lab_id: str) -> str:
    safe = _safe_id(lab_id)
    L = _labels(lang)
    r1 = html.escape(str(spec["resistors"][0]))
    r2 = html.escape(str(spec["resistors"][1]))
    if lang == "ar":
        cues = [
            {"target": "switch", "text": "أولًا ننظر إلى المفتاح. إذا كان مفتوحًا فالدارة مفتوحة، ولذلك لا يمر تيار كهربائي."},
            {"target": "r1", "text": f"هذه هي {r1}. وهي موصولة على التوالي مع المقاومة الثانية."},
            {"target": "r2", "text": f"وهذه هي {r2}. في التوصيل على التوالي يمر التيار الكهربائي نفسه في المقاومتين عندما يكون المفتاح مغلقًا."},
            {"target": "path", "text": "الآن نغلق المفتاح أولًا. يصبح المسار الكهربائي كاملًا، وعندها فقط نُظهر حركة التيار الكهربائي في الدارة.", "state": "closed"},
        ]
    elif lang == "fr":
        cues = [
            {"target": "switch", "text": "On commence par l’interrupteur. S’il est ouvert, le circuit est ouvert et aucun courant ne circule."},
            {"target": "r1", "text": f"Voici {r1}, la première résistance en série."},
            {"target": "r2", "text": f"Voici {r2}. En série, le même courant traverse les deux résistances lorsque l’interrupteur est fermé."},
            {"target": "path", "text": "On ferme d’abord l’interrupteur. Le trajet devient complet et seulement alors le courant peut circuler.", "state": "closed"},
        ]
    else:
        cues = [
            {"target": "switch", "text": "First inspect the switch. When it is open, the circuit is open and no current flows."},
            {"target": "r1", "text": f"This is {r1}, the first series resistor."},
            {"target": "r2", "text": f"This is {r2}. In series, the same current passes through both resistors when the switch is closed."},
            {"target": "path", "text": "First close the switch. That completes the path, and only then is current animation allowed.", "state": "closed"},
        ]

    return f"""
<section class="interactive-lab nabil-science-lab" id="lab_{safe}"
 data-lab-kind="DC_SERIES_CIRCUIT" data-teacher-pointer="synced" data-demo-ms="11000"
 data-science-rule="OPEN_CIRCUIT_ZERO_CURRENT;CURRENT_REQUIRES_CLOSED_SWITCH;SERIES_SAME_CURRENT"
 style="margin-top:16px;background:#071827;color:#f8fafc;border:1px solid #24506f;border-radius:14px;padding:16px;">
 <h3 style="margin-top:0;color:#2de1ff;">{html.escape(str(spec["title"]))}</h3>
 <p>{html.escape(str(spec["instructions"]))}</p>
 <svg id="{safe}_svg" viewBox="0 0 620 360" style="width:100%;max-width:720px;touch-action:none;background:#030b14;border-radius:12px;">
  <defs><marker id="{safe}_arrowHead" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3z" fill="#2de1ff"/></marker></defs>
  <path id="{safe}_path" d="M90 90 H520 V285 H90 Z" fill="none" stroke="#b6c8d8" stroke-width="5"/>
  <path id="{safe}_current" d="M90 90 H520 V285 H90 Z" fill="none" stroke="#22c55e" stroke-width="5" stroke-dasharray="3 18" style="opacity:.05;animation:none;"/>
  <line x1="90" y1="145" x2="90" y2="225" stroke="#facc15" stroke-width="7"/><line x1="72" y1="160" x2="72" y2="210" stroke="#facc15" stroke-width="3"/>
  <g id="{safe}_r1"><path d="M190 90 l12 -18 l18 36 l18 -36 l18 36 l18 -36 l12 18" fill="none" stroke="#fb7185" stroke-width="5"/><text x="208" y="58" fill="#fb7185" font-size="15" font-weight="700">{r1}</text></g>
  <g id="{safe}_r2"><path d="M330 285 l12 -18 l18 36 l18 -36 l18 36 l18 -36 l12 18" fill="none" stroke="#c084fc" stroke-width="5"/><text x="350" y="335" fill="#c084fc" font-size="15" font-weight="700">{r2}</text></g>
  <g id="{safe}_switch" style="cursor:pointer"><circle cx="520" cy="170" r="7" fill="#fff"/><circle cx="520" cy="220" r="7" fill="#fff"/>
   <line id="{safe}_lever" x1="520" y1="170" x2="494" y2="210" stroke="#fff" stroke-width="5"/>
   <text id="{safe}_switchText" x="535" y="199" fill="#facc15" font-size="12" font-weight="700">OPEN</text></g>
  <line id="{safe}_teacherArrow" x1="600" y1="48" x2="520" y2="190" stroke="#2de1ff" stroke-width="3" stroke-dasharray="8 6" marker-end="url(#{safe}_arrowHead)"/>
 </svg>
 <div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-top:10px;">
  <label>{html.escape(L["source_voltage"])} V<input id="{safe}_V" type="number" inputmode="decimal" style="width:100%;padding:8px;"></label>
  <label>{r1} Ω<input id="{safe}_R1" type="number" inputmode="decimal" style="width:100%;padding:8px;"></label>
  <label>{r2} Ω<input id="{safe}_R2" type="number" inputmode="decimal" style="width:100%;padding:8px;"></label>
 </div>
 <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:10px;">
  <button type="button" id="{safe}_toggle">{html.escape(L["close"])}</button>
  <button type="button" id="{safe}_teach">{html.escape(L["explain"])}</button>
  <button type="button" id="{safe}_stop">{html.escape(L["stop"])}</button>
 </div>
 <div id="{safe}_status" aria-live="polite" style="margin-top:10px;font-weight:700;">{html.escape(L["switch_open"])}</div>
 <div id="{safe}_result" style="margin-top:8px;padding:10px;background:#fff;border-radius:8px;color:#0f172a;"></div>
 <p style="font-size:12px;color:#b6c8d8;">{html.escape(str(spec["observation"]))}</p>
 <script>
 (()=>{{
   const q=id=>document.getElementById(id);let switchClosed=false;
   const current=q('{safe}_current'),lever=q('{safe}_lever'),status=q('{safe}_status'),toggle=q('{safe}_toggle'),result=q('{safe}_result'),teacher=q('{safe}_teacherArrow');
   const targets={{switch:[520,190],r1:[245,90],r2:[385,285],path:[500,90]}};
   function pointTeacher(name){{const p=targets[name]||targets.path;teacher.setAttribute('x2',p[0]);teacher.setAttribute('y2',p[1]);}}
   {_voice_helpers(lang)}
   function n(id){{const v=Number(q(id).value);return Number.isFinite(v)&&v>0?v:NaN;}}
   function calculate(){{
     const V=n('{safe}_V'),R1=n('{safe}_R1'),R2=n('{safe}_R2');
     if(!Number.isFinite(V)||!Number.isFinite(R1)||!Number.isFinite(R2)){{result.textContent='—';return;}}
     const Rt=R1+R2,I=switchClosed?V/Rt:0,V1=switchClosed?I*R1:0,V2=switchClosed?I*R2:0,Vswitch=switchClosed?0:V;
     result.textContent='Rtotal = '+Rt.toFixed(3)+' Ω · I = '+I.toFixed(3)+' A · V1 = '+V1.toFixed(3)+' V · V2 = '+V2.toFixed(3)+' V · Vswitch = '+Vswitch.toFixed(3)+' V';
   }}
   function renderSwitch(){{
     q('lab_{safe}').dataset.switchState=switchClosed?'closed':'open';
     if(switchClosed){{
       lever.setAttribute('x2','520');lever.setAttribute('y2','220');lever.setAttribute('stroke','#22c55e');
       q('{safe}_switchText').textContent='CLOSED';q('{safe}_switchText').setAttribute('fill','#22c55e');
       current.style.opacity='1';current.style.animation='{safe}_flow 1s linear infinite';
       toggle.textContent={json.dumps(L["open"])};status.textContent={json.dumps(L["switch_closed"])};
     }}else{{
       lever.setAttribute('x2','494');lever.setAttribute('y2','210');lever.setAttribute('stroke','#fff');
       q('{safe}_switchText').textContent='OPEN';q('{safe}_switchText').setAttribute('fill','#facc15');
       current.style.opacity='.05';current.style.animation='none';
       toggle.textContent={json.dumps(L["close"])};status.textContent={json.dumps(L["switch_open"])};
     }}
     calculate();
   }}
   function applyTeacherState(detail){{
     const after=(detail&&detail.state_after)||{{}};
     if(Object.prototype.hasOwnProperty.call(after,'switch_closed')){{
       switchClosed=Boolean(after.switch_closed);renderSwitch();
     }}
   }}
   const style=document.createElement('style');style.textContent='@keyframes {safe}_flow{{to{{stroke-dashoffset:-42}}}} @keyframes {safe}_pointer{{to{{stroke-dashoffset:-28}}}} #{safe}_teacherArrow{{animation:{safe}_pointer .85s linear infinite}}';document.head.appendChild(style);
   q('{safe}_switch').addEventListener('click',()=>{{teacherStop();switchClosed=!switchClosed;pointTeacher('switch');renderSwitch();}});
   toggle.addEventListener('click',()=>{{teacherStop();switchClosed=!switchClosed;pointTeacher('switch');renderSwitch();}});
   const runDemo=()=>{{
     switchClosed=false;renderSwitch();
     const demoCues={json.dumps(cues,ensure_ascii=False)};
     teacherStop();const token=teacherToken;let i=0;
     q('lab_{safe}').dispatchEvent(new CustomEvent('nabil:teacher-start',{{detail:{{labRef:'{safe}',stepCount:demoCues.length}},bubbles:true}}));
     const next=()=>{{
       if(token!==teacherToken)return;
       if(i>=demoCues.length){{
         q('lab_{safe}').dispatchEvent(new CustomEvent('nabil:teacher-complete',{{detail:{{labRef:'{safe}',stepCount:demoCues.length}},bubbles:true}}));return;
       }}
       const cue=demoCues[i++];
       if(cue.state==='closed'){{switchClosed=true;renderSwitch();}}
       teacherSpeakCue(cue.text,cue.target,next);
     }};next();
   }};
   q('{safe}_teach').addEventListener('click',runDemo);
   q('{safe}_stop').addEventListener('click',teacherStop);
   q('lab_{safe}').addEventListener('nabil:demo',runDemo);
   q('lab_{safe}').addEventListener('nabil:teach-all',runDemo);
   q('lab_{safe}').addEventListener('nabil:teach-stop',()=>{{teacherStop();q('lab_{safe}').dispatchEvent(new CustomEvent('nabil:teacher-stopped',{{detail:{{labRef:'{safe}'}},bubbles:true}}));}});
   q('lab_{safe}').addEventListener('nabil:teacher-stop',()=>{{teacherStop();q('lab_{safe}').dispatchEvent(new CustomEvent('nabil:teacher-stopped',{{detail:{{labRef:'{safe}'}},bubbles:true}}));}});
   q('lab_{safe}').addEventListener('nabil:teacher-state',e=>applyTeacherState(e.detail||{{}}));
   ['{safe}_V','{safe}_R1','{safe}_R2'].forEach(id=>q(id).addEventListener('input',calculate));
   renderSwitch();
 }})();
 </script>
</section>"""


def _render_optics(spec: Dict[str, Any], lang: str, lab_id: str) -> str:
    safe = _safe_id(lab_id)
    L = _labels(lang)
    if lang == "ar":
        cues = [
            {"target": "incident", "text": "هذا هو الشعاع الساقط المتجه إلى نقطة السقوط."},
            {"target": "normal", "text": "وهذا هو الناظم، وهو عمودي على سطح المرآة عند نقطة السقوط."},
            {"target": "angle_i", "text": "تُقاس زاوية السقوط بين الشعاع الساقط والناظم، وليس انطلاقًا من سطح المرآة."},
            {"target": "reflected", "text": "وهذا هو الشعاع المنعكس. وفق قانون الانعكاس تساوي زاوية الانعكاس زاوية السقوط."},
        ]
    elif lang == "fr":
        cues = [
            {"target": "incident", "text": "Voici le rayon incident qui arrive au point d’incidence."},
            {"target": "normal", "text": "Voici la normale, perpendiculaire au miroir au point d’incidence."},
            {"target": "angle_i", "text": "L’angle d’incidence est mesuré entre le rayon incident et la normale, pas avec le miroir."},
            {"target": "reflected", "text": "Voici le rayon réfléchi. Selon la loi de la réflexion, les deux angles sont égaux."},
        ]
    else:
        cues = [
            {"target": "incident", "text": "This is the incident ray arriving at the point of incidence."},
            {"target": "normal", "text": "This is the normal, perpendicular to the mirror at the point of incidence."},
            {"target": "angle_i", "text": "The angle of incidence is measured from the normal, not from the mirror surface."},
            {"target": "reflected", "text": "This is the reflected ray. The law of reflection requires equal incidence and reflection angles."},
        ]
    return f"""
<section class="interactive-lab nabil-science-lab" id="lab_{safe}" data-lab-kind="OPTICS_REFLECTION" data-demo-ms="11000"
 data-teacher-pointer="synced" data-angle-reference="normal"
 data-science-rule="ANGLES_FROM_NORMAL;NORMAL_PERPENDICULAR_SURFACE;I_EQUALS_R"
 style="margin-top:16px;background:#071827;color:#f8fafc;border:1px solid #24506f;border-radius:14px;padding:16px;">
 <h3 style="margin-top:0;color:#2de1ff;">{html.escape(str(spec["title"]))}</h3><p>{html.escape(str(spec["instructions"]))}</p>
 <div style="font-size:12px;font-weight:700;color:#7dd3fc;">☝ {html.escape(L["drag_source"])}</div>
 <svg id="{safe}_svg" viewBox="0 0 620 390" style="width:100%;max-width:720px;touch-action:none;background:#030b14;border-radius:12px;">
  <defs><marker id="{safe}_arrowHead" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3z" fill="#2de1ff"/></marker></defs>
  <line x1="60" y1="315" x2="560" y2="315" stroke="#cbd5e1" stroke-width="7"/>
  <line id="{safe}_normal" x1="310" y1="70" x2="310" y2="315" stroke="#facc15" stroke-width="2.5" stroke-dasharray="7 6"/><text x="323" y="92" fill="#facc15" font-size="12">normal</text>
  <line id="{safe}_incident" x1="145" y1="90" x2="310" y2="315" stroke="#fb7185" stroke-width="4"/>
  <line id="{safe}_reflected" x1="310" y1="315" x2="475" y2="90" stroke="#22c55e" stroke-width="4"/>
  <path id="{safe}_arcI" fill="none" stroke="#c084fc" stroke-width="4"/><path id="{safe}_arcR" fill="none" stroke="#c084fc" stroke-width="4"/>
  <circle cx="310" cy="315" r="6" fill="#fff"/>
  <g id="{safe}_source" style="cursor:grab"><circle id="{safe}_sourceDot" cx="145" cy="90" r="13" fill="#facc15" stroke="#fff" stroke-width="3"/><text id="{safe}_sourceText" x="164" y="84" fill="#facc15" font-size="14" font-weight="800">S</text></g>
  <line id="{safe}_teacherArrow" x1="580" y1="45" x2="215" y2="180" stroke="#2de1ff" stroke-width="3" stroke-dasharray="8 6" marker-end="url(#{safe}_arrowHead)"/>
 </svg>
 <div id="{safe}_angles" style="margin-top:9px;font-weight:700;"></div>
 <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:10px;"><button type="button" id="{safe}_teach">{html.escape(L["explain"])}</button><button type="button" id="{safe}_stop">{html.escape(L["stop"])}</button></div>
 <p style="font-size:12px;color:#b6c8d8;">{html.escape(str(spec["observation"]))}</p>
 <script>
 (()=>{{
  const q=id=>document.getElementById(id),svg=q('{safe}_svg'),I={{x:310,y:315}};let S={{x:145,y:90}},drag=false,pid=null;const teacher=q('{safe}_teacherArrow');
  const targets={{incident:[215,180],normal:[310,165],angle_i:[277,255],reflected:[405,180]}};
  function pointTeacher(name){{const p=targets[name]||targets.incident;teacher.setAttribute('x2',p[0]);teacher.setAttribute('y2',p[1]);}}
  {_voice_helpers(lang)}
  function arc(C,A,B,r){{const a1=Math.atan2(A.y-C.y,A.x-C.x),a2=Math.atan2(B.y-C.y,B.x-C.x);let d=a2-a1;while(d>Math.PI)d-=2*Math.PI;while(d<-Math.PI)d+=2*Math.PI;const p1={{x:C.x+r*Math.cos(a1),y:C.y+r*Math.sin(a1)}},p2={{x:C.x+r*Math.cos(a1+d),y:C.y+r*Math.sin(a1+d)}};return 'M'+p1.x+','+p1.y+' A'+r+','+r+' 0 0 '+(d>0?1:0)+' '+p2.x+','+p2.y;}}
  function update(){{
   S.x=Math.min(285,Math.max(45,S.x));S.y=Math.min(270,Math.max(45,S.y));
   q('{safe}_sourceDot').setAttribute('cx',S.x);q('{safe}_sourceDot').setAttribute('cy',S.y);
   q('{safe}_sourceText').setAttribute('x',S.x+18);q('{safe}_sourceText').setAttribute('y',S.y-7);
   q('{safe}_incident').setAttribute('x1',S.x);q('{safe}_incident').setAttribute('y1',S.y);
   const R={{x:I.x+(I.x-S.x),y:S.y}},N={{x:I.x,y:I.y-160}};
   q('{safe}_reflected').setAttribute('x2',R.x);q('{safe}_reflected').setAttribute('y2',R.y);
   q('{safe}_arcI').setAttribute('d',arc(I,N,S,52));q('{safe}_arcR').setAttribute('d',arc(I,R,N,52));
   const theta=Math.atan2(Math.abs(S.x-I.x),I.y-S.y)*180/Math.PI;
   q('{safe}_angles').textContent='θi = '+theta.toFixed(1)+'° · θr = '+theta.toFixed(1)+'°';
  }}
  function local(e){{const p=svg.createSVGPoint();p.x=e.clientX;p.y=e.clientY;return p.matrixTransform(svg.getScreenCTM().inverse());}}
  q('{safe}_source').addEventListener('pointerdown',e=>{{teacherStop();drag=true;pid=e.pointerId;q('{safe}_source').setPointerCapture?.(pid);e.preventDefault();}});
  q('{safe}_source').addEventListener('pointermove',e=>{{if(!drag||e.pointerId!==pid)return;const p=local(e);S={{x:p.x,y:p.y}};update();e.preventDefault();}});
  const end=e=>{{if(!drag||e.pointerId!==pid)return;drag=false;q('{safe}_source').releasePointerCapture?.(pid);}};
  q('{safe}_source').addEventListener('pointerup',end);q('{safe}_source').addEventListener('pointercancel',end);
  const style=document.createElement('style');style.textContent='@keyframes {safe}_pointer{{to{{stroke-dashoffset:-28}}}} #{safe}_teacherArrow{{animation:{safe}_pointer .85s linear infinite}}';document.head.appendChild(style);
  const runDemo=()=>{{
     const demoCues={json.dumps(cues,ensure_ascii=False)};
     q('lab_{safe}').dispatchEvent(new CustomEvent('nabil:teacher-start',{{detail:{{labRef:'{safe}',stepCount:demoCues.length}},bubbles:true}}));
     playTeacherCues(demoCues,()=>q('lab_{safe}').dispatchEvent(new CustomEvent('nabil:teacher-complete',{{detail:{{labRef:'{safe}',stepCount:demoCues.length}},bubbles:true}})));
   }};
  q('{safe}_teach').addEventListener('click',runDemo);q('{safe}_stop').addEventListener('click',teacherStop);
  q('lab_{safe}').addEventListener('nabil:demo',runDemo);
   q('lab_{safe}').addEventListener('nabil:teach-all',runDemo);
   q('lab_{safe}').addEventListener('nabil:teach-stop',()=>{{teacherStop();q('lab_{safe}').dispatchEvent(new CustomEvent('nabil:teacher-stopped',{{detail:{{labRef:'{safe}'}},bubbles:true}}));}});
   q('lab_{safe}').addEventListener('nabil:teacher-stop',()=>{{teacherStop();q('lab_{safe}').dispatchEvent(new CustomEvent('nabil:teacher-stopped',{{detail:{{labRef:'{safe}'}},bubbles:true}}));}});update();
 }})();
 </script>
</section>"""


def _render_ionic(spec: Dict[str, Any], lang: str, lab_id: str) -> str:
    safe = _safe_id(lab_id)
    L = _labels(lang)
    c = spec["cation"]; a = spec["anion"]
    cs = html.escape(str(c["symbol"])); an = html.escape(str(a["symbol"]))
    cq = int(c["charge"]); aq = int(a["charge"])
    cr = int(spec["cation_ratio"]); ar = int(spec["anion_ratio"])
    transfer = int(spec["electron_transfer_count"])
    formula = cs + ("" if cr == 1 else str(cr)) + an + ("" if ar == 1 else str(ar))
    if lang == "ar":
        cues = [
            {"target": "cation", "text": f"نبدأ بـ {cs}. وفق الدليل الموثق يتحول إلى أيون موجب."},
            {"target": "electron", "text": f"الرابطة أيونية، لذلك نتابع انتقال {transfer} إلكترونًا وفق الدليل الموثق."},
            {"target": "anion", "text": f"يستقبل {an} الإلكترونات وفق الشحنة الموثقة."},
            {"target": "formula", "text": f"نسبة الأيونات الموثقة هي {cr} إلى {ar}. لذلك الصيغة المتعادلة هي {formula}، ومجموع الشحنات يساوي صفرًا."},
        ]
    elif lang == "fr":
        cues = [
            {"target": "cation", "text": f"On commence par {cs}, qui forme le cation vérifié."},
            {"target": "electron", "text": f"La liaison est ionique et implique le transfert de {transfer} électron ou électrons."},
            {"target": "anion", "text": f"{an} reçoit les électrons et forme l’anion vérifié."},
            {"target": "formula", "text": f"Le rapport ionique vérifié est {cr} à {ar}. La formule neutre est {formula}."},
        ]
    else:
        cues = [
            {"target": "cation", "text": f"Start with {cs}, which forms the verified cation."},
            {"target": "electron", "text": f"This is ionic bonding with {transfer} transferred electron or electrons."},
            {"target": "anion", "text": f"{an} receives the transferred electron or electrons and forms the verified anion."},
            {"target": "formula", "text": f"The verified ion ratio is {cr} to {ar}, so the neutral formula is {formula}."},
        ]

    positions = [(115, 215), (515, 215), (115, 95), (515, 95)]
    anions = []
    for i in range(ar):
        x, y = positions[i]
        charge_label = f"{an}{abs(aq)}−" if abs(aq) != 1 else f"{an}−"
        anions.append(
            f'<g id="{safe}_anion_{i}"><circle cx="{x}" cy="{y}" r="58" fill="#0e2630" stroke="#55e6a4" stroke-width="4"/>'
            f'<text x="{x-18}" y="{y+7}" fill="#55e6a4" font-size="18" font-weight="900">{an}</text>'
            f'<text id="{safe}_anionCharge_{i}" x="{x-24}" y="{y-68}" fill="#55e6a4" font-size="15" font-weight="900" opacity="0">{charge_label}</text></g>'
        )
    electrons = []
    for i in range(transfer):
        ang = (i / max(1, transfer)) * 2 * math.pi
        x = 310 + 72 * math.cos(ang); y = 215 + 72 * math.sin(ang)
        electrons.append(f'<circle id="{safe}_e_{i}" cx="{x:.1f}" cy="{y:.1f}" r="7" fill="#c084fc" stroke="#fff" stroke-width="2"/>')
    c_charge_label = f"{cs}{cq}+" if cq != 1 else f"{cs}+"

    return f"""
<section class="interactive-lab nabil-science-lab" id="lab_{safe}" data-lab-kind="IONIC_COMPOUND" data-teacher-pointer="synced" data-charge-neutral="true" data-demo-ms="12000"
 data-science-rule="IONIC_ELECTRON_TRANSFER;CHARGE_NEUTRALITY"
 style="margin-top:16px;background:#071827;color:#f8fafc;border:1px solid #24506f;border-radius:14px;padding:16px;">
 <h3 style="margin-top:0;color:#2de1ff;">{html.escape(str(spec["title"]))}</h3><p>{html.escape(str(spec["instructions"]))}</p>
 <svg id="{safe}_svg" viewBox="0 0 620 410" style="width:100%;max-width:720px;background:#030b14;border-radius:12px;">
  <defs><marker id="{safe}_arrowHead" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3z" fill="#2de1ff"/></marker></defs>
  <g id="{safe}_cation"><circle cx="310" cy="215" r="78" fill="#11283d" stroke="#facc15" stroke-width="4"/><text x="285" y="223" fill="#facc15" font-size="20" font-weight="900">{cs}</text><text id="{safe}_cationCharge" x="277" y="122" fill="#facc15" font-size="16" font-weight="900" opacity="0">{c_charge_label}</text></g>
  {"".join(anions)}<g id="{safe}_electrons">{"".join(electrons)}</g>
  <text id="{safe}_formula" x="260" y="380" fill="#fff" font-size="26" font-weight="900" opacity="0">{html.escape(formula)}</text>
  <line id="{safe}_teacherArrow" x1="590" y1="45" x2="310" y2="145" stroke="#2de1ff" stroke-width="3" stroke-dasharray="8 6" marker-end="url(#{safe}_arrowHead)"/>
 </svg>
 <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:10px;"><button type="button" id="{safe}_transfer">{html.escape(L["transfer"])}</button><button type="button" id="{safe}_teach">{html.escape(L["explain"])}</button><button type="button" id="{safe}_stop">{html.escape(L["stop"])}</button><button type="button" id="{safe}_reset">{html.escape(L["reset"])}</button></div>
 <div id="{safe}_status" aria-live="polite" style="margin-top:9px;font-weight:700;"></div>
 <p style="font-size:12px;color:#b6c8d8;">{html.escape(str(spec["observation"]))}</p>
 <script>
 (()=>{{
  const q=id=>document.getElementById(id),teacher=q('{safe}_teacherArrow'),electronCount={transfer},anionCount={ar};let transferred=false;
  const targets={{cation:[310,145],electron:[310,150],anion:[{positions[0][0]},{positions[0][1]}],formula:[310,370]}};
  function pointTeacher(name){{const p=targets[name]||targets.cation;teacher.setAttribute('x2',p[0]);teacher.setAttribute('y2',p[1]);}}
  {_voice_helpers(lang)}
  function reset(){{transferred=false;for(let i=0;i<electronCount;i++){{const e=q('{safe}_e_'+i);if(e){{e.style.opacity='1';e.removeAttribute('transform');e.style.transition='';}}}}q('{safe}_cationCharge').setAttribute('opacity','0');for(let i=0;i<anionCount;i++)q('{safe}_anionCharge_'+i)?.setAttribute('opacity','0');q('{safe}_formula').setAttribute('opacity','0');q('{safe}_status').textContent='';}}
  function transfer(){{if(transferred)return;transferred=true;pointTeacher('electron');const positions={json.dumps(positions)};for(let i=0;i<electronCount;i++){{const e=q('{safe}_e_'+i);if(!e)continue;const targetIndex=i%anionCount,tx=positions[targetIndex][0]-310,ty=positions[targetIndex][1]-215;e.style.transition='transform .65s ease';e.setAttribute('transform','translate('+tx+' '+ty+')');}}setTimeout(()=>{{q('{safe}_cationCharge').setAttribute('opacity','1');for(let i=0;i<anionCount;i++)q('{safe}_anionCharge_'+i)?.setAttribute('opacity','1');q('{safe}_formula').setAttribute('opacity','1');q('{safe}_status').textContent='net charge = 0';pointTeacher('formula');}},700);}}
  const style=document.createElement('style');style.textContent='@keyframes {safe}_pointer{{to{{stroke-dashoffset:-28}}}} #{safe}_teacherArrow{{animation:{safe}_pointer .85s linear infinite}}';document.head.appendChild(style);
  const runDemo=()=>{{
     reset();const demoCues={json.dumps(cues,ensure_ascii=False)};
     teacherStop();const token=teacherToken;let i=0;
     q('lab_{safe}').dispatchEvent(new CustomEvent('nabil:teacher-start',{{detail:{{labRef:'{safe}',stepCount:demoCues.length}},bubbles:true}}));
     const next=()=>{{
       if(token!==teacherToken)return;
       if(i>=demoCues.length){{q('lab_{safe}').dispatchEvent(new CustomEvent('nabil:teacher-complete',{{detail:{{labRef:'{safe}',stepCount:demoCues.length}},bubbles:true}}));return;}}
       const cue=demoCues[i++];
       if(cue.target==='electron'&&!transferred)transfer();
       teacherSpeakCue(cue.text,cue.target,next);
     }};next();
   }};
  q('{safe}_transfer').addEventListener('click',transfer);q('{safe}_teach').addEventListener('click',runDemo);q('{safe}_stop').addEventListener('click',teacherStop);q('{safe}_reset').addEventListener('click',()=>{{teacherStop();reset();pointTeacher('cation');}});
  q('lab_{safe}').addEventListener('nabil:demo',runDemo);
   q('lab_{safe}').addEventListener('nabil:teach-all',runDemo);
   q('lab_{safe}').addEventListener('nabil:teach-stop',()=>{{teacherStop();q('lab_{safe}').dispatchEvent(new CustomEvent('nabil:teacher-stopped',{{detail:{{labRef:'{safe}'}},bubbles:true}}));}});
   q('lab_{safe}').addEventListener('nabil:teacher-stop',()=>{{teacherStop();q('lab_{safe}').dispatchEvent(new CustomEvent('nabil:teacher-stopped',{{detail:{{labRef:'{safe}'}},bubbles:true}}));}});reset();
 }})();
 </script>
</section>"""


def render_advanced_verified_lab(spec: Dict[str, Any], lang_code: str, lab_id: str) -> Tuple[str, bool]:
    validate_advanced_lab_spec(spec)
    kind = str(spec.get("kind") or "").upper()
    if kind == "DC_SERIES_CIRCUIT":
        return _render_circuit(spec, lang_code, lab_id), True
    if kind == "OPTICS_REFLECTION":
        return _render_optics(spec, lang_code, lab_id), True
    if kind == "IONIC_COMPOUND":
        return _render_ionic(spec, lang_code, lab_id), True
    if kind == "GEOMETRY_PROOF":
        return render_geometry_proof_lab(spec, lang_code, lab_id)
    raise RuntimeError(f"LAB_ADVANCED_KIND_UNSUPPORTED:{kind}")
