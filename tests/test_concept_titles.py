import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.nabil_factory.factory import orchestrator as o  # noqa: E402

BAD = ["grain in the first box;", "prains in the second ;", "CLS",
       "Let a and b be two positive numbers. Consider:| *]",
       "smallest natural number» so that the given", "product is an integer"]
GOOD = ["Property 4", "Powers of ten", "Product of powers", "Puissances de dix"]


def test_title_quality_detector():
    assert not any(o.concept_title_is_clean(t) for t in BAD)
    assert all(o.concept_title_is_clean(t) for t in GOOD)


def _theory():
    return {"activities": [{"concept_id": f"C0{i}", "title": t} for i, t in enumerate(BAD[:3] + GOOD[:1], 1)]}


def test_llm_titles_used_when_clean_and_fallback_otherwise(monkeypatch):
    ev = {"concepts": [{"concept_id": f"C0{i}", "raw_text": "text"} for i in range(1, 5)]}
    monkeypatch.setitem(o.__dict__, "execute_llm_completion",
                        lambda *a, **k: json.dumps({"titles": {"1": "Wheat on the chessboard", "2": "bad;", "3": "Naming a power"}}))
    out = o.ensure_clean_concept_titles(_theory(), ev, "en")
    t = [a["title"] for a in out["activities"]]
    assert t == ["Wheat on the chessboard", "Idea 2", "Naming a power", "Property 4"]


def test_llm_failure_never_raises(monkeypatch):
    def boom(*a, **k):
        raise RuntimeError("down")
    monkeypatch.setitem(o.__dict__, "execute_llm_completion", boom)
    out = o.ensure_clean_concept_titles(_theory(), {"concepts": []}, "ar")
    assert [a["title"] for a in out["activities"]][:3] == ["الفكرة 1", "الفكرة 2", "الفكرة 3"]


def test_restored_theory_board_is_rebuilt_with_clean_titles(monkeypatch):
    monkeypatch.setitem(o.__dict__, "execute_llm_completion",
                        lambda *a, **k: json.dumps({"titles": {"1": "Wheat on the chessboard"}}))
    acts = [{"concept_id": "C01", "title": "grain in the first box;", "lab_html": "", "allow_no_lab": True,
             "teaching_steps": [{"sentence": "We place one grain of wheat on the first square"}],
             "conclusion": "2^n"}]
    theory = {"title": "Powers", "activities": acts, "whole_lesson_lab_html": "OLD grain in the first box;"}
    out = o.ensure_clean_concept_titles(theory, {"concepts": []}, "en", subject="Mathematics")
    assert "grain in the first box;" not in out["whole_lesson_lab_html"]
    assert "Wheat on the chessboard" in out["whole_lesson_lab_html"]
