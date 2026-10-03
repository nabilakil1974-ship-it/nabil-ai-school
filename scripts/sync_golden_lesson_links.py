#!/usr/bin/env python3
"""Synchronize NABIL Golden lessons from Drive for Grades 1-12."""
from __future__ import annotations
import argparse, json, re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from scripts.index_books import get_drive_service

REGISTRY=Path("data/golden_lessons_registry.json")
OUTPUT=Path("data/golden_lesson_links.json")
FIELDS="id,name,mimeType,modifiedTime,webViewLink,trashed,appProperties"
DOC="application/vnd.google-apps.document"
LESSON_RE=re.compile(r"\b(G(?:0[1-9]|1[0-2])-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3})\b",re.I)
REJECT_RE=re.compile(r"\b(SUPERSEDED|OLD|DRAFT|ARCHIVE|ARCHIVED|BACKUP|TEMPLATE|OBSOLETE)\b",re.I)

def _registry(path:Path)->dict[str,Any]:
    if not path.exists(): return {}
    raw=json.loads(path.read_text(encoding="utf-8")); rows=raw.get("lessons",raw)
    return {str(k).upper():v for k,v in rows.items()} if isinstance(rows,dict) else {}

def _list(service,q):
    out=[]; token=None
    while True:
        r=service.files().list(q=q,fields=f"nextPageToken,files({FIELDS})",pageSize=1000,pageToken=token,supportsAllDrives=True,includeItemsFromAllDrives=True).execute()
        out.extend(r.get("files",[])); token=r.get("nextPageToken")
        if not token:return out

def _lid(row):
    p=row.get("appProperties") or {}; x=str(p.get("nabil_lesson_id") or "").strip().upper()
    if LESSON_RE.fullmatch(x):return x
    m=LESSON_RE.search(str(row.get("name") or "")); return m.group(1).upper() if m else ""

def _explicit(row):return str((row.get("appProperties") or {}).get("nabil_golden") or "").lower()=="true"
def _valid(row):return bool(_lid(row)) and (_explicit(row) or not REJECT_RE.search(str(row.get("name") or "")))
def _rank(row):
    p=row.get("appProperties") or {}; name=str(row.get("name") or "")
    return (_explicit(row),bool(re.search(r"\bGOLDEN\b",name,re.I)),str(p.get("nabil_artifact") or "").lower() in {"theory","lesson","golden_lesson","complete_lesson"},str(row.get("modifiedTime") or ""))

def build_catalogue(registry_path=REGISTRY):
    service=get_drive_service(); reg=_registry(Path(registry_path))
    explicit=_list(service,"trashed = false and appProperties has { key='nabil_golden' and value='true' }")
    docs=_list(service,f"trashed = false and mimeType = '{DOC}'")
    files={str(x.get('id')):x for x in docs if _valid(x)}
    files.update({str(x.get('id')):x for x in explicit})
    by={}; orphans=[]
    for x in files.values():
        lid=_lid(x)
        if lid:by.setdefault(lid,[]).append(x)
        elif _explicit(x):orphans.append({"id":x.get("id"),"name":x.get("name")})
    lessons={}
    for lid in sorted(set(reg)|set(by)):
        entry=reg.get(lid) if isinstance(reg.get(lid),dict) else {}
        candidates=by.get(lid,[]); x=max(candidates,key=_rank) if candidates else None
        fid=str((x or {}).get("id") or entry.get("drive_theory_id") or entry.get("drive_file_id") or "")
        url=str((x or {}).get("webViewLink") or entry.get("drive_url") or (f"https://docs.google.com/document/d/{fid}/edit" if fid else ""))
        p=(x or {}).get("appProperties") or {}
        lessons[lid]={"lesson_id":lid,"title":str(entry.get("title") or p.get("nabil_title") or (x or {}).get("name") or lid),"language":str(entry.get("language") or p.get("nabil_language") or "en"),"version":str(entry.get("version") or p.get("nabil_version") or "0.01"),"grade":entry.get("grade") or p.get("nabil_grade"),"subject":entry.get("subject") or p.get("nabil_subject"),"branch":entry.get("branch") or p.get("nabil_branch"),"golden":True,"status":"available" if x else "unavailable","drive_file_id":fid or None,"drive_url":url or None,"drive_modified_time":(x or {}).get("modifiedTime"),"mime_type":(x or {}).get("mimeType"),"artifact_type":p.get("nabil_artifact"),"sync_source":"drive_explicit_golden" if x and _explicit(x) else "drive_canonical_auto_discovery" if x else "registry_unavailable"}
    counts={}
    for lid,x in lessons.items():
        if x["status"]=="available":counts[lid.split('-',1)[0]]=counts.get(lid.split('-',1)[0],0)+1
    return {"schema_version":"3.0","generated_at":datetime.now(timezone.utc).isoformat(),"source_of_truth":"google_drive","discovery_mode":"metadata_plus_all_canonical_G01_to_G12_docs","lesson_count":len(lessons),"available_lesson_count":sum(x["status"]=="available" for x in lessons.values()),"grade_counts":counts,"orphan_golden_count":len(orphans),"orphan_golden_files":orphans,"lessons":lessons}

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--registry",default=str(REGISTRY));ap.add_argument("--output",default=str(OUTPUT));a=ap.parse_args()
    c=build_catalogue(Path(a.registry));o=Path(a.output);o.parent.mkdir(parents=True,exist_ok=True);o.write_text(json.dumps(c,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"SYNCED {c['available_lesson_count']}/{c['lesson_count']} Golden lessons; grades={c['grade_counts']}; orphans={c['orphan_golden_count']} -> {o}")
if __name__=="__main__":main()
