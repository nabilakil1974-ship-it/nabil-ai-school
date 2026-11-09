from app.timetable_solver import solve_timetable


def _payload(limits, classes=("1A", "1B"), count=14):
    reqs, teachers = [], []
    for i, c in enumerate(classes):
        t = "T" + c
        teachers.append(t)
        reqs.append({"teacher": t, "subject": "Math", "class": c, "count": count})
    return {"days": [0, 1, 2, 3], "periods": 8, "teachers": teachers, "classes": list(classes),
            "requirements": reqs, "blocked": [], "class_day_limits": limits}


def test_class_specific_daily_limits_are_respected():
    limits = {"1A": {"0": 6, "1": 6, "2": 7, "3": 6}, "1B": {"0": 8, "1": 8, "2": 8, "3": 8}}
    r = solve_timetable(_payload(limits, count=12))
    assert r["ok"], r
    for e in r["schedule"]:
        assert e["period"] <= limits[e["class"]][str(e["day"])]
    assert sum(1 for e in r["schedule"] if e["class"] == "1A") == 12


def test_over_capacity_for_short_class_is_reported():
    r = solve_timetable(_payload({"1A": {"0": 1, "1": 1, "2": 1, "3": 1}}, count=6))
    assert not r["ok"] and "1A" in r.get("details", {})


def test_no_limits_behaves_as_before():
    r = solve_timetable(_payload({}, count=10))
    assert r["ok"], r


def test_zero_day_for_class():
    r = solve_timetable(_payload({"1A": {"3": 0}}, count=10))
    assert r["ok"] and all(not (e["class"] == "1A" and e["day"] == 3) for e in r["schedule"])
