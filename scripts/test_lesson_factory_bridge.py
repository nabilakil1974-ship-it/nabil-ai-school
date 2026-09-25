"""Contract tests for the owner-controlled NABIL lesson factory bridge.

Tests do NOT call AI, Google Drive, launch a real factory, or claim pilot QA.
"""
import os
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi import HTTPException

from app.api import routes_lesson_factory as bridge

ROOT = Path(__file__).resolve().parents[1]


class FactoryBridgeContractTest(unittest.TestCase):
    def setUp(self):
        bridge._jobs.clear()

    def tearDown(self):
        bridge._jobs.clear()

    def test_catalog_is_actual_source_locked_pilot(self):
        entries = bridge.factory_catalog(grade="الصف السابع", subject="فيزياء")["lessons"]
        self.assertTrue(any(
            item["lesson_id"] == "G07-PHYSICS-001" and
            item["title"] == "Solids and Liquids"
            for item in entries
        ))

    def test_prepare_requires_server_secret_not_ai_key(self):
        with patch.dict(os.environ, {"NABIL_FACTORY_OWNER_TOKEN": "test-owner"}, clear=False):
            with self.assertRaises(HTTPException) as error:
                bridge.prepare({"lesson_id": "G07-PHYSICS-001"}, x_nabil_factory_token="invalid")
            self.assertEqual(403, error.exception.status_code)

    def test_pilot_preparation_queues_without_claiming_success(self):
        with patch.dict(os.environ, {
            "NABIL_FACTORY_OWNER_TOKEN": "test-owner",
            "NABIL_FACTORY_ENABLED": "1",
        }, clear=False), patch.object(bridge.threading.Thread, "start", return_value=None):
            result = bridge.prepare({"lesson_id": "G07-PHYSICS-001"},
                                    x_nabil_factory_token="test-owner")
            self.assertEqual("RUNNING", result["status"])
            self.assertNotIn("url", result)
            again = bridge.prepare({"lesson_id": "G07-PHYSICS-001"},
                                   x_nabil_factory_token="test-owner")
            self.assertEqual("RUNNING", again["status"])
            status = bridge.preparation_status(
                "G07-PHYSICS-001", x_nabil_factory_token="test-owner")
            self.assertEqual("RUNNING", status["status"])

    def test_view_fail_closed_before_quality_gates(self):
        with self.assertRaises(HTTPException) as error:
            bridge.view_local_lesson("G07-PHYSICS-001", "wrong")
        self.assertEqual(404, error.exception.status_code)

    def test_picker_script_is_loaded_before_drive_handler(self):
        main = (ROOT / "app/main.py").read_text(encoding="utf-8")
        self.assertLess(main.index("nabil_factory_prepare_v1.js"),
                        main.index("nabil_drive_prepared_lesson_v1.js"))
        js = (ROOT / "app/static/nabil_factory_prepare_v1.js").read_text(encoding="utf-8")
        self.assertIn("/api/interactive-lessons/factory/prepare", js)
        self.assertIn("X-Nabil-Factory-Token", js)
        self.assertIn("QA_PASSED_LOCAL", js)
        self.assertNotIn("OPENROUTER_API_KEY", js)


if __name__ == "__main__":
    unittest.main()
