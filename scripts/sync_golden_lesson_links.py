#!/usr/bin/env python3
"""Synchronize every NABIL Golden lesson discoverable on Google Drive.

Drive is the source of truth. Registry entries are retained as fallback metadata,
but discovery is global: any non-trashed Drive artifact carrying
appProperties nabil_golden=true and a nabil_lesson_id is catalogued even when the
lesson was never pre-registered in GitHub. Theory artifacts are preferred; when
multiple files describe one lesson the newest theory file wins deterministically.
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
FIELDS = "id,name,mimeType,modifiedTime,webViewLink,trashed,appProperties"


def _load_registry(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    lessons = raw.get("lessons", raw)
    if not isinstance(lessons, dict):
        raise RuntimeError("GOLDEN_REGISTRY_LESSONS_INVALID")
    return lessons


def _get_registered(service, file_id: str) -> dict[str, Any] | None:
    if not file_id:
        return None
    try:
        return service.files().get(fileId=file_id, fields=FIELDS, supportsAllDrives=True).execute()
    except Exception:
        return None


def _discover_all_golden(service) -> list[dict[str, Any]]:
    """Global Drive scan, paginated. No registry lesson-id prerequisite."""
    rows: list[dict[str, Any]] = []
    token = None
    q = "trashed = false and appProperties has { key='nabil_golden' and value='true' }"
    while True:
        response = service.files().list(
            q=q,
            fields=f"nextPageToken,files({FIELDS})",
            pageSize=1000,
            pageToken=token,
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        ).execute()
        rows.extend(response.get("files", []))
        token = response.get("nextPageToken")
        if not token:
            break
    return rows


def _lesson_id(row: dict[str, Any]) -> str:
    props = row.get("appProperties") or {}
    return str(props.get("nabil_lesson_id") or "").strip().upper()


def _rank(row: dict[str, Any]) -> tuple[int, str, str]:
    props = row.get("appProperties") or {}
    artifact = str(props.get("nabil_artifact") or "").lower()
    # Prefer the complete/theory lesson over worksheet/lab satellites, then newest.
    theory = 1 if artifact in {"theory", "lesson", "golden_lesson", "complete_lesson"} else 0
    return (theory, str(row.get("modifiedTime") or ""), str(row.get("id") or ""))


def _row(lesson_id: str, entry: dict[str, Any], meta: dict[str, Any] | None, source: str) -> dict[str, Any]:
    props = (meta or {}).get("appProperties") or {}
    file_id = str((meta or {}).get("id") or entry.get("drive_theory_id") or entry.get("drive_file_id") or "").strip()
    drive_url = str((meta or {}).get("webViewLink") or entry.get("drive_url") or "").strip()
    if file_id and not drive_url:
        drive_url = f"https://docs.google.com/document/d/{file_id}/edit"
    return {
        "lesson_id": lesson_id,
        "title": str(entry.get("title") or props.get("nabil_title") or (meta or {}).get("name") or lesson_id),
        "language": str(entry.get("language") or props.get("nabil_language") or "en"),
        "version": str(entry.get("version") or props.get("nabil_version") or "0.01"),
        "grade": entry.get("grade") or props.get("nabil_grade"),
        "subject": entry.get("subject") or props.get("nabil_subject"),
        "branch": entry.get("branch") or props.get("nabil_branch"),
        "golden": True,
        "status": "available" if meta and not meta.get("trashed") else "unavailable",
        "drive_file_id": file_id or None,
        "drive_url": drive_url or None,
        "drive_modified_time": (meta or {}).get("modifiedTime"),
        "mime_type": (meta or {}).get("mimeType"),
        "artifact_type": props.get("nabil_artifact"),
        "sync_source": source,
    }


def build_catalogue(registry_path: Path = REGISTRY) -> dict[str, Any]:
    service = get_drive_service()
    registry = _load_registry(registry_path)
    discovered = _discover_all_golden(service)

    by_lesson: dict[str, list[dict[str, Any]]] = {}
    orphan_golden: list[dict[str, Any]] = []
    for meta in discovered:
        lid = _lesson_id(meta)
        if not lid:
            orphan_golden.append({"id": meta.get("id"), "name": meta.get("name"), "modifiedTime": meta.get("modifiedTime")})
            continue
        by_lesson.setdefault(lid, []).append(meta)

    out: dict[str, Any] = {}
    all_ids = set(str(x).strip().upper() for x in registry) | set(by_lesson)
    for lesson_id in sorted(x for x in all_ids if x):
        entry = registry.get(lesson_id) or registry.get(lesson_id.lower()) or {}
        if not isinstance(entry, dict):
            entry = {}
        candidates = by_lesson.get(lesson_id, [])
        meta = max(candidates, key=_rank) if candidates else None
        source = "drive_global_discovery" if meta else "registry"
        if meta is None:
            registered_id = str(entry.get("drive_theory_id") or entry.get("drive_file_id") or "").strip()
            meta = _get_registered(service, registered_id)
            source = "registry_verified" if meta else "registry_unavailable"
        out[lesson_id] = _row(lesson_id, entry, meta, source)

    return {
        "schema_version": "2.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_of_truth": "google_drive",
        "discovery_mode": "global_app_properties_scan",
        "lesson_count": len(out),
        "drive_golden_file_count": len(discovered),
        "orphan_golden_count": len(orphan_golden),
        "orphan_golden_files": orphan_golden,
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
    print(
        f"SYNCED {catalogue['lesson_count']} lessons; "
        f"Drive Golden files={catalogue['drive_golden_file_count']}; "
        f"orphans={catalogue['orphan_golden_count']} -> {output}"
    )


if __name__ == "__main__":
    main()
