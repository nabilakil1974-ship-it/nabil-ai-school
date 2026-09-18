"""Batch-index CRDP mathematics textbooks from Drive into Railway PostgreSQL/pgvector."""
import json
from pathlib import Path
from scripts.index_books import index_book

MANIFEST = Path("data/math_textbooks_manifest.json")

def main():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    books = data["books"]
    print(f"Starting mathematics cloud indexing: {len(books)} books", flush=True)
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
    print("\nMathematics cloud indexing complete.", flush=True)

if __name__ == "__main__":
    main()
