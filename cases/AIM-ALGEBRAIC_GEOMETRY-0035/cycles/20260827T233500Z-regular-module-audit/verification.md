# Independent-method verification

The verifier and baseline existed before theory.py. Starting only from input.json,
it checks J_3 plus J_1 and J_2 plus J_1, zero and invalid scalar actions, then
enumerates the full finite domains before reading a theory certificate.

It iterates g on each standard basis vector and rejects g^q != I. It computes
orbit-span rank by incremental modular elimination, rather than relying on a
Jordan classification or a matrix-power nonvanishing implication. For each
regular action, it checks full rank and g*b_j=b_(j+1 mod q). Finite differences
of the orbit independently recover the two tested N-powers. Matrix encodings
are enumerated by Cartesian products, versus base-p integer decoding in theory.

All 19,699 input matrices, 733 valid actions and 627 regular-action certificates
agree. The nine larger block controls agree. Seven deliberately altered outputs
are rejected by reconstructed-table comparison: false regularity in dimension
q+1, weakened exponent, broken basis, omitted action, erased generator, changed
enumeration bound and changed group order. These are integrity/adversarial tests,
not a formal proof-checker completeness claim.

Reproduce from this packet directory:

```
python experiments/run.py baseline
python experiments/run.py theory
python experiments/run.py verify
python experiments/run.py replay
```

The runner uses fresh Python -I children, an empty environment, CPU/wall/memory
limits and no imports between mathematical implementations. The programs have
no network calls, dynamic code execution or imported-text execution. Isolation
is process/resource isolation, not a network namespace. Replay checks output
bytes, and logs record commands, source/input/output hashes and timestamps.
Both implementations have same-assistant authorship and share the specification;
there is no independent human/model or kernel proof review.

## Remaining objections

The ordinary proof separates the dimension condition from the top-power test;
its independence argument is sound as written but not independently authored or
kernel accepted. The small exhaustive census cannot prove it for every field or q.
The matrix certificate does not establish existence of a finite spectrum realizing
this residual action. It does not check grading, Morava K-cohomology, descent,
filtration attachments or the imported stable-multiple assertion. The AIM source
is unavailable. Carrick's source supplies a defect formula, not an automatic
rank-one realization theorem. Parent statuses and canonical statement stay unchanged.
