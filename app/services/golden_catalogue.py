"""Canonical Golden catalogue + verified zero-AI Smart-Lab runtime.

Student path is deterministic and local-only:
NABIL_GOLDEN_CATALOGUE.json -> golden_package_store -> renderer/labs.
Drive/AI belong to the production pipeline, never to student page rendering.
"""
from __future__ import annotations

import hashlib
import html
import json
import logging
import os
import re
from pathlib import Path
from urllib.parse import quote

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from app.services.golden_package_store import catalogue_entries, lesson_source, readiness

PUBLISHED_LABS_DIR = Path(os.getenv("NABIL_PUBLISHED_LABS_DIR", "data/published_labs")).resolve()
PUBLISHED_LABS_INDEX = PUBLISHED_LABS_DIR / "index.json"

RENDERER_URL = "/static/nabil_reference_classroom_v16.js?v=1"
INTERRUPT_FIX_URL = "/static/nabil_reference_interrupt_fix_v17.js?v=1"
VERIFIED_LAB_LOADER_URL = "/static/nabil_verified_lab_loader_v19.js?v=1"
READABILITY_CSS_URL = "/static/nabil_classroom_readability_v1.css?v=1"

LANG_CODES = {"EN", "FR", "AR"}
BRANCH_CODES = {"GS", "LS", "SV", "SE", "ES", "LH", "HUM"}


def _norm(v):
    return re.sub(r"[^a-z0-9\u0600-\u06ff]+", "", str(v or "").casefold())


def _grade(v):
    raw = str(v or "").strip(); x = _norm(raw)
    if re.fullmatch(r"(?:[1-9]|10|11|12)", raw): return str(int(raw))
    m = re.search(r"(?:grade|eb|g)0?([1-9]|1[0-2])$", x)
    if m: return str(int(m.group(1)))
    for k,n in [("الثانيعشر","12"),("الثالثثانوي","12"),("الحاديعشر","11"),("الثانيثانوي","11"),("العاشر","10"),("الأولثانوي","10"),("الاولثانوي","10"),("التاسع","9"),("الثامن","8"),("السابع","7"),("السادس","6"),("الخامس","5"),("الرابع","4"),("الثالث","3"),("الثاني","2"),("الأول","1"),("الاول","1")]:
        if _norm(k) in x: return n
    return ""


def _subject(v):
    x = _norm(v)
    if "رياض" in x or x in {"math","maths","mathematics","mathematiques"}: return "MATH"
    if "فيز" in x or x in {"physics","physique"}: return "PHYSICS"
    if "كيمي" in x or x in {"chemistry","chimie"}: return "CHEMISTRY"
    if "علومالحياة" in x or x in {"biology","biologie"}: return "BIOLOGY"
    return ""


def _branch(v):
    x=_norm(v); u=str(v or "").strip().upper()
    if not x:return ""
    if u=="GS" or "علومعامة" in x or "العامة" in x:return "GS"
    if u in {"LS","SV"} or "علومالحياة" in x or "الحياة" in x:return "LS"
    if u in {"SE","ES"} or "اجتماع" in x or "اقتصاد" in x:return "SE"
    if u in {"LH","HUM"} or "آداب" in x or "انساني" in x:return "LH"
    return ""


def _lang(v):
    x=_norm(v)
    if x in {"en","english","anglais"}:return "EN"
    if x in {"fr","french","francais"}:return "FR"
    if x in {"ar","arabic","العربية","عربي"}:return "AR"
    return ""


def _meta(lid):
    p=str(lid or "").strip().upper().split("-")
    if len(p)<3 or not re.fullmatch(r"G\d{2}",p[0]) or not re.fullmatch(r"\d{3}",p[-1]):return None
    branch=""; lang=""
    for token in p[2:-1]:
        if token in LANG_CODES:lang=token
        elif token in BRANCH_CODES:branch={"SV":"LS","ES":"SE","HUM":"LH"}.get(token,token)
    return {"grade":str(int(p[0][1:])),"subject":p[1],"branch":branch,"language":lang,"seq":p[-1]}


def _registry_rows():
    rows=[]
    for lid,e in sorted(catalogue_entries().items()):
        m=_meta(lid) or {}
        lang=str(e.get("language") or "English")
        rows.append({
            "lesson_id":lid,"title":str(e.get("title") or lid),
            "language":"fr" if "fr" in lang.lower() else ("ar" if "ar" in lang.lower() else "en"),
            "version":str(e.get("version") or "0.01"),
            "grade":str(e.get("grade") or m.get("grade") or ""),
            "branch":str(e.get("branch") or m.get("branch") or ""),"golden":True,
        })
    return rows


def _catalogue(grade,subject,language="",branch=""):
    gn=_grade(grade); sc=_subject(subject); bc=_branch(branch); lc=_lang(language); out=[]
    if not gn or not sc:return out
    for row in _registry_rows():
        m=_meta(row["lesson_id"])
        if not m:continue
        if m["grade"] and m["grade"]!=gn:continue
        if m["subject"] and m["subject"]!=sc:continue
        if gn=="12" and bc and m["branch"] and m["branch"]!=bc:continue
        rl=m["language"] or _lang(row.get("language"))
        if lc and rl and lc!=rl:continue
        ready=readiness(row["lesson_id"])
        out.append({k:row[k] for k in ("lesson_id","title","version","language","golden")} | {"runtime_ready":ready["runtime_ready"]})
    return out


def _entry(lid):
    lid=str(lid or "").strip().upper()
    return next((r for r in _registry_rows() if r["lesson_id"]==lid),None)


def _source(entry):
    found=lesson_source(entry["lesson_id"])
    if not found:raise RuntimeError(f"LOCAL_GOLDEN_PACKAGE_MISSING: {entry['lesson_id']}")
    _catalogue_entry,text,source=found
    return text,source


def _source_or_503(entry):
    try:return _source(entry)
    except Exception as exc:
        logging.getLogger("nabil_ai.golden").exception("GOLDEN_SOURCE_UNAVAILABLE %s",entry.get("lesson_id"))
        raise HTTPException(503,"GOLDEN_SOURCE_UNAVAILABLE") from exc


def _published_index():
    if not PUBLISHED_LABS_INDEX.is_file():return {}
    try:data=json.loads(PUBLISHED_LABS_INDEX.read_text(encoding="utf-8"))
    except (OSError,ValueError,TypeError):return {}
    return data if isinstance(data,dict) else {}


def _lesson_lab_records(lesson_id,language=""):
    lid=str(lesson_id or "").strip().upper(); lang=(_lang(language) or "").lower(); idx=_published_index()
    labs=idx.get("labs") if isinstance(idx.get("labs"),dict) else {}
    lesson=(idx.get("lessons") or {}).get(lid,{}) if isinstance(idx.get("lessons"),dict) else {}
    keys=lesson.get("artifact_keys") or [] if isinstance(lesson,dict) else []; out=[]
    for key in keys:
        raw=labs.get(key)
        if not isinstance(raw,dict) or str(raw.get("lesson_id") or "").strip().upper()!=lid:continue
        raw_lang=(_lang(raw.get("language")) or "").lower()
        if lang and raw_lang and lang!=raw_lang:continue
        rel=str(raw.get("path") or raw.get("html_file") or "").strip()
        if not rel:continue
        candidate=(PUBLISHED_LABS_DIR/rel).resolve()
        try:candidate.relative_to(PUBLISHED_LABS_DIR)
        except ValueError:continue
        if not candidate.is_file():continue
        try:payload=candidate.read_bytes()
        except OSError:continue
        expected=str(raw.get("sha256") or "").strip().lower(); actual=hashlib.sha256(payload).hexdigest()
        if not expected or expected!=actual:continue
        contract=str(raw.get("renderer_contract") or "").strip()
        if not contract:continue
        out.append({**raw,"artifact_key":str(raw.get("artifact_key") or key),"lab_id":str(raw.get("lab_key") or raw.get("lab_id") or ""),"path":rel,"verified":True,"source_signature":expected,"html":payload.decode("utf-8")})
    return out


def _verified_lab(lesson_id,lab_id,language):
    wanted=str(lab_id or "").strip().casefold()
    for raw in _lesson_lab_records(lesson_id,language):
        if str(raw.get("lab_id") or "").strip().casefold()==wanted:
            return {"found":True,"verified":True,"lesson_id":str(lesson_id).strip().upper(),"lab_id":raw["lab_id"],"language":str(raw.get("language") or language),"kind":str(raw.get("kind") or ""),"title":str(raw.get("title") or "NABIL Smart Lab"),"renderer_contract":str(raw.get("renderer_contract") or ""),"source_signature":str(raw.get("source_signature") or ""),"teacher_pointer":"sentence-synced","teacher_lifecycle":"start|state|step|complete|stopped","source":"factory_quality_gated_static_lab","ai_used":False,"generation_started":False,"html":raw["html"]}
    return None


def _page(entry,text,source):
    meta=_meta(entry["lesson_id"]) or {}
    payload=json.dumps({"lesson_id":entry["lesson_id"],"title":entry["title"],"text":text,"source":source,"language":meta.get("language") or entry.get("language") or "ar"},ensure_ascii=False).replace("</","<\\/")
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
        if not entry:raise HTTPException(404,"GOLDEN_LESSON_NOT_FOUND")
        text,source=_source_or_503(entry)
        return {"found":True,"title":entry["title"],"url":"/api/interactive-lessons/golden-classroom?lesson_id="+quote(lid),"source":source,"bytes":len(text.encode()),"lesson_id":lid,"zero_ai":True,"renderer":"nabil_reference_classroom_v16","reference_cards":True,"interrupt_resume_same_line":True,"lab_contract":"factory_quality_gated_multi_lab_v19"}
    @router.get("/interactive-lessons/verified-labs")
    def verified_labs(lesson_id:str,language:str=""):
        if not _entry(lesson_id):raise HTTPException(404,"GOLDEN_LESSON_NOT_FOUND")
        rows=_lesson_lab_records(lesson_id,language)
        return {"found":bool(rows),"verified":True,"lesson_id":str(lesson_id).strip().upper(),"count":len(rows),"runtime_ai":False,"labs":[{"lab_id":r["lab_id"],"kind":r.get("kind",""),"language":r.get("language",""),"renderer_contract":r.get("renderer_contract",""),"source_signature":r.get("source_signature","")} for r in rows]}
    @router.get("/interactive-lessons/verified-lab")
    def verified_lab(lesson_id:str,lab_id:str,language:str=""):
        if not _entry(lesson_id):raise HTTPException(404,"GOLDEN_LESSON_NOT_FOUND")
        item=_verified_lab(lesson_id,lab_id,language)
        return item if item is not None else {"found":False,"verified":False,"lesson_id":str(lesson_id).strip().upper(),"lab_id":str(lab_id),"reason":"PUBLISHED_LAB_NOT_READY","generation_started":False,"fallback":False}
    @router.get("/interactive-lessons/golden-classroom",response_class=HTMLResponse)
    def classroom(lesson_id:str):
        entry=_entry(lesson_id)
        if not entry:raise HTTPException(404,"GOLDEN_LESSON_NOT_FOUND")
        text,source=_source_or_503(entry)
        return HTMLResponse(_page(entry,text,source),headers={"Cache-Control":"public, max-age=300, stale-while-revalidate=3600","X-NABIL-Lesson-ID":entry["lesson_id"],"X-NABIL-Lab-Contract":"factory-quality-gated-multi-lab-v19","X-NABIL-Runtime-Source":source})
    @router.get("/interactive-lessons/golden-structured-view",response_class=HTMLResponse)
    def old_structured(lesson_id:str):return classroom(lesson_id)
    return router
