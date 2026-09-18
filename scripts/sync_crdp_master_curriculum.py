from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse

import fitz
import requests


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
    "crdp.org", "www.crdp.org", "ns1.crdp.org", "ns2.crdp.org",
    "store.crdp.org", "212.36.216.179"
}

GRADES = [
    "الصف الأول", "الصف الثاني", "الصف الثالث", "الصف الرابع", "الصف الخامس", "الصف السادس",
    "الصف السابع", "الصف الثامن", "الصف التاسع",
    "الأول ثانوي",
    "الثاني ثانوي - العلوم", "الثاني ثانوي - الإنسانيات",
    "الثالث ثانوي - علوم الحياة", "الثالث ثانوي - العلوم العامة",
    "الثالث ثانوي - الاجتماع والاقتصاد", "الثالث ثانوي - الآداب والإنسانيات",
]

SUBJECTS = [
    "اللغة العربية", "اللغة الفرنسية", "اللغة الإنجليزية",
    "الرياضيات", "علوم", "الفيزياء", "الكيمياء", "علوم الحياة",
    "التربية الوطنية والتنشئة المدنية", "الجغرافيا",
    
]

SUBJECT_ALIASES = [
    ("مادة اللغة العربية وآدابها", "اللغة العربية"),
    ("مادة اللغة الفرنسية وآدابها", "اللغة الفرنسية"),
    ("مادة اللغة الانكليزية وآدابها", "اللغة الإنجليزية"),
    ("مادة اللغة الإنجليزية وآدابها", "اللغة الإنجليزية"),
    ("مادة التربية الوطنية والتنشئة المدنية", "التربية الوطنية والتنشئة المدنية"),
    ("مادة علوم الحياة", "علوم الحياة"),
    ("مادة الفيزياء", "الفيزياء"),
    ("مادة الكيمياء", "الكيمياء"),
    ("مادة الرياضيات", "الرياضيات"),
    ("مادة العلوم", "علوم"),
]

BAD_NOTE_PATTERNS = [
    r"\bsuspend\b", r"\bmaintain(?:ed)?\b", r"\bretained\b", r"\bprerequisite",
    r"\brecall(?:ing)?\b", r"\bwithout writing\b", r"\bdo not\b", r"\bnot required\b",
    r"\bomitted\b", r"\bdeleted\b", r"\bpages?\s+\d+\s*(?:and|-)\s*\d+",
    r"معل[ّ]?ق", r"محذوف", r"لا يطلب", r"موقوف", r"يُلغى", r"يلغى",
]

REVERSED_ARABIC_MARKERS = [
    "لسلست", "ةداملا", "ةيميلعتلا", "عقاولا", "شاعملا",
    "اذه يف يهتني", "ة يعماجلا", "تاصاصتخ",
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


def norm(value):
    return " ".join(str(value or "").replace("\u00a0", " ").split()).strip()


def allowed(url):
    return (urlparse(url).hostname or "").lower() in ALLOWED_HOSTS


def get(url):
    if not allowed(url):
        raise RuntimeError(f"Refusing non-CRDP host: {url}")
    r = requests.get(
        url, timeout=75,
        headers={"User-Agent": "NABIL-AI-CRDP-Sync/7.0"},
        allow_redirects=True,
    )
    r.raise_for_status()
    return r


def html_links(url):
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


def detect_subject_from_link(label, url):
    hay = f"{label} {url}"
    for raw, canon in SUBJECT_ALIASES:
        if raw in hay:
            return canon
    return None


def grade_from_text(text):
    """
    Strong grade detection for headers AND grade-marker table rows.
    Kindergarten is intentionally excluded for now.
    No cross-page inheritance.
    """
    s = norm(text).lower()

    # Kindergarten is intentionally postponed and excluded from this phase.
    if re.search(r"(?:الروضة|مرحلة الروضة|\bkg\s*[123]\b|\bps\s*[123]\b)", s, re.I):
        return None

    rules = [
        # KG
        (r"(?:الروضة|مرحلة الروضة).*(?:السنة\s*)?الأولى|(?:kg|ps)\s*1\b", "الروضة الأولى"),
        (r"(?:الروضة|مرحلة الروضة).*(?:السنة\s*)?الثانية|(?:kg|ps)\s*2\b", "الروضة الثانية"),
        (r"(?:الروضة|مرحلة الروضة).*(?:السنة\s*)?الثالثة|(?:kg|ps)\s*3\b", "الروضة الثالثة"),

        # Third secondary branches — Arabic
        (r"(?:الصف\s*)?الثالث\s*ثانوي.*علوم\s*الحياة|السنة\s*الثالثة.*علوم\s*الحياة", "الثالث ثانوي - علوم الحياة"),
        (r"(?:الصف\s*)?الثالث\s*ثانوي.*العلوم\s*العامة|السنة\s*الثالثة.*العلوم\s*العامة", "الثالث ثانوي - العلوم العامة"),
        (r"(?:الصف\s*)?الثالث\s*ثانوي.*(?:اجتماع|الاجتماع).*(?:اقتصاد|الاقتصاد)|السنة\s*الثالثة.*(?:اجتماع|الاجتماع).*(?:اقتصاد|الاقتصاد)", "الثالث ثانوي - الاجتماع والاقتصاد"),
        (r"(?:الصف\s*)?الثالث\s*ثانوي.*(?:آداب|الآداب).*(?:إنسانيات|الإنسانيات)|السنة\s*الثالثة.*(?:آداب|الآداب).*(?:إنسانيات|الإنسانيات)", "الثالث ثانوي - الآداب والإنسانيات"),

        # Third secondary branches — English/French/common abbreviations
        (r"(?:grade\s*12|third\s*secondary|3(?:rd)?\s*secondary|s3).*(?:life\s*sciences?|sciences?\s*de\s*la\s*vie|\bsv\b|\bls\b)", "الثالث ثانوي - علوم الحياة"),
        (r"(?:grade\s*12|third\s*secondary|3(?:rd)?\s*secondary|s3).*(?:general\s*sciences?|sciences?\s*g[ée]n[ée]rales?|\bsg\b|\bgs\b)", "الثالث ثانوي - العلوم العامة"),
        (r"(?:grade\s*12|third\s*secondary|3(?:rd)?\s*secondary|s3).*(?:socio.?economics?|economics?.*sociology|\bse\b)", "الثالث ثانوي - الاجتماع والاقتصاد"),
        (r"(?:grade\s*12|third\s*secondary|3(?:rd)?\s*secondary|s3).*(?:literature.*humanities|humanities.*literature|\blh\b)", "الثالث ثانوي - الآداب والإنسانيات"),

        # Second secondary
        (r"(?:الصف\s*)?الثاني\s*ثانوي.*(?:فرع\s*)?العلوم|السنة\s*الثانية.*فرع\s*العلوم", "الثاني ثانوي - العلوم"),
        (r"(?:الصف\s*)?الثاني\s*ثانوي.*(?:إنسانيات|الإنسانيات)|السنة\s*الثانية.*(?:إنسانيات|الإنسانيات)", "الثاني ثانوي - الإنسانيات"),
        (r"(?:grade\s*11|second\s*secondary|2(?:nd)?\s*secondary|s2).*(?:science|scientifique)", "الثاني ثانوي - العلوم"),
        (r"(?:grade\s*11|second\s*secondary|2(?:nd)?\s*secondary|s2).*(?:humanit|litt[ée]raire)", "الثاني ثانوي - الإنسانيات"),

        # First secondary
        (r"(?:الصف\s*)?الأول\s*ثانوي|التعليم\s*الثانوي.*السنة\s*الأولى|\bgrade\s*10\b|first\s*secondary|1(?:st)?\s*secondary|\bs1\b", "الأول ثانوي"),
    ]
    for pat, grade in rules:
        if re.search(pat, s, re.I):
            return grade

    basic_words = {
        "الأولى": "الصف الأول", "الثانية": "الصف الثاني", "الثالثة": "الصف الثالث",
        "الرابعة": "الصف الرابع", "الخامسة": "الصف الخامس", "السادسة": "الصف السادس",
        "السابعة": "الصف السابع", "الثامنة": "الصف الثامن", "التاسعة": "الصف التاسع",
    }
    for word, grade in basic_words.items():
        if re.search(rf"(?:الصف|السنة)\s+{word}\s*(?:الأساسي|الاساسي)?\b", s):
            return grade

    m = re.search(r"\b(?:grade|eb)\s*([1-9])\b", s, re.I)
    if m:
        names = ["", "الأول", "الثاني", "الثالث", "الرابع", "الخامس",
                 "السادس", "السابع", "الثامن", "التاسع"]
        return f"الصف {names[int(m.group(1))]}"

    return None


def detect_language(text):
    low = text.lower()
    if "national textbook" in low or "number of periods" in low:
        return "English"
    if "livre national" in low or "nombre de périodes" in low:
        return "Français"
    ar = len(re.findall(r"[\u0600-\u06FF]", text))
    lat = len(re.findall(r"[A-Za-zÀ-ÿ]", text))
    if ar > lat * 1.2:
        return "العربية"
    return None


def numeric(value):
    s = norm(value)
    return int(s) if re.fullmatch(r"\d{1,3}", s) else None


def bad_title(title, language=None):
    t = norm(title)
    if len(t) < 3 or len(t) > 170:
        return True
    low = t.lower()

    if any(re.search(p, low, re.I) for p in BAD_NOTE_PATTERNS):
        return True
    if any(marker in t for marker in REVERSED_ARABIC_MARKERS):
        return True
    if re.match(r"^ch\.?\s*\d+\b", t, re.I):
        return True
    if re.match(r"^(?:chapter|unit|chapitre|unité)\s*\d+\s*$", t, re.I):
        return True
    if low in {
        "total", "content", "contenu", "page", "pages",
        "important for healthy life", "important for a healthy life",
        "national textbook", "livre national", "number of periods",
        "nombre de périodes", "chapter-topic", "chapter- topic", "chapitre-sujet",
    }:
        return True

    # Language/script mismatch filter.
    ar = len(re.findall(r"[\u0600-\u06FF]", t))
    lat = len(re.findall(r"[A-Za-zÀ-ÿ]", t))
    if language in {"English", "Français"} and ar > lat and ar > 4:
        return True

    return False


def clean_source_title(value):
    t = norm(value)

    # CRDP PDF tables often contain "_" placeholders between wrapped words.
    t = re.sub(r"\s*_+\s*", " ", t)
    t = norm(t)

    # Keep the official lesson title but drop appended administrative notes.
    t = re.split(
        r"\s+(?:Note|Remarque|ملاحظة)\s*[:：]",
        t,
        maxsplit=1,
        flags=re.I,
    )[0].strip()

    return t.rstrip(" -_;:")


def choose_title(cells, language):
    candidates = []
    for c in cells:
        c = clean_source_title(c)
        if not c or numeric(c) is not None or bad_title(c, language):
            continue
        if grade_from_text(c):
            continue
        # Avoid long curriculum objectives/prose.
        if len(c) > 105:
            continue
        # Avoid cells that are mostly punctuation.
        alnum = len(re.findall(r"[\w\u0600-\u06FFÀ-ÿ]", c))
        if alnum < 3:
            continue
        candidates.append(c)

    if not candidates:
        return None

    # Prefer title-like cells: 3–90 chars, not full sentences.
    candidates.sort(key=lambda s: (
        0 if 3 <= len(s) <= 90 else 1,
        1 if s.endswith((".", ":", ";")) else 0,
        len(s),
    ))
    return candidates[0]


def row_lesson(row, grade, subject, language, page_no, source_url):
    cells = [norm(c) for c in (row or [])]
    nums = [numeric(c) for c in cells if numeric(c) is not None]

    # Official tables generally provide order/page/period numeric columns.
    if len(nums) < 2:
        return None

    title = choose_title(cells, language)
    if not title:
        return None

    title_grade = grade_from_text(title)
    if title_grade and title_grade != grade:
        return None

    return {
        "title": title,
        "official_order": nums[-1] if nums else None,
        "textbook_page": next((n for n in nums if 5 <= n <= 450), None),
        "source_pdf_page": page_no,
        "source_url": source_url,
        "source_grade": grade,
        "source_subject": subject,
        "verification_status": "verified-from-official-crdp-table",
    }


def extract_page(page, subject, source_url):
    """
    V7 strategy:
    - Never inherit a grade across pages.
    - A page may have a strong page-local grade.
    - Within ONE table only, a grade-marker row may set table_grade for the
      following rows in that same table. It resets for each new table/page.
    This recovers sparse CRDP layouts without reintroducing cross-grade leakage.
    """
    text = page.get_text("text")
    page_grade = grade_from_text(text[:3000])

    language = detect_language(text)
    low = text.lower()

    table_signal = any(k in low for k in (
        "national textbook", "livre national", "chapter- topic", "chapter-topic",
        "chapitre-sujet", "الكتاب الوطني", "الكتاب المدرسي",
        "عدد الحصص", "عدد الفترات", "المحتوى",
    ))
    if not table_signal:
        return []

    try:
        tables = page.find_tables().tables
    except Exception:
        tables = []

    out = []
    for table in tables:
        try:
            rows = table.extract()
        except Exception:
            continue

        table_grade = page_grade  # resets per table
        for row in rows or []:
            cells = [norm(c) for c in (row or [])]
            row_text = " | ".join(cells)

            row_grade = grade_from_text(row_text)

            if row_grade:
                table_grade = row_grade
                # A pure grade-marker/header row is not a lesson.
                non_numeric = [c for c in cells if c and numeric(c) is None]
                if len(non_numeric) <= 3:
                    continue

            if not table_grade:
                continue

            item = row_lesson(
                row=row,
                grade=table_grade,
                subject=subject,
                language=language,
                page_no=page.number + 1,
                source_url=source_url,
            )
            if item:
                out.append((table_grade, language, item))

    # De-dup within page.
    seen = set()
    dedup = []
    for grade, lang, item in out:
        key = (grade, lang, item["title"].casefold())
        if key in seen:
            continue
        seen.add(key)
        dedup.append((grade, lang, item))
    return dedup


def add(master, grade, subject, language, item, source_url):
    if not grade or not subject or not item:
        return

    # Languages remain available for Grades 1–9, but are intentionally excluded
    # from all secondary branches in this phase.
    secondary = (
        grade == "الأول ثانوي"
        or grade.startswith("الثاني ثانوي")
        or grade.startswith("الثالث ثانوي")
    )
    if secondary and subject in {"اللغة العربية", "اللغة الفرنسية", "اللغة الإنجليزية"}:
        return

    # Kindergarten entries are accepted only from the official Kindergarten source.
    if grade.startswith("الروضة") and subject != "الروضة":
        return
    g = master["catalog"][grade]
    s = g["subjects"].setdefault(subject, {"languages": {}})
    l = s["languages"].setdefault(
        language or "unspecified",
        {"lessons": [], "source_url": source_url}
    )
    existing = {x["title"].casefold() for x in l["lessons"]}
    if item["title"].casefold() not in existing:
        l["lessons"].append(item)
    g["_status"] = "partially_synced"


def main(dest="app/static/crdp_official",
         output="app/static/crdp_master_curriculum_index.json"):
    root = Path(dest)
    pdfdir = root / "pdf"
    pdfdir.mkdir(parents=True, exist_ok=True)

    master = {
        "schema_version": "11.0",
        "authority": "CRDP Lebanon",
        "academic_year": "2025-2026",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "policy": {
            "all_grades": True,
            "all_subjects": True,
            "never_invent_lesson_titles": True,
            "preserve_official_order": True,
            "reject_instruction_rows": True,
            "reject_language_script_mismatch": True,
            "never_inherit_grade_across_pages": True,
            "allow_grade_state_only_inside_same_table": True,
            "kindergarten_excluded_for_now": True,
            "globally_excluded_subjects": [
                "علم الاجتماع", "علم الاقتصاد", "التاريخ",
                "الجغرافيا", "الفلسفة والحضارات"
            ],
            "secondary_languages_excluded_for_now": [
                "اللغة العربية", "اللغة الفرنسية", "اللغة الإنجليزية"
            ],
            "strip_inline_editorial_notes": True,
            "normalize_pdf_wrap_markers": True,
        },
        "catalog": {
            g: {"_status": "awaiting_official_sync", "subjects": {}}
            for g in GRADES
        },
        "annual_sources": [],
        "book_lists": [],
        "errors": [],
    }

    links = [
        (label, url, detect_subject_from_link(label, url))
        for label, url in html_links(ANNUAL_PAGE)
        if ".pdf" in url.lower()
    ]
    seen_urls = set()
    links = [
        x for x in links
        if not (x[1] in seen_urls or seen_urls.add(x[1]))
    ]

    for i, (label, url, subject) in enumerate(links, 1):
        # Skip subjects intentionally excluded from the current NABIL AI scope.
        if subject not in SUBJECTS:
            continue

        rec = {"label": label, "url": url, "subject": subject}
        try:
            data = get(url).content
            path = pdfdir / f"annual_{i:02d}.pdf"
            path.write_bytes(data)
            rec["sha256"] = hashlib.sha256(data).hexdigest()

            doc = fitz.open(path)
            for page in doc:
                if not subject:
                    continue
                for grade, language, item in extract_page(page, subject, url):
                    add(master, grade, subject, language, item, url)

        except Exception as exc:
            rec["error"] = str(exc)
            master["errors"].append({"url": url, "error": str(exc)})

        master["annual_sources"].append(rec)

    try:
        for label, url in html_links(BOOKS_PAGE):
            if ".pdf" in url.lower():
                master["book_lists"].append({
                    "label": label,
                    "url": url,
                    "grade": grade_from_text(label),
                })
    except Exception as exc:
        master["errors"].append({"url": BOOKS_PAGE, "error": str(exc)})

    lesson_count = 0
    populated_grades = 0
    subject_grade_pairs = 0
    missing_grades = []

    for grade, gnode in master["catalog"].items():
        if gnode["subjects"]:
            populated_grades += 1
        else:
            missing_grades.append(grade)

        subject_grade_pairs += len(gnode["subjects"])
        for snode in gnode["subjects"].values():
            for lnode in snode["languages"].values():
                lesson_count += len(lnode["lessons"])

    master["coverage"] = {
        "grades_total": len(GRADES),
        "grades_with_data": populated_grades,
        "subject_grade_pairs": subject_grade_pairs,
        "verified_lessons": lesson_count,
        "annual_subject_pdfs": len(master["annual_sources"]),
        "book_list_pdfs": len(master["book_lists"]),
        "missing_grades": missing_grades,
        "complete": populated_grades == len(GRADES),
    }

    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(master, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(json.dumps(master["coverage"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(
        sys.argv[1] if len(sys.argv) > 1 else "app/static/crdp_official",
        sys.argv[2] if len(sys.argv) > 2 else "app/static/crdp_master_curriculum_index.json",
    ))
