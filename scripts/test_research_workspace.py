"""Verify postgraduate Word export and source/survey safeguards without service credentials."""
import ast
import io
from pathlib import Path
import unittest
from zipfile import ZipFile
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = (ROOT / "app/api/routes_research.py").read_text(encoding="utf-8")
UI = (ROOT / "app/static/nabil_research_v1.js").read_text(encoding="utf-8")
MAIN = (ROOT / "app/main.py").read_text(encoding="utf-8")
TREE = ast.parse(RESEARCH)


def isolate(name):
    node = next(n for n in TREE.body if isinstance(n, ast.FunctionDef) and n.name == name)
    from app.services.research_docx_notes import attach_researcher_footnotes
    namespace = {"io": io, "ResearchExport": object,
                 "attach_researcher_footnotes": attach_researcher_footnotes}
    exec("from __future__ import annotations\n" + ast.unparse(node), namespace)
    return namespace[name]


class FakeRequest:
    degree = "doctorate"
    title = "An evidence-based research inquiry into school leadership"
    language = "en"
    manuscript = "# Research Problem\nA preliminary, editable proposal.\n\n## Methodology\nNo fieldwork has been completed."
    sources = "Researcher-supplied bibliographic note; verification required"


class ResearchContract(unittest.TestCase):
    def test_syntax_and_ui_integration(self):
        for path in ("app/api/routes_research.py", "app/main.py"):
            compile((ROOT / path).read_text(encoding="utf-8"), path, "exec")
        self.assertIn("routes_research.router", MAIN)
        self.assertIn("nabil_research_v1.js", MAIN)
        for word in ("/api/research/draft", "/api/research/export/docx", "/api/research/survey/csv",
                     "doctorate", "masters", "previous_text", "textContent"):
            self.assertIn(word, UI)

    def test_both_degrees_and_source_integrity(self):
        for word in ("masters", "doctorate", "NEVER fabricate", "[SOURCE NEEDED]",
                     "complete_thesis", "sources_verified", "Google Forms creation requires"):
            self.assertIn(word, RESEARCH)

    def test_actual_editable_docx_contains_stage_and_reference_warning(self):
        create = isolate("build_research_docx")
        data = create(FakeRequest())
        self.assertGreater(len(data), 1200)
        with ZipFile(io.BytesIO(data)) as file:
            xml = file.read("word/document.xml")
            root = ET.fromstring(xml)
            text = " ".join((n.text or "") for n in root.iter() if n.tag.endswith("}t"))
            for phrase in ("school leadership", "Research Problem", "Methodology",
                           "verification required", "No fieldwork has been completed"):
                self.assertIn(phrase, text)

    def test_real_word_footnotes_from_user_supplied_marker(self):
        from app.services.research_docx_notes import attach_researcher_footnotes
        create = isolate("build_research_docx")
        request = FakeRequest()
        request.manuscript = "# Research Problem\\nGrounded claim [FN:1] must be checked."
        data = create(request)
        with ZipFile(io.BytesIO(data)) as file:
            self.assertIn("word/footnotes.xml", file.namelist())
            document = file.read("word/document.xml").decode("utf-8")
            notes = file.read("word/footnotes.xml").decode("utf-8")
            self.assertIn("footnoteReference", document)
            self.assertIn("researcher-supplied", notes.lower())
            self.assertIn("Researcher-supplied bibliographic note", notes)
            self.assertNotIn("[FN:1]", document)
        unknown = attach_researcher_footnotes(
            create(FakeRequest()), "Provided source"
        )
        self.assertTrue(unknown.startswith(b"PK"))

    def test_google_apps_script_creates_sections_and_questions_after_authorization(self):
        import json
        node = next(n for n in TREE.body if isinstance(n, ast.FunctionDef)
                    and n.name == "build_google_form_script")
        namespace = {"json": json, "GoogleFormScriptRequest": object,
                     "HTTPException": ValueError}
        exec("from __future__ import annotations\n" + ast.unparse(node), namespace)
        req = type("Request", (), {
            "title": "Doctoral research questionnaire",
            "language": "en",
            "questions": [
                {"axis": "Leadership", "item": "The principal involves staff in decisions."},
                {"axis": "Training", "item": "I have access to training opportunities."},
            ],
        })()
        script = namespace["build_google_form_script"](req)
        self.assertIn("FormApp.create(spec.title)", script)
        self.assertIn("form.addSectionHeaderItem()", script)
        self.assertIn("form.addMultipleChoiceItem()", script)
        self.assertIn("Staff", script.replace("staff", "Staff"))
        self.assertIn("getEditUrl()", script)
        self.assertIn("function createNabilResearchForm() {\\n", script)
        self.assertNotIn("created automatically", script)

    def test_survey_is_labeled_template_not_created_form(self):
        self.assertIn('"google_form_created": False', RESEARCH)
        self.assertIn("RESEARCHER TO WRITE AND VALIDATE QUESTION", RESEARCH)


if __name__ == "__main__":
    unittest.main(verbosity=2)
