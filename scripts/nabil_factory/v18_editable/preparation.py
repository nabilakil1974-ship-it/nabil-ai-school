"""V18 structured lesson preparation from audited textbook concept narratives.

No invented curriculum objectives. Teaching follows explanation, exploration,
observation, interpretation, conclusion, guided application, and assessment.
"""
from __future__ import annotations

CONFIG = {"teacher_objectives": True, "prerequisites": True,
          "activities": True, "guided_practice": True,
          "formative_assessment": True, "final_summary": True,
          "format_version": "v18"}

def prepare_verified_lesson(theory):
    if not isinstance(theory, dict):
        raise ValueError("V18_THEORY_DATA_REQUIRED")
    activities = theory.get("activities") or []
    if not activities:
        raise RuntimeError("V18_NO_VERIFIED_CONCEPTS")
    plan = []
    for activity in activities:
        concept_id = str(activity.get("concept_id") or "")
        narration = []
        for part in ("phenomenon", "investigation", "observation",
                     "interpretation", "conclusion"):
            value = str(activity.get(part) or "").strip()
            if value:
                narration.append({"phase": part, "text": value})
        for step in activity.get("teaching_steps") or ():
            phrase = str(step.get("sentence") or "").strip()
            if phrase:
                narration.append({"phase": str(step.get("label") or "explain"),
                                  "text": phrase,
                                  "formula": str(step.get("formula") or "")})
        if not narration:
            raise RuntimeError("V18_TEACHER_EXPLANATION_MISSING:" + concept_id)
        apply = activity.get("student_apply_prompt") or {}
        plan.append({
            "concept_id": concept_id,
            "title": str(activity.get("title") or ""),
            "narration": narration,
            "lab_html": str(activity.get("lab_html") or ""),
            "guided_application": str(apply.get("prompt") or ""),
            "formative_question": activity.get("student_question") or {},
        })
    return {"title": str(theory.get("title") or ""),
            "concepts": plan,
            "assessment_after_explanation": True,
            "golden_card_last": True}

__all__ = ["CONFIG", "prepare_verified_lesson"]
