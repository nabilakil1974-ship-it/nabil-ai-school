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


# ============================================================================
# V18 deterministic mathematical solution contract
# ----------------------------------------------------------------------------
# The LLM may propose steps, but the FINAL ANSWER shown to the student must be
# consistent with arithmetic that Python itself verified (Fractions, exact).
#   VERIFIED     every numeric equality in the steps holds and the final answer
#                only states values the steps computed (or the prompt gave)
#   CONTRADICTED an equality is false, or the final answer states a value the
#                steps did not compute / omits a computed result
#   UNPROVEN     numeric final answer but no verifiable equality in the steps
# CONTRADICTED-by-final-only is repaired by DERIVING the final answer from the
# verified steps (never from the LLM). Anything else leaves the exercise
# unapproved. General engine: no per-exercise special cases.
# ============================================================================
from fractions import Fraction as _Fr

MATH_CONTRACT_VERSION = "NABIL_V18_MATH_CONTRACT_V1"

_AR_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")
_SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺", "0123456789-+")
_SUP_CHARS = "⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺"
_NUM_RUN_RE = re.compile(
    r"[\-−–]?[0-9٠-٩۰-۹(][0-9٠-٩۰-۹.,٫\s()+\-−–×xX*·÷/^" + _SUP_CHARS + r"=]*"
    r"[0-9٠-٩۰-۹)" + _SUP_CHARS + r"]")
_NUMBER_TOKEN_RE = re.compile(r"-?\d+(?:\.\d+)?")
_LABEL_RE = re.compile(r"^\s*[\(\[]?\s*([A-Za-z؀-ۿ]|\d{1,2})\s*[\)\]\.:\-–]\s+")


class _NotNumeric(Exception):
    pass


def _prep(expr: str) -> str:
    s = str(expr or "").translate(_AR_DIGITS)
    s = re.sub("([" + _SUP_CHARS + "]+)", lambda m: "^(" + m.group(1).translate(_SUP) + ")", s)
    s = s.replace("−", "-").replace("–", "-").replace("٫", ".").replace(",", ".")
    s = s.replace("×", "*").replace("·", "*").replace("÷", "/")
    s = re.sub(r"(?<=[\d)])\s*[xX]\s*(?=[\d(])", "*", s)
    return re.sub(r"\s+", "", s)


def _parse_numeric(expr: str) -> _Fr:
    s = _prep(expr)
    if not s or re.search(r"[^0-9.+\-*/^()]", s):
        raise _NotNumeric(expr)
    pos = 0

    def peek():
        return s[pos] if pos < len(s) else ""

    def number():
        nonlocal pos
        m = re.match(r"\d+(?:\.\d+)?|\.\d+", s[pos:])
        if not m:
            raise _NotNumeric(expr)
        pos += m.end()
        return _Fr(m.group(0))

    def atom():
        nonlocal pos
        c = peek()
        if c == "(":
            pos += 1
            v = add()
            if peek() != ")":
                raise _NotNumeric(expr)
            pos += 1
            return v
        if c == "-":
            pos += 1
            return -power()
        if c == "+":
            pos += 1
            return power()
        return number()

    def power():
        nonlocal pos
        base = atom()
        if peek() == "^":
            pos += 1
            exp = atom()
            if exp.denominator != 1 or abs(exp.numerator) > 64:
                raise _NotNumeric(expr)
            if base == 0 and exp < 0:
                raise _NotNumeric(expr)
            return base ** int(exp)
        return base

    def mul():
        nonlocal pos
        v = power()
        while peek() in ("*", "/"):
            op = peek()
            pos += 1
            r = power()
            if op == "/":
                if r == 0:
                    raise _NotNumeric(expr)
                v = v / r
            else:
                v = v * r
        return v

    def add():
        nonlocal pos
        v = mul()
        while peek() in ("+", "-"):
            op = peek()
            pos += 1
            r = mul()
            v = v + r if op == "+" else v - r
        return v

    v = add()
    if pos != len(s):
        raise _NotNumeric(expr)
    return v


def format_exact_number(v: _Fr) -> str:
    """Terminating decimals as decimals, everything else as p/q."""
    if v.denominator == 1:
        return str(v.numerator)
    d = v.denominator
    for p in (2, 5):
        while d % p == 0:
            d //= p
    if d != 1:
        return f"{v.numerator}/{v.denominator}"
    n, den = abs(v.numerator), v.denominator
    whole, rem = divmod(n, den)
    digits = ""
    while rem:
        rem *= 10
        q, rem = divmod(rem, den)
        digits += str(q)
    return ("-" if v < 0 else "") + str(whole) + "." + digits


def _chains_in_step(step: str) -> list[dict]:
    out = []
    text = str(step or "")
    label_m = _LABEL_RE.match(text)
    label = label_m.group(1) if label_m else ""
    segments = re.split(r"[;؛،\n]|,\s", text)
    runs = []
    for seg in segments:
        for m in _NUM_RUN_RE.finditer(seg):
            before = seg[:m.start()].rstrip()
            after = seg[m.end():]
            after_s = after.lstrip()
            # never evaluate a fragment glued to context the parser cannot see
            if before and ((m.start() == len(before) and before[-1].isalpha())
                           or before[-1] in "+-−–×*·÷/^=√%.,xX("):
                continue
            if after_s and (after_s[0] in "+-−–×*·÷/^=√%" + _SUP_CHARS
                            or (after and after[0].isalpha())):
                continue
            runs.append(m.group(0))
    for run in runs:
        if "=" not in run:
            continue
        sides = [x.strip() for x in run.split("=")]
        parsed = []
        for side in sides:
            try:
                parsed.append((side, _parse_numeric(side)))
            except _NotNumeric:
                parsed.append((side, None))
        # adjacent verifiable pairs only
        verified, contradictions = [], []
        for (a, va), (b, vb) in zip(parsed, parsed[1:]):
            if va is not None and vb is not None:
                (verified if va == vb else contradictions).append((a, b, va, vb))
        if not verified and not contradictions:
            continue
        values = [v for _, v in parsed if v is not None]
        out.append({
            "label": label, "text": run.strip(), "values": values,
            "end": values[-1],
            "contradictions": [f"{a} = {b} (but {format_exact_number(va)} != {format_exact_number(vb)}) in step: {str(step)[:120]}"
                               for a, b, va, vb in contradictions],
        })
    return out


def verify_math_solution(prompt: str, steps: list, final_answer: str) -> dict:
    """Deterministic verdict on a math solution. Pure; no AI."""
    chains = [c for s in (steps or []) for c in _chains_in_step(str(s))]
    bad = [x for c in chains for x in c["contradictions"]]
    if bad:
        return {"status": "CONTRADICTED", "kind": "ARITHMETIC_FALSE",
                "reason": "STEP_ARITHMETIC_FALSE: " + "; ".join(bad[:4]),
                "chains": len(chains), "derived_final": None, "repairable": False}
    final_text = str(final_answer or "").translate(_AR_DIGITS).replace(",", ".").replace("٫", ".")
    final_text = final_text.replace("−", "-")
    final_text = re.sub(r"(?<=\d)[ \u00a0\u202f](?=\d{3}(?!\d))", "", final_text)
    final_nums = []
    for tok in _NUMBER_TOKEN_RE.findall(re.sub(r"[" + _SUP_CHARS + "]+", " ", final_text)):
        try:
            final_nums.append(_Fr(tok))
        except (ValueError, ZeroDivisionError):
            pass
    if not chains:
        if final_nums:
            return {"status": "UNPROVEN", "kind": "VERIFIER_COULD_NOT_PARSE",
                    "reason": "NUMERIC_FINAL_WITHOUT_VERIFIABLE_STEP_EQUALITY",
                    "chains": 0, "derived_final": None, "repairable": False}
        return {"status": "VERIFIED", "reason": "NO_NUMERIC_CLAIMS", "chains": 0,
                "derived_final": None, "repairable": False}
    allowed = set()
    for c in chains:
        allowed.update(c["values"])
    prompt_text = str(prompt or "").translate(_AR_DIGITS).replace(",", ".")
    prompt_text = re.sub(r"(?<=\d)[ \u00a0\u202f](?=\d{3}(?!\d))", "", prompt_text)
    for tok in _NUMBER_TOKEN_RE.findall(prompt_text):
        allowed.add(_Fr(tok))
    # last chain per label (or last overall) = the stated result of that part
    last_by_label: dict[str, dict] = {}
    for c in chains:
        last_by_label[c["label"]] = c
    required = [c["end"] for c in last_by_label.values()]
    problems = []
    for n in final_nums:
        if n not in allowed:
            problems.append("FINAL_STATES_UNCOMPUTED_VALUE:" + format_exact_number(n))
    have = set(final_nums)
    for r in required:
        if r not in have:
            problems.append("FINAL_OMITS_COMPUTED_RESULT:" + format_exact_number(r))
    if not problems:
        return {"status": "VERIFIED", "reason": "STEPS_AND_FINAL_CONSISTENT",
                "chains": len(chains), "derived_final": None, "repairable": False}
    parts = []
    for label, c in last_by_label.items():
        val = format_exact_number(c["end"])
        parts.append(f"{label}) {val}" if label else val)
    return {"status": "CONTRADICTED", "kind": "FINAL_MISMATCH", "reason": "; ".join(problems[:4]),
            "chains": len(chains), "derived_final": "; ".join(parts), "repairable": True}


def enforce_math_solution_contract(exercise: dict, solution: dict, subject: str) -> dict:
    """Return a solution whose Final Answer is guaranteed consistent with its
    verified steps, or raise RuntimeError('MATH_SOLUTION_CONTRADICTION:...' /
    'MATH_EXPRESSION_UNVERIFIED:...') so the exercise stays unapproved."""
    if str(subject or "").strip().lower() not in {"math", "mathematics", "رياضيات", "mathématiques"}:
        return solution
    if not isinstance(solution, dict):
        raise RuntimeError("MATH_EXPRESSION_UNVERIFIED:NO_SOLUTION_OBJECT")
    prompt = str(exercise.get("exact_source_prompt") or exercise.get("prompt") or "")
    verdict = verify_math_solution(prompt, solution.get("steps") or [],
                                   str(solution.get("final_answer") or ""))
    if verdict["status"] == "CONTRADICTED" and verdict["repairable"] and verdict["derived_final"]:
        repaired = dict(solution)
        repaired["final_answer_original_rejected"] = str(solution.get("final_answer") or "")
        repaired["final_answer"] = verdict["derived_final"]
        again = verify_math_solution(prompt, repaired["steps"], repaired["final_answer"])
        if again["status"] != "VERIFIED":
            raise RuntimeError("MATH_SOLUTION_CONTRADICTION:" + again["reason"])
        repaired["math_contract"] = {"version": MATH_CONTRACT_VERSION, "status": "VERIFIED",
                                     "final_answer_derived_from_steps": True,
                                     "rejected_reason": verdict["reason"]}
        return repaired
    if verdict["status"] == "CONTRADICTED":
        raise RuntimeError("MATH_SOLUTION_CONTRADICTION:" + verdict["reason"])
    if verdict["status"] == "UNPROVEN":
        raise RuntimeError("MATH_EXPRESSION_UNVERIFIED:" + verdict["reason"])
    out = dict(solution)
    out["math_contract"] = {"version": MATH_CONTRACT_VERSION, "status": "VERIFIED",
                            "final_answer_derived_from_steps": False,
                            "chains_verified": verdict["chains"]}
    return out
