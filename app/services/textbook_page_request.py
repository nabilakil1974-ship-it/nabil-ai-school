"""Exact book-page routing, independent of imperfect chapter dropdown titles.

Only page numbers attached to the selected indexed book are eligible.
A student can request one printed page or start a lesson at a printed page.
"""
import re

from app.core.textbook_page_citations import resolve_book_printed_page
from app.db.models import Book, BookPage, BookChunk

_PAGE_REQUEST = re.compile(
    r"(?i)(?:\b(?:page|pages|p\.)\s*(?:no\.?|number|n°)?\s*[:#-]?\s*"
    r"|(?:صفحة|الصفحة|صفحه|ص\.)\s*(?:رقم)?\s*[:#-]?\s*)"
    r"(?P<page>\d{1,4})\b"
)
_LESSON_INTENT = re.compile(
    r"(?i)\b(?:lesson|chapter|unit|from\s+page|start\s+at\s+page|"
    r"continue\s+from|leçon|chapitre|commencer|depuis)\b|"
    r"الدرس|الفصل|الوحدة|من\s+صفحة|ابتداء\s+من|من\s+الصفحة"
)
_EXPLICIT_EXTENDED_PAGE = re.compile(
    r"(?i)(?:from\s+(?:printed\s+)?page|start\s+at\s+page|"
    r"continue\s+from\s+page|depuis\s+la\s+page|"
    r"من\s+(?:ال)?صفحة|ابتداء\s+من\s+(?:ال)?صفحة)"
)
_NEXT_CHAPTER = re.compile(
    r"(?im)^\s*(?:chapter\s+(?:\d+|one|two|three|four|five|six|"
    r"i{1,3}|iv|v)\s*[:.\-–]?|"
    r"unit\s+(?:\d+|one|two|three|four|five)|"
    r"الفصل\s+(?:الأول|الثاني|الثالث|الرابع|\d+)|"
    r"الوحدة\s+(?:الأولى|الثانية|الثالثة|\d+))\b"
)


def parse_textbook_page_request(message: str, book_page: str = "") -> tuple[int, str] | None:
    """Return printed page and ('page'|'lesson'); never infer from exercise N."""
    supplied = str(book_page or "").strip()
    if supplied:
        if not re.fullmatch(r"\d{1,4}", supplied):
            raise ValueError("Invalid printed textbook page")
        page = int(supplied)
    else:
        match = _PAGE_REQUEST.search(str(message or ""))
        if match is None:
            return None
        page = int(match.group("page"))
    if page < 1:
        raise ValueError("Printed textbook page must be positive")
    # A numeric picker + generic "Begin selected lesson" is a PAGE request,
    # not permission to teach 12 adjacent pages. Expand only if the student
    # explicitly asks to teach/continue FROM that page.
    return page, ("lesson" if _EXPLICIT_EXTENDED_PAGE.search(message or "") else "page")


def _source_for_page(db, book: Book, page: BookPage, printed: int) -> dict:
    fragments = (
        db.query(BookChunk)
        .filter(BookChunk.book_id == book.id,
                BookChunk.printed_page_number == page.printed_page_number)
        .order_by(BookChunk.chunk_index_in_page.asc())
        .all()
    )
    text = "\n".join(str(x.text_content or "").strip()
                     for x in fragments if x.text_content).strip()
    if not text:
        text = str(page.text_content or "").strip()
    return {
        "book_title": book.title,
        "book_id": book.id,
        "page": page.printed_page_number,
        "pdf_page": page.pdf_page_index,
        "text": text,
        "printed_page": printed,
    }


def indexed_textbook_page_context(
    db, *, grade: str, subject: str, curriculum: str,
    printed_page: int, mode: str = "page", max_lesson_pages: int = 12,
) -> list[dict]:
    """Resolve the specific PRINTED page from indexed BookPage rows.

    Never search neighboring textbooks or use semantically similar pages as
    a fallback. If several books match, ask the student to identify their book
    rather than choose a random PDF. A chapter request stops at the next
    recognizable chapter heading or a bounded lesson segment.
    """
    books = (
        db.query(Book)
        .filter(Book.grade == grade, Book.subject == subject,
                Book.curriculum == curriculum)
        .order_by(Book.title.asc())
        .all()
    )
    matches = []
    for book in books:
        pages = (
            db.query(BookPage)
            .filter(BookPage.book_id == book.id)
            .order_by(BookPage.pdf_page_index.asc())
            .all()
        )
        for index, page in enumerate(pages):
            printed = resolve_book_printed_page({
                "book_title": book.title,
                "page": page.printed_page_number,
                "pdf_page": page.pdf_page_index,
                # Needed so resolve_book_printed_page can check this page's
                # own extracted text for a stated page number (the general
                # fix for the platform-wide page_offset=0 indexing bug).
                # Without it, this lookup silently fell back to only the
                # single pre-verified chemistry-grade-9 offset, meaning an
                # exact-page request like "page 90" for any OTHER book never
                # benefited from the general fix at all.
                "text": page.text_content,
            })
            if printed == printed_page:
                matches.append((book, pages, index))
                break
    if not matches:
        raise LookupError("REQUESTED_BOOK_PAGE_NOT_INDEXED")
    if len(matches) > 1:
        raise ValueError("MULTIPLE_INDEXED_BOOKS_MATCH_PAGE")
    book, pages, start_index = matches[0]
    if mode == "page":
        chosen = pages[start_index:start_index + 1]
    else:
        chosen = []
        for page in pages[start_index:start_index + max_lesson_pages]:
            snippet = (page.text_content or "")[:600]
            if chosen and _NEXT_CHAPTER.search(snippet):
                break
            chosen.append(page)
    sources = []
    for page in chosen:
        printed = resolve_book_printed_page({
            "book_title": book.title,
            "page": page.printed_page_number,
            "pdf_page": page.pdf_page_index,
            "text": page.text_content,
        })
        result = _source_for_page(db, book, page, printed)
        if result["text"]:
            sources.append(result)
    if not sources or sources[0]["printed_page"] != printed_page:
        raise LookupError("REQUESTED_BOOK_PAGE_TEXT_UNAVAILABLE")
    return sources


# Universal Drive-index routing. No per-lesson HTML or hardcoded book IDs.
_EXERCISE_REQUEST = re.compile(
    r"(?i)(?:\\b(?:exercise|exercice|problem|question|ex\\.)\\s*(?:n[°o]\\s*)?"
    r"|(?:تمرين|التمرين|السؤال|مسألة|مسأله)\\s*(?:رقم\\s*)?)"
    r"(?P<number>\\d{1,3})\\b"
)


def parse_textbook_exercise_request(message: str) -> int | None:
    match = _EXERCISE_REQUEST.search(str(message or ""))
    return int(match.group("number")) if match else None


def indexed_textbook_exercise_context(
    db, *, grade: str, subject: str, curriculum: str,
    exercise_number: int, printed_page: int | None = None,
    book_id: int | None = None,
) -> list[dict]:
    """Find the actual numbered exercise in an indexed ORIGINAL Drive PDF.

    Never substitute a similar exercise, another language, or an invented page.
    A numbered exercise can recur across chapters; ambiguous results require a
    printed page or selected book rather than guessing.
    """
    if not 1 <= exercise_number <= 999:
        raise ValueError("INVALID_EXERCISE_NUMBER")
    books = db.query(Book).filter(
        Book.grade == grade, Book.subject == subject,
        Book.curriculum == curriculum,
    ).all()
    if book_id is not None:
        books = [book for book in books if book.id == book_id]
    heading = re.compile(
        rf"(?im)(?:^|\\n)\\s*(?:(?:exercise|exercice|ex\\.|تمرين|السؤال)\\s*(?:n[°o]\\s*)?)?"
        rf"{exercise_number}\\s*[.)\\-:]\\s*"
    )
    matches = []
    for book in books:
        if not book.drive_file_id:
            continue
        pages = db.query(BookPage).filter(BookPage.book_id == book.id).order_by(
            BookPage.pdf_page_index.asc()
        ).all()
        for page in pages:
            printed = resolve_book_printed_page({
                "book_title": book.title, "page": page.printed_page_number,
                "pdf_page": page.pdf_page_index, "text": page.text_content,
            })
            if printed_page is not None and printed != printed_page:
                continue
            source = _source_for_page(db, book, page, printed)
            if heading.search(source["text"]):
                matches.append(source)
    if not matches:
        raise LookupError("EXERCISE_NOT_FOUND_IN_INDEXED_ORIGINAL_BOOK")
    if len(matches) != 1:
        raise ValueError("AMBIGUOUS_EXERCISE_SPECIFY_BOOK_AND_PRINTED_PAGE")
    return matches
