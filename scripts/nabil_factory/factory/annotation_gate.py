"""Annotation gate (NABIL rules LL-05, LL-12, LL-13).

Every scene whose narration states a geometric property (equal segments, equal angles, right angle, parallel,
congruence) must SHOW that property on the figure: the hand points at it and the mark is drawn while the sentence
is spoken. This gate is a static check over a lesson's scene data (`nabilV6Data`). It fails closed on scenes that
state a property with no figure at all, and reports scenes whose figure marks cannot be inspected as UNVERIFIED.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List

_SEG = r"[A-Z]{2}"
_CLAIM = re.compile(
    rf"(\b{_SEG}\s*=\s*{_SEG}\b)"            # AB = CD
    r"|(∠\s*[A-Z]{1,3}\s*=\s*∠?\s*[A-Z0-9]{1,3})"  # ∠B = ∠N
    r"|(⟂)|(∥)|(≅)"                            # perpendicular, parallel, congruent
    r"|(زاوية\s+قائمة)|(متساوي(?:ان|ة)?\s+(?:الأضلاع|الساقين|الزاويتين|الضلعين))|(متوازي|عمودي)"
    r"|(?i:\b(?:right angle|equal sides|equal angles|parallel|perpendicular|congruent)\b)"
    r"|(?i:\b(?:angle droit|côtés égaux|angles égaux|parallèles?|perpendiculaires?|congrus?)\b)"
)
_ANNOTATE = ("annotate",)


def property_claims(text: str) -> int:
    return len(_CLAIM.findall(str(text or "")))


def _args_have_marks(args: Any) -> bool:
    if not isinstance(args, dict):
        return False
    return bool(args.get("items") or args.get("marks") or args.get("segments"))


def audit_scene(scene: Dict[str, Any]) -> Dict[str, Any]:
    steps = [s for s in scene.get("steps", []) if isinstance(s, dict)]
    claims = sum(property_claims(s.get("text", "")) for s in steps if s.get("t") in ("text", "formula"))
    draws = [s for s in steps if s.get("t") == "draw"]
    annotated = [s for s in draws if s.get("draw") in _ANNOTATE or _args_have_marks(s.get("args"))]
    if not claims:
        status = "NOT_APPLICABLE"
    elif not draws:
        status = "FAIL_NO_FIGURE"
    elif annotated:
        status = "PASS_MARKED"
    else:
        status = "UNVERIFIED_PREBAKED_DRAW"
    return {"scene": scene.get("id") or scene.get("title"), "claims": claims, "draws": len(draws),
            "annotated_draws": len(annotated), "status": status}


def audit_lesson(data: Dict[str, Any]) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = [audit_scene(sc) for sc in data.get("scenes", []) if isinstance(sc, dict)]
    count = lambda k: sum(1 for r in rows if r["status"] == k)
    return {"scenes": len(rows), "applicable": sum(1 for r in rows if r["status"] != "NOT_APPLICABLE"),
            "fail_no_figure": count("FAIL_NO_FIGURE"), "unverified_prebaked": count("UNVERIFIED_PREBAKED_DRAW"),
            "pass_marked": count("PASS_MARKED"),
            "verdict": "FAIL" if count("FAIL_NO_FIGURE") else ("UNVERIFIED" if count("UNVERIFIED_PREBAKED_DRAW") else "PASS"),
            "failing_scenes": [r["scene"] for r in rows if r["status"] == "FAIL_NO_FIGURE"]}
