"""NABIL Lesson Factory pilot: deterministic quality gate for authored CRDP lessons.

Usage:
  python -m scripts.nabil_lesson_factory --pilot --report /tmp/nabil-pilot.json
  python -m scripts.nabil_lesson_factory --pilot --require-drive-write --report /tmp/nabil-pilot.json

No AI calls, no deletes, no publishing. A failed lesson is never marked complete.
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
        if not re.search(r"(?:exercise|exercice|تمرين)\\s*(?:n[°o.]?\\s*)?"+str(n)+r"\\b", plain, re.I):
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
    report["status"]="PILOT_REQUIRES_SOURCE_REVIEW" if report["lessons"] and all(
        item["pass"] for item in report["lessons"]) and
        (not require_drive_write or report["drive_can_add_children"]) else "BLOCKED"
    return report

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--pilot",action="store_true",required=True)
    ap.add_argument("--require-drive-write",action="store_true")
    ap.add_argument("--report",default="")
    args=ap.parse_args()
    try:
        report=pilot(args.require_drive_write)
    except Exception as exc:
        report={"status":"ERROR","error_type":type(exc).__name__,"error":str(exc)}
    data=json.dumps(report,ensure_ascii=False,indent=2)
    if args.report:
        Path(args.report).write_text(data,encoding="utf-8")
    print(data)
    return 0 if report["status"]=="PILOT_REQUIRES_SOURCE_REVIEW" else 2

if __name__=="__main__":
    sys.exit(main())
