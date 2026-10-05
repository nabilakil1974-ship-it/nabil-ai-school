"""Canonical local Golden package store for the student runtime.

Production happens before runtime (source/Drive -> factory -> reviewed Golden package).
Student runtime is local-only: catalogue -> local package -> renderer.
No Google/LLM calls are permitted from this module.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any

ROOT = Path(os.getenv("GOLDEN_DATA_ROOT", ".")).resolve()
CATALOGUE = Path(os.getenv("GOLDEN_REGISTRY", "data/NABIL_GOLDEN_CATALOGUE.json"))
LEGACY_ARTIFACTS = Path(os.getenv("NABIL_GOLDEN_ARTIFACT_DIR", "data/golden_artifacts"))

LESSON_ID_RE = re.compile(r"^G(?:0[1-9]|1[0-2])-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3}$", re.I)


def _safe(path: Path) -> Path:
    p = path.resolve()
    p.relative_to(ROOT)
    return p


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def catalogue_entries() -> dict[str, dict]:
    try:
        raw = _json(_safe(ROOT / CATALOGUE))
    except (OSError, ValueError, TypeError):
        return {}
    src = raw.get("lessons") if isinstance(raw, dict) else None
    if isinstance(src, dict):
        src = list(src.values())
    if not isinstance(src, list):
        return {}
    out: dict[str, dict] = {}
    for item in src:
        if not isinstance(item, dict):
            continue
        lid = str(item.get("lesson_id") or "").strip().upper()
        if not LESSON_ID_RE.fullmatch(lid):
            continue
        if str(item.get("title") or "").strip().upper().startswith("SUPERSEDED"):
            continue
        if lid not in out:
            out[lid] = dict(item)
    return out


def _verified_snapshot(entry: dict) -> tuple[str, str] | None:
    asset = ((entry.get("assets") or {}).get("lesson") or {})
    if not isinstance(asset, dict):
        return None
    rel = str(asset.get("content_path") or "").strip()
    want = str(asset.get("sha256") or "").strip().lower()
    if not rel or not want:
        return None
    try:
        p = _safe(ROOT / rel)
        payload = p.read_bytes()
    except (OSError, ValueError):
        return None
    if hashlib.sha256(payload).hexdigest() != want:
        return None
    try:
        if p.suffix.lower() == ".json":
            obj = json.loads(payload.decode("utf-8"))
            if isinstance(obj, dict):
                text = obj.get("markdown") or obj.get("text") or obj.get("content")
            else:
                text = None
        else:
            text = payload.decode("utf-8")
    except (ValueError, UnicodeDecodeError):
        return None
    text = str(text or "").strip()
    return (text, "verified_golden_snapshot") if text else None


def _legacy_text(lid: str) -> tuple[str, str] | None:
    try:
        p = _safe(ROOT / LEGACY_ARTIFACTS / f"{lid}.txt")
        text = p.read_text(encoding="utf-8").strip()
    except (OSError, ValueError, UnicodeDecodeError):
        return None
    return (text, "golden_local_artifact") if text else None


def lesson_source(lesson_id: str) -> tuple[dict, str, str] | None:
    """Return (catalogue entry, complete lesson text, local source kind).

    Priority during migration:
      1. SHA-256 verified snapshot produced before deployment.
      2. Existing data/golden_artifacts/<lesson_id>.txt.
    Never fetch Drive at student runtime.
    """
    lid = str(lesson_id or "").strip().upper()
    if not LESSON_ID_RE.fullmatch(lid):
        return None
    entry = catalogue_entries().get(lid)
    if not entry:
        return None
    found = _verified_snapshot(entry) or _legacy_text(lid)
    if not found:
        return None
    text, source = found
    return entry, text, source


def readiness(lesson_id: str) -> dict:
    lid = str(lesson_id or "").strip().upper()
    entries = catalogue_entries()
    entry = entries.get(lid)
    if not entry:
        return {"lesson_id": lid, "catalogued": False, "runtime_ready": False, "reason": "NOT_IN_CANONICAL_CATALOGUE"}
    found = lesson_source(lid)
    return {
        "lesson_id": lid,
        "catalogued": True,
        "runtime_ready": bool(found),
        "source": found[2] if found else None,
        "reason": None if found else "LOCAL_GOLDEN_PACKAGE_MISSING",
    }
