# NABIL Official Exam Archive — free, diskless operating mode

## Scope
This phase indexes public Lebanese official mathematics certificate examinations exposed by the CRDP archive:
- https://www.crdp.org/official-exams-corrections-lebanon
- https://www.crdp.org/guideline-official-exams

The scanner checks archive pagination (default 300 pages), discovers direct PDF links hosted only on `crdp.org` / `www.crdp.org`, and reads the surrounding CRDP table row because the visible link itself is often labelled only “PDF”. It fetches each PDF transiently, extracts its text, and keeps a compact metadata catalogue plus extracted text **in process memory only**. It does not write PDFs, OCR output, or an index to Render's filesystem. SHA-256 identifies each source file and detects if it changes before a later download.

## Storage and cost
- No Render persistent disk is required.
- No paid storage or external storage account is required.
- Do not set `NABIL_EXAM_ARCHIVE_DIR`; this implementation does not use it.
- The in-memory catalogue and extracted text are lost whenever the service restarts, sleeps, or redeploys. Run a fresh CRDP sync after that. The CRDP website remains the source of truth.
- Original PDFs are downloaded on demand from their official CRDP URLs and streamed to the browser; they are not retained on the service.
- This mode avoids persistent storage costs but requires network access to CRDP and may take time to rebuild the catalogue.

## Render environment
Set:
- `NABIL_ARCHIVE_ADMIN_TOKEN`: optional. If configured, the archive sync endpoint requires this secret; if omitted, the public UI can start a scan subject to a six-hour in-memory cooldown and one active scan at a time.
- `GEMINI_API_KEY` (or `NABIL_LLM_API_KEY`): enables retrieval-augmented AI question generation.
- `NABIL_LLM_MODEL`: optional model override.
- `NABIL_LLM_BASE_URL`: optional OpenAI-compatible API base URL.

Never commit the archive admin token or provider API key to Git. No storage bucket, paid disk, or storage credentials are needed.

## How to run
1. Open the competitions site.
2. Open “Official Lebanese exam archive”.
3. Start the CRDP mathematics archive sync; no token is required in the default configuration.
4. Wait for the scan to finish, then refresh status.
5. Browse by branch/year, search the extracted text, and download original PDFs.
6. The public scan endpoint enforces one active scan and a six-hour cooldown to reduce abuse.

API:
- `GET /api/competitions/archive/status`
- `GET /api/competitions/archive/documents?grade=Terminale%20GS&year=2024&limit=50&offset=0` browses the mathematics PDF catalogue.
- `GET /api/competitions/archive/search?q=derivatives&grade=Terminale%20GS` searches extracted text and returns matching excerpts.
- `GET /api/competitions/archive/documents/{id}` fetches and downloads the matching original PDF from CRDP on demand.
- The public page provides branch/year filters, text search, and direct PDF download links. The sync token is needed only to start a fresh scan, not to browse or download already-indexed records.
- `POST /api/competitions/archive/sync` starts a background scan. If `NABIL_ARCHIVE_ADMIN_TOKEN` is configured, send it in `X-Archive-Admin-Token`; otherwise the endpoint applies a six-hour cooldown.

## Extraction and classification
Embedded PDF text is extracted in memory. If a PDF is scanned and Tesseract with Arabic, English, and French language data is available on the host, OCR is attempted in memory; otherwise it is marked `needs_ocr`. OCR failure is visible and is never represented as successful learning. Branch, year, session, language, and correction indicators are inferred from document titles/content and must be treated as catalogue hints, not guaranteed official metadata.

## Generation and quality policy
When an AI model key is configured, matching archive excerpts are supplied as **historical examination-style evidence**, not as proof of the current curriculum. Without an AI model key, NABIL can still catalogue, search, display and download original CRDP PDFs and attach local mathematics teaching blueprints to its question drafts; it cannot honestly claim to have semantically read, understood or learned the archive. The local blueprint is a transparent rule-based guide, not a substitute for an AI researcher or a teacher's mathematical review. Generated questions must match the selected lessons exactly; each question must have a corresponding solution and rubric; question parts, rubric criteria, and total marks must reconcile. Failed checks stop generation.

If no model key is configured, the service uses the deterministic offline generator and marks that official archive records were **not used to generate** the paper. It must not describe this fallback as AI or claim it learned from the archive.

## Limitations
- This phase indexes mathematics examinations only.
- A catalogue scan is only as complete as the CRDP pages reachable during that scan; status reports page failures and whether the scan reached its configured end.
- The in-memory catalogue disappears on restart; a new sync is required.
- Some years, sessions, or corrections may be absent from CRDP. Never invent missing answer keys.
- Historical papers inform examination style and assessment depth. Current curriculum verification requires the latest official scope/specification.
- Generated assessments must be newly authored, not copied wholesale from official papers.
