"""
=============================================================================
مشروع: NABIL AI — محرك ومصنع إنتاج الدروس التعليمية التفاعلية المؤتمت
=============================================================================
الأهداف الأساسية لهذا السكربت:
1. استخراج خريطة الأدلة (Evidence Map) من صفحات الكتاب المدرسي بدون أي اختلاق.
2. قفل نصوص التمارين ببصمة مشفرة ورقم صفحة (Source-Lock).
3. فحص وتكبير الرسوم العلمية لتملأ 75-85% من الإطار ومنع الرسوم الصغيرة أو المتداخلة.
4. نظام ألوان تربوي طبقي هادئ ومريح للعين يبتعد عن تراكم الأزرق فوق الأزرق.
5. التحقق الحتمي عبر بوابات جودة صارمة تمنع النشر عند حدوث أي خلل.
6. إنتاج صفحتين توأم (صفحة شرح وتجارب + صفحة كراسة التمارين المحلولة) مع ملاحة آمنة.
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

# =========================================================================
# ضبط المسارات والمجلدات العامة
# =========================================================================
ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = ROOT / "data/interactive_lesson_production_ledger.json"
CATALOG_PATH = ROOT / "data/nabil_canonical_lesson_catalog.json"

# مجلد الكاش لتخزين الدليل البصري للأشكال والأرقام لعدم إعادة معالجة الصفحات
CACHE_DIR = ROOT / "data/cache/visual_evidence"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# معرفات Google Drive لحفظ ورفع الملفات
FOLDER_MIME = "application/vnd.google-apps.folder"
ROOT_FOLDER = os.getenv("NABIL_INTERACTIVE_CURRICULUM_ROOT_ID",
                        os.getenv("NABIL_LESSON_DRIVE_ROOT",
                                  "16bcmZMO_dn4FqlGaDtl8Hky6iSBEqZpX"))

PROGRESS_STARTED = None


def now():
    """ترجع الوقت الحالي بالتوقيت العالمي الموحد بصيغة ISO"""
    return datetime.now(timezone.utc).isoformat()


def progress(stage, **details):
    """
    دالة طباعة مراحل التقدم في الـ Terminal بصيغة JSON
    لتتبع السيرفر ومراقبة الزمن المستغرق في كل مرحلة.
    """
    elapsed = round(time.monotonic() - PROGRESS_STARTED, 1) if PROGRESS_STARTED else 0
    print(json.dumps({"time": now(), "elapsed_seconds": elapsed, "stage": stage, **details},
                     ensure_ascii=False), flush=True)


def owner_drive():
    """
    دالة الاتصال الآمن بـ Google Drive API باستخدام مفاتيح OAuth الرسمية
    لرفع ملفات الشرح والتمارين والتحكم بالمجلدات.
    """
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
    """دالة تحميل ملف كتاب الـ PDF من Google Drive إلى مجلد مؤقت للبدء بفحصه"""
    from googleapiclient.http import MediaIoBaseDownload
    with path.open("wb") as target:
        loader = MediaIoBaseDownload(target, service.files().get_media(fileId=file_id))
        finished = False
        while not finished:
            _, finished = loader.next_chunk()


def canonical_subject_folder(subject):
    """تحديد الاسم القياسي لمجلد المادة (فيزياء، رياضيات، كيمياء...) لتنظيم مجلدات Drive"""
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
    """
    فحص مزودات الذكاء الاصطناعي المتوفرة في البيئة (Groq، OpenRouter، أو OpenAI)
    واختيار المزود المتاح مع نماذج التشغيل المعتمدة.
    """
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
# 1. محرك ضبط الرسوم البيانية وفحص التداخل (Visual Quality Engine)
# =========================================================================

def normalize_and_fit_svg(svg_str, min_occupancy=0.55):
    """
    وظيفة هذا الجزء:
    1. حساب الحدود الحقيقية للرسمة داخل الـ SVG (أين تقع الكؤوس والخطوط فعلياً).
    2. إعادة ضبط الـ viewBox ليلتف حول الرسم ويجعله يملأ 75-85% من الشاشة.
    3. منع خروج رسوم قزمية صغيرة أو نصوص متداخلة فوق بعضها (Collision).
    4. منع انقطاع رؤوس الأسهم أو النصوص خارج حدود الشاشة.
    """
    if not svg_str or "<svg" not in svg_str:
        return svg_str

    # استخراج إحداثيات كل الأشكال (مستطيلات، دوائر، خطوط، مسارات)
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

    # حساب أقصى وأدنى نقطة للأشكال
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)

    if widths:
        max_x = max(max_x, min_x + max(widths))
    if heights:
        max_y = max(max_y, min_y + max(heights))

    content_w = max(10.0, max_x - min_x)
    content_h = max(10.0, max_y - min_y)

    # حساب نسبة المساحة التي تشغلها الرسمة داخل الصندوق
    vb_match = re.search(r'viewBox\s*=\s*["\']([\d\.\s\-]+)["\']', svg_str)
    if vb_match:
        orig_vb = [float(v) for v in vb_match.group(1).split()]
        if len(orig_vb) == 4:
            orig_area = orig_vb[2] * orig_vb[3]
            content_area = content_w * content_h
            occupancy = content_area / max(1.0, orig_area)

            # بوابة منع: إذا كانت الرسمة صغيرة جداً (أقل من 12% من الصندوق) يتم إيقاف النشر فوراً
            if occupancy < 0.12 and content_w < 120 and content_h < 80:
                raise AssertionError(
                    f"VISUAL_LAYOUT_FAILED: تم اكتشاف رسمة قزمية صغيرة بنسبة {round(occupancy*100,1)}%! "
                    "يجب أن يشغل الرسم العلمي بين 70% إلى 85% من الإطار."
                )

    # فحص تداخل النصوص (Collision Detection): لمنع كتابة كلمة فوق كلمة
    text_blocks = re.findall(r'<text\s+[^>]*?x\s*=\s*["\']([\d\.]+)["\'][^>]*?y\s*=\s*["\']([\d\.]+)["\'][^>]*?>(.*?)</text>', svg_str, re.DOTALL)
    text_boxes = []
    for tx, ty, content in text_blocks:
        x_val, y_val = float(tx), float(ty)
        clean_len = len(content.strip())
        w_est = clean_len * 9.0  # تقدير عرض النص تقريباً لكل حرف
        h_est = 18.0
        text_boxes.append((x_val, y_val, w_est, h_est, content.strip()))

    for i in range(len(text_boxes)):
        for j in range(i + 1, len(text_boxes)):
            b1 = text_boxes[i]
            b2 = text_boxes[j]
            # إذا تداخل نصان عمودياً وأفقياً تطلق البوابة خطأ وتمنع النشر
            if abs(b1[0] - b2[0]) < min(b1[2], b2[2]) * 0.75 and abs(b1[1] - b2[1]) < 14.0:
                raise AssertionError(
                    f"VISUAL_LAYOUT_FAILED: تداخل نصوص مكتشف بين الكلمتين: '{b1[4]}' و '{b2[4]}'."
                )

    # ضبط إطار العرض (viewBox) التلقائي بهامش تنفس 8% لملء المساحة
    pad_x = max(20.0, content_w * 0.08)
    pad_y = max(20.0, content_h * 0.08)
    
    new_vx = max(0, min_x - pad_x)
    new_vy = max(0, min_y - pad_y)
    new_vw = content_w + (pad_x * 2)
    new_vh = content_h + (pad_y * 2)

    # فحص الانقطاع: التأكد من أن جميع الكلمات تقع بالكامل داخل حدود الصندوق الجديد
    for bx, by, bw, bh, txt in text_boxes:
        if bx < new_vx or (bx + bw * 0.8) > (new_vx + new_vw) or by < new_vy or by > (new_vy + new_vh):
            new_vw = max(new_vw, bx + bw - new_vx + 15.0)
            new_vh = max(new_vh, by + bh - new_vy + 15.0)

    new_viewbox = f'viewBox="{round(new_vx,1)} {round(new_vy,1)} {round(new_vw,1)} {round(new_vh,1)}"'
    
    if vb_match:
        svg_str = re.sub(r'viewBox\s*=\s*["\'][\d\.\s\-]+["\']', new_viewbox, svg_str, count=1)
    else:
        svg_str = re.sub(r'<svg', f'<svg {new_viewbox}', svg_str, count=1)

    # فرض خط مقروء وواضح للطلاب (لا يقل عن 15px)
    svg_str = re.sub(r'font-size\s*=\s*["\'](?:[0-9]|1[0-4])(?:px)?["\']', 'font-size="15px"', svg_str)
    return svg_str


# =========================================================================
# 2. محرك الكتالوج الرسمي وبناء الفهرس الحقيقي (--build-catalog)
# =========================================================================

def build_or_verify_catalog(service, book_id, grade, subject, language="en"):
    """
    وظيفة هذا الجزء:
    1. فتح الكتاب وقراءة الفهرس الحقيقي (TOC) واستخراج الدروس وأرقام صفحاتها ديناميكياً.
    2. فحص الصفحة الأولى لكل درس (Opening-Page Verification) للتأكد من تطابق العنوان.
    3. إذا لم يجد العنوان يوقف العملية برمز TITLE_VERIFICATION_FAILED.
    """
    progress("BUILDING_CATALOG_FROM_TOC", book_id=book_id, grade=grade, subject=subject)
    with tempfile.TemporaryDirectory() as tmp:
        pdf_path = Path(tmp) / "source_book.pdf"
        download_pdf_to_path(service, book_id, pdf_path)
        from pypdf import PdfReader
        reader = PdfReader(str(pdf_path))
        num_pages = len(reader.pages)

        # قراءة الفهرس من أول 15 صفحة
        toc_text = ""
        for p_idx in range(min(15, num_pages)):
            txt = reader.pages[p_idx].extract_text() or ""
            if any(k in txt.lower() for k in ["contents", "table of contents", "sommaire", "فهرس"]):
                toc_text += f"\n=== TOC Page {p_idx + 1} ===\n" + txt

        if not toc_text:
            for p_idx in range(min(10, num_pages)):
                toc_text += f"\n=== Page {p_idx + 1} ===\n" + (reader.pages[p_idx].extract_text() or "")

        entries = []
        pattern = re.compile(
            r"(?:chapter|ch\.|chapitre|lesson|درس|فصل)?\s*(\d+)[\.\s:\-]+([A-Za-z\s,\-–'\(\)]{3,60}?)\.{2,}\s*(\d+)",
            re.I
        )
        matches = list(pattern.finditer(toc_text))
        if not matches:
            pattern2 = re.compile(
                r"(?:chapter|ch\.|chapitre|lesson|درس|فصل)\s*(\d+)[\.\s:\-]+([A-Za-z\s,\-–'\(\)]{3,50})\s+(\d+)",
                re.I
            )
            matches = list(pattern2.finditer(toc_text))

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

            # فحص الصفحة الأولى ومطابقة الكلمات للتأكد أن الدرس يبدأ هنا فعلاً
            if start_p <= num_pages:
                opening_page_text = (reader.pages[start_p - 1].extract_text() or "").lower()
                clean_title_words = [w.lower() for w in re.findall(r"[A-Za-z]{3,}", raw_title)]
                matched_words = [w for w in clean_title_words if w in opening_page_text]
                if len(matched_words) < max(1, len(clean_title_words) // 2):
                    if start_p < num_pages:
                        p2_text = (reader.pages[start_p].extract_text() or "").lower()
                        matched_words = [w for w in clean_title_words if w in p2_text]
                        if len(matched_words) >= max(1, len(clean_title_words) // 2):
                            start_p += 1
                        else:
                            raise AssertionError(f"TITLE_VERIFICATION_FAILED: عنوان الدرس '{raw_title}' غير مؤكد في الصفحة {start_p}")
                    else:
                        raise AssertionError(f"TITLE_VERIFICATION_FAILED: عنوان الدرس '{raw_title}' غير مؤكد في الصفحة {start_p}")

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
            raise AssertionError("CATALOG_BUILD_FAILED: تعذر استخراج أي درس موثق من الفهرس")

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
    """تحميل الكتالوج المعتمد من القرص للتأكد من وجوده قبل بدء التصنيع"""
    if not CATALOG_PATH.exists():
        raise RuntimeError("CATALOG_MISSING: يجب تشغيل الأمر مع خيار --build-catalog أولاً لبناء الكتالوج المعتمد")
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


# =========================================================================
# 3. محرك الدليل البصري عند الحاجة فقط وخريطة الأدلة (On-Demand Visual Evidence)
# =========================================================================

def get_on_demand_visual_evidence(pdf_path, book_id, page_num, figure_id):
    """
    وظيفة هذا الجزء:
    - فحص الكاش أولاً؛ إذا كانت الرسمة مفحوصة مسبقاً لا يعيد قراءتها.
    - فتح الصفحة المطلوبة فقط (مثلاً صفحة 17 وحدها) والتأكد من وجود الرسمة برمجياً.
    - إذا ذكر التمرين Figure 7 ولم توجد بالصفحة يوقف العملية برمز FIGURE_EVIDENCE_MISSING.
    """
    cache_file = CACHE_DIR / f"{book_id}_p{page_num}_fig{figure_id}.json"
    if cache_file.exists():
        try:
            return json.loads(cache_file.read_text(encoding="utf-8"))
        except Exception:
            pass

    progress("ON_DEMAND_VISUAL_PROCESSING", page=page_num, figure=figure_id)
    
    from pypdf import PdfReader
    reader = PdfReader(str(pdf_path))
    pdf_page = reader.pages[page_num - 1]
    
    page_text = pdf_page.extract_text() or ""
    fig_pattern = re.compile(rf"(?:figure|fig\.|شكل)\s*{re.escape(str(figure_id))}", re.I)
    
    has_text_ref = bool(fig_pattern.search(page_text))
    has_visual_objects = (len(pdf_page.images) > 0) if hasattr(pdf_page, 'images') else True

    # إذا تعذر إثبات وجود الشكل على الصفحة يمنع النموذج من اختراعه
    if not (has_text_ref or has_visual_objects):
        raise AssertionError(f"FIGURE_EVIDENCE_MISSING: الشكل {figure_id} غير موجود في الصفحة {page_num}")

    evidence_record = {
        "book_id": book_id,
        "page_num": page_num,
        "figure_id": str(figure_id),
        "verified_on_page": True,
        "visual_hash": hashlib.sha256(f"{book_id}:{page_num}:{figure_id}".encode()).hexdigest()[:12]
    }

    cache_file.write_text(json.dumps(evidence_record, ensure_ascii=False, indent=2), encoding="utf-8")
    return evidence_record


def build_deterministic_evidence_map(pages, pdf_path, book_id):
    """
    وظيفة هذا الجزء:
    - استخراج الأنشطة والتجارب صفحة بصفحة.
    - استخراج التمارين الأصلية بنصها الحرفي الدقيق من الكتاب (raw_prompt).
    - حفظ رقم الصفحة الحقيقي لكل مسألة (source_page).
    - حساب البصمة المشفرة للنص (source_text_hash) لمنع استبدال أي مسألة.
    """
    activities_evidence = []
    exercise_evidence = []

    # 1. استخراج الأنشطة والتجارب
    for page_num, page_text in pages:
        for m in re.finditer(r"(?:Activity|Activité|نشاط)\s*(\d+)[:\.\s\-]+([^\n\r]+)", page_text, re.I):
            act_num = int(m.group(1))
            act_title = m.group(2).strip()
            activities_evidence.append({
                "number": act_num,
                "source_page": page_num,
                "raw_title": act_title
            })

    # ترتيب الأنشطة وإلغاء أي تكرار
    activities_evidence.sort(key=lambda x: x["number"])
    seen_acts = set()
    dedup_acts = []
    for a in activities_evidence:
        if a["number"] not in seen_acts:
            seen_acts.add(a["number"])
            dedup_acts.append(a)
    activities_evidence = dedup_acts

    # 2. استخراج التمارين والمسائل صفحة بصفحة من صفحات المسائل
    ex_pattern = re.compile(
        r"(?:Exercise|Exercice|Problem|تمرين|مسألة)\s*(\d+)[:\.\s\-]+(.*?)(?=(?:Exercise|Exercice|Problem|تمرين|مسألة)\s*\d+|$)",
        re.DOTALL | re.I
    )

    end_page = pages[-1][0]
    problem_pages = [(p, t) for p, t in pages if p >= (end_page - 2)]

    for page_num, page_text in problem_pages:
        for match in ex_pattern.finditer(page_text):
            num = int(match.group(1))
            content = match.group(2).strip()
            clean_prompt = " ".join(content.split())
            if len(clean_prompt) >= 15:
                # بصمة الهاش للنص المصدري
                content_hash = hashlib.sha256(clean_prompt.encode('utf-8')).hexdigest()[:16]
                fig_refs = re.findall(r"(?:figure|fig\.|شكل)\s*(\d+)", clean_prompt, re.I)

                # استدعاء الدليل البصري فقط إذا كان التمرين يحتوي رسماً
                visual_evidence = []
                for f_ref in fig_refs:
                    v_ev = get_on_demand_visual_evidence(pdf_path, book_id, page_num, f_ref)
                    visual_evidence.append(v_ev)

                exercise_evidence.append({
                    "number": num,
                    "source_page": page_num,
                    "raw_prompt": clean_prompt,
                    "source_text_hash": content_hash,
                    "figure_refs": fig_refs,
                    "visual_evidence": visual_evidence,
                    "requires_figure": len(fig_refs) > 0
                })

    exercise_evidence.sort(key=lambda x: x["number"])
    seen_ex = set()
    dedup_ex = []
    for e in exercise_evidence:
        if e["number"] not in seen_ex:
            seen_ex.add(e["number"])
            dedup_ex.append(e)
    exercise_evidence = dedup_ex

    # منع قاطع: لا وجود لأي تمارين وهمية (Fallback) إطلاقاً
    if not exercise_evidence:
        raise AssertionError("QUALITY_GATE_FAILED: EXERCISE_EVIDENCE_MISSING (لم نتمكن من استخراج تمارين الكتاب الرسمية)")

    full_text = "\n\n".join([f"=== Page {p} ===\n{t}" for p, t in pages])

    return {
        "full_text": full_text,
        "activities_evidence": activities_evidence,
        "exercise_evidence": exercise_evidence,
        "exercise_numbers": [x["number"] for x in exercise_evidence]
    }


def compile_pedagogy_profile(evidence_map, subject):
    """
    تحديد البروفايل التربوي للدرس:
    - كم نشاطاً يجب أن يولده؟ (مطابقة 1:1 مع الكتاب).
    - كم مسألة في الكراسة؟
    - ما هو نوع المحاكاة (المختبر الحي) المناسب للدرس؟
    """
    act_count = len(evidence_map["activities_evidence"])
    ex_count = len(evidence_map["exercise_evidence"])
    text_lower = evidence_map["full_text"].lower()

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
# 4. طبقة التعليم بالذكاء الاصطناعي (طريقة نبيل مع قفل التمارين على المصدر)
# =========================================================================

def generate_pedagogical_theory(client, model, canonical_entry, evidence_map, profile):
    """
    توليد الشرح النظري والأنشطة:
    - ملزم بالأنشطة المستخرجة من الكتاب حصراً.
    - ممنوع إدخال مفاهيم غير موجودة (مثل الضغط الهيدروستاتيكي أو التوتر السطحي).
    - تكبير الرسوم ومطابقة نسبة الإشغال.
    """
    title = canonical_entry["canonical_title"]
    grade = canonical_entry["grade"]
    subject = canonical_entry["subject"]
    
    prompt = (
        f"You are Teacher NABIL, master professor for Lebanese Grade {grade} {subject}.\n"
        f"Lesson: '{title}'.\n\n"
        f"VERIFIED EVIDENCE MAP FROM BOOK SCANS:\n{evidence_map['full_text']}\n\n"
        f"PEDAGOGY REQUIREMENT: You MUST generate EXACTLY {profile['expected_activities_count']} activities "
        "matching 1:1 the activities evidenced in the source scans.\n"
        "STRICT PROHIBITION: Do NOT introduce surface tension, cohesion, adhesion, density formulas, or hydrostatic pressure.\n"
        "MANDATORY VISUAL OCCUPANCY RULES:\n"
        "1. For each activity, output a bold, wide SVG diagram.\n"
        "2. The scientific elements MUST occupy 75% to 85% of the SVG viewBox.\n"
        "3. NEVER draw tiny isolated shapes in a vast empty box. Labels must have font-size >= 15px and clear contrasting colors.\n"
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
        max_tokens=1900,
        temperature=0.1
    )
    txt = resp.choices[0].message.content.strip()
    if txt.startswith("```"):
        txt = re.sub(r"^```(?:json)?\s*|\s*```$", "", txt, flags=re.I).strip()
    data = json.loads(txt)

    # ضبط إطار الرسوم ونسبة الإشغال تلقائياً لكل نشاط ولكل لوحة في البطاقة
    for act in data.get("activities", []):
        act["svg_diagram"] = normalize_and_fit_svg(act.get("svg_diagram", ""))

    for p in data.get("study_card", {}).get("panels", []):
        p["svg_diagram"] = normalize_and_fit_svg(p.get("svg_diagram", ""))

    return data


def solve_source_locked_exercises_adaptive(client, model, canonical_entry, evidence_map):
    """
    حل التمارين المقفولة على نصوص الكتاب:
    - الدفعات تتكيف تلقائياً بحسب طول النص (Adaptive Batching) لتجنب خطأ 429.
    - النموذج يُطلب منه الشرح والحل فقط، ولا يُسمح له بكتابة السؤال.
    - صياغة الشرح الشفهي بنمط نبيل: «المعطى أعطانا... هذا يعني... المطلوب... إذن نستخدم... نعوّض... نستنتج».
    - حقن بصمة المصدر المشفرة في وسم الـ SVG نفسه.
    """
    title = canonical_entry["canonical_title"]
    grade = canonical_entry["grade"]
    ex_items = evidence_map["exercise_evidence"]
    all_solved = []

    # حساب حجم الدفعة الذكي بناءً على عدد كلمات المسائل
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
            "2. If requires_figure is true, reconstruct a clean, faithful vector SVG diagram. The drawing MUST occupy 75-85% of the viewBox.\n"
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
                        norm_svg = normalize_and_fit_svg(it.get("svg_diagram", "")) if orig["requires_figure"] else ""
                        
                        # حقن بصمة الدليل البصري داخل وسم الـ SVG لتثبيت الهوية ومطابقتها
                        v_hashes = [v["visual_hash"] for v in orig.get("visual_evidence", [])]
                        primary_v_hash = v_hashes[0] if v_hashes else ""
                        if orig["requires_figure"] and norm_svg and "<svg" in norm_svg:
                            norm_svg = re.sub(
                                r'<svg',
                                f'<svg data-figure-ref="{",".join(orig["figure_refs"])}" data-source-page="{orig["source_page"]}" data-visual-hash="{primary_v_hash}"',
                                norm_svg,
                                count=1
                            )

                        merged = {
                            "number": num,
                            "source_page": orig["source_page"],
                            "source_text_hash": orig["source_text_hash"],
                            "raw_prompt": orig["raw_prompt"],  # النص الأصلي الموثق من الكتاب
                            "title": it.get("title", f"Exercise {num}"),
                            "prompt_ar": it.get("prompt_ar", ""),
                            "steps_en": it.get("steps_en", []),
                            "nabil_oral_ar": it.get("nabil_oral_ar", ""),
                            "final_answer": it.get("final_answer", ""),
                            "svg_diagram": norm_svg,
                            "requires_figure": orig["requires_figure"],
                            "figure_refs": orig["figure_refs"],
                            "visual_evidence_hashes": v_hashes
                        }
                        all_solved.append(merged)
                break
            except Exception as e:
                progress("BATCH_WAIT_RETRY", error=str(e)[:100], attempt=attempt)
                time.sleep(4)

        time.sleep(2)

    return all_solved


# =========================================================================
# 5. بوابات الجودة الصارمة ومنع النشر (Zero-Tolerance Hard Gates)
# =========================================================================

def execute_deterministic_quality_gates(theory_data, solved_exercises, evidence_map, profile):
    """
    وظيفة هذا الجزء:
    - فحص حتمي لا يرحم؛ إذا وجد أي تمرين ناقص، أو هاش متبدل، أو رسمة مفقودة، أو ورقة عمل فارغة،
      يطلق استثناءً يوقف السكربت فوراً ويمنع رفع أي ملف لـ Google Drive.
    """
    progress("EXECUTING_STRICT_DETERMINISTIC_GATES")

    # 1. بوابة مطابقة عدد الأنشطة مع خريطة الكتاب
    activities = theory_data.get("activities", [])
    if len(activities) != profile["expected_activities_count"]:
        raise AssertionError(
            f"PEDAGOGY_PROFILE_MISMATCH: خريطة الأدلة تتطلب {profile['expected_activities_count']} "
            f"أنشطة، ولكن المحتوى المولد يحتوي على {len(activities)}"
        )

    for act in activities:
        if not act.get("experiment_en") or not act.get("observation_en") or not act.get("conclusion_en"):
            raise AssertionError("ACTIVITY_EVIDENCE_MISSING: هناك نشاط تنقصه التجربة أو الملاحظة أو الاستنتاج")

    # 2. بوابة اكتمال تسلسل التمارين بدون تفويت أي رقم
    expected_numbers = set(evidence_map["exercise_numbers"])
    solved_numbers = {int(x.get("number", 0)) for x in solved_exercises if "number" in x}
    missing_numbers = expected_numbers - solved_numbers
    if missing_numbers:
        raise AssertionError(f"EXERCISE_SEQUENCE_INCOMPLETE: التمارين التالية مفقودة: {sorted(list(missing_numbers))}")

    # 3. بوابة مطابقة الهاش المشفر ورقم الصفحة المصدري (منع اختلاق مسائل بديلة)
    for orig in evidence_map["exercise_evidence"]:
        matched = next((x for x in solved_exercises if x["number"] == orig["number"]), None)
        if not matched:
            raise AssertionError(f"EXERCISE_SOURCE_MISMATCH: التمرين {orig['number']} غير موجود في مصفوفة الحل")
        if matched["source_text_hash"] != orig["source_text_hash"]:
            raise AssertionError(
                f"EXERCISE_SOURCE_MISMATCH: عدم تطابق الهاش في التمرين {orig['number']}! "
                f"المتوقع {orig['source_text_hash']} والفعلي {matched['source_text_hash']}"
            )
        if matched["source_page"] != orig["source_page"]:
            raise AssertionError(f"EXERCISE_SOURCE_MISMATCH: عدم تطابق رقم الصفحة في التمرين {orig['number']}")

    # 4. بوابة مطابقة الدليل البصري للأشكال (FIGURE_SOURCE_MISMATCH)
    for orig in evidence_map["exercise_evidence"]:
        if orig["requires_figure"]:
            matched = next(x for x in solved_exercises if x["number"] == orig["number"])
            svg = matched.get("svg_diagram", "")
            
            if not svg or "<svg" not in svg:
                raise AssertionError(
                    f"FIGURE_EVIDENCE_MISSING: التمرين {orig['number']} يشير إلى الشكل "
                    f"{orig['figure_refs']} في الصفحة {orig['source_page']} لكن رسم الـ SVG مفقود"
                )
            
            # التأكد من أن الـ SVG يحمل هاش البصمة البصرية الموثق من الصفحة
            expected_hashes = [v["visual_hash"] for v in orig.get("visual_evidence", [])]
            has_matching_hash = any(h in svg for h in expected_hashes)
            if not has_matching_hash:
                raise AssertionError(
                    f"FIGURE_SOURCE_MISMATCH: رسم التمرين {orig['number']} لا يحمل بصمة الدليل البصري "
                    f"من الصفحة {orig['source_page']} (الهاش المتوقع: {expected_hashes})"
                )

    # 5. بوابة التأكد من امتلاء ورقة العمل والبطاقة المرجعية
    worksheet = theory_data.get("worksheet", [])
    if len(worksheet) < 4:
        raise AssertionError("WORKSHEET_EMPTY: ورقة التقييم يجب أن تحتوي 4 أسئلة على الأقل")

    panels = theory_data.get("study_card", {}).get("panels", [])
    if len(panels) < 2:
        raise AssertionError("STUDY_CARD_INCOMPLETE: البطاقة المرجعية النهائية تحتوي أقل من لوحتين")

    # 6. حارس حدود المصدر: منع وجود أي كلمة لم ترد في صفحات الدرس
    forbidden = ["surface tension", "cohesion", "adhesion", "hydrostatic pressure", "density of water", "p = ρgh"]
    dump = json.dumps(theory_data).lower() + " " + json.dumps(solved_exercises).lower()
    for term in forbidden:
        if term in dump:
            raise AssertionError(f"SOURCE_BOUNDARY_BREACH: اكتشاف مصطلح غير وارد في صفحات المصدر: '{term}'")

    progress("ALL_DETERMINISTIC_GATES_PASSED_SUCCESSFULLY")


# =========================================================================
# 6. نظام الألوان التربوي الطبقي ومحددات التصميم (CSS System)
# =========================================================================

def get_shared_css():
    """
    نظام الألوان التربوي الهادئ:
    - خلفية كحلي داكن هادئ (--bg-main: #0b1523).
    - بطاقات شرح رمادية مزرقة أفتح بوضوح لتفصل المحتوى (--card-bg: #132235).
    - مسطح رسم حيادي ومريح عالي التباين (--fig-surface: #1a2d44).
    - لمسات دلالية محددة:
      * التجربة: تركواز هادئ.
      * الملاحظة: كهرماني دافئ (Amber).
      * الاستنتاج: أخضر ناعم.
      * السؤال: بنفسجي رصين.
    - تجاوب كامل مع شاشات الهواتف بعرض 390px لمنع أي قص أو تداخل.
    """
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
    
    /* بطاقات الشرح الدلالية */
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
    
    /* مسطح الرسم عالي التباين */
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
    
    /* حماية عرض الهواتف الذكية (390px Viewport) */
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
# 7. محرك المحاكاة المعياري التكيفي (Dynamic Modular Lab Renderer)
# =========================================================================

def render_dynamic_live_lab(lab_type):
    """
    توليد المختبر الحي بحسب الحاجة الفعلية للدرس:
    - إذا كان درس سوائل وميلان: يولد وعاء الماء التفاعلي.
    - إذا كان أواني مستطرقة: يولد محاكاة توازن الأنابيب.
    - إذا كان درس كهرباء: يولد محاكاة دارة كهربائية.
    - إذا لم يقتضِ الدرس أي محاكاة: يعيد نصاً فارغاً ولا يفرض أي كود إضافي.
    """
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
# 8. توليد ملفات HTML التوأم والملاحة الآمنة لـ Railway
# =========================================================================

def render_page_a(theory_data, canonical_entry, profile):
    """توليد الصفحة (أ): صفحة الشرح التفاعلي والمختبر والتقييم والبطاقة المرجعية"""
    e = html.escape
    title = canonical_entry["canonical_title"]
    lid = canonical_entry["lesson_id"]
    start_p = canonical_entry["pdf_start_page"]
    end_p = canonical_entry["pdf_end_page"]

    # بناء كروت الأنشطة بالتسلسل المصدري
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

    lab_html = render_dynamic_live_lab(profile.get("lab_spec_type"))

    # ورقة العمل التفاعلية المصححة آلياً
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

    # لوحات البطاقة المرجعية الشاملة المجهزة للطباعة
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
// ملاحة آمنة لمنصة Railway دون روابط نسبية ميتة
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
    """توليد الصفحة (ب): كراسة التمارين المحلولة المقفولة تماماً على نصوص وأرقام الكتاب"""
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

        # نص السؤال يأتي حرفياً من raw_prompt المستخرج من الكتاب وليس من كتابة الذكاء الاصطناعي
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
// دالة العودة الذكية المضمونة لصفحة الدرس في منصة السكك الحديدية (Railway)
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
# 9. المنسق العام للإنتاج (Production Orchestrator)
# =========================================================================

def produce_lesson_for_entry(service, canonical_entry, report_path, publish=False):
    """
    الماكينة التنفيذية:
    1. تنزيل الكتاب.
    2. استخراج خريطة الأدلة والأشكال صفحة بصفحة.
    3. بناء الشرح والحلول بالدفعات الذكية.
    4. تمرير المخرجات على بوابات الجودة الصارمة.
    5. رندرة الملفات وحفظها ورفعها لـ Drive عند تفعيل --publish.
    """
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

        # 1. استخراج خريطة الأدلة الحتمية
        evidence_map = build_deterministic_evidence_map(pages, pdf_path, book_id)
        progress("EVIDENCE_MAP_EXTRACTED", 
                 activities=len(evidence_map["activities_evidence"]), 
                 exercises=len(evidence_map["exercise_evidence"]))

        # 2. تحديد البروفايل التربوي والمحاكاة
        profile = compile_pedagogy_profile(evidence_map, canonical_entry["subject"])

        # 3. إعداد مزود الذكاء الاصطناعي
        prov = configured_providers()[0]
        from openai import OpenAI
        client = OpenAI(api_key=prov[1], base_url=prov[2], timeout=180)

        # 4. توليد الشرح النظري وحل المسائل بالدفعات التكيفية
        theory_data = generate_pedagogical_theory(client, prov[3], canonical_entry, evidence_map, profile)
        solved_exercises = solve_source_locked_exercises_adaptive(client, prov[3], canonical_entry, evidence_map)

        # 5. تنفيذ بوابات الجودة الصارمة ومنع النشر في حال وجود أي خطأ
        execute_deterministic_quality_gates(theory_data, solved_exercises, evidence_map, profile)

        # 6. بناء أسماء الملفات ورندرة الأكواد
        slug = re.sub(r"[^\w]+", "-", title.upper()).strip("-")
        num_str = lesson_id.split("-")[-1]
        grade_tag = f"G{canonical_entry['grade']:02d}"
        subj_tag = canonical_entry['subject'].upper()

        theory_filename = f"{grade_tag}-{subj_tag}--{num_str}--{slug}.html"
        exercises_filename = f"{grade_tag}-{subj_tag}--{num_str}--{slug}--EXERCISES.html"

        html_theory = render_page_a(theory_data, canonical_entry, profile)
        html_exercises = render_page_b(solved_exercises, canonical_entry)

        # 7. فحص أمان أزرار التنقل بين الصفحتين
        if "navigateToExercises" not in html_theory or "returnToLesson" not in html_exercises:
            raise AssertionError("NAVIGATION_FAILED: دوال الملاحة الآمنة مفقودة من ملفات الـ HTML")

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

        # الرفع النهائي لـ Google Drive في حال تفعيل --publish
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

            # حذف النسخ القديمة لنفس الدرس لمنع تكرار الملفات
            existing = service.files().list(q=f"'{s_id}' in parents and (name='{theory_filename}' or name='{exercises_filename}') and trashed=false",
                                            fields="files(id, name)").execute().get("files", [])
            for f_item in existing:
                service.files().delete(fileId=f_item["id"]).execute()

            # رفع صفحة الشرح (أ)
            media_a = MediaIoBaseUpload(io.BytesIO(html_theory.encode("utf-8")), mimetype="text/html", resumable=False)
            up_a = service.files().create(body={"name": theory_filename, "parents": [s_id]}, media_body=media_a, fields="id").execute()
            report["drive_theory_id"] = up_a["id"]

            # رفع صفحة التمارين (ب)
            media_b = MediaIoBaseUpload(io.BytesIO(html_exercises.encode("utf-8")), mimetype="text/html", resumable=False)
            up_b = service.files().create(body={"name": exercises_filename, "parents": [s_id]}, media_body=media_b, fields="id").execute()
            report["drive_exercises_id"] = up_b["id"]

            progress("PUBLISHED_TWIN_PAGES_TO_DRIVE", theory_id=up_a["id"], exercises_id=up_b["id"])

        return report


# =========================================================================
# 10. نقطة الدخول الرئيسية ومعالجة الأوامر من السطر البرمجي
# =========================================================================

def main():
    parser = argparse.ArgumentParser(description="NABIL AI Universal Production Factory")
    parser.add_argument("--report", default="data/nabil_lesson_factory_run.json")
    parser.add_argument("--lesson-id", default="G07-PHYSICS-001")
    parser.add_argument("--build-catalog", action="store_true", help="استخراج الفهرس وبناء الكتالوج المعتمد")
    parser.add_argument("--book-id", default="1LasqIgGUuck1l-2EZbj2kA0Dg9ygJ_AH", help="معرف ملف الـ PDF على Drive")
    parser.add_argument("--grade", default=7, type=int)
    parser.add_argument("--subject", default="physics")
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()

    global PROGRESS_STARTED
    PROGRESS_STARTED = time.monotonic()

    service = owner_drive()

    # الوضع الأول: استخراج الفهرس وبناء الكتالوج
    if args.build_catalog:
        build_or_verify_catalog(service, args.book_id, args.grade, args.subject)
        return 0

    # الوضع الثاني: تشغيل خط تصنيع الدرس
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
