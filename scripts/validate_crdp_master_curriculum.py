import json, re, sys
from pathlib import Path

BAD = [
 r"\bsuspend\b",r"\bmaintain(?:ed)?\b",r"\bretained\b",r"\bprerequisite",
 r"\brecall(?:ing)?\b",r"\bwithout writing\b",r"\bdo not\b",
 r"لسلست",r"ةداملا",r"ةيميلعتلا"
]

def main(path):
    d=json.loads(Path(path).read_text(encoding="utf-8"))
    cov=d.get("coverage",{})
    if cov.get("annual_subject_pdfs",0)<15:
        raise SystemExit("Missing annual CRDP subject PDFs.")
    if cov.get("verified_lessons",0)==0:
        raise SystemExit("ZERO verified lessons — refusing false success.")

    errors=[]
    for grade,gn in d.get("catalog",{}).items():
        for subject,sn in gn.get("subjects",{}).items():
            for lang,ln in sn.get("languages",{}).items():
                for x in ln.get("lessons",[]):
                    title=str(x.get("title") or "")
                    if x.get("source_grade") != grade:
                        errors.append(f"grade provenance mismatch: {grade} / {title}")
                    if x.get("source_subject") != subject:
                        errors.append(f"subject provenance mismatch: {subject} / {title}")
                    if any(re.search(p,title,re.I) for p in BAD):
                        errors.append(f"instruction/gibberish leaked as lesson: {title}")
    if errors:
        raise SystemExit("\n".join(errors[:40]))
    print("CRDP CLEAN validation: PASS")
    print(json.dumps(cov,ensure_ascii=False))
    return 0

if __name__=="__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv)>1 else "app/static/crdp_master_curriculum_index.json"))
