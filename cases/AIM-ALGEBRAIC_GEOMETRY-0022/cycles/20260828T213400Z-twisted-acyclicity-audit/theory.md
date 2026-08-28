# Twisting invalidates an Euler-only immaculate test

## Scope and changed evidence

The parent cycle `20260827T193500Z-orthogonality-direction` checked Hom variance
and the immaculate locus on products of projective spaces. This cycle keeps the
same total-cohomology question but tests a nontrivial P1-bundle: the Hirzebruch
surface F_n. It does not construct a mirror or alter the imported statement.
Selection is queue rank 12 after ranks 1–11 were excluded by cooldown.

Two exact failures distinguish the twisted case from the earlier product:

- On F2, O(S) has (h0,h1,h2)=(1,1,0), although chi=0. The H0 character is
  (0,0); an H1 character is (-1,-1). Both carry explicit non-boundary cocycles.
- On F2, O(S-F) has (0,2,0), whereas the same coordinates on F0 give (0,0,0).
  A base-coordinate b=-1 is not by itself sufficient after twisting.

The replacement is a precise locus for this family, not more product cases.
An additional source-level discrepancy is audited below. These are known
algebraic-geometry calculations and regression certificates, not novelty claims.

## Definitions and quantifiers

Let k be a characteristic-zero field, n>=0 an integer, and
F_n=P(O_P1 plus O_P1(n)) in the quotient convention. Let F be a fibre and S
the negative section, so S^2=-n, S.F=1, F^2=0. The relative hyperplane is
H=S+nF. For arbitrary integers a,b let L=O(aS+bF). Immaculate means H^q(L)=0
for every q, including q=0. The Euler characteristic is h0-h1+h2; its vanishing
is only necessary. The fan is fixed by rays (0,1),(1,0),(0,-1),(-1,n), with
consecutive maximal cones and divisor coefficients (a,b,0,0).

The finite domain is n=0,...,6, a=-4,...,4, b=-14,...,14. Additional explicit
controls are listed in the outputs, including (n,a,b)=(2,-1,100). Rational
matrix ranks test characteristic zero; no positive-characteristic claim is
inferred from those ranks. Universal geometric arguments remain ordinary
derivations pending independent proof review.

## Approach A: projection, splitting and duality

For a>=0, projection to P1 has no higher direct image and
pi_*L = direct sum for j=0,...,a of O_P1(b-jn).
Indeed L=O_P(E)(a) tensor pi^*O(b-an), and Sym^a(O plus O(n)) splits into
degrees 0,n,...,an. Reindexing gives the formula. The projective-bundle and P1
cohomology formulas are the dependencies in Stacks tag 01XS. Leray gives

h0 = sum_j max(b-jn+1,0),
h1 = sum_j max(-b+jn-1,0), h2=0.

For a=-1 all derived direct images vanish. For a<=-2 use
K=-2S-(n+2)F and Serre duality: hq(a,b)=h_(2-q)(-a-2,-b-n-2).
This yields the complete proposed immaculate locus:

- n=0: a=-1 or b=-1;
- n>0: a=-1, or (a,b)=(0,-1), or (a,b)=(-2,-n-1).

For a>=0 all summands must have degree -1, since dimensions cannot cancel
within a cohomological degree. If n>0 and a>=1 their degrees differ, so this
is impossible. The dual range gives the second isolated point. This is an
ordinary universal proof, not a conclusion drawn from the finite census.

The index calculation using the intersection numbers gives
chi=(a+1)(b+1-na/2). Its two zero loci are a=-1 and 2b+2=na. For n>0,
the latter usually consists of false acceptances. In the range a>=0 and
2b+2=na, put m=floor(a/2). If a=2m, h0=h1=n*m*(m+1)/2. If a=2m+1,
integrality requires n even and h0=h1=n*(m+1)^2/2. The a<=-2 range is dual.
Thus Euler zero becomes sufficient on F0, but not on a general F_n.

## Approach B: toric affine-cover cochains

At character (x,y), let N be the rays where the section inequality fails:
y+a<0, x+b<0, -y<0, -x+ny<0, respectively. A face of the four-chart Cech
complex is allowed when the rays common to its charts avoid N. The verifier
constructs all 16 possible signed incidence complexes over Q. Only N empty,
N all, and the two opposite pairs have cohomology, in degrees 0,2,1,1.
For these four patterns both x and y are bounded by the defining inequalities.
The other patterns are acyclic regardless of the magnitude of the character.
This eliminates an arbitrary weight-box cutoff.

For the F2 O(S) H1 class, N={1,3}. C0 is zero and C1 has faces
(0,2),(0,3),(1,2),(1,3). The vector (1,1,1,1) is closed; with C0=0 it cannot
be a boundary. The H0 class at (0,0) is the constant vector on all four charts.
Eight bundle certificates retain 26 such class vectors and their weights.
The independent lane checks closure and rank modulo boundaries, not just counts.

## Source boundary discovered during citation checking

In Hochenegger v4, Example 4.6, the last displayed immaculate entry is
O((n-2)F-2C_+). Example 2.7 identifies this same divisor as K. Our F2 calculation
gives H2(K)=k, not zero; K+F is the adjacent immaculate bundle. The proposed
coefficient repair is n-1 rather than n-2. Both PDF text and HTML show the
discrepancy. This is a literal source-level objection requiring human review,
not an assertion about the paper's main theorem or an upstream status change.

For every n in the frozen domain, the canonical character (n+1,1) violates
all four ray inequalities. In degree two, order the chart triples
012,013,023,123. A cocycle is v=(1,1,0,0). The incoming boundary columns are
(-1,0,1,0) and (0,1,0,-1); the outgoing row is (-1,1,-1,1).
The functional lambda=(1,0,1,0) kills both boundaries and has lambda(v)=1.
This is an exact non-boundary certificate. A separate literal checker verifies
seven such certificates and rejects four specified corruptions.

## Typed claims and falsifiers

- EULER — FALSIFIED, DERIVED shortcut: chi=0 implies immaculate on all F_n.
  The exact (n,a,b)=(2,1,0) certificate refutes it. A wrong fan/divisor
  identification, cocycle or quotient rank would defeat the witness.
- BASE-WINDOW — FALSIFIED, DERIVED shortcut: b=-1 suffices on every F_n.
  O(S-F) on F2 has h1=2. A failed projection or Cech calculation falsifies it.
- LOCUS — UNVERIFIED, DERIVED: the all-integer locus and index-zero dimensions
  above. Falsify with a missing summand, duality shift or Cech/geometric bridge.
- FINITE — EXPERIMENTALLY_SUPPORTED, DERIVED: 1,827 cases, 36,841 nonzero
  character classes, 223 immaculate cases, 27 Euler false acceptances, and 42
  b=-1 false acceptances. Falsify by an omitted tuple or mismatched row digest.
- CERTIFICATES — EXPERIMENTALLY_SUPPORTED, DERIVED: eight bundles/26 class
  vectors and seven canonical non-boundaries check; seven plus four corruptions
  fail. Falsify by a failed vector equation or accepted specified corruption.
- SOURCE — PRIMARY_SOURCE_SUPPORTED, PRIMARY_SOURCE: the versioned text has
  the displayed entry and canonical-divisor identification. Falsify by a wrong
  locator, transcription or convention. The geometric correction is our
  derivation, not a claimed author-issued erratum.

The source's general toric, Ulrich and mirror results are not audited wholesale.
No actual symplectic object or equivalence is constructed. The universal
classification and source correction need independently authored or kernel
review. More values of n,a,b alone would not be material progress; rotate.
