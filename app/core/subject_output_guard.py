"""Remove clear function-study contamination from unrelated student answers.

A response is not authorized for calculus merely because the model wrote
Domain/Limits. Authorization comes from the student's request or selected
Mathematics function chapter, using the same decision as visual routing.
"""
import re
from app.core.lesson_quality import drawing_matches_subject

_ORDERED_STUDY = re.compile(
    r"(?is)\bDomain\b[\s\S]{0,1100}?\bLimits?\b"
    r"[\s\S]{0,1100}?\bAsymptotes?\b"
    r"[\s\S]{0,1100}?\bDerivative\b"
)
_RESUME_LESSON = re.compile(
    r"(?im)(?:^|\\n)\\s*(?:#{1,6}\\s*)?"
    r"(?:Let's\\s+(?:complete|make\\s+sure|continue|review)|"
    r"Here\\s+is\\s+the\\s+complete|"
    r"Final\\s+Card|Practice\\s+Exercises|Quick\\s+Check|\\Z)"
)
_SECONDARY = re.compile(
    r"(?i)(?:الثانوي|ثانوي|secondary|secondaire|seconde|première|premiere|"
    r"terminale|grade\\s*1[012]|g\\.?\\s*1[012]|"
    r"الأول\\s+ثانوي|الثاني\\s+ثانوي|الثالث\\s+ثانوي)"
)


def permits_complete_function_study(
    subject: str, grade: str, lesson: str, message: str
) -> bool:
    """Complete calculus study is a SECONDARY MATHEMATICS lesson only."""
    is_math = bool(re.search(r"(?i)math|رياضيات", subject or ""))
    if not is_math or not _SECONDARY.search(grade or ""):
        return False
    return drawing_matches_subject(
        {"type": "function", "expression": "f(x)"}, subject, lesson, message
    )


def sanitize_unrelated_function_study(
    text: str, subject: str, lesson: str = "", message: str = "", grade: str = ""
) -> str:
    """Cut only a confirmed foreign Domain→Limits→Asymptotes→Derivative run.

    Avoid stripping isolated legitimate words such as the domain of a website,
    a physics limit, or a derivative genuinely requested by the student.
    """
    result = str(text or "")
    if permits_complete_function_study(subject, grade, lesson, message):
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
