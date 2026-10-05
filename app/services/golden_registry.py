"""Canonical Golden registry facade.

Student runtime contract:
    data/NABIL_GOLDEN_CATALOGUE.json
        -> app.services.golden_package_store
        -> local reviewed Golden package
        -> renderer

This module deliberately contains no Drive, Google API, or LLM runtime path.
Production/synchronization may use Drive before deployment, but every student
must read the same deployed Golden package for fast, deterministic, zero-AI-cost
lesson delivery.
"""
from __future__ import annotations

from app.services.golden_package_store import catalogue_entries, lesson_source

KINDS = ("lesson", "exercises", "worksheet", "lab", "pptx")


def load():
    """Compatibility return shape used by older callers: (lessons, duplicates)."""
    return catalogue_entries(), set()


def rows():
    out = []
    for lid, ent in sorted(catalogue_entries().items()):
        assets = ent.get("assets") or {}
        lesson_asset = assets.get("lesson") if isinstance(assets, dict) else {}
        if not isinstance(lesson_asset, dict):
            lesson_asset = {}
        local = lesson_source(lid)
        out.append({
            "lesson_id": lid,
            "title": str(ent.get("title") or lid),
            "language": str(ent.get("language") or ""),
            "version": str(ent.get("version") or lesson_asset.get("version") or "0.01"),
            "drive_file_id": lesson_asset.get("drive_file_id") or ent.get("drive_file_id"),
            "drive_url": lesson_asset.get("drive_url") or ent.get("drive_url"),
            "golden": True,
            "status": "ready" if local else "package_missing",
            "runtime_source": local[2] if local else None,
        })
    return out


def get_asset(lesson_id, kind="lesson"):
    """Return a runtime asset from the deployed Golden package.

    Lesson text supports the migration fallback in golden_package_store.
    Other kinds are returned only when their reviewed snapshot exists in the
    canonical package metadata. They are never generated or fetched at runtime.
    """
    lid = str(lesson_id or "").strip().upper()
    entries = catalogue_entries()
    ent = entries.get(lid)
    if not ent:
        return None

    if kind == "lesson":
        found = lesson_source(lid)
        if not found:
            return None
        entry, text, source = found
        return {
            "lesson_id": lid,
            "kind": "lesson",
            "entry": entry,
            "asset": ((entry.get("assets") or {}).get("lesson") or {}),
            "content": text,
            "via": source,
        }

    # Structured non-lesson assets are intentionally local-only.  The package
    # store will become their single reader as those assets are migrated.
    return None


def lesson_text(lesson_id):
    found = lesson_source(lesson_id)
    return found[1] if found else None
