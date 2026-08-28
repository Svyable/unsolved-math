# Reproduction and boundaries

From this packet directory, with Python 3.12 or later:

```sh
python experiments/run.py baseline
python experiments/run.py theory
python experiments/run.py verify
python experiments/run.py replay
```

Only Python's standard library is used. Scripts consume input.json and do not
use the network. The baseline intentionally needs no theory certificate.
Generated execution logs include exact commands, timestamps, interpreter,
source/input/output hashes and limits. Re-running the first three modes changes
their timing logs and therefore the sealed manifest; use a scratch copy for a
full rerun. Replay preserves its existing log and requires unchanged outputs.

From the repository root:

```sh
uv run oplab loop validate-cycle cases/AIM-GEOMETRY-0233/cycles/20260828T123300Z-monodromy-period-audit
uv run oplab loop verify-manifest cases/AIM-GEOMETRY-0233/cycles/20260828T123300Z-monodromy-period-audit
```

The original run used seven mathematical subprocesses, including a second
replay after style-only fixes. Original source bytes are archived alongside
their execution logs; final replay hashes refer to the current scripts. Packet generation,
provenance, repository tests and sealing are separate administrative checks.
Finite outputs certify finite monodromy and graph paths only. They do not
implement surface topology, prove an infinite geometric claim, or change any
upstream status.
