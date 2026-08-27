# Reproduce

From this cycle directory, using Python 3.12 (standard library only):

```sh
python -I theory_check.py
python -I verify.py
```

Compare stdout byte-for-byte with `theory-output.json` and
`verification-output.json`, respectively. Commands take less than one second
on the preparation environment; runtime is not part of the mathematical claim.
No network, external model, or random generator is used. Do not overwrite sealed
packet files when rerunning; compare stdout or use temporary output paths.

The raw dataset is not redistributed in this packet. Its exact statement is in
`snapshot.json`, with the original file SHA-256 and immutable source revision.
The restored normalized index and ranked queues are outside the cycle under
`data/`, sealed by their own dataset manifest. Its SHA and the selection-time
queue/history hashes are recorded in `selection.json`.

From the repository root:

```sh
uv run oplab validate
uv run oplab loop validate-cycle cases/AIM-ALGEBRAIC_NUMBER_THEORY-0096/cycles/20260827T043400Z-index-effectivity-audit
uv run oplab loop verify-manifest cases/AIM-ALGEBRAIC_NUMBER_THEORY-0096/cycles/20260827T043400Z-index-effectivity-audit
```

Claim origins, cross-lane references and limitations are in `cycle.json`.
Neither this packet nor the restored queue is evidence of parent-problem resolution.
