# NABIL Official Exam Archive — setup and operating notes

## Scope of this phase
This phase indexes **Lebanese official mathematics certificate examinations** and the PDFs exposed by the CRDP archive page. It scans all requested archive pages (default 300), not just the newest page, because older mathematics records may be separated by pages containing other subjects.

Official source:
- https://www.crdp.org/official-exams-corrections-lebanon
- https://www.crdp.org/guideline-official-exams

The indexer downloads only HTTPS PDF links hosted on `crdp.org` / `www.crdp.org`. It preserves original PDFs, computes SHA-256 hashes, extracts embedded PDF text, and stores metadata for branch, year, session, and language. If a PDF has no usable text layer, it is marked `needs_ocr`; it is not silently treated as searchable or fully learned. Some CRDP PDFs contain both the question paper and correction/barème in one file; this is recorded when detected in extracted text.

## Required Render environment configuration
Set these environment variables on the **nabil-competitions-preview** service:

- `NABIL_ARCHIVE_ADMIN_TOKEN`: a long random secret used by the archive-sync button/API.
- `NABIL_EXAM_ARCHIVE_DIR`: a persistent mounted path, e.g. `/var/data/exam_archive`. Attach a persistent disk mounted at `/var/data` first. Without persistent storage, downloaded PDFs and the index can disappear on a redeploy/restart.
- `GEMINI_API_KEY` (or `NABIL_LLM_API_KEY`): enables retrieval-augmented AI question generation. The key must have access to the configured model.
- `NABIL_LLM_MODEL`: optional model override; default is `gemini-2.5-flash`.
- `NABIL_LLM_BASE_URL`: optional OpenAI-compatible API base URL. If only `GEMINI_API_KEY` is set, the Google Gemini OpenAI-compatible endpoint is selected automatically.

Never commit the archive admin token or provider API key to Git.

## How to run
1. Open the competitions site.
2. In “Official Lebanese exam archive”, enter the archive admin token.
3. Select “Sync and download official mathematics archive”.
4. Wait for the background job to finish and refresh the status.
5. Check counts by branch and the number of PDFs requiring OCR.

The API also exposes:
- `GET /api/competitions/archive/status`
- `GET /api/competitions/archive/search?q=derivatives&grade=Terminale%20GS`
- `POST /api/competitions/archive/sync` with `X-Archive-Admin-Token` header.

## Generation and quality policy
When a model key is configured, generation retrieves matching archive excerpts and feeds them to the model as **historical exam-style evidence**, not as proof of the current curriculum. The generated questions must match the selected lesson list exactly; every question must have a corresponding solution and rubric; question parts and rubric criteria must sum to the question marks; all questions must sum to the requested total. Failed checks stop generation.

If no model key is configured, the service explicitly falls back to the deterministic offline generator and marks that official archive records were **not used to generate** the paper. It must not describe this fallback as AI or claim it learned from the archive.

## Limitations to keep visible
- This first phase indexes mathematics exams only. Other subjects are a later expansion.
- OCR for scanned/image-only PDFs is flagged but not performed automatically in this phase.
- The CRDP archive may contain missing years, sessions, or corrections; the application must report what it actually indexed and must never invent missing answer keys.
- Historical exam papers inform exam style and assessment depth; current curriculum verification must use the latest official scope/specification.
- Original exam PDFs are source materials. Generated assessments must be newly authored, not copied wholesale.
