"""Read-only previews of the exact indexed government textbook PDF page.

Download only an authorized indexed Book's Drive PDF; never accept arbitrary Drive
file IDs or page offsets from the browser. A page must be in BookPage.
"""
import os
import subprocess
import tempfile
from functools import lru_cache

from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Book, BookPage, BookChunk
from app.services.textbook_scope import resolve_textbook_curriculum
from app.core.textbook_page_citations import resolve_book_printed_page

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


@router.post("/textbooks/lesson-preview")
def indexed_lesson_preview(
    grade: str = Form(""),
    subject: str = Form(""),
    curriculum: str = Form(""),
    language: str = Form(""),
    lesson: str = Form(""),
    db: Session = Depends(get_db),
):
    """Fast, provider-free first book card while the lesson AI is still working.

    Only indexed material from selected grade, subject and curriculum is shown.
    No invented paragraph, book exercise, page number, or visual is allowed.
    """
    title = str(lesson or "").strip()[:160]
    scoped_grade = str(grade or "").strip()
    scoped_subject = str(subject or "").strip()
    if not title or not scoped_grade or not scoped_subject:
        return {"status": "unavailable", "message": "Select a lesson and grade"}
    book_curriculum = resolve_textbook_curriculum(curriculum, language)
    q = (
        db.query(BookChunk)
        .join(Book, Book.id == BookChunk.book_id)
        .filter(
            BookChunk.grade == scoped_grade,
            BookChunk.subject == scoped_subject,
            BookChunk.curriculum == book_curriculum,
        )
    )
    # A fast lexical lookup avoids another embedding-model load while the
    # actual RAG call runs. Do not infer a page when a title has no match.
    candidates = [title]
    tokens = [token for token in title.split() if len(token) >= 4]
    candidates += tokens[:3]
    item = None
    for phrase in candidates:
        if len(phrase) < 4:
            continue
        item = q.filter(BookChunk.text_content.ilike(f"%{phrase}%")).order_by(
            BookChunk.printed_page_number.asc(),
            BookChunk.chunk_index_in_page.asc(),
        ).first()
        if item:
            break
    if item is None:
        return {"status": "unavailable", "lesson": title}
    recorded = (
        db.query(BookPage.pdf_page_index)
        .filter(
            BookPage.book_id == item.book_id,
            BookPage.printed_page_number == item.printed_page_number,
        )
        .first()
    )
    source = {
        "book_title": item.book.title,
        "book_id": item.book_id,
        "page": item.printed_page_number,
        "pdf_page": recorded[0] if recorded else None,
    }
    printed = resolve_book_printed_page(source)
    return {
        "status": "indexed",
        "lesson": title,
        "book_title": item.book.title,
        "printed_page": printed,
        "page_image_url": (
            f"/api/textbooks/{item.book_id}/pages/{printed}/image"
            if recorded and printed else None
        ),
        "source_excerpt": (item.text_content or "").strip()[:420],
        "disclaimer": "Book excerpt / original page preview. The full lesson is still being prepared.",
    }
