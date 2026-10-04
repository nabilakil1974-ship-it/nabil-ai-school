#!/usr/bin/env python3
"""Synchronize data/NABIL_GOLDEN_CATALOGUE.json from the master Google Sheet.

The Sheet is the maintainer-facing source of truth. Runtime continues to read the
local JSON only, so student requests never depend on Google Sheets/Drive.
Existing audit/package fields are preserved by lesson_id while canonical names,
links, grade/branch/language are refreshed from ALL_GOLDEN.
"""
from __future__ import annotations

import json
import os
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

from google.oauth2 import service_account
from googleapiclient.discovery import build

SPREADSHEET_ID = os.getenv(
    "GOLDEN_CATALOGUE_SHEET_ID", "1BHO6mxegYXPBjvNUIjYhaOrOswXPrICKXlvkaN0licI"
)
SHEET_RANGE = os.getenv("GOLDEN_CATALOGUE_RANGE", "ALL_GOLDEN!A:R")
OUTPUT = Path(os.getenv("GOLDEN_CATALOGUE_OUTPUT", "data/NABIL_GOLDEN_CATALOGUE.json"))
LESSON_ID_RE = re.compile(r"^G(?:0[1-9]|1[0-2])-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3}$", re.I)
DRIVE_ID_RE = re.compile(r"/d/([A-Za-z0-9_-]+)")


def credentials():
    raw = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip()
    if not raw:
        raise SystemExit("GOOGLE_SERVICE_ACCOUNT_JSON is required")
    info = json.loads(raw)
    return service_account.Credentials.from_service_account_info(
        info,
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets.readonly",
            "https://www.googleapis.com/auth/drive.readonly",
        ],
    )


def cell(row, index):
    return str(row[index]).strip() if index < len(row) and row[index] is not None else ""


def drive_id(url: str) -> str:
    m = DRIVE_ID_RE.search(url or "")
    return m.group(1) if m else ""


def language_name(value: str) -> str:
    v = value.strip().upper()
    return {"EN": "English", "AR": "Arabic", "FR": "French"}.get(v, value.strip())


def grade_branch(value: str, lesson_id: str):
    token = value.strip().upper()
    m = re.match(r"^(\d{1,2})(?:[- ]([A-Z]+))?$", token)
    if m:
        return str(int(m.group(1))), (m.group(2) or "")
    m = re.match(r"^G(\d{2})(?:-([A-Z]+))?", lesson_id.upper())
    return (str(int(m.group(1))), m.group(2) or "") if m else ("", "")


def subject_name(course: str, lesson_id: str) -> str:
    c = course.lower()
    if "math" in c or "-MATH-" in lesson_id.upper():
        return "Mathematics"
    if "physics" in c or "-PHYS" in lesson_id.upper():
        return "Physics"
    if "chem" in c or "-CHEM" in lesson_id.upper():
        return "Chemistry"
    if "biology" in c or "-BIO" in lesson_id.upper():
        return "Biology"
    return course.strip() or "Unknown"


def main():
    svc = build("sheets", "v4", credentials=credentials(), cache_discovery=False)
    rows = (
        svc.spreadsheets()
        .values()
        .get(spreadsheetId=SPREADSHEET_ID, range=SHEET_RANGE)
        .execute()
        .get("values", [])
    )

    old = {}
    policy = {}
    schema_version = 2
    if OUTPUT.exists():
        previous = json.loads(OUTPUT.read_text("utf-8"))
        schema_version = previous.get("schema_version", 2)
        policy = previous.get("policy", {})
        old = {
            str(x.get("lesson_id", "")).upper(): x
            for x in previous.get("lessons", [])
            if isinstance(x, dict) and x.get("lesson_id")
        }

    merged = {}
    skipped = 0
    for row in rows:
        # ALL_GOLDEN contract: A status, B source, C grade/branch, D language,
        # E course, F lesson_id, H title, N kind, Q verification, R canonical URL.
        if cell(row, 0).upper() != "GOLDEN":
            continue
        lid = cell(row, 5).upper()
        title = cell(row, 7)
        if not LESSON_ID_RE.fullmatch(lid) or not title or title.upper().startswith("SUPERSEDED"):
            skipped += 1
            continue
        if lid in merged:
            raise SystemExit(f"Duplicate lesson_id in ALL_GOLDEN: {lid}")
        grade, branch = grade_branch(cell(row, 2), lid)
        url = cell(row, 17)
        entry = dict(old.get(lid, {}))
        entry.update(
            lesson_id=lid,
            grade=grade,
            subject=subject_name(cell(row, 4), lid),
            language=language_name(cell(row, 3)),
            title=title,
            status="verified_from_master_sheet",
        )
        if branch:
            entry["branch"] = branch
        else:
            entry.pop("branch", None)
        fid = drive_id(url)
        if fid:
            entry["drive_file_id"] = fid
        if url:
            entry["drive_url"] = url
        merged[lid] = entry

    if not merged:
        raise SystemExit("Refusing to write an empty Golden catalogue")

    # The master Sheet is authoritative for membership: removed rows disappear
    # from the runtime allow-list; audit/package metadata survives for retained IDs.
    lessons = [merged[k] for k in sorted(merged)]
    payload = {
        "schema_version": schema_version,
        "purpose": "Canonical runtime allow-list synchronized automatically from NABIL GOLDEN CATALOGUE / ALL_GOLDEN. Runtime reads this local file only.",
        "policy": policy,
        "source": {
            "type": "google_sheet",
            "spreadsheet_id": SPREADSHEET_ID,
            "range": SHEET_RANGE,
        },
        "last_verified_from_drive": date.today().isoformat(),
        "count": len(lessons),
        "lessons": lessons,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    new_text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    old_text = OUTPUT.read_text("utf-8") if OUTPUT.exists() else ""
    if new_text == old_text:
        print(f"UNCHANGED: {len(lessons)} Golden lessons")
        return
    OUTPUT.write_text(new_text, "utf-8")
    print(f"UPDATED: {len(lessons)} Golden lessons from ALL_GOLDEN; skipped={skipped}")


if __name__ == "__main__":
    main()
