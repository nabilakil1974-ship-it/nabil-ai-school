"""Canonical Golden lesson catalogue and zero-runtime-AI classroom routes.

Golden selection is strict by lesson_id/grade/subject/branch. The classroom uses the
reference-card renderer. Requirement 5 is fail-closed: only pre-published verified
lesson-aware labs for the exact lesson/lab id may be rendered; runtime never invents
lab values, behaviour, or a fallback from another lesson.
"""
from __future__ import annotations

import html
import json
import os
import re
import time
from pathlib import Path
from urllib.parse import quote

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

GOLDEN_ARTIFACT_DIR = Path("data/golden_artifacts")
PUBLISHED_LABS_DIR = Path(os.getenv("NABIL_PUBLISHED_LABS_DIR", "data/published_labs")).resolve()
PUBLISHED_LABS_INDEX = PUBLISHED_LABS_DIR / "index.json"
RENDERER_URL = "/static/nabil_reference_classroom_v16.js?v=1"
INTERRUPT_FIX_URL = "/static/nabil_reference_interrupt_fix_v17.js?v=1"
VERIFIED_LAB_LOADER_URL = "/static/nabil_verified_lab_loader_v18.js?v=1"
READABILITY_CSS_URL = "/static/nabil_classroom_readability_v1.css?v=1"
_CACHE = {"at": 0.0, "rows": []}
LANG_CODES = {"EN", "FR", "AR"}
BRANCH_CODES = {"GS", "LS", "SV", "SE", "ES", "LH", "HUM"}


def _norm(v):
    return re.sub(r"[^a-z0-9\u0600-\u06ff]+", "", str(v or "").casefold())


def _grade(v):
    raw = str(v or "").strip(); x = _norm(raw)
    if re.fullmatch(r"(?:[1-9]|10|11|12)", raw): return str(int(raw))
    secondary = [
        (("الثالثثانوي", "الصفالثالثثانوي", "الثانيعشر", "الصفالثانيعشر"), "12"),
        (("الثانيثانوي", "الصفالثانيثانوي", "الحاديعشر", "الصفالحاديعشر"), "11"),
        (("الأولثانوي", "الاولثانوي", "الصفالأولثانوي", "الصفالاولثانوي", "العاشر", "الصفالعاشر"), "10"),
    ]
    for names, n in secondary:
        if any(_norm(k) in x for k in names): return n
    for k,n in [("التاسع","9"),("الثامن","8"),("السابع","7"),("السادس","6"),("الخامس","5"),("الرابع","4"),("الثالث","3"),("الثاني","2"),("الأول","1"),("الاول","1")]:
        if _norm(k) in x: return n
    m = re.search(r"(?:grade|eb|g)0?([1-9]|1[0-2])$", x)
    return str(int(m.group(1))) if m else ""


def _subject(v):
    x = _norm(v)
    if "رياض" in x or x in {"math", "maths", "mathematics", "mathematiques"}: return "MATH"
    if "فيز" in x or x in {"physics", "physique"}: return "PHYSICS"
    if "كيمي" in x or x in {"chemistry", "chimie"}: return "CHEMISTRY"
    if "علومالحياة" in x or x in {"biology", "biologie"}: return "BIOLOGY"
    return ""


def _branch(v):
    x = _norm(v); u = str(v or "").strip().upper()
    if not x: return ""
    if u == "GS" or "علومعامة" in x: return "GS"
    if u in {"LS", "SV"} or "علومالحياة" in x: return "LS"
    if u in {"SE", "ES"} or "اجتماع" in x or "اقتصاد" in x: return "SE"
    if u in {"LH", "HUM"} or "آداب" in x or "انساني" in x: return "LH"
    return ""


def _lang(v):
    x = _norm(v)
    if x in {"en", "english", "anglais"}: return "EN"
    if x in {"fr", "french", "francais"}: return "FR"
    if x in {"ar", "arabic", "العربية", "عربي"}: return "AR"
    return ""


def _meta(lid):
    p = str(lid or "").strip().upper().split("-")
    if len(p) < 3 or not re.fullmatch(r"G\d{2}", p[0]) or not re.fullmatch(r"\d{3}", p[-1]): return None
    grade, subject, branch, lang = str(int(p[0][1:])), p[1], "", ""
    for token in p[2:-1]:
        if token in LANG_CODES: lang = token
        elif token in BRANCH_CODES: branch = {"SV":"LS", "ES":"SE", "HUM":"LH"}.get(token, token)
    return {"grade": grade, "subject": subject, "branch": branch, "language": lang, "seq": p[-1]}


def _drive_rows(force=False):
    if _CACHE["rows"] and not force and time.time() - _CACHE["at"] < 60: return _CACHE["rows"]
    from scripts.index_books import get_drive_service
    svc = get_drive_service(); rows = []; token = None
    while True:
        result = svc.files().list(q="trashed=false", spaces="drive", fields="nextPageToken,files(id,name,mimeType,webViewLink,appProperties)", pageSize=1000, pageToken=token).execute()
        for f in result.get("files", []):
            props = f.get("appProperties") or {}; lid = str(props.get("nabil_lesson_id") or "").strip().upper(); meta = _meta(lid)
            if not meta or not re.fullmatch(r"G\d{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3}", lid): continue
            kind = str(props.get("nabil_artifact") or "theory").lower()
            if kind not in {"theory", "lesson", "golden", "golden_lesson"}: continue
            title = str(props.get("nabil_title") or props.get("lesson_title") or f.get("name") or lid)
            title = re.sub("^" + re.escape(lid) + r"\s*[—–:-]?\s*", "", title, flags=re.I).strip() or lid
            rows.append({"lesson_id":lid,"title":title,"language":str(props.get("nabil_language") or props.get("language") or meta["language"] or "en"),"version":str(props.get("nabil_version") or props.get("version") or "0.01"),"drive_file_id":f["id"],"drive_theory_id":f["id"],"drive_url":f.get("webViewLink"),"mime_type":f.get("mimeType") or "application/vnd.google-apps.document","golden":True})
        token = result.get("nextPageToken")
        if not token: break
    dedup = {x["lesson_id"]:x for x in rows}; _CACHE.update(at=time.time(), rows=[dedup[k] for k in sorted(dedup)])
    return _CACHE["rows"]


def _catalogue(grade, subject, language="", branch=""):
    gn,sc,bc,lc = _grade(grade),_subject(subject),_branch(branch),_lang(language)
    if not gn or not sc: return []
    out=[]
    for row in _drive_rows():
        m=_meta(row["lesson_id"])
        if not m or m["grade"]!=gn or m["subject"]!=sc: continue
        if m["branch"] and m["branch"]!=bc: continue
        if gn=="12" and m["branch"] and not bc: continue
        row_lang=m["language"] or _lang(row.get("language"))
        if lc and row_lang and lc!=row_lang: continue
        out.append({k:row[k] for k in ("lesson_id","title","version","language","golden")})
    return out


def _entry(lid):
    lid=str(lid or "").strip().upper()
    return next((r for r in _drive_rows() if r["lesson_id"]==lid),None)


def _source(entry):
    lid=entry["lesson_id"]; local=GOLDEN_ARTIFACT_DIR/f"{lid}.txt"
    if local.exists() and (text:=local.read_text(encoding="utf-8").strip()): return text,"golden_structured_artifact"
    from app.services.golden_store import _drive_service, _fetch_artifact
    item=_fetch_artifact(_drive_service(),{"drive_file_id":entry["drive_file_id"],"mime_type":entry["mime_type"],"name":entry["title"],"artifact_id":lid+"-LESSON"})
    if not item or not str(item.get("text") or "").strip(): raise RuntimeError("GOLDEN_TEACHING_TEXT_EMPTY:"+lid)
    return str(item["text"]).strip(),"golden_drive_0.01"


def _safe_token(value):
    return re.sub(r"[^a-zA-Z0-9._-]+", "-", str(value or "").strip()).strip("-").lower()


def _published_index():
    if not PUBLISHED_LABS_INDEX.is_file(): return {}
    try:
        data=json.loads(PUBLISHED_LABS_INDEX.read_text(encoding="utf-8"))
    except (OSError,ValueError,TypeError): return {}
    return data if isinstance(data,dict) else {}


def _verified_lab(lesson_id, lab_id, language):
    """Resolve one exact verified lab. Supports v18 multi-lab records and legacy master-lab records."""
    lid=str(lesson_id or "").strip().upper(); wanted=_safe_token(lab_id); lang=(_lang(language) or "AR").lower()
    if not lid or not wanted: return None
    index=_published_index(); candidates=[]
    for key,raw in index.items():
        if not isinstance(raw,dict): continue
        raw_lid=str(raw.get("lesson_id") or "").strip().upper()
        raw_lab=_safe_token(raw.get("lab_id") or raw.get("concept_id") or raw.get("solution_id") or ("master-lab" if str(raw.get("kind") or "").lower() in {"master_lab","masterlab"} else ""))
        raw_lang=(_lang(raw.get("language")) or "AR").lower()
        if raw_lid==lid and raw_lab==wanted and raw_lang==lang: candidates.append(raw)
    # Backward-compatible master lab only; never map a concept/solution lab to a legacy lesson-wide lab.
    if not candidates and wanted in {"master-lab","master_lab","masterlab"}:
        for raw in index.values():
            if isinstance(raw,dict) and str(raw.get("lesson_id") or "").strip().upper()==lid and (_lang(raw.get("language")) or "AR").lower()==lang:
                candidates.append(raw)
    if not candidates: return None
    raw=candidates[0]
    # Published factory output is considered verified only when it carries provenance.
    verified=raw.get("verified") is True or (bool(str(raw.get("source_signature") or "").strip()) and bool(str(raw.get("renderer_contract") or "").strip()))
    if not verified: return None
    rel=str(raw.get("html_file") or "").strip()
    if not rel: return None
    candidate=(PUBLISHED_LABS_DIR/rel).resolve()
    try: candidate.relative_to(PUBLISHED_LABS_DIR)
    except ValueError: return None
    if not candidate.is_file(): return None
    try: html_text=candidate.read_text(encoding="utf-8")
    except OSError: return None
    if not html_text.strip(): return None
    return {"found":True,"verified":True,"lesson_id":lid,"lab_id":wanted,"language":lang,"kind":str(raw.get("kind") or ""),"title":str(raw.get("title") or "NABIL Smart Lab"),"engine_version":str(raw.get("engine_version") or ""),"renderer_contract":str(raw.get("renderer_contract") or ""),"source_signature":str(raw.get("source_signature") or ""),"concept_id":str(raw.get("concept_id") or ""),"solution_id":str(raw.get("solution_id") or ""),"teacher_pointer":"sentence-synced","teacher_lifecycle":"start|state|step|complete|stopped","source":"published_verified_lab_v18","ai_used":False,"generation_started":False,"html":html_text}


def _page(entry,text,source):
    meta=_meta(entry["lesson_id"]) or {}
    payload=json.dumps({"lesson_id":entry["lesson_id"],"title":entry["title"],"text":text,"source":source,"language":(meta.get("language") or entry.get("language") or "ar")},ensure_ascii=False).replace("</","<\\/")
    return f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(entry['title'])}</title><style>html,body,#nabil-classroom-root{{margin:0;min-height:100%;background:#030b14}}</style><link rel="stylesheet" href="{READABILITY_CSS_URL}"></head><body><main id="nabil-classroom-root"></main><script>window.__NABIL_GOLDEN__={payload};</script><script src="{INTERRUPT_FIX_URL}"></script><script src="{RENDERER_URL}"></script><script src="{VERIFIED_LAB_LOADER_URL}"></script><script>(function(){{var r=window.NABILReferenceClassroomV16,p=window.__NABIL_GOLDEN__,root=document.getElementById('nabil-classroom-root');if(r&&p)r.mount(root,p.text,p.title,p);else root.innerHTML='<pre style="color:#f99">NABIL reference classroom failed to load</pre>';}})();</script></body></html>'''


def build_router()->APIRouter:
    router=APIRouter()
    @router.get("/chat/curriculum/lessons")
    @router.get("/curriculum/lessons")
    def curriculum(grade:str="",subject:str="",language:str="",branch:str=""):
        rows=_catalogue(grade,subject,language,branch)
        return {"source":"canonical_golden_registry","runtime_ai":False,"count":len(rows),"lessons":rows}

    @router.get("/interactive-lessons/resolve")
    def resolve(grade:str,subject:str,lesson:str="",language:str="",lesson_id:str="",branch:str=""):
        lid=str(lesson_id or "").strip().upper(); entry=_entry(lid)
        if not entry: raise HTTPException(404,"GOLDEN_LESSON_NOT_FOUND")
        m=_meta(lid)
        if not m or m["grade"]!=_grade(grade) or m["subject"]!=_subject(subject) or (m["branch"] and m["branch"]!=_branch(branch)): raise HTTPException(404,"GOLDEN_SELECTION_MISMATCH")
        requested_lang=_lang(language); actual_lang=m["language"] or _lang(entry.get("language"))
        if requested_lang and actual_lang and requested_lang!=actual_lang: raise HTTPException(404,"GOLDEN_LANGUAGE_MISMATCH")
        text,source=_source(entry)
        return {"found":True,"title":entry["title"],"url":"/api/interactive-lessons/golden-classroom?lesson_id="+quote(lid),"source":source,"bytes":len(text.encode()),"lesson_id":lid,"zero_ai":True,"renderer":"nabil_reference_classroom_v16","reference_cards":True,"interrupt_resume_same_line":True,"interrupt_chat_contract":"formdata_v17","lab_contract":"verified_multi_lab_v18_fail_closed"}

    @router.get("/interactive-lessons/verified-lab")
    def verified_lab(lesson_id:str,lab_id:str,language:str="ar"):
        if not _entry(lesson_id): raise HTTPException(404,"GOLDEN_LESSON_NOT_FOUND")
        item=_verified_lab(lesson_id,lab_id,language)
        if item is None:
            return {"found":False,"verified":False,"lesson_id":str(lesson_id).strip().upper(),"lab_id":_safe_token(lab_id),"language":(_lang(language) or "AR").lower(),"reason":"PUBLISHED_LAB_NOT_READY","generation_started":False,"fallback":False}
        return item

    @router.get("/interactive-lessons/golden-classroom",response_class=HTMLResponse)
    def classroom(lesson_id:str):
        entry=_entry(lesson_id)
        if not entry: raise HTTPException(404,"GOLDEN_LESSON_NOT_FOUND")
        text,source=_source(entry)
        return HTMLResponse(_page(entry,text,source),headers={"Cache-Control":"no-store","X-NABIL-Lesson-ID":entry["lesson_id"],"X-NABIL-Lesson-Source":source,"X-NABIL-Renderer":"reference-v16","X-NABIL-Interrupt-Contract":"formdata-v17","X-NABIL-Lab-Contract":"verified-multi-lab-v18-fail-closed"})

    @router.get("/interactive-lessons/golden-structured-view",response_class=HTMLResponse)
    def old_structured(lesson_id:str): return classroom(lesson_id)
    return router
