"""Only real RAG pages may be presented to students as official-book citations."""
import unittest
from app.core.textbook_page_citations import (
    render_verified_page_citations, verified_source_pages,
)


class TextbookPageCitationTests(unittest.TestCase):
    def setUp(self):
        self.sources = [
            {"book_title": "chemistry - grade 9.pdf", "page": 55, "text": "ionic bond"},
            {"book_title": "chemistry - grade 9.pdf", "page": 56, "text": "NaCl"},
            {"book_title": "chemistry - grade 9.pdf", "page": 57, "text": "crystal lattice"},
            {"book_title": "chemistry - grade 9.pdf", "page": 56, "text": "second chunk"},
        ]

    def test_verified_pages_are_distinct_real_printed_pages(self):
        self.assertEqual(verified_source_pages(self.sources), [
            {"book_title": "chemistry - grade 9.pdf", "page": 55},
            {"book_title": "chemistry - grade 9.pdf", "page": 56},
            {"book_title": "chemistry - grade 9.pdf", "page": 57},
        ])

    def test_valid_concept_page_is_highlighted(self):
        out = render_verified_page_citations(
            "## Formation of NaCl\nElectron transfer. [BOOK_PAGE:56]",
            self.sources,
        )
        self.assertIn("📘 كتاب الدولة | الصفحة المطبوعة: 56", out)
        self.assertIn("Formation of NaCl", out)
        self.assertNotIn("[BOOK_PAGE:", out)

    def test_hallucinated_page_is_never_shown_as_official(self):
        out = render_verified_page_citations(
            "Claimed textbook figure. [BOOK_PAGE:999]",
            self.sources,
        )
        self.assertNotIn("999", out)
        self.assertNotIn("[BOOK_PAGE:", out)

    def test_multiple_pages_must_all_be_in_actual_retrieval(self):
        ok = render_verified_page_citations(
            "Linked concept. [BOOK_PAGE:55,56]", self.sources
        )
        self.assertIn("الصفحات المطبوعة: 55، 56", ok)
        bad = render_verified_page_citations(
            "Mixed citation. [BOOK_PAGE:55,99]", self.sources
        )
        self.assertNotIn("99", bad)
        self.assertNotIn("📘 كتاب الدولة | الصفحات المطبوعة: 55، 99", bad)

    def test_every_answer_shows_exact_pages_that_reached_model(self):
        out = render_verified_page_citations("Simple explanation.", self.sources)
        self.assertIn("الصفحات المسترجعة فعلًا من كتاب الدولة لهذا الجواب", out)
        self.assertIn("55, 56, 57", out)

    def test_no_sources_means_no_fake_index(self):
        text = "NABIL AI explanation"
        self.assertEqual(render_verified_page_citations(text, []), text)


if __name__ == "__main__":
    unittest.main()
