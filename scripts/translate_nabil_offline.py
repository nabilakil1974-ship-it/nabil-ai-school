"""Translate a cached NABIL Golden lesson to French without AI API calls.

Usage:
 python -m scripts.translate_nabil_offline --input /data/nabil/output/lesson.html \
   --output /data/nabil/output/lesson--FR.html --backend opus
Requires preinstalled OPUS-MT weights and enough local CPU/RAM.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path

from scripts.nabil_factory.offline_translation import (
    get_free_translator, translate_html_offline,
    translate_v18_embedded_board_html, OfflineTranslationUnavailable
)

def translate_lesson(input_html: str, translator) -> tuple[str, dict]:
    """Translate HTML text and structured V18 board, both mandatory."""
    static_html, static_report = translate_html_offline(
        input_html, "en", "fr", translator)
    output, boards = translate_v18_embedded_board_html(static_html, translator)
    if "data-nabil-v18-board" in input_html and boards == 0:
        raise OfflineTranslationUnavailable("V18_BOARD_MISSING_FROM_FRENCH")
    if boards:
        # Every V18 board must be translated; a second unconverted board is
        # not acceptable. This does not validate other custom JS data.
        count = input_html.count('id="nabilV18Data"')
        if count != boards:
            raise OfflineTranslationUnavailable("V18_BOARDS_PARTIALLY_TRANSLATED")
    return output, {"source":"en","target":"fr","offline_only":True,
                    "static_nodes":static_report["translated_nodes"],
                    "translated_v18_boards":boards,
                    "scientific_review":"NOT_REVIEWED",
                    "publish_approved":False,
                    "requires_visual_and_scientific_acceptance":True}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--input",required=True)
    parser.add_argument("--output",required=True)
    parser.add_argument("--backend",choices=("opus","argos"),default="opus")
    args=parser.parse_args()
    inp=Path(args.input)
    out=Path(args.output)
    if inp.resolve() == out.resolve():
        raise SystemExit("CANNOT_OVERWRITE_SOURCE_LESSON")
    tr=get_free_translator("en","fr",args.backend)
    result, report=translate_lesson(inp.read_text(encoding="utf-8"),tr)
    # This is a DRAFT translation; never claim Golden publish acceptance.
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(result,encoding="utf-8")
    out.with_suffix(".translation-report.json").write_text(
        json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({"output":str(out),**report},ensure_ascii=False))

if __name__=="__main__":
    main()
