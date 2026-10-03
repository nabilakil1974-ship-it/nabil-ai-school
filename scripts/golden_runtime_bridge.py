"""Production bridge: Golden lesson registry -> verified artifact -> structured NABIL lesson.

Runtime is deterministic and zero-AI. lesson_id is canonical. During acceptance
we expose a temporary diagnostic panel; remove it after live validation.
"""
from __future__ import annotations

import html
import re
from pathlib import Path
from urllib.parse import quote

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

GOLDEN_ARTIFACT_DIR = Path("data/golden_artifacts")
RENDERER_URL = "/static/nabil_golden_structured_renderer_v1.js"


def _norm(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(value or "").casefold())


def _grade_number(value: str) -> str:
    raw = str(value or "")
    compact = _norm(raw)
    if "الثالثثانوي" in raw.replace(" ", ""): return "12"
    if "الثانيثانوي" in raw.replace(" ", ""): return "11"
    if "الأولثانوي" in raw.replace(" ", ""): return "10"
    m = re.search(r"(?:grade|g|eb)?0?([1-9]|1[0-2])", compact)
    return str(int(m.group(1))) if m else ""


def _subject_code(value: str) -> str:
    raw = str(value or "").casefold(); compact = _norm(raw)
    if "رياض" in raw or compact in {"math","maths","mathematics","mathematiques"}: return "MATH"
    if "فيز" in raw or compact in {"physics","physique"}: return "PHYSICS"
    if "كيمي" in raw or compact in {"chemistry","chimie"}: return "CHEMISTRY"
    if "biology" in compact or "biologie" in compact or "علومالحياة" in raw.replace(" ", ""): return "BIOLOGY"
    return ""


def _golden_entry(grade: str, subject: str, lesson: str, lesson_id: str = ""):
    from app.services.golden_store import get_registry_entry, list_registry_entries
    requested_id = str(lesson_id or "").strip().upper()
    lesson_as_id = str(lesson or "").strip().upper()
    if not requested_id and re.fullmatch(r"G\d{2}-[A-Z]+(?:-[A-Z]+)?-\d{3}", lesson_as_id): requested_id = lesson_as_id
    if requested_id:
        row = get_registry_entry(requested_id)
        return row if row and row.get("golden") else None
    grade_no, subject_code, wanted = _grade_number(grade), _subject_code(subject), _norm(lesson)
    matches=[]
    for row in list_registry_entries():
        row_id=str(row.get("lesson_id") or "").upper(); title=str(row.get("title") or "")
        if not row.get("golden") or _norm(title)!=wanted: continue
        parts=row_id.split("-")
        if grade_no and (not parts or parts[0] != f"G{int(grade_no):02d}"): continue
        if subject_code and (len(parts)<2 or parts[1]!=subject_code): continue
        matches.append(row)
    if len(matches)>1: raise HTTPException(409,"Multiple Golden lessons match this title; send lesson_id.")
    return matches[0] if matches else None


def _artifact_path(lesson_id: str) -> Path:
    safe = str(lesson_id or "").strip().upper()
    if not re.fullmatch(r"G\d{2}-[A-Z]+(?:-[A-Z]+)?-\d{3}", safe): raise HTTPException(422,"INVALID_LESSON_ID")
    return GOLDEN_ARTIFACT_DIR / f"{safe}.txt"


def _diagnostic_markup(stage: str, lesson_id: str, detail: str = "") -> str:
    return "<aside id='nabilDiag' style='position:fixed;z-index:99999;right:8px;bottom:8px;max-width:92vw;background:#250b0b;color:#ffd7d7;border:1px solid #ff6b6b;border-radius:10px;padding:8px 10px;font:12px/1.35 monospace'>TEST DIAGNOSTIC · stage="+html.escape(stage)+" · lesson="+html.escape(lesson_id)+(" · "+html.escape(detail) if detail else "")+"</aside>"


def install_golden_runtime_bridge() -> None:
    from app.main import app
    from app.api import routes_interactive_lessons as legacy
    from app.services.golden_store import fetch_golden_from_drive
    if getattr(app.state,"nabil_golden_runtime_bridge",False): return
    bridge=APIRouter(prefix="/api/interactive-lessons")

    @bridge.get("/resolve")
    def golden_first_resolve(grade:str, subject:str, lesson:str="", language:str="", lesson_id:str=""):
        entry=_golden_entry(grade,subject,lesson,lesson_id=lesson_id)
        if entry is None:
            if lesson_id: raise HTTPException(404,detail={"stage":"golden_registry","reason":"LESSON_ID_NOT_FOUND","lesson_id":lesson_id})
            return legacy.resolve(grade=grade,subject=subject,lesson=lesson,language=language)
        resolved_id=str(entry["lesson_id"])
        artifact=_artifact_path(resolved_id)
        if artifact.exists():
            return {"found":True,"title":entry.get("title") or lesson,"url":"/api/interactive-lessons/golden-structured-view?lesson_id="+quote(resolved_id),"source":"golden_structured_artifact","bytes":artifact.stat().st_size,"lesson_id":resolved_id,"zero_ai":True,"resolved_by":"lesson_id" if lesson_id else "title_fallback"}
        lang=str(entry.get("language") or language or "en"); version=str(entry.get("version") or "0.01")
        try: payload=fetch_golden_from_drive(resolved_id,lang,version)
        except Exception as exc: raise HTTPException(503,detail={"stage":"golden_drive","reason":type(exc).__name__,"message":str(exc)[:1200],"lesson_id":resolved_id}) from exc
        return {"found":True,"title":payload.get("title") or entry.get("title") or lesson,"url":"/api/interactive-lessons/golden-view?lesson_id="+quote(resolved_id)+"&language="+quote(lang)+"&version="+quote(version),"source":"golden_drive_zero_ai","bytes":len((payload.get("lesson_html") or payload.get("reply") or "").encode("utf-8")),"lesson_id":resolved_id,"zero_ai":True}

    @bridge.get("/golden-structured-view",response_class=HTMLResponse)
    def golden_structured_view(lesson_id:str):
        from app.services.golden_store import get_registry_entry
        entry=get_registry_entry(lesson_id)
        if not entry or not entry.get("golden"): raise HTTPException(404,"GOLDEN_LESSON_NOT_FOUND")
        path=_artifact_path(lesson_id)
        if not path.exists(): raise HTTPException(404,detail={"stage":"golden_artifact","reason":"ARTIFACT_NOT_SYNCED","lesson_id":lesson_id})
        text=path.read_text(encoding="utf-8").strip()
        if not text: raise HTTPException(500,detail={"stage":"golden_artifact","reason":"EMPTY_ARTIFACT","lesson_id":lesson_id})
        title=str(entry.get("title") or lesson_id)
        # JSON encoding prevents source text from becoming executable markup.
        import json
        js_text=json.dumps(text,ensure_ascii=False).replace("</","<\\/")
        js_title=json.dumps(title,ensure_ascii=False).replace("</","<\\/")
        diag=_diagnostic_markup("structured_renderer",lesson_id,"artifact=OK renderer=pending")
        markup=f"""<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{html.escape(title)}</title></head><body style='margin:0;background:#071d30'><div id='boot' style='color:#dff7ff;padding:20px;font-family:Arial'>Loading NABIL structured lesson…</div>{diag}<script src='{RENDERER_URL}'></script><script>
(function(){{
 const diag=document.getElementById('nabilDiag');
 try {{
   if(!window.NABILGoldenStructuredRenderer) throw new Error('RENDERER_NOT_LOADED');
   const doc=window.NABILGoldenStructuredRenderer.render({js_text},{js_title});
   document.open(); document.write(doc); document.close();
   window.addEventListener('load',()=>{{try{{window.NABILGoldenStructuredRenderer.activate(document);}}catch(e){{console.error(e);}}}});
 }} catch(e) {{
   console.error('NABIL_GOLDEN_RENDER_ERROR',e);
   document.getElementById('boot').innerHTML='<h2>Golden renderer failed</h2><pre>'+String(e && (e.stack||e.message)||e).replace(/[&<>]/g,s=>({{'&':'&amp;','<':'&lt;','>':'&gt;'}}[s]))+'</pre>';
   if(diag) diag.textContent='TEST DIAGNOSTIC · stage=structured_renderer · lesson={html.escape(lesson_id)} · ERROR='+String(e && e.message || e);
 }}
}})();
</script></body></html>"""
        return HTMLResponse(markup,headers={"Cache-Control":"no-store","Content-Security-Policy":"default-src 'self' data: blob:; script-src 'unsafe-inline' 'self'; style-src 'unsafe-inline' 'self'; frame-ancestors 'self'","X-NABIL-Lesson-Source":"golden-structured-artifact","X-NABIL-Lesson-ID":lesson_id})

    @bridge.get("/golden-view",response_class=HTMLResponse)
    def golden_view(lesson_id:str,language:str="en",version:str="0.01"):
        try: payload=fetch_golden_from_drive(lesson_id,language,version)
        except Exception as exc: raise HTTPException(503,detail={"stage":"golden_drive","reason":type(exc).__name__,"message":str(exc)[:1200],"lesson_id":lesson_id}) from exc
        markup=str(payload.get("lesson_html") or "").strip()
        if not markup:
            text=html.escape(str(payload.get("reply") or "")); markup="<!doctype html><html><body style='background:#071d30;color:#eefaff'><pre style='white-space:pre-wrap'>"+text+"</pre></body></html>"
        return HTMLResponse(markup,headers={"Cache-Control":"private, no-store","X-NABIL-Lesson-Source":"golden-drive-zero-ai","X-NABIL-Lesson-ID":lesson_id})

    for route in reversed(bridge.routes): app.router.routes.insert(0,route)
    app.state.nabil_golden_runtime_bridge=True
