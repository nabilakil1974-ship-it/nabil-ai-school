from __future__ import annotations

import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import copy
import hashlib
import tempfile
import fitz

import scripts.nabil_lesson_factory as factory
import scripts.nabil_page_checkpoint as checkpoints
from scripts.nabil_transient_resilience_v1781 import ProviderTransientError


def main():
    solution_store = {}
    state_store = []
    calls = {i: 0 for i in range(1, 9)}
    fail_once = {7: True}

    with tempfile.TemporaryDirectory(prefix="nabil_real_pipeline_503_") as td:
        root = Path(td)
        for p in ("versions", "artifacts", "out", "recovery"):
            (root / p).mkdir(parents=True, exist_ok=True)
        factory.VERSIONS_DIR = root / "versions"
        factory.ARTIFACTS_DIR = root / "artifacts"
        factory.OUT_DIR = root / "out"
        factory.RECOVERY_STATE_DIR = root / "recovery"

        pdf = root / "fixture.pdf"
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((72, 72), "NABIL integration fixture")
        doc.save(pdf)
        doc.close()

        entry = {
            "lesson_id": "G07-PHYSICS-503-INTEGRATION",
            "book_id": "BOOK-503-FIXTURE",
            "canonical_title": "Transient Resume Fixture",
            "pdf_start_page": 1,
            "pdf_end_page": 1,
            "grade": 7,
            "subject": "physics",
            "language": "en",
            "source_pdf_sha256": "source-hash-fixture",
            "source_key": "FIXTURE",
        }

        def exercise(n):
            prompt = f"Verified textbook exercise {n}: determine the documented result."
            return {
                "exercise_id": f"EX-{n}",
                "lesson_id": entry["lesson_id"],
                "section_type": "EXERCISE",
                "number": n,
                "source_page": 1,
                "exact_source_prompt": prompt,
                "source_prompt_hash": hashlib.sha256(prompt.encode()).hexdigest()[:16],
                "subquestions": [],
                "requires_figure": False,
                "figure_refs": [],
                "figure_hashes": [],
                "solution_mode": "PRE_SOLVED",
                "source_origin": "TEXTBOOK",
                "verified_against_source": True,
                "scope_concept_ids": ["C01"],
            }

        base_ev = {
            "book_id": entry["book_id"],
            "lesson_id": entry["lesson_id"],
            "pages_evidence": [{"page_num": 1, "text": "Verified law.", "figures": []}],
            "concepts": [{
                "concept_id": "C01",
                "title": "Verified law",
                "source_page": 1,
                "raw_text": "Verified law.",
                "normalized_text": "Verified law.",
            }],
            "exercise_evidence": [exercise(i) for i in range(1, 9)],
        }

        factory.assert_renderer_family_contract = lambda: None
        factory.resolve_source_book_pdf = lambda book_id, drive_service=None: pdf
        factory.resolve_pedagogy_profile = lambda e: {
            "subject": "physics", "grade": 7, "language": "en", "level": "L2"
        }
        factory.build_evidence_map = lambda *a, **k: copy.deepcopy(base_ev)
        factory.synthesize_universal_pedagogy = lambda *a, **k: {
            "activities": [], "worksheet": [], "quiz_items": [],
            "whole_lesson_lab_active": False,
        }
        factory.generate_ai_practice_for_insufficient_book_exercises = lambda *a, **k: []

        def labs(entry_arg, exercises_arg, profile, ev):
            for ex in exercises_arg:
                ex["_prebuilt_lab_key"] = f"exercise:{ex['exercise_id']}"
                ex["_prebuilt_lab_html"] = "<div>lab</div>"
                ex["_prebuilt_lab_active"] = True
        factory.prepare_prebuilt_exercise_labs = labs
        factory.build_prebuilt_lab_index = lambda *a, **k: {
            "schema": "fixture", "concept_labs": [], "exercise_labs": [],
        }
        factory.render_lesson_page_a = lambda *a, **k: "<html>A</html>"
        factory.render_lesson_page_b = lambda *a, **k: "<html>B</html>"
        factory.strip_source_rasters_from_student_html = lambda x, *a, **k: x
        factory.build_trilingual_page_translation = lambda html, *a, **k: (
            html, {"complete": True, "languages": ["ar", "en", "fr"]}
        )
        factory.run_all_quality_gates = lambda candidate: {"gates": []}
        factory.independent_scientific_review = lambda *a, **k: {"status": "PASS"}
        factory.persist_quality_gated_labs = lambda *a, **k: {
            "artifacts": [], "index": None
        }
        factory.resolve_drive_root_id = lambda: "ROOT"

        checkpoints.load_solution = lambda service, root_id, e, ex, **k: copy.deepcopy(
            solution_store.get(ex["exercise_id"])
        )
        def save_solution(service, root_id, e, ex, sol, **k):
            solution_store[ex["exercise_id"]] = copy.deepcopy(sol)
            return True
        checkpoints.save_solution = save_solution
        def save_state(service, root_id, e, state):
            state_store.append(copy.deepcopy(state))
            return copy.deepcopy(state)
        checkpoints.save_factory_state = save_state

        current_provenance = {
            "provider": "fake-provider",
            "model": "fake-503-model",
            "primary_provider": "fake-provider",
            "used_failover": False,
            "completed_at": "2026-10-09T00:00:00+00:00",
        }

        def fake_json(prompt, *, purpose="factory_json", **kwargs):
            if purpose.startswith("exercise_solution_audit_EX-"):
                return {
                    "keep_step_indexes": [0],
                    "final_answer_valid": True,
                    "final_answer_complete": True,
                    "figure_faithful": True,
                    "no_unrequested_actions": True,
                    "pruned_solution_valid": True,
                    "reasons": [],
                }
            if purpose.startswith("exercise_solution_EX-"):
                n = int(purpose.rsplit("-", 1)[1])
                calls[n] += 1
                if n == 7 and fail_once[7]:
                    fail_once[7] = False
                    raise RuntimeError(
                        "HTTP 503 Service Unavailable; retry after 1s")
                return {
                    "steps": [f"Verified step {n}"],
                    "final_answer": f"Verified answer {n}",
                }
            raise AssertionError("Unexpected LLM purpose: " + purpose)

        factory._execute_llm_json_strict = fake_json
        factory.get_last_llm_provenance = lambda: dict(current_provenance)

        fake_drive = object()

        try:
            factory.produce_lesson_for_entry(
                copy.deepcopy(entry), drive_service=fake_drive, publish=False)
            raise AssertionError("first run must pause on synthetic 503")
        except ProviderTransientError as exc:
            assert getattr(exc, "state", {}).get("status") == "PAUSED_TRANSIENT"
            assert getattr(exc, "state", {}).get("unit_id") == "EX-7"

        assert set(solution_store) == {f"EX-{i}" for i in range(1, 7)}
        assert state_store and state_store[-1]["status"] == "PAUSED_TRANSIENT"
        print("PASS real_pipeline_first_run_paused_at_unit_7")

        report = factory.produce_lesson_for_entry(
            copy.deepcopy(entry), drive_service=fake_drive, publish=False)
        assert report["status"] == "QA_PASSED_LOCAL"
        assert set(solution_store) == {f"EX-{i}" for i in range(1, 9)}
        assert all(calls[i] == 1 for i in range(1, 7)), calls
        assert calls[7] == 2, calls
        assert calls[8] == 1, calls
        print("PASS real_pipeline_resume_saved_units_not_rerequested")
        print("CALL_COUNTS", calls)

        original_main = factory.main
        try:
            err = ProviderTransientError(
                "503 fixture", retry_after_seconds=1, status_code=503)
            err.state = {"status": "PAUSED_TRANSIENT", "unit_id": "EX-7"}
            def raising_main():
                raise err
            factory.main = raising_main
            assert factory._cli_entry() == 75
        finally:
            factory.main = original_main
        print("PASS cli_transient_exit_75_no_traceback")

        # Real production-stage wrapper: a provider cooldown raised from inside
        # theory/lab synthesis must become PAUSED_TRANSIENT, not a traceback.
        original_synthesis = factory.synthesize_universal_pedagogy
        try:
            def cooling_synthesis(*args, **kwargs):
                inner = RuntimeError(
                    "AI_ALL_PROVIDERS_COOLING_DOWN: shortest_provider=groq "
                    "wait_seconds=62.0")
                raise RuntimeError(
                    "LAB_PIPELINE_FAILED:C01:LAB_SPEC_JSON_INVALID: "
                    + str(inner)) from inner
            factory.synthesize_universal_pedagogy = cooling_synthesis
            try:
                factory.produce_lesson_for_entry(
                    copy.deepcopy(entry), drive_service=fake_drive, publish=False)
                raise AssertionError("theory/lab cooldown must pause")
            except ProviderTransientError as exc:
                st = getattr(exc, "state", {})
                assert st.get("status") == "PAUSED_TRANSIENT", st
                assert st.get("unit_id") == "C01", st
                assert st.get("operation") == "theory_lab_synthesis", st
                assert st.get("retry_after_seconds") == 62, st
        finally:
            factory.synthesize_universal_pedagogy = original_synthesis
        print("PASS real_pipeline_theory_lab_cooldown_paused_no_traceback")

        print("NABIL_REAL_PRODUCE_LESSON_503_INTEGRATION_PASS")


if __name__ == "__main__":
    main()
