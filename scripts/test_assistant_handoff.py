import json
import hashlib
import tempfile
import unittest
from pathlib import Path
from scripts.nabil_factory.assistant_handoff import (
    bind_source_verified_solutions, create_handoff,
    verify_deterministic_audit, verify_return)

class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.entry = {"lesson_id":"G07-MATHEMATICS-TEST-001",
            "book_id":"test-book", "grade":7, "subject":"mathematics",
            "language":"en","canonical_title":"Powers",
            "pdf_start_page":13, "pdf_end_page":18}
        self.evidence = {"concept_evidence":[{"id":"p13-c1","text":"2^3=8"}],
                         "exercise_evidence":[{"exercise_id":"p14-e1"}]}
    def test_export_is_grounded_and_has_source_hash(self):
        with tempfile.TemporaryDirectory() as d:
            job = create_handoff(self.entry, self.evidence, str(Path(d)/"job.json"))
            self.assertEqual(job["source_evidence"]["concept_evidence"][0]["id"],"p13-c1")
            self.assertEqual(len(job["input_sha256"]),64)
            self.assertEqual(json.loads((Path(d)/"job.json").read_text())["input_sha256"],job["input_sha256"])
    def test_real_evidence_map_keeps_pages_concepts_and_backlog(self):
        evidence = {"pages_evidence": [{"source_page": 13}],
                    "concepts": [{"concept_id": "C1", "raw_text": "2^3=8"}],
                    "exercise_evidence": self.evidence["exercise_evidence"],
                    "source_backlog": {"pending_count": 1}}
        with tempfile.TemporaryDirectory() as d:
            job = create_handoff(self.entry, evidence, str(Path(d)/"job.json"))
            self.assertEqual(job["source_evidence"]["source_pages"], evidence["pages_evidence"])
            self.assertEqual(job["source_evidence"]["concept_evidence"], evidence["concepts"])
            self.assertEqual(job["source_evidence"]["source_backlog"]["pending_count"], 1)

    def test_answer_pending_review_not_auto_accepted(self):
        with tempfile.TemporaryDirectory() as d:
            job=create_handoff(self.entry,self.evidence,str(Path(d)/"job.json"))
            result={"schema":"nabil.lesson.answer.v1",
                    "lesson_id":job["lesson_id"],"input_sha256":job["input_sha256"],
                    "teaching_steps":[{"concept_id":"p13-c1","text":"2 cubed is eight"}],
                    "exercise_solutions":[{"exercise_id":"p14-e1","steps":["2×2×2=8"],"final_answer":"8"}]}
            self.assertEqual(verify_return(job,result)["status"],"PENDING_INDEPENDENT_REVIEW")
            result["scientific_review"]="PASS"
            with self.assertRaises(ValueError):
                verify_return(job,result)
    def test_answer_rejects_incomplete_or_unknown_evidence_coverage(self):
        with tempfile.TemporaryDirectory() as d:
            job=create_handoff(self.entry,self.evidence,str(Path(d)/"job.json"))
            base={"schema":"nabil.lesson.answer.v1",
                  "lesson_id":job["lesson_id"],"input_sha256":job["input_sha256"],
                  "teaching_steps":[{"concept_id":"p13-c1","text":"grounded"}],
                  "exercise_solutions":[]}
            with self.assertRaisesRegex(ValueError,"EXERCISE_COVERAGE_MISMATCH"):
                verify_return(job,base)
            base["exercise_solutions"]=[{"exercise_id":"invented","steps":["x"],"final_answer":"x"}]
            with self.assertRaisesRegex(ValueError,"EXERCISE_COVERAGE_MISMATCH"):
                verify_return(job,base)

    def test_pipeline_has_drive_answer_readback_and_never_publishes_receipt(self):
        pipeline = (Path(__file__).parent / "nabil_factory" / "factory" / "pipeline.py").read_text(encoding="utf-8")
        self.assertIn("NABIL_HANDOFF_ANSWER_DRIVE_ID", pipeline)
        self.assertIn("HANDOFF_V18_EXPERIMENTAL_PREVIEW_CREATED", pipeline)
        self.assertIn('"published": False', pipeline)
    def test_pipeline_marks_owner_approved_experiment_unverified(self):
        pipeline = (Path(__file__).parent / "nabil_factory" / "factory" / "pipeline.py").read_text(encoding="utf-8")
        self.assertIn(
            'candidate["review_status"] = "INDEPENDENT_REVIEW_DISABLED_BY_OWNER"',
            pipeline)
        self.assertIn('candidate["publication_unverified"] = True', pipeline)
        self.assertIn('status_str = "PUBLISHED_UNVERIFIED"', pipeline)

    def test_unverified_release_is_not_routed_to_golden_folder(self):
        delivery = (Path(__file__).parent / "nabil_factory" / "drive_runtime" /
                    "core.py").read_text(encoding="utf-8")
        self.assertIn("unverified_release", delivery)
        self.assertIn('"nabil_golden": "false" if unverified_release', delivery)

    def test_stale_source_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            job=create_handoff(self.entry,self.evidence,str(Path(d)/"job.json"))
            with self.assertRaises(ValueError):
                verify_return(job,{"schema":"nabil.lesson.answer.v1",
                    "lesson_id":job["lesson_id"],"input_sha256":"stale",
                    "teaching_steps":[],"exercise_solutions":[]})

    def test_verified_solution_binding_requires_exact_source_hash_and_page(self):
        exercises=[{"exercise_id":"E1","source_prompt_hash":"abc",
                    "source_page":22,"solution_mode":"PRE_SOLVED"}]
        solutions=[{"exercise_id":"E1","source_prompt_hash":"abc",
                    "source_page":22,"steps":["2×2×2=8"],
                    "final_answer":"8"}]
        bind_source_verified_solutions(exercises, solutions)
        self.assertEqual(exercises[0]["solution_status"], "SOLVED")
        self.assertTrue(
            exercises[0]["_pre_solved_solution"]["source_scope_audited"])
        self.assertEqual(
            exercises[0]["_pre_solved_solution"]["independent_scientific_review"],
            "NOT_RUN")
        bad=[dict(solutions[0], source_prompt_hash="stale")]
        with self.assertRaisesRegex(ValueError, "SOURCE_PROMPT_HASH_MISMATCH"):
            bind_source_verified_solutions([dict(exercises[0])], bad)

    def test_pipeline_uses_imported_solutions_without_external_solver(self):
        pipeline = (Path(__file__).parent / "nabil_factory" / "factory" /
                    "pipeline.py").read_text(encoding="utf-8")
        bind = "bind_source_verified_solutions("
        solve = "prepare_verified_solutions("
        self.assertIn(bind, pipeline)
        self.assertLess(pipeline.index(bind), pipeline.index(solve))

    def test_deterministic_audit_is_hash_bound_and_not_independent(self):
        answer={"lesson_id":"L1","input_sha256":"input"}
        raw=json.dumps(answer,sort_keys=True).encode()
        audit={"schema":"nabil.lesson.answer.audit.v1","lesson_id":"L1",
               "answer_drive_id":"A1",
               "answer_sha256":hashlib.sha256(raw).hexdigest(),
               "input_sha256":"input","passed":True,
               "audit_type":"DETERMINISTIC_SELF_CHECK_NOT_INDEPENDENT_REVIEW",
               "checks":[{"check":"coverage","passed":True}],
               "independent_scientific_review":"NOT_RUN"}
        receipt=verify_deterministic_audit(raw,answer,audit,"A1")
        self.assertEqual(receipt["status"],"PASS")
        self.assertEqual(receipt["independent_scientific_review"],"NOT_RUN")
        with self.assertRaisesRegex(ValueError,"ANSWER_SHA256_MISMATCH"):
            verify_deterministic_audit(raw+b"x",answer,audit,"A1")
if __name__=="__main__": unittest.main()
