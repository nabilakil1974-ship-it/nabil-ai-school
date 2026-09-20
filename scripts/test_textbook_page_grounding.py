"""Government textbook page provenance and original-image fallback regressions."""
import unittest
from app.core.textbook_page_citations import (
    verified_source_pages, verified_page_refs, resolve_book_printed_page,
    render_verified_page_citations,
)

def source(page=54, pdf=54, title="chemistry - grade 9.pdf", book="real-book-id"):
    return dict(page=page, pdf_page=pdf, book_id=book,
                book_title=title, text="Verified indexed passage")

class PageGroundingTests(unittest.TestCase):
    def test_real_pdf_and_printed_page_are_not_confused(self):
        self.assertEqual(resolve_book_printed_page(source()), 56)
        self.assertEqual(resolve_book_printed_page(source(56, 54)), 56)
        self.assertEqual(resolve_book_printed_page(source(56, 54, "other.pdf")), 56)
        self.assertEqual(verified_source_pages([source(), source()]),
                         [{"book_title": "chemistry - grade 9.pdf", "page": 56}])

    def test_figure_falls_back_to_original_book_page_not_ai_illustration(self):
        text = "## Formation of ions [BOOK_PAGE:56]\n" + (
            "[BOOK_FIGURE_PAGE:56] The student can inspect the original diagram."
        )
        answer = render_verified_page_citations(text, [source()])
        self.assertIn("📘 كتاب الدولة | الصفحة المطبوعة: 56", answer)
        self.assertIn("الرسم الأصلي من كتاب الدولة", answer)
        self.assertIn("![صورة صفحة الكتاب الأصلية", answer)
        self.assertIn("/api/textbooks/real-book-id/pages/56/image", answer)
        self.assertNotIn("BOOK_PAGE:", answer)
        self.assertNotIn("BOOK_FIGURE_PAGE:", answer)

    def test_no_model_fabricated_page_citations_or_images(self):
        answer = render_verified_page_citations(
            "An invented page [BOOK_PAGE:99] and image [BOOK_FIGURE_PAGE:99]",
            [source()],
        )
        self.assertNotIn("BOOK_PAGE", answer)
        self.assertNotIn("BOOK_FIGURE_PAGE", answer)
        self.assertNotIn("pages/99/image", answer)
        self.assertIn("الصفحات المسترجعة فعلًا", answer)

    def test_no_source_no_official_book_claim(self):
        answer = render_verified_page_citations(
            "Explaining ionic bonding [BOOK_PAGE:56] [BOOK_FIGURE_PAGE:56]", []
        )
        self.assertNotIn("📘", answer)
        self.assertNotIn("BOOK_PAGE", answer)
        self.assertNotIn("BOOK_FIGURE_PAGE", answer)

    def test_indexed_image_requires_real_book_and_pdf_position(self):
        self.assertEqual(verified_page_refs([{
            "page": 56, "book_title": "chemistry - grade 9.pdf"
        }]), [])
        self.assertEqual(len(verified_page_refs([source(), source()])), 1)

if __name__=="__main__":
    unittest.main()
