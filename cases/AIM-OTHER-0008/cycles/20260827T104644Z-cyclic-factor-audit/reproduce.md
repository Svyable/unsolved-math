# Reproduce the finite audit

From the repository root, use Python 3.12 (no third-party experiment dependency):

```bash
CYCLE=cases/AIM-OTHER-0008/cycles/20260827T104644Z-cyclic-factor-audit
python -I "$CYCLE/verify.py"
python -I "$CYCLE/theory.py"
uv run oplab loop validate-cycle "$CYCLE"
uv run oplab loop verify-manifest "$CYCLE"
```

Run in a disposable checkout if replaying a sealed packet. Programs overwrite
their own deterministic output JSON only; identical replay preserves hashes.
Do not rebuild a manifest to suppress a mismatch. Each experiment was limited
to 60 seconds, with no network, paid model, randomness or external source code.
Both read only `input.json`; neither imports or reads the other's artifacts.

Expected common fields: 47,312 systems, 7,180 positive surjective systems,
10,919 global-order false positives, matching six weighting records, and table
SHA-256 `3f7c6df2560d9da94ce91cb9eed88bdc7f620ef043fa41aa381ca83cbf5dc565`.
Verification also exhausts 165,170 label assignments over 616 systems, checks
nine boundaries, and rejects seven malformed/mutated controls.

The table digest hashes UTF-8 compact JSON rows followed by LF, ordered by
n=0..7, lexicographic permutations, and N=1..8. Full tables are regenerated,
not bundled. `selection.json` records the original dataset and gate hashes.
No parent-problem solution or proof by finite extrapolation is asserted.
