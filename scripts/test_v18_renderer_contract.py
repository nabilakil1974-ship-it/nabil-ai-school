"""V18 HTML contract: test the actual standalone renderer, not retired V17 hooks."""
import unittest
from scripts.nabil_factory.v18_editable.renderer import render_v18_lesson


def fixture():
    entry = {
        "lesson_id": "G07-MATHEMATICS-69B7C840-001",
        "canonical_title": "Powers",
        "language": "en",
        "grade": 7,
        "subject": "mathematics",
        "book_id": "source",
    }
    theory = {
        "activities": [{
            "concept_id": "C01",
            "title": "Powers",
            "teaching_steps": [{
                "label": "See",
                "sentence": "Two multiplied by itself three times equals eight.",
            }],
            "lab_html": "<div>Verified power sequence</div>",
            "student_apply_prompt": {
                "prompt": "Calculate 2 cubed",
                "verified_against_source": True,
            },
        }],
        "quiz_eligible_count": 1,
        "quiz_html": '<section id="fullQuizBlock">Verified quiz</section>',
        "reference_card_html": '<section id="goldenReferenceCard">Verified Golden Card</section>',
    }
    return entry, theory


class V18RendererTest(unittest.TestCase):
    def test_real_html_embeds_runtime_and_golden_last(self):
        entry, theory = fixture()
        out = render_v18_lesson(entry, theory, {})
        for required in (
            'name="nabil-v18-renderer"',
            'id="boardWriting"',
            'id="teacherSpeech"',
            'id="studySlots"',
            'id="finalHost"',
            'id="v18VerifiedQuiz"',
            'id="nabilLessonData"',
            'id="goldenReferenceCard"',
            'id="fullQuizBlock"',
            'window.NabilV18=',
            'speechSynthesis',
            'function renderLab(s)',
            'function navigateToExercises()',
        ):
            with self.subTest(required=required):
                self.assertIn(required, out)
        # The golden card and the final quiz are gated until the lesson ends.
        self.assertIn('id="finalHost" class="panel" hidden', out)
        self.assertIn('id="v18VerifiedQuiz" class="panel quiz" hidden', out)
        self.assertIn("const final=index===steps.length", out)
        self.assertIn("el('finalHost').hidden=!final", out)
        self.assertIn("el('v18VerifiedQuiz').hidden=!final", out)
        self.assertIn("if(final)renderFinalCard()", out)
        self.assertIn("const u=new SpeechSynthesisUtterance(text)", out)
        self.assertIn("f.setAttribute('sandbox','allow-scripts allow-forms')", out)
        self.assertIn('Verified power sequence', out)
        self.assertIn('Calculate 2 cubed', out)
        self.assertNotIn('class="nabil-sci-grid"', out)
        self.assertLess(out.index('id="goldenReferenceCard"'), out.index('id="nabilLessonData"'))

    def test_missing_source_flow_rejected(self):
        with self.assertRaises(RuntimeError):
            render_v18_lesson(
                {"canonical_title": "Powers"},
                {"activities": [{"concept_id": "C01", "title": "No evidence"}]},
                {},
            )


if __name__ == "__main__":
    unittest.main()
