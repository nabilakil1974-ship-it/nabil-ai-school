"""P0 #58: verified full-work solution must survive board AND final Golden card.
No source PDFs, AI API, or Google Drive requests in this test.
"""
import unittest
from scripts.nabil_factory.cards.v18_board import build_exercise_activities, build_golden_spec, build_slide

class CompleteExerciseGoldenTest(unittest.TestCase):
    def test_solution_is_teaching_not_a_single_number(self):
        source = [{
            "exercise_id": "QA-POWERS", "number": 1,
            "exact_source_prompt": "Write 2^3 as repeated multiplication.",
            "solution_status": "SOLVED",
            "_prebuilt_lab_html": "<p>FAKE_DUPLICATE_LAB</p>",
            "_pre_solved_solution": {
                "steps": ["2^3 means three factors of 2", "2 × 2 × 2 = 8"],
                "final_answer": "2^3 = 8",
            },
        }]
        labels = {"problem":"Problem", "step":"Step", "final":"Conclusion",
                  "exercise":"Exercise"}
        acts=build_exercise_activities(source,labels)
        self.assertEqual(len(acts),1)
        self.assertFalse(acts[0]["lab_html"])
        slide=build_slide(acts[0],"en")
        self.assertGreaterEqual(len(slide["steps"]),4)
        self.assertEqual(slide["steps"][0]["kind"],"problem")
        golden=build_golden_spec("Powers",acts,"en",subject="mathematics")
        items=golden["sections"][0]["items"]
        self.assertEqual(len(items),len(acts[0]["teaching_steps"]))
        self.assertTrue(any("factors of 2" in x for x in items))
        self.assertTrue(any("2 × 2 × 2" in x for x in items))
        self.assertNotEqual(items,["2³ = 8"])

    def test_unverified_exercise_not_taught_as_solved(self):
        invalid={"exercise_id":"UNVERIFIED","number":2,
                 "exact_source_prompt":"Explain 2^4 without computing",
                 "solution_status":"REJECTED",
                 "_pre_solved_solution":{"steps":["unverified"],"final_answer":"16"}}
        self.assertEqual(build_exercise_activities([invalid],{"exercise":"Exercise"}),[])

if __name__=="__main__":
    unittest.main()
