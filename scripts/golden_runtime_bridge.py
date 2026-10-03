"""NABIL Golden runtime bridge.

Canonical rule: the picker never guesses. A lesson is visible only when its
lesson_id metadata matches the selected grade, subject and (when encoded) branch.
Unknown picker values fail closed instead of leaking another grade's catalogue.
"""
from __future__ import annotations
import html, json, re
from pathlib import Path
from urllib.parse import quote
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

GOLDEN_ARTIFACT_DIR = Path("data/golden_artifacts")
RENDERER_URL = "/static/nabil_classroom_engine_v10.js?v=14"

_ARABIC_GRADES = {
    "الأول":"1","الاول":"1","الصفالأول":"1","الصفالاول":"1",
    "الثاني":"2","الصفالثاني":"2",
    "الثالث":"3","الصفالثالث":"3",
    "الرابع":"4","الصفالرابع":"4",
    "الخامس":"5","الصفالخامس":"5",
    "السادس":"6","الصفالسادس":"6",
    "السابع":"7","الصفالسابع":"7",
    "الثامن":"8","الصفالثامن":"8",
    "التاسع":"9","الصفالتاسع":"9",
    "الأولثانوي":"10","الاولثانوي":"10","الصفالأولثانوي":"10","الصفالاولثانوي":"10",
    "الثانيثانوي":"11","الصفالثانيثانوي":"11",
    "الثالثثانوي":"12","الصفالثالثثانوي":"12",
}

def _norm(v):
    return re.sub(r"[^a-z0-9\u0600-\u06ff]+", "", str(v or "").casefold())

def _grade_number(v):
    raw=str(v or "").strip(); compact=_norm(raw)
    if compact in _ARABIC_GRADES: return _ARABIC_GRADES[compact]
    # Accept explicit school-grade forms only; never infer from unrelated digits.
    m=re.fullmatch(r"(?:grade|g|eb)?0?([1-9]|1[0-2])",compact)
    return str(int(m.group(1))) if m else ""

def _subject_code(v):
    raw=str(v or "").casefold(); compact=_norm(raw)
    if "رياض" in raw or compact in {"math","maths","mathematics","mathematiques","mathématiques"}: return "MATH"
    if "فيز" in raw or compact in {"physics","physique"}: return "PHYSICS"
    if "كيمي" in raw or compact in {"chemistry","chimie"}: return "CHEMISTRY"
    if "علومالحياة" in compact or compact in {"biology","biologie"}: return "BIOLOGY"
    return ""

def _branch_code(v):
    raw=str(v or "").strip(); upper=raw.upper(); compact=_norm(raw)
    if not raw: return ""
    if upper=="GS" or "علومعامة" in compact or "GENERALSCIENCE" in upper.replace(" ","") or "SCIENCESGENERALES" in upper.replace(" ","") or "SCIENCESGÉNÉRALES" in upper.replace(" ",""): return "GS"
    if upper in {"LS","SV"} or "علومالحياة" in compact: return "LS"
    if upper in {"SE","ES"} or "اجتماع" in raw or "اقتصاد" in raw: return "SE"
    if upper in {"LH","HUM"} or "آداب" in raw or "انساني" in compact or "إنساني" in raw: return "LH"
    return ""

def _parse_lesson_id(lid):
    p=str(lid or "").strip().upper().split("-")
    if len(p)<3 or not re.fullmatch(r"G\d{2}",p[0]) or not p[-1].isdigit(): return None
    return {"grade":str(int(p[0][1:])),"subject":p[1],"branch":p[2] if len(p)>=4 and not p[2].isdigit() else ""}

def _language_matches(row_language, requested):
    want=_norm(requested); have=_norm(row_language)
    if not want or not have: return True
    groups=({"english","en"},{"french","fr","francais","français"},{"arabic","ar","العربية"})
    for g in groups:
        if want in g: return have in g
    return have==want

def _catalogue(grade,subject,language="",branch=""):
    from app.services.golden_store import list_registry_entries
    gn=_grade_number(grade); sc=_subject_code(subject); bc=_branch_code(branch)
    # Critical invariant: an unrecognised picker value must NEVER mean "all".
    if not gn or not sc: return []
    out=[]; seen=set()
    for row in list_registry_entries():
        if not row.get("golden"): continue
        lid=str(row.get("lesson_id") or "").strip().upper(); meta=_parse_lesson_id(lid)
        if not meta or lid in seen: continue
        if meta["grade"]!=gn or meta["subject"]!=sc: continue
        # If a lesson encodes a branch, a branch selection is mandatory and exact.
        if meta["branch"]:
            if not bc or meta["branch"]!=bc: continue
        elif bc and gn=="12":
            # Grade 12 is branch-sensitive: never mix an unbranched item into it.
            continue
        if not _language_matches(row.get("language"),language): continue
        seen.add(lid)
        out.append({"lesson_id":lid,"title":str(row.get("title") or lid),"version":str(row.get("version") or "0.01"),"language":str(row.get("language") or ""),"golden":True})
    out.sort(key=lambda x:x["lesson_id"])
    return out

def _golden_entry(grade,subject,lesson,lesson_id="",branch=""):
    from app.services.golden_store import get_registry_entry
    gn=_grade_number(grade); sc=_subject_code(subject); bc=_branch_code(branch)
    if not gn or not sc: return None
    requested=str(lesson_id or "").strip().upper()
    as_id=str(lesson or "").strip().upper()
    if not requested and re.fullmatch(r"G\d{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3}",as_id): requested=as_id
    if requested:
        row=get_registry_entry(requested); meta=_parse_lesson_id(requested)
        if not row or not row.get("golden") or not meta: return None
        if meta["grade"]!=gn or meta["subject"]!=sc: return None
        if meta["branch"] and (not bc or meta["branch"]!=bc): return None
        return row
    wanted=_norm(lesson)
    rows=_catalogue(grade,subject,"",branch)
    matches=[r for r in rows if not wanted or _norm(r["title"])==wanted]
    if len(matches)!=1: return None
    return get_registry_entry(matches[0]["lesson_id"])

def _artifact_path(lesson_id):
    safe=str(lesson_id or "").strip().upper()
    if not re.fullmatch(r"G\d{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3}",safe): raise HTTPException(422,"INVALID_LESSON_ID")
    return GOLDEN_ARTIFACT_DIR/f"{safe}.txt"

def _source_text(lesson_id,language="en",version="0.01"):
    path=_artifact_path(lesson_id)
    if path.exists():
        text=path.read_text(encoding="utf-8").strip()
        if text:return text,"golden_structured_artifact"
    from app.services.golden_store import fetch_golden_from_drive
    payload=fetch_golden_from_drive(lesson_id,language,version); text=str(payload.get("reply") or "").strip()
    if not text: raise RuntimeError(f"GOLDEN_TEACHING_TEXT_EMPTY:{lesson_id}")
    return text,"golden_drive_structured"

def _render_page(lesson_id,title,text,source):
    payload=json.dumps({"lesson_id":lesson_id,"title":title,"text":text,"source":source},ensure_ascii=False).replace("</","<\\/")
    return f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="nabil-lesson-id" content="{html.escape(lesson_id)}"><meta name="nabil-source" content="{html.escape(source)}"><title>{html.escape(title)}</title><style>html,body,#nabil-classroom-root{{margin:0;min-height:100%;background:#030b14}}#nabil-boot{{color:#dff9ff;padding:24px;font:700 18px system-ui}}</style></head><body><main id="nabil-classroom-root"><div id="nabil-boot">NABIL يجهّز الدرس…</div></main><script>window.__NABIL_GOLDEN__={payload};</script><script src="{RENDERER_URL}"></script><script>(function(){{function boot(){{var r=window.NABILClassroomV10,p=window.__NABIL_GOLDEN__,root=document.getElementById('nabil-classroom-root');if(!r||!p||!root){{root.innerHTML='<pre style="color:#ff9aaa;padding:20px">NABIL classroom failed to load.</pre>';return;}}try{{r.mount(root,p.text,p.title,p);}}catch(e){{console.error(e);root.innerHTML='<pre style="color:#ff9aaa;white-space:pre-wrap;padding:20px">'+String(e&&e.stack||e)+'</pre>';}}}}if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();}})();</script></body></html>'''

def install_golden_runtime_bridge():
    from app.main import app
    if getattr(app.state,"nabil_golden_runtime_bridge",False): return
    bridge=APIRouter()
    @bridge.get("/api/chat/curriculum/lessons")
    @bridge.get("/api/curriculum/lessons")
    def curriculum(grade:str="",subject:str="",language:str="",branch:str=""):
        rows=_catalogue(grade,subject,language,branch)
        return {"source":"canonical_golden_registry","runtime_ai":False,"count":len(rows),"lessons":rows}
    @bridge.get("/api/interactive-lessons/resolve")
    def resolve(grade:str,subject:str,lesson:str="",language:str="",lesson_id:str="",branch:str=""):
        entry=_golden_entry(grade,subject,lesson,lesson_id,branch)
        if entry is None: raise HTTPException(404,detail={"stage":"golden_registry","reason":"NO_EXACT_GOLDEN_MATCH","grade":grade,"subject":subject,"branch":branch,"lesson_id":lesson_id})
        rid=str(entry["lesson_id"]); lang=str(entry.get("language") or language or "en"); ver=str(entry.get("version") or "0.01"); text,source=_source_text(rid,lang,ver)
        return {"found":True,"title":entry.get("title") or lesson,"url":"/api/interactive-lessons/golden-classroom?lesson_id="+quote(rid)+"&language="+quote(lang)+"&version="+quote(ver),"source":source,"bytes":len(text.encode()),"lesson_id":rid,"zero_ai":True,"renderer":"nabil_classroom_v14"}
    @bridge.get("/api/interactive-lessons/golden-classroom",response_class=HTMLResponse)
    def classroom(lesson_id:str,language:str="en",version:str="0.01"):
        from app.services.golden_store import get_registry_entry
        entry=get_registry_entry(lesson_id)
        if not entry or not entry.get("golden"): raise HTTPException(404,"GOLDEN_LESSON_NOT_FOUND")
        try:text,source=_source_text(lesson_id,language,version)
        except Exception as exc: raise HTTPException(503,detail={"stage":"golden_source","reason":type(exc).__name__,"message":str(exc)[:1000],"lesson_id":lesson_id}) from exc
        title=str(entry.get("title") or lesson_id)
        return HTMLResponse(_render_page(lesson_id,title,text,source),headers={"Cache-Control":"no-store, no-cache, must-revalidate","Pragma":"no-cache","Content-Security-Policy":"default-src 'self' data: blob:; script-src 'unsafe-inline' 'self'; style-src 'unsafe-inline' 'self'; frame-ancestors 'self'","X-NABIL-Lesson-Source":source,"X-NABIL-Lesson-ID":lesson_id,"X-NABIL-Renderer":"nabil-classroom-v14"})
    @bridge.get("/api/interactive-lessons/golden-structured-view",response_class=HTMLResponse)
    def old_structured(lesson_id:str): return classroom(lesson_id)
    @bridge.get("/api/interactive-lessons/golden-view",response_class=HTMLResponse)
    def old_drive(lesson_id:str,language:str="en",version:str="0.01"): return classroom(lesson_id,language,version)
    for route in reversed(bridge.routes): app.router.routes.insert(0,route)
    app.state.nabil_golden_runtime_bridge=True
