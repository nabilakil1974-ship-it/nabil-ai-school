"""Regression build for the owner's warm tutor, terminology and visual-only requests.

Runs without Railway credentials, AI providers or database connectivity.
"""
import ast
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAT = (ROOT / "app/api/routes_chat.py").read_text(encoding="utf-8")
OPEN = (ROOT / "app/static/nabil_open_tutor_v1.js").read_text(encoding="utf-8")
CSS = (ROOT / "app/static/nabil_reference_theme.css").read_text(encoding="utf-8")


def isolated_figure_helpers():
    tree = ast.parse(CHAT, filename="routes_chat.py")
    names = {"_nabil_figure_only_request", "_nabil_exact_sphere_drawing"}
    selected = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name in names
    ]
    assert {node.name for node in selected} == names
    ns = {
        "re": re,
        "validate_drawing_strict": lambda d: (
            d.get("type") == "sphere"
            and isinstance(d.get("radius"), (int, float))
            and d["radius"] > 0
        ),
    }
    exec(compile(ast.Module(body=selected, type_ignores=[]), "routes_chat.py", "exec"), ns)
    return ns


class TutorOwnerContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.helper = isolated_figure_helpers()

    def test_figure_only_intent_in_three_languages(self):
        recognize = self.helper["_nabil_figure_only_request"]
        for request in (
            "Draw a sphere with radius equal to 5 cm. Give me the figure, only the figure.",
            "Just the figure, please.",
            "Dessine une sphère, uniquement la figure.",
            "ارسم كرة نصف قطرها 3 سم، بس الرسمة.",
            "بدي الرسم فقط",
        ):
            with self.subTest(request=request):
                self.assertTrue(recognize(request))
        for request in ("Please explain the sphere.", "Study the function ln x."):
            with self.subTest(request=request):
                self.assertFalse(recognize(request))

    def test_exact_radius_sphere_and_no_hallucinated_size(self):
        sphere = self.helper["_nabil_exact_sphere_drawing"]
        for radius in (3, 5):
            spec = sphere(
                f"Draw a sphere with radius equal to {radius} cm. Only the figure."
            )
            self.assertIsNotNone(spec)
            self.assertEqual(spec["type"], "sphere")
            self.assertEqual(spec["radius"], radius)
            self.assertEqual(spec["labels"]["radius"], f"r = {radius} cm")
        self.assertIsNone(sphere("Draw a sphere, only the figure."))
        self.assertIsNone(sphere("Draw a cylinder with radius 5 cm."))
        self.assertIsNone(sphere("Draw a sphere with radius 0 cm."))

    def test_student_side_term_mapping_no_inversion(self):
        for fragment in (
            "SPOKEN_TUTOR_COMPANION_RULE_V2",
            "البسط = numerator",
            "المقام = denominator",
            "French",
            "Physics",
            "Chemistry",
            "Biology",
            "روضة",
            "4–6",
            "7–9",
            "الثانوي",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, CHAT)
        self.assertIn("HOME_TUTOR_INTENT_AND_SPEECH_V1", CHAT)
        self.assertIn("general_exercises_mode and str(teaching_mode", CHAT)
        self.assertIn("Do NOT label a function-study request as Language / Grammar", CHAT)
        self.assertIn("FIGURE_ONLY_RESPONSE_CONTRACT_V1", CHAT)
        self.assertIn("if figure_only_request:", CHAT)
        self.assertIn("drawings = [exact_sphere]", CHAT)
        self.assertIn("if exact_visual:", CHAT)
        self.assertIn("if figure_only_request and image_bytes is None", CHAT)

    def test_open_figure_is_visual_not_faux_exercise(self):
        for fragment in (
            "figureOnly",
            "if(figureOnly&&!hasVisual)throw Error",
            "if(!figureOnly)explanation.appendChild(text)",
            "if(!figureOnly)toolsHost.append(copy,read,stop)",
            "if(!shown.figureOnly&&spoken",
            "renderNabilDiagram",
            "prepareSpeechTypewriter",
            "nabilSpeakClear",
            "nabilVoicePace",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, OPEN)

    def test_owner_visual_board_left_robot_and_unclipped_mobile(self):
        for fragment in (
            "OWNER_HOME_WIDE_BOARD_V6",
            "background-position:left center!important",
            "width:clamp(570px,calc(100vw - 590px),1150px)",
            "#nabilOpenExplanation",
            "#nabilOpenVisuals .nabil-open-visual svg",
            "min-height:clamp(300px,34vw,570px)",
            "@media (max-width:900px)",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, CSS)


if __name__ == "__main__":
    unittest.main(verbosity=2)
