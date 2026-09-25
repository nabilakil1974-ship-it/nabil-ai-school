"""
NABIL AI — Enterprise Autonomous Twin-Engine Lesson Factory

Key Architecture:
1. Twin-Page Output:
   - Page A: Theory, Activities, Live Lab, Graded Worksheet, Printable Summary Card.
   - Page B: Dedicated Solved Exercises & Problems Workbook.
2. NABIL Pedagogical Oral Style:
   - "المعطى أعطانا... هذا يعني... المطلوب... إذن نستخدم... نعوّض... نستنتج..."
3. Dynamic In-Place Trilingual/Arabic Toggle:
   - English remains the primary standard; interactive Arabic explanations toggle on demand.
4. Micro-Batched Safe Processing:
   - Immune to 429 RateLimitError.
"""

import argparse
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
    catalog_data = {
        "G07": {
            "physics": {
                "book_id": "1LasqIgGUuck1l-2EZbj2kA0Dg9ygJ_AH",
                "language": "en",
                "lessons": [
                    {
                        "lesson_id": "G07-PHYSICS-001",
                        "grade": 7,
                        "subject": "physics",
                        "language": "en",
                        "book_id": "1LasqIgGUuck1l-2EZbj2kA0Dg9ygJ_AH",
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


def discover_all_exercises_and_problems(pages_text):
    pattern = re.compile(r"(?:exercise|exercice|problem|question|تمرين|مسألة)\s*(\d+)", re.I)
    seen = set()
    items = []
    for match in pattern.finditer(pages_text):
        num = int(match.group(1))
        if num not in seen:
            seen.add(num)
            items.append(num)
    if not items:
        items = list(range(1, 10))
    return sorted(items)


def solve_all_exercises_with_nabil_method(client, model, canonical_entry, pages, exercise_ids):
    """
    Micro-Batched Exercise Solving injecting NABIL's Arabic Pedagogical Oral Flow:
    المعطى أعطانا -> هذا يعني -> المطلوب -> إذن نستخدم -> نعوّض -> نستنتج
    """
    title = canonical_entry["canonical_title"]
    end_p = canonical_entry["pdf_end_page"]
    ex_pages = [(p, t) for p, t in pages if p >= (end_p - 2)]
    ex_text = "\n\n".join([f"=== Page {p} ===\n{t}" for p, t in ex_pages])

    all_solved = []
    batch_size = 2
    batches = [exercise_ids[i:i + batch_size] for i in range(0, len(exercise_ids), batch_size)]

    for idx, batch in enumerate(batches, 1):
        progress("PROCESSING_NABIL_EXERCISE_BATCH", batch=idx, total=len(batches), items=batch)
        prompt = (
            f"You are Teacher NABIL, the master physics professor for the Lebanese CRDP curriculum.\n"
            f"Chapter: '{title}'. Textbook Problem Pages:\n{ex_text}\n\n"
            f"TASK: Solve items: {batch}.\n"
            "STRICT PEDAGOGICAL INSTRUCTIONS:\n"
            "1. Keep the official question prompt and technical steps in English.\n"
            "2. Provide NABIL's spoken explanation in clear, friendly Arabic using this EXACT structured flow:\n"
            "   - المعطى أعطانا: (State givens)\n"
            "   - هذا يعني: (Physical meaning)\n"
            "   - المطلوب: (Goal)\n"
            "   - إذن نستخدم: (Rule or Law)\n"
            "   - نعوّض / نعلل: (Application)\n"
            "   - نستنتج: (Final deduction)\n"
            "3. If an item references a figure (e.g. tilted container, fuel tank, tubes), output a clear SVG (viewBox='0 0 600 240').\n\n"
            "Output valid JSON: {'items': [\n"
            "  {\n"
            "    'number': int,\n"
            "    'title': str,\n"
            "    'prompt_en': str,\n"
            "    'prompt_ar': str,\n"
            "    'steps_en': [str],\n"
            "    'nabil_oral_explanation_ar': str,\n"
            "    'final_answer': str,\n"
            "    'svg_diagram': str\n"
            "  }\n"
            "]}"
        )

        for attempt in range(1, 4):
            try:
                resp = client.chat.completions.create(
                    model=model,
                    response_format={"type": "json_object"},
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=850,
                    temperature=0.0
                )
                txt = resp.choices[0].message.content.strip()
                if txt.startswith("```"):
                    txt = re.sub(r"^```(?:json)?\s*|\s*```$", "", txt, flags=re.I).strip()
                items = json.loads(txt).get("items", [])
                for it in items:
                    all_solved.append(it)
                break
            except Exception as e:
                progress("BATCH_WAIT_RETRY", error=str(e)[:100], attempt=attempt)
                time.sleep(4)

        time.sleep(2)

    return all_solved


def generate_lesson_theory_package(client, model, canonical_entry, pages):
    title = canonical_entry["canonical_title"]
    full_text = "\n\n".join([f"=== Page {p} ===\n{t}" for p, t in pages])

    progress("GENERATING_THEORY_WITH_BILINGUAL_SUPPORT")
    prompt = (
        f"Create the structured classroom lesson for Grade {canonical_entry['grade']} Physics: '{title}'.\n"
        f"SOURCE EVIDENCE ONLY:\n{full_text}\n\n"
        "RULES:\n"
        "1. Strictly NO surface tension, cohesion, adhesion, or molecular subatomic physics.\n"
        "2. Provide 4 activities with English text, along with optional Arabic translations for experiment, observation, conclusion, and inquiry.\n"
        "3. Live lab configuration for tilting the vessel.\n"
        "4. Formative graded worksheet of 6 questions.\n"
        "5. Final Study Card: 3 comprehensive panels (Solids, Liquids at rest, Communicating vessels) with SVG diagrams.\n"
        "Return strictly JSON: {\n"
        "  'hook_en': str, 'hook_ar': str,\n"
        "  'objectives': [str],\n"
        "  'activities': [\n"
        "    {\n"
        "      'title_en': str, 'title_ar': str,\n"
        "      'experiment_en': str, 'experiment_ar': str,\n"
        "      'observation_en': str, 'observation_ar': str,\n"
        "      'conclusion_en': str, 'conclusion_ar': str,\n"
        "      'question_prompt_en': str, 'question_prompt_ar': str,\n"
        "      'correct_is_yes': bool,\n"
        "      'svg_diagram': str\n"
        "    }\n"
        "  ],\n"
        "  'worksheet': [\n"
        "    {'q': str, 'options': [str], 'correct_index': int}\n"
        "  ],\n"
        "  'study_card': {\n"
        "    'title': str,\n"
        "    'panels': [\n"
        "      {'heading': str, 'points': [str], 'svg_diagram': str}\n"
        "    ]\n"
        "  }\n"
        "}"
    )

    resp = client.chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": prompt}],
        max_tokens=950,
        temperature=0.1
    )
    txt = resp.choices[0].message.content.strip()
    if txt.startswith("```"):
        txt = re.sub(r"^```(?:json)?\s*|\s*```$", "", txt, flags=re.I).strip()
    return json.loads(txt)


def get_shared_css():
    return """
    :root {
      --bg-main: #061325;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --card-bg: #0c1e36;
      --card-border: #1e3a5f;
      --c-hook-border: #38bdf8;
      --c-exp-bar: #38bdf8;
      --c-obs-bar: #fbbf24;
      --c-concl-bar: #34d399;
      --c-lab-border: #06b6d4;
      --c-ex-border: #10b981;
      --c-sol-bg: #052e24;
      --c-sol-text: #ecfdf5;
      --c-card-gold: #f59e0b;
      --c-arabic-box: #082845;
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      background: var(--bg-main);
      color: var(--text-main);
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
      line-height: 1.65;
      font-size: 16px;
    }
    header {
      background: linear-gradient(135deg, #0f2744 0%, #034275 100%);
      padding: 16px 22px;
      position: sticky;
      top: 0;
      z-index: 100;
      box-shadow: 0 4px 20px rgba(0,0,0,0.5);
      border-bottom: 2px solid var(--c-hook-border);
    }
    header .bar {
      max-width: 1150px;
      margin: auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }
    .source { color: var(--c-obs-bar); font-size: 0.95rem; font-weight: bold; }
    nav a, .nav-btn {
      color: #ffffff;
      text-decoration: none;
      background: #0b294a;
      border: 1px solid var(--c-hook-border);
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 14px;
      font-weight: 600;
      margin-left: 6px;
      display: inline-block;
      transition: all 0.25s ease;
    }
    nav a:hover, .nav-btn:hover {
      background: var(--c-hook-border);
      color: #061325;
      transform: translateY(-1px);
    }
    .cta-exercises-box {
      background: linear-gradient(135deg, #072a4a, #0b3d68);
      border: 2px solid var(--c-ex-border);
      border-radius: 16px;
      padding: 24px;
      text-align: center;
      margin: 28px 0;
      box-shadow: 0 8px 24px rgba(0,0,0,0.4);
    }
    .cta-exercises-btn {
      background: var(--c-ex-border);
      color: #042114;
      font-size: 1.15rem;
      font-weight: 800;
      padding: 14px 28px;
      border-radius: 10px;
      text-decoration: none;
      display: inline-block;
      margin-top: 12px;
      transition: 0.25s;
    }
    .cta-exercises-btn:hover {
      background: #34d399;
      transform: scale(1.03);
    }
    main { max-width: 1150px; margin: auto; padding: 20px 16px; }
    h1 { font-size: clamp(1.6rem, 3.5vw, 2.3rem); margin: 0.2em 0; color: #ffffff; font-weight: 800; }
    h2 { color: var(--c-hook-border); margin-top: 0; font-size: 1.4rem; }
    h3 { color: #bae6fd; font-size: 1.15rem; }
    .card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 22px;
      margin: 22px 0;
      box-shadow: 0 10px 25px rgba(0,0,0,0.35);
    }
    .card.teacher { border-left: 6px solid var(--c-hook-border); background: #092038; }
    .chips span {
      display: inline-block;
      padding: 5px 12px;
      border: 1px solid #3d8fb6;
      border-radius: 999px;
      margin: 4px 4px 4px 0;
      background: #0b263b;
      font-size: 13px;
      font-weight: bold;
    }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
    .stage-exp { border-left: 4px solid var(--c-exp-bar); padding: 12px 16px; margin: 10px 0; background: #0a2544; border-radius: 8px; }
    .stage-obs { border-left: 4px solid var(--c-obs-bar); padding: 12px 16px; margin: 10px 0; background: #241d08; border-radius: 8px; }
    .stage-concl { border-left: 4px solid var(--c-concl-bar); padding: 12px 16px; margin: 10px 0; background: #062b21; border-radius: 8px; }
    .figure {
      background: #051424;
      border: 1px solid #1a3d64;
      border-radius: 14px;
      padding: 18px;
      margin: 14px 0;
      text-align: center;
    }
    .figure svg {
      width: 100%;
      max-width: 650px;
      min-height: 200px;
      height: auto;
      display: block;
      margin: auto;
    }
    .figure svg text { font-family: system-ui, sans-serif; font-weight: 600; fill: #e2e8f0; }
    .water { stroke: #53cfff; stroke-width: 7; }
    .ask { background: #201738; border: 1px solid #8d62ba; border-radius: 12px; padding: 14px; margin: 14px 0; }
    button {
      background: #176dcc;
      color: white;
      border: 0;
      border-radius: 8px;
      padding: 9px 16px;
      cursor: pointer;
      font-weight: bold;
      margin: 4px;
    }
    button:hover { filter: brightness(1.15); }
    button.secondary { background: #16684f; }
    .btn-toggle-ar {
      background: #0f3d64;
      border: 1px solid #38bdf8;
      color: #bae6fd;
      font-size: 13.5px;
      padding: 6px 12px;
      border-radius: 6px;
      cursor: pointer;
      margin-top: 6px;
      display: inline-block;
    }
    .arabic-explanation-box {
      background: var(--c-arabic-box);
      border-right: 4px solid #38bdf8;
      border-radius: 8px;
      padding: 14px;
      margin: 10px 0;
      direction: rtl;
      text-align: right;
      font-family: "Noto Kufi Arabic", Tahoma, sans-serif;
      line-height: 1.7;
    }
    .nabil-oral-box {
      background: #092c22;
      border-right: 4px solid var(--c-concl-bar);
      border-radius: 8px;
      padding: 14px;
      margin: 12px 0;
      direction: rtl;
      text-align: right;
      font-family: "Noto Kufi Arabic", Tahoma, sans-serif;
    }
    .feedback { display: inline-block; margin-left: 10px; font-weight: bold; }
    .exercise {
      background: #0b223c;
      border: 1px solid #1b456f;
      border-left: 5px solid var(--c-ex-border);
      border-radius: 14px;
      padding: 20px;
      margin: 20px 0;
    }
    .exhead {
      display: flex;
      justify-content: space-between;
      font-weight: bold;
      color: #6ee7b7;
      font-size: 1.05rem;
      border-bottom: 1px solid #1a4268;
      padding-bottom: 10px;
      margin-bottom: 12px;
    }
    .prompt { background: #05182c; border-radius: 8px; padding: 14px; margin: 12px 0; font-size: 15.5px; color: #f1f5f9; }
    details { margin-top: 10px; }
    summary { cursor: pointer; font-weight: bold; color: var(--c-concl-bar); padding: 4px 0; }
    .answer {
      background: var(--c-sol-bg);
      border: 1px solid var(--c-concl-bar);
      color: var(--c-sol-text);
      padding: 14px 18px;
      border-radius: 8px;
      margin-top: 12px;
      font-weight: 500;
    }
    .lab { background: #09283f; border: 1px solid var(--c-lab-border); border-radius: 14px; padding: 18px; }
    input[type=range] { width: 100%; margin: 10px 0; }
    select { padding: 8px 12px; border-radius: 6px; background: #071a2b; color: #fff; border: 1px solid var(--c-hook-border); }
    .summary { border: 2px solid var(--c-card-gold); background: #0c1a2d; box-shadow: 0 0 25px rgba(245, 158, 11, 0.15); }
    .sc-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px; }
    .sc-panel { background: #061527; border: 1px solid #1c3d63; border-radius: 12px; padding: 16px; }
    @media print {
      body * { visibility: hidden; }
      #printableCard, #printableCard * { visibility: visible; }
      #printableCard {
        position: absolute;
        left: 0;
        top: 0;
        width: 100% !important;
        margin: 0 !important;
        padding: 12mm !important;
        background: #ffffff !important;
        color: #000000 !important;
        border: 2pt solid #000 !important;
      }
      .sc-panel { background: #ffffff !important; border: 1pt solid #444 !important; color: #000 !important; }
      header, nav, .ask, .lab, select, button, .cta-exercises-box, .btn-toggle-ar { display: none !important; }
      @page { size: A4 portrait; margin: 10mm; }
    }
    @media(max-width:720px){ .grid { grid-template-columns: 1fr; } }
    """


def render_page_a_theory(theory_data, canonical_entry, exercises_filename):
    e = html.escape
    title = canonical_entry["canonical_title"]
    lid = canonical_entry["lesson_id"]
    start_p = canonical_entry["pdf_start_page"]
    end_p = canonical_entry["pdf_end_page"]

    activities_html = ""
    for idx, act in enumerate(theory_data.get("activities", []), 1):
        yes_no = "true" if act.get("correct_is_yes", True) else "false"
        no_yes = "false" if act.get("correct_is_yes", True) else "true"
        svg = act.get("svg_diagram", "")
        if not svg or "<svg" not in svg:
            svg = '<svg viewBox="0 0 600 240"><rect x="40" y="30" width="520" height="180" fill="#081f31" stroke="#2f86b1" stroke-width="4" rx="10"/><text x="180" y="125" fill="#8ce9ff" font-size="20" font-weight="bold">Core Activity Observation</text></svg>'

        activities_html += f"""
        <section class="card">
          <h2>{idx} · {e(act.get('title_en', 'Activity'))}</h2>
          <button class="btn-toggle-ar" onclick="toggleAr('ar-act-{idx}')">🌐 الشرح والترجمة بالعربية</button>
          
          <div id="ar-act-{idx}" class="arabic-explanation-box" style="display:none;">
            <strong>النشاط {idx}: {e(act.get('title_ar', ''))}</strong>
            <p><strong>التجربة:</strong> {e(act.get('experiment_ar', ''))}</p>
            <p><strong>الملاحظة:</strong> {e(act.get('observation_ar', ''))}</p>
            <p><strong>الاستنتاج العلمي:</strong> {e(act.get('conclusion_ar', ''))}</p>
          </div>

          <div class="grid">
            <div>
              <div class="stage-exp"><b>🧪 Experiment:</b> {e(act.get('experiment_en', ''))}</div>
              <div class="stage-obs"><b>👁️ Observation:</b> {e(act.get('observation_en', ''))}</div>
              <div class="stage-concl"><b>💡 Conclusion:</b> {e(act.get('conclusion_en', ''))}</div>
            </div>
            <div class="figure">{svg}</div>
          </div>
          <div class="ask">
            <b>NABIL Inquiry:</b> {e(act.get('question_prompt_en', ''))}
            <button onclick="fb('chk-{idx}', {yes_no})">Yes</button>
            <button onclick="fb('chk-{idx}', {no_yes})">No</button>
            <span id="chk-{idx}" class="feedback"></span>
            <div style="font-size:13px; color:var(--text-muted); margin-top:4px; direction:rtl; text-align:right;">{e(act.get('question_prompt_ar', ''))}</div>
          </div>
        </section>"""

    ws_html = ""
    for q_idx, q in enumerate(theory_data.get("worksheet", []), 1):
        opts = "".join(f'<option value="{i}">{opt}</option>' for i, opt in enumerate(q.get("options", [])))
        ws_html += f"""
        <div class="exercise">
          <b>{q_idx}.</b> {e(q.get('q', ''))}
          <select id="wq{q_idx}">
            <option value="">-- Choose Answer --</option>
            {opts}
          </select>
          <span id="wfb{q_idx}" class="feedback"></span>
        </div>"""

    panels_html = ""
    for p in theory_data.get("study_card", {}).get("panels", []):
        pts = "".join(f"<li>{pt}</li>" for pt in p.get("points", []))
        svg_panel = p.get("svg_diagram", "")
        fig_p = f'<div class="figure">{svg_panel}</div>' if svg_panel and "<svg" in svg_panel else ""
        panels_html += f"""
        <div class="sc-panel">
          <h3 style="color:#6ee7b7;">{e(p.get('heading', ''))}</h3>
          <ul style="padding-left:18px;">{pts}</ul>
          {fig_p}
        </div>"""

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<meta name="nabil-lesson-id" content="{e(lid)}"/>
<title>NABIL AI | Grade {canonical_entry['grade']} Physics | {e(title)}</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css"/>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>
<style>{get_shared_css()}</style>
</head>
<body>
<header>
  <div class="bar">
    <div>
      <b>🧠 NABIL AI · Grade {canonical_entry['grade']} Physics</b>
      <h1>{e(title)}</h1>
      <div class="source">Curriculum Scope: Lebanese CRDP Official Textbook · pp. {start_p}–{end_p}</div>
    </div>
    <nav>
      <a href="#learn">Activities</a>
      <a href="#lab">Live Lab</a>
      <a href="#worksheet">Worksheet</a>
      <a href="{e(exercises_filename)}" style="background:#10b981; color:#042114; font-weight:800;">📘 Solved Exercises ➔</a>
      <a href="javascript:window.print()">🖨️ Print Study Card</a>
    </nav>
  </div>
</header>
<main>
<section class="card teacher">
  <h2>🎯 Scientific Investigation &amp; Objectives</h2>
  <p>{e(theory_data.get('hook_en', 'Observe matter, test changes, and establish laws.'))}</p>
  <div class="arabic-explanation-box">
    <strong>الهدف والمقدمة: </strong>{e(theory_data.get('hook_ar', 'التعرف على خصائص المواد الصلبة والسوائل وتطبيقاتها العلمية.'))}
  </div>
  <div class="chips">
    {"".join(f"<span>{e(obj)}</span>" for obj in theory_data.get('objectives', ['Observe', 'Experiment', 'Conclude']))}
  </div>
</section>

<div id="learn">
  {activities_html}
</div>

<section id="lab" class="card">
  <h2>🧪 Live Lab · Tilt the Vessel &amp; Measure Surface</h2>
  <div class="lab">
    <p>Move the slider to tilt the container. The container walls rotate while the <b>free surface remains strictly horizontal</b> relative to gravity:</p>
    <label>Tilt angle: <b id="ang" style="color:var(--c-obs-bar);">0°</b>
      <input id="tilt" type="range" min="-35" max="35" value="0"/>
    </label>
    <div class="figure">
      <svg id="labSvg" viewBox="0 0 650 300">
        <g id="labV">
          <path d="M 180 50 L 180 240 L 440 240 L 440 50" fill="none" stroke="#8ce9ff" stroke-width="8"/>
        </g>
        <line class="water" x1="190" y1="150" x2="430" y2="150"/>
        <line x1="550" y1="40" x2="550" y2="230" stroke="var(--c-obs-bar)" stroke-width="3" stroke-dasharray="5 5"/>
        <circle cx="550" cy="245" r="14" fill="var(--c-obs-bar)"/>
        <text x="495" y="280" fill="var(--c-obs-bar)" font-size="14">Vertical reference</text>
      </svg>
    </div>
    <div id="labmsg" class="answer">At 0°, the vessel is upright and the free surface is horizontal.</div>
  </div>
</section>

<div class="cta-exercises-box">
  <h2 style="color:#6ee7b7; margin-bottom:8px;">📘 Ready to Practice &amp; Master the Concepts?</h2>
  <p>Access the complete, step-by-step textbook exercises &amp; problems workbook:</p>
  <a href="{e(exercises_filename)}" class="cta-exercises-btn">Open All Solved Textbook Exercises &amp; Problems ➔</a>
</div>

<section id="worksheet" class="card">
  <h2>📝 Interactive Graded Worksheet (Formative Assessment)</h2>
  {ws_html}
  <div style="margin-top:14px;">
    <button class="secondary" onclick="gradeWS()">Correct My Worksheet</button>
    <strong id="finalScore" style="margin-left:14px; font-size:1.2rem; color:var(--c-obs-bar);"></strong>
  </div>
</section>

<section class="card summary" id="printableCard">
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; border-bottom:2px solid var(--c-concl-bar); padding-bottom:10px; margin-bottom:14px;">
    <h2>💡 Master Reference Study Card · {e(title)} (Grade {canonical_entry['grade']})</h2>
    <span class="source">Official CRDP Curriculum</span>
  </div>
  <div class="sc-grid">
    {panels_html}
  </div>
</section>
</main>
<script>
document.addEventListener("DOMContentLoaded", function() {{
  if (typeof renderMathInElement !== 'undefined') {{
    renderMathInElement(document.body, {{delimiters: [{{left: '$$', right: '$$', display: true}}, {{left: '$', right: '$', display: false}}], throwOnError: false}});
  }}
}});
function toggleAr(id) {{
  const el = document.getElementById(id);
  el.style.display = (el.style.display === 'none' || el.style.display === '') ? 'block' : 'none';
}}
function fb(id, ok) {{
  const el = document.getElementById(id);
  el.textContent = ok ? '✓ Correct observation!' : '✗ Re-check textbook observation.';
  el.style.color = ok ? 'var(--c-concl-bar)' : 'var(--danger)';
}}
const tilt = document.getElementById('tilt');
const labV = document.getElementById('labV');
const labmsg = document.getElementById('labmsg');
const ang = document.getElementById('ang');
if (tilt && labV) {{
  tilt.addEventListener('input', () => {{
    const a = tilt.value;
    ang.textContent = a + '°';
    labV.setAttribute('transform', `rotate(${{a}} 310 145)`);
    labmsg.textContent = `The vessel is tilted ${{a}}°. The liquid surface remains strictly horizontal.`;
  }});
}}
const wsKeys = {json.dumps([q.get('correct_index', 0) for q in theory_data.get('worksheet', [])])};
function gradeWS() {{
  let score = 0;
  for (let i = 1; i <= wsKeys.length; i++) {{
    const sel = document.getElementById('wq' + i);
    const fbEl = document.getElementById('wfb' + i);
    if (sel && sel.value !== "") {{
      if (parseInt(sel.value) === wsKeys[i-1]) {{
        score++; fbEl.textContent = '✓ Correct'; fbEl.style.color = 'var(--c-concl-bar)';
      }} else {{
        fbEl.textContent = '✗ Review observation'; fbEl.style.color = 'var(--danger)';
      }}
    }}
  }}
  document.getElementById('finalScore').textContent = `Score: ${{score}} / ${{wsKeys.length}}`;
}}
</script>
</body>
</html>"""


def render_page_b_exercises(exercises_list, canonical_entry, theory_filename):
    e = html.escape
    title = canonical_entry["canonical_title"]
    lid = canonical_entry["lesson_id"]
    start_p = canonical_entry["pdf_start_page"]
    end_p = canonical_entry["pdf_end_page"]

    items_html = ""
    for ex in exercises_list:
        num = ex.get("number", 1)
        steps = "".join(f"<li>{s}</li>" for s in ex.get("steps_en", []))
        svg = ex.get("svg_diagram", "")
        fig_html = f'<div class="figure ex-figure">{svg}</div>' if svg and "<svg" in svg else ""
        nabil_oral = ex.get("nabil_oral_explanation_ar", "")

        items_html += f"""
        <article class="exercise" id="ex{num}" data-ex-number="{num}">
          <div class="exhead">
            <span>Problem #{num} — {e(ex.get('title', 'Textbook Exercise'))}</span>
            <span class="source">Textbook pp. {start_p}–{end_p}</span>
          </div>
          <div class="prompt">
            <b>Task Prompt:</b>
            <p>{e(ex.get('prompt_en', ''))}</p>
            {f'<div style="font-size:14px; color:#bae6fd; direction:rtl; text-align:right; margin-top:6px;"><b>ترجمة المسألة:</b> {e(ex.get("prompt_ar"))}</div>' if ex.get("prompt_ar") else ''}
          </div>
          {fig_html}
          <details open>
            <summary>Guided Step-by-Step Resolution (English)</summary>
            <ol>{steps}</ol>
            <div class="answer"><b>Final Answer / Conclusion:</b> {ex.get('final_answer', '')}</div>
          </details>

          <button class="btn-toggle-ar" onclick="toggleAr('nabil-oral-{num}')">🗣️ شرح الأستاذ نبيل الشفهي بالعربية</button>
          <div id="nabil-oral-{num}" class="nabil-oral-box" style="display:none;">
            <h4 style="color:#6ee7b7; margin-bottom:6px;">طريقة نبيل لتفكيك المسألة:</h4>
            <div style="white-space: pre-line;">{e(nabil_oral)}</div>
          </div>
        </article>"""

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<meta name="nabil-lesson-id" content="{e(lid)}-EXERCISES"/>
<title>NABIL AI | Solved Exercises Workbook | {e(title)}</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css"/>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>
<style>{get_shared_css()}</style>
</head>
<body>
<header>
  <div class="bar">
    <div>
      <b>📘 Official Solved Workbook · Grade {canonical_entry['grade']} Physics</b>
      <h1>{e(title)} — All Solved Problems</h1>
      <div class="source">Official CRDP Textbook Problem Set</div>
    </div>
    <nav>
      <a href="{e(theory_filename)}" style="background:#38bdf8; color:#061325; font-weight:800;">⬅️ Return to Lesson &amp; Lab</a>
      <a href="javascript:window.print()">🖨️ Print Workbook</a>
    </nav>
  </div>
</header>
<main>
<div class="card teacher">
  <h2>📘 Comprehensive Textbook Resolution</h2>
  <p>Every exercise and problem solved with step-by-step scientific justification, full diagrams, and NABIL's spoken Arabic analysis.</p>
</div>

<div id="exercisesContainer">
  {items_html}
</div>

<div style="text-align:center; margin:30px 0;">
  <a href="{e(theory_filename)}" class="nav-btn" style="font-size:1.1rem; padding:12px 24px;">⬅️ Return to Main Lesson and Interactive Lab</a>
</div>
</main>
<script>
document.addEventListener("DOMContentLoaded", function() {{
  if (typeof renderMathInElement !== 'undefined') {{
    renderMathInElement(document.body, {{delimiters: [{{left: '$$', right: '$$', display: true}}, {{left: '$', right: '$', display: false}}], throwOnError: false}});
  }}
}});
function toggleAr(id) {{
  const el = document.getElementById(id);
  el.style.display = (el.style.display === 'none' || el.style.display === '') ? 'block' : 'none';
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

    progress("STARTING_TWIN_PAGE_PRODUCTION", lesson_id=lesson_id, title=title, pages=f"{start_p}-{end_p}")

    with tempfile.TemporaryDirectory() as tmp:
        pdf_path = Path(tmp) / "book.pdf"
        download_pdf_to_path(service, book_id, pdf_path)
        from pypdf import PdfReader
        reader = PdfReader(str(pdf_path))

        pages = [(p, (reader.pages[p - 1].extract_text() or "").strip())
                 for p in range(start_p, end_p + 1)]

        full_text = "\n\n".join([f"=== Page {p} ===\n{t}" for p, t in pages])
        detected_exercises = discover_all_exercises_and_problems(full_text)
        progress("DISCOVERED_EXERCISE_ITEMS", total_found=len(detected_exercises), items=detected_exercises)

        prov = configured_providers()[0]
        from openai import OpenAI
        client = OpenAI(api_key=prov[1], base_url=prov[2], timeout=180)

        # 1. Solve all exercises with NABIL oral flow in safe batches
        solved_exercises = solve_all_exercises_with_nabil_method(client, prov[3], canonical_entry, pages, detected_exercises)
        if len(solved_exercises) == 0:
            raise AssertionError("QUALITY_GATE_FAILED: ZERO_EXERCISES_SOLVED")

        # 2. Generate Theory, Lab & Study Card with Bilingual support
        theory_package = generate_lesson_theory_package(client, prov[3], canonical_entry, pages)

        slug = re.sub(r"[^\w]+", "-", title.upper()).strip("-")
        num_str = lesson_id.split("-")[-1]
        grade_tag = f"G{canonical_entry['grade']:02d}"
        subj_tag = canonical_entry['subject'].upper()

        theory_filename = f"{grade_tag}-{subj_tag}--{num_str}--{slug}.html"
        exercises_filename = f"{grade_tag}-{subj_tag}--{num_str}--{slug}--EXERCISES.html"

        html_theory = render_page_a_theory(theory_package, canonical_entry, exercises_filename)
        html_exercises = render_page_b_exercises(solved_exercises, canonical_entry, theory_filename)

        out_theory_path = report_path.with_name(theory_filename)
        out_ex_path = report_path.with_name(exercises_filename)

        out_theory_path.write_text(html_theory, encoding="utf-8")
        out_ex_path.write_text(html_exercises, encoding="utf-8")

        progress("TWIN_PAGES_COMPILED_LOCALLY", theory_file=theory_filename, exercises_file=exercises_filename)

        report = {
            "status": "VERIFIED_COMPLETE",
            "lesson_id": lesson_id,
            "title": title,
            "theory_filename": theory_filename,
            "exercises_filename": exercises_filename,
            "exercises_count": len(solved_exercises)
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

            media_a = MediaIoBaseUpload(io.BytesIO(html_theory.encode("utf-8")), mimetype="text/html", resumable=False)
            up_a = service.files().create(body={"name": theory_filename, "parents": [s_id]}, media_body=media_a, fields="id").execute()
            report["drive_theory_id"] = up_a["id"]

            media_b = MediaIoBaseUpload(io.BytesIO(html_exercises.encode("utf-8")), mimetype="text/html", resumable=False)
            up_b = service.files().create(body={"name": exercises_filename, "parents": [s_id]}, media_body=media_b, fields="id").execute()
            report["drive_exercises_id"] = up_b["id"]

            progress("PUBLISHED_TWIN_PAGES_TO_DRIVE", theory_id=up_a["id"], exercises_id=up_b["id"])

        return report


def main():
    parser = argparse.ArgumentParser(description="NABIL AI Twin-Engine Lesson Factory")
    parser.add_argument("--report", default="data/nabil_lesson_factory_run.json")
    parser.add_argument("--lesson-id", default="G07-PHYSICS-001")
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()

    global PROGRESS_STARTED
    PROGRESS_STARTED = time.monotonic()

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
        print("[ERROR] Lesson entry not found:", args.lesson_id)
        return 1

    rep = produce_lesson_for_entry(service, target_entry, report_path, publish=args.publish)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(rep, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(rep, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
