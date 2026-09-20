"""Read-only previews of the exact indexed government textbook PDF page.

Download only an authorized indexed Book's Drive PDF; never accept arbitrary Drive
file IDs or page offsets from the browser. A page must be in BookPage.
"""
import os
import subprocess
import tempfile
from functools import lru_cache
import io

from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Book, BookPage, BookChunk
from app.services.textbook_scope import resolve_textbook_curriculum
from app.core.textbook_page_citations import resolve_book_printed_page
from app.services.textbook_page_request import parse_textbook_page_request, indexed_textbook_page_context

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


@lru_cache(maxsize=48)
def _embedded_figure_pngs(file_id: str, pdf_page: int) -> tuple[bytes, ...]:
    """Extract real embedded textbook figures, never the whole scanned page.

    This is a conservative fallback. Tiny icons and full-page scan/background
    images are excluded. If a page has no separable embedded figure, return no
    crops rather than pretending a generated image is the book figure.
    """
    import fitz
    payload = _drive_pdf_bytes(file_id)
    doc = fitz.open(stream=payload, filetype="pdf")
    if pdf_page < 1 or pdf_page > doc.page_count:
        return tuple()
    page = doc[pdf_page - 1]
    candidates = []
    seen = set()
    for image in page.get_images(full=True):
        xref = int(image[0])
        if xref in seen:
            continue
        seen.add(xref)
        try:
            pix = fitz.Pixmap(doc, xref)
            width, height = int(pix.width), int(pix.height)
            area = width * height
            # Exclude full-page scans / backgrounds and decorative micro-icons.
            if width < 110 or height < 90 or area < 18000:
                continue
            if width >= 1500 and height >= 1000:
                continue
            if area > 1_450_000:
                continue
            if pix.alpha or pix.n > 4:
                pix = fitz.Pixmap(fitz.csRGB, pix)
            png = pix.tobytes("png")
            if len(png) < 2500:
                continue
            candidates.append((area, png))
        except Exception:
            continue
    # Larger meaningful illustrations first; cap to avoid flooding the lesson.
    candidates.sort(key=lambda item: item[0], reverse=True)
    return tuple(png for _, png in candidates[:4])


def _resolve_indexed_book_page(book, printed_page: int, db: Session):
    page = None
    if book.title.strip().lower() == "chemistry - grade 9.pdf":
        legacy_pdf_page = printed_page - 2
        if legacy_pdf_page >= 1:
            page = (
                db.query(BookPage)
                .filter(
                    BookPage.book_id == book.id,
                    BookPage.printed_page_number == legacy_pdf_page,
                    BookPage.pdf_page_index == legacy_pdf_page,
                )
                .first()
            )
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
    return page


@router.get("/textbooks/{book_id}/pages/{printed_page}/figures/{figure_index}/image")
def textbook_figure_image(
    book_id: str, printed_page: int, figure_index: int,
    db: Session = Depends(get_db),
):
    """Return one REAL embedded figure from a verified indexed textbook page."""
    if printed_page < 1 or figure_index < 0 or figure_index > 3:
        raise HTTPException(status_code=404, detail="Textbook figure not found")
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    page = _resolve_indexed_book_page(book, printed_page, db)
    if page is None or not page.pdf_page_index:
        raise HTTPException(status_code=404, detail="Indexed page unavailable")
    figures = _embedded_figure_pngs(book.drive_file_id, int(page.pdf_page_index))
    if figure_index >= len(figures):
        raise HTTPException(status_code=404, detail="No separable original figure on this page")
    return Response(
        figures[figure_index], media_type="image/png",
        headers={"Cache-Control": "public, max-age=3600", "X-Content-Type-Options": "nosniff"},
    )


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
    page = _resolve_indexed_book_page(book, printed_page, db)
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
    message: str = Form(""),
    book_page: str = Form(""),
    db: Session = Depends(get_db),
):
    """Fast, provider-free first book card while the lesson AI is still working.

    Only indexed material from selected grade, subject and curriculum is shown.
    No invented paragraph, book exercise, page number, or visual is allowed.
    """
    try:
        page_request = parse_textbook_page_request(message, book_page)
    except ValueError:
        return {'status': 'invalid_page', 'message': 'Invalid printed book page'}
    if page_request is not None:
        try:
            sources = indexed_textbook_page_context(
                db, grade=str(grade or '').strip(),
                subject=str(subject or '').strip(),
                curriculum=resolve_textbook_curriculum(curriculum, language),
                printed_page=page_request[0], mode='page',
            )
        except (LookupError, ValueError):
            return {'status': 'unavailable', 'message': 'Requested printed page not uniquely indexed'}
        indexed = sources[0]
        printed = indexed['printed_page']
        return {
            'status': 'indexed',
            'lesson': str(lesson or '').strip() or f'Printed page {printed}',
            'book_title': indexed['book_title'],
            'printed_page': printed,
            'pdf_page': indexed.get('pdf_page'),
            'page_image_url': (
                f"/api/textbooks/{indexed['book_id']}/pages/{printed}/image"
                if indexed.get('pdf_page') else None
            ),
            'figure_image_urls': [],
            'source_excerpt': indexed['text'][:420],
            'disclaimer': 'Exact indexed textbook page. Image opens the original PDF page.',
        }
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
        # Return verified metadata immediately; NEVER download a PDF or extract
        # its embedded figures before the first teaching card can render.
        # Candidate URLs are resolved lazily by browser; absent figures 404
        # and are hidden, not represented as original textbook figures.
        "figure_image_urls": (
            [
                f"/api/textbooks/{item.book_id}/pages/{printed}/figures/{i}/image"
                for i in range(3)
            ]
            if recorded and recorded[0] and printed else []
        ),
        "source_excerpt": (item.text_content or "").strip()[:420],
        "disclaimer": "Book excerpt / original page preview. The full lesson is still being prepared.",
    }
