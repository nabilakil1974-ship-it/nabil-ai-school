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
    def test_answer_pending_review_not_auto_accepted(self):
        with tempfile.TemporaryDirectory() as d:
            job=create_handoff(self.entry,self.evidence,str(Path(d)/"job.json"))
            result={"schema":"nabil.lesson.answer.v1",
                    "lesson_id":job["lesson_id"],"input_sha256":job["input_sha256"],
                    "teaching_steps":[{"text":"2 cubed is eight"}],
                    "exercise_solutions":[{"exercise_id":"p14-e1","answer":"8"}]}
            self.assertEqual(verify_return(job,result)["status"],"PENDING_INDEPENDENT_REVIEW")
            result["scientific_review"]="PASS"
            with self.assertRaises(ValueError):
                verify_return(job,result)
    def test_stale_source_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            job=create_handoff(self.entry,self.evidence,str(Path(d)/"job.json"))
            with self.assertRaises(ValueError):
                verify_return(job,{"schema":"nabil.lesson.answer.v1",
                    "lesson_id":job["lesson_id"],"input_sha256":"stale",
                    "teaching_steps":[],"exercise_solutions":[]})
if __name__=="__main__": unittest.main()
