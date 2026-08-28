# Quartic eliminant: field and multiplicity boundary audit

## Frozen scope and definitions

The exact parent question and imported summary are in snapshot.json and selection.json.
Only the summary's final quartic-divisor subclaim is examined. The source already
specifies squarefree complex divisors: the shortcuts below are deliberately weakened
tests, NOT errors attributed to that wording. No surface is constructed, no camera
matrix is recovered, and no novelty or parent solution is claimed.

Let q=aX^4+bX^3Y+cX^2Y^2+dXY^3+eY^4 be nonzero. Its root divisor is on P^1(K),
with multiplicities over an algebraic closure. Equivalence means transport of that
divisor by PGL2(K), allowing arbitrary nonzero scalar multiplication of q.
Use unscaled coefficients and define

    I = 12ae - 3bd + c^2
    J = 72ace + 9bcd - 27ad^2 - 27b^2e - 2c^3
    D0 = (4I^3-J^2)/27
    E(q1,q2) = J(q1)^2 I(q2)^3 - J(q2)^2 I(q1)^3.

D0 is our normalization, not Fisher's genus-one discriminant Delta=16D0.
Only its nonvanishing is used for squarefreeness. No division by I or J is allowed.
The precise universal target is: for every pair of squarefree binary quartics over
C, E=0 iff their four-point divisors are PGL2(C)-equivalent. Its ordinary proof
below is not independently authored or kernel verified.

## Approach A: cross-ratio reduction and polynomial certificate

Normalize three distinct roots to infinity, 0 and 1. The remaining root is
t in C minus {0,1}, with q_t=XY(X-Y)(X-tY). Direct substitution gives
I(t)=t^2-t+1 and J(t)=(t+1)(2t-1)(t-2).
For all s,t the exact polynomial identity is

    J(s)^2 I(t)^3 - J(t)^2 I(s)^3
    = -27 (s-t)(s+t-1)(ts-1)((1-t)s-1)((t-1)s-t)(ts-t+1).

The theory implementation expands sparse bivariate integer coefficients, not
samples; theory-details.json records the resulting coefficients. For t not 0 or 1,
the six factors vanish exactly at t, 1-t, 1/t, 1/(1-t), t/(t-1), (t-1)/t.
Permuting the four roots gives these six cross-ratio values; the transformations
t -> 1-t and t -> 1/t generate them. Three distinct point images determine a
unique projectivity. Thus these values exhaust unordered-divisor equivalence.

Proof steps requiring ordinary mathematical review:

1. A nonzero squarefree binary quartic over C has four distinct projective roots.
2. Three-point normalization is invertible and leaves the fourth outside {0,1,infinity}.
3. Under coordinate substitution by M, I and J have determinant weights 4 and 6;
   under rescaling q by u, weights 2 and 3. Consequently independent changes to
   either input multiply both terms of E by the same nonzero factor.
4. The displayed coefficient identity reduces E=0 to the six cross-ratio values.
5. The permutation argument converts equality of unordered cross ratios to the
   required projectivity. It is NOT a surface-gluing argument.

At J=0, the harmonic orbit {-1,1/2,2} has size three, hence eight automorphisms.
At I=0, collisions also occur, but the polynomial test does not divide by I.
The squarefree control X^4+XY^3 has (I,J,D0)=(0,-27,-27). Rational normalized
parameters do not cover this exceptional complex orbit; the identity and ordinary
argument, not the rational census, address it.

## Approach B: field-blind or multiplicity-blind use (retired)

REAL certificate: q1=X^4+Y^4, q2=X^4-6X^2Y^2+Y^4. Their (I,J,D0) triples are
(12,0,256) and (48,0,16384), so both are squarefree and E=0. The first has no real
projective root. For the second, the four disjoint intervals (-3,-2),(-1,0),(0,1),
(2,3) each have a sign change. A degree-four polynomial has no additional roots;
neither quartic has a root at infinity. PGL2(R) preserves the number of real roots,
so the divisors are not real-projectively equivalent. Over C they are equivalent.

MULTIPLICITY certificate: X^4 and X^3Y both have I=J=D0=0 and E=0. Their
multiplicity partitions (4) and (3,1) differ, which an invertible projectivity cannot
change. Dropping squarefreeness makes the eliminant insufficient even over C.

These two exact certificates make the hypotheses actionable in a future test:
validate squarefreeness and state the ground field before interpreting E=0.

## Typed claims and falsifiers

- BOUNDARY [DERIVED, EXPERIMENTALLY_SUPPORTED]: the two certificates have the
  stated invariants, real-root counts and multiplicities. Falsified by any wrong
  coefficient, root count, projective infinity handling, or multiplicity computation.
- IDENTITY [DERIVED, EXPERIMENTALLY_SUPPORTED]: exact expansion equals the six-factor
  product; all 2,025 specified pairs yield 213 equivalent pairs and 888 projectivities.
  Falsified by any nonzero coefficient residual, omitted parameter, or direct-map mismatch.
- COMPLETENESS [DERIVED, UNVERIFIED]: the five-step ordinary argument establishes
  the stated squarefree-complex equivalence if all steps hold. Falsified by a
  squarefree complex pair with E=0 but no projectivity, or a normalization/weight gap.
- SOURCE [PRIMARY_SOURCE, PRIMARY_SOURCE_SUPPORTED]: Fisher's Section 2 supplies
  the chosen I,J convention and transformation weights, not silhouette realization.
  Falsified by a convention, field, or locator mismatch. See sources/source-audit.md.

## Evidence and delta

Before this packet the selected repository record contained an unverified summary,
not these executable field/multiplicity certificates or a discriminating cross-ratio
census. theory-output.json records the 45 parameters (reduced p/q, -6<=p<=6,
1<=q<=6, excluding 0 and 1), all ordered pairs, and map counts. The expansion and
sign-change certificate are in theory-details.json. These are bounded verification
of known invariant theory, not an improved vision algorithm or novel theorem.
