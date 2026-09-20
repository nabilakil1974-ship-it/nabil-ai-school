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
    # Test the production cached HTML builder as well as the root route.
    # Executing root() alone no longer works: its cache is initialized by
    # _build_root_html() at module import time in the actual application.
    functions = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in {"_build_root_html", "root"}:
            function = copy.deepcopy(node)
            function.decorator_list = []
            functions.append(function)
    if len(functions) != 2:
        raise AssertionError("Expected _build_root_html and root in app/main.py")
    module = ast.fix_missing_locations(ast.Module(body=functions, type_ignores=[]))
    namespace = {
        "Path": lambda name: ROOT / name,
        "HTMLResponse": lambda html, headers=None: html,
    }
    exec(compile(module, "app/main.py", "exec"), namespace)
    namespace["_CACHED_ROOT_HTML"] = namespace["_build_root_html"]()
    return namespace["root"]()


class NabilUiIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = assemble_home_html()

    def test_ionic_chemistry_visual_uses_electrons_not_function_graph(self):
        visual = (STATIC / "nabil_ionic_diagram_fix.js").read_text(encoding="utf-8")
        self.assertIn('/static/nabil_ionic_diagram_fix.js?v=1', self.html)
        for marker in (
            "NABIL_IONIC_REJECT_UNRELATED_FUNCTION_GRAPH",
            'const loss=m.charge,gain=a.charge,g=gcd(loss,gain),mc=gain/g,ac=loss/g',
            "for(let k=0;k<mc*loss;k++)",
            "const top=(k%2===0)",
            "Lewis representation — pairs (doublets)",
            "const pts=[[-8,-40],[8,-40],[-8,42],[8,42],[-46,-6],[-46,10],[46,-6],[46,10]]",
            "Each ${esc(nonmetal)} ion has four electron pairs",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, visual)
        self.assertNotIn("f(x)", visual)

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
        self.assertIn("nabil_open_tutor_v1.js?v=18", self.html)
        tutor = (STATIC / "nabil_open_tutor_v1.js").read_text(encoding="utf-8")
        self.assertIn("nabilOpenVoiceUpload", tutor)
        self.assertIn("voiceFile.addEventListener", tutor)
        self.assertIn("request({audio:file})", tutor)

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

    def test_full_lesson_uses_compact_verified_book_passages_and_logs_failure(self):
        import ast
        route = (ROOT / "app" / "api" / "routes_chat.py").read_text(encoding="utf-8")
        ast.parse(route)
        for marker in (
            "lesson_start_from_book = (",
            "and _nabil_lesson_start_request(message)",
            "and bool(source_chunks)",
            "Verified book excerpts:",
            "messages=history_messages",
            "instructions=lesson_instructions if lesson_start_from_book else SYSTEM_PROMPT",
            "LESSON_COMPACT_SOURCE_PROMPT",
            "LESSON_GENERATION_FAILED",
            "max_output_tokens=output_budget",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, route)
        self.assertIn("book_curriculum = resolve_textbook_curriculum", route)

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
        self.assertIn("nabil_worksheet_v1.js?v=5", self.html)
        self.assertIn('window.addEventListener("click"', script)
        self.assertIn('closest("#nabilWorksheetBtn")', script)
        self.assertIn('block:"start"})},true)', script)
        self.assertNotIn('||$("nabilWorksheetBtn"))return', script)
        self.assertIn('let btn=$("nabilWorksheetBtn")', script)


    def test_worksheet_waits_for_student_attempt_and_grades_real_task(self):
        script = (STATIC / "nabil_worksheet_v1.js").read_text(encoding="utf-8")
        for token in (
            "function needsAttempt()",
            "assessedStages:[]",
            "||needsAttempt();",
            "activeTask=state.sections.findLast",
            "state.assessedStages.push(state.index-1)",
            "صحّح هذه المحاولة مقابل السؤال",
        ):
            with self.subTest(token=token):
                self.assertIn(token, script)

    def test_worksheet_stage_error_recovery_contract(self):
        script = (STATIC / "nabil_worksheet_v1.js").read_text(encoding="utf-8")
        for token in (
            "new AbortController()",
            "controller.abort()",
            "clearTimeout(timer)",
            "typeof data.reply",
            "لم تُحفَظ مرحلة فارغة",
            '$("nwReset").disabled=busy',
        ):
            with self.subTest(token=token):
                self.assertIn(token, script)

    def test_worksheet_preserves_all_retrieved_textbook_citations(self):
        script = (STATIC / "nabil_worksheet_v1.js").read_text(encoding="utf-8")
        for token in (
            "state.sources=Array.isArray(state.sources)?state.sources:[]",
            "const seen=new Set(state.sources.map",
            "if(!seen.has(identifier))",
            "state.sources.push({book_title:source.book_title,page:source.page})",
        ):
            with self.subTest(token=token):
                self.assertIn(token, script)
        self.assertNotIn("if(data.sources?.length)state.sources=data.sources;", script)

    def test_each_verified_figure_has_individual_keyboard_preview(self):
        script = (STATIC / "nabil_open_tutor_v1.js").read_text(encoding="utf-8")
        for token in (
            'pane.setAttribute("role","button")',
            'pane.setAttribute("aria-label","تكبير هذه الرسمة وحدها")',
            "const clone=pane.cloneNode(true)",
            'pane.addEventListener("click",previewOne)',
            'pane.addEventListener("keydown",e=>',
            "content.replaceChildren(clone);modal.hidden=false",
        ):
            with self.subTest(token=token):
                self.assertIn(token, script)

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

    def test_open_tutor_voice_does_not_outpace_answer_card(self):
        tutor = (STATIC / "nabil_open_tutor_v1.js").read_text(encoding="utf-8")
        for token in (
            "function playSynchronizedAnswer(reply,lang)",
            "explanation.hidden=true;",
            "if(activeTyper!==controller)return",
            "if(index>=words.length)return;",
            "if(!board.classList.contains(\"nabil-open-figure-only\"))explanation.hidden=false",
            "read.addEventListener(\"click\",()=>playSynchronizedAnswer(reply,lang))",
            "if(!shown.figureOnly)playSynchronizedAnswer(shown.reply,shown.lang)",
            "activeTyper?.finish()",
        ):
            with self.subTest(token=token):
                self.assertIn(token, tutor)
        self.assertNotIn("Math.min(420,(duration*1000)", tutor)

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
