"""Deterministic table of variation for single-variable real functions.

Never produced by an LLM: derived with sympy from an explicit f(x) expression.
Returns None whenever any step cannot be proven (no table is better than a wrong one).
"""
from __future__ import annotations

import re

_ALLOWED = re.compile(r"^[0-9xX+\-*/^().\s]*$")
_FUNC_RE = re.compile(r"\b[fgh]\s*\(\s*x\s*\)\s*=\s*([^;,\n]+?)\s*(?:$|[;\n])", re.I)


def extract_function_expr(act: dict) -> str:
    """Find an explicit f(x)=... in the activity (explicit field, lab spec, formulas)."""
    cands = [act.get("function_expr")]
    spec = act.get("lab_spec")
    if isinstance(spec, dict):
        cands += [spec.get("function_expr"), spec.get("function"), spec.get("expression")]
    for c in cands:
        if isinstance(c, str) and c.strip():
            return re.sub(r"^\s*[fgh]\s*\(\s*x\s*\)\s*=\s*", "", c.strip())
    for f in (act.get("formulas") or []):
        m = _FUNC_RE.search(str(f) + "\n")
        if m:
            return m.group(1).strip()
    return ""


def _fmt(v) -> str:
    try:
        f = float(v)
    except Exception:
        return str(v)
    return f"{f:.3f}".rstrip("0").rstrip(".").replace("-", "−")


def build_variation_table(expr_text: str) -> dict | None:
    s = (expr_text or "").strip().replace("−", "-").replace("×", "*").replace("·", "*")
    s = s.replace("²", "^2").replace("³", "^3").replace("^", "**")
    s = re.sub(r"(\d)\s*x", r"\1*x", s, flags=re.I)
    s = re.sub(r"\)\s*\(", ")*(", s)
    s = re.sub(r"(\d|x|\))\s*\(", r"\1*(", s)
    if not s or len(s) > 120 or not _ALLOWED.match(s.replace("**", "^")):
        return None
    try:
        import sympy as sp
        x = sp.Symbol("x", real=True)
        f = sp.sympify(s.replace("X", "x"), locals={"x": x}, rational=True)
        if f.free_symbols - {x}:
            return None
        den = sp.denom(sp.together(f))
        poles = sorted({r for r in sp.solve(den, x) if r.is_real}, key=lambda r: float(r)) if den.has(x) else []
        d = sp.simplify(sp.diff(f, x))
        crit = sorted({r for r in sp.solve(sp.numer(sp.together(d)), x)
                       if r.is_real and r not in poles}, key=lambda r: float(r))
        pts = sorted(set(poles) | set(crit), key=lambda r: float(r))
        if not pts or len(pts) > 6:
            return None
        cols, dsign, fsign = [], [], []
        edges = [None] + pts + [None]
        for i in range(len(edges) - 1):
            lo, hi = edges[i], edges[i + 1]
            lo_s = "−∞" if lo is None else _fmt(lo)
            hi_s = "+∞" if hi is None else _fmt(hi)
            probe = (float(hi) - 1) if lo is None else (float(lo) + 1) if hi is None else (float(lo) + float(hi)) / 2
            v = d.subs(x, sp.Rational(probe).limit_denominator(10**6))
            if v == 0 or not v.is_real:
                return None
            up = bool(v > 0)
            cols.append(f"({lo_s}, {hi_s})")
            dsign.append("+" if up else "−")
            fsign.append("↗" if up else "↘")
            if hi is not None:
                if hi in poles:
                    cols.append(_fmt(hi)); dsign.append("∥"); fsign.append("∥")
                else:
                    cols.append(_fmt(hi)); dsign.append("0")
                    nxt = d.subs(x, sp.Rational(float(hi) + 0.5 if i + 2 >= len(edges) - 1 and edges[i + 2] is None
                                                else (float(hi) + float(edges[i + 2])) / 2).limit_denominator(10**6))
                    kind = ("max" if up and nxt < 0 else "min" if (not up) and nxt > 0 else "")
                    val = _fmt(f.subs(x, hi))
                    fsign.append((f"local {kind} ≈ {val}" if kind else val))
        return {"columns": cols,
                "rows": [{"label": "f′(x)", "cells": dsign}, {"label": "f(x)", "cells": fsign}],
                "poles": [_fmt(p) for p in poles], "critical": [_fmt(c) for c in crit]}
    except Exception:
        return None


def build_function_drawing(expr_text: str, table: dict | None = None) -> dict | None:
    """Deterministic graph spec (engine `function` drawing) for the same f(x)."""
    t = table or build_variation_table(expr_text)
    if not t:
        return None
    try:
        import sympy as sp
        s = (expr_text or "").replace("−", "-").replace("×", "*").replace("·", "*")
        s = s.replace("²", "^2").replace("³", "^3").replace("^", "**")
        s = re.sub(r"(\d)\s*x", r"\1*x", s, flags=re.I)
        s = re.sub(r"\)\s*\(", ")*(", s)
        s = re.sub(r"(\d|x|\))\s*\(", r"\1*(", s)
        x = sp.Symbol("x", real=True)
        f = sp.sympify(s, locals={"x": x}, rational=True)
        fn = sp.lambdify(x, f, "math")
        poles = [float(p.replace("−", "-")) for p in t.get("poles", [])]
        crit = [float(c.replace("−", "-")) for c in t.get("critical", [])]
        pts = sorted(poles + crit)
        span = max(pts) - min(pts)
        pad = max(span * 0.8, 3.0)
        xmin, xmax = min(pts) - pad, max(pts) + pad
        cuts = [xmin - 1] + sorted(poles) + [xmax + 1]
        series, ys = [], []
        for a, b in zip(cuts, cuts[1:]):
            seg, n = [], 220
            lo, hi = max(a, xmin) + (0.02 if a in poles else 0), min(b, xmax) - (0.02 if b in poles else 0)
            if hi <= lo:
                continue
            for i in range(n + 1):
                xv = lo + (hi - lo) * i / n
                try:
                    yv = float(fn(xv))
                except Exception:
                    continue
                if abs(yv) < 1e3:
                    seg.append([round(xv, 3), round(yv, 4)]); ys.append(yv)
            if len(seg) > 1:
                series.append(seg)
        if not ys:
            return None
        cy = sorted(float(fn(c)) for c in crit)
        ref = cy if cy else ys
        ymin = max(min(ys), min(ref) - 8) - 1
        ymax = min(max(ys), max(ref) + 8) + 1
        if ymax - ymin < 2:
            ymin, ymax = ymin - 2, ymax + 2
        oblique = []
        num, den = sp.fraction(sp.together(f))
        if den.has(x) and sp.degree(num, x) == sp.degree(den, x) + 1:
            q, _ = sp.div(num, den, x)
            m, bb = sp.Poly(q, x).all_coeffs()
            oblique.append({"m": float(m), "b": float(bb),
                            "label": f"y = {_fmt(m)}x + {_fmt(bb)}".replace("+ −", "− ")})
        markers = []
        for c in crit:
            markers.append({"x": round(c, 3), "y": round(float(fn(c)), 3),
                            "label": f"x = {_fmt(c)}"})
        return {"type": "function", "title": "f(x)", "curve_label": "f(x) = " + expr_text.strip(),
                "xmin": round(xmin, 2), "xmax": round(xmax, 2), "ymin": round(ymin, 2), "ymax": round(ymax, 2),
                "series": series,
                "vertical_asymptotes": [{"x": p, "label": f"x = {_fmt(p)}"} for p in poles],
                "oblique_asymptotes": oblique, "markers": markers}
    except Exception:
        return None
