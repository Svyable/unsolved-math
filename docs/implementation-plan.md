# Implementation plan

## Milestone 1 — deterministic vertical slice

- Pin and download/import `problems.json`.
- Preserve an immutable local raw snapshot and source manifest.
- Normalize only the fields needed for status tracking and ranking.
- Diff upstream statuses while labeling every change unverified.
- Produce explainable research and status-review queues.
- Test the integrity boundary and run it in CI.

## Milestone 2 — human verification ledger

- Add reviewer-owned assessments with named reviewer, date, primary-source
  evidence, and explicit confidence.
- Prevent imports from overwriting human assessments.
- Add review assignment and aging policies.

## Milestone 3 — research cases

- Create immutable problem snapshots and case directories.
- Add bounded experiments, adversarial review, and provenance manifests.
- Keep speculative, computational, cited, and formally checked claims separate.

## Milestone 4 — optional formalization and literature adapters

- Add opt-in, allowlisted literature retrieval with captured evidence.
- Add a Lean 4 boundary for narrowly scoped lemmas only.
- Require human approval before remote-model or expensive formalization runs.
