#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NABIL AI - POWER_EXPLORER: a real, computing math lab for powers/exponents.

Unlike EVIDENCE_REVEAL (which only re-displays source text), the student types
numbers and the lab COMPUTES both sides of the rule with exact integer maths
(BigInt) and shows real superscripts and the repeated multiplication. It adds no
scientific claim: the rule it demonstrates must be quoted verbatim from the
source (evidence_quote), and the student chooses every value.
"""
from __future__ import annotations

import html
import json
import re
from typing import Any, Dict, List, Optional

LAWS = ("definition", "product_same_base", "quotient_same_base", "power_of_power",
        "product_same_exponent", "quotient_same_exponent", "scientific_notation")

_FIELDS = {
    "definition": ("a", "n"),
    "product_same_base": ("a", "m", "n"),
    "quotient_same_base": ("a", "m", "n"),
    "power_of_power": ("a", "m", "n"),
    "product_same_exponent": ("a", "b", "m"),
    "quotient_same_exponent": ("a", "b", "m"),
    "scientific_notation": ("a", "n"),
}
_SAMPLE = {
    "definition": {"a": "2", "n": "5"},
    "product_same_base": {"a": "2", "m": "3", "n": "2"},
    "quotient_same_base": {"a": "3", "m": "5", "n": "2"},
    "power_of_power": {"a": "2", "m": "3", "n": "2"},
    "product_same_exponent": {"a": "2", "b": "3", "m": "3"},
    "quotient_same_exponent": {"a": "6", "b": "3", "m": "2"},
    "scientific_notation": {"a": "3.2", "n": "4"},
}
_L = {
    "en": {"a": "Base a", "b": "Base b", "m": "Exponent m", "n": "Exponent n", "run": "Compute",
           "left": "Left side", "right": "Right side", "equal": "✓ Both sides are equal",
           "limit": "Use whole numbers; exponents up to 12 (6 for a power of a power).",
           "bad": "Enter valid numbers (b ≠ 0, and m ≥ n for a quotient).", "factors": "factors",
           "sci": "Digits a with 1 ≤ a < 10, e.g. 3.2"},
    "fr": {"a": "Base a", "b": "Base b", "m": "Exposant m", "n": "Exposant n", "run": "Calculer",
           "left": "Membre gauche", "right": "Membre droit", "equal": "✓ Les deux membres sont égaux",
           "limit": "Nombres entiers ; exposants jusqu'à 12 (6 pour une puissance de puissance).",
           "bad": "Entre des nombres valides (b ≠ 0, et m ≥ n pour un quotient).", "factors": "facteurs",
           "sci": "Chiffres a avec 1 ≤ a < 10, ex. 3,2"},
    "ar": {"a": "الأساس a", "b": "الأساس b", "m": "الأس m", "n": "الأس n", "run": "احسب",
           "left": "الطرف الأيسر", "right": "الطرف الأيمن", "equal": "✓ الطرفان متساويان",
           "limit": "أعداد صحيحة؛ الأسس حتى 12 (حتى 6 في قوة القوة).",
           "bad": "أدخل أعدادًا صحيحة (b ≠ 0، وm ≥ n في القسمة).", "factors": "عوامل",
           "sci": "رقم a حيث 1 ≤ a < 10، مثل 3.2"},
}
_SAY = {
    "en": ["Look at the two boxes: you choose the numbers.",
           "Watch how each side is built from repeated multiplication.",
           "Now compare the left side and the right side.",
           "Each side is just a different way of writing the same repeated product.",
           "Both sides give exactly the same number, so the rule holds."],
    "fr": ["Regarde les cases : c'est toi qui choisis les nombres.",
           "Observe comment chaque membre est construit par multiplications répétées.",
           "Compare maintenant le membre gauche et le membre droit.",
           "Chaque membre n'est qu'une autre écriture du même produit répété.",
           "Les deux membres donnent exactement le même nombre : la règle est vérifiée."],
    "ar": ["انظر إلى الخانتين: أنت من يختار الأعداد.",
           "لاحظ كيف يُبنى كل طرف بالضرب المتكرر.",
           "قارن الآن بين الطرف الأيسر والطرف الأيمن.",
           "كل طرف هو مجرد طريقة أخرى لكتابة الضرب المتكرر نفسه.",
           "الطرفان يعطيان العدد نفسه تمامًا، إذن القاعدة صحيحة."],
}
_SIGNAL = re.compile(
    r"\^|[⁰¹²³⁴⁵⁶⁷⁸⁹]|\bpowers?\b|\bexponent|\bindices\b|puissance|exposant|"
    r"الأس|أسس|الأسس|القوى|قوة|الترميز العلمي|scientific notation|notation scientifique",
    re.I)


def has_power_signal(title: str, raw_text: str) -> bool:
    return bool(_SIGNAL.search(f"{title}\n{raw_text}"))


def detect_law(title: str, raw_text: str) -> str:
    from scripts.nabil_factory.cards.mathtext import canonical_math
    t = canonical_math(f"{title}\n{raw_text}").casefold()
    if re.search(r"scientific notation|notation scientifique|الترميز العلمي|a × 10\^\{", t):
        return "scientific_notation"
    if re.search(r"\(\s*\w+\^\{[^}]+\}\s*\)\^\{|power of a power|puissance d.une puissance", t):
        return "power_of_power"
    if re.search(r"\(\s*\w+\s*×\s*\w+\s*\)\^\{", t):
        return "product_same_exponent"
    if re.search(r"\(\s*\w+\s*[/÷]\s*\w+\s*\)\^\{", t):
        return "quotient_same_exponent"
    if re.search(r"\^\{\s*\w+\s*\+\s*\w+\s*\}|same base.*(?:product|multipl)", t):
        return "product_same_base"
    if re.search(r"\^\{\s*\w+\s*-\s*\w+\s*\}|same base.*(?:quotient|divi)", t):
        return "quotient_same_base"
    return "definition"


def _quote(raw_text: str, title: str) -> str:
    lines = [ln.strip() for ln in re.split(r"[\n\r]+", str(raw_text or "")) if ln.strip()]
    for ln in lines:
        if _SIGNAL.search(ln) and len(ln) >= 8:
            return ln[:700]
    for ln in lines:
        if len(ln) >= 8:
            return ln[:700]
    return ""


def _teacher_script(spec_quote: str, lang: str) -> List[Dict[str, Any]]:
    say = _SAY.get(lang, _SAY["en"])
    def step(i, action, targets, before, after):
        return {"say": say[i], "target_ids": targets, "action": action,
                "state_before": before, "state_after": after,
                "scientific_constraints": ["Exact integer arithmetic; the student chooses every value."],
                "evidence_quote": spec_quote}
    return [
        step(0, "point", ["power_inputs"], {"computed": False}, {"computed": False}),
        step(1, "set_state", ["power_inputs"], {"computed": False}, {"computed": True}),
        step(2, "highlight", ["power_left", "power_right"], {"computed": True}, {"computed": True}),
        step(3, "explain", ["power_left", "power_right"], {"computed": True}, {"computed": True}),
        step(4, "conclude", ["power_right"], {"computed": True}, {"computed": True}),
    ]


def build_power_spec(title: str, raw_text: str, lang: str, concept_id: str) -> Optional[Dict[str, Any]]:
    """Deterministic spec; None when the source gives no quotable power content."""
    quote = _quote(raw_text, title)
    if not quote or not has_power_signal(title, raw_text):
        return None
    law = detect_law(title, raw_text)
    L = _L.get(lang, _L["en"])
    return {
        "supported": True, "kind": "POWER_EXPLORER", "law": law,
        "title": str(title or "Powers"),
        "instructions": {"en": "Type your own numbers and compute both sides.",
                         "fr": "Écris tes propres nombres et calcule les deux membres.",
                         "ar": "اكتب أعدادك بنفسك واحسب الطرفين."}.get(lang, "Type your own numbers and compute both sides."),
        "observation": {"en": "The lab computes with exact integers; nothing is pre-filled.",
                        "fr": "Le labo calcule avec des entiers exacts ; rien n'est prérempli.",
                        "ar": "المختبر يحسب بأعداد صحيحة دقيقة؛ لا قيم جاهزة."}.get(lang, "Exact integer arithmetic."),
        "evidence_ref": concept_id, "evidence_basis": "text", "evidence_quote": quote,
        "teacher_script": _teacher_script(quote, lang),
    }


def validate_power_spec(spec: Dict[str, Any]) -> None:
    if str(spec.get("law") or "") not in LAWS:
        raise RuntimeError("LAB_POWER_LAW_INVALID")


_JS = r"""
(()=>{
const SAFE='__SAFE__',LAW='__LAW__',LABELS=__LABELS__,SAMPLE=__SAMPLE__,FIELDS=__FIELDS__,FALLBACK='__LANG__';
const $=id=>document.getElementById(SAFE+'_'+id);
const lang=()=>{try{const l=parent.NABILPageLanguage&&parent.NABILPageLanguage.get&&parent.NABILPageLanguage.get();return LABELS[l]?l:FALLBACK}catch(e){return FALLBACK}};
const Lb=()=>LABELS[lang()];
function sup(host,text){ // "2^{3} × 2^{2}" -> real superscripts
  host.textContent='';let i=0,buf='';
  const flush=()=>{if(buf){host.appendChild(document.createTextNode(buf));buf=''}};
  while(i<text.length){
    if(text[i]==='^'&&text[i+1]==='{'){flush();let d=0,k=i+1;for(;k<text.length;k++){if(text[k]==='{')d++;else if(text[k]==='}'){d--;if(!d)break}}
      const s=document.createElement('sup');s.textContent=text.slice(i+2,k);host.appendChild(s);i=k+1}
    else buf+=text[i++];
  }
  flush();return host;
}
const P=(a,e)=>a**BigInt(e);
const ci=(v,hi)=>{const n=Number(v);return Number.isInteger(n)&&n>=0&&n<=hi?n:null};
const ai=v=>{const n=Number(v);return Number.isInteger(n)&&Math.abs(n)<=99?BigInt(n):null};
function chain(a,e){ // repeated multiplication, honest about long chains
  const s=String(a);if(e===0)return '1';if(e===1)return s;
  if(e<=6)return Array(e).fill(s).join(' × ');
  return s+' × '+s+' × … × '+s+' ('+e+' '+Lb().factors+')';
}
function shiftDecimal(str,n){ // exact decimal shift, no floating point
  let [ip,fp='']=str.split('.');let digits=ip+fp,point=ip.length+n;
  if(point<=0){digits='0'.repeat(1-point)+digits;point=1}
  if(point>digits.length)digits=digits+'0'.repeat(point-digits.length);
  let out=digits.slice(0,point),frac=digits.slice(point).replace(/0+$/,'');
  out=out.replace(/^0+(?=\d)/,'');return frac?out+'.'+frac:out;
}
function compute(v){
  const a=ai(v.a),b=ai(v.b);let L=null,R=null,eq=false;
  if(LAW==='definition'){const n=ci(v.n,12);if(a===null||n===null||(a===0n&&n===0))return null;
    const x=P(a,n);return {eq:true,single:true,expr:v.a+'^{'+n+'}',val:x.toString()}}
  if(LAW==='product_same_base'){const m=ci(v.m,12),n=ci(v.n,12);if(a===null||m===null||n===null)return null;
    L=[v.a+'^{'+m+'} × '+v.a+'^{'+n+'}',(P(a,m)*P(a,n)).toString()];R=[v.a+'^{'+(m+n)+'}',P(a,m+n).toString()]}
  if(LAW==='quotient_same_base'){const m=ci(v.m,12),n=ci(v.n,12);if(a===null||a===0n||m===null||n===null||m<n)return null;
    L=[v.a+'^{'+m+'} ÷ '+v.a+'^{'+n+'}',(P(a,m)/P(a,n)).toString()];R=[v.a+'^{'+(m-n)+'}',P(a,m-n).toString()]}
  if(LAW==='power_of_power'){const m=ci(v.m,6),n=ci(v.n,6);if(a===null||m===null||n===null)return null;
    L=['('+v.a+'^{'+m+'})^{'+n+'}',P(P(a,m),n).toString()];R=[v.a+'^{'+(m*n)+'}',P(a,m*n).toString()]}
  if(LAW==='product_same_exponent'){const m=ci(v.m,12);if(a===null||b===null||m===null)return null;
    L=['('+v.a+' × '+v.b+')^{'+m+'}',P(a*b,m).toString()];R=[v.a+'^{'+m+'} × '+v.b+'^{'+m+'}',(P(a,m)*P(b,m)).toString()]}
  if(LAW==='quotient_same_exponent'){const m=ci(v.m,12);if(a===null||b===null||b===0n||m===null)return null;
    const q=(Number(a)/Number(b))**m,r=Number(P(a,m))/Number(P(b,m));
    L=['('+v.a+' ÷ '+v.b+')^{'+m+'}',String(+q.toPrecision(10))];R=[v.a+'^{'+m+'} ÷ '+v.b+'^{'+m+'}',String(+r.toPrecision(10))]}
  if(LAW==='scientific_notation'){const n=Number(v.n);if(!/^\d(\.\d+)?$/.test(String(v.a).trim())||!Number.isInteger(n)||Math.abs(n)>12)return null;
    const val=shiftDecimal(String(v.a).trim(),n);L=[String(v.a).trim()+' × 10^{'+n+'}',val];R=[val,val]}
  if(!L)return null;
  return {L,R,eq:L[1]===R[1]};
}
function render(){
  const v={};FIELDS.forEach(f=>{v[f]=$(f).value.trim()});const out=$('out');out.textContent='';
  const res=compute(v);
  if(!res){out.textContent=Lb().bad;return}
  if(res.single){const d=document.createElement('div');d.className='pw-row';
    const e=document.createElement('div');e.className='pw-expr';sup(e,res.expr);
    const c=document.createElement('div');c.className='pw-chain';c.textContent=chain(v.a,Number(v.n))+' = '+res.val;
    d.append(e,c);out.appendChild(d);return}
  const box=(label,pair,id)=>{const d=document.createElement('div');d.className='pw-row';d.id=SAFE+'_'+id;
    const h=document.createElement('div');h.className='pw-h';h.textContent=label;
    const e=document.createElement('div');e.className='pw-expr';sup(e,pair[0]);
    const val=document.createElement('div');val.className='pw-val';val.textContent='= '+pair[1];
    d.append(h,e,val);return d};
  out.append(box(Lb().left,res.L,'left'),box(Lb().right,res.R,'right'));
  const s=document.createElement('div');s.className='pw-eq';s.textContent=res.eq?Lb().equal:'≠';out.appendChild(s);
}
function paintLabels(){FIELDS.forEach(f=>{const l=document.getElementById(SAFE+'_l_'+f);if(l)l.firstChild.nodeValue=Lb()[f]+' ';});
  const g=$('go');if(g)g.textContent=Lb().run;const n=$('note');if(n)n.textContent=Lb().limit}
FIELDS.forEach(f=>$(f).addEventListener('input',render));
$('go').addEventListener('click',render);
try{parent.addEventListener('nabil:page-language-change',()=>{paintLabels();render()})}catch(e){}
paintLabels();
document.getElementById('lab_'+SAFE).addEventListener('nabil:demo',()=>{FIELDS.forEach(f=>{$(f).value=SAMPLE[f]});render()});
})();
"""


def render_power_lab(spec: Dict[str, Any], lang_code: str, lab_id: str, safe: str) -> str:
    law = str(spec["law"])
    fields = _FIELDS[law]
    L = _L.get(lang_code, _L["en"])
    inputs = "".join(
        f'<label id="{safe}_l_{f}">{html.escape(L[f])} '
        f'<input id="{safe}_{f}" type="{"text" if (law == "scientific_notation" and f == "a") else "number"}" '
        f'inputmode="{"decimal" if (law == "scientific_notation" and f == "a") else "numeric"}" '
        f'style="width:100%;box-sizing:border-box;padding:10px;margin-top:4px;"></label>'
        for f in fields)
    js = (_JS.replace("__SAFE__", safe).replace("__LAW__", law)
          .replace("__LABELS__", json.dumps(_L, ensure_ascii=False))
          .replace("__SAMPLE__", json.dumps(_SAMPLE[law]))
          .replace("__FIELDS__", json.dumps(list(fields)))
          .replace("__LANG__", lang_code if lang_code in _L else "en"))
    css = ("#lab_%s .pw-row{margin-top:10px;padding:10px;border-radius:10px;background:#06223a;"
           "border:1px solid #1b6a96}#lab_%s .pw-h{font-size:12px;color:#9ccbe4;font-weight:800}"
           "#lab_%s .pw-expr{font-size:26px;font-weight:800;direction:ltr;unicode-bidi:isolate;color:#ffd447}"
           "#lab_%s .pw-expr sup{font-size:.62em}#lab_%s .pw-val,#lab_%s .pw-chain{font-size:18px;direction:ltr;"
           "unicode-bidi:isolate;overflow-wrap:anywhere;color:#eef8ff}#lab_%s .pw-eq{margin-top:10px;font-weight:900;"
           "color:#7dffb2}") % ((safe,) * 7)
    return f"""
    <section class="interactive-lab nabil-live-lab" id="lab_{safe}" data-lab-kind="POWER_EXPLORER" data-law="{law}" data-demo-ms="9000"
      style="margin-top:16px;background:#f0f9ff;border:1px solid #7dd3fc;border-radius:12px;padding:16px;">
      <style>{css}</style>
      <h3 style="margin:0 0 8px;">{html.escape(str(spec["title"]))}</h3>
      <p style="margin:0 0 12px;">{html.escape(str(spec["instructions"]))}</p>
      <div id="{safe}_inputs" style="display:grid;grid-template-columns:repeat({min(len(fields), 3)},1fr);gap:10px;">{inputs}</div>
      <button type="button" class="nav-btn" id="{safe}_go" style="margin-top:12px;">{html.escape(L["run"])}</button>
      <div id="{safe}_out" aria-live="polite" style="margin-top:8px;"></div>
      <p id="{safe}_note" style="font-size:12px;margin:10px 0 0;">{html.escape(L["limit"])}</p>
      <p style="font-size:12px;margin:6px 0 0;">{html.escape(str(spec["observation"]))}</p>
      <script>{js}</script>
    </section>"""
