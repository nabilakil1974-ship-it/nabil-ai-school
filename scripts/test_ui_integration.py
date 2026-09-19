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

    def test_structured_exercise_real_answer_and_separate_drawing(self):
        script = (STATIC / "nabil_learning_v132.js").read_text(encoding="utf-8")
        for marker in (
            '"solve_exercise","✍️ حلّ التمرين"',
            "if(!showLastActivity(previousAnswer))",
            "given data will appear here",
            "nv132-figure-card",
            "figureNodes.forEach",
            "min-height:clamp(240px,32vw,480px)",
        ):
            self.assertIn(marker, script)
        self.assertNotIn("max-height:min(65vh,560px);overflow:auto", script)

    def test_exercise_send_never_disappears_without_feedback(self):
        learning = (STATIC / "nabil_learning_v132.js").read_text(encoding="utf-8")
        tutor = (STATIC / "nabil_open_tutor_v1.js").read_text(encoding="utf-8")
        for fragment in (
            "ما زلنا بانتظار حلّ التمرين",
            "لم يصل حلّ جديد",
            "Promise.race([",
            "clearTimeout(lateNotice)",
        ):
            self.assertIn(fragment, learning)
        self.assertIn("if(!audio&&String(question||", tutor)
        self.assertIn("return false;", tutor)
        self.assertIn("if(ok===false&&!input.value.trim())input.value=q", tutor)
        self.assertIn("nabil_learning_v132.js?v=139", self.html)
        self.assertIn("nabil_open_tutor_v1.js?v=17", self.html)

    def test_lesson_explanation_and_preview_never_disappear_silently(self):
        tutor = (STATIC / "nabil_open_tutor_v1.js").read_text(encoding="utf-8")
        theme = (STATIC / "nabil_reference_theme.css").read_text(encoding="utf-8")
        strict = (STATIC / "curriculum_strict.js").read_text(encoding="utf-8")
        for marker in (
            "text.textContent", "وصل الجواب؛ عم بعرض الشرح",
            "closeDrawingPreviewBtn", "e.key===\"Escape\"",
            "drawingModal.hidden=true",
        ):
            self.assertIn(marker, tutor)
        for marker in (
            "#drawingPreviewModal:not([hidden])",
            "#drawingPreviewContent svg",
            "max-height:calc(100dvh - 12px)",
        ):
            self.assertIn(marker, theme)
        self.assertIn("اختر فرع الثالث ثانوي أولًا", strict)
        self.assertIn("curriculum_strict.js?v=138", self.html)
        self.assertIn("nabil_reference_theme.css?v=16", self.html)

    def test_third_secondary_branch_catalog_precedes_old_unbranched_index(self):
        backend = (ROOT / "app" / "api" / "routes_chat.py").read_text(encoding="utf-8")
        self.assertIn("Branch-specific third-secondary master entries", backend)
        self.assertLess(backend.index("master_first = json.loads("),
                        backend.index("grade_node = subject_node.get(curated_grade"))

    def test_full_lesson_projector_rule_highlight_and_language_contract(self):
        learning = (STATIC / "nabil_learning_v132.js").read_text(encoding="utf-8")
        theme = (STATIC / "nabil_reference_theme.css").read_text(encoding="utf-8")
        backend = (ROOT / "app" / "api" / "routes_chat.py").read_text(encoding="utf-8")
        for token in ("projector", "requestFullscreen", "nabil-projector-mode", "markKeyRules"):
            self.assertIn(token, learning)
        for token in (".nabil-key-rule", "body.nabil-projector-mode", "color:#ff5b62"):
            self.assertIn(token, theme)
        self.assertIn('policy_language in {"English", "Français", "العربية"}', backend)
        self.assertIn("top_k=10 if str(teaching_mode", backend)
        self.assertIn("🔴 Key Rule:", backend)

    def test_math_manifest_covers_all_school_grades_and_secondary_branches(self):
        import json
        books = json.loads((ROOT / "data" / "math_textbooks_manifest.json").read_text(encoding="utf-8"))["books"]
        self.assertEqual(len(books), 32)
        grades = {item["grade"] for item in books}
        for grade in (
            "الصف الأول","الصف الثاني","الصف الثالث","الصف الرابع","الصف الخامس",
            "الصف السادس","الصف السابع","الصف الثامن","الصف التاسع","الأول ثانوي",
            "الثاني ثانوي - العلوم","الثاني ثانوي - الإنسانيات",
            "الثالث ثانوي - العلوم العامة","الثالث ثانوي - علوم الحياة",
            "الثالث ثانوي - الاجتماع والاقتصاد","الثالث ثانوي - الآداب والإنسانيات",
        ):
            self.assertIn(grade, grades)
        for grade in grades:
            langs = {x["language"] for x in books if x["grade"] == grade}
            self.assertEqual(langs, {"English", "Français"})
        progress = (ROOT / "scripts" / "math_progress.py").read_text(encoding="utf-8")
        indexer = (ROOT / "scripts" / "index_math_textbooks.py").read_text(encoding="utf-8")
        self.assertIn("Read-only report", progress)
        self.assertIn("pg_advisory_lock(728168120)", indexer)

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
        for token in ("#06182e", "#0b263f", "#14c8f5", "#0bb353", "#e5232e"):
            with self.subTest(token=token):
                self.assertIn(token, css)
        self.assertIn("#nabilHomeTutorHost", css)
        self.assertIn(".selection-stage[hidden]", css)

    def test_open_tutor_uses_shared_audio_and_visual_engine(self):
        js = (STATIC / "nabil_open_tutor_v1.js").read_text(encoding="utf-8")
        for token in (
            '"/api/chat"', '"general_exercises"', '"AUTO"',
            "nabilSpeakClear", "renderNabilDiagram", "renderAIText",
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

    def test_source_grounded_interactive_worksheet_contract(self):
        script = (STATIC / "nabil_worksheet_v1.js").read_text(encoding="utf-8")
        backend = (ROOT / "app" / "api" / "routes_chat.py").read_text(encoding="utf-8")
        theme = (STATIC / "nabil_reference_theme.css").read_text(encoding="utf-8")
        for token in (
            "nabilWorksheetBtn", "worksheet_plan", "worksheet_observe",
            "worksheet_apply", "worksheet_self_assess", "worksheet_assess_answer",
            "localStorage", '"/api/worksheet/export/"+format', 'download("docx")', 'download("pdf")',
            "requestFullscreen", "renderNabilDiagram",
            "[SOLUTION", "nw-solution", "pngOf", "drawingPreviewModal",
        ):
            self.assertIn(token, script)
        for token in (
            '"worksheet_plan"', '"worksheet_apply"', '"worksheet_assess_answer"',
            '"book_title": str(item.get("book_title")',
        ):
            self.assertIn(token, backend)
        self.assertIn("#nabilWorksheetPanel", theme)
        self.assertIn("@media(max-width:720px)", theme)
        self.assertIn("nabil_worksheet_v1.js?v=1", self.html)


    def test_owner_voice_language_pacing_and_visual_contract(self):
        js = (STATIC / "nabil_open_tutor_v1.js").read_text(encoding="utf-8")
        css = (STATIC / "nabil_reference_theme.css").read_text(encoding="utf-8")
        main_py = (ROOT / "app" / "main.py").read_text(encoding="utf-8")
        for token in (
            "prepareSpeechTypewriter", "nabilOpenPace", "window.nabilVoicePace",
            'board.dir=dir', 'board.lang=', "detectLanguage(reply&&detectLanguage(reply)",
            "drawingPreviewModal", "Enlarge figure", "Agrandir le schéma",
            "معاينة الرسمة كبيرة",
            'input.dir=lang==="العربية"?"rtl":"ltr"',
            'row.dir=lang==="العربية"?"rtl":"ltr"',
        ):
            with self.subTest(token=token):
                self.assertIn(token, js)
        for token in (
            "min-height:clamp(200px,27vw,390px)",
            "min-height:clamp(280px,46vw,650px)",
            "#drawingPreviewContent",
            "--nabil-owner-bg:#05172d",
            "#nabilOpenAnswer[lang=\"en\"]",
            "#nabilOpenAnswer[lang=\"fr\"]",
        ):
            with self.subTest(token=token):
                self.assertIn(token, css)
        self.assertIn("pace_browser_new", main_py)
        self.assertIn("pace_neural_new", main_py)

    def test_owner_three_dimensional_and_same_renderer_contract(self):
        route = (ROOT / "app" / "api" / "routes_chat.py").read_text(encoding="utf-8")
        tutor = (STATIC / "nabil_open_tutor_v1.js").read_text(encoding="utf-8")
        for token in (
            "cube", "rectangular_prism", "cylinder", "cone", "sphere",
            "مجسم 3D", "3D-style circuits",
        ):
            with self.subTest(token=token):
                self.assertIn(token, route)
        self.assertIn("renderNabilDiagram", tutor)
        self.assertNotIn("invent", tutor.lower().split("renderNabilDiagram",1)[0][-500:])

    def test_learning_dock_is_real_and_in_normal_flow(self):
        css = (STATIC / "nabil_reference_theme.css").read_text(encoding="utf-8")
        js = (STATIC / "nabil_learning_v132.js").read_text(encoding="utf-8")
        self.assertIn("position:relative!important", css)
        self.assertIn("clear:both!important", css)
        for action in (
            "checkpoint", "explain_another_way", "adaptive_practice",
            "flashcards", "quick_quiz", "study_plan", "dashboard",
        ):
            with self.subTest(action=action):
                self.assertIn(action, js)
        self.assertIn("showLastActivity", js)
        self.assertIn("sendToAI(question,false)", js)



if __name__ == "__main__":
    unittest.main(verbosity=2)
