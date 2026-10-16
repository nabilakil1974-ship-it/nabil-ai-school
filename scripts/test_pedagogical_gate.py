"""PEDAGOGICAL_GOLDEN_GATE must reject the exact failures seen on the first Powers lesson."""
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.nabil_factory.cards.v18_board import render_v18_smart_board, build_golden_spec
from scripts.nabil_factory.factory import pedagogical_gate as g


def act(cid, sentences, kind="POWER_EXPLORER"):
    return {"concept_id": cid, "lab_spec": {"kind": kind},
            "teaching_steps": [{"sentence": s, "kind": "step"} for s in sentences]}


def sol(*steps):
    return {"solution_status": "SOLVED", "number": 1, "_pre_solved_solution": {"steps": list(steps), "final_answer": "x"}}


GOOD_STEPS = ["Given: 2^3 × 2^4", "Rule: same base, add the exponents because a^m × a^n = a^(m+n)",
              "Substitution: 2^(3+4)", "Calculation: 2^7 = 128", "Verification: 8 × 16 = 128"]


class Gate(unittest.TestCase):
    def cand(self, acts=None, exs=None):
        acts = acts if acts is not None else [act("C1", ["Imagine doubling grains on a chessboard", "Each square holds twice the previous one"])]
        return {"theory": {"activities": acts}, "exercises": exs if exs is not None else [sol(*GOOD_STEPS)],
                "page_a_html": "", "page_b_html": ""}

    def test_filler_is_rejected(self):
        c = self.cand([act("C1", ["We now explain the next step: 2^3 = 8"])])
        with self.assertRaisesRegex(g.PedagogicalGateFailed, "GENERIC_OR_REPEATED_EXPLANATION"):
            g.check_explanations(c)

    def test_repeated_openings_are_rejected(self):
        c = self.cand([act("C1", ["Now we compute the first value", "Now we compute the second value", "Now we compute the third value"])])
        with self.assertRaisesRegex(g.PedagogicalGateFailed, "GENERIC_OR_REPEATED_EXPLANATION"):
            g.check_explanations(c)

    def test_text_reveal_labs_are_rejected_for_math(self):
        c = self.cand([act(f"C{i}", [f"idea {i} explained differently {i}"], "EVIDENCE_REVEAL") for i in range(4)])
        with self.assertRaisesRegex(g.PedagogicalGateFailed, "LAB_TEXT_REVEAL_INSTEAD_OF_INTERACTION"):
            g.check_labs(c, "mathematics")
        g.check_labs(c, "history")  # other subjects keep the evidence fallback

    def test_real_labs_pass(self):
        g.check_labs(self.cand(), "mathematics")

    def test_unexplained_solutions_are_rejected(self):
        c = self.cand(exs=[sol("2^3 × 2^4 = 2^7", "2^7 = 128")] * 5)
        with self.assertRaisesRegex(g.PedagogicalGateFailed, "SOLUTION_STEPS_NOT_EXPLAINED"):
            g.check_solutions(c, "mathematics")
        self.assertEqual(g.check_solutions(self.cand(), "mathematics")["explained"], 1)

    def test_raw_math_in_data_is_rejected(self):
        acts = [{"concept_id": "C1", "title": "T", "lab_html": "", "allow_no_lab": True,
                 "teaching_steps": [{"sentence": "x", "kind": "step"}], "conclusion": "ok"}]
        spec = build_golden_spec("T", acts, "en", subject="mathematics")
        page = render_v18_smart_board("T", acts, "en", golden_spec=spec)
        g.check_math_data(page)  # canonical form passes
        bad = page.replace('"text": "x"', '"text": "2^(3 * 4)"')
        self.assertNotEqual(bad, page)
        with self.assertRaisesRegex(g.PedagogicalGateFailed, "DISTORTED_MATH"):
            g.check_math_data(bad)

    def test_review_is_required(self):
        with self.assertRaisesRegex(g.PedagogicalGateFailed, "INDEPENDENT_SCIENTIFIC_REVIEW_MISSING"):
            g.check_independent_review({"review_status": "UNREVIEWED"})
        g.check_independent_review({"review_status": "REVIEWED"})

    def test_browser_gate_passes_good_and_rejects_raw_math(self):
        acts = [{"concept_id": "C1", "title": "Powers", "lab_html": "", "allow_no_lab": True,
                 "teaching_steps": [{"sentence": "(a × b)^m = a^m × b^m", "kind": "step"},
                                    {"sentence": "So 2^(3 * 4) = 2^12", "kind": "step"}],
                 "conclusion": "10^(4 * 2) = 10^8"}]
        spec = build_golden_spec("Q", acts, "en", subject="mathematics")
        page = "<html><head><meta charset='utf-8'></head><body>" + render_v18_smart_board("Q", acts, "en", golden_spec=spec) + "</body></html>"
        with TemporaryDirectory() as tmp:
            f = Path(tmp) / "ok.html"
            f.write_text(page, encoding="utf-8")
            rep = g.run_browser_gate(str(f), "ok")
            self.assertTrue(rep["controls"]["paused"] and rep["controls"]["resumed"])
            # a page whose math is injected raw (bypassing the canonical renderer) must fail
            bad = page.replace('<nav class="nb-ctl"', "<p id='rawx'>apply 2^3 * 4 here</p><nav class=\"nb-ctl\"")
            self.assertNotEqual(bad, page)
            f2 = Path(tmp) / "bad.html"
            f2.write_text(bad, encoding="utf-8")
            with self.assertRaisesRegex(g.PedagogicalGateFailed, "RENDERED_RAW_MATH|CONTROLS_BROKEN"):
                g.run_browser_gate(str(f2), "bad")


if __name__ == "__main__":
    unittest.main()
