#!/usr/bin/env python3
"""Drive -> canonical catalogue -> verified snapshots for NABIL runtime.
The canonical membership source is data/NABIL_GOLDEN_CATALOGUE.json (ALL_GOLDEN).
Google is read-only. A failed refresh never deletes a last-good snapshot.
"""
from __future__ import annotations
import hashlib,json,os,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; CAT=ROOT/'data/NABIL_GOLDEN_CATALOGUE.json'
def write(path,data):
 path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_name(path.name+'.tmp');tmp.write_bytes(data);os.replace(tmp,path)
def clients():
 from google.oauth2 import service_account
 from googleapiclient.discovery import build
 raw=os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON','').strip()
 if not raw:raise RuntimeError('GOOGLE_SERVICE_ACCOUNT_JSON_REQUIRED')
 creds=service_account.Credentials.from_service_account_info(json.loads(raw),scopes=['https://www.googleapis.com/auth/drive.readonly','https://www.googleapis.com/auth/documents.readonly'])
 return build('drive','v3',credentials=creds,cache_discovery=False),build('docs','v1',credentials=creds,cache_discovery=False)
def text(doc):
 out=[]
 for block in (doc.get('body') or {}).get('content',[]):
  p=block.get('paragraph')
  if p:
   s=''.join(str((e.get('textRun') or {}).get('content') or '') for e in p.get('elements',[])).strip()
   if not s:continue
   style=(p.get('paragraphStyle') or {}).get('namedStyleType','')
   if style.startswith('HEADING_'):
    try:s='#'*int(style.rsplit('_',1)[1])+' '+s
    except Exception:pass
   elif style=='TITLE':s='# '+s
   elif style=='SUBTITLE':s='## '+s
   if p.get('bullet'):s='- '+s
   out.append(s);continue
  table=block.get('table')
  if table:
   for row in table.get('tableRows',[]):
    cells=[]
    for cell in row.get('tableCells',[]):
     parts=[]
     for c in cell.get('content',[]):
      pp=c.get('paragraph') or {};parts.append(''.join(str((e.get('textRun') or {}).get('content') or '') for e in pp.get('elements',[])).strip())
     cells.append(' '.join(x for x in parts if x))
    if any(cells):out.append(' | '.join(cells))
 return '\n\n'.join(out).strip()+'\n'
def main():
 raw=json.loads(CAT.read_text('utf-8'));lessons=raw.get('lessons') or []
 if not isinstance(lessons,list) or not lessons:raise RuntimeError('EMPTY_CANONICAL_CATALOGUE')
 drive,docs=clients();now=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime());updated=[];unchanged=[];errors=[]
 for ent in lessons:
  lid=str(ent.get('lesson_id') or '').strip().upper();fid=str(ent.get('drive_file_id') or '').strip();asset=ent.setdefault('assets',{}).setdefault('lesson',{})
  if not lid or not fid:errors.append(f'{lid or "UNKNOWN"}:NO_DRIVE_FILE_ID');continue
  try:
   meta=drive.files().get(fileId=fid,fields='id,name,mimeType,modifiedTime,version,webViewLink',supportsAllDrives=True).execute()
   if meta.get('mimeType')!='application/vnd.google-apps.document':raise RuntimeError('LESSON_NOT_GOOGLE_DOC')
   rel=f'data/golden/{lid}/lesson.json';target=ROOT/rel
   if asset.get('status')=='ok' and asset.get('modified_time')==meta.get('modifiedTime') and target.is_file() and asset.get('sha256')==hashlib.sha256(target.read_bytes()).hexdigest():unchanged.append(lid);continue
   doc=docs.documents().get(documentId=fid).execute();md=text(doc)
   if len(md.strip())<20:raise RuntimeError('EMPTY_DOCUMENT')
   payload=json.dumps({'lesson_id':lid,'kind':'lesson','title':ent.get('title') or doc.get('title') or lid,'markdown':md},ensure_ascii=False,indent=2).encode()
   write(target,payload);asset.update({'drive_file_id':fid,'drive_url':meta.get('webViewLink') or ent.get('drive_url'),'mime':meta.get('mimeType'),'modified_time':meta.get('modifiedTime'),'version':str(meta.get('version') or ent.get('version') or '0.01'),'sha256':hashlib.sha256(payload).hexdigest(),'content_path':rel,'status':'ok','synced_at':now,'error':None});updated.append(lid)
  except Exception as e:
   asset['status']='stale' if asset.get('content_path') and (ROOT/str(asset.get('content_path'))).is_file() else 'error';asset['error']=f'{type(e).__name__}:{e}';asset['last_error_at']=now;errors.append(f'{lid}:{type(e).__name__}:{e}')
 raw['snapshot_sync']={'synced_at':now,'updated':len(updated),'unchanged':len(unchanged),'errors':len(errors)};write(CAT,(json.dumps(raw,ensure_ascii=False,indent=2)+'\n').encode());print(json.dumps({'updated':updated,'unchanged':unchanged,'errors':errors},ensure_ascii=False));raise SystemExit(1 if errors else 0)
if __name__=='__main__':main()
