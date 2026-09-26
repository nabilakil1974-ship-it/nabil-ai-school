import unittest

from scripts.nabil_lesson_factory import (
    _normalize_exercise_review_payload,
    _normalize_exercise_scan_payload,
)


class ExerciseVisionSchemaTest(unittest.TestCase):
    def test_scan_array_root(self):
        rows = [{"number": 1}]
        self.assertEqual(_normalize_exercise_scan_payload(rows, 18), rows)

    def test_scan_wrapped_root(self):
        rows = [{"number": 1}, {"number": 2}]
        self.assertEqual(
            _normalize_exercise_scan_payload({"exercises": rows}, 18), rows)

    def test_review_array_root(self):
        checks = [{"number": 1, "faithful": True}]
        self.assertEqual(
            _normalize_exercise_review_payload(checks, 18), checks)

    def test_review_wrapped_root(self):
        checks = [{"number": 1, "faithful": True}]
        self.assertEqual(
            _normalize_exercise_review_payload({"checks": checks}, 18), checks)

    def test_invalid_shape_fails_closed(self):
        with self.assertRaises(RuntimeError):
            _normalize_exercise_scan_payload({"unexpected": "value"}, 18)
        with self.assertRaises(RuntimeError):
            _normalize_exercise_review_payload({"unexpected": "value"}, 18)


if __name__ == "__main__":
    unittest.main()
