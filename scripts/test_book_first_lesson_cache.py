"""Regression tests for book-first lesson preview and reusable lesson packages."""
import pathlib
import unittest
from app.services.lesson_cache import lesson_cache_key, source_signature


class BookFirstLessonTests(unittest.TestCase):
    def test_cache_key_is_exact_scope_and_stable(self):
        a = lesson_cache_key("الصف التاسع", "", "كيمياء", "CRDP-EN",
                             "English", "Ionic bond", "full_lesson")
        b = lesson_cache_key("الصف التاسع", "", "كيمياء", "CRDP-EN",
                             "English", "Ionic bond", "full_lesson")
        other = lesson_cache_key("الصف التاسع", "", "كيمياء", "CRDP-EN",
                                 "English", "Covalent bond", "full_lesson")
        self.assertEqual(a, b)
        self.assertNotEqual(a, other)

    def test_source_signature_changes_when_real_book_source_changes(self):
        base = [{"book_id":"b1","page":56,"pdf_page":54,"text":"NaCl electron transfer"}]
        changed = [{"book_id":"b1","page":57,"pdf_page":55,"text":"Crystal lattice"}]
        self.assertEqual(source_signature(base), source_signature(list(base)))
        self.assertNotEqual(source_signature(base), source_signature(changed))

    def test_preview_shows_figure_crops_not_full_page_on_board(self):
        js = pathlib.Path("app/static/nabil_book_first_preview_v1.js").read_text("utf-8")
        self.assertIn("figure_image_urls", js)
        self.assertIn("Original textbook figure", js)
        self.assertIn("complete original page (not shown on the lesson board)", js)
        self.assertNotIn('img.src=path', js)

    def test_figure_route_excludes_full_page_backgrounds(self):
        route = pathlib.Path("app/api/routes_textbook_pages.py").read_text("utf-8")
        self.assertIn("_embedded_figure_pngs", route)
        self.assertIn("width >= 1500 and height >= 1000", route)
        self.assertIn("/figures/{figure_index}/image", route)

    def test_chat_has_cache_hit_and_explicit_refresh_paths(self):
        chat = pathlib.Path("app/api/routes_chat.py").read_text("utf-8")
        self.assertIn("LESSON_PACKAGE_CACHE_HIT", chat)
        self.assertIn("LESSON_PACKAGE_CACHE_SAVED", chat)
        self.assertIn("_force_lesson_refresh", chat)
        self.assertIn("save_cached_lesson(", chat)


if __name__ == "__main__":
    unittest.main()
