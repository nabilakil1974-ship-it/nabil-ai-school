"""Deterministic lesson output contracts, shared across subjects and languages.

Only the supplied lesson content is inspected here. Never infer textbook pages.
"""
import re

_PRACTICE_HEADER = re.compile(
    r"(?im)^\s*#{2,4}\s*(?:\*\*)?\s*"
    r"(?:Exercise|Exercice|تمرين)\s*(?:#\s*)?([1-9]\d*)\b"
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


# A function-study diagram is never a default illustration for a lesson.
# Physical graphs and geometry constructions have different learning intents.
_FUNCTION_TYPES = frozenset({"function", "graph"})
_PLANE_TYPES = frozenset({
    "coordinate_plane", "analytic_plane", "orthonormal_plane",
    "orthonormal_system", "vector_plane",
})
_FUNCTION_REQUEST = re.compile(
    r"(?i)(?:\\b(?:study|analyse|analyze|plot|graph|sketch|draw|trace)\\b"
    r"[^\\n]{0,90}\\b(?:the\\s+)?function\\b|"
    r"\\b(?:function|fonction)\\s+study\\b|"
    r"\\b(?:study|graph|plot|draw)\\b[^\\n]{0,90}f\\s*\\(\\s*x\\s*\\)\\s*=|"
    r"\\b(?:étudier|etudier|tracer|dessiner|analyser)\\b[^\\n]{0,90}"
    r"(?:fonction|f\\s*\\(\\s*x\\s*\\))|"
    r"دراسة\\s*الدال|ادرس\\s*الدال|ارسم\\s*الدال|"
    r"جدول\\s*التغي|tableau\\s+de\\s+variations)"
)
_FUNCTION_CHAPTER = re.compile(
    r"(?i)\\b(?:functions?|fonctions?|variation\\s+of\\s+a\\s+function|"
    r"study\\s+of\\s+(?:a\\s+)?function)\\b|دوال|الدوال|الدالة"
)
_PLOT_MARKERS = ("function", "expression", "vertical_asymptote",
                 "vertical_asymptotes", "horizontal_asymptote",
                 "oblique_asymptote", "derivative", "variation_table")


def drawing_matches_subject(
    drawing: dict, subject: str, lesson: str = "", message: str = ""
) -> bool:
    """Reject function-study figures outside a real function-study request.

    The subject alone cannot authorize f(x): even a Mathematics geometry or
    statistics lesson must not inherit a generic derivative/limits plot.
    Conversely, a learner's explicit function question works in open chat.
    Ordinary Physics/Geography data charts and Math coordinate geometry stay
    available; they do not masquerade as a function-study diagram.
    """
    if not isinstance(drawing, dict):
        return False
    kind = str(drawing.get("type") or "").casefold()
    if kind not in _FUNCTION_TYPES | _PLANE_TYPES:
        return True
    selected = str(subject or "").casefold()
    is_math = any(t in selected for t in ("math", "رياضيات"))
    explicit_function = bool(_FUNCTION_REQUEST.search(message or ""))
    chapter_is_function = is_math and bool(_FUNCTION_CHAPTER.search(lesson or ""))
    function_intent = explicit_function or chapter_is_function
    has_function_data = any(drawing.get(key) is not None for key in _PLOT_MARKERS)
    if kind == "function" or (kind == "graph" and has_function_data):
        return function_intent
    if kind in _PLANE_TYPES:
        # A coordinate-plane diagram can be valid in geometry or mechanics,
        # but not when an unrequested function/variation plot is attached.
        if has_function_data:
            return function_intent
        if is_math or explicit_function:
            return True
        # Don't silently include blank coordinate planes in unrelated lessons.
        context = (str(lesson or "") + " " + str(message or "")).casefold()
        return bool(re.search(
            r"(?i)\\b(?:coordinates?|vectors?|cartesian|axes|force|motion|"
            r"velocity|position|displacement|graph|plot|chart|statistics|"
            r"tracer|repère|coordonnées|vecteurs?)\\b|إحداثيات|محاور|متجه|"
            r"رسم بياني|سرعة|إزاحة", context
        ))
    # A real labelled chart should not be confused with a derivative plot.
    return True
