"""PEDAGOGICAL_GOLDEN_GATE - an independent teaching-quality gate.

The technical gates answer "does the page work?". This one answers "does it
teach?". It never inspects only that an HTML element or button exists: it reads
the actual teaching text, the actual lab kinds and the actual worked solutions,
and (in the browser step) the actual rendered text on a phone viewport.

Rejection reasons (all raise PedagogicalGateFailed, prefix
``PEDAGOGICAL_GOLDEN_GATE_FAILED``):
  GENERIC_OR_REPEATED_EXPLANATION  filler phrases / the same opening repeated
  LAB_TEXT_REVEAL_INSTEAD_OF_INTERACTION  mathematics ideas whose "lab" only
                                   re-displays text
  SOLUTION_STEPS_NOT_EXPLAINED     worked solutions without Rule + Calculation
  DISTORTED_MATH                   raw ^ / * / ^( ) left in student-facing data
  RENDERED_RAW_MATH / CONTROLS_BROKEN  (browser step) raw symbols on screen,
                                   play/pause not working on a phone viewport
  INDEPENDENT_SCIENTIFIC_REVIEW_MISSING  lesson not independently reviewed
Source fidelity is enforced by the existing SOURCE_* and evidence gates.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from typing import Any, Dict, Iterable, List

PREFIX = "PEDAGOGICAL_GOLDEN_GATE_FAILED"
EVIDENCE_ONLY_KINDS = {"EVIDENCE_REVEAL", "EVIDENCE_SEQUENCE"}
MATH_SCIENCE_LAB_REQUIRED = {"mathematics"}

FILLER_RE = re.compile(
    r"we now explain|let us begin and explain|we conclude from the steps above|"
    r"read the question and identify what is required|"
    r"expliquons maintenant l.étape|commençons et expliquons la première|"
    r"nous concluons des étapes précédentes|lisons la question et identifions|"
    r"ننتقل الآن إلى الخطوة التالية|نبدأ الحلّ خطوةً خطوة|نقرأ نصّ السؤال ونحدّد|"
    r"نستنتج من الخطوات السابقة", re.I)

# step tags a worked solution may start with (en / fr / ar)
_TAGS = {
    "given": r"given|données?|donnée|المعطيات|المعطى",
    "required": r"required|to find|demandé|à trouver|المطلوب",
    "rule": r"rule|property|théorème|propriété|règle|القاعدة|الخاصية|القانون",
    "substitution": r"substitution|substitue|remplacement|التعويض",
    "calculation": r"calculation|calcul|الحساب",
    "verification": r"verification|vérification|التحقق",
}
TAG_RE = re.compile(
    r"^\s*(?:[a-z]\)\s*)?(" + "|".join(f"(?P<{k}>{v})" for k, v in _TAGS.items()) + r")\s*[:：]",
    re.I)


class PedagogicalGateFailed(AssertionError):
    pass


def _fail(reason: str, detail: str = "") -> None:
    raise PedagogicalGateFailed(f"{PREFIX}: {reason} -> {detail[:600]}")


def solution_tags(step: str) -> str:
    m = TAG_RE.match(str(step or ""))
    if not m:
        return ""
    for key in _TAGS:
        if m.group(key):
            return key
    return ""


def _sentences(candidate: dict) -> Dict[str, List[str]]:
    groups: Dict[str, List[str]] = {}
    for act in (candidate.get("theory") or {}).get("activities", []) or []:
        groups[f"idea:{act.get('concept_id')}"] = [
            str(s.get("sentence") or "").strip()
            for s in act.get("teaching_steps") or [] if isinstance(s, dict)]
    for ex in candidate.get("exercises") or []:
        sol = ex.get("_pre_solved_solution")
        if isinstance(sol, dict):
            groups[f"exercise:{ex.get('number')}"] = [str(x) for x in sol.get("steps") or []]
    return groups


def check_explanations(candidate: dict) -> Dict[str, Any]:
    groups = _sentences(candidate)
    total = 0
    for name, lines in groups.items():
        openings: Counter = Counter()
        for line in lines:
            if not line:
                continue
            total += 1
            if FILLER_RE.search(line):
                _fail("GENERIC_OR_REPEATED_EXPLANATION", f"{name}: filler phrase in {line[:120]!r}")
            openings[" ".join(re.findall(r"\w+", line.casefold())[:4])] += 1
        for opening, n in openings.items():
            if opening and n >= 3 and len(opening.split()) >= 3:
                _fail("GENERIC_OR_REPEATED_EXPLANATION",
                      f"{name}: {n} steps open with {opening!r}")
    if total == 0:
        _fail("GENERIC_OR_REPEATED_EXPLANATION", "no teaching text at all")
    return {"checked_sentences": total}


def check_labs(candidate: dict, subject: str) -> Dict[str, Any]:
    acts = (candidate.get("theory") or {}).get("activities", []) or []
    kinds = [str((a.get("lab_spec") or {}).get("kind") or "").upper() for a in acts]
    if subject.strip().lower() in MATH_SCIENCE_LAB_REQUIRED and kinds:
        reveal = sum(1 for k in kinds if k in EVIDENCE_ONLY_KINDS)
        if reveal / len(kinds) > 0.5:
            _fail("LAB_TEXT_REVEAL_INSTEAD_OF_INTERACTION",
                  f"{reveal}/{len(kinds)} mathematics ideas only re-display text: {kinds}")
    return {"lab_kinds": dict(Counter(kinds))}


def check_solutions(candidate: dict, subject: str) -> Dict[str, Any]:
    if subject.strip().lower() not in MATH_SCIENCE_LAB_REQUIRED:
        return {"checked": 0}
    sols = [e["_pre_solved_solution"] for e in candidate.get("exercises") or []
            if isinstance(e.get("_pre_solved_solution"), dict)]
    if not sols:
        return {"checked": 0}
    explained = 0
    for sol in sols:
        tags = {solution_tags(s) for s in sol.get("steps") or []}
        if "rule" in tags and "calculation" in tags and len(sol.get("steps") or []) >= 3:
            explained += 1
    if explained / len(sols) < 0.7:
        _fail("SOLUTION_STEPS_NOT_EXPLAINED",
              f"only {explained}/{len(sols)} solutions state the rule and the calculation as separate steps")
    return {"checked": len(sols), "explained": explained}


_RAW = re.compile(r"\^(?!\{)|\^\{[^}]*\([^)]*$|(?<=[\w)}\]])\s\*\s(?=[\w({\[])")


def _strings(obj: Any) -> Iterable[str]:
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("srcdoc", "avatar_base64"):
                continue
            yield from _strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _strings(v)


def check_math_data(page_html: str) -> Dict[str, Any]:
    m = re.search(r'<script type="application/json" id="(?:nabilV18Data|nabilV6Data)">(.*?)</script>', page_html, re.S)
    if not m:
        return {"checked": 0}
    data = json.loads(m.group(1).replace("<\\!--", "<!--").replace("<\\u0021--", "<!--"))
    bad = [s for s in _strings({"slides": data.get("slides"), "scenes": data.get("scenes"), "golden": data.get("golden")}) if _RAW.search(s)]
    if bad:
        _fail("DISTORTED_MATH", f"{len(bad)} strings keep raw ^ or *: {bad[0][:140]!r}")
    return {"checked_strings": sum(1 for _ in _strings(data.get("slides")))}


def check_independent_review(candidate: dict) -> Dict[str, Any]:
    if str(candidate.get("review_status") or "") != "REVIEWED":
        _fail("INDEPENDENT_SCIENTIFIC_REVIEW_MISSING",
              f"review_status={candidate.get('review_status')!r}")
    return {"review_status": "REVIEWED"}


def run_static_gate(candidate: dict, subject: str) -> Dict[str, Any]:
    """Everything decidable from the candidate data. Raises on the first failure."""
    report = {
        "explanations": check_explanations(candidate),
        "labs": check_labs(candidate, subject),
        "solutions": check_solutions(candidate, subject),
        "math_data": {"page_a": check_math_data(str(candidate.get("page_a_html") or "")),
                      "page_b": check_math_data(str(candidate.get("page_b_html") or ""))},
    }
    return report


BROWSER_JS_PLAY = """async () => {
  const O = window.NABILWholeLessonOrchestrator;
  if (!O) return {error: 'NO_ORCHESTRATOR'};
  O.play();
  const t0 = Date.now();
  while (!O.state().final && Date.now() - t0 < 60000) await new Promise(r => setTimeout(r, 50));
  const root = document.getElementById('nabilWholeLessonSmartLab');
  const vis = [...root.querySelectorAll('*')].filter(e => e.checkVisibility && e.checkVisibility() && !e.closest('script,style'));
  const txt = vis.map(e => [...e.childNodes].filter(n => n.nodeType === 3).map(n => n.nodeValue).join('')).join(' ');
  return {final: O.state().final, raw: /[\\^*]/.test(txt), sample: (txt.match(/.{0,30}[\\^*].{0,30}/) || [''])[0],
          sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth};
}"""

BROWSER_JS_CONTROLS = """async () => {
  const O = window.NABILWholeLessonOrchestrator;
  const play = document.getElementById('nabilWholePlay');
  play.click();
  await new Promise(r => setTimeout(r, 600));
  const playing = !O.state().paused;
  play.click();
  const paused = O.state().paused === true;
  play.click();
  const resumed = O.state().paused === false;
  const vis = [...document.querySelectorAll('#nabilWholeLessonSmartLab button')].filter(b => b.checkVisibility && b.checkVisibility()).length;
  O.stop();
  return {playing, paused, resumed, visible_buttons: vis};
}"""


def run_browser_gate(html_path: str, label: str) -> Dict[str, Any]:
    """Real Chromium at 390x844: whole lesson plays to the end with no raw math on
    screen, and play/pause/resume genuinely work."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            errs: List[str] = []
            page = browser.new_page(viewport={"width": 390, "height": 844})
            page.on("pageerror", lambda e: errs.append(str(e)))
            page.goto(f"file://{html_path}", wait_until="domcontentloaded")
            page.wait_for_function("!!window.NABILWholeLessonOrchestrator", timeout=20000)
            controls = page.evaluate(BROWSER_JS_CONTROLS)
            page.close()
            # second page: FAST flag must exist BEFORE the board script runs
            page2 = browser.new_page(viewport={"width": 390, "height": 844})
            page2.on("pageerror", lambda e: errs.append(str(e)))
            page2.add_init_script("window.NABIL_V18_FAST=true")
            page2.goto(f"file://{html_path}", wait_until="domcontentloaded")
            page2.wait_for_function("!!window.NABILWholeLessonOrchestrator", timeout=20000)
            played = page2.evaluate(BROWSER_JS_PLAY)
        finally:
            browser.close()
    if errs:
        _fail("CONTROLS_BROKEN", f"{label}: page errors {errs[:3]}")
    if played.get("error") or not played.get("final"):
        _fail("CONTROLS_BROKEN", f"{label}: lesson did not reach its final stage: {played}")
    if played.get("raw"):
        _fail("RENDERED_RAW_MATH", f"{label}: raw ^ or * visible on screen near {played.get('sample')!r}")
    if played.get("sw", 0) > played.get("cw", 0):
        _fail("CONTROLS_BROKEN", f"{label}: horizontal scroll on phone {played}")
    if not (controls.get("playing") and controls.get("paused") and controls.get("resumed")):
        _fail("CONTROLS_BROKEN", f"{label}: play/pause/resume not working {controls}")
    return {"controls": controls, "played": played}
