import json, sys
from pathlib import Path

EXPECTED_GRADES = [
    "الروضة الأولى","الروضة الثانية","الروضة الثالثة",
    "الصف الأول","الصف الثاني","الصف الثالث","الصف الرابع","الصف الخامس","الصف السادس",
    "الصف السابع","الصف الثامن","الصف التاسع",
    "الأول ثانوي","الثاني ثانوي - العلوم","الثاني ثانوي - الإنسانيات",
    "الثالث ثانوي - علوم الحياة","الثالث ثانوي - العلوم العامة",
    "الثالث ثانوي - الاجتماع والاقتصاد","الثالث ثانوي - الآداب والإنسانيات",
]

def validate(path):
    data=json.loads(Path(path).read_text(encoding="utf-8"))
    assert data.get("policy",{}).get("no_grade_specific_hardcoding") is True
    catalog=data.get("catalog",{})
    missing=[g for g in EXPECTED_GRADES if g not in catalog]
    if missing:
        raise SystemExit("Missing grades: "+", ".join(missing))

    errors=[]
    for grade,gdata in catalog.items():
        subjects=gdata.get("subjects",{}) if isinstance(gdata,dict) else {}
        for subject,sdata in subjects.items():
            languages=sdata.get("languages",{}) if isinstance(sdata,dict) else {}
            for language,ldata in languages.items():
                books=ldata.get("books",[]) if isinstance(ldata,dict) else []
                for book in books:
                    lessons=book.get("lessons",[])
                    seen=set()
                    for lesson in lessons:
                        title=str(lesson.get("title") or "").strip()
                        if not title:
                            errors.append(f"{grade}/{subject}/{language}: blank title")
                            continue
                        k=title.casefold()
                        if k in seen:
                            errors.append(f"{grade}/{subject}/{language}: duplicate {title}")
                        seen.add(k)
                        if lesson.get("verification_status") not in {
                            "verified","official-crdp-book-source","source-extracted-needs-review"
                        }:
                            errors.append(f"{grade}/{subject}/{language}: bad verification status for {title}")

    if errors:
        raise SystemExit("\n".join(errors))
    print("Master curriculum validation: OK")

if __name__=="__main__":
    validate(sys.argv[1] if len(sys.argv)>1 else "app/static/crdp_master_curriculum_index.json")
