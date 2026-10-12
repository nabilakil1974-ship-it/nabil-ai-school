import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.nabil_factory.factory import orchestrator as o  # noqa: E402


def _act(i, q=None):
    return {"activity_num": i, "concept_id": f"C0{i}", "title": f"Idea {i}", "phenomenon": "p",
            "investigation": "i", "observation": "o", "interpretation": "t", "conclusion": f"10^{i}",
            "visual_html": "", "lab_html": "<div class='nabil-reference-smart-lab'>lab</div>",
            "student_question": q, "source_page": 10 + i,
            "teaching_steps": [{"label": "a", "sentence": "s", "formula": ""}]}


def test_every_concept_ends_with_visible_documented_apply_in_page_a():
    q = {"q": "What is 10^1?", "options": ["10", "1", "100"], "correct_index": 0,
         "explanation": "x", "feedback": "ok"}
    ex = [{"exercise_id": f"E{i}", "number": i, "source_page": 10 + i, "verified_against_source": True,
           "solution_status": "SOLVED", "source_origin": "TEXTBOOK",
           "exact_source_prompt": f"Compute 10^{i} idea {i}"} for i in (2, 3)]
    ev = {"concepts": [{"concept_id": f"C0{i}", "title": f"Idea {i}", "raw_text": f"idea {i}",
                        "source_page": 10 + i} for i in (1, 2, 3)]}
    th = o.ensure_verified_apply_steps({"activities": [_act(1, q), _act(2), _act(3)], "worksheet": []}, ex, ev, "en")
    entry = {"canonical_title": "Powers", "language": "en", "lesson_id": "T", "subject": "Mathematics",
             "book_id": "B", "grade": "7", "pdf_start_page": 10, "pdf_end_page": 20}
    html = o.render_lesson_page_a(entry, th, ev)
    assert html.count('data-step="application"') == len(ev["concepts"])
    assert "Verified textbook exercise #2" in html and "Verified textbook exercise #3" in html


def test_no_verified_exercise_means_no_invented_apply():
    ev = {"concepts": [{"concept_id": "C02", "title": "Idea 2", "raw_text": "x", "source_page": 12}]}
    th = o.ensure_verified_apply_steps({"activities": [_act(2)]}, [], ev, "en")
    assert not th["activities"][0].get("student_question") and not th["activities"][0].get("student_apply_prompt")


def test_math_rejections_are_recorded_with_page_number_reason():
    ex = [{"exercise_id": "E9", "number": 9, "source_page": 21, "exact_source_prompt": "5⁶ = ?",
           "solution_status": "OMITTED_UNVERIFIED", "solution_rejection_kind": "CONTRADICTED",
           "solution_omission_reason": "MATH_SOLUTION_CONTRADICTION: 5⁶ = 15625 × 5",
           "_rejected_solution": {"steps": ["5⁶ = 15625 × 5"], "final_answer": "78125"}},
          {"exercise_id": "E1", "number": 1, "solution_status": "SOLVED"}]
    rec = o.math_rejection_records(ex)
    assert len(rec) == 1 and rec[0]["source_page"] == 21 and rec[0]["number"] == 9
    assert rec[0]["kind"] == "CONTRADICTED" and rec[0]["last_rejected_attempt"]["final_answer"] == "78125"


def test_llm_metrics_counts_scopes_and_never_invents_cost(monkeypatch):
    monkeypatch.delenv("NABIL_LLM_USD_PER_1M_TOKENS", raising=False)
    o.llm_metrics_reset()
    with o.llm_metrics_scope("translation"):
        b = o._llm_bucket(o._LLM_SCOPE[-1]); b["calls"] += 3; b["prompt_chars"] += 8000
    snap = o.llm_metrics_snapshot()
    assert snap["scopes"]["translation"]["calls"] == 3 and snap["total"]["est_tokens"] == 2000
    assert snap["total"]["est_cost_usd"] is None
    monkeypatch.setenv("NABIL_LLM_USD_PER_1M_TOKENS", "2")
    assert o.llm_metrics_snapshot()["total"]["est_cost_usd"] == 0.004


def test_pipeline_entry_points_are_not_self_recursive():
    """Regression: the recovery wrapper and its impl must each be defined exactly once
    (a rename once made the wrapper call itself -> RecursionError on Railway)."""
    import ast
    src = (Path(__file__).resolve().parents[1] / "scripts/nabil_factory/factory/pipeline.py").read_text()
    tree = ast.parse(src)
    defs = [n.name for n in tree.body if isinstance(n, ast.FunctionDef)]
    assert defs.count("produce_lesson_for_entry") == 1
    assert defs.count("_produce_lesson_for_entry_impl") == 1
    impl = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "_produce_lesson_for_entry_impl")
    assert not any(isinstance(c, ast.Call) and getattr(c.func, "id", "") == "_produce_lesson_for_entry_impl"
                   for c in ast.walk(impl))
    assert callable(o.lesson_metrics_emitter)
