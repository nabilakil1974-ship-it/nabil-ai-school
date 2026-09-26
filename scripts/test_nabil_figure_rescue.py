import unittest

from scripts.nabil_lesson_factory import _normalize_targeted_figure_payload


class TargetedFigureRescueSchemaTest(unittest.TestCase):
    def test_array_root(self):
        rows = [{"printed_label": "1"}]
        self.assertEqual(_normalize_targeted_figure_payload(rows, 14), rows)

    def test_wrapped_root(self):
        rows = [{"printed_label": "1"}]
        self.assertEqual(
            _normalize_targeted_figure_payload({"figures": rows}, 14), rows)

    def test_list_wrapper(self):
        rows = [{"printed_label": "1"}]
        self.assertEqual(
            _normalize_targeted_figure_payload({"list": rows}, 14), rows)

    def test_invalid_shape_fails_closed(self):
        with self.assertRaises(RuntimeError):
            _normalize_targeted_figure_payload(
                {"unexpected": "value"}, 14)


if __name__ == "__main__":
    unittest.main()
