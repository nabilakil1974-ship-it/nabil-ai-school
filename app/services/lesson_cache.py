"""Persistent lesson-package cache keyed by exact curriculum lesson and source set."""
import json
from sqlalchemy.orm import Session
from app.db.models import LessonPackage


from app.core.lesson_cache_contract import lesson_cache_key, source_signature

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
