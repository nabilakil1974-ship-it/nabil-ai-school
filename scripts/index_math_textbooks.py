"""Batch-index CRDP mathematics textbooks from Drive into Railway PostgreSQL/pgvector."""
import json
from pathlib import Path
from sqlalchemy import text
from app.db.session import engine
from scripts.index_books import index_book

MANIFEST = Path("data/math_textbooks_manifest.json")

def main():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    books = data["books"]
    print(f"Starting mathematics cloud indexing: {len(books)} books", flush=True)
    # Use the SAME global textbook/OCR advisory lock as the science worker.
    # This prevents two expensive PDF/OCR indexers from competing once the
    # exclusive science worker patch is deployed.
    with engine.connect() as connection:
        locked = False
        if connection.dialect.name == "postgresql":
            print("MATH_INDEX_WAITING_FOR_EXCLUSIVE_TEXTBOOK_LOCK", flush=True)
            connection.execute(text("SELECT pg_advisory_lock(728168120)"))
            connection.commit()
            locked = True
            print("MATH_INDEX_LOCK_ACQUIRED", flush=True)
        try:
            for n, b in enumerate(books, 1):
                print(f"\n[{n}/{len(books)}] {b['grade']} | {b['language']} | {b['title']}", flush=True)
                index_book(
                    file_id=b["drive_file_id"],
                    title=b["title"],
                    subject=b["subject"],
                    grade=b["grade"],
                    curriculum=b["curriculum"],
                    printed_page_offset=int(b.get("page_offset", 0)),
                )
        finally:
            if locked:
                connection.execute(text("SELECT pg_advisory_unlock(728168120)"))
                connection.commit()
                print("MATH_INDEX_LOCK_RELEASED", flush=True)
    print("\nMathematics cloud indexing complete.", flush=True)

if __name__ == "__main__":
    main()
