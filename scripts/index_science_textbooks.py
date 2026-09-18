"""Index CRDP science textbooks (chemistry, physics, biology) into PostgreSQL/pgvector."""
import argparse, json
from pathlib import Path
from scripts.index_books import index_book

MANIFESTS = {
    "chemistry": Path("data/chemistry_textbooks_manifest.json"),
    "physics": Path("data/physics_textbooks_manifest.json"),
    "biology": Path("data/biology_textbooks_manifest.json"),
}

def run_manifest(name):
    data=json.loads(MANIFESTS[name].read_text(encoding="utf-8"))
    books=data["books"]
    print(f"Starting {name} cloud indexing: {len(books)} book mappings", flush=True)
    seen=set()
    for n,b in enumerate(books,1):
        key=(b["drive_file_id"],b["grade"],b["language"])
        if key in seen: continue
        seen.add(key)
        print(f"[{n}/{len(books)}] {b['grade']} | {b['language']} | {b['title']}", flush=True)
        index_book(file_id=b["drive_file_id"],title=b["title"],subject=b["subject"],grade=b["grade"],
                   curriculum=b["curriculum"],printed_page_offset=int(b.get("page_offset",0)))
    print(f"{name} cloud indexing complete.", flush=True)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("subject",choices=["chemistry","physics","biology","all"])
    args=ap.parse_args()
    names=list(MANIFESTS) if args.subject=="all" else [args.subject]
    for name in names: run_manifest(name)

if __name__=="__main__": main()
