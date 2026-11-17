import os, json, uuid, shutil, re, zipfile, hashlib, unicodedata, mimetypes, io, asyncio, logging
from pathlib import Path
from datetime import datetime, timezone
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import FileResponse, RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import fitz
from PIL import Image, ImageOps
import pytesseract
from docx import Document
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from gemini_service import analyze_document_images, GeminiError, GeminiNotConfigured

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("nabil.archive")

BASE=Path(os.getenv("DATA_DIR","/tmp/school-archive-data"))
FILES=BASE/"files"; INDEX=BASE/"documents.json"
FILES.mkdir(parents=True,exist_ok=True)
if not INDEX.exists(): INDEX.write_text("[]",encoding="utf-8")
TOKEN_FILE=BASE/"google-token.json"
DRIVE_FOLDER_FILE=BASE/"google-drive-folder.json"
DRIVE_SCOPE=["https://www.googleapis.com/auth/drive.file","openid","https://www.googleapis.com/auth/userinfo.email","https://www.googleapis.com/auth/userinfo.profile"]
REDIRECT_URI=os.getenv("GOOGLE_REDIRECT_URI","https://nabil-school-directors-archive-api.onrender.com/auth/google/callback")

def google_client_config():
 cid=os.getenv("GOOGLE_CLIENT_ID"); secret=os.getenv("GOOGLE_CLIENT_SECRET")
 if not cid or not secret: raise HTTPException(503,"إعدادات Google OAuth غير مكتملة")
 return {"web":{"client_id":cid,"client_secret":secret,"auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","redirect_uris":[REDIRECT_URI]}}

def persist_google_credentials(creds):
 # Store the OAuth refresh token in Render's encrypted service environment so it
 # survives container replacement. Requires a one-time RENDER_API_KEY secret.
 api_key=os.getenv("RENDER_API_KEY")
 service_id=os.getenv("RENDER_SERVICE_ID") or "srv-dbub2ton74is73dee6b0"
 if not api_key: return False
 try:
  from urllib.request import Request as UrlRequest, urlopen
  payload=json.dumps({"value":creds.to_json()}).encode("utf-8")
  req=UrlRequest("https://api.render.com/v1/services/"+service_id+"/env-vars/GOOGLE_TOKEN_JSON",
                 data=payload,headers={"Authorization":"Bearer "+api_key,"Content-Type":"application/json","Accept":"application/json"},method="PUT")
  with urlopen(req,timeout=15) as response:
   return 200 <= response.status < 300
 except Exception:
  return False

def google_credentials():
 if not TOKEN_FILE.exists() and os.getenv("GOOGLE_TOKEN_JSON"):
  TOKEN_FILE.write_text(os.environ["GOOGLE_TOKEN_JSON"],encoding="utf-8")
 if not TOKEN_FILE.exists(): return None
 try: return Credentials.from_authorized_user_file(str(TOKEN_FILE),DRIVE_SCOPE)
 except Exception: return None

def drive_service():
 creds=google_credentials()
 if not creds: return None
 if creds.expired and creds.refresh_token:
  from google.auth.transport.requests import Request as GoogleRequest
  creds.refresh(GoogleRequest())
  TOKEN_FILE.write_text(creds.to_json(),encoding="utf-8")
  persist_google_credentials(creds)
 return build("drive","v3",credentials=creds,cache_discovery=False)

def ensure_drive_folder(service):
 if DRIVE_FOLDER_FILE.exists():
  try: return json.loads(DRIVE_FOLDER_FILE.read_text(encoding="utf-8"))["id"]
  except Exception: pass
 found=service.files().list(q="mimeType='application/vnd.google-apps.folder' and name='NABIL - School Directors Archive' and trashed=false",spaces="drive",fields="files(id,name)",pageSize=10).execute().get("files",[])
 if found: folder_id=found[0]["id"]
 else:
  folder=service.files().create(body={"name":"NABIL - School Directors Archive","mimeType":"application/vnd.google-apps.folder"},fields="id").execute(); folder_id=folder["id"]
 DRIVE_FOLDER_FILE.write_text(json.dumps({"id":folder_id}),encoding="utf-8")
 return folder_id

def drive_upload(path, filename, folder_id):
 service=drive_service()
 if not service: return None
 media=MediaFileUpload(str(path),resumable=True)
 return service.files().create(body={"name":filename,"parents":[folder_id]},media_body=media,fields="id,name,webViewLink,mimeType").execute()

def restore_index_from_drive(service=None, folder_id=None):
 service=service or drive_service()
 if not service: return rows()
 folder_id=folder_id or ensure_drive_folder(service)
 query="name='archive-index.json' and '"+folder_id+"' in parents and trashed=false"
 found=service.files().list(q=query,spaces="drive",fields="files(id)",pageSize=1).execute().get("files",[])
 if not found: return rows()
 raw=service.files().get(fileId=found[0]["id"],alt="media").execute()
 if isinstance(raw,bytes): raw=raw.decode("utf-8")
 # Drive may return parsed JSON data as a dict/list instead of raw text.
 restored=raw if isinstance(raw,(dict,list)) else json.loads(raw)
 if isinstance(restored,dict):
  restored=restored.get("documents",restored.get("items",[]))
 if isinstance(restored,list):
  save(restored)
  return restored
 return rows()

def sync_index_to_drive(items, folder_id):
 service=drive_service()
 if not service: return
 payload=json.dumps(items,ensure_ascii=False,indent=2).encode("utf-8")
 from googleapiclient.http import MediaInMemoryUpload
 query="name='archive-index.json' and '"+folder_id+"' in parents and trashed=false"
 found=service.files().list(q=query,spaces="drive",fields="files(id)",pageSize=1).execute().get("files",[])
 media=MediaInMemoryUpload(payload,mimetype="application/json",resumable=False)
 if found: service.files().update(fileId=found[0]["id"],media_body=media).execute()
 else: service.files().create(body={"name":"archive-index.json","parents":[folder_id]},media_body=media,fields="id").execute()
app=FastAPI(title="NABIL AI School Directors Archive")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])
ALLOWED={".pdf",".docx",".png",".jpg",".jpeg",".webp",".tif",".tiff"}

def rows():
 try: return json.loads(INDEX.read_text(encoding="utf-8"))
 except: return []
def save(items): INDEX.write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding="utf-8")
def ocr(path):
 img=Image.open(path)
 img=ImageOps.exif_transpose(img)
 # Keep OCR workload small enough for the current low-memory CPU instance.
 img.thumbnail((1100,1500))
 img=ImageOps.grayscale(img)
 img=ImageOps.autocontrast(img)
 # Arabic and English cover the common official-document text; avoid the slower three-language pass.
 return pytesseract.image_to_string(img,lang="ara+eng",config="--oem 1 --psm 6 -c preserve_interword_spaces=1",timeout=22)

def extract(path,ext):
 if ext in {".png",".jpg",".jpeg",".webp",".tif",".tiff"}: return ocr(path)
 if ext==".pdf":
  doc=fitz.open(path); out=[]
  for i,page in enumerate(doc):
   text=page.get_text("text").strip()
   if len(text)<30:
    pix=page.get_pixmap(matrix=fitz.Matrix(2,2),alpha=False); tmp=path.parent/(path.stem+"-page-"+str(i)+".png"); pix.save(tmp)
    try: text=ocr(tmp)
    finally: tmp.unlink(missing_ok=True)
   out.append("[صفحة "+str(i+1)+"]\n"+text)
  return "\n".join(out)
 if ext==".docx":
  d=Document(path); return "\n".join(p.text for p in d.paragraphs)+"\n"+"\n".join(" | ".join(c.text for c in row.cells) for t in d.tables for row in t.rows)
 return ""

def detect_metadata(text, filename):
 clean=[re.sub(r"\s+"," ",x).strip(" -–—:؛") for x in text.splitlines()]; clean=[x for x in clean if len(x)>3]; joined="\n".join(clean[:100]); number=""
 pats=[r"(?:رقم|الرقم)\s*(?:الأساس|الأساسي)?\s*[:：#-]?\s*([0-9٠-٩]+\s*[/\\-]\s*[0-9٠-٩]{2,4}|[0-9٠-٩]{2,})",r"(?:قرار|تعميم|مذكرة|مرسوم|قانون)\s*رقم\s*[:：#-]?\s*([0-9٠-٩]+(?:\s*[/\\-]\s*[0-9٠-٩]+)?)",r"(?:N[°ºo]|No\\.?|Numéro)\s*[:：#-]?\s*([0-9٠-٩]+(?:\s*[/\\-]\s*[0-9٠-٩]+)?)"]
 for p in pats:
  m=re.search(p,joined,re.I)
  if m: number=re.sub(r"\s+","",m.group(1)); break
 date=""
 date_patterns=[r"([0-3]?[0-9٠-٩]{1,2}\s*[/.-]\s*[01]?[0-9٠-٩]{1,2}\s*[/.-]\s*(?:19|20)?[0-9٠-٩]{2})",r"([0-3]?[0-9٠-٩]{1,2}\s+(?:كانون الثاني|شباط|آذار|اذار|نيسان|أيار|ايار|حزيران|تموز|آب|اب|أيلول|ايلول|تشرين الأول|تشرين الثاني|كانون الأول)\s+[0-9٠-٩]{4})",r"([0-3]?[0-9]{1,2}\s+(?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+[0-9]{4})"]
 for p in date_patterns:
  m=re.search(p,joined,re.I)
  if m: date=re.sub(r"\s+"," ",m.group(1)); break
 low=joined.lower()
 if re.search(r"قانون|loi\b|law\b",low): category="قانون"
 elif re.search(r"مرسوم|décret|decret",low): category="مرسوم"
 elif re.search(r"قرار|قرار رقم|décision|decision",low): category="قرار"
 elif re.search(r"تعميم|بلاغ|circulaire",low): category="تعميم"
 elif re.search(r"كتاب|مذكرة|مراسلة|كتاب رقم|note de service",low): category="كتاب"
 else: category="غير مصنّف"
 subject=""
 for p in [r"(?:الموضوع|موضوعه|الموضوع:|Subject|Objet)\s*[:：-]?\s*(.{8,180})",r"(?:بشأن|حول|المتعلق(?:ة)? ب)\s+(.{8,140})"]:
  m=re.search(p,joined,re.I)
  if m: subject=m.group(1).split("\n")[0].strip(); break
 if not subject:
  skip=re.compile(r"^(?:الجمهورية اللبنانية|وزارة|المديرية|رقم|التاريخ|تاريخ|قرار|تعميم|مرسوم|قانون|لبنان|République|Ministère)",re.I)
  subject=next((x for x in clean if len(x)>=12 and not skip.search(x)), "")
 if not subject: subject=Path(filename).stem.replace("_"," ").replace("-"," ")
 issuer=""
 m=re.search(r"(وزارة[^\n]{2,70}|المديرية العامة[^\n]{2,70}|République Libanaise[^\n]{0,60})",joined,re.I)
 if m: issuer=m.group(1).strip()
 return {"number":number,"date":date,"subject":subject[:220],"category":category,"issuer":issuer}

@app.get("/api/health")
def health(): return {"status":"ok","document_reader":"Gemini Vision","gemini_configured":bool(os.getenv("GEMINI_API_KEY")),"gemini_model":os.getenv("GEMINI_MODEL","gemini-3.8-flash"),"google_drive_connected":google_credentials() is not None,"google_token_persistence_configured":bool(os.getenv("RENDER_API_KEY")),"google_token_persisted":bool(os.getenv("GOOGLE_TOKEN_JSON"))}
@app.get("/auth/google")
def google_auth():
 flow=Flow.from_client_config(google_client_config(),scopes=DRIVE_SCOPE,redirect_uri=REDIRECT_URI); url,state=flow.authorization_url(access_type="offline",include_granted_scopes="true",prompt="consent"); return RedirectResponse(url)
@app.get("/auth/google/callback")
def google_callback(request:Request):
 try:
  flow=Flow.from_client_config(google_client_config(),scopes=DRIVE_SCOPE,state=request.query_params.get("state"),redirect_uri=REDIRECT_URI); flow.fetch_token(authorization_response=str(request.url)); TOKEN_FILE.write_text(flow.credentials.to_json(),encoding="utf-8"); token_persisted=persist_google_credentials(flow.credentials); service=drive_service(); folder_id=ensure_drive_folder(service)
  if not rows(): restore_index_from_drive(service,folder_id)
  sync_index_to_drive(rows(),folder_id)
  return HTMLResponse("<html lang='ar' dir='rtl'><meta charset='utf-8'><body style='font-family:Tahoma;padding:40px'><h2>تم ربط Google Drive بنجاح</h2><p>تم إنشاء مجلد NABIL - School Directors Archive وبدء مزامنة فهرس الأرشيف.</p><p>"+("تم حفظ تفويض Google في إعدادات Render الدائمة." if token_persisted else "تنبيه: الاتصال يعمل الآن، لكن حفظ التفويض بعد إعادة النشر غير مفعّل بعد؛ يلزم إعداد RENDER_API_KEY مرة واحدة في Render.")+"</p><p>يمكنك العودة إلى الموقع.</p><a href='/'>العودة إلى الأرشيف</a></body></html>")
 except Exception as e: return HTMLResponse("<html lang='ar' dir='rtl'><meta charset='utf-8'><body style='font-family:Tahoma;padding:40px'><h2>تعذر ربط Google Drive</h2><p>"+str(e)+"</p><a href='/'>العودة</a></body></html>",status_code=400)
@app.get("/api/documents")
def documents():
 items=rows()
 if not items:
  try: items=restore_index_from_drive()
  except Exception: pass
 return items
def normalize_key(value):
 value=str(value or "").strip().lower()
 value=value.translate(str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹","01234567890123456789"))
 value=unicodedata.normalize("NFKD",value)
 value="".join(ch for ch in value if not unicodedata.combining(ch))
 value=re.sub(r"[\s\W_]+","",value,flags=re.UNICODE)
 return value

def find_duplicate(items, number, date, subject, exclude_id=None):
 n,d,sub=normalize_key(number),normalize_key(date),normalize_key(subject)
 if not (n and d and sub): return None
 for item in items:
  if item.get("id")==exclude_id: continue
  if (normalize_key(item.get("number") or item.get("document_number"))==n
      and normalize_key(item.get("date") or item.get("document_date"))==d
      and normalize_key(item.get("subject"))==sub):
   return item
 return None

def category_from_type(value):
 v=str(value or "").lower()
 if "قانون" in v or "law" in v: return "قانون"
 if "مرسوم" in v or "decree" in v: return "مرسوم"
 if "قرار" in v or "decision" in v: return "قرار"
 if "تعميم" in v or "circulaire" in v: return "تعميم"
 if any(x in v for x in ("كتاب","مذكرة","مراسلة","بلاغ","note")): return "كتاب"
 return "غير مصنّف"

def retry_pending_documents():
 if not os.getenv("GEMINI_API_KEY"):
  logger.error("retry skipped: GEMINI_API_KEY is not configured")
  return
 logger.info("retry cycle started")
 service=drive_service()
 if not service:
  logger.error("retry skipped: Google Drive credentials unavailable")
  return
 items=rows()
 if not items: items=restore_index_from_drive(service)
 logger.info("retry queue inspected count=%s pending=%s",len(items),sum(1 for x in items if x.get("processing_status")=="pending_ai" and x.get("drive_status")=="saved"))
 changed=False
 now=datetime.now(timezone.utc)
 for d in list(items):
  if d.get("processing_status")!="pending_ai" or d.get("drive_status")!="saved": continue
  retry_at=d.get("next_retry_at")
  if retry_at:
   try:
    retry_time=datetime.fromisoformat(retry_at.replace("Z","+00:00"))
    uploaded_at=datetime.fromisoformat(str(d.get("uploaded_at") or "").replace("Z","+00:00"))
    # Do not leave old pending uploads stranded behind an exponential-backoff timestamp.
    if retry_time>now and (now-uploaded_at).total_seconds()<600: continue
   except Exception: pass
  try:
   images=[]
   remote_files=sorted(d.get("drive_files") or [],key=lambda x:x.get("page",0))
   logger.info("retry document=%s attempt=%s drive_pages=%s",d.get("id"),int(d.get("retry_count",0))+1,len(remote_files))
   if not remote_files: raise RuntimeError("لا توجد ملفات صور مرتبطة بالمستند في Google Drive")
   for remote in remote_files:
    buffer=io.BytesIO()
    downloader=MediaIoBaseDownload(buffer,service.files().get_media(fileId=remote["id"]))
    done=False
    while not done: _,done=downloader.next_chunk()
    payload=buffer.getvalue()
    if not payload: raise RuntimeError("Google Drive أعاد ملف صورة فارغاً: "+str(remote.get("name","unknown")))
    mime=mimetypes.guess_type(remote.get("name",""))[0] or "image/jpeg"
    logger.info("downloaded document=%s page=%s bytes=%s mime=%s",d.get("id"),remote.get("page"),len(payload),mime)
    images.append({"bytes":payload,"mime_type":mime})
   extracted=analyze_document_images(images)
   full_text=str(extracted.get("full_text") or "").strip()
   number=str(extracted.get("document_number") or "").strip()
   date=str(extracted.get("document_date") or "").strip()
   subject=str(extracted.get("subject") or "").strip()
   doc_type=str(extracted.get("document_type") or "").strip()
   verified=bool(extracted.get("data_verified")) and bool(number and date and subject)
   d.update({"title":subject or d.get("title"),"number":number,"document_number":number,
             "date":date,"document_date":date,"subject":subject,
             "issuer":str(extracted.get("issuer") or ""),"category":category_from_type(doc_type),
             "document_type":doc_type,"text":full_text,
             "referenced_decisions":extracted.get("referenced_decisions") or [],
             "field_confidence":extracted.get("field_confidence") or {},
             "review_notes":str(extracted.get("review_notes") or ""),
             "data_verified":verified,"review_required":not verified,
             "gemini_status":"complete" if full_text else "needs_review",
             "processing_status":"complete" if verified and full_text else "needs_review",
             "processed_at":datetime.now(timezone.utc).isoformat()})
   duplicate=find_duplicate(items,number,date,subject,exclude_id=d.get("id"))
   if duplicate:
    duplicate.setdefault("duplicate_uploads",[]).append({
      "uploaded_at":d.get("uploaded_at"),"drive_files":d.get("drive_files") or [],
      "page_count":d.get("page_count",0),"source_school":None,"upload_id":d.get("id")})
    items=[x for x in items if x.get("id")!=d.get("id")]
   logger.info("retry result document=%s chars=%s status=%s",d.get("id"),len(full_text),d.get("processing_status"))
   changed=True
  except Exception as exc:
   logger.exception("retry failed document=%s",d.get("id"))
   count=int(d.get("retry_count",0))+1
   delay=min(600,60*(2**min(count,4)))
   d["retry_count"]=count
   d["next_retry_at"]=(datetime.now(timezone.utc)+__import__("datetime").timedelta(seconds=delay)).isoformat()
   d["gemini_error"]=str(exc)[:500]
   changed=True
 if changed:
  save(items)
  try:
   sync_index_to_drive(items,ensure_drive_folder(service))
   logger.info("retry index synchronized to Drive")
  except Exception:
   logger.exception("retry index synchronization failed")

async def retry_worker():
 logger.info("retry worker started")
 while True:
  await asyncio.sleep(60)
  try:
   await asyncio.to_thread(retry_pending_documents)
  except Exception:
   logger.exception("retry worker cycle crashed")

@app.on_event("startup")
async def start_retry_worker():
 logger.info("starting archive retry worker")
 asyncio.create_task(retry_worker())

def upload_result(d, text="", message=None, duplicate=False):
 public={k:v for k,v in d.items() if k not in {"text","ocr_errors"}}
 return {"ok":d.get("drive_status")=="saved","message":message or "تم حفظ الصور وتسجيل حالة المعالجة.","document":public,
         "extracted_characters":len(text),"extracted_text":text,
         "ocr_status":d.get("processing_status","pending"),
         "processing_status":d.get("processing_status","pending"),
         "storage_status":d.get("drive_status","not_connected"),"duplicate":duplicate}

@app.post("/api/upload")
async def upload(files: list[UploadFile] = File(...)):
 if not files: raise HTTPException(400,"اختر صورة واحدة على الأقل")
 if len(files)>25: raise HTTPException(400,"يمكن رفع 25 صورة كحد أقصى للمستند الواحد")
 ident=uuid.uuid4().hex; saved=[]; image_payloads=[]; total_bytes=0
 allowed={".png":"image/png",".jpg":"image/jpeg",".jpeg":"image/jpeg",".webp":"image/webp",".tif":"image/tiff",".tiff":"image/tiff"}
 try:
  for i,up in enumerate(files,1):
   name=Path(up.filename or f"page-{i}.jpg").name; ext=Path(name).suffix.lower()
   if ext not in allowed: raise HTTPException(415,"ارفع صوراً فقط، ويمكن اختيار عدة صور للمستند نفسه")
   content=await up.read()
   if not content: raise HTTPException(400,"إحدى الصور فارغة")
   if len(content)>12*1024*1024: raise HTTPException(413,"حجم الصورة الواحدة يتجاوز 12 ميغابايت")
   total_bytes+=len(content)
   if total_bytes>18*1024*1024: raise HTTPException(413,"الحجم الإجمالي للصور يتجاوز 18 ميغابايت؛ قسّم المستند إلى دفعتين")
   target=FILES/(ident+"-"+str(i)+ext)
   target.write_bytes(content)
   saved.append({"filename":name,"stored":target.name,"page":i})
   image_payloads.append({"bytes":content,"mime_type":allowed[ext]})
  d={"id":ident,"title":saved[0]["filename"],"filename":saved[0]["filename"],"files":saved,
     "page_count":len(saved),"number":"","document_number":"","date":"","document_date":"",
     "subject":"","category":"قيد المعالجة","issuer":"","text":"",
     "uploaded_at":datetime.now(timezone.utc).isoformat(),"url":"/api/file/"+ident,
     "download":"/api/file/"+ident+"?download=1","review_required":True,
     "processing_status":"saving_to_drive","drive_status":"pending",
     "referenced_decisions":[],"schools":[],"upload_sources":[]}
  items=rows(); items.insert(0,d); save(items)

  # The original images must reach Drive before any AI call.
  service=drive_service()
  if not service:
   d["drive_status"]="not_connected"; d["processing_status"]="pending_storage"
   d["processing_message"]="الصور محفوظة مؤقتاً على الخادم، لكن لم يتم تأكيد حفظها في Google Drive. أعد ربط Drive."
   items[0]=d; save(items)
   return upload_result(d,message=d["processing_message"])

  try:
   folder_id=ensure_drive_folder(service); drive_files=[]
   for entry in saved:
    uploaded=drive_upload(FILES/entry["stored"],entry["filename"],folder_id)
    if not uploaded or not uploaded.get("id"): raise RuntimeError("لم يؤكد Google Drive حفظ إحدى الصفحات")
    drive_files.append({"id":uploaded["id"],"name":uploaded["name"],
                        "webViewLink":uploaded.get("webViewLink"),"page":entry["page"]})
    d["drive_files"]=list(drive_files); items[0]=d; save(items)
   d["drive_files"]=drive_files; d["drive_folder_id"]=folder_id
   d["drive_status"]="saved"; d["processing_status"]="queued"
   items[0]=d; save(items)
   sync_index_to_drive(items,folder_id)
  except Exception as drive_error:
   d["drive_status"]="partial"; d["processing_status"]="pending_storage"
   d["drive_error"]=str(drive_error)[:300]
   items[0]=d; save(items)
   return upload_result(d,message="لم يكتمل تأكيد حفظ كل الصور في Google Drive؛ لم نبدأ التحليل حتى لا نفقد صفحات المستند.")

  # Gemini reads the original image bytes in their upload order. No Tesseract call is made.
  try:
   extracted=analyze_document_images(image_payloads)
   full_text=str(extracted.get("full_text") or "").strip()
   number=str(extracted.get("document_number") or "").strip()
   date=str(extracted.get("document_date") or "").strip()
   subject=str(extracted.get("subject") or "").strip()
   issuer=str(extracted.get("issuer") or "").strip()
   doc_type=str(extracted.get("document_type") or "").strip()
   confidence=extracted.get("field_confidence") if isinstance(extracted.get("field_confidence"),dict) else {}
   verified=bool(extracted.get("data_verified")) and bool(number and date and subject)
   d.update({"title":subject or saved[0]["filename"],"number":number,"document_number":number,
             "date":date,"document_date":date,"subject":subject,"issuer":issuer,
             "category":category_from_type(doc_type),"document_type":doc_type,
             "text":full_text,"referenced_decisions":extracted.get("referenced_decisions") or [],
             "field_confidence":confidence,"review_notes":str(extracted.get("review_notes") or ""),
             "data_verified":verified,"review_required":not verified,
             "gemini_status":"complete" if full_text else "needs_review",
             "processing_status":"complete" if verified and full_text else "needs_review",
             "processed_at":datetime.now(timezone.utc).isoformat()})
   if not full_text:
    d["processing_message"]="حُفظت الصور، لكن Gemini لم يستخرج نصاً كافياً. المستند بانتظار التحقق."
   elif not verified:
    d["processing_message"]="تم استخراج النص، وبعض البيانات غير مؤكدة؛ المستند محفوظ وقيد التحقق."
   else:
    d["processing_message"]="تمت قراءة المستند وفهرسته بواسطة Gemini."
   duplicate=find_duplicate(items,number,date,subject,exclude_id=ident)
   if duplicate:
    duplicate.setdefault("duplicate_uploads",[]).append({
      "uploaded_at":d["uploaded_at"],"drive_files":drive_files,"page_count":len(saved),
      "source_school":None,"upload_id":ident})
    duplicate["last_uploaded_at"]=d["uploaded_at"]
    items=[x for x in items if x.get("id")!=ident]
    d=duplicate
    duplicate_flag=True
    message="المستند موجود مسبقاً؛ احتفظنا بصور الرفع الجديد وربطناها بالسجل نفسه."
   else:
    items[0]=d; duplicate_flag=False; message=d["processing_message"]
   save(items)
   try: sync_index_to_drive(items,folder_id)
   except Exception as sync_error: d["index_sync_warning"]=str(sync_error)[:240]
   return upload_result(d,full_text,message,duplicate_flag)
  except GeminiNotConfigured as ai_error:
   d["gemini_status"]="not_configured"; d["processing_status"]="pending_ai"
   d["processing_message"]="تم حفظ الصور الأصلية في Google Drive. يلزم ضبط GEMINI_API_KEY في Render لبدء القراءة."
  except Exception as ai_error:
   d["gemini_status"]="failed"; d["processing_status"]="pending_ai"
   d["retry_count"]=0; d["next_retry_at"]=(datetime.now(timezone.utc)+__import__("datetime").timedelta(seconds=60)).isoformat()
   d["gemini_error"]=str(ai_error)[:500]
   d["processing_message"]="تم حفظ الصور الأصلية في Google Drive، لكن تعذرت قراءة Gemini مؤقتاً. المستند محفوظ بانتظار إعادة المعالجة."
  items=rows()
  current=next((x for x in items if x.get("id")==ident),d)
  current.update(d); save(items)
  try: sync_index_to_drive(items,folder_id)
  except Exception: pass
  return upload_result(d,message=d.get("processing_message"))
 except HTTPException: raise
 except Exception as e:
  # Never report successful archiving when storage was not confirmed.
  try:
   items=rows(); current=next((x for x in items if x.get("id")==ident),None)
   if current:
    current["processing_status"]="error"; current["processing_error"]=str(e)[:300]; save(items)
  except Exception: pass
  raise HTTPException(500,"تعذرت معالجة الرفع: "+str(e)[:240]+". احتفظ بالصور الأصلية إلى أن تتأكد من ظهورها في الأرشيف وGoogle Drive.")
def ensure_local_page(d, entry):
 stored=entry.get("stored") or (d.get("id","document")+Path(entry.get("filename") or d.get("filename","document.jpg")).suffix.lower())
 p=FILES/stored
 if p.exists(): return p
 drive_files=d.get("drive_files") or []
 page_no=entry.get("page",1)
 remote=next((x for x in drive_files if x.get("page")==page_no),None)
 if not remote and len(drive_files)>=page_no: remote=drive_files[page_no-1]
 if not remote or not remote.get("id"):
  logger.error("image unavailable: no Drive file mapping document=%s page=%s",d.get("id"),page_no)
  return None
 service=drive_service()
 if not service:
  logger.error("image unavailable: Drive credentials missing document=%s",d.get("id"))
  return None
 p.parent.mkdir(parents=True,exist_ok=True)
 request=service.files().get_media(fileId=remote["id"])
 with p.open("wb") as fh:
  downloader=MediaIoBaseDownload(fh,request)
  done=False
  while not done: _,done=downloader.next_chunk()
 return p if p.exists() and p.stat().st_size else None

@app.get("/api/file/{ident}")
def get_file(ident:str,download:int=0,page:int=1):
 d=next((x for x in documents() if x["id"]==ident),None)
 if not d: raise HTTPException(404,"غير موجود")
 group=d.get("files") or [{"filename":d["filename"],"stored":ident+Path(d["filename"]).suffix.lower(),"page":1}]
 if download:
  archive=BASE/(ident+".zip")
  with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
   added=0
   for entry in group:
    p=ensure_local_page(d,entry)
    if p and p.exists(): z.write(p,arcname=entry["filename"]); added+=1
  if not added: raise HTTPException(404,"الملفات الأصلية غير متاحة حالياً؛ تحقق من اتصال Google Drive")
  return FileResponse(archive,filename=(d.get("number") or "document")+"-pages.zip",media_type="application/zip")
 entry=group[min(max(page-1,0),len(group)-1)]
 p=ensure_local_page(d,entry)
 if not p: raise HTTPException(404,"الصورة غير متاحة؛ تحقق من اتصال Google Drive")
 return FileResponse(p,filename=entry["filename"],content_disposition_type="inline")
@app.get("/document/{ident}",response_class=HTMLResponse)
def document_page(ident:str):
 items=documents()
 d=next((x for x in items if x.get("id")==ident),None)
 # Local Render storage may be recreated on deploy. If the requested ID is
 # absent locally, recover the durable Drive index before returning 404.
 if not d:
  service=None
  try:
   service=drive_service()
   if service:
    try:
     restored=restore_index_from_drive(service)
     merged={x.get("id"):x for x in restored if x.get("id")}
     for item in items:
      if item.get("id"): merged[item["id"]]=item
     items=list(merged.values())
     save(items)
     d=next((x for x in items if x.get("id")==ident),None)
    except Exception:
     logger.exception("Drive index restore failed during document lookup id=%s",ident)
    # Recover this known orphaned upload directly from its original Drive image,
    # even when the JSON index was lost with Render's ephemeral filesystem.
    if not d and ident=="1f435403e4134123a4581e17e95ca170":
     folder_id=ensure_drive_folder(service)
     found=service.files().list(
      q="name='1001679933.jpg' and '"+folder_id+"' in parents and trashed=false",
      spaces="drive",fields="files(id,name,mimeType,createdTime,webViewLink)",pageSize=10
     ).execute().get("files",[])
     if found:
      remote=found[0]
      d={"id":ident,"title":remote.get("name","1001679933.jpg"),
         "filename":remote.get("name","1001679933.jpg"),
         "files":[{"filename":remote.get("name","1001679933.jpg"),"stored":ident+Path(remote.get("name","1001679933.jpg")).suffix.lower(),"page":1}],
         "page_count":1,"number":"","document_number":"","date":"","document_date":"",
         "subject":"","category":"قيد المعالجة","issuer":"","text":"",
         "uploaded_at":remote.get("createdTime") or datetime.now(timezone.utc).isoformat(),
         "url":"/api/file/"+ident,"download":"/api/file/"+ident+"?download=1",
         "review_required":True,"processing_status":"pending_ai","drive_status":"saved",
         "drive_files":[{"id":remote["id"],"name":remote.get("name","1001679933.jpg"),
                         "webViewLink":remote.get("webViewLink"),"page":1}],
         "drive_folder_id":folder_id,"referenced_decisions":[],"schools":[],"upload_sources":[],
         "recovered_from_drive":True}
      items.insert(0,d); save(items); sync_index_to_drive(items,folder_id)
      logger.info("recovered orphaned image from Drive id=%s file_id=%s",ident,remote["id"])
      # Run Gemini against the recovered original immediately, then reload its
      # indexed metadata before rendering the document page.
      retry_pending_documents()
      items=rows()
      d=next((x for x in items if x.get("id")==ident),d)
  except Exception:
   logger.exception("document lookup recovery failed id=%s",ident)
 if not d: raise HTTPException(404,"المستند غير موجود في الأرشيف أو لم يُسترجع من فهرس Google Drive")
 esc=__import__("html").escape
 title=esc(str(d.get("title") or d.get("subject") or "مستند إداري"))
 meta=[]
 for label,key in [("الفئة","category"),("الرقم","number"),("التاريخ","date"),("الجهة","issuer"),("الموضوع","subject")]:
  value=str(d.get(key) or "").strip()
  if value: meta.append("<p><b>"+label+":</b> "+esc(value)+"</p>")
 pages=d.get("files") or [{"filename":d.get("filename","document"),"page":1}]
 page_count=max(1,len(pages))
 body_text=esc(str(d.get("text") or ""))
 return HTMLResponse("""<!doctype html><html lang="ar" dir="rtl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>"""+title+""" | NABIL AI</title>
 <style>body{font-family:Tahoma,Arial;background:#f3f6fa;color:#203246;margin:0;padding:18px}.wrap{max-width:900px;margin:auto}.panel{background:white;border-radius:16px;padding:20px;margin:14px 0;box-shadow:0 4px 18px #102a4310}h1{font-size:21px}.meta p{line-height:1.7;margin:6px 0}.viewer{text-align:center}.viewer img{max-width:100%;max-height:72vh;object-fit:contain;border:1px solid #ddd;border-radius:8px}.controls{display:flex;gap:10px;justify-content:center;align-items:center;flex-wrap:wrap;margin:14px}.controls button,a{background:#1769aa;color:white;border:0;border-radius:9px;padding:11px 16px;text-decoration:none;font-weight:bold}.controls button:disabled{opacity:.4}.text{white-space:pre-wrap;line-height:1.9;max-height:420px;overflow:auto;background:#f8fafc;padding:14px;border-radius:10px}.muted{color:#718195}</style>
 <div class="wrap"><p><a href="/">← العودة إلى الأرشيف</a></p><section class="panel"><h1>"""+title+"""</h1><div class="meta">"""+ "".join(meta)+"""</div></section>
 <section class="panel viewer"><h2>المستند الأصلي</h2><img id="pageImage" src="/api/file/"""+ident+"""?page=1" alt="صفحة المستند"><div class="controls"><button id="prev" disabled>الصفحة السابقة</button><span id="pageLabel">الصفحة 1 من """+str(page_count)+"""</span><button id="next" """+("disabled" if page_count<=1 else "")+""">الصفحة التالية</button><a href="/api/file/"""+ident+"""?download=1">تنزيل جميع الصفحات</a></div></section>
 <section class="panel"><h2>النص المستخرج</h2><div class="text">"""+(body_text or "لم يتوفر نص مستخرج لهذا المستند بعد.")+"""</div></section></div>
 <script>let p=1;const total="""+str(page_count)+""";const img=document.getElementById('pageImage'),label=document.getElementById('pageLabel'),prev=document.getElementById('prev'),next=document.getElementById('next');function show(){img.src='/api/file/"""+ident+"""?page='+p;label.textContent='الصفحة '+p+' من '+total;prev.disabled=p===1;next.disabled=p===total}prev.onclick=()=>{if(p>1){p--;show()}};next.onclick=()=>{if(p<total){p++;show()}}</script></html>""")

@app.get("/api/ask")
def ask(q:str):
 items=[]
 for d in rows():
  body=(d.get("text","")+" "+d.get("subject","")+" "+d.get("title","")).lower(); score=sum(body.count(w) for w in q.lower().split() if len(w)>2)
  if score: items.append({"title":d["title"],"number":d["number"],"date":d["date"],"url":d["url"],"score":score,"text":d["text"][:900]})
 return {"question":q,"results":sorted(items,key=lambda x:x["score"],reverse=True)[:8],"notice":"تحقق من المستند الأصلي قبل اعتماد أي معلومة."}
@app.get("/")
def home(): return FileResponse(Path(__file__).parent/"index.html")
