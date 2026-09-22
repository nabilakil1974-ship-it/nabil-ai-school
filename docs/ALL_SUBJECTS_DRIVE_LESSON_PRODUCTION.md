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

## Owner's non-negotiable AI policy (2026-09-22)
**Prepared textbook-authored Drive HTML FIRST; no generative AI to recreate the lesson when a verified HTML lesson exists.** AI only for student follow-up, alternate explanations, genuinely missing material or unavailable prepared lesson, with original indexed PDF grounding and explicit source limitations. Do not auto-generate hundreds of superficial template pages and call them finished. Exact source figures and exercise numbering must be checked individually. Keep the source PDF manifest and authored HTML connected via the production ledger.

## Durable progress
`data/interactive_lesson_production_ledger.json` is the authoritative per-book/grade record; status `verified_complete` only after EVERY lesson in the book is authored, uploaded and tested. The Drive lesson folder was listed via owner's connected Drive on 2026-09-22 and contained ONLY the two EB9 Conducteurs ohmiques HTML variants and associated manifests/readmes; this is NOT proof of the Railway service account's access. The repository contains 16 physics, 32 math, 11 chemistry, 11 biology book-to-grade mappings. General science mapping remains open. Do not misrepresent mappings as authored lessons.

## Strict sequential production rule — owner approved
For each subject in priority order, process **one grade/stream/language textbook at a time, from its actual table of contents, chapter 1 lesson 1 through the final lesson**. Never skip a chapter, lesson, activity, figure or exercise; never jump to a later grade because it is easier. Before authoring, transcribe and verify the complete source TOC with printed and PDF page boundaries and store a per-lesson checklist in the durable ledger. For each lesson, record source book ID, TOC ordinal, chapter, original title, printed/PDF page ranges, numbered exercises, HTML Drive ID, authoring and live verification statuses. An unreadable or inaccessible lesson is marked BLOCKED and cannot be silently passed over; resume it before advancing. No grade/stream/language is complete until all TOC entries are VERIFIED. Existing EB9 Conducteurs ohmiques is a reference example, not permission to skip preceding chapters in EB9. G07 Solids and Liquids is authored/uploaded but remains unverified; proceed with G07's actual next TOC lesson before G08. Never use generative AI to substitute for prepared source-grounded lesson unless necessary.

## Owner-visible Drive filing convention (2026-09-22)
Root **NABIL AI - Interactive Curriculum** Drive ID `16bcmZMO_dn4FqlGaDtl8Hky6iSBEqZpX`; per grade folder e.g. Grade 7 `1baLppRVEbnjIa62vb7KUFaTLSUiRiEIa`; per subject subfolder e.g. Physics - فيزياء `12BzdBUmPIK2__Fl3yTXpfZ-LXNjfimAq`. Every NEW authored HTML belongs inside ROOT / Grade N / Subject / ordered lesson file; when mathematics starts, create Mathematics - رياضيات INSIDE that same grade folder, not at root. G07 Solids and Liquids owner-visible file ID `17u-wfoft9hSFMyZJNIBxsEMDwMxLyXby` moved into Grade 7 / Physics. Its separate original Drive lesson ID `1tEPcbUBaPvIblK-4Zo3rXb31lqUE0tCN` remains in backend configured lesson collection for resolver compatibility. For every new lesson maintain both discoverable owner folder organization and backend resolution, or update backend to traverse grade/subject folders safely; never assume the two folder trees are the same.

## Actual owner Drive folder creation
On 2026-09-22 created/verified Grade 1 through Grade 12 under owner root `16bcmZMO_dn4FqlGaDtl8Hky6iSBEqZpX`; each grade has the five subject folders Physics - فيزياء, Mathematics - رياضيات, Chemistry - كيمياء, Biology - علوم الحياة, General Science - علوم عامة (Grade 9 pre-existing Physics folder is named "Physics" and was preserved). These folders are organizational placeholders; only authored, source-verified HTML belongs inside, and an empty folder does not imply that subject is taught in that grade. Existing G07 Solids and Liquids is in Grade 7 / Physics - فيزياء. Dynamic resolver `app/api/routes_interactive_lessons.py` scans root/grade/subject HTML every 10 seconds, no per-lesson code edits; the ONE-TIME backend deploy and Drive service-account read access to owner root/descendants must still be verified. Avoid per-lesson hard-coded IDs. Grade 11/12 may require stream-specific subfolders in future; ensure resolver handles streams before authoring them.
