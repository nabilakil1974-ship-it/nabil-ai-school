"""Regression checks against the actual Ionic Bond failure observed on Railway."""
import unittest
from app.core.lesson_output_guard import sanitize_chemistry_lesson


class ChemistryLessonOutputGuardTests(unittest.TestCase):
    def test_oxide_has_ten_electrons_not_eighteen(self):
        source = "O²⁻ (arrangement 2,8,8) and Mg²⁺ (arrangement 2,8)"
        self.assertEqual(
            sanitize_chemistry_lesson(source, "كيمياء"),
            "O²⁻ (arrangement 2,8) and Mg²⁺ (arrangement 2,8)",
        )

    def test_bad_drawing_protocol_not_visible_to_learner(self):
        source = (
            "Ionic Bond\\n```DRAWING_JSON{invalid, atoms: []}```\\n"
            "Opposite charges attract."
        ).replace("\\n", "\n")
        actual = sanitize_chemistry_lesson(source, "Chemistry")
        self.assertNotIn("DRAWING_JSON", actual)
        self.assertIn("Opposite charges attract.", actual)

    def test_science_math_insert_removed_but_lesson_retained(self):
        source = (
            "Ionic Bond\\nDomain(0,∞)Limits lim x→0 = -∞ "
            "Derivative f'(x) = 0\\nBoard Lesson: Ionic Bond\\n"
            "Na⁺ and Cl⁻ attract."
        ).replace("\\n", "\n")
        actual = sanitize_chemistry_lesson(source, "Chemistry")
        self.assertNotIn("Derivative", actual)
        self.assertIn("Board Lesson: Ionic Bond", actual)
        self.assertIn("Na⁺ and Cl⁻", actual)

    def test_never_transform_math_lesson(self):
        source = "Domain(0,∞)Limits\\nBoard Lesson: f(x)\\nO²⁻ (arrangement 2,8,8)"
        self.assertEqual(sanitize_chemistry_lesson(source, "Mathematics"), source)

    def test_never_mutate_neutral_oxygen(self):
        source = "O (arrangement 2,6); O²⁻ (arrangement 2,8)"
        self.assertEqual(sanitize_chemistry_lesson(source, "Chemistry"), source)


if __name__ == "__main__":
    unittest.main()
