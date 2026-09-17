import json
import sys
from pathlib import Path

def main(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    coverage = data.get("coverage", {})

    if coverage.get("annual_subject_pdfs", 0) < 10:
        raise SystemExit(
            f"CRDP sync incomplete: only {coverage.get('annual_subject_pdfs',0)} annual subject PDFs discovered."
        )

    if coverage.get("grades_with_data", 0) == 0:
        raise SystemExit("CRDP sync produced ZERO populated grades. Refusing false success.")

    if coverage.get("verified_lessons", 0) == 0:
        raise SystemExit("CRDP sync produced ZERO verified lesson titles. Refusing false success.")

    # Catch the exact secondary-grade bug seen in the previous artifact.
    for src in data.get("book_lists", []):
        label = str(src.get("label") or "")
        grade = src.get("grade")
        if "التعليم الثانوي - السنة الثالثة" in label and grade in {"الصف الثالث", None}:
            raise SystemExit(f"Secondary grade misclassified: {label!r} -> {grade!r}")
        if "التعليم الثانوي - السنة الثانية" in label and grade in {"الصف الثاني", None}:
            raise SystemExit(f"Secondary grade misclassified: {label!r} -> {grade!r}")
        if "التعليم الثانوي - السنة الأولى" in label and grade in {"الصف الأول", None}:
            raise SystemExit(f"Secondary grade misclassified: {label!r} -> {grade!r}")

    print("CRDP master curriculum validation: PASS")
    print(json.dumps(coverage, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main(
        sys.argv[1] if len(sys.argv) > 1
        else "app/static/crdp_master_curriculum_index.json"
    ))
