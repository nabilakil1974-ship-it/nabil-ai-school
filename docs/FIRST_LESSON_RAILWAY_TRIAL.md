# NABIL AI — first full-bundle trial (EB9 Physics)

**No existing approved lesson is overwritten.** Source of truth is the owner's
Google Drive. GitHub holds code only. The first trial is a review draft, not a
live approved lesson.

## Actual Railway layout

The web service runs `python -m scripts.start_server` (railpack.json and
Procfile). **Do not replace its start command** with a one-shot authoring job.
Use a separate Railway worker/job in the same project and with the needed
server-side secrets. The project name alone does not prove a worker exists.
No Railway access token or OAuth refresh token should be sent in chat.

## First lesson: source-verified Conducteurs ohmiques

Book Drive ID: `11dqVqafG9zhr1sQzsjD3kxc5thA2DvZC`.
Grade 9 / physics / chapter 8 / French source. PDF pages **92–102**
correspond to printed pages 93–103 in the recorded reference manifest.
This page mapping is a manifest claim and must be checked against the PDF
before approval. English is a translation, NOT an independently verified
English textbook.

Use a Railway worker shell in the checkout of branch
`feature/verified-drive-lesson-pipeline`:

```sh
python -m scripts.nabil_lesson_factory --author-lesson \
 --book-id 11dqVqafG9zhr1sQzsjD3kxc5thA2DvZC \
 --grade 9 --subject physics --chapter 8 \
 --title "Conducteurs ohmiques" --pages 92-102 --language fr \
 --out /tmp/nabil-eb9-physics-ohmic
```

Requires existing Drive read credentials and server-only OPENAI_API_KEY.
Never place credentials in HTML, GitHub commits or student devices.

Outputs in ONE command: `source.pdf`, `lesson_draft.json`,
`lesson.html`, `lesson_en.pptx`, `lesson_fr.pptx`,
`source_pdf_page_*.png`, `manifest.json`, `report.json`.
The original page pictures preserve book evidence, but are **not a substitute
for verified reconstructed scientific diagrams**. PPTX has concept → original
source page → activity → solution → exercise → solution → worksheet → answer
→ summary. The ABC3 PowerPoint reference must be supplied and visually
compared before design approval; it is not present in this pipeline.

## Gate before Drive publication

```sh
python -m scripts.verified_lesson_publisher \
 --manifest /tmp/nabil-eb9-physics-ohmic/manifest.json \
 --report /tmp/nabil-eb9-physics-ohmic/acceptance.json
```

This checks PDF citations, bilingual HTML, images, PPTX and browser display.
It requires Playwright + Chromium on the worker:
`pip install playwright && python -m playwright install chromium`.
The existing requirements.txt does not include Playwright; the normal web
service should not be made to download Chromium merely for this pilot.

Scientific and reference-design review must be performed on the **actual
generated artifacts**. Only then set BOTH manifest fields
`scientific_review_approved` and `reference_design_approved` to true.
An unreviewed AI draft MUST NOT set them. Publishing uses explicit
`--publish` and owner OAuth credentials; no overwrite.

Destination must resolve to:
`NABIL AI - Interactive Curriculum/Grade 9/Physics/08 - Conducteurs ohmiques`.
The current approved reference resides in a legacy physics collection and
must not be deleted or overwritten during the trial. A successfully uploaded
draft is still `UPLOADED_PENDING_RAILWAY_ACCEPTANCE` until
`/api/interactive-lessons/resolve` and `/view` pass for BOTH fr and en,
including diagrams on a mobile viewport.

## Acceptance ledger

- [ ] Worker generated complete bundle from the actual PDF.
- [ ] Every cited excerpt matches its PDF page.
- [ ] All science diagrams and solutions independently checked.
- [ ] ABC3 reference PowerPoint supplied and both language decks compared.
- [ ] Browser tests pass mobile and desktop, both languages.
- [ ] Explicit approval then Drive write/read-back.
- [ ] Railway NABIL view and resolve work in French and English.
- [ ] Only then: APPROVED.

A green GitHub mock test is **not** evidence that the Railway worker ran,
Drive upload worked, or that an actual lesson matches the reference.
