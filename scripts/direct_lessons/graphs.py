"""Function-graph helper: fn_graph(f, xr, yr, pts, vlines, hlines, extra_curves, tag) -> scene (for D/svgScene)."""
import math
from scripts.direct_lessons.common import scene

W, H, M = 660, 440, 40


def fn_graph(f, xr=(-5, 5), yr=(-5, 5), pts=None, vlines=(), hlines=(), curves=(), tag="G", label=None, poles=()):
    """f: python callable. pts: {'A':(x,y)}. vlines/hlines: asymptote positions. curves: extra callables (dashed, e.g. tangent/inverse).
    poles: x values where f is discontinuous (curve is split there). Returns a scene whose ids are tag+'a'(axes) tag+'c'(curve) tag+'p<name>'."""
    x0, x1 = xr; y0, y1 = yr
    X = lambda v: M + (v - x0) / (x1 - x0) * (W - 2 * M)
    Y = lambda v: H - M - (v - y0) / (y1 - y0) * (H - 2 * M)
    sx = max(1, round((x1 - x0) / 10)); sy = max(1, round((y1 - y0) / 8))
    s = f'<g id="{tag}a">'
    for i in range(math.ceil(x0), math.floor(x1) + 1):
        if i % sx == 0:
            s += f'<line x1="{X(i):.1f}" y1="{Y(y0):.1f}" x2="{X(i):.1f}" y2="{Y(y1):.1f}" stroke="#e0e6ea" stroke-width="2"/>'
            if i: s += f'<text x="{X(i):.1f}" y="{Y(0)+20 if y0<0<y1 else H-12:.1f}" font-size="15" text-anchor="middle" fill="#0b3d5c" font-family="sans-serif">{i}</text>'
    for j in range(math.ceil(y0), math.floor(y1) + 1):
        if j % sy == 0:
            s += f'<line x1="{X(x0):.1f}" y1="{Y(j):.1f}" x2="{X(x1):.1f}" y2="{Y(j):.1f}" stroke="#e0e6ea" stroke-width="2"/>'
            if j: s += f'<text x="{X(0)-8 if x0<0<x1 else 30:.1f}" y="{Y(j)+5:.1f}" font-size="15" text-anchor="end" fill="#0b3d5c" font-family="sans-serif">{j}</text>'
    ax = Y(0) if y0 < 0 < y1 else Y(y0); ay = X(0) if x0 < 0 < x1 else X(x0)
    s += (f'<line x1="{X(x0):.1f}" y1="{ax:.1f}" x2="{X(x1):.1f}" y2="{ax:.1f}" stroke="#0b3d5c" stroke-width="4"/>'
          f'<line x1="{ay:.1f}" y1="{Y(y0):.1f}" x2="{ay:.1f}" y2="{Y(y1):.1f}" stroke="#0b3d5c" stroke-width="4"/></g>')
    ids = [tag + "a"]

    def path(fn, color, dash=""):
        segs, cur = [], []
        n = 400
        for k in range(n + 1):
            x = x0 + (x1 - x0) * k / n
            try:
                y = fn(x)
                ok = isinstance(y, (int, float)) and math.isfinite(y) and y0 <= y <= y1 and not any(abs(x - p) < (x1 - x0) / n * 1.5 for p in poles)
            except Exception:
                ok = False
            if ok: cur.append((X(x), Y(y)))
            elif cur: segs.append(cur); cur = []
        if cur: segs.append(cur)
        d = "".join("M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in sg) for sg in segs if len(sg) > 1)
        return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="5" stroke-linejoin="round" {dash}/>'
    s += f'<g id="{tag}c">{path(f, "#e53935")}'
    if label: s += f'<text x="{W-M-6}" y="{M+4}" font-size="20" font-weight="700" text-anchor="end" fill="#e53935" font-family="sans-serif">{label}</text>'
    s += '</g>'; ids.append(tag + "c")
    if vlines or hlines:
        s += f'<g id="{tag}s">'
        for v in vlines: s += f'<line x1="{X(v):.1f}" y1="{Y(y0):.1f}" x2="{X(v):.1f}" y2="{Y(y1):.1f}" stroke="#8e24aa" stroke-width="3" stroke-dasharray="10 7"/>'
        for h in hlines: s += f'<line x1="{X(x0):.1f}" y1="{Y(h):.1f}" x2="{X(x1):.1f}" y2="{Y(h):.1f}" stroke="#8e24aa" stroke-width="3" stroke-dasharray="10 7"/>'
        s += '</g>'; ids.append(tag + "s")
    for i, cf in enumerate(curves):
        s += f'<g id="{tag}x{i}">{path(cf, "#1e88e5", "stroke-dasharray=\"12 8\"")}</g>'; ids.append(f"{tag}x{i}")
    for k, (x, y) in (pts or {}).items():
        s += (f'<g id="{tag}p{k}"><circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="9" fill="#1e88e5" stroke="#0b3d5c" stroke-width="2"/>'
              f'<text x="{X(x)+12:.1f}" y="{Y(y)-10:.1f}" font-size="19" font-weight="700" fill="#0b3d5c" font-family="sans-serif">{k}({x:g},{y:g})</text></g>')
        ids.append(f"{tag}p{k}")
    return scene(s, ids)


def section(m, en_title):
    """Return the step list of the THEORY section whose English title matches (for upgrades)."""
    for s in m.THEORY:
        if s[0] == en_title:
            return s[-1]
    raise KeyError(en_title)
