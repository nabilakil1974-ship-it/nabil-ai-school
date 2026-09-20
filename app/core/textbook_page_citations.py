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


def verified_page_refs(source_chunks: list[dict]) -> list[dict]:
    """Source records carrying BOTH printed page and actual PDF position.

    No PDF position may be inferred by adding an offset to the printed page.
    """
    out = []
    seen = set()
    for item in source_chunks or []:
        if not isinstance(item, dict):
            continue
        book_id = str(item.get("book_id") or "")
        pdf_page = item.get("pdf_page")
        title = str(item.get("book_title") or "")
        try:
            page = int(item.get("page"))
            actual_pdf = int(pdf_page)
        except (TypeError, ValueError):
            continue
        if not book_id or not title or page < 1 or actual_pdf < 1:
            continue
        key = (book_id, page, actual_pdf)
        if key in seen:
            continue
        seen.add(key)
        out.append({
            "book_title": title,
            "book_id": book_id,
            "page": page,
            "pdf_page": actual_pdf,
            "page_image_url": f"/api/textbooks/{book_id}/pages/{page}/image",
        })
    return sorted(out, key=lambda item: (item["book_title"], item["page"]))


def render_verified_page_citations(text: str, source_chunks: list[dict]) -> str:
    """Replace model-suggested tags with conspicuous, verified printed-page badges.

    If the model cites a page that was not retrieved, suppress the citation;
    never promote it to an official-book claim. Missing citations are not
    invented: the source index shows which pages actually reached this answer.
    """
    original = str(text or "")
    sources = verified_source_pages(source_chunks)
    images = verified_page_refs(source_chunks)
    image_by_page = {p["page"]: p for p in images}
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
        image_links = "\\n".join(
            f"[📷 عرض صفحة الكتاب الأصلية (ص. {p})]"
            f"({image_by_page[p]['page_image_url']})"
            for p in pages if p in image_by_page
        )
        return (
            f"\\n\\n**📘 كتاب الدولة | {label}: {rendered}**\\n"
            + (image_links + "\\n" if image_links else "")
            + "\\n"
        )

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
    for original_page in images:
        index_lines.append(
            f"[📷 صفحة الكتاب المصوّرة {original_page['page']}]"
            f"({original_page['page_image_url']})"
        )
    index_lines.append(
        "*الصفحات أعلاه مسترجعة من الفهرس، وليست إثباتًا بأن كل فكرة "
        "أو رسمة واردة فيها ما لم يُذكر مرجعها تحت الفكرة نفسها.*"
    )
    return "\n".join(index_lines) + "\n\n" + body
