# Verification: independent algorithms, explicit authorship limits

## Starting context and independence

The initial constraint solver and exhaustive-label baseline in `verify.py` were
implemented/run from `input.json` before `theory.py` was written. Global-order
counting and formatting were added afterward. It does not read theory notes,
claims, output, or code. A fresh
isolated Python process builds modular difference constraints and propagates
labels along forward and reverse edges. Theory instead explicitly finds
cycles and counts independent phases from their lengths. The verifier also
enumerates every possible labeling on a smaller domain, rather than relying
solely on a second structural algorithm.

This is process and algorithm separation, **not** independent model or human
authorship. Both programs were written by the same assistant. They share the
input specification, permutation enumeration library, serialization convention,
Python runtime, and standard-library arithmetic. General proofs remain open
to an independent referee; no kernel acceptance is claimed.

## Counterexamples and boundaries first

Before the main sweep, the verifier exhausts all eight assignments for
T=(0 1)(2), N=2 and confirms zero maps despite source order 2. It checks nine
boundary cases: empty domains, singleton domains, N=1, consistent and
inconsistent cycles, disjoint cycles, and composite periods. It explicitly
distinguishes the empty equivariant map from surjectivity. Valid wraparound
and noninjective maps are positive controls.

Seven adversarial controls reject a changed color, constant map, out-of-range
color, missing value, nonbijective input, bad vertex index, and zero modulus.
The rejection checks are executable assertions, not an inferred test status.

## Computation check

The constraint solver agrees with the theory count across all 47,312 systems
on 0–7 labelled vertices and N=1–8. The shared digest of the ordered rows
`[n, permutation, N, equivariant_count, surjective_count]` is
`3f7c6df2560d9da94ce91cb9eed88bdc7f620ef043fa41aa381ca83cbf5dc565`.

Separately, all 165,170 possible label assignments across 616 systems on
0–5 vertices and N=1–4 were tested directly against every equivariance equation
and surjectivity; zero mismatches occurred. Repeated composition, without
cycle-length lcm, checks global order and reproduces the 10,919 shortcut
false positives. Six explicit weighting examples independently yield the same
fractions and zero factor maps, including 40/41 versus 1/21 at k=20.

## Proof-step and citation checks

Necessity uses the closing congruence on **each** orbit, not just the lcm of
orbit lengths. Sufficiency chooses phases independently and verifies closure.
Counting has no quotient by relabelling: X is labelled, C_N has fixed labels,
and distinct phases are distinct maps. Surjectivity uses a nonempty orbit;
the empty-domain exception is tested. The weighting limits use k≥1 and do not
sample or claim anything about actual ASMs. These steps are a same-author
argument audit, not an independent theorem verification.

The primary PDF was checked directly, separately from the imported summary.
Printed pages 5–6 locate the extraction across commentary/section boundaries
and distinguish Problem 2.5 from Problem 2.4. This verifies a source-location
claim, not the present mathematical status of resonance or all claims in the
dataset. Access details and capture limits are in `sources.json`.

## Delta and unresolved objections

The imported criterion now has an exact finite regression audit, an empty-set
boundary, and a fully exhausted obstruction certificate. State and orbit
weighting are experimentally distinguished rather than silently conflated.
General proof, actual combinatorial systems, primary-source scope review, and
independent human/model review remain separate obligations. The correct
disposition is human scope review, not a parent-problem result.
