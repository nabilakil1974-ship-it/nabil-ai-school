# Durable science textbook indexing — Railway

## Why the old Console command stopped
Railway replaces the web container on each deployment. A command started in
**web → Console** runs inside that container. Neither `nohup` nor `&` can
guarantee it survives the container being destroyed.

## Preferred permanent setup (one time)
Create a **second Railway service** in the same project/environment, connected
to the same GitHub repository and PostgreSQL/database + Drive variables.

- Service name: `science-worker`
- Builder: Dockerfile; path: `/Dockerfile`
- Custom Start Command: `python -m scripts.science_worker`
- Copy or reference `DATABASE_URL` and `GOOGLE_DRIVE_CREDENTIALS_JSON` from
  the web service via Railway shared variables/references. Never put them in git.
- It needs sufficient RAM for the multilingual embedding model and OCR.
- No public domain/port is required for the worker.
- Leave the web service command as `python -m scripts.start_server`.
- Do NOT run a second science indexer in web Console simultaneously.

This lets web deployments proceed without interrupting science-worker.
If the worker itself restarts or gets redeployed, per-PDF-page checkpoints in
PostgreSQL make it skip committed pages and continue missing ones. PostgreSQL
advisory lock serializes concurrently booting workers during rolling deploys.

## Alternative if a separate service is not possible
Set `NABIL_AUTO_INDEX_SCIENCE=1` in web service Variables, then deploy. The
existing `python -m scripts.start_server` launches one background indexer on
EVERY web container start; restarting/deploying web then relaunches it.
WARNING: OCR + sentence-transformers can consume significant CPU/RAM; this may
slow or crash the student website on a small Railway instance. Prefer worker.

## Progress and safe re-run
On any running service using the current code:
```bash
python -m scripts.science_progress
python -m scripts.index_science_textbooks all
```
The second command is manual and only runs until that container exits; the
database progress survives. NEVER run it while science-worker is active
(waiting for exclusive lock is safe, but redundant).

The index order is chemistry → physics → biology. A completed PDF page,
including OCR-empty page verified without subprocess error, is tracked using
`book_pages.pdf_page_index` (1-based). Existing older `book_chunks` pages are
also recognized. A partial page transaction is retried, and a failed OCR
page is NOT checkpointed as complete. Original PDFs remain on Google Drive.
