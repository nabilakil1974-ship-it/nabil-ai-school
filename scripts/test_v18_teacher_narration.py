"""Narration contract: verified reasoning is shown as grounded, with NO canned filler and real math notation."""
import unittest
from scripts.nabil_factory.cards.v18_board import (
    teaching_sentence, build_slide, build_exercise_activities, build_golden_spec,
)
FILLER = ("We now explain", "Let us begin and explain", "We conclude from the steps",
          "Read the question and identify", "نقرأ نصّ السؤال", "ننتقل الآن إلى الخطوة", "Expliquons maintenant")
class TutorNarrationContract(unittest.TestCase):
    def test_no_canned_filler_in_any_language(self):
        for locale in ("ar", "en", "fr"):
            for kind, pos in (("problem", 0), ("step", 1), ("step", 2), ("final", 3)):
                a = teaching_sentence("x = 3 + 4", kind, locale, pos)
                self.assertEqual(a, "x = 3 + 4")
                self.assertFalse(any(f in a for f in FILLER))
    def test_math_is_canonical_not_raw(self):
        a = teaching_sentence("For (2^3)^4, apply 2^(3 * 4) = 2^12", "step", "en", 2)
        self.assertNotIn("*", a)
        self.assertIn("2^{3 × 4}", a)
        self.assertNotIn("^(", a)
    def test_one_same_explanation_on_board_and_golden_card(self):
        ex = {"number": 1, "exercise_id": "QA", "exact_source_prompt": "Write 2^3 as repeated multiplication",
              "solution_status": "SOLVED", "_pre_solved_solution": {
                  "steps": ["2^3 means three factors of 2", "2 × 2 × 2 = 8"], "final_answer": "8"}}
        acts = build_exercise_activities([ex], {"problem": "المسألة", "step": "الخطوة",
                                                "final": "الجواب", "exercise": "التمرين"})
        board = build_slide(acts[0], "ar")
        card = build_golden_spec("الأسس", acts, "ar", subject="mathematics")
        board_lines = [x["text"] for x in board["steps"]]
        self.assertEqual(board_lines, card["sections"][0]["items"])
        self.assertFalse(any(f in l for l in board_lines for f in FILLER))
        self.assertIn("2 × 2 × 2 = 8", " ".join(board_lines))
if __name__ == "__main__":
    unittest.main()
