#!/usr/bin/env python3
"""Synchronize the existing canonical Golden registry to local verified snapshots.

Uses the lesson IDs/file IDs already present in data/golden_lesson_links.json, so it does
not require reorganizing Drive before fixing the student runtime. Drive is read only.
Last-good snapshots are retained on any export failure.
"""
from __future__ import annotations
import hashlib,json,os,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app.services.golden_registry import normalize

def _write(path,data):
 path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_name(path.name+".tmp");tmp.write_bytes(data);os.replace(tmp,path)

def _client():
 from google.oauth2 import service_account
 from googleapiclient.discovery import build
 info=json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])
 creds=service_account.Credentials.from_service_account_info(info,scopes=["https://www.googleapis.com/auth/drive.readonly","https://www.googleapis.com/auth/documents.readonly"])
 return build("drive","v3",credentials=creds,cache_discovery=False),build("docs","v1",credentials=creds,cache_discovery=False)

def _text(doc):
 out=[]
 for block in (doc.get("body") or {}).get("content",[]):
  p=block.get("paragraph")
  if not p:continue
  s="".join(str((e.get("textRun") or {}).get("content") or "") for e in p.get("elements",[])).strip()
  if not s:continue
  style=(p.get("paragraphStyle") or {}).get("namedStyleType","")
  if style.startswith("HEADING_"):
   try:s="#"*int(style.rsplit("_",1)[1])+" "+s
   except Exception:pass
  elif style=="TITLE":s="# "+s
  elif style=="SUBTITLE":s="## "+s
  out.append(s)
 return "\n\n".join(out).strip()+"\n"

def sync(repo=Path(".")):
 reg=repo/"data/golden_lesson_links.json";raw=json.loads(reg.read_text("utf-8"));lessons,_=normalize(raw);drive,docs=_client();now=time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime());report={"updated":[],"unchanged":[],"errors":[]}
 for lid,ent in sorted(lessons.items()):
  assets=ent.setdefault("assets",{});asset=assets.setdefault("lesson",{});fid=asset.get("drive_file_id") or ent.get("drive_file_id")
  if not fid:report["errors"].append(f"{lid}:NO_DRIVE_FILE_ID");continue
  try:
   meta=drive.files().get(fileId=fid,fields="id,name,mimeType,modifiedTime,version,webViewLink",supportsAllDrives=True).execute();prev_path=asset.get("content_path")
   if asset.get("status")=="ok" and asset.get("modified_time")==meta.get("modifiedTime") and prev_path and (repo/prev_path).is_file():report["unchanged"].append(lid);continue
   if meta.get("mimeType")!="application/vnd.google-apps.document":raise RuntimeError("LESSON_NOT_GOOGLE_DOC")
   doc=docs.documents().get(documentId=fid).execute();md=_text(doc)
   if len(md.strip())<20:raise RuntimeError("EMPTY_DOCUMENT")
   snap=json.dumps({"lesson_id":lid,"kind":"lesson","title":ent.get("title") or doc.get("title") or lid,"markdown":md},ensure_ascii=False,indent=1).encode();rel=f"data/golden/{lid}/lesson.json";_write(repo/rel,snap)
   asset.update({"drive_file_id":fid,"drive_url":meta.get("webViewLink") or ent.get("drive_url"),"mime":meta.get("mimeType"),"modified_time":meta.get("modifiedTime"),"version":str(meta.get("version") or ent.get("version") or "0.01"),"sha256":hashlib.sha256(snap).hexdigest(),"content_path":rel,"status":"ok","synced_at":now,"error":None});report["updated"].append(lid)
  except Exception as e:
   asset["status"]="stale" if asset.get("content_path") else "error";asset["error"]=f"{type(e).__name__}:{e}";asset["last_error_at"]=now;report["errors"].append(f"{lid}:{type(e).__name__}:{e}")
 # Preserve lesson metadata while upgrading to schema 2.
 for lid,ent in lessons.items():
  if "title" not in ent:
   old=(raw.get("lessons") or {}).get(lid,{}) if isinstance(raw,dict) else {};ent["title"]=old.get("title") or lid;ent["language"]=old.get("language") or "";ent["version"]=old.get("version") or "0.01";ent["golden"]=True
 _write(reg,(json.dumps({"schema":2,"generated_at":now,"lessons":lessons},ensure_ascii=False,indent=1,sort_keys=True)+"\n").encode());return report

if __name__=="__main__":
 r=sync(Path("."));print(json.dumps(r,ensure_ascii=False,indent=1));sys.exit(1 if r["errors"] else 0)
