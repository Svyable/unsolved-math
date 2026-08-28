# Verification from the frozen scalar input

## Independence and order

`verify.py` was authored and its baseline executed before `theory.py` was
authored. It reads only `input.json` in baseline mode, starts with the proposed
primitive-only shortcut and strict boundaries, and reconstructs each finite
union by all raw event endpoints. On every open atom it tests the literal
distance-to-integers inequality, not the reduced-union formula. The theory
instead constructs reduced centers, merges their intervals and factors integers
to compute totients. The verifier counts coprime residues directly.

The confirmation process recomputes that baseline before opening the theory
certificate, then compares every summary field and every center and span.
The canonical table files are separate and have equal SHA-256. Same assistant,
shared input, Python/Fraction runtime, and overlapping elementary proof ideas
remain limitations; this is algorithmic/process independence, not independent
human/model authorship or kernel verification.

## Counterexamples and boundaries first

At x=1/2, E_4 is true. Direct primitive search over q=4..128 finds no witness.
The odd/even argument in the theory note is required for all q; the finite
search does not prove the infinite exclusion. Separately, raw endpoint atoms
give U(4,4)=1/8 and primitive-only measure 1/16. Thus there is an actual
positive finite measure loss, not only the omission of a measure-zero point.

Seven controls check x=0, x=1, both strict E_4 boundaries 1/2+-1/64,
the interior point 1/2+1/128, absence of reduced denominator 3 at K=5,
and its entry at q=6. Ineligible remainder cases are represented by null,
not silently passed through the K>=max(6,2R-2) formula.

## Computation and certificate checks

21 (R,K) cases use 4,799 consecutive endpoint atoms. Raw and reduced membership
agree on every atom, and exact areas agree with interval merging. 128 direct
gcd counts verify phi(q)<=q*w(q) and the selected-prime inclusion-exclusion
weights. For R=4,K=32, all 325 reduced-center records and 297 merged spans
match the reconstruction. The prefix area equals the prior packet's area.

Seven altered packets are rejected: changed prefix area, changed remainder,
changed totient-case count, wrong first multiple, wrong radius, wrong merged
endpoint, and missing center. These controls test certificate validation,
not every possible implementation fault. Replays preserve both main output
hashes and both separately stored table hashes.

## Independent remainder envelope and proof-step audit

For each residue r mod 6 let a_r be its first integer greater than K. The
weight w is constant on that progression. Convexity of x^-2 gives

    1/(a_r+6j)^2 <= (1/6)*integral_[a_r+6j-3,a_r+6j+3] x^-2 dx.

For K>=6 all cells are positive. Summing nonnegative terms gives

    2*sum_{q>K} w(q)/q^2 <= C(K)
      = (1/3)*sum_{r=0}^5 w(a_r)/(a_r-3).

The verifier derives the six weights by counting residues coprime to
gcd(a_r,6), not by using signed divisor coefficients. At K=32,
C=7210711/175301280<=B=17333/403920. This independently supplies an
analytic envelope sufficient for the featured B certificate. It is not
a claim that C<=B for every K. The table records both bounds for eligible cases.

Audit findings: reducing p/q preserves centers; first multiples maximize
radii; d=1 needs both endpoints; q_d<=2R-2 covers exceptions; primitive
q>K centers are interior; countable subadditivity needs no independence;
the signed T decomposition is absolutely convergent; negative coefficients
require lower integral bounds; strict endpoints cannot be read literally
from merged closed-span certificates. No contradiction found in these steps.
These are ordinary same-author arguments, still pending independent proof review.

## Reproduction and diagnostics

From this packet: `python experiments/run.py baseline`, `theory`, `verify`,
and `replay`. The run used five mathematical child processes, with Python -I,
empty environments, 180-second CPU, 200-second wall and 512 MiB limits.
The runner provides process/resource isolation, not a network namespace.

Initial scripts had lint-only findings (pairwise iteration, condition ordering,
and line length). The exact initial sources are preserved as
`verify-prelint.py.txt` and `theory-prelint.py.txt`; the three initial execution
records hash those bytes. They remain executable with Python despite the .txt
suffix. The two replay records hash the final lint-clean .py sources. No math
output changed. Source-to-log hash matching includes these archived versions.

Source review is in a separate verification-source note. Its scope does not
verify present-day problem status or a matrix-manifold theorem. No newly
verified upstream status or parent solution is asserted.
