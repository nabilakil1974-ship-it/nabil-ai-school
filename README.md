NABIL AI — MASTER CURRICULUM LINKED

Replace exactly:
1) app/static/chat.html
2) app/static/teacher_assessment.html
3) app/api/routes_chat.py
4) app/static/crdp_master_curriculum_index.json

What changed:
- Lesson page loads crdp_master_curriculum_index.json first.
- Teacher assessment uses the same master index.
- Secondary branch keys are mapped to the combined master grade keys.
- Secondary languages are excluded in the current phase.
- Kindergarten is excluded in the current phase.
- Sociology/economics/history/geography/philosophy are excluded from the current UI scope.
- Assessment rejects lesson titles that are not in the current verified catalog.
- Backend lesson grounding resolves the master catalog before legacy fallback.
- Legacy scientific index remains only an emergency fallback for scopes not present in master.


---

# NABIL AI — V18 GOLDEN FACTORY MASTER SPECIFICATION
**Living engineering and pedagogical contract | 2026-10-10 | Branch: v18**

> **Purpose:** This is the source of truth for requirements, architecture, evidence, teaching, question bank, translation, interactive labs, Golden Cards, cost controls, recovery and actual acceptance. Future Claude/ChatGPT sessions and code contributors must read this section **before changing production**.
>
> **Status discipline:** "implemented" means code observed, not end-to-end accepted; **Golden / Published** means real-book evidence, scientific acceptance, real Drive write/readback, and actual UI review. A passing Docker build alone does not establish lesson acceptance.

## 0. Non-negotiable contract / العقد الأساسي

- The Lebanese curriculum from kindergarten through Grade 12 (including the correct S3 tracks) is the **long-term scope**, with correct grade, subject, language, official branch and actual source-book identity. Do not relabel one grade/branch as another. Current master-index/UI exclusions mentioned in the legacy README are *current implementation restrictions*, not the educational end goal.
- **Real source only.** Index books and identify their actual lessons before generating content. Do not invent a title, page, example, problem, figure, source citation or lab.
- **No fake success**: a fixture, mock, placeholder simulation, snapshot of textbook pages, locally generated HTML, or a Docker test is NOT a published Golden lesson.
- Preserve separately audited gates: source identity and boundaries, page/text/visual evidence, reviewer independence, mathematical/scientific verification, coverage and completeness, language integrity and publication verification.
- **Fail closed where critical** (e.g. wrong source, missing independent reviewer, ungrounded scientific claim); **isolate and defer an individual recoverable exercise/translation error** when policy allows without falsely saying the full lesson is complete.
- Protect working code, existing approved source evidence, paid checkpoints, Google Drive books and ledgers. Never purge the original PDFs or checkpoint records to clean a pilot output folder.
- Development must be **modular and limited to the affected file**. Do not edit the already agreed V18 renderer, cards and labs merely to fix pipeline failures; use contract tests and adapters, with explicit review before changing these components.
- Three classroom languages: **English, Arabic, French**; UI labels alone are not scientific translations. Verified lesson AND exercise content, labels, spoken script, drawing labels and final cards must follow chosen language. The original language is the explicit fallback when a verified translation is unavailable, never silently masquerade as another language.

## 1. Source → catalogue → lesson / الكتاب والفهرسة

1. Connect Google Drive using minimally scoped access; discover actual Lebanese curriculum PDF books. Preserve Drive IDs, source URLs, language, grade, subject, branch, version and PDF-page versus printed-page mapping.
2. Read the book itself: TOC, chapter/lesson headers, actual concept ranges, activities, examples, figures, summary and exercises. Visually inspect figures/tables/diagrams when understanding depends on the image, not OCR alone.
3. Create/reuse a **verified catalogue**: one stable \`lesson_id\` per true lesson, source \`book_id\`, exact page ranges, content units, exercises and source metadata. Reject mismatches rather than selecting a similar book by title.
4. Divide a book into individual lessons, lessons into ordered **concepts C01…Cn**, and each concept into concise teaching ideas / verified activities. Inventory every textbook exercise, number, figure and page; preserve unsolved/pending items in a coverage backlog.
5. Reuse verified page evidence and checkpoint artefacts on restarts instead of downloading/re-extracting or paying to infer everything again.
6. A sample acceptance source, **not a global hard-coded scope**: *Building up Mathematics Grade 7.pdf*, Drive PDF ID \`1E-nj01QlpvZCa_kHy92qQDlm6ko1ba_D\`; example lesson \`G07-MATHEMATICS-69B7C840-001\` = **Powers**. Actual pages and numerical exercises must always be checked against the PDF.

## 2. Golden lesson pedagogy / كيف يشرح الأستاذ نبيل

For **every concept**, show *one idea at a time* in a paced, pedagogical classroom sequence:

1. **Prepare / hook:** an accessible question, observation or prerequisite based on the source; connect with what students know.
2. **See:** show the actual verified figure, mathematically accurate drawing, text, diagram or real situation **next to the idea it explains**. A missing visual is shown as unavailable, not fabricated.
3. **Understand:** the teacher explains WHY as well as HOW; avoid merely pasting book pages. Use short progressive sentences, an appropriate example and precise mathematical/scientific notation.
4. **Teacher writes and speaks together:** synchronized board, teacher voice and visible text, controlled pacing, start/stop/previous/next/replay and accessibility controls. Do not declare spoken output if browser audio is unavailable.
5. **Think / predict:** a brief Socratic question before immediately revealing the answer.
6. **Try / experiment:** a **source-grounded interactive lab**, if educationally justified; calculations/manipulations must really respond to student actions.
7. **Check:** short formative verification of the particular idea; do not unlock a correct-answer state prematurely. Preserve per-concept progress.
8. **Next idea:** continue in book order while maintaining clear learning progression.
9. **Conclude:** only at the end reveal a real **Golden Reference Card** summarizing the verified rules, figures, examples, and important caveats; include a final understanding check.
10. **Exercise page:** every textbook exercise or problem receives its own identified page/section, original problem and figure, independent step-by-step verified solution, optional interactive lab, controls, speech and end-of-solution Golden Card when applicable. Do not skip exercises silently.

**Display contract:** the reference V18 three-zone Smart Board: results/concepts on the side, explanatory classroom board and interactive visual in the center, teacher assistant/voice on the other side. On phones collapse responsively with no clipped sidebar, horizontal overflow or inaccessible buttons. Preserve the user's chosen reference color palette and cards.

**Mathematics:** render superscripts/fractions/equalities correctly, with calculations evaluated independently. **Physics/chemistry/biology/geometry:** use the correct domain figures, apparatus, circuits, vectors, diagrams or 3D *only when verified and technically supported*. No generic graph standing in for a chemistry atom, or text-only fake lab.

## 3. Exercises, common questions and question bank / بنك الأسئلة الشائعة

- Index by grade, subject, branch, language, book, \`lesson_id\`, concept, exact exercise ID, **printed/PDF page**, provenance and difficulty.
- Keep three non-confused origins: **verbatim textbook questions**, **source-grounded teacher-created formative questions**, and **frequently asked student questions (FAQ)**; tag origin on each record.
- Each question has an approved question statement, verified answer, explicit reasoning steps, prerequisite/concept association, optional verified figure/lab, typical mistake and remediation explanation.
- FAQ includes misunderstandings gathered from actual repeated questions; AI-proposed FAQs must be labeled proposed until editorially verified, not presented as evidence of student demand.
- Differentiate *practice, application, challenge, homework, formative and summative* uses; offer interactive worksheet, hints before solutions, answer checking and student feedback.
- Reject malformed arithmetic and unsupported results, rather than inventing the right answer; keep the question in a backlog for later repair.
- Maintain a **coverage ledger**: expected/extracted/validated/approved/deferred numbers and reason codes. Completing 9/10 exercises must never be called 10/10.

## 4. Real reference labs / المختبر المرجعي

**Reference implementation:** [V18 interactive labs module](scripts/nabil_factory/v18_editable/labs.py) and [renderer interface](scripts/nabil_factory/v18_editable/renderer.py).

- Build an interactive lab **for every verified activity that genuinely calls for an experiment/manipulation**, including exercises where justified. The source evidence defines correct parameters, permitted inputs and outcomes.
- Maintain one-to-one \`concept_id\` / \`exercise_id\` association and a machine-readable lab index. Embed only approved lab HTML/spec. Labs should respond to changes and teach, not just open a textbook image.
- Sequence: premise → initial state → action → visible response/observation → teacher interpretation → verified conclusion → reset.
- Use bounded calculations, real interactions, no unverified externally fetched simulations or hidden paid model calls during student runtime. Screen size and mobile controls matter.
- Textbook source image and activity description must remain available as grounding where necessary. If evidence is absent, display \`UNVERIFIED_LAB_UNAVAILABLE\` and record a backlog task.
- Requirements apply across subjects; e.g. power patterns, geometric constructions, verified function transformations, real electrical circuits or chemical arrangements where source supports them.
- **Never replace an experiment with a decorative “interactive” button.**

## 5. Golden Reference Card / البطاقة المرجعية

**Reference implementation:** [V18 universal cards module](scripts/nabil_factory/v18_editable/cards.py) and its **embedded reference engine**; [V18 board renderer](scripts/nabil_factory/v18_editable/renderer.py).

- Use the already approved visual style and layout; not an unrelated template.
- The Gold Card contains verified concept title, prerequisites/givens, question/goal, ordered scientific or mathematical reasoning, appropriate original/validated diagram or chart, key rule/formula, worked example, quick check and student-facing final takeaway.
- Appropriate visual panels (such as study/diagram/calculation/teacher) must be subject-specific. Scientific diagrams and math are grounded, not cosmetically generated.
- Golden summary is unlocked **after completing verified explanation**; exercise cards after the solution sequence. There must be no premature answer reveal.
- The *same underlying approved facts* feed board, exercise, lab, card and exports. Do not create conflicting versions across views.
- Arabic, English and French versions must preserve all facts, symbolic math and units.

> **Reference links policy:** These two repository modules and the renderer are **verified existing links**. The exact original design screenshots/Claude external attachment URLs are **not yet revalidated in this repository**: add their permanent URLs only after verifying them, never invent a link.

## 6. Evidence and independent scientific review / المراجع المستقل

- Source identity **before** generation, including exact Drive PDF ID and grade/branch; evidence map from **text + image of relevant PDF pages**, with figure description and page ID.
- Three independent duties where required: content generator, visual/text evidence extractor, scientific reviewer. Enforce genuine model/provider separation for independent review, or fail closed.
- Explicit gates before output/publish: \`SOURCE IDENTITY\`, \`SOURCE EVIDENCE\`, \`SCIENTIFIC REVIEW\`, \`MATH CONTRACT\`, \`CONCEPT COVERAGE\`, \`EXERCISE COVERAGE\`, \`LAB/CARD CONTRACT\`, \`LANGUAGE COVERAGE\`, \`RENDER/UI QA\` and \`DRIVE READBACK\`.
- For equations: validate both sides with deterministic arithmetic/symbolic checks (e.g. exponent rules), not LLM confidence. Missing steps are *unverified*, not automatically equivalent to wrong arithmetic.
- Keep structured, auditable evidence links: file ID, page number (PDF & printed), excerpt, figure identifier, proof/reviewer verdict and rejection rationale. The final prose must never cite an invented source.
- Do not delete rejected material silently; store it as explicit backlog with reason, stage and next action.

## 7. Cost, accuracy, reliability and recovery / كيف خفّفنا الأخطاء والكلفة

**Source-first checkpointing** is core engineering, not an optional optimization.

1. **Reuse** book TOC, extracted figures/page evidence, concept narratives, lab specs, verified solutions and translations from Drive by stable keys and source hashes, only if still valid for current gate/prompt/model versions.
2. **Bounded retry + self-heal:** retry only the rejected **smallest component**, preferably repair format deterministically; use independent source evidence for semantic repair. Record before/after verdicts.
3. **Skip/continue only where safe:** a rejected exercise may be withheld from a provisional lesson while other concepts progress; mark exercise **deferred** and the lesson **coverage incomplete**. Source identity/scientific/publication fatal gates remain blocking.
4. **Provider fallback/cooldown:** OpenRouter/Groq/other configured providers, separate generation/evidence/review responsibilities, respect rate-limit \`Retry-After\`, capped exponential backoff, budget and maximum request count. If providers cool down, checkpoint the job and resume; don't endlessly wait or spin.
5. **Translation budget:** translate stable structured fields in small batches with strict JSON Schema; validate content, math, identifiers and completeness. Cache each successful translation. Never retry all three languages because one French JSON response is malformed.
6. **Prebuild labs/illustrations/exercise answers** before publication; student browsing must not invoke the lesson-production model for every opening.
7. **Restart-safe/idempotent:** keep run state, version and ledger; do not overwrite a verified published lesson with an incomplete attempt.
8. **Performance metrics:** calls, per-provider tokens/estimated cost, cache hit rate, retries, time at each gate, approved/deferred exercise counts, build and source errors.
9. **Stop conditions:** bounded limits and explicit error statuses, never silent runaway cost or fake success.
10. **Restore from existing checkpoints before regeneration** when safe and within provenance/version rules.

**Pilot observations (2026-10-10, Claude branch \`13767ec\`):** actual Grade 7 Powers run restored cached evidence and narratives; logs showed \`MATH_CONTRACT_EXERCISE_UNAPPROVED\`, \`EXERCISE_DROPPED_NOT_LESSON\`, teaching self-heal, invalid translation JSON, rate limits and provider cooldown. This **did not prove** atomic publication. Keep it as a regression case; don't infer that the same code exists in \`v18\`.

## 8. Modular code map / تقسيم المصنع لسهولة الإصلاح

### Current verified paths on \`v18\`

| Responsibility | Existing file / link | Rule |
|---|---|---|
| Minimal CLI entry | [scripts/nabil_lesson_factory.py](scripts/nabil_lesson_factory.py) | Entrypoint stays thin; implementation lives in package |
| Book scan/catalogue and sequential production | [scripts/nabil_book_factory.py](scripts/nabil_book_factory.py) | Source-first, resumable, accurate lesson catalog |
| Production pipeline, evidence/translation/publication orchestration | [scripts/nabil_factory/factory/pipeline.py](scripts/nabil_factory/factory/pipeline.py) | Connect modules; do not bypass gates |
| Safety gate separation | [scripts/nabil_factory/factory/locked_v18_safety.py](scripts/nabil_factory/factory/locked_v18_safety.py) | Do not weaken source/independence boundaries |
| Factory package boundary | [scripts/nabil_factory/factory/__init__.py](scripts/nabil_factory/factory/__init__.py) | Keep orchestrator isolated from UI changes |
| V18 presentation registry | [scripts/nabil_factory/v18_editable/settings.py](scripts/nabil_factory/v18_editable/settings.py) | UI config only, no scientific acceptance flags |
| V18 lesson board | [scripts/nabil_factory/v18_editable/renderer.py](scripts/nabil_factory/v18_editable/renderer.py) | Slow explanation, voice, responsive layout, last Golden |
| Source-based interactive labs | [scripts/nabil_factory/v18_editable/labs.py](scripts/nabil_factory/v18_editable/labs.py) | Concept + exercise, real approved interaction |
| Verified Golden Cards | [scripts/nabil_factory/v18_editable/cards.py](scripts/nabil_factory/v18_editable/cards.py) | Shared visual language, verified scientific source |
| V18 module independence test | [scripts/nabil_factory/v18_editable/test_independence.py](scripts/nabil_factory/v18_editable/test_independence.py) | Prevent safety/UI coupling |
| V18 board contract test | [scripts/test_v18_renderer_contract.py](scripts/test_v18_renderer_contract.py) | Test actual behavior, not retired hooks |
| Live interactive lessons API | [app/api/routes_interactive_lessons.py](app/api/routes_interactive_lessons.py) | Serve published Drive lessons to NABIL |
| Pilot runner | [scripts/run_g07_math.py](scripts/run_g07_math.py) | Grade 7/Powers example, **not** universal workflow |
| Railway deployment config | [railway.toml](railway.toml) | Audit branch/start command before production |
| Docker build gates | [Dockerfile](Dockerfile) | Keep tests enabled; no green claims before complete build |

### Intended logical boundaries

\`\`\`text
Drive book / source
  └── Book discovery & index (book_factory)
        └── Evidence map (OCR + VISUAL, pages, figures, exercises)
              ├── Concepts and pedagogical sequences
              ├── Question & FAQ bank
              ├── Verified exercise solutions
              ├── Audited interactive lab specifications
              └── Structured AR / EN / FR translations
                     ↓
            Independent scientific and math review
                     ↓
       v18_editable presentation (renderer / labs / cards)
                     ↓
       Quality, coverage and atomic publishing gate
                     ↓
           Google Drive write + read-back
                     ↓
       NABIL interactive lesson/exercise platform
\`\`\`

**When an issue is found:** identify which layer owns it; change the **minimal owning file**, add an actual regression test, run checks, then deploy. Don't rewrite a functioning module to repair a different one. The diagram shows logical responsibilities; **it does not claim each responsibility is already a separate Python file**.

## 9. Required artifacts per lesson / مخرجات كل درس

- Stable catalog record (\`book_id\`, \`lesson_id\`, page map and source version).
- Evidence map including original text and verified visuals.
- Interactive lesson page with concept-by-concept explanation and synchronized voice.
- Separate verified exercises and problem solutions page.
- Real exercises/activities lab index, optional verified figures and dynamic components.
- Concept/lesson Golden Cards and worked exercise cards.
- Student worksheet with progressive questions, feedback and answer controls.
- Multilingual coverage proof for Arabic, English and French.
- Where supported by verified pipeline: real editable presentations / PPTX and printable/exportable materials, not a substitute for web lesson.
- QA/review summary, provenance, cost/attempt report and **published Drive IDs/URLs** only after write + readback.

## 10. End-to-end acceptance / كيف نقرر النجاح

1. Actual book indexed, exact lesson chosen by ID and verified against page evidence.
2. Every core concept and exercise is accounted for. Report numerical coverage and deferred items transparently.
3. No unapproved scientific claim or arithmetic mistake in a published section.
4. Boards, labs, questions, cards and exercises use **the same** approved evidence.
5. Check **all three languages** on real content (not merely translated interface labels).
6. Desktop AND real mobile inspection: interactions, voice availability, no clipping; board flow and Golden Card appear at correct time.
7. Every output is published to Drive and verified **by reading it back**, including immutable IDs and useful URLs.
8. The NABIL frontend actually displays the published lesson and exercise pages.
9. Only then report \`ATOMIC_PUBLISHED_AND_VERIFIED_TO_DRIVE\` and acceptance; otherwise \`REJECTED\` with the first actual failure and resumable state.
10. Roll out conservatively: **Powers only first**; then all math lessons/grades in batches, then remaining subjects after proven acceptance, keeping failure budgets and observability.

## 11. Where we are now / الحالة المثبتة، لا الوعود

- **Railway service:** \`v1782-g07-pilot\`; intended active branch \`v18\` (verify directly in Railway for current truth).
- Earlier \`v18\` Docker build failed due to a stale renderer contract assertion referencing retired \`NabilRuntime.TeacherPlaybackController\`. That assertion was replaced by V18-compatible checks in [the test](scripts/test_v18_renderer_contract.py); last follow-up commit for the contract was \`b4a4bfba\`. **Actual final build result must be checked**, not assumed.
- The older Claude refactor is retained separately on \`refactor/lesson-factory-modular-v1\`; it is **not** the source of the \`v18\` build.
- Two pilot-generated Powers HTML pages from 2026-10-10 were intentionally deleted from Drive to avoid mixing test artifacts; original textbook and evidence/checkpoint folders were kept.
- Real Powers V18 end-to-end / published / visually accepted remains **UNVERIFIED / REJECTED** until the explicit acceptance evidence above.
- Before touching any production file, consult this README and latest GitHub commit, Railway build/runtime logs, and Drive artifacts; list exact changes and test results.

## 12. Permanent reference index / روابط الرجوع السريع

- [GitHub — NABIL AI V18 branch](https://github.com/nabilakil1974-ship-it/nabil-ai-school/tree/v18)
- [Factory pipeline](scripts/nabil_factory/factory/pipeline.py)
- [Book → lessons factory](scripts/nabil_book_factory.py)
- [V18 golden teaching board](scripts/nabil_factory/v18_editable/renderer.py)
- [V18 reference interactive lab](scripts/nabil_factory/v18_editable/labs.py)
- [V18 reference scientific cards](scripts/nabil_factory/v18_editable/cards.py)
- [Independent scientific safety boundaries](scripts/nabil_factory/factory/locked_v18_safety.py)
- [Acceptance/test contract](scripts/test_v18_renderer_contract.py)
- [Railway service](https://railway.com/project/500bdcf3-f403-43d6-aea6-c636a0f16094/service/13b23912-b28b-40ce-8a3c-95267dcaaf40)
- [Grade 7 source book on Google Drive](https://drive.google.com/file/d/1E-nj01QlpvZCa_kHy92qQDlm6ko1ba_D/view)
- [Separate Claude refactor (not merged into V18)](https://github.com/nabilakil1974-ship-it/nabil-ai-school/tree/refactor/lesson-factory-modular-v1)

**Documentation maintenance:** Update the *status* section on every accepted milestone with exact commit, proof, dates and Drive links. Never silently rewrite historical evidence. All new requirements must say whether they are **required**, **implemented**, **tested**, or **accepted**.


## 13. Original visual HTML references / روابط النماذج الأصلية (verified on Drive 2026-10-10)

**These are the real HTML reference artifacts, NOT merely Python source-module links.** Preserve these as visual/functional comparison fixtures. A Drive preview may not execute active JavaScript; download or open with an HTML-capable test environment as needed. Their existence does not prove they match the current V18 page or that its scientific content is approved.

| Original artifact on Google Drive | Actual permanent link | Reference purpose |
|---|---|---|
| **G12-MATH-GS-001-FINAL-MASTER-LAB.html** | [Open original full master lab](https://drive.google.com/file/d/1huJPwwPBNnDP4W5huCEf0fX5MvPWLqgG/view) | Full reference interactive lab; sequence, controls, drawings and behavior |
| **G12-MATH-GS-001-LAB-01.html** | [Open original single lab](https://drive.google.com/file/d/1xelTK0eYdOOrK8u_RAbeg1NwrPK_djD8/view) | Reference activity-level lab |
| **lesson.html** | [Open original lesson HTML](https://drive.google.com/file/d/1wYWwaL0ZGp_qvUz2K9c6PKlTVfvdMiep/view) | Original teaching/lesson HTML to compare together with lab |
| **Golden visual card engine source** | [V18 actual embedded shared cards source](scripts/nabil_factory/v18_editable/cards.py) | Verified repository implementation preserving shared visual/card engine |

**Golden Card original screenshot / preview:** the previously discussed artifact name is \`V18_UNIVERSAL_GOLDEN_CARDS_PREVIEW.html\`, but a stable external URL for that specific file was **not found/verified** on Google Drive in this review. It must not be represented by an invented Google Drive link. Its layout reference is the previously approved Golden Card imagery, together with the existing real shared engine [cards.py](scripts/nabil_factory/v18_editable/cards.py) and [renderer.py](scripts/nabil_factory/v18_editable/renderer.py). When the original screenshot or preview is uploaded to the repository or Drive with a stable verified ID, add its URL HERE.

**Acceptance rule:** test reference visual equivalence and actual mobile interactions; linking the files does not automatically mean the V18 renderer/lab/card conforms to them.
