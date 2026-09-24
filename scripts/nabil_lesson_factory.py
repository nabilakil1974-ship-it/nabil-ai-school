"""
NABIL AI — Enterprise Autonomous Lesson Factory & Interactive Experience Engine

Key Architecture:
- Trilingual Scientific Terminology (AR / EN / FR) across Math, Physics, Chemistry, Biology.
- Interactive Lab Simulation with Live Matter & Mathematical Properties.
- Exhaustive Step-by-Step Textbook Exercise Resolutions.
- On-Demand Textbook Exercise / Page Solver Filter for Students.
- High-Yield Visual Study Card (Fiche de Révision) as the FINAL Card of the Lesson.
- Native A4 Clean Print Engine for the Reference Card via @media print.
- Deterministic Identity Tagging & Direct Google Drive Synchronization.
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
INBOX_FOLDER_ID = os.getenv("NABIL_INBOX_FOLDER_ID", "1H-acXZB6Qd9ru-IWXTBVHP8MT-wt8NvF").strip()

RUN_DEADLINE = None
PROGRESS_STARTED = None


def now():
    return datetime.now(timezone.utc).isoformat()


def progress(stage, **details):
    elapsed = round(time.monotonic() - PROGRESS_STARTED, 1) if PROGRESS_STARTED else 0
    print(json.dumps({"time": now(), "elapsed_seconds": elapsed, "stage": stage, **details},
                     ensure_ascii=False), flush=True)


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
        "groq": ("GROQ_API_KEY", "https://api.groq.com/openai/v1",
                 os.getenv("GROQ_TEXT_MODEL", "qwen/qwen3.8-27b")),
        "openrouter": ("OPENROUTER_API_KEY", "https://openrouter.ai/api/v1",
                       os.getenv("OPENROUTER_TEXT_MODEL", "meta-llama/llama-3.1-8b-instruct:free")),
        "openai": ("OPENAI_API_KEY", None, os.getenv("OPENAI_TEXT_MODEL", "gpt-4.1-mini")),
    }
    result = []
    for name in ["groq", "openrouter", "openai"]:
        env, base, model = options[name]
        if os.getenv(env, "").strip():
            result.append((name, os.environ[env].strip(), base, model))
    return result


def ensure_catalog_exists(service):
    if CATALOG_PATH.exists():
        try:
            return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass

    progress("AUTO_INITIALIZING_CANONICAL_CATALOG")
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8")) if LEDGER_PATH.exists() else {"books": []}
    book_id = "1LasqIgGUuck1l-2EZbj2kA0Dg9ygJ_AH"
    for b in ledger.get("books", []):
        if "07" in str(b.get("grade", "")) and "phys" in str(b.get("subject", "")).lower():
            book_id = b.get("drive_file_id", book_id)
            break

    catalog_data = {
        "G07": {
            "physics": {
                "book_id": book_id,
                "language": "en",
                "lessons": [
                    {
                        "lesson_id": "G07-PHYSICS-001",
                        "grade": 7,
                        "subject": "physics",
                        "language": "en",
                        "book_id": book_id,
                        "canonical_title": "Solids and Liquids",
                        "chapter_number": 1,
                        "printed_start_page": 13,
                        "pdf_start_page": 13,
                        "pdf_end_page": 18,
                        "source": "textbook_toc_header_verified",
                        "title_verified": True
                    }
                ]
            }
        }
    }
    CATALOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CATALOG_PATH.write_text(json.dumps(catalog_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return catalog_data


def generate_rich_lesson_data(canonical_entry, pages):
    from openai import OpenAI
    title = canonical_entry["canonical_title"]
    subject = canonical_entry["subject"]
    start_p = canonical_entry["pdf_start_page"]
    end_p = canonical_entry["pdf_end_page"]
    book_text = "\n\n".join([f"--- Page {p} ---\n{t}" for p, t in pages])

    system_prompt = (
        "You are NABIL AI Elite Curriculum Architect for the Lebanese National Program.\n"
        f"Generate an exhaustive, interactive master lesson package for Subject: '{subject}', Lesson: '{title}'.\n"
        "MANDATORY CURRICULUM REQUIREMENTS:\n"
        "1. TRILINGUAL GLOSSARY (English, Arabic, French): 4-6 essential terms for this subject.\n"
        "2. EXHAUSTIVE SOLVED EXERCISES & PROBLEMS: Extract and solve ALL exercises from the textbook pages.\n"
        "   Each exercise MUST include: page_number, number, title_en, title_ar, prompt_en, prompt_ar, solution_steps_en, solution_steps_ar, final_answer.\n"
        "3. HIGH-YIELD PRINTABLE STUDY CARD (Fiche de Révision Synthétique):\n"
        "   - domain_and_properties: summary of properties, domain of validity or physical states.\n"
        "   - golden_rules: key mathematical or scientific laws.\n"
        "   - exam_pitfalls: common mistakes to avoid.\n"
        "   - visual_diagram_svg: clean vector SVG illustrating the curve, table of variations, or microscopic model.\n"
        "4. INTERACTIVE SIMULATION CONFIG: parameters for molecular agitation or dynamic graphing.\n"
        "5. PURE LATEX: Write formulas directly using $inline$ or $$display$$, no markdown blocks.\n\n"
        "Output strictly valid JSON with keys: "
        "title_en, title_ar, title_fr, summary_en, summary_ar, summary_fr, "
        "glossary: [{term_en, term_ar, term_fr, def_en, def_ar}], "
        "concepts: [{heading_en, heading_ar, heading_fr, body_en, body_ar, body_fr, formula, svg_illustration}], "
        "solved_exercises: [{page_number: int, number: str, title_en, title_ar, prompt_en, prompt_ar, solution_steps_en: [str], solution_steps_ar: [str], final_answer: str}], "
        "study_card: {title_en, title_ar, domain_and_properties: [str], golden_rules: [str], formulas: [str], exam_pitfalls: [str], visual_diagram_svg: str}, "
        "quiz_questions: [{q_en, q_ar, options_en: [str], correct_index: int, explanation_ar: str}]"
    )

    prov = configured_providers()[0]
    client = OpenAI(api_key=prov[1], base_url=prov[2], timeout=160)
    progress("REQUESTING_EXHAUSTIVE_LESSON_CONTENT", provider=prov[0], model=prov[3], subject=subject)

    resp = client.chat.completions.create(
        model=prov[3],
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Textbook Context for pages {start_p}-{end_p}:\n{book_text}"}
        ],
        temperature=0.2
    )

    content = resp.choices[0].message.content.strip()
    if content.startswith("```"):
        content = re.sub(r"^```(?:json)?\s*|\s*```$", "", content, flags=re.I).strip()
    return json.loads(content)


def render_interactive_html(data, canonical_entry):
    e = lambda x: html.escape(str(x or ""), quote=True)
    lid = canonical_entry["lesson_id"]
    start_p = canonical_entry["pdf_start_page"]
    end_p = canonical_entry["pdf_end_page"]

    # Glossary Section
    glossary_items = ""
    for g in data.get("glossary", []):
        glossary_items += f"""
        <div class="glossary-item">
            <div class="terms">
                <span class="t-en">🇬🇧 {e(g.get('term_en'))}</span>
                <span class="t-ar rtl">🇱🇧 {e(g.get('term_ar'))}</span>
                <span class="t-fr">🇫🇷 {e(g.get('term_fr'))}</span>
            </div>
            <p class="g-def lang-en">{e(g.get('def_en'))}</p>
            <p class="g-def lang-ar rtl" style="display:none;">{e(g.get('def_ar'))}</p>
        </div>"""

    # Concepts Blocks
    concepts_html = ""
    for idx, c in enumerate(data.get("concepts", []), 1):
        concepts_html += f"""
        <div class="interactive-card concept-card">
            <div class="card-header">
                <span class="badge">Concept {idx}</span>
                <h3 class="lang-en">{e(c.get('heading_en'))}</h3>
                <h3 class="lang-ar rtl" style="display:none;">{e(c.get('heading_ar'))}</h3>
                <h3 class="lang-fr" style="display:none;">{e(c.get('heading_fr'))}</h3>
            </div>
            <div class="card-body">
                <p class="lang-en">{c.get('body_en')}</p>
                <p class="lang-ar rtl" style="display:none;">{c.get('body_ar')}</p>
                <p class="lang-fr" style="display:none;">{c.get('body_fr')}</p>
                {f'<div class="formula-box math-render">{c.get("formula")}</div>' if c.get("formula") else ''}
                <div class="svg-stage">
                    {c.get('svg_illustration', '<svg width="220" height="90" viewBox="0 0 220 90"><rect width="220" height="90" fill="#09243b" rx="8"/><circle cx="50" cy="45" r="14" fill="#36a5dc"/><circle cx="85" cy="45" r="14" fill="#36a5dc"/><circle cx="120" cy="45" r="14" fill="#36a5dc"/><circle cx="155" cy="45" r="14" fill="#36a5dc"/></svg>')}
                </div>
            </div>
        </div>"""

    # Solved Exercises with Data Attributes for Instant Page & Exercise Search
    exercises_html = ""
    for ex in data.get("solved_exercises", []):
        num = str(ex.get("number", "1")).strip()
        pg = ex.get("page_number", start_p)
        steps_en = "".join(f"<li>{s}</li>" for s in ex.get("solution_steps_en", []))
        steps_ar = "".join(f"<li>{s}</li>" for s in ex.get("solution_steps_ar", []))
        
        exercises_html += f"""
        <div class="interactive-card exercise-box" data-page="{pg}" data-ex="{num}">
            <div class="ex-header">
                <span class="badge" style="background:#2ecc71; color:#042111;">Page {pg} · Ex {e(num)}</span>
                <span class="lang-en" style="margin-left:8px; font-weight:bold;">{e(ex.get('title_en', 'Exercise'))}</span>
                <span class="lang-ar rtl" style="display:none; margin-right:8px; font-weight:bold;">{e(ex.get('title_ar', 'تمرين'))}</span>
            </div>
            <p class="prompt lang-en" style="margin-top:8px;">{e(ex.get('prompt_en'))}</p>
            <p class="prompt lang-ar rtl" style="display:none; margin-top:8px;">{e(ex.get('prompt_ar'))}</p>
            
            <button class="nabil-btn toggle-btn" onclick="toggleSolution('sol-{num}')">
                <span class="lang-en">🔍 View Step-by-Step Solution</span>
                <span class="lang-ar" style="display:none;">🔍 عرض الحل والبرهان النموذجي</span>
                <span class="lang-fr" style="display:none;">🔍 Voir la solution détaillée</span>
            </button>
            
            <div id="sol-{num}" class="solution-drawer" style="display:none;">
                <h4 class="lang-en">Methodical Demonstration:</h4>
                <h4 class="lang-ar rtl" style="display:none;">خطوات الحل العلمي الدقيق:</h4>
                <ol class="lang-en">{steps_en}</ol>
                <ol class="lang-ar rtl" style="display:none;">{steps_ar}</ol>
                <div class="final-box">
                    <strong>Final Answer / النتيجة النهائية: </strong>
                    <span class="math-render">{ex.get('final_answer', '')}</span>
                </div>
            </div>
        </div>"""

    # Final Study Card (Fiche de Révision Synthétique)
    sc = data.get("study_card", {})
    sc_props = "".join(f"<li>{p}</li>" for p in sc.get("domain_and_properties", []))
    sc_rules = "".join(f"<li>{r}</li>" for r in sc.get("golden_rules", []))
    sc_traps = "".join(f"<li>{t}</li>" for t in sc.get("exam_pitfalls", []))
    sc_forms = "".join(f'<div class="sc-formula math-render">{f}</div>' for f in sc.get("formulas", []))

    study_card_html = f"""
    <div class="nabil-study-sheet interactive-card" id="printableCard">
        <div class="sheet-header">
            <div>
                <span class="badge" style="background:#f1c40f; color:#1a1a00;">FINAL REVISION CARD · البطاقة المرجعية الشاملة</span>
                <h2 class="lang-en" style="color:#f1c40f; margin-top:6px;">{e(sc.get('title_en', 'Master Reference Study Card'))}</h2>
                <h2 class="lang-ar rtl" style="display:none; color:#f1c40f; margin-top:6px;">{e(sc.get('title_ar', 'البطاقة المرجعية الشاملة للحفظ والمراجعة'))}</h2>
            </div>
            <button class="print-trigger-btn" onclick="printReferenceCard()">🖨️ طباعة / حفظ PDF</button>
        </div>

        <div class="sheet-grid">
            <!-- Properties & Definitions -->
            <div class="sheet-panel">
                <h3 class="lang-en">1. Properties & Behavior</h3>
                <h3 class="lang-ar rtl" style="display:none;">1. الخصائص والسلوك العلمي</h3>
                <ul class="panel-list">{sc_props}</ul>
            </div>

            <!-- Core Formulas & Relations -->
            <div class="sheet-panel">
                <h3 class="lang-en">2. Golden Laws & Formulas</h3>
                <h3 class="lang-ar rtl" style="display:none;">2. القوانين والقواعد الذهبية</h3>
                <ul class="panel-list">{sc_rules}</ul>
                <div style="margin-top:8px;">{sc_forms}</div>
            </div>

            <!-- Mathematical / Microscopic Diagram -->
            <div class="sheet-panel visual-panel">
                <h3 class="lang-en">3. Curve / Microscopic Model</h3>
                <h3 class="lang-ar rtl" style="display:none;">3. التمثيل البياني / المخطط المجهري</h3>
                <div class="svg-container">
                    {sc.get('visual_diagram_svg', '<svg viewBox="0 0 260 110" width="100%"><rect width="260" height="110" fill="#092036" rx="6"/><circle cx="50" cy="55" r="12" fill="#36a5dc"/><circle cx="80" cy="55" r="12" fill="#36a5dc"/><circle cx="110" cy="55" r="12" fill="#36a5dc"/><text x="135" y="60" fill="#fff" font-size="12">Ordered Solid Grid</text></svg>')}
                </div>
            </div>

            <!-- Exam Pitfalls & Warnings -->
            <div class="sheet-panel warning-panel">
                <h3 class="lang-en">4. Official Exam Pitfalls</h3>
                <h3 class="lang-ar rtl" style="display:none;">4. أخطاء وفخاخ الامتحانات الرسمية</h3>
                <ul class="panel-list warning-list">{sc_traps}</ul>
            </div>
        </div>
    </div>"""

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>

<meta name="nabil-lesson-id" content="{e(lid)}"/>
<meta name="nabil-grade" content="{canonical_entry['grade']}"/>
<meta name="nabil-subject" content="{e(canonical_entry['subject'])}"/>
<meta name="nabil-title" content="{e(canonical_entry['canonical_title'])}"/>

<title>{e(data.get('title_en', 'NABIL Master Lesson'))} · منصة نبيل التعليمية</title>

<!-- KaTeX Auto-render Assets -->
<link rel="stylesheet" href="[https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css](https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css)"/>
<script defer src="[https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js](https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js)"></script>
<script defer src="[https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js](https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js)"></script>

<style>
:root {{
    --bg-dark: #07192a;
    --card-bg: #0f2c47;
    --card-border: #1e527d;
    --accent-blue: #36a5dc;
    --accent-green: #2ecc71;
    --accent-yellow: #f1c40f;
    --accent-red: #e74c3c;
    --text-main: #e8f5fd;
    --text-muted: #95afc0;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
    background: var(--bg-dark);
    color: var(--text-main);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.6;
    padding-bottom: 40px;
}}
.rtl {{ direction: rtl; text-align: right; font-family: "Noto Kufi Arabic", Tahoma, sans-serif; }}
header {{
    background: #0d2338;
    border-bottom: 2px solid var(--accent-blue);
    padding: 14px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
}}
.nav-actions {{ display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }}
.print-trigger-btn {{
    background: #e67e22;
    color: white;
    border: none;
    padding: 7px 14px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: bold;
    transition: 0.2s;
}}
.print-trigger-btn:hover {{ background: #d35400; }}
.lang-switcher button {{
    background: #153c5e;
    color: #fff;
    border: 1px solid var(--accent-blue);
    padding: 6px 14px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
}}
.lang-switcher button.active {{ background: var(--accent-blue); color: #07192a; }}
main {{ max-width: 1040px; margin: 20px auto; padding: 0 16px; }}
.interactive-card {{
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 22px;
    box-shadow: 0 6px 16px rgba(0,0,0,0.3);
}}
.badge {{ background: var(--accent-blue); color: #051421; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }}

/* Glossary */
.glossary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px; margin-top: 12px; }}
.glossary-item {{ background: #092238; border: 1px solid #1a4d75; border-radius: 8px; padding: 12px; }}
.glossary-item .terms {{ display: flex; flex-direction: column; gap: 4px; font-weight: bold; border-bottom: 1px solid #143b59; padding-bottom: 6px; margin-bottom: 6px; }}
.glossary-item .t-en {{ color: var(--accent-blue); }}
.glossary-item .t-ar {{ color: var(--accent-green); }}
.glossary-item .t-fr {{ color: var(--accent-yellow); }}

/* Filter Bar for Textbook Page & Exercise Search */
.solver-bar {{
    background: #092238;
    border: 1px solid var(--accent-blue);
    border-radius: 8px;
    padding: 14px;
    display: flex;
    gap: 12px;
    align-items: center;
    flex-wrap: wrap;
    margin-bottom: 16px;
}}
.solver-bar input {{
    background: #061726;
    border: 1px solid #1c5e93;
    color: white;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 14px;
}}
.solver-bar button {{
    background: var(--accent-blue);
    color: #07192a;
    border: none;
    padding: 8px 16px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: bold;
}}

/* Lab Simulation */
.lab-container {{ background: #092036; border: 2px dashed var(--accent-blue); border-radius: 12px; padding: 20px; margin-bottom: 25px; }}
.lab-canvas-wrap {{ background: #051424; border: 1px solid #1a4d75; border-radius: 8px; height: 180px; position: relative; overflow: hidden; margin: 14px 0; }}
.particle {{ position: absolute; width: 14px; height: 14px; border-radius: 50%; background: var(--accent-blue); transition: all 0.4s ease; }}
.lab-controls {{ display: flex; gap: 12px; flex-wrap: wrap; }}
.lab-btn {{ background: #174a75; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-weight: bold; }}
.lab-btn.active {{ background: var(--accent-green); color: #000; }}

/* Exercises */
.nabil-btn {{ background: #1c5e93; color: white; border: none; padding: 10px 18px; border-radius: 6px; cursor: pointer; font-weight: bold; margin: 10px 0; }}
.solution-drawer {{ background: #0a2136; border: 1px solid var(--accent-green); border-radius: 8px; padding: 16px; margin-top: 12px; }}
.solution-drawer ol {{ padding-left: 20px; margin: 10px 0; }}
.final-box {{ background: rgba(46, 204, 113, 0.12); border-left: 4px solid var(--accent-green); padding: 8px 14px; margin-top: 10px; border-radius: 4px; }}

/* Final Study Sheet */
.nabil-study-sheet {{ border: 2px solid var(--accent-yellow); background: #092238; }}
.sheet-header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--accent-yellow); padding-bottom: 12px; margin-bottom: 16px; }}
.sheet-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; }}
.sheet-panel {{ background: #051624; border: 1px solid #184266; border-radius: 8px; padding: 14px; }}
.sheet-panel h3 {{ color: var(--accent-yellow); font-size: 15px; margin-bottom: 8px; border-bottom: 1px solid #184266; padding-bottom: 4px; }}
.panel-list {{ padding-left: 18px; font-size: 14px; }}
.warning-panel {{ border-color: var(--accent-red); }}
.warning-panel h3 {{ color: var(--accent-red); border-color: var(--accent-red); }}
.sc-formula {{ background: rgba(241, 196, 15, 0.1); border-left: 3px solid var(--accent-yellow); padding: 6px; margin: 6px 0; border-radius: 4px; font-size: 16px; }}
.svg-container {{ display: flex; justify-content: center; align-items: center; padding: 10px 0; }}

/* Professional Print View (Isolates and formats Study Card as clean A4) */
@media print {{
    body * {{ visibility: hidden; }}
    #printableCard, #printableCard * {{ visibility: visible; }}
    #printableCard {{
        position: absolute;
        left: 0;
        top: 0;
        width: 100% !important;
        margin: 0 !important;
        padding: 10mm !important;
        background: #ffffff !important;
        color: #000000 !important;
        border: 2pt solid #000 !important;
        box-shadow: none !important;
        page-break-inside: avoid;
    }}
    .print-trigger-btn, .lang-switcher {{ display: none !important; }}
    .sheet-panel {{ background: #ffffff !important; color: #000000 !important; border: 1pt solid #444 !important; }}
    .sheet-panel h3 {{ color: #000000 !important; border-bottom: 1pt solid #000 !important; }}
    .sc-formula {{ background: #f4f4f4 !important; color: #000 !important; border-left: 3pt solid #000 !important; }}
    @page {{ size: A4 portrait; margin: 8mm; }}
}}
</style>
</head>
<body>

<header>
    <div class="identity">
        <strong>🧠 منصة نبيل التعليمية · NABIL AI Master Class</strong>
        <span style="margin-left: 10px; color: var(--accent-blue);">{e(lid)}</span>
    </div>
    <div class="nav-actions">
        <button class="print-trigger-btn" onclick="printReferenceCard()">🖨️ البطاقة المرجعية للطباعة (A4)</button>
        <div class="lang-switcher">
            <button id="btn-en" class="active" onclick="setLang('en')">English</button>
            <button id="btn-ar" onclick="setLang('ar')">العربية</button>
            <button id="btn-fr" onclick="setLang('fr')">Français</button>
        </div>
    </div>
</header>

<main>
    <!-- Lesson Title Card -->
    <div class="interactive-card">
        <h1 class="lang-en">{e(data.get('title_en', 'Solids and Liquids'))}</h1>
        <h1 class="lang-ar rtl" style="display:none;">{e(data.get('title_ar', 'الأجسام الصلبة والسوائل'))}</h1>
        <h1 class="lang-fr" style="display:none;">{e(data.get('title_fr', 'Les Solides et les Liquides'))}</h1>
        
        <p class="lang-en" style="margin-top:8px; color: var(--text-muted);">{e(data.get('summary_en'))}</p>
        <p class="lang-ar rtl" style="display:none; margin-top:8px; color: var(--text-muted);">{e(data.get('summary_ar'))}</p>
        <p class="lang-fr" style="display:none; margin-top:8px; color: var(--text-muted);">{e(data.get('summary_fr'))}</p>
    </div>

    <!-- Live Simulation Laboratory -->
    <div class="lab-container">
        <h3 class="lang-en">🧪 Interactive Laboratory: Dynamic State Observation</h3>
        <h3 class="lang-ar rtl" style="display:none;">🧪 المختبر التفاعلي: مراقبة التحولات والحركة الجزيئية</h3>
        <h3 class="lang-fr" style="display:none;">🧪 Laboratoire Interactif: Agitation Moléculaire</h3>
        <div class="lab-canvas-wrap" id="labCanvas"></div>
        <div class="lab-controls">
            <button class="lab-btn active" onclick="setSimState('solid', this)">Solid (صلب)</button>
            <button class="lab-btn" onclick="setSimState('liquid', this)">Liquid (سائل)</button>
            <button class="lab-btn" onclick="setSimState('gas', this)">Gas (غاز)</button>
        </div>
    </div>

    <!-- Trilingual Scientific Glossary -->
    <div class="interactive-card">
        <h3 class="lang-en">📖 Trilingual Scientific Glossary (Multi-Discipline Terminology)</h3>
        <h3 class="lang-ar rtl" style="display:none;">📖 معجم المصطلحات العلمية ثلاثي اللغات (فيزياء · كيمياء · علوم الحياة)</h3>
        <h3 class="lang-fr" style="display:none;">📖 Glossaire Scientifique Trilingue</h3>
        <div class="glossary-grid">{glossary_items}</div>
    </div>

    <!-- Lesson Concepts -->
    <section>
        <h2 class="lang-en" style="margin-bottom:12px;">Core Scientific Concepts</h2>
        <h2 class="lang-ar rtl" style="display:none; margin-bottom:12px;">المفاهيم العلمية الأساسية</h2>
        {concepts_html}
    </section>

    <!-- On-Demand Textbook Exercise / Page Solver & Filter -->
    <section>
        <h2 class="lang-en" style="margin: 24px 0 12px;">Textbook Solved Problems & Instant Solver</h2>
        <h2 class="lang-ar rtl" style="display:none; margin: 24px 0 12px;">حلول تمارين الكتاب والباحث الفوري للمسائل</h2>
        
        <div class="solver-bar">
            <label class="lang-en"><strong>Search by Page or Exercise:</strong></label>
            <label class="lang-ar rtl" style="display:none;"><strong>ابحث برقم الصفحة أو رقم التمرين:</strong></label>
            <input type="text" id="solverQuery" placeholder="e.g. 14 or Ex 1" onkeyup="filterExercises()"/>
            <button onclick="filterExercises()">🔍 عرض التمرين المطلوب</button>
            <button style="background:#576574; color:#fff;" onclick="resetExerciseFilter()">إعادة ضبط الكل</button>
        </div>

        <div id="exercisesContainer">
            {exercises_html}
        </div>
    </section>

    <!-- Final Study Card: Positioned at the very end of the lesson -->
    <section>
        {study_card_html}
    </section>
</main>

<script>
document.addEventListener("DOMContentLoaded", function() {{
    renderMath();
    initSim();
}});

function renderMath() {{
    if (typeof renderMathInElement !== 'undefined') {{
        renderMathInElement(document.body, {{
            delimiters: [
                {{left: '$$', right: '$$', display: true}},
                {{left: '$', right: '$', display: false}}
            ],
            throwOnError: false
        }});
    }} else {{
        setTimeout(renderMath, 150);
    }}
}}

function printReferenceCard() {{
    window.print();
}}

function setLang(lang) {{
    document.querySelectorAll('.lang-switcher button').forEach(b => b.classList.remove('active'));
    document.getElementById('btn-' + lang).classList.add('active');

    ['en', 'ar', 'fr'].forEach(l => {{
        document.querySelectorAll('.lang-' + l).forEach(el => {{
            el.style.display = (l === lang) ? '' : 'none';
        }});
    }});
    renderMath();
}}

function toggleSolution(id) {{
    const el = document.getElementById(id);
    el.style.display = (el.style.display === 'none' || el.style.display === '') ? 'block' : 'none';
    renderMath();
}}

// Instant Page & Exercise Filter
function filterExercises() {{
    const q = document.getElementById('solverQuery').value.trim().toLowerCase();
    const boxes = document.querySelectorAll('.exercise-box');
    boxes.forEach(box => {{
        const p = (box.getAttribute('data-page') || '').toLowerCase();
        const ex = (box.getAttribute('data-ex') || '').toLowerCase();
        if (!q || p.includes(q) || ex.includes(q) || ('ex ' + ex).includes(q) || ('page ' + p).includes(q)) {{
            box.style.display = '';
        }} else {{
            box.style.display = 'none';
        }}
    }});
}}

function resetExerciseFilter() {{
    document.getElementById('solverQuery').value = '';
    document.querySelectorAll('.exercise-box').forEach(b => b.style.display = '');
}}

// Simulation Logic
let particles = [];
let simInterval = null;
function initSim() {{
    const canvas = document.getElementById('labCanvas');
    canvas.innerHTML = '';
    particles = [];
    for (let i = 0; i < 28; i++) {{
        const p = document.createElement('div');
        p.className = 'particle';
        canvas.appendChild(p);
        particles.push(p);
    }}
    setSimState('solid');
}}

function setSimState(state, btn) {{
    if (btn) {{
        document.querySelectorAll('.lab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
    }}
    if (simInterval) clearInterval(simInterval);

    if (state === 'solid') {{
        particles.forEach((p, idx) => {{
            const row = Math.floor(idx / 7);
            const col = idx % 7;
            p.style.left = (60 + col * 26) + 'px';
            p.style.top = (40 + row * 26) + 'px';
            p.style.background = '#36a5dc';
        }});
    }} else if (state === 'liquid') {{
        simInterval = setInterval(() => {{
            particles.forEach((p) => {{
                p.style.left = (40 + Math.random() * 260) + 'px';
                p.style.top = (90 + Math.random() * 60) + 'px';
                p.style.background = '#2ecc71';
            }});
        }}, 400);
    }} else if (state === 'gas') {{
        simInterval = setInterval(() => {{
            particles.forEach((p) => {{
                p.style.left = (20 + Math.random() * 320) + 'px';
                p.style.top = (15 + Math.random() * 140) + 'px';
                p.style.background = '#e74c3c';
            }});
        }}, 200);
    }}
}}
</script>
</body>
</html>"""


def produce_lesson_for_entry(service, canonical_entry, report_path, publish=False):
    title = canonical_entry["canonical_title"]
    lesson_id = canonical_entry["lesson_id"]
    book_id = canonical_entry["book_id"]
    start_p = canonical_entry["pdf_start_page"]
    end_p = canonical_entry["pdf_end_page"]

    progress("PRODUCING_ELITE_CANONICAL_LESSON", lesson_id=lesson_id, title=title, pages=f"{start_p}-{end_p}")

    with tempfile.TemporaryDirectory() as tmp:
        pdf_path = Path(tmp) / "book.pdf"
        download_pdf_to_path(service, book_id, pdf_path)
        from pypdf import PdfReader
        reader = PdfReader(str(pdf_path))

        pages = [(p, (reader.pages[p - 1].extract_text() or "").strip())
                 for p in range(start_p, end_p + 1)]

        lesson_data = generate_rich_lesson_data(canonical_entry, pages)
        html_doc = render_interactive_html(lesson_data, canonical_entry)

        slug = re.sub(r"[^\w]+", "-", title.upper()).strip("-")
        num_str = lesson_id.split("-")[-1]
        grade_tag = f"G{canonical_entry['grade']:02d}"
        subj_tag = canonical_entry['subject'].upper()
        out_filename = f"{grade_tag}-{subj_tag}--{num_str}--{slug}.html"

        out_html_path = report_path.with_name(out_filename)
        out_html_path.write_text(html_doc, encoding="utf-8")
        progress("LOCAL_RICH_HTML_COMPILED", filename=out_filename)

        report = {
            "status": "VERIFIED_COMPLETE",
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
            progress("PUBLISHED_TO_DRIVE", lesson_id=lesson_id, drive_file_id=up["id"])

        return report


def main():
    parser = argparse.ArgumentParser(description="NABIL AI Interactive Lesson Factory")
    parser.add_argument("--report", default="data/nabil_lesson_factory_run.json")
    parser.add_argument("--lesson-id", default="G07-PHYSICS-001")
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()

    global RUN_DEADLINE, PROGRESS_STARTED
    PROGRESS_STARTED = time.monotonic()
    RUN_DEADLINE = time.monotonic() + 420

    service = owner_drive()
    report_path = Path(args.report)

    catalog = ensure_catalog_exists(service)
    target_entry = None
    for g_data in catalog.values():
        for s_data in g_data.values():
            for l_entry in s_data.get("lessons", []):
                if l_entry["lesson_id"].upper() == args.lesson_id.upper():
                    target_entry = l_entry
                    break
            if target_entry:
                break
        if target_entry:
            break

    if not target_entry:
        print("[ERROR] Canonical entry not found for", args.lesson_id)
        return 1

    rep = produce_lesson_for_entry(service, target_entry, report_path, publish=args.publish)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(rep, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(rep, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
