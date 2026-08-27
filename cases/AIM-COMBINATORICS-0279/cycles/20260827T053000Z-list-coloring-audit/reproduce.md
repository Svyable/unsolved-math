# Reproduction

Python 3.12, standard library only; no network, randomness or external models.
From this packet directory:

```sh
python -I theory_check.py --certificates /tmp/oplab-0279-peeling.jsonl
python -I verify.py
python -I check_certificates.py
```

Compare stdout with the corresponding `theory-output.json` and
`verification-output.json`; compare the temporary certificate file byte-for-byte
with `peeling-certificates.jsonl`. Do not overwrite sealed packet files.
The final command checks stored certificates against the independently generated
verification digest; its stdout matches `certificate-check-output.json`.
Both runs complete in seconds on the preparation machine. Finite assertions
are checked exactly, without floating-point tolerances.

The verification executable reads only the shared raw fixture. It recomputes
all accepted graph invariants with different recognition and degree algorithms,
then reports a comparable classification digest. Executable replay is not a
formal-kernel proof of the cited structural theorem or arbitrary-list corollary.

From the repository root:

```sh
uv run oplab loop validate-cycle cases/AIM-COMBINATORICS-0279/cycles/20260827T053000Z-list-coloring-audit
uv run oplab loop verify-manifest cases/AIM-COMBINATORICS-0279/cycles/20260827T053000Z-list-coloring-audit
```

Selection uses the already validated review-branch queue; this packet does not
change its ranking, raw source revision, imported statuses or prior cycles.
