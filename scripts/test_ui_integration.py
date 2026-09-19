"""Lightweight UI integration build without importing the live database.

Run: python -m scripts.test_ui_integration
The root HTML response is exercised by extracting only the FastAPI route body,
so tests can run during CI without Railway secrets or PostgreSQL.
"""
import ast
import copy
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
STATIC = ROOT / "app" / "static"


def assemble_home_html() -> str:
    source = (ROOT / "app" / "main.py").read_text(encoding="utf-8")
    tree = ast.parse(source, filename="app/main.py")
    route = next(
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "root"
    )
    route = copy.deepcopy(route)
    route.decorator_list = []
    module = ast.fix_missing_locations(ast.Module(body=[route], type_ignores=[]))
    namespace = {
        "Path": lambda name: ROOT / name,
        "HTMLResponse": lambda html, headers=None: html,
    }
    exec(compile(module, "app/main.py", "exec"), namespace)
    return namespace["root"]()


class NabilUiIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = assemble_home_html()

    def test_one_robot_home_no_separate_gateway(self):
        self.assertIn('id="nabilHome"', self.html)
        self.assertNotIn('<script id="nabil-v105-startup-script">', self.html)
        self.assertIn("function bootstrapNabilHome(){ return;", self.html)
        self.assertNotIn("#nabilHome,#nabilProfessorGateway{display:none", self.html)
        self.assertIn("#nabilProfessorGateway{display:none", self.html)

    def test_removed_fake_progress_engine(self):
        self.assertNotIn('<script id="nabilV130Script">', self.html)

    def test_script_insertion_only_at_final_body(self):
        self.assertEqual(self.html.count("/static/nabil_open_tutor_v1.js?"), 1)
        self.assertEqual(self.html.count("/static/nabil_learning_v132.js?"), 1)
        self.assertEqual(self.html.count("/static/nabil_reference_theme.css?"), 1)
        self.assertTrue(self.html.rstrip().endswith("</html>"))

    def test_open_question_language_is_independent_of_dropdown(self):
        section = self.html[self.html.index("async function sendToAI("):]
        self.assertIn(
            "detectMessageRenderLanguage(showStudentMessage ? message", section
        )
        self.assertIn('generalExercisesMode ? "" : lessonSelect.value', section)

    def test_reference_palette_and_mobile_home(self):
        css = (STATIC / "nabil_reference_theme.css").read_text(encoding="utf-8")
        for token in ("#06182e", "#102940", "#38bdf8", "#05a34c", "#e12932"):
            with self.subTest(token=token):
                self.assertIn(token, css)
        self.assertIn("#nabilHomeTutorHost", css)
        self.assertIn(".selection-stage[hidden]", css)

    def test_open_tutor_uses_shared_audio_and_visual_engine(self):
        js = (STATIC / "nabil_open_tutor_v1.js").read_text(encoding="utf-8")
        for token in (
            '"/api/chat"', '"general_exercises"', '"AUTO"',
            "nabilSpeakClear", "renderNabilDiagram", "renderGeneralExerciseBoards",
            "MediaRecorder", "nabilOpenInput", "nabilOpenAnswer",
        ):
            with self.subTest(token=token):
                self.assertIn(token, js)

    def test_real_learning_actions_and_nonrecursive_dock(self):
        js = (STATIC / "nabil_learning_v132.js").read_text(encoding="utf-8")
        for token in (
            "nv132Result", "learning", "checkpoint", "adaptive_practice",
            "flashcards", "quick_quiz", "study_plan",
            "latest.nextElementSibling!==dock",
        ):
            with self.subTest(token=token):
                self.assertIn(token, js)


if __name__ == "__main__":
    unittest.main(verbosity=2)
