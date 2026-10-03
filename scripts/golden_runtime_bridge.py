"""NABIL Golden runtime bridge — canonical Golden source -> autonomous classroom."""
from __future__ import annotations
import html, json, re
from pathlib import Path
from urllib.parse import quote
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

GOLDEN_ARTIFACT_DIR = Path("data/golden_artifacts")
# This is the file actually served by app.main's /static mount: app/static/...
# Bump on every classroom change so an old browser/service-worker copy cannot
# leave a previously-working Golden lesson as a blank black iframe.
RENDERER_URL = "/static/nabil_classroom_engine_v10.js?v=13"

def _norm(v):
    return re.sub(r"[^a-z0-9\u0600-\u06ff]+", "", str(v or "").casefold())

def _grade_number(v):
    raw = str(v or ""); compact = _norm(raw); ar = raw.replace(" ", "")
    if "الثالثثانوي" in ar: return "12"
    if "الثانيثانوي" in ar: return "11"
    if "الأولثانوي" in ar: return "10"
    m = re.search(r"(?:grade|g|eb)?0?([1-9]|1[0-2])", compact)
    return str(int(m.group(1))) if m else ""

def _subject_code(v):
    raw = str(v or "").casefold(); compact = _norm(raw)
    if "رياض" in raw or compact in {"math","maths","mathematics","mathematiques","mathématiques"}: return "MATH"
    if "فيز" in raw or compact in {"physics","physique"}: return "PHYSICS"
    if "كيمي" in raw or compact in {"chemistry","chimie"}: return "CHEMISTRY"
    if "biology" in compact or "biologie" in compact or "علومالحياة" in raw.replace(" ",""): return "BIOLOGY"
    return ""

def _branch_code(v):
    raw=str(v or "").strip(); upper=raw.upper()
    if not raw: return ""
    if upper=="GS" or "علوم عامة" in raw or "GENERAL SCIENCE" in upper or "SCIENCES GENERALES" in upper or "SCIENCES GÉNÉRALES" in upper: return "GS"
    if upper in {"LS","SV"} or "علوم الحياة" in raw: return "LS"
    if upper in {"SE","ES"} or "اجتماع" in raw or "اقتصاد" in raw: return "SE"
    if upper in {"LH","HUM"} or "آداب" in raw or "إنساني" in raw: return "LH"
    return upper

def _golden_entry(grade, subject, lesson, lesson_id=""):
    from app.services.golden_store import get_registry_entry, list_registry_entries
    requested = str(lesson_id or "").strip().upper(); as_id = str(lesson or "").strip().upper()
    if not requested and re.fullmatch(r"G\d{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3}", as_id): requested = as_id
    if requested:
        row = get_registry_entry(requested); return row if row and row.get("golden") else None
    gn, sc, wanted = _grade_number(grade), _subject_code(subject), _norm(lesson); matches=[]
    for row in list_registry_entries():
        if not row.get("golden"): continue
        rid=str(row.get("lesson_id") or "").upper(); title=str(row.get("title") or ""); p=rid.split("-")
        if gn and (not p or p[0] != f"G{int(gn):02d}"): continue
        if sc and (len(p)<2 or p[1]!=sc): continue
        if wanted and _norm(title)!=wanted: continue
        matches.append(row)
    if len(matches)>1 and wanted: raise HTTPException(409,"Multiple Golden lessons match this title; send lesson_id.")
    return matches[0] if len(matches)==1 else None

def _catalogue(grade, subject, language="", branch=""):
    """Return every published Golden lesson matching the actual picker state.

    Do not silently discard lessons merely because an older registry row lacks
    language metadata. Branch filtering is applied only when the lesson id has
    an explicit branch segment; this keeps non-branched grades visible.
    """
    from app.services.golden_store import list_registry_entries
    gn=_grade_number(grade); sc=_subject_code(subject); bc=_branch_code(branch); want_lang=_norm(language); out=[]; seen=set()
    for row in list_registry_entries():
        if not row.get("golden"): continue
        lid=str(row.get("lesson_id") or "").strip().upper(); p=lid.split("-")
        if len(p)<3 or lid in seen: continue
        if gn and p[0]!=f"G{int(gn):02d}": continue
        if sc and p[1]!=sc: continue
        # IDs are G12-MATH-GS-001 for branched curricula and G07-MATH-001
        # otherwise. Never interpret the numeric lesson segment as a branch.
        explicit_branch = len(p)>=4 and not p[2].isdigit()
        if bc and explicit_branch and p[2]!=bc: continue
        lang=_norm(row.get("language") or "")
        if want_lang and lang:
            aliases={want_lang}
            if want_lang in {"english","en"}: aliases|={"english","en"}
            elif want_lang in {"french","fr","francais","français"}: aliases|={"french","fr","francais","français"}
            elif want_lang in {"arabic","ar","العربية"}: aliases|={"arabic","ar","العربية"}
            if lang not in aliases: continue
        seen.add(lid)
        out.append({"lesson_id":lid,"title":str(row.get("title") or lid),"version":str(row.get("version") or "0.01"),"language":str(row.get("language") or ""),"golden":True})
    out.sort(key=lambda x:x["lesson_id"])
    return out

def _artifact_path(lesson_id):
    safe=str(lesson_id or "").strip().upper()
    if not re.fullmatch(r"G\d{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3}",safe): raise HTTPException(422,"INVALID_LESSON_ID")
    return GOLDEN_ARTIFACT_DIR/f"{safe}.txt"

def _source_text(lesson_id, language="en", version="0.01"):
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
    from app.api import routes_interactive_lessons as legacy
    if getattr(app.state,"nabil_golden_runtime_bridge",False): return
    bridge=APIRouter()

    @bridge.get("/api/chat/curriculum/lessons")
    @bridge.get("/api/curriculum/lessons")
    def curriculum(grade:str="",subject:str="",language:str="",branch:str=""):
        rows=_catalogue(grade,subject,language,branch)
        return {"source":"canonical_golden_registry","runtime_ai":False,"count":len(rows),"lessons":rows}

    @bridge.get("/api/interactive-lessons/resolve")
    def resolve(grade:str,subject:str,lesson:str="",language:str="",lesson_id:str=""):
        entry=_golden_entry(grade,subject,lesson,lesson_id)
        if entry is None:
            if lesson_id: raise HTTPException(404,detail={"stage":"golden_registry","reason":"LESSON_ID_NOT_FOUND","lesson_id":lesson_id})
            return legacy.resolve(grade=grade,subject=subject,lesson=lesson,language=language)
        rid=str(entry["lesson_id"]); lang=str(entry.get("language") or language or "en"); ver=str(entry.get("version") or "0.01"); text,source=_source_text(rid,lang,ver)
        return {"found":True,"title":entry.get("title") or lesson,"url":"/api/interactive-lessons/golden-classroom?lesson_id="+quote(rid)+"&language="+quote(lang)+"&version="+quote(ver),"source":source,"bytes":len(text.encode()),"lesson_id":rid,"zero_ai":True,"renderer":"nabil_classroom_v13"}

    @bridge.get("/api/interactive-lessons/golden-classroom",response_class=HTMLResponse)
    def classroom(lesson_id:str,language:str="en",version:str="0.01"):
        from app.services.golden_store import get_registry_entry
        entry=get_registry_entry(lesson_id)
        if not entry or not entry.get("golden"): raise HTTPException(404,"GOLDEN_LESSON_NOT_FOUND")
        try:text,source=_source_text(lesson_id,language,version)
        except Exception as exc: raise HTTPException(503,detail={"stage":"golden_source","reason":type(exc).__name__,"message":str(exc)[:1000],"lesson_id":lesson_id}) from exc
        title=str(entry.get("title") or lesson_id)
        return HTMLResponse(_render_page(lesson_id,title,text,source),headers={"Cache-Control":"no-store, no-cache, must-revalidate","Pragma":"no-cache","Content-Security-Policy":"default-src 'self' data: blob:; script-src 'unsafe-inline' 'self'; style-src 'unsafe-inline' 'self'; frame-ancestors 'self'","X-NABIL-Lesson-Source":source,"X-NABIL-Lesson-ID":lesson_id,"X-NABIL-Renderer":"nabil-classroom-v13"})

    @bridge.get("/api/interactive-lessons/golden-structured-view",response_class=HTMLResponse)
    def old_structured(lesson_id:str): return classroom(lesson_id)
    @bridge.get("/api/interactive-lessons/golden-view",response_class=HTMLResponse)
    def old_drive(lesson_id:str,language:str="en",version:str="0.01"): return classroom(lesson_id,language,version)
    for route in reversed(bridge.routes): app.router.routes.insert(0,route)
    app.state.nabil_golden_runtime_bridge=True
