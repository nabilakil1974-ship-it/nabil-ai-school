"""Source completeness inventory/gate for NABIL lesson production.

This module is intentionally independent from rendering, providers and Drive.
It only compares source-page evidence with verified extracted evidence.
"""
import json
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
    """Require every explicit source exercise/figure reference to be accounted for."""
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

    missing_ex = sorted(set(inventory["exercise_numbers"]) - accepted_ex)
    missing_fig = sorted(set(inventory["figure_labels"]) - accounted_figs)
    report = {
        "passed": not missing_ex and not missing_fig,
        "inventory": inventory,
        "missing_exercise_numbers": missing_ex,
        "missing_figure_labels": missing_fig,
    }
    ev_map["source_inventory"] = inventory
    ev_map["source_completeness"] = report
    if not report["passed"]:
        raise RuntimeError(
            "SOURCE_COMPLETENESS_GATE_FAILED:"
            + json.dumps(report, ensure_ascii=False))
    return report
