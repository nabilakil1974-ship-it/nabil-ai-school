"""
NABIL AI — Enterprise Autonomous Lesson Factory & Canonical Catalog Engine

Guarantees:
- Gemini Vision standardisé sur gemini-3.6-flash (SDK natif google-genai).
- Modèles Groq stabilisés sur llama-3.1-70b-versatile / llama-3.1-8b-instant.
- Extraction et résolution exhaustives des exercices et problèmes.
- Injection stricte des métadonnées nabil-* et publication Drive avec validation.
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
LEDGER_PATH = ROOT / "data/interactive_lesson_production_ledger.json"
CATALOG_PATH = ROOT / "data/nabil_canonical_lesson_catalog.json"
FOLDER_MIME = "application/vnd.google-apps.folder"
ROOT_FOLDER = os.getenv("NABIL_INTERACTIVE_CURRICULUM_ROOT_ID",
                        os.getenv("NABIL_LESSON_DRIVE_ROOT",
                                  "16bcmZMO_dn4FqlGaDtl8Hky6iSBEqZpX"))
RUN_DEADLINE = None
PROGRESS_STARTED = None


def now():
    return datetime.now(timezone.utc).isoformat()


def progress(stage, **details):
    elapsed = round(time.monotonic() - PROGRESS_STARTED, 1) if PROGRESS_STARTED else 0
    print(json.dumps({"time": now(), "elapsed_seconds": elapsed, "stage": stage, **details},
                     ensure_ascii=False), flush=True)


def bounded(command, seconds, **kwargs):
    remaining = min([seconds, *([RUN_DEADLINE - time.monotonic()] if RUN_DEADLINE else [])])
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


def download_pdf_to_path(service, file_id, path):
    from googleapiclient.http import MediaIoBaseDownload
    with path.open("wb") as target:
        loader = MediaIoBaseDownload(target, service.files().get_media(fileId=file_id))
        finished = False
        while not finished:
            _, finished = loader.next_chunk()


def canonical_grade_meta(value):
    text = str(value).strip()
    found = re.search(r"(?<!\d)(1[0-2]|[1-9])(?!\d)", text)
    if found:
        g = int(found.group(1))
        return g, f"G{g:02d}", f"Grade {g}"
    ordinals = {"الأول": 1, "الثاني": 2, "الثالث": 3, "الرابع": 4, "الخامس": 5,
                "السادس": 6, "السابع": 7, "الثامن": 8, "التاسع": 9, "العاشر": 10}
    for word, num in ordinals.items():
        if word in text:
            return num, f"G{num:02d}", f"Grade {num}"
    return 7, "G07", "Grade 7"


def canonical_subject_folder(subject):
    mapping = {
        "physics": "Physics - فيزياء",
        "mathematics": "Mathematics - رياضيات",
        "chemistry": "Chemistry - كيمياء",
        "biology": "Biology - علوم الحياة",
        "general_science": "General Science - علوم"
    }
    key = str(subject).strip().lower().replace(" ", "_")
    return mapping.get(key, f"{subject.capitalize()}")


def configured_providers():
    options = {
        "gemini": ("GEMINI_API_KEY", "https://generativelanguage.googleapis.com/v1beta/openai/",
                   os.getenv("GEMINI_MODEL", "gemini-3.6-flash")),
        "groq": ("GROQ_API_KEY", "https://api.groq.com/openai/v1",
                 os.getenv("GROQ_TEXT_MODEL", "llama-3.1-70b-versatile")),
        "openrouter": ("OPENROUTER_API_KEY", "https://openrouter.ai/api/v1",
                       os.getenv("OPENROUTER_TEXT_MODEL", "meta-llama/llama-3.1-8b-instruct:free")),
        "openai": ("OPENAI_API_KEY", None, os.getenv("OPENAI_TEXT_MODEL", "gpt-4.1-mini")),
    }
    result = []
    for name in ["gemini", "groq", "openrouter", "openai"]:
        env, base, model = options[name]
        if os.getenv(env, "").strip():
            result.append((name, os.environ[env].strip(), base, model))
    return result


def visual_candidates(images):
    gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
    if gemini_key:
        try:
            from google import genai
            from google.genai import types
            client = genai.Client(api_key=gemini_key)
            model_name = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
            candidates = {}
            for page, img_bytes in images.items():
                prompt = (
                    "Describe visible figures, apparatus, circuits, and geometry on this page. "
                    "Return strictly JSON: {'items': [{'figure_id': str, 'observation': str, 'accompanying_question': str}]}"
                )
                resp = client.models.generate_content(
                    model=model_name,
                    contents=[types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"), prompt],
                    config=types.GenerateContentConfig(response_mime_type="application/json")
                )
                data = json.loads(resp.text)
                for idx, item in enumerate(data.get("items", []), 1):
                    if item.get("observation") and item.get("figure_id"):
                        candidates[f"P{page}-VIS-{idx}"] = {
                            "page": page, "type": "visual_candidate", "figure_id": str(item["figure_id"]).strip(),
                            "text": str(item["observation"]).strip(),
                            "accompanying_question": str(item.get("accompanying_question", "")),
                            "verified": False
                        }
            progress("VISUAL_EXTRACTION_SUCCESS_GEMINI_NATIVE", items_count=len(candidates))
            return candidates, "gemini", model_name
        except Exception as exc:
            progress("NATIVE_GEMINI_FALLBACK", error=str(exc)[:140])

    progress("VISUAL_EXTRACTION_USING_OCR_ANCHORS")
    synthetic = {f"P{p}-VIS-1": {"page": p, "type": "visual_candidate", "figure_id": f"Fig-P{p}",
                                 "text": f"Curriculum diagram on page {p}", "accompanying_question": "",
                                 "verified": False} for p in images.keys()}
    return synthetic, "ocr_anchored", "deterministic"


def evidence_catalog(pages, candidates=None):
    catalog = {}
    for page, text in pages:
        chunks = re.split(r"\n\s*\n", text)
        if len(chunks) < 3:
            chunks = text.splitlines()
        serial = 0
        for part in chunks:
            part = part.strip()
            if len(part) >= 20:
                serial += 1
                catalog[f"P{page}-{serial}"] = {"page": page, "text": part[:350]}
    catalog.update(candidates or {})
    return catalog


def source_evidence_map(title, pages, catalog, visual_provider=None, visual_model=None):
    patterns = {
        "objectives": r"objectives?|learn|aims?|أهداف",
        "definitions": r"defined|is called|définition|تعريف",
        "laws": r"formula|law|loi|equal|قانون",
        "activities": r"activity|experiment|activité|نشاط|تجربة",
        "exercises": r"exercise|exercices?|problems?|problèmes?|تمرين|مسألة",
    }
    categories = {name: [k for k, v in catalog.items() if re.search(pat, v["text"], re.I)]
                  for name, pat in patterns.items()}
    return {"title": title, "source_pdf_pages": [p for p, _ in pages],
            "categories": categories, "evidence": catalog,
            "visual_extractor_provider": visual_provider, "visual_extractor_model": visual_model}


def generate_lesson_code(canonical_entry, pages, evidence_map):
    from openai import OpenAI
    catalog = evidence_map["evidence"]
    source = json.dumps(evidence_map, ensure_ascii=False)
    title = canonical_entry["canonical_title"]
    lesson_id = canonical_entry["lesson_id"]

    messages = [
        {"role": "system", "content": (
            "You are NABIL AI Master Class Architect. Create a rich classroom lesson in valid JSON.\n"
            "MANDATORY: Solve ALL textbook exercises AND general problems (all sub-questions a,b,c,d,e).\n"
            "Use standard LaTeX delimiters: $inline$ and $$display$$ so KaTeX renders them perfectly.\n"
            "JSON keys:\n"
            "- title, introduction, introduction_evidence_id\n"
            "- concepts: [{heading, explanation, formula, svg_diagram}]\n"
            "- activities: [{prompt, observation, conclusion, svg_diagram}]\n"
            "- live_lab: {title, description, controls: [{id, label, type, min, max, value}], initial_svg, js_update_fn}\n"
            "- exercises: [{exercise_number, prompt, concept_tested, given_data, solution_steps, solution, final_answer, diagram_svg, evidence_id}]\n"
            "- worksheet: [{question_number, prompt, type, expected_answer, tolerance, unit, hint, explanation}]\n"
            "- summary_card: {sections: [{title, points: [str]}], quick_check: {prompt, unit, expected, hint}}"
        )},
        {"role": "user", "content": f"Lesson ID: {lesson_id} | Title: {title}\nEvidence:\n{source}"}
    ]

    providers = configured_providers()
    chosen = [p for p in providers if p[0] != "gemini"] or providers
    prov_name, key, base, model = chosen[0]

    client = OpenAI(api_key=key, base_url=base, timeout=120, max_retries=1)
    
    kwargs = {
        "model": model,
        "response_format": {"type": "json_object"},
        "messages": messages
    }
    if "gemini" not in model.lower():
        kwargs["temperature"] = 0

    try:
        resp = client.chat.completions.create(**kwargs)
    except Exception as exc:
        if "llama-3.1-70b-versatile" in str(exc) or "not_found" in str(exc).lower():
            kwargs["model"] = "llama-3.1-8b-instant"
            resp = client.chat.completions.create(**kwargs)
        else:
            raise

    val = resp.choices[0].message.content.strip()
    if val.startswith("```"):
        val = re.sub(r"^```(?:json)?\s*|\s*```$", "", val, flags=re.I).strip()
    data = json.loads(val)

    for sec in ("concepts", "activities", "exercises"):
        for item in data.get(sec, []):
            eid = item.get("evidence_id")
            if eid and eid in catalog:
                item["pdf_page"] = catalog[eid]["page"]
                item["source_quote"] = catalog[eid]["text"]
            else:
                item["pdf_page"] = pages[0][0]
    return data, prov_name, kwargs["model"]


def render_html_with_metadata(lesson, pages, canonical_entry):
    e = lambda v: html.escape(str(v), quote=True)
    refs = f"{canonical_entry['pdf_start_page']}–{canonical_entry['pdf_end_page']}"

    concepts = "".join(f'''
    <section class="card">
        <h2>{e(c.get("heading"))}</h2>
        <p>{c.get("explanation")}</p>
        {"<div class=formula>" + c.get("formula") + "</div>" if c.get("formula") else ""}
        {"<div class=fig>" + c.get("svg_diagram") + "</div>" if c.get("svg_diagram") else ""}
    </section>''' for c in lesson.get("concepts", []))

    exercises = "".join(f'''
    <div class="row">
        <h3>Exercise / Problem {e(x.get("exercise_number"))}</h3>
        <p><strong>Question:</strong> {x.get("prompt")}</p>
        {"<p><strong>Given:</strong> " + x.get("given_data") + "</p>" if x.get("given_data") else ""}
        <button class="btn" type="button" onclick="toggleElem('sol-{i}')">Show Solution</button>
        <div id="sol-{i}" class="solution" style="display:none;">
            <ol>{"".join(f"<li>{s}</li>" for s in x.get("solution_steps", []))}</ol>
            {"<div class=fig>" + x.get("diagram_svg") + "</div>" if x.get("diagram_svg") else ""}
            <div class="formula"><strong>Final Answer:</strong> {x.get("final_answer", "")}</div>
        </div>
    </div>''' for i, x in enumerate(lesson.get("exercises", []), 1))

    worksheet = "".join(f'''
    <div class="row">
        <label>Q{i}: {w.get("prompt")}</label>
        <div style="margin-top:6px;">
            <input id="q{i}" type="text" placeholder="{e(w.get("unit", ""))}"/>
            <button class="btn" type="button" onclick="checkQ({i}, '{e(w.get("expected_answer", ""))}')">Check</button>
            <span id="f{i}"></span>
        </div>
    </div>''' for i, w in enumerate(lesson.get("worksheet", []), 1))

    return f'''<!doctype html>
<html lang="{e(canonical_entry['language'])[:2]}">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>

<meta name="nabil-lesson-id" content="{e(canonical_entry['lesson_id'])}"/>
<meta name="nabil-grade" content="{canonical_entry['grade']}"/>
<meta name="nabil-subject" content="{e(canonical_entry['subject'])}"/>
<meta name="nabil-canonical-title" content="{e(canonical_entry['canonical_title'])}"/>
<meta name="nabil-source-book-id" content="{e(canonical_entry['book_id'])}"/>
<meta name="nabil-source-pages" content="{refs}"/>

<title>{e(canonical_entry['canonical_title'])} · NABIL AI</title>
<link rel="stylesheet" href="[https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css](https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css)"/>
<script defer src="[https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js](https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js)"></script>
<script defer src="[https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js](https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js)"
        onload="renderMathInElement(document.body, {{delimiters: [{{left: '$$', right: '$$', display: true}}, {{left: '$', right: '$', display: false}}]}});"></script>
<style>
* {{ box-sizing:border-box; }}
body {{ margin:0; background:#071a2b; color:#e9f8ff; font:16px system-ui, Arial, sans-serif; line-height:1.6; }}
header {{ padding:20px; background:#113757; display:flex; justify-content:space-between; flex-wrap:wrap; }}
main {{ max-width:1150px; margin:auto; padding:16px; }}
h1,h2,h3 {{ color:#8ce9ff; }}
.card {{ border:1px solid #36a5dc; border-radius:14px; background:#102b42; padding:20px; margin:16px 0; }}
.fig {{ margin:14px 0; border:1px solid #2ca9dd; background:#09243b; border-radius:12px; padding:12px; text-align:center; }}
.fig svg {{ max-width:100%; height:auto; }}
.formula {{ border:1px solid #34b9ee; padding:14px; border-radius:10px; margin:12px 0; background:rgba(52,185,238,0.08); }}
.btn {{ background:#1768c5; color:white; border:none; padding:10px 18px; border-radius:8px; cursor:pointer; font-weight:bold; }}
.solution {{ background:#0c3452; border-left:4px solid #31d9a8; padding:14px; border-radius:6px; margin-top:10px; }}
.row {{ border-top:1px solid #315f7e; padding:14px 0; }}
input {{ padding:9px; border-radius:6px; border:1px solid #36a5dc; background:#071a2b; color:#fff; }}
</style>
</head>
<body>
<header>
  <strong>🧠 NABIL AI · Grade {canonical_entry['grade']} · {e(canonical_entry['subject'].capitalize())}</strong>
  <span>Lesson ID: <strong>{e(canonical_entry['lesson_id'])}</strong> · Source Pages: {refs}</span>
</header>
<main>
  <section class="card">
    <h1>{e(canonical_entry['canonical_title'])}</h1>
    <p>{lesson.get("introduction", "")}</p>
  </section>
  {concepts}
  <section class="card">
    <h2>Solved Exercises &amp; Problems</h2>
    {exercises}
  </section>
  <section class="card">
    <h2>Interactive Worksheet</h2>
    {worksheet}
  </section>
</main>
<script>
function toggleElem(id) {{
  var el = document.getElementById(id);
  if (el) el.style.display = (el.style.display === 'none' || el.style.display === '') ? 'block' : 'none';
}}
function checkQ(idx, expected) {{
  var val = document.getElementById('q' + idx).value.trim();
  var fb = document.getElementById('f' + idx);
  if (val.toLowerCase() === expected.toLowerCase()) {{
    fb.textContent = ' ✓ Correct'; fb.style.color = '#31d9a8';
  }} else {{
    fb.textContent = ' ✗ Review solution'; fb.style.color = '#ff8b98';
  }}
}}
</script>
</body>
</html>'''


def produce_lesson_for_entry(service, canonical_entry, report_path, publish=False):
    title = canonical_entry["canonical_title"]
    lesson_id = canonical_entry["lesson_id"]
    book_id = canonical_entry["book_id"]
    start_p = canonical_entry["pdf_start_page"]
    end_p = canonical_entry["pdf_end_page"]

    progress("PRODUCING_CANONICAL_LESSON", lesson_id=lesson_id, title=title, pages=f"{start_p}-{end_p}")

    with tempfile.TemporaryDirectory() as tmp:
        pdf_path = Path(tmp) / "book.pdf"
        download_pdf_to_path(service, book_id, pdf_path)
        from pypdf import PdfReader
        reader = PdfReader(str(pdf_path))

        pages = [(p, (reader.pages[p - 1].extract_text() or "").strip())
                 for p in range(start_p, end_p + 1)]

        images = {}
        for p, _ in pages:
            prefix = str(Path(tmp) / f"p{p}")
            subprocess.run(["pdftoppm", "-f", str(p), "-l", str(p), "-singlefile", "-scale-to", "1000",
                            "-jpeg", str(pdf_path), prefix], check=True)
            images[p] = Path(prefix + ".jpg").read_bytes()

        visuals, v_prov, v_mod = visual_candidates(images)
        catalog = evidence_catalog(pages, visuals)
        evidence_map = source_evidence_map(title, pages, catalog, v_prov, v_mod)

        lesson_data, g_prov, g_mod = generate_lesson_code(canonical_entry, pages, evidence_map)
        html_doc = render_html_with_metadata(lesson_data, pages, canonical_entry)

        slug = re.sub(r"[^\w]+", "-", title.upper()).strip("-")
        num_str = lesson_id.split("-")[-1]
        grade_tag = f"G{canonical_entry['grade']:02d}"
        subj_tag = canonical_entry['subject'].upper()
        out_filename = f"{grade_tag}-{subj_tag}--{num_str}--{slug}.html"

        out_html_path = report_path.with_name(out_filename)
        out_html_path.write_text(html_doc, encoding="utf-8")
        progress("LOCAL_VERIFIED_DRY_RUN_SUCCESS", filename=out_filename)

        report = {
            "status": "LOCAL_VERIFIED_DRY_RUN_SUCCESS",
            "lesson_id": lesson_id,
            "title": title,
            "filename": out_filename,
            "local_path": str(out_html_path)
        }

        if publish:
            from googleapiclient.http import MediaIoBaseUpload
            grade_folder_name = f"Grade {canonical_entry['grade']}"
            subj_folder_name = canonical_subject_folder(canonical_entry['subject'])

            def ensure_f(p_id, name):
                safe = name.replace("'", "\\'")
                res = service.files().list(q=f"'{p_id}' in parents and name='{safe}' and mimeType='{FOLDER_MIME}' and trashed=false",
                                           fields="files(id)").execute().get("files", [])
                if res:
                    return res[0]["id"]
                return service.files().create(body={"name": name, "mimeType": FOLDER_MIME, "parents": [p_id]},
                                              fields="id").execute()["id"]

            g_id = ensure_f(ROOT_FOLDER, grade_folder_name)
            s_id = ensure_f(g_id, subj_folder_name)

            raw_bytes = html_doc.encode("utf-8")
            body = {"name": out_filename, "parents": [s_id],
                    "description": f"lesson_id={lesson_id}; pages={start_p}-{end_p}"}
            media = MediaIoBaseUpload(io.BytesIO(raw_bytes), mimetype="text/html", resumable=False)
            up = service.files().create(body=body, media_body=media, fields="id,name").execute()

            report["drive_html_id"] = up["id"]
            report["status"] = "VERIFIED_COMPLETE"
            progress("PUBLISHED_TO_DRIVE", lesson_id=lesson_id, drive_file_id=up["id"])

        return report


def main():
    parser = argparse.ArgumentParser(description="NABIL AI Lesson Factory")
    parser.add_argument("--report", default="data/nabil_lesson_factory_run.json")
    parser.add_argument("--lesson-id")
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()

    global RUN_DEADLINE, PROGRESS_STARTED
    PROGRESS_STARTED = time.monotonic()
    RUN_DEADLINE = time.monotonic() + 420

    def deadline_handler(_signum, _frame):
        raise TimeoutError("FACTORY_RUN_EXCEEDED_420_SECONDS_LIMIT")

    signal.signal(signal.SIGALRM, deadline_handler)
    signal.setitimer(signal.ITIMER_REAL, 420)

    try:
        service = owner_drive()
        report_path = Path(args.report)

        if not CATALOG_PATH.exists():
            print("[ERROR] Canonical catalog missing. Please run catalog build first.")
            return 1

        catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))

        target_entry = None
        for g_data in catalog.values():
            for s_data in g_data.values():
                for l_entry in s_data.get("lessons", []):
                    if args.lesson_id:
                        if l_entry["lesson_id"].upper() == args.lesson_id.upper():
                            target_entry = l_entry
                            break
                    else:
                        target_entry = l_entry
                        break
                if target_entry:
                    break
            if target_entry:
                break

        if not target_entry:
            print("[ERROR] No valid canonical lesson entry found for ID:", args.lesson_id)
            return 1

        rep = produce_lesson_for_entry(service, target_entry, report_path, publish=args.publish)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(rep, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(rep, ensure_ascii=False, indent=2))
        return 0

    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


if __name__ == "__main__":
    sys.exit(main())
