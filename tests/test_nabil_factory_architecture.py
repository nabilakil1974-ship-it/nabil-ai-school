from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "scripts" / "nabil_factory"


def test_modular_factory_boundaries_exist():
    required = [
        PKG / "p1" / "__init__.py",
        PKG / "p2" / "__init__.py",
        PKG / "cards" / "__init__.py",
        PKG / "drive_runtime" / "__init__.py",
        PKG / "factory" / "__init__.py",
        PKG / "ARCHITECTURE.md",
    ]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
    assert not missing, "missing modular factory boundaries: " + ", ".join(missing)


def test_entrypoint_must_not_grow_again():
    # During migration the old file is still large.  This test intentionally
    # becomes strict once the thin entrypoint marker is introduced.
    entry = ROOT / "scripts" / "nabil_lesson_factory.py"
    text = entry.read_text(encoding="utf-8")
    if "NABIL_THIN_FACTORY_ENTRYPOINT" in text:
        assert len(text.splitlines()) <= 250
        forbidden = (
            "extract_scanned_page_exercises",
            "attach_and_verify_source_completeness",
            "compile_twin_pages",
            "publish_to_drive",
        )
        for token in forbidden:
            assert token not in text
