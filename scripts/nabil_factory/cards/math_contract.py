from __future__ import annotations

"""Deterministic mixed text/math contract for legacy lesson HTML.

Legacy content may still contain prose accidentally wrapped in MathJax
 delimiters. This module separates that prose from true math without using AI.
It also normalizes the prebuilt translation bundle so language switching cannot
reintroduce the same defect.
"""

import json
import re

_MATH_RE = re.compile(
    r"\\\[(?P<display>.*?)\\\]"
    r"|\\\((?P<inline>.*?)\\\)"
    r"|\$\$(?P<dollar_display>.*?)\$\$"
    r"|(?<!\\)\$(?P<dollar_inline>[^$\n]+?)(?<!\\)\$",
    re.S,
)

_SKIP_BLOCK_RE = re.compile(
    r"(<(?:script|style|textarea|noscript)\b[^>]*>.*?</(?:script|style|textarea|noscript)>)",
    re.I | re.S,
)

_TAG_SPLIT_RE = re.compile(r"(<[^>]+>)", re.S)

_TRANSLATION_BUNDLE_RE = re.compile(
    r'(<script\s+id="nabilPageTranslationBundle"\s+type="application/json">)'
    r'(.*?)'
    r'(</script>)',
    re.I | re.S,
)


def _looks_like_prose_math(body: str) -> bool:
    text = str(body or "")
    text = re.sub(r"\\(?:text|mathrm|mbox|operatorname)\{[^}]*\}", " ", text)
    text = re.sub(r"\\[A-Za-z]+", " ", text)
    words = re.findall(r"(?<![A-Za-z])[A-Za-z]{3,}(?![A-Za-z])", text)
    return len(words) >= 2


def _demote_math_body(body: str) -> str:
    text = str(body or "")
    text = re.sub(
        r"\\(?:text|mathrm|mbox|operatorname)\{([^}]*)\}",
        r"\1",
        text,
    )
    text = re.sub(r"\\[A-Za-z]+", "", text)
    return re.sub(r"\s+", " ", text).strip()


def normalize_mixed_math_text(value: str, *, context: str = "") -> tuple[str, int]:
    """Demote prose inside legacy math delimiters while preserving real math."""
    text = str(value or "")
    demoted = 0

    def repl(match: re.Match) -> str:
        nonlocal demoted
        body = next(
            (g for g in (
                match.group("display"),
                match.group("inline"),
                match.group("dollar_display"),
                match.group("dollar_inline"),
            ) if g is not None),
            "",
        )
        if not _looks_like_prose_math(body):
            return match.group(0)
        demoted += 1
        cleaned = _demote_math_body(body)
        try:
            progress(
                "PROSE_IN_MATH_DEMOTED",
                context=context,
                source=cleaned[:160],
            )
        except Exception:
            pass
        return cleaned

    return _MATH_RE.sub(repl, text), demoted


def _normalize_visible_html_text(markup: str, *, context: str) -> tuple[str, int]:
    parts = _SKIP_BLOCK_RE.split(str(markup or ""))
    total = 0
    out = []
    for part in parts:
        if not part:
            continue
        if _SKIP_BLOCK_RE.fullmatch(part):
            out.append(part)
            continue
        chunks = _TAG_SPLIT_RE.split(part)
        healed = []
        for chunk in chunks:
            if not chunk or chunk.startswith("<"):
                healed.append(chunk)
                continue
            fixed, count = normalize_mixed_math_text(
                chunk, context=context)
            healed.append(fixed)
            total += count
        out.append("".join(healed))
    return "".join(out), total


def _normalize_translation_bundle(markup: str, *, context: str) -> tuple[str, int]:
    match = _TRANSLATION_BUNDLE_RE.search(str(markup or ""))
    if not match:
        return str(markup or ""), 0
    try:
        payload = json.loads(match.group(2))
    except Exception:
        return str(markup or ""), 0

    strings = payload.get("strings")
    if not isinstance(strings, dict):
        return str(markup or ""), 0

    total = 0
    for lang, mapping in list(strings.items()):
        if not isinstance(mapping, dict):
            continue
        healed = {}
        for key, value in mapping.items():
            new_key, c1 = normalize_mixed_math_text(
                str(key), context=f"{context}:bundle:{lang}:key")
            new_val, c2 = normalize_mixed_math_text(
                str(value), context=f"{context}:bundle:{lang}:value")
            healed[new_key] = new_val
            total += c1 + c2
        strings[lang] = healed
    payload["strings"] = strings

    encoded = json.dumps(
        payload, ensure_ascii=False, separators=(",", ":")
    ).replace("</", "<\\/")
    fixed = (
        str(markup or "")[:match.start(2)]
        + encoded
        + str(markup or "")[match.end(2):]
    )
    return fixed, total


def normalize_legacy_mixed_math_html(
        markup: str, *, context: str = "lesson") -> tuple[str, int]:
    """Normalize legacy mixed text/math in page DOM + language bundle.

    Safe for cached pages: no provider call, no scientific inference, and no
    change to genuine math delimiters.
    """
    fixed, bundle_count = _normalize_translation_bundle(
        markup, context=context)

    # The translation bundle script must stay opaque during visible DOM healing.
    bundle_match = _TRANSLATION_BUNDLE_RE.search(fixed)
    placeholder = None
    bundle_blob = None
    if bundle_match:
        placeholder = "__NABIL_TRANSLATION_BUNDLE_OPAQUE__"
        bundle_blob = bundle_match.group(0)
        fixed = fixed[:bundle_match.start()] + placeholder + fixed[bundle_match.end():]

    fixed, visible_count = _normalize_visible_html_text(
        fixed, context=context)

    if placeholder and bundle_blob is not None:
        fixed = fixed.replace(placeholder, bundle_blob, 1)

    total = bundle_count + visible_count
    if total:
        try:
            progress(
                "MIXED_MATH_LEGACY_NORMALIZED",
                context=context,
                demoted_segments=total,
            )
        except Exception:
            pass
    return fixed, total
