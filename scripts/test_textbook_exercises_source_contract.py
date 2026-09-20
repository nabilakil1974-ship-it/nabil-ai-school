"""Integration source-contract checks for official-book exercise priority.

Text inspection is NOT an end-to-end test of the database or deployed lesson.
It prevents accidental restoration of mandatory fabricated practice in the
source-grounded lesson path.
"""
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class OfficialBookExerciseContract(unittest.TestCase):
    def test_book_page_exercise_lookup_is_scoped(self):
        code=(ROOT/"app/services/rag_search.py").read_text(encoding="utf-8")
        for clause in (
            "BookChunk.book_id == book_id",
            "BookChunk.grade == grade",
            "BookChunk.subject == subject",
            "BookChunk.curriculum == curriculum",
            "BookChunk.printed_page_number <= first_page + max_distance_pages",
        ):
            with self.subTest(clause=clause):
                self.assertIn(clause, code)

    def test_book_sources_win_over_generated_practice(self):
        code=(ROOT/"app/api/routes_chat.py").read_text(encoding="utf-8")
        self.assertIn("book_exercise_chunks = find_nearest_book_exercises(",code)
        self.assertIn('"[VERIFIED BOOK EXERCISES] "',code)
        self.assertIn("and not lesson_start_from_book  # textbook exercises",code)
        self.assertIn("Only if official exercises were not retrieved",code)

if __name__=="__main__":
    unittest.main()
