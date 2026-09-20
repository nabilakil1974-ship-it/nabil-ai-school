"""Pure deterministic helpers for reusable textbook lesson packages."""
import hashlib
import json


def lesson_cache_key(
    grade: str, branch: str, subject: str, curriculum: str,
    language: str, lesson: str, teaching_mode: str,
) -> str:
    raw = "|".join(str(x or "").strip().casefold() for x in (
        grade, branch, subject, curriculum, language, lesson, teaching_mode,
    ))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def source_signature(source_chunks: list[dict]) -> str:
    rows = []
    for item in source_chunks or []:
        if not isinstance(item, dict):
            continue
        rows.append((
            str(item.get("book_id") or ""),
            str(item.get("page") or ""),
            str(item.get("pdf_page") or ""),
            str(item.get("text") or "")[:240],
        ))
    rows.sort()
    raw = json.dumps(rows, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()
