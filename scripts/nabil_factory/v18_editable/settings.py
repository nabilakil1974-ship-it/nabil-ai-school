"""Stable registry for V18 presentation controls.

No scientific, source, or publication gates can be modified through this module.
"""
from __future__ import annotations
from types import MappingProxyType
from . import pacing, cards, labs, terminology, preparation

SETTINGS = MappingProxyType({
    "pacing": MappingProxyType(dict(pacing.CONFIG)),
    "cards": MappingProxyType(dict(cards.CONFIG)),
    "labs": MappingProxyType(dict(labs.CONFIG)),
    "terminology": MappingProxyType(dict(terminology.CONFIG)),
    "preparation": MappingProxyType(dict(preparation.CONFIG)),
})

def ui_settings(component: str) -> dict:
    """Return an isolated mutable copy of one component's presentation options."""
    if component not in SETTINGS:
        raise KeyError(f"UNKNOWN_V18_COMPONENT:{component}")
    return dict(SETTINGS[component])

def validate_settings() -> None:
    required = {"pacing", "cards", "labs", "terminology", "preparation"}
    if set(SETTINGS) != required:
        raise RuntimeError("V18_EDITABLE_INCOMPLETE")
    for name, values in SETTINGS.items():
        if not isinstance(values, MappingProxyType) or not values:
            raise RuntimeError(f"V18_INVALID_COMPONENT:{name}")
    pace = SETTINGS["pacing"]
    if not (0.1 <= pace["speech_rate"] <= 2.5):
        raise RuntimeError("V18_INVALID_SPEECH_RATE")
    if pace["minimum_speech_ms"] > pace["maximum_speech_ms"]:
        raise RuntimeError("V18_INVALID_SPEECH_TIMING")

validate_settings()
