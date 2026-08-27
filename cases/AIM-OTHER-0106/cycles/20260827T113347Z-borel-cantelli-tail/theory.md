# Quantitative ambient tail audit

Agent output is unverified research assistance, not a mathematical result.
No novelty, parent-resolution, kernel, or independent human/model review claim.

## Frozen scope and source boundary

The original record is retained verbatim in `snapshot.json`; the imported summary
in `selection.json` is an unverified lead. The primary workshop document is dated
November 1, 2004. Printed pages 11–12 place the fragment across the end of the
equidistribution discussion and the setup for Diophantine analysis. The subsequent
numbered question is about matrix manifolds, not merely ambient measure. The
matrix convention raises the max-norm error to the power m. See
[AIM, section 5.1](https://aimath.org/WWN/measrigid/measrigid.pdf).
This cycle audits a clearly specified ambient special case, not that manifold question.

## Definitions, quantifiers, and assumptions

Let m,n be positive integers, epsilon>0, q a NONZERO integer n-vector,
Q=||q||_infinity, and A in the unit matrix cube [0,1]^(mn), with Lebesgue measure.
Write E_q(delta) for existence of p in Z^m with ||Aq-p||_infinity<delta.
The source-powered inequality uses delta=Q^(-(n+epsilon)/m), not Q^(-n-epsilon).
The tail is the union over Q>=R. Integer translates of the cube have the same
events. No independence between different q is assumed.

The executable specialization fixes m=n=epsilon=1. For positive integer q,
E_q consists, up to finitely many endpoints, of intervals centered at p/q with
radius 1/q^3. Negative q gives the SAME event, not a second independent event.
Let U(R,K) be the measure of the union for R<=q<=K, with 2<=R<=K.
All code arithmetic is rational. Strict inequalities at endpoints are tested
separately; adding/removing finitely many endpoints does not change measure.

## Approaches

1. Row-wise torus uniformity and a shell union bound give an explicit ambient
   remainder without counting each numerator separately.
2. Exact scalar interval merging accounts for overlapping numerator slabs;
   combine the finite union with the same analytic remainder. This is the
   selected discriminating certificate route.
3. Replacing a union with an independence product is a tempting but unsupported
   shortcut. The explicit q=2,3 counterexample retires it. It is a constructed
   test hypothesis, not a claim attributed to the source or imported summary.

## Analytic proof steps (ordinary derivation, not kernel-accepted)

P1. Fix one row, and choose a coordinate j with q_j!=0. Conditional on the other
row coordinates, q_j*a_j plus their fixed contribution traverses |q_j| complete
unit periods as a_j ranges over [0,1]. Thus its residue is uniform; the measure
within delta of an integer is min(1,2*delta). Fubini across the m independent ROW
coordinates gives measure(E_q(delta))=min(1,2*delta)^m. No gcd-one restriction
on q is needed. This independence is between coordinates, NOT denominator events.

P2. E_q=E_-q. The number of max-norm-shell representatives modulo sign is
((2Q+1)^n-(2Q-1)^n)/2 <= n*3^(n-1)*Q^(n-1), by the mean value theorem for t^n.
Therefore the tail on one unit matrix cube is at most
min(1, 2^m*n*3^(n-1)/(epsilon*(R-1)^epsilon)), for integer R>=2.
Here sum(Q^(-1-epsilon), Q>=R) <= integral(R-1,infinity,t^(-1-epsilon)dt).
The constant is explicit but not claimed optimal. A bounded matrix box is
covered by finitely many integer unit cubes, so multiply by their number.

P3. For fixed epsilon, the bound tends to zero, giving the null limsup. VWA
permits SOME epsilon; use the countable union of exponents 1/j, j>=1, choosing
1/j<epsilon. Fixed bounded A and fixed q admit finitely many p, so infinitely
many pairs require unbounded Q. At epsilon=0 the dyadic harmonic blocks are
each at least 1/2; the convergence argument fails. Divergence alone is not a
proof of a full-measure limsup.

P4. In the scalar specialization, for q>=2 the exact event measure is 2/q^2.
By subadditivity for the remaining infinite union,

    measure(tail R) <= min(1, U(R,K) + 2/K),

since sum(q^(-2),q>K) <= integral(K,infinity,t^(-2)dt)=1/K.
This is an infinite-tail upper bound, NOT the exact infinite-tail measure and
NOT a probabilistic independence estimate. The remainder proof is required;
finite enumeration alone is insufficient.

## Concrete changed evidence

For R=4,K=32, `theory-output.json` stores 297 merged rational intervals.
Their total length is

    284968313371778844546722106704309081947931 /
    752789659364709316726334427027022464000000.

Adding 1/16 gives the certified candidate upper bound

    332017667082073176842118008393497985947931 /
    752789659364709316726334427027022464000000 < 9/20.

The first-moment prefix plus the SAME remainder is
5928461642876288008045764061/10426193044147366466460480000 > 9/20.
Thus the exact union certifies a 9/20 threshold that this specified baseline
cannot certify. Approximate values 0.44105 vs 0.56861 are display only.
The integral-only baseline is 2/3. This is a known-method refinement, not a
best-known bound. Of the 42 frozen cases, 34 strictly improve the capped
first-moment baseline; none reverses the safe inequality.

For q=2 and q=3, the event masses are 1/2 and 2/9. Their intersection has
measure 2/27, whereas independence predicts 1/9. Endpoint partition and interval
intersection give the same exact counterexample.

## Claim map and falsifiers

- TAIL: the finite union certificate plus P4 beats 9/20 for the featured case.
  Falsified by a wrong interval, missing slab, wrong exact sum or invalid remainder.
- DEPENDENCE: the proposed denominator-event independence shortcut is false.
  Falsified as a counterexample by an incorrect joint/product calculation.
- AMBIENT: P1–P3 give the stated general ambient bound; an analytic derivation,
  not universally validated by the scalar finite tests. Failed Fubini hypotheses,
  normalization, shell count, or summation would invalidate it.
- SOURCE: the imported fragment omits the following numbered manifold question.
  Falsified by contradictory primary-page placement.

## Remaining gap

Ambient nullity cannot be restricted automatically to a lower-dimensional
manifold. For example the row A(t)=(t,0) has Aq=0 for q=(0,k), k>=1, so every
point of this line satisfies every positive-exponent VWA test. This elementary
obstruction does not decide nondegeneracy/extremality conditions. Human scope
review of the source fragment and genuinely independent proof review remain
necessary. Neither a new solution nor a mathematical status change is asserted.
