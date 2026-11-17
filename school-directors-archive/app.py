import os, json, uuid, shutil
from pathlib import Path
from datetime import datetime, timezone
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
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
ALLOWED={".pdf",".docx",".doc",".png",".jpg",".jpeg",".webp",".tif",".tiff"}
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
 if ext==".doc": raise ValueError("حوّل ملف DOC القديم إلى DOCX أو PDF.")
 return ""
@app.get("/api/health")
def health(): return {"status":"ok","ocr_languages":"ara+fra+eng"}
@app.get("/api/documents")
def documents(): return rows()
@app.post("/api/upload")
async def upload(file:UploadFile=File(...),category:str=Form(...),number:str=Form(""),date:str=Form(""),issuer:str=Form(""),subject:str=Form("")):
 name=Path(file.filename or "document").name; ext=Path(name).suffix.lower()
 if ext not in ALLOWED: raise HTTPException(415,"نوع الملف غير مدعوم")
 ident=uuid.uuid4().hex; target=FILES/(ident+ext)
 with target.open("wb") as out: shutil.copyfileobj(file.file,out)
 try: text=extract(target,ext)
 except Exception as e:
  target.unlink(missing_ok=True); raise HTTPException(422,"فشل استخراج النص: "+str(e))
 d={"id":ident,"title":name,"filename":name,"category":category,"number":number,"date":date,"issuer":issuer,"subject":subject,"text":text,"uploaded_at":datetime.now(timezone.utc).isoformat(),"url":"/api/file/"+ident,"download":"/api/file/"+ident+"?download=1"}
 items=rows(); items.insert(0,d); save(items)
 return {"ok":True,"document":{k:v for k,v in d.items() if k!="text"},"extracted_characters":len(text)}
@app.get("/api/file/{ident}")
def get_file(ident:str,download:int=0):
 d=next((x for x in rows() if x["id"]==ident),None)
 if not d: raise HTTPException(404,"غير موجود")
 p=FILES/(ident+Path(d["filename"]).suffix.lower())
 if not p.exists(): raise HTTPException(404,"الملف غير متاح")
 return FileResponse(p,filename=d["filename"],content_disposition_type="attachment" if download else "inline")
@app.get("/api/ask")
def ask(q:str):
 items=[]
 for d in rows():
  body=(d.get("text","")+" "+d.get("subject","")+" "+d.get("title","")).lower()
  score=sum(body.count(w) for w in q.lower().split() if len(w)>2)
  if score: items.append({"title":d["title"],"number":d["number"],"date":d["date"],"url":d["url"],"score":score,"text":d["text"][:900]})
 return {"question":q,"results":sorted(items,key=lambda x:x["score"],reverse=True)[:8],"notice":"تحقق من المستند الأصلي قبل اعتماد أي معلومة."}
