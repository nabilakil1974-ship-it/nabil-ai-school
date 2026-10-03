"""Production bridge: Golden lesson registry -> verified artifact -> structured NABIL lesson.
Runtime is deterministic and zero-AI for source content. lesson_id is canonical.
"""
from __future__ import annotations
import html,re
from pathlib import Path
from urllib.parse import quote
from fastapi import APIRouter,HTTPException
from fastapi.responses import HTMLResponse
GOLDEN_ARTIFACT_DIR=Path("data/golden_artifacts");RENDERER_URL="/static/nabil_golden_structured_renderer_v1.js?v=5"
def _norm(v):return re.sub(r"[^a-z0-9]+","",str(v or "").casefold())
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
 if not requested and re.fullmatch(r"G\d{2}-[A-Z]+(?:-[A-Z]+)?-\d{3}",as_id):requested=as_id
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
 if not re.fullmatch(r"G\d{2}-[A-Z]+(?:-[A-Z]+)?-\d{3}",safe):raise HTTPException(422,"INVALID_LESSON_ID")
 return GOLDEN_ARTIFACT_DIR/f"{safe}.txt"
def install_golden_runtime_bridge():
 from app.main import app
 from app.api import routes_interactive_lessons as legacy
 from app.services.golden_store import fetch_golden_from_drive
 if getattr(app.state,"nabil_golden_runtime_bridge",False):return
 bridge=APIRouter(prefix="/api/interactive-lessons")
 @bridge.get("/resolve")
 def resolve(grade:str,subject:str,lesson:str="",language:str="",lesson_id:str=""):
  entry=_golden_entry(grade,subject,lesson,lesson_id)
  if entry is None:
   if lesson_id:raise HTTPException(404,detail={"stage":"golden_registry","reason":"LESSON_ID_NOT_FOUND","lesson_id":lesson_id})
   return legacy.resolve(grade=grade,subject=subject,lesson=lesson,language=language)
  rid=str(entry["lesson_id"]);artifact=_artifact_path(rid)
  if artifact.exists():return {"found":True,"title":entry.get("title") or lesson,"url":"/api/interactive-lessons/golden-structured-view?lesson_id="+quote(rid),"source":"golden_structured_artifact","bytes":artifact.stat().st_size,"lesson_id":rid,"zero_ai":True,"resolved_by":"lesson_id" if lesson_id else "title_fallback"}
  lang=str(entry.get("language") or language or "en");version=str(entry.get("version") or "0.01")
  try:payload=fetch_golden_from_drive(rid,lang,version)
  except Exception as exc:raise HTTPException(503,detail={"stage":"golden_drive","reason":type(exc).__name__,"message":str(exc)[:1200],"lesson_id":rid}) from exc
  return {"found":True,"title":payload.get("title") or entry.get("title") or lesson,"url":"/api/interactive-lessons/golden-view?lesson_id="+quote(rid)+"&language="+quote(lang)+"&version="+quote(version),"source":"golden_drive_zero_ai","bytes":len((payload.get("lesson_html") or payload.get("reply") or "").encode()),"lesson_id":rid,"zero_ai":True}
 @bridge.get("/golden-structured-view",response_class=HTMLResponse)
 def view(lesson_id:str):
  import json
  from app.services.golden_store import get_registry_entry
  entry=get_registry_entry(lesson_id)
  if not entry or not entry.get("golden"):raise HTTPException(404,"GOLDEN_LESSON_NOT_FOUND")
  path=_artifact_path(lesson_id)
  if not path.exists():raise HTTPException(404,detail={"stage":"golden_artifact","reason":"ARTIFACT_NOT_SYNCED","lesson_id":lesson_id})
  text=path.read_text(encoding="utf-8").strip()
  if not text:raise HTTPException(500,detail={"stage":"golden_artifact","reason":"EMPTY_ARTIFACT","lesson_id":lesson_id})
  title=str(entry.get("title") or lesson_id);jt=json.dumps(text,ensure_ascii=False).replace("</","<\\/");jtitle=json.dumps(title,ensure_ascii=False).replace("</","<\\/")
  markup=f'''<!doctype html><html lang="ar"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="nabil-lesson-id" content="{html.escape(lesson_id)}"><meta name="nabil-canonical-title" content="{html.escape(title)}"><title>{html.escape(title)}</title></head><body style="margin:0;background:#071d30"><div id="boot" style="color:#dff7ff;padding:20px;font-family:Arial">Loading NABIL teaching lesson…</div><script src="{RENDERER_URL}"></script><script>(function(){{try{{if(!window.NABILGoldenStructuredRenderer)throw new Error('RENDERER_NOT_LOADED');const doc=window.NABILGoldenStructuredRenderer.render({jt},{jtitle});document.open();document.write(doc);document.close();setTimeout(()=>window.NABILGoldenStructuredRenderer.activate(document),0);}}catch(e){{console.error('NABIL_GOLDEN_RENDER_ERROR',e);document.body.innerHTML='<pre style="color:white">'+String(e&&e.stack||e)+'</pre>';}}}})();</script></body></html>'''
  return HTMLResponse(markup,headers={"Cache-Control":"no-store","Content-Security-Policy":"default-src 'self' data: blob:; script-src 'unsafe-inline' 'self'; style-src 'unsafe-inline' 'self'; frame-ancestors 'self'","X-NABIL-Lesson-Source":"golden-structured-artifact","X-NABIL-Lesson-ID":lesson_id,"X-NABIL-Renderer":"teaching-v5"})
 @bridge.get("/golden-view",response_class=HTMLResponse)
 def drive_view(lesson_id:str,language:str="en",version:str="0.01"):
  try:payload=fetch_golden_from_drive(lesson_id,language,version)
  except Exception as exc:raise HTTPException(503,detail={"stage":"golden_drive","reason":type(exc).__name__,"message":str(exc)[:1200],"lesson_id":lesson_id}) from exc
  markup=str(payload.get("lesson_html") or "").strip()
  if not markup:markup="<!doctype html><html><body><pre>"+html.escape(str(payload.get("reply") or ""))+"</pre></body></html>"
  return HTMLResponse(markup,headers={"Cache-Control":"private, no-store","X-NABIL-Lesson-Source":"golden-drive-zero-ai","X-NABIL-Lesson-ID":lesson_id})
 for route in reversed(bridge.routes):app.router.routes.insert(0,route)
 app.state.nabil_golden_runtime_bridge=True
