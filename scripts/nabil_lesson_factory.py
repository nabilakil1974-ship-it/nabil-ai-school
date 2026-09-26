#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NABIL AI — Universal Pedagogical Lesson Factory
Version: 25.0.0 (Pure Plain-Text URLs & Strict Markdown Contamination Guard)
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

ROOT = Path(__file__).resolve().parents[1] if len(Path(__file__).resolve().parents) > 1 else Path("/app")
CATALOG_PATH = ROOT / "data/nabil_canonical_lesson_catalog.json"
PERM_EVIDENCE_DIR = ROOT / "data/evidence_maps"
CACHE_DIR = ROOT / "data/cache/visual_evidence"
VERSIONS_DIR = ROOT / "data/versions"
ARTIFACTS_DIR = VERSIONS_DIR / "artifacts"
OUT_DIR = ROOT / "output"

for d in [PERM_EVIDENCE_DIR, CACHE_DIR, VERSIONS_DIR, ARTIFACTS_DIR, OUT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

PROGRESS_STARTED = None


def now():
    return datetime.now(timezone.utc).isoformat()


def progress(stage: str, **details):
    elapsed = round(time.monotonic() - PROGRESS_STARTED, 1) if PROGRESS_STARTED else 0
    print(json.dumps({"time": now(), "elapsed_seconds": elapsed, "stage": stage, **details}, ensure_ascii=False), flush=True)


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


def resolve_pedagogy_profile(entry: dict) -> dict:
    if "grade" not in entry or entry["grade"] is None:
        raise RuntimeError("CANONICAL_CATALOG_CORRUPT: Missing grade")
    if "language" not in entry or not str(entry["language"]).strip():
        raise RuntimeError("CANONICAL_CATALOG_CORRUPT: Missing mandatory field 'language'")

    grade = int(entry["grade"])
    subject = entry.get("subject", "").strip().lower().replace(" ", "_")

    if subject not in SUBJECT_PROFILES:
        raise RuntimeError(f"PEDAGOGY_PROFILE_MISMATCH: Unknown curriculum subject '{subject}'")

    level = "L1" if grade <= 6 else ("L2" if grade <= 9 else "L3")
    return {
        "level": level,
        "level_profile": PEDAGOGY_PROFILES[level],
        "subject": subject,
        "subject_profile": SUBJECT_PROFILES[subject],
        "language": entry["language"],
        "grade": grade,
    }


# ==============================================================================
# 3. LLM INFERENCE ENGINE (FAIL-CLOSED)
# ==============================================================================
def execute_llm_completion(prompt: str, json_mode: bool = True, temperature: float = 0.0, image_base64: Optional[str] = None) -> str:
    # Select explicitly when several server-side keys exist. Default preserves
    # the original OpenRouter-first behavior to avoid unapproved image sharing.
    preferred = os.getenv("NABIL_FACTORY_AI_PROVIDER", "auto").strip().lower()
    keys = {
        "openrouter": os.getenv("OPENROUTER_API_KEY"),
        "groq": os.getenv("GROQ_API_KEY"),
        "openai": os.getenv("OPENAI_API_KEY"),
    }
    if preferred not in ("auto", *keys):
        raise RuntimeError(f"AI_PROVIDER_INVALID: {preferred}")
    if preferred == "auto":
        provider = next((name for name in ("openrouter", "groq", "openai")
                         if keys[name]), None)
    else:
        provider = preferred
    api_key = keys.get(provider) if provider else None
    if not api_key:
        raise RuntimeError(f"AI_PROVIDER_NOT_CONFIGURED: provider={provider or preferred}")

    if provider == "openrouter":
        url = "https://openrouter.ai/api/v1/chat/completions"
        model = (os.getenv("OPENROUTER_VISION_MODEL") if image_base64 else None) or os.getenv("OPENROUTER_TEXT_MODEL", "google/gemini-2.5-flash")
    elif provider == "groq":
        url = "https://api.groq.com/openai/v1/chat/completions"
        # A text-only model must never silently receive a textbook page image.
        model = (os.getenv("GROQ_VISION_MODEL", "qwen/qwen3.8-27b") if image_base64
                 else os.getenv("GROQ_TEXT_MODEL", "llama-3.3-70b-versatile"))
    else:
        url = "https://api.openai.com/v1/chat/completions"
        model = (os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini") if image_base64
                 else os.getenv("OPENAI_TEXT_MODEL", "gpt-4o-mini"))

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json",
               "User-Agent": "NABIL-AI-Lesson-Factory/1.0"}
    
    messages_content = [{"type": "text", "text": prompt}]
    if image_base64:
        messages_content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}})

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": messages_content if image_base64 else prompt}],
        "temperature": temperature
    }
    if json_mode:
        payload["response_format"] = {"type": "json_object"}

    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    max_attempts = 5
    for attempt in range(1, max_attempts + 1):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                content = data["choices"][0]["message"]["content"].strip()
                if content.startswith("```"):
                    content = re.sub(r"^```(?:json)?\s*|\s*```$", "", content, flags=re.I).strip()
                return content
        except urllib.error.HTTPError as exc:
            # The AI-provider refusal is not a Google Drive or PDF download error.
            # Include a short, sanitized explanation without disclosing API keys.
            provider = "openrouter" if "openrouter.ai" in url else ("groq" if "groq.com" in url else "openai")
            # Read upstream body once: Groq/edge providers may send non-JSON
            # (including HTML or an empty 403). Never discard the only diagnostic.
            try:
                raw_body = exc.read(4096).decode("utf-8", errors="replace")
            except OSError:
                raw_body = ""
            content_type = str(exc.headers.get("Content-Type", "")).split(";")[0].lower()
            detail, code = "", ""
            if raw_body:
                try:
                    upstream = json.loads(raw_body)
                    error = upstream.get("error", upstream) if isinstance(upstream, dict) else {}
                    if isinstance(error, dict):
                        detail = str(error.get("message") or error.get("detail") or "")
                        code = str(error.get("code") or error.get("type") or "")
                    elif isinstance(error, str):
                        detail = error
                except ValueError:
                    # Upstream access-control pages are often HTML, not JSON.
                    detail = re.sub(r"<[^>]+>", " ", raw_body)
            detail = re.sub(r"\s+", " ", detail).strip()
            code = re.sub(r"\s+", " ", code).strip()
            if not detail:
                detail = f"Empty or unrecognized provider 403 response (content_type={content_type or 'not-provided'})"
            for secret_name in ("OPENROUTER_API_KEY", "OPENAI_API_KEY", "GROQ_API_KEY"):
                secret = os.getenv(secret_name, "")
                if secret:
                    detail, code = detail.replace(secret, "[REDACTED]"), code.replace(secret, "[REDACTED]")
            detail = re.sub(r"(?i)\b(?:sk-or-v1-|sk-)[a-z0-9_-]{8,}", "[REDACTED]", detail)
            code = re.sub(r"(?i)\b(?:sk-or-v1-|sk-)[a-z0-9_-]{8,}", "[REDACTED]", code)
            if exc.code == 429 and attempt < max_attempts:
                # Groq commonly reports a fractional "Please try again in 15.78s".
                # Honor server's Retry-After when numeric; otherwise parse its
                # message. Keep the same provider and same textbook page, never
                # silently send approved book images to another provider.
                retry_header = str(exc.headers.get("Retry-After", "")).strip()
                try:
                    retry_after = float(retry_header)
                except ValueError:
                    retry_after = 0.0
                # A daily token ceiling often answers "5m12.336s" rather
                # than "15.7s". Previously this was capped at 120 seconds,
                # causing five unnecessary requests and total pilot failure.
                duration = re.search(
                    r"(?i)try again in\s+"
                    r"(?:(\d+(?:\.\d+)?)\s*h(?:ours?)?\s*)?"
                    r"(?:(\d+(?:\.\d+)?)\s*m(?:in(?:utes?)?)?\s*)?"
                    r"(?:(\d+(?:\.\d+)?)\s*s(?:ec(?:onds?)?)?)?",
                    detail,
                )
                indicated = 0.0
                if duration and any(group is not None for group in duration.groups()):
                    hours, minutes, seconds = duration.groups()
                    indicated = (3600 * float(hours or 0)
                                 + 60 * float(minutes or 0)
                                 + float(seconds or 0))
                wait_seconds = max(
                    retry_after, indicated, min(20.0 * attempt, 90.0)
                ) + 2.0
                max_wait = max(30.0, min(3600.0, float(
                    os.getenv("NABIL_FACTORY_MAX_RATE_LIMIT_WAIT_SECONDS", "1800")
                )))
                if wait_seconds > max_wait:
                    progress(
                        "AI_PROVIDER_RATE_LIMIT_LONG_COOLDOWN",
                        provider=provider, model=model,
                        required_wait_seconds=round(wait_seconds, 2),
                        max_wait_seconds=max_wait,
                    )
                    raise RuntimeError(
                        f"AI_PROVIDER_COOLDOWN_EXCEEDS_RUN_LIMIT: provider={provider} "
                        f"model={model} wait_seconds={wait_seconds:.1f}"
                    ) from None

                progress(
                    "AI_PROVIDER_RATE_LIMIT_WAIT", provider=provider, model=model,
                    attempt=attempt, max_attempts=max_attempts,
                    wait_seconds=round(wait_seconds, 2),
                    http_status=429, provider_code=code[:80],
                )
                time.sleep(wait_seconds)
                continue
            reason = detail[:360] or "No explanatory error message provided by the AI provider"
            progress("AI_PROVIDER_REQUEST_REJECTED", provider=provider, model=model,
                     http_status=exc.code, provider_code=code[:80], detail=reason)
            raise RuntimeError(
                f"AI_PROVIDER_HTTP_ERROR: provider={provider} model={model} "
                f"http_status={exc.code} provider_code={code[:80]} detail={reason}"
            ) from None


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


def assert_authorized_source_vision(lesson_id: str, book_id: str, pdf_page: int):
    """Only transfer textbook images approved for this provider and source range.

    A working API key or a successful AI probe never grants sharing consent.
    """
    consent_path = ROOT / "data/nabil_vision_consent.json"
    if not consent_path.exists():
        raise RuntimeError("VISION_SHARING_NOT_AUTHORIZED: consent catalog unavailable")
    scopes = json.loads(consent_path.read_text(encoding="utf-8")).get("approved_scopes", [])
    provider = os.getenv("NABIL_FACTORY_AI_PROVIDER", "auto").strip().lower()
    if provider == "auto":
        provider = next((name for name, key in (
            ("openrouter", os.getenv("OPENROUTER_API_KEY")),
            ("groq", os.getenv("GROQ_API_KEY")),
            ("openai", os.getenv("OPENAI_API_KEY"))
        ) if key), None)
    for item in scopes:
        lesson_allowed = (
            item.get("lesson_id") == lesson_id
            or bool(item.get("lesson_id_prefix")
                    and lesson_id.startswith(item["lesson_id_prefix"]))
        )
        if (lesson_allowed
                and item.get("book_id") == book_id
                and item.get("provider") == provider
                and int(item["pdf_start_page"]) <= pdf_page <= int(item["pdf_end_page"])):
            if not os.getenv(f"{provider.upper()}_API_KEY"):
                raise RuntimeError(f"AI_PROVIDER_NOT_CONFIGURED: {provider} required for approved visual evidence")
            return
    raise RuntimeError(
        f"VISION_SHARING_NOT_AUTHORIZED: provider={provider} lesson_id={lesson_id} page={pdf_page}"
    )


# ==============================================================================
# 6. MULTIMODAL EXTRACTION: TRUE VISION PAYLOAD, TOC & VECTOR GROUPING
# ==============================================================================
def extract_page_text_robust(doc, page_num: int, lesson_id: str, book_id: str, cache_dir: Path) -> str:
    page = doc[page_num - 1]
    txt = (page.get_text() or "").strip()
    if len(txt) >= 60:
        return txt

    if shutil.which("tesseract"):
        try:
            pix = page.get_pixmap(dpi=200)
            with tempfile.NamedTemporaryFile(suffix=".png") as img_tmp:
                pix.save(img_tmp.name)
                res = subprocess.run(["tesseract", img_tmp.name, "stdout", "-l", "eng+fra+ara", "--oem", "1"], capture_output=True, text=True, timeout=30)
                ocr_txt = res.stdout.strip()
                if len(ocr_txt) >= 60:
                    return ocr_txt
        except Exception:
            pass

    assert_authorized_source_vision(lesson_id, book_id, page_num)
    page_img = cache_dir / f"page_vision_{page_num}.png"
    page.get_pixmap(dpi=150).save(str(page_img))
    b64_img = base64.b64encode(page_img.read_bytes()).decode("utf-8")
    prompt = "Extract all text, exercises, and formulas verbatim from this curriculum page. Return JSON: {'text': str}"
    res = execute_llm_completion(prompt, json_mode=True, image_base64=b64_img)
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
                request_prompt, json_mode=True, image_base64=page_image)
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
                "evidence_method": "APPROVED_VISION_BOX_CROPPED_FROM_SOURCE_PDF"
            })
        progress("FIGURE_VISION_CROPS_VERIFIED", page=page_num,
                 candidates=len(extracted["figures"]),
                 accepted=len(figures),
                 printed_labels=[f.get("printed_label") for f in figures],
                 rejected=rejected_figures[:8])
    return figures


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
        "figure_labels (list of exact cited Figure numbers), confidence 0..1, "
        "and unreadable_parts (array). Include each exercise exactly once; "
        "do not confuse printed figure numbers, chapter numbers or page "
        "numbers with exercise numbers. Preserve table entries and all "
        "instructions. Do not invent any text. No numbered exercises -> []."
    )
    extracted = json.loads(execute_llm_completion(instruction, image_base64=page_b64))
    rows = _normalize_exercise_scan_payload(extracted, page_num)
    if not rows:
        return []
    audit_prompt = (
        "Independently compare these exercise transcriptions to the PROVIDED "
        "original source page image. Return JSON: "
        "{'checks':[{'number':int,'faithful':bool,'reason':str}]}. "
        "Mark false for a missing part, wrong figure number, invented words, "
        "wrong item boundaries, incorrect circled-number reading, or bad "
        "two-column order. No favorable assumptions. Transcriptions: "
        + json.dumps(rows, ensure_ascii=False)
    )
    review = json.loads(execute_llm_completion(audit_prompt, image_base64=page_b64))
    checks = _normalize_exercise_review_payload(review, page_num)
    approved = {int(x["number"]): x for x in checks if isinstance(x, dict)
                and "number" in x and x.get("faithful") is True}
    from fitz import Rect
    result = []
    for row in rows:
        if not isinstance(row, dict):
            raise RuntimeError(f"EXERCISE_SOURCE_MISMATCH: unexpected page item p{page_num}")
        number = int(row["number"])
        prompt = str(row.get("exact_source_prompt") or "").strip()
        coords = row.get("bbox_1000")
        if (number < 1 or number > 999 or len(prompt) < 10
                or row.get("unreadable_parts")
                or float(row.get("confidence", 0)) < 0.85
                or number not in approved
                or not isinstance(coords, list) or len(coords) != 4):
            raise RuntimeError(f"EXERCISE_SOURCE_MISMATCH: unverified exercise {number} p{page_num}")
        x0, y0, x1, y1 = [float(v) for v in coords]
        if not (0 <= x0 < x1 <= 1000 and 0 <= y0 < y1 <= 1000):
            raise RuntimeError(f"EXERCISE_SOURCE_MISMATCH: invalid region #{number} p{page_num}")
        rect = Rect(x0*page.rect.width/1000, y0*page.rect.height/1000,
                    x1*page.rect.width/1000, y1*page.rect.height/1000)
        raw_region = page.get_pixmap(clip=rect, dpi=200).tobytes("png")
        region_path = cache_dir / f"exercise_p{page_num}_{number}.png"
        region_path.write_bytes(raw_region)
        kind = str(row.get("section_type") or "EXERCISE").upper()
        if kind not in ("EXERCISE", "PROBLEM"):
            raise RuntimeError("EXERCISE_SOURCE_MISMATCH: invalid section type")
        result.append({
            "number": number, "section_type": kind, "exact_source_prompt": prompt,
            "subquestions": list(row.get("subquestions") or []),
            "source_page": page_num,
            "source_bbox": [rect.x0, rect.y0, rect.x1, rect.y1],
            "source_region_image_ref": str(region_path),
            "source_region_sha256": hashlib.sha256(raw_region).hexdigest(),
            "verified_against_source": True, "evidence_method": "TWO_PASS_SOURCE_PAGE_VISION"
        })
    return result


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
                                         "google/gemini-2.5-flash")),
        "openai": os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini"),
    }.get(source_provider, "none")
    if persist_pages:
        if drive_service is None:
            raise RuntimeError("PAGE_CHECKPOINT_REQUIRES_DRIVE_SERVICE")
        from scripts import nabil_page_checkpoint as page_checkpoints
        checkpoint_root = resolve_drive_root_id()
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
            if any(
                f.get("evidence_method") ==
                "APPROVED_VISION_BOX_CROPPED_FROM_SOURCE_PDF"
                for f in saved_page["figures"]
            ):
                assert_authorized_source_vision(lesson_id, book_id, p_num)
            pages_evidence.append(saved_page)
            progress("PAGE_EVIDENCE_RESTORED_FROM_DRIVE",
                     lesson_id=lesson_id, page=p_num,
                     figures=len(saved_page["figures"]))
            continue
        txt = (opening_text if p_num == start_p else
               extract_page_text_robust(doc, p_num, lesson_id, book_id, lesson_cache))
        figs = extract_multimodal_page_figures(
            doc, p_num, lesson_cache, lesson_id, book_id)
        page_evidence = {
            "page_num": p_num,
            "text": txt,
            "text_hash": hashlib.sha256(txt.encode("utf-8")).hexdigest()[:16],
            "figures": figs,
        }
        if page_checkpoints:
            # Save only when source labels mentioned by the real OCR text are
            # linked to source-page image crops. Never cache an unverified page.
            mentions = {m.lower() for m in re.findall(
                r"(?i)\bfig(?:ure)?\.?\s*(\d+[a-z]?)", txt)}
            found = {
                str(f.get("printed_label") or "").lower() for f in figs
            } | {
                str(f.get("printed_number")) for f in figs
                if f.get("printed_number") is not None
            }
            if not mentions or mentions.issubset(found):
                page_checkpoints.save_page(
                    drive_service, checkpoint_root, doc, entry,
                    page_evidence, source_provider, source_model)
                progress("PAGE_EVIDENCE_SAVED_TO_DRIVE",
                         lesson_id=lesson_id, page=p_num,
                         figures=len(figs))
            else:
                progress("PAGE_EVIDENCE_NOT_SAVED_UNVERIFIED_FIGURES",
                         lesson_id=lesson_id, page=p_num,
                         missing_labels=sorted(mentions - found))
        pages_evidence.append(page_evidence)

    concepts = []
    act_regex = re.compile(r"(?:Activity|Activité|نشاط|Section|Partie|Chapitre|فقرة)\s*(\d*)[:\s.-]+([^\n.]+)", re.I)
    for p in pages_evidence:
        page_doc = doc[p["page_num"] - 1]
        for m in act_regex.finditer(p["text"]):
            act_num = int(m.group(1)) if m.group(1) else len(concepts) + 1
            act_title = m.group(2).strip()
            chunk = " ".join(p["text"][m.start():m.start() + 500].split())
            matched_figs = match_figure_to_item({"raw_text": chunk, "requires_figure": False}, p["figures"], page_doc.rect)
            fig_ref = matched_figs[0] if matched_figs else "NONE"
            
            rects = page_doc.search_for(act_title[:20])
            act_bbox = [round(rects[0].x0, 1), round(rects[0].y0, 1), round(rects[0].x1, 1), round(rects[0].y1, 1)] if rects else [0.0, 0.0, page_doc.rect.width, 100.0]

            norm_chunk, math_ok, math_recs = MathRenderingEngine.normalize_math(chunk, p["page_num"], act_bbox, fig_ref)

            concepts.append({
                "concept_id": f"C{act_num:02d}",
                "title": act_title,
                "source_page": p["page_num"],
                "raw_text": chunk,
                "normalized_text": norm_chunk,
                "figure_refs": matched_figs,
                "math_records": math_recs,
                "sha256": hashlib.sha256(chunk.encode("utf-8")).hexdigest()[:16]
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
            refs = match_figure_to_item({"exact_source_prompt": content,
                                          "requires_figure": req_fig},
                                         p["figures"], source_page.rect)
            hashes = [f["image_sha256"] for f in p["figures"] if f["figure_id"] in refs]
            subqs = row.get("subquestions") or []
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
                "evidence_method": row.get("evidence_method", "NATIVE_PDF_TEXT")
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

    # All verified textbook exercises remain in the lesson.  AI-generated
    # practice is considered only later, and only when zero book exercises
    # could be faithfully extracted.
    for e in unique_ex:
        e["solution_mode"] = "PRE_SOLVED"

    ev_map = {
        "lesson_id": lesson_id,
        "book_id": entry["book_id"],
        "source_lock": {"start": start_p, "end": end_p},
        "pages_evidence": pages_evidence,
        "concepts": concepts,
        "exercise_evidence": unique_ex,
        "canonical_title": entry["canonical_title"]
    }

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
    """Return the required number of AI practice exercises."""
    if textbook_count <= 0:
        return 2
    if textbook_count == 1:
        return 3
    return 0


def generate_ai_practice_for_insufficient_book_exercises(
        entry: dict, ev_map: dict, profile: dict) -> List[dict]:
    """Supplement insufficient book exercises using the fixed product rule."""
    textbook_count = len(ev_map.get("exercise_evidence") or [])
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
            f"The official textbook yielded only {textbook_count} reliably "
            "extractable exercise(s), which is insufficient under the product "
            "rule (minimum 2 source exercises). Preserve every source exercise; "
            "generate ADDITIONAL practice ONLY from the VERIFIED LESSON SCOPE "
            "below. Do not introduce a law, definition, symbol, apparatus, "
            "formula, fact, or prerequisite that is absent from this scope. "
            "Do not require a figure. Make each question solvable entirely from "
            "what the student learned in this lesson. Return JSON exactly as "
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

        generated = json.loads(execute_llm_completion(
            generator_prompt, json_mode=True, temperature=0.2))
        candidates = generated.get("candidates")
        if not isinstance(candidates, list):
            raise RuntimeError(
                "AI_ADDITIONAL_PRACTICE_SCHEMA_INVALID: candidates missing")

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
                "fact, rule, relation and required reasoning is directly "
                "supported by that scope, the task is age-appropriate, internally "
                "consistent, solvable without outside knowledge, and its supplied "
                "solution outline is scientifically correct. Reject if uncertain. "
                "Return JSON exactly as "
                "{'approved':bool,'reasons':[str],'supported_concept_ids':[str],"
                "'solution_consistent':bool,'within_scope':bool}.\n"
                "VERIFIED LESSON SCOPE:\n"
                + json.dumps(scope, ensure_ascii=False)
                + "\nCANDIDATE:\n"
                + json.dumps(candidate, ensure_ascii=False)
            )
            verdict = json.loads(execute_llm_completion(
                gate_prompt, json_mode=True, temperature=0.0))
            approved = bool(
                verdict.get("approved")
                and verdict.get("solution_consistent")
                and verdict.get("within_scope")
                and isinstance(verdict.get("supported_concept_ids"), list)
                and verdict.get("supported_concept_ids")
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
            supported = [str(x) for x in verdict["supported_concept_ids"]]
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
                "generator_claimed_concept_ids": [
                    str(x) for x in claimed_ids],
                "evidence_method":
                    "AI_GENERATED_AFTER_SOURCE_SCOPE_SCIENTIFIC_GATE",
            })
            progress("AI_ADDITIONAL_PRACTICE_ACCEPTED",
                     number=idx, round=round_no,
                     supported_concepts=supported)

    if len(accepted) < desired_count:
        raise RuntimeError(
            "AI_ADDITIONAL_PRACTICE_INSUFFICIENT: "
            f"accepted={len(accepted)}/{desired_count}; "
            f"rejections={rejected_reasons[-8:]}")
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
                            fig_base64 = base64.b64encode(Path(f["image_path"]).read_bytes()).decode("ascii")
                        except Exception as exc:
                            raise RuntimeError(f"FIGURE_EVIDENCE_MISSING: Cannot read referenced source image: {exc}")
                        break

    if source_origin == "TEXTBOOK":
        provenance = f"official textbook exercise verbatim from Page {page}"
        scope_note = ""
    else:
        provenance = (
            "additional practice exercise already approved by the strict "
            "lesson-scope scientific gate"
        )
        supported = set(exercise.get("scope_concept_ids") or [])
        supported_scope = [
            {
                "concept_id": c.get("concept_id"),
                "text": c.get("normalized_text") or c.get("raw_text"),
            }
            for c in evidence_map.get("concepts", [])
            if c.get("concept_id") in supported
        ]
        scope_note = (
            "\nYou MUST solve using only these verified lesson concepts: "
            + json.dumps(supported_scope, ensure_ascii=False)
        )

    query = (
        f"You are Teacher NABIL, master professor of Lebanese "
        f"{subj.capitalize()} Grade {grade}.\n"
        f"Solve this {provenance}.\n"
        f"Prompt: {prompt}\n"
        f"Subquestions: {json.dumps(exercise.get('subquestions', []))}"
        f"{scope_note}\n\n"
        "RULES:\n"
        "1. Step-by-step rigorous deduction, derivation, and calculation. "
        "Analyze an accompanying figure only when a verified source figure "
        "is actually provided. No generic text or placeholders.\n"
        "2. State formulas, substitutions with units, and clear final answer.\n"
        "3. Never introduce knowledge outside the verified lesson scope.\n"
        "Return strictly JSON: {'steps': [str], 'final_answer': str}"
    )

    try:
        res = execute_llm_completion(query, json_mode=True, temperature=0.0, image_base64=fig_base64)
        parsed = json.loads(res)
        if not parsed.get("steps") or not parsed.get("final_answer"):
            raise ValueError("Incomplete solver response schema")
        
        verify_prompt = (
            f"Verify if this solution correctly answers the exercise prompt without contradictions.\n"
            f"Prompt: {prompt}\nSolution: {json.dumps(parsed, ensure_ascii=False)}\n"
            "Return strictly JSON: {'valid': bool}"
        )
        val_res = json.loads(execute_llm_completion(verify_prompt, json_mode=True, temperature=0.0))
        if not val_res.get("valid", False):
            raise RuntimeError("SOLVER_SOLUTION_VALIDATION_FAILED")

        exercise["solution_status"] = "SOLVED"
        return parsed
    except Exception as e:
        raise RuntimeError(f"PRE_SOLVE_FAILED: grounded solver unavailable or failed for Ex #{exercise['number']}: {e}")


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
    return {"status": "SUCCESS", "solution": sol}


# ==============================================================================
# 8. EVIDENCE-DRIVEN SYNTHESIS
# ==============================================================================
def synthesize_concept_narrative(concept: dict, profile: dict, figure_image_base64: Optional[str] = None) -> dict:
    prompt = (
        f"You are grounding a lesson explanation STRICTLY in the following extracted textbook text and source figure, when provided. "
        f"Generate plausible wrong answers (distractors) derived from common misconceptions of this text.\n\n"
        f"TEXT: {concept['raw_text']}\n\n"
        f"Subject: {profile['subject']}, Level: {profile['level']}\n"
        "Return strictly JSON: {"
        "'phenomenon': str, 'investigation': str, 'observation': str, 'interpretation': str, 'conclusion': str, "
        "'distractor_1': str, 'distractor_2': str, 'formulas': [str], 'units': [str]"
        "} — every field must be traceable to the TEXT above."
    )
    try:
        res = execute_llm_completion(prompt, json_mode=True, temperature=0.0, image_base64=figure_image_base64)
        parsed = json.loads(res)
        for k in ["phenomenon", "investigation", "observation", "interpretation", "conclusion", "distractor_1", "distractor_2"]:
            if not parsed.get(k):
                raise ValueError(f"Missing field {k}")
        return parsed
    except Exception as e:
        raise RuntimeError(f"NARRATIVE_SYNTHESIS_FAILED: Unable to ground concept narrative from evidence ({e})")


def synthesize_universal_pedagogy(entry: dict, ev_map: dict, profile: dict) -> dict:
    title = entry["canonical_title"]
    concepts = ev_map["concepts"]

    activities_theory = []
    worksheet = []
    panels = ""

    for idx, c in enumerate(concepts, 1):
        p_num = c["source_page"]
        fig_images = []
        fig_html = ""
        for p in ev_map["pages_evidence"]:
            if p["page_num"] == p_num and p["figures"]:
                for f in p["figures"]:
                    if f["figure_id"] in c.get("figure_refs", []):
                        with open(f["image_path"], "rb") as fh:
                            b64 = base64.b64encode(fh.read()).decode("ascii")
                        fig_images.append(f["image_path"])
                        fig_html += f'''<div class="figure" style="text-align:center; margin:14px 0;">
                            <img src="data:image/png;base64,{b64}" alt="{html.escape(c['title'])}" onclick="zoomImage(this)" style="max-width:100%; height:auto; border-radius:8px; border:1px solid #cbd5e1; cursor:zoom-in; transition: transform 0.2s;"/>
                            <div style="font-size:12px; color:#64748b; margin-top:4px;">Official Curriculum Figure: Page {p_num} (Click to Zoom)</div>
                        </div>'''
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
        narrative = synthesize_concept_narrative(c, profile, figure_image_base64)

        activities_theory.append({
            "activity_num": c["concept_id"].replace("C", ""),
            "title": c["title"],
            "source_page": p_num,
            "phenomenon": narrative["phenomenon"],
            "investigation": narrative["investigation"],
            "observation": narrative["observation"],
            "interpretation": narrative["interpretation"],
            "conclusion": narrative["conclusion"],
            "visual_html": fig_html,
            "student_question": {
                "q": f"Based on verified findings in '{c['title']}', what is confirmed?",
                "options": [narrative["conclusion"], narrative["distractor_1"], narrative["distractor_2"]],
                "correct_index": 0,
                "feedback": "Correct! Directly grounded in verified curriculum evidence."
            }
        })

        if idx <= 5:
            worksheet.append({
                "id": idx,
                "concept_id": c["concept_id"],
                "source_page": p_num,
                "source_hash": c["sha256"],
                "evidence_ref": c["concept_id"],
                "question": f"Which scientific deduction is confirmed regarding '{c['title']}'?",
                "options": [narrative["conclusion"], narrative["distractor_1"], narrative["distractor_2"]],
                "correct_index": 0,
                "explanation": f"Grounded directly in curriculum evidence on page {p_num} (Ref: {c['concept_id']})."
            })

        formulas_html = "".join([f"<li><b>Formula/Law:</b> {html.escape(f)}</li>" for f in narrative.get("formulas", [])])
        units_html = "".join([f"<li><b>Units:</b> {html.escape(u)}</li>" for u in narrative.get("units", [])])
        subject_metadata = f"<ul style='margin:4px 0 0 16px; padding:0; font-size:12px; color:#0369a1;'>{formulas_html}{units_html}</ul>" if (narrative.get("formulas") or narrative.get("units")) else ""

        panels += f'''<div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:10px; padding:14px; box-shadow:0 2px 4px rgba(0,0,0,0.04);">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #e2e8f0; padding-bottom:6px;">
                <span style="font-weight:700; color:#0369a1; font-size:15px;">{html.escape(c["title"])}</span>
                <span style="font-size:11px; background:#e0f2fe; color:#0284c7; padding:2px 6px; border-radius:4px; font-weight:600;">p. {c["source_page"]}</span>
            </div>
            <div style="margin-top:8px; font-size:13px; color:#334155; line-height:1.5;"><b>Extracted Principle:</b> {html.escape(narrative["conclusion"])}</div>
            {subject_metadata}
            {fig_html}
            <div style="margin-top:8px; font-size:12px; color:#059669; font-weight:600;">✓ Verified Evidence Grounding</div>
        </div>'''

    ref_card_html = f'''
    <!-- NABIL Golden Reference Final Study Card -->
    <div id="goldenReferenceCard" style="margin-top:28px; background:linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); border:2px solid #0284c7; border-radius:14px; padding:20px; box-shadow:0 4px 12px rgba(2,132,199,0.08);">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; border-bottom:2px solid #0284c7; padding-bottom:12px;">
        <div>
          <span style="background:#0284c7; color:#fff; font-size:11px; font-weight:800; padding:3px 8px; border-radius:4px; text-transform:uppercase;">Golden Reference Card</span>
          <h2 style="margin:4px 0 0 0; font-size:20px; color:#0f172a;">{html.escape(title)}</h2>
        </div>
        <span style="font-size:13px; font-weight:600; color:#64748b;">{profile["subject"].capitalize()} • Level {profile["level"]}</span>
      </div>
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap:14px; margin-top:16px;">
        {panels}
      </div>
      <div style="margin-top:16px; background:#eff6ff; border:1px solid #bfdbfe; border-radius:8px; padding:10px 14px; font-size:12px; color:#1e40af; display:flex; align-items:center; gap:8px;">
        <span>📌</span>
        <span><b>Study Reminder:</b> Formulated strictly from official textbook page ranges {ev_map["source_lock"]["start"]}–{ev_map["source_lock"]["end"]}.</span>
      </div>
    </div>'''

    return {
        "title": title,
        "activities": activities_theory,
        "lab_html": "",
        "has_active_sim": False,
        "worksheet": worksheet,
        "reference_card_html": ref_card_html
    }


# ==============================================================================
# 9. TWIN-PAGE HTML COMPILATION
# ==============================================================================
def render_lesson_page_a(entry: dict, theory: dict, ev_map: dict) -> str:
    clean_title = html.escape(re.sub(r'^\s*\d{2,3}\s*(?:--|[-_ ]+)\s*', '', entry["canonical_title"]))
    clean_title = html.escape(re.sub(r'\s+\d{2,3}$', '', clean_title).strip())
    lang = entry.get("language", "en")

    acts_html = ""
    for act in theory["activities"]:
        q = act["student_question"]
        opts = "".join([f'<button onclick="gradeStep(this, {i == q["correct_index"]}, \'{html.escape(q["feedback"])}\')" class="q-opt">{html.escape(o)}</button>' for i, o in enumerate(q["options"])])
        acts_html += f'''
        <div class="card" style="margin-top:20px;">
          <h3 style="color:#0369a1; margin-top:0;">{act["activity_num"]}. {html.escape(act["title"])}</h3>
          <p><b>Phenomenon:</b> {html.escape(act["phenomenon"])}</p>
          <p><b>Investigation:</b> {html.escape(act["investigation"])}</p>
          {act["visual_html"]}
          <p><b>Observation:</b> {html.escape(act["observation"])}</p>
          <p><b>Scientific Deduction:</b> <b>{html.escape(act["conclusion"])}</b></p>
          <div style="background:#f1f5f9; padding:12px; border-radius:6px; margin-top:12px;">
            <div style="font-weight:600; font-size:14px; margin-bottom:8px;">Check Understanding: {html.escape(q["q"])}</div>
            <div style="display:flex; gap:8px; flex-wrap:wrap;">{opts}</div>
            <div class="step-fb" style="margin-top:8px; font-size:13px; font-weight:600; display:none;"></div>
          </div>
        </div>'''

    ws_items = ""
    for idx, item in enumerate(theory["worksheet"]):
        opts = "".join([f'<button onclick="gradeWs(this, {i == item["correct_index"]}, \'{html.escape(item["explanation"])}\')" class="q-opt">{html.escape(o)}</button>' for i, o in enumerate(item["options"])])
        ws_items += f'''
        <div class="ws-item" style="margin-bottom:14px; padding:12px; background:#fff; border:1px solid #e2e8f0; border-radius:6px;">
          <div style="font-weight:600; margin-bottom:6px;">Question {idx+1}: {html.escape(item["question"])} <span style="font-size:11px; color:#64748b;">(p. {item['source_page']})</span></div>
          <div style="display:flex; gap:8px; flex-wrap:wrap;">{opts}</div>
          <div class="ws-fb" style="margin-top:6px; font-size:12px; font-weight:600; display:none;"></div>
        </div>'''

    return f'''<!DOCTYPE html>
<html lang="{html.escape(lang)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="nabil-lesson-id" content="{html.escape(entry['lesson_id'])}">
<meta name="nabil-canonical-title" content="{clean_title}">
<meta name="nabil-grade" content="{entry.get('grade', 7)}">
<meta name="nabil-subject" content="{html.escape(entry.get('subject', 'Physics'))}">
<meta name="nabil-source-book-id" content="{html.escape(entry['book_id'])}">
<meta name="nabil-source-pages" content="{entry['pdf_start_page']}-{entry['pdf_end_page']}">
<title>{clean_title} - NABIL Universal Engine</title>
{MathRenderingEngine.inject_mathjax_head()}
<style>
  :root {{ --primary: #0284c7; --bg: #f8fafc; --card: #ffffff; --text: #0f172a; --text-muted: #64748b; }}
  body {{ font-family: system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 16px; overflow-x: hidden; max-width: 100vw; box-sizing: border-box; }}
  .container {{ max-width: 860px; margin: 0 auto; width: 100%; box-sizing: border-box; }}
  .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #e2e8f0; padding-bottom: 12px; }}
  .card {{ background: var(--card); border-radius: 8px; padding: 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
  .nav-btn {{ background: var(--primary); color: #fff; padding: 10px 16px; border-radius: 6px; text-decoration: none; font-weight: 600; cursor: pointer; border: none; font-size: 14px; min-height: 44px; display: inline-flex; align-items: center; }}
  .q-opt {{ background:#fff; border:1px solid #cbd5e1; padding:8px 14px; border-radius:4px; cursor:pointer; font-size:13px; font-weight:500; min-height: 44px; }}
  .q-opt:hover {{ background:#e2e8f0; }}
  #zoomModal {{ display:none; position:fixed; z-index:9999; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.85); justify-content:center; align-items:center; cursor:zoom-out; }}
  #zoomModal img {{ max-width:90%; max-height:90%; border-radius:8px; box-shadow:0 4px 20px rgba(0,0,0,0.5); }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1 style="margin:0; font-size:22px;">{clean_title}</h1>
    <button onclick="navigateToExercises()" class="nav-btn">View Exercises ➔</button>
  </div>
  {acts_html}
  <div class="card" style="margin-top:24px;">
    <div style="display:flex; justify-content:space-between; align-items:center;">
      <h3 style="margin:0; color:#0284c7;">📝 Interactive Student Worksheet</h3>
      <div id="wsScoreBadge" style="font-size:13px; font-weight:bold; color:#059669;">Score: 0 / {len(theory['worksheet'])}</div>
    </div>
    <div style="width:100%; background:#e2e8f0; height:6px; border-radius:3px; margin:12px 0;">
      <div id="wsProgressBar" style="width:0%; background:#0284c7; height:6px; border-radius:3px; transition:width 0.3s ease;"></div>
    </div>
    {ws_items}
  </div>
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
  box.innerHTML = (isCorrect ? 'Correct! ' : 'Incorrect. ') + exp;

  document.getElementById('wsProgressBar').style.width = ((answeredCount / totalQuestions) * 100) + '%';
  document.getElementById('wsScoreBadge').innerText = 'Score: ' + score + ' / ' + totalQuestions;
}}
</script>
</body>
</html>'''


def render_lesson_page_b(entry: dict, exercises: list, profile: dict, ev_map: dict) -> str:
    clean_title = html.escape(re.sub(r'^\s*\d{2,3}\s*(?:--|[-_ ]+)\s*', '', entry["canonical_title"]))
    clean_title = html.escape(re.sub(r'\s+\d{2,3}$', '', clean_title).strip())
    lesson_id = entry["lesson_id"]
    lang = entry.get("language", "en")

    ex_cards = ""
    for ex in exercises:
        ex_num = ex["number"]
        sec_type = ex["section_type"]
        source_origin = ex.get("source_origin", "TEXTBOOK")
        if source_origin == "TEXTBOOK":
            provenance_html = (
                f'<span style="font-size:12px; color:#64748b;">'
                f'Source Page {ex["source_page"]}</span>'
            )
            card_title = f"{sec_type} {ex_num}"
        else:
            provenance_html = (
                '<span style="font-size:12px; color:#64748b;">'
                'Additional Practice — passed lesson scientific gate</span>'
            )
            card_title = f"Additional Practice {ex_num}"

        ex_fig_html = ""
        if ex.get("figure_refs"):
            for p in ev_map["pages_evidence"]:
                if p["page_num"] == ex["source_page"]:
                    for f in p["figures"]:
                        if f["figure_id"] in ex["figure_refs"]:
                            try:
                                b64 = base64.b64encode(Path(f["image_path"]).read_bytes()).decode("ascii")
                                ex_fig_html = f'''<div style="text-align:center; margin:12px 0;">
                                  <img src="data:image/png;base64,{b64}" alt="Exercise Figure" onclick="zoomImage(this)" style="max-width:100%; max-height:220px; border-radius:8px; border:1px solid #cbd5e1; cursor:zoom-in;"/>
                                  <div style="font-size:11px; color:#64748b; margin-top:3px;">Source Figure for {sec_type} {ex_num} (Click to Zoom)</div>
                                </div>'''
                            except Exception:
                                pass
                            break

        if ex["solution_mode"] == "PRE_SOLVED":
            sol = grounded_subject_solver(ex, ev_map, profile)
            steps_html = "<br>".join([f"• <b>Step:</b> {s}" for s in sol["steps"]])
            sol_box = f'''
            <div style="margin-top:10px; padding:12px; background:#ecfdf5; border-radius:6px; font-size:13px; color:#065f46; line-height:1.6;">
              <b>Step-by-Step Model Solution:</b><br>
              {steps_html}<br>
              • <b>Final Answer:</b> {sol["final_answer"]}
            </div>'''
        else:
            sol_box = f'''
            <div id="demandBox_{sec_type}_{ex_num}" style="margin-top:10px;">
              <button onclick="requestServerSolution('{lesson_id}', '{sec_type}', {ex_num})" class="nav-btn" style="background:#475569; padding:8px 14px; font-size:12px;">Solve {sec_type} {ex_num} On-Demand ⚡</button>
              <div id="demandAns_{sec_type}_{ex_num}" style="display:none; margin-top:8px; padding:12px; background:#eff6ff; border-radius:6px; font-size:13px; color:#1e40af; line-height:1.6;"></div>
            </div>'''

        sub_html = ""
        if ex.get("subquestions"):
            sub_items = "".join([f"<li style='margin-top:4px;'>{html.escape(sq)}</li>" for sq in ex["subquestions"]])
            sub_html = f"<ul style='margin:6px 0 0 16px; padding:0; font-size:13px; color:#334155;'>{sub_items}</ul>"

        ex_cards += f'''
        <div class="card" style="margin-top:16px;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <h3 style="margin:0; font-size:16px;">{card_title}</h3>
            {provenance_html}
          </div>
          <p style="margin:10px 0; font-size:14px; line-height:1.5;">{html.escape(ex["exact_source_prompt"])}</p>
          {ex_fig_html}
          {sub_html}
          {sol_box}
        </div>'''

    return f'''<!DOCTYPE html>
<html lang="{html.escape(lang)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="nabil-lesson-id" content="{html.escape(entry['lesson_id'])}">
<meta name="nabil-canonical-title" content="{clean_title}">
<meta name="nabil-grade" content="{entry.get('grade', 7)}">
<meta name="nabil-subject" content="{html.escape(entry.get('subject', 'Physics'))}">
<meta name="nabil-source-book-id" content="{html.escape(entry['book_id'])}">
<meta name="nabil-source-pages" content="{entry['pdf_start_page']}-{entry['pdf_end_page']}">
<title>{clean_title} - Official Exercises</title>
{MathRenderingEngine.inject_mathjax_head()}
<style>
  :root {{ --primary: #0284c7; --bg: #f8fafc; --card: #ffffff; --text: #0f172a; --text-muted: #64748b; }}
  body {{ font-family: system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 16px; overflow-x: hidden; max-width: 100vw; box-sizing: border-box; }}
  .container {{ max-width: 860px; margin: 0 auto; width: 100%; box-sizing: border-box; }}
  .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #e2e8f0; padding-bottom: 12px; }}
  .card {{ background: var(--card); border-radius: 8px; padding: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
  .nav-btn {{ background: var(--primary); color: #fff; padding: 10px 16px; border-radius: 6px; text-decoration: none; font-weight: 600; cursor: pointer; border: none; font-size: 13px; min-height: 44px; display: inline-flex; align-items: center; }}
  #zoomModal {{ display:none; position:fixed; z-index:9999; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.85); justify-content:center; align-items:center; cursor:zoom-out; }}
  #zoomModal img {{ max-width:90%; max-height:90%; border-radius:8px; box-shadow:0 4px 20px rgba(0,0,0,0.5); }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1 style="margin:0; font-size:20px;">{clean_title} - Exercises &amp; Problems</h1>
    <button onclick="returnToLesson()" class="nav-btn" style="background:#475569;">⬅ Back to Lesson</button>
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
  ansBox.innerHTML = '<i>Connecting to NABIL Solver Backend...</i>';

  try {{
    const resp = await fetch('/api/interactive-lessons/solve-on-demand', {{
      method: 'POST',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify({{ lesson_id: lessonId, section_type: secType, exercise_number: exNum }})
    }});
    const data = await resp.json();
    if (data.status === 'SUCCESS') {{
      const sol = data.solution;
      let stepsHtml = sol.steps.map(s => '• ' + s).join('<br>');
      ansBox.innerHTML = '<b>Verified Resolution:</b><br>' + stepsHtml + '<br><b>Answer:</b> ' + sol.final_answer;
    }} else {{
      ansBox.innerHTML = '<b>Error:</b> ' + (data.error || 'Unable to retrieve solution');
      ansBox.style.color = '#dc2626';
    }}
  }} catch (err) {{
    ansBox.innerHTML = '<b>Network Error:</b> Failed to reach solver endpoint.';
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
        check("EXERCISE_SEQUENCE_INCOMPLETE",
              ex_nums == list(range(1, len(ex_nums) + 1)),
              "CRITICAL", f"Exercises: {ex_nums}")
    # 0 source exercises: add 2 AI exercises.
    # 1 source exercise: preserve it and add 3 AI exercises.
    # 2 or more source exercises: add no AI exercises.
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
            check("EXERCISE_DIAGRAM_REQUIRED_MISSING",
                  len(e["figure_refs"]) > 0,
                  "CRITICAL", f"Ex {e['number']}")

    check("PRE_SOLVE_FAILED", all(e["solution_status"] == "SOLVED" for e in candidate["exercises"] if e["solution_mode"] == "PRE_SOLVED"), "CRITICAL", "Pre-solved exercises unverified")
    check("WORKSHEET_NOT_GRADABLE", all("correct_index" in q for q in candidate["theory"]["worksheet"]), "CRITICAL", "Worksheet grading keys")
    check("REFERENCE_CARD_CONTENT_INCOMPLETE", "goldenReferenceCard" in candidate["page_a_html"], "CRITICAL", "Golden reference card missing")

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

    check("NAVIGATION_FAILED", "navigateToExercises" in candidate["page_a_html"] and "returnToLesson" in candidate["page_b_html"], "CRITICAL", "Navigation intact")

    return {"passed": True, "gates": report}


def independent_scientific_review(entry: dict, candidate: dict) -> dict:
    # A genuine textbook phrase is not a code hardcode: audit evidence, not a word blacklist.
    prompt = (
        f"You are an Independent Senior Curriculum Auditor for Lebanese {entry['subject'].capitalize()} Grade {entry['grade']}.\n"
        f"Audit this complete lesson payload including evidence concepts and exercise solutions for absolute scientific rigor.\n"
        f"Lesson Title: {entry['canonical_title']}\n"
        f"Evidence Concepts: {json.dumps(candidate['evidence_map']['concepts'], ensure_ascii=False)}\n"
        f"Exercises & Solutions: {json.dumps(candidate['exercises'], ensure_ascii=False)}\n\n"
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

    if not (old_a.exists() and old_b.exists()):
        raise RuntimeError(f"ROLLBACK_ARTIFACTS_MISSING: Version v{target_version} files not found")

    content_a = old_a.read_text(encoding="utf-8")
    content_b = old_b.read_text(encoding="utf-8")

    from googleapiclient.http import MediaIoBaseUpload
    if meta.get("drive_theory_id"):
        media_a = MediaIoBaseUpload(io.BytesIO(content_a.encode("utf-8")), mimetype="text/html", resumable=True)
        drive_service.files().update(fileId=meta["drive_theory_id"], media_body=media_a).execute()

    if meta.get("drive_exercises_id"):
        media_b = MediaIoBaseUpload(io.BytesIO(content_b.encode("utf-8")), mimetype="text/html", resumable=True)
        drive_service.files().update(fileId=meta["drive_exercises_id"], media_body=media_b).execute()

    meta["published_version"] = target_version
    meta["status"] = "ROLLED_BACK"
    meta["history"].append({"action": "ROLLBACK", "target": target_version, "time": now()})
    ver_file.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    progress("ROLLBACK_DRIVE_EXECUTING_SUCCESS", lesson_id=lesson_id, target_version=target_version)


def promote_candidate(candidate: dict, entry: dict, drive_service) -> Tuple[str, str]:
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
    backup_data_a = None
    backup_data_b = None
    if existing_a:
        backup_data_a = drive_service.files().get_media(fileId=existing_a["id"]).execute()
    if existing_b:
        backup_data_b = drive_service.files().get_media(fileId=existing_b["id"]).execute()

    def upload_or_update(fname: str, content: str, existing: Optional[dict]) -> str:
        media = MediaIoBaseUpload(io.BytesIO(content.encode("utf-8")), mimetype="text/html", resumable=True)
        if existing:
            drive_service.files().update(fileId=existing["id"], media_body=media).execute()
            return existing["id"]
        return drive_service.files().create(body={"name": fname, "parents": [subject_fid]}, media_body=media, fields="id").execute()["id"]

    tid = None
    eid = None
    try:
        tid = upload_or_update(candidate["filename_a"], candidate["page_a_html"], existing_a)
        eid = upload_or_update(candidate["filename_b"], candidate["page_b_html"], existing_b)

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

        raise RuntimeError(f"ATOMIC_PROMOTION_FAILED: Transaction rolled back safely ({e})")

    return tid, eid


# ==============================================================================
# PRODUCTION PIPELINE ENTRY (LAZY DRIVE RESOLUTION)
# ==============================================================================
def produce_lesson_for_entry(entry: dict, drive_service=None, publish: bool = False, allow_pilot_publish: bool = False) -> dict:
    lesson_id = entry["lesson_id"]
    book_id = entry["book_id"]
    progress("PRODUCTION_PIPELINE_START", lesson_id=lesson_id)

    if lesson_id == "G07-PHYSICS-001" and publish and not allow_pilot_publish:
        raise RuntimeError("PILOT_PUBLISH_PROHIBITED: Golden Pilot lesson G07-PHYSICS-001 is QA-only and cannot be published directly to Drive.")

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

    pdf_path = resolve_source_book_pdf(book_id, drive_service)
    import fitz
    doc = fitz.open(str(pdf_path))
    try:
        ev_map = build_evidence_map(
            doc, entry, drive_service=drive_service, persist_pages=publish)
    finally:
        doc.close()

    theory = synthesize_universal_pedagogy(entry, ev_map, profile)
    textbook_exercises = list(ev_map["exercise_evidence"])
    generated_practice = generate_ai_practice_for_insufficient_book_exercises(
        entry, ev_map, profile)
    exercises = textbook_exercises + generated_practice
    if generated_practice:
        # Keep the candidate/evidence payload self-describing for scientific
        # review and on-demand solving. The official book evidence remains
        # separately identifiable by source_origin=TEXTBOOK.
        ev_map["exercise_evidence"] = exercises

    page_a = render_lesson_page_a(entry, theory, ev_map)
    page_b = render_lesson_page_b(entry, exercises, profile, ev_map)

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

    candidate = {
        "lesson_id": lesson_id,
        "candidate_version": candidate_v,
        "filename_a": filename_a,
        "filename_b": filename_b,
        "page_a_html": page_a,
        "page_b_html": page_b,
        "evidence_map": ev_map,
        "theory": theory,
        "exercises": exercises,
        "hashes": {
            "page_a": hashlib.sha256(page_a.encode("utf-8")).hexdigest(),
            "page_b": hashlib.sha256(page_b.encode("utf-8")).hexdigest(),
            "evidence": hashlib.sha256(json.dumps(ev_map).encode("utf-8")).hexdigest()
        }
    }

    gates_res = run_all_quality_gates(candidate)
    review_res = independent_scientific_review(entry, candidate)

    path_a = OUT_DIR / filename_a
    path_b = OUT_DIR / filename_b

    (ARTIFACTS_DIR / f"{lesson_id}_v{candidate_v}_A.html").write_text(page_a, encoding="utf-8")
    (ARTIFACTS_DIR / f"{lesson_id}_v{candidate_v}_B.html").write_text(page_b, encoding="utf-8")

    path_a.write_text(page_a, encoding="utf-8")
    path_b.write_text(page_b, encoding="utf-8")
    progress("LOCAL_ARTIFACTS_COMPILED", file_a=filename_a, file_b=filename_b)

    drive_theory_id = None
    drive_exercises_id = None
    status_str = "QA_PASSED_LOCAL"
    if publish:
        if drive_service is None:
            drive_service = get_drive_service()
        drive_theory_id, drive_exercises_id = promote_candidate(candidate, entry, drive_service)
        ver_meta["published_version"] = candidate_v
        ver_meta["drive_theory_id"] = drive_theory_id
        ver_meta["drive_exercises_id"] = drive_exercises_id
        ver_meta["history"].append({"action": "PUBLISH", "version": candidate_v, "time": now()})
        ver_file.write_text(json.dumps(ver_meta, indent=2), encoding="utf-8")
        status_str = "PUBLISHED_VERIFIED"
        progress("ATOMIC_PUBLISHED_AND_VERIFIED_TO_DRIVE", theory_id=drive_theory_id, exercises_id=drive_exercises_id)

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
        "drive_theory_id": drive_theory_id,
        "drive_exercises_id": drive_exercises_id,
        "gates_report": gates_res["gates"],
        "scientific_review": review_res,
        "local_files": [str(path_a), str(path_b)]
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
    parser.add_argument("--lesson-id", type=str, default="G07-PHYSICS-001", help="Target canonical lesson ID")
    parser.add_argument("--check-ai", action="store_true", help="Probe vision with generated blank image; no textbook page or Drive access")
    parser.add_argument("--publish", action="store_true", help="Publish directly to Google Drive")
    parser.add_argument("--rollback", type=int, default=None, help="Target version to rollback")
    args = parser.parse_args()

    if args.rollback is not None:
        drive_service = get_drive_service()
        rollback_lesson_drive(drive_service, args.lesson_id, args.rollback)
        return 0

    execute_preflight_checks(require_drive=args.publish)
    if args.check_ai:
        # Probe the image model without any source material; no Drive access.
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
    entry = resolve_canonical_entry(args.lesson_id)
    
    drive_service = get_drive_service() if args.publish else None

    report = produce_lesson_for_entry(entry, drive_service=drive_service, publish=args.publish)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    main()
