#!/usr/bin/env python3
"""Synchronize ONLY complete immutable NABIL Golden lesson packages from Drive.

A Golden lesson is generated/approved once, then rendered identically for every
student. Runtime AI must not regenerate canonical lesson content.

Every Drive artifact belonging to the same lesson_id is grouped into one package:
lesson/theory, activities, exercises, worksheets, solutions, visuals, labs,
master lab and Golden Card.  The package exposes stable artifact IDs/URLs and a
content fingerprint so the runtime can load/render the same approved package.
"""
from __future__ import annotations
import argparse, hashlib, json, re
from datetime import datetime, timezone
from pathlib import Path
from scripts.index_books import get_drive_service

REGISTRY=Path('data/golden_lessons_registry.json'); OUTPUT=Path('data/golden_lesson_links.json')
FIELDS='id,name,mimeType,modifiedTime,webViewLink,trashed,appProperties'
LESSON_RE=re.compile(r'\b(G(?:0[1-9]|1[0-2])-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3})\b',re.I)
REJECT_RE=re.compile(r'\b(SUPERSEDED|OLD|DRAFT|ARCHIVE|ARCHIVED|BACKUP|TEMPLATE|OBSOLETE)\b',re.I)
ARTIFACT_KINDS=('lesson','activities','exercises','worksheets','solutions','visuals','labs','master_lab','golden_card')

def _list(s,q):
 out=[]; token=None
 while True:
  r=s.files().list(q=q,fields=f'nextPageToken,files({FIELDS})',pageSize=1000,pageToken=token,supportsAllDrives=True,includeItemsFromAllDrives=True).execute();out+=r.get('files',[]);token=r.get('nextPageToken')
  if not token:return out

def _lid(x):
 p=x.get('appProperties') or {};v=str(p.get('nabil_lesson_id') or '').strip().upper()
 if LESSON_RE.fullmatch(v):return v
 m=LESSON_RE.search(str(x.get('name') or ''));return m.group(1).upper() if m else ''
def _explicit(x):return str((x.get('appProperties') or {}).get('nabil_golden') or '').lower()=='true'
def _golden(x):return _explicit(x) or bool(re.search(r'\bGOLDEN\b',str(x.get('name') or ''),re.I))
def _rank(x):return (_explicit(x),str(x.get('modifiedTime') or ''))
def _kind(x):
 p=x.get('appProperties') or {};a=str(p.get('nabil_artifact') or '').strip().lower().replace('-','_').replace(' ','_');n=str(x.get('name') or '').lower()
 aliases={'theory':'lesson','complete_lesson':'lesson','golden_lesson':'lesson','activity':'activities','exercise':'exercises','worksheet':'worksheets','solution':'solutions','visual':'visuals','diagram':'visuals','lab':'labs','masterlab':'master_lab','goldencard':'golden_card','summary_card':'golden_card'}
 if a in aliases:a=aliases[a]
 if a in ARTIFACT_KINDS:return a
 for k,words in [('master_lab',('master lab','smart board')),('golden_card',('golden card','summary card')),('activities',('activity','activities')),('exercises',('exercise','exercises','practice')),('worksheets',('worksheet','work sheet')),('solutions',('solution','answer key')),('visuals',('visual','diagram','graph')),('labs',('lab','laboratory','interactive'))]:
  if any(w in n for w in words):return k
 return 'lesson'
def _artifact(x):
 p=x.get('appProperties') or {};fid=str(x.get('id') or '');kind=_kind(x)
 return {'artifact_id':str(p.get('nabil_artifact_id') or f"{_lid(x)}-{kind.upper().replace('_','-')}-{fid[-8:]}").upper(),'kind':kind,'drive_file_id':fid,'name':x.get('name'),'url':str(x.get('webViewLink') or (f'https://drive.google.com/open?id={fid}' if fid else '')),'modified_time':x.get('modifiedTime'),'mime_type':x.get('mimeType')}
def _fingerprint(lid,artifacts):
 raw=json.dumps({'lesson_id':lid,'artifacts':[(a['artifact_id'],a['drive_file_id'],a['modified_time']) for a in artifacts]},sort_keys=True,separators=(',',':')).encode();return hashlib.sha256(raw).hexdigest()

def build_catalogue(registry_path=REGISTRY):
 s=get_drive_service()
 # Golden marker may live on the canonical lesson while satellite artifacts use
 # the same lesson_id. First identify Golden lesson IDs, then collect ALL their
 # non-draft artifacts so nothing is lost from the immutable package.
 all_docs=_list(s,"trashed = false")
 golden_ids={_lid(x) for x in all_docs if _lid(x) and _golden(x) and not REJECT_RE.search(str(x.get('name') or ''))}
 by={lid:[] for lid in golden_ids}
 for x in all_docs:
  lid=_lid(x)
  if lid in golden_ids and not REJECT_RE.search(str(x.get('name') or '')):by[lid].append(x)
 lessons={}
 for lid,files in sorted(by.items()):
  arts=sorted((_artifact(x) for x in files),key=lambda a:(ARTIFACT_KINDS.index(a['kind']),a['artifact_id']))
  groups={k:[a for a in arts if a['kind']==k] for k in ARTIFACT_KINDS}
  canonical=max([x for x in files if _kind(x)=='lesson'] or files,key=_rank);p=canonical.get('appProperties') or {};fid=str(canonical.get('id') or '')
  # Required runtime sections are explicit even when currently empty; this lets
  # quality gates reject incomplete Golden packages rather than silently invent.
  package={'package_schema':'nabil.golden.package.v1','lesson_id':lid,'generation_policy':'GENERATE_ONCE_RENDER_MANY','runtime_ai_generation':False,'immutable':True,'content_fingerprint':_fingerprint(lid,arts),'artifacts':groups,'artifact_count':len(arts)}
  lessons[lid]={'lesson_id':lid,'title':str(p.get('nabil_title') or canonical.get('name') or lid),'language':str(p.get('nabil_language') or 'en'),'version':str(p.get('nabil_version') or '0.01'),'grade':p.get('nabil_grade'),'subject':p.get('nabil_subject'),'branch':p.get('nabil_branch'),'golden':True,'status':'available','drive_file_id':fid,'drive_url':str(canonical.get('webViewLink') or f'https://drive.google.com/open?id={fid}'),'drive_modified_time':canonical.get('modifiedTime'),'mime_type':canonical.get('mimeType'),'sync_source':'drive_golden_package','package':package}
 counts={}
 for lid in lessons:counts[lid.split('-',1)[0]]=counts.get(lid.split('-',1)[0],0)+1
 return {'schema_version':'4.0','generated_at':datetime.now(timezone.utc).isoformat(),'source_of_truth':'google_drive','discovery_mode':'GOLDEN_ONLY_COMPLETE_PACKAGE','generation_policy':'GENERATE_ONCE_RENDER_MANY','runtime_ai_generation':False,'lesson_count':len(lessons),'available_lesson_count':len(lessons),'grade_counts':counts,'lessons':lessons}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--registry',default=str(REGISTRY));ap.add_argument('--output',default=str(OUTPUT));a=ap.parse_args();c=build_catalogue(Path(a.registry));o=Path(a.output);o.parent.mkdir(parents=True,exist_ok=True);o.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(f"SYNCED IMMUTABLE GOLDEN PACKAGES: {c['lesson_count']} lessons; grades={c['grade_counts']} -> {o}")
if __name__=='__main__':main()
