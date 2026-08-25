# Durable prompt: hourly research loop

Work in `Svyable/unsolved-math` for one bounded research cycle. Read the current
`README.md`, `docs/hourly-loop.md`, `docs/research-integrity.md`,
`config/research-loop.toml`, ranked queue, loop history, and open automation PR
before acting.

1. Select the highest-ranked research candidate outside cooldown and
   anti-thrashing gates. If the queue is missing, first try to restore the sync;
   if it cannot be restored in this run, choose a clearly labeled provisional
   L1–L3 UnsolvedMath record with an accessible primary source. Never invent a
   ranking.
2. Freeze the exact statement, upstream revision, source links, and prior-cycle
   dependencies. Narrow the target to one falsifiable subclaim or lemma.
3. Perform the theory lane: definitions, quantifiers, assumptions, at least two
   approaches, explicit typed claims, and one evidence-backed progress unit.
4. Perform the verification lane from fresh context. Counterexample and edge
   cases first; then independently check claims, citations, computations, and
   proof steps. Produce one evidence-backed verification progress unit and at
   least one `independent_context: true` check.
5. Material progress means a concrete new artifact or changed evidentiary
   state: counterexample/certificate, assumption reduction, equivalent
   formulation, verified primary-source claim, reproducible discriminating
   experiment, exact proof gap, retired approach, or kernel-accepted sublemma.
   More prose is not progress. Never fabricate progress to satisfy cadence.
6. Store the packet under
   `cases/<problem-id>/cycles/<cycle-id>/`, including `cycle.json`, theory and
   verification notes, executable artifacts, captured primary-source evidence
   where permitted, and `manifest.json`. Validate hashes and the two-lane
   contract.
7. Create or refresh only the branch `automation/hourly-research-loop` and its
   human-review pull request. Never commit directly to `main`, merge, modify an
   upstream status, publish externally, call paid external models, or claim the
   parent problem is solved.
8. Report the exact theory delta, verification delta, remaining blocking
   objections, commands/checks run, artifact hashes, and PR link. If no honest
   two-lane progress was possible, report that plainly and explain the minimum
   blocker; do not create a cosmetic cycle.
