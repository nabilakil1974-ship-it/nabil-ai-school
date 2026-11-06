"""Local, deterministic timetable reader. No remote LLM/API calls."""
from __future__ import annotations
import io, re
from collections import Counter
from typing import Any

DAY_ALIASES = {
    "الاثنين":"الإثنين", "الإثنين":"الإثنين", "monday":"Monday",
    "الثلاثاء":"الثلاثاء", "tuesday":"Tuesday",
    "الاربعاء":"الأربعاء", "الأربعاء":"الأربعاء", "wednesday":"Wednesday",
    "الخميس":"الخميس", "thursday":"Thursday",
    "الجمعة":"الجمعة", "friday":"Friday",
    "السبت":"السبت", "saturday":"Saturday",
    "الاحد":"الأحد", "الأحد":"الأحد", "sunday":"Sunday",
}
ALIASES = {
 "day":{"اليوم","day","النهار"},
 "period":{"الحصة","رقم الحصة","period","الساعة"},
 "class":{"الشعبة","الصف","الصف/الشعبة","class","section"},
 "subject":{"المادة","المواد","subject"},
 "teacher":{"المعلم","الأستاذ","المدرس","teacher"},
}
def _norm(v: Any) -> str:
    return re.sub(r"\s+"," ",str(v or "")).strip().lower()
def _day(v: Any) -> str:
    s=_norm(v)
    return DAY_ALIASES.get(s, str(v or "").strip())
def _rows_from_docx(data: bytes):
    from docx import Document
    doc=Document(io.BytesIO(data)); rows=[]
    for t in doc.tables:
        rows.extend([[c.text.replace("\n"," ").strip() for c in r.cells] for r in t.rows])
    return rows
def _rows_from_xlsx(data: bytes):
    from openpyxl import load_workbook
    wb=load_workbook(io.BytesIO(data),read_only=True,data_only=True); rows=[]
    for ws in wb.worksheets:
        rows.extend([[str(v).strip() if v is not None else "" for v in r] for r in ws.iter_rows(values_only=True)])
    wb.close(); return rows
def _rows_from_ocr(data: bytes):
    try:
        from PIL import Image
        import pytesseract
    except Exception as exc:
        raise RuntimeError("ميزة OCR المحلي غير مثبّتة على الخادم.") from exc
    image=Image.open(io.BytesIO(data)).convert("RGB")
    # OCR runs on this server; no image is sent to an external AI service.
    raw=pytesseract.image_to_string(image, lang="ara+eng+fra", config="--psm 6")
    rows=[]
    for line in raw.splitlines():
        line=line.strip()
        if not line: continue
        cells=[x.strip() for x in re.split(r"\s*\|\s*|\t+|\s*;\s*",line) if x.strip()]
        if len(cells)>=5: rows.append(cells)
    if not rows:
        raise ValueError("قرأ OCR النص محلياً، لكنه لم يجد صفوفاً واضحة بصيغة أعمدة مفصولة. لا يمكن تخمين مواقع الحصص من صورة غير مفهومة.")
    return rows
def read_timetable(data: bytes, kind: str) -> dict[str, Any]:
    if kind=="docx": rows=_rows_from_docx(data)
    elif kind=="xlsx": rows=_rows_from_xlsx(data)
    elif kind=="image": rows=_rows_from_ocr(data)
    else: raise ValueError("صيغة غير مدعومة")
    rows=[[str(c or "").strip() for c in row] for row in rows if any(str(c or "").strip() for c in row)]
    header_i=-1; indexes={}
    for ri,row in enumerate(rows[:30]):
        found={}
        for ci,cell in enumerate(row):
            n=_norm(cell)
            for key, names in ALIASES.items():
                if n in {_norm(x) for x in names}: found[key]=ci
        if len(found)>=4 and {"day","period","class","subject","teacher"}.issubset(found):
            header_i=ri; indexes=found; break
    if header_i<0:
        raise ValueError("لم أجد جدولاً منظماً بعناوين الأعمدة الخمسة: اليوم، الحصة، الشعبة، المادة، المعلم. لم أستخدم أي خدمة ذكاء اصطناعي خارجية.")
    entries=[]; unreadable=[]
    for ri,row in enumerate(rows[header_i+1:],header_i+2):
        try:
            vals={k:(row[i] if i<len(row) else "") for k,i in indexes.items()}
            day=_day(vals["day"]); period=int(re.search(r"\d+",vals["period"]).group())
            cls=vals["class"].strip(); subject=vals["subject"].strip(); teacher=vals["teacher"].strip()
            if not all([day,cls,subject,teacher]): raise ValueError()
            entries.append({"day":day,"period":period,"class":cls,"subject":subject,"teacher":teacher})
        except Exception:
            if any(row): unreadable.append(f"السطر {ri}: تعذر تحديد اليوم والحصة والشعبة والمادة والمعلم")
    if not entries: raise ValueError("لم أتمكن من استخراج أي حصة كاملة من الجدول.")
    days=list(dict.fromkeys(x["day"] for x in entries))
    classes=list(dict.fromkeys(x["class"] for x in entries))
    teachers=list(dict.fromkeys(x["teacher"] for x in entries))
    loads=Counter((x["teacher"],x["class"],x["subject"]) for x in entries)
    weekly=[{"teacher":t,"class":c,"subject":s,"count":n} for (t,c,s),n in loads.items()]
    return {"school_name":"","days":days,"periods_per_day":max(x["period"] for x in entries),
      "teachers":teachers,"classes":classes,"entries":entries,"teacher_unavailable":[],
      "weekly_loads":weekly,"unreadable":unreadable,
      "notes":["تمت القراءة محلياً داخل NABIL دون Gemini أو أي API خارجي.",
               "الأنصبة الأسبوعية المستنتجة هي عدد الحصص الظاهرة في الملف فقط؛ لا تثبت اكتمال النصاب."]}
