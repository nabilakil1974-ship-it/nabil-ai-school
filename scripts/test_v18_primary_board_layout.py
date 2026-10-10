"""Reject old main layout: one full-width V18 teacher board is the PRIMARY lesson and exercise view."""
from pathlib import Path
import unittest
from scripts.nabil_factory.cards.v18_board import render_v18_smart_board

class PrimaryBoardContract(unittest.TestCase):
    def test_theory_and_exercises_have_same_primary_teacher_board(self):
        activity={"concept_id":"C01","title":"Powers","allow_no_lab":True,
          "teaching_steps":[{"label":"See","sentence":"2 × 2 × 2"},
                            {"label":"Conclude","sentence":"2³ = 8"}],
          "conclusion":"2³ = 8"}
        for mode in ("lesson","exercises"):
            with self.subTest(mode=mode):
                html=render_v18_smart_board("Powers",[activity],"en",mode=mode)
                self.assertIn('id="nabilWholeLessonSmartLab"',html)
                self.assertIn('id="v18Lines"',html)
                self.assertIn('grid-template-columns:minmax(0,1fr) minmax(0,1fr)',html)
                self.assertIn('grid-column:1/-1;grid-row:1',html)
    def test_source_pages_put_board_before_old_cards(self):
        source=Path("scripts/nabil_factory/cards/core.py").read_text()
        self.assertIn('  {theory.get("whole_lesson_lab_html", "")}\n  <details class="nabil-legacy-material"',source)
        self.assertIn('  {v18_exercises_board}\n  <details class="nabil-legacy-material"',source)
        self.assertEqual(source.count('  {theory.get("whole_lesson_lab_html", "")}'),1)

if __name__=="__main__":
    unittest.main()
