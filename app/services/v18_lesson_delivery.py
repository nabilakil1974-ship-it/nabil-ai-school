"""NABIL V18 lesson visibility and delivery.

Only this module owns: lesson selector rows, resolving published lessons,
the view URL, and runtime asset injection. Scientific gates stay independent.
"""
from __future__ import annotations
import re
from urllib.parse import quote

RUNTIME_ASSETS = (
    "/static/nabil_browser_tts_v1.js",
    "/static/nabil_lesson_e2e_runtime_v1.js",
    "/static/nabil_smart_lab_bridge_v1.js",
)

def catalogue_rows(indexed, prepared_lookup, prepared_entries, *, grade, subject,
                   norm, normalize_grade, normalize_subject, clean_title):
    lessons = []
    seen = set()
    for row in indexed:
        key = norm(row["title"])
        prepared = prepared_lookup.get(key)
        lessons.append({
            **row,
            "prepared": bool(prepared),
            "available_to_open": bool(prepared),
            "filename": str(prepared.get("filename", "")) if prepared else "",
            "drive_file_id": str(prepared.get("drive_file_id", "")) if prepared else "",
        })
        seen.add(key)
    for prepared in prepared_entries:
        if normalize_grade(prepared.get("grade")) != normalize_grade(grade):
            continue
        if normalize_subject(prepared.get("subject")) != normalize_subject(subject):
            continue
        filename = str(prepared.get("filename", ""))
        if re.search(r"--EXERCISES\\.html$", filename, re.I):
            continue
        title = clean_title(prepared["lesson"])
        key = norm(title)
        if key in seen:
            continue
        seen.add(key)
        lessons.append({
            "title": title, "raw_title": prepared["lesson"],
            "aliases": prepared.get("aliases", []),
            "filename": filename,
            "drive_file_id": str(prepared.get("drive_file_id", "")),
            "prepared": True, "available_to_open": True,
            "source": "prepared_drive_fallback",
        })
    return {
        "grade": grade, "subject": subject, "lessons": lessons,
        "source": "factory_book_index+prepared_drive" if indexed else "prepared_drive_fallback",
        "indexed_count": len(indexed),
        "prepared_count": sum(bool(x.get("prepared")) for x in lessons),
        "count": len(lessons),
    }

def resolve_item(resolver, grade, subject, lesson, language=""):
    item = resolver(grade, subject, lesson, language)
    if not isinstance(item, dict) or not item.get("drive_file_id"):
        raise ValueError("LESSON_NOT_PUBLISHED_OR_MISSING_DRIVE_FILE")
    return item

def view_url(grade, subject, lesson, language="", trace=""):
    return ("/api/interactive-lessons/view?grade=" + quote(grade)
            + "&subject=" + quote(subject) + "&lesson=" + quote(lesson)
            + "&language=" + quote(language) + "&trace=" + quote(trace))

def valid_html_bytes(payload):
    return (b"<html" in payload[:4096].lower()
            or b"<!doctype html" in payload[:4096].lower())

def ensure_runtime_scripts(html):
    """Embed only the shared browser runtime once. Never invent lesson data."""
    if 'name="nabil-renderer-contract"' not in html or "</body>" not in html.lower():
        return html
    tags = [
        '<script src="' + asset + '?v=1"></script>'
        for asset in RUNTIME_ASSETS if asset not in html
    ]
    if not tags:
        return html
    return re.sub(r"</body>", "".join(tags) + "</body>", html, count=1, flags=re.I)
