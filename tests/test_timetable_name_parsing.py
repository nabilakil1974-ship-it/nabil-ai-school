"""Regression tests for Arabic teacher-name extraction."""
import unittest
from app.local_timetable_intake import _extract_teacher_segments


class TeacherNameParsing(unittest.TestCase):
    def test_trailing_preposition_is_not_part_of_teacher_name(self):
        rows = _extract_teacher_segments("الأستاذ خالد إلى بيدرس رياضيات للسابع أ")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], "خالد")
        self.assertIn("رياضيات", rows[0][1])

    def test_real_two_word_name_is_preserved(self):
        rows = _extract_teacher_segments("الأستاذ خالد علي بيدرس رياضيات للسابع أ")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], "خالد علي")


if __name__ == "__main__":
    unittest.main(verbosity=2)
