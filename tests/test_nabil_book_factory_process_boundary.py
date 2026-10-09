import os
import subprocess
import sys
import unittest


class BookFactoryProcessBoundaryTests(unittest.TestCase):
    CASES = {
        "TRANSIENT": 75,
        "PROVIDER_UNAVAILABLE": 78,
        "NEEDS_ATTENTION": 79,
        "SCIENTIFIC_BLOCKED": 1,
    }

    def run_case(self, signal):
        env = os.environ.copy()
        env["NABIL_FACTORY_TEST_RAISE"] = signal
        proc = subprocess.run(
            [sys.executable, "-m", "scripts.nabil_book_factory"],
            env=env,
            text=True,
            capture_output=True,
            timeout=30,
        )
        return proc

    def test_typed_boundary_exit_codes_have_no_traceback(self):
        for signal, expected in self.CASES.items():
            with self.subTest(signal=signal):
                proc = self.run_case(signal)
                self.assertEqual(proc.returncode, expected, proc.stdout + proc.stderr)
                self.assertNotIn("Traceback", proc.stderr)
                self.assertNotIn("Traceback", proc.stdout)
                self.assertIn('"stage": "FINAL_STATUS"', proc.stdout)


if __name__ == "__main__":
    unittest.main()
