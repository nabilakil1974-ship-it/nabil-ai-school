from __future__ import annotations
import hashlib, json, re, sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
import requests
import fitz

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
ALLOWED_HOSTS = {"crdp.org","www.crdp.org","ns1.crdp.org","ns2.crdp.org","store.crdp.org","212.36.216.179"}

GRADES = [
 "الروضة الأولى","الروضة الثانية","الروضة الثالثة",
 "الصف الأول","الصف الثاني","الصف الثالث","الصف الرابع","الصف الخامس","الصف السادس",
 "الصف السابع","الصف الثامن","الصف التاسع","الأول ثانوي",
 "الثاني ثانوي - العلوم","الثاني ثانوي - الإنسانيات",
 "الثالث ثانوي - علوم الحياة","الثالث ثانوي - العلوم العامة",
 "الثالث ثانوي - الاجتماع والاقتصاد","الثالث ثانوي - الآداب والإنسانيات"
]
SUBJECTS = ["الروضة","اللغة العربية","اللغة الفرنسية","اللغة الإنجليزية","الرياضيات","علوم","الفيزياء","الكيمياء","علوم الحياة","التربية الوطنية والتنشئة المدنية","التاريخ","الجغرافيا","علم الاجتماع","علم الاقتصاد","الفلسفة والحضارات"]

SUBJECT_ALIASES = [
 ("مادة اللغة العربية وآدابها","اللغة العربية"),
 ("مادة اللغة الفرنسية وآدابها","اللغة الفرنسية"),
 ("مادة اللغة الانكليزية وآدابها","اللغة الإنجليزية"),
 ("مادة اللغة الإنجليزية وآدابها","اللغة الإنجليزية"),
 ("مادة التربية الوطنية والتنشئة المدنية","التربية الوطنية والتنشئة المدنية"),
 ("مادة علم الاجتماع","علم الاجتماع"),("مادة علم الاقتصاد","علم الاقتصاد"),
 ("مادة علوم الحياة","علوم الحياة"),("مادة الفيزياء","الفيزياء"),
 ("مادة الكيمياء","الكيمياء"),("مادة الرياضيات","الرياضيات"),
 ("مادة التاريخ","التاريخ"),("مادة الجغرافيا","الجغرافيا"),
 ("مادة العلوم","علوم"),("مادة الفلسفة","الفلسفة والحضارات"),
 ("منهج الروضة","الروضة"),
]

NOTE_PATTERNS = [
 r"\bsuspend\b", r"\bmaintain(?:ed)?\b", r"\bretained\b", r"\bprerequisite",
 r"\brecall(?:ing)?\b", r"\bwithout writing\b", r"\bdo not\b", r"\bnot required\b",
 r"\bomitted\b", r"\bdeleted\b", r"معل[ّ]?ق", r"محذوف", r"لا يطلب", r"موقوف"
]

class LinkParser(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]; self.href=None; self.buf=[]
    def handle_starttag(self,tag,attrs):
        if tag.lower()=="a": self.href=dict(attrs).get("href"); self.buf=[]
    def handle_data(self,data):
        if self.href is not None: self.buf.append(data)
    def handle_endtag(self,tag):
        if tag.lower()=="a" and self.href is not None:
            self.links.append((" ".join("".join(self.buf).split()),self.href)); self.href=None; self.buf=[]

def norm(s): return " ".join(str(s or "").replace("\u00a0"," ").split()).strip()
def allowed(url): return (urlparse(url).hostname or "").lower() in ALLOWED_HOSTS
def get(url):
    if not allowed(url): raise RuntimeError(f"Refusing non-CRDP host: {url}")
    r=requests.get(url,timeout=75,headers={"User-Agent":"NABIL-AI-CRDP-Sync/6.0"},allow_redirects=True)
    r.raise_for_status()
    return r
def html_links(url):
    p=LinkParser(); p.feed(get(url).text); out=[]
    for label,href in p.links:
        if href:
            full=urljoin(url,href)
            if allowed(full): out.append((norm(label),full))
    return out
def detect_subject_from_link(label,url):
    h=f"{label} {url}"
    for raw,canon in SUBJECT_ALIASES:
        if raw in h: return canon
    return None

def detect_grade_from_page(text):
    """
    STRICT page-local grade detection.
    Never inherit a grade from prior pages.
    """
    h=norm(text[:2500]).lower()

    # Secondary branches first.
    rules = [
      (r"السنة الثالثة.*علوم الحياة", "الثالث ثانوي - علوم الحياة"),
      (r"السنة الثالثة.*العلوم العامة|الثالث.*علوم عامة", "الثالث ثانوي - العلوم العامة"),
      (r"السنة الثالثة.*الاجتماع.*الاقتصاد", "الثالث ثانوي - الاجتماع والاقتصاد"),
      (r"السنة الثالثة.*الآداب.*الإنسانيات", "الثالث ثانوي - الآداب والإنسانيات"),
      (r"السنة الثانية.*فرع العلوم", "الثاني ثانوي - العلوم"),
      (r"السنة الثانية.*الإنسانيات", "الثاني ثانوي - الإنسانيات"),
      (r"التعليم الثانوي.*السنة الأولى|الأول ثانوي", "الأول ثانوي"),
      (r"grade\s*12.*life sciences|3(?:rd)?\s*secondary.*life sciences|s3.*sv", "الثالث ثانوي - علوم الحياة"),
      (r"grade\s*12.*general sciences|3(?:rd)?\s*secondary.*general sciences|s3.*sg", "الثالث ثانوي - العلوم العامة"),
      (r"grade\s*12.*socio.?economics|s3.*se", "الثالث ثانوي - الاجتماع والاقتصاد"),
      (r"grade\s*12.*literature.*humanities|s3.*lh", "الثالث ثانوي - الآداب والإنسانيات"),
      (r"grade\s*11.*science|s2.*science", "الثاني ثانوي - العلوم"),
      (r"grade\s*11.*humanit|s2.*humanit", "الثاني ثانوي - الإنسانيات"),
      (r"grade\s*10|1(?:st)?\s*secondary|\bs1\b", "الأول ثانوي"),
    ]
    for pat,grade in rules:
        if re.search(pat,h,re.I):
            return grade

    # KG.
    if "الروضة" in h:
        if "الثالثة" in h:return "الروضة الثالثة"
        if "الثانية" in h:return "الروضة الثانية"
        if "الأولى" in h:return "الروضة الأولى"

    # Basic grades.
    arabic = {
      "الأولى":"الصف الأول","الثانية":"الصف الثاني","الثالثة":"الصف الثالث",
      "الرابعة":"الصف الرابع","الخامسة":"الصف الخامس","السادسة":"الصف السادس",
      "السابعة":"الصف السابع","الثامنة":"الصف الثامن","التاسعة":"الصف التاسع",
    }
    for word,grade in arabic.items():
        if re.search(rf"(?:الصف|السنة)\s+{word}\b",h):
            return grade

    m=re.search(r"\b(?:grade|eb)\s*([1-9])\b",h,re.I)
    if m:
        names=['','الأول','الثاني','الثالث','الرابع','الخامس','السادس','السابع','الثامن','التاسع']
        return f"الصف {names[int(m.group(1))]}"

    return None

def detect_language(text):
    low=text.lower()
    if "national textbook" in low or "number of periods" in low:return "English"
    if "livre national" in low or "nombre de périodes" in low:return "Français"
    ar=len(re.findall(r"[\u0600-\u06FF]",text)); lat=len(re.findall(r"[A-Za-zÀ-ÿ]",text))
    if ar>lat*1.2:return "العربية"
    return None

def is_note(title):
    low=title.lower()
    return any(re.search(p,low,re.I) for p in NOTE_PATTERNS)

def bad_title(title):
    t=norm(title)
    if len(t)<3 or len(t)>160:return True
    if is_note(t):return True
    if any(x in t for x in ("لسلست","ةداملا","ةيميلعتلا","ةقحللاا")):return True
    if re.match(r"^ch\.?\s*\d+\b",t,re.I):return True
    if re.match(r"^(?:chapter|unit)\s*\d+\s*$",t,re.I):return True
    if t.lower() in {"total","content","contenu","page"}:return True
    return False

def numeric(s):
    s=norm(s)
    return int(s) if re.fullmatch(r"\d{1,3}",s) else None

def page_lessons(page, grade, subject, source_url):
    text=page.get_text("text")
    language=detect_language(text)
    low=text.lower()
    if not any(k in low for k in ("national textbook","livre national","chapter- topic","chapitre-sujet","الكتاب الوطني","الكتاب المدرسي")):
        return language,[]
    try:
        tables=page.find_tables().tables
    except Exception:
        tables=[]
    out=[]
    for table in tables:
        try: rows=table.extract()
        except Exception: continue
        for row in rows or []:
            cells=[norm(c) for c in (row or [])]
            nums=[numeric(c) for c in cells if numeric(c) is not None]
            if len(nums)<2: continue
            candidates=[]
            for c in cells:
                if not c or numeric(c) is not None or bad_title(c): continue
                if len(c)>100: continue
                candidates.append(c)
            if not candidates: continue
            title=min(candidates,key=len)
            if bad_title(title): continue
            out.append({
              "title":title,
              "official_order":nums[-1] if nums else None,
              "textbook_page":next((n for n in nums if 5<=n<=400),None),
              "source_pdf_page":page.number+1,
              "source_url":source_url,
              "source_grade":grade,
              "source_subject":subject,
              "verification_status":"verified-from-official-crdp-table"
            })
    seen=set(); dedup=[]
    for x in out:
        k=x["title"].casefold()
        if k not in seen:
            seen.add(k); dedup.append(x)
    return language,dedup

def add(master,grade,subject,language,lessons,source_url):
    if not grade or not subject or not lessons:return
    g=master["catalog"][grade]
    s=g["subjects"].setdefault(subject,{"languages":{}})
    l=s["languages"].setdefault(language or "unspecified",{"lessons":[],"source_url":source_url})
    existing={x["title"].casefold() for x in l["lessons"]}
    for x in lessons:
        if x["title"].casefold() not in existing:
            l["lessons"].append(x); existing.add(x["title"].casefold())
    g["_status"]="partially_synced"

def main(dest="app/static/crdp_official",output="app/static/crdp_master_curriculum_index.json"):
    root=Path(dest); pdfdir=root/"pdf"; pdfdir.mkdir(parents=True,exist_ok=True)
    master={
      "schema_version":"6.0",
      "authority":"CRDP Lebanon",
      "academic_year":"2025-2026",
      "generated_at":datetime.now(timezone.utc).isoformat(),
      "policy":{
        "all_grades":True,"all_subjects":True,
        "never_invent_lesson_titles":True,
        "preserve_official_order":True,
        "reject_instruction_rows":True,
        "page_local_grade_detection":True,
        "never_inherit_grade_across_pages":True
      },
      "catalog":{g:{"_status":"awaiting_official_sync","subjects":{}} for g in GRADES},
      "annual_sources":[],"book_lists":[],"errors":[]
    }

    links=[(lab,url,detect_subject_from_link(lab,url)) for lab,url in html_links(ANNUAL_PAGE) if ".pdf" in url.lower()]
    seen=set(); links=[x for x in links if not (x[1] in seen or seen.add(x[1]))]

    for i,(label,url,subject) in enumerate(links,1):
        rec={"label":label,"url":url,"subject":subject}
        try:
            data=get(url).content
            path=pdfdir/f"annual_{i:02d}.pdf"
            path.write_bytes(data)
            rec["sha256"]=hashlib.sha256(data).hexdigest()
            doc=fitz.open(path)

            for page in doc:
                page_text=page.get_text("text")
                grade=detect_grade_from_page(page_text)   # STRICT: page-local only
                if not grade or not subject:
                    continue
                language,lessons=page_lessons(page,grade,subject,url)
                add(master,grade,subject,language,lessons,url)

        except Exception as e:
            rec["error"]=str(e)
            master["errors"].append({"url":url,"error":str(e)})

        master["annual_sources"].append(rec)

    try:
        for label,url in html_links(BOOKS_PAGE):
            if ".pdf" in url.lower():
                master["book_lists"].append({"label":label,"url":url})
    except Exception as e:
        master["errors"].append({"url":BOOKS_PAGE,"error":str(e)})

    lesson_count=0; populated=0; pairs=0
    for gnode in master["catalog"].values():
        if gnode["subjects"]: populated+=1
        pairs+=len(gnode["subjects"])
        for snode in gnode["subjects"].values():
            for lnode in snode["languages"].values():
                lesson_count+=len(lnode["lessons"])

    master["coverage"]={
      "grades_total":len(GRADES),
      "grades_with_data":populated,
      "subject_grade_pairs":pairs,
      "verified_lessons":lesson_count,
      "annual_subject_pdfs":len(master["annual_sources"]),
      "book_list_pdfs":len(master["book_lists"]),
      "complete":False
    }

    out=Path(output)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(master,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(master["coverage"],ensure_ascii=False))
    return 0

if __name__=="__main__":
    raise SystemExit(main(
      sys.argv[1] if len(sys.argv)>1 else "app/static/crdp_official",
      sys.argv[2] if len(sys.argv)>2 else "app/static/crdp_master_curriculum_index.json"
    ))
