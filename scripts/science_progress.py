"""Report persisted science indexing progress from PostgreSQL (no Google Drive calls)."""
from app.db.session import SessionLocal
from app.db.models import Book, BookChunk, BookPage
from scripts.index_science_textbooks import MANIFESTS, load_books


def main():
    db = SessionLocal()
    try:
        for name, path in MANIFESTS.items():
            print(f"\n{name.upper()}", flush=True)
            total_books = complete_books = 0
            for item in load_books(path):
                total_books += 1
                book = db.query(Book).filter(
                    Book.drive_file_id == item["drive_file_id"],
                    Book.grade == item["grade"],
                    Book.subject == item["subject"],
                    Book.curriculum == item["curriculum"],
                ).first()
                if book is None:
                    print(f"  NOT STARTED | {item['grade']} | {item['title']}", flush=True)
                    continue
                offset = int(item.get("page_offset", 0))
                completed = {
                    int(p) + offset for (p,) in db.query(
                        BookChunk.printed_page_number
                    ).filter(BookChunk.book_id == book.id).distinct().all()
                }
                completed.update(
                    int(p) for (p,) in db.query(BookPage.pdf_page_index).filter(
                        BookPage.book_id == book.id
                    ).all() if p is not None
                )
                total = book.total_pages or 0
                done = sum(1 <= p <= total for p in completed) if total else len(completed)
                complete = bool(total and done >= total)
                complete_books += int(complete)
                label = "DONE" if complete else "IN PROGRESS"
                print(
                    f"  {label} {done}/{total or '?'} PDF pages | "
                    f"{item['grade']} | {item['title']}",
                    flush=True,
                )
            print(f"  Completed books: {complete_books}/{total_books}", flush=True)
    finally:
        db.close()


if __name__ == "__main__":
    main()
