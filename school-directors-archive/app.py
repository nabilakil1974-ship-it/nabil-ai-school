import os, json, uuid, shutil, re, zipfile
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
from googleapiclient.http import MediaFileUpload

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

def google_credentials():
 if not TOKEN_FILE.exists(): return None
 try:
  return Credentials.from_authorized_user_file(str(TOKEN_FILE),DRIVE_SCOPE)
 except Exception: return None

def drive_service():
 creds=google_credentials()
 if not creds: return None
 if creds.expired and creds.refresh_token:
  from google.auth.transport.requests import Request as GoogleRequest
  creds.refresh(GoogleRequest()); TOKEN_FILE.write_text(creds.to_json(),encoding="utf-8")
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
 result=service.files().create(body={"name":filename,"parents":[folder_id]},media_body=media,fields="id,name,webViewLink,mimeType").execute()
 return result

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
 img.thumbnail((1600,1600))
 img=ImageOps.grayscale(img)
 img=ImageOps.autocontrast(img)
 return pytesseract.image_to_string(img,lang="ara+fra+eng",config="--psm 3",timeout=18)
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
 clean=[re.sub(r"\s+"," ",x).strip(" -–—:؛") for x in text.splitlines()]
 clean=[x for x in clean if len(x)>3]
 joined="\n".join(clean[:100])
 # Document number: Arabic and French/English common labels
 number=""
 pats=[
  r"(?:رقم|الرقم)\s*(?:الأساس|الأساسي)?\s*[:：#-]?\s*([0-9٠-٩]+\s*[/\\-]\s*[0-9٠-٩]{2,4}|[0-9٠-٩]{2,})",
  r"(?:قرار|تعميم|مذكرة|مرسوم|قانون)\s*رقم\s*[:：#-]?\s*([0-9٠-٩]+(?:\s*[/\\-]\s*[0-9٠-٩]+)?)",
  r"(?:N[°ºo]|No\\.?|Numéro)\s*[:：#-]?\s*([0-9٠-٩]+(?:\s*[/\\-]\s*[0-9٠-٩]+)?)"
 ]
 for p in pats:
  m=re.search(p,joined,re.I)
  if m: number=re.sub(r"\s+","",m.group(1)); break
 date=""
 date_patterns=[
  r"([0-3]?[0-9٠-٩]{1,2}\s*[/.-]\s*[01]?[0-9٠-٩]{1,2}\s*[/.-]\s*(?:19|20)?[0-9٠-٩]{2})",
  r"([0-3]?[0-9٠-٩]{1,2}\s+(?:كانون الثاني|شباط|آذار|اذار|نيسان|أيار|ايار|حزيران|تموز|آب|اب|أيلول|ايلول|تشرين الأول|تشرين الثاني|كانون الأول)\s+[0-9٠-٩]{4})",
  r"([0-3]?[0-9]{1,2}\s+(?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+[0-9]{4})"
 ]
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
 # prefer explicit subject/object label
 for p in [r"(?:الموضوع|موضوعه|الموضوع:|Subject|Objet)\s*[:：-]?\s*(.{8,180})",r"(?:بشأن|حول|المتعلق(?:ة)? ب)\s+(.{8,140})"]:
  m=re.search(p,joined,re.I)
  if m: subject=m.group(1).split("\n")[0].strip(); break
 if not subject:
  skip=re.compile(r"^(?:الجمهورية اللبنانية|وزارة|المديرية|رقم|التاريخ|تاريخ|قرار|تعميم|مرسوم|قانون|لبنان|République|Ministère|Ministère)",re.I)
  subject=next((x for x in clean if len(x)>=12 and not skip.search(x)), "")
 if not subject: subject=Path(filename).stem.replace("_"," ").replace("-"," ")
 issuer=""
 m=re.search(r"(وزارة[^\n]{2,70}|المديرية العامة[^\n]{2,70}|République Libanaise[^\n]{0,60})",joined,re.I)
 if m: issuer=m.group(1).strip()
 return {"number":number,"date":date,"subject":subject[:220],"category":category,"issuer":issuer}

@app.get("/api/health")
def health(): return {"status":"ok","ocr_languages":"ara+fra+eng","google_drive_connected":google_credentials() is not None}

@app.get("/auth/google")
def google_auth():
 flow=Flow.from_client_config(google_client_config(),scopes=DRIVE_SCOPE,redirect_uri=REDIRECT_URI)
 url,state=flow.authorization_url(access_type="offline",include_granted_scopes="true",prompt="consent")
 return RedirectResponse(url)

@app.get("/auth/google/callback")
def google_callback(request:Request):
 try:
  flow=Flow.from_client_config(google_client_config(),scopes=DRIVE_SCOPE,state=request.query_params.get("state"),redirect_uri=REDIRECT_URI)
  flow.fetch_token(authorization_response=str(request.url))
  TOKEN_FILE.write_text(flow.credentials.to_json(),encoding="utf-8")
  service=drive_service(); folder_id=ensure_drive_folder(service)
  sync_index_to_drive(rows(),folder_id)
  return HTMLResponse("<html lang='ar' dir='rtl'><meta charset='utf-8'><body style='font-family:Tahoma;padding:40px'><h2>تم ربط Google Drive بنجاح</h2><p>تم إنشاء مجلد NABIL - School Directors Archive وبدء مزامنة فهرس الأرشيف.</p><p>يمكنك العودة إلى الموقع.</p><a href='/'>العودة إلى الأرشيف</a></body></html>")
 except Exception as e:
  return HTMLResponse("<html lang='ar' dir='rtl'><meta charset='utf-8'><body style='font-family:Tahoma;padding:40px'><h2>تعذر ربط Google Drive</h2><p>"+str(e)+"</p><a href='/'>العودة</a></body></html>",status_code=400)
@app.get("/api/documents")
def documents(): return rows()
@app.post("/api/upload")
async def upload(files: list[UploadFile] = File(...)):
 if not files: raise HTTPException(400,"اختر صورة واحدة على الأقل")
 if len(files)>25: raise HTTPException(400,"يمكن رفع 25 صورة كحد أقصى للمستند الواحد")
 ident=uuid.uuid4().hex; saved=[]; texts=[]; ocr_errors=[]
 try:
  for i,up in enumerate(files,1):
   name=Path(up.filename or f"page-{i}.jpg").name; ext=Path(name).suffix.lower()
   if ext not in {".png",".jpg",".jpeg",".webp",".tif",".tiff"}:
    raise HTTPException(415,"ارفع صوراً فقط، ويمكن اختيار عدة صور للمستند نفسه")
   target=FILES/(ident+"-"+str(i)+ext)
   with target.open("wb") as out: shutil.copyfileobj(up.file,out)
   saved.append({"filename":name,"stored":target.name,"page":i})
   try:
    page_text=extract(target,ext)
   except Exception as ocr_error:
    page_text=""
    ocr_errors.append({"page":i,"error":str(ocr_error)[:240]})
   texts.append("[الصورة / الصفحة "+str(i)+"]\n"+page_text)
  text="\n\n".join(texts)
  meta=detect_metadata(text," ".join(x["filename"] for x in saved))
 except HTTPException:
  for x in saved: (FILES/x["stored"]).unlink(missing_ok=True)
  raise
 except Exception as e:
  # Keep uploaded originals even when document processing fails.
  raise HTTPException(422,"تعذرت معالجة المستند: "+str(e)+". الصور الأصلية محفوظة على الخادم إن اكتمل نسخها.")
 d={"id":ident,"title":meta["subject"] or saved[0]["filename"],"filename":saved[0]["filename"],"files":saved,"page_count":len(saved),**meta,"text":text,"uploaded_at":datetime.now(timezone.utc).isoformat(),"url":"/api/file/"+ident,"download":"/api/file/"+ident+"?download=1","review_required":not bool(text.strip()) or bool(ocr_errors),"ocr_status":"partial" if ocr_errors and text.strip() else ("failed" if ocr_errors else "complete"),"ocr_errors":ocr_errors}
 items=rows(); items.insert(0,d); save(items)
 try:
  service=drive_service()
  if service:
   folder_id=ensure_drive_folder(service); drive_files=[]
   for entry in saved:
    uploaded=drive_upload(FILES/entry["stored"],entry["filename"],folder_id)
    if uploaded: drive_files.append({"id":uploaded["id"],"name":uploaded["name"],"webViewLink":uploaded.get("webViewLink")})
   d["drive_files"]=drive_files; d["drive_folder_id"]=folder_id; d["drive_status"]="saved" if len(drive_files)==len(saved) else "partial"
   items[0]=d; save(items); sync_index_to_drive(items,folder_id)
  else: d["drive_status"]="not_connected"
 except Exception as drive_error:
  d["drive_status"]="error"; d["drive_error"]=str(drive_error)[:300]; items[0]=d; save(items)
 return {"ok":True,"document":{k:v for k,v in d.items() if k!="text"},"extracted_characters":len(text),"extracted_text":text[:1800],"ocr_status":d.get("ocr_status","complete"),"ocr_errors":ocr_errors,"storage_status":d.get("drive_status","not_connected") }

@app.get("/api/file/{ident}")
def get_file(ident:str,download:int=0,page:int=1):
 d=next((x for x in rows() if x["id"]==ident),None)
 if not d: raise HTTPException(404,"غير موجود")
 group=d.get("files") or [{"filename":d["filename"],"stored":ident+Path(d["filename"]).suffix.lower(),"page":1}]
 existing=[FILES/x["stored"] for x in group if (FILES/x["stored"]).exists()]
 if not existing: raise HTTPException(404,"الملفات غير متاحة")
 if download:
  archive=BASE/(ident+".zip")
  with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
   for entry,p in zip(group, [FILES/x["stored"] for x in group]):
    if p.exists(): z.write(p,arcname=entry["filename"])
  return FileResponse(archive,filename=(d.get("number") or "document")+"-pages.zip",media_type="application/zip")
 entry=group[min(max(page-1,0),len(group)-1)]
 p=FILES/entry["stored"]
 if not p.exists(): raise HTTPException(404,"الصورة غير متاحة")
 return FileResponse(p,filename=entry["filename"],content_disposition_type="inline")
@app.get("/api/ask")
def ask(q:str):
 items=[]
 for d in rows():
  body=(d.get("text","")+" "+d.get("subject","")+" "+d.get("title","")).lower()
  score=sum(body.count(w) for w in q.lower().split() if len(w)>2)
  if score: items.append({"title":d["title"],"number":d["number"],"date":d["date"],"url":d["url"],"score":score,"text":d["text"][:900]})
 return {"question":q,"results":sorted(items,key=lambda x:x["score"],reverse=True)[:8],"notice":"تحقق من المستند الأصلي قبل اعتماد أي معلومة."}
@app.get("/")
def home(): return FileResponse(Path(__file__).parent/"index.html")
