#!/usr/bin/env python3
"""Source-first, resumable ONE-BOOK lesson production; never fake an index.

Usage: python -m scripts.nabil_book_factory --book-id <actual Drive PDF ID>
       python -m scripts.nabil_book_factory --book-id <id> --index-only

The book's own scanned TOC and independently checked opening pages determine
lesson boundaries. No manually authored canonical catalog is required.
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import io
import json
import os
import re
import subprocess
import tempfile
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

from scripts import nabil_lesson_factory as factory

ROOT = Path(__file__).resolve().parents[1]
BOOK_INDEX_DIR = ROOT / "data" / "factory_book_indexes"
BOOK_RUNS_DIR = ROOT / "data" / "factory_book_runs"
BOOK_INDEX_DIR.mkdir(parents=True, exist_ok=True)
BOOK_RUNS_DIR.mkdir(parents=True, exist_ok=True)
MANIFESTS = (
    ROOT / "data/physics_textbooks_manifest.json",
    ROOT / "data/math_textbooks_manifest.json",
    ROOT / "data/chemistry_textbooks_manifest.json",
    ROOT / "data/biology_textbooks_manifest.json",
)


def announce(stage: str, **kwargs):
    print(json.dumps({"time": datetime.now(timezone.utc).isoformat(),
                      "stage": stage, **kwargs}, ensure_ascii=False), flush=True)


def registered_book(book_id: str, *, drive_service=None, grade: str = "", subject: str = "", language: str = "", branch: str = "") -> dict:
    matches = []
    for path in MANIFESTS:
        if not path.is_file():
            continue
        for book in json.loads(path.read_text(encoding="utf-8")).get("books", []):
            if book.get("drive_file_id") == book_id:
                matches.append(book)
    if not matches:
        if not all((str(grade).strip(), str(subject).strip(), str(language).strip())):
            raise RuntimeError(
                "NEW_BOOK_METADATA_REQUIRED: choose grade, subject, language; do not infer them from PDF filename"
            )
        if drive_service is None:
            drive_service = factory.get_drive_service()
        meta = drive_service.files().get(
            fileId=book_id, fields="id,name,mimeType,trashed"
        ).execute()
        if (meta.get("id") != book_id or meta.get("trashed")
                or meta.get("mimeType") != "application/pdf"):
            raise RuntimeError("SOURCE_IS_NOT_ORIGINAL_DRIVE_PDF")
        _ = grade_number(grade)
        _ = subject_name(subject)
        if language.strip().lower() not in ("english", "français", "french", "en", "fr"):
            raise RuntimeError("BOOK_LANGUAGE_UNSUPPORTED: provide English or Français")
        return {
            "grade": grade.strip(), "subject": subject.strip(),
            "language": language.strip(), "title": meta["name"],
            "drive_file_id": book_id, "branch": branch.strip(),
            "registration": "SOURCE_DRIVE_PDF_CLASSIFIED_BY_OWNER",
        }
    # A shared PDF in two secondary streams is not two source PDFs.
    if len({(b['language'], b['subject']) for b in matches}) != 1:
        raise RuntimeError("BOOK_MANIFEST_AMBIGUOUS: same PDF has incompatible subjects/languages")
    result = dict(matches[0])
    grades = {b['grade'] for b in matches}
    if len(grades) > 1 and any(not x.startswith("الثالث ثانوي") for x in grades):
        raise RuntimeError("BOOK_GRADE_AMBIGUOUS: select stream before producing")
    return result


def grade_number(grade: str) -> int:
    grade = str(grade).strip()
    m = re.search(r"(\d+)", grade)
    if m:
        n = int(m.group())
        if 1 <= n <= 12:
            return n
    for word, value in (("السابع", 7), ("الثامن", 8), ("التاسع", 9),
                        ("الأول ثانوي", 10), ("الثاني ثانوي", 11),
                        ("الثالث ثانوي", 12),
                        ("الصف الأول", 1), ("الصف الثاني", 2),
                        ("الصف الثالث", 3), ("الصف الرابع", 4),
                        ("الصف الخامس", 5), ("الصف السادس", 6)):
        if word in grade:
            return value
    raise RuntimeError(f"BOOK_GRADE_UNSUPPORTED: {grade}")


def subject_name(value: str) -> str:
    values = {"فيزياء": "physics", "رياضيات": "mathematics", "كيمياء": "chemistry",
              "علوم الحياة": "biology", "علوم عامة": "general_science"}
    result = values.get(value.strip(), value.strip().lower().replace(" ", "_"))
    if result not in factory.SUBJECT_PROFILES:
        raise RuntimeError(f"BOOK_SUBJECT_UNSUPPORTED: {value}")
    return result


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.casefold())
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^\w]+", " ", text)
    return " ".join(text.split())


def local_ocr(page, *, clip=None, dpi=190, psm=6, lang="eng+fra") -> str:
    """No textbook image leaves Railway: local OCR only for TOC + title checks."""
    import fitz
    if clip is not None:
        clip = fitz.Rect(*clip)
    pix = page.get_pixmap(dpi=dpi, clip=clip)
    with tempfile.TemporaryDirectory(prefix="nabil-toc-") as folder:
        image = Path(folder) / "page.png"
        pix.save(str(image))
        result = subprocess.run(
            ["tesseract", str(image), "stdout", "-l", lang, "--psm", str(psm)],
            capture_output=True, text=True, timeout=35,
        )
    if result.returncode:
        raise RuntimeError("LOCAL_TOC_OCR_FAILED: " + result.stderr[-220:])
    return result.stdout


# Scanned chapter headings sometimes have a decorative separated drop cap:
# "G hapter 5", "Cc hapter 11", "Ch apter 14".
HEADING = re.compile(r"(?im)^\s*(?:ch\s*apter|[a-z{©=]{1,2}\s*hapter)\s*(\d{1,2})\s*[:;.]*\s*$")


def chapter_rows(text: str, toc_pdf_page: int) -> list[dict]:
    matches = list(HEADING.finditer(text))
    rows = []
    for j, match in enumerate(matches):
        end = matches[j + 1].start() if j + 1 < len(matches) else min(len(text), match.end() + 480)
        following = [line.strip(" :-;\t") for line in text[match.end():end].splitlines() if line.strip()]
        if not following:
            continue
        title_raw = following[0]
        # Page numbers are hints, not trusted boundary evidence. e.g. "Volume: 19".
        title = re.sub(r"\s*[:;|. ]*\d{1,3}\s*\|?\s*$", "", title_raw).strip(" :-;|\t")
        title = re.sub(r"\s*:\s*[&a-zA-Z]{1,2}$", "", title).strip(" :-;|\t")
        if not (3 <= len(title) <= 100) or re.match(r"^(?:\d+[.)-]|exercises?)", title, re.I):
            continue
        page_match = re.search(r"(?<!\d)(\d{1,3})\s*$", title_raw)
        printed_hint = int(page_match.group(1)) if page_match else None
        rows.append({"chapter_number": int(match.group(1)), "title": title, "printed_start_hint": printed_hint,
                     "toc_pdf_page": toc_pdf_page,
                     "toc_ocr_excerpt": text[match.start():min(end, match.end()+130)].strip()})
    return rows


def scan_original_toc(doc) -> list[dict]:
    """Find true multi-chapter TOC pages rather than treating filenames as TOCs."""
    bookmark = doc.get_toc()
    if bookmark:
        candidates = [{"chapter_number": int(m.group(1)), "title": m.group(2).strip(),
                       "toc_pdf_page": None, "pdf_start_page": int(page)}
                      for depth, title, page in bookmark
                      for m in [re.match(r"(?:chapter|chapitre)\s*(\d+)\s*[:.-]?\s*(.+)", title, re.I)]
                      if depth <= 2 and m]
        if len(candidates) >= 2:
            return validate_sequence(candidates)

    if not shutil_which_tesseract():
        raise RuntimeError("DEPENDENCY_MISSING:tesseract required for scanned TOC")
    discovered = []
    found_toc_pages = 0
    # A TOC must appear in the book's front matter, not in a content chapter.
    limit = min(len(doc), max(18, min(32, round(len(doc) * .18))))
    for ix in range(limit):
        page = doc[ix]
        quick = local_ocr(page, dpi=165, psm=3)
        if len(re.findall(r"(?i)(?:chapter|[a-z]\s*hapter)\s*\d{1,2}", quick)) < 3:
            if found_toc_pages:
                break  # End of consecutive physical TOC pages.
            continue
        found_toc_pages += 1
        # Two columns: OCR each reading column separately so titles and numbers
        # from opposite columns cannot be interleaved.
        for x0, x1 in ((0, .5), (.5, 1.0)):
            text = local_ocr(page, clip=(page.rect.x0 + page.rect.width*x0,
                                        page.rect.y0 + page.rect.height*.13,
                                        page.rect.x0 + page.rect.width*x1,
                                        page.rect.y1 - page.rect.height*.05),
                             dpi=255, psm=6)
            discovered += chapter_rows(text, ix+1)
        announce("TOC_PAGE_SCANNED", pdf_page=ix+1, candidates=len(discovered))
    return validate_sequence(discovered)


def shutil_which_tesseract() -> bool:
    from shutil import which
    return bool(which("tesseract"))


def validate_sequence(rows: list[dict]) -> list[dict]:
    ordered = sorted(rows, key=lambda r: r["chapter_number"])
    numbers = [r["chapter_number"] for r in ordered]
    if len(numbers) < 2 or numbers != list(range(1, max(numbers) + 1)):
        raise RuntimeError("TOC_NOT_FOUND_OR_AMBIGUOUS: missing/duplicate chapter numbers: " + repr(numbers))
    if len({normalize(r["title"]) for r in ordered}) != len(ordered):
        raise RuntimeError("TOC_AMBIGUOUS: duplicate source chapter title")
    announce("SOURCE_TOC_FOUND", count=len(ordered), titles=[r["title"] for r in ordered])
    return ordered


def _header_ocr(page, variant: str = "rgb", psm: int = 6) -> str:
    """Read ONLY original colored chapter heading; try local OCR color bands."""
    from PIL import Image, ImageOps
    import fitz
    pix = page.get_pixmap(dpi=255, clip=fitz.Rect(
        0, 0, page.rect.width, page.rect.height*.18))
    img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
    if variant == "gray":
        img = ImageOps.grayscale(img)
    elif variant == "red":
        img = ImageOps.invert(img.getchannel("R"))
    elif variant == "sat":
        img = img.convert("HSV").getchannel("S")
    with tempfile.TemporaryDirectory(prefix="nabil-header-") as folder:
        path = Path(folder)/"header.png"
        img.save(path)
        proc = subprocess.run(["tesseract", str(path), "stdout", "-l", "eng+fra",
                               "--psm", str(psm)], capture_output=True, text=True,
                              timeout=25)
    if proc.returncode:
        raise RuntimeError("LOCAL_HEADING_OCR_FAILED: " + proc.stderr[-160:])
    return " ".join(proc.stdout.split())


def _title_match(title: str, header: str, chapter: int) -> float:
    title_norm = normalize(title).replace(" ", "")
    header_norm = normalize(header).replace(" ", "")
    if not title_norm or not header_norm:
        return 0
    if title_norm in header_norm:
        return 1.0
    window = len(title_norm)
    best = max((difflib.SequenceMatcher(None,title_norm,header_norm[i:i+window+2]).ratio()
                for i in range(max(1,len(header_norm)-window+2))),default=0)
    return best


def _best_header_match(page, row: dict) -> tuple[float,str]:
    best=(0.0, "")
    for variant,mode in (("rgb",6),("red",6),("gray",6),("sat",6),
                         ("red",11),("sat",11),("gray",11)):
        header=_header_ocr(page,variant,psm=mode)
        score=_title_match(row["title"],header,row["chapter_number"])
        marker = bool(re.search(r"(?:ch\s*apter|[a-z]\s*hapter)\s*"+
                                str(row["chapter_number"])+r"\b",normalize(header)))
        # Ornate drop-cap OCR may lose a chapter prefix, so high title
        # similarity is accepted only in the first 18% title band.
        if score>=.99 or score>=.92 or (score>=.83 and marker):
            return score,header
        if score>best[0]:best=score,header
    return best


def verify_openers(doc, rows: list[dict]) -> list[dict]:
    """Cross-check exact book TOC vs physical chapter-opening images."""
    if all(row.get("pdf_start_page") for row in rows):
        # PDF bookmarks are useful hints, not proof that the title and source
        # opening page agree. Verify each original opener before trusting it.
        results = []
        for row in rows:
            page_num = int(row["pdf_start_page"])
            if not 1 <= page_num <= len(doc):
                raise RuntimeError("BOOKMARK_PAGE_OUT_OF_RANGE")
            score, header = _best_header_match(doc[page_num-1], row)
            if score < .92:
                raise RuntimeError(
                    f"BOOKMARK_OPENING_UNVERIFIED: chapter={row['chapter_number']} "
                    f"page={page_num} score={score:.2f}"
                )
            results.append({**row, "heading_ocr_excerpt": header[:200],
                            "opening_match_score": round(score, 3)})
            announce("BOOKMARK_OPENING_VERIFIED", chapter=row["chapter_number"],
                     pdf_page=page_num)
    else:
        results=[]
        lower=max(row["toc_pdf_page"] or 1 for row in rows)+1
        for row in rows:
            n=int(row["chapter_number"])
            hint=row.get("printed_start_hint")
            candidates=[]
            # A printed TOC number is a hint only; never accept it without
            # inspecting the actual opener image.
            if isinstance(hint,int) and lower<=hint<=len(doc):
                candidates += [hint]
            candidates += [i for i in range(lower,len(doc)+1) if i not in candidates]
            found=None
            for page_num in candidates:
                score,header=_best_header_match(doc[page_num-1],row)
                if score>=.92 or (score>=.83 and bool(re.search(
                    r"(?:ch\s*apter|[a-z]\s*hapter)\s*"+str(n)+r"\b",normalize(header)))):
                    found=page_num
                    break
            if found is None:
                raise RuntimeError(f"OPENING_PAGE_NOT_VERIFIED: chapter={n} {row['title']}")
            # Resolve a TOC OCR typo only when the independently read opener
            # has an equally long, highly similar title after its heading.
            corrected=row["title"]
            tail=re.search(r"[:;]\s*([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ \-]{2,90})$",header)
            if tail:
                from_opener=" ".join(tail.group(1).split()).strip(" -")
                similarity=difflib.SequenceMatcher(
                    None,normalize(corrected),normalize(from_opener)).ratio()
                if .91<=similarity<1 and len(from_opener.split())==len(corrected.split()):
                    corrected=from_opener
            results.append({**row,"title":corrected,"pdf_start_page":found,
                            "heading_ocr_excerpt":header[:200]})
            lower=found+1
            announce("CHAPTER_OPENING_VERIFIED",chapter=n,title=row["title"],pdf_page=found)
    starts=[r["pdf_start_page"] for r in results]
    if starts!=sorted(set(starts)) or min(starts)<1 or max(starts)>len(doc):
        raise RuntimeError("CHAPTER_BOUNDARIES_AMBIGUOUS: source pages not strictly ascending")
    for i,row in enumerate(results):
        row["pdf_end_page"]=(results[i+1]["pdf_start_page"]-1
                             if i+1<len(results) else len(doc))
        if row["pdf_end_page"]<row["pdf_start_page"]:
            raise RuntimeError("CHAPTER_BOUNDARIES_AMBIGUOUS: empty chapter")
    return results


def build_index(doc, book: dict, *, book_id: str, pdf_hash: str) -> dict:
    toc = scan_original_toc(doc)
    toc = verify_openers(doc, toc)
    subject = subject_name(book["subject"])
    grade = grade_number(book["grade"])
    lang = "fr" if book.get("language", "").casefold() in ("fr", "french", "français") else "en"
    entries=[]
    for row in toc:
        number=row["chapter_number"]
        # Original pilot ID stays stable; other source PDFs include a unique
        # source ID fragment so EN/FR or different editions never collide.
        pilot_book = "1LasqIgGUuck1l-2EZbj2kA0Dg9ygJ_AH"
        namespace = "" if book_id == pilot_book else hashlib.sha256(
            book_id.encode("utf-8")).hexdigest()[:8].upper() + "-"
        entries.append({"lesson_id": f"G{grade:02d}-{subject.upper().replace('_','-')}-{namespace}{number:03d}",
                        "canonical_title": row["title"],
                        "grade": grade, "subject": subject, "language": lang,
                        "book_id": book_id, "source_book_title": book["title"],
                        "source_key": ("" if book_id == pilot_book else namespace.rstrip("-")),
                        "pdf_start_page": row["pdf_start_page"],
                        "pdf_end_page": row["pdf_end_page"],
                        "toc_pdf_page": row.get("toc_pdf_page"),
                        "source_book_sha256": pdf_hash,
                        "source_index_method": "TOC_PLUS_INDEPENDENT_OPENER",
                        "chapter_number": number,
                        "catalog_status": "SOURCE_TOC_AND_OPENING_VERIFIED_NOT_PRODUCED",
                        "source_pdf_sha256": pdf_hash})
    return {"schema_version": 2, "book_id": book_id, "source_pdf_sha256": pdf_hash,
            "source_book": {k: book.get(k) for k in ("title", "grade", "subject", "language", "branch", "registration")},
            "total_pdf_pages": len(doc), "index_method": "ACTUAL_TOC_PLUS_PHYSICAL_OPENING_LOCAL_OCR",
            "indexed_at": datetime.now(timezone.utc).isoformat(), "lessons": entries}


def remote_checkpoint(service, root_id: str, book_id: str, data: dict | None = None) -> dict | None:
    """Durable per-book ledger stored in Drive, not ephemeral Railway /app."""
    from googleapiclient.http import MediaIoBaseUpload
    folder_name="NABIL Factory Checkpoints"
    q="name = '%s' and mimeType = 'application/vnd.google-apps.folder' and '%s' in parents and trashed = false" % (folder_name,root_id)
    hits=service.files().list(q=q,fields="files(id)").execute().get("files",[])
    if len(hits)>1:
        raise RuntimeError("CHECKPOINT_FOLDER_AMBIGUOUS")
    if hits:
        folder=hits[0]["id"]
    elif data is not None:
        folder=service.files().create(body={"name":folder_name,"mimeType":"application/vnd.google-apps.folder","parents":[root_id]},fields="id").execute()["id"]
    else:
        return None
    filename=f"BOOK_{book_id}.json"
    nameq="name = '%s' and '%s' in parents and trashed = false" % (filename,folder)
    items=service.files().list(q=nameq,fields="files(id)").execute().get("files",[])
    if len(items)>1:
        raise RuntimeError("CHECKPOINT_DUPLICATE_FILES")
    if data is None:
        if not items:
            return None
        media=service.files().get_media(fileId=items[0]["id"]).execute()
        return json.loads(media.decode("utf-8") if isinstance(media,bytes) else media)
    payload=MediaIoBaseUpload(io.BytesIO(json.dumps(data,ensure_ascii=False,indent=2).encode("utf-8")),mimetype="application/json")
    if items:
        service.files().update(fileId=items[0]["id"],media_body=payload).execute()
    else:
        service.files().create(body={"name":filename,"parents":[folder]},media_body=payload,fields="id").execute()
    return data


def run(book_id: str, *, index_only: bool, publish: bool,
        grade: str = "", subject: str = "", language: str = "",
        branch: str = "", max_new_lessons: int = 0) -> dict:
    if max_new_lessons < 0:
        raise RuntimeError("MAX_NEW_LESSONS_INVALID: must be zero or positive")
    import fitz
    factory.PROGRESS_STARTED=time.monotonic()
    service=factory.get_drive_service()
    book=registered_book(book_id, drive_service=service, grade=grade,
                         subject=subject, language=language, branch=branch)
    announce("BOOK_SELECTED", book_id=book_id, title=book["title"], grade=book["grade"])
    factory.execute_preflight_checks(require_drive=publish)
    if publish:
        root_id = factory.resolve_drive_root_id()
        destination = service.files().get(
            fileId=root_id, fields="id,name,mimeType,driveId,capabilities(canAddChildren)"
        ).execute()
        if (destination.get("mimeType") != "application/vnd.google-apps.folder"
                or destination.get("capabilities", {}).get("canAddChildren") is not True):
            raise RuntimeError(
                "DRIVE_DESTINATION_NOT_WRITABLE: production identity cannot add "
                "files to the selected curriculum root. Grant the Railway Drive "
                "service account Editor access before running OCR/production."
            )
        # Service accounts have no personal My Drive storage quota even when
        # Editor: fail before OCR/checkpoint retries; Shared Drives are different.
        if (not destination.get("driveId")
                and not os.getenv("NABIL_DRIVE_OAUTH_TOKEN_JSON", "").strip()):
            raise RuntimeError(
                "PERSONAL_DRIVE_REQUIRES_USER_OAUTH: service accounts cannot "
                "upload new files into a personal My Drive. Authorize the "
                "owner and set NABIL_DRIVE_OAUTH_TOKEN_JSON in Railway secrets."
            )
        announce("DRIVE_DESTINATION_WRITE_PERMISSION_VERIFIED",
                 folder=destination.get("name", ""), folder_id=root_id)
    book_path=factory.resolve_source_book_pdf(book_id,service)
    pdf_hash=hashlib.sha256(book_path.read_bytes()).hexdigest()
    local_index=BOOK_INDEX_DIR/f"{book_id}.json"
    cached=json.loads(local_index.read_text(encoding="utf-8")) if local_index.exists() else None
    root = factory.resolve_drive_root_id() if (
        publish or os.getenv("NABIL_CURRICULUM_ROOT_ID")
        or os.getenv("NABIL_INTERACTIVE_CURRICULUM_ROOT_ID")
        or os.getenv("NABIL_LESSON_DRIVE_ROOT")
    ) else None
    saved=remote_checkpoint(service,root,book_id) if root else None
    if saved and saved.get("source_pdf_sha256") != pdf_hash:
        raise RuntimeError("SOURCE_BOOK_CHANGED: manual source edition reconciliation required")
    if (cached and cached.get("schema_version") == 2
            and cached.get("source_pdf_sha256") == pdf_hash
            and cached.get("index_method") == "ACTUAL_TOC_PLUS_PHYSICAL_OPENING_LOCAL_OCR"):
        index=cached
    elif (saved and saved.get("index",{}).get("schema_version") == 2
          and saved.get("index",{}).get("source_pdf_sha256") == pdf_hash
          and saved.get("index",{}).get("index_method") == "ACTUAL_TOC_PLUS_PHYSICAL_OPENING_LOCAL_OCR"):
        index=saved["index"]
    else:
        with fitz.open(str(book_path)) as doc:
            index=build_index(doc,book,book_id=book_id,pdf_hash=pdf_hash)
    local_index.write_text(json.dumps(index,ensure_ascii=False,indent=2),encoding="utf-8")
    announce("BOOK_INDEX_VERIFIED", count=len(index["lessons"]), book_id=book_id)
    if index_only:
        # Persist the source-derived TOC in Drive as well as Railway's
        # replaceable /app filesystem. Do not overwrite a production ledger.
        if root:
            checkpoint = saved or {
                "book_id": book_id, "source_pdf_sha256": pdf_hash,
                "index": index, "lessons": {}
            }
            checkpoint["index"] = index
            remote_checkpoint(service, root, book_id, checkpoint)
        return {"status":"INDEXED_NOT_PRODUCED", "index_file":str(local_index),
                "lessons":index["lessons"], "drive_checkpoint":bool(root)}
    if not publish:
        raise RuntimeError("PUBLISH_REQUIRED: full-book run must upload verified lessons to Drive")
    state=saved or {"book_id":book_id,"source_pdf_sha256":pdf_hash,"index":index,"lessons":{}}
    if state.get("index",{}).get("source_pdf_sha256")!=pdf_hash:
        raise RuntimeError("CHECKPOINT_INDEX_MISMATCH")
    remote_checkpoint(service,root,book_id,state)
    done=0
    newly_published=0
    for entry in index["lessons"]:
        lid=entry["lesson_id"]
        old=state["lessons"].get(lid,{})
        if old.get("status")=="PUBLISHED_VERIFIED" and old.get("drive_theory_id") and old.get("drive_exercises_id"):
            done+=1
            announce("LESSON_ALREADY_PUBLISHED_SKIPPED",lesson_id=lid)
            continue
        state["lessons"][lid]={"status":"RUNNING","started_at":datetime.now(timezone.utc).isoformat()}
        remote_checkpoint(service,root,book_id,state)
        announce("LESSON_START",lesson_id=lid,title=entry["canonical_title"])
        try:
            # The owner's full-book command, unlike the single QA-only pilot,
            # authorizes promotion only AFTER all original science/mobile gates.
            report=factory.produce_lesson_for_entry(entry,drive_service=service,publish=True,allow_pilot_publish=True)
            if report.get("status")!="PUBLISHED_VERIFIED":
                raise RuntimeError("LESSON_NOT_PUBLISHED_VERIFIED")
            ev_file = factory.PERM_EVIDENCE_DIR / f"{lid}.json"
            if not ev_file.is_file():
                raise RuntimeError("EXERCISE_INDEX_NOT_PERSISTED: source evidence absent")
            evidence = json.loads(ev_file.read_text(encoding="utf-8"))
            exercise_index = [{
                "exercise_id": ex["exercise_id"],
                "number": ex["number"],
                "section_type": ex["section_type"],
                "source_page": ex["source_page"],
                "exact_source_prompt": ex["exact_source_prompt"],
                "subquestions": ex.get("subquestions", []),
                "figure_refs": ex.get("figure_refs", []),
                "source_prompt_hash": ex["source_prompt_hash"],
            } for ex in evidence["exercise_evidence"]]
            state["lessons"][lid]={"status":"PUBLISHED_VERIFIED",
                "source_exercises": exercise_index,
                "indexed_exercise_count": len(exercise_index),
                "drive_theory_id":report["drive_theory_id"],
                "drive_exercises_id":report["drive_exercises_id"],
                "source_pages":report["source_pages"],
                "completed_at":datetime.now(timezone.utc).isoformat()}
            remote_checkpoint(service,root,book_id,state)
            done+=1
            newly_published+=1
            announce("LESSON_PUBLISHED",lesson_id=lid,done=done,total=len(index["lessons"]),
                     drive_theory_id=report["drive_theory_id"],
                     drive_exercises_id=report["drive_exercises_id"])
            if max_new_lessons and newly_published >= max_new_lessons:
                state["status"] = "FIRST_LESSON_PUBLISHED_VERIFIED" if max_new_lessons == 1 else "PARTIAL_PRODUCTION_VERIFIED"
                remote_checkpoint(service, root, book_id, state)
                announce("PILOT_STOP_AFTER_VERIFIED_UPLOAD",
                         lesson_id=lid, new_lessons=newly_published,
                         drive_theory_id=report["drive_theory_id"],
                         drive_exercises_id=report["drive_exercises_id"])
                return state
        except Exception as exc:
            state["lessons"][lid]={"status":"BLOCKED","error":str(exc)[:1200],
                                  "blocked_at":datetime.now(timezone.utc).isoformat()}
            remote_checkpoint(service,root,book_id,state)
            announce("BOOK_STOPPED_ON_BLOCKED_LESSON",lesson_id=lid,reason=str(exc)[:800])
            raise
    state["status"]="ALL_CHAPTERS_PUBLISHED_VERIFIED"
    remote_checkpoint(service,root,book_id,state)
    announce("BOOK_DONE",book_id=book_id,done=done,total=len(index["lessons"]))
    return state


def folder_pdf_ids(service, folder_id: str) -> list[str]:
    """Read all direct PDF children of a selected Drive intake folder.

    This never guesses a grade/subject from a filename or claims that a file
    elsewhere on the user's Drive belongs to the production queue.
    """
    ids = []
    token = None
    while True:
        params = {
            "q": f"'{folder_id}' in parents and trashed = false and mimeType = 'application/pdf'",
            "fields": "nextPageToken,files(id,name,mimeType)",
            "pageSize": 1000,
        }
        if token:
            params["pageToken"] = token
        response = service.files().list(**params).execute()
        for row in response.get("files", []):
            if row.get("id") and row.get("mimeType") == "application/pdf":
                ids.append(row["id"])
        token = response.get("nextPageToken")
        if not token:
            return list(dict.fromkeys(ids))


def run_folder(folder_id: str, *, grade: str = "", subject: str = "",
               language: str = "", branch: str = "",
               index_only: bool = False, watch: bool = False,
               poll_seconds: int = 300) -> dict:
    """One folder = a clearly classified collection of source PDFs.

    Use --grade/subject/language for any new, unregistered PDFs in this
    intake folder. Already registered books keep their manifest classification.
    """
    if poll_seconds < 60:
        raise RuntimeError("WATCH_POLL_INTERVAL_TOO_SHORT: minimum 60 seconds")
    service = factory.get_drive_service()
    last_report = {"status": "NO_PDFS_FOUND", "books": []}
    retry_not_before = {}
    while True:
        ids = folder_pdf_ids(service, folder_id)
        report = {"status": "FOLDER_SCAN_COMPLETE", "source_folder_id": folder_id,
                  "pdf_count": len(ids), "books": []}
        for book_id in ids:
            if watch and time.monotonic() < retry_not_before.get(book_id, 0):
                report["books"].append({"book_id": book_id,
                                        "status": "WAITING_AFTER_FAILURE"})
                continue
            try:
                result = run(book_id, index_only=index_only,
                             publish=not index_only, grade=grade,
                             subject=subject, language=language, branch=branch)
                report["books"].append({"book_id": book_id,
                                        "status": result["status"]})
            except Exception as exc:
                report["books"].append({"book_id": book_id,
                                        "status": "BLOCKED", "reason": str(exc)[:600]})
                announce("BOOK_BLOCKED", book_id=book_id, error=str(exc)[:600])
                retry_not_before[book_id] = time.monotonic() + 3600
                if not watch:
                    # No false success exit code when one-shot production fails.
                    raise
        announce("FOLDER_SCAN_STATUS", **report)
        last_report = report
        if not watch:
            return report
        time.sleep(poll_seconds)


def main():
    ap=argparse.ArgumentParser(description="NABIL real TOC to final-Drive one-book production")
    source=ap.add_mutually_exclusive_group(required=True)
    source.add_argument("--book-id",help="One original Drive PDF ID")
    source.add_argument("--source-folder-id",help="Drive folder containing original PDF books")
    ap.add_argument("--grade",default="",help="Required for new books, e.g. 7")
    ap.add_argument("--subject",default="",help="Required for new books, e.g. physics")
    ap.add_argument("--language",default="",help="Required for new books: en/fr")
    ap.add_argument("--branch",default="",help="Optional secondary stream")
    ap.add_argument("--index-only",action="store_true",help="Inspect and persist true source TOC without generating or uploading lessons")
    ap.add_argument("--max-new-lessons",type=int,default=0,
                    help="Stop after exactly N newly published verified lessons (1 for first-lesson pilot; 0 full book)")
    ap.add_argument("--watch",action="store_true",help="Continuously scan intake folder for newly uploaded PDF books")
    ap.add_argument("--poll-seconds",type=int,default=300,help="Folder watch interval (minimum 60s)")
    args=ap.parse_args()
    if args.watch and not args.source_folder_id:
        ap.error("--watch requires --source-folder-id")
    if args.max_new_lessons < 0:
        ap.error("--max-new-lessons cannot be negative")
    if args.source_folder_id and args.max_new_lessons:
        ap.error("--max-new-lessons requires --book-id, not --source-folder-id")
    if args.index_only and args.max_new_lessons:
        ap.error("--index-only cannot generate lessons")
    if args.source_folder_id:
        result=run_folder(args.source_folder_id,index_only=args.index_only,
                          grade=args.grade,subject=args.subject,
                          language=args.language,branch=args.branch,
                          watch=args.watch,poll_seconds=args.poll_seconds)
    else:
        result=run(args.book_id,index_only=args.index_only,publish=not args.index_only,
                   grade=args.grade,subject=args.subject,
                   language=args.language,branch=args.branch,
                   max_new_lessons=args.max_new_lessons)
    announce("FINAL_STATUS",status=result["status"])

if __name__=="__main__":
    main()