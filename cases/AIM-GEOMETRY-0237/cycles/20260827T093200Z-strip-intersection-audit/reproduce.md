# Reproduce

Python 3.12 standard library only; no network, randomness, external model,
floating-point tolerance, or package installation is used by the experiments.
From this directory:

```bash
python -I theory.py
python -I verify.py
```

Compare stdout byte-for-byte with `theory-output.json` and
`verification-output.json`, respectively. The verifier reads the existing
theory output only as untrusted certificate coordinates after its own
counterexample/boundary controls. Neither executable writes artifacts.

Expected: 96 certificates accepted, 63 with shorter side greater than strip
width, 384 zero-area complement regions, 216 rejected oversized rectangles,
five polygon controls, one equal-width boundary, seven rejected corruptions.
See `execution.json` for versions, timeout, replay time and lockfile hash.

Repository checks:

```bash
oplab loop validate-cycle <this-directory>
oplab loop verify-manifest <this-directory>
```

Do not regenerate `manifest.json` after a change and call it the same immutable
packet. Any changed input or implementation requires a new reviewed packet.
