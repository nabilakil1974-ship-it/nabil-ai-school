"""Constraint-based school timetable generator for NABIL.

Uses bounded depth-first search with dynamic minimum-remaining-values selection.
A result is returned only after every requested lesson is assigned and independently audited.
"""
from __future__ import annotations

import time
from collections import Counter
from typing import Any


def solve_timetable(payload: dict[str, Any]) -> dict[str, Any]:
    days = list(dict.fromkeys(int(x) for x in payload.get("days", [])))
    periods = int(payload.get("periods", 0))
    raw_limits = payload.get("day_period_limits") or {}
    day_period_limits = {}
    for day in days:
        value = raw_limits.get(str(day), raw_limits.get(day, periods))
        try:
            day_period_limits[day] = max(1, min(periods, int(value)))
        except (TypeError, ValueError):
            day_period_limits[day] = periods
    raw_class_limits = payload.get("class_day_limits") or {}
    class_limits: dict[tuple[str, int], int] = {}
    if isinstance(raw_class_limits, dict):
        for cname, per_day in raw_class_limits.items():
            if not isinstance(per_day, dict):
                continue
            for day in days:
                value = per_day.get(str(day), per_day.get(day))
                if value in (None, ""):
                    continue
                try:
                    class_limits[(str(cname).strip(), day)] = max(0, min(day_period_limits[day], int(value)))
                except (TypeError, ValueError):
                    pass

    def cls_limit(cname: str, day: int) -> int:
        return class_limits.get((cname, day), day_period_limits.get(day, periods))

    teachers = {str(x).strip() for x in payload.get("teachers", []) if str(x).strip()}
    classes = {str(x).strip() for x in payload.get("classes", []) if str(x).strip()}
    requirements = payload.get("requirements") or []
    blocked = set()
    for item in payload.get("blocked", []) or []:
        blocked.add((str(item.get("teacher", "")).strip(), int(item.get("day")), int(item.get("period"))))

    if not days or periods < 1 or periods > 14 or not teachers or not classes or not requirements:
        return {"ok": False, "status": "invalid_input", "message": "أكمل أيام الدوام والحصص والمعلمين والشعب والأنصبة أولاً."}
    if len(days) > 7 or any(d < 0 or d > 6 for d in days):
        return {"ok": False, "status": "invalid_input", "message": "أيام الدوام غير صالحة."}

    try:
        break_after = int(payload.get("break_after_period") or 0)
    except (TypeError, ValueError):
        break_after = 0
    # Optional merged classes: some subjects are taught to several classes together
    # (one teacher, one slot, all those classes busy), while other subjects stay separate.
    merge_lookup: dict[tuple[str, str], int] = {}
    for mi, m in enumerate(payload.get("merges") or []):
        if not isinstance(m, dict):
            continue
        for mc in m.get("classes") or []:
            for ms in m.get("subjects") or []:
                merge_lookup[(str(mc).strip(), str(ms).strip())] = mi
    norm: list[dict[str, Any]] = []
    joint: dict[tuple[int, str, str], dict[str, Any]] = {}
    for req in requirements:
        cls = str(req.get("class", "")).strip()
        teacher = str(req.get("teacher", "")).strip()
        subject = str(req.get("subject", "")).strip()
        try:
            count = int(req.get("count", 0))
        except (TypeError, ValueError):
            count = 0
        if cls not in classes or teacher not in teachers or not subject or count < 1 or count > 60:
            return {"ok": False, "status": "invalid_input", "message": "يوجد نصاب غير صحيح أو مرتبط بمعلم/شعبة غير مسجلين."}
        try:
            doubles = int(req.get("double", 0) or 0)
        except (TypeError, ValueError):
            doubles = 0
        key = (merge_lookup[(cls, subject)], teacher, subject) if (cls, subject) in merge_lookup else None
        if key is None:
            norm.append({"classes": [cls], "teacher": teacher, "subject": subject, "count": count, "double": doubles})
        elif key in joint:
            j = joint[key]
            if j["count"] != count:
                return {"ok": False, "status": "invalid_input",
                        "message": "حصص مادة «" + subject + "» المدمجة للمعلم " + teacher + " يجب أن تكون متساوية في الصفوف المدمجة."}
            if cls not in j["classes"]:
                j["classes"].append(cls)
        else:
            joint[key] = {"classes": [cls], "teacher": teacher, "subject": subject, "count": count, "double": doubles}
            norm.append(joint[key])

    tasks = []
    group_counts: Counter[tuple[str, str, str]] = Counter()
    order_counts: Counter[tuple[str, str, str, int]] = Counter()
    for req in norm:
        cls_list = req["classes"]
        cls = " + ".join(cls_list)
        teacher, subject, count = req["teacher"], req["subject"], req["count"]
        group = (cls, teacher, subject)
        doubles = max(0, min(req["double"], count // 2))
        spans = [2] * doubles + [1] * (count - 2 * doubles)
        for span in spans:
            first = group_counts[group] + 1
            group_counts[group] += span
            order_counts[group + (span,)] += 1
            tasks.append({"class": cls, "classes": cls_list, "teacher": teacher, "subject": subject,
                          "lesson": first, "span": span,
                          "order": order_counts[group + (span,)]})

    total_lessons = sum(t["span"] * len(t["classes"]) for t in tasks)
    per_class = Counter()
    for t in tasks:
        for c in t["classes"]:
            per_class[c] += t["span"]
    over = {c: n for c, n in per_class.items() if n > sum(cls_limit(c, day) for day in days)}
    if over:
        return {"ok": False, "status": "infeasible", "message": "نصاب إحدى الشعب يتجاوز عدد خانات الدوام المتاحة.", "details": over}

    slots = [(d, p) for d in days for p in range(1, day_period_limits.get(d, periods) + 1)]
    candidates = []
    for task in tasks:
        span = task["span"]
        valid = []
        for d, p in slots:
            cells = [(d, p + k) for k in range(span)]
            if any(c[1] > cls_limit(cn, d) for c in cells for cn in task["classes"]):
                continue
            if span == 2 and break_after and p == break_after:
                continue  # never join two periods across the break
            if any((task["teacher"], dd, pp) in blocked for dd, pp in cells):
                continue
            valid.append((d, p))
        if not valid:
            if span == 2:
                return {"ok": False, "status": "infeasible",
                        "message": "لا توجد حصتان متتاليتان متاحتان للمعلم " + task["teacher"] +
                                   " في الشعبة " + task["class"] + " (مادة " + task["subject"] + ")؛ قلّل الحصص المتتالية أو غيّر أوقات التفرغ."}
            return {"ok": False, "status": "infeasible", "message": "أحد المعلمين غير متاح في جميع الخانات المحددة."}
        candidates.append(valid)

    assigned: list[dict[str, Any] | None] = [None] * len(tasks)
    teacher_busy: set[tuple[str, int, int]] = set()
    class_busy: set[tuple[str, int, int]] = set()
    remaining = set(range(len(tasks)))

    # Index identical lessons once. The previous symmetry check scanned every
    # task for every candidate slot, which made forward checking needlessly
    # expensive on schools with many repeated weekly lessons.
    identical_groups: dict[tuple[str, str, str], list[int]] = {}
    teacher_task_counts = Counter(t["teacher"] for t in tasks)
    class_task_counts: Counter[str] = Counter()
    for t in tasks:
        for cn in t["classes"]:
            class_task_counts[cn] += 1
    for index, task in enumerate(tasks):
        identity = (task["class"], task["teacher"], task["subject"], task["span"])
        identical_groups.setdefault(identity, []).append(index)
    nodes = 0
    node_limit = max(10000, min(int(payload.get("node_limit", 180000)), 500000))
    deadline = time.monotonic() + max(1.0, min(float(payload.get("time_limit_seconds", 8)), 15.0))
    timed_out = False

    def ordered_identical_slot(i: int, day: int, period: int) -> bool:
        task = tasks[i]
        slot = (day, period)
        identity = (task["class"], task["teacher"], task["subject"], task["span"])
        for j in identical_groups[identity]:
            if j == i or assigned[j] is None:
                continue
            other_slot = (assigned[j]["day"], assigned[j]["period"])
            if tasks[j]["order"] < task["order"] and other_slot >= slot:
                return False
            if tasks[j]["order"] > task["order"] and slot >= other_slot:
                return False
        return True

    def cells_free(task: dict[str, Any], day: int, period: int) -> bool:
        for k in range(task["span"]):
            if (task["teacher"], day, period + k) in teacher_busy or any((cn, day, period + k) in class_busy for cn in task["classes"]):
                return False
        return True

    def search() -> bool:
        nonlocal nodes, timed_out
        if not remaining:
            return True
        if nodes >= node_limit or time.monotonic() >= deadline:
            timed_out = True
            return False
        best_i = -1
        best_options = None
        # Dynamic MRV: select the unassigned lesson with the fewest currently legal slots.
        best_priority = None
        # Stable MRV tie-breaking: when two lessons have the same domain size,
        # schedule the lesson attached to the most constrained teacher/class
        # first. This avoids relying on set iteration order between runs.
        for i in sorted(remaining):
            t = tasks[i]
            opts = [(d, p) for d, p in candidates[i]
                    if cells_free(t, d, p)
                    and ordered_identical_slot(i, d, p)]
            if not opts:
                return False
            priority = (len(opts), -(teacher_task_counts[t["teacher"]] + max(class_task_counts[cn] for cn in t["classes"])), i)
            if best_priority is None or priority < best_priority:
                best_i, best_options, best_priority = i, opts, priority
                if len(opts) == 1:
                    break
        t = tasks[best_i]
        # Prefer spreading the same class/subject over days, then earlier periods.
        def preference(slot):
            d, p = slot
            same_day = sum(1 for x in assigned if x and x["classes"][0] == t["classes"][0]
                           and x["subject"] == t["subject"] and x["day"] == d)
            return (same_day, p, d)
        best_options.sort(key=preference)
        remaining.remove(best_i)
        for d, p in best_options:
            nodes += 1
            teacher_keys = [(t["teacher"], d, p + k) for k in range(t["span"])]
            class_keys = [(cn, d, p + k) for k in range(t["span"]) for cn in t["classes"]]
            teacher_busy.update(teacher_keys)
            class_busy.update(class_keys)
            assigned[best_i] = {**t, "day": d, "period": p}
            # Forward check: every remaining lesson must retain at least one legal slot.
            viable = True
            for j in remaining:
                u = tasks[j]
                if not any(cells_free(u, sd, sp)
                           and ordered_identical_slot(j, sd, sp)
                           for sd, sp in candidates[j]):
                    viable = False
                    break
            if viable and search():
                return True
            assigned[best_i] = None
            teacher_busy.difference_update(teacher_keys)
            class_busy.difference_update(class_keys)
            if timed_out:
                break
        remaining.add(best_i)
        return False

    solved = search()
    if not solved:
        return {
            "ok": False,
            "status": "search_limit" if timed_out else "infeasible",
            "message": ("بلغ البحث الحد الزمني/الحسابي دون إثبات حل؛ خفّف القيود أو أعد المحاولة."
                        if timed_out else "لم يوجد توزيع يحقق جميع الأنصبة والقيود المحددة."),
            "requested_lessons": total_lessons, "search_nodes": nodes,
        }

    schedule = []
    for x in assigned:
        if x is None:
            continue
        for k in range(x["span"]):
            for cn in x["classes"]:
                entry = {"class": cn, "teacher": x["teacher"], "subject": x["subject"],
                         "lesson": x["lesson"] + k, "day": x["day"], "period": x["period"] + k}
                if x["span"] == 2:
                    entry["double"] = True
                if len(x["classes"]) > 1:
                    entry["merged_with"] = [c for c in x["classes"] if c != cn]
                schedule.append(entry)
    # Independent final audit; never report success if a hard constraint is violated.
    teacher_slots = [(x["teacher"], x["day"], x["period"] + k) for x in assigned if x is not None for k in range(x["span"])]
    class_slots = [(x["class"], x["day"], x["period"]) for x in schedule]
    violations = []
    if len(teacher_slots) != len(set(teacher_slots)):
        violations.append("teacher_double_booking")
    if len(class_slots) != len(set(class_slots)):
        violations.append("class_double_booking")
    if any(slot in blocked for slot in teacher_slots):
        violations.append("teacher_unavailable")
    if any(x["period"] > cls_limit(x["class"], x["day"]) for x in schedule):
        violations.append("outside_daily_period_limit")
    if len(schedule) != total_lessons:
        violations.append("missing_lessons")
    # Every requested double must really be two consecutive periods of one class on one day.
    for x in assigned:
        if x is not None and x["span"] == 2:
            pair = [(s["day"], s["period"]) for s in schedule
                    if s["class"] == x["classes"][0] and s["teacher"] == x["teacher"]
                    and s["subject"] == x["subject"] and s.get("double")
                    and s["lesson"] in (x["lesson"], x["lesson"] + 1)]
            if len(pair) != 2 or pair[0][0] != pair[1][0] or abs(pair[0][1] - pair[1][1]) != 1:
                violations.append("double_not_consecutive")
            elif break_after and min(pair[0][1], pair[1][1]) == break_after:
                violations.append("double_across_break")
    if violations:
        return {"ok": False, "status": "audit_failed", "message": "فشل التدقيق النهائي؛ لم يعتمد الجدول.", "violations": violations}

    return {
        "ok": True, "status": "success", "schedule": schedule,
        "requested_lessons": total_lessons, "scheduled_lessons": len(schedule),
        "search_nodes": nodes, "audit": {"passed": True, "violations": []},
        "message": "اكتمل توزيع جميع الحصص واجتاز التدقيق المستقل للقيود الصارمة.",
    }
