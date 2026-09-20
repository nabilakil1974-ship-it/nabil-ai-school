"""Small deterministic pre-delivery gate for EXACT printed textbook pages.

Only inspect content against the indexed page(s). A rejected answer is regenerated
once from the same sources rather than silently publishing made-up book content.
This is not an OCR/figure vision substitute or a universal fact checker.
"""
import re

_MATH_HEADER = re.compile(
    r"(?im)^\s*#{1,5}\s*(?:Domain|Limits?|Asymptotes?|Derivative|"
    r"Variation\s+table|Domaine|Limites?|Dérivée|Tableau\s+de\s+variations)"
    r"\b"
)
_BOOK_FIG = re.compile(
    r"(?i)\b(?:fig(?:ure)?\.?\s*|الشكل\s*رقم\s*)(\d{1,3})\b"
)
_BOOK_ACTIVITY = re.compile(
    r"(?i)\b(?:activity|activité|نشاط)\s*(\d{1,3})\b"
)
_GRADE9_CHEM = re.compile(r"chem|chimie|كيمياء", re.I)


def lesson_page_issues(
    reply: str, indexed_text: str, *, subject: str,
    printed_page: int, strict_single_page: bool = True,
) -> list[str]:
    """Identify high-confidence source mismatch and objective scientific errors.

    Page-56 chemistry checks are specific regression invariants; other pages
    receive general source-figure/activity and math-leak checks.
    """
    answer = str(reply or "")
    source = str(indexed_text or "")
    issues = []
    if not answer.strip():
        return ["empty lesson"]
    if _GRADE9_CHEM.search(subject or ""):
        if _MATH_HEADER.search(answer):
            issues.append("math function-study headings in a chemistry lesson")
        if re.search(r"(?i)\bO(?:\^?\{?2\+?[-⁻−]\}?|²⁻)[^\n]{0,70}"
                     r"(?:configuration|arrangement|after)\s*[:=]?\s*(?:2\s*,\s*8\s*,\s*8|"
                     r"K\^?2\s*,?\s*L\^?8\s*,?\s*M\^?8)", answer):
            issues.append("oxide O2- has 10 electrons, not 18")
        if re.search(
            r"(?i)\\b(?:fluorine|fluor|fluorure|الفلور)\\b[^\\n]{0,140}"
            r"(?:\\[\\s*Ne\\s*\\]\\s*2s\\s*[²2]\\s*2p\\s*[⁵5]|"
            r"\\bNe\\s+2s\\s*[²2]\\s*2p\\s*[⁵5])",
            answer,
        ):
            issues.append("neutral fluorine is [He]2s2 2p5, not [Ne]2s2 2p5")
        # The order 2,6,8 is not a valid neutral oxygen arrangement (8 e-).
        if re.search(r"(?i)oxygen.{0,105}?(?:configuration|arrangement)"
                     r"[^\n]{0,25}(?:2\s*,\s*6\s*,\s*8|K\^?2\s*,?\s*L\^?6\s*,?\s*M\^?8)", answer):
            issues.append("neutral oxygen has electron arrangement 2,6")
        if re.search(r"(?is)\bHCl\b.{0,550}?(?:solid|melting\s+point)"
                     r".{0,130}?(?:ionic\s+solid|high\s+melting\s+point|high\s+mp)", answer):
            issues.append("HCl is molecular; aqueous conductivity is not evidence of ionic solid")
    if strict_single_page:
        src_figs = set(_BOOK_FIG.findall(source))
        src_acts = set(_BOOK_ACTIVITY.findall(source))
        for n in set(_BOOK_FIG.findall(answer)):
            if n not in src_figs:
                issues.append(f"unsupported original textbook figure {n}")
        for n in set(_BOOK_ACTIVITY.findall(answer)):
            if n not in src_acts:
                issues.append(f"unsupported original textbook activity {n}")
    # The actual photographed Grade 9 chemistry p.56: NaCl plus the START of
    # MgF2. Do not mistake an unrelated chapter survey for this one-page lesson.
    if strict_single_page and printed_page == 56 and _GRADE9_CHEM.search(subject or ""):
        if all(t in source.lower() for t in ("sodium", "chlorine", "magnesium", "fluor")):
            if not re.search(r"(?i)\bMgF\s*(?:_?2|₂)\b|magnesium\s+fluoride", answer):
                issues.append("missing magnesium fluoride section actually on printed p.56")
            if not re.search(r"(?i)\bNaCl\b|sodium\s+chloride", answer):
                issues.append("missing sodium chloride section actually on printed p.56")
            if re.search(r"(?i)\b(?:conductivity\s+test|salt\s+vs\s+sugar|"
                         r"NaCl\s+vs\s+sugar)\b", answer):
                issues.append("unverified conductivity activity displaced page-56 bonding sequence")
    if strict_single_page and printed_page == 57 and _GRADE9_CHEM.search(subject or ""):
        # Enforce only when these headings were actually indexed in the page;
        # this rule never extrapolates page 57 to some other book or subject.
        src_low = source.casefold()
        ans_low = answer.casefold()
        if "crystal lattice" in src_low:
            if "crystal lattice" not in ans_low:
                issues.append("missing crystal lattice, the actual page-57 section")
            if "fig. 14" in src_low or "fig 14" in src_low:
                if not re.search(r"(?i)\\bfig(?:ure)?\\.?\\s*14\\b", answer):
                    issues.append("missing source Fig. 14 when page 57 explicitly includes it")
        if "build using ball" in src_low and ("activity 2" in ans_low or "activité 2" in ans_low):
            # The book asks the learner to CONSTRUCT a lattice using models,
            # not to identify lattice type from a unit cell on the next page.
            if not re.search(r"(?i)ball.and.stick|build\\s+(?:using|a)|"
                             r"model(?:s|ling)?\\s+clay|toothpick|"
                             r"كرات|أعواد|صلصال|نماذج|بناء", answer):
                issues.append("Activity 2 on p57 is ball-and-stick lattice construction")
    # Repeated full-start headings indicate the model restarted its response.
    starts = re.findall(r"(?im)^\s*#{1,3}\s*(?:lesson\s*[:—-]|"
                        r"interactive\s+lesson\s*[:—-])", answer)
    if len(starts) > 1:
        issues.append("lesson restarted in one response")
    return list(dict.fromkeys(issues))
