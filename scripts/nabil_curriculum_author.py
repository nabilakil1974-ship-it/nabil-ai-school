"""NABIL curriculum lesson authoring engine (opt-in, fail-closed).

Reads a specified PDF from Drive, extracts exact 1-based PDF pages, asks the
configured model for a structured bilingual *draft*, and writes a reviewable
bundle locally. No draft is uploaded automatically. Publishing is a separate
approval-gated step; see scripts/verified_lesson_publisher.py.

Example:
 python -m scripts.nabil_curriculum_author --book-id ID --grade 9 \
  --subject physics --chapter 8 --title "Conducteurs ohmiques" \
  --pages 92-102 --language fr --out /tmp/nabil-eb9-ohm

This tool does not infer unverified chapter boundaries or certify diagrams.
"""
import argparse
import hashlib
import html
import io
import json
import os
import re
from pathlib import Path

from pypdf import PdfReader

MAX_PAGES = 18
MAX_TEXT = 58000
PROMPT = """You are authoring a Lebanese curriculum lesson. The supplied PDF text
is the ONLY evidence for book-specific claims, numerical values and exercises.
Never invent a textbook exercise, page, quote, drawing, or experimental result.
Return ONLY valid JSON, no markdown, with this exact schema:
{
 "title":{"fr":"...","en":"..."},
 "objectives":[{"fr":"...","en":"..."}],
 "concepts":[{"heading":{"fr":"...","en":"..."},
   "explanation":{"fr":"...","en":"..."},
   "source_pdf_page":92,"verbatim_excerpt":"EXACT PDF text excerpt >=12 characters",
   "figure_spec":{"kind":"none","scientific_labels":[],"review_note":"..."}}],
 "activities":[{"prompt":{"fr":"...","en":"..."},
   "solution":{"fr":"...","en":"..."},"source_pdf_page":92,
   "verbatim_excerpt":"EXACT PDF excerpt >=12 characters"}],
 "exercises":[{"number":"1","prompt":{"fr":"...","en":"..."},
   "solution":{"fr":"...","en":"..."},"source_pdf_page":92,
   "verbatim_excerpt":"EXACT PDF excerpt >=12 characters"}],
 "worksheet":[{"question":{"fr":"...","en":"..."},
   "answer":{"fr":"...","en":"..."}}],
 "summary":[{"fr":"...","en":"..."}],
 "scientific_review_notes":["..."]
}
Each concept and sourced activity/exercise must cite an exact PDF page and a
literal excerpt found on that page. If a page has insufficient extractable text
or the exercise depends on a figure you cannot see, OMIT that item and record
the omission in scientific_review_notes. Never invent SVG paths or scientific
diagrams: figure_spec.kind='none' pending independent drawing verification.
Include a minimum of four concepts, two activities, two exercises, and four
worksheet questions only if supported. French and English convey equivalent
meaning. Do not claim English text is the English textbook. Produce meaningful,
age-appropriate pedagogy with worked reasoning, not generic filler.
"""

def _norm(s):
    return re.sub(r"\s+", " ", s).strip().casefold()

def _pages(raw, count):
    m = re.fullmatch(r"(\d+)-(\d+)", raw)
    if not m:
        raise ValueError("PAGES_REQUIRE_EXPLICIT_START-END")
    first, last = map(int, m.groups())
    if first < 1 or last < first or last > count or last-first+1 > MAX_PAGES:
        raise ValueError("PAGES_OUT_OF_RANGE_OR_TOO_MANY")
    return list(range(first, last+1))

def _download(book_id):
    from scripts.nabil_lesson_factory import drive
    from googleapiclient.http import MediaIoBaseDownload
    service = drive(write=False)
    meta = service.files().get(fileId=book_id,
             fields="id,name,mimeType").execute()
    if meta["mimeType"] != "application/pdf":
        raise ValueError("SOURCE_NOT_PDF")
    stream = io.BytesIO()
    loader = MediaIoBaseDownload(stream, service.files().get_media(fileId=book_id))
    done = False
    while not done:
        _, done = loader.next_chunk()
        if stream.tell() > 70_000_000:
            raise ValueError("PDF_TOO_LARGE")
    return meta, stream.getvalue()

def _generate(prompt):
    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY_REQUIRED_ON_SERVER_ONLY")
    client = OpenAI(api_key=api_key, timeout=150)
    response = client.chat.completions.create(
        model=os.getenv("NABIL_LESSON_AUTHOR_MODEL",
                        os.getenv("OPENAI_TEXT_MODEL", "gpt-5.5")),
        messages=[{"role":"system","content":PROMPT},
                  {"role":"user","content":prompt}],
        response_format={"type":"json_object"},
        temperature=0)
    return json.loads(response.choices[0].message.content)

def _validate(draft, source):
    for key in ("title","objectives","concepts","activities","exercises",
                "worksheet","summary","scientific_review_notes"):
        if key not in draft:
            raise ValueError("MISSING_"+key)
    if (len(draft["concepts"]) < 4 or len(draft["activities"]) < 2
            or len(draft["exercises"]) < 2 or len(draft["worksheet"]) < 4
            or len(draft["summary"]) < 3):
        raise ValueError("INSUFFICIENT_SOURCE_GROUNDED_LESSON")
    for kind in ("concepts","activities","exercises"):
        for entry in draft[kind]:
            page = entry["source_pdf_page"]
            excerpt = entry["verbatim_excerpt"]
            if page not in source or len(excerpt.strip()) < 12:
                raise ValueError("INVALID_SOURCE_CITATION_"+kind)
            if _norm(excerpt) not in _norm(source[page]):
                raise ValueError("UNVERIFIABLE_SOURCE_EXCERPT_"+str(page))
            if kind == "concepts" and entry["figure_spec"]["kind"] != "none":
                raise ValueError("UNVERIFIED_GENERATED_SCIENTIFIC_FIGURE")
    for section in ("objectives","summary"):
        for item in draft[section]:
            if not item.get("fr") or not item.get("en"):
                raise ValueError("BILINGUAL_TEXT_MISSING")
    for kind in ("concepts","activities","exercises","worksheet"):
        for entry in draft[kind]:
            fields = ("heading","explanation") if kind == "concepts" else (
                ("question","answer") if kind == "worksheet" else ("prompt","solution"))
            for field in fields:
                if not entry[field].get("fr") or not entry[field].get("en"):
                    raise ValueError("BILINGUAL_TEXT_MISSING_"+field)

def _bilingual(value, tag="span"):
    fr = html.escape(value["fr"])
    en = html.escape(value["en"])
    return f'<{tag} data-fr="{fr}" data-en="{en}">{fr}</{tag}>'

def _render(draft, manifest):
    cards = []
    def section(title, body, klass=""):
        cards.append(f'<section class="card {klass}"><h2>{title}</h2>{body}</section>')
    section(_bilingual({"fr":"Objectifs","en":"Objectives"}),
            "".join("<p>"+_bilingual(x)+"</p>" for x in draft["objectives"]))
    for x in draft["concepts"]:
        section(_bilingual(x["heading"]),"<p>"+_bilingual(x["explanation"])+
                "</p><small>PDF p. "+str(x["source_pdf_page"])+
                " · figure pending independent scientific verification</small>")
    for i,x in enumerate(draft["activities"],1):
        section(_bilingual({"fr":"Activité "+str(i),"en":"Activity "+str(i)}),
                "<p>"+_bilingual(x["prompt"])+
                "</p><details><summary>Solution / حل</summary><p>"+
                _bilingual(x["solution"])+"</p></details>")
    for x in draft["exercises"]:
        section(_bilingual({"fr":"Exercice "+str(x["number"]),
                            "en":"Exercise "+str(x["number"])}),
                "<p>"+_bilingual(x["prompt"])+
                "</p><details><summary>Solution / حل</summary><p>"+
                _bilingual(x["solution"])+"</p></details>")
    worksheet = []
    for i,x in enumerate(draft["worksheet"],1):
        worksheet.append('<div class="question"><p>'+str(i)+". "+
                         _bilingual(x["question"])+
                         '</p><input aria-label="Answer '+str(i)+'"><details><summary>Answer / Réponse</summary><p>'+
                         _bilingual(x["answer"])+"</p></details></div>")
    section(_bilingual({"fr":"Fiche de travail interactive",
                        "en":"Interactive worksheet"}),"".join(worksheet))
    section(_bilingual({"fr":"Carte de synthèse","en":"Final reference card"}),
            "".join("<p>"+_bilingual(x)+"</p>" for x in draft["summary"]),
            "summary")
    cards_html = "".join(cards)
    title = _bilingual(draft["title"])
    return """<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>NABIL AI | Draft lesson</title><style>
*{box-sizing:border-box}body{margin:0;background:#071a2b;color:#e9f8ff;
font:16px/1.6 system-ui,Arial}header{padding:20px;background:#103858}
main{max-width:1050px;margin:auto;padding:14px}.card{background:#102b42;
border:1px solid #36a5dc;border-radius:16px;padding:20px;margin:16px 0}
h1,h2{color:#8ce9ff}p{overflow-wrap:anywhere}.summary{border:2px solid #31d9a8}
details{border-left:3px solid #31d9a8;padding:10px}input,select{font:inherit;
max-width:100%;padding:10px}small{color:#ffdb88}
@media(max-width:600px){main{padding:8px}.card{padding:13px}}
</style></head><body><header><h1>"""+title+"""</h1>
<label>Langue / Language <select id="lesson-language">
<option value="fr">Français</option><option value="en">English</option>
</select></label><p>REVIEW DRAFT — NOT APPROVED / BROUILLON NON VALIDÉ</p>
</header><main>"""+cards_html+"""</main><script>
function language(l){document.documentElement.lang=l;
document.querySelectorAll('[data-en][data-fr]').forEach(e=>e.textContent=e.dataset[l]);}
document.getElementById('lesson-language').addEventListener('change',
e=>language(e.target.value));language('fr');
</script></body></html>"""

def main():
    p = argparse.ArgumentParser()
    for name in ("book-id","subject","title","pages","out"):
        p.add_argument("--"+name, required=True)
    p.add_argument("--grade",type=int,required=True)
    p.add_argument("--chapter",type=int,required=True)
    p.add_argument("--language",choices=("fr","en"),required=True)
    args = p.parse_args()
    if args.grade not in range(1,13) or args.chapter < 1:
        p.error("invalid grade/chapter")
    if args.subject not in ("mathematics","physics","chemistry","biology","general_science"):
        p.error("unsupported subject")
    out = Path(args.out).resolve()
    out.mkdir(parents=True,exist_ok=True)
    meta, raw = _download(args.book_id)
    reader = PdfReader(io.BytesIO(raw))
    pages = _pages(args.pages,len(reader.pages))
    source = {n:reader.pages[n-1].extract_text() or "" for n in pages}
    if any(len(t.strip()) < 150 for t in source.values()):
        raise ValueError("SCANNED_OR_UNREADABLE_PAGE_REQUIRES_VISION_REVIEW")
    if sum(map(len,source.values())) > MAX_TEXT:
        raise ValueError("SOURCE_TOO_LONG_SPLIT_CHAPTER")
    source_prompt = json.dumps({
        "grade":args.grade,"subject":args.subject,"chapter":args.chapter,
        "title":args.title,"original_language":args.language,
        "pdf_filename":meta["name"],"pages":source},ensure_ascii=False)
    draft = _generate(source_prompt)
    _validate(draft,source)
    from scripts.nabil_lesson_artifacts import build_bundle
    (out/"source.pdf").write_bytes(raw)
    (out/"lesson_draft.json").write_text(json.dumps(draft,ensure_ascii=False,indent=2),
                                          encoding="utf-8")
    artifacts = build_bundle(draft,raw,out,_render(draft,{}),
                             args.grade,args.subject,args.chapter,args.title)
    manifest = {
        "lesson_id": "G%02d-%s-CH%02d" % (args.grade,args.subject.upper(),args.chapter),
        "grade":args.grade,"subject":args.subject,"chapter":args.chapter,
        "title":args.title,"source_pdf":"source.pdf",
        "source_sha256":hashlib.sha256(raw).hexdigest(),
        "source_drive_file_id":args.book_id,
        **artifacts,
    }
    (out/"manifest.json").write_text(
        json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
    report = {"status":"SOURCE_TEXT_MATCHED_DRAFT_NOT_APPROVED_NOT_PUBLISHED",
              "book_id":args.book_id,"book_name":meta["name"],
              "pdf_sha256":hashlib.sha256(raw).hexdigest(),
              "pdf_pages":pages,"grade":args.grade,"subject":args.subject,
              "chapter":args.chapter,"title":args.title,
              "concepts":len(draft["concepts"]),
              "activities":len(draft["activities"]),
              "exercises":len(draft["exercises"]),
              "worksheet":len(draft["worksheet"]),
              "scientific_review_notes":draft["scientific_review_notes"],
              "bundle_manifest":"manifest.json",
              "html":"lesson.html",
              "pptx_en":"lesson_en.pptx","pptx_fr":"lesson_fr.pptx",
              "original_pdf_page_images":len(artifacts["images"]),
              "missing":["independently reviewed scientific diagrams",
                         "reference-matched PowerPoint visual approval",
                         "independent solution verification",
                         "live Railway display acceptance"]}
    (out/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),
                                   encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
