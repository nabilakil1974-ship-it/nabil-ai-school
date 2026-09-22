"""Index textbook PDFs from Google Drive into PostgreSQL/pgvector.

This indexer intentionally avoids importing PyMuPDF at runtime because Railway's
standalone Python loader can be isolated from the system libstdc++ runtime.
Direct PDF text extraction uses pypdf. Pages with little/no usable text fall
back to server-side OCR via Poppler (pdftoppm) + Tesseract.
"""

import argparse
import gc
import io
import json
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
from pypdf import PdfReader

from app.core.config import settings
from app.db.session import SessionLocal
from app.db.models import Book, BookChunk, BookPage
from app.services.rag_search import embed_text

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
MAX_CHUNK_CHARS = 1800
MIN_USABLE_TEXT_CHARS = 40


def get_drive_service():
    raw = (settings.GOOGLE_DRIVE_CREDENTIALS_JSON or "").strip()
    if raw:
        creds = service_account.Credentials.from_service_account_info(
            json.loads(raw), scopes=SCOPES
        )
    else:
        creds = service_account.Credentials.from_service_account_file(
            "drive_service_account.json", scopes=SCOPES
        )
    return build("drive", "v3", credentials=creds)


def list_pdfs_in_folder(service, folder_id: str):
    query = f"'{folder_id}' in parents and mimeType='application/pdf' and trashed=false"
    files, page_token = [], None
    while True:
        resp = service.files().list(
            q=query,
            fields="nextPageToken, files(id, name)",
            pageToken=page_token,
        ).execute()
        files.extend(resp.get("files", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return files


def download_pdf(service, file_id: str) -> bytes:
    # 2026-09-22: no timeout existed here at all - confirmed from a live
    # Railway log that the student-facing page-image endpoint consistently
    # 404'd on one specific book/page across 4 separate requests over
    # several minutes, while the AI-generation path's OWN fetch of the same
    # page (same _render_pdf_page function, wrapped there in an 8s
    # asyncio.wait_for) logged BOOK_PAGE_VISION_UNAVAILABLE reason=
    # TimeoutError for that exact request. Since _render_pdf_page is
    # lru_cache'd, a download that never completes means the cache is never
    # populated and every future request pays the same cost again. A
    # generous but finite timeout here means a genuinely slow/stuck Drive
    # download fails fast and cleanly (freeing the worker thread) instead of
    # potentially hanging indefinitely, which matters on a 1GB RAM instance
    # with a limited number of worker threads.
    request = service.files().get_media(fileId=file_id)
    buffer = io.BytesIO()
    downloader = MediaIoBaseDownload(buffer, request)
    done = False
    _download_started_at = time.monotonic()
    _DOWNLOAD_TIMEOUT_SECONDS = 40.0
    while not done:
        if time.monotonic() - _download_started_at > _DOWNLOAD_TIMEOUT_SECONDS:
            raise TimeoutError(
                f"Google Drive PDF download exceeded {_DOWNLOAD_TIMEOUT_SECONDS:.0f}s for file_id={file_id}"
            )
        _, done = downloader.next_chunk()
    return buffer.getvalue()


def split_into_chunks(text: str) -> list[str]:
    text = text.strip()
    if len(text) <= MAX_CHUNK_CHARS:
        return [text] if text else []
    return [
        text[start : start + MAX_CHUNK_CHARS]
        for start in range(0, len(text), MAX_CHUNK_CHARS)
    ]


def _detect_printed_page_number(page_text: str, pdf_page_number: int, max_drift: int = 30):
    """Best-effort detection of the page number actually printed on this page
    (header/footer), independent of any manually-supplied --page-offset.

    Why this exists: printed_page_offset defaults to 0 and, as of 2026-09-20,
    is 0 for every single book across all subject manifests (chemistry,
    physics, biology, math) - meaning printed_page_number has been silently
    set equal to the raw PDF page index platform-wide, with no correction for
    cover pages / table of contents / front matter. The previous fix for this
    was a single hardcoded patch for one book's title at read time
    (routes_textbook_pages.py) rather than a general one at index time.

    Only the first and last few lines of the page are checked, since a
    printed page number conventionally sits in a header or footer, not
    embedded in body text (this avoids matching an unrelated number that
    happens to appear in a math problem or a chemistry formula). A candidate
    is accepted only if it is a standalone number (not part of a longer word
    or a decimal) and within max_drift of the raw PDF index - this keeps the
    detector from being fooled by e.g. a chapter or exercise number, since a
    real printed page number is always close to the actual PDF position; it
    just should never be trusted to be exactly equal to it.

    Returns the detected printed page number, or None if nothing found
    reaches a confident conclusion (caller should then fall back to the
    existing pdf_page_number - printed_page_offset behaviour).
    """
    if not page_text:
        return None

    lines = [ln.strip() for ln in page_text.splitlines() if ln.strip()]
    if not lines:
        return None

    # Printed page numbers live in the first/last couple of lines of a page,
    # not scattered through the body - checking only these avoids matching
    # unrelated numbers (exercise numbers, chemical formulas, dates) that
    # happen to appear elsewhere on the page.
    candidate_lines = lines[:2] + lines[-2:]

    best_candidate = None
    best_drift = max_drift + 1
    for line in candidate_lines:
        # A standalone number: the whole line (after stripping common
        # decorative page-number punctuation) is digits only. Deliberately
        # strict - a line like "Exercise 12" or "Figure 3.2" must NOT match.
        stripped = line.strip(" -–—.|•")
        if not stripped.isdigit():
            continue
        try:
            candidate = int(stripped)
        except ValueError:
            continue
        if candidate <= 0:
            continue
        drift = abs(candidate - pdf_page_number)
        if drift <= max_drift and drift < best_drift:
            best_candidate = candidate
            best_drift = drift

    return best_candidate


def _ocr_page(pdf_path: str, page_number_1based: int) -> str:
    """Render one PDF page with Poppler and OCR it with Tesseract."""
    pdftoppm = shutil.which("pdftoppm")
    tesseract = shutil.which("tesseract")
    if not pdftoppm or not tesseract:
        missing = []
        if not pdftoppm:
            missing.append("pdftoppm (poppler-utils)")
        if not tesseract:
            missing.append("tesseract")
        raise RuntimeError("OCR dependencies unavailable: " + ", ".join(missing))

    with tempfile.TemporaryDirectory(prefix="nabil_ocr_") as tmpdir:
        prefix = str(Path(tmpdir) / "page")
        render = subprocess.run(
            [
                pdftoppm,
                "-f",
                str(page_number_1based),
                "-l",
                str(page_number_1based),
                "-singlefile",
                "-r",
                "180",
                "-png",
                pdf_path,
                prefix,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=120,
        )
        if render.returncode != 0:
            raise RuntimeError(
                f"pdftoppm failed for page {page_number_1based}: "
                f"{render.stderr.strip()[:500]}"
            )

        image_path = prefix + ".png"
        ocr = subprocess.run(
            [tesseract, image_path, "stdout", "-l", "eng"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=120,
        )
        if ocr.returncode != 0:
            raise RuntimeError(
                f"tesseract failed for page {page_number_1based}: "
                f"{ocr.stderr.strip()[:500]}"
            )
        return (ocr.stdout or "").strip()


def index_book(
    file_id: str,
    title: str,
    subject: str,
    grade: str,
    curriculum: str,
    printed_page_offset: int = 0,
):
    db = SessionLocal()
    pdf_path = None

    try:
        book = (
            db.query(Book)
            .filter(
                Book.drive_file_id == file_id,
                Book.grade == grade,
                Book.subject == subject,
                Book.curriculum == curriculum,
            )
            .first()
        )
        # A last-page high-water mark loses gaps caused by OCR failures or
        # interrupted writes. Track EVERY committed PDF page instead.
        completed_pdf_pages = set()
        if book:
            existing_printed = (
                db.query(BookChunk.printed_page_number)
                .filter(BookChunk.book_id == book.id)
                .distinct()
                .all()
            )
            completed_pdf_pages.update(
                int(row[0]) + printed_page_offset for row in existing_printed
            )
            existing_pages = (
                db.query(BookPage.pdf_page_index)
                .filter(BookPage.book_id == book.id)
                .all()
            )
            completed_pdf_pages.update(
                int(row[0]) for row in existing_pages if row[0] is not None
            )
            print(
                f"📚 {title}: {len(completed_pdf_pages)} distinct PDF pages "
                "already committed; resume ONLY missing pages.",
                flush=True,
            )
            if book.total_pages and len(
                {p for p in completed_pdf_pages if 1 <= p <= book.total_pages}
            ) >= book.total_pages:
                print(f"⏭️ Entire book complete: {title}; no download/OCR needed", flush=True)
                return

        service = get_drive_service()
        print(f"⏳ تحميل ملف PDF: {title}", flush=True)
        pdf_bytes = download_pdf(service, file_id)

        with tempfile.NamedTemporaryFile(
            prefix="nabil_book_", suffix=".pdf", delete=False
        ) as tmp:
            tmp.write(pdf_bytes)
            pdf_path = tmp.name

        reader = PdfReader(io.BytesIO(pdf_bytes))
        total_pages = len(reader.pages)
        print(f"📄 عدد صفحات الملف: {total_pages}", flush=True)

        if not book:
            book = Book(
                title=title,
                subject=subject,
                grade=grade,
                curriculum=curriculum,
                drive_file_id=file_id,
                total_pages=total_pages,
            )
            db.add(book)
            db.commit()
            db.refresh(book)

        ocr_pages = 0
        text_pages = 0
        skipped_pages = 0
        total_chunks = 0

        for pdf_index, page in enumerate(reader.pages):
            page_number = pdf_index + 1
            if page_number in completed_pdf_pages:
                continue

            print(f"  🔎 معالجة صفحة PDF رقم {page_number}...", flush=True)

            try:
                text = (page.extract_text() or "").strip()
            except Exception as exc:
                print(f"  ⚠️ استخراج النص المباشر فشل: {exc}", flush=True)
                text = ""

            used_ocr = False
            if len(text) < MIN_USABLE_TEXT_CHARS:
                try:
                    print(
                        "  👁️ الصفحة مصوّرة/نصها قليل؛ تشغيل OCR...",
                        flush=True,
                    )
                    ocr_text = _ocr_page(pdf_path, page_number)
                    if len(ocr_text) > len(text):
                        text = ocr_text
                        used_ocr = True
                except Exception as exc:
                    print(f"  ⚠️ OCR فشل في صفحة {page_number}: {exc}", flush=True)
                    if not text:
                        # Do not checkpoint a failed OCR page: retry on resume.
                        raise

            print(
                f"  📝 استخرج {len(text)} حرف من صفحة {page_number}",
                flush=True,
            )

            # Prefer the page number actually printed on the page (detected
            # from its own header/footer text) over a blind PDF-index-minus-
            # offset calculation. This is what makes the fix general across
            # every book instead of needing a manually-verified --page-offset
            # or a per-book hardcoded patch: a manually-set printed_page_offset
            # (nonzero) is still honored as an override for a book someone has
            # already verified, but the common case - offset left at the
            # default 0, which as of 2026-09-20 is every book in the catalog -
            # now self-corrects from the real printed page number when it can
            # be read from the page, instead of silently assuming no front
            # matter exists.
            detected_page = _detect_printed_page_number(text, page_number)
            if printed_page_offset:
                printed_page = page_number - printed_page_offset
            elif detected_page is not None:
                printed_page = detected_page
            else:
                printed_page = page_number
            if not text:
                skipped_pages += 1
                # Only a successfully inspected (possibly blank) page is marked
                # complete; failures above deliberately leave a retryable gap.
                db.add(
                    BookPage(
                        book_id=book.id,
                        printed_page_number=printed_page,
                        pdf_page_index=page_number,
                        text_content="",
                    )
                )
                db.commit()
                print(
                    f"  ⏭️ صفحة {page_number} بلا نص قابل للاستخراج (checkpoint saved)",
                    flush=True,
                )
                continue

            if used_ocr:
                ocr_pages += 1
            else:
                text_pages += 1

            chunks = split_into_chunks(text)

            for i, chunk_text in enumerate(chunks):
                vector = embed_text(chunk_text)
                db.add(
                    BookChunk(
                        book_id=book.id,
                        subject=subject,
                        grade=grade,
                        curriculum=curriculum,
                        printed_page_number=printed_page,
                        chunk_index_in_page=i,
                        text_content=chunk_text,
                        embedding=vector,
                    )
                )
                total_chunks += 1

            # Page text and all vector chunks commit in one transaction.
            # On interruption either the entire page exists or none of it does.
            db.add(
                BookPage(
                    book_id=book.id,
                    printed_page_number=printed_page,
                    pdf_page_index=page_number,
                    text_content=text,
                )
            )
            db.commit()
            db.expire_all()
            print(f"  ✅ خزّنت صفحة {page_number}/{total_pages}", flush=True)

            if pdf_index % 10 == 0:
                gc.collect()

        print(
            "✅ خلصت فهرسة: "
            f"{title} ({total_pages} صفحة) | "
            f"direct-text={text_pages} | OCR={ocr_pages} | "
            f"skipped={skipped_pages} | chunks={total_chunks}",
            flush=True,
        )

    finally:
        db.close()
        if pdf_path and os.path.exists(pdf_path):
            try:
                os.unlink(pdf_path)
            except OSError:
                pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--grade", required=True)
    parser.add_argument("--curriculum", required=True)
    parser.add_argument("--page-offset", type=int, default=0)
    args = parser.parse_args()

    index_book(
        file_id=args.file_id,
        title=args.title,
        subject=args.subject,
        grade=args.grade,
        curriculum=args.curriculum,
        printed_page_offset=args.page_offset,
    )
