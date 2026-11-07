from __future__ import annotations

"""Official Lebanese certificate-exam archive: crawl, download, extract and search.

Only the CRDP official-exams archive is crawled. PDFs are retained as originals;
extracted text is an index aid, never a replacement for the source document.
"""
import hashlib
import json
import os
import re
import threading
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

ARCHIVE_URL = "https://www.crdp.org/official-exams-corrections-lebanon"
ALLOWED_HOSTS = {"www.crdp.org", "crdp.org"}
ARCHIVE_DIR = Path(os.getenv("NABIL_EXAM_ARCHIVE_DIR", "data/exam_archive"))
INDEX_FILE = ARCHIVE_DIR / "index.jsonl"
STATE_FILE = ARCHIVE_DIR / "sync-state.json"
REQUEST_TIMEOUT = (12, 45)
_lock = threading.Lock()
_job_lock = threading.Lock()
_job_running = False


def _safe_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme == "https" and parsed.hostname in ALLOWED_HOSTS


def _normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def _classify(title: str) -> dict:
    value = title.lower()
    if any(x in value for x in ("الشهادة المتوسطة", "brevet", "intermediate certificate")):
        grade = "Brevet"
    elif any(x in value for x in ("علوم عامة", "sciences générales", "general sciences")):
        grade = "Terminale GS"
    elif any(x in value for x in ("علوم الحياة", "sciences de la vie", "life sciences")):
        grade = "Terminale LS"
    elif any(x in value for x in ("اجتماع واقتصاد", "اجتماع و اقتصاد", "sociologie et économie", "economics")):
        grade = "Terminale SE"
    elif any(x in value for x in ("آداب", "اداب", "humanités", "humanities", "literature")):
        grade = "Terminale LH"
    else:
        grade = "Secondary certificate / branch unspecified"
    if any(x in value for x in ("رياضيات", "mathématiques", "mathematiques", "mathematics", "math")):
        subject = "Mathematics"
    else:
        subject = "Other"
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
    language = "French" if any(x in value for x in ("فرنسي", "فرنسية", "français", "francais", "french")) else ("English" if any(x in value for x in ("انكليزي", "إنكليزي", "انجليزية", "إنجليزية", "anglais", "english")) else ("Arabic" if any(x in value for x in ("عربي", "العربية", "arabic")) else "Arabic / unspecified"))
    return {"grade": grade, "subject": subject, "year": year, "session": session, "language": language}


def _extract_pdf_text(path: Path) -> tuple[str, int]:
    try:
        import fitz
        doc = fitz.open(path)
        pages = []
        for page in doc:
            pages.append(page.get_text("text"))
        extracted = "\n".join(pages).strip()
        if len(extracted) >= 80:
            return extracted, len(doc)
        # Scanned/image-only exam papers: attempt local OCR in Arabic, English and French.
        try:
            import pytesseract
            from PIL import Image
            ocr_pages = []
            for page_number in range(min(len(doc), 40)):
                page = doc.load_page(page_number)
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
                image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                ocr_pages.append(pytesseract.image_to_string(image, lang="ara+eng+fra"))
            ocr_text = "\n".join(ocr_pages).strip()
            if len(ocr_text) > len(extracted):
                extracted = ocr_text
        except Exception:
            pass
        return extracted, len(doc)
    except Exception:
        return "", 0


def _write_state(state: dict) -> None:
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(STATE_FILE)


def get_status() -> dict:
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    records = []
    if INDEX_FILE.exists():
        for line in INDEX_FILE.read_text(encoding="utf-8").splitlines():
            try:
                records.append(json.loads(line))
            except Exception:
                continue
    by_grade = {}
    for item in records:
        grade = item.get("grade", "Unclassified")
        by_grade[grade] = by_grade.get(grade, 0) + 1
    state = {}
    if STATE_FILE.exists():
        try:
            state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            state = {}
    return {
        "source": ARCHIVE_URL,
        "documents": len(records),
        "mathematics_documents": sum(1 for x in records if x.get("subject") == "Mathematics"),
        "text_searchable": sum(1 for x in records if x.get("text_status") == "extracted"),
        "needs_ocr": sum(1 for x in records if x.get("text_status") == "needs_ocr"),
        "by_grade": by_grade,
        "job_running": _job_running,
        "last_sync": state.get("finished_at"),
        "last_state": state,
        "storage_dir": str(ARCHIVE_DIR),
        "note": "Original official PDFs are retained. Scanned files without a text layer are flagged for OCR; no missing correction is fabricated."
    }


def sync_archive(max_pages: int = 300, mathematics_only: bool = True) -> dict:
    """Crawl CRDP paginated index and download eligible original PDFs."""
    if max_pages < 1 or max_pages > 400:
        raise ValueError("max_pages must be between 1 and 400.")
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers.update({"User-Agent": "NABIL-AI-Educational-Archive/1.0 (official public exam archive indexer)"})
    known = set()
    if INDEX_FILE.exists():
        for line in INDEX_FILE.read_text(encoding="utf-8").splitlines():
            try:
                known.add(json.loads(line).get("source_url"))
            except Exception:
                pass
    discovered = {}
    pages_ok = 0
    page_failures = 0
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
            found_on_page = 0
            for anchor in soup.find_all("a", href=True):
                title = _normalise(anchor.get_text(" ", strip=True))
                url = urljoin(page_url, anchor["href"])
                if not title or not _safe_url(url) or not url.lower().split("?")[0].endswith(".pdf"):
                    continue
                if mathematics_only and not re.search(r"رياضيات|math[ée]matiques|mathematics|\bmath\b", title, re.I):
                    continue
                discovered[url] = title
                found_on_page += 1
            # Scan every requested page: older mathematics papers may be separated by long runs of other subjects.
        except requests.RequestException:
            page_failures += 1
            continue

    added, skipped, failed = 0, 0, 0
    with INDEX_FILE.open("a", encoding="utf-8") as index:
        for url, title in discovered.items():
            if url in known:
                skipped += 1
                continue
            try:
                response = session.get(url, timeout=REQUEST_TIMEOUT)
                response.raise_for_status()
                if "pdf" not in response.headers.get("Content-Type", "").lower() and not response.content.startswith(b"%PDF"):
                    raise ValueError("The CRDP link did not return a PDF.")
                if not response.content.startswith(b"%PDF"):
                    raise ValueError("Invalid PDF signature.")
                digest = hashlib.sha256(response.content).hexdigest()
                pdf_path = ARCHIVE_DIR / f"{digest}.pdf"
                if not pdf_path.exists():
                    pdf_path.write_bytes(response.content)
                extracted, page_count = _extract_pdf_text(pdf_path)
                text_status = "extracted" if len(extracted) >= 80 else "needs_ocr"
                text_path = ARCHIVE_DIR / f"{digest}.txt"
                if extracted:
                    text_path.write_text(extracted, encoding="utf-8")
                record = {
                    "id": digest,
                    "title": title,
                    "source_url": url,
                    "source_page": ARCHIVE_URL,
                    "local_pdf": str(pdf_path),
                    "local_text": str(text_path) if extracted else None,
                    "sha256": digest,
                    "bytes": len(response.content),
                    "pages": page_count,
                    "text_status": text_status,
                    "correction_in_same_pdf": bool(re.search(r"corrig[eé]|bar[eè]me|éléments? de réponse|elements? de reponse|أسس التصحيح|التصحيح", title + " " + extracted, re.I)),
                    **_classify(title),
                    "downloaded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                }
                index.write(json.dumps(record, ensure_ascii=False) + "\n")
                index.flush()
                known.add(url)
                added += 1
            except Exception:
                failed += 1
    result = {
        "finished_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "pages_checked": pages_ok,
        "pages_failed": page_failures,
        "archive_scan_complete": page_failures == 0 and (reached_end or pages_ok == max_pages),
        "pdfs_discovered": len(discovered),
        "added": added,
        "already_indexed": skipped,
        "failed": failed,
        "mathematics_only": mathematics_only
    }
    _write_state(result)
    return result


def start_sync(max_pages: int = 300) -> dict:
    global _job_running
    with _job_lock:
        if _job_running:
            return {"started": False, "reason": "A sync job is already running."}
        _job_running = True

    def worker():
        global _job_running
        try:
            _write_state({"started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "status": "running"})
            sync_archive(max_pages=max_pages, mathematics_only=True)
        except Exception as exc:
            _write_state({"status": "failed", "error": str(exc)[:500]})
        finally:
            with _job_lock:
                _job_running = False

    threading.Thread(target=worker, name="nabil-official-exam-archive", daemon=True).start()
    return {"started": True, "message": "Official mathematics exam archive sync started in the background."}


def search_archive(query: str, grade: str | None = None, limit: int = 8) -> list[dict]:
    """Simple transparent local full-text retrieval over indexed official PDFs."""
    query_terms = [x.lower() for x in re.findall(r"[\w\u0600-\u06ff]+", query) if len(x) > 1]
    if not query_terms or not INDEX_FILE.exists():
        return []
    results = []
    for line in INDEX_FILE.read_text(encoding="utf-8").splitlines():
        try:
            item = json.loads(line)
        except Exception:
            continue
        if item.get("subject") != "Mathematics":
            continue
        if grade and grade.lower() not in item.get("grade", "").lower():
            continue
        text_content = ""
        text_path = item.get("local_text")
        if text_path and Path(text_path).exists():
            text_content = Path(text_path).read_text(encoding="utf-8", errors="ignore")
        haystack = (item.get("title", "") + " " + text_content).lower()
        score = sum(haystack.count(term) for term in query_terms)
        if score:
            excerpt = ""
            for term in query_terms:
                pos = text_content.lower().find(term)
                if pos >= 0:
                    excerpt = text_content[max(0, pos - 350):pos + 1000].replace("\\n", " ")
                    break
            results.append({**item, "score": score, "excerpt": _normalise(excerpt)[:1400]})
    results.sort(key=lambda x: (x["score"], x.get("year") or 0), reverse=True)
    return results[:max(1, min(limit, 20))]


def get_document_path(document_id: str) -> tuple[Path, dict] | None:
    """Resolve a previously indexed PDF by its SHA-256 identifier."""
    if not re.fullmatch(r"[a-f0-9]{64}", document_id or "") or not INDEX_FILE.exists():
        return None
    for line in INDEX_FILE.read_text(encoding="utf-8").splitlines():
        try:
            item = json.loads(line)
        except Exception:
            continue
        if item.get("id") != document_id:
            continue
        candidate = Path(item.get("local_pdf", "")).resolve()
        root = ARCHIVE_DIR.resolve()
        if root not in candidate.parents or not candidate.is_file():
            return None
        return candidate, item
    return None
