"""Shared helpers for direct lesson modules (data -> V6 scenes)."""
from __future__ import annotations

def T(en, ar, fr, label=None):
    return {"k": "t", "en": en, "ar": ar, "fr": fr, "label": label}


def F(f):
    return {"k": "f", "f": f}


def D(name, **args):
    return {"k": "d", "draw": name, "args": args}



def EX(n, page, stmt, steps):
    return {"n": n, "page": page, "stmt": stmt, "steps": steps}


def st(en, ar, fr):
    return (en, ar, fr)


S = T


def _step(x):
    if x["k"] == "t":
        d = {"t": "text", "text": x["en"], "label": x.get("label") or "", "speech": x["en"],
             "ar": x["ar"], "en": x["en"], "fr": x["fr"]}
        return d
    if x["k"] == "f":
        return {"t": "formula", "text": x["f"]}
    return {"t": "draw", "draw": x["draw"], "args": x.get("args", {})}


def make_scenes(THEORY, EXERCISES):
    out = []
    for i, (te, ta, tf, page, steps) in enumerate(THEORY, 1):
        out.append({"id": f"P{i}", "page": page, "title": te, "title_en": te, "title_ar": ta, "title_fr": tf,
                    "start_mode": "single", "steps": [_step(s) for s in steps]})
    for e in EXERCISES:
        en, ar, fr = e["stmt"]
        label = {"en": "Exercise", "ar": "التمرين", "fr": "Exercice"}
        steps = [{"t": "text", "text": en, "label": "Problem", "speech": en, "ar": ar, "en": en, "fr": fr}]
        steps += [_step(s) for s in e["steps"]]
        out.append({"id": f"EX-{e['n']}", "page": e["page"], "exercise": e["n"], "solved": True,
                    "title": f"Exercise {e['n']}", "title_en": f"Exercise {e['n']}",
                    "title_ar": f"التمرين {e['n']}", "title_fr": f"Exercice {e['n']}",
                    "start_mode": "single", "steps": steps})
    return out
