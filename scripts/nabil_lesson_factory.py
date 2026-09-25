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
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY") or os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("AI_PROVIDER_NOT_CONFIGURED: Missing LLM API key for intelligent grounded operations.")

    if os.getenv("OPENROUTER_API_KEY"):
        url = "https://openrouter.ai/api/v1/chat/completions"
        model = (os.getenv("OPENROUTER_VISION_MODEL") if image_base64 else None) or os.getenv("OPENROUTER_TEXT_MODEL", "google/gemini-2.5-flash")
    elif os.getenv("GROQ_API_KEY"):
        url = "https://api.groq.com/openai/v1/chat/completions"
        model = (os.getenv("GROQ_VISION_MODEL") if image_base64 else None) or os.getenv("GROQ_TEXT_MODEL", "llama-3.3-70b-versatile")
    else:
        url = "https://api.openai.com/v1/chat/completions"
        model = (os.getenv("OPENAI_VISION_MODEL") if image_base64 else None) or os.getenv("OPENAI_TEXT_MODEL", "gpt-4o-mini")

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    
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
        try:
            upstream = json.loads(exc.read(4096).decode("utf-8", errors="replace"))
            error = upstream.get("error", upstream) if isinstance(upstream, dict) else {}
            detail = str(error.get("message", "")) if isinstance(error, dict) else ""
            code = str(error.get("code", "")) if isinstance(error, dict) else ""
        except (ValueError, OSError):
            detail, code = "", ""
        detail = re.sub(r"\s+", " ", detail).strip()
        code = re.sub(r"\s+", " ", code).strip()
        for secret_name in ("OPENROUTER_API_KEY", "OPENAI_API_KEY", "GROQ_API_KEY"):
            secret = os.getenv(secret_name, "")
            if secret:
                detail, code = detail.replace(secret, "[REDACTED]"), code.replace(secret, "[REDACTED]")
        detail = re.sub(r"(?i)\b(?:sk-or-v1-|sk-)[a-z0-9_-]{8,}", "[REDACTED]", detail)
        code = re.sub(r"(?i)\b(?:sk-or-v1-|sk-)[a-z0-9_-]{8,}", "[REDACTED]", code)
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
    try:
        from scripts.index_books import get_drive_service as base_get_drive
        return base_get_drive()
    except Exception:
        pass

    creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "/app/credentials.json")
    scopes = ["https://www.googleapis.com/auth/drive"]
    if os.path.exists(creds_path):
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        creds = service_account.Credentials.from_service_account_file(creds_path, scopes=scopes)
        return build("drive", "v3", credentials=creds, cache_discovery=False)

    import google.auth
    from googleapiclient.discovery import build
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
        raise RuntimeError(f"LESSON_NOT_FOUND_IN_CATALOG: {lesson_id}")

    required = ["lesson_id", "canonical_title", "grade", "subject", "book_id", "pdf_start_page", "pdf_end_page", "language"]
    for f in required:
        if f not in found or found[f] is None:
            raise RuntimeError(f"CANONICAL_CATALOG_CORRUPT: Missing mandatory field '{f}' in {lesson_id}")

    return found


def assert_authorized_source_vision(lesson_id: str, book_id: str, pdf_page: int):
    """Only transfer textbook images approved by the owner for this exact book
    and page range. Never treat a working API key as sharing consent.
    """
    consent_path = ROOT / "data/nabil_vision_consent.json"
    if not consent_path.exists():
        raise RuntimeError("VISION_SHARING_NOT_AUTHORIZED: consent catalog unavailable")
    scopes = json.loads(consent_path.read_text(encoding="utf-8")).get("approved_scopes", [])
    for item in scopes:
        if (item.get("lesson_id") == lesson_id
                and item.get("book_id") == book_id
                and item.get("provider") == "openrouter"
                and int(item["pdf_start_page"]) <= pdf_page <= int(item["pdf_end_page"])):
            if not os.getenv("OPENROUTER_API_KEY"):
                raise RuntimeError("AI_PROVIDER_NOT_CONFIGURED: OpenRouter required for approved visual evidence")
            return
    raise RuntimeError(f"VISION_SHARING_NOT_AUTHORIZED: {lesson_id} page {pdf_page}")


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
                "bbox": [round(rect.x0, 1), round(rect.y0, 1),
                         round(rect.x1, 1), round(rect.y1, 1)],
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
            pix.save(str(path))
            content = path.read_bytes()
            figures.append({
                "figure_id": f"FIG_P{page_num}_V{idx+1}", "printed_number": None,
                "printed_label": None, "source_page": page_num,
                "bbox": [round(rect.x0, 1), round(rect.y0, 1),
                         round(rect.x1, 1), round(rect.y1, 1)],
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
        extracted = json.loads(execute_llm_completion(
            prompt, image_base64=base64.b64encode(pix.tobytes("png")).decode("ascii")))
        if not isinstance(extracted.get("figures"), list):
            raise RuntimeError("FIGURE_EVIDENCE_MISSING: vision figure schema invalid")
        for idx, info in enumerate(extracted["figures"]):
            if not isinstance(info, dict) or float(info.get("confidence", 0)) < 0.75:
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
            label = str(info.get("printed_label") or "").strip().lower()
            label_match = re.fullmatch(r"(\d+)([a-z]?)", label)
            if label and not label_match:
                continue
            content = page.get_pixmap(clip=rect, dpi=180).tobytes("png")
            path = cache_dir / f"fig_p{page_num}_scanned_{idx+1}.png"
            path.write_bytes(content)
            figures.append({
                "figure_id": f"FIG_P{page_num}_SCAN_{idx+1}",
                "printed_number": int(label_match.group(1)) if label_match else None,
                "printed_label": label or None, "source_page": page_num,
                "bbox": [round(rect.x0, 1), round(rect.y0, 1),
                         round(rect.x1, 1), round(rect.y1, 1)],
                "caption": str(info.get("caption") or ""),
                "visual_description": str(info.get("visual_description") or ""),
                "image_path": str(path),
                "image_sha256": hashlib.sha256(content).hexdigest(),
                "visual_occupancy": round(
                    rect.width*rect.height/(page.rect.width*page.rect.height), 3),
                "confidence": float(info["confidence"]),
                "evidence_method": "APPROVED_VISION_BOX_CROPPED_FROM_SOURCE_PDF"
            })
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
    if not title_clean or title_clean not in opener:
        return False

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
    rows = extracted.get("exercises")
    if not isinstance(rows, list):
        raise RuntimeError(f"EXERCISE_SOURCE_MISMATCH: invalid scan evidence p{page_num}")
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
    checks = review.get("checks")
    if not isinstance(checks, list):
        raise RuntimeError(f"EXERCISE_SOURCE_MISMATCH: review missing p{page_num}")
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
            "source_bbox": [round(v, 1) for v in (rect.x0,rect.y0,rect.x1,rect.y1)],
            "source_region_image_ref": str(region_path),
            "source_region_sha256": hashlib.sha256(raw_region).hexdigest(),
            "verified_against_source": True, "evidence_method": "TWO_PASS_SOURCE_PAGE_VISION"
        })
    return result


def build_evidence_map(doc, entry: dict) -> dict:
    start_p = int(entry["pdf_start_page"])
    end_p = int(entry["pdf_end_page"])
    lesson_id = entry["lesson_id"]
    book_id = entry["book_id"]
    if start_p < 1 or end_p < start_p or end_p > len(doc):
        raise RuntimeError(f"SOURCE_PAGE_OUT_OF_RANGE: {lesson_id}, pages {start_p}-{end_p}, book length {len(doc)}")

    pages_evidence = []
    lesson_cache = CACHE_DIR / f"{book_id}_{lesson_id}"
    lesson_cache.mkdir(parents=True, exist_ok=True)
    for p_num in range(start_p, end_p + 1):
        txt = extract_page_text_robust(doc, p_num, lesson_id, book_id, lesson_cache)
        figs = extract_multimodal_page_figures(doc, p_num, lesson_cache, lesson_id, book_id)
        p_hash = hashlib.sha256(txt.encode("utf-8")).hexdigest()[:16]
        pages_evidence.append({
            "page_num": p_num,
            "text": txt,
            "text_hash": p_hash,
            "figures": figs
        })

    if not verify_title_double_evidence_strict(doc, entry, pages_evidence[0]["text"]):
        raise AssertionError(f"TITLE_VERIFICATION_FAILED: Strict Double Evidence TOC + Opening failed for '{entry['canonical_title']}'.")

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
            rows = extract_scanned_page_exercises(doc, page_num, lesson_id, book_id, lesson_cache)
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
                "solution_mode": "ON_DEMAND", "solution_status": "NOT_SOLVED",
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

    ex_c, pr_c = 0, 0
    for e in unique_ex:
        if e["section_type"] == "EXERCISE" and ex_c < 2:
            e["solution_mode"] = "PRE_SOLVED"
            ex_c += 1
        elif e["section_type"] == "PROBLEM" and pr_c < 3:
            e["solution_mode"] = "PRE_SOLVED"
            pr_c += 1

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
# 7. MULTI-MODAL GROUNDED SOLVER & STRICT FAIL-CLOSED VERIFIER
# ==============================================================================
def grounded_subject_solver(exercise: dict, evidence_map: dict, profile: dict) -> Dict[str, Any]:
    prompt = exercise["exact_source_prompt"]
    page = exercise["source_page"]
    subj = profile["subject"]
    grade = profile.get("grade", 7)

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

    query = (
        f"You are Teacher NABIL, master professor of Lebanese {subj.capitalize()} Grade {grade}.\n"
        f"Solve this official textbook exercise verbatim from Page {page}.\n"
        f"Prompt: {prompt}\n"
        f"Subquestions: {json.dumps(exercise.get('subquestions', []))}\n\n"
        "RULES:\n"
        "1. Step-by-step rigorous deduction, derivation, and calculation. Analyze accompanying figure if provided. No generic text or placeholders.\n"
        "2. State formulas, substitutions with units, and clear final answer.\n"
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
            <h3 style="margin:0; font-size:16px;">{sec_type} {ex_num}</h3>
            <span style="font-size:12px; color:#64748b;">Source Page {ex["source_page"]}</span>
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

    ex_nums = sorted([e["number"] for e in candidate["exercises"] if e["section_type"] == "EXERCISE"])
    check("EXERCISE_SEQUENCE_INCOMPLETE", len(ex_nums) > 0 and ex_nums == list(range(1, len(ex_nums) + 1)), "CRITICAL", f"Exercises: {ex_nums}")

    for e in candidate["exercises"]:
        check("EXERCISE_SOURCE_MISMATCH", len(e["exact_source_prompt"]) >= 10, "CRITICAL", f"Ex {e['number']}")
        check("EXERCISE_FIDELITY_UNVERIFIED", e.get("verified_against_source", False), "CRITICAL", f"Ex {e['number']} source mismatch")
        if e["requires_figure"]:
            check("EXERCISE_DIAGRAM_REQUIRED_MISSING", len(e["figure_refs"]) > 0, "CRITICAL", f"Ex {e['number']}")

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
    subject_fid = get_or_create_folder(entry['subject'], grade_fid)

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
def produce_lesson_for_entry(entry: dict, drive_service=None, publish: bool = False) -> dict:
    lesson_id = entry["lesson_id"]
    book_id = entry["book_id"]
    progress("PRODUCTION_PIPELINE_START", lesson_id=lesson_id)

    if lesson_id == "G07-PHYSICS-001" and publish:
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
    ev_map = build_evidence_map(doc, entry)
    doc.close()

    theory = synthesize_universal_pedagogy(entry, ev_map, profile)
    exercises = ev_map["exercise_evidence"]

    page_a = render_lesson_page_a(entry, theory, ev_map)
    page_b = render_lesson_page_b(entry, exercises, profile, ev_map)

    slug_subj = re.sub(r'[^\w]+', '-', entry.get("subject", "PHYSICS")).upper()
    slug_title = re.sub(r'[^\w]+', '-', entry["canonical_title"]).upper()
    seq_match = re.search(r'-(\d{3})$', lesson_id)
    seq_str = seq_match.group(1) if seq_match else "001"
    grade_str = f"G{int(entry.get('grade', 7)):02d}"

    filename_a = f"{grade_str}-{slug_subj}--{seq_str}--{slug_title}.html"
    filename_b = f"{grade_str}-{slug_subj}--{seq_str}--{slug_title}--EXERCISES.html"

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
        Image.new("RGB", (16, 16), "white").save(sample, format="PNG")
        progress("AI_VISION_PROBE_START", image="generated_blank_16x16")
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
