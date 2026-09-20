"""Regression: exact printed-page lessons may not invent activities or miscount ions."""
import pathlib
import unittest

from app.core.textbook_lesson_gate import lesson_page_issues

PAGE_56 = (
    "Sodium atom K2 L8 M1 Chlorine atom K2 L8 M7 Sodium chloride NaCl. "
    "The transfer of electrons can be represented by the dot structure. "
    "b) Describing the formation of ionic bond in magnesium fluoride. "
    "Mg K2 L8 M2 and F K2 L7."
)


class ExactTextbookLessonGateTests(unittest.TestCase):
    def check(self, reply, page=56, text=PAGE_56, subject="Chemistry"):
        return lesson_page_issues(reply, text, subject=subject,
                                  printed_page=page, strict_single_page=True)

    def test_na_cl_mgf2_source_order_passes(self):
        self.assertEqual(self.check(
            "## Sodium chloride NaCl\nNa loses 1 electron to Cl. "
            "Na+ and Cl- attract.\n## Magnesium fluoride MgF2\n"
            "Mg transfers one electron to EACH of two F atoms; "
            "Mg2+ + 2F- gives MgF2."), [])

    def test_missing_second_real_page_section_rejected(self):
        self.assertTrue(any("magnesium fluoride" in v for v in
                            self.check("## Sodium chloride NaCl\nNa+ Cl- attract.")))

    def test_fake_book_figure_and_activity_rejected_on_any_page(self):
        issues = self.check(
            "## Sodium chloride NaCl\n## Magnesium fluoride MgF2\n"
            "According to Fig. 15, Activity 3 compares salt and sugar.")
        self.assertTrue(any("figure 15" in v for v in issues))
        self.assertTrue(any("activity 3" in v for v in issues))
        assert self.check("See Fig. 4 on printed page 73.", page=73,
                          text="Fig. 4: convergent lens.", subject="Physics") == []

    def test_chemistry_not_calculus(self):
        self.assertTrue(any("math" in v for v in
                            self.check("## Domain\n(0,infinity)\n## NaCl and MgF2")))

    def test_alternate_page_is_not_hardcoded_to_page_56(self):
        self.assertEqual(
            self.check("The convex lens changes ray direction.",
                       page=23, text="A convex lens changes ray direction.",
                       subject="Physics"),
            [],
        )

    def test_page_57_crystal_lattice_and_activity_2(self):
        page = (
            "2.2.2 Crystal Lattice. Sodium chloride is shown in Fig. 14. "
            "Activity 2 Build using ball-and-stick models crystal lattice arrangements."
        )
        good = (
            "Crystal lattice is an electrically neutral regular arrangement. "
            "Fig. 14 shows the NaCl crystal. Activity 2 asks us to build using "
            "ball-and-stick models crystal lattice arrangements."
        )
        self.assertEqual(self.check(good, page=57, text=page), [])
        bad = (
            "Magnesium fluoride MgF2 is an ionic bond. Activity 2: identify the "
            "lattice type and draw the unit cell on the next page."
        )
        problems = self.check(bad, page=57, text=page)
        self.assertTrue(any("crystal lattice" in x for x in problems))
        self.assertTrue(any("Activity 2" in x for x in problems))

    def test_neutral_fluorine_noble_gas_configuration(self):
        source = "Fluorine has the electronic configuration [He]2s2 2p5."
        bad = "Fluorine gains an electron: [Ne]2s²2p⁵ → [Ne]."
        issues = self.check(bad, page=57, text=source)
        self.assertTrue(any("fluorine" in x for x in issues))

    def test_function_study_appender_is_disabled_for_book_lessons(self):
        source = pathlib.Path("app/api/routes_chat.py").read_text("utf-8")
        self.assertIn("and not lesson_start_from_book", source)
        self.assertIn("BOOK_PAGE_DELIVERY_REJECTED", source)
        self.assertLess(source.index("BOOK_PAGE_DELIVERY_REJECTED"),
                        source.index("LESSON_PACKAGE_CACHE_SAVED"))

    def test_chemistry_trailing_calculus_is_stripped(self):
        from app.core.lesson_output_guard import sanitize_chemistry_lesson
        sample = (
            "Crystal lattice and Activity 2.\n## ملخص الدرس للدفتر\n"
            "Build the lattice.\n### Domain\n(0, infinity)\n"
            "### Limits\nlim x = 0\n### Derivative\nf'(x)=2x"
        )
        cleaned = sanitize_chemistry_lesson(sample.replace("\\\n", "\n"), "Chemistry")
        self.assertIn("Build the lattice.", cleaned)
        self.assertNotIn("### Domain", cleaned)
        self.assertNotIn("### Limits", cleaned)
        self.assertEqual(sanitize_chemistry_lesson(sample, "Mathematics"), sample)

    def test_route_guards_before_caching_or_saving(self):
        src = pathlib.Path("app/api/routes_chat.py").read_text("utf-8")
        self.assertIn("BOOK_PAGE_QUALITY_REJECTED", src)
        self.assertIn("raw_reply = _replacement", src)
        self.assertLess(src.index("BOOK_PAGE_QUALITY_REJECTED"),
                        src.index("LESSON_PACKAGE_CACHE_SAVED"))


if __name__ == "__main__":
    unittest.main()
