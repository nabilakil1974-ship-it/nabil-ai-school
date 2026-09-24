"""Produce at most one verified, source-grounded lesson from registered Drive PDFs.

Usage: python -m scripts.nabil_lesson_factory --report /tmp/nabil-lesson-run.json
Requires owner Drive OAuth and an existing configured AI provider key. A failed candidate is
logged and the next registered book is tried. No existing HTML is read.
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

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data/interactive_lesson_production_ledger.json"
FOLDER_MIME = "application/vnd.google-apps.folder"
ROOT_FOLDER = os.getenv("NABIL_LESSON_DRIVE_ROOT", "16bcmZMO_dn4FqlGaDtl8Hky6iSBEqZpX")
RUN_DEADLINE = None
BOOK_DEADLINE = None
PROGRESS_STARTED = None


def now():
    return datetime.now(timezone.utc).isoformat()


def progress(stage, **details):
    elapsed=round(time.monotonic()-PROGRESS_STARTED,1) if PROGRESS_STARTED else 0
    print(json.dumps({"time":now(),"elapsed_seconds":elapsed,"stage":stage,**details},
                     ensure_ascii=False),flush=True)


def bounded(command, seconds, **kwargs):
    """Kill the whole OCR process group when a page exceeds its time budget."""
    remaining=min([seconds,*([RUN_DEADLINE-time.monotonic()] if RUN_DEADLINE else []),
                   *([BOOK_DEADLINE-time.monotonic()] if BOOK_DEADLINE else [])])
    if remaining <= 0:
        raise TimeoutError("RUN_DEADLINE_EXCEEDED")
    process=subprocess.Popen(command,start_new_session=True,**kwargs)
    try:
        out,err=process.communicate(timeout=remaining)
    except BaseException:
        os.killpg(process.pid,signal.SIGKILL)
        process.communicate()
        raise
    if process.returncode:
        raise subprocess.CalledProcessError(process.returncode,command,output=out,stderr=err)
    return out


def vision_page_text(image, page):
    """Transcribe the rendered page with an available vision-capable provider."""
    from openai import OpenAI
    models={
        "openai":os.getenv("OPENAI_VISION_MODEL","gpt-4.1-mini"),
        "gemini":os.getenv("GEMINI_VISION_MODEL","gemini-2.5-flash"),
        "openrouter":os.getenv("OPENROUTER_VISION_MODEL","openrouter/free"),
        "groq":os.getenv("GROQ_VISION_MODEL","meta-llama/llama-4-scout-17b-16e-instruct"),
    }
    errors=[]
    for provider,key,base,_ in configured_providers():
        remaining=min([20,*([RUN_DEADLINE-time.monotonic()] if RUN_DEADLINE else []),
                       *([BOOK_DEADLINE-time.monotonic()] if BOOK_DEADLINE else [])])
        if remaining<=0:
            raise TimeoutError("VISION_DEADLINE_EXCEEDED")
        try:
            response=OpenAI(api_key=key,base_url=base,timeout=remaining,max_retries=0
                ).chat.completions.create(
                    model=models[provider],
                    messages=[{"role":"user","content":[
                        {"type":"text","text":"Transcribe ALL visible textbook text in reading order. Preserve section titles, formulas, exercise numbers and page numbers. Do not answer exercises or invent illegible text."},
                        {"type":"image_url","image_url":{"url":"data:image/jpeg;base64,"+base64.b64encode(image).decode()}}
                    ]}])
            text=(response.choices[0].message.content or "").strip()
            if len(text)>=80:
                progress("VISION_OK",page=page,provider=provider,characters=len(text))
                return text
            errors.append(provider+":INSUFFICIENT_TEXT")
        except Exception as exc:
            errors.append(provider+":"+type(exc).__name__)
    raise ValueError(f"OCR_AND_VISION_FAILED_PAGE_{page}: "+",".join(errors))


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


def ocr_pdf(raw, page_indices, vision_on_failure=False):
    """OCR selected pages; scanned books have no extractable PDF text."""
    with tempfile.TemporaryDirectory(prefix="nabil_toc_") as directory:
        pdf = Path(directory) / "source.pdf"
        if isinstance(raw, Path):
            pdf = raw
        else:
            pdf.write_bytes(raw)
        result = {}
        for index in page_indices:
            if (RUN_DEADLINE and time.monotonic()>=RUN_DEADLINE
                or BOOK_DEADLINE and time.monotonic()>=BOOK_DEADLINE):
                raise TimeoutError("OCR_BUDGET_EXCEEDED")
            prefix = str(Path(directory) / f"page_{index}")
            progress("SOURCE_RENDER",page=index+1)
            bounded(["pdftoppm", "-f", str(index+1), "-l", str(index+1),
                     "-singlefile", "-r", "140", "-jpeg", str(pdf), prefix],
                    8,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
            progress("OCR",page=index+1)
            try:
                text=bounded(["tesseract", prefix+".jpg", "stdout", "-l", "eng"],
                             7,stdout=subprocess.PIPE,stderr=subprocess.PIPE).decode("utf-8","replace").strip()
            except subprocess.TimeoutExpired:
                progress("OCR_TIMEOUT_VISION",page=index+1)
                text=(vision_page_text(Path(prefix+".jpg").read_bytes(),index+1)
                      if vision_on_failure else "")
            if len(text)<80 and vision_on_failure:
                progress("OCR_INSUFFICIENT_VISION",page=index+1)
                text=vision_page_text(Path(prefix+".jpg").read_bytes(),index+1)
            result[index]=text
            progress("SOURCE_PAGE_READY",page=index+1,characters=len(text))
        return result


def trustworthy_title(title):
    words=re.findall(r"[A-Za-zÀ-ÿ]+",str(title))
    if (not words or len(title)>90 or
        re.search(r"\.(?:pdf|jpg|png)|^(?:img|screenshot)[_ -]|^\d+$",
                  title,re.I) or
        title.casefold().strip() in {"introduction","foreword","préface","livre"}):
        return False
    # One short OCR word is especially likely to be a truncated heading.
    return len(words)>1 or len(words[0])>=6


def visual_chapter_starts(pdf, total_pages, toc_text):
    """Read the upper title band of actual page images, checking the TOC.

    Full-page OCR commonly misses decorative colored headings. No PDF
    bookmark or filename is accepted as a chapter title in scanned books.
    """
    from PIL import Image, ImageEnhance, ImageOps
    chapters = []
    with tempfile.TemporaryDirectory(prefix="nabil_headers_") as directory:
        for index in range(10, min(total_pages, 45)):
            if BOOK_DEADLINE and time.monotonic()>=BOOK_DEADLINE:
                raise TimeoutError("BOOK_DISCOVERY_BUDGET_EXCEEDED")
            progress("HEADER_SCAN",page=index+1)
            prefix = str(Path(directory) / "page")
            bounded(["pdftoppm", "-f", str(index+1), "-l", str(index+1),
                     "-singlefile", "-r", "150", "-jpeg", str(pdf), prefix],
                    8,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
            picture = Image.open(prefix+".jpg")
            band = picture.crop((0,0,picture.width,int(picture.height*.19)))
            ImageEnhance.Contrast(ImageOps.grayscale(band)).enhance(2).save(prefix+"_top.png")
            try:
                title_band=bounded(
                    ["tesseract", prefix+"_top.png", "stdout", "-l", "eng", "--psm", "6"],
                    5,stdout=subprocess.PIPE,stderr=subprocess.PIPE).decode("utf-8","replace")
            except subprocess.TimeoutExpired:
                progress("HEADER_OCR_TIMEOUT",page=index+1)
                title_band=""
            found = re.search(r"(?:\b(?:chapter|chapitre)\s*|^\W*)"
                              r"(\d{1,2})\s*[:.\-]\s*"
                              r"([A-Za-z][A-Za-z '&\-]{4,65})",title_band,re.I|re.M)
            if not found:
                continue
            number, title = int(found.group(1)), found.group(2).strip(" .-")
            if not trustworthy_title(title):
                progress("TITLE_REJECTED_OCR_FRAGMENT",page=index+1,title=title)
                continue
            words = re.findall(r"[A-Za-z]{4,}",title.lower())
            if not words or sum(bool(re.search(r"\b"+re.escape(w)+r"\b",
                                              toc_text,re.I)) for w in words) < max(1,len(words)-1):
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
                          if p > 0 and trustworthy_title(t)
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
        if trustworthy_title(title):
            chapter_titles.append((int(match.group(1)),title))
    if chapter_titles:
        # Do not OCR 50+ full pages merely to find chapter headings. The
        # bounded rendered-header scan above has already tried this source.
        probe = range(12,min(len(page_text),65))
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
        if not trustworthy_title(title):
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


def visual_candidates(images):
    """Unverified figure observations proposed from page pixels, never approvals."""
    providers = configured_providers()
    if len({p[0] for p in providers}) < 3:
        raise RuntimeError("THREE_INDEPENDENT_PROVIDERS_REQUIRED")
    from openai import OpenAI
    selected = os.getenv("NABIL_VISUAL_PROVIDER", "").strip().lower()
    reserved_reviewer = os.getenv("NABIL_REVIEWER_PROVIDER", "").strip().lower()
    choices = [p for p in providers if p[0] != reserved_reviewer
               and (not selected or p[0] == selected)]
    if not choices:
        raise RuntimeError("VISUAL_EXTRACTOR_UNAVAILABLE")
    name, key, base, default_model = choices[0]
    model = os.getenv("NABIL_VISUAL_MODEL", default_model)
    if not model:
        raise RuntimeError("VISUAL_MODEL_NOT_CONFIGURED")
    client = OpenAI(api_key=key, base_url=base, timeout=45, max_retries=0)
    candidates = {}
    for page, image in images.items():
        messages = [
            {"role": "system", "content": (
                "Describe only visible figures, graphs, circuits, apparatus, structures and "
                "geometry on this textbook page. Identify a printed figure label if visible; "
                "otherwise use a short location description. Keep observed relationships "
                "separate from inferences. Never answer an activity from general knowledge. "
                "Return JSON {items:[{figure_id:string, observation:string, "
                "accompanying_question:string}]}.")},
            {"role": "user", "content": [
                {"type": "text", "text": f"PDF page {page}; extract tentative visual observations."},
                {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," +
                    base64.b64encode(image).decode("ascii")}}]},
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
            progress("VISUAL_CANDIDATE_EXTRACTION_FAILED", page=page,
                     error_type=type(exc).__name__)
    return candidates, name, model


def evidence_catalog(pages, candidates=None):
    """Immutable literal spans from each PDF page; IDs carry page provenance."""
    catalog={}
    for page,text in pages:
        chunks=re.split(r"\n\s*\n",text)
        if len(chunks)<3:
            chunks=text.splitlines()
        buffer=""
        serial=0
        for part in chunks:
            part=part.strip()
            if not part:
                continue
            if len(buffer)+len(part)<220:
                buffer+=(("\n" if buffer else "")+part)
                continue
            if buffer:
                serial+=1; catalog[f"P{page}-{serial}"]={"page":page,"text":buffer}
                buffer=""
            while len(part)>320:
                serial+=1; catalog[f"P{page}-{serial}"]={"page":page,"text":part[:300]}
                part=part[300:]
            buffer=part
        if buffer:
            serial+=1; catalog[f"P{page}-{serial}"]={"page":page,"text":buffer}
    catalog.update(candidates or {})
    return catalog


def source_evidence_map(title, pages, catalog, visual_provider=None,
                        visual_model=None):
    """Index source spans by the educational roles visibly present in the PDF.

    Classification is only an index. Text spans are literal source excerpts;
    visual candidates require independent review against the original image.
    """
    patterns={
        "objectives":r"objectives?|learn|aims?",
        "definitions":r"defined|is called|is a |are called|consists of",
        "laws":r"formula|law|horizontal|equal|unit|measure|=|proportional",
        "examples":r"example|for instance|e\.g\.",
        "activities":r"activity|experiment|observe|try|place|take a",
        "figures":r"figure|fig\.|draw|diagram|vessel|surface",
        "exercises":r"exercise|calculate|complete|explain|question",
        "symbols_units":r"\b(?:cm|mm|kg|g|mL|L|N|V|A|Ω)\b|symbol|units?",
    }
    categories={name:[key for key,entry in catalog.items()
                      if re.search(pattern,entry["text"],re.I)]
                for name,pattern in patterns.items()}
    return {"title":title,"source_pdf_pages":[page for page,_ in pages],
            "categories":categories,"evidence":catalog,
            "visual_extractor_provider":visual_provider,
            "visual_extractor_model":visual_model,
            "visual_evidence_status":"unverified_candidates"}


def record_role_provenance(evidence_map, attempt, role, provider, model):
    """Keep the on-disk evidence map and attempt report role identities aligned."""
    if role not in ("generator", "visual_extractor", "reviewer"):
        raise ValueError("UNKNOWN_PROVENANCE_ROLE")
    for suffix, value in (("provider", provider), ("model", model)):
        key = f"{role}_{suffix}"
        evidence_map[key] = value
        attempt[key] = value


def attach_evidence(lesson,catalog):
    if lesson.get("introduction_evidence_id") in catalog:
        entry=catalog[lesson["introduction_evidence_id"]]
        lesson["introduction_source_page"]=entry["page"]
        lesson["introduction_source_quote"]=entry["text"]
    for section in ("concepts","activities","questions","exercises","summary"):
        for item in lesson.get(section,[]):
            evidence=catalog.get(str(item.get("evidence_id","")))
            if evidence:
                item["pdf_page"]=evidence["page"]
                item["source_quote"]=evidence["text"]
                if evidence.get("type")=="visual_candidate":
                    item["unverified_visual_candidate"]={
                        "figure_id":evidence["figure_id"],
                        "observation":evidence["text"],
                        "accompanying_question":evidence["accompanying_question"]}


def source_excerpt(reader, raw, start, end):
    if end <= start or end-start > 14:
        raise ValueError("SOURCE_BOUNDARY_AMBIGUOUS")
    pages = [(i+1, (reader.pages[i].extract_text() or "").strip())
             for i in range(start, end)]
    for number,text in pages:
        if len(text)>=80:
            progress("SOURCE_TEXT",page=number,characters=len(text))
    missing = [i for i in range(start,end) if len(pages[i-start][1]) < 80]
    if missing:
        scanned = ocr_pdf(raw, missing, vision_on_failure=True)
        pages = [(i+1, scanned.get(i, pages[i-start][1])) for i in range(start,end)]
    if sum(len(t) for _, t in pages) < 1100:
        raise ValueError("SOURCE_TEXT_INSUFFICIENT_OR_SCANNED")
    if sum(len(t) for _, t in pages) > 42000:
        raise ValueError("SOURCE_TOO_LONG_FOR_VERIFIABLE_GENERATION")
    return pages


def parse_provider_json(client,provider,messages,response,model):
    content=response.choices[0].message.content
    if content is None and provider=="openrouter":
        # Some OpenRouter free routes do not populate content under JSON mode.
        # Retry once using plain chat before moving to the next free provider.
        retry=client.chat.completions.create(
            model=model,temperature=0,
            messages=[{"role":"system","content":"Return a valid JSON object only."},*messages])
        content=retry.choices[0].message.content
    if not isinstance(content,str) or not content.strip():
        raise ValueError(provider.upper()+"_EMPTY_RESPONSE")
    value=content.strip()
    if value.startswith("```"):
        value=re.sub(r"^```(?:json)?\s*|\s*```$","",value,flags=re.I).strip()
    result=json.loads(value)
    if not isinstance(result,dict):
        raise ValueError(provider.upper()+"_NON_OBJECT_RESPONSE")
    return result


def generate(title, pages, language, evidence_map, previous_failures=None,
             visual_provider=None, visual_model=None):
    from openai import OpenAI
    catalog=evidence_map["evidence"]
    source = json.dumps(evidence_map,ensure_ascii=False)
    messages = [
            {"role": "system", "content": (
                "Create a complete, accurate classroom lesson from the supplied source map. "
                "Visual candidates are unverified observations, never authoritative facts. "
                "Return JSON with keys title, introduction, introduction_evidence_id, "
                "concepts (array of objects: heading, explanation, "
                "evidence_id, visual_evidence_id, example if source has one), "
                "activities (array of objects: prompt, answer, evidence_id), "
                "questions (array of objects: prompt, options [exactly 3 strings], correct_index [0..2], "
                "explanation, evidence_id), exercises (array of objects: "
                "prompt, solution, solution_steps [array of explanatory steps], evidence_id), "
                "summary (array of objects: text, evidence_id). "
                "At least 3 concepts, 2 activities, 3 questions, 2 fully worked exercises "
                "and 4 summary points. Exercises should be taken from source pages, with "
                "solutions consistent with the source; if an exercise depends on a figure "
                "you cannot interpret, do not invent its solution. "
                "Each concept's visual_evidence_id must identify the source page with the figure or "
                "observation for that concept; use its own evidence_id if the page itself is the visual. "
                "Every item must cite one evidence_id from the supplied catalog that directly supports "
                "the claim or answer. Never create an evidence_id or pretend a diagram shows a value. "
                "Do not invent source exercises or answers. A question in the source is NOT "
                "evidence for its answer: cite an explicit source statement or a fully "
                "verifiable worked derivation. For visual answers cite the relevant "
                "P{page}-VIS-{index} candidate, subject to independent image review. "
                "Omit any activity whose answer cannot be "
                "verified, and select another supported activity. If insufficient evidence "
                "return {error: reason}. "
                "Use the evidence map categories to cover objectives, concepts, activities, figures "
                "and exercises. Never copy or reuse GitHub HTML. Write in the textbook's language.")},
            {"role": "user", "content": f"Book language: {language}; TOC title: {title}\n{source}"},
        ]
    if previous_failures:
        messages.append({"role":"user","content":(
            "The independent scientific reviewer REJECTED the preceding draft. "
            "Regenerate from the source map without repeating these unsupported claims; "
            "do not merely change their citations: "
            + json.dumps(previous_failures,ensure_ascii=False))})
    errors = []
    reserved_reviewer = os.getenv("NABIL_REVIEWER_PROVIDER", "").strip().lower()
    eligible = [(provider, api_key, base_url,
                 os.getenv("NABIL_LESSON_MODEL", model))
                for provider, api_key, base_url, model in configured_providers()
                if provider not in (visual_provider, reserved_reviewer)
                and os.getenv("NABIL_LESSON_MODEL", model) != visual_model]
    if not eligible:
        raise RuntimeError("INDEPENDENT_REVIEWER_UNAVAILABLE")
    for provider, api_key, base_url, chosen_model in eligible:
        try:
            client = OpenAI(api_key=api_key, base_url=base_url,
                            timeout=90, max_retries=0)
            response = client.chat.completions.create(
                model=chosen_model,
                temperature=0, response_format={"type": "json_object"},
                messages=messages)
            result = parse_provider_json(client,provider,messages,response,
                                         chosen_model)
            if result.get("error"):
                raise ValueError("GENERATION_REFUSED: " + str(result["error"])[:200])
            attach_evidence(result,catalog)
            return result, provider, chosen_model
        except Exception as exc:
            errors.append(f"{provider}: {type(exc).__name__}: {str(exc)[:180]}")
    raise RuntimeError("ALL_CONFIGURED_PROVIDERS_FAILED: " + " | ".join(errors))


def configured_providers():
    """Use existing platform credentials, in its configured priority order."""
    cloudflare_account = os.getenv("CLOUDFLARE_ACCOUNT_ID", "").strip()
    options = {
        "groq": ("GROQ_API_KEY", "https://api.groq.com/openai/v1",
                 os.getenv("GROQ_TEXT_MODEL", "openai/gpt-oss-120b")),
        "openrouter": ("OPENROUTER_API_KEY", "https://openrouter.ai/api/v1",
                       os.getenv("OPENROUTER_TEXT_MODEL", "openrouter/free")),
        "gemini": ("GEMINI_API_KEY", "https://generativelanguage.googleapis.com/v1beta/openai/",
                   os.getenv("GEMINI_TEXT_MODEL", "gemini-3.6-flash")),
        "cloudflare": ("CLOUDFLARE_API_TOKEN",
                       f"https://api.cloudflare.com/client/v4/accounts/{cloudflare_account}/ai/v1",
                       os.getenv("CLOUDFLARE_TEXT_MODEL", "@cf/google/gemma-4-26b-a4b-it")),
        "openai": ("OPENAI_API_KEY", None, os.getenv("OPENAI_TEXT_MODEL", "gpt-5.5")),
    }
    order = os.getenv("NABIL_AI_PROVIDER_ORDER", "groq,openrouter,gemini,openai")
    result = []
    # Railway may configure a partial or outdated order. Never silently hide
    # a configured key merely because its provider is absent from that list.
    names = dict.fromkeys([*(x.strip().lower() for x in order.split(",")),
                           "groq", "openrouter", "gemini", "cloudflare", "openai"])
    for name in names:
        if name not in options:
            continue
        env, base, model = options[name]
        if name == "cloudflare" and not cloudflare_account:
            continue
        if name=="openai" and os.getenv("NABIL_LESSON_ALLOW_PAID_OPENAI")!="1":
            continue
        if os.getenv(env, "").strip():
            result.append((name, os.environ[env], base, model))
    return result


def check_content(lesson, title, pages, catalog):
    errors = []
    if re.sub(r"\W+", "", str(lesson.get("title", "")).casefold()) != re.sub(r"\W+", "", title.casefold()):
        errors.append("TITLE_MISMATCH")
    requirements = (("concepts", 3), ("activities", 2), ("questions", 3),
                    ("exercises", 2), ("summary", 4))
    for field, minimum in requirements:
        if not isinstance(lesson.get(field), list) or len(lesson[field]) < minimum:
            errors.append("INSUFFICIENT_" + field.upper())
    by_page = dict(pages)
    for section in ("concepts", "activities", "questions", "exercises", "summary"):
        for i, item in enumerate(lesson.get(section, [])):
            try:
                quote = str(item["source_quote"]).strip()
                page = int(item["pdf_page"])
                evidence=catalog[item["evidence_id"]]
                if evidence["page"]!=page or evidence["text"].strip()!=quote:
                    raise ValueError()
                if section=="concepts" and item["visual_evidence_id"] not in catalog:
                    raise ValueError()
                # PDF OCR inserts line breaks inside otherwise verbatim quotes.
                # Collapse whitespace only; never tolerate changed words or
                # fabricated source text.
                if (len(quote) < 15 or
                    (evidence.get("type") != "visual_candidate" and
                     re.sub(r"\s+"," ",quote) not in
                     re.sub(r"\s+"," ",by_page[page]))):
                    raise ValueError()
                if section == "questions" and (len(item["options"]) != 3 or
                    type(item["correct_index"]) is not int or not 0 <= item["correct_index"] < 3):
                    raise ValueError()
                if section == "exercises" and (len(str(item["prompt"])) < 15
                                                or len(str(item["solution"])) < 35
                                                or not isinstance(item.get("solution_steps"),list)
                                                or len(item["solution_steps"])<2):
                    raise ValueError()
            except (ValueError, KeyError, TypeError, IndexError):
                errors.append(f"UNVERIFIED_{section}_{i+1}")
    if len(str(lesson.get("introduction", ""))) < 60:
        errors.append("INTRODUCTION_TOO_SHORT")
    intro=catalog.get(lesson.get("introduction_evidence_id"))
    if (not intro or lesson.get("introduction_source_page")!=intro["page"]
        or lesson.get("introduction_source_quote")!=intro["text"]):
        errors.append("INTRODUCTION_EVIDENCE_INVALID")
    return errors


def repair_source_quotes(lesson,pages,catalog,failures,generator_provider):
    """One bounded attempt to replace invalid citations with catalog IDs.

    The original claims and answers remain unchanged; the scientific review
    still decides whether those claims are actually supported by the spans.
    """
    from openai import OpenAI
    targets=[]
    for failure in failures:
        found=re.fullmatch(r"UNVERIFIED_(concepts|activities|questions|exercises|summary)_(\d+)",failure)
        if found:
            section,index=found.group(1),int(found.group(2))-1
            targets.append({"section":section,"index":index,
                            "item":lesson[section][index]})
    if not targets:
        return False
    source=json.dumps(catalog,ensure_ascii=False)
    for provider,key,base,model in configured_providers():
        if provider != generator_provider:
            continue
        try:
            client=OpenAI(api_key=key,base_url=base,timeout=35,max_retries=0)
            messages=[
                {"role":"system","content":(
                    "Repair only source citations for these educational items. "
                    "Return JSON {repairs:[{section,index,evidence_id}]}. "
                    "Each evidence_id must exist in the supplied catalog and directly support "
                    "the item's claim or answer. If no supporting evidence "
                    "exists, omit that item. Do not change any lesson claim, exercise or answer.")},
                {"role":"user","content":json.dumps(
                    {"source":source,"targets":targets},ensure_ascii=False)},
            ]
            response=client.chat.completions.create(
                    model=os.getenv("NABIL_LESSON_MODEL",model),
                    temperature=0,response_format={"type":"json_object"},
                    messages=messages)
            data=parse_provider_json(client,provider,messages,response,
                                     os.getenv("NABIL_LESSON_MODEL",model))
            allowed={(x["section"],x["index"]) for x in targets}
            repaired=0
            for fix in data.get("repairs",[]):
                section,index=fix.get("section"),fix.get("index")
                if (section,index) not in allowed:
                    continue
                evidence_id=str(fix.get("evidence_id",""))
                if evidence_id in catalog:
                    lesson[section][index]["evidence_id"]=evidence_id
                    repaired+=1
            attach_evidence(lesson,catalog)
            progress("SOURCE_QUOTES_REPAIRED",provider=provider,count=repaired,
                     requested=len(targets))
            return repaired>0
        except Exception as exc:
            progress("SOURCE_QUOTE_REPAIR_PROVIDER_FAILED",provider=provider,
                     error_type=type(exc).__name__)
    return False


def independent_reviewer(generator_provider, generator_model,
                         visual_provider, visual_model):
    """Fail closed unless a third, separately configured reviewer is available."""
    if not visual_provider or not visual_model or visual_provider == generator_provider:
        raise RuntimeError("INDEPENDENT_REVIEWER_UNAVAILABLE")
    candidates = [p for p in configured_providers()
                  if p[0] not in (generator_provider, visual_provider)]
    selected = os.getenv("NABIL_REVIEWER_PROVIDER", "").strip().lower()
    if selected:
        candidates = [p for p in candidates if p[0] == selected]
    if not candidates:
        raise RuntimeError("INDEPENDENT_REVIEWER_UNAVAILABLE")
    name, key, base, default_model = candidates[0]
    model = os.getenv("NABIL_LESSON_REVIEW_MODEL", "").strip()
    if not model:
        raise RuntimeError("VISION_REVIEW_MODEL_NOT_CONFIGURED")
    if model in (generator_model, visual_model):
        raise RuntimeError("INDEPENDENT_REVIEWER_UNAVAILABLE")
    return name, key, base, model


def review_claim(client, provider, model, item, image, page_text, page):
    """One claim and its cited original page; candidate descriptions are untrusted."""
    content = [{"type": "text", "text": json.dumps(
        {"pdf_page": page, "ocr": page_text, "claim": item}, ensure_ascii=False)},
        {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," +
         base64.b64encode(image).decode("ascii")}}]
    messages = [
        {"role": "system", "content": (
            "You are an independent, skeptical scientific reviewer. Inspect the actual "
            "textbook page image and OCR. Verify this ONE proposed claim and its cited "
            "figure against what is visibly present on this page. Descriptions produced "
            "by another model are unverified candidates. A question is not evidence for "
            "its answer. Reject ambiguous drawings, unsupported answers, invented "
            "measurements and theoretical leaps. Return JSON with approved (boolean) "
            "and specific_reason (nonempty string).")},
        {"role": "user", "content": content},
    ]
    response = client.chat.completions.create(model=model, temperature=0,
        response_format={"type": "json_object"}, messages=messages)
    verdict = parse_provider_json(client, provider, messages, response, model)
    if type(verdict.get("approved")) is not bool or not verdict.get("specific_reason"):
        raise ValueError("INVALID_VISUAL_REVIEW_VERDICT")
    return verdict


def scientific_review(lesson, pages, images, generator_provider, generator_model,
                      visual_provider, visual_model):
    """Review every cited claim directly against its original page image."""
    from openai import OpenAI
    name = None
    model = None
    try:
        name, key, base, model = independent_reviewer(
            generator_provider, generator_model, visual_provider, visual_model)
        client = OpenAI(api_key=key, base_url=base, timeout=90, max_retries=0)
        page_texts = dict(pages)
        targets = [("introduction", lesson.get("introduction_source_page"),
                    {"text": lesson.get("introduction"),
                     "citation": lesson.get("introduction_source_quote")})]
        for section in ("concepts", "activities", "questions", "exercises", "summary"):
            for index, item in enumerate(lesson.get(section, []), 1):
                targets.append((f"{section}_{index}", item.get("pdf_page"), item))
        for label, page, item in targets:
            if type(page) is not int or page not in images or page not in page_texts:
                return {"pass": False, "reviewer": name, "model": model,
                        "errors": [f"{label}:SOURCE_IMAGE_OR_PAGE_MISSING"]}
            verdict = review_claim(client, name, model, item, images[page],
                                   page_texts[page], page)
            if verdict["approved"] is not True:
                return {"pass": False, "reviewer": name, "model": model,
                        "errors": [f"{label}:{verdict['specific_reason']}"]}
        return {"pass": True, "reviewer": name, "model": model, "errors": []}
    except Exception as exc:
        return {"pass": False, "reviewer": name, "model": model,
                "errors": ["REVIEW_UNAVAILABLE", type(exc).__name__ + ": " + str(exc)[:160]]}


def source_images(pdf, pages):
    """Embed original figures and exercise layouts, not a guessed redraw."""
    result={}
    with tempfile.TemporaryDirectory(prefix="nabil_figures_") as directory:
        for number,_ in pages:
            prefix=str(Path(directory)/f"p{number}")
            subprocess.run(["pdftoppm","-f",str(number),"-l",str(number),
                            "-singlefile","-scale-to","1100","-jpeg",
                            "-jpegopt","quality=72",str(pdf),prefix],
                           check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,timeout=45)
            image=Path(prefix+".jpg").read_bytes()
            if len(image)<5000:
                raise ValueError("SOURCE_PAGE_RENDER_FAILED")
            result[number]=image
    return result


def concept_diagram(source_text):
    """Source-triggered SVG adapters; otherwise the original PDF page is shown."""
    text=source_text.casefold()
    if "communicating vessel" in text and "horizont" in text:
        return '''<svg viewBox="0 0 480 210" role="img" aria-label="Communicating vessels with equal water levels">
<path d="M65 22 V180 H415 V22 M180 22 V180 M300 22 V180" fill="none" stroke="#8ce9ff" stroke-width="7"/>
<path d="M69 100 V176 H411 V100 M184 100 V176 M304 100 V176" fill="none" stroke="#38aada" stroke-width="14"/>
<path d="M54 100 H428" fill="none" stroke="#31d9a8" stroke-width="3" stroke-dasharray="9 6"/>
<text x="125" y="85" fill="#e9f8ff" font-size="16">same horizontal level</text></svg>'''
    if "free surface" in text and "horizont" in text:
        return '''<svg viewBox="0 0 480 210" role="img" aria-label="Horizontal free surface of the liquid">
<path d="M50 26 L65 180 H410 L425 26" fill="none" stroke="#8ce9ff" stroke-width="7"/>
<path d="M59 106 H416 L409 176 H66 Z" fill="#38aada" opacity=".65"/>
<line x1="58" x2="417" y1="106" y2="106" stroke="#31d9a8" stroke-width="4"/>
<text x="68" y="94" fill="#e9f8ff" font-size="16">horizontal</text></svg>'''
    if "shape" in text and "liquid" in text and "vessel" in text:
        return '''<svg viewBox="0 0 480 210" role="img" aria-label="Liquid adapting to two different vessel shapes">
<path d="M35 30 L55 180 H205 L225 30 M290 55 L300 180 H430 L440 55" fill="none" stroke="#8ce9ff" stroke-width="7"/>
<path d="M46 105 H214 L202 176 H58Z M294 116 H436 L427 176 H303Z" fill="#38aada" opacity=".7"/>
<path d="M230 95 L275 95 M260 82 L275 95 L260 108" fill="none" stroke="#31d9a8" stroke-width="5"/></svg>'''
    return ""


def render_html(lesson, pages, book, images, evidence_map):
    e = lambda value: html.escape(str(value), quote=True)
    catalog=evidence_map["evidence"]
    golden_css=(ROOT/"app/static/nabil_lesson_golden.css").read_text(encoding="utf-8")
    def source_tag(item):
        return (f'<small data-evidence-id="{e(item["evidence_id"])}" '
                f'data-source-page="{int(item["pdf_page"])}">PDF p. {int(item["pdf_page"])}'
                f' · <q>{e(item["source_quote"])}</q></small>')
    def visual(x):
        entry=catalog[x["visual_evidence_id"]]
        svg=concept_diagram(entry["text"])
        return (f'<figure class="fig" data-evidence-id="{e(x["visual_evidence_id"])}" '
                f'data-source-page="{entry["page"]}">'
                f'{svg}<img loading="lazy" src="data:image/jpeg;base64,'
                f'{base64.b64encode(images[entry["page"]]).decode()}" '
                f'alt="Original textbook page {entry["page"]}">'
                f'<figcaption>{("Source-backed explanatory reconstruction · " if svg else "")}'
                f'Original PDF p. {entry["page"]} · evidence {e(x["visual_evidence_id"])}</figcaption>'
                '</figure>')
    cards = "".join(
        f'<section class="card concept"><h2>{i} · {e(x["heading"])}</h2>'
        f'<p>{e(x["explanation"])}</p>'
        f'{visual(x)}'
        f'{("<p class=example>"+e(x["example"])+"</p>") if x.get("example") else ""}'
        f'{source_tag(x)}</section>'
        for i,x in enumerate(lesson["concepts"],1))
    activities = "".join(
        f'<details class="card"><summary>{e(x["prompt"])}</summary><p>{e(x["answer"])}</p>'
        f'{source_tag(x)}</details>' for x in lesson["activities"])
    questions = "".join(
        f'<fieldset class="card" data-answer="{x["correct_index"]}"><legend>{e(x["prompt"])}</legend>'
        + "".join(f'<label><input type="radio" name="q{i}" value="{j}">{e(option)}</label>'
                  for j, option in enumerate(x["options"]))
        + f'<button type="button" class="check">Check</button><output aria-live="polite"></output>'
          f'<span class="explanation" hidden>{e(x["explanation"])}</span>{source_tag(x)}</fieldset>'
        for i, x in enumerate(lesson["questions"]))
    exercises = "".join(
        f'<details class="card"><summary>Exercise {i+1}: {e(x["prompt"])}</summary>'
        f'<ol>{"".join("<li>"+e(step)+"</li>" for step in x["solution_steps"])}</ol>'
        f'<p><strong>{e(x["solution"])}</strong></p>{source_tag(x)}</details>'
        for i,x in enumerate(lesson["exercises"]))
    summary = "".join(f"<li>{e(s['text'])}<br>{source_tag(s)}</li>"
                      for s in lesson["summary"])
    original = "".join(
        f'<figure class="card"><img loading="lazy" alt="Original source PDF page {number}" '
        f'src="data:image/jpeg;base64,{base64.b64encode(images[number]).decode()}">'
        f'<figcaption>{e(book["title"])} · PDF page {number}</figcaption></figure>'
        for number,_ in pages)
    source_text=" ".join(text for _,text in pages).lower()
    lab = ""
    if "free surface" in source_text and "horizontal" in source_text:
        lab_ids=[key for key,item in catalog.items()
                 if "free surface" in item["text"].lower()
                 and "horizontal" in item["text"].lower()]
        if lab_ids:
            lab_id=lab_ids[0]; lab_page=catalog[lab_id]["page"]
            lab = f'<section class="card" id="source-lab" data-evidence-id="{e(lab_id)}" data-source-page="{lab_page}">' + '''<h2>Explore the free surface</h2>
<p>Change the vessel and liquid level. Observe that the free surface stays horizontal.</p>
<label>Vessel <select id="vessel"><option value="wide">Wide</option>
<option value="narrow">Narrow</option></select></label>
<label>Liquid level <input id="liquid-level" type="range" min="25" max="135" value="85"></label>
<svg viewBox="0 0 360 210" role="img" aria-label="Water surface remains horizontal as the vessel changes">
<path id="vessel-outline" d="M70 25 L70 180 L290 180 L290 25" fill="none"
stroke="#173b69" stroke-width="7"/>
<path id="water-area" d="M73 85 L287 85 L287 177 L73 177 Z" fill="#54bce7" opacity=".7"/>
<line id="waterline" x1="73" y1="85" x2="287" y2="85" stroke="#086a9d" stroke-width="4"/>
</svg><p>The free surface is horizontal at every level: y(left) = y(right).</p></section>
<script>const vessel=document.getElementById("vessel"),level=document.getElementById("liquid-level");
function updateLab(){const narrow=vessel.value==="narrow",left=narrow?130:73,right=narrow?230:287,
y=Number(level.value);document.getElementById("vessel-outline").setAttribute("d",
"M"+(left-3)+" 25 L"+(left-3)+" 180 L"+(right+3)+" 180 L"+(right+3)+" 25");
document.getElementById("water-area").setAttribute("d",
"M"+left+" "+y+" L"+right+" "+y+" L"+right+" 177 L"+left+" 177 Z");
const line=document.getElementById("waterline");line.setAttribute("x1",left);
line.setAttribute("x2",right);line.setAttribute("y1",y);line.setAttribute("y2",y)}
vessel.addEventListener("change",updateLab);level.addEventListener("input",updateLab);</script>'''
    refs = ", ".join(str(p) for p, _ in pages)
    return f'''<!doctype html><html lang="{e(book.get("language", "en"))[:2].lower()}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(lesson["title"])} · NABIL AI</title>
<style>{golden_css}
img{{width:100%;height:auto;display:block}}.concept img{{max-height:460px;object-fit:contain}}
figure{{margin:14px 0}}.concept{{border-inline-start:6px solid #168a83}}
#summary-card{{border:3px solid #31d9a8}}
#summary-card ul{{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:10px;padding:0;list-style:none}}
#summary-card li{{padding:12px;border-radius:10px;background:#09243b}}
.concept small,.card small{{display:block;margin-top:9px;color:#b6d8e7}}.concept q{{display:block;font-size:.86rem}}
label{{display:block;padding:9px;margin:8px 0}}fieldset{{border:1px solid #315f7e;border-radius:12px}}
output{{display:block;font-weight:700}}details summary{{cursor:pointer;font-weight:700}}
.source-pages img{{max-height:700px;object-fit:contain}}
@media(max-width:500px){{main{{padding:9px}}.card,header{{padding:14px}}}}</style></head>
<body><header><strong>🧠 NABIL AI · {e(book["grade"])} · {e(book["subject"])}</strong></header>
<nav class="langbar"><span data-en="Lesson from the official textbook" data-fr="Leçon du manuel officiel">Lesson from the official textbook</span>
<button type="button" onclick="window.print()">Print / طباعة</button></nav><main><section class="card">
<h1>{e(lesson["title"])}</h1><p>{e(lesson["introduction"])}</p>
<small data-evidence-id="{e(lesson["introduction_evidence_id"])}" data-source-page="{int(lesson["introduction_source_page"])}">{e(book["title"])} · PDF pages {refs}</small></section>
<h2>Ideas · الأفكار</h2>{cards}<h2>Activities · الأنشطة</h2>{activities}{lab}
<h2>Exercises and worked solutions</h2>{exercises}
<h2>Interactive worksheet · ورقة عمل</h2>{questions}<section class="card" id="summary-card"><h2>Summary Card · بطاقة الخلاصة</h2><ul>{summary}</ul></section>
<section class="source-pages"><h2>Original textbook figures and exercises</h2>{original}</section>
<section class="card"><h2>Source</h2><p>{e(book["title"])} · Drive PDF ID {e(book["drive_file_id"])} · PDF pages {refs}</p></section>
</main><script>document.querySelectorAll("fieldset").forEach(f=>f.querySelector("button").onclick=()=>{{
const choice=f.querySelector("input:checked"),out=f.querySelector("output");
out.textContent=choice?(Number(choice.value)===Number(f.dataset.answer)?"✓ Correct · ":"Try again · ")+f.querySelector(".explanation").textContent:"Choose an answer first";
}});</script></body></html>'''


def check_html(document, lesson, pages, evidence_map):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(document, "html.parser")
    errors = []
    if not soup.select_one("meta[name=viewport]") or not soup.select_one("main"):
        errors.append("MOBILE_OR_SEMANTIC_STRUCTURE_MISSING")
    if len(soup.select("fieldset[data-answer]")) != len(lesson["questions"]):
        errors.append("QUIZ_RENDER_MISMATCH")
    if len(soup.select("details")) != len(lesson["activities"])+len(lesson["exercises"]):
        errors.append("EXERCISES_OR_SOLUTIONS_MISSING")
    if len(soup.select("figure.card img[src^='data:image/jpeg;base64,']")) != len(pages):
        errors.append("ORIGINAL_SOURCE_FIGURES_MISSING")
    if len(soup.select(".concept figure img")) != len(lesson["concepts"]):
        errors.append("CONCEPT_VISUALS_MISSING")
    catalog=evidence_map["evidence"]
    tagged=soup.select("[data-evidence-id][data-source-page]")
    for tag in tagged:
        entry=catalog.get(tag.get("data-evidence-id"))
        if not entry or str(entry["page"])!=tag.get("data-source-page"):
            errors.append("HTML_EVIDENCE_MAPPING_INVALID")
            break
    expected=1+len(lesson["concepts"])+sum(
        len(lesson[key]) for key in ("concepts","activities","questions","exercises","summary"))
    if len(tagged)<expected:
        errors.append("HTML_EVIDENCE_MAPPING_INCOMPLETE")
    for tag in tagged:
        quote=tag.select_one("q")
        if quote and (re.sub(r"\s+"," ",quote.get_text(" ",strip=True))!=
                      re.sub(r"\s+"," ",catalog[tag["data-evidence-id"]]["text"].strip())):
            errors.append("HTML_EVIDENCE_QUOTE_MISMATCH")
            break
    if not soup.select_one(".langbar") or ".grid" not in document:
        errors.append("GOLDEN_LAYOUT_CONTRACT_MISSING")
    if not soup.select_one("#summary-card"):
        errors.append("SUMMARY_CARD_MISSING")
    if soup.select_one("#source-lab") and (
        not soup.select_one("#waterline") or "updateLab()" not in document or
        not soup.select_one("#liquid-level")):
        errors.append("SOURCE_LAB_INCOMPLETE")
    if "querySelectorAll" not in document or len(document.encode()) < 3500:
        errors.append("INTERACTIVITY_OR_CONTENT_MISSING")
    if re.search(r"(?<!\\)\\\(|(?<!\\)\\\[|\$\$|\\frac\b|\\sqrt\b",soup.get_text(" ")):
        errors.append("UNRENDERED_MATH_MARKUP")
    if soup.select_one('meta[name=viewport]') and "width=device-width" not in str(soup.select_one('meta[name=viewport]')):
        errors.append("MOBILE_VIEWPORT_INVALID")
    return errors


def make_pptx(lesson, book, pages, images):
    """A separate visual export; all shapes and text are generated from checked JSON."""
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.33), Inches(7.5)
    def slide(title, body, n, page=None):
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
        width=7.1 if page in images else 10.9
        if len(body)>850:
            raise ValueError("PPTX_SLIDE_TEXT_TOO_LONG")
        size=16 if len(body)>580 else (19 if len(body)>350 else 22)
        textbox(body, 1.25, 2.2, width, 3.85, size, RGBColor(239,248,255))
        if page in images:
            from PIL import Image
            picture=Image.open(io.BytesIO(images[page]))
            if picture.height < 200:
                raise ValueError("SOURCE_VISUAL_TOO_SMALL")
            s.shapes.add_picture(io.BytesIO(images[page]), Inches(8.8), Inches(1.85),
                                 height=Inches(4.5))
        textbox(f'NABIL AI  •  {book["title"]}  •  PDF pp. {pages[0][0]}–{pages[-1][0]}  •  {n}',
                1, 6.7, 11.3, .4, 12, RGBColor(111, 222, 214))
    slide(lesson["title"], lesson["introduction"], 1)
    for i, item in enumerate(lesson["concepts"], 2):
        slide(item["heading"], item["explanation"] + f'\n\nSource: PDF p. {item["pdf_page"]}',
              i, int(item["pdf_page"]))
    offset = len(prs.slides)
    for i, item in enumerate(lesson["activities"], offset+1):
        slide("Explore · " + item["prompt"], item["answer"], i,int(item["pdf_page"]))
    for item in lesson["exercises"]:
        steps="\n".join(f"{i}. {step}" for i,step in enumerate(item["solution_steps"],1))
        slide("Worked exercise · " + item["prompt"], steps+"\n\n"+item["solution"],
              len(prs.slides)+1,int(item["pdf_page"]))
    slide("Summary Card · key ideas", "\n• ".join(item["text"] for item in lesson["summary"]),
          len(prs.slides)+1,pages[0][0])
    stream = io.BytesIO(); prs.save(stream)
    return stream.getvalue()


def check_pptx(raw, lesson):
    from pptx import Presentation
    slides = list(Presentation(io.BytesIO(raw)).slides)
    if len(slides) != 2 + len(lesson["concepts"]) + len(lesson["activities"])+len(lesson["exercises"]):
        return ["PPTX_SLIDE_COUNT_MISMATCH"]
    text = "\n".join(shape.text for slide in slides for shape in slide.shapes if shape.has_text_frame)
    missing = [x["heading"] for x in lesson["concepts"] if x["heading"] not in text]
    for exercise in lesson["exercises"]:
        if any(step not in text for step in exercise["solution_steps"]):
            return ["PPTX_SOLUTION_STEPS_MISSING"]
    if not any(shape.shape_type==13 for slide in slides for shape in slide.shapes):
        return ["PPTX_SOURCE_IMAGES_MISSING"]
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


def find_named(service,parent,name):
    safe=name.replace("'","\\'")
    files=service.files().list(q=f"'{parent}' in parents and name='{safe}' and trashed=false",
        fields="files(id,name,mimeType)",pageSize=20).execute().get("files",[])
    if len(files)>1:
        raise ValueError("AMBIGUOUS_EXISTING_DRIVE_FILE: "+name)
    return files[0] if files else None


def upload_verified(service, parent, name, raw, mime):
    from googleapiclient.http import MediaIoBaseUpload
    minimum = 40_000 if mime == "text/html" else 30_000
    if len(raw) < minimum:
        raise ValueError("ARTIFACT_TOO_SMALL_BEFORE_UPLOAD: "+name)
    existing=find_named(service,parent,name)
    if existing:
        verify_uploaded(service,existing["id"],parent,raw,mime)
        return existing
    item = service.files().create(body={"name":name, "parents":[parent]},
        media_body=MediaIoBaseUpload(io.BytesIO(raw), mimetype=mime, resumable=False),
        fields="id,name,size,webViewLink").execute()
    verify_uploaded(service,item["id"],parent,raw,mime)
    return item


def verify_uploaded(service, file_id, parent, raw, mime):
    metadata=service.files().get(fileId=file_id,
        fields="id,name,mimeType,size,parents,trashed").execute()
    if (metadata.get("trashed") or parent not in metadata.get("parents",[])
        or metadata.get("mimeType")!=mime
        or int(metadata.get("size",0))!=len(raw)):
        raise ValueError("DRIVE_FILE_LOCATION_TYPE_OR_SIZE_MISMATCH")
    if hashlib.sha256(download(service,file_id)).digest()!=hashlib.sha256(raw).digest():
        raise ValueError("DRIVE_READBACK_HASH_MISMATCH")


def verify_folder_chain(service, folder, subject_folder, grade_folder):
    for child,parent in ((folder,grade_folder),(grade_folder,subject_folder),
                         (subject_folder,ROOT_FOLDER)):
        meta=service.files().get(fileId=child,
            fields="id,mimeType,parents,trashed").execute()
        if (meta.get("trashed") or meta.get("mimeType")!=FOLDER_MIME
            or parent not in meta.get("parents",[])):
            raise ValueError("DRIVE_FOLDER_CHAIN_MISMATCH")


def read_ledger(service, default):
    item=find_named(service,ROOT_FOLDER,LEDGER.name)
    if not item:
        return default,item
    remote=json.loads(download(service,item["id"]).decode("utf-8-sig"))
    if not isinstance(remote.get("books"),list):
        raise ValueError("REMOTE_LEDGER_INVALID")
    # Existing ledger on Drive is authoritative across Railway redeployments.
    return remote,item


def save_ledger(service,ledger,item):
    from googleapiclient.http import MediaIoBaseUpload
    raw=(json.dumps(ledger,ensure_ascii=False,indent=2)+"\n").encode()
    media=MediaIoBaseUpload(io.BytesIO(raw),mimetype="application/json",resumable=False)
    if item:
        saved=service.files().update(fileId=item["id"],media_body=media,
                                     fields="id,name").execute()
    else:
        saved=service.files().create(body={"name":LEDGER.name,"parents":[ROOT_FOLDER]},
                                     media_body=media,fields="id,name").execute()
    if download(service,saved["id"])!=raw:
        raise ValueError("REMOTE_LEDGER_READBACK_FAILED")
    return saved


def run(report_path, pilot_book_id=None, pilot_lesson=None, pilot_pages=None,
        publish=False):
    global RUN_DEADLINE,BOOK_DEADLINE,PROGRESS_STARTED
    PROGRESS_STARTED=time.monotonic()
    RUN_DEADLINE=time.monotonic()+420
    max_books=max(1,min(5,int(os.getenv("NABIL_PILOT_MAX_BOOKS","3"))))
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    report = {"started":now(), "status":"RUNNING", "attempts":[], "production":None}
    if pilot_book_id or pilot_lesson:
        report["pilot_filter"]={"book_id":pilot_book_id,"lesson":pilot_lesson}
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
            ledger,ledger_item=read_ledger(service,ledger)
        else:
            ledger_item=None
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
                book.get("language","")!="English",book.get("order",999))
    for book in sorted(ledger["books"], key=book_order):
        if pilot_book_id and book.get("drive_file_id")!=pilot_book_id:
            continue
        if time.monotonic()>=RUN_DEADLINE:
            report["status"]="RUN_DEADLINE_EXCEEDED"; checkpoint()
            break
        if len(report["attempts"])>=max_books:
            report["status"]="PILOT_BOOK_LIMIT_REACHED"
            report["max_books"]=max_books
            checkpoint()
            progress("PILOT_BOOK_LIMIT_REACHED",attempts=len(report["attempts"]))
            break
        if not book.get("drive_file_id"):
            continue
        if book["drive_file_id"] in seen_ids:
            continue
        seen_ids.add(book["drive_file_id"])
        attempt = {"book":book["title"],"book_id":book["drive_file_id"],"started":now()}
        BOOK_DEADLINE=min(RUN_DEADLINE,time.monotonic()+120)
        report["attempts"].append(attempt); checkpoint()
        progress("BOOK_STARTED",book=book["title"])
        try:
            from pypdf import PdfReader
            temp = tempfile.TemporaryDirectory(prefix="nabil_book_")
            pdf = Path(temp.name) / "book.pdf"
            download_pdf_to_path(service, book["drive_file_id"], pdf)
            reader = PdfReader(str(pdf))
            progress("SOURCE_DISCOVERY_STARTED",book=book["title"])
            entries = candidates(reader,pdf)
            finished_records = [x for x in book.get("authored_lessons",[])
                                if x.get("status") in ("verified_complete","REQUIRES_TEACHER_REVIEW")
                                and x.get("drive_html_id") and x.get("drive_pptx_id")]
            finished = {x.get("lesson_key") for x in finished_records}
            finished_starts = {x["source_pdf_pages"][0]-1 for x in finished_records
                               if x.get("source_pdf_pages")}
            available = [(title, start, end) for title, start, end in entries
                         if lesson_key(book,title,start) not in finished and start not in finished_starts]
            if pilot_lesson:
                available=[entry for entry in available if entry[0].strip().casefold()==pilot_lesson.strip().casefold()]
            if not available:
                raise ValueError("NO_UNFINISHED_TOC_LESSON")
            title, start, end = available[0]
            if pilot_pages and (start+1,end)!=pilot_pages:
                raise ValueError(f"PILOT_SOURCE_PAGES_MISMATCH: discovered {start+1}-{end}; expected {pilot_pages[0]}-{pilot_pages[1]}")
            attempt.update({"lesson":title,"source_pdf_pages":list(range(start+1,end+1)),
                            "lesson_key":lesson_key(book,title,start)})
            progress("SOURCE_LESSON_SELECTED",lesson=title,pages=attempt["source_pdf_pages"])
            pages = source_excerpt(reader,pdf,start,end)
            images=source_images(pdf,pages)
            proposed_visuals, visual_provider, visual_model = visual_candidates(images)
            catalog=evidence_catalog(pages,proposed_visuals)
            if len(catalog)<10:
                raise ValueError("SOURCE_EVIDENCE_CATALOG_TOO_SPARSE")
            digest = hashlib.sha256()
            with pdf.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024*1024), b""):
                    digest.update(chunk)
            attempt["source_sha256"]=digest.hexdigest()
            checkpoint()
            evidence_map=source_evidence_map(title,pages,catalog,
                                             visual_provider,visual_model)
            record_role_provenance(evidence_map,attempt,"visual_extractor",
                                   visual_provider,visual_model)
            record_role_provenance(evidence_map,attempt,"generator",None,None)
            record_role_provenance(evidence_map,attempt,"reviewer",None,None)
            evidence_path=report_path.with_name(report_path.stem+"-evidence-map.json")
            evidence_path.write_text(json.dumps(evidence_map,ensure_ascii=False,indent=2),encoding="utf-8")
            attempt["evidence_map_path"]=str(evidence_path)
            attempt["source_evidence_counts"]={key:len(value) for key,value in
                                                evidence_map["categories"].items()}
            attempt["generation_checks"]=[]
            previous_failures=[]
            for generation_attempt in (1,2):
                progress("GENERATION_STARTED",lesson=title,attempt=generation_attempt)
                lesson, generator_provider, generator_model = generate(
                    title,pages,book.get("language",""),evidence_map,
                    previous_failures,visual_provider=visual_provider,
                    visual_model=visual_model)
                attempt["generator"]={"provider":generator_provider,
                                       "model":generator_model}
                record_role_provenance(evidence_map,attempt,"generator",
                                       generator_provider,generator_model)
                evidence_path.write_text(json.dumps(evidence_map,ensure_ascii=False,indent=2),
                                         encoding="utf-8")
                draft_path=report_path.with_name(report_path.stem+f"-draft-{generation_attempt}.json")
                draft_path.write_text(json.dumps(lesson,ensure_ascii=False,indent=2),encoding="utf-8")
                attempt.setdefault("draft_paths",[]).append(str(draft_path))
                progress("QUALITY_GATE_STARTED",lesson=title,attempt=generation_attempt)
                failures = check_content(lesson,title,pages,catalog)
                if any(x.startswith("UNVERIFIED_") for x in failures):
                    progress("SOURCE_QUOTE_REPAIR_STARTED",count=sum(
                        x.startswith("UNVERIFIED_") for x in failures))
                    if repair_source_quotes(lesson,pages,catalog,failures,
                                            generator_provider):
                        failures=check_content(lesson,title,pages,catalog)
                review=None
                if not failures:
                    review=scientific_review(lesson,pages,images,
                                             generator_provider,generator_model,
                                             visual_provider,visual_model)
                    attempt["scientific_review"]=review
                    record_role_provenance(evidence_map,attempt,"reviewer",
                                           review.get("reviewer"),review.get("model"))
                    evidence_path.write_text(json.dumps(evidence_map,ensure_ascii=False,indent=2),
                                             encoding="utf-8")
                    if not review["pass"]:
                        failures.append("SCIENTIFIC_REVIEW_REJECTED")
                previous_failures=(review["errors"] if review and not review["pass"]
                                   else failures[:])
                attempt["generation_checks"].append(
                    {"attempt":generation_attempt,"failures":failures,"scientific_review":review})
                checkpoint()
                if not failures:
                    break
            document = render_html(lesson,pages,book,images,evidence_map) if not failures else ""
            failures.extend(check_html(document,lesson,pages,evidence_map) if document else [])
            attempt["html_quality"]={"pass":not failures,"failures":failures}
            checkpoint()
            if failures:
                raise ValueError("HTML_QUALITY_FAILED: " + ",".join(failures))
            powerpoint = make_pptx(lesson,book,pages,images)
            failures = check_pptx(powerpoint,lesson)
            attempt["pptx_quality"]={"pass":not failures,"failures":failures,"slides":2+len(lesson["concepts"])+len(lesson["activities"])+len(lesson["exercises"])}
            checkpoint()
            if failures:
                raise ValueError("PPTX_QUALITY_FAILED: " + ",".join(failures))
            html_path=report_path.with_name(report_path.stem+"-lesson.html")
            pptx_path=report_path.with_name(report_path.stem+"-lesson.pptx")
            html_path.write_text(document,encoding="utf-8")
            pptx_path.write_bytes(powerpoint)
            attempt["local_artifacts"]={"html":str(html_path),"pptx":str(pptx_path)}
            checkpoint()
            if not publish:
                report["status"]="LOCAL_VERIFIED_DRY_RUN_SUCCESS"
                attempt["status"]="LOCAL_VERIFIED_DRY_RUN_SUCCESS"
                checkpoint()
                break
            progress("UPLOAD_STARTED",lesson=title)
            subject_folder = ensure_folder(service,ROOT_FOLDER,book["subject"])
            grade_folder = ensure_folder(service,subject_folder,book["grade"])
            folder = ensure_folder(service,grade_folder,title)
            verify_folder_chain(service,folder,subject_folder,grade_folder)
            base = (re.sub(r"[^a-zA-Z0-9_-]+","-",title).strip("-")[:45]
                    or "lesson")+"-"+attempt["lesson_key"]
            html_item = upload_verified(service,folder,base+".html",document.encode("utf-8"),"text/html")
            attempt["drive_html_id"]=html_item["id"]; checkpoint()
            ppt_item = upload_verified(service,folder,base+".pptx",powerpoint,
                                       "application/vnd.openxmlformats-officedocument.presentationml.presentation")
            attempt["drive_pptx_id"]=ppt_item["id"]
            attempt["status"]="VERIFIED_UPLOAD"
            record = {"title":title,"lesson_key":attempt["lesson_key"],
                      "book_drive_file_id":book["drive_file_id"],
                      "source_pdf_pages":attempt["source_pdf_pages"],"source_sha256":attempt["source_sha256"],
                      "source_pages_sha256":hashlib.sha256(json.dumps(pages,ensure_ascii=False).encode()).hexdigest(),
                      "source_evidence_sha256":hashlib.sha256(
                          json.dumps(evidence_map,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),
                      "source_evidence_counts":attempt["source_evidence_counts"],
                      "html_sha256":hashlib.sha256(document.encode("utf-8")).hexdigest(),
                      "pptx_sha256":hashlib.sha256(powerpoint).hexdigest(),
                      "drive_folder_id":folder,"drive_html_id":html_item["id"],"drive_pptx_id":ppt_item["id"],
                      "html_bytes":len(document.encode("utf-8")),"pptx_bytes":len(powerpoint),
                      "status":"REQUIRES_TEACHER_REVIEW","completed_at":now()}
            book.setdefault("authored_lessons",[]).append(record)
            ledger["updated"]=now()
            ledger_item=save_ledger(service,ledger,ledger_item)
            LEDGER.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
            report["production"]=record
            report["status"]="ONE_PILOT_REVIEW_PENDING"
            checkpoint()
            progress("ONE_PILOT_REVIEW_PENDING",lesson=title)
            break
        except Exception as exc:
            attempt.update({"status":"FAILED","reason":f"{type(exc).__name__}: {exc}","finished":now()})
            checkpoint()
            progress("BOOK_FAILED",book=book["title"],reason=attempt["reason"])
            if attempt.get("lesson"):
                report["status"]="PILOT_LESSON_FAILED"
                checkpoint()
                break
        finally:
            BOOK_DEADLINE=None
            if "temp" in locals():
                temp.cleanup()
                del temp
    else:
        report["status"]="NO_LESSON_COMPLETE"; checkpoint()
    return report


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--report",default="data/nabil_lesson_factory_run.json")
    parser.add_argument("--pilot-book-id",help="Only consider this registered Drive PDF ID")
    parser.add_argument("--pilot-lesson",help="Only consider this exact TOC lesson heading")
    parser.add_argument("--pilot-pages",help="Require exact inclusive PDF page range, e.g. 13-18")
    parser.add_argument("--publish", action="store_true",
                        help="Explicitly allow Drive writes and production ledger updates")
    args=parser.parse_args()
    pilot_pages=None
    if args.pilot_pages:
        match=re.fullmatch(r"(\d+)-(\d+)",args.pilot_pages)
        if not match or int(match[1])>int(match[2]):
            parser.error("--pilot-pages must be START-END")
        pilot_pages=(int(match[1]),int(match[2]))
    def deadline_handler(_signum,_frame):
        raise TimeoutError("FACTORY_RUN_EXCEEDED_420_SECONDS")
    old_handler=signal.signal(signal.SIGALRM,deadline_handler)
    signal.setitimer(signal.ITIMER_REAL,420)
    try:
        report=run(Path(args.report),args.pilot_book_id,args.pilot_lesson,pilot_pages,
                   publish=args.publish)
    except TimeoutError as exc:
        report={"status":"RUN_DEADLINE_EXCEEDED","error":str(exc)}
        if Path(args.report).exists():
            previous=json.loads(Path(args.report).read_text(encoding="utf-8"))
            previous.update(report)
            report=previous
            Path(args.report).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    finally:
        signal.setitimer(signal.ITIMER_REAL,0)
        signal.signal(signal.SIGALRM,old_handler)
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if report["status"] in ("ONE_PILOT_REVIEW_PENDING",
                                      "LOCAL_VERIFIED_DRY_RUN_SUCCESS") else 2


if __name__=="__main__":
    sys.exit(main())
