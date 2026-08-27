# Reproduce the exact certificates

Python 3.12, standard library only. From this cycle directory:

```sh
python -I theory_check.py
python -I verify.py
```

Compare stdout byte-for-byte with `theory-output.json` and
`verification-output.json`, respectively. No network, external model, seed or
floating-point tolerance is involved. Do not overwrite sealed packet files.

The first executable uses exact convolution integrals. The second starts in an
isolated process from the raw fixture and uses direct segment dynamics plus
matrix-vector coefficient checks. Their comparable case values and attaining
states are checked only after both runs complete. Both are same-assistant code;
there is no claim of independent human/model proof review.

From the repository root:

```sh
uv run oplab loop validate-cycle cases/AIM-COMPUTATION-0010/cycles/20260827T063300Z-support-margin-audit
uv run oplab loop verify-manifest cases/AIM-COMPUTATION-0010/cycles/20260827T063300Z-support-margin-audit
```

Scope is the fixed terminal reachable-set problem in `input.json`. Analytic
all-input bounds and their assumptions are explicit in the two lane notes.
No finite collection of trajectories is promoted to a general HJ solver guarantee.
