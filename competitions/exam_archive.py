from __future__ import annotations

"""Free, diskless index of the public CRDP mathematics-exam archive.

CRDP remains the source of truth. PDFs are fetched into memory for extraction or
download-on-demand; no PDF, OCR output, or index is written to Render's ephemeral
filesystem. The catalogue is intentionally rebuilt after a process restart.
"""
import hashlib
import io
import re
import shutil
import threading
import time
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

ARCHIVE_URL = "https://www.crdp.org/official-exams-corrections-lebanon"
ALLOWED_HOSTS = {"www.crdp.org", "crdp.org"}
REQUEST_TIMEOUT = (12, 45)
HEADERS = {"User-Agent": "NABIL-AI-Educational-Archive/2.0 (public CRDP exam catalogue)"}
_records: dict[str, dict] = {}
_texts: dict[str, str] = {}
_text_bytes = 0
MAX_TEXT_CACHE_BYTES = 32 * 1024 * 1024
MAX_TEXT_PER_DOCUMENT = 24000
_state: dict = {"status": "not_synced", "note": "The in-memory catalogue is empty. Run a CRDP sync."}
_lock = threading.RLock()
_job_lock = threading.Lock()
_job_running = False
_last_sync_started = 0.0
SYNC_COOLDOWN_SECONDS = 6 * 60 * 60


def _safe_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme == "https" and parsed.hostname in ALLOWED_HOSTS


def _normalise(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def _classify(title: str) -> dict:
    value = title.lower()
    if any(x in value for x in ("الشهادة المتوسطة", "brevet", "intermediate certificate")):
        grade = "Brevet"
    elif any(x in value for x in ("علوم عامة", "sciences générales", "sciences generales", "general sciences")):
        grade = "Terminale GS"
    elif any(x in value for x in ("علوم الحياة", "sciences de la vie", "life sciences")):
        grade = "Terminale LS"
    elif any(x in value for x in ("اجتماع واقتصاد", "اجتماع و اقتصاد", "sociologie et économie", "sociologie et economie", "economics")):
        grade = "Terminale SE"
    elif any(x in value for x in ("آداب", "اداب", "humanités", "humanites", "humanities", "literature")):
        grade = "Terminale LH"
    else:
        grade = "Secondary certificate / branch unspecified"
    subject = "Mathematics" if re.search(r"رياضيات|math[ée]matiques|mathematics|\bmath\b", value, re.I) else "Other"
    year_match = re.search(r"(?:19|20)\d{2}", title)
    year = int(year_match.group(0)) if year_match else None
    if "استثنائية" in value or "exceptionnelle" in value or "exceptional" in value:
        session = "Exceptional"
    elif re.search(r"دورة\s*2|session\s*2|2e\s*session|\bsecond\b", value) or "الثانية" in value:
        session = "Session 2"
    elif re.search(r"دورة\s*1|session\s*1|1re\s*session|\bfirst\b", value) or "الأولى" in value or "الاولى" in value:
        session = "Session 1"
    elif "العادية" in value or "normal" in value or "regular" in value:
        session = "Regular"
    else:
        session = "Unspecified"
    language = ("French" if any(x in value for x in ("فرنسي", "فرنسية", "français", "francais", "french"))
                else "English" if any(x in value for x in ("انكليزي", "إنكليزي", "انجليزية", "إنجليزية", "anglais", "english"))
                else "Arabic" if any(x in value for x in ("عربي", "العربية", "arabic"))
                else "Arabic / unspecified")
    return {"grade": grade, "subject": subject, "year": year, "session": session, "language": language}


def _extract_pdf_text(content: bytes) -> tuple[str, int, str]:
    try:
        import fitz
        doc = fitz.open(stream=content, filetype="pdf")
        pages = [page.get_text("text") for page in doc]
        extracted = "\n".join(pages).strip()
        page_count = len(doc)
        status = "extracted" if len(extracted) >= 80 else "needs_ocr"
        if status == "needs_ocr" and shutil.which("tesseract"):
            try:
                import pytesseract
                from PIL import Image
                ocr_pages = []
                for page_number in range(min(page_count, 30)):
                    pix = doc.load_page(page_number).get_pixmap(matrix=fitz.Matrix(1.6, 1.6), alpha=False)
                    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    ocr_pages.append(pytesseract.image_to_string(image, lang="ara+eng+fra"))
                ocr_text = "\n".join(ocr_pages).strip()
                if len(ocr_text) > len(extracted):
                    extracted = ocr_text
                    status = "extracted_ocr" if len(extracted) >= 80 else "needs_ocr"
            except Exception:
                pass
        doc.close()
        return extracted, page_count, status
    except Exception:
        return "", 0, "downloaded_text_unavailable"


def get_status() -> dict:
    with _lock:
        records = list(_records.values())
        by_grade: dict[str, int] = {}
        for item in records:
            grade = item.get("grade", "Unclassified")
            by_grade[grade] = by_grade.get(grade, 0) + 1
        state = dict(_state)
        return {
            "source": ARCHIVE_URL,
            "storage_mode": "memory_only_no_paid_storage",
            "documents": len(records),
            "mathematics_documents": sum(x.get("subject") == "Mathematics" for x in records),
            "text_searchable": sum(x.get("text_status") in ("extracted", "extracted_ocr") for x in records),
            "needs_ocr": sum(x.get("text_status") == "needs_ocr" for x in records),
            "ocr_available": bool(shutil.which("tesseract")),
            "by_grade": by_grade,
            "job_running": _job_running,
            "last_sync": state.get("finished_at"),
            "last_state": state,
            "storage_dir": None,
            "persistent_archive": False,
            "note": "CRDP is the source of truth. PDFs and extracted text are processed in memory only; the catalogue must be rebuilt after a service restart. Original files remain available at their official CRDP URLs."
        }


def _anchor_exam_title(anchor) -> tuple[str, bool]:
    """Read exam title from the containing CRDP table row; links often say only PDF."""
    row = anchor.find_parent(["tr", "li", "article", "div"])
    row_text = _normalise(row.get_text(" ", strip=True)) if row else ""
    anchor_text = _normalise(anchor.get_text(" ", strip=True))
    anchor_title = _normalise(anchor.get("title", ""))
    title = row_text or anchor_title or anchor_text
    is_math = bool(re.search(
        r"رياضيات|الرياضيات|math[ée]matiques|mathematics|\bmath\b",
        title + " " + anchor_title + " " + anchor_text, re.I))
    if title.lower() in {"pdf", "download", "تحميل"}:
        title = anchor_title or "CRDP PDF"
    return title, is_math


def sync_archive(max_pages: int = 300, mathematics_only: bool = True) -> dict:
    """Scan CRDP archive pages; fetch PDFs transiently and retain only metadata/text in RAM."""
    global _state, _text_bytes
    if max_pages < 1 or max_pages > 400:
        raise ValueError("max_pages must be between 1 and 400.")
    session = requests.Session()
    session.headers.update(HEADERS)
    discovered: dict[str, str] = {}
    pages_ok = page_failures = 0
    reached_end = False
    for page_no in range(max_pages):
        page_url = ARCHIVE_URL if page_no == 0 else f"{ARCHIVE_URL}?page={page_no}"
        try:
            response = session.get(page_url, timeout=REQUEST_TIMEOUT)
            if response.status_code == 404:
                reached_end = True
                break
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            pages_ok += 1
            for anchor in soup.find_all("a", href=True):
                url = urljoin(page_url, anchor["href"])
                if not _safe_url(url):
                    continue
                path = urlparse(url).path.lower()
                title, is_math = _anchor_exam_title(anchor)
                if not path.endswith(".pdf"):
                    continue
                if mathematics_only and not is_math:
                    continue
                discovered[url] = title or urlparse(url).path.rsplit("/", 1)[-1]
        except requests.RequestException:
            page_failures += 1

    added = updated = failed = 0
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    for url, title in discovered.items():
        try:
            response = session.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            if not response.content.startswith(b"%PDF"):
                raise ValueError("CRDP link did not return a valid PDF.")
            digest = hashlib.sha256(response.content).hexdigest()
            extracted, page_count, text_status = _extract_pdf_text(response.content)
            metadata = {
                "id": digest, "title": title, "source_url": url,
                "source_page": ARCHIVE_URL, "sha256": digest,
                "bytes": len(response.content), "pages": page_count,
                "text_status": text_status,
                "correction_in_same_pdf": bool(re.search(
                    r"corrig[eé]|bar[eè]me|éléments? de réponse|elements? de reponse|أسس التصحيح|التصحيح|حلول|إجابات|اجابات",
                    title + " " + extracted, re.I)),
                **_classify(title), "indexed_at": now
            }
            with _lock:
                if digest in _records:
                    updated += 1
                else:
                    added += 1
                _records[digest] = metadata
                if extracted:
                    compact_text = extracted[:MAX_TEXT_PER_DOCUMENT]
                    if digest in _texts:
                        _text_bytes -= len(_texts.pop(digest).encode("utf-8"))
                    compact_size = len(compact_text.encode("utf-8"))
                    if _text_bytes + compact_size <= MAX_TEXT_CACHE_BYTES:
                        _texts[digest] = compact_text
                        _text_bytes += compact_size
                    else:
                        metadata["text_status"] = "extracted_not_cached_memory_limit"
                        _records[digest] = metadata
        except Exception:
            failed += 1

    result = {
        "status": "completed" if page_failures == 0 else "completed_with_page_errors",
        "finished_at": now, "pages_checked": pages_ok, "pages_failed": page_failures,
        "archive_scan_complete": page_failures == 0 and (reached_end or pages_ok == max_pages),
        "pdfs_discovered": len(discovered), "added": added, "updated": updated,
        "failed": failed, "mathematics_only": mathematics_only,
        "storage_mode": "memory_only_no_paid_storage",
        "note": "PDFs were processed transiently and were not saved to disk. Data in this catalogue is lost on process restart; run sync again."
    }
    with _lock:
        _state = dict(result)
    return result


def start_sync(max_pages: int = 300) -> dict:
    global _job_running, _state, _last_sync_started
    with _job_lock:
        if _job_running:
            return {"started": False, "reason": "A sync job is already running."}
        remaining = SYNC_COOLDOWN_SECONDS - (time.time() - _last_sync_started)
        if remaining > 0:
            return {"started": False, "reason": "A public archive scan was already started recently.",
                    "cooldown_seconds_remaining": int(remaining)}
        _last_sync_started = time.time()
        _job_running = True

    def worker():
        global _job_running, _state
        try:
            with _lock:
                _state = {"status": "running", "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
            sync_archive(max_pages=max_pages, mathematics_only=True)
        except Exception as exc:
            with _lock:
                _state = {"status": "failed", "error": str(exc)[:500]}
        finally:
            with _job_lock:
                _job_running = False

    threading.Thread(target=worker, name="nabil-crdp-memory-index", daemon=True).start()
    return {"started": True, "message": "CRDP catalogue scan started. Files are processed in memory; no paid disk is used."}


def list_archive(grade: str | None = None, year: int | None = None,
                 session_name: str | None = None, limit: int = 20,
                 offset: int = 0) -> dict:
    """Return a paginated public catalogue of indexed mathematics PDFs."""
    with _lock:
        records = [dict(x) for x in _records.values() if x.get("subject") == "Mathematics"]
    if grade:
        records = [x for x in records if grade.lower() in x.get("grade", "").lower()]
    if year:
        records = [x for x in records if x.get("year") == year]
    if session_name:
        records = [x for x in records if session_name.lower() in x.get("session", "").lower()]
    records.sort(key=lambda x: (x.get("year") or 0, x.get("title", "")), reverse=True)
    total = len(records)
    start = max(0, offset)
    page = records[start:start + max(1, min(limit, 100))]
    for item in page:
        item["download_url"] = f"/api/competitions/archive/documents/{item['id']}"
    return {"total": total, "offset": start, "limit": max(1, min(limit, 100)), "results": page}


def search_archive(query: str, grade: str | None = None, limit: int = 8) -> list[dict]:
    terms = [x.lower() for x in re.findall(r"[\w\u0600-\u06ff]+", query) if len(x) > 1]
    if not terms:
        return []
    results = []
    with _lock:
        records = list(_records.values())
        texts = dict(_texts)
    for item in records:
        if item.get("subject") != "Mathematics":
            continue
        if grade and grade.lower() not in item.get("grade", "").lower():
            continue
        body = texts.get(item["id"], "")
        haystack = (item.get("title", "") + " " + body).lower()
        score = sum(haystack.count(term) for term in terms)
        if score:
            excerpt = ""
            for term in terms:
                pos = body.lower().find(term)
                if pos >= 0:
                    excerpt = body[max(0, pos - 350):pos + 1000]
                    break
            results.append({**item, "score": score, "excerpt": _normalise(excerpt)[:1400]})
    results.sort(key=lambda x: (x["score"], x.get("year") or 0), reverse=True)
    return results[:max(1, min(limit, 20))]


def get_document(document_id: str) -> tuple[bytes, dict] | None:
    """Fetch one indexed original PDF from its official CRDP URL on demand."""
    if not re.fullmatch(r"[a-f0-9]{64}", document_id or ""):
        return None
    with _lock:
        metadata = dict(_records.get(document_id, {}))
    if not metadata:
        return None
    response = requests.get(metadata["source_url"], headers=HEADERS, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    if not response.content.startswith(b"%PDF"):
        raise ValueError("The official CRDP source no longer returns the indexed PDF.")
    if hashlib.sha256(response.content).hexdigest() != document_id:
        raise ValueError("The CRDP PDF changed since indexing; run archive sync again.")
    return response.content, metadata
