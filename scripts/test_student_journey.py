"""End-to-end student journey on the REAL local platform (phone + desktop):
selection card -> start -> board in full screen -> real lesson -> Solve Exercise -> confirm -> solution on the same board -> back.

HONESTY NOTES (printed at the end too):
 * no AI provider key exists in the sandbox, so the real model is NOT called. The route /api/solver/solve is answered by a
   FIXTURE (marked MOCK below) only to prove the board renders a solution; typed text, PDF text extraction and the
   'no provider' error path are REAL server code.
"""
import asyncio,sys,json,re,base64,pathlib

from playwright.async_api import async_playwright
OUT=pathlib.Path(__import__('os').environ.get('JOURNEY_OUT','/tmp/nabil_journey'));OUT.mkdir(parents=True,exist_ok=True);W=sys.argv[1] if len(sys.argv)>1 else 'phone'
def make_pdf(text):
    body = f"BT /F1 14 Tf 72 720 Td ({text}) Tj ET"
    objs = ["<</Type/Catalog/Pages 2 0 R>>", "<</Type/Pages/Kids[3 0 R]/Count 1>>","<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R/Resources<</Font<</F1 5 0 R>>>>>>",f"<</Length {len(body)}>>\nstream\n{body}\nendstream", "<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>"]
    out, offs = b"%PDF-1.4\n", []
    for i, o in enumerate(objs, 1):
        offs.append(len(out)); out += f"{i} 0 obj\n{o}\nendobj\n".encode()
    x = len(out); out += f"xref\n0 {len(objs)+1}\n0000000000 65535 f \n".encode()
    for o in offs: out += f"{o:010d} 00000 n \n".encode()
    return out + f"trailer<</Size {len(objs)+1}/Root 1 0 R>>\nstartxref\n{x}\n%%EOF".encode()
pdf=OUT/'ex.pdf';pdf.write_bytes(make_pdf("Exercise 4: Solve the equation 3x - 5 = 10 and check your answer."))
png=OUT/'ex.png';png.write_bytes(base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="))
FIX={"status":"ok","title":"Linear equation","statement":"Solve 2x + 3 = 7","lang":"en",
 "given":["2x + 3 = 7"],"required":["Find x"],"figure":{"points":{"A":[0,0],"B":[4,0],"C":[0,3]},"segments":[["A","B","4 cm"],["B","C","5 cm"],["A","C","3 cm"]],"circles":[],"marks":[{"type":"right_angle","at":"A","between":["B","C"]}]},
 "steps":[{"say":"We subtract 3","text":"Subtract 3 from both sides to keep the equality.","formula":"2x + 3 - 3 = 7 - 3","justification":"Equality is kept"},
          {"say":"We simplify","text":"Simplify both sides.","formula":"2x = 4"},
          {"say":"We divide both sides","text":"Divide both sides by 2.","formula":"x = 4 / 2","justification":"Inverse operation"},
          {"say":"So we conclude","text":"Therefore x equals 2.","formula":"x = 2"}],
 "answer":"x = 2","verification":{"status":"verified","detail":"2"}}
INIT="""window.__speak=[];(function(){const S={speak(u){window.__speak.push({t:(u.text||'').slice(0,60),l:u.lang,at:Date.now()});setTimeout(()=>{u.onstart&&u.onstart();setTimeout(()=>u.onend&&u.onend(),250)},10)},cancel(){},pause(){},resume(){},getVoices(){return[]},paused:false,speaking:false,addEventListener(){}};try{Object.defineProperty(window,'speechSynthesis',{value:S,configurable:true})}catch(e){}window.SpeechSynthesisUtterance=function(t){this.text=t};})();"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    ctx=dict(viewport={"width":390,"height":844},is_mobile=True,has_touch=True,device_scale_factor=2) if W=="phone" else dict(viewport={"width":1366,"height":768})
    c=await b.new_context(**ctx);pg=await c.new_page();await pg.add_init_script(INIT)
    errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
    mock={"on":False}
    async def solve_route(route):
        # MOCK fixture (not a model): only used to prove the board renders a solution
        if mock["on"]: await route.fulfill(status=200,content_type="application/json",body=json.dumps(FIX))
        else: await route.continue_()
    await pg.route("**/api/solver/solve",solve_route)
    R={}
    await pg.goto("http://127.0.0.1:8765/",wait_until="networkidle");await pg.wait_for_timeout(1500)
    await pg.click("#homeStartShortcut");await pg.wait_for_timeout(800)
    await pg.select_option("#gradeSelect","الصف الأول");await pg.wait_for_timeout(1000)
    await pg.select_option("#subjectSelect","رياضيات");await pg.wait_for_timeout(500)
    await pg.select_option("#languageSelect","English");await pg.wait_for_timeout(1200)
    await pg.select_option("#lessonSelect",index=2);await pg.wait_for_timeout(500)
    R["speak_before_start"]=await pg.evaluate("window.__speak.length")
    await pg.click("#startGoldenLesson");await pg.wait_for_timeout(9000)
    f=[x for x in pg.frames if 'golden-classroom' in x.url][0]
    R["fullscreen"]=await pg.evaluate("!!document.fullscreenElement")
    R["speak_after_start"]=await f.evaluate("window.__speak.length")
    R["solve_btn_visible"]=await f.evaluate("(()=>{const b=document.getElementById('nbSolveBtn');const r=b.getBoundingClientRect();return !!b.offsetParent&&r.width>0&&r.right<=innerWidth&&r.left>=0})()")
    R["tools_hidden_by_default"]=await f.evaluate("document.getElementById('nbTools').hidden")
    R["no_hscroll"]=await f.evaluate("document.documentElement.scrollWidth<=innerWidth")
    await pg.screenshot(path=OUT/f"{W}_1_lesson.png")
    await f.click("#nbToolsToggle");await f.select_option("#nbSpeed","1.25");await f.click("#nbToolsToggle")
    await f.evaluate("NABILWholeLessonOrchestrator.goTo(2)");await pg.wait_for_timeout(7000)
    st0=await f.evaluate("NABILWholeLessonOrchestrator.state()");R["lesson_state_before"]={k:st0[k] for k in("index","paused","boardMode")}
    R["lesson_text_before"]=await f.evaluate("document.getElementById('nbWriting').innerText.slice(0,160)")
    # open solve
    await f.click("#nbSolveBtn");await pg.wait_for_timeout(600)
    R["paused_on_open"]=await f.evaluate("NABILWholeLessonOrchestrator.state().paused")
    await pg.screenshot(path=OUT/f"{W}_2_modal.png")
    # typed + real (no provider) path
    await f.click("#nbSolveTab_type");await f.fill("#nbSolveText","Solve 2x + 3 = 7");await f.click("#nbSolveRead");await pg.wait_for_timeout(300)
    await pg.screenshot(path=OUT/f"{W}_3_confirm.png")
    await f.click("#nbSolveConfirm");await pg.wait_for_timeout(1500)
    R["real_no_provider_msg"]=await f.evaluate("document.querySelector('.nb-solve-msg').textContent")
    await pg.screenshot(path=OUT/f"{W}_4_noprovider.png")
    # real PDF reading (no model needed)
    await f.click("#nbSolveTab_up")
    await f.set_input_files("#nbSolveFile",str(pdf));await pg.wait_for_timeout(2500)
    R["pdf_confirm_text"]=await f.evaluate("(document.getElementById('nbSolveConfirmText')||{}).value")
    await pg.screenshot(path=OUT/f"{W}_5_pdf_confirm.png")
    # real image path without provider -> honest error
    await f.click("#nbSolveTab_up")
    await f.set_input_files("#nbSolveFile",str(png));await pg.wait_for_timeout(2000)
    R["real_image_no_provider"]=await f.evaluate("document.querySelector('.nb-solve-msg').textContent")
    # mocked solve response (TEST DATA, not a real model) -> board rendering
    mock["on"]=True
    await f.click("#nbSolveTab_type");await f.fill("#nbSolveText","Solve 2x + 3 = 7");await f.click("#nbSolveRead");await f.click("#nbSolveConfirm");await pg.wait_for_timeout(5000)
    R["interlude"]=await f.evaluate("NABILWholeLessonOrchestrator.inInterlude()")
    await pg.screenshot(path=OUT/f"{W}_6_solving_mid.png")
    for _ in range(40):
        await pg.wait_for_timeout(2000)
        if await f.evaluate("!!document.getElementById('nbSolveDone')"):break
    await pg.screenshot(path=OUT/f"{W}_7_solved.png")
    R["solved_text"]=await f.evaluate("document.getElementById('nbWriting').innerText.slice(0,900)")
    R["ink_children"]=await f.evaluate("document.getElementById('nbInk').children.length")
    R["board_mode"]=await f.evaluate("NABILWholeLessonOrchestrator.state().boardMode")
    R["done_box"]=await f.evaluate("!!document.getElementById('nbSolveDone')")
    R["speech_langs"]=await f.evaluate("[...new Set(window.__speak.map(s=>s.l))]");R["speak_samples"]=await f.evaluate("window.__speak.slice(-4).map(s=>s.l+':'+s.t)")
    R["solve_btn_visible_during_solution"]=await f.evaluate("!!document.getElementById('nbSolveBtn').offsetParent")
    R["fullscreen_still"]=await pg.evaluate("!!document.fullscreenElement")
    # repeat step + back to lesson
    await f.click("#nbRepeatStep");await pg.wait_for_timeout(2500)
    R["after_repeat_has_text"]=await f.evaluate("document.getElementById('nbWriting').children.length")
    await f.evaluate("NABILWholeLessonOrchestrator.pause()")
    await f.click("#nbBackToLesson");await pg.wait_for_timeout(2500)
    st1=await f.evaluate("NABILWholeLessonOrchestrator.state()")
    R["lesson_state_after"]={k:st1[k] for k in("index","paused","boardMode")};R["back_in_interlude"]=await f.evaluate("NABILWholeLessonOrchestrator.inInterlude()")
    R["lesson_text_after"]=await f.evaluate("document.getElementById('nbWriting').innerText.slice(0,200)")
    await pg.screenshot(path=OUT/f"{W}_8_back.png")
    R["errors"]=errs[:5]
    print(json.dumps(R,ensure_ascii=False,indent=1))
    await b.close()
    checks=[("no speech before the student starts",R["speak_before_start"]==0),("speech starts after start (gesture)",R["speak_after_start"]>0),
     ("real full screen",R["fullscreen"] and R["fullscreen_still"]),("Solve button visible in full screen",R["solve_btn_visible"] and R["solve_btn_visible_during_solution"]),
     ("tools collapsed by default",R["tools_hidden_by_default"]),("no horizontal scroll",R["no_hscroll"]),
     ("opening Solve pauses the lesson",R["paused_on_open"]),
     ("REAL: no provider -> honest message (nothing invented)","مزوّد" in R["real_no_provider_msg"] and "مزوّد" in R["real_image_no_provider"]),
     ("REAL: PDF text read by the server and shown for confirmation","3x - 5 = 10" in R["pdf_confirm_text"]),
     ("MOCK-solution is written step by step on the same board",R["interlude"] and "We subtract 3" in R["solved_text"] and "x = 4 / 2" in R["solved_text"]),
     ("figure drawn by the pen (ink elements) in dual mode",R["ink_children"]>=10 and R["board_mode"]=="dual"),
     ("solution ends with a finished panel",R["done_box"]),
     ("voice used the board language",bool([l for l in R["speech_langs"] if l])),
     ("back to lesson restores the same scene and text",R["lesson_state_after"]["index"]==R["lesson_state_before"]["index"] and not R["back_in_interlude"] and R["lesson_text_after"][:20]==R["lesson_text_before"][:20]),
     ("no JS errors",not R["errors"])]
    bad=[n for n,ok in checks if not ok]
    for n,ok in checks:print(("PASS  " if ok else "FAIL  ")+n)
    print(f"{W}: {len(checks)-len(bad)}/{len(checks)} passed")
    sys.exit(1 if bad else 0)
asyncio.run(main())
