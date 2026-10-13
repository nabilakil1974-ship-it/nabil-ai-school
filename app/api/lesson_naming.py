"""Pure helpers: turn a Claude-factory Drive file name into what the student sees."""
import re

# G07-MATHEMATICS--<book hash>--<seq>--POWERS[--EXERCISES].html
FACTORY_FILE = re.compile(
    r"^G0?(\d{1,2})-([A-Za-z]+)--[0-9A-Fa-f]{6,10}--\d{2,3}--(.+?)(?:--EXERCISES)?$")


def factory_title(raw: str) -> str:
    text = re.sub(r"[-_]+", " ", raw).strip()
    return text.title() if text.isupper() else text


def parse_factory_filename(name: str):
    """Return {grade, subject, lesson, exercises} or None for non-factory names."""
    stem = name.rsplit(".", 1)[0]
    m = FACTORY_FILE.match(stem)
    if not m:
        return None
    return {"grade": m.group(1), "subject": m.group(2),
            "lesson": factory_title(m.group(3)),
            "exercises": stem.upper().endswith("--EXERCISES")}
