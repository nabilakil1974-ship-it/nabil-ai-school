"""Pure deterministic helpers for reusable NABIL AI lesson packages.

Architecture
------------
NABIL AI has two different content paths:

1. Published / Golden lessons
   These lessons already exist and must be reused exactly as published.
   Students must NOT trigger RAG, embeddings, LLM generation, lab generation,
   or any other expensive operation merely to open such a lesson.

   The stable identity of a published package is:

       lesson_id + language + version

   Example:

       G12-MATH-LS-020 | en | 0.01

2. Legacy / dynamically generated lessons
   Older application code may still identify reusable lessons from curriculum
   fields such as grade, branch, subject, curriculum, language, lesson, and
   teaching mode.

   lesson_cache_key() is intentionally retained for backward compatibility
   until all callers (especially routes_chat.py) are migrated safely.

Source signatures are validation metadata. They are NOT the primary lookup key
for a published lesson and must not force RAG/book retrieval before a known
published lesson can be served.
"""

import hashlib
import json
import re
from typing import Any


DEFAULT_LESSON_LANGUAGE = "en"
DEFAULT_PACKAGE_VERSION = "0.01"

# Keep identifiers deliberately conservative because they may later be used
# inside URLs, filenames, manifests, CDN paths, or database indexes.
_LESSON_ID_RE = re.compile(r"^[A-Z0-9][A-Z0-9._-]{2,127}$")


def _normalize(value: Any) -> str:
    """Normalize ordinary metadata used in deterministic internal keys."""
    return str(value or "").strip().casefold()


def normalize_lesson_id(lesson_id: str) -> str:
    """Return the canonical representation of a NABIL lesson id.

    Example:
        " g12-math-ls-020 " -> "G12-MATH-LS-020"

    Raises:
        ValueError: if the identifier is empty or unsafe.
    """
    value = str(lesson_id or "").strip().upper()

    if not value:
        raise ValueError("lesson_id is required")

    if not _LESSON_ID_RE.fullmatch(value):
        raise ValueError(
            "Invalid lesson_id. Expected a stable identifier such as "
            "'G12-MATH-LS-020'."
        )

    return value


def normalize_language(language: str | None) -> str:
    """Normalize the package language without guessing a translation."""
    value = str(language or DEFAULT_LESSON_LANGUAGE).strip().casefold()

    if not value:
        return DEFAULT_LESSON_LANGUAGE

    # Accept values such as en, fr, ar, ar-lb.
    value = value.replace("_", "-")

    if len(value) > 32:
        raise ValueError("Invalid language identifier")

    return value


def normalize_package_version(version: str | None) -> str:
    """Normalize the immutable published-package version."""
    value = str(version or DEFAULT_PACKAGE_VERSION).strip()

    if not value:
        return DEFAULT_PACKAGE_VERSION

    if len(value) > 64:
        raise ValueError("Invalid package version")

    # Versions are used as internal identifiers / path components.
    if not re.fullmatch(r"[A-Za-z0-9._-]+", value):
        raise ValueError("Invalid package version")

    return value


def lesson_package_identity(
    lesson_id: str,
    language: str = DEFAULT_LESSON_LANGUAGE,
    version: str = DEFAULT_PACKAGE_VERSION,
) -> str:
    """Return the human-readable canonical identity of a Golden package.

    This identity is intentionally based only on stable publication metadata.
    It does not depend on the wording of a student's request, RAG results,
    embeddings, or source retrieval.

    Example:
        G12-MATH-LS-020|en|0.01
    """
    return "|".join(
        (
            normalize_lesson_id(lesson_id),
            normalize_language(language),
            normalize_package_version(version),
        )
    )


def lesson_package_key(
    lesson_id: str,
    language: str = DEFAULT_LESSON_LANGUAGE,
    version: str = DEFAULT_PACKAGE_VERSION,
) -> str:
    """Return the deterministic internal key for a published lesson package.

    The readable lesson_id remains the real curriculum identity.  This SHA-256
    value is only a storage-safe internal key where a fixed-length key is useful.

    IMPORTANT:
    Calling this function requires no RAG, embedding model, book lookup, LLM,
    or network request.
    """
    identity = lesson_package_identity(
        lesson_id=lesson_id,
        language=language,
        version=version,
    )

    return hashlib.sha256(identity.encode("utf-8")).hexdigest()


def lesson_cache_key(
    grade: str,
    branch: str,
    subject: str,
    curriculum: str,
    language: str,
    lesson: str,
    teaching_mode: str,
) -> str:
    """Legacy deterministic cache key.

    Retained temporarily for backward compatibility with existing callers.

    New Golden/published lessons should use lesson_package_key() with a stable
    lesson_id instead.

    Do NOT remove this function until routes_chat.py and every other caller have
    been inspected and migrated.
    """
    raw = "|".join(
        _normalize(x)
        for x in (
            grade,
            branch,
            subject,
            curriculum,
            language,
            lesson,
            teaching_mode,
        )
    )

    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def source_signature(source_chunks: list[dict]) -> str:
    """Build a deterministic signature for source evidence.

    The signature remains available for publication/factory validation and
    provenance checks.

    It must NOT be used in a way that forces a student request for an already
    published Golden lesson to run RAG first merely to reconstruct this value.
    """
    rows: list[tuple[str, str, str, str]] = []

    for item in source_chunks or []:
        if not isinstance(item, dict):
            continue

        rows.append(
            (
                str(item.get("book_id") or ""),
                str(item.get("page") or ""),
                str(item.get("pdf_page") or ""),
                str(item.get("text") or "")[:240],
            )
        )

    rows.sort()

    raw = json.dumps(
        rows,
        ensure_ascii=False,
        separators=(",", ":"),
    )

    return hashlib.sha256(raw.encode("utf-8")).hexdigest()
