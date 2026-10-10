import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.nabil_factory.cards.v18_board import (  # noqa: E402
    build_golden_spec, plain_math, render_v18_exercises_board, render_v18_smart_board)

ACTS = [{"concept_id": "C1", "title": "Powers", "conclusion": "10² = 100",
         "lab_html": "<div class='nabil-reference-smart-lab'>lab</div>",
         "teaching_steps": [{"label": "See", "sentence": "10² means 10 × 10.", "formula": "10² = 100"}]}]


def test_board_has_contract_markers_and_inline_engine():
    spec = build_golden_spec("T", ACTS, "en", subject="Mathematics")
    h = render_v18_smart_board("T", ACTS, "en", spec, "C")
    for marker in ('data-nabil-v18-board="NABIL_V18_SMART_BOARD_V1"', 'id="nabilWholeLessonFrame"',
                   'id="nabilWholePlay"', 'data-nabil-v18-golden="true"', "window.NABILScientificCards={",
                   "nabil:page-language-change", "data-v18-labels="):
        assert marker in h, marker
    assert "/static/nabil_scientific_solution_cards_e2e.js" not in h


def test_golden_spec_required():
    import pytest
    with pytest.raises(RuntimeError, match="V18_GOLDEN_CARD_SPEC_EMPTY"):
        render_v18_smart_board("T", ACTS, "en", {"sections": []}, "C")


def test_exercises_board_only_shows_solved():
    ex = [{"number": 1, "exercise_id": "E1", "exact_source_prompt": "x", "solution_status": "OMITTED_UNVERIFIED",
           "_pre_solved_solution": None}]
    assert render_v18_exercises_board("T", ex, "ar", "Mathematics") == ""
    ex[0].update(solution_status="SOLVED", _pre_solved_solution={"steps": ["a) 2 × 3 = 6"], "final_answer": "6"})
    assert 'data-v18-mode="exercises"' in render_v18_exercises_board("T", ex, "fr", "Mathematics")


def test_plain_math_strips_delimiters():
    assert plain_math(r"\(67 \times 10^{2}\)") == "67 × 10²"
