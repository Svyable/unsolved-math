# Verification lane

The verifier was authored and its baseline executed before theory.py existed.
It starts from input.json, checks escaping-denominator witnesses and the zero/
unit boundary, then reconstructs all finite groups and paths before reading
the theory output. The baseline source is archived byte-for-byte in
experiments/baseline-verifier.txt; the final verifier only wraps one string
literal to meet the line-length check. It imports no theory or previous research code. Repeated
addition computes element orders; residue enumeration checks transition
surjectivity and equal fibers. This differs from valuation/totient formulas.

All 32 group tables, 4,008 elements, 480 denominator witnesses and 52 exponent
escapes agree. Seven mutated tables are rejected by complete reconstruction
and equality comparison: erased residue, wrong escape level, wrong exponent,
wrong identity count, wrong fiber, missing row, and erased escape residue.
These are certificate-integrity controls, not proof-checker completeness tests.

Commands from the packet directory:

```
python experiments/run.py baseline
python experiments/run.py theory
python experiments/run.py verify
python experiments/run.py replay
```

Each mathematical child runs Python -I with empty environment and explicit
CPU/wall/memory/file limits. This is process/resource isolation, not a network
namespace. The reviewed programs contain no networking or dynamic execution.
Replay must preserve exact output bytes. Execution logs record code/input/output
hashes and commands. Both algorithms have same-assistant authorship and share
the specification: there is no independent model, human or kernel proof review.

## Proof and citation objections

The finite census cannot certify nonvanishing in an infinite limit. The ordinary
proof instead quantifies over every nonzero integer and gives coordinate
v_p(d)+1; negative d have the same annihilation behavior. The localization
definition then requires one annihilator, not one per coordinate. This is the
precise failed dependency in the stagewise shortcut.

The bounded-exponent control verifies the sufficient common-annihilator
repair, not a general continuity theorem. The group construction lives in
ordinary abelian groups. No identification with a derived limit of spectra,
Tate fixed points, Frobenius map or HRW filtration is checked. The theorem about
the p-complete sphere is externally cited, not independently proved here.
The live AIM page failed to load. Its frozen text and imported summary are
not verified merely because their hashes match. Parent question remains open
to review; no solve claim or status mutation is made.
