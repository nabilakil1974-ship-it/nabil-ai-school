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


## IMMEDIATE OWNER TEST — Grade 9 Mathematics textbook-grounded lesson

After the latest Railway build/deploy for commit `9c3fac70cdcde99b086c7574e8a7567ecb330697` is live, run this test before broader pedagogy testing:

1. Select **Grade 9 → Mathematics → English**.
2. Confirm the lesson selector contains only the 15 newly approved Grade 9 Mathematics textbook TOC entries.
3. Select the **first lesson: “Lines and circles”** and run **Full Lesson / Start Lesson**.
4. This is a SOURCE-GROUNDING acceptance test: the explanation must follow the actual Grade 9 textbook content for that lesson. It must NOT invent a generic lesson merely from the title, and it must NOT import concepts from other grades/chapters.
5. Compare the generated explanation against the Grade 9 Mathematics book in the owner's connected Google Drive (**Building up Mathematics Grade 9.pdf**). Check the concepts, properties/theorems, terminology, examples, order/scope, and diagrams that the book actually supports.
6. Separately judge teaching quality: it should explain the book content in NABIL/ChatGPT student-facing style rather than copy or dump textbook prose.
7. Report **PASS/FAIL** for (a) selector list, (b) textbook grounding/content fidelity, (c) mathematical correctness, (d) pedagogy, and (e) visuals. Include concrete evidence for any mismatch.
8. If the live build is not yet deployed, wait for deployment/readiness and then test; do not test an older build and call it current.

Owner requirement: **the book is the source of lesson content; the model may explain that content pedagogically, but may not fabricate the lesson scope from the title.**


## IMMEDIATE — Cloud textbook RAG completion

Owner approved the architecture: Google Drive remains the private source library; Railway/PostgreSQL stores the searchable textbook index; students need no Drive access and no local computer.

Commit `351ff2a443de6131333a86e083f70d674c4d1e56` wires lesson chat to `search_book_pages()` and injects retrieved book passages into the lesson prompt with strict source-grounding rules.

Complete and test the ingestion side now:
- Start with Grade 9 Mathematics English, Drive file id `1Em9-vpBX8clwSv8_fMk3zPsgSx8Psyw_`, title `Building up Mathematics Grade 9.pdf`.
- The PDF is scan-heavy; plain PyMuPDF extraction may return empty pages. Add a cloud/server OCR fallback for pages with no usable text rather than silently skipping them. Do not fabricate OCR text.
- Persist page text/chunks + page identity in PostgreSQL/pgvector. Drive is the source; do not require the owner's computer.
- Ensure retrieval is constrained by grade + subject + language/book identity so English and French books cannot mix. Do not rely on a curriculum-label mismatch that can return zero results.
- Add lesson-to-page/chapter boundaries when discoverable so selecting “Lines and circles” retrieves that chapter first, not arbitrary semantically similar pages elsewhere in the book.
- Never expose Drive credentials/service-account secrets to the browser.
- After deployment/indexing, run the owner test: Grade 9 → Mathematics → English → Lines and circles → Full Lesson. Verify the generated content is grounded in retrieved textbook passages and cite the book/page internally/visibly as appropriate. A generic model-generated lesson from the title is FAIL.
- Record ingestion counts (pages with text, OCR pages, chunks), retrieval evidence, and PASS/FAIL in the pedagogy report. Then reread this mailbox.


## IMMEDIATE OWNER TEST — French Mathematics selector parity after TOC replacement (2026-09-18)

Latest math curriculum commits:
- `0e3efcd103fb4a9cae623fe7d9519e277c3cda2e` — replace master Mathematics with verified French textbook TOCs.
- `32826fbb5d1afdf9999c20622ea3c08721b2f0d8` — remove legacy Arabic/English Mathematics lists and keep verified French TOCs.
- `2a40f36eaa4787b135ac81df34b3201909761e87` — cache-bust strict curriculum UI.

### OPEN — Run immediately after the latest Railway build is live
Verify the LIVE platform, not repository JSON only.

1. For Mathematics, select Français and check every grade from Grade 1 through Grade 9, then S1/first secondary.
2. Verify the lesson selector contains exactly the same French lesson titles, order, and count as the corresponding verified TOC now stored in `app/static/crdp_master_curriculum_index.json`.
3. Verify no old Arabic/English Mathematics lesson list leaks into Français and no lesson from another grade appears.
4. For S2, test both branches separately: Sciences = 29 lessons; Humanities = 20 lessons.
5. For S3, test all four branches separately: General Sciences = 24; Life Sciences = 26; Sociology & Economics = 23; Literature & Humanities = 10.
6. Verify branch changes refresh the Mathematics lesson selector to the correct branch-specific list without stale lessons.
7. Report PASS/FAIL per grade/branch, with actual count vs expected count and at least first/last title. Any mismatch must include reproduction steps and screenshot/evidence.
8. Save the report as `audit/work-reports/MATH-FRENCH-TOC-PARITY-REPORT.md` and reread this mailbox.

Expected counts: G1 60, G2 74, G3 62, G4 35, G5 32, G6 27, G7 17, G8 23, G9 15, S1 27, S2 Sciences 29, S2 Humanities 20, S3 GS 24, S3 SV 26, S3 SE 23, S3 LH 10.


## SCIENCE CLOUD TEXTBOOK PIPELINE + PEDAGOGY QA — 2026-09-18

Programmer implementation is now on main for Chemistry, Physics, and Biology/Life Science.

Please verify after Railway deploy:
1. Existing web service still starts normally.
2. PyMuPDF imports successfully and Tesseract OCR is available.
3. Run/observe science indexing in this strict order: chemistry -> physics -> biology.
4. Confirm scanned textbook pages no longer get silently skipped when direct PDF text is empty.
5. Confirm RAG isolation by grade + subject + curriculum/language, including shared Grade 12 source PDFs mapped to more than one branch.
6. Live pedagogical QA:
   - Chemistry: textbook-grounded explanation + equation/charge/balance checks + image/PDF exercise reconstruction.
   - Physics: textbook-grounded explanation + Given/Required/Law/SI units + circuits/rays/forces/graphs reconstruction.
   - Biology: textbook-grounded explanation + Observation/Interpretation/Conclusion + scientific-document/diagram reconstruction.
7. For multi-part image exercises, verify ORIGINAL -> per-part additions -> FINAL and ensure the initial drawing never reveals a result the student is asked to prove/label.
8. Save report: audit/work-reports/SCIENCE-RAG-PEDAGOGY-QA.md

Do not report success from repository inspection alone; verify the live Railway deployment and actual retrieval behavior.


### Science selector builds completed — programmer handoff
- Chemistry selector build commit: 5f78b106c8a36d0167924a55ce3f881d9ff3e545
- Physics selector build commit: ce14ade345d98e3e7c7704e9eaca38e7cd8fe8a5
- Life Science selector build commit: 680dc9234457aaaaa1fed71207759eeb312dca6d
- Extensible extra-book manifest support: 40c3f5101eb429a439b19c09ec61df56c99ada8e

Verify LIVE after the latest Railway deployment:
- Grade/branch -> Chemistry/Physics/Life Science -> English returns these verified textbook titles in exact order.
- No invented fallback titles when a language/book is absent.
- Existing French data must not be overwritten by English.
- Report exact mismatches and selector routing defects.


## OWNER PRIORITY — Voice + real age-adaptive learning path + exposed JS (2026-09-19)
Programmer handoff from the user's live Railway screenshots:
- The browser displays enormous raw JavaScript source BELOW the lesson board. This is a major, independently visible frontend defect, NOT a stylistic issue. Investigate the legacy `app/static/chat.html` (5.7 MB), especially malformed inline <script> boundaries and source leaked into visible DOM; restore a clean mobile and desktop lesson view. Preserve the chat and assessment features. Do not mark fixed without browser QA.
- Owner wants natural spoken AND typed Lebanese Arabic, including mixed English/French scientific terminology, interpreted as the same actual student question and routed to the same lesson/solution engine; meaningful short spoken replies, no dry lecture. No fabricated source.
- Voice transcription stub was replaced on main with server-side OpenAI (or Groq fallback) transcription, commit `39703bc4aff314fc9fe1a781e2cfe115f279fa7f`; confirm in production that actual microphone audio reaches /api/chat, correct `audio` multipart upload and transcript, and receives an answer. The separate oral tutor must retain context and never expose transcript or raw JS.
- Age-appropriate learning-action prompt and colloquial voice instructions updated in `fb4be10d0c96877e5ab5facb6b9ae4161e0a030b`. Check the EXISTING UI `مسار التعلم الذكي` actions truly submit learning_action values via the request, create meaningful lesson-specific actions, display the outcome, accept the learner's answer and update profile. Buttons alone are FAIL. Adapt grade 1–3 vs grades 4–6 vs 7–9 vs secondary.
- Earlier progressive drawing contract commit `eca5637f973111a12f643f050a686dc340ab2d50` is prompt-level and NOT an image-overlay renderer. Verify uploaded exercise original is preserved, and five solved practice exercises have validated, correctly assigned visual payloads for stages. No fake redrawing, no unsupported image overlays.
- Watch Railway deploy state and do NOT assert auto-deploy success from GitHub commit alone. Owner had chemistry indexing running in the production console; account for deploy interrupt/resume and avoid running simultaneous index jobs.
Save evidence and a PASS/FAIL report for browser, typed Lebanese, recorded voice, adaptive learning actions and diagram fidelity. Report source gaps clearly.

### Voice follow-up (main commits 75d0582, 0e4effd, 4ced41e)
The gateway speech interface now loads `/static/nabil_voice_v133.js` at the end of `app/main.py`, using MediaRecorder and server-side transcription, rather than the disabled v114 or browser SpeechRecognition v118. The /api/chat audio and text paths must keep the SAME subject-independent gateway reasoning mode and conversation context. Validate a Lebanese spoken request mixing e.g. «Study f(x) ln x over x شو الـ derivative؟», French and English questions; confirm the true transcript is shown and correct student-facing terminology, not a silent browser auto-rewrite. Ensure legacy v118 controls do not double-send. Check live after actual Railway deployment and report.