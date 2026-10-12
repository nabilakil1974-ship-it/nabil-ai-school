"""Real-browser contract for the calm 'video' playback: one continuous lesson,
slow pace tied to the voice, true pause/resume, minimal visible controls."""
from pathlib import Path
from tempfile import TemporaryDirectory
from playwright.sync_api import sync_playwright
from scripts.nabil_factory.cards.v18_board import render_v18_smart_board, build_golden_spec

SENT = "We place one grain of wheat on the first square of the board today"


def main():
    acts = [{
        "concept_id": f"C{i}", "title": f"Idea number {i}", "lab_html": "", "allow_no_lab": True,
        "teaching_steps": [{"sentence": SENT}, {"sentence": "Then we double the grains on every square"}],
        "conclusion": "2^n",
    } for i in (1, 2)]
    with TemporaryDirectory() as tmp, sync_playwright() as p:
        spec = build_golden_spec("Calm", acts, "en", subject="mathematics")
        html = render_v18_smart_board("Calm", acts, "en", golden_spec=spec)
        f = Path(tmp) / "calm.html"
        f.write_text("<html><head><meta charset='utf-8'></head><body>" + html + "</body></html>")
        b = p.chromium.launch(headless=True)
        try:
            page = b.new_page(viewport={"width": 1280, "height": 900})
            errs = []
            page.on("pageerror", lambda e: errs.append(str(e)))
            # Fake voice that reports word boundaries slowly (350 ms per word) and honours pause/resume.
            page.add_init_script("""(() => {
              window.__rates=[]; let cur=null, timer=null, paused=false, i=0, words=[];
              class U{constructor(t){this.text=t}}
              Object.defineProperty(window,'SpeechSynthesisUtterance',{configurable:true,value:U});
              function run(){ clearInterval(timer); timer=setInterval(()=>{ if(paused||!cur) return;
                  if(i>=words.length){clearInterval(timer);const u=cur;cur=null;u.onend&&u.onend();return}
                  const w=words[i++]; cur.onboundary&&cur.onboundary({name:'word',charIndex:w.s,charLength:w.l}); },350) }
              Object.defineProperty(window,'speechSynthesis',{configurable:true,value:{
                cancel(){clearInterval(timer);cur=null;paused=false},
                pause(){paused=true}, resume(){paused=false},
                getVoices(){return [{lang:'en-US',name:'QA'}]},
                speak(u){window.__rates.push(u.rate);cur=u;i=0;paused=false;words=[];
                  const re=/\\S+/g;let m;while((m=re.exec(u.text)))words.push({s:m.index,l:m[0].length});run()}}});
            })()""")
            page.goto(f.as_uri())
            visible = page.evaluate("""[...document.querySelectorAll('#nabilWholeLessonSmartLab button')].filter(b=>b.checkVisibility({checkVisibilityCSS:true,contentVisibilityAuto:true})).map(b=>b.id)""")
            core = [v for v in visible if v and not v.startswith("v18") or v in ("v18Speed",)]
            assert "nabilWholeStop" not in visible and "nabilWholeNext" not in visible, visible
            assert page.locator("#v18LabWrap").is_hidden(), "inline lab must be hidden by default"
            assert page.locator(".v18-box").first.is_hidden(), "summary side panel must be hidden"
            page.locator("#nabilWholePlay").click()
            page.wait_for_function("document.querySelector('#v18Lines .v18-line.now .t')?.textContent.length>3")
            assert page.evaluate("window.__rates[0]") < 0.85, "default pace must be slow"
            # writing follows the spoken words: after ~1.2 s only a few words are written
            page.wait_for_timeout(1200)
            n1 = page.evaluate("document.querySelector('#v18Lines .v18-line.now .t').textContent.length")
            assert 0 < n1 < len(SENT) * 0.6, n1
            assert page.locator("#nabilWholePlay").inner_text().startswith("⏸"), "button must become Pause"
            # true pause: nothing is written while paused, then it resumes where it stopped
            page.locator("#nabilWholePlay").click()
            assert page.evaluate("window.NABILWholeLessonOrchestrator.state().paused") is True
            a = page.evaluate("document.querySelector('#v18Lines .v18-line.now .t').textContent")
            page.wait_for_timeout(1500)
            b2 = page.evaluate("document.querySelector('#v18Lines .v18-line.now .t').textContent")
            assert a == b2, "board must not advance while paused"
            assert page.locator("#nabilWholePlay").inner_text().startswith("▶")
            page.locator("#nabilWholePlay").click()
            page.wait_for_function(f"document.querySelector('#v18Lines .v18-line.now .t').textContent.length>{len(a)}")
            # the lesson continues by itself into step 2 (no click needed)
            page.wait_for_function("window.NABILWholeLessonOrchestrator.state().step===1", timeout=30000)
            assert not errs, errs
            print("PASS calm playback: slow, voice-paced, pause/resume, minimal controls")
        finally:
            b.close()


if __name__ == "__main__":
    main()
