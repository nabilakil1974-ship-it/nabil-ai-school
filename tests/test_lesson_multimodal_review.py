"""Local contract tests; no Drive or model credentials required."""
import json
import unittest
import types
from unittest.mock import patch

from scripts import nabil_lesson_factory as factory


class FakeResponse:
    def __init__(self, approved):
        self.choices = [type("Choice", (), {"message": type("Message", (), {
            "content": json.dumps({"approved": approved, "specific_reason": "image checked"})
        })()})()]


class FakeClient:
    def __init__(self, approved):
        self.approved = approved
        self.messages = None
        self.chat = type("Chat", (), {})()
        self.chat.completions = type("Completions", (), {})()
        self.chat.completions.create = self.create

    def create(self, **kwargs):
        self.messages = kwargs["messages"]
        return FakeResponse(self.approved)


class ReviewTests(unittest.TestCase):
    providers = [("openai", "key1", None, "model-a"),
                 ("gemini", "key2", "url2", "model-b"),
                 ("groq", "key3", "url3", "model-c")]

    def test_distinct_reviewer_required(self):
        with patch.object(factory, "configured_providers", return_value=[
            ("openai", "key", None, "model-a")]):
            with self.assertRaisesRegex(RuntimeError, "INDEPENDENT_REVIEWER_UNAVAILABLE"):
                factory.independent_reviewer("openai", "model-a", "gemini", "model-b")

    def test_reviewer_cannot_be_visual_extractor(self):
        with patch.object(factory, "configured_providers", return_value=self.providers), patch.dict(
                "os.environ", {"NABIL_REVIEWER_PROVIDER": "gemini",
                               "NABIL_LESSON_REVIEW_MODEL": "review-vision"}):
            with self.assertRaisesRegex(RuntimeError, "INDEPENDENT_REVIEWER_UNAVAILABLE"):
                factory.independent_reviewer("openai", "model-a", "gemini", "model-b")

    def test_two_providers_cannot_fill_three_roles(self):
        with patch.object(factory, "configured_providers", return_value=self.providers[:2]), patch.dict(
                "os.environ", {"NABIL_REVIEWER_PROVIDER": "openai",
                               "NABIL_LESSON_REVIEW_MODEL": "third-model"}):
            with self.assertRaisesRegex(RuntimeError, "INDEPENDENT_REVIEWER_UNAVAILABLE"):
                factory.independent_reviewer("gemini", "model-b", "openai", "model-a")

    def test_reviewer_model_cannot_equal_visual_model(self):
        with patch.object(factory, "configured_providers", return_value=self.providers), patch.dict(
                "os.environ", {"NABIL_REVIEWER_PROVIDER": "groq",
                               "NABIL_LESSON_REVIEW_MODEL": "model-b"}):
            with self.assertRaisesRegex(RuntimeError, "INDEPENDENT_REVIEWER_UNAVAILABLE"):
                factory.independent_reviewer("openai", "model-a", "gemini", "model-b")

    def test_third_provider_selected(self):
        with patch.object(factory, "configured_providers", return_value=self.providers), patch.dict(
                "os.environ", {"NABIL_REVIEWER_PROVIDER": "groq",
                               "NABIL_LESSON_REVIEW_MODEL": "review-vision"}):
            self.assertEqual(factory.independent_reviewer(
                "openai", "model-a", "gemini", "model-b")[0], "groq")

    def test_three_roles_are_recorded_in_map_and_attempt(self):
        evidence_map, attempt = {}, {}
        for role, provider, model in (("visual_extractor", "gemini", "vision-a"),
                                      ("generator", "openai", "text-b"),
                                      ("reviewer", "groq", "vision-c")):
            factory.record_role_provenance(evidence_map, attempt, role, provider, model)
            self.assertEqual(evidence_map[f"{role}_provider"], provider)
            self.assertEqual(attempt[f"{role}_model"], model)
        self.assertEqual(evidence_map, attempt)

    def test_visual_extractor_requires_three_providers(self):
        with patch.object(factory, "configured_providers", return_value=self.providers[:2]):
            with self.assertRaisesRegex(RuntimeError, "THREE_INDEPENDENT_PROVIDERS_REQUIRED"):
                factory.visual_candidates({15: b"image"})

    def test_generator_skips_extractor_and_reserved_reviewer(self):
        fake_openai = types.SimpleNamespace(OpenAI=lambda **kw: FakeClient(True))
        with patch.dict("sys.modules", {"openai": fake_openai}), patch.dict(
                "os.environ", {"NABIL_REVIEWER_PROVIDER": "groq"}), patch.object(
                factory, "configured_providers", return_value=self.providers), patch.object(
                factory, "parse_provider_json", return_value={"title": "Draft"}), patch.object(
                factory, "attach_evidence"):
            _, provider, model = factory.generate("Demo", [(15, "source")], "en",
                {"evidence": {}}, visual_provider="gemini", visual_model="model-b")
        self.assertEqual((provider, model), ("openai", "model-a"))

    def test_visual_candidate_is_not_an_approval(self):
        entry = {"page": 14, "type": "visual_candidate", "figure_id": "Fig. A",
                 "text": "two visible lines", "accompanying_question": "What do you observe?",
                 "verified": False}
        catalog = factory.evidence_catalog([(14, "Book text")], {"P14-VIS-1": entry})
        self.assertFalse(catalog["P14-VIS-1"]["verified"])
        self.assertEqual(catalog["P14-VIS-1"]["page"], 14)
        evidence_map = factory.source_evidence_map("Demo", [(14, "Book text")],
            catalog, "gemini", "vision-model")
        self.assertEqual(evidence_map["visual_extractor_provider"], "gemini")
        self.assertEqual(evidence_map["visual_extractor_model"], "vision-model")
        self.assertEqual(evidence_map["visual_evidence_status"],
                         "unverified_candidates")

    def test_unsupported_visual_claim_rejected_and_original_image_sent(self):
        client = FakeClient(False)
        with patch.object(factory, "parse_provider_json", side_effect=lambda *a: json.loads(
                a[3].choices[0].message.content)):
            verdict = factory.review_claim(client, "reviewer", "model-b",
                {"answer": "curved liquid surface"}, b"actual-page-image", "What do you observe?", 14)
        self.assertFalse(verdict["approved"])
        sent = client.messages[1]["content"]
        self.assertEqual(sent[1]["image_url"]["url"],
            "data:image/jpeg;base64,YWN0dWFsLXBhZ2UtaW1hZ2U=")
        self.assertIn('"pdf_page": 14', sent[0]["text"])

    def test_supported_visual_claim_can_pass_only_after_image_review(self):
        client = FakeClient(True)
        with patch.object(factory, "parse_provider_json", side_effect=lambda *a: json.loads(
                a[3].choices[0].message.content)):
            verdict = factory.review_claim(client, "reviewer", "model-b",
                {"answer": "a visible right angle", "evidence_id": "P15-VIS-1"},
                b"source-image", "Activity question", 15)
        self.assertTrue(verdict["approved"])
        self.assertIn("data:image/jpeg;base64,", client.messages[1]["content"][1]["image_url"]["url"])

    def test_missing_image_fails_closed(self):
        fake_openai = types.SimpleNamespace(OpenAI=lambda **kw: FakeClient(True))
        with patch.dict("sys.modules", {"openai": fake_openai}), patch.object(
                factory, "independent_reviewer", return_value=(
                "gemini", "key", "url", "model-b")):
            result = factory.scientific_review({"introduction": "claim",
                 "introduction_source_page": 14}, [(14, "question")], {},
                 "openai", "model-a", "gemini", "model-b")
        self.assertFalse(result["pass"])


if __name__ == "__main__":
    unittest.main()
