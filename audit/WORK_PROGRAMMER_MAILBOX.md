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


## HIGH PRIORITY — Pedagogical acceptance testing

The owner explicitly prioritizes testing the QUALITY of teaching and exercise solving, not only UI reliability.

After the current regression/deployment is stable, run a dedicated pedagogical phase using the live platform. Test representative Mathematics, Physics, Chemistry, Biology/Life Sciences, and language lessons/exercises across at least primary, intermediate, and secondary levels.

For FULL LESSON explanations verify:
- explanation is progressive, student-level, and teacher-like rather than a lecture;
- correct grade/subject/language/lesson boundary;
- concept -> explanation -> worked example/application -> final summary;
- accurate useful diagram/graph when pedagogically needed;
- exactly 5 additional exercises after a full lesson, each with the required visual when appropriate and a complete step-by-step solution;
- no invented givens, facts, labels, points, or source claims.

For EXERCISE SOLVING verify the NABIL teacher method:
- Given -> Required -> Formula/Property -> substitution/reasoning -> units -> Final Answer;
- Mathematics: exact reasoning and valid geometry/function graphs; function study includes domain, limits, intercepts, asymptotes, derivative, extrema, increasing/decreasing intervals, variation table, exact graph when applicable;
- Physics: correct law, substitution, SI units, direction/signs and diagram;
- Chemistry: correct symbols/equations/balancing/structures;
- Biology: scientifically accurate labelled diagrams/processes;
- Languages: natural level-appropriate explanation and correction.

Also test “Explain another way” and remediation after a wrong answer: it must genuinely change strategy and target the misconception, not merely paraphrase the first explanation.

Use several real prompts per subject. Judge mathematical/scientific correctness separately from pedagogy and rendering. Save evidence for failures. Do NOT mark PASS merely because a response rendered.

Create a dedicated report named `PHASE-PEDAGOGY-REPORT.md` with PASS/FAIL by subject and concrete examples. Then reread this mailbox and continue automatically.


## OWNER PEDAGOGICAL SIGNATURE — mandatory

The owner clarified that NABIL AI's explanations and exercise solutions must match ChatGPT's best student-facing teaching quality: clear, elegant, warm, concise where possible, and deeply explanatory where needed. Do not produce robotic textbook dumps or dry lecture prose.

Required teaching signature:
- Start directly from what the student needs; avoid long introductions.
- Break difficult ideas into small logical steps and explain WHY each step is done.
- Use simple student-appropriate wording while preserving exact scientific terminology.
- In bilingual scientific/math contexts, naturally use familiar terms such as limit, increasing, decreasing, maximum/minimum when this improves student comprehension; never read raw LaTeX/symbol syntax aloud.
- Visually organize equations and key results so the student can scan the solution.
- For exercises, use Given -> Required -> Formula/Property -> step-by-step reasoning/substitution -> units/check -> Final Answer, but make it read naturally rather than like a rigid form.
- For geometry/science, connect the explanation explicitly to the diagram and labels.
- For a wrong answer, diagnose the likely misconception, explain the specific mistake kindly, then reteach with a different route and a short check question.
- “Explain another way” MUST use a genuinely different representation (example, analogy, visual, simpler decomposition, or alternate valid method), not a paraphrase.
- End a full lesson with a compact synthesis that helps retention, followed by exactly 5 well-chosen additional exercises with full solutions and appropriate visuals as already required.
- Never sacrifice correctness for friendliness; never invent data, labels, source claims, or mathematical points.

Acceptance criterion: a technically correct answer that is confusing, overly verbose, robotic, poorly structured, or not suitable for the selected student grade is a PEDAGOGICAL FAIL.

Use this signature both when fixing prompts/backend behavior and when running PHASE-PEDAGOGY acceptance tests.
