"""P0 pedagogical narration: verified reasoning stays intact in same board and Golden card."""
import unittest
from scripts.nabil_factory.cards.v18_board import (
    teaching_sentence, build_slide, build_exercise_activities, build_golden_spec,
)
class TutorNarrationContract(unittest.TestCase):
    def test_fusha_on_one_line_preserves_source(self):
        a=teaching_sentence("2 × 2 × 2 = 8","step","ar",2)
        self.assertTrue(a.startswith("ننتقل الآن إلى الخطوة التالية"))
        self.assertIn("2 × 2 × 2 = 8",a)
        self.assertNotIn("\\n",a)
        self.assertTrue(teaching_sentence("ما المطلوب؟","problem","ar").startswith("نقرأ نصّ السؤال"))
    def test_three_languages(self):
        for locale in ("ar","en","fr"):
            a=teaching_sentence("x = 3 + 4","step",locale,1)
            self.assertIn("x = 3 + 4",a)
    def test_one_same_explanation_on_board_and_golden_card(self):
        ex={"number":1,"exercise_id":"QA","exact_source_prompt":"Write 2^3 as repeated multiplication",
            "solution_status":"SOLVED","_pre_solved_solution":{
                "steps":["2^3 means three factors of 2","2 × 2 × 2 = 8"],
                "final_answer":"8"}}
        acts=build_exercise_activities([ex],{"problem":"المسألة","step":"الخطوة",
                                       "final":"الجواب","exercise":"التمرين"})
        board=build_slide(acts[0],"ar")
        card=build_golden_spec("الأسس",acts,"ar",subject="mathematics")
        board_lines=[x["text"] for x in board["steps"]]
        self.assertEqual(board_lines,card["sections"][0]["items"])
        self.assertTrue(all("\\n" not in x for x in board_lines))
        self.assertTrue(board_lines[0].startswith("نقرأ"))
        self.assertTrue(board_lines[-1].startswith("نستنتج"))
        self.assertIn("2 × 2 × 2 = 8"," ".join(board_lines))
if __name__=="__main__":unittest.main()
