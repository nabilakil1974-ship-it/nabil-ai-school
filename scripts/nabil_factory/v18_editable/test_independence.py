"""V18 import/integrity regression; execute with python -m unittest."""
from __future__ import annotations
import importlib
import unittest

ROOT = "scripts.nabil_factory.v18_editable"
PARTS = ("pacing", "cards", "labs", "terminology", "preparation")

class TestV18EditableStructure(unittest.TestCase):
    def test_package_and_all_modules_import(self):
        package = importlib.import_module(ROOT)
        package.settings.validate_settings()
        for part in PARTS:
            mod = importlib.import_module(ROOT + "." + part)
            self.assertTrue(isinstance(mod.CONFIG, dict))
            self.assertTrue(mod.CONFIG)

    def test_registry_contains_every_component(self):
        settings = importlib.import_module(ROOT + ".settings")
        self.assertEqual(set(settings.SETTINGS), set(PARTS))

    def test_component_settings_cannot_mutate_registry(self):
        settings = importlib.import_module(ROOT + ".settings")
        old = settings.SETTINGS["pacing"]["speech_rate"]
        mutable = settings.ui_settings("pacing")
        mutable["speech_rate"] = 99
        self.assertEqual(settings.SETTINGS["pacing"]["speech_rate"], old)
        with self.assertRaises(TypeError):
            settings.SETTINGS["pacing"]["speech_rate"] = 99

    def test_unknown_component_fails_closed(self):
        settings = importlib.import_module(ROOT + ".settings")
        with self.assertRaises(KeyError):
            settings.ui_settings("nonexistent")

if __name__ == "__main__":
    unittest.main()
