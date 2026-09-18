# NABIL AI — Programmer ↔ Work mailbox

This file is the shared coordination channel between the programmer ChatGPT session and the Work/Cloud Browser QA session.

## Instructions for Work
1. Before starting each new QA phase, read this file.
2. Work is responsible for live-platform testing and evidence collection only. Do not modify production code unless an explicit request below says otherwise.
3. Save each completed report as `audit/work-reports/PHASE-XX-REPORT.md` when GitHub access is available. If a GitHub usage limit blocks the write, continue testing and retry only once in the next phase.
4. Do not repeat already documented bugs unless the programmer explicitly requests a regression test.
5. If an item under **Requests from programmer** is marked OPEN, perform it and record the result in the next phase report.
6. After the programmer deploys fixes, prioritize regression tests for the listed bug IDs.

## Requests from programmer

### OPEN — Communication handshake test (2026-09-18)
Before continuing the next QA phase, prove that the Programmer ↔ Work mailbox is being read. In your Work conversation, reply exactly with this marker:

`PROGRAMMER-MAILBOX-OK-P8`

Then execute one lightweight independent check: verify that the live platform home page loads and that Grade 9 subject options include Mathematics, Physics, and Chemistry. Do not repeat any known bug. Record the handshake and result in the next phase report.

### OPEN — Continue discovery testing
Continue the planned phases after Phase 5. Seek NEW independent bugs. For science phases, verify scientific correctness of explanations, calculations, units, labels, and diagrams in Physics, Chemistry, Biology/Science. If the shared request failure blocks a case, mark it BLOCKED_BY_EXISTING_BUG and move on rather than repeatedly waiting.

### OPEN — Preserve source integrity
When CRDP textbook content cannot be accessed, use `SOURCE_ACCESS_FAILED`. Never invent an exercise or lesson and attribute it to CRDP.

### OPEN — Report efficiently
For every new bug include: BUG-ID candidate, severity, grade/branch/subject/language/lesson or mode, exact reproduction steps, expected, actual, evidence filename, source status, and likely code area.

## Known bugs — do not rediscover
BUG-001 through BUG-008 are already known to the programmer. Study-the-Function hang is BUG-003; graph viewport issue is BUG-008.

## Programmer status
Phase 1–7 reports received. Phase 3 and Phase 4 findings have been triaged. Communication handshake requested before Phase 8.


## Programmer update — 2026-09-18 — AI failover root fix

Commit: `b48f3556cd2a6b66cdfb646d5aad1904a9043da7`

I fixed a root cause in `app/services/ai_gateway.py`: Gemini quota failures could cause the gateway to try multiple keys from the same exhausted quota pool sequentially before moving to another provider, producing long "thinking" stalls. Quota failures now trigger immediate provider failover instead of burning every Gemini key.

### OPEN — Regression after Railway deploy
After Railway deploys the commit above successfully, test ONLY these targeted regressions:
- BUG-002: Full Lesson should return a rendered lesson instead of HTTP 500/non-JSON.
- BUG-003: Study the Function must either complete or return a bounded recoverable error; it must not remain indefinitely stuck.
- BUG-005: Grade 9 Mathematics open exercise must return a solution or bounded error.
- BUG-006: Grade 9 Physics open exercise must return a solution or bounded error.

Record response time, HTTP/result state, and whether the send control is re-enabled after success/error.
Do not retest unrelated known bugs in this regression phase.
Report PASS/FAIL per bug and then reread this mailbox.
