from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests

try:
    import fitz  # PyMuPDF
except Exception:
    fitz = None

CRDP_BASE = "https://www.crdp.org"
BOOKS_PAGE = "https://www.crdp.org/books-pdf"
CURRICULUM_PAGE = "https://www.crdp.org/curriculum"
LEGACY_CURRICULUM = "https://www.crdp.org/curriculum1/173"

ALLOWED_HOSTS = {"crdp.org", "www.crdp.org", "212.36.216.179"}

GRADES = [
    "الروضة الأولى","الروضة الثانية","الروضة الثالثة",
    "الصف الأول","الصف الثاني","الصف الثالث","الصف الرابع","الصف الخامس","الصف السادس",
    "الصف السابع","الصف الثامن","الصف التاسع",
    "الأول ثانوي",
    "الثاني ثانوي - العلوم","الثاني ثانوي - الإنسانيات",
    "الثالث ثانوي - علوم الحياة","الثالث ثانوي - العلوم العامة",
    "الثالث ثانوي - الاجتماع والاقتصاد","الثالث ثانوي - الآداب والإنسانيات",
]

SUBJECTS = [
    "الروضة",
    "اللغة العربية","اللغة الفرنسية","اللغة الإنجليزية",
    "الرياضيات","علوم","الفيزياء","الكيمياء","علوم الحياة",
    "التربية الوطنية والتنشئة المدنية","التاريخ","الجغرافيا",
    "علم الاجتماع","علم الاقتصاد","الفلسفة والحضارات",
]

LANGUAGES = ["العربية", "English", "Français"]

GRADE_ALIASES = {
    "الروضة الأولى":"الروضة الأولى",
    "الروضة الثانية":"الروضة الثانية",
    "الروضة الثالثة":"الروضة الثالثة",
    "السنة الأولى":"الصف الأول",
    "السنة الثانية":"الصف الثاني",
    "السنة الثالثة":"الصف الثالث",
    "السنة الرابعة":"الصف الرابع",
    "السنة الخامسة":"الصف الخامس",
    "السنة السادسة":"الصف السادس",
    "السنة السابعة":"الصف السابع",
    "السنة الثامنة":"الصف الثامن",
    "السنة التاسعة":"الصف التاسع",
    "التعليم الثانوي - السنة الأولى":"الأول ثانوي",
    "السنة الثانية - فرع العلوم":"الثاني ثانوي - العلوم",
    "السنة الثانية - فرع الإنسانيات":"الثاني ثانوي - الإنسانيات",
    "السنة الثالثة - فرع علوم الحياة":"الثالث ثانوي - علوم الحياة",
    "السنة الثالثة - فرع العلوم العامة":"الثالث ثانوي - العلوم العامة",
    "السنة الثالثة - فرع الاجتماع والاقتصاد":"الثالث ثانوي - الاجتماع والاقتصاد",
    "السنة الثالثة - فرع الآداب والإنسانيات":"الثالث ثانوي - الآداب والإنسانيات",
}

SUBJECT_ALIASES = {
    "الروضة":"الروضة", "kindergarten":"الروضة",
    "رياضيات":"الرياضيات", "math":"الرياضيات",
    "عربي":"اللغة العربية", "العربية":"اللغة العربية", "arabic":"اللغة العربية",
    "فرنسي":"اللغة الفرنسية", "الفرنسية":"اللغة الفرنسية", "french":"اللغة الفرنسية", "français":"اللغة الفرنسية",
    "انكليزي":"اللغة الإنجليزية", "إنكليزي":"اللغة الإنجليزية", "الإنكليزية":"اللغة الإنجليزية", "english":"اللغة الإنجليزية",
    "علوم الحياة":"علوم الحياة", "life science":"علوم الحياة", "biology":"علوم الحياة",
    "فيزياء":"الفيزياء", "physics":"الفيزياء",
    "كيمياء":"الكيمياء", "chemistry":"الكيمياء",
    "علوم":"علوم", "science":"علوم",
    "تربية وطنية":"التربية الوطنية والتنشئة المدنية", "مدنية":"التربية الوطنية والتنشئة المدنية",
    "تاريخ":"التاريخ", "history":"التاريخ",
    "جغرافيا":"الجغرافيا", "geography":"الجغرافيا",
    "اجتماع":"علم الاجتماع", "sociology":"علم الاجتماع",
    "اقتصاد":"علم الاقتصاد", "economics":"علم الاقتصاد",
    "فلسفة":"الفلسفة والحضارات", "philosophy":"الفلسفة والحضارات",
}

LANG_HINTS = {
    "english": "English", "انكليزي": "English", "إنكليزي": "English",
    "français": "Français", "francais": "Français", "فرنسي": "Français",
    "arabic": "العربية", "عربي": "العربية", "العربية": "العربية",
}

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self._href = None
        self._text = []
    def handle_starttag(self, tag, attrs):
        if tag.lower() == "a":
            self._href = dict(attrs).get("href")
            self._text = []
    def handle_data(self, data):
        if self._href is not None:
            self._text.append(data)
    def handle_endtag(self, tag):
        if tag.lower() == "a" and self._href is not None:
            text = " ".join("".join(self._text).split())
            self.links.append((text, self._href))
            self._href = None
            self._text = []

def allowed(url: str) -> bool:
    return (urlparse(url).hostname or "").lower() in ALLOWED_HOSTS

def get(url: str):
    if not allowed(url):
        raise RuntimeError(f"Refusing non-CRDP host: {url}")
    r = requests.get(url, timeout=60, headers={"User-Agent":"NABIL-AI-CRDP-Sync/3.0"})
    r.raise_for_status()
    return r

def html_links(url: str):
    p = LinkParser()
    p.feed(get(url).text)
    out = []
    for text, href in p.links:
        if not href:
            continue
        full = urljoin(url, href)
        if allowed(full):
            out.append((text, full))
    return out

def normalize_space(s: str) -> str:
    return " ".join(str(s or "").replace("\u00a0", " ").split()).strip()

def detect_grade(text: str):
    s = normalize_space(text)
    for raw, canon in GRADE_ALIASES.items():
        if raw in s:
            return canon
    return None

def detect_subject(text: str):
    s = normalize_space(text).lower()
    for raw, canon in SUBJECT_ALIASES.items():
        if raw.lower() in s:
            return canon
    return None

def detect_language(text: str):
    s = normalize_space(text).lower()
    for raw, canon in LANG_HINTS.items():
        if raw.lower() in s:
            return canon
    return None

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def safe_name(s: str) -> str:
    return re.sub(r"[^0-9A-Za-z\u0600-\u06FF._-]+", "_", s).strip("_")[:120] or "source"

def pdf_text_and_links(path: Path):
    if fitz is None:
        return "", []
    doc = fitz.open(path)
    text = []
    links = []
    for page_no, page in enumerate(doc, start=1):
        text.append(page.get_text("text"))
        for lk in page.get_links():
            uri = lk.get("uri")
            if uri and allowed(uri):
                links.append({"url": uri, "source_page": page_no})
    return "\n".join(text), links

def conservative_toc(text: str):
    """
    Extract only titles that look like explicit table-of-contents rows or numbered
    chapter/unit headings. Anything uncertain remains needs-review.
    """
    out = []
    seen = set()

    for raw in text.splitlines():
        line = normalize_space(raw)
        if not 3 <= len(line) <= 180:
            continue

        page_match = re.match(r"^(.*?)(?:\.{2,}|\s{2,})(\d{1,3})$", line)
        unit_match = re.match(
            r"^(?:Chapter|Chapitre|Unit|Unité|الوحدة|الفصل|Lesson|Leçon|درس)\s*([0-9IVXLC\u0660-\u0669]+)?[:.\- ]+(.+)$",
            line,
            re.I,
        )

        if page_match:
            title = normalize_space(page_match.group(1)).strip(" .:-")
            page = int(page_match.group(2))
        elif unit_match:
            title = normalize_space(unit_match.group(2)).strip(" .:-")
            page = None
        else:
            continue

        key = title.casefold()
        if len(title) < 3 or key in seen:
            continue
        seen.add(key)

        out.append({
            "title": title,
            "page": page,
            "verification_status": "source-extracted-needs-review",
        })

    return out

def empty_master():
    return {
        "schema_version":"3.0",
        "authority":"Centre for Educational Research and Development (CRDP) Lebanon",
        "generated_at":datetime.now(timezone.utc).isoformat(),
        "scope":{"grades":GRADES,"subjects":SUBJECTS,"languages":LANGUAGES},
        "policy":{
            "all_grades":True,
            "all_subjects":True,
            "no_grade_specific_hardcoding":True,
            "never_invent_lesson_titles":True,
            "preserve_official_order":True,
            "publish_only_verified_lessons":True,
        },
        "catalog":{
            grade:{
                "_status":"awaiting_official_sync",
                "subjects":{}
            } for grade in GRADES
        },
        "sources":[],
        "textbooks":[],
    }

def put_book(master, grade, subject, language, book_record):
    if not grade or not subject:
        return
    grade_node = master["catalog"].setdefault(grade, {"_status":"awaiting_official_sync","subjects":{}})
    subj = grade_node["subjects"].setdefault(subject, {"languages":{}})
    lang = language or "unspecified"
    lang_node = subj["languages"].setdefault(lang, {"books":[]})
    lang_node["books"].append(book_record)
    grade_node["_status"] = "partially_synced"

def main(dest="app/static/crdp_official", output="app/static/crdp_master_curriculum_index.json"):
    root = Path(dest)
    pdfdir = root / "pdf"
    txtdir = root / "text"
    pdfdir.mkdir(parents=True, exist_ok=True)
    txtdir.mkdir(parents=True, exist_ok=True)

    master = empty_master()
    discovered = []

    # A) Annual curriculum + books pages: discover official PDFs for every subject/grade.
    for landing, kind in ((CURRICULUM_PAGE, "curriculum"), (BOOKS_PAGE, "book_list"), (LEGACY_CURRICULUM, "legacy_curriculum")):
        try:
            for label, url in html_links(landing):
                if ".pdf" not in url.lower():
                    continue
                discovered.append({
                    "kind":kind,
                    "label":label,
                    "url":url,
                    "grade":detect_grade(label + " " + url),
                    "subject":detect_subject(label + " " + url),
                    "language":detect_language(label + " " + url),
                })
        except Exception as exc:
            master["sources"].append({"landing":landing,"error":str(exc)})

    # De-duplicate exact PDFs.
    unique = []
    seen = set()
    for item in discovered:
        if item["url"] in seen:
            continue
        seen.add(item["url"])
        unique.append(item)

    # B) Download source PDFs, keep text and embedded CRDP textbook links.
    embedded = []
    for idx, item in enumerate(unique, start=1):
        rec = dict(item)
        try:
            data = get(item["url"]).content
            name = f"{idx:04d}_{safe_name(item['label'] or Path(urlparse(item['url']).path).name)}.pdf"
            path = pdfdir / name
            path.write_bytes(data)
            text, links = pdf_text_and_links(path)
            tpath = txtdir / (path.stem + ".txt")
            tpath.write_text(text, encoding="utf-8")

            rec.update({
                "sha256":sha256(data),
                "local_pdf":str(path),
                "text_file":str(tpath),
                "toc_candidates":conservative_toc(text),
            })

            for lk in links:
                embedded.append({
                    "grade":item.get("grade"),
                    "subject":item.get("subject"),
                    "language":item.get("language"),
                    "discovered_from":item["url"],
                    **lk,
                })
        except Exception as exc:
            rec["error"] = str(exc)
        master["sources"].append(rec)

    # C) Download every actual textbook linked from official CRDP PDFs.
    seen_books = set()
    for idx, item in enumerate(embedded, start=1):
        url = item["url"]
        if url in seen_books:
            continue
        seen_books.add(url)

        book = dict(item)
        try:
            data = get(url).content
            if not data.startswith(b"%PDF"):
                continue

            path = pdfdir / f"book_{idx:05d}_{safe_name(Path(urlparse(url).path).name)}.pdf"
            path.write_bytes(data)
            text, _ = pdf_text_and_links(path)
            tpath = txtdir / (path.stem + ".txt")
            tpath.write_text(text, encoding="utf-8")

            book.update({
                "sha256":sha256(data),
                "local_pdf":str(path),
                "text_file":str(tpath),
                "lessons":conservative_toc(text),
                "verification_status":"official-crdp-book-source",
            })

            # Re-detect from the textbook itself when the book-list label was too generic.
            sample = text[:12000]
            grade = book.get("grade") or detect_grade(sample)
            subject = book.get("subject") or detect_subject(sample)
            language = book.get("language") or detect_language(sample)
            book["grade"] = grade
            book["subject"] = subject
            book["language"] = language

            put_book(master, grade, subject, language, book)
        except Exception as exc:
            book["error"] = str(exc)

        master["textbooks"].append(book)

    # D) Never silently claim complete coverage.
    for grade in GRADES:
        node = master["catalog"][grade]
        if node["subjects"]:
            node["_status"] = "partially_synced"
        else:
            node["_status"] = "awaiting_official_sync"

    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(master, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "ok":True,
        "source_pdfs":len(master["sources"]),
        "textbooks":len(master["textbooks"]),
        "grades_with_data":sum(bool(master["catalog"][g]["subjects"]) for g in GRADES),
        "output":str(out),
    }, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    dest = sys.argv[1] if len(sys.argv) > 1 else "app/static/crdp_official"
    output = sys.argv[2] if len(sys.argv) > 2 else "app/static/crdp_master_curriculum_index.json"
    raise SystemExit(main(dest, output))
