import os, json, uuid, shutil, re, zipfile
from pathlib import Path
from datetime import datetime, timezone
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import fitz
from PIL import Image
import pytesseract
from docx import Document

BASE=Path(os.getenv("DATA_DIR","/tmp/school-archive-data"))
FILES=BASE/"files"; INDEX=BASE/"documents.json"
FILES.mkdir(parents=True,exist_ok=True)
if not INDEX.exists(): INDEX.write_text("[]",encoding="utf-8")
app=FastAPI(title="NABIL AI School Directors Archive")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])
ALLOWED={".pdf",".docx",".png",".jpg",".jpeg",".webp",".tif",".tiff"}

def rows():
 try: return json.loads(INDEX.read_text(encoding="utf-8"))
 except: return []
def save(items): INDEX.write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding="utf-8")
def ocr(path): return pytesseract.image_to_string(Image.open(path),lang="ara+fra+eng")
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
def health(): return {"status":"ok","ocr_languages":"ara+fra+eng"}
@app.get("/api/documents")
def documents(): return rows()
@app.post("/api/upload")
async def upload(files: list[UploadFile] = File(...)):
 if not files: raise HTTPException(400,"اختر صورة واحدة على الأقل")
 if len(files)>25: raise HTTPException(400,"يمكن رفع 25 صورة كحد أقصى للمستند الواحد")
 ident=uuid.uuid4().hex; saved=[]; texts=[]
 try:
  for i,up in enumerate(files,1):
   name=Path(up.filename or f"page-{i}.jpg").name; ext=Path(name).suffix.lower()
   if ext not in {".png",".jpg",".jpeg",".webp",".tif",".tiff"}:
    raise HTTPException(415,"ارفع صوراً فقط، ويمكن اختيار عدة صور للمستند نفسه")
   target=FILES/(ident+"-"+str(i)+ext)
   with target.open("wb") as out: shutil.copyfileobj(up.file,out)
   saved.append({"filename":name,"stored":target.name,"page":i})
   page_text=extract(target,ext)
   texts.append("[الصورة / الصفحة "+str(i)+"]\\n"+page_text)
  text="\\n\\n".join(texts)
  meta=detect_metadata(text," ".join(x["filename"] for x in saved))
 except HTTPException:
  for x in saved: (FILES/x["stored"]).unlink(missing_ok=True)
  raise
 except Exception as e:
  for x in saved: (FILES/x["stored"]).unlink(missing_ok=True)
  raise HTTPException(422,"تعذرت قراءة الصور: "+str(e))
 d={"id":ident,"title":meta["subject"] or saved[0]["filename"],"filename":saved[0]["filename"],"files":saved,"page_count":len(saved),**meta,"text":text,"uploaded_at":datetime.now(timezone.utc).isoformat(),"url":"/api/file/"+ident,"download":"/api/file/"+ident+"?download=1","review_required":not bool(text.strip())}
 items=rows(); items.insert(0,d); save(items)
 return {"ok":True,"document":{k:v for k,v in d.items() if k!="text"},"extracted_characters":len(text)}

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
