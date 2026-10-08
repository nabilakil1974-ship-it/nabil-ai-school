# NABIL platform — batch lesson receiving contract

The platform is prepared to receive lessons produced by the all-books/all-lessons
factory without hardcoding a subject list into the runtime.

## Package destination

Default directory:

`data/lesson_packages/<LESSON_ID>/`

Each package must contain `manifest.json`. The platform never fuzzy-matches a
lesson title and never chooses a different lesson when the exact ID is missing.

## Minimal manifest

```json
{
  "schema_version": "1.0",
  "lesson_id": "G12-MATH-GS-001",
  "title": "Irrational Functions",
  "grade": "12",
  "subject": "Mathematics",
  "language": "en",
  "status": "READY",
  "source_identity": "...",
  "p1_identity": "...",
  "p2_scientific_identity": "...",
  "p3_status": "candidate",
  "artifacts": {
    "lesson_html": "lesson.html",
    "exercise_html": "exercises.html",
    "teacher_docx": "teacher/G12-MATH-GS-001-TEACHER-PREPARATION-CRDP.docx",
    "teacher_json": "teacher/G12-MATH-GS-001-TEACHER-PREPARATION.json",
    "faq_bank": "faq_bank.json",
    "exercise_bank": "exercise_bank.json",
    "p3_manifest": "p3/manifest.json"
  }
}
```

A package is student-runtime-ready only when:

- `status == READY`;
- `lesson_html` exists inside that lesson package;
- artifact paths remain inside the package directory.

## Runtime endpoints

- `GET /api/content-registry/readiness`
- `GET /api/content-registry/lessons`
- `GET /api/content-registry/lessons/{lesson_id}`
- `GET /api/content-registry/artifact/{lesson_id}/{artifact_kind}`

The Golden resolver is also patched to prefer an exact READY packaged
`lesson_html` before its older Drive-backed path. No runtime AI call is needed.

## Supported catalogue dimensions

Grades 1–12, branches, AR/EN/FR, and a universal subject-code resolver including
Math, Physics, Chemistry, Biology, General Science, Arabic, English, French,
History, Geography, Civics, Philosophy, Sociology, Economics, Computer Science,
Art, Music and Physical Education. Stable explicit subject codes in lesson IDs
remain accepted even when a new subject alias is added later.

## Batch-worker rule

The producer writes all artifacts first and writes/renames `manifest.json` last.
That makes publication atomic: the platform never serves a half-built lesson.

Failed lessons remain visible as FAILED/NEEDS_AUDIT in readiness statistics but
are never served as READY student lessons.
