"""Offline regression checks; no Drive writes and no AI charges."""
import json
import tempfile
import unittest
from pathlib import Path

import fitz
from pptx import Presentation

from scripts.nabil_curriculum_author import _pages, _validate, _render
from scripts.nabil_lesson_artifacts import build_bundle
from scripts.verified_lesson_publisher import source_gate, artifact_gate

class FactoryTests(unittest.TestCase):
    def setUp(self):
        self.pdf = fitz.open()
        page = self.pdf.new_page()
        page.insert_text((60, 60), "Original textbook source evidence for a verified concept.")
        self.raw = self.pdf.tobytes()
        self.draft = {
          "title":{"fr":"Conducteurs ohmiques","en":"Ohmic conductors"},
          "objectives":[{"fr":"Comprendre la loi","en":"Understand the law"}],
          "concepts":[{"heading":{"fr":"Concept "+str(i),"en":"Concept "+str(i)},
             "explanation":{"fr":"Explication","en":"Explanation"},
             "source_pdf_page":1,
             "verbatim_excerpt":"Original textbook source evidence for a verified concept.",
             "figure_spec":{"kind":"none","scientific_labels":[],
                            "review_note":"Needs figure review"}} for i in range(4)],
          "activities":[{"prompt":{"fr":"Activité","en":"Activity"},
             "solution":{"fr":"Solution","en":"Solution"},"source_pdf_page":1,
             "verbatim_excerpt":"Original textbook source evidence for a verified concept."}
             for _ in range(2)],
          "exercises":[{"number":str(i),"prompt":{"fr":"Exercice","en":"Exercise"},
             "solution":{"fr":"Solution","en":"Solution"},"source_pdf_page":1,
             "verbatim_excerpt":"Original textbook source evidence for a verified concept."}
             for i in range(1,3)],
          "worksheet":[{"question":{"fr":"Question","en":"Question"},
             "answer":{"fr":"Réponse","en":"Answer"}} for _ in range(4)],
          "summary":[{"fr":"Résumé","en":"Summary"} for _ in range(3)],
          "scientific_review_notes":["Mock test only"]}
    def tearDown(self):
        self.pdf.close()
    def test_pages(self):
        self.assertEqual(_pages("1-1",1),[1])
        with self.assertRaises(ValueError):
            _pages("0-1",1)
    def test_citations(self):
        self.assertIsNone(_validate(self.draft,{1:"Original textbook source evidence for a verified concept."}))
        self.draft["concepts"][0]["verbatim_excerpt"]="Fabricated excerpt not present"
        with self.assertRaises(ValueError):
            _validate(self.draft,{1:"Original textbook source evidence for a verified concept."})
    def test_full_bundle_and_fail_closed_publish(self):
        import hashlib
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)
            (out/"source.pdf").write_bytes(self.raw)
            html=_render(self.draft,{})
            files=build_bundle(self.draft,self.raw,out,html,9,"physics",8,"Conducteurs ohmiques")
            manifest={"lesson_id":"TEST","grade":9,"subject":"physics",
                "chapter":8,"title":"Conducteurs ohmiques",
                "source_pdf":"source.pdf",
                "source_sha256":hashlib.sha256(self.raw).hexdigest(),**files}
            self.assertEqual(source_gate(manifest,out)["claims_checked"],8)
            self.assertEqual(artifact_gate(manifest,out)["pptx"]["fr"]["slides"],
                             len(Presentation(out/"lesson_fr.pptx").slides))
            self.assertFalse(manifest["scientific_review_approved"])
            self.assertFalse(manifest["reference_design_approved"])
            self.assertIn("source_pdf_page_001.png",
                          (out/"lesson.html").read_text())
if __name__=="__main__":
    unittest.main()
