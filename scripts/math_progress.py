"""Read-only Railway/PostgreSQL progress for all CRDP mathematics textbooks.

No Drive download, OCR, embeddings or indexing worker is started.
"""
import json
from pathlib import Path

from app.db.models import Book, BookChunk, BookPage
from app.db.session import SessionLocal

MANIFEST = Path("data/math_textbooks_manifest.json")


def load_books():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return list(data.get("books", []))


def main():
    books = load_books()
    db = SessionLocal()
    complete_books = 0
    started_books = 0
    known_pages = 0
    done_known_pages = 0
    missing = []
    try:
        print(f"MATHEMATICS — {len(books)} mapped textbooks", flush=True)
        for item in books:
            book = db.query(Book).filter(
                Book.drive_file_id == item["drive_file_id"],
                Book.grade == item["grade"],
                Book.subject == item["subject"],
                Book.curriculum == item["curriculum"],
            ).first()
            if book is None:
                missing.append(item)
                print(
                    f"  NOT STARTED | {item['grade']} | {item['language']} | {item['title']}",
                    flush=True,
                )
                continue

            offset = int(item.get("page_offset", 0))
            completed = {
                int(p) + offset for (p,) in db.query(
                    BookChunk.printed_page_number
                ).filter(BookChunk.book_id == book.id).distinct().all()
                if p is not None
            }
            completed.update(
                int(p) for (p,) in db.query(BookPage.pdf_page_index).filter(
                    BookPage.book_id == book.id
                ).all() if p is not None
            )
            total = int(book.total_pages or 0)
            done = sum(1 <= p <= total for p in completed) if total else len(completed)
            started_books += int(done > 0)
            if total:
                known_pages += total
                done_known_pages += min(done, total)
            complete = bool(total and done >= total)
            complete_books += int(complete)
            label = "DONE" if complete else "IN PROGRESS"
            print(
                f"  {label} {done}/{total or '?'} PDF pages | "
                f"{item['grade']} | {item['language']} | {item['title']}",
                flush=True,
            )

        remaining_pages = max(known_pages - done_known_pages, 0)
        print("\nMATHEMATICS SUMMARY", flush=True)
        print(
            f"  Completed books: {complete_books}/{len(books)} | "
            f"started: {started_books}/{len(books)} | "
            f"not started: {len(missing)}",
            flush=True,
        )
        if known_pages:
            pct = round(100 * done_known_pages / known_pages, 1)
            print(
                f"  Known PDF pages: {done_known_pages}/{known_pages} "
                f"({pct}%) | remaining: {remaining_pages}",
                flush=True,
            )
        print(
            "  Read-only report: no Drive download, OCR or indexing worker started.",
            flush=True,
        )
        if missing:
            print(
                "  To resume ONLY missing/incomplete books safely after checking "
                "that no other OCR worker is running: "
                "python -m scripts.index_math_textbooks",
                flush=True,
            )
    finally:
        db.close()


if __name__ == "__main__":
    main()
