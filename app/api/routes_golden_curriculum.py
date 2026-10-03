"""Canonical Golden curriculum API used by the lesson selector.

This route deliberately exposes only lessons that are already marked Golden.
It does not generate lessons and does not invoke AI/RAG at student runtime.
"""
from __future__ import annotations

import re
from fastapi import APIRouter

from app.services.golden_store import list_registry_entries

router = APIRouter()


def _norm(value: str) -> str:
    return re.sub(r"[^a-z0-9\u0600-\u06ff]+", "", str(value or "").casefold())


def _grade_number(value: str) -> str:
    raw = str(value or "")
    compact = _norm(raw)
    ar = raw.replace(" ", "")
    if "الثالثثانوي" in ar:
        return "12"
    if "الثانيثانوي" in ar:
        return "11"
    if "الأولثانوي" in ar:
        return "10"
    match = re.search(r"(?:grade|g|eb)?0?([1-9]|1[0-2])", compact)
    return str(int(match.group(1))) if match else ""


def _subject_code(value: str) -> str:
    raw = str(value or "").casefold()
    compact = _norm(raw)
    if "رياض" in raw or compact in {"math", "maths", "mathematics", "mathematiques"}:
        return "MATH"
    if "فيز" in raw or compact in {"physics", "physique"}:
        return "PHYSICS"
    if "كيمي" in raw or compact in {"chemistry", "chimie"}:
        return "CHEMISTRY"
    if "biology" in compact or "biologie" in compact or "علومالحياة" in raw.replace(" ", ""):
        return "BIOLOGY"
    return ""


def _branch_code(value: str) -> str:
    raw = str(value or "").strip()
    upper = raw.upper()
    if upper == "GS" or "علوم عامة" in raw or "GENERAL SCIENCE" in upper or "SCIENCES GENERALES" in upper or "SCIENCES GÉNÉRALES" in upper:
        return "GS"
    return upper


@router.get("/chat/curriculum/lessons")
@router.get("/curriculum/lessons")
def golden_curriculum_lessons(grade: str = "", subject: str = "", language: str = "", branch: str = ""):
    grade_no = _grade_number(grade)
    subject_code = _subject_code(subject)
    branch_code = _branch_code(branch)
    requested_language = _norm(language)
    lessons = []

    for row in list_registry_entries():
        if not row.get("golden"):
            continue
        lesson_id = str(row.get("lesson_id") or "").strip().upper()
        parts = lesson_id.split("-")
        if len(parts) < 3:
            continue
        if grade_no and parts[0] != f"G{int(grade_no):02d}":
            continue
        if subject_code and parts[1] != subject_code:
            continue
        if branch_code and len(parts) >= 4 and parts[2] != branch_code:
            continue
        row_language = _norm(row.get("language") or "")
        if requested_language and row_language:
            aliases = {requested_language}
            if requested_language in {"english", "en"}:
                aliases |= {"english", "en"}
            elif requested_language in {"french", "fr", "francais", "français"}:
                aliases |= {"french", "fr", "francais", "français"}
            elif requested_language in {"arabic", "ar", "العربية"}:
                aliases |= {"arabic", "ar", "العربية"}
            if row_language not in aliases:
                continue
        lessons.append({
            "lesson_id": lesson_id,
            "title": str(row.get("title") or lesson_id),
            "version": str(row.get("version") or "0.01"),
            "language": str(row.get("language") or ""),
            "golden": True,
        })

    lessons.sort(key=lambda item: item["lesson_id"])
    return {
        "source": "canonical_golden_registry",
        "runtime_ai": False,
        "count": len(lessons),
        "lessons": lessons,
    }
