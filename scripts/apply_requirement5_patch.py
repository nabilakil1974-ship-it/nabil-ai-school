#!/usr/bin/env python3
"""One-shot deterministic source patch for Requirement 5.

This script edits nabil_lesson_factory.py by function boundaries instead of line
numbers, so it survives unrelated line movement. It is idempotent and fails
closed if the expected factory function cannot be located.
"""
from pathlib import Path
import re

PATH = Path("scripts/nabil_lesson_factory.py")
s = PATH.read_text(encoding="utf-8")

IMPORT = "from scripts.nabil_requirement5_gate import validate_requirement5_lab, assert_requirement5_publishable\n"
if IMPORT not in s:
    # Insert after the last top-level import/from statement before executable code.
    lines = s.splitlines(True)
    pos = 0
    for i, line in enumerate(lines[:250]):
        if line.startswith("import ") or line.startswith("from "):
            pos = i + 1
    lines.insert(pos, IMPORT)
    s = "".join(lines)

start = s.find("def build_verified_lab_spec(")
if start < 0:
    raise SystemExit("R5_PATCH_FAILED: build_verified_lab_spec not found")
next_def = re.search(r"\n(?:async\s+)?def\s+[A-Za-z_]\w*\s*\(", s[start + 1:])
end = start + 1 + next_def.start() if next_def else len(s)
block = s[start:end]

MARKER = "# REQUIREMENT_5_FINAL_GATE"
if MARKER not in block:
    # Use the final top-level-indented return spec in this function.
    returns = list(re.finditer(r"(?m)^    return spec\s*$", block))
    if not returns:
        raise SystemExit("R5_PATCH_FAILED: final return spec not found")
    r = returns[-1]
    injection = '''    # REQUIREMENT_5_FINAL_GATE\n    # Final fail-closed source/science/visual acceptance. This runs AFTER the\n    # existing domain validators and BEFORE the spec can leave the factory.\n    spec = validate_requirement5_lab(\n        spec,\n        source_text=str(concept.get("raw_text") or ""),\n        source_figure_verified=bool(\n            figure_image_base64 and (concept.get("figure_refs") or vision_context)\n        ),\n    )\n    assert_requirement5_publishable(\n        spec,\n        lesson_id=str(entry.get("lesson_id") or ""),\n        lab_id=str(concept.get("concept_id") or ""),\n    )\n'''
    block = block[:r.start()] + injection + block[r.start():]
    s = s[:start] + block + s[end:]

PATH.write_text(s, encoding="utf-8")
print("R5_PATCH_OK", PATH)
