import json
import tempfile
import unittest
from pathlib import Path
from scripts.nabil_factory.assistant_handoff import create_handoff, verify_return

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
        self.assertIn("HANDOFF_ANSWER_STRUCTURALLY_VERIFIED_AWAITING_INDEPENDENT_REVIEW", pipeline)
        self.assertIn('"published": False', pipeline)
    def test_pipeline_fails_closed_without_independent_review(self):
        pipeline = (Path(__file__).parent / "nabil_factory" / "factory" / "pipeline.py").read_text(encoding="utf-8")
        gate = 'if candidate["needs_review"] or candidate["review_status"] != "REVIEWED":'
        freeze = "published_labs = persist_quality_gated_labs(entry, theory, exercises)"
        publish = "if publish:"
        self.assertIn(gate, pipeline)
        self.assertIn("INDEPENDENT_SCIENTIFIC_REVIEW_REQUIRED", pipeline)
        self.assertLess(pipeline.index(gate), pipeline.index(freeze))
        self.assertLess(pipeline.index(gate), pipeline.index(publish))

    def test_stale_source_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            job=create_handoff(self.entry,self.evidence,str(Path(d)/"job.json"))
            with self.assertRaises(ValueError):
                verify_return(job,{"schema":"nabil.lesson.answer.v1",
                    "lesson_id":job["lesson_id"],"input_sha256":"stale",
                    "teaching_steps":[],"exercise_solutions":[]})
if __name__=="__main__": unittest.main()
