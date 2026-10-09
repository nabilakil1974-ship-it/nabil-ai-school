from __future__ import annotations

"""Pragmatic scientific gate: block only deterministic or located contradictions."""

import json
import re
import unicodedata
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Literal

from pydantic import BaseModel, Field

Category = Literal[
    "ocr_typo", "spacing", "symbol", "formatting",
    "formula_error", "wrong_concept", "false_statement", "unclear_evidence",
]


class ReviewerIssue(BaseModel):
    category: Category
    quote: str = Field(
        description="VERBATIM excerpt from the student-facing lesson text")
    message: str
    confidence: float = Field(ge=0, le=1)


class ReviewerReport(BaseModel):
    issues: list[ReviewerIssue] = Field(default_factory=list)


_SUP = str.maketrans({
    "⁰": "^0", "¹": "^1", "²": "^2", "³": "^3", "⁴": "^4",
    "⁵": "^5", "⁶": "^6", "⁷": "^7", "⁸": "^8", "⁹": "^9",
    "⁻": "^-",
})
_CHAR_MAP = str.maketrans({
    "−": "-", "–": "-", "—": "-", "×": "×", "∙": "·", "⋅": "·",
    "÷": "÷", "\u00a0": " ", "\u2009": " ", "\u200a": " ",
})
_ZW = re.compile(r"[\u200b-\u200f\u202a-\u202e\ufeff]")


def normalize_ocr(text: str) -> str:
    t = unicodedata.normalize("NFKC", text or "")
    t = _ZW.sub("", t).translate(_CHAR_MAP)
    t = t.translate(_SUP)
    t = re.sub(r"(\d)\s*\^\s*(-?\d)", r"\1^\2", t)
    t = re.sub(r"\s*=\s*", " = ", t)
    t = re.sub(r"[ \t]+", " ", t)
    return t.strip()


def normalize_payload_strings(obj):
    if isinstance(obj, str):
        return normalize_ocr(obj)
    if isinstance(obj, list):
        return [normalize_payload_strings(x) for x in obj]
    if isinstance(obj, dict):
        return {
            k: (
                normalize_payload_strings(v)
                if k not in {"kind", "lang"} else v
            )
            for k, v in obj.items()
        }
    return obj


_NUM = r"\d+(?:/\d+)?"
_POW = re.compile(
    rf"(?<![\w.^])(?P<neg>-)?(?P<open>\()?\s*"
    rf"(?P<sign>-)?(?P<base>{_NUM})\s*(?(open)\))"
    rf"\s*\^\s*\{{?\s*(?P<exp>-?\d+)\s*\}}?\s*=\s*"
    rf"(?P<val>-?{_NUM})(?![\w/^])"
)


def check_power_claims(text: str) -> list[str]:
    bad = []
    for m in _POW.finditer(normalize_ocr(text)):
        try:
            base = Fraction(m["base"])
            exp = int(m["exp"])
            if abs(exp) > 64 or (base == 0 and exp <= 0):
                continue
            if m["open"] and m["sign"]:
                base = -base
                value = base ** exp
            elif m["neg"] and not m["open"]:
                value = -(base ** exp)
            else:
                value = base ** exp
            claimed = Fraction(m["val"])
        except (ValueError, ZeroDivisionError):
            continue
        if value != claimed:
            bad.append(
                f"{m.group(0).strip()}  (correct value: {value})")
    return bad


NOISE = {"ocr_typo", "spacing", "symbol", "formatting"}
SERIOUS = {"formula_error", "wrong_concept", "false_statement"}


def _squash(s: str) -> str:
    return re.sub(r"\s+", "", normalize_ocr(s)).casefold()


@dataclass
class GateResult:
    verdict: Literal[
        "PASS", "PASS_NORMALIZED", "PASS_FLAGGED", "BLOCK"]
    text: str
    needs_review: bool = False
    block_reasons: list[str] = field(default_factory=list)
    flagged: list[str] = field(default_factory=list)
    noise_count: int = 0


def scientific_gate(
        lesson_text: str,
        report: ReviewerReport,
        *,
        block_confidence: float = 0.8,
        emit=None,
) -> GateResult:
    text = normalize_ocr(lesson_text)
    squashed = _squash(text)
    changed = text != lesson_text

    reasons = [
        f"NUMERIC_POWER_MISMATCH: {m}"
        for m in check_power_claims(text)
    ]

    noise, flagged = 0, []
    for it in report.issues:
        located = (
            bool(it.quote.strip())
            and _squash(it.quote) in squashed
        )
        if it.category in NOISE:
            noise += 1
        elif (
            it.category in SERIOUS
            and located
            and it.confidence >= block_confidence
        ):
            reasons.append(
                f"REVIEWER_CONTRADICTION[{it.category}@"
                f"{it.confidence:.2f}]: {it.quote[:100]} -> "
                f"{it.message[:160]}")
        else:
            why = (
                "quote not found in lesson"
                if not located
                else "low confidence / unclear evidence"
            )
            flagged.append(
                f"{it.category}: {it.message[:140]} ({why})")

    if reasons:
        if emit is not None:
            emit("SCIENTIFIC_REVIEW_BLOCKED", reasons=reasons[:8])
        return GateResult(
            "BLOCK", text, True, reasons, flagged, noise)

    verdict = (
        "PASS_FLAGGED"
        if flagged
        else (
            "PASS_NORMALIZED"
            if (noise or changed)
            else "PASS"
        )
    )
    if verdict != "PASS" and emit is not None:
        emit(
            "SCIENTIFIC_REVIEW_TOLERATED",
            verdict=verdict,
            ocr_noise_ignored=noise,
            flagged=flagged[:8],
            text_normalized=changed,
        )
    return GateResult(
        verdict, text, bool(flagged), [], flagged, noise)


def report_from_json(raw: str) -> ReviewerReport:
    return ReviewerReport.model_validate_json(raw)
