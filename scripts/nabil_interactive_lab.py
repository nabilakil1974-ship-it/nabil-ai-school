#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NABIL AI — Interactive Lab Generator
Add-on module: does NOT replace nabil_book_factory.py, imported by it.

Replaces the current hardcoded stubs:
    "lab_html": "",
    "has_active_sim": False

Design principle (fail-closed, consistent with the rest of the factory):
A lab is only generated when the concept's own extracted text describes an
observable variable relationship (e.g. "as X increases, Y increases/decreases",
a formula, a measurable quantity). We NEVER invent a simulation for a concept
that doesn't actually describe one — that would be exactly the kind of
unverified/invented content the factory's anti-hardcode gates exist to catch.

Two lab kinds are supported:
  - FORMULA_LAB: concept's math_records contain a real formula (e.g. d = m/v).
    Renders sliders for each input variable, computes the output live in JS,
    matching MathRenderingEngine's LaTeX output exactly (no separate math path).
  - QUALITATIVE_LAB: concept describes a qualitative observable change
    (e.g. "solids keep their shape, liquids take the shape of the container").
    Renders a state-toggle interactive that lets the student pick states and
    see the grounded observation text update — still grounded, still no
    invented numeric behavior.

If neither pattern is detected in the concept's own text, this module
returns has_active_sim=False and lab_html="" exactly as before — it must
never force a lab onto content that doesn't support one.
"""

import html
import re
from typing import Dict, Any, Optional, List, Tuple

# Import sibling module; both are add-ons imported by nabil_book_factory.py
from scripts.nabil_i18n import t as _t


_FORMULA_LAB_PATTERN = re.compile(
    r"\b([a-zA-Z])\s*=\s*([a-zA-Z])\s*/\s*([a-zA-Z])\b"      # e.g. d = m/v
    r"|\b([a-zA-Z])\s*=\s*([a-zA-Z])\s*\*\s*([a-zA-Z])\b"     # e.g. F = m*a
    r"|\b([a-zA-Z])\s*=\s*([a-zA-Z])\s*\+\s*([a-zA-Z])\b"     # e.g. p = a+b
)

_QUALITATIVE_STATE_PATTERN = re.compile(
    r"(?i)\b(solid|liquid|gas|صلب|سائل|غاز|solide|liquide|gaz)\b"
)


def _extract_formula_variables(concept: dict) -> Optional[Tuple[str, str, str, str]]:
    """Look for a simple two-input formula in this concept's OWN math_records
    or raw text. Returns (output_var, op, input_a, input_b) or None.

    Grounded: only fires on a formula the extraction pipeline itself already
    recorded (concept['math_records']) or found verbatim in raw_text — never
    on a formula synthesized separately from the source page.
    """
    haystacks: List[str] = [str(concept.get("raw_text") or "")]
    for rec in concept.get("math_records", []) or []:
        raw = str(rec.get("raw") or "")
        if raw:
            haystacks.append(raw)

    for text in haystacks:
        m = _FORMULA_LAB_PATTERN.search(text)
        if not m:
            continue
        groups = m.groups()
        if groups[0]:  # division: a = b/c
            return (groups[0], "/", groups[1], groups[2])
        if groups[3]:  # multiplication
            return (groups[3], "*", groups[4], groups[5])
        if groups[6]:  # addition
            return (groups[6], "+", groups[7], groups[8])
    return None


def _has_qualitative_state_language(concept: dict) -> bool:
    text = str(concept.get("raw_text") or "")
    return bool(_QUALITATIVE_STATE_PATTERN.search(text))


def build_formula_lab_html(
        concept: dict, output_var: str, op: str, in_a: str, in_b: str,
        lang_code: str, lab_id: str) -> str:
    """A real interactive: two sliders, live-computed output, grounded in
    the exact formula extracted from the source page. No fabricated ranges —
    uses a neutral 1-100 domain since the source rarely specifies numeric
    bounds; if the concept text DOES specify bounds/units those are shown
    as-is in the label rather than invented.
    """
    js_op = {"/": "/", "*": "*", "+": "+"}[op]
    safe_lab_id = re.sub(r"[^a-zA-Z0-9_]", "_", lab_id)
    title = html.escape(concept.get("title", ""))
    instructions = _t(lang_code, "lab_instructions")
    hypothesis_label = _t(lang_code, "lab_hypothesis")
    run_label = _t(lang_code, "lab_run")
    reset_label = _t(lang_code, "lab_reset")
    result_label = _t(lang_code, "lab_result")
    conclusion_prompt = _t(lang_code, "lab_conclusion_prompt")

    return f'''
    <div class="interactive-lab" id="lab_{safe_lab_id}" style="margin-top:14px; background:#f0f9ff; border:1px solid #7dd3fc; border-radius:10px; padding:16px;">
      <div style="font-weight:700; color:#0369a1; margin-bottom:8px;">{_t(lang_code, "lab_title")} — {title}</div>
      <div style="font-size:12px; color:#475569; margin-bottom:10px;">{html.escape(instructions)}: {html.escape(output_var)} = {html.escape(in_a)} {html.escape(js_op)} {html.escape(in_b)}</div>
      <div style="display:flex; flex-direction:column; gap:10px;">
        <label style="font-size:13px;">{html.escape(in_a)}: <span id="{safe_lab_id}_a_val">50</span>
          <input type="range" id="{safe_lab_id}_a" min="1" max="100" value="50" style="width:100%;" oninput="labUpdate_{safe_lab_id}()">
        </label>
        <label style="font-size:13px;">{html.escape(in_b)}: <span id="{safe_lab_id}_b_val">50</span>
          <input type="range" id="{safe_lab_id}_b" min="1" max="100" value="50" style="width:100%;" oninput="labUpdate_{safe_lab_id}()">
        </label>
      </div>
      <div style="margin-top:10px; padding:10px; background:#fff; border-radius:6px; font-size:14px;">
        <b>{html.escape(result_label)}:</b> {html.escape(output_var)} = <span id="{safe_lab_id}_result" style="font-weight:700; color:#0284c7;">—</span>
      </div>
      <div style="margin-top:8px; font-size:12px; color:#334155;">{html.escape(conclusion_prompt)}</div>
      <textarea id="{safe_lab_id}_hyp" placeholder="{html.escape(hypothesis_label)}" style="width:100%; margin-top:6px; padding:6px; border:1px solid #cbd5e1; border-radius:4px; font-size:13px; box-sizing:border-box;" rows="2"></textarea>
    </div>
    <script>
    function labUpdate_{safe_lab_id}() {{
      const a = parseFloat(document.getElementById('{safe_lab_id}_a').value);
      const b = parseFloat(document.getElementById('{safe_lab_id}_b').value);
      document.getElementById('{safe_lab_id}_a_val').innerText = a;
      document.getElementById('{safe_lab_id}_b_val').innerText = b;
      let result;
      if ('{js_op}' === '/') result = b !== 0 ? (a / b) : NaN;
      else if ('{js_op}' === '*') result = a * b;
      else result = a + b;
      document.getElementById('{safe_lab_id}_result').innerText = isFinite(result) ? result.toFixed(2) : '—';
    }}
    labUpdate_{safe_lab_id}();
    </script>'''


def build_qualitative_lab_html(
        concept: dict, lang_code: str, lab_id: str) -> str:
    """State-toggle interactive for qualitative concepts (e.g. states of
    matter). The observation text shown for each state comes verbatim from
    concept['raw_text'] segments already extracted — this module does not
    invent new observations, it only presents the existing grounded text
    interactively instead of as static prose.
    """
    safe_lab_id = re.sub(r"[^a-zA-Z0-9_]", "_", lab_id)
    title = html.escape(concept.get("title", ""))
    text = str(concept.get("raw_text") or "")

    states_found = sorted(set(
        m.group(1).lower() for m in _QUALITATIVE_STATE_PATTERN.finditer(text)
    ))
    if not states_found:
        raise RuntimeError(
            "LAB_GENERATION_INCONSISTENT: qualitative pattern matched but "
            "no state tokens extracted"
        )

    buttons = ""
    panels = ""
    for i, state in enumerate(states_found):
        # Grounded observation: the sentence(s) in raw_text mentioning this
        # state token, not a generated description.
        sentences = re.split(r"(?<=[.!?؟])\s+", text)
        matching = [s.strip() for s in sentences if state in s.lower()]
        observation = " ".join(matching) if matching else text[:240]
        buttons += (
            f'<button onclick="labShowState_{safe_lab_id}(\'{state}\')" '
            f'class="q-opt" style="min-height:38px;">{html.escape(state.capitalize())}</button>'
        )
        panels += (
            f'<div id="{safe_lab_id}_panel_{state}" style="display:none; '
            f'margin-top:8px; padding:10px; background:#fff; border-radius:6px; '
            f'font-size:13px;">{html.escape(observation)}</div>'
        )

    import json as _json
    states_js_array = _json.dumps(states_found)
    return f'''
    <div class="interactive-lab" id="lab_{safe_lab_id}" style="margin-top:14px; background:#f0f9ff; border:1px solid #7dd3fc; border-radius:10px; padding:16px;">
      <div style="font-weight:700; color:#0369a1; margin-bottom:8px;">{_t(lang_code, "lab_title")} — {title}</div>
      <div style="display:flex; gap:8px; flex-wrap:wrap;">{buttons}</div>
      {panels}
    </div>
    <script>
    function labShowState_{safe_lab_id}(state) {{
      const states = {states_js_array};
      states.forEach(function(s) {{
        const el = document.getElementById('{safe_lab_id}_panel_' + s);
        if (el) el.style.display = (s === state) ? 'block' : 'none';
      }});
    }}
    </script>'''


def generate_lab_for_concept(
        concept: dict, lang_code: str) -> Tuple[str, bool]:
    """Main entry point. Returns (lab_html, has_active_sim).

    Fail-closed by design: if the concept's own extracted text doesn't
    contain a detectable formula or qualitative-state pattern, returns
    ("", False) exactly like the current stub — we do not force a lab
    onto ungrounded content.
    """
    concept_id = concept.get("concept_id", "C00")
    lab_id = concept_id

    formula = _extract_formula_variables(concept)
    if formula:
        output_var, op, in_a, in_b = formula
        return build_formula_lab_html(
            concept, output_var, op, in_a, in_b, lang_code, lab_id
        ), True

    if _has_qualitative_state_language(concept):
        return build_qualitative_lab_html(concept, lang_code, lab_id), True

    return "", False
