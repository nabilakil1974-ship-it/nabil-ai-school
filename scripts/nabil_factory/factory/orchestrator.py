"""NABIL Golden factory modular loader.

This preserves one shared runtime namespace while the former monolith is
physically owned by P1, P2, cards, Drive delivery and factory modules.
"""
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_PARTS = [
    "scripts/nabil_factory/factory/shared.py",
    "scripts/nabil_factory/cards/core.py",
    "scripts/nabil_factory/drive_runtime/core.py",
    "scripts/nabil_factory/factory/guards.py",
    "scripts/nabil_factory/p2/core.py",
    "scripts/nabil_factory/factory/providers.py",
    "scripts/nabil_factory/p1/source_pipeline.py",
    "scripts/nabil_factory/factory/pipeline.py",
]

for _rel in _PARTS:
    _path = _ROOT / _rel
    _source = _path.read_text(encoding="utf-8")
    exec(compile(_source, str(_path), "exec"), globals(), globals())

def export_symbols():
    return {
        k: v for k, v in globals().items()
        if not k.startswith("__") and k not in {"Path", "_ROOT", "_PARTS", "_rel", "_path", "_source"}
    }
