# NABIL AI — Reference lessons and truthful lesson-generation contract

**Purpose:** A non-runtime reference for Claude or any developer working on the existing NABIL AI lesson generator. This document does not change application code, deployment, routes, or indexing jobs.

## Verified classroom reference files (Google Drive)

- Grade 7 Mathematics — **Powers**, PowerPoint: https://docs.google.com/presentation/d/14VEZmrJdemu-vzHFLvLq2Y7qntqbkSFR/edit
- Grade 9 Mathematics — **Line and Circle**, PowerPoint: https://docs.google.com/presentation/d/1D3P-t0bysMGBJZUS3TyqycREZD61WYw_/edit
- Grade 9 Physics — **Refraction of Light**, reading/lesson document: https://docs.google.com/document/d/10zi9Qr09usaNzcWurY9VPp9DAI01cCeynDEsupJWFbo/edit
- Grade 9 Physics — **Lenses**, reading/lesson document: https://docs.google.com/document/d/17CJ-EpA2W_RG2R45KZZqVw6h_-D1dxsOwWBg_QWZr6g/edit
- Curriculum library folder: https://drive.google.com/drive/folders/16bcmZMO_dn4FqlGaDtl8Hky6iSBEqZpX

**Important:** These links are visual/content references, not proof that NABIL's live website already renders them or that the linked documents alone constitute the full textbook. Do not claim textbook-page verification, working audio, animation, quiz, or deployment unless actually tested.

## Required teaching experience

NABIL is the teacher, not a slide reader. Introduce the idea briefly in natural Lebanese Arabic, preserve English/French subject terminology as appropriate, show one colored concept card at a time, explain the diagram immediately below the relevant idea, solve examples step by step, ask students a question, wait for an answer, give feedback, then proceed. No unrelated subject material or long monologue. The mobile view must fit the screen. End with one visually coherent comprehensive summary card matching the approved reference style.

Each lesson should have: source provenance (book ID, grade, subject, language, printed page and PDF page when independently known); objectives; sequenced concepts; scientifically verified figures; progressive worked examples; textbook exercises only when actually retrieved; interactive checks; an interactive worksheet with answer keys and explanations; classroom presentation/slides; and final summary. A lesson can be marked complete only when each required component is present and validated. If source retrieval fails, report the missing source rather than inventing content, pages, exercise numbers, or quotations.

## Science and math correctness gates

- Grade 7 Powers: a^m × a^n = a^(m+n); a^m / a^n = a^(m−n) only for a ≠ 0; (a^m)^n = a^(mn); a^0 = 1 for a ≠ 0; distinguish (−2)^2 from −2^2.
- Grade 9 Line and Circle: distance d(O,L) < R means secant (two intersections); = R tangent (one); > R exterior (none). At tangency OT ⟂ tangent. From an external M, tangent lengths MA = MB. Figures must obey the actual conditions and labels.
- Physics Refraction: use correct normal, incidence and refraction angles measured from the normal; apply Snell's law n₁ sin i = n₂ sin r when applicable; do not invent refractive indices or rays.
- Every numerical figure, geometry point, circuit, chemistry atom/electron count, graph and plotted curve must be derived from checked inputs, not decorative image generation. Reject or flag inconsistent diagrams.

## Implementation request for Claude

1. Inspect the repository's **existing** lesson pipeline, textbook retrieval/index, content guard, frontend renderer, speech, and slide/export paths. Preserve existing functionality and work already done for physics.
2. Identify the exact existing files and root causes before changing anything. Do not add a parallel generator that bypasses existing indexing or source validation.
3. Implement a reusable lesson schema and source-grounded generator for all grades/subjects, with per-subject validators and the teaching sequence above. The reference files are examples, not a substitute for source textbooks.
4. Support explicit presentation mode for classroom display, stepwise reveal, diagrams aligned under their explanation, interactive checks and final summary card. Speech should match the revealed teaching step rather than reading an entire slide.
5. Test on Grade 7 Powers, Grade 9 Line and Circle, Grade 9 Refraction of Light. Include source-grounding, math/science figure correctness, mobile 390×844 layout, answer checking, presentation output, and regression tests on existing physics lessons.
6. Provide a concise report with changed paths, commands, actual test output, and live Railway verification if performed. Distinguish **implemented**, **tested locally**, **deployed**, and **verified on live site**. Never assert a status without evidence.

## No disruption / safety

This file is documentation only. Do not alter the deployment or production data merely to read it. Do not request Google passwords or expose API keys. If Claude lacks Drive access, ask the user to connect Drive through the provider's authorization flow or provide the specific references; do not pretend to have read them.
