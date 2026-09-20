"""Subject-scoped, conservative output sanitation for textbook chemistry lessons.

Only remove protocol leaks and a clearly foreign function-study insert.
Never infer a book page, exercise, or diagram from these transformations.
"""
import re

_CHEMISTRY = re.compile(r"chem|chimie|كيمياء", re.I)
_MATH_SECTION = re.compile(
    r"(?i)(?:^|\n)\s*(?:#{1,4}\s*)?Domain\s*\(?0\s*,\s*∞\)?"
    r"[\s\S]*?(?=(?:Board Lesson:|Interactive Board Lesson:|Practice Exercises:|Final Card\s*[—:-]|\Z))"
)
# Remove entire foreign function-study tail after a chemistry notebook summary.
_FOREIGN_MATH_TAIL = re.compile(
    r"(?im)^\\s*#{1,5}\\s*(?:Domain|Limits?|Asymptotes?|Derivative|"
    r"Variation\\s+Table|Domaine|Limites?|Dérivée)\\s*$"
)
_BAD_DRAWING_FENCE = re.compile(r"```\s*DRAWING_JSON\b[\s\S]*?```", re.I)
_OXYGEN_ION = re.compile(
    r"(?i)(?P<prefix>O\s*(?:²⁻|2\s*[-−⁻])[^\n•]{0,55}?"
    r"(?:arrangement|configuration|electronic\s+structure)\s*[:=]?\s*)"
    r"(?:K\s*2\s*L\s*8\s*M\s*8|2\s*[,،]\s*8\s*[,،]\s*8)"
)


def sanitize_chemistry_lesson(text: str, subject: str) -> str:
    """Remove malformed internal transport and verified cross-subject leakage."""
    if not _CHEMISTRY.search(subject or ""):
        return text
    result = _BAD_DRAWING_FENCE.sub("", text or "")
    # The Ionic Bond sample contained a whole injected function study between
    # chemistry sections. Never apply this cut to mathematics content.
    result = _MATH_SECTION.sub("\n", result)
    math_tail = _FOREIGN_MATH_TAIL.search(result)
    if math_tail:
        # Preserve later chemistry when the foreign block was inserted mid-lesson.
        follow = re.search(
            r"(?im)^\\s*#{1,4}\\s*(?:Electron\\s+configurations?|"
            r"Ionic\\s+bond|Crystal\\s+lattice|"
            r"Activity\\s+\\d+|Exercise\\s+\\d+|"
            r"Magnesium\\s+fluoride|Sodium\\s+chloride|"
            r"ملخص\\s+الدرس|التمارين|الرابطة|"
            r"Résumé\\s+pour\\s+le\\s+cahier)",
            result[math_tail.end():],
        )
        if follow:
            result = (result[:math_tail.start()] + "\\n" +
                      result[math_tail.end() + follow.start():])
        else:
            result = result[:math_tail.start()]

    # Oxide has 8 protons and 10 electrons: two filled shells, NOT three.
    result = _OXYGEN_ION.sub(lambda m: m.group("prefix") + "2,8", result)
    return re.sub(r"\n{3,}", "\n\n", result).strip()
