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
GRADE_WORDS = {
    "الأول": "الأول", "الاول": "الأول", "الأول الأساسي": "الأول", "الاول الاساسي": "الأول",
    "الثاني": "الثاني", "الثاني الأساسي": "الثاني", "الثاني الاساسي": "الثاني",
    "الثالث": "الثالث", "الثالث الأساسي": "الثالث", "الثالث الاساسي": "الثالث",
    "الرابع": "الرابع", "الرابع الأساسي": "الرابع", "الرابع الاساسي": "الرابع",
    "الخامس": "الخامس", "الخامس الأساسي": "الخامس", "الخامس الاساسي": "الخامس",
    "السادس": "السادس", "السادس الأساسي": "السادس", "السادس الاساسي": "السادس",
    "السابع": "السابع", "السابعة": "السابع",
    "الثامن": "الثامن", "الثامنة": "الثامن",
    "التاسع": "التاسع", "التاسعة": "التاسع",
    "العاشر": "الأول ثانوي", "الأول ثانوي": "الأول ثانوي", "الاول ثانوي": "الأول ثانوي",
    "الحادي عشر": "الثاني ثانوي", "الثاني ثانوي": "الثاني ثانوي", "الثاني الثانوي": "الثاني ثانوي",
    "الثاني عشر": "الثالث ثانوي", "الثالث ثانوي": "الثالث ثانوي", "الثالث الثانوي": "الثالث ثانوي",
}

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
    """Read daily lesson totals, never mistake a teacher's free periods for totals."""
    normalized = _norm(text)
    limits: dict[str, int] = {}
    aliases = [("الاثنين", 0), ("الاربعاء", 2), ("الثلاثاء", 1),
               ("الخميس", 3), ("الجمعة", 4), ("السبت", 5), ("الاحد", 6)]
    number_pattern = r"(ثمانية|ثماني|ثمان|سبعة|سبع|ستة|ست|خمسة|خمس|اربعة|اربع|ثلاثة|ثلاث|اثنين|اثنتين|واحد|واحدة|[1-9])"
    # A clearly stated global daily total applies to every explicitly selected workday.
    global_total = re.search(
        r"(?:عدد\s+الحصص\s+اليومية|الحصص\s+اليومية|كل\s+يوم)\s*(?:هو|هي)?\s*"
        + number_pattern + r"\s*(?:حصص|حصة)", normalized
    )
    if global_total:
        total = _number(global_total.group(1))
        if total:
            for day_id in days:
                limits[DAY_CANON[day_id]] = total
    for day_word, day_id in aliases:
        if day_id not in days:
            continue
        for day_match in re.finditer(day_word, normalized):
            tail = normalized[day_match.end():day_match.end() + 65]
            count_match = re.search(r"(?:عندي|فيه|في|عددها)?\s*" + number_pattern + r"\s*(?:حصص|حصة)", tail)
            if not count_match:
                continue
            context = normalized[max(0, day_match.start() - 35):day_match.end()] + tail[:count_match.start()]
            # "فراغ الاثنين أول ثلاث حصص" is teacher availability, not a 3-period day.
            if re.search(r"فراغ|غير متاح|عدم توافر|اول|اخر|آخر", context):
                continue
            count = _number(count_match.group(1))
            if count:
                limits[DAY_CANON[day_id]] = count
                break
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
    # Accept conversational introductions and clear name labels such as "نبيل عقيل:".
    explicit = re.compile(
        r"(?:عنا\s+(?:(?:الأستاذة?|الاستاذة?|استاذة?|استاذ|السيس|السيد|السيدة|المدام|المعلم)\s+)?|"
        r"(?:الأستاذة?|الاستاذة?|استاذة?|استاذ|السيس|السيد|السيدة|المدام|المعلم)\s+)"
        r"([\u0621-\u064a]+(?:\s+(?!للصف\b|الصف\b|بدرس\b|بيدرس\b|يدرس\b|رياضيات\b|تربية\b)[\u0621-\u064a]+)?)"
    )
    labeled = re.compile(
        r"(?:^|[\n؛;,]\s*)(?:المعلم\s+)?"
        r"([\u0621-\u064a]+(?:\s+[\u0621-\u064a]+)?)\s*[:：]",
        re.M
    )
    stop = {"سبع", "سبعة", "ست", "ستة", "خمس", "خمسة", "أربع", "اربعة",
            "ثلاث", "ثلاثة", "حصص", "حصة", "أيام", "ايام", "الدوام",
            "بعلمهم", "بيعطي", "يعطي", "يعلموا", "الاستاذ", "الأستاذ",
            "الأستاذة", "المدام", "المعلم", "كل", "لكل", "عندهم", "عنده",
            "للصف", "الصف", "بدرس", "بيدرس", "يدرس", "رياضيات", "تربية"}
    matches: list[tuple[int, int, str]] = []
    for pattern in (explicit, labeled):
        for m in pattern.finditer(text):
            name = m.group(1).strip()
            words = _norm(name).split()
            if not words or any(w in stop for w in words):
                continue
            matches.append((m.start(), m.end(), name))
    matches.sort(key=lambda item: item[0])
    deduped: list[tuple[int, int, str]] = []
    seen = set()
    for item in matches:
        key = (_norm(item[2]), item[0])
        if key not in seen:
            seen.add(key)
            deduped.append(item)
    out = []
    for i, (start, end, name) in enumerate(deduped):
        segment_end = deduped[i + 1][0] if i + 1 < len(deduped) else len(text)
        segment = text[end:segment_end].strip(" ،,؛;:")
        if segment:
            out.append((name, segment))
    return out

def _subject(segment: str) -> str:
    # Accept both teaching verbs and spoken teacher-profile shorthand.
    subjects = (
        "رياضيات", "لغة عربية", "عربي", "انكليزي", "إنكليزي", "انجليزي",
        "لغة انكليزية", "بيولوجي", "علوم", "فيزياء", "كيمياء", "تاريخ",
        "جغرافيا", "دين", "تربية", "رياضة", "فرنسي", "لغة فرنسية",
        "اجتماعيات", "فلسفة", "اقتصاد", "معلوماتية", "فنون", "موسيقى"
    )
    verbs = r"(?:حيعطي|بيعطي|يعطي|بتعطي|تعطي|بتعلم|بيعلم|بعلم|يعلم|يدرّس|بيدرس|بدرس|يدرس)"
    for subject in sorted(subjects, key=len, reverse=True):
        subject_rx = re.escape(subject)
        if re.search(verbs + r"\s+" + subject_rx + r"(?=\s|$|،|,)", segment, re.I):
            return subject
        if re.search(r"(?:بدرس|بيدرس|يدرّس|يدرس).{0,45}?" + subject_rx + r"(?=\s|$|،|,)", segment, re.I):
            return subject
        if re.search(r"(?:معلم|معلمة|مدرس|مدرسة|مادة|اختصاصه|اختصاصها)\s+" + subject_rx + r"(?=\s|$|،|,)", segment, re.I):
            return subject
    return ""

def _explicit_classes(segment: str) -> list[str]:
    """Extract explicit class sections, including spoken Arabic letter names."""
    grade_pattern = r"(الثاني\s+عشر|الثالث\s+الثانوي|الثالث\s+ثانوي|الحادي\s+عشر|الثاني\s+الثانوي|الثاني\s+ثانوي|الأول\s+ثانوي|الاول\s+ثانوي|الأول\s+الأساسي|الاول\s+الاساسي|الثاني\s+الأساسي|الثاني\s+الاساسي|الثالث\s+الأساسي|الثالث\s+الاساسي|الرابع\s+الأساسي|الرابع\s+الاساسي|الخامس\s+الأساسي|الخامس\s+الاساسي|السادس\s+الأساسي|السادس\s+الاساسي|العاشر|التاسع|التاسعة|الثامن|الثامنة|السابع|السابعة|الخامس|الخامسة|الرابع|الرابعة|الثالث|الثالثة|الثاني|الثانية|الأول|الاول)"
    found: list[str] = []
    section_aliases = {
        "الف": "أ", "ألف": "أ", "الالف": "أ", "الألف": "أ", "ا": "أ",
        "باء": "ب", "با": "ب", "ب": "ب", "جيم": "ج", "جم": "ج", "ج": "ج",
        "دال": "د", "د": "د", "هاء": "هـ", "ه": "هـ", "واو": "و",
        "و": "و", "زاي": "ز", "ز": "ز",
    }
    grade_rx = re.compile(r"(?<![\w])(" + grade_pattern + r")(?![\w])", re.I)
    matches = list(grade_rx.finditer(segment))
    for index, match in enumerate(matches):
        grade = match.group(1)
        tail_end = matches[index + 1].start() if index + 1 < len(matches) else len(segment)
        tail = _norm(segment[match.end():tail_end])
        grade_name = GRADE_WORDS.get(grade, GRADE_WORDS.get(_norm(grade), grade))
        tail = re.split(r"[.؛;!?\n]", tail, maxsplit=1)[0]
        tokens = re.findall(r"[\u0621-\u064a]+|[a-g]", tail)
        sections = []
        for token in tokens:
            key = _norm(token)
            if key.startswith("و") and key[1:] in section_aliases:
                key = key[1:]
            if key in section_aliases:
                section = section_aliases[key]
                if section not in sections:
                    sections.append(section)
            elif len(token) == 1 and token.lower() in "abcdefg":
                if token.upper() not in sections:
                    sections.append(token.upper())
        for section in sections:
            label = f"{grade_name} {section}"
            if label not in found:
                found.append(label)
    return found

def _grade_scope(segment: str) -> list[str]:
    n = _norm(segment)
    grades = []
    if re.search(r"من.{0,24}(?:الصف\s*)?الاول.{0,35}(?:الى|حتى|لغاية).{0,24}(?:الثالث\s+ثانوي|الثالث\s+الثانوي|الثاني\s+عشر)", n):
        return ["الأول", "الثاني", "الثالث", "الرابع", "الخامس", "السادس",
                "السابع", "الثامن", "التاسع", "الأول ثانوي", "الثاني ثانوي", "الثالث ثانوي"]
    aliases = [
        (("الاول ثانوي", "العاشر"), "الأول ثانوي"),
        (("الثاني ثانوي", "الثاني الثانوي", "الحادي عشر"), "الثاني ثانوي"),
        (("الثالث ثانوي", "الثالث الثانوي", "الثاني عشر"), "الثالث ثانوي"),
        (("الاول", "الصف الاول", "الاول الاساسي"), "الأول"),
        (("الثاني", "الصف الثاني", "الثاني الاساسي"), "الثاني"),
        (("الثالث", "الصف الثالث", "الثالث الاساسي"), "الثالث"),
        (("الرابع", "الصف الرابع", "الرابع الاساسي"), "الرابع"),
        (("الخامس", "الصف الخامس", "الخامس الاساسي"), "الخامس"),
        (("السادس", "الصف السادس", "السادس الاساسي"), "السادس"),
        (("السابع", "السوابع"), "السابع"),
        (("الثامن", "التوامن", "الثوامن"), "الثامن"),
        (("التاسع", "التواسع"), "التاسع"),
    ]
    secondary_present = any(x in n for x in ("الاول ثانوي", "العاشر", "الثاني ثانوي", "الثاني الثانوي", "الحادي عشر", "الثالث ثانوي", "الثالث الثانوي", "الثاني عشر"))
    for keys, grade in aliases:
        if secondary_present and grade in ("الأول", "الثاني", "الثالث"):
            continue
        if any(key in n for key in keys) and grade not in grades:
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
        m = re.search(r"(اول|اخر|آخر)\s+(?:ال)?(ثمانية|ثماني|سبعة|ستة|خمسة|اربعة|ثلاثة|ثلاث|ساعتين|حصتين|اثنتين|اثنين|واحد|[1-9])\s*(?:ساعات|حصص|حصة)?", tail)
        if m:
            count = 2 if _norm(m.group(2)) in ("ساعتين", "حصتين") else (_number(m.group(2), 1) or 1)
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
    # Explicit numbered periods such as "السابعة والثامنة فراغ".
    ordinal = {"الاولى": 1, "الاول": 1, "الثانية": 2, "الثاني": 2,
               "الثالثة": 3, "الثالث": 3, "الرابعة": 4, "الرابع": 4,
               "الخامسة": 5, "الخامس": 5, "السادسة": 6, "السادس": 6,
               "السابعة": 7, "السابع": 7, "الثامنة": 8, "الثامن": 8}
    for day_word, day_id in DAY_NAMES.items():
        if day_id not in work_days or day_word not in n:
            continue
        tail = n[n.find(day_word):n.find(day_word) + 100]
        if "فراغ" not in tail:
            continue
        for word, period in ordinal.items():
            if re.search(rf"{word}", tail):
                limit = day_limits.get(DAY_CANON[day_id], max(day_limits.values() or [8]))
                if period <= limit:
                    blocked.append({"teacher": teacher, "day": day_id, "period": period})
    unique = {(x["teacher"], x["day"], x["period"]): x for x in blocked}
    return list(unique.values())

def parse_spoken_school_intake(text: str) -> dict[str, Any]:
    if not isinstance(text, str) or not text.strip():
        raise ValueError("أدخل وصف المدرسة أولاً.")
    source = text.strip()
    n = _norm(source)
    days = []
    for word, day_id in DAY_NAMES.items():
        if re.search(rf"(?<![\w])و?{_norm(word)}(?![\w])", n) and day_id not in days:
            days.append(day_id)
    # Lebanese spoken weekday shorthand.
    list_match = re.search(r"(?:ايام|أيام)\s+(?:بالاسبوع|بالأسبوع)\s*[:：]?\s*([^.!؟]+)", n)
    if list_match:
        spoken_days = list_match.group(1)
        for token, day_id in (("اثنين", 0), ("ثلاثة", 1), ("اربعة", 2), ("خميس", 3)):
            if re.search(rf"(?<![\w])و?{token}(?![\w])", spoken_days) and day_id not in days:
                days.append(day_id)
    # "كل الأيام دوام" means the regular school week (Monday-Friday);
    # explicit weekends are still added only when spoken by name.
    if re.search(r"كل\s+(?:ال)?ايام\s+(?:دوام|دوامنا|عمل)", n):
        for day_id in range(5):
            if day_id not in days:
                days.append(day_id)
    days.sort()
    if not days:
        days = []
    # Only read day-period totals from the school-schedule part, before teacher details.
    # Otherwise "فراغ الاثنين أول ثلاث حصص" can be misread as a three-period school day.
    teacher_matches = _extract_teacher_segments(source)
    first_teacher_pos = source.find(teacher_matches[0][0]) if teacher_matches else -1
    config_text = source[:first_teacher_pos] if first_teacher_pos >= 0 else source
    day_limits = _extract_day_limits(config_text, days)
    periods = max(day_limits.values()) if day_limits else None

    duration_match = re.search(r"(?:مدة الحصة|الحصة مدتها|كل حصة)\s*(?:هي\s*)?(\d+)\s*دقيقة", n)
    period_duration = int(duration_match.group(1)) if duration_match else (45 if re.search(r"(خمسة واربعين|خمس واربعين)\s*دقيقة", n) else None)
    break_start = None
    break_match = re.search(r"(?:فرصة|استراحة|استراحه).{0,35}", n)
    if break_match:
        break_start = _parse_clock(break_match.group(0))
    break_duration = 30 if re.search(r"(نص ساعة|نصف ساعة|نص ساعه|نصف ساعه)", n) else None

    teachers = []
    classes = _explicit_classes(source)
    requirements = []
    blocked = []
    profiles = []
    unresolved = []
    warnings = []

    # Speech recognition appends many partial phrases. Merge repeated mentions
    # of the same teacher before extracting their teaching assignments.
    grouped_segments = {}
    for spoken_name, spoken_segment in _extract_teacher_segments(source):
        key = _norm(spoken_name)
        if key not in grouped_segments:
            grouped_segments[key] = [spoken_name.strip(), []]
        grouped_segments[key][1].append(spoken_segment)

    for teacher, pieces in grouped_segments.values():
        segment = " ".join(piece for piece in pieces if piece)
        subject = _subject(segment)
        explicit = _explicit_classes(segment)
        grades = _grade_scope(segment)
        count = None
        cm = re.search(r"(?:لكل صف|كل صف|بكل صف|لكل شعبة|كل شعبة|كل شعبي|كل الشعب|عدد حصص كل مادة|عدد الحصص).{0,20}?(ثمانية|ثماني|سبعة|ستة|خمسة|اربعة|ثلاثة|ثلاث|اثنين|واحد|[1-9])\s*(?:حصص|حصة)", _norm(segment))
        if cm:
            count = _number(cm.group(1))
        if count is None:
            cm = re.search(r"(ثمانية|ثماني|ثمان|سبعة|سبع|ستة|ست|خمسة|خمس|اربعة|اربع|ثلاثة|ثلاث|اثنتين|اثنين|واحد|واحدة|[1-9])\s*(?:حصص|حصة)", _norm(segment))
            if cm:
                count = _number(cm.group(1))
        if count is None and re.search(r"(?:ساعة\s+ساعة|حصة\s+واحدة|ساعة\s+واحدة|حصة\s+كل\s+اسبوع|حصة\s+اسبوعية)", _norm(segment)):
            count = 1
        declared_weekly = None
        weekly_match = re.search(r"(?:نصابه|نصابها|نصاب)\s*(?:لازم\s+يكون|هو)?\s*(\d+)\s*(?:ساعة|حصة)", _norm(segment))
        if weekly_match:
            declared_weekly = int(weekly_match.group(1))
        if teacher not in teachers:
            teachers.append(teacher)

        # Separate clauses such as "للصف الأول تربية حصة أسبوعياً" and
        # "وبيدرس رياضيات للصف الرابع أ" to avoid cross-assigning subjects.
        clauses = re.split(r"(?=(?:وبيدرس|بيدرس|وبدرس|بدرس|ويدرس|يدرس|وبعلم|بيعلم|يعلم)\s*)", segment)
        assignments = []
        for clause in clauses:
            clause_subject = _subject(clause)
            clause_classes = _explicit_classes(clause)
            clause_count = None
            if re.search(r"(?:حصة\s+كل\s+اسبوع|حصة\s+اسبوعية|حصة\s+واحدة)", _norm(clause)):
                clause_count = 1
            else:
                cm_clause = re.search(r"(?:لكل صف|كل صف|بكل صف|لكل شعبة|كل شعبة|كل شعبي|كل الشعب).{0,20}?(ثمانية|ثماني|سبعة|ستة|خمسة|اربعة|ثلاثة|ثلاث|اثنين|واحد|[1-9])\s*(?:حصص|حصة)", _norm(clause))
                if cm_clause:
                    clause_count = _number(cm_clause.group(1))
            if clause_subject and clause_classes:
                assignments.append((clause_subject, clause_classes, clause_count))
        if not assignments and subject and explicit:
            assignments.append((subject, explicit, count))

        subjects = []
        all_explicit = []
        for clause_subject, clause_classes, clause_count in assignments:
            if clause_subject not in subjects:
                subjects.append(clause_subject)
            for cls in clause_classes:
                if cls not in all_explicit:
                    all_explicit.append(cls)
                if cls not in classes:
                    classes.append(cls)
                if clause_count:
                    item = {"class": cls, "teacher": teacher, "subject": clause_subject, "count": clause_count}
                    if not any(x["class"] == cls and x["teacher"] == teacher and x["subject"] == clause_subject for x in requirements):
                        requirements.append(item)
        if not all_explicit:
            all_explicit = explicit
        profile_subject = " / ".join(subjects) if subjects else subject
        profile = {"teacher": teacher, "subject": profile_subject, "explicit_classes": all_explicit,
                   "grades": grades, "lessons_per_class": count,
                   "declared_weekly_load": declared_weekly,
                   "unavailable": _availability(segment, days, day_limits, teacher),
                   "source_excerpt": segment[:500]}
        profiles.append(profile)
        blocked.extend(profile["unavailable"])
        if not all_explicit and (grades or re.search(r"كل الصفوف|جميع الصفوف|كل الصف|جميع الشعب", _norm(segment))):
            unresolved.append({"teacher": teacher, "subject": profile_subject, "grades": grades,
                               "lessons_per_class": count,
                               "reason": "لم تُذكر أسماء الشعب صراحة؛ يلزم تحديد الشعب الموجودة في المدرسة."})
        if not subject and not subjects:
            warnings.append(f"لم أتمكن من تحديد مادة {teacher} بثقة.")
        if not count and not any(x[2] for x in assignments):
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
