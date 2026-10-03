#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NABIL AI Requirement 5 gate.

Fail-closed acceptance for published interactive labs. A lab may be impressive,
but every scientific claim/state/action must remain locked to verified lesson
evidence. Visual choreography (pointer, focus, justified motion, explanation,
conclusion) is required without allowing decoration to create science.
"""
from __future__ import annotations

import re
from typing import Any, Dict

R5_VERSION = "NABIL_REQUIREMENT5_V1"
REFERENCE_RENDERER_CONTRACT = "NABIL_REFERENCE_RENDERER_V1"


def _norm(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip().casefold()


def validate_requirement5_lab(
    spec: Dict[str, Any], *, source_text: str,
    source_figure_verified: bool = False,
) -> Dict[str, Any]:
    if not isinstance(spec, dict) or spec.get("supported") is not True:
        raise RuntimeError("R5_LAB_NOT_SUPPORTED")

    source = _norm(source_text)
    if not source and not source_figure_verified:
        raise RuntimeError("R5_NO_VERIFIED_SOURCE")

    kind = str(spec.get("kind") or "").strip().upper()
    basis = str(spec.get("evidence_basis") or "text").strip().lower()
    if basis == "figure":
        if not source_figure_verified:
            raise RuntimeError("R5_UNVERIFIED_FIGURE_EVIDENCE")
    elif basis == "text":
        quote = _norm(spec.get("evidence_quote"))
        if not quote:
            raise RuntimeError("R5_MAIN_EVIDENCE_QUOTE_REQUIRED")
        if quote not in source:
            raise RuntimeError("R5_MAIN_EVIDENCE_OUTSIDE_LESSON")
    else:
        raise RuntimeError("R5_INVALID_EVIDENCE_BASIS")

    teacher = spec.get("teacher_script")
    if not isinstance(teacher, list) or not 2 <= len(teacher) <= 12:
        raise RuntimeError("R5_TEACHER_SCRIPT_REQUIRED")

    allowed = {"point", "highlight", "set_state", "animate", "observe", "explain", "conclude"}
    actions = []
    for i, step in enumerate(teacher):
        if not isinstance(step, dict):
            raise RuntimeError(f"R5_STEP_INVALID:{i}")
        if not str(step.get("say") or "").strip():
            raise RuntimeError(f"R5_STEP_SPEECH_REQUIRED:{i}")
        action = str(step.get("action") or "").strip()
        if action not in allowed:
            raise RuntimeError(f"R5_STEP_ACTION_NOT_ALLOWED:{i}:{action}")
        targets = step.get("target_ids")
        if not isinstance(targets, list) or not targets or any(not str(x or "").strip() for x in targets):
            raise RuntimeError(f"R5_STEP_TARGET_REQUIRED:{i}")
        before, after = step.get("state_before"), step.get("state_after")
        if not isinstance(before, dict) or not isinstance(after, dict):
            raise RuntimeError(f"R5_STEP_STATE_REQUIRED:{i}")
        constraints = step.get("scientific_constraints")
        if not isinstance(constraints, list) or not constraints:
            raise RuntimeError(f"R5_SCIENTIFIC_CONSTRAINTS_REQUIRED:{i}")
        quote = _norm(step.get("evidence_quote"))
        if basis == "text" and (not quote or quote not in source):
            raise RuntimeError(f"R5_STEP_OUTSIDE_LESSON:{i}")
        if basis == "figure" and not source_figure_verified:
            raise RuntimeError(f"R5_STEP_UNVERIFIED_FIGURE:{i}")
        if action in {"animate", "set_state"}:
            changed = {k for k in set(before) | set(after) if before.get(k) != after.get(k)}
            if changed and basis == "text" and quote not in source:
                raise RuntimeError(f"R5_ANIMATION_WITHOUT_EVIDENCE:{i}")
        actions.append(action)

    # Every advanced declared invariant/claim must have its own source quote.
    quotes = spec.get("evidence_quotes")
    if quotes is not None:
        if not isinstance(quotes, dict):
            raise RuntimeError("R5_EVIDENCE_QUOTES_INVALID")
        for claim, raw in quotes.items():
            quote = _norm(raw)
            if not quote:
                raise RuntimeError(f"R5_EMPTY_CLAIM_EVIDENCE:{claim}")
            if basis == "text" and quote not in source:
                raise RuntimeError(f"R5_CLAIM_OUTSIDE_LESSON:{claim}")

    # Universal evidence fallback must never masquerade as a richer simulation.
    if kind == "EVIDENCE_REVEAL":
        items = spec.get("items")
        if not isinstance(items, list) or not items:
            raise RuntimeError("R5_EVIDENCE_REVEAL_ITEMS_REQUIRED")
        for i, item in enumerate(items):
            quote = _norm((item or {}).get("evidence_quote"))
            if not quote or quote not in source:
                raise RuntimeError(f"R5_REVEAL_ITEM_OUTSIDE_SOURCE:{i}")
        forbidden = {"formula", "rules", "cation", "anion", "proof_steps", "resistors"}
        leaked = forbidden.intersection(spec)
        if leaked:
            raise RuntimeError("R5_FALLBACK_PRETENDING_RICH:" + ",".join(sorted(leaked)))

    # Reference choreography: pointer -> focus -> evidence-backed change when meaningful
    # -> explanation/observation -> conclusion.
    if "point" not in actions:
        raise RuntimeError("R5_REFERENCE_POINTER_MISSING")
    if "highlight" not in actions:
        raise RuntimeError("R5_REFERENCE_HIGHLIGHT_MISSING")
    if not ({"observe", "explain"} & set(actions)):
        raise RuntimeError("R5_REFERENCE_EXPLANATION_MISSING")
    if "conclude" not in actions:
        raise RuntimeError("R5_REFERENCE_CONCLUSION_MISSING")

    motion_required = {
        "FORMULA_CALCULATOR", "ORIENTATION_INVARIANT", "SHAPE_RESPONSE",
        "DC_SERIES_CIRCUIT", "OPTICS_REFLECTION", "IONIC_COMPOUND",
        "GEOMETRY_PROOF", "EVIDENCE_SEQUENCE",
    }
    if kind in motion_required and not ({"animate", "set_state"} & set(actions)):
        raise RuntimeError("R5_REFERENCE_ANIMATION_MISSING")

    visual = spec.setdefault("visual_contract", {})
    visual.update({
        "renderer_contract": REFERENCE_RENDERER_CONTRACT,
        "dark_stage": True,
        "cyan_focus": True,
        "teacher_pointer": True,
        "target_glow": True,
        "animated_transition": kind in motion_required,
        "mobile_safe": True,
        "preserve_scientific_colors": True,
        "decorative_animation_may_not_change_science": True,
    })

    spec["_requirement5"] = {
        "version": R5_VERSION,
        "passed": True,
        "source_locked": True,
        "scientific_fidelity": True,
        "no_invented_lab": True,
        "no_invented_science": True,
        "teacher_pointer": True,
        "target_highlight": True,
        "animation_evidence_locked": True,
        "explanation_present": True,
        "conclusion_present": True,
        "reference_visual_contract": REFERENCE_RENDERER_CONTRACT,
    }
    return spec


def assert_requirement5_publishable(spec: Dict[str, Any], *, lesson_id: str = "", lab_id: str = "") -> None:
    cert = (spec or {}).get("_requirement5") or {}
    required = (
        "source_locked", "scientific_fidelity", "no_invented_lab", "no_invented_science",
        "teacher_pointer", "target_highlight", "animation_evidence_locked",
        "explanation_present", "conclusion_present",
    )
    if cert.get("passed") is not True or cert.get("version") != R5_VERSION:
        raise RuntimeError(f"R5_PUBLISH_BLOCKED:{lesson_id}:{lab_id}")
    missing = [key for key in required if cert.get(key) is not True]
    if missing:
        raise RuntimeError("R5_PUBLISH_BLOCKED_MISSING:" + ",".join(missing))
