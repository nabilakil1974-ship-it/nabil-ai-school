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

ROOT = Path(__file__).resolve().parents[1] if len(Path(__file__).resolve().parents) > 1 else Path("/app")
CATALOG_PATH = ROOT / "data/nabil_canonical_lesson_catalog.json"
PERM_EVIDENCE_DIR = ROOT / "data/evidence_maps"
CACHE_DIR = ROOT / "data/cache/visual_evidence"
VERSIONS_DIR = ROOT / "data/versions"
ARTIFACTS_DIR = VERSIONS_DIR / "artifacts"
OUT_DIR = ROOT / "output"
GOLDEN_REGISTRY_PATH = ROOT / "data" / "golden_lessons_registry.json"

for d in [PERM_EVIDENCE_DIR, CACHE_DIR, VERSIONS_DIR, ARTIFACTS_DIR, OUT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

PROGRESS_STARTED = None


def now():
    return datetime.now(timezone.utc).isoformat()


def progress(stage: str, **details):
    elapsed = round(time.monotonic() - PROGRESS_STARTED, 1) if PROGRESS_STARTED else 0
    print(json.dumps({"time": now(), "elapsed_seconds": elapsed, "stage": stage, **details}, ensure_ascii=False), flush=True)


# ==============================================================================
# GOLDEN REFERENCE RENDERER CONTRACT — CONTENT-AGNOSTIC
# ==============================================================================
# This is the visual/interaction contract distilled from the approved golden
# reference lesson.  It contains NO lesson-specific science.  Scientific data
# comes only from Evidence Map -> audited narrative/solution -> verified lab.
REFERENCE_RENDERER_CONTRACT = "NABIL_REFERENCE_RENDERER_V1"
REFERENCE_RENDERER_LANGUAGES = ("ar", "en", "fr")
REFERENCE_MOBILE_VIEWPORT = (390, 844)


# ============================================================================== 
# PUBLISHED LAB ARTIFACT STORE — BUILD ONCE, SERVE MANY
# ============================================================================== 
# Only factory-produced, quality-gated lab HTML is written here. Runtime/student
# requests must read these static artifacts; they must not invoke AI/RAG to rebuild
# an already published lab.
PUBLISHED_LABS_DIR = ROOT / "data" / "published_labs"
PUBLISHED_LABS_INDEX = PUBLISHED_LABS_DIR / "index.json"
PUBLISHED_LABS_DIR.mkdir(parents=True, exist_ok=True)


def _published_lab_safe_part(value: str) -> str:
    value = str(value or "").strip()
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-.")
    return value or "unknown"


def _published_lab_artifact_key(
        lesson_id: str, lab_key: str, language: str,
        engine_version: str = REFERENCE_RENDERER_CONTRACT) -> str:
    raw = "|".join(str(x or "").strip().casefold() for x in (
        lesson_id, lab_key, language, engine_version,
    ))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _atomic_write_text(path: Path, content: str) -> None:
    """Replace a static artifact atomically; never expose a half-written file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        tmp.write_text(content, encoding="utf-8")
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            try:
                tmp.unlink()
            except OSError:
                pass


def _load_published_labs_index() -> dict:
    if not PUBLISHED_LABS_INDEX.exists():
        return {"schema": "nabil-published-labs/v1", "labs": {}, "lessons": {}}
    try:
        data = json.loads(PUBLISHED_LABS_INDEX.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RuntimeError(f"PUBLISHED_LABS_INDEX_INVALID:{exc}") from exc
    if not isinstance(data, dict):
        raise RuntimeError("PUBLISHED_LABS_INDEX_INVALID:ROOT_NOT_OBJECT")
    if not isinstance(data.get("labs", {}), dict):
        raise RuntimeError("PUBLISHED_LABS_INDEX_INVALID:LABS_NOT_OBJECT")
    if not isinstance(data.get("lessons", {}), dict):
        raise RuntimeError("PUBLISHED_LABS_INDEX_INVALID:LESSONS_NOT_OBJECT")
    data.setdefault("schema", "nabil-published-labs/v1")
    data.setdefault("labs", {})
    data.setdefault("lessons", {})
    return data


def _persist_one_verified_lab(
        *, lesson_id: str, lab_key: str, language: str, html_text: str,
        kind: str, spec: Optional[dict] = None) -> dict:
    """Persist HTML already built by the factory; validate spec again when present."""
    lesson_id = str(lesson_id or "").strip()
    lab_key = str(lab_key or "").strip()
    language = resolve_lang_code(language or "en")
    html_text = str(html_text or "")
    if not lesson_id or not lab_key:
        raise RuntimeError("PUBLISHED_LAB_IDENTITY_REQUIRED")
    if not html_text.strip():
        raise RuntimeError(f"PUBLISHED_LAB_HTML_EMPTY:{lesson_id}:{lab_key}")
    if spec is not None:
        if not isinstance(spec, dict):
            raise RuntimeError(f"PUBLISHED_LAB_SPEC_INVALID:{lesson_id}:{lab_key}")
        # Preserve the existing fail-closed scientific/evidence validation.
        validate_lab_spec(spec)

    artifact_key = _published_lab_artifact_key(lesson_id, lab_key, language)
    rel = (Path(_published_lab_safe_part(lesson_id)) /
           _published_lab_safe_part(language) /
           _published_lab_safe_part(REFERENCE_RENDERER_CONTRACT) /
           f"{artifact_key}.html")
    out = PUBLISHED_LABS_DIR / rel
    payload = html_text.encode("utf-8")
    sha = hashlib.sha256(payload).hexdigest()
    if not out.exists() or hashlib.sha256(out.read_bytes()).hexdigest() != sha:
        _atomic_write_text(out, html_text)
    return {
        "artifact_key": artifact_key,
        "lesson_id": lesson_id,
        "lab_key": lab_key,
        "language": language,
        "kind": str(kind or "lab"),
        "renderer_contract": REFERENCE_RENDERER_CONTRACT,
        "path": rel.as_posix(),
        "sha256": sha,
        "bytes": len(payload),
    }


def persist_quality_gated_labs(entry: dict, theory: dict, exercises: list) -> dict:
    """Publish all prebuilt labs only AFTER lesson QA + scientific review succeed."""
    lesson_id = str(entry.get("lesson_id") or "").strip()
    language = resolve_lang_code(entry.get("language", "en"))
    records = []

    for act in theory.get("activities") or []:
        lab_html = str(act.get("lab_html") or "")
        if not lab_html.strip():
            continue
        concept_id = str(act.get("concept_id") or "").strip()
        records.append(_persist_one_verified_lab(
            lesson_id=lesson_id,
            lab_key=f"concept:{concept_id}",
            language=language,
            html_text=lab_html,
            kind=str((act.get("lab_spec") or {}).get("kind") or "concept"),
            spec=act.get("lab_spec"),
        ))

    for ex in exercises or []:
        lab_html = str(ex.get("_prebuilt_lab_html") or "")
        lab_key = str(ex.get("_prebuilt_lab_key") or "").strip()
        if not lab_html.strip() or not lab_key:
            continue
        records.append(_persist_one_verified_lab(
            lesson_id=lesson_id,
            lab_key=lab_key,
            language=language,
            html_text=lab_html,
            kind=str((ex.get("_prebuilt_lab_spec") or {}).get("kind") or "exercise"),
            spec=ex.get("_prebuilt_lab_spec"),
        ))

    # This is the complete autonomous teacher-led lesson lab assembled from the
    # already verified concept labs/teaching steps. Persist the exact generated HTML.
    whole_html = str(theory.get("whole_lesson_lab_html") or "")
    if whole_html.strip():
        records.append(_persist_one_verified_lab(
            lesson_id=lesson_id,
            lab_key="lesson:whole",
            language=language,
            html_text=whole_html,
            kind="whole_lesson_teacher",
            spec=None,
        ))

    index = _load_published_labs_index()
    lesson_record_keys = []
    for record in records:
        key = record["artifact_key"]
        index["labs"][key] = record
        lesson_record_keys.append(key)
    index["lessons"][lesson_id] = {
        "lesson_id": lesson_id,
        "language": language,
        "renderer_contract": REFERENCE_RENDERER_CONTRACT,
        "artifact_keys": lesson_record_keys,
        "runtime_ai_required": False,
        "updated_at": now(),
    }
    index["updated_at"] = now()
    _atomic_write_text(
        PUBLISHED_LABS_INDEX,
        json.dumps(index, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    )
    progress(
        "PUBLISHED_STATIC_LABS_READY",
        lesson_id=lesson_id,
        artifacts=len(records),
        index=str(PUBLISHED_LABS_INDEX),
    )
    return {
        "lesson_id": lesson_id,
        "artifacts": records,
        "index": str(PUBLISHED_LABS_INDEX),
    }

_ARABIC_COLLOQUIAL_TOKENS = (
    "هلق", "شو", "بدك", "بدي", "فيك", "هيك", "هيدا", "هيدي",
    "هني", "ليش", "يلا", "خلينا", "رح ", "عم ", "منشوف", "منعمل",
)


def _assert_formal_arabic_text(value: str, *, purpose: str) -> None:
    """Reject generated/translated Arabic dialect in student teaching text.

    Never run this against raw textbook evidence; only NABIL-authored teaching
    or translation output is checked.
    """
    text = " " + re.sub(r"\s+", " ", str(value or "")).strip() + " "
    found = [tok.strip() for tok in _ARABIC_COLLOQUIAL_TOKENS
             if tok in text]
    if found:
        raise RuntimeError(
            f"FORMAL_ARABIC_REQUIRED:{purpose}:"
            + ",".join(sorted(set(found))))


def reference_renderer_css() -> str:
    """Shared lesson/exercise presentation contract for every subject/grade."""
    return r"""
:root{
 --nabil-ref-page:#05172d;--nabil-ref-header:#002973;
 --nabil-ref-panel:#081e33;--nabil-ref-card:#062039;
 --nabil-ref-deep:#0b1c36;--nabil-ref-control:#0d223d;
 --nabil-ref-border:#13618f;--nabil-ref-cyan:#14c8f5;
 --nabil-ref-cyan-text:#65dfff;--nabil-ref-text:#eef8ff;
 --nabil-ref-muted:#b9d7ea;--nabil-ref-green:#009e48;
 --nabil-ref-red:#ea202c;--nabil-ref-blue:#0874e8;
 --nabil-ref-purple:#5a35ca;--nabil-ref-yellow:#ffd447;
}
*{box-sizing:border-box}
html{color-scheme:dark;background:var(--nabil-ref-page)}
body{
 margin:0!important;padding:14px!important;max-width:100vw!important;
 overflow-x:hidden!important;background:var(--nabil-ref-page)!important;
 color:var(--nabil-ref-text)!important;
 font-family:system-ui,-apple-system,"Segoe UI",Arial,sans-serif!important;
}
.container{width:100%!important;max-width:1180px!important;margin:0 auto!important;min-width:0!important}
.header{
 display:flex!important;justify-content:space-between!important;align-items:center!important;
 gap:10px!important;flex-wrap:wrap!important;padding:12px 14px!important;
 background:linear-gradient(90deg,#05172d,var(--nabil-ref-header),#05172d)!important;
 border:1px solid #0b4d7f!important;border-radius:16px!important;
 position:sticky;top:4px;z-index:30;
}
.header h1{color:var(--nabil-ref-cyan-text)!important;overflow-wrap:anywhere}
.header-actions{display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end;align-items:center}
.card,.nabil-concept-card,.nabil-exercise-card,.ws-item,
#goldenReferenceCard,.lesson-final-card,.nabil-sci-card{
 background:linear-gradient(180deg,#08243d,#061d33)!important;
 color:var(--nabil-ref-text)!important;
 border:1px solid var(--nabil-ref-border)!important;
 border-radius:16px!important;box-shadow:0 12px 28px rgba(0,0,0,.28)!important;
 min-width:0!important;max-width:100%!important;
}
.card{padding:16px!important}
.nabil-concept-card h3,.nabil-exercise-card h3,#goldenReferenceCard h2,
.nabil-reference-concept>div>span:first-child{
 color:var(--nabil-ref-cyan-text)!important;
}
.nabil-teacher-step{
 background:#0b2a45!important;color:var(--nabil-ref-text)!important;
 border-inline-start-color:var(--nabil-ref-cyan)!important;
}
.nav-btn,.q-opt,.nabil-smart-lab-action{
 min-height:44px!important;border-radius:10px!important;
 border:1px solid #1f77aa!important;color:#fff!important;
 background:#0f3655!important;padding:9px 12px!important;
 font:inherit!important;font-weight:800!important;cursor:pointer;
 max-width:100%;
}
.q-opt{background:#0d2b45!important}
.nav-btn[style*="#0f766e"],.nabil-explain-lab-btn{background:#0f766e!important;border-color:#39c7b0!important}
.nav-btn[style*="#7c3aed"]{background:var(--nabil-ref-purple)!important;border-color:#9b7af1!important}
.nabil-prebuilt-exercise-lab,.interactive-lab{
 width:100%!important;max-width:100%!important;min-width:0!important;
 overflow:hidden!important;
}
.interactive-lab svg,.nabil-prebuilt-exercise-lab svg,
.nabil-explanatory-visual svg,.nabil-sci-visual-stage svg{
 display:block!important;width:100%!important;max-width:100%!important;height:auto!important;
}
.nabil-reference-concept{
 background:linear-gradient(160deg,#0f3151,#0a2239)!important;
 color:var(--nabil-ref-text)!important;border:1px solid #2f5f86!important;
 border-radius:14px!important;padding:12px!important;min-width:0!important;
}
.nabil-reference-concept *{color:inherit}

/* APPROVED NABIL SCIENTIFIC CARD — concept + final */
.nabil-sci-card{--bg:#07192d;--panel:#0d2945;--panel2:#0a2239;--line:#2f5f86;--cyan:#6ce7ff;--gold:#ffd36a;--green:#7ce6b8;--red:#ff8b98;--txt:#f4fbff;--muted:#bed4e5;background:radial-gradient(circle at 50% -20%,#153f68,#07192d 70%)!important;color:var(--txt)!important;border:1px solid #2d638d!important;border-radius:22px!important;padding:14px!important;box-shadow:0 16px 44px rgba(0,0,0,.24)!important;margin:14px 0!important;overflow:hidden!important;width:100%!important;box-sizing:border-box!important}
.nabil-sci-top{display:flex;gap:12px;align-items:center;justify-content:space-between;border-bottom:1px solid #2a5479;padding:2px 4px 11px;flex-wrap:wrap}
.nabil-sci-brand{font-weight:900;color:var(--cyan);letter-spacing:.7px}.nabil-sci-badge{font-size:.75rem;border:1px solid #46789e;border-radius:999px;padding:4px 10px;color:#d8efff}
.nabil-sci-title{margin:9px 0 2px;font-size:clamp(1.15rem,3vw,1.65rem);line-height:1.25;overflow-wrap:anywhere;color:#f4fbff!important}
.nabil-sci-grid{display:grid;grid-template-columns:minmax(250px,.92fr) minmax(390px,1.55fr) minmax(190px,.64fr);gap:12px;margin-top:12px;align-items:stretch}
.nabil-sci-panel{background:linear-gradient(160deg,#0f3151,#0a2239)!important;border:1px solid var(--line)!important;border-radius:17px!important;padding:13px!important;min-width:0}
.nabil-sci-panel h3{margin:0 0 9px;color:#9eeeff!important;font-size:1rem}.nabil-sci-section{border-top:1px solid #284e6f;padding-top:9px;margin-top:9px}.nabil-sci-label{font-weight:800;color:#8fe8ff}.nabil-sci-value{color:#fff;white-space:pre-wrap;overflow-wrap:anywhere}
.nabil-sci-visual{min-height:310px;display:flex;flex-direction:column;gap:10px}.nabil-sci-visual-stage{flex:1;display:block;background:#061827;border:1px solid #274d6d;border-radius:14px;padding:10px;overflow:auto}.nabil-sci-visual-stage svg,.nabil-sci-visual-stage canvas,.nabil-sci-visual-stage img{display:block;max-width:100%;height:auto;max-height:480px}
.nabil-sci-teacher{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:8px;min-height:100%}.nabil-sci-avatar{width:min(100%,180px);max-height:230px;object-fit:contain;filter:drop-shadow(0 12px 22px rgba(0,0,0,.25))}.nabil-sci-teacher strong{color:var(--cyan);font-size:1.05rem}.nabil-sci-teacher p{margin:0;color:#d7e9f6;line-height:1.5}
.nabil-sci-final{margin-top:12px;background:linear-gradient(145deg,#0e3547,#0b2939);border:1px solid #3b8b8a;border-radius:16px;padding:12px}.nabil-sci-final h3{margin:0 0 7px;color:#8ff3d7!important}.nabil-sci-results{display:flex;gap:8px;flex-wrap:wrap}.nabil-sci-chip{border:1px solid #41769a;background:#0c2a45;border-radius:999px;padding:5px 9px;font-size:.84rem;overflow-wrap:anywhere}.nabil-sci-verify{margin-top:9px;border-inline-start:4px solid var(--green);background:#0d2d36;border-radius:9px;padding:9px 10px}.nabil-sci-list{margin:0;padding-inline-start:18px;line-height:1.65}.nabil-sci-list li{margin:5px 0;overflow-wrap:anywhere}
.nabil-sci-tools{display:flex;gap:7px;flex-wrap:wrap;margin-top:10px}.nabil-sci-tools button{border:1px solid #4d80a5;background:#123d60;color:white;border-radius:10px;padding:8px 11px;cursor:pointer;font:inherit}.nabil-flow-row{margin:8px 0;padding:9px 11px;border-radius:10px;background:#0b2a45;border-inline-start:4px solid #14c8f5;line-height:1.55}.nabil-flow-row b{color:#8fe8ff}.nabil-flow-row.nabil-conclude{border-inline-start-color:#7ce6b8;background:#0d2d36}.nabil-flow-row.nabil-apply{border-inline-start-color:#ffd36a;background:#302b18}
@media(max-width:1080px){.nabil-sci-grid{grid-template-columns:minmax(250px,.9fr) minmax(360px,1.5fr)}.nabil-sci-teacher-panel{grid-column:1/-1}.nabil-sci-teacher{flex-direction:row;text-align:start;justify-content:flex-start}.nabil-sci-avatar{width:110px}}
@media(max-width:760px){.nabil-sci-card{padding:10px!important;border-radius:16px!important}.nabil-sci-grid{grid-template-columns:1fr!important}.nabil-sci-panel{padding:11px!important}.nabil-sci-teacher-panel{grid-column:auto}.nabil-sci-teacher{flex-direction:row;text-align:start}.nabil-sci-avatar{width:84px;max-height:112px}.nabil-sci-visual{min-height:250px}}

#goldenReferenceCard{
 background:radial-gradient(circle at 50% -20%,#153f68,#07192d 70%)!important;
 border:1px solid #2d638d!important;padding:16px!important;
}
#goldenReferenceCard>div:first-child{border-bottom-color:#2d638d!important}
#goldenReferenceCard [style*="#334155"],
#goldenReferenceCard [style*="#64748b"]{color:#d7e9f6!important}
#goldenReferenceCard [style*="#0369a1"]{color:var(--nabil-ref-cyan-text)!important}
#goldenReferenceCard [style*="#eff6ff"]{
 background:#0b2943!important;border-color:#315f82!important;color:#dff5ff!important;
}
img[data-source-scan],.source-page-scan,.textbook-page-scan{display:none!important}
mjx-container{max-width:100%!important;overflow-x:auto;overflow-y:hidden}
table{max-width:100%}
@media(max-width:430px){
 body{padding:6px!important}
 .container{max-width:100%!important;margin:0!important}
 .header{position:relative!important;display:block!important;padding:10px!important}
 .header h1{font-size:20px!important;margin:0 0 9px!important}
 .header-actions,.header>div{width:100%!important}
 .header-actions{display:grid!important;grid-template-columns:1fr!important}
 .header button,.header select,.nav-btn{width:100%!important;justify-content:center!important}
 .card,.nabil-concept-card,.nabil-exercise-card,#goldenReferenceCard{padding:10px!important;border-radius:13px!important}
 .nabil-teacher-step{padding:9px!important;margin:7px 0!important}
 .nabil-reference-concept{padding:10px!important}
 .nabil-prebuilt-exercise-lab,.interactive-lab{margin-inline:0!important}
 .nabil-sci-grid{grid-template-columns:1fr!important}
 .nabil-sci-panel{min-width:0!important}
 .nabil-sci-table-wrap{max-width:100%!important;overflow-x:auto!important}
 button,input,select,textarea{font-size:16px!important}
}
"""


# ==============================================================================
# 1. STRICT ANTI-HARDCODE & MARKDOWN CONTAMINATION SCANNER
# ==============================================================================
FORBIDDEN_EDUCATIONAL_HARDCODE = [
    "a solid has a definite shape",
    "a liquid has a definite volume",
    "free surface of a liquid",
    "standard macroscopic rule applied",
    "solid wooden block",
    "cylinder vessel",
    "communicating vessels",
    "standard pedagogical investigation",
    "documented curriculum phenomenon",
    "y = 2 * x",
    "y = 2*x",
    "conclusive solution for",
    "evaluation conforming to level",
    "directly observed curriculum setup",
    "procedure structured under official curriculum guidelines",
    "core principle p.",
]


def assert_no_lesson_specific_hardcode(source_code: str):
    # Scan executable/source content while excluding the detector's own
    # forbidden-pattern declaration; otherwise the scanner detects itself.
    import ast
    tree = ast.parse(source_code)
    lines = source_code.splitlines(keepends=True)
    scan_lines = list(lines)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(isinstance(t, ast.Name) and t.id == "FORBIDDEN_EDUCATIONAL_HARDCODE" for t in targets):
                for idx in range(node.lineno - 1, node.end_lineno):
                    scan_lines[idx] = "\n"
    scan_source = "".join(scan_lines)
    found = [p for p in FORBIDDEN_EDUCATIONAL_HARDCODE if p.lower() in scan_source.lower()]
    if found:
        raise RuntimeError(f"LESSON_SPECIFIC_HARDCODE_DETECTED: Found {found}")


def assert_no_markdown_urls_in_runtime_code(source_code: str):
    bad_patterns = [
        'src="[http',
        'scopes = ["[http',
        '](http',
    ]
    # Exclude this scanner's own bad-pattern declaration from the scan.
    import ast
    tree = ast.parse(source_code)
    lines = source_code.splitlines(keepends=True)
    scan_lines = list(lines)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(isinstance(t, ast.Name) and t.id == "bad_patterns" for t in targets):
                for idx in range(node.lineno - 1, node.end_lineno):
                    scan_lines[idx] = "\n"
    scan_source = "".join(scan_lines)
    found = [p for p in bad_patterns if p in scan_source]
    if found:
        raise RuntimeError(f"MARKDOWN_URL_CONTAMINATION_DETECTED: Found banned markdown patterns -> {found}")



def assert_renderer_family_contract() -> None:
    """Fail closed when deployed lab renderers do not support teacher-led labs."""
    import importlib
    interactive = importlib.import_module("scripts.nabil_interactive_lab")
    if not callable(getattr(interactive, "render_verified_lab", None)):
        raise RuntimeError("RENDERER_CONTRACT_MISSING:render_verified_lab")
    if not callable(getattr(interactive, "validate_lab_spec", None)):
        raise RuntimeError("RENDERER_CONTRACT_MISSING:validate_lab_spec")
    source = Path(interactive.__file__).read_text(encoding="utf-8")
    for token in ("teacher_script", "data-teacher-pointer", "nabil:teacher"):
        if token not in source:
            raise RuntimeError(f"RENDERER_TEACHER_CONTRACT_MISSING:{token}")
    optional = (
        ("scripts.nabil_geometry_lab", "render_geometry_proof_lab"),
        ("scripts.nabil_advanced_lab", "render_advanced_verified_lab"),
    )
    for module_name, callable_name in optional:
        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            continue
        if not callable(getattr(module, callable_name, None)):
            raise RuntimeError(
                f"RENDERER_FAMILY_CONTRACT_MISSING:{module_name}:{callable_name}")


def _inventory_norm(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip().casefold()


def build_independent_source_inventory(ev_map: dict) -> dict:
    """Inventory explicit source objects independently of generated pedagogy."""
    exercise_numbers, figure_labels = set(), set()
    for page in ev_map.get("pages_evidence") or []:
        text = str(page.get("text") or "")
        for m in re.finditer(
                r"(?im)(?:^|\n)\s*(?:(?:problem|exercise|problème|exercice|تمرين|مسألة)\s*)?(\d+)\s*[.\-)]+\s+",
                text):
            exercise_numbers.add(m.group(1))
        for m in re.finditer(r"(?i)\bfig(?:ure)?\.?\s*(\d+[a-z]?)", text):
            figure_labels.add(m.group(1).casefold())
    return {
        "exercise_numbers": sorted(exercise_numbers, key=lambda x: int(re.match(r"\d+", x).group())),
        "figure_labels": sorted(figure_labels),
    }


def attach_and_verify_source_completeness(ev_map: dict) -> dict:
    """Require every explicit source exercise/figure reference to be accounted for."""
    inventory = build_independent_source_inventory(ev_map)
    accepted_ex = {str(x.get("number")) for x in ev_map.get("exercise_evidence") or []}
    accounted_figs = set()
    for page in ev_map.get("pages_evidence") or []:
        for fig in page.get("figures") or []:
            for value in (fig.get("printed_label"), fig.get("printed_number")):
                if value is not None and str(value).strip():
                    accounted_figs.add(str(value).strip().casefold())
        accounted_figs |= {
            str(x).strip().casefold()
            for x in (page.get("skipped_unverified_figure_labels") or [])
        }
        accounted_figs |= {
            str(x).strip().casefold()
            for x in (page.get("required_unverified_figure_labels") or [])
        }
    missing_ex = sorted(set(inventory["exercise_numbers"]) - accepted_ex)
    missing_fig = sorted(set(inventory["figure_labels"]) - accounted_figs)
    report = {
        "passed": not missing_ex and not missing_fig,
        "inventory": inventory,
        "missing_exercise_numbers": missing_ex,
        "missing_figure_labels": missing_fig,
    }
    ev_map["source_inventory"] = inventory
    ev_map["source_completeness"] = report
    if not report["passed"]:
        raise RuntimeError(
            "SOURCE_COMPLETENESS_GATE_FAILED:" + json.dumps(report, ensure_ascii=False))
    return report


# ==============================================================================
# 2. UNIVERSAL PEDAGOGY & CURRICULUM PROFILES
# ==============================================================================
PEDAGOGY_PROFILES = {
    "L1": {"strategy": ["observe", "explore", "describe", "practice", "check"], "max_concepts": 1},
    "L2": {"strategy": ["phenomenon", "investigation", "observation", "interpretation", "rule", "application", "check"], "max_concepts": 1},
    "L3": {"strategy": ["problem", "analysis", "model", "reasoning", "derivation", "application", "verification"], "max_concepts": 2},
}

SUBJECT_PROFILES = {
    "physics": {
        "sequence": ["phenomenon", "experiment", "observation", "interpretation", "law", "application"],
        "visual_types": ["source_figure", "scientific_diagram", "graph", "simulation"],
    },
    "chemistry": {
        "sequence": ["phenomenon", "experiment", "observation", "particle_model", "equation", "application"],
        "visual_types": ["apparatus", "molecular_model", "equation", "table"],
    },
    "biology": {
        "sequence": ["observation", "structure", "function", "relationship", "interpretation", "application"],
        "visual_types": ["source_figure", "labelled_diagram", "process_diagram"],
    },
    "mathematics": {
        "sequence": ["prerequisite", "concept", "worked_example", "reasoning", "guided_practice", "independent_practice"],
        "visual_types": ["geometric_figure", "graph", "number_line", "table"],
    },
    "general_science": {
        "sequence": ["phenomenon", "investigation", "observation", "concept", "application"],
        "visual_types": ["source_figure", "scientific_diagram", "table"],
    }
}

# Non-science subjects use the same evidence-first architecture. These
# profiles define teaching order/visual form only; lesson facts still come
# exclusively from Evidence Map.
SUBJECT_PROFILES.update({
    "arabic_language": {
        "sequence": ["context", "reading", "meaning", "language_pattern", "rule", "guided_practice", "application"],
        "visual_types": ["text_highlight", "sentence_structure", "sequence", "table"],
    },
    "english_language": {
        "sequence": ["context", "reading", "meaning", "language_pattern", "rule", "guided_practice", "application"],
        "visual_types": ["text_highlight", "sentence_structure", "sequence", "table"],
    },
    "french_language": {
        "sequence": ["context", "reading", "meaning", "language_pattern", "rule", "guided_practice", "application"],
        "visual_types": ["text_highlight", "sentence_structure", "sequence", "table"],
    },
    "history": {
        "sequence": ["context", "source", "chronology", "evidence", "cause_effect", "interpretation", "synthesis"],
        "visual_types": ["timeline", "map", "source_excerpt", "comparison_table"],
    },
    "geography": {
        "sequence": ["map_or_data", "observation", "comparison", "pattern", "interpretation", "application"],
        "visual_types": ["map", "chart", "table", "process_diagram"],
    },
    "civics": {
        "sequence": ["situation", "concept", "rule", "rights_responsibilities", "case_application", "check"],
        "visual_types": ["scenario", "flowchart", "comparison_table"],
    },
    "philosophy": {
        "sequence": ["problematic", "concepts", "argument", "reasoning", "comparison", "synthesis", "critical_check"],
        "visual_types": ["argument_map", "concept_map", "comparison_table"],
    },
    "economics": {
        "sequence": ["situation", "data", "concept", "relationship", "interpretation", "application", "check"],
        "visual_types": ["chart", "table", "flowchart", "graph"],
    },
    "sociology": {
        "sequence": ["situation", "data", "concept", "relationship", "interpretation", "application", "check"],
        "visual_types": ["chart", "table", "relationship_map"],
    },
    "computer_science": {
        "sequence": ["problem", "inputs_outputs", "algorithm", "trace", "test", "debug", "application"],
        "visual_types": ["flowchart", "trace_table", "state_diagram", "code_highlight"],
    },
})

SUBJECT_ALIASES = {
    "math": "mathematics", "maths": "mathematics",
    "mathématiques": "mathematics", "رياضيات": "mathematics",
    "physique": "physics", "فيزياء": "physics",
    "chimie": "chemistry", "كيمياء": "chemistry",
    "biologie": "biology", "أحياء": "biology",
    "science": "general_science", "sciences": "general_science", "علوم": "general_science",
    "arabic": "arabic_language", "arabic_language": "arabic_language",
    "العربية": "arabic_language", "لغة_عربية": "arabic_language",
    "english": "english_language", "english_language": "english_language",
    "الإنجليزية": "english_language", "الانجليزية": "english_language",
    "french": "french_language", "français": "french_language",
    "french_language": "french_language", "الفرنسية": "french_language",
    "histoire": "history", "تاريخ": "history",
    "géographie": "geography", "جغرافيا": "geography",
    "civic_education": "civics", "تربية_مدنية": "civics", "مدنيات": "civics",
    "philosophie": "philosophy", "فلسفة": "philosophy",
    "économie": "economics", "اقتصاد": "economics",
    "sociologie": "sociology", "علم_الاجتماع": "sociology", "اجتماع": "sociology",
    "informatics": "computer_science", "informatique": "computer_science",
    "معلوماتية": "computer_science",
}


TEACHING_ENGINE_PROFILES = {
    "L1": {
        "learner": "early primary",
        "pace": "one concrete idea at a time; very short sentences; frequent visible checks",
        "teacher_moves": [
            "show one concrete object/action",
            "ask the learner to predict or point",
            "name what was observed",
            "state one simple rule",
            "let the learner imitate or try",
            "check with one short question",
        ],
    },
    "L2": {
        "learner": "upper primary/intermediate",
        "pace": "short connected steps; ask why before stating the rule; guided practice before independence",
        "teacher_moves": [
            "start from a visible phenomenon, diagram or problem",
            "ask a focused prediction",
            "run or inspect the evidence",
            "compare what changed and what stayed invariant",
            "explain why in student language",
            "formulate the rule/property",
            "apply it to one guided case",
            "check understanding before moving on",
        ],
    },
    "L3": {
        "learner": "secondary",
        "pace": "compact but rigorous; connect representations; derive or justify before exam-style application",
        "teacher_moves": [
            "state the problem or mathematical/scientific target",
            "separate givens from what must be proved/found",
            "choose and justify the property/model",
            "derive or prove step by step",
            "connect formula, graph, diagram or microscopic model",
            "verify signs, units, domain, assumptions or logical conditions",
            "apply to a representative problem",
            "end with a concise synthesis and independent check",
        ],
    },
}

SUBJECT_TEACHING_ENGINES = {
    "mathematics": {
        "default": [
            "activate the exact prerequisite",
            "show the object/problem",
            "let the learner notice a pattern",
            "name/define the idea",
            "derive or prove the property",
            "work one example while explaining WHY each step is legal",
            "let the learner try a nearby case",
            "verify and summarize",
        ],
        "geometry": [
            "read givens directly on the figure",
            "mark only verified equalities/parallelism/perpendicularity/midpoints",
            "state exactly what is required",
            "choose the theorem/property and explain why its conditions hold",
            "build the proof one relation at a time while the matching visual mark appears",
            "distinguish what is given from what is proved",
            "finish with a compact proof chain and a check question",
        ],
        "functions": [
            "identify the expression and domain first",
            "study limits/intercepts/asymptotes only when applicable",
            "compute and interpret the derivative",
            "build sign/variation reasoning",
            "connect the variation table to the graph",
            "highlight maxima/minima and verified intersections",
            "check the graph against the algebra",
        ],
        "algebra": [
            "identify the target and known form",
            "choose the transformation/property",
            "perform one algebraic move at a time",
            "explain why equivalence is preserved",
            "check by substitution or reverse operation when appropriate",
        ],
        "statistics_probability": [
            "identify population/data/events",
            "organize the given information visually",
            "choose the exact statistic/probability rule",
            "calculate with units/denominators visible",
            "interpret the result in the problem context",
        ],
    },
    "physics": {
        "default": [
            "show the physical situation",
            "identify system, variables and directions",
            "predict what should happen",
            "run/inspect the experiment or diagram",
            "state the observation",
            "explain the physical reason/model",
            "derive/state the law with units and sign convention",
            "apply and verify",
        ],
    },
    "chemistry": {
        "default": [
            "start from the observable change or chemical question",
            "separate macroscopic observation from particle interpretation",
            "identify species/symbols/charges from evidence",
            "show particle/electron/bond changes visually",
            "write and balance the equation only when supported",
            "check atom/charge conservation",
            "apply to a nearby case",
        ],
    },
    "biology": {
        "default": [
            "observe the structure/process",
            "identify parts using verified labels",
            "connect each structure to its function",
            "follow the process in causal order",
            "compare normal/changed states only when evidence supports it",
            "formulate the biological relationship",
            "apply and check understanding",
        ],
    },
    "general_science": {
        "default": [
            "observe the phenomenon",
            "ask a testable question",
            "inspect evidence or run the activity",
            "record what changes and what remains",
            "interpret without exceeding the evidence",
            "formulate the concept",
            "apply and check",
        ],
    },
}




# Teaching engines for languages/humanities remain evidence-driven.
SUBJECT_TEACHING_ENGINES.update({
    "arabic_language": {"default": [
        "read the source in context",
        "highlight the exact word/sentence feature",
        "ask the learner to infer meaning or pattern",
        "explain the language rule from the evidence",
        "apply it to one guided item",
        "let the learner produce or analyze a nearby item",
        "check and summarize",
    ]},
    "english_language": {"default": [
        "read/listen to the source in context",
        "highlight the target expression or structure",
        "infer meaning/pattern from examples",
        "state the language rule or usage clearly",
        "practice one guided item",
        "let the learner respond independently",
        "check and reformulate",
    ]},
    "french_language": {"default": [
        "read/listen to the source in context",
        "highlight the target expression or structure",
        "infer meaning/pattern from examples",
        "state the language rule or usage clearly",
        "practice one guided item",
        "let the learner respond independently",
        "check and reformulate",
    ]},
    "history": {"default": [
        "place the event/source in its verified context",
        "identify actors, dates and places only from evidence",
        "arrange the verified chronology",
        "distinguish evidence from interpretation",
        "explain supported causes/consequences",
        "connect the pieces into a concise historical synthesis",
        "check with a source-based question",
    ]},
    "geography": {"default": [
        "read the map/data/source first",
        "locate and identify verified features",
        "compare values/regions/patterns",
        "describe what the evidence shows",
        "interpret the supported relationship",
        "apply the same reading method to a nearby case",
        "check the conclusion against the data",
    ]},
    "civics": {"default": [
        "start from the verified situation or text",
        "identify the civic concept/rule",
        "separate rights, duties and institutions when present",
        "explain how the rule applies to the case",
        "compare alternatives without adding an outside claim",
        "check with a practical scenario",
    ]},
    "philosophy": {"default": [
        "state the source's problem/question",
        "define concepts from the source context",
        "reconstruct the argument and premises",
        "show the reasoning relation step by step",
        "compare positions only when the source provides them",
        "build a concise synthesis",
        "check whether the conclusion follows from the presented argument",
    ]},
    "economics": {"default": [
        "identify the economic situation and variables",
        "read the verified table/graph/data",
        "define the relevant concept from the lesson",
        "trace the supported relationship",
        "interpret the result in context",
        "apply to a guided case",
        "check against the original data",
    ]},
    "sociology": {"default": [
        "identify the social situation/source",
        "read the verified data or statements",
        "define the relevant concept",
        "map the supported relationships",
        "interpret without exceeding the evidence",
        "apply to a guided case",
        "check against the source",
    ]},
    "computer_science": {"default": [
        "state the exact problem, inputs and expected outputs",
        "trace the given algorithm/code/state",
        "show one execution step at a time",
        "explain why each step changes the state",
        "test with source-supported examples",
        "identify an error only when the trace proves it",
        "summarize the reusable method",
    ]},
})

# Topic modes change HOW NABIL teaches, never WHAT is scientifically true.
# Content still comes only from Evidence Map / verified solution.
SUBJECT_TEACHING_ENGINES["mathematics"].update({
    "trigonometry": [
        "identify the angle/triangle/circle data and the exact target",
        "place the known relations on the visual before calculating",
        "choose the relevant verified trigonometric relation",
        "transform one step at a time with exact symbolic notation",
        "connect algebraic result to the geometry",
        "check sign, interval/quadrant and reasonableness when applicable",
    ],
    "vectors_analytic_geometry": [
        "place points/vectors in the coordinate system",
        "separate geometric information from coordinate data",
        "build the required vector/line relation step by step",
        "show each coordinate operation beside the visual",
        "interpret the algebraic result geometrically",
        "verify the final relation on the diagram",
    ],
    "sequences": [
        "identify how the terms are defined and what is known",
        "generate only source-supported terms or relations",
        "look for the relevant recurrence/direct-form structure",
        "derive the requested relation one step at a time",
        "connect symbolic result to term behavior",
        "check with a permitted term/example",
    ],
    "complex_numbers": [
        "separate algebraic and geometric representations",
        "identify the requested form or geometric meaning",
        "perform one legal complex-number transformation at a time",
        "connect modulus/argument/affix to the diagram when applicable",
        "verify the result in the alternate representation",
    ],
})
SUBJECT_TEACHING_ENGINES["physics"].update({
    "mechanics": [
        "define the system and reference frame",
        "mark directions, known quantities and target on the diagram",
        "predict the motion/effect qualitatively",
        "select the source-supported law/model",
        "derive with signs and units visible",
        "connect equation to motion/force/energy representation",
        "verify dimensions, sign and physical meaning",
    ],
    "electricity": [
        "identify components and actual circuit connections",
        "mark current/voltage directions only when supported",
        "predict the circuit state before calculation",
        "apply the verified circuit law one relation at a time",
        "animate current only when the circuit state permits it",
        "check units, conservation and component values",
    ],
    "optics": [
        "identify the optical elements and reference lines",
        "mark normals/axes/points only when established",
        "trace the verified ray construction step by step",
        "state the applicable optical relation",
        "connect the construction to the conclusion",
        "check orientation/angles against the evidence",
    ],
    "waves": [
        "identify what is oscillating/propagating and the measured variables",
        "show the time/space representation",
        "connect period, frequency, wavelength or speed only when present",
        "derive the requested relation with units",
        "relate the graph/animation to the physical meaning",
        "verify the result against the observed behavior",
    ],
})
SUBJECT_TEACHING_ENGINES["chemistry"].update({
    "acid_base": [
        "identify the given species/solution information",
        "separate observation from acid-base interpretation",
        "write only evidence-supported species/reactions",
        "track the relevant transfer/equilibrium visually",
        "calculate with units and definitions visible",
        "check chemical and charge consistency",
    ],
    "redox": [
        "identify the species before and after change",
        "track oxidation states/electron transfer only when supported",
        "separate oxidation from reduction",
        "balance the verified transformation systematically",
        "check atoms and charge",
        "connect the symbolic equation to the observed process",
    ],
    "organic": [
        "identify the verified functional group/structure",
        "show the structural change visually",
        "name the reaction/property only when supported",
        "track atoms/groups through the transformation",
        "write the verified equation or product",
        "check structure and conservation",
    ],
    "quantitative": [
        "list the measured/given quantities with units",
        "identify the exact amount-of-substance relation",
        "convert units before substitution",
        "calculate symbolically then numerically",
        "connect the number to the chemical meaning",
        "check units and conservation",
    ],
})
SUBJECT_TEACHING_ENGINES["biology"].update({
    "cell": [
        "zoom from whole structure to the verified cell component",
        "identify each labelled part before naming a function",
        "connect structure to function one relation at a time",
        "animate transport/process only when evidence supports it",
        "summarize the cell-level relationship",
        "check by asking the learner to locate or explain one part",
    ],
    "genetics": [
        "identify the given genetic entities and generations/data",
        "separate observation/data from inheritance interpretation",
        "track chromosomes/alleles/process stages visually when supported",
        "build the reasoning chain without skipping a generation or condition",
        "verify ratios/conclusions against the supplied data",
        "finish with one transfer question",
    ],
    "physiology": [
        "locate the organ/structure in the system",
        "follow the verified path of matter/signal/process",
        "connect each structure to its role",
        "explain causal links in order",
        "compare states only when evidence supports the comparison",
        "check the whole pathway from start to finish",
    ],
    "ecology": [
        "identify organisms/populations/environmental factors",
        "map verified relationships visually",
        "follow matter/energy/interaction in the supported direction",
        "interpret changes without inventing causes",
        "connect local relation to the system-level conclusion",
        "check using the same evidence map",
    ],
})


SECONDARY_YEAR_TEACHING = {
    10: {
        "stage": "first_secondary",
        "depth": "build the secondary-school model from prerequisite ideas; keep one new abstraction visible at a time",
        "assessment": "guided transfer before independent multi-step work",
    },
    11: {
        "stage": "second_secondary",
        "depth": "connect several representations and require explicit justification of each chosen law/property",
        "assessment": "multi-step application with an intermediate self-check",
    },
    12: {
        "stage": "third_secondary",
        "depth": "exam-ready synthesis: select the method independently, justify assumptions, and verify the final result rigorously",
        "assessment": "representative exam-style transfer after the concept is understood, never before",
    },
}


def _concept_teaching_text(concept: dict) -> str:
    return (
        str(concept.get("title") or "") + " " +
        str(concept.get("raw_text") or "")
    ).casefold()


def _subject_teaching_mode(concept: dict, subject: str) -> str:
    """Choose a PEDAGOGICAL mode only; this never creates subject facts."""
    text = _concept_teaching_text(concept)
    if subject == "mathematics":
        return _mathematics_teaching_mode(concept)
    if subject == "physics":
        if re.search(r"motion|velocity|speed|acceleration|force|energy|momentum|mouvement|vitesse|accélération|force|énergie|حركة|سرعة|تسارع|قوة|طاقة", text):
            return "mechanics"
        if re.search(r"circuit|current|voltage|resistance|electric|circuit|courant|tension|résistance|دارة|تيار|توتر|جهد|مقاومة|كهرب", text):
            return "electricity"
        if re.search(r"light|mirror|lens|reflection|refraction|optics|lumière|miroir|lentille|réflexion|réfraction|ضوء|مرآة|عدسة|انعكاس|انكسار|بصري", text):
            return "optics"
        if re.search(r"wave|frequency|period|sound|onde|fréquence|période|son|موجة|تواتر|تردد|دور|صوت", text):
            return "waves"
    if subject == "chemistry":
        if re.search(r"acid|base|ph|acide|base|حمض|قاعدة", text):
            return "acid_base"
        if re.search(r"oxid|reduc|redox|electro|أكسد|اختزال|كهروكيمي", text):
            return "redox"
        if re.search(r"organic|hydrocarbon|alcohol|ester|organique|hydrocarbure|alcool|عضوي|هيدروكربون|كحول|إستر", text):
            return "organic"
        if re.search(r"mole|stoich|molar|amount of substance|quantité de matière|مول|ستوكيومتر|كمية المادة", text):
            return "quantitative"
    if subject == "biology":
        if re.search(r"cell|membrane|organelle|cellule|membrane|خلية|غشاء|عضية", text):
            return "cell"
        if re.search(r"gene|dna|chromosome|inherit|gène|adn|chromosome|hérédit|جين|وراث|صبغي|كروموسوم", text):
            return "genetics"
        if re.search(r"organ|system|blood|respir|digest|nerve|organe|système|sang|تنفس|هضم|عصب|عضو|جهاز|دم", text):
            return "physiology"
        if re.search(r"ecosystem|ecology|population|food chain|écosystème|écologie|سلسلة غذائية|نظام بيئي|بيئة", text):
            return "ecology"
    return "default"


def _mathematics_teaching_mode(concept: dict) -> str:
    text = _concept_teaching_text(concept)
    if re.search(
        r"triangle|circle|angle|tangent|parallel|perpendicular|"
        r"midpoint|bisector|congruen|similar|polygon|geometry|"
        r"مثلث|دائرة|زاوية|مماس|متواز|عمود|منتصف|منصف|هندس",
        text,
    ):
        return "geometry"
    if re.search(
        r"function|fonction|domain|domaine|limit|limite|derivative|"
        r"dérivée|asymptote|variation|graph|دال|نهاية|مشتق|مقارب",
        text,
    ):
        return "functions"
    if re.search(
        r"trigon|sine|cosine|tangent ratio|sinus|cosinus|trigonom|"
        r"جيب|جيب تمام|مثلثات",
        text,
    ):
        return "trigonometry"
    if re.search(
        r"vector|coordinate|analytic geometry|droite|repère|vecteur|"
        r"متجه|إحداثي|معلم|مستقيم",
        text,
    ):
        return "vectors_analytic_geometry"
    if re.search(
        r"sequence|suite|recurrence|récurrence|متتالية|تراجعية",
        text,
    ):
        return "sequences"
    if re.search(
        r"complex number|nombre complexe|affix|module|argument|"
        r"عدد مركب|لاحقة|مطال",
        text,
    ):
        return "complex_numbers"
    if re.search(
        r"probability|probabilité|statistics|statistique|mean|median|"
        r"احتمال|إحصاء|متوسط|وسيط",
        text,
    ):
        return "statistics_probability"
    if re.search(
        r"equation|inequality|factor|expand|polynomial|identity|"
        r"معادلة|متراجحة|تحليل|نشر|كثير حدود",
        text,
    ):
        return "algebra"
    return "default"


def resolve_teaching_signature(concept: dict, profile: dict) -> dict:
    subject = profile["subject"]
    level = profile["level"]
    level_spec = TEACHING_ENGINE_PROFILES[level]
    subject_spec = SUBJECT_TEACHING_ENGINES[subject]
    mode = _subject_teaching_mode(concept, subject)
    sequence = subject_spec.get(mode) or subject_spec["default"]
    grade = int(profile.get("grade") or 0)
    secondary_year = SECONDARY_YEAR_TEACHING.get(grade) if level == "L3" else None
    return {
        "level": level,
        "learner": level_spec["learner"],
        "pace": level_spec["pace"],
        "teacher_moves": list(level_spec["teacher_moves"]),
        "subject": subject,
        "mode": mode,
        "subject_sequence": list(sequence),
        "secondary_year_contract": dict(secondary_year) if secondary_year else None,
        "autonomous_teacher": True,
        "human_teacher_required": False,
    }



def build_teaching_steps(
        concept: dict, narrative: dict, profile: dict,
        lab_spec: Optional[dict] = None) -> list:
    """Build the student-facing teaching sequence without adding new science.

    The scientific sentences are reused from the already source-audited
    narrative or from the evidence-locked GEOMETRY_PROOF steps.  This function
    decides only pedagogical order/labels for the learner's age and subject.
    """
    sig = resolve_teaching_signature(concept, profile)
    lang = resolve_lang_code(profile["language"])
    subject = sig["subject"]
    mode = sig["mode"]
    concept_id = str(concept.get("concept_id") or "")
    source_page = concept.get("source_page")
    lab_key = f"concept:{concept_id}"

    if isinstance(lab_spec, dict) and str(lab_spec.get("kind") or "").upper() == "GEOMETRY_PROOF":
        out = []
        for idx, proof in enumerate(lab_spec.get("proof_steps") or [], 1):
            sentence = str(proof.get("text") or "").strip()
            if not sentence:
                continue
            out.append({
                "step_id": f"{concept_id}-S{idx:02d}",
                "concept_id": concept_id,
                "kind": "reasoning",
                "order": idx,
                "label": str(proof.get("title") or "").strip(),
                "sentence": sentence,
                "formula": str(proof.get("formula") or "").strip(),
                "evidence": {
                    "concept_id": concept_id,
                    "source_page": source_page,
                    "quote": str(proof.get("evidence_quote") or "").strip(),
                },
                "visual_cues": [{
                    "cue_type": "proof_visual_marks",
                    "target_ids": [str(v) for v in proof.get("target_ids") or []],
                    "reveal_marks": [str(v) for v in proof.get("reveal_marks") or []],
                }],
                "lab_key": lab_key,
            })
        if out:
            return out

    labels = {
        "ar": {
            "math_geometry": ["المعطيات", "ابنِ الفكرة", "لاحظ", "فكّر في السبب", "استنتج"],
            "math_functions": ["ابدأ من الدالة", "ادرس", "لاحظ العلاقة", "فسّر", "استنتج"],
            "math_algebra": ["حدّد المطلوب", "نفّذ خطوة", "لاحظ", "لماذا هذه الخطوة صحيحة؟", "النتيجة"],
            "math_default": ["ابدأ من المعطى", "جرّب", "لاحظ", "فكّر", "استنتج"],
            "physics": ["شاهد الظاهرة", "جرّب", "لاحظ", "فسّر", "استنتج القانون أو القاعدة"],
            "chemistry": ["ابدأ من التغيّر", "جرّب أو تتبّع", "لاحظ", "فسّر على المستوى الجسيمي", "استنتج"],
            "biology": ["لاحظ", "تتبّع البنية أو العملية", "ما الوظيفة؟", "فسّر العلاقة", "استنتج"],
            "general_science": ["لاحظ الظاهرة", "اختبر", "سجّل الملاحظة", "فسّر", "استنتج"],
        },
        "fr": {
            "math_geometry": ["Données", "Construis l’idée", "Observe", "Justifie", "Conclus"],
            "math_functions": ["Pars de la fonction", "Étudie", "Observe la relation", "Interprète", "Conclus"],
            "math_algebra": ["Identifie l’objectif", "Transforme", "Observe", "Justifie", "Résultat"],
            "math_default": ["Pars des données", "Essaie", "Observe", "Réfléchis", "Conclus"],
            "physics": ["Observe le phénomène", "Expérimente", "Observe", "Interprète", "Énonce la loi ou la règle"],
            "chemistry": ["Pars du changement", "Expérimente", "Observe", "Interprète au niveau particulaire", "Conclus"],
            "biology": ["Observe", "Repère la structure ou le processus", "Quelle fonction ?", "Interprète la relation", "Conclus"],
            "general_science": ["Observe le phénomène", "Teste", "Note l’observation", "Interprète", "Conclus"],
        },
        "en": {
            "math_geometry": ["Givens", "Build the idea", "Notice", "Why is this valid?", "Conclude"],
            "math_functions": ["Start from the function", "Study", "Notice the relation", "Interpret", "Conclude"],
            "math_algebra": ["Identify the target", "Transform", "Notice", "Why is this valid?", "Result"],
            "math_default": ["Start from the givens", "Try", "Notice", "Think", "Conclude"],
            "physics": ["See the phenomenon", "Try the experiment", "Observe", "Explain", "State the law or rule"],
            "chemistry": ["Start from the change", "Try or trace", "Observe", "Interpret at particle level", "Conclude"],
            "biology": ["Observe", "Trace the structure or process", "What is its function?", "Explain the relation", "Conclude"],
            "general_science": ["Observe the phenomenon", "Test", "Record the observation", "Explain", "Conclude"],
        },
    }
    labels["ar"].update({
        "language": ["اقرأ في السياق", "جرّب", "لاحظ النمط", "فسّر", "استنتج القاعدة"],
        "history": ["حدّد السياق", "رتّب الأدلة", "لاحظ", "فسّر العلاقة", "ركّب الخلاصة"],
        "geography": ["اقرأ الخريطة أو البيانات", "قارن", "لاحظ النمط", "فسّر", "استنتج"],
        "civics": ["ابدأ من الحالة", "حدّد المفهوم", "طبّق القاعدة", "فسّر", "استنتج"],
        "philosophy": ["اطرح الإشكالية", "حدّد المفاهيم", "حلّل الحجة", "اختبر الترابط", "ركّب الخلاصة"],
        "social_science": ["اقرأ المعطيات", "نظّمها", "لاحظ العلاقة", "فسّر", "استنتج"],
        "computer_science": ["حدّد المطلوب", "تتبّع الخطوات", "لاحظ تغيّر الحالة", "فسّر", "استنتج الطريقة"],
    })
    labels["fr"].update({
        "language": ["Lis en contexte", "Essaie", "Observe le modèle", "Explique", "Formule la règle"],
        "history": ["Situe le contexte", "Ordonne les preuves", "Observe", "Interprète", "Synthétise"],
        "geography": ["Lis la carte ou les données", "Compare", "Observe", "Interprète", "Conclus"],
        "civics": ["Pars de la situation", "Identifie le concept", "Applique la règle", "Explique", "Conclus"],
        "philosophy": ["Pose la problématique", "Définis les concepts", "Analyse l’argument", "Vérifie le raisonnement", "Synthétise"],
        "social_science": ["Lis les données", "Organise", "Observe la relation", "Interprète", "Conclus"],
        "computer_science": ["Identifie l’objectif", "Trace les étapes", "Observe l’état", "Explique", "Dégage la méthode"],
    })
    labels["en"].update({
        "language": ["Read in context", "Try", "Notice the pattern", "Explain", "State the rule"],
        "history": ["Set the context", "Order the evidence", "Notice", "Interpret", "Synthesize"],
        "geography": ["Read the map or data", "Compare", "Notice the pattern", "Interpret", "Conclude"],
        "civics": ["Start from the case", "Identify the concept", "Apply the rule", "Explain", "Conclude"],
        "philosophy": ["State the problem", "Define the concepts", "Analyze the argument", "Test the reasoning", "Synthesize"],
        "social_science": ["Read the data", "Organize it", "Notice the relation", "Interpret", "Conclude"],
        "computer_science": ["Identify the target", "Trace the steps", "Notice the state", "Explain", "Extract the method"],
    })

    if subject == "mathematics":
        label_key = {
            "geometry": "math_geometry",
            "functions": "math_functions",
            "algebra": "math_algebra",
        }.get(mode, "math_default")
    else:
        label_key = {
            "arabic_language": "language",
            "english_language": "language",
            "french_language": "language",
            "history": "history",
            "geography": "geography",
            "civics": "civics",
            "philosophy": "philosophy",
            "economics": "social_science",
            "sociology": "social_science",
            "computer_science": "computer_science",
        }.get(subject, subject if subject in {
            "physics", "chemistry", "biology", "general_science"
        } else "general_science")
    display = labels.get(lang, labels["en"])[label_key]
    fields = [
        ("hook", "phenomenon"),
        ("student_try", "investigation"),
        ("observation", "observation"),
        ("reasoning", "interpretation"),
        ("law_or_rule", "conclusion"),
    ]
    out = []
    order = 0
    for pos, (kind, field) in enumerate(fields):
        sentence = str(narrative.get(field) or "").strip()
        if not sentence:
            continue
        order += 1
        out.append({
            "step_id": f"{concept_id}-S{order:02d}",
            "concept_id": concept_id,
            "kind": kind,
            "order": order,
            "label": display[pos],
            "sentence": sentence,
            "formula": "",
            "evidence": {
                "concept_id": concept_id,
                "source_page": source_page,
                "quote": str(concept.get("raw_text") or "")[:700],
            },
            "visual_cues": [{"cue_type": "point", "target_ids": []}],
            "lab_key": lab_key,
        })
    return out


def resolve_pedagogy_profile(entry: dict) -> dict:
    if "grade" not in entry or entry["grade"] is None:
        raise RuntimeError("CANONICAL_CATALOG_CORRUPT: Missing grade")
    if "language" not in entry or not str(entry["language"]).strip():
        raise RuntimeError("CANONICAL_CATALOG_CORRUPT: Missing mandatory field 'language'")

    grade = int(entry["grade"])
    subject_raw = entry.get("subject", "").strip()
    subject_key = subject_raw.lower().replace(" ", "_")
    subject = SUBJECT_ALIASES.get(subject_key, subject_key)

    if subject not in SUBJECT_PROFILES:
        raise RuntimeError(f"PEDAGOGY_PROFILE_MISMATCH: Unknown curriculum subject '{subject}'")

    level = "L1" if grade <= 6 else ("L2" if grade <= 9 else "L3")
    return {
        "level": level,
        "level_profile": PEDAGOGY_PROFILES[level],
        "subject": subject,
        "subject_raw": subject_raw,
        "subject_profile": SUBJECT_PROFILES[subject],
        "branch": entry.get("branch") or entry.get("track") or "",
        "language": entry["language"],
        "grade": grade,
    }


# ==============================================================================
# 3. LLM INFERENCE ENGINE (FAIL-CLOSED)
# ==============================================================================
_AI_PROVIDER_COOLDOWNS: Dict[str, float] = {}
_LAST_LLM_PROVENANCE: Dict[str, Any] = {}


def get_last_llm_provenance() -> Dict[str, Any]:
    """Return metadata for the provider/model that actually answered last."""
    return dict(_LAST_LLM_PROVENANCE)


def _provider_keys() -> Dict[str, Optional[str]]:
    return {
        "openrouter": os.getenv("OPENROUTER_API_KEY"),
        "groq": os.getenv("GROQ_API_KEY"),
        "openai": os.getenv("OPENAI_API_KEY"),
    }


def _provider_order(preferred: str, keys: Dict[str, Optional[str]]) -> List[str]:
    """Primary provider first, then configured failover providers, no duplicates."""
    valid = ("groq", "openrouter", "openai")
    if preferred not in ("auto", *valid):
        raise RuntimeError(f"AI_PROVIDER_INVALID: {preferred}")

    if preferred == "auto":
        primary = next(
            (name for name in ("openrouter", "groq", "openai")
             if keys.get(name)), None)
    else:
        primary = preferred

    if not primary or not keys.get(primary):
        raise RuntimeError(
            f"AI_PROVIDER_NOT_CONFIGURED: provider={primary or preferred}")

    raw = os.getenv(
        "NABIL_FACTORY_AI_FAILOVER_PROVIDERS",
        "openrouter,openai,groq",
    )
    requested = [
        token.strip().lower() for token in raw.split(",") if token.strip()
    ]
    invalid = [name for name in requested if name not in valid]
    if invalid:
        raise RuntimeError(
            "AI_PROVIDER_FAILOVER_INVALID: " + ",".join(invalid))

    order = [primary]
    for name in requested:
        if name not in order and keys.get(name):
            order.append(name)
    return order


def _vision_provider_authorized(provider: str, vision_context: Dict[str, Any],
                                require_key: bool = True) -> bool:
    """Check explicit owner consent for one provider/source page."""
    consent_path = ROOT / "data/nabil_vision_consent.json"
    if not consent_path.exists():
        return False
    lesson_id = str(vision_context.get("lesson_id") or "")
    book_id = str(vision_context.get("book_id") or "")
    try:
        pdf_page = int(vision_context.get("pdf_page"))
    except (TypeError, ValueError):
        return False
    try:
        scopes = json.loads(
            consent_path.read_text(encoding="utf-8")
        ).get("approved_scopes", [])
    except Exception:
        return False

    for item in scopes:
        lesson_allowed = (
            item.get("lesson_id") == lesson_id
            or bool(
                item.get("lesson_id_prefix")
                and lesson_id.startswith(item["lesson_id_prefix"])
            )
        )
        if (
            lesson_allowed
            and item.get("book_id") == book_id
            and item.get("provider") == provider
            and int(item["pdf_start_page"]) <= pdf_page
            <= int(item["pdf_end_page"])
        ):
            if require_key and not os.getenv(f"{provider.upper()}_API_KEY"):
                return False
            return True
    return False


def _provider_request_config(provider: str, image_base64: Optional[str]):
    keys = _provider_keys()
    api_key = keys.get(provider)
    if not api_key:
        raise RuntimeError(
            f"AI_PROVIDER_NOT_CONFIGURED: provider={provider}")
    if provider == "openrouter":
        url = "https://openrouter.ai/api/v1/chat/completions"
        model = (
            os.getenv("OPENROUTER_VISION_MODEL")
            if image_base64 else None
        ) or os.getenv(
            "OPENROUTER_TEXT_MODEL", "google/gemini-3.6-flash")
    elif provider == "groq":
        url = "https://api.groq.com/openai/v1/chat/completions"
        model = (
            os.getenv("GROQ_VISION_MODEL", "qwen/qwen3.8-27b")
            if image_base64
            else os.getenv(
                "GROQ_TEXT_MODEL", "llama-3.3-70b-versatile")
        )
    elif provider == "openai":
        url = "https://api.openai.com/v1/chat/completions"
        model = (
            os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini")
            if image_base64
            else os.getenv("OPENAI_TEXT_MODEL", "gpt-4o-mini")
        )
    else:
        raise RuntimeError(f"AI_PROVIDER_INVALID: {provider}")
    return api_key, url, model


def _parse_rate_limit_wait_seconds(exc, detail: str,
                                   provider_attempt: int) -> float:
    retry_header = str(exc.headers.get("Retry-After", "")).strip()
    try:
        retry_after = float(retry_header)
    except ValueError:
        retry_after = 0.0
    duration = re.search(
        r"(?i)try again in\s+"
        r"(?:(\d+(?:\.\d+)?)\s*h(?:ours?)?\s*)?"
        r"(?:(\d+(?:\.\d+)?)\s*m(?:in(?:utes?)?)?\s*)?"
        r"(?:(\d+(?:\.\d+)?)\s*s(?:ec(?:onds?)?)?)?",
        detail,
    )
    indicated = 0.0
    if duration and any(
            group is not None for group in duration.groups()):
        hours, minutes, seconds = duration.groups()
        indicated = (
            3600 * float(hours or 0)
            + 60 * float(minutes or 0)
            + float(seconds or 0)
        )
    return max(
        retry_after,
        indicated,
        min(20.0 * max(1, provider_attempt), 90.0),
    ) + 2.0


def _next_provider_or_wait(candidates: List[str],
                           cooldowns: Dict[str, float],
                           now_mono: float):
    """Pure scheduling helper: use an available provider or shortest cooldown."""
    available = [
        p for p in candidates if cooldowns.get(p, 0.0) <= now_mono
    ]
    if available:
        return "provider", available[0], 0.0
    earliest = min(candidates, key=lambda p: cooldowns.get(p, now_mono))
    wait = max(0.0, cooldowns.get(earliest, now_mono) - now_mono)
    return "wait", earliest, wait


def _sanitize_provider_error(exc):
    try:
        raw_body = exc.read(4096).decode("utf-8", errors="replace")
    except OSError:
        raw_body = ""
    content_type = str(
        exc.headers.get("Content-Type", "")
    ).split(";")[0].lower()
    detail, code = "", ""
    if raw_body:
        try:
            upstream = json.loads(raw_body)
            error = (
                upstream.get("error", upstream)
                if isinstance(upstream, dict) else {}
            )
            if isinstance(error, dict):
                detail = str(
                    error.get("message") or error.get("detail") or "")
                code = str(
                    error.get("code") or error.get("type") or "")
            elif isinstance(error, str):
                detail = error
        except ValueError:
            detail = re.sub(r"<[^>]+>", " ", raw_body)
    detail = re.sub(r"\s+", " ", detail).strip()
    code = re.sub(r"\s+", " ", code).strip()
    if not detail:
        detail = (
            "Empty or unrecognized provider response "
            f"(content_type={content_type or 'not-provided'})"
        )
    for secret_name in (
        "OPENROUTER_API_KEY", "OPENAI_API_KEY", "GROQ_API_KEY"
    ):
        secret = os.getenv(secret_name, "")
        if secret and len(secret) >= 8:
            detail = detail.replace(secret, "[REDACTED]")
            code = code.replace(secret, "[REDACTED]")
    detail = re.sub(
        r"(?i)\b(?:sk-or-v1-|sk-)[a-z0-9_-]{8,}",
        "[REDACTED]", detail)
    code = re.sub(
        r"(?i)\b(?:sk-or-v1-|sk-)[a-z0-9_-]{8,}",
        "[REDACTED]", code)
    return detail, code


def execute_llm_completion(
        prompt: str,
        json_mode: bool = True,
        temperature: float = 0.0,
        image_base64: Optional[str] = None,
        vision_context: Optional[Dict[str, Any]] = None,
        preferred_provider_override: Optional[str] = None,
        excluded_providers: Optional[set] = None) -> str:
    """Execute with rate-limit failover while preserving source consent.

    A 429 never sleeps on one provider while another configured, explicitly
    authorized provider is available. If every candidate is cooling down, wait
    only for the shortest cooldown; if that shortest wait is still too long,
    fail fast so durable checkpoints can be resumed later instead of burning a
    Railway session idling.
    """
    global _LAST_LLM_PROVENANCE

    preferred = (
        preferred_provider_override
        or os.getenv("NABIL_FACTORY_AI_PROVIDER", "auto")
    ).strip().lower()
    keys = _provider_keys()
    candidates = _provider_order(preferred, keys)

    # Source images may move between providers ONLY when the owner explicitly
    # approved that exact lesson/book/page for each fallback provider.
    if image_base64:
        if vision_context is None:
            candidates = candidates[:1]
        else:
            candidates = [
                p for p in candidates
                if _vision_provider_authorized(
                    p, vision_context, require_key=True)
            ]
            if not candidates:
                raise RuntimeError(
                    "VISION_SHARING_NOT_AUTHORIZED: no configured provider "
                    "is approved for this source page")
    if excluded_providers:
        excluded = {str(p).strip().lower() for p in excluded_providers}
        candidates = [p for p in candidates if p not in excluded]
        if not candidates:
            raise RuntimeError(
                "AI_PROVIDER_POOL_EXHAUSTED_AFTER_JSON_FAILURES:"
                + ",".join(sorted(excluded)))

    primary = candidates[0]
    progress(
        "AI_PROVIDER_FAILOVER_POOL",
        primary=primary,
        candidates=candidates,
        image_request=bool(image_base64),
        vision_context=vision_context if image_base64 else None,
    )

    max_requests = max(
        3, min(30, int(os.getenv(
            "NABIL_FACTORY_MAX_FAILOVER_REQUESTS", "12"))))
    # A temporary 429 on the last healthy provider must not discard a lesson
    # that has already completed expensive OCR/vision work.  Keep this bounded
    # and configurable; long quota quarantines still lose to the shortest
    # healthy-provider cooldown selected by _next_provider_or_wait().
    max_all_wait = max(
        0.0, min(1800.0, float(os.getenv(
            "NABIL_FACTORY_MAX_ALL_PROVIDER_WAIT_SECONDS", "300"))))
    provider_attempts = {p: 0 for p in candidates}
    total_requests = 0

    while total_requests < max_requests:
        now_mono = time.monotonic()
        mode, provider, wait_seconds = _next_provider_or_wait(
            candidates, _AI_PROVIDER_COOLDOWNS, now_mono)

        if mode == "wait":
            if wait_seconds > max_all_wait:
                remaining = {
                    p: round(max(
                        0.0,
                        _AI_PROVIDER_COOLDOWNS.get(p, now_mono)
                        - now_mono), 2)
                    for p in candidates
                }
                progress(
                    "AI_ALL_PROVIDERS_COOLING_DOWN_FAIL_FAST",
                    candidates=candidates,
                    remaining_seconds=remaining,
                    shortest_provider=provider,
                    shortest_wait_seconds=round(wait_seconds, 2),
                    max_all_provider_wait_seconds=max_all_wait,
                )
                raise RuntimeError(
                    "AI_ALL_PROVIDERS_COOLING_DOWN: "
                    f"shortest_provider={provider} "
                    f"wait_seconds={wait_seconds:.1f} "
                    f"remaining={remaining}")
            progress(
                "AI_ALL_PROVIDERS_COOLING_DOWN_WAIT_SHORTEST",
                provider=provider,
                wait_seconds=round(wait_seconds, 2),
                candidates=candidates,
            )
            time.sleep(wait_seconds + 0.25)
            continue

        provider_attempts[provider] += 1
        total_requests += 1
        api_key, url, model = _provider_request_config(
            provider, image_base64)

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "NABIL-AI-Lesson-Factory/1.0",
        }
        messages_content = [{"type": "text", "text": prompt}]
        if image_base64:
            messages_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{image_base64}"
                },
            })
        payload = {
            "model": model,
            "messages": [{
                "role": "user",
                "content": (
                    messages_content if image_base64 else prompt)
            }],
            "temperature": temperature,
            # OpenRouter may otherwise assume a very large provider maximum
            # (for Gemini 3.6 Flash this can be 65k+ output tokens), which can
            # trigger a 402 credit preflight even for a tiny JSON response.
            # Keep factory calls bounded and configurable.
            "max_tokens": max(
                256,
                min(
                    8192,
                    int(os.getenv(
                        "NABIL_FACTORY_VISION_MAX_OUTPUT_TOKENS"
                        if image_base64
                        else "NABIL_FACTORY_TEXT_MAX_OUTPUT_TOKENS",
                        "2048" if image_base64 else "4096",
                    )),
                ),
            ),
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
        )

        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                content = data["choices"][0]["message"]["content"].strip()
                if content.startswith("```"):
                    content = re.sub(
                        r"^```(?:json)?\s*|\s*```$",
                        "", content, flags=re.I).strip()
                _LAST_LLM_PROVENANCE = {
                    "provider": provider,
                    "model": model,
                    "primary_provider": primary,
                    "used_failover": provider != primary,
                    "request_index": total_requests,
                    "provider_attempt": provider_attempts[provider],
                    "completed_at": now(),
                }
                if provider != primary:
                    progress(
                        "AI_PROVIDER_FAILOVER_SUCCESS",
                        primary=primary,
                        actual_provider=provider,
                        model=model,
                        request_index=total_requests,
                    )
                return content
        except urllib.error.HTTPError as exc:
            detail, code = _sanitize_provider_error(exc)
            if exc.code == 429:
                terminal_quota_tokens = (
                    "credit_balance_exhausted",
                    "insufficient_quota",
                    "billing_hard_limit_reached",
                    "billing_not_active",
                    "payment_required",
                )
                combined_error = (code + " " + detail).casefold()
                if any(token in combined_error
                       for token in terminal_quota_tokens):
                    quarantine_seconds = 86400.0
                    _AI_PROVIDER_COOLDOWNS[provider] = (
                        time.monotonic() + quarantine_seconds)
                    ready_alternatives = [
                        p for p in candidates
                        if p != provider
                        and _AI_PROVIDER_COOLDOWNS.get(p, 0.0)
                        <= time.monotonic()
                    ]
                    progress(
                        "AI_PROVIDER_QUOTA_EXHAUSTED_FAILOVER",
                        provider=provider,
                        model=model,
                        provider_attempt=provider_attempts[provider],
                        total_requests=total_requests,
                        quarantine_seconds=quarantine_seconds,
                        ready_alternatives=ready_alternatives,
                        provider_code=code[:80],
                    )
                    continue

                cooldown = _parse_rate_limit_wait_seconds(
                    exc, detail, provider_attempts[provider])
                max_provider_wait = max(
                    30.0, min(3600.0, float(os.getenv(
                        "NABIL_FACTORY_MAX_RATE_LIMIT_WAIT_SECONDS",
                        "1800"))))
                if cooldown > max_provider_wait:
                    # Treat a very long provider cooldown as unavailable for
                    # this run; the other providers still get an immediate try.
                    cooldown = max_provider_wait
                _AI_PROVIDER_COOLDOWNS[provider] = (
                    time.monotonic() + cooldown)
                next_now = time.monotonic()
                ready_alternatives = [
                    p for p in candidates
                    if p != provider
                    and _AI_PROVIDER_COOLDOWNS.get(p, 0.0) <= next_now
                ]
                progress(
                    "AI_PROVIDER_RATE_LIMIT_FAILOVER",
                    provider=provider,
                    model=model,
                    provider_attempt=provider_attempts[provider],
                    total_requests=total_requests,
                    cooldown_seconds=round(cooldown, 2),
                    ready_alternatives=ready_alternatives,
                    provider_code=code[:80],
                )
                continue

            if exc.code in (408, 425, 500, 502, 503, 504):
                transient_cooldown = 10.0
                _AI_PROVIDER_COOLDOWNS[provider] = (
                    time.monotonic() + transient_cooldown)
                progress(
                    "AI_PROVIDER_TRANSIENT_FAILOVER",
                    provider=provider,
                    model=model,
                    http_status=exc.code,
                    cooldown_seconds=transient_cooldown,
                    provider_code=code[:80],
                )
                continue

            if exc.code == 402 and "in-flight requests" in detail.casefold():
                transient_cooldown = 3.0
                _AI_PROVIDER_COOLDOWNS[provider] = (
                    time.monotonic() + transient_cooldown)
                progress(
                    "AI_PROVIDER_INFLIGHT_LIMIT_RETRY",
                    provider=provider,
                    model=model,
                    http_status=exc.code,
                    cooldown_seconds=transient_cooldown,
                    detail=detail[:240],
                )
                continue

            if exc.code in (400, 401, 402, 403, 404, 422):
                quarantine_seconds = 3600.0
                _AI_PROVIDER_COOLDOWNS[provider] = (
                    time.monotonic() + quarantine_seconds)
                ready_alternatives = [
                    p for p in candidates
                    if p != provider
                    and _AI_PROVIDER_COOLDOWNS.get(p, 0.0)
                    <= time.monotonic()
                ]
                progress(
                    "AI_PROVIDER_UNAVAILABLE_FAILOVER",
                    provider=provider,
                    model=model,
                    http_status=exc.code,
                    quarantine_seconds=quarantine_seconds,
                    ready_alternatives=ready_alternatives,
                    provider_code=code[:80],
                    detail=detail[:240],
                )
                continue

            reason = detail[:360]
            progress(
                "AI_PROVIDER_REQUEST_REJECTED",
                provider=provider,
                model=model,
                http_status=exc.code,
                provider_code=code[:80],
                detail=reason,
            )
            raise RuntimeError(
                "AI_PROVIDER_HTTP_ERROR: "
                f"provider={provider} model={model} "
                f"http_status={exc.code} "
                f"provider_code={code[:80]} detail={reason}"
            ) from None
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            _AI_PROVIDER_COOLDOWNS[provider] = time.monotonic() + 10.0
            progress(
                "AI_PROVIDER_NETWORK_FAILOVER",
                provider=provider,
                model=model,
                error_type=type(exc).__name__,
                cooldown_seconds=10.0,
            )
            continue

    remaining = {
        p: round(max(
            0.0, _AI_PROVIDER_COOLDOWNS.get(p, 0.0)
            - time.monotonic()), 2)
        for p in candidates
    }
    raise RuntimeError(
        "AI_PROVIDER_FAILOVER_EXHAUSTED: "
        f"requests={total_requests} remaining={remaining}")


# ==============================================================================
# 4. MATHEMATICAL RENDERING ENGINE (PURE PLAIN-TEXT MATHJAX URL)
# ==============================================================================
class MathRenderingEngine:
    @staticmethod
    def render_inline(expr: str) -> str:
        return f"\\({expr.strip()}\\)"

    @staticmethod
    def render_display(expr: str) -> str:
        return f"\\[\n{expr.strip()}\n\\]"

    @staticmethod
    def normalize_math(text: str, source_page: int, bbox: List[float], image_ref: str) -> Tuple[str, bool, List[Dict[str, Any]]]:
        if not text:
            return text, True, []

        verified = True
        math_records = []

        for m in re.finditer(r'(?<!\w)(\d+|[a-zA-Z])\s*/\s*(\d+|[a-zA-Z])(?!\w)', text):
            math_records.append({
                "raw": m.group(0),
                "raw_source_text": text,
                "normalized_math": f"\\frac{{{m.group(1)}}}{{{m.group(2)}}}",
                "latex": f"\\frac{{{m.group(1)}}}{{{m.group(2)}}}",
                "verified": True,
                "source_page": source_page,
                "source_bbox": bbox,
                "source_image_ref": image_ref,
                "verification_status": "VERIFIED"
            })

        for m in re.finditer(r'\b([a-zA-Z])\s*=\s*([^,\n\.]+)', text):
            raw_eq = m.group(0)
            is_balanced = raw_eq.count('(') == raw_eq.count(')') and raw_eq.count('{') == raw_eq.count('}')
            status = "VERIFIED" if is_balanced else "MATH_EXPRESSION_UNVERIFIED"
            math_records.append({
                "raw": raw_eq,
                "raw_source_text": text,
                "normalized_math": f"{m.group(1)} = {m.group(2).strip()}",
                "latex": f"{m.group(1)} = {m.group(2).strip()}",
                "verified": is_balanced,
                "source_page": source_page,
                "source_bbox": bbox,
                "source_image_ref": image_ref,
                "verification_status": status
            })
            if not is_balanced:
                verified = False

        try:
            text = re.sub(r'\(\s*([^()]+)\s*\)\s*/\s*\(\s*([^()]+)\s*\)', r'\\(\\frac{\1}{\2}\\)', text)
            text = re.sub(r'(?<!\w)(\d+|[a-zA-Z])\s*/\s*(\d+|[a-zA-Z])(?!\w)', r'\\(\\frac{\1}{\2}\\)', text)
            text = re.sub(r'\bsqrt\s*\(\s*([^()]+)\s*\)', r'\\(\\sqrt{\1}\\)', text)
            text = re.sub(r'\broot\[\s*(\d+)\s*\]\s*\(\s*([^()]+)\s*\)', r'\\(\\sqrt[\1]{\2}\\)', text)
            text = re.sub(r'\blim_\{\s*([^}]+)\s*\}', r'\\(\\lim_{\1}\\)', text)
            text = re.sub(r'\bint\s+([^$]+?)\s+d([a-zA-Z])\b', r'\\(\\int \1 \\, d\2\\)', text)
            text = re.sub(r'\bvec\(\s*([a-zA-Z]{1,2})\s*\)', r'\\(\\vec{\1}\\)', text)
            text = re.sub(r'\b(cm|m|mm|kg|g|s|mol|N|J|W|Pa)3\b', r'\1\\(^3\\)', text)
            text = re.sub(r'\b(cm|m|mm|kg|g|s|mol|N|J|W|Pa)2\b', r'\1\\(^2\\)', text)
            text = re.sub(r'\b([a-zA-Z])\^(\d+|\{[^}]+\})', r'\1\\(^{\2}\\)', text)
            text = re.sub(r'\b([A-Z][a-z]?)(\d+)\b', r'\1\\(_{\2}\\)', text)
            text = re.sub(r'\s*->\s*', r' \\(\\rightarrow\\) ', text)
        except Exception:
            verified = False

        return text, verified, math_records

    @staticmethod
    def inject_mathjax_head() -> str:
        return '''<script>
window.MathJax = {
  tex: { inlineMath: [['\\\\(', '\\\\)']], displayMath: [['\\\\[', '\\\\]']], processEscapes: true },
  options: { renderActions: { addMenu: [] } },
  chtml: { scale: 0.95 }
};
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
'''


# ==============================================================================
# 5. PREFLIGHT & DRIVE SERVICE (PURE PLAIN-TEXT SCOPES)
# ==============================================================================
def execute_preflight_checks(require_drive: bool = False) -> Dict[str, Any]:
    progress("PREFLIGHT: Executing universal runtime verification...")
    report = {"status": "PASS", "dependencies": {}}

    required = [("pypdf", "pypdf"), ("PIL", "Pillow"), ("googleapiclient", "google-api-python-client"), ("google.auth", "google-auth"), ("playwright", "playwright")]
    for mod, pkg in required:
        try:
            __import__(mod)
            report["dependencies"][pkg] = True
        except ImportError:
            report["dependencies"][pkg] = False
            raise RuntimeError(f"DEPENDENCY_MISSING:{pkg}")

    try:
        import fitz
        report["dependencies"]["PyMuPDF"] = True
    except ImportError:
        report["dependencies"]["PyMuPDF"] = False
        raise RuntimeError("DEPENDENCY_MISSING:PyMuPDF")

    if require_drive:
        root_id = resolve_drive_root_id()
        try:
            service = get_drive_service()
            about = service.about().get(fields="user(emailAddress)").execute()
            report["drive_user"] = about.get("user", {}).get("emailAddress")
        except Exception as e:
            raise RuntimeError(f"DRIVE_AUTH_FAILED:{e}")

    for d in [PERM_EVIDENCE_DIR, CACHE_DIR, OUT_DIR, ARTIFACTS_DIR]:
        d.mkdir(parents=True, exist_ok=True)
        if not os.access(d, os.W_OK):
            raise RuntimeError(f"CANNOT_WRITE_DIR:{d}")

    progress("PREFLIGHT: Universal environment verified.")
    return report


def get_drive_service():
    """Use the owner's OAuth credentials for uploads to their personal My Drive.

    A service account can read shared source PDFs but cannot own uploaded files
    in personal Drive, even if shared as Editor. Keep tokens in Railway secrets;
    never commit them to the repository.
    """
    from googleapiclient.discovery import build
    from google.oauth2 import service_account
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request

    scopes = ["https://www.googleapis.com/auth/drive"]
    # Preserve the owner's ORIGINAL three-variable Railway OAuth workflow.
    # These names were used by the preceding NABIL lesson factory; do not
    # require a new consent flow if a working refresh token already exists.
    owner_keys = (
        "GOOGLE_DRIVE_OAUTH_CLIENT_ID",
        "GOOGLE_DRIVE_OAUTH_CLIENT_SECRET",
        "GOOGLE_DRIVE_OAUTH_REFRESH_TOKEN",
    )
    owner_values = [os.getenv(name, "").strip() for name in owner_keys]
    if all(owner_values):
        credentials = Credentials(
            token=None,
            refresh_token=owner_values[2],
            token_uri="https://oauth2.googleapis.com/token",
            client_id=owner_values[0],
            client_secret=owner_values[1],
            scopes=scopes,
        )
        credentials.refresh(Request())
        return build("drive", "v3", credentials=credentials,
                     cache_discovery=False)

    raw_oauth = os.getenv("NABIL_DRIVE_OAUTH_TOKEN_JSON", "").strip()
    if any(owner_values) and not raw_oauth:
        missing = [name for name, value in zip(owner_keys, owner_values) if not value]
        raise RuntimeError("OWNER_DRIVE_OAUTH_INCOMPLETE: missing " + ",".join(missing))
    if raw_oauth:
        try:
            info = json.loads(raw_oauth)
            creds = Credentials.from_authorized_user_info(info, scopes=scopes)
            if not creds.valid and creds.refresh_token:
                creds.refresh(Request())
            if not creds.valid:
                raise RuntimeError("NABIL_DRIVE_OAUTH_REFRESH_REQUIRED")
        except (ValueError, KeyError, TypeError) as exc:
            raise RuntimeError("NABIL_DRIVE_OAUTH_TOKEN_INVALID: check Railway secret JSON") from exc
        return build("drive", "v3", credentials=creds, cache_discovery=False)

    # Keep existing read-only source access for index-only operations.
    try:
        from scripts.index_books import get_drive_service as base_get_drive
        return base_get_drive()
    except Exception:
        pass

    paths = [
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "").strip(),
        str(ROOT / "drive_service_account.json"),
        str(ROOT / "credentials.json"),
    ]
    path = next((p for p in paths if p and Path(p).is_file()), None)
    if path:
        creds = service_account.Credentials.from_service_account_file(
            path, scopes=scopes)
    else:
        import google.auth
        creds, _ = google.auth.default(scopes=scopes)
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def resolve_drive_root_id() -> str:
    root_id = os.getenv("NABIL_CURRICULUM_ROOT_ID",
                        os.getenv("NABIL_INTERACTIVE_CURRICULUM_ROOT_ID",
                                  os.getenv("NABIL_LESSON_DRIVE_ROOT", ""))).strip()
    if not root_id:
        raise RuntimeError("NABIL_CURRICULUM_ROOT_ID_NOT_CONFIGURED: Set NABIL_CURRICULUM_ROOT_ID in environment.")
    return root_id


def resolve_source_book_pdf(book_id: str, drive_service=None) -> Path:
    cache_dir = Path("/tmp/nabil_source_books")
    cache_dir.mkdir(parents=True, exist_ok=True)
    target = cache_dir / f"{book_id}.pdf"

    if target.exists() and target.stat().st_size > 20000:
        try:
            import fitz
            doc = fitz.open(str(target))
            if len(doc) >= 1:
                doc.close()
                return target
            doc.close()
        except Exception:
            target.unlink(missing_ok=True)

    candidates = [Path(f"/app/data/books/{book_id}.pdf"), Path(f"/app/books/{book_id}.pdf"), Path(f"data/books/{book_id}.pdf"), Path(f"{book_id}.pdf")]
    for c in candidates:
        if c.exists() and c.stat().st_size > 20000:
            try:
                import fitz
                doc = fitz.open(str(c))
                if len(doc) >= 1:
                    doc.close()
                    shutil.copy2(c, target)
                    return target
                doc.close()
            except Exception:
                pass

    if not drive_service:
        drive_service = get_drive_service()

    progress("DOWNLOADING_SOURCE_PDF", file_id=book_id)
    from googleapiclient.http import MediaIoBaseDownload
    with target.open("wb") as fh:
        loader = MediaIoBaseDownload(fh, drive_service.files().get_media(fileId=book_id))
        done = False
        while not done:
            _, done = loader.next_chunk()

    try:
        import fitz
        doc = fitz.open(str(target))
        if len(doc) < 1:
            doc.close()
            target.unlink(missing_ok=True)
            raise ValueError("Zero-page PDF")
        doc.close()
    except Exception as e:
        target.unlink(missing_ok=True)
        raise RuntimeError(f"SOURCE_PDF_NOT_FOUND: PDF is corrupted or unreadable ({e})")

    return target

# ==============================================================================
# AUTOMATIC BOOK -> TOC -> LESSONS -> ACTIVITIES/EXERCISES INDEX
# ============================================================================== 
BOOK_INDEX_DIR = ROOT / "data/factory_book_indexes"
BOOK_INDEX_DIR.mkdir(parents=True, exist_ok=True)

_TOC_HINT_RE = re.compile(
    r"(?i)(contents?|table\s+of\s+contents?|sommaire|table\s+des\s+mati[eè]res|فهرس|المحتويات)"
)

_EXERCISE_RE = re.compile(
    r"(?im)^\s*(exercise|exercises|activity|activities|problem|problems|"
    r"application|applications|practice|worksheet|exercice|exercices|"
    r"activité|activités|problème|problèmes|تمرين|تمارين|نشاط|أنشطة|مسألة|مسائل|تطبيق|تطبيقات)"
    r"(?:\s*(?:no\.?|n°|#)?\s*(\d+[A-Za-z]?))?\s*[:.\-–—)]?\s*(.*)$"
)


def _book_index_safe_id(book_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", str(book_id or "").strip())


def _clean_toc_title(value: str) -> str:
    value = re.sub(r"\s+", " ", str(value or "")).strip(" .\t-–—")
    value = re.sub(
        r"(?i)^(chapter|unit|lesson|chapitre|unité|leçon|درس|وحدة|فصل)"
        r"\s*(?:\d+[A-Za-z]?)?\s*[:.\-–—]*\s*", "", value
    ).strip()
    return value


_BOOK_INDEX_TEXT_CACHE: Dict[Tuple[int, int], str] = {}


def _page_is_scanned(page) -> bool:
    """True when a page is essentially a full-page image (scanned textbook)."""
    try:
        page_area = max(float(page.rect.width * page.rect.height), 1.0)
        for image in page.get_images(full=True):
            for rect in page.get_image_rects(image[0]):
                if float(rect.width * rect.height) / page_area >= 0.80:
                    return True
    except Exception:
        pass
    return False


def _render_book_page_image(page, *, dpi: int = 300) -> Path:
    """Render the real PDF page to an image before reading it.

    This is the same input strategy used for scanned curriculum pages: the
    physical page is rendered first, so indexing never depends on a missing or
    broken hidden text layer.
    """
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    tmp.close()
    path = Path(tmp.name)
    page.get_pixmap(dpi=dpi, alpha=False).save(str(path))
    return path


def _local_ocr_from_page_image(image_path: Path) -> str:
    """Read a rendered curriculum page locally; try layouts useful for TOCs."""
    if not shutil.which("tesseract"):
        return ""
    candidates = []
    for psm in (3, 6, 11):
        try:
            res = subprocess.run(
                ["tesseract", str(image_path), "stdout", "-l", "eng+fra+ara",
                 "--oem", "1", "--psm", str(psm)],
                capture_output=True, text=True, timeout=45,
            )
            txt = re.sub(r"\r\n?", "\n", res.stdout or "").strip()
            if txt:
                # Prefer useful structure, not just maximum character count.
                numbered = sum(1 for line in txt.splitlines()
                               if re.search(r"\b\d{1,4}\s*$", line.strip()))
                score = len(txt) + numbered * 120
                candidates.append((score, txt))
        except Exception:
            continue
    return max(candidates, key=lambda x: x[0])[1] if candidates else ""


def _page_text_for_book_index(doc, pdf_page: int) -> str:
    """Read a book page from the rendered page image when needed.

    Native text is used only for genuinely text-based pages. Scanned/image
    books are rendered to PNG and OCR-read locally, matching the proven
    PDF->page-image->reading path instead of trusting page.get_text().
    """
    if pdf_page < 1 or pdf_page > len(doc):
        return ""
    key = (id(doc), int(pdf_page))
    if key in _BOOK_INDEX_TEXT_CACHE:
        return _BOOK_INDEX_TEXT_CACHE[key]

    page = doc[pdf_page - 1]
    try:
        native = re.sub(r"\r\n?", "\n", page.get_text("text") or "").strip()
    except Exception:
        native = ""
    scanned = _page_is_scanned(page)

    if len(native) >= 60 and not scanned:
        _BOOK_INDEX_TEXT_CACHE[key] = native
        return native

    image_path = None
    ocr_text = ""
    try:
        image_path = _render_book_page_image(page, dpi=300 if scanned else 240)
        ocr_text = _local_ocr_from_page_image(image_path)
        if ocr_text:
            progress("BOOK_INDEX_RENDERED_PAGE_READ", page=pdf_page,
                     scanned=scanned, chars=len(ocr_text))
    except Exception as exc:
        progress("BOOK_INDEX_RENDERED_PAGE_READ_FAILED", page=pdf_page, error=str(exc))
    finally:
        if image_path:
            try:
                image_path.unlink(missing_ok=True)
            except Exception:
                pass

    final = ocr_text if len(ocr_text) >= max(20, len(native)) else native
    _BOOK_INDEX_TEXT_CACHE[key] = final
    return final

def _toc_numbered_line(line: str) -> bool:
    line = str(line or "").strip()
    # OCR often collapses dot leaders / columns to one space.
    return bool(re.search(r"\b\d{1,4}\s*$", line) and
                len(re.sub(r"\d{1,4}\s*$", "", line).strip(" .-–—\t")) >= 3)


def _detect_toc_pages(doc, max_scan_pages: int = 40) -> List[int]:
    candidates = []
    limit = min(len(doc), max_scan_pages)
    for pdf_page in range(1, limit + 1):
        text = _page_text_for_book_index(doc, pdf_page)
        if not text:
            continue
        lines = [x.strip() for x in text.splitlines() if x.strip()]
        numbered_lines = sum(1 for line in lines if _toc_numbered_line(line))
        if _TOC_HINT_RE.search(text) or numbered_lines >= 4:
            candidates.append(pdf_page)
    if not candidates:
        return []

    expanded = set(candidates)
    for p in list(candidates):
        for neighbor in (p - 1, p + 1):
            if 1 <= neighbor <= limit:
                nxt = _page_text_for_book_index(doc, neighbor)
                numbered = sum(1 for line in nxt.splitlines() if _toc_numbered_line(line))
                if numbered >= 3:
                    expanded.add(neighbor)
    return sorted(expanded)


def _parse_toc_entries(doc, toc_pages: List[int]) -> List[dict]:
    entries = []
    for toc_pdf_page in toc_pages:
        text = _page_text_for_book_index(doc, toc_pdf_page)
        for raw_line in text.splitlines():
            line = re.sub(r"\s+", " ", raw_line).strip()
            if not line:
                continue
            match = re.match(r"^(?P<title>.+?)(?:\s*\.{2,}\s*|\s+)(?P<page>\d{1,4})\s*$", line)
            if not match:
                continue
            raw_title = match.group("title")
            # Keep the real title but remove a standalone chapter/unit ordinal
            # commonly emitted by OCR at the left edge of a TOC row.
            raw_title = re.sub(r"^\s*(?:chapter|chapitre|unit|unité|lesson|leçon)?\s*\d{1,3}\s*[:.\-–—]?\s+", "", raw_title, flags=re.I)
            title = _clean_toc_title(raw_title)
            try:
                printed_page = int(match.group("page"))
            except ValueError:
                continue
            if len(title) < 3 or _TOC_HINT_RE.fullmatch(title):
                continue
            if printed_page < 1:
                continue
            entries.append({
                "title": title,
                "printed_page": printed_page,
                "toc_pdf_page": toc_pdf_page,
                "toc_line": raw_line.strip(),
            })
    unique, seen = [], set()
    for item in entries:
        key = (item["title"].casefold(), item["printed_page"])
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique


def _candidate_pdf_offsets(doc, toc_entries: List[dict]) -> List[int]:
    """Resolve printed->physical offset without OCR-scanning the whole book repeatedly."""
    offsets = []
    for entry in toc_entries[:20]:
        tokens = [
            token.casefold() for token in re.findall(r"\w+", entry["title"], flags=re.UNICODE)
            if len(token) >= 4
        ]
        if not tokens:
            continue
        printed = int(entry["printed_page"])
        # Textbooks normally differ by front-matter offset. Search only plausible range.
        lo = max(1, printed - 10)
        hi = min(len(doc), printed + 60)
        for pdf_page in range(lo, hi + 1):
            text = _page_text_for_book_index(doc, pdf_page).casefold()
            hits = sum(1 for token in tokens if token in text)
            required = 1 if len(tokens) == 1 else min(2, len(tokens))
            if hits >= required:
                offsets.append(pdf_page - printed)
                break
    return offsets


def _resolve_printed_to_pdf_offset(doc, toc_entries: List[dict]) -> int:
    offsets = _candidate_pdf_offsets(doc, toc_entries)
    if offsets:
        counts = {}
        for offset in offsets:
            counts[offset] = counts.get(offset, 0) + 1
        best_offset, votes = max(counts.items(), key=lambda pair: pair[1])
        if votes >= 2 or len(toc_entries) < 2:
            return best_offset

    # Deterministic fallback: use PDF page labels when the document exposes them.
    label_votes = []
    for pdf_page in range(1, len(doc) + 1):
        try:
            label = str(doc[pdf_page - 1].get_label() or "").strip()
        except Exception:
            label = ""
        if label.isdigit():
            label_votes.append(pdf_page - int(label))
    if label_votes:
        counts = {}
        for offset in label_votes:
            if -10 <= offset <= 60:
                counts[offset] = counts.get(offset, 0) + 1
        if counts:
            return max(counts.items(), key=lambda pair: pair[1])[0]

    raise RuntimeError(
        "BOOK_INDEX_PAGE_OFFSET_UNVERIFIED: could not map printed TOC pages to physical PDF pages"
    )

def _lesson_slug(book_id: str, number: int) -> str:
    return f"{_book_index_safe_id(book_id).upper()}-AUTO-{number:03d}"


def _extract_lesson_works(doc, start_page: int, end_page: int) -> List[dict]:
    works = []
    sequence = 0
    for pdf_page in range(start_page, end_page + 1):
        text = _page_text_for_book_index(doc, pdf_page)
        for line_no, raw_line in enumerate(text.splitlines(), 1):
            line = re.sub(r"\s+", " ", raw_line).strip()
            if not line:
                continue
            match = _EXERCISE_RE.match(line)
            if not match:
                continue
            sequence += 1
            label = (match.group(1) or "").strip()
            printed_number = (match.group(2) or "").strip()
            remainder = (match.group(3) or "").strip()
            kind_lower = label.casefold()
            if any(x in kind_lower for x in ("activity", "activité", "نشاط", "أنشطة")):
                work_type = "activity"
            elif any(x in kind_lower for x in ("problem", "problème", "مسألة", "مسائل")):
                work_type = "problem"
            else:
                work_type = "exercise"
            works.append({
                "work_id": f"W{sequence:03d}",
                "type": work_type,
                "label": label,
                "printed_number": printed_number or None,
                "pdf_page": pdf_page,
                "line_number": line_no,
                "source_heading": line,
                "source_preview": remainder[:500],
            })
    return works


def _iter_canonical_lesson_entries(catalog: dict):
    """Yield every lesson-like record from supported canonical catalog shapes."""
    if not isinstance(catalog, dict):
        return
    lessons = catalog.get("lessons")
    if isinstance(lessons, list):
        for entry in lessons:
            if isinstance(entry, dict):
                yield entry
        return
    for grade_value in catalog.values():
        if not isinstance(grade_value, dict):
            continue
        for subject_value in grade_value.values():
            if isinstance(subject_value, dict) and isinstance(subject_value.get("lessons"), list):
                for entry in subject_value["lessons"]:
                    if isinstance(entry, dict):
                        yield entry
            elif isinstance(subject_value, list):
                for entry in subject_value:
                    if isinstance(entry, dict):
                        yield entry


def _drive_list_curriculum_pdfs(drive_service=None) -> List[dict]:
    """Discover curriculum PDFs strictly below the configured Drive root.

    Primary path: recursive parent traversal.
    Recovery path: search visible PDFs/shortcuts and prove ancestry back to the
    configured curriculum root.  The recovery path never admits an unrelated
    PDF merely because it is visible to the OAuth credential.
    """
    if drive_service is None:
        drive_service = get_drive_service()

    folder_mime = "application/vnd.google-apps.folder"
    shortcut_mime = "application/vnd.google-apps.shortcut"
    pdf_mime = "application/pdf"
    configured_root_id = resolve_drive_root_id()
    root_id = configured_root_id

    def _get_item(file_id: str) -> dict:
        return drive_service.files().get(
            fileId=file_id,
            fields=("id,name,mimeType,description,parents,"
                    "shortcutDetails(targetId,targetMimeType)"),
            supportsAllDrives=True,
        ).execute()

    root_meta = _get_item(root_id)
    if str(root_meta.get("mimeType") or "") == shortcut_mime:
        details = root_meta.get("shortcutDetails") or {}
        target_id = str(details.get("targetId") or "").strip()
        target_mime = str(details.get("targetMimeType") or "").strip()
        if not target_id:
            raise RuntimeError("CURRICULUM_DRIVE_ROOT_SHORTCUT_INVALID")
        if target_mime == pdf_mime:
            return [{
                "book_id": target_id,
                "name": str(root_meta.get("name") or f"{target_id}.pdf"),
                "drive_path": str(root_meta.get("name") or "").strip(),
                "description": str(root_meta.get("description") or ""),
            }]
        if target_mime != folder_mime:
            raise RuntimeError(
                f"CURRICULUM_DRIVE_ROOT_NOT_FOLDER:{target_mime or 'unknown'}")
        root_id = target_id
        root_meta = _get_item(root_id)

    root_mime = str(root_meta.get("mimeType") or "")
    if root_mime == pdf_mime:
        return [{
            "book_id": root_id,
            "name": str(root_meta.get("name") or f"{root_id}.pdf"),
            "drive_path": str(root_meta.get("name") or "").strip(),
            "description": str(root_meta.get("description") or ""),
        }]
    if root_mime != folder_mime:
        raise RuntimeError(
            f"CURRICULUM_DRIVE_ROOT_NOT_FOLDER:{root_mime or 'unknown'}")

    out: List[dict] = []
    seen_pdfs = set()

    def _append_pdf(book_id: str, name: str, path: str, description: str) -> None:
        book_id = str(book_id or "").strip()
        if not book_id or book_id in seen_pdfs:
            return
        seen_pdfs.add(book_id)
        out.append({
            "book_id": book_id,
            "name": str(name or f"{book_id}.pdf").strip(),
            "drive_path": str(path or name or "").strip("/"),
            "description": str(description or ""),
        })

    # Normal recursive traversal first.  This is fast when Drive exposes folder
    # children normally to the active OAuth identity.
    queue = [(root_id, "")]
    seen_folders = set()
    while queue:
        folder_id, parent_path = queue.pop(0)
        if folder_id in seen_folders:
            continue
        seen_folders.add(folder_id)
        token = None
        while True:
            resp = drive_service.files().list(
                q=f"'{folder_id}' in parents and trashed=false",
                spaces="drive",
                fields=("nextPageToken,files(id,name,mimeType,description,parents,"
                        "shortcutDetails(targetId,targetMimeType))"),
                pageSize=1000,
                pageToken=token,
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
            ).execute()
            for item in resp.get("files") or []:
                item_id = str(item.get("id") or "").strip()
                name = str(item.get("name") or "").strip()
                path = f"{parent_path}/{name}".strip("/")
                mime = str(item.get("mimeType") or "")
                description = str(item.get("description") or "")

                effective_id = item_id
                effective_mime = mime
                if mime == shortcut_mime:
                    details = item.get("shortcutDetails") or {}
                    effective_id = str(details.get("targetId") or "").strip()
                    effective_mime = str(details.get("targetMimeType") or "").strip()
                    if not effective_id:
                        continue

                if effective_mime == folder_mime:
                    queue.append((effective_id, path))
                elif effective_mime == pdf_mime or name.casefold().endswith(".pdf"):
                    _append_pdf(effective_id, name, path, description)
            token = resp.get("nextPageToken")
            if not token:
                break

    if out:
        progress("CURRICULUM_DRIVE_DISCOVERY", root=root_id,
                 method="recursive_parents", pdf_count=len(out))
        return out

    # Some shared/My-Drive layouts allow direct file access but do not enumerate
    # children reliably from the configured root.  Recover by searching visible
    # PDF files/shortcuts, then PROVE that the item itself descends from root.
    # This is intentionally not a global-PDF fallback.
    meta_cache = {root_id: root_meta}

    def _meta(file_id: str) -> Optional[dict]:
        file_id = str(file_id or "").strip()
        if not file_id:
            return None
        if file_id in meta_cache:
            return meta_cache[file_id]
        try:
            meta_cache[file_id] = _get_item(file_id)
        except Exception:
            meta_cache[file_id] = None
        return meta_cache[file_id]

    def _is_descendant(item: dict) -> bool:
        frontier = [str(x) for x in (item.get("parents") or []) if str(x).strip()]
        visited = set()
        while frontier:
            parent_id = frontier.pop()
            if parent_id == root_id:
                return True
            if parent_id in visited:
                continue
            visited.add(parent_id)
            parent = _meta(parent_id)
            if not parent:
                continue
            frontier.extend(
                str(x) for x in (parent.get("parents") or []) if str(x).strip())
        return False

    token = None
    while True:
        resp = drive_service.files().list(
            q=("trashed=false and (mimeType='application/pdf' or "
               "mimeType='application/vnd.google-apps.shortcut')"),
            spaces="drive",
            fields=("nextPageToken,files(id,name,mimeType,description,parents,"
                    "shortcutDetails(targetId,targetMimeType))"),
            pageSize=1000,
            pageToken=token,
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        ).execute()
        for item in resp.get("files") or []:
            if not _is_descendant(item):
                continue
            item_id = str(item.get("id") or "").strip()
            name = str(item.get("name") or "").strip()
            mime = str(item.get("mimeType") or "")
            description = str(item.get("description") or "")
            effective_id = item_id
            effective_mime = mime
            if mime == shortcut_mime:
                details = item.get("shortcutDetails") or {}
                effective_id = str(details.get("targetId") or "").strip()
                effective_mime = str(details.get("targetMimeType") or "").strip()
            if effective_id and (effective_mime == pdf_mime or name.casefold().endswith(".pdf")):
                _append_pdf(effective_id, name, name, description)
        token = resp.get("nextPageToken")
        if not token:
            break

    if out:
        progress("CURRICULUM_DRIVE_DISCOVERY", root=root_id,
                 method="verified_ancestry_search", pdf_count=len(out))
        return out

    raise RuntimeError(
        f"CURRICULUM_DRIVE_NO_PDFS: configured_root={configured_root_id}; "
        f"resolved_root={root_id}; root is readable, recursive enumeration "
        "returned no PDFs, and ancestry-verified Drive search found no PDFs "
        "below that root")

def _discover_lesson_boundaries_without_toc(doc) -> List[dict]:
    """Find evidence-backed lesson starts when a printed TOC is absent/unreadable.

    This deliberately does NOT split by arbitrary page counts. A boundary is
    accepted only when an OCR/native-text page contains a strong lesson/chapter
    heading. If evidence is insufficient the caller fails closed.
    """
    explicit = re.compile(
        r"(?i)^\s*(?:chapter|unit|lesson|chapitre|unité|leçon|"
        r"الفصل|الوحدة|الدرس)\s*(?:[0-9ivxlcdm]+|[A-Z]|[٠-٩]+)?\s*[:.\-–—]?\s*(.+?)\s*$")
    starts = []
    for pdf_page in range(1, len(doc) + 1):
        text = _page_text_for_book_index(doc, pdf_page)
        lines = [re.sub(r"\s+", " ", x).strip() for x in text.splitlines() if x.strip()]
        for line in lines[:18]:
            m = explicit.match(line)
            if not m:
                continue
            title = _clean_toc_title(line)
            if len(title) < 3 or len(title) > 160:
                continue
            starts.append({
                "title": title, "printed_page": pdf_page,
                "toc_pdf_page": None, "toc_line": line,
                "pdf_start_page": pdf_page, "boundary_source": "verified_heading",
            })
            break
    deduped, seen_pages = [], set()
    for item in starts:
        if item["pdf_start_page"] not in seen_pages:
            seen_pages.add(item["pdf_start_page"]); deduped.append(item)
    if len(deduped) < 2:
        raise RuntimeError(
            "BOOK_INDEX_LESSON_BOUNDARIES_UNVERIFIED: no TOC and fewer than two verified lesson/chapter headings")
    return deduped


def _registered_books_from_catalog() -> List[dict]:
    """Return one metadata record per unique registered source book."""
    catalog = load_canonical_catalog()
    books = {}
    for entry in _iter_canonical_lesson_entries(catalog):
        book_id = str(entry.get("book_id") or "").strip()
        if not book_id:
            continue
        meta = books.setdefault(book_id, {"book_id": book_id})
        for key in ("grade", "subject", "language", "branch", "track"):
            value = entry.get(key)
            if value not in (None, "") and key not in meta:
                meta[key] = value
    # The canonical catalog is optional for discovery. Drive is authoritative
    # for finding curriculum PDFs; an empty catalog must not block indexing.
    return list(books.values())


def _metadata_for_book(book_id: str) -> dict:
    for meta in _registered_books_from_catalog():
        if meta["book_id"] == book_id:
            return meta
    return {"book_id": book_id}


def build_all_registered_book_indexes(drive_service=None, force: bool = False) -> dict:
    """Index every unique book registered in the canonical catalog, truthfully."""
    catalog_books = {m["book_id"]: m for m in _registered_books_from_catalog()}
    discovered = _drive_list_curriculum_pdfs(drive_service=drive_service)
    books = []
    for item in discovered:
        meta = dict(item)
        meta.update(catalog_books.get(item["book_id"], {}))
        books.append(meta)
    report = {
        "status": "RUNNING",
        "schema": "NABIL_ALL_BOOK_INDEX_V1",
        "generated_at": now(),
        "book_count": len(books),
        "indexed": [],
        "failed": [],
    }
    progress("ALL_BOOK_INDEX_START", books=len(books))
    for position, meta in enumerate(books, 1):
        book_id = meta["book_id"]
        try:
            result = build_book_lesson_index(
                book_id,
                drive_service=drive_service,
                force=force,
                book_metadata=meta,
            )
            report["indexed"].append({
                "book_id": book_id,
                "position": position,
                "lesson_count": result.get("lesson_count", 0),
                "work_count": result.get("work_count", 0),
                "index_path": str(BOOK_INDEX_DIR / f"{_book_index_safe_id(book_id)}.json"),
            })
        except Exception as exc:
            report["failed"].append({
                "book_id": book_id,
                "position": position,
                "error": f"{type(exc).__name__}: {exc}",
            })
            progress("ALL_BOOK_INDEX_BOOK_FAILED", book_id=book_id, error=str(exc))
    report["indexed_count"] = len(report["indexed"])
    report["failed_count"] = len(report["failed"])
    report["status"] = "INDEXED" if not report["failed"] else "PARTIAL_FAILURE"
    report["completed_at"] = now()
    summary_path = BOOK_INDEX_DIR / "_all_books_report.json"
    summary_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    progress("ALL_BOOK_INDEX_COMPLETE", indexed=report["indexed_count"], failed=report["failed_count"], output=str(summary_path))
    return report



def _normalize_grade_selector(value: Any) -> Optional[int]:
    """Normalize CLI/catalog grade values such as 7, G07, EB7 or Grade 7."""
    if value in (None, ""):
        return None
    if isinstance(value, int):
        return value
    text = str(value).strip()
    match = re.search(r"(\d{1,2})", text)
    if not match:
        raise RuntimeError(f"GRADE_SELECTOR_INVALID: {value}")
    return int(match.group(1))


def _normalize_subject_selector(value: Any) -> str:
    """Use the same subject aliases as the teaching engine."""
    text = str(value or "").strip().casefold().replace(" ", "_")
    return SUBJECT_ALIASES.get(text, text)


def _book_matches_scope(meta: dict, grade: Any = None, subject: Any = None) -> bool:
    wanted_grade = _normalize_grade_selector(grade)
    wanted_subject = _normalize_subject_selector(subject) if subject not in (None, "") else ""
    if wanted_grade is not None:
        try:
            actual_grade = _normalize_grade_selector(meta.get("grade"))
        except RuntimeError:
            return False
        if actual_grade != wanted_grade:
            return False
    if wanted_subject:
        actual_subject = _normalize_subject_selector(meta.get("subject"))
        if actual_subject != wanted_subject:
            return False
    return True


def _probe_drive_book_metadata(meta: dict, drive_service=None) -> dict:
    """Infer scope metadata without requiring TOC/lesson indexing to succeed."""
    import fitz
    book_id = str(meta.get("book_id") or "").strip()
    if not book_id:
        raise RuntimeError("BOOK_METADATA_PROBE_MISSING_BOOK_ID")
    pdf_path = resolve_source_book_pdf(book_id, drive_service=drive_service)
    doc = fitz.open(str(pdf_path))
    try:
        if len(doc) < 1:
            raise RuntimeError("BOOK_INDEX_EMPTY_PDF")
        return _infer_book_metadata_for_index(book_id, drive_service, doc, meta)
    finally:
        doc_id = id(doc)
        for cache_key in [k for k in _BOOK_INDEX_TEXT_CACHE if k[0] == doc_id]:
            _BOOK_INDEX_TEXT_CACHE.pop(cache_key, None)
        doc.close()


def build_scoped_book_indexes(
        drive_service=None, force: bool = False,
        grade: Any = None, subject: Any = None) -> dict:
    """Index every registered book matching a grade and/or subject selector."""
    catalog_books = {m["book_id"]: m for m in _registered_books_from_catalog()}
    discovered = _drive_list_curriculum_pdfs(drive_service=drive_service)
    books = []
    # Prefer metadata already proven by the catalog/name/path. Unknown books are
    # indexed once so cover OCR can infer their real grade/subject; no random PDF
    # is ever relabelled as the requested scope.
    for item in discovered:
        meta = dict(item)
        meta.update(catalog_books.get(item["book_id"], {}))
        if _book_matches_scope(meta, grade=grade, subject=subject):
            books.append(meta)
            continue
        if not meta.get("grade") or not meta.get("subject"):
            try:
                inferred = _probe_drive_book_metadata(meta, drive_service=drive_service)
                if _book_matches_scope(inferred, grade=grade, subject=subject):
                    books.append(inferred)
            except Exception as exc:
                progress("SCOPED_BOOK_DISCOVERY_SKIPPED", book_id=meta.get("book_id"), error=str(exc))
    if not books:
        raise RuntimeError(
            f"BOOK_INDEX_SCOPE_EMPTY_AFTER_DRIVE_DISCOVERY: grade={grade!r} subject={subject!r}")

    report = {
        "status": "RUNNING",
        "schema": "NABIL_SCOPED_BOOK_INDEX_V1",
        "generated_at": now(),
        "grade": _normalize_grade_selector(grade),
        "subject": _normalize_subject_selector(subject) if subject not in (None, "") else None,
        "book_count": len(books),
        "indexed": [],
        "failed": [],
    }
    progress(
        "SCOPED_BOOK_INDEX_START", books=len(books),
        grade=report["grade"], subject=report["subject"])

    for position, meta in enumerate(books, 1):
        book_id = meta["book_id"]
        try:
            result = build_book_lesson_index(
                book_id,
                drive_service=drive_service,
                force=force,
                book_metadata=meta,
            )
            report["indexed"].append({
                "book_id": book_id,
                "position": position,
                "grade": meta.get("grade"),
                "subject": meta.get("subject"),
                "lesson_count": result.get("lesson_count", 0),
                "work_count": result.get("work_count", 0),
                "index_path": str(
                    BOOK_INDEX_DIR / f"{_book_index_safe_id(book_id)}.json"),
            })
        except Exception as exc:
            report["failed"].append({
                "book_id": book_id,
                "position": position,
                "error": f"{type(exc).__name__}: {exc}",
            })
            progress(
                "SCOPED_BOOK_INDEX_BOOK_FAILED",
                book_id=book_id, error=str(exc))

    report["indexed_count"] = len(report["indexed"])
    report["failed_count"] = len(report["failed"])
    report["status"] = "INDEXED" if not report["failed"] else "PARTIAL_FAILURE"
    report["completed_at"] = now()
    progress(
        "SCOPED_BOOK_INDEX_COMPLETE",
        indexed=report["indexed_count"], failed=report["failed_count"])
    return report


def _indexed_lessons_for_scope(grade: Any = None, subject: Any = None) -> List[dict]:
    """Read discovered lessons from completed per-book indexes for a scope."""
    lessons: List[dict] = []
    for index_path in sorted(BOOK_INDEX_DIR.glob("*.json")):
        if index_path.name.startswith("_"):
            continue
        try:
            payload = json.loads(index_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if payload.get("status") != "INDEXED":
            continue
        for entry in payload.get("lessons") or []:
            if isinstance(entry, dict) and _book_matches_scope(
                    entry, grade=grade, subject=subject):
                lessons.append(entry)
    return lessons


def resolve_lesson_selector(
        lesson: str, grade: Any = None, subject: Any = None) -> dict:
    """Resolve a lesson by exact/fuzzy title inside the requested grade/subject."""
    needle = re.sub(r"\s+", " ", str(lesson or "")).strip().casefold()
    if not needle:
        raise RuntimeError("LESSON_SELECTOR_EMPTY")

    candidates = _indexed_lessons_for_scope(grade=grade, subject=subject)
    exact = [
        e for e in candidates
        if re.sub(r"\s+", " ", str(e.get("canonical_title") or "")).strip().casefold() == needle
        or str(e.get("lesson_id") or "").strip().casefold() == needle
    ]
    if len(exact) == 1:
        return exact[0]
    if len(exact) > 1:
        raise RuntimeError(
            "LESSON_SELECTOR_AMBIGUOUS: " +
            "; ".join(f"{e.get('lesson_id')}={e.get('canonical_title')}" for e in exact[:20]))

    partial = [
        e for e in candidates
        if needle in re.sub(r"\s+", " ", str(e.get("canonical_title") or "")).strip().casefold()
    ]
    if len(partial) == 1:
        return partial[0]
    if len(partial) > 1:
        raise RuntimeError(
            "LESSON_SELECTOR_AMBIGUOUS: " +
            "; ".join(f"{e.get('lesson_id')}={e.get('canonical_title')}" for e in partial[:20]))
    raise RuntimeError(
        f"LESSON_SELECTOR_NOT_FOUND: lesson={lesson!r} grade={grade!r} subject={subject!r}")

def _infer_book_metadata_for_index(book_id: str, drive_service, doc, metadata: dict) -> dict:
    """Fill missing grade/subject/language from Drive filename + locally read cover pages."""
    out = dict(metadata or {})
    name = ""
    if drive_service:
        try:
            meta = drive_service.files().get(fileId=book_id, fields="name,description").execute()
            name = str(meta.get("name") or "")
            out["source_name"] = name
        except Exception:
            pass

    sample_parts = [name]
    for page_num in range(1, min(len(doc), 8) + 1):
        sample_parts.append(_page_text_for_book_index(doc, page_num))
    sample = "\n".join(sample_parts)
    folded = sample.casefold()

    if out.get("grade") in (None, ""):
        m = re.search(r"(?i)\b(?:grade|eb|basic\s+education\s+grade)\s*[-:]?\s*(\d{1,2})\b", sample)
        if m:
            out["grade"] = int(m.group(1))
        else:
            # OCR occasionally reads Eight as Tight; filename is preferred when available.
            words = {"seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12}
            for word, number in words.items():
                if re.search(rf"(?i)\bgrade\s+{word}\b", sample):
                    out["grade"] = number
                    break

    if not out.get("subject"):
        subject_patterns = [
            ("mathematics", r"\b(mathematics|mathématiques|maths?)\b|رياضيات"),
            ("physics", r"\b(physics|physique)\b|فيزياء"),
            ("chemistry", r"\b(chemistry|chimie)\b|كيمياء"),
            ("biology", r"\b(biology|biologie)\b|أحياء"),
            ("general_science", r"\b(general\s+science|sciences?)\b|علوم"),
            ("english_language", r"\benglish\b|الإنجليزية|الانجليزية"),
            ("french_language", r"\b(french|français)\b|الفرنسية"),
            ("arabic_language", r"\barabic\b|العربية"),
        ]
        for subject, pattern in subject_patterns:
            if re.search(pattern, folded, flags=re.I):
                out["subject"] = subject
                break

    if not out.get("language"):
        # Prefer explicit filename markers, then script/subject hints.
        if re.search(r"(?i)\b(french|français|francais)\b", name):
            out["language"] = "fr"
        elif re.search(r"(?i)\b(english|anglais)\b", name):
            out["language"] = "en"
        elif re.search(r"[\u0600-\u06ff]", sample):
            out["language"] = "ar"
        elif re.search(r"\b(le|la|les|des|chapitre|exercice)\b", folded):
            out["language"] = "fr"
        else:
            out["language"] = "en"

    out.setdefault("book_id", book_id)
    return out


def build_book_lesson_index(book_id: str, drive_service=None, force: bool = False, book_metadata: Optional[dict] = None) -> dict:
    """Drive/local PDF -> TOC -> lessons -> page ranges -> linked activities/exercises."""
    import fitz

    safe_id = _book_index_safe_id(book_id)
    book_metadata = dict(book_metadata or _metadata_for_book(book_id))
    output_path = BOOK_INDEX_DIR / f"{safe_id}.json"
    if output_path.exists() and not force:
        try:
            existing = json.loads(output_path.read_text(encoding="utf-8"))
            if existing.get("book_id") == book_id and existing.get("status") == "INDEXED" and existing.get("lessons"):
                progress("BOOK_INDEX_CACHE_HIT", book_id=book_id, lessons=len(existing["lessons"]))
                return existing
        except Exception:
            pass

    pdf_path = resolve_source_book_pdf(book_id, drive_service=drive_service)
    doc = fitz.open(str(pdf_path))
    try:
        if len(doc) < 1:
            raise RuntimeError("BOOK_INDEX_EMPTY_PDF")
        book_metadata = _infer_book_metadata_for_index(
            book_id, drive_service, doc, book_metadata)
        progress("BOOK_INDEX_START", book_id=book_id, pdf_pages=len(doc),
                 grade=book_metadata.get("grade"), subject=book_metadata.get("subject"),
                 language=book_metadata.get("language"))
        toc_pages = _detect_toc_pages(doc)
        toc_entries = _parse_toc_entries(doc, toc_pages) if toc_pages else []
        if toc_entries:
            offset = _resolve_printed_to_pdf_offset(doc, toc_entries)
            valid_entries = []
            for entry in toc_entries:
                pdf_start = entry["printed_page"] + offset
                if 1 <= pdf_start <= len(doc):
                    valid_entries.append({**entry, "pdf_start_page": pdf_start,
                                          "boundary_source": "printed_toc"})
        else:
            progress("BOOK_INDEX_TOC_FALLBACK_TO_VERIFIED_HEADINGS", book_id=book_id)
            offset = None
            valid_entries = _discover_lesson_boundaries_without_toc(doc)
        valid_entries.sort(key=lambda x: (x["pdf_start_page"], x["printed_page"]))

        deduped, seen_starts = [], set()
        for item in valid_entries:
            if item["pdf_start_page"] not in seen_starts:
                seen_starts.add(item["pdf_start_page"])
                deduped.append(item)
        if not deduped:
            raise RuntimeError("BOOK_INDEX_NO_VALID_LESSON_STARTS")

        lessons = []
        for idx, item in enumerate(deduped):
            start_page = item["pdf_start_page"]
            end_page = deduped[idx + 1]["pdf_start_page"] - 1 if idx + 1 < len(deduped) else len(doc)
            if end_page < start_page:
                raise RuntimeError(f"BOOK_INDEX_INVALID_LESSON_RANGE: {item['title']} {start_page}-{end_page}")
            lesson_id = _lesson_slug(book_id, idx + 1)
            works = _extract_lesson_works(doc, start_page, end_page)
            lesson = {
                "lesson_id": lesson_id,
                "canonical_title": item["title"],
                "book_id": book_id,
                "grade": book_metadata.get("grade"),
                "subject": book_metadata.get("subject"),
                "language": book_metadata.get("language"),
                "branch": book_metadata.get("branch") or book_metadata.get("track") or "",
                "toc_pdf_page": item["toc_pdf_page"],
                "printed_start_page": item["printed_page"],
                "pdf_start_page": start_page,
                "pdf_end_page": end_page,
                "works": works,
                "activities": [w for w in works if w["type"] == "activity"],
                "exercises": [w for w in works if w["type"] in ("exercise", "problem")],
            }
            lessons.append(lesson)
            progress(
                "BOOK_INDEX_LESSON", book_id=book_id, lesson_id=lesson_id,
                title=item["title"], pages=f"{start_page}-{end_page}", works=len(works)
            )

        result = {
            "status": "INDEXED",
            "schema": "NABIL_BOOK_INDEX_V1",
            "generated_at": now(),
            "book_id": book_id,
            "book_metadata": book_metadata,
            "index_method": "printed_toc" if toc_entries else "verified_headings",
            "source_pdf": str(pdf_path),
            "pdf_pages": len(doc),
            "toc_pdf_pages": toc_pages,
            "printed_to_pdf_offset": offset,
            "lesson_count": len(lessons),
            "work_count": sum(len(lesson["works"]) for lesson in lessons),
            "lessons": lessons,
        }
        tmp = output_path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(output_path)
        progress(
            "BOOK_INDEX_COMPLETE", book_id=book_id, lessons=result["lesson_count"],
            works=result["work_count"], output=str(output_path)
        )
        return result
    finally:
        doc_id = id(doc)
        for cache_key in [k for k in _BOOK_INDEX_TEXT_CACHE if k[0] == doc_id]:
            _BOOK_INDEX_TEXT_CACHE.pop(cache_key, None)
        doc.close()


def load_canonical_catalog() -> dict:
    candidates = [CATALOG_PATH, ROOT / "config/canonical_lessons_catalog.json", ROOT / "canonical_lessons_catalog.json", ROOT / "lessons_catalog.json"]
    for c in candidates:
        if c.exists():
            try:
                data = json.loads(c.read_text(encoding="utf-8"))
                if isinstance(data, dict) and data:
                    return data
            except Exception:
                pass
    raise RuntimeError("CANONICAL_CATALOG_NOT_FOUND")


def resolve_canonical_entry(lesson_id: str) -> dict:
    catalog = load_canonical_catalog()
    found = None
    if "lessons" in catalog and isinstance(catalog["lessons"], list):
        for e in catalog["lessons"]:
            if e.get("lesson_id", "").upper() == lesson_id.upper():
                found = e
                break
    else:
        for g_k, g_v in catalog.items():
            if isinstance(g_v, dict):
                for s_k, s_v in g_v.items():
                    if isinstance(s_v, dict) and "lessons" in s_v:
                        for e in s_v["lessons"]:
                            if e.get("lesson_id", "").upper() == lesson_id.upper():
                                found = e
                                break
                    elif isinstance(s_v, list):
                        for e in s_v:
                            if isinstance(e, dict) and e.get("lesson_id", "").upper() == lesson_id.upper():
                                found = e
                                break

    if not found:
        # Book factory discovers source chapter records automatically; its
        # cached indexes extend the old one-pilot catalog, never replace it.
        # On-Demand routes can resolve lessons from the same source index.
        for book_index in sorted((ROOT / "data/factory_book_indexes").glob("*.json")):
            try:
                source = json.loads(book_index.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            for entry in source.get("lessons", []):
                if entry.get("lesson_id", "").upper() == lesson_id.upper():
                    found = entry
                    break
            if found:
                break

    if not found:
        raise RuntimeError(f"LESSON_NOT_FOUND_IN_CATALOG: {lesson_id}")

    required = ["lesson_id", "canonical_title", "grade", "subject", "book_id", "pdf_start_page", "pdf_end_page", "language"]
    for f in required:
        if f not in found or found[f] is None:
            raise RuntimeError(f"CANONICAL_CATALOG_CORRUPT: Missing mandatory field '{f}' in {lesson_id}")

    return found


def assert_authorized_source_vision(
        lesson_id: str, book_id: str, pdf_page: int,
        provider_override: Optional[str] = None):
    """Require explicit owner consent for at least one eligible provider.

    When a concrete provider produced stored evidence, provider_override pins
    revalidation to that exact provider. Otherwise the configured failover pool
    is checked so an unauthorized primary cannot block an authorized fallback.
    """
    context = {
        "lesson_id": lesson_id,
        "book_id": book_id,
        "pdf_page": pdf_page,
    }
    if provider_override:
        if _vision_provider_authorized(
                provider_override, context, require_key=True):
            return
        raise RuntimeError(
            "VISION_SHARING_NOT_AUTHORIZED: "
            f"provider={provider_override} lesson_id={lesson_id} "
            f"page={pdf_page}")

    preferred = os.getenv(
        "NABIL_FACTORY_AI_PROVIDER", "auto").strip().lower()
    keys = _provider_keys()
    candidates = _provider_order(preferred, keys)
    authorized = [
        p for p in candidates
        if _vision_provider_authorized(
            p, context, require_key=True)
    ]
    if authorized:
        return
    raise RuntimeError(
        "VISION_SHARING_NOT_AUTHORIZED: "
        f"providers={candidates} lesson_id={lesson_id} page={pdf_page}")


# ==============================================================================
# 6. MULTIMODAL EXTRACTION: TRUE VISION PAYLOAD, TOC & VECTOR GROUPING
# ==============================================================================
def extract_page_text_robust(doc, page_num: int, lesson_id: str, book_id: str, cache_dir: Path) -> str:
    page = doc[page_num - 1]
    txt = (page.get_text() or "").strip()
    scanned = any(
        (rect.width * rect.height) / (page.rect.width * page.rect.height) >= 0.80
        for image in page.get_images(full=True)
        for rect in page.get_image_rects(image[0])
    )
    # A scanned textbook can contain a partial/low-quality hidden OCR layer.
    # For source segmentation, re-read the real page locally at high resolution
    # instead of accepting a merely "long enough" hidden text layer.
    if len(txt) >= 60 and not scanned:
        return txt

    image_path = None
    try:
        image_path = _render_book_page_image(page, dpi=300 if scanned else 240)
        ocr_txt = _local_ocr_from_page_image(image_path)
        if len(ocr_txt) >= 60:
            progress(
                "SOURCE_PAGE_RENDERED_OCR_SELECTED",
                page=page_num, scanned=scanned, chars=len(ocr_txt),
            )
            return ocr_txt
    except Exception:
        pass
    finally:
        if image_path:
            try:
                image_path.unlink(missing_ok=True)
            except Exception:
                pass

    assert_authorized_source_vision(lesson_id, book_id, page_num)
    page_img = cache_dir / f"page_vision_{page_num}.png"
    page.get_pixmap(dpi=150).save(str(page_img))
    b64_img = base64.b64encode(page_img.read_bytes()).decode("utf-8")
    prompt = "Extract all text, exercises, and formulas verbatim from this curriculum page. Return JSON: {'text': str}"
    res = execute_llm_completion(
        prompt, json_mode=True, image_base64=b64_img,
        vision_context={
            "lesson_id": lesson_id,
            "book_id": book_id,
            "pdf_page": page_num,
        })
    return json.loads(res).get("text", "")


def extract_multimodal_page_figures(doc, page_num: int, cache_dir: Path,
                                    lesson_id: str, book_id: str) -> List[Dict[str, Any]]:
    """Find actual figure regions. A scanned full-page bitmap is not a figure."""
    import fitz
    from PIL import Image

    page = doc[page_num - 1]
    figures = []
    has_scanned_page = False
    for idx, img in enumerate(page.get_images(full=True)):
        xref = img[0]
        rects = page.get_image_rects(xref)
        if not rects:
            continue
        for rect in rects:
            area = (rect.width * rect.height) / (page.rect.width * page.rect.height)
            if area >= 0.80:
                has_scanned_page = True
                continue
            extracted = doc.extract_image(xref)
            try:
                with Image.open(io.BytesIO(extracted["image"])) as picture:
                    out = io.BytesIO()
                    picture.convert("RGB").save(out, format="PNG")
                    img_bytes = out.getvalue()
            except Exception as exc:
                raise RuntimeError(f"FIGURE_EVIDENCE_MISSING: unreadable embedded image p{page_num}: {exc}")
            path = cache_dir / f"fig_p{page_num}_embedded_{idx+1}.png"
            path.write_bytes(img_bytes)
            cap_area = fitz.Rect(max(0, rect.x0 - 15), rect.y1,
                                 min(page.rect.width, rect.x1 + 15),
                                 min(page.rect.height, rect.y1 + 50))
            caption = page.get_text("text", clip=cap_area).strip()
            match = re.search(r"(?:fig(?:ure)?\.?|شكل|وثيقة)\s*(\d+[a-z]?)", caption, re.I)
            label = match.group(1).lower() if match else None
            figures.append({
                "figure_id": f"FIG_P{page_num}_E{idx+1}",
                "printed_number": int(re.match(r"\d+", label).group()) if label else None,
                "printed_label": label,
                "source_page": page_num,
                "bbox": [rect.x0, rect.y0, rect.x1, rect.y1],
                "caption": caption,
                "image_path": str(path),
                "image_sha256": hashlib.sha256(img_bytes).hexdigest(),
                "visual_occupancy": round(area, 3),
                "evidence_method": "EMBEDDED_IMAGE_WITH_SOURCE_BBOX"
            })

    # Vector diagrams are cropped from the genuine PDF geometry.
    if not has_scanned_page:
        for idx, drawing in enumerate(page.get_drawings()):
            rect = drawing["rect"]
            if rect.width < 60 or rect.height < 60:
                continue
            pix = page.get_pixmap(clip=rect, dpi=180)
            path = cache_dir / f"fig_p{page_num}_vector_{idx+1}.png"
            content = pix.tobytes("png")
            path.write_bytes(content)
            figures.append({
                "figure_id": f"FIG_P{page_num}_V{idx+1}", "printed_number": None,
                "printed_label": None, "source_page": page_num,
                "bbox": [rect.x0, rect.y0, rect.x1, rect.y1],
                "caption": "Source PDF vector region", "image_path": str(path),
                "image_sha256": hashlib.sha256(content).hexdigest(),
                "visual_occupancy": round(
                    rect.width * rect.height / (page.rect.width * page.rect.height), 3),
                "evidence_method": "PDF_VECTOR_CROP"
            })

    if has_scanned_page:
        # OCR cannot reveal where Fig. 3a, Fig. 3b, etc. are. Ask an approved
        # vision provider for coordinates, then crop *the original PDF page*.
        assert_authorized_source_vision(lesson_id, book_id, page_num)
        pix = page.get_pixmap(dpi=180)
        prompt = (
            "Inspect this original scanned school textbook page. Return ONLY JSON "
            "with a figures array. Identify each actual labelled Fig./Figure diagram "
            "or photo separately; never return the whole page or a paragraph. "
            "Each figure has printed_label (e.g. 3a, 3b, 6 or null), "
            "bbox_1000=[left,top,right,bottom] normalized to 0..1000, "
            "caption (verbatim when readable), visual_description and confidence 0..1. "
            "Do not invent diagram labels or content. Empty array if none."
        )
        page_image = base64.b64encode(pix.tobytes("png")).decode("ascii")
        extracted = None
        response_shape = "no response"
        # A vision model may return valid JSON with the WRONG root object.
        # Re-ask on the SAME approved source page, never fabricate a box and
        # never weaken downstream source-figure matching / scientific review.
        for attempt in range(1, 3):
            request_prompt = prompt
            if attempt == 2:
                request_prompt += (
                    '\\nYour previous reply did NOT match the required structure. '
                    'Use precisely this JSON root shape: '
                    '{"figures":[{"printed_label":"3a","bbox_1000":'
                    '[100,120,450,390],"caption":"","visual_description":'
                    '"","confidence":0.9}]}. The example is ONLY a schema '
                    'illustration, NOT evidence: replace all values solely '
                    'with figures actually visible in the attached page. '
                    'If the page contains no figures, reply {"figures":[]}. '
                    'Do not return any other keys or explanations.'
                )
            raw_figures = execute_llm_completion(
                request_prompt, json_mode=True, image_base64=page_image,
                vision_context={
                    "lesson_id": lesson_id,
                    "book_id": book_id,
                    "pdf_page": page_num,
                })
            vision_provenance = get_last_llm_provenance()
            try:
                proposed = json.loads(raw_figures)
            except (ValueError, TypeError):
                response_shape = "invalid_json"
                proposed = None
            if isinstance(proposed, dict):
                response_shape = ",".join(sorted(str(k)[:40] for k in proposed))[:160] or "empty_object"
                if isinstance(proposed.get("figures"), list):
                    extracted = proposed
                    break
                # Groq JSON mode can wrap the requested figures in "list" or
                # return a SINGLE figure object. Normalize structure only:
                # coordinates, labels, confidence and scientific evidence are
                # still independently validated below.
                if (set(proposed) == {"list"}
                        and isinstance(proposed["list"], list)
                        and all(isinstance(v, dict) for v in proposed["list"])):
                    extracted = {"figures": proposed["list"]}
                    progress("FIGURE_VISION_SCHEMA_NORMALIZED", page=page_num,
                             original_shape="list", figure_candidates=len(proposed["list"]))
                    break
                if "bbox_1000" in proposed and "confidence" in proposed:
                    extracted = {"figures": [proposed]}
                    progress("FIGURE_VISION_SCHEMA_NORMALIZED", page=page_num,
                             original_shape="single_figure", figure_candidates=1)
                    break
            elif isinstance(proposed, list):
                response_shape = "array"
                if all(isinstance(v, dict) for v in proposed):
                    extracted = {"figures": proposed}
                    progress("FIGURE_VISION_SCHEMA_NORMALIZED", page=page_num,
                             original_shape="array", figure_candidates=len(proposed))
                    break
            elif proposed is not None:
                response_shape = type(proposed).__name__
            progress("FIGURE_VISION_SCHEMA_CHECK", page=page_num,
                     attempt=attempt, valid=extracted is not None,
                     response_shape=response_shape)
        if extracted is None:
            raise RuntimeError(
                f"FIGURE_EVIDENCE_MISSING: page={page_num} vision figure "
                f"schema invalid after 2 attempts; response_shape={response_shape}"
            )
        progress("FIGURE_VISION_SCHEMA_VALID", page=page_num,
                 figure_candidates=len(extracted["figures"]))
        rejected_figures = []
        for idx, info in enumerate(extracted["figures"]):
            if not isinstance(info, dict):
                rejected_figures.append("not_an_object")
                continue
            try:
                confidence = float(info.get("confidence", 0))
            except (ValueError, TypeError):
                confidence = 0.0
            if confidence < 0.75:
                rejected_figures.append("low_or_missing_confidence")
                continue
            coords = info.get("bbox_1000")
            if (not isinstance(coords, list) or len(coords) != 4
                    or not all(isinstance(v, (int, float)) for v in coords)):
                continue
            x0, y0, x1, y1 = [float(v) for v in coords]
            if not (0 <= x0 < x1 <= 1000 and 0 <= y0 < y1 <= 1000
                    and (x1-x0) >= 25 and (y1-y0) >= 25):
                continue
            rect = fitz.Rect(page.rect.x0 + x0*page.rect.width/1000,
                             page.rect.y0 + y0*page.rect.height/1000,
                             page.rect.x0 + x1*page.rect.width/1000,
                             page.rect.y0 + y1*page.rect.height/1000)
            label_raw = str(info.get("printed_label") or "").strip().lower()
            label_match = re.fullmatch(
                r"(?:fig(?:ure)?\.?\s*)?(\d+)([a-z]?)\.?",
                label_raw, re.I)
            if not label_match:
                # The model sometimes puts the authentic "Fig. 1" label in
                # caption instead of printed_label. Accept this exact
                # structural format, not an inferred figure number.
                label_match = re.match(
                    r"\s*(?:fig(?:ure)?\.?\s*)(\d+)([a-z]?)(?![\da-z])",
                    str(info.get("caption") or "").lower(), re.I)
            label = (label_match.group(1) + label_match.group(2)
                     if label_match else "")
            # Never infer figure numbers by left-to-right order. On genuine
            # scanned pages, captions are often *below* the vision bounding
            # box and Groq may omit printed_label. Read ONLY the adjoining
            # physical caption strip using LOCAL OCR; the figure number must
            # appear directly next to this source image, not elsewhere on page.
            if shutil.which("tesseract"):
                caption_rect = fitz.Rect(
                    max(page.rect.x0, rect.x0 - 4),
                    max(page.rect.y0, rect.y1 - 12),
                    min(page.rect.x1, rect.x1 + 4),
                    min(page.rect.y1, rect.y1 + 56),
                )
                if caption_rect.width > 25 and caption_rect.height > 15:
                    with tempfile.TemporaryDirectory(
                            prefix="nabil_caption_") as cap_dir:
                        cap_path = Path(cap_dir) / "caption.png"
                        page.get_pixmap(clip=caption_rect, dpi=300).save(
                            str(cap_path))
                        cap_proc = subprocess.run(
                            ["tesseract", str(cap_path), "stdout",
                             "-l", "eng+fra", "--psm", "6"],
                            capture_output=True, text=True, timeout=16)
                    if cap_proc.returncode == 0:
                        caption_source = cap_proc.stdout.strip()
                        source_labels = {
                            m.group(1) + m.group(2).lower()
                            for m in re.finditer(
                                r"(?i)\bfig(?:ure)?[\.,:]?\s*"
                                r"(\d+)([a-z]?)\s*[:;\.,]?",
                                caption_source)
                        }
                        if len(source_labels) == 1:
                            source_label = next(iter(source_labels))
                            if label and label != source_label:
                                progress("FIGURE_LABEL_SOURCE_CONFLICT",
                                         page=page_num,
                                         claimed=label, source=source_label)
                                continue
                            label = source_label
                            label_match = re.fullmatch(
                                r"(\d+)([a-z]?)", label)
                            progress("FIGURE_LABEL_LOCAL_SOURCE_VERIFIED",
                                     page=page_num, figure_label=label,
                                     caption_excerpt=caption_source[:120])
                        elif len(source_labels) > 1:
                            progress("FIGURE_CAPTION_AMBIGUOUS",
                                     page=page_num,
                                     labels=sorted(source_labels))
                            continue
            content = page.get_pixmap(clip=rect, dpi=180).tobytes("png")
            path = cache_dir / f"fig_p{page_num}_scanned_{idx+1}.png"
            path.write_bytes(content)
            figures.append({
                "figure_id": f"FIG_P{page_num}_SCAN_{idx+1}",
                "printed_number": int(label_match.group(1)) if label_match else None,
                "printed_label": label or None, "source_page": page_num,
                "bbox": [rect.x0, rect.y0, rect.x1, rect.y1],
                "caption": str(info.get("caption") or ""),
                "visual_description": str(info.get("visual_description") or ""),
                "image_path": str(path),
                "image_sha256": hashlib.sha256(content).hexdigest(),
                "visual_occupancy": round(
                    rect.width*rect.height/(page.rect.width*page.rect.height), 3),
                "confidence": confidence,
                "ai_provenance": dict(vision_provenance),
                "evidence_method": "APPROVED_VISION_BOX_CROPPED_FROM_SOURCE_PDF"
            })
        progress("FIGURE_VISION_CROPS_VERIFIED", page=page_num,
                 candidates=len(extracted["figures"]),
                 accepted=len(figures),
                 printed_labels=[f.get("printed_label") for f in figures],
                 rejected=rejected_figures[:8])
    return figures


def _normalize_targeted_figure_payload(payload: Any, page_num: int) -> List[dict]:
    """Normalize only container shape; scientific/source checks happen later."""
    if isinstance(payload, list):
        progress("TARGETED_FIGURE_SCHEMA_NORMALIZED", page=page_num,
                 original_shape="array", candidates=len(payload))
        return payload
    if isinstance(payload, dict):
        figures = payload.get("figures")
        if isinstance(figures, list):
            progress("TARGETED_FIGURE_SCHEMA_VALID", page=page_num,
                     original_shape="object.figures", candidates=len(figures))
            return figures
        for key in ("list", "items", "data"):
            figures = payload.get(key)
            if isinstance(figures, list):
                progress("TARGETED_FIGURE_SCHEMA_NORMALIZED", page=page_num,
                         original_shape=f"object.{key}",
                         candidates=len(figures))
                return figures
    raise RuntimeError(
        f"FIGURE_EVIDENCE_MISSING: targeted rescue schema invalid p{page_num}")


def rescue_missing_labeled_figures(doc, page_num: int, cache_dir: Path,
                                   lesson_id: str, book_id: str,
                                   missing_labels: set,
                                   existing_figures: List[Dict[str, Any]]
                                   ) -> List[Dict[str, Any]]:
    """Second-pass rescue for source labels missed by the normal vision pass.

    Vision proposes image/caption boxes at higher resolution; LOCAL OCR of the
    proposed caption box must independently verify exactly that printed label.
    No figure number is inferred from order or neighboring figures.
    """
    import fitz

    wanted = {
        str(label).strip().lower() for label in missing_labels
        if re.fullmatch(r"\d+[a-z]?", str(label).strip().lower())
    }
    existing = {
        str(f.get("printed_label") or "").strip().lower()
        for f in existing_figures
    }
    wanted -= existing
    if not wanted:
        return []

    assert_authorized_source_vision(lesson_id, book_id, page_num)
    page = doc[page_num - 1]
    page_png = page.get_pixmap(dpi=300).tobytes("png")
    page_b64 = base64.b64encode(page_png).decode("ascii")
    prompt = (
        "TARGETED SOURCE-FIGURE RESCUE. Inspect this original textbook page at "
        "high resolution. Locate ONLY these missing printed figure labels: "
        f"{sorted(wanted)}. For each label that is actually visible, return "
        "one object with printed_label, image_bbox_1000 (the image/diagram only, "
        "not neighboring figures), caption_bbox_1000 (tight box containing its "
        "printed 'Fig. N' caption), and confidence 0..1. Never infer a label "
        "from left-to-right order. Never merge two figures into one box. "
        "If a requested printed label cannot be seen, omit it. Return JSON "
        "exactly as {'figures':[...]} and no explanation."
    )
    raw = execute_llm_completion(
        prompt, json_mode=True, image_base64=page_b64,
        vision_context={
            "lesson_id": lesson_id,
            "book_id": book_id,
            "pdf_page": page_num,
        })
    rescue_provenance = get_last_llm_provenance()
    candidates = _normalize_targeted_figure_payload(
        json.loads(raw), page_num)

    def norm_rect(coords):
        if (not isinstance(coords, list) or len(coords) != 4
                or not all(isinstance(v, (int, float)) for v in coords)):
            return None
        x0, y0, x1, y1 = [float(v) for v in coords]
        if not (0 <= x0 < x1 <= 1000 and 0 <= y0 < y1 <= 1000):
            return None
        return fitz.Rect(
            page.rect.x0 + x0 * page.rect.width / 1000,
            page.rect.y0 + y0 * page.rect.height / 1000,
            page.rect.x0 + x1 * page.rect.width / 1000,
            page.rect.y0 + y1 * page.rect.height / 1000,
        )

    def local_caption_fallback(label: str, image_rect):
        """Locate an exact source Fig/Figure label by LOCAL full-page OCR.

        This is used only when the provider's proposed caption box is wrong.
        The external model still proposes the figure image box; local OCR must
        independently find exactly one matching printed label physically next
        to that box. Nothing is inferred from figure order.
        """
        with tempfile.TemporaryDirectory(
                prefix="nabil_targeted_page_ocr_") as page_ocr_dir:
            full_path = Path(page_ocr_dir) / "page.png"
            full_pix = page.get_pixmap(dpi=350)
            full_pix.save(str(full_path))
            proc = subprocess.run(
                ["tesseract", str(full_path), "stdout",
                 "-l", "eng+fra", "--psm", "6", "tsv"],
                capture_output=True, text=True, timeout=35)
        if proc.returncode != 0 or not proc.stdout.strip():
            return None

        rows = []
        raw_lines = proc.stdout.splitlines()
        if not raw_lines:
            return None
        header = raw_lines[0].split("\t")
        for raw_line in raw_lines[1:]:
            cols = raw_line.split("\t")
            if len(cols) != len(header):
                continue
            row = dict(zip(header, cols))
            if row.get("level") != "5":
                continue
            token = str(row.get("text") or "").strip()
            if not token:
                continue
            try:
                row["_left"] = int(row["left"])
                row["_top"] = int(row["top"])
                row["_width"] = int(row["width"])
                row["_height"] = int(row["height"])
            except (KeyError, TypeError, ValueError):
                continue
            rows.append(row)

        grouped = {}
        for row in rows:
            key = (
                row.get("block_num"), row.get("par_num"),
                row.get("line_num"))
            grouped.setdefault(key, []).append(row)

        occurrences = []
        wanted_norm = re.sub(r"[^0-9a-z]", "", label.casefold())
        for line_rows in grouped.values():
            line_rows.sort(key=lambda row: row["_left"])
            for pos, row in enumerate(line_rows):
                token = str(row.get("text") or "")
                token_letters = re.sub(
                    r"[^a-z]", "", token.casefold())
                match_rows = None
                if re.fullmatch(
                        rf"(?i)fig(?:ure)?[\.,:]?{re.escape(wanted_norm)}[\.:;]?",
                        token):
                    match_rows = [row]
                elif token_letters in ("fig", "figure"):
                    for nxt in line_rows[pos + 1:pos + 3]:
                        nxt_norm = re.sub(
                            r"[^0-9a-z]", "",
                            str(nxt.get("text") or "").casefold())
                        if nxt_norm == wanted_norm:
                            match_rows = [row, nxt]
                            break
                if not match_rows:
                    continue

                px0 = min(r["_left"] for r in match_rows)
                py0 = min(r["_top"] for r in match_rows)
                px1 = max(r["_left"] + r["_width"] for r in match_rows)
                py1 = max(r["_top"] + r["_height"] for r in match_rows)
                label_rect = fitz.Rect(
                    page.rect.x0 + px0 * page.rect.width / full_pix.width,
                    page.rect.y0 + py0 * page.rect.height / full_pix.height,
                    page.rect.x0 + px1 * page.rect.width / full_pix.width,
                    page.rect.y0 + py1 * page.rect.height / full_pix.height,
                )
                horizontal_gap = max(
                    0.0, image_rect.x0 - label_rect.x1,
                    label_rect.x0 - image_rect.x1)
                vertical_gap = max(
                    0.0, image_rect.y0 - label_rect.y1,
                    label_rect.y0 - image_rect.y1)
                # A real caption should be very close to its figure. This
                # rejects body text such as "Observe figure 1" elsewhere.
                if (horizontal_gap <= page.rect.width * 0.12
                        and vertical_gap <= page.rect.height * 0.08):
                    occurrences.append(label_rect)

        if len(occurrences) != 1:
            progress(
                "TARGETED_FIGURE_LOCAL_PAGE_LABEL_AMBIGUOUS",
                page=page_num, label=label,
                adjacent_matches=len(occurrences))
            return None

        label_rect = occurrences[0]
        caption_rect = fitz.Rect(
            max(page.rect.x0,
                image_rect.x0 - page.rect.width * 0.015),
            max(page.rect.y0,
                label_rect.y0 - page.rect.height * 0.008),
            min(page.rect.x1,
                image_rect.x1 + page.rect.width * 0.015),
            min(page.rect.y1,
                label_rect.y1 + page.rect.height * 0.018),
        )
        progress(
            "TARGETED_FIGURE_LOCAL_PAGE_LABEL_VERIFIED",
            page=page_num, label=label,
            method="FULL_PAGE_LOCAL_OCR_ADJACENT_TO_MODEL_IMAGE")
        return caption_rect

    rescued = []
    for idx, item in enumerate(candidates):
        if not isinstance(item, dict):
            continue
        raw_label = str(item.get("printed_label") or "").strip().lower()
        m = re.fullmatch(r"(?:fig(?:ure)?\.?\s*)?(\d+)([a-z]?)\.?",
                         raw_label, re.I)
        label = (m.group(1) + m.group(2).lower()) if m else ""
        if label not in wanted:
            continue
        try:
            confidence = float(item.get("confidence", 0))
        except (TypeError, ValueError):
            confidence = 0.0
        if confidence < 0.80:
            progress("TARGETED_FIGURE_RESCUE_REJECTED", page=page_num,
                     label=label, reason="LOW_CONFIDENCE")
            continue

        image_rect = norm_rect(item.get("image_bbox_1000"))
        caption_rect = norm_rect(item.get("caption_bbox_1000"))
        if image_rect is None or caption_rect is None:
            progress("TARGETED_FIGURE_RESCUE_REJECTED", page=page_num,
                     label=label, reason="INVALID_BBOX")
            continue
        if image_rect.width < 20 or image_rect.height < 20:
            progress("TARGETED_FIGURE_RESCUE_REJECTED", page=page_num,
                     label=label, reason="IMAGE_BBOX_TOO_SMALL")
            continue

        # A model may return an extremely tight box around the printed
        # "Fig. N" token. Expand only the caption box locally before OCR;
        # the actual figure crop is never enlarged or inferred. Acceptance
        # still requires unique LOCAL OCR of the requested source label.
        if caption_rect.width < 24 or caption_rect.height < 14:
            cx = (caption_rect.x0 + caption_rect.x1) / 2
            cy = (caption_rect.y0 + caption_rect.y1) / 2
            half_w = max(12.0, caption_rect.width / 2 + 8.0)
            half_h = max(7.0, caption_rect.height / 2 + 5.0)
            caption_rect = fitz.Rect(
                max(page.rect.x0, cx - half_w),
                max(page.rect.y0, cy - half_h),
                min(page.rect.x1, cx + half_w),
                min(page.rect.y1, cy + half_h),
            )
            progress("TARGETED_FIGURE_CAPTION_BOX_PADDED",
                     page=page_num, label=label,
                     width=round(caption_rect.width, 1),
                     height=round(caption_rect.height, 1))

        # The caption must be physically close to its proposed source figure;
        # this prevents a valid Fig. 1 caption elsewhere on the page from
        # authorizing the wrong crop.
        horizontal_gap = max(
            0.0, image_rect.x0 - caption_rect.x1,
            caption_rect.x0 - image_rect.x1)
        vertical_gap = max(
            0.0, image_rect.y0 - caption_rect.y1,
            caption_rect.y0 - image_rect.y1)
        if (horizontal_gap > page.rect.width * 0.12
                or vertical_gap > page.rect.height * 0.16):
            progress("TARGETED_FIGURE_RESCUE_REJECTED", page=page_num,
                     label=label, reason="CAPTION_NOT_ADJACENT")
            continue

        with tempfile.TemporaryDirectory(
                prefix="nabil_targeted_caption_") as cap_dir:
            cap_path = Path(cap_dir) / "caption.png"
            page.get_pixmap(
                clip=caption_rect, dpi=350).save(str(cap_path))
            proc = subprocess.run(
                ["tesseract", str(cap_path), "stdout",
                 "-l", "eng+fra", "--psm", "6"],
                capture_output=True, text=True, timeout=20)
        if proc.returncode != 0:
            progress("TARGETED_FIGURE_RESCUE_REJECTED", page=page_num,
                     label=label, reason="LOCAL_OCR_FAILED")
            continue

        caption_source = proc.stdout.strip()
        source_labels = {
            mm.group(1) + mm.group(2).lower()
            for mm in re.finditer(
                r"(?i)\bfig(?:ure)?[\.,:]?\s*"
                r"(\d+)([a-z]?)\s*[:;\.,]?",
                caption_source)
        }
        if source_labels != {label}:
            # The provider may have returned a caption box on nearby body
            # text even when its image box is correct. Do not trust or widen
            # that box blindly. Re-locate the requested printed label using
            # LOCAL full-page OCR and require a unique occurrence physically
            # adjacent to the proposed source image.
            fallback_rect = local_caption_fallback(label, image_rect)
            if fallback_rect is not None:
                with tempfile.TemporaryDirectory(
                        prefix="nabil_targeted_caption_fallback_") as cap_dir:
                    cap_path = Path(cap_dir) / "caption.png"
                    page.get_pixmap(
                        clip=fallback_rect, dpi=350).save(str(cap_path))
                    retry_proc = subprocess.run(
                        ["tesseract", str(cap_path), "stdout",
                         "-l", "eng+fra", "--psm", "6"],
                        capture_output=True, text=True, timeout=20)
                if retry_proc.returncode == 0:
                    retry_source = retry_proc.stdout.strip()
                    retry_labels = {
                        mm.group(1) + mm.group(2).lower()
                        for mm in re.finditer(
                            r"(?i)\bfig(?:ure)?[\.,:]?\s*"
                            r"(\d+)([a-z]?)\s*[:;\.,]?",
                            retry_source)
                    }
                    if retry_labels == {label}:
                        caption_rect = fallback_rect
                        caption_source = retry_source
                        source_labels = retry_labels
                        progress(
                            "TARGETED_FIGURE_CAPTION_RECOVERED_LOCALLY",
                            page=page_num, label=label,
                            caption_excerpt=caption_source[:120])

        if source_labels != {label}:
            progress("TARGETED_FIGURE_RESCUE_REJECTED", page=page_num,
                     label=label,
                     reason="LOCAL_CAPTION_LABEL_NOT_UNIQUE",
                     source_labels=sorted(source_labels),
                     caption_excerpt=caption_source[:120])
            continue

        image_bytes = page.get_pixmap(
            clip=image_rect, dpi=220).tobytes("png")
        path = cache_dir / (
            f"fig_p{page_num}_targeted_{label}_{idx+1}.png")
        path.write_bytes(image_bytes)
        rescued.append({
            "figure_id": f"FIG_P{page_num}_TARGET_{label}",
            "printed_number": int(re.match(r"\d+", label).group()),
            "printed_label": label,
            "source_page": page_num,
            "bbox": [
                image_rect.x0, image_rect.y0,
                image_rect.x1, image_rect.y1,
            ],
            "caption": caption_source,
            "visual_description": "",
            "image_path": str(path),
            "image_sha256": hashlib.sha256(image_bytes).hexdigest(),
            "visual_occupancy": round(
                image_rect.width * image_rect.height /
                (page.rect.width * page.rect.height), 3),
            "confidence": confidence,
            "ai_provenance": dict(rescue_provenance),
            "evidence_method":
                "TARGETED_HIGHRES_VISION_PLUS_LOCAL_CAPTION_OCR",
        })
        progress("TARGETED_FIGURE_RESCUE_ACCEPTED", page=page_num,
                 label=label, caption_excerpt=caption_source[:120])

    return rescued


def match_figure_to_item(item: dict, page_figures: List[Dict[str, Any]], page_rect) -> List[str]:
    """Match by source figure number/letter, never by any random image on page."""
    prompt = item.get("exact_source_prompt", item.get("raw_text", ""))
    mentioned = re.findall(
        r"(?:fig(?:ure)?\.?|document|doc|شكل|وثيقة)\s*(\d+[a-z]?)",
        prompt, re.I,
    )
    wanted = {label.casefold() for label in mentioned}
    if wanted:
        matches = []
        for fig in page_figures:
            label = str(fig.get("printed_label") or "").casefold()
            number = str(fig.get("printed_number") or "")
            if any((w == label or (not re.search(r"[a-z]$", w) and w == number))
                   for w in wanted):
                matches.append(fig["figure_id"])
        if not matches:
            raise RuntimeError(f"FIGURE_EVIDENCE_MISSING: Source labelled figures {sorted(wanted)} were not extracted")
        return list(dict.fromkeys(matches))

    if item.get("requires_figure"):
        raise RuntimeError("FIGURE_EVIDENCE_MISSING: Diagram required but textbook figure identity is unverified")
    return []


def verify_title_double_evidence_strict(doc, entry: dict, opening_txt: str) -> bool:
    """Require both the chapter opener and the real book TOC. Never infer TOC
    from a filename or submit unauthorized preface pages to an AI provider.
    The canonical catalog records the TOC PDF page for scanned textbooks.
    """
    title_clean = re.sub(r"[^\w]+", " ", entry["canonical_title"].casefold()).strip()
    opener = re.sub(r"[^\w]+", " ", opening_txt.casefold())
    if not title_clean:
        return False
    if title_clean not in opener:
        # Stylized printed headers are often missed by full-page OCR even
        # when body text is readable. Re-read the real PDF header locally.
        import fitz
        page_no = int(entry["pdf_start_page"])
        page = doc[page_no - 1]
        r = page.rect
        header = page.get_pixmap(
            clip=fitz.Rect(r.x0, r.y0, r.x1, r.y0 + r.height * 0.20),
            dpi=300)
        with tempfile.TemporaryDirectory(prefix="nabil_title_ocr_") as directory:
            image_path = Path(directory) / "opening_header.png"
            header.save(str(image_path))
            proc = subprocess.run(
                ["tesseract", str(image_path), "stdout", "-l", "eng+fra",
                 "--psm", "6"],
                capture_output=True, text=True, timeout=35)
        if proc.returncode != 0:
            raise RuntimeError(
                f"TITLE_VERIFICATION_FAILED: chapter opening OCR unavailable p{page_no}")
        opener_header = re.sub(
            r"[^\w]+", " ", proc.stdout.casefold()).strip()
        if title_clean not in opener_header:
            progress("TITLE_OPENING_EVIDENCE_FAILED", page=page_no,
                     expected_title=entry["canonical_title"],
                     header_excerpt=opener_header[:180])
            return False
        progress("TITLE_OPENING_HEADER_VERIFIED", page=page_no,
                 title=entry["canonical_title"],
                 method="SOURCE_HEADER_LOCAL_OCR_300DPI")

    toc_page = entry.get("toc_pdf_page")
    if toc_page is None:
        # Native-text PDFs may expose a genuine PDF bookmark TOC.
        for depth, name, p_num in doc.get_toc():
            if re.sub(r"[^\w]+", " ", name.casefold()).strip() == title_clean:
                return 1 <= p_num <= int(entry["pdf_start_page"])
        return False

    toc_page = int(toc_page)
    if not 1 <= toc_page <= len(doc) or toc_page >= int(entry["pdf_start_page"]):
        return False
    toc_txt = (doc[toc_page - 1].get_text() or "").strip()
    if not toc_txt:
        if not shutil.which("tesseract"):
            raise RuntimeError("DEPENDENCY_MISSING:tesseract for scanned textbook TOC")
        # Local OCR: exactly the catalogued TOC page, NOT an external transfer.
        cache = CACHE_DIR / f"toc_{entry['book_id']}_p{toc_page}.txt"
        if cache.exists():
            toc_txt = cache.read_text(encoding="utf-8")
        else:
            with tempfile.TemporaryDirectory() as temp_dir:
                image_path = Path(temp_dir) / "toc.png"
                doc[toc_page - 1].get_pixmap(dpi=200).save(str(image_path))
                proc = subprocess.run(
                    ["tesseract", str(image_path), "stdout", "-l", "eng+fra", "--psm", "3"],
                    capture_output=True, text=True, timeout=60,
                )
            if proc.returncode != 0:
                raise RuntimeError("TITLE_VERIFICATION_FAILED: local TOC OCR unavailable")
            toc_txt = proc.stdout.strip()
            if toc_txt:
                cache.write_text(toc_txt, encoding="utf-8")
    toc_normalized = re.sub(r"[^\w]+", " ", toc_txt.casefold())
    return title_clean in toc_normalized and (
        "chapter" in toc_normalized or "chapitre" in toc_normalized
        or "contents" in toc_normalized or "فهرس" in toc_normalized
    )

def _execute_llm_json_strict(
        prompt: str,
        *,
        image_base64: Optional[str] = None,
        vision_context: Optional[Dict[str, Any]] = None,
        purpose: str = "factory_json",
        max_attempts: int = 3) -> Any:
    """Require parseable RFC-8259 JSON; retry from the original source if malformed.

    We deliberately do NOT repair malformed source transcriptions after the
    fact. A repair model could alter quoted textbook text. Instead, every retry
    re-reads the same authorized source image with a stricter serialization
    contract, preserving the source-first/fail-closed guarantee.
    """
    attempts = max(1, min(4, int(max_attempts)))
    base_prompt = str(prompt)
    strict_suffix = (
        "\n\nSTRICT JSON SERIALIZATION CONTRACT:\n"
        "- Return exactly one valid RFC-8259 JSON value and nothing else.\n"
        "- Use double quotes for every object key and every JSON string.\n"
        "- Escape every double quote, backslash, newline, tab, and other "
        "control character inside string values correctly.\n"
        "- No comments, no trailing commas, no Markdown fences, no Python "
        "dict syntax, and no explanatory text outside the JSON.\n"
        "- Preserve source wording exactly; serialization escaping must not "
        "change the underlying textbook text."
    )
    # A malformed JSON response is a provider-quality failure, not a reason
    # to ask the same provider for the same malformed serialization three
    # times. Rotate through configured/authorized providers while always
    # re-reading the ORIGINAL source image.
    configured = _provider_order(
        os.getenv("NABIL_FACTORY_AI_PROVIDER", "auto").strip().lower(),
        _provider_keys(),
    )
    if image_base64 and vision_context is not None:
        configured = [
            p for p in configured
            if _vision_provider_authorized(
                p, vision_context, require_key=True)
        ]
    if not configured:
        raise RuntimeError(
            "AI_JSON_RETRY_NO_AUTHORIZED_PROVIDER:"
            f"{purpose}")

    last_error = None
    malformed_providers = set()
    for attempt in range(1, attempts + 1):
        preferred_retry_provider = configured[(attempt - 1) % len(configured)]
        effective_prompt = (
            base_prompt if attempt == 1
            else base_prompt + strict_suffix +
            f"\nThis is strict JSON retry {attempt} of {attempts}."
        )
        raw = execute_llm_completion(
            effective_prompt,
            json_mode=True,
            temperature=0.0,
            image_base64=image_base64,
            vision_context=vision_context,
            preferred_provider_override=preferred_retry_provider,
            excluded_providers=malformed_providers,
        )
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            last_error = exc
            actual_bad_provider = get_last_llm_provenance().get("provider")
            if actual_bad_provider:
                malformed_providers.add(str(actual_bad_provider).lower())
            progress(
                "AI_JSON_INVALID_RETRY",
                purpose=purpose,
                attempt=attempt,
                max_attempts=attempts,
                line=exc.lineno,
                column=exc.colno,
                char=exc.pos,
                provider=get_last_llm_provenance().get("provider"),
                model=get_last_llm_provenance().get("model"),
                preferred_retry_provider=preferred_retry_provider,
                retry_provider_cycle=configured,
                excluded_after_malformed=sorted(malformed_providers),
                image_request=bool(image_base64),
                vision_context=vision_context if image_base64 else None,
            )
    raise RuntimeError(
        f"AI_JSON_INVALID_AFTER_RETRIES:{purpose}:"
        f"line={getattr(last_error, 'lineno', 0)}:"
        f"column={getattr(last_error, 'colno', 0)}"
    ) from last_error


def _normalize_exercise_scan_payload(payload: Any, page_num: int) -> List[dict]:
    """Accept the provider's semantically equivalent array/object JSON roots."""
    if isinstance(payload, list):
        progress("EXERCISE_VISION_SCHEMA_NORMALIZED", page=page_num,
                 original_shape="array", exercise_candidates=len(payload))
        return payload
    if isinstance(payload, dict):
        rows = payload.get("exercises")
        if isinstance(rows, list):
            progress("EXERCISE_VISION_SCHEMA_VALID", page=page_num,
                     original_shape="object.exercises",
                     exercise_candidates=len(rows))
            return rows
        for key in ("items", "list", "data"):
            rows = payload.get(key)
            if isinstance(rows, list):
                progress("EXERCISE_VISION_SCHEMA_NORMALIZED", page=page_num,
                         original_shape=f"object.{key}",
                         exercise_candidates=len(rows))
                return rows
    raise RuntimeError(
        f"EXERCISE_SOURCE_MISMATCH: invalid scan evidence p{page_num}")


def _normalize_exercise_review_payload(payload: Any, page_num: int) -> List[dict]:
    """Normalize the independent review response without weakening validation."""
    if isinstance(payload, list):
        progress("EXERCISE_REVIEW_SCHEMA_NORMALIZED", page=page_num,
                 original_shape="array", checks=len(payload))
        return payload
    if isinstance(payload, dict):
        checks = payload.get("checks")
        if isinstance(checks, list):
            progress("EXERCISE_REVIEW_SCHEMA_VALID", page=page_num,
                     original_shape="object.checks", checks=len(checks))
            return checks
        for key in ("items", "list", "data"):
            checks = payload.get(key)
            if isinstance(checks, list):
                progress("EXERCISE_REVIEW_SCHEMA_NORMALIZED", page=page_num,
                         original_shape=f"object.{key}", checks=len(checks))
                return checks
    raise RuntimeError(
        f"EXERCISE_SOURCE_MISMATCH: review missing p{page_num}")


def _rescue_unverified_exercise(
        page, row: dict, page_num: int, lesson_id: str, book_id: str) -> Optional[dict]:
    """Re-read one rejected exercise from a high-resolution source crop.

    This is stricter than accepting the first page transcription: the candidate
    bbox is cropped from the original PDF, re-transcribed, then independently
    audited against that exact crop. No guessed repair is allowed.
    """
    from fitz import Rect
    try:
        number = int(row.get("number"))
        coords = row.get("bbox_1000")
        if not isinstance(coords, list) or len(coords) != 4:
            return None
        x0, y0, x1, y1 = [float(v) for v in coords]
        if not (0 <= x0 < x1 <= 1000 and 0 <= y0 < y1 <= 1000):
            return None
    except (TypeError, ValueError):
        return None

    # Pad the proposed source region so the circled number and any nearby
    # figure reference are not clipped. Padding is presentation geometry only.
    px = page.rect.width * 0.035
    py = page.rect.height * 0.025
    rect = Rect(
        max(page.rect.x0, x0 * page.rect.width / 1000 - px),
        max(page.rect.y0, y0 * page.rect.height / 1000 - py),
        min(page.rect.x1, x1 * page.rect.width / 1000 + px),
        min(page.rect.y1, y1 * page.rect.height / 1000 + py),
    )
    crop_bytes = page.get_pixmap(clip=rect, dpi=320).tobytes("png")
    crop_b64 = base64.b64encode(crop_bytes).decode("ascii")
    context = {
        "lesson_id": lesson_id,
        "book_id": book_id,
        "pdf_page": page_num,
    }
    prompt = (
        f"This is a HIGH-RESOLUTION crop from the original textbook page. "
        f"Verify and transcribe ONLY the visibly printed exercise numbered {number}. "
        "Return one JSON object with: verified_visible_number (bool), number "
        "(integer), section_type (EXERCISE or PROBLEM), exact_source_prompt "
        "(all visible words and blanks verbatim, do not solve), subquestions "
        "(array of exact strings), figure_labels (array of exact printed figure "
        "labels), blank_count (integer), confidence (0..1), unreadable_parts "
        "(array). Represent EVERY visibly empty answer box, underline blank, or "
        "fill-in slot in exact_source_prompt with the literal token [BLANK] in "
        "its exact reading position. Empty boxes are source content and must not "
        "disappear. blank_count must equal the number of visible answer blanks. "
        "If the requested exercise number is not visibly present and readable "
        "in this crop, set verified_visible_number=false. Do not infer missing "
        "words and do not correct the textbook."
    )
    payload = _execute_llm_json_strict(
        prompt,
        image_base64=crop_b64,
        vision_context=context,
        purpose=f"exercise_rescue_extract_p{page_num}_n{number}",
    )
    if not isinstance(payload, dict):
        return None
    if payload.get("verified_visible_number") is not True:
        return None
    try:
        if int(payload.get("number")) != number:
            return None
        confidence = float(payload.get("confidence", 0))
    except (TypeError, ValueError):
        return None
    prompt_text = str(payload.get("exact_source_prompt") or "").strip()
    kind = str(payload.get("section_type") or "EXERCISE").upper()
    if (kind not in ("EXERCISE", "PROBLEM") or len(prompt_text) < 10
            or confidence < 0.90 or payload.get("unreadable_parts")):
        return None
    extraction_provenance = get_last_llm_provenance()

    audit_prompt = (
        f"Independently audit the proposed transcription of exercise {number} "
        "against this SAME original high-resolution crop. Return JSON object "
        "with faithful (bool), number_visible (bool), complete (bool), "
        "reason (string). Mark false for any missing word, invented word, "
        "wrong number, wrong item boundary, omitted visible subquestion, or "
        "a missing/misplaced [BLANK] token. Independently count the visible "
        "answer boxes/blanks in the crop and require that count to match "
        "blank_count and the number of [BLANK] tokens in exact_source_prompt. "
        "Proposed transcription: "
        + json.dumps(payload, ensure_ascii=False)
    )
    audit = _execute_llm_json_strict(
        audit_prompt,
        image_base64=crop_b64,
        vision_context=context,
        purpose=f"exercise_rescue_audit_p{page_num}_n{number}",
    )
    audit_provenance = get_last_llm_provenance()
    if not isinstance(audit, dict):
        return None
    if not (audit.get("faithful") is True
            and audit.get("number_visible") is True
            and audit.get("complete") is True):
        progress(
            "EXERCISE_TARGETED_RESCUE_REJECTED",
            page=page_num,
            number=number,
            reason=str(audit.get("reason") or "")[:240],
        )
        return None

    progress(
        "EXERCISE_TARGETED_RESCUE_ACCEPTED",
        page=page_num,
        number=number,
        extraction_provider=extraction_provenance.get("provider"),
        audit_provider=audit_provenance.get("provider"),
        confidence=confidence,
    )
    return {
        "number": number,
        "section_type": kind,
        "exact_source_prompt": prompt_text,
        "subquestions": list(payload.get("subquestions") or []),
        "figure_labels": list(payload.get("figure_labels") or []),
        "bbox_1000": coords,
        "_rescue_crop_rect": [rect.x0, rect.y0, rect.x1, rect.y1],
        "_rescue_crop_bytes": crop_bytes,
        "_rescue_extraction_provenance": dict(extraction_provenance),
        "_rescue_audit_provenance": dict(audit_provenance),
        "confidence": confidence,
        "unreadable_parts": [],
    }


def extract_scanned_page_exercises(doc, page_num: int, lesson_id: str,
                                   book_id: str, cache_dir: Path) -> List[dict]:
    """Read numbered exercise regions from the real page image, not OCR digits.

    Scanned textbooks frequently use circled numbers in two columns, which
    plain OCR mistakes for letters. Two visual passes independently compare
    the proposed prompts against the source page before accepting them.
    """
    assert_authorized_source_vision(lesson_id, book_id, page_num)
    page = doc[page_num - 1]
    image_bytes = page.get_pixmap(dpi=200).tobytes("png")
    page_b64 = base64.b64encode(image_bytes).decode("ascii")
    instruction = (
        "Read this school textbook page, paying attention to TWO-COLUMN reading "
        "order and circled exercise numbers. Return JSON with exercises array. "
        "For every numbered exercise or problem return: number (integer), "
        "section_type (EXERCISE or PROBLEM), exact_source_prompt (all words and "
        "blanks verbatim, do not solve), subquestions (array of exact strings), "
        "bbox_1000 (entire exercise prompt region, normalized x0,y0,x1,y1), "
        "figure_labels (list of exact cited Figure numbers), blank_count "
        "(integer), confidence 0..1, and unreadable_parts (array). Represent "
        "EVERY visibly empty answer box, underline blank, or fill-in slot with "
        "the literal token [BLANK] at its exact reading position, and set "
        "blank_count to the number of visible blanks. Include each exercise exactly once; "
        "do not confuse printed figure numbers, chapter numbers or page "
        "numbers with exercise numbers. Preserve table entries and all "
        "instructions. Do not invent any text. No numbered exercises -> []."
    )
    extracted = _execute_llm_json_strict(
        instruction,
        image_base64=page_b64,
        vision_context={
            "lesson_id": lesson_id,
            "book_id": book_id,
            "pdf_page": page_num,
        },
        purpose=f"exercise_scan_p{page_num}",
    )
    extraction_provenance = get_last_llm_provenance()
    rows = _normalize_exercise_scan_payload(extracted, page_num)
    if not rows:
        # A first-pass page read may miss small circled exercise numbers or a
        # compact two-column exercise page. Re-read the SAME original page at
        # higher resolution before concluding that no exercises exist.
        highres_bytes = page.get_pixmap(dpi=320).tobytes("png")
        highres_b64 = base64.b64encode(highres_bytes).decode("ascii")
        rescue_instruction = (
            "Re-inspect this SAME original textbook page at high resolution. "
            "Return JSON with exercises array containing EVERY visibly numbered "
            "exercise/problem on the page, preserving two-column reading order. "
            "For each item return number, section_type, exact_source_prompt, "
            "subquestions, bbox_1000, figure_labels, blank_count, confidence, "
            "unreadable_parts. Preserve every printed word and every visible "
            "answer blank as [BLANK]. Do not solve, infer, renumber, or invent. "
            "If there are genuinely no numbered exercises, return "
            "{\"exercises\":[]}.")
        rescued_scan = _execute_llm_json_strict(
            rescue_instruction,
            image_base64=highres_b64,
            vision_context={
                "lesson_id": lesson_id,
                "book_id": book_id,
                "pdf_page": page_num,
            },
            purpose=f"exercise_scan_highres_rescue_p{page_num}",
        )
        rows = _normalize_exercise_scan_payload(rescued_scan, page_num)
        if rows:
            extraction_provenance = get_last_llm_provenance()
            page_b64 = highres_b64
            progress(
                "EXERCISE_PAGE_HIGHRES_RESCUE_ACCEPTED",
                page=page_num,
                exercise_candidates=len(rows),
            )
        else:
            progress(
                "EXERCISE_PAGE_HIGHRES_RESCUE_EMPTY",
                page=page_num,
            )
            return []
    audit_prompt = (
        "Independently compare these exercise transcriptions to the PROVIDED "
        "original source page image. Return JSON: "
        "{'checks':[{'number':int,'faithful':bool,'blank_count_visible':int,"
        "'blank_tokens_match':bool,'reason':str}]}. "
        "Mark false for a missing part, wrong figure number, invented words, "
        "wrong item boundaries, incorrect circled-number reading, bad "
        "two-column order, or any missing/misplaced [BLANK] token. Independently "
        "count visible answer blanks for each exercise and reject a transcription "
        "when blank_count or the number of [BLANK] tokens does not match. "
        "No favorable assumptions. Transcriptions: "
        + json.dumps(rows, ensure_ascii=False)
    )
    review = _execute_llm_json_strict(
        audit_prompt,
        image_base64=page_b64,
        vision_context={
            "lesson_id": lesson_id,
            "book_id": book_id,
            "pdf_page": page_num,
        },
        purpose=f"exercise_review_p{page_num}",
    )
    audit_provenance = get_last_llm_provenance()
    checks = _normalize_exercise_review_payload(review, page_num)

    # Do not interpret an incomplete audit schema as a source rejection. Ask
    # again against the SAME source page and SAME candidate transcriptions.
    # This remains fail-closed: no item is approved until every required audit
    # field is explicitly present with the correct type.
    expected_review_numbers = {
        int(row["number"]) for row in rows
        if isinstance(row, dict) and "number" in row
    }

    def _exercise_review_schema_complete(items: List[dict]) -> bool:
        if not isinstance(items, list):
            return False
        seen = set()
        for item in items:
            if not isinstance(item, dict) or "number" not in item:
                return False
            try:
                item_number = int(item["number"])
            except (TypeError, ValueError):
                return False
            if item_number in seen:
                return False
            seen.add(item_number)
            if not isinstance(item.get("faithful"), bool):
                return False
            if not isinstance(item.get("blank_count_visible"), int) or isinstance(
                    item.get("blank_count_visible"), bool):
                return False
            if not isinstance(item.get("blank_tokens_match"), bool):
                return False
            if not isinstance(item.get("reason"), str):
                return False
        return seen == expected_review_numbers

    if not _exercise_review_schema_complete(checks):
        progress(
            "EXERCISE_REVIEW_SCHEMA_RETRY_REQUIRED",
            page=page_num,
            expected_numbers=sorted(expected_review_numbers),
        )
        strict_review_prompt = (
            "Re-audit these candidate exercise transcriptions against the SAME "
            "original textbook page image. Return EXACTLY one strict JSON object "
            "with key checks. checks must contain exactly one object for every "
            "candidate exercise number, no omissions and no extras. Every object "
            "must contain all fields: number (integer), faithful (boolean), "
            "blank_count_visible (integer >= 0), blank_tokens_match (boolean), "
            "reason (string). Count visible answer boxes/blanks independently "
            "from the source image. faithful=false for any missing/invented word, "
            "wrong boundary/number/figure/table entry, or blank mismatch. "
            "Do not repair or reinterpret candidate text. Candidates: "
            + json.dumps(rows, ensure_ascii=False)
        )
        strict_review = _execute_llm_json_strict(
            strict_review_prompt,
            image_base64=page_b64,
            vision_context={
                "lesson_id": lesson_id,
                "book_id": book_id,
                "pdf_page": page_num,
            },
            purpose=f"exercise_review_schema_retry_p{page_num}",
            max_attempts=3,
        )
        checks = _normalize_exercise_review_payload(strict_review, page_num)
        audit_provenance = get_last_llm_provenance()
        if not _exercise_review_schema_complete(checks):
            raise RuntimeError(
                f"EXERCISE_REVIEW_SCHEMA_INCOMPLETE: p{page_num}"
            )
        progress(
            "EXERCISE_REVIEW_SCHEMA_RETRY_ACCEPTED",
            page=page_num,
            checks=len(checks),
        )

    approved = {
        int(x["number"]): x
        for x in checks
        if isinstance(x, dict)
        and "number" in x
        and x.get("faithful") is True
        and x.get("blank_tokens_match") is True
        and isinstance(x.get("blank_count_visible"), int)
    }
    from fitz import Rect
    result = []
    for row in rows:
        if not isinstance(row, dict):
            raise RuntimeError(f"EXERCISE_SOURCE_MISMATCH: unexpected page item p{page_num}")
        number = int(row["number"])
        prompt = str(row.get("exact_source_prompt") or "").strip()
        coords = row.get("bbox_1000")
        rejection_reasons = []
        if number < 1 or number > 999:
            rejection_reasons.append("number_out_of_range")
        if len(prompt) < 10:
            rejection_reasons.append("prompt_too_short")
        if row.get("unreadable_parts"):
            rejection_reasons.append("unreadable_parts")
        try:
            if float(row.get("confidence", 0)) < 0.85:
                rejection_reasons.append("low_confidence")
        except (TypeError, ValueError):
            rejection_reasons.append("invalid_confidence")
        review_item = next(
            (x for x in checks if isinstance(x, dict)
             and str(x.get("number")) == str(number)), {})
        if number not in approved:
            rejection_reasons.append(
                "independent_review_rejected:" +
                str(review_item.get("reason") or "not_approved")[:180])
        else:
            visible_blank_count = int(review_item.get("blank_count_visible", 0))
            token_blank_count = prompt.count("[BLANK]")
            try:
                declared_blank_count = int(row.get("blank_count", -1))
            except (TypeError, ValueError):
                declared_blank_count = -1
            if not (
                declared_blank_count == visible_blank_count
                and token_blank_count == visible_blank_count
            ):
                rejection_reasons.append(
                    "blank_count_mismatch:"
                    f"declared={declared_blank_count},"
                    f"tokens={token_blank_count},"
                    f"visible={visible_blank_count}"
                )
        if not isinstance(coords, list) or len(coords) != 4:
            rejection_reasons.append("invalid_bbox_shape")
        else:
            try:
                bx0, by0, bx1, by1 = [float(v) for v in coords]
                if not (0 <= bx0 < bx1 <= 1000 and 0 <= by0 < by1 <= 1000):
                    rejection_reasons.append("invalid_bbox_bounds")
            except (TypeError, ValueError):
                rejection_reasons.append("invalid_bbox_values")
        kind_candidate = str(row.get("section_type") or "EXERCISE").upper()
        if kind_candidate not in ("EXERCISE", "PROBLEM"):
            rejection_reasons.append("invalid_section_type")

        if rejection_reasons:
            progress(
                "EXERCISE_TARGETED_RESCUE_START",
                page=page_num,
                number=number,
                reasons=rejection_reasons,
            )
            rescued = _rescue_unverified_exercise(
                page, row, page_num, lesson_id, book_id)
            if rescued is None:
                progress(
                    "SKIPPED_UNVERIFIED_EXERCISE",
                    page=page_num,
                    number=number,
                    reasons=rejection_reasons,
                )
                # Fail closed at ITEM level: never display/solve an exercise
                # that could not be verified, but do not discard the whole
                # verified lesson because one page item is unreadable.
                continue
            row = rescued
            prompt = str(row["exact_source_prompt"]).strip()
            coords = row["bbox_1000"]

        x0, y0, x1, y1 = [float(v) for v in coords]
        if not (0 <= x0 < x1 <= 1000 and 0 <= y0 < y1 <= 1000):
            progress(
                "SKIPPED_UNVERIFIED_EXERCISE",
                page=page_num,
                number=number,
                reasons=["invalid_region_after_rescue"],
            )
            continue
        rect = Rect(x0*page.rect.width/1000, y0*page.rect.height/1000,
                    x1*page.rect.width/1000, y1*page.rect.height/1000)
        raw_region = row.get("_rescue_crop_bytes")
        if not isinstance(raw_region, (bytes, bytearray)):
            raw_region = page.get_pixmap(clip=rect, dpi=200).tobytes("png")
        region_path = cache_dir / f"exercise_p{page_num}_{number}.png"
        region_path.write_bytes(raw_region)
        kind = str(row.get("section_type") or "EXERCISE").upper()
        if kind not in ("EXERCISE", "PROBLEM"):
            progress(
                "SKIPPED_UNVERIFIED_EXERCISE",
                page=page_num,
                number=number,
                reasons=["invalid_section_type_after_rescue"],
            )
            continue
        result.append({
            "number": number, "section_type": kind, "exact_source_prompt": prompt,
            "subquestions": list(row.get("subquestions") or []),
            "source_page": page_num,
            "source_bbox": [rect.x0, rect.y0, rect.x1, rect.y1],
            "source_region_image_ref": str(region_path),
            "source_region_sha256": hashlib.sha256(raw_region).hexdigest(),
            "verified_against_source": True,
            "ai_provenance": {
                "extraction": dict(row.get(
                    "_rescue_extraction_provenance", extraction_provenance)),
                "audit": dict(row.get(
                    "_rescue_audit_provenance", audit_provenance)),
            },
            "evidence_method": (
                "TARGETED_HIGHRES_TWO_PASS_EXERCISE_VISION"
                if row.get("_rescue_extraction_provenance")
                else "TWO_PASS_SOURCE_PAGE_VISION"
            )
        })
    return result


def _render_verified_text_diagram_svg(plan: dict) -> str:
    """Render a reviewed text-grounded diagram plan as deterministic SVG."""
    allowed = {"rect", "ellipse", "line", "arrow", "point", "text"}
    objects = plan.get("objects") or []
    if not isinstance(objects, list) or not objects:
        raise RuntimeError("TEXT_DIAGRAM_OBJECTS_MISSING")

    def num(value, default=0.0):
        try:
            return max(0.0, min(1000.0, float(value)))
        except (TypeError, ValueError):
            return float(default)

    parts = [
        '<svg class="nabil-text-grounded-diagram" viewBox="0 0 1000 600" '
        'role="img" xmlns="http://www.w3.org/2000/svg" '
        'style="max-width:100%;height:auto;border:1px solid #cbd5e1;'
        'border-radius:10px;background:#fff;">',
        '<defs><marker id="nabilArrow" markerWidth="10" markerHeight="10" '
        'refX="9" refY="3" orient="auto" markerUnits="strokeWidth">'
        '<path d="M0,0 L0,6 L9,3 z" fill="currentColor"/></marker></defs>',
    ]
    for obj in objects[:40]:
        if not isinstance(obj, dict):
            continue
        kind = str(obj.get("kind") or "").lower()
        if kind not in allowed:
            continue
        label = html.escape(str(obj.get("label") or ""))
        x = num(obj.get("x"), 100)
        y = num(obj.get("y"), 100)
        if kind == "rect":
            w = max(5.0, min(900.0, num(obj.get("w"), 120)))
            h = max(5.0, min(500.0, num(obj.get("h"), 80)))
            parts.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" '
                f'height="{h:.1f}" rx="8" fill="none" stroke="currentColor" '
                f'stroke-width="3"/>')
        elif kind == "ellipse":
            rx = max(4.0, min(450.0, num(obj.get("rx"), 50)))
            ry = max(4.0, min(250.0, num(obj.get("ry"), 30)))
            parts.append(
                f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx:.1f}" '
                f'ry="{ry:.1f}" fill="none" stroke="currentColor" '
                f'stroke-width="3"/>')
        elif kind in ("line", "arrow"):
            x2 = num(obj.get("x2"), x + 100)
            y2 = num(obj.get("y2"), y)
            marker = ' marker-end="url(#nabilArrow)"' if kind == "arrow" else ""
            parts.append(
                f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x2:.1f}" '
                f'y2="{y2:.1f}" stroke="currentColor" stroke-width="3"{marker}/>')
        elif kind == "point":
            parts.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="currentColor"/>')
        elif kind == "text":
            parts.append(
                f'<text x="{x:.1f}" y="{y:.1f}" font-size="28" '
                f'font-family="Arial, sans-serif">{label}</text>')
        if label and kind != "text":
            parts.append(
                f'<text x="{x + 10:.1f}" y="{max(24.0, y - 10):.1f}" '
                f'font-size="24" font-family="Arial, sans-serif">{label}</text>')
    parts.append("</svg>")
    svg = "".join(parts)
    if "<svg" not in svg or "</svg>" not in svg:
        raise RuntimeError("TEXT_DIAGRAM_RENDER_FAILED")
    return svg



def build_nabil_explanatory_redrawing(
        source_text: str,
        page_num: int,
        figure_paths: Optional[List[str]] = None,
        vision_context: Optional[Dict[str, Any]] = None,
        purpose: str = "concept_visual",
        visual_required: bool = False) -> Optional[dict]:
    """Create a NEW NABIL schematic from locked evidence, never expose the scan.

    Source figures may be inspected by vision, but their pixels are never
    returned to the student. The model proposes only semantic objects and
    relations; deterministic SVG is rendered locally and independently audited
    against the same locked text/figure evidence.
    """
    source_text = str(source_text or "").strip()
    figure_paths = [str(p) for p in (figure_paths or []) if p and Path(p).is_file()]
    if len(source_text) < 12 and not figure_paths:
        return None

    figure_b64 = None
    if figure_paths:
        from PIL import Image
        pics = []
        for filename in figure_paths[:4]:
            with Image.open(filename) as image:
                pic = image.convert("RGB")
                pic.thumbnail((1200, 850))
                pics.append(pic.copy())
        if pics:
            canvas = Image.new(
                "RGB",
                (max(p.width for p in pics),
                 sum(p.height for p in pics) + 10 * (len(pics) - 1)),
                "white",
            )
            top = 0
            for pic in pics:
                canvas.paste(pic, (0, top))
                top += pic.height + 10
            buf = io.BytesIO()
            canvas.save(buf, format="PNG")
            figure_b64 = base64.b64encode(buf.getvalue()).decode("ascii")

    request = (
        "You are NABIL, a classroom teacher creating a NEW explanatory schematic, "
        "not reproducing textbook artwork. Use the locked source text and, when "
        "provided, the verified source figure ONLY as evidence. The student must "
        "never see the source scan. Decide whether a visual is pedagogically useful. "
        "If not useful and VISUAL_REQUIRED is false, return "
        "{'needed':false,'reason':str}. If VISUAL_REQUIRED is true, needed must be "
        "true unless the evidence is insufficient, in which case return "
        "{'needed':false,'reason':'INSUFFICIENT_EVIDENCE'}. "
        "For a visual return strict JSON with needed=true, title, objects, relations. "
        "objects: at most 24 items, kind in rect|ellipse|line|arrow|point|text, "
        "id, label, x,y and optional x2,y2,w,h,rx,ry. Each object must contain "
        "evidence_basis='text' or 'figure'. For text basis include evidence_quote "
        "that is an EXACT contiguous quote from SOURCE_TEXT. For figure basis use "
        "evidence_quote='' and only encode something visibly verifiable in the "
        "provided source figure. relations has type,a,b,evidence_basis,evidence_quote "
        "under the same rule. Coordinates are presentation layout only, never data. "
        "Do not copy decorative styling, page layout, colors, icons, or typography "
        "from the textbook. Do not invent labels, measurements, geometry, direction, "
        "scientific behavior, historical facts, grammar rules, or missing steps. "
        f"VISUAL_REQUIRED={str(bool(visual_required)).lower()}\n"
        "SOURCE_TEXT:\n" + source_text
    )
    plan = _execute_llm_json_strict(
        request,
        image_base64=figure_b64,
        vision_context=vision_context if figure_b64 else None,
        purpose=f"{purpose}_plan_p{page_num}",
        max_attempts=3,
    )
    if not isinstance(plan, dict) or plan.get("needed") is not True:
        progress(
            "NABIL_EXPLANATORY_REDRAW_NOT_BUILT",
            page=page_num,
            purpose=purpose,
            reason=str(plan.get("reason") if isinstance(plan, dict) else "INVALID_PLAN")[:240],
        )
        return None

    objects = plan.get("objects")
    relations = plan.get("relations")
    if not isinstance(objects, list) or not objects or not isinstance(relations, list):
        raise RuntimeError("NABIL_REDRAW_SCHEMA_INVALID")
    source_norm = _normalized_lab_evidence(source_text)
    ids = set()
    allowed_kinds = {"rect", "ellipse", "line", "arrow", "point", "text"}
    for obj in objects:
        if not isinstance(obj, dict):
            raise RuntimeError("NABIL_REDRAW_OBJECT_INVALID")
        if str(obj.get("kind") or "").lower() not in allowed_kinds:
            raise RuntimeError("NABIL_REDRAW_OBJECT_KIND_INVALID")
        oid = str(obj.get("id") or "").strip()
        if not oid or oid in ids:
            raise RuntimeError("NABIL_REDRAW_OBJECT_ID_INVALID")
        ids.add(oid)
        basis = str(obj.get("evidence_basis") or "").lower()
        quote = _normalized_lab_evidence(obj.get("evidence_quote", ""))
        if basis == "text":
            if not quote or quote not in source_norm:
                raise RuntimeError("NABIL_REDRAW_TEXT_EVIDENCE_NOT_FOUND")
        elif basis == "figure":
            if not figure_b64:
                raise RuntimeError("NABIL_REDRAW_FIGURE_EVIDENCE_MISSING")
        else:
            raise RuntimeError("NABIL_REDRAW_EVIDENCE_BASIS_INVALID")
    for rel in relations:
        if not isinstance(rel, dict):
            raise RuntimeError("NABIL_REDRAW_RELATION_INVALID")
        if str(rel.get("a") or "") not in ids or str(rel.get("b") or "") not in ids:
            raise RuntimeError("NABIL_REDRAW_RELATION_ENDPOINT_INVALID")
        basis = str(rel.get("evidence_basis") or "").lower()
        quote = _normalized_lab_evidence(rel.get("evidence_quote", ""))
        if basis == "text":
            if not quote or quote not in source_norm:
                raise RuntimeError("NABIL_REDRAW_RELATION_TEXT_EVIDENCE_NOT_FOUND")
        elif basis == "figure":
            if not figure_b64:
                raise RuntimeError("NABIL_REDRAW_RELATION_FIGURE_EVIDENCE_MISSING")
        else:
            raise RuntimeError("NABIL_REDRAW_RELATION_EVIDENCE_BASIS_INVALID")

    audit_prompt = (
        "Independently audit this proposed NABIL explanatory schematic against "
        "the SAME locked SOURCE_TEXT and source figure if provided. It must be a "
        "fresh schematic, not a textbook-page reproduction. Reject any object, "
        "label, orientation, measurement, connection, process step or relation "
        "that is not directly supported by text or visibly supported by the "
        "source figure. Also reject if the schematic copies page styling/layout "
        "rather than teaching the concept. Return strict JSON exactly: "
        "{'approved':bool,'all_claims_traceable':bool,'no_invented_science':bool,"
        "'not_source_scan_reproduction':bool,'pedagogically_useful':bool,'reason':str}.\n"
        "SOURCE_TEXT:\n" + source_text + "\nPLAN:\n" +
        json.dumps(plan, ensure_ascii=False)
    )
    audit = _execute_llm_json_strict(
        audit_prompt,
        image_base64=figure_b64,
        vision_context=vision_context if figure_b64 else None,
        purpose=f"{purpose}_audit_p{page_num}",
        max_attempts=3,
    )
    if not isinstance(audit, dict) or not (
        audit.get("approved") is True
        and audit.get("all_claims_traceable") is True
        and audit.get("no_invented_science") is True
        and audit.get("not_source_scan_reproduction") is True
        and audit.get("pedagogically_useful") is True
    ):
        progress(
            "NABIL_EXPLANATORY_REDRAW_REJECTED",
            page=page_num,
            purpose=purpose,
            reason=str(audit.get("reason") if isinstance(audit, dict) else "INVALID_AUDIT")[:240],
        )
        return None

    svg = _render_verified_text_diagram_svg(plan)
    progress(
        "NABIL_EXPLANATORY_REDRAW_ACCEPTED",
        page=page_num,
        purpose=purpose,
        objects=len(objects),
        relations=len(relations),
    )
    return {
        "verified": True,
        "method": "NABIL_EXPLANATORY_REDRAW_FROM_LOCKED_EVIDENCE",
        "plan": plan,
        "svg": svg,
        "source_text_sha256": hashlib.sha256(source_text.encode("utf-8")).hexdigest(),
        "used_source_figure_as_hidden_evidence": bool(figure_b64),
    }


def build_text_grounded_exercise_diagram(
        entry: dict, prompt_text: str, subquestions: list,
        page_num: int, concepts: list) -> Optional[dict]:
    """Reconstruct a schematic only when verified text fully supports it.

    The output is never treated as the original textbook figure. Scientific
    objects/relations must be traceable to exact evidence quotes; layout
    coordinates are illustrative only and independently audited.
    """
    page_scope = [
        {
            "concept_id": c.get("concept_id"),
            "text": c.get("raw_text") or c.get("normalized_text") or "",
        }
        for c in concepts
        if int(c.get("source_page") or -1) == int(page_num)
    ]
    source_blob = (
        str(prompt_text or "").strip() + "\n" +
        "\n".join(str(x) for x in (subquestions or [])) + "\n" +
        "\n".join(str(x.get("text") or "") for x in page_scope)
    ).strip()
    if len(source_blob) < 20:
        return None

    request = (
        "You are reconstructing a SIMPLE SCHEMATIC for a textbook exercise "
        "ONLY from verified text. The original figure is unavailable and MUST "
        "NOT be guessed. If the text does not fully specify every scientific "
        "object and relation needed to solve the exercise, return "
        "{\"reconstructable\":false,\"reason\":str}. "
        "If reconstructable, return JSON with reconstructable=true, reason, "
        "objects and relations. objects is an array of at most 20 items with "
        "kind limited to rect|ellipse|line|arrow|point|text, id, label, x,y "
        "and when needed x2,y2,w,h,rx,ry, plus evidence_quote. Coordinates are "
        "only illustrative page layout. relations is an array with type, a, b, "
        "and evidence_quote. EVERY evidence_quote must be an exact contiguous "
        "quote from VERIFIED TEXT. Do not add an object, label, orientation, "
        "relative position, scale, measurement, angle, or scientific relation "
        "unless the verified text explicitly supports it. A reference such as "
        "'see Fig. 6' by itself is NOT enough. Never imitate or claim to "
        "reproduce the missing textbook image.\nVERIFIED TEXT:\n" + source_blob
    )
    plan = _execute_llm_json_strict(
        request, purpose=f"text_diagram_plan_p{page_num}")
    if not isinstance(plan, dict) or plan.get("reconstructable") is not True:
        progress(
            "TEXT_DIAGRAM_RECONSTRUCTION_NOT_POSSIBLE",
            page=page_num,
            reason=str(plan.get("reason") if isinstance(plan, dict) else
                       "INVALID_PLAN")[:240],
        )
        return None

    source_norm = _normalized_lab_evidence(source_blob)
    objects = plan.get("objects")
    relations = plan.get("relations")
    if not isinstance(objects, list) or not objects:
        return None
    if not isinstance(relations, list):
        return None
    allowed_kinds = {"rect", "ellipse", "line", "arrow", "point", "text"}
    ids = set()
    for obj in objects:
        if not isinstance(obj, dict):
            return None
        if str(obj.get("kind") or "").lower() not in allowed_kinds:
            return None
        oid = str(obj.get("id") or "").strip()
        quote = _normalized_lab_evidence(obj.get("evidence_quote", ""))
        if not oid or oid in ids or not quote or quote not in source_norm:
            return None
        ids.add(oid)
    for rel in relations:
        if not isinstance(rel, dict):
            return None
        quote = _normalized_lab_evidence(rel.get("evidence_quote", ""))
        if (str(rel.get("a") or "") not in ids
                or str(rel.get("b") or "") not in ids
                or not quote or quote not in source_norm):
            return None

    audit_prompt = (
        "Act as an independent scientific diagram auditor. Decide whether this "
        "schematic plan can be drawn from VERIFIED TEXT without inventing any "
        "scientific information. Coordinates are merely visual layout, but "
        "object existence, labels, orientation, relative placement, connections, "
        "measurements and scientific relations must all be text-supported. "
        "Reject if the exercise cannot be solved from the text-grounded plan "
        "without relying on the missing original image. Return strict JSON: "
        "{\"approved\":bool,\"all_claims_traceable\":bool,"
        "\"no_unstated_geometry\":bool,\"sufficient_for_exercise\":bool,"
        "\"reason\":str}.\nVERIFIED TEXT:\n" + source_blob +
        "\nPLAN:\n" + json.dumps(plan, ensure_ascii=False)
    )
    audit = _execute_llm_json_strict(
        audit_prompt, purpose=f"text_diagram_audit_p{page_num}")
    if not isinstance(audit, dict) or not (
            audit.get("approved") is True
            and audit.get("all_claims_traceable") is True
            and audit.get("no_unstated_geometry") is True
            and audit.get("sufficient_for_exercise") is True):
        progress(
            "TEXT_DIAGRAM_RECONSTRUCTION_REJECTED",
            page=page_num,
            reason=str(audit.get("reason") if isinstance(audit, dict) else
                       "INVALID_AUDIT")[:240],
        )
        return None

    svg = _render_verified_text_diagram_svg(plan)
    progress(
        "TEXT_DIAGRAM_RECONSTRUCTION_ACCEPTED",
        page=page_num,
        objects=len(objects),
        relations=len(relations),
    )
    return {
        "verified": True,
        "method": "AI_RECONSTRUCTED_DIAGRAM_FROM_VERIFIED_TEXT",
        "plan": plan,
        "svg": svg,
        "source_text_sha256": hashlib.sha256(
            source_blob.encode("utf-8")).hexdigest(),
    }


def build_evidence_map(doc, entry: dict, drive_service=None, persist_pages=False) -> dict:
    start_p = int(entry["pdf_start_page"])
    end_p = int(entry["pdf_end_page"])
    lesson_id = entry["lesson_id"]
    book_id = entry["book_id"]
    if start_p < 1 or end_p < start_p or end_p > len(doc):
        raise RuntimeError(f"SOURCE_PAGE_OUT_OF_RANGE: {lesson_id}, pages {start_p}-{end_p}, book length {len(doc)}")

    pages_evidence = []
    lesson_cache = CACHE_DIR / f"{book_id}_{lesson_id}"
    lesson_cache.mkdir(parents=True, exist_ok=True)
    page_checkpoints = None
    checkpoint_root = None
    source_provider = os.getenv("NABIL_FACTORY_AI_PROVIDER", "auto").strip().lower()
    if source_provider == "auto":
        source_provider = next(
            (name for name in ("openrouter", "groq", "openai")
             if os.getenv(name.upper() + "_API_KEY")), "none")
    source_model = {
        "groq": os.getenv("GROQ_VISION_MODEL", "qwen/qwen3.8-27b"),
        "openrouter": os.getenv("OPENROUTER_VISION_MODEL",
                               os.getenv("OPENROUTER_TEXT_MODEL",
                                         "google/gemini-3.6-flash")),
        "openai": os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini"),
    }.get(source_provider, "none")
    # Page checkpoints are recovery infrastructure, not scientific evidence.
    # Missing Drive/root must never abort lesson generation.  When configured,
    # checkpoints remain enabled; otherwise the factory continues normally.
    checkpoint_root = None
    page_checkpoints = None
    if persist_pages and drive_service is not None:
        checkpoint_root = str(os.getenv("NABIL_CURRICULUM_ROOT_ID") or "").strip() or None
        if checkpoint_root:
            from scripts import nabil_page_checkpoint as page_checkpoints
        else:
            progress(
                "CHECKPOINT_DISABLED_NO_ROOT_ID",
                lesson_id=lesson_id,
                reason="NABIL_CURRICULUM_ROOT_ID_NOT_CONFIGURED")
    elif persist_pages and page_checkpoints is not None and checkpoint_root:
        progress(
            "CHECKPOINT_DISABLED_NO_DRIVE",
            lesson_id=lesson_id,
            reason="DRIVE_SERVICE_UNAVAILABLE")
    opening_text = extract_page_text_robust(
        doc, start_p, lesson_id, book_id, lesson_cache)
    # Validate the two physical title sources BEFORE costly page-by-page vision.
    if not verify_title_double_evidence_strict(doc, entry, opening_text):
        raise AssertionError(
            f"TITLE_VERIFICATION_FAILED: Strict Double Evidence TOC + Opening "
            f"failed for '{entry['canonical_title']}'.")
    progress("LESSON_TITLE_DOUBLE_EVIDENCE_VERIFIED",
             lesson_id=lesson_id, title=entry["canonical_title"],
             opener_pdf_page=start_p, toc_pdf_page=entry.get("toc_pdf_page"))
    for p_num in range(start_p, end_p + 1):
        saved_page = (page_checkpoints.load_page(
            drive_service, checkpoint_root, doc, entry, p_num, lesson_cache,
            source_provider, source_model) if page_checkpoints else None)
        if saved_page is not None:
            for restored_figure in saved_page["figures"]:
                if restored_figure.get("evidence_method") in (
                    "APPROVED_VISION_BOX_CROPPED_FROM_SOURCE_PDF",
                    "TARGETED_HIGHRES_VISION_PLUS_LOCAL_CAPTION_OCR",
                ):
                    provenance = restored_figure.get("ai_provenance") or {}
                    actual_provider = provenance.get("provider")
                    assert_authorized_source_vision(
                        lesson_id, book_id, p_num,
                        provider_override=actual_provider)
            pages_evidence.append(saved_page)
            progress("PAGE_EVIDENCE_RESTORED_FROM_DRIVE",
                     lesson_id=lesson_id, page=p_num,
                     figures=len(saved_page["figures"]))
            continue
        txt = (opening_text if p_num == start_p else
               extract_page_text_robust(doc, p_num, lesson_id, book_id, lesson_cache))
        figs = extract_multimodal_page_figures(
            doc, p_num, lesson_cache, lesson_id, book_id)
        # Source-first completeness check. If the normal pass missed a
        # printed figure label that the real page text mentions, make one
        # targeted higher-resolution rescue attempt. The rescue still requires
        # independent LOCAL OCR of the exact caption box.
        mentions = {m.lower() for m in re.findall(
            r"(?i)\bfig(?:ure)?\.?\s*(\d+[a-z]?)", txt)}
        found = {
            str(f.get("printed_label") or "").lower() for f in figs
        } | {
            str(f.get("printed_number")) for f in figs
            if f.get("printed_number") is not None
        }
        missing = mentions - found
        if missing:
            progress("TARGETED_FIGURE_RESCUE_START",
                     lesson_id=lesson_id, page=p_num,
                     missing_labels=sorted(missing))
            rescued = rescue_missing_labeled_figures(
                doc, p_num, lesson_cache, lesson_id, book_id,
                missing, figs)
            if rescued:
                figs.extend(rescued)
                found = {
                    str(f.get("printed_label") or "").lower() for f in figs
                } | {
                    str(f.get("printed_number")) for f in figs
                    if f.get("printed_number") is not None
                }
                missing = mentions - found

        page_evidence = {
            "page_num": p_num,
            "text": txt,
            "text_hash": hashlib.sha256(txt.encode("utf-8")).hexdigest()[:16],
            "figures": figs,
            "unverified_figure_labels": sorted(missing),
        }
        if page_checkpoints:
            # Never cache an incomplete page as a completed checkpoint.
            if not missing:
                page_checkpoints.save_page(
                    drive_service, checkpoint_root, doc, entry,
                    page_evidence, source_provider, source_model)
                progress("PAGE_EVIDENCE_SAVED_TO_DRIVE",
                         lesson_id=lesson_id, page=p_num,
                         figures=len(figs))
            else:
                progress("PAGE_EVIDENCE_NOT_SAVED_UNVERIFIED_FIGURES",
                         lesson_id=lesson_id, page=p_num,
                         missing_labels=sorted(missing))
        pages_evidence.append(page_evidence)

    concepts = []
    act_regex = re.compile(
        r"(?:Activity|Activité|نشاط)\s*(\d*)[:\s.-]+([^\n.]+)", re.I)
    numbered_section_regex = re.compile(
        r"(?im)^\s*(\d+)\s+([A-ZÀ-ÖØ-Ý][^\n]{2,90})")

    def _concept_title_key(value: str) -> str:
        return re.sub(r"[^a-z0-9]+", " ", str(value or "").casefold()).strip()

    next_concept_num = 1
    concept_exercise_section_seen = False
    exercise_section_start_page = None
    for p in pages_evidence:
        page_text = str(p["text"] or "")
        if re.search(
                r"(?i)\b(exercises|problems|exercices|problèmes)\b|تمارين|مسائل",
                page_text):
            concept_exercise_section_seen = True
            if exercise_section_start_page is None:
                exercise_section_start_page = int(p["page_num"])
                progress(
                    "EXERCISE_SECTION_BOUNDARY_LOCKED",
                    page=exercise_section_start_page,
                )
        if concept_exercise_section_seen:
            continue
        page_doc = doc[p["page_num"] - 1]
        activity_matches = list(act_regex.finditer(page_text))
        headings = []
        for m in activity_matches:
            headings.append({
                "start": m.start(),
                "end_head": m.end(),
                "title": m.group(2).strip(),
                "declared_num": (
                    int(m.group(1)) if str(m.group(1) or "").isdigit()
                    else None),
                "kind": "ACTIVITY",
            })

        # Standalone numbered content after the last activity is still part of
        # the lesson (notably explanatory sections that are not called Activity).
        # Ignore broad numbered section headers that merely precede activities.
        last_activity_start = (
            max((m.start() for m in activity_matches), default=-1))
        for m in numbered_section_regex.finditer(page_text):
            title = m.group(2).strip(" .:-")
            key = _concept_title_key(title)
            if not key or key == _concept_title_key(entry["canonical_title"]):
                continue
            if activity_matches and m.start() < last_activity_start:
                continue
            if re.search(r"(?i)chapter|contents|objectives|exercise", title):
                continue
            # Avoid duplicating an Activity heading that OCR also exposed as a
            # bare numbered heading.
            if any(
                key == _concept_title_key(h["title"])
                or key in _concept_title_key(h["title"])
                or _concept_title_key(h["title"]) in key
                for h in headings
            ):
                continue
            headings.append({
                "start": m.start(),
                "end_head": m.end(),
                "title": title,
                "declared_num": None,
                "kind": "SECTION",
            })

        headings.sort(key=lambda h: h["start"])
        for pos, heading in enumerate(headings):
            end = (
                headings[pos + 1]["start"]
                if pos + 1 < len(headings)
                else len(page_text)
            )
            raw_chunk = page_text[heading["start"]:end].strip()
            chunk = " ".join(raw_chunk.split())
            if len(chunk) < 25:
                continue

            concept_num = heading["declared_num"]
            if concept_num is None or any(
                    x.get("concept_id") == f"C{concept_num:02d}"
                    for x in concepts):
                while any(
                        x.get("concept_id") == f"C{next_concept_num:02d}"
                        for x in concepts):
                    next_concept_num += 1
                concept_num = next_concept_num
            next_concept_num = max(next_concept_num, concept_num + 1)

            matched_figs = match_figure_to_item(
                {"raw_text": chunk, "requires_figure": False},
                p["figures"], page_doc.rect)
            fig_ref = matched_figs[0] if matched_figs else "NONE"

            rects = page_doc.search_for(heading["title"][:20])
            act_bbox = (
                [round(rects[0].x0, 1), round(rects[0].y0, 1),
                 round(rects[0].x1, 1), round(rects[0].y1, 1)]
                if rects
                else [0.0, 0.0, page_doc.rect.width, 100.0]
            )
            norm_chunk, math_ok, math_recs = MathRenderingEngine.normalize_math(
                chunk, p["page_num"], act_bbox, fig_ref)

            concepts.append({
                "concept_id": f"C{concept_num:02d}",
                "title": heading["title"],
                "source_page": p["page_num"],
                "raw_text": chunk,
                "normalized_text": norm_chunk,
                "figure_refs": matched_figs,
                "math_records": math_recs,
                "source_section_kind": heading["kind"],
                "sha256": hashlib.sha256(
                    chunk.encode("utf-8")).hexdigest()[:16],
            })

    if not concepts:
        raise RuntimeError("EVIDENCE_EXTRACTION_INCOMPLETE: No verifiable concepts or activities found within source page range.")

    exercises = []
    ex_pattern = re.compile(r'(?:^|\n)\s*(?:(Problem|Exercise|Problème|Exercice|تمرين|مسألة)\s*)?(\d+)[\.\-\)]\s+([^\n]+(?:\n(?!\s*(?:(?:Problem|Exercise|Problème|Exercice|تمرين|مسألة)\s*)?\d+[\.\-\)]\s+)[^\n]+)*)', re.I)
    exercise_section_seen = False
    for p in pages_evidence:
        page_num = p["page_num"]
        if re.search(r"(?i)\b(exercises|problems|exercices|problèmes)\b|تمارين|مسائل", p["text"]):
            exercise_section_seen = True
        source_page = doc[page_num - 1]
        scanned = any(
            (rect.width*rect.height)/(source_page.rect.width*source_page.rect.height) >= 0.80
            for image in source_page.get_images(full=True)
            for rect in source_page.get_image_rects(image[0])
        )
        if scanned:
            if not exercise_section_seen and page_num < end_p - 1:
                continue
            rows = (page_checkpoints.load_exercises(
                drive_service, checkpoint_root, doc, entry, page_num,
                lesson_cache, source_provider, source_model)
                if page_checkpoints else None)
            if rows is not None:
                assert_authorized_source_vision(lesson_id, book_id, page_num)
                progress("EXERCISES_RESTORED_FROM_DRIVE",
                         page=page_num, count=len(rows))
            else:
                rows = extract_scanned_page_exercises(
                    doc, page_num, lesson_id, book_id, lesson_cache)
                if page_checkpoints:
                    # Two independent source-image reads already confirmed
                    # the exact text/bbox for every returned exercise.
                    page_checkpoints.save_exercises(
                        drive_service, checkpoint_root, doc, entry,
                        page_num, rows, source_provider, source_model)
                    progress("EXERCISES_SAVED_TO_DRIVE",
                             page=page_num, count=len(rows))
        else:
            rows = []
            for m in ex_pattern.finditer(p["text"]):
                prompt = " ".join(m.group(3).split())
                if len(prompt) < 10:
                    continue
                kind = m.group(1)
                rows.append({
                    "number": int(m.group(2)),
                    "section_type": ("PROBLEM" if kind and kind.upper() in
                        ("PROBLEM", "PROBLÈME", "مسألة") else "EXERCISE"),
                    "exact_source_prompt": prompt,
                    "subquestions": [],
                    "source_page": page_num,
                    "verified_against_source": re.sub(r"\s+", " ", prompt).strip().casefold() in
                        re.sub(r"\s+", " ", p["text"]).strip().casefold(),
                    "evidence_method": "NATIVE_PDF_TEXT"
                })
        for row in rows:
            content = row["exact_source_prompt"]
            number = int(row["number"])
            kind = row["section_type"]
            req_fig = bool(re.search(r"(?:fig(?:ure)?\.?|document|doc|شكل|وثيقة)\s*\d+", content, re.I)
                           or any(k in content.casefold() for k in ("diagram", "sketch", "draw", "graph")))
            reconstructed = None
            try:
                refs = match_figure_to_item(
                    {"exact_source_prompt": content,
                     "requires_figure": req_fig},
                    p["figures"], source_page.rect)
            except RuntimeError as exc:
                reason = str(exc)
                if not reason.startswith("FIGURE_EVIDENCE_MISSING"):
                    raise
                reconstructed = build_text_grounded_exercise_diagram(
                    entry, content, row.get("subquestions") or [],
                    page_num, concepts)
                if reconstructed is None:
                    progress(
                        "SKIPPED_UNVERIFIED_EXERCISE",
                        page=page_num,
                        number=number,
                        reasons=[reason,
                                 "TEXT_GROUNDED_DIAGRAM_NOT_RECONSTRUCTABLE"],
                    )
                    continue
                refs = []
                progress(
                    "EXERCISE_USING_TEXT_GROUNDED_DIAGRAM",
                    page=page_num,
                    number=number,
                    method=reconstructed["method"],
                )
            hashes = [f["image_sha256"] for f in p["figures"] if f["figure_id"] in refs]
            subqs = row.get("subquestions") or []

            # When an exercise depends on a verified source figure, NABIL must
            # redraw its semantics instead of exposing the textbook crop.
            if refs and reconstructed is None:
                source_figure_paths = [
                    f["image_path"] for f in p["figures"]
                    if f["figure_id"] in refs and f.get("image_path")
                ]
                try:
                    reconstructed = build_nabil_explanatory_redrawing(
                        source_text=(
                            str(content) + "\n" +
                            "\n".join(str(x) for x in subqs)
                        ),
                        page_num=page_num,
                        figure_paths=source_figure_paths,
                        vision_context={
                            "lesson_id": lesson_id,
                            "book_id": book_id,
                            "pdf_page": page_num,
                        } if source_figure_paths else None,
                        purpose=f"exercise_{kind}_{number}",
                        visual_required=True,
                    )
                except RuntimeError as exc:
                    # Exercise-level redraw evidence failure must not abort the
                    # whole lesson. Keep the universal fail-closed rule: reject
                    # this exercise only; never invent or expose the source scan.
                    if str(exc) != "NABIL_REDRAW_TEXT_EVIDENCE_NOT_FOUND":
                        raise
                    progress(
                        "SKIPPED_EXERCISE_NABIL_REDRAW_UNVERIFIED",
                        page=page_num,
                        number=number,
                        reason=str(exc),
                    )
                    continue
                if reconstructed is None and req_fig:
                    progress(
                        "SKIPPED_EXERCISE_NABIL_REDRAW_UNVERIFIED",
                        page=page_num,
                        number=number,
                        reason="SOURCE_FIGURE_CANNOT_BE_SAFELY_REPRESENTED_WITHOUT_SCAN",
                    )
                    continue

            ex = {
                "exercise_id": f"{lesson_id}-{kind[:2]}-{number:02d}",
                "lesson_id": lesson_id, "section_type": kind, "number": number,
                "source_page": page_num, "exact_source_prompt": content,
                "source_prompt_hash": hashlib.sha256(content.encode("utf-8")).hexdigest()[:16],
                "subquestions": subqs, "requires_figure": req_fig,
                "figure_refs": refs, "figure_hashes": hashes,
                # Every exercise that the factory can faithfully extract from
                # the official book is kept. There is deliberately NO numeric
                # cap such as "first 2 exercises".
                "solution_mode": "PRE_SOLVED", "solution_status": "NOT_SOLVED",
                "source_origin": "TEXTBOOK",
                "verified_against_source": row["verified_against_source"],
                "evidence_method": row.get("evidence_method", "NATIVE_PDF_TEXT"),
                "reconstructed_diagram_verified": bool(reconstructed),
                "reconstructed_diagram_method": (
                    reconstructed.get("method") if reconstructed else None),
                "reconstructed_diagram_plan": (
                    reconstructed.get("plan") if reconstructed else None),
                "reconstructed_diagram_svg": (
                    reconstructed.get("svg") if reconstructed else None),
                "reconstructed_diagram_source_sha256": (
                    reconstructed.get("source_text_sha256")
                    if reconstructed else None),
            }
            for key in ("source_bbox", "source_region_image_ref", "source_region_sha256"):
                if key in row:
                    ex[key] = row[key]
            exercises.append(ex)

    unique_ex = []
    seen = set()
    for e in sorted(exercises, key=lambda x: (x["section_type"], x["number"])):
        k = (e["section_type"], e["number"])
        if k not in seen:
            seen.add(k)
            unique_ex.append(e)

    # All verified textbook exercises remain in the lesson. Unverified page
    # items are skipped, never guessed. If fewer than 3 textbook exercises are
    # verified, add at least 3 evidence-gated AI practice exercises in addition.
    for e in unique_ex:
        e["solution_mode"] = "PRE_SOLVED"

    # An unresolved printed figure is critical only when accepted lesson
    # content actually refers to that figure. Otherwise it remains explicitly
    # recorded as skipped/unverified and is never rendered or used as evidence.
    def _explicit_figure_labels(text_value: str) -> set:
        return {
            str(label).casefold()
            for label in re.findall(
                r"(?:fig(?:ure)?\.?|document|doc|شكل|وثيقة)\s*(\d+[a-z]?)",
                str(text_value or ""),
                re.I,
            )
        }

    for page_item in pages_evidence:
        unresolved = {
            str(x).casefold()
            for x in (page_item.get("unverified_figure_labels") or [])
        }
        used_labels = set()
        if unresolved:
            page_no = int(page_item["page_num"])
            for concept in concepts:
                if int(concept.get("source_page") or -1) == page_no:
                    used_labels |= _explicit_figure_labels(
                        concept.get("raw_text", ""))
            for exercise in unique_ex:
                if (int(exercise.get("source_page") or -1) == page_no
                        and not exercise.get("reconstructed_diagram_verified")):
                    used_labels |= _explicit_figure_labels(
                        exercise.get("exact_source_prompt", ""))
        required_unverified = sorted(unresolved & used_labels)
        optional_unverified = sorted(unresolved - used_labels)
        page_item["required_unverified_figure_labels"] = required_unverified
        page_item["skipped_unverified_figure_labels"] = optional_unverified
        for label in optional_unverified:
            progress(
                "SKIPPED_UNVERIFIED_SOURCE_FIGURE",
                page=page_item["page_num"],
                figure_label=label,
                reason="NOT_REFERENCED_BY_ACCEPTED_CONCEPT_OR_EXERCISE",
            )

    ev_map = {
        "lesson_id": lesson_id,
        "book_id": entry["book_id"],
        "source_lock": {"start": start_p, "end": end_p},
        "pages_evidence": pages_evidence,
        "concepts": concepts,
        "exercise_section_start_page": exercise_section_start_page,
        "exercise_evidence": unique_ex,
        "canonical_title": entry["canonical_title"]
    }

    # Independent completeness gate runs before the permanent Evidence Map is accepted.
    attach_and_verify_source_completeness(ev_map)
    perm_path = PERM_EVIDENCE_DIR / f"{lesson_id}.json"
    perm_path.write_text(json.dumps(ev_map, ensure_ascii=False, indent=2), encoding="utf-8")
    return ev_map


# ==============================================================================
# 6B. TEXTBOOK-FIRST EXERCISE POLICY + STRICT AI FALLBACK
# ==============================================================================
def _lesson_scope_for_exercise_gate(ev_map: dict) -> List[dict]:
    """Compact, source-grounded lesson scope used by the exercise gate."""
    scope = []
    for c in ev_map.get("concepts", []):
        text = str(c.get("normalized_text") or c.get("raw_text") or "").strip()
        if not text:
            continue
        scope.append({
            "concept_id": c.get("concept_id"),
            "title": c.get("title"),
            "source_page": c.get("source_page"),
            "text": text[:1600],
        })
    if not scope:
        raise RuntimeError(
            "AI_ADDITIONAL_PRACTICE_PROHIBITED: no verified lesson concepts")
    return scope


def required_ai_practice_count(textbook_count: int) -> int:
    """Add at least three AI practice exercises when book practice is sparse.

    Product rule:
    - preserve and solve every verified textbook exercise;
    - never replace a verified textbook exercise with AI;
    - if fewer than 3 verified textbook exercises exist, generate at least
      3 evidence-gated AI practice exercises in addition to the verified ones;
    - if 3 or more verified textbook exercises exist, add no AI practice.
    """
    count = max(0, int(textbook_count))
    return 3 if count < 3 else 0


def generate_ai_practice_for_insufficient_book_exercises(
        entry: dict, ev_map: dict, profile: dict,
        verified_textbook_count: Optional[int] = None) -> List[dict]:
    """Add strictly lesson-grounded AI practice only when <=2 textbook exercises survived.

    Important: the trigger is the number of textbook exercises that were actually
    solved and scientifically verified, not the number merely extracted.
    Rejected AI candidates are discarded individually; they never cancel the lesson.
    """
    textbook_count = (
        max(0, int(verified_textbook_count))
        if verified_textbook_count is not None
        else len(ev_map.get("exercise_evidence") or [])
    )
    desired_count = required_ai_practice_count(textbook_count)
    if desired_count == 0:
        progress("AI_ADDITIONAL_PRACTICE_SKIPPED_BOOK_SUFFICIENT",
                 textbook_count=textbook_count)
        return []

    progress("AI_ADDITIONAL_PRACTICE_REQUIRED_BOOK_INSUFFICIENT",
             textbook_count=textbook_count,
             ai_target=desired_count)

    scope = _lesson_scope_for_exercise_gate(ev_map)
    accepted = []
    rejected_reasons = []

    for round_no in range(1, 4):
        remaining = desired_count - len(accepted)
        if remaining <= 0:
            break

        generator_prompt = (
            f"You are creating additional practice for Lebanese "
            f"{profile['subject']} Grade {profile['grade']}.\n"
            f"Lesson title: {entry['canonical_title']}\n"
            f"The official textbook yielded {textbook_count} reliably "
            "extractable exercise(s). Because fewer than 3 verified textbook "
            "exercises are available, generate AT LEAST 3 additional AI practice "
            "exercises. Preserve every verified textbook exercise and generate "
            "the AI practice ONLY from the VERIFIED LESSON SCOPE "
            "below. Do not introduce a law, definition, scientific concept, "
            "symbol, apparatus, material, quantity, unit, formula, fact, "
            "prerequisite, or real-world scenario that is absent from this scope. "
            "A new numeric value is allowed only as a practice input to a formula "
            "or quantitative relation explicitly present in the verified scope, "
            "using only units already present there. Do not require a figure. "
            "Make each question solvable entirely from what the student learned "
            "in THIS lesson, with no outside knowledge. Return JSON exactly as "
            "{'candidates':[{'prompt':str,'subquestions':[str],"
            "'solution_outline':str,'concept_ids':[str]}]}. "
            f"Return at least {max(remaining * 2, 4)} candidates so rejected "
            "ones can be discarded.\nVERIFIED LESSON SCOPE:\n"
            + json.dumps(scope, ensure_ascii=False)
        )
        if rejected_reasons:
            generator_prompt += (
                "\nDo NOT repeat these previously rejected defects:\n"
                + json.dumps(rejected_reasons[-8:], ensure_ascii=False)
            )

        try:
            generated = json.loads(execute_llm_completion(
                generator_prompt, json_mode=True, temperature=0.2))
        except Exception as exc:
            rejected_reasons.append(f"AI generator unavailable: {exc}")
            progress(
                "AI_ADDITIONAL_PRACTICE_GENERATOR_FAILED_EXERCISE_ONLY",
                round=round_no, reason=str(exc)[:240])
            continue
        candidates = generated.get("candidates")
        if not isinstance(candidates, list):
            rejected_reasons.append("AI candidate list missing")
            progress(
                "AI_ADDITIONAL_PRACTICE_SCHEMA_REJECTED_EXERCISE_ONLY",
                round=round_no)
            continue

        for candidate in candidates:
            if len(accepted) >= desired_count:
                break
            if not isinstance(candidate, dict):
                continue
            prompt_text = str(candidate.get("prompt") or "").strip()
            subqs = candidate.get("subquestions") or []
            outline = str(candidate.get("solution_outline") or "").strip()
            claimed_ids = candidate.get("concept_ids") or []
            if (len(prompt_text) < 10 or not isinstance(subqs, list)
                    or not outline):
                rejected_reasons.append("incomplete candidate schema")
                progress("EXERCISE_REJECTED_SCHEMA",
                         round=round_no,
                         prompt_excerpt=prompt_text[:80])
                continue

            gate_prompt = (
                "Act as a strict curriculum exercise gate. Compare ONE proposed "
                "exercise with the VERIFIED LESSON SCOPE. Approve only if every "
                "fact, rule, relation, concept, apparatus/material, quantity, "
                "unit, formula, scenario, and required reasoning is directly "
                "supported by that scope. New numeric inputs are permitted only "
                "for a verified formula/relation and verified units already in "
                "scope. The task must be age-appropriate, internally consistent, "
                "solvable without outside knowledge, and its supplied solution "
                "outline scientifically correct. Reject if anything is merely "
                "plausible from general knowledge rather than traceable to this "
                "lesson. Reject if uncertain. "
                "Return JSON exactly as "
                "{'approved':bool,'reasons':[str],'supported_concept_ids':[str],"
                "'solution_consistent':bool,'within_scope':bool}.\n"
                "VERIFIED LESSON SCOPE:\n"
                + json.dumps(scope, ensure_ascii=False)
                + "\nCANDIDATE:\n"
                + json.dumps(candidate, ensure_ascii=False)
            )
            try:
                verdict = json.loads(execute_llm_completion(
                    gate_prompt, json_mode=True, temperature=0.0))
            except Exception as exc:
                rejected_reasons.append(f"scientific gate unavailable: {exc}")
                progress(
                    "EXERCISE_REJECTED_SCIENTIFIC_GATE_UNAVAILABLE",
                    round=round_no,
                    prompt_excerpt=prompt_text[:100],
                    reason=str(exc)[:240])
                continue
            supported_ids = [
                str(x) for x in (verdict.get("supported_concept_ids") or [])
            ] if isinstance(verdict.get("supported_concept_ids"), list) else []
            actual_scope_ids = {
                str(item.get("concept_id")) for item in scope
                if item.get("concept_id")
            }
            supported_ids_valid = bool(
                supported_ids
                and set(supported_ids).issubset(actual_scope_ids)
            )
            approved = bool(
                verdict.get("approved")
                and verdict.get("solution_consistent")
                and verdict.get("within_scope")
                and supported_ids_valid
            )
            if not approved:
                reasons = verdict.get("reasons")
                if not isinstance(reasons, list):
                    reasons = ["scientific/scope gate rejected candidate"]
                rejected_reasons.extend(str(x) for x in reasons)
                progress("EXERCISE_REJECTED_SCIENTIFIC_GATE",
                         round=round_no,
                         prompt_excerpt=prompt_text[:100],
                         reasons=[str(x) for x in reasons][:5])
                continue

            idx = len(accepted) + 1
            supported = supported_ids
            accepted.append({
                "exercise_id": f"{entry['lesson_id']}-AI-{idx:02d}",
                "lesson_id": entry["lesson_id"],
                "section_type": "ADDITIONAL_PRACTICE",
                "number": idx,
                "source_page": None,
                "exact_source_prompt": prompt_text,
                "source_prompt_hash": hashlib.sha256(
                    prompt_text.encode("utf-8")).hexdigest()[:16],
                "subquestions": [str(x) for x in subqs],
                "requires_figure": False,
                "figure_refs": [],
                "figure_hashes": [],
                "solution_mode": "PRE_SOLVED",
                "solution_status": "NOT_SOLVED",
                "source_origin": "AI_ADDITIONAL_PRACTICE",
                "verified_against_source": False,
                "scientific_gate_passed": True,
                "scope_concept_ids": supported,
                "scope_snapshot_sha256": hashlib.sha256(
                    json.dumps(
                        [item for item in scope
                         if str(item.get("concept_id")) in set(supported)],
                        ensure_ascii=False,
                        sort_keys=True,
                    ).encode("utf-8")
                ).hexdigest(),
                "generator_claimed_concept_ids": [
                    str(x) for x in claimed_ids],
                "evidence_method":
                    "AI_GENERATED_AFTER_SOURCE_SCOPE_SCIENTIFIC_GATE",
            })
            progress("AI_ADDITIONAL_PRACTICE_ACCEPTED",
                     number=idx, round=round_no,
                     supported_concepts=supported)

    if len(accepted) < desired_count:
        # Never sacrifice a scientifically valid lesson because an optional AI
        # exercise could not pass the strict scope gate. Invalid exercises are
        # discarded individually. The target remains >=3 valid AI exercises.
        progress(
            "AI_ADDITIONAL_PRACTICE_BELOW_TARGET_LESSON_PRESERVED",
            accepted=len(accepted), target=desired_count,
            rejections=rejected_reasons[-8:])
    return accepted


# ==============================================================================
# 7. MULTI-MODAL GROUNDED SOLVER & STRICT FAIL-CLOSED VERIFIER
# ==============================================================================
def grounded_subject_solver(exercise: dict, evidence_map: dict, profile: dict) -> Dict[str, Any]:
    prompt = exercise["exact_source_prompt"]
    page = exercise.get("source_page")
    subj = profile["subject"]
    grade = profile.get("grade", 7)
    source_origin = exercise.get("source_origin", "TEXTBOOK")

    fig_base64 = None
    if exercise.get("figure_refs"):
        for p in evidence_map["pages_evidence"]:
            if p["page_num"] == page:
                for f in p["figures"]:
                    if f["figure_id"] in exercise["figure_refs"]:
                        try:
                            fig_base64 = base64.b64encode(
                                Path(f["image_path"]).read_bytes()
                            ).decode("ascii")
                        except Exception as exc:
                            raise RuntimeError(
                                "FIGURE_EVIDENCE_MISSING: Cannot read "
                                f"referenced source image: {exc}")
                        break

    all_scope = [
        {
            "concept_id": c.get("concept_id"),
            "title": c.get("title"),
            "source_page": c.get("source_page"),
            "text": c.get("normalized_text") or c.get("raw_text"),
        }
        for c in evidence_map.get("concepts", [])
        if str(c.get("normalized_text") or c.get("raw_text") or "").strip()
    ]

    if source_origin == "TEXTBOOK":
        provenance = f"official textbook exercise verbatim from Page {page}"
        source_exercise_examples = [
            {
                "source_kind": "TEXTBOOK_EXERCISE_EVIDENCE",
                "exercise_id": e.get("exercise_id"),
                "number": e.get("number"),
                "source_page": e.get("source_page"),
                "text": e.get("exact_source_prompt"),
            }
            for e in evidence_map.get("exercise_evidence", [])
            if e.get("verified_against_source") is True
            and str(e.get("exact_source_prompt") or "").strip()
        ]
        supported_scope = all_scope + source_exercise_examples
    else:
        provenance = (
            "additional practice exercise already approved by the strict "
            "lesson-scope scientific gate"
        )
        supported = set(exercise.get("scope_concept_ids") or [])
        supported_scope = [
            item for item in all_scope
            if item.get("concept_id") in supported
        ]

    if not supported_scope:
        raise RuntimeError(
            "PRE_SOLVE_FAILED: no verified lesson scope for exercise")

    scope_note = (
        "\nVERIFIED LESSON EVIDENCE — use this and the exercise itself only:\n"
        + json.dumps(supported_scope, ensure_ascii=False)
    )

    reconstructed_note = ""
    if exercise.get("reconstructed_diagram_verified"):
        reconstructed_note = (
            "\nUse ONLY this independently verified NABIL schematic plan as "
            "the student-facing visual. The original textbook/source image, if "
            "available, is hidden evidence only and must never be reproduced "
            "or exposed to the student: "
            + json.dumps(
                exercise.get("reconstructed_diagram_plan") or {},
                ensure_ascii=False)
        )

    solver_lang_code = resolve_lang_code(profile["language"])
    figure_rule = (
        "A verified source figure is attached. Treat only relationships actually "
        "visible in that figure as visual evidence. Never claim that objects are "
        "connected, aligned, equal, parallel, at the same level, measured, or "
        "made of a particular material unless the prompt, verified lesson text, "
        "or attached figure establishes that relationship."
        if fig_base64 else
        "No source figure is attached. Do not infer any missing geometry or "
        "visual relationship."
    )
    query = (
        f"You are Teacher NABIL, master professor of Lebanese "
        f"{subj.capitalize()} Grade {grade}.\n"
        f"{narrative_language_instruction(solver_lang_code)}\n"
        f"Solve this {provenance}.\n"
        f"Prompt: {prompt}\n"
        f"Subquestions: {json.dumps(exercise.get('subquestions', []))}"
        f"{scope_note}{reconstructed_note}\n\n"
        "STRICT SOURCE RULES:\n"
        "1. Answer the textbook task directly and minimally. The final_answer "
        "must itself answer EVERY explicit requested action/subquestion; do not "
        "leave a required part only in the reasoning steps.\n"
        "2. Every explanatory fact, law, property, example, material, unit, "
        "quantity, or scientific relationship must come from the exercise "
        "prompt, VERIFIED LESSON EVIDENCE, or a verified attached figure.\n"
        "3. Do not add general textbook knowledge merely because it is true. "
        "For example/list/classification questions, give the requested answer "
        "without adding unrelated background facts. Preserve exact source labels "
        "and example names when available; do not generalize them. Do not add "
        "unrequested drawing actions such as shading, coloring, measuring, "
        "marking, or construction steps unless the prompt/source requires them.\n"
        f"4. {figure_rule}\n"
        "5. If the prompt asks for a drawing, describe only what must be drawn "
        "from the verified rule and visible source geometry.\n"
        "Return strictly JSON: {'steps': [str], 'final_answer': str}"
    )

    vision_context = ({
        "lesson_id": exercise.get("lesson_id"),
        "book_id": evidence_map.get("book_id"),
        "pdf_page": page,
    } if fig_base64 else None)

    def _generate_solution(extra_instruction: str = "") -> Tuple[dict, dict]:
        parsed = _execute_llm_json_strict(
            query + extra_instruction,
            image_base64=fig_base64,
            vision_context=vision_context,
            purpose=f"exercise_solution_{exercise.get('exercise_id')}",
            max_attempts=3,
        )
        provenance_data = get_last_llm_provenance()
        if not isinstance(parsed, dict):
            raise ValueError("Incomplete solver response schema")
        if not isinstance(parsed.get("steps"), list) or not parsed.get("steps"):
            raise ValueError("Incomplete solver steps")
        if not str(parsed.get("final_answer") or "").strip():
            raise ValueError("Incomplete solver final answer")
        return parsed, dict(provenance_data)

    def _audit_solution(candidate: dict) -> Tuple[dict, dict]:
        audit_prompt = (
            "Act as a DELETE-FIRST source-grounding auditor for a school "
            "exercise solution. Compare every step and the final answer against "
            "the exercise prompt, VERIFIED LESSON EVIDENCE, and the attached "
            "verified source figure when present.\n"
            "Reject unsupported embellishment even if scientifically true. "
            "A direct answer required by the exercise may be kept, but its "
            "explanation may not introduce outside facts. Any statement about "
            "connections, relative levels, orientation, shape, measurements, "
            "materials, or geometry must be stated in the prompt/evidence or be "
            "visibly established by the attached figure.\n"
            "Return strict JSON: {"
            "'keep_step_indexes':[int],"
            "'final_answer_valid':bool,"
            "'final_answer_complete':bool,"
            "'figure_faithful':bool,"
            "'no_unrequested_actions':bool,"
            "'pruned_solution_valid':bool,"
            "'reasons':[str]"
            "}. keep_step_indexes are ZERO-BASED indexes of steps that can remain "
            "unchanged. final_answer_complete=true only when the final answer "
            "itself answers every explicit requested action/subquestion. "
            "no_unrequested_actions=false for extra procedures such as shading, "
            "coloring, measuring, marking or construction not requested/supported "
            "by source evidence. pruned_solution_valid=true only when keeping exactly "
            "those steps plus the unchanged final answer produces a correct, "
            "complete, source-grounded solution. If no figure is attached, "
            "figure_faithful must be true.\n"
            f"Exercise: {prompt}\n"
            f"VERIFIED LESSON EVIDENCE: "
            f"{json.dumps(supported_scope, ensure_ascii=False)}\n"
            f"Candidate solution: {json.dumps(candidate, ensure_ascii=False)}"
        )
        parsed_audit = _execute_llm_json_strict(
            audit_prompt,
            image_base64=fig_base64,
            vision_context=vision_context,
            purpose=f"exercise_solution_audit_{exercise.get('exercise_id')}",
            max_attempts=3,
        )
        if not isinstance(parsed_audit, dict):
            raise ValueError("Incomplete solution audit schema")
        return parsed_audit, dict(get_last_llm_provenance())

    try:
        parsed, solution_provenance = _generate_solution()
        audit, verification_provenance = _audit_solution(parsed)

        def _apply_delete_first(candidate: dict, verdict: dict) -> Optional[dict]:
            try:
                keep = sorted({
                    int(x) for x in (verdict.get("keep_step_indexes") or [])
                    if 0 <= int(x) < len(candidate.get("steps") or [])
                })
            except (TypeError, ValueError):
                keep = []
            if not (
                verdict.get("final_answer_valid") is True
                and verdict.get("final_answer_complete") is True
                and verdict.get("figure_faithful") is True
                and verdict.get("no_unrequested_actions") is True
                and verdict.get("pruned_solution_valid") is True
                and keep
            ):
                return None
            removed = [
                idx for idx in range(len(candidate["steps"])) if idx not in keep
            ]
            for idx in removed:
                progress(
                    "REMOVED_OUT_OF_SCOPE_SOLUTION_STEP",
                    exercise_id=exercise.get("exercise_id"),
                    number=exercise.get("number"),
                    step_index=idx,
                )
            cleaned = dict(candidate)
            cleaned["steps"] = [candidate["steps"][idx] for idx in keep]
            cleaned["scope_audit_reasons"] = list(verdict.get("reasons") or [])
            return cleaned

        cleaned = _apply_delete_first(parsed, audit)
        if cleaned is None:
            progress(
                "SOLUTION_STRICT_REGENERATION_REQUIRED",
                exercise_id=exercise.get("exercise_id"),
                number=exercise.get("number"),
                reasons=[str(x) for x in (audit.get("reasons") or [])][:6],
            )
            correction = (
                "\n\nYour previous candidate failed source/figure grounding. "
                "Generate a NEW, shorter solution from scratch. Do not repeat "
                "the rejected claims. Use only the prompt, verified lesson "
                "evidence, and attached verified figure. Auditor reasons: "
                + json.dumps(audit.get("reasons") or [], ensure_ascii=False)
            )
            parsed, solution_provenance = _generate_solution(correction)
            audit, verification_provenance = _audit_solution(parsed)
            cleaned = _apply_delete_first(parsed, audit)

        if cleaned is None:
            raise RuntimeError(
                "SOLVER_SOLUTION_VALIDATION_FAILED:"
                f"{audit.get('reasons', [])}")

        exercise["solution_status"] = "SOLVED"
        cleaned["ai_provenance"] = {
            "solution": dict(solution_provenance),
            "verification": dict(verification_provenance),
        }
        cleaned["source_scope_audited"] = True
        return cleaned
    except Exception as e:
        raise RuntimeError(
            "PRE_SOLVE_FAILED: grounded solver unavailable or failed for "
            f"Ex #{exercise['number']}: {e}")



def prepare_verified_solutions(entry: dict, exercises: list,
                               profile: dict, ev_map: dict,
                               drive_service=None,
                               persist: bool = False) -> None:
    """Solve once, persist each verified result, and resume independently."""
    page_checkpoints = None
    checkpoint_root = None
    if persist:
        if drive_service is None:
            raise RuntimeError("SOLUTION_CHECKPOINT_REQUIRES_DRIVE_SERVICE")
        from scripts import nabil_page_checkpoint as page_checkpoints
        checkpoint_root = resolve_drive_root_id()

    for ex in exercises:
        if ex.get("solution_mode") != "PRE_SOLVED":
            continue
        cached = None
        if page_checkpoints:
            cached = page_checkpoints.load_solution(
                drive_service, checkpoint_root, entry, ex)
        if cached is not None:
            ex["solution_status"] = "SOLVED"
            ex["_pre_solved_solution"] = cached
            progress("SOLUTION_RESTORED_FROM_DRIVE",
                     exercise_id=ex.get("exercise_id"),
                     number=ex.get("number"))
            continue

        try:
            sol = grounded_subject_solver(ex, ev_map, profile)
        except RuntimeError as exc:
            if not str(exc).startswith("PRE_SOLVE_FAILED"):
                raise
            ex["solution_status"] = "OMITTED_UNVERIFIED"
            ex["_pre_solved_solution"] = None
            ex["solution_omission_reason"] = str(exc)[:500]
            progress(
                "SKIPPED_UNVERIFIED_EXERCISE_SOLUTION",
                exercise_id=ex.get("exercise_id"),
                number=ex.get("number"),
                reason=str(exc)[:240],
            )
            continue
        ex["_pre_solved_solution"] = sol
        if page_checkpoints:
            page_checkpoints.save_solution(
                drive_service, checkpoint_root, entry, ex, sol)
            progress("SOLUTION_SAVED_TO_DRIVE",
                     exercise_id=ex.get("exercise_id"),
                     number=ex.get("number"))



def retain_only_verified_solved_exercises(
        exercises: list, *, origin: Optional[str] = None) -> List[dict]:
    """Drop only the exercise that cannot be solved/verified; never drop the lesson."""
    kept = []
    for ex in exercises:
        if origin and ex.get("source_origin", "TEXTBOOK") != origin:
            continue
        solved = (
            ex.get("solution_status") == "SOLVED"
            and isinstance(ex.get("_pre_solved_solution"), dict)
            and bool(ex["_pre_solved_solution"].get("steps"))
            and bool(str(ex["_pre_solved_solution"].get("final_answer") or "").strip())
        )
        if solved:
            kept.append(ex)
        else:
            progress(
                "EXERCISE_DROPPED_NOT_LESSON",
                exercise_id=ex.get("exercise_id"),
                number=ex.get("number"),
                origin=ex.get("source_origin", "TEXTBOOK"),
                reason=str(ex.get("solution_omission_reason") or
                           "NOT_SCIENTIFICALLY_VERIFIED")[:240],
            )
    return kept


def strip_source_rasters_from_student_html(
        html_text: str, ev_map: dict, page_name: str) -> str:
    """Absolute student-facing ban on textbook/page/figure raster pixels.

    Source figures remain available internally to OCR/vision/scientific audit.
    Only NABIL-generated SVG/redraw/lab visuals may reach the lesson pages.
    """
    source_paths = set()
    source_basenames = set()
    for page in ev_map.get("pages_evidence", []):
        for fig in page.get("figures") or []:
            raw = str(fig.get("image_path") or "").strip()
            if raw:
                source_paths.add(raw)
                source_basenames.add(Path(raw).name)

    img_re = re.compile(r"<img\b[^>]*>", re.I | re.S)
    src_re = re.compile(r"\bsrc\s*=\s*([\"'])(.*?)\1", re.I | re.S)
    removed = 0

    def scrub(match):
        nonlocal removed
        tag = match.group(0)
        sm = src_re.search(tag)
        src_value = sm.group(2).strip() if sm else ""
        low = src_value.lower()
        is_source = (
            low.startswith("data:image/")
            or low.startswith("file:")
            or any(path and path in src_value for path in source_paths)
            or any(name and name in src_value for name in source_basenames)
            or ("page" in low and ("cache" in low or "source" in low))
            or ("figure" in low and ("cache" in low or "source" in low))
        )
        if is_source:
            removed += 1
            return "<!-- NABIL: source textbook raster removed; evidence remains internal -->"
        return tag

    cleaned = img_re.sub(scrub, html_text)
    if removed:
        progress("STUDENT_SOURCE_RASTERS_REMOVED",
                 page=page_name, count=removed)

    # Belt-and-suspenders: source raster data URLs must never survive.
    if re.search(r"<img\b[^>]*\bsrc\s*=\s*['\"]data:image/", cleaned, re.I | re.S):
        raise RuntimeError(
            f"STUDENT_SOURCE_RASTER_LEAK_BLOCKED:{page_name}")
    for raw in source_paths:
        if raw and raw in cleaned:
            raise RuntimeError(
                f"STUDENT_SOURCE_RASTER_PATH_LEAK_BLOCKED:{page_name}")
    return cleaned

def build_factory_solution_card_spec(
        entry: dict, exercise: dict, solution: dict) -> Dict[str, Any]:
    """Build the approved Scientific Solution Card payload from verified data only.

    This layer never solves or changes a scientific value. It only maps the
    already-verified solver output into the shared frontend card contract.
    """
    lang_code = resolve_lang_code(entry.get("language", "en"))
    subject = str(entry.get("subject", "")).strip()
    kind_map = {
        "mathematics": "mathematics",
        "math": "mathematics",
        "physics": "physics",
        "chemistry": "chemistry",
        "biology": "biology",
        "science": "general_science",
        "general science": "general_science",
    }
    kind = kind_map.get(subject.lower(), subject.lower() or "general_science")
    steps = [
        str(step).strip() for step in solution.get("steps", [])
        if str(step).strip()
    ]
    final_answer = str(solution.get("final_answer") or "").strip()
    if not steps or not final_answer:
        raise RuntimeError("SCIENTIFIC_SOLUTION_CARD_REQUIRES_VERIFIED_SOLUTION")

    sections = [{
        "label": ui_t(lang_code, "solution_steps"),
        "items": steps,
    }]
    method = str(solution.get("method") or "").strip()
    if method:
        sections.insert(0, {
            "label": ui_t(lang_code, "formula_law"),
            "items": [method],
        })
    verification = solution.get("verification") or []
    if isinstance(verification, str):
        verification = [verification] if verification.strip() else []
    else:
        verification = [
            str(item).strip() for item in verification if str(item).strip()
        ]

    return {
        "renderer_contract": REFERENCE_RENDERER_CONTRACT,
        "lab_key": str(
            exercise.get("_solution_lab_key")
            or exercise.get("_prebuilt_lab_key")
            or ""
        ),
        "exercise_id": str(exercise.get("exercise_id") or ""),
        "kind": kind,
        "subject": subject,
        "language": lang_code,
        "title": str(exercise.get("exact_source_prompt") or entry["canonical_title"])[:220],
        "sections": sections,
        "key_results": [final_answer],
        "verification": verification,
        "source": {
            "lesson_id": entry["lesson_id"],
            "book_id": entry["book_id"],
            "source_page": exercise.get("source_page"),
            "exercise_id": exercise.get("exercise_id"),
            "source_origin": exercise.get("source_origin", "TEXTBOOK"),
        },
    }


def solve_exercise_on_demand_payload(lesson_id: str, sec_type: str, ex_num: int) -> Dict[str, Any]:
    """Universal On-Demand Backend Resolution — Zero Hardcode."""
    ev_path = PERM_EVIDENCE_DIR / f"{lesson_id}.json"
    if not ev_path.exists():
        raise RuntimeError(f"EVIDENCE_NOT_FOUND: {lesson_id}")

    ev_map = json.loads(ev_path.read_text(encoding="utf-8"))
    entry = resolve_canonical_entry(lesson_id)
    profile = resolve_pedagogy_profile(entry)

    matched = None
    for ex in ev_map.get("exercise_evidence", []):
        if ex["section_type"].upper() == sec_type.upper() and int(ex["number"]) == int(ex_num):
            matched = ex
            break

    if not matched:
        raise RuntimeError(f"EXERCISE_NOT_FOUND: {sec_type} #{ex_num} in lesson {lesson_id}")

    sol = grounded_subject_solver(matched, ev_map, profile)
    card = build_factory_solution_card_spec(entry, matched, sol)
    return {"status": "SUCCESS", "solution": sol, "solution_card": card}


# ==============================================================================
# 8. EVIDENCE-DRIVEN SYNTHESIS
# ==============================================================================
def sanitize_generated_narrative(
        concept: dict, narrative: dict, profile: dict,
        figure_image_base64: Optional[str] = None,
        vision_context: Optional[Dict[str, Any]] = None) -> dict:
    """Remove unsupported generated claims at field/item level.

    The official source concept is never edited here. Only AI-generated
    explanation fields, distractors, formulas and units can be removed.
    """
    scalar_fields = [
        "phenomenon", "investigation", "observation", "interpretation",
        "conclusion", "distractor_1", "distractor_2",
    ]
    source_text = str(concept.get("raw_text") or "")
    audit_prompt = (
        "You are a strict curriculum-grounding auditor. Compare the GENERATED "
        "content with the VERIFIED SOURCE text and the verified source figure "
        "when supplied. This audit is DELETE-ONLY: never rewrite, repair, add, "
        "or improve any generated statement.\n"
        "For phenomenon, investigation, observation, interpretation and "
        "conclusion: keep a field only when every scientific claim is supported "
        "by the source evidence.\n"
        "For distractor_1 and distractor_2: keep only when it is intentionally "
        "incorrect as a misconception, uses only concepts/vocabulary within the "
        "lesson scope, and introduces no outside fact, law, apparatus, unit, "
        "quantity or prerequisite.\n"
        "For formulas and units: keep only indexes whose entire item is explicitly "
        "supported by the verified evidence.\n"
        "If uncertain, remove it. Return strict JSON exactly as "
        "{\"keep_fields\":[str],\"keep_formula_indexes\":[int],"
        "\"keep_unit_indexes\":[int],\"removed_reasons\":{str:str}}.\n"
        "Allowed keep_fields: " + json.dumps(scalar_fields) + "\n"
        "VERIFIED SOURCE:\n" + source_text + "\nGENERATED:\n" +
        json.dumps(narrative, ensure_ascii=False)
    )
    try:
        audit = _execute_llm_json_strict(
            audit_prompt,
            image_base64=figure_image_base64,
            vision_context=vision_context,
            purpose=f"narrative_scope_audit_{concept.get('concept_id')}",
        )
    except Exception as exc:
        progress(
            "GENERATED_NARRATIVE_AUDIT_FAILED_CONTENT_REMOVED",
            concept_id=concept.get("concept_id"),
            reason=str(exc)[:240],
        )
        audit = {
            "keep_fields": [],
            "keep_formula_indexes": [],
            "keep_unit_indexes": [],
            "removed_reasons": {
                "all": "AUDIT_UNAVAILABLE_FAIL_CLOSED"
            },
        }

    if not isinstance(audit, dict):
        audit = {}
    keep_fields = {
        str(x) for x in (audit.get("keep_fields") or [])
        if str(x) in scalar_fields
    }
    formula_indexes = {
        int(x) for x in (audit.get("keep_formula_indexes") or [])
        if isinstance(x, int) or (isinstance(x, str) and x.isdigit())
    }
    unit_indexes = {
        int(x) for x in (audit.get("keep_unit_indexes") or [])
        if isinstance(x, int) or (isinstance(x, str) and x.isdigit())
    }
    reasons = audit.get("removed_reasons")
    if not isinstance(reasons, dict):
        reasons = {}

    cleaned = dict(narrative)
    removed = []
    for field in scalar_fields:
        value = str(cleaned.get(field) or "").strip()
        if value and field not in keep_fields:
            removed.append(field)
            cleaned[field] = ""
            progress(
                "REMOVED_OUT_OF_SCOPE_GENERATED_CONTENT",
                concept_id=concept.get("concept_id"),
                component="narrative_field",
                field=field,
                reason=str(reasons.get(field) or "NOT_VERIFIED_AGAINST_SOURCE")[:240],
            )

    formulas = list(cleaned.get("formulas") or [])
    kept_formulas = []
    for idx, value in enumerate(formulas):
        if idx in formula_indexes:
            kept_formulas.append(value)
        else:
            progress(
                "REMOVED_OUT_OF_SCOPE_GENERATED_CONTENT",
                concept_id=concept.get("concept_id"),
                component="formula",
                field=str(idx),
                reason=str(reasons.get(f"formula_{idx}") or
                           "FORMULA_NOT_VERIFIED_AGAINST_SOURCE")[:240],
            )
    cleaned["formulas"] = kept_formulas

    units = list(cleaned.get("units") or [])
    kept_units = []
    for idx, value in enumerate(units):
        if idx in unit_indexes:
            kept_units.append(value)
        else:
            progress(
                "REMOVED_OUT_OF_SCOPE_GENERATED_CONTENT",
                concept_id=concept.get("concept_id"),
                component="unit",
                field=str(idx),
                reason=str(reasons.get(f"unit_{idx}") or
                           "UNIT_NOT_VERIFIED_AGAINST_SOURCE")[:240],
            )
    cleaned["units"] = kept_units
    cleaned["_removed_generated_fields"] = removed
    cleaned["_scope_audited"] = True
    return cleaned


def synthesize_concept_narrative(
        concept: dict, profile: dict,
        figure_image_base64: Optional[str] = None,
        vision_context: Optional[Dict[str, Any]] = None) -> dict:
    narrative_lang_code = resolve_lang_code(profile["language"])
    teaching_signature = resolve_teaching_signature(concept, profile)
    prompt = (
        f"You are Teacher NABIL, an autonomous digital teacher teaching this concept so a learner can understand it without a human teacher operating the lesson. "
        "Stay grounded STRICTLY in the extracted textbook text and verified source figure when provided. "
        "Teach like an excellent student-facing tutor: start directly, use small logical steps, explain WHY each move is made, ask the learner to notice/predict/try, and never dump textbook prose. "
        f"AGE/LEVEL TEACHING CONTRACT: {json.dumps(teaching_signature, ensure_ascii=False)}. "
        "Follow the subject_sequence as the pedagogical order, but NEVER add a scientific or mathematical fact that is not supported by evidence. "
        "Do NOT sound like a scanned textbook and do NOT reproduce textbook layout. Re-teach the idea in a natural classroom flow: "
        "phenomenon = what the learner should first LOOK AT or wonder about; "
        "investigation = what the learner should TRY or manipulate; "
        "observation = what the learner can NOTICE from the evidence; "
        "interpretation = the short WHY/WHAT-DOES-THIS-MEAN discussion; "
        "conclusion = the concise rule the learner should formulate. "
        "Keep each field short, concrete and age-appropriate. The lesson flow must feel like: SEE → TRY → NOTICE → THINK → CONCLUDE → APPLY. "
        f"Generate plausible wrong answers (distractors) derived only from common misconceptions of this same text.\n\n"
        f"{narrative_language_instruction(narrative_lang_code)}\n"
        + ("When the lesson language is Arabic, write clear Modern Standard Arabic (فصحى) only; understand dialect but do not imitate it. " if narrative_lang_code == "ar" else "")
        + "Preserve established mathematical/scientific terminology, symbols and units.\n\n"
        f"TEXT: {concept['raw_text']}\n\n"
        f"Subject: {profile['subject']}, Level: {profile['level']}\n"
        "Return strictly JSON: {"
        "'phenomenon': str, 'investigation': str, 'observation': str, 'interpretation': str, 'conclusion': str, "
        "'distractor_1': str, 'distractor_2': str, 'formulas': [str], 'units': [str]"
        "} — every field must be traceable to the TEXT above."
    )
    try:
        res = execute_llm_completion(
            prompt, json_mode=True, temperature=0.0,
            image_base64=figure_image_base64,
            vision_context=vision_context)
        parsed = json.loads(res)
        for k in ["phenomenon", "investigation", "observation", "interpretation", "conclusion", "distractor_1", "distractor_2"]:
            if not parsed.get(k):
                raise ValueError(f"Missing field {k}")
        cleaned = sanitize_generated_narrative(
            concept, parsed, profile,
            figure_image_base64=figure_image_base64,
            vision_context=vision_context)
        if narrative_lang_code == "ar":
            for key in (
                "phenomenon", "investigation", "observation",
                "interpretation", "conclusion", "distractor_1", "distractor_2",
            ):
                _assert_formal_arabic_text(
                    cleaned.get(key, ""),
                    purpose=f"narrative_{concept.get('concept_id')}_{key}",
                )
            cleaned["_formal_arabic_verified"] = True
        return cleaned
    except Exception as e:
        raise RuntimeError(f"NARRATIVE_SYNTHESIS_FAILED: Unable to ground concept narrative from evidence ({e})")


def _normalized_lab_evidence(value: str) -> str:
    # تطبيع بسيط للتحقق من أن الاقتباس الذي استند إليه المختبر موجود فعلاً في الدليل.
    return re.sub(r"\\s+", " ", str(value or "")).strip().lower()


def _deduction_question(lang_code: str, title: str) -> str:
    # صياغة السؤال بحسب لغة الدرس، من دون تغيير المصطلح العلمي الأصلي.
    if lang_code == "ar":
        return f"أي استنتاج علمي تؤكده الأدلة الخاصة بـ «{title}»؟"
    if lang_code == "fr":
        return f"Quelle déduction scientifique est confirmée par les preuves concernant « {title} » ?"
    return f"Which scientific deduction is confirmed by the evidence for '{title}'?"


def build_verified_lab_spec(entry: dict, concept: dict, narrative: dict, profile: dict,
                            figure_image_base64: Optional[str] = None,
                            vision_context: Optional[Dict[str, Any]] = None) -> dict:
    """
    يبني Lab Spec من الدليل نفسه.
    لا يُسمح للموديل بإدخال أرقام أو قوانين أو سلوك غير موجود في النص/الشكل الموثق.
    إذا المفهوم لا يناسب مختبراً من الأنواع المدعومة، يعيد supported=false.
    """
    lang_code = resolve_lang_code(entry["language"])
    math_records = concept.get("math_records") or []
    prompt = (
        "You are designing ONE evidence-grounded interactive educational lab strictly from verified curriculum evidence.\n"
        "If the SOURCE or verified FIGURE explicitly describes a manipulable change, observable invariant, quantitative relation, ordered process, or experiment that fits one of the allowed kinds, you MUST return supported=true and build it. "
        "Return supported=false only when no allowed interaction can be supported without adding scientific information. Never suppress an applicable lab just because the specification is difficult to produce.\n"
        "Allowed kinds only:\n"
        "1) FORMULA_CALCULATOR: only when an explicit two-input formula using +, -, *, or / exists in SOURCE or MATH_RECORDS. "
        "Never invent min/max/default/step values; the student will enter numbers.\n"
        "2) ORIENTATION_INVARIANT: only when SOURCE/FIGURE explicitly establishes that an observable element keeps a horizontal or vertical orientation while its surrounding object changes orientation.\n"
        "3) SHAPE_RESPONSE: only when SOURCE/FIGURE explicitly establishes that the observed object's shape is fixed or conforms to a changed container/boundary.\n"
        "4) DC_SERIES_CIRCUIT: only when SOURCE explicitly supports a two-resistor series circuit, Ohm's law, same-current-in-series, series equivalent resistance, AND the open/closed-switch current rule. "
        "Required fields: resistors=[two source labels], switch_control=true, rules={series_resistance_sum:true,series_same_current:true,ohms_law:true,open_switch_zero_current:true}.\n"
        "5) OPTICS_REFLECTION: only when SOURCE explicitly supports a normal perpendicular to the reflecting surface, angles measured from the normal, AND angle of incidence equals angle of reflection. "
        "Required fields: angles_measured_from_normal=true, normal_perpendicular_surface=true, law='angle_of_incidence_equals_angle_of_reflection'.\n"
        "6) IONIC_COMPOUND: only when SOURCE explicitly supports ionic electron transfer, the cation/anion charges, the whole-number ion ratio, and charge neutrality. "
        "Required fields: cation={symbol,charge}, anion={symbol,charge}, cation_ratio, anion_ratio, electron_transfer_count, bond_type='ionic'.\n"
        "7) GEOMETRY_PROOF: prefer this for geometry theorems/proofs/constructions when SOURCE or verified FIGURE supports named points/segments and proof relations. "
        "Required: points=[{label,x,y}] with x,y as 0..100 LAYOUT coordinates only; segments=[{id,a,b}]; marks=[...]; proof_steps=[...]. "
        "Allowed mark types: equal_segments, equal_angles, perpendicular, parallel, midpoint, symmetry_axis. "
        "Every mark MUST carry evidence_quote copied exactly from SOURCE. Equal segment marks use targets=[segment ids]; equal angle/perpendicular marks use angles=[{a,vertex,b}]; parallel/midpoint use targets; symmetry_axis uses axis_segment and optional point_pairs. "
        "Every proof step MUST contain title,text,formula,target_ids,reveal_marks,evidence_quote; evidence_quote must be an exact SOURCE quote. "
        "In target_ids use ONLY a mark id, point:<point label>, or segment:<segment id>; order target_ids to match the spoken sentences so the teacher arrow follows the sentence meaning. "
        "Never add an equality tick, equal-angle arc, right-angle square, parallel arrow, midpoint mark, congruence implication or symmetry effect merely because the sketch looks that way.\n"
        "8) EVIDENCE_SEQUENCE: for ANY subject when SOURCE explicitly gives two or more ordered or structurally related evidence-backed ideas, parts, stages, transformations, constructions, grammatical steps, historical developments, geographic relations, or other explainable sequence that can be highlighted or animated without inventing a missing fact. "
        "Required field: steps=[{label:str,evidence_quote:str}] with 2..8 ordered steps; every evidence_quote must be an exact contiguous SOURCE quote.\n"
        "9) EVIDENCE_REVEAL: universal fallback for ANY subject/concept when no richer lab kind fits. "
        "Use 1..8 exact SOURCE-backed items and reveal/highlight them interactively. "
        "Required field: items=[{label:str,evidence_quote:str}], each evidence_quote an exact contiguous SOURCE quote. "
        "This means every concept can still have a real interactive lab without inventing science.\n"
        "For DC_SERIES_CIRCUIT, OPTICS_REFLECTION and IONIC_COMPOUND also return evidence_quotes: an object containing an EXACT SOURCE quote for EACH scientific invariant declared by the spec.\n"
        "Every supported lab must contain an exact evidence quote from SOURCE when evidence_basis=text. "
        "If evidence_basis=figure, a verified source figure must be supplied.\n"
        "Every supported lab MUST include teacher_script with 2..12 steps derived from THIS evidence, never a canned demo. "
        "Each step contains say,target_ids,action,state_before,state_after,scientific_constraints,evidence_quote. "
        "Allowed actions: point,highlight,set_state,animate,observe,explain,conclude. "
        "Apply state_after BEFORE NABIL speaks its consequence; target_ids follow the sentence meaning. "
        "For circuits, current/charge flow is forbidden while switch_closed=false; close the switch visibly first. "
        "For every domain, animate/reveal a result only after its evidence-backed conditions are established. "
        "All states/actions/constraints come from SOURCE or verified FIGURE; never invent science for animation.\n"
        "Student-facing title/instructions/observation must stay within the scientific meaning of the evidence.\n"
        + narrative_language_instruction(lang_code) + "\n\n"
        f"CONCEPT_ID: {concept['concept_id']}\n"
        f"SUBJECT: {profile['subject']}\n"
        f"SOURCE: {concept.get('raw_text','')}\n"
        f"MATH_RECORDS: {json.dumps(math_records, ensure_ascii=False)}\n"
        f"GROUNDED_NARRATIVE: {json.dumps(narrative, ensure_ascii=False)}\n\n"
        "Return strict JSON. For unsupported: "
        "{'supported': false, 'reason': str, 'evidence_ref': str}. "
        "For supported include: supported=true, kind, title, instructions, observation, evidence_ref, evidence_basis ('text'|'figure'), evidence_quote. "
        "FORMULA_CALCULATOR additionally: source_formula and formula={output,input_a,input_b,operator,output_unit}. "
        "ORIENTATION_INVARIANT additionally: invariant_orientation ('horizontal'|'vertical'). "
        "SHAPE_RESPONSE additionally: behavior ('fixed'|'conforms'). "
        "GEOMETRY_PROOF additionally uses the exact points/segments/marks/proof_steps schema above. "
        "EVIDENCE_SEQUENCE additionally: steps=[{label,evidence_quote}]. "
        "EVIDENCE_REVEAL additionally: items=[{label,evidence_quote}]. "
        "Advanced science kinds must include the exact fields listed above plus evidence_quotes."
    )
    try:
        spec = _execute_llm_json_strict(
            prompt,
            image_base64=figure_image_base64,
            vision_context=vision_context,
            purpose=f"lab_spec_{concept.get('concept_id')}",
            max_attempts=3,
        )
    except Exception as exc:
        raise RuntimeError(f"LAB_SPEC_JSON_INVALID: {exc}") from exc

    if not isinstance(spec, dict):
        raise RuntimeError("LAB_SPEC_INVALID: expected object")
    if spec.get("supported") is not True:
        # Universal classroom contract: every concept must still have an
        # interactive lab. When no richer simulation is justified, fall back
        # deterministically to an evidence-reveal lab built only from the
        # verified source text. No new scientific claim is introduced.
        source_text = str(concept.get("raw_text") or "").strip()
        if not source_text:
            raise RuntimeError("LAB_FALLBACK_SOURCE_EMPTY")
        fallback_quote = source_text[:700]
        spec = {
            "supported": True,
            "kind": "EVIDENCE_REVEAL",
            "title": str(concept.get("title") or "NABIL Interactive Explanation"),
            "instructions": {
                "ar": "استكشف الفكرة مع نبيل خطوة خطوة.",
                "fr": "Explore l’idée avec NABIL étape par étape.",
                "en": "Explore the idea with NABIL step by step.",
            }.get(resolve_lang_code(entry.get("language", "en")), "Explore the idea with NABIL step by step."),
            "observation": {
                "ar": "كل ما يظهر هنا مأخوذ من الدليل الموثق لهذه الفكرة.",
                "fr": "Tout ce qui apparaît ici vient de la preuve vérifiée de cette idée.",
                "en": "Everything shown here comes from the verified evidence for this idea.",
            }.get(resolve_lang_code(entry.get("language", "en")), "Everything shown here comes from the verified evidence for this idea."),
            "evidence_ref": concept["concept_id"],
            "evidence_basis": "text",
            "evidence_quote": fallback_quote,
            "items": [{
                "label": str(concept.get("title") or "Verified idea"),
                "evidence_quote": fallback_quote,
            }],
            "fallback_reason": str(spec.get("reason") or "NO_RICHER_LAB_KIND"),
            "teacher_script": [
                {"say": str(concept.get("title") or "Observe the verified evidence."), "target_ids": ["evidence:0"], "action": "point",
                 "state_before": {"revealed_index": -1}, "state_after": {"revealed_index": 0},
                 "scientific_constraints": ["Reveal only verified source evidence."], "evidence_quote": fallback_quote},
                {"say": str(narrative.get("conclusion") or narrative.get("observation") or concept.get("title") or "Conclude from the verified evidence."),
                 "target_ids": ["evidence:0"], "action": "conclude",
                 "state_before": {"revealed_index": 0}, "state_after": {"revealed_index": 0},
                 "scientific_constraints": ["Do not exceed verified source evidence."], "evidence_quote": fallback_quote},
            ],
        }
        progress(
            "LAB_UNIVERSAL_EVIDENCE_REVEAL_FALLBACK",
            concept_id=concept.get("concept_id"),
            source_page=concept.get("source_page"),
        )
    # A provider can return a scientifically useful supported lab while omitting
    # the teacher_script object.  That is a recoverable output-shape failure,
    # not a reason to discard the verified lesson.  First ask for a bounded,
    # evidence-locked repair of the EXISTING spec.  If repair still fails,
    # downgrade only this lab to the deterministic EVIDENCE_REVEAL contract.
    # We never fabricate domain state transitions for a richer lab.
    def _teacher_script_shape_valid(value: Any) -> bool:
        if not isinstance(value, list) or not 2 <= len(value) <= 12:
            return False
        allowed_actions = {"point", "highlight", "set_state", "animate", "observe", "explain", "conclude"}
        for teacher_step in value:
            if not isinstance(teacher_step, dict):
                return False
            if not str(teacher_step.get("say") or "").strip():
                return False
            if str(teacher_step.get("action") or "") not in allowed_actions:
                return False
            if not isinstance(teacher_step.get("target_ids"), list):
                return False
            if not isinstance(teacher_step.get("state_before"), dict):
                return False
            if not isinstance(teacher_step.get("state_after"), dict):
                return False
            if not isinstance(teacher_step.get("scientific_constraints"), list):
                return False
            if not str(teacher_step.get("evidence_quote") or "").strip():
                return False
        return True

    teacher_script = spec.get("teacher_script")
    if spec.get("supported") is True and not _teacher_script_shape_valid(teacher_script):
        progress(
            "LAB_TEACHER_SCRIPT_REPAIR_START",
            concept_id=concept.get("concept_id"),
            source_page=concept.get("source_page"),
            kind=str(spec.get("kind") or ""),
        )
        repair_prompt = (
            "Repair ONLY the missing/invalid teacher_script of this already generated "
            "evidence-grounded lab. Do not add, remove, or alter any scientific claim, "
            "number, law, relation, geometry mark, circuit rule, or evidence quote. "
            "Return the COMPLETE lab spec as strict JSON. teacher_script must contain "
            "2..12 steps. Each step must contain say,target_ids,action,state_before,"
            "state_after,scientific_constraints,evidence_quote. Allowed actions: "
            "point,highlight,set_state,animate,observe,explain,conclude. Every "
            "evidence_quote must be an exact contiguous quote from SOURCE when the "
            "lab uses text evidence. target_ids must refer only to objects already "
            "present in the supplied lab spec. Apply state_after before speaking its "
            "consequence. Never animate/reveal a consequence before its verified "
            "condition is established. For a DC circuit, current/charge flow is "
            "forbidden while switch_closed=false; visibly close the switch first. "
            "If you cannot repair without inventing information, return "
            "{\"repairable\":false}.\n\n"
            f"SOURCE:\n{concept.get('raw_text','')}\n\n"
            f"EXISTING_LAB_SPEC:\n{json.dumps(spec, ensure_ascii=False)}"
        )
        repaired = None
        try:
            candidate = _execute_llm_json_strict(
                repair_prompt,
                image_base64=figure_image_base64,
                vision_context=vision_context,
                purpose=f"lab_teacher_script_repair_{concept.get('concept_id')}",
                max_attempts=2,
            )
            if isinstance(candidate, dict) and candidate.get("repairable") is not False:
                candidate_script = candidate.get("teacher_script")
                if _teacher_script_shape_valid(candidate_script):
                    # SECURITY/SCIENCE BOUNDARY: the repair model is allowed to
                    # supply ONLY teacher_script.  Never accept a rewritten kind,
                    # law, geometry, circuit state, evidence basis, quote, or any
                    # other scientific field from the repair response.
                    repaired = dict(spec)
                    repaired["teacher_script"] = candidate_script
        except Exception as exc:
            progress(
                "LAB_TEACHER_SCRIPT_REPAIR_PROVIDER_FAILED",
                concept_id=concept.get("concept_id"),
                reason=str(exc)[:300],
            )

        if repaired is not None:
            spec = repaired
            progress(
                "LAB_TEACHER_SCRIPT_REPAIRED",
                concept_id=concept.get("concept_id"),
                steps=len(spec.get("teacher_script") or []),
            )
        else:
            source_text = str(concept.get("raw_text") or "").strip()
            if not source_text:
                raise RuntimeError("LAB_TEACHER_SCRIPT_REPAIR_FAILED_SOURCE_EMPTY")
            fallback_quote = source_text[:700]
            conclusion = str(
                narrative.get("conclusion")
                or narrative.get("observation")
                or concept.get("title")
                or "Conclude from the verified evidence."
            ).strip()
            spec = {
                "supported": True,
                "kind": "EVIDENCE_REVEAL",
                "title": str(concept.get("title") or "NABIL Interactive Explanation"),
                "instructions": {
                    "ar": "استكشف الفكرة مع نبيل خطوة خطوة.",
                    "fr": "Explore l’idée avec NABIL étape par étape.",
                    "en": "Explore the idea with NABIL step by step.",
                }.get(lang_code, "Explore the idea with NABIL step by step."),
                "observation": {
                    "ar": "كل ما يظهر هنا مأخوذ من الدليل الموثق لهذه الفكرة.",
                    "fr": "Tout ce qui apparaît ici vient de la preuve vérifiée de cette idée.",
                    "en": "Everything shown here comes from the verified evidence for this idea.",
                }.get(lang_code, "Everything shown here comes from the verified evidence for this idea."),
                "evidence_ref": concept["concept_id"],
                "evidence_basis": "text",
                "evidence_quote": fallback_quote,
                "items": [{
                    "label": str(concept.get("title") or "Verified idea"),
                    "evidence_quote": fallback_quote,
                }],
                "fallback_reason": "TEACHER_SCRIPT_OUTPUT_SHAPE_UNRECOVERABLE",
                "teacher_script": [
                    {
                        "say": str(concept.get("title") or "Observe the verified evidence."),
                        "target_ids": ["evidence:0"],
                        "action": "point",
                        "state_before": {"revealed_index": -1},
                        "state_after": {"revealed_index": 0},
                        "scientific_constraints": ["Reveal only verified source evidence."],
                        "evidence_quote": fallback_quote,
                    },
                    {
                        "say": conclusion,
                        "target_ids": ["evidence:0"],
                        "action": "conclude",
                        "state_before": {"revealed_index": 0},
                        "state_after": {"revealed_index": 0},
                        "scientific_constraints": ["Do not exceed verified source evidence."],
                        "evidence_quote": fallback_quote,
                    },
                ],
            }
            progress(
                "LAB_TEACHER_SCRIPT_SAFE_EVIDENCE_REVEAL_FALLBACK",
                concept_id=concept.get("concept_id"),
                source_page=concept.get("source_page"),
            )

    if spec.get("evidence_ref") != concept.get("concept_id"):
        # evidence_ref is provenance metadata, not a scientific claim. The lab
        # has just been generated from this concept's locked SOURCE/FIGURE, so
        # canonicalize a model formatting mistake instead of silently deleting
        # an otherwise verifiable interactive lab.
        progress(
            "LAB_SPEC_EVIDENCE_REF_CANONICALIZED",
            concept_id=concept.get("concept_id"),
            source_page=concept.get("source_page"),
            received_ref=str(spec.get("evidence_ref") or "")[:120],
        )
        spec["evidence_ref"] = concept["concept_id"]

    basis = str(spec.get("evidence_basis") or "").lower()
    quote = str(spec.get("evidence_quote") or "").strip()
    if basis == "text":
        if not quote:
            raise RuntimeError("LAB_SPEC_TEXT_EVIDENCE_MISSING")
        source_norm = _normalized_lab_evidence(concept.get("raw_text", ""))
        quote_norm = _normalized_lab_evidence(quote)
        if quote_norm not in source_norm:
            raise RuntimeError("LAB_SPEC_TEXT_EVIDENCE_NOT_FOUND")
    elif basis == "figure":
        if not figure_image_base64 or not concept.get("figure_refs"):
            raise RuntimeError("LAB_SPEC_FIGURE_EVIDENCE_MISSING")
    else:
        raise RuntimeError("LAB_SPEC_EVIDENCE_BASIS_INVALID")

    kind = str(spec.get("kind") or "").upper()
    if kind == "FORMULA_CALCULATOR":
        source_formula = _normalized_lab_evidence(spec.get("source_formula", ""))
        formula_haystack = _normalized_lab_evidence(
            str(concept.get("raw_text", "")) + " " +
            " ".join(str(r.get("raw") or "") for r in math_records if isinstance(r, dict))
        )
        if not source_formula or source_formula not in formula_haystack:
            raise RuntimeError("LAB_FORMULA_NOT_PRESENT_IN_SOURCE")

    # Advanced science labs must prove each declared invariant with an exact
    # textbook quote before deterministic rendering is allowed. This prevents
    # a visually impressive lab from silently introducing a scientific rule.
    advanced_required_quotes = {
        "DC_SERIES_CIRCUIT": {
            "series_resistance_sum",
            "series_same_current",
            "ohms_law",
            "open_switch_zero_current",
        },
        "OPTICS_REFLECTION": {
            "normal_perpendicular_surface",
            "angles_measured_from_normal",
            "reflection_law",
        },
        "IONIC_COMPOUND": {
            "ionic_bond",
            "cation_charge",
            "anion_charge",
            "ion_ratio",
            "electron_transfer",
            "charge_neutrality",
        },
    }
    if kind in advanced_required_quotes:
        evidence_quotes = spec.get("evidence_quotes")
        if not isinstance(evidence_quotes, dict):
            raise RuntimeError("LAB_ADVANCED_EVIDENCE_QUOTES_MISSING")
        source_norm = _normalized_lab_evidence(concept.get("raw_text", ""))
        missing = advanced_required_quotes[kind] - set(evidence_quotes)
        if missing:
            raise RuntimeError(
                "LAB_ADVANCED_EVIDENCE_QUOTES_INCOMPLETE:" +
                ",".join(sorted(missing)))
        for claim in sorted(advanced_required_quotes[kind]):
            exact_quote = _normalized_lab_evidence(evidence_quotes.get(claim, ""))
            if not exact_quote or exact_quote not in source_norm:
                raise RuntimeError(
                    f"LAB_ADVANCED_EVIDENCE_QUOTE_NOT_FOUND:{claim}")

    if kind == "GEOMETRY_PROOF":
        source_norm = _normalized_lab_evidence(concept.get("raw_text", ""))
        marks = spec.get("marks")
        proof_steps = spec.get("proof_steps")
        if not isinstance(marks, list) or not isinstance(proof_steps, list):
            raise RuntimeError("LAB_GEOMETRY_EVIDENCE_STRUCTURE_MISSING")
        for index, mark in enumerate(marks):
            quote = _normalized_lab_evidence((mark or {}).get("evidence_quote", ""))
            if not quote or quote not in source_norm:
                raise RuntimeError(
                    f"LAB_GEOMETRY_MARK_EVIDENCE_NOT_FOUND:{index}")
        for index, step in enumerate(proof_steps):
            quote = _normalized_lab_evidence((step or {}).get("evidence_quote", ""))
            if not quote or quote not in source_norm:
                raise RuntimeError(
                    f"LAB_GEOMETRY_STEP_EVIDENCE_NOT_FOUND:{index}")

    if kind == "EVIDENCE_SEQUENCE":
        steps = spec.get("steps")
        if not isinstance(steps, list) or not 2 <= len(steps) <= 8:
            raise RuntimeError("LAB_SEQUENCE_STEPS_INVALID")
        source_norm = _normalized_lab_evidence(concept.get("raw_text", ""))
        for index, step in enumerate(steps):
            if not isinstance(step, dict):
                raise RuntimeError(f"LAB_SEQUENCE_STEP_INVALID:{index}")
            label = str(step.get("label") or "").strip()
            quote = _normalized_lab_evidence(step.get("evidence_quote", ""))
            if not label or not quote or quote not in source_norm:
                raise RuntimeError(
                    f"LAB_SEQUENCE_EVIDENCE_QUOTE_NOT_FOUND:{index}")

    if kind == "EVIDENCE_REVEAL":
        items = spec.get("items")
        if not isinstance(items, list) or not 1 <= len(items) <= 8:
            raise RuntimeError("LAB_REVEAL_ITEMS_INVALID")
        source_norm = _normalized_lab_evidence(concept.get("raw_text", ""))
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                raise RuntimeError(f"LAB_REVEAL_ITEM_INVALID:{index}")
            label = str(item.get("label") or "").strip()
            quote = _normalized_lab_evidence(item.get("evidence_quote", ""))
            if not label or not quote or quote not in source_norm:
                raise RuntimeError(
                    f"LAB_REVEAL_EVIDENCE_QUOTE_NOT_FOUND:{index}")

    teacher_script = spec.get("teacher_script")
    if not isinstance(teacher_script, list) or not 2 <= len(teacher_script) <= 12:
        raise RuntimeError("LAB_TEACHER_SCRIPT_REQUIRED")
    allowed_teacher_actions = {"point","highlight","set_state","animate","observe","explain","conclude"}
    source_norm = _normalized_lab_evidence(concept.get("raw_text", ""))
    switch_closed = False
    for step_index, step in enumerate(teacher_script):
        if not isinstance(step, dict) or not str(step.get("say") or "").strip():
            raise RuntimeError(f"LAB_TEACHER_STEP_INVALID:{step_index}")
        if str(step.get("action") or "") not in allowed_teacher_actions:
            raise RuntimeError(f"LAB_TEACHER_ACTION_INVALID:{step_index}")
        if not isinstance(step.get("target_ids", []), list) or not isinstance(step.get("state_before"), dict) or not isinstance(step.get("state_after"), dict):
            raise RuntimeError(f"LAB_TEACHER_STATE_INVALID:{step_index}")
        if not isinstance(step.get("scientific_constraints"), list):
            raise RuntimeError(f"LAB_TEACHER_CONSTRAINTS_INVALID:{step_index}")
        q = _normalized_lab_evidence(step.get("evidence_quote", ""))
        if not q or (basis == "text" and q not in source_norm):
            raise RuntimeError(f"LAB_TEACHER_EVIDENCE_NOT_FOUND:{step_index}")
        if kind == "DC_SERIES_CIRCUIT":
            before=step.get("state_before") or {}; after=step.get("state_after") or {}
            if "switch_closed" in before and bool(before["switch_closed"]) != switch_closed:
                raise RuntimeError(f"LAB_CIRCUIT_STATE_DISCONTINUITY:{step_index}")
            next_closed=bool(after.get("switch_closed",switch_closed))
            words=(str(step.get("say") or "")+" "+str(step.get("action") or "")).lower()
            if any(x in words for x in ("current","charge flow","تيار","مرور الشحن")) and not next_closed:
                raise RuntimeError(f"LAB_CIRCUIT_FLOW_WITH_OPEN_SWITCH:{step_index}")
            switch_closed=next_closed
    validate_lab_spec(spec)
    # REQUIREMENT_5_FINAL_GATE
    # Final fail-closed source/science/visual acceptance. This runs AFTER the
    # existing domain validators and BEFORE the spec can leave the factory.
    spec = validate_requirement5_lab(
        spec,
        source_text=str(concept.get("raw_text") or ""),
        source_figure_verified=bool(
            figure_image_base64 and (concept.get("figure_refs") or vision_context)
        ),
    )
    assert_requirement5_publishable(
        spec,
        lesson_id=str(entry.get("lesson_id") or ""),
        lab_id=str(concept.get("concept_id") or ""),
    )
    return spec



def render_whole_lesson_smart_lab(
        title: str, activities: list, lang_code: str) -> str:
    """One final Smart Board that orchestrates every already-verified concept lab.

    It introduces no new science.  Each slide uses the audited narrative and
    loads that concept's prebuilt lab inside an isolated iframe, so ids/scripts
    do not collide with the concept lab already embedded beside its paragraph.
    """
    if not activities:
        return ""
    labels = {
        "ar": {
            "title": "🧠 مختبر نبيل الشامل للدرس",
            "subtitle": "سيشرح نبيل الدرس من الفكرة الأولى حتى الأخيرة، مع المختبر المناسب لكل فكرة.",
            "prev": "◀ الفكرة السابقة",
            "next": "الفكرة التالية ▶",
            "current": "🔊 اشرح هذه الفكرة",
            "all": "▶ اشرح الدرس من البداية",
            "stop": "■ أوقف الشرح",
            "teacher": "نبيل يشرح الآن",
            "first_transition": "نبدأ الآن بالفكرة:",
            "next_transition": "ننتقل الآن إلى الفكرة التالية:",
            "see": "انظر", "try": "جرّب", "notice": "لاحظ",
            "think": "فكّر", "conclude": "استنتج",
        },
        "fr": {
            "title": "🧠 Laboratoire intégral de la leçon",
            "subtitle": "NABIL enseigne la leçon du premier concept au dernier avec le laboratoire vérifié de chaque idée.",
            "prev": "◀ Concept précédent", "next": "Concept suivant ▶",
            "current": "🔊 Expliquer ce concept",
            "all": "▶ Expliquer toute la leçon",
            "stop": "■ Arrêter", "teacher": "NABIL explique",
            "first_transition": "Commençons par l’idée :",
            "next_transition": "Passons maintenant à l’idée suivante :",
            "see": "Observe", "try": "Essaie", "notice": "Remarque",
            "think": "Réfléchis", "conclude": "Conclus",
        },
        "en": {
            "title": "🧠 NABIL Whole-Lesson Smart Lab",
            "subtitle": "NABIL teaches the lesson from the first concept to the last, using each concept's verified lab.",
            "prev": "◀ Previous concept", "next": "Next concept ▶",
            "current": "🔊 Explain this concept",
            "all": "▶ Explain the whole lesson",
            "stop": "■ Stop", "teacher": "NABIL is explaining",
            "first_transition": "We begin with the idea:",
            "next_transition": "Now we move to the next idea:",
            "see": "See", "try": "Try", "notice": "Notice",
            "think": "Think", "conclude": "Conclude",
        },
    }[lang_code if lang_code in {"ar", "fr", "en"} else "en"]
    slides = []
    for act in activities:
        lab_html = str(act.get("lab_html") or "")
        if not lab_html:
            continue
        match = re.search(r'data-demo-ms="(\d+)"', lab_html)
        demo_ms = max(3500, min(30000, int(match.group(1)) if match else 9000))
        teaching_steps = act.get("teaching_steps") or []
        if teaching_steps:
            flow = [{
                "label": str(step.get("label") or ""),
                "text": str(step.get("sentence") or ""),
                "formula": str(step.get("formula") or ""),
                "kind": str(step.get("kind") or ""),
            } for step in teaching_steps if str(step.get("sentence") or "").strip()]
        else:
            fallback_flow = [
                [labels["see"], str(act.get("phenomenon") or "")],
                [labels["try"], str(act.get("investigation") or "")],
                [labels["notice"], str(act.get("observation") or "")],
                [labels["think"], str(act.get("interpretation") or "")],
                [labels["conclude"], str(act.get("conclusion") or "")],
            ]
            flow = [{"label": k, "text": v, "formula": "", "kind": ""}
                    for k, v in fallback_flow if v.strip()]
        srcdoc = (
            '<!doctype html><html><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<style>html,body{margin:0;background:#05172d;color:#eef8ff;overflow-x:hidden}'
            'body{padding:4px}*{box-sizing:border-box}</style>'
            '<script>try{window.NABILLessonE2E=parent.NABILLessonE2E}catch(e){}</script>'
            '</head><body>' + lab_html + '</body></html>'
        )
        slides.append({
            "concept_id": str(act.get("concept_id") or ""),
            "title": str(act.get("title") or ""),
            "flow": flow,
            "teaching_mode": str((act.get("teaching_signature") or {}).get("mode") or "default"),
            "teaching_level": str((act.get("teaching_signature") or {}).get("level") or ""),
            "first_transition": labels["first_transition"],
            "next_transition": labels["next_transition"],
            "srcdoc": srcdoc,
            "demo_ms": demo_ms,
        })
    if not slides:
        return ""
    payload = json.dumps(slides, ensure_ascii=False).replace("</", "<\\/")
    return f'''
<section id="nabilWholeLessonSmartLab" class="nabil-whole-lesson-smart-lab"
 data-whole-lesson-smart-lab="true" data-renderer-contract="{REFERENCE_RENDERER_CONTRACT}"
 data-concept-count="{len(slides)}" style="margin-top:26px;background:#071827;color:#eef8ff;border:1px solid #24506f;border-radius:18px;padding:13px;box-shadow:0 18px 42px #0006;">
 <style>
 #nabilWholeLessonSmartLab .wl-top{{display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap}}
 #nabilWholeLessonSmartLab .wl-teacher{{display:flex;align-items:center;gap:7px;background:#061725;border:1px solid #2b6485;border-radius:999px;padding:6px 10px;font-size:12px;font-weight:800}}
 #nabilWholeLessonSmartLab .wl-orb{{width:18px;height:18px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff,#2de1ff 35%,#0c5d76 70%);box-shadow:0 0 16px #2de1ff99}}
 #nabilWholeLessonSmartLab .wl-layout{{display:grid;grid-template-columns:minmax(0,1.55fr) minmax(280px,.8fr);gap:11px;margin-top:10px}}
 #nabilWholeLessonSmartLab .wl-stage{{background:#020912;border:1px solid #1c4569;border-radius:14px;overflow:hidden;min-width:0}}
 #nabilWholeLessonSmartLab iframe{{display:block;width:100%;height:590px;border:0;background:#05172d}}
 #nabilWholeLessonSmartLab .wl-panel{{background:#061725;border:1px solid #1a3b55;border-radius:13px;padding:11px;min-width:0}}
 #nabilWholeLessonSmartLab .wl-flow{{display:grid;gap:7px;margin-top:8px}}
 #nabilWholeLessonSmartLab .wl-row{{padding:8px 9px;border-inline-start:3px solid #2de1ff;background:#09243b;border-radius:8px;line-height:1.55}}
 #nabilWholeLessonSmartLab .wl-row b{{color:#65dfff}}
 #nabilWholeLessonSmartLab .wl-controls{{display:flex;gap:7px;flex-wrap:wrap;margin-top:9px}}
 #nabilWholeLessonSmartLab button{{min-height:44px;border:1px solid #426d8b;background:#153955;color:#fff;padding:8px 11px;border-radius:9px;font-weight:800}}
 #nabilWholeLessonSmartLab .wl-play{{background:#6047a8;border-color:#a98cff}}
 #nabilWholeLessonSmartLab .wl-stop{{background:#5a2330;border-color:#bd546b}}
 #nabilWholeLessonSmartLab .wl-timeline{{display:flex;gap:5px;flex-wrap:wrap;margin-top:9px}}
 #nabilWholeLessonSmartLab .wl-dot{{width:32px;height:32px;min-height:32px;border-radius:50%;padding:0;background:#071725;color:#9fb5c9;border:1px solid #31506b}}
 #nabilWholeLessonSmartLab .wl-dot.on{{background:#0b5d70;border-color:#2de1ff;color:#fff}}
 #nabilWholeLessonSmartLab .wl-dot.done{{background:#0d4c3c;border-color:#55e6a4;color:#fff}}
 @media(max-width:920px){{#nabilWholeLessonSmartLab .wl-layout{{grid-template-columns:1fr}}#nabilWholeLessonSmartLab iframe{{height:520px}}}}
 @media(max-width:430px){{#nabilWholeLessonSmartLab{{padding:7px}}#nabilWholeLessonSmartLab iframe{{height:66vh;min-height:430px}}#nabilWholeLessonSmartLab .wl-controls{{display:grid;grid-template-columns:1fr 1fr}}}}
 </style>
 <div class="wl-top"><div><h2 style="margin:0;color:#65dfff">{html.escape(labels["title"])}</h2><p style="margin:4px 0;color:#b9d7ea">{html.escape(labels["subtitle"])}</p></div>
 <div class="wl-teacher"><span class="wl-orb"></span><span>{html.escape(labels["teacher"])}</span></div></div>
 <div class="wl-layout"><div class="wl-stage"><iframe id="nabilWholeLessonFrame" title="{html.escape(labels["title"])}"></iframe></div>
 <aside class="wl-panel"><div style="font-size:11px;color:#9fb5c9">{html.escape(title)}</div><h3 id="nabilWholeLessonTitle" style="color:#ffd76b;margin:6px 0"></h3><div class="wl-flow" id="nabilWholeLessonFlow"></div></aside></div>
 <div class="wl-controls"><button id="nabilWholePrev">{html.escape(labels["prev"])}</button><button id="nabilWholeNext">{html.escape(labels["next"])}</button><button id="nabilWholeCurrent">{html.escape(labels["current"])}</button><button class="wl-play" id="nabilWholePlay">{html.escape(labels["all"])}</button><button class="wl-stop" id="nabilWholeStop">{html.escape(labels["stop"])}</button></div>
 <div class="wl-timeline" id="nabilWholeTimeline"></div>
 <script>
 (()=>{{
  const slides={payload};let idx=0,runToken=0,loadingToken=0;
  const frame=document.getElementById('nabilWholeLessonFrame'),titleEl=document.getElementById('nabilWholeLessonTitle'),flowEl=document.getElementById('nabilWholeLessonFlow'),timeline=document.getElementById('nabilWholeTimeline');
  function stop(){{runToken++;try{{window.NABILLessonE2E?.stopSpeech?.()}}catch(_e){{}}}}
  function buildTimeline(){{timeline.innerHTML='';slides.forEach((_,i)=>{{const b=document.createElement('button');b.className='wl-dot';b.textContent=i+1;b.onclick=()=>{{stop();idx=i;render()}};timeline.appendChild(b)}})}}
  function render(){{
    const s=slides[idx];titleEl.textContent=(idx+1)+'. '+s.title;flowEl.innerHTML='';
    s.flow.forEach(r=>{{
      const d=document.createElement('div');d.className='wl-row';
      const b=document.createElement('b');b.textContent=r.label+': ';
      const span=document.createElement('span');span.textContent=r.text;d.append(b,span);
      if(r.formula){{
        const f=document.createElement('div');f.textContent=r.formula;
        f.style.cssText='direction:ltr;text-align:center;margin-top:6px;padding:6px;border:1px dashed #315d79;border-radius:7px;font-family:Cambria Math,serif;color:#fff';
        d.appendChild(f);
      }}
      flowEl.appendChild(d);
    }});
    loadingToken++;frame.srcdoc=s.srcdoc;
    [...timeline.children].forEach((b,i)=>b.className='wl-dot '+(i<idx?'done':i===idx?'on':''));
  }}
  function teachCurrent(){{
    const my=++loadingToken;
    return new Promise(resolve=>{{
      let settled=false;
      const finish=()=>{{if(settled)return;settled=true;resolve()}};
      const launch=()=>{{
        if(my!==loadingToken){{finish();return}}
        try{{
          const doc=frame.contentDocument;
          const shell=doc?.querySelector('.nabil-reference-smart-lab');
          if(!shell){{finish();return}}
          const onComplete=()=>{{shell.removeEventListener('nabil:teacher-complete',onComplete);finish()}};
          shell.addEventListener('nabil:teacher-complete',onComplete,{{once:true}});
          shell.dispatchEvent(new CustomEvent('nabil:teach-all'));
        }}catch(_e){{finish()}}
      }};
      if(frame.contentDocument?.readyState==='complete')setTimeout(launch,120);
      else frame.onload=()=>setTimeout(launch,120);
    }});
  }}
  async function announceConcept(index){{
    const s=slides[index];
    const prefix=index===0?s.first_transition:s.next_transition;
    const message=(prefix+' '+s.title).trim();
    try{{await Promise.resolve(window.NABILLessonE2E?.speak?.(message,{json.dumps(lang_code)}));}}catch(_e){{}}
  }}
  async function playAll(){{
    stop();const token=runToken;idx=0;
    for(idx=0;idx<slides.length;idx++){{
      if(token!==runToken)return;
      render();
      await announceConcept(idx);
      if(token!==runToken)return;
      await teachCurrent();
      if(token!==runToken)return;
      [...timeline.children].forEach((b,i)=>b.className='wl-dot '+(i<=idx?'done':''));
      await new Promise(r=>setTimeout(r,220));
    }}
  }}
  document.getElementById('nabilWholePrev').onclick=()=>{{stop();idx=(idx+slides.length-1)%slides.length;render()}};
  document.getElementById('nabilWholeNext').onclick=()=>{{stop();idx=(idx+1)%slides.length;render()}};
  document.getElementById('nabilWholeCurrent').onclick=()=>{{stop();teachCurrent()}};
  document.getElementById('nabilWholePlay').onclick=playAll;
  document.getElementById('nabilWholeStop').onclick=()=>{{
    stop();
    try{{frame.contentDocument?.querySelector('.nabil-reference-smart-lab')?.dispatchEvent(new CustomEvent('nabil:teach-stop'))}}catch(_e){{}}
  }};
  window.NABILWholeLessonOrchestrator={{
    play:playAll,
    stop:()=>document.getElementById('nabilWholeStop')?.click(),
    current:()=>teachCurrent(),
    goTo:(i)=>{{stop();idx=Math.max(0,Math.min(slides.length-1,Number(i)||0));render();}}
  }};
  buildTimeline();render();
 }})();
 </script>
</section>'''


def synthesize_universal_pedagogy(entry: dict, ev_map: dict, profile: dict) -> dict:
    title = entry["canonical_title"]
    concepts = ev_map["concepts"]

    activities_theory = []
    worksheet = []
    panels = ""
    lesson_lang_code = resolve_lang_code(profile["language"])

    for idx, c in enumerate(concepts, 1):
        p_num = c["source_page"]
        # Textbook figures are EVIDENCE ONLY. Their pixels are never placed in
        # the student lesson. NABIL may inspect them to build an independently
        # audited redraw or interactive lab.
        fig_images = []
        for p in ev_map["pages_evidence"]:
            if p["page_num"] == p_num and p["figures"]:
                for f in p["figures"]:
                    if f["figure_id"] in c.get("figure_refs", []):
                        fig_images.append(f["image_path"])
        # Multiple source figures (e.g. 3a/3b) must be read together.
        figure_image_base64 = None
        if fig_images:
            from PIL import Image, ImageOps
            pictures = []
            for filename in fig_images:
                with Image.open(filename) as image:
                    pic = image.convert("RGB")
                    pic.thumbnail((1100, 850))
                    pictures.append(pic.copy())
            canvas = Image.new("RGB", (max(im.width for im in pictures),
                                       sum(im.height for im in pictures) + 8*(len(pictures)-1)), "white")
            top = 0
            for pic in pictures:
                canvas.paste(pic, (0, top))
                top += pic.height + 8
            buffered = io.BytesIO()
            canvas.save(buffered, format="PNG")
            figure_image_base64 = base64.b64encode(buffered.getvalue()).decode("ascii")
        vision_context = ({
            "lesson_id": entry["lesson_id"],
            "book_id": entry["book_id"],
            "pdf_page": p_num,
        } if figure_image_base64 else None)
        narrative = synthesize_concept_narrative(
            c, profile, figure_image_base64,
            vision_context=vision_context)

        try:
            lab_spec = build_verified_lab_spec(
                entry, c, narrative, profile,
                figure_image_base64=figure_image_base64,
                vision_context=vision_context)
        except RuntimeError as exc:
            reason = str(exc)
            if not reason.startswith("LAB_"):
                raise
            progress(
                "LAB_PIPELINE_BLOCKED",
                concept_id=c.get("concept_id"),
                source_page=p_num,
                reason=reason[:240],
            )
            # Technical/specification failures are not equivalent to "this
            # concept has no lab". Fail closed so an applicable animated lab
            # can never disappear silently and still be published.
            raise RuntimeError(
                f"LAB_PIPELINE_FAILED:{c.get('concept_id')}:{reason}") from exc
        concept_lab_html, concept_has_sim = render_verified_lab(
            lab_spec, lesson_lang_code, c["concept_id"])

        concept_visual = None
        if not concept_has_sim:
            concept_visual = build_nabil_explanatory_redrawing(
                source_text=c.get("raw_text", ""),
                page_num=p_num,
                figure_paths=fig_images,
                vision_context=vision_context,
                purpose=f"concept_{c['concept_id']}",
                visual_required=bool(c.get("figure_refs")),
            )
        if c.get("figure_refs") and not concept_has_sim and not concept_visual:
            raise RuntimeError(
                f"NABIL_VISUAL_REQUIRED_BUT_NOT_VERIFIED:{c['concept_id']}:p{p_num}"
            )
        concept_visual_html = ""
        if concept_visual:
            caption = {
                "ar": "رسم NABIL التوضيحي المبني على الدليل",
                "fr": "Schéma explicatif NABIL fondé sur les preuves",
                "en": "NABIL explanatory visual built from verified evidence",
            }.get(lesson_lang_code, "NABIL explanatory visual built from verified evidence")
            concept_visual_html = (
                '<div class="nabil-explanatory-visual" style="margin:14px 0;">'
                + str(concept_visual["svg"])
                + '<div style="font-size:11px;color:#64748b;margin-top:5px;">'
                + html.escape(caption) + '</div></div>'
            )

        question_ready = all(
            str(narrative.get(k) or "").strip()
            for k in ("conclusion", "distractor_1", "distractor_2")
        )
        student_question = None
        if question_ready:
            student_question = {
                "q": ui_t(
                    lesson_lang_code, "based_on_verified_findings",
                    title=c["title"]),
                "options": [
                    narrative["conclusion"],
                    narrative["distractor_1"],
                    narrative["distractor_2"],
                ],
                "correct_index": 0,
                "feedback": ui_t(lesson_lang_code, "grounded_feedback"),
            }
        else:
            progress(
                "SKIPPED_UNVERIFIED_QUIZ_ITEM",
                concept_id=c.get("concept_id"),
                source_page=p_num,
                reason="GENERATED_QUIZ_CONTENT_REMOVED_BY_SCOPE_AUDIT",
            )

        activities_theory.append({
            "activity_num": c["concept_id"].replace("C", ""),
            "concept_id": c["concept_id"],
            "title": c["title"],
            "source_page": p_num,
            "source_excerpt": c.get("raw_text", ""),
            "phenomenon": narrative.get("phenomenon", ""),
            "investigation": narrative.get("investigation", ""),
            "observation": narrative.get("observation", ""),
            "interpretation": narrative.get("interpretation", ""),
            "conclusion": narrative.get("conclusion", ""),
            "visual_html": concept_visual_html,
            "visual_method": (
                concept_visual.get("method") if concept_visual else
                ("INTERACTIVE_LAB" if concept_has_sim else None)
            ),
            "source_figure_used_as_hidden_evidence": bool(fig_images),
            "lab_spec": lab_spec,
            "lab_html": concept_lab_html,
            "has_active_sim": concept_has_sim,
            "student_question": student_question,
            "generated_content_scope_audited": narrative.get("_scope_audited", False),
            "removed_generated_fields": narrative.get("_removed_generated_fields", []),
            "formal_arabic_verified": (
                narrative.get("_formal_arabic_verified", False)
                if lesson_lang_code == "ar" else True
            ),
            "teaching_signature": resolve_teaching_signature(c, profile),
            "teaching_steps": build_teaching_steps(
                c, narrative, profile, lab_spec=lab_spec),
        })

        if question_ready:
            worksheet.append({
                "id": len(worksheet) + 1,
                "concept_id": c["concept_id"],
                "source_page": p_num,
                "source_hash": c["sha256"],
                "evidence_ref": c["concept_id"],
                "question": ui_t(
                    lesson_lang_code, "confirmed_deduction_question",
                    title=c["title"]),
                "options": [
                    narrative["conclusion"],
                    narrative["distractor_1"],
                    narrative["distractor_2"],
                ],
                "correct_index": 0,
                "explanation": ui_t(
                    lesson_lang_code, "grounded_explanation",
                    page=p_num, ref=c["concept_id"]),
            })

        formula_label = html.escape(ui_t(lesson_lang_code, "formula_law"))
        units_label = html.escape(ui_t(lesson_lang_code, "units_label"))
        formulas_html = "".join([f"<li><b>{formula_label}:</b> {html.escape(f)}</li>" for f in narrative.get("formulas", [])])
        units_html = "".join([f"<li><b>{units_label}:</b> {html.escape(u)}</li>" for u in narrative.get("units", [])])
        subject_metadata = f"<ul style='margin:4px 0 0 16px; padding:0; font-size:12px; color:#0369a1;'>{formulas_html}{units_html}</ul>" if (narrative.get("formulas") or narrative.get("units")) else ""

        principle_html = ""
        if str(narrative.get("conclusion") or "").strip():
            principle_html = (
                '<div style="margin-top:8px; font-size:13px; color:#334155; '
                'line-height:1.5;"><b>'
                + html.escape(ui_t(lesson_lang_code, "extracted_principle"))
                + ':</b> ' + html.escape(str(narrative["conclusion"])) + '</div>'
            )
        panels += f'''<div class="nabil-reference-concept" data-reference-concept="{html.escape(str(c["concept_id"]))}" style="background:#ffffff; border:1px solid #cbd5e1; border-radius:10px; padding:14px; box-shadow:0 2px 4px rgba(0,0,0,0.04);">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #e2e8f0; padding-bottom:6px;">
                <span style="font-weight:700; color:#0369a1; font-size:15px;">{html.escape(c["title"])}</span>
            </div>
            {principle_html}
            {subject_metadata}
            {concept_visual_html}
            <div style="margin-top:8px; font-size:12px; color:#059669; font-weight:600;">{html.escape(ui_t(lesson_lang_code, "verified_evidence_grounding"))}</div>
        </div>'''

    final_labels = {
        "ar":{"analysis":"📘 خلاصة الأفكار","visual":"📈 الرسوم والتمثيل","final":"✅ البطاقة النهائية","verify":"التحقق","badge":"ملخص الدرس","read":"🔊 قراءة البطاقة","stop":"⏹ إيقاف الصوت","enlarge":"🔎 تكبير"},
        "fr":{"analysis":"📘 Synthèse des idées","visual":"📈 Visuels","final":"✅ Carte finale","verify":"Vérification","badge":"Résumé de la leçon","read":"🔊 Lire la carte","stop":"⏹ Arrêter","enlarge":"🔎 Agrandir"},
        "en":{"analysis":"📘 Concept Summary","visual":"📈 Visuals","final":"✅ Final Card","verify":"Verification","badge":"Lesson Summary","read":"🔊 Read card","stop":"⏹ Stop voice","enlarge":"🔎 Enlarge"},
    }.get(lesson_lang_code,{})
    final_results=[str(x.get("conclusion") or "").strip() for x in activities_theory if str(x.get("conclusion") or "").strip()]
    final_chips="".join('<span class="nabil-sci-chip">'+html.escape(v)+'</span>' for v in final_results)
    final_analysis="".join(
        '<div class="nabil-sci-section"><div class="nabil-sci-label">'+html.escape(str(x.get("title") or ""))+
        '</div><div class="nabil-sci-value">'+html.escape(str(x.get("conclusion") or x.get("observation") or ""))+'</div></div>'
        for x in activities_theory
    )
    final_visuals="".join(
        '<div class="nabil-reference-concept" data-reference-concept="'+html.escape(str(x.get("concept_id") or ""))+'">'+
        '<div class="nabil-sci-label">'+html.escape(str(x.get("title") or ""))+'</div>'+str(x.get("visual_html") or "")+'</div>'
        for x in activities_theory
    )
    final_verify="".join('<li>'+html.escape(str(x.get("title") or ""))+': '+html.escape(ui_t(lesson_lang_code,"verified_evidence_grounding"))+'</li>' for x in activities_theory)
    teacher_note={"ar":"راجع كل فكرة بالترتيب: شاهد، جرّب، لاحظ، فكّر، استنتج، ثم طبّق.","fr":"Revois chaque idée : observe, essaie, remarque, réfléchis, conclus puis applique.","en":"Review each idea: See, Try, Notice, Think, Conclude, then Apply."}.get(lesson_lang_code,"Review each idea.")
    final_speech=" ".join([str(title)]+[str(x.get("title") or "")+". "+str(x.get("conclusion") or "") for x in activities_theory])

    ref_card_html = f'''
    <section id="goldenReferenceCard" class="nabil-sci-card lesson-final-card">
      <div class="nabil-sci-top">
        <div><div class="nabil-sci-brand">NABIL AI | منصة نبيل التعليمية الذكية</div><h2 class="nabil-sci-title">{html.escape(title)}</h2></div>
        <div class="nabil-sci-badge">{html.escape(final_labels.get("badge","Lesson Summary"))}</div>
      </div>
      <div class="nabil-sci-grid">
        <div class="nabil-sci-panel nabil-sci-analysis"><h3>{html.escape(final_labels.get("analysis","📘 Concept Summary"))}</h3>{final_analysis}</div>
        <div class="nabil-sci-panel nabil-sci-visual"><h3>{html.escape(final_labels.get("visual","📈 Visuals"))}</h3><div class="nabil-sci-visual-stage">{final_visuals}</div></div>
        <div class="nabil-sci-panel nabil-sci-teacher-panel"><div class="nabil-sci-teacher">
          <img class="nabil-sci-avatar" src="/static/nabil-profile.jpg" alt="NABIL AI" onerror="this.style.display='none'">
          <div><strong>NABIL AI</strong><p>{html.escape(teacher_note)}</p></div>
        </div></div>
      </div>
      <div class="nabil-sci-final">
        <h3>{html.escape(final_labels.get("final","✅ Final Card"))}</h3>
        <div class="nabil-sci-results">{final_chips}</div>
        <div class="nabil-sci-verify"><b>{html.escape(final_labels.get("verify","Verification"))}:</b><ul class="nabil-sci-list">{final_verify}</ul></div>
        <div class="nabil-sci-tools">
          <button type="button" onclick="document.querySelector('#goldenReferenceCard .nabil-sci-visual-stage')?.requestFullscreen?.()">{html.escape(final_labels.get("enlarge","🔎 Enlarge"))}</button>
          <button type="button" onclick="nabilReadFinalCard()">{html.escape(final_labels.get("read","🔊 Read card"))}</button>
          <button type="button" onclick="nabilStopFinalCard()">{html.escape(final_labels.get("stop","⏹ Stop voice"))}</button>
        </div>
      </div>
      <script type="application/json" id="nabilFinalCardSpeech">{html.escape(json.dumps({"text":final_speech,"lang":lesson_lang_code},ensure_ascii=False))}</script>
    </section>'''


    # Aggregate labs across all concepts that actually produced one.
    all_labs_html = [
        act["lab_html"] for act in activities_theory if act.get("has_active_sim")
    ]
    any_active_sim = bool(all_labs_html)

    whole_lesson_lab_html = render_whole_lesson_smart_lab(
        title, activities_theory, lesson_lang_code)

    # Full-coverage quiz: reuses the exact grounded conclusion/distractor
    # fields already produced per concept above — no new LLM calls, no new
    # invented content, same evidence guarantee as the worksheet.
    full_quiz_items = build_full_quiz_items(activities_theory)
    full_quiz_html = render_quiz_html(full_quiz_items, lesson_lang_code)

    return {
        "title": title,
        "activities": activities_theory,
        "lab_html": "\n".join(all_labs_html),
        "has_active_sim": any_active_sim,
        "worksheet": worksheet,
        "quiz_items": full_quiz_items,
        "quiz_html": full_quiz_html,
        "quiz_eligible_count": sum(
            1 for act in activities_theory if act.get("student_question")),
        "reference_card_html": ref_card_html,
        "whole_lesson_lab_html": whole_lesson_lab_html,
        "whole_lesson_lab_active": bool(whole_lesson_lab_html),
    }



# ==============================================================================
# PREBUILT FULL-PAGE AR / EN / FR TRANSLATION
# ==============================================================================
def _looks_like_formula_only(value: str) -> bool:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    if not text:
        return True
    letters = re.findall(r"[A-Za-zÀ-ÿ\u0600-\u06ff]", text)
    operators = re.findall(r"[=+\-×÷*/^∠⊥≅≤≥<>√∞]", text)
    # Mathematical labels/formulas stay canonical and are never sent through
    # translation. This protects point labels, equations and symbolic results.
    return bool(operators) and len(letters) <= max(5, len(text) // 5)


def _is_translatable_display_string(value: str) -> bool:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    if len(text) < 2 or len(text) > 1200:
        return False
    if _looks_like_formula_only(text):
        return False
    if "://" in text or text.startswith(("#", ".", "/", "{", "}", "[", "]")):
        return False
    if re.search(r"</?[A-Za-z][^>]*>", text):
        return False
    if re.fullmatch(r"[A-Za-z0-9_.:/#-]+", text):
        # Keep human one-word labels, reject ids/paths/camelCase/code tokens.
        if any(ch in text for ch in "_./:#") or re.search(r"[a-z][A-Z]", text):
            return False
        if "-" in text and text.lower() not in {"step-by-step"}:
            return False
    if not re.search(r"[A-Za-zÀ-ÿ\u0600-\u06ff]", text):
        return False
    return True


def _extract_translation_candidates(markup: str) -> List[str]:
    """Collect static/dynamic display strings using Python stdlib only."""
    from html.parser import HTMLParser

    ordered: List[str] = []
    seen = set()
    script_chunks: List[str] = []

    def add(value):
        text = re.sub(r"\s+", " ", str(value or "")).strip()
        if text and text not in seen and _is_translatable_display_string(text):
            seen.add(text)
            ordered.append(text)

    class Collector(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.skip_depth = 0
            self.in_script = False

        def handle_starttag(self, tag, attrs):
            lower = tag.lower()
            if lower == "script":
                self.in_script = True
                return
            if lower in {"style", "noscript"}:
                self.skip_depth += 1
                return
            if self.skip_depth == 0:
                amap = dict(attrs)
                for attr in ("title", "placeholder", "aria-label"):
                    add(amap.get(attr))

        def handle_endtag(self, tag):
            lower = tag.lower()
            if lower == "script":
                self.in_script = False
            elif lower in {"style", "noscript"} and self.skip_depth:
                self.skip_depth -= 1

        def handle_data(self, data):
            if self.in_script:
                script_chunks.append(data)
            elif self.skip_depth == 0:
                add(data)

    parser = Collector()
    parser.feed(markup)
    parser.close()

    # Labs/whole-lesson/proof engines keep some display strings in JS data and
    # reveal them later. Include human-readable literals so the runtime
    # MutationObserver translates those dynamic updates too.
    source = "\n".join(script_chunks)
    for match in re.finditer(r'"((?:\\.|[^"\\])*)"', source):
        raw = match.group(1)
        try:
            value = json.loads('"' + raw + '"')
        except Exception:
            value = raw.replace('\\"', '"').replace("\\n", " ")
        add(value)
    for match in re.finditer(r"'((?:\\.|[^'\\])*)'", source):
        raw = match.group(1)
        if "\\" in raw and not re.search(r"\\[nrt'\\]", raw):
            continue
        add(raw.replace("\\'", "'").replace("\\n", " "))
    return ordered

def _translation_integrity_tokens(value: str) -> Tuple[List[str], List[str]]:
    text = str(value or "")
    numbers = re.findall(r"(?<![\w])[-+]?\d+(?:[.,]\d+)?(?:%|°)?", text)
    protected = re.findall(
        r"(?:[A-Z][A-Za-z]?\d{0,3}|[A-Z]{1,4}\d*|"
        r"[A-Za-z]\d*[₀₁₂₃₄₅₆₇₈₉]*|"
        r"Ω|V|A|mA|kΩ|kg|g|m|cm|mm|s|ms|mol|Pa|N|J|W|Hz)"
        r"(?=\b|[^A-Za-zÀ-ÿ])",
        text,
    )
    return numbers, protected


def _translate_strings_batch(
        strings: List[str], source_lang: str, target_lang: str,
        purpose: str) -> Dict[str, str]:
    if target_lang == source_lang:
        return {value: value for value in strings}
    if not strings:
        return {}
    target_name = {"ar": "Modern Standard Arabic", "en": "English",
                   "fr": "French"}[target_lang]
    source_name = {"ar": "Modern Standard Arabic", "en": "English",
                   "fr": "French"}.get(source_lang, source_lang)
    output: Dict[str, str] = {}
    batch_size = 55
    for start in range(0, len(strings), batch_size):
        batch = strings[start:start + batch_size]
        items = [{"id": str(start + i), "text": value}
                 for i, value in enumerate(batch)]
        prompt = (
            "You are a strict translation-only engine for a school lesson. "
            f"Translate each item from {source_name} to {target_name}. "
            "Do not add, omit, explain, simplify or correct scientific content. "
            "Preserve every number exactly as written. Preserve mathematical "
            "expressions, point/segment labels, variable names, chemical formulas, "
            "units and standard symbols exactly. Keep NABIL as NABIL. "
            "Use clear school-level Modern Standard Arabic when target is Arabic. "
            "Return strict JSON exactly as {\"items\":[{\"id\":\"...\",\"text\":\"...\"}]}. "
            "The item count and ids must match.\nITEMS:\n" +
            json.dumps(items, ensure_ascii=False)
        )
        result = _execute_llm_json_strict(
            prompt,
            purpose=f"{purpose}_{target_lang}_{start}",
            max_attempts=3,
        )
        translated = result.get("items") if isinstance(result, dict) else None
        if not isinstance(translated, list) or len(translated) != len(items):
            raise RuntimeError(
                f"PAGE_TRANSLATION_SCHEMA_INVALID:{target_lang}:{start}")
        by_id = {
            str(row.get("id")): str(row.get("text") or "").strip()
            for row in translated if isinstance(row, dict)
        }
        for item in items:
            source = item["text"]
            value = by_id.get(item["id"], "")
            if not value:
                raise RuntimeError(
                    f"PAGE_TRANSLATION_EMPTY:{target_lang}:{item['id']}")
            src_numbers, src_protected = _translation_integrity_tokens(source)
            dst_numbers, dst_protected = _translation_integrity_tokens(value)
            if src_numbers != dst_numbers:
                raise RuntimeError(
                    f"PAGE_TRANSLATION_NUMBER_CHANGED:{target_lang}:{item['id']}")
            # Protected token order may contain ordinary one-letter words in
            # prose. Enforce exact preservation only when the source looks
            # mathematical/scientific enough to make those tokens meaningful.
            if (
                re.search(r"[=+\-×÷*/^∠⊥≅Ω₀₁₂₃₄₅₆₇₈₉]", source)
                and src_protected != dst_protected
            ):
                raise RuntimeError(
                    f"PAGE_TRANSLATION_SYMBOL_CHANGED:{target_lang}:{item['id']}")
            if target_lang == "ar":
                _assert_formal_arabic_text(
                    value, purpose=f"{purpose}_ar_{item['id']}")
            output[source] = value
    return output


def build_trilingual_page_translation(
        markup: str, source_lang_code: str, purpose: str
        ) -> Tuple[str, Dict[str, Any]]:
    source_lang = (
        source_lang_code if source_lang_code in REFERENCE_RENDERER_LANGUAGES
        else "en"
    )
    candidates = _extract_translation_candidates(markup)
    bundles = {source_lang: {value: value for value in candidates}}
    for target in REFERENCE_RENDERER_LANGUAGES:
        if target == source_lang:
            continue
        bundles[target] = _translate_strings_batch(
            candidates, source_lang, target, purpose)
    if any(len(bundles.get(lang, {})) != len(candidates)
           for lang in REFERENCE_RENDERER_LANGUAGES):
        raise RuntimeError("FULL_PAGE_TRANSLATION_COVERAGE_INCOMPLETE")

    payload = json.dumps(
        {
            "source": source_lang,
            "languages": list(REFERENCE_RENDERER_LANGUAGES),
            "strings": bundles,
        },
        ensure_ascii=False, separators=(",", ":"),
    ).replace("</", "<\\/")

    language_bar = r'''
<div id="nabilPageLanguage" data-nabil-page-language="true"
 style="position:sticky;top:4px;z-index:2147482000;display:flex;gap:6px;
 align-items:center;justify-content:center;flex-wrap:wrap;margin:0 auto 8px;
 width:max-content;max-width:100%;background:#061725;border:1px solid #2b6485;
 border-radius:13px;padding:6px 8px;box-shadow:0 7px 22px #0007;direction:ltr">
 <span aria-hidden="true">🌐</span>
 <button type="button" data-nabil-lang="ar" style="min-height:40px">العربية</button>
 <button type="button" data-nabil-lang="en" style="min-height:40px">English</button>
 <button type="button" data-nabil-lang="fr" style="min-height:40px">Français</button>
</div>
'''
    runtime = r'''
<script id="nabilPageTranslationRuntime">
(()=>{
"use strict";
const data=JSON.parse(document.getElementById("nabilPageTranslationBundle").textContent);
const source=data.source,strings=data.strings||{},langs=data.languages||["ar","en","fr"];
const originals=new WeakMap();
const reverse={};
langs.forEach(lang=>{reverse[lang]=new Map(Object.entries(strings[lang]||{}).map(([a,b])=>[String(b),a]))});
function trimmedParts(v){const m=String(v||"").match(/^(\s*)([\s\S]*?)(\s*)$/);return m||["","","",""]}
function baseFor(value){
 const t=String(value||"").trim();if(!t)return "";
 if((strings[source]||{})[t]!==undefined)return t;
 for(const lang of langs){const hit=reverse[lang]?.get(t);if(hit!==undefined)return hit}
 return t;
}
function translateNode(node,lang){
 if(!node||node.nodeType!==Node.TEXT_NODE)return;
 const p=node.parentElement;if(!p||["SCRIPT","STYLE","NOSCRIPT"].includes(p.tagName))return;
 const parts=trimmedParts(node.nodeValue),current=parts[2];if(!current)return;
 let base=originals.get(node);
 const inferred=baseFor(current);
 if(!base||(strings[source]||{})[inferred]!==undefined&&current!==((strings[lang]||{})[base]||base)){
   base=inferred;originals.set(node,base);
 }
 const out=(strings[lang]||{})[base];
 if(out!==undefined&&current!==out)node.nodeValue=parts[1]+out+parts[3];
}
function translateAttrs(root,lang){
 (root.querySelectorAll?.("[title],[placeholder],[aria-label]")||[]).forEach(el=>{
  ["title","placeholder","aria-label"].forEach(attr=>{
   if(!el.hasAttribute(attr))return;
   const key="__nabilBase_"+attr.replace("-","_");
   let base=el.dataset[key]||baseFor(el.getAttribute(attr));
   el.dataset[key]=base;
   const out=(strings[lang]||{})[base];if(out!==undefined)el.setAttribute(attr,out);
  })
 })
}
const frameObservers=new WeakMap();
function translateRoot(root,lang){
 if(!root)return;
 const walker=(root.ownerDocument||document).createTreeWalker(root,NodeFilter.SHOW_TEXT);
 const nodes=[];while(walker.nextNode())nodes.push(walker.currentNode);
 nodes.forEach(n=>translateNode(n,lang));translateAttrs(root,lang);
}
function watchFrame(frame){
 try{
  const doc=frame.contentDocument;if(!doc?.body)return;
  translateRoot(doc.body,current);
  if(frameObservers.has(frame))frameObservers.get(frame).disconnect();
  const obs=new MutationObserver(records=>{
   if(applying)return;applying=true;
   for(const rec of records){
    if(rec.type==="characterData")translateNode(rec.target,current);
    for(const added of rec.addedNodes||[]){
     if(added.nodeType===Node.TEXT_NODE)translateNode(added,current);
     else if(added.nodeType===Node.ELEMENT_NODE)translateRoot(added,current);
    }
   }
   applying=false;
  });
  obs.observe(doc.body,{subtree:true,childList:true,characterData:true});
  frameObservers.set(frame,obs);
 }catch(_e){}
}
function translateFrames(lang){
 document.querySelectorAll("iframe").forEach(frame=>{
  try{watchFrame(frame)}catch(_e){}
  if(!frame.dataset.nabilTranslationWatch){
   frame.dataset.nabilTranslationWatch="1";
   frame.addEventListener("load",()=>watchFrame(frame));
  }
 })
}
let applying=false,current=source;
function apply(lang){
 if(!langs.includes(lang))lang=source;
 applying=true;current=lang;
 document.documentElement.lang=lang;
 document.documentElement.dir=lang==="ar"?"rtl":"ltr";
 translateRoot(document.body,lang);translateFrames(lang);
 document.querySelectorAll("#nabilPageLanguage [data-nabil-lang]").forEach(b=>{
  const on=b.dataset.nabilLang===lang;b.setAttribute("aria-pressed",String(on));
  b.style.background=on?"#0b84bd":"#153955";b.style.borderColor=on?"#7af3ff":"#426d8b";
 });
 try{localStorage.setItem("nabil.lesson.page.language",lang)}catch(_e){}
 applying=false;
 window.dispatchEvent(new CustomEvent("nabil:page-language-change",{detail:{language:lang}}));
}
document.getElementById("nabilPageLanguage")?.addEventListener("click",e=>{
 const b=e.target.closest("[data-nabil-lang]");if(b)apply(b.dataset.nabilLang)
});
const observer=new MutationObserver(records=>{
 if(applying)return;applying=true;
 for(const rec of records){
  if(rec.type==="characterData")translateNode(rec.target,current);
  for(const added of rec.addedNodes||[]){
   if(added.nodeType===Node.TEXT_NODE)translateNode(added,current);
   else if(added.nodeType===Node.ELEMENT_NODE){
    translateRoot(added,current);
    if(added.tagName==="IFRAME")watchFrame(added);
    else added.querySelectorAll?.("iframe").forEach(watchFrame);
   }
  }
 }
 applying=false;
});
observer.observe(document.body,{subtree:true,childList:true,characterData:true});
let initial=source;try{const saved=localStorage.getItem("nabil.lesson.page.language");if(langs.includes(saved))initial=saved}catch(_e){}
apply(initial);
window.NABILPageLanguage={
 apply,get:()=>current,source,
 translateText:(value,lang=current)=>{
  const raw=String(value||""),base=baseFor(raw.trim());
  const out=(strings[lang]||{})[base];
  return out===undefined?raw:out;
 }
};
})();
</script>
'''
    bundle_script = (
        '<script id="nabilPageTranslationBundle" type="application/json">'
        + payload + '</script>'
    )
    if "<body" not in markup.lower():
        raise RuntimeError("FULL_PAGE_TRANSLATION_BODY_MISSING")
    markup = re.sub(
        r"(<body[^>]*>)",
        lambda m: (
            m.group(1)
            + '\n<div data-nabil-translation-complete="true" hidden></div>\n'
            + language_bar + bundle_script
        ),
        markup, count=1, flags=re.I,
    )
    markup = re.sub(
        r"</body>", lambda m: runtime + "\n" + m.group(0),
        markup, count=1, flags=re.I,
    )
    report = {
        "source_language": source_lang,
        "languages": list(REFERENCE_RENDERER_LANGUAGES),
        "candidate_strings": len(candidates),
        "translated_counts": {
            lang: len(bundles.get(lang, {}))
            for lang in REFERENCE_RENDERER_LANGUAGES
        },
        "complete": True,
    }
    return markup, report


# ==============================================================================
# 9. TWIN-PAGE HTML COMPILATION
# ==============================================================================
def render_lesson_page_a(entry: dict, theory: dict, ev_map: dict, lab_index: Optional[dict] = None) -> str:
    clean_title = html.escape(re.sub(r'^\s*\d{2,3}\s*(?:--|[-_ ]+)\s*', '', entry["canonical_title"]))
    clean_title = html.escape(re.sub(r'\s+\d{2,3}$', '', clean_title).strip())
    lang = entry.get("language", "en")
    page_a_lang_code = resolve_lang_code(lang)

    acts_html = ""
    for act in theory["activities"]:
        q = act.get("student_question")
        question_html = ""
        if q:
            opts = "".join([
                f'<button onclick="gradeStep(this, {i == q["correct_index"]}, '
                f'\'{html.escape(q["feedback"])}\')" class="q-opt">'
                f'{html.escape(o)}</button>'
                for i, o in enumerate(q["options"])
            ])
            question_html = f'''
          <div style="background:#f1f5f9; padding:12px; border-radius:6px; margin-top:12px;">
            <div style="font-weight:600; font-size:14px; margin-bottom:8px;">{ui_t(page_a_lang_code, "check_understanding")}: {html.escape(q["q"])}</div>
            <div style="display:flex; gap:8px; flex-wrap:wrap;">{opts}</div>
            <div class="step-fb" style="margin-top:8px; font-size:13px; font-weight:600; display:none;"></div>
          </div>'''
        flow_labels = {
            "ar": {
                "phenomenon": "👀 شوف",
                "investigation": "🖐️ جرّب",
                "observation": "🔎 لاحظ",
                "interpretation": "💡 فكّر",
                "conclusion": "✅ استنتج",
            },
            "fr": {
                "phenomenon": "👀 Observe",
                "investigation": "🖐️ Essaie",
                "observation": "🔎 Remarque",
                "interpretation": "💡 Réfléchis",
                "conclusion": "✅ Conclus",
            },
            "en": {
                "phenomenon": "👀 See",
                "investigation": "🖐️ Try",
                "observation": "🔎 Notice",
                "interpretation": "💡 Think",
                "conclusion": "✅ Conclude",
            },
        }.get(page_a_lang_code, {})
        generated_rows = []
        for field in (
            "phenomenon",
            "investigation",
            "observation",
            "interpretation",
            "conclusion",
        ):
            value = str(act.get(field) or "").strip()
            if value:
                label = flow_labels.get(field, field.title())
                generated_rows.append(
                    '<div class="nabil-flow-row ' + ('nabil-conclude' if field == 'conclusion' else '') + '" data-step="' + html.escape(field) + '">'
                    '<b>' + html.escape(label) + ':</b> ' + html.escape(value) + '</div>'
                )
        apply_text = str(act.get("student_question") or "").strip()
        if apply_text:
            apply_label = {"ar":"✍️ طبّق","fr":"✍️ Applique","en":"✍️ Apply"}.get(page_a_lang_code,"✍️ Apply")
            generated_rows.append(
                '<div class="nabil-flow-row nabil-apply" data-step="application"><b>'
                + html.escape(apply_label) + ':</b> ' + html.escape(apply_text) + '</div>'
            )
        generated_html = "".join(generated_rows)
        concept_badge = {"ar":"بطاقة فكرة","fr":"Carte concept","en":"Concept Card"}.get(page_a_lang_code,"Concept Card")
        analysis_label = {"ar":"📘 الشرح","fr":"📘 Explication","en":"📘 Explanation"}.get(page_a_lang_code,"📘 Explanation")
        visual_label = {"ar":"🧪 الرسم والمختبر","fr":"🧪 Visuel et laboratoire","en":"🧪 Visual & Lab"}.get(page_a_lang_code,"🧪 Visual & Lab")
        teacher_note = {"ar":"شاهد، جرّب، لاحظ، فكّر، استنتج، ثم طبّق.","fr":"Observe, essaie, remarque, réfléchis, conclus puis applique.","en":"See, Try, Notice, Think, Conclude, then Apply."}.get(page_a_lang_code,"See, Try, Notice, Think, Conclude, then Apply.")
        acts_html += f"""
        <section class="nabil-sci-card nabil-concept-card" data-nabil-concept-id="{html.escape(str(act["concept_id"]))}">
          <div class="nabil-sci-top">
            <div><div class="nabil-sci-brand">NABIL AI | منصة نبيل التعليمية الذكية</div>
            <h2 class="nabil-sci-title">{act["activity_num"]}. {html.escape(act["title"])}</h2></div>
            <div class="nabil-sci-badge">{html.escape(concept_badge)}</div>
          </div>
          <div class="nabil-sci-grid">
            <div class="nabil-sci-panel nabil-sci-analysis"><h3>{html.escape(analysis_label)}</h3>{generated_html}</div>
            <div class="nabil-sci-panel nabil-sci-visual"><h3>{html.escape(visual_label)}</h3>
              <div class="nabil-sci-visual-stage">{act["visual_html"]}{act.get("lab_html","")}</div>
            </div>
            <div class="nabil-sci-panel nabil-sci-teacher-panel"><div class="nabil-sci-teacher">
              <img class="nabil-sci-avatar" src="/static/nabil-profile.jpg" alt="NABIL AI" onerror="this.style.display='none'">
              <div><strong>NABIL AI</strong><p>{html.escape(teacher_note)}</p></div>
            </div></div>
          </div>
          <div class="nabil-sci-final"><h3>{html.escape({"ar":"✍️ طبّق وتحقق","fr":"✍️ Applique et vérifie","en":"✍️ Apply & Check"}.get(page_a_lang_code,"✍️ Apply & Check"))}</h3>{question_html}</div>
        </section>"""


    ws_items = ""
    for idx, item in enumerate(theory["worksheet"]):
        opts = "".join([f'<button onclick="gradeWs(this, {i == item["correct_index"]}, \'{html.escape(item["explanation"])}\')" class="q-opt">{html.escape(o)}</button>' for i, o in enumerate(item["options"])])
        ws_items += f'''
        <div class="ws-item" style="margin-bottom:14px; padding:12px; background:#fff; border:1px solid #e2e8f0; border-radius:6px;">
          <div style="font-weight:600; margin-bottom:6px;">{html.escape(ui_t(page_a_lang_code, "question_label"))} {idx+1}: {html.escape(item["question"])}</div>
          <div style="display:flex; gap:8px; flex-wrap:wrap;">{opts}</div>
          <div class="ws-fb" style="margin-top:6px; font-size:12px; font-weight:600; display:none;"></div>
        </div>'''

    return f'''<!DOCTYPE html>
<html lang="{html.escape(lang)}" dir="{html_dir_attr(page_a_lang_code)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="nabil-lesson-id" content="{html.escape(entry['lesson_id'])}">
<meta name="nabil-canonical-title" content="{clean_title}">
<meta name="nabil-grade" content="{entry.get('grade', 7)}">
<meta name="nabil-subject" content="{html.escape(entry.get('subject', 'Physics'))}">
<meta name="nabil-source-book-id" content="{html.escape(entry['book_id'])}">
<meta name="nabil-source-pages" content="{entry['pdf_start_page']}-{entry['pdf_end_page']}">
<meta name="nabil-renderer-contract" content="{REFERENCE_RENDERER_CONTRACT}">
<meta name="nabil-translation-languages" content="ar,en,fr">
<title>{clean_title} - NABIL Universal Engine</title>
{MathRenderingEngine.inject_mathjax_head()}
<script defer src="/static/nabil_browser_tts_v1.js?v=1"></script>\n<script defer src="/static/nabil_lab_voice_v1.js?v=1"></script>\n<script defer src="/static/nabil_scientific_solution_cards_e2e.js?v=4"></script>
<script defer src="/static/nabil_lesson_e2e_runtime_v1.js?v=4"></script>
<script defer src="/static/nabil_smart_lab_bridge_v1.js?v=3"></script>
<style>
{reference_renderer_css()}
#zoomModal {{ display:none; position:fixed; z-index:9999; inset:0; background:rgba(0,0,0,.88); justify-content:center; align-items:center; cursor:zoom-out; }}
#zoomModal img {{ max-width:92%; max-height:92%; border-radius:10px; }}
</style>
</head>
<body>
{_lab_index_script(lab_index or build_prebuilt_lab_index(entry, theory, []))}
<div class="container">
  <div class="header">
    <h1 style="margin:0; font-size:22px;">{clean_title}</h1>
    <div class="header-actions" style="display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end;">
      <button type="button" id="nabilExplainWholeLessonLabs" class="nav-btn" style="background:#0f766e;">🧪 {html.escape({"ar":"اشرح الدرس كاملًا بالمختبرات","fr":"Expliquer toute la leçon avec les laboratoires","en":"Explain the whole lesson with labs"}.get(page_a_lang_code,"Explain the whole lesson with labs"))}</button>
      <button type="button" onclick="document.getElementById('goldenReferenceCard')?.scrollIntoView({behavior:'smooth',block:'start'})" class="nav-btn" style="background:#7c3aed;">📌 {html.escape({"ar":"البطاقة النهائية","fr":"Carte finale","en":"Final reference card"}.get(page_a_lang_code,"Final reference card"))}</button>
      <button onclick="navigateToExercises()" class="nav-btn">{html.escape(ui_t(page_a_lang_code, "view_exercises"))}</button>
    </div>
  </div>
  {acts_html}
  <div class="card" style="margin-top:24px;">
    <div style="display:flex; justify-content:space-between; align-items:center;">
      <h3 style="margin:0; color:#0284c7;">{html.escape(ui_t(page_a_lang_code, "worksheet_title"))}</h3>
      <div id="wsScoreBadge" style="font-size:13px; font-weight:bold; color:#059669;">{html.escape(ui_t(page_a_lang_code, "score_label"))}: 0 / {len(theory['worksheet'])}</div>
    </div>
    <div style="width:100%; background:#e2e8f0; height:6px; border-radius:3px; margin:12px 0;">
      <div id="wsProgressBar" style="width:0%; background:#0284c7; height:6px; border-radius:3px; transition:width 0.3s ease;"></div>
    </div>
    {ws_items}
  </div>
  {theory.get("quiz_html", "")}
  {theory.get("whole_lesson_lab_html", "")}
  {theory.get("reference_card_html", "")}
</div>
<div id="zoomModal" onclick="this.style.display='none'"><img id="zoomImg" src=""></div>
<script>
let answeredCount = 0;
let score = 0;
const totalQuestions = {len(theory['worksheet'])};

function zoomImage(img) {{
  const modal = document.getElementById('zoomModal');
  const modalImg = document.getElementById('zoomImg');
  modal.style.display = 'flex';
  modalImg.src = img.src;
}}

function startNABILWholeLesson() {{
  const lab = document.getElementById('nabilWholeLessonSmartLab');
  if (!lab) return;
  lab.scrollIntoView({behavior:'smooth', block:'start'});
  setTimeout(() => {{
    if (window.NABILWholeLessonOrchestrator?.play) {{
      window.NABILWholeLessonOrchestrator.play();
    }} else {{
      document.getElementById('nabilWholePlay')?.click();
    }}
  }}, 280);
}}
document.getElementById('nabilExplainWholeLessonLabs')?.addEventListener('click', startNABILWholeLesson);

function nabilReadFinalCard(){{
  try{{
    const n=document.getElementById('nabilFinalCardSpeech'); if(!n)return;
    const d=JSON.parse(n.textContent||'{{}}'), spoken=String(d.text||'').trim(); if(!spoken)return;
    try{{window.NABILLessonE2E?.stopSpeech?.()}}catch(_e){{}}
    if(window.NABILLessonE2E?.speak){{window.NABILLessonE2E.speak(spoken,d.lang||'en');return;}}
    if('speechSynthesis' in window){{window.speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(spoken);u.lang=d.lang==='ar'?'ar':d.lang==='fr'?'fr-FR':'en-US';window.speechSynthesis.speak(u);}}
  }}catch(_e){{}}
}}
function nabilStopFinalCard(){{try{{window.NABILLessonE2E?.stopSpeech?.()}}catch(_e){{}}try{{window.speechSynthesis?.cancel?.()}}catch(_e){{}}}}

function navigateToExercises() {{
  const url = new URL(window.location.href);
  if (url.searchParams.has('lesson')) {{
    url.searchParams.set('view', 'exercises');
    window.location.href = url.toString();
  }} else {{
    const cur = window.location.pathname.split('/').pop();
    window.location.href = cur.replace('.html', '--EXERCISES.html');
  }}
}}
function gradeStep(btn, isCorrect, fb) {{
  const box = btn.parentElement.nextElementSibling;
  box.style.display = 'block';
  box.style.color = isCorrect ? '#059669' : '#dc2626';
  box.innerHTML = (isCorrect ? '✓ ' : '✗ ') + fb;
}}
function gradeWs(btn, isCorrect, exp) {{
  const parent = btn.parentElement;
  if (parent.dataset.answered) return;
  parent.dataset.answered = 'true';
  answeredCount++;
  if (isCorrect) score++;

  const box = parent.nextElementSibling;
  box.style.display = 'block';
  box.style.color = isCorrect ? '#059669' : '#dc2626';
  box.innerHTML = (isCorrect ? '{html.escape(ui_t(page_a_lang_code, "ws_correct"))}' : '{html.escape(ui_t(page_a_lang_code, "ws_incorrect"))}') + exp;

  document.getElementById('wsProgressBar').style.width = ((answeredCount / totalQuestions) * 100) + '%';
  document.getElementById('wsScoreBadge').innerText = '{html.escape(ui_t(page_a_lang_code, "score_label"))}: ' + score + ' / ' + totalQuestions;
}}
</script>
</body>
</html>'''



def _deterministic_evidence_reveal_spec(
        evidence_id: str, title: str, source_text: str, lang_code: str) -> dict:
    """No-LLM fallback: a real interactive lab using only supplied evidence."""
    quote = str(source_text or "").strip()[:1200]
    if not quote:
        raise RuntimeError("PREBUILT_LAB_SOURCE_EMPTY")
    return {
        "supported": True,
        "kind": "EVIDENCE_REVEAL",
        "title": str(title or "NABIL Interactive Explanation"),
        "instructions": {
            "ar": "استكشف المعطيات مع نبيل خطوة خطوة.",
            "fr": "Explore les données avec NABIL étape par étape.",
            "en": "Explore the givens with NABIL step by step.",
        }.get(lang_code, "Explore the givens with NABIL step by step."),
        "observation": {
            "ar": "هذا المختبر مبني فقط على المعطيات الموثقة.",
            "fr": "Ce laboratoire utilise uniquement les données vérifiées.",
            "en": "This lab uses only the verified givens.",
        }.get(lang_code, "This lab uses only the verified givens."),
        "evidence_ref": evidence_id,
        "evidence_basis": "text",
        "evidence_quote": quote,
        "items": [{
            "label": str(title or "Verified task"),
            "evidence_quote": quote,
        }],
        "prebuilt": True,
        "teacher_script": [
            {"say": str(title or "Read the verified task."), "target_ids": ["evidence:0"], "action": "point",
             "state_before": {"revealed_index": -1}, "state_after": {"revealed_index": 0},
             "scientific_constraints": ["Use only verified exercise evidence."], "evidence_quote": quote},
            {"say": str(title or "Work from the verified givens."), "target_ids": ["evidence:0"], "action": "explain",
             "state_before": {"revealed_index": 0}, "state_after": {"revealed_index": 0},
             "scientific_constraints": ["Do not introduce unsupported givens or relations."], "evidence_quote": quote},
        ],
    }


def prepare_prebuilt_exercise_labs(
        entry: dict, exercises: list, profile: dict, ev_map: dict) -> None:
    """Generate every exercise lab ONCE during lesson production.

    Student runtime never needs an LLM for an indexed exercise. Richer lab
    kinds are attempted from the exact verified prompt; if no richer kind is
    justified, an evidence-only interactive reveal is prebuilt deterministically.
    """
    lang_code = resolve_lang_code(entry.get("language", "en"))
    for ex in exercises:
        evidence_id = str(ex.get("exercise_id") or
                          f"{entry['lesson_id']}-EX-{ex.get('number')}")
        source_text = (
            str(ex.get("exact_source_prompt") or "").strip()
            + "\n"
            + "\n".join(str(x) for x in (ex.get("subquestions") or []))
        ).strip()
        figure_paths = []
        figure_refs = list(ex.get("figure_refs") or [])
        if figure_refs:
            for page_item in ev_map.get("pages_evidence", []):
                if int(page_item.get("page_num") or -1) != int(
                        ex.get("source_page") or -2):
                    continue
                for fig in page_item.get("figures") or []:
                    if (fig.get("figure_id") in figure_refs
                            and fig.get("image_path")
                            and Path(fig["image_path"]).is_file()):
                        figure_paths.append(str(fig["image_path"]))

        figure_image_base64 = None
        if figure_paths:
            from PIL import Image
            pics = []
            for filename in figure_paths[:4]:
                with Image.open(filename) as image:
                    pic = image.convert("RGB")
                    pic.thumbnail((1100, 850))
                    pics.append(pic.copy())
            if pics:
                canvas = Image.new(
                    "RGB",
                    (max(im.width for im in pics),
                     sum(im.height for im in pics) + 8 * (len(pics) - 1)),
                    "white",
                )
                top = 0
                for pic in pics:
                    canvas.paste(pic, (0, top))
                    top += pic.height + 8
                buf = io.BytesIO()
                canvas.save(buf, format="PNG")
                figure_image_base64 = base64.b64encode(
                    buf.getvalue()).decode("ascii")

        pseudo_concept = {
            "concept_id": evidence_id,
            "title": (
                f"{ex.get('section_type', 'EXERCISE')} {ex.get('number', '')}"
            ).strip(),
            "source_page": ex.get("source_page"),
            "raw_text": source_text,
            "normalized_text": source_text,
            "figure_refs": figure_refs,
            "math_records": [],
        }
        minimal_narrative = {
            "phenomenon": "",
            "investigation": "",
            "observation": "",
            "interpretation": "",
            "conclusion": "",
            "distractor_1": "",
            "distractor_2": "",
            "formulas": [],
            "units": [],
            "_scope_audited": True,
        }
        try:
            spec = build_verified_lab_spec(
                entry, pseudo_concept, minimal_narrative, profile,
                figure_image_base64=figure_image_base64,
                vision_context={
                    "lesson_id": entry.get("lesson_id"),
                    "book_id": entry.get("book_id"),
                    "pdf_page": ex.get("source_page"),
                } if figure_image_base64 else None)
        except Exception as exc:
            progress(
                "EXERCISE_RICH_LAB_FALLBACK_TO_PREBUILT_REVEAL",
                exercise_id=evidence_id,
                reason=str(exc)[:240],
            )
            spec = _deterministic_evidence_reveal_spec(
                evidence_id,
                pseudo_concept["title"],
                source_text,
                lang_code,
            )
        if spec.get("supported") is not True:
            spec = _deterministic_evidence_reveal_spec(
                evidence_id,
                pseudo_concept["title"],
                source_text,
                lang_code,
            )
        # Exercise lab provenance is canonicalized to the exercise index key.
        spec["evidence_ref"] = evidence_id
        try:
            lab_html, active = render_verified_lab(
                spec, lang_code, evidence_id)
        except Exception as exc:
            ex["_exercise_render_rejected"] = True
            ex["_exercise_render_rejection_reason"] = str(exc)[:500]
            progress(
                "EXERCISE_DROPPED_LAB_RENDER_FAILED_NOT_LESSON",
                exercise_id=evidence_id, reason=str(exc)[:240])
            continue
        if not active or not lab_html:
            ex["_exercise_render_rejected"] = True
            ex["_exercise_render_rejection_reason"] = (
                f"PREBUILT_EXERCISE_LAB_RENDER_FAILED:{evidence_id}")
            progress(
                "EXERCISE_DROPPED_LAB_RENDER_FAILED_NOT_LESSON",
                exercise_id=evidence_id)
            continue
        ex["_prebuilt_lab_spec"] = spec
        ex["_prebuilt_lab_html"] = lab_html
        ex["_prebuilt_lab_active"] = True
        ex["_prebuilt_lab_key"] = f"exercise:{evidence_id}"
        progress(
            "PREBUILT_EXERCISE_LAB_READY",
            exercise_id=evidence_id,
            kind=spec.get("kind"),
        )


def build_prebuilt_lab_index(entry: dict, theory: dict, exercises: list) -> dict:
    """Serializable concept/exercise/solution lab directory shipped once.

    Contract:
      concept id -> lab key
      exercise id -> solution card -> SAME lab key
    Indexed students never regenerate these labs at runtime.
    """
    concept_labs = []
    for act in theory.get("activities", []):
        spec = act.get("lab_spec") or {}
        key = f"concept:{act.get('concept_id')}"
        concept_labs.append({
            "key": key,
            "artifact": "theory",
            "concept_id": act.get("concept_id"),
            "title": act.get("title"),
            "kind": spec.get("kind"),
            "renderer_contract": REFERENCE_RENDERER_CONTRACT,
            "translation_languages": list(REFERENCE_RENDERER_LANGUAGES),
            "teacher_pointer": "sentence_synced",
            "teaching_mode": (act.get("teaching_signature") or {}).get("mode"),
            "teaching_level": (act.get("teaching_signature") or {}).get("level"),
            "secondary_year_contract": (
                act.get("teaching_signature") or {}
            ).get("secondary_year_contract"),
            "teaching_steps_count": len(act.get("teaching_steps") or []),
            "prebuilt": True,
            "active": bool(act.get("has_active_sim")),
        })
    exercise_labs = []
    for ex in exercises:
        spec = ex.get("_prebuilt_lab_spec") or {}
        key = str(ex.get("_prebuilt_lab_key") or "")
        ex["_solution_lab_key"] = key
        exercise_labs.append({
            "key": key,
            "solution_lab_key": key,
            "artifact": "exercises",
            "exercise_id": ex.get("exercise_id"),
            "number": ex.get("number"),
            "section_type": ex.get("section_type"),
            "kind": spec.get("kind"),
            "renderer_contract": REFERENCE_RENDERER_CONTRACT,
            "translation_languages": list(REFERENCE_RENDERER_LANGUAGES),
            "teacher_pointer": "sentence_synced",
            "prebuilt": True,
            "active": bool(ex.get("_prebuilt_lab_active")),
        })
    return {
        "schema": "nabil-prebuilt-lab-index/v2",
        "renderer_contract": REFERENCE_RENDERER_CONTRACT,
        "lesson_id": entry.get("lesson_id"),
        "grade": entry.get("grade"),
        "subject": entry.get("subject"),
        "translation_languages": list(REFERENCE_RENDERER_LANGUAGES),
        "voice": {
            "engine": "SpeechSynthesis",
            "paid_endpoint": False,
            "male_voice_preferred": True,
            "male_voice_guaranteed": False,
        },
        "mobile_reference_viewport": {
            "width": REFERENCE_MOBILE_VIEWPORT[0],
            "height": REFERENCE_MOBILE_VIEWPORT[1],
        },
        "concept_labs": concept_labs,
        "exercise_labs": exercise_labs,
        "whole_lesson_lab": {
            "key": "lesson:whole",
            "artifact": "theory",
            "renderer_contract": REFERENCE_RENDERER_CONTRACT,
            "concept_keys": [x["key"] for x in concept_labs],
            "teaching_story": True,
            "prebuilt": True,
            "active": bool(theory.get("whole_lesson_lab_active")),
        },
        "runtime_ai_required_for_indexed_labs": False,
    }


def _lab_index_script(lab_index: dict) -> str:
    payload = json.dumps(lab_index, ensure_ascii=False, separators=(",", ":"))
    payload = payload.replace("</", "<\\/")
    return (
        '<script id="nabilLabIndex" type="application/json">'
        + payload + '</script>'
    )


def render_lesson_page_b(entry: dict, exercises: list, profile: dict, ev_map: dict, lab_index: Optional[dict] = None) -> str:
    clean_title = html.escape(re.sub(r'^\s*\d{2,3}\s*(?:--|[-_ ]+)\s*', '', entry["canonical_title"]))
    clean_title = html.escape(re.sub(r'\s+\d{2,3}$', '', clean_title).strip())
    lesson_id = entry["lesson_id"]
    lang = entry.get("language", "en")
    page_b_lang_code = resolve_lang_code(lang)
    connecting_js = ui_t(page_b_lang_code, "connecting_solver")
    verified_js = ui_t(page_b_lang_code, "verified_solution")
    error_js = ui_t(page_b_lang_code, "solution_error")
    network_error_js = ui_t(page_b_lang_code, "network_error")
    final_answer_js = ui_t(page_b_lang_code, "final_answer_label")

    ex_cards = ""
    for ex in exercises:
        ex_num = ex["number"]
        sec_type = ex["section_type"]
        source_origin = ex.get("source_origin", "TEXTBOOK")
        localized_sec_type = (
            ui_t(page_b_lang_code, "exercise_label") if sec_type == "EXERCISE"
            else ui_t(page_b_lang_code, "problem_label") if sec_type == "PROBLEM"
            else sec_type
        )
        if source_origin == "TEXTBOOK":
            provenance_html = (
                '<span style="font-size:12px; color:#059669;">'
                '✓ ' + html.escape({
                    "ar": "موثّق من المصدر",
                    "fr": "Vérifié à la source",
                    "en": "Source verified",
                }.get(page_b_lang_code, "Source verified")) + '</span>'
            )
            card_title = f"{localized_sec_type} {ex_num}"
        else:
            provenance_html = (
                f'<span style="font-size:12px; color:#64748b;">'
                f'{ui_t(page_b_lang_code, "additional_practice_note")}</span>'
            )
            card_title = f"{ui_t(page_b_lang_code, 'additional_practice')} {ex_num}"

        ex_fig_html = ""
        if ex.get("reconstructed_diagram_verified") and ex.get("reconstructed_diagram_svg"):
            note = {
                "ar": "رسم تخطيطي معاد بناؤه من النص الموثق — ليس صورة الكتاب الأصلية",
                "fr": "Schéma reconstruit à partir du texte vérifié — ce n’est pas la figure originale du manuel",
                "en": "Schematic reconstructed from verified text — not the original textbook figure",
            }.get(page_b_lang_code, "Schematic reconstructed from verified text — not the original textbook figure")
            ex_fig_html = (
                '<div style="text-align:center; margin:12px 0;">'
                + str(ex["reconstructed_diagram_svg"])
                + '<div style="font-size:11px;color:#64748b;margin-top:4px;">'
                + html.escape(note) + '</div></div>'
            )
        # Original textbook figure pixels are deliberately not student-facing.
        # A verified NABIL redraw is required when the exercise needs a figure.

        if ex["solution_mode"] == "PRE_SOLVED":
            if ex.get("solution_status") == "OMITTED_UNVERIFIED":
                omitted_note = {
                    "ar": "لم يُعرض الحل الآلي لأن كل ادعاء فيه لم يمكن توثيقه بأمان من نص الدرس/الشكل الأصلي.",
                    "fr": "La solution automatique n'est pas affichée car toutes ses affirmations n'ont pas pu être vérifiées à partir du texte/figure source.",
                    "en": "Automatic solution omitted because every claim could not be safely verified against the lesson text/source figure.",
                }.get(
                    page_b_lang_code,
                    "Automatic solution omitted because every claim could not be safely verified against the lesson text/source figure."
                )
                sol_box = (
                    '<div style="margin-top:10px;padding:12px;background:#fff7ed;'
                    'border:1px solid #fed7aa;border-radius:6px;font-size:13px;'
                    'color:#9a3412;line-height:1.6;">'
                    + html.escape(omitted_note) + '</div>'
                )
            else:
                sol = ex.get("_pre_solved_solution")
                if sol is None:
                    sol = grounded_subject_solver(ex, ev_map, profile)
                    ex["_pre_solved_solution"] = sol
                step_label = ui_t(page_b_lang_code, "step_label")
                steps_html = "<br>".join([
                    f"• <b>{step_label}:</b> {html.escape(str(step))}"
                    for step in sol["steps"]
                ])
                card_spec = build_factory_solution_card_spec(entry, ex, sol)
                card_json = html.escape(
                    json.dumps(card_spec, ensure_ascii=False), quote=True)
                sol_box = f'''
                <div data-nabil-solution-card="{card_json}" style="margin-top:10px;">
                  <div class="nabil-solution-fallback" style="padding:12px; background:#ecfdf5; border-radius:6px; font-size:13px; color:#065f46; line-height:1.6;">
                    {verified_js}<br>
                    {steps_html}<br>
                    • <b>{final_answer_js}:</b> {html.escape(str(sol["final_answer"]))}
                  </div>
                </div>'''
        else:
            solve_label = ui_t(page_b_lang_code, "solve_on_demand", sec=sec_type, num=ex_num)
            sol_box = f'''
            <div id="demandBox_{sec_type}_{ex_num}" style="margin-top:10px;">
              <button onclick="requestServerSolution('{lesson_id}', '{sec_type}', {ex_num})" class="nav-btn" style="background:#475569; padding:8px 14px; font-size:12px;">{html.escape(solve_label)}</button>
              <div id="demandAns_{sec_type}_{ex_num}" style="display:none; margin-top:8px; padding:12px; background:#eff6ff; border-radius:6px; font-size:13px; color:#1e40af; line-height:1.6;"></div>
            </div>'''

        sub_html = ""
        if ex.get("subquestions"):
            sub_items = "".join([f"<li style='margin-top:4px;'>{html.escape(sq)}</li>" for sq in ex["subquestions"]])
            sub_html = f"<ul style='margin:6px 0 0 16px; padding:0; font-size:13px; color:#334155;'>{sub_items}</ul>"

        ex_cards += f'''
        <div class="card nabil-exercise-card" data-nabil-exercise-number="{ex_num}" data-nabil-section-type="{html.escape(sec_type)}" data-nabil-solution-lab-key="{html.escape(str(ex.get("_solution_lab_key") or ex.get("_prebuilt_lab_key") or ""))}" style="margin-top:16px;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <h3 style="margin:0; font-size:16px;">{card_title}</h3>
            {provenance_html}
          </div>
          <p class="nabil-exercise-prompt" style="margin:10px 0; font-size:14px; line-height:1.5;">{html.escape(ex["exact_source_prompt"])}</p>
          <button type="button" class="nabil-explain-lab-btn nav-btn" data-nabil-prebuilt-lab="true" style="background:#0f766e;margin:2px 0 8px;">🧪 {html.escape({"ar":"اشرح هذا التمرين بالمختبر","fr":"Expliquer cet exercice avec un laboratoire","en":"Explain this exercise with a lab"}.get(page_b_lang_code,"Explain this exercise with a lab"))}</button>
          <div class="nabil-prebuilt-exercise-lab" data-lab-key="{html.escape(str(ex.get("_prebuilt_lab_key") or ""))}" hidden>
            {ex.get("_prebuilt_lab_html", "")}
          </div>
          {ex_fig_html}
          {sub_html}
          {sol_box}
        </div>'''

    return f'''<!DOCTYPE html>
<html lang="{html.escape(lang)}" dir="{html_dir_attr(page_b_lang_code)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="nabil-lesson-id" content="{html.escape(entry['lesson_id'])}">
<meta name="nabil-canonical-title" content="{clean_title}">
<meta name="nabil-grade" content="{entry.get('grade', 7)}">
<meta name="nabil-subject" content="{html.escape(entry.get('subject', 'Physics'))}">
<meta name="nabil-source-book-id" content="{html.escape(entry['book_id'])}">
<meta name="nabil-source-pages" content="{entry['pdf_start_page']}-{entry['pdf_end_page']}">
<meta name="nabil-renderer-contract" content="{REFERENCE_RENDERER_CONTRACT}">
<meta name="nabil-translation-languages" content="ar,en,fr">
<title>{clean_title} - Official Exercises</title>
{MathRenderingEngine.inject_mathjax_head()}
<script defer src="/static/nabil_browser_tts_v1.js?v=1"></script>\n<script defer src="/static/nabil_lab_voice_v1.js?v=1"></script>\n<script defer src="/static/nabil_scientific_solution_cards_e2e.js?v=4"></script>
<script defer src="/static/nabil_lesson_e2e_runtime_v1.js?v=4"></script>
<script defer src="/static/nabil_smart_lab_bridge_v1.js?v=3"></script>
<style>
{reference_renderer_css()}
#zoomModal {{ display:none; position:fixed; z-index:9999; inset:0; background:rgba(0,0,0,.88); justify-content:center; align-items:center; cursor:zoom-out; }}
#zoomModal img {{ max-width:92%; max-height:92%; border-radius:10px; }}
</style>
</head>
<body>
{_lab_index_script(lab_index or build_prebuilt_lab_index(entry, {"activities": []}, exercises))}
<div class="container">
  <div class="header">
    <h1 style="margin:0; font-size:20px;">{html.escape(ui_t(page_b_lang_code, "exercises_page_title", title=html.unescape(clean_title)))}</h1>
    <button onclick="returnToLesson()" class="nav-btn" style="background:#475569;">{html.escape(ui_t(page_b_lang_code, "back_to_lesson"))}</button>
  </div>
  {ex_cards}
</div>
<div id="zoomModal" onclick="this.style.display='none'"><img id="zoomImg" src=""></div>
<script>
function zoomImage(img) {{
  const modal = document.getElementById('zoomModal');
  const modalImg = document.getElementById('zoomImg');
  modal.style.display = 'flex';
  modalImg.src = img.src;
}}

function returnToLesson() {{
  const url = new URL(window.location.href);
  if (url.searchParams.has('view')) {{
    url.searchParams.delete('view');
    window.location.href = url.toString();
  }} else {{
    const cur = window.location.pathname.split('/').pop();
    window.location.href = cur.replace('--EXERCISES.html', '.html');
  }}
}}

async function requestServerSolution(lessonId, secType, exNum) {{
  const ansBox = document.getElementById('demandAns_' + secType + '_' + exNum);
  ansBox.style.display = 'block';
  ansBox.innerHTML = '<i>{connecting_js}</i>';

  try {{
    const resp = await fetch('/api/interactive-lessons/solve-on-demand', {{
      method: 'POST',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify({{ lesson_id: lessonId, section_type: secType, exercise_number: exNum }})
    }});
    const data = await resp.json();
    if (data.status === 'SUCCESS') {{
      const sol = data.solution;
      if (data.solution_card && window.NABILScientificCards?.renderCard) {{
        window.NABILScientificCards.renderCard(data.solution_card, ansBox);
      }} else {{
        let stepsHtml = sol.steps.map(s => '• ' + s).join('<br>');
        ansBox.innerHTML = '{verified_js}' + stepsHtml + '<br><b>{final_answer_js}:</b> ' + sol.final_answer;
      }}
    }} else {{
      ansBox.innerHTML = '{error_js}' + (data.error || 'Unable to retrieve solution');
      ansBox.style.color = '#dc2626';
    }}
  }} catch (err) {{
    ansBox.innerHTML = '{network_error_js}';
    ansBox.style.color = '#dc2626';
  }}
}}
</script>
</body>
</html>'''


# ==============================================================================
# 11. QUALITY GATES & REAL PLAYWRIGHT CHROMIUM COMPREHENSIVE QA (390x844)
# ==============================================================================
def run_real_playwright_chromium_qa(html_path: str) -> bool:
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 390, "height": 844})
            page.goto(f"file://{Path(html_path).resolve()}")
            
            try:
                page.wait_for_selector('mjx-container', timeout=5000)
            except Exception:
                pass
            
            check_result = page.evaluate("""() => {
                const doc = document.documentElement;
                
                if (doc.scrollWidth > doc.clientWidth + 2) {
                    return { passed: false, reason: "HORIZONTAL_OVERFLOW" };
                }

                const buttons = Array.from(document.querySelectorAll('button, .q-opt'));
                for (let b of buttons) {
                    if (b.getBoundingClientRect().height < 43) {
                        return { passed: false, reason: "TOUCH_TARGET_TOO_SMALL", height: b.getBoundingClientRect().height };
                    }
                }

                const bodyText = document.body.innerText;
                if (bodyText.includes('\\\\(') || bodyText.includes('\\\\[')) {
                    return { passed: false, reason: "RAW_LATEX_DETECTED" };
                }

                const allElements = document.querySelectorAll('img, .card, mjx-container, p, h1, h2, h3');
                for (let el of allElements) {
                    const rect = el.getBoundingClientRect();
                    if (rect.right > 392 || rect.left < -2) {
                        return { passed: false, reason: "ELEMENT_BOUNDING_BOX_OVERFLOW", tag: el.tagName, right: rect.right };
                    }
                }

                const mathContentPresent = document.body.innerHTML.includes('\\\\(') || document.body.innerHTML.includes('\\\\[');
                const mjxCount = document.querySelectorAll('mjx-container').length;
                if (mathContentPresent && mjxCount === 0) {
                    return { passed: false, reason: "MATHJAX_CONTAINER_MISSING_DESPITE_MATH" };
                }

                const whole = document.getElementById('nabilWholeLessonSmartLab');
                if (whole) {
                    const frame = document.getElementById('nabilWholeLessonFrame');
                    if (!frame) return { passed:false, reason:"WHOLE_LESSON_FRAME_MISSING" };
                    if (!window.NABILWholeLessonOrchestrator ||
                        typeof window.NABILWholeLessonOrchestrator.current !== 'function' ||
                        typeof window.NABILWholeLessonOrchestrator.stop !== 'function') {
                        return { passed:false, reason:"WHOLE_LESSON_ORCHESTRATOR_MISSING" };
                    }
                }
                return { passed: true };
            }""")
            browser.close()
            
            if not check_result.get("passed", False):
                return False
        return True
    except Exception as e:
        raise RuntimeError(f"PLAYWRIGHT_CHROMIUM_QA_EXECUTION_FAILED: {e}")


def run_all_quality_gates(candidate: dict) -> Dict[str, Any]:
    progress("QUALITY_GATES: Auditing candidate against Real Playwright Chromium Comprehensive QA...")
    report = []

    def check(name: str, cond: bool, severity: str, det: str = ""):
        report.append({"name": name, "passed": bool(cond), "severity": severity, "details": det})
        if not cond and severity == "CRITICAL":
            raise AssertionError(f"QUALITY_GATE_FAILED: {name} -> {det}")

    ev_map = candidate["evidence_map"]
    s_lock = ev_map["source_lock"]
    expected_p = s_lock["end"] - s_lock["start"] + 1
    check("SOURCE_COVERAGE_INCOMPLETE", len(ev_map["pages_evidence"]) == expected_p, "CRITICAL", f"{len(ev_map['pages_evidence'])}/{expected_p} pages")
    completeness = ev_map.get("source_completeness") or {}
    check(
        "SOURCE_INVENTORY_COMPLETENESS_FAILED",
        completeness.get("passed") is True,
        "CRITICAL",
        json.dumps(completeness, ensure_ascii=False)[:1200],
    )

    exercise_start = ev_map.get("exercise_section_start_page")
    leaked_concepts = [
        {
            "concept_id": concept.get("concept_id"),
            "title": concept.get("title"),
            "source_page": concept.get("source_page"),
        }
        for concept in ev_map.get("concepts", [])
        if exercise_start is not None
        and int(concept.get("source_page") or -1) >= int(exercise_start)
    ]
    check(
        "LESSON_CONCEPT_LEAKED_FROM_EXERCISE_SECTION",
        not leaked_concepts,
        "CRITICAL",
        f"exercise_start_page={exercise_start}, leaked={leaked_concepts}",
    )

    required_unresolved_figures = {
        p["page_num"]: p.get("required_unverified_figure_labels", [])
        for p in ev_map["pages_evidence"]
        if p.get("required_unverified_figure_labels")
    }
    skipped_optional_figures = {
        p["page_num"]: p.get("skipped_unverified_figure_labels", [])
        for p in ev_map["pages_evidence"]
        if p.get("skipped_unverified_figure_labels")
    }
    check("SOURCE_FIGURE_REQUIRED_COVERAGE_INCOMPLETE",
          not required_unresolved_figures, "CRITICAL",
          f"required_unverified_source_figures={required_unresolved_figures}")
    check("OPTIONAL_SOURCE_FIGURE_SKIPPED",
          not skipped_optional_figures, "WARNING",
          f"skipped_unverified_source_figures={skipped_optional_figures}")

    textbook = [
        e for e in candidate["exercises"]
        if e.get("source_origin", "TEXTBOOK") == "TEXTBOOK"
    ]
    generated = [
        e for e in candidate["exercises"]
        if e.get("source_origin") == "AI_ADDITIONAL_PRACTICE"
    ]
    ex_nums = sorted([
        e["number"] for e in textbook
        if e["section_type"] == "EXERCISE"
    ])
    if ex_nums:
        check("EXERCISE_NUMBERING_INVALID",
              all(int(n) > 0 for n in ex_nums)
              and len(ex_nums) == len(set(ex_nums)),
              "CRITICAL", f"Verified exercises: {ex_nums}")
    # Missing numbers are allowed when those page items could not be verified.
    # We never invent/fill a missing textbook exercise.
    # Preserve all verified source exercises. If fewer than 3 are available,
    # add at least 3 gated AI practice exercises in addition to them.
    expected_ai = required_ai_practice_count(len(textbook))
    check("AI_FALLBACK_POLICY_VIOLATION",
          len(generated) == expected_ai, "CRITICAL",
          f"textbook={len(textbook)}, generated={len(generated)}, "
          f"expected_generated={expected_ai}")
    check("NO_PRACTICE_AVAILABLE",
          bool(textbook or generated), "CRITICAL",
          "Neither verified textbook exercises nor gated AI practice exists")

    for e in candidate["exercises"]:
        origin = e.get("source_origin", "TEXTBOOK")
        check("EXERCISE_PROMPT_INVALID",
              len(e["exact_source_prompt"]) >= 10,
              "CRITICAL", f"Ex {e['number']}")
        if origin == "TEXTBOOK":
            check("EXERCISE_FIDELITY_UNVERIFIED",
                  e.get("verified_against_source", False),
                  "CRITICAL", f"Ex {e['number']} source mismatch")
        else:
            check("AI_EXERCISE_SCIENTIFIC_GATE_FAILED",
                  e.get("scientific_gate_passed", False)
                  and bool(e.get("scope_concept_ids")),
                  "CRITICAL", f"Additional practice {e['number']}")
        if e["requires_figure"]:
            has_verified_reconstruction = bool(
                e.get("reconstructed_diagram_verified")
                and e.get("reconstructed_diagram_svg")
                and e.get("reconstructed_diagram_plan")
                and e.get("reconstructed_diagram_method") in {
                    "AI_RECONSTRUCTED_DIAGRAM_FROM_VERIFIED_TEXT",
                    "NABIL_EXPLANATORY_REDRAW_FROM_LOCKED_EVIDENCE",
                }
            )
            check("EXERCISE_DIAGRAM_REQUIRED_MISSING",
                  has_verified_reconstruction,
                  "CRITICAL",
                  f"Ex {e['number']} must have a NABIL redraw; source scan is hidden")

    pre_solved_statuses = [
        e.get("solution_status")
        for e in candidate["exercises"]
        if e.get("solution_mode") == "PRE_SOLVED"
    ]
    check(
        "PRE_SOLVE_STATUS_INVALID",
        all(s in {"SOLVED", "OMITTED_UNVERIFIED"} for s in pre_solved_statuses),
        "CRITICAL",
        f"statuses={pre_solved_statuses}",
    )
    solved_items = [
        e for e in candidate["exercises"]
        if e.get("solution_status") == "SOLVED"
    ]
    check(
        "SOLUTION_SOURCE_SCOPE_AUDIT_MISSING",
        all(
            (e.get("_pre_solved_solution") or {}).get("source_scope_audited") is True
            for e in solved_items
        ),
        "CRITICAL",
        "Every displayed solved exercise must pass text/figure source-scope audit",
    )
    check("WORKSHEET_NOT_GRADABLE", all("correct_index" in q for q in candidate["theory"]["worksheet"]), "CRITICAL", "Worksheet grading keys")
    check("REFERENCE_CARD_CONTENT_INCOMPLETE",
          "goldenReferenceCard" in candidate["page_a_html"],
          "CRITICAL", "Golden reference card missing")
    check("APPROVED_CARD_LAYOUT_MISSING",
          all(x in candidate["page_a_html"] for x in ("nabil-sci-card","nabil-sci-grid","nabil-sci-analysis","nabil-sci-visual","nabil-sci-teacher-panel","nabil-sci-final")),
          "CRITICAL", "Approved NABIL card division/colors missing")
    check("TEACHING_FLOW_APPLY_MISSING",
          candidate["page_a_html"].count('data-step="application"') == len(ev_map["concepts"]),
          "CRITICAL", "Every concept must end with Apply")
    check(
        "REFERENCE_CARD_CONCEPT_COVERAGE_INCOMPLETE",
        candidate["page_a_html"].count('class="nabil-reference-concept"') == len(ev_map["concepts"]),
        "CRITICAL",
        "reference_concepts="
        + str(candidate["page_a_html"].count('class="nabil-reference-concept"'))
        + ", concepts=" + str(len(ev_map["concepts"])),
    )
    lab_index = candidate.get("lab_index") or {}
    concept_lab_index = lab_index.get("concept_labs") or []
    exercise_lab_index = lab_index.get("exercise_labs") or []
    check(
        "PREBUILT_LAB_INDEX_SCHEMA_INVALID",
        lab_index.get("schema") == "nabil-prebuilt-lab-index/v2"
        and lab_index.get("renderer_contract") == REFERENCE_RENDERER_CONTRACT
        and lab_index.get("lesson_id") == candidate.get("lesson_id")
        and lab_index.get("runtime_ai_required_for_indexed_labs") is False,
        "CRITICAL",
        "Standalone/embedded lab index must identify this lesson and declare zero runtime AI for indexed labs",
    )
    whole_lab = lab_index.get("whole_lesson_lab") or {}
    check(
        "WHOLE_LESSON_SMART_LAB_MISSING",
        whole_lab.get("key") == "lesson:whole"
        and whole_lab.get("prebuilt") is True
        and whole_lab.get("active") is True
        and len(whole_lab.get("concept_keys") or []) == len(concept_lab_index)
        and 'data-whole-lesson-smart-lab="true"' in candidate["page_a_html"]
        and 'id="nabilWholeLessonFrame"' in candidate["page_a_html"],
        "CRITICAL",
        "Every lesson must ship one final Smart Board orchestrating all verified concept labs",
    )
    check(
        "TEACHING_ENGINE_SEQUENCE_INCOMPLETE",
        all(
            bool(a.get("teaching_signature"))
            and a.get("teaching_signature", {}).get("autonomous_teacher") is True
            and len(a.get("teaching_steps") or []) >= 3
            and all(
                str(step.get("sentence") or "").strip()
                and str(step.get("lab_key") or "") == "concept:" + str(a.get("concept_id") or "")
                and (step.get("evidence") or {}).get("concept_id") == a.get("concept_id")
                for step in (a.get("teaching_steps") or [])
            )
            for a in candidate["theory"].get("activities", [])
        ),
        "CRITICAL",
        "Every concept must carry an age/subject-specific evidence-locked teaching sequence linked to its concept lab",
    )
    geometry_acts = [
        a for a in candidate["theory"].get("activities", [])
        if str((a.get("lab_spec") or {}).get("kind") or "").upper() == "GEOMETRY_PROOF"
    ]
    check(
        "GEOMETRY_VISUAL_PROOF_MARKS_MISSING",
        all(
            'data-proof-marks="evidence-gated"' in str(a.get("lab_html") or "")
            and 'data-teacher-pointer="sentence-synced"' in str(a.get("lab_html") or "")
            and all(
                str(mark.get("evidence_quote") or "").strip()
                for mark in ((a.get("lab_spec") or {}).get("marks") or [])
            )
            and all(
                str(step.get("evidence_quote") or "").strip()
                and isinstance(step.get("target_ids") or [], list)
                for step in ((a.get("lab_spec") or {}).get("proof_steps") or [])
            )
            for a in geometry_acts
        ),
        "CRITICAL",
        "Geometry proof labs must reveal evidence-backed equality/angle/perpendicular/parallel/midpoint/symmetry marks while NABIL explains",
    )
    check(
        "SENTENCE_POINTER_SYNC_MISSING",
        all(
            'data-teacher-pointer="sentence-synced"' in str(a.get("lab_html") or "")
            for a in candidate["theory"].get("activities", [])
            if a.get("has_active_sim")
        )
        and all(
            'data-teacher-pointer="sentence-synced"' in str(
                e.get("_prebuilt_lab_html") or "")
            for e in candidate.get("exercises") or []
            if e.get("_prebuilt_lab_active")
        ),
        "CRITICAL",
        "Every concept/exercise lab must expose sentence-synchronized NABIL pointer behavior",
    )


    check(
        "PREBUILT_CONCEPT_LAB_INDEX_INCOMPLETE",
        len(concept_lab_index) == len(ev_map.get("concepts") or [])
        and all(x.get("prebuilt") is True and x.get("active") is True
                and str(x.get("key") or "").startswith("concept:")
                for x in concept_lab_index),
        "CRITICAL",
        f"indexed_concept_labs={len(concept_lab_index)}, concepts={len(ev_map.get('concepts') or [])}",
    )
    check(
        "PREBUILT_EXERCISE_LAB_INDEX_INCOMPLETE",
        len(exercise_lab_index) == len(candidate.get("exercises") or [])
        and all(x.get("prebuilt") is True and x.get("active") is True
                and str(x.get("key") or "").startswith("exercise:")
                for x in exercise_lab_index),
        "CRITICAL",
        f"indexed_exercise_labs={len(exercise_lab_index)}, exercises={len(candidate.get('exercises') or [])}",
    )
    check(
        "PREBUILT_LAB_INDEX_NOT_EMBEDDED",
        'id="nabilLabIndex"' in candidate["page_a_html"]
        and 'id="nabilLabIndex"' in candidate["page_b_html"],
        "CRITICAL",
        "Both lesson and exercise pages must carry the same prebuilt lab index",
    )
    check(
        "PREBUILT_EXERCISE_LABS_NOT_EMBEDDED",
        candidate["page_b_html"].count(
            'class="nabil-prebuilt-exercise-lab"')
        == len(candidate.get("exercises") or [])
        and candidate["page_b_html"].count(
            'data-nabil-prebuilt-lab="true"')
        == len(candidate.get("exercises") or []),
        "CRITICAL",
        "Every indexed exercise must ship with its ready-to-run lab HTML",
    )
    check(
        "STANDALONE_LAB_INDEX_ARTIFACT_MISSING",
        bool(candidate.get("filename_labs"))
        and bool(candidate.get("lab_index_json"))
        and candidate.get("hashes", {}).get("labs")
        == hashlib.sha256(
            str(candidate.get("lab_index_json") or "").encode("utf-8")
        ).hexdigest(),
        "CRITICAL",
        "Every lesson publish must include a separately hashed --LABS.json artifact",
    )

    check(
        "FORMAL_ARABIC_TEACHING_FAILED",
        all(
            a.get("formal_arabic_verified") is True
            for a in candidate["theory"].get("activities", [])
        ),
        "CRITICAL",
        "NABIL-authored Arabic teaching must use clear Modern Standard Arabic only",
    )

    check(
        "GENERATED_CONTENT_SCOPE_AUDIT_MISSING",
        all(
            a.get("generated_content_scope_audited") is True
            for a in candidate["theory"].get("activities", [])
        ),
        "CRITICAL",
        "Every generated lesson narrative must pass delete-only source-scope auditing",
    )

    # Quiz coverage applies only to generated question content that survived
    # the independent source-scope audit. Unsafe/out-of-scope generated quiz
    # material is omitted at item level rather than failing the whole lesson.
    concept_count = len(ev_map["concepts"])
    worksheet_count = len(candidate["theory"]["worksheet"])
    quiz_items = candidate["theory"].get("quiz_items") or []
    activities = candidate["theory"].get("activities") or []
    eligible_quiz_count = int(
        candidate["theory"].get("quiz_eligible_count", len(quiz_items)))
    check("QUIZ_VERIFIED_COVERAGE_INCONSISTENT",
          worksheet_count == eligible_quiz_count
          and len(quiz_items) == eligible_quiz_count
          and len(activities) == concept_count,
          "CRITICAL",
          f"worksheet={worksheet_count}, quiz={len(quiz_items)}, "
          f"eligible={eligible_quiz_count}, activities={len(activities)}, "
          f"concepts={concept_count}")

    check("FULL_QUIZ_BLOCK_MISSING",
          (eligible_quiz_count == 0)
          or ("fullQuizBlock" in candidate["page_a_html"]),
          "CRITICAL",
          "Verified quiz items exist but full quiz block is missing from Page A")

    # Every concept must have an explicit lab decision. A technical generation
    # failure is blocked earlier; supported=false is allowed only as a verified
    # "no evidence-backed interaction fits" decision.
    check(
        "LAB_REQUIRED_FOR_EVERY_CONCEPT",
        all(
            isinstance(a.get("lab_spec"), dict)
            and (a.get("lab_spec") or {}).get("supported") is True
            and a.get("has_active_sim") is True
            and bool(a.get("lab_html"))
            for a in activities
        ),
        "CRITICAL",
        "Every lesson concept/paragraph must have a verified interactive lab",
    )

    # Every declared lab must be evidence-validated and genuinely interactive.
    lab_activities = [
        a for a in activities
        if (a.get("lab_spec") or {}).get("supported") is True
    ]
    for act in lab_activities:
        spec = act.get("lab_spec") or {}
        lab_html = act.get("lab_html") or ""
        validate_lab_spec(spec)
        check("LAB_RENDER_MISSING",
              bool(lab_html), "CRITICAL",
              f"concept={act.get('concept_id')}")
        check("LAB_STUB_FORBIDDEN",
              'data-lab-kind=' in lab_html
              and '<script>' in lab_html
              and (
                  '<svg' in lab_html
                  or 'type="number"' in lab_html
                  or 'nabil-seq-step' in lab_html
                  or 'nabil-reveal-item' in lab_html
              )
              and 'nabil:demo' in lab_html,
              "CRITICAL",
              f"concept={act.get('concept_id')}")
        check("LAB_FAKE_NUMERIC_RANGE_FORBIDDEN",
              'type="range"' not in lab_html
              and ' min=' not in lab_html
              and ' max=' not in lab_html,
              "CRITICAL",
              f"concept={act.get('concept_id')}")

        lab_kind = str(spec.get("kind") or "").upper()
        if lab_kind in {"DC_SERIES_CIRCUIT", "OPTICS_REFLECTION", "IONIC_COMPOUND"}:
            check("LAB_TEACHER_POINTER_NOT_SYNCED",
                  'data-teacher-pointer="synced"' in lab_html
                  and 'teacherArrow' in lab_html
                  and 'pointTeacher' in lab_html,
                  "CRITICAL",
                  f"concept={act.get('concept_id')} kind={lab_kind}")
        if lab_kind == "DC_SERIES_CIRCUIT":
            check("LAB_OPEN_CIRCUIT_CURRENT_GUARD_MISSING",
                  "OPEN_CIRCUIT_ZERO_CURRENT" in lab_html
                  and "CURRENT_REQUIRES_CLOSED_SWITCH" in lab_html
                  and "switchClosed?V/Rt:0" in lab_html,
                  "CRITICAL",
                  f"concept={act.get('concept_id')}")
        elif lab_kind == "OPTICS_REFLECTION":
            check("LAB_OPTICS_NORMAL_REFERENCE_GUARD_MISSING",
                  'data-angle-reference="normal"' in lab_html
                  and "ANGLES_FROM_NORMAL" in lab_html
                  and "I_EQUALS_R" in lab_html,
                  "CRITICAL",
                  f"concept={act.get('concept_id')}")
        elif lab_kind == "IONIC_COMPOUND":
            check("LAB_IONIC_NEUTRALITY_GUARD_MISSING",
                  'data-charge-neutral="true"' in lab_html
                  and "CHARGE_NEUTRALITY" in lab_html,
                  "CRITICAL",
                  f"concept={act.get('concept_id')}")

    with tempfile.NamedTemporaryFile(suffix=".html", mode="w", encoding="utf-8", delete=False) as tmp_a:
        tmp_a.write(candidate["page_a_html"])
        path_a = tmp_a.name
    with tempfile.NamedTemporaryFile(suffix=".html", mode="w", encoding="utf-8", delete=False) as tmp_b:
        tmp_b.write(candidate["page_b_html"])
        path_b = tmp_b.name

    try:
        qa_a = run_real_playwright_chromium_qa(path_a)
        qa_b = run_real_playwright_chromium_qa(path_b)
    finally:
        Path(path_a).unlink(missing_ok=True)
        Path(path_b).unlink(missing_ok=True)

    check("MATH_RENDERING_FAILED", qa_a and qa_b, "CRITICAL", "MathJax successful rendering & bounding box overflow checks verified via real Playwright Chromium execution")
    check("MOBILE_REAL_PLAYWRIGHT_CHROMIUM_QA_390_844", qa_a and qa_b, "CRITICAL", "Real Playwright Chromium headless browser QA verified for 390x844 bounds, bounding boxes clipping & touch targets")

    check(
        "ONLY_VERIFIED_SOLVED_EXERCISES_STUDENT_FACING",
        all(
            e.get("solution_status") == "SOLVED"
            and isinstance(e.get("_pre_solved_solution"), dict)
            and bool(e.get("_prebuilt_lab_key"))
            for e in candidate.get("exercises") or []
        ),
        "CRITICAL",
        "Any exercise that cannot be solved, scientifically verified, and rendered is dropped individually; the lesson remains",
    )
    check(
        "AI_EXERCISE_SCOPE_GATE_REQUIRED",
        all(
            e.get("source_origin") != "AI_ADDITIONAL_PRACTICE"
            or (
                e.get("scientific_gate_passed") is True
                and bool(e.get("scope_concept_ids"))
                and e.get("solution_status") == "SOLVED"
            )
            for e in candidate.get("exercises") or []
        ),
        "CRITICAL",
        "AI practice must be traceable to verified lesson concepts and pass the scientific gate",
    )

    check(
        "STUDENT_SOURCE_SCAN_FORBIDDEN",
        "data:image/" not in candidate["page_a_html"]
        and "data:image/" not in candidate["page_b_html"],
        "CRITICAL",
        "Textbook/source raster images are evidence-only and must not be embedded in student lesson HTML",
    )
    forbidden_raster_tokens = (
        "page_image_url", "figure_image_urls", "originalPageImage",
        "عرض الصورة الأصلية لصفحة الكتاب", "Open original textbook page",
        "Actual scanned page from the indexed government textbook",
    )
    check(
        "STUDENT_SOURCE_RASTER_UI_FORBIDDEN",
        all(
            token not in candidate["page_a_html"]
            and token not in candidate["page_b_html"]
            for token in forbidden_raster_tokens
        ),
        "CRITICAL",
        "Textbook scans/figure pixels may be internal evidence only; student HTML may contain verified NABIL redraws/SVG only",
    )
    translation_report = candidate.get("translation_report") or {}
    check(
        "FULL_PAGE_TRANSLATION_INCOMPLETE",
        all(
            (translation_report.get(key) or {}).get("complete") is True
            and (translation_report.get(key) or {}).get("languages")
                == list(REFERENCE_RENDERER_LANGUAGES)
            and all(
                int(((translation_report.get(key) or {}).get(
                    "translated_counts") or {}).get(lang, -1))
                == int((translation_report.get(key) or {}).get(
                    "candidate_strings", -2))
                for lang in REFERENCE_RENDERER_LANGUAGES
            )
            for key in ("page_a", "page_b")
        )
        and all(
            'id="nabilPageLanguage"' in page
            and 'id="nabilPageTranslationBundle"' in page
            and 'data-nabil-translation-complete="true"' in page
            and 'data-nabil-lang="ar"' in page
            and 'data-nabil-lang="en"' in page
            and 'data-nabil-lang="fr"' in page
            for page in (candidate["page_a_html"], candidate["page_b_html"])
        ),
        "CRITICAL",
        "Lesson and exercise pages must ship complete prebuilt Arabic/English/French translation dictionaries and one global language control",
    )

    check(
        "REFERENCE_RENDERER_CONTRACT_MISSING",
        all(
            f'name="nabil-renderer-contract" content="{REFERENCE_RENDERER_CONTRACT}"' in page
            for page in (candidate["page_a_html"], candidate["page_b_html"])
        ),
        "CRITICAL",
        "Both student pages must use the approved content-agnostic golden reference renderer contract",
    )
    check(
        "EXERCISE_SOLUTION_LAB_LINKAGE_INCOMPLETE",
        all(
            bool(e.get("_prebuilt_lab_key"))
            and e.get("_solution_lab_key") == e.get("_prebuilt_lab_key")
            for e in candidate.get("exercises") or []
        )
        and candidate["page_b_html"].count("data-nabil-solution-lab-key=")
            == len(candidate.get("exercises") or []),
        "CRITICAL",
        "Every exercise/solution card must link to exactly its own prebuilt lab key",
    )
    check(
        "SCIENTIFIC_SOLUTION_CARD_LAB_KEY_MISSING",
        all(
            (
                e.get("solution_status") != "SOLVED"
                or str(e.get("_prebuilt_lab_key") or "") in candidate["page_b_html"]
            )
            for e in candidate.get("exercises") or []
        ),
        "CRITICAL",
        "Every displayed solved exercise must carry the same lab key into its Scientific Solution Card",
    )
    check(
        "NABIL_VISUAL_PIPELINE_MISSING",
        all(
            (a.get("has_active_sim") is True)
            or not a.get("source_figure_used_as_hidden_evidence")
            or a.get("visual_method") == "NABIL_EXPLANATORY_REDRAW_FROM_LOCKED_EVIDENCE"
            for a in candidate["theory"].get("activities", [])
        ),
        "CRITICAL",
        "Every concept that used a hidden source figure must teach through a verified NABIL lab/redraw",
    )
    check("NAVIGATION_FAILED", "navigateToExercises" in candidate["page_a_html"] and "returnToLesson" in candidate["page_b_html"], "CRITICAL", "Navigation intact")
    check("E2E_RUNTIME_NOT_WIRED",
          all("nabil_lesson_e2e_runtime_v1.js" in page for page in
              (candidate["page_a_html"], candidate["page_b_html"])),
          "CRITICAL",
          "Generated lesson/exercise pages must load the shared E2E runtime")
    check(
        "BROWSER_TTS_CONTRACT_NOT_WIRED",
        all("nabil_browser_tts_v1.js?v=1" in page for page in
            (candidate["page_a_html"], candidate["page_b_html"])),
        "CRITICAL",
        "All generated student pages must use the free browser SpeechSynthesis voice contract",
    )
    browser_tts_path = ROOT / "app/static/nabil_browser_tts_v1.js"
    browser_tts_source = (
        browser_tts_path.read_text(encoding="utf-8")
        if browser_tts_path.exists() else ""
    )
    check(
        "BROWSER_TTS_CONTRACT_INVALID",
        bool(browser_tts_source)
        and 'engine:"SpeechSynthesis"' in browser_tts_source
        and "SpeechSynthesisUtterance" in browser_tts_source
        and "maleVoicePreferred:true" in browser_tts_source
        and "paidEndpoint:false" in browser_tts_source
        and "/api/tts" not in browser_tts_source
        and "fetch(" not in browser_tts_source,
        "CRITICAL",
        "NABIL lesson voice must be browser SpeechSynthesis only; male voice is preferred when the device supplies one",
    )
    check("SCIENTIFIC_CARD_RENDERER_NOT_WIRED",
          all("nabil_scientific_solution_cards_e2e.js" in page for page in
              (candidate["page_a_html"], candidate["page_b_html"])),
          "CRITICAL",
          "Generated pages must use the approved Scientific Solution Card renderer")
    if any(e.get("solution_mode") == "PRE_SOLVED" for e in candidate["exercises"]):
        check("PRE_SOLVED_SCIENTIFIC_CARD_MISSING",
              "data-nabil-solution-card" in candidate["page_b_html"],
              "CRITICAL",
              "Verified pre-solved exercises must render through Scientific Solution Card")

    return {"passed": True, "gates": report}


def independent_scientific_review(entry: dict, candidate: dict) -> dict:
    # A genuine textbook phrase is not a code hardcode: audit evidence, not a word blacklist.
    prompt = (
        f"You are an Independent Senior Curriculum Auditor for Lebanese {entry['subject'].capitalize()} Grade {entry['grade']}.\n"
        f"Audit this complete lesson payload including evidence concepts and exercise solutions for absolute scientific rigor.\n"
        f"Lesson Title: {entry['canonical_title']}\n"
        f"Evidence Concepts: {json.dumps(candidate['evidence_map']['concepts'], ensure_ascii=False)}\n"
        f"Interactive Lab Specs: {json.dumps([a.get('lab_spec') for a in candidate['theory'].get('activities', [])], ensure_ascii=False)}\n"
        f"Teaching Steps: {json.dumps([a.get('teaching_steps') for a in candidate['theory'].get('activities', [])], ensure_ascii=False)}\n"
        f"Quiz Items: {json.dumps(candidate['theory'].get('quiz_items', []), ensure_ascii=False)}\n"
        f"Exercises & Solutions: {json.dumps(candidate['exercises'], ensure_ascii=False)}\n\n"
        "Reject any lab that introduces a scientific behavior, formula, orientation, shape rule, unit, "
        "or numeric claim not supported by the evidence. Verify every quiz answer against the evidence. "
        "Return strictly JSON: {'approved': bool, 'issues': [str], 'scientific_notes': str}"
    )

    try:
        res = execute_llm_completion(prompt, json_mode=True, temperature=0.0)
        parsed = json.loads(res)
        if not parsed.get("approved", False):
            raise RuntimeError(f"SCIENTIFIC_REVIEW_REJECTED: Audit failed -> {parsed.get('issues')}")
        return parsed
    except Exception as e:
        raise RuntimeError(f"SCIENTIFIC_REVIEW_REJECTED: reviewer unavailable or failed: {e}")


# ==============================================================================
# 12. ATOMIC PROMOTION & POST-UPLOAD SHA-256 VERIFICATION
# ==============================================================================
def rollback_lesson_drive(drive_service, lesson_id: str, target_version: int):
    root_id = resolve_drive_root_id()
    ver_file = VERSIONS_DIR / f"{lesson_id}.json"
    if not ver_file.exists():
        raise RuntimeError("ROLLBACK_VERSION_NOT_FOUND")

    meta = json.loads(ver_file.read_text(encoding="utf-8"))
    old_a = ARTIFACTS_DIR / f"{lesson_id}_v{target_version}_A.html"
    old_b = ARTIFACTS_DIR / f"{lesson_id}_v{target_version}_B.html"
    old_labs = ARTIFACTS_DIR / f"{lesson_id}_v{target_version}_LABS.json"

    if not (old_a.exists() and old_b.exists()):
        raise RuntimeError(f"ROLLBACK_ARTIFACTS_MISSING: Version v{target_version} files not found")

    content_a = old_a.read_text(encoding="utf-8")
    content_b = old_b.read_text(encoding="utf-8")
    content_labs = (
        old_labs.read_text(encoding="utf-8")
        if old_labs.exists() else None
    )

    from googleapiclient.http import MediaIoBaseUpload
    if meta.get("drive_theory_id"):
        media_a = MediaIoBaseUpload(io.BytesIO(content_a.encode("utf-8")), mimetype="text/html", resumable=True)
        drive_service.files().update(fileId=meta["drive_theory_id"], media_body=media_a).execute()

    if meta.get("drive_exercises_id"):
        media_b = MediaIoBaseUpload(io.BytesIO(content_b.encode("utf-8")), mimetype="text/html", resumable=True)
        drive_service.files().update(fileId=meta["drive_exercises_id"], media_body=media_b).execute()

    if meta.get("drive_labs_id") and content_labs is not None:
        media_labs = MediaIoBaseUpload(
            io.BytesIO(content_labs.encode("utf-8")),
            mimetype="application/json",
            resumable=True)
        drive_service.files().update(
            fileId=meta["drive_labs_id"], media_body=media_labs).execute()

    meta["published_version"] = target_version
    meta["status"] = "ROLLED_BACK"
    meta["history"].append({"action": "ROLLBACK", "target": target_version, "time": now()})
    ver_file.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    progress("ROLLBACK_DRIVE_EXECUTING_SUCCESS", lesson_id=lesson_id, target_version=target_version)



def _update_golden_registry(entry: dict, *, version: str, theory_id: str,
                            exercises_id: str | None = None, labs_id: str | None = None) -> None:
    """Atomically register a successfully verified Drive publication."""
    try:
        data = json.loads(GOLDEN_REGISTRY_PATH.read_text(encoding="utf-8")) if GOLDEN_REGISTRY_PATH.exists() else {}
    except Exception as exc:
        raise RuntimeError(f"GOLDEN_REGISTRY_INVALID:{exc}") from exc
    if not isinstance(data, dict):
        data = {}
    lessons = data.setdefault("lessons", {})
    lesson_id = str(entry.get("lesson_id") or "").strip().upper()
    if not lesson_id:
        raise RuntimeError("GOLDEN_REGISTRY_LESSON_ID_REQUIRED")
    language = resolve_lang_code(entry.get("language") or "en")
    lessons[lesson_id] = {
        "lesson_id": lesson_id,
        "title": str(entry.get("canonical_title") or lesson_id),
        "grade": str(entry.get("grade") or ""),
        "branch": str(entry.get("branch") or ""),
        "subject": str(entry.get("subject") or ""),
        "curriculum": str(entry.get("curriculum") or "Lebanese"),
        "language": language,
        "version": str(version),
        "drive_file_id": theory_id,
        "drive_theory_id": theory_id,
        "drive_exercises_id": exercises_id,
        "drive_labs_id": labs_id,
        "drive_url": f"https://drive.google.com/file/d/{theory_id}/view",
        "runtime_ai_required": False,
        "updated_at": now(),
    }
    data["schema"] = "nabil-golden-lessons/v1"
    data["updated_at"] = now()
    _atomic_write_text(GOLDEN_REGISTRY_PATH, json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\\n")


def promote_candidate(candidate: dict, entry: dict, drive_service) -> Tuple[str, str, str]:
    """Atomic Promotion with Post-Upload SHA-256 Verification & Safe Revert Backup."""
    root_id = resolve_drive_root_id()
    from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload

    def get_or_create_folder(name: str, parent: str) -> str:
        q = f"name = '{name}' and mimeType = 'application/vnd.google-apps.folder' and '{parent}' in parents and trashed = false"
        res = drive_service.files().list(q=q, fields="files(id)").execute().get("files", [])
        if len(res) > 1:
            raise RuntimeError(f"DRIVE_FOLDER_DUPLICATE_FAILED: Multiple folders named '{name}' under {parent}")
        if res:
            return res[0]["id"]
        meta = {"name": name, "mimeType": "application/vnd.google-apps.folder", "parents": [parent]}
        return drive_service.files().create(body=meta, fields="id").execute()["id"]

    grade_fid = get_or_create_folder(f"Grade {entry['grade']}", root_id)
    subject_folder_names = {
        "physics": "Physics - فيزياء",
        "mathematics": "Mathematics - رياضيات",
        "chemistry": "Chemistry - كيمياء",
        "biology": "Biology - علوم الحياة",
        "general_science": "General Science - علوم عامة",
    }
    subject_fid = get_or_create_folder(subject_folder_names.get(entry['subject'], entry['subject']), grade_fid)

    def get_existing_file(fname: str) -> Optional[dict]:
        q = f"name = '{fname}' and '{subject_fid}' in parents and trashed = false"
        files = drive_service.files().list(q=q, fields="files(id, name)").execute().get("files", [])
        return files[0] if files else None

    existing_a = get_existing_file(candidate["filename_a"])
    existing_b = get_existing_file(candidate["filename_b"])
    existing_labs = get_existing_file(candidate["filename_labs"])
    backup_data_a = None
    backup_data_b = None
    backup_data_labs = None
    if existing_a:
        backup_data_a = drive_service.files().get_media(fileId=existing_a["id"]).execute()
    if existing_b:
        backup_data_b = drive_service.files().get_media(fileId=existing_b["id"]).execute()
    if existing_labs:
        backup_data_labs = drive_service.files().get_media(
            fileId=existing_labs["id"]).execute()

    def upload_or_update(fname: str, content: str, existing: Optional[dict],
                         mimetype: str = "text/html", artifact: str = "theory") -> str:
        media = MediaIoBaseUpload(io.BytesIO(content.encode("utf-8")), mimetype=mimetype, resumable=True)
        props = {
            "nabil_lesson_id": str(entry.get("lesson_id") or "").strip().upper(),
            "nabil_language": resolve_lang_code(entry.get("language") or "en"),
            "nabil_version": str(candidate.get("version") or candidate.get("candidate_version") or "0.01"),
            "nabil_artifact": artifact,
            "nabil_golden": "true",
        }
        body={"name": fname, "appProperties": props}
        if existing:
            drive_service.files().update(fileId=existing["id"], body=body, media_body=media).execute()
            return existing["id"]
        body["parents"]=[subject_fid]
        return drive_service.files().create(body=body, media_body=media, fields="id").execute()["id"]

    tid = None
    eid = None
    lid = None
    try:
        tid = upload_or_update(
            candidate["filename_a"], candidate["page_a_html"], existing_a)
        eid = upload_or_update(
            candidate["filename_b"], candidate["page_b_html"], existing_b, artifact="exercises")
        lid = upload_or_update(
            candidate["filename_labs"], candidate["lab_index_json"],
            existing_labs, mimetype="application/json", artifact="labs")

        def verify_remote_sha256(file_id: str, local_content: str):
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, drive_service.files().get_media(fileId=file_id))
            done = False
            while not done:
                _, done = downloader.next_chunk()
            remote_sha = hashlib.sha256(fh.getvalue()).hexdigest()
            local_sha = hashlib.sha256(local_content.encode("utf-8")).hexdigest()
            if remote_sha != local_sha:
                raise RuntimeError(f"POST_UPLOAD_VERIFICATION_FAILED: SHA256 mismatch for file id {file_id}")

        verify_remote_sha256(tid, candidate["page_a_html"])
        verify_remote_sha256(eid, candidate["page_b_html"])
        verify_remote_sha256(lid, candidate["lab_index_json"])

    except Exception as e:
        if tid and existing_a and backup_data_a:
            revert_media_a = MediaIoBaseUpload(io.BytesIO(backup_data_a), mimetype="text/html", resumable=True)
            drive_service.files().update(fileId=tid, media_body=revert_media_a).execute()
        elif tid and not existing_a:
            drive_service.files().delete(fileId=tid).execute()

        if eid and existing_b and backup_data_b:
            revert_media_b = MediaIoBaseUpload(io.BytesIO(backup_data_b), mimetype="text/html", resumable=True)
            drive_service.files().update(fileId=eid, media_body=revert_media_b).execute()
        elif eid and not existing_b:
            drive_service.files().delete(fileId=eid).execute()

        if lid and existing_labs and backup_data_labs:
            revert_media_labs = MediaIoBaseUpload(
                io.BytesIO(backup_data_labs),
                mimetype="application/json",
                resumable=True)
            drive_service.files().update(
                fileId=lid, media_body=revert_media_labs).execute()
        elif lid and not existing_labs:
            drive_service.files().delete(fileId=lid).execute()

        raise RuntimeError(f"ATOMIC_PROMOTION_FAILED: Transaction rolled back safely ({e})")

    return tid, eid, lid


# ==============================================================================
# PRODUCTION PIPELINE ENTRY (LAZY DRIVE RESOLUTION)
# ==============================================================================
def produce_lesson_for_entry(entry: dict, drive_service=None, publish: bool = False) -> dict:
    lesson_id = entry["lesson_id"]
    book_id = entry["book_id"]
    progress("PRODUCTION_PIPELINE_START", lesson_id=lesson_id)
    assert_renderer_family_contract()

    ver_file = VERSIONS_DIR / f"{lesson_id}.json"
    if ver_file.exists():
        ver_meta = json.loads(ver_file.read_text(encoding="utf-8"))
        candidate_v = ver_meta.get("published_version", 0) + 1
    else:
        ver_meta = {"lesson_id": lesson_id, "published_version": 0, "history": []}
        candidate_v = 1

    profile = resolve_pedagogy_profile(entry)
    
    if drive_service is None and (publish or not Path(f"/app/data/books/{book_id}.pdf").exists()):
        drive_service = get_drive_service()
    elif drive_service is None:
        # Best-effort recovery channel. A local-book dry run remains valid if
        # Drive auth is unavailable; publication still requires Drive normally.
        try:
            drive_service = get_drive_service()
            progress("RECOVERY_CHECKPOINT_DRIVE_READY", lesson_id=lesson_id)
        except Exception as exc:
            progress(
                "RECOVERY_CHECKPOINT_DRIVE_UNAVAILABLE_CONTINUING_LOCAL",
                lesson_id=lesson_id, reason=str(exc)[:240])
            drive_service = None

    pdf_path = resolve_source_book_pdf(book_id, drive_service)
    import fitz
    doc = fitz.open(str(pdf_path))
    try:
        # Checkpointing is recovery infrastructure, not publication.
        # If Drive is already available, persist verified page evidence even in
        # dry-run mode so a transient provider/process failure can resume work.
        ev_map = build_evidence_map(
            doc, entry,
            drive_service=drive_service,
            persist_pages=(drive_service is not None))
    finally:
        doc.close()

    theory = synthesize_universal_pedagogy(entry, ev_map, profile)

    # 1) Attempt EVERY verified textbook exercise first.
    textbook_exercises = [dict(ex) for ex in ev_map["exercise_evidence"]]
    prepare_verified_solutions(
        entry, textbook_exercises, profile, ev_map,
        drive_service=drive_service, persist=publish)
    verified_textbook = retain_only_verified_solved_exercises(
        textbook_exercises, origin="TEXTBOOK")
    progress(
        "TEXTBOOK_EXERCISE_SOLVE_SUMMARY",
        extracted=len(textbook_exercises),
        verified_solved=len(verified_textbook),
        dropped=len(textbook_exercises) - len(verified_textbook))

    # 2) If only 0, 1, or 2 textbook exercises survived, ask AI for >=3
    #    ADDITIONAL exercises. Every candidate must pass the strict lesson-scope
    #    scientific gate; invented/out-of-scope exercises are discarded alone.
    generated_practice = generate_ai_practice_for_insufficient_book_exercises(
        entry, ev_map, profile,
        verified_textbook_count=len(verified_textbook))
    if generated_practice:
        prepare_verified_solutions(
            entry, generated_practice, profile, ev_map,
            drive_service=drive_service, persist=publish)
    verified_ai = retain_only_verified_solved_exercises(
        generated_practice, origin="AI_ADDITIONAL_PRACTICE")

    # The lesson survives exercise-level rejection. Only scientifically verified
    # solved exercises become student-facing.
    exercises = verified_textbook + verified_ai

    # 3) Build exercise labs individually. A bad exercise/lab is dropped, not
    #    the whole lesson.
    prepare_prebuilt_exercise_labs(entry, exercises, profile, ev_map)
    exercises = [
        ex for ex in exercises
        if not ex.get("_exercise_render_rejected")
        and ex.get("_prebuilt_lab_key")
        and ex.get("_pre_solved_solution")
        and ex.get("solution_status") == "SOLVED"
    ]
    progress(
        "FINAL_STUDENT_EXERCISE_SET",
        textbook=sum(1 for ex in exercises
                     if ex.get("source_origin", "TEXTBOOK") == "TEXTBOOK"),
        ai=sum(1 for ex in exercises
               if ex.get("source_origin") == "AI_ADDITIONAL_PRACTICE"),
        total=len(exercises))

    lab_index = build_prebuilt_lab_index(entry, theory, exercises)
    page_a_raw = render_lesson_page_a(
        entry, theory, ev_map, lab_index=lab_index)
    page_b_raw = render_lesson_page_b(
        entry, exercises, profile, ev_map, lab_index=lab_index)

    # Source/book raster pixels are NEVER student-facing. They may be used only
    # internally as hidden scientific evidence for OCR/vision/audit/redraw.
    page_a_raw = strip_source_rasters_from_student_html(
        page_a_raw, ev_map, "LESSON")
    page_b_raw = strip_source_rasters_from_student_html(
        page_b_raw, ev_map, "EXERCISES")

    source_lang_code = resolve_lang_code(entry.get("language", "en"))
    page_a, translation_a = build_trilingual_page_translation(
        page_a_raw, source_lang_code,
        purpose=f"lesson_page_translation_{lesson_id}")
    page_b, translation_b = build_trilingual_page_translation(
        page_b_raw, source_lang_code,
        purpose=f"exercise_page_translation_{lesson_id}")

    slug_subj = re.sub(r'[^\w]+', '-', entry.get("subject", "PHYSICS")).upper()
    slug_title = re.sub(r'[^\w]+', '-', entry["canonical_title"]).upper()
    seq_match = re.search(r'-(\d{3})$', lesson_id)
    seq_str = seq_match.group(1) if seq_match else "001"
    grade_str = f"G{int(entry.get('grade', 7)):02d}"

    # Two source PDFs may share grade/subject/title. Never overwrite a French
    # edition or revised textbook because its chapter number happens to match.
    source_key = re.sub(r"[^A-Za-z0-9]", "", entry.get("source_key", "")).upper()
    stem = f"{grade_str}-{slug_subj}--{source_key}--{seq_str}--{slug_title}" if source_key else f"{grade_str}-{slug_subj}--{seq_str}--{slug_title}"
    filename_a = stem + ".html"
    filename_b = stem + "--EXERCISES.html"
    filename_labs = stem + "--LABS.json"
    lab_index_json = json.dumps(
        lab_index, ensure_ascii=False, indent=2, sort_keys=True)

    candidate = {
        "lesson_id": lesson_id,
        "candidate_version": candidate_v,
        "filename_a": filename_a,
        "filename_b": filename_b,
        "filename_labs": filename_labs,
        "page_a_html": page_a,
        "page_b_html": page_b,
        "lab_index_json": lab_index_json,
        "evidence_map": ev_map,
        "theory": theory,
        "exercises": exercises,
        "lab_index": lab_index,
        "translation_report": {
            "page_a": translation_a,
            "page_b": translation_b,
        },
        "hashes": {
            "page_a": hashlib.sha256(page_a.encode("utf-8")).hexdigest(),
            "page_b": hashlib.sha256(page_b.encode("utf-8")).hexdigest(),
            "labs": hashlib.sha256(lab_index_json.encode("utf-8")).hexdigest(),
            "evidence": hashlib.sha256(json.dumps(ev_map).encode("utf-8")).hexdigest()
        }
    }

    gates_res = run_all_quality_gates(candidate)
    review_res = independent_scientific_review(entry, candidate)

    # QA and independent scientific review have passed. Only now freeze the
    # already-rendered labs as static reusable artifacts for every student.
    published_labs = persist_quality_gated_labs(entry, theory, exercises)

    path_a = OUT_DIR / filename_a
    path_b = OUT_DIR / filename_b
    path_labs = OUT_DIR / filename_labs

    (ARTIFACTS_DIR / f"{lesson_id}_v{candidate_v}_A.html").write_text(page_a, encoding="utf-8")
    (ARTIFACTS_DIR / f"{lesson_id}_v{candidate_v}_B.html").write_text(page_b, encoding="utf-8")
    (ARTIFACTS_DIR / f"{lesson_id}_v{candidate_v}_LABS.json").write_text(
        lab_index_json, encoding="utf-8")

    path_a.write_text(page_a, encoding="utf-8")
    path_b.write_text(page_b, encoding="utf-8")
    path_labs.write_text(lab_index_json, encoding="utf-8")
    progress(
        "LOCAL_ARTIFACTS_COMPILED",
        file_a=filename_a,
        file_b=filename_b,
        file_labs=filename_labs)

    drive_theory_id = None
    drive_exercises_id = None
    drive_labs_id = None
    status_str = "QA_PASSED_LOCAL"
    if publish:
        if drive_service is None:
            drive_service = get_drive_service()
        drive_theory_id, drive_exercises_id, drive_labs_id = promote_candidate(
            candidate, entry, drive_service)
        ver_meta["published_version"] = candidate_v
        ver_meta["drive_theory_id"] = drive_theory_id
        ver_meta["drive_exercises_id"] = drive_exercises_id
        ver_meta["drive_labs_id"] = drive_labs_id
        ver_meta["history"].append({"action": "PUBLISH", "version": candidate_v, "time": now()})
        _update_golden_registry(
            entry, version=str(candidate_v), theory_id=drive_theory_id,
            exercises_id=drive_exercises_id, labs_id=drive_labs_id,
        )
        ver_file.write_text(json.dumps(ver_meta, indent=2), encoding="utf-8")
        status_str = "PUBLISHED_VERIFIED"
        progress(
            "ATOMIC_PUBLISHED_AND_VERIFIED_TO_DRIVE",
            theory_id=drive_theory_id,
            exercises_id=drive_exercises_id,
            labs_id=drive_labs_id)

    rep = {
        "status": status_str,
        "lesson_id": lesson_id,
        "candidate_version": candidate_v,
        "canonical_title": entry["canonical_title"],
        "source_book_id": entry["book_id"],
        "source_pages": f"{entry['pdf_start_page']}..{entry['pdf_end_page']}",
        "evidence_hash": candidate["hashes"]["evidence"][:16],
        "activities_count": len(theory["activities"]),
        "exercises_count": len(exercises),
        "prebuilt_concept_labs": len(lab_index.get("concept_labs") or []),
        "prebuilt_exercise_labs": len(lab_index.get("exercise_labs") or []),
        "runtime_ai_required_for_indexed_labs": False,
        "published_static_labs": len(published_labs.get("artifacts") or []),
        "published_labs_index": published_labs.get("index"),
        "renderer_contract": REFERENCE_RENDERER_CONTRACT,
        "mobile_reference_viewport": {"width": 390, "height": 844},
        "source_raster_student_facing": False,
        "voice_engine": "SpeechSynthesis",
        "voice_paid_endpoint": False,
        "male_voice_preferred": True,
        "male_voice_guaranteed": False,
        "autonomous_teaching_engine": True,
        "whole_lesson_smart_lab": bool(theory.get("whole_lesson_lab_active")),
        "translation_report": candidate.get("translation_report"),
        "drive_theory_id": drive_theory_id,
        "drive_exercises_id": drive_exercises_id,
        "drive_labs_id": drive_labs_id,
        "gates_report": gates_res["gates"],
        "scientific_review": review_res,
        "local_files": [str(path_a), str(path_b), str(path_labs)]
    }
    return rep


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================
def main():
    global PROGRESS_STARTED
    PROGRESS_STARTED = time.monotonic()

    source_code = Path(__file__).read_text(encoding="utf-8")
    assert_no_lesson_specific_hardcode(source_code)
    assert_no_markdown_urls_in_runtime_code(source_code)
    py_compile.compile(__file__, doraise=True)

    parser = argparse.ArgumentParser(description="NABIL AI Universal Production Factory")
    parser.add_argument("--lesson-id", type=str, default=None, help="Exact canonical/discovered lesson ID")
    parser.add_argument("--grade", type=str, default=None, help="Grade selector, e.g. 7, G07, EB7, 9")
    parser.add_argument("--subject", type=str, default=None, help="Subject selector, e.g. physics, mathematics, فيزياء, رياضيات")
    parser.add_argument("--lesson", type=str, default=None, help="Lesson title/name inside the selected grade/subject")
    parser.add_argument("--index-book", type=str, default=None, help="Google Drive book file ID: index its TOC, lessons and works")
    parser.add_argument("--index-all-books", action="store_true", help="Discover and index every curriculum PDF under the configured Google Drive root")
    parser.add_argument("--force-book-index", action="store_true", help="Rebuild book indexes even when a valid cached index exists")
    parser.add_argument("--check-ai", action="store_true", help="Probe vision with generated blank image; no textbook page or Drive access")
    parser.add_argument("--publish", action="store_true", help="Publish produced lesson directly to Google Drive")
    parser.add_argument("--rollback", type=int, default=None, help="Target version to rollback; requires --lesson-id")
    args = parser.parse_args()

    if args.rollback is not None:
        if not args.lesson_id:
            raise RuntimeError("ROLLBACK_REQUIRES_LESSON_ID")
        drive_service = get_drive_service()
        rollback_lesson_drive(drive_service, args.lesson_id, args.rollback)
        return 0

    if args.check_ai:
        execute_preflight_checks(require_drive=False)
        from PIL import Image
        sample = io.BytesIO()
        Image.new("RGB", (64, 64), "white").save(sample, format="PNG")
        progress("AI_VISION_PROBE_START", image="generated_blank_64x64")
        response = execute_llm_completion(
            'Return only valid JSON: {"ok":true}', json_mode=True,
            image_base64=base64.b64encode(sample.getvalue()).decode("ascii"))
        json.loads(response)
        progress("AI_VISION_PROBE_PASS")
        return 0

    # No target means the universal action: discover and index the whole Drive curriculum.
    if not any((args.lesson_id, args.grade, args.subject, args.lesson, args.index_book, args.index_all_books)):
        args.index_all_books = True

    if args.index_all_books:
        drive_service = get_drive_service()
        report = build_all_registered_book_indexes(
            drive_service=drive_service,
            force=args.force_book_index,
        )
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["failed_count"] == 0 else 2

    if args.index_book:
        drive_service = get_drive_service()
        book_index = build_book_lesson_index(
            args.index_book,
            drive_service=drive_service,
            force=args.force_book_index,
        )
        print(json.dumps(book_index, ensure_ascii=False, indent=2))
        return 0

    # Grade and/or subject without a lesson means: index that complete scope.
    if (args.grade or args.subject) and not (args.lesson or args.lesson_id):
        drive_service = get_drive_service()
        report = build_scoped_book_indexes(
            drive_service=drive_service,
            force=args.force_book_index,
            grade=args.grade,
            subject=args.subject,
        )
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["failed_count"] == 0 else 2

    # A lesson title is dynamic: first ensure its grade/subject books are indexed,
    # then resolve the real discovered lesson and feed the unchanged production pipeline.
    if args.lesson:
        if not args.grade or not args.subject:
            raise RuntimeError("LESSON_SELECTOR_REQUIRES_GRADE_AND_SUBJECT")
        drive_service = get_drive_service()
        scope_report = build_scoped_book_indexes(
            drive_service=drive_service,
            force=args.force_book_index,
            grade=args.grade,
            subject=args.subject,
        )
        if scope_report["failed_count"]:
            raise RuntimeError(
                f"LESSON_SCOPE_INDEX_INCOMPLETE: failed_books={scope_report['failed_count']}")
        entry = resolve_lesson_selector(
            args.lesson, grade=args.grade, subject=args.subject)
    elif args.lesson_id:
        entry = resolve_canonical_entry(args.lesson_id)
    else:
        raise RuntimeError("TARGET_REQUIRED: use --index-all-books, --index-book, --grade/--subject, --lesson, or --lesson-id")

    execute_preflight_checks(require_drive=args.publish)
    drive_service = get_drive_service() if args.publish else None
    report = produce_lesson_for_entry(
        entry, drive_service=drive_service, publish=args.publish)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    main()
