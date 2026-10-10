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

    def test_v18_embedded_board_and_golden(self):
        import json
        from bs4 import BeautifulSoup
        from scripts.nabil_factory.offline_translation import translate_v18_embedded_board_html
        payload={"lang":"en","title":"The power","slides":[
            {"title":"The power","steps":[{"text":"We observe $2^3=8$","formula":"2^3=8"}]}],
            "golden":{"sections":[{"label":"The power","items":["We observe $2^3=8$"]}]}}
        document='<script type="application/json" id="nabilV18Data">'+json.dumps(payload)+'</script>'
        translated, count=translate_v18_embedded_board_html(document,French())
        data=json.loads(BeautifulSoup(translated,"html.parser").find("script").string)
        self.assertEqual(count,1)
        self.assertEqual(data["lang"],"fr")
        self.assertEqual(data["slides"][0]["title"],"La puissance")
        self.assertEqual(data["golden"]["sections"][0]["label"],"La puissance")
        self.assertIn("$2^3=8$",data["slides"][0]["steps"][0]["text"])
        self.assertEqual(data["slides"][0]["steps"][0]["formula"],"2^3=8")
    def test_unsupported_pair_fails_closed(self):
        from scripts.nabil_factory.offline_translation import get_free_translator
        with self.assertRaises(OfflineTranslationUnavailable):
            get_free_translator("en","ar","opus")
if __name__=="__main__":unittest.main()
