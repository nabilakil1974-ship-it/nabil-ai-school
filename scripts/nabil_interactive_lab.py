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
from typing import Dict,Any,Tuple
try:
    from scripts.nabil_i18n import t as _t
    from scripts.nabil_advanced_lab import (
        ADVANCED_LAB_KINDS,
        render_advanced_verified_lab,
        validate_advanced_lab_spec,
    )
except Exception:
    from nabil_i18n import t as _t
    from nabil_advanced_lab import (
        ADVANCED_LAB_KINDS,
        render_advanced_verified_lab,
        validate_advanced_lab_spec,
    )

_ALLOWED_KINDS={"FORMULA_CALCULATOR","ORIENTATION_INVARIANT","SHAPE_RESPONSE","EVIDENCE_SEQUENCE"} | ADVANCED_LAB_KINDS
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

    if kind=="EVIDENCE_SEQUENCE":
        steps=spec.get("steps")
        if not isinstance(steps,list) or not 2<=len(steps)<=8:
            raise RuntimeError("LAB_SEQUENCE_STEPS_INVALID")
        for i,step in enumerate(steps):
            if not isinstance(step,dict) or not str(step.get("label") or "").strip() or not str(step.get("evidence_quote") or "").strip():
                raise RuntimeError(f"LAB_SEQUENCE_STEP_INVALID:{i}")
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

def render_verified_lab(spec:Dict[str,Any],lang_code:str,lab_id:str)->Tuple[str,bool]:
    # نقطة الدخول الوحيدة: المختبر لا يظهر قبل نجاح validate_lab_spec.
    if not isinstance(spec,dict) or spec.get("supported") is not True:
        return "",False
    validate_lab_spec(spec)
    kind=str(spec["kind"]).upper()
    if kind=="FORMULA_CALCULATOR":
        return _render_formula(spec,lang_code,lab_id),True
    if kind=="ORIENTATION_INVARIANT":
        return _render_orientation(spec,lang_code,lab_id),True
    if kind=="SHAPE_RESPONSE":
        return _render_shape(spec,lang_code,lab_id),True
    if kind=="EVIDENCE_SEQUENCE":
        return _render_sequence(spec,lang_code,lab_id),True
    if kind in ADVANCED_LAB_KINDS:
        return render_advanced_verified_lab(spec,lang_code,lab_id)
    raise RuntimeError(f"LAB_KIND_UNSUPPORTED: {kind}")
