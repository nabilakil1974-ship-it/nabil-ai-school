#!/usr/bin/env python3
"""Synchronize NABIL AI Golden lesson links from Google Drive into GitHub data.

Drive remains the source of truth. This script reads the existing Golden registry,
checks registered Google Drive artifacts with the same authenticated Drive client
used by the book indexer, optionally discovers artifacts by NABIL appProperties,
and writes a deterministic JSON catalogue that can be committed by GitHub Actions.

No lesson content is copied to GitHub; only identifiers, titles, versions, status,
Drive links, MIME type, and Drive modified time are recorded.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from scripts.index_books import get_drive_service

REGISTRY = Path("data/golden_lessons_registry.json")
OUTPUT = Path("data/golden_lesson_links.json")


def _load_registry(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    lessons = raw.get("lessons", raw)
    if not isinstance(lessons, dict):
        raise RuntimeError("GOLDEN_REGISTRY_LESSONS_INVALID")
    return lessons


def _get_registered(service, file_id: str) -> dict[str, Any] | None:
    try:
        return service.files().get(
            fileId=file_id,
            fields="id,name,mimeType,modifiedTime,webViewLink,trashed,appProperties",
            supportsAllDrives=True,
        ).execute()
    except Exception:
        return None


def _discover(service, lesson_id: str) -> dict[str, Any] | None:
    safe_id = lesson_id.replace("'", "\\'")
    q = (
        "trashed = false and "
        f"appProperties has {{ key='nabil_lesson_id' and value='{safe_id}' }} and "
        "appProperties has { key='nabil_golden' and value='true' } and "
        "appProperties has { key='nabil_artifact' and value='theory' }"
    )
    rows = service.files().list(
        q=q,
        fields="files(id,name,mimeType,modifiedTime,webViewLink,trashed,appProperties)",
        pageSize=100,
    ).execute().get("files", [])
    if not rows:
        return None
    rows.sort(key=lambda x: str(x.get("modifiedTime") or ""), reverse=True)
    return rows[0]


def build_catalogue(registry_path: Path = REGISTRY) -> dict[str, Any]:
    service = get_drive_service()
    registry = _load_registry(registry_path)
    out: dict[str, Any] = {}

    for lesson_id in sorted(registry):
        entry = registry[lesson_id]
        if not isinstance(entry, dict):
            continue
        registered_id = str(entry.get("drive_theory_id") or entry.get("drive_file_id") or "").strip()
        meta = _get_registered(service, registered_id) if registered_id else None
        source = "registry"
        if meta is None:
            meta = _discover(service, lesson_id)
            source = "drive_discovery" if meta else "unavailable"

        file_id = str((meta or {}).get("id") or registered_id)
        drive_url = str((meta or {}).get("webViewLink") or "")
        if file_id and not drive_url:
            drive_url = f"https://docs.google.com/document/d/{file_id}/edit"

        out[lesson_id] = {
            "lesson_id": lesson_id,
            "title": str(entry.get("title") or (meta or {}).get("name") or lesson_id),
            "language": str(entry.get("language") or "en"),
            "version": str(entry.get("version") or "0.01"),
            "golden": bool(entry.get("golden", True)),
            "status": "available" if meta and not meta.get("trashed") else "unavailable",
            "drive_file_id": file_id or None,
            "drive_url": drive_url or None,
            "drive_modified_time": (meta or {}).get("modifiedTime"),
            "mime_type": (meta or {}).get("mimeType"),
            "sync_source": source,
        }

    return {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_of_truth": "google_drive",
        "lesson_count": len(out),
        "lessons": out,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", default=str(REGISTRY))
    ap.add_argument("--output", default=str(OUTPUT))
    args = ap.parse_args()
    catalogue = build_catalogue(Path(args.registry))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(catalogue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"SYNCED {catalogue['lesson_count']} lessons -> {output}")


if __name__ == "__main__":
    main()
