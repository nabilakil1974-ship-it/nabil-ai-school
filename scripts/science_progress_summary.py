"""Pure formatting for DB-backed textbook-index progress.

A book mapping (grade/subject/curriculum) can share its source PDF with
another mapping. Count mapped books and pages separately from unique PDFs.
Unknown page totals cannot be declared complete.
"""
from __future__ import annotations


def summarize(rows: list[tuple[int, int, bool]]) -> dict[str, object]:
    """Each row: completed PDF pages, known PDF page total or zero, complete."""
    total_mappings = len(rows)
    complete = sum(1 for _, _, yes in rows if yes)
    started = sum(1 for done, _, _ in rows if done > 0)
    known_pages = sum(total for _, total, _ in rows if total > 0)
    done_pages = sum(min(max(done, 0), total) for done, total, _ in rows if total > 0)
    return {
        "mappings": total_mappings,
        "complete": complete,
        "started": started,
        "remaining_mappings": total_mappings - complete,
        "known_pages": known_pages,
        "done_pages": done_pages,
        "remaining_known_pages": known_pages - done_pages,
        "percent_known_pages": round(100 * done_pages / known_pages, 1)
        if known_pages else None,
    }


def summary_line(stats: dict[str, object]) -> str:
    percent = stats["percent_known_pages"]
    shown = f"{percent:.1f}%" if isinstance(percent, (int, float)) else "unknown"
    return (
        f"  MAPPED BOOKS: {stats['complete']}/{stats['mappings']} complete; "
        f"{stats['remaining_mappings']} remaining; "
        f"{stats['started']} started. PDF pages (known totals): "
        f"{stats['done_pages']}/{stats['known_pages']} "
        f"({shown}); {stats['remaining_known_pages']} pages remaining."
    )
