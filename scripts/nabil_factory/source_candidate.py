"""Strict import of a visually audited source candidate into factory evidence.

This repairs extraction inventory only.  It never grants scientific review or
publication approval, and every imported exercise retains that pending state.
"""
from __future__ import annotations

import copy


def apply_source_candidate(entry: dict, evidence_map: dict, candidate: dict) -> dict:
    if candidate.get("schema") != "nabil.lesson.handoff.v2":
        raise ValueError("SOURCE_CANDIDATE_SCHEMA_MISMATCH")
    if candidate.get("lesson_id") != entry.get("lesson_id"):
        raise ValueError("SOURCE_CANDIDATE_LESSON_MISMATCH")
    if candidate.get("book_id") != entry.get("book_id"):
        raise ValueError("SOURCE_CANDIDATE_BOOK_MISMATCH")
    expected_pdf = (
        entry.get("source_pdf_sha256")
        or entry.get("source_book_sha256")
    )
    if not expected_pdf or candidate.get("source_pdf_sha256") != expected_pdf:
        raise ValueError("SOURCE_CANDIDATE_PDF_FINGERPRINT_MISMATCH")
    expected_range = [entry.get("pdf_start_page"), entry.get("pdf_end_page")]
    if candidate.get("source_pages") != expected_range:
        raise ValueError("SOURCE_CANDIDATE_PAGE_RANGE_MISMATCH")

    source = candidate.get("source_evidence") or {}
    exercises = source.get("exercise_evidence")
    if not isinstance(exercises, list) or not exercises:
        raise ValueError("SOURCE_CANDIDATE_EXERCISES_MISSING")
    ids = [str(item.get("exercise_id") or "").strip()
           for item in exercises if isinstance(item, dict)]
    if len(ids) != len(exercises) or any(not item for item in ids):
        raise ValueError("SOURCE_CANDIDATE_EXERCISE_ID_MISSING")
    if len(ids) != len(set(ids)):
        raise ValueError("SOURCE_CANDIDATE_EXERCISE_ID_DUPLICATED")

    for item in exercises:
        page = item.get("source_page")
        if not isinstance(page, int) or not expected_range[0] <= page <= expected_range[1]:
            raise ValueError("SOURCE_CANDIDATE_EXERCISE_PAGE_OUT_OF_RANGE")
        if not str(item.get("exact_source_prompt") or "").strip():
            raise ValueError("SOURCE_CANDIDATE_EXERCISE_PROMPT_MISSING")
        if not str(item.get("source_prompt_hash") or "").strip():
            raise ValueError("SOURCE_CANDIDATE_EXERCISE_PROMPT_HASH_MISSING")
        if item.get("source_origin") != "TEXTBOOK":
            raise ValueError("SOURCE_CANDIDATE_NON_TEXTBOOK_EXERCISE")

    completeness = source.get("source_completeness") or {}
    if completeness.get("source_inventory_candidate_complete") is not True:
        raise ValueError("SOURCE_CANDIDATE_INVENTORY_NOT_COMPLETE")
    if completeness.get("exercise_group_count") != len(exercises):
        raise ValueError("SOURCE_CANDIDATE_COUNT_MISMATCH")
    if completeness.get("independent_review") != "NOT_RUN":
        raise ValueError("SOURCE_CANDIDATE_REVIEW_STATUS_INVALID")
    if completeness.get("passed") is not False or completeness.get("blocking") is not True:
        raise ValueError("SOURCE_CANDIDATE_MUST_REMAIN_BLOCKING")

    imported = copy.deepcopy(exercises)
    for item in imported:
        item["source_correction_pending_independent_review"] = True
        item["verified_against_source"] = bool(item.get("verified_against_source"))

    repaired = dict(evidence_map)
    repaired["exercise_evidence"] = imported
    repaired["source_completeness"] = copy.deepcopy(completeness)
    repaired["source_backlog"] = copy.deepcopy(source.get("source_backlog") or {})
    repaired["source_candidate"] = {
        "input_sha256": candidate.get("input_sha256"),
        "status": candidate.get("status"),
        "exercise_group_count": len(imported),
        "independent_review": "NOT_RUN",
        "publication_allowed": False,
    }
    return repaired
