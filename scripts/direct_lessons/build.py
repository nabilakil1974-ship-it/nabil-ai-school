"""Render a direct-lesson module to a standalone HTML page (no AI calls)."""
import importlib, sys, time
from pathlib import Path
from scripts.nabil_factory.cards import golden_v6 as g6


def build(module: str, out: str, lang: str = "en") -> Path:
    m = importlib.import_module(module)
    t0 = time.time()
    body = g6.render_golden_v6_board(
        m.TITLES["en"], m.scenes(), lang, golden_spec=m.GOLDEN, titles=m.TITLES,
        meta={"lesson_id": m.LESSON_ID, "grade": "7", "subject": "mathematics", "language": lang})
    html = (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{m.TITLES["en"]}</title></head><body style="margin:0">{body}</body></html>')
    p = Path(out); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(html, encoding="utf-8")
    print("built", p, len(html), "bytes in %.1fs" % (time.time() - t0))
    return p


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "en")
