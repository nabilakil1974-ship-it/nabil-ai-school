"""Persistent lesson-package cache keyed by exact curriculum lesson and source set."""
import hashlib
import json
from sqlalchemy.orm import Session
from app.db.models import LessonPackage


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


def get_cached_lesson(db: Session, cache_key: str, signature: str):
    item = db.query(LessonPackage).filter(LessonPackage.cache_key == cache_key).first()
    if item is None or item.source_signature != signature:
        return None
    try:
        drawings = json.loads(item.drawings_json or "[]")
        sources = json.loads(item.sources_json or "[]")
    except Exception:
        return None
    if not isinstance(drawings, list) or not isinstance(sources, list):
        return None
    return {"reply": item.reply, "drawings": drawings, "sources": sources}


def save_cached_lesson(
    db: Session, *, cache_key: str, signature: str, grade: str, branch: str,
    subject: str, curriculum: str, language: str, lesson: str,
    reply: str, drawings: list[dict], sources: list[dict],
) -> None:
    if not reply or not signature:
        return
    item = db.query(LessonPackage).filter(LessonPackage.cache_key == cache_key).first()
    if item is None:
        item = LessonPackage(cache_key=cache_key)
    item.source_signature = signature
    item.grade = str(grade or "")
    item.branch = str(branch or "")
    item.subject = str(subject or "")
    item.curriculum = str(curriculum or "")
    item.language = str(language or "")
    item.lesson = str(lesson or "")
    item.reply = str(reply)
    item.drawings_json = json.dumps(drawings or [], ensure_ascii=False)
    item.sources_json = json.dumps(sources or [], ensure_ascii=False)
    db.add(item)
    db.commit()
