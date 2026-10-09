#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fail-closed curriculum coverage contract for NABIL scientific laboratories.

This module does not invent experiments. It verifies that every concept in the
target science/mathematics curriculum has an evidence-locked interactive
activity after Requirement-5 has passed.

Coverage target:
- Grades 1..12
- mathematics, physics, chemistry, biology, general_science

A rich simulation is preferred when source evidence supports it. When it does
not, EVIDENCE_SEQUENCE / EVIDENCE_REVEAL remain valid interactive applications
because they expose only verified source evidence and never fabricate science.
"""
from __future__ import annotations

import re
from typing import Any, Dict, Iterable

COVERAGE_VERSION = "NABIL_SCI_LAB_COVERAGE_V1"
TARGET_GRADES = tuple(range(1, 13))
TARGET_SUBJECTS = {
    "mathematics", "physics", "chemistry", "biology", "general_science",
}

_SUBJECT_ALIASES = {
    "math": "mathematics", "maths": "mathematics",
    "mathematics": "mathematics", "mathématiques": "mathematics",
    "رياضيات": "mathematics",
    "physics": "physics", "physique": "physics", "فيزياء": "physics",
    "chemistry": "chemistry", "chimie": "chemistry", "كيمياء": "chemistry",
    "biology": "biology", "biologie": "biology", "أحياء": "biology",
    "science": "general_science", "sciences": "general_science",
    "general science": "general_science", "general_science": "general_science",
    "علوم": "general_science",
}

RICH_SCIENCE_KINDS = {
    "ORIENTATION_INVARIANT", "SHAPE_RESPONSE", "DC_SERIES_CIRCUIT",
    "OPTICS_REFLECTION", "IONIC_COMPOUND",
}
MATH_APPLICATION_KINDS = {"FORMULA_CALCULATOR", "GEOMETRY_PROOF"}
EVIDENCE_ACTIVITY_KINDS = {"EVIDENCE_SEQUENCE", "EVIDENCE_REVEAL"}
ALL_ACCEPTED_KINDS = RICH_SCIENCE_KINDS | MATH_APPLICATION_KINDS | EVIDENCE_ACTIVITY_KINDS


def normalize_subject(value: Any) -> str:
    raw = re.sub(r"\s+", " ", str(value or "")).strip()
    return _SUBJECT_ALIASES.get(raw.casefold(), raw.casefold().replace(" ", "_"))


def normalize_grade(value: Any) -> int:
    raw = str(value or "").strip()
    m = re.search(r"(\d{1,2})", raw)
    if not m:
        raise RuntimeError(f"SCI_LAB_GRADE_INVALID:{raw}")
    grade = int(m.group(1))
    if grade not in TARGET_GRADES:
        raise RuntimeError(f"SCI_LAB_GRADE_OUT_OF_RANGE:{grade}")
    return grade


def expected_level(grade: int) -> str:
    if grade <= 3:
        return "L1"
    if grade <= 9:
        return "L2"
    return "L3"


def lab_activity_class(subject: str, kind: str) -> str:
    subject = normalize_subject(subject)
    kind = str(kind or "").strip().upper()
    if subject == "mathematics":
        if kind in MATH_APPLICATION_KINDS:
            return "mathematical_application"
        if kind in EVIDENCE_ACTIVITY_KINDS:
            return "mathematical_evidence_exploration"
        return "mathematical_simulation"
    if kind in RICH_SCIENCE_KINDS:
        return "scientific_simulation"
    if kind == "EVIDENCE_SEQUENCE":
        return "scientific_process_exploration"
    if kind == "EVIDENCE_REVEAL":
        return "scientific_evidence_exploration"
    if kind in MATH_APPLICATION_KINDS:
        return "scientific_quantitative_application"
    return "interactive_application"


def is_target(subject: Any, grade: Any) -> bool:
    try:
        return normalize_subject(subject) in TARGET_SUBJECTS and normalize_grade(grade) in TARGET_GRADES
    except RuntimeError:
        return False


def validate_and_annotate_curriculum_lab(
    spec: Dict[str, Any], *, entry: Dict[str, Any],
    profile: Dict[str, Any], concept: Dict[str, Any],
) -> Dict[str, Any]:
    subject = normalize_subject(profile.get("subject") or entry.get("subject"))
    grade = normalize_grade(profile.get("grade") or entry.get("grade"))

    if subject not in TARGET_SUBJECTS:
        return spec

    if not isinstance(spec, dict) or spec.get("supported") is not True:
        raise RuntimeError(
            f"SCI_LAB_COVERAGE_MISSING:{subject}:G{grade}:{concept.get('concept_id')}"
        )

    cert = spec.get("_requirement5") or {}
    if cert.get("passed") is not True or cert.get("source_locked") is not True:
        raise RuntimeError(
            f"SCI_LAB_R5_REQUIRED:{subject}:G{grade}:{concept.get('concept_id')}"
        )

    kind = str(spec.get("kind") or "").strip().upper()
    if kind not in ALL_ACCEPTED_KINDS:
        raise RuntimeError(f"SCI_LAB_KIND_NOT_COVERED:{subject}:G{grade}:{kind}")

    basis = str(spec.get("evidence_basis") or "").strip().lower()
    if basis not in {"text", "figure"}:
        raise RuntimeError("SCI_LAB_EVIDENCE_BASIS_REQUIRED")
    if basis == "text" and not str(spec.get("evidence_quote") or "").strip():
        raise RuntimeError("SCI_LAB_TEXT_EVIDENCE_REQUIRED")

    teacher = spec.get("teacher_script")
    if not isinstance(teacher, list) or not 2 <= len(teacher) <= 12:
        raise RuntimeError("SCI_LAB_TEACHER_SCRIPT_REQUIRED")
    for i, step in enumerate(teacher):
        if not isinstance(step, dict):
            raise RuntimeError(f"SCI_LAB_TEACHER_STEP_INVALID:{i}")
        if not isinstance(step.get("scientific_constraints"), list):
            raise RuntimeError(f"SCI_LAB_CONSTRAINTS_REQUIRED:{i}")
        if not str(step.get("evidence_quote") or "").strip():
            raise RuntimeError(f"SCI_LAB_STEP_EVIDENCE_REQUIRED:{i}")

    level = str(profile.get("level") or expected_level(grade))
    expected = expected_level(grade)
    # Preserve the factory's explicit pedagogical level if it has a documented
    # different mapping, but record both values for audit.
    coverage = {
        "version": COVERAGE_VERSION,
        "passed": True,
        "grade": grade,
        "subject": subject,
        "factory_level": level,
        "expected_age_band": expected,
        "activity_class": lab_activity_class(subject, kind),
        "kind": kind,
        "source_locked": True,
        "requirement5_passed": True,
        "teacher_led": True,
        "interactive": True,
        "no_fabricated_science": True,
        "concept_id": str(concept.get("concept_id") or ""),
        "source_page": concept.get("source_page"),
    }
    spec["_curriculum_scientific_lab"] = coverage
    return spec


def validate_lesson_scientific_lab_coverage(
    profile: Dict[str, Any], activities: Iterable[Dict[str, Any]],
) -> Dict[str, Any]:
    subject = normalize_subject(profile.get("subject"))
    grade = normalize_grade(profile.get("grade"))
    if subject not in TARGET_SUBJECTS:
        return {
            "version": COVERAGE_VERSION,
            "required": False,
            "passed": True,
            "grade": grade,
            "subject": subject,
        }

    rows = list(activities or [])
    if not rows:
        raise RuntimeError(f"SCI_LAB_LESSON_HAS_NO_CONCEPTS:{subject}:G{grade}")

    missing = []
    rich = 0
    classes: Dict[str, int] = {}
    for row in rows:
        cid = str(row.get("concept_id") or "")
        spec = row.get("lab_spec")
        cert = (spec or {}).get("_curriculum_scientific_lab") if isinstance(spec, dict) else None
        if not isinstance(cert, dict) or cert.get("passed") is not True:
            missing.append(cid or "?")
            continue
        cls = str(cert.get("activity_class") or "")
        classes[cls] = classes.get(cls, 0) + 1
        if str(cert.get("kind") or "") in RICH_SCIENCE_KINDS | MATH_APPLICATION_KINDS:
            rich += 1

    if missing:
        raise RuntimeError(
            "SCI_LAB_LESSON_COVERAGE_FAILED:" + ",".join(missing)
        )

    return {
        "version": COVERAGE_VERSION,
        "required": True,
        "passed": True,
        "grade": grade,
        "subject": subject,
        "concept_count": len(rows),
        "covered_concepts": len(rows),
        "rich_or_domain_specific_count": rich,
        "activity_classes": classes,
        "fallback_allowed_only_when_source_locked": True,
        "grades_contract": list(TARGET_GRADES),
        "subjects_contract": sorted(TARGET_SUBJECTS),
    }


def curriculum_matrix() -> list[dict[str, Any]]:
    return [
        {
            "grade": grade,
            "subject": subject,
            "required": True,
            "expected_age_band": expected_level(grade),
        }
        for grade in TARGET_GRADES
        for subject in sorted(TARGET_SUBJECTS)
    ]
