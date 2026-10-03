#!/usr/bin/env python3
"""Synchronize ONLY NABIL Golden lessons from Drive, Grades 1-12."""
from __future__ import annotations
import argparse,json,re
from datetime import datetime,timezone
from pathlib import Path
from scripts.index_books import get_drive_service
REGISTRY=Path('data/golden_lessons_registry.json'); OUTPUT=Path('data/golden_lesson_links.json')
FIELDS='id,name,mimeType,modifiedTime,webViewLink,trashed,appProperties'
LESSON_RE=re.compile(r'\b(G(?:0[1-9]|1[0-2])-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3})\b',re.I)
REJECT_RE=re.compile(r'\b(SUPERSEDED|OLD|DRAFT|ARCHIVE|ARCHIVED|BACKUP|TEMPLATE|OBSOLETE)\b',re.I)
def _list(s,q):
 out=[]; token=None
 while True:
  r=s.files().list(q=q,fields=f'nextPageToken,files({FIELDS})',pageSize=1000,pageToken=token,supportsAllDrives=True,includeItemsFromAllDrives=True).execute(); out+=r.get('files',[]); token=r.get('nextPageToken')
  if not token:return out
def _lid(x):
 p=x.get('appProperties') or {}; v=str(p.get('nabil_lesson_id') or '').strip().upper()
 if LESSON_RE.fullmatch(v):return v
 m=LESSON_RE.search(str(x.get('name') or '')); return m.group(1).upper() if m else ''
def _explicit(x):return str((x.get('appProperties') or {}).get('nabil_golden') or '').lower()=='true'
def _golden(x):return _explicit(x) or bool(re.search(r'\bGOLDEN\b',str(x.get('name') or ''),re.I))
def _rank(x):return (_explicit(x),str(x.get('modifiedTime') or ''))
def build_catalogue(registry_path=REGISTRY):
 s=get_drive_service(); docs=_list(s,"trashed = false and mimeType = 'application/vnd.google-apps.document'")
 docs=[x for x in docs if _golden(x) and _lid(x) and not REJECT_RE.search(str(x.get('name') or ''))]
 by={}
 for x in docs:by.setdefault(_lid(x),[]).append(x)
 lessons={}
 for lid,candidates in sorted(by.items()):
  x=max(candidates,key=_rank); p=x.get('appProperties') or {}; fid=str(x.get('id') or ''); url=str(x.get('webViewLink') or f'https://docs.google.com/document/d/{fid}/edit')
  lessons[lid]={'lesson_id':lid,'title':str(p.get('nabil_title') or x.get('name') or lid),'language':str(p.get('nabil_language') or 'en'),'version':str(p.get('nabil_version') or '0.01'),'grade':p.get('nabil_grade'),'subject':p.get('nabil_subject'),'branch':p.get('nabil_branch'),'golden':True,'status':'available','drive_file_id':fid,'drive_url':url,'drive_modified_time':x.get('modifiedTime'),'mime_type':x.get('mimeType'),'artifact_type':p.get('nabil_artifact'),'sync_source':'drive_explicit_golden' if _explicit(x) else 'drive_name_golden'}
 counts={}
 for lid in lessons:counts[lid.split('-',1)[0]]=counts.get(lid.split('-',1)[0],0)+1
 return {'schema_version':'3.1','generated_at':datetime.now(timezone.utc).isoformat(),'source_of_truth':'google_drive','discovery_mode':'GOLDEN_ONLY_metadata_or_name','lesson_count':len(lessons),'available_lesson_count':len(lessons),'grade_counts':counts,'lessons':lessons}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--registry',default=str(REGISTRY));ap.add_argument('--output',default=str(OUTPUT));a=ap.parse_args();c=build_catalogue(Path(a.registry));o=Path(a.output);o.parent.mkdir(parents=True,exist_ok=True);o.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(f"SYNCED GOLDEN ONLY: {c['lesson_count']} lessons; grades={c['grade_counts']} -> {o}")
if __name__=='__main__':main()
