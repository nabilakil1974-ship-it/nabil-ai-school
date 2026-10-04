# NABIL — Live acceptance status

Rule: **Implemented != GREEN. GREEN means live End-to-End verified on deployed Railway with a real Golden lesson.**

| # | Requirement | Current status | Current evidence |
|---|---|---|---|
| 1 | Canonical Golden lesson catalogue and exact selection | 🟠 IMPLEMENTED / NOT LIVE VERIFIED | 2026-10-04: previous Railway test failed to load lessons. Runtime has now been changed to read `data/golden_lesson_links.json` locally instead of Google Drive. Must retest after deploy. |
| 2 | No fallback; immutable exact lesson_id | 🟠 IMPLEMENTED / NOT LIVE VERIFIED | Code is strict; blocked from live proof until #1 is retested. |
| 3 | Approved reference cards and readable desktop/mobile layout | 🟠 IMPLEMENTED / NOT LIVE VERIFIED | Renderer exists; not yet observed on a real lesson after catalogue recovery. |
| 4 | Complete ordered teaching sequence + Golden Final Card | 🟠 IMPLEMENTED / NOT LIVE VERIFIED | Code path exists; not yet live-proven. |
| 5 | Source-locked, scientifically verified, reference-quality animated labs | 🟠 IMPLEMENTED / NOT LIVE VERIFIED | Requirement-5 gates and reference lab renderer exist; real published mathematics lab still must be observed live. |
| 6 | Interrupt -> answer -> resume same card/line | 🟠 IMPLEMENTED / NOT LIVE VERIFIED | FormData interrupt bridge and position state exist; still requires live proof. |

## 2026-10-04 snapshot-runtime integration

Merged the snapshot architecture supplied for review into the existing NABIL Golden path without creating a second student-facing catalogue.

Changes:
- Added `app/services/golden_registry.py`: local canonical registry reader, exact lesson IDs, SHA-256 verified snapshots, path-traversal protection, last-good registry cache.
- Changed `app/services/golden_catalogue.py`: catalogue reads the local canonical registry; **student requests no longer call Google Drive**. Lesson content uses a verified synchronized snapshot first, then an already-published structured artifact for compatibility. If neither exists, it fails closed with `GOLDEN_CONTENT_UNAVAILABLE` and never substitutes another lesson.
- Added `scripts/sync_golden_snapshots.py`: read-only Drive/Docs synchronization for the lesson IDs/file IDs already present in NABIL's registry; preserves the last good snapshot on failure.
- Added `.github/workflows/sync-golden-snapshots.yml`: scheduled/manual snapshot sync and commit.

Important: the existing registry currently contains real Golden entries such as `G12-MATH-GS-001` and `G12-MATH-GS-002`, so the catalogue can be served locally after deployment even when Drive is unavailable. Opening the lesson itself requires either its synchronized snapshot or an existing structured artifact.

Next acceptance action: deploy, verify the mathematics dropdown loads from the canonical local registry, then open a real lesson and proceed through requirements 2–6. Do not mark any item GREEN before that live test.
