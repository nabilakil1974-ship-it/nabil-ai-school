"""Convert an already-published 'Golden V6' scene lesson (NABIL_*.html) into smart-board data."""
import json, math, re
from pathlib import Path
from scripts.direct_lessons.draw import geo
import scripts.direct_lessons.lessons.g07_math_en_ch04 as G

INK = "#0b3d5c"
IMGS = {}
W, H = 660, 440


def rgba(c, a=0.14):
    c = c.lstrip("#")
    if len(c) == 3: c = "".join(x * 2 for x in c)
    r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    return f"rgba({r},{g},{b},{a})"


def load(path):
    s = Path(path).read_text(errors="ignore")
    return json.loads(re.search(r'<script id="nabilV6Data" type="application/json">(.*?)</script>', s, re.S).group(1))


AR_TITLES = {
    "intro": "مقدمة الفصل", "recall-1": "نشاط استذكاري 1: المثلث ABC", "recall-2": "نشاط استذكاري 2: عناصر المثلث",
    "recall-3": "نشاط استذكاري 3: أنواع المثلثات", "prep-1": "تحضير 1", "prep-2": "تحضير 2", "vocabulary": "المفردات",
    "equal-triangles": "المثلثان المتساويان", "asa": "الحالة: زاوية – ضلع – زاوية", "sas": "الحالة: ضلع – زاوية – ضلع",
    "sss": "الحالة: ضلع – ضلع – ضلع", "construct-asa": "إنشاء: زاوية – ضلع – زاوية", "construct-sas": "إنشاء: ضلع – زاوية – ضلع",
    "construct-sss": "إنشاء: ضلع – ضلع – ضلع", "angles": "حساب الزوايا", "proof-segments": "برهان تساوي قطعتين",
    "proof-angles": "برهان تساوي زاويتين", "focus": "تركيز",
}


def ar_title(sid):
    k = sid.split("-", 2)[2] if sid.count("-") >= 2 else sid
    if k in AR_TITLES: return AR_TITLES[k]
    m = re.match(r"ex(\d+)", k)
    if m: return f"التمرين {m.group(1)}"
    m = re.match(r"selfA(\d)", k)
    if m: return f"التقويم الذاتي A{m.group(1)}"
    m = re.match(r"problem(\d)", k)
    if m: return f"المسألة {m.group(1)}"
    if k.startswith("V60-GOLDEN") or k == "V60-GOLDEN": return "البطاقة الذهبية: الخلاصة"
    m = re.match(r"V60-(\d+)", k)
    if m: return f"تدريب إضافي {int(m.group(1))}"
    return k


class Fig:
    def __init__(self):
        self.pts = {}      # name -> screen xy
        self.T = lambda u: u
        self.groups = []   # (group, temp)

    def reset(self):
        self.groups = []


def _fit(units, extra=0.0, margin=46):
    xs = [p[0] for p in units]; ys = [p[1] for p in units]
    x0, x1, y0, y1 = min(xs) - extra, max(xs) + extra, min(ys) - extra, max(ys) + extra
    w, h = max(x1 - x0, 1e-6), max(y1 - y0, 1e-6)
    sc = min((W - 2 * margin) / w, (H - 2 * margin) / h)
    ox = (W - sc * w) / 2 - sc * x0; oy = (H - sc * h) / 2 + sc * y1
    return lambda u: (ox + sc * u[0], oy - sc * u[1]), sc


def _label(p, name, cen, col=INK):
    dx, dy = p[0] - cen[0], p[1] - cen[1]; L = math.hypot(dx, dy) or 1
    return ("pt", p, name, dx / L * 24, dy / L * 24 + 9, col)


def _outward(a, b, cen, d):
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    nx, ny = -(b[1] - a[1]), b[0] - a[0]; L = math.hypot(nx, ny) or 1; nx, ny = nx / L, ny / L
    if (mx - cen[0]) * nx + (my - cen[1]) * ny < 0: nx, ny = -nx, -ny
    return (mx + nx * d, my + ny * d)


def base_points(fig, points, segments, T):
    fig.pts = {k: T(v) for k, v in points.items()}
    cen = (sum(p[0] for p in fig.pts.values()) / len(fig.pts), sum(p[1] for p in fig.pts.values()) / len(fig.pts))
    segs = [("seg", fig.pts[a], fig.pts[b], INK, 4, None) for a, b in [s[:2] for s in segments] if a in fig.pts and b in fig.pts]
    pts = [_label(p, n, cen) for n, p in fig.pts.items() if re.fullmatch(r"[A-Z]", n)]
    return segs, pts


def step_fig2(fig, a):
    T, _ = _fit(list(a["points"].values()), 0.5)
    segs, pts = base_points(fig, a["points"], a["segments"], T)
    fig.T = T; fig.reset(); return [segs, pts]


def step_construct(fig, a, keep):
    T, sc = _fit(list(a["points"].values()), a.get("extra", 0.8))
    fig.T = T; fig.pts = {k: T(v) for k, v in a["points"].items()}
    cen = (sum(p[0] for p in fig.pts.values()) / len(fig.pts), sum(p[1] for p in fig.pts.values()) / len(fig.pts))
    if not keep: fig.reset()
    out = []
    for o in a.get("ops", []):
        op = o["op"]
        if op == "ruler":
            pa, pb = fig.pts[o["a"]], fig.pts[o["b"]]
            g = [("seg", pa, pb, INK, 4, None)]
            if o.get("label"): g.append(("text", _outward(pa, pb, cen, 24), o["label"], 22, "#1e88e5"))
            out.append(g)
        elif op == "protractor":
            v, f, t = fig.pts[o["at"]], fig.pts[o["from"]], fig.pts[o["to"]]
            tt = (v[0] + (t[0] - v[0]) * 1.1, v[1] + (t[1] - v[1]) * 1.1)
            g = [("seg", v, tt, INK, 3, "7 5"), ("arc", v, f, t, 34, 1, "#e53935")]
            bis = ((f[0] - v[0]) / (math.hypot(f[0] - v[0], f[1] - v[1]) or 1) + (t[0] - v[0]) / (math.hypot(t[0] - v[0], t[1] - v[1]) or 1),
                   (f[1] - v[1]) / (math.hypot(f[0] - v[0], f[1] - v[1]) or 1) + (t[1] - v[1]) / (math.hypot(t[0] - v[0], t[1] - v[1]) or 1))
            bl = math.hypot(*bis) or 1
            g.append(("text", (v[0] + bis[0] / bl * 62, v[1] + bis[1] / bl * 62 + 8), f"{o['deg']}°", 22, "#e53935"))
            out.append(g)
        elif op == "arc":
            c = fig.pts[o["center"]]; r = o["r"] * sc
            out.append([("carc", c, r, -o["a0"], -o["a1"], "#2e7d32", "6 5")])
        elif op == "mark":
            out.append([_label(fig.pts[o["p"]], o["p"], cen)])
        elif op == "perp":
            pass
    return out


def step_source(fig, a, figs):
    f = figs[a["key"]]; iw, ih = f["width"], f["height"]
    sc = min((W - 20) / iw, (H - 20) / ih); w, h = iw * sc, ih * sc; x0, y0 = (W - w) / 2, (H - h) / 2
    fig.T = lambda u: (x0 + u[0] * w, y0 + u[1] * h)
    fig.pts = {k: fig.T(v) for k, v in (a.get("points") or {}).items()}
    fig.reset()
    IMGS[a["key"]] = f'data:{f["mime"]};base64,{f["base64"]}'
    img = f'<image href="@@IMG:{a["key"]}@@" x="{x0:.1f}" y="{y0:.1f}" width="{w:.1f}" height="{h:.1f}"/>'
    return [[("raw", img)]]


def _pt(fig, v):
    if isinstance(v, str): return fig.pts.get(v)
    return fig.T(v)


def step_annot(fig, items):
    out = []
    for it in items:
        k = it["kind"]; c = it.get("c", "#e8590c"); g = None
        try:
            if k == "poly":
                P = [fig.pts[n] for n in it["pts"]]; g = [("poly", P, rgba(c), c, 5)]
            elif k == "seg":
                g = [("seg", fig.pts[it["a"]], fig.pts[it["b"]], c, 7, None)]
            elif k == "ring":
                p = fig.pts[it["p"]]; g = [("carc", p, 24, 0, 179.9, c, None), ("carc", p, 24, 180, 359.9, c, None)]
            elif k == "equal":
                g = [("tick", fig.pts[a], fig.pts[b], it.get("n", 1), c) for a, b in it["segs"]]
            elif k == "right":
                g = [("right", fig.pts[it["at"]], fig.pts[it["u"]], fig.pts[it["v"]], 18, c)]
            elif k == "arc":
                v, f, t = fig.pts[it["at"]], fig.pts[it["from"]], fig.pts[it["to"]]
                r = max(20, min(40, it.get("r", 30) * 0.8))
                g = [("arc", v, f, t, r, it.get("n", 1), c)]
                if it.get("text"):
                    u1 = ((f[0] - v[0]), (f[1] - v[1])); u2 = ((t[0] - v[0]), (t[1] - v[1]))
                    l1 = math.hypot(*u1) or 1; l2 = math.hypot(*u2) or 1
                    bx, by = u1[0] / l1 + u2[0] / l2, u1[1] / l1 + u2[1] / l2; bl = math.hypot(bx, by) or 1
                    g.append(("text", (v[0] + bx / bl * (r + 24), v[1] + by / bl * (r + 24) + 8), it["text"], 22, c))
            elif k == "label":
                g = [("text", _pt(fig, it["p"]), it["text"], 24, c)]
        except (KeyError, TypeError):
            g = None
        if g: out.append((g, bool(it.get("temp"))))
    return out


def stock(case_fn):
    sc = case_fn()
    return sc["args"]


def tri_el(kind):
    A, B, C = (330, 60), (130, 360), (540, 360)
    M = ((B[0] + C[0]) / 2, 360)
    base = [("poly", [A, B, C], "rgba(30,136,229,.08)", INK, 5), ("pt", A, "A", 0, -16, INK), ("pt", B, "B", -22, 12, INK), ("pt", C, "C", 22, 12, INK)]
    if kind == "median":
        return [base, [("seg", A, M, "#fb8c00", 5, None), ("pt", M, "M", 0, 34, INK), ("tick", B, M, 1, "#2e7d32"), ("tick", M, C, 1, "#2e7d32")]]
    if kind == "perp":
        top = (M[0], 40)
        return [base, [("seg", top, (M[0], 395), "#fb8c00", 5, None), ("pt", M, "M", 18, 34, INK), ("tick", B, M, 1, "#2e7d32"), ("tick", M, C, 1, "#2e7d32"), ("right", M, B, top, 18, "#e53935")]]
    if kind == "height":
        H_ = (A[0], 360)
        return [base, [("seg", A, H_, "#fb8c00", 5, None), ("pt", H_, "H", 0, 34, INK), ("right", H_, B, A, 18, "#e53935")]]
    D = (B[0] + (C[0] - B[0]) * 0.42, 360)
    return [base, [("seg", A, D, "#fb8c00", 5, None), ("pt", D, "D", 0, 34, INK), ("arc", A, B, D, 36, 1, "#e53935"), ("arc", A, D, C, 36, 1, "#e53935")]]


def tri_types():
    iso = [(120, 340), (240, 340), (180, 160)]
    eq = [(290, 340), (410, 340), (350, 236)]
    rt = [(470, 340), (600, 340), (470, 190)]
    return [[("poly", iso, "rgba(30,136,229,.1)", INK, 4), ("tick", iso[0], iso[2], 1, "#2e7d32"), ("tick", iso[1], iso[2], 1, "#2e7d32"), ("text", (180, 385), "Isosceles", 22, INK)],
            [("poly", eq, "rgba(46,125,50,.1)", INK, 4), ("tick", eq[0], eq[1], 1, "#2e7d32"), ("tick", eq[1], eq[2], 1, "#2e7d32"), ("tick", eq[0], eq[2], 1, "#2e7d32"), ("text", (350, 385), "Equilateral", 22, INK)],
            [("poly", rt, "rgba(229,57,53,.1)", INK, 4), ("right", rt[0], rt[1], rt[2], 18, "#e53935"), ("text", (535, 385), "Right", 22, INK)]]


def construct_tools(kind, stage):
    A, B = (120, 340), (320, 340)
    if kind == "asa":
        C = (A[0] + 100, 340 - 110)
        st = {"ab": [[("seg", A, B, INK, 4, None), ("pt", A, "A", -20, 10, INK), ("pt", B, "B", 20, 10, INK)]],
              "angleA": [[("seg", A, (A[0] + 250, A[1] - 150), INK, 3, "7 5"), ("arc", A, B, (A[0] + 250, A[1] - 150), 44, 1, "#e53935")]],
              "angleB": [[("seg", B, (B[0] - 230, B[1] - 200), INK, 3, "7 5"), ("arc", B, (B[0] - 230, B[1] - 200), A, 40, 1, "#e53935")]],
              "meet": [[("seg", A, C, INK, 4, None), ("seg", B, C, INK, 4, None), ("pt", C, "C", 0, -16, INK)]]}
    else:
        C = (A[0] + 40, 340 - 180)
        st = {"ab": [[("seg", A, B, INK, 4, None), ("pt", A, "A", -20, 10, INK), ("pt", B, "B", 20, 10, INK)]],
              "arcA": [[("carc", A, 180, -80, -45, "#2e7d32", "6 5")]],
              "arcB": [[("carc", B, 250, -150, -125, "#2e7d32", "6 5")]],
              "meet": [[("seg", A, C, INK, 4, None), ("seg", B, C, INK, 4, None), ("pt", C, "C", 0, -16, INK)]]}
    return st[stage]


def two_tri(a):
    ps = a["t1"] + a["t2"]; T, _ = _fit([(p[0], -p[1]) for p in ps], 0, 50)
    mk = lambda t: [T((p[0], -p[1])) for p in t]
    t1, t2 = mk(a["t1"]), mk(a["t2"])
    return [[("poly", t1, "rgba(30,136,229,.1)", INK, 4)], [("poly", t2, "rgba(251,140,0,.12)", INK, 4)]]


def locus(a):
    P = a["primitives"]; xs = [q for p in P for q in ([p["a"][0], p["b"][0]] if "a" in p else [p["at"][0]])]
    ys = [q for p in P for q in ([p["a"][1], p["b"][1]] if "a" in p else [p["at"][1]])]
    T, _ = _fit([(min(xs), -max(ys)), (max(xs), -min(ys))], 0, 60); f = lambda q: T((q[0], -q[1]))
    g1 = [("seg", f(p["a"]), f(p["b"]), p.get("color", INK), 5, None) for p in P if p["kind"] == "line"]
    g2 = [("pt", f(p["at"]), p["label"], 0, -14, INK) for p in P if p["kind"] == "point"]
    return [g1, g2]


def convert(path):
    IMGS.clear(); d = load(path); figs = d["source_figures"]; pages = []
    for sc in d["scenes"]:
        fig = Fig(); items = []
        titles = {"en": sc["title"], "fr": sc.get("title_fr") or sc["title"], "ar": ar_title(sc["id"])}
        pending_groups = []

        def emit(newgroups, tagi, base_reset=False):
            nonlocal items
            if not newgroups: return
            fig.groups = [(g, t) for g, t in fig.groups if not t] if not base_reset else []
            for g, t in newgroups: fig.groups.append((g, t))
            sceneobj = geo([g for g, _ in fig.groups], f"S{tagi}_")
            a = sceneobj["args"]; n = len(newgroups)
            a["show"] = a["show"][-n:]
            items.append({"k": "d", "svg": a["svg"], "vb": [W, H], "show": a["show"]})

        for si, st in enumerate(sc["steps"]):
            t = st["t"]
            if t == "text":
                items.append({"k": "t", "ar": st["text"], "en": st.get("en") or st["text"], "fr": st.get("fr") or st.get("en") or st["text"], "label": ""})
            elif t == "formula":
                items.append({"k": "f", "f": st["text"]})
            elif t == "draw":
                sp = st.get("speech")
                if sp:
                    items.append({"k": "t", "ar": sp, "en": st.get("speech_en") or sp, "fr": st.get("speech_fr") or st.get("speech_en") or sp, "label": ""})
                k = st["draw"]; a = st.get("args", {}); tag = f"{sc['id'][-6:]}{si}".replace("-", "")
                if k == "fig2":
                    emit([(g, False) for g in step_fig2(fig, a)], tag, True)
                elif k == "sourceFigure":
                    emit([(g, False) for g in step_source(fig, a, figs)], tag, True)
                elif k == "construct":
                    keep = bool(a.get("keep"))
                    gs = step_construct(fig, a, keep); emit([(g, False) for g in gs], tag, not keep)
                elif k == "annotate":
                    emit(step_annot(fig, a.get("items", [])), tag)
                elif k == "congruenceCases":
                    fn = {"ASA": G.d_asa, "SAS": G.d_sas, "SSS": G.d_sss}[a["case"]]
                    sc_ = fn()["args"]; items.append({"k": "d", "svg": sc_["svg"], "vb": [660, 440], "show": sc_["show"]})
                    fig.pts = {}; fig.groups = []
                elif k == "verifiedConstruction":
                    fn = {"asa": G.d_asa, "sas": G.d_sas, "sss": G.d_sss}[a["kind"]]
                    sc_ = fn()["args"]; items.append({"k": "d", "svg": sc_["svg"], "vb": [660, 440], "show": sc_["show"]})
                elif k == "triEl":
                    emit([(g, False) for g in tri_el(a["kind"])], tag, True)
                elif k == "triangleTypes":
                    emit([(g, False) for g in tri_types()][:1 if si == 0 else 3] if False else [(g, False) for g in tri_types()], tag, True)
                elif k == "constructTools":
                    emit([(g, False) for g in construct_tools(a["kind"], a["stage"])], tag, a["stage"] == "ab")
                elif k == "twoTri":
                    emit([(g, False) for g in two_tri(a)], tag, True)
                elif k == "locusSketch":
                    emit([(g, False) for g in locus(a)], tag, True)
        pages.append({"title": titles, "items": items})
    pages = [p for p in pages if p["items"]]
    t = d["titles"]
    return {"title": {"en": t["en"], "ar": t["ar"], "fr": t["fr"]}, "lang": "ar", "pages": pages, "imgs": dict(IMGS)}


class Mod:
    def __init__(self, path):
        self.BOARD_DATA = convert(path); self.TITLES = self.BOARD_DATA["title"]


if __name__ == "__main__":
    import sys
    from scripts.direct_lessons import smartboard
    m = Mod(sys.argv[1]); out = Path(sys.argv[2]); out.write_text(smartboard.render(m), encoding="utf-8"); print(out, out.stat().st_size, len(m.BOARD_DATA["pages"]))
