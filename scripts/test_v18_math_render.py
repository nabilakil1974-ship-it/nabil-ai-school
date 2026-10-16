"""Powers must render as real superscripts, never raw ^ or *, and stay LTR-isolated inside Arabic."""
from pathlib import Path
from tempfile import TemporaryDirectory
from playwright.sync_api import sync_playwright
from scripts.nabil_factory.cards.v18_board import render_v18_smart_board, build_golden_spec


def page_for(lang, text):
    acts = [{"concept_id": "C1", "title": "Powers", "lab_html": "", "allow_no_lab": True,
             "teaching_steps": [{"sentence": text, "label": "Rule", "kind": "step"},
                                {"sentence": "(a × b)^m = a^m × b^m", "kind": "step"}],
             "conclusion": "10^(4 * 2) = 10^8"}]
    spec = build_golden_spec("Q", acts, lang, subject="mathematics")
    return ("<html><head><meta charset='utf-8'></head><body>"
            + render_v18_smart_board("Q", acts, lang, golden_spec=spec) + "</body></html>")


def check(browser, tmp, lang, text):
    f = Path(tmp) / f"m_{lang}.html"
    f.write_text(page_for(lang, text), encoding="utf-8")
    page = browser.new_page(viewport={"width": 390, "height": 800})
    errs = []
    page.on("pageerror", lambda e: errs.append(str(e)))
    page.add_init_script("window.NABIL_V18_FAST=true")
    page.goto(f.as_uri())
    page.evaluate("void window.NABILWholeLessonOrchestrator.play()")
    page.wait_for_function("window.NABILWholeLessonOrchestrator.state().final===true", timeout=20000)
    res = page.evaluate("""()=>{const r=document.getElementById('nabilWholeLessonSmartLab');
      const vis=[...r.querySelectorAll('*')].filter(e=>e.checkVisibility&&e.checkVisibility()&&!e.closest('script'));
      const txt=vis.map(e=>[...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.nodeValue).join('')).join(' ');
      return {raw:/[\\^*]/.test(txt),sup:r.querySelectorAll('sup.nb-sup').length,bdi:r.querySelectorAll('bdi.nb-math').length,sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth}}""")
    page.close()
    assert not errs, errs
    assert not res["raw"], (lang, res)
    assert res["sup"] >= 4, (lang, res)
    assert res["sw"] <= res["cw"], (lang, res)
    return res


def main():
    with TemporaryDirectory() as tmp, sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        try:
            en = check(b, tmp, "en", "For (2^3)^4, apply 2^(3 * 4) = 2^12")
            ar = check(b, tmp, "ar", "نحسب (2^3)^4 باستخدام 2^(3 * 4) = 2^12 ثم نكمل")
            assert ar["bdi"] >= 2, ar
            print("PASS math render: real superscripts, no raw ^ or *, RTL isolation", en, ar)
        finally:
            b.close()


if __name__ == "__main__":
    main()
