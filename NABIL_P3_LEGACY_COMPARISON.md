# NABIL AI — P3 Legacy Comparison Report

## Scope
Compared three sources:

1. **Current local P3 fallback**: `NABIL_P3_FALLBACK_v1.zip`
2. **Legacy GitHub Smart Lab / Requirement-5 architecture** from `nabilakil1974-ship-it/nabil-ai-school`
3. **Old standalone Railway lab prototypes** supplied by the user (`/labs`, `/labs/secondary-physics`) and their attached HTML snapshots.

## 1. Current P3 fallback — strongest parts
- Declarative P3 spec.
- P1 + P2 scientific identity binding.
- Separate P3 scientific/runtime identities.
- Deterministic Python evaluator for `function_graph`.
- Independent checks for function value, asymptote and MH distance.
- Teaching/Reference modes.
- Progressive-reveal state.
- Exact Restart for science + reveal state.
- Two-run scientific lock helper.
- Isolated P3 backlog helper.
- Mandatory Node behavior test.
- Rejects constant-readout fake runtime.

### Missing
- Only `function_graph` evaluator exists.
- No production renderer comparable to legacy Smart Lab.
- No real teacher voice/pointer DOM runtime.
- No legacy published-lab routing/loader integration.
- No source-evidence quote / verified-figure contract in P3 spec.
- No Physics/Chemistry/Biology evaluators yet.
- No interrupt→answer→exact-resume bridge in P3.
- No cross-subject production integration.

## 2. Legacy GitHub — reusable pieces

### Core scientific/renderer files
- `scripts/nabil_interactive_lab.py`
  - Generic verified kinds:
    - `FORMULA_CALCULATOR`
    - `ORIENTATION_INVARIANT`
    - `SHAPE_RESPONSE`
    - `EVIDENCE_SEQUENCE`
    - `EVIDENCE_REVEAL`
    - plus advanced families.
  - Validates teacher script, targets, before/after state, scientific constraints and evidence quote.
  - Has reference lab shell, teacher pointer, highlights and teach controls.

- `scripts/nabil_advanced_lab.py`
  - `DC_SERIES_CIRCUIT`
  - `OPTICS_REFLECTION`
  - `IONIC_COMPOUND`
  - `GEOMETRY_PROOF`
  - Valuable deterministic domain invariants:
    - open DC switch => no current;
    - reflection angle measured from normal and i=r;
    - ionic charge/ratio/electron-transfer checks.

- `scripts/nabil_geometry_lab.py`
  - Geometry proof renderer/validator.
  - Points, segments, equal marks, parallel/right-angle marks, proof steps, drag constraints.

- `scripts/nabil_requirement5_gate.py`
  - Fail-closed source/evidence gate.
  - Requires source text or verified figure.
  - Requires teacher script with evidence-backed actions.
  - Requires pointer/highlight/explanation/conclusion; dynamic labs require justified animation.

### Runtime / route pieces
- `app/api/routes_smart_labs.py`
  - Published zero-AI lab endpoint.
  - `PUBLISHED_LAB_NOT_READY` fail-closed behavior.
  - `POST /from-question`.
  - Published artifact reading.

- `app/static/nabil_verified_lab_loader_v19.js`
  - Exact `lesson_id + lab_id + language` loader.
  - No silent wrong-lab fallback.

- `app/static/nabil_smart_lab_bridge_v1.js`
  - `nabil:teach-all`, `nabil:teach-stop`.
  - Smart Lab from student question.
  - Whole-lesson lab orchestration.
  - Bridges to speech.

- `app/static/nabil_lab_voice_v1.js`
  - Shared browser speech helper.

- `app/static/nabil_lesson_e2e_runtime_v1.js`
  - Existing lesson speech / interaction runtime and chat bridge.

## 3. Old standalone lab prototypes

### `/labs/light`
Strong UX/reference value:
- Reflection + refraction.
- Converging lens.
- Sliders/readouts.
- Responsive layout.
- Teacher explanation, steps, quiz.
- Offline standalone behavior.

Weakness:
- Standalone/hard-coded scientific demo, not bound to exact lesson/P1/P2 evidence.

### `/labs/math`
Strong UX/reference value:
- Points, vectors, line, midpoint.
- Coordinate controls.
- Arabic/English/French.
- Teacher explanation, formulas, quiz, notebook summary.

Weakness:
- General-purpose prototype, not a source-locked Golden lesson lab.

### `/labs/secondary-physics`
Strong UX/reference value:
- Thin lens.
- Projectile motion.
- RC charging circuit.
- Play/Pause/Step/Restart.
- Live equations/readouts/graphs.
- Arabic/English/French.
- Quiz + notebook summary.

Scientific behavior is better than a static fake because control values recalculate the visible model, but it is still browser-JS scientific authority and is explicitly a prototype rather than a verified textbook artifact.

### Other GitHub standalone lab
- `/labs/chemistry`
- `nabil_lab_chemistry_full.html`

## 4. Best architecture — merge, do not choose one

### Scientific authority
Use **current P3 architecture** as authority:
- source identity
- P1 identity
- locked P2 science
- declarative model
- independent evaluator
- behavior gate
- lock/backlog

### Evidence authority
Import from **legacy Requirement 5**:
- `evidence_basis`
- `evidence_quote`
- verified figure status
- per-step `state_before`
- `state_after`
- `scientific_constraints`
- fail-closed publication

### Family evaluators
Port legacy domain knowledge into independent P3 evaluators:
- `DC_SERIES_CIRCUIT` -> Python circuit evaluator
- `OPTICS_REFLECTION` -> Python optics evaluator
- `IONIC_COMPOUND` -> Python chemistry evaluator
- `GEOMETRY_PROOF` -> geometry evaluator
- `EVIDENCE_REVEAL` -> evidence-only evaluator/runtime
- then add projectile, RC, lens, biology families.

### Presentation/runtime
Reuse legacy:
- reference Smart Lab shell
- pointer/glow
- voice
- teach-all/stop
- verified loader
- published artifact routes
- exact lesson/lab/language loading

Use old standalone labs as **visual and interaction fixtures**, never as scientific authority.

## 5. Required P3 v2 merge order

1. Keep P3 identity/lock/backlog unchanged.
2. Add evidence binding fields to P3 spec.
3. Add teacher step fields:
   - `evidence_quote`
   - `state_before`
   - `state_after`
   - `scientific_constraints`
   - `target_ids`
4. Port Requirement-5 fail-closed gate.
5. Add independent evaluators:
   - function graph
   - DC circuit
   - reflection/refraction/lens
   - projectile
   - RC
   - ionic compound
   - geometry proof
   - evidence reveal
6. Reuse old Smart Lab renderer/pointer/voice shell.
7. Bind verified-loader routes to P3 identities.
8. Add Node behavior tests per family.
9. Add Teaching/Reference reveal tests.
10. Preserve interrupt→answer→exact resume.
11. Use old Railway labs as visual acceptance fixtures.
12. Never publish an old prototype directly as a Golden lab without source/P1/P2/P3 validation.

## Conclusion
The legacy system is **not obsolete**. It contains substantial renderer, evidence-gate, domain-validation, voice, route and UI work that the current P3 fallback does not yet have.

The current P3 fallback is stronger in **identity, deterministic scientific authority, behavioral testing, locking and isolation**.

The correct P3 is the **union**:
`P3 identity/evaluator/lock` + `Requirement-5 evidence gate` + `legacy Smart Lab runtime/pointer/voice/routes` + `old lab UX as visual fixtures`.

Do not replace one with the other.
