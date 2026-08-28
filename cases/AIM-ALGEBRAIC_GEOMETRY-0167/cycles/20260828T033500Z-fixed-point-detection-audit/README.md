# Fixed-point detection audit

Run from this directory with Python 3.12 or newer:

```sh
python experiments/run.py baseline
python experiments/run.py theory
python experiments/run.py verify
python experiments/run.py replay
```

The original initial-baseline-execution.json predates theory.py. Re-running baseline later reproduces its data but does not recreate that authorship order. Initial source bytes (as .py.txt) and logs preserve the five original runs; current logs record three reruns after lint-only corrections. The runner limits CPU, memory, output size and wall time. It does not isolate networking; the math scripts contain no network calls.

The finite tables and counterexamples do not compute stable homotopy groups. Read theory.md for the source-dependent cofiber interpretation and all-subgroup repair, verification.md for checks and limitations, snapshot.json for exact imported provenance, and cycle.json/manifest.json for evidence references. No parent solution or changed imported status is claimed.
