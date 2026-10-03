"""Canonical Golden lesson catalogue and zero-runtime-AI classroom routes.

This replaces the retired scripts/golden_runtime_bridge.py monkey-patch.
Routes returned by build_router() are relative to /api; app/main.py owns the /api prefix.
"""
from __future__ import annotations

import html
import json
import re
import time
from pathlib import Path
from urllib.parse import quote

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

GOLDEN_ARTIFACT_DIR = Path("data/golden_artifacts")
RENDERER_URL = "/static/nabil_classroom_engine_v10.js?v=15"
_CACHE = {"at": 0.0, "rows": []}
LANG_CODES = {"EN", "FR", "AR"}
BRANCH_CODES = {"GS", "LS", "SV", "SE", "ES", "LH", "HUM"}


def _norm(v):
    return re.sub(r"[^a-z0-9\u0600-\u06ff]+", "", str(v or "").casefold())


def _grade(v):
    raw = str(v or "").strip()
    x = _norm(raw)
    if re.fullmatch(r"(?:[1-9]|10|11|12)", raw):
        return str(int(raw))
    secondary = [
        (("الثالثثانوي", "الصفالثالثثانوي", "الثانيعشر", "الصفالثانيعشر"), "12"),
        (("الثانيثانوي", "الصفالثانيثانوي", "الحاديعشر", "الصفالحاديعشر"), "11"),
        (("الأولثانوي", "الاولثانوي", "الصفالأولثانوي", "الصفالاولثانوي", "العاشر", "الصفالعاشر"), "10"),
    ]
    for names, n in secondary:
        if any(_norm(k) in x for k in names):
            return n
    primary = [("التاسع","9"),("الثامن","8"),("السابع","7"),("السادس","6"),("الخامس","5"),("الرابع","4"),("الثالث","3"),("الثاني","2"),("الأول","1"),("الاول","1")]
    for k, n in primary:
        if _norm(k) in x:
            return n
    m = re.search(r"(?:grade|eb|g)0?([1-9]|1[0-2])$", x)
    return str(int(m.group(1))) if m else ""


def _subject(v):
    x = _norm(v)
    if "رياض" in x or x in {"math", "maths", "mathematics", "mathematiques"}: return "MATH"
    if "فيز" in x or x in {"physics", "physique"}: return "PHYSICS"
    if "كيمي" in x or x in {"chemistry", "chimie"}: return "CHEMISTRY"
    if "علومالحياة" in x or x in {"biology", "biologie"}: return "BIOLOGY"
    return ""


def _branch(v):
    x = _norm(v); u = str(v or "").strip().upper()
    if not x: return ""
    if u == "GS" or "علومعامة" in x: return "GS"
    if u in {"LS", "SV"} or "علومالحياة" in x: return "LS"
    if u in {"SE", "ES"} or "اجتماع" in x or "اقتصاد" in x: return "SE"
    if u in {"LH", "HUM"} or "آداب" in x or "انساني" in x: return "LH"
    return ""


def _lang(v):
    x = _norm(v)
    if x in {"en", "english", "anglais"}: return "EN"
    if x in {"fr", "french", "francais"}: return "FR"
    if x in {"ar", "arabic", "العربية", "عربي"}: return "AR"
    return ""


def _meta(lid):
    p = str(lid or "").strip().upper().split("-")
    if len(p) < 3 or not re.fullmatch(r"G\d{2}", p[0]) or not re.fullmatch(r"\d{3}", p[-1]):
        return None
    grade, subject = str(int(p[0][1:])), p[1]
    branch = ""; lang = ""
    for token in p[2:-1]:
        if token in LANG_CODES:
            lang = token
        elif token in BRANCH_CODES:
            branch = {"SV":"LS", "ES":"SE", "HUM":"LH"}.get(token, token)
    return {"grade": grade, "subject": subject, "branch": branch, "language": lang, "seq": p[-1]}


def _drive_rows(force=False):
    if _CACHE["rows"] and not force and time.time() - _CACHE["at"] < 60:
        return _CACHE["rows"]
    from scripts.index_books import get_drive_service
    svc = get_drive_service(); rows = []; token = None
    while True:
        result = svc.files().list(
            q="trashed=false", spaces="drive",
            fields="nextPageToken,files(id,name,mimeType,webViewLink,appProperties)",
            pageSize=1000, pageToken=token,
        ).execute()
        for f in result.get("files", []):
            props = f.get("appProperties") or {}
            lid = str(props.get("nabil_lesson_id") or "").strip().upper()
            meta = _meta(lid)
            if not meta or not re.fullmatch(r"G\d{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3}", lid):
                continue
            kind = str(props.get("nabil_artifact") or "theory").lower()
            if kind not in {"theory", "lesson", "golden", "golden_lesson"}:
                continue
            title = str(props.get("nabil_title") or props.get("lesson_title") or f.get("name") or lid)
            title = re.sub("^" + re.escape(lid) + r"\s*[—–:-]?\s*", "", title, flags=re.I).strip() or lid
            rows.append({
                "lesson_id": lid, "title": title,
                "language": str(props.get("nabil_language") or props.get("language") or meta["language"] or "en"),
                "version": str(props.get("nabil_version") or props.get("version") or "0.01"),
                "drive_file_id": f["id"], "drive_theory_id": f["id"],
                "drive_url": f.get("webViewLink"),
                "mime_type": f.get("mimeType") or "application/vnd.google-apps.document",
                "golden": True,
            })
        token = result.get("nextPageToken")
        if not token: break
    dedup = {x["lesson_id"]: x for x in rows}
    _CACHE.update(at=time.time(), rows=[dedup[k] for k in sorted(dedup)])
    return _CACHE["rows"]


def _catalogue(grade, subject, language="", branch=""):
    gn, sc, bc, lc = _grade(grade), _subject(subject), _branch(branch), _lang(language)
    if not gn or not sc: return []
    out = []
    for row in _drive_rows():
        m = _meta(row["lesson_id"])
        if not m or m["grade"] != gn or m["subject"] != sc: continue
        if m["branch"] and m["branch"] != bc: continue
        if gn == "12" and m["branch"] and not bc: continue
        row_lang = m["language"] or _lang(row.get("language"))
        if lc and row_lang and lc != row_lang: continue
        out.append({k: row[k] for k in ("lesson_id", "title", "version", "language", "golden")})
    return out


def _entry(lid):
    lid = str(lid or "").strip().upper()
    return next((r for r in _drive_rows() if r["lesson_id"] == lid), None)


def _source(entry):
    lid = entry["lesson_id"]
    local = GOLDEN_ARTIFACT_DIR / f"{lid}.txt"
    if local.exists() and (text := local.read_text(encoding="utf-8").strip()):
        return text, "golden_structured_artifact"
    from app.services.golden_store import _drive_service, _fetch_artifact
    item = _fetch_artifact(_drive_service(), {
        "drive_file_id": entry["drive_file_id"], "mime_type": entry["mime_type"],
        "name": entry["title"], "artifact_id": lid + "-LESSON",
    })
    if not item or not str(item.get("text") or "").strip():
        raise RuntimeError("GOLDEN_TEACHING_TEXT_EMPTY:" + lid)
    return str(item["text"]).strip(), "golden_drive_0.01"


def _page(entry, text, source):
    payload = json.dumps({"lesson_id": entry["lesson_id"], "title": entry["title"], "text": text, "source": source}, ensure_ascii=False).replace("</", "<\\/")
    return f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(entry['title'])}</title><style>html,body,#nabil-classroom-root{{margin:0;min-height:100%;background:#030b14}}</style></head><body><main id="nabil-classroom-root"></main><script>window.__NABIL_GOLDEN__={payload};</script><script src="{RENDERER_URL}"></script><script>(function(){{var r=window.NABILClassroomV10,p=window.__NABIL_GOLDEN__,root=document.getElementById('nabil-classroom-root');if(r&&p)r.mount(root,p.text,p.title,p);else root.innerHTML='<pre style="color:#f99">NABIL classroom failed to load</pre>';}})();</script></body></html>'''


def build_router() -> APIRouter:
    """Build canonical routes. app/main.py registers this router with prefix='/api'."""
    router = APIRouter()

    @router.get("/chat/curriculum/lessons")
    @router.get("/curriculum/lessons")
    def curriculum(grade: str = "", subject: str = "", language: str = "", branch: str = ""):
        rows = _catalogue(grade, subject, language, branch)
        return {"source": "canonical_golden_registry", "runtime_ai": False, "count": len(rows), "lessons": rows}

    @router.get("/interactive-lessons/resolve")
    def resolve(grade: str, subject: str, lesson: str = "", language: str = "", lesson_id: str = "", branch: str = ""):
        lid = str(lesson_id or "").strip().upper()
        entry = _entry(lid)
        if not entry: raise HTTPException(404, "GOLDEN_LESSON_NOT_FOUND")
        m = _meta(lid)
        if not m or m["grade"] != _grade(grade) or m["subject"] != _subject(subject) or (m["branch"] and m["branch"] != _branch(branch)):
            raise HTTPException(404, "GOLDEN_SELECTION_MISMATCH")
        text, source = _source(entry)
        return {"found": True, "title": entry["title"], "url": "/api/interactive-lessons/golden-classroom?lesson_id=" + quote(lid), "source": source, "bytes": len(text.encode()), "lesson_id": lid, "zero_ai": True, "renderer": "nabil_classroom_v15"}

    @router.get("/interactive-lessons/golden-classroom", response_class=HTMLResponse)
    def classroom(lesson_id: str):
        entry = _entry(lesson_id)
        if not entry: raise HTTPException(404, "GOLDEN_LESSON_NOT_FOUND")
        text, source = _source(entry)
        return HTMLResponse(_page(entry, text, source), headers={"Cache-Control": "no-store", "X-NABIL-Lesson-ID": entry["lesson_id"], "X-NABIL-Lesson-Source": source})

    @router.get("/interactive-lessons/golden-structured-view", response_class=HTMLResponse)
    def old_structured(lesson_id: str):
        return classroom(lesson_id)

    return router
