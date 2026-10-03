"""NABIL AI Golden lesson runtime store.

Zero-AI runtime contract: Golden lessons are generated/approved once, grouped
into an immutable package, and rendered many times identically for students.
No LLM/RAG generation occurs here.
"""
from __future__ import annotations
import hashlib, html as html_lib, io, json, os, re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Optional
from urllib.request import Request, urlopen
from app.services.lesson_cache import normalize_lesson_id, normalize_language, normalize_package_version
GOLDEN_REGISTRY_PATH=Path(os.getenv('NABIL_GOLDEN_REGISTRY_PATH','data/golden_lessons_registry.json'))
GOLDEN_LINKS_PATH=Path(os.getenv('NABIL_GOLDEN_LINKS_PATH','data/golden_lesson_links.json'))
ARTIFACT_ORDER=('lesson','activities','exercises','worksheets','solutions','visuals','labs','master_lab','golden_card')
class _VisibleText(HTMLParser):
 BLOCKS={'p','div','section','article','h1','h2','h3','h4','li','tr','br'}
 def __init__(self):super().__init__(convert_charrefs=True);self.parts=[]
 def handle_starttag(self,tag,attrs):
  if tag.lower() in self.BLOCKS:self.parts.append('\n')
 def handle_endtag(self,tag):
  if tag.lower() in self.BLOCKS:self.parts.append('\n')
 def handle_data(self,data):
  if data and data.strip():self.parts.append(data.strip()+' ')
 def text(self):
  v=html_lib.unescape(''.join(self.parts));v=re.sub(r'[ \t]+',' ',v);return re.sub(r'\n\s*\n\s*\n+','\n\n',v).strip()
def html_to_student_text(v):p=_VisibleText();p.feed(v or '');return p.text()
def _load_lessons(path):
 if not path.exists():return {}
 raw=json.loads(path.read_text(encoding='utf-8')); lessons=raw.get('lessons') if isinstance(raw,dict) else None
 if lessons is None and isinstance(raw,dict) and all(isinstance(v,dict) for v in raw.values()):lessons=raw
 if not isinstance(lessons,dict):raise RuntimeError(f'GOLDEN_LESSONS_INVALID:{path}')
 return lessons
def _registry():return {'lessons':_load_lessons(GOLDEN_REGISTRY_PATH)}
def _catalogue_entry(lid):
 item=_load_lessons(GOLDEN_LINKS_PATH).get(normalize_lesson_id(lid))
 if not isinstance(item,dict) or item.get('golden') is False or str(item.get('status') or 'available')!='available':return None
 return dict(item)
def get_registry_entry(lid):
 lid=normalize_lesson_id(lid);base=_registry()['lessons'].get(lid);synced=_catalogue_entry(lid)
 if not isinstance(base,dict) and not isinstance(synced,dict):return None
 merged=dict(base or {});merged.update({k:v for k,v in (synced or {}).items() if v not in (None,'')});merged.setdefault('lesson_id',lid);return merged
def list_registry_entries():
 ids=set(_registry()['lessons'])|set(_load_lessons(GOLDEN_LINKS_PATH));return [x for lid in sorted(ids) if (x:=get_registry_entry(lid))]
def _drive_service():
 from scripts.index_books import get_drive_service
 return get_drive_service()
def _download_bytes(service,fid,mime):
 from googleapiclient.http import MediaIoBaseDownload
 req=service.files().export_media(fileId=fid,mimeType='text/html') if mime=='application/vnd.google-apps.document' else service.files().get_media(fileId=fid);fh=io.BytesIO();dl=MediaIoBaseDownload(fh,req);done=False
 while not done:_,done=dl.next_chunk()
 return fh.getvalue()
def _anonymous_google_doc_export(fid):
 if not re.fullmatch(r'[A-Za-z0-9_-]{10,200}',fid or ''):raise ValueError('INVALID_GOLDEN_DRIVE_FILE_ID')
 with urlopen(Request(f'https://docs.google.com/document/d/{fid}/export?format=html',headers={'User-Agent':'NABIL-AI-Golden/1.0'}),timeout=20) as r:data=r.read(12_000_001)
 if not data or len(data)>12_000_000:raise RuntimeError('GOLDEN_PUBLIC_EXPORT_INVALID_SIZE')
 return data
def _browser_preview(fid,title):
 safe=html_lib.escape(title or 'NABIL Golden artifact');src=f'https://docs.google.com/document/d/{fid}/preview'
 return f"<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{safe}</title><style>html,body{{margin:0;width:100%;height:100%;background:#071d30}}iframe{{border:0;width:100%;height:100%;display:block;background:white}}</style></head><body><iframe src='{src}' title='{safe}'></iframe></body></html>"
def _fetch_artifact(service,a):
 fid=str(a.get('drive_file_id') or '');mime=str(a.get('mime_type') or '');title=str(a.get('name') or a.get('artifact_id') or 'Golden artifact');preview=False
 if not fid:return None
 try:payload=_download_bytes(service,fid,mime)
 except Exception:
  try:payload=_anonymous_google_doc_export(fid);mime='application/vnd.google-apps.document'
  except Exception:payload=_browser_preview(fid,title).encode();mime='text/html';preview=True
 text=payload.decode('utf-8',errors='replace').strip();is_html='html' in mime or 'google-apps.document' in mime or text.lower().startswith(('<!doctype html','<html'))
 return {**a,'html':text if is_html else '','text':title if preview else (html_to_student_text(text) if is_html else text),'sha256':hashlib.sha256(payload).hexdigest(),'browser_drive_preview':preview}
def fetch_golden_from_drive(lesson_id,language='en',version='0.01'):
 lid=normalize_lesson_id(lesson_id);entry=get_registry_entry(lid)
 if not entry or not entry.get('golden'):raise FileNotFoundError(f'GOLDEN_LESSON_NOT_PUBLISHED:{lid}')
 package=entry.get('package') or {}
 if package and (package.get('runtime_ai_generation') is not False or package.get('generation_policy')!='GENERATE_ONCE_RENDER_MANY'):raise RuntimeError(f'GOLDEN_PACKAGE_POLICY_INVALID:{lid}')
 groups=package.get('artifacts') if isinstance(package.get('artifacts'),dict) else {}
 # Backward-compatible package for an older Golden catalogue entry.
 if not groups:
  fid=str(entry.get('drive_file_id') or entry.get('drive_theory_id') or '')
  if not fid:raise FileNotFoundError(f'GOLDEN_PACKAGE_EMPTY:{lid}')
  groups={'lesson':[{'artifact_id':f'{lid}-LESSON','kind':'lesson','drive_file_id':fid,'name':entry.get('title') or lid,'url':entry.get('drive_url'),'mime_type':entry.get('mime_type') or 'application/vnd.google-apps.document'}]}
 service=_drive_service();rendered={k:[] for k in ARTIFACT_ORDER};sources=[]
 for kind in ARTIFACT_ORDER:
  for a in groups.get(kind,[]) or []:
   item=_fetch_artifact(service,a)
   if item:
    rendered[kind].append(item);sources.append({'type':'golden_package_artifact','lesson_id':lid,'kind':kind,'artifact_id':item.get('artifact_id'),'drive_file_id':item.get('drive_file_id'),'sha256':item.get('sha256')})
 lesson_items=rendered['lesson']
 if not lesson_items:raise RuntimeError(f'GOLDEN_PACKAGE_NO_LESSON:{lid}')
 primary=lesson_items[0];fingerprint=str(package.get('content_fingerprint') or hashlib.sha256(json.dumps([(s['artifact_id'],s['sha256']) for s in sources],sort_keys=True).encode()).hexdigest())
 return {'lesson_id':lid,'language':normalize_language(entry.get('language') or language),'version':normalize_package_version(entry.get('version') or version),'title':str(entry.get('title') or primary.get('name') or lid),'reply':primary.get('text') or entry.get('title') or lid,'lesson_html':primary.get('html') or '','drive_file_id':primary.get('drive_file_id'),'drive_url':primary.get('url') or entry.get('drive_url'),'sha256':primary.get('sha256'),'browser_drive_preview':bool(primary.get('browser_drive_preview')),'golden_package':rendered,'package_schema':package.get('package_schema') or 'nabil.golden.package.v1','generation_policy':'GENERATE_ONCE_RENDER_MANY','runtime_ai_generation':False,'immutable':True,'content_fingerprint':fingerprint,'sources':sources}
