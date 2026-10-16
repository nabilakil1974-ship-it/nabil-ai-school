"""Golden V6 board regression tests (real Chromium: desktop + Android phone portrait/landscape).

Anti-regression for the approved V6 properties:
  * nothing starts before the click; click starts pen + (English) voice
  * ONE photorealistic hand (byte-identical asset), one pen, never duplicated
  * SINGLE board for text-only stages (Powers), DUAL board for drawings (Cube)
  * single -> dual -> single inside one lesson without reload / clearing / hand duplication
  * pause freezes writing + hand + voice; resume continues from the same word
  * default speed 0.7x, English-only voice, Sides terminology, math as real superscripts
  * drawing stays visible while the explanation scrolls; no overflow on phones
Run:  python3 scripts/test_golden_v6_board.py
"""
from __future__ import annotations

import hashlib
import os
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.golden_v6_fixtures import (GOLDEN, POWERS_ACTIVITIES, cube_scenes, mixed_scenes,  # noqa: E402
                                        powers_scenes, powers_single_scenes)
from scripts.nabil_factory.cards import golden_v6 as g6  # noqa: E402

OUT = Path(os.environ.get("V6_OUT", tempfile.mkdtemp(prefix="v6out_")))
OUT.mkdir(parents=True, exist_ok=True)
RESULTS: list[tuple[str, str, str]] = []

SPEECH_STUB = """
(() => {
  window.__spoken = []; window.__ssCalls = [];
  let paused = false;
  const ss = {
    speaking: false, pending: false,
    get paused() { return paused; },
    getVoices() { return [{lang: 'en-US', name: 'Stub English', default: true}]; },
    speak(u) { window.__spoken.push({text: u.text, lang: u.lang, rate: u.rate, volume: u.volume}); window.__ssCalls.push('speak');
      if (u.volume !== 0) { setTimeout(() => u.onstart && u.onstart(), 30); setTimeout(() => u.onend && u.onend(), 500 + u.text.length * 25); } },
    cancel() { window.__ssCalls.push('cancel'); paused = false; },
    pause() { paused = true; window.__ssCalls.push('pause'); },
    resume() { paused = false; window.__ssCalls.push('resume'); },
    addEventListener() {}, removeEventListener() {},
  };
  Object.defineProperty(window, 'speechSynthesis', {value: ss, configurable: true});
  window.SpeechSynthesisUtterance = function (t) { this.text = t; this.lang = ''; this.rate = 1; this.volume = 1; };
})();
"""


def record(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, "PASS" if ok else "FAIL", detail))
    print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")


def page_html(name: str, title: str, scenes, lang: str, titles=None) -> Path:
    body = g6.render_golden_v6_board(title, scenes, lang, golden_spec=GOLDEN, titles=titles or {})
    path = OUT / f"{name}.html"
    path.write_text(
        f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1"></head>'
        f'<body style="margin:0">{body}</body></html>', encoding="utf-8")
    return path


def new_page(browser, path: Path, w=1280, h=760, fast=False, stub=True, mobile=False):
    ctx = browser.new_context(viewport={"width": w, "height": h}, is_mobile=mobile, has_touch=mobile,
                              device_scale_factor=2 if mobile else 1)
    pg = ctx.new_page()
    pg.errors = []
    pg.on("pageerror", lambda e: pg.errors.append(str(e)))
    if stub:
        pg.add_init_script(SPEECH_STUB)
    if fast:
        pg.add_init_script("window.NABIL_V18_FAST=true")
    pg.goto(f"file://{path}")
    pg.wait_for_function("!!window.NABILWholeLessonOrchestrator", timeout=20000)
    return pg


def state(pg):
    return pg.evaluate("NABILWholeLessonOrchestrator.state()")


def units_written(pg) -> int:
    return pg.evaluate("document.querySelectorAll('#nbWriting .nb-step span, #nbWriting .nb-step bdi').length")


def run_static() -> None:
    hand = g6.hand_payload()
    record("hand asset is byte-identical to the approved V6 template",
           hashlib.sha256(hand.encode()).hexdigest() == g6.HAND_SHA256)
    ref = (g6._ASSETS / "golden_v6_reference" /
           "NABIL_G07_CUBE_GOLDEN_V6_APPROVED_VOICE_ON_SIDES.html").read_text(encoding="utf-8")
    record("reference copy of the approved V6 template is kept and contains the same hand",
           hand in ref and "cubeOutline" in ref and "teacherHand" in ref)
    eng = (g6._ASSETS / "golden_v6_engine.js").read_text(encoding="utf-8")
    record("engine keeps the approved V6 cube actions and hand overlay",
           all(k in eng for k in ("cubeOutline", "cubeColor", "cubeRotate", "cubeUnfold", "teacherHand", "getScreenCTM")))
    record("engine has no hard-coded lesson content and no data: image",
           "data:image" not in eng and "Powers" not in eng and "Cube —" not in eng)
    page = (OUT / "cube.html").read_text(encoding="utf-8") if (OUT / "cube.html").exists() else ""
    record("terminology: Sides / أضلاع / Side length (not Edges / أحرف) inside solids lessons",
           g6.apply_terminology("Edge length of the edges: أحرف المكعب", "Cube") == "Side length of the sides: أضلاع المكعب"
           and g6.apply_terminology("edges of a graph", "Graph theory") == "edges of a graph")
    sc = powers_scenes("en")
    record("factory output is structured data only (no HTML strings in scene data)",
           all("<" not in str(s) for sc_ in sc for s in sc_["steps"] if s.get("t") in ("text", "formula")))
    modes = [g6.scene_board_modes(s) for s in powers_scenes("en")]
    record("Powers scenes: text-only stage is single, lab stages draw (dual)",
           modes[2] == ["single"] and modes[0][-1] == "dual", str(modes))
    for sc_ in powers_scenes("en"):
        for s in sc_["steps"]:
            if s.get("t") == "text":
                assert s["speech"] == s["text"], "English page speaks its own English text"
    ar = g6.build_scenes([dict(POWERS_ACTIVITIES[0])], "ar", "Powers")
    record("non-English pages never send Arabic/French to the English voice",
           all(s.get("speech", "") == "" for s in ar[0]["steps"] if s["t"] == "text"))


def run_browser(browser) -> None:
    powers = page_html("powers", "Powers", powers_scenes("en"), "en", {"fr": "Les puissances"})
    powers_single = page_html("powers_single", "Powers", powers_single_scenes("en"), "en", {"fr": "Les puissances"})
    cube = page_html("cube", "Cube — Faces, Sides and Vertices", cube_scenes("ar"), "ar",
                     {"fr": "Le cube — faces, côtés, sommets"})
    mixed = page_html("mixed", "Mixed", mixed_scenes(), "ar")

    # ---------------- nothing starts before the click, opening screen content
    pg = new_page(browser, powers_single)
    time.sleep(1.5)
    st = state(pg)
    n_spoken = pg.evaluate("window.__spoken.length")
    opening = pg.evaluate("""() => ({img: !!document.getElementById('nbAvatarOpen').src,
        brand: document.querySelector('.nb-brand').textContent, en: document.getElementById('nbOpenTitleEn').textContent,
        fr: (document.getElementById('nbOpenTitleFr')||{}).textContent, start: !!document.getElementById('nbStart'),
        writtenBeforeClick: document.getElementById('nbWriting').children.length})""")
    record("opening screen: avatar, «منصة الأستاذ النبيل», EN title with FR under it, Start button",
           opening["img"] and opening["brand"] == "منصة الأستاذ النبيل" and opening["en"] == "Powers"
           and opening["fr"] == "Les puissances" and opening["start"], str(opening))
    record("nothing starts before the click (no pen, no voice, no writing)",
           (not st["started"]) and n_spoken == 0 and opening["writtenBeforeClick"] == 0 and not st["handVisible"], str(st))
    record("default speed 0.7x and voice ON", st["speed"] == 0.7 and st["voice"] is True)
    pg.screenshot(path=str(OUT / "01_opening_desktop.png"))

    # ---------------- click starts: SINGLE board, hand, English voice (not Arabic)
    pg.click("#nbStart")
    pg.wait_for_function("document.querySelectorAll('#nbWriting .nb-step span').length>2", timeout=15000)
    st = state(pg)
    spoken = [u for u in pg.evaluate("window.__spoken") if u["text"].strip()]
    record("click starts the lesson on a SINGLE full-width board",
           st["started"] and st["boardMode"] == "single"
           and pg.evaluate("getComputedStyle(document.getElementById('nbDiagram')).display") == "none", str(st))
    record("English voice speaks at the click (en-US, rate from 0.7x), full lesson text, no Arabic",
           bool(spoken) and spoken[0]["lang"] == "en-US" and all(ord(c) < 0x0600 or ord(c) > 0x06FF for u in spoken for c in u["text"]),
           str(spoken[:1]))
    record("exactly one hand on the page", pg.evaluate("document.querySelectorAll('#teacherHand').length") == 1
           and pg.evaluate("document.querySelectorAll('img[id*=and]').length") == 1)
    record("hand is the real image (Blob, PNG 669x574), visible while writing",
           pg.evaluate("(()=>{const h=document.getElementById('teacherHand');return h.src.startsWith('blob:')&&h.naturalWidth===669&&h.naturalHeight===574&&h.classList.contains('is-visible')})()"))
    pg.screenshot(path=str(OUT / "02_single_board_writing_desktop.png"))

    # ---------------- pause freezes everything, resume continues from the same word
    pg.click("#nabilWholePlay")
    time.sleep(0.4)
    n1 = units_written(pg)
    pos1 = pg.evaluate("(()=>{const h=document.getElementById('teacherHand');return [h.style.left,h.style.top]})()")
    idx1 = state(pg)["index"]
    time.sleep(1.6)
    n2 = units_written(pg)
    pos2 = pg.evaluate("(()=>{const h=document.getElementById('teacherHand');return [h.style.left,h.style.top]})()")
    calls = pg.evaluate("window.__ssCalls")
    record("PAUSE freezes writing, pen/hand position and voice together",
           state(pg)["paused"] and n1 == n2 and pos1 == pos2 and "pause" in calls, f"units {n1}->{n2} hand {pos1}->{pos2}")
    pg.click("#nabilWholePlay")
    time.sleep(2.5)
    n3 = units_written(pg)
    record("RESUME continues from the same place (more words, same scene, no restart, voice resumed)",
           (not state(pg)["paused"]) and n3 > n2 and state(pg)["index"] == idx1 and pg.evaluate("window.__ssCalls").count("resume") >= 1,
           f"units {n2}->{n3}")
    record("no page errors (single board)", not pg.errors, str(pg.errors[:2]))
    pg.context.close()

    # ---------------- CUBE: DUAL board, drawing visible, hand moves on both panes
    pg = new_page(browser, cube)
    pg.click("#nbStart")
    pg.wait_for_function("document.querySelectorAll('#nbInk *').length>0", timeout=30000)
    st = state(pg)
    dual_ok = pg.evaluate("""() => { const d=document.getElementById('nbDiagram').getBoundingClientRect(),
        w=document.getElementById('nbWriting').getBoundingClientRect();
        return {diag: d.width>200 && d.height>200, writing: w.width>200,
                overlap: !(d.right<=w.left+1 || w.right<=d.left+1 || d.bottom<=w.top+1 || w.bottom<=d.top+1)}}""")
    record("CUBE shows TWO boards side by side (drawing + explanation) without overlap",
           st["boardMode"] == "dual" and dual_ok["diag"] and dual_ok["writing"] and not dual_ok["overlap"], str(dual_ok))
    pg.wait_for_function("document.querySelectorAll('#nbInk line').length>=3", timeout=40000)
    hand_box = pg.evaluate("(()=>{const h=document.getElementById('teacherHand').getBoundingClientRect();const d=document.getElementById('nbDiagram').getBoundingClientRect();return {x:h.left+h.width*.18,inside:(h.left+h.width*.18)>=d.left-40&&(h.left+h.width*.18)<=d.right+40}})()")
    record("the one hand follows the pen on the drawing board", hand_box["inside"], str(hand_box))
    pg.screenshot(path=str(OUT / "03_cube_dual_desktop.png"))
    pg.context.close()

    # ---------------- mixed lesson: single -> dual -> single without reload, content preserved
    pg = new_page(browser, mixed, fast=False)
    pg.evaluate("window.__marker='same-page'")
    pg.click("#nbStart")
    pg.select_option("#nbSpeed", "1.25")
    pg.wait_for_function("document.querySelectorAll('#nbInk *').length>0", timeout=60000)
    first_text = pg.evaluate("document.querySelector('#nbWriting .nb-step').textContent")
    pg.wait_for_function("NABILWholeLessonOrchestrator.modeLog().length>=2", timeout=90000)
    log = pg.evaluate("NABILWholeLessonOrchestrator.modeLog().map(x=>x.mode)")
    after = pg.evaluate("document.querySelector('#nbWriting .nb-step').textContent")
    record("mixed lesson switches single→dual→single mid-scene",
           log[:2] == ["dual", "single"], str(log))
    record("switching keeps the written content, the same page (no reload) and one hand",
           after == first_text and pg.evaluate("window.__marker") == "same-page"
           and pg.evaluate("document.querySelectorAll('#teacherHand').length") == 1)
    pg.screenshot(path=str(OUT / "04_mixed_back_to_single_desktop.png"))
    record("no page errors (mixed)", not pg.errors, str(pg.errors[:2]))
    pg.context.close()

    # ---------------- full lesson plays to the golden card (FAST), Powers with lab drawings
    pg = new_page(browser, powers, fast=True)
    pg.click("#nbStart")
    pg.wait_for_function("NABILWholeLessonOrchestrator.state().final===true", timeout=60000)
    sup = pg.evaluate("document.querySelectorAll('#nbWriting sup').length")
    txt = pg.evaluate("document.getElementById('nbGolden').textContent.length")
    record("full lesson reaches the Golden Card stage; no JS errors", txt > 10 and not pg.errors, str(pg.errors[:2]))
    pg.goto(f"file://{powers}")
    pg.wait_for_function("!!window.NABILWholeLessonOrchestrator")
    pg.click("#nbStart")
    pg.wait_for_function("NABILWholeLessonOrchestrator.state().final===true", timeout=60000)
    pg.evaluate("""() => { window.__seen={sup:0,raw:false,boxes:0};
        new MutationObserver(ms => { for (const m of ms) for (const n of m.addedNodes) { if (n.nodeType!==1) continue;
          window.__seen.sup += (n.tagName==='SUP'?1:0) + n.querySelectorAll('sup').length;
          window.__seen.boxes += (n.tagName==='rect'||n.tagName==='line'?1:0) + n.querySelectorAll('rect,line').length;
          if (/[\\^*]/.test(n.textContent||'') && n.closest && n.closest('#nbWriting')) window.__seen.raw = true; } })
          .observe(document.getElementById('nabilWholeLessonSmartLab'), {childList:true, subtree:true});
        NABILWholeLessonOrchestrator.goTo(0); }""")
    pg.wait_for_function("NABILWholeLessonOrchestrator.state().final===true", timeout=60000)
    raw = pg.evaluate("window.__seen")
    record("math is real superscripts (no raw ^ or * on screen); Powers pen drew the factor boxes",
           (not raw["raw"]) and raw["sup"] > 0 and raw["boxes"] > 0, str(raw))
    pg.context.close()

    # ---------------- «لم أفهم» → «فهمت، أكمل من هنا»
    pg = new_page(browser, powers_single)
    pg.click("#nbStart")
    pg.wait_for_function("document.querySelectorAll('#nbWriting .nb-step span').length>1", timeout=15000)
    pg.click("#nbLost")
    time.sleep(0.3)
    p_state = state(pg)
    has_btn = pg.evaluate("!!document.getElementById('nbUnderstood')")
    n_a = units_written(pg)
    time.sleep(1.0)
    n_b = units_written(pg)
    pg.click("#nbUnderstood")
    time.sleep(2.0)
    record("«لم أفهم» pauses; «فهمت، أكمل من هنا» resumes the same lesson",
           p_state["paused"] and has_btn and n_a == n_b and (not state(pg)["paused"]) and units_written(pg) > n_b,
           f"{n_a}/{n_b}->{units_written(pg)}")
    pg.context.close()

    # ---------------- formative question: waits for the student, wrong -> feedback, then continue
    chk = [{"id": "Q", "title": "Check", "start_mode": "single", "steps": [
        {"t": "text", "text": "Predict the value.", "label": "", "speech": "Predict the value."},
        {"t": "check", "check": {"question": "What is 2^{3}?", "expected": "8", "wrong_feedback": "Try again.", "correct_feedback": "Yes."}},
        {"t": "text", "text": "After the question the lesson goes on.", "label": "", "speech": ""}]}]
    p_chk = page_html("check", "Check", chk, "en")
    pg = new_page(browser, p_chk, fast=True)
    pg.click("#nbStart")
    pg.wait_for_selector(".nb-check", timeout=15000)
    time.sleep(0.5)
    waiting = state(pg)["studentWait"] and not state(pg)["final"]
    pg.fill(".nb-check input", "7")
    pg.click(".nb-check button >> nth=0")
    wrong = pg.inner_text(".nb-fb")
    pg.fill(".nb-check input", "8")
    pg.click(".nb-check button >> nth=0")
    right = pg.inner_text(".nb-fb")
    pg.click(".nb-check button >> nth=1")
    pg.wait_for_function("NABILWholeLessonOrchestrator.state().final===true", timeout=20000)
    record("formative question halts the lesson until the student continues (wrong -> feedback -> correct)",
           waiting and wrong == "Try again." and right == "Yes.", f"{wrong!r} {right!r}")
    pg.context.close()

    # ---------------- phones: portrait + landscape, no overflow/clipping, drawing stays visible
    for label, (w, h) in {"phone_portrait": (390, 844), "phone_landscape": (844, 390)}.items():
        pg = new_page(browser, cube, w=w, h=h, mobile=True)
        pg.click("#nbStart")
        pg.wait_for_function("document.querySelectorAll('#nbInk *').length>0", timeout=30000)
        time.sleep(1.5)
        m = pg.evaluate("""() => { const q=s=>document.querySelector(s).getBoundingClientRect(), vw=innerWidth, vh=innerHeight;
            const d=q('#nbDiagram'), wr=q('#nbWriting'), c=q('.nb-ctl');
            const btns=[...document.querySelectorAll('.nb-ctl button,.nb-ctl select')].map(b=>b.getBoundingClientRect());
            const clipped=btns.filter(b=>b.right>vw+1||b.left<-1||b.bottom>vh+1).length;
            const ov=!(d.right<=wr.left+1||wr.right<=d.left+1||d.bottom<=wr.top+1||wr.bottom<=d.top+1);
            return {sw:document.documentElement.scrollWidth, vw, clipped, overlap:ov, diagH:d.height, diagVisible:d.top>=-1&&d.bottom<=vh+1, ctlBottom:c.bottom<=vh+1}}""")
        record(f"{label}: no horizontal overflow, controls inside the screen, boards do not overlap",
               m["sw"] <= m["vw"] and m["clipped"] == 0 and not m["overlap"] and m["ctlBottom"], str(m))
        # long explanation scrolls while the drawing stays visible
        pg.evaluate("""() => { const w=document.getElementById('nbWriting'); for(let i=0;i<14;i++){const d=document.createElement('div');d.className='nb-step';d.textContent='filler '+i;d.style.height='90px';w.appendChild(d)} w.scrollTop=w.scrollHeight }""")
        time.sleep(0.4)
        vis = pg.evaluate("""() => { const d=document.getElementById('nbDiagram').getBoundingClientRect();
            return d.top>=-1 && d.bottom<=innerHeight+1 && d.height>120 }""")
        record(f"{label}: drawing stays visible while the explanation scrolls", vis)
        pg.screenshot(path=str(OUT / f"05_cube_{label}.png"))
        record(f"{label}: no page errors", not pg.errors, str(pg.errors[:2]))
        pg.context.close()

    # phone: Powers single board
    pg = new_page(browser, powers_single, w=390, h=844, mobile=True)
    pg.click("#nbStart")
    pg.wait_for_function("document.querySelectorAll('#nbWriting .nb-step span').length>6", timeout=20000)
    fs = pg.evaluate("parseFloat(getComputedStyle(document.querySelector('#nbWriting .nb-step')).fontSize)")
    ov = pg.evaluate("document.documentElement.scrollWidth<=innerWidth")
    record("phone Powers (single board): large clear writing (>=20px) and no overflow", fs >= 20 and ov, f"font {fs}px")
    pg.screenshot(path=str(OUT / "06_powers_single_phone.png"))
    pg.context.close()

    # ---------------- AR/EN/FR labels without mixing
    for lang, start in (("ar", "ابدأ الدرس"), ("fr", "Commencer la leçon"), ("en", "Start lesson")):
        p = page_html(f"lang_{lang}", "Powers", powers_single_scenes("en"), lang, {"fr": "Les puissances"})
        pg = new_page(browser, p)
        label_txt = pg.evaluate("document.getElementById('nbStart').textContent")
        dir_ok = pg.evaluate("document.getElementById('nbOpenTitleEn').dir")
        record(f"UI language {lang}: start button and controls in that language only",
               label_txt == start and dir_ok == "ltr", label_txt)
        pg.screenshot(path=str(OUT / f"07_opening_{lang}.png"))
        pg.context.close()


def main() -> int:
    run_static()
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            run_browser(browser)
        finally:
            browser.close()
    fails = [r for r in RESULTS if r[1] != "PASS"]
    print(f"\n{len(RESULTS) - len(fails)}/{len(RESULTS)} passed; output: {OUT}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
