"""Canonical, display-ready math text for the V18 board and Golden cards.

The factory stores one canonical notation: powers are written ``base^{exp}``
(braces always present) and products use ``×``. The browser turns that into real
superscripts (see ``richMath`` in v18_board.py); raw ``^``/``*`` must never
reach a student. Pure functions, no AI.
"""
from __future__ import annotations

import re

_SUP_TO_ASCII = {"⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4", "⁵": "5",
                 "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9", "⁻": "-", "⁺": "+",
                 "ⁿ": "n", "ᵐ": "m", "ᵃ": "a", "ᵇ": "b", "ˣ": "x"}
_SUP_RUN = re.compile("[" + "".join(_SUP_TO_ASCII) + "]+")


def _balanced(text: str, start: int) -> int:
    """Index just after the parenthesis group opening at ``start`` (or -1)."""
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
            if depth == 0:
                return i + 1
    return -1


def canonical_math(text: str) -> str:
    s = str(text or "")
    s = re.sub(r"\\[\(\)\[\]]|\$\$?", "", s)
    s = (s.replace("\\times", "×").replace("\\cdot", "·").replace("\\div", "÷")
          .replace("\\left", "").replace("\\right", "").replace("\\,", " "))
    s = re.sub(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"(\1)/(\2)", s)
    s = re.sub(r"\\text\{([^{}]*)\}", r"\1", s)
    # unicode superscripts -> canonical ^{...}
    s = _SUP_RUN.sub(lambda m: "^{" + "".join(_SUP_TO_ASCII[c] for c in m.group(0)) + "}", s)
    # ^(...) with balanced parentheses -> ^{...}
    out, i = [], 0
    while i < len(s):
        if s[i] == "^" and i + 1 < len(s) and s[i + 1] == "(":
            end = _balanced(s, i + 1)
            if end != -1:
                out.append("^{" + s[i + 2:end - 1].strip() + "}")
                i = end
                continue
        out.append(s[i])
        i += 1
    s = "".join(out)
    # ^token -> ^{token}  (digits, signed digits, single letter)
    s = re.sub(r"\^(?!\{)(-?\d+|[A-Za-z])", r"^{\1}", s)
    # multiplication sign
    s = re.sub(r"(?<=[\w)}\]])\s*\*\s*(?=[\w({\[])", " × ", s)
    s = re.sub(r"\s*×\s*", " × ", s)
    s = re.sub(r"\s+", " ", s).strip()
    # adjacent exponent groups of a superscript run: x^{2}^{3} is never intended
    return s


_RAW_POWER = re.compile(r"\^|(?<![\w*])\*(?![\w*])|(?<=\w)\*(?=\w)")


def has_raw_math(visible_text: str) -> bool:
    """True when displayed text still contains ASCII ^ or * used as math."""
    return bool(_RAW_POWER.search(str(visible_text or "")))
