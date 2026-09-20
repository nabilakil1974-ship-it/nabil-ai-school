"""Function-study output must never contaminate unrelated subjects or grades."""
import unittest
from app.core.subject_output_guard import (
    sanitize_unrelated_function_study, permits_complete_function_study,
)


class FunctionStudyRoutingTests(unittest.TestCase):
    def test_secondary_math_only(self):
        self.assertTrue(permits_complete_function_study(
            "رياضيات", "الأول ثانوي", "Study of Functions", "ابدأ الدرس المحدد"
        ))
        self.assertTrue(permits_complete_function_study(
            "Mathematics", "Grade 12", "Functions", "Study the function f(x)=ln(x)"
        ))
        for subject, grade, lesson in (
            ("كيمياء", "الصف التاسع", "Ionic bond"),
            ("Physics", "Grade 12", "Motion"),
            ("Mathematics", "الصف التاسع", "Lines and Circles"),
            ("Mathematics", "Grade 11", "Geometry"),
            ("Biology", "Grade 12", "Cells"),
            ("Mathematics", "Grade 7", "Functions"),
        ):
            with self.subTest(subject=subject, grade=grade):
                self.assertFalse(permits_complete_function_study(
                    subject, grade, lesson, "Begin the selected lesson"
                ))

    def test_inline_ionic_math_pollution_removed_preserve_summary(self):
        data = (
            "## Lesson Summary\\nIons attract. Domain(0,∞)Limits lim x→0 "
            "Asymptotes y=0 Derivative f'(x)=bogus "
            "Let's complete our lesson on ionic bonding.\\n"
            "## Final Card\\nCharge balance."
        ).replace("\\n", "\n")
        answer = sanitize_unrelated_function_study(
            data, "Chemistry", "Ionic Bond", "Begin the selected lesson",
            "الصف التاسع"
        )
        self.assertIn("Ions attract.", answer)
        self.assertNotIn("Domain(0", answer)
        self.assertNotIn("Derivative", answer)
        self.assertIn("Final Card", answer)

    def test_secondary_math_preserves_calculus(self):
        data = "Domain(0,∞)Limits at 0 Asymptotes x=0 Derivative f'(x)"
        self.assertEqual(sanitize_unrelated_function_study(
            data, "Mathematics", "Functions", "Study the function f(x)=ln(x)",
            "Grade 12"
        ), data)

    def test_unrelated_domain_words_not_removed(self):
        data = "The domain of the school website is example.edu. Physics has limits."
        self.assertEqual(sanitize_unrelated_function_study(
            data, "English", "Reading", "What is a domain?", "Grade 9"
        ), data)


if __name__ == "__main__":
    unittest.main()
