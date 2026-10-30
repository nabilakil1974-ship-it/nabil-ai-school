"""Build every direct lesson module into standalone pages + catalog.json.

usage: python -m scripts.direct_lessons.build_all OUT_DIR
A module needs: LESSON_ID, TITLES{en,ar,fr}, GRADE(int), SUBJECT('math'|'physics'|'chem'|'bio'),
THEORY, EXERCISES (see common.py); optional GOLDEN, LANG ('en' default).
"""
import importlib, importlib.util, json, os, pkgutil, re, sys, traceback
from pathlib import Path
from scripts.nabil_factory.cards import golden_v6 as g6
from scripts.direct_lessons.common import make_scenes
from scripts.direct_lessons.engage import layer
import scripts.direct_lessons.lessons as pkg

POWERS = "scripts.direct_lessons.g07_powers"


def default_golden(m):
    items = []
    for sc in m.THEORY[-1:]:
        for s in sc[-1]:
            if s["k"] == "f":
                items.append(s["f"])
    items = items[:6] or [m.TITLES["en"]]
    return {"kind": "mathematics", "subject": "mathematics", "language": "en", "title": m.TITLES["en"],
            "sections": [{"label": "Results:", "items": items}], "key_results": items[:3],
            "verification": ["checked"], "panels": [{"title": m.TITLES["en"], "icon": "✅", "steps": items}],
            "rule_summary": items[0], "concept_ids": ["x"], "avatar_src": ""}


def page(m, lang="en"):
    scenes = m.scenes() if hasattr(m, "scenes") else make_scenes(m.THEORY, m.EXERCISES)
    golden = getattr(m, "GOLDEN", None) or default_golden(m)
    body = g6.render_golden_v6_board(m.TITLES["en"], scenes, getattr(m, "LANG", lang), golden_spec=golden,
                                     titles=m.TITLES, meta={"lesson_id": m.LESSON_ID, "grade": str(getattr(m, "GRADE", "")),
                                                            "subject": "mathematics", "language": "en"})
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{m.TITLES["en"]}</title></head><body style="margin:0">{body}{layer(m)}</body></html>')


def main(out):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    mods = [POWERS] + [f"scripts.direct_lessons.lessons.{n.name}" for n in pkgutil.iter_modules(pkg.__path__)]
    cat, bad = [], []
    for name in mods:
        try:
            if os.environ.get("ONLY") and not re.search(os.environ["ONLY"], name):
                continue
            m = importlib.import_module(name)
            up = f"scripts.direct_lessons.upgrades.{name.rsplit('.', 1)[-1]}"
            if importlib.util.find_spec(up):
                importlib.import_module(up).upgrade(m)  # enrich: extra graphs, explanations, exercises
            html = page(m)
            fn = f"{m.LESSON_ID.lower()}.html"
            (out / fn).write_text(html, encoding="utf-8")
            cat.append({"g": int(getattr(m, "GRADE", 7)), "s": getattr(m, "SUBJECT", "math"),
                        "t": f'{m.TITLES["ar"]} — {m.TITLES["en"]}', "id": m.LESSON_ID, "u": f"/static/lessons/{fn}"})
        except Exception as e:
            bad.append((name, repr(e)[:200])); traceback.print_exc()
    if not os.environ.get("ONLY"):
        (out / "catalog.json").write_text(json.dumps(cat, ensure_ascii=False), encoding="utf-8")
    print("built", len(cat), "failed", len(bad))
    for b in bad: print("FAIL", b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
