"""Source completeness inventory for NABIL lesson production.

Completeness is tracked independently from generation. Verified source items may
ship immediately; unresolved items are recorded in a durable backlog and retried
later. Nothing unresolved is invented or rendered to students.
"""
import re


def _inventory_norm(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip().casefold()


def build_independent_source_inventory(ev_map: dict) -> dict:
    """Inventory explicit source objects independently of generated pedagogy."""
    exercise_numbers, figure_labels = set(), set()
    for page in ev_map.get("pages_evidence") or []:
        text = str(page.get("text") or "")
        for m in re.finditer(
                r"(?im)(?:^|\n)\s*(?:(?:problem|exercise|problème|exercice|تمرين|مسألة)\s*)?(\d+)\s*[.\-)]+\s+",
                text):
            exercise_numbers.add(m.group(1))
        for m in re.finditer(r"(?i)\bfig(?:ure)?\.?\s*(\d+[a-z]?)", text):
            figure_labels.add(m.group(1).casefold())
    return {
        "exercise_numbers": sorted(
            exercise_numbers,
            key=lambda x: int(re.match(r"\d+", x).group())),
        "figure_labels": sorted(figure_labels),
    }


def attach_and_verify_source_completeness(ev_map: dict) -> dict:
    """Attach COMPLETE or DEFERRED status without blocking verified production."""
    inventory = build_independent_source_inventory(ev_map)
    accepted_ex = {
        str(x.get("number"))
        for x in ev_map.get("exercise_evidence") or []
    }
    accounted_figs = set()
    for page in ev_map.get("pages_evidence") or []:
        for fig in page.get("figures") or []:
            for value in (fig.get("printed_label"), fig.get("printed_number")):
                if value is not None and str(value).strip():
                    accounted_figs.add(str(value).strip().casefold())
        accounted_figs |= {
            str(x).strip().casefold()
            for x in (page.get("skipped_unverified_figure_labels") or [])
        }
        accounted_figs |= {
            str(x).strip().casefold()
            for x in (page.get("required_unverified_figure_labels") or [])
        }

    disproved_ex = {
        str(x) for x in (ev_map.get("disproved_exercise_numbers") or [])
    }
    missing_ex = sorted(
        set(inventory["exercise_numbers"]) - accepted_ex - disproved_ex)
    missing_fig = sorted(set(inventory["figure_labels"]) - accounted_figs)
    complete = not missing_ex and not missing_fig
    report = {
        "passed": complete,
        "status": "COMPLETE" if complete else "DEFERRED",
        "blocking": False,
        "inventory": inventory,
        "missing_exercise_numbers": missing_ex,
        "disproved_exercise_numbers": sorted(disproved_ex),
        "missing_figure_labels": missing_fig,
        "backlog_persisted": bool(ev_map.get("source_backlog_persisted")) or complete,
    }
    ev_map["source_inventory"] = inventory
    ev_map["source_completeness"] = report
    return report
