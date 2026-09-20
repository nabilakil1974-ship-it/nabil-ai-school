"""Offline regression for CRDP manifest vs teacher-facing curriculum routing.

Run: python -m scripts.test_textbook_scope
"""
import json
from pathlib import Path
import unittest

from app.services.textbook_scope import resolve_textbook_curriculum


ROOT = Path(__file__).resolve().parents[1]


class TextbookScopeTests(unittest.TestCase):
    def test_ninth_grade_english_ionic_bond_uses_indexed_chemistry_book(self):
        books = json.loads(
            (ROOT / "data/chemistry_textbooks_manifest.json").read_text(encoding="utf-8")
        )["books"]
        indexed = [
            book for book in books
            if book["grade"] == "الصف التاسع"
            and book["subject"] == "كيمياء"
            and book["curriculum"] == resolve_textbook_curriculum(
                "المنهج اللبناني الرسمي", "English"
            )
        ]
        self.assertEqual(len(indexed), 1)
        self.assertEqual(indexed[0]["title"], "chemistry - grade 9.pdf")

    def test_english_french_scope_never_crosses_languages(self):
        self.assertEqual(resolve_textbook_curriculum("المنهج اللبناني الرسمي", "English"), "CRDP-EN")
        self.assertEqual(resolve_textbook_curriculum("المنهج اللبناني الرسمي", "Français"), "CRDP-FR")
        self.assertEqual(resolve_textbook_curriculum("CRDP-EN", "Français"), "CRDP-EN")
        self.assertEqual(resolve_textbook_curriculum("CRDP-FR", "English"), "CRDP-FR")

    def test_other_curricula_and_arabic_are_not_automatically_relabelled(self):
        self.assertEqual(resolve_textbook_curriculum("Private school", "English"), "Private school")
        self.assertEqual(
            resolve_textbook_curriculum("المنهج اللبناني الرسمي", "العربية"),
            "المنهج اللبناني الرسمي",
        )

    def test_lesson_route_uses_resolved_scope_for_check_and_rag(self):
        source = (ROOT / "app/api/routes_chat.py").read_text(encoding="utf-8")
        anchor = source[source.index("book_curriculum = resolve_textbook_curriculum"):source.index(
            '        educational_context = f"""', source.index("book_curriculum = resolve_textbook_curriculum")
        )]
        self.assertIn("BookChunk.curriculum == book_curriculum", anchor)
        self.assertIn("curriculum=book_curriculum,", anchor)
        self.assertIn("BOOK_RAG_SCOPE_MATCH", anchor)


if __name__ == "__main__":
    unittest.main(verbosity=2)
