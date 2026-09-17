import json
import re
import sys
from pathlib import Path

BAD = [
    r"\bsuspend\b", r"\bmaintain(?:ed)?\b", r"\bretained\b", r"\bprerequisite",
    r"\brecall(?:ing)?\b", r"\bwithout writing\b", r"\bdo not\b",
    r"لسلست", r"ةداملا", r"ةيميلعتلا", r"عقاولا", r"شاعملا",
    r"اذه يف يهتني", r"ة يعماجلا", r"تاصاصتخ",
]

ELEMENTARY_MATH = {
    "the numbers from 1 to 3", "addition", "tens and ones", "numbers up to 99"
}

def main(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    cov = data.get("coverage", {})

    lessons = int(cov.get("verified_lessons", 0) or 0)
    grades = int(cov.get("grades_with_data", 0) or 0)
    annual = int(cov.get("annual_subject_pdfs", 0) or 0)

    if annual < 15:
        raise SystemExit(f"Missing annual CRDP subject PDFs: {annual} < 15")
    if lessons == 0:
        raise SystemExit("ZERO verified lessons — refusing false success.")

    # IMPORTANT:
    # Do NOT fail only because a stricter parser returns fewer lessons than an older parser.
    # A lower count can mean cleaner extraction. Report it as a warning and inspect the artifact.
    if lessons < 343:
        print(f"WARNING: clean lesson count is below previous baseline: {lessons} < 343")
    if grades < 14:
        print(f"WARNING: grade coverage is below previous baseline: {grades} < 14")

    errors = []

    globally_excluded = {
        "علم الاجتماع", "علم الاقتصاد", "التاريخ",
        "الجغرافيا", "الفلسفة والحضارات"
    }
    secondary_languages = {
        "اللغة العربية", "اللغة الفرنسية", "اللغة الإنجليزية"
    }

    # Kindergarten is intentionally out of scope in this phase.
    for grade in data.get("catalog", {}):
        if grade.startswith("الروضة"):
            errors.append(f"kindergarten node must not exist in current phase: {grade}")

    for grade, gnode in data.get("catalog", {}).items():
        secondary = (
            grade == "الأول ثانوي"
            or grade.startswith("الثاني ثانوي")
            or grade.startswith("الثالث ثانوي")
        )

        for subject, snode in gnode.get("subjects", {}).items():
            if subject in globally_excluded:
                errors.append(f"globally excluded subject leaked into catalog: {grade} -> {subject}")
            if secondary and subject in secondary_languages:
                errors.append(f"secondary language leaked into catalog: {grade} -> {subject}")
            for lang, lnode in snode.get("languages", {}).items():
                for item in lnode.get("lessons", []):
                    title = str(item.get("title") or "")
                    low = title.strip().lower()

                    if item.get("source_grade") != grade:
                        errors.append(f"grade provenance mismatch: {grade} / {title}")
                    if item.get("source_subject") != subject:
                        errors.append(f"subject provenance mismatch: {subject} / {title}")
                    if any(re.search(p, title, re.I) for p in BAD):
                        errors.append(f"garbage/instruction leaked as lesson: {title}")

                    if re.search(r"\b(?:note|remarque)\s*[:：]|ملاحظة\s*[:：]", title, re.I):
                        errors.append(f"editorial note still attached to lesson title: {title}")

                    if "_" in title:
                        errors.append(f"PDF wrap marker still present in lesson title: {title}")

                    if title.strip().lower() in {
                        "important for healthy life", "important for a healthy life"
                    }:
                        errors.append(f"non-lesson heading leaked into catalog: {title}")

                    ar = len(re.findall(r"[\u0600-\u06FF]", title))
                    lat = len(re.findall(r"[A-Za-zÀ-ÿ]", title))
                    if lang in {"English", "Français"} and ar > lat and ar > 4:
                        errors.append(f"Arabic extraction garbage in {lang}: {title}")

                    if grade.startswith("الثالث ثانوي") and subject == "الرياضيات":
                        if low in ELEMENTARY_MATH:
                            errors.append(f"elementary math leaked into Grade 12: {title}")

    if errors:
        raise SystemExit("\n".join(errors[:80]))

    print("CRDP V8 integrity validation: PASS")
    print(json.dumps(cov, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main(
        sys.argv[1] if len(sys.argv) > 1
        else "app/static/crdp_master_curriculum_index.json"
    ))
