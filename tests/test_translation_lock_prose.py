import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.nabil_factory.factory import orchestrator as o  # noqa: E402


def _locked(text):
    out, locks = o._lock_scientific_translation_tokens(text, "t")
    return out, [orig for _k, orig in locks]


def test_english_prose_words_are_not_frozen():
    out, locked = _locked("Imagine a chessboard with 64 squares. We place 1 grain of wheat. If you add 2 more, the king's total grows.")
    for w in ("a", "We", "If", "s"):
        assert w not in locked, locked
    assert "64" in locked and "1" in locked and "2" in locked
    assert " a chessboard" in out and "We place" in out and "If you" in out and "king's total" in out


def test_math_symbols_are_still_frozen():
    out, locked = _locked("Compute a × b = 12 and 5 m + 3 cm for x² when A + B = 90")
    for t in ("a", "b", "12", "x", "A", "B", "90", "×", "="):
        assert t in locked, (t, locked)
