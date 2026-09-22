"""NABIL Lesson Factory pilot: deterministic quality gate for authored CRDP lessons.

Usage:
  python -m scripts.nabil_lesson_factory --pilot --report /tmp/nabil-pilot.json
  python -m scripts.nabil_lesson_factory --pilot --require-drive-write --report /tmp/nabil-pilot.json
  python -m scripts.nabil_lesson_factory --pilot --produce-first

No AI calls or deletes. --produce-first creates an explicitly labeled factory edition
from the existing authored source lesson; it never invents unseen PDF material.
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
    """Use the same service account as the application; do not expose secrets."""
    from scripts.index_books import get_drive_service
    service = get_drive_service()
    if write:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        from app.core.config import settings
        raw = (settings.GOOGLE_DRIVE_CREDENTIALS_JSON or "").strip()
        scopes = ["https://www.googleapis.com/auth/drive"]
        creds = (service_account.Credentials.from_service_account_info(json.loads(raw), scopes=scopes)
                 if raw else service_account.Credentials.from_service_account_file("drive_service_account.json", scopes=scopes))
        service = build("drive", "v3", credentials=creds)
    return service

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

def produce_first(require_drive_write=True):
    """Produce a real new Drive HTML, source-preserving, with embedded interactive lab.

    This is a factory edition of an ALREADY AUTHORED chapter, not extraction
    of an unseen textbook or certification of scientific completeness.
    Idempotent: same filename is updated only if the factory marker is present.
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
        raise PermissionError("FACTORY_DRIVE_WRITE_NOT_GRANTED")
    html = get_html(service, chapter["drive_html_id"])
    soup = BeautifulSoup(html, "html.parser")
    if not soup.find("main") or not soup.find("h1"):
        raise ValueError("SOURCE_LESSON_NOT_VALID_HTML")
    if chapter["title"].casefold() not in soup.find("h1").get_text(" ", strip=True).casefold():
        raise ValueError("SOURCE_LESSON_TITLE_MISMATCH")
    # Inline lab for offline/Drive portability. No external AI, no runtime key.
    lab_path = ROOT / "app/static/nabil_g7_physics_lab_v1.js"
    lab = lab_path.read_text(encoding="utf-8")
    if not lab or "g7-surface" not in lab or "g7-tubes" not in lab:
        raise ValueError("INTERACTIVE_LAB_NOT_READY")
    for node in soup.select("[data-nabil-factory-banner]"):
        node.decompose()
    banner = soup.new_tag("aside")
    banner["data-nabil-factory-banner"] = "1"
    banner["style"] = ("padding:12px;margin:14px auto;max-width:1010px;"
                       "border:2px solid #28bfc8;border-radius:12px;"
                       "background:#e8fcfc;color:#073c50;font:16px/1.6 Arial")
    banner.string = ("NABIL AI · Factory edition 1 — generated from the "
                     "previously authored lesson, G 07 physics.pdf pp. 13–17. "
                     "The lab is an explanatory simulation, not a scanned "
                     "textbook figure. Original exercise/figure fidelity "
                     "still requires source review.")
    soup.find("main").insert(0, banner)
    if not soup.find("meta", attrs={"name": "viewport"}):
        meta = soup.new_tag("meta", attrs={"name": "viewport",
                         "content": "width=device-width,initial-scale=1"})
        (soup.head or soup).append(meta)
    style = soup.new_tag("style")
    style.string = ("@media(max-width:760px){html,body,main{max-width:100%;"
                    "min-width:0;box-sizing:border-box}main{padding:10px}"
                    "img,svg,canvas{max-width:100%;height:auto}}")
    (soup.head or soup).append(style)
    # An inline script is safe here because the code is repository-owned and
    # the only source document is the trusted, owner-authored Drive lesson.
    lab_script = soup.new_tag("script")
    lab_script.string = lab.replace("</script", "<\\/script")
    (soup.body or soup).append(lab_script)
    rendered = str(soup)
    if len(rendered) > 8_000_000:
        raise ValueError("FACTORY_LESSON_EXCEEDS_VIEW_LIMIT")
    name = "G07-PHYSICS--SOLIDS-AND-LIQUIDS-FACTORY.html"
    existing = [f for f in children(service, PILOT_FOLDER)
                if f["name"].casefold() == name.casefold()]
    media = MediaIoBaseUpload(io.BytesIO(rendered.encode("utf-8")),
                              mimetype="text/html", resumable=False)
    if existing:
        previous = get_html(service, existing[0]["id"])
        if 'data-nabil-factory-banner="1"' not in previous:
            raise ValueError("REFUSE_OVERWRITE_NON_FACTORY_LESSON")
        file = service.files().update(fileId=existing[0]["id"], media_body=media,
                                      fields="id,name,webViewLink").execute()
        action = "updated"
    else:
        file = service.files().create(
            body={"name": name, "mimeType": "text/html",
                  "parents": [PILOT_FOLDER]},
            media_body=media, fields="id,name,webViewLink").execute()
        action = "created"
    # Read-back verification: no success claim based on an upload response alone.
    saved = get_html(service, file["id"])
    if 'data-nabil-factory-banner="1"' not in saved or "g7-tubes" not in saved:
        raise ValueError("FACTORY_READBACK_VERIFICATION_FAILED")
    return {"status": "FACTORY_EDITION_PUBLISHED_NEEDS_SOURCE_REVIEW",
            "action": action, "title": "Solids and Liquids — Factory edition",
            "filename": name, "drive_file_id": file["id"],
            "source_drive_html_id": chapter["drive_html_id"],
            "source_pdf_id": book["drive_file_id"],
            "bytes": len(saved.encode("utf-8")),
            "interactive_lab": True,
            "scientifically_verified": False,
            "view_url": "/api/interactive-lessons/view?grade=7&subject=physics&lesson="
                        + quote("SOLIDS AND LIQUIDS FACTORY")}

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
    ok = (report.get("production",{}).get("status") == "FACTORY_EDITION_PUBLISHED_NEEDS_SOURCE_REVIEW"
          or (not (args.produce_first or args.require_drive_write)
              and report["status"] == "PILOT_REQUIRES_SOURCE_REVIEW"))
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
