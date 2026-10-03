"""Production bridge: every Golden lesson -> one structured NABIL classroom renderer.

There is deliberately no raw Google-Doc/iframe rendering path here.  Whether a
lesson comes from a checked-in structured artifact or the immutable Drive Golden
package, the student sees the same renderer and the same teaching runtime.
"""
from __future__ import annotations
import html,json,re
from pathlib import Path
from urllib.parse import quote
from fastapi import APIRouter,HTTPException
from fastapi.responses import HTMLResponse

GOLDEN_ARTIFACT_DIR=Path("data/golden_artifacts")
RENDERER_URL="/static/nabil_golden_structured_renderer_v1.js?v=7"
LAB_THEME_URL="/static/nabil_lab_reference_theme_v1.js?v=2"

def _norm(v):return re.sub(r"[^a-z0-9\u0600-\u06ff]+","",str(v or "").casefold())
def _grade_number(v):
 raw=str(v or "");compact=_norm(raw)
 if "الثالثثانوي" in raw.replace(" ",""):return "12"
 if "الثانيثانوي" in raw.replace(" ",""):return "11"
 if "الأولثانوي" in raw.replace(" ",""):return "10"
 m=re.search(r"(?:grade|g|eb)?0?([1-9]|1[0-2])",compact);return str(int(m.group(1))) if m else ""
def _subject_code(v):
 raw=str(v or "").casefold();compact=_norm(raw)
 if "رياض" in raw or compact in {"math","maths","mathematics","mathematiques"}:return "MATH"
 if "فيز" in raw or compact in {"physics","physique"}:return "PHYSICS"
 if "كيمي" in raw or compact in {"chemistry","chimie"}:return "CHEMISTRY"
 if "biology" in compact or "biologie" in compact or "علومالحياة" in raw.replace(" ",""):return "BIOLOGY"
 return ""
def _golden_entry(grade,subject,lesson,lesson_id=""):
 from app.services.golden_store import get_registry_entry,list_registry_entries
 requested=str(lesson_id or "").strip().upper();as_id=str(lesson or "").strip().upper()
 if not requested and re.fullmatch(r"G\d{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3}",as_id):requested=as_id
 if requested:
  row=get_registry_entry(requested);return row if row and row.get("golden") else None
 gn,sc,wanted=_grade_number(grade),_subject_code(subject),_norm(lesson);matches=[]
 for row in list_registry_entries():
  rid=str(row.get("lesson_id") or "").upper();title=str(row.get("title") or "")
  if not row.get("golden") or _norm(title)!=wanted:continue
  p=rid.split("-")
  if gn and (not p or p[0]!=f"G{int(gn):02d}"):continue
  if sc and (len(p)<2 or p[1]!=sc):continue
  matches.append(row)
 if len(matches)>1:raise HTTPException(409,"Multiple Golden lessons match this title; send lesson_id.")
 return matches[0] if matches else None
def _artifact_path(lesson_id):
 safe=str(lesson_id or "").strip().upper()
 if not re.fullmatch(r"G\d{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3}",safe):raise HTTPException(422,"INVALID_LESSON_ID")
 return GOLDEN_ARTIFACT_DIR/f"{safe}.txt"
def _source_text(lesson_id,language="en",version="0.01"):
 """Return canonical Golden teaching text; never return raw Drive HTML."""
 path=_artifact_path(lesson_id)
 if path.exists():
  text=path.read_text(encoding="utf-8").strip()
  if text:return text,"golden_structured_artifact"
 from app.services.golden_store import fetch_golden_from_drive
 payload=fetch_golden_from_drive(lesson_id,language,version)
 # The visible text extracted from the canonical lesson is the renderer input.
 # Raw HTML/Google preview is intentionally never exposed to students.
 text=str(payload.get("reply") or "").strip()
 if not text:raise RuntimeError(f"GOLDEN_TEACHING_TEXT_EMPTY:{lesson_id}")
 return text,"golden_drive_structured"
def _render_page(lesson_id,title,text,source):
 jt=json.dumps(text,ensure_ascii=False).replace("</","<\\/");jtitle=json.dumps(title,ensure_ascii=False).replace("</","<\\/")
 return f'''<!doctype html><html lang="ar"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="nabil-lesson-id" content="{html.escape(lesson_id)}"><meta name="nabil-canonical-title" content="{html.escape(title)}"><meta name="nabil-source" content="{html.escape(source)}"><title>{html.escape(title)}</title></head><body style="margin:0;background:#06111f"><div id="boot" style="color:#dff7ff;padding:20px;font-family:Arial">Loading NABIL Golden lesson…</div><script src="{RENDERER_URL}"></script><script>(function(){{try{{const r=window.NABILGoldenStructured;if(!r||typeof r.render!=='function')throw new Error('RENDERER_NOT_LOADED');const doc=r.render({jt},{jtitle});document.open();document.write(doc);document.close();setTimeout(()=>{{try{{r.bind&&r.bind();}}catch(e){{console.error(e)}}}},0);}}catch(e){{console.error('NABIL_GOLDEN_RENDER_ERROR',e);document.body.innerHTML='<pre style="color:white;white-space:pre-wrap;padding:16px">'+String(e&&e.stack||e)+'</pre>';}}}})();</script></body></html>'''
def install_golden_runtime_bridge():
 from app.main import app
 from app.api import routes_interactive_lessons as legacy
 if getattr(app.state,"nabil_golden_runtime_bridge",False):return
 bridge=APIRouter(prefix="/api/interactive-lessons")
 @bridge.get("/resolve")
 def resolve(grade:str,subject:str,lesson:str="",language:str="",lesson_id:str=""):
  entry=_golden_entry(grade,subject,lesson,lesson_id)
  if entry is None:
   if lesson_id:raise HTTPException(404,detail={"stage":"golden_registry","reason":"LESSON_ID_NOT_FOUND","lesson_id":lesson_id})
   return legacy.resolve(grade=grade,subject=subject,lesson=lesson,language=language)
  rid=str(entry["lesson_id"]);lang=str(entry.get("language") or language or "en");ver=str(entry.get("version") or "0.01")
  try:text,source=_source_text(rid,lang,ver)
  except Exception as exc:raise HTTPException(503,detail={"stage":"golden_source","reason":type(exc).__name__,"message":str(exc)[:1200],"lesson_id":rid}) from exc
  return {"found":True,"title":entry.get("title") or lesson,"url":"/api/interactive-lessons/golden-classroom?lesson_id="+quote(rid)+"&language="+quote(lang)+"&version="+quote(ver),"source":source,"bytes":len(text.encode()),"lesson_id":rid,"zero_ai":True,"renderer":"unified_structured_v7"}
 @bridge.get("/golden-classroom",response_class=HTMLResponse)
 def classroom(lesson_id:str,language:str="en",version:str="0.01"):
  from app.services.golden_store import get_registry_entry
  entry=get_registry_entry(lesson_id)
  if not entry or not entry.get("golden"):raise HTTPException(404,"GOLDEN_LESSON_NOT_FOUND")
  try:text,source=_source_text(lesson_id,language,version)
  except Exception as exc:raise HTTPException(503,detail={"stage":"golden_source","reason":type(exc).__name__,"message":str(exc)[:1200],"lesson_id":lesson_id}) from exc
  title=str(entry.get("title") or lesson_id)
  return HTMLResponse(_render_page(lesson_id,title,text,source),headers={"Cache-Control":"no-store","Content-Security-Policy":"default-src 'self' data: blob:; script-src 'unsafe-inline' 'self'; style-src 'unsafe-inline' 'self'; frame-ancestors 'self'","X-NABIL-Lesson-Source":source,"X-NABIL-Lesson-ID":lesson_id,"X-NABIL-Renderer":"unified-structured-v7"})
 # Old URLs remain aliases but now go through the exact same renderer.
 @bridge.get("/golden-structured-view",response_class=HTMLResponse)
 def old_structured(lesson_id:str):return classroom(lesson_id)
 @bridge.get("/golden-view",response_class=HTMLResponse)
 def old_drive(lesson_id:str,language:str="en",version:str="0.01"):return classroom(lesson_id,language,version)
 for route in reversed(bridge.routes):app.router.routes.insert(0,route)
 app.state.nabil_golden_runtime_bridge=True
