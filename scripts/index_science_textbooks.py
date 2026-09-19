"""Index CRDP science textbooks (chemistry, physics, biology) into PostgreSQL/pgvector."""
import argparse
import json
from pathlib import Path

from sqlalchemy import text
from app.db.session import engine

from scripts.index_books import index_book

MANIFESTS = {
    "chemistry": Path("data/chemistry_textbooks_manifest.json"),
    "physics": Path("data/physics_textbooks_manifest.json"),
    "biology": Path("data/biology_textbooks_manifest.json"),
}


def load_books(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    books = data.get("books")
    if not isinstance(books, list):
        raise ValueError(f"{path} must contain a books[] array")
    return books


def run_books(books, label: str):
    print(f"Starting {label} cloud indexing: {len(books)} book mappings", flush=True)
    seen = set()
    for n, book in enumerate(books, 1):
        key = (
            book["drive_file_id"],
            book["grade"],
            book["subject"],
            book["curriculum"],
        )
        if key in seen:
            continue
        seen.add(key)
        print(
            f"[{n}/{len(books)}] {book['grade']} | "
            f"{book.get('language', book['curriculum'])} | {book['title']}",
            flush=True,
        )
        index_book(
            file_id=book["drive_file_id"],
            title=book["title"],
            subject=book["subject"],
            grade=book["grade"],
            curriculum=book["curriculum"],
            printed_page_offset=int(book.get("page_offset", 0)),
        )
    print(f"{label} cloud indexing complete.", flush=True)


def run_manifest(name: str):
    run_books(load_books(MANIFESTS[name]), name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("subject", choices=["chemistry", "physics", "biology", "all"])
    ap.add_argument(
        "--manifest",
        help=(
            "Optional additional textbook manifest JSON; same books[] schema, "
            "so new CRDP/Drive books can be added without changing application code."
        ),
    )
    args = ap.parse_args()

    names = list(MANIFESTS) if args.subject == "all" else [args.subject]

    # PostgreSQL session advisory lock: at most one indexer across deployments,
    # containers and manual Console sessions using this version of the script.
    with engine.connect() as connection:
        locked = False
        if connection.dialect.name == "postgresql":
            print("Waiting for exclusive science indexer lock (another container may still be finishing)...", flush=True)
            # BLOCK instead of returning. During a rolling deployment the new
            # container can boot before the old one is terminated. A try-lock
            # would make the only new worker exit permanently at that moment.
            connection.execute(text("SELECT pg_advisory_lock(728168120)"))
            connection.commit()
            locked = True
            print("Science indexer lock acquired; resuming saved pages.", flush=True)
        try:
            for name in names:
                run_manifest(name)

            if args.manifest:
                manifest_path = Path(args.manifest)
                run_books(load_books(manifest_path), f"extra manifest {manifest_path}")
        finally:
            if locked:
                connection.execute(text("SELECT pg_advisory_unlock(728168120)"))
                connection.commit()


if __name__ == "__main__":
    main()
