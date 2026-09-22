"""Serve prepared interactive HTML lessons from Google Drive, never from app/static.

Configure NABIL_INTERACTIVE_LESSONS_FOLDER_ID (shared with the backend service
account) or NABIL_INTERACTIVE_LESSONS_CATALOG_FILE_ID for an explicit JSON catalog.
The catalog is stored on Drive, NOT in the repository:
{"lessons":[{"grade":"الصف التاسع","subject":"فيزياء","lesson":"Conducteurs ohmiques",
"language":"Français","drive_file_id":"...","aliases":["Ohmic conductors"]}]}
"""
import io
import json
import os
import re
import unicodedata
from functools import lru_cache
from time import monotonic

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from googleapiclient.http import MediaIoBaseDownload

router = APIRouter(prefix="/interactive-lessons", tags=["drive-interactive-lessons"])
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
        return _CACHE["entries"]
    service = _service()
    catalog_id = os.getenv("NABIL_INTERACTIVE_LESSONS_CATALOG_FILE_ID", "").strip()
    if catalog_id:
        payload = json.loads(_download(service, catalog_id).decode("utf-8-sig"))
        items = payload.get("lessons", [])
        if not isinstance(items, list):
            raise ValueError("INVALID_LESSON_CATALOG")
    else:
        folder = os.getenv("NABIL_INTERACTIVE_LESSONS_FOLDER_ID", _DEFAULT_FOLDER).strip()
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
                    items.append({"grade": grade, "subject": subject,
                                  "lesson": title.replace("-", " "),
                                  "drive_file_id": file["id"], "language": ""})
            token = result.get("nextPageToken")
            if not token:
                break
    valid = [x for x in items if isinstance(x, dict) and x.get("drive_file_id") and x.get("lesson")]
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
    if len(matches) > 1:
        raise HTTPException(409, "Multiple prepared lessons match; specify the language and textbook.")
    if not matches:
        raise HTTPException(404, "No prepared interactive lesson in the configured Google Drive collection.")
    return matches[0]


@router.get("/resolve")
def resolve(grade: str, subject: str, lesson: str, language: str = ""):
    try:
        item = _resolve(grade, subject, lesson, language)
        return {"found": True, "title": item["lesson"],
                "url": "/api/interactive-lessons/view?grade=" + __import__("urllib.parse", fromlist=["quote"]).quote(grade)
                + "&subject=" + __import__("urllib.parse", fromlist=["quote"]).quote(subject)
                + "&lesson=" + __import__("urllib.parse", fromlist=["quote"]).quote(lesson)
                + "&language=" + __import__("urllib.parse", fromlist=["quote"]).quote(language)}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(503, "Google Drive lesson collection unavailable.") from exc


@router.get("/view", response_class=HTMLResponse)
def view(grade: str, subject: str, lesson: str, language: str = ""):
    try:
        item = _resolve(grade, subject, lesson, language)
        html = _download(_service(), item["drive_file_id"]).decode("utf-8-sig")
        if "<html" not in html.lower():
            raise ValueError("NOT_AN_HTML_LESSON")
        return HTMLResponse(html, headers={
            "Cache-Control": "private, no-store",
            "Content-Security-Policy": "default-src 'self' data: blob: https:; script-src 'unsafe-inline' 'self' https:; style-src 'unsafe-inline' 'self' https:; frame-ancestors 'self'",
        })
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(503, "Could not retrieve the prepared lesson from Google Drive.") from exc
