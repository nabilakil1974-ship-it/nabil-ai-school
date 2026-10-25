from __future__ import annotations
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.services import lesson_package_registry as reg


class TestLessonPackageRegistry(unittest.TestCase):
    def test_subjects_are_universal(self):
        self.assertEqual(reg.canonical_subject("Mathematics"), "MATH")
        self.assertEqual(reg.canonical_subject("تاريخ"), "HISTORY")
        self.assertEqual(reg.canonical_subject("géographie"), "GEOGRAPHY")
        self.assertEqual(reg.canonical_subject("لغة عربية"), "ARABIC")
        self.assertEqual(reg.canonical_subject("informatique"), "COMPUTER")

    def test_ready_package_and_path_guard(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            pkg = root / "G07-PHYSICS-001"
            pkg.mkdir()
            (pkg / "lesson.html").write_text("<html>ok</html>", encoding="utf-8")
            (pkg / "manifest.json").write_text(json.dumps({
                "lesson_id": "G07-PHYSICS-001",
                "title": "Solids and Liquids",
                "status": "READY",
                "artifacts": {
                    "lesson_html": "lesson.html",
                    "bad": "../escape.html",
                },
            }), encoding="utf-8")
            with patch.object(reg, "PACKAGE_ROOT", root), patch.object(
                reg, "CATALOGUE_PATH", root / "none.json"
            ):
                rows = reg.package_rows()
                self.assertEqual(len(rows), 1)
                self.assertTrue(rows[0]["runtime_ready"])
                self.assertIn("lesson_html", rows[0]["artifacts"])
                self.assertNotIn("bad", rows[0]["artifacts"])
                self.assertEqual(
                    reg.get_artifact("G07-PHYSICS-001", "lesson_html"),
                    (pkg / "lesson.html").resolve(),
                )

    def test_not_ready_without_lesson_html(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            pkg = root / "G12-MATH-GS-001"
            pkg.mkdir()
            (pkg / "manifest.json").write_text(json.dumps({
                "lesson_id": "G12-MATH-GS-001",
                "status": "READY",
                "artifacts": {"teacher_json": "missing.json"},
            }), encoding="utf-8")
            with patch.object(reg, "PACKAGE_ROOT", root), patch.object(
                reg, "CATALOGUE_PATH", root / "none.json"
            ):
                self.assertFalse(reg.package_rows()[0]["runtime_ready"])


if __name__ == "__main__":
    unittest.main()
