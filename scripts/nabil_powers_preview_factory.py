"""Fail-closed Powers draft renderer from owner Google Doc; never publishes."""
import html, io, re
LESSON="G07-MATHEMATICS-69B7C840-001"
DOC="1LNV8uUpCGnw1DX5tSZvgSpEWY2gssEHir3rgxAz2KaE"
PENDING="1zJoMqzgA_XJGEEHhMHEgn5F5O0kCtOWn"
NAME="NABIL_DRAFT_"+LESSON+"_TEACHER_BOARD.html"

def render(source):
    if ("lesson_id: "+LESSON) not in source or "VII. FACTORY REQUIRED ACTION" not in source:
        raise ValueError("SOURCE_IDENTITY_OR_COMPLETENESS_FAILED")
    p=[]
    for raw in source.splitlines():
        line=raw.strip()
        if line.startswith("VII. FACTORY REQUIRED ACTION"): break
        if not line: continue
        if re.match(r"^(CARD \d+|Ex\d+|Problem \d+|[IVX]+\.)",line):
            p.append("<h2>"+html.escape(line)+"</h2>")
        elif re.match(r"^(TEACHER|OBSERVE|EXPLORE|DISCOVER|VERIFY|EXPLAIN|EXAMPLE|ASK|RULE|CHECK|CAUTION|LAB DESIGN|ANSWER|STUDENT PROMPT):",line):
            k,v=line.split(":",1)
            p.append("<p class='step'><b>"+html.escape(k)+":</b> "+html.escape(v)+"</p>")
        else: p.append("<p>"+html.escape(line)+"</p>")
    if not any("CARD 8" in x for x in p) or not any("Problem 4" in x for x in p):
        raise ValueError("SOURCE_COVERAGE_FAILED")
    css="""body{margin:0;background:#f5f7fb;color:#142943;font:17px/1.7 system-ui}main{max-width:980px;margin:auto;padding:18px}header{background:#082c49;color:white;padding:22px;border-radius:20px}article h2{background:#dceaf8;border-radius:12px;padding:16px;margin-top:28px}article p{background:white;border-radius:8px;padding:10px 15px;overflow-wrap:anywhere;white-space:pre-wrap}.step{border-left:4px solid #119579}.warning{background:#fff1cc;padding:12px;border-radius:8px}.lab,.golden{padding:20px;background:#e5f4ef;border-radius:15px;margin:20px 0}.golden{background:#ffedb9;border:4px solid #c69024}input{width:100%}@media(max-width:540px){main{padding:7px}article p{font-size:15px}}"""
    js="""<script>function go(){const b=+document.getElementById('base').value,e=+document.getElementById('exp').value;document.getElementById('val').textContent=b+' ^ '+e+' = '+b**e;}document.querySelectorAll('input').forEach(x=>x.addEventListener('input',go));go();</script>"""
    lab="<section class='lab'><h2>Interactive powers lab</h2>Base: <input id='base' type='range' min='1' max='10' value='3'> Exponent: <input id='exp' type='range' min='0' max='8' value='4'><output id='val'></output></section>"
    golden="<section id='goldenReferenceCard' class='golden'><h2>FINAL GOLDEN CARD</h2><p>aⁿ means repeated multiplication. a¹=a; a⁰=1 for a≠0.</p><p>aᵐ×aⁿ=aᵐ⁺ⁿ; (aᵐ)ⁿ=aᵐⁿ; (ab)ⁿ=aⁿbⁿ; (a/b)ⁿ=aⁿ/bⁿ, b≠0.</p></section>"
    return "<!doctype html><html lang='en'><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>NABIL Powers DRAFT</title><style>"+css+"</style><main><header><h1>POWERS — Grade 7</h1><p>Source: Building up Mathematics — PDF pp.15–23</p></header><p class='warning'>DRAFT ONLY. Independent scientific review and V18 Playwright checks NOT PASSED. Not published.</p>"+lab+"<article>"+"".join(p)+"</article>"+golden+js+"</main></html>"

def main():
    from googleapiclient.http import MediaIoBaseUpload
    from scripts import nabil_lesson_factory as factory
    drive=factory.get_drive_service()
    source_bytes=drive.files().export(fileId=DOC,mimeType="text/plain").execute()
    source=source_bytes.decode("utf-8-sig") if isinstance(source_bytes,bytes) else str(source_bytes)
    payload=render(source).encode("utf-8")
    q="name = '%s' and '%s' in parents and trashed = false"%(NAME,PENDING)
    hits=drive.files().list(q=q,fields="files(id,name)").execute().get("files",[])
    if len(hits)>1: raise RuntimeError("DUPLICATE_PREVIEW")
    media=MediaIoBaseUpload(io.BytesIO(payload),mimetype="text/html")
    if hits:
        fid=hits[0]["id"];drive.files().update(fileId=fid,media_body=media).execute()
    else:
        fid=drive.files().create(body={"name":NAME,"parents":[PENDING],"mimeType":"text/html"},media_body=media,fields="id").execute()["id"]
    if drive.files().get_media(fileId=fid).execute()!=payload:raise RuntimeError("READBACK_MISMATCH")
    print("DRAFT_HTML_DRIVE_VERIFIED",fid,"bytes",len(payload),flush=True)
    print("INDEPENDENT_REVIEW_NOT_RUN_AND_NO_PUBLISH",flush=True)

if __name__=="__main__":main()
