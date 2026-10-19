import unittest
from scripts.nabil_factory.factory.annotation_gate import audit_scene, audit_lesson, property_claims


class AnnotationGate(unittest.TestCase):
    def test_claims(self):
        self.assertGreaterEqual(property_claims("AB = PM، و∠A = ∠P"), 2)
        self.assertEqual(property_claims("180° ÷ 3 = 60°"), 0)

    def test_fail_without_figure(self):
        sc = {"id": "s", "steps": [{"t": "text", "text": "AB = PM"}]}
        self.assertEqual(audit_scene(sc)["status"], "FAIL_NO_FIGURE")

    def test_pass_with_annotate(self):
        sc = {"id": "s", "steps": [{"t": "draw", "draw": "annotate", "args": {"items": [1]}}, {"t": "text", "text": "AB = PM"}]}
        self.assertEqual(audit_scene(sc)["status"], "PASS_MARKED")

    def test_prebaked_is_unverified(self):
        sc = {"id": "s", "steps": [{"t": "draw", "draw": "congruenceCases", "args": {}}, {"t": "text", "text": "AB = PM"}]}
        self.assertEqual(audit_scene(sc)["status"], "UNVERIFIED_PREBAKED_DRAW")
        self.assertEqual(audit_lesson({"scenes": [sc]})["verdict"], "UNVERIFIED")


if __name__ == "__main__":
    unittest.main()
