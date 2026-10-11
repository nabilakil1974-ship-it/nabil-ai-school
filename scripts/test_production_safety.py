import ast
import os
from pathlib import Path
import unittest
from unittest.mock import Mock, patch
from scripts.nabil_factory.coverage_gate import require_textbook_coverage


class ProductionSafetyTests(unittest.TestCase):
    def test_missing_book_exercise_cannot_be_replaced_by_extra_practice(self):
        expected = [{"exercise_id": "a"}, {"exercise_id": "b"}]
        actual = [{"exercise_id": "a"}, {"exercise_id": "extra",
                   "source_origin": "AI_ADDITIONAL_PRACTICE"}]
        with self.assertRaisesRegex(RuntimeError, "COVERAGE_INCOMPLETE"):
            require_textbook_coverage(expected, actual, "solutions")

    def test_rendered_set_must_keep_every_original_exercise(self):
        rows = [{"exercise_id": "a"}, {"exercise_id": "b"}]
        require_textbook_coverage(rows, list(reversed(rows)), "rendered_labs")
        with self.assertRaisesRegex(RuntimeError, "COVERAGE_INCOMPLETE"):
            require_textbook_coverage(rows, rows[:1], "rendered_labs")

    def test_duplicate_id_cannot_mask_coverage_loss(self):
        with self.assertRaisesRegex(RuntimeError, "DUPLICATED"):
            require_textbook_coverage([{"exercise_id": "a"}],
                                     [{"exercise_id": "a"}] * 2, "solutions")

    def test_external_ai_disabled_before_provider_lookup(self):
        # Execute the real production entry function without importing optional
        # factory dependencies. This exercises its control flow, not a copy.
        path = Path(__file__).parent / "nabil_factory/factory/providers.py"
        tree = ast.parse(path.read_text())
        fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                  and n.name == "execute_llm_completion")
        module = ast.Module(body=[ast.ImportFrom(module="__future__",
                            names=[ast.alias(name="annotations")], level=0), fn],
                            type_ignores=[])
        keys = Mock(side_effect=AssertionError("provider lookup must not run"))
        namespace = {"os": os, "_provider_keys": keys}
        exec(compile(ast.fix_missing_locations(module), str(path), "exec"), namespace)
        with patch.dict(os.environ, {"NABIL_NO_EXTERNAL_AI": "1"}):
            with self.assertRaisesRegex(RuntimeError, "EXTERNAL_AI_DISABLED"):
                namespace["execute_llm_completion"]("test", operation="qa")
        keys.assert_not_called()


if __name__ == "__main__":
    unittest.main()
