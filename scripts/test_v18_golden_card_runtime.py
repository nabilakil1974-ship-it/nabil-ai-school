"""Chromium Golden Card contract; no AI or Drive calls."""
from pathlib import Path
from tempfile import TemporaryDirectory
from playwright.sync_api import sync_playwright
from scripts.nabil_factory.cards.v18_board import render_v18_smart_board, build_golden_spec, verify_v18_scientific_card_inline_engine

def main():
    activity = {
        "concept_id": "SYNTHETIC-001",
        "title": "Meaning of powers",
        "teaching_steps": [{"sentence": "Two cubed means multiplying two three times."}],
        "lab_html": "<div class='nabil-reference-smart-lab'>2 × 2 × 2 = 8</div>",
        "conclusion": "2³ = 8 because 2 × 2 × 2 = 8.",
    }
    with TemporaryDirectory() as temp, sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            for mode in ("lesson", "exercises"):
                for lang in ("en", "ar", "fr"):
                    golden = build_golden_spec(
                        "Powers — synthetic Chromium contract", [activity],
                        lang, subject="mathematics", verification_note="Synthetic arithmetic check")
                    board = render_v18_smart_board(
                        "Powers — synthetic Chromium contract", [activity],
                        lang, golden_spec=golden, mode=mode)
                    assert board and "nabilV18CardEnginePayload" in board
                    assert verify_v18_scientific_card_inline_engine(board), (mode, lang, "embedded source mismatch")
                    assert not verify_v18_scientific_card_inline_engine(
                        board.replace('nabilV18CardEnginePayload">', 'nabilV18CardEnginePayload">A', 1)
                    ), "Tampered payload falsely accepted"
                    assert 'data:image/' not in board, 'Inline raster URL leaked into student HTML'
                    path = Path(temp) / (mode + "_" + lang + ".html")
                    path.write_text('<!doctype html><html><head><meta charset="utf-8">'
                        '<meta name="viewport" content="width=device-width,initial-scale=1">'
                        '</head><body>' + board + '</body></html>', encoding="utf-8")
                    page = browser.new_page(viewport={"width":390, "height":844})
                    errors = []
                    page.on("pageerror", lambda e:errors.append(str(e)))
                    try:
                        page.goto(path.as_uri(), wait_until="domcontentloaded")
                        result = page.evaluate("""() => {
                            const engine=window.NABILScientificCards;
                            const o=window.NABILWholeLessonOrchestrator;
                            if(!engine?.fromLesson || !o) return {init:false};
                            o.goTo(o.finalIndex);
                            const host=document.getElementById('goldenReferenceCard');
                            const card=host?.querySelector('.nabil-sci-card');
                            return {
                                init:true, final:o.state().final, finalIndex:o.finalIndex,
                                visible:document.getElementById('nabilWholeLessonSmartLab').classList.contains('is-final'),
                                height:card?.getBoundingClientRect().height||0,
                                text:card?.innerText||'',
                                grid:!!card?.querySelector('.nabil-sci-grid'),
                                rule:!!card?.querySelector('.nabil-sci-final'),
                                error:host?.dataset.failed||'',
                                avatar:card?.querySelector('.nabil-sci-avatar')?.getAttribute('src')||''
                            };
                        }""")
                        assert result.get("init"), (mode,lang,result,errors)
                        assert result["finalIndex"] == 1 and result["final"] and result["visible"],(mode,lang,result,errors)
                        assert result["height"] > 120 and result["grid"] and result["rule"],(mode,lang,result,errors)
                        assert "2³ = 8" in result["text"] and not result["error"],(mode,lang,result,errors)
                        assert result["avatar"].startswith("blob:"),(mode,lang,result,errors)
                        page.wait_for_function("() => {const img=document.querySelector('#goldenReferenceCard .nabil-sci-avatar');return !!img && img.complete && img.naturalWidth > 0}",timeout=5000)
                        assert not errors,(mode,lang,errors)
                        page.evaluate("() => window.NABILWholeLessonOrchestrator.goTo(0)")
                        assert not page.evaluate("() => window.NABILWholeLessonOrchestrator.state().final")
                        print("PASS V18 REAL CHROMIUM",mode,lang,flush=True)
                    finally:
                        page.close()
        finally:
            browser.close()
if __name__ == "__main__":
    main()
