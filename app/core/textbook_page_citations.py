"""Render only database-backed textbook page references in student lessons.

The model can propose a citation, but cannot create its provenance.
A page displayed as verified must occur in the exact RAG source set.
"""
import re

_PAGE_TAG = re.compile(r"\[BOOK_PAGE\s*:\s*([^\]\n]{1,45})\]", re.I)
_NUMBER = re.compile(r"(?<!\d)\d{1,4}(?!\d)")


def verified_source_pages(source_chunks: list[dict]) -> list[dict]:
    """Distinct real printed pages, with book title; no invented PDF offsets."""
    seen: set[tuple[str, int]] = set()
    out: list[dict] = []
    for item in source_chunks or []:
        if not isinstance(item, dict):
            continue
        title = str(item.get("book_title") or "").strip()
        raw = item.get("page")
        if not title or isinstance(raw, bool):
            continue
        try:
            page = int(raw)
        except (ValueError, TypeError):
            continue
        if page < 1 or str(raw).strip() != str(page):
            continue
        pair = (title, page)
        if pair not in seen:
            seen.add(pair)
            out.append({"book_title": title, "page": page})
    return sorted(out, key=lambda x: (x["book_title"], x["page"]))


def render_verified_page_citations(text: str, source_chunks: list[dict]) -> str:
    """Replace model-suggested tags with conspicuous, verified printed-page badges.

    If the model cites a page that was not retrieved, suppress the citation;
    never promote it to an official-book claim. Missing citations are not
    invented: the source index shows which pages actually reached this answer.
    """
    original = str(text or "")
    sources = verified_source_pages(source_chunks)
    valid = {int(s["page"]) for s in sources}

    def replace(match: re.Match) -> str:
        raw = match.group(1)
        # Accept only number lists, never prose or long misleading references.
        if not re.fullmatch(r"\s*\d{1,4}(?:\s*[,،]\s*\d{1,4}){0,5}\s*", raw):
            return ""
        pages = sorted({int(n) for n in _NUMBER.findall(raw)})
        if not pages or any(p not in valid for p in pages):
            return ""
        rendered = "، ".join(str(p) for p in pages)
        label = "الصفحة المطبوعة" if len(pages) == 1 else "الصفحات المطبوعة"
        return f"\n\n**📘 كتاب الدولة | {label}: {rendered}**\n\n"

    body = _PAGE_TAG.sub(replace, original).strip()
    if not sources:
        return body

    groups: dict[str, list[int]] = {}
    for item in sources:
        groups.setdefault(item["book_title"], []).append(item["page"])
    index_lines = [
        "**📚 الصفحات المسترجعة فعلًا من كتاب الدولة لهذا الجواب:**",
    ]
    for title, pages in groups.items():
        index_lines.append(
            f"- {title} — الصفحات المطبوعة: {', '.join(map(str, pages))}"
        )
    index_lines.append(
        "*الصفحات أعلاه مسترجعة من الفهرس، وليست إثباتًا بأن كل فكرة "
        "أو رسمة واردة فيها ما لم يُذكر مرجعها تحت الفكرة نفسها.*"
    )
    return "\n".join(index_lines) + "\n\n" + body
