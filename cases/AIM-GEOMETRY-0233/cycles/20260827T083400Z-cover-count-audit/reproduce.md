# Reproduce the cover-count audit

Python 3.12, standard library only. From this packet directory:

```sh
python -I theory_count.py
python -I verify.py
```

Compare stdout byte-for-byte with `theory-output.json` and
`verification-output.json`. Neither program writes files, accesses a network,
uses random seeds or calls external models. Allow up to 90 seconds for the
verifier's 553,385 explicitly enumerated tuples. Do not overwrite sealed files.

Compare all 50 `based_subgroups` values from the verification `formal_log_rows`
with the theory `rows`, keyed by `(rank,degree)`. Compare all 23 verification
enumeration rows on both `based_subgroups` and `transitive_tuples`. The example
denominator and guaranteed count must also agree.

From the repository root:

```sh
uv run oplab loop validate-cycle cases/AIM-GEOMETRY-0233/cycles/20260827T083400Z-cover-count-audit
uv run oplab loop verify-manifest cases/AIM-GEOMETRY-0233/cycles/20260827T083400Z-cover-count-audit
```

Both implementations have same-assistant authorship with separate algorithms
and fresh-process execution. The mathematical statement is conditional; no
geodesic existence or uniform-degree hypothesis is supplied by enumeration.
