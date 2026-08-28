# Frobenius determinant audit

## Scope, definitions and quantifiers

This packet audits the numerical mechanism in the imported summary, not the
existence question in the frozen statement. Imported status is unchanged.
For each prime power q>1 and integer traces t_i of three elliptic curves,
write P_i(z)=z^2-t_i*z+q and let alpha_i,beta_i be its roots, counted with
multiplicity. Put N_i=q+1-t_i, R=product(q^2-r_1*r_2*r_3) over the eight
choices r_i in {alpha_i,beta_i}, and B=R*product(N_i^2).
The executable census uses only q=5,7,11 and traces witnessed by enumerated
nonsingular models y^2=x^3+a*x+b. It is not a census of isomorphism classes.

Let M_i=[[0,-q],[1,t_i]]. Define F_20 as the direct sum of the rank-eight
tensor M_1 tensor M_2 tensor M_3 and two copies of q*M_i for each i.
The standard geometric motivation is Kunneth applied to H^0,H^1,H^2 of
elliptic curves, of ranks 1,2,1 and Frobenius eigenvalues 1,{alpha,beta},q.
The six permutations of degrees (2,1,0) contribute twelve dimensions,
in addition to eight from (1,1,1). This external geometric identification
is not a new theorem established by the executable census.

## Two approaches

1. Power sums: s_i(0)=2, s_i(1)=t_i,
   s_i(k)=t_i*s_i(k-1)-q*s_i(k-2). The eight eigenvalue power sums
   are product_i s_i(k); those of F_20 add 2*q^k*sum_i s_i(k).
   Newton identities construct exact characteristic polynomials and evaluate
   them at q^2. All divisions are checked for zero remainder.
2. Block determinants: det(q^2 I_2-q M_i)=q^3*N_i. Consequently
   D_20=det(q^2 I_20-F_20)=q^18*B.
   The separate verifier constructs matrices and uses fraction-free elimination.
   For the trace-zero branch, pairing opposite triple roots gives
   R=(q^4+q^3)^4=q^12(q+1)^4 and B=q^12(q+1)^10.

For every prime ell not dividing q, D_20 and B have the same ell-adic
valuation. Do not omit the characteristic exclusion: D_20 is not B as an
integer. A draft normalization q^12*B failed the verifier before theory
implementation; the corrected factor is q^18.

## Typed claims and changed evidence

- FINITE (DERIVED, EXPERIMENTALLY_SUPPORTED): 172 models, 906 unordered
  trace triples with repetition, and all three trace-zero rows agree between
  two implementations. Falsifier: one incorrect point count, omitted tuple,
  characteristic coefficient, determinant or normalization.
- OMIT (DERIVED, EXPERIMENTALLY_SUPPORTED): for E:y^2=x^3+1 over F_5,
  N=6 and t=0. R=316406250000 has v_2=4, whereas
  B=14762250000000000 and D_20 have v_2=10. Omitting the six
  (2,1,0) summands understates this determinant exponent by six.
  Falsifier: a differing count, decomposition or valuation. The imported B
  already includes those factors; this refutes an omission shortcut, not B.
- IDENTITY (DERIVED, UNVERIFIED by independent author/kernel): the displayed
  block determinant identity holds for all integer q,t_i. The block
  calculation is an ordinary proof, not inferred from the finite census.
  Falsifier: a failed block identity or wrong multiplicity.
- TRANSFER (IMPORTED_UNVERIFIED, UNVERIFIED): the claimed order bound for
  unramified cohomology has not been established here. Falsifier of the
  claimed bound: an actual geometric group with order exceeding it.
  A missing argument is not such a counterexample.

The concrete progress units are the exact omitted-summand counterexample,
the reproducible determinant census, and the specific transfer gap below.
These are calibration and audit of known ingredients, not novel geometry.

## What the determinant does and does not control

For a free Z_ell lattice T carrying this Frobenius, set A=1-q^-2 F.
If A is invertible over Q_ell, the exact sequence
0 -> T -> T tensor Q_ell -> T tensor Q_ell/Z_ell -> 0
identifies ker(A on the last term) with T/AT. Smith normal form then
gives order ell^v_ell(det A)=ell^v_ell(B), since det A=q^-22 B.
For actual Weil roots q>1, complex absolute values q^(3/2) exclude q^2
as an eigenvalue. This is an ordinary lattice argument requiring independent
proof review, and concerns this lattice's torsion invariants, not H^3_nr.

The primary-source dependency is recorded in sources/theory-source.md.
To transfer the determinant bound to H^3_nr, the available summary still
needs either a justified subquotient comparison to these invariants, or
control of the relevant integral cycle-class cokernel together with the
divisible part. Neither is present in the material checked here.
The source's rational vector-space information alone cannot fill an integral
saturation gap: multiplication by 7 on Z_7 is rationally invertible but
has cokernel Z/7. The verifier checks its reduction modulo 49 against the
unit-map control. This abstract example is not a cycle map of a variety.

No Frobenius determinant computed here is evidence that H^3_nr is nonzero.
No asserted vanishing for ell>=7 has been certified. In particular ell=p
is excluded throughout the lattice argument. The imported Fermat-model
identification itself was not checked; the explicit Weierstrass model above
suffices for the arithmetic witness.

## Reproduction

From the packet directory: python experiments/run.py replay.
Canonical input: input.json. Exact theory evidence:
experiments/theory.py and experiments/theory-output.json. Verification
uses distinct files. Source files, notes and outputs are covered by manifest.json.
