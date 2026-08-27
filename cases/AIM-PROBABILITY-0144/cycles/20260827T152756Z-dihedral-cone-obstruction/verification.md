# Independent-method verification record

## Fresh context and independence basis

The baseline `verify.py` was written and run from the frozen input BEFORE the
theory program was created. It consumes no theory code or notes. Its method
families are INDEPENDENT_IMPLEMENTATION, COUNTEREXAMPLE_SEARCH and, for the
separate analytic discussion below, PROOF_STEP_AUDIT.

Verifier arithmetic represents a+b*sqrt(5) using rational coefficients and signs
by exact squared comparisons. Theory arithmetic represents a+b*phi with integer
coefficients and signs by rational bisection of the positive root of X^2-X-1.
The verifier uses a five-step rotation orbit and checks reflection closure and
Gram norms; the theory independently generates the whole reflection closure
by BFS. The verifier counts ideal maxima; theory directly enumerates
incomparable subsets. The verifier exhausts pair-state assignments; theory
constructs permutations of a chain from its proposed rigidity proof.

Both programs have same-assistant authorship and share Python, integer/rational
arithmetic, root input and mathematical definitions. Fresh -I processes with
empty environments provide execution separation, not independent human/model
reasoning or kernel acceptance. The later certificate comparison receives
theory output only AFTER recomputing the entire checked core from input.

## Falsification and boundaries first

The first check obtains the cone's non-target H polynomial and incomparable
nonsimple roots 2,3 directly from exact coordinate differences. It does not
assume the desired abstract model is geometric. Ten probes cover that
incomparability, zero and mixed-sign radical comparisons, the two minima, empty
and full subsets, self-relations, reverse cycles, and missing transitivity.
Malformed orders are rejected before ideal or orbit enumeration.

## Exact computation checks

The explicit input roots and their negatives equal the independently computed
rotation orbit and its negative. All ten have Gram norm one; both reflections
preserve the set and square to the identity. The product has order five on a
simple root. No floating-point evaluation is used.

The cone has eight antichains and orbit lengths [2,2,4]. Each of the two minimal
abstract extensions has seven antichains and lengths [2,5]. Full cycle maps,
not only lengths, are compared between the two implementations. All eight
abstract family profiles m=3..10 agree exactly.

The independent census uses 2^(2*(m-2)) choices for relations from the two
marked minima and 3^choose(m-2,2) states for each remaining unordered pair.
No relations into the marked minima or between them are allowed. Transitivity,
irreflexivity and asymmetry are checked; all other vertices must have a
predecessor. Thus every labelled poset with exactly those minima occurs once.

| m | Pair-state assignments | Valid posets | Target H orders |
|---:|---:|---:|---:|
| 3 | 4 | 3 | 1 |
| 4 | 48 | 19 | 2 |
| 5 | 1,728 | 219 | 6 |
| 6 | 186,624 | 4,231 | 24 |

Total: 188,404 assignments, 4,472 valid posets, 33 target orders. All target
relation sets match the independently constructed chain permutations. Of the
six size-five target orders, exactly two contain the geometric cone order;
each adds one relation. This verifies minimality within the stated class.

Seven modified proposed cores are rejected against the independently
recomputed core: removed H coefficient, wrong orbit profile, missing relation,
wrong root count, missing refinement, wrong marked count, and wrong family
coefficient. These are deterministic semantic mismatches, not file-hash-only
checks or a general claim about malformed JSON handling.

## Proof-step and citation checks

The cone difference (phi-1,1-phi) has opposite signs because phi>1. An added
middle comparison cannot be a true cone comparison. The target t^2 coefficient
accounts only for the two marked minima; every other pair must be comparable.
With the minima fixed, that forces all remaining vertices above them and into
one chain. The displayed abstract orbit has length m, while the two singleton
minima form a disjoint 2-cycle. These are definition-based ordinary checks,
not a machine-checked proof for every m.

Primary source audit uses the AIM PDF printed pages 4–5 and Cuntz–Stump v1,
introduction, Property 4, Table 2, section 3.1 and Figure 1. Web inspection and
separately downloaded PDF bytes agree with the input convention and abstract
model. `sources.json` records fingerprints; full PDFs are not redistributed.
Only those locators and the stated warning are checked, not the full paper's
proofs, modern literature completeness, or current mathematical status.

## Reproduce and remaining limitations

In a disposable copy run `python -I reproduce.py`. It reruns both methods,
compares all core values and checks against the preserved verifier baseline.
Use `python -I reproduce.py --baseline` only to regenerate a baseline in that
copy, never to overwrite sealed evidence. The output JSON is deterministic;
runtime seconds and absolute interpreter paths in logs are environment-specific.

Each child has 180 CPU seconds, 200 wall seconds, 512 MiB address space and a
16 MiB file-output limit. No network/model calls or secrets are used; no OS
network namespace was created. Initial work uses three children and one final
two-child replay, five research children total.

Blocking limitations: same-author reasoning, no kernel/human/model review;
source-fragment scope; no H4 or all-root-realization claim. The general rigidity
argument is labelled UNVERIFIED in the contract pending stronger proof review.
