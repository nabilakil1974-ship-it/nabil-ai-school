"""Deterministic tests; no AI credits or Argos downloads."""
import unittest
from scripts.nabil_factory.offline_translation import (
    translate_html_offline, translate_scientific_text, OfflineTranslationUnavailable,
)
class French:
    def translate(self, text):
        return text.replace("We observe", "Nous observons").replace("The power", "La puissance")
class Broken:
    def translate(self, text):
        return text.replace("NABILPROTECTEDTOKEN0END", "MISSING")
class OfflineTranslationTests(unittest.TestCase):
    def test_preserve_math_and_translate_visible_prose(self):
        html='<html><body><p>We observe \\(2^3=8\\).</p><script>const message="The power";</script><math>2^3</math></body></html>'
        output, report=translate_html_offline(html,"en","fr",French())
        self.assertIn("Nous observons",output)
        self.assertIn("\\(2^3=8\\)",output)
        self.assertIn('const message="The power"',output)
        self.assertFalse(report["complete"],"JS-driven boards are not yet translated")
        self.assertEqual(report["mode"],"offline_argos")
    def test_fail_closed_if_math_placeholder_is_changed(self):
        with self.assertRaises(OfflineTranslationUnavailable):
            translate_scientific_text(r"We observe \\(x^2=4\\)",Broken())
    def test_no_untranslated_language_claim(self):
        _, report=translate_html_offline("<p>The power</p>","en","fr",French())
        self.assertNotEqual(report["complete"],True)
    def test_identity(self):
        html="<p>Original language</p>"
        self.assertEqual(translate_html_offline(html,"fr","fr")[0],html)
if __name__=="__main__":unittest.main()
