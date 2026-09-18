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
from pathlib import Path

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
from pypdf import PdfReader

from app.core.config import settings
from app.db.session import SessionLocal
from app.db.models import Book, BookChunk
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
    request = service.files().get_media(fileId=file_id)
    buffer = io.BytesIO()
    downloader = MediaIoBaseDownload(buffer, request)
    done = False
    while not done:
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
        already_indexed_pdf_pages = 0

        if book:
            print(
                f"📚 الكتاب موجود أصلاً بالداتابيز (id={book.id}) - "
                "رح نتحقق وين وقفنا",
                flush=True,
            )
            last_chunk = (
                db.query(BookChunk)
                .filter(BookChunk.book_id == book.id)
                .order_by(BookChunk.printed_page_number.desc())
                .first()
            )
            if last_chunk:
                already_indexed_pdf_pages = (
                    last_chunk.printed_page_number + printed_page_offset
                )
                print(
                    f"⏩ آخر صفحة محفوظة: {already_indexed_pdf_pages} - "
                    "رح نكمل من بعدها",
                    flush=True,
                )

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
            if page_number <= already_indexed_pdf_pages:
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
                    print(f"  ⚠️ OCR غير متاح لهذه الصفحة: {exc}", flush=True)

            print(
                f"  📝 استخرج {len(text)} حرف من صفحة {page_number}",
                flush=True,
            )

            if not text:
                skipped_pages += 1
                print(
                    f"  ⏭️ صفحة {page_number} بلا نص قابل للاستخراج",
                    flush=True,
                )
                continue

            if used_ocr:
                ocr_pages += 1
            else:
                text_pages += 1

            printed_page = page_number - printed_page_offset
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
