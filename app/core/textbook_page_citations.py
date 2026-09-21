"""Render only database-backed textbook page references in student lessons.

The model can propose a citation, but cannot create its provenance.
A page displayed as verified must occur in the exact RAG source set.
"""
import re

_PAGE_TAG = re.compile(r"\[BOOK_PAGE\s*:\s*([^\]\n]{1,45})\]", re.I)
_NUMBER = re.compile(r"(?<!\d)\d{1,4}(?!\d)")
_FIGURE_TAG = re.compile(r"\[BOOK_FIGURE_PAGE\s*:\s*(\d{1,4})\]", re.I)


def _text_states_printed_page(page_text: str, pdf_page_index: int, max_drift: int = 30):
    """Look for the real printed page number stated in a page's own
    extracted/OCR'd text (header or footer), independent of whatever
    printed_page_number happens to be stored for it in the database.

    Same detection approach used in scripts/index_books.py (index time) and
    app/api/routes_textbook_pages.py (page-image lookup) - duplicated here
    rather than imported since this module intentionally stays dependency-
    free (it is on the hot path of every chat response that cites a book).
    Only the first/last couple of lines are checked (a printed page number
    conventionally sits in a header or footer, not body text), and a
    candidate is accepted only if it is a standalone number within
    max_drift of the raw PDF position - this avoids matching an unrelated
    number (an exercise number, a chemical formula, a chapter number).
    """
    if not page_text:
        return None
    lines = [ln.strip() for ln in str(page_text).splitlines() if ln.strip()]
    if not lines:
        return None
    for line in lines[:2] + lines[-2:]:
        stripped = line.strip(" -–—.|•")
        if not stripped.isdigit():
            continue
        candidate = int(stripped)
        if candidate <= 0:
            continue
        if abs(candidate - pdf_page_index) <= max_drift:
            return candidate
    return None


# Every book in the catalog was indexed with printed_page_offset left at its
# default of 0 (confirmed 2026-09-20 across all subject manifests: chemistry,
# physics, biology, math) - meaning the "printed" page number stored in the
# database is actually the raw PDF page index for every book, not just this
# one. This was previously a single hardcoded, manually-verified offset for
# one book title; resolve_book_printed_page() below now derives the offset
# generally, from each item's own already-fetched text, instead of only
# trusting a lookup table that only ever had one entry.
_VERIFIED_PRINTED_PAGE_OFFSETS = {
    "chemistry - grade 9.pdf": 2,
}


def resolve_book_printed_page(item: dict) -> int | None:
    try:
        page = int(item.get("page"))
        pdf_page = int(item.get("pdf_page")) if item.get("pdf_page") else None
    except (TypeError, ValueError):
        return None
    if page < 1:
        return None

    # General case: this source chunk already carries its own extracted
    # text (search_book_pages() always includes it for building the answer)
    # - use it as direct evidence of what page this really is, the same way
    # index-time and page-image-lookup already do. This works for ANY book,
    # not just ones with a manually verified offset on file.
    stated = _text_states_printed_page(item.get("text") or "", pdf_page if pdf_page is not None else page)
    if stated is not None:
        return stated

    # Fallback for the one book with a manually pre-verified offset, in case
    # its chunk text for some reason doesn't carry a detectable page number
    # (e.g. a page whose only content is a diagram with a caption OCR missed).
    title = str(item.get("book_title") or "").strip().lower()
    offset = _VERIFIED_PRINTED_PAGE_OFFSETS.get(title)
    if offset is not None and pdf_page is not None and page == pdf_page:
        return page + offset
    return page


def verified_source_pages(source_chunks: list[dict]) -> list[dict]:
    """Distinct real printed pages, with book title; no invented PDF offsets."""
    seen: set[tuple[str, int]] = set()
    out: list[dict] = []
    for item in source_chunks or []:
        if not isinstance(item, dict):
            continue
        title = str(item.get("book_title") or "").strip()
        raw = resolve_book_printed_page(item)
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
            page = int(resolve_book_printed_page(item))
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
        image_links = "\n".join(
            f"[📷 عرض صفحة الكتاب الأصلية (ص. {p})]"
            f"({image_by_page[p]['page_image_url']})"
            for p in pages if p in image_by_page
        )
        return (
            f"\n\n**📘 كتاب الدولة | {label}: {rendered}**\n"
            + (image_links + "\n" if image_links else "")
            + "\n"
        )

    body = _PAGE_TAG.sub(replace, original).strip()

    def render_original_figure(match: re.Match) -> str:
        page = int(match.group(1))
        data = image_by_page.get(page)
        if not data:
            return ""
        link = data["page_image_url"]
        return (
            f"\n\n**📘 الرسم الأصلي من كتاب الدولة — الصفحة المطبوعة {page}**\n"
            f"![صورة صفحة الكتاب الأصلية، الصفحة {page}]({link})\n"
            f"[🔎 تكبير صفحة الكتاب الأصلية]({link})\n\n"
        )

    body = _FIGURE_TAG.sub(render_original_figure, body).strip()
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
