import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from playwright.sync_api import sync_playwright
from app.timetable_solver import solve_timetable
ROOT = pathlib.Path(__file__).resolve().parents[1]

def main():
    import functools, http.server, threading
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT / 'timetable')); h.log_message = lambda *a, **k: None
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), h); threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = 'http://127.0.0.1:%d/index.html' % srv.server_address[1]
    data = {'school': 'م', 'days': [0, 1, 2, 3], 'periods': 8, 'teachers': ['TA', 'TB'], 'classes': ['1A', '1B'], 'blocked': [], 'schedule': [],
            'requirements': [{'teacher': 'TA', 'subject': 'Math', 'class': '1A', 'count': 12}, {'teacher': 'TB', 'subject': 'Math', 'class': '1B', 'count': 12}]}
    sent = {}
    with sync_playwright() as p:
        b = p.chromium.launch(); page = b.new_page(); errs = []; page.on('pageerror', lambda e: errs.append(str(e)))
        def route(rt):
            body = json.loads(rt.request.post_data); sent['b'] = body; res = solve_timetable(body)
            rt.fulfill(status=200 if res.get('ok') else 422, content_type='application/json', body=json.dumps(res if res.get('ok') else {'detail': res}))
        page.route('**/api/timetable/generate', route)
        page.goto(url); page.evaluate("d=>localStorage.setItem('nabil-timetable-v3',JSON.stringify(d))", data); page.reload(); page.wait_for_timeout(400)
        page.select_option('#clsLimClasses', ['1A'])
        for d, v in zip(['الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس'], ['6', '6', '7', '6']):
            loc = page.locator('[data-cl-day]'); n = loc.count(); assert n == 4, n
        inputs = page.locator('[data-cl-day]')
        for i, v in enumerate(['6', '6', '7', '6']): inputs.nth(i).fill(v)
        page.click('#clsLimApply'); page.wait_for_timeout(200)
        assert '1A' in page.inner_text('#clsLimList')
        page.click('[data-tab="results"]'); page.click('#generate'); page.wait_for_timeout(1500)
        assert sent['b']['class_day_limits'] == {'1A': {'0': 6, '1': 6, '2': 7, '3': 6}}, sent['b'].get('class_day_limits')
        sc = page.evaluate("JSON.parse(localStorage.getItem('nabil-timetable-v3')).schedule"); assert len(sc) == 24, len(sc)
        lim = {0: 6, 1: 6, 2: 7, 3: 6}
        assert all(e['period'] <= lim[e['day']] for e in sc if e['class'] == '1A')
        page.reload(); page.wait_for_timeout(300); assert '1A' in page.inner_text('#clsLimList')
        assert not errs, errs; b.close(); srv.shutdown()
    print('PASS class daily limits UI')
if __name__ == "__main__":
    main()
