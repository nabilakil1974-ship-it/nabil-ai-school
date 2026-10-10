"""V18 verified progressive results and final Golden Card presentation."""
from __future__ import annotations
import html

CONFIG = {"final_card_last": True, "card_theme": "nabil-v18",
          "interactive_zoom": True, "voice_button": True,
          "teacher_panel": True, "show_visual_evidence": True}

def result_slots(steps):
    """Seven or more concept-dependent slots; content is sourced from V18 steps."""
    out = []
    for i, step in enumerate(steps or ()):
        title = html.escape(str(step.get("title") or "Concept"))
        cid = html.escape(str(step.get("concept_id") or ""), quote=True)
        out.append(
            f'<div class="v18-result-slot" data-result-index="{i}" '
            f'data-concept-id="{cid}" aria-live="polite">'
            f'<b>{title}</b><div class="v18-result-value">—</div></div>'
        )
    return "".join(out)

def verified_final_card(theory):
    """Preserve EXACT audited scientific reference card, not an invented recap."""
    card = str((theory or {}).get("reference_card_html") or "").strip()
    if not card:
        raise RuntimeError("V18_VERIFIED_GOLDEN_CARD_MISSING")
    return card

__all__ = ["CONFIG", "result_slots", "verified_final_card"]
