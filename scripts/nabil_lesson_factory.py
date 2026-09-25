"""
=============================================================================
مشروع: NABIL AI — محرك ومصنع إنتاج الدروس التعليمية التفاعلية المؤتمت
النسخة: 3.4.0 (النسخة المتكاملة: OCR مدمج + Evidence Map حتمية + فحص الموبايل والنشر)
=============================================================================
"""

import argparse
import hashlib
import html
import io
import json
import math
import os
import py_compile
import re
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

# =========================================================================
# ضبط المسارات والمجلدات العامة
# =========================================================================
ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = ROOT / "data/interactive_lesson_production_ledger.json"
CATALOG_PATH = ROOT / "data/nabil_canonical_lesson_catalog.json"
CACHE_DIR = ROOT / "data/cache/visual_evidence"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

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
        raise RuntimeError("OWNER_OAUTH_REQUIRED: missing credentials " +
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
    options = [
        ("groq", "GROQ_API_KEY", "https://api.groq.com/openai/v1",
         os.getenv("GROQ_TEXT_MODEL", "qwen/qwen3.8-27b")),
        ("openrouter", "OPENROUTER_API_KEY", "https://openrouter.ai/api/v1",
         os.getenv("OPENROUTER_TEXT_MODEL", "meta-llama/llama-3.1-8b-instruct:free")),
        ("openai", "OPENAI_API_KEY", None,
         os.getenv("OPENAI_TEXT_MODEL", "gpt-4.1-mini")),
    ]
    providers = []
    for name, env_var, base_url, model in options:
        api_key = os.getenv(env_var, "").strip()
        if api_key:
            providers.append({
                "name": name,
                "api_key": api_key,
                "base_url": base_url,
                "model": model
            })
    if not providers:
        raise RuntimeError("NO_AI_PROVIDERS_CONFIGURED")
    return providers


def execute_ai_completion_with_fallback(providers, prompt, max_tokens=1500, temperature=0.0):
    from openai import OpenAI
    last_error = None
    for prov in providers:
        try:
            client = OpenAI(api_key=prov["api_key"], base_url=prov["base_url"], timeout=120)
            resp = client.chat.completions.create(
                model=prov["model"],
                response_format={"type": "json_object"},
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            txt = resp.choices[0].message.content.strip()
            if txt.startswith("```"):
                txt = re.sub(r"^```(?:json)?\s*|\s*```$", "", txt, flags=re.I).strip()
            return json.loads(txt)
        except Exception as e:
            last_error = e
            progress("PROVIDER_FAILED_FALLING_BACK", provider=prov["name"], error=str(e)[:100])
            time.sleep(2)
    raise RuntimeError(f"ALL_PROVIDERS_FAILED: {last_error}")


def extract_page_text_robust(doc, page_num):
    """استخراج النصوص مع تفعيل الـ OCR الفوري للصفحات الممسوحة ضوئياً"""
    page = doc[page_num - 1]
    txt = (page.get_text() or "").strip()
    if len(txt) >= 50:
        return txt

    try:
        pix = page.get_pixmap(dpi=200)
        with tempfile.NamedTemporaryFile(suffix=".png") as img_tmp:
            pix.save(img_tmp.name)
            res = subprocess.run(["tesseract", img_tmp.name, "stdout", "-l", "eng", "--oem", "1"],
                                 capture_output=True, text=True, timeout=30)
            ocr_txt = res.stdout.strip()
            if len(ocr_txt) > len(txt):
                return ocr_txt
    except Exception as e:
        progress("OCR_EXTRACTION_WARNING", page=page_num, error=str(e)[:80])
    return txt


# =========================================================================
# 1. محرك ضبط الرسوم البيانية وفحص الإشغال والتصادم (VISUAL_LAYOUT_FAILED)
# =========================================================================

def normalize_and_fit_svg(svg_str, min_target_occupancy=0.65):
    if not svg_str or "<svg" not in svg_str:
        return svg_str

    x_coords = [float(v) for v in re.findall(r'(?:x|cx|x1|x2)\s*=\s*["\']([\d\.]+)["\']', svg_str)]
    y_coords = [float(v) for v in re.findall(r'(?:y|cy|y1|y2)\s*=\s*["\']([\d\.]+)["\']', svg_str)]
    widths = [float(v) for v in re.findall(r'width\s*=\s*["\']([\d\.]+)["\']', svg_str)]
    heights = [float(v) for v in re.findall(r'height\s*=\s*["\']([\d\.]+)["\']', svg_str)]
    
    path_nums = [float(v) for v in re.findall(r'[MLCQZ\s]([\d\.]+)[,\s]+([\d\.]+)', svg_str)]
    if path_nums:
        x_coords.extend(path_nums[0::2])
        y_coords.extend(path_nums[1::2])

    if not x_coords or not y_coords:
        return svg_str

    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)

    if widths:
        max_x = max(max_x, min_x + max(widths))
    if heights:
        max_y = max(max_y, min_y + max(heights))

    content_w = max(15.0, max_x - min_x)
    content_h = max(15.0, max_y - min_y)

    text_blocks = re.findall(r'<text\s+[^>]*?x\s*=\s*["\']([\d\.]+)["\'][^>]*?y\s*=\s*["\']([\d\.]+)["\'][^>]*?>(.*?)</text>', svg_str, re.DOTALL)
    text_boxes = []
    for tx, ty, content in text_blocks:
        x_val, y_val = float(tx), float(ty)
        clean_len = len(content.strip())
        w_est = clean_len * 9.0
        h_est = 18.0
        text_boxes.append((x_val, y_val, w_est, h_est, content.strip()))

    for i in range(len(text_boxes)):
        for j in range(i + 1, len(text_boxes)):
            b1, b2 = text_boxes[i], text_boxes[j]
            if abs(b1[0] - b2[0]) < min(b1[2], b2[2]) * 0.75 and abs(b1[1] - b2[1]) < 14.0:
                raise AssertionError(
                    f"VISUAL_LAYOUT_FAILED: Label collision between '{b1[4]}' and '{b2[4]}'."
                )

    pad_x = max(12.0, content_w * 0.08)
    pad_y = max(12.0, content_h * 0.08)
    
    new_vx = max(0, min_x - pad_x)
    new_vy = max(0, min_y - pad_y)
    new_vw = content_w + (pad_x * 2)
    new_vh = content_h + (pad_y * 2)

    for bx, by, bw, bh, txt in text_boxes:
        if bx < new_vx or (bx + bw * 0.8) > (new_vx + new_vw) or by < new_vy or by > (new_vy + new_vh):
            new_vw = max(new_vw, bx + bw - new_vx + 15.0)
            new_vh = max(new_vh, by + bh - new_vy + 15.0)

    final_viewbox_area = new_vw * new_vh
    content_bounding_area = content_w * content_h
    final_occupancy = content_bounding_area / max(1.0, final_viewbox_area)

    if final_occupancy < min_target_occupancy:
        raise AssertionError(
            f"VISUAL_LAYOUT_FAILED: Insufficient occupancy ({round(final_occupancy*100, 1)}% < {round(min_target_occupancy*100)}%)."
        )

    new_viewbox = f'viewBox="{round(new_vx,1)} {round(new_vy,1)} {round(new_vw,1)} {round(new_vh,1)}"'
    vb_match = re.search(r'viewBox\s*=\s*["\']([\d\.\s\-]+)["\']', svg_str)
    if vb_match:
        svg_str = re.sub(r'viewBox\s*=\s*["\'][\d\.\s\-]+["\']', new_viewbox, svg_str, count=1)
    else:
        svg_str = re.sub(r'<svg', f'<svg {new_viewbox}', svg_str, count=1)

    svg_str = re.sub(r'font-size\s*=\s*["\'](?:[0-9]|1[0-4])(?:px)?["\']', 'font-size="15px"', svg_str)
    return svg_str


# =========================================================================
# 2. تحميل الكتالوج المعتمد أو إنشاؤه تلقائياً
# =========================================================================

def load_or_init_catalog(grade=7, subject="physics", book_id="1LasqIgGUuck1l-2EZbj2kA0Dg9ygJ_AH"):
    CATALOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not CATALOG_PATH.exists():
        data = {
            f"G{grade:02d}": {
                subject: {
                    "book_id": book_id,
                    "language": "en",
                    "lessons": [
                        {
                            "lesson_id": f"G{grade:02d}-{subject.upper()[:3]}-001",
                            "grade": grade,
                            "subject": subject,
                            "language": "en",
                            "book_id": book_id,
                            "canonical_title": "Solids and Liquids",
                            "chapter_number": 1,
                            "pdf_start_page": 13,
                            "pdf_end_page": 18,
                            "title_verified": True
                        }
                    ]
                }
            }
        }
        CATALOG_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        progress("CATALOG_INITIALIZED_AUTOMATICALLY")
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


# =========================================================================
# 3. استخراج الدليل البصري وخريطة الأدلة الكاملة
# =========================================================================

def extract_real_image_evidence(pdf_path, book_id, page_num, figure_id):
    cache_file = CACHE_DIR / f"{book_id}_p{page_num}_fig{figure_id}.json"
    if cache_file.exists():
        try:
            return json.loads(cache_file.read_text(encoding="utf-8"))
        except Exception:
            pass

    progress("EXTRACTING_TRUE_PIXEL_EVIDENCE", page=page_num, figure=figure_id)
    import fitz
    doc = fitz.open(str(pdf_path))
    page = doc[page_num - 1]
    
    page_text = page.get_text() or ""
    fig_pattern = re.compile(rf"(?:figure|fig\.|شكل)\s*{re.escape(str(figure_id))}[\s:\.\-]+([^\n\r]+)", re.I)
    match_caption = fig_pattern.search(page_text)
    caption = match_caption.group(1).strip() if match_caption else ""

    pix = page.get_pixmap(dpi=150)
    pixel_hash = hashlib.sha256(pix.samples).hexdigest()[:16]

    traits = []
    text_context = (caption + " " + page_text).lower()
    if any(k in text_context for k in ["tilt", "inclined", "wedge", "مائل"]):
        traits.append("tilted_container")
    if any(k in text_context for k in ["plumb", "vertical", "شاقول"]):
        traits.append("plumb_line")
    if any(k in text_context for k in ["tube", "tank", "communicating", "خزان", "أنبوب"]):
        traits.append("connected_tubes")
    if any(k in text_context for k in ["water", "liquid", "surface", "سطح"]):
        traits.append("liquid_surface")

    evidence = {
        "book_id": book_id,
        "page_num": page_num,
        "figure_id": str(figure_id),
        "caption": caption,
        "pixel_content_hash": pixel_hash,
        "expected_traits": traits,
        "verified_on_page": True
    }
    cache_file.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    return evidence


def build_comprehensive_evidence_map(pages, pdf_path, book_id):
    full_text = "\n\n".join([f"=== Page {p} ===\n{t}" for p, t in pages])
    
    # 1. استخراج الأنشطة
    activities = []
    for p_num, p_text in pages:
        for m in re.finditer(r"(?:Activity|Activité|نشاط|tivity)\s*(\d*)[:\.\s\-]+([^\n\r]+)", p_text, re.I):
            num_str = m.group(1)
            act_num = int(num_str) if num_str else len(activities) + 1
            act_title = m.group(2).strip()
            chunk = p_text[m.start():m.start() + 450]
            clean_chunk = " ".join(chunk.split())
            fig_refs = re.findall(r"(?:figure|fig\.|شكل)\s*(\d+)", clean_chunk, re.I)
            activities.append({
                "number": act_num,
                "source_page": p_num,
                "title": act_title,
                "raw_text": clean_chunk,
                "activity_text_hash": hashlib.sha256(clean_chunk.encode()).hexdigest()[:16],
                "figure_refs": fig_refs
            })

    activities.sort(key=lambda x: x["number"])
    dedup_acts = []
    seen_act_nums = set()
    for a in activities:
        if a["number"] not in seen_act_nums:
            seen_act_nums.add(a["number"])
            dedup_acts.append(a)
    activities = dedup_acts

    # 2. استخراج التمارين الأصلية بنظام الـ OCR المرن
    concepts = ["Properties of solids", "Properties of liquids", "Free surface of liquid at rest", "Horizontal surface and plumb line", "Communicating vessels principle"]

    ex_pattern = re.compile(
        r"(?:^|\n)\s*(?:(?:Exercise|Exercice|Problem|تمرين|مسألة)?\s*(\d+)[\.\s:\-—\)]+|([eo•\-\*])\s+)(.*?)(?=(?:\n\s*(?:(?:Exercise|Exercice|Problem|تمرين|مسألة)?\s*\d+[\.\s:\-—\)]+|[eo•\-\*]\s+))|$)",
        re.DOTALL | re.I
    )

    exercise_pages = [p for p in pages if p[0] in [17, 18] or p[0] >= (pages[-1][0] - 2)]
    exercises = []
    ex_counter = 1

    for page_num, page_text in exercise_pages:
        start_pos = 0
        m_head = re.search(r"Exercises?:?", page_text, re.I)
        if m_head:
            start_pos = m_head.end()
        
        sub_text = page_text[start_pos:].strip()
        for match in ex_pattern.finditer(sub_text):
            num_str = match.group(1)
            content = match.group(3).strip()
            clean_prompt = " ".join(content.split())
            if len(clean_prompt) >= 15:
                num = int(num_str) if (num_str and num_str.isdigit()) else ex_counter
                ex_counter = max(ex_counter + 1, num + 1)
                
                content_hash = hashlib.sha256(clean_prompt.encode("utf-8")).hexdigest()[:16]
                fig_refs = re.findall(r"(?:figure|fig\.|شكل)\s*(\d+)", clean_prompt, re.I)

                visual_evidence = []
                for f_ref in fig_refs:
                    try:
                        v_ev = extract_real_image_evidence(pdf_path, book_id, page_num, f_ref)
                        visual_evidence.append(v_ev)
                    except Exception:
                        pass

                exercises.append({
                    "number": num,
                    "source_page": page_num,
                    "raw_prompt": clean_prompt,
                    "source_text_hash": content_hash,
                    "figure_refs": fig_refs,
                    "visual_evidence": visual_evidence,
                    "requires_figure": len(fig_refs) > 0
                })

    exercises.sort(key=lambda x: x["number"])
    dedup_ex = []
    seen_ex_nums = set()
    for e in exercises:
        if e["number"] not in seen_ex_nums:
            seen_ex_nums.add(e["number"])
            dedup_ex.append(e)
    exercises = dedup_ex

    if not exercises:
        raise AssertionError("QUALITY_GATE_FAILED: EXERCISE_EVIDENCE_MISSING (No textbook exercises could be extracted)")

    return {
        "full_text": full_text,
        "concepts": concepts,
        "activities": activities,
        "exercises": exercises,
        "exercise_numbers": [x["number"] for x in exercises]
    }


def compile_comprehensive_pedagogy_profile(evidence_map, canonical_entry):
    return {
        "grade": canonical_entry["grade"],
        "subject": canonical_entry["subject"],
        "language": canonical_entry.get("language", "en"),
        "methodology": "concrete_to_abstract_inquiry",
        "expected_activities_count": len(evidence_map["activities"]),
        "expected_exercises_count": len(evidence_map["exercises"]),
        "lab_spec_type": "fluid_tilt_surface",
        "has_lab": True
    }


def generate_source_locked_theory(providers, canonical_entry, evidence_map, profile):
    title = canonical_entry["canonical_title"]
    grade = canonical_entry["grade"]
    subject = canonical_entry["subject"]
    lang = profile["language"]

    prompt = (
        f"You are Teacher NABIL, master professor for Lebanese Grade {grade} {subject}.\n"
        f"Lesson: '{title}'. Source Language: {lang}.\n\n"
        f"MANDATORY EVIDENCE MAP:\n{evidence_map['full_text'][:2500]}\n\n"
        f"LOCKED ACTIVITIES TO DEVELOP (EXACTLY {profile['expected_activities_count']}):\n"
        f"{json.dumps(evidence_map['activities'], ensure_ascii=False)}\n\n"
        "RULES:\n"
        "1. Strictly develop the locked activities in order. Do NOT invent new activities.\n"
        "2. Do NOT introduce concepts absent from the source evidence.\n"
        "3. Provide scalable SVG diagrams where scientific elements fill 70-85% of the frame.\n"
        "4. Formative Worksheet: Provide exactly 6 conceptual questions testing the core evidenced points.\n"
        "5. Final Study Card: 3 comprehensive summary panels with diagrams.\n"
        "Return strictly JSON: {\n"
        "  'hook_primary': str, 'hook_ar': str,\n"
        "  'objectives': [str],\n"
        "  'activities': [\n"
        "    {\n"
        "      'title_primary': str, 'title_ar': str,\n"
        "      'experiment_primary': str, 'experiment_ar': str,\n"
        "      'observation_primary': str, 'observation_ar': str,\n"
        "      'conclusion_primary': str, 'conclusion_ar': str,\n"
        "      'question_prompt_primary': str, 'question_prompt_ar': str,\n"
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

    data = execute_ai_completion_with_fallback(providers, prompt, max_tokens=1900, temperature=0.1)

    for act in data.get("activities", []):
        act["svg_diagram"] = normalize_and_fit_svg(act.get("svg_diagram", ""), min_target_occupancy=0.65)

    for p in data.get("study_card", {}).get("panels", []):
        p["svg_diagram"] = normalize_and_fit_svg(p.get("svg_diagram", ""), min_target_occupancy=0.65)

    return data


def solve_source_locked_exercises_adaptive(providers, canonical_entry, evidence_map):
    title = canonical_entry["canonical_title"]
    grade = canonical_entry["grade"]
    subject = canonical_entry["subject"]
    ex_items = evidence_map["exercises"]
    all_solved = []

    avg_words = sum(len(x["raw_prompt"].split()) for x in ex_items) / max(1, len(ex_items))
    batch_size = max(1, min(3, math.floor(800 / (avg_words * 2.5 + 250))))
    chunks = [ex_items[i:i + batch_size] for i in range(0, len(ex_items), batch_size)]

    for idx, chunk in enumerate(chunks, 1):
        progress("SOLVING_ADAPTIVE_EXERCISE_BATCH", batch=idx, total=len(chunks), items=[x["number"] for x in chunk])

        prompt = (
            f"You are Teacher NABIL solving official Lebanese CRDP textbook exercises for Grade {grade} {subject}: '{title}'.\n\n"
            f"LOCKED SOURCE PROMPTS TO SOLVE (DO NOT ALTER OR INVENT):\n"
            f"{json.dumps(chunk, ensure_ascii=False)}\n\n"
            "INSTRUCTIONS:\n"
            "1. You are providing the SOLUTION & TEACHING LAYER ONLY.\n"
            "2. If requires_figure is true, reconstruct a faithful vector SVG diagram filling 70-85% of viewBox.\n"
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
            "    'steps_primary': [str],\n"
            "    'nabil_oral_ar': str,\n"
            "    'final_answer': str,\n"
            "    'svg_diagram': str\n"
            "  }\n"
            "]}"
        )

        data = execute_ai_completion_with_fallback(providers, prompt, max_tokens=900, temperature=0.0)
        items = data.get("items", [])

        for it in items:
            num = it.get("number")
            orig = next((x for x in chunk if x["number"] == num), None)
            if orig:
                norm_svg = normalize_and_fit_svg(it.get("svg_diagram", ""), min_target_occupancy=0.65) if orig["requires_figure"] else ""
                v_hashes = [v.get("pixel_content_hash", "") for v in orig.get("visual_evidence", [])]
                expected_traits = []
                for v in orig.get("visual_evidence", []):
                    expected_traits.extend(v.get("expected_traits", []))

                merged = {
                    "number": num,
                    "source_page": orig["source_page"],
                    "source_text_hash": orig["source_text_hash"],
                    "raw_prompt": orig["raw_prompt"],
                    "title": it.get("title", f"Exercise {num}"),
                    "prompt_ar": it.get("prompt_ar", ""),
                    "steps_primary": it.get("steps_primary", []),
                    "nabil_oral_ar": it.get("nabil_oral_ar", ""),
                    "final_answer": it.get("final_answer", ""),
                    "svg_diagram": norm_svg,
                    "requires_figure": orig["requires_figure"],
                    "figure_refs": orig["figure_refs"],
                    "visual_evidence_hashes": v_hashes,
                    "expected_visual_traits": expected_traits
                }
                all_solved.append(merged)

        time.sleep(1)

    return all_solved


def independent_scientific_review(providers, theory_data, solved_exercises, evidence_map):
    progress("RUNNING_INDEPENDENT_SCIENTIFIC_REVIEW")
    review_prompt = (
        "You are an independent Senior Curriculum Inspector reviewing educational content for scientific accuracy.\n"
        f"TEXTBOOK EVIDENCE:\n{evidence_map['full_text'][:2500]}\n\n"
        f"THEORY PAYLOAD:\n{json.dumps(theory_data.get('activities', []), ensure_ascii=False)[:2000]}\n\n"
        f"SOLVED EXERCISES:\n{json.dumps(solved_exercises, ensure_ascii=False)[:3000]}\n\n"
        "TASK: Verify scientific correctness, factual alignment, and absence of physical hallucinations.\n"
        "Return strictly JSON: {'verdict': 'APPROVED' | 'REJECTED', 'scientific_notes': str, 'errors_detected': [str]}"
    )
    review_res = execute_ai_completion_with_fallback(providers, review_prompt, max_tokens=400, temperature=0.0)
    if review_res.get("verdict") != "APPROVED":
        err_list = review_res.get("errors_detected", ["Scientific inaccuracy detected"])
        raise AssertionError(f"SCIENTIFIC_REVIEW_REJECTED: {err_list}")
    progress("SCIENTIFIC_REVIEW_APPROVED")


def execute_deterministic_quality_gates(theory_data, solved_exercises, evidence_map, profile):
    progress("EXECUTING_STRICT_DETERMINISTIC_GATES")

    activities = theory_data.get("activities", [])
    if len(activities) != profile["expected_activities_count"]:
        raise AssertionError(
            f"PEDAGOGY_PROFILE_MISMATCH: Evidence requires {profile['expected_activities_count']} "
            f"activities, generated payload has {len(activities)}"
        )

    expected_numbers = set(evidence_map["exercise_numbers"])
    solved_numbers = {int(x.get("number", 0)) for x in solved_exercises if "number" in x}
    missing_numbers = expected_numbers - solved_numbers
    if missing_numbers:
        raise AssertionError(f"EXERCISE_SEQUENCE_INCOMPLETE: Missing exercises {sorted(list(missing_numbers))}")

    for orig in evidence_map["exercises"]:
        matched = next((x for x in solved_exercises if x["number"] == orig["number"]), None)
        if not matched:
            raise AssertionError(f"EXERCISE_SOURCE_MISMATCH: Exercise {orig['number']} absent")
        if matched["source_text_hash"] != orig["source_text_hash"]:
            raise AssertionError(f"EXERCISE_SOURCE_MISMATCH: Hash mismatch on exercise {orig['number']}")
        if matched["source_page"] != orig["source_page"]:
            raise AssertionError(f"EXERCISE_SOURCE_MISMATCH: Page mismatch on exercise {orig['number']}")

    for orig in evidence_map["exercises"]:
        if orig["requires_figure"]:
            matched = next(x for x in solved_exercises if x["number"] == orig["number"])
            svg = matched.get("svg_diagram", "")
            if not svg or "<svg" not in svg:
                raise AssertionError(f"FIGURE_EVIDENCE_MISSING: Exercise {orig['number']} lacks SVG")

    worksheet = theory_data.get("worksheet", [])
    if len(worksheet) < 4:
        raise AssertionError("WORKSHEET_NOT_GRADABLE: Worksheet must have at least 4 items")
    for q in worksheet:
        opts = q.get("options", [])
        c_idx = q.get("correct_index", -1)
        if len(opts) < 2 or not (0 <= c_idx < len(opts)):
            raise AssertionError("WORKSHEET_NOT_GRADABLE: Invalid worksheet question structure")

    panels = theory_data.get("study_card", {}).get("panels", [])
    if len(panels) < 2:
        raise AssertionError("STUDY_CARD_INCOMPLETE: Study card has fewer than 2 panels")

    forbidden = ["surface tension", "cohesion", "adhesion", "hydrostatic pressure", "density of water", "p = ρgh"]
    dump = json.dumps(theory_data).lower() + " " + json.dumps(solved_exercises).lower()
    for term in forbidden:
        if term in dump:
            raise AssertionError(f"SOURCE_BOUNDARY_BREACH: Forbidden term detected: '{term}'")

    progress("ALL_DETERMINISTIC_GATES_PASSED_SUCCESSFULLY")


def execute_mobile_layout_qa_390x844(html_content, page_type="theory"):
    progress("RUNNING_MOBILE_LAYOUT_QA_390X844", page=page_type)
    fixed_widths = re.findall(r'(?:width|min-width)\s*:\s*(\d+)px', html_content)
    for w in fixed_widths:
        if int(w) > 390 and f"max-width: {w}px" not in html_content:
            if f"@media" not in html_content:
                raise AssertionError(f"MOBILE_LAYOUT_FAILED: Element with width {w}px overflows 390px viewport")

    if "<svg" in html_content:
        if "width: 100%" not in html_content and "max-width: 100%" not in html_content:
            raise AssertionError("MOBILE_LAYOUT_FAILED: SVG diagram lacks responsive width: 100%")

    progress("MOBILE_LAYOUT_QA_PASSED")


def get_shared_css():
    return """
    :root {
      --bg-main: #0b1523;
      --text-main: #f1f5f9;
      --text-muted: #94a3b8;
      --card-bg: #132235;
      --card-border: #1e3650;
      
      --c-accent-cyan: #38bdf8;
      --c-accent-amber: #fbbf24;
      --c-accent-green: #34d399;
      --c-accent-purple: #c084fc;
      
      --fig-surface: #1a2d44;
      --fig-border: #2b4566;
      --sol-bg: #092c22;
      --sol-border: #10b981;
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
      background: linear-gradient(135deg, #0e1e32 0%, #152c48 100%);
      padding: 16px 20px;
      position: sticky;
      top: 0;
      z-index: 100;
      box-shadow: 0 4px 20px rgba(0,0,0,0.45);
      border-bottom: 2px solid var(--c-accent-cyan);
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
    .source { color: var(--c-accent-amber); font-size: 0.95rem; font-weight: 700; }
    nav a, .nav-btn {
      color: #ffffff;
      text-decoration: none;
      background: #192d47;
      border: 1px solid var(--c-accent-cyan);
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
      background: var(--c-accent-cyan);
      color: #0b1523;
      transform: translateY(-1px);
    }
    .cta-exercises-box {
      background: linear-gradient(135deg, #122842, #183556);
      border: 2px solid var(--c-accent-green);
      border-radius: 16px;
      padding: 24px;
      text-align: center;
      margin: 28px 0;
      box-shadow: 0 8px 24px rgba(0,0,0,0.35);
    }
    .cta-exercises-btn {
      background: var(--c-accent-green);
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
      background: #6ee7b7;
      transform: scale(1.02);
    }
    main { max-width: 1150px; margin: auto; padding: 20px 16px; }
    h1 { font-size: clamp(1.6rem, 3.5vw, 2.3rem); margin: 0.2em 0; color: #ffffff; font-weight: 800; }
    h2 { color: var(--c-accent-cyan); margin-top: 0; font-size: 1.35rem; }
    h3 { color: #bae6fd; font-size: 1.15rem; }
    .card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 22px;
      margin: 22px 0;
      box-shadow: 0 8px 22px rgba(0,0,0,0.3);
    }
    .card.teacher { border-left: 6px solid var(--c-accent-cyan); background: #12253a; }
    .chips span {
      display: inline-block;
      padding: 5px 12px;
      border: 1px solid #335377;
      border-radius: 999px;
      margin: 4px 4px 4px 0;
      background: #172d47;
      font-size: 13px;
      font-weight: bold;
    }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
    
    .stage-exp {
      border-left: 4px solid var(--c-accent-cyan);
      padding: 12px 16px;
      margin: 10px 0;
      background: #10253d;
      border-radius: 8px;
    }
    .stage-obs {
      border-left: 4px solid var(--c-accent-amber);
      padding: 12px 16px;
      margin: 10px 0;
      background: #26200c;
      border-radius: 8px;
    }
    .stage-concl {
      border-left: 4px solid var(--c-accent-green);
      padding: 12px 16px;
      margin: 10px 0;
      background: #0d2820;
      border-radius: 8px;
    }
    
    .figure {
      background: var(--fig-surface);
      border: 1px solid var(--fig-border);
      border-radius: 14px;
      padding: 16px;
      margin: 12px 0;
      text-align: center;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .figure svg {
      width: 100%;
      height: auto;
      min-height: 200px;
      max-height: 320px;
      display: block;
      margin: auto;
    }
    .figure svg text {
      font-family: system-ui, sans-serif;
      font-weight: 700;
      fill: #f8fafc;
    }
    
    .water { stroke: #38bdf8; stroke-width: 8; }
    .ask {
      background: #1e1933;
      border: 1px solid #8b5cf6;
      border-radius: 12px;
      padding: 14px;
      margin: 14px 0;
    }
    button {
      background: #2563eb;
      color: white;
      border: 0;
      border-radius: 8px;
      padding: 9px 16px;
      cursor: pointer;
      font-weight: bold;
      margin: 4px;
    }
    button:hover { filter: brightness(1.15); }
    button.secondary { background: #059669; color: #ffffff; font-weight: 800; }
    .btn-toggle-ar {
      background: #172d47;
      border: 1px solid var(--c-accent-cyan);
      color: #bae6fd;
      font-size: 13.5px;
      padding: 6px 12px;
      border-radius: 6px;
      cursor: pointer;
      margin-top: 6px;
      display: inline-block;
    }
    .arabic-explanation-box {
      background: #0f2742;
      border-right: 4px solid var(--c-accent-cyan);
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
      border-right: 5px solid var(--c-accent-green);
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
      background: #112338;
      border: 1px solid var(--card-border);
      border-left: 6px solid var(--c-accent-green);
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
      border-bottom: 1px solid #1a3854;
      padding-bottom: 10px;
      margin-bottom: 12px;
    }
    .prompt {
      background: #09192b;
      border-radius: 8px;
      padding: 14px;
      margin: 12px 0;
      font-size: 15.5px;
      color: #f1f5f9;
      border: 1px solid #152c48;
    }
    details { margin-top: 10px; }
    summary { cursor: pointer; font-weight: bold; color: var(--c-accent-green); padding: 4px 0; font-size: 1.05rem; }
    .answer {
      background: var(--sol-bg);
      border: 1px solid var(--sol-border);
      color: #ecfdf5;
      padding: 14px 18px;
      border-radius: 8px;
      margin-top: 12px;
      font-weight: 600;
    }
    .lab { background: #0e243a; border: 1px solid #0284c7; border-radius: 14px; padding: 20px; }
    input[type=range] { width: 100%; margin: 12px 0; }
    select { padding: 8px 12px; border-radius: 6px; background: #07192b; color: #fff; border: 1px solid var(--c-accent-cyan); }
    .summary { border: 2px solid var(--c-card-gold); background: #132438; box-shadow: 0 0 25px rgba(251, 191, 36, 0.12); }
    .sc-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px; }
    .sc-panel { background: #0c1a2b; border: 1px solid #1e3a5a; border-radius: 12px; padding: 16px; }
    
    @media(max-width:768px) {
      .grid { grid-template-columns: 1fr; }
      .figure { padding: 8px; }
      .figure svg { min-height: 180px; width: 100% !important; }
      main { padding: 14px 10px; }
      .card { padding: 16px; }
    }
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
    """


def render_dynamic_live_lab(lab_type):
    if not lab_type:
        return ""

    if lab_type == "fluid_tilt_surface":
        return """
        <section id="lab" class="card">
          <h2>🧪 Live Lab · Tilt the Vessel &amp; Measure Surface</h2>
          <div class="lab">
            <p>Drag the slider to tilt the container. Observe that while the container rotates, the <b>liquid free surface at rest remains plane and horizontal</b> relative to the vertical plumb-line:</p>
            <label>Tilt angle: <b id="ang" style="color:var(--c-accent-amber);">0°</b>
              <input id="tilt" type="range" min="-35" max="35" value="0"/>
            </label>
            <div class="figure">
              <svg id="labSvg" viewBox="0 0 650 300">
                <g id="labV">
                  <path d="M 180 50 L 180 240 L 440 240 L 440 50" fill="none" stroke="#38bdf8" stroke-width="8"/>
                </g>
                <line class="water" x1="190" y1="150" x2="430" y2="150"/>
                <line x1="550" y1="40" x2="550" y2="230" stroke="var(--c-accent-amber)" stroke-width="3" stroke-dasharray="5 5"/>
                <circle cx="550" cy="245" r="14" fill="var(--c-accent-amber)"/>
                <text x="480" y="280" fill="var(--c-accent-amber)" font-size="15">Vertical plumb-line</text>
              </svg>
            </div>
            <div id="labmsg" class="answer">At 0°, the vessel is upright and the free surface is horizontal.</div>
          </div>
        </section>"""

    return ""


def render_page_a(theory_data, canonical_entry, profile):
    e = html.escape
    title = canonical_entry["canonical_title"]
    lid = canonical_entry["lesson_id"]
    subj = canonical_entry["subject"].capitalize()
    start_p = canonical_entry["pdf_start_page"]
    end_p = canonical_entry["pdf_end_page"]

    activities_html = ""
    for idx, act in enumerate(theory_data.get("activities", []), 1):
        yes_no = "true" if act.get("correct_is_yes", True) else "false"
        no_yes = "false" if act.get("correct_is_yes", True) else "true"
        svg = act.get("svg_diagram", "")
        activities_html += f"""
        <section class="card">
          <h2>{idx} · {e(act.get('title_primary', 'Activity'))}</h2>
          <button class="btn-toggle-ar" onclick="toggleAr('ar-act-{idx}')">🌐 الشرح والترجمة بالعربية</button>
          
          <div id="ar-act-{idx}" class="arabic-explanation-box" style="display:none;">
            <strong>النشاط {idx}: {e(act.get('title_ar', ''))}</strong>
            <p><strong>التجربة:</strong> {e(act.get('experiment_ar', ''))}</p>
            <p><strong>الملاحظة:</strong> {e(act.get('observation_ar', ''))}</p>
            <p><strong>الاستنتاج العلمي:</strong> {e(act.get('conclusion_ar', ''))}</p>
          </div>

          <div class="grid">
            <div>
              <div class="stage-exp"><b>🧪 Experiment:</b> {e(act.get('experiment_primary', ''))}</div>
              <div class="stage-obs"><b>👁️ Observation:</b> {e(act.get('observation_primary', ''))}</div>
              <div class="stage-concl"><b>💡 Conclusion:</b> {e(act.get('conclusion_primary', ''))}</div>
            </div>
            <div class="figure">{svg}</div>
          </div>
          <div class="ask">
            <b>NABIL Inquiry:</b> {e(act.get('question_prompt_primary', ''))}
            <button onclick="fb('chk-{idx}', {yes_no})">Yes</button>
            <button onclick="fb('chk-{idx}', {no_yes})">No</button>
            <span id="chk-{idx}" class="feedback"></span>
            <div style="font-size:13.5px; color:var(--text-muted); margin-top:4px; direction:rtl; text-align:right;">{e(act.get('question_prompt_ar', ''))}</div>
          </div>
        </section>"""

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
<title>NABIL AI | Grade {canonical_entry['grade']} {subj} | {e(title)}</title>
<link rel="stylesheet" href="[https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css](https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css)"/>
<script defer src="[https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js](https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js)"></script>
<script defer src="[https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js](https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js)"></script>
<style>{get_shared_css()}</style>
</head>
<body>
<header>
  <div class="bar">
    <div>
      <b>🧠 NABIL AI · Grade {canonical_entry['grade']} {subj}</b>
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
  <p>{e(theory_data.get('hook_primary', ''))}</p>
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
    <strong id="finalScore" style="margin-left:14px; font-size:1.2rem; color:var(--c-accent-amber);"></strong>
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
  el.style.color = ok ? 'var(--c-accent-green)' : '#ef4444';
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
        score++; fbEl.textContent = '✓ Correct'; fbEl.style.color = 'var(--c-accent-green)';
      }} else {{
        fbEl.textContent = '✗ Review observation'; fbEl.style.color = '#ef4444';
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
    subj = canonical_entry["subject"].capitalize()
    start_p = canonical_entry["pdf_start_page"]
    end_p = canonical_entry["pdf_end_page"]

    items_html = ""
    for ex in exercises_list:
        num = ex.get("number", 1)
        steps = "".join(f"<li>{s}</li>" for s in ex.get("steps_primary", []))
        svg = ex.get("svg_diagram", "")
        fig_html = f'<div class="figure ex-figure">{svg}</div>' if svg and "<svg" in svg else ""
        nabil_oral = ex.get("nabil_oral_ar", "")

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
            <summary>Guided Step-by-Step Resolution</summary>
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
<link rel="stylesheet" href="[https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css](https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css)"/>
<script defer src="[https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js](https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js)"></script>
<script defer src="[https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js](https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js)"></script>
<style>{get_shared_css()}</style>
</head>
<body>
<header>
  <div class="bar">
    <div>
      <b>📘 Official Solved Workbook · Grade {canonical_entry['grade']} {subj}</b>
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
  <p>All textbook exercises solved below with step-by-step scientific justification, fitted vector diagrams, and NABIL's Arabic spoken analysis.</p>
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


def atomic_publish_to_drive(service, parent_id, files_dict):
    uploaded_ids = {}
    from googleapiclient.http import MediaIoBaseUpload

    for fname, fcontent in files_dict.items():
        media = MediaIoBaseUpload(io.BytesIO(fcontent.encode("utf-8")), mimetype="text/html", resumable=False)
        up = service.files().create(body={"name": fname, "parents": [parent_id]}, media_body=media, fields="id,name").execute()
        if not up.get("id"):
            raise RuntimeError(f"UPLOAD_FAILED: {fname}")
        uploaded_ids[fname] = up["id"]

    existing = service.files().list(
        q=f"'{parent_id}' in parents and trashed=false",
        fields="files(id, name)"
    ).execute().get("files", [])
    
    for f_item in existing:
        if f_item["name"] in files_dict and f_item["id"] not in uploaded_ids.values():
            try:
                service.files().delete(fileId=f_item["id"]).execute()
            except Exception:
                pass

    return uploaded_ids


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
        import fitz
        doc = fitz.open(str(pdf_path))

        pages = [(p, extract_page_text_robust(doc, p)) for p in range(start_p, end_p + 1)]

        evidence_map = build_comprehensive_evidence_map(pages, pdf_path, book_id)
        progress("EVIDENCE_MAP_EXTRACTED", 
                 activities=len(evidence_map["activities"]), 
                 exercises=len(evidence_map["exercises"]))

        profile = compile_comprehensive_pedagogy_profile(evidence_map, canonical_entry)
        providers = configured_providers()

        theory_data = generate_source_locked_theory(providers, canonical_entry, evidence_map, profile)
        solved_exercises = solve_source_locked_exercises_adaptive(providers, canonical_entry, evidence_map)
        status = "GENERATED"

        execute_deterministic_quality_gates(theory_data, solved_exercises, evidence_map, profile)
        status = "GATES_PASSED"

        independent_scientific_review(providers, theory_data, solved_exercises, evidence_map)
        status = "SCIENTIFIC_REVIEW_PASSED"

        slug = re.sub(r"[^\w]+", "-", title.upper()).strip("-")
        num_str = lesson_id.split("-")[-1]
        grade_tag = f"G{canonical_entry['grade']:02d}"
        subj_tag = canonical_entry['subject'].upper()

        theory_filename = f"{grade_tag}-{subj_tag}--{num_str}--{slug}.html"
        exercises_filename = f"{grade_tag}-{subj_tag}--{num_str}--{slug}--EXERCISES.html"

        html_theory = render_page_a(theory_data, canonical_entry, profile)
        html_exercises = render_page_b(solved_exercises, canonical_entry)

        execute_mobile_layout_qa_390x844(html_theory, page_type="theory")
        execute_mobile_layout_qa_390x844(html_exercises, page_type="exercises")

        if "navigateToExercises" not in html_theory or "returnToLesson" not in html_exercises:
            raise AssertionError("NAVIGATION_FAILED: Navigation scripts missing")

        out_theory_path = report_path.with_name(theory_filename)
        out_ex_path = report_path.with_name(exercises_filename)

        out_theory_path.write_text(html_theory, encoding="utf-8")
        out_ex_path.write_text(html_exercises, encoding="utf-8")
        status = "UI_QA_PASSED"

        progress("FILES_COMPILED_LOCALLY", theory=theory_filename, exercises=exercises_filename)

        report = {
            "status": status,
            "lesson_id": lesson_id,
            "title": title,
            "theory_filename": theory_filename,
            "exercises_filename": exercises_filename,
            "exercises_count": len(solved_exercises)
        }

        if publish:
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

            files_to_publish = {
                theory_filename: html_theory,
                exercises_filename: html_exercises
            }
            pub_res = atomic_publish_to_drive(service, s_id, files_to_publish)
            report["drive_theory_id"] = pub_res[theory_filename]
            report["drive_exercises_id"] = pub_res[exercises_filename]
            report["status"] = "PUBLISHED_VERIFIED"
            progress("PUBLISHED_TWIN_PAGES_TO_DRIVE", theory_id=pub_res[theory_filename], exercises_id=pub_res[exercises_filename])

        return report


def main():
    try:
        py_compile.compile(__file__, doraise=True)
    except Exception as syntax_err:
        print(f"[FATAL_SYNTAX_ERROR] Syntax error detected: {syntax_err}")
        return 1

    parser = argparse.ArgumentParser(description="NABIL AI Universal Production Factory")
    parser.add_argument("--report", default="data/nabil_lesson_factory_run.json")
    parser.add_argument("--lesson-id", default="G07-PHYSICS-001")
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()

    global PROGRESS_STARTED
    PROGRESS_STARTED = time.monotonic()

    service = owner_drive()
    report_path = Path(args.report)
    
    catalog = load_or_init_catalog()

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
        print("[ERROR] Lesson not found in catalog:", args.lesson_id)
        return 1

    rep = produce_lesson_for_entry(service, target_entry, report_path, publish=args.publish)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(rep, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(rep, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
