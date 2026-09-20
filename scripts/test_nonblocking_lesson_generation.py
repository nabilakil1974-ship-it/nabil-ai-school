"""Regression: slow synchronous AI calls cannot block book preview on ASGI loop."""
import pathlib
import unittest


class NonblockingLessonGenerationTests(unittest.TestCase):
    def test_every_chat_generation_yields_event_loop(self):
        text = pathlib.Path("app/api/routes_chat.py").read_text(encoding="utf-8")
        chat = text.split("async def voice_chat(", 1)[1]
        self.assertIn("from starlette.concurrency import run_in_threadpool", text)
        self.assertIn("raw_reply = await run_in_threadpool(", chat)
        self.assertIn("BOOK_VISION_GENERATION_FAILED_TEXT_RETRY", chat)
        self.assertIn("image_bytes=None,", chat)
        self.assertIn("BOOK_TEXT_ONLY_LESSON_FALLBACK_SUCCESS", chat)
        for variable in ("repair_reply", "repaired_reply", "_science_repaired", "repaired"):
            self.assertIn(variable + " = await run_in_threadpool(ai.generate,", chat)
        self.assertNotIn("raw_reply = ai.generate(", chat)

    def test_exact_page_and_lesson_route_currently_supported(self):
        text = pathlib.Path("app/api/routes_chat.py").read_text(encoding="utf-8")
        self.assertIn("parse_textbook_page_request(message, book_page", text)
        self.assertIn("indexed_textbook_page_context(", text)
        self.assertIn("BOOK_EXACT_PAGE_REQUEST", text)


if __name__ == "__main__":
    unittest.main()
