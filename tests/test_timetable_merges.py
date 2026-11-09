from collections import defaultdict
from app.timetable_solver import solve_timetable


def payload(merges=True):
    reqs = []
    for c in ("3", "4"):
        reqs.append({"teacher": "TL", "subject": "Language", "class": c, "count": 5})
        reqs.append({"teacher": "TS", "subject": "Social", "class": c, "count": 2})
        reqs.append({"teacher": "TM" + c, "subject": "Math", "class": c, "count": 4})
        reqs.append({"teacher": "TE" + c, "subject": "Science", "class": c, "count": 3})
    p = {"days": [0, 1, 2, 3, 4], "periods": 6, "teachers": ["TL", "TS", "TM3", "TM4", "TE3", "TE4"],
         "classes": ["3", "4"], "requirements": reqs, "blocked": []}
    if merges:
        p["merges"] = [{"classes": ["3", "4"], "subjects": ["Language", "Social"]}]
    return p


def test_merged_subjects_share_slot_and_others_stay_separate():
    r = solve_timetable(payload())
    assert r["ok"], r
    sc = r["schedule"]
    assert len(sc) == 2 * 14
    by = defaultdict(set)
    for e in sc:
        if e["subject"] in ("Language", "Social"):
            by[(e["subject"], e["day"], e["period"])].add(e["class"])
    assert all(v == {"3", "4"} for v in by.values()), by
    assert sum(1 for e in sc if e["subject"] == "Language" and e["class"] == "3") == 5
    assert all("merged_with" in e for e in sc if e["subject"] in ("Language", "Social"))
    assert all("merged_with" not in e for e in sc if e["subject"] in ("Math", "Science"))
    assert r["audit"]["passed"]


def test_without_merges_teacher_needs_twice_the_slots():
    r = solve_timetable(payload(False))
    assert r["ok"]
    assert len([e for e in r["schedule"] if e["teacher"] == "TL"]) == 10


def test_unequal_merged_counts_are_rejected():
    p = payload()
    p["requirements"][0]["count"] = 4
    r = solve_timetable(p)
    assert not r["ok"] and r["status"] == "invalid_input"


def test_merged_with_double_and_class_limits():
    p = payload()
    for q in p["requirements"]:
        if q["subject"] == "Language":
            q["double"] = 1
    p["class_day_limits"] = {"3": {"0": 4}}
    r = solve_timetable(p)
    assert r["ok"], r
    assert all(e["period"] <= 4 for e in r["schedule"] if e["class"] == "3" and e["day"] == 0)
