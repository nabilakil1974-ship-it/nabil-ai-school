"""NABIL open tutor handles platform support and uploaded WhatsApp voices."""
import ast
from pathlib import Path
import unittest


class PlatformSelfHelpTests(unittest.TestCase):
    def test_chat_includes_platform_knowledge_only_for_open_tutor(self):
        route = Path("app/api/routes_chat.py").read_text("utf-8")
        ast.parse(route)
        self.assertIn("from app.core.platform_support import PLATFORM_HELP", route)
        self.assertIn('if is_home_live_tutor:\n        educational_context += "\\n\\n" + PLATFORM_HELP', route)

    def test_platform_information_is_correctly_scoped(self):
        support = Path("app/core/platform_support.py").read_text("utf-8")
        ast.parse(support)
        for key in ("/labs/chemistry", "/labs/light", "/labs/math",
                    "/labs/secondary-physics", "فويس واتساب", "no repository",
                    "beyond NABIL"):
            self.assertIn(key, support)

    def test_voice_files_are_uploaded_to_same_transcription_path(self):
        tutor = Path("app/static/nabil_open_tutor_v1.js").read_text("utf-8")
        gateway = Path("app/services/ai_gateway.py").read_text("utf-8")
        ast.parse(gateway)
        for key in ('nabilOpenVoiceFile', 'request({audio:file})',
                    'data.append("audio",audio,originalName'):
            self.assertIn(key, tutor)
        self.assertIn('subprocess.run(', gateway)
        self.assertIn('student_voice.mp3', gateway)


if __name__ == "__main__":
    unittest.main()
