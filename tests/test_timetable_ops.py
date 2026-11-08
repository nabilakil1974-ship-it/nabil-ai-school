import json, sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.timetable_ops import apply, new_state, load_of

def run(texts, s=None):
    s = s or new_state(); out = []
    for t in texts:
        r = apply(s, t); s = r['state']; out.append(r)
    return s, out

DIALOGUE = ["نبيل، عنا دوام الاثنين والخميس، وكل يوم ست حصص", "ضيف الأربعاء كمان",
            "الأستاذ نبيل بيدرس رياضيات للسابع ألف وباء وجيم، وللثامن باء", "خلي لكل شعبة خمس حصص بالأسبوع",
            "فراغاته الاثنين أول ثلاث حصص", "لا، الخميس كمان أول حصتين فراغ", "قصدي الخميس أول حصة فقط، مش حصتين"]

class Ops(unittest.TestCase):
    def test_days_add_keeps_existing(self):
        s, _ = run(DIALOGUE[:2]); self.assertEqual(s['days'], ['الاثنين', 'الأربعاء', 'الخميس']); self.assertEqual(s['periods_per_day'], 6)
    def test_assignment_sections_and_load(self):
        s, _ = run(DIALOGUE[:4]); a = s['teachers']['نبيل']['assignments'][0]
        self.assertEqual(a['sections'], ['7أ', '7ب', '7ج', '8ب']); self.assertEqual(a['per_section'], 5)
        self.assertEqual(load_of(s, 'نبيل')['required'], 20)
    def test_free_time_is_not_teaching_and_correction_replaces(self):
        s, _ = run(DIALOGUE); t = s['teachers']['نبيل']
        self.assertEqual(t['free']['الاثنين'], [1, 2, 3]); self.assertEqual(t['free']['الخميس'], [1])   # corrected: first period only
        self.assertEqual(len(t['assignments']), 1)
    def test_add_subject_to_existing_teacher_no_new_teacher(self):
        s, rs = run(DIALOGUE + ["ضيف للأستاذ نبيل مادة العلوم"]); self.assertEqual(list(s['teachers']), ['نبيل'])
        self.assertEqual([a['subject'] for a in s['teachers']['نبيل']['assignments']], ['رياضيات', 'علوم'])
        self.assertTrue(any('لأي شعب' in q for q in rs[-1]['questions']))        # asks, does not guess sections
    def test_delete_subject_only(self):
        s, _ = run(DIALOGUE + ["ضيف للأستاذ نبيل مادة العلوم", "احذف العلوم عن نبيل، وخلي الرياضيات"])
        t = s['teachers']['نبيل']; self.assertEqual([a['subject'] for a in t['assignments']], ['رياضيات'])
        self.assertEqual(t['free']['الاثنين'], [1, 2, 3]); self.assertEqual(t['assignments'][0]['per_section'], 5)
    def test_undo_last_change_only(self):
        s, _ = run(DIALOGUE); before = json.dumps(s['teachers'], ensure_ascii=False)
        s2, _ = run(["قصدي الاثنين أول حصة فقط"], s); self.assertEqual(s2['teachers']['نبيل']['free']['الاثنين'], [1])
        s3, _ = run(["لا، رجّع آخر تعديل"], s2); self.assertEqual(json.dumps(s3['teachers'], ensure_ascii=False), before)
        self.assertEqual(s3['days'], s['days'])     # earlier changes survive
    def test_query_load_and_missing(self):
        s, rs = run(DIALOGUE + ["قديش صار نصاب نبيل؟ وشو بعد ناقصنا؟"]); ans = ' '.join(rs[-1]['answers'])
        self.assertIn('20', ans); self.assertIn('لا يوجد نقص', ans)
    def test_ambiguity_asks_and_changes_nothing(self):
        s, rs = run(["الأستاذ سمر بيدرس علوم للثامن"]); self.assertTrue(any('الشعب' in q for q in rs[0]['questions']))
        s, rs = run(["بلا بلا بلا"], new_state()); self.assertTrue(rs[0]['questions']); self.assertEqual(rs[0]['state']['teachers'], {})
    def test_wide_delete_needs_confirmation(self):
        s, _ = run(DIALOGUE)
        r = apply(s, "احذف الأستاذ نبيل"); self.assertTrue(r['confirm_needed']); self.assertIn('نبيل', r['state']['teachers'])
        r2 = apply(s, "احذف الأستاذ نبيل", confirm=True); self.assertNotIn('نبيل', r2['state']['teachers'])
        r3 = apply(s, "احذف كل المواد عن نبيل"); self.assertTrue(r3['confirm_needed']); self.assertEqual(len(r3['state']['teachers']['نبيل']['assignments']), 1)
        r4 = apply(s, "احذف كل المواد عن نبيل", confirm=True); self.assertIn('نبيل', r4['state']['teachers']); self.assertEqual(r4['state']['teachers']['نبيل']['assignments'], [])
        self.assertEqual(r4['state']['teachers']['نبيل']['free']['الاثنين'], [1, 2, 3])      # teacher + free times survive
    def test_remove_day(self):
        s, _ = run(["عنا دوام الاثنين والثلاثاء والخميس", "شيل الثلاثاء"]); self.assertEqual(s['days'], ['الاثنين', 'الخميس'])
    def test_http_endpoint_roundtrip(self):
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        from app.api.routes_timetable import router
        app = FastAPI(); app.include_router(router); c = TestClient(app); st = None
        for t in DIALOGUE[:4]:
            r = c.post('/timetable/converse', json={'text': t, 'state': st}); self.assertEqual(r.status_code, 200); st = r.json()['state']
        self.assertEqual(r.json()['loads']['نبيل']['required'], 20); self.assertFalse(r.json()['external_ai'])
        self.assertEqual(c.post('/timetable/converse', json={'text': ' '}).status_code, 400)
    def test_no_external_services(self):
        import re; src = (Path(__file__).resolve().parent.parent / 'app' / 'timetable_ops.py').read_text(encoding='utf-8')
        self.assertIsNone(re.search(r'requests|urllib|httpx|openai|anthropic|gemini|http://|https://', src))
if __name__ == '__main__': unittest.main(verbosity=1)


def test_different_periods_per_day_and_day_ranges():
    from app import timetable_ops as t
    s = t.new_state()
    s = t.apply(s, "الدوام من الاثنين الى الجمعة وكل يوم ست حصص")["state"]
    assert s["days"] == ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة"] and s["periods_per_day"] == 6
    s = t.apply(s, "الاثنين 8 حصص والثلاثاء 7 حصص")["state"]
    assert s["day_periods"] == {"الاثنين": 8, "الثلاثاء": 7}
    s = t.apply(s, "تراجع عن آخر تعديل")["state"]
    assert s["day_periods"] == {}
    s = t.apply(s, "الاثنين 8 حصص")["state"]
    s = t.apply(s, "كل يوم سبع حصص")["state"]
    assert s["day_periods"] == {} and s["periods_per_day"] == 7
