"""Real-browser regression tests for timetable/index.html (Chromium via Playwright, fake SpeechRecognition engine).
Run: python tests/test_timetable_browser.py"""
import os, re, subprocess, sys, tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright

PAGE = Path(__file__).resolve().parent.parent / 'timetable' / 'index.html'

FAKE = """
window.__recs=[];
class FakeSR{constructor(){this.started=false;window.__recs.push(this)}
 start(){this.started=true;setTimeout(()=>this.onstart&&this.onstart(),0)}
 stop(){this.started=false;setTimeout(()=>this.onend&&this.onend(),0)}
 say(text,final=true){const r=[{transcript:text}];r.isFinal=final;this.onresult({resultIndex:0,results:[r]})}}
window.webkitSpeechRecognition=FakeSR;window.SpeechRecognition=undefined;
"""

def script_syntax():
    html = PAGE.read_text(encoding='utf-8')
    js = '\n'.join(re.findall(r'<script[^>]*>(.*?)</script>', html, re.S))
    f = tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8'); f.write(js); f.close()
    r = subprocess.run(['node', '--check', f.name], capture_output=True, text=True); os.unlink(f.name)
    assert r.returncode == 0, 'JS syntax error in timetable/index.html:\n' + r.stderr[:600]
    print('PASS script syntax (node --check)')

def voice():
    with sync_playwright() as p:
        b = p.chromium.launch(); ctx = b.new_context(); page = ctx.new_page()
        errors = []; page.on('pageerror', lambda e: errors.append(str(e)))
        page.add_init_script(FAKE); page.goto(PAGE.as_uri()); page.wait_for_timeout(300)
        assert not errors, 'page errors on load: %s' % errors
        assert page.is_enabled('#voiceStart') and page.is_disabled('#voiceStop')
        page.click('#voiceStart')                                                     # 1 start
        assert page.evaluate('window.__recs.length') == 1 and page.evaluate('window.__recs[0].started')
        assert page.is_disabled('#voiceStart') and page.is_enabled('#voiceStop')       # 2 listening state
        assert 'listening' in page.get_attribute('.voice-panel', 'class')
        page.evaluate("window.__recs[0].say('الأستاذ أحمد يدرّس الرياضيات')")           # 3-4 capture -> textarea
        assert page.input_value('#pastedTimetable') == 'الأستاذ أحمد يدرّس الرياضيات'
        page.evaluate("window.__recs[0].say('الأستاذ أحمد يدرّس الرياضيات')")           # 9 duplicate suppressed
        assert page.input_value('#pastedTimetable').count('أحمد') == 1
        page.evaluate("window.__recs[0].onend()")                                      # 5 browser ends session -> auto restart
        page.wait_for_timeout(900)
        assert page.evaluate('window.__recs.length') == 2 and page.evaluate('window.__recs[1].started'), 'did not continue listening'
        page.evaluate("window.__recs[1].say('للسابع أ والسابع ب')")
        page.click('#voiceStop')                                                       # 6/10 stop really closes
        assert page.evaluate('window.__recs[1].started') is False
        assert page.is_enabled('#voiceStart') and page.is_disabled('#voiceStop')
        page.evaluate("window.__recs[1].say('نص متأخر بعد الإيقاف')")                  # late result after stop is ignored
        txt = page.input_value('#pastedTimetable'); assert 'متأخر' not in txt
        page.click('#voiceStart')                                                      # 7 second session
        assert page.evaluate('window.__recs.length') == 3 and page.evaluate('window.__recs[2].started')
        page.evaluate("window.__recs[2].say('أربع حصص لكل شعبة')")                      # 8 second text without losing the first
        txt = page.input_value('#pastedTimetable')
        assert 'الأستاذ أحمد' in txt and 'للسابع أ والسابع ب' in txt and 'أربع حصص لكل شعبة' in txt, txt
        assert not errors, errors
        b.close()
    print('PASS microphone flow (start/listen/capture/continue/stop/second session/no duplicates/no loss)')

if __name__ == '__main__':
    script_syntax(); voice()
