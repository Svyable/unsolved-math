# Independent action-count audit

## Fresh context and falsification first

`python -I verify.py` reads only `input.json`; it imports neither theory code nor
theory output. It begins by rejecting disconnected actions, nonbijective
generators, degree zero, invalid roots and nontransitive rooted encodings.
Both programs were authored by the same assistant. Independence is algorithmic
and fresh-process based, not independent human/model authorship or kernel review.

The specific quotient trap is real: for r=2,d=2 there are 3 labelled transitive
actions and 3 unbased classes, not 3/2. Division by d! is invalid because full
relabelling can fix an action. In contrast, every root-fixing orbit in the
enumeration has size (d-1)!, exactly as required for the based count.

## Methods distinct from the theory recurrence

1. Enumerate ordered permutation tuples. Union-find on generator edges tests
   connectedness/transitivity; deterministic breadth-first labelling from root 0
   identifies based action classes. This uses no recurrence for t_r(d).
2. Compute the formal power-series logarithm of
   A_r(z)=sum_(d>=0) (d!)^r*z^d/d! by truncated polynomial multiplication and
   log(1+x)=sum (-1)^(k+1)*x^k/k. Orbit decomposition gives
   a_r(d)=d*[z^d]log A_r(z). This independently checks all 50 table entries with
   exact fractions, including ranks/degrees outside explicit enumeration.

The exponential-series identity follows from decomposing labelled actions into
their orbits. It is a second arithmetic realization of the same combinatorial
structure, not a logically unrelated theorem. Direct action enumeration is the
separate finite check against a shared conceptual mistake.

## Exact results

Enumeration covers 23 rank/degree pairs: r=0 through degree 6, r=1 through 7,
r=2 through 6, and r=3 through 4. It examines all 553,385 tuples, including
nontransitive ones. Every rooted class has the predicted multiplicity. Ordered
canonical-inventory SHA-256 digests are retained in `verification-output.json`.

For F_2 the based counts at degrees 1..6 are 1,3,13,71,461,3447. Independently
computed unbased counts are 1,3,7,26,97,624; these confirm that based and unbased
counts differ. They are not silently equated in the universal bound.

Restricting the two generators to commute gives based counts 1,3,4,7,6,12,
agreeing with the sum-of-divisors formula for subgroups of Z^2. At degree 3,
this is strictly smaller than the free-group count 13. Extra relations must not
be ignored when claiming equality for a particular manifold group.

The finite enumeration and formal-log table agree on every overlapping entry.
After independent execution, the harness compares all 50 formal-log values and
all 23 enumerated transitive/based values with the theory output. The example
denominator is 3996 and the conditional ceiling is 134. An additional 1,010
balanced occupancy cases check ceiling arithmetic, including N=0 as a vacuous
boundary. These occupancy arrays are not geometric experiments.

## Citation and proof-step audit

The primary geodesics PDF, printed page 12, visibly places the selected sentence
at the end of Section 5.5 and its second fragment in the Section 5.6 heading.
Question 5.6.1 is separate. The packet does not replace the extraction with that
question or infer a current mathematical status from this historical survey.

Hatcher's Proposition 1.32 identifies cover degree with subgroup index, and
Theorem 1.38 distinguishes based covers/subgroups from unbased covers/conjugacy
classes under its local hypotheses. Smooth connected manifolds satisfy them.
The proof audit checks the root stabilizer, quotient-group preimages, cover
isomorphisms over the base, pullback metrics, geometric distinctness of lifts,
uniformity of D, and the finite versus infinite pigeonhole steps.

The refined denominator is justified under the stated hypotheses, but there is
no construction of uniformly bounded simple lifts. A simple lift need not
project simply. The general counting proof and cited topology are not accepted
by a formal kernel or independently human/model reviewed. No theorem about
existence of simple geodesics on the base manifold follows from this packet.
