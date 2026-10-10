"""NABIL assistant handoff. No paid model calls, no auto-publish.

The factory exports a source-grounded job; a connected ChatGPT Work task or
human reviewer may produce an answer file. That answer must be validated
before it enters the existing Golden publication gate.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

SCHEMA = "nabil.lesson.handoff.v1"
_REQUIRED = ("lesson_id", "book_id", "grade", "subject", "canonical_title",
             "pdf_start_page", "pdf_end_page")

def create_handoff(entry: dict, evidence_map: dict, destination: str) -> dict:
    missing = [key for key in _REQUIRED if key not in entry]
    if missing:
        raise ValueError("HANDOFF_ENTRY_MISSING: " + ",".join(missing))
    evidence = {
        "source_pages": evidence_map.get("source_pages") or [],
        "concept_evidence": evidence_map.get("concept_evidence") or [],
        "exercise_evidence": evidence_map.get("exercise_evidence") or [],
        "title_verification": evidence_map.get("title_verification") or {},
        "source_completeness": evidence_map.get("source_completeness") or {},
    }
    core = {
        "schema": SCHEMA,
        "lesson_id": entry["lesson_id"], "book_id": entry["book_id"],
        "grade": entry["grade"], "subject": entry["subject"],
        "language": entry.get("language", "en"),
        "canonical_title": entry["canonical_title"],
        "source_pages": [entry["pdf_start_page"], entry["pdf_end_page"]],
        "source_evidence": evidence,
        "task": {
            "teacher": "Create progressive NABIL teaching steps from the evidence only.",
            "exercise": "Solve every evidenced textbook exercise; cite the book page.",
            "constraints": [
                "Do not invent sources, figures, diagrams or verified solutions.",
                "Keep mathematical expressions invariant and independently check them.",
                "Return unresolved questions as unresolved, not guessed answers.",
                "No Arabic translation is required.",
                "Return teaching_steps and exercise_solutions, keyed by evidence IDs."
            ]
        },
    }
    payload = json.dumps(core, sort_keys=True, ensure_ascii=False, default=str)
    core["input_sha256"] = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    p = Path(destination)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(core, ensure_ascii=False, indent=2, default=str),
                 encoding="utf-8")
    return core

def verify_return(job: dict, result: dict) -> dict:
    """Structural verification only; scientific review is still mandatory."""
    if result.get("schema") != "nabil.lesson.answer.v1":
        raise ValueError("HANDOFF_ANSWER_SCHEMA_MISMATCH")
    if result.get("lesson_id") != job.get("lesson_id"):
        raise ValueError("HANDOFF_ANSWER_LESSON_MISMATCH")
    if result.get("input_sha256") != job.get("input_sha256"):
        raise ValueError("HANDOFF_ANSWER_STALE_SOURCE")
    steps = result.get("teaching_steps")
    solutions = result.get("exercise_solutions")
    if not isinstance(steps, list) or not isinstance(solutions, list):
        raise ValueError("HANDOFF_ANSWER_MISSING_CONTENT")
    if result.get("scientific_review") == "PASS":
        raise ValueError("SELF_DECLARED_SCIENTIFIC_REVIEW_NOT_ACCEPTED")
    return {
        "lesson_id": job["lesson_id"], "status": "PENDING_INDEPENDENT_REVIEW",
        "teaching_steps": steps, "exercise_solutions": solutions,
    }
