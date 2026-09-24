"""
NABIL AI — Enterprise Autonomous Lesson Factory (Universal Multi-Disciplinary Engine)
Automates the lifecycle: Drive PDF Ingestion -> Verification -> Interactive HTML + PPTX Generation -> Drive Publishing.
"""

import argparse
import base64
import hashlib
import html
import io
import json
import os
import re
import signal
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data/interactive_lesson_production_ledger.json"
FOLDER_MIME = "application/vnd.google-apps.folder"
ROOT_FOLDER = os.getenv("NABIL_INTERACTIVE_CURRICULUM_ROOT_ID",
                        os.getenv("NABIL_LESSON_DRIVE_ROOT",
                                  "16bcmZMO_dn4FqlGaDtl8Hky6iSBEqZpX"))
RUN_DEADLINE = None
BOOK_DEADLINE = None
PROGRESS_STARTED = None

NABIL_OFFICIAL_AVATAR_B64 = (
    "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"
)


def now():
    return datetime.now(timezone.utc).isoformat()


def progress(stage, **details):
    elapsed = round(time.monotonic() - PROGRESS_STARTED, 1) if PROGRESS_STARTED else 0
    print(json.dumps({"time": now(), "elapsed_seconds": elapsed, "stage": stage, **details}, ensure_ascii=False), flush=True)


def bounded(command, seconds, **kwargs):
    remaining = min([seconds, *([RUN_DEADLINE - time.monotonic()] if RUN_DEADLINE else []),
                     *([BOOK_DEADLINE - time.monotonic()] if BOOK_DEADLINE else [])])
    if remaining <= 0:
        raise TimeoutError("RUN_DEADLINE_EXCEEDED")
    process = subprocess.Popen(command, start_new_session=True, **kwargs)
    try:
        out, err = process.communicate(timeout=remaining)
    except BaseException:
        os.killpg(process.pid, signal.SIGKILL)
        process.communicate()
        raise
    if process.returncode:
        raise subprocess.CalledProcessError(process.returncode, command, output=out, stderr=err)
    return out


def vision_page_text(image, page):
    from openai import OpenAI
    models = {
        "openai": os.getenv("OPENAI_VISION_MODEL", "gpt-4.1-mini"),
        "gemini": os.getenv("GEMINI_VISION_MODEL", "gemini-2.5-flash"),
        "openrouter": os.getenv("OPENROUTER_VISION_MODEL", "openrouter/free"),
        "groq": os.getenv("GROQ_VISION_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct"),
    }
    errors = []
    for provider, key, base, _ in configured_providers():
        remaining = min([20, *([RUN_DEADLINE - time.monotonic()] if RUN_DEADLINE else []),
                         *([BOOK_DEADLINE - time.monotonic()] if BOOK_DEADLINE else [])])
        if remaining <= 0:
            raise TimeoutError("VISION_DEADLINE_EXCEEDED")
        try:
            response = OpenAI(api_key=key, base_url=base, timeout=remaining, max_retries=0
                ).chat.completions.create(
                    model=models[provider],
                    messages=[{"role": "user", "content": [
                        {"type": "text", "text": "Transcribe ALL visible textbook text in reading order. Preserve titles, geometric labels, exercises, sub-questions (a,b,c,d,e) and formulas accurately."},
                        {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + base64.b64encode(image).decode()}}
                    ]}])
            text = (response.choices[0].message.content or "").strip()
            if len(text) >= 80:
                progress("VISION_OK", page=page, provider=provider, characters=len(text))
                return text
            errors.append(provider + ":INSUFFICIENT_TEXT")
        except Exception as exc:
            errors.append(provider + ":" + type(exc).__name__)
    raise ValueError(f"OCR_AND_VISION_FAILED_PAGE_{page}: " + ",".join(errors))


def owner_drive():
    names = ("GOOGLE_DRIVE_OAUTH_CLIENT_ID", "GOOGLE_DRIVE_OAUTH_CLIENT_SECRET", "GOOGLE_DRIVE_OAUTH_REFRESH_TOKEN")
    values = [os.getenv(name, "").strip() for name in names]
    if not all(values):
        raise RuntimeError("OWNER_OAUTH_REQUIRED: missing " +
                           ",".join(name for name, value in zip(names, values) if not value))
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    creds = Credentials(token=None, refresh_token=values[2],
                        token_uri="https://oauth2.googleapis.com/token",
                        client_id=values[0], client_secret=values[1],
                        scopes=["https://www.googleapis.com/auth/drive"])
    creds.refresh(Request())
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def download(service, file_id):
    from googleapiclient.http import MediaIoBaseDownload
    output = io.BytesIO()
    loader = MediaIoBaseDownload(output, service.files().get_media(fileId=file_id))
    finished = False
    while not finished:
        _, finished = loader.next_chunk()
        if output.tell() > 80_000_000:
            raise ValueError("SOURCE_PDF_TOO_LARGE")
    return output.getvalue()


def download_pdf_to_path(service, file_id, path):
    from googleapiclient.http import MediaIoBaseDownload
    with path.open("wb") as target:
        loader = MediaIoBaseDownload(target, service.files().get_media(fileId=file_id))
        finished = False
        while not finished:
            _, finished = loader.next_chunk()


def ocr_pdf(raw, page_indices, vision_on_failure=False):
    with tempfile.TemporaryDirectory(prefix="nabil_toc_") as directory:
        pdf = Path(directory) / "source.pdf"
        if isinstance(raw, Path):
            pdf = raw
        else:
            pdf.write_bytes(raw)
        result = {}
        for index in page_indices:
            if (RUN_DEADLINE and time.monotonic() >= RUN_DEADLINE
                or BOOK_DEADLINE and time.monotonic() >= BOOK_DEADLINE):
                raise TimeoutError("OCR_BUDGET_EXCEEDED")
            prefix = str(Path(directory) / f"page_{index}")
            progress("SOURCE_RENDER", page=index + 1)
            bounded(["pdftoppm", "-f", str(index + 1), "-l", str(index + 1),
                     "-singlefile", "-r", "140", "-jpeg", str(pdf), prefix],
                    8, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            progress("OCR", page=index + 1)
            try:
                text = bounded(["tesseract", prefix + ".jpg", "stdout", "-l", "eng+fra+ara"],
                               7, stdout=subprocess.PIPE, stderr=subprocess.PIPE).decode("utf-8", "replace").strip()
            except subprocess.TimeoutExpired:
                progress("OCR_TIMEOUT_VISION", page=index + 1)
                text = (vision_page_text(Path(prefix + ".jpg").read_bytes(), index + 1)
                        if vision_on_failure else "")
            if len(text) < 80 and vision_on_failure:
                progress("OCR_INSUFFICIENT_VISION", page=index + 1)
                text = vision_page_text(Path(prefix + ".jpg").read_bytes(), index + 1)
            result[index] = text
            progress("SOURCE_PAGE_READY", page=index + 1, characters=len(text))
        return result


def trustworthy_title(title):
    words = re.findall(r"[A-Za-zÀ-ÿ\u0600-\u06FF]+", str(title))
    if (not words or len(title) > 90 or
        re.search(r"\.(?:pdf|jpg|png)|^(?:img|screenshot)[_ -]|^\d+$", title, re.I) or
        title.casefold().strip() in {"introduction", "foreword", "préface", "livre"}):
        return False
    return len(words) > 1 or len(words[0]) >= 4


def visual_chapter_starts(pdf, total_pages, toc_text):
    from PIL import Image, ImageEnhance, ImageOps
    chapters = []
    with tempfile.TemporaryDirectory(prefix="nabil_headers_") as directory:
        for index in range(8, min(total_pages, 50)):
            if BOOK_DEADLINE and time.monotonic() >= BOOK_DEADLINE:
                raise TimeoutError("BOOK_DISCOVERY_BUDGET_EXCEEDED")
            progress("HEADER_SCAN", page=index + 1)
            prefix = str(Path(directory) / "page")
            bounded(["pdftoppm", "-f", str(index + 1), "-l", str(index + 1),
                     "-singlefile", "-r", "150", "-jpeg", str(pdf), prefix],
                    8, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            picture = Image.open(prefix + ".jpg")
            band = picture.crop((0, 0, picture.width, int(picture.height * .19)))
            ImageEnhance.Contrast(ImageOps.grayscale(band)).enhance(2).save(prefix + "_top.png")
            try:
                title_band = bounded(
                    ["tesseract", prefix + "_top.png", "stdout", "-l", "eng+fra+ara", "--psm", "6"],
                    5, stdout=subprocess.PIPE, stderr=subprocess.PIPE).decode("utf-8", "replace")
            except subprocess.TimeoutExpired:
                progress("HEADER_OCR_TIMEOUT", page=index + 1)
                title_band = ""
            found = re.search(r"(?:\b(?:chapter|chapitre|فصل|باب)\s*|^\W*)"
                              r"(\d{1,2})\s*[:.\-]\s*"
                              r"([A-Za-z\u0600-\u06FF][A-Za-z\u0600-\u06FF '&\-]{3,65})", title_band, re.I | re.M)
            if not found:
                continue
            number, title = int(found.group(1)), found.group(2).strip(" .-")
            if not trustworthy_title(title):
                progress("TITLE_REJECTED_OCR_FRAGMENT", page=index + 1, title=title)
                continue
            words = re.findall(r"[A-Za-z\u0600-\u06FF]{3,}", title.lower())
            if not words or sum(bool(re.search(r"\b" + re.escape(w) + r"\b",
                                              toc_text, re.I)) for w in words) < max(1, len(words) - 1):
                continue
            if chapters and (number <= chapters[-1][2] or index - chapters[-1][0] < 2):
                continue
            chapters.append((index, title, number))
            if len(chapters) >= 2 and chapters[1][0] - chapters[0][0] <= 16:
                break
    return [(title, start, chapters[i + 1][0] if i + 1 < len(chapters)
             else min(start + 8, total_pages))
            for i, (start, title, _) in enumerate(chapters)
            if 2 <= (chapters[i + 1][0] if i + 1 < len(chapters)
                     else min(start + 8, total_pages)) - start <= 16]


def candidates(reader, raw):
    page_text = [(page.extract_text() or "") for page in reader.pages]
    entries = []

    def walk(nodes):
        for node in nodes:
            if isinstance(node, list):
                walk(node)
            elif getattr(node, "title", None):
                try:
                    page = reader.get_destination_page_number(node)
                    if page >= 0:
                        entries.append((str(node.title).strip(), page))
                except Exception:
                    continue

    walk(reader.outline)
    if len(entries) >= 2:
        ordered = sorted({(p, t) for t, p in entries
                          if p > 0 and trustworthy_title(t)
                          and not re.search(r"\.(?:pdf|jpg|png)|^(?:img|screenshot)[_ -]|livre$", t, re.I)})
        if len(ordered) >= 2:
            return [(title, start, ordered[i + 1][0] if i + 1 < len(ordered)
                     else min(start + 8, len(page_text)))
                    for i, (start, title) in enumerate(ordered)
                    if 2 <= (ordered[i + 1][0] if i + 1 < len(ordered) else min(start + 8, len(page_text))) - start <= 16]

    front = range(min(12, len(page_text)))
    if sum(len(page_text[i]) for i in front) < 700:
        front_ocr = ocr_pdf(raw, front)
        for i, t in front_ocr.items():
            page_text[i] = t
    if isinstance(raw, Path):
        visual = visual_chapter_starts(raw, len(page_text), " ".join(page_text[:12]))
        if visual:
            return visual

    toc_lines = "\n".join(page_text[:min(12, len(page_text))]).splitlines()
    chapter_titles = []
    for i, line in enumerate(toc_lines):
        match = re.search(r"\b(?:chapter|chapitre|فصل)\s*(\d+)\s*:\s*(.*)", line, re.I)
        if not match:
            continue
        title = match.group(2).strip(" -:.") or next(
            (x.strip(" -:.") for x in toc_lines[i + 1:i + 4] if len(x.strip()) > 5), "")
        if trustworthy_title(title):
            chapter_titles.append((int(match.group(1)), title))
    if chapter_titles:
        probe = range(12, min(len(page_text), 65))
        matches = []
        for n, title in chapter_titles:
            words = [w for w in re.findall(r"[A-Za-z\u0600-\u06FF]{3,}", title.casefold())
                     if w not in {"chapter", "chapitre"}]
            if not words:
                continue
            found = [i for i in probe if
                     re.search(rf"\b(?:chapter|chapitre|فصل)\s*{n}\b", page_text[i][:750], re.I)
                     and sum(w in page_text[i][:1000].casefold() for w in words)
                     >= max(1, len(words) - 1)]
            if len(found) == 1:
                matches.append((found[0], title))
        ordered = sorted(set(matches))
        if ordered:
            return [(title, start, ordered[j + 1][0] if j + 1 < len(ordered)
                     else min(start + 8, len(page_text)))
                    for j, (start, title) in enumerate(ordered)
                    if 2 <= (ordered[j + 1][0] if j + 1 < len(ordered)
                             else min(start + 8, len(page_text))) - start <= 16]
    toc = " ".join(page_text[:min(12, len(page_text))])
    if not re.search(r"\bcontents\b|\bsommaire\b|فهرس", toc, re.I):
        raise ValueError("SOURCE_TOC_NOT_FOUND")
    lines = "\n".join(page_text[:min(12, len(page_text))]).splitlines()
    found = []
    for line in lines:
        m = re.match(r"\s*(?:\d+[.)-]?\s+)?([\w\s,:'’()\-/]{5,85}?)\s*(?:\.{2,}|\s{2,})\s*(\d{1,3})\s*$", line)
        if not m:
            continue
        title = m.group(1).strip(" .-")
        if not trustworthy_title(title):
            continue
        matches = [i for i, text in enumerate(page_text[5:], 5) if re.search(re.escape(title), text[:1600], re.I)]
        if len(matches) == 1:
            found.append((matches[0], title))
    ordered = sorted(set(found))
    if len(ordered) < 2:
        raise ValueError("SOURCE_TOC_AMBIGUOUS: cannot locate two distinct lesson starts")
    return [(title, start, ordered[i + 1][0] if i + 1 < len(ordered)
             else min(start + 8, len(page_text))) for i, (start, title) in enumerate(ordered)]


def lesson_key(book, title, start):
    return hashlib.sha256(f"{book['drive_file_id']}|{start}".encode()).hexdigest()[:20]


def visual_candidates(images):
    providers = configured_providers()
    if len({p[0] for p in providers}) < 3:
        raise RuntimeError("THREE_INDEPENDENT_PROVIDERS_REQUIRED")
    from openai import OpenAI
    selected = os.getenv("NABIL_VISUAL_PROVIDER", "").strip().lower()
    reserved_reviewer = os.getenv("NABIL_REVIEWER_PROVIDER", "").strip().lower()
    choices = [p for p in providers if p[0] != reserved_reviewer and (not selected or p[0] == selected)]
    if not choices:
        raise RuntimeError("VISUAL_EXTRACTOR_UNAVAILABLE")
    name, key, base, default_model = choices[0]
    model = os.getenv("NABIL_VISUAL_MODEL", default_model)
    if not model:
        raise RuntimeError("VISUAL_MODEL_NOT_CONFIGURED")
    client = OpenAI(api_key=key, base_url=base, timeout=45, max_retries=0)
    candidates = {}
    extraction_failures = []
    for page, image in images.items():
        messages = [
            {"role": "system", "content": (
                "Describe only visible figures, graphs, circuits, apparatus, chemical structures, and "
                "geometry on this textbook page. Identify a printed figure label if visible; "
                "otherwise use a short location description. Return JSON {items:[{figure_id:string, observation:string, "
                "accompanying_question:string}]}.")},
            {"role": "user", "content": [
                {"type": "text", "text": f"PDF page {page}; extract tentative visual observations."},
                {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + base64.b64encode(image).decode("ascii")}}]},
        ]
        try:
            response = client.chat.completions.create(model=model, temperature=0,
                response_format={"type": "json_object"}, messages=messages)
            data = parse_provider_json(client, name, messages, response, model)
            items = data.get("items", [])
            if not isinstance(items, list):
                continue
            for index, item in enumerate(items[:30], 1):
                if not isinstance(item, dict):
                    continue
                observation = item.get("observation")
                figure = item.get("figure_id")
                if not isinstance(observation, str) or not observation.strip():
                    continue
                if not isinstance(figure, str) or not figure.strip():
                    continue
                candidates[f"P{page}-VIS-{index}"] = {
                    "page": page, "type": "visual_candidate", "figure_id": figure,
                    "text": observation.strip(),
                    "accompanying_question": str(item.get("accompanying_question", "")),
                    "verified": False,
                }
        except Exception as exc:
            progress("VISUAL_CANDIDATE_EXTRACTION_FAILED", page=page, error_type=type(exc).__name__)
            extraction_failures.append(f"{page}:{type(exc).__name__}")
            if type(exc).__name__ == "RateLimitError":
                break
    if extraction_failures:
        raise RuntimeError("VISUAL_CANDIDATE_EXTRACTION_FAILED: " + ",".join(extraction_failures))
    return candidates, name, model


def evidence_catalog(pages, candidates=None):
    catalog = {}
    for page, text in pages:
        chunks = re.split(r"\n\s*\n", text)
        if len(chunks) < 3:
            chunks = text.splitlines()
        buffer = ""
        serial = 0
        for part in chunks:
            part = part.strip()
            if not part:
                continue
            if len(buffer) + len(part) < 220:
                buffer += (("\n" if buffer else "") + part)
                continue
            if buffer:
                serial += 1
                catalog[f"P{page}-{serial}"] = {"page": page, "text": buffer}
                buffer = ""
            while len(part) > 320:
                serial += 1
                catalog[f"P{page}-{serial}"] = {"page": page, "text": part[:300]}
                part = part[300:]
            buffer = part
        if buffer:
            serial += 1
            catalog[f"P{page}-{serial}"] = {"page": page, "text": buffer}
    catalog.update(candidates or {})
    return catalog


def source_evidence_map(title, pages, catalog, visual_provider=None, visual_model=None):
    patterns = {
        "objectives": r"objectives?|learn|aims?|buts?|أهداف|كفاءات",
        "definitions": r"defined|is called|is a |are called|consists of|définition|تعريف",
        "laws": r"formula|law|loi|horizontal|equal|unit|measure|=|proportional|قانون|علاقة",
        "examples": r"example|for instance|e\.g\.|مثال",
        "activities": r"activity|experiment|activité|expérience|observe|try|place|take a|نشاط|تجربة",
        "figures": r"figure|fig\.|draw|diagram|vessel|surface|schéma|شكل|رسم",
        "exercises": r"exercise|exercices?|calculate|complete|explain|question|problème|تمرين|مسألة",
        "symbols_units": r"\b(?:cm|mm|kg|g|mL|L|N|V|A|Ω|dioptries?|δ)\b|symbol|units?|وحدة",
    }
    categories = {name: [key for key, entry in catalog.items() if re.search(pattern, entry["text"], re.I)]
                  for name, pattern in patterns.items()}
    exercise_starts = exercise_section_pages(pages)
    exercise_pages = [page for page, _ in pages if exercise_starts and page >= min(exercise_starts)]
    exercise_evidence_map = [{
        "pdf_page": page,
        "ocr_text": dict(pages)[page],
        "visual_candidate_ids": [key for key, entry in catalog.items()
                                 if entry.get("type") == "visual_candidate" and entry["page"] == page],
        "status": "unverified_source_candidates",
    } for page in exercise_pages]
    return {"title": title, "source_pdf_pages": [page for page, _ in pages],
            "categories": categories, "evidence": catalog,
            "exercise_evidence_map": exercise_evidence_map,
            "visual_extractor_provider": visual_provider,
            "visual_extractor_model": visual_model,
            "visual_evidence_status": "unverified_candidates"}


def record_role_provenance(evidence_map, attempt, role, provider, model):
    if role not in ("generator", "visual_extractor", "reviewer"):
        raise ValueError("UNKNOWN_PROVENANCE_ROLE")
    for suffix, value in (("provider", provider), ("model", model)):
        key = f"{role}_{suffix}"
        evidence_map[key] = value
        attempt[key] = value


def attach_evidence(lesson, catalog):
    if lesson.get("introduction_evidence_id") in catalog:
        entry = catalog[lesson["introduction_evidence_id"]]
        lesson["introduction_source_page"] = entry["page"]
        lesson["introduction_source_quote"] = entry["text"]
    for section in ("concepts", "activities", "questions", "exercises", "summary"):
        for item in lesson.get(section, []):
            evidence = catalog.get(str(item.get("evidence_id", "")))
            if evidence:
                item["pdf_page"] = evidence["page"]
                item["source_quote"] = evidence["text"]
                if evidence.get("type") == "visual_candidate":
                    item["unverified_visual_candidate"] = {
                        "figure_id": evidence["figure_id"],
                        "observation": evidence["text"],
                        "accompanying_question": evidence["accompanying_question"]}


def source_excerpt(reader, raw, start, end):
    if end <= start or end - start > 14:
        raise ValueError("SOURCE_BOUNDARY_AMBIGUOUS")
    pages = [(i + 1, (reader.pages[i].extract_text() or "").strip()) for i in range(start, end)]
    for number, text in pages:
        if len(text) >= 80:
            progress("SOURCE_TEXT", page=number, characters=len(text))
    missing = [i for i in range(start, end) if len(pages[i - start][1]) < 80]
    if missing:
        scanned = ocr_pdf(raw, missing, vision_on_failure=True)
        pages = [(i + 1, scanned.get(i, pages[i - start][1])) for i in range(start, end)]
    if sum(len(t) for _, t in pages) < 1100:
        raise ValueError("SOURCE_TEXT_INSUFFICIENT_OR_SCANNED")
    if sum(len(t) for _, t in pages) > 42000:
        raise ValueError("SOURCE_TOO_LONG_FOR_VERIFIABLE_GENERATION")
    return pages


def parse_provider_json(client, provider, messages, response, model):
    content = response.choices[0].message.content
    if content is None and provider == "openrouter":
        retry = client.chat.completions.create(
            model=model, temperature=0,
            messages=[{"role": "system", "content": "Return a valid JSON object only."}, *messages])
        content = retry.choices[0].message.content
    if not isinstance(content, str) or not content.strip():
        raise ValueError(provider.upper() + "_EMPTY_RESPONSE")
    value = content.strip()
    if value.startswith("```"):
        value = re.sub(r"^```(?:json)?\s*|\s*```$", "", value, flags=re.I).strip()
    result = json.loads(value)
    if not isinstance(result, dict):
        raise ValueError(provider.upper() + "_NON_OBJECT_RESPONSE")
    return result


def generate(title, pages, language, evidence_map, previous_failures=None, visual_provider=None, visual_model=None):
    from openai import OpenAI
    catalog = evidence_map["evidence"]
    source = json.dumps(evidence_map, ensure_ascii=False)
    messages = [
            {"role": "system", "content": (
                "You are NABIL AI Master Class Architect. Create a rich, authoritative, source-grounded classroom lesson.\n"
                "Return JSON with keys:\n"
                "- title, introduction, introduction_evidence_id\n"
                "- concepts (array: heading, explanation, formula [or null], evidence_id, visual_evidence_id, svg_diagram [vector SVG])\n"
                "- activities (array: prompt, observation, conclusion, evidence_id, visual_evidence_id, svg_diagram)\n"
                "- live_lab: object defining an interactive simulation: {title, description, controls: [{id, label, type, min, max, value}], initial_svg, js_update_fn}\n"
                "- exercises (array: exercise_number, prompt, concept_tested, given_data, figure_number, solution_steps, solution, final_answer, diagram_svg [inline SVG], evidence_id, external_scientific_knowledge)\n"
                "- worksheet (array of evaluative questions: question_number, prompt, type [numeric/select/text], expected_answer, tolerance, unit, hint, explanation)\n"
                "- summary_card: {\n"
                "    title: str,\n"
                "    estimated_time: str,\n"
                "    learning_objectives: str,\n"
                "    left_panel: { heading: str, formula: str, properties: [{label: str, value: str}], rule_summary: str },\n"
                "    center_panel: { title: str, svg_diagram: str, secondary_block: { title: str, html_content: str } },\n"
                "    quick_check: { prompt: str, expected_answer: str, hint: str }\n"
                "  }\n"
                "\n"
                "MANDATORY SCIENTIFIC & VISUAL RULES FOR ALL SUBJECTS:\n"
                "1. EXHAUSTIVE EXERCISE COVERAGE: Every single numbered textbook exercise and ALL its sub-questions (a, b, c, d, e) MUST be fully transcribed and solved step-by-step. Do not omit any sub-question.\n"
                "2. COLOR-CODED GEOMETRIC & PHYSICAL DIAGRAMS:\n"
                "   - Base/Given elements MUST be drawn in solid Cyan/Blue ('#8ce9ff' or '#ffffff').\n"
                "   - Auxiliary lines/constructions added during the proof MUST be drawn in DASHED Yellow/Orange ('#ffe49a' with 'stroke-dasharray=\"5,4\"').\n"
                "   - Target angles/segments/results proved MUST be drawn in Emerald Green ('#31d9a8').\n"
                "   - Include a concise SVG color legend at the top of the diagram.\n"
                "3. MATHEMATICAL TYPOGRAPHY:\n"
                "   Use standard LaTeX delimiters: '$...$' for inline math and '$$...$$' for display equations so KaTeX renders them perfectly.\n"
                "4. All SVGs must be responsive ('viewBox=\"0 0 W H\"')."
            )},
            {"role": "user", "content": f"Language: {language}; Lesson Title: {title}\nEvidence Map:\n{source}"},
        ]
    if previous_failures:
        messages.append({"role": "user", "content": (
            "The independent reviewer REJECTED the previous draft with errors:\n"
            + json.dumps(previous_failures, ensure_ascii=False))})
    errors = []
    reserved_reviewer = os.getenv("NABIL_REVIEWER_PROVIDER", "").strip().lower()
    eligible = [(provider, api_key, base_url, os.getenv("NABIL_LESSON_MODEL", model))
                for provider, api_key, base_url, model in configured_providers()
                if provider not in (visual_provider, reserved_reviewer)
                and os.getenv("NABIL_LESSON_MODEL", model) != visual_model]
    if not eligible:
        raise RuntimeError("INDEPENDENT_REVIEWER_UNAVAILABLE")
    for provider, api_key, base_url, chosen_model in eligible:
        try:
            client = OpenAI(api_key=api_key, base_url=base_url, timeout=120, max_retries=0)
            response = client.chat.completions.create(
                model=chosen_model, temperature=0, response_format={"type": "json_object"}, messages=messages)
            result = parse_provider_json(client, provider, messages, response, chosen_model)
            if result.get("error"):
                raise ValueError("GENERATION_REFUSED: " + str(result["error"])[:200])
            attach_evidence(result, catalog)
            return result, provider, chosen_model
        except Exception as exc:
            errors.append(f"{provider}: {type(exc).__name__}: {str(exc)[:180]}")
    raise RuntimeError("ALL_CONFIGURED_PROVIDERS_FAILED: " + " | ".join(errors))


def configured_providers():
    cloudflare_account = os.getenv("CLOUDFLARE_ACCOUNT_ID", "").strip()
    options = {
        "groq": ("GROQ_API_KEY", "[https://api.groq.com/openai/v1](https://api.groq.com/openai/v1)", os.getenv("GROQ_TEXT_MODEL", "openai/gpt-oss-120b")),
        "openrouter": ("OPENROUTER_API_KEY", "[https://openrouter.ai/api/v1](https://openrouter.ai/api/v1)", os.getenv("OPENROUTER_TEXT_MODEL", "openrouter/free")),
        "gemini": ("GEMINI_API_KEY", "[https://generativelanguage.googleapis.com/v1beta/openai/](https://generativelanguage.googleapis.com/v1beta/openai/)", os.getenv("GEMINI_TEXT_MODEL", "gemini-2.5-flash")),
        "cloudflare": ("CLOUDFLARE_API_TOKEN", f"[https://api.cloudflare.com/client/v4/accounts/](https://api.cloudflare.com/client/v4/accounts/){cloudflare_account}/ai/v1", os.getenv("CLOUDFLARE_TEXT_MODEL", "@cf/google/gemma-4-26b-a4b-it")),
        "openai": ("OPENAI_API_KEY", None, os.getenv("OPENAI_TEXT_MODEL", "gpt-4.1-mini")),
    }
    order = os.getenv("NABIL_AI_PROVIDER_ORDER", "groq,openrouter,gemini,openai")
    result = []
    names = dict.fromkeys([*(x.strip().lower() for x in order.split(",")), "groq", "openrouter", "gemini", "cloudflare", "openai"])
    for name in names:
        if name not in options:
            continue
        env, base, model = options[name]
        if name == "cloudflare" and not cloudflare_account:
            continue
        if name == "openai" and os.getenv("NABIL_LESSON_ALLOW_PAID_OPENAI") != "1":
            continue
        if os.getenv(env, "").strip():
            result.append((name, os.environ[env], base, model))
    return result


def exercise_section_pages(pages):
    heading = re.compile(r"^\s*(?:exercises?|exercices?|problems?|تمارين|تدريبات|مسائل)\s*[:：]?(?:\s*\d{1,3}[.)]?\s+[^\n]*)?\s*$", re.I | re.M)
    return [page for page, source in pages if heading.search(source)]


def verify_exercise_diagrams(lesson_data):
    errors = []
    visual_triggers = re.compile(
        r"\b(draw|trace|tracer|dessiner|représenter|schématiser|construct|graph|plot|"
        r"figure|fig\.|circuit|ray|prisme|périscope|lentille|miroir|force|vecteur|"
        r"courbe|tableau|arbre|forme|erlenmeyer|tube|angle|triangle|cercle|tangent|tangente|plane|plan|"
        r"ارسم|خطط|مثل|حدد مسار|الشكل|دارة|شعاع|موشور|قوة|متجهة|منحنى|مماس|دائرة|مستوي)\b",
        re.I
    )
    exercises = lesson_data.get("exercises", [])
    for ex in exercises:
        ex_num = ex.get("exercise_number", "?")
        prompt = str(ex.get("prompt", ""))
        solution = str(ex.get("solution", ""))
        full_text = prompt + " " + solution
        needs_diagram = bool(visual_triggers.search(full_text)) or (ex.get("figure_number") is not None)
        if needs_diagram:
            svg = str(ex.get("diagram_svg", "")).strip()
            if not svg or not ("<svg" in svg and "</svg>" in svg):
                errors.append(f"EXERCISE_{ex_num}_MISSING_REQUIRED_TECHNICAL_SVG")
            elif "viewBox" not in svg:
                errors.append(f"EXERCISE_{ex_num}_SVG_NOT_RESPONSIVE_MISSING_VIEWBOX")
    return errors


def check_content(lesson, title, pages, catalog):
    errors = []
    if re.sub(r"\W+", "", str(lesson.get("title", "")).casefold()) != re.sub(r"\W+", "", title.casefold()):
        errors.append("TITLE_MISMATCH")
    requirements = (("concepts", 2), ("activities", 2), ("exercises", 2))
    for field, minimum in requirements:
        if not isinstance(lesson.get(field), list) or len(lesson[field]) < minimum:
            errors.append("INSUFFICIENT_" + field.upper())
    exercise_pages = exercise_section_pages(pages)
    first_exercise_page = min(exercise_pages) if exercise_pages else None
    if first_exercise_page is None:
        errors.append("NUMBERED_EXERCISES_NOT_LOCATED")

    for section in ("concepts", "activities", "exercises"):
        for i, item in enumerate(lesson.get(section, [])):
            try:
                page = int(item["pdf_page"])
                evidence = catalog[item["evidence_id"]]
                if evidence["page"] != page:
                    raise ValueError()
                if section == "activities" and (len(str(item.get("observation", ""))) < 10 or len(str(item.get("conclusion", ""))) < 10):
                    raise ValueError()
                if section == "exercises" and (len(str(item.get("prompt", ""))) < 10 or len(str(item.get("solution", ""))) < 15):
                    raise ValueError()
            except (ValueError, KeyError, TypeError, IndexError):
                errors.append(f"UNVERIFIED_{section}_{i+1}")

    if not lesson.get("live_lab") or not isinstance(lesson["live_lab"], dict):
        errors.append("LIVE_LAB_MISSING")

    worksheet = lesson.get("worksheet", [])
    if not isinstance(worksheet, list) or len(worksheet) < 3:
        errors.append("INTERACTIVE_WORKSHEET_INSUFFICIENT")

    diagram_errors = verify_exercise_diagrams(lesson)
    errors.extend(diagram_errors)
    return errors


def repair_source_quotes(lesson, pages, catalog, failures, generator_provider):
    from openai import OpenAI
    targets = []
    for failure in failures:
        found = re.fullmatch(r"UNVERIFIED_(concepts|activities|exercises)_(\d+)", failure)
        if found:
            section, index = found.group(1), int(found.group(2)) - 1
            targets.append({"section": section, "index": index, "item": lesson[section][index]})
    if not targets:
        return False
    source = json.dumps(catalog, ensure_ascii=False)
    for provider, key, base, model in configured_providers():
        if provider != generator_provider:
            continue
        try:
            client = OpenAI(api_key=key, base_url=base, timeout=35, max_retries=0)
            messages = [
                {"role": "system", "content": "Repair source citation evidence_ids for these items from the catalog. Return JSON {repairs:[{section,index,evidence_id}]}."},
                {"role": "user", "content": json.dumps({"source": source, "targets": targets}, ensure_ascii=False)},
            ]
            response = client.chat.completions.create(
                    model=os.getenv("NABIL_LESSON_MODEL", model), temperature=0, response_format={"type": "json_object"}, messages=messages)
            data = parse_provider_json(client, provider, messages, response, os.getenv("NABIL_LESSON_MODEL", model))
            allowed = {(x["section"], x["index"]) for x in targets}
            repaired = 0
            for fix in data.get("repairs", []):
                section, index = fix.get("section"), fix.get("index")
                if (section, index) not in allowed:
                    continue
                evidence_id = str(fix.get("evidence_id", ""))
                if evidence_id in catalog:
                    lesson[section][index]["evidence_id"] = evidence_id
                    repaired += 1
            attach_evidence(lesson, catalog)
            return repaired > 0
        except Exception:
            pass
    return False


def independent_reviewer(generator_provider, generator_model, visual_provider, visual_model):
    if not visual_provider or not visual_model or visual_provider == generator_provider:
        raise RuntimeError("INDEPENDENT_REVIEWER_UNAVAILABLE")
    candidates = [p for p in configured_providers() if p[0] not in (generator_provider, visual_provider)]
    selected = os.getenv("NABIL_REVIEWER_PROVIDER", "").strip().lower()
    if selected:
        candidates = [p for p in candidates if p[0] == selected]
    if not candidates:
        raise RuntimeError("INDEPENDENT_REVIEWER_UNAVAILABLE")
    name, key, base, default_model = candidates[0]
    model = os.getenv("NABIL_LESSON_REVIEW_MODEL", "").strip() or default_model
    if model in (generator_model, visual_model):
        raise RuntimeError("INDEPENDENT_REVIEWER_UNAVAILABLE")
    return name, key, base, model


def review_page_claims(client, provider, model, page, image, page_text, claims, exercise_coverage=False):
    payload = {"pdf_page": page, "ocr": page_text, "claims": claims, "exercise_coverage_required": exercise_coverage}
    messages = [{"role": "system", "content": (
        "You are an independent skeptical science reviewer. Audit each claim, exercise, formula, "
        "and SVG diagram against the original textbook page image. Verify that diagrams match "
        "geometric and physical facts without invention, and verify that auxiliary constructions "
        "are clearly distinguished from given data. Return JSON {verdicts:[{id:string,approved:boolean,specific_reason:string}], "
        "exercise_coverage:{approved:boolean,specific_reason:string}}."
    )},
        {"role": "user", "content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False)},
                                      {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + base64.b64encode(image).decode("ascii")}}]}]
    response = client.chat.completions.create(model=model, temperature=0, response_format={"type": "json_object"}, messages=messages)
    result = parse_provider_json(client, provider, messages, response, model)
    verdicts = result.get("verdicts", [])
    found = {v["id"]: v for v in verdicts if isinstance(v, dict) and "id" in v}
    coverage = result.get("exercise_coverage", {"approved": True, "specific_reason": "ok"})
    return found, coverage


def scientific_review(lesson, pages, images, generator_provider, generator_model, visual_provider, visual_model, catalog=None):
    from openai import OpenAI
    try:
        name, key, base, model = independent_reviewer(generator_provider, generator_model, visual_provider, visual_model)
        client = OpenAI(api_key=key, base_url=base, timeout=90, max_retries=0)
        by_page = {page: [] for page, _ in pages}

        for section in ("concepts", "activities", "exercises"):
            for index, item in enumerate(lesson.get(section, []), 1):
                p = item.get("pdf_page")
                if p in by_page:
                    by_page[p].append({"id": f"{section}_{index}", "claim": item})

        exercise_starts = exercise_section_pages(pages)
        for page, source in pages:
            claims = by_page[page]
            cov_req = bool(exercise_starts and page >= min(exercise_starts))
            if not claims and not cov_req:
                continue
            found, coverage = review_page_claims(client, name, model, page, images[page], source, claims, cov_req)
            for c in claims:
                v = found.get(c["id"])
                if not v or not v.get("approved"):
                    reason = v.get("specific_reason", "Unverified claim") if v else "Missing verdict"
                    return {"pass": False, "reviewer": name, "model": model, "errors": [f"{c['id']}:{reason}"]}
            if cov_req and not coverage.get("approved"):
                return {"pass": False, "reviewer": name, "model": model, "errors": [f"coverage_p{page}:{coverage.get('specific_reason')}"]}

        return {"pass": True, "reviewer": name, "model": model, "errors": []}
    except Exception as exc:
        return {"pass": False, "reviewer": None, "model": None, "errors": ["REVIEW_FAILED: " + str(exc)[:150]]}


def source_images(pdf, pages):
    result = {}
    with tempfile.TemporaryDirectory(prefix="nabil_figures_") as directory:
        for number, _ in pages:
            prefix = str(Path(directory) / f"p{number}")
            subprocess.run(["pdftoppm", "-f", str(number), "-l", str(number),
                            "-singlefile", "-scale-to", "1100", "-jpeg",
                            "-jpegopt", "quality=72", str(pdf), prefix],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=45)
            image = Path(prefix + ".jpg").read_bytes()
            if len(image) < 5000:
                raise ValueError("SOURCE_PAGE_RENDER_FAILED")
            result[number] = image
    return result


def export_to_powerpoint(lesson_data, output_pptx_path):
    """Generates an executive presentation matching NABIL AI theme for classroom projection."""
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    bg_color = RGBColor(7, 26, 43)
    cyan_color = RGBColor(140, 233, 255)
    gold_color = RGBColor(255, 228, 154)
    white_color = RGBColor(233, 248, 255)

    def set_slide_background(slide):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = bg_color

    # Title Slide
    slide = prs.slides.add_slide(blank_layout)
    set_slide_background(slide)
    txBox = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(11.3), Inches(3))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🧠 NABIL AI · Interactive Classroom Slide"
    p.font.size = Pt(20)
    p.font.color.rgb = gold_color

    p2 = tf.add_paragraph()
    p2.text = lesson_data.get("title", "Lesson")
    p2.font.size = Pt(40)
    p2.font.bold = True
    p2.font.color.rgb = cyan_color

    p3 = tf.add_paragraph()
    p3.text = lesson_data.get("introduction", "")
    p3.font.size = Pt(16)
    p3.font.color.rgb = white_color

    # Exercise Slides
    for ex in lesson_data.get("exercises", []):
        slide = prs.slides.add_slide(blank_layout)
        set_slide_background(slide)
        txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(6))
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"Exercise {ex.get('exercise_number', '')} — Worked Solution"
        p.font.size = Pt(26)
        p.font.bold = True
        p.font.color.rgb = cyan_color

        p_q = tf.add_paragraph()
        p_q.text = "Question: " + ex.get("prompt", "")
        p_q.font.size = Pt(16)
        p_q.font.color.rgb = gold_color

        p_steps_title = tf.add_paragraph()
        p_steps_title.text = "\nSolution Steps:"
        p_steps_title.font.size = Pt(16)
        p_steps_title.font.bold = True
        p_steps_title.font.color.rgb = cyan_color

        for step in ex.get("solution_steps", []):
            p_s = tf.add_paragraph()
            p_s.text = "• " + step
            p_s.font.size = Pt(14)
            p_s.font.color.rgb = white_color

        p_ans = tf.add_paragraph()
        p_ans.text = f"\nFinal Answer: {ex.get('final_answer', ex.get('solution', ''))}"
        p_ans.font.size = Pt(16)
        p_ans.font.bold = True
        p_ans.font.color.rgb = gold_color

    # Summary Dashboard Slide
    slide = prs.slides.add_slide(blank_layout)
    set_slide_background(slide)
    txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(6))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "💡 Summary Dashboard & Core Rules"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = cyan_color

    sum_card = lesson_data.get("summary_card", {})
    p_rule = tf.add_paragraph()
    p_rule.text = "\nRule Summary:\n" + sum_card.get("left_panel", {}).get("rule_summary", "")
    p_rule.font.size = Pt(18)
    p_rule.font.color.rgb = white_color

    p_qc = tf.add_paragraph()
    qc = sum_card.get("quick_check", {})
    p_qc.text = f"\nQuick Check: {qc.get('prompt', '')}\nAnswer: {qc.get('expected_answer', '')}"
    p_qc.font.size = Pt(16)
    p_qc.font.color.rgb = gold_color

    prs.save(output_pptx_path)


def render_html(lesson, pages, book, images, evidence_map):
    e = lambda value: html.escape(str(value), quote=True)
    golden_css = (ROOT / "app/static/nabil_lesson_golden.css").read_text(encoding="utf-8") if (ROOT / "app/static/nabil_lesson_golden.css").exists() else ""
    refs = ", ".join(str(p) for p, _ in pages)

    concepts_html = []
    for i, x in enumerate(lesson.get("concepts", []), 1):
        formula_box = f'<div class="formula">{x["formula"]}</div>' if x.get("formula") else ""
        svg_box = f'<div class="fig">{x["svg_diagram"]}</div>' if x.get("svg_diagram") else ""
        concepts_html.append(f'''
        <section class="card">
            <h2>{i} · {e(x["heading"])}</h2>
            <p class="tag">PDF p. {int(x.get("pdf_page", pages[0][0]))} · Concept {i}</p>
            <p>{x["explanation"]}</p>
            {formula_box}
            {svg_box}
        </section>''')

    activities_html = []
    for i, x in enumerate(lesson.get("activities", []), 1):
        svg_box = f'<div class="fig">{x["svg_diagram"]}</div>' if x.get("svg_diagram") else ""
        activities_html.append(f'''
        <div class="row">
            <h3>Activity {i}</h3>
            <p>{x["prompt"]}</p>
            {svg_box}
            <button class="btn" type="button" onclick="toggleElem('act-{i}')">Show Observation &amp; Conclusion</button>
            <div id="act-{i}" class="solution" style="display:none;">
                <h4>Observation:</h4>
                <p>{x["observation"]}</p>
                <h4>Conclusion:</h4>
                <p><strong>{x["conclusion"]}</strong></p>
            </div>
        </div>''')

    lab = lesson.get("live_lab", {})
    controls_html = []
    for c in lab.get("controls", []):
        controls_html.append(f'''
        <p><label>{e(c["label"])}: 
            <input id="{e(c["id"])}" type="{e(c["type"])}" min="{c.get("min", 0)}" max="{c.get("max", 100)}" value="{c.get("value", 50)}"/>
            <span id="{e(c["id"])}-val"></span>
        </label></p>''')

    lab_html = f'''
    <section class="card">
        <h2>{e(lab.get("title", "Interactive Laboratory"))}</h2>
        <p>{e(lab.get("description", ""))}</p>
        <div class="grid">
            <div>
                {"".join(controls_html)}
                <button class="btn" type="button" id="lab-reset">Reset</button>
            </div>
            <div>
                <div class="fig" id="lab-canvas">{lab.get("initial_svg", "")}</div>
                <div id="lab-output" class="formula">Ready.</div>
            </div>
        </div>
    </section>'''

    exercises_html = []
    for x in lesson.get("exercises", []):
        ex_n = e(x.get("exercise_number", ""))
        steps_html = "".join(f"<li>{step}</li>" for step in x.get("solution_steps", []))
        svg_box = f'<div class="svg-wrapper">{x["diagram_svg"]}</div>' if x.get("diagram_svg") else ""
        ext_note = f'<p class="tag">{e("; ".join(x["external_scientific_knowledge"]))}</p>' if x.get("external_scientific_knowledge") else ""
        exercises_html.append(f'''
        <div class="exercise-container">
          <div class="exercise-header">
            <span class="badge-ex">Exercise {ex_n}</span>
            <span class="badge-sub">PDF p. {int(x.get("pdf_page", pages[0][0]))}</span>
          </div>
          <div class="exercise-grid">
            <div class="diagram-panel">
              <div class="diagram-title">{e(x.get("concept_tested", "Scientific Schema"))}</div>
              {svg_box}
            </div>
            <div class="content-panel">
              <div>
                <div class="given-title">Given &amp; Formulation</div>
                <p><strong>Question:</strong> {x.get("prompt", "")}</p>
                {"<p class=tag><strong>Data:</strong> " + x.get("given_data") + "</p>" if x.get("given_data") else ""}
                {ext_note}
              </div>
              <div>
                <button class="btn-solve" type="button" onclick="toggleElem('sol-{ex_n}')">Show Complete Solution &amp; Steps</button>
                <div id="sol-{ex_n}" class="solution-box" style="display:none;">
                  <ol style="padding-left:18px; margin:6px 0;">{steps_html}</ol>
                  <div class="formula"><strong>Final Answer:</strong> {x.get("final_answer", x.get("solution", ""))}</div>
                </div>
              </div>
            </div>
            <div class="assistant-panel">
              <h4 class="bot-title">NABIL AI</h4>
              <span class="bot-sub">Your Learning Assistant</span>
              <div class="bot-avatar-box">
                <img src="data:image/jpeg;base64,{NABIL_OFFICIAL_AVATAR_B64}" alt="NABIL AI Official" class="nabil-official-avatar"/>
                <p class="bot-speech">أنا هنا لمساعدتك، اسألني أي سؤال في أي وقت.</p>
              </div>
              <button class="btn-talk" type="button">Talk to Me 🎙️</button>
              <div class="qc-box"><strong>Quick Check:</strong> Ready when you are.</div>
            </div>
          </div>
        </div>''')

    worksheet_rows = []
    js_answers = []
    for i, w in enumerate(lesson.get("worksheet", [])):
        q_idx = i
        exp = str(w.get("expected_answer", "")).strip()
        tol = float(w.get("tolerance", 0.01))
        unit = w.get("unit", "")
        hint = w.get("hint", "Review the step-by-step solution.")
        js_answers.append({"expected": exp, "tol": tol, "type": w.get("type", "text"), "hint": hint})
        
        input_widget = f'<input id="q{q_idx}" type="text" placeholder="{e(unit)}"/>'
        if w.get("type") == "select" and "options" in w:
            opts = "".join(f'<option value="{e(opt)}">{e(opt)}</option>' for opt in w["options"])
            input_widget = f'<select id="q{q_idx}"><option value="">-- Choose --</option>{opts}</select>'

        worksheet_rows.append(f'''
        <div class="row">
            <label for="q{q_idx}">Q{i+1}: {w.get("prompt", "")}</label>
            <div style="margin-top:6px;">
                {input_widget}
                <button class="btn" type="button" onclick="checkQ({q_idx})">Check</button>
                <span class="feedback" id="f{q_idx}"></span>
            </div>
        </div>''')

    sum_data = lesson.get("summary_card", {})
    left_p = sum_data.get("left_panel", {})
    center_p = sum_data.get("center_panel", {})
    quick = sum_data.get("quick_check", {})

    left_props = "".join(f'<div class="prop-row"><span>{e(p.get("label", ""))}:</span> <span>{p.get("value", "")}</span></div>'
                         for p in left_p.get("properties", []))

    dashboard_html = f'''
    <section class="nabil-dashboard">
      <div class="dash-header">
        <div>
          <span class="dash-badge">💡 {e(sum_data.get("title", lesson.get("title", "Lesson Summary")))}</span>
          <p class="dash-sub">{e(sum_data.get("learning_objectives", lesson.get("introduction", "")))}</p>
        </div>
        <div class="dash-meta">
          <span>⏱️ Estimated time: <strong>{e(sum_data.get("estimated_time", "20 minutes"))}</strong></span>
          <span>🎯 Subject: <strong>{e(book.get("subject", ""))}</strong></span>
        </div>
      </div>
      <div class="dash-main-grid">
        <div class="dash-panel left-panel">
          <h3>{e(left_p.get("heading", "Formulations & Properties"))}</h3>
          <div class="math-hero">{left_p.get("formula", "")}</div>
          {left_props}
          <div class="dash-rule-box"><strong>Rule Summary:</strong><p>{left_p.get("rule_summary", "")}</p></div>
        </div>
        <div class="dash-panel center-panel">
          <div class="panel-header"><h3>{e(center_p.get("title", "Visual & Graphical Modeling"))}</h3></div>
          <div class="dash-graph">{center_p.get("svg_diagram", "")}</div>
          <div class="secondary-info" style="margin-top:10px;">{center_p.get("secondary_block", {}).get("html_content", "")}</div>
        </div>
        <div class="dash-panel right-panel">
          <div class="bot-header"><h4 style="margin:0; color:#8ce9ff;">NABIL AI</h4><small style="color:#7193b2;">Your Learning Assistant</small></div>
          <div class="bot-avatar-box" style="margin:12px 0;">
            <img src="data:image/jpeg;base64,{NABIL_OFFICIAL_AVATAR_B64}" alt="NABIL AI" class="nabil-official-avatar"/>
            <p class="bot-speech">أنا هنا لمساعدتك، اسألني أي سؤال في أي وقت.</p>
          </div>
          <button class="dash-btn mic-btn" type="button">🎙️ Talk to Me</button>
          <div class="quick-card">
            <div class="qc-head">❓ Quick Check</div>
            <p>{quick.get("prompt", "")}</p>
            <input id="quickInput" type="text" placeholder="Your answer" style="width:100%; margin:8px 0;"/>
            <button class="btn" type="button" onclick="checkQuick()">Verify</button>
            <div id="quickFb" class="feedback" style="margin-top:6px;"></div>
          </div>
        </div>
      </div>
      <div class="dash-footer">
        <div class="action-buttons">
          <button class="act-btn" type="button" onclick="window.print()">🖨️ Print Lesson</button>
          <button class="act-btn" type="button" onclick="navigator.clipboard.writeText(window.location.href)">🔗 Share Lesson</button>
        </div>
        <div style="font-size:0.85rem; color:#7193b2;">NABIL AI Platform · Universal Production Lesson</div>
      </div>
    </section>'''

    return f'''<!doctype html>
<html lang="{e(book.get("language", "en"))[:2].lower()}">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{e(lesson.get("title", ""))}</title>
<link rel="stylesheet" href="[https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css](https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css)"/>
<script defer src="[https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js](https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js)"></script>
<script defer src="[https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js](https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js)"
        onload="renderMathInElement(document.body, {{delimiters: [{{left: '$$', right: '$$', display: true}}, {{left: '$', right: '$', display: false}}]}});"></script>
<style>
{golden_css}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:#071a2b; color:#e9f8ff; font:16px system-ui, Arial, sans-serif; line-height:1.6; }}
header {{ padding:20px; background:linear-gradient(95deg,#113757,#0757b2); display:flex; justify-content:space-between; flex-wrap:wrap; }}
main {{ max-width:1150px; margin:auto; padding:16px; }}
h1,h2,h3,h4 {{ color:#8ce9ff; }}
.card {{ border:1px solid #36a5dc; border-radius:14px; background:#102b42; padding:20px; margin:16px 0; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:16px; }}
.fig {{ margin:14px 0; border:1px solid #2ca9dd; background:#09243b; border-radius:12px; padding:12px; text-align:center; }}
.fig svg {{ max-width:100%; height:auto; display:block; margin:auto; }}
.formula {{ border:1px solid #34b9ee; padding:14px; border-radius:10px; margin:12px 0; background:rgba(52,185,238,0.08); font-family:monospace; font-size:1.1rem; }}
.tag {{ color:#ffe49a; font-size:0.95rem; font-weight:bold; }}
.btn {{ background:#1768c5; color:white; border:none; padding:10px 18px; border-radius:8px; cursor:pointer; font-weight:bold; margin:6px 0; }}
.btn:hover {{ background:#2187ef; }}
.solution {{ background:#0c3452; border-left:4px solid #31d9a8; padding:14px; border-radius:6px; margin-top:10px; }}
.row {{ border-top:1px solid #315f7e; padding:14px 0; }}
.feedback {{ font-weight:bold; margin-left:10px; }}
input, select {{ padding:9px; border-radius:6px; border:1px solid #36a5dc; background:#071a2b; color:#fff; }}
.exercise-container {{ background:#071e33; border:1.5px solid #1f6498; border-radius:14px; padding:18px; margin-bottom:24px; box-shadow:0 8px 24px rgba(0,0,0,0.4); }}
.exercise-header {{ display:flex; align-items:center; gap:12px; margin-bottom:16px; }}
.badge-ex {{ background:#005a9c; color:#fff; font-weight:bold; padding:4px 14px; border-radius:6px; font-size:1.1rem; }}
.badge-sub {{ background:#093354; color:#8ce9ff; border:1px solid #36a5dc; padding:3px 10px; border-radius:12px; font-size:0.8rem; }}
.exercise-grid {{ display:grid; grid-template-columns:1.1fr 1fr 240px; gap:14px; }}
.diagram-panel {{ background:#06192a; border:1px solid #1b4b73; border-radius:10px; padding:12px; display:flex; flex-direction:column; }}
.diagram-title {{ color:#8ce9ff; font-size:0.85rem; font-weight:bold; margin-bottom:8px; border-bottom:1px solid #163857; padding-bottom:4px; }}
.svg-wrapper {{ flex:1; display:flex; align-items:center; justify-content:center; min-height:240px; }}
.svg-wrapper svg {{ max-width:100%; height:auto; }}
.content-panel {{ background:#06192a; border:1px solid #1b4b73; border-radius:10px; padding:14px; display:flex; flex-direction:column; justify-content:space-between; }}
.given-title {{ color:#ffe49a; font-size:1.05rem; font-weight:bold; margin-bottom:10px; }}
.btn-solve {{ background:#1768c5; color:white; border:none; padding:8px 14px; border-radius:6px; cursor:pointer; font-weight:bold; margin-top:10px; align-self:flex-start; }}
.btn-solve:hover {{ background:#2187ef; }}
.solution-box {{ margin-top:10px; padding:10px; background:#092942; border-left:3px solid #31d9a8; border-radius:6px; font-size:0.88rem; }}
.assistant-panel {{ background:#06192a; border:1px solid #1b4b73; border-radius:10px; padding:12px; display:flex; flex-direction:column; align-items:center; text-align:center; }}
.bot-title {{ color:#8ce9ff; font-weight:bold; margin:0; font-size:1rem; }}
.bot-sub {{ color:#7193b2; font-size:0.75rem; margin-bottom:8px; }}
.bot-avatar-box {{ background:#092640; border:2px solid #36a5dc; border-radius:16px; padding:10px; width:100%; display:flex; flex-direction:column; align-items:center; margin-bottom:10px; }}
.bot-speech {{ font-size:0.8rem; color:#e9f8ff; margin:6px 0 0; direction:rtl; }}
.btn-talk {{ background:#d9383a; color:#fff; border:none; width:100%; padding:8px; border-radius:20px; font-weight:bold; cursor:pointer; font-size:0.85rem; margin-bottom:10px; }}
.qc-box {{ background:#09243b; border:1px solid #163857; border-radius:8px; padding:8px; width:100%; font-size:0.75rem; color:#ffe49a; }}
.nabil-official-avatar {{ width:90px; height:90px; object-fit:cover; border-radius:50%; border:2.5px solid #38aada; box-shadow:0 0 15px rgba(56,170,218,0.45); background:#071e33; margin-bottom:8px; }}
.nabil-dashboard {{ background:#06192a; color:#e9f8ff; border:1.5px solid #1f6498; border-radius:16px; padding:20px; margin:24px 0; box-shadow:0 10px 30px rgba(0,0,0,0.5); }}
.dash-header {{ display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #163857; padding-bottom:12px; margin-bottom:16px; flex-wrap:wrap; gap:12px; }}
.dash-badge {{ background:#0b3456; color:#8ce9ff; font-weight:bold; padding:6px 14px; border-radius:20px; border:1px solid #36a5dc; }}
.dash-sub {{ margin:6px 0 0; font-size:0.9rem; color:#9cbacf; }}
.dash-meta {{ display:flex; gap:16px; font-size:0.85rem; color:#ffe49a; }}
.dash-main-grid {{ display:grid; grid-template-columns:280px 1fr 220px; gap:16px; }}
.dash-panel {{ background:#09243b; border:1px solid #1f5077; border-radius:12px; padding:16px; }}
.prop-row {{ display:flex; justify-content:space-between; margin:8px 0; font-size:0.88rem; border-bottom:1px dashed #163857; padding-bottom:4px; }}
.dash-rule-box {{ background:#071a2b; border-left:3px solid #31d9a8; padding:10px; border-radius:6px; margin-top:14px; font-size:0.85rem; }}
.mic-btn {{ background:#e63946; color:#fff; border:none; width:100%; padding:10px; border-radius:20px; font-weight:bold; cursor:pointer; }}
.quick-card {{ margin-top:16px; background:#071a2b; border:1px solid #1f6498; border-radius:10px; padding:12px; width:100%; }}
.dash-footer {{ display:flex; justify-content:space-between; align-items:center; margin-top:16px; border-top:1px solid #163857; padding-top:14px; }}
.action-buttons {{ display:flex; gap:8px; flex-wrap:wrap; }}
.act-btn {{ background:#102b42; border:1px solid #36a5dc; color:#8ce9ff; border-radius:6px; padding:6px 10px; font-size:0.8rem; cursor:pointer; }}
@media (max-width:900px) {{
  .exercise-grid {{ grid-template-columns:1fr; }}
  .dash-main-grid {{ grid-template-columns:1fr; }}
}}
</style>
</head>
<body>
<header>
  <strong>🧠 NABIL AI · {e(book.get("grade", ""))} · {e(book.get("subject", ""))}</strong>
  <span>National Textbook Collection · Source: {e(book.get("title", ""))}</span>
</header>
<main>
  <section class="card">
    <h1>{e(lesson.get("title", ""))}</h1>
    <p class="tag">{e(book.get("title", ""))} · PDF pages {refs}</p>
    <p>{lesson.get("introduction", "")}</p>
  </section>
  {"".join(concepts_html)}
  <section class="card">
    <h2>Inquiry &amp; Activities</h2>
    {"".join(activities_html)}
  </section>
  {lab_html}
  <section>
    <h2>Solved Textbook Exercises</h2>
    {"".join(exercises_html)}
  </section>
  <section class="card">
    <h2>Interactive Worksheet</h2>
    {"".join(worksheet_rows)}
    <div style="margin-top:16px;">
      <button class="btn" type="button" onclick="gradeWorksheet()">Grade Worksheet</button>
      <strong id="finalScore" style="margin-left:15px; color:#31d9a8; font-size:1.2rem;"></strong>
    </div>
  </section>
  {dashboard_html}
</main>
<script>
function toggleElem(id) {{
  var el = document.getElementById(id);
  if (!el) return;
  el.style.display = (el.style.display === 'none' || el.style.display === '') ? 'block' : 'none';
}}
var wsAnswers = {json.dumps(js_answers)};
var userScores = new Array(wsAnswers.length).fill(false);
function checkQ(idx) {{
  var cfg = wsAnswers[idx];
  var el = document.getElementById('q' + idx);
  var fb = document.getElementById('f' + idx);
  if (!el || !fb) return;
  var val = el.value.trim().toLowerCase();
  if (val === '') {{
    fb.textContent = 'Please enter an answer.';
    fb.style.color = '#ffe49a';
    return;
  }}
  var ok = false;
  if (cfg.type === 'numeric') {{
    var num = parseFloat(val);
    var exp = parseFloat(cfg.expected);
    ok = !isNaN(num) && Math.abs(num - exp) <= cfg.tol;
  }} else {{
    ok = (val === cfg.expected.toLowerCase());
  }}
  if (ok) {{
    fb.textContent = '✓ Correct';
    fb.style.color = '#31d9a8';
    userScores[idx] = true;
  }} else {{
    fb.textContent = '✗ ' + cfg.hint;
    fb.style.color = '#ff8b98';
    userScores[idx] = false;
  }}
}}
function gradeWorksheet() {{
  var s = 0;
  for (var i = 0; i < userScores.length; i++) {{ if (userScores[i]) s++; }}
  document.getElementById('finalScore').textContent = 'Score: ' + s + ' / ' + userScores.length;
}}
var quickExpected = {json.dumps(str(quick.get("expected_answer", "")).strip().lower())};
var quickHint = {json.dumps(str(quick.get("hint", "")).strip())};
function checkQuick() {{
  var val = document.getElementById('quickInput').value.trim().toLowerCase();
  var fb = document.getElementById('quickFb');
  if (val === quickExpected) {{
    fb.textContent = '✓ Correct';
    fb.style.color = '#31d9a8';
  }} else {{
    fb.textContent = 'Hint: ' + quickHint;
    fb.style.color = '#ff8b98';
  }}
}}
{lab.get("js_update_fn", "")}
</script>
</body>
</html>'''


def check_html(document, lesson, pages, evidence_map):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(document, "html.parser")
    errors = []
    if not soup.select_one("meta[name=viewport]") or not soup.select_one("main"):
        errors.append("MOBILE_OR_SEMANTIC_STRUCTURE_MISSING")
    if not soup.select_one("#finalScore"):
        errors.append("WORKSHEET_GRADE_MISSING")
    if not soup.select_one(".nabil-dashboard"):
        errors.append("MASTER_DASHBOARD_CARD_MISSING")
    if len(soup.select(".card")) < 3:
        errors.append("LESSON_SECTIONS_INCOMPLETE")
    return errors


def ensure_folder(service, parent, name):
    safe = name.replace("'", "\\'")
    result = service.files().list(q=f"'{parent}' in parents and name='{safe}' and mimeType='{FOLDER_MIME}' and trashed=false",
                                  fields="files(id,name)", pageSize=10).execute().get("files", [])
    if len(result) > 1:
        raise ValueError("AMBIGUOUS_DRIVE_FOLDER")
    if result:
        return result[0]["id"]
    created = service.files().create(body={"name": name, "mimeType": FOLDER_MIME, "parents": [parent]},
                                     fields="id").execute()
    return created["id"]


def find_named(service, parent, name):
    safe = name.replace("'", "\\'")
    files = service.files().list(q=f"'{parent}' in parents and name='{safe}' and trashed=false",
        fields="files(id,name,mimeType)", pageSize=20).execute().get("files", [])
    if len(files) > 1:
        raise ValueError("AMBIGUOUS_EXISTING_DRIVE_FILE: " + name)
    return files[0] if files else None


def upload_verified(service, parent, name, raw, mime, description=None):
    from googleapiclient.http import MediaIoBaseUpload
    minimum = 20_000
    if len(raw) < minimum:
        raise ValueError("ARTIFACT_TOO_SMALL_BEFORE_UPLOAD: " + name)
    existing = find_named(service, parent, name)
    if existing:
        verify_uploaded(service, existing["id"], parent, raw, mime)
        return existing
    body = {"name": name, "parents": [parent]}
    if description:
        body["description"] = description
    item = service.files().create(body=body,
        media_body=MediaIoBaseUpload(io.BytesIO(raw), mimetype=mime, resumable=False),
        fields="id,name,size,webViewLink").execute()
    verify_uploaded(service, item["id"], parent, raw, mime)
    return item


def verify_uploaded(service, file_id, parent, raw, mime):
    metadata = service.files().get(fileId=file_id, fields="id,name,mimeType,size,parents,trashed").execute()
    if (metadata.get("trashed") or parent not in metadata.get("parents", [])
        or metadata.get("mimeType") != mime or int(metadata.get("size", 0)) != len(raw)):
        raise ValueError("DRIVE_FILE_LOCATION_TYPE_OR_SIZE_MISMATCH")
    if hashlib.sha256(download(service, file_id)).digest() != hashlib.sha256(raw).digest():
        raise ValueError("DRIVE_READBACK_HASH_MISMATCH")


def curriculum_grade_number(value):
    text = str(value).strip()
    found = re.search(r"(?<!\d)(1[0-2]|[1-9])(?!\d)", text)
    if found:
        return int(found.group(1))
    for prefix, number in (("الأول ثانوي", 10), ("الثاني ثانوي", 11), ("الثالث ثانوي", 12)):
        if text.startswith(prefix):
            return number
    ordinals = {"الأول": 1, "الثاني": 2, "الثالث": 3, "الرابع": 4,
                "الخامس": 5, "السادس": 6, "السابع": 7, "الثامن": 8, "التاسع": 9}
    for word, number in ordinals.items():
        if text == f"الصف {word}":
            return number
    raise ValueError("CURRICULUM_GRADE_UNMAPPED: " + text)


def curriculum_subject_folder(subject):
    labels = {"physics": "Physics - فيزياء",
              "mathematics": "Mathematics - رياضيات",
              "chemistry": "Chemistry - كيمياء",
              "biology": "Biology - علوم الحياة",
              "general_science": "General Science - علوم"}
    if subject not in labels:
        raise ValueError("CURRICULUM_SUBJECT_UNMAPPED: " + str(subject))
    return labels[subject]


def lesson_html_filename(book, title):
    grade = curriculum_grade_number(book["grade"])
    subject = book["subject"].upper().replace("_", "-")
    slug = re.sub(r"[^\w]+", "-", title, flags=re.UNICODE).strip("-")[:90]
    if not slug:
        raise ValueError("EMPTY_LESSON_FILENAME")
    return f"G{grade:02d}-{subject}--{slug}.html"


def lesson_pptx_filename(book, title):
    return lesson_html_filename(book, title).replace(".html", ".pptx")


def check_lesson_alias_collision(service, folder, book, title, start):
    canonical = lesson_html_filename(book, title)
    for record in book.get("authored_lessons", []):
        pages = record.get("source_pdf_pages") or []
        if (record.get("drive_html_id") and pages and pages[0] == start + 1
                and record.get("title") != title):
            raise ValueError("LESSON_ALIAS_COLLISION_REQUIRES_REVIEW")
    token = f"G{curriculum_grade_number(book['grade']):02d}-{book['subject'].upper().replace('_', '-') }--"
    page_token = str(start + 1)
    page = None
    while True:
        result = service.files().list(
            q=f"'{folder}' in parents and trashed=false",
            fields="nextPageToken,files(id,name,mimeType,description)",
            pageSize=1000, pageToken=page).execute()
        for item in result.get("files", []):
            name = item.get("name", "")
            if (name.startswith(token) and name.endswith(".html") and name != canonical
                    and item.get("description", "").find(f"source_pdf_page={page_token}") >= 0):
                raise ValueError("LESSON_ALIAS_COLLISION_REQUIRES_REVIEW")
        page = result.get("nextPageToken")
        if not page:
            break


def verify_folder_chain(service, subject_folder, grade_folder):
    for child, parent in ((subject_folder, grade_folder), (grade_folder, ROOT_FOLDER)):
        meta = service.files().get(fileId=child, fields="id,mimeType,parents,trashed").execute()
        if (meta.get("trashed") or meta.get("mimeType") != FOLDER_MIME or parent not in meta.get("parents", [])):
            raise ValueError("DRIVE_FOLDER_CHAIN_MISMATCH")


def read_ledger(service, default):
    item = find_named(service, ROOT_FOLDER, LEDGER.name)
    if not item:
        return default, item
    remote = json.loads(download(service, item["id"]).decode("utf-8-sig"))
    if not isinstance(remote.get("books"), list):
        raise ValueError("REMOTE_LEDGER_INVALID")
    return remote, item


def save_ledger(service, ledger, item):
    from googleapiclient.http import MediaIoBaseUpload
    raw = (json.dumps(ledger, ensure_ascii=False, indent=2) + "\n").encode()
    media = MediaIoBaseUpload(io.BytesIO(raw), mimetype="application/json", resumable=False)
    if item:
        saved = service.files().update(fileId=item["id"], media_body=media, fields="id,name").execute()
    else:
        saved = service.files().create(body={"name": LEDGER.name, "parents": [ROOT_FOLDER]}, media_body=media, fields="id,name").execute()
    if download(service, saved["id"]) != raw:
        raise ValueError("REMOTE_LEDGER_READBACK_FAILED")
    return saved


def run(report_path, pilot_book_id=None, pilot_lesson=None, pilot_pages=None, publish=False):
    global RUN_DEADLINE, BOOK_DEADLINE, PROGRESS_STARTED
    PROGRESS_STARTED = time.monotonic()
    RUN_DEADLINE = time.monotonic() + 420
    if pilot_book_id or pilot_lesson:
        max_books = 1
    else:
        max_books = max(1, min(70, int(os.getenv("NABIL_LESSON_BATCH_BOOKS", "5"))))
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    report = {"started": now(), "status": "RUNNING", "attempts": [], "production": None}
    if pilot_book_id or pilot_lesson:
        report["pilot_filter"] = {"book_id": pilot_book_id, "lesson": pilot_lesson}

    def checkpoint():
        report["updated"] = now()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    checkpoint()
    try:
        service = owner_drive()
        root = service.files().get(fileId=ROOT_FOLDER, fields="id,name,capabilities(canAddChildren)").execute()
        if publish and not root.get("capabilities", {}).get("canAddChildren"):
            raise PermissionError("OWNER_ROOT_NOT_WRITABLE")
        if publish:
            ledger, ledger_item = read_ledger(service, ledger)
        else:
            ledger_item = None
    except Exception as exc:
        report["status"] = "BLOCKED_CREDENTIALS_OR_DRIVE"
        report["error"] = f"{type(exc).__name__}: {exc}"
        checkpoint()
        return report

    if not configured_providers():
        report["status"] = "BLOCKED_GENERATION_CREDENTIALS"
        report["error"] = "NO_CONFIGURED_AI_PROVIDER_KEY"
        checkpoint()
        return report

    seen_ids = set()
    priority = {name: i for i, name in enumerate(ledger.get("priority", []))}

    def book_order(book):
        grade = re.search(r"\d+", book.get("grade", ""))
        return (priority.get(book.get("subject"), 999),
                int(grade.group()) if grade else 999,
                book.get("language", "") != "English", book.get("order", 999))

    for book in sorted(ledger["books"], key=book_order):
        if pilot_book_id and book.get("drive_file_id") != pilot_book_id:
            continue
        if time.monotonic() >= RUN_DEADLINE:
            report["status"] = "RUN_DEADLINE_EXCEEDED"
            checkpoint()
            break
        if len(report["attempts"]) >= max_books:
            report["status"] = "PILOT_BOOK_LIMIT_REACHED"
            report["max_books"] = max_books
            checkpoint()
            progress("PILOT_BOOK_LIMIT_REACHED", attempts=len(report["attempts"]))
            break
        if not book.get("drive_file_id") or book["drive_file_id"] in seen_ids:
            continue
        seen_ids.add(book["drive_file_id"])
        attempt = {"book": book["title"], "book_id": book["drive_file_id"], "started": now()}
        BOOK_DEADLINE = min(RUN_DEADLINE, time.monotonic() + (360 if pilot_book_id else 120))
        report["attempts"].append(attempt)
        checkpoint()
        progress("BOOK_STARTED", book=book["title"])

        try:
            from pypdf import PdfReader
            temp = tempfile.TemporaryDirectory(prefix="nabil_book_")
            pdf = Path(temp.name) / "book.pdf"
            download_pdf_to_path(service, book["drive_file_id"], pdf)
            reader = PdfReader(str(pdf))
            progress("SOURCE_DISCOVERY_STARTED", book=book["title"])
            entries = candidates(reader, pdf)
            finished_records = [x for x in book.get("authored_lessons", [])
                                if x.get("status") in ("verified_complete", "REQUIRES_TEACHER_REVIEW")
                                and x.get("drive_html_id")]
            finished = {x.get("lesson_key") for x in finished_records}
            finished_starts = {x["source_pdf_pages"][0] - 1 for x in finished_records if x.get("source_pdf_pages")}
            available = [(title, start, end) for title, start, end in entries
                         if lesson_key(book, title, start) not in finished and start not in finished_starts]
            if pilot_lesson:
                available = [entry for entry in available if entry[0].strip().casefold() == pilot_lesson.strip().casefold()]
            if not available:
                raise ValueError("NO_UNFINISHED_TOC_LESSON")
            title, start, end = available[0]
            if pilot_pages and (start + 1, end) != pilot_pages:
                raise ValueError(f"PILOT_SOURCE_PAGES_MISMATCH: discovered {start+1}-{end}; expected {pilot_pages[0]}-{pilot_pages[1]}")
            attempt.update({"lesson": title, "source_pdf_pages": list(range(start + 1, end + 1)),
                            "lesson_key": lesson_key(book, title, start)})
            progress("SOURCE_LESSON_SELECTED", lesson=title, pages=attempt["source_pdf_pages"])
            pages = source_excerpt(reader, pdf, start, end)
            images = source_images(pdf, pages)
            proposed_visuals, visual_provider, visual_model = visual_candidates(images)
            catalog = evidence_catalog(pages, proposed_visuals)
            if len(catalog) < 10:
                raise ValueError("SOURCE_EVIDENCE_CATALOG_TOO_SPARSE")
            digest = hashlib.sha256()
            with pdf.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
            attempt["source_sha256"] = digest.hexdigest()
            checkpoint()
            evidence_map = source_evidence_map(title, pages, catalog, visual_provider, visual_model)
            record_role_provenance(evidence_map, attempt, "visual_extractor", visual_provider, visual_model)
            record_role_provenance(evidence_map, attempt, "generator", None, None)
            record_role_provenance(evidence_map, attempt, "reviewer", None, None)
            evidence_path = report_path.with_name(report_path.stem + "-evidence-map.json")
            evidence_path.write_text(json.dumps(evidence_map, ensure_ascii=False, indent=2), encoding="utf-8")
            attempt["evidence_map_path"] = str(evidence_path)
            attempt["source_evidence_counts"] = {key: len(value) for key, value in evidence_map["categories"].items()}
            attempt["generation_checks"] = []
            previous_failures = []

            for generation_attempt in (1, 2):
                progress("GENERATION_STARTED", lesson=title, attempt=generation_attempt)
                lesson, generator_provider, generator_model = generate(
                    title, pages, book.get("language", ""), evidence_map,
                    previous_failures, visual_provider=visual_provider, visual_model=visual_model)
                attempt["generator"] = {"provider": generator_provider, "model": generator_model}
                record_role_provenance(evidence_map, attempt, "generator", generator_provider, generator_model)
                evidence_path.write_text(json.dumps(evidence_map, ensure_ascii=False, indent=2), encoding="utf-8")
                draft_path = report_path.with_name(report_path.stem + f"-draft-{generation_attempt}.json")
                draft_path.write_text(json.dumps(lesson, ensure_ascii=False, indent=2), encoding="utf-8")
                attempt.setdefault("draft_paths", []).append(str(draft_path))
                progress("QUALITY_GATE_STARTED", lesson=title, attempt=generation_attempt)
                failures = check_content(lesson, title, pages, catalog)
                if any(x.startswith("UNVERIFIED_") for x in failures):
                    progress("SOURCE_QUOTE_REPAIR_STARTED", count=sum(x.startswith("UNVERIFIED_") for x in failures))
                    if repair_source_quotes(lesson, pages, catalog, failures, generator_provider):
                        failures = check_content(lesson, title, pages, catalog)
                review = None
                if not failures:
                    review = scientific_review(lesson, pages, images,
                                               generator_provider, generator_model,
                                               visual_provider, visual_model, catalog)
                    attempt["scientific_review"] = review
                    record_role_provenance(evidence_map, attempt, "reviewer", review.get("reviewer"), review.get("model"))
                    evidence_path.write_text(json.dumps(evidence_map, ensure_ascii=False, indent=2), encoding="utf-8")
                    if not review["pass"]:
                        failures.append("SCIENTIFIC_REVIEW_REJECTED")
                previous_failures = (review["errors"] if review and not review["pass"] else failures[:])
                attempt["generation_checks"].append(
                    {"attempt": generation_attempt, "failures": failures, "scientific_review": review})
                checkpoint()
                if not failures:
                    break

            document = render_html(lesson, pages, book, images, evidence_map) if not failures else ""
            failures.extend(check_html(document, lesson, pages, evidence_map) if document else [])
            attempt["html_quality"] = {"pass": not failures, "failures": failures}
            checkpoint()
            if failures:
                raise ValueError("HTML_QUALITY_FAILED: " + ",".join(failures))

            # تصدير ملفي الـ HTML والـ PPTX محلياً
            html_path = report_path.with_name(report_path.stem + "-lesson.html")
            html_path.write_text(document, encoding="utf-8")
            pptx_path = report_path.with_name(report_path.stem + "-lesson.pptx")
            export_to_powerpoint(lesson, str(pptx_path))
            attempt["local_artifacts"] = {"html": str(html_path), "pptx": str(pptx_path)}
            checkpoint()

            if not publish:
                report["status"] = "LOCAL_VERIFIED_DRY_RUN_SUCCESS"
                attempt["status"] = "LOCAL_VERIFIED_DRY_RUN_SUCCESS"
                checkpoint()
                break

            progress("UPLOAD_STARTED", lesson=title)
            grade_folder = ensure_folder(service, ROOT_FOLDER, f'Grade {curriculum_grade_number(book["grade"])}')
            subject_folder = ensure_folder(service, grade_folder, curriculum_subject_folder(book["subject"]))
            folder = subject_folder
            verify_folder_chain(service, subject_folder, grade_folder)
            html_name = lesson_html_filename(book, title)
            pptx_name = lesson_pptx_filename(book, title)
            check_lesson_alias_collision(service, folder, book, title, start)

            # رفع ملف الـ HTML
            html_item = upload_verified(service, folder, html_name, document.encode("utf-8"),
                                        "text/html", f"source_pdf_page={start + 1}; source_book={book['drive_file_id']}")
            # رفع ملف الـ PowerPoint
            pptx_bytes = pptx_path.read_bytes()
            pptx_item = upload_verified(service, folder, pptx_name, pptx_bytes,
                                        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                                        f"source_pdf_page={start + 1}; source_book={book['drive_file_id']}")

            attempt["drive_html_id"] = html_item["id"]
            attempt["drive_pptx_id"] = pptx_item["id"]
            checkpoint()
            attempt["status"] = "VERIFIED_UPLOAD"
            record = {"title": title, "lesson_key": attempt["lesson_key"],
                      "book_drive_file_id": book["drive_file_id"],
                      "source_pdf_pages": attempt["source_pdf_pages"], "source_sha256": attempt["source_sha256"],
                      "source_pages_sha256": hashlib.sha256(json.dumps(pages, ensure_ascii=False).encode()).hexdigest(),
                      "source_evidence_sha256": hashlib.sha256(
                          json.dumps(evidence_map, ensure_ascii=False, sort_keys=True).encode()).hexdigest(),
                      "source_evidence_counts": attempt["source_evidence_counts"],
                      "html_sha256": hashlib.sha256(document.encode("utf-8")).hexdigest(),
                      "drive_folder_id": folder, "drive_html_id": html_item["id"], "drive_pptx_id": pptx_item["id"],
                      "html_bytes": len(document.encode("utf-8")),
                      "status": "REQUIRES_TEACHER_REVIEW", "completed_at": now()}
            book.setdefault("authored_lessons", []).append(record)
            ledger["updated"] = now()
            ledger_item = save_ledger(service, ledger, ledger_item)
            LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            report["production"] = record
            report["status"] = "ONE_PILOT_REVIEW_PENDING"
            checkpoint()
            progress("ONE_PILOT_REVIEW_PENDING", lesson=title)
            break
        except Exception as exc:
            attempt.update({"status": "FAILED", "reason": f"{type(exc).__name__}: {exc}", "finished": now()})
            checkpoint()
            progress("BOOK_FAILED", book=book["title"], reason=attempt["reason"])
            if attempt.get("lesson"):
                report["status"] = "PILOT_LESSON_FAILED"
                checkpoint()
                break
        finally:
            BOOK_DEADLINE = None
            if "temp" in locals():
                temp.cleanup()
                del temp
    else:
        report["status"] = "NO_LESSON_COMPLETE"
        checkpoint()
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", default="data/nabil_lesson_factory_run.json")
    parser.add_argument("--pilot-book-id", help="Only consider this registered Drive PDF ID")
    parser.add_argument("--pilot-lesson", help="Only consider this exact TOC lesson heading")
    parser.add_argument("--pilot-pages", help="Require exact inclusive PDF page range, e.g. 13-18")
    parser.add_argument("--publish", action="store_true", help="Explicitly allow Drive writes and production ledger updates")
    args = parser.parse_args()
    pilot_pages = None
    if args.pilot_pages:
        match = re.fullmatch(r"(\d+)-(\d+)", args.pilot_pages)
        if not match or int(match[1]) > int(match[2]):
            parser.error("--pilot-pages must be START-END")
        pilot_pages = (int(match[1]), int(match[2]))

    def deadline_handler(_signum, _frame):
        raise TimeoutError("FACTORY_RUN_EXCEEDED_420_SECONDS")

    old_handler = signal.signal(signal.SIGALRM, deadline_handler)
    signal.setitimer(signal.ITIMER_REAL, 420)
    try:
        report = run(Path(args.report), args.pilot_book_id, args.pilot_lesson, pilot_pages, publish=args.publish)
    except TimeoutError as exc:
        report = {"status": "RUN_DEADLINE_EXCEEDED", "error": str(exc)}
        if Path(args.report).exists():
            previous = json.loads(Path(args.report).read_text(encoding="utf-8"))
            previous.update(report)
            report = previous
            Path(args.report).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old_handler)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] in ("ONE_PILOT_REVIEW_PENDING", "LOCAL_VERIFIED_DRY_RUN_SUCCESS") else 2


if __name__ == "__main__":
    sys.exit(main())
