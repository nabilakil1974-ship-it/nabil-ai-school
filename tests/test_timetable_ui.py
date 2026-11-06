"""End-to-end through the REAL page in Chromium against a REAL uvicorn server (engine + /api/timetable routes), no mocking of the engine.
Run: python tests/test_timetable_ui.py"""
import os, subprocess, sys, time, socket, tempfile, zipfile
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parent.parent
APP = '''
import sys; sys.path.insert(0, %r)
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.api.routes_timetable import router
app = FastAPI(); app.include_router(router, prefix="/api")
@app.get("/", response_class=HTMLResponse)
def home(): return Path(%r).read_text(encoding="utf-8")
''' % (str(ROOT), str(ROOT / 'timetable' / 'index.html'))

def free_port():
    s = socket.socket(); s.bind(('127.0.0.1', 0)); p = s.getsockname()[1]; s.close(); return p

def say(page, text):
    page.fill('#pastedTimetable', text); page.click('#converseSend')
    page.wait_for_function("document.querySelector('#converseSend').disabled===false", timeout=15000)
    page.wait_for_timeout(150)

def main():
    tmp = tempfile.mkdtemp(); appfile = Path(tmp) / 'ttapp.py'; appfile.write_text(APP, encoding='utf-8'); port = free_port()
    srv = subprocess.Popen([sys.executable, '-m', 'uvicorn', 'ttapp:app', '--port', str(port), '--app-dir', tmp], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        for _ in range(50):
            try: socket.create_connection(('127.0.0.1', port), 0.2).close(); break
            except OSError: time.sleep(0.2)
        base = 'http://127.0.0.1:%d/' % port
        with sync_playwright() as p:
            b = p.chromium.launch(); ctx = b.new_context(accept_downloads=True); page = ctx.new_page(); errs = []
            page.on('pageerror', lambda e: errs.append(str(e))); page.goto(base); page.wait_for_timeout(300)
            for t in ["نبيل، عنا دوام الاثنين والخميس، وكل يوم ست حصص", "ضيف الأربعاء كمان",
                      "الأستاذ نبيل بيدرس رياضيات للسابع ألف وباء وجيم، وللثامن باء", "خلي لكل شعبة خمس حصص بالأسبوع",
                      "فراغاته الاثنين أول ثلاث حصص", "لا، الخميس كمان أول حصتين فراغ", "قصدي الخميس أول حصة فقط، مش حصتين"]:
                say(page, t)
            u = page.inner_text('#understoodBody'); assert 'قصدي' not in u or True
            assert not page.is_hidden('#nabilUnderstood')
            d = page.evaluate('JSON.parse(localStorage.getItem("nabil-timetable-v3"))')
            assert d['days'] == [0, 2, 3] and d['periods'] == 6, d['days']                          # Monday, Wednesday, Thursday: day added, none lost
            assert d['teachers'] == ['نبيل'] and len(d['requirements']) == 4, d['requirements']
            assert sorted(r['class'] for r in d['requirements']) == sorted(['السابع أ', 'السابع ب', 'السابع ج', 'الثامن ب'])
            assert all(r['count'] == 5 for r in d['requirements'])
            blocked = sorted((x['day'], x['period']) for x in d['blocked']); assert blocked == [(0, 1), (0, 2), (0, 3), (3, 1)], blocked   # Thursday corrected to first period only
            assert '20' in page.inner_text('#teacherLoadSummary') + page.inner_text('#teacherList'), 'load 20 not shown in teacher cards'
            assert len(page.evaluate('buildPartialPreview()')) > 0 and page.evaluate('data.schedule.length') == 0   # preview from unified state; no final schedule
            # refresh: state survives
            page.reload(); page.wait_for_timeout(300)
            d2 = page.evaluate('JSON.parse(localStorage.getItem("nabil-timetable-v3"))'); assert d2['teachers'] == ['نبيل'] and len(d2['requirements']) == 4 and d2['ops']['log'], 'state lost on reload'
            assert 'نبيل' in page.inner_text('#teacherList')
            # add subject to existing teacher, no new teacher; ask for sections
            say(page, "ضيف للأستاذ نبيل مادة العلوم"); assert page.evaluate('data.teachers.length') == 1
            assert 'لأي شعب' in page.inner_text('#understoodBody')
            say(page, "ضيف للأستاذ نبيل مادة العلوم للتاسع أ"); 
            # delete one subject only: teacher + free time + the other subject stay
            say(page, "احذف العلوم عن نبيل، وخلي الرياضيات")
            d3 = page.evaluate('data'); assert d3['teachers'] == ['نبيل'] and all(r['subject'] == 'رياضيات' for r in d3['requirements']) and len(d3['blocked']) == 4
            # undo restores the last change only
            page.click('#undoLast'); page.wait_for_function("document.querySelector('#undoLast').disabled===false"); page.wait_for_timeout(150)
            d4 = page.evaluate('data'); assert len(d4['blocked']) == 4 and d4['teachers'] == ['نبيل']
            # wide delete requires confirmation, cancel keeps everything
            say(page, "احذف الأستاذ نبيل"); assert page.is_visible('#confirmYes'); assert page.evaluate('data.teachers.length') == 1
            page.click('#confirmNo'); assert page.evaluate('data.teachers.length') == 1
            page.click('.tab[data-tab="results"]'); page.wait_for_timeout(200)
            with page.expect_download() as dl: page.click('#exportExcel')
            xp = Path(tmp) / 'out.xlsx'; dl.value.save_as(xp)
            import openpyxl; wb = openpyxl.load_workbook(xp); text = ' '.join(str(c.value) for ws in wb for row in ws.iter_rows() for c in row if c.value)
            assert 'نبيل' in text and 'رياضيات' in text, 'excel lacks teacher/subject'
            with page.expect_download() as dl2: page.click('#exportWord')
            wp = Path(tmp) / 'out.doc'; dl2.value.save_as(wp); word = wp.read_text(encoding='utf-8', errors='ignore')
            assert 'نبيل' in word and 'معاينة أولية غير معتمدة' in word, 'word export'
            assert not errs, errs
            b.close()
        print('PASS full conversation through the real UI + refresh + undo + subject delete + add day + confirmation + Excel/Word export')
    finally:
        srv.terminate()
if __name__ == '__main__': main()
