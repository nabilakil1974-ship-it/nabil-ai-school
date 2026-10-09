from __future__ import annotations

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NABIL AI — Universal Pedagogical Lesson Factory
Version: 27.0.0 (Golden Reference Renderer Contract + End-to-End Labs)
Strict Fail-Closed Architecture across all 400+ Curriculum Lessons.
Applicable to Mathematics, Physics, Chemistry, Biology & General Science.
"""

import os
import sys
import time
import html
import io
import json
import math
import re
import hashlib
import argparse
import tempfile
import shutil
import base64
import py_compile
import subprocess
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

sys.path.insert(0, "/app")
sys.path.insert(0, os.path.abspath("."))

from scripts.nabil_i18n import (
    resolve_lang_code, t as ui_t, html_dir_attr, narrative_language_instruction,
)
from scripts.nabil_interactive_lab import render_verified_lab, validate_lab_spec
from scripts.nabil_quiz_engine import build_full_quiz_items, render_quiz_html
from scripts.nabil_requirement5_gate import validate_requirement5_lab, assert_requirement5_publishable
from scripts.nabil_scientific_lab_coverage import (
    validate_and_annotate_curriculum_lab,
    validate_lesson_scientific_lab_coverage,
)
from scripts.nabil_transient_resilience_v1781 import (
    classify_provider_error,
    ProviderTransientError,
    ProviderDailyQuotaError,
    ProviderUnavailableError,
    NeedsAttentionError,
    CheckpointWriteError,
    save_state as save_resilience_state,
    STATUS_PAUSED_TRANSIENT,
    STATUS_PROVIDER_UNAVAILABLE,
    STATUS_NEEDS_ATTENTION,
    EXIT_PAUSED_TRANSIENT,
    EXIT_PROVIDER_UNAVAILABLE,
    EXIT_NEEDS_ATTENTION,
    ScientificGateBlocked,
)

ROOT = Path(__file__).resolve().parents[3] if len(Path(__file__).resolve().parents) > 3 else Path("/app")
CATALOG_PATH = ROOT / "data/nabil_canonical_lesson_catalog.json"
PERM_EVIDENCE_DIR = ROOT / "data/evidence_maps"
CACHE_DIR = ROOT / "data/cache/visual_evidence"
VERSIONS_DIR = ROOT / "data/versions"
ARTIFACTS_DIR = VERSIONS_DIR / "artifacts"
OUT_DIR = ROOT / "output"
GOLDEN_REGISTRY_PATH = ROOT / "data" / "golden_lessons_registry.json"
RECOVERY_STATE_DIR = ROOT / "data" / "factory_recovery_state"
REDRAW_PROMPT_VERSION = "NABIL_REDRAW_V1783"
TEXT_DIAGRAM_PROMPT_VERSION = "NABIL_TEXT_DIAGRAM_V1783"
CONCEPT_NARRATIVE_PROMPT_VERSION = "NABIL_CONCEPT_NARRATIVE_V1783"
LAB_SPEC_PROMPT_VERSION = "NABIL_LAB_SPEC_V1783"
EXERCISE_SCAN_PROMPT_VERSION = "NABIL_EXERCISE_SCAN_V1784"
EXERCISE_REVIEW_PROMPT_VERSION = "NABIL_EXERCISE_REVIEW_V1784"

for d in [PERM_EVIDENCE_DIR, CACHE_DIR, VERSIONS_DIR, ARTIFACTS_DIR, OUT_DIR, RECOVERY_STATE_DIR]:
    d.mkdir(parents=True, exist_ok=True)

PROGRESS_STARTED = None


def now():
    return datetime.now(timezone.utc).isoformat()


def progress(stage: str, **details):
    elapsed = round(time.monotonic() - PROGRESS_STARTED, 1) if PROGRESS_STARTED else 0
    print(json.dumps({"time": now(), "elapsed_seconds": elapsed, "stage": stage, **details}, ensure_ascii=False), flush=True)



def _persist_factory_recovery_state(
        entry: dict, drive_service, *, status: str, reason: str,
        unit_id: str, operation: str,
        retry_seconds: Optional[int] = None) -> dict:
    """Persist pause/attention state locally and, when available, to Drive."""
    max_cycles = max(1, int(os.getenv(
        "NABIL_FACTORY_MAX_PAUSE_RESUME_CYCLES", "12")))
    state = save_resilience_state(
        RECOVERY_STATE_DIR,
        lesson_id=str(entry.get("lesson_id") or "unknown"),
        status=status,
        reason=str(reason)[:1200],
        unit_id=str(unit_id or ""),
        operation=str(operation or ""),
        retry_seconds=retry_seconds,
        max_pause_cycles=max_cycles,
    )
    if drive_service is not None:
        from scripts import nabil_page_checkpoint as page_checkpoints
        checkpoint_root = resolve_drive_root_id()
        state = page_checkpoints.save_factory_state(
            drive_service, checkpoint_root, entry, state)
    progress(
        "FACTORY_RECOVERY_STATE_SAVED",
        lesson_id=entry.get("lesson_id"),
        status=state.get("status"),
        unit_id=unit_id,
        operation=operation,
        retry_after_seconds=state.get("retry_after_seconds"),
        next_retry_at=state.get("next_retry_at"),
    )
    return state


def _raise_if_provider_pause_required(
        entry: dict, drive_service, *, unit_id: str,
        operation: str, exc: Exception) -> None:
    """Normalize legacy provider errors to typed signals without persisting.

    Persistence happens once at the produce_lesson_for_entry boundary.
    """
    if isinstance(exc, (ProviderDailyQuotaError, ProviderTransientError,
                        ProviderUnavailableError, NeedsAttentionError)):
        if not getattr(exc, "operation", None):
            exc.operation = operation
        if not getattr(exc, "unit_id", None):
            exc.unit_id = unit_id
        raise exc

    info = classify_provider_error(exc)
    if info.kind == "daily_quota":
        raise ProviderDailyQuotaError(
            info.message,
            retry_after_seconds=info.retry_after_seconds or 21600,
            status_code=info.status_code,
            operation=operation,
            unit_id=unit_id,
            reason=info.message,
        ) from exc
    if info.kind == "transient":
        raise ProviderTransientError(
            info.message,
            retry_after_seconds=info.retry_after_seconds or 60,
            status_code=info.status_code,
            operation=operation,
            unit_id=unit_id,
            reason=info.message,
        ) from exc
    if info.kind == "auth_billing":
        raise ProviderUnavailableError(
            info.message, operation=operation, unit_id=unit_id,
            reason=info.message) from exc
    if info.kind == "needs_attention":
        raise NeedsAttentionError(
            info.message, operation=operation, unit_id=unit_id,
            reason=info.message) from exc
