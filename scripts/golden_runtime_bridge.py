"""Production bridge: Golden lesson registry -> Drive -> student, with zero AI.

Installed before Uvicorn starts. Registered Golden lessons take precedence over
legacy prepared-HTML lookup. lesson_id is the canonical key; title matching is
only a backward-compatible fallback for older UI calls.
"""
from __future__ import annotations

import html
import re
from urllib.parse import quote

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse


def _norm(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(value or "").casefold())


def _grade_number(value: str) -> str:
    raw = str(value or "")
    compact = _norm(raw)
    if "الثالثثانوي" in raw.replace(" ", ""):
        return "12"
    if "الثانيثانوي" in raw.replace(" ", ""):
        return "11"
    if "الأولثانوي" in raw.replace(" ", ""):
        return "10"
    m = re.search(r"(?:grade|g|eb)?0?([1-9]|1[0-2])", compact)
    return str(int(m.group(1))) if m else ""


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


def _golden_entry(grade: str, subject: str, lesson: str, lesson_id: str = ""):
    from app.services.golden_store import get_registry_entry, list_registry_entries
    requested_id = str(lesson_id or "").strip().upper()
    lesson_as_id = str(lesson or "").strip().upper()
    if not requested_id and re.fullmatch(r"G\d{2}-[A-Z]+(?:-[A-Z]+)?-\d{3}", lesson_as_id):
        requested_id = lesson_as_id
    if requested_id:
        row = get_registry_entry(requested_id)
        if row and row.get("golden"):
            return row
        return None
    grade_no = _grade_number(grade)
    subject_code = _subject_code(subject)
    wanted = _norm(lesson)
    matches = []
    for row in list_registry_entries():
        row_id = str(row.get("lesson_id") or "").upper()
        title = str(row.get("title") or "")
        if not row.get("golden") or _norm(title) != wanted:
            continue
        parts = row_id.split("-")
        if grade_no and (not parts or parts[0] != f"G{int(grade_no):02d}"):
            continue
        if subject_code and (len(parts) < 2 or parts[1] != subject_code):
            continue
        matches.append(row)
    if len(matches) > 1:
        raise HTTPException(409, "Multiple Golden lessons match this title; send lesson_id.")
    return matches[0] if matches else None


def _drive_failure_detail(exc: Exception, lesson_id: str) -> dict:
    message = str(exc or "").strip() or repr(exc)
    cause = getattr(exc, "__cause__", None)
    context = getattr(exc, "__context__", None)
    detail = {"stage":"golden_drive","reason":type(exc).__name__,"message":message[:1200],"lesson_id":lesson_id}
    if cause is not None:
        detail["cause_type"] = type(cause).__name__
        detail["cause"] = (str(cause).strip() or repr(cause))[:1200]
    elif context is not None and context is not exc:
        detail["context_type"] = type(context).__name__
        detail["context"] = (str(context).strip() or repr(context))[:1200]
    return detail


def install_golden_runtime_bridge() -> None:
    from app.main import app
    from app.api import routes_interactive_lessons as legacy
    from app.services.golden_store import fetch_golden_from_drive, get_registry_entry
    if getattr(app.state, "nabil_golden_runtime_bridge", False):
        return
    bridge = APIRouter(prefix="/api/interactive-lessons")

    @bridge.get("/resolve")
    def golden_first_resolve(grade: str, subject: str, lesson: str = "", language: str = "", lesson_id: str = ""):
        entry = _golden_entry(grade, subject, lesson, lesson_id=lesson_id)
        if entry is None:
            if lesson_id:
                raise HTTPException(404, detail={"stage":"golden_registry","reason":"LESSON_ID_NOT_FOUND","lesson_id":lesson_id})
            return legacy.resolve(grade=grade, subject=subject, lesson=lesson, language=language)
        resolved_id = str(entry["lesson_id"])
        lang = str(entry.get("language") or language or "en")
        version = str(entry.get("version") or "0.01")

        # Owner-requested live isolation test.  G12-MATH-GS-001 is a native
        # Google Doc, unlike the old G07 Physics prepared HTML.  Do not ask the
        # Railway service account to download it: let the browser render the
        # exact registered Drive document.  This identifies auth vs rendering.
        if resolved_id == "G12-MATH-GS-001" and entry.get("drive_file_id"):
            return {
                "found": True,
                "title": entry.get("title") or lesson,
                "url": "/api/interactive-lessons/golden-drive-preview?lesson_id=" + quote(resolved_id),
                "source": "golden_registry_browser_drive_preview",
                "bytes": 0,
                "lesson_id": resolved_id,
                "zero_ai": True,
                "resolved_by": "lesson_id" if lesson_id else "title_fallback",
            }

        try:
            payload = fetch_golden_from_drive(resolved_id, lang, version)
        except Exception as exc:
            raise HTTPException(503, detail=_drive_failure_detail(exc, resolved_id)) from exc
        url = "/api/interactive-lessons/golden-view?lesson_id=" + quote(resolved_id) + "&language=" + quote(lang) + "&version=" + quote(version)
        return {"found":True,"title":payload.get("title") or entry.get("title") or lesson,"url":url,"source":"golden_drive_zero_ai","bytes":len((payload.get("lesson_html") or payload.get("reply") or "").encode("utf-8")),"lesson_id":resolved_id,"zero_ai":True,"resolved_by":"lesson_id" if lesson_id else "title_fallback"}

    @bridge.get("/golden-drive-preview", response_class=HTMLResponse)
    def golden_drive_preview(lesson_id: str):
        entry = get_registry_entry(lesson_id)
        if not entry or not entry.get("golden"):
            raise HTTPException(404, "GOLDEN_LESSON_NOT_FOUND")
        file_id = str(entry.get("drive_file_id") or "").strip()
        if not re.fullmatch(r"[A-Za-z0-9_-]{10,200}", file_id):
            raise HTTPException(422, "GOLDEN_DRIVE_FILE_ID_INVALID")
        title = html.escape(str(entry.get("title") or lesson_id))
        src = "https://docs.google.com/document/d/" + quote(file_id) + "/preview"
        markup = """<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>%s</title><style>html,body{margin:0;width:100%%;height:100%%;background:#071d30}iframe{border:0;width:100%%;height:100vh;display:block}.tag{position:fixed;z-index:2;left:8px;top:8px;background:#063b59;color:#8ee8ff;padding:6px 10px;border-radius:8px;font:12px monospace}</style></head><body><div class='tag'>GOLDEN DIRECT DRIVE TEST · %s</div><iframe src='%s' title='%s' allow='clipboard-read; clipboard-write'></iframe></body></html>""" % (title, html.escape(lesson_id), html.escape(src, quote=True), title)
        return HTMLResponse(markup, headers={"Cache-Control":"no-store","Content-Security-Policy":"default-src 'self' https: data: blob:; frame-src https://docs.google.com https://drive.google.com; style-src 'unsafe-inline' 'self'; frame-ancestors 'self'","X-NABIL-Lesson-Source":"golden-browser-drive-preview","X-NABIL-Lesson-ID":lesson_id})

    @bridge.get("/golden-view", response_class=HTMLResponse)
    def golden_view(lesson_id: str, language: str = "en", version: str = "0.01"):
        try:
            payload = fetch_golden_from_drive(lesson_id, language, version)
        except Exception as exc:
            raise HTTPException(503, detail=_drive_failure_detail(exc, lesson_id)) from exc
        markup = str(payload.get("lesson_html") or "").strip()
        if not markup:
            text = html.escape(str(payload.get("reply") or ""))
            markup = "<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><style>body{font:18px/1.65 Arial,sans-serif;margin:0;padding:24px;background:#071d30;color:#eefaff}pre{white-space:pre-wrap}</style></head><body><pre>" + text + "</pre></body></html>"
        return HTMLResponse(markup, headers={"Cache-Control":"private, no-store","Content-Security-Policy":"default-src 'self' data: blob: https:; script-src 'unsafe-inline' 'self' https:; style-src 'unsafe-inline' 'self' https:; frame-ancestors 'self'","X-NABIL-Lesson-Source":"golden-drive-zero-ai","X-NABIL-Lesson-ID":lesson_id})

    for route in reversed(bridge.routes):
        app.router.routes.insert(0, route)
    app.state.nabil_golden_runtime_bridge = True
