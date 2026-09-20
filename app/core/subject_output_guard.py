"""Remove clear function-study contamination from unrelated student answers.

A response is not authorized for calculus merely because the model wrote
Domain/Limits. Authorization comes from the student's request or selected
Mathematics function chapter, using the same decision as visual routing.
"""
import re
from app.core.lesson_quality import drawing_matches_subject

_CALCULUS_START = re.compile(r"(?i)\bDomain\s*(?:\(?\s*0\s*[,،]|[:：]|\b)")
_ORDERED_STUDY = re.compile(
    r"(?is)\bDomain\b[\s\S]{0,1100}?\bLimits?\b"
    r"[\s\S]{0,1100}?\bAsymptotes?\b"
    r"[\s\S]{0,1100}?\bDerivative\b"
)
_RESUME_LESSON = re.compile(
    r"(?im)(?=Let's\s+(?:complete|make\s+sure|continue|look|review)|"
    r"Here\s+is\s+the\s+complete|"
    r"(?=^\s*#{1,6}\s*(?!Domain\b|Limits?\b|Asymptotes?\b|Derivative\b))"
    r"|Final\s+Card\s*[—:-]|Practice\s+Exercises\s*:|\Z)"
)


def sanitize_unrelated_function_study(
    text: str, subject: str, lesson: str = "", message: str = ""
) -> str:
    """Cut only a confirmed foreign Domain→Limits→Asymptotes→Derivative run.

    Avoid stripping isolated legitimate words such as the domain of a website,
    a physics limit, or a derivative genuinely requested by the student.
    """
    result = str(text or "")
    if drawing_matches_subject(
        {"type": "function", "expression": "f(x)"}, subject, lesson, message
    ):
        return result
    for _ in range(5):
        sequence = _ORDERED_STUDY.search(result)
        if not sequence:
            break
        start = sequence.start()
        # Preserve scientific prose preceding a contaminated inline segment.
        end_match = _RESUME_LESSON.search(result, sequence.end())
        end = end_match.start() if end_match else len(result)
        if end <= start:
            break
        result = result[:start].rstrip() + "\n\n" + result[end:].lstrip()
    return re.sub(r"\n{3,}", "\n\n", result).strip()
