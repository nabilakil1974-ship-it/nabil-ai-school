# NABIL AI — README for Claude: Golden Lesson System Requirements 1–6

**Repository:** `nabilakil1974-ship-it/nabil-ai-school`  
**Purpose of this file:** This is the authoritative handoff for Claude. Do not redesign the goal, weaken the gates, or replace the Golden system with generic lesson generation. Read the current code before changing anything and preserve working behavior.

## URGENT CURRENT TASK — 2026-10-04

The immediate blocker is **not Drive synchronization**. Stop spending time on cron/sync until the already-present catalogue entries can actually appear in NABIL.

Observed live fact: **even Golden lessons already present in `data/NABIL_GOLDEN_CATALOGUE.json` do not appear in NABIL's lesson selector.** Therefore trace and repair the complete runtime path first:

`data/NABIL_GOLDEN_CATALOGUE.json -> app/services/golden_registry.py -> app/services/golden_catalogue.py -> registered router in app/main.py -> /api/chat/curriculum/lessons and/or /api/curriculum/lessons -> app/static/curriculum_strict.js -> NABIL lesson dropdown`

Required action for Claude:

1. Inspect the current deployed code and determine the exact break in that path. Do not guess.
2. Verify `golden_registry.rows()` actually returns the catalogue rows at runtime.
3. Verify `golden_catalogue.build_router()` is registered under the prefix expected by the browser.
4. Hit the real Railway catalogue endpoint and record HTTP status + JSON/body.
5. Inspect `curriculum_strict.js` request URLs, query parameters, canonical-source check and `golden=true` filtering.
6. Fix any route-prefix, response-schema, field, filtering, grade/subject/language/branch normalization, startup/import, static-JS or deployment mismatch that prevents the existing rows from displaying.
7. Do **not** add a fake/static fallback list. The UI must display only canonical catalogue rows.
8. After the fix, deploy and test Mathematics on Railway: select grade + subject + language and prove the existing Golden lesson names appear.
9. Launch one existing lesson and verify the same `lesson_id` flows into the Golden classroom.
10. Only after this live path works should catalogue synchronization from Drive be revisited.

Acceptance condition for this urgent task: **an entry already present in `data/NABIL_GOLDEN_CATALOGUE.json` must visibly appear in NABIL on Railway and launch through the canonical Golden path.** A passing CI/build alone is not acceptance.

---

## 0. Product goal

NABIL AI must behave like a complete intelligent Lebanese-curriculum teacher, not like a PDF viewer, text chatbot, or generic AI lesson generator.

The intended path is:

`Google Drive textbook/source -> verified lesson identity -> Evidence Map -> complete prepared Golden lesson -> reference teaching cards -> NABIL teaches sequentially -> student can interrupt -> NABIL answers and resumes at the exact place -> verified concept/solution labs -> assessment/practice -> Golden Final Card -> whole-lesson Smart Lab.`

Scientific fidelity and source fidelity are mandatory. Visual richness is also mandatory, but animation must never invent science that is absent from the lesson/source.

The Golden content on Google Drive is the prepared educational source. The runtime must never silently substitute another lesson, a generic lesson, a guessed lesson, or a fake local list.

---

# REQUIREMENT 1 — Exact Golden lesson selection

NABIL must select the exact prepared Golden lesson using its stable identity, including as applicable:

- `lesson_id`
- grade
- subject
- language
- Grade 12 branch (`GS`, `LS`, `SE`, `LH`, etc.)
- package/version identity

The catalogue must return only real published Golden lessons. A student choosing mathematics must never receive physics/chemistry content; a branch must never leak into another branch; language must match.

### Required behavior

- Canonical Golden catalogue only.
- Stable `lesson_id` is the primary identity.
- Grade/subject/language/branch are validation dimensions, not fuzzy hints.
- No title-only selection.
- No fabricated lesson options.

### Current code/status

The canonical catalogue is implemented in `app/services/golden_catalogue.py` and registered normally by `app/main.py`. `curriculum_strict.js` accepts only responses whose source is `canonical_golden_registry` and only rows marked `golden=true`.

**CODE STATUS: GREEN.**

**LIVE STATUS ON RAILWAY (2026-10-04): RED/BLOCKED.** The live screenshot shows the lesson dropdown message:

`تعذر تحميل فهرس Golden الحقيقي — لم نستخدم قائمة وهمية`

So the deployed UI currently cannot load the Golden lesson catalogue. This must be fixed before claiming end-to-end success. Do not solve this by restoring a fake/static lesson list. The catalogue must remain canonical.

Important architectural direction: the student-facing lesson list should not become unavailable merely because Google Drive/OAuth is temporarily unavailable at page-open time. Prefer a published/cached canonical Golden catalogue produced during sync/build, with Drive as the synchronization source, while preserving exact provenance and fail-closed identity rules.

---

# REQUIREMENT 2 — No fallback to another lesson

Once a `lesson_id` is selected, it is immutable for that lesson session.

### Required behavior

If any of these disagree with the selected Golden package:

- lesson ID
- grade
- subject
- language
- branch

NABIL must fail closed with a clear mismatch/not-ready result. It must **never** choose a nearby title, another lesson, another grade, another language, or generic AI output.

No fallback means no educational substitution. A temporary infrastructure failure is preferable to teaching the wrong lesson.

### Current code/status

Golden resolve/catalogue logic validates the selected identity and rejects mismatches. The newer classroom/lab loaders are also intended to remain locked to the same lesson identity.

**CODE STATUS: GREEN.**

Live end-to-end validation is still blocked by Requirement 1 catalogue loading failure.

---

# REQUIREMENT 3 — Reference teaching cards, not generic cards or raw text

The lesson must not be displayed as a raw PDF, raw extracted text, one giant paragraph, or generic `Hook/Discover/Explain` cards unrelated to the approved references.

The approved reference-card visual language is the target for **desktop and mobile**. Mobile is the same educational design responsively rearranged, not a different impoverished design.

### Required teaching-card structure

The exact number depends on the lesson, but the lesson pipeline must be able to represent:

- prerequisite / recall
- engaging entry
- concept/discovery
- explanation
- definition/rule/theorem/formula
- visual/diagram card
- worked example
- solution card
- Apply & Check / checkpoint
- practice
- assessment
- concept lab when scientifically appropriate
- solution/exercise lab when scientifically appropriate
- Golden Final Card
- whole-lesson Smart Lab

### Text layout requirement

Writing must be readable like a well-written teacher explanation:

- headings visually separated
- paragraphs separated
- one idea does not run into the next
- adequate line-height and spacing
- mathematical notation remains readable
- no horizontal overflow
- desktop and phone both readable

### Golden Final Card

The final card is not a token summary. It must visually synthesize the lesson: key concepts, rules/formulas/relationships, important visual cues/diagram where appropriate, memory cue, and lesson takeaway in the approved reference style.

### Current code/status

The reference classroom renderer and reference styling have been added and the old generic-only behavior has been superseded for the Golden path. Text-spacing/responsive work was also added.

**CODE STATUS: GREEN by static code review.**

**LIVE STATUS: NOT YET PROVEN**, because no lesson currently loads from the deployed catalogue.

---

# REQUIREMENT 4 — Complete lesson teaching sequence

NABIL must teach the **whole prepared lesson**, not show a textbook page and not stop after a short explanation.

### Required sequence

For a complete lesson, use the source-supported elements that exist for that lesson:

`prerequisites -> introduction/question -> concept 1 -> explanation/visual -> rule or theorem -> worked example -> check -> next concept(s) -> textbook/application exercises -> verified solutions -> practice -> assessment -> synthesis -> Golden Final Card -> whole-lesson Smart Lab`

Each concept and exercise/solution may have its own verified lab when pedagogically/scientifically meaningful.

Do not pad a lesson with invented sections just to satisfy a template. Completeness means all source-supported lesson content is taught; it does not mean inventing content absent from the source.

### Current code/status

The Golden/reference renderer can organize the complete prepared content and guarantee the final synthesis card. The factory contract also contains concept/solution/whole-lesson stages.

**CODE STATUS: GREEN by static code review.**

**LIVE STATUS: NOT YET PROVEN**, blocked by catalogue loading.

---

# REQUIREMENT 5 — Scientific, source-locked, spectacular reference labs

This requirement is intentionally strict. NABIL's lab must be visually impressive **and** scientifically honest.

## 5A. Never leave the lesson/source

A lab must be generated from the verified Evidence Map/source text/verified figure for the exact lesson/concept/solution.

Forbidden:

- invented formula
- invented numeric value
- invented scientific relationship
- invented geometry property
- invented physical/chemical behavior
- invented state transition
- a generic sine-wave animation used as a fake lab
- a lab from another lesson
- a rich simulation when the source only supports a static observation/reveal

If evidence is insufficient, fail closed or use an honest `EVIDENCE_REVEAL`; never pretend that an unsupported experiment is verified.

## 5B. Multi-lab structure

The lab identity must support more than one lab per lesson, conceptually:

`lesson_id + lab_id + language + engine_version`

and should identify whether the lab belongs to:

- a concept (`concept_id`)
- an exercise/solution (`solution_id` / exercise key)
- the whole lesson (`master_lab` / `lesson:whole`)

## 5C. Prebuilt verified runtime

AI should not improvise the scientific simulation live in front of the student. The factory should build it once, validate it, independently review it, quality-gate it, publish the verified HTML/artifact, and the student runtime should load that artifact with zero-AI scientific improvisation.

The runtime must verify provenance/artifact identity and fail closed with `PUBLISHED_LAB_NOT_READY` (or equivalent) when the exact lab is unavailable. No fallback to a different lab.

## 5D. Reference visual choreography

Every lab is rendered in the approved NABIL reference visual language, including where meaningful:

- dark/reference stage
- approved cyan/focus visual language
- NABIL teacher presence
- moving teacher pointer/arrow
- target glow/highlight
- animated transition/state change when the science actually contains change/process
- synchronized explanation
- conclusion
- responsive desktop/mobile presentation
- preserve scientifically meaningful colors

The pedagogical choreography is:

`NABIL points -> target highlights -> state/reveal/animation occurs when evidence permits -> NABIL explains/observes -> NABIL concludes.`

A static concept must not be given fake physical motion merely for decoration. It can still be visually rich through pointer, glow, staged reveal, focus, annotation and narration.

## 5E. Evidence and scientific gates

Each relevant teacher step must be tied to evidence (`evidence_quote` or verified figure evidence), targets, before/after state when applicable, and scientific constraints. Animation must not create a scientific fact.

A final Requirement-5 gate must run before a lab spec can leave the factory/publish path. A lab that does not pass must not be published.

### Current code/status

Implemented components include:

- `scripts/nabil_interactive_lab.py`
- `app/api/routes_smart_labs.py`
- `scripts/nabil_requirement5_gate.py`
- Requirement-5 integration in `scripts/nabil_lesson_factory.py`
- published/verified lab loading for the Golden classroom
- reference renderer wrapper with teacher pointer/highlight/animation choreography
- concept/exercise/solution/whole-lesson lab publishing architecture

The Requirement-5 workflow produced the factory integration commit `99aa3af7167be4d819dd44cdf148a92e1718231e` (`Requirement 5: enforce source-locked scientific visual lab gate`).

**CODE STATUS: GREEN by static code review.**

**LIVE STATUS: NOT YET PROVEN.** Existing previously-published lab artifacts must not automatically be assumed to have been regenerated with the newest renderer/gate. After catalogue recovery, test a newly generated/published mathematics lesson and inspect the actual rendered labs.

---

# REQUIREMENT 6 — Interactive NABIL teaching: interrupt, answer, resume exactly

NABIL must behave like a teacher, not a slideshow.

### Required behavior

During automatic teaching:

1. NABIL is explaining a specific card and line/step.
2. Student asks a question.
3. Teaching pauses immediately.
4. Exact lesson/card/line position is saved.
5. Question is sent through the real `/api/chat` contract using the exact current lesson context.
6. NABIL answers the question.
7. NABIL may speak the answer.
8. The lesson returns to the **same card and same line/step**.
9. Teaching continues from there; it does not restart the lesson and does not skip ahead.

The interruption must preserve the same `lesson_id`. No fallback.

The real chat contract uses `FormData` fields such as:

- `student_id`
- `grade`
- `subject`
- `lesson`
- `language`
- `message`

and the current lesson context may be supplied for the interruption.

### Current code/status

The classroom runtime has position state (`card index` / `line index`), pause/resume behavior, and the interrupt bridge was corrected to use the real FormData chat contract rather than the earlier incorrect JSON request.

**CODE STATUS: GREEN by static code review.**

**LIVE STATUS: NOT YET PROVEN**, because a lesson cannot currently be selected from the deployed catalogue.

---

# Current truth table — 2026-10-04

| # | Requirement | Code | Live Railway |
|---|---|---|---|
| 1 | Exact canonical Golden lesson selection | GREEN | RED — catalogue fails to load |
| 2 | No fallback / exact lesson identity | GREEN | BLOCKED by #1 |
| 3 | Reference cards + readable desktop/mobile layout | GREEN | BLOCKED by #1 |
| 4 | Complete lesson sequence + Golden Final Card | GREEN | BLOCKED by #1 |
| 5 | Source-locked verified spectacular reference labs | GREEN | BLOCKED / not yet visually proven |
| 6 | Interrupt -> answer -> exact resume | GREEN | BLOCKED / not yet live-proven |

**Do not report 6/6 live green.** Static code review and deployed end-to-end behavior are separate acceptance layers.

---

# Immediate problem Claude should investigate first

The deployed Railway UI currently displays:

`تعذر تحميل فهرس Golden الحقيقي — لم نستخدم قائمة وهمية`

`app/static/curriculum_strict.js` attempts the canonical catalogue endpoints and intentionally refuses non-canonical/fake data. The live diagnostic indicates the Golden launcher exists, yet lesson-list loading fails.

Claude should trace the deployed request end-to-end:

`browser curriculum_strict.js -> /api/chat/curriculum/lessons or /api/curriculum/lessons -> golden_catalogue router -> catalogue source/cache/Drive -> canonical JSON response`

Determine the exact HTTP status/exception on Railway. Fix the root cause without weakening canonical validation and without introducing a fake fallback list.

A robust target architecture is:

`Drive/prepared Golden lessons -> synchronization/build step -> canonical published catalogue/cache with provenance -> Railway student read endpoint`

so that temporary Drive/OAuth unavailability at page-open time does not erase the lesson dropdown.

After fixing the catalogue, perform the acceptance test with **Mathematics**, not only Physics:

1. Select grade + Mathematics + English (+ branch where required).
2. Confirm real Golden lessons appear.
3. Launch one real mathematics Golden lesson.
4. Confirm reference cards and readable separated text on desktop.
5. Confirm the same responsive design on mobile.
6. Let NABIL teach through several cards.
7. Interrupt with a question and verify exact-position resume.
8. Open concept/solution lab(s): verify pointer, glow, meaningful animation/reveal, narration, source fidelity and scientific/mathematical fidelity.
9. Reach assessment and Golden Final Card.
10. Open whole-lesson Smart Lab.
11. Confirm no wrong lesson, no generic fallback, no invented science/mathematics, and no impoverished static lab.

---

# Non-negotiable engineering rules for Claude

- Inspect current code before editing; do not replace working systems with stubs.
- No mock pipeline presented as production.
- No fake success status.
- No silent fallback.
- No weakening scientific review to make a test pass.
- No lesson content invented outside verified source evidence.
- No lab motion that implies unsupported science/mathematics.
- Do not manually repair hundreds of lessons when the factory/pipeline can be fixed generally.
- Preserve the canonical Golden architecture and stable lesson IDs.
- Preserve desktop and mobile behavior.
- Keep visual excellence and scientific fidelity together.
- A code-level GREEN is not a live GREEN until Railway is tested end-to-end.

## Definition of Done

NABIL is done only when a student can choose a real Golden mathematics lesson on the deployed platform, receive the exact prepared lesson, see the approved reference cards, hear/see NABIL teach it sequentially, interrupt and resume exactly, interact with evidence-locked reference-quality labs, complete practice/assessment, receive the Golden Final Card and whole-lesson Smart Lab — on desktop and mobile — without fallback, invented content, or dependency on a fake lesson list.
