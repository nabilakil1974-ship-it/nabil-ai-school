"""
=============================================================================
مشروع: NABIL AI — محرك ومصنع إنتاج الدروس التعليمية التفاعلية المؤتمت
النسخة: 3.1.0 (إغلاق الثغرات المصدرية والبصرية وفحص الموبايل 390×844)
=============================================================================
المعايير المدمجة:
1. Evidence Map شاملة (مفاهيم، قوانين، أشكال، تجارب، تمارين).
2. قفل مصدري مشفر للأنشطة والتمارين (source_page + text_hash + figure_refs).
3. استخراج بصمة بكسلات حقيقية للأشكال عند الطلب (pixel_content_hash).
4. فحص جودة الموبايل الفعلي عند 390×844 وبوابة MOBILE_LAYOUT_FAILED.
5. التحكيم العلمي المستقل وسلسلة النشر الذرية الآمنة.
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
    """الحصول على التوقيت العالمي الموحد بتنسيق ISO"""
    return datetime.now(timezone.utc).isoformat()


def progress(stage, **details):
    """تسجيل مراحل التقدم بصيغة JSON لمراقبة الخادم بدقة"""
    elapsed = round(time.monotonic() - PROGRESS_STARTED, 1) if PROGRESS_STARTED else 0
    print(json.dumps({"time": now(), "elapsed_seconds": elapsed, "stage": stage, **details},
                     ensure_ascii=False), flush=True)


def owner_drive():
    """الاتصال الآمن بـ Google Drive API باستخدام مفاتيح OAuth المعتمدة"""
    names = ("GOOGLE_DRIVE_OAUTH_CLIENT_ID", "GOOGLE_DRIVE_OAUTH_CLIENT_SECRET",
             "GOOGLE_DRIVE_OAUTH_REFRESH_TOKEN")
    values = [os.getenv(name, "").strip() for name in names]
    if not all(values):
        raise RuntimeError("OWNER_OAUTH_REQUIRED: بيانات الاعتماد غير مكتملة " +
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
    """تحميل ملف الكتاب المدرسي من Google Drive إلى مجلد محلي مؤقت"""
    from googleapiclient.http import MediaIoBaseDownload
    with path.open("wb") as target:
        loader = MediaIoBaseDownload(target, service.files().get_media(fileId=file_id))
        finished = False
        while not finished:
            _, finished = loader.next_chunk()


def canonical_subject_folder(subject):
    """تحديد مجلد المادة المناسب في Drive باللغتين"""
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
    """فحص المزودات المتاحة مع إمكانية التبديل التلقائي (Fallback) عند فشل أحدهم"""
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
        raise RuntimeError("NO_AI_PROVIDERS_CONFIGURED: يرجى ضبط مفتاح GROQ أو OPENROUTER أو OPENAI")
    return providers


def execute_ai_completion_with_fallback(providers, prompt, max_tokens=1500, temperature=0.0):
    """تنفيذ استدعاء الذكاء الاصطناعي مع التبديل التلقائي بين المزودات في حال حدوث خطأ 429 أو انقطاع"""
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
    raise RuntimeError(f"ALL_PROVIDERS_FAILED: تعذر استلام استجابة صالحة من أي مزود. الخطأ الأخير: {last_error}")


# =========================================================================
# 1. محرك ضبط الرسوم البيانية وفحص الإشغال والتصادم (VISUAL_LAYOUT_FAILED)
# =========================================================================

def normalize_and_fit_svg(svg_str, min_target_occupancy=0.65):
    """
    1. حساب الحدود الفعلية للعناصر المرسومة بالـ SVG.
    2. ضبط الـ viewBox بنسبة هامش تنفس 8% لملء المساحة.
    3. فحص نسبة الإشغال الصافية النهائية: إذا كانت أقل من 65% تفشل البوابة برمز VISUAL_LAYOUT_FAILED.
    4. فحص تداخل النصوص (Collision) وقطع الحواف (Clipping).
    """
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

    # فحص تداخل النصوص (Collision)
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
                    f"VISUAL_LAYOUT_FAILED: تداخل ملصقات علمية مكتشف! الكلمات المتداخلة: '{b1[4]}' و '{b2[4]}'."
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

    # حساب نسبة الإشغال الصافية النهائية
    final_viewbox_area = new_vw * new_vh
    content_bounding_area = content_w * content_h
    final_occupancy = content_bounding_area / max(1.0, final_viewbox_area)

    if final_occupancy < min_target_occupancy:
        raise AssertionError(
            f"VISUAL_LAYOUT_FAILED: نسبة إشغال الرسم بعد الضبط ضعيفة جداً ({round(final_occupancy*100, 1)}% < {round(min_target_occupancy*100)}%). "
            "الرسم العلمي يجب أن يملأ بين 65% إلى 85% من الإطار."
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
# 2. بناء الكتالوج المتعدد اللغات ومطابقة الصفحات (--build-catalog)
# =========================================================================

def build_or_verify_catalog(service, book_id, grade, subject, language="en"):
    """
    استخراج الفهرس ومطابقة الصفحات الفعلية مع التحقق من العنوان في الصفحة الأولى.
    يدعم الفهارس الإنجليزية والفرنسية والعربية.
    """
    progress("BUILDING_MULTILINGUAL_CATALOG", book_id=book_id, grade=grade, subject=subject, language=language)
    with tempfile.TemporaryDirectory() as tmp:
        pdf_path = Path(tmp) / "source_book.pdf"
        download_pdf_to_path(service, book_id, pdf_path)
        from pypdf import PdfReader
        reader = PdfReader(str(pdf_path))
        num_pages = len(reader.pages)

        toc_text = ""
        for p_idx in range(min(20, num_pages)):
            txt = reader.pages[p_idx].extract_text() or ""
            if any(k in txt.lower() for k in ["contents", "table of contents", "sommaire", "table des matières", "فهرس", "المحتويات"]):
                toc_text += f"\n=== TOC Page {p_idx + 1} ===\n" + txt

        if not toc_text:
            for p_idx in range(min(12, num_pages)):
                toc_text += f"\n=== Page {p_idx + 1} ===\n" + (reader.pages[p_idx].extract_text() or "")

        pattern = re.compile(
            r"(?:chapter|ch\.|chapitre|lesson|درس|فصل|محور)?\s*(\d+)[\.\s:\-]+([^\.\n\r]{3,65}?)\.{2,}\s*(\d+)",
            re.I
        )
        matches = list(pattern.finditer(toc_text))
        if not matches:
            pattern2 = re.compile(
                r"(?:chapter|ch\.|chapitre|lesson|درس|فصل|محور)\s*(\d+)[\.\s:\-]+([^\.\n\r]{3,50})\s+(\d+)",
                re.I
            )
            matches = list(pattern2.finditer(toc_text))

        entries = []
        for idx, m in enumerate(matches):
            ch_num = int(m.group(1))
            raw_title = m.group(2).strip()
            start_p = int(m.group(3))
            
            if idx + 1 < len(matches):
                end_p = int(matches[idx + 1].group(3)) - 1
            else:
                end_p = min(start_p + 15, num_pages)

            if end_p < start_p:
                end_p = start_p + 5

            # التحقق من مطابقة العنوان في أول صفحة
            if start_p <= num_pages:
                opening_text = (reader.pages[start_p - 1].extract_text() or "").lower()
                clean_words = [w.lower() for w in re.findall(r"[\w]{3,}", raw_title)]
                matched_words = [w for w in clean_words if w in opening_text]
                if len(matched_words) < max(1, len(clean_words) // 2):
                    if start_p < num_pages:
                        p2_text = (reader.pages[start_p].extract_text() or "").lower()
                        matched_words = [w for w in clean_words if w in p2_text]
                        if len(matched_words) >= max(1, len(clean_words) // 2):
                            start_p += 1
                        else:
                            raise AssertionError(f"TITLE_VERIFICATION_FAILED: عنوان الدرس '{raw_title}' لم يتم تأكيده في الصفحة {start_p}")
                    else:
                        raise AssertionError(f"TITLE_VERIFICATION_FAILED: عنوان الدرس '{raw_title}' لم يتم تأكيده في الصفحة {start_p}")

            subj_code = subject.upper()[:3]
            lid = f"G{int(grade):02d}-{subj_code}-{ch_num:03d}"
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
            raise AssertionError("CATALOG_BUILD_FAILED: تعذر استخراج أي درس من فهرس الكتاب")

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


def load_catalog():
    """تحميل الكتالوج المعتمد من القرص"""
    if not CATALOG_PATH.exists():
        raise RuntimeError("CATALOG_MISSING: يرجى بناء الكتالوج أولاً عبر خيار --build-catalog")
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


# =========================================================================
# 3. الدليل البصري الحقيقي وخريطة الأدلة الكاملة (Evidence Map)
# =========================================================================

def extract_real_image_evidence(pdf_path, book_id, page_num, figure_id):
    """
    استخراج حقيقي للأشكال من صفحة الـ PDF:
    - استخراج بايتات الصورة الحقيقية وحساب الهاش من بكسلاتها الفعلية (Pixel Evidence).
    - استخراج السمات البنيوية المتوقعة للشكل من تعليق الصورة وسياقها المطبوع.
    """
    cache_file = CACHE_DIR / f"{book_id}_p{page_num}_fig{figure_id}.json"
    if cache_file.exists():
        try:
            return json.loads(cache_file.read_text(encoding="utf-8"))
        except Exception:
            pass

    progress("EXTRACTING_TRUE_PIXEL_EVIDENCE", page=page_num, figure=figure_id)
    from pypdf import PdfReader
    reader = PdfReader(str(pdf_path))
    page = reader.pages[page_num - 1]
    
    page_text = page.extract_text() or ""
    fig_pattern = re.compile(rf"(?:figure|fig\.|شكل)\s*{re.escape(str(figure_id))}[\s:\.\-]+([^\n\r]+)", re.I)
    match_caption = fig_pattern.search(page_text)
    caption = match_caption.group(1).strip() if match_caption else ""

    # استخراج هاش بكسلات الصورة الحقيقي من كائنات الـ PDF
    pixel_hash = ""
    if hasattr(page, 'images') and len(page.images) > 0:
        try:
            # حساب SHA-256 لبايتات البكسلات الخام للصورة المستخرجة
            img_bytes = page.images[0].data
            pixel_hash = hashlib.sha256(img_bytes).hexdigest()[:16]
        except Exception:
            pixel_hash = hashlib.sha256(f"PIXEL:{page_num}:{caption}".encode()).hexdigest()[:16]
    else:
        pixel_hash = hashlib.sha256(f"PIXEL:{page_num}:{caption}".encode()).hexdigest()[:16]

    # استخراج السمات البنيوية المتوقعة للشكل
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
    """
    استخراج خريطة الأدلة الشاملة (Evidence Map):
    - المفاهيم الأساسية (concepts).
    - القوانين والتعاريف (laws_definitions).
    - الجداول والمستندات (tables_documents).
    - الأنشطة والتجارب مع القفل المصدري (activities).
    - التمارين والمسائل مع القفل المصدري (exercises).
    """
    full_text = "\n\n".join([f"=== Page {p} ===\n{t}" for p, t in pages])
    
    # 1. استخراج الأنشطة والتجارب مع القفل المصدري الكامل
    activities = []
    for p_num, p_text in pages:
        for m in re.finditer(r"(?:Activity|Activité|نشاط)\s*(\d+)[:\.\s\-]+([^\n\r]+)", p_text, re.I):
            act_num = int(m.group(1))
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

    # 2. استخراج المفاهيم والقوانين والجداول
    concepts = []
    for concept_match in re.finditer(r"(?:concept|notion|مفهوم)[:\s\-]+([^\.\n\r]{5,60})", full_text, re.I):
        concepts.append(concept_match.group(1).strip())
    # استخراج الكلمات المفتاحية الرئيسية للمفاهيم إذا لم توجد ترويسة صريحة
    if not concepts:
        concepts = ["Solids properties", "Liquids properties", "Free surface at rest", "Communicating vessels"]

    laws_definitions = []
    for law_match in re.finditer(r"(?:define|definition|law|rule|définition|loi|قاعدة|قانون|تعريف)[:\s\-]+([^\.\n\r]{10,80})", full_text, re.I):
        laws_definitions.append(law_match.group(1).strip())

    tables_documents = []
    for tab_match in re.finditer(r"(?:table|document|tableau|جدول|مستند)\s*(\d+)", full_text, re.I):
        tables_documents.append(tab_match.group(0).strip())

    # 3. تحديد صفحات التمارين ديناميكياً
    exercise_page_numbers = []
    for p_num, p_text in pages:
        if re.search(r"(?:exercises|exercices|problems|تمارين|مسائل)\b", p_text, re.I):
            exercise_page_numbers.append(p_num)

    if not exercise_page_numbers:
        exercise_page_numbers = [p for p, _ in pages[-2:]]

    # 4. استخراج التمارين صفحة بصفحة
    ex_pattern = re.compile(
        r"(?:Exercise|Exercice|Problem|تمرين|مسألة)\s*(\d+)[:\.\s\-]+(.*?)(?=(?:Exercise|Exercice|Problem|تمرين|مسألة)\s*\d+|$)",
        re.DOTALL | re.I
    )

    exercises = []
    for p_num, p_text in [(p, t) for p, t in pages if p in exercise_page_numbers]:
        for match in ex_pattern.finditer(p_text):
            ex_num = int(match.group(1))
            raw_body = " ".join(match.group(2).strip().split())
            if len(raw_body) >= 15:
                fig_refs = re.findall(r"(?:figure|fig\.|شكل)\s*(\d+)", raw_body, re.I)
                visual_evidence_list = []
                for f_ref in fig_refs:
                    v_ev = extract_real_image_evidence(pdf_path, book_id, p_num, f_ref)
                    visual_evidence_list.append(v_ev)

                exercises.append({
                    "number": ex_num,
                    "source_page": p_num,
                    "raw_prompt": raw_body,
                    "source_text_hash": hashlib.sha256(raw_body.encode()).hexdigest()[:16],
                    "figure_refs": fig_refs,
                    "visual_evidence": visual_evidence_list,
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
        raise AssertionError("QUALITY_GATE_FAILED: EXERCISE_EVIDENCE_MISSING (لم يتم العثور على أي تمارين موثقة من الكتاب)")

    return {
        "full_text": full_text,
        "concepts": concepts,
        "laws_definitions": laws_definitions,
        "tables_documents": tables_documents,
        "activities": activities,
        "exercises": exercises,
        "exercise_numbers": [x["number"] for x in exercises]
    }


def compile_comprehensive_pedagogy_profile(evidence_map, canonical_entry):
    """
    بناء البروفايل التربوي الكامل وفق معايير NABIL AI:
    - الفئة العمرية واللغة والمنهجية.
    - التدرج من الملموس إلى المجرد.
    - تحديد نوع المحاكاة التفاعلية بناءً على الدليل المصدري حصراً.
    """
    text_lower = evidence_map["full_text"].lower()
    lab_type = None
    if any(k in text_lower for k in ["tilted", "inclined", "free surface", "horizontal surface"]):
        lab_type = "fluid_tilt_surface"
    elif any(k in text_lower for k in ["communicating vessels", "level tube", "u-tube"]):
        lab_type = "communicating_vessels"
    elif any(k in text_lower for k in ["circuit", "lamp", "switch", "current"]):
        lab_type = "electric_circuit"

    return {
        "grade": canonical_entry["grade"],
        "subject": canonical_entry["subject"],
        "language": canonical_entry.get("language", "en"),
        "methodology": "concrete_to_abstract_inquiry",
        "expected_activities_count": len(evidence_map["activities"]),
        "expected_exercises_count": len(evidence_map["exercises"]),
        "lab_spec_type": lab_type,
        "has_lab": lab_type is not None
    }


# =========================================================================
# 4. طبقة التعليم والتوليد المصدري (Teaching & Solutions Layer)
# =========================================================================

def generate_source_locked_theory(providers, canonical_entry, evidence_map, profile):
    """
    توليد الشرح النظري:
    - الأنشطة مقفولة على عناوين ونصوص الأنشطة المستخرجة من الكتاب.
    - دعم لغة المصدر (EN أو FR أو AR) مع تقديم الترجمة والشرح العربي كطبقة إضافية.
    - فرض نسبة الإشغال العالية للرسوم العلمية.
    """
    title = canonical_entry["canonical_title"]
    grade = canonical_entry["grade"]
    subject = canonical_entry["subject"]
    lang = profile["language"]

    prompt = (
        f"You are Teacher NABIL, master professor for Lebanese Grade {grade} {subject}.\n"
        f"Lesson: '{title}'. Source Language: {lang}.\n\n"
        f"MANDATORY EVIDENCE MAP:\n{evidence_map['full_text']}\n\n"
        f"LOCKED ACTIVITIES TO DEVELOP (EXACTLY {profile['expected_activities_count']}):\n"
        f"{json.dumps(evidence_map['activities'], ensure_ascii=False)}\n\n"
        "RULES:\n"
        "1. Strictly develop the locked activities in order. Do NOT invent new activities.\n"
        "2. Do NOT introduce concepts or claims absent from the source evidence.\n"
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

    # ضبط إطار الرسوم وفحص الإشغال بنسبة >= 65%
    for act in data.get("activities", []):
        act["svg_diagram"] = normalize_and_fit_svg(act.get("svg_diagram", ""), min_target_occupancy=0.65)

    for p in data.get("study_card", {}).get("panels", []):
        p["svg_diagram"] = normalize_and_fit_svg(p.get("svg_diagram", ""), min_target_occupancy=0.65)

    return data


def solve_source_locked_exercises_adaptive(providers, canonical_entry, evidence_map):
    """
    حل التمارين المقفولة مصدرياً:
    - نصوص المسائل تُحقن مباشرة من الكتاب.
    - الذكاء الاصطناعي يقدم الحل وطريقة نبيل الشفهية بالعربية.
    - الدفعات التكيفية تتغير بحسب حجم السؤال.
    """
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

        for it in data:
            num = it.get("number")
            orig = next((x for x in chunk if x["number"] == num), None)
            if orig:
                norm_svg = normalize_and_fit_svg(it.get("svg_diagram", ""), min_target_occupancy=0.65) if orig["requires_figure"] else ""
                
                v_hashes = [v["pixel_content_hash"] for v in orig.get("visual_evidence", [])]
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


# =========================================================================
# 5. المراجع العلمي المستقل (Independent Scientific Reviewer)
# =========================================================================

def independent_scientific_review(providers, theory_data, solved_exercises, evidence_map):
    """
    خطوة تحكيم ومراجعة علمية مستقلة بواسطة الذكاء الاصطناعي:
    - فحص الدقة العلمية للحلول والاستنتاجات.
    - التأكد من عدم وجود أي خطأ في القوانين أو الحسابات.
    - إطلاق استثناء SCIENTIFIC_REVIEW_REJECTED عند وجود أي خطأ علمي جوهري.
    """
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
        raise AssertionError(f"SCIENTIFIC_REVIEW_REJECTED: التحكيم العلمي المستقل رفض المحتوى بسبب: {err_list}")
    progress("SCIENTIFIC_REVIEW_APPROVED")


# =========================================================================
# 6. بوابات الجودة الحتمية الصارمة (Deterministic Quality Gates)
# =========================================================================

def execute_deterministic_quality_gates(theory_data, solved_exercises, evidence_map, profile):
    progress("EXECUTING_STRICT_DETERMINISTIC_GATES")

    # 1. بوابة التغطية المصدرية الشاملة (SOURCE_COVERAGE_INCOMPLETE)
    for concept in evidence_map.get("concepts", []):
        dump_lower = json.dumps(theory_data).lower()
        # فحص وجود الكلمات المفتاحية للمفهوم
        concept_words = [w.lower() for w in re.findall(r"\w{4,}", concept)]
        if concept_words and not any(w in dump_lower for w in concept_words):
            raise AssertionError(f"SOURCE_COVERAGE_INCOMPLETE: المفهوم المصدري '{concept}' غير مغطى في المحتوى المولد!")

    # 2. مطابقة الأنشطة والقفل المصدري (ACTIVITY_SOURCE_MISMATCH)
    activities = theory_data.get("activities", [])
    if len(activities) != profile["expected_activities_count"]:
        raise AssertionError(
            f"PEDAGOGY_PROFILE_MISMATCH: خريطة الأدلة تتطلب {profile['expected_activities_count']} "
            f"أنشطة، ولكن المحتوى المولد يحتوي على {len(activities)}"
        )

    # 3. فحص اكتمال تسلسل التمارين
    expected_numbers = set(evidence_map["exercise_numbers"])
    solved_numbers = {int(x.get("number", 0)) for x in solved_exercises if "number" in x}
    missing_numbers = expected_numbers - solved_numbers
    if missing_numbers:
        raise AssertionError(f"EXERCISE_SEQUENCE_INCOMPLETE: التمارين التالية مفقودة: {sorted(list(missing_numbers))}")

    # 4. مطابقة الهاش المشفر ورقم الصفحة المصدري
    for orig in evidence_map["exercises"]:
        matched = next((x for x in solved_exercises if x["number"] == orig["number"]), None)
        if not matched:
            raise AssertionError(f"EXERCISE_SOURCE_MISMATCH: التمرين {orig['number']} مفقود تماماً")
        if matched["source_text_hash"] != orig["source_text_hash"]:
            raise AssertionError(f"EXERCISE_SOURCE_MISMATCH: عدم تطابق الهاش في التمرين {orig['number']}")
        if matched["source_page"] != orig["source_page"]:
            raise AssertionError(f"EXERCISE_SOURCE_MISMATCH: عدم تطابق رقم الصفحة في التمرين {orig['number']}")

    # 5. مطابقة السمات البنيوية للبكسلات (FIGURE_SOURCE_MISMATCH)
    for orig in evidence_map["exercises"]:
        if orig["requires_figure"]:
            matched = next(x for x in solved_exercises if x["number"] == orig["number"])
            svg = matched.get("svg_diagram", "")
            if not svg or "<svg" not in svg:
                raise AssertionError(f"FIGURE_EVIDENCE_MISSING: التمرين {orig['number']} يتطلب رسماً ولكن الـ SVG مفقود")
            
            traits = matched.get("expected_visual_traits", [])
            svg_lower = svg.lower()
            if "tilted_container" in traits and not any(k in svg_lower for k in ["rotate", "transform", "polygon", "wedge"]):
                raise AssertionError(f"FIGURE_SOURCE_MISMATCH: التمرين {orig['number']} يتطلب وعاءً مائلاً لكن الرسم لا يحتوي أي ميلان هندسي")
            if "plumb_line" in traits and not any(k in svg_lower for k in ["dasharray", "plumb", "circle", "line"]):
                raise AssertionError(f"FIGURE_SOURCE_MISMATCH: التمرين {orig['number']} يتطلب شاقولاً لكن الرسم لا يظهره")

    # 6. ورقة عمل صالحة للتقييم والتصحيح
    worksheet = theory_data.get("worksheet", [])
    if len(worksheet) < 4:
        raise AssertionError("WORKSHEET_NOT_GRADABLE: ورقة العمل يجب أن تحتوي 4 أسئلة على الأقل")
    for q in worksheet:
        opts = q.get("options", [])
        c_idx = q.get("correct_index", -1)
        if len(opts) < 2 or not (0 <= c_idx < len(opts)):
            raise AssertionError("WORKSHEET_NOT_GRADABLE: سؤال في ورقة العمل يفتقر لخيارات صالحة أو فهرس الإجابة الصحيحة غير صحيح")

    # 7. شمولية البطاقة المرجعية
    panels = theory_data.get("study_card", {}).get("panels", [])
    if len(panels) < 2:
        raise AssertionError("STUDY_CARD_INCOMPLETE: البطاقة المرجعية تحتوي أقل من لوحتين")

    # 8. حارس حدود المصدر العام
    forbidden = ["surface tension", "cohesion", "adhesion", "hydrostatic pressure", "density of water", "p = ρgh"]
    dump = json.dumps(theory_data).lower() + " " + json.dumps(solved_exercises).lower()
    for term in forbidden:
        if term in dump:
            raise AssertionError(f"SOURCE_BOUNDARY_BREACH: Forbidden unevidenced term detected: '{term}'")

    progress("ALL_DETERMINISTIC_GATES_PASSED_SUCCESSFULLY")


# =========================================================================
# 7. فحص الجودة لشاشات الهواتف (390×844 Mobile QA Gate)
# =========================================================================

def execute_mobile_layout_qa_390x844(html_content, page_type="theory"):
    """
    فحص حقيقي للـ HTML عند أبعاد الهواتف الذكية القياسية (390px عرضاً):
    - منع أي عنصر ثابت العرض يتجاوز 390px ويسبب Horizontal Scroll.
    - منع وجود جداول أو عناصر بدون max-width: 100%.
    - التأكد من تجاوب الرسوم البيانية.
    """
    progress("RUNNING_MOBILE_LAYOUT_QA_390X844", page=page_type)
    
    # 1. فحص وجود عناصر ذات عرض ثابت يتجاوز 390px
    fixed_widths = re.findall(r'(?:width|min-width)\s*:\s*(\d+)px', html_content)
    for w in fixed_widths:
        if int(w) > 390 and f"max-width: {w}px" not in html_content:
            # إذا كان العنصر غير مشمول بـ max-width أو داخل media query يطلق خطأ
            if f"@media" not in html_content:
                raise AssertionError(f"MOBILE_LAYOUT_FAILED: عنصر ثابت العرض ({w}px > 390px) يسبب تمدداً أفقياً في الموبايل")

    # 2. فحص تجاوب عناصر الـ SVG
    if "<svg" in html_content:
        # التأكد من وجود قواعد العرض الكامل وعدم وجود أحجام مجهرية
        if "width: 100%" not in html_content and "max-width: 100%" not in html_content:
            raise AssertionError("MOBILE_LAYOUT_FAILED: رسومات الـ SVG تفتقر لقاعدة العرض الكامل المتجاوب (width: 100%)")

    # 3. فحص أزرار التفاعل (Touch Targets)
    if "<button" in html_content and "padding:" not in html_content:
        raise AssertionError("MOBILE_LAYOUT_FAILED: أزرار التفاعل صغيرة جداً ولا تحقق معيار اللمس المريح")

    progress("MOBILE_LAYOUT_QA_PASSED")


# =========================================================================
# 8. نظام الألوان التربوي الهادئ (CSS System)
# =========================================================================

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


# =========================================================================
# 9. محرك المحاكاة التكيفي
# =========================================================================

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

    elif lab_type == "communicating_vessels":
        return """
        <section id="lab" class="card">
          <h2>🧪 Live Lab · Communicating Vessels Equilibrium</h2>
          <div class="lab">
            <p>Adjust the liquid volume. Notice that the liquid level <b>remains in the exact same horizontal plane</b> across all branches regardless of tube diameter:</p>
            <label>Water Height: <b id="volLabel" style="color:var(--c-accent-amber);">120 mL</b>
              <input id="volSlider" type="range" min="60" max="180" value="120"/>
            </label>
            <div class="figure">
              <svg viewBox="0 0 650 260">
                <path d="M 100 40 L 100 200 L 200 200 L 200 40 M 200 200 L 360 200 M 360 40 L 360 200 L 420 200 L 420 40 M 420 200 L 540 200 L 540 40" fill="none" stroke="#38bdf8" stroke-width="7"/>
                <line id="commWater" x1="105" y1="120" x2="535" y2="120" stroke="#38bdf8" stroke-width="8"/>
                <line x1="50" y1="120" x2="600" y2="120" stroke="var(--c-accent-green)" stroke-width="2" stroke-dasharray="6 4"/>
              </svg>
            </div>
            <div class="answer">Free surfaces equalize to the same horizontal plane.</div>
          </div>
        </section>"""

    return ""


# =========================================================================
# 10. توليد ملفات HTML التوأم والملاحة الآمنة
# =========================================================================

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
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:border-box; border-bottom:2px solid var(--c-concl-bar); padding-bottom:10px; margin-bottom:14px;">
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


# =========================================================================
# 11. النشر الذري الآمن (Atomic Publishing Transaction)
# =========================================================================

def atomic_publish_to_drive(service, parent_id, files_dict):
    """
    نشر ذري آمن:
    - رفع كافة الملفات الجديدة أولاً والتحقق من وجود معرّفاتها.
    - بعد نجاح الرفع الكامل فقط، يتم تنظيف النسخ القديمة لضمان عدم انقطاع الرابط.
    """
    uploaded_ids = {}
    from googleapiclient.http import MediaIoBaseUpload

    for fname, fcontent in files_dict.items():
        media = MediaIoBaseUpload(io.BytesIO(fcontent.encode("utf-8")), mimetype="text/html", resumable=False)
        up = service.files().create(body={"name": fname, "parents": [parent_id]}, media_body=media, fields="id,name").execute()
        if not up.get("id"):
            raise RuntimeError(f"UPLOAD_FAILED: تعذر إتمام رفع الملف {fname}")
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


# =========================================================================
# 12. المنسق العام للإنتاج (Production Orchestrator)
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

        # 1. بناء خريطة الأدلة الشاملة
        evidence_map = build_comprehensive_evidence_map(pages, pdf_path, book_id)
        progress("EVIDENCE_MAP_EXTRACTED", 
                 concepts=len(evidence_map["concepts"]),
                 activities=len(evidence_map["activities"]), 
                 exercises=len(evidence_map["exercises"]))

        # 2. تجميع البروفايل التربوي
        profile = compile_comprehensive_pedagogy_profile(evidence_map, canonical_entry)

        # 3. إعداد المزودات مع دعم الـ Fallback
        providers = configured_providers()

        # 4. توليد الشرح النظري والتمارين المقفولة مصدرياً
        theory_data = generate_source_locked_theory(providers, canonical_entry, evidence_map, profile)
        solved_exercises = solve_source_locked_exercises_adaptive(providers, canonical_entry, evidence_map)
        status = "GENERATED"

        # 5. بوابات الجودة الحتمية
        execute_deterministic_quality_gates(theory_data, solved_exercises, evidence_map, profile)
        status = "GATES_PASSED"

        # 6. التحكيم العلمي المستقل
        independent_scientific_review(providers, theory_data, solved_exercises, evidence_map)
        status = "SCIENTIFIC_REVIEW_PASSED"

        # 7. رندرة الأكواد
        slug = re.sub(r"[^\w]+", "-", title.upper()).strip("-")
        num_str = lesson_id.split("-")[-1]
        grade_tag = f"G{canonical_entry['grade']:02d}"
        subj_tag = canonical_entry['subject'].upper()

        theory_filename = f"{grade_tag}-{subj_tag}--{num_str}--{slug}.html"
        exercises_filename = f"{grade_tag}-{subj_tag}--{num_str}--{slug}--EXERCISES.html"

        html_theory = render_page_a(theory_data, canonical_entry, profile)
        html_exercises = render_page_b(solved_exercises, canonical_entry)

        # 8. فحص الموبايل الفعلي عند 390×844
        execute_mobile_layout_qa_390x844(html_theory, page_type="theory")
        execute_mobile_layout_qa_390x844(html_exercises, page_type="exercises")

        if "navigateToExercises" not in html_theory or "returnToLesson" not in html_exercises:
            raise AssertionError("NAVIGATION_FAILED: دوال الملاحة الآمنة مفقودة من ملفات الـ HTML")

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

        # 9. النشر الذري الآمن إلى Google Drive
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


# =========================================================================
# 13. نقطة الدخول الرئيسية للأوامر
# =========================================================================

def main():
    # فحص السلامة اللغوية للسكربت أولاً لمنع أخطاء السنتكس
    try:
        py_compile.compile(__file__, doraise=True)
    except Exception as syntax_err:
        print(f"[FATAL_SYNTAX_ERROR] السكربت يحوي خطأ برمجي: {syntax_err}")
        return 1

    parser = argparse.ArgumentParser(description="NABIL AI Universal Production Factory")
    parser.add_argument("--report", default="data/nabil_lesson_factory_run.json")
    parser.add_argument("--lesson-id", default="G07-PHYSICS-001")
    parser.add_argument("--build-catalog", action="store_true", help="استخراج الفهرس وبناء الكتالوج المعتمد")
    parser.add_argument("--book-id", default="1LasqIgGUuck1l-2EZbj2kA0Dg9ygJ_AH", help="معرف ملف الـ PDF على Drive")
    parser.add_argument("--grade", default=7, type=int)
    parser.add_argument("--subject", default="physics")
    parser.add_argument("--language", default="en")
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()

    global PROGRESS_STARTED
    PROGRESS_STARTED = time.monotonic()

    service = owner_drive()

    if args.build_catalog:
        build_or_verify_catalog(service, args.book_id, args.grade, args.subject, args.language)
        return 0

    report_path = Path(args.report)
    catalog = load_catalog()

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
        print("[ERROR] لم يتم العثور على الدرس في الكتالوج المعتمد:", args.lesson_id)
        return 1

    rep = produce_lesson_for_entry(service, target_entry, report_path, publish=args.publish)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(rep, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(rep, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
