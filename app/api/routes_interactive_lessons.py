"""Serve prepared interactive HTML lessons from Google Drive, never from app/static.

Configure NABIL_INTERACTIVE_LESSONS_FOLDER_ID (shared with the backend service
account) or NABIL_INTERACTIVE_LESSONS_CATALOG_FILE_ID for an explicit JSON catalog.
The catalog is stored on Drive, NOT in the repository:
{"lessons":[{"grade":"الصف التاسع","subject":"فيزياء","lesson":"Conducteurs ohmiques",
"language":"Français","drive_file_id":"...","aliases":["Ohmic conductors"]}]}
"""
import io
import logging
import uuid
import json
import os
import re
import unicodedata
from time import monotonic
from urllib.parse import quote

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from googleapiclient.http import MediaIoBaseDownload

router = APIRouter(prefix="/interactive-lessons", tags=["drive-interactive-lessons"])
log = logging.getLogger("nabil_ai.drive_lessons")
_CACHE = {"at": 0.0, "entries": []}
_DEFAULT_FOLDER = "19Y7wVw2hBYG6_aHe6nygXVZmRJXoHvoM"  # Existing Drive lesson collection; configurable.


def _service():
    from scripts.index_books import get_drive_service
    return get_drive_service()


def _download(service, file_id):
    stream = io.BytesIO()
    media = service.files().get_media(fileId=file_id)
    loader = MediaIoBaseDownload(stream, media)
    done = False
    while not done:
        _, done = loader.next_chunk()
        if stream.tell() > 8_000_000:
            raise ValueError("INTERACTIVE_LESSON_TOO_LARGE")
    return stream.getvalue()


def _norm(value):
    value = unicodedata.normalize("NFKC", str(value or "")).casefold()
    value = re.sub(r"[\u064b-\u065f]", "", value)
    return re.sub(r"[^\w]+", "", value, flags=re.UNICODE)


def _grade(value):
    s = _norm(value)
    for number, names in {
        7: ("7", "٧", "السابع", "septieme", "seventh"),
        8: ("8", "٨", "الثامن", "huitieme", "eighth"),
        9: ("9", "٩", "التاسع", "neuvieme", "ninth"),
    }.items():
        if any(n in s for n in names):
            return str(number)
    return s


def _entries():
    now = monotonic()
    if now - _CACHE["at"] < 120:
        log.info("DRIVE_LESSON_CATALOG_CACHE_HIT entries=%d", len(_CACHE["entries"]))
        return _CACHE["entries"]
    log.info("DRIVE_LESSON_CONNECT_START")
    service = _service()
    log.info("DRIVE_LESSON_CONNECT_OK")
    catalog_id = os.getenv("NABIL_INTERACTIVE_LESSONS_CATALOG_FILE_ID", "").strip()
    if catalog_id:
        log.info("DRIVE_LESSON_CATALOG_FETCH_START")
        payload = json.loads(_download(service, catalog_id).decode("utf-8-sig"))
        items = payload.get("lessons", [])
        if not isinstance(items, list):
            raise ValueError("INVALID_LESSON_CATALOG")
    else:
        folder = os.getenv("NABIL_INTERACTIVE_LESSONS_FOLDER_ID", _DEFAULT_FOLDER).strip()
        log.info("DRIVE_LESSON_FOLDER_LIST_START folder=%s", folder)
        # Filename convention: G09-PHYSICS--LESSON-TITLE.html (catalog preferred).
        items, token = [], None
        while True:
            result = service.files().list(
                q=f"'{folder}' in parents and trashed=false",
                fields="nextPageToken,files(id,name,mimeType)",
                pageSize=1000, pageToken=token,
            ).execute()
            for file in result.get("files", []):
                if file["name"].lower().endswith(".html"):
                    stem = file["name"].rsplit(".", 1)[0]
                    parts = re.split(r"--", stem, maxsplit=1)
                    if len(parts) == 2:
                        prefix, title = parts
                        tokens = prefix.split("-", 1)
                        grade, subject = (tokens + [""])[:2]
                    else:
                        match = re.match(r"(?:EB|G)[-_ ]?0?(\d{1,2})[-_ ]+(.*)", stem, re.I)
                        grade = match.group(1) if match else ""
                        subject = ""
                        title = match.group(2) if match else stem
                    title = re.sub(r"[-_ ]+(?:BILINGUAL|FRANCAIS|ENGLISH)$", "", title, flags=re.I)
                    items.append({"grade": grade, "subject": subject,
                                  "lesson": title.replace("-", " "),
                                  "drive_file_id": file["id"], "language": "",
                                  "filename": file["name"]})
            token = result.get("nextPageToken")
            if not token:
                break
    valid = [x for x in items if isinstance(x, dict) and x.get("drive_file_id") and x.get("lesson")]
    log.info("DRIVE_LESSON_FOLDER_LIST_OK entries=%d names=%s", len(valid), [x.get("filename", x["lesson"]) for x in valid[:20]])
    _CACHE.update(at=now, entries=valid)
    return valid


def _resolve(grade, subject, lesson, language):
    matches = []
    for item in _entries():
        if item.get("grade") and _grade(item["grade"]) != _grade(grade):
            continue
        if item.get("subject") and _norm(item["subject"]) != _norm(subject):
            continue
        titles = [item["lesson"]] + list(item.get("aliases") or [])
        if _norm(lesson) not in {_norm(title) for title in titles}:
            continue
        if language and item.get("language") and _norm(language) != _norm(item["language"]):
            continue
        matches.append(item)
    log.info("DRIVE_LESSON_MATCH grade=%r subject=%r lesson=%r language=%r count=%d", grade, subject, lesson, language, len(matches))
    if len(matches) > 1:
        bilingual = [x for x in matches if x.get("bilingual") or "BILINGUAL" in str(x.get("filename", "")).upper()]
        if len(bilingual) == 1:
            matches = bilingual
        else:
            raise HTTPException(409, "Multiple prepared lessons match; specify the language and textbook.")
    if not matches:
        raise HTTPException(404, "No prepared interactive lesson in the configured Google Drive collection.")
    return matches[0]



@router.get("/diagnose")
def diagnose(grade: str, subject: str, lesson: str, language: str = ""):
    """Temporary owner-facing, read-only end-to-end trace; no AI calls."""
    trace = uuid.uuid4().hex[:12]
    steps = []
    def step(stage, **details):
        record = {"step": len(steps)+1, "stage": stage, **details}
        steps.append(record)
        log.info("DRIVE_LESSON_DIAGNOSTIC trace=%s step=%s stage=%s details=%s",
                 trace, record["step"], stage, details)
    step("REQUEST_RECEIVED", grade=grade, subject=subject, lesson=lesson, language=language)
    try:
        step("DRIVE_AUTH_START")
        service = _service()
        step("DRIVE_AUTH_OK")
        folder = os.getenv("NABIL_INTERACTIVE_LESSONS_FOLDER_ID", _DEFAULT_FOLDER).strip()
        catalog_id = os.getenv("NABIL_INTERACTIVE_LESSONS_CATALOG_FILE_ID", "").strip()
        step("SOURCE_SELECTED", source="catalog" if catalog_id else "folder",
             folder=folder if not catalog_id else None)
        # Force refresh for diagnosis; do not mistake an earlier cached list for live Drive access.
        _CACHE["at"] = 0.0
        items = _entries()
        step("DRIVE_LIST_OK", count=len(items),
             filenames=[x.get("filename", x.get("lesson")) for x in items[:30]])
        matches = []
        for item in items:
            if item.get("grade") and _grade(item["grade"]) != _grade(grade):
                continue
            if item.get("subject") and _norm(item["subject"]) != _norm(subject):
                continue
            if _norm(lesson) not in {_norm(x) for x in [item["lesson"]] + list(item.get("aliases") or [])}:
                continue
            if language and item.get("language") and _norm(language) != _norm(item["language"]):
                continue
            matches.append(item)
        step("TITLE_MATCH", count=len(matches),
             filenames=[x.get("filename", x["lesson"]) for x in matches])
        if not matches:
            step("NO_PREPARED_LESSON", next="AI_TEXTBOOK_FALLBACK")
            return {"trace": trace, "found": False, "steps": steps}
        item = _resolve(grade, subject, lesson, language)
        step("FILE_SELECTED", filename=item.get("filename", item["lesson"]))
        data = _download(service, item["drive_file_id"])
        step("FILE_DOWNLOADED", bytes=len(data))
        if b"<html" not in data[:4096].lower() and b"<!doctype html" not in data[:4096].lower():
            raise ValueError("INVALID_PREPARED_LESSON_HTML")
        step("HTML_VERIFIED", next="DISPLAY_DRIVE_LESSON_WITHOUT_AI")
        return {"trace": trace, "found": True, "steps": steps}
    except Exception as exc:
        step("DIAGNOSTIC_FAILED", error_type=type(exc).__name__,
             http_status=getattr(getattr(exc, "resp", None), "status", None),
             next="AI_TEXTBOOK_FALLBACK")
        log.exception("DRIVE_LESSON_DIAGNOSTIC_FAILED trace=%s", trace)
        return {"trace": trace, "found": False, "steps": steps}

@router.get("/resolve")
def resolve(grade: str, subject: str, lesson: str, language: str = ""):
    trace = uuid.uuid4().hex[:12]
    started = monotonic()
    log.info("DRIVE_LESSON_LOOKUP_START trace=%s grade=%r subject=%r lesson=%r language=%r",
             trace, grade, subject, lesson, language)
    try:
        item = _resolve(grade, subject, lesson, language)
        log.info("DRIVE_LESSON_FOUND trace=%s file=%s name=%r",
                 trace, item["drive_file_id"], item.get("filename", item["lesson"]))
        html_bytes = _download(_service(), item["drive_file_id"])
        if b"<html" not in html_bytes[:4096].lower() and b"<!doctype html" not in html_bytes[:4096].lower():
            raise ValueError("INVALID_PREPARED_LESSON_HTML")
        log.info("DRIVE_LESSON_READ_OK trace=%s bytes=%d elapsed_ms=%d",
                 trace, len(html_bytes), round((monotonic()-started)*1000))
        url = ("/api/interactive-lessons/view?grade=" + quote(grade)
               + "&subject=" + quote(subject) + "&lesson=" + quote(lesson)
               + "&language=" + quote(language) + "&trace=" + quote(trace))
        return {"found": True, "title": item["lesson"], "url": url, "trace": trace,
                "source": "google_drive", "bytes": len(html_bytes)}
    except HTTPException as exc:
        log.warning("DRIVE_LESSON_LOOKUP_RESULT trace=%s status=%d reason=%s elapsed_ms=%d",
                    trace, exc.status_code, exc.detail, round((monotonic()-started)*1000))
        raise HTTPException(exc.status_code, detail={"trace": trace, "stage": "match",
                                                    "reason": str(exc.detail)})
    except Exception as exc:
        log.exception("DRIVE_LESSON_LOOKUP_FAILED trace=%s stage=connect_list_or_read error_type=%s elapsed_ms=%d",
                      trace, type(exc).__name__, round((monotonic()-started)*1000))
        raise HTTPException(503, detail={"trace": trace, "stage": "connect_list_or_read",
                                         "reason": type(exc).__name__})


@router.get("/view", response_class=HTMLResponse)
def view(grade: str, subject: str, lesson: str, language: str = "", trace: str = ""):
    trace = re.sub(r"[^a-zA-Z0-9]", "", trace)[:24] or uuid.uuid4().hex[:12]
    log.info("DRIVE_LESSON_VIEW_START trace=%s lesson=%r", trace, lesson)
    try:
        item = _resolve(grade, subject, lesson, language)
        html = _download(_service(), item["drive_file_id"]).decode("utf-8-sig")
        if "<html" not in html.lower():
            raise ValueError("NOT_AN_HTML_LESSON")
        log.info("DRIVE_LESSON_VIEW_OK trace=%s file=%s bytes=%d", trace, item["drive_file_id"], len(html.encode("utf-8")))
        return HTMLResponse(html, headers={
            "Cache-Control": "private, no-store",
            "Content-Security-Policy": "default-src 'self' data: blob: https:; script-src 'unsafe-inline' 'self' https:; style-src 'unsafe-inline' 'self' https:; frame-ancestors 'self'",
        })
    except HTTPException as exc:
        log.warning("DRIVE_LESSON_VIEW_FAILED trace=%s status=%d", trace, exc.status_code)
        raise
    except Exception as exc:
        log.exception("DRIVE_LESSON_VIEW_FAILED trace=%s error_type=%s", trace, type(exc).__name__)
        raise HTTPException(503, detail={"trace": trace, "stage": "view", "reason": type(exc).__name__}) from exc
