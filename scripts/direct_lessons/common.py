"""Shared helpers for direct lesson modules (data -> V6 scenes)."""
from __future__ import annotations

def T(en, ar, fr, label=None):
    return {"k": "t", "en": en, "ar": ar, "fr": fr, "label": label}


def F(f):
    return {"k": "f", "f": f}


def D(name, **args):
    return {"k": "d", "draw": name, "args": args}



def EX(n, page, stmt, steps):
    return {"n": n, "page": page, "stmt": stmt, "steps": steps}


def st(en, ar, fr):
    return (en, ar, fr)


S = T


def _step(x):
    if x["k"] == "t":
        d = {"t": "text", "text": x["en"], "label": x.get("label") or "", "speech": x["en"],
             "ar": x["ar"], "en": x["en"], "fr": x["fr"]}
        return d
    if x["k"] == "f":
        return {"t": "formula", "text": x["f"]}
    return {"t": "draw", "draw": x["draw"], "args": x.get("args", {})}


def make_scenes(THEORY, EXERCISES):
    out = []
    for i, (te, ta, tf, page, steps) in enumerate(THEORY, 1):
        out.append({"id": f"P{i}", "page": page, "title": te, "title_en": te, "title_ar": ta, "title_fr": tf,
                    "start_mode": "single", "steps": [_step(s) for s in steps]})
    for e in EXERCISES:
        en, ar, fr = e["stmt"]
        label = {"en": "Exercise", "ar": "التمرين", "fr": "Exercice"}
        steps = [{"t": "text", "text": en, "label": "Problem", "speech": en, "ar": ar, "en": en, "fr": fr}]
        steps += [_step(s) for s in e["steps"]]
        out.append({"id": f"EX-{e['n']}", "page": e["page"], "exercise": e["n"], "solved": True,
                    "title": f"Exercise {e['n']}", "title_en": f"Exercise {e['n']}",
                    "title_ar": f"التمرين {e['n']}", "title_fr": f"Exercice {e['n']}",
                    "start_mode": "single", "steps": steps})
    return out


# ------------------------------------------------------------ drawing helpers
def _shape(kind, cx, cy, r, color, sid):
    if kind == "star":
        import math
        pts = []
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5
            rr = r if i % 2 == 0 else r * 0.45
            pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
        return f'<polygon id="{sid}" points="{" ".join(pts)}" fill="{color}" stroke="#0b3d5c" stroke-width="3"/>'
    if kind == "square":
        return f'<rect id="{sid}" x="{cx - r}" y="{cy - r}" width="{2 * r}" height="{2 * r}" fill="{color}" stroke="#0b3d5c" stroke-width="3"/>'
    if kind == "tri":
        return (f'<polygon id="{sid}" points="{cx},{cy - r} {cx - r},{cy + r} {cx + r},{cy + r}" fill="{color}" '
                f'stroke="#0b3d5c" stroke-width="3"/>')
    return f'<circle id="{sid}" cx="{cx}" cy="{cy}" r="{r}" fill="{color}" stroke="#0b3d5c" stroke-width="3"/>'


def row(n, kind="circle", color="#e53935", y=200, prefix="o", r=34, vbw=660, gap=None, x0=None):
    """n identical objects on a line. returns (svg, ids)."""
    gap = gap or (2 * r + 30)
    total = gap * (n - 1)
    x0 = x0 if x0 is not None else (vbw - total) / 2
    ids = [f"{prefix}{i}" for i in range(n)]
    svg = "".join(_shape(kind, x0 + i * gap, y, r, color, ids[i]) for i in range(n))
    return svg, ids


def numeral(txt, x=330, y=330, size=90, sid="num", color="#0b3d5c"):
    return (f'<text id="{sid}" x="{x}" y="{y}" font-size="{size}" font-weight="700" text-anchor="middle" '
            f'fill="{color}" font-family="sans-serif">{txt}</text>')


def scene(svg, ids):
    return D("svgScene", svg=svg, vb=[660, 440], show=ids)


def objects(n, kind="circle", color="#e53935", number=None, y=170, prefix="o", r=34):
    svg, ids = row(n, kind, color, y, prefix, r)
    if number is not None:
        svg += numeral(number, y=y + 170, sid=prefix + "n")
        ids = ids + [prefix + "n"]
    return scene(svg, ids)


def join(a, b, ka="star", kb="star", ca="#fbc02d", cb="#43a047", y=150, total=True):
    """two groups side by side with a plus sign; optional equals + total."""
    r = 26
    svg1, ids1 = row(a, ka, ca, y, "A", r, gap=64, x0=40)
    svg2, ids2 = row(b, kb, cb, y, "B", r, gap=64, x0=40 + 64 * a + 70)
    plus = numeral("+", 40 + 64 * (a - 1) + 55, y + 22, 60, "plus")
    svg, ids = svg1 + plus + svg2, ids1 + ["plus"] + ids2
    if total:
        svg += numeral(f"{a} + {b} = {a + b}", 330, 340, 90, "eqn")
        ids.append("eqn")
    return scene(svg, ids)


def pairs(a, b, ka="star", kb="circle", ca="#fbc02d", cb="#1e63d6", lines=True, gap=70, tag="P", r=24, ya=90, yb=300):
    """two rows (a above, b below); one-to-one lines for min(a,b). returns scene."""
    def xs(n):
        return [(660 - gap * (n - 1)) / 2 + i * gap for i in range(n)]
    xa, xb = xs(a), xs(b)
    svg, ids = "", []
    for i, x in enumerate(xa):
        sid = f"{tag}a{i}"
        svg += _shape(ka, x, ya, r, ca, sid); ids.append(sid)
    for i, x in enumerate(xb):
        sid = f"{tag}b{i}"
        svg += _shape(kb, x, yb, r, cb, sid); ids.append(sid)
    if lines:
        for i in range(min(a, b)):
            sid = f"{tag}l{i}"
            svg += (f'<line id="{sid}" x1="{xa[i]}" y1="{ya + r}" x2="{xb[i]}" y2="{yb - r}" '
                    f'stroke="#0b3d5c" stroke-width="4"/>')
            ids.append(sid)
    return scene(svg, ids)


def spread(n, gap, kind="circle", color="#e53935", y=200, tag="S", r=24):
    svg, ids = row(n, kind, color, y, tag, r, gap=gap)
    return scene(svg, ids)


def numpath(items, hi=None, tag="N", y=200, size=64):
    """a row of numeral boxes. items: list of str ('' or '?' = blank). hi: index to highlight."""
    n = len(items)
    gap = min(80, 620 / max(n, 1))
    x0 = (660 - gap * (n - 1)) / 2
    svg, ids = "", []
    for i, v in enumerate(items):
        x = x0 + i * gap
        sid = f"{tag}{i}"
        fill = "#ffe082" if hi == i else ("#ffffff" if v not in ("", "?") else "#e0e0e0")
        txt = v if v not in ("", "?") else "?"
        svg += (f'<g id="{sid}"><rect x="{x - gap / 2 + 4}" y="{y - 44}" width="{gap - 8}" height="88" rx="10" '
                f'fill="{fill}" stroke="#0b3d5c" stroke-width="3"/>'
                f'<text x="{x}" y="{y + 22}" font-size="{size * 0.8:.0f}" font-weight="700" text-anchor="middle" '
                f'fill="#0b3d5c" font-family="sans-serif">{txt}</text></g>')
        ids.append(sid)
    return scene(svg, ids)


def tens(t, o, bundled=True, tag="T", color="#1e63d6", ocolor="#e53935", label=True, eq=False):
    """t bundles of ten (boxed, 2 rows of 5) + o loose ones. bundled=False: open tens drawn loose in a row."""
    svg, ids = "", []
    for r in (13, 11, 9, 7, 6):
        bw, bh = 5 * 2 * r + 30, 2 * 2 * r + 30
        gap = 26
        loose_w = (min(o, 5) * (2 * r + 8)) if o else 0
        total_w = t * bw + max(t - 1, 0) * gap + (gap + loose_w if o and t else loose_w)
        if total_w <= 620:
            break
    x = (660 - total_w) / 2
    y = 120
    for b in range(t):
        bid = f"{tag}b{b}"
        if bundled:
            svg += f'<rect id="{bid}" x="{x}" y="{y}" width="{bw}" height="{bh}" rx="12" fill="#e3f2fd" stroke="#0b3d5c" stroke-width="3"/>'
            ids.append(bid)
        for k in range(10):
            cx = x + 15 + r + (k % 5) * (2 * r + 0)
            cy = y + 15 + r + (k // 5) * (2 * r)
            sid = f"{tag}c{b}_{k}"
            svg += _shape("circle", cx, cy, r - 1, color, sid); ids.append(sid)
        x += bw + gap
    for k in range(o):
        cx = x + r + (k % 5) * (2 * r + 8)
        cy = y + 30 + (k // 5) * (2 * r + 8) + r
        sid = f"{tag}o{k}"
        svg += _shape("circle", cx, cy, r - 1, ocolor, sid); ids.append(sid)
    if label:
        txt = f"{t} ten" + ("s" if t != 1 else "") + (f" + {o} one" + ("s" if o != 1 else "") if o else "")
        if eq:
            txt += f" = {t * 10 + o}"
        svg += numeral(txt, 330, 340, 54, tag + "lab")
        ids.append(tag + "lab")
    return scene(svg, ids)


def jumps(start, k, hi=10, back=False, tag="J", label=True):
    """number line 0..hi, k unit jumps from start (arcs drawn in order)."""
    x0, x1, y = 40, 620, 270
    step = (x1 - x0) / hi
    X = lambda n: x0 + n * step
    svg = f'<line id="{tag}ln" x1="{x0 - 10}" y1="{y}" x2="{x1 + 10}" y2="{y}" stroke="#0b3d5c" stroke-width="5"/>'
    ids = [tag + "ln"]
    for n in range(hi + 1):
        svg += (f'<line x1="{X(n)}" y1="{y - 10}" x2="{X(n)}" y2="{y + 10}" stroke="#0b3d5c" stroke-width="3"/>'
                f'<text x="{X(n)}" y="{y + 42}" font-size="26" font-weight="700" text-anchor="middle" fill="#0b3d5c" font-family="sans-serif">{n}</text>')
    svg += f'<circle id="{tag}st" cx="{X(start)}" cy="{y}" r="12" fill="#e53935" stroke="#0b3d5c" stroke-width="3"/>'
    ids.append(tag + "st")
    d = -1 if back else 1
    for i in range(k):
        a, b = start + d * i, start + d * (i + 1)
        mid = (X(a) + X(b)) / 2
        sid = f"{tag}j{i}"
        svg += (f'<path id="{sid}" d="M {X(a)} {y - 14} Q {mid} {y - 95} {X(b)} {y - 14}" fill="none" stroke="#1e63d6" stroke-width="5"/>')
        ids.append(sid)
    end = start + d * k
    svg += f'<circle id="{tag}en" cx="{X(end)}" cy="{y}" r="14" fill="#43a047" stroke="#0b3d5c" stroke-width="3"/>'
    ids.append(tag + "en")
    if label:
        op = "-" if back else "+"
        svg += numeral(f"{start} {op} {k} = {end}", 330, 130, 64, tag + "eq")
        ids.append(tag + "eq")
    return scene(svg, ids)


def strips(items, tag="L", x_min=40, unit=50, gap=70, ref=None, rot=None):
    """items: list of (label, start, length, color). draws horizontal strips; optional start guide line."""
    svg, ids = "", []
    y = 80
    for i, (lab, s, ln, col) in enumerate(items):
        sid = f"{tag}{i}"
        x = x_min + s * unit
        r = ""
        if rot and rot.get(i):
            cx, cy = x + ln * unit / 2, y + 18
            r = f' transform="rotate({rot[i]} {cx} {cy})"'
        svg += (f'<g id="{sid}"{r}><rect x="{x}" y="{y}" width="{ln * unit}" height="36" rx="6" fill="{col}" stroke="#0b3d5c" stroke-width="3"/>'
                f'<text x="{x - 22}" y="{y + 27}" font-size="28" font-weight="700" text-anchor="end" fill="#0b3d5c" font-family="sans-serif">{lab}</text></g>')
        ids.append(sid)
        y += gap
    if ref is not None:
        gx = x_min + ref * unit
        svg += f'<line id="{tag}g" x1="{gx}" y1="40" x2="{gx}" y2="{y}" stroke="#e53935" stroke-width="3" stroke-dasharray="8 6"/>'
        ids.append(tag + "g")
    return scene(svg, ids)
