# NABIL — Lessons-learned registry (cumulative defects → permanent rules)

Every defect the user or a test finds is recorded here once, with a rule that EVERY future lesson and the factory
quality gate must satisfy. Add new rows; never delete. Status: FIXED-TEST (fixed in a test copy / engine, not yet
confirmed on production), CONFIRMED (user confirmed on device), OPEN.

| ID | Defect found (date) | Permanent rule | Check | Status |
|---|---|---|---|---|
| LL-01 | Phone: no sound at all; engine skipped speech when the browser listed no matching voice (2026-10-18) | Always attempt to speak with `utterance.lang`; never bail out because `getVoices()` has no match; give a visible "test sound" button with diagnostics | stub with zero voices must still receive utterances | CONFIRMED (user heard sound on phone) |
| LL-02 | Arabic + Latin in one utterance read with the wrong voice | Split speech by language run: Arabic chunk → ar, Latin → en/fr, one utterance each | no utterance mixes scripts | FIXED-TEST |
| LL-03 | Point names/acronyms (A, ABC, SAS), °, ∠, =, ×, ÷ read wrongly or not at all | Spell capital runs; map symbols to words in the speech language | no raw `[A-Z]{2,4}` / symbols in speech text | FIXED-TEST |
| LL-04 | Formula steps silent in some lessons (EN-007) | Every formula step has a spoken rendering | formula steps without speech = 0 | FIXED-TEST (engine), OPEN (EN-007 copy) |
| LL-05 | One drawing shown for four definitions (median only) (2026-10-18) | Each definition/property gets its OWN drawing, drawn BEFORE its text, one board image per concept | scene with N definitions has ≥N draw steps | FIXED-TEST (EN-004 scene 3) |
| LL-06 | Definition written only in Arabic with the foreign term inline | Every definition written twice, separately: foreign language (LTR, left) AND Arabic (RTL, right) so the student copies both to the notebook; no mixed lines | each definition has a foreign + an Arabic step | FIXED-TEST (EN-004 scene 3) |
| LL-07 | Figure had no properties | Mark properties with textbook conventions + a colour per group: equal segments = same number of ticks, equal angles = same number of arcs, right angle = square, parallel = arrow heads | figure with given equalities carries marks | FIXED-TEST (engine + solver schema) |
| LL-08 | Voice button said "voice unavailable" while voice worked | Status label must reflect reality; never show a warning when speech runs | label check | FIXED-TEST |
| LL-09 | Exercise board: base figure missing / wrong order | Order: question → figure → givens → steps; base figure always drawn first | step order test | FIXED-TEST |
| LL-10 | Risk of presenting a stored/mock solution as AI success | Never report stored solutions as AI output; label the provenance | provenance flag | RULE |
| LL-12 | Text said "equal sides / equal angles" but nothing was marked on the figure (2026-10-19) | Whenever the narration states a property (equal segments, equal angles, right angle, parallel), the SAME step shows it on the figure: the hand points to the element, then draws the mark (ticks / arcs / square / arrows) in the group colour, while the sentence is spoken | each property sentence has an `annotate` step with speech | FIXED-TEST (EN-004 scenes 10, 30, 32, 39; generic `annotate` in test copy) |
| LL-13 | Book figure shown as an image but never completed (AK, AL never drawn); exercise 12 had no figure | If the solution needs a line/mark the book figure lacks, overlay it ON the book image (new colour, animated); if the exercise has no figure, draw one from the data | solution mentions a segment/angle not drawn → fail | FIXED-TEST (scenes 30, 32, 39) |
| LL-14 | Arabic sentences with letters/∠/° scrambled (bidi): "A∠ ,PM AB =" | Latin/maths runs are isolated LTR; Arabic prefix letters (و) split from the run; Arabic comma stays outside the run | render check on sentences with ∠ and ، | FIXED (repo engine + test copy) |
| LL-15 | Overlapping figure labels (property text on a side; two captions on top of each other) | Property captions go below the figure, never on its sides; one caption per figure | visual check | FIXED-TEST |
| LL-16 | User (2026-10-19): the Exercise-14 method (hand points, marks drawn on/over the figure, missing lines completed, per-step narration) is THE standard for every exercise, lesson, subject | One shared `annotate` action in the engine + `figure_step` marks in the solver schema/prompt + `annotation_gate` (fail-closed on property statements with no figure) | `scripts/test_annotation_gate.py`; gate report per lesson | IMPLEMENTED in engine/solver/gate (repo); existing Drive lessons NOT yet regenerated (gate report: most G07 lessons FAIL/UNVERIFIED) |
| LL-11 | Drive lessons come from ≥3 engine generations, provenance unknown | Factory must stamp every lesson with generator version + source commit | stamp present | OPEN |

Pending from the user's 17-point spec (not yet implemented): teacher's book + French edition for solutions,
reuse existing Golden lessons before generating, CRDP verification of the teacher plan, terminology glossary.
