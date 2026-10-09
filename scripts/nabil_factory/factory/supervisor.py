from __future__ import annotations

"""Autonomous self-healing supervisor for NABIL lesson production."""

import functools
import hashlib
import os
import re
from pathlib import Path

SELF_HEAL_SUPERVISOR_VERSION = "NABIL_SELF_HEAL_SUPERVISOR_V1"

_RECOVERABLE_PREFIXES = (
    "PAGE_TRANSLATION_",
    "FULL_PAGE_TRANSLATION_",
    "FORMAL_ARABIC_REQUIRED",
    "CACHED_TRANSLATION_",
    "TRANSLATION_",
    "JSON_",
    "SCHEMA_",
    "FORMAT_",
)

_TRUTH_CRITICAL_MARKERS = (
    "SCIENTIFIC",
    "SOURCE_IDENTITY",
    "SOURCE_GATE",
    "EVIDENCE_UNVERIFIED",
    "UNVERIFIED_EVIDENCE",
    "MATH_EXPRESSION_UNVERIFIED",
    "LESSON_SCOPE",
)


def _self_heal_reason(exc: Exception) -> str:
    return f"{type(exc).__name__}:{exc}"


def is_truth_critical_factory_error(exc: Exception) -> bool:
    reason = str(exc or "").upper()
    return any(marker in reason for marker in _TRUTH_CRITICAL_MARKERS)


def is_recoverable_factory_error(exc: Exception) -> bool:
    if is_truth_critical_factory_error(exc):
        return False
    reason = str(exc or "")
    return any(reason.startswith(prefix) or prefix in reason
               for prefix in _RECOVERABLE_PREFIXES)


def guardrail_execute(
        operation: str,
        fn,
        *,
        local_repair=None,
        ai_repair=None,
        fallback=None,
        max_ai_repairs: int | None = None):
    """Closed-loop: operation -> local repair -> bounded smart repair -> fallback."""
    max_repairs = max_ai_repairs
    if max_repairs is None:
        max_repairs = max(
            0, min(3, int(os.getenv("NABIL_SELF_HEAL_MAX_AI_REPAIRS", "1"))))

    try:
        return fn()
    except Exception as first:
        if not is_recoverable_factory_error(first):
            raise
        progress(
            "SELF_HEAL_TRIGGERED",
            operation=operation,
            reason=_self_heal_reason(first)[:360],
        )
        current = first

        if local_repair is not None:
            try:
                repaired = local_repair(current)
                if repaired is not None:
                    progress("SELF_HEAL_LOCAL_REPAIR_SUCCESS", operation=operation)
                    return repaired
            except Exception as exc:
                current = exc
                if not is_recoverable_factory_error(exc):
                    raise

        if ai_repair is not None:
            for attempt in range(1, max_repairs + 1):
                try:
                    repaired = ai_repair(current, attempt)
                    if repaired is not None:
                        progress(
                            "SELF_HEAL_SMART_REPAIR_SUCCESS",
                            operation=operation,
                            attempt=attempt,
                        )
                        return repaired
                except Exception as exc:
                    current = exc
                    if not is_recoverable_factory_error(exc):
                        raise

        if fallback is not None:
            repaired = fallback(current)
            progress(
                "SELF_HEAL_SAFE_FALLBACK_APPLIED",
                operation=operation,
                reason=_self_heal_reason(current)[:360],
            )
            return repaired

        raise current


def factory_guardrail(
        *, operation: str | None = None,
        local_repair=None, ai_repair=None, fallback=None,
        max_ai_repairs: int | None = None):
    def decorate(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            return guardrail_execute(
                operation or func.__name__,
                lambda: func(*args, **kwargs),
                local_repair=local_repair,
                ai_repair=ai_repair,
                fallback=fallback,
                max_ai_repairs=max_ai_repairs,
            )
        return wrapped
    return decorate


_NUMERIC_SPAN_RE = re.compile(
    r"[-+]?[0-9٠-٩۰-۹]+(?:[.,٫٬][0-9٠-٩۰-۹]+)?(?:%|٪|°)?"
)


def repair_numeric_spans_exact(source: str, candidate: str):
    """Restore exact source numeric spans when source/candidate counts match."""
    src = list(_NUMERIC_SPAN_RE.finditer(str(source or "")))
    dst = list(_NUMERIC_SPAN_RE.finditer(str(candidate or "")))
    if not src and not dst:
        return str(candidate or "")
    if len(src) != len(dst):
        return None
    src_values = [m.group(0) for m in src]
    dst_values = [m.group(0) for m in dst]
    if src_values == dst_values:
        return str(candidate or "")
    repaired = str(candidate or "")
    for dm, sv in reversed(list(zip(dst, src_values))):
        repaired = repaired[:dm.start()] + sv + repaired[dm.end():]
    return repaired


def self_heal_logic_fingerprint() -> str:
    """Hash self-heal/validation code so stale translation caches expire."""
    root = globals().get("ROOT")
    if not isinstance(root, Path):
        root = Path("/app")
    rels = (
        "scripts/nabil_factory/factory/supervisor.py",
        "scripts/nabil_factory/cards/core.py",
        "scripts/nabil_factory/drive_runtime/core.py",
        "scripts/nabil_factory/factory/guards.py",
    )
    h = hashlib.sha256(SELF_HEAL_SUPERVISOR_VERSION.encode("utf-8"))
    for rel in rels:
        p = root / rel
        h.update(rel.encode("utf-8"))
        try:
            h.update(p.read_bytes())
        except OSError:
            h.update(b"MISSING")
    return h.hexdigest()
