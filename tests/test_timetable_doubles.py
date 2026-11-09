"""Double-period (two consecutive lessons) support: solver + real browser UI.
Run: python tests/test_timetable_doubles.py"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from app.timetable_solver import solve_timetable
from playwright.sync_api import sync_playwright

def school(double):
    classes = ['7A', '7B', '8A', '8B']; teachers = ['T%d' % i for i in range(8)]
    reqs = []
    for ci, c in enumerate(classes):
        for si, (sub, cnt) in enumerate([('عربي', 6), ('رياضيات', 5), ('علوم', 3), ('فرنسي', 5), ('انكليزي', 4), ('تاريخ', 1)]):
            reqs.append({'class': c, 'teacher': teachers[(si + ci * 2) % 8] if si < 5 else teachers[5], 'subject': sub,
                         'count': cnt, 'double': double if sub in ('عربي', 'رياضيات') else 0})
    return {'days': [0, 1, 2, 3, 4], 'periods': 7, 'teachers': teachers, 'classes': classes, 'requirements': reqs,
            'blocked': [], 'break_after_period': 3}

def check_pairs(sc, break_after=3):
    pairs = {}
    for x in sc:
        if x.get('double'):
            pairs.setdefault((x['class'], x['subject'], x['day'], x['lesson'] - (x['lesson'] % 2 == 0)), []).append(x['period'])
    n = 0
    by = {}
    for x in sc:
        if x.get('double'):
            by.setdefault((x['class'], x['teacher'], x['subject'], x['day']), []).append(x['period'])
    for k, v in by.items():
        v.sort(); assert len(v) % 2 == 0, k
        for a, b in zip(v[::2], v[1::2]):
            assert b == a + 1 and a != break_after, (k, v); n += 1
    return n

def solver():
    for d in (0, 1, 2):
        r = solve_timetable(school(d)); assert r['ok'] and r['scheduled_lessons'] == r['requested_lessons'] == 96, r
        assert check_pairs(r['schedule']) == 8 * d
    # no teacher conflicts / class conflicts
    r = solve_timetable(school(2)); assert len({(x['teacher'], x['day'], x['period']) for x in r['schedule']}) == 96
    assert len({(x['class'], x['day'], x['period']) for x in r['schedule']}) == 96
    # impossible: teacher free in a single period only -> clear message, not a wrong schedule
    p = school(1)
    for day in range(5):
        for per in range(1, 8):
            if per != 3: p['blocked'].append({'teacher': 'T0', 'day': day, 'period': per})
    r = solve_timetable(p); assert not r['ok'] and 'متتاليتان' in r['message'], r
    # double larger than count//2 is clamped
    q = school(0); q['requirements'][0]['double'] = 99
    r = solve_timetable(q); assert r['ok'] and check_pairs(r['schedule']) == 3
    print('PASS solver doubles')

def _serve():
    import functools, http.server, threading
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT / 'timetable'))
    h.log_message = lambda *a, **k: None
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), h); threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv

def browser():
    srv = _serve(); url = 'http://127.0.0.1:%d/index.html' % srv.server_address[1]
    data = {'school': 'مدرسة', 'days': [0, 1, 2, 3, 4], 'periods': 7, 'breakAfterPeriod': 3,
            'teachers': ['T%d' % i for i in range(8)], 'classes': ['7A', '7B', '8A', '8B'], 'blocked': [], 'schedule': [],
            'requirements': [{'teacher': r['teacher'], 'subject': r['subject'], 'class': r['class'], 'count': r['count']} for r in school(0)['requirements']]}
    sent = {}
    with sync_playwright() as p:
        b = p.chromium.launch(); page = b.new_page(); errs = []; page.on('pageerror', lambda e: errs.append(str(e)))
        def route(rt):
            body = json.loads(rt.request.post_data); sent['body'] = body; res = solve_timetable(body)
            rt.fulfill(status=200 if res.get('ok') else 422, content_type='application/json', body=json.dumps(res if res.get('ok') else {'detail': res}))
        page.route('**/api/timetable/generate', route)
        page.goto(url)
        page.evaluate("d=>localStorage.setItem('nabil-timetable-v3',JSON.stringify(d))", data); page.reload(); page.wait_for_timeout(400)
        page.click('[data-tab="subjects"]'); page.wait_for_timeout(200)
        sel = page.locator('#reqList select'); assert sel.count() == 20, sel.count()
        for i in (0, 6):   # first two rows of different classes -> choose "1 time" and the largest
            pass
        sel.nth(0).select_option('1'); sel.nth(1).select_option('2')
        page.wait_for_timeout(200)
        stored = page.evaluate("JSON.parse(localStorage.getItem('nabil-timetable-v3')).requirements.slice(0,2).map(r=>r.double)"); assert stored == [1, 2], stored
        page.click('[data-tab="results"]'); page.click('#generate'); page.wait_for_timeout(1500)
        assert 'body' in sent, page.inner_text('#resultStatus')
        assert [r['double'] for r in sent['body']['requirements'][:2]] == [1, 2] and sent['body']['break_after_period'] == 3
        sc = page.evaluate("JSON.parse(localStorage.getItem('nabil-timetable-v3')).schedule"); assert len(sc) == 96, len(sc)
        assert check_pairs(sc) == 3, 'expected 1+2 doubles'
        # reload keeps the choice
        page.reload(); page.wait_for_timeout(300); page.click('[data-tab="subjects"]')
        assert page.locator('#reqList select').nth(1).input_value() == '2'
        assert not errs, errs; b.close(); srv.shutdown()
    print('PASS browser doubles (UI -> payload -> schedule)')

if __name__ == '__main__':
    solver(); browser()
