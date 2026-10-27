"""Engagement layer injected into every direct lesson page (no external services).

Adds: stars + daily streak + progress, and short 'predict/challenge' pauses while the student
clicks Next. Questions are generated from the lesson's own verified equations (so they are always
correct) and use plausible distractors (off-by-one, off-by-ten, digit swap) with a 'why' explanation.
A module may also define QUIZ = [{"q":str,"opts":[...],"a":index,"why":{"en","ar","fr"}}].
"""
import json
import re

EQ = re.compile(r"(\d{1,4})\s*([+\-−×÷x*/])\s*(\d{1,4})\s*=\s*(\d{1,5})(?!\s*[+\-−×÷x*/]\s*\d)")


def _val(a, op, b):
    if op == "+":
        return a + b
    if op in "-−":
        return a - b
    if op in "×x*":
        return a * b
    if op in "÷/":
        return a // b if b and a % b == 0 else None


def _opts(c):
    s = str(c)
    cand = [c + 1, c - 1, c + 10, c - 10]
    if len(s) == 2 and s[0] != s[1]:
        cand.append(int(s[::-1]))
    cand = [x for x in dict.fromkeys(cand) if x >= 0 and x != c]
    return cand[:3]


def _why(c, w):
    d = w - c
    if abs(d) == 1:
        return {"en": "Close! Check the ones.", "ar": "قريب! راجع خانة الآحاد.", "fr": "Presque ! Vérifie les unités."}
    if abs(d) == 10:
        return {"en": "Close! Check the tens.", "ar": "قريب! راجع خانة العشرات.", "fr": "Presque ! Vérifie les dizaines."}
    return {"en": "The digits are swapped. Read the places again.", "ar": "الأرقام معكوسة. اقرأ المنازل من جديد.", "fr": "Les chiffres sont inversés. Relis les positions."}


def questions(m, cap=8):
    out, seen = [], set()
    for q in getattr(m, "QUIZ", []):
        out.append(q)
    texts = []
    for ex in m.EXERCISES:
        for s in ex["steps"]:
            if s["k"] == "f":
                texts.append(s["f"])
    for sc in m.THEORY:
        for s in sc[-1]:
            if s["k"] == "f":
                texts.append(s["f"])
    for t in texts:
        for a, op, b, c in EQ.findall(t):
            a, b, c = int(a), int(b), int(c)
            if _val(a, op, b) != c or (a, op, b) in seen:
                continue
            seen.add((a, op, b))
            wrong = _opts(c)
            if len(wrong) < 3:
                continue
            opts = [c] + wrong
            out.append({"q": f"{a} {op.replace('x','×').replace('*','×').replace('/','÷')} {b} = ?", "opts": [str(o) for o in opts], "a": 0,
                        "why": {str(w): _why(c, w) for w in wrong},
                        "ok": f"{a} {op} {b} = {c}"})
            if len(out) >= cap:
                return out
    return out


CSS = """
#nbEng{position:fixed;top:64px;left:8px;z-index:2147483000;display:flex;gap:8px;font:700 15px sans-serif;direction:ltr}
#nbEng span{background:#fff;border:2px solid #0b3d5c;border-radius:999px;padding:4px 12px;color:#0b3d5c;box-shadow:0 2px 6px #0003}
#nbEngBar{position:fixed;top:0;left:0;height:5px;background:linear-gradient(90deg,#fbc02d,#43a047);width:0;z-index:2147483000;transition:width .4s}
#nbQz{position:fixed;inset:0;background:#0b3d5ccc;z-index:2147483600;display:none;align-items:center;justify-content:center;font-family:sans-serif}
#nbQz .c{background:#fff;border-radius:22px;padding:22px 26px;max-width:460px;width:92%;text-align:center;box-shadow:0 10px 40px #0007}
#nbQz h3{margin:0 0 4px;color:#0b3d5c;font-size:20px}#nbQz .q{font-size:46px;font-weight:800;color:#0b3d5c;margin:10px 0 14px;direction:ltr}
#nbQz .o{display:grid;grid-template-columns:1fr 1fr;gap:10px}
#nbQz .o button{font:800 28px sans-serif;padding:14px;border-radius:14px;border:3px solid #0b3d5c;background:#e3f2fd;color:#0b3d5c;cursor:pointer}
#nbQz .o button.bad{background:#ffcdd2;border-color:#e53935;animation:nbsh .35s}
#nbQz .o button.good{background:#c8e6c9;border-color:#2e7d32}
#nbQz .m{min-height:48px;margin:12px 0 4px;font-size:18px;color:#0b3d5c}
#nbQz .s{background:none;border:0;color:#607d8b;font-size:14px;cursor:pointer;text-decoration:underline}
@keyframes nbsh{25%{transform:translateX(-8px)}75%{transform:translateX(8px)}}
"""

JS = r"""
(function(){
var Q=__Q__, UI=__UI__, lang='ar', stars=0, done=0, clicks=0, every=3, idx=0, total=Q.length;
function ls(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){return null}}
var today=new Date().toISOString().slice(0,10), last=ls('nbStreakDay'), st=parseInt(ls('nbStreak')||'0',10);
if(last!==today){var y=new Date(Date.now()-864e5).toISOString().slice(0,10); st=(last===y)?st+1:1; ls('nbStreakDay',today); ls('nbStreak',String(st));}
var hud=document.createElement('div');hud.id='nbEng';hud.innerHTML='<span id="nbE1">⭐ 0</span><span>🔥 '+st+'</span>';
var bar=document.createElement('div');bar.id='nbEngBar';
var qz=document.createElement('div');qz.id='nbQz';
var host=document.getElementById('nabilWholeLessonSmartLab')||document.body;host.appendChild(hud);host.appendChild(bar);host.appendChild(qz);lang=(host.getAttribute('lang')||'ar').slice(0,2);if(!/^(ar|en|fr)$/.test(lang))lang='ar';
function T(k){return (UI[k]||{})[lang]||(UI[k]||{}).en||''}
function render(){hud.firstChild.textContent='⭐ '+stars;bar.style.width=(total?Math.min(100,done/total*100):0)+'%'}
function ask(){
  if(idx>=total) return;
  var q=Q[idx++], o=q.opts.map(function(t,i){return {t:t,i:i}}).sort(function(){return Math.random()-.5});
  qz.innerHTML='<div class="c" dir="'+(lang==='ar'?'rtl':'ltr')+'"><h3>'+T('think')+'</h3><div class="q">'+q.q+'</div><div class="o"></div><div class="m"></div><button class="s">'+T('skip')+'</button></div>';
  var box=qz.querySelector('.o'), msg=qz.querySelector('.m'), tried=false;
  o.forEach(function(x){var b=document.createElement('button');b.textContent=x.t;b.onclick=function(){
    if(x.i===q.a){b.className='good';if(!tried)stars++;done++;render();msg.textContent=T('yes')+' '+(q.ok||'');setTimeout(function(){qz.style.display='none';if(done>=total)badge()},1100)}
    else{tried=true;b.className='bad';var w=(q.why&&q.why[x.t])||{};msg.textContent=(w[lang]||w.en||T('retry'))}};box.appendChild(b)});
  qz.querySelector('.s').onclick=function(){done++;render();qz.style.display='none'};
  qz.style.display='flex';
}
function badge(){qz.innerHTML='<div class="c"><div style="font-size:70px">🏅</div><h3>'+T('badge')+'</h3><div class="m">⭐ '+stars+' / '+total+'</div><button class="s">OK</button></div>';qz.style.display='flex';qz.querySelector('.s').onclick=function(){qz.style.display='none'}}
document.addEventListener('click',function(e){
  var l=e.target.closest&&e.target.closest('[data-l]'); if(l&&/^(ar|en|fr)$/.test(l.getAttribute('data-l'))) lang=l.getAttribute('data-l');
  var n=e.target.closest&&e.target.closest('#nabilWholeNext'); if(n&&total){clicks++; if(clicks%every===0&&idx<total)setTimeout(ask,700)}
},true);
render();
})();
"""

UI = {
    "think": {"en": "Quick challenge!", "ar": "تحدٍّ سريع!", "fr": "Petit défi !"},
    "skip": {"en": "Skip", "ar": "تخطَّ", "fr": "Passer"},
    "yes": {"en": "Great! ⭐", "ar": "أحسنت! ⭐", "fr": "Bravo ! ⭐"},
    "retry": {"en": "Try again", "ar": "حاول مرة أخرى", "fr": "Réessaie"},
    "badge": {"en": "You finished the challenges!", "ar": "أنهيتَ كل التحديات!", "fr": "Tous les défis réussis !"},
}


def layer(m):
    qs = questions(m)
    if not qs:
        return ""
    return (f"<style>{CSS}</style><script>{JS.replace('__Q__', json.dumps(qs, ensure_ascii=False)).replace('__UI__', json.dumps(UI, ensure_ascii=False))}</script>")
