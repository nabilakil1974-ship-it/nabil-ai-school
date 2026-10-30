"""Render any lesson module as a NABIL AI Smart Board page (single self-contained HTML)."""
import json
from pathlib import Path

A = Path(__file__).parent / "sb_assets"


def _items(steps):
    out = []
    for s in steps:
        if s["k"] == "t":
            out.append({"k": "t", "en": s["en"], "ar": s["ar"], "fr": s["fr"], "label": s.get("label") or ""})
        elif s["k"] == "f":
            out.append({"k": "f", "f": s["f"]})
        elif s["k"] == "d" and s["draw"] == "svgScene":
            a = s["args"]
            out.append({"k": "d", "svg": a["svg"], "vb": a.get("vb", [660, 440]), "show": a.get("show", [])})
    return out


def data(m, lang="ar"):
    pages = []
    for te, ta, tf, page, steps in m.THEORY:
        pages.append({"title": {"en": te, "ar": ta, "fr": tf}, "items": _items(steps)})
    for e in m.EXERCISES:
        en, ar, fr = e["stmt"]
        head = [{"k": "t", "en": en, "ar": ar, "fr": fr, "label": "Problem"}]
        pages.append({"title": {"en": f"Exercise {e['n']}", "ar": f"التمرين {e['n']}", "fr": f"Exercice {e['n']}"},
                      "items": head + _items(e["steps"])})
    pages = [p for p in pages if p["items"]]
    return {"title": m.TITLES, "lang": lang, "pages": pages}


def _photo():
    import base64
    return "data:image/jpeg;base64," + base64.b64encode((A / "ustaz.jpg").read_bytes()).decode()


def render(m, lang="ar"):
    html = (A / "template.html").read_text(encoding="utf-8")
    css = (A / "base.css").read_text() + (A / "extra.css").read_text()
    js = json.dumps(data(m, lang), ensure_ascii=False).replace("</", "<\\/")
    return (html.replace("%%CSS%%", css).replace("%%TEACHER%%", (A / "teacher.js").read_text())
            .replace("%%INK%%", (A / "ink.js").read_text()).replace("%%DATA%%", js).replace("%%PHOTO%%", _photo())
            .replace("%%TITLE%%", m.TITLES["en"]))


if __name__ == "__main__":
    import importlib, sys
    import importlib.util
    mod = importlib.import_module("scripts.direct_lessons.lessons." + sys.argv[1])
    up = "scripts.direct_lessons.upgrades." + sys.argv[1]
    if importlib.util.find_spec(up):
        importlib.import_module(up).upgrade(mod)
    out = Path(sys.argv[2]); out.write_text(render(mod), encoding="utf-8"); print(out, out.stat().st_size)
