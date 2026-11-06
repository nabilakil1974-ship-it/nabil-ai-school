"""Universal timetable image/document extraction and conflict analysis for NABIL."""
from __future__ import annotations

import io
import json
import logging
import base64
import os
import urllib.request
import urllib.error
import re
from collections import defaultdict
from typing import Any

from fastapi import APIRouter, File, HTTPException, UploadFile
from starlette.concurrency import run_in_threadpool

from app.services.ai_gateway import get_ai_gateway

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

    def alternatives(index: int, reason: str) -> list[dict[str, Any]]:
        target = entries[index]
        options = []
        # Prefer another period on the same day, then other school days.
        ordered_days = [target["day"]] + [d for d in days if d != target["day"]]
        for day in ordered_days:
            for period in range(1, max_period + 1):
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

    return {
        "school_name": parsed.get("school_name") or "",
        "days": days,
        "periods_per_day": max_period,
        "period_times": parsed.get("period_times") or [],
        "teachers": parsed.get("teachers") or [],
        "classes": parsed.get("classes") or [],
        "entries": entries,
        "teacher_unavailable": parsed.get("teacher_unavailable") or [],
        "weekly_loads": parsed.get("weekly_loads") or [],
        "unreadable": parsed.get("unreadable") or [],
        "notes": parsed.get("notes") or [],
        "conflicts": conflicts,
        "conflict_count": len(conflicts),
        "status": "conflicts_found" if conflicts else "no_conflicts_detected",
        "solutions_note": "البدائل تُحسب من الخانات المستخرجة فقط. راجع دقة قراءة الصورة والقيود قبل اعتماد أي نقل.",
    }

def _call_nabil_engine(*, image_bytes: bytes | None, mime: str, text: str = "") -> str:
    """Send school data to the authenticated NABIL Executive AI vision/text endpoint."""
    base = os.getenv("NABIL_EXECUTIVE_API_URL", "").rstrip("/")
    secret = os.getenv("NABIL_EXECUTIVE_API_KEY", "")
    if not base or not secret:
        raise RuntimeError("NABIL_EXECUTIVE_API_URL / NABIL_EXECUTIVE_API_KEY are not configured")
    payload = {
        "instructions": TIMETABLE_INSTRUCTIONS,
        "text": text,
        "mimeType": mime,
        "imageBase64": base64.b64encode(image_bytes).decode("ascii") if image_bytes else "",
    }
    request = urllib.request.Request(
        base + "/api/internal/timetable/analyze",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "X-NABIL-Internal-Key": secret},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=100) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:500]
        raise RuntimeError(f"NABIL engine returned HTTP {exc.code}: {detail}") from exc
    if not result.get("ok") or not result.get("output"):
        raise RuntimeError(str(result.get("error") or "NABIL returned no analysis"))
    return str(result["output"])


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
    filename = (file.filename or "").lower()
    data = await file.read(MAX_UPLOAD_BYTES + 1)
    if not data:
        raise HTTPException(status_code=400, detail="الملف فارغ.")
    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="حجم الملف أكبر من 15 ميغابايت.")
    image_bytes = None
    mime = file.content_type or "application/octet-stream"
    prompt = "حلّل ملف جدول الدوام المرفق واستخرج JSON المطلوب بدقة. أعطني جميع الحصص، لا تكتفِ بملخص."
    if filename.endswith((".png", ".jpg", ".jpeg", ".webp")) or mime in {"image/png", "image/jpeg", "image/webp"}:
        if mime not in {"image/png", "image/jpeg", "image/webp"}:
            mime = "image/jpeg" if filename.endswith((".jpg", ".jpeg")) else "image/png"
        image_bytes = data
    elif filename.endswith(".docx") or mime == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        prompt += "\n\nنص ملف Word وجدوله كما استُخرج: \n" + _docx_to_text(data)
    elif filename.endswith(".xlsx") or mime == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        prompt += "\n\nبيانات جميع أوراق ملف Excel كما استُخرجت: \n" + _xlsx_to_text(data)
    else:
        raise HTTPException(status_code=415, detail="الملفات المدعومة: JPG أو PNG أو WEBP أو Word DOCX أو Excel XLSX.")

    try:
        doc_text = (_docx_to_text(data) if filename.endswith(".docx") or mime == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" else _xlsx_to_text(data) if filename.endswith(".xlsx") or mime == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" else "")
        raw = await run_in_threadpool(
            _call_nabil_engine,
            image_bytes=image_bytes,
            mime=mime,
            text=doc_text,
        )
        parsed = _extract_json(raw)
        result = _audit(parsed)
        if not result["entries"]:
            raise HTTPException(status_code=422, detail={
                "message": "لم يتمكن نبيل من استخراج حصص واضحة. جرّب صورة أوضح أو ملف Word.",
                "unreadable": result["unreadable"], "notes": result["notes"],
            })
        result["engine"] = "NABIL Executive AI"
        return result
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("TIMETABLE_ANALYSIS_FAILED")
        raise HTTPException(status_code=503, detail="نبيل غير قادر على تحليل الجدول حالياً. أعد المحاولة لاحقاً.") from exc
