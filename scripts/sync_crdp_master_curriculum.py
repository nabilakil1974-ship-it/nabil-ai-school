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


ANNUAL_PAGE = (
    "https://www.crdp.org/curriculum/"
    "%D8%A7%D9%84%D9%85%D9%86%D9%87%D8%AC-%D8%A7%D9%84%D8%AA%D8%B9%D9%84%D9%8A%D9%85%D9%8A-"
    "%D9%84%D9%84%D8%B9%D8%A7%D9%85-%D9%A2%D9%A0%D9%A2%D9%A5-%D9%A2%D9%A0%D9%A2%D9%A6%D8%8C-"
    "%D9%88%D8%B2%D8%A7%D8%B1%D8%A9-%D8%A7%D9%84%D8%AA%D8%B1%D8%A8%D9%8A%D8%A9-"
    "%D9%88%D8%A7%D9%84%D8%AA%D8%B9%D9%84%D9%8A%D9%85-%D8%A7%D9%84%D8%B9%D8%A7%D9%84%D9%8A-"
    "%D8%A7%D9%84%D9%85%D8%B1%D9%83%D8%B2-%D8%A7%D9%84%D8%AA%D8%B1%D8%A8%D9%88%D9%8A-"
    "%D9%84%D9%84%D8%A8%D8%AD%D9%88%D8%AB"
)
BOOKS_PAGE = "https://www.crdp.org/books-pdf"

ALLOWED_HOSTS = {
    "crdp.org",
    "www.crdp.org",
    "ns1.crdp.org",
    "ns2.crdp.org",
    "store.crdp.org",
    "212.36.216.179",
}

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

# IMPORTANT: longest / most specific aliases are checked FIRST.
GRADE_ALIASES = [
    ("التعليم الثانوي - السنة الثالثة - فرع الاجتماع والاقتصاد", "الثالث ثانوي - الاجتماع والاقتصاد"),
    ("التعليم الثانوي - السنة الثالثة - فرع الآداب والإنسانيات", "الثالث ثانوي - الآداب والإنسانيات"),
    ("التعليم الثانوي - السنة الثالثة - فرع علوم الحياة", "الثالث ثانوي - علوم الحياة"),
    ("التعليم الثانوي - السنة الثالثة - فرع العلوم العامة", "الثالث ثانوي - العلوم العامة"),
    ("السنة الثالثة - فرع الاجتماع والاقتصاد", "الثالث ثانوي - الاجتماع والاقتصاد"),
    ("السنة الثالثة - فرع الآداب والإنسانيات", "الثالث ثانوي - الآداب والإنسانيات"),
    ("السنة الثالثة - فرع علوم الحياة", "الثالث ثانوي - علوم الحياة"),
    ("السنة الثالثة - فرع العلوم العامة", "الثالث ثانوي - العلوم العامة"),
    ("التعليم الثانوي - السنة الثانية - فرع الإنسانيات", "الثاني ثانوي - الإنسانيات"),
    ("التعليم الثانوي - السنة الثانية - فرع العلوم", "الثاني ثانوي - العلوم"),
    ("السنة الثانية - فرع الإنسانيات", "الثاني ثانوي - الإنسانيات"),
    ("السنة الثانية - فرع العلوم", "الثاني ثانوي - العلوم"),
    ("التعليم الثانوي - السنة الأولى", "الأول ثانوي"),
    ("الثالث ثانوي", "الثالث ثانوي"),
    ("الثاني ثانوي", "الثاني ثانوي"),
    ("الأول ثانوي", "الأول ثانوي"),
    ("الروضة الثالثة", "الروضة الثالثة"),
    ("الروضة الثانية", "الروضة الثانية"),
    ("الروضة الأولى", "الروضة الأولى"),
    ("السنة التاسعة", "الصف التاسع"),
    ("السنة الثامنة", "الصف الثامن"),
    ("السنة السابعة", "الصف السابع"),
    ("السنة السادسة", "الصف السادس"),
    ("السنة الخامسة", "الصف الخامس"),
    ("السنة الرابعة", "الصف الرابع"),
    ("السنة الثالثة", "الصف الثالث"),
    ("السنة الثانية", "الصف الثاني"),
    ("السنة الأولى", "الصف الأول"),
    ("الصف التاسع", "الصف التاسع"),
    ("الصف الثامن", "الصف الثامن"),
    ("الصف السابع", "الصف السابع"),
    ("الصف السادس", "الصف السادس"),
    ("الصف الخامس", "الصف الخامس"),
    ("الصف الرابع", "الصف الرابع"),
    ("الصف الثالث", "الصف الثالث"),
    ("الصف الثاني", "الصف الثاني"),
    ("الصف الأول", "الصف الأول"),
]

SUBJECT_ALIASES = [
    ("التربية الوطنية والتنشئة المدنية","التربية الوطنية والتنشئة المدنية"),
    ("اللغة الانكليزية","اللغة الإنجليزية"),
    ("اللغة الإنكليزية","اللغة الإنجليزية"),
    ("اللغة الإنجليزية","اللغة الإنجليزية"),
    ("اللغة الفرنسية","اللغة الفرنسية"),
    ("اللغة العربية","اللغة العربية"),
    ("علوم الحياة","علوم الحياة"),
    ("علم الاجتماع","علم الاجتماع"),
    ("علم الاقتصاد","علم الاقتصاد"),
    ("الفلسفة","الفلسفة والحضارات"),
    ("الرياضيات","الرياضيات"),
    ("رياضيات","الرياضيات"),
    ("math","الرياضيات"),
    ("physics","الفيزياء"),
    ("فيزياء","الفيزياء"),
    ("chemistry","الكيمياء"),
    ("كيمياء","الكيمياء"),
    ("life science","علوم الحياة"),
    ("biology","علوم الحياة"),
    ("التاريخ","التاريخ"),
    ("history","التاريخ"),
    ("الجغرافيا","الجغرافيا"),
    ("geography","الجغرافيا"),
    ("العلوم","علوم"),
    ("science","علوم"),
    ("الروضة","الروضة"),
    ("kindergarten","الروضة"),
]

LANGUAGE_MARKERS = [
    ("Content Details", "English"),
    ("National Textbook", "English"),
    ("Détails du contenu", "Français"),
    ("Livre National", "Français"),
]


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.href = None
        self.buf = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "a":
            self.href = dict(attrs).get("href")
            self.buf = []

    def handle_data(self, data):
        if self.href is not None:
            self.buf.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "a" and self.href is not None:
            self.links.append((" ".join("".join(self.buf).split()), self.href))
            self.href = None
            self.buf = []


def norm(value: str) -> str:
    return " ".join(str(value or "").replace("\u00a0", " ").split()).strip()


def allowed(url: str) -> bool:
    return (urlparse(url).hostname or "").lower() in ALLOWED_HOSTS


def get(url: str):
    if not allowed(url):
        raise RuntimeError(f"Refusing non-CRDP host: {url}")
    r = requests.get(
        url,
        timeout=75,
        headers={"User-Agent": "NABIL-AI-CRDP-Sync/4.0"},
        allow_redirects=True,
    )
    r.raise_for_status()
    return r


def html_links(url: str):
    p = LinkParser()
    p.feed(get(url).text)
    out = []
    for label, href in p.links:
        if not href:
            continue
        full = urljoin(url, href)
        if allowed(full):
            out.append((norm(label), full))
    return out


def detect_grade(text: str):
    s = norm(text)
    for raw, canon in GRADE_ALIASES:
        if raw in s:
            return canon
    return None


def detect_subject(text: str):
    s = norm(text).lower()
    for raw, canon in SUBJECT_ALIASES:
        if raw.lower() in s:
            return canon
    return None


def detect_language(text: str):
    for marker, language in LANGUAGE_MARKERS:
        if marker.lower() in text.lower():
            return language
    # Arabic tables / prose are the fallback when Arabic letters dominate.
    ar = len(re.findall(r"[\u0600-\u06FF]", text))
    lat = len(re.findall(r"[A-Za-zÀ-ÿ]", text))
    if ar > lat:
        return "العربية"
    return None


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe(s: str) -> str:
    return re.sub(r"[^0-9A-Za-z\u0600-\u06FF._-]+", "_", s).strip("_")[:110] or "source"


def new_master():
    return {
        "schema_version": "4.0",
        "authority": "Centre for Educational Research and Development (CRDP) Lebanon",
        "academic_year": "2025-2026",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": {"grades": GRADES, "subjects": SUBJECTS, "languages": ["العربية","English","Français"]},
        "policy": {
            "all_grades": True,
            "all_subjects": True,
            "never_invent_lesson_titles": True,
            "preserve_official_order": True,
            "publish_only_source_traced_lessons": True,
        },
        "catalog": {
            g: {"_status": "awaiting_official_sync", "subjects": {}}
            for g in GRADES
        },
        "annual_sources": [],
        "book_lists": [],
        "errors": [],
    }


def clean_cell(value):
    return norm(str(value or "").replace("\n", " "))


def looks_like_title(value: str) -> bool:
    s = clean_cell(value)
    if len(s) < 3 or len(s) > 180:
        return False
    if re.fullmatch(r"[\d\s✓✔./-]+", s):
        return False
    if s.lower() in {
        "content","contenu","page","prerequisites","prérequis",
        "number of periods","nombre de périodes","order of chapters",
        "ordre des chapitres","national textbook","livre national",
    }:
        return False
    return True


def numeric(value):
    s = clean_cell(value)
    m = re.fullmatch(r"\d{1,3}", s)
    return int(m.group()) if m else None


def strict_table_lessons(page, grade, subject, language, source_url):
    """
    Extract source-traced lesson titles from official CRDP tables.
    A row is accepted only when it has:
      - a short textual title cell,
      - at least two numeric cells (e.g. chapter/page/order),
      - and the page contains the official textbook table header.
    """
    text = page.get_text("text")
    low = text.lower()
    has_table_header = any(
        x in low for x in (
            "chapter- topic", "chapter-topic", "chapitre-sujet",
            "national textbook", "livre national",
            "الكتاب الوطني", "الكتاب المدرسي"
        )
    )
    if not has_table_header:
        return []

    out = []
    try:
        finder = page.find_tables()
        tables = finder.tables if finder else []
    except Exception:
        tables = []

    for table in tables:
        try:
            rows = table.extract()
        except Exception:
            continue
        for row in rows or []:
            cells = [clean_cell(c) for c in (row or [])]
            nums = [(i, numeric(c)) for i, c in enumerate(cells) if numeric(c) is not None]
            if len(nums) < 2:
                continue

            candidates = [
                (i, c) for i, c in enumerate(cells)
                if looks_like_title(c)
                and not re.match(r"^\d+(?:\.\d+)+\s", c)
                and not re.match(r"^[IVXLC]+\.", c, re.I)
            ]
            if not candidates:
                continue

            # Prefer a concise topic-like cell over long curriculum-detail prose.
            candidates.sort(key=lambda pair: (
                0 if 3 <= len(pair[1]) <= 90 else 1,
                len(pair[1])
            ))
            idx, title = candidates[0]

            # Avoid section bullet lists as lesson titles.
            if title.count(" I.") + title.count(" II.") + title.count(" III.") >= 2:
                continue

            numbers = [n for _, n in nums]
            page_no = next((n for n in numbers if 5 <= n <= 400), None)
            order = numbers[-1] if numbers else None

            out.append({
                "title": title,
                "official_order": order,
                "textbook_page": page_no,
                "source_pdf_page": page.number + 1,
                "source_url": source_url,
                "verification_status": "verified-from-official-table",
            })

    # Stable de-dup preserving first appearance.
    seen = set()
    dedup = []
    for item in out:
        k = item["title"].casefold()
        if k in seen:
            continue
        seen.add(k)
        dedup.append(item)
    return dedup


def add_lessons(master, grade, subject, language, lessons, source_url):
    if not grade or not subject or not lessons:
        return
    gnode = master["catalog"].setdefault(grade, {"_status":"awaiting_official_sync","subjects":{}})
    snode = gnode["subjects"].setdefault(subject, {"languages":{}})
    lnode = snode["languages"].setdefault(language or "unspecified", {"lessons":[]})
    existing = {x.get("title","").casefold() for x in lnode["lessons"]}
    for item in lessons:
        if item["title"].casefold() not in existing:
            lnode["lessons"].append(item)
            existing.add(item["title"].casefold())
    lnode["source_url"] = source_url
    gnode["_status"] = "partially_synced"


def process_annual_pdf(master, rec, pdf_path):
    doc = fitz.open(pdf_path)
    current_grade = None
    subject = rec.get("subject")
    for page in doc:
        text = page.get_text("text")
        page_grade = detect_grade(text)
        if page_grade:
            current_grade = page_grade
        page_subject = detect_subject(text) or subject
        language = detect_language(text)
        lessons = strict_table_lessons(
            page, current_grade, page_subject, language, rec["url"]
        )
        add_lessons(
            master, current_grade, page_subject, language, lessons, rec["url"]
        )


def main(dest="app/static/crdp_official",
         output="app/static/crdp_master_curriculum_index.json"):
    if fitz is None:
        raise RuntimeError("PyMuPDF is required: pip install pymupdf")

    root = Path(dest)
    pdf_dir = root / "pdf"
    pdf_dir.mkdir(parents=True, exist_ok=True)

    master = new_master()

    # 1) The authoritative 2025-2026 subject documents.
    annual_links = html_links(ANNUAL_PAGE)
    annual_pdfs = []
    for label, url in annual_links:
        if ".pdf" not in url.lower():
            continue
        subject = detect_subject(label + " " + url)
        annual_pdfs.append((label, url, subject))

    seen = set()
    annual_pdfs = [x for x in annual_pdfs if not (x[1] in seen or seen.add(x[1]))]

    for idx, (label, url, subject) in enumerate(annual_pdfs, 1):
        rec = {"label":label, "url":url, "subject":subject}
        try:
            r = get(url)
            data = r.content
            path = pdf_dir / f"annual_{idx:02d}_{safe(label or Path(urlparse(url).path).name)}.pdf"
            path.write_bytes(data)
            rec["sha256"] = sha256(data)
            rec["local_pdf"] = str(path)
            process_annual_pdf(master, rec, path)
        except Exception as exc:
            rec["error"] = str(exc)
            master["errors"].append({"url":url, "error":str(exc)})
        master["annual_sources"].append(rec)

    # 2) Keep the official grade/branch book-list PDFs as source metadata.
    try:
        for label, url in html_links(BOOKS_PAGE):
            if ".pdf" not in url.lower():
                continue
            master["book_lists"].append({
                "label": label,
                "url": url,
                "grade": detect_grade(label),
            })
    except Exception as exc:
        master["errors"].append({"url":BOOKS_PAGE, "error":str(exc)})

    # 3) Coverage summary. Never claim full coverage silently.
    grades_with_data = 0
    subject_grade_pairs = 0
    lesson_count = 0
    for grade, gnode in master["catalog"].items():
        subjects = gnode.get("subjects", {})
        if subjects:
            grades_with_data += 1
        subject_grade_pairs += len(subjects)
        for snode in subjects.values():
            for lnode in snode.get("languages", {}).values():
                lesson_count += len(lnode.get("lessons", []))

    master["coverage"] = {
        "grades_total": len(GRADES),
        "grades_with_data": grades_with_data,
        "subject_grade_pairs": subject_grade_pairs,
        "verified_lessons": lesson_count,
        "annual_subject_pdfs": len(master["annual_sources"]),
        "book_list_pdfs": len(master["book_lists"]),
        "complete": grades_with_data == len(GRADES) and lesson_count > 0,
    }

    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(master, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(master["coverage"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    dest = sys.argv[1] if len(sys.argv) > 1 else "app/static/crdp_official"
    output = sys.argv[2] if len(sys.argv) > 2 else "app/static/crdp_master_curriculum_index.json"
    raise SystemExit(main(dest, output))
