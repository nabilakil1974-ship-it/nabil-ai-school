"""Snapshot-backed Golden registry.

Runtime catalogue contract:
  lesson_id -> data/NABIL_GOLDEN_CATALOGUE.json
Runtime content contract:
  lesson_id -> verified local snapshot when available.

The student runtime never scans Google Drive. Maintainers update the canonical
catalogue whenever a new Golden lesson/material is completed. SUPERSEDED files
must never be entered in the canonical catalogue.
"""
from __future__ import annotations
import hashlib, json, os, re, threading
from pathlib import Path

LESSON_ID_RE=re.compile(r"^G(?:0[1-9]|1[0-2])-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3}$",re.I)
KINDS=("lesson","exercises","worksheet","lab","pptx")
_lock=threading.Lock(); _cache={"key":None,"lessons":{},"dups":set()}

def registry_path(): return Path(os.getenv("GOLDEN_REGISTRY","data/NABIL_GOLDEN_CATALOGUE.json"))
def data_root(): return Path(os.getenv("GOLDEN_DATA_ROOT",".")).resolve()

def _legacy_asset(it):
 return {"drive_file_id":it.get("drive_file_id"),"drive_url":it.get("drive_url"),"status":it.get("status") or "link_only"}

def normalize(raw):
 lessons={}; dups=set()
 if not isinstance(raw,dict): return lessons,dups
 src=raw.get("lessons")
 # Canonical maintained catalogue: {schema_version, lessons:[...]}
 if isinstance(src,list):
  for it in src:
   if not isinstance(it,dict): continue
   lid=str(it.get("lesson_id") or "").upper()
   if not LESSON_ID_RE.fullmatch(lid): continue
   if str(it.get("title") or "").strip().upper().startswith("SUPERSEDED"): continue
   if lid in lessons: dups.add(lid); continue
   ent=dict(it); ent["assets"]={"lesson":_legacy_asset(it)}
   lessons[lid]=ent
  return lessons,dups
 # Snapshot schema retained for compatibility if an explicitly configured registry uses it.
 if raw.get("schema")==2 and isinstance(src,dict):
  for lid,ent in src.items():
   lid=str(lid).upper()
   if LESSON_ID_RE.fullmatch(lid) and isinstance(ent,dict) and isinstance(ent.get("assets"),dict): lessons[lid]=ent
  return lessons,dups
 if isinstance(src,dict):
  for key,val in src.items():
   if not isinstance(val,dict): continue
   lid=str(val.get("lesson_id") or key).upper()
   if not LESSON_ID_RE.fullmatch(lid): continue
   if str(val.get("title") or "").strip().upper().startswith("SUPERSEDED"): continue
   if lid in lessons: dups.add(lid); continue
   ent=dict(val)
   if not isinstance(ent.get("assets"),dict): ent["assets"]={"lesson":_legacy_asset(val)}
   lessons[lid]=ent
 return lessons,dups

def load():
 p=registry_path()
 try: st=p.stat()
 except OSError: return {},set()
 key=(str(p.resolve()),st.st_mtime_ns,st.st_size)
 with _lock:
  if _cache["key"]!=key:
   try: lessons,dups=normalize(json.loads(p.read_text("utf-8")))
   except (OSError,ValueError,TypeError):
    if _cache["key"] is not None:return _cache["lessons"],_cache["dups"]
    return {},set()
   _cache.update(key=key,lessons=lessons,dups=dups)
  return _cache["lessons"],_cache["dups"]

def rows():
 lessons,dups=load(); out=[]
 for lid,ent in sorted(lessons.items()):
  if lid in dups: continue
  a=(ent.get("assets") or {}).get("lesson") or {}
  out.append({"lesson_id":lid,"title":str(ent.get("title") or lid),"language":str(ent.get("language") or ""),"version":str(ent.get("version") or a.get("version") or "0.01"),"drive_file_id":a.get("drive_file_id") or ent.get("drive_file_id"),"drive_url":a.get("drive_url") or ent.get("drive_url"),"golden":True,"status":a.get("status") or ent.get("status") or "available"})
 return out

def _read_snapshot(asset):
 rel=str(asset.get("content_path") or "").strip()
 if not rel:return None
 root=data_root(); p=(root/rel).resolve()
 try:p.relative_to(root)
 except ValueError:return None
 try:b=p.read_bytes()
 except OSError:return None
 want=str(asset.get("sha256") or "").lower()
 if not want or hashlib.sha256(b).hexdigest()!=want:return None
 if p.suffix.lower()==".json":
  try:return json.loads(b.decode("utf-8"))
  except (ValueError,UnicodeDecodeError):return None
 return b

def get_asset(lesson_id,kind="lesson"):
 lid=str(lesson_id or "").upper()
 if not LESSON_ID_RE.fullmatch(lid):return None
 lessons,dups=load()
 if lid in dups:return None
 ent=lessons.get(lid)
 if not ent:return None
 asset=(ent.get("assets") or {}).get(kind)
 if not isinstance(asset,dict):return None
 content=_read_snapshot(asset)
 if content is None:return None
 return {"lesson_id":lid,"kind":kind,"entry":ent,"asset":asset,"content":content,"via":"snapshot"}

def lesson_text(lesson_id):
 res=get_asset(lesson_id,"lesson")
 if not res:return None
 content=res["content"]
 if isinstance(content,dict):
  text=content.get("markdown") or content.get("text") or content.get("content")
  return str(text).strip() if text else None
 if isinstance(content,(bytes,bytearray)):
  try:return bytes(content).decode("utf-8").strip()
  except UnicodeDecodeError:return None
 return str(content).strip() if content else None
