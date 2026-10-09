from __future__ import annotations

"""Fuzzy, normalized TOC-vs-opener title verification. Never raises."""

import json
import re
import unicodedata
from dataclasses import asdict, dataclass
from difflib import SequenceMatcher

ACCEPT_THRESHOLD = 85.0
REVIEW_FLOOR = 60.0

_AR_MARKS = re.compile(r"[\u064B-\u065F\u0670\u0640]")
_LEAD_NUM = re.compile(
    r"^\s*(?:lesson|leçon|lecon|درس|الدرس)?\s*\d+"
    r"(?:\s*[.\-–—]\s*\d+)*\s*[:.\-–—)]?\s*",
    re.I,
)
_ZW = re.compile(r"[\u200b-\u200f\u202a-\u202e\ufeff]")


def normalize_title(s: str, *, strip_numbering: bool = True) -> str:
    s = unicodedata.normalize("NFKC", s or "")
    s = _ZW.sub("", s)
    if strip_numbering:
        s = _LEAD_NUM.sub("", s)
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = _AR_MARKS.sub("", s)
    s = re.sub("[إأآٱ]", "ا", s).replace("ى", "ي")
    s = s.casefold()
    s = "".join(
        " " if unicodedata.category(c)[0] in "PSZC" else c
        for c in s
    )
    return re.sub(r"\s+", " ", s).strip()


def _digits(s: str) -> list[str]:
    return re.findall(r"\d+", unicodedata.normalize("NFKC", s or ""))


def similarity(a: str, b: str) -> float:
    na, nb = normalize_title(a), normalize_title(b)
    if not na or not nb:
        return 0.0
    if na == nb:
        return 100.0
    ratio = SequenceMatcher(None, na, nb).ratio()
    ts = SequenceMatcher(
        None,
        " ".join(sorted(na.split())),
        " ".join(sorted(nb.split())),
    ).ratio()
    score = max(ratio, ts) * 100
    short, long_ = sorted((na, nb), key=len)
    if (
        len(short) >= 4
        and re.search(rf"(?<!\w){re.escape(short)}(?!\w)", long_)
    ):
        score = max(score, 95.0)
    return score


@dataclass(frozen=True)
class TitleDecision:
    title: str
    status: str
    score: float
    needs_review: bool
    reason: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def _clean(s: str) -> str:
    return re.sub(
        r"\s+", " ", unicodedata.normalize("NFKC", s or "")
    ).strip()


def best_title_candidate(text: str, expected_hint: str = "") -> str:
    """Pick the OCR line most title-like and closest to the expected hint."""
    lines = [
        _clean(line) for line in str(text or "").splitlines()
        if 2 <= len(_clean(line)) <= 180
    ]
    if not lines:
        return ""
    if expected_hint:
        return max(lines, key=lambda line: similarity(line, expected_hint))
    return lines[0]


def verify_title(
        toc_title: str,
        opener_title: str,
        *,
        fallback_title: str,
        emit=None,
        lesson_id: str = "",
) -> TitleDecision:
    """Never raises. Low-confidence identity becomes needs_review."""
    toc, opener = _clean(toc_title), _clean(opener_title)

    if not toc and not opener:
        d = TitleDecision(
            fallback_title, "FALLBACK_PLACEHOLDER", 0.0, True,
            "both titles empty",
        )
    elif not toc or not opener:
        only = toc or opener
        d = TitleDecision(
            only,
            "FALLBACK_TOC" if toc else "FALLBACK_OPENER",
            0.0,
            True,
            "only one title evidence available",
        )
    else:
        score = similarity(toc, opener)
        toc_digits_raw = _digits(
            normalize_title(toc, strip_numbering=False))
        opener_digits_raw = _digits(
            normalize_title(opener, strip_numbering=False))
        toc_digits_clean = _digits(normalize_title(toc))
        opener_digits_clean = _digits(normalize_title(opener))
        digits_ok = (
            toc_digits_raw == opener_digits_raw
            or toc_digits_clean == opener_digits_clean
        )
        if score >= ACCEPT_THRESHOLD and digits_ok:
            d = TitleDecision(toc, "ACCEPTED", score, False)
        elif score >= REVIEW_FLOOR and digits_ok:
            d = TitleDecision(
                toc, "FALLBACK_TOC", score, False,
                "below accept threshold; using TOC title",
            )
        else:
            reason = (
                "digit mismatch between TOC and opener"
                if not digits_ok
                else "titles disagree strongly; lesson boundaries may be wrong"
            )
            d = TitleDecision(
                toc, "FALLBACK_TOC", score, True, reason)

    stage = (
        "TITLE_VERIFIED_FUZZY"
        if d.status == "ACCEPTED"
        else (
            "TITLE_FALLBACK_LOW_CONFIDENCE"
            if d.needs_review
            else "TITLE_FALLBACK_TOC_WARNING"
        )
    )
    payload = {
        "lesson_id": lesson_id,
        "status": d.status,
        "score": round(d.score, 1),
        "needs_review": d.needs_review,
        "toc": toc,
        "opener": opener,
        "chosen": d.title,
        "reason": d.reason,
    }
    if emit is not None:
        try:
            emit(stage, **payload)
        except TypeError:
            emit(json.dumps(
                {"stage": stage, **payload},
                ensure_ascii=False,
            ))
    return d
