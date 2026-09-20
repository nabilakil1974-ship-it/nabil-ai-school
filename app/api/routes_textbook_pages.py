"""Read-only previews of the exact indexed government textbook PDF page.

Download only an authorized indexed Book's Drive PDF; never accept arbitrary Drive
file IDs or page offsets from the browser. A page must be in BookPage.
"""
import os
import subprocess
import tempfile
from functools import lru_cache

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Book, BookPage

router = APIRouter()


@lru_cache(maxsize=3)
def _drive_pdf_bytes(file_id: str) -> bytes:
    # The same reader used by the running textbook indexer authenticates with
    # the server's read-only service account. Never send credentials to clients.
    from scripts.index_books import download_pdf, get_drive_service
    data = download_pdf(get_drive_service(), file_id)
    if not data.startswith(b"%PDF") or len(data) > 70 * 1024 * 1024:
        raise ValueError("Invalid or oversized textbook PDF")
    return data


@lru_cache(maxsize=24)
def _render_pdf_page(file_id: str, pdf_page: int) -> bytes:
    from pypdf import PdfReader
    import io

    payload = _drive_pdf_bytes(file_id)
    if pdf_page < 1 or pdf_page > len(PdfReader(io.BytesIO(payload)).pages):
        raise ValueError("PDF page outside of book")
    with tempfile.TemporaryDirectory(prefix="nabil_book_page_") as tmp:
        original = os.path.join(tmp, "book.pdf")
        prefix = os.path.join(tmp, "page")
        with open(original, "wb") as handle:
            handle.write(payload)
        process = subprocess.run(
            [
                "pdftoppm", "-f", str(pdf_page), "-l", str(pdf_page),
                "-singlefile", "-scale-to", "1400", "-jpeg", original, prefix,
            ],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=45, check=False,
        )
        if process.returncode:
            raise ValueError("Could not render textbook page")
        with open(prefix + ".jpg", "rb") as handle:
            return handle.read()


@router.get("/textbooks/{book_id}/pages/{printed_page}/image")
def textbook_page_image(book_id: str, printed_page: int, db: Session = Depends(get_db)):
    if printed_page < 1:
        raise HTTPException(status_code=404, detail="Book page not found")
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    # Legacy Grade 9 Chemistry indexed its true PDF page as printed page.
    # Convert the verified printed page back to that indexed value only for
    # this exact book when the indexed value and PDF position agree.
    page = None
    if book.title.strip().lower() == "chemistry - grade 9.pdf":
        legacy_pdf_page = printed_page - 2
        if legacy_pdf_page >= 1:
            candidate = (
                db.query(BookPage)
                .filter(
                    BookPage.book_id == book.id,
                    BookPage.printed_page_number == legacy_pdf_page,
                    BookPage.pdf_page_index == legacy_pdf_page,
                )
                .first()
            )
            if candidate is not None:
                page = candidate
    if page is None:
        page = (
            db.query(BookPage)
            .filter(
                BookPage.book_id == book.id,
                BookPage.printed_page_number == printed_page,
            )
            .order_by(BookPage.pdf_page_index.asc())
            .first()
        )
    if page is None or not page.pdf_page_index:
        raise HTTPException(status_code=404, detail="Indexed page unavailable")
    try:
        jpg = _render_pdf_page(book.drive_file_id, int(page.pdf_page_index))
    except Exception:
        raise HTTPException(status_code=503, detail="Original textbook page is temporarily unavailable")
    return Response(
        jpg, media_type="image/jpeg",
        headers={"Cache-Control": "public, max-age=3600", "X-Content-Type-Options": "nosniff"},
    )
