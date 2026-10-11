import unittest

from scripts.nabil_factory.answer_preview import (
    _concept_activities, _exercise_records, _page)


class AnswerPreviewTests(unittest.TestCase):
    def test_maps_exact_ids_and_keeps_preview_blocked(self):
        job={"input_sha256":"abc","source_evidence":{"exercise_evidence":[{
            "exercise_id":"E1","number":1,"exact_source_prompt":"2³",
            "source_page":20}]}}
        answer={"teaching_steps":[{"concept_id":"C1","title":"Power",
                                  "text":"2³ is a repeated product.",
                                  "student_prompts":["Expand it."],
                                  "conclusion":"2³=8"}],
                "exercise_solutions":[{"exercise_id":"E1",
                                       "steps":["2×2×2"],
                                       "final_answer":"8"}]}
        acts=_concept_activities(answer)
        exercises=_exercise_records(job,answer)
        self.assertEqual(["C1"],[x["concept_id"] for x in acts])
        self.assertEqual("E1",exercises[0]["exercise_id"])
        self.assertEqual("SOLVED",exercises[0]["solution_status"])
        page=_page("Powers","<div>board</div>","theory","abc")
        self.assertIn('data-publication-status="BLOCKED"',page)
        self.assertIn('data-review-status="PENDING_INDEPENDENT_REVIEW"',page)


if __name__ == "__main__":
    unittest.main()
