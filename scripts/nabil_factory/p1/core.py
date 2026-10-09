from __future__ import annotations

# ==============================================================================
# AUTOMATIC BOOK -> TOC -> LESSONS -> ACTIVITIES/EXERCISES INDEX
# ============================================================================== 
BOOK_INDEX_DIR = ROOT / "data/factory_book_indexes"
BOOK_INDEX_DIR.mkdir(parents=True, exist_ok=True)

_TOC_HINT_RE = re.compile(
    r"(?i)(contents?|table\s+of\s+contents?|sommaire|table\s+des\s+mati[eè]res|فهرس|المحتويات)"
)

_EXERCISE_RE = re.compile(
    r"(?im)^\s*(exercise|exercises|activity|activities|problem|problems|"
    r"application|applications|practice|worksheet|exercice|exercices|"
    r"activité|activités|problème|problèmes|تمرين|تمارين|نشاط|أنشطة|مسألة|مسائل|تطبيق|تطبيقات)"
    r"(?:\s*(?:no\.?|n°|#)?\s*(\d+[A-Za-z]?))?\s*[:.\-–—)]?\s*(.*)$"
)


def _book_index_safe_id(book_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", str(book_id or "").strip())


def _clean_toc_title(value: str) -> str:
    value = re.sub(r"\s+", " ", str(value or "")).strip(" .\t-–—")
    value = re.sub(
        r"(?i)^(chapter|unit|lesson|chapitre|unité|leçon|درس|وحدة|فصل)"
        r"\s*(?:\d+[A-Za-z]?)?\s*[:.\-–—]*\s*", "", value
    ).strip()
    return value


_BOOK_INDEX_TEXT_CACHE: Dict[Tuple[int, int], str] = {}


def _page_is_scanned(page) -> bool:
    """True when a page is essentially a full-page image (scanned textbook)."""
    try:
        page_area = max(float(page.rect.width * page.rect.height), 1.0)
        for image in page.get_images(full=True):
            for rect in page.get_image_rects(image[0]):
                if float(rect.width * rect.height) / page_area >= 0.80:
                    return True
    except Exception:
        pass
    return False


def _render_book_page_image(page, *, dpi: int = 300) -> Path:
    """Render the real PDF page to an image before reading it.

    This is the same input strategy used for scanned curriculum pages: the
    physical page is rendered first, so indexing never depends on a missing or
    broken hidden text layer.
    """
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    tmp.close()
    path = Path(tmp.name)
    page.get_pixmap(dpi=dpi, alpha=False).save(str(path))
    return path


def _local_ocr_from_page_image(image_path: Path) -> str:
    """Read a rendered curriculum page locally; try layouts useful for TOCs."""
    if not shutil.which("tesseract"):
        return ""
    candidates = []
    for psm in (3, 6, 11):
        try:
            res = subprocess.run(
                ["tesseract", str(image_path), "stdout", "-l", "eng+fra+ara",
                 "--oem", "1", "--psm", str(psm)],
                capture_output=True, text=True, timeout=45,
            )
            txt = re.sub(r"\r\n?", "\n", res.stdout or "").strip()
            if txt:
                # Prefer useful structure, not just maximum character count.
                numbered = sum(1 for line in txt.splitlines()
                               if re.search(r"\b\d{1,4}\s*$", line.strip()))
                score = len(txt) + numbered * 120
                candidates.append((score, txt))
        except Exception:
            continue
    return max(candidates, key=lambda x: x[0])[1] if candidates else ""


def _page_text_for_book_index(doc, pdf_page: int) -> str:
    """Read a book page from the rendered page image when needed.

    Native text is used only for genuinely text-based pages. Scanned/image
    books are rendered to PNG and OCR-read locally, matching the proven
    PDF->page-image->reading path instead of trusting page.get_text().
    """
    if pdf_page < 1 or pdf_page > len(doc):
        return ""
    key = (id(doc), int(pdf_page))
    if key in _BOOK_INDEX_TEXT_CACHE:
        return _BOOK_INDEX_TEXT_CACHE[key]

    page = doc[pdf_page - 1]
    try:
        native = re.sub(r"\r\n?", "\n", page.get_text("text") or "").strip()
    except Exception:
        native = ""
    scanned = _page_is_scanned(page)

    if len(native) >= 60 and not scanned:
        _BOOK_INDEX_TEXT_CACHE[key] = native
        return native

    image_path = None
    ocr_text = ""
    try:
        image_path = _render_book_page_image(page, dpi=300 if scanned else 240)
        ocr_text = _local_ocr_from_page_image(image_path)
        if ocr_text:
            progress("BOOK_INDEX_RENDERED_PAGE_READ", page=pdf_page,
                     scanned=scanned, chars=len(ocr_text))
    except Exception as exc:
        progress("BOOK_INDEX_RENDERED_PAGE_READ_FAILED", page=pdf_page, error=str(exc))
    finally:
        if image_path:
            try:
                image_path.unlink(missing_ok=True)
            except Exception:
                pass

    final = ocr_text if len(ocr_text) >= max(20, len(native)) else native
    _BOOK_INDEX_TEXT_CACHE[key] = final
    return final

def _toc_numbered_line(line: str) -> bool:
    line = str(line or "").strip()
    # OCR often collapses dot leaders / columns to one space.
    return bool(re.search(r"\b\d{1,4}\s*$", line) and
                len(re.sub(r"\d{1,4}\s*$", "", line).strip(" .-–—\t")) >= 3)


def _detect_toc_pages(doc, max_scan_pages: int = 40) -> List[int]:
    candidates = []
    limit = min(len(doc), max_scan_pages)
    for pdf_page in range(1, limit + 1):
        text = _page_text_for_book_index(doc, pdf_page)
        if not text:
            continue
        lines = [x.strip() for x in text.splitlines() if x.strip()]
        numbered_lines = sum(1 for line in lines if _toc_numbered_line(line))
        if _TOC_HINT_RE.search(text) or numbered_lines >= 4:
            candidates.append(pdf_page)
    if not candidates:
        return []

    expanded = set(candidates)
    for p in list(candidates):
        for neighbor in (p - 1, p + 1):
            if 1 <= neighbor <= limit:
                nxt = _page_text_for_book_index(doc, neighbor)
                numbered = sum(1 for line in nxt.splitlines() if _toc_numbered_line(line))
                if numbered >= 3:
                    expanded.add(neighbor)
    return sorted(expanded)


def _parse_toc_entries(doc, toc_pages: List[int]) -> List[dict]:
    entries = []
    for toc_pdf_page in toc_pages:
        text = _page_text_for_book_index(doc, toc_pdf_page)
        for raw_line in text.splitlines():
            line = re.sub(r"\s+", " ", raw_line).strip()
            if not line:
                continue
            match = re.match(r"^(?P<title>.+?)(?:\s*\.{2,}\s*|\s+)(?P<page>\d{1,4})\s*$", line)
            if not match:
                continue
            raw_title = match.group("title")
            # Keep the real title but remove a standalone chapter/unit ordinal
            # commonly emitted by OCR at the left edge of a TOC row.
            raw_title = re.sub(r"^\s*(?:chapter|chapitre|unit|unité|lesson|leçon)?\s*\d{1,3}\s*[:.\-–—]?\s+", "", raw_title, flags=re.I)
            title = _clean_toc_title(raw_title)
            try:
                printed_page = int(match.group("page"))
            except ValueError:
                continue
            if len(title) < 3 or _TOC_HINT_RE.fullmatch(title):
                continue
            if printed_page < 1:
                continue
            entries.append({
                "title": title,
                "printed_page": printed_page,
                "toc_pdf_page": toc_pdf_page,
                "toc_line": raw_line.strip(),
            })
    unique, seen = [], set()
    for item in entries:
        key = (item["title"].casefold(), item["printed_page"])
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique


def _candidate_pdf_offsets(doc, toc_entries: List[dict]) -> List[int]:
    """Resolve printed->physical offset without OCR-scanning the whole book repeatedly."""
    offsets = []
    for entry in toc_entries[:20]:
        tokens = [
            token.casefold() for token in re.findall(r"\w+", entry["title"], flags=re.UNICODE)
            if len(token) >= 4
        ]
        if not tokens:
            continue
        printed = int(entry["printed_page"])
        # Textbooks normally differ by front-matter offset. Search only plausible range.
        lo = max(1, printed - 10)
        hi = min(len(doc), printed + 60)
        for pdf_page in range(lo, hi + 1):
            text = _page_text_for_book_index(doc, pdf_page).casefold()
            hits = sum(1 for token in tokens if token in text)
            required = 1 if len(tokens) == 1 else min(2, len(tokens))
            if hits >= required:
                offsets.append(pdf_page - printed)
                break
    return offsets


def _resolve_printed_to_pdf_offset(doc, toc_entries: List[dict]) -> int:
    offsets = _candidate_pdf_offsets(doc, toc_entries)
    if offsets:
        counts = {}
        for offset in offsets:
            counts[offset] = counts.get(offset, 0) + 1
        best_offset, votes = max(counts.items(), key=lambda pair: pair[1])
        if votes >= 2 or len(toc_entries) < 2:
            return best_offset

    # Deterministic fallback: use PDF page labels when the document exposes them.
    label_votes = []
    for pdf_page in range(1, len(doc) + 1):
        try:
            label = str(doc[pdf_page - 1].get_label() or "").strip()
        except Exception:
            label = ""
        if label.isdigit():
            label_votes.append(pdf_page - int(label))
    if label_votes:
        counts = {}
        for offset in label_votes:
            if -10 <= offset <= 60:
                counts[offset] = counts.get(offset, 0) + 1
        if counts:
            return max(counts.items(), key=lambda pair: pair[1])[0]

    raise RuntimeError(
        "BOOK_INDEX_PAGE_OFFSET_UNVERIFIED: could not map printed TOC pages to physical PDF pages"
    )

def _lesson_slug(book_id: str, number: int) -> str:
    return f"{_book_index_safe_id(book_id).upper()}-AUTO-{number:03d}"


def _extract_lesson_works(doc, start_page: int, end_page: int) -> List[dict]:
    works = []
    sequence = 0
    for pdf_page in range(start_page, end_page + 1):
        text = _page_text_for_book_index(doc, pdf_page)
        for line_no, raw_line in enumerate(text.splitlines(), 1):
            line = re.sub(r"\s+", " ", raw_line).strip()
            if not line:
                continue
            match = _EXERCISE_RE.match(line)
            if not match:
                continue
            sequence += 1
            label = (match.group(1) or "").strip()
            printed_number = (match.group(2) or "").strip()
            remainder = (match.group(3) or "").strip()
            kind_lower = label.casefold()
            if any(x in kind_lower for x in ("activity", "activité", "نشاط", "أنشطة")):
                work_type = "activity"
            elif any(x in kind_lower for x in ("problem", "problème", "مسألة", "مسائل")):
                work_type = "problem"
            else:
                work_type = "exercise"
            works.append({
                "work_id": f"W{sequence:03d}",
                "type": work_type,
                "label": label,
                "printed_number": printed_number or None,
                "pdf_page": pdf_page,
                "line_number": line_no,
                "source_heading": line,
                "source_preview": remainder[:500],
            })
    return works


def _iter_canonical_lesson_entries(catalog: dict):
    """Yield every lesson-like record from supported canonical catalog shapes."""
    if not isinstance(catalog, dict):
        return
    lessons = catalog.get("lessons")
    if isinstance(lessons, list):
        for entry in lessons:
            if isinstance(entry, dict):
                yield entry
        return
    for grade_value in catalog.values():
        if not isinstance(grade_value, dict):
            continue
        for subject_value in grade_value.values():
            if isinstance(subject_value, dict) and isinstance(subject_value.get("lessons"), list):
                for entry in subject_value["lessons"]:
                    if isinstance(entry, dict):
                        yield entry
            elif isinstance(subject_value, list):
                for entry in subject_value:
                    if isinstance(entry, dict):
                        yield entry


def _drive_list_curriculum_pdfs(drive_service=None) -> List[dict]:
    """Discover curriculum PDFs strictly below the configured Drive root.

    Primary path: recursive parent traversal.
    Recovery path: search visible PDFs/shortcuts and prove ancestry back to the
    configured curriculum root.  The recovery path never admits an unrelated
    PDF merely because it is visible to the OAuth credential.
    """
    if drive_service is None:
        drive_service = get_drive_service()

    folder_mime = "application/vnd.google-apps.folder"
    shortcut_mime = "application/vnd.google-apps.shortcut"
    pdf_mime = "application/pdf"
    configured_root_id = resolve_drive_root_id()
    root_id = configured_root_id

    def _get_item(file_id: str) -> dict:
        return drive_service.files().get(
            fileId=file_id,
            fields=("id,name,mimeType,description,parents,"
                    "shortcutDetails(targetId,targetMimeType)"),
            supportsAllDrives=True,
        ).execute()

    root_meta = _get_item(root_id)
    if str(root_meta.get("mimeType") or "") == shortcut_mime:
        details = root_meta.get("shortcutDetails") or {}
        target_id = str(details.get("targetId") or "").strip()
        target_mime = str(details.get("targetMimeType") or "").strip()
        if not target_id:
            raise RuntimeError("CURRICULUM_DRIVE_ROOT_SHORTCUT_INVALID")
        if target_mime == pdf_mime:
            return [{
                "book_id": target_id,
                "name": str(root_meta.get("name") or f"{target_id}.pdf"),
                "drive_path": str(root_meta.get("name") or "").strip(),
                "description": str(root_meta.get("description") or ""),
            }]
        if target_mime != folder_mime:
            raise RuntimeError(
                f"CURRICULUM_DRIVE_ROOT_NOT_FOLDER:{target_mime or 'unknown'}")
        root_id = target_id
        root_meta = _get_item(root_id)

    root_mime = str(root_meta.get("mimeType") or "")
    if root_mime == pdf_mime:
        return [{
            "book_id": root_id,
            "name": str(root_meta.get("name") or f"{root_id}.pdf"),
            "drive_path": str(root_meta.get("name") or "").strip(),
            "description": str(root_meta.get("description") or ""),
        }]
    if root_mime != folder_mime:
        raise RuntimeError(
            f"CURRICULUM_DRIVE_ROOT_NOT_FOLDER:{root_mime or 'unknown'}")

    out: List[dict] = []
    seen_pdfs = set()

    def _append_pdf(book_id: str, name: str, path: str, description: str) -> None:
        book_id = str(book_id or "").strip()
        if not book_id or book_id in seen_pdfs:
            return
        seen_pdfs.add(book_id)
        out.append({
            "book_id": book_id,
            "name": str(name or f"{book_id}.pdf").strip(),
            "drive_path": str(path or name or "").strip("/"),
            "description": str(description or ""),
        })

    # Normal recursive traversal first.  This is fast when Drive exposes folder
    # children normally to the active OAuth identity.
    queue = [(root_id, "")]
    seen_folders = set()
    while queue:
        folder_id, parent_path = queue.pop(0)
        if folder_id in seen_folders:
            continue
        seen_folders.add(folder_id)
        token = None
        while True:
            resp = drive_service.files().list(
                q=f"'{folder_id}' in parents and trashed=false",
                spaces="drive",
                fields=("nextPageToken,files(id,name,mimeType,description,parents,"
                        "shortcutDetails(targetId,targetMimeType))"),
                pageSize=1000,
                pageToken=token,
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
            ).execute()
            for item in resp.get("files") or []:
                item_id = str(item.get("id") or "").strip()
                name = str(item.get("name") or "").strip()
                path = f"{parent_path}/{name}".strip("/")
                mime = str(item.get("mimeType") or "")
                description = str(item.get("description") or "")

                effective_id = item_id
                effective_mime = mime
                if mime == shortcut_mime:
                    details = item.get("shortcutDetails") or {}
                    effective_id = str(details.get("targetId") or "").strip()
                    effective_mime = str(details.get("targetMimeType") or "").strip()
                    if not effective_id:
                        continue

                if effective_mime == folder_mime:
                    queue.append((effective_id, path))
                elif effective_mime == pdf_mime or name.casefold().endswith(".pdf"):
                    _append_pdf(effective_id, name, path, description)
            token = resp.get("nextPageToken")
            if not token:
                break

    if out:
        progress("CURRICULUM_DRIVE_DISCOVERY", root=root_id,
                 method="recursive_parents", pdf_count=len(out))
        return out

    # Some shared/My-Drive layouts allow direct file access but do not enumerate
    # children reliably from the configured root.  Recover by searching visible
    # PDF files/shortcuts, then PROVE that the item itself descends from root.
    # This is intentionally not a global-PDF fallback.
    meta_cache = {root_id: root_meta}

    def _meta(file_id: str) -> Optional[dict]:
        file_id = str(file_id or "").strip()
        if not file_id:
            return None
        if file_id in meta_cache:
            return meta_cache[file_id]
        try:
            meta_cache[file_id] = _get_item(file_id)
        except Exception:
            meta_cache[file_id] = None
        return meta_cache[file_id]

    def _is_descendant(item: dict) -> bool:
        frontier = [str(x) for x in (item.get("parents") or []) if str(x).strip()]
        visited = set()
        while frontier:
            parent_id = frontier.pop()
            if parent_id == root_id:
                return True
            if parent_id in visited:
                continue
            visited.add(parent_id)
            parent = _meta(parent_id)
            if not parent:
                continue
            frontier.extend(
                str(x) for x in (parent.get("parents") or []) if str(x).strip())
        return False

    token = None
    while True:
        resp = drive_service.files().list(
            q=("trashed=false and (mimeType='application/pdf' or "
               "mimeType='application/vnd.google-apps.shortcut')"),
            spaces="drive",
            fields=("nextPageToken,files(id,name,mimeType,description,parents,"
                    "shortcutDetails(targetId,targetMimeType))"),
            pageSize=1000,
            pageToken=token,
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        ).execute()
        for item in resp.get("files") or []:
            if not _is_descendant(item):
                continue
            item_id = str(item.get("id") or "").strip()
            name = str(item.get("name") or "").strip()
            mime = str(item.get("mimeType") or "")
            description = str(item.get("description") or "")
            effective_id = item_id
            effective_mime = mime
            if mime == shortcut_mime:
                details = item.get("shortcutDetails") or {}
                effective_id = str(details.get("targetId") or "").strip()
                effective_mime = str(details.get("targetMimeType") or "").strip()
            if effective_id and (effective_mime == pdf_mime or name.casefold().endswith(".pdf")):
                _append_pdf(effective_id, name, name, description)
        token = resp.get("nextPageToken")
        if not token:
            break

    if out:
        progress("CURRICULUM_DRIVE_DISCOVERY", root=root_id,
                 method="verified_ancestry_search", pdf_count=len(out))
        return out

    raise RuntimeError(
        f"CURRICULUM_DRIVE_NO_PDFS: configured_root={configured_root_id}; "
        f"resolved_root={root_id}; root is readable, recursive enumeration "
        "returned no PDFs, and ancestry-verified Drive search found no PDFs "
        "below that root")

def _discover_lesson_boundaries_without_toc(doc) -> List[dict]:
    """Find evidence-backed lesson starts when a printed TOC is absent/unreadable.

    This deliberately does NOT split by arbitrary page counts. A boundary is
    accepted only when an OCR/native-text page contains a strong lesson/chapter
    heading. If evidence is insufficient the caller fails closed.
    """
    explicit = re.compile(
        r"(?i)^\s*(?:chapter|unit|lesson|chapitre|unité|leçon|"
        r"الفصل|الوحدة|الدرس)\s*(?:[0-9ivxlcdm]+|[A-Z]|[٠-٩]+)?\s*[:.\-–—]?\s*(.+?)\s*$")
    starts = []
    for pdf_page in range(1, len(doc) + 1):
        text = _page_text_for_book_index(doc, pdf_page)
        lines = [re.sub(r"\s+", " ", x).strip() for x in text.splitlines() if x.strip()]
        for line in lines[:18]:
            m = explicit.match(line)
            if not m:
                continue
            title = _clean_toc_title(line)
            if len(title) < 3 or len(title) > 160:
                continue
            starts.append({
                "title": title, "printed_page": pdf_page,
                "toc_pdf_page": None, "toc_line": line,
                "pdf_start_page": pdf_page, "boundary_source": "verified_heading",
            })
            break
    deduped, seen_pages = [], set()
    for item in starts:
        if item["pdf_start_page"] not in seen_pages:
            seen_pages.add(item["pdf_start_page"]); deduped.append(item)
    if len(deduped) < 2:
        raise RuntimeError(
            "BOOK_INDEX_LESSON_BOUNDARIES_UNVERIFIED: no TOC and fewer than two verified lesson/chapter headings")
    return deduped


def _registered_books_from_catalog() -> List[dict]:
    """Return one metadata record per unique registered source book."""
    catalog = load_canonical_catalog()
    books = {}
    for entry in _iter_canonical_lesson_entries(catalog):
        book_id = str(entry.get("book_id") or "").strip()
        if not book_id:
            continue
        meta = books.setdefault(book_id, {"book_id": book_id})
        for key in ("grade", "subject", "language", "branch", "track"):
            value = entry.get(key)
            if value not in (None, "") and key not in meta:
                meta[key] = value
    # The canonical catalog is optional for discovery. Drive is authoritative
    # for finding curriculum PDFs; an empty catalog must not block indexing.
    return list(books.values())


def _metadata_for_book(book_id: str) -> dict:
    for meta in _registered_books_from_catalog():
        if meta["book_id"] == book_id:
            return meta
    return {"book_id": book_id}


def build_all_registered_book_indexes(drive_service=None, force: bool = False) -> dict:
    """Index every unique book registered in the canonical catalog, truthfully."""
    catalog_books = {m["book_id"]: m for m in _registered_books_from_catalog()}
    discovered = _drive_list_curriculum_pdfs(drive_service=drive_service)
    books = []
    for item in discovered:
        meta = dict(item)
        meta.update(catalog_books.get(item["book_id"], {}))
        books.append(meta)
    report = {
        "status": "RUNNING",
        "schema": "NABIL_ALL_BOOK_INDEX_V1",
        "generated_at": now(),
        "book_count": len(books),
        "indexed": [],
        "failed": [],
    }
    progress("ALL_BOOK_INDEX_START", books=len(books))
    for position, meta in enumerate(books, 1):
        book_id = meta["book_id"]
        try:
            result = build_book_lesson_index(
                book_id,
                drive_service=drive_service,
                force=force,
                book_metadata=meta,
            )
            report["indexed"].append({
                "book_id": book_id,
                "position": position,
                "lesson_count": result.get("lesson_count", 0),
                "work_count": result.get("work_count", 0),
                "index_path": str(BOOK_INDEX_DIR / f"{_book_index_safe_id(book_id)}.json"),
            })
        except Exception as exc:
            report["failed"].append({
                "book_id": book_id,
                "position": position,
                "error": f"{type(exc).__name__}: {exc}",
            })
            progress("ALL_BOOK_INDEX_BOOK_FAILED", book_id=book_id, error=str(exc))
    report["indexed_count"] = len(report["indexed"])
    report["failed_count"] = len(report["failed"])
    report["status"] = "INDEXED" if not report["failed"] else "PARTIAL_FAILURE"
    report["completed_at"] = now()
    summary_path = BOOK_INDEX_DIR / "_all_books_report.json"
    summary_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    progress("ALL_BOOK_INDEX_COMPLETE", indexed=report["indexed_count"], failed=report["failed_count"], output=str(summary_path))
    return report



def _normalize_grade_selector(value: Any) -> Optional[int]:
    """Normalize CLI/catalog grade values such as 7, G07, EB7 or Grade 7."""
    if value in (None, ""):
        return None
    if isinstance(value, int):
        return value
    text = str(value).strip()
    match = re.search(r"(\d{1,2})", text)
    if not match:
        raise RuntimeError(f"GRADE_SELECTOR_INVALID: {value}")
    return int(match.group(1))


def _normalize_subject_selector(value: Any) -> str:
    """Use the same subject aliases as the teaching engine."""
    text = str(value or "").strip().casefold().replace(" ", "_")
    return SUBJECT_ALIASES.get(text, text)


def _book_matches_scope(meta: dict, grade: Any = None, subject: Any = None) -> bool:
    wanted_grade = _normalize_grade_selector(grade)
    wanted_subject = _normalize_subject_selector(subject) if subject not in (None, "") else ""
    if wanted_grade is not None:
        try:
            actual_grade = _normalize_grade_selector(meta.get("grade"))
        except RuntimeError:
            return False
        if actual_grade != wanted_grade:
            return False
    if wanted_subject:
        actual_subject = _normalize_subject_selector(meta.get("subject"))
        if actual_subject != wanted_subject:
            return False
    return True


def _probe_drive_book_metadata(meta: dict, drive_service=None) -> dict:
    """Infer scope metadata without requiring TOC/lesson indexing to succeed."""
    import fitz
    book_id = str(meta.get("book_id") or "").strip()
    if not book_id:
        raise RuntimeError("BOOK_METADATA_PROBE_MISSING_BOOK_ID")
    pdf_path = resolve_source_book_pdf(book_id, drive_service=drive_service)
    doc = fitz.open(str(pdf_path))
    try:
        if len(doc) < 1:
            raise RuntimeError("BOOK_INDEX_EMPTY_PDF")
        return _infer_book_metadata_for_index(book_id, drive_service, doc, meta)
    finally:
        doc_id = id(doc)
        for cache_key in [k for k in _BOOK_INDEX_TEXT_CACHE if k[0] == doc_id]:
            _BOOK_INDEX_TEXT_CACHE.pop(cache_key, None)
        doc.close()


def build_scoped_book_indexes(
        drive_service=None, force: bool = False,
        grade: Any = None, subject: Any = None) -> dict:
    """Index every registered book matching a grade and/or subject selector."""
    catalog_books = {m["book_id"]: m for m in _registered_books_from_catalog()}
    discovered = _drive_list_curriculum_pdfs(drive_service=drive_service)
    books = []
    # Prefer metadata already proven by the catalog/name/path. Unknown books are
    # indexed once so cover OCR can infer their real grade/subject; no random PDF
    # is ever relabelled as the requested scope.
    for item in discovered:
        meta = dict(item)
        meta.update(catalog_books.get(item["book_id"], {}))
        if _book_matches_scope(meta, grade=grade, subject=subject):
            books.append(meta)
            continue
        if not meta.get("grade") or not meta.get("subject"):
            try:
                inferred = _probe_drive_book_metadata(meta, drive_service=drive_service)
                if _book_matches_scope(inferred, grade=grade, subject=subject):
                    books.append(inferred)
            except Exception as exc:
                progress("SCOPED_BOOK_DISCOVERY_SKIPPED", book_id=meta.get("book_id"), error=str(exc))
    if not books:
        raise RuntimeError(
            f"BOOK_INDEX_SCOPE_EMPTY_AFTER_DRIVE_DISCOVERY: grade={grade!r} subject={subject!r}")

    report = {
        "status": "RUNNING",
        "schema": "NABIL_SCOPED_BOOK_INDEX_V1",
        "generated_at": now(),
        "grade": _normalize_grade_selector(grade),
        "subject": _normalize_subject_selector(subject) if subject not in (None, "") else None,
        "book_count": len(books),
        "indexed": [],
        "failed": [],
    }
    progress(
        "SCOPED_BOOK_INDEX_START", books=len(books),
        grade=report["grade"], subject=report["subject"])

    for position, meta in enumerate(books, 1):
        book_id = meta["book_id"]
        try:
            result = build_book_lesson_index(
                book_id,
                drive_service=drive_service,
                force=force,
                book_metadata=meta,
            )
            report["indexed"].append({
                "book_id": book_id,
                "position": position,
                "grade": meta.get("grade"),
                "subject": meta.get("subject"),
                "lesson_count": result.get("lesson_count", 0),
                "work_count": result.get("work_count", 0),
                "index_path": str(
                    BOOK_INDEX_DIR / f"{_book_index_safe_id(book_id)}.json"),
            })
        except Exception as exc:
            report["failed"].append({
                "book_id": book_id,
                "position": position,
                "error": f"{type(exc).__name__}: {exc}",
            })
            progress(
                "SCOPED_BOOK_INDEX_BOOK_FAILED",
                book_id=book_id, error=str(exc))

    report["indexed_count"] = len(report["indexed"])
    report["failed_count"] = len(report["failed"])
    report["status"] = "INDEXED" if not report["failed"] else "PARTIAL_FAILURE"
    report["completed_at"] = now()
    progress(
        "SCOPED_BOOK_INDEX_COMPLETE",
        indexed=report["indexed_count"], failed=report["failed_count"])
    return report


def _indexed_lessons_for_scope(grade: Any = None, subject: Any = None) -> List[dict]:
    """Read discovered lessons from completed per-book indexes for a scope."""
    lessons: List[dict] = []
    for index_path in sorted(BOOK_INDEX_DIR.glob("*.json")):
        if index_path.name.startswith("_"):
            continue
        try:
            payload = json.loads(index_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if payload.get("status") != "INDEXED":
            continue
        for entry in payload.get("lessons") or []:
            if isinstance(entry, dict) and _book_matches_scope(
                    entry, grade=grade, subject=subject):
                lessons.append(entry)
    return lessons


def resolve_lesson_selector(
        lesson: str, grade: Any = None, subject: Any = None) -> dict:
    """Resolve a lesson by exact/fuzzy title inside the requested grade/subject."""
    needle = re.sub(r"\s+", " ", str(lesson or "")).strip().casefold()
    if not needle:
        raise RuntimeError("LESSON_SELECTOR_EMPTY")

    candidates = _indexed_lessons_for_scope(grade=grade, subject=subject)
    exact = [
        e for e in candidates
        if re.sub(r"\s+", " ", str(e.get("canonical_title") or "")).strip().casefold() == needle
        or str(e.get("lesson_id") or "").strip().casefold() == needle
    ]
    if len(exact) == 1:
        return exact[0]
    if len(exact) > 1:
        raise RuntimeError(
            "LESSON_SELECTOR_AMBIGUOUS: " +
            "; ".join(f"{e.get('lesson_id')}={e.get('canonical_title')}" for e in exact[:20]))

    partial = [
        e for e in candidates
        if needle in re.sub(r"\s+", " ", str(e.get("canonical_title") or "")).strip().casefold()
    ]
    if len(partial) == 1:
        return partial[0]
    if len(partial) > 1:
        raise RuntimeError(
            "LESSON_SELECTOR_AMBIGUOUS: " +
            "; ".join(f"{e.get('lesson_id')}={e.get('canonical_title')}" for e in partial[:20]))
    raise RuntimeError(
        f"LESSON_SELECTOR_NOT_FOUND: lesson={lesson!r} grade={grade!r} subject={subject!r}")

def _infer_book_metadata_for_index(book_id: str, drive_service, doc, metadata: dict) -> dict:
    """Fill missing grade/subject/language from Drive filename + locally read cover pages."""
    out = dict(metadata or {})
    name = ""
    if drive_service:
        try:
            meta = drive_service.files().get(fileId=book_id, fields="name,description").execute()
            name = str(meta.get("name") or "")
            out["source_name"] = name
        except Exception:
            pass

    sample_parts = [name]
    for page_num in range(1, min(len(doc), 8) + 1):
        sample_parts.append(_page_text_for_book_index(doc, page_num))
    sample = "\n".join(sample_parts)
    folded = sample.casefold()

    if out.get("grade") in (None, ""):
        m = re.search(r"(?i)\b(?:grade|eb|basic\s+education\s+grade)\s*[-:]?\s*(\d{1,2})\b", sample)
        if m:
            out["grade"] = int(m.group(1))
        else:
            # OCR occasionally reads Eight as Tight; filename is preferred when available.
            words = {"seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12}
            for word, number in words.items():
                if re.search(rf"(?i)\bgrade\s+{word}\b", sample):
                    out["grade"] = number
                    break

    if not out.get("subject"):
        subject_patterns = [
            ("mathematics", r"\b(mathematics|mathématiques|maths?)\b|رياضيات"),
            ("physics", r"\b(physics|physique)\b|فيزياء"),
            ("chemistry", r"\b(chemistry|chimie)\b|كيمياء"),
            ("biology", r"\b(biology|biologie)\b|أحياء"),
            ("general_science", r"\b(general\s+science|sciences?)\b|علوم"),
            ("english_language", r"\benglish\b|الإنجليزية|الانجليزية"),
            ("french_language", r"\b(french|français)\b|الفرنسية"),
            ("arabic_language", r"\barabic\b|العربية"),
        ]
        for subject, pattern in subject_patterns:
            if re.search(pattern, folded, flags=re.I):
                out["subject"] = subject
                break

    if not out.get("language"):
        # Prefer explicit filename markers, then script/subject hints.
        if re.search(r"(?i)\b(french|français|francais)\b", name):
            out["language"] = "fr"
        elif re.search(r"(?i)\b(english|anglais)\b", name):
            out["language"] = "en"
        elif re.search(r"[\u0600-\u06ff]", sample):
            out["language"] = "ar"
        elif re.search(r"\b(le|la|les|des|chapitre|exercice)\b", folded):
            out["language"] = "fr"
        else:
            out["language"] = "en"

    out.setdefault("book_id", book_id)
    return out


def build_book_lesson_index(book_id: str, drive_service=None, force: bool = False, book_metadata: Optional[dict] = None) -> dict:
    """Drive/local PDF -> TOC -> lessons -> page ranges -> linked activities/exercises."""
    import fitz

    safe_id = _book_index_safe_id(book_id)
    book_metadata = dict(book_metadata or _metadata_for_book(book_id))
    output_path = BOOK_INDEX_DIR / f"{safe_id}.json"
    if output_path.exists() and not force:
        try:
            existing = json.loads(output_path.read_text(encoding="utf-8"))
            if existing.get("book_id") == book_id and existing.get("status") == "INDEXED" and existing.get("lessons"):
                progress("BOOK_INDEX_CACHE_HIT", book_id=book_id, lessons=len(existing["lessons"]))
                return existing
        except Exception:
            pass

    pdf_path = resolve_source_book_pdf(book_id, drive_service=drive_service)
    doc = fitz.open(str(pdf_path))
    try:
        if len(doc) < 1:
            raise RuntimeError("BOOK_INDEX_EMPTY_PDF")
        book_metadata = _infer_book_metadata_for_index(
            book_id, drive_service, doc, book_metadata)
        progress("BOOK_INDEX_START", book_id=book_id, pdf_pages=len(doc),
                 grade=book_metadata.get("grade"), subject=book_metadata.get("subject"),
                 language=book_metadata.get("language"))
        toc_pages = _detect_toc_pages(doc)
        toc_entries = _parse_toc_entries(doc, toc_pages) if toc_pages else []
        if toc_entries:
            offset = _resolve_printed_to_pdf_offset(doc, toc_entries)
            valid_entries = []
            for entry in toc_entries:
                pdf_start = entry["printed_page"] + offset
                if 1 <= pdf_start <= len(doc):
                    valid_entries.append({**entry, "pdf_start_page": pdf_start,
                                          "boundary_source": "printed_toc"})
        else:
            progress("BOOK_INDEX_TOC_FALLBACK_TO_VERIFIED_HEADINGS", book_id=book_id)
            offset = None
            valid_entries = _discover_lesson_boundaries_without_toc(doc)
        valid_entries.sort(key=lambda x: (x["pdf_start_page"], x["printed_page"]))

        deduped, seen_starts = [], set()
        for item in valid_entries:
            if item["pdf_start_page"] not in seen_starts:
                seen_starts.add(item["pdf_start_page"])
                deduped.append(item)
        if not deduped:
            raise RuntimeError("BOOK_INDEX_NO_VALID_LESSON_STARTS")

        lessons = []
        for idx, item in enumerate(deduped):
            start_page = item["pdf_start_page"]
            end_page = deduped[idx + 1]["pdf_start_page"] - 1 if idx + 1 < len(deduped) else len(doc)
            if end_page < start_page:
                raise RuntimeError(f"BOOK_INDEX_INVALID_LESSON_RANGE: {item['title']} {start_page}-{end_page}")
            lesson_id = _lesson_slug(book_id, idx + 1)
            works = _extract_lesson_works(doc, start_page, end_page)
            lesson = {
                "lesson_id": lesson_id,
                "canonical_title": item["title"],
                "book_id": book_id,
                "grade": book_metadata.get("grade"),
                "subject": book_metadata.get("subject"),
                "language": book_metadata.get("language"),
                "branch": book_metadata.get("branch") or book_metadata.get("track") or "",
                "toc_pdf_page": item["toc_pdf_page"],
                "printed_start_page": item["printed_page"],
                "pdf_start_page": start_page,
                "pdf_end_page": end_page,
                "works": works,
                "activities": [w for w in works if w["type"] == "activity"],
                "exercises": [w for w in works if w["type"] in ("exercise", "problem")],
            }
            lessons.append(lesson)
            progress(
                "BOOK_INDEX_LESSON", book_id=book_id, lesson_id=lesson_id,
                title=item["title"], pages=f"{start_page}-{end_page}", works=len(works)
            )

        result = {
            "status": "INDEXED",
            "schema": "NABIL_BOOK_INDEX_V1",
            "generated_at": now(),
            "book_id": book_id,
            "book_metadata": book_metadata,
            "index_method": "printed_toc" if toc_entries else "verified_headings",
            "source_pdf": str(pdf_path),
            "pdf_pages": len(doc),
            "toc_pdf_pages": toc_pages,
            "printed_to_pdf_offset": offset,
            "lesson_count": len(lessons),
            "work_count": sum(len(lesson["works"]) for lesson in lessons),
            "lessons": lessons,
        }
        tmp = output_path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(output_path)
        progress(
            "BOOK_INDEX_COMPLETE", book_id=book_id, lessons=result["lesson_count"],
            works=result["work_count"], output=str(output_path)
        )
        return result
    finally:
        doc_id = id(doc)
        for cache_key in [k for k in _BOOK_INDEX_TEXT_CACHE if k[0] == doc_id]:
            _BOOK_INDEX_TEXT_CACHE.pop(cache_key, None)
        doc.close()


def load_canonical_catalog() -> dict:
    candidates = [CATALOG_PATH, ROOT / "config/canonical_lessons_catalog.json", ROOT / "canonical_lessons_catalog.json", ROOT / "lessons_catalog.json"]
    for c in candidates:
        if c.exists():
            try:
                data = json.loads(c.read_text(encoding="utf-8"))
                if isinstance(data, dict) and data:
                    return data
            except Exception:
                pass
    raise RuntimeError("CANONICAL_CATALOG_NOT_FOUND")


def resolve_canonical_entry(lesson_id: str) -> dict:
    catalog = load_canonical_catalog()
    found = None
    if "lessons" in catalog and isinstance(catalog["lessons"], list):
        for e in catalog["lessons"]:
            if e.get("lesson_id", "").upper() == lesson_id.upper():
                found = e
                break
    else:
        for g_k, g_v in catalog.items():
            if isinstance(g_v, dict):
                for s_k, s_v in g_v.items():
                    if isinstance(s_v, dict) and "lessons" in s_v:
                        for e in s_v["lessons"]:
                            if e.get("lesson_id", "").upper() == lesson_id.upper():
                                found = e
                                break
                    elif isinstance(s_v, list):
                        for e in s_v:
                            if isinstance(e, dict) and e.get("lesson_id", "").upper() == lesson_id.upper():
                                found = e
                                break

    if not found:
        # Book factory discovers source chapter records automatically; its
        # cached indexes extend the old one-pilot catalog, never replace it.
        # On-Demand routes can resolve lessons from the same source index.
        for book_index in sorted((ROOT / "data/factory_book_indexes").glob("*.json")):
            try:
                source = json.loads(book_index.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            for entry in source.get("lessons", []):
                if entry.get("lesson_id", "").upper() == lesson_id.upper():
                    found = entry
                    break
            if found:
                break

    if not found:
        raise RuntimeError(f"LESSON_NOT_FOUND_IN_CATALOG: {lesson_id}")

    required = ["lesson_id", "canonical_title", "grade", "subject", "book_id", "pdf_start_page", "pdf_end_page", "language"]
    for f in required:
        if f not in found or found[f] is None:
            raise RuntimeError(f"CANONICAL_CATALOG_CORRUPT: Missing mandatory field '{f}' in {lesson_id}")

    return found


def assert_authorized_source_vision(
        lesson_id: str, book_id: str, pdf_page: int,
        provider_override: Optional[str] = None):
    """Require explicit owner consent for at least one eligible provider.

    When a concrete provider produced stored evidence, provider_override pins
    revalidation to that exact provider. Otherwise the configured failover pool
    is checked so an unauthorized primary cannot block an authorized fallback.
    """
    context = {
        "lesson_id": lesson_id,
        "book_id": book_id,
        "pdf_page": pdf_page,
    }
    if provider_override:
        if _vision_provider_authorized(
                provider_override, context, require_key=True):
            return
        raise RuntimeError(
            "VISION_SHARING_NOT_AUTHORIZED: "
            f"provider={provider_override} lesson_id={lesson_id} "
            f"page={pdf_page}")

    preferred = os.getenv(
        "NABIL_FACTORY_AI_PROVIDER", "auto").strip().lower()
    keys = _provider_keys()
    candidates = _provider_order(preferred, keys)
    authorized = [
        p for p in candidates
        if _vision_provider_authorized(
            p, context, require_key=True)
    ]
    if authorized:
        return
    raise RuntimeError(
        "VISION_SHARING_NOT_AUTHORIZED: "
        f"providers={candidates} lesson_id={lesson_id} page={pdf_page}")



# ==============================================================================
# 6. MULTIMODAL EXTRACTION: TRUE VISION PAYLOAD, TOC & VECTOR GROUPING
# ==============================================================================
def extract_page_text_robust(doc, page_num: int, lesson_id: str, book_id: str, cache_dir: Path) -> str:
    page = doc[page_num - 1]
    txt = (page.get_text() or "").strip()
    scanned = any(
        (rect.width * rect.height) / (page.rect.width * page.rect.height) >= 0.80
        for image in page.get_images(full=True)
        for rect in page.get_image_rects(image[0])
    )
    # A scanned textbook can contain a partial/low-quality hidden OCR layer.
    # For source segmentation, re-read the real page locally at high resolution
    # instead of accepting a merely "long enough" hidden text layer.
    if len(txt) >= 60 and not scanned:
        return txt

    image_path = None
    try:
        image_path = _render_book_page_image(page, dpi=300 if scanned else 240)
        ocr_txt = _local_ocr_from_page_image(image_path)
        if len(ocr_txt) >= 60:
            progress(
                "SOURCE_PAGE_RENDERED_OCR_SELECTED",
                page=page_num, scanned=scanned, chars=len(ocr_txt),
            )
            return ocr_txt
    except Exception:
        pass
    finally:
        if image_path:
            try:
                image_path.unlink(missing_ok=True)
            except Exception:
                pass

    assert_authorized_source_vision(lesson_id, book_id, page_num)
    page_img = cache_dir / f"page_vision_{page_num}.png"
    page.get_pixmap(dpi=150).save(str(page_img))
    b64_img = base64.b64encode(page_img.read_bytes()).decode("utf-8")
    prompt = "Extract all text, exercises, and formulas verbatim from this curriculum page. Return JSON: {'text': str}"
    res = execute_llm_completion(
        prompt, json_mode=True, image_base64=b64_img,
        vision_context={
            "lesson_id": lesson_id,
            "book_id": book_id,
            "pdf_page": page_num,
        },
        operation=f"page_text_vision_p{page_num}",
        unit_id=f"page:{page_num}:text")
    return json.loads(res).get("text", "")


def extract_multimodal_page_figures(doc, page_num: int, cache_dir: Path,
                                    lesson_id: str, book_id: str) -> List[Dict[str, Any]]:
    """Find actual figure regions. A scanned full-page bitmap is not a figure."""
    import fitz
    from PIL import Image

    page = doc[page_num - 1]
    figures = []
    has_scanned_page = False
    for idx, img in enumerate(page.get_images(full=True)):
        xref = img[0]
        rects = page.get_image_rects(xref)
        if not rects:
            continue
        for rect in rects:
            area = (rect.width * rect.height) / (page.rect.width * page.rect.height)
            if area >= 0.80:
                has_scanned_page = True
                continue
            extracted = doc.extract_image(xref)
            try:
                with Image.open(io.BytesIO(extracted["image"])) as picture:
                    out = io.BytesIO()
                    picture.convert("RGB").save(out, format="PNG")
                    img_bytes = out.getvalue()
            except Exception as exc:
                raise RuntimeError(f"FIGURE_EVIDENCE_MISSING: unreadable embedded image p{page_num}: {exc}")
            path = cache_dir / f"fig_p{page_num}_embedded_{idx+1}.png"
            path.write_bytes(img_bytes)
            cap_area = fitz.Rect(max(0, rect.x0 - 15), rect.y1,
                                 min(page.rect.width, rect.x1 + 15),
                                 min(page.rect.height, rect.y1 + 50))
            caption = page.get_text("text", clip=cap_area).strip()
            match = re.search(r"(?:fig(?:ure)?\.?|شكل|وثيقة)\s*(\d+[a-z]?)", caption, re.I)
            label = match.group(1).lower() if match else None
            figures.append({
                "figure_id": f"FIG_P{page_num}_E{idx+1}",
                "printed_number": int(re.match(r"\d+", label).group()) if label else None,
                "printed_label": label,
                "source_page": page_num,
                "bbox": [rect.x0, rect.y0, rect.x1, rect.y1],
                "caption": caption,
                "image_path": str(path),
                "image_sha256": hashlib.sha256(img_bytes).hexdigest(),
                "visual_occupancy": round(area, 3),
                "evidence_method": "EMBEDDED_IMAGE_WITH_SOURCE_BBOX"
            })

    # Vector diagrams are cropped from the genuine PDF geometry.
    if not has_scanned_page:
        for idx, drawing in enumerate(page.get_drawings()):
            rect = drawing["rect"]
            if rect.width < 60 or rect.height < 60:
                continue
            pix = page.get_pixmap(clip=rect, dpi=180)
            path = cache_dir / f"fig_p{page_num}_vector_{idx+1}.png"
            content = pix.tobytes("png")
            path.write_bytes(content)
            figures.append({
                "figure_id": f"FIG_P{page_num}_V{idx+1}", "printed_number": None,
                "printed_label": None, "source_page": page_num,
                "bbox": [rect.x0, rect.y0, rect.x1, rect.y1],
                "caption": "Source PDF vector region", "image_path": str(path),
                "image_sha256": hashlib.sha256(content).hexdigest(),
                "visual_occupancy": round(
                    rect.width * rect.height / (page.rect.width * page.rect.height), 3),
                "evidence_method": "PDF_VECTOR_CROP"
            })

    if has_scanned_page:
        # OCR cannot reveal where Fig. 3a, Fig. 3b, etc. are. Ask an approved
        # vision provider for coordinates, then crop *the original PDF page*.
        assert_authorized_source_vision(lesson_id, book_id, page_num)
        pix = page.get_pixmap(dpi=180)
        prompt = (
            "Inspect this original scanned school textbook page. Return ONLY JSON "
            "with a figures array. Identify each actual labelled Fig./Figure diagram "
            "or photo separately; never return the whole page or a paragraph. "
            "Each figure has printed_label (e.g. 3a, 3b, 6 or null), "
            "bbox_1000=[left,top,right,bottom] normalized to 0..1000, "
            "caption (verbatim when readable), visual_description and confidence 0..1. "
            "Do not invent diagram labels or content. Empty array if none."
        )
        page_image = base64.b64encode(pix.tobytes("png")).decode("ascii")
        extracted = None
        response_shape = "no response"
        # A vision model may return valid JSON with the WRONG root object.
        # Re-ask on the SAME approved source page, never fabricate a box and
        # never weaken downstream source-figure matching / scientific review.
        for attempt in range(1, 3):
            request_prompt = prompt
            if attempt == 2:
                request_prompt += (
                    '\\nYour previous reply did NOT match the required structure. '
                    'Use precisely this JSON root shape: '
                    '{"figures":[{"printed_label":"3a","bbox_1000":'
                    '[100,120,450,390],"caption":"","visual_description":'
                    '"","confidence":0.9}]}. The example is ONLY a schema '
                    'illustration, NOT evidence: replace all values solely '
                    'with figures actually visible in the attached page. '
                    'If the page contains no figures, reply {"figures":[]}. '
                    'Do not return any other keys or explanations.'
                )
            raw_figures = execute_llm_completion(
                request_prompt, json_mode=True, image_base64=page_image,
                vision_context={
                    "lesson_id": lesson_id,
                    "book_id": book_id,
                    "pdf_page": page_num,
                },
                operation=f"page_figure_detection_p{page_num}",
                unit_id=f"page:{page_num}:figures")
            vision_provenance = get_last_llm_provenance()
            try:
                proposed = json.loads(raw_figures)
            except (ValueError, TypeError):
                response_shape = "invalid_json"
                proposed = None
            if isinstance(proposed, dict):
                response_shape = ",".join(sorted(str(k)[:40] for k in proposed))[:160] or "empty_object"
                if isinstance(proposed.get("figures"), list):
                    extracted = proposed
                    break
                # Groq JSON mode can wrap the requested figures in "list" or
                # return a SINGLE figure object. Normalize structure only:
                # coordinates, labels, confidence and scientific evidence are
                # still independently validated below.
                if (set(proposed) == {"list"}
                        and isinstance(proposed["list"], list)
                        and all(isinstance(v, dict) for v in proposed["list"])):
                    extracted = {"figures": proposed["list"]}
                    progress("FIGURE_VISION_SCHEMA_NORMALIZED", page=page_num,
                             original_shape="list", figure_candidates=len(proposed["list"]))
                    break
                if "bbox_1000" in proposed and "confidence" in proposed:
                    extracted = {"figures": [proposed]}
                    progress("FIGURE_VISION_SCHEMA_NORMALIZED", page=page_num,
                             original_shape="single_figure", figure_candidates=1)
                    break
            elif isinstance(proposed, list):
                response_shape = "array"
                if all(isinstance(v, dict) for v in proposed):
                    extracted = {"figures": proposed}
                    progress("FIGURE_VISION_SCHEMA_NORMALIZED", page=page_num,
                             original_shape="array", figure_candidates=len(proposed))
                    break
            elif proposed is not None:
                response_shape = type(proposed).__name__
            progress("FIGURE_VISION_SCHEMA_CHECK", page=page_num,
                     attempt=attempt, valid=extracted is not None,
                     response_shape=response_shape)
        if extracted is None:
            raise RuntimeError(
                f"FIGURE_EVIDENCE_MISSING: page={page_num} vision figure "
                f"schema invalid after 2 attempts; response_shape={response_shape}"
            )
        progress("FIGURE_VISION_SCHEMA_VALID", page=page_num,
                 figure_candidates=len(extracted["figures"]))
        rejected_figures = []
        for idx, info in enumerate(extracted["figures"]):
            if not isinstance(info, dict):
                rejected_figures.append("not_an_object")
                continue
            try:
                confidence = float(info.get("confidence", 0))
            except (ValueError, TypeError):
                confidence = 0.0
            if confidence < 0.75:
                rejected_figures.append("low_or_missing_confidence")
                continue
            coords = info.get("bbox_1000")
            if (not isinstance(coords, list) or len(coords) != 4
                    or not all(isinstance(v, (int, float)) for v in coords)):
                continue
            x0, y0, x1, y1 = [float(v) for v in coords]
            if not (0 <= x0 < x1 <= 1000 and 0 <= y0 < y1 <= 1000
                    and (x1-x0) >= 25 and (y1-y0) >= 25):
                continue
            rect = fitz.Rect(page.rect.x0 + x0*page.rect.width/1000,
                             page.rect.y0 + y0*page.rect.height/1000,
                             page.rect.x0 + x1*page.rect.width/1000,
                             page.rect.y0 + y1*page.rect.height/1000)
            label_raw = str(info.get("printed_label") or "").strip().lower()
            label_match = re.fullmatch(
                r"(?:fig(?:ure)?\.?\s*)?(\d+)([a-z]?)\.?",
                label_raw, re.I)
            if not label_match:
                # The model sometimes puts the authentic "Fig. 1" label in
                # caption instead of printed_label. Accept this exact
                # structural format, not an inferred figure number.
                label_match = re.match(
                    r"\s*(?:fig(?:ure)?\.?\s*)(\d+)([a-z]?)(?![\da-z])",
                    str(info.get("caption") or "").lower(), re.I)
            label = (label_match.group(1) + label_match.group(2)
                     if label_match else "")
            # Never infer figure numbers by left-to-right order. On genuine
            # scanned pages, captions are often *below* the vision bounding
            # box and Groq may omit printed_label. Read ONLY the adjoining
            # physical caption strip using LOCAL OCR; the figure number must
            # appear directly next to this source image, not elsewhere on page.
            if shutil.which("tesseract"):
                caption_rect = fitz.Rect(
                    max(page.rect.x0, rect.x0 - 4),
                    max(page.rect.y0, rect.y1 - 12),
                    min(page.rect.x1, rect.x1 + 4),
                    min(page.rect.y1, rect.y1 + 56),
                )
                if caption_rect.width > 25 and caption_rect.height > 15:
                    with tempfile.TemporaryDirectory(
                            prefix="nabil_caption_") as cap_dir:
                        cap_path = Path(cap_dir) / "caption.png"
                        page.get_pixmap(clip=caption_rect, dpi=300).save(
                            str(cap_path))
                        cap_proc = subprocess.run(
                            ["tesseract", str(cap_path), "stdout",
                             "-l", "eng+fra", "--psm", "6"],
                            capture_output=True, text=True, timeout=16)
                    if cap_proc.returncode == 0:
                        caption_source = cap_proc.stdout.strip()
                        source_labels = {
                            m.group(1) + m.group(2).lower()
                            for m in re.finditer(
                                r"(?i)\bfig(?:ure)?[\.,:]?\s*"
                                r"(\d+)([a-z]?)\s*[:;\.,]?",
                                caption_source)
                        }
                        if len(source_labels) == 1:
                            source_label = next(iter(source_labels))
                            if label and label != source_label:
                                progress("FIGURE_LABEL_SOURCE_CONFLICT",
                                         page=page_num,
                                         claimed=label, source=source_label)
                                continue
                            label = source_label
                            label_match = re.fullmatch(
                                r"(\d+)([a-z]?)", label)
                            progress("FIGURE_LABEL_LOCAL_SOURCE_VERIFIED",
                                     page=page_num, figure_label=label,
                                     caption_excerpt=caption_source[:120])
                        elif len(source_labels) > 1:
                            progress("FIGURE_CAPTION_AMBIGUOUS",
                                     page=page_num,
                                     labels=sorted(source_labels))
                            continue
            content = page.get_pixmap(clip=rect, dpi=180).tobytes("png")
            path = cache_dir / f"fig_p{page_num}_scanned_{idx+1}.png"
            path.write_bytes(content)
            figures.append({
                "figure_id": f"FIG_P{page_num}_SCAN_{idx+1}",
                "printed_number": int(label_match.group(1)) if label_match else None,
                "printed_label": label or None, "source_page": page_num,
                "bbox": [rect.x0, rect.y0, rect.x1, rect.y1],
                "caption": str(info.get("caption") or ""),
                "visual_description": str(info.get("visual_description") or ""),
                "image_path": str(path),
                "image_sha256": hashlib.sha256(content).hexdigest(),
                "visual_occupancy": round(
                    rect.width*rect.height/(page.rect.width*page.rect.height), 3),
                "confidence": confidence,
                "ai_provenance": dict(vision_provenance),
                "evidence_method": "APPROVED_VISION_BOX_CROPPED_FROM_SOURCE_PDF"
            })
        progress("FIGURE_VISION_CROPS_VERIFIED", page=page_num,
                 candidates=len(extracted["figures"]),
                 accepted=len(figures),
                 printed_labels=[f.get("printed_label") for f in figures],
                 rejected=rejected_figures[:8])
    return figures


def _normalize_targeted_figure_payload(payload: Any, page_num: int) -> List[dict]:
    """Normalize only container shape; scientific/source checks happen later."""
    if isinstance(payload, list):
        progress("TARGETED_FIGURE_SCHEMA_NORMALIZED", page=page_num,
                 original_shape="array", candidates=len(payload))
        return payload
    if isinstance(payload, dict):
        figures = payload.get("figures")
        if isinstance(figures, list):
            progress("TARGETED_FIGURE_SCHEMA_VALID", page=page_num,
                     original_shape="object.figures", candidates=len(figures))
            return figures
        for key in ("list", "items", "data"):
            figures = payload.get(key)
            if isinstance(figures, list):
                progress("TARGETED_FIGURE_SCHEMA_NORMALIZED", page=page_num,
                         original_shape=f"object.{key}",
                         candidates=len(figures))
                return figures
    raise RuntimeError(
        f"FIGURE_EVIDENCE_MISSING: targeted rescue schema invalid p{page_num}")


def rescue_missing_labeled_figures(doc, page_num: int, cache_dir: Path,
                                   lesson_id: str, book_id: str,
                                   missing_labels: set,
                                   existing_figures: List[Dict[str, Any]]
                                   ) -> List[Dict[str, Any]]:
    """Second-pass rescue for source labels missed by the normal vision pass.

    Vision proposes image/caption boxes at higher resolution; LOCAL OCR of the
    proposed caption box must independently verify exactly that printed label.
    No figure number is inferred from order or neighboring figures.
    """
    import fitz

    wanted = {
        str(label).strip().lower() for label in missing_labels
        if re.fullmatch(r"\d+[a-z]?", str(label).strip().lower())
    }
    existing = {
        str(f.get("printed_label") or "").strip().lower()
        for f in existing_figures
    }
    wanted -= existing
    if not wanted:
        return []

    assert_authorized_source_vision(lesson_id, book_id, page_num)
    page = doc[page_num - 1]
    page_png = page.get_pixmap(dpi=300).tobytes("png")
    page_b64 = base64.b64encode(page_png).decode("ascii")
    prompt = (
        "TARGETED SOURCE-FIGURE RESCUE. Inspect this original textbook page at "
        "high resolution. Locate ONLY these missing printed figure labels: "
        f"{sorted(wanted)}. For each label that is actually visible, return "
        "one object with printed_label, image_bbox_1000 (the image/diagram only, "
        "not neighboring figures), caption_bbox_1000 (tight box containing its "
        "printed 'Fig. N' caption), and confidence 0..1. Never infer a label "
        "from left-to-right order. Never merge two figures into one box. "
        "If a requested printed label cannot be seen, omit it. Return JSON "
        "exactly as {'figures':[...]} and no explanation."
    )
    raw = execute_llm_completion(
        prompt, json_mode=True, image_base64=page_b64,
        vision_context={
            "lesson_id": lesson_id,
            "book_id": book_id,
            "pdf_page": page_num,
        },
        operation=f"figure_rescue_p{page_num}",
        unit_id=f"page:{page_num}:figure_rescue")
    rescue_provenance = get_last_llm_provenance()
    candidates = _normalize_targeted_figure_payload(
        json.loads(raw), page_num)

    def norm_rect(coords):
        if (not isinstance(coords, list) or len(coords) != 4
                or not all(isinstance(v, (int, float)) for v in coords)):
            return None
        x0, y0, x1, y1 = [float(v) for v in coords]
        if not (0 <= x0 < x1 <= 1000 and 0 <= y0 < y1 <= 1000):
            return None
        return fitz.Rect(
            page.rect.x0 + x0 * page.rect.width / 1000,
            page.rect.y0 + y0 * page.rect.height / 1000,
            page.rect.x0 + x1 * page.rect.width / 1000,
            page.rect.y0 + y1 * page.rect.height / 1000,
        )

    def local_caption_fallback(label: str, image_rect):
        """Locate an exact source Fig/Figure label by LOCAL full-page OCR.

        This is used only when the provider's proposed caption box is wrong.
        The external model still proposes the figure image box; local OCR must
        independently find exactly one matching printed label physically next
        to that box. Nothing is inferred from figure order.
        """
        with tempfile.TemporaryDirectory(
                prefix="nabil_targeted_page_ocr_") as page_ocr_dir:
            full_path = Path(page_ocr_dir) / "page.png"
            full_pix = page.get_pixmap(dpi=350)
            full_pix.save(str(full_path))
            proc = subprocess.run(
                ["tesseract", str(full_path), "stdout",
                 "-l", "eng+fra", "--psm", "6", "tsv"],
                capture_output=True, text=True, timeout=35)
        if proc.returncode != 0 or not proc.stdout.strip():
            return None

        rows = []
        raw_lines = proc.stdout.splitlines()
        if not raw_lines:
            return None
        header = raw_lines[0].split("\t")
        for raw_line in raw_lines[1:]:
            cols = raw_line.split("\t")
            if len(cols) != len(header):
                continue
            row = dict(zip(header, cols))
            if row.get("level") != "5":
                continue
            token = str(row.get("text") or "").strip()
            if not token:
                continue
            try:
                row["_left"] = int(row["left"])
                row["_top"] = int(row["top"])
                row["_width"] = int(row["width"])
                row["_height"] = int(row["height"])
            except (KeyError, TypeError, ValueError):
                continue
            rows.append(row)

        grouped = {}
        for row in rows:
            key = (
                row.get("block_num"), row.get("par_num"),
                row.get("line_num"))
            grouped.setdefault(key, []).append(row)

        occurrences = []
        wanted_norm = re.sub(r"[^0-9a-z]", "", label.casefold())
        for line_rows in grouped.values():
            line_rows.sort(key=lambda row: row["_left"])
            for pos, row in enumerate(line_rows):
                token = str(row.get("text") or "")
                token_letters = re.sub(
                    r"[^a-z]", "", token.casefold())
                match_rows = None
                if re.fullmatch(
                        rf"(?i)fig(?:ure)?[\.,:]?{re.escape(wanted_norm)}[\.:;]?",
                        token):
                    match_rows = [row]
                elif token_letters in ("fig", "figure"):
                    for nxt in line_rows[pos + 1:pos + 3]:
                        nxt_norm = re.sub(
                            r"[^0-9a-z]", "",
                            str(nxt.get("text") or "").casefold())
                        if nxt_norm == wanted_norm:
                            match_rows = [row, nxt]
                            break
                if not match_rows:
                    continue

                px0 = min(r["_left"] for r in match_rows)
                py0 = min(r["_top"] for r in match_rows)
                px1 = max(r["_left"] + r["_width"] for r in match_rows)
                py1 = max(r["_top"] + r["_height"] for r in match_rows)
                label_rect = fitz.Rect(
                    page.rect.x0 + px0 * page.rect.width / full_pix.width,
                    page.rect.y0 + py0 * page.rect.height / full_pix.height,
                    page.rect.x0 + px1 * page.rect.width / full_pix.width,
                    page.rect.y0 + py1 * page.rect.height / full_pix.height,
                )
                horizontal_gap = max(
                    0.0, image_rect.x0 - label_rect.x1,
                    label_rect.x0 - image_rect.x1)
                vertical_gap = max(
                    0.0, image_rect.y0 - label_rect.y1,
                    label_rect.y0 - image_rect.y1)
                # A real caption should be very close to its figure. This
                # rejects body text such as "Observe figure 1" elsewhere.
                if (horizontal_gap <= page.rect.width * 0.12
                        and vertical_gap <= page.rect.height * 0.08):
                    occurrences.append(label_rect)

        if len(occurrences) != 1:
            progress(
                "TARGETED_FIGURE_LOCAL_PAGE_LABEL_AMBIGUOUS",
                page=page_num, label=label,
                adjacent_matches=len(occurrences))
            return None

        label_rect = occurrences[0]
        caption_rect = fitz.Rect(
            max(page.rect.x0,
                image_rect.x0 - page.rect.width * 0.015),
            max(page.rect.y0,
                label_rect.y0 - page.rect.height * 0.008),
            min(page.rect.x1,
                image_rect.x1 + page.rect.width * 0.015),
            min(page.rect.y1,
                label_rect.y1 + page.rect.height * 0.018),
        )
        progress(
            "TARGETED_FIGURE_LOCAL_PAGE_LABEL_VERIFIED",
            page=page_num, label=label,
            method="FULL_PAGE_LOCAL_OCR_ADJACENT_TO_MODEL_IMAGE")
        return caption_rect

    rescued = []
    for idx, item in enumerate(candidates):
        if not isinstance(item, dict):
            continue
        raw_label = str(item.get("printed_label") or "").strip().lower()
        m = re.fullmatch(r"(?:fig(?:ure)?\.?\s*)?(\d+)([a-z]?)\.?",
                         raw_label, re.I)
        label = (m.group(1) + m.group(2).lower()) if m else ""
        if label not in wanted:
            continue
        try:
            confidence = float(item.get("confidence", 0))
        except (TypeError, ValueError):
            confidence = 0.0
        if confidence < 0.80:
            progress("TARGETED_FIGURE_RESCUE_REJECTED", page=page_num,
                     label=label, reason="LOW_CONFIDENCE")
            continue

        image_rect = norm_rect(item.get("image_bbox_1000"))
        caption_rect = norm_rect(item.get("caption_bbox_1000"))
        if image_rect is None or caption_rect is None:
            progress("TARGETED_FIGURE_RESCUE_REJECTED", page=page_num,
                     label=label, reason="INVALID_BBOX")
            continue
        if image_rect.width < 20 or image_rect.height < 20:
            progress("TARGETED_FIGURE_RESCUE_REJECTED", page=page_num,
                     label=label, reason="IMAGE_BBOX_TOO_SMALL")
            continue

        # A model may return an extremely tight box around the printed
        # "Fig. N" token. Expand only the caption box locally before OCR;
        # the actual figure crop is never enlarged or inferred. Acceptance
        # still requires unique LOCAL OCR of the requested source label.
        if caption_rect.width < 24 or caption_rect.height < 14:
            cx = (caption_rect.x0 + caption_rect.x1) / 2
            cy = (caption_rect.y0 + caption_rect.y1) / 2
            half_w = max(12.0, caption_rect.width / 2 + 8.0)
            half_h = max(7.0, caption_rect.height / 2 + 5.0)
            caption_rect = fitz.Rect(
                max(page.rect.x0, cx - half_w),
                max(page.rect.y0, cy - half_h),
                min(page.rect.x1, cx + half_w),
                min(page.rect.y1, cy + half_h),
            )
            progress("TARGETED_FIGURE_CAPTION_BOX_PADDED",
                     page=page_num, label=label,
                     width=round(caption_rect.width, 1),
                     height=round(caption_rect.height, 1))

        # The caption must be physically close to its proposed source figure;
        # this prevents a valid Fig. 1 caption elsewhere on the page from
        # authorizing the wrong crop.
        horizontal_gap = max(
            0.0, image_rect.x0 - caption_rect.x1,
            caption_rect.x0 - image_rect.x1)
        vertical_gap = max(
            0.0, image_rect.y0 - caption_rect.y1,
            caption_rect.y0 - image_rect.y1)
        if (horizontal_gap > page.rect.width * 0.12
                or vertical_gap > page.rect.height * 0.16):
            progress("TARGETED_FIGURE_RESCUE_REJECTED", page=page_num,
                     label=label, reason="CAPTION_NOT_ADJACENT")
            continue

        with tempfile.TemporaryDirectory(
                prefix="nabil_targeted_caption_") as cap_dir:
            cap_path = Path(cap_dir) / "caption.png"
            page.get_pixmap(
                clip=caption_rect, dpi=350).save(str(cap_path))
            proc = subprocess.run(
                ["tesseract", str(cap_path), "stdout",
                 "-l", "eng+fra", "--psm", "6"],
                capture_output=True, text=True, timeout=20)
        if proc.returncode != 0:
            progress("TARGETED_FIGURE_RESCUE_REJECTED", page=page_num,
                     label=label, reason="LOCAL_OCR_FAILED")
            continue

        caption_source = proc.stdout.strip()
        source_labels = {
            mm.group(1) + mm.group(2).lower()
            for mm in re.finditer(
                r"(?i)\bfig(?:ure)?[\.,:]?\s*"
                r"(\d+)([a-z]?)\s*[:;\.,]?",
                caption_source)
        }
        if source_labels != {label}:
            # The provider may have returned a caption box on nearby body
            # text even when its image box is correct. Do not trust or widen
            # that box blindly. Re-locate the requested printed label using
            # LOCAL full-page OCR and require a unique occurrence physically
            # adjacent to the proposed source image.
            fallback_rect = local_caption_fallback(label, image_rect)
            if fallback_rect is not None:
                with tempfile.TemporaryDirectory(
                        prefix="nabil_targeted_caption_fallback_") as cap_dir:
                    cap_path = Path(cap_dir) / "caption.png"
                    page.get_pixmap(
                        clip=fallback_rect, dpi=350).save(str(cap_path))
                    retry_proc = subprocess.run(
                        ["tesseract", str(cap_path), "stdout",
                         "-l", "eng+fra", "--psm", "6"],
                        capture_output=True, text=True, timeout=20)
                if retry_proc.returncode == 0:
                    retry_source = retry_proc.stdout.strip()
                    retry_labels = {
                        mm.group(1) + mm.group(2).lower()
                        for mm in re.finditer(
                            r"(?i)\bfig(?:ure)?[\.,:]?\s*"
                            r"(\d+)([a-z]?)\s*[:;\.,]?",
                            retry_source)
                    }
                    if retry_labels == {label}:
                        caption_rect = fallback_rect
                        caption_source = retry_source
                        source_labels = retry_labels
                        progress(
                            "TARGETED_FIGURE_CAPTION_RECOVERED_LOCALLY",
                            page=page_num, label=label,
                            caption_excerpt=caption_source[:120])

        if source_labels != {label}:
            progress("TARGETED_FIGURE_RESCUE_REJECTED", page=page_num,
                     label=label,
                     reason="LOCAL_CAPTION_LABEL_NOT_UNIQUE",
                     source_labels=sorted(source_labels),
                     caption_excerpt=caption_source[:120])
            continue

        image_bytes = page.get_pixmap(
            clip=image_rect, dpi=220).tobytes("png")
        path = cache_dir / (
            f"fig_p{page_num}_targeted_{label}_{idx+1}.png")
        path.write_bytes(image_bytes)
        rescued.append({
            "figure_id": f"FIG_P{page_num}_TARGET_{label}",
            "printed_number": int(re.match(r"\d+", label).group()),
            "printed_label": label,
            "source_page": page_num,
            "bbox": [
                image_rect.x0, image_rect.y0,
                image_rect.x1, image_rect.y1,
            ],
            "caption": caption_source,
            "visual_description": "",
            "image_path": str(path),
            "image_sha256": hashlib.sha256(image_bytes).hexdigest(),
            "visual_occupancy": round(
                image_rect.width * image_rect.height /
                (page.rect.width * page.rect.height), 3),
            "confidence": confidence,
            "ai_provenance": dict(rescue_provenance),
            "evidence_method":
                "TARGETED_HIGHRES_VISION_PLUS_LOCAL_CAPTION_OCR",
        })
        progress("TARGETED_FIGURE_RESCUE_ACCEPTED", page=page_num,
                 label=label, caption_excerpt=caption_source[:120])

    return rescued


def match_figure_to_item(item: dict, page_figures: List[Dict[str, Any]], page_rect) -> List[str]:
    """Match by source figure number/letter, never by any random image on page."""
    prompt = item.get("exact_source_prompt", item.get("raw_text", ""))
    mentioned = re.findall(
        r"(?:fig(?:ure)?\.?|document|doc|شكل|وثيقة)\s*(\d+[a-z]?)",
        prompt, re.I,
    )
    wanted = {label.casefold() for label in mentioned}
    if wanted:
        matches = []
        for fig in page_figures:
            label = str(fig.get("printed_label") or "").casefold()
            number = str(fig.get("printed_number") or "")
            if any((w == label or (not re.search(r"[a-z]$", w) and w == number))
                   for w in wanted):
                matches.append(fig["figure_id"])
        if not matches:
            raise RuntimeError(f"FIGURE_EVIDENCE_MISSING: Source labelled figures {sorted(wanted)} were not extracted")
        return list(dict.fromkeys(matches))

    if item.get("requires_figure"):
        raise RuntimeError("FIGURE_EVIDENCE_MISSING: Diagram required but textbook figure identity is unverified")
    return []


def verify_title_double_evidence_strict(doc, entry: dict, opening_txt: str) -> bool:
    """Require both the chapter opener and the real book TOC. Never infer TOC
    from a filename or submit unauthorized preface pages to an AI provider.
    The canonical catalog records the TOC PDF page for scanned textbooks.
    """
    title_clean = re.sub(r"[^\w]+", " ", entry["canonical_title"].casefold()).strip()
    opener = re.sub(r"[^\w]+", " ", opening_txt.casefold())
    if not title_clean:
        return False
    if title_clean not in opener:
        # Stylized printed headers are often missed by full-page OCR even
        # when body text is readable. Re-read the real PDF header locally.
        import fitz
        page_no = int(entry["pdf_start_page"])
        page = doc[page_no - 1]
        r = page.rect
        header = page.get_pixmap(
            clip=fitz.Rect(r.x0, r.y0, r.x1, r.y0 + r.height * 0.20),
            dpi=300)
        with tempfile.TemporaryDirectory(prefix="nabil_title_ocr_") as directory:
            image_path = Path(directory) / "opening_header.png"
            header.save(str(image_path))
            proc = subprocess.run(
                ["tesseract", str(image_path), "stdout", "-l", "eng+fra",
                 "--psm", "6"],
                capture_output=True, text=True, timeout=35)
        if proc.returncode != 0:
            raise RuntimeError(
                f"TITLE_VERIFICATION_FAILED: chapter opening OCR unavailable p{page_no}")
        opener_header = re.sub(
            r"[^\w]+", " ", proc.stdout.casefold()).strip()
        if title_clean not in opener_header:
            progress("TITLE_OPENING_EVIDENCE_FAILED", page=page_no,
                     expected_title=entry["canonical_title"],
                     header_excerpt=opener_header[:180])
            return False
        progress("TITLE_OPENING_HEADER_VERIFIED", page=page_no,
                 title=entry["canonical_title"],
                 method="SOURCE_HEADER_LOCAL_OCR_300DPI")

    toc_page = entry.get("toc_pdf_page")
    if toc_page is None:
        # Native-text PDFs may expose a genuine PDF bookmark TOC.
        for depth, name, p_num in doc.get_toc():
            if re.sub(r"[^\w]+", " ", name.casefold()).strip() == title_clean:
                return 1 <= p_num <= int(entry["pdf_start_page"])
        return False

    toc_page = int(toc_page)
    if not 1 <= toc_page <= len(doc) or toc_page >= int(entry["pdf_start_page"]):
        return False
    toc_txt = (doc[toc_page - 1].get_text() or "").strip()
    if not toc_txt:
        if not shutil.which("tesseract"):
            raise RuntimeError("DEPENDENCY_MISSING:tesseract for scanned textbook TOC")
        # Local OCR: exactly the catalogued TOC page, NOT an external transfer.
        cache = CACHE_DIR / f"toc_{entry['book_id']}_p{toc_page}.txt"
        if cache.exists():
            toc_txt = cache.read_text(encoding="utf-8")
        else:
            with tempfile.TemporaryDirectory() as temp_dir:
                image_path = Path(temp_dir) / "toc.png"
                doc[toc_page - 1].get_pixmap(dpi=200).save(str(image_path))
                proc = subprocess.run(
                    ["tesseract", str(image_path), "stdout", "-l", "eng+fra", "--psm", "3"],
                    capture_output=True, text=True, timeout=60,
                )
            if proc.returncode != 0:
                raise RuntimeError("TITLE_VERIFICATION_FAILED: local TOC OCR unavailable")
            toc_txt = proc.stdout.strip()
            if toc_txt:
                cache.write_text(toc_txt, encoding="utf-8")
    toc_normalized = re.sub(r"[^\w]+", " ", toc_txt.casefold())

    # Dense page OCR (PSM 3) can miss short first-row titles on graphical TOC
    # pages even while correctly reading "TABLE OF CONTENTS". Before failing,
    # re-read the exact same catalogued TOC page locally with sparse modes.
    # This preserves strict double evidence; it does not infer a title from a
    # filename, manifest, or model.
    if title_clean not in toc_normalized and shutil.which("tesseract"):
        import fitz
        page = doc[toc_page - 1]
        with tempfile.TemporaryDirectory(prefix="nabil_toc_title_ocr_") as temp_dir:
            image_path = Path(temp_dir) / "toc_title.png"
            page.get_pixmap(dpi=260).save(str(image_path))
            sparse_parts = []
            for psm in (11, 12, 6):
                proc = subprocess.run(
                    ["tesseract", str(image_path), "stdout", "-l", "eng+fra",
                     "--psm", str(psm)],
                    capture_output=True, text=True, timeout=45,
                )
                if proc.returncode == 0 and proc.stdout.strip():
                    sparse_parts.append(proc.stdout)
                    sparse_normalized = re.sub(
                        r"[^\w]+", " ", proc.stdout.casefold())
                    if title_clean in sparse_normalized:
                        progress(
                            "TITLE_TOC_SPARSE_OCR_VERIFIED",
                            page=toc_page,
                            title=entry["canonical_title"],
                            psm=psm,
                        )
                        toc_txt = toc_txt + "\n" + proc.stdout
                        toc_normalized = re.sub(
                            r"[^\w]+", " ", toc_txt.casefold())
                        break

    return title_clean in toc_normalized and (
        "chapter" in toc_normalized or "chapitre" in toc_normalized
        or "contents" in toc_normalized or "فهرس" in toc_normalized
    )

def _execute_llm_json_strict(
        prompt: str,
        *,
        image_base64: Optional[str] = None,
        vision_context: Optional[Dict[str, Any]] = None,
        purpose: str = "factory_json",
        max_attempts: int = 3) -> Any:
    """Require parseable RFC-8259 JSON; retry from the original source if malformed.

    We deliberately do NOT repair malformed source transcriptions after the
    fact. A repair model could alter quoted textbook text. Instead, every retry
    re-reads the same authorized source image with a stricter serialization
    contract, preserving the source-first/fail-closed guarantee.
    """
    attempts = max(1, min(4, int(max_attempts)))
    base_prompt = str(prompt)
    strict_suffix = (
        "\n\nSTRICT JSON SERIALIZATION CONTRACT:\n"
        "- Return exactly one valid RFC-8259 JSON value and nothing else.\n"
        "- Use double quotes for every object key and every JSON string.\n"
        "- Escape every double quote, backslash, newline, tab, and other "
        "control character inside string values correctly.\n"
        "- No comments, no trailing commas, no Markdown fences, no Python "
        "dict syntax, and no explanatory text outside the JSON.\n"
        "- Preserve source wording exactly; serialization escaping must not "
        "change the underlying textbook text."
    )
    # A malformed JSON response is a provider-quality failure, not a reason
    # to ask the same provider for the same malformed serialization three
    # times. Rotate through configured/authorized providers while always
    # re-reading the ORIGINAL source image.
    configured = _provider_order(
        os.getenv("NABIL_FACTORY_AI_PROVIDER", "auto").strip().lower(),
        _provider_keys(),
    )
    if image_base64 and vision_context is not None:
        configured = [
            p for p in configured
            if _vision_provider_authorized(
                p, vision_context, require_key=True)
        ]
    if not configured:
        raise RuntimeError(
            "AI_JSON_RETRY_NO_AUTHORIZED_PROVIDER:"
            f"{purpose}")

    last_error = None
    malformed_providers = set()
    for attempt in range(1, attempts + 1):
        preferred_retry_provider = configured[(attempt - 1) % len(configured)]
        effective_prompt = (
            base_prompt if attempt == 1
            else base_prompt + strict_suffix +
            f"\nThis is strict JSON retry {attempt} of {attempts}."
        )
        raw = execute_llm_completion(
            effective_prompt,
            json_mode=True,
            temperature=0.0,
            image_base64=image_base64,
            vision_context=vision_context,
            preferred_provider_override=preferred_retry_provider,
            excluded_providers=malformed_providers,
            operation=purpose,
            unit_id=purpose,
        )
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            last_error = exc
            actual_bad_provider = get_last_llm_provenance().get("provider")
            if actual_bad_provider:
                malformed_providers.add(str(actual_bad_provider).lower())
            progress(
                "AI_JSON_INVALID_RETRY",
                purpose=purpose,
                attempt=attempt,
                max_attempts=attempts,
                line=exc.lineno,
                column=exc.colno,
                char=exc.pos,
                provider=get_last_llm_provenance().get("provider"),
                model=get_last_llm_provenance().get("model"),
                preferred_retry_provider=preferred_retry_provider,
                retry_provider_cycle=configured,
                excluded_after_malformed=sorted(malformed_providers),
                image_request=bool(image_base64),
                vision_context=vision_context if image_base64 else None,
            )
    raise RuntimeError(
        f"AI_JSON_INVALID_AFTER_RETRIES:{purpose}:"
        f"line={getattr(last_error, 'lineno', 0)}:"
        f"column={getattr(last_error, 'colno', 0)}"
    ) from last_error


def _normalize_exercise_scan_payload(payload: Any, page_num: int) -> List[dict]:
    """Accept the provider's semantically equivalent array/object JSON roots."""
    if isinstance(payload, list):
        progress("EXERCISE_VISION_SCHEMA_NORMALIZED", page=page_num,
                 original_shape="array", exercise_candidates=len(payload))
        return payload
    if isinstance(payload, dict):
        rows = payload.get("exercises")
        if isinstance(rows, list):
            progress("EXERCISE_VISION_SCHEMA_VALID", page=page_num,
                     original_shape="object.exercises",
                     exercise_candidates=len(rows))
            return rows
        for key in ("items", "list", "data"):
            rows = payload.get(key)
            if isinstance(rows, list):
                progress("EXERCISE_VISION_SCHEMA_NORMALIZED", page=page_num,
                         original_shape=f"object.{key}",
                         exercise_candidates=len(rows))
                return rows
    raise RuntimeError(
        f"EXERCISE_SOURCE_MISMATCH: invalid scan evidence p{page_num}")


def _normalize_exercise_review_payload(payload: Any, page_num: int) -> List[dict]:
    """Normalize the independent review response without weakening validation."""
    if isinstance(payload, list):
        progress("EXERCISE_REVIEW_SCHEMA_NORMALIZED", page=page_num,
                 original_shape="array", checks=len(payload))
        return payload
    if isinstance(payload, dict):
        checks = payload.get("checks")
        if isinstance(checks, list):
            progress("EXERCISE_REVIEW_SCHEMA_VALID", page=page_num,
                     original_shape="object.checks", checks=len(checks))
            return checks
        for key in ("items", "list", "data"):
            checks = payload.get(key)
            if isinstance(checks, list):
                progress("EXERCISE_REVIEW_SCHEMA_NORMALIZED", page=page_num,
                         original_shape=f"object.{key}", checks=len(checks))
                return checks
    raise RuntimeError(
        f"EXERCISE_SOURCE_MISMATCH: review missing p{page_num}")


def _rescue_unverified_exercise(
        page, row: dict, page_num: int, lesson_id: str, book_id: str) -> Optional[dict]:
    """Re-read one rejected exercise from a high-resolution source crop.

    This is stricter than accepting the first page transcription: the candidate
    bbox is cropped from the original PDF, re-transcribed, then independently
    audited against that exact crop. No guessed repair is allowed.
    """
    from fitz import Rect
    try:
        number = int(row.get("number"))
        coords = row.get("bbox_1000")
        if not isinstance(coords, list) or len(coords) != 4:
            return None
        x0, y0, x1, y1 = [float(v) for v in coords]
        if not (0 <= x0 < x1 <= 1000 and 0 <= y0 < y1 <= 1000):
            return None
    except (TypeError, ValueError):
        return None

    # Pad the proposed source region so the circled number and any nearby
    # figure reference are not clipped. Padding is presentation geometry only.
    px = page.rect.width * 0.035
    py = page.rect.height * 0.025
    rect = Rect(
        max(page.rect.x0, x0 * page.rect.width / 1000 - px),
        max(page.rect.y0, y0 * page.rect.height / 1000 - py),
        min(page.rect.x1, x1 * page.rect.width / 1000 + px),
        min(page.rect.y1, y1 * page.rect.height / 1000 + py),
    )
    crop_bytes = page.get_pixmap(clip=rect, dpi=320).tobytes("png")
    crop_b64 = base64.b64encode(crop_bytes).decode("ascii")
    context = {
        "lesson_id": lesson_id,
        "book_id": book_id,
        "pdf_page": page_num,
    }
    prompt = (
        f"This is a HIGH-RESOLUTION crop from the original textbook page. "
        f"Verify and transcribe ONLY the visibly printed exercise numbered {number}. "
        "Return one JSON object with: verified_visible_number (bool), number "
        "(integer), section_type (EXERCISE or PROBLEM), exact_source_prompt "
        "(all visible words and blanks verbatim, do not solve), subquestions "
        "(array of exact strings), figure_labels (array of exact printed figure "
        "labels), blank_count (integer), confidence (0..1), unreadable_parts "
        "(array). Represent EVERY visibly empty answer box, underline blank, or "
        "fill-in slot in exact_source_prompt with the literal token [BLANK] in "
        "its exact reading position. Empty boxes are source content and must not "
        "disappear. blank_count must equal the number of visible answer blanks. "
        "If the requested exercise number is not visibly present and readable "
        "in this crop, set verified_visible_number=false. Do not infer missing "
        "words and do not correct the textbook."
    )
    payload = _execute_llm_json_strict(
        prompt,
        image_base64=crop_b64,
        vision_context=context,
        purpose=f"exercise_rescue_extract_p{page_num}_n{number}",
    )
    if not isinstance(payload, dict):
        return None
    if payload.get("verified_visible_number") is not True:
        return None
    try:
        if int(payload.get("number")) != number:
            return None
        confidence = float(payload.get("confidence", 0))
    except (TypeError, ValueError):
        return None
    prompt_text = str(payload.get("exact_source_prompt") or "").strip()
    kind = str(payload.get("section_type") or "EXERCISE").upper()
    if (kind not in ("EXERCISE", "PROBLEM") or len(prompt_text) < 10
            or confidence < 0.90 or payload.get("unreadable_parts")):
        return None
    extraction_provenance = get_last_llm_provenance()

    audit_prompt = (
        f"Independently audit the proposed transcription of exercise {number} "
        "against this SAME original high-resolution crop. Return JSON object "
        "with faithful (bool), number_visible (bool), complete (bool), "
        "reason (string). Mark false for any missing word, invented word, "
        "wrong number, wrong item boundary, omitted visible subquestion, or "
        "a missing/misplaced [BLANK] token. Independently count the visible "
        "answer boxes/blanks in the crop and require that count to match "
        "blank_count and the number of [BLANK] tokens in exact_source_prompt. "
        "Proposed transcription: "
        + json.dumps(payload, ensure_ascii=False)
    )
    audit = _execute_llm_json_strict(
        audit_prompt,
        image_base64=crop_b64,
        vision_context=context,
        purpose=f"exercise_rescue_audit_p{page_num}_n{number}",
    )
    audit_provenance = get_last_llm_provenance()
    if not isinstance(audit, dict):
        return None
    if not (audit.get("faithful") is True
            and audit.get("number_visible") is True
            and audit.get("complete") is True):
        progress(
            "EXERCISE_TARGETED_RESCUE_REJECTED",
            page=page_num,
            number=number,
            reason=str(audit.get("reason") or "")[:240],
        )
        return None

    progress(
        "EXERCISE_TARGETED_RESCUE_ACCEPTED",
        page=page_num,
        number=number,
        extraction_provider=extraction_provenance.get("provider"),
        audit_provider=audit_provenance.get("provider"),
        confidence=confidence,
    )
    return {
        "number": number,
        "section_type": kind,
        "exact_source_prompt": prompt_text,
        "subquestions": list(payload.get("subquestions") or []),
        "figure_labels": list(payload.get("figure_labels") or []),
        "bbox_1000": coords,
        "_rescue_crop_rect": [rect.x0, rect.y0, rect.x1, rect.y1],
        "_rescue_crop_bytes": crop_bytes,
        "_rescue_extraction_provenance": dict(extraction_provenance),
        "_rescue_audit_provenance": dict(audit_provenance),
        "confidence": confidence,
        "unreadable_parts": [],
    }


def extract_scanned_page_exercises(
        doc, page_num: int, lesson_id: str, book_id: str, cache_dir: Path,
        *, drive_service=None, checkpoint_root=None, entry=None,
        force_refresh: bool = False) -> List[dict]:
    """Read numbered exercise regions from the real page image, not OCR digits.

    Scanned textbooks frequently use circled numbers in two columns, which
    plain OCR mistakes for letters. Two visual passes independently compare
    the proposed prompts against the source page before accepting them.
    """
    assert_authorized_source_vision(lesson_id, book_id, page_num)
    page = doc[page_num - 1]
    image_bytes = page.get_pixmap(
        dpi=320 if force_refresh else 200).tobytes("png")
    page_b64 = base64.b64encode(image_bytes).decode("ascii")

    # Durable *stage* checkpoints: a provider pause during the independent
    # review must never force the expensive extraction pass to run again.
    # This is separate from the final EXERCISES page checkpoint, which is only
    # written after both passes and all item-level verification succeed.
    stage_cp = None
    source_page_hash = hashlib.sha256(
        page.get_pixmap(dpi=72).samples).hexdigest()
    if drive_service is not None and checkpoint_root and entry is not None:
        from scripts import nabil_page_checkpoint as stage_cp
    instruction = (
        ("COMPLETENESS RECOVERY: scan the ENTIRE page at high resolution, "
         "including BOTH columns from top to bottom; do not stop after the first "
         "column or after the first consecutive exercise sequence. " if force_refresh else "")
        + "Read this school textbook page, paying attention to TWO-COLUMN reading "
        "order and circled exercise numbers. Return JSON with exercises array. "
        "For every numbered exercise or problem return: number (integer), "
        "section_type (EXERCISE or PROBLEM), exact_source_prompt (all words and "
        "blanks verbatim, do not solve), subquestions (array of exact strings), "
        "bbox_1000 (entire exercise prompt region, normalized x0,y0,x1,y1), "
        "figure_labels (list of exact cited Figure numbers), blank_count "
        "(integer), confidence 0..1, and unreadable_parts (array). Represent "
        "EVERY visibly empty answer box, underline blank, or fill-in slot with "
        "the literal token [BLANK] at its exact reading position, and set "
        "blank_count to the number of visible blanks. Include each exercise exactly once; "
        "do not confuse printed figure numbers, chapter numbers or page "
        "numbers with exercise numbers. Preserve table entries and all "
        "instructions. Do not invent any text. No numbered exercises -> []."
    )
    scan_unit = f"page:{page_num}"
    scan_record = (
        stage_cp.load_paid_unit(
            drive_service, checkpoint_root, entry,
            operation="exercise_scan",
            unit_id=scan_unit,
            source_hash=source_page_hash,
            prompt_version=EXERCISE_SCAN_PROMPT_VERSION,
        ) if stage_cp and not force_refresh else None
    )
    if isinstance(scan_record, dict) and "data" in scan_record:
        extracted = scan_record["data"]
        extraction_provenance = dict(
            scan_record.get("provenance") or {})
        progress("EXERCISE_SCAN_STAGE_RESTORED_FROM_DRIVE",
                 page=page_num)
    else:
        extracted = _execute_llm_json_strict(
            instruction,
            image_base64=page_b64,
            vision_context={
                "lesson_id": lesson_id,
                "book_id": book_id,
                "pdf_page": page_num,
            },
            purpose=f"exercise_scan_p{page_num}",
        )
        extraction_provenance = get_last_llm_provenance()
    rows = _normalize_exercise_scan_payload(extracted, page_num)
    if not rows:
        # A first-pass page read may miss small circled exercise numbers or a
        # compact two-column exercise page. Re-read the SAME original page at
        # higher resolution before concluding that no exercises exist.
        highres_bytes = page.get_pixmap(dpi=320).tobytes("png")
        highres_b64 = base64.b64encode(highres_bytes).decode("ascii")
        rescue_instruction = (
            "Re-inspect this SAME original textbook page at high resolution. "
            "Return JSON with exercises array containing EVERY visibly numbered "
            "exercise/problem on the page, preserving two-column reading order. "
            "For each item return number, section_type, exact_source_prompt, "
            "subquestions, bbox_1000, figure_labels, blank_count, confidence, "
            "unreadable_parts. Preserve every printed word and every visible "
            "answer blank as [BLANK]. Do not solve, infer, renumber, or invent. "
            "If there are genuinely no numbered exercises, return "
            "{\"exercises\":[]}.")
        rescued_scan = _execute_llm_json_strict(
            rescue_instruction,
            image_base64=highres_b64,
            vision_context={
                "lesson_id": lesson_id,
                "book_id": book_id,
                "pdf_page": page_num,
            },
            purpose=f"exercise_scan_highres_rescue_p{page_num}",
        )
        rows = _normalize_exercise_scan_payload(rescued_scan, page_num)
        extracted = rescued_scan
        extraction_provenance = get_last_llm_provenance()
        page_b64 = highres_b64
        if rows:
            progress(
                "EXERCISE_PAGE_HIGHRES_RESCUE_ACCEPTED",
                page=page_num,
                exercise_candidates=len(rows),
            )
        else:
            if stage_cp:
                stage_cp.save_paid_unit(
                    drive_service, checkpoint_root, entry,
                    operation="exercise_scan",
                    unit_id=scan_unit,
                    source_hash=source_page_hash,
                    prompt_version=EXERCISE_SCAN_PROMPT_VERSION,
                    payload={"data": extracted,
                             "provenance": extraction_provenance},
                    provenance=extraction_provenance,
                )
                progress("EXERCISE_SCAN_STAGE_SAVED_TO_DRIVE",
                         page=page_num, count=0)
            progress(
                "EXERCISE_PAGE_HIGHRES_RESCUE_EMPTY",
                page=page_num,
            )
            return []
    if stage_cp and scan_record is None:
        stage_cp.save_paid_unit(
            drive_service, checkpoint_root, entry,
            operation="exercise_scan",
            unit_id=scan_unit,
            source_hash=source_page_hash,
            prompt_version=EXERCISE_SCAN_PROMPT_VERSION,
            payload={"data": extracted,
                     "provenance": extraction_provenance},
            provenance=extraction_provenance,
        )
        progress("EXERCISE_SCAN_STAGE_SAVED_TO_DRIVE",
                 page=page_num, count=len(rows))

    audit_prompt = (
        "Independently compare these exercise transcriptions to the PROVIDED "
        "original source page image. Return JSON: "
        "{'checks':[{'number':int,'faithful':bool,'blank_count_visible':int,"
        "'blank_tokens_match':bool,'reason':str}]}. "
        "Mark false for a missing part, wrong figure number, invented words, "
        "wrong item boundaries, incorrect circled-number reading, bad "
        "two-column order, or any missing/misplaced [BLANK] token. Independently "
        "count visible answer blanks for each exercise and reject a transcription "
        "when blank_count or the number of [BLANK] tokens does not match. "
        "No favorable assumptions. Transcriptions: "
        + json.dumps(rows, ensure_ascii=False)
    )
    review_source_hash = hashlib.sha256(
        (source_page_hash + "|" + json.dumps(
            rows, sort_keys=True, ensure_ascii=False, default=str)
        ).encode("utf-8")).hexdigest()
    review_unit = f"page:{page_num}"
    review_record = (
        stage_cp.load_paid_unit(
            drive_service, checkpoint_root, entry,
            operation="exercise_review",
            unit_id=review_unit,
            source_hash=review_source_hash,
            prompt_version=EXERCISE_REVIEW_PROMPT_VERSION,
        ) if stage_cp and not force_refresh else None
    )
    if isinstance(review_record, dict) and "data" in review_record:
        review = review_record["data"]
        audit_provenance = dict(
            review_record.get("provenance") or {})
        progress("EXERCISE_REVIEW_STAGE_RESTORED_FROM_DRIVE",
                 page=page_num)
    else:
        review = _execute_llm_json_strict(
            audit_prompt,
            image_base64=page_b64,
            vision_context={
                "lesson_id": lesson_id,
                "book_id": book_id,
                "pdf_page": page_num,
            },
            purpose=f"exercise_review_p{page_num}",
        )
        audit_provenance = get_last_llm_provenance()
    checks = _normalize_exercise_review_payload(review, page_num)

    # Do not interpret an incomplete audit schema as a source rejection. Ask
    # again against the SAME source page and SAME candidate transcriptions.
    # This remains fail-closed: no item is approved until every required audit
    # field is explicitly present with the correct type.
    expected_review_numbers = {
        int(row["number"]) for row in rows
        if isinstance(row, dict) and "number" in row
    }

    def _exercise_review_schema_complete(items: List[dict]) -> bool:
        if not isinstance(items, list):
            return False
        seen = set()
        for item in items:
            if not isinstance(item, dict) or "number" not in item:
                return False
            try:
                item_number = int(item["number"])
            except (TypeError, ValueError):
                return False
            if item_number in seen:
                return False
            seen.add(item_number)
            if not isinstance(item.get("faithful"), bool):
                return False
            if not isinstance(item.get("blank_count_visible"), int) or isinstance(
                    item.get("blank_count_visible"), bool):
                return False
            if not isinstance(item.get("blank_tokens_match"), bool):
                return False
            if not isinstance(item.get("reason"), str):
                return False
        return seen == expected_review_numbers

    if not _exercise_review_schema_complete(checks):
        progress(
            "EXERCISE_REVIEW_SCHEMA_RETRY_REQUIRED",
            page=page_num,
            expected_numbers=sorted(expected_review_numbers),
        )
        strict_review_prompt = (
            "Re-audit these candidate exercise transcriptions against the SAME "
            "original textbook page image. Return EXACTLY one strict JSON object "
            "with key checks. checks must contain exactly one object for every "
            "candidate exercise number, no omissions and no extras. Every object "
            "must contain all fields: number (integer), faithful (boolean), "
            "blank_count_visible (integer >= 0), blank_tokens_match (boolean), "
            "reason (string). Count visible answer boxes/blanks independently "
            "from the source image. faithful=false for any missing/invented word, "
            "wrong boundary/number/figure/table entry, or blank mismatch. "
            "Do not repair or reinterpret candidate text. Candidates: "
            + json.dumps(rows, ensure_ascii=False)
        )
        strict_review = _execute_llm_json_strict(
            strict_review_prompt,
            image_base64=page_b64,
            vision_context={
                "lesson_id": lesson_id,
                "book_id": book_id,
                "pdf_page": page_num,
            },
            purpose=f"exercise_review_schema_retry_p{page_num}",
            max_attempts=3,
        )
        checks = _normalize_exercise_review_payload(strict_review, page_num)
        audit_provenance = get_last_llm_provenance()
        if not _exercise_review_schema_complete(checks):
            raise RuntimeError(
                f"EXERCISE_REVIEW_SCHEMA_INCOMPLETE: p{page_num}"
            )
        progress(
            "EXERCISE_REVIEW_SCHEMA_RETRY_ACCEPTED",
            page=page_num,
            checks=len(checks),
        )

    if stage_cp and review_record is None:
        stage_cp.save_paid_unit(
            drive_service, checkpoint_root, entry,
            operation="exercise_review",
            unit_id=review_unit,
            source_hash=review_source_hash,
            prompt_version=EXERCISE_REVIEW_PROMPT_VERSION,
            payload={"data": checks,
                     "provenance": audit_provenance},
            provenance=audit_provenance,
        )
        progress("EXERCISE_REVIEW_STAGE_SAVED_TO_DRIVE",
                 page=page_num, checks=len(checks))

    approved = {
        int(x["number"]): x
        for x in checks
        if isinstance(x, dict)
        and "number" in x
        and x.get("faithful") is True
        and x.get("blank_tokens_match") is True
        and isinstance(x.get("blank_count_visible"), int)
    }
    from fitz import Rect
    result = []
    for row in rows:
        if not isinstance(row, dict):
            raise RuntimeError(f"EXERCISE_SOURCE_MISMATCH: unexpected page item p{page_num}")
        number = int(row["number"])
        prompt = str(row.get("exact_source_prompt") or "").strip()
        coords = row.get("bbox_1000")
        rejection_reasons = []
        if number < 1 or number > 999:
            rejection_reasons.append("number_out_of_range")
        if len(prompt) < 10:
            rejection_reasons.append("prompt_too_short")
        if row.get("unreadable_parts"):
            rejection_reasons.append("unreadable_parts")
        try:
            if float(row.get("confidence", 0)) < 0.85:
                rejection_reasons.append("low_confidence")
        except (TypeError, ValueError):
            rejection_reasons.append("invalid_confidence")
        review_item = next(
            (x for x in checks if isinstance(x, dict)
             and str(x.get("number")) == str(number)), {})
        if number not in approved:
            rejection_reasons.append(
                "independent_review_rejected:" +
                str(review_item.get("reason") or "not_approved")[:180])
        else:
            visible_blank_count = int(review_item.get("blank_count_visible", 0))
            token_blank_count = prompt.count("[BLANK]")
            try:
                declared_blank_count = int(row.get("blank_count", -1))
            except (TypeError, ValueError):
                declared_blank_count = -1
            if not (
                declared_blank_count == visible_blank_count
                and token_blank_count == visible_blank_count
            ):
                rejection_reasons.append(
                    "blank_count_mismatch:"
                    f"declared={declared_blank_count},"
                    f"tokens={token_blank_count},"
                    f"visible={visible_blank_count}"
                )
        if not isinstance(coords, list) or len(coords) != 4:
            rejection_reasons.append("invalid_bbox_shape")
        else:
            try:
                bx0, by0, bx1, by1 = [float(v) for v in coords]
                if not (0 <= bx0 < bx1 <= 1000 and 0 <= by0 < by1 <= 1000):
                    rejection_reasons.append("invalid_bbox_bounds")
            except (TypeError, ValueError):
                rejection_reasons.append("invalid_bbox_values")
        kind_candidate = str(row.get("section_type") or "EXERCISE").upper()
        if kind_candidate not in ("EXERCISE", "PROBLEM"):
            rejection_reasons.append("invalid_section_type")

        if rejection_reasons:
            progress(
                "EXERCISE_TARGETED_RESCUE_START",
                page=page_num,
                number=number,
                reasons=rejection_reasons,
            )
            rescued = _rescue_unverified_exercise(
                page, row, page_num, lesson_id, book_id)
            if rescued is None:
                progress(
                    "SKIPPED_UNVERIFIED_EXERCISE",
                    page=page_num,
                    number=number,
                    reasons=rejection_reasons,
                )
                # Fail closed at ITEM level: never display/solve an exercise
                # that could not be verified, but do not discard the whole
                # verified lesson because one page item is unreadable.
                continue
            row = rescued
            prompt = str(row["exact_source_prompt"]).strip()
            coords = row["bbox_1000"]

        x0, y0, x1, y1 = [float(v) for v in coords]
        if not (0 <= x0 < x1 <= 1000 and 0 <= y0 < y1 <= 1000):
            progress(
                "SKIPPED_UNVERIFIED_EXERCISE",
                page=page_num,
                number=number,
                reasons=["invalid_region_after_rescue"],
            )
            continue
        rect = Rect(x0*page.rect.width/1000, y0*page.rect.height/1000,
                    x1*page.rect.width/1000, y1*page.rect.height/1000)
        raw_region = row.get("_rescue_crop_bytes")
        if not isinstance(raw_region, (bytes, bytearray)):
            raw_region = page.get_pixmap(clip=rect, dpi=200).tobytes("png")
        region_path = cache_dir / f"exercise_p{page_num}_{number}.png"
        region_path.write_bytes(raw_region)
        kind = str(row.get("section_type") or "EXERCISE").upper()
        if kind not in ("EXERCISE", "PROBLEM"):
            progress(
                "SKIPPED_UNVERIFIED_EXERCISE",
                page=page_num,
                number=number,
                reasons=["invalid_section_type_after_rescue"],
            )
            continue
        result.append({
            "number": number, "section_type": kind, "exact_source_prompt": prompt,
            "subquestions": list(row.get("subquestions") or []),
            "source_page": page_num,
            "source_bbox": [rect.x0, rect.y0, rect.x1, rect.y1],
            "source_region_image_ref": str(region_path),
            "source_region_sha256": hashlib.sha256(raw_region).hexdigest(),
            "verified_against_source": True,
            "ai_provenance": {
                "extraction": dict(row.get(
                    "_rescue_extraction_provenance", extraction_provenance)),
                "audit": dict(row.get(
                    "_rescue_audit_provenance", audit_provenance)),
            },
            "evidence_method": (
                "TARGETED_HIGHRES_TWO_PASS_EXERCISE_VISION"
                if row.get("_rescue_extraction_provenance")
                else "TWO_PASS_SOURCE_PAGE_VISION"
            )
        })
    return result


def _render_verified_text_diagram_svg(plan: dict) -> str:
    """Render a reviewed text-grounded diagram plan as deterministic SVG."""
    allowed = {"rect", "ellipse", "line", "arrow", "point", "text"}
    objects = plan.get("objects") or []
    if not isinstance(objects, list) or not objects:
        raise RuntimeError("TEXT_DIAGRAM_OBJECTS_MISSING")

    def num(value, default=0.0):
        try:
            return max(0.0, min(1000.0, float(value)))
        except (TypeError, ValueError):
            return float(default)

    parts = [
        '<svg class="nabil-text-grounded-diagram" viewBox="0 0 1000 600" '
        'role="img" xmlns="http://www.w3.org/2000/svg" '
        'style="max-width:100%;height:auto;border:1px solid #cbd5e1;'
        'border-radius:10px;background:#fff;">',
        '<defs><marker id="nabilArrow" markerWidth="10" markerHeight="10" '
        'refX="9" refY="3" orient="auto" markerUnits="strokeWidth">'
        '<path d="M0,0 L0,6 L9,3 z" fill="currentColor"/></marker></defs>',
    ]
    for obj in objects[:40]:
        if not isinstance(obj, dict):
            continue
        kind = str(obj.get("kind") or "").lower()
        if kind not in allowed:
            continue
        label = html.escape(str(obj.get("label") or ""))
        x = num(obj.get("x"), 100)
        y = num(obj.get("y"), 100)
        if kind == "rect":
            w = max(5.0, min(900.0, num(obj.get("w"), 120)))
            h = max(5.0, min(500.0, num(obj.get("h"), 80)))
            parts.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" '
                f'height="{h:.1f}" rx="8" fill="none" stroke="currentColor" '
                f'stroke-width="3"/>')
        elif kind == "ellipse":
            rx = max(4.0, min(450.0, num(obj.get("rx"), 50)))
            ry = max(4.0, min(250.0, num(obj.get("ry"), 30)))
            parts.append(
                f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx:.1f}" '
                f'ry="{ry:.1f}" fill="none" stroke="currentColor" '
                f'stroke-width="3"/>')
        elif kind in ("line", "arrow"):
            x2 = num(obj.get("x2"), x + 100)
            y2 = num(obj.get("y2"), y)
            marker = ' marker-end="url(#nabilArrow)"' if kind == "arrow" else ""
            parts.append(
                f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x2:.1f}" '
                f'y2="{y2:.1f}" stroke="currentColor" stroke-width="3"{marker}/>')
        elif kind == "point":
            parts.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="currentColor"/>')
        elif kind == "text":
            parts.append(
                f'<text x="{x:.1f}" y="{y:.1f}" font-size="28" '
                f'font-family="Arial, sans-serif">{label}</text>')
        if label and kind != "text":
            parts.append(
                f'<text x="{x + 10:.1f}" y="{max(24.0, y - 10):.1f}" '
                f'font-size="24" font-family="Arial, sans-serif">{label}</text>')
    parts.append("</svg>")
    svg = "".join(parts)
    if "<svg" not in svg or "</svg>" not in svg:
        raise RuntimeError("TEXT_DIAGRAM_RENDER_FAILED")
    return svg



def build_nabil_explanatory_redrawing(
        source_text: str,
        page_num: int,
        figure_paths: Optional[List[str]] = None,
        vision_context: Optional[Dict[str, Any]] = None,
        purpose: str = "concept_visual",
        visual_required: bool = False) -> Optional[dict]:
    """Create a NEW NABIL schematic from locked evidence, never expose the scan.

    Source figures may be inspected by vision, but their pixels are never
    returned to the student. The model proposes only semantic objects and
    relations; deterministic SVG is rendered locally and independently audited
    against the same locked text/figure evidence.
    """
    source_text = str(source_text or "").strip()
    figure_paths = [str(p) for p in (figure_paths or []) if p and Path(p).is_file()]
    if len(source_text) < 12 and not figure_paths:
        return None

    figure_b64 = None
    if figure_paths:
        from PIL import Image
        pics = []
        for filename in figure_paths[:4]:
            with Image.open(filename) as image:
                pic = image.convert("RGB")
                pic.thumbnail((1200, 850))
                pics.append(pic.copy())
        if pics:
            canvas = Image.new(
                "RGB",
                (max(p.width for p in pics),
                 sum(p.height for p in pics) + 10 * (len(pics) - 1)),
                "white",
            )
            top = 0
            for pic in pics:
                canvas.paste(pic, (0, top))
                top += pic.height + 10
            buf = io.BytesIO()
            canvas.save(buf, format="PNG")
            figure_b64 = base64.b64encode(buf.getvalue()).decode("ascii")

    request = (
        "You are NABIL, a classroom teacher creating a NEW explanatory schematic, "
        "not reproducing textbook artwork. Use the locked source text and, when "
        "provided, the verified source figure ONLY as evidence. The student must "
        "never see the source scan. Decide whether a visual is pedagogically useful. "
        "If not useful and VISUAL_REQUIRED is false, return "
        "{'needed':false,'reason':str}. If VISUAL_REQUIRED is true, needed must be "
        "true unless the evidence is insufficient, in which case return "
        "{'needed':false,'reason':'INSUFFICIENT_EVIDENCE'}. "
        "For a visual return strict JSON with needed=true, title, objects, relations. "
        "objects: at most 24 items, kind in rect|ellipse|line|arrow|point|text, "
        "id, label, x,y and optional x2,y2,w,h,rx,ry. Each object must contain "
        "evidence_basis='text' or 'figure'. For text basis include evidence_quote "
        "that is an EXACT contiguous quote from SOURCE_TEXT. For figure basis use "
        "evidence_quote='' and only encode something visibly verifiable in the "
        "provided source figure. relations has type,a,b,evidence_basis,evidence_quote "
        "under the same rule. Coordinates are presentation layout only, never data. "
        "Do not copy decorative styling, page layout, colors, icons, or typography "
        "from the textbook. Do not invent labels, measurements, geometry, direction, "
        "scientific behavior, historical facts, grammar rules, or missing steps. "
        f"VISUAL_REQUIRED={str(bool(visual_required)).lower()}\n"
        "SOURCE_TEXT:\n" + source_text
    )
    plan = _execute_llm_json_strict(
        request,
        image_base64=figure_b64,
        vision_context=vision_context if figure_b64 else None,
        purpose=f"{purpose}_plan_p{page_num}",
        max_attempts=3,
    )
    plan_provenance = dict(get_last_llm_provenance())
    if not isinstance(plan, dict) or plan.get("needed") is not True:
        progress(
            "NABIL_EXPLANATORY_REDRAW_NOT_BUILT",
            page=page_num,
            purpose=purpose,
            reason=str(plan.get("reason") if isinstance(plan, dict) else "INVALID_PLAN")[:240],
        )
        return None

    objects = plan.get("objects")
    relations = plan.get("relations")
    if not isinstance(objects, list) or not objects or not isinstance(relations, list):
        raise RuntimeError("NABIL_REDRAW_SCHEMA_INVALID")
    source_norm = _normalized_lab_evidence(source_text)
    ids = set()
    allowed_kinds = {"rect", "ellipse", "line", "arrow", "point", "text"}
    for obj in objects:
        if not isinstance(obj, dict):
            raise RuntimeError("NABIL_REDRAW_OBJECT_INVALID")
        if str(obj.get("kind") or "").lower() not in allowed_kinds:
            raise RuntimeError("NABIL_REDRAW_OBJECT_KIND_INVALID")
        oid = str(obj.get("id") or "").strip()
        if not oid or oid in ids:
            raise RuntimeError("NABIL_REDRAW_OBJECT_ID_INVALID")
        ids.add(oid)
        basis = str(obj.get("evidence_basis") or "").lower()
        quote = _normalized_lab_evidence(obj.get("evidence_quote", ""))
        if basis == "text":
            if not quote or quote not in source_norm:
                raise RuntimeError("NABIL_REDRAW_TEXT_EVIDENCE_NOT_FOUND")
        elif basis == "figure":
            if not figure_b64:
                raise RuntimeError("NABIL_REDRAW_FIGURE_EVIDENCE_MISSING")
        else:
            raise RuntimeError("NABIL_REDRAW_EVIDENCE_BASIS_INVALID")
    for rel in relations:
        if not isinstance(rel, dict):
            raise RuntimeError("NABIL_REDRAW_RELATION_INVALID")
        if str(rel.get("a") or "") not in ids or str(rel.get("b") or "") not in ids:
            raise RuntimeError("NABIL_REDRAW_RELATION_ENDPOINT_INVALID")
        basis = str(rel.get("evidence_basis") or "").lower()
        quote = _normalized_lab_evidence(rel.get("evidence_quote", ""))
        if basis == "text":
            if not quote or quote not in source_norm:
                raise RuntimeError("NABIL_REDRAW_RELATION_TEXT_EVIDENCE_NOT_FOUND")
        elif basis == "figure":
            if not figure_b64:
                raise RuntimeError("NABIL_REDRAW_RELATION_FIGURE_EVIDENCE_MISSING")
        else:
            raise RuntimeError("NABIL_REDRAW_RELATION_EVIDENCE_BASIS_INVALID")

    audit_prompt = (
        "Independently audit this proposed NABIL explanatory schematic against "
        "the SAME locked SOURCE_TEXT and source figure if provided. It must be a "
        "fresh schematic, not a textbook-page reproduction. Reject any object, "
        "label, orientation, measurement, connection, process step or relation "
        "that is not directly supported by text or visibly supported by the "
        "source figure. Also reject if the schematic copies page styling/layout "
        "rather than teaching the concept. Return strict JSON exactly: "
        "{'approved':bool,'all_claims_traceable':bool,'no_invented_science':bool,"
        "'not_source_scan_reproduction':bool,'pedagogically_useful':bool,'reason':str}.\n"
        "SOURCE_TEXT:\n" + source_text + "\nPLAN:\n" +
        json.dumps(plan, ensure_ascii=False)
    )
    audit = _execute_llm_json_strict(
        audit_prompt,
        image_base64=figure_b64,
        vision_context=vision_context if figure_b64 else None,
        purpose=f"{purpose}_audit_p{page_num}",
        max_attempts=3,
    )
    audit_provenance = dict(get_last_llm_provenance())
    if not isinstance(audit, dict) or not (
        audit.get("approved") is True
        and audit.get("all_claims_traceable") is True
        and audit.get("no_invented_science") is True
        and audit.get("not_source_scan_reproduction") is True
        and audit.get("pedagogically_useful") is True
    ):
        progress(
            "NABIL_EXPLANATORY_REDRAW_REJECTED",
            page=page_num,
            purpose=purpose,
            reason=str(audit.get("reason") if isinstance(audit, dict) else "INVALID_AUDIT")[:240],
        )
        return None

    svg = _render_verified_text_diagram_svg(plan)
    progress(
        "NABIL_EXPLANATORY_REDRAW_ACCEPTED",
        page=page_num,
        purpose=purpose,
        objects=len(objects),
        relations=len(relations),
    )
    return {
        "verified": True,
        "method": "NABIL_EXPLANATORY_REDRAW_FROM_LOCKED_EVIDENCE",
        "plan": plan,
        "svg": svg,
        "source_text_sha256": hashlib.sha256(source_text.encode("utf-8")).hexdigest(),
        "used_source_figure_as_hidden_evidence": bool(figure_b64),
        "ai_provenance": {
            "plan": plan_provenance,
            "audit": audit_provenance,
        },
    }


def build_text_grounded_exercise_diagram(
        entry: dict, prompt_text: str, subquestions: list,
        page_num: int, concepts: list) -> Optional[dict]:
    """Reconstruct a schematic only when verified text fully supports it.

    The output is never treated as the original textbook figure. Scientific
    objects/relations must be traceable to exact evidence quotes; layout
    coordinates are illustrative only and independently audited.
    """
    page_scope = [
        {
            "concept_id": c.get("concept_id"),
            "text": c.get("raw_text") or c.get("normalized_text") or "",
        }
        for c in concepts
        if int(c.get("source_page") or -1) == int(page_num)
    ]
    source_blob = (
        str(prompt_text or "").strip() + "\n" +
        "\n".join(str(x) for x in (subquestions or [])) + "\n" +
        "\n".join(str(x.get("text") or "") for x in page_scope)
    ).strip()
    if len(source_blob) < 20:
        return None

    request = (
        "You are reconstructing a SIMPLE SCHEMATIC for a textbook exercise "
        "ONLY from verified text. The original figure is unavailable and MUST "
        "NOT be guessed. If the text does not fully specify every scientific "
        "object and relation needed to solve the exercise, return "
        "{\"reconstructable\":false,\"reason\":str}. "
        "If reconstructable, return JSON with reconstructable=true, reason, "
        "objects and relations. objects is an array of at most 20 items with "
        "kind limited to rect|ellipse|line|arrow|point|text, id, label, x,y "
        "and when needed x2,y2,w,h,rx,ry, plus evidence_quote. Coordinates are "
        "only illustrative page layout. relations is an array with type, a, b, "
        "and evidence_quote. EVERY evidence_quote must be an exact contiguous "
        "quote from VERIFIED TEXT. Do not add an object, label, orientation, "
        "relative position, scale, measurement, angle, or scientific relation "
        "unless the verified text explicitly supports it. A reference such as "
        "'see Fig. 6' by itself is NOT enough. Never imitate or claim to "
        "reproduce the missing textbook image.\nVERIFIED TEXT:\n" + source_blob
    )
    plan = _execute_llm_json_strict(
        request, purpose=f"text_diagram_plan_p{page_num}")
    plan_provenance = dict(get_last_llm_provenance())
    if not isinstance(plan, dict) or plan.get("reconstructable") is not True:
        progress(
            "TEXT_DIAGRAM_RECONSTRUCTION_NOT_POSSIBLE",
            page=page_num,
            reason=str(plan.get("reason") if isinstance(plan, dict) else
                       "INVALID_PLAN")[:240],
        )
        return None

    source_norm = _normalized_lab_evidence(source_blob)
    objects = plan.get("objects")
    relations = plan.get("relations")
    if not isinstance(objects, list) or not objects:
        return None
    if not isinstance(relations, list):
        return None
    allowed_kinds = {"rect", "ellipse", "line", "arrow", "point", "text"}
    ids = set()
    for obj in objects:
        if not isinstance(obj, dict):
            return None
        if str(obj.get("kind") or "").lower() not in allowed_kinds:
            return None
        oid = str(obj.get("id") or "").strip()
        quote = _normalized_lab_evidence(obj.get("evidence_quote", ""))
        if not oid or oid in ids or not quote or quote not in source_norm:
            return None
        ids.add(oid)
    for rel in relations:
        if not isinstance(rel, dict):
            return None
        quote = _normalized_lab_evidence(rel.get("evidence_quote", ""))
        if (str(rel.get("a") or "") not in ids
                or str(rel.get("b") or "") not in ids
                or not quote or quote not in source_norm):
            return None

    audit_prompt = (
        "Act as an independent scientific diagram auditor. Decide whether this "
        "schematic plan can be drawn from VERIFIED TEXT without inventing any "
        "scientific information. Coordinates are merely visual layout, but "
        "object existence, labels, orientation, relative placement, connections, "
        "measurements and scientific relations must all be text-supported. "
        "Reject if the exercise cannot be solved from the text-grounded plan "
        "without relying on the missing original image. Return strict JSON: "
        "{\"approved\":bool,\"all_claims_traceable\":bool,"
        "\"no_unstated_geometry\":bool,\"sufficient_for_exercise\":bool,"
        "\"reason\":str}.\nVERIFIED TEXT:\n" + source_blob +
        "\nPLAN:\n" + json.dumps(plan, ensure_ascii=False)
    )
    audit = _execute_llm_json_strict(
        audit_prompt, purpose=f"text_diagram_audit_p{page_num}")
    audit_provenance = dict(get_last_llm_provenance())
    if not isinstance(audit, dict) or not (
            audit.get("approved") is True
            and audit.get("all_claims_traceable") is True
            and audit.get("no_unstated_geometry") is True
            and audit.get("sufficient_for_exercise") is True):
        progress(
            "TEXT_DIAGRAM_RECONSTRUCTION_REJECTED",
            page=page_num,
            reason=str(audit.get("reason") if isinstance(audit, dict) else
                       "INVALID_AUDIT")[:240],
        )
        return None

    svg = _render_verified_text_diagram_svg(plan)
    progress(
        "TEXT_DIAGRAM_RECONSTRUCTION_ACCEPTED",
        page=page_num,
        objects=len(objects),
        relations=len(relations),
    )
    return {
        "verified": True,
        "method": "AI_RECONSTRUCTED_DIAGRAM_FROM_VERIFIED_TEXT",
        "plan": plan,
        "svg": svg,
        "source_text_sha256": hashlib.sha256(
            source_blob.encode("utf-8")).hexdigest(),
        "ai_provenance": {
            "plan": plan_provenance,
            "audit": audit_provenance,
        },
    }


def build_evidence_map(doc, entry: dict, drive_service=None, persist_pages=False) -> dict:
    start_p = int(entry["pdf_start_page"])
    end_p = int(entry["pdf_end_page"])
    lesson_id = entry["lesson_id"]
    book_id = entry["book_id"]
    if start_p < 1 or end_p < start_p or end_p > len(doc):
        raise RuntimeError(f"SOURCE_PAGE_OUT_OF_RANGE: {lesson_id}, pages {start_p}-{end_p}, book length {len(doc)}")

    pages_evidence = []
    lesson_cache = CACHE_DIR / f"{book_id}_{lesson_id}"
    lesson_cache.mkdir(parents=True, exist_ok=True)
    page_checkpoints = None
    checkpoint_root = None
    source_provider = os.getenv("NABIL_FACTORY_AI_PROVIDER", "auto").strip().lower()
    if source_provider == "auto":
        source_provider = next(
            (name for name in ("openrouter", "groq", "openai")
             if os.getenv(name.upper() + "_API_KEY")), "none")
    source_model = {
        "groq": os.getenv("GROQ_VISION_MODEL", "qwen/qwen3.8-27b"),
        "openrouter": os.getenv("OPENROUTER_VISION_MODEL",
                               os.getenv("OPENROUTER_TEXT_MODEL",
                                         "google/gemini-3.6-flash")),
        "openai": os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini"),
    }.get(source_provider, "none")
    # Page checkpoints are recovery infrastructure, not scientific evidence.
    # Missing Drive/root must never abort lesson generation.  When configured,
    # checkpoints remain enabled; otherwise the factory continues normally.
    checkpoint_root = None
    page_checkpoints = None
    if persist_pages and drive_service is not None:
        checkpoint_root = str(os.getenv("NABIL_CURRICULUM_ROOT_ID") or "").strip() or None
        if checkpoint_root:
            from scripts import nabil_page_checkpoint as page_checkpoints
        else:
            progress(
                "CHECKPOINT_DISABLED_NO_ROOT_ID",
                lesson_id=lesson_id,
                reason="NABIL_CURRICULUM_ROOT_ID_NOT_CONFIGURED")
    elif persist_pages and page_checkpoints is not None and checkpoint_root:
        progress(
            "CHECKPOINT_DISABLED_NO_DRIVE",
            lesson_id=lesson_id,
            reason="DRIVE_SERVICE_UNAVAILABLE")
    opening_text = extract_page_text_robust(
        doc, start_p, lesson_id, book_id, lesson_cache)
    # Validate the two physical title sources BEFORE costly page-by-page vision.
    if not verify_title_double_evidence_strict(doc, entry, opening_text):
        raise AssertionError(
            f"TITLE_VERIFICATION_FAILED: Strict Double Evidence TOC + Opening "
            f"failed for '{entry['canonical_title']}'.")
    progress("LESSON_TITLE_DOUBLE_EVIDENCE_VERIFIED",
             lesson_id=lesson_id, title=entry["canonical_title"],
             opener_pdf_page=start_p, toc_pdf_page=entry.get("toc_pdf_page"))
    for p_num in range(start_p, end_p + 1):
        saved_page = (page_checkpoints.load_page(
            drive_service, checkpoint_root, doc, entry, p_num, lesson_cache,
            source_provider, source_model) if page_checkpoints else None)
        if saved_page is not None:
            for restored_figure in saved_page["figures"]:
                if restored_figure.get("evidence_method") in (
                    "APPROVED_VISION_BOX_CROPPED_FROM_SOURCE_PDF",
                    "TARGETED_HIGHRES_VISION_PLUS_LOCAL_CAPTION_OCR",
                ):
                    provenance = restored_figure.get("ai_provenance") or {}
                    actual_provider = provenance.get("provider")
                    assert_authorized_source_vision(
                        lesson_id, book_id, p_num,
                        provider_override=actual_provider)
            pages_evidence.append(saved_page)
            progress("PAGE_EVIDENCE_RESTORED_FROM_DRIVE",
                     lesson_id=lesson_id, page=p_num,
                     figures=len(saved_page["figures"]))
            continue
        txt = (opening_text if p_num == start_p else
               extract_page_text_robust(doc, p_num, lesson_id, book_id, lesson_cache))
        figs = extract_multimodal_page_figures(
            doc, p_num, lesson_cache, lesson_id, book_id)
        # Source-first completeness check. If the normal pass missed a
        # printed figure label that the real page text mentions, make one
        # targeted higher-resolution rescue attempt. The rescue still requires
        # independent LOCAL OCR of the exact caption box.
        mentions = {m.lower() for m in re.findall(
            r"(?i)\bfig(?:ure)?\.?\s*(\d+[a-z]?)", txt)}
        found = {
            str(f.get("printed_label") or "").lower() for f in figs
        } | {
            str(f.get("printed_number")) for f in figs
            if f.get("printed_number") is not None
        }
        missing = mentions - found
        if missing:
            progress("TARGETED_FIGURE_RESCUE_START",
                     lesson_id=lesson_id, page=p_num,
                     missing_labels=sorted(missing))
            rescued = rescue_missing_labeled_figures(
                doc, p_num, lesson_cache, lesson_id, book_id,
                missing, figs)
            if rescued:
                figs.extend(rescued)
                found = {
                    str(f.get("printed_label") or "").lower() for f in figs
                } | {
                    str(f.get("printed_number")) for f in figs
                    if f.get("printed_number") is not None
                }
                missing = mentions - found

        page_evidence = {
            "page_num": p_num,
            "text": txt,
            "text_hash": hashlib.sha256(txt.encode("utf-8")).hexdigest()[:16],
            "figures": figs,
            "unverified_figure_labels": sorted(missing),
        }
        if page_checkpoints:
            # Never cache an incomplete page as a completed checkpoint.
            if not missing:
                page_checkpoints.save_page(
                    drive_service, checkpoint_root, doc, entry,
                    page_evidence, source_provider, source_model)
                progress("PAGE_EVIDENCE_SAVED_TO_DRIVE",
                         lesson_id=lesson_id, page=p_num,
                         figures=len(figs))
            else:
                progress("PAGE_EVIDENCE_NOT_SAVED_UNVERIFIED_FIGURES",
                         lesson_id=lesson_id, page=p_num,
                         missing_labels=sorted(missing))
        pages_evidence.append(page_evidence)

    concepts = []
    act_regex = re.compile(
        r"(?:Activity|Activité|نشاط)\s*(\d*)[:\s.-]+([^\n.]+)", re.I)
    numbered_section_regex = re.compile(
        r"(?im)^\s*(\d+)\s+([A-ZÀ-ÖØ-Ý][^\n]{2,90})")

    def _concept_title_key(value: str) -> str:
        return re.sub(r"[^a-z0-9]+", " ", str(value or "").casefold()).strip()

    next_concept_num = 1
    concept_exercise_section_seen = False
    exercise_section_start_page = None
    for p in pages_evidence:
        page_text = str(p["text"] or "")
        if re.search(
                r"(?i)\b(exercises|problems|exercices|problèmes)\b|تمارين|مسائل",
                page_text):
            concept_exercise_section_seen = True
            if exercise_section_start_page is None:
                exercise_section_start_page = int(p["page_num"])
                progress(
                    "EXERCISE_SECTION_BOUNDARY_LOCKED",
                    page=exercise_section_start_page,
                )
        if concept_exercise_section_seen:
            continue
        page_doc = doc[p["page_num"] - 1]
        activity_matches = list(act_regex.finditer(page_text))
        headings = []
        for m in activity_matches:
            headings.append({
                "start": m.start(),
                "end_head": m.end(),
                "title": m.group(2).strip(),
                "declared_num": (
                    int(m.group(1)) if str(m.group(1) or "").isdigit()
                    else None),
                "kind": "ACTIVITY",
            })

        # Standalone numbered content after the last activity is still part of
        # the lesson (notably explanatory sections that are not called Activity).
        # Ignore broad numbered section headers that merely precede activities.
        last_activity_start = (
            max((m.start() for m in activity_matches), default=-1))
        for m in numbered_section_regex.finditer(page_text):
            title = m.group(2).strip(" .:-")
            key = _concept_title_key(title)
            if not key or key == _concept_title_key(entry["canonical_title"]):
                continue
            if activity_matches and m.start() < last_activity_start:
                continue
            if re.search(r"(?i)chapter|contents|objectives|exercise", title):
                continue
            # Avoid duplicating an Activity heading that OCR also exposed as a
            # bare numbered heading.
            if any(
                key == _concept_title_key(h["title"])
                or key in _concept_title_key(h["title"])
                or _concept_title_key(h["title"]) in key
                for h in headings
            ):
                continue
            headings.append({
                "start": m.start(),
                "end_head": m.end(),
                "title": title,
                "declared_num": None,
                "kind": "SECTION",
            })

        headings.sort(key=lambda h: h["start"])
        for pos, heading in enumerate(headings):
            end = (
                headings[pos + 1]["start"]
                if pos + 1 < len(headings)
                else len(page_text)
            )
            raw_chunk = page_text[heading["start"]:end].strip()
            chunk = " ".join(raw_chunk.split())
            if len(chunk) < 25:
                continue

            concept_num = heading["declared_num"]
            if concept_num is None or any(
                    x.get("concept_id") == f"C{concept_num:02d}"
                    for x in concepts):
                while any(
                        x.get("concept_id") == f"C{next_concept_num:02d}"
                        for x in concepts):
                    next_concept_num += 1
                concept_num = next_concept_num
            next_concept_num = max(next_concept_num, concept_num + 1)

            matched_figs = match_figure_to_item(
                {"raw_text": chunk, "requires_figure": False},
                p["figures"], page_doc.rect)
            fig_ref = matched_figs[0] if matched_figs else "NONE"

            rects = page_doc.search_for(heading["title"][:20])
            act_bbox = (
                [round(rects[0].x0, 1), round(rects[0].y0, 1),
                 round(rects[0].x1, 1), round(rects[0].y1, 1)]
                if rects
                else [0.0, 0.0, page_doc.rect.width, 100.0]
            )
            norm_chunk, math_ok, math_recs = MathRenderingEngine.normalize_math(
                chunk, p["page_num"], act_bbox, fig_ref)

            concepts.append({
                "concept_id": f"C{concept_num:02d}",
                "title": heading["title"],
                "source_page": p["page_num"],
                "raw_text": chunk,
                "normalized_text": norm_chunk,
                "figure_refs": matched_figs,
                "math_records": math_recs,
                "source_section_kind": heading["kind"],
                "sha256": hashlib.sha256(
                    chunk.encode("utf-8")).hexdigest()[:16],
            })

    if not concepts:
        raise RuntimeError("EVIDENCE_EXTRACTION_INCOMPLETE: No verifiable concepts or activities found within source page range.")

    exercises = []
    ex_pattern = re.compile(r'(?:^|\n)\s*(?:(Problem|Exercise|Problème|Exercice|تمرين|مسألة)\s*)?(\d+)[\.\-\)]\s+([^\n]+(?:\n(?!\s*(?:(?:Problem|Exercise|Problème|Exercice|تمرين|مسألة)\s*)?\d+[\.\-\)]\s+)[^\n]+)*)', re.I)
    exercise_section_seen = False
    for p in pages_evidence:
        page_num = p["page_num"]
        if re.search(r"(?i)\b(exercises|problems|exercices|problèmes)\b|تمارين|مسائل", p["text"]):
            exercise_section_seen = True
        source_page = doc[page_num - 1]
        scanned = any(
            (rect.width*rect.height)/(source_page.rect.width*source_page.rect.height) >= 0.80
            for image in source_page.get_images(full=True)
            for rect in source_page.get_image_rects(image[0])
        )
        if scanned:
            if not exercise_section_seen and page_num < end_p - 1:
                continue
            rows = (page_checkpoints.load_exercises(
                drive_service, checkpoint_root, doc, entry, page_num,
                lesson_cache, source_provider, source_model)
                if page_checkpoints else None)
            if rows is not None:
                assert_authorized_source_vision(lesson_id, book_id, page_num)
                progress("EXERCISES_RESTORED_FROM_DRIVE",
                         page=page_num, count=len(rows))
            else:
                rows = extract_scanned_page_exercises(
                    doc, page_num, lesson_id, book_id, lesson_cache,
                    drive_service=drive_service,
                    checkpoint_root=checkpoint_root,
                    entry=entry)
                if page_checkpoints:
                    # Two independent source-image reads already confirmed
                    # the exact text/bbox for every returned exercise.
                    page_checkpoints.save_exercises(
                        drive_service, checkpoint_root, doc, entry,
                        page_num, rows, source_provider, source_model)
                    progress("EXERCISES_SAVED_TO_DRIVE",
                             page=page_num, count=len(rows))
        else:
            rows = []
            for m in ex_pattern.finditer(p["text"]):
                prompt = " ".join(m.group(3).split())
                if len(prompt) < 10:
                    continue
                kind = m.group(1)
                rows.append({
                    "number": int(m.group(2)),
                    "section_type": ("PROBLEM" if kind and kind.upper() in
                        ("PROBLEM", "PROBLÈME", "مسألة") else "EXERCISE"),
                    "exact_source_prompt": prompt,
                    "subquestions": [],
                    "source_page": page_num,
                    "verified_against_source": re.sub(r"\s+", " ", prompt).strip().casefold() in
                        re.sub(r"\s+", " ", p["text"]).strip().casefold(),
                    "evidence_method": "NATIVE_PDF_TEXT"
                })
        for row in rows:
            content = row["exact_source_prompt"]
            number = int(row["number"])
            kind = row["section_type"]
            req_fig = bool(re.search(r"(?:fig(?:ure)?\.?|document|doc|شكل|وثيقة)\s*\d+", content, re.I)
                           or any(k in content.casefold() for k in ("diagram", "sketch", "draw", "graph")))
            reconstructed = None
            try:
                refs = match_figure_to_item(
                    {"exact_source_prompt": content,
                     "requires_figure": req_fig},
                    p["figures"], source_page.rect)
            except RuntimeError as exc:
                reason = str(exc)
                if not reason.startswith("FIGURE_EVIDENCE_MISSING"):
                    raise
                reconstructed = build_text_grounded_exercise_diagram(
                    entry, content, row.get("subquestions") or [],
                    page_num, concepts)
                if reconstructed is None:
                    progress(
                        "SKIPPED_UNVERIFIED_EXERCISE",
                        page=page_num,
                        number=number,
                        reasons=[reason,
                                 "TEXT_GROUNDED_DIAGRAM_NOT_RECONSTRUCTABLE"],
                    )
                    continue
                refs = []
                progress(
                    "EXERCISE_USING_TEXT_GROUNDED_DIAGRAM",
                    page=page_num,
                    number=number,
                    method=reconstructed["method"],
                )
            hashes = [f["image_sha256"] for f in p["figures"] if f["figure_id"] in refs]
            subqs = row.get("subquestions") or []

            # When an exercise depends on a verified source figure, NABIL must
            # redraw its semantics instead of exposing the textbook crop.
            if refs and reconstructed is None:
                source_figure_paths = [
                    f["image_path"] for f in p["figures"]
                    if f["figure_id"] in refs and f.get("image_path")
                ]
                redraw_unit = f"p{page_num}_{kind}_{number}"
                redraw_source_hash = hashlib.sha256(json.dumps({
                    "prompt": str(content),
                    "subquestions": [str(x) for x in subqs],
                    "figure_hashes": [
                        f.get("image_sha256") for f in p["figures"]
                        if f["figure_id"] in refs
                    ],
                }, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
                if page_checkpoints:
                    reconstructed = page_checkpoints.load_paid_unit(
                        drive_service, checkpoint_root, entry,
                        operation="explanatory_redrawing",
                        unit_id=redraw_unit,
                        source_hash=redraw_source_hash,
                        prompt_version=REDRAW_PROMPT_VERSION,
                    )
                    if reconstructed is not None:
                        progress(
                            "EXPLANATORY_REDRAW_RESTORED_FROM_DRIVE",
                            page=page_num, number=number, unit_id=redraw_unit)
                try:
                    if reconstructed is None:
                        reconstructed = build_nabil_explanatory_redrawing(
                            source_text=(
                                str(content) + "\n" +
                                "\n".join(str(x) for x in subqs)
                            ),
                            page_num=page_num,
                            figure_paths=source_figure_paths,
                            vision_context={
                                "lesson_id": lesson_id,
                                "book_id": book_id,
                                "pdf_page": page_num,
                            } if source_figure_paths else None,
                            purpose=f"exercise_{kind}_{number}",
                            visual_required=True,
                        )
                        if reconstructed is not None and page_checkpoints:
                            prov = (
                                reconstructed.get("ai_provenance", {})
                                .get("audit", {})
                            )
                            page_checkpoints.save_paid_unit(
                                drive_service, checkpoint_root, entry,
                                operation="explanatory_redrawing",
                                unit_id=redraw_unit,
                                source_hash=redraw_source_hash,
                                prompt_version=REDRAW_PROMPT_VERSION,
                                payload=reconstructed,
                                provenance=prov,
                            )
                            progress(
                                "EXPLANATORY_REDRAW_SAVED_TO_DRIVE",
                                page=page_num, number=number,
                                unit_id=redraw_unit)
                except RuntimeError as exc:
                    # Exercise-level redraw evidence failure must not abort the
                    # whole lesson. Keep the universal fail-closed rule: reject
                    # this exercise only; never invent or expose the source scan.
                    if str(exc) != "NABIL_REDRAW_TEXT_EVIDENCE_NOT_FOUND":
                        raise
                    progress(
                        "SKIPPED_EXERCISE_NABIL_REDRAW_UNVERIFIED",
                        page=page_num,
                        number=number,
                        reason=str(exc),
                    )
                    continue
                if reconstructed is None and req_fig:
                    progress(
                        "SKIPPED_EXERCISE_NABIL_REDRAW_UNVERIFIED",
                        page=page_num,
                        number=number,
                        reason="SOURCE_FIGURE_CANNOT_BE_SAFELY_REPRESENTED_WITHOUT_SCAN",
                    )
                    continue

            ex = {
                "exercise_id": f"{lesson_id}-{kind[:2]}-{number:02d}",
                "lesson_id": lesson_id, "section_type": kind, "number": number,
                "source_page": page_num, "exact_source_prompt": content,
                "source_prompt_hash": hashlib.sha256(content.encode("utf-8")).hexdigest()[:16],
                "subquestions": subqs, "requires_figure": req_fig,
                "figure_refs": refs, "figure_hashes": hashes,
                # Every exercise that the factory can faithfully extract from
                # the official book is kept. There is deliberately NO numeric
                # cap such as "first 2 exercises".
                "solution_mode": "PRE_SOLVED", "solution_status": "NOT_SOLVED",
                "source_origin": "TEXTBOOK",
                "verified_against_source": row["verified_against_source"],
                "evidence_method": row.get("evidence_method", "NATIVE_PDF_TEXT"),
                "reconstructed_diagram_verified": bool(reconstructed),
                "reconstructed_diagram_method": (
                    reconstructed.get("method") if reconstructed else None),
                "reconstructed_diagram_plan": (
                    reconstructed.get("plan") if reconstructed else None),
                "reconstructed_diagram_svg": (
                    reconstructed.get("svg") if reconstructed else None),
                "reconstructed_diagram_source_sha256": (
                    reconstructed.get("source_text_sha256")
                    if reconstructed else None),
            }
            for key in ("source_bbox", "source_region_image_ref", "source_region_sha256"):
                if key in row:
                    ex[key] = row[key]
            exercises.append(ex)

    unique_ex = []
    seen = set()
    for e in sorted(exercises, key=lambda x: (x["section_type"], x["number"])):
        k = (e["section_type"], e["number"])
        if k not in seen:
            seen.add(k)
            unique_ex.append(e)

    # All verified textbook exercises remain in the lesson. Unverified page
    # items are skipped, never guessed. If fewer than 3 textbook exercises are
    # verified, add at least 3 evidence-gated AI practice exercises in addition.
    for e in unique_ex:
        e["solution_mode"] = "PRE_SOLVED"

    # An unresolved printed figure is critical only when accepted lesson
    # content actually refers to that figure. Otherwise it remains explicitly
    # recorded as skipped/unverified and is never rendered or used as evidence.
    def _explicit_figure_labels(text_value: str) -> set:
        return {
            str(label).casefold()
            for label in re.findall(
                r"(?:fig(?:ure)?\.?|document|doc|شكل|وثيقة)\s*(\d+[a-z]?)",
                str(text_value or ""),
                re.I,
            )
        }

    for page_item in pages_evidence:
        unresolved = {
            str(x).casefold()
            for x in (page_item.get("unverified_figure_labels") or [])
        }
        used_labels = set()
        if unresolved:
            page_no = int(page_item["page_num"])
            for concept in concepts:
                if int(concept.get("source_page") or -1) == page_no:
                    used_labels |= _explicit_figure_labels(
                        concept.get("raw_text", ""))
            for exercise in unique_ex:
                if (int(exercise.get("source_page") or -1) == page_no
                        and not exercise.get("reconstructed_diagram_verified")):
                    used_labels |= _explicit_figure_labels(
                        exercise.get("exact_source_prompt", ""))
        required_unverified = sorted(unresolved & used_labels)
        optional_unverified = sorted(unresolved - used_labels)
        page_item["required_unverified_figure_labels"] = required_unverified
        page_item["skipped_unverified_figure_labels"] = optional_unverified
        for label in optional_unverified:
            progress(
                "SKIPPED_UNVERIFIED_SOURCE_FIGURE",
                page=page_item["page_num"],
                figure_label=label,
                reason="NOT_REFERENCED_BY_ACCEPTED_CONCEPT_OR_EXERCISE",
            )

    ev_map = {
        "lesson_id": lesson_id,
        "book_id": entry["book_id"],
        "source_lock": {"start": start_p, "end": end_p},
        "pages_evidence": pages_evidence,
        "concepts": concepts,
        "exercise_section_start_page": exercise_section_start_page,
        "exercise_evidence": unique_ex,
        "canonical_title": entry["canonical_title"]
    }

    # Independent completeness gate runs before the permanent Evidence Map is accepted.
    # If a two-column scan checkpoint is incomplete, refresh ONLY the source
    # page(s) that visibly contain missing exercise numbers, then rebuild once.
    inventory = build_independent_source_inventory(ev_map)
    accepted_numbers = {
        str(x.get("number")) for x in ev_map.get("exercise_evidence") or []
    }
    missing_numbers = sorted(
        set(inventory.get("exercise_numbers") or []) - accepted_numbers)
    if (
        missing_numbers
        and not entry.get("_completeness_recovery_attempted")
        and page_checkpoints
        and checkpoint_root
    ):
        recovery_pages = []
        for page_item in pages_evidence:
            page_num = int(page_item["page_num"])
            page_text = str(page_item.get("text") or "")
            page_missing = [
                n for n in missing_numbers
                if re.search(
                    rf"(?m)(?:^|\\n)\\s*{re.escape(str(n))}\\s*[.\\-)]",
                    page_text)
            ]
            if not page_missing:
                continue
            progress(
                "SOURCE_COMPLETENESS_TARGETED_RECOVERY_START",
                page=page_num, missing_numbers=page_missing)
            refreshed = extract_scanned_page_exercises(
                doc, page_num, lesson_id, book_id, lesson_cache,
                drive_service=drive_service,
                checkpoint_root=checkpoint_root,
                entry=entry,
                force_refresh=True)
            page_checkpoints.save_exercises(
                drive_service, checkpoint_root, doc, entry,
                page_num, refreshed, source_provider, source_model)
            progress(
                "SOURCE_COMPLETENESS_TARGETED_RECOVERY_SAVED",
                page=page_num, extracted=len(refreshed))
            recovery_pages.append(page_num)
        if recovery_pages:
            retry_entry = dict(entry)
            retry_entry["_completeness_recovery_attempted"] = True
            return build_evidence_map(
                doc, retry_entry, drive_service=drive_service,
                persist_pages=persist_pages)

    attach_and_verify_source_completeness(ev_map)
    perm_path = PERM_EVIDENCE_DIR / f"{lesson_id}.json"
    perm_path.write_text(json.dumps(ev_map, ensure_ascii=False, indent=2), encoding="utf-8")
    return ev_map



# ==============================================================================
# 6B. TEXTBOOK-FIRST EXERCISE POLICY + STRICT AI FALLBACK
# ==============================================================================
def _lesson_scope_for_exercise_gate(ev_map: dict) -> List[dict]:
    """Compact, source-grounded lesson scope used by the exercise gate."""
    scope = []
    for c in ev_map.get("concepts", []):
        text = str(c.get("normalized_text") or c.get("raw_text") or "").strip()
        if not text:
            continue
        scope.append({
            "concept_id": c.get("concept_id"),
            "title": c.get("title"),
            "source_page": c.get("source_page"),
            "text": text[:1600],
        })
    if not scope:
        raise RuntimeError(
            "AI_ADDITIONAL_PRACTICE_PROHIBITED: no verified lesson concepts")
    return scope


def required_ai_practice_count(textbook_count: int) -> int:
    """Add at least three AI practice exercises when book practice is sparse.

    Product rule:
    - preserve and solve every verified textbook exercise;
    - never replace a verified textbook exercise with AI;
    - if fewer than 3 verified textbook exercises exist, generate at least
      3 evidence-gated AI practice exercises in addition to the verified ones;
    - if 3 or more verified textbook exercises exist, add no AI practice.
    """
    count = max(0, int(textbook_count))
    return 3 if count < 3 else 0


def generate_ai_practice_for_insufficient_book_exercises(
        entry: dict, ev_map: dict, profile: dict,
        verified_textbook_count: Optional[int] = None) -> List[dict]:
    """Add strictly lesson-grounded AI practice only when <=2 textbook exercises survived.

    Important: the trigger is the number of textbook exercises that were actually
    solved and scientifically verified, not the number merely extracted.
    Rejected AI candidates are discarded individually; they never cancel the lesson.
    """
    textbook_count = (
        max(0, int(verified_textbook_count))
        if verified_textbook_count is not None
        else len(ev_map.get("exercise_evidence") or [])
    )
    desired_count = required_ai_practice_count(textbook_count)
    if desired_count == 0:
        progress("AI_ADDITIONAL_PRACTICE_SKIPPED_BOOK_SUFFICIENT",
                 textbook_count=textbook_count)
        return []

    progress("AI_ADDITIONAL_PRACTICE_REQUIRED_BOOK_INSUFFICIENT",
             textbook_count=textbook_count,
             ai_target=desired_count)

    scope = _lesson_scope_for_exercise_gate(ev_map)
    accepted = []
    rejected_reasons = []

    for round_no in range(1, 4):
        remaining = desired_count - len(accepted)
        if remaining <= 0:
            break

        generator_prompt = (
            f"You are creating additional practice for Lebanese "
            f"{profile['subject']} Grade {profile['grade']}.\n"
            f"Lesson title: {entry['canonical_title']}\n"
            f"The official textbook yielded {textbook_count} reliably "
            "extractable exercise(s). Because fewer than 3 verified textbook "
            "exercises are available, generate AT LEAST 3 additional AI practice "
            "exercises. Preserve every verified textbook exercise and generate "
            "the AI practice ONLY from the VERIFIED LESSON SCOPE "
            "below. Do not introduce a law, definition, scientific concept, "
            "symbol, apparatus, material, quantity, unit, formula, fact, "
            "prerequisite, or real-world scenario that is absent from this scope. "
            "A new numeric value is allowed only as a practice input to a formula "
            "or quantitative relation explicitly present in the verified scope, "
            "using only units already present there. Do not require a figure. "
            "Make each question solvable entirely from what the student learned "
            "in THIS lesson, with no outside knowledge. Return JSON exactly as "
            "{'candidates':[{'prompt':str,'subquestions':[str],"
            "'solution_outline':str,'concept_ids':[str]}]}. "
            f"Return at least {max(remaining * 2, 4)} candidates so rejected "
            "ones can be discarded.\nVERIFIED LESSON SCOPE:\n"
            + json.dumps(scope, ensure_ascii=False)
        )
        if rejected_reasons:
            generator_prompt += (
                "\nDo NOT repeat these previously rejected defects:\n"
                + json.dumps(rejected_reasons[-8:], ensure_ascii=False)
            )

        try:
            generated = json.loads(execute_llm_completion(
                generator_prompt, json_mode=True, temperature=0.2,
                operation=f"ai_practice_generate_round_{round_no}",
                unit_id=f"ai_practice:round:{round_no}"))
        except (ProviderDailyQuotaError, ProviderTransientError,
                ProviderUnavailableError, NeedsAttentionError):
            raise
        except Exception as exc:
            rejected_reasons.append(f"AI generator unavailable: {exc}")
            progress(
                "AI_ADDITIONAL_PRACTICE_GENERATOR_FAILED_EXERCISE_ONLY",
                round=round_no, reason=str(exc)[:240])
            continue
        candidates = generated.get("candidates")
        if not isinstance(candidates, list):
            rejected_reasons.append("AI candidate list missing")
            progress(
                "AI_ADDITIONAL_PRACTICE_SCHEMA_REJECTED_EXERCISE_ONLY",
                round=round_no)
            continue

        for candidate in candidates:
            if len(accepted) >= desired_count:
                break
            if not isinstance(candidate, dict):
                continue
            prompt_text = str(candidate.get("prompt") or "").strip()
            subqs = candidate.get("subquestions") or []
            outline = str(candidate.get("solution_outline") or "").strip()
            claimed_ids = candidate.get("concept_ids") or []
            if (len(prompt_text) < 10 or not isinstance(subqs, list)
                    or not outline):
                rejected_reasons.append("incomplete candidate schema")
                progress("EXERCISE_REJECTED_SCHEMA",
                         round=round_no,
                         prompt_excerpt=prompt_text[:80])
                continue

            gate_prompt = (
                "Act as a strict curriculum exercise gate. Compare ONE proposed "
                "exercise with the VERIFIED LESSON SCOPE. Approve only if every "
                "fact, rule, relation, concept, apparatus/material, quantity, "
                "unit, formula, scenario, and required reasoning is directly "
                "supported by that scope. New numeric inputs are permitted only "
                "for a verified formula/relation and verified units already in "
                "scope. The task must be age-appropriate, internally consistent, "
                "solvable without outside knowledge, and its supplied solution "
                "outline scientifically correct. Reject if anything is merely "
                "plausible from general knowledge rather than traceable to this "
                "lesson. Reject if uncertain. "
                "Return JSON exactly as "
                "{'approved':bool,'reasons':[str],'supported_concept_ids':[str],"
                "'solution_consistent':bool,'within_scope':bool}.\n"
                "VERIFIED LESSON SCOPE:\n"
                + json.dumps(scope, ensure_ascii=False)
                + "\nCANDIDATE:\n"
                + json.dumps(candidate, ensure_ascii=False)
            )
            try:
                verdict = json.loads(execute_llm_completion(
                    gate_prompt, json_mode=True, temperature=0.0,
                    operation=f"ai_practice_gate_round_{round_no}",
                    unit_id=f"ai_practice_gate:round:{round_no}"))
            except (ProviderDailyQuotaError, ProviderTransientError,
                    ProviderUnavailableError, NeedsAttentionError):
                raise
            except Exception as exc:
                rejected_reasons.append(f"scientific gate unavailable: {exc}")
                progress(
                    "EXERCISE_REJECTED_SCIENTIFIC_GATE_UNAVAILABLE",
                    round=round_no,
                    prompt_excerpt=prompt_text[:100],
                    reason=str(exc)[:240])
                continue
            supported_ids = [
                str(x) for x in (verdict.get("supported_concept_ids") or [])
            ] if isinstance(verdict.get("supported_concept_ids"), list) else []
            actual_scope_ids = {
                str(item.get("concept_id")) for item in scope
                if item.get("concept_id")
            }
            supported_ids_valid = bool(
                supported_ids
                and set(supported_ids).issubset(actual_scope_ids)
            )
            approved = bool(
                verdict.get("approved")
                and verdict.get("solution_consistent")
                and verdict.get("within_scope")
                and supported_ids_valid
            )
            if not approved:
                reasons = verdict.get("reasons")
                if not isinstance(reasons, list):
                    reasons = ["scientific/scope gate rejected candidate"]
                rejected_reasons.extend(str(x) for x in reasons)
                progress("EXERCISE_REJECTED_SCIENTIFIC_GATE",
                         round=round_no,
                         prompt_excerpt=prompt_text[:100],
                         reasons=[str(x) for x in reasons][:5])
                continue

            idx = len(accepted) + 1
            supported = supported_ids
            accepted.append({
                "exercise_id": f"{entry['lesson_id']}-AI-{idx:02d}",
                "lesson_id": entry["lesson_id"],
                "section_type": "ADDITIONAL_PRACTICE",
                "number": idx,
                "source_page": None,
                "exact_source_prompt": prompt_text,
                "source_prompt_hash": hashlib.sha256(
                    prompt_text.encode("utf-8")).hexdigest()[:16],
                "subquestions": [str(x) for x in subqs],
                "requires_figure": False,
                "figure_refs": [],
                "figure_hashes": [],
                "solution_mode": "PRE_SOLVED",
                "solution_status": "NOT_SOLVED",
                "source_origin": "AI_ADDITIONAL_PRACTICE",
                "verified_against_source": False,
                "scientific_gate_passed": True,
                "scope_concept_ids": supported,
                "scope_snapshot_sha256": hashlib.sha256(
                    json.dumps(
                        [item for item in scope
                         if str(item.get("concept_id")) in set(supported)],
                        ensure_ascii=False,
                        sort_keys=True,
                    ).encode("utf-8")
                ).hexdigest(),
                "generator_claimed_concept_ids": [
                    str(x) for x in claimed_ids],
                "evidence_method":
                    "AI_GENERATED_AFTER_SOURCE_SCOPE_SCIENTIFIC_GATE",
            })
            progress("AI_ADDITIONAL_PRACTICE_ACCEPTED",
                     number=idx, round=round_no,
                     supported_concepts=supported)

    if len(accepted) < desired_count:
        # Never sacrifice a scientifically valid lesson because an optional AI
        # exercise could not pass the strict scope gate. Invalid exercises are
        # discarded individually. The target remains >=3 valid AI exercises.
        progress(
            "AI_ADDITIONAL_PRACTICE_BELOW_TARGET_LESSON_PRESERVED",
            accepted=len(accepted), target=desired_count,
            rejections=rejected_reasons[-8:])
    return accepted
