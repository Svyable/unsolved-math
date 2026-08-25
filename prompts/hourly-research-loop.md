# Durable prompt: hourly research loop

Work in `Svyable/unsolved-math` for one bounded research cycle. Read the current
`README.md`, `docs/hourly-loop.md`, `docs/research-integrity.md`,
`config/research-loop.toml`, `config/first-run.json`, ranked queue, loop history,
and open automation PR before acting. Run `oplab loop preflight` before spending
the research budget.

1. Select the highest-ranked research candidate outside cooldown and
   anti-thrashing gates. If the queue is missing, first try to restore the sync;
   if it cannot be restored in this run, use only an unexpired, validated
   candidate from `config/first-run.json`. Its ordering is explicitly not a
   ranking. Do not improvise a replacement candidate.
2. Freeze the exact statement, statement SHA-256, upstream revision and file
   SHA-256, source links, imported status claim, and prior-cycle dependencies in
   the schema-v2 `frozen_problem` object. Narrow the target to one falsifiable
   subclaim or lemma.
3. Perform the theory lane: definitions, quantifiers, assumptions, at least two
   approaches, explicit typed claims, and one evidence-backed progress unit.
4. Perform the verification lane from fresh context and separate evidence
   files. Counterexample and edge cases first; then independently check claims,
   citations, computations, and proof steps. Record the method family and the
   concrete independence basis. Produce one evidence-backed verification
   progress unit and at least one `independent_context: true` check.
5. Material progress means a concrete new artifact or changed evidentiary
   state: counterexample/certificate, assumption reduction, equivalent
   formulation, verified primary-source claim, reproducible discriminating
   experiment, exact proof gap, retired approach, or kernel-accepted sublemma.
   More prose is not progress. Never fabricate progress to satisfy cadence.
6. Store the packet under
   `cases/<problem-id>/cycles/<cycle-id>/`, including `cycle.json`, theory and
   verification notes, executable artifacts, captured primary-source evidence
   where permitted, and `manifest.json`. Build and then verify the canonical
   manifest over every packet file. Record the cycle only after
   `oplab loop verify-manifest` passes.
7. Create or refresh only the branch `automation/hourly-research-loop` and its
   human-review pull request. Never commit directly to `main`, merge, modify an
   upstream status, publish externally, call paid external models, or claim the
   parent problem is solved.
8. Report the exact theory delta, verification delta, remaining blocking
   objections, commands/checks run, artifact hashes, and PR link. If no honest
   two-lane progress was possible, report that plainly and explain the minimum
   blocker; do not create a cosmetic cycle.
