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
