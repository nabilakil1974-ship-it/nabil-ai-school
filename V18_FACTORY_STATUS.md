# NABIL AI — V18 factory branch

This branch was created from `refactor/lesson-factory-modular-v1` to preserve the established PDF indexing, source evidence, Pydantic contracts, OCR normalization, deterministic mathematics, scientific review, QA, Drive publishing, checkpoint/resume, and error handling.

## V18 integration acceptance criteria

The production renderer must use the original V18 P3 runtime, not a slow-text approximation:
- original runtime_controller.js and universal_smart_board.js
- scientific_visual_router.js and scientific_models.js
- p3_lab_standard_v12.js and associated dependencies
- step-level synchronized speech and board progression
- functioning interactive labs for concepts and exercises
- final Golden Card as the LAST step
- self-contained or correctly served dependencies on both NABIL platform and local exported HTML
- complete Chrome/Playwright and mobile manual verification
- fail-closed scientific gates; no unchecked publishing

## Current state

The branch has been created, but the V18 runtime bundle has NOT yet been uploaded/fully integrated. Do not call this branch V18-complete or deploy it as a replacement for production until the above conditions pass.

The original 126-file V18 archive is available in the working session as `NABIL_V18_FULL_COMPREHENSIVE_P1_P2_P3_TEACHER(1).zip`.
