# Integral effectivity audit

## Frozen scope and changed evidence

This follows `20260827T043400Z-index-effectivity-audit`; selection.json pins its cycle and manifest hashes. Rank 1 passed preflight after its 24-hour cooldown. The immutable imported passage is historical commentary, not a newly posed open question. No imported status is changed.

The earlier certificate used the disconnected finite etale scheme Spec(F4) disjoint union Spec(F8). Its limitation was failure of geometric integrality, not lack of smoothness or properness. This packet replaces that example with a fixed smooth projective geometrically integral curve. This is an assumption reduction in the repository's diagnostic, not mathematical novelty. It does not remove the crucial rational-connectedness objection.

## Definitions, quantifiers and assumptions

Over k=F2 let C be the projective zero scheme of
F=X^4+Y^4+Z^4+X^2Y^2+X^2Z^2+Y^2Z^2+XYZ(X+Y+Z).
For a closed point P, deg(P)=[k(P):k]. A zero-cycle is a finite integral linear combination of closed points; it is effective if every coefficient is nonnegative. Its degree is the corresponding weighted sum. The index is the positive gcd of degrees of all closed points. An effective degree-one cycle is a k-rational point; an integral degree-one cycle need not be effective.

The weakened universal implication under test is: for every smooth projective geometrically integral curve over a finite field, index one implies a rational point. The certificate below negates that implication. It says nothing about the narrower rationally connected class. Characteristic two is essential to the displayed identities. Field quotients must be genuine fields; the implementations check irreducibility of each modulus.

## Approaches considered

1. Continue the finite-etale degree-profile model. This is useful for index transport but cannot establish geometric integrality of the example. Retired for this target: more profile enumeration would not remove the obstruction.
2. Use a projective plane model, exact Jacobian ideal certificates on all charts, and explicit Frobenius orbits. This yields a geometric example with the required signed-cycle behavior. Searching only for singularities over small extensions would be insufficient, so it is replaced by polynomial unit identities.
3. As verification, reconstruct finite-field arithmetic with coefficient tuples and determine orbit degrees by first Frobenius fixation; recover chart certificates by polynomial division rather than using the proposed multipliers.

## Typed claims and certificates

POINTS [DERIVED; EXPERIMENTALLY_SUPPORTED]. All seven projective F2 points have F=1. Over extensions of degrees 1 through 6, the exact point counts are 0,14,24,14,0,38. The full point lists, not just counts, are stored. Falsified by any missing normalized point, wrong field reduction, orbit degree, or count.

For alpha^2+alpha+1=0 the point [1:0:alpha] has orbit [1:0:alpha], [1:0:alpha+1], of length 2. For beta^3+beta+1=0, [1:beta:beta^2] has the length-3 orbit encoded as (1,2,4), (1,4,6), (1,6,2). Integers encode polynomial coefficients in binary. Thus closed points P2,P3 have degrees 2,3 and deg(P3-P2)=1.

JACOBIAN [DERIVED; EXPERIMENTALLY_SUPPORTED]. On each of the three standard charts, with remaining coordinates u,v, set P=u^2+u and Q=v^2+v. The chart polynomial is
f=1+P^2+Q^2+PQ, with f_u=Q and f_v=P. The identity
1=f+Q f_u+(P+Q) f_v
holds in F2[u,v]. Three expanded certificates are in experiments/theory-details.json. Falsified by a nonzero coefficient residual, incorrect derivative, or omitted chart. This is an identity over the polynomial ring, not an extrapolation from the finite census.

GEOMETRY [DERIVED; UNVERIFIED by independent author or kernel]. The ordinary argument is:

1. The nonzero homogeneous quartic defines a projective plane curve; the displayed extension points ensure nonemptiness.
2. For any algebraic extension of F2, a common zero of f,f_u,f_v contradicts the unit identity. The affine hypersurface Jacobian criterion on all charts gives geometric smoothness.
3. Over an algebraic closure, two distinct positive-degree plane components intersect (the projective plane intersection theorem). At an intersection, a product equation and all its partials vanish. A repeated factor likewise gives singular points. Both contradict step 2, so the curve is geometrically integral.
4. The index divides 2 and 3, hence is 1. No effective degree-one cycle exists because there are no F2 points.
5. The smooth plane curve genus formula gives genus (4-1)(4-2)/2=3. In particular this curve is not rationally connected.

The certificates support the algebra in steps 2 and 4. The Jacobian criterion, plane intersection theorem, Frobenius/closed-point correspondence, and genus formula remain ordinary mathematical dependencies, without independent human/model or kernel review. A failure of any hypothesis or implication falsifies this inference.

SOURCE [PRIMARY_SOURCE; PRIMARY_SOURCE_SUPPORTED]. The model matches the known C2 in Castryck--Voight; see sources/source-audit.md for exact locator and attribution. This is not a discovery claim. Falsified by a model, characteristic, or locator mismatch.

## Material delta and limits

The concrete new evidence is a geometrically integral candidate with exact degree-2/degree-3 orbit certificates and three global-in-extension smoothness certificates, removing the disconnectedness limitation of the earlier diagnostic. The finite census is auxiliary and does not prove geometric integrality by itself. Neither Ax's hypersurface nor the Colliot-Thelene--Madore construction is reconstructed. No statement about rationally connected varieties, C_1^0, novelty, or resolution of the parent problem is claimed.

Reproduce from this directory: `python experiments/run.py baseline`, `python experiments/run.py theory`, `python experiments/run.py verify`, then `python experiments/run.py replay`. The recorded execution files are provenance from this run; regenerating them changes manifest-covered bytes.
