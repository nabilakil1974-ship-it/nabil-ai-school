#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NABIL AI — محرك عرض المختبرات التفاعلية الموثقة.

المبدأ:
- هذا الملف لا يقرر قاعدة علمية من عنده.
- يستقبل Lab Spec تم توليده والتحقق من مرجعه داخل المصنع.
- لا يضع sliders رقمية ولا min/max/default مخترعة.
- إذا المواصفة ناقصة أو نوع التجربة غير مدعوم يفشل Fail-Closed.
"""
import html
import json
import re
import math
from typing import Dict,Any,Tuple
try:
    from scripts.nabil_i18n import t as _t
    from scripts.nabil_advanced_lab import (
        ADVANCED_LAB_KINDS,
        render_advanced_verified_lab,
        validate_advanced_lab_spec,
    )
    from scripts.nabil_geometry_lab import (
        render_geometry_proof_lab,
        validate_geometry_proof_spec,
    )
except Exception:
    from nabil_i18n import t as _t
    from nabil_advanced_lab import (
        ADVANCED_LAB_KINDS,
        render_advanced_verified_lab,
        validate_advanced_lab_spec,
    )
    from nabil_geometry_lab import (
        render_geometry_proof_lab,
        validate_geometry_proof_spec,
    )

_ALLOWED_KINDS={"FORMULA_CALCULATOR","ORIENTATION_INVARIANT","SHAPE_RESPONSE","EVIDENCE_SEQUENCE","EVIDENCE_REVEAL","GEOMETRY_PROOF"} | ADVANCED_LAB_KINDS
_ALLOWED_OPS={"+","-","*","/"}

def _safe_id(value:str)->str:
    return re.sub(r"[^a-zA-Z0-9_]","_",str(value or "lab"))

def validate_lab_spec(spec:Dict[str,Any])->Dict[str,Any]:
    # هذا التحقق يمنع أي Lab شكلي أو مواصفة ناقصة من المرور.
    if not isinstance(spec,dict):
        raise RuntimeError("LAB_SPEC_INVALID: expected object")
    if spec.get("supported") is not True:
        raise RuntimeError("LAB_SPEC_NOT_SUPPORTED")
    kind=str(spec.get("kind") or "").strip().upper()
    if kind not in _ALLOWED_KINDS:
        raise RuntimeError(f"LAB_KIND_UNSUPPORTED: {kind}")
    for key in ("title","instructions","observation","evidence_ref"):
        if not str(spec.get(key) or "").strip():
            raise RuntimeError(f"LAB_SPEC_MISSING_FIELD: {key}")
    teacher_script=spec.get("teacher_script")
    if not isinstance(teacher_script,list) or not 2<=len(teacher_script)<=12:
        raise RuntimeError("LAB_TEACHER_SCRIPT_REQUIRED")
    allowed={"point","highlight","set_state","animate","observe","explain","conclude"}
    switch_closed=False
    for i,step in enumerate(teacher_script):
        if not isinstance(step,dict) or not str(step.get("say") or "").strip() or str(step.get("action") or "") not in allowed:
            raise RuntimeError(f"LAB_TEACHER_STEP_INVALID:{i}")
        target_ids=step.get("target_ids")
        if not isinstance(target_ids,list) or not target_ids or any(not str(x or "").strip() for x in target_ids):
            raise RuntimeError(f"LAB_TEACHER_TARGET_REQUIRED:{i}")
        if not isinstance(step.get("state_before"),dict) or not isinstance(step.get("state_after"),dict):
            raise RuntimeError(f"LAB_TEACHER_STATE_INVALID:{i}")
        if not isinstance(step.get("scientific_constraints"),list) or not str(step.get("evidence_quote") or "").strip():
            raise RuntimeError(f"LAB_TEACHER_EVIDENCE_INVALID:{i}")
        if kind=="DC_SERIES_CIRCUIT":
            before=step.get("state_before") or {}; after=step.get("state_after") or {}
            if "switch_closed" in before and bool(before["switch_closed"])!=switch_closed:
                raise RuntimeError(f"LAB_CIRCUIT_STATE_DISCONTINUITY:{i}")
            next_closed=bool(after.get("switch_closed",switch_closed))
            words=(str(step.get("say") or "")+" "+str(step.get("action") or "")).lower()
            if any(x in words for x in ("current","charge flow","تيار","مرور الشحن")) and not next_closed:
                raise RuntimeError(f"LAB_CIRCUIT_FLOW_WITH_OPEN_SWITCH:{i}")
            switch_closed=next_closed

    if kind=="FORMULA_CALCULATOR":
        formula=spec.get("formula") or {}
        for key in ("output","input_a","input_b","operator"):
            if not str(formula.get(key) or "").strip():
                raise RuntimeError(f"LAB_FORMULA_MISSING_FIELD: {key}")
        if formula["operator"] not in _ALLOWED_OPS:
            raise RuntimeError("LAB_FORMULA_OPERATOR_UNSUPPORTED")
        # ممنوع اختراع مجال رقمي. الطالب يدخل القيم بنفسه.
        if any(k in formula for k in ("min","max","default","initial","step")):
            raise RuntimeError("LAB_FORMULA_FAKE_RANGE_FORBIDDEN")

    if kind=="ORIENTATION_INVARIANT":
        if str(spec.get("invariant_orientation") or "").lower() not in ("horizontal","vertical"):
            raise RuntimeError("LAB_ORIENTATION_INVALID")

    if kind=="SHAPE_RESPONSE":
        if str(spec.get("behavior") or "").lower() not in ("fixed","conforms"):
            raise RuntimeError("LAB_SHAPE_BEHAVIOR_INVALID")

    if kind=="GEOMETRY_PROOF":
        validate_geometry_proof_spec(spec)

    if kind=="EVIDENCE_SEQUENCE":
        steps=spec.get("steps")
        if not isinstance(steps,list) or not 2<=len(steps)<=8:
            raise RuntimeError("LAB_SEQUENCE_STEPS_INVALID")
        for i,step in enumerate(steps):
            if not isinstance(step,dict) or not str(step.get("label") or "").strip() or not str(step.get("evidence_quote") or "").strip():
                raise RuntimeError(f"LAB_SEQUENCE_STEP_INVALID:{i}")
    if kind=="EVIDENCE_REVEAL":
        items=spec.get("items")
        if not isinstance(items,list) or not 1<=len(items)<=8:
            raise RuntimeError("LAB_REVEAL_ITEMS_INVALID")
        for i,item in enumerate(items):
            if not isinstance(item,dict) or not str(item.get("label") or "").strip() or not str(item.get("evidence_quote") or "").strip():
                raise RuntimeError(f"LAB_REVEAL_ITEM_INVALID:{i}")
    if kind in ADVANCED_LAB_KINDS:
        validate_advanced_lab_spec(spec)
    return spec

def _render_formula(spec:Dict[str,Any],lang_code:str,lab_id:str)->str:
    # مختبر العلاقة الرياضية: لا قيم جاهزة. يدخل الطالب القيم ويرى النتيجة الحقيقية.
    f=spec["formula"]; safe=_safe_id(lab_id); op=f["operator"]
    js_expr={"+":"a+b","-":"a-b","*":"a*b","/":"(b===0?NaN:a/b)"}[op]
    output=html.escape(str(f["output"]))
    unit=html.escape(str(f.get("output_unit") or ""))
    unit_suffix=(" "+unit) if unit else ""
    return f"""
    <section class="interactive-lab nabil-live-lab" id="lab_{safe}" data-lab-kind="FORMULA_CALCULATOR" data-demo-ms="5000"
      style="margin-top:16px;background:#f0f9ff;border:1px solid #7dd3fc;border-radius:12px;padding:16px;">
      <h3 style="margin:0 0 8px;color:#0369a1;">{html.escape(_t(lang_code,'lab_title'))} — {html.escape(spec['title'])}</h3>
      <p style="margin:0 0 12px;color:#334155;">{html.escape(spec['instructions'])}</p>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
        <label>{html.escape(str(f['input_a']))}<input id="{safe}_a" type="number" inputmode="decimal" style="width:100%;box-sizing:border-box;padding:10px;margin-top:4px;"></label>
        <label>{html.escape(str(f['input_b']))}<input id="{safe}_b" type="number" inputmode="decimal" style="width:100%;box-sizing:border-box;padding:10px;margin-top:4px;"></label>
      </div>
      <button type="button" class="nav-btn" style="margin-top:12px;" onclick="run_{safe}()">{html.escape(_t(lang_code,'lab_run'))}</button>
      <div id="{safe}_result" style="margin-top:12px;padding:10px;background:#fff;border-radius:8px;display:none;"></div>
      <p style="font-size:12px;color:#475569;margin:10px 0 0;">{html.escape(spec['observation'])}</p>
      <script>
      function run_{safe}(){{
        const a=Number(document.getElementById('{safe}_a').value);
        const b=Number(document.getElementById('{safe}_b').value);
        const box=document.getElementById('{safe}_result');
        box.style.display='block';
        if(!Number.isFinite(a)||!Number.isFinite(b)){{box.textContent='—';return;}}
        const out={js_expr};
        box.textContent=Number.isFinite(out)?'{output} = '+out+'{unit_suffix}':'—';
      }}
      document.getElementById('lab_{safe}').addEventListener('nabil:demo',()=>{{
        const box=document.getElementById('{safe}_result');box.style.display='block';
        box.textContent={json.dumps(str(spec["observation"]))};
        try{{window.NABILLessonE2E?.speak?.({json.dumps(str(spec["instructions"]) + ". " + str(spec["observation"]))},{json.dumps(lang_code)});}}catch(_e){{}}
      }});
      </script>
    </section>"""

def _render_orientation(spec:Dict[str,Any],lang_code:str,lab_id:str)->str:
    """Direct-manipulation orientation lab.

    The learner drags the vessel left/right with mouse, pen, or finger. Only
    the vessel rotates; the evidence-backed invariant element remains at the
    verified horizontal/vertical orientation.
    """
    safe=_safe_id(lab_id)
    orient=str(spec["invariant_orientation"]).lower()
    invariant_line=(
        '<line x1="93" y1="96" x2="207" y2="96" stroke="#0284c7" '
        'stroke-width="8" stroke-linecap="round"/>'
        if orient=="horizontal" else
        '<line x1="150" y1="45" x2="150" y2="148" stroke="#0284c7" '
        'stroke-width="8" stroke-linecap="round"/>'
    )
    drag_hint={"ar":"اسحب الوعاء يمينًا ويسارًا","fr":"Fais glisser le récipient à gauche et à droite","en":"Drag the vessel left and right"}.get(lang_code,"Drag the vessel left and right")
    reset_label={"ar":"إعادة","fr":"Réinitialiser","en":"Reset"}.get(lang_code,"Reset")
    return f"""
    <section class="interactive-lab nabil-live-lab" id="lab_{safe}" data-lab-kind="ORIENTATION_INVARIANT" data-demo-ms="7000"
      style="margin-top:16px;background:#f0f9ff;border:1px solid #7dd3fc;border-radius:14px;padding:16px;box-shadow:0 8px 24px rgba(2,132,199,.08);">
      <div style="display:flex;justify-content:space-between;gap:10px;align-items:flex-start;flex-wrap:wrap;">
        <div>
          <h3 style="margin:0 0 6px;color:#0369a1;">{html.escape(_t(lang_code,'lab_title'))} — {html.escape(spec['title'])}</h3>
          <p style="margin:0;color:#334155;">{html.escape(spec['instructions'])}</p>
        </div>
        <button type="button" class="q-opt" onclick="reset_{safe}()" style="min-height:44px;">↺ {html.escape(reset_label)}</button>
      </div>
      <div style="margin:12px 0 8px;font-size:12px;font-weight:700;color:#0369a1;">☝ {html.escape(drag_hint)}</div>
      <svg id="{safe}_stage" viewBox="0 0 300 190" role="img" aria-label="{html.escape(spec['title'])}"
        style="width:100%;max-width:560px;background:linear-gradient(#ffffff,#f8fafc);border-radius:12px;border:1px solid #cbd5e1;touch-action:none;user-select:none;cursor:grab;">
        <defs>
          <filter id="{safe}_shadow" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="4" stdDeviation="4" flood-opacity=".15"/>
          </filter>
        </defs>
        <rect x="18" y="18" width="264" height="154" rx="16" fill="#f8fafc"/>
        <g id="{safe}_moving" transform="rotate(0 150 100)" filter="url(#{safe}_shadow)">
          <path d="M75 45 L225 45 L205 155 L95 155 Z" fill="#ffffff" stroke="#334155" stroke-width="5"/>
          <circle id="{safe}_grab" cx="150" cy="32" r="12" fill="#0ea5e9" stroke="#ffffff" stroke-width="4"/>
          <path d="M143 32h14M150 25v14" stroke="#ffffff" stroke-width="2.6" stroke-linecap="round"/>
        </g>
        <g id="{safe}_invariant">{invariant_line}</g>
      </svg>
      <p style="font-size:12px;color:#475569;margin:10px 0 0;">{html.escape(spec['observation'])}</p>
      <script>
      (()=>{{
        const stage=document.getElementById('{safe}_stage');
        const moving=document.getElementById('{safe}_moving');
        let active=false,startX=0,startAngle=0,angle=0,pid=null;
        function apply(next){{
          // The clamp is a UI-only gesture bound, not a scientific measurement.
          // Never expose this presentation angle as textbook data.
          angle=Math.max(-28,Math.min(28,next));
          moving.setAttribute('transform','rotate('+angle.toFixed(1)+' 150 100)');
        }}
        function localX(e){{
          const pt=stage.createSVGPoint();pt.x=e.clientX;pt.y=e.clientY;
          return pt.matrixTransform(stage.getScreenCTM().inverse()).x;
        }}
        stage.addEventListener('pointerdown',e=>{{
          active=true;pid=e.pointerId;startX=localX(e);startAngle=angle;
          stage.setPointerCapture?.(pid);stage.style.cursor='grabbing';e.preventDefault();
        }});
        stage.addEventListener('pointermove',e=>{{
          if(!active||e.pointerId!==pid)return;
          apply(startAngle+(localX(e)-startX)*0.34);e.preventDefault();
        }});
        const end=e=>{{
          if(!active||e.pointerId!==pid)return;
          active=false;stage.releasePointerCapture?.(pid);stage.style.cursor='grab';
        }};
        stage.addEventListener('pointerup',end);
        stage.addEventListener('pointercancel',end);
        window.reset_{safe}=()=>apply(0);
        document.getElementById('lab_{safe}').addEventListener('nabil:demo',()=>{{
          try{{window.NABILLessonE2E?.speak?.({json.dumps(str(spec["instructions"]) + ". " + str(spec["observation"]))},{json.dumps(lang_code)});}}catch(_e){{}}
          apply(-20);setTimeout(()=>apply(20),1300);setTimeout(()=>apply(0),2800);
        }});
      }})();
      </script>
    </section>"""


def _render_shape(spec:Dict[str,Any],lang_code:str,lab_id:str)->str:
    """Drag-and-drop state/shape lab with two real drop zones."""
    safe=_safe_id(lab_id)
    fixed=str(spec["behavior"]).lower()=="fixed"
    fixed_js="true" if fixed else "false"
    drag_hint={"ar":"اسحب المادة من الوعاء A إلى الوعاء B","fr":"Fais glisser la matière du récipient A vers B","en":"Drag the material from vessel A to vessel B"}.get(lang_code,"Drag the material from vessel A to vessel B")
    reset_label={"ar":"إعادة","fr":"Réinitialiser","en":"Reset"}.get(lang_code,"Reset")
    return f"""
    <section class="interactive-lab nabil-live-lab" id="lab_{safe}" data-lab-kind="SHAPE_RESPONSE" data-demo-ms="7000"
      style="margin-top:16px;background:#f0f9ff;border:1px solid #7dd3fc;border-radius:14px;padding:16px;box-shadow:0 8px 24px rgba(2,132,199,.08);">
      <div style="display:flex;justify-content:space-between;gap:10px;align-items:flex-start;flex-wrap:wrap;">
        <div>
          <h3 style="margin:0 0 6px;color:#0369a1;">{html.escape(_t(lang_code,'lab_title'))} — {html.escape(spec['title'])}</h3>
          <p style="margin:0;color:#334155;">{html.escape(spec['instructions'])}</p>
        </div>
        <button type="button" class="q-opt" onclick="reset_{safe}()" style="min-height:44px;">↺ {html.escape(reset_label)}</button>
      </div>
      <div style="margin:12px 0 8px;font-size:12px;font-weight:700;color:#0369a1;">☝ {html.escape(drag_hint)}</div>
      <svg id="{safe}_stage" viewBox="0 0 420 220" role="img" aria-label="{html.escape(spec['title'])}"
        style="width:100%;max-width:620px;background:linear-gradient(#ffffff,#f8fafc);border-radius:12px;border:1px solid #cbd5e1;touch-action:none;user-select:none;">
        <defs>
          <filter id="{safe}_shadow" x="-30%" y="-30%" width="160%" height="160%">
            <feDropShadow dx="0" dy="5" stdDeviation="5" flood-opacity=".18"/>
          </filter>
        </defs>
        <text x="105" y="30" text-anchor="middle" font-size="15" font-weight="700" fill="#334155">A</text>
        <text x="315" y="30" text-anchor="middle" font-size="15" font-weight="700" fill="#334155">B</text>
        <path id="{safe}_vesselA" d="M45 48 L165 48 L150 190 L60 190 Z" fill="#fff" stroke="#334155" stroke-width="4"/>
        <path id="{safe}_vesselB" d="M262 48 L368 48 L352 190 L278 190 Z" fill="#fff" stroke="#334155" stroke-width="4"/>
        <g id="{safe}_matter" filter="url(#{safe}_shadow)" style="cursor:grab">
          <path id="{safe}_matterShape" d="M70 116 L140 116 L137 178 L73 178 Z" fill="#38bdf8" opacity=".82" stroke="#0284c7" stroke-width="2"/>
          <circle cx="105" cy="145" r="11" fill="#ffffff" opacity=".92"/>
          <path d="M98 145h14M105 138v14" stroke="#0284c7" stroke-width="2.5" stroke-linecap="round"/>
        </g>
        <rect id="{safe}_dropA" x="38" y="40" width="134" height="158" rx="14" fill="transparent" stroke="transparent" stroke-width="4"/>
        <rect id="{safe}_dropB" x="254" y="40" width="122" height="158" rx="14" fill="transparent" stroke="transparent" stroke-width="4"/>
      </svg>
      <div id="{safe}_state" aria-live="polite" style="margin-top:8px;font-size:12px;font-weight:700;color:#0369a1;"></div>
      <p style="font-size:12px;color:#475569;margin:10px 0 0;">{html.escape(spec['observation'])}</p>
      <script>
      (()=>{{
        const stage=document.getElementById('{safe}_stage');
        const matter=document.getElementById('{safe}_matter');
        const shape=document.getElementById('{safe}_matterShape');
        const state=document.getElementById('{safe}_state');
        const dropA=document.getElementById('{safe}_dropA');
        const dropB=document.getElementById('{safe}_dropB');
        const fixed={fixed_js};
        let active=false,pid=null,start={{x:0,y:0}},offset={{x:0,y:0}},home='A';
        function svgPoint(e){{
          const pt=stage.createSVGPoint();pt.x=e.clientX;pt.y=e.clientY;
          return pt.matrixTransform(stage.getScreenCTM().inverse());
        }}
        function setTransform(x,y){{offset={{x:x,y:y}};matter.setAttribute('transform','translate('+x+' '+y+')');}}
        function inBox(p,el){{
          const b=el.getBBox();
          return p.x>=b.x&&p.x<=b.x+b.width&&p.y>=b.y&&p.y<=b.y+b.height;
        }}
        function setShape(dest){{
          if(fixed){{shape.setAttribute('d','M70 116 L140 116 L137 178 L73 178 Z');return;}}
          if(dest==='B')shape.setAttribute('d','M75 115 L135 115 L130 178 L80 178 Z');
          else shape.setAttribute('d','M70 116 L140 116 L137 178 L73 178 Z');
        }}
        function snap(dest){{
          home=dest;
          if(dest==='B'){{
            setShape('B');setTransform(210,0);
          }}else{{setTransform(0,0);setShape('A');}}
          dropA.setAttribute('stroke','transparent');dropB.setAttribute('stroke','transparent');
          state.textContent=dest;
        }}
        matter.addEventListener('pointerdown',e=>{{
          active=true;pid=e.pointerId;start=svgPoint(e);
          matter.setPointerCapture?.(pid);matter.style.cursor='grabbing';e.preventDefault();
        }});
        matter.addEventListener('pointermove',e=>{{
          if(!active||e.pointerId!==pid)return;
          const p=svgPoint(e),dx=p.x-start.x,dy=p.y-start.y;
          matter.setAttribute('transform','translate('+(offset.x+dx)+' '+(offset.y+dy)+')');
          dropA.setAttribute('stroke',inBox(p,dropA)?'#38bdf8':'transparent');
          dropB.setAttribute('stroke',inBox(p,dropB)?'#38bdf8':'transparent');
          e.preventDefault();
        }});
        const end=e=>{{
          if(!active||e.pointerId!==pid)return;
          const p=svgPoint(e);active=false;matter.releasePointerCapture?.(pid);matter.style.cursor='grab';
          if(inBox(p,dropB))snap('B');else if(inBox(p,dropA))snap('A');else snap(home);
        }};
        matter.addEventListener('pointerup',end);
        matter.addEventListener('pointercancel',end);
        window.reset_{safe}=()=>{{home='A';setTransform(0,0);setShape('A');state.textContent='';}};
        document.getElementById('lab_{safe}').addEventListener('nabil:demo',()=>{{
          try{{window.NABILLessonE2E?.speak?.({json.dumps(str(spec["instructions"]) + ". " + str(spec["observation"]))},{json.dumps(lang_code)});}}catch(_e){{}}
          snap('A');setTimeout(()=>snap('B'),1100);setTimeout(()=>snap('A'),3000);
        }});
      }})();
      </script>
    </section>"""



def _render_sequence(spec:Dict[str,Any],lang_code:str,lab_id:str)->str:
    """Cross-subject evidence sequence: animate only exact source-backed steps."""
    safe=_safe_id(lab_id)
    steps=spec["steps"]
    explain={"ar":"▶ اشرح الفكرة","fr":"▶ Expliquer l’idée","en":"▶ Explain the idea"}.get(lang_code,"▶ Explain the idea")
    stop={"ar":"■ إيقاف","fr":"■ Arrêter","en":"■ Stop"}.get(lang_code,"■ Stop")
    step_cards="".join(
        f'<div id="{safe}_step_{i}" class="nabil-seq-step" '
        f'style="padding:10px;border:1px solid #334155;border-radius:10px;background:#fff;color:#0f172a;">'
        f'<b>{i+1}. {html.escape(str(step["label"]))}</b>'
        f'<div style="font-size:12px;color:#475569;margin-top:4px;">'
        f'{html.escape(str(step["evidence_quote"]))}</div></div>'
        for i,step in enumerate(steps)
    )
    demo_ms=max(6000,len(steps)*3200)
    labels=[str(step["label"]) for step in steps]
    return f"""
<section class="interactive-lab nabil-live-lab" id="lab_{safe}"
 data-lab-kind="EVIDENCE_SEQUENCE" data-teacher-pointer="synced"
 data-demo-ms="{demo_ms}"
 style="margin-top:16px;background:#071827;border:1px solid #24506f;border-radius:14px;padding:16px;color:#f8fafc;">
 <h3 style="margin:0 0 6px;color:#2de1ff;">{html.escape(spec["title"])}</h3>
 <p style="margin:0 0 12px;color:#dbeafe;">{html.escape(spec["instructions"])}</p>
 <div style="position:relative;">
  <div id="{safe}_pointer" style="position:absolute;left:-8px;top:12px;width:5px;height:42px;border-radius:6px;background:#2de1ff;box-shadow:0 0 14px #2de1ff;transition:transform .45s ease;"></div>
  <div id="{safe}_steps" style="display:grid;gap:8px;padding-left:8px;">{step_cards}</div>
 </div>
 <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:12px;">
  <button type="button" id="{safe}_teach" class="nav-btn">{html.escape(explain)}</button>
  <button type="button" id="{safe}_stop" class="q-opt">{html.escape(stop)}</button>
 </div>
 <p style="font-size:12px;color:#b6c8d8;">{html.escape(spec["observation"])}</p>
 <script>
 (()=>{{
   const root=document.getElementById('lab_{safe}');
   const pointer=document.getElementById('{safe}_pointer');
   const labels={json.dumps(labels,ensure_ascii=False)};
   let token=0,timers=[];
   function stopAll(){{token++;timers.forEach(clearTimeout);timers=[];try{{window.NABILLessonE2E?.stopSpeech?.();}}catch(_e){{}}}}
   function focus(i){{
     document.querySelectorAll('#{safe}_steps .nabil-seq-step').forEach((el,j)=>{{
       el.style.borderColor=j===i?'#2de1ff':'#334155';
       el.style.boxShadow=j===i?'0 0 18px rgba(45,225,255,.25)':'none';
     }});
     const el=document.getElementById('{safe}_step_'+i);
     if(el) pointer.style.transform='translateY('+(el.offsetTop)+'px)';
   }}
   async function play(){{
     stopAll();const mine=token;
     for(let i=0;i<labels.length;i++){{
       if(mine!==token)return;
       focus(i);
       try{{await Promise.resolve(window.NABILLessonE2E?.speak?.(labels[i],{json.dumps(lang_code)}));}}catch(_e){{}}
       if(mine!==token)return;
       await new Promise(resolve=>timers.push(setTimeout(resolve,220)));
     }}
   }}
   document.getElementById('{safe}_teach').addEventListener('click',play);
   document.getElementById('{safe}_stop').addEventListener('click',stopAll);
   root.addEventListener('nabil:demo',play);
   focus(0);
 }})();
 </script>
</section>"""


def _render_evidence_reveal(spec:Dict[str,Any],lang_code:str,lab_id:str)->str:
    """Universal interactive teaching lab for any evidence-backed paragraph/task."""
    safe=_safe_id(lab_id)
    items=spec["items"]
    explain={"ar":"▶ اشرح الفكرة","fr":"▶ Expliquer l’idée","en":"▶ Explain the idea"}.get(lang_code,"▶ Explain the idea")
    next_label={"ar":"التالي","fr":"Suivant","en":"Next"}.get(lang_code,"Next")
    reset_label={"ar":"إعادة","fr":"Recommencer","en":"Reset"}.get(lang_code,"Reset")
    rows="".join(
        f'<button type="button" id="{safe}_item_{i}" class="nabil-reveal-item" '
        f'style="display:block;width:100%;text-align:start;padding:12px;margin:7px 0;'
        f'border:1px solid #334155;border-radius:10px;background:#fff;color:#0f172a;">'
        f'<b>{i+1}. {html.escape(str(item["label"]))}</b>'
        f'<span style="display:block;font-size:12px;color:#475569;margin-top:4px;">'
        f'{html.escape(str(item["evidence_quote"]))}</span></button>'
        for i,item in enumerate(items)
    )
    labels=[str(item["label"]) for item in items]
    demo_ms=max(5000,len(items)*2800)
    return f"""
<section class="interactive-lab nabil-live-lab" id="lab_{safe}"
 data-lab-kind="EVIDENCE_REVEAL" data-teacher-pointer="synced"
 data-demo-ms="{demo_ms}"
 style="margin-top:16px;background:#071827;border:1px solid #24506f;border-radius:14px;padding:16px;color:#f8fafc;">
 <h3 style="margin:0 0 6px;color:#2de1ff;">{html.escape(spec["title"])}</h3>
 <p style="margin:0 0 12px;color:#dbeafe;">{html.escape(spec["instructions"])}</p>
 <div style="position:relative;padding-inline-start:10px;">
   <div id="{safe}_pointer" style="position:absolute;inset-inline-start:0;top:7px;width:5px;height:48px;border-radius:6px;background:#2de1ff;box-shadow:0 0 14px #2de1ff;transition:transform .4s ease;"></div>
   <div>{rows}</div>
 </div>
 <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:12px;">
   <button type="button" id="{safe}_teach" class="nav-btn">{html.escape(explain)}</button>
   <button type="button" id="{safe}_next" class="q-opt">{html.escape(next_label)}</button>
   <button type="button" id="{safe}_reset" class="q-opt">{html.escape(reset_label)}</button>
 </div>
 <p style="font-size:12px;color:#b6c8d8;">{html.escape(spec["observation"])}</p>
 <script>
 (()=>{{
   const root=document.getElementById('lab_{safe}');
   const pointer=document.getElementById('{safe}_pointer');
   const labels={json.dumps(labels,ensure_ascii=False)};
   let index=0,token=0,timers=[];
   function stopAll(){{token++;timers.forEach(clearTimeout);timers=[];try{{window.NABILLessonE2E?.stopSpeech?.();}}catch(_e){{}}}}
   function focus(i){{
     index=((i%labels.length)+labels.length)%labels.length;
     document.querySelectorAll('#lab_{safe} .nabil-reveal-item').forEach((el,j)=>{{
       el.style.borderColor=j===index?'#2de1ff':'#334155';
       el.style.boxShadow=j===index?'0 0 18px rgba(45,225,255,.25)':'none';
     }});
     const el=document.getElementById('{safe}_item_'+index);
     if(el) pointer.style.transform='translateY('+Math.max(0,el.offsetTop-7)+'px)';
   }}
   async function speakCurrent(){{
     focus(index);
     try{{await Promise.resolve(window.NABILLessonE2E?.speak?.(labels[index],{json.dumps(lang_code)}));}}catch(_e){{}}
   }}
   async function play(){{
     stopAll();const mine=token;index=0;
     while(index<labels.length){{
       if(mine!==token)return;
       await speakCurrent();
       if(mine!==token)return;
       index++;
       if(index<labels.length)
         await new Promise(resolve=>timers.push(setTimeout(resolve,220)));
     }}
   }}
   document.getElementById('{safe}_teach').addEventListener('click',play);
   document.getElementById('{safe}_next').addEventListener('click',()=>{{stopAll();index=(index+1)%labels.length;speakCurrent();}});
   document.getElementById('{safe}_reset').addEventListener('click',()=>{{stopAll();index=0;focus(0);}});
   document.querySelectorAll('#lab_{safe} .nabil-reveal-item').forEach((el,i)=>el.addEventListener('click',()=>{{stopAll();index=i;speakCurrent();}}));
   root.addEventListener('nabil:demo',play);
   focus(0);
 }})();
 </script>
</section>"""



REFERENCE_RENDERER_CONTRACT="NABIL_REFERENCE_RENDERER_V1"

def _reference_contract_wrap(raw_html:str,spec:Dict[str,Any],lang_code:str,lab_id:str)->str:
    """Apply the owner-approved NABIL lab shell without changing science.

    The wrapped renderer remains content-agnostic: all scientific text/behavior
    comes from the already-validated Lab Spec.  The shell only standardizes
    presentation, NABIL teacher presence, pointer, controls and phone layout.
    """
    safe=_safe_id(lab_id)
    shell_id=f"nabil_ref_{safe}"
    explain={
        "ar":"🔊 اشرح هذه الفكرة",
        "fr":"🔊 Expliquer cette idée",
        "en":"🔊 Explain this idea",
    }.get(lang_code,"🔊 Explain this idea")
    explain_all={
        "ar":"▶ اشرح من البداية",
        "fr":"▶ Expliquer depuis le début",
        "en":"▶ Explain from the beginning",
    }.get(lang_code,"▶ Explain from the beginning")
    stop={
        "ar":"■ إيقاف",
        "fr":"■ Arrêter",
        "en":"■ Stop",
    }.get(lang_code,"■ Stop")
    teacher_steps=list(spec.get("teacher_script") or [])
    cues=[str(x.get("say") or "").strip() for x in teacher_steps]
    cues=[x for x in cues if x]
    return f"""
<section id="{shell_id}" class="nabil-reference-smart-lab"
 data-renderer-contract="{REFERENCE_RENDERER_CONTRACT}"
 data-teacher-pointer="sentence-synced" data-lab-ref="{safe}">
 <style>
 #{shell_id}{{position:relative;margin:16px 0;background:#071827;color:#eef8ff;
   border:1px solid #24506f;border-radius:18px;padding:12px;overflow:hidden;
   box-shadow:0 18px 42px rgba(0,0,0,.34);min-width:0;max-width:100%}}
 #{shell_id} .nabil-ref-head{{display:flex;align-items:center;justify-content:space-between;
   gap:8px;flex-wrap:wrap;margin-bottom:8px}}
 #{shell_id} .nabil-ref-teacher{{display:flex;align-items:center;gap:7px;padding:6px 10px;
   border:1px solid #2b6485;border-radius:999px;background:#061725;color:#eafaff;
   font-size:12px;font-weight:900}}
 #{shell_id} .nabil-ref-orb{{width:19px;height:19px;border-radius:50%;
   background:radial-gradient(circle at 35% 30%,#fff,#2de1ff 35%,#0c5d76 70%);
   box-shadow:0 0 16px #2de1ff99}}
 #{shell_id} .interactive-lab{{margin:0!important;background:#081e33!important;
   color:#eef8ff!important;border:1px solid #176895!important;border-radius:15px!important;
   padding:12px!important;box-shadow:none!important;min-width:0!important;max-width:100%!important}}
 #{shell_id} .interactive-lab h3{{color:#65dfff!important}}
 #{shell_id} .interactive-lab p,#{shell_id} .interactive-lab label{{color:#dbeefe!important}}
 #{shell_id} .interactive-lab svg{{display:block!important;width:100%!important;max-width:100%!important;
   height:auto!important;background:#061827!important}}
 #{shell_id} .interactive-lab input,#{shell_id} .interactive-lab select{{
   min-height:44px!important;max-width:100%!important;background:#061827!important;
   color:#fff!important;border:1px solid #315f82!important;border-radius:8px!important}}
 #{shell_id} .interactive-lab button{{min-height:44px!important;max-width:100%!important;
   white-space:normal!important}}
 #{shell_id} .nabil-ref-controls{{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}}
 #{shell_id} .nabil-ref-controls button{{min-height:44px;border-radius:10px;border:1px solid #2b6485;
   background:#0f3655;color:#fff;padding:9px 12px;font:800 13px system-ui;cursor:pointer}}
 #{shell_id} .nabil-ref-controls .primary{{background:#0f766e;border-color:#39c7b0}}
 #{shell_id} .nabil-ref-controls .stop{{background:#5a2330;border-color:#bd546b}}
 #{shell_id} .teacherArrow{{position:absolute;inset:0;width:100%;height:100%;
   pointer-events:none;z-index:9;overflow:visible}}
 #{shell_id} .teacherArrow line{{stroke:#2de1ff;stroke-width:2.5;stroke-dasharray:8 6;
   filter:drop-shadow(0 0 4px #2de1ff);transition:x2 .28s ease,y2 .28s ease}}
 #{shell_id} .nabil-ref-focused{{outline:3px solid #ffd447!important;outline-offset:2px!important;
   filter:drop-shadow(0 0 8px rgba(255,212,71,.55))}}
 @media(max-width:430px){{
   #{shell_id}{{padding:7px;border-radius:13px}}
   #{shell_id} .interactive-lab{{padding:8px!important}}
   #{shell_id} .nabil-ref-controls{{display:grid;grid-template-columns:1fr 1fr}}
   #{shell_id} .nabil-ref-controls button{{width:100%}}
 }}
 </style>
 <div class="nabil-ref-head">
   <div class="nabil-ref-teacher"><span class="nabil-ref-orb"></span><span>NABIL</span></div>
   <span style="font-size:11px;color:#9ccbe4">{html.escape(str(spec.get("title") or ""))}</span>
 </div>
 <svg class="teacherArrow" aria-hidden="true">
   <defs><marker id="{safe}_ref_arr" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3z" fill="#2de1ff"/></marker></defs>
   <line id="{safe}_ref_line" x1="96%" y1="32" x2="50%" y2="120" marker-end="url(#{safe}_ref_arr)"/>
 </svg>
 <div class="nabil-ref-body">{raw_html}</div>
 <div class="nabil-ref-controls">
   <button type="button" id="{safe}_ref_current">{html.escape(explain)}</button>
   <button type="button" class="primary" id="{safe}_ref_all">{html.escape(explain_all)}</button>
   <button type="button" class="stop" id="{safe}_ref_stop">{html.escape(stop)}</button>
 </div>
 <script>
 (()=>{{
   const shell=document.getElementById('{shell_id}');
   const inner=shell?.querySelector('.interactive-lab');
   const line=document.getElementById('{safe}_ref_line');
   const cues={json.dumps(cues,ensure_ascii=False)};
   const teacherSteps={json.dumps(teacher_steps,ensure_ascii=False)};
   let cueIndex=0,token=0;
   function visible(el){{
     if(!el)return false;
     const r=el.getBoundingClientRect?.();
     return !!r && r.width>0 && r.height>0;
   }}
   function fallbackTargets(){{
     if(!inner)return [];
     const preferred=[...inner.querySelectorAll(
       '.nabil-seq-step,.nabil-reveal-item,[data-teacher-target],svg g[id],svg path[id],svg line[id],svg circle[id],input,select,[id$="_result"],p'
     )].filter(visible);
     return preferred.length?preferred:[inner];
   }}
   function targetById(raw){{
     if(!inner||!raw)return null;
     const key=String(raw),slug=key.replace(/[^a-zA-Z0-9_]/g,'_');
     const direct=[key,slug,'{safe}_'+slug,'{safe}_'+key]
       .map(id=>document.getElementById(id)).find(el=>el&&inner.contains(el)&&visible(el));
     if(direct)return direct;
     const data=[...inner.querySelectorAll('[data-teacher-target]')]
       .find(el=>String(el.dataset.teacherTarget||'')===key&&visible(el));
     if(data)return data;
     const suffix=[...inner.querySelectorAll('[id]')]
       .find(el=>visible(el)&&(el.id.endsWith('_'+slug)||el.id.endsWith(slug)));
     return suffix||null;
   }}
   function point(index,targetIds=[]){{
     if(!line)return;
     const explicit=(Array.isArray(targetIds)?targetIds:[]).map(targetById).find(Boolean);
     const list=fallbackTargets();
     const target=explicit||(list.length?list[Math.max(0,Math.min(index,list.length-1))]:inner);
     if(!target)return;
     shell.querySelectorAll('.nabil-ref-focused').forEach(x=>x.classList.remove('nabil-ref-focused'));
     target.classList.add('nabil-ref-focused');
     const sr=shell.getBoundingClientRect(),tr=target.getBoundingClientRect();
     const x2=Math.max(18,Math.min(sr.width-18,tr.left-sr.left+tr.width/2));
     const y2=Math.max(52,Math.min(sr.height-18,tr.top-sr.top+Math.min(tr.height/2,60)));
     line.setAttribute('x2',x2);line.setAttribute('y2',y2);
   }}
   function publishTeacherState(detail){{
     // Renderers own the science.  The shell publishes the verified transition
     // before narration so a renderer can visibly apply state_after first.
     inner?.dispatchEvent(new CustomEvent('nabil:teacher-state',{{detail,bubbles:true}}));
     shell?.dispatchEvent(new CustomEvent('nabil:teacher-step',{{detail}}));
     const after=detail.state_after||{{}};
     if(inner){{
       Object.entries(after).forEach(([k,v])=>{{
         const name='teacher'+String(k).replace(/(^|_)([a-z])/g,(_m,_p,c)=>c.toUpperCase());
         try{{inner.dataset[name]=typeof v==='object'?JSON.stringify(v):String(v)}}catch(_e){{}}
       }});
     }}
   }}
   async function speakCue(index){{
     if(!cues.length)return;
     cueIndex=((index%cues.length)+cues.length)%cues.length;
     const step=teacherSteps[cueIndex]||{{}};
     const detail={{index:cueIndex,action:step.action||"point",target_ids:step.target_ids||[],
       state_before:step.state_before||{{}},state_after:step.state_after||{{}},
       scientific_constraints:step.scientific_constraints||[],evidence_quote:step.evidence_quote||""}};
     publishTeacherState(detail);
     point(cueIndex,detail.target_ids);
     // Let the renderer paint the verified state transition before speech.
     await new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));
     try{{await Promise.resolve(window.NABILLessonE2E?.speak?.(cues[cueIndex],{json.dumps(lang_code)}));}}catch(_e){{}}
   }}
   async function playAll(){{
     token++;const mine=token;
     shell?.dispatchEvent(new CustomEvent('nabil:teacher-start',{{detail:{{labRef:'{safe}',stepCount:cues.length}}}}));
     for(let i=0;i<cues.length;i++){{
       if(mine!==token)return;
       await speakCue(i);
       if(mine!==token)return;
       await new Promise(r=>setTimeout(r,260));
     }}
     if(mine===token){{
       shell?.dispatchEvent(new CustomEvent('nabil:teacher-complete',{{detail:{{labRef:'{safe}',stepCount:cues.length}}}}));
     }}
   }}
   function stopTeaching(){{
     token++;
     try{{window.NABILLessonE2E?.stopSpeech?.()}}catch(_e){{}}
     try{{inner?.dispatchEvent(new CustomEvent('nabil:teacher-stop',{{bubbles:false}}))}}catch(_e){{}}
     shell?.querySelectorAll('.nabil-ref-focused').forEach(x=>x.classList.remove('nabil-ref-focused'));
     shell?.dispatchEvent(new CustomEvent('nabil:teacher-stopped',{{detail:{{labRef:'{safe}'}}}}));
   }}
   document.getElementById('{safe}_ref_current')?.addEventListener('click',async()=>{{
     token++;const mine=token;await speakCue(cueIndex);
     if(mine===token && cues.length) cueIndex=(cueIndex+1)%cues.length;
   }});
   document.getElementById('{safe}_ref_all')?.addEventListener('click',playAll);
   document.getElementById('{safe}_ref_stop')?.addEventListener('click',stopTeaching);
   shell?.addEventListener('nabil:teach-all',playAll);
   shell?.addEventListener('nabil:teach-stop',stopTeaching);
   inner?.addEventListener('nabil:demo',()=>{{cueIndex=0;point(0,(teacherSteps[0]||{{}}).target_ids||[]);}});
   window.addEventListener('resize',()=>point(cueIndex,(teacherSteps[cueIndex]||{{}}).target_ids||[]),{{passive:true}});
   requestAnimationFrame(()=>point(0,(teacherSteps[0]||{{}}).target_ids||[]));
 }})();
 </script>
</section>"""

def render_verified_lab(spec:Dict[str,Any],lang_code:str,lab_id:str)->Tuple[str,bool]:
    # نقطة الدخول الوحيدة: المختبر لا يظهر قبل نجاح validate_lab_spec.
    if not isinstance(spec,dict) or spec.get("supported") is not True:
        return "",False
    validate_lab_spec(spec)
    kind=str(spec["kind"]).upper()
    if kind=="FORMULA_CALCULATOR":
        raw=_render_formula(spec,lang_code,lab_id)
    elif kind=="ORIENTATION_INVARIANT":
        raw=_render_orientation(spec,lang_code,lab_id)
    elif kind=="SHAPE_RESPONSE":
        raw=_render_shape(spec,lang_code,lab_id)
    elif kind=="EVIDENCE_SEQUENCE":
        raw=_render_sequence(spec,lang_code,lab_id)
    elif kind=="EVIDENCE_REVEAL":
        raw=_render_evidence_reveal(spec,lang_code,lab_id)
    elif kind=="GEOMETRY_PROOF":
        raw,active=render_geometry_proof_lab(spec,lang_code,lab_id)
        if not active:
            return "",False
    elif kind in ADVANCED_LAB_KINDS:
        raw,active=render_advanced_verified_lab(spec,lang_code,lab_id)
        if not active:
            return "",False
    else:
        raise RuntimeError(f"LAB_KIND_UNSUPPORTED: {kind}")
    return _reference_contract_wrap(raw,spec,lang_code,lab_id),True
