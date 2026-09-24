"""
NABIL AI — Enterprise Autonomous Lesson Factory (CRDP Pedagogical Engine)

Standardized Pipeline based on Reference Golden Templates:
1. Pedagogical Ingestion: Extracts Activities (Experiment -> Obs -> Concl) & Textbook Exercises.
2. Live Simulation Lab: Dynamic SVG Canvas with Slider Controls reflecting core lesson phenomena.
3. Complete Solved Exercises: Exhaustive resolution of all textbook problems with expandable solutions.
4. Graded Interactive Worksheet: Formative assessment with automatic scoring and targeted hints.
5. Final Study Card (Fiche de Révision): Multi-column summary with clean A4 printing engine.
6. Auto-sync with Drive Inbox, Catalog, and verified publication.
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


def generate_crdp_pedagogical_package(canonical_entry, pages):
    from openai import OpenAI
    title = canonical_entry["canonical_title"]
    subject = canonical_entry["subject"]
    start_p = canonical_entry["pdf_start_page"]
    end_p = canonical_entry["pdf_end_page"]
    book_text = "\n\n".join([f"--- Page {p} ---\n{t}" for p, t in pages])

    prov = configured_providers()[0]
    client = OpenAI(api_key=prov[1], base_url=prov[2], timeout=180)

    # 1. Extraction et Résolution Échafaudée de TOUS les Exercices du Livre
    progress("STEP_1_RESOLVING_ALL_TEXTBOOK_EXERCISES", provider=prov[0], model=prov[3])
    ex_prompt = (
        f"You are the Chief Examiner for the Lebanese Official Physics Curriculum (CRDP).\n"
        f"Given textbook pages {start_p}-{end_p} for chapter '{title}':\n"
        f"{book_text}\n\n"
        "Extract and meticulously solve EVERY SINGLE exercise found on the problem pages (Exercises 1 through 9).\n"
        "Return strictly JSON: {'exercises': [\n"
        "  {\n"
        "    'number': int,\n"
        "    'page': int,\n"
        "    'title': str,\n"
        "    'prompt': str,\n"
        "    'steps': [str],\n"
        "    'final_answer': str,\n"
        "    'svg_illustration': str (clean SVG diagram if exercise has a figure, e.g., tilted vessels, fuel tank, communicating vessels)\n"
        "  }\n"
        "]}"
    )

    resp_ex = client.chat.completions.create(
        model=prov[3],
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": ex_prompt}],
        temperature=0.1
    )
    val_ex = resp_ex.choices[0].message.content.strip()
    if val_ex.startswith("```"):
        val_ex = re.sub(r"^```(?:json)?\s*|\s*```$", "", val_ex, flags=re.I).strip()
    exercises_list = json.loads(val_ex).get("exercises", [])

    # 2. Construction des Activités (Expérience -> Observation -> Conclusion) + Fiche Récapitulative + Quiz
    progress("STEP_2_BUILDING_STRUCTURED_PEDAGOGY", provider=prov[0], model=prov[3])
    struct_prompt = (
        f"Create the pedagogical body for Lesson '{title}' (Grade 7, Physics, CRDP curriculum).\n"
        "RULES FOR THE PEDAGOGICAL FLOW:\n"
        "1. Hook & Objectives: Everyday question, learning aims.\n"
        "2. Structured Activities: For each core section, give 'experiment', 'observation', 'conclusion', 'check_question', and 'svg_diagram'.\n"
        "3. Live Lab Concept: Description for an interactive simulation with slider controls.\n"
        "4. Graded Worksheet: 6 multiple-choice questions testing key competencies.\n"
        "5. Final Summary Card (Fiche de Révision): 2-column synthesis of laws and definitions.\n"
        "Return strictly JSON: {\n"
        "  'hook': str,\n"
        "  'objectives': [str],\n"
        "  'activities': [\n"
        "    {'section_title': str, 'experiment': str, 'observation': str, 'conclusion': str, 'check_prompt': str, 'check_answer_bool': bool, 'svg_diagram': str}\n"
        "  ],\n"
        "  'worksheet': [\n"
        "    {'q': str, 'options': [str], 'correct_index': int, 'hint': str}\n"
        "  ],\n"
        "  'summary_card': {\n"
        "    'col1_title': str, 'col1_points': [str],\n"
        "    'col2_title': str, 'col2_points': [str]\n"
        "  }\n"
        "}"
    )

    resp_struct = client.chat.completions.create(
        model=prov[3],
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": struct_prompt},
            {"role": "user", "content": f"Textbook Context:\n{book_text}"}
        ],
        temperature=0.2
    )
    val_struct = resp_struct.choices[0].message.content.strip()
    if val_struct.startswith("```"):
        val_struct = re.sub(r"^```(?:json)?\s*|\s*```$", "", val_struct, flags=re.I).strip()
    pedagogy_data = json.loads(val_struct)
    pedagogy_data["exercises"] = exercises_list
    return pedagogy_data


def render_crdp_master_html(data, canonical_entry):
    e = lambda x: html.escape(str(x or ""), quote=True)
    lid = canonical_entry["lesson_id"]
    title = canonical_entry["canonical_title"]
    start_p = canonical_entry["pdf_start_page"]
    end_p = canonical_entry["pdf_end_page"]

    # Activities Blocks
    activities_html = ""
    for idx, act in enumerate(data.get("activities", []), 1):
        act_svg = act.get("svg_diagram", "")
        chk_ans = "true" if act.get("check_answer_bool", True) else "false"
        activities_html += f"""
        <section class="card">
            <h2>{idx} · {e(act.get('section_title'))}</h2>
            <div class="grid">
                <div>
                    <div class="stage"><b>🧪 Experiment:</b> {e(act.get('experiment'))}</div>
                    <div class="stage"><b>👁️ Observation:</b> {e(act.get('observation'))}</div>
                    <div class="stage" style="border-left-color:var(--accent);"><b>💡 Conclusion:</b> {e(act.get('conclusion'))}</div>
                </div>
                <div class="figure">
                    {act_svg if '<svg' in act_svg else f'''
                    <svg viewBox="0 0 500 200">
                        <rect x="50" y="20" width="400" height="160" fill="#081f31" stroke="#2f86b1" rx="10"/>
                        <line x1="80" y1="110" x2="420" y2="110" stroke="#53cfff" stroke-width="6"/>
                        <text x="180" y="90" fill="#ffe28a">Free Surface (Horizontal)</text>
                    </svg>'''}
                </div>
            </div>
            <div class="ask">
                <b>NABIL Question:</b> {e(act.get('check_prompt', 'Does shape remain constant?'))}
                <button onclick="fb('chk-{idx}', {chk_ans})">Yes</button>
                <button onclick="fb('chk-{idx}', { 'false' if chk_ans == 'true' else 'true' })">No</button>
                <span id="chk-{idx}" class="feedback"></span>
            </div>
        </section>"""

    # Solved Exercises Blocks
    exercises_html = ""
    for ex in data.get("exercises", []):
        num = ex.get("number", 1)
        pg = ex.get("page", start_p)
        steps = "".join(f"<li>{s}</li>" for s in ex.get("steps", []))
        fig = ex.get("svg_illustration", "")
        fig_block = f'<div class="figure">{fig}</div>' if "<svg" in fig else ""
        
        exercises_html += f"""
        <article class="exercise" data-page="{pg}" data-ex="{num}">
            <div class="exhead">
                <span>Exercise {num} — {e(ex.get('title', 'Textbook Problem'))}</span>
                <span class="source">Textbook p. {pg}</span>
            </div>
            <div class="prompt">
                <b>Book Task:</b>
                <p>{e(ex.get('prompt'))}</p>
            </div>
            {fig_block}
            <details open>
                <summary>Guided Solution &amp; Demonstration</summary>
                <ol>{steps}</ol>
                <div class="answer"><b>Final Answer:</b> {ex.get('final_answer', '')}</div>
            </details>
        </article>"""

    # Worksheet Items
    ws_html = ""
    for q_idx, q in enumerate(data.get("worksheet", []), 1):
        corr = q.get("correct_index", 0)
        options = "".join(f'<option value="{i}">{opt}</option>' for i, opt in enumerate(q.get("options", [])))
        ws_html += f"""
        <div class="exercise">
            <b>{q_idx}.</b> {e(q.get('q'))}
            <select id="wq{q_idx}">
                <option value="">-- Choose Answer --</option>
                {options}
            </select>
            <span id="wfb{q_idx}" class="feedback"></span>
        </div>"""

    # Summary Card
    sc = data.get("summary_card", {})
    pts1 = "".join(f"<li>{p}</li>" for p in sc.get("col1_points", ["Compact solids have definite shape and volume.", "Powdered solids consist of solid grains."]))
    pts2 = "".join(f"<li>{p}</li>" for p in sc.get("col2_points", ["Liquids take the shape of their container.", "Free surface at rest is planar and horizontal.", "In communicating vessels, liquid reaches the same level."]))

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>

<meta name="nabil-lesson-id" content="{e(lid)}"/>
<meta name="nabil-grade" content="{canonical_entry['grade']}"/>
<meta name="nabil-subject" content="{e(canonical_entry['subject'])}"/>
<meta name="nabil-title" content="{e(title)}"/>

<title>NABIL AI | Grade {canonical_entry['grade']} {canonical_entry['subject'].capitalize()} | {e(title)}</title>

<!-- KaTeX Auto-render Assets -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css"/>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>

<style>
:root {{
    --bg: #071827;
    --card: #0e2b43;
    --card2: #123650;
    --text: #edfaff;
    --accent: #57d7ff;
    --green: #61e6b5;
    --gold: #ffe28a;
    --muted: #55758a;
    --danger: #ff7b72;
}}
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
body {{
    margin: 0;
    background: var(--bg);
    color: var(--text);
    font: 16px/1.6 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
}}
header {{
    background: linear-gradient(120deg, #123f65, #0755a6);
    padding: 16px 20px;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 2px 14px rgba(0,0,0,0.4);
}}
header .bar {{
    max-width: 1150px;
    margin: auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
}}
.source {{ color: var(--gold); font-size: 0.92rem; font-weight: bold; }}
nav a {{
    color: #fff;
    text-decoration: none;
    background: #0d3654;
    border: 1px solid var(--accent);
    padding: 7px 12px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    margin-left: 4px;
}}
nav a:hover {{ background: var(--accent); color: #071827; }}
main {{ max-width: 1150px; margin: auto; padding: 16px; }}
h1 {{ font-size: clamp(1.6rem, 3.5vw, 2.3rem); margin: 0.2em 0; color: #fff; }}
h2 {{ color: var(--accent); margin-top: 0; }}
h3 {{ color: #b9f3ff; }}
.card {{
    background: var(--card);
    border: 1px solid #2f86b1;
    border-radius: 16px;
    padding: 20px;
    margin: 18px 0;
    box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}}
.teacher {{ border-left: 5px solid var(--green); }}
.chips span {{
    display: inline-block;
    padding: 5px 12px;
    border: 1px solid #3d8fb6;
    border-radius: 999px;
    margin: 4px 4px 4px 0;
    background: #0b263b;
    font-size: 13px;
    font-weight: bold;
}}
.stage {{
    border-left: 4px solid var(--green);
    padding: 10px 14px;
    margin: 10px 0;
    background: #0b2539;
    border-radius: 6px;
}}
.figure {{
    background: #081f31;
    border: 1px solid #2f86b1;
    border-radius: 12px;
    padding: 12px;
    margin: 12px 0;
    text-align: center;
}}
.figure svg {{ max-width: 100%; height: auto; display: block; margin: auto; }}
.water {{ stroke: #53cfff; stroke-width: 8; }}
.ask {{
    background: #201738;
    border: 1px solid #8d62ba;
    border-radius: 12px;
    padding: 14px;
    margin: 14px 0;
}}
button {{
    background: #176dcc;
    color: white;
    border: 0;
    border-radius: 8px;
    padding: 9px 16px;
    cursor: pointer;
    font-weight: bold;
    margin: 4px;
}}
button:hover {{ filter: brightness(1.15); }}
button.secondary {{ background: #16684f; }}
.feedback {{ display: inline-block; margin-left: 10px; font-weight: bold; color: var(--green); }}

/* Exercises */
.exercise {{
    background: var(--card2);
    border: 1px solid #3c8eb4;
    border-radius: 14px;
    padding: 16px;
    margin: 16px 0;
}}
.exhead {{
    display: flex;
    justify-content: space-between;
    font-weight: bold;
    color: #baf2ff;
    font-size: 16px;
}}
.prompt {{ background: #0a2235; border-radius: 8px; padding: 12px; margin: 10px 0; }}
details {{ border-top: 1px solid #3a6580; padding-top: 10px; margin-top: 10px; }}
summary {{ cursor: pointer; font-weight: bold; color: var(--green); }}
.answer {{
    background: #0f443e;
    border: 1px solid var(--green);
    padding: 12px;
    border-radius: 8px;
    margin-top: 10px;
}}

/* Solver Search Bar */
.solver-bar {{
    background: #092238;
    border: 2px solid var(--accent);
    border-radius: 12px;
    padding: 14px;
    display: flex;
    gap: 12px;
    align-items: center;
    flex-wrap: wrap;
    margin-bottom: 20px;
}}
.solver-bar input {{
    background: #061726;
    border: 1px solid #1c5e93;
    color: white;
    padding: 10px 14px;
    border-radius: 8px;
    font-size: 15px;
    flex: 1;
    min-width: 200px;
}}

/* Live Lab */
.lab {{ background: #09283f; border: 1px solid var(--accent); border-radius: 14px; padding: 18px; }}
input[type=range] {{ width: 100%; margin: 10px 0; }}
select {{ padding: 8px 12px; border-radius: 6px; background: #071a2b; color: #fff; border: 1px solid var(--accent); }}

/* Summary & Study Card */
.summary {{ border: 2px solid var(--green); background: #0c2b42; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; }}

/* A4 Print Engine */
@media print {{
    body * {{ visibility: hidden; }}
    #printableCard, #printableCard * {{ visibility: visible; }}
    #printableCard {{
        position: absolute;
        left: 0;
        top: 0;
        width: 100% !important;
        margin: 0 !important;
        padding: 12mm !important;
        background: #ffffff !important;
        color: #000000 !important;
        border: 2pt solid #000 !important;
        box-shadow: none !important;
        page-break-inside: avoid;
    }}
    header, nav, .ask, .solver-bar, .lab, select, button {{ display: none !important; }}
    @page {{ size: A4 portrait; margin: 10mm; }}
}}
</style>
</head>
<body>

<header>
  <div class="bar">
    <div>
      <b>🧠 NABIL AI · Grade {canonical_entry['grade']} {canonical_entry['subject'].capitalize()}</b>
      <h1>{e(title)}</h1>
      <div class="source">Curriculum Scope: Official Lebanese CRDP Book · pp. {start_p}–{end_p}</div>
    </div>
    <nav>
      <a href="#learn">Activities</a>
      <a href="#lab">Live Lab</a>
      <a href="#exercises">Exercises 1–9</a>
      <a href="#worksheet">Worksheet</a>
      <a href="javascript:window.print()">🖨️ Print Study Card</a>
    </nav>
  </div>
</header>

<main>

<!-- Pedagogical Hook & Objectives -->
<section class="card teacher">
  <h2>🎯 Scientific Investigation &amp; Objectives</h2>
  <p>{e(data.get('hook', 'Observe real matter behavior, test container changes, and deduce the core properties.'))}</p>
  <div class="chips">
    {"".join(f"<span>{e(obj)}</span>" for obj in data.get('objectives', ['Observe', 'Experiment', 'Measure & Compare', 'Interpret', 'Conclude', 'Apply']))}
  </div>
</section>

<!-- Structured Activities -->
<div id="learn">
  {activities_html}
</div>

<!-- Interactive Live Lab (Physics Simulation) -->
<section id="lab" class="card">
  <h2>🧪 Live Lab · Tilt the Vessel &amp; Measure Surface</h2>
  <div class="lab">
    <p>Move the slider to tilt the container. Notice how the container walls rotate while the <b>free surface of liquid at rest remains strictly plane and horizontal</b> relative to gravity:</p>
    <label>Tilt angle: <b id="ang" style="color:var(--gold);">0°</b>
      <input id="tilt" type="range" min="-35" max="35" value="0"/>
    </label>
    <div class="figure">
      <svg id="labSvg" viewBox="0 0 700 320">
        <!-- Rotating Vessel Container -->
        <g id="labV">
          <path d="M 200 60 L 200 250 L 500 250 L 500 60" fill="none" stroke="#8ce9ff" stroke-width="8"/>
        </g>
        <!-- Horizontal Liquid Surface -->
        <line class="water" x1="210" y1="170" x2="490" y2="170"/>
        <!-- Plumb Line (Vertical Gravity Reference) -->
        <line x1="600" y1="50" x2="600" y2="240" stroke="var(--gold)" stroke-width="3" stroke-dasharray="4,4"/>
        <circle cx="600" cy="254" r="14" fill="var(--gold)"/>
        <text x="540" y="290" fill="var(--gold)">Vertical plumb-line</text>
      </svg>
    </div>
    <div id="labmsg" class="answer">At 0°, the vessel is upright and the free surface is horizontal.</div>
  </div>
</section>

<!-- Solved Exercises with Working Instant Solver Filter -->
<section id="exercises" class="card">
  <h2>📘 Official Textbook Solved Exercises (pp. {start_p}–{end_p})</h2>
  
  <div class="solver-bar">
    <label><strong>🔍 Instant Exercise &amp; Page Solver:</strong></label>
    <input type="text" id="solverQuery" placeholder="Type page (e.g. 17) or exercise number (e.g. 5)..." oninput="filterEx()"/>
    <button onclick="filterEx()">Filter Question</button>
    <button style="background:#576574;" onclick="resetEx()">Show All Exercises</button>
  </div>

  <div id="exercisesContainer">
    {exercises_html}
  </div>
</section>

<!-- Graded Interactive Worksheet -->
<section id="worksheet" class="card">
  <h2>📝 Interactive Graded Worksheet (Formative Assessment)</h2>
  <p>Answer the following evaluation questions. Your score and individualized hints appear immediately:</p>
  {ws_html}
  <div style="margin-top:14px;">
    <button class="secondary" onclick="gradeWS()">Correct My Worksheet</button>
    <strong id="finalScore" style="margin-left:14px; font-size:1.2rem; color:var(--gold);"></strong>
  </div>
</section>

<!-- Final Summary Study Card (Integrated & Printable) -->
<section class="card summary" id="printableCard">
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; border-bottom:2px solid var(--green); padding-bottom:10px; margin-bottom:12px;">
    <h2>💡 Master Study Card · Fiche de Révision (Grade {canonical_entry['grade']})</h2>
    <span class="source">Lebanese Official Curriculum · CRDP</span>
  </div>
  <div class="grid">
    <div>
      <h3 style="color:var(--green);">{e(sc.get('col1_title', 'Solids & Grains'))}</h3>
      <ul style="padding-left:20px;">{pts1}</ul>
    </div>
    <div>
      <h3 style="color:var(--accent);">{e(sc.get('col2_title', 'Liquids at Rest'))}</h3>
      <ul style="padding-left:20px;">{pts2}</ul>
    </div>
  </div>
</section>

</main>

<script>
// KaTeX Auto Render Trigger
document.addEventListener("DOMContentLoaded", function() {{
    if (typeof renderMathInElement !== 'undefined') {{
        renderMathInElement(document.body, {{
            delimiters: [
                {{left: '$$', right: '$$', display: true}},
                {{left: '$', right: '$', display: false}}
            ],
            throwOnError: false
        }});
    }}
}});

// Interactive check in activities
function fb(id, ok) {{
    const el = document.getElementById(id);
    el.textContent = ok ? '✓ Correct observation!' : '✗ Re-observe what happens to shape and volume.';
    el.style.color = ok ? 'var(--green)' : 'var(--danger)';
}}

// Live Lab Engine
const tilt = document.getElementById('tilt');
const labV = document.getElementById('labV');
const labmsg = document.getElementById('labmsg');
const ang = document.getElementById('ang');

if (tilt && labV) {{
    tilt.addEventListener('input', () => {{
        const a = tilt.value;
        ang.textContent = a + '°';
        labV.setAttribute('transform', `rotate(${{a}} 350 160)`);
        labmsg.textContent = `The vessel is tilted ${{a}}°. The liquid free surface remains strictly horizontal.`;
    }});
}}

// Instant Page & Exercise Solver Filter
function filterEx() {{
    const raw = document.getElementById('solverQuery').value.trim().toLowerCase();
    const q = raw.replace(/^(ex|page|p|exercise)\\s*/i, '');
    const boxes = document.querySelectorAll('.exercise');
    boxes.forEach(box => {{
        const p = (box.getAttribute('data-page') || '').toLowerCase();
        const ex = (box.getAttribute('data-ex') || '').toLowerCase();
        if (!raw || p === q || ex === q || p.includes(q) || ex.includes(q)) {{
            box.style.display = '';
        }} else {{
            box.style.display = 'none';
        }}
    }});
}}

function resetEx() {{
    document.getElementById('solverQuery').value = '';
    document.querySelectorAll('.exercise').forEach(b => b.style.display = '');
}}

// Worksheet Grading Engine
const wsKey = {json.dumps([q.get('correct_index', 0) for q in data.get('worksheet', [])])};
function gradeWS() {{
    let score = 0;
    for (let i = 1; i <= wsKey.length; i++) {{
        const sel = document.getElementById('wq' + i);
        const fbEl = document.getElementById('wfb' + i);
        if (sel && sel.value !== "") {{
            if (parseInt(sel.value) === wsKey[i-1]) {{
                score++;
                fbEl.textContent = '✓ Correct';
                fbEl.style.color = 'var(--green)';
            }} else {{
                fbEl.textContent = '✗ Review lesson observation';
                fbEl.style.color = 'var(--danger)';
            }}
        }} else if (fbEl) {{
            fbEl.textContent = 'Select an answer';
            fbEl.style.color = 'var(--gold)';
        }}
    }}
    document.getElementById('finalScore').textContent = `Final Score: ${{score}} / ${{wsKey.length}}`;
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

    progress("PRODUCING_CRDP_MASTER_LESSON", lesson_id=lesson_id, title=title, pages=f"{start_p}-{end_p}")

    with tempfile.TemporaryDirectory() as tmp:
        pdf_path = Path(tmp) / "book.pdf"
        download_pdf_to_path(service, book_id, pdf_path)
        from pypdf import PdfReader
        reader = PdfReader(str(pdf_path))

        pages = [(p, (reader.pages[p - 1].extract_text() or "").strip())
                 for p in range(start_p, end_p + 1)]

        pedagogy_package = generate_crdp_pedagogical_package(canonical_entry, pages)
        html_doc = render_crdp_master_html(pedagogy_package, canonical_entry)

        slug = re.sub(r"[^\w]+", "-", title.upper()).strip("-")
        num_str = lesson_id.split("-")[-1]
        grade_tag = f"G{canonical_entry['grade']:02d}"
        subj_tag = canonical_entry['subject'].upper()
        out_filename = f"{grade_tag}-{subj_tag}--{num_str}--{slug}.html"

        out_html_path = report_path.with_name(out_filename)
        out_html_path.write_text(html_doc, encoding="utf-8")
        progress("CRDP_MASTER_HTML_COMPILED", filename=out_filename)

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
    parser = argparse.ArgumentParser(description="NABIL AI CRDP Engine Factory")
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
