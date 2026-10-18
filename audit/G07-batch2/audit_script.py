import asyncio,json,re,hashlib,sys
from playwright.async_api import async_playwright
INIT=open('/tmp/claude-0/l4/audit2.py').read().split('INIT="""')[1].split('"""')[0]
async def one(name,w,h,mobile,secs):
  async with async_playwright() as p:
    b=await p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    pg=await (await b.new_context(viewport={"width":w,"height":h},is_mobile=mobile,has_touch=mobile)).new_page();await pg.add_init_script(INIT)
    errs=[];pg.on("pageerror",lambda e:errs.append(str(e)[:120]))
    await pg.goto(f"file:///tmp/claude-0/aud/{name}.html");await pg.wait_for_timeout(2000)
    R={"file":name,"viewport":f"{w}x{h}","overflow_x":await pg.evaluate("document.documentElement.scrollWidth>innerWidth")}
    html=open(f'/tmp/claude-0/aud/{name}.html',encoding='utf-8').read()
    R["has_letter_spelling"]=bool(re.search(r'إيه|إتش|AR_LET|NB_LET',html));R["has_speech_lang_split"]='speech_lang' in html
    try:
      await pg.click("#nbStart",timeout=5000);await pg.wait_for_timeout(secs*1000)
    except Exception as e: R["start_err"]=str(e)[:80]
    sp=await pg.evaluate("window.__speak");R["n_speech"]=len(sp);R["langs"]=sorted({str(s['l']) for s in sp})
    R["unspelled_caps"]=sorted({m for s in sp for m in re.findall(r'\b[A-Z]{2,4}\b',s['t'])})[:10]
    R["mixed_script_utterances"]=sum(1 for s in sp if re.search(r'[؀-ۿ]',s['t']) and re.search(r'[A-Za-z]{3,}',s['t']))
    R["raw_symbols_spoken"]=sum(1 for s in sp if re.search(r'[°∠=]|equals',s['t']))
    R["sample"]=[str(s['l'])+':'+s['t'][:100] for s in sp[1:5]];R["errors"]=errs[:3]
    await b.close();return R
async def m():
  out=[]
  for n in sys.argv[1:]:
    out.append(await one(n,1366,768,False,70));out.append(await one(n,390,844,True,5))
  json.dump(out,open('/tmp/claude-0/aud/result.json','w'),ensure_ascii=False,indent=1)
asyncio.run(m())
