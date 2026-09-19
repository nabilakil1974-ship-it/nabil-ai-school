"""Isolated backend drawing-protocol regressions (stdlib-only CI).

Exercise the ACTUAL extract_drawings / sphere recovery functions parsed from
routes_chat.py, without importing the web service and its DB/AI dependencies.
"""
import ast
import json
import re
import unittest
from pathlib import Path


ROUTES = Path(__file__).resolve().parents[1] / "app/api/routes_chat.py"
tree = ast.parse(ROUTES.read_text(encoding="utf-8"))
names = {"extract_drawings", "_nabil_exact_sphere_drawing"}
selected = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in names]
assert len(selected) == len(names), "Actual backend drawing functions must exist"
module = ast.Module(body=selected, type_ignores=[])
ast.fix_missing_locations(module)
context = {
    "json": json,
    "re": re,
    "_normalize_drawing": lambda item: item if isinstance(item, dict) and item.get("type") else None,
    "validate_drawing_strict": lambda item: isinstance(item, dict) and item.get("type") == "sphere",
}
exec(compile(module, str(ROUTES), "exec"), context)


class DrawingProtocolRecoveryTests(unittest.TestCase):
    def test_bare_json_after_text_on_same_line(self):
        reply, drawings = context["extract_drawings"](
            'See this sphere. DRAWINGS_JSON: [{"type":"sphere","radius":3,"title":"Sphere"}]'
        )
        self.assertEqual(len(drawings), 1)
        self.assertEqual(drawings[0]["radius"], 3)
        self.assertEqual(reply, "See this sphere.")
        self.assertNotIn("DRAWINGS_JSON", reply)

    def test_bare_json_with_trailing_answer(self):
        reply, drawings = context["extract_drawings"](
            'Here is the figure.\nDRAWINGS_JSON:\n[{"type":"sphere","radius":5}]\nDone.'
        )
        self.assertEqual(len(drawings), 1)
        self.assertIn("Done.", reply)
        self.assertNotIn('"radius"', reply)

    def test_wrapped_json_still_works(self):
        reply, drawings = context["extract_drawings"](
            '<DRAWINGS_JSON>[{"type":"sphere","radius":3}]</DRAWINGS_JSON>'
        )
        self.assertEqual(len(drawings), 1)
        self.assertEqual(reply, "")

    def test_malformed_protocol_not_leaked(self):
        reply, drawings = context["extract_drawings"](
            'A sphere. DRAWINGS_JSON: [{"type":"sphere", "radius":3'
        )
        self.assertEqual(drawings, [])
        self.assertEqual(reply, "A sphere.")

    def test_exact_sphere_radius_and_units(self):
        figure = context["_nabil_exact_sphere_drawing"](
            "Draw a sphere with radius equal to 3 cm. Only the figure."
        )
        self.assertIsNotNone(figure)
        self.assertEqual(figure["radius"], 3)
        self.assertEqual(figure["type"], "sphere")
        self.assertIn("3 cm", figure["radius_label"])

    def test_sphere_wins_over_hallucinated_dimensions(self):
        source = ROUTES.read_text(encoding="utf-8")
        self.assertIn("if exact_sphere and not compound_solids:", source)
        self.assertIn("drawings = [exact_sphere]", source)
        self.assertIn("compound_solids", source)

    def test_missing_radius_does_not_invent_one(self):
        self.assertIsNone(context["_nabil_exact_sphere_drawing"]("Draw a sphere."))


if __name__ == "__main__":
    unittest.main(verbosity=2)
