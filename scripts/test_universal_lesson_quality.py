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

    def test_reject_function_figures_in_all_unrelated_subjects(self):
        for subject, lesson in (
            ("Chemistry", "Ionic Bond"),
            ("Physics", "Electricity"),
            ("Biology", "Mitosis"),
            ("Geography", "Climate"),
            ("History", "Ancient Civilizations"),
            ("English", "Grammar"),
            ("رياضيات", "Pythagoras"),
            ("Math", "Lines and Circles"),
            ("Mathematics", "Statistics"),
        ):
            with self.subTest(subject=subject, lesson=lesson):
                self.assertFalse(drawing_matches_subject(
                    {"type": "function", "expression": "ln(x)"},
                    subject, lesson, "Begin the selected lesson",
                ))
                self.assertFalse(drawing_matches_subject(
                    {"type": "coordinate_plane", "expression": "ln(x)"},
                    subject, lesson, "Begin the selected lesson",
                ))

    def test_explicit_function_questions_and_chapters_keep_their_graphs(self):
        plot = {"type": "function", "expression": "ln(x)"}
        self.assertTrue(drawing_matches_subject(
            plot, "Mathematics", "Functions", "Begin the selected lesson"
        ))
        self.assertTrue(drawing_matches_subject(
            plot, "", "", "Study the function f(x)=ln(x)"
        ))
        self.assertTrue(drawing_matches_subject(
            plot, "رياضيات", "دراسة الدالة", "ابدأ الدرس المحدد"
        ))

    def test_nonfunction_valid_diagrams_remain_supported(self):
        self.assertTrue(drawing_matches_subject(
            {"type": "coordinate_plane", "points": [{"x": 1, "y": 2}]},
            "Physics", "Motion and velocity", "Draw velocity graph"
        ))
        self.assertTrue(drawing_matches_subject(
            {"type": "ionic_bond"}, "Chemistry", "Ionic Bond"
        ))
        self.assertTrue(drawing_matches_subject(
            {"type": "right_triangle"}, "Math", "Pythagoras"
        ))


if __name__ == "__main__":
    unittest.main()
