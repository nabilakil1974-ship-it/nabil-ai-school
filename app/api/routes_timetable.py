"""Universal timetable image/document extraction and conflict analysis for NABIL."""
from __future__ import annotations

import io
import json
import logging
import re
from collections import Counter, defaultdict
from typing import Any

from fastapi import APIRouter, Body, File, HTTPException, UploadFile
from starlette.concurrency import run_in_threadpool

from app.local_timetable_reader import read_timetable, read_pasted_timetable
from app.local_timetable_intake import parse_spoken_school_intake
from app.timetable_solver import solve_timetable

router = APIRouter(prefix="/timetable", tags=["timetable"])
logger = logging.getLogger("nabil_ai.timetable")
MAX_UPLOAD_BYTES = 15 * 1024 * 1024

TIMETABLE_INSTRUCTIONS = """
أنت محرك قراءة وتحليل جداول الدوام المدرسي في NABIL.
المطلوب قراءة جدول المدرسة من الصورة أو النص، لا حل تمرين مدرسي.
استخرج كل ما يمكن قراءته كما هو، ولا تخترع اسماً أو مادة أو حصة أو وقتاً.
قد يكون الجدول عربياً أو إنكليزياً أو فرنسياً، وقد يكون مخطوطاً.
أعد JSON صالحاً فقط، بلا Markdown أو مقدمة، وفق البنية:
{
 "school_name": "",
 "days": ["الاثنين"],
 "periods_per_day": 7,
 "period_times": [{"period":1,"start":"08:00","end":"08:45"}],
 "teachers": ["اسم الأستاذ"],
 "classes": ["السابع أ"],
 "entries": [
  {"day":"الاثنين","period":1,"class":"السابع أ","subject":"رياضيات","teacher":"اسم الأستاذ"}
 ],
 "teacher_unavailable": [
  {"teacher":"اسم الأستاذ","day":"الثلاثاء","period":3}
 ],
 "weekly_loads": [
  {"teacher":"اسم الأستاذ","class":"السابع أ","subject":"رياضيات","count":4}
 ],
 "unreadable": ["وصف الخانة أو الاسم غير الواضح"],
 "notes": ["أي ملاحظة لازمة"]
}
قواعد إلزامية:
- كل خانة درس واضحة في الجدول تصبح entry واحدة.
- لا تعتبر الاستراحة حصة.
- إذا كانت أوقات الفراغ مكتوبة صراحة، ضعها في teacher_unavailable؛ لا تستنتج الفراغ من عدم وجود درس.
- إذا لم يظهر المعلم أو المادة بوضوح، اترك القيمة فارغة وأضفها إلى unreadable بدلاً من التخمين.
- إذا كان الملف يحتوي عدة جداول/صفحات، استخرجها كلها.
- حافظ على أسماء الشعب والمعلمين كما هي، ولا تدمج اسمين متشابهين دون دليل.
- إذا لم يكن هناك جدول حصص، أعد entries فارغة ووضح السبب في notes.
"""

def _extract_json(raw: str) -> dict[str, Any]:
    text = (raw or "").strip()
    text = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", text, flags=re.I)
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("AI response did not contain a JSON object")
    value = json.loads(text[start:end + 1])
    if not isinstance(value, dict):
        raise ValueError("AI response is not an object")
    return value

def _slot_key(day: str, period: int) -> tuple[str, int]:
    return (str(day).strip(), int(period))

def _audit(parsed: dict[str, Any]) -> dict[str, Any]:
    entries = []
    for raw in parsed.get("entries", []) or []:
        if not isinstance(raw, dict):
            continue
        try:
            period = int(raw.get("period"))
        except (TypeError, ValueError):
            continue
        day = str(raw.get("day") or "").strip()
        cls = str(raw.get("class") or "").strip()
        teacher = str(raw.get("teacher") or "").strip()
        subject = str(raw.get("subject") or "").strip()
        if period < 1 or not day or not cls:
            continue
        entries.append({"day": day, "period": period, "class": cls,
                        "teacher": teacher, "subject": subject})

    by_teacher: dict[tuple[str, str, int], list[int]] = defaultdict(list)
    by_class: dict[tuple[str, str, int], list[int]] = defaultdict(list)
    for i, e in enumerate(entries):
        if e["teacher"]:
            by_teacher[(e["teacher"], e["day"], e["period"])].append(i)
        by_class[(e["class"], e["day"], e["period"])].append(i)

    unavailable = []
    for item in parsed.get("teacher_unavailable", []) or []:
        try:
            unavailable.append((str(item.get("teacher") or "").strip(),
                                str(item.get("day") or "").strip(),
                                int(item.get("period"))))
        except (AttributeError, TypeError, ValueError):
            continue
    blocked = set(unavailable)
    max_period = max([e["period"] for e in entries] + [int(parsed.get("periods_per_day") or 0)])
    days = [str(x).strip() for x in (parsed.get("days") or []) if str(x).strip()]
    days = list(dict.fromkeys(days + [e["day"] for e in entries]))
    day_period_limits = {str(k).strip(): int(v) for k, v in (parsed.get("day_period_limits") or {}).items()
                         if str(k).strip() and str(v).isdigit()}
    for day in days:
        observed = max([e["period"] for e in entries if e["day"] == day] or [0])
        day_period_limits.setdefault(day, observed)

    def alternatives(index: int, reason: str) -> list[dict[str, Any]]:
        target = entries[index]
        options = []
        # Prefer another period on the same day, then other school days.
        ordered_days = [target["day"]] + [d for d in days if d != target["day"]]
        for day in ordered_days:
            for period in range(1, day_period_limits.get(day, 0) + 1):
                if day == target["day"] and period == target["period"]:
                    continue
                if any(j != index and e["class"] == target["class"]
                       and e["day"] == day and e["period"] == period
                       for j, e in enumerate(entries)):
                    continue
                if target["teacher"] and any(j != index and e["teacher"] == target["teacher"]
                       and e["day"] == day and e["period"] == period
                       for j, e in enumerate(entries)):
                    continue
                if target["teacher"] and (target["teacher"], day, period) in blocked:
                    continue
                options.append({"day": day, "period": period,
                                "move_class": target["class"],
                                "teacher": target["teacher"],
                                "subject": target["subject"],
                                "from_day": target["day"],
                                "from_period": target["period"],
                                "reason": "موعد بديل لا يظهر فيه إشغال للشعبة أو للمدرس ضمن البيانات المستخرجة"})
                if len(options) >= 3:
                    return options
        return options

    conflicts = []
    for (teacher, day, period), indexes in by_teacher.items():
        if len(indexes) > 1:
            conflicts.append({
                "type": "teacher_double_booking", "severity": "high",
                "teacher": teacher, "day": day, "period": period,
                "entries": [entries[i] for i in indexes],
                "solutions": [{"move": entries[i], "alternatives": alternatives(i, "teacher")}
                              for i in indexes],
            })
    for (cls, day, period), indexes in by_class.items():
        if len(indexes) > 1:
            conflicts.append({
                "type": "class_double_booking", "severity": "high",
                "class": cls, "day": day, "period": period,
                "entries": [entries[i] for i in indexes],
                "solutions": [{"move": entries[i], "alternatives": alternatives(i, "class")}
                              for i in indexes],
            })
    for i, e in enumerate(entries):
        if e["teacher"] and (e["teacher"], e["day"], e["period"]) in blocked:
            conflicts.append({
                "type": "teacher_unavailable", "severity": "high",
                "teacher": e["teacher"], "day": e["day"], "period": e["period"],
                "entries": [e],
                "solutions": [{"move": e, "alternatives": alternatives(i, "unavailable")}],
            })

    # Compare subject lesson counts between parallel sections of the same grade.
    # This is a diagnostic signal, not an assumed official curriculum requirement.
    def grade_group(class_name: str) -> str:
        return re.sub(r"\\s+[اأإآء-ي]$", "", str(class_name).strip())

    def subject_key(subject: str) -> str:
        value = re.sub(r"\\s+", " ", str(subject).strip())
        folded = value.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
        aliases = {"انكايزي": "انكليزي", "الانكليزي": "انكليزي", "انجليزي": "انكليزي",
                   "الانجليزي": "انكليزي"}
        return aliases.get(folded, folded)

    counts_by_class_subject = Counter((e["class"], subject_key(e["subject"]))
                                      for e in entries if e["subject"])
    grade_classes: dict[str, list[str]] = defaultdict(list)
    for cls in dict.fromkeys(e["class"] for e in entries):
        grade_classes[grade_group(cls)].append(cls)
    subject_balance = []
    for grade, parallel_classes in grade_classes.items():
        if len(parallel_classes) < 2:
            continue
        subjects = set(subj for (cls, subj) in counts_by_class_subject if cls in parallel_classes)
        for subj in sorted(subjects):
            distribution = {cls: counts_by_class_subject.get((cls, subj), 0)
                            for cls in parallel_classes}
            values = set(distribution.values())
            if len(values) > 1:
                subject_balance.append({"grade": grade, "subject": subj,
                                         "counts_by_class": distribution,
                                         "difference": max(values) - min(values),
                                         "note": "اختلاف بين الشعب المتوازية؛ راجع النصاب المعتمد لهذه المادة قبل تعديل الجدول."})

    return {
        "school_name": parsed.get("school_name") or "",
        "days": days,
        "periods_per_day": max_period,
        "day_period_limits": day_period_limits,
        "period_times": parsed.get("period_times") or [],
        "teachers": parsed.get("teachers") or [],
        "classes": parsed.get("classes") or [],
        "entries": entries,
        "teacher_unavailable": parsed.get("teacher_unavailable") or [],
        "weekly_loads": parsed.get("weekly_loads") or [],
        "unreadable": parsed.get("unreadable") or [],
        "notes": parsed.get("notes") or [],
        "conflicts": conflicts,
        "subject_balance": subject_balance,
        "conflict_count": len(conflicts),
        "status": "conflicts_found" if conflicts else "no_conflicts_detected",
        "solutions_note": "البدائل تُحسب من الخانات المستخرجة فقط. راجع دقة قراءة الصورة والقيود قبل اعتماد أي نقل.",
    }

def _docx_to_text(data: bytes) -> str:
    try:
        from docx import Document
        doc = Document(io.BytesIO(data))
    except Exception as exc:
        raise HTTPException(status_code=400, detail="تعذرت قراءة ملف Word. ارفع ملف DOCX صالحاً.") from exc
    parts = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    for table_no, table in enumerate(doc.tables, 1):
        parts.append(f"\n[جدول {table_no}]")
        for row in table.rows:
            parts.append(" | ".join(cell.text.replace("\n", " / ").strip() for cell in row.cells))
    return "\n".join(parts).strip()


def _xlsx_to_text(data: bytes) -> str:
    try:
        from openpyxl import load_workbook
        workbook = load_workbook(io.BytesIO(data), read_only=True, data_only=True)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="تعذرت قراءة ملف Excel. ارفع ملف XLSX صالحاً.") from exc
    parts = []
    for sheet in workbook.worksheets:
        parts.append(f"\n[ورقة العمل: {sheet.title}]")
        for row in sheet.iter_rows(values_only=True):
            values = [str(value).strip() if value is not None else "" for value in row]
            while values and not values[-1]:
                values.pop()
            if any(values):
                parts.append(" | ".join(values))
    workbook.close()
    return "\n".join(parts).strip()

@router.post("/analyze")
async def analyze_timetable(file: UploadFile = File(...)):
    """Read supported timetable files locally; this endpoint never calls a hosted LLM."""
    filename = (file.filename or "").lower()
    data = await file.read(MAX_UPLOAD_BYTES + 1)
    if not data:
        raise HTTPException(status_code=400, detail="الملف فارغ.")
    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="حجم الملف أكبر من 15 ميغابايت.")
    if filename.endswith((".png", ".jpg", ".jpeg", ".webp")):
        kind = "image"
    elif filename.endswith(".docx"):
        kind = "docx"
    elif filename.endswith(".xlsx"):
        kind = "xlsx"
    else:
        raise HTTPException(status_code=415, detail="الملفات المدعومة: JPG أو PNG أو WEBP أو Word DOCX أو Excel XLSX.")
    try:
        parsed = await run_in_threadpool(read_timetable, data, kind)
        result = _audit(parsed)
        if not result["entries"]:
            raise HTTPException(status_code=422, detail={
                "message": "لم يستخرج نبيل حصصاً مكتملة. راجع تنسيق الملف وعناوين أعمدته.",
                "unreadable": result["unreadable"], "notes": result["notes"],
            })
        result["engine"] = "NABIL Local Engine"
        result["external_ai_used"] = False
        return result
    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("LOCAL_TIMETABLE_ANALYSIS_FAILED")
        raise HTTPException(status_code=422, detail="تعذرت القراءة المحلية للملف: " + str(exc)) from exc


@router.post("/analyze-text")
async def analyze_timetable_text(payload: dict[str, Any] = Body(...)):
    """Analyze an Excel-copied timetable text locally; no external AI."""
    raw = payload.get("text", "")
    try:
        parsed = await run_in_threadpool(read_pasted_timetable, raw)
        result = _audit(parsed)
        if not result["entries"]:
            raise HTTPException(status_code=422, detail="لم يستخرج نبيل حصصاً من النص الملصق.")
        result["engine"] = "NABIL Local Engine"
        result["external_ai_used"] = False
        return result
    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("PASTED_TIMETABLE_ANALYSIS_FAILED")
        raise HTTPException(status_code=422, detail="تعذر تحليل النص الملصق: " + str(exc)) from exc


@router.post("/intake-text")
async def intake_spoken_school_text(payload: dict[str, Any] = Body(...)):
    """Convert spoken Arabic school setup notes into a reviewable local draft."""
    raw = payload.get("text", "")
    try:
        result = await run_in_threadpool(parse_spoken_school_intake, raw)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("SPOKEN_TIMETABLE_INTAKE_FAILED")
        raise HTTPException(status_code=422, detail="تعذر تنظيم الوصف الصوتي محلياً: " + str(exc)) from exc


@router.post("/diagnose")
async def diagnose_timetable_file(file: UploadFile = File(...)):
    """Return a temporary, bounded workbook structure report; never persist uploaded data."""
    filename = (file.filename or "").lower()
    if not filename.endswith(".xlsx"):
        raise HTTPException(status_code=415, detail="تقرير التشخيص متاح حالياً لملفات Excel XLSX فقط.")
    data = await file.read(MAX_UPLOAD_BYTES + 1)
    if not data:
        raise HTTPException(status_code=400, detail="الملف فارغ.")
    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="حجم الملف أكبر من 15 ميغابايت.")
    try:
        from openpyxl import load_workbook
        workbook = load_workbook(io.BytesIO(data), read_only=False, data_only=True)
        report = {
            "title": "NABIL Excel Diagnostic Report",
            "filename": file.filename or "workbook.xlsx",
            "file_size_bytes": len(data),
            "storage": "memory_only_not_saved",
            "external_ai_used": False,
            "sheets": []
        }
        for sheet in workbook.worksheets:
            max_rows = min(sheet.max_row or 0, 120)
            max_cols = min(sheet.max_column or 0, 40)
            rows = []
            for row in sheet.iter_rows(min_row=1, max_row=max_rows, min_col=1, max_col=max_cols):
                vals = [str(cell.value).replace("\\n", " / ").strip() if cell.value is not None else "" for cell in row]
                while vals and not vals[-1]:
                    vals.pop()
                if any(vals):
                    rows.append(vals)
            report["sheets"].append({
                "name": sheet.title,
                "state": sheet.sheet_state,
                "max_row": sheet.max_row,
                "max_column": sheet.max_column,
                "merged_ranges": [str(rng) for rng in list(sheet.merged_cells.ranges)[:80]],
                "preview_rows": rows,
                "preview_truncated": (sheet.max_row or 0) > 120 or (sheet.max_column or 0) > 40
            })
        workbook.close()
        return report
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("TIMETABLE_DIAGNOSTIC_FAILED")
        raise HTTPException(status_code=422, detail="تعذر إعداد تقرير Excel: " + str(exc)) from exc


@router.post("/generate")
async def generate_timetable(payload: dict[str, Any] = Body(...)):
    """Generate a complete timetable from explicit school requirements."""
    try:
        result = await run_in_threadpool(solve_timetable, payload)
        if not result.get("ok"):
            raise HTTPException(status_code=422, detail=result)
        return result
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("TIMETABLE_GENERATION_FAILED")
        raise HTTPException(status_code=500, detail="تعذر إنشاء الجدول بسبب خطأ داخلي.") from exc
