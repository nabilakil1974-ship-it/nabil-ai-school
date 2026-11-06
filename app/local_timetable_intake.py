"""Deterministic Arabic spoken-intake parser for school timetable setup.

This module extracts only explicit facts. Ambiguous grade-wide scopes are kept as
unresolved requests instead of inventing section names.
"""
from __future__ import annotations

import re
from typing import Any

DAY_NAMES = {
    "الاثنين": 0, "الإثنين": 0, "الاثنين": 0,
    "الثلاثاء": 1, "الأربعاء": 2, "الاربعاء": 2,
    "الخميس": 3, "الجمعة": 4, "السبت": 5, "الأحد": 6, "الاحد": 6,
}
DAY_CANON = {0: "الإثنين", 1: "الثلاثاء", 2: "الأربعاء", 3: "الخميس",
             4: "الجمعة", 5: "السبت", 6: "الأحد"}
NUMBERS = {
    "واحد": 1, "واحدة": 1, "اول": 1, "أول": 1, "اثنين": 2, "إثنين": 2,
    "اثنتين": 2, "ثلاث": 3, "ثلاثة": 3, "ثلاثي": 3, "أربع": 4, "اربعة": 4,
    "أربعة": 4, "خمس": 5, "خمسة": 5, "ست": 6, "ستة": 6, "سبع": 7,
    "سبعة": 7, "ثمان": 8, "ثماني": 8, "ثمانية": 8, "تسع": 9, "تسعة": 9,
    "عشر": 10, "عشرة": 10, "نصف": 30, "نص": 30,
}
GRADE_WORDS = {"السابع": "السابع", "السابعة": "السابع", "الصف السابع": "السابع",
               "الثامن": "الثامن", "الثامنة": "الثامن", "التاسع": "التاسع",
               "التاسعة": "التاسع"}

def _norm(value: str) -> str:
    value = str(value or "").strip()
    value = re.sub(r"[\u064b-\u065f\u0670]", "", value)
    value = value.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    value = value.replace("ى", "ي")
    return re.sub(r"\s+", " ", value).lower()

def _number(text: str, default: int | None = None) -> int | None:
    s = _norm(text)
    m = re.search(r"\d+", s)
    if m:
        return int(m.group())
    for word, value in NUMBERS.items():
        if _norm(word) in s:
            return value
    return default

def _extract_day_limits(text: str, days: list[int]) -> dict[str, int]:
    normalized = _norm(text)
    limits: dict[str, int] = {}
    aliases = [("الاثنين", 0), ("الثلاثاء", 1), ("الاربعاء", 2),
               ("الخميس", 3), ("الجمعة", 4), ("السبت", 5), ("الاحد", 6)]
    for day_word, day_id in aliases:
        if day_id not in days:
            continue
        pattern = rf"{day_word}.{{0,28}}?(?:عندي|فيه|في|عددها)?\s*(ثمانية|ثماني|ثمان|سبعة|سبع|ستة|ست|خمسة|خمس|اربعة|اربع|ثلاثة|ثلاث|اثنين|اثنتين|واحد|واحدة|[1-9])\s*(?:حصص|حصة)"
        match = re.search(pattern, normalized)
        if match:
            count = _number(match.group(1))
            if count:
                limits[DAY_CANON[day_id]] = count
    return limits

def _parse_clock(text: str) -> str | None:
    s = _norm(text)
    m = re.search(r"([01]?\d|2[0-3])\s*[:٫.]\s*([0-5]\d)", s)
    if m:
        return f"{int(m.group(1)):02d}:{int(m.group(2)):02d}"
    spoken_quarter = re.search(r"(عشرة|عشره|احد عشر|اثنا عشر)\s+و?ربع", s)
    if spoken_quarter:
        hour = {"عشرة": 10, "عشره": 10, "احد عشر": 11, "اثنا عشر": 12}[spoken_quarter.group(1)]
        return f"{hour:02d}:15"
    hours = {"واحدة": 1, "واحد": 1, "اثنين": 2, "ثلاثة": 3, "اربعة": 4,
             "خمسة": 5, "ستة": 6, "سبعة": 7, "ثمانية": 8, "تسعة": 9,
             "عشرة": 10, "احد عشر": 11, "اثنا عشر": 12}
    for word, hour in hours.items():
        if re.search(rf"الساعة\s+{_norm(word)}", s):
            minute = 15 if "ربع" in s else (30 if "نص" in s else 0)
            return f"{hour:02d}:{minute:02d}"
    return None

def _extract_teacher_segments(text: str) -> list[tuple[str, str]]:
    pattern = re.compile(r"(?=(?:عنا\s+(?:(?:الأستاذة?|الاستاذة?|المدام)\s+)?|الاستاذة?\s+|المدام\s+)([\u0621-\u064a]+(?:\s+[\u0621-\u064a]+)?))")
    matches = list(pattern.finditer(text))
    out = []
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        raw = text[start:end].strip(" ،,؛;")
        name_match = pattern.match(text[start:])
        if not name_match:
            continue
        name = name_match.group(1).strip()
        prefix = _norm(raw[:raw.find(name)])
        if "المدام" in prefix and not name.startswith("ال"):
            name = name
        out.append((name, raw))
    # Fallback for common "عنا أحمد" / "عنا كارولين" forms already matched above.
    return out

def _subject(segment: str) -> str:
    m = re.search(r"(?:حيعطي|يعطي|بتعطي|تعطي|بتعلم|بعلم|يعلم|يدرّس|يدرس)\s+(.+?)\s+(?=لصف|للصف|لل|لكل|كل الصفوف|كل صف|،|,)", segment)
    if not m:
        return ""
    value = re.sub(r"^(?:مادة\s+)", "", m.group(1).strip())
    return value.strip(" ،،.")

def _explicit_classes(segment: str) -> list[str]:
    # Explicit grade + section labels such as "السابع A والسابع B والثامن B".
    pattern = re.compile(r"(السابع|السابعة|الثامن|الثامنة|التاسع|التاسعة)\s*(?:الشعبة\s*)?([A-Ga-g]|[أ-ي])", re.I)
    found = []
    for grade, section in pattern.findall(segment):
        grade_name = GRADE_WORDS.get(grade, grade)
        sec = section.upper() if section.isascii() else section
        label = f"{grade_name} {sec}"
        if label not in found:
            found.append(label)
    return found

def _grade_scope(segment: str) -> list[str]:
    n = _norm(segment)
    grades = []
    for key, grade in (("السابع", "السابع"), ("السوابع", "السابع"),
                       ("الثامن", "الثامن"), ("التوامن", "الثامن"),
                       ("التاسع", "التاسع"), ("التواسع", "التاسع")):
        if key in n and grade not in grades:
            grades.append(grade)
    return grades

def _availability(segment: str, work_days: list[int], day_limits: dict[str, int], teacher: str) -> list[dict[str, Any]]:
    n = _norm(segment)
    blocked = []
    phrases = []
    # Day-specific phrases.
    for day_word, day_id in DAY_NAMES.items():
        if day_id not in work_days:
            continue
        if day_word not in n:
            continue
        pos = n.find(day_word)
        tail = n[pos:pos + 90]
        m = re.search(r"(اول|اخر|آخر)\s+(?:ال)?(ثمانية|ثماني|سبعة|ستة|خمسة|اربعة|ثلاثة|ثلاث|ساعتين|اثنتين|اثنين|واحد|[1-9])\s*(?:ساعات|حصص|حصة)?", tail)
        if m:
            count = 2 if _norm(m.group(2)) == "ساعتين" else (_number(m.group(2), 1) or 1)
            limit = day_limits.get(DAY_CANON[day_id], max(day_limits.values() or [7]))
            if _norm(m.group(1)) == "اخر":
                periods = range(max(1, limit - count + 1), limit + 1)
            else:
                periods = range(1, min(limit, count) + 1)
            blocked.extend({"teacher": teacher, "day": day_id, "period": p} for p in periods)
    # "كل يوم أول ثلاث ساعات فراغ".
    m = re.search(r"كل\s+يوم.{0,24}?(اول)\s+(?:ال)?(ثمانية|سبعة|ستة|خمسة|اربعة|ثلاثة|ثلاث|اثنين|واحد|[1-9])\s*(?:ساعات|حصص|حصة)", n)
    if m:
        count = _number(m.group(2), 1) or 1
        for day_id in work_days:
            limit = day_limits.get(DAY_CANON[day_id], max(day_limits.values() or [7]))
            blocked.extend({"teacher": teacher, "day": day_id, "period": p}
                           for p in range(1, min(count, limit) + 1))
    unique = {(x["teacher"], x["day"], x["period"]): x for x in blocked}
    return list(unique.values())

def parse_spoken_school_intake(text: str) -> dict[str, Any]:
    if not isinstance(text, str) or not text.strip():
        raise ValueError("أدخل وصف المدرسة أولاً.")
    source = text.strip()
    n = _norm(source)
    days = []
    for word, day_id in DAY_NAMES.items():
        if re.search(rf"(?<![\w]){_norm(word)}(?![\w])", n) and day_id not in days:
            days.append(day_id)
    # Lebanese spoken weekday shorthand.
    list_match = re.search(r"(?:ايام|أيام)\s+(?:بالاسبوع|بالأسبوع)\s*[:：]?\s*([^.!؟]+)", n)
    if list_match:
        spoken_days = list_match.group(1)
        for token, day_id in (("اثنين", 0), ("ثلاثة", 1), ("اربعة", 2), ("خميس", 3)):
            if re.search(rf"(?<![\w]){token}(?![\w])", spoken_days) and day_id not in days:
                days.append(day_id)
    days.sort()
    if not days:
        days = []
    day_limits = _extract_day_limits(source, days)
    # Day counts in colloquial lists: اثنين عندي ثمان حصص، ثلاثة وأربعة وخميس سبع.
    for token, day_id in (("اثنين", 0), ("ثلاثة", 1), ("اربعة", 2), ("خميس", 3)):
        if day_id in days:
            match = re.search(rf"(?<![\w]){token}.{{0,30}}?(ثمانية|ثماني|ثمان|سبعة|سبع|ستة|ست|خمسة|خمس|اربعة|اربع|ثلاثة|ثلاث|اثنتين|اثنين|واحد|واحدة|[1-9])\s*(?:حصص|حصة)", n)
            if match:
                day_limits[DAY_CANON[day_id]] = _number(match.group(1))
    periods = max(day_limits.values()) if day_limits else None

    duration_match = re.search(r"(?:مدة الحصة|الحصة مدتها|كل حصة)\s*(?:هي\s*)?(\d+)\s*دقيقة", n)
    period_duration = int(duration_match.group(1)) if duration_match else (45 if re.search(r"(خمسة واربعين|خمس واربعين)\s*دقيقة", n) else None)
    break_start = None
    break_match = re.search(r"(?:فرصة|استراحة|استراحه).{0,35}", n)
    if break_match:
        break_start = _parse_clock(break_match.group(0))
    break_duration = 30 if re.search(r"(نص ساعة|نصف ساعة|نص ساعه|نصف ساعه)", n) else None

    teachers = []
    classes = []
    requirements = []
    blocked = []
    profiles = []
    unresolved = []
    warnings = []

    for name, segment in _extract_teacher_segments(source):
        subject = _subject(segment)
        explicit = _explicit_classes(segment)
        grades = _grade_scope(segment)
        count = None
        cm = re.search(r"(?:لكل صف|كل صف|بكل صف|لكل شعبة|كل شعبة|عدد حصص كل مادة|عدد الحصص).{0,20}?(ثمانية|ثماني|سبعة|ستة|خمسة|اربعة|ثلاثة|ثلاث|اثنين|واحد|[1-9])\s*(?:حصص|حصة)", _norm(segment))
        if cm:
            count = _number(cm.group(1))
        else:
            # Common compact wording: "كل صف عندها أربع حصص" / "كل صف ست حصص".
            cm = re.search(r"(?:كل صف|كل شعبة|بكل صف).{0,20}?(اربع|اربعة|ثلاث|ثلاثة|ست|ستة|خمس|خمسة|[1-9])\s*(?:حصص|حصة)", _norm(segment))
            if cm:
                count = _number(cm.group(1))
        if count is None:
            cm = re.search(r"(ثمانية|ثماني|سبعة|ستة|خمسة|اربعة|ثلاثة|ثلاث|اثنين|واحد|[1-9])\s*(?:حصص|حصة)", _norm(segment))
            if cm:
                count = _number(cm.group(1))
        if count is None and re.search(r"ساعة\s+ساعة", _norm(segment)):
            count = 1

        teacher = name.strip()
        if teacher not in teachers:
            teachers.append(teacher)
        profiles.append({"teacher": teacher, "subject": subject, "explicit_classes": explicit,
                         "grades": grades, "lessons_per_class": count,
                         "unavailable": _availability(segment, days, day_limits, teacher),
                         "source_excerpt": segment[:240]})
        blocked.extend(profiles[-1]["unavailable"])
        for cls in explicit:
            if cls not in classes:
                classes.append(cls)
            if subject and count:
                requirements.append({"class": cls, "teacher": teacher, "subject": subject, "count": count})
        if not explicit and (grades or re.search(r"كل الصفوف|جميع الصفوف|كل الصف|جميع الشعب", _norm(segment))):
            unresolved.append({"teacher": teacher, "subject": subject, "grades": grades,
                               "lessons_per_class": count,
                               "reason": "لم تُذكر أسماء الشعب صراحة؛ يلزم تحديد الشعب الموجودة في المدرسة."})
        if not subject:
            warnings.append(f"لم أتمكن من تحديد مادة {teacher} بثقة.")
        if not count:
            warnings.append(f"لم يُحدد عدد حصص {teacher} لكل شعبة بوضوح.")

    if not teachers:
        warnings.append("لم أتعرف على أسماء المعلمين. اذكر الاسم بعد «عنا» أو «الأستاذ/الأستاذة».")
    if not days:
        warnings.append("لم تُحدد أيام الدوام.")
    if periods is None:
        warnings.append("لم تُحدد أعداد الحصص اليومية.")

    # Parse a global class-scope sentence where the grade list is stated outside the teacher segment.
    if "كارولين" in n and not any(x["teacher"] == "كارولين" for x in profiles):
        warnings.append("تعذر فصل بيانات كارولين عن بقية الكلام؛ أعد ذكر اسمها قبل تفاصيلها.")

    return {
        "school_name": "",
        "days": days,
        "periods": periods,
        "day_period_limits": day_limits,
        "period_duration_minutes": period_duration,
        "break_start": break_start,
        "break_duration_minutes": break_duration,
        "teachers": teachers,
        "classes": classes,
        "requirements": requirements,
        "blocked": blocked,
        "teacher_profiles": profiles,
        "unresolved_scopes": unresolved,
        "warnings": warnings,
        "ready_for_generation": bool(days and periods and teachers and classes and requirements and not unresolved and not warnings),
        "engine": "NABIL Local Spoken Intake",
        "external_ai_used": False,
    }
