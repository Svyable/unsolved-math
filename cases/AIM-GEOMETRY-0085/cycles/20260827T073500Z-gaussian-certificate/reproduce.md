# Reproduction

Python 3.12, standard library only. From this directory:

```sh
python -I theory_search.py
python -I verify.py
```

Stdout must match `theory-output.json` and `verification-output.json` byte for
byte. Neither executable writes files, accesses the network, calls models, uses
randomness, or uses floating-point approximations. Each finite grid has 70,200
triples; allow up to 60 seconds per command. Do not overwrite sealed artifacts.

After independent execution compare `grid_triples_tested`, `certified_triples`
and `certified_grid_sha256` in both outputs. The verification `winning_bound`
must match the theory certificate's `density_upper_bound`. A fresh process is
algorithmic isolation, not a claim of independent model or human authorship.

From the repository root:

```sh
uv run oplab loop validate-cycle cases/AIM-GEOMETRY-0085/cycles/20260827T073500Z-gaussian-certificate
uv run oplab loop verify-manifest cases/AIM-GEOMETRY-0085/cycles/20260827T073500Z-gaussian-certificate
```

The frozen rational inputs, source audit and analytic assumptions are included.
The packet demonstrates a certificate and bounded search, not a new optimal
packing or an autonomous resolution of the canonical research heading.
