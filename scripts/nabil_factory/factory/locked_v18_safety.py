"""NABIL V18 — isolated, fail-closed factory safety contracts.

This module does not render lessons and must never import V18 UI modules.
Keep scientific/source/publication safeguards independent of future UI changes.
"""
from __future__ import annotations

import re
from fractions import Fraction

LOCKED_CONTRACT_VERSION = "nabil-factory-safety/v18.1"
MANDATORY_COMPONENTS = (
    "source_identity", "source_page_evidence", "scientific_review",
    "deterministic_math", "publication_quality_gate",
    "verified_drive_upload", "checkpoint_resume",
)

class SafetyContractViolation(RuntimeError):
    pass

def assert_safe_factory_boundaries() -> None:
    """Reject changes that silently couple safety contracts to visual rendering."""
    if len(set(MANDATORY_COMPONENTS)) != len(MANDATORY_COMPONENTS):
        raise SafetyContractViolation("DUPLICATE_FACTORY_CONTRACT")
    if any(not re.fullmatch(r"[a-z][a-z0-9_]+", x) for x in MANDATORY_COMPONENTS):
        raise SafetyContractViolation("INVALID_FACTORY_CONTRACT_NAME")

def assert_source_identity(entry: dict, source_book_id: str) -> None:
    if not isinstance(entry, dict) or not entry.get("lesson_id"):
        raise SafetyContractViolation("LESSON_IDENTITY_MISSING")
    if not source_book_id or str(entry.get("book_id") or "") != str(source_book_id):
        raise SafetyContractViolation("SOURCE_BOOK_ID_MISMATCH")

def assert_verified_publication(*, quality_passed: bool,
                                scientific_status: str,
                                upload_verified: bool) -> None:
    if not quality_passed:
        raise SafetyContractViolation("QUALITY_GATE_NOT_PASSED")
    if scientific_status not in {"APPROVED", "PASS", "VERIFIED"}:
        raise SafetyContractViolation("SCIENTIFIC_REVIEW_NOT_VERIFIED")
    if not upload_verified:
        raise SafetyContractViolation("DRIVE_UPLOAD_NOT_VERIFIED")

def verify_rational_arithmetic(numerator: int, denominator: int,
                               expected_numerator: int,
                               expected_denominator: int) -> None:
    if not denominator or not expected_denominator:
        raise SafetyContractViolation("INVALID_ZERO_DENOMINATOR")
    if Fraction(numerator, denominator) != Fraction(expected_numerator, expected_denominator):
        raise SafetyContractViolation("DETERMINISTIC_MATH_MISMATCH")

assert_safe_factory_boundaries()
