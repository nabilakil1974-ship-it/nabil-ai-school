import copy
import unittest

from scripts.nabil_factory.source_candidate import apply_source_candidate


class SourceCandidateTests(unittest.TestCase):
    def setUp(self):
        self.entry = {
            "lesson_id": "G07-MATHEMATICS-69B7C840-001",
            "book_id": "book",
            "pdf_start_page": 15,
            "pdf_end_page": 23,
            "source_pdf_sha256": "abc",
        }
        self.candidate = {
            "schema": "nabil.lesson.handoff.v2",
            "lesson_id": self.entry["lesson_id"],
            "book_id": "book",
            "source_pdf_sha256": "abc",
            "source_pages": [15, 23],
            "input_sha256": "candidate-hash",
            "status": "SOURCE_COMPLETE_CANDIDATE_PENDING_INDEPENDENT_REVIEW",
            "source_evidence": {
                "exercise_evidence": [{
                    "exercise_id": "ex-1",
                    "source_page": 20,
                    "printed_page": 18,
                    "exact_source_prompt": "Compute 2^3.",
                    "source_prompt_hash": "prompt-hash",
                    "source_origin": "TEXTBOOK",
                    "verified_against_source": True,
                }],
                "source_backlog": {"pending_count": 0, "pending": []},
                "source_completeness": {
                    "source_inventory_candidate_complete": True,
                    "exercise_group_count": 1,
                    "independent_review": "NOT_RUN",
                    "passed": False,
                    "blocking": True,
                },
            },
        }

    def test_import_replaces_bad_ocr_inventory_but_stays_blocked(self):
        repaired = apply_source_candidate(
            self.entry, {"exercise_evidence": [{"exercise_id": "wrong"}]},
            self.candidate)
        self.assertEqual([row["exercise_id"] for row in repaired["exercise_evidence"]], ["ex-1"])
        self.assertTrue(repaired["source_completeness"]["blocking"])
        self.assertFalse(repaired["source_candidate"]["publication_allowed"])
        self.assertEqual(repaired["source_candidate"]["independent_review"], "NOT_RUN")

    def test_rejects_stale_pdf_wrong_pages_duplicates_and_false_review(self):
        for mutate, error in (
            (lambda c: c.update(source_pdf_sha256="stale"), "PDF_FINGERPRINT"),
            (lambda c: c.update(source_pages=[14, 23]), "PAGE_RANGE"),
            (lambda c: c["source_evidence"]["exercise_evidence"].append(
                copy.deepcopy(c["source_evidence"]["exercise_evidence"][0])), "DUPLICATED"),
            (lambda c: c["source_evidence"]["source_completeness"].update(
                independent_review="PASS"), "REVIEW_STATUS"),
        ):
            candidate = copy.deepcopy(self.candidate)
            mutate(candidate)
            with self.assertRaisesRegex(ValueError, error):
                apply_source_candidate(self.entry, {}, candidate)

    def test_pipeline_reads_candidate_before_handoff_export(self):
        from pathlib import Path
        pipeline = (Path(__file__).parent / "nabil_factory" / "factory" / "pipeline.py").read_text()
        imported = pipeline.index("SOURCE_CANDIDATE_IMPORTED_PENDING_INDEPENDENT_REVIEW")
        handoff = pipeline.index("HANDOFF_WAITING_FOR_ASSISTANT")
        self.assertLess(imported, handoff)
        self.assertIn("NABIL_SOURCE_CANDIDATE_DRIVE_ID", pipeline)


if __name__ == "__main__":
    unittest.main()
