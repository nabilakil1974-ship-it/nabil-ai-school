"""V18 textbook-grounded terminology and mathematical notation.

Only display source-backed terminology; this module never fabricates a
translation or scientific definition.
"""
from __future__ import annotations
import html
import re

CONFIG = {"show_original_term": True, "show_verified_translation": True,
          "show_definition": True, "show_example": True,
          "first_use_emphasis": True, "bilingual_layout": True}

POWER_TERMS = {
    "power": {"en": "Power", "ar": "قوة", "fr": "Puissance"},
    "base": {"en": "Base", "ar": "الأساس", "fr": "Base"},
    "exponent": {"en": "Exponent", "ar": "الأسّ", "fr": "Exposant"},
    "product": {"en": "Product", "ar": "حاصل الضرب", "fr": "Produit"},
}

def terminology_cards(terms, language="en"):
    """Present explicitly verified source entries; no inferred definitions."""
    out = []
    for term in terms or ():
        if not isinstance(term, dict) or not term.get("verified_against_source"):
            continue
        original = html.escape(str(term.get("original") or term.get("term") or ""))
        translated = html.escape(str((term.get("translations") or {}).get(language) or original))
        definition = html.escape(str(term.get("definition") or ""))
        example = html.escape(str(term.get("example") or ""))
        if not original:
            continue
        out.append('<article class="v18-term"><b>' + original + '</b> · <strong>'
                   + translated + '</strong><p>' + definition + '</p><code>'
                   + example + '</code></article>')
    return "\n".join(out)

def readable_powers(text):
    """Render simple power notation as actual exponents in DOM-safe HTML."""
    escaped = html.escape(str(text or ""))
    return re.sub(r'(?<![\\w])([a-zA-Z0-9]+)\\^([a-zA-Z0-9]+)',
                  lambda m: m.group(1) + '<sup>' + m.group(2) + '</sup>', escaped)

__all__ = ["CONFIG", "POWER_TERMS", "terminology_cards", "readable_powers"]
