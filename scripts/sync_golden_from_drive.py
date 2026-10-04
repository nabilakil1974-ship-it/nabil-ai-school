#!/usr/bin/env python3
"""Build the COMPLETE canonical Golden registry from Drive.

Contract:
- recursively scan the configured GOLDEN root (Grade 1 .. Grade 12 and branches)
- accept ONLY files whose names contain an exact stable lesson_id
- never fuzzy-match titles
- fail on duplicate lesson_id
- export supported lesson content to SHA-256 verified local snapshots
- atomically replace the registry only after a successful complete scan
- student runtime never calls Drive

Required env: GOLDEN_DRIVE_FOLDER_ID (preferred) or NABIL_INTERACTIVE_CURRICULUM_ROOT_ID.
Auth uses the project's existing get_drive_service(), so the same Railway/GitHub credentials work.
"""
from __future__ import annotations
import hashlib, json, os, re, sys, tempfile
from pathlib import Path

from scripts.index_books import get_drive_service

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "golden_lesson_links.json"
SNAPSHOT_DIR = ROOT / "data" / "golden_snapshots"
LESSON_RE = re.compile(r"(?<![A-Z0-9])G(?:0[1-9]|1[0-2])-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3}(?![A-Z0-9])", re.I)
FOLDER_MIME = "application/vnd.google-apps.folder"
DOC_MIME = "application/vnd.google-apps.document"


def _root_id() -> str:
    value = (os.getenv("GOLDEN_DRIVE_FOLDER_ID") or os.getenv("NABIL_INTERACTIVE_CURRICULUM_ROOT_ID") or "").strip()
    if not value:
        raise RuntimeError("GOLDEN_DRIVE_FOLDER_ID_REQUIRED")
    return value


def _children(service, folder_id):
    token = None
    while True:
        result = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields="nextPageToken,files(id,name,mimeType,modifiedTime,webViewLink,md5Checksum,size)",
            pageSize=1000,
            pageToken=token,
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        ).execute()
        yield from result.get("files", [])
        token = result.get("nextPageToken")
        if not token:
            return


def _walk(service, folder_id, path=""):
    for item in _children(service, folder_id):
        name = str(item.get("name") or "")
        current = f"{path}/{name}" if path else name
        if item.get("mimeType") == FOLDER_MIME:
            yield from _walk(service, item["id"], current)
        else:
            yield item, current


def _lesson_id(name: str) -> str | None:
    hits = {m.group(0).upper() for m in LESSON_RE.finditer(str(name or ""))}
    if len(hits) > 1:
        raise RuntimeError("MULTIPLE_LESSON_IDS_IN_FILENAME:" + name)
    return next(iter(hits), None)


def _meta(lid: str):
    p = lid.upper().split("-")
    grade = str(int(p[0][1:]))
    branch = ""
    language = ""
    for token in p[2:-1]:
        if token in {"EN", "FR", "AR"}: language = token.lower()
        elif token in {"GS", "LS", "SV", "SE", "ES", "LH", "HUM"}: branch = {"SV":"LS","ES":"SE","HUM":"LH"}.get(token, token)
    return grade, p[1], branch, language


def _title(name: str, lid: str) -> str:
    text = re.sub(re.escape(lid), "", str(name), flags=re.I)
    text = re.sub(r"\.(gdoc|html?|md|txt)$", "", text, flags=re.I)
    text = re.sub(r"^[\s_\-–—:]+|[\s_\-–—:]+$", "", text)
    return text or lid


def _download_text(service, item) -> bytes | None:
    mime = str(item.get("mimeType") or "")
    fid = item["id"]
    if mime == DOC_MIME:
        return service.files().export(fileId=fid, mimeType="text/plain").execute()
    if mime.startswith("text/") or str(item.get("name") or "").lower().endswith((".md", ".txt", ".html", ".htm")):
        return service.files().get_media(fileId=fid).execute()
    return None


def main():
    service = get_drive_service()
    root_id = _root_id()
    found = {}
    ignored = 0
    for item, drive_path in _walk(service, root_id):
        lid = _lesson_id(item.get("name", ""))
        if not lid:
            ignored += 1
            continue
        if lid in found:
            raise RuntimeError(f"DUPLICATE_GOLDEN_LESSON_ID:{lid}:{found[lid]['drive_path']}:{drive_path}")
        grade, subject, branch, language = _meta(lid)
        payload = _download_text(service, item)
        asset = {
            "drive_file_id": item["id"],
            "drive_url": item.get("webViewLink") or f"https://drive.google.com/open?id={item['id']}",
            "modifiedTime": item.get("modifiedTime") or "",
            "status": "link_only",
        }
        if payload:
            # Never publish an empty/broken export over a good registry.
            if not payload.strip():
                raise RuntimeError("EMPTY_GOLDEN_EXPORT:" + lid)
            rel = Path("data/golden_snapshots") / f"{lid}.txt"
            asset.update({
                "content_path": rel.as_posix(),
                "sha256": hashlib.sha256(payload).hexdigest(),
                "bytes": len(payload),
                "status": "available",
            })
            item["_payload"] = payload
        found[lid] = {
            "lesson_id": lid,
            "title": _title(item.get("name", ""), lid),
            "grade": grade,
            "subject": subject,
            "branch": branch,
            "language": language,
            "version": item.get("modifiedTime") or "1",
            "golden": True,
            "drive_path": drive_path,
            "assets": {"lesson": asset},
            "_payload": item.pop("_payload", None),
        }

    if not found:
        raise RuntimeError("NO_GOLDEN_LESSONS_DISCOVERED_REFUSING_TO_ERASE_REGISTRY")

    grades = {int(v["grade"]) for v in found.values()}
    # The requested production catalogue spans Grade 1 through Grade 12.
    missing_grades = [g for g in range(1, 13) if g not in grades]
    if missing_grades:
        raise RuntimeError("INCOMPLETE_GOLDEN_SCAN_MISSING_GRADES:" + ",".join(map(str, missing_grades)))

    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    for lid, ent in found.items():
        payload = ent.pop("_payload", None)
        if payload:
            target = SNAPSHOT_DIR / f"{lid}.txt"
            tmp = target.with_suffix(".tmp")
            tmp.write_bytes(payload)
            os.replace(tmp, target)

    registry = {
        "schema": 2,
        "source": "NABIL Golden complete Drive synchronization",
        "root_folder_id": root_id,
        "count": len(found),
        "grades": sorted(grades),
        "lessons": {lid: found[lid] for lid in sorted(found)},
    }
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    encoded = (json.dumps(registry, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with tempfile.NamedTemporaryFile(dir=REGISTRY.parent, delete=False) as fh:
        fh.write(encoded); tmp_name = fh.name
    os.replace(tmp_name, REGISTRY)
    print(json.dumps({"ok": True, "lessons": len(found), "grades": sorted(grades), "ignored_without_lesson_id": ignored}, ensure_ascii=False))


if __name__ == "__main__":
    main()
