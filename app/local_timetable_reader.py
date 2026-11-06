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
        from pytesseract import Output
    except Exception as exc:
        raise RuntimeError("ميزة OCR المحلي غير مثبّتة على الخادم.") from exc
    image=Image.open(io.BytesIO(data)).convert("RGB")
    # All OCR is performed on this server; no image is sent to an external AI service.
    info=pytesseract.image_to_data(image, lang="ara+eng+fra", config="--psm 6", output_type=Output.DICT)
    words=[]
    for i,word in enumerate(info["text"]):
        word=str(word or "").strip()
        if not word or int(info["conf"][i])<15: continue
        x=int(info["left"][i]); y=int(info["top"][i]); w=int(info["width"][i]); h=int(info["height"][i])
        words.append((y+h/2,x+w/2,word))
    if len(words)<10:
        raise ValueError("لم يتمكن OCR المحلي من قراءة عدد كافٍ من الكلمات. استخدم صورة أوضح.")
    # Group tokens into visual text rows.
    words.sort(key=lambda z:z[0]); lines=[]
    for item in words:
        if not lines or abs(item[0]-lines[-1][0])>max(12,image.height*0.012):
            lines.append([item[0],[item]])
        else:
            lines[-1][1].append(item)
    # Estimate five table columns from token x-coordinates using 1-D k-means.
    xs=[z[1] for line in lines for z in line[1]]
    lo,hi=min(xs),max(xs)
    centers=[lo+(hi-lo)*(j+0.5)/5 for j in range(5)]
    for _ in range(18):
        buckets=[[] for _ in centers]
        for x in xs: buckets[min(range(5),key=lambda j:abs(x-centers[j]))].append(x)
        centers=[sum(v)/len(v) if v else centers[j] for j,v in enumerate(buckets)]
    order=sorted(range(5),key=lambda j:centers[j]); rows=[]
    for _,line in lines:
        cells=[]
        for j in order:
            tokens=[z for z in line if min(range(5),key=lambda k:abs(z[1]-centers[k]))==j]
            tokens.sort(key=lambda z:z[1])
            cells.append(" ".join(z[2] for z in tokens).strip())
        if sum(bool(x) for x in cells)>=3: rows.append(cells)
    if not rows:
        raise ValueError("قرأ OCR الصورة محلياً، لكنه لم يستطع إعادة بناء أعمدة الجدول بثقة.")
    return rows
def _read_matrix_xlsx(data: bytes) -> dict[str, Any]:
    """Read a school timetable arranged as class columns with teacher/subject pairs."""
    from openpyxl import load_workbook

    wb = load_workbook(io.BytesIO(data), read_only=False, data_only=True)
    try:
        all_entries = []
        all_classes = []
        all_days = []
        all_unreadable = []
        for ws in wb.worksheets:
            if ws.sheet_state != "visible" or not ws.max_row or not ws.max_column:
                continue
            def cell_text(r: int, c: int) -> str:
                value = ws.cell(r, c).value
                return str(value).strip() if value is not None else ""

            # Locate the row naming periods/days and the row naming teachers/subjects.
            period_col = day_col = pair_header_row = class_header_row = None
            for r in range(1, min(ws.max_row, 25) + 1):
                vals = [_norm(cell_text(r, c)) for c in range(1, ws.max_column + 1)]
                for c, val in enumerate(vals, 1):
                    if val in {"الحصة", "رقم الحصة", "period"}:
                        period_col = c
                    if val in {"اليوم", "day"}:
                        day_col = c
            # Teacher/subject labels occur together on one row.
            for r in range(1, min(ws.max_row, 25) + 1):
                vals = [_norm(cell_text(r, c)) for c in range(1, ws.max_column + 1)]
                teacher_cols = [c for c, v in enumerate(vals, 1) if v in {"المدرس", "المعلم", "الأستاذ", "teacher"}]
                subject_cols = [c for c, v in enumerate(vals, 1) if v in {"المادة", "subject"}]
                if teacher_cols and subject_cols:
                    pair_header_row = r
                    break
            if not period_col or not day_col or not pair_header_row:
                continue
            # Class names are directly above the teacher/subject labels; merged cells
            # leave the second cell of each pair blank, so retain each detected heading.
            class_header_row = pair_header_row - 1
            pairs = []
            c = 1
            while c <= ws.max_column:
                teacher_label = _norm(cell_text(pair_header_row, c))
                if teacher_label in {"المدرس", "المعلم", "الأستاذ", "teacher"}:
                    subject_c = c + 1
                    if subject_c <= ws.max_column and _norm(cell_text(pair_header_row, subject_c)) in {"المادة", "subject"}:
                        class_name = cell_text(class_header_row, c)
                        if not class_name:
                            # Some workbooks place a merged class title over the pair.
                            for back in range(c - 1, 0, -1):
                                class_name = cell_text(class_header_row, back)
                                if class_name:
                                    break
                        if class_name:
                            pairs.append((c, subject_c, class_name))
                            all_classes.append(class_name)
                        c = subject_c + 1
                        continue
                c += 1
            if not pairs:
                continue
            current_day = ""
            for r in range(pair_header_row + 1, ws.max_row + 1):
                ptxt = cell_text(r, period_col)
                dtext = cell_text(r, day_col)
                if _norm(dtext) in {_norm(x) for x in DAY_ALIASES}:
                    current_day = _day(dtext)
                    if current_day not in all_days:
                        all_days.append(current_day)
                match = re.fullmatch(r"\s*(\d+)\s*", ptxt)
                if not match or not current_day:
                    continue
                period = int(match.group(1))
                for teacher_c, subject_c, class_name in pairs:
                    teacher = cell_text(r, teacher_c)
                    subject = cell_text(r, subject_c)
                    if not teacher and not subject:
                        continue
                    if not teacher or not subject:
                        all_unreadable.append(
                            f"{ws.title}، السطر {r}، {class_name}، الحصة {period}: المدرس أو المادة ناقص"
                        )
                        continue
                    all_entries.append({"day": current_day, "period": period,
                                        "class": class_name, "subject": subject,
                                        "teacher": teacher})
        if not all_entries:
            raise ValueError("لم أتمكن من تحديد بنية جدول الحصص المصفوفي في ملف Excel.")
        teachers = list(dict.fromkeys(e["teacher"] for e in all_entries))
        classes = list(dict.fromkeys(all_classes))
        loads = Counter((e["teacher"], e["class"], e["subject"]) for e in all_entries)
        weekly = [{"teacher": t, "class": c, "subject": s, "count": n}
                  for (t, c, s), n in loads.items()]
        return {"school_name": "", "days": all_days,
                "periods_per_day": max(e["period"] for e in all_entries),
                "teachers": teachers, "classes": classes, "entries": all_entries,
                "teacher_unavailable": [], "weekly_loads": weekly,
                "unreadable": all_unreadable,
                "notes": ["تمت قراءة جدول Excel المصفوفي محلياً مع الحفاظ على أزواج المدرس/المادة والشعب.",
                          "لم تُدمج أسماء المعلمين المتشابهة تلقائياً؛ يجب مراجعة اختلافات الإملاء قبل اعتماد التعارضات والأنصبة."]}
    finally:
        wb.close()


def read_timetable(data: bytes, kind: str) -> dict[str, Any]:
    if kind=="xlsx": return _read_matrix_xlsx(data)
    if kind=="docx": rows=_rows_from_docx(data)
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


def read_pasted_timetable(raw: str) -> dict[str, Any]:
    """Parse an Excel-copied timetable matrix locally (tab-separated cells)."""
    if not isinstance(raw, str) or not raw.strip():
        raise ValueError("ألصق الجدول أولاً.")
    lines = [line.rstrip("\r") for line in raw.splitlines()]
    rows = [line.split("\t") for line in lines if line.strip()]
    if not rows:
        raise ValueError("النص الملصق لا يحتوي على صفوف.")
    classes = ["السابع ج", "السابع ب", "السابع أ", "الثامن ب", "الثامن أ", "التاسع أ"]
    day_names = { _norm(k): v for k, v in DAY_ALIASES.items() }
    entries, unreadable, days = [], [], []
    current_day = ""
    period_times = []
    for row_no, row in enumerate(rows, 1):
        cells = [str(x or "").strip() for x in row]
        # Identify the lesson number and day at the right edge of the pasted matrix.
        period_idx = next((i for i, v in enumerate(cells) if re.fullmatch(r"[1-8]", v)), -1)
        if period_idx < 0:
            continue
        day_idx = next((i for i in range(period_idx + 1, len(cells))
                        if _norm(cells[i]) in day_names), -1)
        if day_idx >= 0:
            current_day = day_names[_norm(cells[day_idx])]
        if not current_day:
            continue
        period = int(cells[period_idx])
        # Six classes, each represented by adjacent teacher/subject cells.
        # Time columns and day/period columns are outside this 12-cell block.
        pairs = cells[:12]
        if len(pairs) < 12:
            pairs += [""] * (12 - len(pairs))
        added = 0
        for class_name, offset in zip(classes, range(0, 12, 2)):
            teacher, subject = pairs[offset].strip(), pairs[offset + 1].strip()
            if not teacher and not subject:
                continue
            if not teacher or not subject:
                unreadable.append(f"السطر {row_no}، {class_name}، الحصة {period}: اسم المدرس أو المادة ناقص")
                continue
            entries.append({"day": current_day, "period": period, "class": class_name,
                            "subject": subject, "teacher": teacher})
            added += 1
        if added == 0:
            continue
        if current_day not in days:
            days.append(current_day)
        # Capture time-looking cells without assuming their left/right orientation.
        times = [v for v in cells if re.fullmatch(r"(?:[01]?\d|2[0-3]):[0-5]\d", v)]
        if len(times) >= 2:
            period_times.append({"period": period, "start": times[-1], "end": times[-2]})
    if not entries:
        raise ValueError("لم أستطع استخراج حصص من النص. انسخ الجدول مباشرة من خلايا Excel كي تبقى فواصل الأعمدة (Tabs).")
    teachers = list(dict.fromkeys(e["teacher"] for e in entries))
    loads = Counter((e["teacher"], e["class"], e["subject"]) for e in entries)
    weekly = [{"teacher": t, "class": c, "subject": s, "count": n}
              for (t, c, s), n in loads.items()]
    return {"school_name": "", "days": days, "periods_per_day": max(e["period"] for e in entries),
            "period_times": period_times, "teachers": teachers, "classes": classes,
            "entries": entries, "teacher_unavailable": [], "weekly_loads": weekly,
            "unreadable": unreadable,
            "notes": ["تم تحليل النص الملصق محلياً دون أي خدمة ذكاء اصطناعي خارجية.",
                      "يجب مراجعة أسماء المعلمين والمواد والأنصبة قبل اعتماد الجدول."]}
