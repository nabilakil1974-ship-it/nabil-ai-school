"""V18 HTML contract: real emitted output must not use legacy three-column renderer."""
import unittest
from scripts.nabil_factory.v18_editable.renderer import render_v18_lesson

class V18RendererTest(unittest.TestCase):
    def test_real_html_embeds_runtime_and_golden_last(self):
        entry={"lesson_id":"G07-MATHEMATICS-69B7C840-001","canonical_title":"Powers",
               "language":"en","grade":7,"subject":"mathematics","book_id":"source"}
        theory={"activities":[{"concept_id":"C01","title":"Powers","teaching_steps":[
            {"label":"See","sentence":"Two multiplied by itself three times equals eight."}],
            "lab_html":"<div>Verified power sequence</div>","student_apply_prompt":{"prompt":"Calculate 2 cubed","verified_against_source":True}}],"quiz_eligible_count":1,"quiz_html":"<section id=\"fullQuizBlock\">Verified quiz</section>"}
        out=render_v18_lesson(entry,theory,{})
        for required in ('name="nabil-v18-renderer"','NabilRuntime.TeacherPlaybackController',
                         'GOLDEN-FINAL-CARD','id="boardWriting"','fullQuizBlock','<script>'):
            self.assertIn(required,out)
        self.assertNotIn('class="nabil-sci-grid"',out)
        self.assertIn('/static/nabil_browser_tts_v1.js?v=1',out)
        self.assertIn('navigateToExercises',out)
        self.assertLess(out.index('C01'),out.index('GOLDEN-FINAL-CARD'))
        self.assertLess(out.index("visual.appendChild(f)"), out.rfind("</body>"))
        self.assertNotIn("+'</body></html>'", out)

    def test_missing_source_flow_rejected(self):
        with self.assertRaises(RuntimeError):
            render_v18_lesson({"canonical_title":"Powers"},
                {"activities":[{"concept_id":"C01","title":"No evidence"}]},{})

if __name__=="__main__": unittest.main()
