from __future__ import annotations

import sys
from pathlib import Path

# Support both "python scripts/..." and "python -m scripts...." on Railway/CI.
if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.nabil_requirement5_gate import validate_requirement5_lab
from scripts.nabil_interactive_lab import render_verified_lab
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
                "say": "Move to the next verified evidence item.",
                "target_ids": ["evidence:1"],
                "action": "set_state",
                "state_before": {"i": 0},
                "state_after": {"i": 1},
                "scientific_constraints": ["Only source-backed sequence state may change."],
                "evidence_quote": q2,
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

    procedure_source = (
        "Use the beaker. Add the sample to the beaker. "
        "Stir the sample. Observe the colour change."
    )
    procedure = {
        "supported": True,
        "kind": "PROCEDURE_OBSERVATION",
        "title": "Verified practical procedure",
        "instructions": "Run only the documented steps.",
        "observation": "Observe only the documented outcome.",
        "evidence_ref": "C-PROC",
        "evidence_basis": "text",
        "evidence_quote": "Add the sample to the beaker.",
        "materials": [
            {"label": "Beaker", "evidence_quote": "Use the beaker."},
        ],
        "procedure_steps": [
            {"label": "Add sample", "evidence_quote": "Add the sample to the beaker."},
            {"label": "Stir", "evidence_quote": "Stir the sample."},
        ],
        "observations": [
            {"label": "Colour change", "evidence_quote": "Observe the colour change."},
        ],
        "teacher_script": [
            {
                "say": "Point to the documented beaker.",
                "target_ids": ["material:0"],
                "action": "point",
                "state_before": {"procedure_index": -1},
                "state_after": {"procedure_index": -1},
                "scientific_constraints": ["Use only documented apparatus."],
                "evidence_quote": "Use the beaker.",
            },
            {
                "say": "Highlight the first documented step.",
                "target_ids": ["procedure:0"],
                "action": "highlight",
                "state_before": {"procedure_index": -1},
                "state_after": {"procedure_index": -1},
                "scientific_constraints": ["Use only documented procedure."],
                "evidence_quote": "Add the sample to the beaker.",
            },
            {
                "say": "Apply the first documented procedure state.",
                "target_ids": ["procedure:0"],
                "action": "set_state",
                "state_before": {"procedure_index": -1},
                "state_after": {"procedure_index": 0},
                "scientific_constraints": ["No invented action or outcome."],
                "evidence_quote": "Add the sample to the beaker.",
            },
            {
                "say": "Advance to the documented stirring step.",
                "target_ids": ["procedure:1"],
                "action": "set_state",
                "state_before": {"procedure_index": 0},
                "state_after": {"procedure_index": 1, "reveal_observations": True},
                "scientific_constraints": ["Reveal only the documented observation after documented steps."],
                "evidence_quote": "Stir the sample.",
            },
            {
                "say": "Observe the documented colour change.",
                "target_ids": ["observation:0"],
                "action": "observe",
                "state_before": {"procedure_index": 1, "reveal_observations": True},
                "state_after": {"procedure_index": 1, "reveal_observations": True},
                "scientific_constraints": ["Observation must match source evidence."],
                "evidence_quote": "Observe the colour change.",
            },
            {
                "say": "Conclude only from the verified observation.",
                "target_ids": ["observation:0"],
                "action": "conclude",
                "state_before": {"procedure_index": 1, "reveal_observations": True},
                "state_after": {"procedure_index": 1, "reveal_observations": True},
                "scientific_constraints": ["Do not add a scientific conclusion absent from source."],
                "evidence_quote": "Observe the colour change.",
            },
        ],
    }
    procedure = validate_requirement5_lab(procedure, source_text=procedure_source)
    procedure = validate_and_annotate_curriculum_lab(
        procedure,
        entry={"grade": 6, "subject": "general_science", "lesson_id": "G06-SCIENCE-001"},
        profile={"grade": 6, "subject": "general_science", "level": "L2"},
        concept={"concept_id": "C-PROC", "source_page": 4},
    )
    html, active = render_verified_lab(procedure, "en", "C-PROC")
    assert active is True
    assert 'data-lab-kind="PROCEDURE_OBSERVATION"' in html
    assert "Run procedure" in html
    assert "nabil-procedure-step" in html
    assert procedure["_curriculum_scientific_lab"]["activity_class"] == "scientific_practical_procedure"
    print("PASS practical_procedure_r5_renderer")

    invalid_procedure = dict(procedure)
    invalid_procedure["observations"] = [
        {"label": "Invented", "evidence_quote": "The temperature becomes 100 C."}
    ]
    invalid_procedure.pop("_requirement5", None)
    invalid_procedure.pop("_curriculum_scientific_lab", None)
    try:
        validate_requirement5_lab(invalid_procedure, source_text=procedure_source)
        raise AssertionError("invented practical observation unexpectedly passed")
    except RuntimeError:
        pass
    print("PASS invented_practical_observation_fails_closed")

    print("NABIL_SCIENTIFIC_LAB_COVERAGE_MATRIX_PASS cells=60")


if __name__ == "__main__":
    main()
