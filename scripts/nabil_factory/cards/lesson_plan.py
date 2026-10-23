"""Lesson-plan (تحضير الدرس) DATA for the Golden V6 board.

Built once per lesson, from the lesson's REAL content only: the idea titles and
steps the board teaches, the book pages those ideas came from, the textbook
exercises (number + page when the source gives one), the formative questions and
the verified key results. Nothing is invented: every field the lesson data does
not contain (school, teacher, date, class, official competencies, prior learning)
stays an empty, editable field for the teacher.

The browser renders the plan in AR / EN / FR, lets the teacher change the period
length and number of periods, and exports a .docx (assets/golden_v6_plan.js).
"""
from __future__ import annotations

import hashlib
import re
from typing import Any, Dict, List


def lesson_id_for(title: str, meta: dict | None) -> str:
    lid = str((meta or {}).get("lesson_id") or "").strip()
    return lid or "LOCAL-" + hashlib.sha1(str(title).encode("utf-8")).hexdigest()[:10].upper()


def build_plan_data(title: str, scenes: List[dict], golden: dict | None, mode: str,
                    meta: dict | None = None) -> Dict[str, Any]:
    meta = dict(meta or {})
    ideas: List[dict] = []
    exercises: List[dict] = []
    checks: List[str] = []
    for sc in scenes:
        if sc.get("exercise"):
            exercises.append({"n": str(sc["exercise"]), "page": str(sc.get("page") or ""),
                              "solved": bool(sc.get("solved")),
                              "statement": next((s["text"] for s in sc["steps"] if s.get("t") == "text"), "")})
            continue
        steps = [s["text"] for s in sc.get("steps", []) if s.get("t") == "text" and s.get("text")]
        formulas = [s["text"] for s in sc.get("steps", []) if s.get("t") == "formula" and s.get("text")]
        for s in sc.get("steps", []):
            if s.get("t") == "check" and isinstance(s.get("check"), dict) and s["check"].get("question"):
                checks.append(str(s["check"]["question"]))
        ideas.append({"title": str(sc.get("title") or ""), "page": str(sc.get("page") or ""),
                      "steps": steps[:8], "formulas": formulas[:6],
                      "has_drawing": any(s.get("t") == "draw" for s in sc.get("steps", []))})
    # twins: primary text -> same text in ar/en/fr, so the plan follows the language chosen on the board
    tw: Dict[str, Dict[str, str]] = {"ar": {}, "en": {}, "fr": {}}
    for sc in scenes:
        for lg in tw:
            if sc.get("title") and sc.get("title_" + lg):
                tw[lg][str(sc["title"])] = str(sc["title_" + lg])
        for st in sc.get("steps", []):
            if st.get("t") in ("text", "formula") and st.get("text"):
                for lg in tw:
                    if isinstance(st.get(lg), str) and st[lg]:
                        tw[lg][str(st["text"])] = st[lg]
    golden = golden or {}
    return {
        "tw": tw,
        "lesson_id": lesson_id_for(title, meta), "title": title, "mode": mode,
        "subject": str(meta.get("subject") or ""), "grade": str(meta.get("grade") or ""),
        "source_lang": str(meta.get("language") or ""),
        "ideas": ideas, "exercises": exercises, "checks": checks[:6],
        "key_results": [str(x) for x in (golden.get("key_results") or [])][:8],
        "pages": sorted({i["page"] for i in ideas if i["page"]} | {e["page"] for e in exercises if e["page"]}),
        "crdp_verified": False,
    }
