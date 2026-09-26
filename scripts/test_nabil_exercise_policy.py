import unittest

from scripts.nabil_lesson_factory import required_ai_practice_count


class ExerciseSupplementPolicyTest(unittest.TestCase):
    def test_zero_textbook_exercises_get_two_ai(self):
        self.assertEqual(required_ai_practice_count(0), 2)

    def test_one_textbook_exercise_gets_three_ai(self):
        self.assertEqual(required_ai_practice_count(1), 3)
        self.assertEqual(1 + required_ai_practice_count(1), 4)

    def test_two_or_more_textbook_exercises_get_no_ai(self):
        for count in (2, 3, 9, 20):
            with self.subTest(count=count):
                self.assertEqual(required_ai_practice_count(count), 0)


if __name__ == "__main__":
    unittest.main()
