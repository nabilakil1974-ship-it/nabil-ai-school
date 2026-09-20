"""Resolve UI curriculum labels to the exact official textbook index namespace.

The lesson picker uses the user-friendly Lebanese curriculum name, whereas
CRDP English/French book manifests are indexed under CRDP-EN / CRDP-FR.
Never substitute another language for an explicitly requested one.
"""

OFFICIAL_LABELS = frozenset({
    "", "المنهج اللبناني الرسمي", "المنهج اللبناني", "Lebanese official curriculum",
    "Lebanese curriculum", "CRDP", "official",
})


def resolve_textbook_curriculum(curriculum: str | None, language: str | None) -> str:
    requested = str(curriculum or "").strip()
    if requested.upper() in {"CRDP-EN", "CRDP-FR"}:
        return requested.upper()
    if requested not in OFFICIAL_LABELS:
        return requested
    if language == "English":
        return "CRDP-EN"
    if language == "Français":
        return "CRDP-FR"
    # No indexed Arabic equivalent is established by the manifest.
    return requested
