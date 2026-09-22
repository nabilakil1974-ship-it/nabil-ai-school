# NABIL AI — verified-textbook interactive lesson production

Owner order (2026-09-22): **Physics (all available grades/streams/languages) → Mathematics → Chemistry → Biology → General Science**. Produce every actual chapter/lesson from the corresponding official textbook using the EB9 Conducteurs ohmiques model, not placeholder lessons. Work through source PDF and source figures, preserve printed vs PDF page mapping, chapter/activity/exercise number, and clearly mark explanatory redrawn figures as such. Do not claim a lesson is complete until its source mapping, full content, interactions, mobile layout, Drive upload, and Railway resolve/view have passed.

## Confirmed inventory from repository manifests
- Physics: `data/physics_textbooks_manifest.json`: 16 grade/language/stream mappings, 13 unique Drive PDFs (some PDFs shared between streams).
- Chemistry: `data/chemistry_textbooks_manifest.json`: 11 mappings, 10 unique Drive PDFs.
- Biology: `data/biology_textbooks_manifest.json`: 11 mappings, 11 unique Drive PDFs.
- Mathematics: locate existing math manifests/index and validate against Drive before claiming any count.
- General science: locate and classify original grade 1–6 general-science books and any separate higher-grade science courses before claiming any count.

## Production queue and acceptance gates for EACH lesson
1. Open exact original book/edition/language; identify actual chapter boundaries and all relevant printed/PDF pages; record textbook Drive file ID and exact title.
2. Audit every activity, experiment, chart, figure and numbered exercise in that chapter; record any unreadable visual as pending verification, NEVER fabricate its data.
3. Author complete accessible bilingual or source-language HTML with accurate formulas and diagrams, worked authentic textbook exercises, responsive cards, practical interactive checks, a scored worksheet, and a comprehensive final reference card. For source-language translations, do not invent independent translated-book page citations.
4. Review scientific and mathematical correctness; distinguish original source image from explanatory redrawing; prevent cross-subject content leakage.
5. Upload HTML into the configured Drive collection (or catalog), with grade, subject, title, language, source ID, source pages and aliases. Do not embed individual lesson HTML in GitHub.
6. Verify Railway service-account access and GET /api/interactive-lessons/resolve and /view for exact grade/subject/lesson/language; confirm bilingual switching, figures, mobile 390x844, quiz, worksheet, printable reference, PowerPoint download.
7. Record per-lesson status and failed checks; only then mark VERIFIED. Indexed-PDF AI teaching remains fallback.

## Status as of initial queue registration
- EB9 French Physics Conducteurs ohmiques: authored bilingual HTML is documented in Drive, with integration code; **live Railway/mobile/export verification not established**.
- Other lessons: **NOT YET AUTHORED OR VERIFIED BY THIS QUEUE**. An indexed textbook is not equivalent to an authored interactive HTML lesson.

## Existing implementation
`app/api/routes_interactive_lessons.py` Drive resolver; `app/static/nabil_drive_prepared_lesson_v1.js` lesson display; `app/api/routes_lesson_export.py` PPTX/reference; `app/static/nabil_universal_lesson_actions_v1.js` student actions; `scripts/index_science_textbooks.py` science indexer. Keep source-authored HTML in Drive, not repository. Owner-approved baseline: `docs/NABIL_DRIVE_LESSON_BASELINE_2026-09-22.md`.
