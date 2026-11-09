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
    reqs = []
    for c in ('3', '4'):
        reqs += [{'teacher': 'TL', 'subject': 'Language', 'class': c, 'count': 5}, {'teacher': 'TM' + c, 'subject': 'Math', 'class': c, 'count': 4}]
    data = {'school': 'م', 'days': [0, 1, 2, 3, 4], 'periods': 6, 'teachers': ['TL', 'TM3', 'TM4'], 'classes': ['3', '4'], 'blocked': [], 'schedule': [], 'requirements': reqs}
    sent = {}
    with sync_playwright() as p:
        b = p.chromium.launch(); page = b.new_page(); errs = []; page.on('pageerror', lambda e: errs.append(str(e)))
        def route(rt):
            body = json.loads(rt.request.post_data); sent['b'] = body; res = solve_timetable(body)
            rt.fulfill(status=200 if res.get('ok') else 422, content_type='application/json', body=json.dumps(res if res.get('ok') else {'detail': res}))
        page.route('**/api/timetable/generate', route)
        page.goto(url); page.evaluate("d=>localStorage.setItem('nabil-timetable-v3',JSON.stringify(d))", data); page.reload(); page.wait_for_timeout(400)
        page.select_option('#mgClasses', ['3', '4']); page.select_option('#mgSubjects', ['Language']); page.click('#mgApply'); page.wait_for_timeout(200)
        assert '3 + 4' in page.inner_text('#mgList')
        page.click('[data-tab="results"]'); page.click('#generate'); page.wait_for_timeout(1500)
        assert sent['b']['merges'] == [{'classes': ['3', '4'], 'subjects': ['Language']}], sent['b'].get('merges')
        sc = page.evaluate("JSON.parse(localStorage.getItem('nabil-timetable-v3')).schedule"); assert len(sc) == 18, len(sc)
        lang = {(e['day'], e['period']) for e in sc if e['subject'] == 'Language'}; assert len(lang) == 5, lang
        page.click('#audit'); page.wait_for_timeout(300); st = page.inner_text('#resultStatus'); assert 'لا يوجد أي تضارب' in st, st
        assert not errs, errs; b.close(); srv.shutdown()
    print('PASS merged classes UI')
if __name__ == "__main__":
    main()
