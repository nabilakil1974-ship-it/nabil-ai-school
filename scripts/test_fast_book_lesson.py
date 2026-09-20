"""CI contract: exact-page lessons cannot wait indefinitely across provider failover.

This is a static/syntax regression; a successful build is NOT an end-to-end
Railway provider availability or latency test.
"""
import ast
from pathlib import Path
import unittest

GATEWAY = Path("app/services/ai_gateway.py")
CHAT = Path("app/api/routes_chat.py")


class BoundedLessonLatencyTests(unittest.TestCase):
    def test_gateway_accepts_fast_lesson_and_has_provider_deadline(self):
        s = GATEWAY.read_text("utf-8")
        ast.parse(s)
        self.assertIn("fast_lesson: bool = False", s)
        self.assertIn("deadline = time.monotonic() + 58.0 if fast_lesson else None", s)
        self.assertIn("min(15.0, max(2.0, deadline - time.monotonic()))", s)
        self.assertIn("client.with_options(timeout=max(2.0, timeout_seconds), max_retries=0)", s)
        self.assertIn("FAST_LESSON_PROVIDER_BUDGET_EXHAUSTED", s)
        for name in ("_try_gemini_keys", "_try_openrouter", "_try_groq", "_try_openai"):
            self.assertIn("def " + name + "(", s)

    def test_page_generation_capped_before_client_90_second_cutoff(self):
        s = CHAT.read_text("utf-8")
        ast.parse(s)
        self.assertIn("fast_lesson=bool(lesson_start_from_book)", s)
        self.assertIn("fast_lesson=True", s)
        self.assertIn("81.0 - (time.monotonic() - _request_started_at)", s)
        self.assertIn("84.0 - (time.monotonic() - _request_started_at)", s)
        self.assertIn("timeout=min(17.0, _quality_remaining)", s)
        self.assertIn("BOOK_PAGE_QUALITY_REJECTED", s)
        self.assertIn("BOOK_TEXT_ONLY_LESSON_FALLBACK_SUCCESS", s)


if __name__ == "__main__":
    unittest.main()
