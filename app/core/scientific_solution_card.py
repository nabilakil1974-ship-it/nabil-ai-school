# -*- coding: utf-8 -*-
"""
NABIL AI — Scientific Solution Card Engine

Backend contract shared by:
1) Root / Root Chat
2) generated lesson exercise pages

Rules:
- Function studies are computed deterministically with SymPy.
- Physics/Chemistry/Biology/Science cards restructure only verified backend output.
- No scientific value is invented by the card layer.
"""

from __future__ import annotations

import math
import re
from typing import Any, Optional

from sympy import (
    Abs,
    E,
    Poly,
    S,
    Symbol,
    cos,
    diff,
    div,
    exp,
    fraction,
    limit,
    log,
    oo,
    pi,
    simplify,
    sin,
    solveset,
    sqrt,
    tan,
    together,
)

from sympy.calculus.util import continuous_domain

from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)


# =============================================================================
# CORE SYMBOLIC CONFIGURATION
# =============================================================================

_X = Symbol("x", real=True)

_TRANSFORMS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)

_ALLOWED_NAMES = {
    "x": _X,
    "ln": log,
    "log": log,
    "exp": exp,
    "sqrt": sqrt,
    "sin": sin,
    "cos": cos,
    "tan": tan,
    "abs": Abs,
    "Abs": Abs,
    "pi": pi,
    "E": E,
}


_FUNCTION_REQUEST = re.compile(
    r"\b(?:study|analyse|analyze|graph|plot|sketch|draw)"
    r"\s+(?:and\s+draw\s+)?(?:the\s+)?function\b|"
    r"\bfunction\s+study\b|"
    r"\b(?:étude|etud\w*)\s+(?:de\s+la\s+)?fonction\b|"
    r"\b(?:tracer|dessiner|analyser)\b[^\n]{0,80}"
    r"(?:fonction|f\s*\(\s*x\s*\))|"
    r"دراسة\s+الدال|"
    r"ادرس\s+الدال|"
    r"حل[ّ ]?ل\s+الدال|"
    r"ارسم\s+الدال|"
    r"جدول\s+التغي|"
    r"tableau\s+de\s+variations",
    re.I,
)


# =============================================================================
# BASIC HELPERS
# =============================================================================

def _txt(value: Any) -> str:
    return str(value or "").strip()


def _language(text: str) -> str:
    raw = _txt(text)

    if re.search(
        r"\b(?:fonction|domaine|limite|dérivée|derivee|"
        r"asymptote|croissante|décroissante|decroissante|"
        r"physique|chimie|biologie)\b",
        raw,
        re.I,
    ):
        return "fr"

    if re.search(
        r"\b(?:function|domain|limit|derivative|asymptote|"
        r"increasing|decreasing|physics|chemistry|biology|"
        r"science|solve|study)\b",
        raw,
        re.I,
    ):
        return "en"

    if re.search(r"[\u0600-\u06ff]", raw):
        return "ar"

    return "en"


def _labels(lang: str) -> dict[str, str]:

    if lang == "fr":
        return {
            "given": "Données",
            "required": "Demandé",
            "method": "Loi / Méthode",
            "steps": "Solution étape par étape",
            "verify": "Vérification",

            "domain": "Domaine",
            "limits": "Limites",
            "asymptotes": "Asymptotes",
            "intercepts": "Intersections avec les axes",
            "derivative": "Dérivée",
            "critical": "Points critiques",
            "variation": "Variations / Extrema",

            "observation": "Observation",
            "interpretation": "Interprétation",
            "conclusion": "Conclusion",

            "chemical_model": "Modèle chimique",

            "structure": "Structure",
            "function": "Fonction",
            "relation": "Relation structure–fonction",

            "evidence": "Preuves / Données",
        }

    if lang == "ar":
        return {
            "given": "المعطيات",
            "required": "المطلوب",
            "method": "القانون / الطريقة",
            "steps": "الحل خطوة بخطوة",
            "verify": "التحقق",

            "domain": "مجال التعريف",
            "limits": "النهايات",
            "asymptotes": "المقاربات",
            "intercepts": "التقاطعات مع المحاور",
            "derivative": "المشتقة",
            "critical": "النقاط الحرجة",
            "variation": "التزايد والتناقص / القيم القصوى",

            "observation": "الملاحظة",
            "interpretation": "التفسير",
            "conclusion": "الاستنتاج",

            "chemical_model": "النموذج الكيميائي",

            "structure": "البنية",
            "function": "الوظيفة",
            "relation": "العلاقة بين البنية والوظيفة",

            "evidence": "الأدلة / المعطيات",
        }

    return {
        "given": "Given",
        "required": "Required",
        "method": "Law / Method",
        "steps": "Step-by-Step Solution",
        "verify": "Verification",

        "domain": "Domain",
        "limits": "Limits",
        "asymptotes": "Asymptotes",
        "intercepts": "Axis Intercepts",
        "derivative": "Derivative",
        "critical": "Critical Points",
        "variation": "Variation / Extrema",

        "observation": "Observation",
        "interpretation": "Interpretation",
        "conclusion": "Conclusion",

        "chemical_model": "Chemical Model",

        "structure": "Structure",
        "function": "Function",
        "relation": "Structure–Function Relation",

        "evidence": "Evidence / Data",
    }


# =============================================================================
# SUBJECT / CARD TYPE DETECTION
# =============================================================================

def _detect_kind(
    message: str,
    subject: str = "",
) -> Optional[str]:

    combined = (
        f"{message or ''}\n"
        f"{subject or ''}"
    )

    if _FUNCTION_REQUEST.search(combined):
        return "function_study"

    if re.search(
        r"\b(?:physics|physique)\b|فيز",
        combined,
        re.I,
    ):
        return "physics"

    if re.search(
        r"\b(?:chemistry|chimie)\b|كيمي",
        combined,
        re.I,
    ):
        return "chemistry"

    if re.search(
        r"\b(?:biology|biologie)\b|أحياء|احياء",
        combined,
        re.I,
    ):
        return "biology"

    if re.search(
        r"\bscience\b|\bsciences\b|علوم",
        combined,
        re.I,
    ):
        return "general_science"

    if re.search(
        r"\b(?:equation|geometry|triangle|circle|"
        r"derivative|integral|function)\b|"
        r"معادلة|هندس|مثلث|دائرة|مشتق|تكامل|دال",
        combined,
        re.I,
    ):
        return "mathematics"

    return None


# =============================================================================
# FUNCTION EXPRESSION EXTRACTION
# =============================================================================

def _extract_function_expression(
    message: str,
) -> Optional[str]:

    text = _txt(message)

    candidates = []

    patterns = (
        r"f\s*\(\s*x\s*\)\s*=\s*([^\n;]+)",
        r"\by\s*=\s*([^\n;]+)",
        r"(?:function|fonction|الدالة)\s*[:=]?\s*([^\n;]+)",
    )

    for pattern in patterns:

        for match in re.finditer(
            pattern,
            text,
            re.I,
        ):
            candidates.append(
                match.group(1).strip()
            )

    if not candidates:

        match = re.search(
            r"(?:study|analyse|analyze|étudier|etudier|"
            r"ادرس|دراسة)[^\n]{0,40}?"
            r"((?:ln|log|exp|sqrt|sin|cos|tan)?"
            r"\s*\(?[x0-9][^\n,;?]*)",
            text,
            re.I,
        )

        if match:
            candidates.append(
                match.group(1).strip()
            )

    if not candidates:
        return None

    expr = candidates[0]

    expr = re.sub(
        r"\bwhere\b.*$",
        "",
        expr,
        flags=re.I,
    ).strip()

    expr = (
        expr
        .replace("÷", "/")
        .replace("×", "*")
        .replace("−", "-")
    )

    expr = re.sub(
        r"(?i)\bln\s*\(",
        "log(",
        expr,
    )

    expr = expr.strip(
        " .,:;"
    )

    return expr or None


# =============================================================================
# SAFE SYMBOLIC PARSING
# =============================================================================

def _safe_parse_expression(
    expr_text: str,
):

    raw = _txt(expr_text)

    if not raw:
        return None

    if len(raw) > 240:
        return None

    cleaned = raw.replace(
        "π",
        "pi",
    )

    # Reject characters that do not belong in a school function expression.
    if re.search(
        r"[^0-9A-Za-z_+\-*/^().,\s]",
        cleaned,
    ):
        return None

    names = re.findall(
        r"[A-Za-z_]+",
        cleaned,
    )

    if any(
        name not in _ALLOWED_NAMES
        and name != "x"
        for name in names
    ):
        return None

    try:

        expr = parse_expr(
            cleaned,
            local_dict=dict(_ALLOWED_NAMES),
            transformations=_TRANSFORMS,
            evaluate=True,
        )

    except Exception:
        return None

    if (
        getattr(
            expr,
            "free_symbols",
            set(),
        )
        -
        {_X}
    ):
        return None

    return simplify(expr)


# =============================================================================
# SYMBOLIC RESULT HELPERS
# =============================================================================

def _finite_real_values(
    solution,
) -> list:

    if solution is S.EmptySet:
        return []

    if getattr(
        solution,
        "is_FiniteSet",
        False,
    ):

        output = []

        for value in solution:

            if value.is_real is False:
                continue

            if value.is_finite is False:
                continue

            output.append(
                simplify(value)
            )

        return output

    return []


def _sort_numeric(
    values: list,
) -> list:

    def key(value):

        try:
            return float(
                value.evalf()
            )

        except Exception:
            return math.inf

    dedup = []
    seen = set()

    for value in values:

        token = str(
            simplify(value)
        )

        if token in seen:
            continue

        seen.add(token)

        dedup.append(
            simplify(value)
        )

    return sorted(
        dedup,
        key=key,
    )


def _plain(
    value: Any,
    digits: int = 6,
) -> str:

    if value in (
        oo,
        S.Infinity,
    ):
        return "+∞"

    if value in (
        -oo,
        S.NegativeInfinity,
    ):
        return "-∞"

    try:

        if getattr(
            value,
            "is_Integer",
            False,
        ):
            return str(value)

        numeric = float(
            value.evalf()
        )

        if math.isfinite(numeric):

            rounded = round(
                numeric,
                digits,
            )

            if abs(
                rounded
                -
                round(rounded)
            ) < 10 ** (-digits):

                return str(
                    int(round(rounded))
                )

            return str(rounded)

    except Exception:
        pass

    return str(value)


# =============================================================================
# LIMITS
# =============================================================================

def _limit_text(
    expr,
    point,
    direction: Optional[str] = None,
) -> Optional[str]:

    try:

        if point == -oo:

            value = limit(
                expr,
                _X,
                -oo,
            )

            return (
                "lim x→-∞ f(x) = "
                +
                _plain(value)
            )

        if point == oo:

            value = limit(
                expr,
                _X,
                oo,
            )

            return (
                "lim x→+∞ f(x) = "
                +
                _plain(value)
            )

        if direction:

            value = limit(
                expr,
                _X,
                point,
                dir=direction,
            )

            side = (
                "⁺"
                if direction == "+"
                else "⁻"
            )

            return (
                "lim x→"
                +
                _plain(point)
                +
                side
                +
                " f(x) = "
                +
                _plain(value)
            )

    except Exception:
        return None

    return None


# =============================================================================
# ASYMPTOTES
# =============================================================================

def _rational_asymptotes(
    expr,
) -> tuple[list[str], list[str]]:

    vertical: list[str] = []
    other: list[str] = []

    try:

        numerator, denominator = fraction(
            together(expr)
        )

        denominator_roots = _finite_real_values(
            solveset(
                denominator,
                _X,
                domain=S.Reals,
            )
        )

        for root in _sort_numeric(
            denominator_roots
        ):

            try:

                if simplify(
                    numerator.subs(
                        _X,
                        root,
                    )
                ) != 0:

                    vertical.append(
                        f"x = {_plain(root)}"
                    )

            except Exception:

                vertical.append(
                    f"x = {_plain(root)}"
                )

        numerator_poly = Poly(
            numerator,
            _X,
        )

        denominator_poly = Poly(
            denominator,
            _X,
        )

        if denominator_poly.degree() >= 0:

            if (
                numerator_poly.degree()
                <
                denominator_poly.degree()
            ):

                other.append(
                    "y = 0"
                )

            elif (
                numerator_poly.degree()
                ==
                denominator_poly.degree()
            ):

                ratio = simplify(
                    numerator_poly.LC()
                    /
                    denominator_poly.LC()
                )

                other.append(
                    f"y = {_plain(ratio)}"
                )

            elif (
                numerator_poly.degree()
                ==
                denominator_poly.degree() + 1
            ):

                quotient, _ = div(
                    numerator_poly,
                    denominator_poly,
                )

                other.append(
                    "y = "
                    +
                    str(
                        quotient.as_expr()
                    )
                )

    except Exception:
        pass

    return vertical, other


# =============================================================================
# VARIATION HELPERS
# =============================================================================

def _interval_test(
    left,
    right,
) -> float:

    if left is None:

        return (
            float(right)
            -
            max(
                1.0,
                abs(float(right)) * 0.25,
            )
        )

    if right is None:

        return (
            float(left)
            +
            max(
                1.0,
                abs(float(left)) * 0.25,
            )
        )

    return (
        float(left)
        +
        float(right)
    ) / 2.0


# =============================================================================
# COMPLETE FUNCTION STUDY
# =============================================================================

def _function_card(
    message: str,
    reply: str,
    drawings: list[dict],
    lang: str,
) -> Optional[dict]:

    expr_text = _extract_function_expression(
        message
    )

    if not expr_text:
        return None

    expr = _safe_parse_expression(
        expr_text
    )

    if expr is None:
        return None

    labels = _labels(lang)

    # -------------------------------------------------------------------------
    # Domain
    # -------------------------------------------------------------------------

    try:

        domain = continuous_domain(
            expr,
            _X,
            S.Reals,
        )

    except Exception:

        domain = S.Reals

    # -------------------------------------------------------------------------
    # Derivative
    # -------------------------------------------------------------------------

    derivative = simplify(
        diff(
            expr,
            _X,
        )
    )

    # -------------------------------------------------------------------------
    # Critical points
    # -------------------------------------------------------------------------

    critical = _finite_real_values(
        solveset(
            derivative,
            _X,
            domain=domain,
        )
    )

    critical = _sort_numeric(
        critical
    )

    # -------------------------------------------------------------------------
    # Asymptotes
    # -------------------------------------------------------------------------

    vertical, other_asymptotes = (
        _rational_asymptotes(
            expr
        )
    )

    vertical_values = []

    for item in vertical:

        raw = (
            item
            .split(
                "=",
                1,
            )[-1]
            .strip()
        )

        parsed = _safe_parse_expression(
            raw
        )

        if parsed is not None:
            vertical_values.append(
                parsed
            )

    # -------------------------------------------------------------------------
    # Limits
    # -------------------------------------------------------------------------

    limits = []

    for point in (
        -oo,
        oo,
    ):

        line = _limit_text(
            expr,
            point,
        )

        if line:
            limits.append(line)

    for value in vertical_values:

        for direction in (
            "-",
            "+",
        ):

            line = _limit_text(
                expr,
                value,
                direction,
            )

            if line:
                limits.append(line)

    # -------------------------------------------------------------------------
    # Intercepts
    # -------------------------------------------------------------------------

    intercepts = []

    try:

        if 0 in domain:

            intercepts.append(
                "y-intercept: "
                +
                "(0, "
                +
                _plain(
                    simplify(
                        expr.subs(
                            _X,
                            0,
                        )
                    )
                )
                +
                ")"
            )

    except Exception:
        pass

    try:

        roots = _finite_real_values(
            solveset(
                expr,
                _X,
                domain=domain,
            )
        )

        for root in _sort_numeric(
            roots
        ):

            intercepts.append(
                "x-intercept: "
                +
                "("
                +
                _plain(root)
                +
                ", 0)"
            )

    except Exception:
        pass

    # -------------------------------------------------------------------------
    # Variation table
    # -------------------------------------------------------------------------

    special = _sort_numeric(
        critical
        +
        vertical_values
    )

    boundaries = (
        [None]
        +
        [
            float(
                value.evalf()
            )
            for value in special
        ]
        +
        [None]
    )

    interval_rows = []

    columns = []
    derivative_cells = []
    function_cells = []

    critical_tokens = {
        str(value): value
        for value in critical
    }

    vertical_tokens = {
        str(value): value
        for value in vertical_values
    }

    for index in range(
        len(boundaries) - 1
    ):

        left = boundaries[index]
        right = boundaries[index + 1]

        left_label = (
            "-∞"
            if left is None
            else _plain(
                special[index - 1]
            )
        )

        right_label = (
            "+∞"
            if right is None
            else _plain(
                special[index]
            )
        )

        columns.append(
            f"({left_label}, {right_label})"
        )

        try:

            sample = _interval_test(
                left,
                right,
            )

            derivative_value = float(
                derivative
                .subs(
                    _X,
                    sample,
                )
                .evalf()
            )

            sign = (
                "+"
                if derivative_value > 1e-10
                else "-"
                if derivative_value < -1e-10
                else "0"
            )

        except Exception:

            sign = "?"

        derivative_cells.append(
            sign
        )

        function_cells.append(
            "↗"
            if sign == "+"
            else "↘"
            if sign == "-"
            else "→"
        )

        interval_rows.append(
            (
                left,
                right,
                sign,
            )
        )

        if index < len(special):

            point = special[index]

            token = str(point)

            columns.append(
                _plain(point)
            )

            if token in vertical_tokens:

                derivative_cells.append(
                    "||"
                )

                function_cells.append(
                    "||"
                )

            else:

                derivative_cells.append(
                    "0"
                )

                try:

                    function_cells.append(
                        _plain(
                            simplify(
                                expr.subs(
                                    _X,
                                    point,
                                )
                            )
                        )
                    )

                except Exception:

                    function_cells.append(
                        "?"
                    )

    # -------------------------------------------------------------------------
    # Increasing / decreasing
    # -------------------------------------------------------------------------

    monotonic = []

    for (
        left,
        right,
        sign,
    ) in interval_rows:

        left_text = (
            "-∞"
            if left is None
            else str(
                round(
                    left,
                    6,
                )
            )
        )

        right_text = (
            "+∞"
            if right is None
            else str(
                round(
                    right,
                    6,
                )
            )
        )

        if sign == "+":

            monotonic.append(
                f"Increasing on ({left_text}, {right_text})"
            )

        elif sign == "-":

            monotonic.append(
                f"Decreasing on ({left_text}, {right_text})"
            )

    # -------------------------------------------------------------------------
    # Extrema
    # -------------------------------------------------------------------------

    extrema = []

    for critical_point in critical:

        try:

            critical_float = float(
                critical_point.evalf()
            )

            y_value = simplify(
                expr.subs(
                    _X,
                    critical_point,
                )
            )

            epsilon = max(
                1e-4,
                abs(critical_float) * 1e-4
                +
                1e-4,
            )

            derivative_left = float(
                derivative
                .subs(
                    _X,
                    critical_float - epsilon,
                )
                .evalf()
            )

            derivative_right = float(
                derivative
                .subs(
                    _X,
                    critical_float + epsilon,
                )
                .evalf()
            )

            if (
                derivative_left > 0
                and
                derivative_right < 0
            ):

                extrema.append(
                    "local maximum at "
                    +
                    "("
                    +
                    _plain(
                        critical_point
                    )
                    +
                    ", "
                    +
                    _plain(
                        y_value
                    )
                    +
                    ")"
                )

            elif (
                derivative_left < 0
                and
                derivative_right > 0
            ):

                extrema.append(
                    "local minimum at "
                    +
                    "("
                    +
                    _plain(
                        critical_point
                    )
                    +
                    ", "
                    +
                    _plain(
                        y_value
                    )
                    +
                    ")"
                )

            else:

                extrema.append(
                    "critical point at "
                    +
                    "("
                    +
                    _plain(
                        critical_point
                    )
                    +
                    ", "
                    +
                    _plain(
                        y_value
                    )
                    +
                    ")"
                )

        except Exception:

            extrema.append(
                "critical point x = "
                +
                _plain(
                    critical_point
                )
            )

    # -------------------------------------------------------------------------
    # Card sections
    # -------------------------------------------------------------------------

    sections = [
        {
            "label": labels["domain"],
            "items": [
                str(domain)
            ],
        },

        {
            "label": labels["limits"],
            "items": limits,
        },

        {
            "label": labels["asymptotes"],
            "items":
                vertical
                +
                other_asymptotes,
        },

        {
            "label": labels["intercepts"],
            "items": intercepts,
        },

        {
            "label": labels["derivative"],
            "items": [
                "f'(x) = "
                +
                str(derivative)
            ],
        },

        {
            "label": labels["critical"],
            "items":
                [
                    "x = "
                    +
                    _plain(value)
                    for value in critical
                ]
                or
                ["None"],
        },

        {
            "label": labels["variation"],
            "items":
                monotonic
                +
                extrema,
        },
    ]

    sections = [
        section
        for section in sections
        if section["items"]
    ]

    # -------------------------------------------------------------------------
    # Final Card
    # -------------------------------------------------------------------------

    key_results = []

    key_results.extend(
        vertical
        +
        other_asymptotes
    )

    key_results.extend(
        extrema
    )

    if not key_results:

        key_results.append(
            "f'(x) = "
            +
            str(derivative)
        )

    # -------------------------------------------------------------------------
    # Return structured card
    # -------------------------------------------------------------------------

    return {
        "kind": "function_study",

        "subject": "Mathematics",

        "language": lang,

        "title":
            "Study of f(x) = "
            +
            expr_text,

        "sections": sections,

        "function_study": {
            "expression":
                expr_text,

            "domain":
                str(domain),

            "limits":
                limits,

            "asymptotes":
                vertical
                +
                other_asymptotes,

            "intercepts":
                intercepts,

            "derivative":
                str(derivative),

            "critical_points":
                [
                    _plain(value)
                    for value in critical
                ],

            "monotonicity":
                monotonic,

            "extrema":
                extrema,

            "variation_table": {
                "columns":
                    columns,

                "rows": [
                    {
                        "label":
                            "f'(x)",

                        "cells":
                            derivative_cells,
                    },

                    {
                        "label":
                            "f(x)",

                        "cells":
                            function_cells,
                    },
                ],
            },
        },

        "drawings":
            drawings,

        "verification": [
            (
                "Function data are computed from "
                "the student's explicit expression."
            ),

            (
                "Graph values must come from the "
                "verified drawing payload; no visual "
                "point is invented by this card engine."
            ),
        ],

        "key_results":
            key_results,
    }


# =============================================================================
# VERIFIED ANSWER BLOCK EXTRACTION
# =============================================================================

def _extract_block(
    reply: str,
    labels: list[str],
) -> str:

    source = _txt(reply)

    for label in labels:

        pattern = re.compile(
            rf"(?im)^\s*(?:#{{1,5}}\s*)?"
            rf"(?:{label})"
            rf"\s*[:：]?\s*(.*)$"
        )

        match = pattern.search(
            source
        )

        if not match:
            continue

        first = _txt(
            match.group(1)
        )

        tail = source[
            match.end():
        ]

        lines = []

        if first:
            lines.append(first)

        for line in tail.splitlines():

            if re.match(
                r"^\s*(?:#{1,5}\s*)?"
                r"[A-Za-zÀ-ÿ\u0600-\u06ff]"
                r"[^:\n]{0,45}[:：]\s*",
                line,
            ):
                break

            if line.strip():
                lines.append(
                    line.strip()
                )

            if len(lines) >= 8:
                break

        return "\n".join(
            lines
        ).strip()

    return ""


# =============================================================================
# PHYSICS / CHEMISTRY / BIOLOGY / SCIENCE / GENERAL MATH
# =============================================================================

def _generic_subject_card(
    kind: str,
    subject: str,
    message: str,
    reply: str,
    drawings: list[dict],
    lang: str,
) -> dict:

    labels = _labels(lang)

    # -------------------------------------------------------------------------
    # Physics
    # -------------------------------------------------------------------------

    if kind == "physics":

        section_specs = [
            (
                labels["given"],
                [
                    r"Given",
                    r"Données",
                    r"المعطيات",
                ],
            ),

            (
                labels["required"],
                [
                    r"Required",
                    r"Demandé",
                    r"المطلوب",
                ],
            ),

            (
                labels["method"],
                [
                    r"Law",
                    r"Formula",
                    r"Loi",
                    r"القانون",
                ],
            ),

            (
                labels["steps"],
                [
                    r"Solution",
                    r"Steps?",
                    r"حل",
                    r"الحل",
                ],
            ),

            (
                labels["verify"],
                [
                    r"Verification",
                    r"Check",
                    r"Vérification",
                    r"التحقق",
                ],
            ),
        ]

    # -------------------------------------------------------------------------
    # Chemistry
    # -------------------------------------------------------------------------

    elif kind == "chemistry":

        section_specs = [
            (
                labels["given"],
                [
                    r"Given",
                    r"Données",
                    r"المعطيات",
                ],
            ),

            (
                labels["required"],
                [
                    r"Required",
                    r"Demandé",
                    r"المطلوب",
                ],
            ),

            (
                labels["chemical_model"],
                [
                    r"Chemical Model",
                    r"Modèle chimique",
                    r"النموذج الكيميائي",
                ],
            ),

            (
                labels["method"],
                [
                    r"Rule",
                    r"Equation",
                    r"Règle",
                    r"Équation",
                    r"القاعدة",
                    r"المعادلة",
                ],
            ),

            (
                labels["steps"],
                [
                    r"Solution",
                    r"Steps?",
                    r"حل",
                    r"الحل",
                ],
            ),

            (
                labels["verify"],
                [
                    r"Verification",
                    r"Check",
                    r"Vérification",
                    r"التحقق",
                ],
            ),
        ]

    # -------------------------------------------------------------------------
    # Biology
    # -------------------------------------------------------------------------

    elif kind == "biology":

        section_specs = [
            (
                labels["observation"],
                [
                    r"Observation",
                    r"الملاحظة",
                ],
            ),

            (
                labels["structure"],
                [
                    r"Structure",
                    r"البنية",
                ],
            ),

            (
                labels["function"],
                [
                    r"Function",
                    r"Fonction",
                    r"الوظيفة",
                ],
            ),

            (
                labels["relation"],
                [
                    r"Structure.?Function",
                    r"Relation structure",
                    r"العلاقة بين البنية والوظيفة",
                ],
            ),

            (
                labels["conclusion"],
                [
                    r"Conclusion",
                    r"استنتاج",
                    r"الاستنتاج",
                ],
            ),
        ]

    # -------------------------------------------------------------------------
    # General Science
    # -------------------------------------------------------------------------

    elif kind == "general_science":

        section_specs = [
            (
                labels["evidence"],
                [
                    r"Evidence",
                    r"Data",
                    r"Données",
                    r"الأدلة",
                    r"المعطيات",
                ],
            ),

            (
                labels["observation"],
                [
                    r"Observation",
                    r"الملاحظة",
                ],
            ),

            (
                labels["interpretation"],
                [
                    r"Interpretation",
                    r"Interprétation",
                    r"التفسير",
                ],
            ),

            (
                labels["conclusion"],
                [
                    r"Conclusion",
                    r"استنتاج",
                    r"الاستنتاج",
                ],
            ),
        ]

    # -------------------------------------------------------------------------
    # Mathematics other than function study
    # -------------------------------------------------------------------------

    else:

        section_specs = [
            (
                labels["given"],
                [
                    r"Given",
                    r"Données",
                    r"المعطيات",
                ],
            ),

            (
                labels["required"],
                [
                    r"Required",
                    r"Demandé",
                    r"المطلوب",
                ],
            ),

            (
                labels["method"],
                [
                    r"Rule",
                    r"Property",
                    r"Method",
                    r"Propriété",
                    r"Méthode",
                    r"القاعدة",
                    r"الخاصية",
                ],
            ),

            (
                labels["steps"],
                [
                    r"Solution",
                    r"Steps?",
                    r"حل",
                    r"الحل",
                ],
            ),

            (
                labels["verify"],
                [
                    r"Verification",
                    r"Check",
                    r"Vérification",
                    r"التحقق",
                ],
            ),
        ]

    sections = []

    for label, aliases in section_specs:

        block = _extract_block(
            reply,
            aliases,
        )

        if block:

            sections.append({
                "label":
                    label,

                "items": [
                    block
                ],
            })

    # Never invent missing sections.
    # If the verified answer has no labelled structure,
    # preserve the actual answer as the solution section.
    if (
        not sections
        and
        _txt(reply)
    ):

        sections.append({
            "label":
                labels["steps"],

            "items": [
                _txt(reply)
            ],
        })

    verification = []

    verification_block = _extract_block(
        reply,
        [
            r"Verification",
            r"Check",
            r"Vérification",
            r"التحقق",
        ],
    )

    if verification_block:

        verification.append(
            verification_block
        )

    final = _extract_block(
        reply,
        [
            r"Final Answer",
            r"Réponse finale",
            r"الجواب النهائي",
            r"النتيجة النهائية",
        ],
    )

    return {
        "kind":
            kind,

        "subject":
            subject
            or
            kind.replace(
                "_",
                " ",
            ).title(),

        "language":
            lang,

        "title":
            _txt(message)[:220]
            or
            "Scientific Solution",

        "sections":
            sections,

        "drawings":
            drawings,

        "verification":
            verification,

        "key_results":
            [final]
            if final
            else [],
    }


# =============================================================================
# PUBLIC ENTRY POINT
# =============================================================================

def build_scientific_solution_card(
    *,
    message: str,
    reply: str,
    subject: str = "",
    drawings: Optional[list[dict]] = None,
) -> Optional[dict]:
    """
    Build one Scientific Solution Card payload.

    Returns None when the request is not a scientific exercise/card request.

    Function studies:
        deterministic symbolic analysis from the student's expression.

    Other scientific subjects:
        only reorganize verified answer content and verified drawings.
        Missing scientific information is never invented here.
    """

    drawings = [
        drawing
        for drawing in (
            drawings
            or
            []
        )
        if isinstance(
            drawing,
            dict,
        )
    ]

    kind = _detect_kind(
        message,
        subject,
    )

    if not kind:
        return None

    lang = _language(
        f"{message}\n{reply}"
    )

    # -------------------------------------------------------------------------
    # Function study
    # -------------------------------------------------------------------------

    if kind == "function_study":

        card = _function_card(
            message,
            reply,
            drawings,
            lang,
        )

        if card:
            return card

        # Fail closed.
        # We preserve verified prose but do not fabricate symbolic analysis.
        return {
            "kind":
                "function_study",

            "subject":
                "Mathematics",

            "language":
                lang,

            "title":
                _txt(message)[:220]
                or
                "Function Study",

            "sections": [
                {
                    "label":
                        _labels(lang)[
                            "steps"
                        ],

                    "items":
                        [
                            _txt(reply)
                        ]
                        if _txt(reply)
                        else [],
                }
            ],

            "drawings":
                drawings,

            "verification": [
                (
                    "Structured symbolic analysis was not created "
                    "because the function expression could not be "
                    "parsed safely."
                )
            ],

            "key_results":
                [],
        }

    # -------------------------------------------------------------------------
    # Other subjects
    # -------------------------------------------------------------------------

    return _generic_subject_card(
        kind,
        subject,
        message,
        reply,
        drawings,
        lang,
    )
