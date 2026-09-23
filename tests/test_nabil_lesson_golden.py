"""Check the reusable renderer against the original EB09 visual contract."""
import io
from types import SimpleNamespace
import unittest
from pathlib import Path

from bs4 import BeautifulSoup
from PIL import Image

from scripts.nabil_lesson_factory import (
    attach_evidence, check_content, check_html, evidence_catalog,
    render_html, source_evidence_map, trustworthy_title,
    parse_provider_json,
)

ROOT = Path(__file__).resolve().parents[1]


class GoldenLessonTest(unittest.TestCase):
    def test_original_reference_has_interactive_visual_contract(self):
        original = BeautifulSoup(
            (ROOT / "tests/fixtures/EB09-CONDUCTEURS-OHMIQUES.html").read_text(),
            "html.parser",
        )
        for selector in (".card", ".langbar", ".fig svg", ".formula",
                         ".summary", "#quick", "input", "select"):
            self.assertTrue(original.select_one(selector), selector)
        self.assertIn("@media(max-width:700px)", original.style.get_text())

    def test_new_renderer_preserves_structure_and_literal_provenance(self):
        page_text = (
            "Activity 1: Observe a solid and a liquid. A solid keeps its shape. "
            "A liquid flows and has a free surface. The free surface of a liquid "
            "at rest is horizontal. Figure 1 shows the water and the vessel. "
            "Exercise 1 asks students to explain why the surface is horizontal. "
        ) * 4
        pages = [(13, page_text)]
        catalog = evidence_catalog(pages)
        evidence_id = next(k for k,v in catalog.items()
                           if "free surface" in v["text"].lower())
        lesson = {
            "title": "Solids and Liquids",
            "introduction": "Observe the physical properties of solids and liquids "
                            "and explain the shape and free surface described by the textbook.",
            "introduction_evidence_id": evidence_id,
            "concepts": [
                {"heading": "The free surface", "explanation": "It is horizontal at rest.",
                 "evidence_id": evidence_id, "visual_evidence_id": evidence_id}
                for _ in range(3)
            ],
            "activities": [
                {"prompt": "Observe the liquid", "answer": "The surface is horizontal.",
                 "evidence_id": evidence_id} for _ in range(2)
            ],
            "questions": [
                {"prompt": "How is the surface?", "options": ["Horizontal", "Vertical", "Curved"],
                 "correct_index": 0, "explanation": "The source says horizontal.",
                 "evidence_id": evidence_id} for _ in range(3)
            ],
            "exercises": [
                {"prompt": "Explain the observed free surface.", "solution": 
                 "At rest, the liquid free surface is horizontal in the vessel.",
                 "solution_steps": ["Identify the liquid at rest.", "Read its level horizontally."],
                 "evidence_id": evidence_id} for _ in range(2)
            ],
            "summary": [
                {"text": "The free surface is horizontal.", "evidence_id": evidence_id}
                for _ in range(4)
            ],
        }
        attach_evidence(lesson,catalog)
        self.assertEqual([],check_content(lesson,lesson["title"],pages,catalog))
        picture=Image.new("RGB",(500,700),"white")
        out=io.BytesIO(); picture.save(out,format="JPEG")
        book={"title":"Test textbook.pdf","drive_file_id":"synthetic",
              "subject":"physics","grade":"الصف السابع","language":"English"}
        evidence_map=source_evidence_map(lesson["title"],pages,catalog)
        document=render_html(lesson,pages,book,{13:out.getvalue()},evidence_map)
        self.assertEqual([],check_html(document,lesson,pages,evidence_map))
        soup=BeautifulSoup(document,"html.parser")
        for selector in (".card.concept", ".concept .fig svg", ".concept figure img", ".langbar",
                         "#source-lab svg", "fieldset[data-answer]",
                         "#summary-card", ".source-pages img"):
            self.assertTrue(soup.select_one(selector),selector)
        lesson["concepts"][0]["evidence_id"]="MADE-UP"
        self.assertIn("UNVERIFIED_concepts_1",
                      check_content(lesson,lesson["title"],pages,catalog))

    def test_ocr_fragment_is_never_a_title(self):
        self.assertFalse(trustworthy_title("momen"))
        self.assertFalse(trustworthy_title("Screenshot_245.pdf"))
        self.assertFalse(trustworthy_title("002"))
        self.assertTrue(trustworthy_title("Solids and Liquids"))

    def test_openrouter_empty_json_mode_retries_plain_json(self):
        class Completions:
            def __init__(self):
                self.calls=[]

            def create(self,**kwargs):
                self.calls.append(kwargs)
                return SimpleNamespace(choices=[
                    SimpleNamespace(message=SimpleNamespace(content='{"ok":true}'))
                ])
        completions=Completions()
        client=SimpleNamespace(chat=SimpleNamespace(completions=completions))
        empty=SimpleNamespace(choices=[
            SimpleNamespace(message=SimpleNamespace(content=None))
        ])
        result=parse_provider_json(client,"openrouter",
                                   [{"role":"user","content":"Return JSON"}],empty,"openrouter/free")
        self.assertEqual({"ok":True},result)
        self.assertNotIn("response_format",completions.calls[0])


if __name__ == "__main__":
    unittest.main()
