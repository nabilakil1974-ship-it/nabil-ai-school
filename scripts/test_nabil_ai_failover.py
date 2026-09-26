import io
import json
import os
import unittest
import urllib.error
from unittest import mock

import scripts.nabil_lesson_factory as factory


class _FakeResponse:
    def __init__(self, payload):
        self.payload = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return self.payload


def _rate_limit(url, seconds):
    body = io.BytesIO(json.dumps({
        "error": {
            "message": f"Please try again in {seconds}s",
            "code": "rate_limit_exceeded",
        }
    }).encode("utf-8"))
    return urllib.error.HTTPError(
        url=url,
        code=429,
        msg="Too Many Requests",
        hdrs={"Retry-After": str(seconds), "Content-Type": "application/json"},
        fp=body,
    )


class SmartFailoverTest(unittest.TestCase):
    def setUp(self):
        factory._AI_PROVIDER_COOLDOWNS.clear()

    def tearDown(self):
        factory._AI_PROVIDER_COOLDOWNS.clear()

    def test_groq_429_fails_over_immediately_to_openrouter(self):
        env = {
            "NABIL_FACTORY_AI_PROVIDER": "groq",
            "NABIL_FACTORY_AI_FAILOVER_PROVIDERS": "openrouter,openai",
            "NABIL_FACTORY_MAX_ALL_PROVIDER_WAIT_SECONDS": "60",
            "GROQ_API_KEY": "g",
            "OPENROUTER_API_KEY": "o",
        }

        def fake_urlopen(req, timeout=60):
            if "groq.com" in req.full_url:
                raise _rate_limit(req.full_url, 600)
            if "openrouter.ai" in req.full_url:
                return _FakeResponse({
                    "choices": [{"message": {"content": '{"ok": true}'}}]
                })
            raise AssertionError("Unexpected provider " + req.full_url)

        with mock.patch.dict(os.environ, env, clear=False),              mock.patch.object(factory.urllib.request, "urlopen",
                               side_effect=fake_urlopen),              mock.patch.object(factory.time, "sleep") as sleep:
            out = factory.execute_llm_completion(
                'Return {"ok": true}', json_mode=True)

        self.assertEqual(json.loads(out), {"ok": True})
        self.assertFalse(sleep.called)
        prov = factory.get_last_llm_provenance()
        self.assertEqual(prov["provider"], "openrouter")
        self.assertEqual(prov["primary_provider"], "groq")
        self.assertTrue(prov["used_failover"])

    def test_transient_network_failure_uses_next_provider(self):
        env = {
            "NABIL_FACTORY_AI_PROVIDER": "groq",
            "NABIL_FACTORY_AI_FAILOVER_PROVIDERS": "openrouter",
            "GROQ_API_KEY": "g",
            "OPENROUTER_API_KEY": "o",
        }

        def fake_urlopen(req, timeout=60):
            if "groq.com" in req.full_url:
                raise urllib.error.URLError("temporary network failure")
            if "openrouter.ai" in req.full_url:
                return _FakeResponse({
                    "choices": [{"message": {"content": '{"ok": true}'}}]
                })
            raise AssertionError("Unexpected provider " + req.full_url)

        with mock.patch.dict(os.environ, env, clear=False), \
             mock.patch.object(factory.urllib.request, "urlopen",
                               side_effect=fake_urlopen), \
             mock.patch.object(factory.time, "sleep") as sleep:
            out = factory.execute_llm_completion(
                'Return {"ok": true}', json_mode=True)

        self.assertEqual(json.loads(out), {"ok": True})
        self.assertFalse(sleep.called)
        self.assertEqual(
            factory.get_last_llm_provenance()["provider"],
            "openrouter")

    def test_all_three_long_cooldowns_fail_fast_without_sleeping(self):
        env = {
            "NABIL_FACTORY_AI_PROVIDER": "groq",
            "NABIL_FACTORY_AI_FAILOVER_PROVIDERS": "openrouter,openai",
            "NABIL_FACTORY_MAX_ALL_PROVIDER_WAIT_SECONDS": "60",
            "GROQ_API_KEY": "g",
            "OPENROUTER_API_KEY": "o",
            "OPENAI_API_KEY": "a",
        }

        def fake_urlopen(req, timeout=60):
            if "groq.com" in req.full_url:
                raise _rate_limit(req.full_url, 600)
            if "openrouter.ai" in req.full_url:
                raise _rate_limit(req.full_url, 300)
            if "api.openai.com" in req.full_url:
                raise _rate_limit(req.full_url, 900)
            raise AssertionError("Unexpected provider " + req.full_url)

        with mock.patch.dict(os.environ, env, clear=False),              mock.patch.object(factory.urllib.request, "urlopen",
                               side_effect=fake_urlopen),              mock.patch.object(factory.time, "sleep") as sleep:
            with self.assertRaisesRegex(
                    RuntimeError, "AI_ALL_PROVIDERS_COOLING_DOWN"):
                factory.execute_llm_completion(
                    'Return {"ok": true}', json_mode=True)

        self.assertFalse(sleep.called)

    def test_pilot_page_14_is_authorized_for_all_three_providers(self):
        context = {
            "lesson_id": "G07-PHYSICS-001",
            "book_id": "1LasqIgGUuck1l-2EZbj2kA0Dg9ygJ_AH",
            "pdf_page": 14,
        }
        for provider in ("groq", "openrouter", "openai"):
            with self.subTest(provider=provider):
                self.assertTrue(factory._vision_provider_authorized(
                    provider, context, require_key=False))

    def test_scheduler_chooses_shortest_when_all_are_cooling(self):
        mode, provider, wait = factory._next_provider_or_wait(
            ["groq", "openrouter", "openai"],
            {"groq": 1000.0, "openrouter": 700.0, "openai": 900.0},
            500.0,
        )
        self.assertEqual(mode, "wait")
        self.assertEqual(provider, "openrouter")
        self.assertEqual(wait, 200.0)


if __name__ == "__main__":
    unittest.main()
