"""Fast offline regression for science progress summary (no DB/Drive/OCR)."""
import unittest
from scripts.science_progress_summary import summarize, summary_line


class ScienceProgressSummaryTest(unittest.TestCase):
    def test_known_total_and_in_progress(self):
        stats = summarize([(152, 152, True), (87, 394, False), (0, 0, False)])
        self.assertEqual(stats["mappings"], 3)
        self.assertEqual(stats["complete"], 1)
        self.assertEqual(stats["started"], 2)
        self.assertEqual(stats["done_pages"], 239)
        self.assertEqual(stats["known_pages"], 546)
        self.assertEqual(stats["remaining_known_pages"], 307)
        self.assertIn("307 pages remaining", summary_line(stats))

    def test_unknown_totals_not_counted_complete(self):
        stats = summarize([(0, 0, False), (0, 0, False)])
        self.assertEqual(stats["complete"], 0)
        self.assertIsNone(stats["percent_known_pages"])
        self.assertIn("(unknown)", summary_line(stats))

    def test_clamp_corrupted_done_count(self):
        stats = summarize([(999, 152, True)])
        self.assertEqual(stats["done_pages"], 152)
        self.assertEqual(stats["remaining_known_pages"], 0)


if __name__ == "__main__":
    unittest.main()
