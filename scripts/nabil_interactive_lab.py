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
   function play(){{
     stopAll();const mine=token;let i=0;
     const next=()=>{{
       if(mine!==token||i>=labels.length)return;
       focus(i);
       try{{window.NABILLessonE2E?.speak?.(labels[i],{json.dumps(lang_code)});}}catch(_e){{}}
       i++;timers.push(setTimeout(next,2800));
     }};next();
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
   function speakCurrent(){{
     focus(index);
     try{{window.NABILLessonE2E?.speak?.(labels[index],{json.dumps(lang_code)});}}catch(_e){{}}
   }}
   function play(){{
     stopAll();const mine=token;index=0;
     const next=()=>{{
       if(mine!==token||index>=labels.length)return;
       speakCurrent();index++;timers.push(setTimeout(next,2400));
     }};next();
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



def _render_geometry_proof(spec:Dict[str,Any],lang_code:str,lab_id:str)->str:
    """Deterministic geometry proof board with evidence-gated visual marks.

    Coordinates are presentation-only. Mathematical claims come exclusively
    from validated relations/steps. Marks remain hidden until their proof step.
    """
    safe=_safe_id(lab_id)
    pts={}
    for p in spec["points"]:
        pts[str(p["label"])]=(60.0+5.2*float(p["x"]), 42.0+3.45*float(p["y"]))
    segs={str(seg["id"]):seg for seg in spec["segments"]}
    marks=spec.get("marks") or []
    steps=spec.get("proof_steps") or []

    def esc_id(v):
        return _safe_id(str(v))
    def line_xy(sid):
        seg=segs[sid]; return pts[str(seg["a"])],pts[str(seg["b"])]
    def norm_vec(a,b):
        dx=b[0]-a[0];dy=b[1]-a[1];L=math.hypot(dx,dy) or 1.0
        return dx/L,dy/L
    def tick_markup(sid,count=1):
        a,b=line_xy(sid); ux,uy=norm_vec(a,b); nx,ny=-uy,ux
        mx,my=(a[0]+b[0])/2,(a[1]+b[1])/2
        out=[]
        for k in range(count):
            off=(k-(count-1)/2)*8
            cx,cy=mx+ux*off,my+uy*off
            out.append(
                f'<line x1="{cx-nx*7:.1f}" y1="{cy-ny*7:.1f}" '
                f'x2="{cx+nx*7:.1f}" y2="{cy+ny*7:.1f}" '
                'stroke="#ffd76b" stroke-width="3.2" stroke-linecap="round"/>'
            )
        return "".join(out)
    def parallel_markup(sid,count=1):
        a,b=line_xy(sid);ux,uy=norm_vec(a,b);nx,ny=-uy,ux
        mx,my=(a[0]+b[0])/2,(a[1]+b[1])/2
        out=[]
        for k in range(count):
            off=(k-(count-1)/2)*12
            cx,cy=mx+ux*off,my+uy*off
            p1=(cx-ux*8+nx*6,cy-uy*8+ny*6)
            p2=(cx,cy)
            p3=(cx-ux*8-nx*6,cy-uy*8-ny*6)
            out.append(
                f'<path d="M{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} '
                f'L{p3[0]:.1f},{p3[1]:.1f}" fill="none" stroke="#c891ff" '
                'stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
            )
        return "".join(out)
    def angle_arc(angle,r=28.0):
        A=pts[str(angle["a"])];V=pts[str(angle["vertex"])];B=pts[str(angle["b"])]
        a1=math.atan2(A[1]-V[1],A[0]-V[0]);a2=math.atan2(B[1]-V[1],B[0]-V[0])
        d=a2-a1
        while d>math.pi:d-=2*math.pi
        while d<-math.pi:d+=2*math.pi
        p1=(V[0]+r*math.cos(a1),V[1]+r*math.sin(a1))
        p2=(V[0]+r*math.cos(a1+d),V[1]+r*math.sin(a1+d))
        sweep=1 if d>0 else 0
        return (
            f'<path d="M{p1[0]:.1f},{p1[1]:.1f} A{r:.1f},{r:.1f} 0 0 {sweep} '
            f'{p2[0]:.1f},{p2[1]:.1f}" fill="none" stroke="#c891ff" '
            'stroke-width="4" stroke-linecap="round"/>'
        )
    def right_angle_markup(angle,size=14.0):
        A=pts[str(angle["a"])];V=pts[str(angle["vertex"])];B=pts[str(angle["b"])]
        u=norm_vec(V,A);v=norm_vec(V,B)
        p1=(V[0]+u[0]*size,V[1]+u[1]*size)
        p2=(p1[0]+v[0]*size,p1[1]+v[1]*size)
        p3=(V[0]+v[0]*size,V[1]+v[1]*size)
        return (
            f'<path d="M{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} '
            f'L{p3[0]:.1f},{p3[1]:.1f}" fill="none" stroke="#55e6a4" '
            'stroke-width="3.2" stroke-linejoin="round"/>'
        )

    base_segments=[]
    for sid,seg in segs.items():
        a,b=pts[str(seg["a"])],pts[str(seg["b"])]
        base_segments.append(
            f'<line id="{safe}_seg_{esc_id(sid)}" data-geom-target="{html.escape(sid)}" '
            f'x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" '
            'stroke="#e7f4ff" stroke-width="3" stroke-linecap="round"/>'
        )
    point_markup=[]
    for label,(x,y) in pts.items():
        point_markup.append(
            f'<g id="{safe}_point_{esc_id(label)}" data-geom-target="{html.escape(label)}">'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="#2de1ff" stroke="#fff" stroke-width="1.5"/>'
            f'<text x="{x+9:.1f}" y="{y-8:.1f}" fill="#f8fbff" font-size="14" font-weight="800">'
            f'{html.escape(label)}</text></g>'
        )

    mark_markup=[]
    mark_index={}
    for idx,mark in enumerate(marks):
        mid=str(mark.get("id") or f"M{idx+1}")
        mark_index[mid]=idx
        mtype=str(mark["type"]).lower()
        body=""
        if mtype in {"equal_segments","midpoint"}:
            count=1+(idx%2)
            body="".join(tick_markup(str(s),count) for s in mark.get("targets") or [])
        elif mtype=="parallel":
            count=1+(idx%2)
            body="".join(parallel_markup(str(s),count) for s in mark.get("targets") or [])
        elif mtype=="equal_angles":
            body="".join(angle_arc(a,26+4*(idx%2)) for a in mark.get("angles") or [])
        elif mtype=="perpendicular":
            body="".join(right_angle_markup(a) for a in mark.get("angles") or [])
        elif mtype=="symmetry_axis":
            a,b=line_xy(str(mark["axis_segment"]))
            body=(
                f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" '
                'stroke="#ffd76b" stroke-width="8" stroke-linecap="round" opacity=".34" '
                'stroke-dasharray="12 8"/>'
            )
            for pair in mark.get("point_pairs") or []:
                p1,p2=pts[str(pair[0])],pts[str(pair[1])]
                body+=(
                    f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" '
                    'stroke="#c891ff" stroke-width="2" stroke-dasharray="5 6" opacity=".8"/>'
                )
        mark_markup.append(
            f'<g id="{safe}_mark_{idx}" data-geom-mark="{html.escape(mid)}" '
            f'data-mark-type="{html.escape(mtype)}" opacity="0">{body}</g>'
        )

    proof_json=[]
    for step in steps:
        proof_json.append({
            "title":str(step.get("title") or ""),
            "text":str(step.get("text") or ""),
            "formula":str(step.get("formula") or ""),
            "target_ids":[str(x) for x in (step.get("target_ids") or [])],
            "reveal_marks":[str(x) for x in (step.get("reveal_marks") or [])],
        })

    L={
        "ar":{"prev":"◀ السابق","next":"التالي ▶","speak":"🔊 اشرح هذه الخطوة",
              "play":"▶ اشرح من البداية","stop":"■ أوقف الشرح","reset":"↺ إعادة",
              "teacher":"نبيل يشرح الآن","step":"الخطوة","hint":"اتبع العلامات التي تظهر مع البرهان."},
        "fr":{"prev":"◀ Précédent","next":"Suivant ▶","speak":"🔊 Expliquer cette étape",
              "play":"▶ Expliquer depuis le début","stop":"■ Arrêter","reset":"↺ Réinitialiser",
              "teacher":"NABIL explique","step":"Étape","hint":"Suis les marques qui apparaissent avec la démonstration."},
        "en":{"prev":"◀ Previous","next":"Next ▶","speak":"🔊 Explain this step",
              "play":"▶ Explain from the beginning","stop":"■ Stop","reset":"↺ Reset",
              "teacher":"NABIL is explaining","step":"Step","hint":"Follow the marks as the proof establishes them."},
    }.get(lang_code)
    if not L:
        L={"prev":"◀ Previous","next":"Next ▶","speak":"🔊 Explain this step",
           "play":"▶ Explain from the beginning","stop":"■ Stop","reset":"↺ Reset",
           "teacher":"NABIL is explaining","step":"Step","hint":"Follow the marks as the proof establishes them."}

    return f"""
<section class="interactive-lab nabil-live-lab nabil-geometry-proof" id="lab_{safe}"
 data-lab-kind="GEOMETRY_PROOF" data-demo-ms="{max(7000,len(steps)*3300)}"
 data-renderer-contract="NABIL_REFERENCE_RENDERER_V1" data-teacher-pointer="sentence-synced"
 data-visual-proof-marks="equal_segments,equal_angles,perpendicular,parallel,midpoint,symmetry_axis">
 <style>
 #lab_{safe}{{background:#071827!important;color:#f8fbff!important;border:1px solid #24506f!important;border-radius:16px!important;padding:12px!important}}
 #lab_{safe} .geom-layout{{display:grid;grid-template-columns:minmax(0,1.45fr) minmax(250px,.75fr);gap:12px}}
 #lab_{safe} .geom-stage{{position:relative;background:#020912;border:1px solid #1c4569;border-radius:14px;overflow:hidden}}
 #lab_{safe} .geom-stage svg{{width:100%;height:auto;max-height:560px;background:#020912!important}}
 #lab_{safe} .geom-teacher{{position:absolute;top:8px;right:8px;z-index:4;background:#061725e8;border:1px solid #2b6485;border-radius:999px;padding:5px 9px;color:#dffaff;font-size:11px;font-weight:800}}
 #lab_{safe} .geom-proof{{background:#061725;border:1px solid #1a3b55;border-radius:13px;padding:12px;min-height:210px}}
 #lab_{safe} .geom-proof h4{{margin:5px 0;color:#ffd76b}}
 #lab_{safe} .geom-formula{{direction:ltr;text-align:center;background:#03111d;border:1px dashed #315d79;border-radius:9px;padding:8px;margin-top:9px;font-family:"Cambria Math",serif;font-size:17px}}
 #lab_{safe} .geom-controls{{display:flex;gap:7px;flex-wrap:wrap;margin-top:10px}}
 #lab_{safe} .geom-controls button{{min-height:44px;border:1px solid #426d8b;background:#153955;color:#fff;border-radius:10px;padding:8px 10px;font-weight:800}}
 #lab_{safe} .geom-controls .primary{{background:#0f766e;border-color:#39c7b0}}
 #lab_{safe} .geom-controls .stop{{background:#5a2330;border-color:#bd546b}}
 #lab_{safe} .geom-timeline{{display:flex;gap:5px;flex-wrap:wrap;margin-top:10px}}
 #lab_{safe} .geom-dot{{width:31px;height:31px;min-height:31px;border-radius:50%;display:grid;place-items:center;background:#071725;border:1px solid #31506b;color:#8fa7ba;padding:0}}
 #lab_{safe} .geom-dot.on{{background:#0b5d70;border-color:#2de1ff;color:#fff;box-shadow:0 0 12px #2de1ff66}}
 #lab_{safe} .geom-dot.done{{background:#0d4c3c;border-color:#55e6a4;color:#dffff0}}
 #lab_{safe} .geom-focus{{filter:drop-shadow(0 0 8px #2de1ff);stroke:#2de1ff!important;stroke-width:5!important}}
 #lab_{safe} .geom-mark-on{{opacity:1!important;transition:opacity .28s ease}}
 #lab_{safe} .geom-arrow{{stroke:#2de1ff;stroke-width:3;stroke-dasharray:8 6;animation:{safe}_dash .8s linear infinite}}
 @keyframes {safe}_dash{{to{{stroke-dashoffset:-28}}}}
 @media(max-width:720px){{#lab_{safe} .geom-layout{{grid-template-columns:1fr}}}}
 </style>
 <h3 style="margin:0 0 6px;color:#2de1ff">{html.escape(str(spec["title"]))}</h3>
 <p style="margin:0 0 10px;color:#cfeeff">{html.escape(str(spec["instructions"]))}</p>
 <div class="geom-layout">
  <div>
   <div class="geom-stage">
    <div class="geom-teacher">● {html.escape(L["teacher"])}</div>
    <svg id="{safe}_geom_svg" viewBox="0 0 640 440" role="img" aria-label="{html.escape(str(spec["title"]))}">
     <defs><marker id="{safe}_geom_arrow_head" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3z" fill="#2de1ff"/></marker></defs>
     <rect width="640" height="440" fill="#020912"/>
     <g opacity=".32" stroke="#0b2944" stroke-width="1">{"".join(f'<path d="M{x} 0V440"/>' for x in range(40,640,40))}{"".join(f'<path d="M0 {y}H640"/>' for y in range(40,440,40))}</g>
     {"".join(base_segments)}
     {"".join(point_markup)}
     {"".join(mark_markup)}
     <line id="{safe}_geom_arrow" class="geom-arrow" x1="603" y1="48" x2="520" y2="105" marker-end="url(#{safe}_geom_arrow_head)"/>
    </svg>
   </div>
   <div class="geom-controls">
    <button id="{safe}_geom_prev">{html.escape(L["prev"])}</button>
    <button class="primary" id="{safe}_geom_next">{html.escape(L["next"])}</button>
    <button id="{safe}_geom_speak">{html.escape(L["speak"])}</button>
    <button class="primary" id="{safe}_geom_play">{html.escape(L["play"])}</button>
    <button class="stop" id="{safe}_geom_stop">{html.escape(L["stop"])}</button>
    <button id="{safe}_geom_reset">{html.escape(L["reset"])}</button>
   </div>
   <div class="geom-timeline" id="{safe}_geom_timeline"></div>
   <div style="margin-top:8px;color:#9fb5c9;font-size:12px">{html.escape(L["hint"])}</div>
  </div>
  <aside class="geom-proof">
   <div style="display:flex;justify-content:space-between;gap:8px"><b id="{safe}_geom_badge"></b><span id="{safe}_geom_count" style="color:#9fb5c9;font-size:12px"></span></div>
   <h4 id="{safe}_geom_title"></h4>
   <div id="{safe}_geom_text" style="line-height:1.7"></div>
   <div class="geom-formula" id="{safe}_geom_formula"></div>
  </aside>
 </div>
 <p style="font-size:12px;color:#b6c8d8;margin:10px 0 0">{html.escape(str(spec["observation"]))}</p>
 <script>
 (()=>{{
  const root=document.getElementById('lab_{safe}');
  const steps={json.dumps(proof_json,ensure_ascii=False)};
  const markIndex={json.dumps(mark_index,ensure_ascii=False)};
  let step=0,token=0,timers=[];
  const q=id=>document.getElementById(id);
  function stop(){{
    token++;timers.forEach(clearTimeout);timers=[];
    try{{window.NABILLessonE2E?.stopSpeech?.();}}catch(_e){{}}
  }}
  function targetNode(id){{
    return q('{safe}_seg_'+String(id).replace(/[^a-zA-Z0-9_]/g,'_'))
      ||q('{safe}_point_'+String(id).replace(/[^a-zA-Z0-9_]/g,'_'))
      ||(markIndex[id]!==undefined?q('{safe}_mark_'+markIndex[id]):null);
  }}
  function pointTo(id){{
    const svg=q('{safe}_geom_svg'),arrow=q('{safe}_geom_arrow'),node=targetNode(id);
    root.querySelectorAll('.geom-focus').forEach(n=>n.classList.remove('geom-focus'));
    if(!svg||!arrow||!node)return;
    node.classList.add('geom-focus');
    let bb;
    try{{bb=node.getBBox();}}catch(_e){{return;}}
    arrow.setAttribute('x2',bb.x+bb.width/2);arrow.setAttribute('y2',bb.y+bb.height/2);
  }}
  function revealThrough(index){{
    root.querySelectorAll('.nabil-geom-mark').forEach(n=>n.classList.remove('geom-mark-on'));
    for(let i=0;i<=index;i++){{
      (steps[i]?.reveal_marks||[]).forEach(mid=>{{
        const mi=markIndex[mid];if(mi!==undefined)q('{safe}_mark_'+mi)?.classList.add('geom-mark-on');
      }});
    }}
  }}
  function render(){{
    const s=steps[step];if(!s)return;
    q('{safe}_geom_badge').textContent={json.dumps(L["step"])}+' '+(step+1);
    q('{safe}_geom_count').textContent=(step+1)+' / '+steps.length;
    q('{safe}_geom_title').textContent=s.title;
    q('{safe}_geom_text').textContent=s.text;
    q('{safe}_geom_formula').textContent=s.formula||'';
    q('{safe}_geom_formula').style.display=s.formula?'block':'none';
    revealThrough(step);
    pointTo((s.target_ids||[])[0]||'');
    root.querySelectorAll('.geom-dot').forEach((n,i)=>n.className='geom-dot '+(i<step?'done':i===step?'on':''));
  }}
  function sentenceParts(text){{
    const parts=String(text||'').split(/(?<=[.!?؟؛])\\s+/).map(x=>x.trim()).filter(Boolean);
    return parts.length?parts:[String(text||'').trim()].filter(Boolean);
  }}
  function explainCurrent(done){{
    stop();const mine=token;render();
    const s=steps[step],parts=sentenceParts(s.text),targets=s.target_ids||[];
    let i=0;
    const next=()=>{{
      if(mine!==token)return;
      if(i>=parts.length){{if(done)done();return;}}
      pointTo(targets[Math.min(i,Math.max(0,targets.length-1))]||targets[0]||'');
      try{{window.NABILLessonE2E?.speak?.(parts[i],{json.dumps(lang_code)});}}catch(_e){{}}
      const wait=Math.max(1600,parts[i].split(/\\s+/).length*330);i++;
      timers.push(setTimeout(next,wait));
    }};
    next();
  }}
  function playAll(){{
    stop();const mine=token;step=0;
    const run=()=>{{
      if(mine!==token)return;render();
      explainCurrent(()=>{{
        if(mine!==token)return;
        if(step<steps.length-1){{step++;timers.push(setTimeout(run,280));}}
      }});
    }};run();
  }}
  function timeline(){{
    const box=q('{safe}_geom_timeline');box.innerHTML='';
    steps.forEach((_,i)=>{{const b=document.createElement('button');b.className='geom-dot';b.textContent=i+1;b.onclick=()=>{{stop();step=i;render();}};box.appendChild(b);}});
  }}
  q('{safe}_geom_prev').onclick=()=>{{stop();step=(step+steps.length-1)%steps.length;render();}};
  q('{safe}_geom_next').onclick=()=>{{stop();step=(step+1)%steps.length;render();}};
  q('{safe}_geom_speak').onclick=()=>explainCurrent();
  q('{safe}_geom_play').onclick=playAll;
  q('{safe}_geom_stop').onclick=stop;
  q('{safe}_geom_reset').onclick=()=>{{stop();step=0;render();}};
  root.addEventListener('nabil:demo',playAll);
  timeline();render();
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
    cues=[]
    kind=str(spec.get("kind") or "").upper()
    if kind=="EVIDENCE_SEQUENCE":
        cues=[str(x.get("label") or "").strip() for x in spec.get("steps") or []]
    elif kind=="EVIDENCE_REVEAL":
        cues=[str(x.get("label") or "").strip() for x in spec.get("items") or []]
    else:
        cues=[
            str(spec.get("instructions") or "").strip(),
            str(spec.get("observation") or "").strip(),
        ]
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
   let cueIndex=0,token=0;
   function targets(){{
     if(!inner)return [];
     const preferred=[...inner.querySelectorAll(
       '.nabil-seq-step,.nabil-reveal-item,svg,input,select,[id$="_result"],p'
     )].filter(x=>x.offsetParent!==null);
     return preferred.length?preferred:[inner];
   }}
   function point(index){{
     const list=targets();if(!list.length||!line)return;
     const target=list[Math.max(0,Math.min(index,list.length-1))];
     shell.querySelectorAll('.nabil-ref-focused').forEach(x=>x.classList.remove('nabil-ref-focused'));
     target.classList.add('nabil-ref-focused');
     const sr=shell.getBoundingClientRect(),tr=target.getBoundingClientRect();
     const x2=Math.max(18,Math.min(sr.width-18,tr.left-sr.left+tr.width/2));
     const y2=Math.max(52,Math.min(sr.height-18,tr.top-sr.top+Math.min(tr.height/2,60)));
     line.setAttribute('x2',x2);line.setAttribute('y2',y2);
   }}
   async function speakCue(index){{
     if(!cues.length)return;
     cueIndex=((index%cues.length)+cues.length)%cues.length;
     point(cueIndex);
     try{{await Promise.resolve(window.NABILLessonE2E?.speak?.(cues[cueIndex],{json.dumps(lang_code)}));}}catch(_e){{}}
   }}
   async function playAll(){{
     token++;const mine=token;
     for(let i=0;i<cues.length;i++){{
       if(mine!==token)return;
       await speakCue(i);
       if(mine!==token)return;
       await new Promise(r=>setTimeout(r,260));
     }}
   }}
   document.getElementById('{safe}_ref_current')?.addEventListener('click',()=>{{token++;speakCue(cueIndex);}});
   document.getElementById('{safe}_ref_all')?.addEventListener('click',playAll);
   document.getElementById('{safe}_ref_stop')?.addEventListener('click',()=>{{token++;try{{window.NABILLessonE2E?.stopSpeech?.()}}catch(_e){{}}}});
   inner?.addEventListener('nabil:demo',()=>{{cueIndex=0;point(0);}});
   window.addEventListener('resize',()=>point(cueIndex),{{passive:true}});
   requestAnimationFrame(()=>point(0));
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
        return raw,True
    elif kind in ADVANCED_LAB_KINDS:
        raw,active=render_advanced_verified_lab(spec,lang_code,lab_id)
        if not active:
            return "",False
    else:
        raise RuntimeError(f"LAB_KIND_UNSUPPORTED: {kind}")
    return _reference_contract_wrap(raw,spec,lang_code,lab_id),True
