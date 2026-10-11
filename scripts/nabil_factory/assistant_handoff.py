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
        "source_pages": evidence_map.get("source_pages") or evidence_map.get("pages_evidence") or [],
        "concept_evidence": evidence_map.get("concept_evidence") or evidence_map.get("concepts") or [],
        "exercise_evidence": evidence_map.get("exercise_evidence") or [],
        "title_verification": evidence_map.get("title_verification") or {},
        "source_completeness": evidence_map.get("source_completeness") or {},
        "source_backlog": evidence_map.get("source_backlog") or {},
    }
    core = {
        "schema": SCHEMA,
        "lesson_id": entry["lesson_id"], "book_id": entry["book_id"],
        "grade": entry["grade"], "subject": entry["subject"],
        "language": entry.get("language", "en"),
        "canonical_title": entry["canonical_title"],
        "source_pages": [entry["pdf_start_page"], entry["pdf_end_page"]],
        "source_pdf_sha256": entry.get("source_pdf_sha256") or entry.get("source_book_sha256"),
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
    expected_concepts = {
        str(item.get("concept_id") or item.get("id") or "").strip()
        for item in job.get("source_evidence", {}).get("concept_evidence", [])
    }
    expected_concepts.discard("")
    expected_exercises = {
        str(item.get("exercise_id") or item.get("id") or "").strip()
        for item in job.get("source_evidence", {}).get("exercise_evidence", [])
    }
    expected_exercises.discard("")

    def _require_exact_ids(items: list, key: str, expected: set, kind: str) -> None:
        actual = [str(item.get(key) or "").strip()
                  for item in items if isinstance(item, dict)]
        if len(actual) != len(items) or any(not value for value in actual):
            raise ValueError(f"HANDOFF_ANSWER_{kind}_ID_MISSING")
        if len(actual) != len(set(actual)):
            raise ValueError(f"HANDOFF_ANSWER_{kind}_ID_DUPLICATE")
        missing = sorted(expected - set(actual))
        unknown = sorted(set(actual) - expected)
        if missing or unknown:
            raise ValueError(
                f"HANDOFF_ANSWER_{kind}_COVERAGE_MISMATCH:"
                + json.dumps({"missing": missing, "unknown": unknown},
                             ensure_ascii=False, sort_keys=True))

    _require_exact_ids(steps, "concept_id", expected_concepts, "CONCEPT")
    _require_exact_ids(solutions, "exercise_id", expected_exercises, "EXERCISE")
    for step in steps:
        if not str(step.get("text") or step.get("conclusion") or "").strip():
            raise ValueError("HANDOFF_ANSWER_EMPTY_TEACHING_STEP")
    for solution in solutions:
        if (not isinstance(solution.get("steps"), list)
                or not solution.get("steps")
                or not str(solution.get("final_answer") or "").strip()):
            raise ValueError("HANDOFF_ANSWER_INCOMPLETE_EXERCISE_SOLUTION")
    if result.get("scientific_review") == "PASS":
        raise ValueError("SELF_DECLARED_SCIENTIFIC_REVIEW_NOT_ACCEPTED")
    return {
        "lesson_id": job["lesson_id"], "status": "PENDING_INDEPENDENT_REVIEW",
        "input_sha256": job["input_sha256"],
        "concept_count": len(steps),
        "exercise_count": len(solutions),
        "teaching_steps": steps, "exercise_solutions": solutions,
    }
