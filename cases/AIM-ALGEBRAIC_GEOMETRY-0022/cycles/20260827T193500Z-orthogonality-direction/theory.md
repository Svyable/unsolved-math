# Direction-sensitive immaculate-locus audit

This packet tests a bounded dictionary used in the imported proposal. It is
known-result calibration, not a new mirror-symmetry theorem or a parent-problem
solution. The exact AIM statement and imported status are unchanged.

## Definitions, quantifiers and assumptions

An immaculate line bundle L has H^q(X,L)=0 for every q, including q=0.
For invertible L, RHom(O,L)=RΓ(L), whereas RHom(L,O)=RΓ(L dual).
We work over a field on X=P2xP2, P1xP2 or (P1)^3 and write L=O(d1,...,dr).
The finite table includes every degree tuple in [-6,6]^r. Universal statements
below refer to arbitrary integer degrees on these fixed products only.

The standard affine cover has a weight subcomplex indexed by the negative
exponent support N. Its degree-q basis is the nonempty subsets S containing N
with |S|=q+1. Its differential is the usual signed inclusion. Product covers
give a tensor total complex, with the Leibniz sign determined by the
degrees of earlier factors. Affine-cover computation and the displayed
Hom identities are the bridge from finite algebra to geometry.

## Approaches

1. Use the closed projective-space cohomology window and binomial dimensions,
   then the product formula. This is the theory implementation.
2. Build exact Čech incidence matrices for every negative support and product
   support; check ranks and integer contracting homotopies. Count monomials
   recursively without binomial formulas. This is the verifier.
3. Ignore Hom direction or infer high-dimensional necessity from the
   two-dimensional collinearity example. Both shortcuts are rejected by the
   explicit product case; neither rejection contradicts the original wording.

## Typed claims and falsifiers

DIRECTION (FALSIFIED, DERIVED proposed shortcut): vanishing of RHom(O,L)
would be equivalent to vanishing of RHom(L,O). On P2xP2 take L=O(-1,0).
The first complex has zero cohomology, but the second has Betti vector
(3,0,0,0,0). The dual example reverses these conclusions. A wrong
Čech differential, monomial count or dualization would defeat the witness.

CENSUS (EXPERIMENTALLY_SUPPORTED, DERIVED): the two programs agree on all
2,535 degree tuples and both Hom directions. Exactly 940 tuples have different
vanishing answers in the two directions. A missing tuple or mismatched Betti
entry would falsify this finite claim.

CONTRACTION (EXPERIMENTALLY_SUPPORTED, DERIVED): all 28 support complexes
and 160 product-support complexes have the recorded Betti profiles. For all
22 nonempty proper supports, the stored integer matrices satisfy dh+hd=I.
An incorrect sign, matrix product or rank would falsify the relevant entry.

LOCUS (UNVERIFIED, DERIVED ordinary argument): on a product of positive-
dimensional projective spaces, O(d1,...,dr) is immaculate exactly when at least
one coordinate lies in [-ni,-1]. This argument is not independently authored
or kernel accepted. Failure of the affine-cover computation, contraction or
product cohomology identification would defeat it.

SOURCE (PRIMARY_SOURCE_SUPPORTED, PRIMARY_SOURCE): Stacks 01XS gives the
projective-space cohomology formula. Borisov–Duncan v2 gives a characteristic-
zero forbidden-cone criterion, not a mirror identification. Wrong hypotheses
or conflating their theorem with the AIM mirror question would defeat this
restricted citation claim.

## Ordinary derivation and finite certificates

For a nonempty proper negative support N, choose a vertex v outside N.
The degree-minus-one map removes v when present and is zero otherwise,
with sign equal to its position among the ordered vertices.
Since N is nonempty, removal never creates an illegal empty face. The usual
insertion/removal cancellation gives dh+hd=I. The verifier stores these
matrices and checks the identity over the integers for n=1,2,3. This handles
mixed-sign weights of arbitrarily large magnitude, not just a truncated box.

Empty negative support contributes one class in degree zero. Full negative
support contributes one class in degree n. Counting nonnegative exponent
vectors of total d gives binomial(d+n,n); counting strictly negative vectors
gives binomial(-d-1,n). Thus O(d) has no cohomology for -n<=d<=-1, and otherwise
has exactly one nonzero cohomological degree. Tensoring over a field yields
the stated product locus. The universal bridge remains an ordinary proof;
the finite computations do not constitute kernel acceptance.

In the tested box, the immaculate counts are 48 on P2xP2, 37 on P1xP2, and
469 on (P1)^3. Of these, respectively 40, 33 and 397 cease to be immaculate
after dualization. Duality accounts for the other half of the 940 asymmetric
tuples. The tables retain every Betti vector, not just totals.

On P2xP2 the unrestricted immaculate locus consists of the four lattice lines
d1=-1,-2 or d2=-1,-2. Its six standard fan rays have no collinear pair: all 15
pairs have rank two, checked by minors in theory and row reduction in
verification. Thus collinear rays are not necessary in dimension four. This
does not contradict the statement's dimension-two example.

## Variance boundary

For a fully faithful covariant dg functor F, the condition transfers to
RHom(F(O),F(L))=0. If instead J is a fully faithful functor from the opposite
category, it transfers to RHom(J(L),J(O))=0. Reversing that order without
accounting for variance is the retired shortcut. We construct no CCC functor,
stopped cotangent brane or wrapped Floer complex. Those mirror statements
remain conditional and outside the finite audit.

## Reproduction and limitations

Use python experiments/run.py baseline, theory, verify and replay. Five
resource-limited mathematical child processes were used, including two for
replay. The wrapper is reused unchanged from rank 11; mathematical programs
are new. Both implementations share authorship and input conventions, not
code imports. No independent human/model or kernel review occurred.

The live AIM page was unavailable. The exact frozen statement, its
classification, the general fan criterion and its symplectic counterpart are
not reclassified by this packet. This is a reproducible direction and
cohomology-window calibration, with no novelty claim.
