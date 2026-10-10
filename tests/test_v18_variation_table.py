import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.nabil_factory.cards.variation_table import (  # noqa: E402
    build_function_drawing, build_variation_table, extract_function_expr)
from scripts.nabil_factory.cards.v18_board import (  # noqa: E402
    build_golden_spec, render_v18_exercises_board, render_v18_smart_board)

ACT = [{"concept_id": "C1", "title": "Rational", "conclusion": "ok", "allow_no_lab": True,
        "formulas": ["f(x) = (x^2+5)/(2x-3)"],
        "teaching_steps": [{"label": "a", "sentence": "s", "formula": ""}]}]


def test_rational_table_matches_reference():
    t = build_variation_table("(x^2+5)/(2x-3)")
    assert t["critical"] == ["−1.193", "4.193"] and t["poles"] == ["1.5"]
    assert t["rows"][0]["cells"] == ["+", "0", "−", "∥", "−", "0", "+"]
    assert "local max" in t["rows"][1]["cells"][1] and "local min" in t["rows"][1]["cells"][5]


def test_unprovable_returns_none():
    assert build_variation_table("sin(x)") is None
    assert build_variation_table("3x+1") is None
    assert build_variation_table("__import__('os')") is None


def test_drawing_and_extraction():
    assert extract_function_expr(ACT[0]) == "(x^2+5)/(2x-3)"
    d = build_function_drawing("(x^2+5)/(2x-3)")
    assert d["type"] == "function" and len(d["series"]) == 2 and d["vertical_asymptotes"][0]["x"] == 1.5
    assert d["oblique_asymptotes"][0]["m"] == 0.5


def test_board_and_golden_carry_table_in_three_languages():
    for lang in ("ar", "fr", "en"):
        spec = build_golden_spec("T", ACT, lang, subject="Mathematics")
        assert spec["kind"] == "function_study"
        assert spec["function_study"]["variation_table"]["columns"]
        assert any(p.get("table") and p.get("drawings") for p in spec["panels"])
        h = render_v18_smart_board("T", ACT, lang, spec, "C")
        assert 'id="v18VarBox"' in h and '"variation"' in h


def test_non_function_lesson_has_no_table():
    a = [{"concept_id": "C", "title": "P", "conclusion": "100", "allow_no_lab": True,
          "teaching_steps": [{"label": "a", "sentence": "10 x 10", "formula": ""}]}]
    assert "function_study" not in build_golden_spec("T", a, "en", subject="Mathematics")


def test_exercise_board_builds_table_from_prompt():
    ex = [{"number": 1, "exercise_id": "E1", "exact_source_prompt": "Study f(x) = (x^2+5)/(2x-3)",
           "solution_status": "SOLVED", "_pre_solved_solution": {"steps": ["f'(x)=0"], "final_answer": "x = 4.193"}}]
    h = render_v18_exercises_board("T", ex, "en", "Mathematics")
    assert "Graph & Variation" in h
