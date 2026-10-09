from __future__ import annotations

"""Offline smoke checks for NABIL self-healing core. No provider/Drive calls."""

import json
import py_compile

from scripts.nabil_factory.factory import orchestrator as factory


def main():
    # Compile the changed modules first.
    for path in (
        "scripts/nabil_factory/factory/supervisor.py",
        "scripts/nabil_factory/factory/title_verifier.py",
        "scripts/nabil_factory/factory/scientific_gate.py",
        "scripts/nabil_factory/cards/math_contract.py",
        "scripts/nabil_factory/p1/source_pipeline.py",
        "scripts/nabil_factory/p2/core.py",
        "scripts/nabil_factory/factory/pipeline.py",
        "scripts/nabil_factory/drive_runtime/core.py",
        "scripts/nabil_book_factory.py",
    ):
        py_compile.compile(path, doraise=True)

    # Title verifier: happy path, digit mismatch, Arabic marks/digits.
    assert factory.verify_title(
        "Parallelepiped / Cuboid",
        "PARALLELEPIPED - CUBOID",
        fallback_title="L2",
    ).status == "ACCEPTED"

    unit_mismatch = factory.verify_title(
        "Unit 2: Powers",
        "Unit 3: Powers",
        fallback_title="L",
    )
    assert unit_mismatch.status != "ACCEPTED"
    assert unit_mismatch.needs_review is True

    arabic = factory.verify_title(
        "الوِحدة ٢: القُوى",
        "الوحدة 2 - القوى",
        fallback_title="القوى",
    )
    assert arabic.status == "ACCEPTED", arabic

    # OCR/math normalization and deterministic Powers checks.
    assert factory.normalize_ocr("2² = 4") == "2^2 = 4"
    assert factory.check_power_claims(
        "(-2)^3 = -8; -2^2 = -4; 2^{-1} = 1/2"
    ) == []
    assert factory.check_power_claims("2^3 = 6") != []

    clean_report = factory.ReviewerReport()
    blocked = factory.scientific_gate("2^3 = 6", clean_report)
    assert blocked.verdict == "BLOCK"
    assert blocked.needs_review is True

    passed = factory.scientific_gate("2^3 = 8", clean_report)
    assert passed.verdict in {"PASS", "PASS_NORMALIZED"}

    # Reviewer outage/malformed JSON must NEVER fake an empty reviewed report.
    report, reviewed = factory.run_review(
        lambda _text: "{not valid json",
        "2^3 = 8",
        retries=0,
    )
    assert report is None
    assert reviewed is False

    report, reviewed = factory.run_review(
        lambda _text: json.dumps({"issues": []}),
        "2^3 = 8",
        retries=0,
    )
    assert reviewed is True
    assert report is not None
    assert report.issues == []

    # Legacy mixed prose/math normalization should preserve true powers while
    # demoting obvious prose accidentally wrapped in delimiters.
    fixed, count = factory.normalize_mixed_math_text(
        r"Keep \(2^3\) but demote \(This is plain prose\).",
        context="smoke",
    )
    assert r"\(2^3\)" in fixed
    assert "This is plain prose" in fixed
    assert count == 1

    print(json.dumps({
        "stage": "NABIL_SELF_HEAL_SMOKE_PASS",
        "tests": 12,
        "provider_calls": 0,
        "drive_calls": 0,
    }))


if __name__ == "__main__":
    main()
