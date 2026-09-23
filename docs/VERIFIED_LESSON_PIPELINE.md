# NABIL verified lesson pipeline — staged integration

This branch introduces `scripts/verified_lesson_publisher.py`. It does **not**
replace `scripts/nabil_lesson_factory.py`, change Railway startup, run
automatically, or mark any lesson scientifically approved.

## Purpose
Take a *source-grounded authored bundle* and reject it unless the PDF hash,
page-specific verbatim excerpts, lesson structure, images, nine-slide EN/FR
PowerPoints, and EN/FR desktop/mobile browser smoke checks pass. With explicit
`--publish`, upload only to the existing
`NABIL AI - Interactive Curriculum/Grade N/Subject/NN - Chapter` tree,
using owner OAuth already supported by `nabil_lesson_factory.drive(write=True)`.
Never overwrite a previous published lesson. The resulting state is
`UPLOADED_PENDING_RAILWAY_ACCEPTANCE`, not APPROVED.

## Run (in a checkout with browser dependencies installed)

```sh
python -m playwright install chromium
python -m scripts.verified_lesson_publisher --manifest /path/to/bundle/manifest.json --report /tmp/lesson-gate.json
python -m scripts.verified_lesson_publisher --manifest /path/to/bundle/manifest.json --publish --report /tmp/lesson-publish.json
```

The manifest must contain:

```json
{
  "lesson_id": "g09_math_lines_and_circles",
  "grade": 9,
  "subject": "mathematics",
  "chapter": 1,
  "title": "Lines and Circles",
  "source_pdf": "Building up Mathematics Grade 9.pdf",
  "source_sha256": "actual lowercase sha256",
  "source_claims": [
    {
      "pdf_page": 19,
      "verbatim_excerpt": "a sufficiently long exact excerpt copied from PDF text",
      "lesson_claim": "Exercise 7a numbers and solution"
    }
  ],
  "html": "g09_math_lines_circles_bilingual.html",
  "pptx_en": "NABIL_EB9_Lines_Circles_EN.pptx",
  "pptx_fr": "NABIL_EB9_Lines_Circles_FR.pptx",
  "images": ["positions.png", "tangents.png", "ex1.png", "ex2.png"]
}
```

## Remaining work before autonomous production

1. Extract verified chapter tables of contents from each actual Drive PDF;
   do not infer chapters/pages from file names or other books.
2. Implement a reusable *authoring* stage, with subject-specific scientific
   figure validation and independent solution checks. The EB9 builder is
   hardcoded for a single math chapter and is not a universal generator.
3. Add semantic, screenshot-diff and real platform endpoint checks to the
   gate; current browser checks are smoke checks, not full acceptance.
4. Confirm owner OAuth variables in Railway without logging tokens; verify
   the platform indexes the resulting Drive folder and opens the lesson.
5. Only then schedule a bounded worker with idempotency, retries, cost limits,
   and a production ledger that never marks a failed or unreviewed lesson
   approved.
