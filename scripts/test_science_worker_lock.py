"""Prevent duplicate OCR workers and indexing script syntax regressions."""
import ast
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ScienceWorkerLockTests(unittest.TestCase):
    def test_indexing_entrypoints_compile(self):
        for name in ("index_science_textbooks.py", "science_worker.py", "index_books.py"):
            with self.subTest(name=name):
                source = (ROOT / "scripts" / name).read_text(encoding="utf-8")
                compile(source, name, "exec")

    def test_worker_shares_session_advisory_lock_with_manual_indexer(self):
        for name in ("index_science_textbooks.py", "science_worker.py"):
            with self.subTest(name=name):
                source = (ROOT / "scripts" / name).read_text(encoding="utf-8")
                tree = ast.parse(source)
                sql = [node.value for node in ast.walk(tree)
                       if isinstance(node, ast.Constant) and isinstance(node.value, str)]
                self.assertIn("SELECT pg_advisory_lock(728168120)", sql)
                self.assertIn("SELECT pg_advisory_unlock(728168120)", sql)
                self.assertTrue(any(isinstance(node, ast.Try) and any(
                    isinstance(child, ast.Call) and isinstance(child.func, ast.Attribute)
                    and child.func.attr == "execute" and any(
                        isinstance(arg, ast.Call) and isinstance(arg.func, ast.Name)
                        and arg.func.id == "text" and any(
                            isinstance(inner, ast.Constant)
                            and inner.value == "SELECT pg_advisory_unlock(728168120)"
                            for inner in arg.args)
                        for arg in child.args)
                    for statement in node.finalbody for child in ast.walk(statement))
                    for node in ast.walk(tree)), "Unlock must happen in finally")


if __name__ == "__main__":
    unittest.main()
