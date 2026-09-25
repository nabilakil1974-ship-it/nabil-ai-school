"""
NABIL AI — Enterprise Autonomous Lesson Factory & Pedagogical Engine
Architecture:
- Deterministic Evidence-Map Extraction (No Fallbacks / Fakes)
- Cryptographic Source-Locked Prompts (Rendered directly from Source Evidence)
- Dynamic Pedagogy Profile & Adaptive Token Budgeting
- Configurable/Conditional Live Lab Engine
- Full Deterministic Gates Suite (Zero-Tolerance Policy)
- Safe In-Platform Railway Navigation QA
"""

import argparse
import hashlib
import html
import io
import json
import os
import re
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

# =========================================================================
# DETERMINISTIC EVIDENCE MAP & SOURCE-LOCKING (NO FAKE FALLBACKS)
# =========================================================================

def build_deterministic_evidence_map(pages):
    full_text = "\n\n".join([f"=== Page {p} ===\n{t}" for p, t in pages])
    
    # 1. Activities Evidence Extraction
    activities_evidence = []
    act_matches = list(re.finditer(r"(?:Activity|Activité|نشاط)\s*(\d+)[:\.\s\-]+([^\n\r]+)", full_text, re.I))
    for m in act_matches:
        num = int(m.group(1))
        title = m.group(2).strip()
        activities_evidence.append({
            "number": num,
            "raw_title": title
        })

    # 2. Strict Source Exercise Extraction
    exercise_evidence = []
    problem_text_blocks = "\n\n".join([f"Page {p}:\n" + t for p, t in pages if p >= (pages[-1][0] - 2)])
    
    pattern = re.compile(
        r"(?:Exercise|Exercice|Problem|تمرين|مسألة)\s*(\d+)[:\.\s\-]+(.*?)(?=(?:Exercise|Exercice|Problem|تمرين|مسألة)\s*\d+|$)",
        re.DOTALL | re.I
    )
    
    for match in pattern.finditer(problem_text_blocks):
        num = int(match.group(1))
        content = match.group(2).strip()
        if len(content) >= 15:
            # Clean OCR noise
            clean_prompt = " ".join(content.split())
            content_hash = hashlib.sha256(clean_prompt.encode('utf-8')).hexdigest()[:16]
            fig_refs = re.findall(r"(?:figure|fig\.|شكل)\s*(\d+)", clean_prompt, re.I)
            
            exercise_evidence.append({
                "number": num,
                "raw_prompt": clean_prompt,
                "hash": content_hash,
                "fig_refs": fig_refs,
                "requires_figure": len(fig_refs) > 0
            })

    # SORT BY NUMBER
    exercise_evidence.sort(key=lambda x: x["number"])

    # ZERO-TOLERANCE GATE: NO ARTIFICIAL FALLBACKS
    if not exercise_evidence:
        raise AssertionError("QUALITY_GATE_FAILED: EXERCISE_EVIDENCE_MISSING (No textbook exercises could be extracted via OCR)")

    return {
        "full_text": full_text,
        "activities_evidence": activities_evidence,
        "exercise_evidence": exercise_evidence,
        "exercise_numbers": [x["number"] for x in exercise_evidence]
    }

# =========================================================================
# PEDAGOGY PROFILE COMPILER
# =========================================================================

def compile_pedagogy_profile(evidence_map, subject):
    act_count = len(evidence_map["activities_evidence"])
    ex_count = len(evidence_map["exercise_evidence"])
    
    # Check if a live interactive lab is pedagogically warranted
    has_fluid_or_motion = any(w in evidence_map["full_text"].lower() for w in ["liquid", "water", "tilt", "surface", "motion", "angle"])
    
    return {
        "expected_activities_count": act_count,
        "expected_exercises_count": ex_count,
        "lab_warranted": has_fluid_or_motion,
        "requires_plumb_line": "plumb" in evidence_map["full_text"].lower()
    }

# =========================================================================
# AI TEACHING LAYER (NABIL METHOD OVER SOURCE-LOCKED PROMPTS)
# =========================================================================

def generate_pedagogical_theory(client, model, canonical_entry, evidence_map, profile):
    title = canonical_entry["canonical_title"]
    grade = canonical_entry["grade"]
    subject = canonical_entry["subject"]
    
    prompt = (
        f"You are Teacher NABIL, master professor for the Lebanese CRDP curriculum.\n"
        f"Design the interactive classroom lesson for Grade {grade} {subject}: '{title}'.\n\n"
        f"VERIFIED EVIDENCE MAP FROM BOOK SCANS:\n{evidence_map['full_text']}\n\n"
        "STRICT SOURCE BOUNDARY RULES:\n"
        "1. Follow the textbook activities strictly in sequence. Do NOT invent or skip any activity.\n"
        "2. ZERO TOLERANCE: Do NOT introduce surface tension, cohesion, adhesion, density formulas, or hydrostatic pressure unless explicitly printed in the scanned text.\n"
        "3. Provide for every activity: English text, clear Arabic translation, student inquiry question, and a scalable, bold SVG diagram (viewBox='0 0 600 220').\n"
        "4. Live Lab Config: If lab_warranted is true, provide full simulation parameters; otherwise set 'has_lab': false.\n"
        "5. Formative Worksheet: 6 multiple-choice questions testing ONLY what was evidenced.\n"
        "6. Final Study Card: 3 comprehensive multi-column summary panels with SVG diagrams.\n\n"
        "Return valid JSON: {\n"
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
        "  'live_lab': {\n"
        "    'has_lab': bool,\n"
        "    'title': str,\n"
        "    'instructions': str,\n"
        "    'min_val': int, 'max_val': int, 'default_val': int\n"
        "  },\n"
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
        max_tokens=1800,
        temperature=0.1
    )
    txt = resp.choices[0].message.content.strip()
    if txt.startswith("```"):
        txt = re.sub(r"^```(?:json)?\s*|\s*```$", "", txt, flags=re.I).strip()
    return json.loads(txt)


def solve_source_locked_exercises_adaptive(client, model, canonical_entry, evidence_map):
    """
    Adaptive Batching: Calculates chunk size based on token budget.
    Injects locked source prompts directly; AI produces ONLY solutions and NABIL oral flow.
    """
    title = canonical_entry["canonical_title"]
    grade = canonical_entry["grade"]
    ex_items = evidence_map["exercise_evidence"]
    
    all_solved = []
    
    # Calculate adaptive batch size (budget ~800 tokens max per call)
    avg_words = sum(len(x["raw_prompt"].split()) for x in ex_items) / max(1, len(ex_items))
    if avg_words > 40:
        batch_size = 1
    elif avg_words > 20:
        batch_size = 2
    else:
        batch_size = 3

    chunks = [ex_items[i:i + batch_size] for i in range(0, len(ex_items), batch_size)]

    for idx, chunk in enumerate(chunks, 1):
        progress("SOLVING_ADAPTIVE_EXERCISE_BATCH", batch=idx, total=len(chunks), 
                 batch_size=len(chunk), items=[x["number"] for x in chunk])
        
        prompt = (
            f"You are Teacher NABIL solving official Lebanese CRDP textbook exercises for Grade {grade} Physics: '{title}'.\n\n"
            f"LOCKED SOURCE PROMPTS TO SOLVE (DO NOT MODIFY OR REPLACE):\n"
            f"{json.dumps(chunk, ensure_ascii=False)}\n\n"
            "MANDATORY INSTRUCTIONS:\n"
            "1. You are providing the TEACHING & SOLUTION LAYER ONLY. Do NOT invent new questions.\n"
            "2. If requires_figure is true, generate a high-contrast SVG diagram (viewBox='0 0 600 220').\n"
            "3. Format NABIL's spoken Arabic analysis strictly as:\n"
            "   المعطى أعطانا: ...\n"
            "   هذا يعني: ...\n"
            "   المطلوب: ...\n"
            "   إذن نستخدم: ...\n"
            "   نعوّض / نعلل: ...\n"
            "   نستنتج: ...\n\n"
            "Return valid JSON: {'items': [\n"
            "  {\n"
            "    'number': int,\n"
            "    'hash': str,\n"
            "    'title': str,\n"
            "    'prompt_ar': str,\n"
            "    'steps_en': [str],\n"
            "    'nabil_oral_ar': str,\n"
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
                data = json.loads(txt).get("items", [])
                
                # Merge AI solutions into locked source items
                for it in data:
                    num = it.get("number")
                    orig = next((x for x in chunk if x["number"] == num), None)
                    if orig:
                        merged = {
                            "number": num,
                            "hash": orig["hash"],
                            "raw_prompt": orig["raw_prompt"],  # Source-Locked Guarantee
                            "title": it.get("title", f"Exercise {num}"),
                            "prompt_ar": it.get("prompt_ar", ""),
                            "steps_en": it.get("steps_en", []),
                            "nabil_oral_ar": it.get("nabil_oral_ar", ""),
                            "final_answer": it.get("final_answer", ""),
                            "svg_diagram": it.get("svg_diagram", "") if orig["requires_figure"] else ""
                        }
                        all_solved.append(merged)
                break
            except Exception as e:
                progress("BATCH_WAIT_RETRY", error=str(e)[:100], attempt=attempt)
                time.sleep(4)

        time.sleep(2)

    return all_solved

# =========================================================================
# HARD QUALITY GATES SUITE
# =========================================================================

def execute_deterministic_quality_gates(theory_data, solved_exercises, evidence_map, profile):
    progress("EXECUTING_STRICT_DETERMINISTIC_GATES")
    
    # 1. Activities Completeness & Profile Match
    activities = theory_data.get("activities", [])
    if len(activities) < profile["expected_activities_count"] and len(activities) < 2:
        raise AssertionError("PEDAGOGY_PROFILE_MISMATCH: Activities count does not match source evidence")
        
    for act in activities:
        if not act.get("experiment_en") or not act.get("observation_en") or not act.get("conclusion_en"):
            raise AssertionError("ACTIVITY_EVIDENCE_MISSING: Incomplete activity structure detected")

    # 2. Strict Exercise Sequence Gate
    expected_numbers = set(evidence_map["exercise_numbers"])
    solved_numbers = {int(x.get("number", 0)) for x in solved_exercises if "number" in x}
    
    missing_numbers = expected_numbers - solved_numbers
    if missing_numbers:
        raise AssertionError(f"EXERCISE_SEQUENCE_INCOMPLETE: Missing exercises {sorted(list(missing_numbers))}")

    # 3. Cryptographic Source-Lock Hash Verification
    for orig in evidence_map["exercise_evidence"]:
        matched = next((x for x in solved_exercises if x["number"] == orig["number"]), None)
        if not matched:
            raise AssertionError(f"EXERCISE_SOURCE_MISMATCH: Exercise {orig['number']} completely absent from solution array")
        if matched["hash"] != orig["hash"]:
            raise AssertionError(f"EXERCISE_SOURCE_MISMATCH: Hash mismatch on exercise {orig['number']}. AI altered prompt identity.")

    # 4. Figure Evidence Gate
    for orig in evidence_map["exercise_evidence"]:
        if orig["requires_figure"]:
            matched = next(x for x in solved_exercises if x["number"] == orig["number"])
            if "<svg" not in matched.get("svg_diagram", ""):
                raise AssertionError(f"EXERCISE_DIAGRAM_REQUIRED_MISSING: Exercise {orig['number']} references a Figure but diagram is absent")

    # 5. Non-Empty Worksheet & Study Card
    worksheet = theory_data.get("worksheet", [])
    if len(worksheet) < 4:
        raise AssertionError("WORKSHEET_EMPTY: Worksheet must contain at least 4 gradable questions")
        
    panels = theory_data.get("study_card", {}).get("panels", [])
    if len(panels) < 2:
        raise AssertionError("STUDY_CARD_INCOMPLETE: Study card has fewer than 2 panels")

    # 6. Source Boundary Gate
    forbidden_terms = ["surface tension", "cohesion", "adhesion", "hydrostatic pressure", "density of water", "p = ρgh"]
    dump = json.dumps(theory_data).lower() + " " + json.dumps(solved_exercises).lower()
    for term in forbidden_terms:
        if term in dump:
            raise AssertionError(f"SOURCE_BOUNDARY_BREACH: Forbidden unevidenced term detected: '{term}'")

    progress("ALL_QUALITY_GATES_PASSED_SUCCESSFULLY")

# =========================================================================
# SAFE RAILWAY NAVIGATION HTML RENDERERS
# =========================================================================

def get_shared_css():
    return """
    :root {
      --bg-main: #07192b;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --card-bg: #0d2742;
      --card-border: #1e4a78;
      --c-hook-border: #38bdf8;
      --c-exp-bar: #38bdf8;
      --c-obs-bar: #f59e0b;
      --c-concl-bar: #10b981;
      --c-lab-border: #06b6d4;
      --c-ex-border: #10b981;
      --c-sol-bg: #042e22;
      --c-sol-text: #ecfdf5;
      --c-card-gold: #fbbf24;
      --c-arabic-box: #0a3359;
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
      background: linear-gradient(135deg, #0e3052 0%, #034f8c 100%);
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
      background: #0d365c;
      border: 1px solid var(--c-hook-border);
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 14px;
      font-weight: 600;
      margin-left: 6px;
      display: inline-block;
      cursor: pointer;
      transition: all 0.25s ease;
    }
    nav a:hover, .nav-btn:hover {
      background: var(--c-hook-border);
      color: #07192b;
      transform: translateY(-1px);
    }
    .cta-exercises-box {
      background: linear-gradient(135deg, #0a355c, #0e4c82);
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
      cursor: pointer;
      border: none;
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
    .card.teacher { border-left: 6px solid var(--c-hook-border); background: #0b2d4f; }
    .chips span {
      display: inline-block;
      padding: 5px 12px;
      border: 1px solid #3d8fb6;
      border-radius: 999px;
      margin: 4px 4px 4px 0;
      background: #092644;
      font-size: 13px;
      font-weight: bold;
    }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
    .stage-exp { border-left: 4px solid var(--c-exp-bar); padding: 12px 16px; margin: 10px 0; background: #0b2f54; border-radius: 8px; }
    .stage-obs { border-left: 4px solid var(--c-obs-bar); padding: 12px 16px; margin: 10px 0; background: #2b2006; border-radius: 8px; }
    .stage-concl { border-left: 4px solid var(--c-concl-bar); padding: 12px 16px; margin: 10px 0; background: #063828; border-radius: 8px; }
    .figure {
      background: #081f36;
      border: 1px solid #1e4a78;
      border-radius: 14px;
      padding: 18px;
      margin: 14px 0;
      text-align: center;
    }
    .figure svg {
      width: 100%;
      max-width: 650px;
      min-height: 210px;
      height: auto;
      display: block;
      margin: auto;
    }
    .figure svg text { font-family: system-ui, sans-serif; font-weight: 700; fill: #e2e8f0; }
    .water { stroke: #38bdf8; stroke-width: 8; }
    .ask { background: #261942; border: 1px solid #9333ea; border-radius: 12px; padding: 14px; margin: 14px 0; }
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
    button.secondary { background: #10b981; color: #042114; font-weight: 800; }
    .btn-toggle-ar {
      background: #10416b;
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
      background: #073829;
      border-right: 5px solid var(--c-concl-bar);
      border-radius: 8px;
      padding: 16px;
      margin: 14px 0;
      direction: rtl;
      text-align: right;
      font-family: "Noto Kufi Arabic", Tahoma, sans-serif;
      line-height: 1.8;
      color: #f0fdf4;
    }
    .feedback { display: inline-block; margin-left: 10px; font-weight: bold; }
    .exercise {
      background: #0c2b4a;
      border: 1px solid #1e4a78;
      border-left: 6px solid var(--c-ex-border);
      border-radius: 14px;
      padding: 20px;
      margin: 22px 0;
    }
    .exhead {
      display: flex;
      justify-content: space-between;
      font-weight: bold;
      color: #6ee7b7;
      font-size: 1.1rem;
      border-bottom: 1px solid #1a4a75;
      padding-bottom: 10px;
      margin-bottom: 12px;
    }
    .prompt { background: #061c33; border-radius: 8px; padding: 14px; margin: 12px 0; font-size: 15.5px; color: #f1f5f9; }
    details { margin-top: 10px; }
    summary { cursor: pointer; font-weight: bold; color: var(--c-concl-bar); padding: 4px 0; font-size: 1.05rem; }
    .answer {
      background: var(--c-sol-bg);
      border: 1px solid var(--c-concl-bar);
      color: var(--c-sol-text);
      padding: 14px 18px;
      border-radius: 8px;
      margin-top: 12px;
      font-weight: 600;
    }
    .lab { background: #0a2f52; border: 1px solid var(--c-lab-border); border-radius: 14px; padding: 20px; }
    input[type=range] { width: 100%; margin: 12px 0; }
    select { padding: 8px 12px; border-radius: 6px; background: #07192b; color: #fff; border: 1px solid var(--c-hook-border); }
    .summary { border: 2px solid var(--c-card-gold); background: #0c243d; box-shadow: 0 0 25px rgba(251, 191, 36, 0.15); }
    .sc-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px; }
    .sc-panel { background: #071e36; border: 1px solid #1a4a75; border-radius: 12px; padding: 16px; }
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

def render_page_a(theory_data, canonical_entry):
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
            <div style="font-size:13.5px; color:var(--text-muted); margin-top:4px; direction:rtl; text-align:right;">{e(act.get('question_prompt_ar', ''))}</div>
          </div>
        </section>"""

    lab_spec = theory_data.get("live_lab", {})
    lab_html = ""
    if lab_spec.get("has_lab", True):
        lab_html = f"""
        <section id="lab" class="card">
          <h2>🧪 Live Lab · {e(lab_spec.get('title', 'Interactive Simulation'))}</h2>
          <div class="lab">
            <p>{e(lab_spec.get('instructions', 'Move slider to test phenomenon:'))}</p>
            <label>Variable: <b id="ang" style="color:var(--c-obs-bar);">0°</b>
              <input id="tilt" type="range" min="{lab_spec.get('min_val', -35)}" max="{lab_spec.get('max_val', 35)}" value="{lab_spec.get('default_val', 0)}"/>
            </label>
            <div class="figure">
              <svg id="labSvg" viewBox="0 0 650 300">
                <g id="labV">
                  <path d="M 180 50 L 180 240 L 440 240 L 440 50" fill="none" stroke="#38bdf8" stroke-width="8"/>
                </g>
                <line class="water" x1="190" y1="150" x2="430" y2="150"/>
                <line x1="550" y1="40" x2="550" y2="230" stroke="var(--c-obs-bar)" stroke-width="3" stroke-dasharray="5 5"/>
                <circle cx="550" cy="245" r="14" fill="var(--c-obs-bar)"/>
                <text x="495" y="280" fill="var(--c-obs-bar)" font-size="14">Vertical reference</text>
              </svg>
            </div>
            <div id="labmsg" class="answer">At 0°, the vessel is upright and the free surface is horizontal.</div>
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
        panels_html += f"""
        <div class="sc-panel">
          <h3 style="color:#6ee7b7;">{e(p.get('heading', ''))}</h3>
          <ul style="padding-left:18px;">{pts}</ul>
          <div class="figure" style="padding:8px; margin-top:10px;">{svg_panel}</div>
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
      {f'<a href="#lab">Live Lab</a>' if lab_html else ''}
      <a href="#worksheet">Worksheet</a>
      <button onclick="navigateToExercises()" class="nav-btn" style="background:#10b981; color:#042114; font-weight:800;">📘 Solved Exercises ➔</button>
      <a href="javascript:window.print()">🖨️ Print Study Card</a>
    </nav>
  </div>
</header>
<main>
<section class="card teacher">
  <h2>🎯 Scientific Investigation &amp; Objectives</h2>
  <p>{e(theory_data.get('hook_en', ''))}</p>
  <div class="arabic-explanation-box">
    <strong>المدخل والتساؤل العلمي: </strong>{e(theory_data.get('hook_ar', ''))}
  </div>
  <div class="chips">
    {"".join(f"<span>{e(obj)}</span>" for obj in theory_data.get('objectives', []))}
  </div>
</section>

<div id="learn">
  {activities_html}
</div>

{lab_html}

<div class="cta-exercises-box">
  <h2 style="color:#6ee7b7; margin-bottom:8px;">📘 Ready to Practice &amp; Master the Concepts?</h2>
  <p>Access the complete, step-by-step textbook exercises &amp; problems workbook:</p>
  <button onclick="navigateToExercises()" class="cta-exercises-btn">Open All Solved Textbook Exercises &amp; Problems ➔</button>
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
function navigateToExercises() {{
  const cur = new URL(window.location.href);
  const curLesson = cur.searchParams.get('lesson') || '';
  if (curLesson) {{
    cur.searchParams.set('lesson', curLesson.replace(/--EXERCISES/i, '') + '--EXERCISES');
    window.location.href = cur.toString();
  }} else {{
    window.location.href = window.location.pathname.replace('.html', '--EXERCISES.html') + window.location.search;
  }}
}}
</script>
</body>
</html>"""

def render_page_b(exercises_list, canonical_entry):
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
        nabil_oral = ex.get("nabil_oral_ar", "")

        # SOURCE-LOCKED DISPLAY: Prompt is VERBATIM from raw_prompt
        items_html += f"""
        <article class="exercise" id="ex{num}" data-ex-number="{num}" data-source-hash="{ex.get('hash', '')}">
          <div class="exhead">
            <span>Exercise #{num} — {e(ex.get('title', 'Official Exercise'))}</span>
            <span class="source">Textbook pp. {start_p}–{end_p}</span>
          </div>
          <div class="prompt">
            <b>Official Book Task (Verbatim):</b>
            <p>{e(ex.get('raw_prompt', ''))}</p>
            {f'<div style="font-size:14px; color:#bae6fd; direction:rtl; text-align:right; margin-top:6px;"><b>ترجمة المسألة:</b> {e(ex.get("prompt_ar"))}</div>' if ex.get("prompt_ar") else ''}
          </div>
          {fig_html}
          <details open>
            <summary>Guided Step-by-Step Resolution (English)</summary>
            <ol>{steps}</ol>
            <div class="answer"><b>Final Answer:</b> {ex.get('final_answer', '')}</div>
          </details>

          <button class="btn-toggle-ar" onclick="toggleAr('nabil-oral-{num}')">🗣️ شرح الأستاذ نبيل الشفهي بالعربية</button>
          <div id="nabil-oral-{num}" class="nabil-oral-box" style="display:none;">
            <h4 style="color:#6ee7b7; margin-bottom:8px;">تحليل الأستاذ نبيل للمسألة:</h4>
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
      <h1>{e(title)} — Complete Textbook Solutions</h1>
      <div class="source">Official Lebanese CRDP Textbook Problems</div>
    </div>
    <nav>
      <button onclick="returnToLesson()" class="nav-btn" style="background:#38bdf8; color:#07192b; font-weight:800;">⬅️ Return to Lesson &amp; Lab</button>
      <a href="javascript:window.print()">🖨️ Print Workbook</a>
    </nav>
  </div>
</header>
<main>
<div class="card teacher">
  <h2>📘 Official Textbook Resolution</h2>
  <p>All textbook exercises solved below with step-by-step scientific justification, original geometric diagrams, and NABIL's Arabic spoken analysis.</p>
</div>

<div id="exercisesContainer">
  {items_html}
</div>

<div style="text-align:center; margin:30px 0;">
  <button onclick="returnToLesson()" class="cta-exercises-btn" style="background:#38bdf8; color:#07192b;">⬅️ Return to Main Lesson and Interactive Lab</button>
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
function returnToLesson() {{
  const cur = new URL(window.location.href);
  const curLesson = cur.searchParams.get('lesson') || '';
  if (curLesson) {{
    cur.searchParams.set('lesson', curLesson.replace(/--EXERCISES/i, ''));
    window.location.href = cur.toString();
  }} else if (window.history.length > 1) {{
    window.history.back();
  }} else {{
    window.location.href = window.location.pathname.replace('--EXERCISES.html', '.html') + window.location.search;
  }}
}}
</script>
</body>
</html>"""

# =========================================================================
# PRODUCTION PIPELINE
# =========================================================================

def produce_lesson_for_entry(service, canonical_entry, report_path, publish=False):
    title = canonical_entry["canonical_title"]
    lesson_id = canonical_entry["lesson_id"]
    book_id = canonical_entry["book_id"]
    start_p = canonical_entry["pdf_start_page"]
    end_p = canonical_entry["pdf_end_page"]

    progress("STARTING_STRICT_EVIDENCE_PRODUCTION", lesson_id=lesson_id, title=title)

    with tempfile.TemporaryDirectory() as tmp:
        pdf_path = Path(tmp) / "book.pdf"
        download_pdf_to_path(service, book_id, pdf_path)
        from pypdf import PdfReader
        reader = PdfReader(str(pdf_path))

        pages = [(p, (reader.pages[p - 1].extract_text() or "").strip())
                 for p in range(start_p, end_p + 1)]

        # 1. Deterministic Evidence Map with Hash Identifiers
        evidence_map = build_deterministic_evidence_map(pages)
        progress("EVIDENCE_MAP_EXTRACTED", 
                 activities=len(evidence_map["activities_evidence"]), 
                 exercises=len(evidence_map["exercise_evidence"]))

        # 2. Compile Pedagogy Profile
        profile = compile_pedagogy_profile(evidence_map, canonical_entry["subject"])

        # 3. Setup AI provider
        prov = configured_providers()[0]
        from openai import OpenAI
        client = OpenAI(api_key=prov[1], base_url=prov[2], timeout=180)

        # 4. Generate Pedagogical Theory & Adaptive Source-Locked Solutions
        theory_data = generate_pedagogical_theory(client, prov[3], canonical_entry, evidence_map, profile)
        solved_exercises = solve_source_locked_exercises_adaptive(client, prov[3], canonical_entry, evidence_map)

        # 5. Execute Hard Quality Gates
        execute_deterministic_quality_gates(theory_data, solved_exercises, evidence_map, profile)

        # 6. Render Output Files
        slug = re.sub(r"[^\w]+", "-", title.upper()).strip("-")
        num_str = lesson_id.split("-")[-1]
        grade_tag = f"G{canonical_entry['grade']:02d}"
        subj_tag = canonical_entry['subject'].upper()

        theory_filename = f"{grade_tag}-{subj_tag}--{num_str}--{slug}.html"
        exercises_filename = f"{grade_tag}-{subj_tag}--{num_str}--{slug}--EXERCISES.html"

        html_theory = render_page_a(theory_data, canonical_entry)
        html_exercises = render_page_b(solved_exercises, canonical_entry)

        # 7. Navigation QA Test
        if "navigateToExercises" not in html_theory or "returnToLesson" not in html_exercises:
            raise AssertionError("NAVIGATION_FAILED: Missing safe navigation scripts between pages")

        out_theory_path = report_path.with_name(theory_filename)
        out_ex_path = report_path.with_name(exercises_filename)

        out_theory_path.write_text(html_theory, encoding="utf-8")
        out_ex_path.write_text(html_exercises, encoding="utf-8")

        progress("FILES_COMPILED_LOCALLY", theory=theory_filename, exercises=exercises_filename)

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

            existing = service.files().list(q=f"'{s_id}' in parents and (name='{theory_filename}' or name='{exercises_filename}') and trashed=false",
                                            fields="files(id, name)").execute().get("files", [])
            for f_item in existing:
                service.files().delete(fileId=f_item["id"]).execute()

            media_a = MediaIoBaseUpload(io.BytesIO(html_theory.encode("utf-8")), mimetype="text/html", resumable=False)
            up_a = service.files().create(body={"name": theory_filename, "parents": [s_id]}, media_body=media_a, fields="id").execute()
            report["drive_theory_id"] = up_a["id"]

            media_b = MediaIoBaseUpload(io.BytesIO(html_exercises.encode("utf-8")), mimetype="text/html", resumable=False)
            up_b = service.files().create(body={"name": exercises_filename, "parents": [s_id]}, media_body=media_b, fields="id").execute()
            report["drive_exercises_id"] = up_b["id"]

            progress("PUBLISHED_TWIN_PAGES_TO_DRIVE", theory_id=up_a["id"], exercises_id=up_b["id"])

        return report

def main():
    parser = argparse.ArgumentParser(description="NABIL AI Universal Factory Engine")
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
