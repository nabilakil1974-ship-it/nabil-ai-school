import asyncio,json,re,hashlib
from playwright.async_api import async_playwright
INIT="""window.__speak=[];window.__w=[];(function(){const V=[{lang:'en-US',name:'en'},{lang:'ar-LB',name:'ar'},{lang:'fr-FR',name:'fr'}];
const S={speak(u){window.__speak.push({t:(u.text||''),l:u.lang,at:Date.now(),wc:(document.getElementById('nbWriting')||{children:[]}).children.length});setTimeout(()=>{u.onstart&&u.onstart();setTimeout(()=>u.onend&&u.onend(),600)},10)},cancel(){},pause(){},resume(){},getVoices(){return V},paused:false,speaking:false,addEventListener(){}};
try{Object.defineProperty(window,'speechSynthesis',{value:S,configurable:true})}catch(e){}window.SpeechSynthesisUtterance=function(t){this.text=t};})();"""
H0=hashlib.sha256(open('l4_test_copy.html','rb').read()).hexdigest()
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    pg=await (await b.new_context(viewport={"width":1366,"height":768})).new_page();await pg.add_init_script(INIT)
    errs=[];pg.on("pageerror",lambda e:errs.append(str(e)[:150]))
    await pg.goto("file:///tmp/claude-0/l4/l4_test_copy.html");await pg.wait_for_timeout(2500)
    await pg.click("#nbStart")
    await pg.wait_for_timeout(100000)
    sp=await pg.evaluate("window.__speak")
    nodes=await pg.evaluate("[...document.querySelectorAll('#nbWriting .nb-step')].map(n=>[n.classList.contains('nb-formula')?'F':'T',n.innerText.slice(0,80)])")
    st=await pg.evaluate("NABILWholeLessonOrchestrator.state()")
    R={"n_speech":len(sp),"langs":sorted({str(s['l']) for s in sp}),"state":{k:st[k] for k in('index','paused') if k in st},
       "n_nodes_T":sum(1 for n in nodes if n[0]=='T'),"n_nodes_F":sum(1 for n in nodes if n[0]=='F'),
       "spoken_samples":[str(s['l'])+':'+s['t'][:110] for s in sp[:10]],
       "caps_unspelled_in_speech":[m for s in sp for m in re.findall(r'\b[A-Z]{2,4}\b',s['t'])][:12],
       "degree_sign_in_speech":sum(1 for s in sp if '°' in s['t']),
       "formula_text_spoken":sum(1 for s in sp if re.search(r'equals|=',s['t'])),
       "written_not_spoken_sample":[n[1] for n in nodes if n[0]=='F'][:4],"errors":errs[:4]}
    print(json.dumps(R,ensure_ascii=False,indent=1))
    await pg.screenshot(path="shot_audit3.png");await b.close()
asyncio.run(m())
print('sha256 after',hashlib.sha256(open('l4_test_copy.html','rb').read()).hexdigest()==H0)
