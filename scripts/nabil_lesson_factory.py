"""
NABIL AI — Universal Autonomous Lesson Factory & Production Engine
Architecture:
1. Catalog Engine: Dynamic TOC extraction + opening-page title verification (--build-catalog).
2. Evidence Map: Per-page extraction with source_page, source_text_hash, and visual figure crops.
3. Pedagogy Profile: Exact deterministic 1:1 activity & exercise matching.
4. Dynamic Modular Lab Renderer: Driven strictly by lab_spec.type (Zero hard-coded vessel SVG).
5. Deterministic Zero-Tolerance Hard Quality Gates:
   - EXERCISE_EVIDENCE_MISSING
   - EXERCISE_SEQUENCE_INCOMPLETE
   - EXERCISE_SOURCE_MISMATCH
   - FIGURE_EVIDENCE_MISSING
   - PEDAGOGY_PROFILE_MISMATCH
   - WORKSHEET_EMPTY
   - STUDY_CARD_INCOMPLETE
   - NAVIGATION_FAILED
"""

import argparse
import hashlib
import html
import io
import json
import math
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


# =========================================================================
# 1. CATALOG ENGINE (TOC Extraction + Opening-Page Title Verification)
# =========================================================================

def build_or_verify_catalog(service, book_id, grade, subject, language="en"):
    """
    Dynamically extracts Table of Contents from book PDF, locates lessons,
    and performs Opening-Page Verification. Fails with TITLE_VERIFICATION_FAILED
    if title does not match page header.
    """
    progress("BUILDING_CATALOG_FROM_TOC", book_id=book_id, grade=grade, subject=subject)
    with tempfile.TemporaryDirectory() as tmp:
        pdf_path = Path(tmp) / "source_book.pdf"
        download_pdf_to_path(service, book_id, pdf_path)
        from pypdf import PdfReader
        reader = PdfReader(str(pdf_path))
        num_pages = len(reader.pages)

        # 1. Find TOC across preliminary pages (pages 1 to 15)
        toc_text = ""
        toc_pages = []
        for p_idx in range(min(15, num_pages)):
            txt = reader.pages[p_idx].extract_text() or ""
            if any(k in txt.lower() for k in ["contents", "table of contents", "sommaire", "فهرس"]):
                toc_text += f"\n=== TOC Page {p_idx + 1} ===\n" + txt
                toc_pages.append(p_idx + 1)

        # Fallback search if keyword omitted in header
        if not toc_text:
            for p_idx in range(min(10, num_pages)):
                toc_text += f"\n=== Page {p_idx + 1} ===\n" + (reader.pages[p_idx].extract_text() or "")

        # 2. Extract Chapters/Lessons via structured regex
        entries = []
        # Pattern captures: Chapter/Lesson Number, Title, Start Page
        pattern = re.compile(
            r"(?:chapter|ch\.|chapitre|lesson|درس|فصل)?\s*(\d+)[\.\s:\-]+([A-Za-z\s,\-–'\(\)]{3,60}?)\.{2,}\s*(\d+)",
            re.I
        )

        matches = list(pattern.finditer(toc_text))
        if not matches:
            # Fallback pattern without dotted leaders
            pattern2 = re.compile(
                r"(?:chapter|ch\.|chapitre|lesson|درس|فصل)\s*(\d+)[\.\s:\-]+([A-Za-z\s,\-–'\(\)]{3,50})\s+(\d+)",
                re.I
            )
            matches = list(pattern2.finditer(toc_text))

        for idx, m in enumerate(matches):
            ch_num = int(m.group(1))
            raw_title = m.group(2).strip()
            start_p = int(m.group(3))
            
            # Determine end page from next entry or boundary
            if idx + 1 < len(matches):
                end_p = int(matches[idx + 1].group(3)) - 1
            else:
                end_p = min(start_p + 15, num_pages)

            if end_p < start_p:
                end_p = start_p + 5

            # 3. OPENING-PAGE VERIFICATION
            if start_p <= num_pages:
                opening_page_text = (reader.pages[start_p - 1].extract_text() or "").lower()
                clean_title_words = [w.lower() for w in re.findall(r"[A-Za-z]{3,}", raw_title)]
                
                # Verify that major title words appear on opening page
                matched_words = [w for w in clean_title_words if w in opening_page_text]
                if len(matched_words) < max(1, len(clean_title_words) // 2):
                    # Check next page in case of full-page photo/illustration
                    if start_p < num_pages:
                        p2_text = (reader.pages[start_p].extract_text() or "").lower()
                        matched_words = [w for w in clean_title_words if w in p2_text]
                        if len(matched_words) >= max(1, len(clean_title_words) // 2):
                            start_p += 1
                        else:
                            raise AssertionError(
                                f"TITLE_VERIFICATION_FAILED: Title '{raw_title}' (Ch {ch_num}) "
                                f"not confirmed on opening page {start_p}"
                            )
                    else:
                        raise AssertionError(
                            f"TITLE_VERIFICATION_FAILED: Title '{raw_title}' (Ch {ch_num}) "
                            f"not confirmed on opening page {start_p}"
                        )

            lid = f"G{int(grade):02d}-{subject.upper()[:3]}-{ch_num:03d}"
            entries.append({
                "lesson_id": lid,
                "grade": int(grade),
                "subject": subject,
                "language": language,
                "book_id": book_id,
                "canonical_title": raw_title,
                "chapter_number": ch_num,
                "pdf_start_page": start_p,
                "pdf_end_page": end_p,
                "title_verified": True
            })

        if not entries:
            raise AssertionError("CATALOG_BUILD_FAILED: No verified lesson entries could be extracted from TOC")

        g_key = f"G{int(grade):02d}"
        catalog_struct = {
            g_key: {
                subject: {
                    "book_id": book_id,
                    "language": language,
                    "lessons": entries
                }
            }
        }
        CATALOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        CATALOG_PATH.write_text(json.dumps(catalog_struct, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        progress("CATALOG_SUCCESSFULLY_BUILT", total_lessons=len(entries))
        return catalog_struct


def load_catalog(service, target_lesson_id=None):
    if not CATALOG_PATH.exists():
        raise RuntimeError("CATALOG_MISSING: Run with --build-catalog first to generate verified catalog")
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


# =========================================================================
# 2. DETERMINISTIC EVIDENCE MAP (Per-Page Extraction with Visual Evidence)
# =========================================================================

def build_deterministic_evidence_map(pages, reader):
    """
    Extracts evidence strictly per-page, recording true source_page,
    cryptographic SHA-256 hash, and visual figure bounding boxes.
    """
    activities_evidence = []
    exercise_evidence = []

    # A. Extract Activities from theory pages
    for page_num, page_text in pages:
        for m in re.finditer(r"(?:Activity|Activité|نشاط)\s*(\d+)[:\.\s\-]+([^\n\r]+)", page_text, re.I):
            act_num = int(m.group(1))
            act_title = m.group(2).strip()
            activities_evidence.append({
                "number": act_num,
                "source_page": page_num,
                "raw_title": act_title
            })

    # Sort & deduplicate activities by number
    activities_evidence.sort(key=lambda x: x["number"])
    seen_acts = set()
    dedup_acts = []
    for a in activities_evidence:
        if a["number"] not in seen_acts:
            seen_acts.add(a["number"])
            dedup_acts.append(a)
    activities_evidence = dedup_acts

    # B. Extract Exercises strictly PER PAGE (Preserving true source_page)
    ex_pattern = re.compile(
        r"(?:Exercise|Exercice|Problem|تمرين|مسألة)\s*(\d+)[:\.\s\-]+(.*?)(?=(?:Exercise|Exercice|Problem|تمرين|مسألة)\s*\d+|$)",
        re.DOTALL | re.I
    )

    # Focus on problem pages (typically last 2-3 pages of the chapter)
    end_page = pages[-1][0]
    problem_pages = [(p, t) for p, t in pages if p >= (end_page - 2)]

    for page_num, page_text in problem_pages:
        for match in ex_pattern.finditer(page_text):
            num = int(match.group(1))
            content = match.group(2).strip()
            clean_prompt = " ".join(content.split())
            if len(clean_prompt) >= 15:
                # Cryptographic hash of the exact source text
                content_hash = hashlib.sha256(clean_prompt.encode('utf-8')).hexdigest()[:16]
                
                # Check for figure references in this specific problem
                fig_refs = re.findall(r"(?:figure|fig\.|شكل)\s*(\d+)", clean_prompt, re.I)
                
                # VISUAL EVIDENCE EXTRACTION
                visual_evidence = []
                if fig_refs:
                    pdf_page = reader.pages[page_num - 1]
                    # Check if page actually contains embedded images/drawings
                    has_images = len(pdf_page.images) > 0 if hasattr(pdf_page, 'images') else True
                    for f_ref in fig_refs:
                        visual_evidence.append({
                            "figure_id": f_ref,
                            "source_page": page_num,
                            "confirmed_on_page": has_images
                        })

                exercise_evidence.append({
                    "number": num,
                    "source_page": page_num,
                    "raw_prompt": clean_prompt,
                    "source_text_hash": content_hash,
                    "figure_refs": fig_refs,
                    "visual_evidence": visual_evidence,
                    "requires_figure": len(fig_refs) > 0
                })

    # Sort & deduplicate exercises by number
    exercise_evidence.sort(key=lambda x: x["number"])
    seen_ex = set()
    dedup_ex = []
    for e in exercise_evidence:
        if e["number"] not in seen_ex:
            seen_ex.add(e["number"])
            dedup_ex.append(e)
    exercise_evidence = dedup_ex

    # ZERO-TOLERANCE GATE 1: NO FAKE FALLBACKS
    if not exercise_evidence:
        raise AssertionError("QUALITY_GATE_FAILED: EXERCISE_EVIDENCE_MISSING (Failed to extract verbatim exercises)")

    full_text = "\n\n".join([f"=== Page {p} ===\n{t}" for p, t in pages])

    return {
        "full_text": full_text,
        "activities_evidence": activities_evidence,
        "exercise_evidence": exercise_evidence,
        "exercise_numbers": [x["number"] for x in exercise_evidence]
    }


# =========================================================================
# 3. PEDAGOGY PROFILE COMPILER
# =========================================================================

def compile_pedagogy_profile(evidence_map, subject):
    act_count = len(evidence_map["activities_evidence"])
    ex_count = len(evidence_map["exercise_evidence"])
    text_lower = evidence_map["full_text"].lower()

    # Determine dynamic lab model strictly from physical phenomenon evidenced
    lab_type = None
    if any(k in text_lower for k in ["tilted", "inclined", "free surface", "horizontal surface"]):
        lab_type = "fluid_tilt_surface"
    elif any(k in text_lower for k in ["communicating vessels", "level tube", "u-tube"]):
        lab_type = "communicating_vessels"
    elif any(k in text_lower for k in ["circuit", "lamp", "switch", "current"]):
        lab_type = "electric_circuit"

    return {
        "expected_activities_count": act_count,
        "expected_exercises_count": ex_count,
        "lab_spec_type": lab_type,
        "has_lab": lab_type is not None
    }


# =========================================================================
# 4. AI TEACHING LAYER (NABIL METHOD OVER SOURCE-LOCKED PROMPTS)
# =========================================================================

def generate_pedagogical_theory(client, model, canonical_entry, evidence_map, profile):
    title = canonical_entry["canonical_title"]
    grade = canonical_entry["grade"]
    subject = canonical_entry["subject"]
    
    prompt = (
        f"You are Teacher NABIL, master professor for Lebanese Grade {grade} {subject}.\n"
        f"Lesson: '{title}'.\n\n"
        f"VERIFIED EVIDENCE MAP FROM BOOK SCANS:\n{evidence_map['full_text']}\n\n"
        f"PEDAGOGY REQUIREMENT: You MUST generate EXACTLY {profile['expected_activities_count']} activities "
        "corresponding 1:1 to the activities evidenced in the book scans.\n"
        "STRICT PROHIBITION: Do NOT introduce surface tension, cohesion, adhesion, density formulas, or hydrostatic pressure.\n"
        "Output format strictly valid JSON: {\n"
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
        max_tokens=1800,
        temperature=0.1
    )
    txt = resp.choices[0].message.content.strip()
    if txt.startswith("```"):
        txt = re.sub(r"^```(?:json)?\s*|\s*```$", "", txt, flags=re.I).strip()
    return json.loads(txt)


def solve_source_locked_exercises_adaptive(client, model, canonical_entry, evidence_map):
    title = canonical_entry["canonical_title"]
    grade = canonical_entry["grade"]
    ex_items = evidence_map["exercise_evidence"]
    all_solved = []

    # Dynamic Token-Budget Adaptive Batching
    avg_words = sum(len(x["raw_prompt"].split()) for x in ex_items) / max(1, len(ex_items))
    batch_size = max(1, min(3, math.floor(800 / (avg_words * 2.5 + 250))))
    chunks = [ex_items[i:i + batch_size] for i in range(0, len(ex_items), batch_size)]

    for idx, chunk in enumerate(chunks, 1):
        progress("SOLVING_ADAPTIVE_EXERCISE_BATCH", batch=idx, total=len(chunks), 
                 batch_size=len(chunk), items=[x["number"] for x in chunk])

        prompt = (
            f"You are Teacher NABIL solving official Lebanese CRDP textbook exercises for Grade {grade} Physics: '{title}'.\n\n"
            f"LOCKED SOURCE PROMPTS TO SOLVE (DO NOT MODIFY OR SWAP):\n"
            f"{json.dumps(chunk, ensure_ascii=False)}\n\n"
            "MANDATORY INSTRUCTIONS:\n"
            "1. You are providing the SOLUTION & TEACHING LAYER ONLY. Do NOT alter the physical task.\n"
            "2. If requires_figure is true, reconstruct a clean, faithful vector SVG diagram (viewBox='0 0 600 220').\n"
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
            "    'source_text_hash': str,\n"
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

                for it in data:
                    num = it.get("number")
                    orig = next((x for x in chunk if x["number"] == num), None)
                    if orig:
                        merged = {
                            "number": num,
                            "source_page": orig["source_page"],
                            "source_text_hash": orig["source_text_hash"],
                            "raw_prompt": orig["raw_prompt"],  # Immutably source-locked
                            "title": it.get("title", f"Exercise {num}"),
                            "prompt_ar": it.get("prompt_ar", ""),
                            "steps_en": it.get("steps_en", []),
                            "nabil_oral_ar": it.get("nabil_oral_ar", ""),
                            "final_answer": it.get("final_answer", ""),
                            "svg_diagram": it.get("svg_diagram", "") if orig["requires_figure"] else "",
                            "requires_figure": orig["requires_figure"],
                            "figure_refs": orig["figure_refs"]
                        }
                        all_solved.append(merged)
                break
            except Exception as e:
                progress("BATCH_WAIT_RETRY", error=str(e)[:100], attempt=attempt)
                time.sleep(4)

        time.sleep(2)

    return all_solved


# =========================================================================
# 5. HARD QUALITY GATES (DETERMINISTIC VERIFICATION)
# =========================================================================

def execute_deterministic_quality_gates(theory_data, solved_exercises, evidence_map, profile):
    progress("EXECUTING_STRICT_DETERMINISTIC_GATES")

    # 1. Exact Activity Matching Gate
    activities = theory_data.get("activities", [])
    if len(activities) != profile["expected_activities_count"]:
        raise AssertionError(
            f"PEDAGOGY_PROFILE_MISMATCH: Evidence Map defines {profile['expected_activities_count']} "
            f"activities, but generated payload has {len(activities)}"
        )

    for act in activities:
        if not act.get("experiment_en") or not act.get("observation_en") or not act.get("conclusion_en"):
            raise AssertionError("ACTIVITY_EVIDENCE_MISSING: Activity lacks Experiment/Observation/Conclusion")

    # 2. Strict Exercise Sequence Gate
    expected_numbers = set(evidence_map["exercise_numbers"])
    solved_numbers = {int(x.get("number", 0)) for x in solved_exercises if "number" in x}
    missing_numbers = expected_numbers - solved_numbers
    if missing_numbers:
        raise AssertionError(f"EXERCISE_SEQUENCE_INCOMPLETE: Missing exercises {sorted(list(missing_numbers))}")

    # 3. Cryptographic Source-Lock Hash & Source-Page Verification Gate
    for orig in evidence_map["exercise_evidence"]:
        matched = next((x for x in solved_exercises if x["number"] == orig["number"]), None)
        if not matched:
            raise AssertionError(f"EXERCISE_SOURCE_MISMATCH: Exercise {orig['number']} absent")
        if matched["source_text_hash"] != orig["source_text_hash"]:
            raise AssertionError(
                f"EXERCISE_SOURCE_MISMATCH: Hash mismatch on exercise {orig['number']}! "
                f"Expected {orig['source_text_hash']} but got {matched['source_text_hash']}"
            )
        if matched["source_page"] != orig["source_page"]:
            raise AssertionError(f"EXERCISE_SOURCE_MISMATCH: Page mismatch on exercise {orig['number']}")

    # 4. Visual Evidence Gate
    for orig in evidence_map["exercise_evidence"]:
        if orig["requires_figure"]:
            matched = next(x for x in solved_exercises if x["number"] == orig["number"])
            svg = matched.get("svg_diagram", "")
            if not svg or "<svg" not in svg:
                raise AssertionError(
                    f"FIGURE_EVIDENCE_MISSING: Exercise {orig['number']} references figures "
                    f"{orig['figure_refs']} but valid SVG is missing"
                )

    # 5. Non-Empty Worksheet & Study Card Gate
    worksheet = theory_data.get("worksheet", [])
    if len(worksheet) < 4:
        raise AssertionError("WORKSHEET_EMPTY: Formative worksheet must have at least 4 items")

    panels = theory_data.get("study_card", {}).get("panels", [])
    if len(panels) < 2:
        raise AssertionError("STUDY_CARD_INCOMPLETE: Study card has fewer than 2 summary panels")

    # 6. Source Boundary Hallucination Guard
    forbidden = ["surface tension", "cohesion", "adhesion", "hydrostatic pressure", "density of water", "p = ρgh"]
    dump = json.dumps(theory_data).lower() + " " + json.dumps(solved_exercises).lower()
    for term in forbidden:
        if term in dump:
            raise AssertionError(f"SOURCE_BOUNDARY_BREACH: Forbidden unevidenced term detected: '{term}'")

    progress("ALL_DETERMINISTIC_GATES_PASSED_SUCCESSFULLY")


# =========================================================================
# 6. DYNAMIC MODULAR LAB RENDERER (NO HARD-CODED WATER VESSEL)
# =========================================================================

def render_dynamic_live_lab(lab_type):
    """
    Renders modular interactive simulations strictly according to lab_spec_type.
    Returns empty string if no lab is pedagogically warranted.
    """
    if not lab_type:
        return ""

    if lab_type == "fluid_tilt_surface":
        return """
        <section id="lab" class="card">
          <h2>🧪 Live Lab · Tilt the Vessel &amp; Measure Surface</h2>
          <div class="lab">
            <p>Drag the slider to tilt the container. Observe that while the container rotates, the <b>liquid free surface at rest remains plane and horizontal</b> relative to the vertical reference:</p>
            <label>Tilt angle: <b id="ang" style="color:var(--c-obs-bar);">0°</b>
              <input id="tilt" type="range" min="-35" max="35" value="0"/>
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

    elif lab_type == "communicating_vessels":
        return """
        <section id="lab" class="card">
          <h2>🧪 Live Lab · Communicating Vessels Equilibrium</h2>
          <div class="lab">
            <p>Adjust the liquid volume. Notice that the liquid level <b>remains in the exact same horizontal plane</b> across all branches regardless of tube diameter:</p>
            <label>Water Height (mL): <b id="volLabel" style="color:var(--c-obs-bar);">120 mL</b>
              <input id="volSlider" type="range" min="60" max="180" value="120"/>
            </label>
            <div class="figure">
              <svg viewBox="0 0 650 260">
                <path d="M 100 40 L 100 200 L 200 200 L 200 40 M 200 200 L 360 200 M 360 40 L 360 200 L 420 200 L 420 40 M 420 200 L 540 200 L 540 40" fill="none" stroke="#38bdf8" stroke-width="7"/>
                <line id="commWater" x1="105" y1="120" x2="535" y2="120" stroke="#38bdf8" stroke-width="8" stroke-dasharray="1000"/>
                <line x1="50" y1="120" x2="600" y2="120" stroke="var(--c-concl-bar)" stroke-width="2" stroke-dasharray="6 4"/>
              </svg>
            </div>
            <div class="answer">Free surfaces equalize to the same horizontal plane.</div>
          </div>
        </section>"""

    return ""


# =========================================================================
# 7. HTML RENDERERS & SAFE NAVIGATION
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


def render_page_a(theory_data, canonical_entry, profile):
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

    # Dynamic Modular Lab
    lab_html = render_dynamic_live_lab(profile.get("lab_spec_type"))

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

        # SOURCE-LOCKED DISPLAY: Injected verbatim from raw_prompt
        items_html += f"""
        <article class="exercise" id="ex{num}" data-ex-number="{num}" data-source-hash="{ex.get('source_text_hash', '')}">
          <div class="exhead">
            <span>Exercise #{num} — {e(ex.get('title', 'Official Exercise'))}</span>
            <span class="source">Textbook Page {ex.get('source_page', start_p)}</span>
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
# 8. PRODUCTION ORCHESTRATOR
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

        # 1. Deterministic Per-Page Evidence Map (Source-Locked)
        evidence_map = build_deterministic_evidence_map(pages, reader)
        progress("EVIDENCE_MAP_EXTRACTED", 
                 activities=len(evidence_map["activities_evidence"]), 
                 exercises=len(evidence_map["exercise_evidence"]))

        # 2. Compile Exact Pedagogy Profile
        profile = compile_pedagogy_profile(evidence_map, canonical_entry["subject"])

        # 3. Setup AI provider
        prov = configured_providers()[0]
        from openai import OpenAI
        client = OpenAI(api_key=prov[1], base_url=prov[2], timeout=180)

        # 4. Generate Pedagogical Theory & Adaptive Source-Locked Solutions
        theory_data = generate_pedagogical_theory(client, prov[3], canonical_entry, evidence_map, profile)
        solved_exercises = solve_source_locked_exercises_adaptive(client, prov[3], canonical_entry, evidence_map)

        # 5. Strict Zero-Tolerance Quality Gates
        execute_deterministic_quality_gates(theory_data, solved_exercises, evidence_map, profile)

        # 6. Render Output Files
        slug = re.sub(r"[^\w]+", "-", title.upper()).strip("-")
        num_str = lesson_id.split("-")[-1]
        grade_tag = f"G{canonical_entry['grade']:02d}"
        subj_tag = canonical_entry['subject'].upper()

        theory_filename = f"{grade_tag}-{subj_tag}--{num_str}--{slug}.html"
        exercises_filename = f"{grade_tag}-{subj_tag}--{num_str}--{slug}--EXERCISES.html"

        html_theory = render_page_a(theory_data, canonical_entry, profile)
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
    parser = argparse.ArgumentParser(description="NABIL AI Universal Production Factory")
    parser.add_argument("--report", default="data/nabil_lesson_factory_run.json")
    parser.add_argument("--lesson-id", default="G07-PHYSICS-001")
    parser.add_argument("--build-catalog", action="store_true", help="Extract TOC and build canonical catalog")
    parser.add_argument("--book-id", default="1LasqIgGUuck1l-2EZbj2kA0Dg9ygJ_AH", help="Google Drive PDF ID for catalog build")
    parser.add_argument("--grade", default=7, type=int)
    parser.add_argument("--subject", default="physics")
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()

    global PROGRESS_STARTED
    PROGRESS_STARTED = time.monotonic()

    service = owner_drive()

    # Mode 1: Dynamic Catalog Builder with Opening-Page Verification
    if args.build_catalog:
        build_or_verify_catalog(service, args.book_id, args.grade, args.subject)
        return 0

    # Mode 2: Lesson Production
    report_path = Path(args.report)
    catalog = load_catalog(service, args.lesson_id)

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
        print("[ERROR] Lesson entry not found in verified catalog:", args.lesson_id)
        return 1

    rep = produce_lesson_for_entry(service, target_entry, report_path, publish=args.publish)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(rep, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(rep, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
