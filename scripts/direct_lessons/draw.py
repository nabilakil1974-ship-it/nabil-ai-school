"""Reusable lesson drawings returned as svgScene steps: number line, Venn, bars, vectors, unit circle."""
import math
from scripts.direct_lessons.common import scene

INK = "#0b3d5c"; RED = "#e53935"; BLUE = "#1e88e5"; GREEN = "#2e7d32"; GOLD = "#f9a825"
FF = 'font-family="sans-serif"'


def numberline(lo, hi, marks=None, intervals=None, tag="NL", step=1):
    """marks: {label: value} dots; intervals: list of (a, b, left_closed, right_closed, color) drawn as thick bars (None = infinite)."""
    X = lambda v: 40 + (v - lo) / (hi - lo) * 580
    y = 220
    s = f'<g id="{tag}a"><line x1="30" y1="{y}" x2="630" y2="{y}" stroke="{INK}" stroke-width="5"/>'
    v = lo if step < 1 else math.ceil(lo)
    while v <= hi + 1e-9:
        s += f'<line x1="{X(v):.1f}" y1="{y-10}" x2="{X(v):.1f}" y2="{y+10}" stroke="{INK}" stroke-width="3"/><text x="{X(v):.1f}" y="{y+34}" font-size="20" text-anchor="middle" fill="{INK}" {FF}>{round(v,2):g}</text>'
        v = round(v + step, 6)
    s += '</g>'
    ids = [tag + "a"]
    for i, (a, b, lc, rc, col) in enumerate(intervals or []):
        a2 = lo - 0.4 if a is None else a; b2 = hi + 0.4 if b is None else b
        g = f'<g id="{tag}i{i}"><line x1="{X(a2):.1f}" y1="{y}" x2="{X(b2):.1f}" y2="{y}" stroke="{col or RED}" stroke-width="12" stroke-linecap="round" opacity=".85"/>'
        if a is not None: g += f'<circle cx="{X(a):.1f}" cy="{y}" r="11" fill="{col or RED if lc else "#fff"}" stroke="{col or RED}" stroke-width="4"/>'
        if b is not None: g += f'<circle cx="{X(b):.1f}" cy="{y}" r="11" fill="{col or RED if rc else "#fff"}" stroke="{col or RED}" stroke-width="4"/>'
        s += g + '</g>'; ids.append(f"{tag}i{i}")
    for k, (lab, val) in enumerate((marks or {}).items()):
        s += f'<g id="{tag}m{k}"><circle cx="{X(val):.1f}" cy="{y}" r="10" fill="{BLUE}" stroke="{INK}" stroke-width="3"/><text x="{X(val):.1f}" y="{y-24}" font-size="22" font-weight="700" text-anchor="middle" fill="{INK}" {FF}>{lab}</text></g>'
        ids.append(f"{tag}m{k}")
    return scene(s, ids)


def venn(a_label, b_label, a_only, b_only, both, outside=None, tag="V"):
    """Two overlapping sets; texts are short strings placed in the regions."""
    s = (f'<g id="{tag}a"><rect x="20" y="30" width="620" height="380" rx="14" fill="none" stroke="{INK}" stroke-width="4"/>'
         f'<circle cx="250" cy="220" r="140" fill="{BLUE}" fill-opacity=".25" stroke="{BLUE}" stroke-width="5"/>'
         f'<circle cx="410" cy="220" r="140" fill="{RED}" fill-opacity=".22" stroke="{RED}" stroke-width="5"/>'
         f'<text x="160" y="70" font-size="26" font-weight="700" fill="{BLUE}" {FF}>{a_label}</text><text x="470" y="70" font-size="26" font-weight="700" fill="{RED}" {FF}>{b_label}</text></g>')
    ids = [tag + "a"]
    for k, (txt, x) in enumerate([(a_only, 185), (both, 330), (b_only, 475)]):
        s += f'<g id="{tag}r{k}"><text x="{x}" y="228" font-size="24" font-weight="700" text-anchor="middle" fill="{INK}" {FF}>{txt}</text></g>'; ids.append(f"{tag}r{k}")
    if outside:
        s += f'<g id="{tag}o"><text x="60" y="390" font-size="22" fill="{INK}" {FF}>{outside}</text></g>'; ids.append(tag + "o")
    return scene(s, ids)


def bars(labels, values, tag="BR", color=BLUE, ymax=None, title=None):
    n = len(values); ymax = ymax or max(values) * 1.15
    bw = 520 / n; base = 380
    Y = lambda v: base - v / ymax * 320
    s = f'<g id="{tag}a"><line x1="60" y1="{base}" x2="630" y2="{base}" stroke="{INK}" stroke-width="4"/><line x1="60" y1="{base}" x2="60" y2="50" stroke="{INK}" stroke-width="4"/>'
    for t in range(0, int(ymax) + 1, max(1, int(ymax // 5) or 1)):
        s += f'<line x1="56" y1="{Y(t):.1f}" x2="64" y2="{Y(t):.1f}" stroke="{INK}" stroke-width="3"/><text x="50" y="{Y(t)+6:.1f}" font-size="16" text-anchor="end" fill="{INK}" {FF}>{t}</text>'
    if title: s += f'<text x="340" y="36" font-size="22" font-weight="700" text-anchor="middle" fill="{INK}" {FF}>{title}</text>'
    s += '</g>'
    ids = [tag + "a"]
    for k, (lab, v) in enumerate(zip(labels, values)):
        x = 70 + k * bw
        s += (f'<g id="{tag}b{k}"><rect x="{x+6:.1f}" y="{Y(v):.1f}" width="{bw-12:.1f}" height="{base-Y(v):.1f}" fill="{color}" stroke="{INK}" stroke-width="2"/>'
              f'<text x="{x+bw/2:.1f}" y="{Y(v)-8:.1f}" font-size="18" font-weight="700" text-anchor="middle" fill="{INK}" {FF}>{v:g}</text>'
              f'<text x="{x+bw/2:.1f}" y="{base+24}" font-size="16" text-anchor="middle" fill="{INK}" {FF}>{lab}</text></g>')
        ids.append(f"{tag}b{k}")
    return scene(s, ids)


def vectors(vecs, lo=(-1, -1), hi=(7, 6), tag="VC", labels=True):
    """vecs: list of (label, (x0,y0), (x1,y1), color). Grid with arrows."""
    X = lambda v: 40 + (v - lo[0]) / (hi[0] - lo[0]) * 580
    Y = lambda v: 400 - (v - lo[1]) / (hi[1] - lo[1]) * 360
    s = f'<g id="{tag}a">'
    for i in range(lo[0], hi[0] + 1):
        s += f'<line x1="{X(i):.1f}" y1="{Y(lo[1]):.1f}" x2="{X(i):.1f}" y2="{Y(hi[1]):.1f}" stroke="#e0e6ea" stroke-width="2"/>'
        if i: s += f'<text x="{X(i):.1f}" y="{Y(0)+20:.1f}" font-size="15" text-anchor="middle" fill="{INK}" {FF}>{i}</text>'
    for j in range(lo[1], hi[1] + 1):
        s += f'<line x1="{X(lo[0]):.1f}" y1="{Y(j):.1f}" x2="{X(hi[0]):.1f}" y2="{Y(j):.1f}" stroke="#e0e6ea" stroke-width="2"/>'
        if j: s += f'<text x="{X(0)-8:.1f}" y="{Y(j)+5:.1f}" font-size="15" text-anchor="end" fill="{INK}" {FF}>{j}</text>'
    s += (f'<line x1="{X(lo[0]):.1f}" y1="{Y(0):.1f}" x2="{X(hi[0]):.1f}" y2="{Y(0):.1f}" stroke="{INK}" stroke-width="4"/>'
          f'<line x1="{X(0):.1f}" y1="{Y(lo[1]):.1f}" x2="{X(0):.1f}" y2="{Y(hi[1]):.1f}" stroke="{INK}" stroke-width="4"/></g>')
    ids = [tag + "a"]
    for k, (lab, p, q, col) in enumerate(vecs):
        x0, y0, x1, y1 = X(p[0]), Y(p[1]), X(q[0]), Y(q[1])
        ang = math.atan2(y1 - y0, x1 - x0); L = 16
        h = f"{x1:.1f},{y1:.1f} {x1-L*math.cos(ang-0.4):.1f},{y1-L*math.sin(ang-0.4):.1f} {x1-L*math.cos(ang+0.4):.1f},{y1-L*math.sin(ang+0.4):.1f}"
        s += (f'<g id="{tag}v{k}"><line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{col}" stroke-width="6" stroke-linecap="round"/>'
              f'<polygon points="{h}" fill="{col}"/>')
        if labels: s += f'<text x="{(x0+x1)/2+10:.1f}" y="{(y0+y1)/2-10:.1f}" font-size="22" font-weight="700" fill="{col}" {FF}>{lab}</text>'
        s += '</g>'; ids.append(f"{tag}v{k}")
    return scene(s, ids)


def unit_circle(angles_deg=(30, 45, 60), tag="UC"):
    cx, cy, r = 215, 220, 160
    s = (f'<g id="{tag}a"><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="4"/>'
         f'<line x1="{cx-r-25}" y1="{cy}" x2="{cx+r+25}" y2="{cy}" stroke="{INK}" stroke-width="3"/><line x1="{cx}" y1="{cy-r-25}" x2="{cx}" y2="{cy+r+25}" stroke="{INK}" stroke-width="3"/>'
         f'<text x="{cx+r+6}" y="{cy+22}" font-size="18" fill="{INK}" {FF}>1</text><text x="{cx+6}" y="{cy-r-6}" font-size="18" fill="{INK}" {FF}>1</text></g>')
    ids = [tag + "a"]
    cols = [RED, GREEN, BLUE, GOLD]
    for k, a in enumerate(angles_deg):
        t = math.radians(a); px, py = cx + r * math.cos(t), cy - r * math.sin(t); col = cols[k % 4]
        s += (f'<g id="{tag}p{k}"><line x1="{cx}" y1="{cy}" x2="{px:.1f}" y2="{py:.1f}" stroke="{col}" stroke-width="5"/>'
              f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{px:.1f}" y2="{cy}" stroke="{col}" stroke-width="3" stroke-dasharray="8 6"/>'
              f'<line x1="{px:.1f}" y1="{cy}" x2="{cx}" y2="{cy}" stroke="{col}" stroke-width="3" stroke-dasharray="8 6"/>'
              f'<circle cx="{px:.1f}" cy="{py:.1f}" r="9" fill="{col}"/><text x="{px+10:.1f}" y="{py-8:.1f}" font-size="18" font-weight="700" fill="{col}" {FF}>{a}°</text>'
              f'<text x="410" y="{60+k*44}" font-size="21" font-weight="700" fill="{col}" {FF}>{a}°: cos {math.cos(t):.2f}, sin {math.sin(t):.2f}</text></g>')
        ids.append(f"{tag}p{k}")
    return scene(s, ids)


def mapping(src, tgt, pairs, tag="MP", rule=None):
    """Arrow diagram from source set to target set. pairs: list of (src_value, tgt_value)."""
    ys = lambda n, i: 90 + (i + 0.5) * (300 / max(n, 1))
    s = (f'<g id="{tag}a"><ellipse cx="160" cy="240" rx="90" ry="170" fill="{BLUE}" fill-opacity=".18" stroke="{BLUE}" stroke-width="4"/>'
         f'<ellipse cx="500" cy="240" rx="90" ry="170" fill="{RED}" fill-opacity=".15" stroke="{RED}" stroke-width="4"/>'
         f'<text x="160" y="50" font-size="24" font-weight="700" text-anchor="middle" fill="{BLUE}" {FF}>Source</text><text x="500" y="50" font-size="24" font-weight="700" text-anchor="middle" fill="{RED}" {FF}>Target</text>')
    if rule: s += f'<text x="330" y="430" font-size="22" font-weight="700" text-anchor="middle" fill="{INK}" {FF}>{rule}</text>'
    for i, v in enumerate(src): s += f'<text x="160" y="{ys(len(src), i)+8:.1f}" font-size="26" font-weight="700" text-anchor="middle" fill="{INK}" {FF}>{v}</text>'
    for i, v in enumerate(tgt): s += f'<text x="500" y="{ys(len(tgt), i)+8:.1f}" font-size="26" font-weight="700" text-anchor="middle" fill="{INK}" {FF}>{v}</text>'
    s += '</g>'
    ids = [tag + "a"]
    for k, (a, b) in enumerate(pairs):
        y1 = ys(len(src), src.index(a)); y2 = ys(len(tgt), tgt.index(b))
        s += (f'<g id="{tag}r{k}"><line x1="200" y1="{y1:.1f}" x2="455" y2="{y2:.1f}" stroke="{GREEN}" stroke-width="5"/>'
              f'<polygon points="460,{y2:.1f} 440,{y2-9:.1f} 440,{y2+9:.1f}" fill="{GREEN}" transform="rotate(0)"/></g>')
        ids.append(f"{tag}r{k}")
    return scene(s, ids)


def cube(section=None, label_vertices=True, extra_lines=None, tag="CB", sec_color="#fb8c00", parallel=None):
    """Oblique cube ABCD (front) / EFGH (back). section: list of vertex names or (x,y) points to fill. extra_lines: [(P,Q,color)]."""
    s0, ox, oy, d = 210, 150, 330, 110
    P = {"A": (ox, oy), "B": (ox + s0, oy), "C": (ox + s0, oy - s0), "D": (ox, oy - s0)}
    for k, n in zip("ABCD", "EFGH"):
        P[n] = (P[k][0] + d, P[k][1] - d * 0.7)
    edges_vis = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("B", "F"), ("C", "G"), ("D", "H"), ("F", "G"), ("G", "H")]
    edges_hid = [("A", "E"), ("E", "F"), ("E", "H")]
    s = f'<g id="{tag}a">'
    if section:
        pts = " ".join(f"{(P[p] if isinstance(p, str) else p)[0]},{(P[p] if isinstance(p, str) else p)[1]}" for p in section)
        s += f'<polygon points="{pts}" fill="{sec_color}" fill-opacity=".35" stroke="{sec_color}" stroke-width="4"/>'
    for a, b in edges_hid:
        s += f'<line x1="{P[a][0]}" y1="{P[a][1]}" x2="{P[b][0]}" y2="{P[b][1]}" stroke="{INK}" stroke-width="3" stroke-dasharray="9 7"/>'
    for a, b in edges_vis:
        s += f'<line x1="{P[a][0]}" y1="{P[a][1]}" x2="{P[b][0]}" y2="{P[b][1]}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
    for a, b, col in (extra_lines or []):
        s += f'<line x1="{P[a][0]}" y1="{P[a][1]}" x2="{P[b][0]}" y2="{P[b][1]}" stroke="{col}" stroke-width="6" stroke-linecap="round"/>'
    if label_vertices:
        for n, (x, y) in P.items():
            dx = -22 if n in "ADE" else 10
            dy = 22 if n in "AB" else -10
            s += f'<text x="{x+dx}" y="{y+dy}" font-size="24" font-weight="700" fill="{BLUE}" {FF}>{n}</text>'
    s += '</g>'
    return scene(s, [tag + "a"])


def hops(start, steps, tag="HP", width=600):
    """Number-line hops: start value then labelled jumps (e.g. [100, 50, 2]); shows each intermediate value."""
    vals = [start]
    for d in steps: vals.append(vals[-1] + d)
    n = len(vals)
    X = lambda i: 70 + i * (width - 40) / max(n - 1, 1)
    y = 250
    s = f'<g id="{tag}a"><line x1="40" y1="{y}" x2="630" y2="{y}" stroke="{INK}" stroke-width="5"/></g>'
    ids = [tag + "a"]
    for i, v in enumerate(vals):
        s += (f'<g id="{tag}n{i}"><line x1="{X(i)}" y1="{y-12}" x2="{X(i)}" y2="{y+12}" stroke="{INK}" stroke-width="4"/>'
              f'<circle cx="{X(i)}" cy="{y}" r="9" fill="{GREEN if i==n-1 else (RED if i==0 else BLUE)}" stroke="{INK}" stroke-width="3"/>'
              f'<text x="{X(i)}" y="{y+52}" font-size="30" font-weight="700" text-anchor="middle" fill="{INK}" {FF}>{v}</text></g>')
        ids.append(f"{tag}n{i}")
        if i < len(steps):
            mid = (X(i) + X(i + 1)) / 2
            sign = "+" if steps[i] >= 0 else "−"
            s += (f'<g id="{tag}h{i}"><path d="M {X(i)} {y-14} Q {mid} {y-110} {X(i+1)} {y-14}" fill="none" stroke="{BLUE}" stroke-width="5"/>'
                  f'<text x="{mid}" y="{y-100}" font-size="30" font-weight="700" text-anchor="middle" fill="{BLUE}" {FF}>{sign}{abs(steps[i])}</text></g>')
            ids.append(f"{tag}h{i}")
    return scene(s, ids)


def blocks(h, t, o, tag="PV", label=True):
    """Place-value blocks: h hundred-squares, t ten-rods, o unit-dots."""
    s = ""; ids = []
    total = h * 100 + (12 if h and (t or o) else 0) + t * 30 + (14 if t and o else 0) + (72 if o else 0)
    x = max(10, (660 - total) / 2)
    for i in range(h):
        s += f'<g id="{tag}h{i}"><rect x="{x}" y="150" width="90" height="90" rx="6" fill="#bbdefb" stroke="{INK}" stroke-width="3"/>' + "".join(
            f'<line x1="{x+9*k}" y1="150" x2="{x+9*k}" y2="240" stroke="#90caf9" stroke-width="1.5"/><line x1="{x}" y1="{150+9*k}" x2="{x+90}" y2="{150+9*k}" stroke="#90caf9" stroke-width="1.5"/>' for k in range(1, 10)) + '</g>'
        ids.append(f"{tag}h{i}"); x += 100
    x += 12
    for i in range(t):
        s += f'<g id="{tag}t{i}"><rect x="{x}" y="150" width="22" height="90" rx="4" fill="#c8e6c9" stroke="{INK}" stroke-width="3"/>' + "".join(
            f'<line x1="{x}" y1="{150+9*k}" x2="{x+22}" y2="{150+9*k}" stroke="#81c784" stroke-width="1.5"/>' for k in range(1, 10)) + '</g>'
        ids.append(f"{tag}t{i}"); x += 30
    x += 14
    for i in range(o):
        s += f'<g id="{tag}o{i}"><rect x="{x+(i%3)*24}" y="{216-(i//3)*24}" width="20" height="20" rx="3" fill="#ffcdd2" stroke="{INK}" stroke-width="2.5"/></g>'
        ids.append(f"{tag}o{i}")
    if label:
        s += f'<g id="{tag}l"><text x="330" y="330" font-size="34" font-weight="700" text-anchor="middle" fill="{INK}" {FF}>{h} hundreds + {t} tens + {o} ones = {h*100+t*10+o}</text></g>'
        ids.append(tag + "l")
    return scene(s, ids)
