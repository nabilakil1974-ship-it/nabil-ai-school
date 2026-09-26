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
import re
from typing import Dict,Any,Tuple
try:
    from scripts.nabil_i18n import t as _t
except Exception:
    from nabil_i18n import t as _t

_ALLOWED_KINDS={"FORMULA_CALCULATOR","ORIENTATION_INVARIANT","SHAPE_RESPONSE"}
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
    return spec

def _render_formula(spec:Dict[str,Any],lang_code:str,lab_id:str)->str:
    # مختبر العلاقة الرياضية: لا قيم جاهزة. يدخل الطالب القيم ويرى النتيجة الحقيقية.
    f=spec["formula"]; safe=_safe_id(lab_id); op=f["operator"]
    js_expr={"+":"a+b","-":"a-b","*":"a*b","/":"(b===0?NaN:a/b)"}[op]
    output=html.escape(str(f["output"]))
    unit=html.escape(str(f.get("output_unit") or ""))
    unit_suffix=(" "+unit) if unit else ""
    return f"""
    <section class="interactive-lab" id="lab_{safe}" data-lab-kind="FORMULA_CALCULATOR"
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
      </script>
    </section>"""

def _render_orientation(spec:Dict[str,Any],lang_code:str,lab_id:str)->str:
    # مختبر اتجاه/ثبات بصري: الميل يغيّر الجسم، أما العنصر الذي تثبت قاعدته العلمية فيبقى وفق المواصفة.
    safe=_safe_id(lab_id)
    orient=str(spec["invariant_orientation"]).lower()
    transform="rotate(0 150 95)" if orient=="horizontal" else "rotate(90 150 95)"
    return f"""
    <section class="interactive-lab" id="lab_{safe}" data-lab-kind="ORIENTATION_INVARIANT"
      style="margin-top:16px;background:#f0f9ff;border:1px solid #7dd3fc;border-radius:12px;padding:16px;">
      <h3 style="margin:0 0 8px;color:#0369a1;">{html.escape(_t(lang_code,'lab_title'))} — {html.escape(spec['title'])}</h3>
      <p style="margin:0 0 10px;color:#334155;">{html.escape(spec['instructions'])}</p>
      <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px;">
        <button type="button" class="q-opt" onclick="tilt_{safe}(-1)">↙</button>
        <button type="button" class="q-opt" onclick="tilt_{safe}(0)">●</button>
        <button type="button" class="q-opt" onclick="tilt_{safe}(1)">↘</button>
      </div>
      <svg viewBox="0 0 300 190" role="img" aria-label="{html.escape(spec['title'])}" style="width:100%;max-width:520px;background:#fff;border-radius:10px;border:1px solid #cbd5e1;">
        <g id="{safe}_moving" transform="rotate(0 150 100)">
          <path d="M75 45 L225 45 L205 155 L95 155 Z" fill="none" stroke="#334155" stroke-width="5"/>
        </g>
        <line x1="98" y1="95" x2="202" y2="95" stroke="#0284c7" stroke-width="7" transform="{transform}"/>
      </svg>
      <p style="font-size:12px;color:#475569;margin:10px 0 0;">{html.escape(spec['observation'])}</p>
      <script>
      function tilt_{safe}(dir){{
        const angle=dir<0?-18:(dir>0?18:0);
        document.getElementById('{safe}_moving').setAttribute('transform','rotate('+angle+' 150 100)');
      }}
      </script>
    </section>"""

def _render_shape(spec:Dict[str,Any],lang_code:str,lab_id:str)->str:
    # مختبر استجابة الشكل: يغيّر الطالب الوعاء، والسلوك المرئي يأتي من behavior الموثق لا من تخمين المحرك.
    safe=_safe_id(lab_id); fixed=str(spec["behavior"]).lower()=="fixed"
    fixed_js="true" if fixed else "false"
    return f"""
    <section class="interactive-lab" id="lab_{safe}" data-lab-kind="SHAPE_RESPONSE"
      style="margin-top:16px;background:#f0f9ff;border:1px solid #7dd3fc;border-radius:12px;padding:16px;">
      <h3 style="margin:0 0 8px;color:#0369a1;">{html.escape(_t(lang_code,'lab_title'))} — {html.escape(spec['title'])}</h3>
      <p style="margin:0 0 10px;color:#334155;">{html.escape(spec['instructions'])}</p>
      <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px;">
        <button type="button" class="q-opt" onclick="shape_{safe}('wide')">A</button>
        <button type="button" class="q-opt" onclick="shape_{safe}('narrow')">B</button>
      </div>
      <svg viewBox="0 0 320 190" style="width:100%;max-width:520px;background:#fff;border-radius:10px;border:1px solid #cbd5e1;">
        <path id="{safe}_vessel" d="M70 40 L250 40 L230 160 L90 160 Z" fill="none" stroke="#334155" stroke-width="5"/>
        <rect id="{safe}_matter" x="115" y="95" width="90" height="55" rx="8" fill="#7dd3fc" opacity="0.85"/>
      </svg>
      <p style="font-size:12px;color:#475569;margin:10px 0 0;">{html.escape(spec['observation'])}</p>
      <script>
      function shape_{safe}(kind){{
        const vessel=document.getElementById('{safe}_vessel');
        const matter=document.getElementById('{safe}_matter');
        vessel.setAttribute('d',kind==='wide'?'M70 40 L250 40 L230 160 L90 160 Z':'M115 35 L205 35 L190 160 L130 160 Z');
        const fixed={fixed_js};
        if(!fixed){{
          if(kind==='wide'){{matter.setAttribute('x','96');matter.setAttribute('width','128');}}
          else{{matter.setAttribute('x','132');matter.setAttribute('width','56');}}
        }}
      }}
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
    raise RuntimeError(f"LAB_KIND_UNSUPPORTED: {kind}")
