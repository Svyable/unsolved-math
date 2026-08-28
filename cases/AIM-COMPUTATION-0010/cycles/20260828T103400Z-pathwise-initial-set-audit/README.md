# Correlated-initial-set pathwise audit

Read snapshot.json, selection.json, input.json, theory.md and verification.md in that order. The exact witness retires a three-sample certification shortcut; the sharper continuous bound preserves initial correlation. This is not a parent solution or new algorithm claim.

From this directory, using Python 3.12+:

    python experiments/run.py baseline
    python experiments/run.py theory
    python experiments/run.py verify
    python experiments/run.py replay

The baseline is a fresh-context direct-dynamics calculation. To reproduce without replacing the original execution metadata, copy this packet to a temporary directory first. Replay preserves its original replay log if present; it still checks output equality.

Table columns: delta, eta, vbar, a, epsilon, T, exact pathwise maximum, earliest maximizing time, maximum at 0/T/2/T, coordinate-box maximum. All values are exact rational strings. The two table files are separately generated and have identical hashes because their complete contents agree.

From the repository root:

    uv run oplab loop validate-cycle cases/AIM-COMPUTATION-0010/cycles/20260828T103400Z-pathwise-initial-set-audit
    uv run oplab loop verify-manifest cases/AIM-COMPUTATION-0010/cycles/20260828T103400Z-pathwise-initial-set-audit

The manifest covers every packet file except itself. Runner logs have source, input and output SHA-256 digests. No imported mathematical status is modified.
