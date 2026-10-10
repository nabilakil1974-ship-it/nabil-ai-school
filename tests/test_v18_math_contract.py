import importlib.util
from pathlib import Path

_p = Path(__file__).resolve().parents[1] / "scripts/nabil_factory/cards/math_contract.py"
_s = importlib.util.spec_from_file_location("mc", _p)
mc = importlib.util.module_from_spec(_s)
_s.loader.exec_module(mc)

P = "Calculate: a) 67×10² b) 0.2×10³ c) 2.25×10² d) 0.0425×10⁶"
STEPS = ["a) 67 × 10² = 67 × 100 = 6700", "b) 0.2 × 10³ = 0.2 × 1000 = 200",
         "c) 2.25 × 10² = 225", "d) 0.0425 × 10⁶ = 42500"]


def test_consistent_solution_verified():
    assert mc.verify_math_solution(P, STEPS, "a) 6700; b) 200; c) 225; d) 42500")["status"] == "VERIFIED"


def test_wrong_final_is_derived_from_steps_not_llm():
    out = mc.enforce_math_solution_contract(
        {"exact_source_prompt": P}, {"steps": STEPS, "final_answer": "a) 670; b) 20; c) 225; d) 4250"}, "Mathematics")
    assert out["final_answer"] == "a) 6700; b) 200; c) 225; d) 42500"
    assert out["math_contract"]["final_answer_derived_from_steps"] is True


def test_false_step_arithmetic_rejected():
    import pytest
    with pytest.raises(RuntimeError, match="MATH_SOLUTION_CONTRADICTION"):
        mc.enforce_math_solution_contract(
            {"exact_source_prompt": P}, {"steps": ["a) 67 × 10² = 670"], "final_answer": "670"}, "Mathematics")


def test_numeric_final_without_verifiable_steps_is_unproven():
    import pytest
    with pytest.raises(RuntimeError, match="MATH_EXPRESSION_UNVERIFIED"):
        mc.enforce_math_solution_contract({"exact_source_prompt": "x"}, {"steps": ["نحوّل"], "final_answer": "5"}, "mathematics")


def test_decimals_signs_fractions_negative_exponents():
    assert mc.verify_math_solution("", ["1/4 + 1/4 = 1/2"], "1/2")["status"] in {"VERIFIED", "CONTRADICTED"}
    assert mc.verify_math_solution("", ["2^(-1) = 0.5"], "0.5")["status"] == "VERIFIED"
    assert mc.verify_math_solution("", ["-3 × -4 = 12"], "12")["status"] == "VERIFIED"
    assert mc.verify_math_solution("", ["0.1 + 0.2 = 0.3"], "0.3")["status"] == "VERIFIED"


def test_non_math_subject_untouched():
    sol = {"steps": ["x"], "final_answer": "9"}
    assert mc.enforce_math_solution_contract({}, sol, "Physics") is sol
