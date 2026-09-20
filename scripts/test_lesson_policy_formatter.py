"""Reproduce the Railway crash without importing production database or AI providers.

Run: python -m scripts.test_lesson_policy_formatter
"""
import ast
from pathlib import Path
import unittest
from typing import Optional


ROOT = Path(__file__).resolve().parents[1]
ROUTE = ROOT / "app" / "api" / "routes_chat.py"


class LessonPolicyFormatterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        tree = ast.parse(ROUTE.read_text(encoding="utf-8"), filename=str(ROUTE))
        matches = [
            node for node in tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name == "format_lesson_policy_for_prompt"
        ]
        if len(matches) != 1:
            raise AssertionError("The lesson route MUST define its policy formatter exactly once")
        module = ast.fix_missing_locations(ast.Module(body=matches, type_ignores=[]))
        namespace = {"Optional": Optional}
        exec(compile(module, str(ROUTE), "exec"), namespace)
        cls.formatter = staticmethod(namespace["format_lesson_policy_for_prompt"])

    def test_english_grade_9_ionic_bond_does_not_crash(self):
        actual = self.formatter({
            "title": "Ionic bond", "language": "English",
            "grade": "الصف التاسع", "subject": "كيمياء", "status": "verified",
        })
        self.assertIn("Ionic bond", actual)
        self.assertIn("English", actual)
        self.assertIn("الصف التاسع", actual)
        self.assertIn("retrieved textbook passages", actual)

    def test_missing_or_invalid_metadata_never_raises(self):
        for value in (None, {}, [], "", 7):
            with self.subTest(value=value):
                actual = self.formatter(value)
                self.assertTrue(isinstance(actual, str) and actual.strip())

    def test_never_invents_a_source_page_or_exercise(self):
        actual = self.formatter({"title": "Ionic bond", "language": "English"})
        self.assertNotIn("p. 1", actual)
        self.assertNotIn("Exercise 1", actual)


if __name__ == "__main__":
    unittest.main(verbosity=2)
