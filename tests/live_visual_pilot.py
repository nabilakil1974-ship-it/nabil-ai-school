"""Read-only, bounded live vision probe for the one G07 physics pilot.

Run only in a trusted worker with owner Drive read credentials and three
independent configured providers. This script never uploads or updates a ledger.
"""
import argparse
import json
import tempfile
from pathlib import Path

from scripts import nabil_lesson_factory as factory

BOOK_ID = "1LasqIgGUuck1l-2EZbj2kA0Dg9ygJ_AH"
PLUMB_CLAIM = ("The plumb line indicates the vertical direction; the set square "
               "shows the free liquid surface perpendicular to that vertical.")
FALSE_CLAIM = "The free surface in the illustrated vessel is a parabolic curve."


def run():
    from openai import OpenAI
    from pypdf import PdfReader

    with tempfile.TemporaryDirectory(prefix="nabil_g07_vision_") as tmp:
        pdf = Path(tmp) / "source.pdf"
        service = factory.owner_drive()
        factory.download_pdf_to_path(service, BOOK_ID, pdf)
        reader = PdfReader(str(pdf))
        if len(reader.pages) < 15:
            raise ValueError("SOURCE_PDF_TOO_SHORT")
        pages = [(page, "") for page in (14, 15)]
        images = factory.source_images(pdf, pages)
        _, visual_provider, visual_model = factory.visual_candidates(images)
        reserved_reviewer = factory.os.getenv("NABIL_REVIEWER_PROVIDER", "").strip().lower()
        generators = [p for p in factory.configured_providers()
                      if p[0] not in (visual_provider, reserved_reviewer)
                      and factory.os.getenv("NABIL_LESSON_MODEL", p[3]) != visual_model]
        if not generators:
            raise RuntimeError("INDEPENDENT_REVIEWER_UNAVAILABLE")
        generator_provider, _, _, generator_default_model = generators[0]
        generator_model = factory.os.getenv("NABIL_LESSON_MODEL", generator_default_model)
        reviewer, key, base, model = factory.independent_reviewer(
            generator_provider, generator_model, visual_provider, visual_model)
        client = OpenAI(api_key=key, base_url=base, timeout=90, max_retries=0)
        checks = []
        for page, claim in ((14, PLUMB_CLAIM), (15, PLUMB_CLAIM),
                            (15, FALSE_CLAIM)):
            verdict = factory.review_claim(client, reviewer, model,
                {"claim": claim, "figure_context": "G07 physics, source page " + str(page)},
                images[page], "", page)
            checks.append({"pdf_page": page, "claim": claim, "verdict": verdict})
        return {"status": "LIVE_PROBE_COMPLETE", "book_id": BOOK_ID,
                "visual_extractor_provider": visual_provider,
                "visual_extractor_model": visual_model,
                "generator_provider": generator_provider,
                "generator_model": generator_model,
                "reviewer_provider": reviewer, "reviewer_model": model,
                "checks": checks,
                "safe_to_dry_run": (checks[0]["verdict"]["approved"] is False
                                    and checks[1]["verdict"]["approved"] is True
                                    and checks[2]["verdict"]["approved"] is False)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    path = Path(args.report)
    try:
        result = run()
    except Exception as exc:
        result = {"status": "LIVE_PROBE_BLOCKED", "book_id": BOOK_ID,
                  "error_type": type(exc).__name__, "error": str(exc)[:180]}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("safe_to_dry_run") else 2


if __name__ == "__main__":
    raise SystemExit(main())
