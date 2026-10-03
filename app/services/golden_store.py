"""NABIL AI Golden lesson runtime store.

Zero-AI runtime contract:
lesson_id -> synchronized Golden catalogue/registry -> Drive artifact -> student.
No RAG, embeddings or LLM calls occur in this module.
"""
from __future__ import annotations

import hashlib
import html as html_lib
import io
import json
import os
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Optional
from urllib.request import Request, urlopen

from app.services.lesson_cache import normalize_lesson_id, normalize_language, normalize_package_version

GOLDEN_REGISTRY_PATH = Path(os.getenv("NABIL_GOLDEN_REGISTRY_PATH", "data/golden_lessons_registry.json"))
GOLDEN_LINKS_PATH = Path(os.getenv("NABIL_GOLDEN_LINKS_PATH", "data/golden_lesson_links.json"))


class _VisibleText(HTMLParser):
    BLOCKS = {"p","div","section","article","h1","h2","h3","h4","li","tr","br"}
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
    def handle_starttag(self, tag: str, attrs) -> None:
        if tag.lower() in self.BLOCKS:
            self.parts.append("\n")
    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in self.BLOCKS:
            self.parts.append("\n")
    def handle_data(self, data: str) -> None:
        if data and data.strip():
            self.parts.append(data.strip() + " ")
    def text(self) -> str:
        value = html_lib.unescape("".join(self.parts))
        value = re.sub(r"[ \t]+", " ", value)
        value = re.sub(r"\n\s*\n\s*\n+", "\n\n", value)
        return value.strip()


def html_to_student_text(value: str) -> str:
    parser = _VisibleText()
    parser.feed(value or "")
    return parser.text()


def _load_lessons(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise RuntimeError(f"GOLDEN_JSON_INVALID:{path}")
    lessons = raw.get("lessons")
    if lessons is None and all(isinstance(v, dict) for v in raw.values()):
        lessons = raw
    if not isinstance(lessons, dict):
        raise RuntimeError(f"GOLDEN_LESSONS_INVALID:{path}")
    return lessons


def _registry() -> dict[str, Any]:
    return {"lessons": _load_lessons(GOLDEN_REGISTRY_PATH)}


def _catalogue_entry(lesson_id: str) -> Optional[dict[str, Any]]:
    lid = normalize_lesson_id(lesson_id)
    item = _load_lessons(GOLDEN_LINKS_PATH).get(lid)
    if not isinstance(item, dict):
        return None
    if item.get("golden") is False or str(item.get("status") or "available") != "available":
        return None
    return dict(item)


def get_registry_entry(lesson_id: str) -> Optional[dict[str, Any]]:
    lid = normalize_lesson_id(lesson_id)
    base = _registry()["lessons"].get(lid)
    synced = _catalogue_entry(lid)
    if not isinstance(base, dict) and not isinstance(synced, dict):
        return None
    merged: dict[str, Any] = dict(base or {})
    if synced:
        merged.update({k: v for k, v in synced.items() if v not in (None, "")})
    merged.setdefault("lesson_id", lid)
    return merged


def list_registry_entries() -> list[dict[str, Any]]:
    ids = set(_registry()["lessons"].keys()) | set(_load_lessons(GOLDEN_LINKS_PATH).keys())
    out: list[dict[str, Any]] = []
    for lid in sorted(ids):
        row = get_registry_entry(lid)
        if row:
            out.append(row)
    return out


def _drive_service():
    from scripts.index_books import get_drive_service
    return get_drive_service()


def _discover_on_drive(service, lesson_id: str, language: str, version: str) -> Optional[dict[str, Any]]:
    lid = normalize_lesson_id(lesson_id)
    lang = normalize_language(language)
    ver = normalize_package_version(version)
    q = (
        "trashed = false and "
        f"appProperties has {{ key='nabil_lesson_id' and value='{lid}' }} and "
        "appProperties has { key='nabil_golden' and value='true' } and "
        "appProperties has { key='nabil_artifact' and value='theory' }"
    )
    rows = service.files().list(q=q, fields="files(id,name,mimeType,modifiedTime,webViewLink,appProperties)", pageSize=20).execute().get("files", [])
    candidates = []
    for row in rows:
        props = row.get("appProperties") or {}
        if normalize_language(props.get("nabil_language") or lang) == lang and normalize_package_version(props.get("nabil_version") or ver) == ver:
            candidates.append(row)
    if not candidates:
        return None
    candidates.sort(key=lambda r: str(r.get("modifiedTime") or ""), reverse=True)
    if len(candidates) > 1 and str(candidates[0].get("modifiedTime")) == str(candidates[1].get("modifiedTime")):
        raise RuntimeError(f"GOLDEN_DRIVE_DUPLICATE:{lid}:{lang}:{ver}")
    return candidates[0]


def _download_bytes(service, file_id: str, mime_type: str) -> bytes:
    from googleapiclient.http import MediaIoBaseDownload
    request = service.files().export_media(fileId=file_id, mimeType="text/html") if mime_type == "application/vnd.google-apps.document" else service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    dl = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = dl.next_chunk()
    return fh.getvalue()


def _anonymous_google_doc_export(file_id: str) -> bytes:
    if not re.fullmatch(r"[A-Za-z0-9_-]{10,200}", file_id or ""):
        raise ValueError("INVALID_GOLDEN_DRIVE_FILE_ID")
    url = f"https://docs.google.com/document/d/{file_id}/export?format=html"
    request = Request(url, headers={"User-Agent": "NABIL-AI-Golden/1.0"})
    with urlopen(request, timeout=20) as response:
        data = response.read(12_000_001)
    if not data or len(data) > 12_000_000:
        raise RuntimeError("GOLDEN_PUBLIC_EXPORT_INVALID_SIZE")
    return data


def _browser_drive_preview(file_id: str, title: str) -> str:
    """Fallback for private Docs the signed-in student's browser can read.

    Railway must not fail the lesson merely because its server/service account
    cannot export a private owner Doc.  The browser already carries the owner's
    Google session, so hand the document to Google Docs preview in an iframe.
    """
    if not re.fullmatch(r"[A-Za-z0-9_-]{10,200}", file_id or ""):
        raise ValueError("INVALID_GOLDEN_DRIVE_FILE_ID")
    safe_title = html_lib.escape(title or "NABIL Golden lesson")
    src = f"https://docs.google.com/document/d/{file_id}/preview"
    return (
        "<!doctype html><html><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<title>" + safe_title + "</title>"
        "<style>html,body{margin:0;width:100%;height:100%;background:#071d30;overflow:hidden}"
        "iframe{border:0;width:100%;height:100%;display:block;background:white}</style>"
        "</head><body><iframe src='" + src + "' title='" + safe_title + "' "
        "allow='clipboard-read; clipboard-write' referrerpolicy='no-referrer-when-downgrade'></iframe>"
        "</body></html>"
    )


def fetch_golden_from_drive(lesson_id: str, language: str = "en", version: str = "0.01") -> dict[str, Any]:
    lid = normalize_lesson_id(lesson_id)
    lang = normalize_language(language)
    ver = normalize_package_version(version)
    entry = get_registry_entry(lid) or {}
    file_id = str(entry.get("drive_file_id") or entry.get("drive_theory_id") or "").strip()
    metadata = None
    payload = None
    browser_preview = False

    if file_id:
        try:
            service = _drive_service()
            metadata = service.files().get(fileId=file_id, fields="id,name,mimeType,modifiedTime,webViewLink,appProperties").execute()
            props = metadata.get("appProperties") or {}
            if props.get("nabil_lesson_id") and normalize_lesson_id(props["nabil_lesson_id"]) != lid:
                raise RuntimeError("GOLDEN_DRIVE_IDENTITY_MISMATCH")
            payload = _download_bytes(service, file_id, str(metadata.get("mimeType") or ""))
        except Exception:
            try:
                payload = _anonymous_google_doc_export(file_id)
                metadata = {
                    "id": file_id,
                    "name": str(entry.get("title") or lid),
                    "mimeType": "application/vnd.google-apps.document",
                    "webViewLink": str(entry.get("drive_url") or f"https://docs.google.com/document/d/{file_id}/edit"),
                    "appProperties": {},
                }
            except Exception:
                # The two server-side readers are unauthorized. Do not return
                # another 503 loop: render Google's authenticated browser preview.
                preview = _browser_drive_preview(file_id, str(entry.get("title") or lid))
                payload = preview.encode("utf-8")
                metadata = {
                    "id": file_id,
                    "name": str(entry.get("title") or lid),
                    "mimeType": "text/html",
                    "webViewLink": str(entry.get("drive_url") or f"https://docs.google.com/document/d/{file_id}/edit"),
                    "appProperties": {},
                }
                browser_preview = True
    else:
        service = _drive_service()
        metadata = _discover_on_drive(service, lid, lang, ver)
        if metadata is None:
            raise FileNotFoundError(f"GOLDEN_LESSON_NOT_PUBLISHED:{lid}:{lang}:{ver}")
        file_id = str(metadata["id"])
        payload = _download_bytes(service, file_id, str(metadata.get("mimeType") or ""))

    assert payload is not None and metadata is not None
    text = payload.decode("utf-8", errors="replace").strip()
    if not text:
        raise RuntimeError("GOLDEN_DRIVE_ARTIFACT_EMPTY")
    mime = str(metadata.get("mimeType") or "")
    is_html = "html" in mime or "google-apps.document" in mime or text.lstrip().lower().startswith(("<!doctype html", "<html"))
    lesson_html = text if is_html else ""
    reply = html_to_student_text(text) if is_html else text
    if not reply and not browser_preview:
        raise RuntimeError("GOLDEN_STUDENT_TEXT_EMPTY")
    if browser_preview:
        reply = str(entry.get("title") or lid)
    sha = hashlib.sha256(payload).hexdigest()
    return {
        "lesson_id": lid,
        "language": normalize_language(entry.get("language") or lang),
        "version": normalize_package_version(entry.get("version") or ver),
        "title": str(entry.get("title") or metadata.get("name") or lid),
        "reply": reply,
        "lesson_html": lesson_html,
        "drive_file_id": file_id,
        "drive_url": metadata.get("webViewLink") or entry.get("drive_url") or f"https://drive.google.com/file/d/{file_id}/view",
        "sha256": sha,
        "browser_drive_preview": browser_preview,
        "sources": [{"type":"golden_drive_browser_preview" if browser_preview else "golden_drive","lesson_id":lid,"drive_file_id":file_id,"sha256":sha}],
    }
