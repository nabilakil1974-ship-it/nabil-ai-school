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

    tasks = []
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
        tasks.extend({"class": cls, "teacher": teacher, "subject": subject, "lesson": n + 1}
                     for n in range(count))

    per_class = Counter(t["class"] for t in tasks)
    capacity = len(days) * periods
    over = {c: n for c, n in per_class.items() if n > capacity}
    if over:
        return {"ok": False, "status": "infeasible", "message": "نصاب إحدى الشعب يتجاوز عدد خانات الدوام المتاحة.", "details": over}

    slots = [(d, p) for d in days for p in range(1, periods + 1)]
    candidates = []
    for task in tasks:
        valid = [(d, p) for d, p in slots if (task["teacher"], d, p) not in blocked]
        if not valid:
            return {"ok": False, "status": "infeasible", "message": "أحد المعلمين غير متاح في جميع الخانات المحددة."}
        candidates.append(valid)

    assigned: list[dict[str, Any] | None] = [None] * len(tasks)
    teacher_busy: set[tuple[str, int, int]] = set()
    class_busy: set[tuple[str, int, int]] = set()
    remaining = set(range(len(tasks)))
    nodes = 0
    node_limit = max(10000, min(int(payload.get("node_limit", 180000)), 500000))
    deadline = time.monotonic() + max(1.0, min(float(payload.get("time_limit_seconds", 8)), 15.0))
    timed_out = False

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
        for i in remaining:
            t = tasks[i]
            opts = [(d, p) for d, p in candidates[i]
                    if (t["teacher"], d, p) not in teacher_busy
                    and (t["class"], d, p) not in class_busy]
            if not opts:
                return False
            if best_options is None or len(opts) < len(best_options):
                best_i, best_options = i, opts
                if len(opts) == 1:
                    break
        t = tasks[best_i]
        # Prefer spreading the same class/subject over days, then earlier periods.
        def preference(slot):
            d, p = slot
            same_day = sum(1 for x in assigned if x and x["class"] == t["class"]
                           and x["subject"] == t["subject"] and x["day"] == d)
            return (same_day, p, d)
        best_options.sort(key=preference)
        remaining.remove(best_i)
        for d, p in best_options:
            nodes += 1
            teacher_key = (t["teacher"], d, p)
            class_key = (t["class"], d, p)
            teacher_busy.add(teacher_key)
            class_busy.add(class_key)
            assigned[best_i] = {**t, "day": d, "period": p}
            # Forward check: every remaining lesson must retain at least one legal slot.
            viable = True
            for j in remaining:
                u = tasks[j]
                if not any((u["teacher"], sd, sp) not in teacher_busy
                           and (u["class"], sd, sp) not in class_busy
                           for sd, sp in candidates[j]):
                    viable = False
                    break
            if viable and search():
                return True
            assigned[best_i] = None
            teacher_busy.remove(teacher_key)
            class_busy.remove(class_key)
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
            "requested_lessons": len(tasks), "search_nodes": nodes,
        }

    schedule = [x for x in assigned if x is not None]
    # Independent final audit; never report success if a hard constraint is violated.
    teacher_slots = [(x["teacher"], x["day"], x["period"]) for x in schedule]
    class_slots = [(x["class"], x["day"], x["period"]) for x in schedule]
    violations = []
    if len(teacher_slots) != len(set(teacher_slots)):
        violations.append("teacher_double_booking")
    if len(class_slots) != len(set(class_slots)):
        violations.append("class_double_booking")
    if any((x["teacher"], x["day"], x["period"]) in blocked for x in schedule):
        violations.append("teacher_unavailable")
    if len(schedule) != len(tasks):
        violations.append("missing_lessons")
    if violations:
        return {"ok": False, "status": "audit_failed", "message": "فشل التدقيق النهائي؛ لم يعتمد الجدول.", "violations": violations}

    return {
        "ok": True, "status": "success", "schedule": schedule,
        "requested_lessons": len(tasks), "scheduled_lessons": len(schedule),
        "search_nodes": nodes, "audit": {"passed": True, "violations": []},
        "message": "اكتمل توزيع جميع الحصص واجتاز التدقيق المستقل للقيود الصارمة.",
    }
