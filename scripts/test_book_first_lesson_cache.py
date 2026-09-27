"""Regression tests for book-first lesson preview and reusable lesson packages."""
import pathlib
import unittest
from app.core.lesson_cache_contract import lesson_cache_key, source_signature


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

    def test_preview_never_renders_source_raster_to_students(self):
        js = pathlib.Path("app/static/nabil_book_first_preview_v1.js").read_text("utf-8")
        self.assertIn("INTERNAL EVIDENCE ONLY", js)
        self.assertIn("grounded in the indexed textbook", js)
        self.assertIn("verified internally", js)
        for forbidden in (
            "originalPageImage",
            "figure_image_urls",
            "page_image_url",
            "Original textbook figure",
            "Open original textbook page",
            "عرض الصورة الأصلية لصفحة الكتاب",
        ):
            self.assertNotIn(forbidden, js)

    def test_failed_ai_request_never_marks_lesson_ready(self):
        js = pathlib.Path("app/static/nabil_book_first_preview_v1.js").read_text("utf-8")
        self.assertIn("lessonFailed=true;updateStatus()", js)
        self.assertIn("if(!title)return {done:()=>{},fail:()=>{}};", js)
        self.assertIn("if(lessonFailed){", js)
        self.assertIn("if(result.ok){", js)
        self.assertIn("}else{", js)
        self.assertIn("fail();", js)

    def test_printed_page_persists_across_provider_retries(self):
        js = pathlib.Path("app/static/nabil_book_first_preview_v1.js").read_text("utf-8")
        self.assertIn('body.set("book_page",String(Number(picker.value)))', js)
        self.assertIn('body.set("book_page",typedPage)', js)
        self.assertNotIn('picker.value="";', js)
        self.assertIn('String(result.printed_page)!==String(Number(chosen))', js)

    def test_preview_never_waits_for_pdf_download_or_figure_extraction(self):
        route = pathlib.Path("app/api/routes_textbook_pages.py").read_text("utf-8")
        preview = route.split('@router.post("/textbooks/lesson-preview")', 1)[1]
        self.assertNotIn("_embedded_figure_pngs(", preview)
        self.assertNotIn("_drive_pdf_bytes(", preview)
        self.assertIn("source_excerpt", preview)
        self.assertIn("printed_page", preview)
        self.assertIn("figure_image_urls", preview)

    def test_source_raster_is_not_rendered_and_preview_timeout_stays_safe(self):
        js = pathlib.Path("app/static/nabil_book_first_preview_v1.js").read_text("utf-8")
        self.assertIn("INTERNAL EVIDENCE ONLY", js)
        self.assertIn("previewTimeout", js)
        self.assertNotIn("original.onerror=()=>holder.remove()", js)
        self.assertNotIn("figure_image_urls", js)
        self.assertNotIn("page_image_url", js)
        self.assertNotIn('controller.abort();\\n    if(el.isConnected)', js)

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
