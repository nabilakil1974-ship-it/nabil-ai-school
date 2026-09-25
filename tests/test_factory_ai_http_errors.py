"""Regression checks: upstream refusal is diagnosed without exposing API keys.

Run: python -m unittest tests.test_factory_ai_http_errors
No network, Drive call, or textbook page transfer.
"""
import io
import json
import os
import unittest
import urllib.error
from unittest.mock import patch

from scripts import nabil_lesson_factory as factory


class FactoryAIHTTPErrorTests(unittest.TestCase):
    def test_403_names_provider_model_and_redacts_api_key(self):
        secret = "sk-or-v1-TOP_SECRET_TEST_KEY"
        error_payload = json.dumps({
            "error": {
                "code": 403,
                "message": "Model access denied for " + secret
            }
        }).encode("utf-8")
        http_error = urllib.error.HTTPError(
            "https://openrouter.ai/api/v1/chat/completions",
            403, "Forbidden", {}, io.BytesIO(error_payload)
        )
        with patch.dict(os.environ, {
            "OPENROUTER_API_KEY": secret,
            "OPENROUTER_VISION_MODEL": "google/gemini-2.5-flash",
        }, clear=True):
            with patch.object(factory.urllib.request, "urlopen", side_effect=http_error) as request:
                with self.assertRaises(RuntimeError) as caught:
                    factory.execute_llm_completion(
                        "Identify figures", image_base64="iVBORw0KGgo="
                    )
        msg = str(caught.exception)
        self.assertIn("AI_PROVIDER_HTTP_ERROR", msg)
        self.assertIn("provider=openrouter", msg)
        self.assertIn("model=google/gemini-2.5-flash", msg)
        self.assertIn("http_status=403", msg)
        self.assertNotIn(secret, msg)
        req = request.call_args.args[0]
        sent = json.loads(req.data.decode("utf-8"))
        self.assertEqual(sent["model"], "google/gemini-2.5-flash")
        self.assertEqual(sent["messages"][0]["content"][1]["type"], "image_url")

    def test_success_response_is_unchanged(self):
        response = {"choices": [{"message": {"content": '{"ok":true}'}}]}
        class FakeResponse:
            def __enter__(self):
                return self
            def __exit__(self, *args):
                return False
            def read(self):
                return json.dumps(response).encode("utf-8")
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "sample"}, clear=True):
            with patch.object(factory.urllib.request, "urlopen", return_value=FakeResponse()):
                result = factory.execute_llm_completion("Return JSON")
        self.assertEqual(json.loads(result), {"ok": True})


if __name__ == "__main__":
    unittest.main()
