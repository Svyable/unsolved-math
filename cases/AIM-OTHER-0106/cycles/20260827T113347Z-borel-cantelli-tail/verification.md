# Counterexample-first independent-method audit

## Context and actual independence

The checker was authored from `input.json`, the frozen statement, and the raw
modular inequalities before the theory program existed. Its first successful
run is preserved as `verification-baseline.json` and `baseline-execution.json`.
It starts with q=2,3 dependence and ten boundary probes. The later certificate
acceptance mode consumes a proposed certificate but recomputes its values from
the input, without importing theory code or reading theory notes.

Method family: INDEPENDENT_IMPLEMENTATION. The verifier partitions every rational
discontinuity point and evaluates the defining modular inequality at each open
cell midpoint. Membership is constant on those cells. The theory lane instead
constructs numerator intervals and merges their sorted endpoints. The verifier's
joint event uses conjunction of direct membership; theory intersects intervals.
Both are exact, but both are by the same assistant and share Python Fraction,
input definitions, and endpoint geometry. Separate fresh -I subprocesses with
empty environments are execution independence, NOT independent model/human
reasoning or a formal kernel. No stronger independence claim is made.

## Counterexamples and boundaries first

The joint event for q=2,3 has measure 2/27 versus product 1/9, rejecting the
constructed independence shortcut. Boundary probes cover zero and saturated
radii, half-radius full measure despite excluded endpoints, strict endpoint
membership, integer centers, nonprimitive and negative q, q=0 rejection,
the m-th power convention, and the epsilon-zero harmonic obstruction.

The power-convention probe has error 1/8, m=2, and right-hand side 1/16.
Squared error 1/64 passes but unsquared error fails. It is realizable by the
two-row one-column matrix with both entries 1/32 and q=4, p=0, epsilon=1.
The harmonic probe checks one block only; the general failure of convergence
follows because every dyadic block has at least half a unit of mass.

## Computation and certificate audit

All 192 single-denominator/radius cases match min(1,2*delta). All 42 (R,K)
finite-union areas and first-moment quantities agree exactly, with zero
mismatches. The featured 297-interval cover is checked on the common partition
formed by the input event boundaries AND certificate endpoints, detecting
missing and spurious positive-length regions. Summing certificate intervals
also detects overlapping duplication. Isolated endpoints are intentionally
irrelevant to the Lebesgue-measure certificate; strictness has separate tests.

Seven actual certificate mutations are rejected: wrong finite area, zero
remainder, zero total bound, wrong first-moment prefix, deleted interval,
shortened interval, and a replaced joint measure that assumes independence.
There are no random trials or floating-point tolerance comparisons.

## Claim/proof-step checks

TAIL: The scalar radius is q^-3 in x-space, since the error is q^-2 in q*x.
Both signs of q generate the same intervals; all p with a positive-length
intersection are covered by 0<=p<=q. The integrand t^-2 decreases, so for
q>K its integral over [q-1,q] is at least q^-2. Sum to obtain the 2/K remainder.
The resulting bound lies below 9/20 while the specified baseline exceeds it.
This checks the analytic bridge separately from finite interval calculation;
it remains ordinary same-assistant proof review, not kernel acceptance.

AMBIENT: Conditional uniformity requires a nonzero integer coordinate and one
FULL unit interval; it does not justify a uniform statement on arbitrary
submanifold measures. Product structure holds across rows of Lebesgue measure.
The shell subtraction removes the zero vector and pairing has no fixed points.
The mean-value bound uses Q>=1; the integral tail needs R>=2 and epsilon>0.
Countability of exponent 1/j and bounded numerator multiplicity handle the two
quantifiers in the VWA definition. None of these infinite assertions is proved
by the 192 scalar tests. The line A(t)=(t,0) independently checks the ambient-to-
manifold gap via an exact common integer kernel, without a numerical experiment.

## Citation check

Method family: PRIMARY_SOURCE_AUDIT. Directly inspected printed pages 11–12 of
the AIM PDF in a fresh web read, then separately fetched the bytes and inspected
local pdftotext output. `sources.json` records its SHA-256 and the page locators.
The powered max-norm convention and the transition into Question 25 agree with
the frozen raw record. The 2004 document is not evidence of current problem
status; no modern literature-completeness claim is made. The imported summary
is never treated as a primary citation or independent verification.

## Reproduction and limitations

Run `python -I reproduce.py` in this directory; it regenerates deterministic
theory/verifier JSON and compares them with the preserved baseline. Runtime and
absolute interpreter paths in execution logs are environment-specific.
An initial baseline can be reconstructed with `python -I reproduce.py --baseline`;
do not overwrite sealed evidence in place when performing external review.
Use a disposable copy and compare output hashes.

Resource limits: 180 CPU seconds, 200 wall seconds per child, 512 MiB address
space, 16 MiB output-file limit. No experiment code accesses the network and no
secrets are passed; an OS-level network namespace was not created. Total initial
research children: three, followed by four verification-replay children (seven total).

Blocking objections: fragment needs human scope review; the analytic remainder
and general ambient argument are not kernel-accepted or independently authored;
no matrix-manifold extremality test or optimal infinite-tail value is provided.
