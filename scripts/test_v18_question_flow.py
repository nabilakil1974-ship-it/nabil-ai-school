"""Autoplay must not stop at a student question: ask, think, reveal answer, continue."""
from pathlib import Path
from tempfile import TemporaryDirectory
from playwright.sync_api import sync_playwright
from scripts.nabil_factory.cards.v18_board import render_v18_smart_board, build_golden_spec


def main():
    acts = [{
        "concept_id": "C1", "title": "Idea one", "lab_html": "", "allow_no_lab": True,
        "teaching_steps": [
            {"sentence": "Look at the cube"},
            {"sentence": "Try a prediction", "student_check": {
                "question": "What is two cubed?", "expected": "8", "hint": "2x2x2",
                "wrong_feedback": "no", "correct_feedback": "Yes, three equal factors."}},
            {"sentence": "So the exponent counts factors"}],
        "conclusion": "2^3 = 8"}]
    with TemporaryDirectory() as tmp, sync_playwright() as p:
        spec = build_golden_spec("Q", acts, "en", subject="mathematics")
        f = Path(tmp) / "q.html"
        f.write_text("<html><head><meta charset='utf-8'></head><body>" + render_v18_smart_board("Q", acts, "en", golden_spec=spec) + "</body></html>")
        b = p.chromium.launch(headless=True)
        try:
            page = b.new_page()
            errs = []
            page.on("pageerror", lambda e: errs.append(str(e)))
            page.add_init_script("window.NABIL_V18_FAST=false;window.__t0=Date.now()")
            page.goto(f.as_uri())
            page.evaluate("void window.NABILWholeLessonOrchestrator.play()")
            page.wait_for_function("window.NABILWholeLessonOrchestrator.state().awaitingStudent===true", timeout=60000)
            # after the thinking pause the answer is revealed, then the lesson moves on by itself
            page.wait_for_function("window.NABILWholeLessonOrchestrator.state().awaitingStudent===false&&(document.querySelector('.v18-student-feedback')?.textContent||'').length>0", timeout=60000)
            fb = page.evaluate("document.querySelector('.v18-student-feedback')?.textContent||''")
            page.wait_for_function("window.NABILWholeLessonOrchestrator.state().step===2||window.NABILWholeLessonOrchestrator.state().final", timeout=60000)
            assert "8" in fb and "three equal factors" in fb, fb
            assert not errs, errs
            print("PASS question flow: ask -> think -> answer -> continue")
        finally:
            b.close()


if __name__ == "__main__":
    main()
