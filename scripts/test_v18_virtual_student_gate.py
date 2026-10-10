"""Real browser contract for the pedagogical student gate; no Drive or AI calls."""
from pathlib import Path
from tempfile import TemporaryDirectory
from playwright.sync_api import sync_playwright
from scripts.nabil_factory.cards.v18_board import render_v18_smart_board, build_golden_spec

def main():
    first = {
        "concept_id": "SYNTHETIC-SEE", "title": "See and Try",
        "teaching_steps": [
            {"sentence": "Observe repeated multiplication."},
            {"sentence": "Try a prediction.", "student_check": {
                "question": "What is two cubed?",
                "expected": "8",
                "hint": "Two times two times two.",
                "wrong_feedback": "Not yet. Count three factors of two.",
                "correct_feedback": "Yes. Explain three equal factors.",
            }},
            {"sentence": "Conclude: exponent counts repeated factors."},
        ],
        "lab_html": "", "allow_no_lab": True,
        "conclusion": "2³ = 8",
    }
    second = {
        "concept_id": "SYNTHETIC-APPLY", "title": "Apply",
        "teaching_steps": [{"sentence": "Use repeated factors to explain the answer."}],
        "lab_html": "", "allow_no_lab": True, "conclusion": "Reason before computing.",
    }
    with TemporaryDirectory() as tmp, sync_playwright() as p:
        spec = build_golden_spec("Synthetic teaching", [first,second], "en", subject="mathematics")
        html = render_v18_smart_board("Synthetic teaching",[first,second],"en",golden_spec=spec)
        file = Path(tmp)/"teaching.html"
        file.write_text("<html><head><meta charset='utf-8'></head><body>"+html+"</body></html>")
        browser = p.chromium.launch(headless=True)
        try:
            page=browser.new_page()
            errors=[]
            page.on("pageerror",lambda exc:errors.append(str(exc)))
            page.add_init_script("""(() => {
              window.__spokenEvents = [];
              class FakeUtterance {
                constructor(text) { this.text = text; this.onend = null; this.onerror = null; }
              }
              Object.defineProperty(window, 'SpeechSynthesisUtterance',
                {configurable:true,value:FakeUtterance});
              Object.defineProperty(window, 'speechSynthesis', {configurable:true,value:{
                cancel(){},
                getVoices(){ return [{lang:'en-US',name:'QA English'}]; },
                speak(u){
                  window.__spokenEvents.push({
                    sentence:u.text,
                    boardAtStart:document.getElementById('v18Lines')?.innerText || ''
                  });
                  Promise.resolve().then(()=>u.onend && u.onend());
                }
              }});
            })()""")
            page.goto(file.as_uri())
            page.locator("#nabilWholeCurrent").click()
            page.wait_for_function("window.__spokenEvents.length > 0")
            speech_event = page.evaluate("window.__spokenEvents[0]")
            assert speech_event["sentence"] == "Observe repeated multiplication."
            assert speech_event["boardAtStart"].count("Observe repeated multiplication.") == 0, (
                "Speech must start before typing finishes, not after the board is complete"
            )
            page.locator("#nabilWholeStop").click()
            page.evaluate("window.NABILWholeLessonOrchestrator.goTo(0)")
            page.locator("#nabilWholeNext").click()
            page.wait_for_function("window.NABILWholeLessonOrchestrator.state().awaitingStudent === true")
            assert page.locator("#v18StudentInteraction").is_visible()
            page.locator("#nabilWholeNext").click()
            assert page.evaluate("window.NABILWholeLessonOrchestrator.state().idea") == 0
            page.locator("#v18StudentInteraction input").fill("6")
            page.locator("#v18StudentInteraction .v18-student-submit").click()
            assert "Count three factors" in page.locator("#v18StudentInteraction").inner_text()
            assert page.evaluate("window.NABILWholeLessonOrchestrator.state().awaitingStudent")
            page.locator("#v18StudentInteraction .v18-student-hint").click()
            assert "Two times" in page.locator("#v18StudentInteraction").inner_text()
            page.locator("#v18StudentInteraction input").fill("8")
            page.locator("#v18StudentInteraction .v18-student-submit").click()
            assert not page.evaluate("window.NABILWholeLessonOrchestrator.state().awaitingStudent")
            page.locator("#nabilWholeNext").click()
            page.wait_for_function("window.NABILWholeLessonOrchestrator.state().step === 2")
            page.locator("#nabilWholeNext").click()
            page.wait_for_function("window.NABILWholeLessonOrchestrator.state().idea === 1")
            assert "Observe repeated multiplication" in page.locator("#v18Lines").inner_text()
            assert not errors, errors
            print("PASS Chromium voice starts before line is finished writing")
            print("PASS virtual student wrong → feedback → hint → correct → cumulative board")
        finally:
            browser.close()

if __name__ == "__main__":
    main()
