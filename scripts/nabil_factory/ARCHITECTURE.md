# NABIL Golden Factory — modular ownership

The lesson factory is split by responsibility.  New fixes go to the owning
module; do not grow `scripts/nabil_lesson_factory.py` again.

## P1 — source/evidence
Path: `scripts/nabil_factory/p1/`

Owns exact source identity, TOC/opener verification, page evidence, figures,
exercise extraction identity, source inventory and source-completeness gates.
P1 output is the verified Evidence Map consumed by P2.

## P2 — locked lesson/science
Path: `scripts/nabil_factory/p2/`

Owns grounded concept generation, exercise solving, independent scientific
review, scientific gates and Requirement-5 scientific contracts.  P2 is not
allowed to pick another book or weaken P1 evidence.

## Cards
Path: `scripts/nabil_factory/cards/`

Owns reference teaching cards, worked-example/solution cards, visual cards,
Golden Final Card and HTML/card compilation.  It consumes approved P2 only.

## Published Drive delivery
Path: `scripts/nabil_factory/drive_runtime/`

Owns production-time retrieval/synchronization of already verified published
Golden packages from Drive into the canonical/local runtime package/catalogue.
The browser/student runtime must not depend on live Drive access.

## Factory
Path: `scripts/nabil_factory/factory/`

Owns orchestration, provider pool, durable checkpoints/resume, process exit
states, atomic promotion and publish verification.  It coordinates modules but
does not contain lesson science or card templates.

## Thin entry point
`scripts/nabil_lesson_factory.py` must become only argument parsing + calls into
`scripts.nabil_factory.factory.orchestrator`.  No new P1/P2/cards/Drive logic
may be added to the entry file.

Target call graph:

```
CLI main
  -> factory.orchestrator
       -> p1
       -> p2
       -> cards
       -> factory.publisher
       -> drive_runtime (published package/catalogue handoff)
```
