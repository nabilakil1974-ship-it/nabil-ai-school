NABIL AI FINAL DROP — 2026-10-02

Contains only local files for manual upload by the owner. Nothing in this bundle writes to GitHub.

Golden runtime:
lesson_id -> local LessonPackage -> Drive service account -> cache -> student.
A supplied lesson_id never falls through to RAG/LLM when Golden is missing.

Protection:
12 requests/minute by default, 4000 chars/message, hashed student+network fingerprint, SQLite WAL.
Configure NABIL_SECURITY_SALT in Railway.

Finance/cost control:
Internal cost ledger in data/nabil_control.db. It records cache/Drive/AI gateway events.
NABIL_DAILY_AI_BUDGET_USD=0 means no hard budget until the owner sets one.
This module does NOT charge cards or invent provider pricing.

Labs:
Factory freezes verified labs after existing quality/scientific gates.
validate_lab_spec/evidence fail-closed logic is unchanged.
Shared browser voice helper is app/static/nabil_lab_voice_v1.js.

Important deployment requirement:
data/ must be on a persistent Railway volume if you want the finance/rate ledger and local Golden cache/registry state to survive container replacement.
