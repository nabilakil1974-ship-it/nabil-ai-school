from __future__ import annotations

from scripts.nabil_requirement5_gate import validate_requirement5_lab
from scripts.nabil_scientific_lab_coverage import (
    TARGET_GRADES, TARGET_SUBJECTS, curriculum_matrix,
    expected_level, validate_and_annotate_curriculum_lab,
    validate_lesson_scientific_lab_coverage,
)


SOURCE = (
    "Observe the verified change. The result follows only from this verified evidence. "
    "Compare the two verified states and conclude from the observation."
)


def base_spec():
    q1 = "Observe the verified change."
    q2 = "The result follows only from this verified evidence."
    return {
        "supported": True,
        "kind": "EVIDENCE_SEQUENCE",
        "title": "Verified activity",
        "instructions": "Explore the verified evidence.",
        "observation": "Conclude only from verified evidence.",
        "evidence_ref": "C1",
        "evidence_basis": "text",
        "evidence_quote": q1,
        "steps": [
            {"label": "Observe", "evidence_quote": q1},
            {"label": "Conclude", "evidence_quote": q2},
        ],
        "teacher_script": [
            {
                "say": "Observe.",
                "target_ids": ["evidence:0"],
                "action": "point",
                "state_before": {"i": -1},
                "state_after": {"i": 0},
                "scientific_constraints": ["Only source evidence."],
                "evidence_quote": q1,
            },
            {
                "say": "Highlight the evidence.",
                "target_ids": ["evidence:0"],
                "action": "highlight",
                "state_before": {"i": 0},
                "state_after": {"i": 0},
                "scientific_constraints": ["Only source evidence."],
                "evidence_quote": q1,
            },
            {
                "say": "Observe the verified result.",
                "target_ids": ["evidence:1"],
                "action": "observe",
                "state_before": {"i": 0},
                "state_after": {"i": 1},
                "scientific_constraints": ["Only source evidence."],
                "evidence_quote": q2,
            },
            {
                "say": "Conclude.",
                "target_ids": ["evidence:1"],
                "action": "conclude",
                "state_before": {"i": 1},
                "state_after": {"i": 1},
                "scientific_constraints": ["Only source evidence."],
                "evidence_quote": q2,
            },
        ],
    }


def main():
    matrix = curriculum_matrix()
    assert len(matrix) == 12 * 5
    assert {x["grade"] for x in matrix} == set(TARGET_GRADES)
    assert {x["subject"] for x in matrix} == set(TARGET_SUBJECTS)
    print("PASS coverage_matrix_60_obligations")

    for grade in TARGET_GRADES:
        assert expected_level(grade) in {"L1", "L2", "L3"}
    print("PASS grades_1_to_12_age_band_contract")

    for grade in TARGET_GRADES:
        for subject in sorted(TARGET_SUBJECTS):
            spec = validate_requirement5_lab(
                base_spec(), source_text=SOURCE, source_figure_verified=False
            )
            profile = {
                "grade": grade,
                "subject": subject,
                "level": expected_level(grade),
            }
            entry = {"grade": grade, "subject": subject, "lesson_id": f"G{grade:02d}-{subject}-001"}
            concept = {"concept_id": "C1", "source_page": 1}
            spec = validate_and_annotate_curriculum_lab(
                spec, entry=entry, profile=profile, concept=concept
            )
            report = validate_lesson_scientific_lab_coverage(
                profile, [{"concept_id": "C1", "lab_spec": spec}]
            )
            assert report["passed"] is True
            assert report["covered_concepts"] == 1
    print("PASS all_60_grade_subject_cells_r5_locked")

    bad = base_spec()
    bad.pop("evidence_quote")
    try:
        validate_requirement5_lab(bad, source_text=SOURCE)
        raise AssertionError("unverified lab unexpectedly passed")
    except RuntimeError:
        pass
    print("PASS missing_evidence_fails_closed")

    spec = validate_requirement5_lab(base_spec(), source_text=SOURCE)
    profile = {"grade": 7, "subject": "physics", "level": "L2"}
    try:
        validate_lesson_scientific_lab_coverage(
            profile, [{"concept_id": "C1", "lab_spec": spec}]
        )
        raise AssertionError("unannotated lab unexpectedly passed coverage")
    except RuntimeError:
        pass
    print("PASS lesson_missing_coverage_annotation_fails_closed")

    print("NABIL_SCIENTIFIC_LAB_COVERAGE_MATRIX_PASS cells=60")


if __name__ == "__main__":
    main()
