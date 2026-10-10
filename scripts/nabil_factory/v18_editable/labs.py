"""V18 verified laboratory presentation contract.

Every lab must originate from the verified lesson activities.  Missing
laboratories stay explicitly unavailable; the renderer must never substitute
unverified fake simulations or external network calls.
"""
from __future__ import annotations
import html

CONFIG = {
    "exercise_inline": True, "auto_scroll": True,
    "audio_on_open": True, "offline_browser_fallback": True,
    "guided_reveal": True, "whole_lesson_lab": True,
}

def render_verified_labs(activities):
    """Return self-contained lesson lab cards backed by audited HTML."""
    sections = []
    for activity in activities or ():
        source = str(activity.get("lab_html") or "").strip()
        if not source:
            continue
        cid = html.escape(str(activity.get("concept_id") or ""), quote=True)
        title = html.escape(str(activity.get("title") or "Verified activity"))
        # Trusted HTML is produced by the existing scientific evidence gate.
        sections.append(
            '<section class="v18-lab" data-nabil-lab-concept="' + cid + '">'
            '<h3>' + title + '</h3>'
            '<div class="v18-lab-stage">' + source + '</div></section>'
        )
    return "\n".join(sections)

__all__ = ["CONFIG", "render_verified_labs"]
