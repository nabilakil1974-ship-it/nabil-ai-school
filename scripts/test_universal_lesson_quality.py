"""Production incident regressions for generic lesson repair and visual routing."""
import unittest
from app.core.lesson_quality import (
    practice_exercise_numbers, missing_practice_exercises, drawing_matches_subject,
)


class UniversalLessonQualityTests(unittest.TestCase):
    def test_h3_chemistry_exercises_are_not_generated_twice(self):
        text = "\n".join(f"### Exercise {i}\n**Problem:** ...\n### Solution" for i in range(1, 6))
        self.assertEqual(practice_exercise_numbers(text), [1, 2, 3, 4, 5])
        self.assertEqual(missing_practice_exercises(text), [])

    def test_h2_h3_h4_french_arabic_exercises(self):
        text = "## Exercice 1\n### تمرين 2\n#### Exercise #3\n## Exercise 4\n### Exercise 5"
        self.assertEqual(missing_practice_exercises(text), [])

    def test_repair_only_missing_exercises(self):
        text = "## Exercise 1\n### Exercise 2\n#### Exercise 4"
        self.assertEqual(missing_practice_exercises(text), [3, 5])

    def test_prose_does_not_count_as_exercise(self):
        text = "We solved Exercise 1 above.\nThere are five exercises in this lesson."
        self.assertEqual(practice_exercise_numbers(text), [])

    def test_reject_function_graph_in_ionic_chemistry(self):
        self.assertFalse(drawing_matches_subject(
            {"type": "function", "function": "ln"}, "كيمياء", "Ionic Bond"
        ))
        self.assertFalse(drawing_matches_subject(
            {"type": "coordinate_plane"}, "Chemistry", "Ionic formation"
        ))
        self.assertTrue(drawing_matches_subject(
            {"type": "function"}, "رياضيات", "Study of function"
        ))
        self.assertTrue(drawing_matches_subject(
            {"type": "forces"}, "Physics", "Newton"
        ))
        self.assertTrue(drawing_matches_subject(
            {"type": "ionic_bond"}, "Chemistry", "Ionic Bond"
        ))


if __name__ == "__main__":
    unittest.main()
