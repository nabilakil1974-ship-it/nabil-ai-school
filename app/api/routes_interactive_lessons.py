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
from threading import Lock
from urllib.parse import quote

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from googleapiclient.http import MediaIoBaseDownload

router = APIRouter(prefix="/interactive-lessons", tags=["drive-interactive-lessons"])
log = logging.getLogger("nabil_ai.drive_lessons")
_CACHE = {"at": 0.0, "entries": []}
_CACHE_LOCK = Lock()
_CACHE_SECONDS = 10  # New owner-uploaded lessons become visible without redeployment.
_OWNER_ROOT = "16bcmZMO_dn4FqlGaDtl8Hky6iSBEqZpX"
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
    """Match Arabic and international grade labels without treating G10 as G1."""
    s = _norm(value)
    names = {
        1: ("الأول", "first", "premier"), 2: ("الثاني", "second", "deuxieme"),
        3: ("الثالث", "third", "troisieme"), 4: ("الرابع", "fourth", "quatrieme"),
        5: ("الخامس", "fifth", "cinquieme"), 6: ("السادس", "sixth", "sixieme"),
        7: ("السابع", "seventh", "septieme"), 8: ("الثامن", "eighth", "huitieme"),
        9: ("التاسع", "ninth", "neuvieme"), 10: ("العاشر", "tenth", "dixieme"),
        11: ("الحاديعشر", "eleventh", "onzieme"), 12: ("الثانيعشر", "twelfth", "douzieme"),
    }
    digits = re.search(r"(?:grade|class|eb|g|الصف)?0?([1-9]|1[0-2])(?:$|[^0-9])", s)
    if digits:
        return str(int(digits.group(1)))
    # Lebanese secondary labels identify their grade, while stream is checked
    # separately through catalog metadata when available.
    for number, labels in ((12, ("الثالثثانوي",)), (11, ("الثانيثانوي",)), (10, ("الأولثانوي",))):
        if any(label in s for label in labels):
            return str(number)
    for number, labels in names.items():
        if any(label in s for label in labels):
            return str(number)
    return s


_SUBJECT_ALIASES = {
    "physics": ("physics", "physique", "فيزياء", "الفيزياء"),
    "mathematics": ("mathematics", "math", "maths", "mathematiques", "رياضيات", "الرياضيات"),
    "chemistry": ("chemistry", "chimie", "كيمياء", "الكيمياء"),
    "biology": ("biology", "life science", "lifescience", "biologie", "علوم الحياة", "بيولوجي"),
    "general_science": ("general science", "science", "sciences", "علوم", "العلوم"),
}


def _subject(value):
    normalized = _norm(value)
    for key, aliases in _SUBJECT_ALIASES.items():
        if normalized in {_norm(alias) for alias in aliases}:
            return key
    return normalized


def _list_children(service, folder_id):
    """Page through a Drive folder; folders and HTML only."""
    token = None
    while True:
        result = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields="nextPageToken,files(id,name,mimeType)",
            pageSize=1000, pageToken=token,
        ).execute()
        yield from result.get("files", [])
        token = result.get("nextPageToken")
        if not token:
            break


def _entry(file, grade="", subject=""):
    stem = file["name"].rsplit(".", 1)[0]
    parts = stem.split("--", 1)
    if len(parts) == 2:
        prefix, title = parts
        match = re.match(r"(?:EB|G)0?(\d{1,2})[-_ ]+(.+)", prefix, re.I)
        if match:
            grade = match.group(1)
            subject = match.group(2)
    else:
        match = re.match(r"(?:EB|G)[-_ ]?0?(\d{1,2})[-_ ]+(.*)", stem, re.I)
        title = match.group(2) if match else stem
        grade = match.group(1) if match else grade
    title = re.sub(r"[-_ ]+(?:BILINGUAL|FRANCAIS|ENGLISH)$", "", title, flags=re.I)
    aliases = []
    # The CRDP selector and the authored HTML name the same G07 chapter differently.
    if _grade(grade) == "7" and _subject(subject) == "physics" and _norm(title) == _norm("Solids and Liquids"):
        aliases = ["Solid and liquid states", "Solids and liquids",
                   "Les états solide et liquide", "Solides et liquides"]
    return {"grade": grade, "subject": subject, "lesson": title.replace("-", " "),
            "aliases": aliases, "drive_file_id": file["id"],
            "filename": file["name"], "language": ""}


def _owner_entries(service):
    """Discover HTML immediately from owner ROOT / Grade [/ Subject].

    Supports HTML directly in Grade 7 (the owner's current layout), as well
    as future Physics/Math/etc subfolders. Filenames G07-PHYSICS--TITLE.html
    carry their own grade and subject; nested files may inherit the folder.
    """
    root = os.getenv("NABIL_INTERACTIVE_CURRICULUM_ROOT_ID", _OWNER_ROOT).strip()
    entries = []
    for grade_folder in _list_children(service, root):
        if grade_folder.get("mimeType") != "application/vnd.google-apps.folder":
            continue
        match = re.search(r"(?:grade|صف)\s*0?(\d{1,2})", grade_folder["name"], re.I)
        if not match:
            continue  # e.g. 00 - Curriculum Index
        grade = match.group(1)
        for child in _list_children(service, grade_folder["id"]):
            if child["name"].lower().endswith(".html"):
                entries.append(_entry(child, grade))
            elif child.get("mimeType") == "application/vnd.google-apps.folder":
                subject = child["name"].split("-", 1)[0].strip()
                for file in _list_children(service, child["id"]):
                    if file["name"].lower().endswith(".html"):
                        entries.append(_entry(file, grade, subject))
    return entries


def _entries():
    now = monotonic()
    if now - _CACHE["at"] < _CACHE_SECONDS:
        return _CACHE["entries"]
    with _CACHE_LOCK:
        if monotonic() - _CACHE["at"] < _CACHE_SECONDS:
            return _CACHE["entries"]
        service = _service()
        items = []
        catalog_id = os.getenv("NABIL_INTERACTIVE_LESSONS_CATALOG_FILE_ID", "").strip()
        if catalog_id:
            payload = json.loads(_download(service, catalog_id).decode("utf-8-sig"))
            items = payload.get("lessons", [])
            if not isinstance(items, list):
                raise ValueError("INVALID_LESSON_CATALOG")
        else:
            legacy = os.getenv("NABIL_INTERACTIVE_LESSONS_FOLDER_ID", _DEFAULT_FOLDER).strip()
            # Keep legacy lessons while the owner migrates to the grade/subject tree.
            for file in _list_children(service, legacy):
                if file["name"].lower().endswith(".html"):
                    items.append(_entry(file))
        try:
            owner = _owner_entries(service)
        except Exception as exc:
            # The service account needs viewer access to the owner root and its
            # descendants. Do not silently claim live owner-folder sync works.
            log.warning("OWNER_CURRICULUM_ROOT_UNAVAILABLE root=%s error=%s",
                        os.getenv("NABIL_INTERACTIVE_CURRICULUM_ROOT_ID", _OWNER_ROOT),
                        type(exc).__name__)
            owner = []
        # Owner-visible grade/subject files win over older flat-folder duplicates.
        keyed = {(_grade(x.get("grade")), _subject(x.get("subject")),
                  _norm(x.get("lesson"))): x for x in items
                 if isinstance(x, dict) and x.get("drive_file_id") and x.get("lesson")}
        for item in owner:
            keyed[(_grade(item["grade"]), _subject(item["subject"]),
                   _norm(item["lesson"]))] = item
        # Keep known legacy bilingual reference available by its actual title.
        # New lessons require NO code edit or hard-coded file ID.
        entries = list(keyed.values())
        log.info("DRIVE_LESSON_DISCOVERY entries=%d owner_entries=%d",
                 len(entries), len(owner))
        _CACHE.update(at=monotonic(), entries=entries)
        return entries


def _resolve(grade, subject, lesson, language):
    matches = []
    for item in _entries():
        if item.get("grade") and _grade(item["grade"]) != _grade(grade):
            continue
        if item.get("subject") and _subject(item["subject"]) != _subject(subject):
            continue
        titles = [item["lesson"]] + list(item.get("aliases") or [])
        if _norm(lesson) not in {_norm(title) for title in titles}:
            continue
        if language and item.get("language") and not item.get("bilingual") and _norm(language) != _norm(item["language"]):
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
            if item.get("subject") and _subject(item["subject"]) != _subject(subject):
                continue
            if _norm(lesson) not in {_norm(x) for x in [item["lesson"]] + list(item.get("aliases") or [])}:
                continue
            if language and item.get("language") and not item.get("bilingual") and _norm(language) != _norm(item["language"]):
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

@router.get("/available")
def available(grade: str, subject: str):
    """Live prepared lessons for the selected grade/subject; never invent titles."""
    try:
        entries = [item for item in _entries()
                   if _grade(item.get("grade")) == _grade(grade)
                   and _subject(item.get("subject")) == _subject(subject)]
        seen = set()
        lessons = []
        for item in entries:
            key = _norm(item["lesson"])
            if key not in seen:
                seen.add(key)
                lessons.append({"title": item["lesson"], "aliases": item.get("aliases", []), "filename": item.get("filename", "")})
        return {"grade": grade, "subject": subject, "lessons": lessons,
                "source": "google_drive", "count": len(lessons)}
    except Exception as exc:
        log.exception("DRIVE_AVAILABLE_FAILED")
        raise HTTPException(503, detail={"reason": type(exc).__name__})


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
def view(grade: str, subject: str, lesson: str, language: str = "", trace: str = "", exercise: int | None = None, page: int | None = None, worksheet: int | None = None):
    trace = re.sub(r"[^a-zA-Z0-9]", "", trace)[:24] or uuid.uuid4().hex[:12]
    log.info("DRIVE_LESSON_VIEW_START trace=%s lesson=%r", trace, lesson)
    try:
        item = _resolve(grade, subject, lesson, language)
        html = _download(_service(), item["drive_file_id"]).decode("utf-8-sig")
        if "<html" not in html.lower():
            raise ValueError("NOT_AN_HTML_LESSON")
        # The same bilingual HTML opens in the selected textbook's language.
        # Do not rewrite or duplicate its source content on Drive.
        if _norm(language) in {_norm("Français"), _norm("French"), _norm("fr")}:
            html = re.sub(r"<body(\s[^>]*)?>", lambda m: m.group(0).replace("<body", '<body class="frmode"') if "class=" not in m.group(0) else re.sub(r'class="([^"]*)"', lambda c: 'class="' + c.group(1) + ' frmode"', m.group(0), count=1), html, count=1, flags=re.I)
        elif _norm(language) in {_norm("English"), _norm("Anglais"), _norm("en")}:
            html = re.sub(r'<body([^>]*)class="([^"]*)"', lambda m: '<body' + m.group(1) + 'class="' + re.sub(r"\bfrmode\b", "", m.group(2)).strip() + '"', html, count=1, flags=re.I)
        # Color-code full concepts and textbook exercises while keeping their figures and solutions together.
        if "</head>" in html.lower():
            html = re.sub(r"</head>", '<link rel="stylesheet" href="/static/nabil_lesson_color_cards_v1.css?v=1"></head>', html, count=1, flags=re.I)
        # Optional precise focus; the lesson HTML remains the verified Drive original.
        if exercise is not None or page is not None or worksheet is not None:
            if sum(x is not None for x in (exercise, page, worksheet)) > 1:
                raise HTTPException(400, "Specify exercise OR printed book page, not both.")
            if exercise is not None and not 1 <= exercise <= 999:
                raise HTTPException(400, "Invalid exercise number.")
            if page is not None and not 1 <= page <= 9999:
                raise HTTPException(400, "Invalid printed page.")
            if worksheet is not None and worksheet != 1:
                raise HTTPException(400, "Invalid worksheet selection.")
            if "</body>" in html.lower():
                html = re.sub(r"</body>", '<script src="/static/nabil_lesson_focus_v1.js?v=1"></script></body>', html, count=1, flags=re.I)
        # Keep the bilingual toggle visible while students scroll to exercises.
        if 'id="lesson-language"' in html and "</body>" in html.lower():
            html = re.sub(r"</body>", '<script src="/static/nabil_lesson_sticky_language_v1.js?v=1"></script><script src="/static/nabil_lesson_teacher_audio_v1.js?v=5"></script></body>', html, count=1, flags=re.I)
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
