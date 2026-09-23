"""Produce at most one verified, source-grounded lesson from registered Drive PDFs.

Usage: python -m scripts.nabil_lesson_factory --report /tmp/nabil-lesson-run.json
Requires owner Drive OAuth and an existing configured AI provider key. A failed candidate is
logged and the next registered book is tried. No existing HTML is read.
"""
import argparse
import hashlib
import html
import io
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data/interactive_lesson_production_ledger.json"
FOLDER_MIME = "application/vnd.google-apps.folder"
ROOT_FOLDER = os.getenv("NABIL_LESSON_DRIVE_ROOT", "16bcmZMO_dn4FqlGaDtl8Hky6iSBEqZpX")


def now():
    return datetime.now(timezone.utc).isoformat()


def owner_drive():
    names = ("GOOGLE_DRIVE_OAUTH_CLIENT_ID", "GOOGLE_DRIVE_OAUTH_CLIENT_SECRET",
             "GOOGLE_DRIVE_OAUTH_REFRESH_TOKEN")
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
    """Stream PDFs to disk; page access remains lazy even for PDFs over 80 MB."""
    from googleapiclient.http import MediaIoBaseDownload
    with path.open("wb") as target:
        loader = MediaIoBaseDownload(target, service.files().get_media(fileId=file_id))
        finished = False
        while not finished:
            _, finished = loader.next_chunk()


def ocr_pdf(raw, page_indices):
    """OCR selected pages; scanned books have no extractable PDF text."""
    with tempfile.TemporaryDirectory(prefix="nabil_toc_") as directory:
        pdf = Path(directory) / "source.pdf"
        if isinstance(raw, Path):
            pdf = raw
        else:
            pdf.write_bytes(raw)
        result = {}
        for index in page_indices:
            prefix = str(Path(directory) / f"page_{index}")
            subprocess.run(["pdftoppm", "-f", str(index+1), "-l", str(index+1),
                            "-singlefile", "-r", "160", "-jpeg", str(pdf), prefix],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=45)
            result[index] = subprocess.run(
                ["tesseract", prefix+".jpg", "stdout", "-l", "eng"],
                check=True, capture_output=True, text=True, timeout=45).stdout.strip()
        return result


def visual_chapter_starts(pdf, total_pages, toc_text):
    """Read the upper title band of actual page images, checking the TOC.

    Full-page OCR commonly misses decorative colored headings. No PDF
    bookmark or filename is accepted as a chapter title in scanned books.
    """
    from PIL import Image, ImageEnhance, ImageOps
    chapters = []
    with tempfile.TemporaryDirectory(prefix="nabil_headers_") as directory:
        for index in range(10, min(total_pages, 75)):
            prefix = str(Path(directory) / "page")
            subprocess.run(["pdftoppm", "-f", str(index+1), "-l", str(index+1),
                            "-singlefile", "-r", "150", "-jpeg", str(pdf), prefix],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=45)
            picture = Image.open(prefix+".jpg")
            band = picture.crop((0,0,picture.width,int(picture.height*.19)))
            ImageEnhance.Contrast(ImageOps.grayscale(band)).enhance(2).save(prefix+"_top.png")
            title_band = subprocess.run(
                ["tesseract", prefix+"_top.png", "stdout", "-l", "eng", "--psm", "6"],
                check=True, capture_output=True, text=True, timeout=45).stdout
            found = re.search(r"(?:\b(?:chapter|chapitre)\s*|^\W*)"
                              r"(\d{1,2})\s*[:.\-]\s*"
                              r"([A-Za-z][A-Za-z '&\-]{4,65})",title_band,re.I|re.M)
            if not found:
                continue
            number, title = int(found.group(1)), found.group(2).strip(" .-")
            words = re.findall(r"[A-Za-z]{4,}",title.lower())
            if not words or sum(w in toc_text.lower() for w in words) < max(1,len(words)-1):
                continue
            if chapters and (number <= chapters[-1][2] or index-chapters[-1][0] < 2):
                continue
            chapters.append((index,title,number))
            if len(chapters) >= 2 and chapters[1][0]-chapters[0][0] <= 14:
                break
    return [(title,start,chapters[i+1][0] if i+1<len(chapters)
             else min(start+8,total_pages))
            for i,(start,title,_) in enumerate(chapters)
            if 2 <= (chapters[i+1][0] if i+1<len(chapters)
                     else min(start+8,total_pages))-start <= 14]


def candidates(reader, raw):
    """Use actual PDF bookmarks or a textual table of contents, then locate
    headings in extracted pages. Never infer a lesson from a stored HTML title.
    Ambiguous matches are rejected instead of guessing an offset.
    """
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
                          if p > 0 and len(t.split()) >= 2
                          and not re.search(r"\.(?:pdf|jpg|png)|^(?:img|screenshot)[_ -]|livre$",
                                            t, re.I)})
        if len(ordered) >= 2:
            return [(title, start, ordered[i+1][0] if i+1 < len(ordered)
                     else min(start+8, len(page_text)))
                    for i, (start, title) in enumerate(ordered)
                    if 2 <= (ordered[i+1][0] if i+1 < len(ordered) else min(start+8,len(page_text)))-start <= 14]
    # OCR front matter only when its PDF text is missing. Image-conversion
    # bookmarks such as 001, IMG_002 or Screenshot.pdf are never lesson titles.
    front = range(min(12,len(page_text)))
    if sum(len(page_text[i]) for i in front) < 700:
        front_ocr = ocr_pdf(raw,front)
        for i,t in front_ocr.items():
            page_text[i]=t
    if isinstance(raw, Path):
        visual = visual_chapter_starts(raw,len(page_text)," ".join(page_text[:12]))
        if visual:
            return visual
    # Many CERD scans use a chapter list without page numbers. Read its real
    # titles, then confirm their occurrence on actual chapter opening pages.
    toc_lines = "\n".join(page_text[:min(12,len(page_text))]).splitlines()
    chapter_titles = []
    for i, line in enumerate(toc_lines):
        match = re.search(r"\b(?:chapter|chapitre)\s*(\d+)\s*:\s*(.*)",line,re.I)
        if not match:
            continue
        title = match.group(2).strip(" -:.") or next(
            (x.strip(" -:.") for x in toc_lines[i+1:i+4] if len(x.strip()) > 5), "")
        if len(title) > 4 and len(title) < 90:
            chapter_titles.append((int(match.group(1)),title))
    if chapter_titles:
        probe = range(12,min(len(page_text),65))
        for i in probe:
            if len(page_text[i]) < 80:
                page_text[i] = ocr_pdf(raw,[i])[i]
        matches = []
        for n,title in chapter_titles:
            words = [w for w in re.findall(r"[A-Za-z]{3,}",title.casefold())
                     if w not in {"chapter","chapitre"}]
            if not words:
                continue
            found = [i for i in probe if
                     re.search(rf"\b(?:chapter|chapitre)\s*{n}\b",
                               page_text[i][:750],re.I)
                     and sum(w in page_text[i][:1000].casefold() for w in words)
                     >= max(1,len(words)-1)]
            if len(found) == 1:
                matches.append((found[0],title))
        ordered = sorted(set(matches))
        if ordered:
            return [(title,start,ordered[j+1][0] if j+1<len(ordered)
                     else min(start+8,len(page_text)))
                    for j,(start,title) in enumerate(ordered)
                    if 2 <= (ordered[j+1][0] if j+1<len(ordered)
                             else min(start+8,len(page_text)))-start <= 14]
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
        if len(title.split()) < 2:
            continue
        matches = [i for i, text in enumerate(page_text[5:], 5)
                   if re.search(re.escape(title), text[:1600], re.I)]
        if len(matches) == 1:
            found.append((matches[0], title))
    ordered = sorted(set(found))
    if len(ordered) < 2:
        raise ValueError("SOURCE_TOC_AMBIGUOUS: cannot locate two distinct lesson starts")
    return [(title, start, ordered[i+1][0] if i+1 < len(ordered)
             else min(start+8, len(page_text))) for i, (start, title) in enumerate(ordered)]


def lesson_key(book, title, start):
    return hashlib.sha256(f"{book['drive_file_id']}|{title}|{start}".encode()).hexdigest()[:20]


def source_excerpt(reader, raw, start, end):
    if end <= start or end-start > 14:
        raise ValueError("SOURCE_BOUNDARY_AMBIGUOUS")
    pages = [(i+1, (reader.pages[i].extract_text() or "").strip())
             for i in range(start, end)]
    missing = [i for i in range(start,end) if len(pages[i-start][1]) < 80]
    if missing:
        scanned = ocr_pdf(raw, missing)
        pages = [(i+1, scanned.get(i, pages[i-start][1])) for i in range(start,end)]
    if sum(len(t) for _, t in pages) < 1100:
        raise ValueError("SOURCE_TEXT_INSUFFICIENT_OR_SCANNED")
    if sum(len(t) for _, t in pages) > 42000:
        raise ValueError("SOURCE_TOO_LONG_FOR_VERIFIABLE_GENERATION")
    return pages


def generate(title, pages, language):
    from openai import OpenAI
    source = "\n".join(f"[PDF PAGE {p}]\n{t}" for p, t in pages)
    messages = [
            {"role": "system", "content": (
                "Create a complete, accurate classroom lesson solely from the supplied PDF text. "
                "Return JSON with keys title, introduction, concepts (array of objects: heading, explanation, "
                "source_quote, pdf_page), activities (array of objects: prompt, answer, source_quote, pdf_page), "
                "questions (array of objects: prompt, options [exactly 3 strings], correct_index [0..2], "
                "explanation, source_quote, pdf_page), summary (array of strings). "
                "At least 3 concepts, 2 activities, 3 questions and 4 summary points. "
                "Each source_quote must be an exact contiguous excerpt of the supplied page text; "
                "do not invent source exercises or answers. If insufficient evidence return {error: reason}. "
                "Never copy or reuse GitHub HTML. Write in the textbook's language.")},
            {"role": "user", "content": f"Book language: {language}; TOC title: {title}\n{source}"},
        ]
    errors = []
    for provider, api_key, base_url, model in configured_providers():
        try:
            client = OpenAI(api_key=api_key, base_url=base_url,
                            timeout=90, max_retries=0)
            response = client.chat.completions.create(
                model=os.getenv("NABIL_LESSON_MODEL", model),
                temperature=0, response_format={"type": "json_object"},
                messages=messages)
            result = json.loads(response.choices[0].message.content)
            if result.get("error"):
                raise ValueError("GENERATION_REFUSED: " + str(result["error"])[:200])
            return result
        except Exception as exc:
            errors.append(f"{provider}: {type(exc).__name__}: {str(exc)[:180]}")
    raise RuntimeError("ALL_CONFIGURED_PROVIDERS_FAILED: " + " | ".join(errors))


def configured_providers():
    """Use existing platform credentials, in its configured priority order."""
    options = {
        "groq": ("GROQ_API_KEY", "https://api.groq.com/openai/v1",
                 os.getenv("GROQ_TEXT_MODEL", "openai/gpt-oss-120b")),
        "openrouter": ("OPENROUTER_API_KEY", "https://openrouter.ai/api/v1",
                       os.getenv("OPENROUTER_TEXT_MODEL", "openrouter/free")),
        "gemini": ("GEMINI_API_KEY", "https://generativelanguage.googleapis.com/v1beta/openai/",
                   os.getenv("GEMINI_TEXT_MODEL", "gemini-3.6-flash")),
        "openai": ("OPENAI_API_KEY", None, os.getenv("OPENAI_TEXT_MODEL", "gpt-5.5")),
    }
    order = os.getenv("NABIL_AI_PROVIDER_ORDER", "groq,openrouter,gemini,openai")
    result = []
    # Railway may configure a partial or outdated order. Never silently hide
    # a configured key merely because its provider is absent from that list.
    names = dict.fromkeys([*(x.strip().lower() for x in order.split(",")),
                           "groq", "openrouter", "gemini", "openai"])
    for name in names:
        if name not in options:
            continue
        env, base, model = options[name]
        if os.getenv(env, "").strip():
            result.append((name, os.environ[env], base, model))
    return result


def check_content(lesson, title, pages):
    errors = []
    if re.sub(r"\W+", "", str(lesson.get("title", "")).casefold()) != re.sub(r"\W+", "", title.casefold()):
        errors.append("TITLE_MISMATCH")
    requirements = (("concepts", 3), ("activities", 2), ("questions", 3), ("summary", 4))
    for field, minimum in requirements:
        if not isinstance(lesson.get(field), list) or len(lesson[field]) < minimum:
            errors.append("INSUFFICIENT_" + field.upper())
    by_page = dict(pages)
    for section in ("concepts", "activities", "questions"):
        for i, item in enumerate(lesson.get(section, [])):
            try:
                quote = str(item["source_quote"]).strip()
                page = int(item["pdf_page"])
                if len(quote) < 15 or quote not in by_page[page]:
                    raise ValueError()
                if section == "questions" and (len(item["options"]) != 3 or
                    type(item["correct_index"]) is not int or not 0 <= item["correct_index"] < 3):
                    raise ValueError()
            except (ValueError, KeyError, TypeError):
                errors.append(f"UNVERIFIED_{section}_{i+1}")
    if len(str(lesson.get("introduction", ""))) < 60:
        errors.append("INTRODUCTION_TOO_SHORT")
    return errors


def render_html(lesson, pages, book):
    e = lambda value: html.escape(str(value), quote=True)
    cards = "".join(
        f'<section class="card"><h2>{e(x["heading"])}</h2><p>{e(x["explanation"])}</p>'
        f'<small>PDF p. {int(x["pdf_page"])} · {e(book["title"])}</small></section>'
        for x in lesson["concepts"])
    activities = "".join(
        f'<details class="card"><summary>{e(x["prompt"])}</summary><p>{e(x["answer"])}</p>'
        f'<small>PDF p. {int(x["pdf_page"])}</small></details>' for x in lesson["activities"])
    questions = "".join(
        f'<fieldset class="card" data-answer="{x["correct_index"]}"><legend>{e(x["prompt"])}</legend>'
        + "".join(f'<label><input type="radio" name="q{i}" value="{j}">{e(option)}</label>'
                  for j, option in enumerate(x["options"]))
        + f'<button type="button" class="check">Check</button><output aria-live="polite"></output>'
          f'<span class="explanation" hidden>{e(x["explanation"])}</span></fieldset>'
        for i, x in enumerate(lesson["questions"]))
    summary = "".join(f"<li>{e(s)}</li>" for s in lesson["summary"])
    refs = ", ".join(str(p) for p, _ in pages)
    return f'''<!doctype html><html lang="{e(book.get("language", "en"))[:2].lower()}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(lesson["title"])} · NABIL AI</title>
<style>body{{margin:0;background:#edf3f9;color:#14263e;font:1.1rem/1.65 system-ui}}
main{{max-width:900px;margin:auto;padding:16px}}header,.card{{background:white;border-radius:18px;
padding:18px;margin:14px 0;box-shadow:0 3px 14px #15304a1a}}header{{background:#173b69;color:white}}
h1{{line-height:1.2}}h2{{color:#125b8f}}header small{{color:#e3f1ff}}small{{color:#315a7a}}
label{{display:block;padding:9px;margin:8px 0;border:1px solid #bed2e3;border-radius:9px}}
button{{background:#096c83;color:white;border:0;border-radius:9px;padding:10px 18px;font:inherit}}
output{{display:block;font-weight:700}}details summary{{cursor:pointer;font-weight:700}}
@media(max-width:500px){{main{{padding:9px}}.card,header{{padding:14px}}}}</style></head>
<body><main><header><h1>{e(lesson["title"])}</h1><p>{e(lesson["introduction"])}</p>
<small>{e(book["title"])} · PDF pages {refs}</small></header>
<h2>Learn</h2>{cards}<h2>Explore and solve</h2>{activities}
<h2>Interactive worksheet</h2>{questions}<section class="card"><h2>Lesson summary</h2><ul>{summary}</ul></section>
<section class="card"><h2>Source</h2><p>{e(book["title"])} · Drive PDF ID {e(book["drive_file_id"])} · PDF pages {refs}</p></section>
</main><script>document.querySelectorAll("fieldset").forEach(f=>f.querySelector("button").onclick=()=>{{
const choice=f.querySelector("input:checked"),out=f.querySelector("output");
out.textContent=choice?(Number(choice.value)===Number(f.dataset.answer)?"✓ Correct":"Try again · "+f.querySelector(".explanation").textContent):"Choose an answer first";
}});</script></body></html>'''


def check_html(document, lesson):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(document, "html.parser")
    errors = []
    if not soup.select_one("meta[name=viewport]") or not soup.select_one("main"):
        errors.append("MOBILE_OR_SEMANTIC_STRUCTURE_MISSING")
    if len(soup.select("fieldset[data-answer]")) != len(lesson["questions"]):
        errors.append("QUIZ_RENDER_MISMATCH")
    if len(soup.select("details")) != len(lesson["activities"]):
        errors.append("ACTIVITY_RENDER_MISMATCH")
    if "querySelectorAll" not in document or len(document.encode()) < 3500:
        errors.append("INTERACTIVITY_OR_CONTENT_MISSING")
    return errors


def make_pptx(lesson, book, pages):
    """A separate visual export; all shapes and text are generated from checked JSON."""
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.33), Inches(7.5)
    def slide(title, body, n):
        s = prs.slides.add_slide(prs.slide_layouts[6])
        bg = s.background.fill
        bg.solid()
        bg.fore_color.rgb = RGBColor(14, 40, 74)
        for x, y, w, h, color in ((.55, .7, .12, 5.8, RGBColor(33, 199, 187)),
                                  (.85, 1.95, 11.7, 4.5, RGBColor(24, 72, 115))):
            shape = s.shapes.add_shape(1, Inches(x), Inches(y), Inches(w), Inches(h))
            shape.fill.solid(); shape.fill.fore_color.rgb = color
            shape.line.fill.background()
        def textbox(value, x, y, w, h, size, color):
            shape = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
            tf = shape.text_frame; tf.word_wrap = True
            tf.text = str(value)
            for p in tf.paragraphs:
                p.font.size = Pt(size); p.font.color.rgb = color
        textbox(title, 1, .55, 11.4, 1.2, 34, RGBColor(255,255,255))
        textbox(body[:1050], 1.25, 2.2, 10.9, 3.85, 23, RGBColor(239,248,255))
        textbox(f'NABIL AI  •  {book["title"]}  •  PDF pp. {pages[0][0]}–{pages[-1][0]}  •  {n}',
                1, 6.7, 11.3, .4, 12, RGBColor(111, 222, 214))
    slide(lesson["title"], lesson["introduction"], 1)
    for i, item in enumerate(lesson["concepts"], 2):
        slide(item["heading"], item["explanation"] + f'\n\nSource: PDF p. {item["pdf_page"]}', i)
    offset = len(prs.slides)
    for i, item in enumerate(lesson["activities"], offset+1):
        slide("Explore · " + item["prompt"], item["answer"], i)
    slide("Quick review", "\n• ".join(lesson["summary"]), len(prs.slides)+1)
    stream = io.BytesIO(); prs.save(stream)
    return stream.getvalue()


def check_pptx(raw, lesson):
    from pptx import Presentation
    slides = list(Presentation(io.BytesIO(raw)).slides)
    if len(slides) != 2 + len(lesson["concepts"]) + len(lesson["activities"]):
        return ["PPTX_SLIDE_COUNT_MISMATCH"]
    text = "\n".join(shape.text for slide in slides for shape in slide.shapes if shape.has_text_frame)
    missing = [x["heading"] for x in lesson["concepts"] if x["heading"] not in text]
    return ["PPTX_CONCEPT_MISSING: " + x for x in missing]


def ensure_folder(service, parent, name):
    safe = name.replace("'", "\\'")
    result = service.files().list(q=f"'{parent}' in parents and name='{safe}' and mimeType='{FOLDER_MIME}' and trashed=false",
                                  fields="files(id,name)", pageSize=10).execute().get("files", [])
    if len(result) > 1:
        raise ValueError("AMBIGUOUS_DRIVE_FOLDER")
    if result:
        return result[0]["id"]
    created = service.files().create(body={"name":name, "mimeType":FOLDER_MIME, "parents":[parent]},
                                     fields="id").execute()
    return created["id"]


def upload_verified(service, parent, name, raw, mime):
    from googleapiclient.http import MediaIoBaseUpload
    item = service.files().create(body={"name":name, "parents":[parent]},
        media_body=MediaIoBaseUpload(io.BytesIO(raw), mimetype=mime, resumable=False),
        fields="id,name,size,webViewLink").execute()
    readback = download(service, item["id"])
    if hashlib.sha256(readback).digest() != hashlib.sha256(raw).digest():
        raise ValueError("DRIVE_READBACK_HASH_MISMATCH")
    return item


def run(report_path):
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    report = {"started":now(), "status":"RUNNING", "attempts":[], "production":None}
    def checkpoint():
        report["updated"] = now()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    checkpoint()
    try:
        service = owner_drive()
        root = service.files().get(fileId=ROOT_FOLDER, fields="id,name,capabilities(canAddChildren)").execute()
        if not root.get("capabilities", {}).get("canAddChildren"):
            raise PermissionError("OWNER_ROOT_NOT_WRITABLE")
    except Exception as exc:
        report["status"]="BLOCKED_CREDENTIALS_OR_DRIVE"
        report["error"]=f"{type(exc).__name__}: {exc}"
        checkpoint(); return report
    if not configured_providers():
        report["status"]="BLOCKED_GENERATION_CREDENTIALS"
        report["error"]="NO_CONFIGURED_AI_PROVIDER_KEY"
        checkpoint(); return report
    seen_ids = set()
    priority = {name:i for i,name in enumerate(ledger.get("priority", []))}
    def book_order(book):
        grade = re.search(r"\d+",book.get("grade",""))
        return (priority.get(book.get("subject"),999),
                int(grade.group()) if grade else 999,
                book.get("order",999),book.get("language","")!="English")
    for book in sorted(ledger["books"], key=book_order):
        if not book.get("drive_file_id"):
            continue
        if book["drive_file_id"] in seen_ids:
            continue
        seen_ids.add(book["drive_file_id"])
        attempt = {"book":book["title"],"book_id":book["drive_file_id"],"started":now()}
        report["attempts"].append(attempt); checkpoint()
        try:
            from pypdf import PdfReader
            temp = tempfile.TemporaryDirectory(prefix="nabil_book_")
            pdf = Path(temp.name) / "book.pdf"
            download_pdf_to_path(service, book["drive_file_id"], pdf)
            reader = PdfReader(str(pdf))
            entries = candidates(reader,pdf)
            finished = {x.get("lesson_key") for x in book.get("authored_lessons",[])
                        if x.get("status") == "verified_complete" and x.get("drive_html_id")
                        and x.get("drive_pptx_id")}
            available = [(title, start, end) for title, start, end in entries
                         if lesson_key(book,title,start) not in finished]
            if not available:
                raise ValueError("NO_UNFINISHED_TOC_LESSON")
            title, start, end = available[0]
            attempt.update({"lesson":title,"source_pdf_pages":list(range(start+1,end+1)),
                            "lesson_key":lesson_key(book,title,start)})
            pages = source_excerpt(reader,pdf,start,end)
            digest = hashlib.sha256()
            with pdf.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024*1024), b""):
                    digest.update(chunk)
            attempt["source_sha256"]=digest.hexdigest()
            checkpoint()
            lesson = generate(title,pages,book.get("language",""))
            failures = check_content(lesson,title,pages)
            document = render_html(lesson,pages,book) if not failures else ""
            failures.extend(check_html(document,lesson) if document else [])
            attempt["html_quality"]={"pass":not failures,"failures":failures}
            checkpoint()
            if failures:
                raise ValueError("HTML_QUALITY_FAILED: " + ",".join(failures))
            powerpoint = make_pptx(lesson,book,pages)
            failures = check_pptx(powerpoint,lesson)
            attempt["pptx_quality"]={"pass":not failures,"failures":failures,"slides":2+len(lesson["concepts"])+len(lesson["activities"])}
            checkpoint()
            if failures:
                raise ValueError("PPTX_QUALITY_FAILED: " + ",".join(failures))
            grade_folder = ensure_folder(service,ROOT_FOLDER,book["grade"])
            subject_folder = ensure_folder(service,grade_folder,book["subject"])
            folder = ensure_folder(service,subject_folder,title)
            base = re.sub(r"[^a-zA-Z0-9_-]+","-",title).strip("-")[:55] or attempt["lesson_key"]
            html_item = upload_verified(service,folder,base+".html",document.encode("utf-8"),"text/html")
            attempt["drive_html_id"]=html_item["id"]; checkpoint()
            ppt_item = upload_verified(service,folder,base+".pptx",powerpoint,
                                       "application/vnd.openxmlformats-officedocument.presentationml.presentation")
            attempt["drive_pptx_id"]=ppt_item["id"]
            attempt["status"]="VERIFIED_UPLOAD"
            record = {"title":title,"lesson_key":attempt["lesson_key"],
                      "source_pdf_pages":attempt["source_pdf_pages"],"source_sha256":attempt["source_sha256"],
                      "drive_folder_id":folder,"drive_html_id":html_item["id"],"drive_pptx_id":ppt_item["id"],
                      "status":"verified_complete","completed_at":now()}
            book.setdefault("authored_lessons",[]).append(record)
            ledger["updated"]=now()
            LEDGER.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
            report["production"]=record
            report["status"]="ONE_LESSON_COMPLETE"
            checkpoint()
            break
        except Exception as exc:
            attempt.update({"status":"FAILED","reason":f"{type(exc).__name__}: {exc}","finished":now()})
            checkpoint()
        finally:
            if "temp" in locals():
                temp.cleanup()
                del temp
    else:
        report["status"]="NO_LESSON_COMPLETE"; checkpoint()
    return report


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--report",default="data/nabil_lesson_factory_run.json")
    args=parser.parse_args()
    report=run(Path(args.report))
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if report["status"]=="ONE_LESSON_COMPLETE" else 2


if __name__=="__main__":
    sys.exit(main())
