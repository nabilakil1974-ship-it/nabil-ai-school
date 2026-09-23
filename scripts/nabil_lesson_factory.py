"""NABIL Lesson Factory pilot: deterministic quality gate for authored CRDP lessons.

Usage:
  python -m scripts.nabil_lesson_factory --pilot --report /tmp/nabil-pilot.json
  python -m scripts.nabil_lesson_factory --pilot --require-drive-write --report /tmp/nabil-pilot.json
  python -m scripts.nabil_lesson_factory --pilot --produce-first

No AI calls or deletes. Production embeds actual PDF pages and refuses to publish
if the source cannot be read and rendered or the authored exercises are missing.
This gate is necessary, NOT sufficient, to certify scientific/source accuracy:
a reviewer must compare original PDF figures, exercises and solutions.
"""
import argparse
import io
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data/interactive_lesson_production_ledger.json"
OWNER_ROOT = "16bcmZMO_dn4FqlGaDtl8Hky6iSBEqZpX"
PILOT_FOLDER = "12BzdBUmPIK2__Fl3yTXpfZ-LXNjfimAq"
MIME_FOLDER = "application/vnd.google-apps.folder"
SUBJECTS = ("physics", "mathematics", "chemistry", "biology", "general_science")
REQUIRED = {
    "source": ("crdp", "source", "المصدر"),
    "activities": ("activity", "activities", "نشاط"),
    "exercises": ("exercise", "exercises", "تمرين"),
    "solutions": ("solution", "solutions", "حل"),
    "worksheet": ("worksheet", "check your understanding", "ورقة عمل"),
    "summary": ("summary", "reference card", "الخلاصة", "البطاقة المرجعية"),
}

def drive(write=False):
    """Read with the existing service account; write as the owner's OAuth user.

    Service accounts have no My Drive storage quota, even with Editor access.
    Never print OAuth tokens or fall back to service-account uploads.
    """
    from scripts.index_books import get_drive_service
    if not write:
        return get_drive_service()

    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    client_id = os.getenv("GOOGLE_DRIVE_OAUTH_CLIENT_ID", "").strip()
    client_secret = os.getenv("GOOGLE_DRIVE_OAUTH_CLIENT_SECRET", "").strip()
    refresh_token = os.getenv("GOOGLE_DRIVE_OAUTH_REFRESH_TOKEN", "").strip()
    if not all((client_id, client_secret, refresh_token)):
        raise RuntimeError(
            "OWNER_OAUTH_REQUIRED: configure GOOGLE_DRIVE_OAUTH_CLIENT_ID, "
            "GOOGLE_DRIVE_OAUTH_CLIENT_SECRET and GOOGLE_DRIVE_OAUTH_REFRESH_TOKEN "
            "in the nabil-ai-school Railway service; service accounts cannot "
            "create files in personal My Drive."
        )
    credentials = Credentials(
        token=None, refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id, client_secret=client_secret,
        scopes=["https://www.googleapis.com/auth/drive"],
    )
    credentials.refresh(Request())
    return build("drive", "v3", credentials=credentials, cache_discovery=False)

def children(service, folder):
    token = None
    while True:
        result = service.files().list(q=f"'{folder}' in parents and trashed=false",
            fields="nextPageToken,files(id,name,mimeType,webViewLink,capabilities(canAddChildren))",
            pageSize=1000, pageToken=token).execute()
        yield from result.get("files", [])
        token = result.get("nextPageToken")
        if not token:
            break

def get_html(service, file_id):
    from googleapiclient.http import MediaIoBaseDownload
    output = io.BytesIO()
    loader = MediaIoBaseDownload(output, service.files().get_media(fileId=file_id))
    done = False
    while not done:
        _, done = loader.next_chunk()
        if output.tell() > 20_000_000:
            raise ValueError("Lesson HTML exceeds 20 MB")
    return output.getvalue().decode("utf-8-sig")

def check_html(html, chapter):
    soup = BeautifulSoup(html, "html.parser")
    plain = soup.get_text(" ", strip=True).casefold()
    failures, warnings = [], []
    title = (soup.find("h1") or soup.title)
    title_text = title.get_text(" ", strip=True) if title else ""
    if not title or chapter["title"].casefold() not in title_text.casefold():
        failures.append("TITLE_NOT_MATCHED_TO_SOURCE_CHAPTER")
    if not soup.find("meta", attrs={"name":"viewport"}):
        failures.append("MOBILE_VIEWPORT_MISSING")
    if not soup.find("main"):
        failures.append("SEMANTIC_MAIN_MISSING")
    if len(plain) < 1200:
        failures.append("LESSON_TOO_SHORT_FOR_SOURCE_REVIEW")
    for name, tokens in REQUIRED.items():
        if not any(t in plain for t in tokens):
            failures.append("MISSING_"+name.upper())
    for n in chapter.get("source_exercises", []):
        if not re.search(r"(?:exercise|exercice|تمرين)\s*(?:n[°o.]?\s*)?"+str(n)+r"\b", plain, re.I):
            failures.append("SOURCE_EXERCISE_"+str(n)+"_NOT_VERIFIABLE")
    figures = soup.select("svg,img,canvas")
    if not figures:
        failures.append("FIGURES_NOT_EMBEDDED")
    if not soup.select("input,select,button,details"):
        failures.append("INTERACTIVITY_MISSING")
    if not any("powerpoint" in t or "pptx" in t for t in plain):
        warnings.append("PPTX_EXPORT_MUST_BE_VERIFIED_VIA_PLATFORM_ENDPOINT")
    if "draft" in plain or "not yet integrated" in plain or "require full figure" in plain:
        failures.append("EXPLICITLY_INCOMPLETE_DRAFT")
    warnings.extend(("SOURCE_FIGURE_FIDELITY_REQUIRES_VISUAL_REVIEW",
                     "SOLUTIONS_REQUIRE_INDEPENDENT_SCIENTIFIC_CHECK",
                     "RAILWAY_MOBILE_AND_PPTX_REQUIRE_LIVE_ACCEPTANCE"))
    return {"title":title_text, "pass":not failures, "failures":failures,
            "warnings":warnings, "figures":len(figures),
            "interactive_controls":len(soup.select("input,select,button,details"))}

def pilot(require_drive_write=False):
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    book = next(b for b in ledger["books"] if b.get("drive_file_id")=="1LasqIgGUuck1l-2EZbj2kA0Dg9ygJ_AH")
    service = drive(write=require_drive_write)
    root = service.files().get(fileId=OWNER_ROOT,
        fields="id,name,capabilities(canAddChildren,canReadRevisions)").execute()
    folder = service.files().get(fileId=PILOT_FOLDER,
        fields="id,name,capabilities(canAddChildren)").execute()
    report = {"timestamp":datetime.now(timezone.utc).isoformat(),
              "pilot":"Grade 7 English Physics",
              "drive_root":root["id"],"folder":folder["id"],
              "drive_can_add_children":folder.get("capabilities",{}).get("canAddChildren",False),
              "lessons":[],"status":"BLOCKED"}
    if require_drive_write and not report["drive_can_add_children"]:
        report["permission_error"]="Grant Editor to nabil-bot service account on curriculum root"
    existing = {f["name"].lower():f for f in children(service,PILOT_FOLDER)}
    for chapter in book.get("authored_lessons",[]):
        title = chapter["title"]
        name = "G07-PHYSICS--"+re.sub(r"[^A-Z0-9]+","-",title.upper()).strip("-")+".html"
        item = existing.get(name.lower())
        if not item:
            report["lessons"].append({"title":title,"pass":False,
                                     "failures":["OWNER_DRIVE_HTML_NOT_FOUND"],"expected":name})
            continue
        try:
            quality = check_html(get_html(service,item["id"]),chapter)
            quality.update({"drive_file_id":item["id"],"source_pdf":book["drive_file_id"],
                            "status":"NEEDS_HUMAN_SOURCE_VERIFICATION" if quality["pass"] else "REJECTED_PENDING_REPAIR"})
            report["lessons"].append(quality)
        except Exception as exc:
            report["lessons"].append({"title":title,"pass":False,
                                      "failures":["FETCH_OR_PARSE_"+type(exc).__name__]})
    all_lessons_pass = bool(report["lessons"]) and all(
        item["pass"] for item in report["lessons"]
    )
    drive_write_ok = not require_drive_write or report["drive_can_add_children"]
    report["status"] = (
        "PILOT_REQUIRES_SOURCE_REVIEW" if all_lessons_pass and drive_write_ok
        else "BLOCKED"
    )
    return report

def _source_pages(service, file_id, pages):
    """Extract original page images AND text from the actual Drive PDF.

    Page numbers are PDF indices, not an unverified printed-page offset.
    The PDF must be accessible and page content must corroborate the chapter.
    """
    import base64
    import subprocess
    import tempfile
    from pypdf import PdfReader
    from scripts.index_books import download_pdf
    raw = download_pdf(service, file_id)
    reader = PdfReader(io.BytesIO(raw))
    if max(pages) > len(reader.pages):
        raise ValueError("SOURCE_PDF_PAGE_OUT_OF_RANGE")
    result = []
    with tempfile.TemporaryDirectory(prefix="nabil_source_") as temp:
        pdf = Path(temp) / "book.pdf"
        pdf.write_bytes(raw)
        for p in pages:
            text = (reader.pages[p-1].extract_text() or "").strip()
            prefix = str(Path(temp) / ("page_" + str(p)))
            proc = subprocess.run(
                ["pdftoppm", "-f", str(p), "-l", str(p),
                 "-singlefile", "-scale-to", "1200", "-jpeg", "-jpegopt",
                 "quality=78", str(pdf), prefix],
                capture_output=True, timeout=70)
            image = Path(prefix + ".jpg")
            if proc.returncode or not image.is_file() or image.stat().st_size < 5000:
                raise RuntimeError("SOURCE_PAGE_RENDER_FAILED_" + str(p))
            result.append((p, text, base64.b64encode(image.read_bytes()).decode("ascii")))
    return result


def produce_first(require_drive_write=True):
    """Create source-illustrated Grade 7 Physics chapter from the actual PDF.

    Fail closed if the original source cannot be read/rendered or if the
    previously authored chapter is missing its exercises or solutions.
    Never label the result scientifically certified by automated checks.
    """
    from googleapiclient.http import MediaIoBaseUpload
    from urllib.parse import quote
    book = next(b for b in json.loads(LEDGER.read_text(encoding="utf-8"))["books"]
                if b.get("drive_file_id") == "1LasqIgGUuck1l-2EZbj2kA0Dg9ygJ_AH")
    chapter = next(x for x in book["authored_lessons"]
                   if x["title"] == "Solids and Liquids")
    service = drive(write=True)
    folder = service.files().get(fileId=PILOT_FOLDER,
                                 fields="id,capabilities(canAddChildren)").execute()
    if not folder.get("capabilities", {}).get("canAddChildren"):
        raise PermissionError("OWNER_DRIVE_WRITE_NOT_GRANTED")
    original = get_html(service, chapter["drive_html_id"])
    quality = check_html(original, chapter)
    if not quality["pass"]:
        raise ValueError("AUTHORED_SOURCE_LESSON_INCOMPLETE: " + ",".join(quality["failures"]))
    soup = BeautifulSoup(original, "html.parser")
    main = soup.find("main")
    if not main:
        raise ValueError("AUTHORED_LESSON_MAIN_MISSING")
    # Do not assume that a printed page number always equals a PDF page index.
    # This first pilot has the PDF-page range recorded in the ledger.
    pages = list(range(13, 18))
    source = _source_pages(service, book["drive_file_id"], pages)
    combined = " ".join(text for _, text, _ in source).casefold()
    if not ("solid" in combined and "liquid" in combined):
        raise ValueError("SOURCE_PAGES_DO_NOT_MATCH_CHAPTER")
    if not any("exercise" in text.casefold() for _, text, _ in source):
        raise ValueError("SOURCE_EXERCISE_PAGE_NOT_FOUND")
    if soup.select("[data-nabil-source-pages]"):
        raise ValueError("SOURCE_IMAGES_ALREADY_PRESENT")
    source_section = soup.new_tag("section", attrs={"class": "card",
                                      "data-nabil-source-pages": "1",
                                      "id": "original-source"})
    h2 = soup.new_tag("h2")
    h2.string = "Original textbook pages · source figures and exercises"
    source_section.append(h2)
    intro = soup.new_tag("p")
    intro.string = ("These are the actual PDF pages, not AI-drawn figures. "
                    "Use them to compare the adapted lesson and all six exercises.")
    source_section.append(intro)
    for p, _, encoded in source:
        figure = soup.new_tag("figure")
        img = soup.new_tag("img", attrs={
            "src": "data:image/jpeg;base64," + encoded,
            "alt": "Original G 07 physics.pdf PDF page " + str(p),
            "loading": "lazy",
            "style": "width:100%;height:auto;max-width:100%;border:1px solid #abc",
        })
        figure.append(img)
        caption = soup.new_tag("figcaption")
        caption.string = "Original G 07 physics.pdf · PDF page " + str(p)
        figure.append(caption)
        source_section.append(figure)
    main.append(source_section)
    worksheet = soup.new_tag("section", attrs={"class": "card", "id": "worksheet"})
    worksheet.append(BeautifulSoup("""
      <h2>Printable worksheet · Solids and Liquids</h2>
      <p>Use the original textbook pages above and the lesson cards.
      Write answers before opening the exercise solutions.</p>
      <ol>
        <li>Classify: pencil, milk, sand, water, salt. Explain sand and salt.</li>
        <li>Draw a horizontal free surface in three differently shaped vessels.</li>
        <li>Describe how a plumb line tests whether the surface is horizontal.</li>
        <li>Explain why a transparent tube shows the fuel level in a tank.</li>
        <li>Complete and solve the six numbered exercises from the original p. 17.</li>
      </ol>
      <p>Answers: refer to the explained activities, exercises 1–6 and
      final reference card above. This worksheet is an NABIL AI adaptation.</p>
    """, "html.parser"))
    main.append(worksheet)
    lab = (ROOT / "app/static/nabil_g7_physics_lab_v1.js").read_text(encoding="utf-8")
    if "g7-surface" not in lab or "g7-tubes" not in lab:
        raise ValueError("INTERACTIVE_LAB_NOT_READY")
    script = soup.new_tag("script")
    script.string = lab.replace("</script", "<\\/script")
    (soup.body or soup).append(script)
    css = soup.new_tag("style")
    css.string = ("@media(max-width:760px){html,body,main{max-width:100%;"
                  "min-width:0;box-sizing:border-box}main{padding:10px}"
                  "img,svg,canvas{max-width:100%;height:auto}}")
    (soup.head or soup).append(css)
    rendered = str(soup)
    final_quality = check_html(rendered, chapter)
    if not final_quality["pass"] or len(source_section.select("img")) != 5:
        raise ValueError("FINAL_LESSON_QUALITY_GATE_FAILED")
    name = "G07-PHYSICS--SOLIDS-AND-LIQUIDS-SOURCE-ILLUSTRATED.html"
    existing = [f for f in children(service, PILOT_FOLDER)
                if f["name"].casefold() == name.casefold()]
    if existing:
        raise FileExistsError("REFUSE_TO_OVERWRITE_EXISTING_SOURCE_LESSON")
    media = MediaIoBaseUpload(io.BytesIO(rendered.encode("utf-8")),
                              mimetype="text/html", resumable=False)
    file = service.files().create(
        body={"name": name, "mimeType": "text/html", "parents": [PILOT_FOLDER]},
        media_body=media, fields="id,name,webViewLink").execute()
    saved = get_html(service, file["id"])
    if (saved.count("data:image/jpeg;base64,") != 5 or
            "id=\"worksheet\"" not in saved or
            "g7-tubes" not in saved):
        raise ValueError("SOURCE_LESSON_READBACK_VERIFICATION_FAILED")
    return {"status": "SOURCE_ILLUSTRATED_LESSON_PUBLISHED_REQUIRES_SCIENTIFIC_REVIEW",
            "title": "Solids and Liquids · original source pages included",
            "drive_file_id": file["id"], "source_pdf_id": book["drive_file_id"],
            "source_pdf_pages": pages, "source_exercises": chapter["source_exercises"],
            "figures_original_pages": 5, "scientifically_verified": False,
            "bytes": len(saved.encode("utf-8")),
            "view_url": "/api/interactive-lessons/view?grade=7&subject=physics&lesson="
                        + quote("SOLIDS AND LIQUIDS SOURCE ILLUSTRATED")}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--pilot",action="store_true",required=True)
    ap.add_argument("--require-drive-write",action="store_true")
    ap.add_argument("--report",default="")
    ap.add_argument("--produce-first",action="store_true")
    args=ap.parse_args()
    try:
        report=pilot(args.require_drive_write)
        # Existing Railway worker uses --pilot --require-drive-write. The owner
        # explicitly requested production; keep that deployed command working.
        if args.produce_first or args.require_drive_write:
            report["production"] = produce_first()
    except Exception as exc:
        report={"status":"ERROR","error_type":type(exc).__name__,"error":str(exc)}
    data=json.dumps(report,ensure_ascii=False,indent=2)
    if args.report:
        Path(args.report).write_text(data,encoding="utf-8")
    print(data)
    ok = (report.get("production",{}).get("status") == "SOURCE_ILLUSTRATED_LESSON_PUBLISHED_REQUIRES_SCIENTIFIC_REVIEW"
          or (not args.produce_first and report.get("drive_can_add_children") is not False
              and report.get("status") in ("PILOT_REQUIRES_SOURCE_REVIEW", "BLOCKED")))
    if ok and (args.produce_first or args.require_drive_write) and os.getenv("PORT"):
        # Railway expects a persistent process. Serve a minimal status endpoint
        # after the one-shot upload, rather than showing CRASHED on normal exit.
        from http.server import BaseHTTPRequestHandler, HTTPServer
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                data = json.dumps(report, ensure_ascii=False).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
        HTTPServer(("0.0.0.0", int(os.environ["PORT"])), Handler).serve_forever()
    return 0 if ok else 2

if __name__=="__main__":
    sys.exit(main())
