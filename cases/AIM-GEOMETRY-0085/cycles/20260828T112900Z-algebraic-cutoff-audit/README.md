# Algebraic cutoff and directed rounding

Read snapshot.json, selection.json, input.json, theory.md and verification.md. The frozen cubic and dimension are unchanged. The new evidence characterizes its admissible cutoff set and certifies directed rounding; this is not a new packing record or a solution to the source heading.

From this directory, Python 3.12+:

    python experiments/run.py baseline
    python experiments/run.py theory
    python experiments/run.py verify
    python experiments/run.py replay

To preserve recorded execution timestamps, reproduce in a temporary copy. The two tables contain rows [bits, lower cutoff, upper cutoff, P(lower), P(upper), nearest cutoff, nearest is valid]. Rational values are strings; no float is used. The final exact bound is U^12/(4^12*12!), with U=63944510809/4294967296. The objective interval encloses only this fixed function's optimum and is not a packing-density lower bound.

From the repository root:

    uv run oplab loop validate-cycle cases/AIM-GEOMETRY-0085/cycles/20260828T112900Z-algebraic-cutoff-audit
    uv run oplab loop verify-manifest cases/AIM-GEOMETRY-0085/cycles/20260828T112900Z-algebraic-cutoff-audit

Every packet file except manifest.json itself is covered by the canonical manifest. Runner logs bind source, input and output SHA-256 values. No upstream status was changed.
