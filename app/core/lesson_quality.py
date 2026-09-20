"""Deterministic lesson output contracts, shared across subjects and languages.

Only the supplied lesson content is inspected here. Never infer textbook pages.
"""
import re

_PRACTICE_HEADER = re.compile(
    r"(?im)^\\s*#{2,4}\\s*(?:\\*\\*)?\\s*"
    r"(?:Exercise|Exercice|تمرين)\\s*(?:#\\s*)?([1-9]\\d*)\\b"
)

def practice_exercise_numbers(text: str, required_count: int = 5) -> list[int]:
    """Recognise H2/H3/H4 practice headings without treating prose as an exercise.

    H3 headings in real Chemistry lessons previously triggered a second full
    provider generation because a former counter recognised only H2.
    """
    return sorted({
        int(m.group(1)) for m in _PRACTICE_HEADER.finditer(text or "")
        if 1 <= int(m.group(1)) <= required_count
    })


def missing_practice_exercises(text: str, required_count: int = 5) -> list[int]:
    present = set(practice_exercise_numbers(text, required_count))
    return [n for n in range(1, required_count + 1) if n not in present]


_MATH_VISUAL_TYPES = frozenset({
    "function", "graph", "coordinate_plane", "analytic_plane",
    "orthonormal_plane", "orthonormal_system", "vector_plane",
})


def drawing_matches_subject(drawing: dict, subject: str, lesson: str = "") -> bool:
    """Fail closed on a function plot leaked into an unrelated selected subject.

    Does not prohibit coordinate systems in Physics: only the well-identified
    chemical ionic lesson leakage is rejected and mathematics remains unaffected.
    """
    if not isinstance(drawing, dict):
        return False
    selected = str(subject or "").casefold()
    chapter = str(lesson or "").casefold()
    chemistry = any(s in selected for s in ("chem", "chimie", "كيمياء"))
    ionic = any(s in chapter for s in ("ionic", "ionique", "أيون"))
    return not (chemistry and ionic and
                str(drawing.get("type") or "").lower() in _MATH_VISUAL_TYPES)
