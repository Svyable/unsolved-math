# Index one is not effectivity

Agent output is unverified research assistance, not a mathematical result.

## Frozen target and scope

The exact imported statement, including its extraction artifacts, is in
`snapshot.json`; selection and source hashes are in `selection.json`. This is the
first actual rank-1 selection after restoring the pinned dataset, not a provisional
choice. The imported status remains `open` with unverified trust. No status is changed.

One falsifiable target: does index one force a rational point for every nonempty
finite etale scheme over F2? This tests a tempting inference, not a claim that the
dataset authors made that inference. It is a small calibration tied to the selected
record's distinction between index and rational points. No novelty is asserted.

The selected paragraph is under remark (iv) following Question 11, not a standalone
question. Its retrospective context needs human scope review; see `sources.json`.
The present example does NOT address the rationally connected variety in that question.

## Definitions, quantifiers, assumptions

For a nonempty finite etale scheme X over a field k, write its closed points as
P_i with residue degrees d_i=[k(P_i):k]. Its index is gcd_i(d_i). A zero-cycle is
an integer combination of the P_i; its degree is sum_i n_i d_i. It is effective
when every n_i is nonnegative. A k-rational point is a closed point of degree one.
An effective cycle of degree one is therefore exactly one rational point.
Bezout gives an integer cycle of degree one when the index is one, but does not
give an effective cycle.

In the transport calculation ONLY, k is a finite field and X is nonempty finite
etale. For every integer m>=1, put k_m=F_(q^m), and g=gcd_i(d_i). Empty schemes,
inseparable algebras, arbitrary varieties and arbitrary fields are outside the
formula's domain. The explicit example takes q=2.

## Two approaches

1. Polynomial algebra and integer degrees: construct field factors with coprime
   degrees greater than one. This produces an exact certificate immediately.
2. Frobenius action on geometric points: count fixed points and orbit lengths,
   then apply the m-th power permutation after a finite-field extension. This
   supplies a structurally different verification algorithm and boundary probes.

Directly reconstructing Ax's hypersurface is deferred: it would require stronger
geometry and source checking than this bounded target. The finite scheme is not
a substitute for that construction.

## Typed claims and falsifiers

- C1, DERIVED / FALSIFIED: the universal implication index(X)=1 => X(F2) nonempty
  in the finite-etale domain. Certificate:
  X=Spec(F2[t]/(t^2+t+1)) disjoint union Spec(F2[t]/(t^3+t+1)).
  A root of either polynomial in F2, a factorization into smaller-degree factors,
  or failure of the signed degree calculation would defeat this certificate.
- C2, DERIVED / EXPERIMENTALLY_SUPPORTED: in the finite-field/finite-etale domain,
  index(X over k_m)=g/gcd(g,m). The derivation below is not kernel checked.
  Any mismatching Frobenius profile or invalid use of that domain falsifies it.
- C3, PRIMARY_SOURCE / PRIMARY_SOURCE_SUPPORTED: the imported passage is a
  historical remark adjoining Question 11, requiring scope review despite its
  imported open label. Incorrect primary-source placement defeats this claim.

## Exact certificate and derivation

Both displayed monic polynomials evaluate to 1 at 0 and 1. A degree-two or
degree-three polynomial over a field is reducible only if it has a linear factor.
They are thus irreducible; finite fields are perfect, so both factors are separable.
X has precisely two closed points, of degrees 2 and 3. Neither is rational, while
gcd(2,3)=1 and the signed cycle P_3-P_2 has degree 1. Its negative coefficient is
essential: 2a+3b=1 has no nonnegative integer solution. X is disconnected and not
geometrically integral; it must not be presented as a rationally connected example.

For transport, the geometric points of Spec(F_(q^d)) form a d-cycle under
Frobenius. Its m-th power has gcd(d,m) cycles each of length d/gcd(d,m).
Consequently the new index is gcd_i(d_i/gcd(d_i,m)). For every prime p, put
a_i=v_p(d_i), b=v_p(m). Its valuation is
min_i max(a_i-b,0)=max(min_i a_i-b,0), equal to v_p(g/gcd(g,m)). This proves the
integer identity within the stated model, pending independent proof/kernel review.
It implies the divisibilities index(X_km) | g | m*index(X_km).

## Evidence delta

`theory_check.py` and `theory-output.json` provide the explicit degree-one signed
certificate, absence of rational/effective degree-one points, and 21,828 bounded
profile/extension calculations. Profiles have 1..4 components, component degrees
1..12, and m=1..12. Finite testing is not a universal proof. This retires the
index-implies-point shortcut and identifies effectivity as the precise missing step.

Remaining: no kernel proof; no Ax construction audit; no result about the original
geometrically integral/rationally connected class. The primary-source audit is
about provenance and scope, not an autonomous resolution of any parent problem.
